"""Production build + task-only browser gate, with immutable per-run evidence."""
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
from datetime import datetime, timezone

root = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding='utf-8')
run = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + secrets.token_hex(6)
record = {'run': run, 'commands': [], 'source_sha256': {}}
evidence = root / 'docs' / 'evidence' / f'12-2-frontend-{run}.json'
try:
    files = list((root/'frontend/src').rglob('*')) + [root/'frontend/tests/fictional-assessment.spec.ts', Path(__file__)]
    files += [p for p in (root/'frontend').iterdir() if p.is_file()]
    record['source_sha256'] = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file()}
    for name, args in [('npm', ['run', 'build']), ('npx', ['playwright', 'test', '--config', 'playwright.story122.config.ts'])]:
        executable = shutil.which(name + ('.cmd' if os.name == 'nt' else ''))
        result = subprocess.run([executable, *args], cwd=root/'frontend', capture_output=True, text=True, encoding='utf-8', errors='replace')
        record['commands'].append({'command': [name, *args], 'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
        print(result.stdout)
        if result.returncode:
            print(result.stderr)
            raise SystemExit(result.returncode)
    record['build_sha256'] = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'frontend/dist').rglob('*') if p.is_file()}
finally:
    evidence.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Evidence:', evidence)
