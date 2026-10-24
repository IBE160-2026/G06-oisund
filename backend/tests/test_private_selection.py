"""Exact-member choices and shared mutable-resource integrity on synthetic PostgreSQL."""
import concurrent.futures
from contextlib import contextmanager
from types import SimpleNamespace
from uuid import UUID, uuid4

import httpx
import pytest
from fastapi import HTTPException
from app import auth, workday_selection_storage, workday_lifecycle_storage
from app.private_storage import database, cleanup, migrate
from app.workday_selection_domain import SaveSelection
from app.workday_lifecycle_domain import StartWorkday
from test_private_access import client, headers, login, synthetic_only, users, URL
from test_private_workdays import prepare, confirm, facts, teardown


def opened(client, users):
    assert login(client, users).status_code == 200
    value = facts()
    value['activities'] = [dict(value['activities'][0], id=str(uuid4()), type=kind, line=line, direction=direction, start=start, end=end)
        for kind, line, direction, start, end in [
            ('trip', '20', 'A', '2031-01-02T23:00+01:00', '2031-01-02T23:10+01:00'),
            ('trip', '24', 'B', '2031-01-02T23:00+01:00', '2031-01-02T23:10+01:00'),
            ('Coffee', None, None, '2031-01-02T23:10+01:00', '2031-01-02T23:20+01:00'),
            ('MealBreak', None, None, '2031-01-02T23:20+01:00', '2031-01-02T23:30+01:00'),
            ('deadhead', '20', 'B', '2031-01-03T00:00+01:00', '2031-01-03T00:10+01:00')]]
    draft, _, decisions = prepare(client, value)
    reply = confirm(client, draft, decisions)
    assert reply.status_code == 200
    return draft, reply.json()


def body(plan, resource, revision=0):
    return {'operation_id': str(uuid4()), 'expected_revision': revision,
            **({'activity_id': plan['draft']['activities'][revision % len(plan['draft']['activities'])]['id']} if resource == 'selection' else {})}


def routes(plan, resource):
    return '/workdays/' + plan['id'] + '/' + resource, '/workdays/' + plan['id'] + '/' + ('lifecycle' if resource == 'start' else resource)


def test_every_exact_member_equal_time_overnight_immutable_without_start(client, users):
    draft, plan = opened(client, users)
    path, _ = routes(plan, 'selection')
    assert client.get(path).json() == {'workday_id': plan['id'], 'activity_id': None, 'revision': 0, 'expires_at': plan['expires_at']}
    initial_start = client.get('/workdays/' + plan['id'] + '/lifecycle').json()
    bus = client.get('/workdays/' + plan['id'] + '/physical-bus').json()
    for revision, activity in enumerate(plan['draft']['activities']):
        payload = {**body(plan, 'selection', revision), 'activity_id': activity['id']}
        response = client.post(path, headers=headers(client), json=payload)
        assert response.status_code == 200
        receipt = response.json()
        assert receipt['result']['activity_id'] == activity['id'] and receipt['result']['revision'] == revision + 1
        assert client.get(path).json() == receipt['result']
        assert client.get('/workday-selection-operations/' + payload['operation_id']).json() == receipt
        assert client.post(path, headers=headers(client), json=payload).json() == receipt
        assert client.get('/workdays/' + plan['id']).json() == plan
        assert client.get('/drafts/' + draft['id']).json() == draft
        assert client.get('/workdays/' + plan['id'] + '/physical-bus').json() == bus
        assert client.get('/workdays/' + plan['id'] + '/lifecycle').json() == initial_start


@pytest.mark.parametrize('resource', ['selection', 'start'])
def test_strict_membership_access_fingerprints_and_delete_cascade(client, users, resource):
    draft, plan = opened(client, users)
    path, read = routes(plan, resource); payload = body(plan, resource)
    before = client.get(read).json()
    assert client.post(path, json=payload).status_code == 403
    assert client.post(path, headers={**headers(client), 'Origin': 'http://evil.invalid'}, json=payload).status_code == 403
    for invalid in [{**payload, 'operation_id': 'bad'}, {**payload, 'expected_revision': True}, {**payload, 'expected_revision': -1}, {**payload, 'expected_revision': '0'}, {**payload, 'extra': 1}]:
        assert client.post(path, headers=headers(client), json=invalid).status_code == 422
    if resource == 'selection':
        for invalid in [{**payload, 'activity_id': None}, {**payload, 'activity_id': str(uuid4())}, {**payload, 'activity_id': 'gap-before-x'}]:
            assert client.post(path, headers=headers(client), json=invalid).status_code == 422
    assert client.get(read).json() == before
    receipt = client.post(path, headers=headers(client), json=payload).json()
    lookup = '/workday-' + resource + '-operations/' + payload['operation_id']
    for route in [read, lookup]: assert client.get(route).headers['cache-control'] == 'no-store'
    with httpx.Client(base_url=URL) as other:
        assert other.get(read).status_code == 401
        assert login(other, users, 1).status_code == 200
        foreign_draft, _, decision = prepare(other); foreign = confirm(other, foreign_draft, decision).json()
        for route in [read, lookup]: assert other.get(route).status_code == 404
        assert other.post(path, headers=headers(other), json=payload).status_code == 404
        if resource == 'selection':
            assert other.post(routes(foreign, resource)[0], headers=headers(other), json={**body(foreign, resource), 'activity_id': payload['activity_id']}).status_code == 422
    source, _, decision = prepare(client); other_plan = confirm(client, source, decision).json()
    assert client.post(routes(other_plan, resource)[0], headers=headers(client), json=payload).status_code == 409
    assert client.post(path, headers=headers(client), json={**payload, 'expected_revision': 4}).status_code == 409
    assert client.get(lookup).json() == receipt
    assert client.post('/workdays/' + plan['id'] + '/delete', headers=headers(client), json={'operation_id': str(uuid4()), 'source_revision': 1}).status_code == 200
    assert client.get(read).status_code == client.get(lookup).status_code == client.post(path, headers=headers(client), json=payload).status_code == 404
    with database() as conn:
        for table in ['workday_selections', 'workday_lifecycles', 'workday_selection_operations', 'workday_start_operations']:
            assert not conn.execute('SELECT 1 FROM ' + table + ' WHERE workday_id=%s', (plan['id'],)).fetchone()
    assert client.get('/drafts/' + draft['id']).json() == draft


@pytest.mark.parametrize('resource', ['selection', 'start'])
@pytest.mark.parametrize('boundary', ['session', 'plan'])
def test_final_atomic_expiry_rolls_back_effect_and_receipt(client, users, monkeypatch, resource, boundary):
    _, plan = opened(client, users)
    path, read = routes(plan, resource); initial = client.get(read).json()
    payload = (SaveSelection if resource == 'selection' else StartWorkday)(**body(plan, resource))
    request = SimpleNamespace(cookies={auth.SESSION: client.cookies.get(auth.SESSION)})
    class Connection:
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            if query.startswith('INSERT INTO workday_' + resource + '_operations'):
                if boundary == 'plan': self.conn.execute("UPDATE workdays SET final_end=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (plan['id'],))
                else: self.conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner=%s", (users[1][0],))
            return self.conn.execute(query, params)
    @contextmanager
    def wrapped():
        with database() as conn: yield Connection(conn)
    storage = workday_selection_storage if resource == 'selection' else workday_lifecycle_storage
    monkeypatch.setattr(storage, 'database', wrapped)
    with pytest.raises(HTTPException) as error: storage.save(request, UUID(plan['id']), payload)
    assert error.value.status_code == (410 if boundary == 'plan' else 401)
    assert client.get(read).json() == initial
    with database() as conn: assert not conn.execute('SELECT 1 FROM workday_' + resource + '_operations WHERE id=%s', (payload.operation_id,)).fetchone()


@pytest.mark.parametrize('resource', ['selection', 'start'])
def test_expiry_cleanup_and_bounded_admission_replay(client, users, resource):
    _, plan = opened(client, users)
    path, read = routes(plan, resource); payload = body(plan, resource)
    receipt = client.post(path, headers=headers(client), json=payload).json()
    table = 'workday_' + resource + '_operations'; lookup = '/workday-' + resource + '-operations/' + payload['operation_id']
    with database() as conn:
        conn.execute('INSERT INTO ' + table + ' SELECT gen_random_uuid(),owner,workday_id,payload_hash,result,expires_at FROM ' + table + ' CROSS JOIN generate_series(1,1999) WHERE id=%s', (payload['operation_id'],))
    assert client.post(path, headers=headers(client), json=body(plan, resource, 1)).status_code == 429
    assert client.get(read).json() == receipt['result']
    assert client.post(path, headers=headers(client), json=payload).json() == receipt
    with database() as conn: conn.execute('UPDATE ' + table + ' SET expires_at=clock_timestamp() WHERE id=%s', (payload['operation_id'],))
    assert client.get(lookup).status_code == client.post(path, headers=headers(client), json=payload).status_code == 410
    cleanup(); assert client.get(lookup).status_code == 404
    assert client.get(read).json() == receipt['result']
    with database() as conn: conn.execute("UPDATE workdays SET final_end=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (plan['id'],))
    assert client.get(read).status_code == client.post(path, headers=headers(client), json=payload).status_code == 410
    cleanup(); assert client.get(read).status_code == 404


def test_concurrent_selection_and_old_receipt_never_rollback(client, users):
    _, plan = opened(client, users); path, _ = routes(plan, 'selection')
    payloads = [body(plan, 'selection'), {**body(plan, 'selection'), 'activity_id': plan['draft']['activities'][1]['id']}]
    proof, cookies = headers(client), dict(client.cookies)
    def send(p): return httpx.post(URL + path, headers=proof, cookies=cookies, json=p, timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: replies = list(pool.map(send, payloads))
    assert sorted(r.status_code for r in replies) == [200, 409]
    index = next(i for i, r in enumerate(replies) if r.status_code == 200); old = replies[index].json()
    latest = client.post(path, headers=headers(client), json=body(plan, 'selection', 1)).json()
    assert client.post(path, headers=headers(client), json=payloads[index]).json() == old
    assert client.get('/workday-selection-operations/' + payloads[index]['operation_id']).json() == old
    assert client.get(path).json() == latest['result']


@pytest.mark.parametrize('resource', ['selection', 'start'])
def test_receipt_capacity_spans_plans_and_isolated_accounts_without_rejected_effect(client, users, resource):
    _, first = opened(client, users)
    def another():
        source, _, decision = prepare(client)
        return confirm(client, source, decision).json()
    second, untouched = another(), another()
    table = 'workday_' + resource + '_operations'
    receipts = []
    for plan, copies in [(first, 999), (second, 998)]:
        payload = body(plan, resource)
        receipt = client.post(routes(plan, resource)[0], headers=headers(client), json=payload)
        assert receipt.status_code == 200
        receipts.append((plan, payload, receipt.json()))
        with database() as conn:
            conn.execute('INSERT INTO ' + table + ' SELECT gen_random_uuid(),owner,workday_id,payload_hash,result,expires_at FROM ' + table + ' CROSS JOIN generate_series(1,%s) WHERE id=%s', (copies, payload['operation_id']))
    # The last available slot belongs to the account across both plans.
    final = client.post(routes(second, resource)[0], headers=headers(client), json=body(second, resource, 1))
    assert final.status_code == 200
    path, read = routes(untouched, resource); original = client.get(read).json(); rejected = body(untouched, resource)
    def state():
        with database() as conn:
            return {name: conn.execute('SELECT t.* FROM ' + name + ' t JOIN workdays w ON t.workday_id=w.id WHERE w.owner=%s ORDER BY t.workday_id,t.' + ('id' if name == table else 'revision'), (users[1][0],)).fetchall()
                    for name in [table, 'workday_selections' if resource == 'selection' else 'workday_lifecycles']}
    before = state(); assert len(before[table]) == 2000
    assert client.post(path, headers=headers(client), json=rejected).status_code == 429
    assert state() == before and client.get(read).json() == original
    plan, payload, receipt = receipts[0]
    assert client.post(routes(plan, resource)[0], headers=headers(client), json=payload).json() == receipt
    assert state() == before
    with httpx.Client(base_url=URL) as other:
        assert login(other, users, 1).status_code == 200
        source, _, decision = prepare(other); foreign = confirm(other, source, decision).json()
        response = other.post(routes(foreign, resource)[0], headers=headers(other), json=body(foreign, resource))
        assert response.status_code == 200 and response.json()['result']['revision'] == 1
    assert state() == before
