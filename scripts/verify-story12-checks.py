"""Integrated build/regression gates; original assertions and evidence are preserved."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'ibe160-story12-integration'
COMPOSE = ['docker', 'compose', '-p', PROJECT, '-f', 'compose.story12-integration.yaml']
RUN = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + secrets.token_hex(4)
LOGS = ROOT / 'tmp/story12' / RUN
LOGS.mkdir(parents=True, exist_ok=True)
sys.stdout.reconfigure(encoding='utf-8')


def hashes():
    names = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', 'backend', 'frontend', 'scripts', 'Eksempelfiler', 'compose.story12-integration.yaml'], cwd=ROOT, text=True).splitlines()
    return {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names if (ROOT/name).is_file()}


def input_hashes(paths):
    result = {}
    for path in paths:
        try:
            result[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            result[str(path.relative_to(ROOT))] = None
    return result


def execute(command, cwd=ROOT, env=None, executed_inputs=()):
    before = hashes()
    started = datetime.now(timezone.utc)
    inputs = input_hashes(executed_inputs)
    record = {'run': RUN, 'mode': sys.argv[1], 'revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'command': command, 'started': started.isoformat(), 'exit_code': 1, 'timeout_seconds': 7200, 'executed_input_sha256': inputs}
    try:
        with (LOGS/'command.log').open('wb') as output:
            result = subprocess.run(command, cwd=cwd, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=7200)
        record['exit_code'] = result.returncode
    except Exception as error:
        record['failure_type'] = type(error).__name__
        record['exit_code'] = 124 if isinstance(error, subprocess.TimeoutExpired) else 1
    finally:
        try:
            after = hashes()
        except Exception as error:
            after = None
            record['manifest_failure_type'] = type(error).__name__
        input_after = input_hashes(executed_inputs)
        record.update(ended=datetime.now(timezone.utc).isoformat(), source_unchanged=before == after, source_sha256=after, executed_inputs_unchanged=inputs == input_after, executed_input_sha256_after=input_after, log=str((LOGS/'command.log').relative_to(ROOT)), log_sha256=hashlib.sha256((LOGS/'command.log').read_bytes()).hexdigest())
        record['gate_exit_code'] = record['exit_code'] if before == after and inputs == input_after else 2
        (ROOT/'docs/evidence'/f'12-integrated-{sys.argv[1]}-{RUN}.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    print((LOGS/'command.log').read_text(encoding='utf-8', errors='replace')[-5000:])
    print(f'EXIT={record["gate_exit_code"]} SOURCE_UNCHANGED={before == after} LOG={LOGS}', flush=True)
    raise SystemExit(record['gate_exit_code'])


def browser(demo=False):
    target = ROOT/f'frontend/tmp/story12-tests-{RUN}'
    target.mkdir(parents=True, exist_ok=True)
    captures = ROOT/'tmp/story12'/RUN/'captures'
    captures.mkdir(parents=True, exist_ok=True)
    for path in (ROOT/'frontend/tests').glob('*.ts'):
        text = path.read_text(encoding='utf-8')
        for original, replacement in [(':8001', ':18313'), (':8000', ':18312'), (':5173', ':15312'), (':15222', ':15312'), ('ibe160-private-tests', PROJECT), ('compose.private.yaml', 'compose.story12-integration.yaml'), ('../docs/evidence', f'../tmp/story12/{RUN}/captures'), ("'../src/", "'../../src/"), ("'../../backend/", "'../../../backend/")]:
            text = text.replace(original, replacement)
        (target/path.name).write_text(text, encoding='utf-8')
    config = ROOT/f'frontend/tmp/story12-{RUN}.config.ts'
    match = 'fictional-*.spec.ts' if demo else 'private-*.spec.ts'
    config.write_text("import { defineConfig } from '@playwright/test';\nexport default defineConfig(" + json.dumps({'testDir': f'./{target.name}', 'testMatch': match, 'outputDir': str(LOGS/'results'), 'workers': 1, 'timeout': 60000, 'use': {'baseURL': 'http://127.0.0.1:15312', 'channel': 'msedge', 'headless': True}, 'reporter': [['line']]}) + ');\n', encoding='utf-8')
    execute([shutil.which('npx.cmd'), 'playwright', 'test', f'--config=tmp/{config.name}', *sys.argv[2:]], ROOT/'frontend', dict(os.environ, COMPOSE_PROJECT_NAME=PROJECT), [config, *target.glob('*.ts')])


def preview(stop=False):
    spec = importlib.util.spec_from_file_location('retained_preview', ROOT/'scripts/verify-retained-data.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PREVIEW_PORT = 15312
    module.LOGS = ROOT/'tmp/story12'
    module.PREVIEW = module.LOGS/'frontend-server.json'
    if stop:
        module.stop_preview()
    else:
        module.serve_preview()


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'build':
        execute([shutil.which('npm.cmd'), 'run', 'build'], ROOT/'frontend', dict(os.environ, VITE_PRIVATE_API='http://127.0.0.1:18313', VITE_FICTIONAL_API='http://127.0.0.1:18312'))
    elif mode == 'backend':
        execute(COMPOSE + ['exec', '-T', 'private-api', 'python', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *(sys.argv[2:] or ['tests', '--ignore=tests/test_assessment.py'])])
    elif mode == 'fictional':
        bootstrap = "import os,runpy,sys; from pathlib import Path; from urllib.parse import quote; os.environ['DATABASE_URL']='postgresql://fictional:'+quote(Path('/run/secrets/integration_password').read_text().strip(),safe='')+'@db/fictional_assessment'; sys.argv=['pytest','-q','-p','no:cacheprovider','tests/test_assessment.py']; runpy.run_module('pytest',run_name='__main__')"
        execute(COMPOSE + ['exec', '-T', 'api', 'python', '-c', bootstrap])
    elif mode in ('browser', 'demo'):
        browser(mode == 'demo')
    elif mode in ('serve', 'stop-preview'):
        preview(mode == 'stop-preview')
    elif mode == 'checks':
        execute([sys.executable, '-m', 'unittest', 'scripts/test_verify_retained_data.py', 'scripts/test_verify_private_drafts.py', 'scripts/test_verify_story12_integration.py', 'scripts/test_verify_story12_checks.py'])
    else:
        raise SystemExit('Use build|backend|fictional|browser|demo|serve|stop-preview|checks')
