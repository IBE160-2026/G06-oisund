"""Read-only candidate source checks; never loads container environment or secrets."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import urllib.request
import uuid
from datetime import datetime, timezone

root = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())
def output(*args):
    return subprocess.check_output(args, cwd=root, encoding='utf-8').strip()
def digest(data):
    return hashlib.sha256(data).hexdigest()
record = {'at': datetime.now(timezone.utc).isoformat(), 'scope': 'read-only isolated candidate images, loopback static assets and health; no private API payloads or environment', 'images': {}, 'served': {}}
for tag, local, remote in [
    ('ibe160-v1followup-gate:20261029-r1', 'deploy/tablet/access_gate/gate.py', '/gate/gate.py'),
    ('ibe160-v1followup-tests-private-api', 'backend/app/private_main.py', '/app/app/private_main.py'),
]:
    image_id = output('docker', 'image', 'inspect', tag, '--format', '{{.Id}}')
    actual = output('docker', 'run', '--rm', '--pull', 'never', '--network', 'none', '--read-only', '--name', 'ibe160-v1followup-source-' + uuid.uuid4().hex, '--entrypoint', 'python', tag, '-c', f'from pathlib import Path; import hashlib; print(hashlib.sha256(Path({remote!r}).read_bytes()).hexdigest())')
    expected = digest((root/local).read_bytes())
    assert actual == expected, local
    record['images'][tag] = {'id': image_id, 'file': local, 'sha256': actual, 'matches_worktree_bytes': True}
tag = 'ibe160-v1followup-gateway:20261029-r1'
image_id = output('docker', 'image', 'inspect', tag, '--format', '{{.Id}}')
actual = output('docker', 'run', '--rm', '--pull', 'never', '--network', 'none', '--read-only', '--name', 'ibe160-v1followup-source-' + uuid.uuid4().hex, '--entrypoint', 'sha256sum', tag, '/etc/nginx/templates/default.conf.template').split()[0]
assert actual == digest((root/'deploy/tablet/nginx.conf.template').read_bytes())
record['images'][tag] = {'id': image_id, 'file': 'deploy/tablet/nginx.conf.template', 'sha256': actual, 'matches_worktree_bytes': True}
with urllib.request.urlopen('http://127.0.0.1:15326/private', timeout=3) as response:
    html = response.read()
assert html == (root/'frontend/dist/index.html').read_bytes()
paths = set(re.findall(rb'(?:src|href)="(/assets/[^\"]+)"', html))
for path in paths:
    name = path.decode('ascii')
    with urllib.request.urlopen('http://127.0.0.1:15326' + name, timeout=3) as response:
        body = response.read()
    assert body == (root/'frontend/dist'/name.lstrip('/')).read_bytes()
    record['served'][name] = digest(body)
# Include lazy chunks and styles referenced by the actual Vite build, not only HTML.
for asset in (root/'frontend/dist/assets').iterdir():
    with urllib.request.urlopen('http://127.0.0.1:15326/assets/' + asset.name, timeout=3) as response:
        body = response.read()
    assert body == asset.read_bytes()
    record['served']['/assets/' + asset.name] = digest(body)
with urllib.request.urlopen('http://127.0.0.1:18330/health', timeout=3) as response:
    health = json.load(response)
assert health['status'] == 'ok' and health['cleanup']['status'] == 'ok'
record['private_health'] = health
record['method_sha256'] = digest(Path(__file__).read_bytes())
target = root/'docs/evidence'/('v1-followup-source-proof-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '.json')
target.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
print('PASS candidate API/gate/proxy image bytes, actual served static assets and separate cleanup health')
