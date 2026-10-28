from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,tarfile,importlib.util
ROOT=Path('D:/IBE160');STORY=ROOT/'tmp/story-12-4'
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True,encoding='utf-8').strip()
def blob(rev,name):return subprocess.check_output(['git','show',rev+':'+name],cwd=ROOT)
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(b):return b.replace(b'\r\n',b'\n')
pre=json.loads((ROOT/'tmp/story124-main-integration/preflight.json').read_text())
merge=git('rev-parse','HEAD');branch=pre['story_head'];accepted='5ee35efb3753bed10bafc21a53a88fec3d93b287'
checks=[]
def check(name,value):checks.append({'name':name,'passed':bool(value)});assert value,name
check('merge has exact expected parents',git('show','-s','--format=%P',merge).split()==[pre['main_before'],branch])
check('entire merge tree equals accepted story tree',git('rev-parse',merge+'^{tree}')==git('rev-parse',branch+'^{tree}'))
product=['frontend','backend','scripts','Eksempelfiler','compose.story124.yaml','.dockerignore']
check('zero product/tool/test/fixture diff from accepted product commit',not git('diff','--name-only',accepted,merge,'--',*product))
for name in ['frontend/src/PrivateAccess.tsx','frontend/src/pdfUpload.ts','frontend/playwright.tablet.config.ts','_bmad-output/implementation-artifacts/spec-mobile-pdf-upload.md','docs/evidence/mobile-pdf-upload.md']:
 check('mobile correction blob unchanged: '+name,blob('c0e809f',name)==blob(merge,name))
r=json.loads((ROOT/'docs/evidence/12-4-browser-20261028T150525812602Z-427d7a87.json').read_text())
source={k:v for k,v in r['source_sha256_before'].items() if k.startswith(('frontend/src/','backend/'))};lineend=[]
for name,expected in source.items():
 tested=(STORY/name).read_bytes();main=(ROOT/name).read_bytes()
 check('tested bytes unchanged: '+name,sha(tested)==expected)
 check('main checkout equals tested source after LF/CRLF normalization: '+name,canonical(main)==canonical(tested))
 if main!=tested:lineend.append(name)
archives=[]
for index in ['docs/evidence/12-4-bundles/20261028T150525812602Z-427d7a87-browser.index.json','docs/evidence/12-4-bundles/20261028T151438853623Z-f3e6ccfa-tablet-browser.index.json','docs/evidence/12-4-experience-device-20261028.index.json']:
 data=json.loads((ROOT/index).read_text());archive=ROOT/data['archive'];expected=data.get('entries',data.get('files'));check('archive hash: '+index,sha(archive.read_bytes())==data.get('archive_sha256',data.get('sha256')))
 with tarfile.open(archive) as t:actual={m.name:sha(t.extractfile(m).read()) for m in t if m.isfile()}
 check('all archived member bytes: '+index,actual==expected);archives.append({'index':index,'members':len(actual),'sha256':sha(archive.read_bytes())})
spec=importlib.util.spec_from_file_location('preflight',ROOT/'tmp/story124-main-integration/preflight.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
after=module.containers();check('all existing27 container identities/images/ports/start/restarts/source-mounts preserved',{r['name']:r for r in after}=={r['name']:r for r in pre['containers_before']})
http=module.http();check('all five unauthenticated loopback responses/transport categories preserved',http==pre['http_before'])
sprint=(ROOT/'_bmad-output/implementation-artifacts/sprint-status.yaml').read_text();check('12.4 done;12.5 backlog','12-4-verify-the-complete-user-flow: done' in sprint and '12-5-deliver-a-reproducible-submission: backlog' in sprint)
for name in ['spec-12-4-complete-user-flow.md','spec-12-4-import-experience.md']:
 s=(ROOT/'_bmad-output/implementation-artifacts'/name).read_text().split('---',2)[1];check(name+' accepted/done','status: done' in s and 'owner_acceptance: accepted' in s)
record={'recorded_at':datetime.now(timezone.utc).isoformat(),'merge':merge,'parents':[pre['main_before'],branch],'merged_tree':git('rev-parse',merge+'^{tree}'),'accepted_product':accepted,'checks':checks,'passed':all(x['passed'] for x in checks),'tested_product_source_files':len(source),'line_ending_only_main_vs_tested':lineend,'archives':archives,'containers_after':after,'http_after':http,'test_reuse':'Approved final64/64 real-API/browser,32/32 controlled mobile boundaries and actual Lenovo evidence reused by exact committed product equality. These are not new runs. Fresh main checks: TypeScript noEmit, offline Python12/12 and Node6/6.','product_changes_from_merge':False,'deploy':False}
(ROOT/'docs/evidence/12-4-main-integration.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({'merge':merge,'tree':record['merged_tree'],'checks':len(checks),'passed':record['passed'],'sources':len(source),'lineEndingOnly':len(lineend),'archives':archives,'containersPreserved':len(after),'httpPreserved':True},indent=2))
