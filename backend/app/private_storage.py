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
    with database() as conn:
        # Requests lock sessions before drafts; cleanup must follow that order too.
        conn.execute('DELETE FROM sessions WHERE expires_at <= clock_timestamp()')
        conn.execute('DELETE FROM drafts WHERE expires_at <= clock_timestamp()')
        conn.execute('DELETE FROM draft_operations WHERE expires_at <= clock_timestamp()')
        conn.execute('DELETE FROM draft_deletions WHERE expires_at <= clock_timestamp()')
        conn.execute('DELETE FROM login_limits WHERE expires_at <= clock_timestamp()')
