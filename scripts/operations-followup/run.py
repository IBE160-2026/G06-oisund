"""Isolated O3/O5 runner. Reuses images by immutable ID, never existing containers.

Only its UUID containers/network/credential are removed, including on failure.
Run from repo root. Output is sanitized synthetic evidence, never credentials.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/evidence/operations-o3-o6-20261031'
if '--only-http' in sys.argv:
    OUT = OUT/('http-retry-'+datetime.now(timezone.utc).strftime('%H%M%S'))
if (OUT/'runs.json').exists():
    raise SystemExit('Evidence already exists. Choose a NEW OUT directory; historical runs must not be overwritten.')
TMP = ROOT/'tmp/operations-followup'
OUT.mkdir(parents=True, exist_ok=True); TMP.mkdir(parents=True, exist_ok=True)
def run(*args, check=True):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and p.returncode: raise RuntimeError(f'{args[0:3]} failed: {p.stderr[:1500]}')
    return p
def docker(*args): return run('docker', *args).stdout
def snapshot():
    ids = docker('ps','-aq').split()
    containers = json.loads(docker('inspect',*ids)) if ids else []
    names = docker('volume','ls','-q').split()
    return {'containers':[{k:c[k] for k in ('Id','Name','Image','Created','State','RestartCount','Mounts')} for c in containers],
            'volumes':json.loads(docker('volume','inspect',*names)) if names else []}
def save(name, obj): (OUT/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
before = snapshot(); save('docker-before.json', before)
identity = {'at_utc':datetime.now(timezone.utc).isoformat(), 'source_commit':run('git','rev-parse','HEAD').stdout.strip(),
            'product_diff_from_v1':run('git','diff','v1.0.0','HEAD','--','backend','frontend','deploy').stdout,
            'images':{}}
assert identity['product_diff_from_v1'] == ''
for role, ref in {'api':'ibe160-v1-final-20261031-private-api:latest',
                  'gate':'ibe160-v1followup-gate-tests:20261029-r1',
                  'gateway':'ibe160-v1followup-gateway:20261029-r1',
                  'db':'postgres:17-alpine@sha256:b0f9560a2de083e2cc7382e75f808c7381a32852a7ec49117deedb300e552b24'}.items():
    identity['images'][role] = json.loads(docker('image','inspect',ref))[0]['Id']
# Verify actual image source before reuse; do not relabel historical test results.
program = "from pathlib import Path;import hashlib,json;print(json.dumps({str(p.relative_to('/app')):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('/app/app').rglob('*.py')}))"
files = json.loads(docker('run','--rm','--network','none','--read-only',identity['images']['api'],'python','-c',program))
assert files
for name, digest in files.items(): assert hashlib.sha256((ROOT/'backend'/name).read_bytes()).hexdigest() == digest, name
identity['api_source_hashes'] = files
gateway_template = docker('run','--rm','--network','none','--entrypoint','cat',identity['images']['gateway'],'/etc/nginx/templates/default.conf.template')
assert gateway_template.replace('\r\n','\n') == (ROOT/'deploy/tablet/nginx.conf.template').read_text().replace('\r\n','\n')
identity['gateway_template_sha256'] = hashlib.sha256(gateway_template.encode()).hexdigest()
identity['methods_sha256'] = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'scripts/operations-followup').glob('*.py')}
save('test-identity.json',identity)
namespace = 'ibe160-ops-' + uuid4().hex
credential = TMP/(namespace+'-password')
credential.write_text(secrets.token_urlsafe(48), encoding='ascii')
resolv = TMP/(namespace+'-resolv.conf')
resolv.write_text('nameserver 127.0.0.1\noptions timeout:5 attempts:2\n',encoding='ascii')
network = False; containers = []
results = []
def capture(name, args):
    start = datetime.now(timezone.utc).isoformat()
    p = run(*args,check=False)
    (OUT/(name+'.txt')).write_text(p.stdout+p.stderr,encoding='utf-8')
    results.append({'name':name,'start_utc':start,'end_utc':datetime.now(timezone.utc).isoformat(),'exit':p.returncode})
    save('runs.json',results)
    print(name, 'exit', p.returncode, flush=True)
    if p.returncode: print((p.stdout+p.stderr)[-1000:],flush=True)
    return p.returncode
try:
    if '--only-http' not in sys.argv:
        capture('https-mode-api', ['pwsh','-NoProfile','-File','scripts/verify-tablet-api.ps1','-ApiImage',identity['images']['api']])
        capture('nginx-proxy', ['pwsh','-NoProfile','-File','scripts/verify-tablet-proxy.ps1','-PythonImage',identity['images']['gate'],'-GatewayImage',identity['images']['gateway']])
    dnsname = namespace+'-dns'; containers.append(dnsname)
    if '--only-http' not in sys.argv: capture('real-os-dns', ['docker','run','--rm','--name',dnsname,'--network','none','--read-only','--user','0:0','--cap-drop','ALL',
        '--mount',f'type=bind,source={resolv},target=/etc/resolv.conf,readonly',
        '--mount',f'type=bind,source={ROOT}/scripts/operations-followup,target=/probe,readonly',
        '--mount',f'type=bind,source={ROOT}/deploy/tablet/access_gate,target=/gate-current,readonly',
        '-e','PYTHONPATH=/gate-current',identity['images']['gate'],'python','/probe/dns_os.py'])
    docker('network','create','--internal',namespace); network=True
    dbname = namespace+'-db'; containers.append(dbname)
    docker('run','-d','--name',dbname,'--network',namespace,'--network-alias','private-db','--user','postgres','--read-only','--cap-drop','ALL',
           '--tmpfs','/tmp:mode=1777','--tmpfs','/var/run/postgresql:mode=1777','--tmpfs','/var/lib/postgresql/data:uid=70,gid=70,mode=0700',
           '-e','POSTGRES_USER=tablet_bootstrap','-e','POSTGRES_DB=private_work','-e','POSTGRES_PASSWORD_FILE=/run/secrets/tablet_postgres_password',
           '--mount',f'type=bind,source={credential},target=/run/secrets/tablet_postgres_password,readonly',
           '--mount',f'type=bind,source={ROOT}/deploy/tablet/init-private-role.sql,target=/docker-entrypoint-initdb.d/010-private-role.sql,readonly',identity['images']['db'])
    for _ in range(50):
        if run('docker','exec',dbname,'pg_isready','-U','tablet_bootstrap','-d','private_work','-h','127.0.0.1',check=False).returncode == 0: break
        time.sleep(.2)
    else: raise RuntimeError('Disposable database not ready')
    clientname = namespace+'-client'; containers.append(clientname)
    capture('http-lost-response', ['docker','run','--rm','--name',clientname,'--network',namespace,'--read-only','--cap-drop','ALL','--user','10001:10001','--tmpfs','/tmp',
          '-e','OPERATIONS_DISPOSABLE=1','-e','APP_MODE=private-local','-e','PRIVATE_LOOPBACK_DEVELOPMENT=1','-e','PRIVATE_ORIGIN=http://127.0.0.1:18000',
          '-e','PRIVATE_DATABASE_URL=postgresql://private_work@private-db/private_work','-e','PRIVATE_DATABASE_PASSWORD_FILE=/run/secrets/password',
          '-e','PYTHONPATH=/app','-e','PYTHONDONTWRITEBYTECODE=1',
          '--mount',f'type=bind,source={credential},target=/run/secrets/password,readonly',
          '--mount',f'type=bind,source={ROOT}/scripts/operations-followup,target=/probe,readonly',identity['images']['api'],'python','/probe/http_loss.py'])
finally:
    for name in containers:
        if run('docker','inspect',name,check=False).returncode == 0: docker('rm','-f',name)
    if network: docker('network','rm',namespace)
    credential.unlink(missing_ok=True); resolv.unlink(missing_ok=True)
    after = snapshot(); save('docker-after.json',after)
    def normalized(data):
        for item in data['containers']:
            item['Mounts'].sort(key=lambda x:x['Destination'])
            # Scheduled health-check timestamps/output rotate during healthy operation.
            # Keep Health.Status and FailingStreak plus every lifecycle/state field.
            item['State'].get('Health',{}).pop('Log',None)
        data['containers'].sort(key=lambda x:x['Id']); data['volumes'].sort(key=lambda x:x['Name'])
        return data
    same = normalized(before) == normalized(after)
    save('cleanup.json',{'namespace':namespace,'removed_own_containers_network_credentials':True,
                        'preexisting_containers_volumes_identical':same,'containers_before':len(before['containers']),
                        'volumes_before':len(before['volumes'])})
    assert same, 'Existing Docker resources changed; inspect before/after, do not reset'
sys.exit(any(r['exit'] != 0 for r in results))
