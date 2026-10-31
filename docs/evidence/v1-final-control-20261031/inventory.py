"""Bounded tracked-file and reachable-history audit. Never prints matched secrets."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,hashlib,json,re
from pypdf import PdfReader
root=Path(__file__).resolve().parents[3]; out=Path(__file__).resolve().parent
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
def sha(b):return hashlib.sha256(b).hexdigest()
head=git('rev-parse','HEAD').decode().strip()
names=git('ls-tree','-r','--name-only',head).decode().splitlines()
forbidden=re.compile(r'(^|/)(node_modules|dist|build|\.private-runtime|\.venv|tmp)/|\.(pem|key|pfx|p12|dump|db|sqlite|bak|tar|zip|7z)$|(^|/)\.env$|Sensorveiledning|Prosjektforslag|reflection-report-in-progress',re.I)
record={'at_utc':datetime.now(timezone.utc).isoformat(),'source_commit':head,'tracked_count':len(names),'forbidden_path_matches':[n for n in names if forbidden.search(n)]}
record['source_manifest']={n:sha(git('show',head+':'+n)) for n in names if n.startswith(('backend/','frontend/','scripts/','deploy/','Eksempelfiler/')) or n.startswith('compose')}
c1='3c2287ed68d0cbb1923439fc6ee00254395072a4'
record['changes_from_C1']=git('diff','--name-status',c1,head,'--','backend','frontend','scripts','deploy','Eksempelfiler','compose*').decode().splitlines()
record['reflection_unchanged_from_approved_commit']=not git('diff','e861625',head,'--','docs/submission/ai-reflection.md').strip()
record['ubuntu_unchanged_from_deployed_source']=not git('diff','addd27b14fe4b26ef24d488d847d1c0d59a98946',head,'--','deploy/ubuntu','scripts/server.ps1','scripts/install-server-backup.ps1').strip()
record['pdfs']=[]
for name in [n for n in names if n.endswith('.pdf')]:
    reader=PdfReader(str(root/name)); text='\n'.join(p.extract_text() or '' for p in reader.pages)
    record['pdfs'].append({'path':name,'pages':len(reader.pages),'metadata_keys':sorted((reader.metadata or {}).keys()),'embedded_files':bool(reader.attachments),'synthetic_driver_marker':'Testsjåfør' in text,'direct_owner_name_present':bool(re.search('Jonas|Øisund|oisund',text,re.I))})
patterns={
    'private_key':re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),
    'github_token':re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,})\b'),
    'aws_access_key':re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'npm_token':re.compile(rb'\bnpm_[A-Za-z0-9]{36}\b'),
    'compact_jwt':re.compile(rb'\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{20,}\b'),
}
objects=git('rev-list','--objects',head).decode().splitlines()
paths={line.split(' ',1)[0]:line.split(' ',1)[1] if ' ' in line else '' for line in objects}
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=root,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
hits=[]; scanned=0; binaries=0
for oid,path in paths.items():
    proc.stdin.write((oid+'\n').encode());proc.stdin.flush()
    header=proc.stdout.readline().decode().split()
    size=int(header[2]);data=proc.stdout.read(size);proc.stdout.read(1)
    if header[1]!='blob':continue
    if b'\0' in data[:8192]:binaries+=1;continue
    scanned+=1
    for category,pattern in patterns.items():
        if pattern.search(data):hits.append({'blob':oid,'path':path,'category':category})
proc.stdin.close();proc.wait()
record['reachable_history_scan']={'commits':int(git('rev-list','--count',head)),'text_blobs_scanned':scanned,'binary_blobs_not_text_scanned':binaries,'patterns':list(patterns),'matches_without_values':hits,'limit':'Heuristic text scan; no entropy/password-all-values proof, binary/image or forensic redaction certification.'}
record['method_sha256']=sha(Path(__file__).read_bytes())
(out/'inventory.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k not in ['source_manifest','pdfs']},indent=2,ensure_ascii=False))
