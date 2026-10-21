"""Disposable-only private draft verification; restores the operational API."""
import json
import os
from pathlib import Path
import secrets
import subprocess
import urllib.request
import urllib.error
import http.cookiejar
from uuid import uuid4

ROOT = Path(__file__).resolve().parent.parent
PROJECT = 'ibe160-private-tests'
if os.environ.get('COMPOSE_PROJECT_NAME') != PROJECT:
    raise SystemExit('Refusing test mutations: select COMPOSE_PROJECT_NAME=ibe160-private-tests first.')
PRIVATE = ['docker', 'compose', '-p', PROJECT, '-f', 'compose.private.yaml']
OPERATIONAL = ['docker', 'compose', '-p', 'ibe160-private-work', '-f', 'compose.private.yaml']


def run(args, program=None, cwd=ROOT):
    result = subprocess.run(args, cwd=cwd, input=program, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        # All output belongs to synthetic tests; never emit provisioned credentials.
        print(result.stdout)
        raise RuntimeError('Verification command failed: ' + ' '.join(args))
    return result.stdout


def python(program):
    guard = 'from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n'
    return run(PRIVATE + ['exec', '-T', 'private-api', 'python', '-'], guard + program)


jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def request(path, body=None):
    headers = {'Origin': 'http://127.0.0.1:5173'}
    if body is not None:
        token = request('/auth/csrf')['csrf_token']
        headers.update({'Content-Type': 'application/json', 'X-CSRF-Token': token})
    with opener.open(urllib.request.Request('http://127.0.0.1:8001' + path, json.dumps(body).encode() if body is not None else None, headers), timeout=20) as response:
        assert response.headers['Cache-Control'] == 'no-store'
        return json.load(response)


def denied(path, code, port=8001):
    try:
        opener.open(f'http://127.0.0.1:{port}' + path, timeout=10)
    except urllib.error.HTTPError as error:
        assert error.code == code
        return
    raise AssertionError('Expected safe denial')


try:
    run(OPERATIONAL + ['stop', 'private-api'])
    run(PRIVATE + ['up', '-d', '--build', '--wait'])
    python('')
    print(run(PRIVATE + ['run', '--rm', '--no-deps', '-v', str(ROOT / 'Eksempelfiler') + ':/fixtures:ro', '-e', 'PRIVATE_TEST_PROJECT=' + PROJECT, '-e', 'PRIVATE_TEST_API=http://private-api:8000', 'private-api', 'python', '-m', 'pytest', '-q', '--tb=short', 'tests/test_private_access.py', 'tests/test_private_drafts.py', 'tests/test_private_import.py', 'tests/test_pdf_import.py']), flush=True)
    username = 'synthetic-draft-restart-' + uuid4().hex
    password = secrets.token_urlsafe(24)
    python(f'from app.auth import provision\nprovision({username!r}, {password!r})\n')
    session = request('/auth/login', {'username': username, 'password': password})
    operation = request('/draft-operations', {})['operation_id']
    body = {'operation_id': operation, 'expected_revision': 0, 'draft': {'service_date': '2026-10-24', 'vehicle_duty': '0007', 'physical_bus': 'Bus-0012', 'activities': [{'id': str(uuid4()), 'raw_code': 'Unknown', 'source_start': '25:10', 'start': '2026-10-25T01:10+02:00', 'end': '2026-10-25T01:10+02:00'}]}}
    imported = json.loads(python('import sys\nsys.path.insert(0, "/app/tests")\nfrom test_pdf_import import synthetic_text_pdf\nfrom app.pdf_import import parse_document\nfrom app.private_import import interpret\nprint(interpret(parse_document(synthetic_text_pdf())).model_dump_json())\n'))
    body['draft'] = {**imported, 'vehicle_duty': '0007', 'physical_bus': 'Bus-0012'}
    original = request('/drafts', body)
    assert original['draft']['realtime_duty'] == '007' and original['draft']['physical_bus'] == 'Bus-0012'
    run(['docker', 'compose', '-p', 'ibe160-fictional-assessment', 'up', '-d', '--build', '--wait', 'api'])
    denied('/drafts', 404, 8000)
    denied('/drafts/' + original['id'], 404, 8000)
    denied('/draft-operations/' + operation, 404, 8000)
    denied('/imports/pdf', 404, 8000)
    expired_operation = request('/draft-operations', {})['operation_id']
    python(f"with database() as conn:\n conn.execute('UPDATE draft_operations SET expires_at=clock_timestamp() WHERE id=%s', ({expired_operation!r},))\n")
    for _ in range(2):
        run(PRIVATE + ['exec', '-T', 'private-api', 'python', '-m', 'app.manage', 'migrate'])
    run(PRIVATE + ['restart', 'private-db', 'private-api'])
    run(PRIVATE + ['up', '-d', '--wait'])
    assert request('/auth/session') == session
    assert request('/drafts/' + original['id']) == original
    assert request('/drafts', body) == original
    assert request('/draft-operations/' + operation) == {'state': 'accepted', 'result': original}
    denied('/draft-operations/' + expired_operation, 404)
    run(PRIVATE + ['exec', '-T', 'private-api', 'python', '-m', 'app.manage', 'cleanup'])
    assert request('/drafts/' + original['id']) == original
    print('PASS: PostgreSQL/API restart, migration replay, account/session preservation, identical draft/operation/deadline and cleanup.', flush=True)
    print(run(['npm.cmd', 'run', 'build'], cwd=ROOT / 'frontend'), flush=True)
    run(['docker', 'compose', '-p', 'ibe160-fictional-assessment', 'up', '-d', '--build', '--wait', 'frontend'])
    print(run(['npx.cmd', 'playwright', 'test'], cwd=ROOT / 'frontend'))
finally:
    # Keep volumes/secret, including the disposable data, available for inspection.
    try:
        run(PRIVATE + ['stop'])
    finally:
        run(OPERATIONAL + ['up', '-d', '--wait', 'private-api'])
