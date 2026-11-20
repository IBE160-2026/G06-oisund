"""Fictional progression controls with real private API and PostgreSQL."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi.testclient import TestClient
from psycopg.types.json import Jsonb

from app import position_coordinates
from app.private_storage import cleanup, database
from test_private_access import ORIGIN, headers, login, synthetic_only, users
from test_private_outcomes import closing, start
from test_private_selection import opened


DAY_A = '2026-11-02'
DAY_B = '2026-11-03'
EVIDENCE_A = DAY_A + 'T23:48:00+01:00'
EVIDENCE_B = DAY_B + 'T00:08:00+01:00'
COORD_REV = 'synthetic-coordinates-1'
QUAYS = ['NSR:Quay:900001', 'NSR:Quay:900002', 'NSR:Quay:900003']
PARENTS = ['NSR:StopPlace:900001', 'NSR:StopPlace:900002', 'NSR:StopPlace:900003']


def instant(value):
    return datetime.fromisoformat(value)


def frozen(activity, trip, service_date, positions, order):
    return {'activity_id': activity, 'decision_revision': 1, 'service_date': service_date,
            'journey_id': 'FIX:Journey:' + trip, 'line_id': 'FIX:Line:20', 'pattern_id': 'FIX:Pattern:' + trip,
            'status': 'compatible', 'start_position': positions[0], 'end_position': positions[-1],
            'position_coordinate_revision': COORD_REV, 'provenance': {'sha256': 'synthetic-r1'},
            'calls': [{'position': position, 'occurrence_id': f'{trip}-o{position}',
                       'scheduled_stop_point_id': f'FIX:ScheduledStopPoint:{trip}-{position}',
                       'stop_place_id': None, 'quay_id': QUAYS[item], 'name': f'Synthetic {item}',
                       'arrival': {'calendar_time': service_date + 'T20:00:00+01:00',
                                   'utc': service_date + 'T19:00:00+00:00'}}
                      for position, item in zip(positions, order, strict=True)]}


def synthetic_sidecar():
    validity = {'valid_from': '2026-11-01T00:00:00+01:00', 'valid_until': '2026-12-01T00:00:00+01:00'}
    return {'contract': position_coordinates.CONTRACT, 'revision': COORD_REV, 'provider': 'synthetic',
            'fetched_at': DAY_A + 'T00:00:00+01:00',
            'source_url': 'https://developer.entur.org/stop-places-v1-read/',
            'license_url': position_coordinates.LICENSE_URL,
            'stops': [{'quay_id': quay, 'stop_place_id': PARENTS[index], 'quay_version': '1', 'stop_place_version': '1',
                       'mapping_revision': 'synthetic-m1', 'coordinate_kind': 'Quay', 'crs': 'WGS84',
                       'latitude': 69 + index / 100, 'longitude': 18, 'quality': 'qualified',
                       'quay_validity': validity.copy(), 'stop_place_validity': validity.copy()}
                      for index, quay in enumerate(QUAYS)]}


def test_real_line20_coordinates_stay_manual_without_dated_quay_validity():
    activity = str(uuid4())
    ref = frozen(activity, 'pilot', '2026-11-23', [2, 3, 4], [0, 1, 2])
    ref['provenance']['sha256'] = position_coordinates.PILOT_ROUTE_SHA
    ref.pop('position_coordinate_revision')
    for call, quay in zip(ref['calls'], ('90847', '89699', '95924'), strict=True):
        call['quay_id'] = 'NSR:Quay:' + quay
    result = position_coordinates.view(ref, activity)
    assert result['reason'] is None and result['route']['compatible']
    assert result['source']['revision'] == position_coordinates.PILOT_REVISION
    assert all(call['coordinate_issue'] == 'validity-unknown' and call['coordinates'] is None for call in result['calls'])
    assert result['calls'][0]['stop_place_id'] == 'NSR:StopPlace:53331'
    ref['calls'][0]['stop_place_id'] = 'NSR:StopPlace:55'
    assert position_coordinates.view(ref, activity)['calls'][0]['coordinate_issue'] == 'mapping-unverified'
    ref['position_coordinate_revision'] = 'missing'
    assert position_coordinates.view(ref, activity)['calls'][0]['coordinate_issue'] == 'coordinate-version-missing'
    ref['calls'][0]['position'] = 3
    assert position_coordinates.view(ref, activity)['reason'] == 'range-invalid'


def test_dated_validity_and_exact_mapping_are_independent(monkeypatch):
    activity = str(uuid4())
    ref = frozen(activity, 'A', DAY_A, [2, 3, 4], [0, 1, 0])
    data = synthetic_sidecar()
    monkeypatch.setattr(position_coordinates, 'sidecar', lambda _: data)
    result = position_coordinates.view(ref, activity)
    assert [call['occurrence_id'] for call in result['calls']] == ['A-o2', 'A-o3', 'A-o4']
    assert all(call['coordinates'] for call in result['calls'])
    data['stops'][0]['quay_validity']['valid_until'] = DAY_A + 'T19:59:59+01:00'
    assert position_coordinates.view(ref, activity)['calls'][0]['coordinate_issue'] == 'validity-mismatch'
    data['stops'][1]['coordinate_kind'] = 'StopPlace'
    assert position_coordinates.view(ref, activity)['calls'][1]['coordinate_issue'] == 'mapping-unverified'
    ref['status'] = 'unverified'
    assert position_coordinates.view(ref, activity)['reason'] == 'route-incompatible'


def test_anchor_handoff_replay_competition_closure_and_expiry(users, monkeypatch):
    from app.private_main import app

    data = synthetic_sidecar()
    monkeypatch.setattr(position_coordinates, 'sidecar', lambda revision: data if revision == COORD_REV else None)
    administrator = TestClient(app, base_url=ORIGIN)
    stranger = TestClient(app, base_url=ORIGIN)
    _, plan = opened(administrator, users)
    workday = plan['id']
    activity_a, activity_b = [item['id'] for item in plan['draft']['activities'][:2]]
    ref_a, ref_b = (frozen(activity_a, 'A', DAY_A, [6, 7, 8], [2, 1, 0]),
                    frozen(activity_b, 'B', DAY_B, [3, 4, 5], [0, 1, 2]))
    with database() as conn:
        conn.execute('UPDATE workdays SET confirmed_at=%s WHERE id=%s', (instant(DAY_A + 'T11:00:00+01:00'), workday))
        for activity, reference in [(activity_a, ref_a), (activity_b, ref_b)]:
            conn.execute('INSERT INTO workday_route_references(workday_id,activity_id,reference) VALUES(%s,%s,%s)',
                         (workday, activity, Jsonb(reference)))
    base = '/workdays/' + workday
    anchor = base + '/position-anchor'

    def select(activity, revision):
        selected = administrator.post(base + '/selection', headers=proof, json={
            'operation_id': str(uuid4()), 'expected_revision': revision, 'activity_id': activity,
        })
        assert selected.status_code == 200, selected.text

    def command(activity, route, occurrence, revision, origin, at, **extra):
        return {'operation_id': str(uuid4()), 'expected_revision': revision, 'activity_id': activity,
                'route_basis': route, 'occurrence_id': occurrence, 'coordinate_revision': COORD_REV,
                'origin': origin, 'evidence_at': at, **extra}

    proof = headers(administrator)
    assert administrator.get(anchor).json()['anchor'] is None
    assert administrator.get(anchor).headers['cache-control'] == 'no-store'
    assert stranger.get(anchor).status_code == 401
    assert login(stranger, users, 1).status_code == 200
    assert stranger.get(anchor).status_code == 404
    assert stranger.get(base + '/position-coordinates/' + activity_a).status_code == 404
    first = administrator.get(base + '/position-coordinates/' + activity_a).json()
    assert first['route']['service_date'] == DAY_A and first['calls'][2]['coordinates']['revision'] == COORD_REV
    assert first['calls'][2]['stop_place_id'] == PARENTS[0]
    select(activity_a, 0)
    initial = command(activity_a, first['route']['basis'], 'A-o6', 0, 'manual', DAY_A + 'T23:44:00+01:00')
    assert administrator.post(anchor, json=initial).status_code == 403
    proof = headers(administrator)
    assert administrator.post(anchor, headers=proof, json=initial | {'latitude': 1}).status_code == 422
    assert administrator.post(anchor, headers=proof, json=initial | {'occurrence_id': 'A-o5'}).status_code == 422
    initial_reply = administrator.post(anchor, headers=proof, json=initial)
    assert initial_reply.status_code == 200, initial_reply.text
    progress = command(activity_a, first['route']['basis'], 'A-o7', 1, 'gps', DAY_A + 'T23:47:54+01:00')
    advance = administrator.post(anchor, headers=proof, json=progress)
    assert advance.status_code == 200, advance.text
    premature = command(activity_a, first['route']['basis'], 'A-o8', 2, 'gps', DAY_A + 'T23:47:59.999+01:00')
    premature_reply = administrator.post(anchor, headers=proof, json=premature)
    assert premature_reply.status_code == 429, premature_reply.text
    assert administrator.get(anchor).json()['revision'] == 2
    assert administrator.get(anchor + '/operations/' + premature['operation_id']).status_code == 404
    gps = command(activity_a, first['route']['basis'], 'A-o8', 2, 'gps', EVIDENCE_A)
    proposal = administrator.post(anchor, headers=proof, json=gps)
    assert proposal.status_code == 200, proposal.text
    lookup = anchor + '/operations/' + gps['operation_id']
    assert administrator.get(lookup).json() == proposal.json()
    assert stranger.get(lookup).status_code == 404
    assert administrator.post(anchor, headers=proof, json=gps).json() == proposal.json()
    assert administrator.post(anchor, headers=proof, json=gps | {'origin': 'manual'}).status_code == 409
    saved = administrator.get(anchor).json()
    assert saved['anchor']['quay_id'] == QUAYS[0]
    assert instant(saved['anchor']['evidence_at']) == instant(EVIDENCE_A)
    assert saved['anchor']['origin'] == 'gps' and saved['anchor']['asserted_at'] is None
    select(activity_b, 1)
    second = administrator.get(base + '/position-coordinates/' + activity_b).json()
    assert second['route']['service_date'] == DAY_B and second['calls'][0]['position'] == 3
    carry = command(activity_b, second['route']['basis'], 'B-o3', 3, 'manual', EVIDENCE_B, carried_from_revision=3)
    assert administrator.post(anchor, headers=proof, json=carry | {'occurrence_id': 'B-o4'}).status_code == 409
    carried = administrator.post(anchor, headers=proof, json=carry)
    assert carried.status_code == 200, carried.text
    latest = administrator.get(anchor).json()['anchor']
    assert latest['occurrence_id'] == 'B-o3' and latest['service_date'] == DAY_B
    assert latest['origin'] == 'manual' and instant(latest['asserted_at']) == instant(EVIDENCE_B)
    assert latest['carried_from']['origin'] == 'gps'
    assert instant(latest['carried_from']['evidence_at']) == instant(EVIDENCE_A)
    assert not {'latitude', 'longitude'} & latest.keys()

    def competitor(occurrence):
        return administrator.post(anchor, headers=proof, json=command(
            activity_b, second['route']['basis'], occurrence, 4, 'manual', DAY_B + 'T00:09:00+01:00'))

    with ThreadPoolExecutor(2) as workers:
        assert sorted(reply.status_code for reply in workers.map(competitor, ['B-o4', 'B-o5'])) == [200, 409]
    assert administrator.get(anchor).json()['revision'] == 5
    assert administrator.get(lookup).json() == proposal.json()

    start(administrator, plan)
    proof = headers(administrator)
    status_before = administrator.get(base + '/recap').json()
    closed = administrator.post(base + '/close', headers=proof, json=closing())
    assert closed.status_code == 200, closed.text
    after = administrator.get(anchor).json()
    assert after['terminal'] and instant(after['expires_at']) == instant(closed.json()['result']['expires_at'])
    assert instant(after['expires_at']) < instant(saved['expires_at'])
    assert administrator.get(base + '/recap').json()['outcomes']['outcomes'] == status_before['outcomes']['outcomes']
    assert administrator.get(lookup).json() == proposal.json()
    assert competitor('B-o3').status_code == 409
    with database() as conn:
        conn.execute('UPDATE workdays SET expires_at=clock_timestamp()-interval \'1 second\' WHERE id=%s', (workday,))
    assert administrator.get(anchor).status_code == 410
    assert administrator.get(lookup).status_code == 410
    cleanup()
    with database() as conn:
        for table in ('workday_position_anchors', 'workday_position_anchor_operations'):
            assert not conn.execute(f'SELECT 1 FROM {table} WHERE workday_id=%s', (workday,)).fetchone()
