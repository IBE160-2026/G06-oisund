"""Only the named story122 project is mutated. Never calls existing orchestrators.

Actual notice creation/retry/lost-response checks are PENDING stable 12.1 admission.
No credentials or private data are written to evidence. Synthetic fixed fixture only.
"""
from __future__ import annotations
import hashlib
import json
import secrets
import socket
import subprocess
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'ibe160-story122-tests'
COMPOSE = ['docker', 'compose', '-p', PROJECT, '-f', str(ROOT / 'compose.story122.yaml')]
RUN = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + secrets.token_hex(6)
EVIDENCE = ROOT / 'docs' / 'evidence' / f'12-2-real-{RUN}.json'
record: dict = {'run': RUN, 'scope': PROJECT, 'commands': [], 'checks': [], 'pending': ['Actual notice creation/retry/lost-response API verification awaits stable 12.1 admission contract.']}

def command(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True)
    record['commands'].append({'command': args, 'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    if result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}): {args[:5]}')
    return result.stdout

def check(name: str, condition: bool) -> None:
    record['checks'].append({'name': name, 'passed': bool(condition)})
    if not condition:
        raise AssertionError(name)

def request(path: str, body=None, port=18222):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(f'http://127.0.0.1:{port}{path}', data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, None

def ready(port):
    for _ in range(60):
        try:
            if request('/health', port=port)[0] == 200:
                return
        except (OSError, urllib.error.URLError):
            pass
        time.sleep(1)
    raise RuntimeError(f'Isolated API {port} never became ready')

try:
    record['baseline'] = command(['git', 'rev-parse', 'HEAD']).strip()
    build_inputs = [p for p in (ROOT / 'backend').rglob('*') if p.is_file() and not any(part in {'.venv', '__pycache__', '.pytest_cache', '.git'} for part in p.parts)]
    build_inputs += [ROOT / 'compose.story122.yaml', Path(__file__)]
    record['source_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(build_inputs)}
    # Refuse to attach to a running project; only this script's new project may be restarted.
    existing = command(['docker', 'ps', '-aq', '--filter', f'label=com.docker.compose.project={PROJECT}']).strip()
    check('isolated project absent before run', not existing)
    volumes = command(['docker', 'volume', 'ls', '-q', '--filter', f'label=com.docker.compose.project={PROJECT}']).strip()
    check('unexpected retained project volumes absent before run', not volumes)
    for port in (18222, 18223):
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', port))
    secret = ROOT / '.private-runtime' / 'story122-postgres-password'
    secret.parent.mkdir(exist_ok=True)
    if not secret.exists():
        secret.write_text(secrets.token_urlsafe(40), encoding='utf-8')
    command(COMPOSE + ['up', '-d', '--build'])
    ready(18222); ready(18223)
    command(COMPOSE + ['exec', '-T', 'api', 'python', '-m', 'pytest', '-q', 'tests/test_assessment.py'])
    command(COMPOSE + ['exec', '-T', 'private-api', 'python', '-c', "from app.auth import provision; import secrets; provision('synthetic-story122-sentinel', secrets.token_urlsafe(40))"])
    command(COMPOSE + ['exec', '-T', 'private-db', 'psql', '-U', 'private_work', '-d', 'private_work', '-c', "CREATE TABLE story122_sentinel (value text NOT NULL); INSERT INTO story122_sentinel VALUES ('synthetic-keep-before-and-after-fictional-reset')"])
    fingerprint_sql = "SELECT count(*), md5(string_agg(row_to_json(a)::text, '' ORDER BY a.id)) FROM accounts a; SELECT count(*), md5(string_agg(value, '' ORDER BY value)) FROM story122_sentinel"
    private_before = command(COMPOSE + ['exec', '-T', 'private-db', 'psql', '-U', 'private_work', '-d', 'private_work', '-Atc', fingerprint_sql]).strip()
    check('populated private synthetic sentinel exists', len(private_before.splitlines()) == 2 and all(row.startswith('1|') for row in private_before.splitlines()))
    fixture = request('/fixture')[1]
    operation = request('/operations', {})[1]['operation_id']
    payload = {'operation_id': operation, 'day': fixture}
    status, saved = request('/days', payload)
    check('actual fixed fixture saved', status == 200 and saved['day'] == fixture)
    check('actual exact replay preserves original receipt', request('/days', payload) == (200, saved))
    changed = json.loads(json.dumps(payload)); changed['day']['vehicle_duty'] = 'synthetic-conflict'
    check('changed replay rejected without overwrite', request('/days', changed)[0] == 409)
    check('read original snapshot after conflict', request('/days/' + saved['id']) == (200, saved))
    # Explicitly lose a response at the caller, then replay SAME operation, never issue a second one.
    lost_op = request('/operations', {})[1]['operation_id']
    lost_payload = {'operation_id': lost_op, 'day': fixture}
    accepted = request('/days', lost_payload)[1]
    check('fictional API lost caller acknowledgement recovered by same replay', request('/days', lost_payload) == (200, accepted))
    command(COMPOSE + ['restart', 'api', 'db'])
    ready(18222)
    check('PostgreSQL snapshot survives own API/database restart', request('/days/' + saved['id']) == (200, saved))
    for path in ('/workdays', '/drafts', '/notices'):
        check(f'private unauthenticated denial {path}', request(path, port=18223)[0] == 401)
    command(COMPOSE + ['exec', '-T', 'api', 'python', '-m', 'app.manage', 'reset', '--fictional-only'])
    check('guarded reset removes first isolated receipt', request('/days/' + saved['id'])[0] == 410)
    check('guarded reset removes second isolated receipt', request('/days/' + accepted['id'])[0] == 410)
    count = command(COMPOSE + ['exec', '-T', 'db', 'psql', '-U', 'fictional', '-d', 'fictional_assessment', '-Atc', 'SELECT count(*) FROM fictional_days']).strip()
    check('guarded reset reseeds exactly one fictional day', count == '1')
    private_after = command(COMPOSE + ['exec', '-T', 'private-db', 'psql', '-U', 'private_work', '-d', 'private_work', '-Atc', fingerprint_sql]).strip()
    check('fictional reset preserves populated private account and sentinel fingerprints', private_before == private_after)
    record['result'] = 'passed-independent-checks; notice integration pending'
finally:
    EVIDENCE.parent.mkdir(exist_ok=True)
    EVIDENCE.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Evidence: {EVIDENCE}')
    print('Own containers retained for inspection. To remove ONLY this project: docker compose -p ibe160-story122-tests -f compose.story122.yaml down -v')
