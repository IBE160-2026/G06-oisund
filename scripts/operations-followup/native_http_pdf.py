"""Real isolated Uvicorn/PG authentication and PDF upload; synthetic data only."""
import json
import os
import secrets
import subprocess
import sys
import time
import httpx
from app import auth
from app.private_storage import database,migrate
from test_pdf_import import synthetic_text_pdf

assert os.environ.get('OPERATIONS_DISPOSABLE')=='1'
assert os.environ['PRIVATE_DATABASE_URL']=='postgresql://private_work@private-db/private_work'
migrate()
password=secrets.token_urlsafe(32)
owner=auth.provision('synthetic-native-pdf',password)
process=subprocess.Popen([sys.executable,'-m','app.run'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
client=httpx.Client(base_url='http://127.0.0.1:8000',trust_env=False,timeout=40)
def headers():
    r=client.get('/auth/csrf');assert r.status_code==200
    return {'Origin':auth.configuration(),'X-CSRF-Token':r.json()['csrf_token']}
try:
    for _ in range(100):
        try:
            if client.get('/health').status_code==200:break
        except httpx.TransportError:pass
        time.sleep(.1)
    else:raise AssertionError('Isolated Uvicorn not ready')
    pdf=synthetic_text_pdf()
    r=client.post('/imports/pdf',content=pdf,headers={**headers(),'Content-Type':'application/pdf'})
    assert r.status_code==401,r.status_code
    r=client.post('/auth/login',json={'username':'synthetic-native-pdf','password':password},headers=headers())
    assert r.status_code==200,r.status_code
    statuses={}
    for label,body,expected in [('valid',pdf,200),('sqlite-not-pdf',b'SQLite format 3\x00'+b'0'*64,422)]:
        r=client.post('/imports/pdf',content=body,headers={**headers(),'Content-Type':'application/pdf'})
        assert r.status_code==expected,(label,r.status_code)
        assert r.headers['cache-control']=='no-store'
        statuses[label]=r.status_code
        if label=='valid':assert r.json()['activities']
    r=client.post('/imports/pdf',content=pdf,headers={'Origin':auth.configuration(),'Content-Type':'application/pdf'})
    assert r.status_code==403,r.status_code
    with database() as conn:
        assert conn.execute('SELECT count(*) AS n FROM drafts WHERE owner=%s',(owner,)).fetchone()['n']==0
    print(json.dumps(dict(authenticated_pdf_statuses=statuses,unauthenticated=401,no_csrf=403,preview_has_activities=True,no_drafts_written=True)))
finally:
    client.close();process.terminate()
    try:process.wait(timeout=10)
    except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)
