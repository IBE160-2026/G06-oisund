"""Restore the documented 10-second GRUB recovery menu; never reboots."""
import hashlib,json,os,re,subprocess,tarfile,time
from pathlib import Path
RECOVERY=Path('/var/backups/bussassistent/o6-pre-5e521cbc')
WINDOW=Path('/tmp/ibe160-o6-window.uNfjQHcy')

def rewrite(data):
 for key,value in [(b'GRUB_TIMEOUT_STYLE',b'menu'),(b'GRUB_TIMEOUT',b'10')]:
  pattern=rb'(?m)^[ \t]*'+key+rb'=.*$'
  if re.search(pattern,data):data=re.sub(pattern,key+b'='+value,data)
  else:data+=b'\n'+key+b'='+value+b'\n'
 return data

def sha(data):return hashlib.sha256(data).hexdigest()

def run(args):
 p=subprocess.run(args,stdin=subprocess.DEVNULL,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(args[0]+' failed rc='+str(p.returncode))
 return p.stdout

def main():
 if os.geteuid()!=0:raise ValueError('Administrator required')
 os.umask(0o077)
 if json.loads(Path('/opt/bussassistent/current/release-identity.json').read_text())['commit']!='5e521cbc658594a47c4568d352a50e46309573c4':raise ValueError('Unexpected release')
 if RECOVERY.is_symlink()or RECOVERY.stat().st_uid!=0:raise ValueError('Unexpected recovery directory')
 default=Path('/etc/default/grub');cfg=Path('/boot/grub/grub.cfg')
 if default.is_symlink()or cfg.is_symlink():raise ValueError('Unexpected GRUB symlink')
 originals={p:p.read_bytes()for p in [default,cfg]}
 archive=RECOVERY/('grub-before-'+str(time.time_ns())+'.tar')
 with tarfile.open(archive,'x')as tar:
  for p in originals:tar.add(p,arcname=str(p).lstrip('/'))
 archive.chmod(0o600)
 result={'backup':str(archive),'backup_sha256':sha(archive.read_bytes()),'before_hashes':{str(p):sha(b)for p,b in originals.items()},'reboot_performed':False,'rollback_used':False}
 try:
  default.write_bytes(rewrite(originals[default]))
  run(['update-grub']);run(['grub-script-check',str(cfg)])
  generated=cfg.read_bytes()
  if not re.search(rb'set timeout_style=menu',generated)or not re.search(rb'set timeout=10(?:\s|$)',generated):raise ValueError('Generated menu does not show required timeout')
  if b'7.0.0-42-generic'not in generated or b'7.0.0-30-generic'not in generated:raise ValueError('Expected kernel recovery entries missing')
  result.update(passed=True,timeout_style='menu',timeout_seconds=10,both_kernel_entries_present=True)
 except Exception as error:
  for p,data in originals.items():p.write_bytes(data)
  run(['grub-script-check',str(cfg)])
  result.update(passed=False,rollback_used=True,failure_message=str(error))
 result['after_hashes']={str(p):sha(p.read_bytes())for p in originals}
 output=WINDOW/'grub-result.json';output.write_text(json.dumps(result,indent=2)+'\n');output.chmod(0o600);os.chown(output,int(os.environ['SUDO_UID']),int(os.environ['SUDO_GID']))
 print(json.dumps(result,indent=2))
 if not result['passed']:raise SystemExit(1)

if __name__=='__main__':main()
