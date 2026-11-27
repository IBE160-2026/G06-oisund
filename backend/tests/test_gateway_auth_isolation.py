"""Opt-in exercise of the real Nginx and Access verifier with a synthetic key."""

import os
from pathlib import Path

import httpx
import pytest

from app import auth, password_recovery
from app.private_storage import database
from test_private_access import headers, pytestmark, synthetic_only, users


def test_rejected_source_cannot_spend_other_sources_login_or_recovery(users):
    gateway = os.getenv('PRIVATE_TEST_GATEWAY')
    if gateway != 'http://gateway:8080/private-api':
        pytest.skip('Requires the isolated synthetic Nginx and Access stack')
    source_a, source_b = '192.0.2.41', '192.0.2.42'
    token = Path('/synthetic/access-token').read_text()
    common = {'Host': 'daybreak-test.invalid', 'Cf-Access-Jwt-Assertion': token}
    name = users[0][1]
    code, proof = password_recovery.issue(password_recovery.resolve(name))
    replacement = 'synthetic replacement password for gateway check'
    credentials = {'username': name, 'password': replacement}
    recovery = {'username': name, 'code': code, 'new_password': replacement, 'confirmation': replacement}
    with database() as conn:
        conn.execute(
            "INSERT INTO login_limits VALUES ('global',99,clock_timestamp()+interval '15 minutes'), "
            "('recover:global',99,clock_timestamp()+interval '15 minutes'), "
            "(%s,20,clock_timestamp()+interval '15 minutes'), (%s,20,clock_timestamp()+interval '15 minutes')",
            ('ip:' + auth.digest(source_a), 'recover:ip:' + auth.digest(source_a)),
        )
    with (
        httpx.Client(base_url=gateway, headers=common | {'Cf-Connecting-IP': source_a, 'X-Verified-Client': source_b}) as a,
        httpx.Client(base_url=gateway, headers=common | {'Cf-Connecting-IP': source_b}) as b,
        httpx.Client(base_url=gateway, headers=common | {'X-Verified-Client': source_b}) as unverified,
    ):
        assert unverified.post('/auth/login', headers=headers(unverified), json=credentials).status_code == 403
        assert a.post('/auth/login', headers=headers(a), json=credentials).status_code == 429
        assert a.post('/auth/password/recover', headers=headers(a), json=recovery).status_code == 429
        with database() as conn:
            counters = conn.execute("SELECT attempts FROM login_limits WHERE bucket IN ('global','recover:global')").fetchall()
            assert [row['attempts'] for row in counters] == [99, 99]
        assert b.post('/auth/password/recover', headers=headers(b), json=recovery).status_code == 200
        assert b.post('/auth/login', headers=headers(b), json=credentials).json().get('account_id') == str(users[1][1])
        with database() as conn:
            assert conn.execute('SELECT state FROM recovery_proofs WHERE id=%s', (proof['id'],)).fetchone()['state'] == 'consumed'
