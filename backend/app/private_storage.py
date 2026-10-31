"""Private storage cannot connect to the fictional cluster or accept URL overrides."""
import os
import secrets
from pathlib import Path
from urllib.parse import urlparse

import psycopg
from psycopg.rows import dict_row


def database():
    url = os.environ.get('PRIVATE_DATABASE_URL', '')
    parsed = urlparse(url)
    if (os.environ.get('APP_MODE') != 'private-local'
            or os.environ.get('DATABASE_URL')
            or parsed.scheme not in {'postgresql', 'postgres'} or parsed.query or parsed.fragment
            or parsed.path != '/private_work' or parsed.username != 'private_work' or parsed.password
            or parsed.hostname not in {'private-db', 'localhost', '127.0.0.1'}):
        raise RuntimeError('Only isolated private storage is allowed')
    password_file = os.environ.get('PRIVATE_DATABASE_PASSWORD_FILE', '')
    if not password_file:
        raise RuntimeError('Private database secret file required')
    return psycopg.connect(url, password=Path(password_file).read_text().strip(), row_factory=dict_row, connect_timeout=3)


def migrate():
    with database() as conn:
        conn.execute('SELECT pg_advisory_xact_lock(903001)')
        conn.execute('CREATE TABLE IF NOT EXISTS private_migrations (name text PRIMARY KEY)')
        for path in sorted((Path(__file__).resolve().parent.parent / 'migrations/private').glob('*.sql')):
            if not conn.execute('SELECT 1 FROM private_migrations WHERE name=%s', (path.name,)).fetchone():
                conn.execute(path.read_text(encoding='utf-8'))
                conn.execute('INSERT INTO private_migrations VALUES (%s)', (path.name,))
        conn.execute('INSERT INTO security_settings VALUES (1,%s) ON CONFLICT DO NOTHING', (secrets.token_hex(32),))


def cleanup():
    from .auth import account_lock
    # One account per transaction; no private row lock before the account gate.
    cursor = None
    while True:
        with database() as conn:
            owners = conn.execute('SELECT id FROM accounts WHERE (%s::uuid IS NULL OR id > %s::uuid) ORDER BY id LIMIT 100', (cursor, cursor)).fetchall()
        if not owners:
            break
        for account in owners:
            with database() as conn:
                account_lock(conn, account['id'])
                conn.execute("DELETE FROM sessions WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM workday_notices WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM account_notice_operations WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM notice_creation_admissions WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM drafts WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM workdays WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM workday_operations WHERE owner=%s AND (expires_at <= clock_timestamp() OR (workday_id IS NULL AND NOT EXISTS (SELECT 1 FROM drafts WHERE drafts.id=workday_operations.draft_id)))", (account['id'],))
                conn.execute("DELETE FROM draft_operations WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM draft_deletions WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM workday_deletions WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM workday_bus_operations WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM workday_selection_operations WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM workday_start_operations WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM workday_outcome_operations WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM workday_close_operations WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM workday_notice_operations WHERE owner=%s AND (expires_at <= clock_timestamp())", (account['id'],))
                conn.execute("DELETE FROM workday_notice_operations o WHERE o.owner=%s AND (NOT EXISTS (SELECT 1 FROM workday_notices n WHERE n.id::text=o.result->>'id'))", (account['id'],))
        cursor = owners[-1]['id']
    with database() as conn:
        conn.execute('DELETE FROM login_limits WHERE expires_at <= clock_timestamp()')
