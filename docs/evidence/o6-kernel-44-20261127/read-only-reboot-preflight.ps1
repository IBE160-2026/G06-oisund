# Owner-run O6 read-only preflight for 44.44. No maintenance actions or server config writes.
# sudo enables OS/backup metadata reads and existing health checks; enter any
# password locally at its prompt. Never share passwords or private key material.
$ErrorActionPreference = 'Stop'
$python = @'
import datetime as dt
import json
import os
import pathlib as P
import re
import subprocess as S

os.environ['LC_ALL'] = 'C'
os.environ['PATH'] = '/usr/sbin:/usr/bin:/sbin:/bin'
command_errors = []
def emit(label, value):
    print(label + '=' + json.dumps(value, ensure_ascii=True), flush=True)
def run(args):
    try:
        p = S.run(args, capture_output=True, text=True, timeout=30)
        if p.returncode:
            command_errors.append(args[0] + ':exit=' + str(p.returncode))
            emit('COMMAND_ERROR', {'command': args[0], 'exit': p.returncode})
        if p.stderr.strip():
            # These commands read OS metadata only; omit arbitrary journal text.
            emit('COMMAND_DIAGNOSTIC', p.stderr.strip()[:600])
        return p.stdout
    except (OSError, S.TimeoutExpired) as e:
        command_errors.append(args[0] + ':' + type(e).__name__)
        emit('COMMAND_ERROR', {'command': args[0], 'type': type(e).__name__})
        return ''
def read(path):
    try:
        return P.Path(path).read_text(errors='replace')
    except OSError as e:
        emit('READ_ERROR', {'path': str(path), 'errno': e.errno})
        return ''
def stamp(value):
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()
def meta(path):
    try:
        p = P.Path(path)
        s = p.lstat()
        return {'name': p.name, 'mtime_utc': stamp(s.st_mtime), 'bytes': s.st_size,
                'mode': oct(s.st_mode & 0o7777), 'symlink': p.is_symlink()}
    except OSError as e:
        return {'name': P.Path(path).name, 'errno': e.errno}

emit('CHECK_TIME', dt.datetime.now().astimezone().isoformat())
emit('ACTIVE_KERNEL', os.uname().release)
emit('VERSION_SIGNATURE', read('/proc/version_signature').strip())
emit('ARCHITECTURE', run(['dpkg', '--print-architecture']).strip())
for line in run(['dpkg-query', '-W', '-f=${db:Status-Abbrev}\t${binary:Package}\t${Version}\t${Architecture}\n', 'linux-*']).splitlines():
    if re.search(r'\tlinux-(image|modules|headers|generic)', line):
        emit('KERNEL_PACKAGE', line)
audit_errors_before = len(command_errors)
audit = run(['dpkg', '--audit']).strip()
emit('DPKG_AUDIT', {'command_completed': len(command_errors) == audit_errors_before, 'reported_issues': audit})
emit('KERNEL_HOLDS', [x for x in run(['apt-mark', 'showhold']).splitlines() if x.startswith('linux-')])
packages = ['linux-generic', 'linux-image-generic', 'linux-headers-generic',
            'linux-image-' + os.uname().release, 'linux-image-7.0.0-44-generic',
            'linux-modules-7.0.0-44-generic', 'linux-modules-extra-7.0.0-44-generic',
            'linux-headers-7.0.0-44-generic']
for line in run(['apt-cache', 'policy'] + list(dict.fromkeys(packages))).splitlines():
    if re.match(r'^\S[^ ]*:$|^\s+(Installed|Candidate):', line):
        print('APT_POLICY ' + line.strip())
for p in [P.Path('/var/lib/apt/periodic/update-success-stamp')]:
    emit('APT_UPDATE_STAMP', meta(p))
for p in sorted(P.Path('/var/lib/apt/lists').glob('*InRelease')):
    t = read(p)
    fields = dict(re.findall(r'^(Origin|Suite|Codename|Date|Valid-Until):\s*(.*)$', t, re.M))
    if fields.get('Origin') == 'Ubuntu':
        emit('UBUNTU_INDEX', dict(fields, mtime_utc=stamp(p.stat().st_mtime)))
for suite in ['resolute', 'resolute-updates', 'resolute-security']:
    rows = list(P.Path('/var/lib/apt/lists').glob('*_dists_' + suite + '_main_binary-amd64_Packages*'))
    emit('APT_PACKAGE_INDEX', {'suite': suite, 'count': len(rows),
         'mtimes_utc': sorted(stamp(p.stat().st_mtime) for p in rows)})
emit('APT_NOTE', 'Local cached metadata only; no apt update performed. Index mtime is not proof of last successful refresh.')

for p in [P.Path('/etc/default/grub')] + sorted(P.Path('/etc/default/grub.d').glob('*.cfg')):
    for line in read(p).splitlines():
        if re.match(r'^\s*GRUB_(DEFAULT|SAVEDEFAULT|TIMEOUT|TIMEOUT_STYLE)=', line):
            emit('GRUB_INPUT', {'file': str(p), 'setting': line.strip()})
for line in run(['grub-editenv', '/boot/grub/grubenv', 'list']).splitlines():
    if re.match(r'^(saved_entry|next_entry|prev_saved_entry|recordfail|initrdfail)=', line):
        emit('GRUB_ENV', line)
cfg = read('/boot/grub/grub.cfg')
emit('GRUB_CFG_META', meta('/boot/grub/grub.cfg'))
for line in cfg.splitlines():
    if re.match(r'^\s*set default=', line):
        emit('GRUB_GENERATED_DEFAULT', line.strip())
    if re.match(r'^\s*(menuentry|submenu)\s', line):
        emit('GRUB_ENTRY', line.strip())
    m = re.match(r'^\s*(?:linux|linuxefi|initrd|initrdefi)\s+(\S+)', line)
    if m:
        emit('GRUB_BOOT_PATH', m.group(1))  # Deliberately omit kernel arguments.
for p in sorted(P.Path('/boot').glob('vmlinuz-*')) + sorted(P.Path('/boot').glob('initrd.img-*')):
    emit('BOOT_ARTIFACT', meta(p))
if P.Path('/sys/firmware/efi').exists():
    efi = run(['efibootmgr'])
    lines = efi.splitlines()
    wanted = set(re.findall(r'^Boot(?:Current|Next):\s*([0-9A-Fa-f]{4})', efi, re.M))
    for line in lines:
        if re.match(r'^Boot(Current|Next|Order):', line) or any(line.startswith('Boot' + n) for n in wanted):
            emit('EFI_SELECTION', line)
else:
    emit('EFI_SELECTION', 'not an EFI boot')
emit('BOOT_NOTE', 'Expected next kernel must be resolved from generated default + next_entry/saved_entry + menu order + EFI override; not inferred from newest package or symlink. Manual boot selection remains possible.')
emit('REBOOT_REQUIRED', P.Path('/run/reboot-required').exists())
if P.Path('/run/reboot-required.pkgs').exists():
    emit('REBOOT_REQUIRED_PACKAGES', read('/run/reboot-required.pkgs').splitlines())

timer = 'bussassistent-backup.timer'
unit = 'bussassistent-backup.service'
def properties(unit, names):
    out = run(['systemctl', 'show', unit] + ['--property=' + n for n in names])
    return dict(x.split('=', 1) for x in out.splitlines() if '=' in x)
emit('BACKUP_TIMER', properties(timer, ['LoadState', 'ActiveState', 'SubState', 'Unit',
     'LastTriggerUSec', 'NextElapseUSecRealtime', 'TimersCalendar', 'Persistent', 'RandomizedDelayUSec']))
emit('BACKUP_SERVICE', properties(unit, ['LoadState', 'ActiveState', 'SubState', 'Result',
     'ExecMainCode', 'ExecMainStatus', 'ExecMainStartTimestamp', 'ExecMainExitTimestamp', 'InvocationID']))
exec_start = properties(unit, ['ExecStart']).get('ExecStart', '')
emit('BACKUP_COMMAND_MATCHES_EXPECTED', bool(re.search(r'argv\[\]=/usr/local/sbin/bussassistentctl backup\s*;', exec_start)))
events = []
dump_pattern = r'/var/backups/bussassistent/[0-9]{8}T[0-9]{6}Z-[a-f0-9]{40}\.dump'
for line in run(['journalctl', '--no-pager', '-u', unit, '--since=30 days ago', '-n', '2000', '-o', 'json']).splitlines():
    try:
        row = json.loads(line)
        message = row.get('MESSAGE', '')
        if not isinstance(message, str):
            continue
        result = row.get('JOB_RESULT') or row.get('UNIT_RESULT')
        dump = re.fullmatch(dump_pattern, message)
        if result or dump or ('Finished ' + unit) in message or ('Failed ' + unit) in message:
            event = {'time_utc': stamp(int(row['__REALTIME_TIMESTAMP']) / 1000000)}
            if result:
                event['result'] = result
                event['job_type'] = row.get('JOB_TYPE')
            if dump:
                event['completed_dump'] = P.Path(message).name
                event['file'] = meta(message)
            if ('Finished ' + unit) in message:
                event['systemd_finished'] = True
            if ('Failed ' + unit) in message:
                event['systemd_failed'] = True
            events.append(event)
    except (ValueError, KeyError, TypeError):
        emit('JOURNAL_PARSE_ERROR', 'one row unreadable')
for event in events[-10:]:
    emit('BACKUP_EVENT', event)
successful_jobs = [e for e in events if e.get('systemd_finished') or
                   (e.get('result') == 'done' and e.get('job_type') == 'start')]
emit('LAST_SUCCESSFUL_BACKUP_JOB', successful_jobs[-1] if successful_jobs else
     'Not established within available 30-day/2000-record journal window')
if not events:
    emit('BACKUP_EVENT', 'No matching result in available journal: last 30 days, at most 2000 records. Not proof of no backups.')
try:
    files = [p for p in P.Path('/var/backups/bussassistent').iterdir()
             if re.fullmatch(r'[0-9]{8}T[0-9]{6}Z-[a-f0-9]{40}\.dump', p.name)]
    for p in sorted(files, key=lambda p: p.lstat().st_mtime, reverse=True)[:3]:
        emit('RECENT_DUMP_METADATA', meta(p))
    emit('RECENT_DUMP_COUNT', len(files))
except OSError as e:
    emit('BACKUP_METADATA_ERROR', {'errno': e.errno})
emit('BACKUP_NOTE', 'Correlate timer trigger, service start/exit/result, journal completion and dump metadata. A manual run is not automatically a timer run. File presence or active timer alone is not success. No backup or restore was run; older restore evidence remains historical.')
# Additional targeted, read-only preflight. Never invoke backup/start/reboot.
emit('UPTIME', run(['uptime']).strip())
emit('BOOT_TIME', run(['uptime', '-s']).strip())
emit('ACTIVE_RELEASE', os.path.realpath('/opt/bussassistent/current'))
target = '7.0.0-44-generic'
emit('TARGET_KERNEL', target)
emit('BOOT_SPACE', run(['df', '-Pk', '/boot', '/boot/efi']).strip())
for package in ['linux-image-' + target, 'linux-modules-' + target]:
    before = len(command_errors)
    result = run(['dpkg', '--verify', package]).strip()
    emit('PACKAGE_VERIFY', {'package': package, 'command_completed': len(command_errors) == before,
         'reported_differences': result})
before = len(command_errors)
initramfs = run(['lsinitramfs', '/boot/initrd.img-' + target])
emit('TARGET_INITRAMFS', {'read_completed': len(command_errors) == before,
     'module_tree_present': any('/lib/modules/' + target + '/' in '/' + x for x in initramfs.splitlines()),
     'contains_init': any(x in ['init', './init'] for x in initramfs.splitlines())})
emit('INITRAMFS_NOTE', 'Listing is a structural check, not a boot test. Boot selection and root/storage drivers still require review.')
for field in ['GRUB_DISABLE_RECOVERY', 'GRUB_ENABLE_CRYPTODISK']:
    for line in read('/etc/default/grub').splitlines():
        if re.match(r'^\s*' + field + '=', line):
            emit('GRUB_EXTRA', line.strip())
emit('ROOT_STORAGE', run(['findmnt', '-rn', '-o', 'SOURCE,FSTYPE', '/']).strip())
for unit_name in ['bussassistent.service', 'docker.service', 'cloudflared.service']:
    emit('SERVICE', dict(unit=unit_name, **properties(unit_name, ['LoadState', 'ActiveState', 'SubState',
         'Result', 'ExecMainStatus', 'ExecMainStartTimestamp', 'NRestarts'])))
emit('FAILED_UNITS', run(['systemctl', '--failed', '--no-legend', '--no-pager', '--plain']).strip())
containers = run(['docker', 'ps', '-a', '--filter', 'label=com.docker.compose.project=bussassistent',
                  '--format', '{{.ID}}\t{{.Label "com.docker.compose.service"}}'])
found = set()
expected = {'private-db', 'private-api', 'gateway', 'access-gate'}
for row in containers.splitlines():
    fields = row.split('\t')
    if len(fields) != 2 or not re.fullmatch(r'[a-f0-9]{12,64}', fields[0]):
        continue
    cid, service = fields
    if service not in expected:
        continue
    found.add(service)
    fmt = '{{.Image}}\t{{.State.Status}}\t{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}\t{{.State.Restarting}}\t{{.State.OOMKilled}}\t{{.RestartCount}}'
    emit('CONTAINER', {'service': service, 'fields': 'image_id/status/health/restarting/oom_killed/restarts',
         'status': run(['docker', 'inspect', '--format', fmt, cid]).strip()})
    if service == 'private-db':
        emit('DATABASE_READINESS', run(['docker', 'exec', cid, 'pg_isready', '-U', 'private_work', '-d', 'private_work']).strip())
emit('MISSING_CONTAINERS', sorted(expected - found))
# The existing check command performs API and loopback origin-access checks.
# Its output is allowlisted; no Compose environment, logs or credentials are emitted.
try:
    check = S.run(['/usr/local/sbin/bussassistentctl', 'check'], capture_output=True, text=True, timeout=45)
    expected_message = 'API healthy; origin access control rejects unauthenticated requests'
    emit('APP_AND_ORIGIN_CHECK', {'exit': check.returncode, 'expected_success_message': expected_message in check.stdout})
    if check.returncode:
        command_errors.append('app/origin check')
except (OSError, S.TimeoutExpired) as e:
    command_errors.append('app/origin check')
    emit('APP_AND_ORIGIN_CHECK', {'error': type(e).__name__})
emit('TUNNEL_LOCAL_READY_HTTP', run(['curl', '--noproxy', '*', '-sS', '--max-time', '10',
     '-o', '/dev/null', '-w', '%{http_code}', 'http://127.0.0.1:18083/ready']).strip())
emit('COLLECTION_ERRORS', command_errors)
emit('DECISION', 'Pending review of boot selection, complete target packages, fresh successful backup and health. No automatic approval or reboot. Historical restore evidence is separate.')

'@
$encoded = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($python))
$sshOptions = @('-t', '-i', (Join-Path $env:USERPROFILE '.ssh/ibe160_server_ed25519'),
    '-o', 'IdentitiesOnly=yes', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
    '-o', 'HostKeyAlias=192.168.1.139', '-o', 'ConnectTimeout=10')
# Base64 transfers this visible script as data without PowerShell/SSH quote damage.
# sudo reads a possible password from the TTY, not the piped Python source.
& ssh @sshOptions jonas@192.168.1.138 "printf %s $encoded | base64 -d | sudo python3 -"
if ($LASTEXITCODE -ne 0) { throw "Read-only SSH collection failed (exit $LASTEXITCODE)." }
