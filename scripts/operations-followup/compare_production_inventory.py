"""Bind the owner-run allowlisted export to previous local scan identities/pins."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/evidence/o6-production-identity-20261101'
OLD=ROOT/'docs/evidence/operations-o3-o6-20261031'

def main():
    inventory=json.loads((OUT/'production-inventory.json').read_text(encoding='utf-8-sig'))
    assert inventory['schema']==1
    assert inventory['method_sha256']==hashlib.sha256((ROOT/'scripts/operations-followup/production_inventory.py').read_bytes()).hexdigest()
    assert inventory['lifecycle_unchanged'] and inventory['release_unchanged']
    assert inventory['release']['commit']=='d367a0e47198aeecc52358258cb6825eecdc8c4a'
    result={'release':inventory['release'],'lifecycle_unchanged':True,'roles':{}}
    bindings=json.loads((OUT/'binding-checks.json').read_text()) if (OUT/'binding-checks.json').exists() else {}
    for old_role,role in [('api','private-api'),('gate','access-gate'),('gateway','gateway'),('db','private-db')]:
        old=json.loads((OLD/('trivy-'+old_role+'-summary.json')).read_text())
        live=inventory['inventory'][role];packages={}
        for line in live['debian']['lines']:
            parts=line.split('\t')
            if len(parts)>=2:packages[parts[0].split(':')[0]]=parts[1]
        for line in live['alpine']['lines']:
            m=re.match(r'^(.+)-([0-9][^-]*-r[0-9]+)$',line)
            if m:packages[m[1]]=m[2]
        python=live.get('python',{}).get('metadata') or {}
        for dist in python.get('distributions',[]):
            fields=dict(x.split(': ',1) for x in dist['fields'])
            if 'Name' in fields and 'Version' in fields:packages['pypi:'+fields['Name'].lower().replace('_','-')]=fields['Version']
        vendors={}
        for manifest in python.get('vendor_manifests',[]):
            for pin in manifest['pins']:
                if re.fullmatch(r'[A-Za-z0-9_.-]+==[A-Za-z0-9.+_-]+',pin):
                    name,version=pin.split('==');vendors[name.lower().replace('_','-')]=version
        matched=[];unmatched=[]
        for group in old['groups']:
            for finding in group['findings']:
                if finding['Severity'] not in ['HIGH','CRITICAL']:continue
                name=finding['PkgName'];key=('pypi:'+name.lower().replace('_','-')) if group['type']=='python-pkg' else name
                installed=packages.get(key)
                vendor=vendors.get(name.lower().replace('_','-'))
                record={k:finding.get(k) for k in ['VulnerabilityID','PkgName','InstalledVersion','Severity','FixedVersion']}
                record.update({'actual_package_version':installed,'pip_vendor_manifest_version':vendor})
                gosu_bound=(role=='private-db' and finding['PkgName']=='stdlib'
                    and inventory['images'][role]['id']==old['metadata'].get('ImageID')
                    and bindings.get('gosu_binary_hash_matches') is True)
                if gosu_bound:record['identity_basis']='same scanned image ID and same gosu SHA256'
                (matched if gosu_bound or finding['InstalledVersion'] in [installed,vendor] else unmatched).append(record)
        source={}
        for path,record in python.get('source_files',{}).items():
            local=ROOT/'backend'/path.removeprefix('/app/') if path.startswith('/app/app/') else ROOT/'deploy/tablet/access_gate/gate.py'
            source[path]=local.is_file() and hashlib.sha256(local.read_bytes().replace(b'\r\n',b'\n')).hexdigest()==record['lf_sha256']
        result['roles'][role]={'actual_image':inventory['images'][role],
            'old_scan_image_id':old['metadata'].get('ImageID'),
            'same_image_id_as_local_scan':inventory['images'][role]['id']==old['metadata'].get('ImageID'),
            'os_packages_readable':live['debian']['exit']==0 or live['alpine']['exit']==0,
            'python_metadata_exit':live.get('python',{}).get('exit'),
            'matched_high_critical':matched,'unmatched_requires_review':unmatched,
            'source_lf_matches':source,'pip_vendor_pins':vendors,
            'nginx':live.get('nginx'),'gosu_hash':live.get('gosu_hash')}
    (OUT/'comparison.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({role:{'same_image':r['same_image_id_as_local_scan'],'matched_high_critical':len(r['matched_high_critical']),
        'unmatched':len(r['unmatched_requires_review']),'source_files':len(r['source_lf_matches'])} for role,r in result['roles'].items()},indent=2))

if __name__=='__main__':main()
