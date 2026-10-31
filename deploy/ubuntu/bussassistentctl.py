#!/usr/bin/python3
"""Root-owned operations for one isolated Compose project. No secret output."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile
import time
import unicodedata

ROOT = Path('/opt/bussassistent')
CONFIG = Path('/etc/bussassistent/server.env')
DATA_READY = Path('/etc/bussassistent/data-ready')
UPLOADS = Path('/home/jonas/ibe160-upload')
BACKUPS = Path('/var/backups/bussassistent')
SHA = re.compile(r'[a-f0-9]{40}')
os.environ['PATH'] = '/usr/sbin:/usr/bin:/sbin:/bin'
os.umask(0o077)


def run(args, **kw):
    return subprocess.run(args, check=True, **kw)


def release(value=None):
    path = ROOT / 'current' if value is None else ROOT / 'releases' / value
    if value is not None and not SHA.fullmatch(value):
        raise ValueError('A full commit SHA is required')
    result = path.resolve(strict=True)
    if result.parent != ROOT / 'releases' or not SHA.fullmatch(result.name):
        raise ValueError('Invalid release path')
    return result


def compose(path, *args, **kw):
    env = dict(os.environ, RELEASE_ID=path.name)
    return run(['docker', 'compose', '--project-name', 'bussassistent',
                '--env-file', str(CONFIG), '-f', str(path / 'deploy/ubuntu/compose.yaml'),
                *args], env=env, **kw)


def recovery(action, username):
    """Bounded operator entry point; check OUTER terminal before Docker's PTY."""
    if (action not in ('recovery-issue', 'recovery-revoke')
            or any(unicodedata.category(c).startswith('C') for c in username)):
        raise ValueError('Invalid recovery command or username')
    username = username.strip().casefold()
    if not 1 <= len(username) <= 100 or username.startswith('-'):
        raise ValueError('Invalid recovery username')
    if not all(os.isatty(fd) for fd in (0, 1, 2)):
        raise ValueError('Recovery requires an interactive terminal without redirection')
    # /dev/tty is an alias, so comparing its st_rdev to /dev/pts/N is invalid.
    terminal = os.open('/dev/tty', os.O_RDWR | os.O_NOCTTY)
    try:
        if (len({os.ttyname(fd) for fd in (0, 1, 2)}) != 1
                or any(os.tcgetpgrp(fd) != os.getpgrp() for fd in (0, 1, 2, terminal))):
            raise ValueError('Recovery requires the same foreground controlling terminal')
        path = release()
        # Never capture the Docker stream. The inner CLI also checks its TTY and
        # performs identity/no-recording/target preflight before issuing a code.
        # Compose exec allocates an interactive TTY by default (no -T).
        compose(path, 'exec', 'private-api',
                'python', '-m', 'app.manage', action, username,
                stdin=terminal, stdout=terminal, stderr=terminal)
    finally:
        os.close(terminal)


def link(name, path):
    temporary = ROOT / (name + '.new')
    temporary.unlink(missing_ok=True)
    temporary.symlink_to(path)
    temporary.replace(ROOT / name)


def migrations(path):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (path / 'backend/migrations/private').glob('*.sql')}


def backup(path):
    BACKUPS.mkdir(mode=0o750, parents=True, exist_ok=True)
    stamp = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    target = BACKUPS / (stamp + '-' + path.name + '.dump')
    temporary = target.with_suffix('.partial')
    with temporary.open('xb') as output:
        compose(path, 'exec', '-T', 'private-db', 'pg_dump',
                '-U', 'tablet_bootstrap', '-d', 'private_work', '-Fc',
                '--no-owner', '--no-acl', stdout=output)
        output.flush()
        os.fsync(output.fileno())
    if temporary.stat().st_size < 100:
        raise ValueError('Backup is unexpectedly empty')
    # pg_restore verifies the archive table of contents without restoring anything.
    with temporary.open('rb') as data:
        compose(path, 'exec', '-T', 'private-db', 'pg_restore', '--list',
                stdin=data, stdout=subprocess.DEVNULL)
    temporary.replace(target)
    import grp
    os.chown(target, 0, grp.getgrnam('jonas').gr_gid)
    target.chmod(0o640)
    # Retain at most 48 hours on server; never touch unrelated files.
    for old in BACKUPS.glob('*.dump'):
        if old.is_file() and not old.is_symlink() and old.stat().st_mtime < time.time() - 172800:
            old.unlink()
    print(target)
    return target


def ready(path):
    compose(path, 'exec', '-T', 'private-api', 'python', '-c',
            "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=5)")
    host = next(line.split('=', 1)[1].strip()
                for line in CONFIG.read_text().splitlines() if line.startswith('TABLET_HOST='))
    result = run(['curl', '-sS', '--max-time', '10', '-o', '/dev/null', '-w', '%{http_code}',
                  '-H', 'Host: ' + host, 'http://127.0.0.1:18081/private'],
                 capture_output=True, text=True)
    if result.stdout != '403':
        raise ValueError('Origin must reject missing Cloudflare assertion with 403')
    print('API healthy; origin access control rejects unauthenticated requests')


def start(path):
    compose(path, 'up', '-d', '--no-build', '--pull', 'never', '--wait', '--wait-timeout', '180')
    for attempt in range(10):
        try:
            ready(path)
            return
        except (ValueError, subprocess.CalledProcessError):
            if attempt == 9:
                raise
            time.sleep(2)


def stage(commit, digest):
    if not SHA.fullmatch(commit) or not re.fullmatch(r'[a-f0-9]{64}', digest):
        raise ValueError('Invalid commit or archive digest')
    archive = UPLOADS / (commit + '.tar')
    target = ROOT / 'releases' / commit
    if target.exists():
        identity = json.loads((target / 'release-identity.json').read_text())
        if identity != {'commit': commit, 'archive_sha256': digest}:
            raise ValueError('Existing release identity mismatch')
        compose(target, 'config', '--quiet')
        compose(target, 'build', '--pull')
        print('Verified and rebuilt existing release ' + commit)
        return
    # Hash and extract the same open file, preventing a path-swap between checks.
    with archive.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
        if actual != digest:
            raise ValueError('Archive digest mismatch')
        stream.seek(0)
        with tarfile.open(fileobj=stream) as tar:
            members = tar.getmembers()
            if any(not (m.isfile() or m.isdir()) or m.name.startswith('/')
                   or '..' in Path(m.name).parts for m in members):
                raise ValueError('Archive contains unsafe entries')
            if sum(m.size for m in members) > 1024 * 1024 * 1024:
                raise ValueError('Release archive is too large')
            with tempfile.TemporaryDirectory(prefix='.stage-', dir=ROOT / 'releases') as tmp:
                tar.extractall(tmp, members=members, filter='data')
                source = Path(tmp)
                for required in ('backend/Dockerfile', 'deploy/tablet/Dockerfile',
                                 'deploy/ubuntu/compose.yaml'):
                    if not (source / required).is_file():
                        raise ValueError('Incomplete release')
                (source / 'release-identity.json').write_text(json.dumps(
                    {'commit': commit, 'archive_sha256': digest}, indent=2))
                for p in source.rglob('*'):
                    os.chown(p, 0, 0)
                    p.chmod(0o755 if p.is_dir() else 0o644)
                source.chmod(0o755)
                source.rename(target)
    compose(target, 'config', '--quiet')
    compose(target, 'build', '--pull')
    print('Staged and built ' + commit)



def install_secrets():
    import shutil
    destination = CONFIG.parent
    files = {
        'bootstrap-password': (destination / 'secrets/bootstrap-password', 0o444),
        'postgres-password': (destination / 'secrets/postgres-password', 0o444),
        'access-policy.json': (destination / 'secrets/access-policy.json', 0o444),
        'tunnel-token': (destination / 'tunnel-token', 0o600),
    }
    # Validate every input before installing any; never echo contents.
    for name, (target, mode) in files.items():
        source = UPLOADS / 'secrets' / name
        if source.is_symlink() or not source.is_file() or not 1 <= source.stat().st_size <= 65536:
            raise ValueError('Invalid credential file: ' + name)
        if target.exists() and source.read_bytes() != target.read_bytes():
            raise ValueError('Refusing to overwrite an existing credential: ' + name)
    policy = json.loads((UPLOADS / 'secrets/access-policy.json').read_text())
    if set(policy) != {'team', 'audience', 'owner_email'}:
        raise ValueError('Unexpected Access policy')
    for name, (target, mode) in files.items():
        if not target.exists():
            shutil.copyfile(UPLOADS / 'secrets' / name, target)
        os.chown(target, 0, 0)
        target.chmod(mode)
    expected = 'TABLET_HOST=app.bussassistent.com\n'
    if CONFIG.exists() and CONFIG.read_text() != expected:
        raise ValueError('Existing hostname configuration differs')
    CONFIG.write_text(expected)
    CONFIG.chmod(0o600)
    print('Credentials installed without displaying values')


def restore_initial(commit, digest):
    if (ROOT / 'current').exists() or DATA_READY.exists():
        raise ValueError('Initial restore refused after deployment')
    path = release(commit)
    count = compose(path, 'exec', '-T', 'private-db', 'psql', '-U', 'tablet_bootstrap',
                    '-d', 'private_work', '-Atc',
                    "SELECT count(*) FROM pg_tables WHERE schemaname='public'",
                    capture_output=True, text=True).stdout.strip()
    if count != '0':
        raise ValueError('Restore requires an empty database; existing data will not be overwritten')
    if not re.fullmatch(r'[a-f0-9]{64}', digest):
        raise ValueError('Invalid dump digest')
    with (UPLOADS / 'initial.dump').open('rb') as dump:
        if hashlib.file_digest(dump, 'sha256').hexdigest() != digest:
            raise ValueError('Dump digest mismatch')
        dump.seek(0)
        compose(path, 'exec', '-T', 'private-db', 'pg_restore', '-U', 'tablet_bootstrap',
                '-d', 'private_work', '--role=private_work', '--no-owner', '--no-privileges',
                '--exit-on-error', '--single-transaction', stdin=dump)
    print('Initial restore completed; app and tunnel remain stopped')


def database_summary(path):
    # Counts only, no identities, row contents, passwords or session values.
    sql = """SELECT 'accounts=' || count(*) FROM accounts;
SELECT 'migrations=' || count(*) FROM private_migrations;
SELECT 'drafts=' || count(*) FROM drafts;
SELECT 'workdays=' || count(*) FROM workdays;"""
    compose(path, 'exec', '-T', 'private-db', 'psql', '-U', 'tablet_bootstrap',
            '-d', 'private_work', '-Atc', sql)


def fingerprint_sql():
    return "CREATE TEMP TABLE fingerprints(table_name text, row_count bigint, digest text);\nDO $body$\nDECLARE r record;\nBEGIN\nFOR r IN SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename LOOP\nEXECUTE format($fmt$INSERT INTO fingerprints SELECT %L, count(*),\nmd5(coalesce(string_agg(row_to_json(t)::text, chr(10) ORDER BY row_to_json(t)::text), ''))\nFROM public.%I t$fmt$, r.tablename, r.tablename);\nEND LOOP;\nEND $body$;\nSELECT * FROM fingerprints ORDER BY table_name;"
def database_fingerprint(path, capture=False):
    return compose(path, 'exec', '-T', 'private-db', 'psql', '-U', 'tablet_bootstrap',
                   '-d', 'private_work', '-qAtc', fingerprint_sql(), capture_output=capture, text=capture)

def install_tools(path):
    import shutil
    for name in ('bussassistent.service', 'cloudflared.service',
                 'bussassistent-backup.service', 'bussassistent-backup.timer'):
        target = Path('/etc/systemd/system') / name
        if target.is_symlink():
            raise ValueError('Unexpected service symlink')
        target.write_text((path / 'deploy/ubuntu' / name).read_text(), newline='\n')
        target.chmod(0o644)
    temporary = Path('/usr/local/sbin/bussassistentctl.new')
    temporary.write_text((path / 'deploy/ubuntu/bussassistentctl.py').read_text(), newline='\n')
    temporary.chmod(0o755)
    temporary.replace('/usr/local/sbin/bussassistentctl')
    run(['systemctl', 'daemon-reload'])

def test_recovery():
    """Controlled crash test for this project's API, DB and tunnel only."""
    import signal
    path = release()
    was_active = subprocess.run(['systemctl', 'is-active', '--quiet', 'cloudflared']).returncode == 0
    run(['systemctl', 'stop', 'cloudflared'])
    backup(path)
    before = database_fingerprint(path, capture=True).stdout
    for service in ('private-api', 'private-db'):
        container_id = compose(path, 'ps', '-q', service, capture_output=True, text=True).stdout.strip()
        record = json.loads(run(['docker', 'inspect', container_id], capture_output=True, text=True).stdout)[0]
        labels = record['Config']['Labels']
        if (labels.get('com.docker.compose.project') != 'bussassistent'
                or labels.get('com.docker.compose.service') != service
                or not record['State']['Running'] or record['State']['Pid'] <= 1):
            raise ValueError('Refusing fault injection outside the running production project')
        previous_restarts = record['RestartCount']
        # pidfd pins the process identity, avoiding signalling a recycled host PID.
        fd = os.pidfd_open(record['State']['Pid'])
        try:
            check = json.loads(run(['docker', 'inspect', container_id], capture_output=True, text=True).stdout)[0]
            if check['State']['Pid'] != record['State']['Pid'] or not check['State']['Running']:
                raise ValueError('Container identity changed before fault injection')
            signal.pidfd_send_signal(fd, signal.SIGKILL)
        finally:
            os.close(fd)
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            check = json.loads(run(['docker', 'inspect', container_id], capture_output=True, text=True).stdout)[0]
            if (check['RestartCount'] > previous_restarts and check['State']['Running']
                    and check['State'].get('Health', {}).get('Status') == 'healthy'):
                break
            time.sleep(2)
        else:
            raise ValueError(service + ' did not automatically recover')
        ready(path)
        print(service + ': automatic recovery after process crash passed')
    after = database_fingerprint(path, capture=True).stdout
    if before != after:
        raise ValueError('Database fingerprint changed during recovery test; inspect before reopening tunnel')
    print('All table fingerprints unchanged during crash tests')
    if was_active:
        run(['systemctl', 'start', '--no-block', 'cloudflared'])
        wait_tunnel()
        old_restarts = run(['systemctl', 'show', 'cloudflared', '-p', 'NRestarts', '--value'],
                           capture_output=True, text=True).stdout.strip()
        run(['systemctl', 'kill', '--kill-whom=main', '--signal=SIGKILL', 'cloudflared'])
        time.sleep(12)
        wait_tunnel()
        new_restarts = run(['systemctl', 'show', 'cloudflared', '-p', 'NRestarts', '--value'],
                           capture_output=True, text=True).stdout.strip()
        if int(new_restarts) <= int(old_restarts):
            raise ValueError('Tunnel restart count did not increase')
        print('Cloudflare Tunnel: automatic recovery after process crash passed')


def wait_tunnel():
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        result = subprocess.run(['curl', '-s', '--max-time', '3', '-o', '/dev/null',
                                 '-w', '%{http_code}', 'http://127.0.0.1:18083/ready'],
                                capture_output=True, text=True)
        if result.returncode == 0 and result.stdout == '200':
            return
        time.sleep(2)
    raise ValueError('Tunnel did not become ready')


def verify_restore():
    """Restore a fresh backup into disposable, networkless tmpfs PostgreSQL."""
    import uuid
    path = release()
    before = database_fingerprint(path, capture=True).stdout
    dump = backup(path)
    after = database_fingerprint(path, capture=True).stdout
    if before != after:
        raise ValueError('Data changed while taking test backup; retry during quiet period')
    db_id = compose(path, 'ps', '-q', 'private-db', capture_output=True, text=True).stdout.strip()
    record = json.loads(run(['docker', 'inspect', db_id], capture_output=True, text=True).stdout)[0]
    image = record['Image']  # Exact installed image, no pull.
    name = 'bussassistent-restore-check-' + uuid.uuid4().hex[:12]
    created = False
    try:
        run(['docker', 'run', '-d', '--name', name, '--network', 'none',
             '--memory', '512m', '--pids-limit', '128',
             '--tmpfs', '/var/lib/postgresql/data:rw,size=512m',
             '-e', 'POSTGRES_HOST_AUTH_METHOD=trust',
             '-e', 'POSTGRES_USER=tablet_bootstrap',
             '-e', 'POSTGRES_DB=private_work', image], stdout=subprocess.DEVNULL)
        created = True
        for attempt in range(45):
            result = subprocess.run(['docker', 'exec', name, 'pg_isready',
                                     '-h', '127.0.0.1', '-U', 'tablet_bootstrap', '-d', 'private_work'],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                break
            time.sleep(1)
        else:
            raise ValueError('Isolated restore database did not become ready')
        run(['docker', 'exec', name, 'psql', '-U', 'tablet_bootstrap', '-d', 'private_work',
             '-v', 'ON_ERROR_STOP=1', '-c', 'CREATE ROLE private_work LOGIN',
             '-c', 'ALTER DATABASE private_work OWNER TO private_work',
             '-c', 'ALTER SCHEMA public OWNER TO private_work'],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        with dump.open('rb') as stream:
            run(['docker', 'exec', '-i', name, 'pg_restore', '-U', 'tablet_bootstrap',
                 '-d', 'private_work', '--role=private_work', '--no-owner',
                 '--no-privileges', '--exit-on-error', '--single-transaction'],
                stdin=stream, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        restored = run(['docker', 'exec', name, 'psql', '-U', 'tablet_bootstrap',
                        '-d', 'private_work', '-qAtc', fingerprint_sql()],
                       capture_output=True, text=True).stdout
        if restored != before:
            raise ValueError('Isolated restore fingerprint mismatch')
        print('Isolated backup restore passed; all table fingerprints match; no production volume mounted')
    finally:
        if created:
            run(['docker', 'rm', '-f', '-v', name], stdout=subprocess.DEVNULL)

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else ''
    if action in ('recovery-issue', 'recovery-revoke'):
        if len(sys.argv) != 3:
            raise ValueError('Use recovery-issue USERNAME | recovery-revoke USERNAME')
        recovery(action, sys.argv[2])
        return
    if action == 'verify-restore' and len(sys.argv) == 2:
        verify_restore()
        return
    if action == 'test-recovery' and len(sys.argv) == 2:
        test_recovery()
        return
    if action == 'install-secrets' and len(sys.argv) == 2:
        install_secrets()
        return
    if action == 'restore-initial' and len(sys.argv) == 4:
        restore_initial(sys.argv[2], sys.argv[3])
        return
    if action == 'database-fingerprint' and len(sys.argv) == 3:
        database_fingerprint(release(sys.argv[2]))
        return
    if action == 'database-summary' and len(sys.argv) == 3:
        database_summary(release(sys.argv[2]))
        return
    if action == 'confirm-data' and len(sys.argv) == 3:
        if (ROOT / 'current').exists():
            raise ValueError('Initial data confirmation refused after deployment')
        database_summary(release(sys.argv[2]))
        DATA_READY.write_text(sys.argv[2] + '\n')
        return
    if action == 'install-tools' and len(sys.argv) == 3:
        install_tools(release(sys.argv[2]))
        return
    if action == 'enable' and len(sys.argv) == 2:
        ready(release())
        run(['systemctl', 'enable', 'bussassistent.service', 'cloudflared.service', 'bussassistent-backup.timer'])
        # ExecStart takes the same operation lock; queue startup without waiting on ourselves.
        run(['systemctl', 'start', '--no-block', 'bussassistent.service', 'cloudflared.service', 'bussassistent-backup.timer'])
        return
    if action == 'reboot' and len(sys.argv) == 2:
        run(['shutdown', '-r', '+1', 'Bussassistent planned restart verification'])
        return
    if action == 'stage' and len(sys.argv) == 4:
        stage(sys.argv[2], sys.argv[3])
        return
    if action == 'status':
        run(['systemctl', 'show', 'bussassistent', 'cloudflared',
             '-p', 'Id', '-p', 'ActiveState', '-p', 'SubState'])
        if (ROOT / 'current').exists():
            path = release()
            print('Release: ' + path.name, flush=True)
            compose(path, 'ps')
        return
    if action == 'logs':
        # Unit status only; journal may contain client metadata, never tokens.
        run(['journalctl', '-u', 'bussassistent', '-u', 'cloudflared',
             '--no-pager', '-n', '60'])
        return
    if action == 'prepare-db' and len(sys.argv) == 3:
        if (ROOT / 'current').exists():
            raise ValueError('Initial database setup refused: current release exists')
        path = release(sys.argv[2])
        compose(path, 'up', '-d', '--no-build', '--wait', 'private-db')
        print('Database ready for controlled restore; app and tunnel not started')
        return
    if action in ('deploy', 'rollback') and len(sys.argv) == 3:
        target = release(sys.argv[2])
        previous = release() if (ROOT / 'current').exists() else None
        if previous is None and not DATA_READY.is_file():
            raise ValueError('First deploy requires verified restore and root-owned data-ready marker')
        if action == 'rollback' and (previous is None or migrations(previous) != migrations(target)):
            raise ValueError('Rollback requires identical migration files; use reviewed database restore otherwise')
        # Builds and config validation happen before downtime.
        compose(target, 'config', '--quiet')
        for service in ('api', 'gateway', 'access-gate'):
            run(['docker', 'image', 'inspect', 'bussassistent-' + service + ':' + target.name],
                stdout=subprocess.DEVNULL)
        tunnel_was_active = subprocess.run(
            ['systemctl', 'is-active', '--quiet', 'cloudflared']).returncode == 0
        run(['systemctl', 'stop', 'cloudflared'])
        if previous:
            compose(previous, 'stop', 'gateway', 'private-api', 'access-gate')
            backup(previous)
            link('previous', previous)
        link('current', target)
        try:
            start(target)
        except Exception:
            # A migration may have happened. Do not restart old code automatically.
            print('Deployment failed; tunnel remains stopped. Inspect before rollback.', file=sys.stderr)
            raise
        if tunnel_was_active:
            run(['systemctl', 'start', '--no-block', 'cloudflared'])
        print('Active release: ' + target.name)
        return
    path = release()
    if action == 'start':
        start(path)
    elif action == 'stop':
        compose(path, 'stop', '--timeout', '45')
    elif action == 'backup':
        backup(path)
    elif action == 'check':
        ready(path)
    else:
        raise ValueError('Use status|logs|start|stop|backup|check|stage SHA DIGEST|prepare-db SHA|deploy SHA|rollback SHA')


def entrypoint():
    if os.geteuid() != 0:
        raise SystemExit('Run through sudo')
    with open('/run/lock/bussassistent.lock', 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            main()
        except (ValueError, OSError, subprocess.CalledProcessError) as error:
            # Do not dump Compose environments, credentials or database contents.
            raise SystemExit(str(error)) from None


if __name__ == '__main__':
    entrypoint()
