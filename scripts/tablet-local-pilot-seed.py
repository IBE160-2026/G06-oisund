"""One-time fictional pilot provisioning; no credential output.

Use only the dedicated compose.tablet.yaml project with the protected JSON file
mounted read-only. No live Access token is manufactured or bypass configured.
"""
import json
import os
from pathlib import Path

from fastapi.testclient import TestClient
from app import auth
from app.private_storage import database

assert os.environ.get('TABLET_LOCAL_PILOT') == 'ibe160-tablet-prep'
assert os.environ.get('APP_MODE') == 'private-local'
assert os.environ.get('PRIVATE_DATABASE_URL') == 'postgresql://private_work@private-db/private_work'
assert auth.configuration() == 'https://app.bussassistent.com'
credential = json.loads(Path('/run/secrets/tablet_pilot_login').read_text())
assert set(credential) == {'username', 'password'}
assert credential['username'] == 'tablet-provebruker'
assert isinstance(credential['password'], str) and len(credential['password']) >= 32
with database() as conn:
    # Refuse an existing database rather than adding accounts to unknown data.
    assert conn.execute('SELECT count(*) AS n FROM accounts').fetchone()['n'] == 0
    assert conn.execute('SELECT count(*) AS n FROM drafts').fetchone()['n'] == 0
    role = conn.execute('SELECT rolsuper,rolcreatedb,rolcreaterole,rolreplication FROM pg_roles WHERE rolname=current_user').fetchone()
    assert not any(role.values())
    migrations = conn.execute('SELECT count(*) AS n FROM private_migrations').fetchone()['n']
    assert migrations == len(list(Path('/app/migrations/private').glob('*.sql')))

auth.provision(credential['username'], credential['password'])
from app.private_main import app

with TestClient(app, base_url=auth.configuration()) as client:
    def proof():
        response = client.get('/auth/csrf')
        assert response.status_code == 200
        assert 'Secure' in response.headers['set-cookie']
        return {'Origin': auth.configuration(), 'X-CSRF-Token': response.json()['csrf_token']}

    assert client.get('/drafts').status_code == 401
    login = client.post('/auth/login', headers=proof(), json=credential)
    assert login.status_code == 200
    assert all(flag in login.headers['set-cookie'] for flag in ('Secure', 'HttpOnly', 'SameSite=strict'))
    assert client.get('/notices').status_code == 200
    operation = client.post('/draft-operations', headers=proof(), json={})
    assert operation.status_code == 200
    body = {'operation_id': operation.json()['operation_id'], 'expected_revision': 0,
            'draft': {'service_date': '2031-01-02', 'physical_bus': 'FIKTIV PILOT - ingen virkelig arbeidsdag', 'activities': []}}
    assert client.post('/drafts', json=body).status_code == 403
    saved = client.post('/drafts', headers=proof(), json=body)
    assert saved.status_code == 200
    record = saved.json()
    reopened = client.get('/drafts/' + record['id'])
    assert reopened.status_code == 200 and reopened.json() == record
    assert reopened.headers['cache-control'] == 'no-store'
    assert client.post('/auth/logout', headers=proof()).status_code == 200
    assert client.get('/drafts').status_code == 401

with database() as conn:
    assert conn.execute('SELECT count(*) AS n FROM accounts').fetchone()['n'] == 1
    assert conn.execute('SELECT count(*) AS n FROM drafts').fetchone()['n'] == 1
    assert conn.execute('SELECT count(*) AS n FROM sessions').fetchone()['n'] == 0
print(f'PASS: {migrations} pilot migrations, restricted role, one fictional user/draft; HTTPS-mode login/CSRF/readback/logout; zero sessions retained. TestClient only, no browser/TLS/Access admission pass claimed.')
