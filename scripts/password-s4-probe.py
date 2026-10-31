"""Synthetic S4 probes. All failures are static; never print credentials/state."""
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import sys
import time
from uuid import uuid4
import httpx
from app import auth
from app.private_storage import database, migrate

ROOT = Path('/state')
ORIGIN = 'https://bus.owner-domain.no'
def check(value, label):
    if not value:
        raise RuntimeError('S4 invariant failed: '+label)
def load():
    return json.loads((ROOT/'state.json').read_text())
def save(s):
    (ROOT/'state.json').write_text(json.dumps(s))
def record(label, details=True):
    path=ROOT/'results.json'
    result=json.loads(path.read_text()) if path.exists() else {}
    result[label]=details
    path.write_text(json.dumps(result,indent=2))
    print('PASS '+label)
def guard():
    check(os.environ.get('PRIVATE_TEST_PROJECT')=='ibe160-private-tests','synthetic marker')
    with database() as conn:
        auth.require_synthetic_accounts(conn)
def snapshot():
    result={}
    with database() as conn:
        tables=[r['tablename'] for r in conn.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")]
        for table in tables:
            if table in ('sessions','login_limits','recovery_proofs','recovery_audit','private_migrations','security_settings','accounts'):continue
            rows=conn.execute('SELECT to_jsonb(t) AS row FROM '+table+' t ORDER BY to_jsonb(t)::text').fetchall()
            result[table]={'rows':len(rows),'sha256':hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()}
    return result
class InternalTransport(httpx.BaseTransport):
    """TLS termination simulated only here; product HTTPS cookies/Origin unchanged."""
    def __init__(self): self.inner=httpx.HTTPTransport()
    def handle_request(self,request):
        path=request.url.raw_path.decode()
        forwarded=httpx.Request(request.method,'http://gateway:8080/private-api'+path,
            headers={**dict(request.headers),'host':'bus.owner-domain.no'},content=request.read(),extensions=request.extensions)
        return self.inner.handle_request(forwarded)
    def close(self):self.inner.close()
def client(admitted=True):
    tokens=httpx.get('http://access-gate:8082').json()
    return httpx.Client(base_url=ORIGIN,transport=InternalTransport(),timeout=25,
        headers={'Cf-Access-Jwt-Assertion':tokens['valid']} if admitted else {})
def headers(c):return {'Origin':ORIGIN,'X-CSRF-Token':c.get('/auth/csrf').json()['csrf_token']}
def post(c,path,body):return c.post(path,headers=headers(c),json=body)
def register_token(s,token):
    check(bool(token),'successful login token registered')
    if token not in s['markers']:s['markers'].append(token)
    save(s)
def login(c,s,password=None,index=0):
    r=post(c,'/auth/login',{'username':s['names'][index],'password':password or s['old']})
    if r.status_code==200:register_token(s,c.cookies.get(auth.SESSION))
    return r
def issue(s,index=0):
    from test_password_recovery_operator import cli
    name=s['names'][index]
    status,output=cli(name,[(b'bekrefte',name),(b'TRYGT:','TRYGT'),(b'MOTTATT','MOTTATT')])
    check(status==0,'PTY issuance')
    match=re.search(rb'Engangskode: ([A-Za-z0-9_-]+)',output)
    check(bool(match),'PTY one-time display')
    code=match[1].decode();s['markers'].append(code);save(s);scan_db()
    return code
def retained(s):check(snapshot()==s['business'],'all business content/ownership/deadlines')
def seed():
    s={'names':['synthetic-s4-'+uuid4().hex for _ in range(2)],'old':secrets.token_urlsafe(24),
       'new':secrets.token_urlsafe(24),'recovered':secrets.token_urlsafe(24),'markers':[]}
    s['markers']=[s['old'],s['new'],s['recovered']]
    s['ids']=[str(auth.provision(name,s['old'])) for name in s['names']]
    from test_private_drafts import save as draft_save
    from test_private_workdays import prepare,confirm
    from test_private_outcomes import start,closing
    from test_account_notices import send,command,content
    from test_pdf_import import synthetic_text_pdf
    with client() as a,client() as second,client() as b:
        for c,index in [(a,0),(second,0),(b,1)]:check(login(c,s,index=index).status_code==200,'seed login')
        s['old_sessions']=[a.cookies.get(auth.SESSION),second.cookies.get(auth.SESSION),b.cookies.get(auth.SESSION)]
        s['markers']+=s['old_sessions']
        saved,a_command=draft_save(a)
        check(saved.status_code==200,'retained draft')
        s['a_draft']=saved.json();s['a_draft_command']=a_command
        b_saved,_=draft_save(b)
        check(b_saved.status_code==200,'B retained draft')
        s['b_draft']=b_saved.json()
        for terminal in [False,True]:
            draft,_,decision=prepare(a);day=confirm(a,draft,decision).json();start(a,day)
            if terminal:check(post(a,'/workdays/'+day['id']+'/close',closing()).status_code==200,'terminal day')
        notice=send(a,command(content=content())).json()
        check('result' in notice,'account notice')
        imported=a.post('/imports/pdf',headers={**headers(a),'Content-Type':'application/pdf'},content=synthetic_text_pdf())
        check(imported.status_code==200,'generated PDF import')
        save(s);s['pre_code']=issue(s)
    s['business']=snapshot()
    with database() as conn:s['accounts']=json.loads(json.dumps(conn.execute('SELECT * FROM accounts ORDER BY id').fetchall(),default=str))
    save(s)
    record('G1 seed drafts active terminal days notices receipts generated PDF',s['business'])
def journeys():
    s=load()
    with client() as a,client() as other,client() as fresh,client(False) as denied:
        check(denied.get('/auth/session').status_code==403,'outer missing identity')
        check(login(a,s).status_code==login(other,s,index=1).status_code==200,'journey login')
        for route in ['/auth/password/change','/auth/password/recover']:
            check(denied.post(route,json={}).status_code==403,'password POST missing admission')
            with client() as invalid:
                invalid.headers['Cf-Access-Jwt-Assertion']='synthetic-invalid-admission'
                check(invalid.post(route,json={}).status_code==403,'password POST invalid admission')
            for boundary in [{},{'Origin':'https://foreign.invalid'}, {'Origin':ORIGIN,'X-CSRF-Token':'synthetic-invalid-csrf'}]:
                rejected=fresh.post(route,headers=boundary,json={})
                check(rejected.status_code==403 and rejected.headers.get('cache-control')=='no-store','password POST Origin CSRF no-store')
        for route,body,fields in [('/auth/password/change',dict(current_password=s['old'],new_password=s['new'],confirmation=s['new']),['current_password','new_password','confirmation']),('/auth/password/recover',dict(username=s['names'][0],code=s['pre_code'],new_password=s['new'],confirmation=s['new']),['username','code','new_password','confirmation'])]:
            c=a if route.endswith('change') else fresh
            for field in fields:
                invalid={**body,field:'\ud800'*12}
                r=c.post(route,headers={**headers(c),'Content-Type':'application/json'},content=json.dumps(invalid).encode())
                check(r.status_code==422,'escaped surrogate safe 422 '+route+' '+field)
                check(not any(m in r.text for m in s['markers']),'validation secret absence')
        changed=post(a,'/auth/password/change',dict(current_password=s['old'],new_password=s['new'],confirmation=s['new']))
        check(changed.status_code==200,'change success')
        check(changed.headers.get('cache-control')=='no-store' and all(flag in changed.headers.get('set-cookie','') for flag in ['Secure','HttpOnly','SameSite=strict','Max-Age=0']),'change secure deletion no-store')
        scan_db()
        for token in s['old_sessions'][:2]:
            with client() as stale:
                stale.cookies.set(auth.SESSION,token,domain='bus.owner-domain.no',path='/')
                for path in ['/auth/session','/drafts','/workdays','/notices']:
                    check(stale.get(path).status_code==401,'old authority rejected')
                check(post(stale,'/draft-operations',{}).status_code==401,'old mutation rejected')
        check(other.get('/auth/session').status_code==200,'B unaffected')
        check(login(a,s).status_code==401 and login(a,s,s['new']).status_code==200,'old/new password')
        retained(s)
        # Own-account operator has no app cookie or password; separate PTY process.
        code=issue(s)
        for name,candidate in [(s['names'][1],code),('synthetic-unknown',code),(s['names'][0],'invalid')]:
            r=post(fresh,'/auth/password/recover',dict(username=name,code=candidate,new_password=s['recovered'],confirmation=s['recovered']))
            check(r.status_code==400,'neutral invalid proof')
        body=dict(username=s['names'][0],code=code,new_password=s['recovered'],confirmation=s['recovered'])
        recovered=post(fresh,'/auth/password/recover',body)
        check(recovered.status_code==200,'PTY recovery through gateway')
        check(recovered.headers.get('cache-control')=='no-store' and all(flag in recovered.headers.get('set-cookie','') for flag in ['Secure','HttpOnly','SameSite=strict','Max-Age=0']),'recovery secure deletion no-store')
        scan_db()
        check(post(fresh,'/auth/password/recover',body).status_code==400,'one use')
        check(a.get('/auth/session').status_code==401,'change-era session revoked')
        check(fresh.get('/auth/session').status_code==401,'no automatic login')
        check(login(fresh,s,s['new']).status_code==401 and login(fresh,s,s['recovered']).status_code==200,'recovered password')
        check(other.get('/auth/session').status_code==200,'B after recovery')
        check(other.get('/drafts/'+s['b_draft']['id']).json()==s['b_draft'],'B own data preserved')
        check(other.get('/drafts/'+s['a_draft']['id']).status_code==404,'B cannot read A draft')
        check(post(other,'/drafts/'+s['a_draft']['id'],s['a_draft_command']).status_code==404,'B cannot mutate A draft')
        s['markers']+=list(fresh.cookies.values())+list(other.cookies.values())
    s['post_code']=issue(s)
    with database() as conn:
        s['post_accounts']=json.loads(json.dumps(conn.execute('SELECT * FROM accounts ORDER BY id').fetchall(),default=str))
        check(bool(conn.execute("SELECT 1 FROM recovery_proofs WHERE digest=%s AND state='active'",(auth.digest(s['post_code']),)).fetchone()),'postbackup active proof')
    retained(s);save(s);scan_db()
    record('G2 gateway change PTY recovery invalid input all-session isolation preservation')
def invalidate(phase):
    s=load();retained(s)
    with database() as conn:
        before=conn.execute('SELECT count(*) AS n FROM sessions').fetchone()['n']
        conn.execute('DELETE FROM sessions')
        conn.execute("UPDATE recovery_proofs SET state='revoked' WHERE state='active'")
        check(conn.execute('SELECT count(*) AS n FROM sessions').fetchone()['n']==0,'restored sessions invalidated')
        check(not conn.execute("SELECT 1 FROM recovery_proofs WHERE state='active'").fetchone(),'restored proofs invalidated')
        current=conn.execute('SELECT * FROM accounts ORDER BY id').fetchall()
        old=json.loads(json.dumps(current,default=str))==s['accounts']
        check(old==(phase=='pre'),'snapshot old/new hash distinction')
        if phase=='post':check(json.loads(json.dumps(current,default=str))==s['post_accounts'],'exact post account snapshot restored')
    s['compat_password']=s['old'] if phase=='pre' else s['recovered'];save(s)
    record('R1 '+phase+' restore quiesced authority invalidation',{'restored_sessions_removed':before,'old_hash_restored':old,'business':snapshot()})
def prior():
    s=load()
    # Exact archived V1 source, current DB kept, no migration downgrade.
    migrate()
    token,account=auth.authenticate(s['names'][0],s['compat_password'],'synthetic-prior')
    register_token(s,token);scan_db()
    check(str(account['owner'])==s['ids'][0],'prior code hash/account compatibility')
    retained(s)
    with database() as conn:conn.execute('DELETE FROM sessions')
    record('R2 prior-code compatibility '+('old' if s['compat_password']==s['old'] else 'current')+' hash')
def pre_schema():
    s=load();retained(s)
    with database() as conn:
        conn.execute('DROP TABLE recovery_proofs,recovery_audit')
        conn.execute("DELETE FROM private_migrations WHERE name='015_password_recovery.sql'")
    record('M1 populated pre015 fixture reconstructed while quiesced')
def upgrade():
    s=load();retained(s)
    with database() as conn:
        check(json.loads(json.dumps(conn.execute('SELECT * FROM accounts ORDER BY id').fetchall(),default=str))==s['accounts'],'upgrade accounts hashes unchanged')
        check(bool(conn.execute("SELECT 1 FROM private_migrations WHERE name='015_password_recovery.sql'").fetchone()),'upgrade migration applied')
    migrate();migrate();retained(s)
    s['pre_code']=issue(s);save(s)
    record('M2 additive startup migration and repeated migration preserve populated rows')
def resumed(phase):
    s=load();migrate();migrate();retained(s)
    if phase!='restart':
        with client() as stale,client() as anonymous:
            stale.cookies.set(auth.SESSION,s['old_sessions'][0],domain='bus.owner-domain.no',path='/')
            check(stale.get('/drafts').status_code==401,'restored stale session denied after reopen')
            restored_code=s['post_code'] if phase=='post-restored' else s['pre_code']
            check(post(anonymous,'/auth/password/recover',dict(username=s['names'][0],code=restored_code,new_password=s['new'],confirmation=s['new'])).status_code==400,'restored proof denied after reopen')
    with client() as c:
        check(login(c,s,s['recovered']).status_code==200,'restart credential retained')
        # Negative control uses this newly registered resumed token, never output.
        rejected=False
        try:scan_bytes(c.cookies.get(auth.SESSION).encode(),s)
        except RuntimeError:rejected=True
        check(rejected,'resumed token scan negative control')
        scan_db()
        check(c.get('/drafts').status_code==200,'same retained workspace')
        if phase=='restored':
            check(login(c,s).status_code==401,'old restored hash replaced before reopening')
    retained(s);record('R3 '+phase+' migrate reapply login preserved')
def settle():
    # Trusted disposable maintenance process, with API/gateway still stopped.
    # Not a production procedure or a new administrative product interface.
    from app import password_recovery as recovery
    from types import SimpleNamespace
    s=load()
    with database() as conn:conn.execute('DELETE FROM login_limits')
    code=issue(s)
    recovery.redeem(SimpleNamespace(cookies={},client=SimpleNamespace(host='synthetic-maintenance')),
        s['names'][0],code,s['recovered'],s['recovered'])
    with database() as conn:
        check(not conn.execute('SELECT 1 FROM sessions').fetchone(),'settled restore sessions absent')
        check(not conn.execute("SELECT 1 FROM recovery_proofs WHERE state='active'").fetchone(),'settled restore proofs absent')
    retained(s);scan_db();record('R4 old hash settled by trusted synthetic recovery before reopening')
def scan_bytes(logs,s):
    check(not any(m.encode() in logs for m in s['markers']),'secret absent logs/database')
def scan_db(logs=b''):
    s=load()
    with database() as conn:
        for table in ['accounts','sessions','recovery_proofs','recovery_audit']:
            logs+=str(conn.execute('SELECT * FROM '+table).fetchall()).encode()
    scan_bytes(logs,s)

if __name__=='__main__':
    try:
        guard();phase=sys.argv[1]
        if phase=='seed':seed()
        elif phase=='pre-schema':pre_schema()
        elif phase=='upgrade':upgrade()
        elif phase=='journeys':journeys()
        elif phase.startswith('invalidate-'):invalidate(phase.split('-')[1])
        elif phase=='prior':prior()
        elif phase=='settle':settle()
        elif phase=='scan':scan_db(sys.stdin.buffer.read())
        elif phase=='scan-db':scan_db()
        else:resumed(phase)
    except Exception as error:
        # Never expose exception repr/locals/requests. Static invariant labels only.
        message=str(error) if isinstance(error,RuntimeError) and str(error).startswith('S4 invariant failed:') else type(error).__name__
        print('FAIL '+message,file=sys.stderr)
        sys.exit(1)
