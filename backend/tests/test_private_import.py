"""Independent fixture mapping and transient import boundaries; disposable data only."""
import asyncio
import copy
import json
import multiprocessing
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from threading import Event
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app import private_import
from app.draft_domain import DraftContent
from app.pdf_import import extract_pdf
from app.qualify_imports import ORACLE
from test_pdf_import import synthetic_pdf, synthetic_text_pdf


ADDITIONAL = json.loads((ORACLE.parent / 'import_additional_expected.json').read_text(encoding='utf-8-sig'))['fixtures']


def assert_additional(facts, number):
    expected = ADDITIONAL[number - 8]
    source = facts['import_metadata']
    assert len(facts['activities']) == len(expected['activities']) == {8: 23, 9: 8}[number]
    assert source['qualification'] == 'bounded-layout'
    assert source['unresolved'] == []
    header = source['header']
    assert header == dict(shift_id=f'9000000{number}', service_date=f'2030-01-{10 if number == 8 else 14}',
                         weekday='Thu' if number == 8 else 'Mon', department='Tromsø',
                         start='06:17' if number == 8 else '04:40', end='15:15' if number == 8 else '14:00',
                         origin='Garasje Gimle', destination='Garasje Gimle', work='8h28' if number == 8 else '9h20',
                         span='8h58' if number == 8 else '9h20', supplements=['25,00% 0h00' if number == 8 else '25,00% 1h20', '40,00% 0h00'],
                         pages=2 if number == 8 else 1, start_instant=f'2030-01-{10 if number == 8 else 14}T'+('06:17' if number == 8 else '04:40')+':00+01:00',
                         end_instant=f'2030-01-{10 if number == 8 else 14}T'+('15:15' if number == 8 else '14:00')+':00+01:00', end_day=0)
    for got, mapped, want in zip(source['activities'], facts['activities'], expected['activities']):
        assert {key: got[key] for key in want} == want
        for original, target in [('label', 'raw_code'), ('start', 'source_start'), ('end', 'source_end'), ('origin', 'from_place'), ('destination', 'to_place'), ('line', 'line'), ('trip_id', 'trip')]:
            assert mapped[target] == want[original]
        assert mapped['id'] == got['activity_id']
        for field in ('label', 'line', 'trip_id', 'origin', 'destination', 'start', 'end'):
            assert got['provenance'][field]
            assert all(point['page'] == 1 and point['column'] in (1, 2) and point['line'] > 0 for point in got['provenance'][field])
        for field in ('start_instant', 'end_instant'):
            assert got['provenance'][field]['derived_from'][0] == f'activities.{got["source_order"]}.{field.split("_")[0]}'
        for field in ('start', 'end'):
            assert mapped[field] == f'2030-01-{10 if number == 8 else 14}T{want[field]}:00+01:00'
    assert facts['physical_bus'] is None
    if number == 8:
        assert [(d['value'], d['suffix'], d['after_activity']) for d in source['duties']] == [('960181', '181', 1), ('960176', '176', 13), ('CAR - 1', None, 20)]
        assert [{key: d['provenance'][key] for key in ('page', 'column', 'line')} for d in source['duties']] == [dict(page=1, column=1, line=2), dict(page=1, column=1, line=49), dict(page=1, column=2, line=49)]
        assert [(c['from_activity_id'], c['vehicle_duty'], c['realtime_duty']) for c in facts['vehicle_duty_changes']] == [(facts['activities'][13]['id'], '960176', '176'), (facts['activities'][20]['id'], 'CAR - 1', None)]
        assert facts['activities'][20]['type'] == 'CAR'
        assert facts['activities'][21]['type'] == 'Tomkjøring med CAR'
        assert source['pause_groups'][0]['rows'] == [11, 12]
    else:
        assert [a['type'] for a in facts['activities']] == ['Sign-on', 'Fadder', 'Coffee', 'Fadder', 'Coffee', 'Fadder', 'Coffee', 'Instruktør']
        assert facts['vehicle_duty'] is facts['realtime_duty'] is None
        assert source['duties'] == []
        assert len(source['pause_groups']) == 3


@pytest.mark.parametrize('number', [8, 9])
def test_additional_approved_source_rows_and_meaning(number):
    import hashlib
    expected = ADDITIONAL[number - 8]
    data = (Path('/fixtures') / expected['file']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == expected['sha256']
    facts = private_import.interpret(extract_pdf(data)).model_dump(mode='json')
    assert_additional(facts, number)


@pytest.mark.parametrize('designation', ['CAR', 'CAR - 1', 'CAR - 2', 'CAR - 3', 'CAR - 4'])
def test_car_designations_have_no_numeric_suffix_and_end_at_next_duty(designation):
    from app.pdf_import import parse_document
    from test_pdf_import import pdf_bytes
    lines = [(810, 'Synthetic Employer - Origin Skift: CAR'), (790, 'Date: 01/01/2030 Tue Synthetic Driver'), (770, 'Division: Example'), (750, 'Skift start: 06:00 Origin Arb.tid: 0h10 Utstrekk: 0h10'), (738, 'Skift slutt: 06:10 Destination Tillegg: 25,00%0h00'), (720, 'Sign-on 06:00 06:01'), (705, 'Vogn '+designation), (690, 'CAR / 1 Origin 06:02'), (675, 'Origin 06:02'), (660, 'tom / 2 Origin 06:02'), (645, 'Destination 06:03'), (630, 'Vogn 960006'), (615, 'tom / 3 Destination 06:04'), (600, 'Origin 06:05'), (585, 'Sign-off 06:09 06:10')]
    content = '\n'.join(f'BT /F1 9 Tf 20 {y} Td ({text}) Tj ET' for y, text in lines).encode()
    data = pdf_bytes([b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Count 1 /Kids [3 0 R] >>', b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 841] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>', b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>', f'<< /Length {len(content)} >>\nstream\n'.encode()+content+b'\nendstream'])
    source = parse_document(data)
    assert source['unresolved'] == []
    assert source['duties'][0]['value'] == designation and source['duties'][0]['suffix'] is None
    assert [row['kind'] for row in source['activities']] == ['Sign-on', 'CAR', 'deadhead_car', 'deadhead', 'Sign-off']
    assert private_import.interpret(source).activities[2].type == 'Tomkjøring med CAR'


def test_unrecognized_vehicle_designation_stays_partial():
    from app.pdf_import import parse_document
    # A separate source row insertion avoids making assumptions about PDF offsets.
    from unittest.mock import patch
    import pdfplumber
    original = pdfplumber.page.CroppedPage.extract_text
    def unknown(page, *args, **kwargs):
        return original(page, *args, **kwargs).replace('Sign-on 06:00 06:01', 'Sign-on 06:00 06:01\nVogn UNKNOWN')
    with patch.object(pdfplumber.page.CroppedPage, 'extract_text', unknown):
        source = parse_document(synthetic_text_pdf())
    assert any(d['value'] == 'UNKNOWN' and d['suffix'] is None for d in source['duties'])
    assert private_import.interpret(source).import_metadata.qualification == 'partial'


@pytest.fixture(scope='module')
def mapped():
    expected = json.loads(ORACLE.read_text())['fixtures']
    return [(f, private_import.interpret(extract_pdf((Path('/fixtures') / f['file']).read_bytes())).model_dump(mode='json')) for f in expected]


def test_all_seven_independent_facts_and_provenance(mapped):
    for expected, draft in mapped:
        metadata = draft['import_metadata']
        assert draft['physical_bus'] is None
        assert len(draft['activities']) == len(expected['activities'])
        for source, row, want in zip(metadata['activities'], draft['activities'], expected['activities']):
            assert row['id'] == source['activity_id']
            for field, target in [('label', 'raw_code'), ('line', 'line'), ('trip_id', 'trip'), ('origin', 'from_place'), ('destination', 'to_place'), ('start', 'source_start'), ('end', 'source_end'), ('start_instant', 'start'), ('end_instant', 'end')]:
                clock = field.removesuffix('_instant')
                if field not in want.get('owner_fields', []) and clock not in want.get('owner_fields', []):
                    value = want[field] if not field.endswith('_instant') else (datetime.fromisoformat(expected['header']['service_date'] + 'T' + want[clock]) + timedelta(days=want[clock + '_day'])).replace(tzinfo=ZoneInfo('Europe/Oslo')).isoformat()
                    assert row[target] == value
            assert source['source_order'] == expected['activities'].index(want) + 1
            assert source['pages'] == want['pages']
            assert source['provenance']
        assert metadata['pause_groups'] == expected['pause_groups']
        assert all(metadata['header'][key] == value for key, value in expected['header'].items() if key not in ('driver', 'employer'))
        assert 'driver' not in metadata['header'] and 'employer' not in metadata['header']
        assert 'header_evidence' not in metadata and 'source_rows' not in metadata
        assert [d['value'] for d in metadata['duties']] == expected['duties']
        assert [d['after_activity'] for d in metadata['duties']] == expected['duty_after_activities']
        assert [d['suffix'] for d in metadata['duties']] == [d[-3:] for d in expected['duties']]
    partial = mapped[5][1]
    travel = partial['activities'][12]
    assert travel['raw_code'] == 'Travel to' and travel['source_end'] == '16:00'
    assert travel['start'] is travel['from_place'] is travel['to_place'] is travel['type'] is None
    assert partial['import_metadata']['qualification'] == 'partial'
    assert mapped[4][1]['import_metadata']['header']['end'] == '08:51'
    assert mapped[4][1]['activities'][-1]['source_end'] == '08:29'


def test_metadata_is_bounded_typed_and_legacy_shape_unchanged(mapped):
    assert DraftContent.model_validate({}).model_dump(mode='json') == {'service_date': None, 'vehicle_duty': None, 'realtime_duty': None, 'physical_bus': None, 'activities': []}
    for field in ['driver', 'employer', 'raw_text', 'filename']:
        bad = copy.deepcopy(mapped[0][1]); bad['import_metadata']['header'][field] = 'forbidden'
        with pytest.raises(ValidationError): DraftContent.model_validate(bad)
    bad = copy.deepcopy(mapped[0][1]); bad['import_metadata']['activities'][1]['activity_id'] = bad['activities'][0]['id']
    with pytest.raises(ValidationError): DraftContent.model_validate(bad)


def test_duty_changes_and_readable_uncertainties_survive_mapping(mapped):
    for expected, draft in mapped:
        previous = expected['duties'][0]
        wanted = []
        for duty, after in zip(expected['duties'], expected['duty_after_activities']):
            if duty != previous and after < len(draft['activities']):
                wanted.append({'from_activity_id': draft['activities'][after]['id'], 'vehicle_duty': duty, 'realtime_duty': duty[-3:]})
                previous = duty
        assert draft.get('vehicle_duty_changes', []) == wanted
    partial = mapped[5][1]['activities'][12]
    assert 'Kontroller start' in partial['uncertainty']
    assert 'Aktivitetstypen er uavklart' in partial['uncertainty']
    assert any('Kildemerket' in (row['uncertainty'] or '') for row in mapped[0][1]['activities'])


def test_duty_change_identity_suffix_and_explicit_empty_override(mapped):
    draft = copy.deepcopy(mapped[0][1])
    draft['vehicle_duty_changes'][0]['vehicle_duty'] = '960006'
    draft['vehicle_duty_changes'][0]['realtime_duty'] = '999'
    result = DraftContent.model_validate(draft).model_dump(mode='json')
    assert result['vehicle_duty_changes'][0]['realtime_duty'] == '006'
    result['vehicle_duty_changes'] = []
    assert DraftContent.model_validate(result).model_dump(mode='json')['vehicle_duty_changes'] == []
    result['vehicle_duty_changes'] = [{'from_activity_id': '00000000-0000-4000-8000-000000000000', 'vehicle_duty': None}]
    with pytest.raises(ValidationError): DraftContent.model_validate(result)
    change = copy.deepcopy(draft['vehicle_duty_changes'][0])
    draft['vehicle_duty_changes'] = [change, change]
    with pytest.raises(ValidationError): DraftContent.model_validate(draft)


@pytest.mark.parametrize('calendar', ['dst', 'extended_header'])
def test_unqualified_calendars_are_rejected(calendar):
    from app.pdf_import import ImportFailure
    data = synthetic_text_pdf()
    if calendar == 'dst': data = data.replace(b'01/01/2030', b'29/03/2026')
    source = extract_pdf(data)
    if calendar == 'extended_header': source['header']['start'] = '24:00'
    with pytest.raises(ImportFailure, match='unqualified_calendar'):
        private_import.interpret(source)


class FakeRequest:
    headers = {'content-type': 'application/pdf'}
    def __init__(self, data, disconnect=False): self.data, self.disconnect = data, disconnect
    async def stream(self):
        for i in range(0, len(self.data), 16384): yield self.data[i:i+16384]
    async def is_disconnected(self): return self.disconnect


def test_preview_success_failure_bounds_and_admission(monkeypatch):
    monkeypatch.setattr(private_import, 'authorize', lambda request: 'owner')
    good = asyncio.run(private_import.preview(FakeRequest(synthetic_text_pdf())))
    assert good.import_metadata and not private_import.active and not multiprocessing.active_children()
    for data, status in [(b'%PDF-broken', 422), (synthetic_pdf(), 422), (b'x' * (private_import.MAX_BYTES + 1), 413)]:
        with pytest.raises(HTTPException) as error: asyncio.run(private_import.preview(FakeRequest(data)))
        assert error.value.status_code == status
        assert not private_import.active and not multiprocessing.active_children()
    private_import.slots.acquire(); private_import.slots.acquire()
    try:
        with pytest.raises(HTTPException) as error: asyncio.run(private_import.preview(FakeRequest(b'%PDF-')))
        assert error.value.status_code == 429
    finally: private_import.slots.release(); private_import.slots.release()


def test_disconnect_task_cancellation_and_shutdown_release_worker(monkeypatch):
    monkeypatch.setattr(private_import, 'authorize', lambda request: 'owner')
    def slow(data, cancel):
        assert cancel.wait(5)
        from app.pdf_import import ImportFailure
        raise ImportFailure('cancelled')
    monkeypatch.setattr(private_import, 'extract_pdf', slow)
    async def exercise(kind):
        work = asyncio.create_task(private_import.preview(FakeRequest(b'%PDF-', disconnect=kind == 'disconnect')))
        await asyncio.sleep(.1)
        if kind == 'cancel': work.cancel()
        if kind == 'shutdown': await private_import.shutdown()
        with pytest.raises((HTTPException, asyncio.CancelledError)): await work
        assert not private_import.active
    for kind in ['disconnect', 'cancel', 'shutdown']: asyncio.run(exercise(kind))
    assert not multiprocessing.active_children()


def test_response_reauthorizes_after_processing(monkeypatch):
    calls = []
    def auth(request):
        calls.append(1)
        if len(calls) == 2: raise HTTPException(401, 'expired')
        return 'owner'
    monkeypatch.setattr(private_import, 'authorize', auth)
    with pytest.raises(HTTPException) as error: asyncio.run(private_import.preview(FakeRequest(synthetic_text_pdf())))
    assert error.value.status_code == 401 and len(calls) == 2
    assert not private_import.active and not multiprocessing.active_children()


def waiting_pdf_worker(data, connection):
    import time
    time.sleep(10)


def test_private_lifecycle_joins_real_spawned_process(monkeypatch):
    from app import pdf_import
    monkeypatch.setattr(private_import, 'authorize', lambda request: 'owner')
    monkeypatch.setattr(pdf_import, '_worker', waiting_pdf_worker)
    class DisconnectRequest(FakeRequest):
        async def is_disconnected(self):
            await asyncio.sleep(.2)
            return self.disconnect
    async def exercise(kind):
        work = asyncio.create_task(private_import.preview(DisconnectRequest(b'%PDF-', disconnect=kind == 'disconnect')))
        deadline = asyncio.get_running_loop().time() + 3
        while not multiprocessing.active_children():
            assert asyncio.get_running_loop().time() < deadline
            await asyncio.sleep(.01)
        assert multiprocessing.active_children()
        if kind == 'cancel': work.cancel()
        if kind == 'shutdown': await private_import.shutdown()
        with pytest.raises((HTTPException, asyncio.CancelledError)): await work
        assert not multiprocessing.active_children() and not private_import.active
    for kind in ['disconnect', 'cancel', 'shutdown']: asyncio.run(exercise(kind))


def test_stalled_upload_deadline_does_not_extract_and_reuses_slot(monkeypatch):
    monkeypatch.setattr(private_import, 'authorize', lambda request: 'owner')
    monkeypatch.setattr(private_import, 'UPLOAD_TIMEOUT', .02)
    calls = []
    from app.pdf_import import parse_document
    source = parse_document(synthetic_text_pdf())
    def extract(data, cancel):
        calls.append(data)
        return copy.deepcopy(source)
    monkeypatch.setattr(private_import, 'extract_pdf', extract)
    class StalledRequest(FakeRequest):
        async def stream(self):
            yield b'%PDF-'
            await asyncio.Event().wait()
    async def exercise():
        with pytest.raises(HTTPException) as error:
            await private_import.preview(StalledRequest(b''))
        assert error.value.status_code == 408 and calls == [] and not private_import.active
        assert (await private_import.preview(FakeRequest(b'%PDF-retry'))).import_metadata
        assert len(calls) == 1 and not private_import.active
    asyncio.run(exercise())


def test_overlapping_admission_repeated_cancellation_and_recovery(monkeypatch):
    monkeypatch.setattr(private_import, 'authorize', lambda request: 'owner')
    releases = [Event(), Event()]
    started = [Event(), Event()]
    cancels = [None, None]
    def extract(data, cancel):
        index = int(data[-1:])
        cancels[index] = cancel
        started[index].set()
        assert releases[index].wait(5)
        from app.pdf_import import ImportFailure
        raise ImportFailure('cancelled')
    monkeypatch.setattr(private_import, 'extract_pdf', extract)
    async def exercise():
        work = [asyncio.create_task(private_import.preview(FakeRequest(b'%PDF-' + str(i).encode()))) for i in range(2)]
        try:
            while not all(event.is_set() for event in started): await asyncio.sleep(.01)
            async def saturated():
                with pytest.raises(HTTPException) as error: await private_import.preview(FakeRequest(b'%PDF-2'))
                assert error.value.status_code == 429
            await saturated()
            work[0].cancel()
            while not cancels[0].is_set(): await asyncio.sleep(.01)
            work[0].cancel(); await asyncio.sleep(.02); work[0].cancel(); await asyncio.sleep(.02)
            assert not work[0].done() and len(private_import.active) == 2
            await saturated()
            releases[0].set()
            with pytest.raises(asyncio.CancelledError): await work[0]
            assert len(private_import.active) == 1
            from app.pdf_import import parse_document
            source = parse_document(synthetic_text_pdf())
            monkeypatch.setattr(private_import, 'extract_pdf', lambda data, cancel: copy.deepcopy(source))
            assert (await private_import.preview(FakeRequest(b'%PDF-recovered'))).import_metadata
            assert len(private_import.active) == 1
        finally:
            for task in work: task.cancel()
            for release in releases: release.set()
            await asyncio.gather(*work, return_exceptions=True)
        assert not private_import.active
    asyncio.run(exercise())
