import difflib
import json
import subprocess
import uuid
from pathlib import Path
from datetime import datetime, timezone
root = Path(__file__).resolve().parents[1]
base = '9677eba434fe1e5a77f9d4efc45827ebb050c5cc'
prior = '6d1259628c5fc7cec2d649e4097331d1606d9574'
names = ['_bmad-output/implementation-artifacts/epic-12-context.md','_bmad-output/implementation-artifacts/epic-12-retro-2026-10-29.md','_bmad-output/implementation-artifacts/spec-12-5-reproducible-submission.md','_bmad-output/planning-artifacts/epics.md','_bmad-output/implementation-artifacts/sprint-status.yaml','docs/submission/README.md','docs/submission/traceability.md','docs/submission/v1-closeout.md']
fixture = root/'tmp'/('tracker-check-'+uuid.uuid4().hex)
patch = root/'docs/evidence/v1-followup-epic12-main-correction.patch'
chunks = []
for name in names:
    old = subprocess.check_output(['git','show',base+':'+name],cwd=root).decode('utf-8')
    new = subprocess.check_output(['git','show',prior+':'+name],cwd=root).decode('utf-8')
    if name.endswith('.yaml'):
        new = new.replace('last_updated: 10-29-2026 10:03','last_updated: 10-29-2026 '+datetime.now().strftime('%H:%M'))
        new = new.replace('  epic-12: in-progress','  epic-12: in-progress # Owner clarified 2026-10-29: only Story12.5 was to be marked done; epic stays open.')
    else:
        lines = new.splitlines(keepends=True)
        heading = next((i for i,line in enumerate(lines) if line.lstrip('\ufeff').startswith('#')), None)
        if heading is None:
            heading = next((i for i,line in enumerate(lines[1:],1) if line.strip() == '---'), -1)
        lines[heading+1:heading+1] = ['\n> Owner clarification,29October2026: the prior Epic12 done publication was a misunderstanding; only Story12.5 was to be marked done. All accepted story results and the completed retrospective remain unchanged. Epic12 stays open pending the closure basis and owner decisions.\n']
        new = ''.join(lines)
    target = fixture/name
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(old,encoding='utf-8',newline='')
    chunks.extend(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='a/'+name,tofile='b/'+name))
patch.write_text(''.join(chunks),encoding='utf-8',newline='')
subprocess.run(['git','apply','--check','--directory='+str(fixture.relative_to(root)).replace('\\','/'),str(patch)],cwd=root,check=True)
record = {'at':datetime.now(timezone.utc).isoformat(),'current_main':base,'candidate':'3c2287ed68d0cbb1923439fc6ee00254395072a4','changed_main_paths':names,'product_test_tooling_diff_from_initial_baseline':False,'prepared_correction':'docs/evidence/v1-followup-epic12-main-correction.patch','isolated_apply_check':'passed','applied_to_main':False,'user_clarification':'The Epic12 completion was a misunderstanding; only12.5 was to be marked done. Epic12 must stay open.','scope':'eight metadata documents only; no product, tests, runtime or prior logs are overwritten'}
(root/'docs/evidence/v1-followup-concurrent-tracking-20261029.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('PASS eight-file tracking-only correction applies to isolated copy of main9677eba; main untouched')
