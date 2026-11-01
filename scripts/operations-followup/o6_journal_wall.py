"""Compensate CVE-2026-40228 by disabling emergency terminal broadcasts."""
import hashlib,json,os,re,subprocess,time
from pathlib import Path
TARGET=Path('/etc/systemd/journald.conf.d/70-bussassistent-wall.conf')
CONTENT=b'[Journal]\nForwardToWall=no\n'
RECOVERY=Path('/var/backups/bussassistent/o6-pre-5e521cbc')
WINDOW=Path('/tmp/ibe160-o6-final.qr9SSt4b')

def run(args):
 p=subprocess.run(args,stdin=subprocess.DEVNULL,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(args[0]+' failed rc='+str(p.returncode))
 return p.stdout

def effective_wall(text):
 values=re.findall(r'(?m)^\s*ForwardToWall\s*=\s*(\S+)\s*$',text)
 return values[-1].lower()if values else None

def main():
 if os.geteuid()!=0:raise ValueError('Administrator required')
 os.umask(0o077)
 if json.loads(Path('/opt/bussassistent/current/release-identity.json').read_text())['commit']!='5e521cbc658594a47c4568d352a50e46309573c4':raise ValueError('Unexpected release')
 if TARGET.is_symlink():raise ValueError('Unexpected target symlink')
 if any('journald.forward_to_wall'in arg for arg in Path('/proc/cmdline').read_text().split()):raise ValueError('Kernel override requires separate review')
 previous=TARGET.read_bytes()if TARGET.exists()else None
 if previous is not None and previous!=CONTENT:raise ValueError('Existing operator config must be preserved')
 backup=RECOVERY/('journal-wall-before-'+str(time.time_ns())+'.json')
 backup.write_text(json.dumps({'target':str(TARGET),'existed':previous is not None,'previous_hex':previous.hex()if previous is not None else None})+'\n');backup.chmod(0o600)
 result={'cve':'CVE-2026-40228','backup':str(backup),'backup_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'rollback_used':False,'reboot_performed':False}
 try:
  TARGET.parent.mkdir(exist_ok=True)
  TARGET.write_bytes(CONTENT);TARGET.chmod(0o644)
  if effective_wall(run(['systemd-analyze','cat-config','systemd/journald.conf']))!='no':raise ValueError('Effective config is not no')
  run(['systemctl','restart','systemd-journald']);run(['systemctl','is-active','--quiet','systemd-journald'])
  run(['/usr/local/sbin/bussassistentctl','check'])
  ready=json.loads(run(['curl','-fsS','--max-time','5','http://127.0.0.1:18083/ready']))
  if ready.get('readyConnections',0)<1:raise ValueError('Tunnel not ready')
  result.update(passed=True,effective_ForwardToWall='no',journal_active=True,tunnel_connections=ready['readyConnections'],dropin_sha256=hashlib.sha256(TARGET.read_bytes()).hexdigest())
 except Exception as error:
  if previous is None:TARGET.unlink(missing_ok=True)
  else:TARGET.write_bytes(previous)
  run(['systemctl','restart','systemd-journald'])
  result.update(passed=False,rollback_used=True,failure_message=str(error))
 output=WINDOW/'journal-wall-result.json';output.write_text(json.dumps(result,indent=2)+'\n');output.chmod(0o600);os.chown(output,int(os.environ['SUDO_UID']),int(os.environ['SUDO_GID']))
 print(json.dumps(result,indent=2))
 if not result['passed']:raise SystemExit(1)

if __name__=='__main__':main()
