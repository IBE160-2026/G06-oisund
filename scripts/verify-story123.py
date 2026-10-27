"""Isolated Story 12.3 gates; no ordinary or Story12-integration service mutation."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import secrets
import signal
import shutil
import subprocess
import sys
import tarfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'ibe160-story123-tests'
STAMP = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + secrets.token_hex(4)
RUN = ROOT / 'tmp/story123' / STAMP
RUN.mkdir(parents=True, exist_ok=True)
MODE = sys.argv[1] if len(sys.argv) > 1 else ''
sys.stdout.reconfigure(encoding='utf-8')


def stop_owned_tree(process):
    """Only the process/session created by execute; never service-name matching."""
    result = {'root_pid': process.pid, 'method': 'owned-session' if os.name != 'nt' else 'owned-pid-tree'}
    if os.name == 'nt':
        query = "$rows=Get-CimInstance Win32_Process; $ids=[System.Collections.Generic.HashSet[int]]::new(); [void]$ids.Add(" + str(process.pid) + "); do {$added=$false; foreach($row in $rows){if($ids.Contains([int]$row.ParentProcessId) -and $ids.Add([int]$row.ProcessId)){$added=$true}}}while($added); @($ids) | ConvertTo-Json -Compress"
        snapshot = subprocess.run(['powershell', '-NoProfile', '-Command', query], capture_output=True, text=True, encoding='utf-8', errors='replace')
        pids = json.loads(snapshot.stdout) if snapshot.returncode == 0 and snapshot.stdout.strip() else [process.pid]
        if isinstance(pids, int): pids = [pids]
        result['observed_pids'] = pids
        killed = subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True, text=True, encoding='utf-8', errors='replace')
        result.update(kill_exit_code=killed.returncode, kill_stdout=killed.stdout, kill_stderr=killed.stderr)
        process.wait(timeout=15)
        import ctypes
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        kernel.CloseHandle.argtypes = [ctypes.c_void_p]
        waits = {}
        for pid in pids:
            handle = kernel.OpenProcess(0x00100000, False, pid)
            waits[str(pid)] = not handle or kernel.WaitForSingleObject(handle, 5000) == 0
            if handle: kernel.CloseHandle(handle)
        result.update(awaited_pids=waits, all_observed_exited=all(waits.values()))
    else:
        os.killpg(process.pid, signal.SIGTERM)
        try: process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=15)
        # A child can survive the leader's SIGTERM handler; signal the owned
        # session once more even after its leader has exited.
        try: os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError: pass
        result['all_observed_exited'] = process.poll() is not None
    result['root_returncode'] = process.returncode
    return result


def manifest():
    names = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', 'frontend', 'backend', 'scripts', 'compose.story123.yaml'], cwd=ROOT, text=True).splitlines()
    return {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names if (ROOT/name).is_file()}


def execute(command, cwd=ROOT, env=None, inputs=(), timeout=3600):
    before = manifest()
    hashes = lambda: {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs if p.is_file()}
    actual = hashes()
    bundle = RUN/'bundle-staging'
    bundle.mkdir(parents=True, exist_ok=False)
    archives = ROOT/'docs/evidence/12-3-bundles'
    archives.mkdir(parents=True, exist_ok=True)
    archive_path = archives/f'{STAMP}-{MODE}.tar.gz'
    snapshot_inputs = list(inputs) + [Path(__file__)]
    if MODE == 'browser':
        snapshot_inputs += [ROOT/'scripts/prepare-story123-tests.mjs', *(ROOT/'frontend/dist').rglob('*')]
    snapshots = {}
    for source in snapshot_inputs:
        if not source.is_file(): continue
        relative = source.resolve().relative_to(ROOT.resolve())
        target = bundle/'executed-inputs'/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        snapshots[relative.as_posix()] = hashlib.sha256(target.read_bytes()).hexdigest()
    record = {'mode': MODE, 'project': PROJECT, 'revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'command': command, 'started': datetime.now(timezone.utc).isoformat(), 'source_sha256_before': before, 'executed_input_sha256': actual, 'timeout_seconds': timeout, 'owner_acceptance': 'pending'}
    record['executed_input_snapshots'] = snapshots
    record['durable_bundle'] = str(archive_path.relative_to(ROOT))
    log = RUN/'command.log'
    try:
        with log.open('wb') as output:
            process = subprocess.Popen(command, cwd=cwd, env=env, stdout=output, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0, start_new_session=os.name != 'nt')
            record['owned_root_pid'] = process.pid
            try:
                process.wait(timeout=timeout)
                record['exit_code'] = process.returncode
            except subprocess.TimeoutExpired:
                record.update(exit_code=124, failure_type='TimeoutExpired')
                try: record['timeout_cleanup'] = stop_owned_tree(process)
                except Exception as cleanup_error:
                    record['timeout_cleanup'] = {'error': repr(cleanup_error), 'all_observed_exited': False}
                output.write(b'\nOwned command timed out; original failure preserved.\n')
    except (OSError, subprocess.TimeoutExpired) as error:
        record.update(exit_code=124 if isinstance(error, subprocess.TimeoutExpired) else 1, failure_type=type(error).__name__)
    after = manifest()
    built = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'frontend/dist').rglob('*') if p.is_file()}
    build_source = {name: value for name, value in before.items() if name.startswith('frontend/src/') or name in ['frontend/package.json', 'frontend/package-lock.json', 'frontend/vite.config.ts', 'frontend/tsconfig.json', 'frontend/index.html', 'frontend/demo.html']}
    identity_path = ROOT/'.private-runtime/story123-build.json'
    if MODE == 'build' and record['exit_code'] == 0 and before == after:
        identity_path.parent.mkdir(exist_ok=True)
        identity_path.write_text(json.dumps({'source': build_source, 'built': built}), encoding='utf-8')
    record['build_sha256'] = built
    if MODE == 'browser':
        identity = json.loads(identity_path.read_text(encoding='utf-8')) if identity_path.exists() else {}
        record['tested_build_matches_current_source'] = identity == {'source': build_source, 'built': built}
    record.update(ended=datetime.now(timezone.utc).isoformat(), source_sha256_after=after, source_unchanged=before == after, executed_inputs_unchanged=actual == hashes(), log=str(log.relative_to(ROOT)), log_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
    if MODE == 'browser' and (RUN/'report.json').exists():
        report = json.loads((RUN/'report.json').read_text(encoding='utf-8'))
        record['browser_stats'] = report.get('stats')
        record['browser_report_sha256'] = hashlib.sha256((RUN/'report.json').read_bytes()).hexdigest()
        measurements = []
        def collect(suites):
            for suite in suites:
                collect(suite.get('suites', []))
                for spec in suite.get('specs', []):
                    for test in spec.get('tests', []):
                        for result in test.get('results', []):
                            for attach in result.get('attachments', []):
                                if attach.get('contentType') == 'application/json' and attach.get('body'):
                                    import base64
                                    measurements.append({'test': spec.get('title'), 'state': attach['name'], 'values': json.loads(base64.b64decode(attach['body']))})
        collect(report.get('suites', []))
        if measurements:
            measurement_path = ROOT/f'docs/evidence/12-3-measurements-{STAMP}.json'
            measurement_path.write_text(json.dumps(measurements, indent=2), encoding='utf-8')
            record['measurements'] = str(measurement_path.relative_to(ROOT))
    record['gate_exit_code'] = record['exit_code'] if record['source_unchanged'] and record['executed_inputs_unchanged'] and record.get('tested_build_matches_current_source', True) else 2
    evidence = ROOT/f'docs/evidence/12-3-{MODE}-{STAMP}.json'
    # Preserve available original bytes and actual pre-launch input copies.
    # This creates no invented snapshots for earlier exploratory runs.
    available = [p for p in RUN.rglob('*') if p.is_file() and not p.is_relative_to(bundle)]
    for source in available:
        if source.is_file():
            target = bundle/'raw'/source.relative_to(RUN)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    record['durable_artifact_sha256'] = {p.relative_to(bundle).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in bundle.rglob('*') if p.is_file()}
    record['durable_status'] = 'pending archive verification'
    evidence.write_text(json.dumps(record, indent=2), encoding='utf-8')
    (bundle/'record.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    entries = {p.relative_to(bundle).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in bundle.rglob('*') if p.is_file()}
    with archive_path.open('xb') as output:
        with tarfile.open(fileobj=output, mode='w:gz') as archive:
            for name in entries: archive.add(bundle/name, arcname=name, recursive=False)
    # Re-read every archived byte before deleting our own verified staging tree.
    with tarfile.open(archive_path, 'r:gz') as archive:
        archived = {member.name: hashlib.sha256(archive.extractfile(member).read()).hexdigest() for member in archive.getmembers() if member.isfile()}
    if archived != entries:
        record.update(durable_status='archive verification failed; staging preserved', gate_exit_code=2)
        evidence.write_text(json.dumps(record, indent=2), encoding='utf-8')
        raise SystemExit(2)
    archive_hash = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    index_path = archives/f'{STAMP}-{MODE}.index.json'
    index_path.write_text(json.dumps({'archive': str(archive_path.relative_to(ROOT)), 'archive_sha256': archive_hash, 'entries': entries}, indent=2), encoding='utf-8')
    record.update(durable_status='verified archive and per-entry hashes', durable_bundle_sha256=archive_hash, durable_bundle_index=str(index_path.relative_to(ROOT)))
    evidence.write_text(json.dumps(record, indent=2), encoding='utf-8')
    expected_parent = (ROOT/'tmp/story123').resolve()
    if bundle.name != 'bundle-staging' or bundle.parent.resolve() != RUN.resolve() or not bundle.resolve().is_relative_to(expected_parent):
        raise RuntimeError('Refusing to remove unverified staging path')
    shutil.rmtree(bundle)
    print(log.read_text(encoding='utf-8', errors='replace')[-6000:])
    print(f'EVIDENCE={evidence} EXIT={record["gate_exit_code"]}', flush=True)
    raise SystemExit(record['gate_exit_code'])


def integration():
    # Execute a disposable translated copy of the already qualified synthetic
    # verifier. Keep its guards and literal assertions; hash the actual copy.
    source = (ROOT/'scripts/verify-story12-integration.py').read_text(encoding='utf-8')
    for old, new in [('ibe160-story12-integration', PROJECT), ('compose.story12-integration.yaml', 'compose.story123.yaml'), ('15312','15323'), ('18312','18323'), ('18313','18324'), ('/run/secrets/integration_password','/run/secrets/story123_password'), ('integration_fictional','story123_fictional'), ('integration_private','story123_private'), ('story12-integration-postgres-password','story123-postgres-password'), ('story12-manual-credentials','story123-manual-credentials'), ('synthetic-story12-manual','synthetic-story123-manual'), ('12-integration-real-', '12-3-real-')]:
        source = source.replace(old, new)
    source = source.replace('ROOT = Path(__file__).resolve().parents[1]', 'ROOT = Path(' + repr(str(ROOT)) + ')')
    actual = RUN/'integration.py'
    actual.write_text(source, encoding='utf-8')
    execute([sys.executable, str(actual), MODE], inputs=[actual])


def browser():
    subprocess.run([shutil.which('node'), 'scripts/prepare-story123-tests.mjs'], cwd=ROOT, check=True)
    target = ROOT/'frontend/.story123-tests'
    captures = RUN/'captures'
    captures.mkdir()
    # Historical evidence files are immutable. Every run gets its own outputs.
    for path in target.glob('*.ts'):
        source = path.read_text(encoding='utf-8').replace('../docs/evidence', '../tmp/story123/'+STAMP+'/captures')
        path.write_text(source, encoding='utf-8')
    config = ROOT/'frontend/playwright.story123.config.ts'
    args = sys.argv[2:] or ['tablet-pc.spec.ts', 'tablet-pc-private.spec.ts']
    env = dict(os.environ, COMPOSE_PROJECT_NAME=PROJECT, STORY123_OUTPUT_DIR=str(RUN/'results'), STORY123_REPORT=str(RUN/'report.json'))
    execute([shutil.which('npx.cmd') or shutil.which('npx'), 'playwright', 'test', '--config=playwright.story123.config.ts', *args], ROOT/'frontend', env, [config, *target.glob('*.ts')])


def preview():
    import importlib.util
    spec = importlib.util.spec_from_file_location('story123_preview', ROOT/'scripts/verify-retained-data.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PREVIEW_PORT = 15323
    module.LOGS = ROOT/'tmp/story123-preview'
    module.LOGS.mkdir(parents=True, exist_ok=True)
    module.PREVIEW = module.LOGS/'frontend-server.json'
    if MODE == 'stop-preview': module.stop_preview()
    else: module.serve_preview()


if __name__ == '__main__':
    if MODE in ('up', 'verify', 'prepare'): integration()
    elif MODE == 'build': execute([shutil.which('npm.cmd') or shutil.which('npm'), 'run', 'build'], ROOT/'frontend', dict(os.environ, VITE_PRIVATE_API='http://127.0.0.1:18324', VITE_FICTIONAL_API='http://127.0.0.1:18323'))
    elif MODE == 'browser': browser()
    elif MODE in ('serve', 'stop-preview'): preview()
    else: raise SystemExit('Use up|verify|prepare|build|browser [specs/filters]|serve|stop-preview')
