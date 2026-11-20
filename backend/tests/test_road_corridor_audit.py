from decimal import Decimal
from io import BytesIO
import json
import struct
import sys
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from app import road_corridor_audit as corridor
from test_road_evidence import Provider, acquire, page, vehicle_object


def edge(link, part, start, end, origin, destination, metres):
    return {'veglenkesekvensid': link, 'veglenkenummer': 1, 'segmentnummer': part,
            'referanse': f'{link}-1-{part}', 'startposisjon': start, 'sluttposisjon': end,
            'startnode': origin, 'sluttnode': destination, 'lengde': metres,
            'geometri': {'srid': 5973, 'wkt': 'LINESTRING Z (1 2 0, 3 4 0)'},
            'metadata': {'startdato': '2020-01-01'}, 'feltoversikt': ['1', '2']}


def scope_piece(occurrence, link, start, end, origin, destination):
    return {'occurrence': occurrence, 'link': link, 'start': start, 'end': end,
            'from_node': origin, 'to_node': destination}


def speed(identifier, link, start, end, value, fields):
    obj = vehicle_object(105, {'type': 'Linje', 'veglenkesekvensid': link, 'startposisjon': start,
                               'sluttposisjon': end, 'kjørefelt': fields, 'retning': 'MOT'})
    obj.update(id=identifier, egenskaper=[{'id': 2021, 'verdi': value}])
    return obj


@pytest.fixture
def inputs():
    network = [edge(10, 8, .75, 1, 'N', 'R', 7), edge(20, 2, 0, 1, 'J', 'F', 20),
               edge(10, 4, 0, .5, 'R', 'J', 12), edge(10, 9, .5, .75, 'P', 'N', 5)]
    scope = {'segments': [scope_piece(1, 10, .5, 1, 'P', 'R'), scope_piece(2, 10, 0, .5, 'R', 'J'),
                          scope_piece(3, 20, 0, 1, 'J', 'F')]}
    limits = [speed(901, 10, 0, 1, 70, []), speed(902, 20, 0, 1, 50, ['1']), speed(903, 20, 0, 1, 50, ['2'])]
    return network, scope, limits


def bundle(network, limits, tmp_path):
    output = tmp_path / 'road.zip'
    # Preserve the real provider's empty tails so the reader must verify closure.
    provider = Provider(network={'': page(network, len(network), 'tail'), 'tail': page([], len(network), 'tail')},
                        objects={105: page(limits, len(limits))})
    acquire(provider, output)
    return output.read_bytes()


def run_audit(inputs, tmp_path):
    network, scope, limits = inputs
    return corridor.audit(bundle(network, limits, tmp_path), json.dumps(scope).encode())


def test_rebuilds_resegmented_spans_and_wrap_with_exact_source_chainage(inputs, tmp_path):
    result = run_audit(inputs, tmp_path)
    assert result['status'] == 'research' and result['spans'] == 3 and result['length_m'] == '44'
    assert result['direct_general_segments'] == 3
    assert result['municipality'] == '0301' and result['archive_sequences'] == [10, 20]
    assert result['archive_observed_from'] <= result['archive_observed_through']
    segments = result['segments']
    assert [row['reference'] for row in segments] == ['10-1-9', '10-1-8', '10-1-4', '20-1-2']
    assert [row['chainage_m'] for row in segments] == ['0', '5', '12', '24']
    assert all(a['to_node'] == b['from_node'] for a, b in zip(segments, segments[1:]))
    assert segments[0]['speed']['records'][0]['orientation'] == 'MOT'
    assert segments[-1]['speed']['direct_gap'] and not segments[-1]['speed']['direct_conflict']
    assert [row['fields'] for row in segments[-1]['speed']['records']] == [['1'], ['2']]


def test_historical_internal_nodes_keep_changed_and_merged_boundaries_visible(inputs, tmp_path):
    inputs[1]['segments'] = [scope_piece(1, 10, .5, .625, 'P', 'M'), scope_piece(2, 10, .625, .75, 'M', 'OldN'),
                             scope_piece(3, 10, .75, 1, 'OldN', 'R'), scope_piece(4, 10, 0, .5, 'R', 'J'),
                             scope_piece(5, 20, 0, 1, 'J', 'F')]
    report = run_audit(inputs, tmp_path)
    assert report['spans'] == 3
    assert report['scope_intermediate_nodes'] == [
        {'span': 1, 'sequence': 10, 'position': '0.625', 'scope_node': 'M', 'archive_node': None},
        {'span': 1, 'sequence': 10, 'position': '0.75', 'scope_node': 'OldN', 'archive_node': 'N'},
    ]


def test_reused_source_segments_keep_separate_corridor_occurrences(tmp_path):
    network = [edge(10, 1, 0, 1, 'P', 'Q', 5), edge(20, 1, 0, 1, 'Q', 'P', 7)]
    scope = {'segments': [scope_piece(1, 10, 0, 1, 'P', 'Q'), scope_piece(2, 20, 0, 1, 'Q', 'P'),
                          scope_piece(3, 10, 0, 1, 'P', 'Q')]}
    result = run_audit((network, scope, []), tmp_path)
    assert [(row['occurrence'], row['reference'], row['chainage_m']) for row in result['segments']] == [
        (1, '10-1-1', '0'), (2, '20-1-1', '5'), (3, '10-1-1', '12'),
    ]


@pytest.mark.parametrize(('mutate', 'message'), [
    (lambda rows: rows.pop(0), 'endpoint mismatch'),
    (lambda rows: rows[0].update(startposisjon=.8), 'gap, overlap'),
    (lambda rows: rows[0].update(startposisjon=.7), 'gap, overlap'),
    (lambda rows: rows[0].update(startnode='unrelated'), 'node mismatch'),
    (lambda rows: rows[0].update(sluttnode='unrelated'), 'endpoint mismatch'),
    (lambda rows: rows[3].update(startposisjon=.4), 'gap, overlap'),
    (lambda rows: rows[0]['geometri'].update(srid=4326), 'geometry or metadata'),
    (lambda rows: rows[0]['geometri'].update(wkt='POLYGON EMPTY'), 'geometry or metadata'),
    (lambda rows: rows[0]['geometri'].update(wkt='LINESTRING (1 2)'), 'geometry or metadata'),
    (lambda rows: rows[0]['geometri'].update(wkt='LINESTRING Z (1 2 0, 3 4 NaN)'), 'geometry or metadata'),
    (lambda rows: rows[0]['metadata'].clear(), 'geometry or metadata'),
])
def test_no_partial_corridor_on_missing_changed_or_overlapping_source(inputs, tmp_path, mutate, message):
    mutate(inputs[0])
    with pytest.raises(corridor.InvalidEvidence, match=message):
        run_audit(inputs, tmp_path)


@pytest.mark.parametrize(('field', 'value', 'message'), [
    ('start', .1, 'sequence continuity'), ('from_node', 'Q', 'node continuity'), ('occurrence', 3, 'Unordered'),
])
def test_scope_rejects_unproven_wrap(inputs, tmp_path, field, value, message):
    inputs[1]['segments'][1][field] = value
    with pytest.raises(corridor.InvalidEvidence, match=message):
        run_audit(inputs, tmp_path)


@pytest.mark.parametrize(('limits', 'gap', 'conflict'), [
    ([(0, .5, 70), (.5, 1, 50)], False, False),
    ([(0, 1, 70), (.2, .7, 70)], False, False),
    ([(0, .8, 70), (.2, 1, 50)], False, True),
    ([(0, .5, 70), (.5000000001, 1, 50)], True, False),
    ([(0, .4, 70), (.2, .3, 50)], True, True),
])
def test_individual_speed_subintervals_distinguish_change_gap_and_conflict(limits, gap, conflict):
    segment = corridor.Span(10, Decimal(0), Decimal(1), 'P', 'Q')
    objects = [speed(900 + i, 10, start, end, value, []) for i, (start, end, value) in enumerate(limits)]
    observed = corridor.coverage(segment, corridor.speed_locations(corridor.decode(json.dumps(objects)))[10])
    assert observed['direct_gap'] is gap and observed['direct_conflict'] is conflict


def test_reports_exact_speed_overlap_and_original_placement_bounds():
    edge = corridor.Span(10, Decimal('.25'), Decimal('.8'), 'P', 'Q')
    objects = corridor.decode(json.dumps([speed(1, 10, 0, .45, 70, []), speed(2, 10, .4, 1, 50, [])]))
    report = corridor.coverage(edge, corridor.speed_locations(objects)[10])
    assert report['direct_intervals'] == [
        {'start': '0.25', 'end': '0.4', 'values_kmh': [70]},
        {'start': '0.4', 'end': '0.45', 'values_kmh': [50, 70]},
        {'start': '0.45', 'end': '0.8', 'values_kmh': [50]},
    ]
    assert [(r['source_start'], r['source_end'], r['start'], r['end']) for r in report['records']] == [
        ('0', '0.45', '0.25', '0.45'), ('0.4', '1', '0.4', '0.8'),
    ]


@pytest.mark.parametrize('fields', [None, '1', ['']])
def test_malformed_lane_metadata_does_not_supply_direct_coverage(inputs, tmp_path, fields):
    inputs[2][1]['lokasjon']['stedfestinger'][0]['kjørefelt'] = fields
    with pytest.raises(corridor.InvalidEvidence, match='Invalid placement'):
        run_audit(inputs, tmp_path)


def rewrite(raw, change):
    with ZipFile(BytesIO(raw)) as archive:
        pages = {name: archive.read(name) for name in archive.namelist() if name != 'receipt.json'}
        receipt = json.loads(archive.read('receipt.json'))
    change(pages, receipt)
    output = BytesIO()
    with ZipFile(output, 'w') as archive:
        archive.writestr('receipt.json', json.dumps(receipt))
        for name, body in pages.items():
            archive.writestr(name, body)
    return output.getvalue()


def drop_tail(pages, receipt):
    receipt['raw_bytes'] -= len(pages.pop('network-1.json'))
    receipt['pages'] = [row for row in receipt['pages'] if row['file'] != 'network-1.json']


@pytest.mark.parametrize(('change', 'message'), [
    (lambda pages, _: pages.update({'network-0.json': pages['network-0.json'] + b' '}), 'hash or byte tally'),
    (drop_tail, 'Incomplete archive series'),
    (lambda pages, _: pages.pop('105-0.json'), 'members disagree'),
    (lambda _, receipt: receipt['pages'][1].update(url=receipt['pages'][0]['url']), 'declared scope'),
    (lambda _, receipt: receipt.update(status='qualified'), 'research archive'),
])
def test_audit_revalidates_archive_integrity_and_page_continuation(inputs, tmp_path, change, message):
    network, scope, limits = inputs
    raw = bundle(network, limits, tmp_path)
    with pytest.raises(corridor.InvalidEvidence, match=message):
        corridor.audit(rewrite(raw, change), json.dumps(scope).encode())


def test_invalid_archive_cli_emits_diagnostic_without_partial_report(tmp_path, monkeypatch, capsys):
    data, scope = tmp_path / 'bad.zip', tmp_path / 'scope.json'
    data.write_bytes(b'not a zip')
    scope.write_text('{}')
    monkeypatch.setattr(sys, 'argv', ['road_corridor_audit', '--archive', str(data), '--scope', str(scope)])
    with pytest.raises(SystemExit) as result:
        corridor.main()
    output = capsys.readouterr()
    assert result.value.code == 1 and not output.out and 'Corridor audit incomplete' in output.err


def test_corrupt_deflate_member_has_a_controlled_cli_error(tmp_path, monkeypatch, capsys):
    data, scope = tmp_path / 'bad.zip', tmp_path / 'scope.json'
    raw = BytesIO()
    with ZipFile(raw, 'w', compression=ZIP_DEFLATED) as archive:
        archive.writestr('receipt.json', '{}')
        archive.writestr('network-0.json', '{}')
        info = archive.getinfo('receipt.json')
    broken = bytearray(raw.getvalue())
    name_length, extra_length = struct.unpack_from('<HH', broken, info.header_offset + 26)
    compressed_offset = info.header_offset + 30 + name_length + extra_length
    broken[compressed_offset] |= 7  # Deflate block type 3 is reserved.
    data.write_bytes(broken)
    scope.write_text('{}')
    monkeypatch.setattr(sys, 'argv', ['road_corridor_audit', '--archive', str(data), '--scope', str(scope)])
    with pytest.raises(SystemExit) as result:
        corridor.main()
    output = capsys.readouterr()
    assert result.value.code == 1 and not output.out and 'Corridor audit incomplete' in output.err
