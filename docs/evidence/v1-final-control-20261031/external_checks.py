"""Bounded GETs and public dependency advisories; no cookies, redirects or writes."""
from pathlib import Path
from datetime import datetime,timezone
import urllib.request,urllib.error,urllib.parse,socket,json,hashlib,subprocess
root=Path(__file__).resolve().parents[3]; out=Path(__file__).resolve().parent
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
opener=urllib.request.build_opener(NoRedirect)
record={'at_utc':datetime.now(timezone.utc).isoformat(),'route':'https://app.bussassistent.com','vantage':'Windows owner LAN via public DNS/HTTPS; not an independent WAN scanner','get_cases':[]}
for path in ['/private','/private-api/drafts']:
    for origin in [None,'https://untrusted.example.invalid']:
        headers={'User-Agent':'IBE160-V1-bounded-readonly/1.0'}
        if origin:headers['Origin']=origin
        request=urllib.request.Request(record['route']+path,headers=headers,method='GET')
        try:
            try:response=opener.open(request,timeout=15)
            except urllib.error.HTTPError as e:response=e
            with response:
                body=response.read(1048576)
                location=urllib.parse.urlsplit(response.headers.get('Location',''))
                record['get_cases'].append({'path':path,'origin':origin,'status':response.status,'cache_control':response.headers.get('Cache-Control'),'redirect_host':location.hostname,'redirect_path':location.path,'app_shell':b'<script' in body and b'/assets/' in body,'bytes':len(body),'body_sha256':hashlib.sha256(body).hexdigest(),'access_control_allow_origin':response.headers.get('Access-Control-Allow-Origin')})
        except Exception as e:record['get_cases'].append({'path':path,'origin':origin,'inconclusive_error_type':type(e).__name__})
for family,label in [(socket.AF_INET,'A'),(socket.AF_INET6,'AAAA')]:
    try:record[label]=sorted({r[4][0] for r in socket.getaddrinfo('app.bussassistent.com',443,family,socket.SOCK_STREAM)})
    except OSError as e:record[label]={'unavailable':type(e).__name__}
(out/'external-get.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
packages={}
for path in ['backend/requirements.lock','deploy/tablet/access_gate/requirements.lock']:
    for line in (root/path).read_text().splitlines():
        if '==' in line:
            name,version=line.split('==');packages[name.lower().replace('_','-')]=version
payload={'queries':[{'package':{'name':n,'ecosystem':'PyPI'},'version':v} for n,v in sorted(packages.items())]}
request=urllib.request.Request('https://api.osv.dev/v1/querybatch',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(request,timeout=30) as response:answers=json.load(response)
    audit={'at_utc':datetime.now(timezone.utc).isoformat(),'service':'https://api.osv.dev/v1/querybatch','queries':payload['queries'],'results':answers,'limit':'Known-advisory lookup for exact pins only; not transitive image/OS/supply-chain/penetration certification.'}
except Exception as e:audit={'inconclusive_error_type':type(e).__name__}
(out/'python-advisories.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
result=subprocess.run(['npm.cmd','audit','--package-lock-only','--json','--prefix','frontend'],cwd=root,stdout=subprocess.PIPE,shell=True)
(out/'npm-audit.json').write_bytes(result.stdout)
print(json.dumps({'external_cases':record['get_cases'],'python_queries':len(packages),'python_advisory_matches':sum(len(r.get('vulns',[])) for r in audit.get('results',{}).get('results',[])) if 'results' in audit else None,'npm_audit_exit':result.returncode},indent=2))
