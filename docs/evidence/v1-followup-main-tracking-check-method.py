import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone
root = Path(__file__).resolve().parents[1]
before = '9677eba434fe1e5a77f9d4efc45827ebb050c5cc'
after = '6f641d75b26a8f5c8b4852a01f7cbf7646905df6'
def show(commit,path):
    return subprocess.check_output(['git','show',commit+':'+path],cwd=root,text=True)
path = '_bmad-output/implementation-artifacts/sprint-status.yaml'
old,new = show(before,path),show(after,path)
def statuses(text):
    text=text.split('development_status:',1)[1].split('action_items:',1)[0]
    return {key:value.strip() for key,value in re.findall(r'^  ([^:\n]+):\s+([^#\n]+)',text,re.M)}
a,b=statuses(old),statuses(new)
assert set(a)==set(b)
changes={key:[a[key],b[key]] for key in a if a[key]!=b[key]}
assert changes=={'epic-12':['done','in-progress']}
assert old.split('action_items:',1)[1]==new.split('action_items:',1)[1]
paths=subprocess.check_output(['git','diff','--name-only',before,after],cwd=root,text=True).splitlines()
assert len(paths)==10 and all(name.startswith(('_bmad-output/','docs/submission/','.logs/')) for name in paths)
subprocess.run(['git','diff','--quiet',before,after,'--','backend','frontend','scripts','deploy','compose.yaml','compose.private.yaml','compose.tablet.yaml'],cwd=root,check=True)
record={'at':datetime.now(timezone.utc).isoformat(),'owner_authorization':'Explicit approval in this chat to publish only the eight-file tracking correction to main; product/test/runtime excluded.','metadata_commit':'26b9e259c72346ca73a7b447998d16e6fcca86be','separate_log_commit_and_verified_remote_main':after,'previous_main':before,'development_status_changes':changes,'action_items_unchanged':True,'story_12_5':b['12-5-deliver-a-reproducible-submission'],'retrospective':b['epic-12-retrospective'],'changed_paths':paths,'product_test_tooling_deployment_diff':False,'product_candidate_unmerged':'3c2287ed68d0cbb1923439fc6ee00254395072a4','other_original_checkout':'setup/ubuntu-server work preserved; separate correction worktree used'}
(root/'docs/evidence/v1-followup-main-tracking-corrected-20261029.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('PASS main tracking only: epic12 in-progress,12.5/retro done, all action items and product/test/tooling unchanged')
