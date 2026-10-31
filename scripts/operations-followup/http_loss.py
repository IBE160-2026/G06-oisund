"""Fifteen mutation families against real Uvicorn/PG through a TCP-loss relay.

ONLY the orchestrator's empty tmpfs DB/internal Docker network is supported.
No credentials, response bodies or actual row values are printed.
"""
import hashlib
import http.client
import json
import os
import secrets
import socket
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from uuid import uuid4
import httpx
from psycopg import sql
from app import auth
from app.private_storage import database, migrate

assert os.environ.get('OPERATIONS_DISPOSABLE') == '1'
assert os.environ['PRIVATE_DATABASE_URL'] == 'postgresql://private_work@private-db/private_work'
migrate()
with database() as conn:
    assert conn.execute('SELECT count(*) AS n FROM accounts').fetchone()['n'] == 0
password = secrets.token_urlsafe(32)
auth.provision('synthetic-operations', password)
origin = auth.configuration()
process = subprocess.Popen([sys.executable, '-m', 'app.run'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
mode = 'normal'
accepted = []
class Relay(BaseHTTPRequestHandler):
    def do_POST(self): self.relay()
    def do_GET(self): self.relay()
    def log_message(self, *args): pass
    def relay(self):
        global mode
        current_mode = mode
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        if current_mode == 'before-dispatch':
            self.connection.shutdown(socket.SHUT_RDWR); self.connection.close(); return
        upstream = http.client.HTTPConnection('127.0.0.1', 8000, timeout=10)
        try:
            upstream.request(self.command, self.path, body, dict(self.headers))
            response = upstream.getresponse(); data = response.read()
            if current_mode == 'after-commit':
                assert response.status == 200, f'Fixture expected acceptance, got {response.status}'
                accepted.append({'path': self.path, 'status': response.status,
                                 'reply_sha256': hashlib.sha256(data).hexdigest(),
                                 'no_store': response.getheader('Cache-Control') == 'no-store'})
                self.connection.shutdown(socket.SHUT_RDWR); self.connection.close(); return
            self.send_response(response.status)
            for key, value in response.getheaders():
                if key.lower() not in ('transfer-encoding', 'connection', 'content-length'):
                    self.send_header(key, value)
            self.send_header('Content-Length', str(len(data))); self.end_headers()
            self.wfile.write(data)
        finally:
            upstream.close()

relay = ThreadingHTTPServer(('127.0.0.1', 18000), Relay)
thread = threading.Thread(target=relay.serve_forever, daemon=True); thread.start()
client = httpx.Client(base_url='http://127.0.0.1:18000', timeout=12, trust_env=False)
def request(method, path, body=None, headers=None):
    response = client.request(method, path, json=body, headers=headers)
    assert response.headers.get('cache-control') == 'no-store', (path, response.status_code)
    return response
def headers():
    return {'Origin': origin, 'X-CSRF-Token': request('GET', '/auth/csrf').json()['csrf_token']}
def post(path, body):
    response = request('POST', path, body, headers())
    assert response.status_code == 200, (path, response.status_code)
    return response.json()
def fingerprint():
    result = {}
    with database() as conn:
        names = conn.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename").fetchall()
        for row in names:
            name = row['tablename']
            # Session last-seen timestamps are not mutation effects/receipts.
            if name == 'sessions': continue
            rows = conn.execute(sql.SQL('SELECT row_to_json(t)::text AS value FROM {} t ORDER BY row_to_json(t)::text').format(sql.Identifier(name))).fetchall()
            result[name] = {'count':len(rows), 'sha256':hashlib.sha256('\n'.join(r['value'] for r in rows).encode()).hexdigest()}
    return result
results = []
def exercise(family, path, body, lookup):
    global mode
    h = headers(); before = fingerprint()
    refused = []
    for label, bad in [('no-origin', {'X-CSRF-Token':h['X-CSRF-Token']}),
                       ('foreign-origin', {**h, 'Origin':'https://foreign.invalid'}),
                       ('null-origin', {**h, 'Origin':'null'}),
                       ('no-csrf', {'Origin':origin}),
                       ('bad-csrf', {**h, 'X-CSRF-Token':'synthetic-invalid'})]:
        response = request('POST', path, body, bad)
        assert response.status_code == 403 and fingerprint() == before, label
        refused.append({'case':label, 'status':response.status_code, 'all_non_session_tables_unchanged':True})
    mode = 'before-dispatch'
    try:
        client.post(path, json=body, headers=h)
        raise AssertionError('Expected connection loss before dispatch')
    except httpx.TransportError:
        pass
    finally:
        mode = 'normal'
    assert fingerprint() == before
    mode = 'after-commit'
    try:
        client.post(path, json=body, headers=h)
        raise AssertionError('Expected connection loss after commit')
    except httpx.TransportError:
        pass
    finally:
        mode = 'normal'
    after = fingerprint()
    assert after != before
    receipt = request('GET', lookup)
    assert receipt.status_code == 200 and fingerprint() == after
    replay = request('POST', path, body, h)
    assert replay.status_code == 200 and fingerprint() == after
    assert hashlib.sha256(replay.content).hexdigest() == accepted[-1]['reply_sha256']
    results.append({'family':family, 'negative_controls':refused, 'before':before, 'after':after,
                    'before_dispatch_loss_unchanged':True, 'accepted_reply_dropped':accepted[-1],
                    'receipt_recovered':True, 'exact_replay_no_second_effect':True})
    return replay.json()
try:
    for _ in range(100):
        try:
            if client.get('/health').status_code == 200: break
        except httpx.TransportError: pass
        time.sleep(.1)
    else: raise AssertionError('Uvicorn not ready')
    post('/auth/login', {'username':'synthetic-operations', 'password':password})
    op = post('/draft-operations', {})['operation_id']
    content = {'service_date':'2031-01-02', 'physical_bus':'Syntetisk', 'activities':[]}
    draft = exercise('draft-create', '/drafts', {'operation_id':op,'expected_revision':0,'draft':content}, '/draft-operations/'+op)
    op = post('/draft-operations', {'draft_id':draft['id']})['operation_id']
    content['physical_bus'] = 'Syntetisk endret'
    draft = exercise('draft-update', '/drafts/'+draft['id'], {'operation_id':op,'expected_revision':1,'draft':content}, '/draft-operations/'+op)
    op = str(uuid4())
    exercise('draft-delete', '/drafts/'+draft['id']+'/delete', {'operation_id':op,'expected_revision':2}, '/draft-deletions/'+op)
    op = post('/notice-operations', {})['operation_id']
    content = {'title':'Syntetisk avvik','line_scope':'all','line_tags':[],'valid_until':'2031-01-04'}
    notice = exercise('notice-create','/notices',{'operation_id':op,'expected_revision':0,'content':content},'/workday-notice-operations/'+op)['result']
    for family, suffix in [('notice-update',''),('notice-check','/check'),('notice-end','/end')]:
        op = str(uuid4()); body = {'operation_id':op,'expected_revision':notice['revision']}
        if not suffix: body['content'] = {**content,'title':'Syntetisk endret avvik'}
        notice = exercise(family, '/notices/'+notice['id']+suffix, body, '/workday-notice-operations/'+op)['result']
    def plan(qualify):
        activity = {'id':str(uuid4()), 'type':'manual', 'start':'2031-01-02T10:00+01:00',
                    'end':'2031-01-02T11:00+01:00', 'from_place':'Syntetisk A', 'to_place':'Syntetisk B'}
        op = post('/draft-operations', {})['operation_id']
        draft = post('/drafts', {'operation_id':op,'expected_revision':0,
                     'draft':{'service_date':'2031-01-02','physical_bus':'Syntetisk','activities':[activity]}})
        review = post('/workday-reviews',{'draft_id':draft['id'],'expected_revision':1})
        assert not review['blockers'] and not review['classifications_required']
        body = {'operation_id':review['operation_id'],'expected_revision':1,
                'acknowledgements':[u['id'] for u in review['unknowns']], 'classifications':{}}
        path = '/drafts/'+draft['id']+'/confirm'
        return (exercise('confirm',path,body,'/workday-operations/'+review['operation_id']) if qualify else post(path,body))
    work = plan(True)
    base = '/workdays/'+work['id']
    op = str(uuid4())
    exercise('physical-bus',base+'/physical-bus',{'operation_id':op,'expected_revision':0,'physical_bus':'Syntetisk 2'},'/workday-bus-operations/'+op)
    op = str(uuid4())
    exercise('selection',base+'/selection',{'operation_id':op,'expected_revision':0,'activity_id':work['draft']['activities'][0]['id']},'/workday-selection-operations/'+op)
    op = str(uuid4())
    exercise('start',base+'/start',{'operation_id':op,'expected_revision':0},'/workday-start-operations/'+op)
    op = str(uuid4())
    exercise('activity-outcome',base+'/outcome',{'operation_id':op,'expected_revision':0,'expected_lifecycle_revision':1,
             'activity_id':work['draft']['activities'][0]['id'],'outcome':'completed'},'/workday-outcome-operations/'+op)
    op = str(uuid4())
    exercise('end',base+'/close',{'operation_id':op,'expected_revision':1,'expected_outcome_revision':1,'action':'ended'},'/workday-close-operations/'+op)
    work = plan(False); base = '/workdays/'+work['id']
    post(base+'/start',{'operation_id':str(uuid4()),'expected_revision':0})
    op = str(uuid4())
    exercise('abort',base+'/close',{'operation_id':op,'expected_revision':1,'expected_outcome_revision':0,'action':'aborted'},'/workday-close-operations/'+op)
    op = str(uuid4())
    exercise('plan-delete',base+'/delete',{'operation_id':op,'source_revision':1},'/workday-deletions/'+op)
    print(json.dumps({'transport':'real HTTP Uvicorn/relay; TCP close before dispatch or after full upstream200',
                      'families':results, 'passed':True}, indent=2))
finally:
    client.close(); relay.shutdown(); relay.server_close(); thread.join(2)
    process.terminate()
    try: process.wait(timeout=10)
    except subprocess.TimeoutExpired: process.kill(); process.wait(timeout=5)
