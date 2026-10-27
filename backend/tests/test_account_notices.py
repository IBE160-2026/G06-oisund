"""Cross-day account incidents on guarded synthetic PostgreSQL and real HTTP."""
import concurrent.futures
from datetime import datetime, timedelta, timezone
from pathlib import Path
from contextlib import contextmanager
from uuid import uuid4
import httpx
from psycopg.types.json import Jsonb
from app import auth
from app import workday_notice_storage, private_storage, draft_storage
from app.workday_notice_domain import NoticeRecord, SaveNotice
from app.private_storage import database, cleanup, migrate
from test_private_access import client, users, synthetic_only, headers, login, URL
from test_private_selection import opened
from test_private_workdays import prepare, confirm, facts
from test_private_outcomes import start, closing


def content(**values):
    return {'title': 'Synthetic account incident', 'line_tags': ['20', '24'], 'valid_until': '2031-01-04', **values}


def command(revision=0, **values):
    return {'operation_id': str(uuid4()), 'expected_revision': revision, **values}


_admitted_commands = set()


def send(c, body, notice=None, action=None):
    if notice is None and body['expected_revision'] == 0 and not c.get('/workday-notice-operations/'+body['operation_id']).is_success:
        # Issue once per original command; never replace an ID on retry.
        if body['operation_id'] not in _admitted_commands:
            issued = c.post('/notice-operations', headers=headers(c), json={})
            assert issued.status_code == 200, issued.text
            body['operation_id'] = issued.json()['operation_id']
        _admitted_commands.add(body['operation_id'])
    payload = body
    return c.post('/notices'+('/'+notice if notice else '')+('/'+action if action else ''), headers=headers(c), json=payload)


def reader(c, plan):
    response = c.get('/workdays/'+plan['id']+'/notice-reader')
    assert response.status_code == 200, response.text
    return response.json()


def test_cross_day_shared_identity_edit_check_and_original_day_removal(client, users):
    _, a = opened(client, users)
    body = command(content=content(summary='One incident', description='Full source text', source_note='SMS'))
    response = send(client, body); assert response.status_code == 200, response.text
    original = response.json(); n = original['result']
    assert n['workday_id'] is None and n['valid_until'] == '2031-01-04T23:59:59+01:00'
    assert n['expires_at'] == '2031-01-11T22:59:59Z'
    assert response.headers['cache-control'] == 'no-store'
    value = facts(); value['service_date'] = '2031-01-03'
    value['activities'][0].update(line='24', start='2031-01-03T10:00+01:00', end='2031-01-03T11:00+01:00')
    draft, _, decisions = prepare(client, value)
    b = confirm(client, draft, decisions).json()
    assert [c['notice']['id'] for c in reader(client, a)['candidates']] == [n['id']]
    assert [c['notice']['id'] for c in reader(client, b)['candidates']] == [n['id']]
    checked = send(client, command(1), n['id'], 'check').json()['result']
    edited = send(client, command(2, content=content(title='Shared edit')), n['id']).json()['result']
    for plan in [a,b]:
        shown = reader(client, plan)['candidates'][0]['notice']
        assert shown['id']==n['id'] and shown['title']=='Shared edit' and shown['checked_at']==checked['checked_at']
    start(client, a)
    assert client.post('/workdays/'+a['id']+'/close', headers=headers(client), json=closing()).status_code == 200
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        conn.execute('DELETE FROM workdays WHERE id=%s', (a['id'],))
    cleanup(); migrate(); migrate()
    assert reader(client,b)['candidates'][0]['notice']==edited
    assert client.get('/workday-notice-operations/'+body['operation_id']).json()==original
    assert send(client,body).json()==original
    assert client.get('/notices').json()['notices']==[edited]
    with httpx.Client(base_url=URL) as other:
        assert login(other,users,1).status_code==200
        assert other.get('/notices').json()['notices']==[]
        assert other.get('/notices/'+n['id']).status_code==404
        assert send(other,command(3),n['id'],'check').status_code==404
        assert other.get('/workday-notice-operations/'+body['operation_id']).status_code==404


def test_required_deadline_exact_clock_dst_and_terminal_history(client, users):
    assert login(client,users).status_code==200
    for ending in [None, '2020-01-01', '2031-03-30T02:30+01:00']:
        assert send(client,command(content=content(valid_until=ending))).status_code==422
    n = send(client,command(content=content(valid_until='2031-10-26T02:30:12+02:00'))).json()['result']
    assert n['valid_until']=='2031-10-26T02:30:12+02:00'
    for day, expected in [('2031-03-30','2031-03-30T23:59:59+02:00'),('2031-10-26','2031-10-26T23:59:59+01:00')]:
        dated=send(client,command(content=content(valid_until=day))).json()['result']
        assert dated['valid_until']==expected
    assert send(client,command(1,content=content(valid_until='2031-10-27')),n['id']).status_code==200
    ended_body=command(2)
    ended=send(client,ended_body,n['id'],'end').json()['result']
    assert ended['status']=='ended_manually'
    assert timedelta(days=7)-timedelta(seconds=1) < datetime.fromisoformat(ended['expires_at'])-datetime.now(timezone.utc) <= timedelta(days=7)
    for action in ['check','end',None]:
        assert send(client,command(3,**({'content':content()} if action is None else {})),n['id'],action).status_code==409
    assert send(client,ended_body,n['id'],'end').json()['result']==ended
    assert client.get('/notices/'+n['id']).json()==ended


def test_expiry_extension_race_uses_server_clock_after_account_lock(client,users):
    assert login(client,users).status_code==200
    live=send(client,command(content=content())).json()['result']
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        conn.execute("UPDATE workday_notices SET valid_until=clock_timestamp()+interval '2 seconds' WHERE id=%s",(live['id'],))
    extension=command(1,content=content(valid_until='2032-01-01'))
    extended=send(client,extension,live['id']); assert extended.status_code==200
    assert extended.json()['result']['id']==live['id'] and extended.json()['result']['revision']==2
    assert send(client,extension,live['id']).json()==extended.json()
    created=command(content=content())
    n=send(client,created).json()['result']
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        conn.execute("UPDATE workday_notices SET valid_until=clock_timestamp()+interval '0.4 seconds' WHERE id=%s",(n['id'],))
    with database() as held:
        held.execute('SELECT id FROM accounts WHERE id=%s FOR UPDATE',(users[1][0],))
        with concurrent.futures.ThreadPoolExecutor() as pool:
            task=pool.submit(send,client,command(1,content=content(valid_until='2032-01-01')),n['id'])
            held.execute('SELECT pg_sleep(0.6)'); held.commit()
            assert task.result().status_code==409
    assert send(client,command(1),n['id'],'check').status_code==409
    current=client.get('/notices/'+n['id']).json()
    assert current['revision']==1 and current['status']=='registered'
    assert send(client,created).json()['result']==n
    assert client.get('/notices/'+n['id']).json()==current
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        conn.execute("UPDATE workday_notices SET expires_at=clock_timestamp()-interval '1 second' WHERE id=%s",(n['id'],))
    assert client.get('/notices/'+n['id']).status_code==410
    assert client.get('/workday-notice-operations/'+created['operation_id']).status_code==410
    cleanup()
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM workday_notices WHERE id=%s',(n['id'],)).fetchone()
        assert not conn.execute('SELECT 1 FROM account_notice_operations WHERE id=%s',(created['operation_id'],)).fetchone()


def test_concurrent_revision_extension_once_and_no_force_overwrite(client,users):
    assert login(client,users).status_code==200
    n=send(client,command(content=content())).json()['result']
    cookie=dict(client.cookies)
    def extension(day):
        with httpx.Client(base_url=URL,cookies=cookie) as other:
            return send(other,command(1,content=content(valid_until=day)),n['id']).status_code
    with concurrent.futures.ThreadPoolExecutor() as pool:
        results=list(pool.map(extension,['2032-01-01','2033-01-01']))
    assert sorted(results)==[200,409]
    assert client.get('/notices/'+n['id']).json()['revision']==2


def test_populated_additive_migration_unknown_grace_provenance_and_immutable_receipt(client,users,monkeypatch):
    # Isolated schema models a populated 012 deployment; the real public schema
    # and every ordinary/synthetic account remain untouched.
    schema='synthetic_'+uuid4().hex
    real_database=database
    try:
        with real_database() as conn:
            auth.require_synthetic_accounts(conn)
            conn.execute('CREATE SCHEMA '+schema)
            conn.execute('SET LOCAL search_path TO '+schema)
            migrations=Path('/app/migrations/private')
            for path in sorted(migrations.glob('*.sql')):
                if path.name<'013': conn.execute(path.read_text())
            owner,plan,unknown,ended,dated,expired=[uuid4() for _ in range(6)]
            conn.execute('INSERT INTO accounts VALUES(%s,%s,%s)',(owner,'synthetic-migration','unused'))
            conn.execute("INSERT INTO workdays(id,owner,source_draft_id,source_revision,final_end,expires_at,content,acknowledgements,classifications) VALUES(%s,%s,%s,1,statement_timestamp(),statement_timestamp()+interval '7 days','{}','[]','{}')",(plan,owner,uuid4()))
            lease=conn.execute('SELECT expires_at FROM workdays WHERE id=%s',(plan,)).fetchone()['expires_at']
            for identifier,ending,status in [(unknown,None,'registered'),(ended,'2020-01-01','ended_manually'),(dated,'2031-01-04','registered'),(expired,'2020-01-01','registered')]:
                conn.execute("INSERT INTO workday_notices(id,workday_id,revision,title,line_tags,source_url,valid_until,status,entered_at,edited_at,checked_at,checked_revision) VALUES(%s,%s,3,'Original','[\"20\"]','https://example.org/source',%s,%s,'2019-01-01','2019-01-03','2019-01-02',2)",(identifier,plan,ending,status))
            before=conn.execute('SELECT * FROM workday_notices ORDER BY id').fetchall()
            receipts={}
            for old in before:
                op=uuid4()
                result=NoticeRecord(**old,expires_at=lease).model_dump(mode='json')
                source={key:result[key] for key in ['title','line_tags','source_url','source_updated_at','valid_from','valid_until']}
                body=SaveNotice(operation_id=op,expected_revision=2,expected_lifecycle_revision=0,content=source)
                payload=body.model_dump(mode='json',exclude={'content':{'summary','description','source_note','line_scope'}})
                digest=draft_storage.fingerprint(plan,{'action':'save','notice_id':str(old['id']),**payload})
                conn.execute('INSERT INTO workday_notice_operations VALUES(%s,%s,%s,%s,%s,%s)',(op,owner,plan,digest,Jsonb(result),lease))
                receipts[op]=(result,digest)
            conn.execute((migrations/'013_account_notice_registry.sql').read_text())
            conn.execute((migrations/'014_notice_creation_admissions.sql').read_text())
            for old in before:
                new=conn.execute('SELECT * FROM workday_notices WHERE id=%s',(old['id'],)).fetchone()
                assert all(new[k]==v for k,v in old.items()) and new['owner']==owner
                if old['id']==unknown: assert new['expires_at']==lease
                if old['id'] in {ended,expired}: assert new['expires_at']>datetime.now(timezone.utc)+timedelta(days=6)
            token='synthetic-migration-'+uuid4().hex
            conn.execute('INSERT INTO sessions(token_hash,owner) VALUES(%s,%s)',(auth.digest(token),owner))
            conn.execute('DELETE FROM workdays WHERE id=%s',(plan,))
        @contextmanager
        def isolated():
            with real_database() as conn:
                conn.execute('SET LOCAL search_path TO '+schema)
                auth.require_synthetic_accounts(conn)
                yield conn
        # Import routes before patching their storage dependency: otherwise the
        # module-level health database alias can retain the dropped schema.
        from app.private_main import app
        monkeypatch.setattr(workday_notice_storage,'database',isolated)
        monkeypatch.setattr(private_storage,'database',isolated)
        cleanup()
        # Exercise the real HTTP route and response model after parent deletion,
        # using only the isolated synthetic schema and complete deployed JSON.
        from fastapi.testclient import TestClient
        from app.private_main import app
        http=TestClient(app)
        http.cookies.set(auth.SESSION,token)
        for op,(result,digest) in receipts.items():
            response=http.get('/workday-notice-operations/'+str(op))
            assert response.status_code==200, response.text
            assert response.headers['cache-control']=='no-store'
            assert response.json()=={'operation_id':str(op),'result':result}
            with isolated() as conn:
                historical=conn.execute('SELECT * FROM workday_notice_operations WHERE id=%s',(op,)).fetchone()
                assert historical['result']==result and historical['payload_hash']==digest and historical['workday_id'] is None
        with isolated() as conn:
            assert conn.execute('SELECT count(*) AS n FROM workday_notices').fetchone()['n']==4
            preserved=conn.execute('SELECT * FROM workday_notices WHERE id=%s',(expired,)).fetchone()
            assert preserved['status']=='registered' and preserved['valid_until']<datetime.now(timezone.utc)-timedelta(days=7)
            assert preserved['workday_id'] is None and preserved['expires_at']>datetime.now(timezone.utc)
        http.close()
    finally:
        with real_database() as conn:
            auth.require_synthetic_accounts(conn)
            conn.execute('DROP SCHEMA IF EXISTS '+schema+' CASCADE')


def test_legacy_unknown_end_completion_or_manual_end_and_original_recovery(client,users):
    _,plan=opened(client,users)
    owner=users[1][0]; notice=uuid4(); operation=uuid4()
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        conn.execute("INSERT INTO workday_notices(id,owner,workday_id,revision,title,line_tags,status,entered_at,edited_at,expires_at) SELECT %s,%s,id,1,'Legacy unknown','[\"20\"]','registered',clock_timestamp(),clock_timestamp(),expires_at FROM workdays WHERE id=%s",(notice,owner,plan['id']))
    assert reader(client,plan)['candidates']==[]
    unknown=client.get('/notices/'+str(notice)).json()
    with database() as conn:
        conn.execute('INSERT INTO workday_notice_operations VALUES(%s,%s,%s,%s,%s,%s)',(operation,owner,plan['id'],'deployed-hash',Jsonb(unknown),unknown['expires_at']))
    assert client.get('/workday-notice-operations/'+str(operation)).json()['result']==unknown
    assert send(client,{'operation_id':str(operation),'expected_revision':1,'content':content()},str(notice)).status_code==409
    completed=send(client,command(1,content=content(title='Legacy unknown')),str(notice))
    assert completed.status_code==200
    assert reader(client,plan)['candidates'][0]['notice']['id']==str(notice)
    with database() as conn:
        conn.execute("UPDATE workday_notices SET valid_until=NULL,expires_at=clock_timestamp()+interval '1 hour' WHERE id=%s",(notice,))
        lease=conn.execute('SELECT expires_at FROM workday_notices WHERE id=%s',(notice,)).fetchone()['expires_at']
    ended=send(client,command(2),str(notice),'end'); assert ended.status_code==200
    assert datetime.fromisoformat(ended.json()['result']['expires_at'])==lease


def test_legacy_accounts_above_aggregate_cap_keep_complete_reader_and_paginated_maintenance(client,users):
    _,a=opened(client,users)
    value=facts(); value['service_date']='2031-01-03'
    value['activities'][0].update(line='20',start='2031-01-03T10:00+01:00',end='2031-01-03T11:00+01:00')
    draft,_,decisions=prepare(client,value); b=confirm(client,draft,decisions).json()
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        # Each legacy day admitted fewer than its historical 200-row cap.
        for plan in [a,b]:
            conn.execute("INSERT INTO workday_notices(id,owner,workday_id,revision,title,line_tags,valid_until,status,entered_at,edited_at,expires_at) SELECT gen_random_uuid(),owner,id,1,'Legacy incident '||g.n,'[\"20\",\"Legacy heading\"]','2031-01-04T23:59:59+01:00','registered',clock_timestamp(),clock_timestamp(),'2031-01-11T23:59:59+01:00' FROM workdays CROSS JOIN generate_series(1,125) g(n) WHERE id=%s",(plan['id'],))
    rows=[]; cursor=None
    while True:
        response=client.get('/notices',params={'cursor':cursor} if cursor else {})
        assert response.status_code==200 and response.headers['cache-control']=='no-store'
        page=response.json(); rows.extend(page['notices']); cursor=page['next_cursor']
        if cursor is None: break
    assert len(rows)==len({n['id'] for n in rows})==250
    for plan in [a,b]:
        projected=reader(client,plan)
        assert projected['stored_count']==projected['unmatched_notice_count']==len(projected['candidates'])==250
        assert {c['notice']['id'] for c in projected['candidates']}=={n['id'] for n in rows}
    assert send(client,command(content=content())).status_code==429
    assert send(client,command(1,content=content(title='Reviewed legacy incident')),rows[-1]['id']).status_code==200


def test_receipt_capacity_still_allows_one_idempotent_manual_end(client,users):
    assert login(client,users).status_code==200
    created=command(content=content()); n=send(client,created).json()['result']
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        conn.execute('INSERT INTO account_notice_operations SELECT gen_random_uuid(),owner,notice_id,payload_hash,result,expires_at FROM account_notice_operations CROSS JOIN generate_series(1,1999) WHERE id=%s',(created['operation_id'],))
    assert send(client,command(1),n['id'],'check').status_code==429
    assert send(client,command(1,content=content()),n['id']).status_code==429
    assert send(client,command(0),n['id'],'end').status_code==409
    ending=command(1); accepted=send(client,ending,n['id'],'end')
    assert accepted.status_code==200 and accepted.json()['result']['status']=='ended_manually'
    assert send(client,ending,n['id'],'end').json()==accepted.json()
    assert send(client,command(2),n['id'],'end').status_code==409
    with database() as conn:
        assert conn.execute('SELECT count(*) AS n FROM account_notice_operations WHERE owner=%s',(users[1][0],)).fetchone()['n']==2001


def test_projection_uses_one_instant_for_boundary_inclusion_and_server_now(monkeypatch):
    from app import notice_reader_domain
    from test_notice_reader import fixture,row
    fixed=datetime(2031,1,2,22,tzinfo=timezone.utc)
    class Clock(datetime):
        calls=0
        @classmethod
        def now(cls,tz=None):
            cls.calls+=1
            return fixed+timedelta(microseconds=cls.calls-1)
    monkeypatch.setattr(notice_reader_domain,'datetime',Clock)
    plan=fixture()
    boundary=row(plan); boundary['valid_until']=fixed
    live=row(plan); live['valid_until']=fixed+timedelta(microseconds=1)
    result=notice_reader_domain.NoticeReader(**notice_reader_domain.project(plan,[boundary,live]))
    assert Clock.calls==1 and result.server_now==fixed
    assert [candidate.notice.id for candidate in result.candidates]==[live['id']]
    assert all(candidate.notice.valid_until>result.server_now for candidate in result.candidates)


def test_maintenance_list_uses_same_database_instant_for_retention_and_response(client, users, monkeypatch):
    from types import SimpleNamespace
    assert login(client, users).status_code == 200
    notice = send(client, command(content=content())).json()['result']
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        conn.execute("UPDATE workday_notices SET expires_at=clock_timestamp()+interval '0.3 seconds' WHERE id=%s", (notice['id'],))
    class Connection:
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            result = self.conn.execute(query, params)
            if query.startswith('SELECT * FROM workday_notices WHERE owner='):
                # Hold an already selected row across its retention boundary.
                self.conn.execute('SELECT pg_sleep(0.5)')
            return result
    @contextmanager
    def wrapped():
        with database() as conn: yield Connection(conn)
    monkeypatch.setattr(workday_notice_storage, 'database', wrapped)
    request = SimpleNamespace(cookies={auth.SESSION: client.cookies.get(auth.SESSION)})
    listed = workday_notice_storage.read(request)
    assert listed['notices'] == []
    assert all(row['expires_at'] > listed['server_now'] for row in listed['notices'])
    assert listed['server_now'] > datetime.now(timezone.utc) - timedelta(seconds=0.2)
