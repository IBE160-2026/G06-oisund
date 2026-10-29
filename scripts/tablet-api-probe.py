"""Real API/DB smoke; run ONLY through verify-tablet-api.ps1's disposable network.

HTTPS TestClient exercises Secure cookies; this is not a real TLS/browser test.
"""
import os
import secrets
from uuid import uuid4
from unittest.mock import patch

from fastapi.testclient import TestClient
from app import auth
from app.private_storage import database, migrate

assert os.environ.get('TABLET_DISPOSABLE_PROBE') == '1'
assert os.environ.get('PRIVATE_DATABASE_URL') == 'postgresql://private_work@private-db/private_work'
migrate()
with database() as conn:
    assert conn.execute('SELECT count(*) AS n FROM accounts').fetchone()['n'] == 0
    role = conn.execute('SELECT rolsuper,rolcreatedb,rolcreaterole,rolreplication FROM pg_roles WHERE rolname=current_user').fetchone()
    assert not any(role.values())
    migration_count = conn.execute('SELECT count(*) AS n FROM private_migrations').fetchone()['n']

origin = auth.configuration()
password = secrets.token_urlsafe(32)
owner = 'synthetic-tablet-' + uuid4().hex
other = 'synthetic-tablet-' + uuid4().hex
auth.provision(owner, password)
auth.provision(other, password)
from app.private_main import app

def headers(client):
    response = client.get('/auth/csrf')
    assert response.status_code == 200
    assert 'Secure' in response.headers['set-cookie']
    return {'Origin': origin, 'X-CSRF-Token': response.json()['csrf_token']}

def login(client, username):
    response = client.post('/auth/login', headers=headers(client), json={'username': username, 'password': password})
    assert response.status_code == 200
    assert all(flag in response.headers['set-cookie'] for flag in ('Secure', 'HttpOnly', 'SameSite=strict'))

with TestClient(app, base_url=origin) as client:
    assert client.get('/drafts').status_code == 401
    login(client, owner)
    assert client.get('/notices').status_code == 200  # Accepted 11.5 account route/migration.
    operation = client.post('/draft-operations', headers=headers(client), json={})
    assert operation.status_code == 200
    operation_id = operation.json()['operation_id']
    body = {'operation_id': operation_id, 'expected_revision': 0,
            'draft': {'service_date': '2031-01-02', 'physical_bus': 'Fiktiv nettbrettprove', 'activities': []}}
    assert client.post('/drafts', json=body).status_code == 403
    wrong_origin = {**headers(client), 'Origin': 'https://unapproved.invalid'}
    assert client.post('/drafts', headers=wrong_origin, json=body).status_code == 403
    for malformed in [
        {**headers(client), 'X-CSRF-Token': 'incorrect-proof'},
        {**headers(client), 'Origin': origin + '.unapproved.invalid'},
        {**headers(client), 'Origin': 'null'},
    ]:
        refused = client.post('/drafts', headers=malformed, json=body)
        assert refused.status_code == 403
        assert refused.headers['cache-control'] == 'no-store'
    assert len(client.get('/drafts').json()['drafts']) == 0
    with TestClient(app, base_url=origin) as no_cookies:
        missing_cookie = no_cookies.post('/drafts', headers=headers(client), json=body)
        assert missing_cookie.status_code == 403
        assert missing_cookie.headers['cache-control'] == 'no-store'
    # Session expires after the request's Origin/CSRF check, before storage
    # authorization: a formerly admitted mutation still must not write.
    original_check = auth.check_mutation
    def expire_after_transport_check(request):
        original_check(request)
        with database() as conn:
            changed = conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '15 days', expires_at=statement_timestamp()-interval '1 day' WHERE token_hash=%s RETURNING token_hash", (auth.digest(request.cookies[auth.SESSION]),)).fetchone()
            assert changed is not None
    transport_headers = headers(client)
    with patch('app.auth.check_mutation', expire_after_transport_check):
        expired_write = client.post('/drafts', headers=transport_headers, json=body)
    assert expired_write.status_code == 401, f'expiry boundary returned HTTP {expired_write.status_code}'
    assert expired_write.headers['cache-control'] == 'no-store'
    login(client, owner)
    assert len(client.get('/drafts').json()['drafts']) == 0
    assert client.get('/draft-operations/' + operation_id).json()['state'] == 'pending'
    saved = client.post('/drafts', headers=headers(client), json=body)
    assert saved.status_code == 200
    record = saved.json()
    # Simulate ignored acknowledgement: authoritative lookup then exact same operation.
    assert client.get('/draft-operations/' + operation_id).status_code == 200
    replay = client.post('/drafts', headers=headers(client), json=body)
    assert replay.status_code == 200 and replay.json() == record
    assert len(client.get('/drafts').json()['drafts']) == 1
    with TestClient(app, base_url=origin) as stranger:
        login(stranger, other)
        assert stranger.get('/drafts/' + record['id']).status_code in (403, 404)
    migrate()  # Repeated migrations must preserve the stored revision.
    reopened = client.get('/drafts/' + record['id'])
    assert reopened.status_code == 200 and reopened.json() == record
    assert reopened.headers['cache-control'] == 'no-store'
    assert client.post('/auth/logout', headers=headers(client)).status_code == 200
    assert client.get('/drafts').status_code == 401
print(f'PASS: {migration_count} real migrations/repeated migration; restricted DB role; HTTPS-mode login/CSRF/ownership; one-effect replay/reopen/logout. No real TLS or browser used.')
