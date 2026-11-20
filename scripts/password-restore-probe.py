"""Disposable restore probe: never prints synthetic credentials or raw exceptions."""
import json
import os
from pathlib import Path
import secrets
import sys
from types import SimpleNamespace
from uuid import uuid4
import httpx
from fastapi import HTTPException
from app import auth, restore, password_recovery as recovery
from app.private_storage import database, migrate

STATE = Path('/state/restore-state.json')


def require(value):
    if not value:
        raise RuntimeError('Restore invariant failed')


def rejected(fn, status):
    try:
        fn()
    except HTTPException as error:
        require(error.status_code == status)
        return
    require(False)


def marker(state, value):
    state.setdefault('fresh_markers', []).append(value)
    STATE.write_text(json.dumps(state))


def main(phase):
    require(os.environ.get('PRIVATE_TEST_PROJECT') == 'ibe160-private-tests')
    if phase != 'guards':
        with database() as conn:
            auth.require_synthetic_accounts(conn)
    if phase == 'seed':
        state = {'names': ['synthetic-restore-' + uuid4().hex for _ in range(2)],
                 'old': secrets.token_urlsafe(24), 'new': secrets.token_urlsafe(24), 'codes': [], 'tokens': []}
        state['ids'] = [str(auth.provision(name, state['old'])) for name in state['names']]
        from test_private_drafts import save
        from test_private_workdays import prepare, confirm
        from test_account_notices import send, command, content
        from test_private_access import headers
        for name in state['names']:
            with httpx.Client(base_url='http://private-api:8000', timeout=30) as client:
                response = client.post('/auth/login', headers=headers(client), json={'username': name, 'password': state['old']})
                require(response.status_code == 200)
                state['tokens'].append(client.cookies.get(auth.SESSION))
                require(save(client)[0].status_code == 200)
                draft, _, decision = prepare(client)
                require(confirm(client, draft, decision).status_code == 200)
                require(send(client, command(content=content())).status_code == 200)
            state['codes'].append(recovery.issue(recovery.resolve(name))[0])
        state['business'] = restore.snapshot()['business']
        STATE.write_text(json.dumps(state))
    elif phase == 'pre015':
        with database() as conn:
            conn.execute('DROP TABLE recovery_audit, recovery_proofs')
            conn.execute("DELETE FROM private_migrations WHERE name='015_password_recovery.sql'")
        require(restore.snapshot()['schema'] == 14)
    elif phase == 'journey':
        state = json.loads(STATE.read_text())
        require(restore.snapshot()['business'] == state['business'])
        migrate()
        require(restore.snapshot()['business'] == state['business'])
        result = restore.quarantine()
        require(result['business'] == state['business'])
        require(result['authority_fingerprint'] == restore.checked()['authority_fingerprint'])
        for name, code, token in zip(state['names'], state['codes'], state['tokens']):
            rejected(lambda: auth.authenticate(name, state['old'], 'synthetic-restore'), 401)
            with database() as conn:
                rejected(lambda: auth.session(conn, SimpleNamespace(cookies={auth.SESSION: token})), 401)
            rejected(lambda: recovery.redeem(SimpleNamespace(cookies={}, client=SimpleNamespace(host='synthetic-restore')),
                     name, code, state['new'], state['new']), 400)
        for i, name in enumerate(state['names']):
            code, _ = recovery.issue(recovery.resolve(name))
            marker(state, code)
            recovery.redeem(SimpleNamespace(cookies={}, client=SimpleNamespace(host='synthetic-fresh')),
                            name, code, state['new'], state['new'])
            token, session = auth.authenticate(name, state['new'], 'synthetic-new')
            marker(state, token)
            require(str(session['owner']) == state['ids'][i])
            if i == 0:
                rejected(lambda: auth.authenticate(state['names'][1], state['old'], 'synthetic-wait'), 401)
        require(restore.snapshot()['business'] == state['business'])
        migrate()
        for name in state['names']:
            token, _ = auth.authenticate(name, state['new'], 'synthetic-ordinary-migration')
            marker(state, token)
    elif phase == 'ordinary-restart':
        state = json.loads(STATE.read_text())
        for name in state['names']:
            token, _ = auth.authenticate(name, state['new'], 'synthetic-ordinary-restart')
            marker(state, token)
    elif phase == 'scan':
        state = json.loads(STATE.read_text())
        text = sys.stdin.read()
        markers = [state['old'], state['new'], *state['codes'], *state['tokens'], *state.get('fresh_markers', [])]
        require(not any(secret in text for secret in markers))
        with database() as conn:
            from psycopg import sql
            for row in conn.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'").fetchall():
                query=sql.SQL('SELECT row_to_json(t)::text AS row FROM {} t').format(sql.Identifier(row['tablename']))
                for item in conn.execute(query):
                    require(not any(secret in item['row'] for secret in markers))
    elif phase == 'guards':
        import re
        import subprocess
        import tempfile
        guards = re.findall(r'test -d /maintenance;[^\n]*?test -f /maintenance/local-start;',Path('/host-tests/compose.yaml').read_text())
        require(len(guards)==3)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'maintenance'
            for guard in guards:
                actual = guard.replace('/maintenance', str(path)) + ' exit 0'
                def allowed():
                    return subprocess.run(['/bin/sh','-ec',actual],capture_output=True).returncode == 0
                require(not allowed()); require(not allowed())
                path.mkdir()
                require(allowed()); require(allowed())
                (path/'pending.json').write_text('{}')
                require(not allowed()); require(not allowed())
                (path/'local-start').write_text('local readiness only')
                require(allowed())
                (path/'local-start').unlink()
                require(not allowed())
                (path/'pending.json').unlink()
                path.chmod(0)
                try: require(not allowed()); require(not allowed())
                finally: path.chmod(0o700)
                path.rmdir()
    elif phase == 'unsupported':
        with database() as conn:
            conn.execute('CREATE TABLE synthetic_unknown_schema(id integer)')
        try:
            try: restore.snapshot()
            except ValueError: pass
            else: require(False)
        finally:
            with database() as conn:conn.execute('DROP TABLE synthetic_unknown_schema')
        with database() as conn:conn.execute("INSERT INTO private_migrations VALUES ('016_unknown.sql')")
        try:
            try: restore.snapshot()
            except ValueError: pass
            else: require(False)
        finally:
            with database() as conn:conn.execute("DELETE FROM private_migrations WHERE name='016_unknown.sql'")
    else:
        raise ValueError('Unknown phase')
    print('PASS restore ' + phase)


try:
    main(sys.argv[1])
except Exception:
    print('FAIL restore invariant', file=sys.stderr)
    raise SystemExit(1) from None
