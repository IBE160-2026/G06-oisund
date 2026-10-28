"""Only the disposable submission runtime may initialize/reset synthetic data."""
import json
import os
import sys
from pathlib import Path
from uuid import uuid4

from app.auth import password_hash, require_synthetic_accounts
from app.private_storage import database


def guard():
    if (os.environ.get('SUBMISSION_PROJECT') != 'ibe160-submission'
            or os.environ.get('PRIVATE_DATABASE_URL') != 'postgresql://private_work@private-db/private_work'
            or os.environ.get('PRIVATE_DATABASE_PASSWORD_FILE') != '/run/secrets/submission_password'
            or os.environ.get('PRIVATE_ORIGIN') != 'http://127.0.0.1:15325'):
        raise RuntimeError('Submission target configuration required')
    account = json.loads(Path('/run/secrets/submission_account').read_text())
    if (account.get('username') != 'synthetic-submission'
            or not isinstance(account.get('password'), str) or not 32 <= len(account['password']) <= 256):
        raise RuntimeError('Generated synthetic submission account required')
    return account


def main(action):
    if action not in {'init', 'reset', 'check'}:
        raise RuntimeError('Use init | reset | check')
    account = guard()
    with database() as conn:
        conn.execute('SELECT pg_advisory_xact_lock(125001)')
        identity = conn.execute('SELECT current_database() AS db,current_user AS role').fetchone()
        if identity != {'db': 'private_work', 'role': 'private_work'}:
            raise RuntimeError('Submission database identity required')
        # Lock before preflight: concurrent account creation cannot race reset.
        conn.execute('LOCK TABLE accounts IN ACCESS EXCLUSIVE MODE')
        require_synthetic_accounts(conn)
        if action == 'reset':
            conn.execute('TRUNCATE accounts,login_limits CASCADE')
        existing = conn.execute('SELECT password_hash FROM accounts WHERE username=%s', (account['username'],)).fetchone()
        if existing:
            salt = existing['password_hash'].split(':')[0]
            if password_hash(account['password'], salt) != existing['password_hash']:
                raise RuntimeError('Preserve the original generated account secret; password mismatch')
        elif action == 'check':
            raise RuntimeError('Initialize the synthetic submission account first')
        else:
            conn.execute('INSERT INTO accounts VALUES (%s,%s,%s)', (uuid4(), account['username'], password_hash(account['password'])))
    print('Synthetic submission account verified; credentials remain in ignored local account.json.')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) == 2 else '')
