"""Read-only, allowlisted production inventory. Run manually with existing sudo.

No Env, labels, logs, credentials, DB queries, files from /run/secrets or updates.
docker exec starts only short metadata readers, never service lifecycle commands.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

NAMES = {role:'bussassistent-'+role+'-1' for role in ['private-api','access-gate','gateway','private-db']}
CONTAINER_TEMPLATE = '''{"id":{{json .Id}},"image_id":{{json .Image}},"image_ref":{{json .Config.Image}},"user":{{json .Config.User}},"read_only":{{json .HostConfig.ReadonlyRootfs}},"privileged":{{json .HostConfig.Privileged}},"cap_add":{{json .HostConfig.CapAdd}},"cap_drop":{{json .HostConfig.CapDrop}},"security_opt":{{json .HostConfig.SecurityOpt}},"network_mode":{{json .HostConfig.NetworkMode}},"ports":{{json .NetworkSettings.Ports}},"running":{{json .State.Running}},"pid":{{json .State.Pid}},"started_at":{{json .State.StartedAt}},"restart_count":{{json .RestartCount}}}'''
IMAGE_TEMPLATE = '''{"id":{{json .Id}},"repo_digests":{{json .RepoDigests}},"architecture":{{json .Architecture}},"os":{{json .Os}},"layers":{{json .RootFS.Layers}}}'''

def sha(data):return hashlib.sha256(data).hexdigest()
def command(args):
    p=subprocess.run(args,capture_output=True,timeout=30)
    return p.returncode,p.stdout,p.stderr
def inspect(name):
    code,data,_=command(['docker','inspect','--format',CONTAINER_TEMPLATE,name])
    if code:raise RuntimeError('Cannot inspect named production container')
    return json.loads(data)
def exec_read(name,args,user=None):
    command_line=['docker','exec']
    if user:command_line+=['--user',user]
    return command(command_line+[name]+args)

PYTHON_METADATA = r'''
import json,hashlib
from pathlib import Path
result={'distributions':[],'vendor_manifests':[],'source_files':{}}
for base in Path('/usr/local/lib').glob('python*/site-packages'):
 for p in sorted(base.glob('*.dist-info/METADATA')):
  fields=[s for s in p.read_text(errors='replace').splitlines() if s.startswith(('Name: ','Version: '))]
  result['distributions'].append({'path':str(p),'fields':fields})
 p=base/'pip/_vendor/vendor.txt'
 if p.is_file():
  result['vendor_manifests'].append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pins':[s.strip() for s in p.read_text().splitlines() if s.strip() and not s.lstrip().startswith('#')]})
 for pkg in ['certifi','urllib3','msgpack']:
  for prefix in [base,base/'pip/_vendor']:
   p=prefix/pkg/'__init__.py'
   if p.is_file():
    result.setdefault('vendor_file_hashes',{})[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
for base in [Path('/app/app'),Path('/gate')]:
 if base.is_dir():
  paths=base.rglob('*.py') if str(base)=='/app/app' else [base/'gate.py']
  for p in sorted(paths):
   if p.is_file():
    data=p.read_bytes();result['source_files'][str(p)]={'sha256':hashlib.sha256(data).hexdigest(),'lf_sha256':hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()}
print(json.dumps(result))
'''

def nginx_summary(data):
    """Keep directive metadata/hashes; never emit arbitrary config literals."""
    text=data.decode(errors='replace').replace('\r\n','\n')
    maps=[];other=[];block=[]
    for line in text.splitlines():
        stripped=line.strip()
        if block:
            block.append(line)
            if stripped=='}':maps.append('\n'.join(block));block=[]
        elif re.match(r'^map\s',stripped):block=[line]
        else:other.append(line)
    if block:raise ValueError('Unclosed map block: do not classify captures')
    allowed={}
    for line in other:
        match=re.match(r'^\s*(listen|proxy_http_version|ignore_invalid_headers|large_client_header_buffers|slice|proxy_cache_background_update)\s+([^;]+);',line)
        if match:allowed.setdefault(match[1],[]).append(match[2])
    return {'config_sha256':sha(data),'directives':allowed,
        'map_blocks':[{'sha256_lf':sha(m.encode()),'regex_lines':sum(bool(re.match(r'\s*[\'\"]?~',s)) for s in m.splitlines()),'volatile':bool(re.search(r'\bvolatile\s*;',m))} for m in maps],
        'numeric_capture_refs_outside_maps':re.findall(r'\$[1-9][0-9]*','\n'.join(s for s in other if not s.lstrip().startswith('#'))),
        'grpc_pass_present':bool(re.search(r'^\s*grpc_pass\s',text,re.M)),
        'rewrite_present':bool(re.search(r'^\s*rewrite\s',text,re.M)),
        'proxy_cache_present':bool(re.search(r'^\s*proxy_cache\s',text,re.M)),
        'raw_config_exported':False}

def main():
    if os.geteuid()!=0:raise SystemExit('Run manually with existing sudo; no privilege changes are made.')
    identity=json.loads(Path('/opt/bussassistent/current/release-identity.json').read_text())
    before={role:inspect(name) for role,name in NAMES.items()}
    if not all(c['running'] for c in before.values()):raise SystemExit('A production container is not running. Stop inventory.')
    result={'schema':1,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'method_sha256':sha(Path(__file__).read_bytes()),'release':identity,'containers':before,'images':{},'inventory':{}}
    for role,name in NAMES.items():
        image=before[role]['image_id']
        code,data,_=command(['docker','image','inspect','--format',IMAGE_TEMPLATE,image])
        result['images'][role]=json.loads(data) if code==0 else {'exit':code}
        record={};result['inventory'][role]=record
        for kind,args in [('debian',['dpkg-query','-W','-f=${binary:Package}\t${Version}\t${source:Package}\n']),('alpine',['apk','info','-v'])]:
            code,data,_=exec_read(name,args)
            record[kind]={'exit':code,'lines':data.decode(errors='replace').splitlines() if code==0 else []}
        if role in ['private-api','access-gate']:
            code,data,_=exec_read(name,['python','-B','-c',PYTHON_METADATA],'10001:10001')
            record['python']={'exit':code,'metadata':json.loads(data) if code==0 else None}
        if role=='gateway':
            code,data,err=exec_read(name,['nginx','-T'],'101:101')
            record['nginx']={'exit':code,'stderr_sha256':sha(err),'summary':nginx_summary(data) if code==0 else None}
        if role=='private-db':
            code,data,_=exec_read(name,['sha256sum','/usr/local/bin/gosu'])
            record['gosu_hash']={'exit':code,'sha256':data.decode().split()[0] if code==0 else None}
    after={role:inspect(name) for role,name in NAMES.items()}
    result['lifecycle_unchanged']=before==after
    result['release_unchanged']=identity==json.loads(Path('/opt/bussassistent/current/release-identity.json').read_text())
    result['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(json.dumps(result,indent=2))
    if not result['lifecycle_unchanged'] or not result['release_unchanged']:raise SystemExit(2)

if __name__=='__main__':main()
