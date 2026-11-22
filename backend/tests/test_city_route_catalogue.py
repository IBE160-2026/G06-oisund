"""Opt-in fit of the public 30 November line 26 trip to an isolated workday."""

from contextlib import closing
from datetime import UTC, date, datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient
import pytest

from app import route_catalogue, route_reference_storage, route_source
from app.private_storage import database
from test_private_access import headers, login, synthetic_only, users
from test_private_drafts import content, save
from test_private_route_references import CHOICES, paths, review, write_choice
from test_private_workdays import confirm


def test_line_26_early_trip_survives_confirmation_and_anchoring(users, monkeypatch):
    from app.private_main import app

    day = date(2026, 11, 30)
    key = 'TRO:ServiceJourney:26_260918101386605_1000'
    with database() as conn:
        stamp = conn.execute("SELECT observed_at FROM public_route_days WHERE line_code='26' AND service_date=%s",
                             (day,)).fetchone()
        if stamp is None:
            pytest.skip('Requires the archived November 2026 public Tromsø catalogue in the isolated database')
        catalogue = route_catalogue.lookup(conn, day, stamp['observed_at'], '26')
    journey = catalogue['journeys'].get(key)
    if not journey or catalogue['provenance']['generation'] != '1795302164876896':
        pytest.skip('Requires the checked NeTEx generation')
    nsr_revision = catalogue['provenance'].get('nsr_revision') or ''
    dated = nsr_revision.startswith('nsr-future-')
    if dated and not nsr_revision.startswith('nsr-future-1795345333303902-'):
        pytest.skip('Requires the checked current-and-future NSR generation')
    monkeypatch.setattr(route_reference_storage, 'now_for', lambda _: stamp['observed_at'])

    first, last = journey['calls'][0], journey['calls'][-1]
    assert first['name'] == 'Pyramiden' and first['departure']['raw_time'] == '05:10:00'
    assert last['name'] == 'Skognesvegen' and last['position'] == 36
    facts = content()
    facts.update(service_date=day.isoformat(), physical_bus='1234')
    facts['activities'][0].update(type='trip', raw_code='Trip', trip='0007', line='26', direction=journey['direction'],
                                  start=first['departure']['calendar_time'], end=last['arrival']['calendar_time'],
                                  source_start='05:10', source_end='05:57', from_place=first['name'],
                                  to_place=last['name'], uncertainty=None)
    end = max(datetime.fromisoformat(last['arrival']['utc']), datetime.now(UTC)) + timedelta(hours=1)
    signoff = end.astimezone(route_source.OSLO).isoformat(timespec='seconds')
    facts['activities'].append({'id': str(uuid4()), 'type': 'Sign-off', 'start': signoff, 'end': signoff})

    with closing(TestClient(app)) as client:
        assert client.get('/route-catalogue', params={'service_date': day, 'line_code': '26'}).status_code == 401
        assert login(client, users).status_code == 200
        response, _ = save(client, facts)
        assert response.status_code == 200, response.text
        draft = response.json()
        query, _, activity = paths(draft)
        departure = client.get(query + '&line_code=26').json()
        assert departure['coverage'] == 'complete' and departure['line_code'] == '26'
        assert [[1, 36]] == next(item['matching_ranges'] for item in departure['journeys'] if item['journey_id'] == key)
        command = {'operation_id': str(uuid4()), 'expected_draft_revision': draft['revision'],
                   'expected_route_revision': 0, 'activity_id': activity,
                   'selection': {'line_code': '26', 'journey_id': key, 'source_sha256': departure['provenance']['sha256'],
                                 'start_position': 1, 'end_position': 36, 'field_decisions': CHOICES}}
        response, _ = write_choice(client, draft, 0, body=command)
        assert response.status_code == 200, response.text
        reference = response.json()['reference']
        assert reference['status'] == 'compatible'
        assert reference['position_coordinate_revision'] == catalogue['provenance']['nsr_revision']

        reviewed, decisions = review(client, draft, 1)
        assert reviewed.status_code == 200 and reviewed.json()['blockers'] == []
        response = confirm(client, draft, {**decisions, 'expected_route_revision': 1})
        assert response.status_code == 200, response.text
        plan = response.json()
        path = '/workdays/' + plan['id']
        assert client.get(path + '/route-references').json()['references'] == [reference]
        view = client.get(path + '/position-coordinates/' + activity).json()
        assert len(view['calls']) == 36
        assert all(call['stop_place_id'] for call in view['calls'])
        if dated:
            assert view['source']['revision'] == reference['position_coordinate_revision']
            assert view['calls'][0]['coordinates']['quay_version'] == '3'
            assert view['calls'][-1]['coordinates']['quay_version'] == '6'
        else:
            assert all(call['coordinates'] is None for call in view['calls'])
        assert client.post(path + '/selection', headers=headers(client), json={
            'operation_id': str(uuid4()), 'expected_revision': 0, 'activity_id': activity,
        }).status_code == 200
        anchor = {'operation_id': str(uuid4()), 'expected_revision': 0, 'activity_id': activity,
                  'route_basis': view['route']['basis'], 'occurrence_id': view['calls'][0]['occurrence_id'],
                  'coordinate_revision': reference['position_coordinate_revision'] if dated else None,
                  'origin': 'manual', 'evidence_at': plan['confirmed_at']}
        response = client.post(path + '/position-anchor', headers=headers(client), json=anchor)
        assert response.status_code == 200, response.text
        assert client.post(path + '/position-anchor', headers=headers(client), json=anchor).json() == response.json()
        gps = {**anchor, 'operation_id': str(uuid4()), 'expected_revision': 1, 'origin': 'gps',
               'occurrence_id': view['calls'][1]['occurrence_id']}
        assert client.post(path + '/position-anchor', headers=headers(client), json=gps).status_code == (200 if dated else 422)
        saved = client.get(path + '/position-anchor').json()['anchor']
        assert saved['origin'] == ('gps' if dated else 'manual')
        assert saved['occurrence_id'] == view['calls'][int(dated)]['occurrence_id']
