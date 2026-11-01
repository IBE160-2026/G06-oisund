"""Authorized O6 host maintenance. One phase only; fixed packages and rollback."""
import hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
WINDOW=Path('/tmp/ibe160-o6-window.uNfjQHcy')
RECOVERY=Path('/var/backups/bussassistent/o6-pre-5e521cbc')
RELEASE='5e521cbc658594a47c4568d352a50e46309573c4'
EXPECTED_BACKUP='86e3fd3246c6ab65d1d3ba0021f1831cd7cd34c7be4b45c939105aa2a075bc87'
HASHES={'libnss-systemd_259.5-0ubuntu3.4_amd64.deb': '9dc03fc62f6010bb1ca252a8403e1f9848dd629756e8cd657afa6b15f35222d1', 'libpam-systemd_259.5-0ubuntu3.4_amd64.deb': 'f27ddf40b22f231732899e3d3fcd3a622b88666c02cd5e32690a92794ba92d38', 'libsystemd-shared_259.5-0ubuntu3.4_amd64.deb': '9b30b1e96cc8b48f94a2df5c1cbee7690e16f727d71b40c458a64aabe15db35f', 'libsystemd0_259.5-0ubuntu3.4_amd64.deb': 'd14d911e893527ee8d75855289bd180f94676607177aeae46946093584b493ce', 'libudev1_259.5-0ubuntu3.4_amd64.deb': '160b6b18d41c94171a3a6894cbc05f183a534adf8775c2c6fbdd550c4cf42534', 'systemd-cryptsetup_259.5-0ubuntu3.4_amd64.deb': '1e276f5437760fa5720b878b6af373e0692412671537dd8ba31e30208aff3ab8', 'systemd-resolved_259.5-0ubuntu3.4_amd64.deb': '99f133977b1d262c8344cd88acb10eaaa091e95370693aee162560476760cb9e', 'systemd-sysv_259.5-0ubuntu3.4_amd64.deb': '2c76e690808c26fbc3bdbfe47d760ba50e7dcb0a821eded3d00412117ae0516e', 'systemd_259.5-0ubuntu3.4_amd64.deb': '1b2eca56c5cfdbc1aca78591a68f94b7e1c996abd52095587069776b816b9dca', 'udev_259.5-0ubuntu3.4_amd64.deb': 'b4de0a05d8cd58e5de0ebb7a5c73784dda6a61df2fe5129affa7e4a5aef282ad', 'libnss-systemd_259.9-0ubuntu0.1_amd64.deb': '9dedf0a0680089779e1ea439b435f4793f8d477620b9ef430e00169e0d1540c3', 'libpam-systemd_259.9-0ubuntu0.1_amd64.deb': '872c0c6ffe9ce1f8c0574d8629834f17d1f0f1741fc371e9aa62cb282de9c47a', 'libsystemd-shared_259.9-0ubuntu0.1_amd64.deb': 'c9b8ee0c0dff4f25a3d27b3d8ac344e7cc31d2f02fd65c75d818562a86aea8ab', 'libsystemd0_259.9-0ubuntu0.1_amd64.deb': 'b255521b18a289d40149e93aef1ee881fb8d25c16fa0993db97c4168f4f82bb1', 'libudev1_259.9-0ubuntu0.1_amd64.deb': '578af34e1b720ffdf3e816e168dd4719d06f2efd15cc0c193a34b9d9ee6237ca', 'systemd-cryptsetup_259.9-0ubuntu0.1_amd64.deb': '8fb5cdacd68b3f6ab91ae621f953c859868c641d9aa07c6910da1a489393b2bf', 'systemd-resolved_259.9-0ubuntu0.1_amd64.deb': 'e6f8f287f6c094d0999f6ed78018e9763d5450d8efa28fc30c64650e8c92de4f', 'systemd-sysv_259.9-0ubuntu0.1_amd64.deb': '23944d67a293918a2eecb4e3f0de747c8f0ad434805d638850f7bab50dff2923', 'systemd_259.9-0ubuntu0.1_amd64.deb': 'f4189a9737929afa8c7e9fcb3cc86ec4d93982477d272c55e67fb4e34a0a13b8', 'udev_259.9-0ubuntu0.1_amd64.deb': '8b7e29109bf3d0e32199b1f2111535740c9cb81e9d4273ec6f05682459cfc3f4', 'cloudflared-2026.10.6-amd64.deb': '13d9a724a4d4271958a3728982ee983870a100959a159d2fa263b3450d0be72a', 'cloudflared-2026.10.7-amd64.deb': '70b1a1e0f46033ffc8d90b406e554044ba6cbf2e4360295ef1163aed31e09393'}
SYSTEMD=['systemd','libnss-systemd','libpam-systemd','libsystemd-shared','libsystemd0','libudev1','systemd-cryptsetup','systemd-resolved','systemd-sysv','udev']
ENV={**os.environ,'DEBIAN_FRONTEND':'noninteractive','NEEDRESTART_MODE':'l'}

def run(args):
 p=subprocess.run(args,capture_output=True,text=True,env=ENV)
 if p.returncode:raise RuntimeError('Command failed: '+args[0]+' rc='+str(p.returncode))
 return p.stdout

def digest(path):
 with path.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()

def validate_simulation(text):
 if re.search(r'^Remv ',text,re.M):raise ValueError('Removal proposed')
 installs=re.findall(r'^Inst ([^ :]+)(?::[^ ]+)? .*?\(([^ ]+)',text,re.M)
 if {p for p,v in installs}!=set(SYSTEMD)or any(v!='259.9-0ubuntu0.1'for p,v in installs):raise ValueError('Unexpected package solution')

def ready_tunnel():
 for _ in range(45):
  p=subprocess.run(['curl','-fsS','--max-time','3','http://127.0.0.1:18083/ready'],capture_output=True,text=True)
  if p.returncode==0 and json.loads(p.stdout).get('readyConnections',0)>0:return
  time.sleep(2)
 raise ValueError('Tunnel not ready')

def health():
 run(['sudo','-n','/usr/local/sbin/bussassistentctl','check'])
 for unit in ['docker','ssh','systemd-resolved','cloudflared','bussassistent-backup.timer']:run(['systemctl','is-active','--quiet',unit])
 ready_tunnel()

def packages(phase,old=False):
 if phase=='systemd':
  version='259.5-0ubuntu3.4'if old else'259.9-0ubuntu0.1'
  return [str(RECOVERY/'packages'/(p+'_'+version+'_amd64.deb'))for p in SYSTEMD]
 return [str(RECOVERY/'packages'/('cloudflared-'+('2026.10.6'if old else'2026.10.7')+'-amd64.deb'))]

def install(phase,old=False):
 if phase=='systemd':run(['apt-get','-y','--no-download','--allow-downgrades','install',*packages(phase,old)])
 else:
  run(['dpkg','-i',*packages(phase,old)])
  run(['systemctl','restart','cloudflared'])

def main():
 if os.geteuid()!=0 or len(sys.argv)!=2 or sys.argv[1]not in ['systemd','cloudflared']:raise ValueError('Root and explicit phase required')
 phase=sys.argv[1]
 active=json.loads(Path('/opt/bussassistent/current/release-identity.json').read_text())['commit']
 if active!=RELEASE:raise ValueError('Unexpected active release')
 if digest(RECOVERY/'host-config.tar')!=EXPECTED_BACKUP:raise ValueError('Host backup changed')
 recovery_packages=RECOVERY/'packages';recovery_packages.mkdir(mode=0o700,exist_ok=True)
 for name,expected in HASHES.items():
  source=WINDOW/'packages'/name
  if source.is_symlink():raise ValueError('Unexpected package symlink')
  data=source.read_bytes()
  if hashlib.sha256(data).hexdigest()!=expected:raise ValueError('Package hash mismatch')
  target=recovery_packages/name
  if not target.exists():
   with target.open('xb')as f:f.write(data)
   target.chmod(0o600)
  if digest(target)!=expected:raise ValueError('Recovery package mismatch')
 (RECOVERY/'o6_host_step.py').write_bytes(Path(__file__).read_bytes())
 (RECOVERY/'o6_host_step.py').chmod(0o600)
 (RECOVERY/'rollback-systemd.txt').write_text('apt-get -y --no-download --allow-downgrades install '+' '.join(packages('systemd',True))+'\n')
 (RECOVERY/'rollback-cloudflared.txt').write_text('dpkg -i '+packages('cloudflared',True)[0]+'\nsystemctl restart cloudflared\n')
 units=[Path('/etc/systemd/system')/n for n in ['bussassistent.service','cloudflared.service','bussassistent-backup.service','bussassistent-backup.timer']]
 before={str(p):digest(p)for p in units};health()
 run(['/usr/local/sbin/bussassistentctl','backup'])
 if phase=='systemd':validate_simulation(run(['apt-get','-s','install',*[p+'=259.9-0ubuntu0.1'for p in SYSTEMD]]))
 result={'phase':phase,'active_release':active,'backup_hash_verified':True,'all_22_recovery_packages_hash_verified':True,'rollback_used':False}
 try:
  install(phase)
  if {str(p):digest(p)for p in units}!=before:raise ValueError('Project unit changed')
  if phase=='systemd':
   versions=run(['dpkg-query','-W','-f=${Version}\n',*SYSTEMD]).splitlines()
   if len(versions)!=10 or set(versions)!={'259.9-0ubuntu0.1'}:raise ValueError('Systemd versions mismatch')
   manager=run(['systemctl','show','-p','Version'])
   if '259.9'not in manager:raise ValueError('PID1 manager not updated')
   result['manager_version']=manager.strip()
  else:
   version=run(['/usr/bin/cloudflared','--version']).strip()
   if '2026.10.7'not in version:raise ValueError('Cloudflared version mismatch')
   pid=run(['systemctl','show','cloudflared','-p','MainPID','--value']).strip()
   if digest(Path('/proc')/pid/'exe')!=digest(Path('/usr/bin/cloudflared')):raise ValueError('Running tunnel binary mismatch')
   result['cloudflared_version']=version;result['running_binary_sha256']=digest(Path('/usr/bin/cloudflared'))
  health();result['passed']=True
 except Exception as error:
  result['passed']=False;result['failure_type']=type(error).__name__
  try:install(phase,True);health();result['rollback_used']=True;result['rollback_health_passed']=True
  except Exception:result['rollback_health_passed']=False
 result['unit_hashes_preserved']={str(p):digest(p)for p in units}==before
 output=WINDOW/(phase+'-result.json');output.write_text(json.dumps(result,indent=2)+'\n');output.chmod(0o600);os.chown(output,int(os.environ['SUDO_UID']),int(os.environ['SUDO_GID']))
 print(json.dumps(result,indent=2))
 if not result['passed']:raise SystemExit(1)

if __name__=='__main__':main()
