"""Bus resource matrix, exclusively on disposable synthetic PostgreSQL."""
import concurrent.futures
import threading
from contextlib import contextmanager
from types import SimpleNamespace
from uuid import UUID, uuid4
import httpx
import pytest
from fastapi import HTTPException
from psycopg.types.json import Jsonb
from app import auth, workday_bus_storage, draft_storage, workday_storage
from app.private_storage import database, cleanup
from app.workday_bus_domain import SaveBus
from app.workday_domain import DeleteWorkdayRequest
from test_private_drafts import wait_for_blocker
from test_private_access import client, headers, login, synthetic_only, users, URL
from test_private_workdays import prepare, confirm, facts, teardown


def opened(client, users, value=None):
    assert login(client, users).status_code == 200
    draft, _, decisions = prepare(client, value)
    plan = confirm(client, draft, decisions).json()
    return draft, plan, '/workdays/' + plan['id'] + '/physical-bus'


def body(value, revision=0):
    return {'operation_id': str(uuid4()), 'expected_revision': revision, 'physical_bus': value}


@pytest.mark.parametrize('duty', ['960006', '960090', 'CAR - 1'])
def test_format_correct_clear_reopen_immutable_snapshot_source_and_deadline(client, users, duty):
    value = facts(); value.update(vehicle_duty=duty, physical_bus=' 0012-A ')
    draft, plan, path = opened(client, users, value)
    original = client.get(path).json()
    assert original == {'workday_id': plan['id'], 'physical_bus': ' 0012-A ', 'revision': 0, 'expires_at': plan['expires_at']}
    for revision, text in enumerate([' 000006 / 090 ', 'Buss-009', '', '   ', None], 1):
        payload = body(text, revision - 1)
        reply = client.post(path, headers=headers(client), json=payload)
        assert reply.status_code == 200
        receipt = reply.json()
        assert receipt['result'] == {**original, 'physical_bus': text if text and text.strip() else None, 'revision': revision}
        assert client.get(path).json() == receipt['result']
        assert client.get('/workday-bus-operations/' + payload['operation_id']).json() == receipt
        assert client.post(path, headers=headers(client), json=payload).json() == receipt
        assert client.get('/workdays/' + plan['id']).json() == plan
        assert client.get('/drafts/' + draft['id']).json() == draft


def test_concurrency_old_receipt_and_changed_payload_do_not_revert_newer_value(client, users):
    _, plan, path = opened(client, users)
    assert client.get(path).json()['physical_bus'] is None
    payloads = [body('0006'), body('0090')]
    proof, cookies = headers(client), dict(client.cookies)
    def send(payload): return httpx.post(URL + path, headers=proof, cookies=cookies, json=payload, timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: replies = list(pool.map(send, payloads))
    assert sorted(reply.status_code for reply in replies) == [200, 409]
    index = next(i for i, reply in enumerate(replies) if reply.status_code == 200)
    first = replies[index].json()
    newer = client.post(path, headers=headers(client), json=body('new', 1)).json()
    assert client.post(path, headers=headers(client), json=payloads[index]).json() == first
    assert client.get('/workday-bus-operations/' + payloads[index]['operation_id']).json() == first
    assert client.get(path).json() == newer['result']
    assert client.post(path, headers=headers(client), json={**payloads[index], 'physical_bus': 'changed'}).status_code == 409


def test_guards_bounds_no_store_and_deleted_cascade(client, users):
    _, plan, path = opened(client, users)
    payload = body('0' * 100)
    assert client.post(path, json=payload).status_code == 403
    assert client.post(path, headers={**headers(client), 'Origin': 'http://evil.invalid'}, json=payload).status_code == 403
    for invalid in [body('x' * 101), body('A\0B'), body(12), body('A', True), {**payload, 'extra': 1}]:
        assert client.post(path, headers=headers(client), json=invalid).status_code == 422
    assert client.post(path, headers=headers(client), content=b'x'*4097).status_code == 413
    assert client.get(path).json()['revision'] == 0
    receipt = client.post(path, headers=headers(client), json=payload).json()
    lookup = '/workday-bus-operations/' + payload['operation_id']
    for route in [path, lookup]: assert client.get(route).headers['cache-control'] == 'no-store'
    with httpx.Client(base_url=URL) as other:
        assert other.get(path).status_code == 401
        assert login(other, users, 1).status_code == 200
        for route in [path, lookup]: assert other.get(route).status_code == 404
        assert other.post(path, headers=headers(other), json=payload).status_code == 404
    assert client.post('/workdays/' + plan['id'] + '/delete', headers=headers(client), json={'operation_id': str(uuid4()), 'source_revision': 1}).status_code == 200
    for route in [path, lookup]: assert client.get(route).status_code == 404
    assert client.post(path, headers=headers(client), json=payload).status_code == 404
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM workday_buses WHERE workday_id=%s', (plan['id'],)).fetchone()
        assert not conn.execute('SELECT 1 FROM workday_bus_operations WHERE id=%s', (payload['operation_id'],)).fetchone()


@pytest.mark.parametrize('boundary', ['session', 'plan'])
def test_atomic_expiry_rolls_back_bus_and_receipt(client, users, monkeypatch, boundary):
    _, plan, path = opened(client, users)
    payload = SaveBus(**body('0012'))
    request = SimpleNamespace(cookies={auth.SESSION: client.cookies.get(auth.SESSION)})
    class Connection:
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            if query.startswith('INSERT INTO workday_bus_operations'):
                if boundary == 'plan': self.conn.execute("UPDATE workdays SET final_end=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (plan['id'],))
                else: self.conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner=%s", (users[1][0],))
            return self.conn.execute(query, params)
    @contextmanager
    def wrapped():
        with database() as conn: yield Connection(conn)
    monkeypatch.setattr(workday_bus_storage, 'database', wrapped)
    with pytest.raises(HTTPException) as error: workday_bus_storage.save(request, UUID(plan['id']), payload)
    assert error.value.status_code == (410 if boundary == 'plan' else 401)
    assert client.get(path).json()['revision'] == 0
    assert client.get('/workdays/' + plan['id']).json() == plan
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM workday_bus_operations WHERE id=%s', (payload.operation_id,)).fetchone()


def test_expired_plan_read_retry_lookup_denied_and_cleanup_cascades(client, users):
    _, plan, path = opened(client, users)
    payload = body('0012')
    assert client.post(path, headers=headers(client), json=payload).status_code == 200
    with database() as conn:
        conn.execute("UPDATE workdays SET final_end=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (plan['id'],))
    assert client.get(path).status_code == 410
    assert client.post(path, headers=headers(client), json=payload).status_code == 410
    assert client.get('/workday-bus-operations/' + payload['operation_id']).status_code == 410
    cleanup()
    assert client.get(path).status_code == 404


def test_unicode_limit_and_receipt_admission_are_bounded_without_mutation(client, users):
    _, plan, path = opened(client, users)
    payload = body('🚍' * 100)
    reply = client.post(path, headers=headers(client), json=payload)
    assert reply.status_code == 200 and reply.json()['result']['physical_bus'] == '🚍' * 100
    assert client.post(path, headers=headers(client), json=body('🚍' * 101, 1)).status_code == 422
    with httpx.Client(base_url=URL) as other:
        assert login(other, users, 1).status_code == 200
        source, _, decisions = prepare(other)
        foreign = confirm(other, source, decisions).json()
    with database() as conn:
        receipt = conn.execute('SELECT * FROM workday_bus_operations WHERE id=%s', (payload['operation_id'],)).fetchone()
        for owner, target, count, expired in [(receipt['owner'], plan['id'], 1998, False), (receipt['owner'], plan['id'], 3, True), (users[1][1], foreign['id'], 2001, False)]:
            conn.execute('INSERT INTO workday_bus_operations SELECT unnest(%s::uuid[]),%s,%s,%s,%s,CASE WHEN %s THEN statement_timestamp() ELSE %s END',
                         ([uuid4() for _ in range(count)], owner, target, receipt['payload_hash'], Jsonb({**receipt['result'], 'workday_id': target}), expired, receipt['expires_at']))
    final = client.post(path, headers=headers(client), json=body('final slot', 1))
    assert final.status_code == 200 and final.json()['result']['revision'] == 2
    def state():
        with database() as conn:
            return [conn.execute('SELECT * FROM '+table+' ORDER BY '+key).fetchall() for table, key in [('workday_buses', 'workday_id'), ('workday_bus_operations', 'id')]]
    before = state()
    assert client.post(path, headers=headers(client), json=body('denied', 2)).status_code == 429
    assert state() == before
    assert client.get(path).json() == final.json()['result']
    assert client.post(path, headers=headers(client), json=payload).json() == reply.json()
    assert state() == before


@pytest.mark.parametrize('value,expected', [('\u0085', None), (' \u0085\t', None), ('\u1680\u2003\u2028\u202f\u205f\u3000', None), ('\u001c', '\u001c'), ('\ufeff', '\ufeff'), (' \u0085A\ufeff ', ' \u0085A\ufeff ')])
def test_explicit_unicode_whitespace_preserves_meaningful_formatting(client, users, value, expected):
    _, plan, path = opened(client, users)
    payload = body(value)
    receipt = client.post(path, headers=headers(client), json=payload)
    assert receipt.status_code == 200 and receipt.json()['result']['physical_bus'] == expected
    assert client.get(path).json() == receipt.json()['result']
    assert client.post(path, headers=headers(client), json=payload).json() == receipt.json()
    assert client.get('/workdays/' + plan['id']).json() == plan


def test_accepted_nonce_cannot_target_another_owned_plan(client, users):
    draft, first, path = opened(client, users)
    source, _, decisions = prepare(client)
    second = confirm(client, source, decisions).json()
    second_path = '/workdays/' + second['id'] + '/physical-bus'
    payload = body('0012')
    receipt = client.post(path, headers=headers(client), json=payload).json()
    other_bus = client.get(second_path).json()
    assert client.post(second_path, headers=headers(client), json=payload).status_code == 409
    assert client.get(path).json() == receipt['result']
    assert client.get(second_path).json() == other_bus
    assert client.get('/workday-bus-operations/' + payload['operation_id']).json() == receipt
    for plan in [first, second]: assert client.get('/workdays/' + plan['id']).json() == plan
    for saved in [draft, source]: assert client.get('/drafts/' + saved['id']).json() == saved


@pytest.mark.parametrize('first', ['save', 'delete'])
def test_real_postgres_save_delete_contention_both_lock_orderings(client, users, monkeypatch, first):
    draft, plan, path = opened(client, users)
    source, _, decisions = prepare(client)
    unrelated = confirm(client, source, decisions).json()
    other_path = '/workdays/' + unrelated['id'] + '/physical-bus'
    other_bus = client.post(other_path, headers=headers(client), json=body('other')).json()
    request = SimpleNamespace(cookies={auth.SESSION: client.cookies.get(auth.SESSION)})
    payload = SaveBus(**body('0012'))
    deletion = DeleteWorkdayRequest(operation_id=uuid4(), source_revision=1)
    entered, release = threading.Event(), threading.Event()
    state = {}
    original = draft_storage.authorized
    def gated(conn, req):
        owner = original(conn, req)
        if not entered.is_set():
            state['pid'] = conn.info.backend_pid
            entered.set()
            assert release.wait(10)
        return owner
    monkeypatch.setattr(draft_storage, 'authorized', gated)
    def action(kind):
        try:
            result = workday_bus_storage.save(request, UUID(plan['id']), payload) if kind == 'save' else workday_storage.delete(request, UUID(plan['id']), deletion)
            return 200, result
        except HTTPException as error: return error.status_code, None
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        leader = pool.submit(action, first)
        assert entered.wait(5)
        follower = pool.submit(action, 'delete' if first == 'save' else 'save')
        try: wait_for_blocker(state['pid'])
        finally: release.set()
        assert leader.result(timeout=10)[0] == 200
        assert follower.result(timeout=10)[0] == (200 if first == 'save' else 404)
    assert client.get(path).status_code == 404
    assert client.post(path, headers=headers(client), json=payload.model_dump(mode='json')).status_code == 404
    assert client.get('/workday-bus-operations/' + str(payload.operation_id)).status_code == 404
    assert client.get('/workdays/' + unrelated['id']).json() == unrelated
    assert client.get(other_path).json() == other_bus['result']
    for saved in [draft, source]: assert client.get('/drafts/' + saved['id']).json() == saved
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM workday_buses WHERE workday_id=%s', (plan['id'],)).fetchone()
        assert not conn.execute('SELECT 1 FROM workday_bus_operations WHERE workday_id=%s', (plan['id'],)).fetchone()


def test_expired_receipt_denied_and_cleaned_while_parent_and_current_bus_survive(client, users):
    _, plan, path = opened(client, users)
    payload = body('0090')
    receipt = client.post(path, headers=headers(client), json=payload).json()
    with database() as conn:
        conn.execute('UPDATE workday_bus_operations SET expires_at=clock_timestamp() WHERE id=%s', (payload['operation_id'],))
    lookup = '/workday-bus-operations/' + payload['operation_id']
    assert client.get(lookup).status_code == 410
    assert client.post(path, headers=headers(client), json=payload).status_code == 410
    assert client.get(path).json() == receipt['result']
    cleanup()
    assert client.get(lookup).status_code == 404
    assert client.post(path, headers=headers(client), json=payload).status_code == 409
    assert client.get(path).json() == receipt['result']
    assert client.get('/workdays/' + plan['id']).json() == plan
