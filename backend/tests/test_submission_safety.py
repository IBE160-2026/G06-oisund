"""Actual disposable PostgreSQL checks for submission initializer/reset guards."""
import hashlib
import json
import os
import subprocess
import sys
from uuid import uuid4

import pytest
from psycopg import sql

from app import auth
from app.private_storage import database

pytestmark = pytest.mark.skipif(
    os.environ.get('SUBMISSION_PROJECT') != 'ibe160-submission',
    reason='Dedicated submission runtime required',
)


def fingerprint():
    """Compare every row without emitting credentials, sessions or application data."""
    result = {}
    with database() as conn:
        tables = conn.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename").fetchall()
        for entry in tables:
            rows = conn.execute(sql.SQL('SELECT row_to_json(t) AS row FROM {} t').format(sql.Identifier(entry['tablename']))).fetchall()
            encoded = sorted(json.dumps(row['row'], sort_keys=True) for row in rows)
            result[entry['tablename']] = hashlib.sha256(json.dumps(encoded).encode()).hexdigest()
    return result


@pytest.fixture(autouse=True)
def synthetic_only():
    if os.environ.get('PRIVATE_TEST_PROJECT') != 'ibe160-private-tests':
        pytest.fail('Disposable test marker required')
    with database() as conn:
        auth.require_synthetic_accounts(conn)


def manage(action, **environment):
    return subprocess.run(
        [sys.executable, '/submission/manage.py', action],
        env={**os.environ, **environment}, capture_output=True, text=True, timeout=30,
    )


def test_submission_initialize_preserves_every_row_and_deadline():
    before = fingerprint()
    for _ in range(2):
        result = manage('init')
        assert result.returncode == 0, result.stderr
        assert fingerprint() == before


@pytest.mark.parametrize('environment', [
    {'SUBMISSION_PROJECT': 'ibe160-private-work'},
    {'PRIVATE_DATABASE_URL': 'postgresql://private_work@localhost/private_work'},
    {'PRIVATE_DATABASE_PASSWORD_FILE': '/run/secrets/operational_password'},
    {'PRIVATE_ORIGIN': 'http://127.0.0.1:5173'},
])
def test_submission_wrong_target_refuses_before_mutation(environment):
    before = fingerprint()
    result = manage('reset', **environment)
    assert result.returncode != 0
    assert 'Submission target configuration required' in result.stderr
    assert fingerprint() == before


def test_submission_reset_refuses_ordinary_account_preserving_all_rows():
    owner, bucket = uuid4(), 'submission-guard-' + uuid4().hex
    with database() as conn:
        conn.execute('INSERT INTO accounts VALUES (%s,%s,%s)', (owner, 'operator-guard-' + uuid4().hex, auth.DUMMY))
        conn.execute('INSERT INTO sessions(token_hash,owner) VALUES (%s,%s)', (auth.digest(uuid4().hex), owner))
        conn.execute("INSERT INTO login_limits VALUES (%s,7,clock_timestamp()+interval '5 minutes')", (bucket,))
    try:
        before = fingerprint()
        result = manage('reset')
        assert result.returncode != 0
        assert 'synthetic-only' in result.stderr
        assert fingerprint() == before
    finally:
        with database() as conn:
            conn.execute('DELETE FROM sessions WHERE owner=%s', (owner,))
            conn.execute('DELETE FROM accounts WHERE id=%s', (owner,))
            conn.execute('DELETE FROM login_limits WHERE bucket=%s', (bucket,))
