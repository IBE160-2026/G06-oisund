"""Fresh, synthetic-only Story 12.1/12.2 actual HTTP/PostgreSQL evidence.

Usage: python scripts/verify-story12-integration.py up|verify|prepare
Root owns execution, browser serving at 15312 and all broader test gates.
No stop/down, ordinary Compose overrides, credential logging or implicit acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import http.cookiejar
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from uuid import UUID, uuid4

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'ibe160-story12-integration'
CONFIG = ROOT / 'compose.story12-integration.yaml'
COMPOSE = ['docker', 'compose', '-p', PROJECT, '-f', str(CONFIG)]
ORIGIN = 'http://127.0.0.1:15312'
SECRET = ROOT / '.private-runtime/story12-integration-postgres-password'
CREDENTIALS = ROOT / '.private-runtime/story12-manual-credentials.json'
RUN = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + secrets.token_hex(6)
EVIDENCE = ROOT / f'docs/evidence/12-integration-real-{RUN}.json'
ACCEPTANCE = 'Jonas har ikke gjennomført manuell/fysisk akseptansetest av Story 12.1 eller Story 12.2. Teknisk integrasjon og automatiske tester innebærer ikke brukeraksept. Begge avventer Jonas sin testing.'
record = {'run': RUN, 'project': PROJECT, 'owner_acceptance': 'pending',
          'acceptance_note': ACCEPTANCE, 'commands': [], 'checks': [], 'result': 'running'}
BOOTSTRAP = "import os; from pathlib import Path; from urllib.parse import quote; os.environ['DATABASE_URL']='postgresql://fictional:'+quote(Path('/run/secrets/integration_password').read_text().strip(),safe='')+'@db/fictional_assessment'\n"


def command(args, program=None, sensitive=False):
    timeout = 600 if '--build' in args else 120
    try:
        result = subprocess.run(args, cwd=ROOT, input=program, capture_output=True,
                                text=True, encoding='utf-8', errors='replace', timeout=timeout)
    except subprocess.TimeoutExpired:
        record['commands'].append({'command': args, 'status': 'timeout',
                                   'timeout_seconds': timeout, 'exit_code': None})
        raise RuntimeError('Subprocess timed out; see evidence') from None
    except OSError as error:
        record['commands'].append({'command': args, 'status': 'launch-failed',
                                   'failure_type': type(error).__name__, 'exit_code': None})
        raise RuntimeError('Subprocess launch failed; see evidence') from None
    entry = {'command': args, 'exit_code': result.returncode}
    entry['status'] = 'passed' if result.returncode == 0 else 'failed'
    # stdin can contain synthetic credentials. It is never captured in evidence.
    if sensitive:
        entry['output'] = 'suppressed: credential-bearing operation'
    else:
        entry.update(stdout=result.stdout, stderr=result.stderr)
    record['commands'].append(entry)
    if result.returncode:
        raise RuntimeError('Subprocess failed; see evidence command exit code')
    return result.stdout.strip()


def check(name, condition):
    record['checks'].append({'name': name, 'status': 'passed' if condition else 'failed'})
    if not condition:
        raise AssertionError(name)


def manifest():
    files = []
    for directory in ['backend', 'frontend/src', 'frontend/tests', 'Eksempelfiler']:
        files.extend(p for p in (ROOT / directory).rglob('*') if p.is_file()
                     and not any(s in p.parts for s in ['__pycache__', '.venv', '.pytest_cache']))
    files.extend(p for p in (ROOT / 'frontend').iterdir() if p.is_file())
    files += [CONFIG, Path(__file__)]
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(set(files))}


def normalized(path):
    return os.path.normcase(str(Path(path).resolve())).replace('\\', '/').casefold()


def guard_runtime(required=True):
    ids = command(['docker', 'ps', '-aq', '--filter', f'label=com.docker.compose.project={PROJECT}']).split()
    if required:
        check('integration runtime exists', bool(ids))
    expected = {'api', 'db', 'private-api', 'private-db'}
    found = set()
    for identifier in ids:
        data = json.loads(command(['docker', 'inspect', identifier]))[0]
        labels = data['Config']['Labels']
        found.add(labels.get('com.docker.compose.service'))
        check('container belongs to exact project/config/workspace',
              labels.get('com.docker.compose.project') == PROJECT
              and normalized(labels.get('com.docker.compose.project.config_files', '')) == normalized(CONFIG)
              and normalized(labels.get('com.docker.compose.project.working_dir', '')) == normalized(ROOT)
              and labels.get('com.docker.compose.service') in expected)
        for mount in data.get('Mounts', []):
            if mount['Type'] == 'volume':
                volume = json.loads(command(['docker', 'volume', 'inspect', mount['Name']]))[0]
                check('attached volume belongs to integration project',
                      (volume.get('Labels') or {}).get('com.docker.compose.project') == PROJECT)
    if required:
        check('all four expected integration services present', found == expected)
        private_python('')
    return bool(ids)


def private_python(program, sensitive=False):
    guard = 'from app.auth import require_synthetic_accounts\nfrom app.private_storage import database\nwith database() as conn:\n require_synthetic_accounts(conn)\n'
    return command(COMPOSE + ['exec', '-T', 'private-api', 'python', '-'], guard + program, sensitive)


def sql(statement, private=True):
    if private:
        # Recheck synthetic accounts in the very transaction performing a mutation.
        return private_python('import json\nwith database() as conn:\n require_synthetic_accounts(conn)\n rows=conn.execute(' + repr(statement) + ').fetchall()\n print(json.dumps(rows,default=str,sort_keys=True))\n')
    return command(COMPOSE + ['exec', '-T', 'db', 'psql', '-U', 'fictional', '-d', 'fictional_assessment', '-Atc', statement])


class Client:
    def __init__(self, port):
        self.port = port
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

    def headers(self):
        return {'Origin': ORIGIN, 'Content-Type': 'application/json',
                'X-CSRF-Token': self.call('/auth/csrf')[1]['csrf_token']}

    def call(self, path, body=None):
        headers = self.headers() if body is not None and self.port == 18313 else {'Content-Type': 'application/json'}
        req = urllib.request.Request(f'http://127.0.0.1:{self.port}' + path,
                                     data=None if body is None else json.dumps(body).encode(), headers=headers)
        try:
            with self.opener.open(req, timeout=20) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            return error.code, None

    def ok(self, path, body=None):
        status, result = self.call(path, body)
        check('HTTP success ' + path, status == 200)
        return result

    def lose_response(self, path, body):
        headers = self.headers()
        req = urllib.request.Request(f'http://127.0.0.1:{self.port}' + path)
        self.jar.add_cookie_header(req)
        headers['Cookie'] = req.get_header('Cookie', '')
        raw = json.dumps(body).encode()
        headers.update(Host=f'127.0.0.1:{self.port}', **{'Content-Length': str(len(raw)), 'Connection': 'close'})
        wire = ('POST ' + path + ' HTTP/1.1\r\n' + ''.join(f'{k}: {v}\r\n' for k, v in headers.items()) + '\r\n').encode() + raw
        with socket.create_connection(('127.0.0.1', self.port), timeout=20) as transport:
            transport.sendall(wire)
            # Keep the request connection alive until independent authorized
            # lookup proves commit. Closing before dispatch can correctly cancel
            # a request; that is not a lost *accepted* acknowledgement.
            for _ in range(100):
                status, receipt = self.call('/workday-notice-operations/'+body['operation_id'])
                if status == 200:
                    check('notice committed before acknowledgement connection discarded', receipt['operation_id'] == body['operation_id'])
                    break
                check('pre-commit receipt lookup remains unknown', status == 404)
                time.sleep(.1)
            else:
                raise AssertionError('Notice did not commit while acknowledgement was withheld')
            # Intentionally no recv/read: acknowledgement is lost at transport boundary.
        record['checks'].append({'name': 'real notice POST sent; socket closed without reading response', 'status': 'passed'})


def ready(port):
    for _ in range(90):
        try:
            if Client(port).call('/health')[0] == 200:
                return
        except (OSError, urllib.error.URLError):
            pass
        time.sleep(1)
    raise RuntimeError(f'Integration API {port} not ready')


def provision(username, password):
    if not username.startswith('synthetic-'):
        raise ValueError('Synthetic username required')
    return private_python('from app.auth import provision\nprint(provision(' + repr(username) + ',' + repr(password) + '))\n', sensitive=True)


def create_day(client, day):
    facts = {'service_date': day, 'vehicle_duty': '0020', 'physical_bus': None,
             'activities': [{'id': str(uuid4()), 'type': 'trip', 'line': '20',
                             'start': day+'T10:00+01:00', 'end': day+'T11:00+01:00',
                             'raw_code': 'Synthetic line 20', 'from_place': None, 'to_place': None}]}
    draft = client.ok('/drafts', {'operation_id': client.ok('/draft-operations', {})['operation_id'],
                                 'expected_revision': 0, 'draft': facts})
    reviewed = client.ok('/workday-reviews', {'draft_id': draft['id'], 'expected_revision': draft['revision']})
    decision = {'operation_id': reviewed['operation_id'], 'expected_revision': draft['revision'],
                'acknowledgements': [v['id'] for v in reviewed['unknowns']
                                     if v['id'].split(':')[0] not in reviewed['classifications_required']],
                'classifications': {key: 'manual' for key in reviewed['classifications_required']}}
    return client.ok('/drafts/'+draft['id']+'/confirm', decision)


def up():
    existing = guard_runtime(required=False)
    # Check known volume names before startup/migrations can touch their contents.
    names = command(['docker', 'volume', 'ls', '--format', '{{.Name}}']).splitlines()
    for suffix in ('integration_fictional', 'integration_private'):
        name = PROJECT + '_' + suffix
        if name in names:
            volume = json.loads(command(['docker', 'volume', 'inspect', name]))[0]
            labels = volume.get('Labels') or {}
            check('preexisting named volume belongs to exact integration runtime', existing
                  and labels.get('com.docker.compose.project') == PROJECT
                  and labels.get('com.docker.compose.volume') == suffix)
    if existing:
        # Refuse incomplete or non-synthetic attached runtimes before any rebuild.
        guard_runtime()
    if not existing:
        for port in (18312, 18313):
            with socket.socket() as probe:
                probe.bind(('127.0.0.1', port))
        volumes = command(['docker', 'volume', 'ls', '-q', '--filter', f'label=com.docker.compose.project={PROJECT}'])
        check('no unattached previous integration volumes', not volumes)
    check('password destination is git ignored', bool(command(['git', 'check-ignore', str(SECRET)])))
    SECRET.parent.mkdir(exist_ok=True)
    if not SECRET.exists():
        check('no missing password for an existing runtime', not existing)
        SECRET.write_text(secrets.token_urlsafe(40), encoding='utf-8')
    command(COMPOSE + ['up', '-d', '--build'])
    ready(18312)
    ready(18313)
    guard_runtime()


def verify():
    owned_names = []
    try:
        _verify(owned_names)
    finally:
        failed = sys.exc_info()[0] is not None
        if owned_names:
            try:
                cleanup_accounts(owned_names)
                record['cleanup'] = {'status': 'passed', 'account_count': len(owned_names)}
            except Exception as error:
                record['cleanup'] = {'status': 'failed', 'failure_type': type(error).__name__}
                if not failed:
                    raise


def cleanup_accounts(names):
    if not all(name.startswith('synthetic-story12-verify-') or name.startswith('synthetic-story12-foreign-') for name in names):
        raise ValueError('Cleanup requires invocation-owned verification usernames')
    private_python("names="+repr(names)+"\nwith database() as conn:\n require_synthetic_accounts(conn)\n owners=[row['id'] for row in conn.execute('SELECT id FROM accounts WHERE username=ANY(%s)',(names,)).fetchall()]\n for table in ['workday_deletions','workday_operations','workdays','draft_deletions','draft_operations','drafts','sessions','accounts']:\n  key='id' if table=='accounts' else 'owner'\n  conn.execute('DELETE FROM '+table+' WHERE '+key+'=ANY(%s::uuid[])',(owners,))\n")


PRIVATE_TABLES = ['accounts', 'sessions', 'security_settings', 'login_limits', 'drafts', 'draft_operations', 'draft_deletions',
                  'workdays', 'workday_operations', 'workday_deletions', 'workday_buses',
                  'workday_bus_operations', 'workday_selections', 'workday_selection_operations',
                  'workday_lifecycles', 'workday_start_operations', 'workday_outcome_revisions',
                  'workday_outcomes', 'workday_outcome_operations', 'workday_close_operations',
                  'workday_notices', 'workday_notice_operations', 'account_notice_operations',
                  'notice_creation_admissions']


def private_fingerprint():
    # Hash complete rows inside PostgreSQL: no password/session hashes or payloads
    # leave the guarded container. Include empty tables and every receipt family.
    statement = ' UNION ALL '.join(
        "SELECT '"+table+"' AS table_name,count(*) AS rows,md5(COALESCE(string_agg(row_to_json(t)::text,'' ORDER BY row_to_json(t)::text),'')) AS hash FROM "+table+' t'
        for table in PRIVATE_TABLES) + ' ORDER BY table_name'
    return sql(statement)


def _verify(owned_names):
    guard_runtime()
    ready(18312)
    ready(18313)
    username = 'synthetic-story12-verify-' + uuid4().hex
    password = secrets.token_urlsafe(32)
    owned_names.append(username)
    owner = str(UUID(provision(username, password)))
    client = Client(18313)
    client.ok('/auth/login', {'username': username, 'password': password})
    a = create_day(client, '2031-01-02')
    b = create_day(client, '2031-01-03')
    content = {'title': 'Synthetic independent notice', 'summary': 'Unknown source time',
               'description': 'Synthetic integration only', 'source_note': 'SMS',
               'line_tags': ['20'], 'valid_until': '2031-01-04'}
    original = {'operation_id': client.ok('/notice-operations', {})['operation_id'],
                'expected_revision': 0, 'content': content}
    receipt = client.ok('/notices', original)
    notice = receipt['result']
    check('original notice identity and unknown facts', receipt['operation_id'] == original['operation_id']
          and notice['valid_from'] is None and notice['source_updated_at'] is None
          and notice['checked_at'] is None and notice['workday_id'] is None)
    check('exact notice replay immutable', client.ok('/notices', original) == receipt)
    altered = {**original, 'content': {**content, 'title': 'Changed replay'}}
    check('altered notice replay denied', client.call('/notices', altered)[0] == 409)
    check('authorized receipt lookup immutable', client.ok('/workday-notice-operations/'+original['operation_id']) == receipt)
    foreign = Client(18313)
    foreign_name = 'synthetic-story12-foreign-'+uuid4().hex
    owned_names.append(foreign_name)
    foreign_owner = str(UUID(provision(foreign_name, password)))
    foreign.ok('/auth/login', {'username': foreign_name, 'password': password})
    check('foreign receipt denied', foreign.call('/workday-notice-operations/'+original['operation_id'])[0] == 404)
    check('foreign admission denied', foreign.call('/notices', original)[0] == 404)
    unknown = {**original, 'operation_id': str(uuid4())}
    check('unknown admission denied', client.call('/notices', unknown)[0] == 404)
    expired = {**original, 'operation_id': client.ok('/notice-operations', {})['operation_id']}
    sql("UPDATE notice_creation_admissions SET expires_at=clock_timestamp()-interval '1 second' WHERE id='"+str(UUID(expired['operation_id']))+"' RETURNING id")
    check('expired admission denied', client.call('/notices', expired)[0] == 410)
    lost = {**original, 'operation_id': client.ok('/notice-operations', {})['operation_id'],
            'content': {**content, 'title': 'Synthetic lost acknowledgement'}}
    client.lose_response('/notices', lost)
    recovered = None
    for _ in range(100):
        status, value = client.call('/workday-notice-operations/'+lost['operation_id'])
        if status == 200:
            recovered = value
            break
        check('unresolved receipt lookup remains unavailable', status == 404)
        time.sleep(.1)
    check('lookup recovers lost response with original operation', recovered is not None and recovered['operation_id'] == lost['operation_id'])
    check('same-ID replay after lookup immutable', client.ok('/notices', lost) == recovered)
    rows = json.loads(sql("SELECT (SELECT count(*) FROM workday_notices WHERE owner='"+owner+"') AS notices, (SELECT count(*) FROM account_notice_operations WHERE owner='"+owner+"') AS receipts"))
    check('two original operations create exactly two notices and receipts', rows == [{'notices': 2, 'receipts': 2}])
    client.ok('/workdays/'+a['id']+'/delete', {'operation_id': str(uuid4()), 'source_revision': a['source_revision']})
    check('deleted original day preserves independent notice', client.ok('/notices/'+notice['id']) == notice)
    check('remaining day reader sees original incident', notice['id'] in [v['notice']['id'] for v in client.ok('/workdays/'+b['id']+'/notice-reader')['candidates']])
    fictional = Client(18312)
    fixture = fictional.ok('/fixture')
    body = {'operation_id': fictional.ok('/operations', {})['operation_id'], 'day': fixture}
    saved = fictional.ok('/days', body)
    check('actual fictional fixture persisted', saved['day'] == fixture)
    check('actual fictional replay preserves receipt', fictional.ok('/days', body) == saved)
    changed = {**body, 'day': {**fixture, 'vehicle_duty': 'synthetic-conflict'}}
    check('fictional altered replay denied', fictional.call('/days', changed)[0] == 409)
    guard_runtime()
    command(COMPOSE + ['restart', 'db', 'private-db'])
    command(COMPOSE + ['up', '-d', '--wait', 'db', 'private-db'])
    command(COMPOSE + ['restart', 'api', 'private-api'])
    ready(18312)
    ready(18313)
    check('fictional snapshot survives restart', fictional.ok('/days/'+saved['id']) == saved)
    check('private original receipt survives restart', client.ok('/workday-notice-operations/'+lost['operation_id']) == recovered)
    before = private_fingerprint()
    command(COMPOSE + ['exec', '-T', 'api', 'python', '-'], BOOTSTRAP + "import runpy,sys\nsys.argv=['app.manage','reset','--fictional-only']\nrunpy.run_module('app.manage',run_name='__main__')\n")
    check('fictional reset removes saved receipt', fictional.call('/days/'+saved['id'])[0] == 410)
    check('fictional reset reseeds exactly one day', sql('SELECT count(*) FROM fictional_days', private=False) == '1')
    check('fictional reset preserves all private rows and receipts', private_fingerprint() == before)
    check('fictional reset preserves notice and lost receipt', client.ok('/notices/'+notice['id']) == notice
          and client.ok('/workday-notice-operations/'+lost['operation_id']) == recovered)
    # Force one synthetic retention boundary; the other notice remains independent.
    sql("UPDATE workday_notices SET expires_at=clock_timestamp()-interval '1 second' WHERE id='"+str(UUID(recovered['result']['id']))+"' RETURNING id")
    check('expired retained notice inaccessible', client.call('/notices/'+recovered['result']['id'])[0] == 410)
    private_python('from app.private_storage import cleanup\ncleanup()\n')
    check('purged accepted operation cannot resurrect', client.call('/notices', lost)[0] in (404, 410))
    check('live independent notice survives other purge', client.ok('/notices/'+notice['id']) == notice)


def prepare():
    guard_runtime()
    check('manual credentials destination is git ignored', bool(command(['git', 'check-ignore', str(CREDENTIALS)])))
    if CREDENTIALS.exists():
        credentials = json.loads(CREDENTIALS.read_text(encoding='utf-8'))
        check('existing manual credentials target exact synthetic runtime',
              credentials.get('username') == 'synthetic-story12-manual'
              and credentials.get('project') == PROJECT and credentials.get('origin') == ORIGIN)
    else:
        credentials = {'username': 'synthetic-story12-manual', 'password': secrets.token_urlsafe(32),
                       'project': PROJECT, 'origin': ORIGIN, 'private_api': 'http://127.0.0.1:18313'}
        # Durable recoverable secret precedes provisioning; never reset passwords.
        CREDENTIALS.parent.mkdir(exist_ok=True)
        with CREDENTIALS.open('x', encoding='utf-8') as handle:
            handle.write(json.dumps(credentials, indent=2))
            handle.flush()
            os.fsync(handle.fileno())
    present = json.loads(private_python("import json\nwith database() as conn:\n require_synthetic_accounts(conn)\n print(json.dumps(conn.execute('SELECT 1 FROM accounts WHERE username=%s',("+repr(credentials['username'])+",)).fetchone() is not None))\n"))
    if not present:
        provision(credentials['username'], credentials['password'])
    client = Client(18313)
    client.ok('/auth/login', {k: credentials[k] for k in ['username', 'password']})
    listing = client.ok('/workdays')
    check('manual fixture listing complete', listing['next_cursor'] is None)
    plans = [client.ok('/workdays/'+v['id']) for v in listing['workdays']]
    dates = [v['draft']['service_date'] for v in plans]
    requested = {'2031-01-02', '2031-01-03'}
    check('existing manual fixtures have unique requested dates and line20',
          len(dates) == len(set(dates)) and set(dates) <= requested
          and all(v['draft']['activities'] and all(a['line'] == '20' for a in v['draft']['activities']) for v in plans))
    for day in sorted(requested - set(dates)):
        create_day(client, day)
    record['manual_credentials'] = '.private-runtime/story12-manual-credentials.json (ignored; values omitted)'


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('mode', choices=['up', 'verify', 'prepare'])
    mode = args.parse_args().mode
    record['mode'] = mode
    before = manifest()
    record['source_sha256_before'] = before
    try:
        record['baseline'] = command(['git', 'rev-parse', 'HEAD'])
        {'up': up, 'verify': verify, 'prepare': prepare}[mode]()
        check('source inputs unchanged during invocation', manifest() == before)
        record['result'] = 'passed'
        record['exit_code'] = 0
    except Exception as error:
        record['result'] = 'failed'
        record['exit_code'] = 1
        # Exception text from auth/HTTP tooling can include secrets; record type only.
        record['failure_type'] = type(error).__name__
        raise
    finally:
        record['source_sha256_after'] = manifest()
        EVIDENCE.parent.mkdir(exist_ok=True)
        EVIDENCE.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'Evidence: {EVIDENCE}')
        print('Integration containers retained; owner acceptance pending.')


if __name__ == '__main__':
    main()
