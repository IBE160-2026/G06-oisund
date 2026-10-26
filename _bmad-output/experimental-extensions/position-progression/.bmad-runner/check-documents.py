"""Document-only checks; no product imports, tests, database, service or network calls."""
import json, os, re, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT=Path('D:/IBE160-plan-position-progression').resolve()
EXT=ROOT/'_bmad-output/experimental-extensions/position-progression'
RUN=EXT/'research/technical-position-progression-2026-10-26'
assert Path.cwd().resolve()==ROOT
assert EXT.resolve().is_relative_to(ROOT)
KIT=ROOT/'.agents/skills/bmad-deep-recon/scripts/recon_kit.py'
MEM=ROOT/'_bmad/scripts/memlog.py'

def execute(script,*args,allowed=(0,)):
    p=subprocess.run(['uv','run','--no-project',str(script),*map(str,args)],capture_output=True,text=True,encoding='utf-8',env={**os.environ,'PYTHONIOENCODING':'utf-8'})
    if p.returncode not in allowed: raise RuntimeError(p.stdout+p.stderr)
    return p.stdout

def save(name,data):
    target=RUN/name
    assert target.resolve().is_relative_to(EXT.resolve())
    target.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

claims=[
 {'id':1,'claim':'Secure context required; localhost exception does not qualify tablet LAN HTTP','class':'patterns','pub_date':'2026-03-26','status':'verified','sources':[1,6]},
 {'id':2,'claim':'Visible-document delivery and lifecycle suspension preclude a background continuity promise','class':'compatibility','pub_date':'2026-10-16','status':'verified','sources':[1,2]},
 {'id':3,'claim':'Measurement timestamp/accuracy/cache/high-accuracy semantics documented, not tablet performance','class':'patterns','pub_date':'2026-03-26','status':'unverified','sources':[1]},
 {'id':4,'claim':'OS power and permission controls matter; exact browser behavior not qualified','class':'compatibility','pub_date':'2026-10-22','status':'unverified','sources':[3,4]},
 {'id':5,'claim':'Brave help documents site prompts on desktop; Android parity remains unqualified','class':'compatibility','pub_date':'2024-11-11','status':'unverified','sources':[5]},
 {'id':6,'claim':'Entur documents vehicle positions; user-bus and dated-trip linkage is unqualified','class':'compatibility','pub_date':'2026-07-15','status':'unverified','sources':[7,9]},
 {'id':7,'claim':'NSR offers location/mapping/version data; selected route coordinate coverage unqualified','class':'compatibility','pub_date':None,'status':'unverified','sources':[8]},
]
if not (RUN/'claims.json').exists():
    save('claims.json',{'claims':claims,'note':'Null publication dates omitted from date arithmetic and require pre-use recheck; verification is independent-publisher corroboration, not product testing.'})
    for c in claims:
        execute(MEM,'append','--workspace',RUN,'--type','claim','--text',f"ref=[{c['id']}] status={c['status']} class={c['class']} pub={c['pub_date'] or 'unknown'} sources={c['sources']} accessed=2026-10-26 — {c['claim']}")
save('checks/citations.json',json.loads(execute(KIT,'citations',RUN/'research.md')))
tally=json.loads(execute(KIT,'tally',RUN/'.memlog.md'))
save('checks/claim-tally.json',tally)
known=[c for c in claims if c['pub_date']]
save('checks/known-date-claims.json',known)
stale=json.loads(execute(KIT,'staleness',RUN/'checks/known-date-claims.json','--windows',json.dumps({'patterns':24,'compatibility':1}),'--today','2026-10-26',allowed=(0,1)))
save('checks/staleness.json',stale)
report=RUN/'research.md'
content=report.read_text(encoding='utf-8-sig')
content=re.sub(r'^claims_verified:.*\n|^claims_unverified:.*\n','',content,flags=re.M)
content=content.replace("updated: '2026-10-26'",f"updated: '2026-10-26'\nclaims_verified: {tally['claims'].get('verified',0)}\nclaims_unverified: {tally['claims'].get('unverified',0)}")
report.write_text(content,encoding='utf-8')
metrics=json.loads(execute(ROOT/'.agents/skills/bmad-review/scripts/word_metrics.py',report))
save('checks/word-metrics.json',metrics)
broken=[]
for p in EXT.rglob('*.md'):
    text=p.read_text(encoding='utf-8-sig')
    for link in re.findall(r'\]\(([^)]+)\)',text):
        if '://' in link or link.startswith('#'): continue
        target=(p.parent/link.split('#')[0]).resolve()
        if not target.exists(): broken.append({'file':str(p.relative_to(EXT)),'link':link})
tracked=subprocess.check_output(['git','diff','--name-only','HEAD'],text=True).splitlines()
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],text=True).splitlines()
prefix='_bmad-output/experimental-extensions/position-progression/'
boundary=all(p.startswith(prefix) for p in tracked+untracked)
labels=all('EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE' in (EXT/p).read_text(encoding='utf-8-sig') for p in ['README.md','scope.md','source-map.md','research/technical-position-progression-2026-10-26/research.md'])
result={'broken_local_links':broken,'changes_only_in_extension':boundary,'tracked_changes':tracked,'canonical_labels_present':labels,'untracked_files':len(untracked),'product_tests_run':False}
save('checks/documents.json',result)
print(json.dumps({'tally':tally['claims'],'earliest_recheck':stale['earliest_recheck'],'stale_known_date_claims':stale['stale_count'],'documents':result},indent=2))
if broken or not boundary or not labels: raise SystemExit(1)
