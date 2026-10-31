"""Local-only expanded source/history scan and normalized vulnerability evidence.

No matched credential values are emitted. Binary ASCII scan cannot decode archives.
Trivy JSON inputs are generated locally, with public database downloads only.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import gzip
import json
import math
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/evidence/operations-o3-o6-20261031'
TMP = ROOT/'tmp/operations-followup'
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)
def sha(data): return hashlib.sha256(data).hexdigest()
def save(name,data): (OUT/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
patterns = {
 'private-key':rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----',
 'github':rb'\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,})\b',
 'aws':rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
 'npm':rb'\bnpm_[A-Za-z0-9]{36}\b',
 'jwt':rb'\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{20,}\b',
 'slack':rb'\bxox[baprs]-[A-Za-z0-9-]{20,}\b',
 'google-key':rb'\bAIza[0-9A-Za-z_-]{35}\b',
 'stripe-live':rb'\b[rs]k_live_[A-Za-z0-9]{20,}\b',
 'gitlab':rb'\bglpat-[A-Za-z0-9_-]{20,}\b',
 'openai':rb'\bsk-(?:proj-|svcacct-)[A-Za-z0-9_-]{30,}\b',
 'credential-url':rb'(?:postgres(?:ql)?|mysql|https?)://[^\s/:"\']+:[^\s/@"\']{12,}@',
 'credential-assignment':rb'(?i)(?:password|secret|api[_-]?key|access[_-]?token)\s*[=:]\s*["\']([A-Za-z0-9_+/=-]{20,})["\']',
}
compiled = {k:re.compile(v) for k,v in patterns.items()}
def matches(data, identity):
    result = []
    for rule, pat in compiled.items():
        for m in pat.finditer(data):
            if rule == 'credential-assignment':
                value = m.group(1); n = len(value)
                entropy = -sum((c/n)*math.log2(c/n) for c in Counter(value).values())
                if entropy < 4.2: continue
            result.append({**identity,'rule':rule,'line':data[:m.start()].count(b'\n')+1})
    return result
head = git('rev-parse','origin/main').decode().strip()
objects = git('rev-list','--objects',head).decode().splitlines()
p = subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
counts = Counter(); hits = []
for entry in objects:
    oid, _, name = entry.partition(' ')
    p.stdin.write((oid+'\n').encode());p.stdin.flush()
    header=p.stdout.readline().decode().split();data=p.stdout.read(int(header[2]));p.stdout.read(1)
    if header[1] != 'blob': continue
    counts['binary_ascii_scanned' if b'\0' in data[:8192] else 'text_scanned'] += 1
    hits.extend(matches(data, {'blob':oid,'path':name}))
p.stdin.close();p.wait()
current = []
for parent in [OUT,ROOT/'scripts/operations-followup']:
    for path in parent.rglob('*'):
        if path.is_file() and path.name not in ['secret-audit.json','index.json']:
            current.extend(matches(path.read_bytes(),{'path':str(path.relative_to(ROOT))}))
save('secret-audit.json',{'at_utc':datetime.now(timezone.utc).isoformat(),'history_head':head,
 'commits':int(git('rev-list','--count',head)),'scope':'reachable origin/main blobs plus new evidence/method files',
 'rules':list(patterns),'counts':dict(counts),'history_hits_metadata_only':hits,'current_hits_metadata_only':current,
 'limits':'Heuristics; binary bytes checked only for literal ASCII patterns, not compressed/encrypted content; no absence-of-all-secrets guarantee.'})
audits=[]
for path in sorted(TMP.glob('trivy-*.json')):
    raw=path.read_bytes();d=json.loads(raw)
    groups=[]
    for row in d.get('Results',[]):
        packages=[{k:p.get(k) for k in ['Name','Version','FilePath','AnalyzedBy']} for p in row.get('Packages',[])]
        findings=[{k:v.get(k) for k in ['VulnerabilityID','PkgName','InstalledVersion','FixedVersion','Status','Severity','Title','PrimaryURL','DataSource','PkgPath']} for v in row.get('Vulnerabilities',[])]
        groups.append({'target':row['Target'],'type':row.get('Type'),'package_count':len(packages),'packages':packages,'findings':findings})
    findings=[v for group in groups for v in group['findings']]
    audit={'input_file':path.name,'raw_sha256':sha(raw),'created_at':d.get('CreatedAt'),'scanner':d.get('Trivy'),
           'artifact':d.get('ArtifactName'),'metadata':{k:d.get('Metadata',{}).get(k) for k in ['ImageID','RepoDigests','OS']},
           'severity_counts':dict(Counter(v['Severity'] for v in findings)),'unique_advisories':len({v['VulnerabilityID'] for v in findings}),
           'groups':groups,'qualified_os_detection':bool(d.get('Metadata',{}).get('OS',{}).get('Family') not in [None,'none'])}
    if len(findings) > 1000:
        compressed = path.stem+'-findings.json.gz'
        (OUT/compressed).write_bytes(gzip.compress(json.dumps(groups,separators=(',',':')).encode(),mtime=0))
        audit['groups'] = [{k:v for k,v in g.items() if k != 'findings'} | {'finding_count':len(g['findings'])} for g in groups]
        audit['full_findings_file'] = compressed
    save(path.stem+'-summary.json',audit);audits.append({k:v for k,v in audit.items() if k!='groups'})
save('vulnerability-index.json',{'at_utc':datetime.now(timezone.utc).isoformat(),
 'database':json.loads((TMP/'trivy-cache/db/metadata.json').read_text()),
 'scanner_archive_sha256':sha((TMP/'trivy_0.76.1_windows-64bit.zip').read_bytes()),
 'scanner_checksums_source':'https://github.com/aquasecurity/trivy/releases/tag/v0.76.1',
 'scope':'Local image/package inventory matching; not proof of production image byte identity or exploitability', 'audits':audits})
print(json.dumps({'history_blobs':dict(counts),'history_hits':len(hits),'current_hits':len(current),'audits':len(audits)}))
