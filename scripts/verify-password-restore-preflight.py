"""Actual restore preflight against a completed synthetic runner's archives.

Usage: python scripts/verify-password-restore-preflight.py ibe160-pm-restore-HEX
       python scripts/verify-password-restore-preflight.py --marker-only
No production project, root entrypoint, systemd, or Docker socket in a container.
On Windows only fcntl import is stubbed; preflight never calls it. The tested
function is unchanged; Compose transport and CONFIG point at synthetic inputs.
"""
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import types
import uuid

root = Path(__file__).resolve().parent.parent
if os.name == 'nt':
    sys.modules['fcntl'] = types.ModuleType('fcntl')
original_path = os.environ['PATH']
spec = importlib.util.spec_from_file_location('restore_ops', root / 'deploy/ubuntu/bussassistentctl.py')
ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ops)
os.environ['PATH'] = original_path


def verify_transaction_marker():
    """Run production marker lookup and restore SQL on an isolated archive."""
    name = 'ibe160-pm-restore-marker-' + uuid.uuid4().hex
    image = next(line.split()[1] for line in (root / 'deploy/ubuntu/Dockerfile.postgres').read_text().splitlines()
                 if line.startswith('FROM postgres:17.'))
    execute = ['docker', 'exec', '-i', name, 'env', 'PGHOST=/tmp']
    sql = ['psql', '-X', '-U', 'tablet_bootstrap', '-d', 'private_work', '-v', 'ON_ERROR_STOP=1']
    original_compose = ops.compose

    def database(args, *, check=True, **kwargs):
        return subprocess.run(execute + args, check=check, capture_output=True, timeout=30, **kwargs)

    def compose(_path, *args, **kwargs):
        if args[:3] != ('exec', '-T', 'private-db') or args[3] not in ('psql', 'pg_restore'):
            raise RuntimeError('Unexpected marker-test transport')
        kwargs.setdefault('timeout', 30)
        return subprocess.run(execute + list(args[3:]), check=True, **kwargs)

    def query(command):
        return database(sql + ['-qAtc', command], text=True).stdout.strip()

    def dump():
        return database(['pg_dump', '-U', 'tablet_bootstrap', '-d', 'private_work',
                         '-Fc', '--no-owner', '--no-acl']).stdout

    def identity():
        return (ops.database_restore_marker(root), query('SELECT last_value FROM public.marker_probe_seq'),
                ops.database_fingerprint(root, capture=True).stdout)

    subprocess.run(['docker', 'run', '-d', '--rm', '--name', name, '--network', 'none',
                    '--read-only', '--user', 'postgres', '--cap-drop', 'ALL',
                    '--security-opt', 'no-new-privileges', '--tmpfs', '/tmp:rw,size=128m,mode=1777',
                    '--entrypoint', 'sh', image, '-ec',
                    'initdb -D /tmp/db -U tablet_bootstrap -A trust --no-sync >/dev/null; '
                    'exec postgres -D /tmp/db -c "listen_addresses=" -k /tmp'],
                   check=True, capture_output=True, timeout=30)
    ops.compose = compose
    try:
        for _ in range(50):
            if database(['pg_isready', '-U', 'tablet_bootstrap', '-d', 'postgres'], check=False).returncode == 0:
                break
            time.sleep(0.2)
        else:
            raise RuntimeError('Disposable marker-test database unavailable')
        database(['psql', '-X', '-U', 'tablet_bootstrap', '-d', 'postgres', '-v', 'ON_ERROR_STOP=1',
                  '-c', 'CREATE ROLE private_work LOGIN', '-c', 'CREATE DATABASE private_work OWNER private_work'])
        query('SET ROLE private_work; CREATE SEQUENCE public.marker_probe_seq START WITH 17; '
              'CREATE TABLE public.marker_probe(value integer); INSERT INTO public.marker_probe VALUES (1)')
        source = dump()
        query('ALTER SEQUENCE public.marker_probe_seq RESTART WITH 7')
        before = identity()
        if before[:2] != ('', '7'):
            raise RuntimeError('Unexpected marker-test initial state')
        operation = uuid.uuid4().hex
        (root / 'tmp').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root / 'tmp') as folder:
            archive = Path(folder) / 'source.dump'
            transaction = Path(folder) / 'replacement.sql'
            archive.write_bytes(source)
            ops.restore_sql(root, archive, transaction, operation)
            contents = transaction.read_bytes()
        body, commit, trailing = contents.rpartition(b'\nCOMMIT;\n')
        if not commit or trailing:
            raise RuntimeError('Unexpected generated transaction boundary')
        rejected = database(sql, input=body + b'\nSELECT 1/0;\n' + commit, check=False)
        if rejected.returncode == 0 or b'division by zero' not in rejected.stderr or identity() != before:
            raise RuntimeError('Failed marked transaction changed the marker, sequence or rows')
        database(sql, input=contents)
        if identity() != (operation, '17', before[2]):
            raise RuntimeError('Committed marked transaction did not restore the expected sequence and rows')
        if ops.RESTORE_SETTING.encode() in database(['pg_restore', '--file=-'], input=dump()).stdout:
            raise RuntimeError('Restore operation marker escaped into ordinary backup')
    finally:
        ops.compose = original_compose
        subprocess.run(['docker', 'stop', '-t', '5', name], check=True, capture_output=True, timeout=15)
    print('PASS production restore marker lookup and SQL: equal rows, rollback, commit, sequence, ordinary backup')


project = sys.argv[1] if len(sys.argv) == 2 else ''
if project == '--marker-only':
    try:
        verify_transaction_marker()
    except Exception as error:
        print('FAIL marker qualification: ' + type(error).__name__)
        raise SystemExit(1) from None
    raise SystemExit(0)
if not re.fullmatch(r'ibe160-pm-restore-[a-f0-9]{12}', project):
    raise SystemExit('An existing isolated restore-test project is required')
task = root / 'tmp' / project
config = json.loads((task / 'compose.json').read_text())
if (config['services']['private-db']['image'] != project + '-postgres'
        or config['services']['private-api']['image'] != project + '-api'
        or config['volumes'] != {'data': {}}):
    raise SystemExit('Unexpected synthetic project configuration')
output = root / 'tmp' / ('restore-parent-preflight-' + uuid.uuid4().hex[:12])
output.mkdir()
(output / 'secrets').mkdir()
shutil.copyfile(task / 'password', output / 'secrets' / 'postgres-password')
ops.CONFIG = output / 'server.env'
ops.MAINTENANCE = output / 'maintenance'
base = ['docker', 'compose', '-p', project, '-f', str(task / 'compose.json')]

def compose(path, *args, **kwargs):
    if args[0] not in ('config', 'exec'):
        raise RuntimeError('Unexpected preflight transport')
    return subprocess.run(base + list(args), check=True, **kwargs)

ops.compose = compose
actual_run = ops.run

def isolated_run(args, **kwargs):
    if args[0] != 'docker':
        raise RuntimeError('Non-Docker operation forbidden')
    return actual_run(args, **kwargs)

ops.run = isolated_run
results = []
try:
    subprocess.run(base + ['up', '-d', '--no-build', '--wait', 'private-db'], check=True, capture_output=True)
    before = ops.database_fingerprint(root, capture=True).stdout
    for name in ('pre015', 'current', 'malformed'):
        directory = output / name
        directory.mkdir()
        try:
            result = ops.preflight_restore(root, task / (name + '.dump'), directory)
        except ValueError as error:
            if name != 'malformed' or str(error) != 'Restore schema differs from supported release':
                raise
            results.append({'archive': name, 'rejected': True})
        else:
            if name == 'malformed':
                raise RuntimeError('Malformed schema accepted')
            results.append({'archive': name, 'schema': result['schema'], 'passed': True})
        if ops.database_fingerprint(root, capture=True).stdout != before:
            raise RuntimeError('Preflight mutated source database')
        if (ops.MAINTENANCE / 'pending.json').exists():
            raise RuntimeError('Preflight created maintenance state')
        print('PASS actual preflight ' + name)
    (output / 'evidence.json').write_text(json.dumps({'project': project, 'checks': results}, indent=2))
    print('PASS preflight qualification; sanitized evidence ' + str(output / 'evidence.json'))
except Exception as error:
    print('FAIL preflight qualification: ' + type(error).__name__)
    raise SystemExit(1) from None
finally:
    subprocess.run(base + ['stop', 'private-db'], check=True, capture_output=True)
