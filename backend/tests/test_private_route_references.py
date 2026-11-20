"""Synthetic route controls against the private HTTP boundary and PostgreSQL."""

from contextlib import closing
from copy import deepcopy
from datetime import UTC, date, datetime, timedelta
import json
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
import pytest

from app import draft_storage, position_coordinates, road_reference_api, route_reference_storage, route_source
from app.private_storage import cleanup, database
from test_position_pilot_coverage import OBSERVED_AT, pilot_timetable
from test_private_access import headers, login, synthetic_only, users
from test_private_drafts import content, save
from test_private_workdays import confirm

DATE = date(2031, 1, 2)
JOURNEY = 'TRO:ServiceJourney:synthetic-outbound'
INBOUND = 'TRO:ServiceJourney:synthetic-inbound'
DIGEST = 'a' * 64
CHOICES = {
    'direction': {'mode': 'keep'},
    'destination': {'mode': 'manual', 'manual': 'Drivers display text'},
    'stops': {'mode': 'source'},
}


def instant(hour):
    return {'raw_time': f'{hour:02d}:00:00', 'raw_day_offset': None, 'day_offset': 0,
            'calendar_time': f'{DATE}T{hour:02d}:00:00+01:00', 'utc': f'{DATE}T{hour - 1:02d}:00:00+00:00'}


def call(position, name, quay, hour, arrival, departure, headsign):
    return {'position': position, 'occurrence_id': f'TRO:StopPointInJourneyPattern:synthetic-{position}',
            'scheduled_stop_point_id': f'TRO:ScheduledStopPoint:{name}', 'quay_id': f'NSR:Quay:{quay}',
            'stop_place_id': f'NSR:StopPlace:synthetic-{name}', 'name': name, 'headsign': headsign,
            'headsign_id': f'TRO:DestinationDisplay:{headsign}', 'boarding': departure, 'alighting': arrival,
            'arrival': instant(hour) if arrival else None, 'departure': instant(hour) if departure else None}


def journey(key, direction, calls):
    return {'service_date': DATE.isoformat(), 'line_id': route_source.LINE_ID, 'journey_id': key,
            'journey_version': '1', 'pattern_id': f'TRO:JourneyPattern:synthetic-{direction}',
            'pattern_version': '1', 'route_id': f'TRO:Route:synthetic-{direction}', 'direction': direction,
            'headsign': calls[0]['headsign'], 'calls': calls, 'calendar': {'day_type_ids': ['synthetic-date']},
            'private_code': '0007', 'operator_id': 'TRO:Operator:synthetic'}


@pytest.fixture
def fake(monkeypatch):
    out = journey(JOURNEY, 'outbound', [
        call(1, 'Start', 1001, 10, False, True, 'Central'),
        call(2, 'Centre', 1002, 10, True, True, 'Central'),
        call(3, 'Start', 1001, 10, True, True, 'Further'),
        call(4, 'End', 1003, 11, True, False, 'Further'),
    ])
    inbound = journey(INBOUND, 'inbound', [
        call(1, 'End', 1103, 12, False, True, 'West'),
        call(2, 'Centre', 1102, 12, True, True, 'North'),
        call(3, 'Start', 1101, 13, True, False, 'North'),
    ])
    day = {'coverage': 'complete', 'reasons': [], 'journeys': {JOURNEY: out, INBOUND: inbound}}
    evidence = {'days': {DATE: day}, 'provenance': {'sha256': DIGEST, 'provider': 'synthetic',
                'observed_at': datetime.now(UTC).isoformat(), 'generation': 'control', 'parser_revision': 1}}
    monkeypatch.setattr(route_source, 'DATES', (DATE,))
    monkeypatch.setattr(route_source, 'EXPECTED', {DATE: 2})
    monkeypatch.setattr(route_source, 'catalogue', evidence)
    # TestClient intentionally bypasses lifespan. This marker describes generated
    # fixtures only and may never load the pinned public archive into this case.
    from app.private_main import app
    client = TestClient(app)
    try:
        yield client, evidence
    finally:
        client.close()


def draft_for(client, *, start='10:00', end='11:00', origin='Start', destination='End'):
    facts = content()
    facts.update(service_date=DATE.isoformat(), physical_bus='1234')
    facts['activities'][0].update(type='trip', raw_code='Trip', line='20', trip='0007', direction='manual direction',
                                  start=f'{DATE}T{start}+01:00', end=f'{DATE}T{end}+01:00',
                                  from_place=origin, to_place=destination, uncertainty=None)
    response, _ = save(client, facts)
    assert response.status_code == 200
    return response.json()


def paths(draft):
    target = f"/drafts/{draft['id']}"
    activity = draft['draft']['activities'][0]['id']
    return (f"{target}/route-departures?revision={draft['revision']}&activity_id={activity}",
            target + '/route-references', activity)


def inspect_state(client, draft):
    _, path, _ = paths(draft)
    response = client.get(path, params={'revision': draft['revision']})
    assert response.status_code == 200
    return response.json()


def write_choice(client, draft, route_revision, *, start=3, end=4, digest=DIGEST, body=None):
    _, path, activity = paths(draft)
    body = body or {'operation_id': str(uuid4()), 'expected_draft_revision': draft['revision'],
                    'expected_route_revision': route_revision, 'activity_id': activity,
                    'selection': {'journey_id': JOURNEY, 'source_sha256': digest, 'start_position': start,
                                  'end_position': end, 'field_decisions': CHOICES}}
    return client.post(path, headers=headers(client), json=body), body


def review(client, draft, route_revision=None):
    payload = {'draft_id': draft['id'], 'expected_revision': draft['revision']}
    if route_revision is not None:
        payload['expected_route_revision'] = route_revision
    response = client.post('/workday-reviews', headers=headers(client), json=payload)
    if response.status_code != 200:
        return response, {}
    value = response.json()
    return response, {'operation_id': value['operation_id'], 'expected_revision': draft['revision'],
                      'acknowledgements': [item['id'] for item in value['unknowns']], 'classifications': {}}


def test_ordinary_repeated_variants_absence_and_outage(fake, users):
    client, evidence = fake
    assert login(client, users).status_code == 200
    draft = draft_for(client)
    query, _, _ = paths(draft)
    result = client.get(query).json()
    assert result['coverage'] == 'complete' and result['outcome'] == 'alternatives'
    out = next(item for item in result['journeys'] if item['journey_id'] == JOURNEY)
    assert out['matching_ranges'] == [[1, 4], [3, 4]]
    assert out['pattern_id'] == 'TRO:JourneyPattern:synthetic-outbound'
    assert inspect_state(client, draft)['references'] == []

    inbound_draft = draft_for(client, start='12:00', end='13:00', origin='End', destination='Start')
    inbound_query = paths(inbound_draft)[0]
    alternative = client.get(inbound_query).json()
    assert alternative['outcome'] == 'possible'
    detail = client.get(inbound_query + '&journey_id=' + INBOUND).json()['journey']
    assert detail['direction'] == 'inbound' and detail['headsign'] == 'West'
    assert [item['headsign'] for item in detail['calls']] == ['West', 'North', 'North']
    assert [item['quay_id'] for item in detail['calls']] == ['NSR:Quay:1103', 'NSR:Quay:1102', 'NSR:Quay:1101']

    absent = draft_for(client, start='09:59')
    path = paths(absent)[0]
    assert client.get(path).json()['outcome'] == 'not_found'
    evidence['days'][DATE].update(coverage='partial', reasons=['unresolved_calendar'])
    assert client.get(path).json()['outcome'] == 'insufficient'
    evidence['days'][DATE].update(coverage='complete', reasons=[], journeys={})
    assert client.get(path).json()['outcome'] == 'insufficient'
    evidence['days'].clear()
    outage = client.get(path).json()
    assert outage['coverage'] == 'unavailable' and outage['outcome'] == 'insufficient'
    assert client.get('/drafts/' + absent['id']).json() == absent


def test_route_command_review_race_and_frozen_expiry(fake, users):
    client, evidence = fake
    assert login(client, users).status_code == 200
    draft = draft_for(client)
    old_review, old_confirmation = review(client, draft)
    assert old_review.status_code == 200
    saved, body = write_choice(client, draft, 0)
    assert saved.status_code == 200
    reference = saved.json()['reference']
    assert reference['status'] == 'compatible'
    assert 'position_coordinate_revision' not in reference
    assert (reference['start_position'], reference['end_position']) == (3, 4)
    assert reference['calls'][0]['quay_id'] == reference['calls'][2]['quay_id'] == 'NSR:Quay:1001'
    assert reference['calls'][0]['occurrence_id'] != reference['calls'][2]['occurrence_id']
    assert reference['field_decisions']['destination']['manual'] == 'Drivers display text'
    assert client.get('/drafts/' + draft['id']).json() == draft
    assert write_choice(client, draft, 0, body=body)[0].json() == saved.json()
    assert write_choice(client, draft, 0, body={**body, 'selection': {**body['selection'], 'start_position': 1}})[0].status_code == 409
    assert confirm(client, draft, old_confirmation).status_code == 409
    assert review(client, draft)[0].status_code == 409
    assert write_choice(client, draft, 1, end=120)[0].status_code == 422
    assert write_choice(client, draft, 1, digest='b' * 64)[0].status_code == 409
    operation = client.get(f"/drafts/{draft['id']}/route-reference-operations/{body['operation_id']}")
    assert operation.json()['result'] == saved.json()

    response, confirmation = review(client, draft, 1)
    assert response.status_code == 200
    assert confirm(client, draft, confirmation).status_code == 409
    newer, _ = write_choice(client, draft, 1, start=1)
    assert newer.status_code == 200
    assert confirm(client, draft, {**confirmation, 'expected_route_revision': 1}).status_code == 409
    _, current = review(client, draft, 2)
    current['expected_route_revision'] = 2

    # The source corrects a headsign and then becomes unavailable between the
    # review and confirmation. The accepted operation must freeze the saved copy.
    evidence['days'][DATE]['journeys'][JOURNEY]['calls'][0]['headsign'] = 'Replacement'
    assert inspect_state(client, draft)['references'][0]['comparison'] == 'changed'
    evidence['days'][DATE]['journeys'].pop(JOURNEY)
    assert inspect_state(client, draft)['references'][0]['comparison'] == 'missing'
    evidence['days'].clear()
    assert inspect_state(client, draft)['references'][0]['comparison'] == 'unavailable'
    accepted = confirm(client, draft, current)
    assert accepted.status_code == 200
    workday = accepted.json()
    frozen_path = '/workdays/' + workday['id'] + '/route-references'
    frozen = client.get(frozen_path)
    assert frozen.headers['cache-control'] == 'no-store'
    assert frozen.json()['references'] == [newer.json()['reference']]
    assert confirm(client, draft, current).json() == workday
    assert confirm(client, draft, confirmation).status_code == 409
    assert write_choice(client, draft, 2)[0].status_code == 409
    assert client.post(frozen_path, headers=headers(client), json={}).status_code == 405

    from app.private_main import app
    other = TestClient(app)
    try:
        assert login(other, users, 1).status_code == 200
        assert other.get(frozen_path).status_code == 404
        assert other.get(paths(draft)[0]).status_code == 404
    finally:
        other.close()
    with database() as conn:
        conn.execute("INSERT INTO workday_lifecycles(workday_id,state,started_at,revision,ended_at) "
                     "VALUES (%s,'ended',statement_timestamp(),2,statement_timestamp())", (workday['id'],))
        conn.execute('DELETE FROM drafts WHERE id=%s', (draft['id'],))
    assert client.get(frozen_path).json() == frozen.json()
    assert confirm(client, draft, current).json() == workday
    with database() as conn:
        conn.execute("UPDATE workdays SET final_end=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s",
                     (workday['id'],))
    assert client.get(frozen_path).status_code == 410
    assert confirm(client, draft, current).status_code == 410
    cleanup()
    with database() as conn:
        assert conn.execute('SELECT 1 FROM workday_route_references WHERE workday_id=%s', (workday['id'],)).fetchone() is None


def test_pinned_pilot_route_save_replay_confirmation_and_manual_anchor(pilot_timetable, users, monkeypatch):
    from app.private_main import app

    monkeypatch.setattr(route_source, 'catalogue', pilot_timetable)
    # Use the original observation instant for route freshness, leaving all
    # private database session, receipt and evidence clocks real.
    observed = datetime.fromisoformat(OBSERVED_AT)
    monkeypatch.setattr(route_reference_storage, 'now_for', lambda _: observed)
    pilot_day = route_source.DATES[0]
    key = 'TRO:ServiceJourney:20_260918101387157_1133'
    journey = pilot_timetable['days'][pilot_day]['journeys'][key]
    first, last = journey['calls'][0], journey['calls'][-1]
    assert last['quay_id'] == 'NSR:Quay:92496' and last['stop_place_id'] is None
    facts = content()
    facts.update(service_date=pilot_day.isoformat(), physical_bus='1234')
    facts['activities'][0].update(type='trip', raw_code='Trip', line='20', trip='0007', direction=journey['direction'],
                                  start=first['departure']['calendar_time'], end=last['arrival']['calendar_time'],
                                  from_place=first['name'], to_place=last['name'], uncertainty=None)
    # Keep the disposable plan eligible for confirmation after the fixed pilot
    # dates have expired, without changing any real route times.
    after = max(datetime.fromisoformat(last['arrival']['utc']), datetime.now(UTC)) + timedelta(hours=1)
    signoff = after.astimezone(route_source.OSLO).isoformat(timespec='seconds')
    facts['activities'].append({'id': str(uuid4()), 'type': 'Sign-off',
                                'start': signoff, 'end': signoff})
    # As in the existing route controls, use TestClient without lifespan. The
    # fixture supplies the real archive without production launch configuration.
    with closing(TestClient(app)) as client:
        assert login(client, users).status_code == 200
        draft_response, _ = save(client, facts)
        assert draft_response.status_code == 200, draft_response.text
        draft = draft_response.json()
        query, _, activity = paths(draft)
        listed = client.get(query).json()
        assert listed['source_state'] == 'available'
        assert listed['provenance']['observed_at'] == pilot_timetable['provenance']['observed_at']
        assert [1, last['position']] in next(item['matching_ranges'] for item in listed['journeys'] if item['journey_id'] == key)
        route_body = {'operation_id': str(uuid4()), 'expected_draft_revision': draft['revision'],
                      'expected_route_revision': 0, 'activity_id': activity,
                      'selection': {'journey_id': key, 'source_sha256': route_source.DIGEST, 'start_position': 1,
                                    'end_position': last['position'], 'field_decisions': CHOICES}}
        saved = write_choice(client, draft, 0, body=route_body)[0]
        assert saved.status_code == 200, saved.text
        reference = saved.json()['reference']
        assert reference['status'] == 'compatible'
        assert reference['position_coordinate_revision'] == position_coordinates.PILOT_MANUAL_REVISION
        assert write_choice(client, draft, 0, body=route_body)[0].json() == saved.json()
        assert client.get(f"/drafts/{draft['id']}/route-reference-operations/{route_body['operation_id']}").json()['result'] == saved.json()
        with database() as conn:
            stored = route_reference_storage.receipt(conn, draft['id'], route_body['operation_id'])
            canonical = deepcopy(route_body)
            for choice in canonical['selection']['field_decisions'].values():
                choice.setdefault('manual', None)
            assert stored['payload_hash'] == draft_storage.fingerprint(draft['id'], canonical)

        reviewed, decisions = review(client, draft, 1)
        assert reviewed.status_code == 200 and reviewed.json()['blockers'] == []
        monkeypatch.setattr(route_source, 'catalogue', route_source.EMPTY)
        confirmed = confirm(client, draft, {**decisions, 'expected_route_revision': 1})
        assert confirmed.status_code == 200, confirmed.text
        plan = confirmed.json()
        path = '/workdays/' + plan['id']
        assert client.get(path + '/route-references').json()['references'] == [reference]
        assert write_choice(client, draft, 0, body=route_body)[0].json() == saved.json()
        projection = client.get(path + '/position-coordinates/' + activity)
        assert projection.status_code == 200
        view = projection.json()
        assert view['route']['basis'] == draft_storage.fingerprint(activity, reference)
        assert view['source']['revision'] == position_coordinates.PILOT_MANUAL_REVISION
        assert view['source']['source_url'] == 'https://developer.entur.no/open-data/stops'
        assert all(call['stop_place_id'] and call['coordinate_issue'] == 'validity-unknown'
                   and call['coordinates'] is None for call in view['calls'])
        call = view['calls'][-1]
        assert call['stop_place_id'] == 'NSR:StopPlace:54202'
        assert client.post(path + '/selection', headers=headers(client), json={
            'operation_id': str(uuid4()), 'expected_revision': 0, 'activity_id': activity,
        }).status_code == 200
        command = {'operation_id': str(uuid4()), 'expected_revision': 0, 'activity_id': activity,
                   'route_basis': view['route']['basis'], 'occurrence_id': call['occurrence_id'],
                   'coordinate_revision': None, 'origin': 'manual', 'evidence_at': plan['confirmed_at']}
        recorded = client.post(path + '/position-anchor', headers=headers(client), json=command)
        assert recorded.status_code == 200, recorded.text
        assert client.post(path + '/position-anchor', headers=headers(client), json=command).json() == recorded.json()
        gps = {**command, 'operation_id': str(uuid4()), 'expected_revision': 1, 'origin': 'gps'}
        rejected = client.post(path + '/position-anchor', headers=headers(client), json=gps)
        assert rejected.status_code == 422
        assert rejected.json()['detail'] == 'Holdeplassen har ingen bekreftet plattformkobling for dette lagringsforsøket.'
        anchor = client.get(path + '/position-anchor').json()['anchor']
        assert anchor['revision'] == 1 and anchor['origin'] == 'manual' and anchor['coordinate_revision'] is None
        assert anchor['quay_id'] == 'NSR:Quay:92496' and anchor['stop_place_id'] == 'NSR:StopPlace:54202'


def test_packaged_pilot_manual_pin_survives_freeze_and_requires_fresh_manual_choice(fake, users):
    client, evidence = fake
    evidence['provenance']['sha256'] = route_source.DIGEST
    calls = evidence['days'][DATE]['journeys'][JOURNEY]['calls']
    calls[2].update(quay_id='NSR:Quay:90847', stop_place_id=None)
    calls[3].update(quay_id='NSR:Quay:92496', stop_place_id=None)
    assert login(client, users).status_code == 200
    facts = content()
    facts.update(service_date=DATE.isoformat(), physical_bus='1234')
    first = facts['activities'][0]
    first.update(type='trip', line='20', trip='synthetic-first', direction='outbound', uncertainty=None,
                 start=instant(10)['calendar_time'], end=instant(11)['calendar_time'], from_place='Start', to_place='End')
    second = {**first, 'id': str(uuid4()), 'trip': 'synthetic-second'}
    facts['activities'].append(second)
    reply, _ = save(client, facts)
    assert reply.status_code == 200
    draft = reply.json()
    saved, body = write_choice(client, draft, 0, digest=route_source.DIGEST)
    assert saved.status_code == 200
    assert saved.json()['reference']['position_coordinate_revision'] == position_coordinates.PILOT_MANUAL_REVISION
    assert write_choice(client, draft, 0, body=body)[0].json() == saved.json()
    other_body = {**body, 'operation_id': str(uuid4()), 'expected_route_revision': 1, 'activity_id': second['id']}
    other = write_choice(client, draft, 1, body=other_body)[0]
    assert other.status_code == 200
    reviewed, decisions = review(client, draft, 2)
    assert reviewed.status_code == 200 and reviewed.json()['blockers'] == []
    accepted = confirm(client, draft, {**decisions, 'expected_route_revision': 2})
    assert accepted.status_code == 200
    plan = accepted.json()
    path = '/workdays/' + plan['id']
    frozen = client.get(path + '/route-references').json()['references']
    assert {item['activity_id']: item for item in frozen} == {
        first['id']: saved.json()['reference'], second['id']: other.json()['reference'],
    }
    for revision, activity in enumerate((first['id'], second['id'])):
        selected = client.post(path + '/selection', headers=headers(client), json={
            'operation_id': str(uuid4()), 'expected_revision': revision, 'activity_id': activity,
        })
        assert selected.status_code == 200
        projection = client.get(path + '/position-coordinates/' + activity).json()
        assert projection['source']['revision'] == position_coordinates.PILOT_MANUAL_REVISION
        call = projection['calls'][-1]
        assert call['stop_place_id'] == 'NSR:StopPlace:54202' and call['coordinates'] is None
        command = {'operation_id': str(uuid4()), 'expected_revision': revision, 'activity_id': activity,
                   'route_basis': projection['route']['basis'], 'occurrence_id': call['occurrence_id'],
                   'coordinate_revision': None, 'origin': 'manual', 'evidence_at': plan['confirmed_at']}
        if revision == 1:
            carried = client.post(path + '/position-anchor', headers=headers(client),
                                  json={**command, 'carried_from_revision': 1})
            assert carried.status_code == 409
            assert client.get(path + '/position-anchor').json()['anchor']['activity_id'] == first['id']
        recorded = client.post(path + '/position-anchor', headers=headers(client), json=command)
        assert recorded.status_code == 200
    anchor = client.get(path + '/position-anchor').json()['anchor']
    assert anchor['revision'] == 2 and anchor['activity_id'] == second['id']
    assert anchor['origin'] == 'manual' and anchor['coordinate_revision'] is None and anchor['carried_from'] is None


def test_new_pilot_pins_loadable_v1_or_explicit_null(fake, users, monkeypatch):
    client, evidence = fake
    evidence['provenance']['sha256'] = route_source.DIGEST
    assert login(client, users).status_code == 200
    draft = draft_for(client)
    load = position_coordinates.sidecar
    monkeypatch.setattr(position_coordinates, 'sidecar',
                        lambda revision: load(revision) if revision == position_coordinates.PILOT_REVISION else None)
    saved, body = write_choice(client, draft, 0, digest=route_source.DIGEST)
    assert saved.status_code == 200
    assert saved.json()['reference']['position_coordinate_revision'] == position_coordinates.PILOT_REVISION

    monkeypatch.setattr(position_coordinates, 'sidecar', lambda _: None)
    new, _ = write_choice(client, draft, 1, digest=route_source.DIGEST)
    assert new.status_code == 200
    assert new.json()['reference']['position_coordinate_revision'] is None
    replay = write_choice(client, draft, 0, body=body)[0].json()
    assert replay['reference'] == saved.json()['reference']
    assert replay['current_route_revision'] == 2


def test_edit_invalidation_and_stale_or_incompatible_selection(fake, users):
    client, evidence = fake
    assert login(client, users).status_code == 200
    draft = draft_for(client, start='09:59')
    assert client.post(paths(draft)[1], json={}).status_code == 403
    result, body = write_choice(client, draft, 0)
    assert result.status_code == 200 and result.json()['reference']['status'] == 'incompatible'
    facts = deepcopy(draft['draft'])
    facts['activities'][0]['start'] = f'{DATE}T10:00+01:00'
    edited, _ = save(client, facts, draft['id'], draft['revision'])
    assert edited.status_code == 200
    updated = edited.json()
    assert client.get(paths(draft)[0]).status_code == 409
    assert write_choice(client, draft, 1, body={**body, 'operation_id': str(uuid4())})[0].status_code == 409
    state = inspect_state(client, updated)
    assert not state['references'] and state['outdated'][0]['decision_revision'] == 1
    evidence['provenance']['observed_at'] = '2001-01-01T00:00:00Z'
    stale = client.get(paths(updated)[0]).json()
    assert stale['coverage'] == 'complete' and stale['source_state'] == 'stale' and stale['outcome'] == 'insufficient'
    selected, body = write_choice(client, updated, 1)
    assert selected.status_code == 200 and selected.json()['reference']['status'] == 'unverified'
    cleared, _ = write_choice(client, updated, 2, body={**body, 'operation_id': str(uuid4()),
                                                       'expected_route_revision': 2, 'selection': None})
    assert cleared.status_code == 200 and not inspect_state(client, updated)['references']
    with database() as conn:
        conn.execute("UPDATE drafts SET created_at=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s",
                     (draft['id'],))
    assert client.get(paths(updated)[0]).status_code == 410
    assert write_choice(client, updated, 2, body=body)[0].status_code == 410
    cleanup()
    with database() as conn:
        assert conn.execute('SELECT 1 FROM draft_route_decisions WHERE draft_id=%s', (draft['id'],)).fetchone() is None


def test_pre017_pending_and_accepted_operation_hashes_are_compatible(fake, users):
    client, _ = fake
    assert login(client, users).status_code == 200
    draft = draft_for(client)
    reviewed, body = review(client, draft)
    assert reviewed.status_code == 200
    with database() as conn:
        conn.execute('UPDATE workday_operations SET route_revision=NULL WHERE id=%s', (body['operation_id'],))
    response = confirm(client, draft, body)
    assert response.status_code == 200
    expected_hash = draft_storage.fingerprint(draft['id'], {**body, 'acknowledgements': sorted(body['acknowledgements'])})
    with database() as conn:
        persisted = conn.execute('SELECT * FROM workday_operations WHERE id=%s', (body['operation_id'],)).fetchone()
        assert persisted['payload_hash'] == expected_hash and persisted['route_revision'] is None
        assert client.get('/workdays/' + response.json()['id'] + '/route-references').json()['references'] == []

        # Exercise actual 017 against a populated pre-017 shape in a transaction-
        # local schema. Public tables and accepted values are unaffected.
        conn.execute('CREATE SCHEMA route_migration_control')
        conn.execute('SET LOCAL search_path TO route_migration_control, public')
        conn.execute('CREATE TABLE drafts(id uuid PRIMARY KEY)')
        conn.execute('CREATE TABLE workdays(id uuid PRIMARY KEY)')
        conn.execute('CREATE TABLE workday_operations(id uuid PRIMARY KEY, payload_hash text)')
        conn.execute('INSERT INTO workday_operations VALUES (%s,%s)', (body['operation_id'], expected_hash))
        conn.execute('INSERT INTO workday_operations VALUES (%s,NULL)', (uuid4(),))
        migration = Path(__file__).resolve().parents[1] / 'migrations/private/017_route_reference.sql'
        conn.execute(migration.read_text(encoding='utf-8'))
        rows = conn.execute('SELECT payload_hash,route_revision FROM workday_operations ORDER BY payload_hash NULLS FIRST').fetchall()
        assert rows == [{'payload_hash': None, 'route_revision': None},
                        {'payload_hash': expected_hash, 'route_revision': None}]
        conn.rollback()
    assert confirm(client, draft, body).json() == response.json()


def test_road_snapshot_follows_owner_and_exact_frozen_route(fake, users, monkeypatch, tmp_path):
    client, _ = fake
    assert login(client, users).status_code == 200
    draft = draft_for(client)
    assert write_choice(client, draft, 0)[0].status_code == 200
    reviewed, body = review(client, draft, 1)
    assert reviewed.status_code == 200
    confirmed = confirm(client, draft, {**body, 'expected_route_revision': 1})
    assert confirmed.status_code == 200
    workday = confirmed.json()['id']
    path = f'/workdays/{workday}/road-reference/{paths(draft)[2]}'
    snapshot = tmp_path / 'fixture.json'
    monkeypatch.setattr(road_reference_api, 'PUBLIC_SNAPSHOT', snapshot)
    assert client.get(path).json() == {'status': 'road-unqualified'}
    assert client.get(f'/workdays/{workday}/road-reference/{uuid4()}').json() == {'status': 'route-unqualified'}
    binding = {'service_date': DATE.isoformat(), 'line_id': route_source.LINE_ID, 'journey_id': JOURNEY,
               'journey_version': '1', 'pattern_id': 'TRO:JourneyPattern:synthetic-outbound', 'pattern_version': '1',
               'direction': 'outbound', 'start_position': 3,
               'end_position': 4, 'route_source_sha256': DIGEST,
               'occurrence_ids': ['TRO:StopPointInJourneyPattern:synthetic-3', 'TRO:StopPointInJourneyPattern:synthetic-4']}
    package = {'version': 1, 'binding': binding, 'manifest': {'control': 'synthetic only'},
               'qualification': dict.fromkeys(('direction', 'coverage', 'topology', 'source', 'error_model'), 'fixture')}
    for field, wrong in [('end_position', 3), ('direction', 'inbound'), ('route_source_sha256', 'b' * 64),
                         ('occurrence_ids', list(reversed(binding['occurrence_ids'])))]:
        snapshot.write_text(json.dumps({**package, 'binding': {**binding, field: wrong}}), encoding='utf-8')
        assert client.get(path).json() == {'status': 'road-unqualified'}
    snapshot.write_text(json.dumps(package), encoding='utf-8')
    assert client.get(path).json() == {'status': 'qualified', 'manifest': package['manifest']}
    with TestClient(client.app) as anonymous:
        assert anonymous.get(path).status_code == 401
