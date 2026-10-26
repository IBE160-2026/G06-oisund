"""Synthetic real PostgreSQL/API contracts for manually maintained notices."""
import concurrent.futures
from contextlib import contextmanager
from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import UUID, uuid4
import httpx
import pytest
from fastapi import HTTPException
from app import auth, workday_notice_storage
from app.private_storage import cleanup, database, migrate
from app.workday_notice_domain import SaveNotice
from test_private_access import client, headers, login, synthetic_only, users, URL
from test_private_selection import opened
from test_private_outcomes import start, closing, read as recap
from test_private_workdays import prepare, confirm, facts, teardown


def command(revision=0, lifecycle=0, **values):
    return {'operation_id': str(uuid4()), 'expected_revision': revision, **values}


def content(**values):
    return {'title': 'Veiarbeid ved Tromsø', 'line_tags': ['020', '24'], 'source_url': 'https://example.org/original', 'source_updated_at': None, 'valid_from': None, 'valid_until': '2031-01-04T23:59:59+01:00', **values}


def send(client, plan, body, notice=None, action=None):
    return client.post('/notices' + ('/' + notice if notice else '') + ('/' + action if action else ''), headers=headers(client), json=body)


def read(client, plan):
    reply = client.get('/notices')
    assert reply.status_code == 200 and reply.headers['cache-control'] == 'no-store'
    return {key: value for key, value in reply.json().items() if key != 'server_now'}


def test_prestart_exact_metadata_independent_nulls_explicit_check_edit_and_end(client, users):
    _, plan = opened(client, users); initial = recap(client, plan)
    payload = command(content=content(title='  Første – veiarbeid  ', line_tags=['020', '24', '020', ' 42 '], valid_until='2031-01-03T02:15+01:00'))
    reply = send(client, plan, payload); assert reply.status_code == 200
    original = reply.json(); n = original['result']; identifier = n['id']
    assert n['revision'] == 1 and n['status'] == 'registered' and n['checked_at'] is n['checked_revision'] is None
    assert n['title'] == 'Første – veiarbeid' and n['line_tags'] == ['020', '24', '42']
    assert n['source_updated_at'] is n['valid_from'] is None and n['valid_until'] == '2031-01-03T02:15:00+01:00'
    assert n['entered_at'] == n['edited_at'] and datetime.fromisoformat(n['expires_at']) == datetime.fromisoformat(n['valid_until']) + __import__('datetime').timedelta(days=7)
    assert send(client, plan, payload).json() == original
    assert client.get('/workday-notice-operations/' + payload['operation_id']).json() == original
    assert client.get('/workdays/' + plan['id'] + '/notices/' + identifier).json() == n
    assert read(client, plan)['notices'] == [n] and recap(client, plan) == initial
    before = datetime.now(timezone.utc)
    checked = send(client, plan, command(1), identifier, 'check').json()['result']
    assert checked['revision'] == checked['checked_revision'] == 2 and datetime.fromisoformat(checked['checked_at']) >= before
    assert checked['edited_at'] == n['edited_at'] and checked['status'] == 'registered'
    edited = send(client, plan, command(2, content=content(title='Ny tittel')), identifier).json()['result']
    assert edited['revision'] == 3 and edited['checked_revision'] == 2 and edited['checked_at'] == checked['checked_at']
    assert edited['entered_at'] == n['entered_at'] and edited['edited_at'] >= n['edited_at']
    ending = command(3); ended = send(client, plan, ending, identifier, 'end').json()
    assert ended['result']['status'] == 'ended_manually' and ended['result']['revision'] == 4
    assert send(client, plan, ending, identifier, 'end').json() == ended
    assert send(client, plan, command(4), identifier, 'end').status_code == 409
    assert send(client, plan, command(4, content=content(title='Cannot revive')), identifier).status_code == 409
    assert send(client, plan, command(4), identifier, 'check').status_code == 409
    latest = ended['result']
    migrate(); migrate(); assert read(client, plan)['notices'] == [latest]


@pytest.mark.parametrize('invalid', [
    {'title': ''}, {'title': ' '}, {'title': 2}, {'title': 'x' * 301}, {'title': 'x\x00y'}, {'title': 'x\ny'},
    {'line_tags': []}, {'line_tags': [' ']}, {'line_tags': [20]}, {'line_tags': ['a' * 301]}, {'line_tags': [str(i) for i in range(51)]}, {'line_tags': '20'},
    {'source_url': 'javascript:alert(1)'}, {'source_url': 'file:///tmp/a'}, {'source_url': 'https://'}, {'source_url': 'https://a/ x'}, {'source_url': 'https://a/\\b'}, {'source_url': 'https://a/' + 'x' * 2048},
    {'source_url': 'https://%/'}, {'source_url': 'https://999.999.999.999'},
    {'source_updated_at': '2031-01-01T01:00'}, {'source_updated_at': '2031-01-01T01:00+02:00'}, {'valid_from': '2026-03-29T02:30+01:00'},
    {'valid_from': '2031-01-02T10:00+01:00', 'valid_until': '2031-01-02T09:00+01:00'}, {'extra': 1},
])
def test_invalid_content_rejected_without_mutation(client, users, invalid):
    _, plan = opened(client, users)
    response = send(client, plan, command(content=content(**invalid)))
    assert response.status_code == 422
    assert read(client, plan)['notices'] == []
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM account_notice_operations WHERE owner=%s', (users[1][0],)).fetchone()


def test_maximum_fields_unicode_url_and_optional_dst_instants(client, users):
    _, plan = opened(client, users)
    values = content(title='ø' * 300, line_tags=['ø' * 37 + f'{i:03}' for i in range(50)], source_url='https://example.org/' + 'x' * (2048 - len('https://example.org/')),
                     source_updated_at='2026-10-25T02:30+02:00', valid_from='2026-10-25T02:30+02:00', valid_until='2031-01-04T02:30+01:00')
    response = send(client, plan, command(content=values)); assert response.status_code == 200
    n = response.json()['result']; assert n['title'] == values['title'] and n['line_tags'] == values['line_tags'] and n['source_url'] == values['source_url']
    assert n['valid_from'] != n['valid_until'] and n['status'] == 'registered'


@pytest.mark.parametrize('source', ['1894-01-01T12:00+00:43', '2026-10-25T02:30+02:00', '2026-10-25T02:30+01:00'])
def test_authoritative_source_clock_roundtrip_and_immutable_old_utc_receipts(client, users, source):
    from psycopg.types.json import Jsonb
    _, plan = opened(client, users)
    body = command(content=content(source_updated_at=source, valid_from=source, line_tags=['020', '20,24', 'Route "A"']))
    receipt = send(client, plan, body).json(); n = receipt['result']
    expected = datetime.fromisoformat(source).isoformat()
    assert all(n[field] == expected for field in ['source_updated_at', 'valid_from'])
    # Simulate an immutable receipt accepted by the prior UTC serializer.
    historical = {**n, **{field: datetime.fromisoformat(source).astimezone(timezone.utc).isoformat().replace('+00:00', 'Z') for field in ['source_updated_at', 'valid_from']}}
    with database() as conn: conn.execute('UPDATE account_notice_operations SET result=%s WHERE id=%s', (Jsonb(historical), body['operation_id']))
    assert client.get('/workday-notice-operations/' + body['operation_id']).json() == receipt
    assert send(client, plan, body).json() == receipt
    edit = {key: n[key] for key in content()}; edit['title'] = 'Kun endret tittel'
    updated = send(client, plan, command(1, content=edit), n['id']); assert updated.status_code == 200
    assert all(updated.json()['result'][field] == expected for field in ['source_updated_at', 'valid_from'])
    assert updated.json()['result']['line_tags'] == body['content']['line_tags']
    with database() as conn: assert conn.execute('SELECT result FROM account_notice_operations WHERE id=%s', (body['operation_id'],)).fetchone()['result'] == historical


@pytest.mark.parametrize('url', ['HTTP://Example.org/Original?A=1#Fragment', 'https://例子.test/ø', 'https://127.0.0.1:8080/source', 'https://[::1]/source'])
def test_compatible_http_source_keeps_original_string(client, users, url):
    _, plan = opened(client, users)
    reply = send(client, plan, command(content=content(source_url=url)))
    assert reply.status_code == 200 and reply.json()['result']['source_url'] == url


def test_revision_target_action_payload_privacy_and_parent_delete(client, users):
    _, plan = opened(client, users); body = command(content=content()); saved = send(client, plan, body).json(); identifier = saved['result']['id']
    for invalid in [{**body, 'expected_revision': True}, {**body, 'expected_revision': '0'}, {**body, 'extra': 1}, {**body, 'expected_lifecycle_revision': True}]:
        assert send(client, plan, invalid).status_code == 422
    assert send(client, plan, {**body, 'content': content(title='Different')}).status_code == 409
    assert send(client, plan, body, identifier).status_code == 409
    assert send(client, plan, command(0, content=content()), identifier).status_code == 409
    assert send(client, plan, command(1), str(uuid4()), 'check').status_code == 404
    lookup = '/workday-notice-operations/' + body['operation_id']
    with httpx.Client(base_url=URL) as other:
        assert other.get(lookup).status_code == 401
        assert login(other, users, 1).status_code == 200
        assert other.get('/notices').json()['notices'] == []
        assert other.get(lookup).status_code == 404 and send(other, plan, body).status_code == 404
    assert client.post('/notices', json=body).status_code == 403
    assert client.post('/workdays/' + plan['id'] + '/delete', headers=headers(client), json={'operation_id': str(uuid4()), 'source_revision': 1}).status_code == 200
    assert client.get(lookup).json() == send(client, plan, body).json() == saved
    with database() as conn:
        assert conn.execute('SELECT 1 FROM workday_notices WHERE id=%s', (identifier,)).fetchone()
        assert conn.execute('SELECT 1 FROM account_notice_operations WHERE id=%s', (body['operation_id'],)).fetchone()


@pytest.mark.parametrize('action', ['save', 'check', 'end'])
def test_terminal_authority_and_atomic_receipt_deadline_shortening(client, users, action):
    _, plan = opened(client, users)
    body=command(content=content()); receipt=send(client,plan,body).json(); identifier=receipt['result']['id']
    start(client,plan)
    closed=client.post('/workdays/'+plan['id']+'/close',headers=headers(client),json=closing())
    assert closed.status_code==200
    fresh=command(1,**({'content':content(title='Account edit')} if action=='save' else {}))
    assert send(client,plan,fresh,identifier,None if action=='save' else action).status_code==200
    assert send(client,plan,command(content=content())).status_code==200
    assert send(client,plan,body).json()==receipt
    assert client.get('/workday-notice-operations/'+body['operation_id']).json()==receipt
    with database() as conn:
        row=conn.execute('SELECT * FROM account_notice_operations WHERE id=%s',(body['operation_id'],)).fetchone()
        current=conn.execute('SELECT expires_at FROM workday_notices WHERE id=%s',(identifier,)).fetchone()
        assert row['expires_at']==current['expires_at'] and row['result']==receipt['result']


def test_pagination_complete_discoverability_record_receipt_limits_expiry_cleanup(client, users):
    _, plan = opened(client, users)
    body = command(content=content()); original = send(client, plan, body).json()
    with database() as conn:
        conn.execute('INSERT INTO workday_notices(id,owner,workday_id,expires_at,revision,title,line_tags,source_url,source_updated_at,valid_from,valid_until,status,entered_at,edited_at,checked_at,checked_revision) SELECT gen_random_uuid(),owner,workday_id,expires_at,revision,title,line_tags,source_url,source_updated_at,valid_from,valid_until,status,entered_at,edited_at,checked_at,checked_revision FROM workday_notices CROSS JOIN generate_series(1,199) WHERE id=%s', (original['result']['id'],))
    assert send(client, plan, command(content=content())).status_code == 429
    rows = []; cursor = None
    for page in range(4):
        reply = client.get('/notices' + ('?cursor=' + cursor if cursor else '')).json(); rows += reply['notices']; cursor = reply['next_cursor']
        assert len(reply['notices']) == 50 and bool(cursor) == (page < 3)
    assert len({row['id'] for row in rows}) == 200
    with database() as conn:
        conn.execute('INSERT INTO account_notice_operations SELECT gen_random_uuid(),owner,notice_id,payload_hash,result,expires_at FROM account_notice_operations CROSS JOIN generate_series(1,1999) WHERE id=%s', (body['operation_id'],))
    rejected = send(client, plan, command(1), original['result']['id'], 'check')
    assert rejected.status_code == 429
    assert send(client, plan, body).json() == original
    with database() as conn: conn.execute('UPDATE workday_notices SET expires_at=clock_timestamp() WHERE id=%s', (original['result']['id'],))
    assert send(client, plan, body).status_code == client.get('/workday-notice-operations/' + body['operation_id']).status_code == 410
    cleanup()
    assert client.get('/workday-notice-operations/'+body['operation_id']).status_code == 404


@pytest.mark.parametrize('action', ['save', 'check', 'end'])
def test_competing_edits_checks_end_have_one_revision_winner(client, users, action):
    _, plan = opened(client, users)
    identifier = send(client, plan, command(content=content())).json()['result']['id']
    commands = [(None, command(1, content=content(title='Competing edit'))), (None if action == 'save' else action, command(1, **({'content': content(title='Second edit')} if action == 'save' else {})))]
    proof, cookies = headers(client), dict(client.cookies)
    def post(item):
        suffix, body = item
        return httpx.post(URL + '/notices/' + identifier + ('/' + suffix if suffix else ''), headers=proof, cookies=cookies, json=body, timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: replies = list(pool.map(post, commands))
    assert sorted(reply.status_code for reply in replies) == [200, 409]
    assert read(client, plan)['notices'] == [next(reply.json()['result'] for reply in replies if reply.status_code == 200)]
    with database() as conn:
        assert conn.execute('SELECT count(*) AS n FROM account_notice_operations WHERE owner=%s', (users[1][0],)).fetchone()['n'] == 2


@pytest.mark.parametrize('boundary', ['session', 'notice'])
def test_final_atomic_authority_rolls_back_notice_and_receipt(client, users, monkeypatch, boundary):
    _, plan = opened(client, users); initial = read(client, plan)
    from app.workday_notice_domain import SaveAccountNotice
    body = SaveAccountNotice(**command(content=content()))
    request = SimpleNamespace(cookies={auth.SESSION: client.cookies.get(auth.SESSION)})
    class Connection:
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            if query.startswith('INSERT INTO account_notice_operations'):
                if boundary == 'notice': self.conn.execute('UPDATE workday_notices SET expires_at=clock_timestamp() WHERE owner=%s', (users[1][0],))
                else: self.conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner=%s", (users[1][0],))
            return self.conn.execute(query, params)
    @contextmanager
    def wrapped():
        with database() as conn: yield Connection(conn)
    monkeypatch.setattr(workday_notice_storage, 'database', wrapped)
    with pytest.raises(HTTPException) as error: workday_notice_storage.save(request, None, body)
    assert error.value.status_code == (410 if boundary == 'notice' else 401)
    assert read(client, plan) == initial


@pytest.mark.parametrize('action', ['create', 'save', 'check', 'end'])
@pytest.mark.parametrize('other', ['close', 'delete'])
def test_notice_commands_serialize_with_parent_closure_and_deletion(client, users, action, other):
    _,plan=opened(client,users)
    n=send(client,plan,command(content=content())).json()['result']; start(client,plan)
    body=command(0 if action=='create' else 1,**({'content':content(title='Racing proposal')} if action in {'create','save'} else {}))
    notice_path='/notices'+('' if action=='create' else '/'+n['id'])+('/'+action if action in {'check','end'} else '')
    competing=closing() if other=='close' else {'operation_id':str(uuid4()),'source_revision':1}
    proof,cookies=headers(client),dict(client.cookies)
    def post(item):
        route,payload=item
        return httpx.post(URL+route,headers=proof,cookies=cookies,json=payload,timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        notice,parent=list(pool.map(post,[(notice_path,body),('/workdays/'+plan['id']+'/'+other,competing)]))
    assert notice.status_code==parent.status_code==200
    rows=read(client,plan)['notices']; assert len(rows)==(2 if action=='create' else 1)
    assert client.get('/workday-notice-operations/'+body['operation_id']).json()==notice.json()
    with database() as conn:
        receipts=conn.execute('SELECT * FROM account_notice_operations WHERE owner=%s',(users[1][0],)).fetchall()
        assert len(receipts)==2
        assert all(row['expires_at']==datetime.fromisoformat(next(n for n in rows if n['id']==row['result']['id'])['expires_at']) for row in receipts)


def test_additive_011_populated_upgrade_preserves_existing_rows_and_receipts(client, users):
    from pathlib import Path
    _, plan = opened(client, users); start(client, plan)
    tables = ['accounts', 'workdays', 'workday_operations', 'workday_lifecycles', 'workday_start_operations']
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        schema = 'upgrade_' + uuid4().hex; conn.execute('CREATE SCHEMA ' + schema)
        conn.execute('SET LOCAL search_path TO ' + schema + ',public')
        for table in tables:
            key = 'id' if table == 'accounts' else 'owner' if table in {'workdays', 'workday_operations', 'workday_start_operations'} else 'workday_id'
            value = users[1][0] if key in {'id', 'owner'} else plan['id']
            conn.execute('CREATE TABLE ' + table + ' AS SELECT * FROM public.' + table + ' WHERE ' + key + '=%s', (value,))
        conn.execute('ALTER TABLE accounts ADD PRIMARY KEY(id)'); conn.execute('ALTER TABLE workdays ADD PRIMARY KEY(id)')
        before = {table: conn.execute('SELECT * FROM ' + table).fetchall() for table in tables}
        assert all(before.values())
        conn.execute((Path(__file__).resolve().parent.parent / 'migrations/private/011_manual_notices.sql').read_text(encoding='utf-8'))
        for table in tables: assert conn.execute('SELECT * FROM ' + table).fetchall() == before[table]
        for table in ['workday_notices', 'workday_notice_operations']: assert conn.execute('SELECT count(*) AS n FROM ' + table).fetchone()['n'] == 0
        conn.execute('DROP SCHEMA ' + schema + ' CASCADE')


def test_sms_explicit_scope_multiline_and_new_limits(client, users):
    _, plan = opened(client, users)
    explanation = 'Monday 06-08\nTuesday 16-18\nUse the temporary stop.\tKeep instructions.'
    values = content(source_url=None, summary='Short explanation', description=explanation, source_note='SMS from traffic control', line_scope='all', line_tags=[])
    body = command(content=values)
    saved = send(client, plan, body); assert saved.status_code == 200
    receipt = saved.json(); n = receipt['result']
    assert all(n[k] == v for k, v in values.items())
    assert send(client, plan, body).json() == client.get('/workday-notice-operations/' + body['operation_id']).json() == receipt
    assert read(client, plan)['notices'] == [n]
    checked = send(client, plan, command(1), n['id'], 'check').json()['result']
    ended = send(client, plan, command(2), n['id'], 'end').json()['result']
    for result in [checked, ended]:
        assert all(result[key] == value for key, value in values.items())
        assert result['entered_at'] == n['entered_at']
    assert checked['revision'] == checked['checked_revision'] == 2 and checked['edited_at'] == n['edited_at']
    assert ended['revision'] == 3 and ended['status'] == 'ended_manually'
    assert ended['checked_at'] == checked['checked_at'] and ended['checked_revision'] == checked['checked_revision']
    selected = content(line_tags=['Route heading ' + 'a' * 286], source_url='https://svipper.no/meny/reise/trafikkmeldinger/trafikkmeldinger/', summary=' ' * 5, description=' ', source_note=' ')
    changed = send(client, plan, command(content=selected)); assert changed.status_code == 200
    current = changed.json()['result']; assert current['line_scope'] == 'selected' and len(current['line_tags'][0]) == 300
    assert current['summary'] is current['description'] is current['source_note'] is None
    for invalid in [dict(line_scope='all'), dict(line_scope='selected', line_tags=[]), dict(line_scope='unknown'), dict(summary='a'*1001), dict(description='a'*5001), dict(source_note='a'*501), dict(summary='line\nbreak'), dict(description='bad\x00text')]:
        assert send(client, plan, command(content=content(**invalid))).status_code == 422


def test_legacy_command_fingerprint_and_receipt_remain_immutable(client, users):
    from psycopg.types.json import Jsonb
    from app import draft_storage
    _,plan=opened(client,users)
    body=command(content=content()); receipt=send(client,plan,body).json()
    old={k:v for k,v in receipt['result'].items() if k not in {'summary','description','source_note','line_scope'}}
    old['workday_id']=plan['id']
    legacy_body={**body,'expected_lifecycle_revision':0}
    legacy_hash=draft_storage.fingerprint(UUID(plan['id']),{'action':'save','notice_id':None,**SaveNotice(**legacy_body).model_dump(mode='json',exclude={'content':{'summary','description','source_note','line_scope'}})})
    with database() as conn:
        conn.execute('DELETE FROM account_notice_operations WHERE id=%s',(body['operation_id'],))
        conn.execute('INSERT INTO workday_notice_operations VALUES(%s,%s,%s,%s,%s,%s)',(body['operation_id'],users[1][0],plan['id'],legacy_hash,Jsonb(old),receipt['result']['expires_at']))
    path='/workdays/'+plan['id']+'/notices'
    accepted=client.post(path,headers=headers(client),json=legacy_body); assert accepted.status_code==200
    expected={**receipt,'result':{**receipt['result'],'workday_id':plan['id']}}
    assert accepted.json()==expected
    assert client.get('/workday-notice-operations/'+body['operation_id']).json()==expected
    for route,payload in [(path,{**legacy_body,'content':content(title='Different')}),(path+'/'+old['id'],legacy_body),('/workdays/'+str(uuid4())+'/notices',legacy_body)]:
        assert client.post(route,headers=headers(client),json=payload).status_code==409
    assert client.post(path+'/'+old['id']+'/check',headers=headers(client),json={k:v for k,v in legacy_body.items() if k!='content'}).status_code==409
    for changed in [{'summary':'New summary'},{'description':'New full source text'},{'source_note':'SMS'},{'line_scope':'all','line_tags':[]}]:
        assert client.post(path,headers=headers(client),json={**legacy_body,'content':content(**changed)}).status_code==409
    with database() as conn:
        raw=conn.execute('SELECT * FROM workday_notice_operations WHERE id=%s',(body['operation_id'],)).fetchone()
        assert raw['result']==old and raw['payload_hash']==legacy_hash
        conn.execute('DELETE FROM workdays WHERE id=%s',(plan['id'],))
    assert client.post(path,headers=headers(client),json=legacy_body).json()==expected
    assert client.get('/workday-notice-operations/'+body['operation_id']).json()==expected


def test_populated_011_to_012_preserves_old_notices_receipts_and_metadata(client, users):
    from pathlib import Path
    _, plan = opened(client, users)
    body = command(content=content()); original = send(client, plan, body).json()
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        schema = 'upgrade_sources_' + uuid4().hex
        conn.execute('CREATE SCHEMA ' + schema)
        conn.execute('SET LOCAL search_path TO ' + schema + ',public')
        for table in ['accounts', 'workdays']:
            conn.execute('CREATE TABLE ' + table + ' AS SELECT * FROM public.' + table + ' WHERE id=%s', (users[1][0] if table == 'accounts' else plan['id'],))
            conn.execute('ALTER TABLE ' + table + ' ADD PRIMARY KEY(id)')
        migrations = Path(__file__).resolve().parent.parent / 'migrations/private'
        conn.execute((migrations / '011_manual_notices.sql').read_text(encoding='utf-8'))
        columns = 'id,workday_id,revision,title,line_tags,source_url,source_updated_at,valid_from,valid_until,status,entered_at,edited_at,checked_at,checked_revision'
        conn.execute('INSERT INTO workday_notices SELECT id,%s,revision,title,line_tags,source_url,source_updated_at,valid_from,valid_until,status,entered_at,edited_at,checked_at,checked_revision FROM public.workday_notices WHERE id=%s', (plan['id'],original['result']['id']))
        conn.execute('INSERT INTO workday_notice_operations SELECT id,owner,%s,payload_hash,result,expires_at FROM public.account_notice_operations WHERE id=%s', (plan['id'],body['operation_id']))
        before = conn.execute('SELECT ' + columns + ' FROM workday_notices').fetchone()
        receipts = conn.execute('SELECT * FROM workday_notice_operations').fetchall()
        conn.execute((migrations / '012_real_notice_sources.sql').read_text(encoding='utf-8'))
        assert conn.execute('SELECT ' + columns + ' FROM workday_notices').fetchone() == before
        assert conn.execute('SELECT * FROM workday_notice_operations').fetchall() == receipts
        upgraded = conn.execute('SELECT * FROM workday_notices').fetchone()
        assert upgraded['line_scope'] == 'selected' and upgraded['summary'] is upgraded['description'] is upgraded['source_note'] is None
        conn.execute("UPDATE workday_notices SET line_scope='all',line_tags='[]',source_url=NULL,description=E'First window\\nSecond window'")
        assert conn.execute('SELECT description FROM workday_notices').fetchone()['description'] == 'First window\nSecond window'
        conn.execute('DROP SCHEMA ' + schema + ' CASCADE')


@pytest.mark.parametrize('changed', [
    {'summary': 'Different summary'}, {'description': 'Different\noperational text'},
    {'source_note': 'SMS source'}, {'line_scope': 'all', 'line_tags': []}, {'source_url': None},
])
def test_additive_content_changes_cannot_reuse_legacy_default_command_id(client, users, changed):
    _, plan = opened(client, users)
    body = command(content=content()); receipt = send(client, plan, body).json()
    assert send(client, plan, {**body, 'content': content(**changed)}).status_code == 409
    assert read(client, plan)['notices'] == [receipt['result']]
    assert client.get('/workday-notice-operations/' + body['operation_id']).json() == receipt
    assert send(client, plan, body).json() == receipt
