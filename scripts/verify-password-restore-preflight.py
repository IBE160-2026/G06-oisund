"""Actual restore preflight against a completed synthetic runner's archives.

Usage: python scripts/verify-password-restore-preflight.py ibe160-pm-restore-HEX
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
import types
import uuid

root = Path(__file__).resolve().parent.parent
project = sys.argv[1] if len(sys.argv) == 2 else ''
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
if os.name == 'nt':
    sys.modules['fcntl'] = types.ModuleType('fcntl')
original_path = os.environ['PATH']
spec = importlib.util.spec_from_file_location('restore_ops', root / 'deploy/ubuntu/bussassistentctl.py')
ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ops)
os.environ['PATH'] = original_path
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
