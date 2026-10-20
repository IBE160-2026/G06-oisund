"""Real PostgreSQL/API draft matrix, exclusively in the disposable project."""
import concurrent.futures
import os
import threading
import time
from types import SimpleNamespace
from uuid import uuid4

import httpx
import pytest
from fastapi import HTTPException

from app import auth
from app.private_storage import cleanup, database, migrate
from test_private_access import client, headers, login, synthetic_only, users, URL

pytestmark = pytest.mark.skipif(os.environ.get('APP_MODE') != 'private-local', reason='Private runtime required')


@pytest.fixture(autouse=True)
def project_guard():
    if os.environ.get('PRIVATE_TEST_PROJECT') != 'ibe160-private-tests':
        pytest.skip('Disposable project marker required')


@pytest.fixture(autouse=True)
def remove_drafts(users):
    yield
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        conn.execute('DELETE FROM drafts WHERE owner=ANY(%s)', (users[1],))
        conn.execute('DELETE FROM draft_operations WHERE owner=ANY(%s)', (users[1],))


def content():
    return {'service_date': '2026-10-24', 'vehicle_duty': '0007', 'realtime_duty': '007', 'physical_bus': None,
            'activities': [{'id': str(uuid4()), 'type': None, 'raw_code': 'Unknown/42',
                            'start': '2026-10-25T00:00+02:00', 'end': '2026-10-25T02:30+01:00',
                            'source_start': '24:00', 'source_end': '26:30', 'from_place': None,
                            'to_place': '?', 'trip': None, 'line': '01', 'direction': None,
                            'uncertainty': 'Uavklart sted', 'provenance': 'Manuell rettelse'}]}


def issue(client, identifier=None):
    response = client.post('/draft-operations', headers=headers(client), json={'draft_id': identifier})
    assert response.status_code == 200
    return response.json()['operation_id']


def save(client, facts=None, identifier=None, revision=0, operation=None):
    body = {'operation_id': operation or issue(client, identifier), 'expected_revision': revision, 'draft': facts or content()}
    return client.post('/drafts' + ('/' + identifier if identifier else ''), headers=headers(client), json=body), body


def test_roundtrip_replay_revisions_and_concurrent_writes(client, users):
    assert login(client, users).status_code == 200
    result, body = save(client)
    assert result.status_code == 200
    original = result.json()
    identifier = original['id']
    assert original['draft'] == body['draft']
    assert client.get('/drafts/' + identifier).json() == original
    assert client.get('/drafts').json()['drafts'][0]['id'] == identifier
    assert client.post('/drafts', headers=headers(client), json=body).json() == original
    assert client.get('/draft-operations/' + body['operation_id']).json() == {'state': 'accepted', 'result': original}
    body['draft']['vehicle_duty'] = 'changed'
    assert client.post('/drafts', headers=headers(client), json=body).status_code == 409
    operations = [issue(client, identifier), issue(client, identifier)]
    proof = headers(client)
    cookies = dict(client.cookies)
    def write(op):
        return httpx.post(URL + '/drafts/' + identifier, headers=proof, cookies=cookies,
                          json={'operation_id': op, 'expected_revision': 1, 'draft': content()}, timeout=20).status_code
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(write, operations)) == [200, 409]
    current = client.get('/drafts/' + identifier).json()
    assert current['revision'] == 2 and current['expires_at'] == original['expires_at']
    migrate(); migrate(); cleanup()
    assert client.get('/drafts/' + identifier).json() == current


def test_all_routes_deny_foreign_unauthenticated_and_forgery(client, users):
    assert login(client, users).status_code == 200
    response, body = save(client)
    identifier = response.json()['id']
    op = body['operation_id']
    reads = ['/drafts/' + identifier, '/draft-operations/' + op]
    writes = [('/drafts', body), ('/drafts/' + identifier, body), ('/draft-operations', {'draft_id': identifier})]
    for path, payload in writes:
        assert client.post(path, json=payload).status_code == 403
        assert client.post(path, headers={**headers(client), 'Origin': 'http://evil.invalid'}, json=payload).status_code == 403
    with httpx.Client(base_url=URL) as other:
        for path in reads + ['/drafts']:
            assert other.get(path).status_code == 401
        for path, payload in writes:
            assert other.post(path, headers=headers(other), json=payload).status_code == 401
        assert login(other, users, 1).status_code == 200
        assert other.get('/drafts').json() == {'drafts': []}
        for path in reads:
            denied = other.get(path)
            assert denied.status_code == 404 and identifier not in denied.text and op not in denied.text
        for path, payload in writes:
            assert other.post(path, headers=headers(other), json=payload).status_code == 404
    assert client.get('/drafts/' + identifier).json() == response.json()
    for path in reads + ['/drafts']:
        assert client.get(path).headers['cache-control'] == 'no-store'


@pytest.mark.parametrize('change', ['negative', 'summer_offset', 'spring_gap', 'no_offset', 'duplicate', 'bus', 'too_many', 'bad_date', 'numeric_date', 'calendar_overflow'])
def test_validation_preserves_unknowns_rejects_contradictions(client, users, change):
    assert login(client, users).status_code == 200
    facts = content()
    if change == 'negative': facts['activities'][0]['end'] = '2026-10-24T23:59+02:00'
    if change == 'summer_offset': facts['activities'][0]['start'] = '2026-07-01T12:00+01:00'
    if change == 'spring_gap': facts['activities'][0]['start'] = '2026-03-29T02:30+01:00'
    if change == 'no_offset': facts['activities'][0]['start'] = '2026-10-25T00:00'
    if change == 'duplicate': facts['activities'].append(facts['activities'][0])
    if change == 'bus': facts['physical_bus'] = 'invented'
    if change == 'too_many': facts['activities'] *= 201
    if change == 'bad_date': facts['service_date'] = '2026-02-30'
    if change == 'numeric_date': facts['service_date'] = 0
    if change == 'calendar_overflow': facts['activities'][0]['start'] = '9999-12-31T23:59+00:00'
    assert save(client, facts)[0].status_code == 422
    assert client.get('/drafts').json() == {'drafts': []}


def test_expiry_session_operation_and_purge_boundaries(client, users):
    assert login(client, users).status_code == 200
    response, body = save(client)
    identifier = response.json()['id']
    unused = issue(client)
    with database() as conn:
        conn.execute("UPDATE draft_operations SET expires_at=clock_timestamp() WHERE id=%s", (unused,))
    assert save(client, operation=unused)[0].status_code == 410
    with database() as conn:
        conn.execute("UPDATE drafts SET created_at=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (identifier,))
        conn.execute('UPDATE draft_operations SET expires_at=(SELECT expires_at FROM drafts WHERE id=%s) WHERE draft_id=%s', (identifier, identifier))
    assert client.get('/drafts/' + identifier).status_code == 410
    assert client.get('/drafts').json() == {'drafts': []}
    assert client.post('/drafts', headers=headers(client), json=body).status_code == 410
    assert client.get('/draft-operations/' + body['operation_id']).status_code == 410
    assert client.post('/draft-operations', headers=headers(client), json={'draft_id': identifier}).status_code == 410
    assert client.post('/drafts/' + identifier, headers=headers(client), json=body).status_code == 410
    cleanup()
    assert client.post('/drafts', headers=headers(client), json=body).status_code == 404
    assert save(client, operation=unused)[0].status_code == 404
    with database() as conn:
        assert conn.execute('SELECT count(*) AS n FROM drafts WHERE owner=%s', (users[1][0],)).fetchone()['n'] == 0
        conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner=%s", (users[1][0],))
    assert client.get('/drafts').status_code == 401
    assert save(client, operation=str(uuid4()))[0].status_code == 401


def test_nulls_zero_interval_request_bounds(client, users):
    assert login(client, users).status_code == 200
    facts = content()
    facts['service_date'] = None
    facts['activities'][0]['end'] = facts['activities'][0]['start']
    assert save(client, facts)[0].status_code == 200
    assert client.post('/drafts', headers=headers(client), content=b'x' * 1048577).status_code == 413
    assert client.post('/auth/login', headers=headers(client), content=b'x' * 4097).status_code == 413


def wait_for_blocker(identifier):
    deadline = time.monotonic() + 5
    with database() as observer:
        while time.monotonic() < deadline:
            observer.execute('SELECT pg_stat_clear_snapshot()')
            if observer.execute('SELECT 1 FROM pg_stat_activity WHERE %s=ANY(pg_blocking_pids(pid))', (identifier,)).fetchone():
                return
            time.sleep(.01)
    raise AssertionError('Expected request to reach the held row lock')


@pytest.mark.parametrize('action', ['read', 'issue', 'lookup', 'replay', 'update'])
def test_blocking_draft_or_operation_lock_cannot_outlive_session(client, users, action):
    assert login(client, users).status_code == 200
    response, accepted_body = save(client)
    identifier = response.json()['id']
    operation = issue(client, identifier)
    proof, cookies = headers(client), dict(client.cookies)
    with database() as blocker, concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        if action in {'lookup', 'replay'}:
            blocker.execute('SELECT id FROM draft_operations WHERE id=%s FOR UPDATE', (accepted_body['operation_id'],))
        else:
            blocker.execute('SELECT id FROM drafts WHERE id=%s FOR UPDATE', (identifier,))
        with database() as setup:
            expiry = setup.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days'+interval '1 second', expires_at=statement_timestamp()+interval '1 second' WHERE owner=%s RETURNING expires_at", (users[1][0],)).fetchone()['expires_at']

        def blocked_request():
            with httpx.Client(base_url=URL, cookies=cookies, timeout=10) as remote:
                if action == 'read': return remote.get('/drafts/' + identifier)
                if action == 'lookup': return remote.get('/draft-operations/' + accepted_body['operation_id'])
                if action == 'issue': return remote.post('/draft-operations', headers=proof, json={'draft_id': identifier})
                if action == 'replay': return remote.post('/drafts', headers=proof, json=accepted_body)
                return remote.post('/drafts/' + identifier, headers=proof, json={'operation_id': operation, 'expected_revision': 1, 'draft': content()})

        future = pool.submit(blocked_request)
        try:
            wait_for_blocker(blocker.info.backend_pid)
            with database() as observer:
                observer.execute('SELECT pg_sleep(GREATEST(0,extract(epoch FROM (%s::timestamptz-clock_timestamp()))+.05))', (expiry,))
        finally:
            blocker.commit()
        assert future.result().status_code == 401
    with database() as conn:
        assert conn.execute('SELECT revision FROM drafts WHERE id=%s', (identifier,)).fetchone()['revision'] == 1
        assert conn.execute('SELECT result FROM draft_operations WHERE id=%s', (operation,)).fetchone()['result'] is None


def test_cleanup_and_expired_request_follow_session_before_draft_locks(client, users, monkeypatch):
    from app import draft_storage
    assert login(client, users).status_code == 200
    response, _ = save(client)
    identifier = response.json()['id']
    request = SimpleNamespace(cookies={auth.SESSION: client.cookies.get(auth.SESSION)})
    entered, release = threading.Event(), threading.Event()
    state = {}
    original = draft_storage.owned

    def gated_owned(*args):
        state['pid'] = args[0].info.backend_pid
        entered.set()
        assert release.wait(5)
        return original(*args)

    monkeypatch.setattr(draft_storage, 'owned', gated_owned)
    with database() as conn:
        expiry = conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days'+interval '1 second',expires_at=statement_timestamp()+interval '1 second' WHERE owner=%s RETURNING expires_at", (users[1][0],)).fetchone()['expires_at']
        conn.execute("UPDATE drafts SET created_at=%s::timestamptz-interval '7 days',expires_at=%s WHERE id=%s", (expiry, expiry, identifier))
        conn.execute('UPDATE draft_operations SET expires_at=%s WHERE draft_id=%s', (expiry, identifier))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        read = pool.submit(draft_storage.read, request, identifier)
        assert entered.wait(3)
        with database() as observer:
            observer.execute('SELECT pg_sleep(GREATEST(0,extract(epoch FROM (%s::timestamptz-clock_timestamp()))+.05))', (expiry,))
        purge = pool.submit(cleanup)
        try:
            wait_for_blocker(state['pid'])
        finally:
            release.set()
        with pytest.raises(HTTPException) as denied:
            read.result(timeout=5)
        assert denied.value.status_code == 401
        purge.result(timeout=5)
