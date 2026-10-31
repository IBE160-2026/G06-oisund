"""Capture one explicitly supplied operation; stop caller on nonzero exit."""
from pathlib import Path
from datetime import datetime,timezone
import sys,subprocess,json,hashlib
out=Path(__file__).resolve().parent
root=out.parents[2]
name=sys.argv[1]
assert name.replace('-','').isalnum()
log=out/(name+'.txt');meta=out/(name+'.json')
assert not log.exists() and not meta.exists(), 'Preserve previous attempts'
record={'started_utc':datetime.now(timezone.utc).isoformat(),'command':sys.argv[2:]}
with log.open('wb') as stream:
 result=subprocess.run(sys.argv[2:],cwd=root,stdout=stream,stderr=subprocess.STDOUT)
record.update(finished_utc=datetime.now(timezone.utc).isoformat(),exit_code=result.returncode,output_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
meta.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(log.read_text(encoding='utf-8',errors='replace')[-6000:])
print(json.dumps(record,indent=2))
raise SystemExit(result.returncode)
