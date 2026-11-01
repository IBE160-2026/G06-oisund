"""Read-only hash inventory of public runtime code, never secrets/private data.

Production use requires owner-run sudo. Only the two expected, read-only project
containers are queried. No application import, request, package change or signal.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

CODE = r'''
import hashlib,json,os
from pathlib import Path
roots=['/usr/local/lib','/usr/lib/x86_64-linux-gnu','/usr/local/bin','/usr/bin','/usr/sbin','/app/app']
result={};seen=set()
for root in roots:
 for p in Path(root).rglob('*'):
  if not p.is_file() or p.is_symlink():continue
  native=False
  with p.open('rb') as f:native=f.read(4)==b'\x7fELF'
  python=p.suffix=='.py'
  if not(native or python):continue
  name=str(p)
  if name in seen:continue
  seen.add(name)
  result[name]={'kind':'ELF' if native else 'python','bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()}
for name in ['/gate/gate.py','/usr/local/bin/python3.13']:
 p=Path(name)
 if p.is_file():
  with p.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
  result[name]={'kind':'ELF' if p.read_bytes()[:4]==b'\x7fELF' else 'python','bytes':p.stat().st_size,'sha256':digest}
maps=[]
for line in Path('/proc/1/maps').read_text().splitlines():
 parts=line.split(None,5)
 if len(parts)==6 and parts[5].startswith(('/usr/lib/','/usr/local/lib/','/lib/','/usr/local/bin/python')):maps.append(parts[5])
print(json.dumps({'files':result,'uid':os.getuid(),'python_version':__import__('sys').version.split()[0],
                 'main_process_mapped_paths':sorted(set(maps))},sort_keys=True))
'''


def run(args):
    return subprocess.run(args,check=True,capture_output=True,text=True).stdout


def inspect(ident):
    fields={'id':'.Id','image':'.Image','pid':'.State.Pid','started':'.State.StartedAt',
            'restarts':'.RestartCount','running':'.State.Running','read_only':'.HostConfig.ReadonlyRootfs',
            'project':'index .Config.Labels "com.docker.compose.project"',
            'service':'index .Config.Labels "com.docker.compose.service"'}
    template='{'+','.join(json.dumps(k)+':{{json ('+v+')}}'for k,v in fields.items())+'}'
    return json.loads(run(['docker','inspect','--format',template,ident]))


def collect(identity,expected,project='bussassistent'):
    report={'started_utc':datetime.now(timezone.utc).isoformat(),'method_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'release':identity,'roles':{}}
    for service,image in expected.items():
        ids=run(['docker','ps','--filter','label=com.docker.compose.project='+project,'--filter','label=com.docker.compose.service='+service,'-q']).split()
        if len(ids)!=1:raise ValueError('Expected one service: '+service)
        before=inspect(ids[0])
        if before['image']!=image or not before['running'] or not before['read_only'] or before['project']!=project or before['service']!=service:
            raise ValueError('Unexpected service identity/policy')
        metadata=json.loads(run(['docker','exec',ids[0],'nice','-n','15','python','-B','-c',CODE]))
        after=inspect(ids[0])
        if before!=after:raise ValueError('Lifecycle changed during read-only inventory')
        report['roles'][service]={'identity':before,'metadata':metadata,'main_process_mapped_paths':metadata.pop('main_process_mapped_paths'),
                                   'lifecycle_unchanged':True}
    report['finished_utc']=datetime.now(timezone.utc).isoformat()
    return report


def main():
    expected={'private-api':'sha256:37b767bae51a464f0e726a784b734627e223bbb102592e09d9f8c4061cea7a45',
              'access-gate':'sha256:6bba55ec94b9e1e994c23e37e6a62efb67d2a32cd6448a616200ffd4cb168bc9'}
    identity=json.loads(Path('/opt/bussassistent/current/release-identity.json').read_text())
    if identity['commit']!='93ee582b1a71a3f7552da1894b570366b89afee1':raise ValueError('Unexpected active release')
    print(json.dumps(collect(identity,expected),indent=2,sort_keys=True))


if __name__=='__main__':main()
