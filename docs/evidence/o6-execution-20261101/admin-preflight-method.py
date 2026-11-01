"""Read-only image export and protected recovery backup; no activation."""
import hashlib,json,os,subprocess,sys,tarfile
from pathlib import Path
SHA='5e521cbc658594a47c4568d352a50e46309573c4'
HERE=Path(__file__).resolve().parent

def run(args):return subprocess.run(args,check=True,capture_output=True,text=True).stdout

def export(refs):
 result={}
 for role,ref in refs.items():
  r=json.loads(run(['docker','image','inspect',ref]))[0]
  result[role]={k:r[k]for k in ['Id','Architecture','Os','RootFS']}
 target=HERE/'staged-images.tar'
 if target.exists():raise ValueError('Export already exists')
 run(['docker','save','-o',str(target),*refs.values()])
 return result,target

def main():
 if os.geteuid()!=0:raise ValueError('Administrator required')
 current=json.loads(Path('/opt/bussassistent/current/release-identity.json').read_text())
 if current['commit']!='93ee582b1a71a3f7552da1894b570366b89afee1':raise ValueError('Active release changed')
 refs={r:'bussassistent-'+r+':'+SHA for r in ['api','access-gate','postgres','gateway']}
 images,target=export(refs)
 recovery=Path('/var/backups/bussassistent/o6-pre-5e521cbc')
 recovery.mkdir(mode=0o700,exist_ok=False)
 paths=['etc/systemd/system','etc/udev','etc/pam.d','etc/nsswitch.conf','etc/resolv.conf','etc/netplan','var/lib/dpkg/status','var/lib/apt/extended_states']
 archive=recovery/'host-config.tar'
 with tarfile.open(archive,'x',dereference=False)as tar:
  for name in paths:
   path=Path('/')/name
   if path.exists()or path.is_symlink():tar.add(path,arcname=name)
 archive.chmod(0o600)
 with tarfile.open(archive)as tar:
  names=tar.getnames()
  if not all(any(x==p or x.startswith(p+'/')for x in names)for p in paths):raise ValueError('Incomplete backup')
 uid=int(os.environ['SUDO_UID']);gid=int(os.environ['SUDO_GID'])
 os.chown(target,uid,gid);target.chmod(0o600)
 def digest(p):
  with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
 result={'release':SHA,'active':current['commit'],'images':images,'export':str(target),'export_sha256':digest(target),'export_bytes':target.stat().st_size,
  'host_backup':str(archive),'host_backup_sha256':digest(archive),'host_backup_members':len(names),'host_backup_mode':'0600; directory0700','production_activation':False}
 output=HERE/'preflight.json';output.write_text(json.dumps(result,indent=2)+'\n');os.chown(output,uid,gid);output.chmod(0o600)
 print('Image export and protected host backup complete; no activation')

if __name__=='__main__':main()
