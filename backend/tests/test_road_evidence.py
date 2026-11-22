from datetime import date
from hashlib import sha256
from io import BytesIO
import json
import signal
import sys
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit
from zipfile import ZipFile

import pytest

from app import road_evidence as evidence


def page(rows, total, cursor=None):
    metadata = {'antall': total, 'returnert': len(rows)}
    if cursor is not None:
        metadata['neste'] = {'start': cursor, 'href': 'https://example.invalid/outside-scope'}
    return {'metadata': metadata, 'objekter': rows}


def segment(sequence, reference=None):
    return {'veglenkesekvensid': sequence, 'referanse': reference or f'{sequence}-1-1',
            'veglenkenummer': 1, 'segmentnummer': 1}


def vehicle_object(type_id, *placements):
    return {'id': 700, 'metadata': {'type': {'id': type_id}, 'versjon': 2},
            'lokasjon': {'stedfestinger': placements}}


class Response(BytesIO):
    status = 200

    def __init__(self, document, content_length=None):
        self.raw = json.dumps(document).encode() if isinstance(document, dict) else document
        super().__init__(self.raw)
        self.headers = {'Content-Length': str(len(self.raw)) if content_length is None else content_length,
                        'Date': 'Fri, 20 Nov 2026 03:42:00 GMT', 'Age': '10'}


class Provider:
    def __init__(self, network=None, objects=None, failures=()):
        self.network = network if network is not None else {
            '': page([segment(10, '10-1-1')], 2, 'first:1'),
            'first:1': page([segment(20, '20-1-1')], 2, 'second:1'),
            'second:1': page([], 2, 'second:1'),
        }
        self.objects = objects or {}
        self.failures = iter(failures)
        self.urls = []
        self.returned_bytes = []

    def open(self, request, *, timeout):
        self.urls.append(request.full_url)
        assert timeout == 12
        failure = next(self.failures, None)
        if failure is not None:
            raise failure
        url = urlsplit(request.full_url)
        args = parse_qs(url.query)
        assert f'{url.scheme}://{url.netloc}' == evidence.BASE
        assert args['kommune'] == ['0301'] and args['veglenkesekvens'] == ['10,20']
        assert args['tidspunkt'] == ['2026-11-20'] and args['inkluderAntall'] == ['true']
        if url.path == evidence.NETWORK:
            assert args['srid'] == ['5973'] and args['trafikantgruppe'] == ['K']
            data = self.network[args.get('start', [''])[0]]
        else:
            type_id = int(url.path.removeprefix('/vegobjekter/api/v4/vegobjekter/'))
            assert type_id in evidence.OBJECT_TYPES
            assert args['inkluder'] == ['egenskaper,metadata,lokasjon']
            data = self.objects.get(type_id, page([], 0, '0:0'))
        result = data if isinstance(data, Response) else Response(data)
        self.returned_bytes.append(result.raw)
        return result


def acquire(provider, path):
    return evidence.collect('0301', (20, 10), date(2026, 11, 20), path, open_response=provider.open)


def test_complete_archive_preserves_original_pages_and_scoped_turns(tmp_path):
    limit = vehicle_object(105, {'veglenkesekvensid': 80}, {'veglenkesekvensid': 10})
    turn = vehicle_object(573, {'startpunkt': {'veglenkesekvensid': 80}, 'sluttpunkt': {'veglenkesekvensid': 20}})
    provider = Provider(objects={105: page([limit], 1), 573: page([turn], 1)})
    output = tmp_path / 'road.zip'
    output.write_bytes(b'previous evidence')
    receipt = acquire(provider, output)
    assert receipt['status'] == 'research' and receipt['missing_network_sequences'] == []
    assert receipt['counts'] == {'network': 2, **{str(i): int(i in (105, 573)) for i in evidence.OBJECT_TYPES}}
    assert receipt['attempts'] == 12
    assert receipt['raw_bytes'] == sum(map(len, provider.returned_bytes))
    with ZipFile(output) as archive:
        assert archive.testzip() is None
        assert json.loads(archive.read('receipt.json')) == receipt
        for details, raw in zip(receipt['pages'], provider.returned_bytes, strict=True):
            assert archive.read(details['file']) == raw
            assert details['sha256'] == sha256(raw).hexdigest() and details['bytes'] == len(raw)
            assert details['response_date'] and details['cache_age'] == '10'


def test_missing_network_sequence_stays_visible_in_research_receipt(tmp_path):
    result = acquire(Provider(network={'': page([segment(10, '10-1-1')], 1)}), tmp_path / 'road.zip')
    assert result['status'] == 'research'
    assert result['missing_network_sequences'] == [20]


@pytest.mark.parametrize(('network', 'match'), [
    ({'': page([segment(10)], 2)}, 'incomplete'),
    ({'': page([segment(10)], 2, 'a'), 'a': page([], 2, 'a')}, 'incomplete'),
    ({'': page([segment(10)], 2, 'a'), 'a': page([segment(20)], 3)}, 'count changed'),
    ({'': page([segment(10)], 2, 'a'), 'a': page([segment(10)], 2)}, 'duplicate'),
    ({'': page([segment(10)], 3, 'a'), 'a': page([segment(20)], 3, 'a')}, 'repeated'),
    ({'': page([segment(10)], 1, 'a'), 'a': page([], 1, 'b')}, 'unexpected cursor'),
    ({'': page([], 0, 'a')}, 'unexpected cursor'),
    ({'': {'metadata': {'antall': 0, 'returnert': 0, 'neste': {}}, 'objekter': []}}, 'invalid NVDB cursor'),
    ({'': page([segment(30)], 1)}, 'scoped'),
    ({'': page([segment(10, '20-1-1')], 1)}, 'scoped'),
    ({'': page([], 501)}, 'row budget'),
    ({'': {'metadata': {'totaltAntall': 0, 'returnert': 0}, 'objekter': []}}, 'invalid NVDB counts'),
    ({'': {'metadata': {'antall': 1, 'returnert': 0}, 'objekter': [segment(10)]}}, 'invalid NVDB counts'),
    ({'': Response(page([], 0), content_length='100000')}, 'length mismatch'),
    ({'': b'{broken'}, 'malformed JSON'),
    ({'': b'{"metadata":{"antall":1,"antall":0,"returnert":0},"objekter":[]}'}, 'duplicate JSON member'),
    ({'': b'{"metadata":{"antall":0,"returnert":0},"objekter":[],"other":NaN}'}, 'numeric constant'),
])
def test_incomplete_series_preserves_existing_archive_and_cleans_staging(tmp_path, network, match):
    output = tmp_path / 'road.zip'
    output.write_bytes(b'previous evidence')
    with pytest.raises(ValueError, match=match):
        acquire(Provider(network=network), output)
    assert output.read_bytes() == b'previous evidence'
    assert list(tmp_path.iterdir()) == [output]


@pytest.mark.parametrize(('document', 'match'), [
    (page([], 101), 'row budget'),
    (page([vehicle_object(573, {'veglenkesekvensid': 10})], 1), 'invalid NVDB object identity'),
    (page([vehicle_object(105, {'veglenkesekvensid': 80})], 1), 'no placement'),
])
def test_speed_objects_require_bounded_exact_scope(tmp_path, document, match):
    with pytest.raises(evidence.IncompleteEvidence, match=match):
        acquire(Provider(objects={105: document}), tmp_path / 'road.zip')
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize(('limit', 'value'), [('MAX_PAGE_BYTES', 50), ('MAX_TOTAL_BYTES', 200), ('MAX_ATTEMPTS', 3)])
def test_shared_budget_stops_the_collect_before_installation(monkeypatch, tmp_path, limit, value):
    monkeypatch.setattr(evidence, limit, value)
    outcome = tmp_path / 'road.zip'
    outcome.write_bytes(b'previous')
    with pytest.raises(evidence.IncompleteEvidence, match='budget'):
        acquire(Provider(), outcome)
    assert outcome.read_bytes() == b'previous'


def unavailable(code):
    return HTTPError(evidence.BASE, code, 'synthetic', {}, None)


def test_retry_is_bounded_and_charged_to_the_shared_attempt_budget(tmp_path):
    provider = Provider(failures=(TimeoutError(), unavailable(503)))
    result = acquire(provider, tmp_path / 'observed.zip')
    assert result['attempts'] == 14 and len(result['pages']) == 12
    assert provider.urls[:3] == [provider.urls[0]] * 3

    provider = Provider(failures=(unavailable(503), unavailable(502), unavailable(504)))
    with pytest.raises(evidence.IncompleteEvidence, match='HTTP 504'):
        acquire(provider, tmp_path / 'failed.zip')
    assert len(provider.urls) == 3 and not (tmp_path / 'failed.zip').exists()


def test_body_timeout_preserves_valid_archive_without_uncounted_retry(tmp_path):
    class TimedOut(Response):
        def read(self, _=-1):
            raise TimeoutError()

    provider = Provider(network={'': TimedOut(page([], 0))})
    output = tmp_path / 'road.zip'
    output.write_bytes(b'previous')
    with pytest.raises(evidence.IncompleteEvidence, match='response body could not be read'):
        acquire(provider, output)
    assert len(provider.urls) == 1
    assert output.read_bytes() == b'previous' and list(tmp_path.iterdir()) == [output]


@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='POSIX command deadline')
def test_deadline_removes_staging_and_restores_signal_handler(tmp_path):
    previous = signal.getsignal(signal.SIGALRM)

    def expiring_response(*args, **kwargs):
        signal.raise_signal(signal.SIGALRM)

    with pytest.raises(evidence.IncompleteEvidence, match='deadline exceeded'):
        evidence.collect('0301', (10, 20), date(2026, 11, 20), tmp_path / 'road.zip',
                         open_response=expiring_response, use_deadline=True)
    assert signal.getsignal(signal.SIGALRM) == previous and signal.alarm(0) == 0
    assert not list(tmp_path.iterdir())


def test_command_reports_missing_sequences(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(sys, 'argv', ['road_evidence', '--municipality', '0301', '--sequence', '10', '20',
                                     '--date', '2026-11-20', '--output', str(tmp_path / 'road.zip')])
    monkeypatch.setattr(evidence, 'collect', lambda *a, **k: {'attempts': 12, 'raw_bytes': 1,
                                                              'missing_network_sequences': [20]})
    evidence.main()
    assert 'Network sequences missing from NVDB: 20' in capsys.readouterr().out


def test_nontransient_http_error_and_rename_failure_leave_previous_bundle(monkeypatch, tmp_path):
    output = tmp_path / 'road.zip'
    output.write_bytes(b'previous')
    provider = Provider(failures=(unavailable(403),))
    with pytest.raises(evidence.IncompleteEvidence, match='HTTP 403'):
        acquire(provider, output)
    assert len(provider.urls) == 1

    def failed_replace(*_):
        raise OSError('synthetic rename failure')

    monkeypatch.setattr(evidence.os, 'replace', failed_replace)
    with pytest.raises(OSError, match='rename failure'):
        acquire(Provider(), output)
    assert output.read_bytes() == b'previous' and list(tmp_path.iterdir()) == [output]


@pytest.mark.parametrize('sequences', [(), (10, 10), (0,), ('10,20',)])
def test_invalid_scope_sends_no_request(tmp_path, sequences):
    provider = Provider()
    with pytest.raises(evidence.IncompleteEvidence, match='sequence IDs'):
        evidence.collect('0301', sequences, date(2026, 11, 20), tmp_path / 'road.zip', open_response=provider.open)
    assert not provider.urls and not list(tmp_path.iterdir())
