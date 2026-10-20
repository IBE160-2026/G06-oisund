"""Sequential, local integration evidence; emits no account/session credentials."""
import http.cookiejar
import json
from pathlib import Path
import secrets
import subprocess
import time
import urllib.error
import urllib.request
from uuid import uuid4

ROOT = Path(__file__).resolve().parent.parent
PRIVATE = ['docker', 'compose', '-f', 'compose.private.yaml']
NAME = 'synthetic-restart-' + uuid4().hex
PASSWORD = secrets.token_urlsafe(24)


def command(args, program=None):
    return subprocess.check_output(args, cwd=ROOT, input=program, text=True, stderr=subprocess.STDOUT)


def sql_program(program):
    return command(PRIVATE + ['exec', '-T', 'private-api', 'python', '-'], program)


jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def request(path, body=None, proof=None, port=8001):
    headers = {'Origin': 'http://127.0.0.1:5173'}
    if proof:
        headers['X-CSRF-Token'] = proof
    if body is not None:
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(f'http://127.0.0.1:{port}' + path,
                                 json.dumps(body).encode() if body is not None else None, headers)
    try:
        with opener.open(req, timeout=5) as response:
            assert response.headers['Cache-Control'] == 'no-store'
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, json.load(error)


def wait():
    for _ in range(40):
        try:
            if request('/health')[0] == 200:
                return
        except (OSError, ValueError):
            pass
        time.sleep(.5)
    raise RuntimeError('Private runtime did not recover')


prepared = False
try:
    sql_program(f'from app.auth import provision, require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\nprovision({NAME!r}, {PASSWORD!r})\n')
    prepared = True
    proof = request('/auth/csrf')[1]['csrf_token']
    status, original = request('/auth/login', {'username': NAME, 'password': PASSWORD}, proof)
    assert status == 200
    identifier = original['account_id']
    metadata_program = "import json\nfrom app.private_storage import database\nwith database() as conn:\n print(json.dumps(conn.execute('SELECT * FROM login_limits ORDER BY bucket').fetchall(), default=str))\n"
    metadata = sql_program(metadata_program)
    command(PRIVATE + ['restart', 'private-db', 'private-api'])
    wait()
    assert request('/auth/session') == (200, original)
    assert sql_program(metadata_program) == metadata
    command(PRIVATE + ['exec', '-T', 'private-api', 'python', '-m', 'app.manage', 'migrate'])
    command(PRIVATE + ['exec', '-T', 'private-api', 'python', '-m', 'app.manage', 'migrate'])
    command(PRIVATE + ['exec', '-T', 'private-api', 'python', '-m', 'app.manage', 'cleanup'])
    assert request('/auth/session') == (200, original)
    command(['docker', 'compose', '-p', 'ibe160-fictional-assessment', 'exec', '-T', 'api', 'python', '-m', 'app.manage', 'reset', '--fictional-only'])
    assert request('/auth/session') == (200, original)
    assert request('/accounts/' + identifier)[0] == 200
    assert request('/accounts/' + identifier, port=8000)[0] == 404
    assert request('/days/' + identifier, port=8000)[0] == 410
    proof = request('/auth/csrf')[1]['csrf_token']
    assert request('/auth/logout', {}, proof) == (200, {'revoked': True})
    assert request('/auth/session')[0] == 401
    print('PASS: private DB/API restart, fixed deadline, migration replay, cleanup, isolated demo reset, crossed identifiers and revocation.')
finally:
    if prepared:
        sql_program(f"from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n conn.execute('DELETE FROM sessions WHERE owner IN (SELECT id FROM accounts WHERE username=%s)', ({NAME!r},))\n conn.execute('DELETE FROM accounts WHERE username=%s', ({NAME!r},))\n")
