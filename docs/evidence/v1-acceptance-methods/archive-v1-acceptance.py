from pathlib import Path
import hashlib,json,shutil,tarfile
root=Path.cwd(); fresh=Path('D:/IBE160/tmp/v1-delivery-candidate')
out=root/'docs/evidence/v1-acceptance-reproduction';out.mkdir(exist_ok=True)
for name in ['submission-runtime-check.json','v1-acceptance-runtime.log','v1-acceptance-npm.log','v1-acceptance-browser.log','submission-browser-report.json']:
 source=fresh/'tmp'/name;assert source.is_file(),name
 shutil.copyfile(source,out/name)
runtime=json.loads((out/'submission-runtime-check.json').read_text());assert runtime['passed'] is True
report=json.loads((out/'submission-browser-report.json').read_text());assert report['stats']['expected']==3 and report['stats']['unexpected']==0
methods=root/'docs/evidence/v1-acceptance-methods';methods.mkdir(exist_ok=True)
for name in ['prepare-final-reproduction.py','record-delivery-proof.py','archive-v1-acceptance.py','prepare-device-suite.cjs','run-device-suite.py','manual-device.cjs','capture-manual-first.cjs']:
 shutil.copyfile(root/'tmp'/name,methods/name)
config=root/'frontend/playwright.v1-device-temp.config.ts'
if config.exists():
 expected=json.loads((root/'docs/evidence/v1-followup-device-browser-20261029T180012285199Z-4df76182.json').read_text())['source_sha256_before']['frontend/playwright.v1-device-temp.config.ts']
 assert hashlib.sha256(config.read_bytes()).hexdigest()==expected
 shutil.copyfile(config,methods/'playwright.v1-device-temp.config.ts')
 config.unlink()
index={}
for folder in [out,methods]:
 for p in sorted(folder.rglob('*')):
  if p.is_file() and p.name!='index.json':index[str(p.relative_to(root)).replace('\\','/')]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(out/'index.json').write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8')
print('PASS lifecycle,3 browser journeys, exact methods and device config archived; own temporary config removed after hash verification')
