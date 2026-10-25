"""Synthetic real PostgreSQL/API manual outcomes, closure, receipts and retention."""
import concurrent.futures
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import UUID, uuid4
import httpx
import pytest
from fastapi import HTTPException
from app import auth, workday_outcome_storage
from app.private_storage import cleanup, database, migrate
from app.workday_outcome_domain import SaveOutcome
from app.workday_lifecycle_domain import CloseWorkday
from test_private_access import client, headers, login, synthetic_only, users, URL
from test_private_selection import opened
from test_private_workdays import prepare, confirm, facts, teardown


def outcome(plan, revision=0, member=0, value='completed'):
    return {'operation_id': str(uuid4()), 'expected_revision': revision, 'expected_lifecycle_revision': 1,
            'activity_id': plan['draft']['activities'][member]['id'], 'outcome': value}


def closing(revision=0, action='ended'):
    return {'operation_id': str(uuid4()), 'expected_revision': 1, 'expected_outcome_revision': revision, 'action': action}


def start(client, plan):
    reply = client.post('/workdays/' + plan['id'] + '/start', headers=headers(client), json={'operation_id': str(uuid4()), 'expected_revision': 0})
    assert reply.status_code == 200
    return reply.json()


def send(client, plan, resource, body):
    return client.post('/workdays/' + plan['id'] + '/' + resource, headers=headers(client), json=body)


def read(client, plan):
    result = client.get('/workdays/' + plan['id'] + '/recap')
    assert result.status_code == 200 and result.headers['cache-control'] == 'no-store'
    return result.json()


def test_prestart_consultation_selection_never_records_or_closes(client, users):
    _, plan = opened(client, users)
    original = read(client, plan)
    assert original['lifecycle']['state'] == 'confirmed'
    assert original['outcomes']['revision'] == 0
    assert [item['outcome'] for item in original['outcomes']['outcomes']] == ['unregistered'] * 5
    assert send(client, plan, 'outcome', outcome(plan)).status_code == 409
    assert send(client, plan, 'close', closing()).status_code == 409
    assert send(client, plan, 'selection', {'operation_id': str(uuid4()), 'expected_revision': 0, 'activity_id': plan['draft']['activities'][3]['id']}).status_code == 200
    assert read(client, plan) == original
    first = start(client, plan)
    assert read(client, plan)['outcomes'] == original['outcomes']
    assert first['result']['ended_at'] is None


def test_exact_ordered_members_corrections_all_values_pause_and_source_independence(client, users):
    source, plan = opened(client, users); start(client, plan)
    revision = 0
    for member in range(5):
        for value in ['completed', 'skipped', 'interrupted', 'unregistered']:
            before = read(client, plan)
            payload = outcome(plan, revision, member, value)
            response = send(client, plan, 'outcome', payload)
            assert response.status_code == 200
            receipt = response.json(); revision += 1
            expected = before['outcomes']['outcomes']
            expected[member]['outcome'] = value
            assert receipt['result']['revision'] == revision and receipt['result']['outcomes'] == expected
            assert send(client, plan, 'outcome', payload).json() == receipt
            assert client.get('/workday-outcome-operations/' + payload['operation_id']).json() == receipt
            assert read(client, plan)['outcomes'] == receipt['result']
            assert client.get('/workdays/' + plan['id']).json() == plan
            assert client.get('/drafts/' + source['id']).json() == source


@pytest.mark.parametrize('action', ['ended', 'aborted'])
def test_terminal_once_unknowns_unchanged_shortened_deadline_historical_retries_and_guards(client, users, action):
    _, plan = opened(client, users)
    first = start(client, plan)
    selection = {'operation_id': str(uuid4()), 'expected_revision': 0, 'activity_id': plan['draft']['activities'][1]['id']}
    selected = send(client, plan, 'selection', selection).json()
    bus = {'operation_id': str(uuid4()), 'expected_revision': 0, 'physical_bus': '0007'}
    saved_bus = send(client, plan, 'physical-bus', bus).json()
    saved_outcome_body = outcome(plan, value='skipped')
    saved_outcome = send(client, plan, 'outcome', saved_outcome_body).json()
    payload = closing(1, action)
    before = datetime.now(timezone.utc); response = send(client, plan, 'close', payload); after = datetime.now(timezone.utc)
    assert response.status_code == 200
    receipt = response.json(); terminal = receipt['result']
    end = datetime.fromisoformat(terminal['ended_at']); expiry = datetime.fromisoformat(terminal['expires_at'])
    assert before <= end <= after and expiry == end + timedelta(days=7)
    assert expiry < datetime.fromisoformat(plan['expires_at'])
    assert terminal['state'] == action and terminal['revision'] == 2 and terminal['started_at'] == first['result']['started_at']
    assert send(client, plan, 'close', payload).json() == receipt
    assert client.get('/workday-close-operations/' + payload['operation_id']).json() == receipt
    recap = read(client, plan)
    assert recap['outcomes']['outcomes'] == saved_outcome['result']['outcomes']
    assert [item['outcome'] for item in recap['outcomes']['outcomes']] == ['skipped'] + ['unregistered'] * 4
    assert recap['bus']['physical_bus'] == '0007'
    assert recap['plan'] == {**plan, 'expires_at': terminal['expires_at']}
    # Previously accepted effects stay immutable; current authority never rolls back.
    for resource, original, old in [('physical-bus', bus, saved_bus), ('selection', selection, selected), ('outcome', saved_outcome_body, saved_outcome)]:
        assert send(client, plan, resource, original).json() == old
        assert send(client, plan, resource, {**original, 'operation_id': str(uuid4()), 'expected_revision': 1}).status_code == 409
    for revision in [0, 1, 2]:
        assert send(client, plan, 'start', {'operation_id': str(uuid4()), 'expected_revision': revision}).status_code == 409
    assert send(client, plan, 'close', closing(1, 'aborted' if action == 'ended' else 'ended')).status_code == 409
    assert read(client, plan) == recap
    with database() as conn:
        for table in ['workday_operations', 'workday_start_operations', 'workday_bus_operations', 'workday_selection_operations', 'workday_outcome_operations', 'workday_close_operations']:
            assert all(row['expires_at'] <= expiry for row in conn.execute('SELECT expires_at FROM ' + table + ' WHERE workday_id=%s', (plan['id'],)).fetchall())
        confirmation = conn.execute('SELECT id FROM workday_operations WHERE workday_id=%s', (plan['id'],)).fetchone()['id']
    assert client.get('/workday-operations/' + str(confirmation)).json()['result'] == recap['plan']
    migrate(); migrate(); assert read(client, plan) == recap


@pytest.mark.parametrize('resource', ['outcome', 'close'])
def test_strict_payload_identity_ownership_no_store_and_delete_cascade(client, users, resource):
    _, plan = opened(client, users); start(client, plan)
    payload = outcome(plan) if resource == 'outcome' else closing()
    before = read(client, plan)
    for invalid in [{**payload, 'operation_id': 'bad'}, {**payload, 'expected_revision': True}, {**payload, 'expected_revision': '1'}, {**payload, 'expected_revision': -1}, {**payload, 'extra': 1}]:
        assert send(client, plan, resource, invalid).status_code == 422
    if resource == 'outcome':
        for invalid in [{**payload, 'activity_id': str(uuid4())}, {**payload, 'activity_id': 'gap-before-x'}, {**payload, 'outcome': 'automatic'}, {**payload, 'expected_lifecycle_revision': True}]:
            assert send(client, plan, resource, invalid).status_code == 422
    else:
        for invalid in [{**payload, 'action': 'active'}, {**payload, 'expected_outcome_revision': True}]:
            assert send(client, plan, resource, invalid).status_code == 422
    assert read(client, plan) == before
    assert client.post('/workdays/' + plan['id'] + '/' + resource, json=payload).status_code == 403
    reply = send(client, plan, resource, payload); assert reply.status_code == 200 and reply.headers['cache-control'] == 'no-store'
    lookup = '/workday-' + resource + '-operations/' + payload['operation_id']
    receipt = reply.json()
    assert client.get(lookup).json() == receipt
    assert send(client, plan, resource, {**payload, 'expected_revision': 9}).status_code == 409
    with httpx.Client(base_url=URL) as other:
        assert other.get(lookup).status_code == 401
        assert login(other, users, 1).status_code == 200
        for path in ['/workdays/' + plan['id'] + '/recap', '/workdays/' + plan['id'] + '/outcomes', lookup]:
            assert other.get(path).status_code == 404
        assert send(other, plan, resource, payload).status_code == 404
    assert send(client, plan, 'delete', {'operation_id': str(uuid4()), 'source_revision': 1}).status_code == 200
    assert client.get(lookup).status_code == send(client, plan, resource, payload).status_code == 404
    with database() as conn:
        for table in ['workday_outcome_revisions', 'workday_outcomes', 'workday_outcome_operations', 'workday_close_operations']:
            assert not conn.execute('SELECT 1 FROM ' + table + ' WHERE workday_id=%s', (plan['id'],)).fetchone()


def test_stale_outcome_review_and_competing_close_require_new_explicit_review(client, users):
    _, plan = opened(client, users); start(client, plan)
    stale = closing()
    assert send(client, plan, 'outcome', outcome(plan)).status_code == 200
    assert send(client, plan, 'close', stale).status_code == 409
    assert read(client, plan)['lifecycle']['state'] == 'active'
    assert send(client, plan, 'outcome', outcome(plan, 0, 1, 'skipped')).status_code == 409
    proof, cookies = headers(client), dict(client.cookies)
    commands = [closing(1, 'ended'), closing(1, 'aborted')]
    def post(payload): return httpx.post(URL + '/workdays/' + plan['id'] + '/close', headers=proof, cookies=cookies, json=payload, timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: replies = list(pool.map(post, commands))
    assert sorted(reply.status_code for reply in replies) == [200, 409]
    winner = next(reply.json()['result'] for reply in replies if reply.status_code == 200)
    assert read(client, plan)['lifecycle'] == winner


@pytest.mark.parametrize('resource', ['outcome', 'close'])
@pytest.mark.parametrize('boundary', ['session', 'plan'])
def test_final_atomic_admission_rolls_back_all_state_and_receipts(client, users, monkeypatch, resource, boundary):
    _, plan = opened(client, users); start(client, plan); initial = read(client, plan)
    payload = (SaveOutcome(**outcome(plan)) if resource == 'outcome' else CloseWorkday(**closing()))
    request = SimpleNamespace(cookies={auth.SESSION: client.cookies.get(auth.SESSION)})
    class Connection:
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            if query.startswith('INSERT INTO workday_' + resource + '_operations'):
                if boundary == 'plan': self.conn.execute('UPDATE workdays SET expires_at=clock_timestamp() WHERE id=%s', (plan['id'],))
                else: self.conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner=%s", (users[1][0],))
            return self.conn.execute(query, params)
    @contextmanager
    def wrapped():
        with database() as conn: yield Connection(conn)
    monkeypatch.setattr(workday_outcome_storage, 'database', wrapped)
    with pytest.raises(HTTPException) as error: workday_outcome_storage.save(request, UUID(plan['id']), payload, close=resource == 'close')
    assert error.value.status_code == (410 if boundary == 'plan' else 401)
    assert read(client, plan) == initial


@pytest.mark.parametrize('resource', ['outcome', 'close'])
def test_capacity_accepted_replay_expiry_cleanup_no_resurrection(client, users, resource):
    _, plan = opened(client, users); start(client, plan)
    payload = outcome(plan) if resource == 'outcome' else closing()
    receipt = send(client, plan, resource, payload).json(); before = read(client, plan)
    # A second active plan tests account-wide capacity even when first is terminal.
    source, _, decision = prepare(client); second = confirm(client, source, decision).json(); start(client, second)
    table = 'workday_' + resource + '_operations'
    with database() as conn:
        conn.execute('INSERT INTO ' + table + ' SELECT gen_random_uuid(),owner,workday_id,payload_hash,result,expires_at FROM ' + table + ' CROSS JOIN generate_series(1,1999) WHERE id=%s', (payload['operation_id'],))
    rejected = send(client, second, resource, outcome(second) if resource == 'outcome' else closing())
    assert rejected.status_code == 429 and rejected.json()['detail']['code'] == resource + '_receipt_capacity'
    assert send(client, plan, resource, payload).json() == receipt and read(client, plan) == before
    lookup = '/workday-' + resource + '-operations/' + payload['operation_id']
    with database() as conn: conn.execute('UPDATE workdays SET expires_at=clock_timestamp() WHERE id=%s', (plan['id'],))
    assert client.get(lookup).status_code == send(client, plan, resource, payload).status_code == 410
    cleanup()
    assert client.get(lookup).status_code == send(client, plan, resource, payload).status_code == 404
    with database() as conn:
        for name in ['workday_outcome_revisions', 'workday_outcomes', 'workday_outcome_operations', 'workday_close_operations']:
            assert not conn.execute('SELECT 1 FROM ' + name + ' WHERE workday_id=%s', (plan['id'],)).fetchone()


@pytest.mark.parametrize('resource', ['outcome', 'selection', 'physical-bus', 'delete'])
def test_parent_lock_serializes_competing_write_and_closure_without_partial_state(client, users, resource):
    _, plan = opened(client, users); start(client, plan)
    proposal = {'outcome': outcome(plan), 'selection': {'operation_id': str(uuid4()), 'expected_revision': 0, 'activity_id': plan['draft']['activities'][2]['id']},
                'physical-bus': {'operation_id': str(uuid4()), 'expected_revision': 0, 'physical_bus': '009'},
                'delete': {'operation_id': str(uuid4()), 'source_revision': 1}}[resource]
    proof, cookies = headers(client), dict(client.cookies)
    def post(item):
        name, body = item
        return httpx.post(URL + '/workdays/' + plan['id'] + '/' + name, headers=proof, cookies=cookies, json=body, timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        writes, closure = list(pool.map(post, [(resource, proposal), ('close', closing())]))
    assert writes.status_code in {200, 409} and closure.status_code in {200, 409, 404}
    if resource == 'delete':
        assert writes.status_code == 200 and client.get('/workdays/' + plan['id'] + '/recap').status_code == 404
    else:
        saved = read(client, plan)
        if resource == 'outcome' and writes.status_code == 200:
            assert closure.status_code == 409 and saved['lifecycle']['state'] == 'active' and saved['outcomes']['revision'] == 1
            assert send(client, plan, 'close', closing(1)).status_code == 200
        else:
            assert closure.status_code == 200 and saved['lifecycle']['state'] == 'ended'
            assert saved['outcomes']['revision'] == 0
        final = read(client, plan)
        assert final['lifecycle']['state'] == 'ended'
        assert send(client, plan, resource, {**proposal, 'operation_id': str(uuid4())}).status_code == 409
        assert read(client, plan) == final


def test_late_close_preserves_earlier_planned_deadline_and_unknowns(client, users):
    from zoneinfo import ZoneInfo
    assert login(client, users).status_code == 200
    content = facts()
    ending = (datetime.now(timezone.utc) - timedelta(days=1)).astimezone(ZoneInfo('Europe/Oslo')).replace(microsecond=0)
    content['service_date'] = ending.date().isoformat()
    content['activities'][0].update(start=(ending - timedelta(minutes=10)).isoformat(), end=ending.isoformat())
    source, _, decisions = prepare(client, content)
    plan = confirm(client, source, decisions).json()
    # Synthetic facts with planned final end yesterday remain retained;
    # closure today cannot turn the planned maximum into a later deadline.
    previous = read(client, plan)
    start(client, plan)
    result = send(client, plan, 'close', closing()).json()['result']
    assert result['expires_at'] == previous['plan']['expires_at']
    assert datetime.fromisoformat(result['expires_at']) < datetime.fromisoformat(result['ended_at']) + timedelta(days=7)
    assert read(client, plan)['outcomes'] == previous['outcomes']


def test_two_outcomes_same_revision_accept_exactly_one_member_change(client, users):
    _, plan = opened(client, users); start(client, plan)
    commands = [outcome(plan, member=0, value='completed'), outcome(plan, member=3, value='skipped')]
    proof, cookies = headers(client), dict(client.cookies)
    def post_command(body):
        return httpx.post(URL + '/workdays/' + plan['id'] + '/outcome', headers=proof, cookies=cookies, json=body, timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        replies = list(pool.map(post_command, commands))
    assert sorted(reply.status_code for reply in replies) == [200, 409]
    winner = next(body for body, reply in zip(commands, replies) if reply.status_code == 200)
    saved = read(client, plan)['outcomes']
    assert saved['revision'] == 1
    assert saved['outcomes'] == [{'activity_id': a['id'], 'outcome': winner['outcome'] if a['id'] == winner['activity_id'] else 'unregistered'} for a in plan['draft']['activities']]
    with database() as conn:
        assert conn.execute('SELECT count(*) AS n FROM workday_outcome_operations WHERE workday_id=%s', (plan['id'],)).fetchone()['n'] == 1


def test_populated_pre010_upgrade_preserves_every_fact_first_start_receipt_and_deadline(client, users):
    from pathlib import Path
    _, active = opened(client, users); start(client, active)
    assert send(client, active, 'physical-bus', {'operation_id': str(uuid4()), 'expected_revision': 0, 'physical_bus': '0007'}).status_code == 200
    assert send(client, active, 'selection', {'operation_id': str(uuid4()), 'expected_revision': 0, 'activity_id': active['draft']['activities'][2]['id']}).status_code == 200
    source, _, decision = prepare(client); confirmed = confirm(client, source, decision).json()
    # Isolated connection-local schema follows the populated migration pattern;
    # the running public schema and real API never change.
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        schema = 'upgrade_' + uuid4().hex
        conn.execute('CREATE SCHEMA ' + schema)
        conn.execute('SET LOCAL search_path TO ' + schema + ',public')
        conn.execute('CREATE TABLE accounts AS SELECT * FROM public.accounts WHERE id=%s', (users[1][0],))
        conn.execute('ALTER TABLE accounts ADD PRIMARY KEY(id)')
        conn.execute('CREATE TABLE workdays AS SELECT * FROM public.workdays WHERE owner=%s', (users[1][0],))
        conn.execute('ALTER TABLE workdays ADD PRIMARY KEY(id)')
        conn.execute("ALTER TABLE workdays ADD CONSTRAINT workdays_check CHECK(expires_at=final_end+interval '7 days')")
        conn.execute('CREATE TABLE workday_lifecycles AS SELECT workday_id,state,started_at,revision FROM public.workday_lifecycles WHERE workday_id=%s', (active['id'],))
        conn.execute('ALTER TABLE workday_lifecycles ADD PRIMARY KEY(workday_id)')
        conn.execute("ALTER TABLE workday_lifecycles ADD CONSTRAINT workday_lifecycles_state_check CHECK(state='active')")
        conn.execute('ALTER TABLE workday_lifecycles ADD CONSTRAINT workday_lifecycles_revision_check CHECK(revision=1)')
        receipts = ['workday_operations', 'workday_start_operations', 'workday_bus_operations', 'workday_selection_operations']
        # Populate every historical mutable receipt as well as confirmation receipts.
        for table in receipts:
            conn.execute('CREATE TABLE ' + table + ' AS SELECT * FROM public.' + table + ' WHERE owner=%s', (users[1][0],))
        conn.execute("UPDATE workday_start_operations SET result=result-'ended_at'")
        before = {table: conn.execute('SELECT * FROM ' + table + ' ORDER BY ' + ('workday_id' if table == 'workday_lifecycles' else 'id')).fetchall() for table in ['workdays', 'workday_lifecycles', *receipts]}
        assert len(before['workdays']) == 2 and len(before['workday_lifecycles']) == 1
        assert all(before[table] for table in receipts)
        sql = (Path(__file__).resolve().parent.parent / 'migrations/private/010_outcomes_and_closure.sql').read_text(encoding='utf-8')
        conn.execute(sql)
        for table, original in before.items():
            after = conn.execute('SELECT * FROM ' + table + ' ORDER BY ' + ('workday_id' if table == 'workday_lifecycles' else 'id')).fetchall()
            if table == 'workday_lifecycles':
                assert all(row['ended_at'] is None for row in after)
                after = [{key: value for key, value in row.items() if key != 'ended_at'} for row in after]
            assert after == original
        for table in ['workday_outcomes', 'workday_outcome_revisions', 'workday_outcome_operations', 'workday_close_operations']:
            assert conn.execute('SELECT count(*) AS n FROM ' + table).fetchone()['n'] == 0
        conn.execute('DROP SCHEMA ' + schema + ' CASCADE')
