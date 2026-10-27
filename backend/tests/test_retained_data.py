"""Deterministic retained-authority regressions, synthetic private runtime only."""
from contextlib import contextmanager
from types import SimpleNamespace
from uuid import uuid4
from zoneinfo import ZoneInfo

import httpx
import pytest
from fastapi import HTTPException

from app import auth, draft_storage, workday_storage, workday_notice_storage
from app.private_storage import database, cleanup, migrate
from app.workday_notice_domain import SaveAccountNotice
from test_private_access import client, users, synthetic_only, headers, login, URL, ORIGIN
from test_account_notices import content, command, send
from test_private_selection import opened


def issue(client):
    response = client.post('/notice-operations', headers=headers(client), json={})
    assert response.status_code == 200, response.text
    assert response.headers['cache-control'] == 'no-store'
    return response.json()


def request(client):
    return SimpleNamespace(cookies={auth.SESSION: client.cookies.get(auth.SESSION)})


def raw_create(client, body):
    return client.post('/notices', headers=headers(client), json=body)


def test_creation_admission_owner_cap_expiry_and_payload_free_cleanup(client, users):
    assert login(client, users).is_success
    unknown = command(content=content())
    assert raw_create(client, unknown).status_code == 404
    issued = issue(client)
    with httpx.Client(base_url=URL) as other:
        assert login(other, users, 1).is_success
        assert raw_create(other, {**unknown, 'operation_id': issued['operation_id']}).status_code == 404
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        row = conn.execute('SELECT * FROM notice_creation_admissions WHERE id=%s', (issued['operation_id'],)).fetchone()
        assert set(row) == {'id', 'owner', 'expires_at'}
        conn.execute("INSERT INTO notice_creation_admissions SELECT gen_random_uuid(),owner,expires_at FROM notice_creation_admissions CROSS JOIN generate_series(1,199) WHERE id=%s", (issued['operation_id'],))
    assert client.post('/notice-operations', headers=headers(client), json={}).status_code == 429
    with database() as conn:
        conn.execute("UPDATE notice_creation_admissions SET expires_at=clock_timestamp()-interval '1 second' WHERE owner=%s", (users[1][0],))
    assert raw_create(client, {**unknown, 'operation_id': issued['operation_id']}).status_code == 410
    cleanup(); migrate(); migrate()
    assert raw_create(client, {**unknown, 'operation_id': issued['operation_id']}).status_code == 404
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM notice_creation_admissions WHERE owner=%s', (users[1][0],)).fetchone()
        assert not conn.execute('SELECT 1 FROM workday_notices WHERE owner=%s', (users[1][0],)).fetchone()


def test_early_ended_purged_create_cannot_resurrect_future_original(client, users):
    assert login(client, users).is_success
    original = command(content=content(valid_until='2035-01-01'))
    accepted = send(client, original).json()
    identifier = accepted['result']['id']
    assert send(client, command(1), identifier, 'end').is_success
    assert raw_create(client, original).json() == accepted
    with database() as conn:
        conn.execute("UPDATE workday_notices SET expires_at=clock_timestamp()-interval '1 second' WHERE id=%s", (identifier,))
    cleanup()
    assert raw_create(client, original).status_code == 404
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM workday_notices WHERE id=%s', (identifier,)).fetchone()
        assert not conn.execute('SELECT 1 FROM account_notice_operations WHERE notice_id=%s', (identifier,)).fetchone()
    fresh = {**original, 'operation_id': issue(client)['operation_id']}
    assert raw_create(client, fresh).is_success


@pytest.mark.parametrize('boundary', ['admission', 'original-ending', 'create-ending'])
def test_notice_late_acceptance_rolls_back_payload_revision_deadline_receipts(client, users, monkeypatch, boundary):
    assert login(client, users).is_success
    if boundary in {'admission', 'create-ending'}:
        issued = issue(client)
        body = {**command(content=content()), 'operation_id': issued['operation_id']}
        identifier = None
        with database() as conn:
            if boundary == 'admission':
                conn.execute("UPDATE notice_creation_admissions SET expires_at=clock_timestamp()+interval '0.15 seconds' WHERE id=%s", (body['operation_id'],))
            else:
                ending = conn.execute("SELECT date_trunc('second',clock_timestamp())+interval '2 seconds' AS ending").fetchone()['ending']
                body['content']['valid_until'] = ending.astimezone(ZoneInfo('Europe/Oslo')).isoformat()
            before_admission = conn.execute('SELECT * FROM notice_creation_admissions WHERE id=%s', (body['operation_id'],)).fetchone()
        trigger = 'INSERT INTO account_notice_operations'
    else:
        identifier = send(client, command(content=content())).json()['result']['id']
        body = command(1, content=content(title='Must roll back', valid_until='2035-01-01'))
        with database() as conn:
            conn.execute("UPDATE workday_notices SET valid_until=clock_timestamp()+interval '0.15 seconds' WHERE id=%s", (identifier,))
            before = conn.execute('SELECT * FROM workday_notices WHERE id=%s', (identifier,)).fetchone()
            before_receipts = conn.execute('SELECT * FROM account_notice_operations WHERE notice_id=%s ORDER BY id', (identifier,)).fetchall()
            before_legacy = conn.execute("SELECT * FROM workday_notice_operations WHERE result->>'id'=%s ORDER BY id", (identifier,)).fetchall()
        trigger = 'UPDATE workday_notices SET title='
    class Connection:
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            result = self.conn.execute(query, params)
            if query.startswith(trigger):
                if boundary == 'create-ending':
                    assert self.conn.execute('SELECT %s>clock_timestamp() AS live', (ending,)).fetchone()['live']
                    self.conn.execute('SELECT pg_sleep(GREATEST(0,extract(epoch FROM (%s::timestamptz-clock_timestamp())))+0.02)', (ending,))
                else:
                    self.conn.execute('SELECT pg_sleep(0.25)')
            return result
    @contextmanager
    def wrapped():
        with database() as conn: yield Connection(conn)
    monkeypatch.setattr(workday_notice_storage, 'database', wrapped)
    with pytest.raises(HTTPException) as error:
        workday_notice_storage.save(request(client), None, SaveAccountNotice(**body), identifier)
    assert error.value.status_code == {'admission': 410, 'original-ending': 409, 'create-ending': 422}[boundary]
    if boundary == 'create-ending':
        assert error.value.detail == 'Oppgi en fremtidig sluttdato for avviket.'
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM account_notice_operations WHERE id=%s', (body['operation_id'],)).fetchone()
        if identifier:
            assert conn.execute('SELECT * FROM workday_notices WHERE id=%s', (identifier,)).fetchone() == before
            assert conn.execute('SELECT * FROM account_notice_operations WHERE notice_id=%s ORDER BY id', (identifier,)).fetchall() == before_receipts
            assert conn.execute("SELECT * FROM workday_notice_operations WHERE result->>'id'=%s ORDER BY id", (identifier,)).fetchall() == before_legacy
        else:
            assert not conn.execute('SELECT 1 FROM workday_notices WHERE owner=%s', (users[1][0],)).fetchone()
            assert conn.execute('SELECT * FROM notice_creation_admissions WHERE id=%s', (body['operation_id'],)).fetchone() == before_admission


@pytest.mark.parametrize('kind', ['draft-list', 'draft-detail', 'day-list', 'notice-detail', 'reader'])
def test_delayed_reads_exclude_retention_crossed_before_final_authority(client, users, monkeypatch, kind):
    draft, plan = opened(client, users)
    notice = send(client, command(content=content())).json()['result']
    module = draft_storage if kind.startswith('draft') else workday_storage if kind.startswith('day') else workday_notice_storage
    table, identifier = ('drafts', draft['id']) if kind.startswith('draft') else ('workdays', plan['id']) if kind.startswith('day') else ('workday_notices', notice['id'])
    with database() as conn:
        if table == 'drafts':
            conn.execute("UPDATE drafts SET created_at=statement_timestamp()-interval '7 days'+interval '0.15 seconds',expires_at=statement_timestamp()+interval '0.15 seconds' WHERE id=%s", (identifier,))
        else:
            conn.execute('UPDATE '+table+" SET expires_at=clock_timestamp()+interval '0.15 seconds' WHERE id=%s", (identifier,))
    class Connection:
        delayed = False
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            result = self.conn.execute(query, params)
            # For details, the first live test succeeds before the boundary;
            # final authorization must subsequently reject the captured row.
            selected = 'FROM '+table+' WHERE owner=' in query if kind.endswith('list') or kind=='reader' else (' AS live' in query and query.startswith('SELECT %s'))
            if selected and not self.delayed:
                self.delayed = True
                self.conn.execute('SELECT pg_sleep(0.25)')
            return result
    @contextmanager
    def wrapped():
        with database() as conn: yield Connection(conn)
    monkeypatch.setattr(module, 'database', wrapped)
    req = request(client)
    if kind.endswith('detail'):
        with pytest.raises(HTTPException) as error:
            module.read(req, identifier) if kind=='draft-detail' else module.read(req, notice_id=identifier)
        assert error.value.status_code == 410
    elif kind=='reader':
        result = module.reader(req, plan['id'])
        assert result['stored_count'] == 0 and result['candidates'] == []
    else:
        result = module.listing(req)
        assert result['drafts' if kind=='draft-list' else 'workdays'] == []


@pytest.mark.parametrize('kind', ['draft', 'day', 'notice'])
@pytest.mark.parametrize('expired_count', [1, 51, 102])
def test_late_expiry_keeps_pagination_scan_continuation(client, users, monkeypatch, kind, expired_count):
    draft, plan = opened(client, users)
    notice = send(client, command(content=content())).json()['result']
    table, identifier, module, key = {
        'draft': ('drafts', draft['id'], draft_storage, 'drafts'),
        'day': ('workdays', plan['id'], workday_storage, 'workdays'),
        'notice': ('workday_notices', notice['id'], workday_notice_storage, 'notices'),
    }[kind]
    with database() as conn:
        # Clone payload facts only inside this dedicated synthetic account.
        columns = [row['column_name'] for row in conn.execute("SELECT column_name FROM information_schema.columns WHERE table_schema=current_schema() AND table_name=%s ORDER BY ordinal_position", (table,)).fetchall()]
        fields = ','.join(columns)
        values = ','.join('gen_random_uuid()' if c=='id' or table=='workdays' and c=='source_draft_id' else c for c in columns)
        conn.execute('INSERT INTO '+table+'('+fields+') SELECT '+values+' FROM '+table+' CROSS JOIN generate_series(1,%s) WHERE id=%s', (expired_count+59, identifier))
        ids = [row['id'] for row in conn.execute('SELECT id FROM '+table+' WHERE owner=%s ORDER BY id', (users[1][0],)).fetchall()]
    doomed = set(ids[:expired_count])
    empty_pages = 0
    class Connection:
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            result = self.conn.execute(query, params)
            if 'FROM '+table+' WHERE owner=' in query:
                rows = result.fetchall()
                selected = [row['id'] for row in rows if row['id'] in doomed]
                if selected:
                    # Replace only the synthetic selected rows' deadline in the
                    # captured result and DB after selection, then cross it.
                    deadline = self.conn.execute("SELECT statement_timestamp()+interval '0.03 seconds' AS ending").fetchone()['ending']
                    if kind == 'draft':
                        self.conn.execute("UPDATE drafts SET created_at=%s-interval '7 days',expires_at=%s WHERE id=ANY(%s)", (deadline, deadline, selected))
                    else:
                        self.conn.execute('UPDATE '+table+' SET expires_at=%s WHERE id=ANY(%s)', (deadline, selected))
                    for row in rows:
                        if row['id'] in doomed: row['expires_at'] = deadline
                    self.conn.execute('SELECT pg_sleep(0.05)')
                return SimpleNamespace(fetchall=lambda: rows)
            return result
    @contextmanager
    def wrapped():
        with database() as conn: yield Connection(conn)
    monkeypatch.setattr(module, 'database', wrapped)
    seen, cursor = [], None
    while True:
        page = module.read(request(client), cursor=cursor) if kind=='notice' else module.listing(request(client), cursor)
        if not page[key]: empty_pages += 1
        seen.extend(row['id'] for row in page[key])
        cursor = page['next_cursor']
        if cursor is None: break
    assert len(seen) == len(set(seen)) == 60
    assert set(seen) == set(ids[expired_count:])
    assert empty_pages == expired_count // 51


def test_notice_admission_route_denials_do_not_issue_rows(client, users):
    def count():
        with database() as conn:
            return conn.execute('SELECT count(*) AS n FROM notice_creation_admissions').fetchone()['n']
    before = count()
    # A valid anonymous double-submit proof still grants no account authority.
    assert client.post('/notice-operations', headers=headers(client), json={}).status_code == 401
    assert count() == before
    assert login(client, users).is_success
    proof = headers(client)
    cases = [
        ({'Origin': ORIGIN}, {}, 403),
        ({**proof, 'X-CSRF-Token': 'synthetic-invalid'}, {}, 403),
        ({**proof, 'Origin': 'http://localhost:15121'}, {}, 403),
        (proof, {'unexpected': 'synthetic'}, 422),
    ]
    for sent_headers, body, status in cases:
        response = client.post('/notice-operations', headers=sent_headers, json=body)
        assert response.status_code == status and response.headers['cache-control'] == 'no-store'
        assert count() == before
