import json, subprocess
from pathlib import Path
from datetime import datetime, timezone

def out(*args):
    return subprocess.check_output(args,encoding='utf-8').strip()
rows=[]
for block in out('git','worktree','list','--porcelain').split('\n\n'):
    path=block.splitlines()[0].removeprefix('worktree ')
    if Path(path).resolve()==Path.cwd().resolve(): continue
    rows.append({'path':path,'head':out('git','--no-optional-locks','-C',path,'rev-parse','HEAD'),'status':out('git','--no-optional-locks','-C',path,'status','--porcelain=v1')})
identifiers=out('docker','ps','-aq').split()
containers=[]
if identifiers:
    for row in json.loads(out('docker','inspect',*identifiers)):
        if (row['Config'].get('Labels') or {}).get('com.docker.compose.project')=='ibe160-v1followup-tests': continue
        item={key:row[key] for key in ['Id','Name','Image']}
        item['State']={key:row['State'].get(key) for key in ['Running','Paused','Restarting','Status','StartedAt','FinishedAt','Pid']}
        item['Mounts']=sorted(row['Mounts'],key=lambda mount:mount['Destination'])
        containers.append(item)
volumes=[]
for name in out('docker','volume','ls','--format','{{.Name}}').splitlines():
    row=json.loads(out('docker','volume','inspect',name))[0]
    if (row.get('Labels') or {}).get('com.docker.compose.project')=='ibe160-v1followup-tests': continue
    volumes.append({key:row.get(key) for key in ['Name','Driver','CreatedAt','Labels']})
record={'at':datetime.now(timezone.utc).isoformat(),'worktrees':rows,'otherContainers':containers,'otherVolumes':volumes,'note':'Metadata only after owner manual Docker start; excludes this follow-up project, contains no environment/secret/account/database payload.'}
target=Path('tmp/preservation-before.json')
if target.exists():
    before=json.loads(target.read_text(encoding='utf-8'))
    for key in ['worktrees','otherContainers','otherVolumes']: assert before[key]==record[key],key
    target=Path('tmp/preservation-after.json')
target.write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({'worktrees':len(rows),'otherContainers':len(containers),'otherVolumes':len(volumes),'result':'recorded' if target.name.endswith('before.json') else 'unchanged'}))
