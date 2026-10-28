"""Read-only identity/isolation audit of an already running synthetic12.4 stack."""
import hashlib
import importlib.util
import json
import platform
from pathlib import Path
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


def command(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding='utf-8').strip()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main(record):
    record['phase'] = 'runtime guard'
    spec = importlib.util.spec_from_file_location('adapter', ROOT/'scripts/verify-story124.py')
    adapter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adapter)
    adapter.load_guard()['guard_runtime']()
    record['phase'] = 'revision identity'
    record['revision'] = command('git', 'rev-parse', 'HEAD')

    def check(name, passed):
        record['checks'].append({'name': name, 'passed': bool(passed)})

    compose = ['docker', 'compose', '-p', record['project'], '-f', 'compose.story124.yaml']
    record['phase'] = 'runtime versions'
    record['versions'] = {
        'host': platform.platform(), 'host_python': platform.python_version(),
        'node': command('node', '--version'),
        'compose': command('docker', 'compose', 'version', '--short'),
        'postgresql': command(*compose, 'exec', '-T', 'private-db', 'postgres', '--version'),
        'api': json.loads(command(*compose, 'exec', '-T', 'private-api', 'python', '-c',
            'import sys,json,importlib.metadata as m; print(json.dumps({"python":sys.version,"packages":{name:m.version(name) for name in ["fastapi","psycopg","pdfplumber","uvicorn"]}}))')),
    }
    record['phase'] = 'backend source identity'
    paths = [p.relative_to(ROOT/'backend').as_posix() for p in (ROOT/'backend').rglob('*')
             if p.is_file() and not any(part in ('__pycache__', '.pytest_cache') for part in p.parts)]
    host = {name: sha((ROOT/'backend'/name).read_bytes()) for name in paths}
    program = 'import hashlib,json,pathlib; names=' + repr(paths) + '; print(json.dumps({name:hashlib.sha256(pathlib.Path("/app",name).read_bytes()).hexdigest() for name in names}))'
    record['backend_sha256'] = host
    record['api_containers'] = {}
    latest_write = max((ROOT/'backend'/name).stat().st_mtime for name in paths)
    for service in ('api', 'private-api'):
        record['phase'] = service + ' container identity'
        actual = json.loads(command(*compose, 'exec', '-T', service, 'python', '-c', program))
        identifier = command(*compose, 'ps', '-q', service)
        data = json.loads(command('docker', 'inspect', identifier))[0]
        started = datetime.fromisoformat(data['State']['StartedAt'].replace('Z', '+00:00')).timestamp()
        record['api_containers'][service] = {'id': data['Id'], 'image': data['Image'], 'started_at': data['State']['StartedAt']}
        check(service + ' mounted source equals host', actual == host)
        check(service + ' started after final source writes', started >= latest_write)
    record['phase'] = 'frontend build identity'
    identity = json.loads((ROOT/'.private-runtime/story124-build.json').read_text(encoding='utf-8'))
    source = {name: sha((ROOT/name).read_bytes()) for name in identity['source']}
    check('frontend build source equals current source', source == identity['source'])
    record['frontend_source_sha256'] = source
    check('exact API build settings', identity['effective_api_settings'] == {
        'VITE_PRIVATE_API_BASE': None, 'VITE_PRIVATE_API': 'http://127.0.0.1:18326', 'VITE_FICTIONAL_API': 'http://127.0.0.1:18325'})
    record['effective_api_settings'] = identity['effective_api_settings']
    record['served_sha256'] = {}
    for name, expected in identity['built'].items():
        record['phase'] = 'served build: ' + name
        path = Path(name).relative_to('frontend/dist').as_posix()
        with urllib.request.urlopen('http://127.0.0.1:15324/' + path, timeout=10) as response:
            actual = sha(response.read())
        record['served_sha256'][path] = actual
        check('served bytes equal recorded build: ' + path,
              actual == expected == sha((ROOT/name).read_bytes()))
    for port in (18325, 18326):
        record['phase'] = 'health: ' + str(port)
        with urllib.request.urlopen(f'http://127.0.0.1:{port}/health', timeout=10) as response:
            check(str(port) + ' health', response.status == 200)
        # No credentials or account data are read by this audit.
    record['phase'] = 'unauthorized session boundary'
    try:
        urllib.request.urlopen('http://127.0.0.1:18326/auth/session', timeout=10)
        check('unauthorized private session denied', False)
    except urllib.error.HTTPError as error:
        check('unauthorized private session denied/no-store', error.code == 401 and error.headers.get('Cache-Control') == 'no-store')
    record['phase'] = 'existing container preservation'
    baseline = json.loads((ROOT/'docs/evidence/12-4-baseline.json').read_text(encoding='utf-8'))
    current = [json.loads(line) for line in command('docker', 'ps', '--format', 'json').splitlines()]
    by_name = {row['Names']: row for row in current}
    record['preserved_container_names'] = []
    for before in baseline['containers']:
        after = by_name.get(before['Names'])
        check('existing container preserved: ' + before['Names'], after is not None and all(after[key] == before[key] for key in ('ID', 'Image', 'Ports')))
        record['preserved_container_names'].append(before['Names'])
    record['passed'] = all(item['passed'] for item in record['checks'])
    record['phase'] = 'complete'
    target = ROOT/'docs/evidence'/('12-4-runtime-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
    target.write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(str(target), 'PASS' if record['passed'] else 'FAIL')
    raise SystemExit(0 if record['passed'] else 1)


def run():
    record = {'recorded_at': datetime.now(timezone.utc).isoformat(),
              'project': 'ibe160-story124-tests', 'checks': [], 'phase': 'initialization'}
    try:
        main(record)
    except Exception as error:
        target = ROOT/'docs/evidence'/('12-4-runtime-failed-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
        record.update(passed=False, failure_type=type(error).__name__, message=str(error))
        target.write_text(json.dumps(record, indent=2), encoding='utf-8')
        print(str(target), 'FAIL')
        raise


if __name__ == '__main__':
    run()
