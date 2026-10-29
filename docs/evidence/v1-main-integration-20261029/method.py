"""Bounded accepted-C1 integration verification; no operational service mutation."""
from pathlib import Path
from datetime import datetime, timezone
import subprocess, os, json, hashlib, urllib.request
root=Path(__file__).resolve().parents[3]
out=Path(__file__).resolve().parent
python='D:/IBE160/tmp/v1-remediation/.venv-followup/Scripts/python.exe'
candidate='3c2287ed68d0cbb1923439fc6ee00254395072a4'
def git(*args):return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
def sha(data):return hashlib.sha256(data).hexdigest()
env=dict(os.environ,PRIVATE_ORIGIN='http://127.0.0.1:15326',PRIVATE_LOOPBACK_DEVELOPMENT='1',PYTHONPATH=str(root/'backend')+';'+str(root/'deploy/tablet/access_gate'))
temp=root/'tmp/v1-main-integration';temp.mkdir(parents=True,exist_ok=True)
env.update(TEMP=str(temp),TMP=str(temp),TMPDIR=str(temp))
record={'started':datetime.now(timezone.utc).isoformat(),'main_parent':git('rev-parse','HEAD'),'accepted_followup':git('rev-parse','MERGE_HEAD'),'product_snapshot':candidate,'commands':[],'served':{}}
try:
 subprocess.run(['git','diff','--cached','--quiet',candidate,'--','backend','frontend','scripts','deploy','compose.v1followup.yaml','compose.submission.yaml'],cwd=root,check=True)
 assert not (root/'deploy/ubuntu').exists() and not (root/'scripts/server.ps1').exists()
 record['accepted_product_test_tooling_identical']=True;record['server_bonus_absent']=True
 commands=[
  ('host',[python,'-m','pytest','-q','-p','no:cacheprovider','backend/tests/test_cleanup_observability.py','deploy/tablet/access_gate/test_gate.py','deploy/tablet/access_gate/test_bounded_gate.py','deploy/tablet/access_gate/test_gate_http.py','scripts/test_verify_v1followup.py','--tb=line'],180),
  ('preparation',['pwsh','-NoProfile','-File','scripts/test-prepare-tablet-parity.ps1'],30),
  ('submission-syntax',['node','--check','scripts/submission.mjs'],15),
  ('adapter-syntax',['node','--check','scripts/prepare-v1followup-tests.mjs'],15),
 ]
 for name,args,timeout in commands:
  started=datetime.now(timezone.utc).isoformat()
  with (out/(name+'.log')).open('wb') as log:
   result=subprocess.run(args,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=timeout)
  record['commands'].append({'name':name,'command':args,'started':started,'exit_code':result.returncode,'log_sha256':sha((out/(name+'.log')).read_bytes())})
  assert result.returncode==0,name+' failed; inspect retained log'
 for port,name,key in [(15326,'v1-followup-source-proof-20261029T175511.json','served'),(15327,'v1-acceptance-reproduction/source-proof.json','served')]:
  expected=json.loads((root/'docs/evidence'/name).read_text(encoding='utf-8'))[key]
  for path,digest in expected.items():
   with urllib.request.urlopen('http://127.0.0.1:'+str(port)+'/'+path.lstrip('/'),timeout=3) as r:body=r.read()
   assert sha(body)==digest,(port,path)
  record['served'][str(port)]={'matched_files':len(expected),'matches_versioned_proof':True}
 for port in [18330,18332]:
  with urllib.request.urlopen('http://127.0.0.1:'+str(port)+'/health',timeout=3) as r:health=json.load(r)
  assert health['status']=='ok' and health['cleanup']['status']=='ok'
  record['served'][str(port)]={'health':health}
 index=json.loads((root/'docs/evidence/v1-acceptance-reproduction/index.json').read_text(encoding='utf-8'))
 for name,entry in index.items():assert sha(subprocess.check_output(['git','show',':'+name],cwd=root))==entry['sha256'],name
 record['all_reproduction_indexed_git_blobs_match']=True
 changed=git('diff','--cached','--name-status','6d1259628c5fc7cec2d649e4097331d1606d9574','--','docs/evidence').splitlines()
 assert all(line.startswith('A\t') for line in changed), 'Historical evidence altered'
 record['historical_evidence_unchanged']=True
 record['passed']=True
except Exception as error:
 record['passed']=False;record['error']=str(error)
finally:
 record['finished']=datetime.now(timezone.utc).isoformat();record['method_sha256']=sha(Path(__file__).read_bytes())
 (out/'result.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'passed':record['passed'],'commands':[(c['name'],c['exit_code']) for c in record['commands']],'error':record.get('error')}))
if not record['passed']:raise SystemExit(1)
