"""Offline controls for the pinned manual stop mapping and historical pins."""
from collections import defaultdict
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from xml.etree import ElementTree as XML
from zipfile import ZipFile

import pytest

from app import automatic_notice_relevance as notices, draft_storage, position_coordinates as positions, route_source


TIMETABLE = 'troms-netex-1795129398375617.zip'
NSR_ARCHIVE = 'troms-nsr-1795125615869698.zip'
NSR_SHA = '2c224106067c28de88b6e67e04d3a33c527ae629ee6b3103dcb309e430d8427a'
NSR_MEMBER = 'tiamat-export-55_Troms-202611192300011691.xml'
OBSERVED_AT = '2026-11-20T01:13:54.5323574Z'
ARCHIVE_DIRS = (Path('/reference'), Path(__file__).resolve().parents[2] / '.private-runtime/route')


def archive_path(name):
    for folder in ARCHIVE_DIRS:
        path = folder / name
        if path.is_file():
            return path
    pytest.skip(f'Pinned public archive {name} is required for this offline control')


@pytest.fixture(scope='module')
def pilot_timetable():
    return route_source.load(archive_path(TIMETABLE), OBSERVED_AT)


def test_manual_pilot_coverage_matches_both_frozen_archives(pilot_timetable):
    expected = defaultdict(set)
    for date, day in pilot_timetable['days'].items():
        assert day['coverage'] == 'complete'
        assert len(day['journeys']) == route_source.EXPECTED[date]
        for journey in day['journeys'].values():
            for call in journey['calls']:
                expected[call['quay_id']].add(call['stop_place_id'])
    assert len(expected) == 120

    data = positions.sidecar(positions.PILOT_MANUAL_REVISION)
    records = {record['quay_id']: record for record in data['stops']}
    assert len(data['stops']) == len(records) == 120
    assert set(records) == set(expected)
    assert len({record['stop_place_id'] for record in records.values()}) == 82
    assert data['timetable']['sha256'] == pilot_timetable['provenance']['sha256']
    assert data['timetable']['generation'] == pilot_timetable['provenance']['generation']
    assert data['timetable']['observed_at'] == OBSERVED_AT
    assert data['fetched_at'] == '2026-11-20T01:14:33Z'
    assert data['license_url'] == positions.LICENSE_URL

    archive_file = archive_path(NSR_ARCHIVE)
    assert archive_file.stat().st_size == data['archive']['bytes'] == 1_980_625
    assert sha256(archive_file.read_bytes()).hexdigest() == data['archive']['sha256'] == NSR_SHA
    assert data['archive']['generation'] == '1795125615869698'
    assert data['archive']['url'] == ('https://storage.googleapis.com/marduk-production/tiamat/'
                                      '55_Troms_latest.zip?generation=1795125615869698')
    with ZipFile(archive_file) as archive:
        member, = archive.infolist()
        assert member.filename == data['archive']['member'] == NSR_MEMBER
        assert member.file_size == data['archive']['member_bytes'] == 31_423_981
        with archive.open(member) as xml:
            root = XML.parse(xml).getroot()

    ns = route_source.NS
    assert root.findtext('PublicationTimestamp', namespaces=ns) == data['archive']['publication_timestamp']
    found = set()
    for parent in root.findall('.//StopPlace', ns):
        for quay in parent.findall('quays/Quay', ns):
            quay_id = quay.get('id')
            if quay_id not in records:
                continue
            assert quay_id not in found
            found.add(quay_id)
            record = records[quay_id]
            assert record['stop_place_id'] == parent.get('id')
            assert expected[quay_id] <= {None, record['stop_place_id']}
            assert record['stop_place_version'] == parent.get('version')
            assert record['quay_version'] == quay.get('version')
            assert record['source_updated_at'] == quay.get('changed')
            assert record['stop_place_updated_at'] == parent.get('changed')
            for key in ('latitude', 'longitude'):
                assert record[key] == float(quay.findtext('Centroid/Location/' + key.title(), namespaces=ns))
            assert quay.find('ValidBetween', ns) is None
            assert record['quay_validity'] == {'valid_from': None, 'valid_until': None}
            assert record['stop_place_validity'] == {
                'valid_from': parent.findtext('ValidBetween/FromDate', namespaces=ns),
                'valid_until': parent.findtext('ValidBetween/ToDate', namespaces=ns),
            }
            assert record['quality'] == 'unverified'
    assert found == set(records)
    assert sum(quay.get('id') in records for quay in root.findall('.//Quay', ns)) == len(found)


def test_notice_pilot_stop_evidence_matches_dated_public_service(pilot_timetable):
    binding = notices.BINDING
    stop = binding['stop_review']
    assert binding['archive_sha256'] == pilot_timetable['provenance']['sha256']
    assert sha256(archive_path(NSR_ARCHIVE).read_bytes()).hexdigest() == stop['nsr_sha256']
    with ZipFile(archive_path(NSR_ARCHIVE)) as archive, archive.open(NSR_MEMBER) as xml:
        places = route_source.index(XML.parse(xml).getroot(), 'StopPlace')
    parent = places[stop['stop_place_ref']]
    assert parent.get('version') == '8'
    quays = set(route_source.index(parent, 'Quay'))
    assert all(call['quay_id'] not in quays for day in pilot_timetable['days'].values()
               for journey in day['journeys'].values() for call in journey['calls'])

    with ZipFile(archive_path(TIMETABLE)) as archive:
        shared = route_source.xml_member(archive, '_TRO_shared_data.xml')
        name, = [name for name in archive.namelist() if name.startswith('TRO_TRO-Line-1_24_')]
        line = route_source.xml_member(archive, name)
    assert list(route_source.index(line, 'Line')) == [stop['line_ref']]
    refs = {'TRO:ScheduledStopPoint:19021442_2': 'NSR:Quay:95718',
            'TRO:ScheduledStopPoint:19021442_4': 'NSR:Quay:95713'}
    assert set(refs.values()) <= quays
    for scheduled, quay in refs.items():
        assignment, = [item for item in route_source.nodes(shared, 'PassengerStopAssignment')
                       if route_source.ref(item, 'ScheduledStopPointRef') == scheduled]
        assert route_source.ref(assignment, 'QuayRef') == quay
    pattern_calls = {
        pattern: {call.get('id'): refs[scheduled]
                  for call in route_source.children(record, 'pointsInSequence/StopPointInJourneyPattern')
                  if (scheduled := route_source.ref(call, 'ScheduledStopPointRef')) in refs}
        for pattern, record in route_source.index(line, 'JourneyPattern').items()
    }
    dated_calls = defaultdict(set)
    journeys = [(journey, [ref.get('ref') for ref in route_source.children(journey, 'dayTypes/DayTypeRef')])
                for journey in route_source.nodes(line, 'ServiceJourney')]
    calendars = route_source.assigned_dates(shared, {key for _, day_types in journeys for key in day_types})
    for journey, day_types in journeys:
        calls = pattern_calls[route_source.ref(journey, 'JourneyPatternRef')]
        for call in route_source.children(journey, 'passingTimes/TimetabledPassingTime'):
            quay = calls.get(route_source.ref(call, 'StopPointInJourneyPatternRef'))
            clock = route_source.field(call, 'DepartureTime') or ''
            if quay and '06:00:00' <= clock < '22:00:00' and route_source.field(call, 'DepartureDayOffset') in (None, '0'):
                for day in {day for key in day_types for day in calendars[key]}:
                    dated_calls[day.isoformat()].add(quay)
    assert dated_calls == {date: set(refs.values()) for date in binding['dates']}


def reference_for(quay_id):
    return {
        'activity_id': 'control', 'status': 'compatible', 'decision_revision': 1, 'service_date': '2026-11-23',
        'journey_id': 'journey', 'pattern_id': 'pattern', 'line_id': route_source.LINE_ID,
        'provenance': {'sha256': positions.PILOT_ROUTE_SHA}, 'start_position': 1, 'end_position': 1,
        'calls': [{'position': 1, 'occurrence_id': 'stop', 'scheduled_stop_point_id': 'schedule',
                   'quay_id': quay_id, 'stop_place_id': None, 'departure': '2026-11-23T16:00:00+01:00'}],
    }


def test_packaged_manual_projection_resolves_every_quay():
    data = positions.sidecar(positions.PILOT_MANUAL_REVISION)
    reference = reference_for(data['stops'][0]['quay_id'])
    template = reference['calls'][0]
    reference.update(position_coordinate_revision=positions.PILOT_MANUAL_REVISION, end_position=120,
                     calls=[{**template, 'quay_id': record['quay_id'], 'position': number, 'occurrence_id': f'stop-{number}'}
                            for number, record in enumerate(data['stops'], 1)])
    view = positions.view(reference, 'control')
    assert view['route']['compatible']
    assert view['source']['revision'] == positions.PILOT_MANUAL_REVISION
    assert len({call['quay_id'] for call in view['calls']}) == 120
    for call, record in zip(view['calls'], data['stops'], strict=True):
        assert call['quay_id'] == record['quay_id'] and call['stop_place_id'] == record['stop_place_id']
        assert call['coordinates'] is None and call['coordinate_issue'] == 'validity-unknown'


def test_historical_v1_pins_and_explicit_null_keep_their_frozen_basis():
    reference = reference_for('NSR:Quay:90847')
    controls = [
        ({}, positions.PILOT_REVISION, 'NSR:StopPlace:53331'),
        ({'position_coordinate_revision': positions.PILOT_REVISION}, positions.PILOT_REVISION, 'NSR:StopPlace:53331'),
        ({'position_coordinate_revision': None}, None, None),
        ({'position_coordinate_revision': 'future-or-unknown'}, None, None),
    ]
    for pin, revision, parent in controls:
        saved = reference | pin
        original = deepcopy(saved)
        view = positions.view(saved, 'control')
        assert saved == original
        assert view['route']['basis'] == draft_storage.fingerprint('control', original)
        assert (view['source']['revision'] if view['source'] else None) == revision
        assert view['calls'][0]['stop_place_id'] == parent
        assert view['calls'][0]['coordinates'] is None

    new_quay = reference_for('NSR:Quay:92496')
    assert positions.view(new_quay, 'control')['calls'][0]['stop_place_id'] is None
    new_quay['position_coordinate_revision'] = None
    new_quay['calls'][0]['stop_place_id'] = 'NSR:StopPlace:54202'
    view = positions.view(new_quay, 'control')
    assert view['source'] is None
    assert view['calls'][0]['stop_place_id'] == 'NSR:StopPlace:54202'
    assert view['calls'][0]['coordinate_issue'] == 'coordinate-version-missing'


def test_historical_v2_read_does_not_consult_current_pilot_selection(monkeypatch):
    reference = reference_for('NSR:Quay:92496') | {'position_coordinate_revision': positions.PILOT_MANUAL_REVISION}
    monkeypatch.setattr(positions, 'current_pilot_revision', lambda: None)
    view = positions.view(reference, 'control')
    assert view['source']['revision'] == positions.PILOT_MANUAL_REVISION
    assert view['calls'][0]['stop_place_id'] == 'NSR:StopPlace:54202'


@pytest.mark.parametrize('actual_digest', [positions.PILOT_ROUTE_SHA, 'b' * 64])
def test_rechecked_timetable_can_only_use_a_frozen_explicit_v2_pin(actual_digest):
    original = reference_for('NSR:Quay:92496')
    rechecked = original | {'selection_mode': 'explicit', 'provenance': {
        'sha256': actual_digest, route_source.RECHECK_BASIS: positions.PILOT_ROUTE_SHA,
    }}
    saved = rechecked | {'position_coordinate_revision': positions.PILOT_MANUAL_REVISION}
    projection = positions.view(saved, 'control')
    assert projection['source']['revision'] == positions.PILOT_MANUAL_REVISION
    assert projection['route']['source_version'] == actual_digest
    assert projection['route']['basis'] == draft_storage.fingerprint('control', saved)
    assert projection['calls'][0]['stop_place_id'] == 'NSR:StopPlace:54202'
    assert projection['calls'][0]['coordinates'] is None
    assert projection['calls'][0]['coordinate_issue'] == 'validity-unknown'
    for missing_authority in (rechecked, rechecked | {'position_coordinate_revision': None},
                              saved | {'selection_mode': 'implicit'},
                              saved | {'position_coordinate_revision': positions.PILOT_REVISION}):
        view = positions.view(missing_authority, 'control')
        assert view['source'] is None and view['calls'][0]['stop_place_id'] is None
    assert positions.view(original, 'control')['source']['revision'] == positions.PILOT_REVISION


def test_mismatched_pilot_authority_cannot_supply_a_parent():
    reference = reference_for('NSR:Quay:92496')
    reference['position_coordinate_revision'] = positions.PILOT_MANUAL_REVISION
    call, = reference['calls']
    call['stop_place_id'] = 'NSR:StopPlace:1'
    assert positions.view(reference, 'control')['calls'][0]['coordinate_issue'] == 'mapping-unverified'
    assert positions.view(reference, 'control')['calls'][0]['stop_place_id'] is None
    for provenance in ({'sha256': 'a' * 64}, {'snapshot': positions.PILOT_ROUTE_SHA}):
        reference['provenance'] = provenance
        call['stop_place_id'] = 'NSR:StopPlace:54202'
        view = positions.view(reference, 'control')
        assert not positions.is_pilot_timetable(reference)
        assert view['source'] is None
        assert view['calls'][0]['stop_place_id'] is None
        assert view['calls'][0]['coordinate_issue'] == 'coordinate-version-missing'


def test_duplicate_or_malformed_manual_pack_cannot_replace_v1(tmp_path, monkeypatch):
    files = Path(positions.__file__).parent
    old = 'nsr_position_sidecar.json'
    new = 'nsr_position_sidecar_v2.json'
    (tmp_path / old).write_bytes((files / old).read_bytes())
    data = json.loads((files / new).read_bytes())
    data['stops'][-1] = data['stops'][0]
    monkeypatch.setattr(positions, '__file__', str(tmp_path / 'position_coordinates.py'))
    reference = reference_for('NSR:Quay:90847')
    reference['calls'][0]['stop_place_id'] = 'NSR:StopPlace:53331'
    try:
        for bad in (json.dumps(data).encode(), b'{', b' ' * 100_001):
            (tmp_path / new).write_bytes(bad)
            positions.sidecar.cache_clear()
            new_ref = reference | {'position_coordinate_revision': positions.PILOT_MANUAL_REVISION}
            view = positions.view(new_ref, 'control')
            assert positions.current_pilot_revision() == positions.PILOT_REVISION
            assert view['source'] is None
            assert view['calls'][0]['stop_place_id'] is None
            assert view['calls'][0]['coordinate_issue'] == 'coordinate-version-missing'
            old_view = positions.view(reference, 'control')
            assert old_view['source']['revision'] == positions.PILOT_REVISION
            assert old_view['calls'][0]['stop_place_id'] == 'NSR:StopPlace:53331'
        (tmp_path / old).unlink()
        positions.sidecar.cache_clear()
        assert positions.current_pilot_revision() is None
    finally:
        positions.sidecar.cache_clear()


def test_digest_accepted_duplicate_leaves_queried_quay_unavailable(tmp_path, monkeypatch):
    data = deepcopy(positions.sidecar(positions.PILOT_MANUAL_REVISION))
    queried = data['stops'][0]
    data['stops'][-1] = queried | {'stop_place_id': 'NSR:StopPlace:1'}
    raw = json.dumps(data).encode()
    (tmp_path / 'nsr_position_sidecar_v2.json').write_bytes(raw)
    monkeypatch.setattr(positions, '__file__', str(tmp_path / 'position_coordinates.py'))
    monkeypatch.setattr(positions, 'PILOT_MANUAL_SIDECAR_SHA', sha256(raw).hexdigest())
    positions.sidecar.cache_clear()
    try:
        assert positions.sidecar(positions.PILOT_MANUAL_REVISION) == data
        reference = reference_for(queried['quay_id']) | {'position_coordinate_revision': positions.PILOT_MANUAL_REVISION}
        reference['calls'][0]['stop_place_id'] = queried['stop_place_id']
        view = positions.view(reference, 'control')
        assert view['calls'][0]['coordinate_issue'] == 'coordinate-ambiguous'
        assert view['calls'][0]['stop_place_id'] is None
        assert view['calls'][0]['coordinates'] is None
    finally:
        positions.sidecar.cache_clear()
