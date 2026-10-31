"""Bind fresh image/served files and compare pre-existing Docker identities/state."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,urllib.request
root=Path(__file__).resolve().parents[3];out=Path(__file__).resolve().parent;instance=root/'tmp/recipe'
project='ibe160-v1-final-20261031'
def run(*args):return subprocess.check_output(args,cwd=instance)
def sha(data):return hashlib.sha256(data).hexdigest()
record={'at_utc':datetime.now(timezone.utc).isoformat(),'source_commit':run('git','rev-parse','HEAD').decode().strip(),'source_files':{},'served_files':{},'images':{}}
for service in ['api','private-api']:
    name=project+'-'+service+'-1'
    program="from pathlib import Path;import hashlib,json;print(json.dumps({str(p.relative_to('/app')):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('/app/app').rglob('*.py')}))"
    files=json.loads(run('docker','exec',name,'python','-c',program))
    for path,digest in files.items():assert sha((instance/'backend'/path).read_bytes())==digest,path
    record['source_files'][service]=files
    record['images'][service]=run('docker','inspect','--format','{{.Image}}',name).decode().strip()
program="const fs=require('fs'),path=require('path'),crypto=require('crypto');let result={};function walk(d){for(const x of fs.readdirSync(d,{withFileTypes:true})){const p=path.join(d,x.name);if(x.isDirectory())walk(p);else result[path.relative('/app/dist',p)]=crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');}}walk('/app/dist');console.log(JSON.stringify(result));"
files=json.loads(run('docker','exec',project+'-frontend-1','node','-e',program))
for path,digest in files.items():
    with urllib.request.urlopen('http://127.0.0.1:15335/'+path,timeout=5) as response:assert sha(response.read())==digest,path
record['served_files']=files
record['images']['frontend']=run('docker','inspect','--format','{{.Image}}',project+'-frontend-1').decode().strip()
for port in [18337,18338]:
    with urllib.request.urlopen(f'http://127.0.0.1:{port}/health',timeout=5) as response:record[str(port)+'_health']=json.load(response)
before=json.loads((root/'tmp/docker-before.json').read_text())
for old in before['containers']:
    new=json.loads(run('docker','inspect',old['Id']))[0]
    # Docker does not promise a stable Mounts-array order. Compare all mount
    # fields after sorting by their unique destination, retaining State exactly.
    assert all((sorted(new[k],key=lambda m:m['Destination'])==sorted(v,key=lambda m:m['Destination'])) if k=='Mounts' else new[k]==v for k,v in old.items()),'Existing container changed: '+old['Name']
for old in before['volumes']:
    new=json.loads(run('docker','volume','inspect',old['Name']))[0]
    assert new==old,'Existing volume changed: '+old['Name']
record['unchanged_existing_containers']=len(before['containers']);record['unchanged_existing_volumes']=len(before['volumes'])
record['docker_version']=run('docker','version','--format','{{.Client.Version}} / {{.Server.Version}}').decode().strip()
record['compose_version']=run('docker','compose','version','--short').decode().strip()
record['node_version']=run('node','--version').decode().strip()
record['passed']=True
(out/'recipe-proof.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('PASS current source/image/served assets; existing containers and volumes unchanged')
