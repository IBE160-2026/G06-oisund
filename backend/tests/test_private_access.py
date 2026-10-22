"""Run explicitly in private-api; real HTTP/PostgreSQL, synthetic accounts only."""
import concurrent.futures
import hashlib
import hmac
import os
import pty
import secrets
import select
import sys
import subprocess
import time
from datetime import datetime
from uuid import uuid4

import httpx
import pytest

from app import auth
from app.private_storage import cleanup, database, migrate

pytestmark = pytest.mark.skipif(os.environ.get('APP_MODE') != 'private-local', reason='Separate private runtime required')
URL = os.environ.get('PRIVATE_TEST_API', 'http://127.0.0.1:8000')
ORIGIN = 'http://127.0.0.1:5173'


@pytest.fixture(autouse=True)
def synthetic_only():
    if os.environ.get('PRIVATE_TEST_PROJECT') != 'ibe160-private-tests':
        pytest.skip('Disposable project marker required')
    with database() as conn:
        auth.require_synthetic_accounts(conn)


@pytest.fixture
def users():
    password = secrets.token_urlsafe(24)
    names = ['synthetic-' + uuid4().hex for _ in range(2)]
    ids = [auth.provision(name, password) for name in names]
    with database() as conn:
        conn.execute('DELETE FROM login_limits')
    yield names, ids, password
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        conn.execute('DELETE FROM workday_deletions WHERE owner=ANY(%s)', (ids,))
        conn.execute('DELETE FROM workday_operations WHERE owner=ANY(%s)', (ids,))
        conn.execute('DELETE FROM workdays WHERE owner=ANY(%s)', (ids,))
        conn.execute('DELETE FROM drafts WHERE owner=ANY(%s)', (ids,))
        conn.execute('DELETE FROM draft_operations WHERE owner=ANY(%s)', (ids,))
        conn.execute('DELETE FROM draft_deletions WHERE owner=ANY(%s)', (ids,))
        conn.execute('DELETE FROM sessions WHERE owner=ANY(%s)', (ids,))
        conn.execute('DELETE FROM accounts WHERE id=ANY(%s)', (ids,))
        conn.execute('DELETE FROM login_limits')


@pytest.fixture
def client():
    with httpx.Client(base_url=URL, timeout=20) as client:
        yield client


def headers(client):
    return {'Origin': ORIGIN, 'X-CSRF-Token': client.get('/auth/csrf').json()['csrf_token']}


def login(client, users, index=0):
    return client.post('/auth/login', headers=headers(client), json={'username': users[0][index], 'password': users[2]})


def test_sessions_ownership_cookies_and_no_renewal(client, users):
    assert client.get('/auth/session').status_code == 401
    response = login(client, users)
    assert response.status_code == 200
    result = response.json()
    assert result['account_id'] == str(users[1][0])
    assert (datetime.fromisoformat(result['expires_at']) - datetime.fromisoformat(result['created_at'])).total_seconds() == 14 * 86400
    cookie = response.headers['set-cookie']
    assert 'HttpOnly' in cookie and 'SameSite=strict' in cookie and 'Domain=' not in cookie
    assert client.get('/auth/session').json() == result
    assert client.get('/accounts/' + str(users[1][0])).json() == {'account_id': str(users[1][0])}
    foreign = client.get('/accounts/' + str(users[1][1]))
    assert foreign.status_code == 404 and str(users[1][1]) not in foreign.text
    for path in ['/auth/session', '/accounts/' + str(users[1][0]), '/accounts/' + str(uuid4())]:
        assert client.get(path).headers['cache-control'] == 'no-store'
    with database() as conn:
        stored = conn.execute('SELECT * FROM sessions WHERE owner=%s', (users[1][0],)).fetchone()
        assert stored['token_hash'] == auth.digest(client.cookies.get(auth.SESSION))
        assert stored['token_hash'] != client.cookies.get(auth.SESSION)
        account = conn.execute('SELECT password_hash FROM accounts WHERE id=%s', (users[1][0],)).fetchone()
        assert users[2] not in account['password_hash']
    migrate()
    assert client.get('/auth/session').json() == result
    with httpx.Client(base_url=URL, timeout=20) as other:
        assert login(other, users, 1).status_code == 200
        assert other.get('/accounts/' + str(users[1][1])).status_code == 200
        assert other.get('/accounts/' + str(users[1][0])).status_code == 404


@pytest.mark.parametrize('path', ['/auth/login', '/auth/logout'])
def test_forgery_denied(client, users, path):
    assert login(client, users).status_code == 200
    proof = headers(client)
    body = {'username': users[0][0], 'password': users[2]} if path.endswith('login') else {}
    for bad in [{}, {'Origin': ORIGIN}, {'X-CSRF-Token': proof['X-CSRF-Token']},
                {**proof, 'Origin': 'http://localhost:5173'}, {**proof, 'X-CSRF-Token': 'forged'}]:
        assert client.post(path, headers=bad, json=body).status_code == 403
    assert client.get('/auth/session').status_code == 200


def test_logout_idempotent_and_expiry(client, users):
    assert login(client, users).status_code == 200
    old_token = client.cookies.get(auth.SESSION)
    proof = headers(client)
    assert client.post('/auth/logout', headers=proof).json() == {'revoked': True}
    assert client.post('/auth/logout', headers=proof).json() == {'revoked': True}
    client.cookies.set(auth.SESSION, old_token)
    assert client.get('/auth/session').status_code == 401
    client.cookies.clear()
    assert login(client, users).status_code == 200
    with database() as conn:
        conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '15 days', expires_at=statement_timestamp()-interval '1 day' WHERE owner=%s", (users[1][0],))
    assert client.get('/auth/session').status_code == 401
    assert client.get('/accounts/' + str(users[1][0])).status_code == 401
    cleanup()
    with database() as conn:
        assert conn.execute('SELECT count(*) AS n FROM sessions WHERE owner=%s', (users[1][0],)).fetchone()['n'] == 0


def test_generic_errors_and_persistent_concurrent_throttle(client, users):
    proof = headers(client)
    failures = [client.post('/auth/login', headers=proof, json={'username': name, 'password': 'incorrect-synthetic'}) for name in [users[0][0], 'absent-' + uuid4().hex]]
    assert failures[0].json() == failures[1].json() and failures[0].status_code == 401
    secret = 'do-not-echo-synthetic'
    malformed = client.post('/auth/login', headers=proof, json={'username': users[0][0], 'password': secret, 'unexpected': secret})
    assert malformed.status_code == 422 and secret not in malformed.text and users[0][0] not in malformed.text
    cookie = client.cookies.get(auth.CSRF)
    def attempt(_):
        return httpx.post(URL + '/auth/login', headers=proof, cookies={auth.CSRF: cookie}, json={'username': users[0][0], 'password': 'incorrect-synthetic'}, timeout=30).status_code
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(attempt, range(12)))
    assert results.count(401) == 9 and results.count(429) == 3
    migrate()
    assert login(client, users).status_code == 429
    with database() as conn:
        conn.execute("UPDATE login_limits SET expires_at=clock_timestamp()-interval '1 second'")
    cleanup()
    assert login(client, users).status_code == 200


def test_storage_and_public_config_fail_closed(monkeypatch):
    for url in ['postgresql://fictional:x@db/fictional_assessment',
                'postgresql://private_work:x@private-db/private_work?host=db',
                'postgresql://private_work:x@private-db/private_work#override']:
        monkeypatch.setenv('PRIVATE_DATABASE_URL', url)
        with pytest.raises(RuntimeError):
            database()
    for origin in ['https://example.com', 'http://0.0.0.0:5173', 'http://127.0.0.1:5173/', 'http://127.0.0.1:5173?x=1']:
        monkeypatch.setenv('PRIVATE_ORIGIN', origin)
        with pytest.raises(RuntimeError):
            auth.configuration()
    monkeypatch.setenv('PRIVATE_ORIGIN', ORIGIN)
    monkeypatch.delenv('PRIVATE_LOOPBACK_DEVELOPMENT')
    with pytest.raises(RuntimeError):
        auth.configuration()


def test_random_names_cannot_grow_unbounded_metadata(client, users):
    proof = headers(client)
    for _ in range(110):
        response = client.post('/auth/login', headers=proof, json={'username': 'absent-' + uuid4().hex, 'password': 'incorrect-synthetic'})
        assert response.status_code in {401, 429}
    with database() as conn:
        assert conn.execute('SELECT count(*) AS n FROM login_limits').fetchone()['n'] <= 201
        assert conn.execute("SELECT attempts FROM login_limits WHERE bucket='global'").fetchone()['attempts'] == 101


def test_cli_hidden_password_and_no_echo():
    name = 'cli-check-' + uuid4().hex
    password = secrets.token_urlsafe(24)
    pid, terminal = pty.fork()
    if pid == 0:
        os.execv(sys.executable, [sys.executable, '-m', 'app.manage', 'provision', name])
    transcript = b''
    try:
        for prompt in [b'Passord', b'Gjenta passord']:
            received = b''
            while prompt not in received:
                assert select.select([terminal], [], [], 10)[0], 'CLI prompt timeout'
                received += os.read(terminal, 4096)
            transcript += received
            os.write(terminal, (password + '\n').encode())
        while select.select([terminal], [], [], 10)[0]:
            try:
                data = os.read(terminal, 4096)
            except OSError:
                break
            if not data:
                break
            transcript += data
        _, status = os.waitpid(pid, 0)
        assert os.waitstatus_to_exitcode(status) == 0
        assert password.encode() not in transcript and b'Konto opprettet' in transcript
        with database() as conn:
            assert conn.execute('SELECT id FROM accounts WHERE username=%s', (name,)).fetchone()
    finally:
        os.close(terminal)
        with database() as conn:
            conn.execute('DELETE FROM accounts WHERE username=%s', (name,))


def test_staggered_window_metadata_expires_together(client, users):
    assert login(client, users).status_code == 200
    with database() as conn:
        conn.execute("UPDATE login_limits SET expires_at=clock_timestamp()+interval '3 minutes'")
        deadline = conn.execute("SELECT expires_at FROM login_limits WHERE bucket='global'").fetchone()['expires_at']
    assert client.post('/auth/login', headers=headers(client), json={'username': 'synthetic-absent-new-window', 'password': 'wrong'}).status_code == 401
    with database() as conn:
        assert all(row['expires_at'] == deadline for row in conn.execute('SELECT expires_at FROM login_limits').fetchall())
        conn.execute("UPDATE login_limits SET expires_at=clock_timestamp()-interval '1 second'")
    assert login(client, users).status_code == 200
    with database() as conn:
        assert conn.execute('SELECT count(*) AS n FROM login_limits').fetchone()['n'] == 3


def test_ip_limit_twenty_below_global(client, users):
    proof = headers(client)
    for attempt in range(1, 22):
        response = client.post('/auth/login', headers=proof, json={'username': 'synthetic-distinct-' + uuid4().hex, 'password': 'wrong'})
        assert response.status_code == (401 if attempt <= 20 else 429)
    with database() as conn:
        assert conn.execute("SELECT attempts FROM login_limits WHERE bucket='global'").fetchone()['attempts'] == 21


def test_invalid_csrf_encoding_signature_and_age(client, users):
    assert login(client, users).status_code == 200
    before = client.get('/auth/session').json()
    with database() as conn:
        key = conn.execute('SELECT csrf_key FROM security_settings WHERE id=1').fetchone()['csrf_key']
    bad_tokens = [str(int(time.time())) + '.synthetic.' + '0' * 64]
    for offset in [-3601, 60]:
        payload = str(int(time.time()) + offset) + '.synthetic'
        bad_tokens.append(payload + '.' + hmac.new(key.encode(), payload.encode(), hashlib.sha256).hexdigest())
    for token in bad_tokens:
        response = client.post('/auth/logout', headers={'Origin': ORIGIN, 'Cookie': f'{auth.CSRF}={token}', 'X-CSRF-Token': token})
        assert response.status_code == 403 and response.headers['cache-control'] == 'no-store'
    response = client.post('/auth/logout', headers={b'Origin': ORIGIN.encode(), b'Cookie': b'private_csrf=\xe9', b'X-CSRF-Token': b'\xe9'})
    assert response.status_code == 403 and response.headers['cache-control'] == 'no-store'
    assert client.get('/auth/session').json() == before


def test_oversized_declared_and_streamed_mutations(client, users):
    proof = headers(client)
    for content in [b'x' * 4097, iter([b'x' * 2000, b'x' * 2097])]:
        response = client.post('/auth/login', headers=proof, content=content)
        assert response.status_code == 413 and response.headers['cache-control'] == 'no-store'
    assert client.get('/auth/session').status_code == 401


def test_delayed_csrf_check_does_not_block_unrelated_requests(monkeypatch):
    import asyncio
    from app.private_main import app
    entered = __import__('threading').Event()
    release = __import__('threading').Event()
    def delayed(request):
        entered.set()
        assert release.wait(5)
    monkeypatch.setattr(auth, 'check_mutation', delayed)
    async def scenario():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=URL) as local:
            task = asyncio.create_task(local.post('/auth/logout'))
            try:
                assert await asyncio.to_thread(entered.wait, 2)
                response = await asyncio.wait_for(local.get('/health'), timeout=1)
                assert response.status_code == 200
            finally:
                release.set()
                await task
    asyncio.run(scenario())


def test_verification_guard_refuses_without_mutation():
    with database() as conn:
        owner = uuid4()
        conn.execute('INSERT INTO accounts VALUES (%s,%s,%s)', (owner, 'operator-check-' + uuid4().hex, auth.DUMMY))
        conn.execute('INSERT INTO sessions(token_hash,owner) VALUES (%s,%s)', (auth.digest(uuid4().hex), owner))
        conn.execute("INSERT INTO login_limits VALUES (%s,7,clock_timestamp()+interval '5 minutes')", ('synthetic-guard-' + uuid4().hex,))
        before_accounts = conn.execute('SELECT * FROM accounts ORDER BY id').fetchall()
        before_limits = conn.execute('SELECT * FROM login_limits ORDER BY bucket').fetchall()
        before_sessions = conn.execute('SELECT * FROM sessions ORDER BY token_hash').fetchall()
        with pytest.raises(RuntimeError):
            auth.require_synthetic_accounts(conn)
        assert conn.execute('SELECT * FROM accounts ORDER BY id').fetchall() == before_accounts
        assert conn.execute('SELECT * FROM login_limits ORDER BY bucket').fetchall() == before_limits
        assert conn.execute('SELECT * FROM sessions ORDER BY token_hash').fetchall() == before_sessions
        conn.rollback()
    result = subprocess.run([sys.executable, '-m', 'app.manage', 'provision', ' SYNTHETIC-reserved '], capture_output=True, text=True)
    assert result.returncode != 0 and 'reservert' in result.stderr
