"""Read-only release/tag/archive/backup identity and external admission check."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,re,urllib.request,urllib.error,urllib.parse,os
out=Path(__file__).resolve().parent;root=out.parents[2]
expected='d367a0e47198aeecc52358258cb6825eecdc8c4a'
def run(*args):return subprocess.check_output(args,cwd=root)
def sha(data):return hashlib.sha256(data).hexdigest()
tag=run('git','rev-parse','v1.0.0^{commit}').decode().strip();assert tag==expected
refs=dict(line.split()[::-1] for line in run('git','ls-remote','origin','refs/tags/v1.0.0','refs/tags/v1.0.0^{}').decode().splitlines())
assert refs['refs/tags/v1.0.0^{}']==expected
assert refs['refs/tags/v1.0.0']=='38bfb0d2f629bc97ea39ca2187285d90f562d608'
release=json.loads(run('gh','release','view','v1.0.0','--repo','IBE160-2026/G06-oisund','--json','url,tagName,targetCommitish,isDraft,isPrerelease,publishedAt'))
assert release['tagName']=='v1.0.0' and release['targetCommitish']==expected and not release['isDraft'] and not release['isPrerelease']
ssh=['ssh','-i',str(Path(os.environ['USERPROFILE'])/'.ssh/ibe160_server_ed25519'),'-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','jonas@192.168.1.139']
identity=json.loads(run(*ssh,'cat /opt/bussassistent/current/release-identity.json'))
assert identity['commit']==expected
archive=run('git','archive','--format=tar',expected,'backend','frontend','deploy')
assert sha(archive)==identity['archive_sha256']
backup=Path(re.search(r'Verified backup: (.+)',(out/'predeploy-backup.txt').read_text()).group(1).strip())
assert backup.parent==Path(os.environ['LOCALAPPDATA'])/'BussassistentServer/backups'
local_hash=sha(backup.read_bytes())
remote_hash=run(*ssh,'sha256sum /var/backups/bussassistent/'+backup.name).decode().split()[0]
assert local_hash==remote_hash
record={'at_utc':datetime.now(timezone.utc).isoformat(),'release':release,'remote_refs':refs,'active_identity':identity,'expected_archive_sha256':sha(archive),'backup':{'filename':backup.name,'bytes':backup.stat().st_size,'sha256':local_hash,'remote_copy_equal':True},'external_gets':[]}
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None
opener=urllib.request.build_opener(NoRedirect)
for path in ['/private','/private-api/drafts']:
 try:r=opener.open(urllib.request.Request('https://app.bussassistent.com'+path,method='GET'),timeout=15)
 except urllib.error.HTTPError as e:r=e
 with r:
  body=r.read();location=urllib.parse.urlsplit(r.headers.get('Location',''))
  record['external_gets'].append({'path':path,'status':r.status,'redirect_host':location.hostname,'redirect_path':location.path,'cache_control':r.headers.get('Cache-Control'),'body_bytes':len(body),'body_sha256':sha(body),'no_app_shell':b'/assets/' not in body,'server':r.headers.get('Server')})
record['identity_backup_passed']=True
record['expected_external_302_passed']=all(x['status']==302 and x['redirect_host']=='bussassistent.cloudflareaccess.com' and 'no-store' in (x['cache_control'] or '') and x['no_app_shell'] for x in record['external_gets'])
(out/'identity.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,indent=2))
