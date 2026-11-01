"""Evidence capture for the authorized gateway window. No implicit deploy.

Run explicit existing server.ps1 actions separately. Receipts never overwrite.
No credentials, backup bytes, container Env or private rows are captured.
"""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/evidence/o6-gateway-deploy-20261101'
TMP=ROOT/'tmp/o6-gateway-deploy-20261101'
SSH=['ssh','-i',str(Path.home()/'.ssh/ibe160_server_ed25519'),'-o','IdentitiesOnly=yes','-o','BatchMode=yes',
     '-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=10','jonas@192.168.1.139']


def capture(name,args,check=True):
    OUT.mkdir(exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
    if (OUT/(name+'.json')).exists() or (OUT/(name+'.txt')).exists():raise RuntimeError('Receipt exists: '+name)
    start=datetime.now(timezone.utc).isoformat()
    p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    data=(p.stdout+p.stderr).encode('utf-8');(OUT/(name+'.txt')).write_bytes(data)
    (OUT/(name+'.json')).write_text(json.dumps(dict(command=args,start_utc=start,end_utc=datetime.now(timezone.utc).isoformat(),
       exit=p.returncode,output_sha256=hashlib.sha256(data).hexdigest()),indent=2)+'\n')
    print(name,'exit',p.returncode,flush=True)
    if check and p.returncode:raise RuntimeError('Control failed: '+name+' '+p.stderr[-1000:])
    return p.stdout


def host(name):
    code='\n'.join(['set -eu','date --iso-8601=seconds','cat /opt/bussassistent/current/release-identity.json',
      'cat /proc/sys/kernel/random/boot_id','uname -r',
      "dpkg-query -W -f='${binary:Package}\\t${Version}\\n' libc6 systemd cloudflared",
      'sha256sum /usr/bin/cloudflared /etc/systemd/system/bussassistent.service /etc/systemd/system/cloudflared.service /etc/systemd/system/bussassistent-backup.service /etc/systemd/system/bussassistent-backup.timer',
      'df -h /','df -i /','systemctl --failed --no-pager','systemctl show cloudflared -p MainPID -p NRestarts -p ActiveEnterTimestamp',
      'systemctl is-active bussassistent-backup.timer',"curl -fsS http://127.0.0.1:18083/ready",'sudo -n /usr/local/sbin/bussassistentctl check','sudo -n /usr/local/sbin/bussassistentctl status'])
    return capture(name,SSH+[code])


if __name__=='__main__':
    if sys.argv[1]=='host':host(sys.argv[2])
    elif sys.argv[1]=='backup':capture('backup-windows',['pwsh','-NoProfile','-File','scripts/server.ps1','-Action','Backup'])
    elif sys.argv[1]=='restore':capture('backup-restore',SSH+['sudo -n /usr/local/sbin/bussassistentctl verify-restore'])
    else:raise SystemExit('Explicit phase required')
