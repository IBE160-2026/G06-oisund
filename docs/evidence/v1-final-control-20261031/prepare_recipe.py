"""Fresh source checkout; four explicit configuration translations only."""
from pathlib import Path
from datetime import datetime, timezone
import subprocess, hashlib, json, socket
root=Path(__file__).resolve().parents[3]
out=Path(__file__).resolve().parent
target=root/'tmp/recipe'
commit='8e590735c495808ae51bf65523d7ab19c6dfb0fd'
project='ibe160-v1-final-20261031'
def run(*args,cwd=root):
    return subprocess.check_output(args,cwd=cwd)
def sha(data):return hashlib.sha256(data).hexdigest()
assert not target.exists(), 'Do not reuse an existing recipe instance'
assert not run('docker','ps','-aq','--filter','label=com.docker.compose.project='+project).strip()
assert not run('docker','volume','ls','-q','--filter','label=com.docker.compose.project='+project).strip()
for port in [15335,18337,18338]:
    with socket.socket() as s:s.bind(('127.0.0.1',port))
ids=run('docker','ps','-aq').decode().split()
containers=json.loads(run('docker','inspect',*ids)) if ids else []
def sanitized(c):
    return {k:c[k] for k in ['Id','Name','Image','State','Mounts']}
before={'containers':[sanitized(c) for c in containers], 'volumes':json.loads(run('docker','volume','inspect',*run('docker','volume','ls','-q').decode().split()))}
# Existing container env/secrets are never saved.
(root/'tmp/docker-before.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
run('git','clone','--no-hardlinks','--no-checkout',str(root),str(target))
run('git','checkout','--detach',commit,cwd=target)
translations=[('ibe160-submission',project),('15325','15335'),('18327','18337'),('18328','18338')]
names=['scripts/submission.mjs','compose.submission.yaml','deploy/submission/Dockerfile','deploy/submission/manage.py','deploy/submission/fictional.py','frontend/playwright.submission.config.ts','scripts/verify-submission-runtime.mjs']
names+=run('git','ls-tree','-r','--name-only',commit,'--','frontend/submission-tests').decode().splitlines()
records={}
for name in names:
    original=run('git','show',commit+':'+name)
    expected=original.decode('utf-8')
    for old,new in translations:expected=expected.replace(old,new)
    (target/name).write_bytes(expected.encode('utf-8'))
    records[name]={'original_git_sha256':sha(original),'instance_sha256':sha((target/name).read_bytes())}
assert set(run('git','diff','--name-only',cwd=target).decode().splitlines())<=set(names)
run('git','diff','--exit-code','--','backend','frontend/src','deploy/ubuntu',cwd=target)
record={'at_utc':datetime.now(timezone.utc).isoformat(),'source_commit':commit,'project':project,'translations':translations,'files':records,'application_and_ubuntu_unchanged':True,'existing_container_count':len(ids),'existing_volume_count':len(before['volumes']),'method_sha256':sha(Path(__file__).read_bytes())}
(out/'recipe-instance.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('PASS fresh recipe instance with explicit configuration translation; existing Docker resources preserved')
