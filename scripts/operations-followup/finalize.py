"""Verify preserved Docker resources, source scope, methods and evidence index."""
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/evidence/operations-o3-o6-20261031'
def run(*args):return subprocess.check_output(args,cwd=ROOT).decode('utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def normalized(d):
    for c in d['containers']:
        c['Mounts'].sort(key=lambda m:m['Destination'])
        c['State'].get('Health',{}).pop('Log',None)
    d['containers'].sort(key=lambda c:c['Id']);d['volumes'].sort(key=lambda v:v['Name'])
    return d
before=json.loads((OUT/'docker-before.json').read_text())
ids=run('docker','ps','-aq').split()
containers=json.loads(run('docker','inspect',*ids))
names=run('docker','volume','ls','-q').split()
after={'containers':[{k:c[k] for k in ('Id','Name','Image','Created','State','RestartCount','Mounts')} for c in containers],
       'volumes':json.loads(run('docker','volume','inspect',*names))}
old_ids={c['Id'] for c in before['containers']}
old_names={v['Name'] for v in before['volumes']}
additions={'containers':[{'Id':c['Id'],'Name':c['Name'],'Created':c['Created']} for c in after['containers'] if c['Id'] not in old_ids],
           'volumes':[v['Name'] for v in after['volumes'] if v['Name'] not in old_names]}
retained={'containers':[c for c in after['containers'] if c['Id'] in old_ids],
          'volumes':[v for v in after['volumes'] if v['Name'] in old_names]}
assert normalized(before)==normalized(retained), 'A preexisting resource changed or disappeared'
original_after=json.loads((OUT/'docker-after.json').read_text())
assert normalized(before)==normalized(original_after), 'Initial preservation error was not limited to health log rotation'
assert not run('git','diff','v1.0.0','--','backend','frontend','deploy','docs/submission/ai-reflection.md').strip()
assert run('git','rev-parse','v1.0.0^{commit}').strip()=='d367a0e47198aeecc52358258cb6825eecdc8c4a'
assert not [x for x in run('docker','ps','-a','--format','{{.Names}}').splitlines() if x.startswith('ibe160-ops-')]
assert not [x for x in run('docker','network','ls','--format','{{.Name}}').splitlines() if x.startswith('ibe160-ops-')]
for path in OUT.rglob('*.json'):
    json.loads(path.read_text(encoding='utf-8-sig'))
for path in OUT.glob('*.json.gz'):
    json.loads(gzip.decompress(path.read_bytes()))
result={'at_utc':datetime.now(timezone.utc).isoformat(),'baseline':'5cee9e03d03d2c9c165c7f8fec64aa3e146959ab',
        'preexisting_containers':len(before['containers']),'preexisting_volumes':len(before['volumes']),
        'lifecycle_images_mounts_volumes_preserved':True,'ignored_comparison_field':'State.Health.Log only',
        'initial_preservation_failure_explained_by_health_log_rotation_only':True,
        'own_test_containers_networks_absent':True,'product_and_approved_reflection_unchanged':True,
        'concurrent_additions_preserved_not_created_by_this_runner':additions,
        'v1_target':'d367a0e47198aeecc52358258cb6825eecdc8c4a',
        'methods_sha256':{str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'scripts/operations-followup').glob('*.py')}}
(OUT/'final-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
index={str(p.relative_to(OUT)):sha(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='index.json'}
(OUT/'index.json').write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
