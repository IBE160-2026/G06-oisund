"""Extra syntax/static/error checks; stop only our UUID synthetic upstream."""
import hashlib
import json
from pathlib import Path
import subprocess
from uuid import uuid4

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/evidence/o6-gateway-deploy-20261101'
def run(*args):
 p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return p.stdout
def main():
 image=json.loads((OUT/'candidate-image.json').read_text())['Id'];inputs=json.loads((OUT/'input.json').read_text());py=inputs['tests_image']
 old=inputs['baseline_image'];files={}
 for label,ref in [('baseline',old),('candidate',image)]:
  data=run('docker','run','--rm','--pull','never','--network','none','--read-only','--entrypoint','find',ref,'/usr/share/nginx/html','-type','f','-exec','sha256sum','{}',';')
  files[label]={s.split(None,1)[1]:s.split()[0] for s in data.splitlines()}
 app=lambda d:{k:v for k,v in d.items() if '/assets/' in k or k.endswith('/index.html')}
 assert app(files['baseline'])==app(files['candidate'])
 namespace='ibe160-o6-gw-extra-'+uuid4().hex;created=[];network=False;results={}
 try:
  run('docker','network','create','--internal',namespace);network=True
  for role,alias,command in [('fixture','access-gate',['python','/probe/tablet-proxy-probe.py','server']),('api','private-api',['python','/extra/gateway_runtime_probe.py','api'])]:
   name=namespace+'-'+role
   run('docker','run','-d','--name',name,'--network',namespace,'--network-alias',alias,'--network-alias',role,'--read-only','--cap-drop','ALL','--user','10001:10001','--tmpfs','/tmp','--mount',f'type=bind,source={ROOT}/scripts,target=/probe,readonly','--mount',f'type=bind,source={ROOT}/scripts/operations-followup,target=/extra,readonly','--mount',f'type=bind,source={ROOT}/deploy/tablet/access_gate,target=/gate-current,readonly','-e','PYTHONPATH=/gate-current',py,*command);created.append(name)
  name=namespace+'-gateway';run('docker','run','-d','--name',name,'--network',namespace,'--network-alias','gateway','--read-only','--cap-drop','ALL','--user','101:101','--tmpfs','/tmp:mode=1777','-e','TABLET_HOST=bus.owner-domain.no',image);created.append(name)
  def probe(mode):return json.loads(run('docker','run','--rm','--pull','never','--network',namespace,'--read-only','--mount',f'type=bind,source={ROOT}/scripts/operations-followup,target=/extra,readonly',py,'python','/extra/gateway_runtime_probe.py',mode))
  results['up']=probe('up')
  p=subprocess.run(['docker','exec',name,'nginx','-t'],capture_output=True,text=True);assert p.returncode==0,p.stderr;results['syntax']=p.stderr
  run('docker','stop','-t','1',namespace+'-api');results['upstream_only_down']=probe('api-down')
 finally:
  for name in reversed(created):run('docker','rm','-f',name)
  if network:run('docker','network','rm',namespace)
 results['static_files']=files;results['app_assets_identical_to_baseline']=True;results['own_namespace_removed']=namespace
 (OUT/'extra-runtime.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS syntax, static byte equality, actual static serving, ten error statuses and independent API-down handling')
if __name__=='__main__':main()
