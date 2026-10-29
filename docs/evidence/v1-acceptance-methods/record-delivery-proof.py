from pathlib import Path
import subprocess, hashlib, json, urllib.request, re, tarfile
from datetime import datetime, timezone
root=Path.cwd(); target=Path('D:/IBE160/tmp/v1-delivery-candidate')
out=root/'docs/evidence/v1-acceptance-reproduction';out.mkdir(exist_ok=True)
def sha(data):return hashlib.sha256(data).hexdigest()
def cmd(*args):return subprocess.check_output(args,cwd=target,text=True).strip()
record={'at':datetime.now(timezone.utc).isoformat(),'source':cmd('git','rev-parse','HEAD'),'instance':'ibe160-v1-delivery','images':{},'served':{}}
for service in ['api','private-api']:
 container='ibe160-v1-delivery-'+service+'-1'
 image=cmd('docker','inspect',container,'--format','{{.Image}}')
 actual=json.loads(cmd('docker','exec',container,'python','-c',"from pathlib import Path; import hashlib,json; print(json.dumps({str(p.relative_to('/app')):hashlib.sha256(p.read_bytes().replace(b'\\r\\n',b'\\n')).hexdigest() for p in Path('/app/app').rglob('*.py')}))"))
 for name,digest in actual.items():assert digest==sha((target/'backend'/name).read_bytes().replace(b'\r\n',b'\n')),name
 record['images'][service]={'id':image,'all_app_python_normalized_sha256':actual,'matches_snapshot':True}
container='ibe160-v1-delivery-frontend-1'
assets=json.loads(cmd('docker','exec',container,'node','-e',"const fs=require('fs'),p=require('path'),c=require('crypto'),out={};function walk(d){for(const n of fs.readdirSync(d)){const f=p.join(d,n);if(fs.statSync(f).isDirectory())walk(f);else out[p.relative('/app/dist',f)]=c.createHash('sha256').update(fs.readFileSync(f)).digest('hex')}}walk('/app/dist');process.stdout.write(JSON.stringify(out))"))
assert assets, 'No frontend assets'
for name,digest in assets.items():
 with urllib.request.urlopen('http://127.0.0.1:15327/'+name,timeout=3) as r:body=r.read()
 assert sha(body)==digest,name
 record['served'][name]=digest
for port in [18331,18332]:
 with urllib.request.urlopen('http://127.0.0.1:'+str(port)+'/health',timeout=3) as r:health=json.load(r)
 assert health['status']=='ok'
 record[str(port)+'_health']=health
record['frontend_image']=cmd('docker','inspect',container,'--format','{{.Image}}')
(out/'source-proof.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('PASS fresh delivery all API Python source bytes and all served frontend files match actual own images')
