"""PM-E1-S1: real HTTP and independent PostgreSQL transactions; synthetic only."""
from concurrent.futures import ThreadPoolExecutor
from threading import Event, local
from time import monotonic, sleep
from types import SimpleNamespace

import httpx
import pytest
from fastapi import HTTPException

from app import auth
from app.private_storage import database, cleanup
from test_private_access import users, client, synthetic_only, headers, login, URL, pytestmark

NEW = 'synthetic-new-password-12345'


@pytest.fixture
def gates(monkeypatch):
    """Observe real DB waiters on identified connections, not thread scheduling."""
    original = auth.account_lock
    identity, connections = local(), {}
    def lock(conn, owner):
        if getattr(identity, 'name', None):
            connections[identity.name] = conn.info.backend_pid if hasattr(conn, 'info') else conn.conn.info.backend_pid
        original(conn, owner)
    monkeypatch.setattr(auth, 'account_lock', lock)
    class Probe:
        def run(self, name, function, *args):
            identity.name = name
            return function(*args)
        def blocked(self, name, blocker=None):
            deadline = monotonic() + 5
            with database() as conn:
                conn.autocommit = True
                while monotonic() < deadline:
                    pid = connections.get(name)
                    if pid:
                        row = conn.execute("SELECT wait_event,pg_blocking_pids(pid) AS blockers FROM pg_stat_activity WHERE pid=%s", (pid,)).fetchone()
                        expected = connections.get(blocker) if isinstance(blocker, str) else blocker
                        if row and row['wait_event'] == 'advisory' and row['blockers'] and (expected is None or expected in row['blockers']):
                            return
                    sleep(.01)
            raise AssertionError('Expected PostgreSQL account-gate contention was not observed')
    return Probe()


def change(client, users, **overrides):
    body = dict(current_password=users[2], new_password=NEW, confirmation=NEW)
    body.update(overrides)
    return client.post('/auth/password/change', headers=headers(client), json=body)


def request_for(token):
    return SimpleNamespace(cookies={auth.SESSION: token}, client=SimpleNamespace(host='synthetic-local'))


def test_change_revokes_all_sessions_keeps_identity_and_data(client, users):
    assert login(client, users).status_code == 200
    from test_private_drafts import save
    saved, body = save(client)
    assert saved.status_code == 200
    record = saved.json()
    from test_private_workdays import prepare, confirm
    draft, _, decisions = prepare(client)
    plan = confirm(client, draft, decisions).json()
    from test_account_notices import send, command, content
    notice_body = command(content=content())
    notice = send(client, notice_body).json()
    with httpx.Client(base_url=URL) as second, httpx.Client(base_url=URL) as other:
        assert login(second, users).status_code == 200
        assert login(other, users, 1).status_code == 200
        with database() as conn:
            before = conn.execute('SELECT * FROM accounts ORDER BY id').fetchall()
        result = change(client, users)
        assert result.status_code == 200 and result.json() == {'changed': True}
        assert result.headers['cache-control'] == 'no-store'
        assert client.get('/auth/session').status_code == 401
        for path in ['/auth/session', '/drafts', '/workdays', '/notices']:
            assert second.get(path).status_code == 401
        assert other.get('/auth/session').status_code == 200
        assert login(client, users).status_code == 401
        response = client.post('/auth/login', headers=headers(client), json={'username': users[0][0], 'password': NEW})
        assert response.json()['account_id'] == str(users[1][0])
        assert client.get('/drafts/' + record['id']).json() == record
        assert client.get('/draft-operations/' + body['operation_id']).status_code == 200
        assert client.get('/workdays/' + plan['id']).json() == plan
        assert client.get('/workday-operations/' + decisions['operation_id']).json()['result'] == plan
        assert client.get('/notices/' + notice['result']['id']).json() == notice['result']
        assert client.get('/workday-notice-operations/' + notice_body['operation_id']).json() == notice
        with database() as conn:
            after = conn.execute('SELECT * FROM accounts ORDER BY id').fetchall()
        for old, new in zip(before, after):
            assert old['id'] == new['id'] and old['username'] == new['username']
            if old['id'] == users[1][0]:
                assert old['password_hash'] != new['password_hash'] and NEW not in new['password_hash']
            else:
                assert old == new


def test_validation_boundaries_do_not_mutate(client, users):
    assert login(client, users).status_code == 200
    before = client.get('/auth/session').json()
    wrong = change(client, users, current_password='synthetic-wrong')
    assert wrong.status_code == 400 and wrong.json()['detail']['code'] == 'current_password'
    for body in [dict(new_password='short'), dict(confirmation='synthetic-mismatch'), dict(account_id=str(users[1][1]))]:
        response = change(client, users, **body)
        assert response.status_code == 422 and NEW not in response.text
    for proof in [{}, {'Origin': 'https://foreign.invalid'}, {'Origin': __import__('os').environ['PRIVATE_TEST_ORIGIN'], 'X-CSRF-Token': 'forged'}]:
        assert client.post('/auth/password/change', headers=proof, json={}).status_code == 403
    assert client.post('/auth/password/change', headers=headers(client), content=b'x' * 4097).status_code == 413
    assert client.get('/auth/session').json() == before
    with httpx.Client(base_url=URL) as anonymous:
        assert change(anonymous, users).status_code == 401
    with database() as conn:
        conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '15 days', expires_at=statement_timestamp()-interval '1 day' WHERE owner=%s", (users[1][0],))
    assert change(client, users).status_code == 401


def test_persistent_parallel_change_budget_separate_from_login(client, users):
    assert login(client, users).status_code == 200
    token = client.cookies.get(auth.SESSION)
    def attempt(_):
        try:
            auth.change_password(request_for(token), 'incorrect', NEW, NEW)
        except HTTPException as error:
            return error.status_code
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(attempt, range(12)))
    assert results.count(400) == 5 and results.count(429) == 7
    with database() as conn:
        before = conn.execute("SELECT bucket,expires_at FROM login_limits WHERE bucket LIKE 'change:%%' ORDER BY bucket").fetchall()
    assert login(client, users).status_code == 200
    with database() as conn:
        assert conn.execute("SELECT bucket,expires_at FROM login_limits WHERE bucket LIKE 'change:%%' ORDER BY bucket").fetchall() == before
        assert conn.execute("SELECT attempts FROM login_limits WHERE bucket LIKE 'change:user:%%'").fetchone()['attempts'] == 12


def test_login_verification_holds_gate_until_session_commit(monkeypatch, users, gates):
    entered, release = Event(), Event()
    original = auth.password_hash
    def barrier(password, salt=None):
        if password == users[2] and salt is not None and not entered.is_set():
            entered.set()
            assert release.wait(10)
        return original(password, salt)
    token, _ = auth.authenticate(users[0][0], users[2], 'synthetic-local')
    monkeypatch.setattr(auth, 'password_hash', barrier)
    def replacement():
        auth.change_password(request_for(token), users[2], NEW, NEW)
    with ThreadPoolExecutor(max_workers=2) as pool:
        logging_in = pool.submit(gates.run, 'login', auth.authenticate, users[0][0], users[2], 'synthetic-local')
        assert entered.wait(5)
        resetting = pool.submit(gates.run, 'change', replacement)
        gates.blocked('change', 'login')
        release.set()
        late_token, _ = logging_in.result(timeout=15)
        resetting.result(timeout=15)
    with database() as conn:
        with pytest.raises(HTTPException) as error:
            auth.session(conn, request_for(late_token))
        assert error.value.status_code == 401


def test_replacement_wins_before_waiting_old_password_login(monkeypatch, users, gates):
    token, _ = auth.authenticate(users[0][0], users[2], 'synthetic-local')
    entered, release = Event(), Event()
    original = auth.password_hash
    def hashing(password, salt=None):
        if salt is None:
            entered.set()
            assert release.wait(10)
        return original(password, salt)
    monkeypatch.setattr(auth, 'password_hash', hashing)
    def old_login():
        try:
            auth.authenticate(users[0][0], users[2], 'synthetic-local')
            return 200
        except HTTPException as error:
            return error.status_code
    with ThreadPoolExecutor(max_workers=2) as pool:
        replacing = pool.submit(gates.run, 'replacement', auth.change_password, request_for(token), users[2], NEW, NEW)
        assert entered.wait(5)
        waiting = pool.submit(gates.run, 'login', old_login)
        gates.blocked('login', 'replacement')
        release.set()
        replacing.result(timeout=15)
        assert waiting.result(timeout=15) == 401
    with database() as conn:
        assert conn.execute('SELECT count(*) AS n FROM sessions WHERE owner=%s', (users[1][0],)).fetchone()['n'] == 0


def test_change_budget_persists_in_independent_process(users):
    import json
    import subprocess
    import sys
    token, _ = auth.authenticate(users[0][0], users[2], 'synthetic-local')
    for _ in range(5):
        with pytest.raises(HTTPException) as error:
            auth.change_password(request_for(token), 'incorrect', NEW, NEW)
        assert error.value.status_code == 400
    # Secrets travel only through stdin, never command arguments/environment/output.
    program = '''
import json, sys
from types import SimpleNamespace
from fastapi import HTTPException
from app import auth
from app.private_storage import database
with database() as conn:
    auth.require_synthetic_accounts(conn)
data = json.load(sys.stdin)
request = SimpleNamespace(cookies={auth.SESSION: data['token']}, client=SimpleNamespace(host='synthetic-local'))
try:
    auth.change_password(request, data['password'], data['replacement'], data['replacement'])
    change_status = 200
except HTTPException as error:
    change_status = error.status_code
try:
    auth.authenticate(data['username'], data['password'], 'synthetic-local')
    login_status = 200
except HTTPException as error:
    login_status = error.status_code
print(json.dumps({'change': change_status, 'login': login_status}))
'''
    result = subprocess.run([sys.executable, '-c', program], input=json.dumps(dict(token=token, username=users[0][0], password=users[2], replacement=NEW)), capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, 'Independent worker failed; output withheld'
    assert result.stdout.strip() == '{"change": 429, "login": 200}', 'Unexpected worker statuses; output withheld'
    assert not result.stderr, 'Unexpected worker diagnostics; output withheld'


@pytest.mark.parametrize('action', ['session', 'logout', 'import'])
def test_revocation_before_waiting_authorization_and_cleanup(users, action, gates):
    token, _ = auth.authenticate(users[0][0], users[2], 'synthetic-local')
    def private_write():
        if action == 'import':
            from app.private_import import authorize
            try:
                authorize(request_for(token))
            except HTTPException as error:
                return error.status_code
            raise AssertionError('Revoked import authority accepted')
        with database() as conn:
            if action == 'logout':
                auth.revoke_browser(conn, request_for(token))
                return 200
            try:
                auth.session(conn, request_for(token))
            except HTTPException as error:
                return error.status_code
            raise AssertionError('Revoked authority reached private mutation')
    with ThreadPoolExecutor(max_workers=2) as pool:
        with database() as conn:
            auth.account_lock(conn, users[1][0])
            waiting = pool.submit(gates.run, 'private', private_write)
            gates.blocked('private', conn.info.backend_pid)
            cleaning = pool.submit(gates.run, 'cleanup', cleanup)
            gates.blocked('cleanup', conn.info.backend_pid)
            conn.execute('DELETE FROM sessions WHERE owner=%s', (users[1][0],))
        assert waiting.result(timeout=15) == (200 if action == 'logout' else 401)
        cleaning.result(timeout=15)


def test_two_password_changes_only_one_wins(users, monkeypatch, gates):
    token, _ = auth.authenticate(users[0][0], users[2], 'synthetic-local')
    entered, release = Event(), Event()
    original = auth.password_hash
    def hash_barrier(password, salt=None):
        if salt is None:
            entered.set()
            assert release.wait(10)
        return original(password, salt)
    monkeypatch.setattr(auth, 'password_hash', hash_barrier)
    def attempt(_):
        try:
            auth.change_password(request_for(token), users[2], NEW, NEW)
            return 200
        except HTTPException as error:
            return error.status_code
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(gates.run, 'first', attempt, 0)
        assert entered.wait(5)
        second = pool.submit(gates.run, 'second', attempt, 1)
        gates.blocked('second', 'first')
        release.set()
        assert sorted([first.result(timeout=15), second.result(timeout=15)]) == [200, 401]

@pytest.mark.parametrize('dimension,maximum', [('proxy', 20), ('global', 100)])
def test_change_cpu_and_storage_caps(users, dimension, maximum):
    from uuid import uuid4
    for index in range(maximum):
        auth.change_admission(uuid4(), 'shared-proxy' if dimension == 'proxy' else str(index))
    with pytest.raises(HTTPException) as error:
        auth.change_admission(uuid4(), 'shared-proxy' if dimension == 'proxy' else 'new-proxy')
    assert error.value.status_code == 429 and error.value.headers['Retry-After'] == '900'
    with database() as conn:
        assert conn.execute("SELECT count(*) AS n FROM login_limits WHERE bucket LIKE 'change:%%'").fetchone()['n'] <= 201


@pytest.mark.parametrize('winner', ['save', 'change'])
def test_actual_draft_save_serializes_with_change(client, users, monkeypatch, winner, gates):
    from contextlib import contextmanager
    from app import draft_storage
    from app.draft_domain import SaveDraft
    from test_private_drafts import issue, content
    assert login(client, users).status_code == 200
    token = client.cookies.get(auth.SESSION)
    body = SaveDraft.model_validate(dict(operation_id=issue(client), expected_revision=0, draft=content()))
    entered, release = Event(), Event()
    original_hash = auth.password_hash
    class Connection:
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            if winner == 'save' and query.startswith('INSERT INTO drafts'):
                entered.set()
                assert release.wait(10)
            return self.conn.execute(query, params)
    @contextmanager
    def wrapped():
        with database() as conn: yield Connection(conn)
    monkeypatch.setattr(draft_storage, 'database', wrapped)
    def hashing(password, salt=None):
        if winner == 'change' and password == NEW and salt is None:
            entered.set()
            assert release.wait(10)
        return original_hash(password, salt)
    monkeypatch.setattr(auth, 'password_hash', hashing)
    def saving():
        try:
            return draft_storage.save(request_for(token), None, body)
        except HTTPException as error:
            return error.status_code
    def changing():
        return auth.change_password(request_for(token), users[2], NEW, NEW)
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(gates.run, 'first', saving if winner == 'save' else changing)
        assert entered.wait(5)
        second = pool.submit(gates.run, 'second', changing if winner == 'save' else saving)
        gates.blocked('second', 'first')
        release.set()
        left, right = first.result(timeout=15), second.result(timeout=15)
    with database() as conn:
        rows = conn.execute('SELECT * FROM drafts WHERE owner=%s', (users[1][0],)).fetchall()
        receipt = conn.execute('SELECT * FROM draft_operations WHERE id=%s', (body.operation_id,)).fetchone()
        assert len(rows) == (1 if winner == 'save' else 0)
        if winner == 'save':
            assert receipt['result'] == left
        else:
            assert right == 401 and receipt['result'] is None


def test_failure_after_hash_update_rolls_back_hash_and_partial_revocation(users, monkeypatch):
    from contextlib import contextmanager
    import psycopg
    tokens = [auth.authenticate(users[0][0], users[2], 'synthetic-local')[0] for _ in range(2)]
    with database() as conn:
        before = conn.execute('SELECT * FROM accounts WHERE id=%s', (users[1][0],)).fetchone()
        sessions = conn.execute('SELECT * FROM sessions WHERE owner=%s ORDER BY token_hash', (users[1][0],)).fetchall()
    injected = []
    class Connection:
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            if query == 'DELETE FROM sessions WHERE owner=%s':
                assert self.conn.execute('SELECT password_hash FROM accounts WHERE id=%s', params).fetchone()['password_hash'] != before['password_hash']
                self.conn.execute('DELETE FROM sessions WHERE token_hash=%s', (auth.digest(tokens[0]),))
                injected.append(True)
                # A real database error after a partial deletion aborts the transaction.
                return self.conn.execute('SELECT 1/0')
            return self.conn.execute(query, params)
    @contextmanager
    def failing_database():
        with database() as conn: yield Connection(conn)
    monkeypatch.setattr(auth, 'database', failing_database)
    with pytest.raises(psycopg.errors.DivisionByZero):
        auth.change_password(request_for(tokens[0]), users[2], NEW, NEW)
    assert injected == [True]
    with database() as conn:
        assert conn.execute('SELECT * FROM accounts WHERE id=%s', (users[1][0],)).fetchone() == before
        assert conn.execute('SELECT * FROM sessions WHERE owner=%s ORDER BY token_hash', (users[1][0],)).fetchall() == sessions


def test_session_expiry_during_hashing_rejects_and_preserves_other_sessions(users, monkeypatch):
    token, _ = auth.authenticate(users[0][0], users[2], 'synthetic-local')
    other, _ = auth.authenticate(users[0][0], users[2], 'synthetic-local')
    with database() as conn:
        conn.execute("UPDATE sessions SET expires_at=statement_timestamp()+interval '2 seconds', created_at=statement_timestamp()+interval '2 seconds'-interval '14 days' WHERE token_hash=%s", (auth.digest(token),))
        before = conn.execute('SELECT password_hash FROM accounts WHERE id=%s', (users[1][0],)).fetchone()
        sessions = conn.execute('SELECT * FROM sessions WHERE owner=%s ORDER BY token_hash', (users[1][0],)).fetchall()
    original = auth.password_hash
    entered = []
    def delayed(password, salt=None):
        result = original(password, salt)
        if salt is None:
            with database() as conn:
                conn.autocommit = True
                assert conn.execute('SELECT expires_at>clock_timestamp() AS live FROM sessions WHERE token_hash=%s', (auth.digest(token),)).fetchone()['live']
                deadline = monotonic() + 5
                while conn.execute('SELECT expires_at>clock_timestamp() AS live FROM sessions WHERE token_hash=%s', (auth.digest(token),)).fetchone()['live']:
                    assert monotonic() < deadline
                    sleep(.01)
            entered.append(True)
        return result
    monkeypatch.setattr(auth, 'password_hash', delayed)
    with pytest.raises(HTTPException) as error:
        auth.change_password(request_for(token), users[2], NEW, NEW)
    assert entered == [True] and error.value.status_code == 401
    with database() as conn:
        assert conn.execute('SELECT password_hash FROM accounts WHERE id=%s', (users[1][0],)).fetchone() == before
        assert conn.execute('SELECT * FROM sessions WHERE owner=%s ORDER BY token_hash', (users[1][0],)).fetchall() == sessions
        assert auth.session(conn, request_for(other))['owner'] == users[1][0]


def test_change_window_rollover_is_independent_of_login(users):
    for _ in range(5): auth.change_admission(users[1][0], 'synthetic-local')
    with pytest.raises(HTTPException) as error: auth.change_admission(users[1][0], 'synthetic-local')
    assert error.value.status_code == 429
    auth.authenticate(users[0][0], users[2], 'synthetic-local')
    with database() as conn:
        login_before = conn.execute("SELECT * FROM login_limits WHERE bucket NOT LIKE 'change:%%' ORDER BY bucket").fetchall()
        conn.execute("UPDATE login_limits SET expires_at=clock_timestamp()-interval '1 second' WHERE bucket LIKE 'change:%%'")
    auth.change_admission(users[1][0], 'synthetic-local')
    with database() as conn:
        rows = conn.execute("SELECT *,expires_at>clock_timestamp() AS live FROM login_limits WHERE bucket LIKE 'change:%%'").fetchall()
        assert len(rows) == 3 and all(r['attempts'] == 1 and r['live'] for r in rows)
        assert conn.execute("SELECT * FROM login_limits WHERE bucket NOT LIKE 'change:%%' ORDER BY bucket").fetchall() == login_before


@pytest.mark.parametrize('password', ['😀' * 12, '😀' * 256, ' ' * 12, '  spaced-password  '])
def test_unicode_and_whitespace_password_policy_exact_round_trip(client, users, password):
    assert login(client, users).status_code == 200
    assert change(client, users, new_password=password, confirmation=password).status_code == 200
    response = client.post('/auth/login', headers=headers(client), json={'username': users[0][0], 'password': password})
    assert response.status_code == 200
    assert change(client, users, current_password=password).status_code == 200


@pytest.mark.parametrize('password', ['😀' * 11, '😀' * 257])
def test_codepoint_length_outside_boundaries_is_rejected(client, users, password):
    assert login(client, users).status_code == 200
    assert change(client, users, new_password=password, confirmation=password).status_code == 422
    assert client.get('/auth/session').status_code == 200
