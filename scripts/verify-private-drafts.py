"""Disposable-only private draft verification; restores the operational API."""
import json
import os
from pathlib import Path
import secrets
import subprocess
import urllib.request
import urllib.error
import http.cookiejar
from datetime import datetime
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
        value = json.load(response)
        if path == '/notices' and body is None: value.pop('server_now', None)
        return value


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
    print(run(PRIVATE + ['run', '--rm', '--no-deps', '-v', str(ROOT / 'Eksempelfiler') + ':/fixtures:ro', '-e', 'PRIVATE_TEST_PROJECT=' + PROJECT, '-e', 'PRIVATE_TEST_API=http://private-api:8000', 'private-api', 'python', '-m', 'pytest', '-q', '--tb=short', 'tests/test_private_access.py', 'tests/test_private_drafts.py', 'tests/test_private_workdays.py', 'tests/test_private_bus.py', 'tests/test_private_selection.py', 'tests/test_private_start.py', 'tests/test_private_outcomes.py', 'tests/test_private_notices.py', 'tests/test_notice_reader.py', 'tests/test_account_notices.py', 'tests/test_private_import.py', 'tests/test_pdf_import.py']), flush=True)
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
    selection_path = '/workdays/' + confirmed['id'] + '/selection'
    lifecycle_path = '/workdays/' + confirmed['id'] + '/lifecycle'
    start_path = '/workdays/' + confirmed['id'] + '/start'
    assert request(selection_path)['activity_id'] is None
    initial_lifecycle = request(lifecycle_path)
    assert initial_lifecycle['state'] == 'confirmed' and initial_lifecycle['started_at'] is None and initial_lifecycle['revision'] == 0
    selection_body = {'operation_id': str(uuid4()), 'expected_revision': 0, 'activity_id': confirmed['draft']['activities'][-1]['id']}
    selection_receipt = request(selection_path, selection_body)
    assert request(lifecycle_path) == initial_lifecycle
    start_body = {'operation_id': str(uuid4()), 'expected_revision': 0}
    start_receipt = request(start_path, start_body)
    assert start_receipt['result']['state'] == 'active' and start_receipt['result']['revision'] == 1
    assert request(selection_path) == selection_receipt['result']
    notice_path = '/notices'
    notice_body = {'operation_id': request('/notice-operations', {})['operation_id'], 'expected_revision': 0, 'content': {'title': 'Synthetic SMS traffic notice', 'summary': 'Temporary stop', 'description': 'Monday 06-08\nTuesday 16-18\nUse the temporary stop.', 'source_note': 'SMS from synthetic traffic control', 'line_scope': 'all', 'line_tags': [], 'source_url': None, 'source_updated_at': None, 'valid_from': '2031-01-02T23:00:00+01:00', 'valid_until': '2031-01-04T23:59:59+01:00'}}
    notice_receipt = request(notice_path, notice_body)
    notice_id = notice_receipt['result']['id']
    assert all(notice_receipt['result'][key] == value for key, value in notice_body['content'].items())
    notice_check = {'operation_id': str(uuid4()), 'expected_revision': 1}
    notice_checked_receipt = request(notice_path + '/' + notice_id + '/check', notice_check)
    notice_ending = {'operation_id': str(uuid4()), 'expected_revision': 2}
    notice_ended_receipt = request(notice_path + '/' + notice_id + '/end', notice_ending)
    notice_snapshot = request(notice_path)
    assert notice_snapshot['notices'] == [notice_ended_receipt['result']]
    assert notice_snapshot['notices'][0]['checked_revision'] == 2 and notice_snapshot['notices'][0]['status'] == 'ended_manually'
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
    # Include raw mutable authorities and both immutable receipt tables in the
    # exact populated migration/restart comparison, with no current-time fields.
    for table, key in [('workday_selections', 'workday_id'), ('workday_lifecycles', 'workday_id'), ('workday_selection_operations', 'id'), ('workday_start_operations', 'id'), ('workday_outcome_revisions', 'workday_id'), ('workday_outcomes', 'activity_id'), ('workday_outcome_operations', 'id'), ('workday_close_operations', 'id'), ('workday_notices', 'id'), ('workday_notice_operations', 'id'), ('account_notice_operations', 'id')]:
        query = ('SELECT t.* FROM ' + table + ' t WHERE t.owner=%s ORDER BY t.' + key) if table in {'workday_notices', 'workday_notice_operations', 'account_notice_operations'} else ('SELECT t.* FROM ' + table + ' t JOIN workdays w ON t.workday_id=w.id WHERE w.owner=%s ORDER BY t.' + key)
        state_program = state_program.replace("'confirmed_sources':", repr(table) + ":conn.execute(" + repr(query) + ", (" + repr(session['account_id']) + ",)).fetchall(), 'confirmed_sources':")
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
    for route in [selection_path, lifecycle_path, '/workday-selection-operations/' + selection_body['operation_id'], '/workday-start-operations/' + start_body['operation_id']]:
        denied(route, 404, 8000)
    denied(selection_path, 404, 8000, selection_body)
    denied(start_path, 404, 8000, start_body)
    for route in [notice_path, notice_path + '/' + notice_id, '/workday-notice-operations/' + notice_body['operation_id']]:
        denied(route, 404, 8000)
    denied(notice_path, 404, 8000, notice_body)
    # Retain a distinct terminal plan while leaving legacy active/unstarted
    # cases intact. Exercise unknown membership and shortened current authority.
    terminal_source = request('/drafts', {'operation_id': request('/draft-operations', {})['operation_id'], 'expected_revision': 0, 'draft': planned})
    terminal_review = request('/workday-reviews', {'draft_id': terminal_source['id'], 'expected_revision': 1})
    terminal_decisions = {'operation_id': terminal_review['operation_id'], 'expected_revision': 1, 'acknowledgements': [item['id'] for item in terminal_review['unknowns']], 'classifications': {key: 'manual' for key in terminal_review['classifications_required']}}
    terminal_plan = request('/drafts/' + terminal_source['id'] + '/confirm', terminal_decisions)
    terminal_base = '/workdays/' + terminal_plan['id']
    terminal_start_body = {'operation_id': str(uuid4()), 'expected_revision': 0}
    terminal_start = request(terminal_base + '/start', terminal_start_body)
    terminal_notice_body = {**notice_body, 'operation_id': str(uuid4())}
    terminal_notice_receipt = request(notice_path, terminal_notice_body)
    outcome_body = {'operation_id': str(uuid4()), 'expected_revision': 0, 'expected_lifecycle_revision': 1, 'activity_id': terminal_plan['draft']['activities'][0]['id'], 'outcome': 'skipped'}
    outcome_receipt = request(terminal_base + '/outcome', outcome_body)
    close_body = {'operation_id': str(uuid4()), 'expected_revision': 1, 'expected_outcome_revision': 1, 'action': 'ended'}
    close_receipt = request(terminal_base + '/close', close_body)
    terminal_snapshot = request(terminal_base + '/recap')
    assert terminal_snapshot['lifecycle'] == close_receipt['result']
    assert terminal_snapshot['lifecycle']['started_at'] == terminal_start['result']['started_at']
    assert terminal_snapshot['outcomes']['outcomes'] == outcome_receipt['result']['outcomes']
    assert terminal_snapshot['outcomes']['outcomes'][0]['outcome'] == 'skipped'
    assert all(item['outcome'] == 'unregistered' for item in terminal_snapshot['outcomes']['outcomes'][1:])
    assert terminal_snapshot['plan']['expires_at'] < terminal_plan['expires_at']
    terminal_notices = request(notice_path)
    assert any(n['id'] == terminal_notice_receipt['result']['id'] for n in terminal_notices['notices'])
    assert next(n for n in terminal_notices['notices'] if n['id'] == terminal_notice_receipt['result']['id'])['expires_at'] == terminal_notice_receipt['result']['expires_at']
    assert datetime.fromisoformat(json.loads(python(f"import json\nwith database() as conn:\n print(json.dumps(str(conn.execute('SELECT expires_at FROM account_notice_operations WHERE id=%s', ({terminal_notice_body['operation_id']!r},)).fetchone()['expires_at'])))\n"))) == datetime.fromisoformat(terminal_notice_receipt['result']['expires_at'])
    for route in [terminal_base + '/outcomes', terminal_base + '/recap', '/workday-outcome-operations/' + outcome_body['operation_id'], '/workday-close-operations/' + close_body['operation_id']]:
        denied(route, 404, 8000)
    denied(terminal_base + '/outcome', 404, 8000, outcome_body)
    denied(terminal_base + '/close', 404, 8000, close_body)
    expired_operation = request('/draft-operations', {})['operation_id']
    python(f"with database() as conn:\n conn.execute('UPDATE draft_operations SET expires_at=clock_timestamp() WHERE id=%s', ({expired_operation!r},))\n")
    # Synthetic pre-upgrade issuance: default v1/false columns preserve pending
    # request bodies, accepted decisions and exact raw facts across migration.
    legacy_operation = request('/draft-operations', {})['operation_id']
    python(f"with database() as conn:\n conn.execute('UPDATE draft_operations SET normalize_physical_bus=false WHERE id=%s', ({legacy_operation!r},))\n")
    legacy_body = {'operation_id': legacy_operation, 'expected_revision': 0, 'draft': {**planned, 'physical_bus': '\u0085\u2003'}}
    legacy_draft = request('/drafts', legacy_body)
    assert legacy_draft['draft']['physical_bus'] == legacy_body['draft']['physical_bus']
    legacy_pending_operation = request('/draft-operations', {})['operation_id']
    python(f"with database() as conn:\n conn.execute('UPDATE draft_operations SET normalize_physical_bus=false WHERE id=%s', ({legacy_pending_operation!r},))\n")
    legacy_pending_body = {'operation_id': legacy_pending_operation, 'expected_revision': 0, 'draft': {**planned, 'physical_bus': '\u0085'}}
    legacy_review = request('/workday-reviews', {'draft_id': legacy_draft['id'], 'expected_revision': 1})
    legacy_review_source = request('/drafts', {'operation_id': request('/draft-operations', {})['operation_id'], 'expected_revision': 0, 'draft': {**planned, 'physical_bus': '\u001c'}})
    legacy_pending_review = request('/workday-reviews', {'draft_id': legacy_review_source['id'], 'expected_revision': 1})
    python(f"with database() as conn:\n conn.execute('UPDATE workday_operations SET assessment_policy_version=1 WHERE id=ANY(%s::uuid[])', ({[legacy_review['operation_id'], legacy_pending_review['operation_id']]!r},))\n")
    legacy_review['unknowns'] = json.loads(python(f"from app.draft_domain import DraftContent\nfrom app.workday_domain import assessment\nimport json\nprint(json.dumps(assessment(DraftContent.model_validate({legacy_draft['draft']!r}), policy_version=1)['unknowns']))\n"))
    legacy_pending_review['unknowns'] = json.loads(python(f"from app.draft_domain import DraftContent\nfrom app.workday_domain import assessment\nimport json\nprint(json.dumps(assessment(DraftContent.model_validate({legacy_review_source['draft']!r}), policy_version=1)['unknowns']))\n"))
    legacy_confirmation = {'operation_id': legacy_review['operation_id'], 'expected_revision': 1, 'acknowledgements': [item['id'] for item in legacy_review['unknowns']], 'classifications': {key: 'manual' for key in legacy_review['classifications_required']}}
    legacy_plan = request('/drafts/' + legacy_draft['id'] + '/confirm', legacy_confirmation)
    legacy_lifecycle_path = '/workdays/' + legacy_plan['id'] + '/lifecycle'
    legacy_lifecycle = request(legacy_lifecycle_path)
    assert legacy_lifecycle['state'] == 'confirmed' and legacy_lifecycle['revision'] == 0 and legacy_lifecycle['started_at'] is None
    # Keep both accepted and not-yet-accepted v2 reviews across the same restart.
    v2_cases = []
    for accepted in [True, False]:
        source = request('/drafts', {'operation_id': request('/draft-operations', {})['operation_id'], 'expected_revision': 0, 'draft': planned})
        issued = request('/workday-reviews', {'draft_id': source['id'], 'expected_revision': 1})
        python(f"with database() as conn:\n conn.execute('UPDATE workday_operations SET assessment_policy_version=2 WHERE id=%s', ({issued['operation_id']!r},))\n")
        unknowns = json.loads(python(f"from app.draft_domain import DraftContent\nfrom app.workday_domain import assessment\nimport json\nprint(json.dumps(assessment(DraftContent.model_validate({source['draft']!r}), policy_version=2)['unknowns']))\n"))
        decision = {'operation_id': issued['operation_id'], 'expected_revision': 1, 'acknowledgements': [item['id'] for item in unknowns], 'classifications': {key: 'manual' for key in issued['classifications_required']}}
        result = request('/drafts/' + source['id'] + '/confirm', decision) if accepted else None
        v2_cases.append((source, decision, result, unknowns))
    state_program = state_program.replace("'plans':", "'drafts':conn.execute('SELECT * FROM drafts WHERE owner=%s ORDER BY id', (" + repr(session['account_id']) + ",)).fetchall(), 'draft_operations':conn.execute('SELECT * FROM draft_operations WHERE owner=%s AND expires_at > clock_timestamp() ORDER BY id', (" + repr(session['account_id']) + ",)).fetchall(), 'plans':")
    persisted_confirmation_state = python(state_program)
    persisted_draft_list = listed_drafts()
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
    assert request(selection_path) == selection_receipt['result']
    assert request(selection_path, selection_body) == selection_receipt
    assert request('/workday-selection-operations/' + selection_body['operation_id']) == selection_receipt
    assert request(lifecycle_path) == start_receipt['result']
    assert request(start_path, start_body) == start_receipt
    assert request('/workday-start-operations/' + start_body['operation_id']) == start_receipt
    assert request(notice_path + '/' + notice_id) == notice_ended_receipt['result']
    assert request(notice_path, notice_body) == notice_receipt
    assert request(notice_path + '/' + notice_id + '/check', notice_check) == notice_checked_receipt
    assert request(notice_path + '/' + notice_id + '/end', notice_ending) == notice_ended_receipt
    for payload, expected in [(notice_body, notice_receipt), (notice_check, notice_checked_receipt), (notice_ending, notice_ended_receipt)]:
        assert request('/workday-notice-operations/' + payload['operation_id']) == expected
    assert request(notice_path) == terminal_notices
    assert request(notice_path, terminal_notice_body) == terminal_notice_receipt
    assert request('/workday-notice-operations/' + terminal_notice_body['operation_id']) == terminal_notice_receipt
    assert request(legacy_lifecycle_path) == legacy_lifecycle
    assert request(terminal_base + '/recap') == terminal_snapshot
    assert request(terminal_base + '/close', close_body) == close_receipt
    assert request('/workday-close-operations/' + close_body['operation_id']) == close_receipt
    assert request(terminal_base + '/outcome', outcome_body) == outcome_receipt
    assert request('/workday-outcome-operations/' + outcome_body['operation_id']) == outcome_receipt
    assert request(terminal_base + '/start', terminal_start_body) == terminal_start
    assert request('/workday-operations/' + terminal_decisions['operation_id'])['result'] == terminal_snapshot['plan']
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
    for source, decision, result, unknowns in v2_cases:
        if result is None:
            assert request('/workday-operations/' + decision['operation_id']) == {'state': 'pending', 'result': None}
            result = request('/drafts/' + source['id'] + '/confirm', decision)
            assert result['unknowns'] == unknowns and result['draft'] == source['draft']
        assert request('/drafts/' + source['id'] + '/confirm', decision) == result
        assert request('/workday-operations/' + decision['operation_id']) == {'state': 'accepted', 'result': result}
        assert request('/workdays/' + result['id']) == result
    assert request('/drafts', legacy_body) == legacy_draft
    assert request('/drafts/' + legacy_draft['id'] + '/confirm', legacy_confirmation) == legacy_plan
    assert request('/workday-operations/' + legacy_pending_review['operation_id']) == {'state': 'pending', 'result': None}
    legacy_pending_result = request('/drafts', legacy_pending_body)
    assert legacy_pending_result['draft']['physical_bus'] == '\u0085'
    legacy_pending_confirmation = {'operation_id': legacy_pending_review['operation_id'], 'expected_revision': 1, 'acknowledgements': [item['id'] for item in legacy_pending_review['unknowns']], 'classifications': {key: 'manual' for key in legacy_pending_review['classifications_required']}}
    legacy_pending_plan = request('/drafts/' + legacy_review_source['id'] + '/confirm', legacy_pending_confirmation)
    assert legacy_pending_plan['draft']['physical_bus'] == '\u001c'
    assert set(legacy_pending_plan['acknowledgements']) == set(legacy_pending_confirmation['acknowledgements'])
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
