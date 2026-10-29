import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
root = Path(__file__).resolve().parents[1]
source = (root/'tmp/preservation.py').read_text(encoding='utf-8').split("target=Path('tmp/preservation-before.json')")[0]
source = source.replace("if Path(path).resolve()==Path.cwd().resolve(): continue", "if Path(path).resolve() in (Path.cwd().resolve(), Path('D:/IBE160/tmp/epic12-tracking-correction').resolve()): continue")
namespace = {'__name__':'read_only_final_preservation'}
exec(compile(source,str(root/'tmp/preservation.py'),'exec'),namespace)
after = namespace['record']
before = json.loads((root/'tmp/preservation-before.json').read_text(encoding='utf-8'))
old = {row['path']:row for row in before['worktrees']}
changes = [row for row in after['worktrees'] if old.get(row['path']) != row]
same = [row for row in after['worktrees'] if old.get(row['path']) == row]
record = {
 'at':datetime.now(timezone.utc).isoformat(), 'baseline_at':before['at'],
 'unchanged_other_worktrees':len(same),'concurrent_worktree_changes_preserved':changes,
 'ordinary_containers_unchanged':before['otherContainers']==after['otherContainers'],
 'ordinary_volumes_unchanged':before['otherVolumes']==after['otherVolumes'],
 'ordinary_containers':len(after['otherContainers']),'ordinary_volumes':len(after['otherVolumes']),
 'own_followup_and_tracking_worktrees_excluded':True,
 'authorized_tracking_correction_main':'6f641d75b26a8f5c8b4852a01f7cbf7646905df6',
 'tracking_only_parent':'9677eba434fe1e5a77f9d4efc45827ebb050c5cc',
 'product_candidate_not_merged':'3c2287ed68d0cbb1923439fc6ee00254395072a4',
 'note':'The original D:/IBE160 checkout switched concurrently to setup/ubuntu-server with untracked deploy/ubuntu work before the tracking correction. It was not edited/switched/stashed by this task. Main metadata correction was explicitly owner-authorized and performed in a separate worktree. Historical earlier unchanged checkpoint remains valid at its timestamp. RestartCount and database contents are not audited.',
 'method_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(root/'docs/evidence/v1-followup-final-preservation-20261029.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record))
