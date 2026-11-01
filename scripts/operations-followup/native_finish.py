"""Verify accepted traces, preservation and evidence bytes; no production action."""
import hashlib
import json
from pathlib import Path
import native_reachability as n

def read(name):return json.loads((n.OUT/name).read_text())
result={}
for label in ['r3-pdf-regression','r3-gate-jwt','r2-http-families','r3-http-pdf']:
    assert read(label+'.json')['exit']==0
    summary=read(label+'-audit-summary.json')
    assert not(summary['target_objects']or summary['target_bindings']or summary['sqlite_events'])
    py=[json.loads(l)for l in (n.OUT/(label+'-python.jsonl')).read_bytes().splitlines()]
    native=[json.loads(l)for l in (n.OUT/(label+'-native.jsonl')).read_bytes().splitlines()]
    pdf={r['pid']for r in py if r['event']=='import'and r['name']=='pdfplumber'}
    audited={r['pid']for r in native}
    assert pdf<=audited
    result[label]={**summary,'pdfplumber_import_pids':sorted(pdf),'all_pdf_worker_pids_have_native_audit_events':True,
      'sqlite_acl_python_import_or_lookup_events':[r for r in py if 'sqlite' in r['name'].lower()or r['name'].startswith('acl_')]}
    assert not result[label]['sqlite_acl_python_import_or_lookup_events']
static={}
for role in ['api-old','gate-old']:
    d=read('r2-static-'+role+'.txt');names=set()
    for path,r in d['all_elf'].items():names.update([Path(path).name,r['soname']])
    missing={p:[dep for dep in d['all_elf'][p]['needed']if dep not in names]for p in d['native_closure']}
    missing={p:v for p,v in missing.items()if v}
    assert not(d['reachable_target_python']or d['native_closure_target_evidence']or missing or d['parse_errors'])
    static[role]=dict(elf_count=len(d['all_elf']),python_modules=len(d['reachable_python_modules']),
      native_closure=len(d['native_closure']),native_roots=len(d['native_roots']),unresolved_dependencies=missing,
      relevant_symbols_or_markers_in_closure=False)
    positive=read('r2-positive-'+role+'-audit-summary.json')
    assert positive['sqlite_events']and len(positive['target_objects'])==3
    assert {'acl_get_file','acl_set_file','acl_extended_file','acl_delete_def_file','sqlite3_open_v2'}<={r['name']for r in positive['target_bindings']}
    assert read('sqlite-guard-'+role+'.txt')['sqlite_connect_blocked']
n.save('accepted-results.json',dict(workloads=result,static=static,positive_controls_and_sqlite_blocking_verified=True))

before=read('environment-before.json');after=n.snapshot()
old={r['Id']:r for r in before['containers']};new={r['Id']:r for r in after['containers']}
different=[key for key,value in old.items()if new.get(key)!=value]
extra=sorted(set(new)-set(old))
assert not different and not extra and sorted(before['volumes'])==sorted(after['volumes'])
expected={'ibe160-o6-gateway:20261101-r1':'sha256:3cae8303e4976d3515db8d515e0d41f53c5a51884a8bc444dfb1046187a65c6a',
 'ibe160-o6-api:20261101-r1':'sha256:efd73839185ba468dea9b8b04be5e857ff1993d8ee67348e07fb53d01712a89e',
 'ibe160-o6-gate:20261101-r1':'sha256:7123555a1f0cc5888839389352554710f741cfce8c8a7f0f0c0b10b7f79701e8',
 'ibe160-o6-postgres:20261101-r2':'sha256:739d55a4454af0ade9c2eb5dbdae8d97a58000aea68ca57eb817598658f93716'}
for tag,ident in expected.items():assert n.run(['docker','image','inspect','-f','{{.Id}}',tag]).stdout.strip()==ident
assert not list(n.TMP.glob('password-*'))
for filename in ['http-fixture-cleanup.json','r2-http-fixture-cleanup.json','r3-http-fixture-cleanup.json']:
    cleanup=read(filename);assert cleanup['password_removed']
    assert n.run(['docker','container','inspect',cleanup['container']],check=False).returncode!=0
    assert n.run(['docker','network','inspect',cleanup['network']],check=False).returncode!=0
n.save('environment-after.json',after)
n.save('preservation.json',dict(existing_containers=len(old),existing_volumes=len(before['volumes']),changed=different,
  extra_containers=extra,volumes_unchanged=True,qualified_images_unchanged=expected,own_http_fixtures_removed=True))
methods=[*n.ROOT.glob('scripts/operations-followup/native*.py'),*n.ROOT.glob('scripts/operations-followup/native_site/*.py'),
 n.ROOT/'scripts/operations-followup/native_audit.c',n.ROOT/'scripts/operations-followup/Dockerfile.native-analysis']
n.save('methods.json',{str(p.relative_to(n.ROOT)).replace('\\','/') : hashlib.sha256(p.read_bytes()).hexdigest()for p in methods})
print('Accepted controls and preservation verified')
