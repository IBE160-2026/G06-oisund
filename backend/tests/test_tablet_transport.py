"""Isolated transport checks. No PostgreSQL, migration, account or network needed."""
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app import auth


@pytest.fixture(autouse=True)
def transport_env(monkeypatch):
    monkeypatch.delenv('PRIVATE_LOOPBACK_DEVELOPMENT', raising=False)
    monkeypatch.setenv('PRIVATE_HTTPS_DEPLOYMENT', '1')
    monkeypatch.setenv('PRIVATE_ORIGIN', 'https://bus.owner-domain.no')


@pytest.mark.parametrize('origin', [
    'http://bus.owner-domain.no', 'https://bus.owner-domain.no/',
    'https://bus.owner-domain.no:443', 'https://user@bus.owner-domain.no',
    'https://bus.owner-domain.no?x=1', 'https://bus.owner-domain.no#fragment',
    'https://127.0.0.1', 'https://localhost', 'https://bus.local',
    'https://bus.YOUR-DOMAIN.invalid', 'https://BUS.owner-domain.no',
    'https://bus.owner-domain.no\\@evil.no',
])
def test_https_rejects_noncanonical_origins(monkeypatch, origin):
    monkeypatch.setenv('PRIVATE_ORIGIN', origin)
    with pytest.raises(RuntimeError):
        auth.configuration()


def test_modes_are_explicit_and_exclusive(monkeypatch):
    assert auth.configuration() == 'https://bus.owner-domain.no'
    assert auth.secure_cookies()
    monkeypatch.setenv('PRIVATE_LOOPBACK_DEVELOPMENT', '1')
    with pytest.raises(RuntimeError):
        auth.configuration()
    monkeypatch.delenv('PRIVATE_HTTPS_DEPLOYMENT')
    monkeypatch.setenv('PRIVATE_ORIGIN', 'http://127.0.0.1:5173')
    assert auth.configuration() == 'http://127.0.0.1:5173'
    assert not auth.secure_cookies()
    monkeypatch.delenv('PRIVATE_LOOPBACK_DEVELOPMENT')
    with pytest.raises(RuntimeError):
        auth.configuration()
    monkeypatch.setenv('PRIVATE_HTTPS_DEPLOYMENT', 'true')
    with pytest.raises(RuntimeError):
        auth.configuration()


def test_https_http_boundary_cookies_and_csrf(monkeypatch):
    # No TestClient context manager: intentionally do not run DB startup/cleanup.
    from app import private_main

    class FakeConnection:
        def execute(self, *args):
            return self

        def fetchone(self):
            return {'csrf_key': 'synthetic-test-key'}

    @contextmanager
    def fake_database():
        yield FakeConnection()

    monkeypatch.setattr(auth, 'database', fake_database)
    monkeypatch.setattr(private_main, 'database', fake_database)
    now = datetime.now(timezone.utc)
    monkeypatch.setattr(auth, 'authenticate', lambda *args: (
        'synthetic-session', {'owner': uuid4(), 'created_at': now, 'expires_at': now + timedelta(days=14)}))
    client = TestClient(private_main.app, base_url='https://bus.owner-domain.no')
    csrf = client.get('/auth/csrf')
    assert csrf.status_code == 200
    assert csrf.headers['cache-control'] == 'no-store'
    assert 'Secure' in csrf.headers['set-cookie']
    proof = csrf.json()['csrf_token']
    headers = {'Origin': auth.configuration(), 'X-CSRF-Token': proof}
    body = {'username': 'synthetic-owner', 'password': 'synthetic-password'}
    for bad in [{}, {**headers, 'Origin': 'https://evil.no'},
                {**headers, 'X-CSRF-Token': 'forged'},
                {'X-Forwarded-Proto': 'https', 'X-Forwarded-Host': 'bus.owner-domain.no'}]:
        assert client.post('/auth/login', headers=bad, json=body).status_code == 403
    login = client.post('/auth/login', headers=headers, json=body)
    assert login.status_code == 200
    cookie = login.headers['set-cookie']
    assert all(flag in cookie for flag in ['Secure', 'HttpOnly', 'SameSite=strict', 'Path=/'])
    assert 'Domain=' not in cookie
    assert login.headers['cache-control'] == 'no-store'
    logout = client.post('/auth/logout', headers=headers)
    assert logout.status_code == 200
    assert 'Secure' in logout.headers['set-cookie'] and 'Max-Age=0' in logout.headers['set-cookie']
    # Secure cookies cannot be used by a plain HTTP client, even with forged headers.
    client.base_url = 'http://bus.owner-domain.no'
    assert client.post('/auth/login', headers=headers, json=body).status_code == 403
