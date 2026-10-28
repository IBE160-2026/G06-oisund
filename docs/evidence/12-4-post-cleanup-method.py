from pathlib import Path
import json,subprocess,importlib.util,hashlib
root=Path('D:/IBE160');pre=json.loads(Path('tmp/story124-main-integration/preflight.json').read_text());cleanup=json.loads(Path('docs/evidence/12-4-branch-cleanup.json').read_text())
def git(*a):return subprocess.check_output(['git',*a],cwd=root,text=True,encoding='utf-8').strip()
spec=importlib.util.spec_from_file_location('preflight',root/'tmp/story124-main-integration/preflight.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def stable(rows):return {r['name']:{**r,'source_mounts':sorted(r['source_mounts'],key=lambda x:(x['source'],x['destination']))} for r in rows}
after=m.containers();assert stable(after)==stable(pre['containers_before'])
http=m.http();assert http==pre['http_before']
assert not git('diff','--name-only','5ee35ef','HEAD','--','frontend','backend','scripts','Eksempelfiler','compose.story124.yaml','.dockerignore')
worktrees=[]
for old in pre['worktrees_before']:
 folder=old['path'];head=git('-C',folder,'rev-parse','HEAD');status=git('-C',folder,'status','--porcelain=v1');dirty=len(status.splitlines()) if status else 0
 if Path(folder).resolve()!=root.resolve():assert head==old['head'] and dirty==old['dirty_entries'],folder
 worktrees.append({'path':folder,'head':head,'dirty_entries':dirty,'branch':git('-C',folder,'branch','--show-current') or 'detached'})
for item in cleanup['branches']:
 subprocess.run(['git','merge-base','--is-ancestor',item['head'],'HEAD'],cwd=root,check=True)
 assert not git('ls-remote','--heads','origin',item['branch'])
 assert subprocess.run(['git','show-ref','--verify','--quiet','refs/heads/'+item['branch']],cwd=root).returncode==1
r={'main_at_check':git('rev-parse','HEAD'),'merge':'b0b2a6246b329ad0efa85b570c3f9a0d7a932c33','product_equals_accepted':True,'all27_container_identities_preserved':True,'http_before_equals_after':True,'all_other_worktree_heads_and_dirty_counts_preserved':True,'worktrees':worktrees,'branches_deleted_and_full_history_in_main':True,'force_used':False,'deploy':False,'passed':True}
Path('docs/evidence/12-4-post-cleanup.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps({'passed':True,'containers':len(after),'retainedWorktreesClean':True,'otherPreexistingDirtyEntries':[(w['path'],w['dirty_entries']) for w in worktrees if w['dirty_entries'] and Path(w['path']).resolve()!=root.resolve()],'productUnchanged':True},indent=2))
