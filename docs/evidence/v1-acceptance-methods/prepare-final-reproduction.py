"""Config-only isolated instance of the unchanged submission recipe at C1.
Preserves existing submission and server work. Run from follow-up checkout.
"""
from pathlib import Path
import subprocess
import hashlib
import json
from datetime import datetime, timezone
root=Path.cwd()
target=Path('D:/IBE160/tmp/v1-delivery-candidate')
commit='3c2287ed68d0cbb1923439fc6ee00254395072a4'
if not target.exists():
 subprocess.run(['git','worktree','add','--detach',str(target),commit],cwd=root,check=True)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=target,text=True).strip()==commit
translations=[('ibe160-submission','ibe160-v1-delivery'),('15325','15327'),('18327','18331'),('18328','18332')]
names=['scripts/submission.mjs','compose.submission.yaml','deploy/submission/Dockerfile','deploy/submission/manage.py','deploy/submission/fictional.py','frontend/playwright.submission.config.ts','scripts/verify-submission-runtime.mjs']
names+=subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'--','frontend/submission-tests'],cwd=root,text=True).splitlines()
records={}
for name in names:
 original=subprocess.check_output(['git','show',commit+':'+name],cwd=root)
 expected=original.decode('utf-8')
 for old,new in translations:expected=expected.replace(old,new)
 current=(target/name).read_bytes().replace(b'\r\n',b'\n')
 assert current in (original.replace(b'\r\n',b'\n'),expected.encode().replace(b'\r\n',b'\n')), 'Unexpected instance edits: '+name
 (target/name).write_text(expected,encoding='utf-8')
 records[name]={'original_git_bytes_sha256':hashlib.sha256(original).hexdigest(),'instance_bytes_sha256':hashlib.sha256((target/name).read_bytes()).hexdigest()}
changed=subprocess.check_output(['git','diff','--name-only'],cwd=target,text=True).splitlines()
assert set(changed)<=set(names)
subprocess.run(['git','diff','--quiet','--','backend/app','frontend/src'],cwd=target,check=True)
assert not (target/'deploy/ubuntu').exists() and not (target/'scripts/server.ps1').exists()
record={'at':datetime.now(timezone.utc).isoformat(),'product_snapshot':commit,'instance_checkout':str(target),'project':'ibe160-v1-delivery','ports':{'frontend':15327,'fictional':18331,'private':18332},'translations':translations,'files':records,'app_source_unchanged':True,'server_bonus_absent':True,'existing_submission_untouched':True,'method_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(root/'docs/evidence/v1-acceptance-reproduction-instance.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('PASS config-only fresh delivery instance prepared from immutable C1; app sources unchanged; bonus server absent')
