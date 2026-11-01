"""Synthetic client/upstream for UUID-only isolated gateway runtime checks."""
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import sys
import time
import urllib.request
import urllib.error

class API(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        code=int(self.path.rsplit('/',1)[-1]) if self.path.startswith('/status/') else 200
        body=b'<html>synthetic upstream failure</html>' if code==502 else b'{"synthetic":true}'
        self.send_response(code);self.send_header('Cache-Control','public, max-age=600');self.send_header('Content-Type','text/html' if code==502 else 'application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)

def client(mode):
    token=json.load(urllib.request.urlopen('http://fixture:8000/fixture-tokens'))['valid']
    def request(path):
        req=urllib.request.Request('http://gateway:8080'+path,headers={'Host':'bus.owner-domain.no','Cf-Access-Jwt-Assertion':token})
        try:r=urllib.request.urlopen(req,timeout=6)
        except urllib.error.HTTPError as e:r=e
        with r:
            body=r.read();assert r.headers['Cache-Control']=='no-store',(path,r.status)
            return r.status,body
    if mode=='up':
        for _ in range(50):
            try:
                code,html=request('/private')
                if code==200:break
            except OSError:pass
            time.sleep(.1)
        else:raise AssertionError('Synthetic gateway readiness failed')
        assets=re.findall(r'(?:src|href)="(/assets/[^" ]+)"',html.decode());assert assets
        results={}
        for path in ['/','/private',*assets]:
            status,body=request(path);assert status==200;results[path]={'status':status,'sha256':hashlib.sha256(body).hexdigest()}
        for code in [401,403,404,409,410,422,429,500,502,503]:
            status,body=request('/private-api/status/'+str(code));assert status==code
            assert (body.startswith(b'<html>')) if code==502 else body==b'{"synthetic":true}'
        print(json.dumps({'static_responses':results,'ten_upstream_error_statuses_preserved_no_store':True}))
    elif mode=='api-down':
        assert request('/private')[0]==200
        status,_=request('/private-api/auth/session');assert status in [502,503,504]
        print(json.dumps({'admission_and_shell_remain_available':True,'api_transport_failure_status':status,'no_store':True}))

if __name__=='__main__':
    if sys.argv[1]=='api':HTTPServer(('0.0.0.0',8000),API).serve_forever()
    else:client(sys.argv[1])
