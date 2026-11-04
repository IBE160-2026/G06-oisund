"""Offline restore primitives. Only the root helper controls maintenance/retry authority.

Never called by migration, startup, cleanup, or an HTTP handler. Each operation
has a 5s lock wait and 120s statement timeout; the host also bounds its process.
"""
import hashlib
import json
import re
import secrets
from pathlib import Path

from psycopg import sql

from .auth import account_lock
from .private_storage import database


def bounded(conn):
    conn.execute("SET LOCAL lock_timeout = '5s'")
    conn.execute("SET LOCAL statement_timeout = '120s'")
    conn.execute("SET LOCAL transaction_timeout = '120s'")


def inspect(conn):
    paths = sorted((Path(__file__).resolve().parent.parent / 'migrations/private').glob('*.sql'))
    names = [p.name for p in paths]
    installed = [r['name'] for r in conn.execute('SELECT name FROM private_migrations ORDER BY name')]
    if installed not in (names, names[:-1]) or names[-1] != '015_password_recovery.sql':
        raise ValueError('Unsupported restore schema')
    expected = {'private_migrations'}
    for path in paths[:len(installed)]:
        expected.update(re.findall(r'CREATE TABLE\s+(\w+)', path.read_text(), re.I))
    actual = {r['tablename'] for r in conn.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")}
    if actual != expected:
        raise ValueError('Unsupported restore tables')
    # Canonical per-row SHA256, streamed in stable order. Passwords, sessions,
    # proofs, rate history and audit are intentionally outside business equality.
    excluded = {'private_migrations', 'sessions', 'security_settings', 'login_limits',
                'recovery_proofs', 'recovery_audit'}
    result = {}
    for table in sorted(actual - excluded):
        expression = sql.SQL("to_jsonb(t) - 'password_hash'") if table == 'accounts' else sql.SQL('to_jsonb(t)')
        query = sql.SQL('SELECT ({expr})::text AS row FROM {table} t ORDER BY ({expr})::text').format(
            expr=expression, table=sql.Identifier(table))
        digest, count = hashlib.sha256(), 0
        with conn.cursor(name='restore_fingerprint') as cursor:
            cursor.execute(query)
            for row in cursor:
                data = row['row'].encode()
                digest.update(len(data).to_bytes(8, 'big'))
                digest.update(data)
                count += 1
        result[table] = {'rows': count, 'sha256': digest.hexdigest()}
    return {'schema': len(installed), 'business': result}


def snapshot():
    with database() as conn:
        bounded(conn)
        conn.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ')
        return inspect(conn)


def verify(conn):
    if conn.execute('SELECT 1 FROM sessions LIMIT 1').fetchone():
        raise ValueError('Restored sessions remain')
    if conn.execute("SELECT 1 FROM recovery_proofs WHERE state='active' LIMIT 1").fetchone():
        raise ValueError('Restored proofs remain')
    if conn.execute("SELECT 1 FROM accounts WHERE password_hash !~ '^[0-9a-f]{32}:[0-9a-f]{128}$' LIMIT 1").fetchone():
        raise ValueError('Invalid quarantine format')


def authority_fingerprint(conn):
    result = hashlib.sha256()
    for row in conn.execute('SELECT id,password_hash FROM accounts ORDER BY id'):
        result.update((str(row['id']) + ':' + row['password_hash'] + '\n').encode())
    return result.hexdigest()


def quarantine():
    with database() as conn:
        bounded(conn)
        owners = conn.execute('SELECT id FROM accounts ORDER BY id').fetchall()
        # Account gates precede row/table locks, in deterministic UUID order.
        for row in owners:
            account_lock(conn, row['id'])
        conn.execute('LOCK TABLE accounts IN EXCLUSIVE MODE')
        if conn.execute('SELECT id FROM accounts ORDER BY id').fetchall() != owners:
            raise ValueError('Restore account set changed')
        before = inspect(conn)
        for row in owners:
            # Independent salt AND digest, no plaintext password ever exists.
            replacement = secrets.token_hex(16) + ':' + secrets.token_hex(64)
            old = conn.execute('SELECT password_hash FROM accounts WHERE id=%s', (row['id'],)).fetchone()['password_hash']
            if replacement == old:
                raise ValueError('Restore replacement collision')
            stored = conn.execute('UPDATE accounts SET password_hash=%s WHERE id=%s RETURNING password_hash',
                                 (replacement, row['id'])).fetchone()['password_hash']
            if stored != replacement:
                raise ValueError('Restore replacement verification failed')
        conn.execute('DELETE FROM sessions')
        conn.execute("UPDATE recovery_proofs SET state='revoked' WHERE state='active'")
        verify(conn)
        if inspect(conn) != before:
            raise ValueError('Restore business equivalence failed')
        fingerprint = authority_fingerprint(conn)
    return {'quarantined_accounts': len(owners), 'authority_fingerprint': fingerprint, **before}


def checked():
    with database() as conn:
        bounded(conn)
        verify(conn)
        return {**inspect(conn), 'authority_fingerprint': authority_fingerprint(conn)}


def command(action):
    try:
        result = {'restore-inspect': snapshot, 'restore-quarantine': quarantine,
                  'restore-verify': checked}[action]()
    except Exception:
        raise SystemExit('Offline restore check failed') from None
    print(json.dumps(result, sort_keys=True))
