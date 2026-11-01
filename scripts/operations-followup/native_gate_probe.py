"""Reuse the repository's synthetic JWT fixture in the unchanged gate image."""
import ast
import copy
import json
from pathlib import Path
import time
import jwt
import http.client
import threading
from cryptography.hazmat.primitives.asymmetric import rsa
from gate import Admission,BoundedServer,handler_for

POLICY = {'team': 'synthetic-team', 'audience': '1' * 64, 'owner_email': 'owner@owner-domain.no'}
tree=ast.parse(Path('/gate-tests/test_gate.py').read_text())
fixture=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='synthetic_fixture')
exec(compile(ast.Module(body=[fixture],type_ignores=[]),'<trusted synthetic fixture>','exec'))
admission,tokens,token,jwk=synthetic_fixture()
assert admission.allows(tokens['valid'])
refused=0
for name,value in tokens.items():
    if name!='valid':assert not admission.allows(value),name;refused+=1
for value in [None,'','x'*16385]:assert not admission.allows(value);refused+=1
assert admission.keys.uri==admission.issuer+'/cdn-cgi/access/certs'
assert admission.allows(token(headers={'jku':'http://evil.invalid/key','x5u':'http://evil.invalid/cert'}))
admission.keys.jwk_set_cache.put(None)
def unavailable():raise jwt.PyJWKClientError('synthetic outage')
admission.keys.fetch_data=unavailable
assert not admission.allows(tokens['valid'])
admission,tokens,*_=synthetic_fixture()
server=BoundedServer(('127.0.0.1',0),handler_for(admission))
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
http_cases=0
try:
    for name,value in tokens.items():
        connection=http.client.HTTPConnection('127.0.0.1',server.server_port,timeout=5)
        connection.request('GET','/verify',headers={'Cf-Access-Jwt-Assertion':value})
        response=connection.getresponse();response.read()
        assert response.status==(204 if name=='valid' else 403),(name,response.status)
        assert response.headers['Cache-Control']=='no-store'
        connection.close();http_cases+=1
    connection=http.client.HTTPConnection('127.0.0.1',server.server_port,timeout=5)
    connection.request('GET','/verify');response=connection.getresponse();response.read()
    assert response.status==403;connection.close();http_cases+=1
finally:server.shutdown();server.server_close();thread.join(3)
print(json.dumps(dict(valid_signed_token=True,refused_variants=refused,real_loopback_http_cases=http_cases,token_urls_cannot_choose_jwks=True,uncached_jwks_failure_closed=True,external_requests=False)))
