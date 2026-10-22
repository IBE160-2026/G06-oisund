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
        conn.execute('DELETE FROM draft_deletions WHERE owner=ANY(%s)', (users[1],))


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


def test_combined_import_correction_structure_and_fixed_expiry(client, users):
    import copy
    from app.private_import import interpret
    from app.pdf_import import parse_document
    from test_pdf_import import synthetic_text_pdf
    assert login(client, users).status_code == 200
    facts = interpret(parse_document(synthetic_text_pdf())).model_dump(mode='json', exclude_none=False)
    original_metadata = copy.deepcopy(facts['import_metadata'])
    first, _ = save(client, facts)
    assert first.status_code == 200
    original = first.json()
    facts = copy.deepcopy(original['draft'])
    anchor = facts['activities'][-1]['id']
    facts['vehicle_duty_changes'] = [{'from_activity_id': anchor, 'vehicle_duty': 'CAR - 1', 'realtime_duty': None}]
    facts['activities'][0].update(type='Manuelt arbeid', from_place='Manuelt sted', trip='001')
    manual = content()['activities'][0]
    facts['activities'] = [facts['activities'][-1], manual, *facts['activities'][:-1]]
    updated, body = save(client, facts, original['id'], 1)
    assert updated.status_code == 200
    result = updated.json()
    assert result['draft'] == body['draft']
    assert result['draft']['import_metadata'] == original_metadata
    assert result['expires_at'] == original['expires_at']
    assert client.get('/drafts/' + original['id']).json() == result
    assert result['draft']['activities'][1]['type'] is None
    assert result['draft']['activities'][1]['from_place'] is None
    assert result['draft']['vehicle_duty_changes'][0]['from_activity_id'] == anchor


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


@pytest.mark.parametrize('change', ['negative', 'summer_offset', 'spring_gap', 'no_offset', 'duplicate', 'bus', 'too_many', 'bad_date', 'numeric_date', 'calendar_overflow', 'offset_minutes_60', 'offset_minutes_winter', 'offset_hour_24'])
def test_validation_preserves_unknowns_rejects_contradictions(client, users, change):
    assert login(client, users).status_code == 200
    facts = content()
    if change == 'negative': facts['activities'][0]['end'] = '2026-10-24T23:59+02:00'
    if change == 'summer_offset': facts['activities'][0]['start'] = '2026-07-01T12:00+01:00'
    if change == 'spring_gap': facts['activities'][0]['start'] = '2026-03-29T02:30+01:00'
    if change == 'no_offset': facts['activities'][0]['start'] = '2026-10-25T00:00'
    if change == 'duplicate': facts['activities'].append(facts['activities'][0])
    if change == 'bus': facts['physical_bus'] = 'x' * 101
    if change == 'too_many': facts['activities'] *= 201
    if change == 'bad_date': facts['service_date'] = '2026-02-30'
    if change == 'numeric_date': facts['service_date'] = 0
    if change == 'calendar_overflow': facts['activities'][0]['start'] = '9999-12-31T23:59+00:00'
    if change == 'offset_minutes_60': facts['activities'][0]['start'] = '2026-10-25T00:00+01:60'
    if change == 'offset_minutes_winter': facts['activities'][0]['start'] = '2026-01-01T12:00+00:60'
    if change == 'offset_hour_24': facts['activities'][0]['start'] = '2026-10-25T00:00+24:00'
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


def test_transient_import_save_reopen_replay_and_access(client, users):
    from pathlib import Path
    from app.qualify_imports import ORACLE
    import json
    expected = json.loads(ORACLE.read_text())['fixtures']
    assert client.post('/imports/pdf', headers={**headers(client), 'Content-Type': 'application/pdf'}, content=b'%PDF-').status_code == 401
    assert login(client, users).status_code == 200
    for fixture in expected:
        data = (Path('/fixtures') / fixture['file']).read_bytes()
        assert client.post('/imports/pdf', content=data).status_code == 403
        result = client.post('/imports/pdf', headers={**headers(client), 'Content-Type': 'application/pdf'}, content=data)
        assert result.status_code == 200 and result.headers['cache-control'] == 'no-store'
        facts = result.json()
        assert facts['physical_bus'] is None and len(facts['activities']) == len(fixture['activities'])
        assert client.get('/drafts').json() == {'drafts': []}
        saved, body = save(client, facts)
        assert saved.status_code == 200 and saved.json()['draft'] == facts
        record = saved.json()
        assert client.get('/drafts/' + record['id']).json() == record
        assert client.post('/drafts', headers=headers(client), json=body).json() == record
        assert client.get('/draft-operations/' + body['operation_id']).json()['result'] == record
        changed = {**facts, 'physical_bus': 'Manual-001'}
        updated, _ = save(client, changed, record['id'], 1)
        assert updated.json()['draft']['import_metadata'] == facts['import_metadata']
        assert updated.json()['expires_at'] == record['expires_at']
        with database() as conn:
            conn.execute('DELETE FROM drafts WHERE id=%s', (record['id'],))
    assert client.post('/imports/pdf', headers=headers(client), content=b'%PDF-').status_code == 415
    assert client.post('/imports/pdf', headers={**headers(client), 'Content-Type': 'application/pdf'}, content=b'x' * (10 * 1024 * 1024 + 1)).status_code == 413
    with database() as conn:
        conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days', expires_at=statement_timestamp() WHERE owner=%s", (users[1][0],))
    assert client.post('/imports/pdf', headers={**headers(client), 'Content-Type': 'application/pdf'}, content=b'%PDF-').status_code == 401


@pytest.mark.parametrize('number', [8, 9])
def test_additional_import_save_reopen_replay(client, users, number):
    from pathlib import Path
    from test_private_import import assert_additional
    assert login(client, users).status_code == 200
    data = Path(f'/fixtures/Eksempel-{number}-anonymisert.pdf').read_bytes()
    result = client.post('/imports/pdf', headers={**headers(client), 'Content-Type': 'application/pdf'}, content=data)
    assert result.status_code == 200
    facts = result.json()
    assert_additional(facts, number)
    assert client.get('/drafts').json() == {'drafts': []}
    saved, body = save(client, facts)
    assert saved.status_code == 200
    record = saved.json()
    assert record['draft'] == facts
    assert client.get('/drafts/' + record['id']).json() == record
    assert client.post('/drafts', headers=headers(client), json=body).json() == record
    assert client.get('/draft-operations/' + body['operation_id']).json()['result'] == record
    assert_additional(record['draft'], number)


def test_duty_changes_roundtrip_replay_and_removal(client, users):
    assert login(client, users).status_code == 200
    facts = content()
    second = {**facts['activities'][0], 'id': str(uuid4())}
    third = {**second, 'id': str(uuid4())}
    facts['activities'] += [second, third]
    facts['vehicle_duty'] = '960181'
    facts['realtime_duty'] = '181'
    facts['vehicle_duty_changes'] = [{'from_activity_id': second['id'], 'vehicle_duty': '960176', 'realtime_duty': '176'}]
    saved, body = save(client, facts)
    assert saved.status_code == 200
    record = saved.json()
    assert record['draft'] == facts
    assert client.get('/drafts/' + record['id']).json() == record
    assert client.post('/drafts', headers=headers(client), json=body).json() == record
    facts['vehicle_duty_changes'] = []
    cleared, _ = save(client, facts, record['id'], 1)
    assert cleared.status_code == 200 and cleared.json()['draft']['vehicle_duty_changes'] == []
    assert cleared.json()['expires_at'] == record['expires_at']
    assert client.get('/drafts/' + record['id']).json() == cleared.json()


def wait_for_blocker(identifier):
    deadline = time.monotonic() + 5
    with database() as observer:
        while time.monotonic() < deadline:
            observer.execute('SELECT pg_stat_clear_snapshot()')
            if observer.execute('SELECT 1 FROM pg_stat_activity WHERE %s=ANY(pg_blocking_pids(pid))', (identifier,)).fetchone():
                return
            time.sleep(.01)
    raise AssertionError('Expected request to reach the held row lock')


@pytest.mark.parametrize('action', ['read', 'issue', 'lookup', 'replay', 'update', 'delete'])
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
                if action == 'delete': return remote.post('/drafts/' + identifier + '/delete', headers=proof, json={'operation_id': str(uuid4()), 'expected_revision': 1})
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


@pytest.mark.parametrize('duty,derived', [('0007', '007'), ('AB001', '001'), ('1234', '234'), ('12', None), ('007x', None), (None, None)])
def test_bus_is_manual_and_realtime_is_derived(client, users, duty, derived):
    assert login(client, users).status_code == 200
    facts = content()
    facts.update(vehicle_duty=duty, realtime_duty='999', physical_bus='Bus-0012')
    response, body = save(client, facts)
    assert response.status_code == 200
    original = response.json()
    assert original['draft']['realtime_duty'] == derived
    assert original['draft']['physical_bus'] == 'Bus-0012'
    assert client.get('/drafts/' + original['id']).json() == original
    facts.update(vehicle_duty='D009', physical_bus='Bus-0008')
    updated, _ = save(client, facts, original['id'], 1)
    assert updated.json()['draft']['realtime_duty'] == '009'
    assert updated.json()['draft']['physical_bus'] == 'Bus-0008'
    assert updated.json()['expires_at'] == original['expires_at']


def test_legacy_draft_operation_normalizes_without_rewriting(client, users):
    from app.draft_storage import fingerprint
    from psycopg.types.json import Jsonb
    assert login(client, users).status_code == 200
    response, body = save(client)
    original = response.json()
    legacy = {**original['draft'], 'realtime_duty': '999'}
    legacy_result = {**original, 'draft': legacy}
    legacy_body = {**body, 'draft': legacy}
    legacy_hash = fingerprint(None, legacy_body)
    with database() as conn:
        conn.execute('UPDATE drafts SET content=%s WHERE id=%s', (Jsonb(legacy), original['id']))
        conn.execute('UPDATE draft_operations SET result=%s,payload_hash=%s WHERE id=%s', (Jsonb(legacy_result), legacy_hash, body['operation_id']))
    assert client.get('/drafts/' + original['id']).json() == original
    assert client.post('/drafts', headers=headers(client), json=legacy_body).json() == original
    assert client.get('/draft-operations/' + body['operation_id']).json()['result'] == original
    legacy_body['draft'] = {**legacy, 'physical_bus': 'changed-fact'}
    assert client.post('/drafts', headers=headers(client), json=legacy_body).status_code == 409
    with database() as conn:
        assert conn.execute('SELECT content FROM drafts WHERE id=%s', (original['id'],)).fetchone()['content'] == legacy
        stored = conn.execute('SELECT result,payload_hash FROM draft_operations WHERE id=%s', (body['operation_id'],)).fetchone()
        assert stored == {'result': legacy_result, 'payload_hash': legacy_hash}


def test_delete_is_owned_revision_checked_and_replayable_without_resurrection(client, users):
    assert login(client, users).status_code == 200
    response, save_body = save(client)
    identifier = response.json()['id']
    other_draft, _ = save(client)
    path = '/drafts/' + identifier + '/delete'
    deletion = {'operation_id': str(uuid4()), 'expected_revision': 1}
    with httpx.Client(base_url=URL) as other:
        assert other.post(path, headers=headers(other), json=deletion).status_code == 401
        assert login(other, users, 1).status_code == 200
        assert other.post(path, headers=headers(other), json=deletion).status_code == 404
    assert client.post(path, json=deletion).status_code == 403
    assert client.post(path, headers={**headers(client), 'Origin': 'http://evil.invalid'}, json=deletion).status_code == 403
    assert client.post(path, headers=headers(client), json={**deletion, 'expected_revision': 2}).status_code == 409
    accepted = client.post(path, headers=headers(client), json=deletion)
    assert accepted.status_code == 200 and accepted.json() == {'deleted_id': identifier}
    assert accepted.headers['cache-control'] == 'no-store'
    assert client.post(path, headers=headers(client), json=deletion).json() == accepted.json()
    assert client.get('/draft-deletions/' + deletion['operation_id']).json() == accepted.json()
    assert client.post(path, headers=headers(client), json={**deletion, 'expected_revision': 2}).status_code == 409
    assert client.get('/drafts/' + identifier).status_code == 404
    assert client.get('/draft-operations/' + save_body['operation_id']).status_code == 404
    assert client.post('/drafts', headers=headers(client), json=save_body).status_code == 404
    assert client.get('/drafts/' + other_draft.json()['id']).status_code == 200
    with httpx.Client(base_url=URL) as other:
        assert login(other, users, 1).status_code == 200
        assert other.get('/draft-deletions/' + deletion['operation_id']).status_code == 404
        assert other.post(path, headers=headers(other), json=deletion).status_code == 404
    with database() as conn:
        tombstone = conn.execute('SELECT * FROM draft_deletions WHERE id=%s', (deletion['operation_id'],)).fetchone()
        assert tombstone['expires_at'].isoformat().replace('+00:00', 'Z') == response.json()['expires_at']
        assert not conn.execute('SELECT 1 FROM draft_operations WHERE draft_id=%s', (identifier,)).fetchone()
        conn.execute('UPDATE draft_deletions SET expires_at=clock_timestamp() WHERE id=%s', (deletion['operation_id'],))
    assert client.get('/draft-deletions/' + deletion['operation_id']).status_code == 410
    cleanup()
    assert client.get('/draft-deletions/' + deletion['operation_id']).status_code == 404


def test_expired_draft_cannot_be_deleted(client, users):
    assert login(client, users).status_code == 200
    response, _ = save(client)
    identifier = response.json()['id']
    with database() as conn:
        conn.execute("UPDATE drafts SET created_at=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (identifier,))
    assert client.post('/drafts/' + identifier + '/delete', headers=headers(client), json={'operation_id': str(uuid4()), 'expected_revision': 1}).status_code == 410
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM draft_deletions WHERE draft_id=%s', (identifier,)).fetchone()


@pytest.mark.parametrize('day,clock,state,candidates', [
    ('2026-01-15', '12:30', 'resolved', ['2026-01-15T12:30+01:00']),
    ('2026-07-15', '12:30', 'resolved', ['2026-07-15T12:30+02:00']),
    ('2026-07-16', '00:10:15', 'resolved', ['2026-07-16T00:10:15+02:00']),
    ('2026-03-29', '02:30', 'gap', []),
    ('2026-10-25', '02:30', 'ambiguous', ['2026-10-25T02:30+02:00', '2026-10-25T02:30+01:00']),
    ('1894-01-01', '12:00', 'resolved', ['1894-01-01T12:00+00:43']),
    ('9999-12-31', '23:59', 'resolved', ['9999-12-31T23:59+01:00']),
])
def test_local_time_resolution_is_authoritative_without_storage_changes(client, users, day, clock, state, candidates):
    assert login(client, users).status_code == 200
    response = client.post('/draft-times/resolve', headers=headers(client), json={'calendar_date': day, 'clock': clock})
    assert response.status_code == 200 and response.json() == {'state': state, 'candidates': candidates}
    assert response.headers['cache-control'] == 'no-store'
    assert client.get('/drafts').json() == {'drafts': []}


@pytest.mark.parametrize('day,clock', [('2026-02-30', '12:00'), ('2026-01-01', '24:00'), ('2026-01-01', '12:60'), ('2026-01-01', '12:00+01:00'), ('10000-01-01', '23:59'), ('0001-01-01', '00:00')])
def test_local_time_resolution_rejects_invalid_or_unrepresentable_values(client, users, day, clock):
    assert login(client, users).status_code == 200
    assert client.post('/draft-times/resolve', headers=headers(client), json={'calendar_date': day, 'clock': clock}).status_code == 422


def test_local_time_resolution_reuses_session_csrf_and_bounds(client, users):
    facts = {'calendar_date': '2026-07-15', 'clock': '12:30'}
    assert client.post('/draft-times/resolve', headers=headers(client), json=facts).status_code == 401
    assert login(client, users).status_code == 200
    assert client.post('/draft-times/resolve', json=facts).status_code == 403
    assert client.post('/draft-times/resolve', headers={**headers(client), 'Origin': 'http://evil.invalid'}, json=facts).status_code == 403
    assert client.post('/draft-times/resolve', headers=headers(client), content=b'x' * 4097).status_code == 413
    with database() as conn:
        conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner=%s", (users[1][0],))
    assert client.post('/draft-times/resolve', headers=headers(client), json=facts).status_code == 401
