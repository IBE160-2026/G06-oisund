"""Explicit O5 release phases through the established authorized operator CLI.

Receipts exclude credentials and row contents. Never performs an implicit deploy.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from gateway_deploy import SSH as EXISTING_SSH

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/evidence/o5-deploy-20261102'
SSH = EXISTING_SSH[:-1] + ['-o', 'ServerAliveInterval=15', '-o', 'ServerAliveCountMax=2'] + EXISTING_SSH[-1:]
OLD = '5e521cbc658594a47c4568d352a50e46309573c4'
TARGET = '7921eb54e4816aaab9368c3efd851bcf692f3823'


def capture(name, args, timeout=120):
    OUT.mkdir(exist_ok=True)
    target = OUT / (name + '.txt')
    metadata = target.with_suffix('.json')
    if target.exists() or metadata.exists():
        raise RuntimeError('Receipt already exists: ' + name)
    start = datetime.now(timezone.utc).isoformat()
    timed_out = False
    try:
        result = subprocess.run(args, cwd=ROOT, stdin=subprocess.DEVNULL,
            capture_output=True, timeout=timeout)
        data, code = result.stdout + result.stderr, result.returncode
    except subprocess.TimeoutExpired as error:
        data = (error.stdout or b'') + (error.stderr or b'')
        code, timed_out = 124, True
    with target.open('xb') as output: output.write(data)
    with metadata.open('x', encoding='utf-8') as output:
        json.dump(dict(command=args, start_utc=start, end_utc=datetime.now(timezone.utc).isoformat(),
            exit=code, timed_out=timed_out, sha256=hashlib.sha256(data).hexdigest()), output, indent=2)
    print(name, 'exit', code, flush=True)
    if code: raise RuntimeError('Phase failed; inspect receipt before continuing: ' + name)
    return data.decode(errors='replace')


def health(name):
    code = '\n'.join(['set -eu', 'date --iso-8601=seconds',
        'cat /opt/bussassistent/current/release-identity.json',
        'readlink -f /opt/bussassistent/previous', 'cat /proc/sys/kernel/random/boot_id',
        'uname -r', 'uptime', 'systemctl --failed --no-pager',
        'systemctl show cloudflared -p MainPID -p NRestarts -p ActiveEnterTimestamp',
        'systemctl is-active bussassistent-backup.timer',
        'curl -fsS --max-time 10 http://127.0.0.1:18083/ready',
        'sudo -n /usr/local/sbin/bussassistentctl check',
        'sudo -n /usr/local/sbin/bussassistentctl status'])
    capture(name, SSH + [code])


if __name__ == '__main__':
    phase = sys.argv[1]
    if phase == 'health': health(sys.argv[2])
    elif phase == 'backup':
        capture(sys.argv[2], ['pwsh','-NoProfile','-File','scripts/server.ps1','-Action','Backup'])
    elif phase == 'restore':
        capture(sys.argv[2], SSH + ['sudo -n /usr/local/sbin/bussassistentctl verify-restore'])
    elif phase == 'fingerprint':
        revision = sys.argv[3]
        if revision not in (OLD, TARGET): raise ValueError('Explicit qualified revision required')
        capture(sys.argv[2], SSH + ['sudo -n /usr/local/sbin/bussassistentctl database-fingerprint ' + revision])
    elif phase == 'inspect':
        revision = sys.argv[3]
        if revision not in (OLD, TARGET): raise ValueError('Explicit qualified revision required')
        capture(sys.argv[2], SSH + ['sudo -n /usr/local/sbin/bussassistentctl gateway-inspect ' + revision])
    elif phase == 'stage':
        capture('stage', ['pwsh','-NoProfile','-File','scripts/server.ps1',
            '-Action','GatewayStage','-Revision',TARGET], timeout=1200)
    elif phase == 'deploy':
        # Recheck identity immediately before the explicitly authorized switch.
        code = ('set -eu\ntest "$(readlink -f /opt/bussassistent/current)" = /opt/bussassistent/releases/' + OLD +
            '\nsudo -n /usr/local/sbin/bussassistentctl deploy ' + TARGET)
        capture('deploy', SSH + [code], timeout=300)
    elif phase == 'edge':
        import urllib.error
        import urllib.request
        from urllib.parse import urlsplit
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args): return None
        opener = urllib.request.build_opener(NoRedirect)
        rows = []
        for path in ['/private','/private-api/auth/session','/private-api/drafts','/private-api/workdays']:
            request = urllib.request.Request('https://app.bussassistent.com' + path)
            try: response = opener.open(request, timeout=15)
            except urllib.error.HTTPError as error: response = error
            with response:
                location = urlsplit(response.headers.get('Location', ''))
                rows.append(dict(path=path, status=response.status,
                    cache_control=response.headers.get('Cache-Control'),
                    location_host=location.hostname, location_path=location.path))
        with (OUT/'external-unauthenticated.json').open('x',encoding='utf-8') as output:
            json.dump(dict(time_utc=datetime.now(timezone.utc).isoformat(),
                no_authentication_or_cookies_supplied=True, redirects_followed=False,
                observations=rows), output, indent=2)
        assert all('no-store' in (r['cache_control'] or '') and (
            (r['status']==302 and (r['location_host'] or '').endswith('.cloudflareaccess.com'))
            or (r['status']==403 and r['location_host'] is None)) for r in rows)
        print('PASS four unauthenticated edge refusals, no-store, no private body inspected')
    else: raise SystemExit('Explicit supported phase required')
