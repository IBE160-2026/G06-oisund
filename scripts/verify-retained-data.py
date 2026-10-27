"""Story 12.1 only: isolated synthetic runtime; never stops ordinary services.
Run with Python from the repository root: scripts/verify-retained-data.py backend|build|browser|serve|restart|stop.
The dedicated project/ports and credentials are deliberately independent.
"""
import hashlib
import json
import os
import shutil
import socket
import urllib.request
from pathlib import Path
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
LOGS = ROOT / 'tmp/story121'
LOGS.mkdir(parents=True, exist_ok=True)
COMPOSE = ['docker', 'compose', '-p', 'ibe160-story121-tests', '-f', 'compose.story121.yaml']

def hashes():
    files = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', 'backend', 'frontend', 'compose.story121.yaml', 'compose.yaml', 'compose.private.yaml', 'scripts/verify-retained-data.py'], cwd=ROOT).decode().splitlines()
    return {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files if (ROOT/f).is_file()}


def run(label, args, cwd=ROOT, env=None):
    started = time.time()
    name = time.strftime('%Y%m%d-%H%M%S') + '-' + label
    before = hashes()
    (LOGS / (name + '-before.json')).write_text(json.dumps(before, indent=2), encoding='utf-8')
    path = LOGS / (name + '.log')
    with path.open('wb') as stream:
        result = subprocess.run(args, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT)
    after = hashes()
    (LOGS / (name + '-after.json')).write_text(json.dumps(after, indent=2), encoding='utf-8')
    unchanged = before == after
    with path.open('a', encoding='utf-8') as stream:
        stream.write(f'\nEXIT_CODE={result.returncode} ELAPSED_SECONDS={time.time()-started:.2f} SOURCE_UNCHANGED={unchanged}\n')
    print(f'{label}: exit={result.returncode} source_unchanged={unchanged} log={path}', flush=True)
    print(path.read_text(encoding='utf-8', errors='replace')[-3000:], flush=True)
    return result.returncode if unchanged else 2

PREVIEW = LOGS / 'frontend-server.json'
VITE = ROOT / 'frontend/node_modules/vite/bin/vite.js'
PREVIEW_PORT = 15121


def process_identity(pid):
    # Read-only inspection. PID is parsed as an integer, never shell text.
    command = (f"$p=Get-CimInstance Win32_Process -Filter 'ProcessId={int(pid)}'; "
               "if($p){@{pid=$p.ProcessId;command=$p.CommandLine;created=$p.CreationDate.ToUniversalTime().ToString('o')}|ConvertTo-Json -Compress}")
    result = subprocess.run(['powershell.exe', '-NoProfile', '-Command', command], capture_output=True, text=True, check=True)
    return json.loads(result.stdout) if result.stdout.strip() else None


def preview_listener(pid):
    result = subprocess.run(['powershell.exe', '-NoProfile', '-Command', f"Get-NetTCPConnection -State Listen -LocalPort {PREVIEW_PORT} -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess"], capture_output=True, text=True)
    return int(pid) in [int(value) for value in result.stdout.split() if value.isdigit()]


def owned_preview(record, current):
    return (record.get('root') == str(ROOT) and record.get('vite') == str(VITE)
            and current is not None and record.get('identity') == current
            and str(VITE).casefold() in current['command'].casefold()
            and f'--port {PREVIEW_PORT}' in current['command'] and '--strictPort' in current['command'])


def stop_preview():
    if not PREVIEW.exists():
        print('No verified preview ownership record; no preview process stopped.', flush=True)
        return
    record = json.loads(PREVIEW.read_text(encoding='utf-8'))
    current = process_identity(record['identity']['pid'])
    if current is None:
        PREVIEW.unlink()
        return
    if not owned_preview(record, current):
        raise RuntimeError('Preview identity changed; refusing to stop any process.')
    subprocess.run(['taskkill.exe', '/PID', str(current['pid']), '/T', '/F'], check=True, capture_output=True)
    PREVIEW.unlink()


def serve_preview():
    # Refuse an existing listener before starting anything. A subsequent port
    # race is also caught by child exit and verified listener ownership.
    with socket.socket() as probe:
        try:
            probe.bind(('127.0.0.1', PREVIEW_PORT))
        except OSError as error:
            raise RuntimeError(f'Port {PREVIEW_PORT} is occupied; existing listener left untouched.') from error
    with (LOGS / 'frontend-server.log').open('ab') as log:
        process = subprocess.Popen([shutil.which('node') or 'node', str(VITE), 'preview', '--host', '127.0.0.1', '--port', str(PREVIEW_PORT), '--strictPort'], cwd=ROOT / 'frontend', stdout=log, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
    identity = process_identity(process.pid)
    record = {'root': str(ROOT), 'vite': str(VITE), 'identity': identity}
    if identity is None or not owned_preview(record, identity):
        raise RuntimeError('Preview exited before ownership could be verified; see frontend-server.log.')
    PREVIEW.write_text(json.dumps(record, indent=2), encoding='utf-8')
    try:
        deadline = time.monotonic()+10
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError('Preview startup failed; see frontend-server.log.')
            try:
                with urllib.request.urlopen(f'http://127.0.0.1:{PREVIEW_PORT}/', timeout=0.5) as response:
                    if response.status == 200 and preview_listener(process.pid):
                        print(f'Verified isolated frontend process {process.pid} ready on {PREVIEW_PORT}', flush=True)
                        return
            except (OSError, TimeoutError):
                pass
            time.sleep(0.1)
        raise RuntimeError('Preview did not become ready on its owned port.')
    except BaseException:
        stop_preview()
        raise


def main():
    mode = sys.argv[1]
    if mode == 'backend':
        code = run('backend', COMPOSE + ['exec', '-T', 'private-api', 'python', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *(sys.argv[2:] or ['tests', '--ignore=tests/test_assessment.py'])])
    elif mode == 'build':
        env = dict(os.environ, VITE_PRIVATE_API='http://127.0.0.1:18121', VITE_FICTIONAL_API='http://127.0.0.1:18122')
        code = run('build', ['cmd', '/c', 'npm', 'run', 'build'], ROOT / 'frontend', env)
    elif mode == 'browser':
        # Preserve every original assertion and source fixture. Only substitute
        # isolated endpoints/project in disposable test copies under ignored tmp.
        target = ROOT / 'frontend/tmp/story121-tests'
        target.mkdir(parents=True, exist_ok=True)
        (LOGS / 'captures').mkdir(parents=True, exist_ok=True)
        for path in (ROOT / 'frontend/tests').glob('*.ts'):
            text = path.read_text(encoding='utf-8').replace(':8001', ':18121').replace(':5173', ':15121').replace('ibe160-private-tests', 'ibe160-story121-tests').replace('compose.private.yaml', 'compose.story121.yaml').replace('../docs/evidence', '../tmp/story121/captures')
            text = text.replace("'../src/", "'../../src/").replace("'../../backend/", "'../../../backend/")
            (target / path.name).write_text(text, encoding='utf-8')
        config = ROOT / 'frontend/tmp/story121.config.ts'
        config.write_text("import { defineConfig } from '@playwright/test';\nexport default defineConfig({ testDir: './story121-tests', workers: 1, timeout: 60000, use: { baseURL: 'http://127.0.0.1:15121', channel: 'msedge', headless: true }, reporter: 'line' });\n", encoding='utf-8')
        env = dict(os.environ, COMPOSE_PROJECT_NAME='ibe160-story121-tests')
        suites = sys.argv[2:] or ['private-retention', 'private-drafts', 'private-access', 'private-import', 'private-crossday', 'private-notice-recovery', 'private-notice-reader', 'private-notices']
        code = run('browser', ['cmd', '/c', 'npx', 'playwright', 'test', '--config=tmp/story121.config.ts', *suites], ROOT / 'frontend', env)
    elif mode == 'restart':
        code = run('restart', COMPOSE + ['restart', 'private-api'])
    elif mode == 'serve':
        serve_preview()
        code = 0
    elif mode == 'stop':
        stop_preview()
        code = run('stop', COMPOSE + ['stop'])
    else:
        raise SystemExit('Unknown mode')
    files = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', 'backend', 'frontend', 'compose.story121.yaml', 'compose.yaml', 'compose.private.yaml', 'scripts/verify-retained-data.py'], cwd=ROOT).decode().splitlines()
    (LOGS / ('source-hashes-' + mode + '.json')).write_text(json.dumps({f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files if (ROOT/f).is_file()}, indent=2), encoding='utf-8')
    raise SystemExit(code)


if __name__ == "__main__":
    main()
