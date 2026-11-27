"""Dated limits and authenticated road-area selection in private test storage."""

from datetime import UTC, datetime, timedelta
from contextlib import closing
from uuid import uuid4

from fastapi.testclient import TestClient
import pytest

from app.road_area_catalogue import OSLO, approved_limits, publish, registered_interiors
from app import road_situation_source
from app.private_storage import database
from test_private_access import client, login, pytestmark, synthetic_only, users


@pytest.fixture
def clocked_area(monkeypatch):
    from app import road_area_api
    from app.private_main import app

    now = datetime(2061, 3, 13, 11, tzinfo=UTC)

    class Clock(datetime):
        @classmethod
        def now(cls, tz=None):
            return now.astimezone(tz) if tz else now.replace(tzinfo=None)

    monkeypatch.setattr(road_area_api, 'datetime', Clock)
    with closing(TestClient(app)) as client:
        yield client, now


def test_area_uses_only_current_oslo_date_and_latest_observation(clocked_area, users, monkeypatch):
    from app import road_area_api

    monkeypatch.setattr(road_area_api, 'relevant_situations', lambda *_: ([], None, None))
    client, now = clocked_area
    today = now.astimezone(OSLO).date()
    observed = now - timedelta(minutes=20)
    assert client.get('/road-areas/tromsoya').status_code == 401
    assert login(client, users).status_code == 200
    assert client.get('/road-areas/bogus').status_code == 422
    revisions = []
    try:
        for day, age, listed in ((today, 2, 'first'), (today, 1, 'recent'),
                                  (today - timedelta(days=1), 0, 'yesterday'), (today, 3, 'older')):
            stamp = observed - timedelta(minutes=age)
            revision = uuid4().hex * 2
            revisions.append(revision)
            source = {'sha256': revision, 'revision': revision}
            data = {'tromsoya': {'id': listed, 'revision': revision, 'packages': [{'edges': [{'kmh': None}]}]}}
            publish(day, stamp, stamp, source, data)
            publish(day, stamp, stamp, source, data)
        response = client.get('/road-areas/tromsoya')
        assert response.status_code == 200 and response.headers['cache-control'] == 'no-store'
        compressed = client.get('/road-areas/tromsoya', headers={'Accept-Encoding': 'gzip'})
        assert compressed.headers['content-encoding'] == 'gzip' and compressed.json() == response.json()
        identity = client.get('/road-areas/tromsoya', headers={'Accept-Encoding': 'gzip;q=0'})
        assert 'content-encoding' not in identity.headers and identity.json() == response.json()
        assert response.json() == {'status': 'qualified', 'manifest': {'id': 'recent', 'revision': revisions[1], 'packages': [
            {'edges': [{'kmh': None}]},
        ]}, 'confirmed': 0}
        assert client.get('/road-areas/fastlandet').json() == {'status': 'road-unqualified'}
        assert client.get('/road-areas/tromsoya/revision').json() == {'revision': revisions[1]}
        with database() as conn:
            assert conn.execute('SELECT count(*) AS count FROM public_road_area_versions WHERE revision=ANY(%s)',
                                (revisions,)).fetchone()['count'] == len(revisions)
        expired_revision = uuid4().hex * 2
        revisions.append(expired_revision)
        expired = {'id': 'tromsoya', 'checkedAt': observed.isoformat(), 'retrievedAt': observed.isoformat(),
                   'validUntil': (now - timedelta(minutes=1)).isoformat(),
                   'packages': [{'edges': [{'kmh': 30, 'confirmedTransitions': ['next']}]}]}
        source = {'sha256': expired_revision, 'revision': expired_revision}
        publish(today, observed, observed, source, {'tromsoya': expired})
        result = client.get('/road-areas/tromsoya').json()
        assert result['confirmed'] == 0
        assert result['manifest']['packages'][0]['edges'] == [{'kmh': None}]
        assert datetime.fromisoformat(result['manifest']['validUntil']).date() == today + timedelta(days=1)

        conflict = uuid4().hex * 2
        revisions.append(conflict)
        with pytest.raises(ValueError, match='Conflicting'):
            publish(today, observed, observed, {'sha256': conflict, 'revision': conflict},
                    {'fastlandet': expired, 'tromsoya': expired})
        assert client.get('/road-areas/fastlandet/revision').json() == {'revision': None}
    finally:
        with database() as conn:
            conn.execute('DELETE FROM public_road_area_versions WHERE revision=ANY(%s)', (revisions,))


def test_pilot_chooses_a_coherent_publication_and_connects_area_edges(clocked_area, users, monkeypatch):
    from app import road_area_api
    from app.road_area_catalogue import AREAS

    monkeypatch.setattr(road_area_api, 'relevant_situations', lambda *_: ([], None, None))
    client, now = clocked_area
    day = now.date()
    def edge(number):
        return {'id': str(number), 'kmh': None, 'shape': [[18.9, 69.6], [19, 69.6]],
                'successors': [str(number + 1)] if number < 4 else []}

    assert client.get('/road-areas/pilot').status_code == 401
    assert login(client, users).status_code == 200
    assert client.get('/road-areas/pilot').json() == {'status': 'road-unqualified'}
    revisions = [uuid4().hex * 2 for _ in range(2)]
    try:
        for index, revision in enumerate(revisions):
            observed = now - timedelta(minutes=2 - index)
            source = {'sha256': revision, 'revision': revision}
            batch = {area: {'id': area, 'profile': 'NVDB-AREA-1', 'revision': revision, 'path': [],
                            'packages': [{'edges': [edge(number), edge(number + 1)]}]}
                     for number, area in enumerate(AREAS, 1)}
            if index == 1:
                batch.pop('kvaloya')
            publish(day, observed, observed, source, batch)
        result = client.get('/road-areas/pilot').json()
        assert result['status'] == 'qualified'
        manifest = result['manifest']
        assert manifest['revision'] == revisions[0]
        assert len(manifest['packages']) == 1
        actual = {e['id']: e for e in manifest['packages'][0]['edges']}
        assert actual == {str(number): edge(number) for number in range(1, 5)}
        assert client.get('/road-areas/pilot/revision').json() == {'revision': revisions[0]}
        assert client.get('/road-areas/fastlandet/revision').json() == {'revision': revisions[1]}
    finally:
        with database() as conn:
            conn.execute('DELETE FROM public_road_area_versions WHERE revision=ANY(%s)', (revisions,))


def test_only_exact_direction_and_reviewed_limit_is_published():
    now = datetime(2026, 11, 30, 10, tzinfo=UTC)
    day = now.date()
    digest = 'e' * 64
    graph = [{'id': 'road-med', 'direction_verified': True, 'kmh': 70, 'speed_basis': 'registered-static',
              'successors': ['unsigned-med']},
             {'id': 'road-mot', 'direction_verified': False, 'kmh': None, 'speed_basis': 'unresolved-direction'},
             {'id': 'unsigned-med', 'direction_verified': True, 'kmh': None, 'speed_basis': 'incomplete-limit',
              'speed_evidence': [], 'parent_evidence': None}]
    review = {'source_sha256': digest, 'effective_date': day.isoformat(), 'checked_at': now.isoformat(),
              'valid_until': (now + timedelta(hours=6)).isoformat(), 'limits': {
                  'road-med': {'kmh': 70, 'basis': 'registered', 'evidence': 'Synthetic exact dated test'},
                  'unsigned-med': {'kmh': 50, 'basis': 'urban-default', 'evidence': 'Synthetic unsigned urban test'},
              }, 'transitions': {'road-med': {'unsigned-med': 'Synthetic dated exact-node observation'}}}
    elapsed = now - timedelta(minutes=5)
    end = now + timedelta(hours=13)
    assert approved_limits(None, digest, day, elapsed, end, now, graph)[2] == {}
    assert approved_limits(review, digest, day, elapsed, end, now, graph)[2:] == (
        {'road-med': 70, 'unsigned-med': 50}, {'road-med': ['unsigned-med']},
    )
    with pytest.raises(ValueError, match='exact'):
        approved_limits(review, '0' * 64, day, elapsed, end, now, graph)
    review['limits']['road-med']['kmh'] = 60
    with pytest.raises(ValueError, match='Unsupported'):
        approved_limits(review, digest, day, elapsed, end, now, graph)
    review.pop('transitions')
    review['limits'] = {'road-mot': {'kmh': 30, 'basis': 'temporary', 'evidence': 'Synthetic order'}}
    with pytest.raises(ValueError, match='Unsupported'):
        approved_limits(review, digest, day, elapsed, end, now, graph)
    review['limits'] = {'road-med': {'kmh': 30, 'basis': 'temporary', 'evidence': 'Synthetic order'}}
    with pytest.raises(ValueError, match='directional placement'):
        approved_limits(review, digest, day, elapsed, end, now, graph)
    proof = {'segment': 'road-med', 'starts_at': elapsed.isoformat(),
             'ends_at': (now + timedelta(hours=6)).isoformat(), 'record_revisions': {'order-1': 'f' * 64}}
    review['limits']['road-med']['restriction'] = proof
    assert approved_limits(review, digest, day, elapsed, end, now, graph)[2] == {'road-med': 30}
    proof['starts_at'] = (now + timedelta(hours=1)).isoformat()
    proof['ends_at'] = (now + timedelta(hours=2)).isoformat()
    assert approved_limits(review, digest, day, elapsed, end, now, graph)[2] == {'road-med': 30}
    proof['ends_at'] = elapsed.isoformat()
    with pytest.raises(ValueError, match='exact validity'):
        approved_limits(review, digest, day, elapsed, end, now, graph)


def test_situation_keeps_only_unresolved_stretch_unknown(clocked_area, users, monkeypatch):
    client, now = clocked_area
    retention_clock = datetime.now(UTC)
    day = now.astimezone(OSLO).date()
    observed = now - timedelta(seconds=20)
    revision, snapshot_hash, amended_hash = (uuid4().hex * 2 for _ in range(3))
    source = {'sha256': revision, 'revision': revision}
    near = [[18.94, 69.66], [18.95, 69.66]]
    far = [[18.90, 69.61], [18.91, 69.61]]
    reviewed = [
        {'id': 'unresolved', 'kmh': 60, 'roadReference': 'FV862 S1D1 m42', 'shape': near},
        {'id': 'temporary', 'kmh': 30, 'roadReference': 'FV862 S1D1 m55', 'shape': near,
         'temporaryRestriction': {'start': observed.isoformat(), 'end': (now + timedelta(minutes=10)).isoformat(),
                                  'records': {'synthetic-record': 'e' * 64}}},
        {'id': 'other', 'kmh': None, 'registeredKmh': 50, 'roadReference': 'FV862 S1D1 m2000', 'shape': far},
    ]
    area = {'id': 'tromsoya', 'revision': revision, 'checkedAt': observed.isoformat(),
            'retrievedAt': observed.isoformat(), 'validUntil': (now + timedelta(minutes=20)).isoformat(),
            'roadNumbers': ['F862'], 'registeredInteriors': True, 'packages': [{'edges': reviewed}],
            'temporaryBoundaries': [observed.isoformat(), (now + timedelta(minutes=10)).isoformat()]}
    event = {'record': 'synthetic-record', 'situation': 'synthetic-roadwork', 'road': 'F862', 'point': False,
             'bounds': [18.94, 69.657, 18.952, 69.663], 'start': observed.isoformat(), 'end': None,
             'speed_management': True, 'revision': 'e' * 64}
    try:
        publish(day, observed, observed, source, {'tromsoya': area})
        road_situation_source.publish({'observed_at': observed.isoformat(), 'sha256': snapshot_hash,
                                       'url': road_situation_source.url(), 'events': [event]}, retention_clock)
        assert login(client, users).status_code == 200
        response = client.get('/road-areas/tromsoya').json()
        assert response['confirmed'] == 2
        assert [edge['kmh'] for edge in response['manifest']['packages'][0]['edges']] == [None, 30, 50]
        assert all('roadReference' not in edge and 'temporaryRestriction' not in edge
                   for edge in response['manifest']['packages'][0]['edges'])
        derived = response['manifest']['revision']
        assert derived != revision
        lease = (observed + road_situation_source.LEASE).isoformat()
        assert response['manifest']['situationLeaseUntil'] == lease
        assert client.get('/road-areas/tromsoya/revision').json() == {'revision': derived, 'situationLeaseUntil': lease}
        road_situation_source.publish({'observed_at': (now - timedelta(seconds=10)).isoformat(),
                                       'sha256': amended_hash, 'url': road_situation_source.url(),
                                       'events': [{**event, 'revision': 'f' * 64}]}, retention_clock)
        amended = client.get('/road-areas/tromsoya').json()['manifest']
        assert [edge['kmh'] for edge in amended['packages'][0]['edges']] == [None, None, 50]
        assert amended['revision'] != derived
        # Simulate a pre-upgrade snapshot with valid stored bounds and linework
        # outside today's geometry budget, even for a previously reviewed record.
        monkeypatch.setattr(road_situation_source, 'MAX_EVENT_POINTS', 1)
        legacy_hash = uuid4().hex * 2
        try:
            road_situation_source.publish({
                'observed_at': (now - timedelta(seconds=5)).isoformat(), 'sha256': legacy_hash,
                'url': road_situation_source.url(), 'events': [event | {'linework': [near]}],
            }, retention_clock)
            masked = client.get('/road-areas/tromsoya').json()['manifest']
            assert [edge['kmh'] for edge in masked['packages'][0]['edges']] == [None, None, 50]
            assert client.get('/road-areas/tromsoya/revision').json()['revision'] == masked['revision']
        finally:
            with database() as conn:
                conn.execute('DELETE FROM public_road_situation_snapshots WHERE sha256=%s', (legacy_hash,))
    finally:
        with database() as conn:
            conn.execute('DELETE FROM public_road_area_versions WHERE revision=%s', (revision,))
            conn.execute('DELETE FROM public_road_situation_snapshots WHERE sha256=ANY(%s)',
                         ([snapshot_hash, amended_hash],))


def test_only_unambiguous_same_road_interiors_use_registered_numbers():
    def edge(identifier, successors, *, road='FV862 S1D1 m1', unresolved=False):
        return {'id': identifier, 'speed_basis': 'registered-static', 'kmh': 50, 'successors': successors,
                'road_reference': road, 'unresolved_at_start': unresolved}

    before, middle, after = edge('a', ['b']), edge('b', ['c']), edge('c', [])
    assert registered_interiors([before, middle, after]) == {'b': 50}
    assert registered_interiors([before, {**middle, 'unresolved_at_start': True}, after]) == {}
    assert registered_interiors([before, {**middle, 'successors': ['c', 'd']}, after, edge('d', [])]) == {}
    assert registered_interiors([before, middle, {**after, 'road_reference': 'EV8 S6D1 m4'}]) == {}
