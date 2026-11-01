"""Reproducible isolated O5 gate qualification; existing images only, no pulls."""
import sys
import json
import subprocess
from uuid import uuid4
from night_controls import ROOT, OUT, EXIT_CODES, capture

if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    label = sys.argv[1]
    image = sys.argv[2] if len(sys.argv) > 2 else 'ibe160-o5-gate-tests:20261102'
    name = 'ibe160-o5-night-qualification-' + uuid4().hex
    args = ['docker', 'run', '--rm', '--pull', 'never', '--name', name,
        '--network', 'none', '--dns', '127.0.0.1', '--dns-option', 'timeout:30', '--dns-option', 'attempts:5',
        '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges:true',
        '--pids-limit', '32', '--user', '10001:10001', '--tmpfs', '/tmp:rw,nosuid,nodev,size=1m,mode=1777',
        '--mount', f'type=bind,source={ROOT}/deploy/tablet/access_gate,target=/gate-tests,readonly',
        '--mount', f'type=bind,source={ROOT}/scripts/operations-followup,target=/repo/scripts/operations-followup,readonly',
        '-e', 'O5_LIBC_DNS=1', '-e', 'PYTHONPATH=/gate:/gate-tests:/repo/scripts/operations-followup', '-w', '/gate', image,
        'python', '-m', 'pytest', '-q', '-rP', '-p', 'no:cacheprovider', '--import-mode=importlib',
        '/gate-tests/test_gate.py', '/gate-tests/test_bounded_gate.py', '/gate-tests/test_gate_http.py',
        '/gate-tests/test_resolver_process.py', '/gate-tests/test_libc_dns.py',
        '/gate-tests/test_https_keys.py', '/repo/scripts/operations-followup/test_night_controls.py']
    try:
        capture(label, args)
    finally:
        # A client timeout does not stop Docker's container. Always clean up
        # only this invocation's unique name, including failed/timed-out runs.
        cleanup = subprocess.run(['docker', 'rm', '-f', name], capture_output=True, timeout=10)
        with (OUT / (label + '-cleanup.json')).open('x', encoding='utf-8') as output:
            json.dump(dict(container=name, exit=cleanup.returncode,
                stdout=cleanup.stdout.decode(errors='replace'),
                stderr=cleanup.stderr.decode(errors='replace')), output, indent=2)
    sys.exit(1 if any(EXIT_CODES) else 0)
