"""Read-only cross-worktree evidence; writes only below this extension."""
import hashlib, json, os, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path('D:/IBE160-plan-position-progression').resolve()
OUT = ROOT / '_bmad-output/experimental-extensions/position-progression/.bmad-runner'
assert Path.cwd().resolve() == ROOT

def git(path, *args):
    return subprocess.check_output(['git', '-C', str(path), *args], env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'})

def snapshot():
    result = {}
    for name in ['IBE160', 'IBE160-plan-complete-route-network', 'IBE160-plan-automatic-notices']:
        path = Path('D:/') / name
        status = git(path, 'status', '--porcelain=v1', '-z')
        dirty = git(path, 'ls-files', '-m', '-o', '--exclude-standard', '-z').decode().split('\0')
        hashes = {p: hashlib.sha256((path/p).read_bytes()).hexdigest() for p in sorted(set(dirty)) if p and (path/p).is_file()}
        result[name] = dict(head=git(path,'rev-parse','HEAD').decode().strip(), branch=git(path,'branch','--show-current').decode().strip(), status_sha256=hashlib.sha256(status).hexdigest(), diff_sha256=hashlib.sha256(git(path,'diff','HEAD','--binary')).hexdigest(), dirty_file_hashes=hashes)
    return result

mode=sys.argv[1]
current=snapshot()
if mode=='before':
    target=OUT/'reference-baseline.json'
    assert not target.exists()
    target.write_text(json.dumps(current, indent=2),encoding='utf-8')
    print(json.dumps({k:{'head':v['head'],'branch':v['branch'],'dirty_files':len(v['dirty_file_hashes'])} for k,v in current.items()},indent=2))
elif mode=='after':
    before=json.loads((OUT/'reference-baseline.json').read_text(encoding='utf-8'))
    changed=[k for k in before if before[k]!=current[k]]
    deltas={k:{'head_before':before[k]['head'],'head_after':current[k]['head'],'status_equal':before[k]['status_sha256']==current[k]['status_sha256'],'diff_equal':before[k]['diff_sha256']==current[k]['diff_sha256'],'changed_dirty_paths':[p for p in sorted(set(before[k]['dirty_file_hashes']) | set(current[k]['dirty_file_hashes'])) if before[k]['dirty_file_hashes'].get(p)!=current[k]['dirty_file_hashes'].get(p)]} for k in changed}
    result={'other_worktrees_unchanged_since_research_baseline':not changed,'changed':changed,'reference_deltas':deltas,'own_head':git(ROOT,'rev-parse','HEAD').decode().strip(),'own_branch':git(ROOT,'branch','--show-current').decode().strip(),'own_status':git(ROOT,'status','--short','--untracked-files=all').decode()}
    (OUT/'isolation-result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='own_status'},indent=2))
else:
    raise SystemExit('expected before or after')

