import runpy,shutil,json,subprocess
from pathlib import Path
s=runpy.run_path('/probe/o6_host_step.py');g=s['install'].__globals__
r=Path('/root/o6-private');r.mkdir(mode=0o700);(r/'packages').mkdir(mode=0o700)
for p in Path('/input').glob('*/*.deb'):
 target=r/'packages'/p.name;target.write_bytes(p.read_bytes());target.chmod(0o600)
g['RECOVERY']=r;g['LOGFILE']=r/'commands.jsonl'
results=[]
for label,old in [('baseline',True),('candidate',False),('returned',True)]:
 s['install']('systemd',old)
 versions=subprocess.run(['dpkg-query','-W','-f=${Version}\n',*s['SYSTEMD']],capture_output=True,text=True,check=True).stdout.splitlines()
 assert len(versions)==10 and set(versions)=={'259.5-0ubuntu3.4'if old else'259.9-0ubuntu0.1'},(label,versions)
 results.append({'phase':label,'versions':versions})
assert r.stat().st_mode&0o777==0o700 and (r/'packages').stat().st_mode&0o777==0o700
print(json.dumps({'network':'none','all_three_phases_passed':True,'private_recovery_directory_still_0700':True,'results':results},indent=2))
print((r/'commands.jsonl').read_text())
