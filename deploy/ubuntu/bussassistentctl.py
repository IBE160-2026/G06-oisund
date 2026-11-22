#!/usr/bin/python3
"""Root-owned operations for one isolated Compose project. No secret output."""
from datetime import date
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
import stat
import unicodedata
import uuid

ROOT = Path('/opt/bussassistent')
CONFIG = Path('/etc/bussassistent/server.env')
DATA_READY = Path('/etc/bussassistent/data-ready')
UPLOADS = Path('/home/jonas/ibe160-upload')
BACKUPS = Path('/var/backups/bussassistent')
MAINTENANCE = Path('/etc/bussassistent/maintenance')
SHA = re.compile(r'[a-f0-9]{40}')
RESTORE_OPERATION = re.compile(r'[a-f0-9]{32}')
RESTORE_SETTING = 'bussassistent.restore_operation'
FINGERPRINT_VERSION = 2
INITIAL_EMPTY_CHECK = """NOT EXISTS (
    SELECT 1 FROM pg_depend
    WHERE refclassid = 'pg_namespace'::regclass AND refobjid = 'public'::regnamespace
) AND NOT EXISTS (
    SELECT 1 FROM pg_namespace
    WHERE nspname NOT IN ('public', 'pg_catalog', 'information_schema', 'pg_toast')
      AND nspname !~ '^pg_(toast_)?temp_[0-9]+$'
)"""
TUNNEL_UNIT = Path('/etc/systemd/system/cloudflared.service')
TUNNEL_CONDITION = 'ConditionPathExists=!/etc/bussassistent/maintenance/pending.json'
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


def import_routes(path, first, last):
    start, end = (date.fromisoformat(value) for value in (first, last))
    if not 0 <= (end - start).days < 14 or any(
        value != parsed.isoformat() for value, parsed in ((first, start), (last, end))
    ):
        raise ValueError('Use one to 14 consecutive route dates in YYYY-MM-DD')
    if (MAINTENANCE / 'pending.json').exists():
        raise ValueError('Route import blocked during database restoration')
    helper = path / 'deploy/ubuntu/public_route_download.py'
    result = run([sys.executable, str(helper)], stdout=subprocess.PIPE, timeout=105)
    compose(path, 'exec', '-T', 'private-api', 'python', '-m', 'app.route_catalogue',
            '--bundle-stdin', '--from-date', first, '--through-date', last, '--publish',
            input=result.stdout, timeout=240)


def import_road_area(path):
    normal_operation()
    compose(path, 'exec', '-T', 'private-api', 'python', '-m', 'app.road_area_catalogue',
            '--bundle-stdin', '--publish', stdin=sys.stdin.buffer, timeout=120)


def fetch_public(path, module, *arguments, timeout):
    name = 'bussassistent-public-' + uuid.uuid4().hex
    try:
        return run(['docker', 'run', '--rm', '--name', name, '--pull=never', '--network', 'bridge',
                    '--user', '10001:10001', '--read-only', '--tmpfs', '/tmp:size=64m,mode=1777',
                    '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges:true',
                    'bussassistent-api:' + path.name, 'python', '-m', module, *arguments],
                   stdout=subprocess.PIPE, timeout=timeout).stdout
    except subprocess.TimeoutExpired:
        subprocess.run(['docker', 'rm', '-f', name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
        raise


def refresh_road_situations(path):
    normal_operation()
    payload = fetch_public(path, 'app.road_situation_source', '--fetch', timeout=40)
    compose(path, 'exec', '-T', 'private-api', 'python', '-m', 'app.road_situation_source', '--publish-stdin',
            input=payload, timeout=30)


def refresh_road_area(path, if_needed=False):
    normal_operation()
    if if_needed:
        state = compose(path, 'exec', '-T', 'private-api', 'python', '-m', 'app.road_area_catalogue',
                        '--ready-day', stdout=subprocess.PIPE, timeout=30)
        if json.loads(state.stdout)['ready'] is True:
            return
    payload = fetch_public(path, 'app.road_area_refresh', timeout=125)
    compose(path, 'exec', '-T', 'private-api', 'python', '-m', 'app.road_area_catalogue',
            '--bundle-stdin', '--publish', input=payload, timeout=120)


def refresh_public_notices(path):
    normal_operation()
    module = 'app.public_notice_bundle'
    reserved = compose(path, 'exec', '-T', 'private-api', 'python', '-m', module, '--reserve',
                       stdout=subprocess.PIPE, timeout=30)
    started = json.loads(reserved.stdout)['started_at']
    if started is None:
        return
    payload = fetch_public(path, module, '--fetch', '--started-at', started, timeout=235)
    compose(path, 'exec', '-T', 'private-api', 'python', '-m', module, '--publish-stdin', input=payload, timeout=40)


def recovery(action, username):
    """Bounded operator entry point; check OUTER terminal before Docker's PTY."""
    if (action not in ('recovery-issue', 'recovery-revoke')
            or any(c == '\x00' or '\ud800' <= c <= '\udfff' for c in username)):
        raise ValueError('Invalid recovery command or username')
    normalized = username.strip().casefold()
    removed = username[:len(username) - len(username.lstrip())] + username[len(username.rstrip()):]
    if (len(username) > 400 or not 1 <= len(normalized) <= 100
            or any(unicodedata.category(char).startswith('C') for char in removed)):
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
                'python', '-m', 'app.manage', action, normalized,
                stdin=terminal, stdout=terminal, stderr=terminal)
    finally:
        os.close(terminal)

def verify_release_images(path):
    """Check every resolved image before downtime, including a built PG overlay.

    Reading Compose also supports older releases that use a registry-pinned DB.
    No pull or build occurs during deploy/rollback's preflight.
    """
    images = compose(path, 'config', '--images', capture_output=True, text=True).stdout.splitlines()
    if not images or any(not image.strip() for image in images):
        raise ValueError('Release has no complete image inventory')
    for image in sorted(set(images)):
        run(['docker', 'image', 'inspect', image], stdout=subprocess.DEVNULL)


def link(name, path):
    temporary = ROOT / (name + '.new')
    temporary.unlink(missing_ok=True)
    temporary.symlink_to(path)
    temporary.replace(ROOT / name)


def migrations(path):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (path / 'backend/migrations/private').glob('*.sql')}


def backup(path, prune=True):
    if prune:
        prune_restore_copies()
    BACKUPS.mkdir(mode=0o750, parents=True, exist_ok=True)
    stamp = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    target = BACKUPS / (stamp + '-' + path.name + '.dump')
    if target.exists():
        raise ValueError('Backup timestamp already exists; retry later')
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
        if prune and old.is_file() and not old.is_symlink() and old.stat().st_mtime < time.time() - 172800:
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
    normal_operation()
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
    if not re.fullmatch(r'[a-f0-9]{64}', digest):
        raise ValueError('Invalid dump digest')
    path = release(commit)
    journal = CONFIG.parent / 'initial-restore.json'
    receipt = CONFIG.parent / 'initial-quarantined.json'
    state = None
    if journal.exists() or journal.is_symlink():
        state = read_restore_metadata(journal)
        if (state['release'] != path.name or state['sha256'] != digest
                or not RESTORE_OPERATION.fullmatch(state['operation'])):
            raise ValueError('Initial restore does not match the prepared release and archive')
    if receipt.exists() or receipt.is_symlink():
        if state is None:
            raise ValueError('An earlier initial restore is already recorded')
        verify_initial_quarantine(path)
        print('Initial restore already quarantined; app and tunnel remain stopped')
        return
    operation = state['operation'] if state else uuid.uuid4().hex
    client = 'bussassistent-restore-replacement-' + operation
    if state:
        remove_restore_client(client)
    current_marker = database_restore_marker(path)
    if state is None or current_marker != operation:
        if current_marker or restore_query(path, 'SELECT (' + INITIAL_EMPTY_CHECK + ')') != 't':
            raise ValueError('Restore requires an empty database; existing data will not be overwritten')
        with tempfile.TemporaryDirectory(prefix='initial-restore-', dir=ROOT) as temporary:
            directory = Path(temporary)
            snapshot_restore_source(UPLOADS / 'initial.dump', directory, digest, require_root=False)
            expected = preflight_restore(path, directory / 'source.dump', directory, operation, require_empty=True)
            if state and state['business'] != expected['business']:
                raise ValueError('Initial restore preflight differs from the prepared archive')
            state = {'operation': operation, 'release': path.name, 'sha256': digest, 'business': expected['business']}
            durable_json(journal, state)
            replace_restore_database(path, directory, client)
        if database_restore_marker(path) != operation:
            raise ValueError('Initial restore transaction is unrecognized')
    if offline(path, 'restore-inspect')['business'] != state['business']:
        raise ValueError('Initial restore business equivalence failed')
    offline(path, 'migrate')
    if offline(path, 'restore-inspect')['business'] != state['business']:
        raise ValueError('Initial restore business equivalence failed')
    quarantined = offline(path, 'restore-quarantine')
    checked = offline(path, 'restore-verify')
    if checked['business'] != state['business'] or checked['authority_fingerprint'] != quarantined['authority_fingerprint']:
        raise ValueError('Initial restore quarantine failed')
    durable_json(receipt, {'release': path.name, 'authority_fingerprint': checked['authority_fingerprint']})
    print('Initial restore quarantined; app and tunnel remain stopped')


def database_summary(path):
    # Counts/runtime metadata only, no identities, row contents or credentials.
    sql = """SELECT 'accounts=' || count(*) FROM accounts;
SELECT 'migrations=' || count(*) FROM private_migrations;
SELECT 'drafts=' || count(*) FROM drafts;
SELECT 'workdays=' || count(*) FROM workdays;
SELECT 'server_version=' || current_setting('server_version');
SELECT 'database_locale=' || json_build_object('provider', datlocprovider,
 'collate', datcollate, 'ctype', datctype, 'version', datcollversion,
 'actual', pg_database_collation_actual_version(oid))::text
 FROM pg_database WHERE datname=current_database();
SELECT 'extension=' || extname || ':' || extversion FROM pg_extension ORDER BY extname;"""
    compose(path, 'exec', '-T', 'private-db', 'psql', '-U', 'tablet_bootstrap',
            '-d', 'private_work', '-Atc', sql)


def fingerprint_sql(version=FINGERPRINT_VERSION):
    if version == 1:
        # A restore begun by the preceding helper can leave a durable receipt.
        rows = 'FROM public.%I t'
        digest = "md5(coalesce(string_agg(row_to_json(t)::text, chr(10) ORDER BY row_to_json(t)::text), ''))"
    else:
        # Sort fixed-size hashes instead of concatenating the full catalogue JSON.
        rows = """FROM (SELECT sha256(convert_to(row_to_json(t)::text, 'UTF8')) AS row_digest
                           FROM public.%I t) AS rows"""
        digest = "md5(coalesce(string_agg(row_digest, ''::bytea ORDER BY row_digest), ''::bytea))"
    return f"""CREATE TEMP TABLE fingerprints(table_name text, row_count bigint, digest text);
DO $body$
DECLARE r record;
BEGIN
  FOR r IN SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename LOOP
    EXECUTE format($fmt$
      INSERT INTO fingerprints SELECT %L, count(*), {digest}
      {rows}
    $fmt$, r.tablename, r.tablename);
  END LOOP;
END $body$;
SELECT * FROM fingerprints ORDER BY table_name;"""


def database_fingerprint(path, capture=False, *, version=FINGERPRINT_VERSION):
    return compose(path, 'exec', '-T', 'private-db', 'psql', '-U', 'tablet_bootstrap',
                   '-d', 'private_work', '-qAtc', fingerprint_sql(version), capture_output=capture, text=capture)

def install_tools(path):
    import shutil
    MAINTENANCE.mkdir(mode=0o755, parents=True, exist_ok=True)
    if MAINTENANCE.is_symlink() or MAINTENANCE.stat().st_uid != 0:
        raise ValueError('Unsafe maintenance directory')
    MAINTENANCE.chmod(0o755)
    for name in ('bussassistent.service', 'cloudflared.service',
                 'bussassistent-backup.service', 'bussassistent-backup.timer',
                 'bussassistent-road-situations.service', 'bussassistent-road-situations.timer',
                 'bussassistent-road-area.service', 'bussassistent-road-area.timer',
                 'bussassistent-public-notices.service', 'bussassistent-public-notices.timer'):
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


def gateway_snapshot(path):
    """Allowlisted lifecycle identity, never Env, credentials, logs or DB rows."""
    result = {}
    for service in ('private-api', 'access-gate', 'private-db', 'gateway'):
        ident = compose(path, 'ps', '-q', service, capture_output=True, text=True).stdout.strip()
        record = json.loads(run(['docker', 'inspect', ident], capture_output=True, text=True).stdout)[0]
        if (record['Config']['Labels'].get('com.docker.compose.project') != 'bussassistent'
                or record['Config']['Labels'].get('com.docker.compose.service') != service
                or not record['State']['Running']):
            raise ValueError('Expected running production service: ' + service)
        result[service] = {'id': record['Id'], 'image': record['Image'],
            'pid': record['State']['Pid'], 'started': record['State']['StartedAt'],
            'restarts': record['RestartCount']}
    result['tunnel'] = run(['systemctl', 'show', 'cloudflared', '-p', 'MainPID', '-p', 'NRestarts',
                            '-p', 'ActiveEnterTimestamp'], capture_output=True, text=True).stdout
    result['boot_id'] = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
    return result


def gateway_source_guard(before, target):
    def files(path, relative):
        base = path / relative
        if not base.exists():
            raise ValueError('Missing gateway scope input: ' + relative)
        paths = [base] if base.is_file() else base.rglob('*')
        return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in paths if p.is_file()}
    for relative in ('backend', 'frontend', 'deploy/tablet/access_gate',
                     'deploy/tablet/nginx-main.conf', 'deploy/tablet/nginx.conf.template'):
        if files(before, relative) != files(target, relative):
            raise ValueError('Gateway-only scope rejects changed ' + relative)
    # Only release directory / generated app image aliases may differ in Compose.
    def configuration(path):
        value = compose(path, 'config', '--format', 'json', capture_output=True, text=True).stdout
        return json.loads(value.replace(str(path), '<release>').replace(path.name, '<sha>'))
    if configuration(before) != configuration(target):
        raise ValueError('Gateway-only scope rejects changed Compose/runtime configuration')


def gateway_switch(commit, expected_image, expected_current):
    if not re.fullmatch(r'sha256:[a-f0-9]{64}', expected_image):
        raise ValueError('Exact gateway image ID required')
    before = release()
    target = release(commit)
    if before.name != expected_current or target == before:
        raise ValueError('Active release changed or target already active')
    gateway_source_guard(before, target)
    gateway_ref = 'bussassistent-gateway:' + target.name
    image = json.loads(run(['docker', 'image', 'inspect', gateway_ref], capture_output=True, text=True).stdout)[0]['Id']
    if image != expected_image:
        raise ValueError('Gateway image differs from qualified artifact')
    ready(before)
    wait_tunnel()
    initial = gateway_snapshot(before)
    backup(before)
    # Stage may build temporary app images. They must never be activated by this
    # operation or a later start: bind new aliases to the exact running images.
    for service, prefix in (('private-api', 'api'), ('access-gate', 'access-gate')):
        run(['docker', 'tag', initial[service]['image'], 'bussassistent-' + prefix + ':' + target.name])
    try:
        compose(target, 'up', '-d', '--no-deps', '--no-build', '--pull', 'never', 'gateway')
        for attempt in range(15):
            try:
                ready(target)
                break
            except (ValueError, subprocess.CalledProcessError):
                if attempt == 14:
                    raise
                time.sleep(1)
        compose(target, 'exec', '-T', 'gateway', 'nginx', '-t')
        wait_tunnel()
        final = gateway_snapshot(target)
        for key in ('private-api', 'access-gate', 'private-db', 'tunnel', 'boot_id'):
            if initial[key] != final[key]:
                raise ValueError('Unrelated production lifecycle changed: ' + key)
        if final['gateway']['image'] != expected_image:
            raise ValueError('Running gateway differs from qualified artifact')
    except Exception:
        # Same application/migrations/DB, so only the gateway is returned.
        compose(before, 'up', '-d', '--no-deps', '--no-build', '--pull', 'never', 'gateway')
        ready(before)
        wait_tunnel()
        restored = gateway_snapshot(before)
        for key in ('private-api', 'access-gate', 'private-db', 'tunnel', 'boot_id'):
            if initial[key] != restored[key]:
                raise ValueError('Unrelated lifecycle changed during gateway recovery: ' + key)
        if restored['gateway']['image'] != initial['gateway']['image']:
            raise ValueError('Previous gateway image not restored')
        print('Gateway returned to previous release; no app/DB/tunnel restart requested', flush=True)
        raise
    link('previous', before)
    link('current', target)
    receipt = {'before_commit': before.name, 'active_commit': target.name,
               'qualified_gateway_image': expected_image, 'before': initial, 'after': final,
               'scope': 'gateway only; app image aliases preserve running bytes'}
    (target / 'gateway-maintenance.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


def gateway_export(commit):
    path = release(commit)
    ref = 'bussassistent-gateway:' + path.name
    target = UPLOADS / ('gateway-' + path.name + '.tar')
    with target.open('xb') as stream:
        run(['docker', 'save', ref], stdout=stream)
    import grp
    os.chown(target, 0, grp.getgrnam('jonas').gr_gid)
    target.chmod(0o640)
    with target.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    print(json.dumps({'path': str(target), 'sha256': digest, 'bytes': target.stat().st_size}))

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

def normal_operation():
    if (MAINTENANCE / 'pending.json').exists():
        raise ValueError('Restore pending; normal operation is inhibited')


def durable_json(path, value):
    temporary = path.with_suffix('.new')
    with temporary.open('w') as stream:
        json.dump(value, stream, sort_keys=True)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.chmod(0o600)
    temporary.replace(path)
    sync_directory(path.parent)


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def read_restore_metadata(path):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
        raise ValueError('Unsafe restore state')
    return json.loads(path.read_text())


def restore_state():
    state = read_restore_metadata(MAINTENANCE / 'pending.json')
    if (not SHA.fullmatch(state['release']) or not RESTORE_OPERATION.fullmatch(state['operation'])
            or state.get('fingerprint_version', 1) not in (1, FINGERPRINT_VERSION)
            or state['stage'] not in {'prepared', 'closed', 'replacing', 'replaced', 'quarantined', 'retaining', 'verified', 'opening', 'ingress-committed'}):
        raise ValueError('Invalid restore state')
    if release().name != state['release']:
        raise ValueError('Restore release changed')
    return state


def save_restore(state, stage):
    state['stage'] = stage
    durable_json(MAINTENANCE / 'pending.json', state)


def offline(path, action):
    if action not in {'migrate', 'cleanup', 'restore-inspect', 'restore-quarantine', 'restore-verify'}:
        raise ValueError('Invalid offline restore action')
    name = 'bussassistent-restore-offline-' + uuid.uuid4().hex
    try:
        result = compose(path, 'run', '--rm', '--no-deps', '-T', '--name', name,
            '-e', 'PGOPTIONS=-c lock_timeout=5s -c statement_timeout=120s -c transaction_timeout=120s',
            'private-api', 'python', '-m', 'app.manage', action, capture_output=True, text=True, timeout=180)
        return json.loads(result.stdout) if action.startswith('restore-') else None
    finally:
        # A timed-out Compose CLI does not necessarily stop its one-off container.
        # Remove only the unique name assigned by this invocation (no socket is
        # mounted into the one-off); normal --rm completion makes this a no-op.
        subprocess.run(['docker', 'rm', '-f', name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)


def has_tunnel_condition(source):
    """Recognize the configured condition only as an active Unit directive."""
    section = ''
    conditions = set()
    for line in source.splitlines():
        line = line.strip()
        if line.startswith(('#', ';')):
            continue
        if line.startswith('[') and line.endswith(']'):
            section = line
        elif section == '[Unit]':
            key, separator, value = line.partition('=')
            key, value = key.strip(), value.strip()
            if separator and key.startswith('Condition'):
                if not value:
                    conditions.clear()
                else:
                    conditions.add(key + '=' + value)
    return TUNNEL_CONDITION in conditions


def restore_guards(path):
    """Old installed containers without a persistent startup guard are ineligible."""
    for service in ('private-api', 'gateway', 'access-gate'):
        ident = compose(path, 'ps', '-a', '-q', service, capture_output=True, text=True).stdout.strip()
        record = json.loads(run(['docker', 'inspect', ident], capture_output=True, text=True).stdout)[0]
        if (record['Config']['Labels'].get('com.docker.compose.project') != 'bussassistent'
                or record['Config']['Labels'].get('com.docker.compose.service') != service
                or not any(m['Destination'] == '/maintenance' and m['Source'] == str(MAINTENANCE)
                           and m['Type'] == 'bind' and not m['RW'] for m in record['Mounts'])
                or '/maintenance/pending.json' not in ' '.join(record['Config']['Cmd'] or [])):
            raise ValueError('Installed restore guards required')
    result = run(['systemctl', 'show', 'cloudflared.service', '-p', 'FragmentPath', '-p',
                  'DropInPaths', '-p', 'NeedDaemonReload'], capture_output=True, text=True, timeout=30)
    properties = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    if (properties.get('FragmentPath') != str(TUNNEL_UNIT) or properties.get('DropInPaths') != ''
            or properties.get('NeedDaemonReload') != 'no' or not has_tunnel_condition(TUNNEL_UNIT.read_text())):
        raise ValueError('Installed tunnel restore guard required')


def close_restore(path):
    (MAINTENANCE / 'local-start').unlink(missing_ok=True)
    sync_directory(MAINTENANCE)
    run(['systemctl', 'stop', 'cloudflared'], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=45)
    # Do not stop bussassistent.service: its ExecStop takes our operation lock.
    compose(path, 'stop', '--timeout', '45', 'gateway', 'private-api', 'access-gate',
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=150)
    running = compose(path, 'ps', '--status', 'running', '--services', capture_output=True, text=True).stdout.splitlines()
    if set(running) - {'private-db'}:
        raise ValueError('Restore writers remain')
    result = subprocess.run(['systemctl', 'is-active', '--quiet', 'cloudflared'])
    if result.returncode == 0:
        raise ValueError('Restore ingress remains')
    compose(path, 'up', '-d', '--no-deps', '--no-build', '--pull', 'never', '--wait',
            '--wait-timeout', '90', 'private-db', stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=120)
    # Established clients cannot survive unnoticed, including offline jobs.
    clients = compose(path, 'exec', '-T', 'private-db', 'psql', '-U', 'tablet_bootstrap',
        '-d', 'private_work', '-Atc', "SELECT count(*) FROM pg_stat_activity WHERE datname=current_database() AND pid<>pg_backend_pid()",
        capture_output=True, text=True).stdout.strip()
    if clients != '0':
        raise ValueError('Restore database clients remain')


def restore_query(path, sql):
    return compose(path, 'exec', '-T', 'private-db', 'psql', '-X', '-U', 'tablet_bootstrap',
                   '-d', 'private_work', '-v', 'ON_ERROR_STOP=1', '-qAtc', sql,
                   capture_output=True, text=True, timeout=30).stdout.strip()


def database_restore_marker(path):
    return restore_query(path, """
        SELECT split_part(setting, '=', 2)
        FROM pg_db_role_setting, unnest(setconfig) AS setting
        WHERE setrole = 0
          AND setdatabase = (SELECT oid FROM pg_database WHERE datname = current_database())
          AND split_part(setting, '=', 1) = '""" + RESTORE_SETTING + "'")


def remove_restore_client(name):
    subprocess.run(['docker', 'rm', '-f', name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)


def replace_restore_database(path, directory, name):
    try:
        with (directory / 'replacement.sql').open('rb') as stream:
            compose(path, 'run', '--rm', '--no-deps', '-T', '--name', name,
                    'private-db', '/bin/sh', '-ec',
                    'export PGPASSWORD="$(cat /run/secrets/tablet_bootstrap_password)"; '
                    'exec psql -X -h private-db -U tablet_bootstrap -d private_work -v ON_ERROR_STOP=1',
                    stdin=stream, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=180)
    finally:
        remove_restore_client(name)


def restore_sql(path, archive, destination, operation=None, *, require_empty=False):
    """Single SQL transaction replaces the entire public schema, including newer tables."""
    with archive.open('rb') as stream:
        contents = compose(path, 'exec', '-T', 'private-db', 'pg_restore', '--list',
                           stdin=stream, capture_output=True).stdout.decode()
    body = destination.with_suffix('.body')
    try:
        with archive.open('rb') as stream, body.open('xb') as output:
            compose(path, 'exec', '-T', 'private-db', 'pg_restore', '--no-owner', '--no-privileges',
                    '--file=-', stdin=stream, stdout=output, stderr=subprocess.PIPE, timeout=180)
        with destination.open('xb') as output:
            write_restore_sql(output, body, contents, operation, require_empty=require_empty)
    finally:
        body.unlink(missing_ok=True)


def write_restore_sql(output, body, contents, operation=None, *, require_empty=False):
    limits = b"SET LOCAL lock_timeout='5s';\nSET LOCAL statement_timeout='120s';\nSET LOCAL transaction_timeout='120s';\n"
    output.write(b'BEGIN;\n' + limits)
    if require_empty:
        output.write(("DO $guard$ BEGIN IF NOT (" + INITIAL_EMPTY_CHECK + ") THEN "
                      "RAISE EXCEPTION 'Initial restore requires an empty database'; END IF; END $guard$;\n").encode())
    output.write(b'DROP SCHEMA public CASCADE;\n')
    if not re.search(r' SCHEMA - public ', contents):
        output.write(b'CREATE SCHEMA public AUTHORIZATION private_work;\n')
    output.write(b'SET LOCAL ROLE private_work;\n')
    # pg_restore emits timeout=0 header settings. Never let those cancel
    # the bounded transaction; leave object definitions and COPY data intact.
    header = True
    with body.open('rb') as stream:
        for line in stream:
            if line.startswith(b'-- Name:'):
                header = False
            if header and re.match(rb'SET (lock_timeout|statement_timeout|transaction_timeout) = ', line):
                continue
            output.write(line)
    if operation is not None:
        if not RESTORE_OPERATION.fullmatch(operation):
            raise ValueError('Invalid restore transaction marker')
        # Database settings are transactional, outside the restored public schema,
        # and excluded from ordinary pg_dump archives made without --create.
        output.write(("\nRESET ROLE;\nALTER DATABASE private_work SET " + RESTORE_SETTING
                      + " = '" + operation + "';\n").encode())
    output.write(b'\nCOMMIT;\n')
    output.flush()
    os.fsync(output.fileno())


def preflight_restore(path, archive, directory, operation=None, *, require_empty=False):
    """Execute source and migration checks in a networkless disposable DB, no production volume."""
    config = json.loads(compose(path, 'config', '--format', 'json', capture_output=True, text=True).stdout)
    db_image = config['services']['private-db']['image']
    api_image = config['services']['private-api']['image']
    name = 'bussassistent-restore-preflight-' + uuid.uuid4().hex
    created = False
    try:
        run(['docker', 'run', '-d', '--name', name, '--network', 'none', '--memory', '512m',
             '--pids-limit', '128', '--tmpfs', '/var/lib/postgresql/data:rw,size=512m',
             '-e', 'POSTGRES_HOST_AUTH_METHOD=trust', '-e', 'POSTGRES_USER=tablet_bootstrap',
             '-e', 'POSTGRES_DB=private_work', db_image], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        created = True
        for attempt in range(45):
            if subprocess.run(['docker', 'exec', name, 'pg_isready', '-h', '127.0.0.1',
                               '-U', 'tablet_bootstrap', '-d', 'private_work'],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                break
            time.sleep(1)
        else:
            raise ValueError('Restore preflight database unavailable')
        run(['docker', 'exec', name, 'psql', '-U', 'tablet_bootstrap', '-d', 'private_work',
             '-v', 'ON_ERROR_STOP=1', '-c', 'CREATE ROLE private_work LOGIN',
             '-c', 'ALTER DATABASE private_work OWNER TO private_work'], capture_output=True)
        restore_sql(path, archive, directory / 'replacement.sql', operation, require_empty=require_empty)
        with (directory / 'replacement.sql').open('rb') as stream:
            run(['docker', 'exec', '-i', name, 'psql', '-X', '-U', 'tablet_bootstrap', '-d', 'private_work',
                 '-v', 'ON_ERROR_STOP=1'], stdin=stream, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=180)
        def check(action):
            check_name = 'bussassistent-restore-check-' + uuid.uuid4().hex
            try:
                result = run(['docker', 'run', '--rm', '--name', check_name, '--network', 'container:' + name,
                '--user', '10001:10001', '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
                '--pids-limit', '128', '--tmpfs', '/tmp:rw,size=32m',
                '-e', 'APP_MODE=private-local', '-e', 'PRIVATE_DATABASE_URL=postgresql://private_work@localhost/private_work',
                '-e', 'PRIVATE_DATABASE_PASSWORD_FILE=/run/db-password',
                '-e', 'PGOPTIONS=-c lock_timeout=5s -c statement_timeout=120s -c transaction_timeout=120s',
                '--mount', 'type=bind,source=' + str(CONFIG.parent / 'secrets/postgres-password') + ',target=/run/db-password,readonly',
                    api_image, 'python', '-m', 'app.manage', action], capture_output=True, text=True, timeout=180)
                return json.loads(result.stdout) if action != 'migrate' else None
            finally:
                subprocess.run(['docker', 'rm', '-f', check_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        original = check('restore-inspect')
        original['database_fingerprint'] = run(['docker', 'exec', name, 'psql', '-U', 'tablet_bootstrap',
            '-d', 'private_work', '-qAtc', fingerprint_sql()], capture_output=True, text=True).stdout
        check('migrate')
        migrated = check('restore-inspect')
        if original['business'] != migrated['business']:
            raise ValueError('Restore migration changed business data')
        check('restore-quarantine')
        check('restore-verify')
        def schema():
            value = run(['docker', 'exec', name, 'pg_dump', '-U', 'tablet_bootstrap', '-d', 'private_work',
                         '--schema-only', '--no-owner', '--no-acl'], capture_output=True, text=True).stdout
            # pg_dump 17.6+ emits random psql restrict keys. They are not schema.
            return '\n'.join(line for line in value.splitlines()
                             if not line.startswith(('\\restrict ', '\\unrestrict ', '--')))
        restored_schema = schema()
        run(['docker', 'exec', name, 'psql', '-U', 'tablet_bootstrap', '-d', 'private_work',
             '-v', 'ON_ERROR_STOP=1', '-c', 'DROP SCHEMA public CASCADE; CREATE SCHEMA public AUTHORIZATION private_work'],
            capture_output=True)
        check('migrate')
        if schema() != restored_schema:
            raise ValueError('Restore schema differs from supported release')
        return original
    finally:
        if created:
            run(['docker', 'rm', '-f', '-v', name], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def remove_restore_copies(directory):
    # Exact, root-owned operation children only; never traverse links or recurse.
    if directory.is_symlink() or directory.parent != ROOT / 'restore' or not re.fullmatch(r'[a-f0-9]{32}', directory.name):
        raise ValueError('Unsafe restore storage')
    for name in ('source.dump', 'prior.dump', 'replacement.sql', 'replacement.body'):
        child = directory / name
        if child.exists() or child.is_symlink():
            info = child.lstat()
            if not stat.S_ISREG(info.st_mode) or info.st_uid != 0:
                raise ValueError('Unsafe restore copy')
            child.unlink()
    sync_directory(directory)


def prune_restore_copies():
    base = ROOT / 'restore'
    if not base.exists():
        return
    pending = restore_state()['operation'] if (MAINTENANCE / 'pending.json').exists() else None
    for directory in base.iterdir():
        if (directory.name == pending or directory.is_symlink() or not directory.is_dir()
                or directory.stat().st_uid != 0 or not re.fullmatch(r'[a-f0-9]{32}', directory.name)):
            continue
        receipt = directory / 'completed.json'
        completed = receipt.is_file() and not receipt.is_symlink()
        aged = (receipt.stat().st_mtime if completed else directory.stat().st_mtime) < time.time() - 172800
        if aged and (completed or not receipt.exists()):
            remove_restore_copies(directory)


def snapshot_restore_source(source, directory, digest, *, require_root=True):
    import shutil
    fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
                or (require_root and (info.st_uid != 0 or info.st_mode & 0o022))):
            raise ValueError('Unsafe restore source')
        with (directory / 'source.dump').open('xb') as output:
            shutil.copyfileobj(stream, output)
            output.flush()
            os.fsync(output.fileno())
    with (directory / 'source.dump').open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != digest:
            raise ValueError('Restore source digest mismatch')


def begin_restore(basename, digest, expected_release):
    normal_operation()
    if not re.fullmatch(r'\d{8}T\d{6}Z-[a-f0-9]{40}\.dump', basename) or not re.fullmatch(r'[a-f0-9]{64}', digest):
        raise ValueError('Invalid restore source identity')
    path = release(expected_release)
    if path != release():
        raise ValueError('Restore release mismatch')
    verify_release_images(path)
    restore_guards(path)
    operation = uuid.uuid4().hex
    directory = ROOT / 'restore' / operation
    directory.mkdir(parents=True, mode=0o700)
    try:
        snapshot_restore_source(BACKUPS / basename, directory, digest)
        expected = preflight_restore(path, directory / 'source.dump', directory, operation)
    except BaseException:
        remove_restore_copies(directory)
        directory.rmdir()
        sync_directory(directory.parent)
        raise
    sync_directory(directory)
    sync_directory(directory.parent)
    sync_directory(ROOT)
    source_fingerprint = expected.pop('database_fingerprint')
    state = {'operation': operation, 'release': path.name, 'source': basename, 'sha256': digest,
             'expected': expected, 'source_fingerprint': source_fingerprint, 'attempts': 0,
             'stage': 'prepared', 'transaction_marker': True, 'fingerprint_version': FINGERPRINT_VERSION}
    save_restore(state, 'prepared')
    resume_restore()


def resume_restore():
    state = restore_state()
    fingerprint_version = state.get('fingerprint_version', 1)
    path, directory = release(), ROOT / 'restore' / state['operation']
    if state['stage'] in {'verified', 'opening', 'ingress-committed'}:
        raise ValueError('Restore already verified; use restore-reopen')
    replacement_name = 'bussassistent-restore-replacement-' + state['operation']
    # Handles a previous helper crash before querying transaction outcome.
    remove_restore_client(replacement_name)
    close_restore(path)
    if state['stage'] == 'prepared':
        # Never prune the selected source while capturing the pre-replacement copy.
        prior = backup(path, prune=False)
        state['prior_fingerprint'] = database_fingerprint(path, capture=True, version=fingerprint_version).stdout
        if state.get('transaction_marker'):
            state['prior_marker'] = database_restore_marker(path)
        import shutil
        shutil.copyfile(prior, directory / 'prior.dump')
        with (directory / 'prior.dump').open('rb') as stream:
            os.fsync(stream.fileno())
        sync_directory(directory)
        save_restore(state, 'closed')
    if state['stage'] == 'replacing':
        current = database_fingerprint(path, capture=True, version=fingerprint_version).stdout
        if state.get('transaction_marker'):
            # The marker commits with schema, rows and sequence state. Equal
            # table digests alone cannot distinguish commit from rollback.
            marker = database_restore_marker(path)
            committed = marker == state['operation'] and current == state['source_fingerprint']
            rolled_back = marker == state['prior_marker'] and current == state['prior_fingerprint']
        else:
            # Older prepared operations have no marker. Only disjoint row
            # outcomes are recognizable; equal digests require investigation.
            committed = current == state['source_fingerprint'] and current != state['prior_fingerprint']
            rolled_back = current == state['prior_fingerprint'] and current != state['source_fingerprint']
        if committed:
            save_restore(state, 'replaced')
        elif rolled_back and state['attempts'] < 3:
            save_restore(state, 'closed')
        else:
            raise ValueError('Restore replacement needs offline investigation')
    if state['stage'] == 'closed':
        state['attempts'] += 1
        save_restore(state, 'replacing')
        replace_restore_database(path, directory, replacement_name)
        if state.get('transaction_marker') and database_restore_marker(path) != state['operation']:
            raise ValueError('Restore replacement needs offline investigation')
        save_restore(state, 'replaced')
    if state['stage'] == 'replaced':
        offline(path, 'migrate')
        if offline(path, 'restore-inspect')['business'] != state['expected']['business']:
            raise ValueError('Restore business equivalence failed')
        state['authority_fingerprint'] = offline(path, 'restore-quarantine')['authority_fingerprint']
        save_restore(state, 'quarantined')
    if state['stage'] == 'quarantined':
        checked = offline(path, 'restore-verify')
        if (checked['business'] != state['expected']['business']
                or checked['authority_fingerprint'] != state['authority_fingerprint']):
            raise ValueError('Restore quarantine verification failed')
        # Equivalence is established before applying normal retention policy.
        save_restore(state, 'retaining')
    if state['stage'] == 'retaining':
        # Cleanup commits bounded per-account batches. Its durable stage makes
        # retry idempotent after interruption without demanding expired rows
        # already removed by a completed batch reappear.
        if offline(path, 'restore-verify')['authority_fingerprint'] != state['authority_fingerprint']:
            raise ValueError('Restore authority changed during retention')
        offline(path, 'cleanup')
        state['retained'] = offline(path, 'restore-verify')['business']
        save_restore(state, 'verified')
    print('Restore verified; ingress remains closed; explicit restore-reopen required')


def reopen_restore():
    pending = MAINTENANCE / 'pending.json'
    receipt = MAINTENANCE / 'last-restore.json'
    state = restore_state() if pending.exists() else read_restore_metadata(receipt)
    if state['stage'] not in {'verified', 'opening', 'ingress-committed', 'completed'}:
        raise ValueError('Restore is not ready for reopening')
    path = release()
    if state['release'] != path.name:
        raise ValueError('Restore release changed')
    if state['stage'] == 'completed':
        print('Restore reopening was already completed')
        return
    if state['stage'] != 'ingress-committed':
        close_restore(path)
        checked = offline(path, 'restore-verify')
        if (checked['authority_fingerprint'] != state['authority_fingerprint']
                or (state['stage'] == 'verified' and checked['business'] != state['retained'])):
            raise ValueError('Restore reopening verification failed')
        # Startup may apply normal retention. An opening retry preserves that
        # completed cleanup instead of comparing against stale business rows.
        save_restore(state, 'opening')
        permit = MAINTENANCE / 'local-start'
        with permit.open('w') as stream:
            stream.write('Local readiness only; tunnel remains inhibited\n')
            stream.flush()
            os.fsync(stream.fileno())
        permit.chmod(0o644)
        sync_directory(MAINTENANCE)
        try:
            compose(path, 'up', '-d', '--no-build', '--pull', 'never', '--wait', '--wait-timeout', '180')
            ready(path)
        except BaseException:
            close_restore(path)
            raise
        # Durable final authorization precedes any tunnel traffic. After this
        # point retries are connectivity-only, never old fingerprint checks.
        save_restore(state, 'ingress-committed')
    if pending.exists():
        durable_json(ROOT / 'restore' / state['operation'] / 'completed.json', state)
        durable_json(receipt, {
            key: state[key] for key in ('operation', 'release', 'stage', 'attempts')})
        pending.unlink()
        (MAINTENANCE / 'local-start').unlink(missing_ok=True)
        sync_directory(MAINTENANCE)
    start(path)
    run(['systemctl', 'start', '--no-block', 'cloudflared'])
    wait_tunnel()
    durable_json(receipt, {**{key: state[key] for key in ('operation', 'release', 'attempts')}, 'stage': 'completed'})
    print('Restore reopened; each account requires a fresh independent recovery code')


def restore_status():
    pending = (MAINTENANCE / 'pending.json').exists()
    receipt = MAINTENANCE / 'last-restore.json'
    if not pending and not receipt.exists():
        return
    state = restore_state() if pending else read_restore_metadata(receipt)
    stage = state['stage']
    next_action = None
    if pending or (stage == 'ingress-committed' and (ROOT / 'current').exists() and release().name == state['release']):
        next_action = 'restore-reopen' if stage in {'verified', 'opening', 'ingress-committed'} else 'restore-resume'
    print(json.dumps({'restore': {key: state[key] for key in ('operation', 'stage', 'attempts')},
        'ingress_committed': stage in {'ingress-committed', 'completed'}, 'next_action': next_action}))


def verify_initial_quarantine(path):
    receipt = read_restore_metadata(CONFIG.parent / 'initial-quarantined.json')
    if receipt['release'] != path.name or receipt['authority_fingerprint'] != offline(path,'restore-verify')['authority_fingerprint']:
        raise ValueError('Initial restore quarantine confirmation required')


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else ''
    if action == 'restore' and len(sys.argv) == 5:
        begin_restore(*sys.argv[2:])
        return
    if action in {'restore-resume', 'restore-reopen'} and len(sys.argv) == 2:
        {'restore-resume': resume_restore, 'restore-reopen': reopen_restore}[action]()
        return
    if action not in {'status', 'logs', 'stop'}:
        normal_operation()
    if action in ('recovery-issue', 'recovery-revoke'):
        if len(sys.argv) != 3:
            raise ValueError('Use recovery-issue USERNAME | recovery-revoke USERNAME')
        recovery(action, sys.argv[2])
        return

    if action == 'gateway-switch' and len(sys.argv) == 5:
        gateway_switch(*sys.argv[2:])
        return
    if action == 'gateway-export' and len(sys.argv) == 3:
        gateway_export(sys.argv[2])
        return
    if action == 'gateway-inspect' and len(sys.argv) == 3:
        path = release(sys.argv[2])
        ref = 'bussassistent-gateway:' + path.name
        image = json.loads(run(['docker', 'image', 'inspect', ref], capture_output=True, text=True).stdout)[0]
        print(json.dumps({'current': release().name, 'production': gateway_snapshot(release()),
                          'staged_gateway': {k: image[k] for k in ('Id', 'Architecture', 'Os', 'RootFS')}}))
        return
    if action == 'import-routes' and len(sys.argv) == 4:
        import_routes(release(), sys.argv[2], sys.argv[3])
        return
    if action == 'import-road-area' and len(sys.argv) == 2:
        import_road_area(release())
        return
    if action == 'refresh-road-situations' and len(sys.argv) == 2:
        refresh_road_situations(release())
        return
    if action == 'road-situation-status' and len(sys.argv) == 2:
        compose(release(), 'exec', '-T', 'private-api', 'python', '-m', 'app.road_situation_source', '--status', timeout=30)
        return
    if action == 'enable-road-situations' and len(sys.argv) == 2:
        path = release()
        refresh_road_situations(path)
        run(['systemctl', 'enable', '--now', 'bussassistent-road-situations.timer'])
        return
    if action == 'refresh-road-area' and len(sys.argv) == 2:
        refresh_road_area(release())
        return
    if action == 'ensure-road-area' and len(sys.argv) == 2:
        refresh_road_area(release(), if_needed=True)
        return
    if action == 'enable-road-area' and len(sys.argv) == 2:
        path = release()
        refresh_road_area(path, if_needed=True)
        run(['systemctl', 'enable', '--now', 'bussassistent-road-area.timer'])
        return
    if action == 'refresh-public-notices' and len(sys.argv) == 2:
        refresh_public_notices(release())
        return
    if action == 'enable-public-notices' and len(sys.argv) == 2:
        path = release()
        refresh_public_notices(path)
        run(['systemctl', 'enable', '--now', 'bussassistent-public-notices.timer'])
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
        path = release(sys.argv[2])
        verify_initial_quarantine(path)
        database_summary(path)
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
        restore_status()
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
        if previous is None:
            verify_initial_quarantine(target)
        if action == 'rollback' and (previous is None or migrations(previous) != migrations(target)):
            raise ValueError('Rollback requires identical migration files; use reviewed database restore otherwise')
        # Builds and config validation happen before downtime.
        compose(target, 'config', '--quiet')
        verify_release_images(target)
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
        except (ValueError, OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
            # Do not dump Compose environments, credentials or database contents.
            if len(sys.argv) > 1 and sys.argv[1].startswith('restore'):
                raise SystemExit('Restore operation failed; ingress remains inhibited if pending. Inspect the durable stage.') from None
            raise SystemExit(str(error)) from None


if __name__ == '__main__':
    entrypoint()
