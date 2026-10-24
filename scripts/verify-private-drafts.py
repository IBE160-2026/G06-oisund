"""Disposable-only private draft verification; restores the operational API."""
import json
import os
from pathlib import Path
import secrets
import subprocess
import urllib.request
import urllib.error
import http.cookiejar
from uuid import UUID, uuid4

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


def denied(path, code, port=8001, body=None):
    try:
        probe = urllib.request.Request(f'http://127.0.0.1:{port}' + path, json.dumps(body).encode() if body is not None else None,
                                       {'Origin': 'http://127.0.0.1:5173', 'Content-Type': 'application/json'}) if body is not None else f'http://127.0.0.1:{port}' + path
        opener.open(probe, timeout=10)
    except urllib.error.HTTPError as error:
        assert error.code == code
        return
    raise AssertionError('Expected safe denial')


try:
    run(OPERATIONAL + ['stop', 'private-api'])
    run(PRIVATE + ['up', '-d', '--build', '--wait'])
    python('')
    print(run(PRIVATE + ['run', '--rm', '--no-deps', '-v', str(ROOT / 'Eksempelfiler') + ':/fixtures:ro', '-e', 'PRIVATE_TEST_PROJECT=' + PROJECT, '-e', 'PRIVATE_TEST_API=http://private-api:8000', 'private-api', 'python', '-m', 'pytest', '-q', '--tb=short', 'tests/test_private_access.py', 'tests/test_private_drafts.py', 'tests/test_private_workdays.py', 'tests/test_private_bus.py', 'tests/test_private_import.py', 'tests/test_pdf_import.py']), flush=True)
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
    # A separate saved revision gives restart evidence for the confirmed snapshot,
    # its decisions and independent deadline, alongside the existing draft proof.
    planned = json.loads(json.dumps(imported))
    planned['service_date'] = '2031-01-02'
    for index, activity in enumerate(planned['activities']):
        activity.update(start=f'2031-01-02T{10 + index // 60:02}:{index % 60:02}+01:00', end=f'2031-01-02T{10 + index // 60:02}:{index % 60:02}+01:00')
    plan_source = request('/drafts', {'operation_id': request('/draft-operations', {})['operation_id'], 'expected_revision': 0, 'draft': planned})
    review = request('/workday-reviews', {'draft_id': plan_source['id'], 'expected_revision': 1})
    confirmation = {'operation_id': review['operation_id'], 'expected_revision': 1, 'acknowledgements': [item['id'] for item in review['unknowns']], 'classifications': {key: 'manual' for key in review['classifications_required']}}
    confirmed = request('/drafts/' + plan_source['id'] + '/confirm', confirmation)
    bus_path = '/workdays/' + confirmed['id'] + '/physical-bus'
    initial_bus = request(bus_path)
    assert initial_bus['revision'] == 0 and initial_bus['physical_bus'] is None
    bus_body = {'operation_id': str(uuid4()), 'expected_revision': 0, 'physical_bus': ' 0006 / 090 '}
    bus_receipt = request(bus_path, bus_body)
    current_bus = request(bus_path)
    assert current_bus == bus_receipt['result'] and current_bus['expires_at'] == confirmed['expires_at']
    deleted_source = request('/drafts', {'operation_id': request('/draft-operations', {})['operation_id'], 'expected_revision': 0, 'draft': planned})
    deleted_review = request('/workday-reviews', {'draft_id': deleted_source['id'], 'expected_revision': 1})
    deleted_confirmation = {'operation_id': deleted_review['operation_id'], 'expected_revision': 1, 'acknowledgements': [item['id'] for item in deleted_review['unknowns']], 'classifications': {key: 'manual' for key in deleted_review['classifications_required']}}
    deleted_plan = request('/drafts/' + deleted_source['id'] + '/confirm', deleted_confirmation)
    deletion = {'operation_id': str(uuid4()), 'source_revision': 1}
    receipt = request('/workdays/' + deleted_plan['id'] + '/delete', deletion)
    pending_review = request('/workday-reviews', {'draft_id': original['id'], 'expected_revision': original['revision']})
    state_program = f"import json\nwith database() as conn:\n print(json.dumps({{'plans':conn.execute('SELECT * FROM workdays WHERE owner=%s ORDER BY id', ({session['account_id']!r},)).fetchall(), 'operations':conn.execute('SELECT * FROM workday_operations WHERE owner=%s ORDER BY id', ({session['account_id']!r},)).fetchall(), 'deletions':conn.execute('SELECT * FROM workday_deletions WHERE owner=%s ORDER BY id', ({session['account_id']!r},)).fetchall(), 'confirmed_sources':conn.execute('SELECT id,confirmed FROM drafts WHERE owner=%s ORDER BY id', ({session['account_id']!r},)).fetchall()}},default=str,sort_keys=True))\n"
    state_program = state_program.replace("'confirmed_sources':", "'buses':conn.execute('SELECT b.* FROM workday_buses b JOIN workdays w ON b.workday_id=w.id WHERE w.owner=%s ORDER BY b.workday_id', (" + repr(session['account_id']) + ",)).fetchall(), 'bus_operations':conn.execute('SELECT * FROM workday_bus_operations WHERE owner=%s ORDER BY id', (" + repr(session['account_id']) + ",)).fetchall(), 'confirmed_sources':")
    persisted_confirmation_state = python(state_program)
    def listed_drafts():
        rows, cursor, visited = [], None, set()
        while True:
            page = request('/drafts' + ('?cursor=' + cursor if cursor else ''))
            assert set(page) == {'drafts', 'next_cursor'} and len(page['drafts']) <= 50
            rows.extend(page['drafts'])
            next_cursor = page['next_cursor']
            if next_cursor is None:
                assert len({row['id'] for row in rows}) == len(rows)
                return rows
            assert next_cursor not in visited and (cursor is None or UUID(next_cursor).int > UUID(cursor).int), 'Draft pagination did not advance'
            visited.add(next_cursor)
            cursor = next_cursor
    persisted_draft_list = listed_drafts()
    run(['docker', 'compose', '-p', 'ibe160-fictional-assessment', 'up', '-d', '--build', '--wait', 'api'])
    denied('/drafts', 404, 8000)
    denied('/drafts/' + original['id'], 404, 8000)
    denied('/draft-operations/' + operation, 404, 8000)
    denied('/imports/pdf', 404, 8000)
    denied('/workdays', 404, 8000)
    denied('/workdays/' + confirmed['id'], 404, 8000)
    denied(bus_path, 404, 8000)
    denied(bus_path, 404, 8000, bus_body)
    denied('/workday-bus-operations/' + bus_body['operation_id'], 404, 8000)
    expired_operation = request('/draft-operations', {})['operation_id']
    python(f"with database() as conn:\n conn.execute('UPDATE draft_operations SET expires_at=clock_timestamp() WHERE id=%s', ({expired_operation!r},))\n")
    for _ in range(2):
        run(PRIVATE + ['exec', '-T', 'private-api', 'python', '-m', 'app.manage', 'migrate'])
    run(PRIVATE + ['restart', 'private-db', 'private-api'])
    run(PRIVATE + ['up', '-d', '--wait'])
    assert request('/auth/session') == session
    assert request('/drafts/' + original['id']) == original
    assert listed_drafts() == persisted_draft_list
    assert request('/drafts', body) == original
    assert request('/draft-operations/' + operation) == {'state': 'accepted', 'result': original}
    assert request(bus_path) == current_bus
    assert request(bus_path, bus_body) == bus_receipt
    assert request('/workday-bus-operations/' + bus_body['operation_id']) == bus_receipt
    assert request('/workdays/' + confirmed['id']) == confirmed
    assert request('/drafts/' + plan_source['id'] + '/confirm', confirmation) == confirmed
    assert request('/workday-operations/' + confirmation['operation_id']) == {'state': 'accepted', 'result': confirmed}
    assert request('/workday-operations/' + pending_review['operation_id']) == {'state': 'pending', 'result': None}
    assert request('/workday-deletions/' + deletion['operation_id']) == receipt
    assert request('/workdays/' + deleted_plan['id'] + '/delete', deletion) == receipt
    assert request('/drafts/' + deleted_source['id']) == deleted_source
    denied('/workdays/' + deleted_plan['id'], 404)
    denied('/workday-operations/' + deleted_confirmation['operation_id'], 404)
    assert python(state_program) == persisted_confirmation_state
    denied('/draft-operations/' + expired_operation, 404)
    run(PRIVATE + ['exec', '-T', 'private-api', 'python', '-m', 'app.manage', 'cleanup'])
    assert request('/drafts/' + original['id']) == original
    print('PASS: PostgreSQL/API restart, migration replay, account/session preservation, identical draft/confirmed-plan/current-bus/bus-operation-receipt/decisions/operation/deletion-receipt/source-marker/deadlines and cleanup.', flush=True)
    print(run(['npm.cmd', 'run', 'build'], cwd=ROOT / 'frontend'), flush=True)
    run(['docker', 'compose', '-p', 'ibe160-fictional-assessment', 'up', '-d', '--build', '--wait', 'frontend'])
    print(run(['npx.cmd', 'playwright', 'test'], cwd=ROOT / 'frontend'))
finally:
    # Keep volumes/secret, including the disposable data, available for inspection.
    try:
        run(PRIVATE + ['stop'])
    finally:
        run(OPERATIONAL + ['up', '-d', '--wait', 'private-api'])
