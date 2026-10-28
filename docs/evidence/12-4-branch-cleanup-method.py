from pathlib import Path
from datetime import datetime,timezone
import subprocess,json
ROOT=Path('D:/IBE160')
def run(*a):return subprocess.check_output(a,cwd=ROOT,text=True,encoding='utf-8').strip()
def git(*a):return run('git',*a)
subprocess.run(['git','fetch','origin','--prune'],cwd=ROOT,check=True)
main=git('rev-parse','main');assert main==git('rev-parse','origin/main')
assert not git('status','--porcelain=v1')
items=[]
for branch,folder in [('story/12-3-tablet-pc-accessibility','D:/IBE160/tmp/story-12-3'),('story/12-4-complete-user-flow','D:/IBE160/tmp/story-12-4')]:
 head=git('rev-parse',branch);remote=git('rev-parse','origin/'+branch)
 assert head==remote==git('-C',folder,'rev-parse','HEAD'),branch
 assert git('-C',folder,'symbolic-ref','--short','HEAD')==branch
 assert not git('-C',folder,'status','--porcelain=v1','--untracked-files=all'),branch
 subprocess.run(['git','merge-base','--is-ancestor',head,main],cwd=ROOT,check=True)
 private=Path(folder,'.private-runtime').is_dir();assert private
 items.append({'branch':branch,'head':head,'remote_head':remote,'fully_in_main':True,'uncommitted_or_untracked_entries':0,'unpushed_commits':0,'worktree':folder,'private_runtime_present':private,'action':'Delete branch refs; retain worktree/private state and running environment at exact original detached HEAD'})
# No force flags. Both remote deletes are atomic; local -d also checks merge safety.
remote_output=subprocess.run(['git','push','--atomic','origin','--delete',*[x['branch'] for x in items]],cwd=ROOT,check=True,text=True,capture_output=True)
print(remote_output.stderr.strip())
for x in items:
 subprocess.run(['git','-C',x['worktree'],'switch','--detach',x['head']],cwd=ROOT,check=True)
 assert git('-C',x['worktree'],'rev-parse','HEAD')==x['head']
 assert not git('-C',x['worktree'],'status','--porcelain=v1','--untracked-files=all')
 assert Path(x['worktree'],'.private-runtime').is_dir()
subprocess.run(['git','branch','-d',*[x['branch'] for x in items]],cwd=ROOT,check=True)
for x in items:
 assert subprocess.run(['git','show-ref','--verify','--quiet','refs/heads/'+x['branch']],cwd=ROOT).returncode==1
 assert not git('ls-remote','--heads','origin',x['branch'])
 assert not git('-C',x['worktree'],'branch','--show-current')
r={'recorded_at':datetime.now(timezone.utc).isoformat(),'published_main_before_cleanup':main,'branches':items,'remote_deleted':True,'local_deleted':True,'force_deletion_used':False,'worktree_directories_removed':False,'private_files_read_or_removed':False,'runtime_stopped_or_rebuilt':False}
Path('docs/evidence/12-4-branch-cleanup.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print(json.dumps({'main':main,'remoteDeleted':[x['branch'] for x in items],'localDeleted':True,'retainedDetachedWorktrees':[{x['worktree']:x['head']} for x in items],'privateRuntimeRetained':True,'force':False},indent=2))
