import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request
from datetime import datetime, timezone

root = Path('D:/IBE160')
compose = ['docker', 'compose', '-p', 'ibe160-story12-integration', '-f', 'compose.story12-integration.yaml']
names = subprocess.check_output(['git', 'ls-files', 'backend'], cwd=root, text=True).splitlines()
host = {n.removeprefix('backend/'): hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}
script = 'import hashlib,json; from pathlib import Path; names='+repr(list(host))+'; print(json.dumps({n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}))'
record = {'revision': subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(), 'time': datetime.now(timezone.utc).isoformat(), 'api_files': {}, 'assets': {}}
for service in ['api','private-api']:
    actual = json.loads(subprocess.check_output(compose+['exec','-T',service,'python','-c',script],cwd=root,text=True))
    assert actual == host, service
    record['api_files'][service] = {'count': len(host), 'sha256': actual}
assets = set()
for name, url in [('index.html','/'),('demo.html','/demo')]:
    data = urllib.request.urlopen('http://127.0.0.1:15312'+url).read()
    assert data == (root/'frontend/dist'/name).read_bytes(), name
    assets.update(re.findall(r'(?:src|href)="(/assets/[^"]+)"',data.decode()))
    record['assets'][name] = hashlib.sha256(data).hexdigest()
for asset in assets:
    data = urllib.request.urlopen('http://127.0.0.1:15312'+asset).read()
    assert data == (root/'frontend/dist'/asset.lstrip('/')).read_bytes(),asset
    record['assets'][asset] = hashlib.sha256(data).hexdigest()
for port in [18312,18313]:
    with urllib.request.urlopen(f'http://127.0.0.1:{port}/health') as response:
        assert response.status == 200
record['result'] = 'passed'
(root/'docs/evidence/12-after-access-runtime.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print('Runtime source and served assets match; both APIs healthy.')
