import os
from pathlib import Path
from urllib.parse import urlparse

import psycopg
from psycopg.rows import dict_row

OWNER = 'fictional-assessment-owner'


def database():
    url = os.environ.get('DATABASE_URL', '')
    parsed = urlparse(url)
    if (os.environ.get('APP_MODE') != 'fictional-assessment'
            or parsed.scheme not in {'postgresql', 'postgres'} or parsed.query or parsed.fragment
            or parsed.path != '/fictional_assessment' or parsed.username != 'fictional'
            or parsed.hostname not in {'db', 'localhost', '127.0.0.1'}):
        raise RuntimeError('Only the isolated fictional assessment database is allowed')
    return psycopg.connect(url, row_factory=dict_row, connect_timeout=3)


def migrate():
    with database() as conn:
        conn.execute(Path('migrations/001_initial.sql').read_text())


def cleanup():
    with database() as conn:
        conn.execute('DELETE FROM creation_operations WHERE expires_at <= clock_timestamp() '
                     'OR id IN (SELECT operation_id FROM fictional_days WHERE expires_at <= clock_timestamp())')
