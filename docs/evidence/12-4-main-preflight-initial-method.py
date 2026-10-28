from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,urllib.request,urllib.error
ROOT=Path('D:/IBE160')
def run(*a):return subprocess.check_output(a,cwd=ROOT,text=True,encoding='utf-8').strip()
def containers():
 rows=[]
 for p in map(json.loads,run('docker','ps','--format','json').splitlines()):
  d=json.loads(run('docker','inspect',p['ID']))[0]
  mounts=[{'source':m['Source'],'destination':m['Destination']} for m in d['Mounts'] if m['Type']=='bind' and not m['Destination'].startswith('/run/secrets')]
  rows.append({'name':p['Names'],'id':d['Id'],'image':d['Image'],'ports':p['Ports'],'started':d['State']['StartedAt'],'restarts':d['RestartCount'],'source_mounts':mounts})
 return rows
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args):return None
def http():
 out={};opener=urllib.request.build_opener(NoRedirect)
 for port in (18081,15324,5173,15312,15323):
  url=f'http://127.0.0.1:{port}/'
  try:
   with opener.open(url,timeout=8) as r:out[str(port)]={'status':r.status,'sha256':hashlib.sha256(r.read()).hexdigest()}
  except urllib.error.HTTPError as e:out[str(port)]={'status':e.code,'sha256':hashlib.sha256(e.read()).hexdigest()}
 return out
if __name__=='__main__':
 branch=run('git','rev-parse','story/12-4-complete-user-flow');main=run('git','rev-parse','main')
 assert branch==run('git','rev-parse','origin/story/12-4-complete-user-flow')=='4e38e240917b29450e68f817b85411185ef5eac3'
 assert main==run('git','rev-parse','origin/main')
 assert not run('git','status','--porcelain=v1')
 assert not run('git','-C','D:/IBE160/tmp/story-12-4','status','--porcelain=v1')
 for commit in ['4198b1a','4e38e24','5ee35ef','2671ef7','c0e809f']:
  subprocess.run(['git','merge-base','--is-ancestor',commit,branch],cwd=ROOT,check=True)
 w=[]
 for block in run('git','worktree','list','--porcelain').split('\n\n'):
  fields=block.splitlines();p=fields[0].removeprefix('worktree ');status=run('git','-C',p,'status','--porcelain=v1');w.append({'path':p,'head':run('git','-C',p,'rev-parse','HEAD'),'dirty_entries':len(status.splitlines()) if status else 0})
 r={'recorded_at':datetime.now(timezone.utc).isoformat(),'main_before':main,'story_head':branch,'required_commits_present':True,'worktrees_before':w,'containers_before':containers(),'http_before':http()}
 Path('tmp/story124-main-integration/preflight.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
 print(json.dumps({'main':main,'story':branch,'worktrees':w,'containers':len(r['containers_before']),'http':r['http_before']},indent=2))
