"""Read-only O3/O4/O6 receipts. No interactive authentication or configuration writes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import socket
import time
import shlex

from gateway_deploy import SSH

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/evidence/o3-o5-night-20261102'
EXIT_CODES = []


def remote_controls(commands):
    lines = ['failed=0']
    for index, command in enumerate(commands):
        lines.extend([f"printf '\\nCONTROL {index}\\n'", 'sh -c ' + shlex.quote(command),
            'result=$?', f"printf 'CONTROL_EXIT {index}=%s\\n' \"$result\"",
            '[ "$result" -eq 0 ] || failed=1'])
    return '\n'.join([*lines, 'exit "$failed"'])


def capture(name, args):
    target = OUT / (name + '.txt')
    if target.exists() or target.with_suffix('.json').exists():
        raise RuntimeError('Receipt already exists')
    start = datetime.now(timezone.utc).isoformat()
    timed_out = False
    try:
        p = subprocess.run(args, cwd=ROOT, stdin=subprocess.DEVNULL, capture_output=True, timeout=90)
        data, code = p.stdout + p.stderr, p.returncode
    except subprocess.TimeoutExpired as error:
        data, code, timed_out = (error.stdout or b'') + (error.stderr or b''), 124, True
    with target.open('xb') as output:
        output.write(data)
    metadata = json.dumps(dict(
        command=args, start_utc=start, end_utc=datetime.now(timezone.utc).isoformat(),
        exit=code, timed_out=timed_out, sha256=hashlib.sha256(data).hexdigest()), indent=2) + '\n'
    with target.with_suffix('.json').open('x', encoding='utf-8') as output:
        output.write(metadata)
    EXIT_CODES.append(code)
    print(name, 'exit', code)


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    phase = sys.argv[1]
    if phase == 'network':
        code = remote_controls([
            'date --iso-8601=seconds', 'ss -lntH', 'ip -4 addr show scope global',
            'ip -6 addr show scope global', 'ip -4 route', 'ip -6 route',
            'sysctl net.ipv6.conf.all.disable_ipv6 net.ipv6.bindv6only',
            'sudo -n ufw status verbose', 'sudo -n nft list ruleset',
            'sudo -n iptables-save', 'sudo -n ip6tables-save',
            "curl -sS -o /dev/null -w 'origin_without_assertion=%{http_code}\\n' --max-time 5 -H 'Host: app.bussassistent.com' http://127.0.0.1:18081/private",
        ])
        capture(sys.argv[2] if len(sys.argv) > 2 else 'network-host', SSH + [code])
    elif phase == 'stability':
        code = remote_controls([
            'date --iso-8601=seconds', 'cat /opt/bussassistent/current/release-identity.json',
            'cat /proc/sys/kernel/random/boot_id', 'uptime', 'uname -r',
            'systemctl --failed --no-pager',
            'systemctl show cloudflared -p MainPID -p NRestarts -p ActiveEnterTimestamp',
            'systemctl list-timers bussassistent-backup.timer --no-pager',
            'systemctl show bussassistent-backup.service -p Result -p ExecMainStatus -p ActiveEnterTimestamp',
            'curl -fsS --max-time 5 http://127.0.0.1:18083/ready',
            'sudo -n /usr/local/sbin/bussassistentctl check',
            'sudo -n /usr/local/sbin/bussassistentctl status',
        ])
        capture(sys.argv[2], SSH + [code])
    elif phase == 'edge':
        # Only regular unauthenticated HTTPS requests; Cloudflare IPs are not origin targets.
        prefix = sys.argv[2] if len(sys.argv) > 2 else 'edge'
        for index, path in enumerate(['/private', '/private-api/auth/session', '/private-api/drafts', '/private-api/workdays']):
            capture(prefix + '-' + str(index), ['curl.exe', '-sS', '--max-time', '15', '-o', 'NUL',
                '-w', 'status=%{http_code}\n', 'https://app.bussassistent.com' + path])
    elif phase == 'origin-host':
        capture('origin-host-corrected', SSH + [
            "curl -sS -o /dev/null -w 'origin_without_assertion=%{http_code}\\n' --max-time 5 -H 'Host: app.bussassistent.com' http://127.0.0.1:18081/private"])
    elif phase == 'lan':
        # Addresses belong to the server confirmed by strict-key SSH/ip output.
        rows = []
        for host in ['192.168.1.138', 'fd11:a8d8:a24a:80c7:ca3d:d4ff:fe7e:afa5']:
            for port in [22, 18081, 18083, 8000, 5432, 8081]:
                started = time.monotonic()
                try:
                    with socket.create_connection((host, port), timeout=.5):
                        result = 'connected'
                except OSError as error:
                    result = type(error).__name__ + ':' + str(error.errno)
                rows.append(dict(host=host, port=port, result=result,
                    elapsed_seconds=round(time.monotonic()-started, 3)))
        target = OUT / 'lan.json'
        if target.exists(): raise RuntimeError('Receipt already exists')
        target.write_text(json.dumps(dict(time_utc=datetime.now(timezone.utc).isoformat(),
            vantage='same LAN Windows; not independent WAN', observations=rows), indent=2) + '\n')
        print('lan', len(rows), 'bounded TCP connection checks')
    else:
        raise SystemExit('Unknown phase')
    sys.exit(1 if any(EXIT_CODES) else 0)
