"""Isolated ACL/SQLite reachability analysis. No production operations."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/evidence/o6-acl-fts5-20261101'
TMP=ROOT/'tmp/o6-acl-fts5-20261101'


def save(name,value):
    path=OUT/name
    if path.exists():raise RuntimeError('Refusing to overwrite '+name)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def run(args,check=True,binary=False,input=None):
    p=subprocess.run(args,cwd=ROOT,capture_output=True,text=not binary,input=input)
    if check and p.returncode:raise RuntimeError(str(args[:3])+': '+str(p.stderr)[-1500:])
    return p


def capture(name,args):
    if (OUT/(name+'.json')).exists():raise RuntimeError('Receipt exists')
    started=datetime.now(timezone.utc).isoformat();p=run(args,check=False)
    data=(p.stdout+p.stderr).encode();(OUT/(name+'.txt')).write_bytes(data)
    save(name+'.json',dict(command=args,start_utc=started,end_utc=datetime.now(timezone.utc).isoformat(),
       exit=p.returncode,sha256=hashlib.sha256(data).hexdigest()))
    print(name,'exit',p.returncode,flush=True)
    if p.returncode:raise RuntimeError('Control failed: '+name)
    return p.stdout


def snapshot():
    ids=run(['docker','ps','-aq']).stdout.split()
    values=json.loads(run(['docker','inspect',*ids]).stdout)
    result=[]
    for c in values:
        c['State'].get('Health',{}).pop('Log',None)
        c['Mounts'].sort(key=lambda m:m['Destination'])
        result.append({k:c[k]for k in ['Id','Name','Image','RestartCount','State','Mounts']})
    return dict(containers=result,volumes=run(['docker','volume','ls','-q']).stdout.split())


if __name__=='__main__':
    OUT.mkdir(exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
    if sys.argv[1]=='before':
        save('environment-before.json',snapshot())
        refs=json.loads(run(['git','show','qualify/remaining-o6-20261101:docs/evidence/o6-remaining-20261101/image-ids.json']).stdout)
        save('images.json',refs)
    else:raise SystemExit('Unknown phase')
