"""Disposable reader contracts; projection never changes saved facts."""
from datetime import date, datetime, timezone
from uuid import uuid4
import pytest
from fastapi import HTTPException
from app.notice_reader_domain import project, NoticeReader
from test_private_notices import client, users, opened, command, content, send, read
from test_private_access import login, URL, synthetic_only
from app.private_storage import database
import httpx
from contextlib import contextmanager
from types import SimpleNamespace
from uuid import UUID
from app import auth, workday_notice_storage
from test_private_outcomes import start, closing
from test_private_access import headers


def fixture(intervals=None, lines=None):
    intervals = intervals or [('2031-01-02T23:00+01:00', '2031-01-02T23:10+01:00'), ('2031-01-03T00:00+01:00', '2031-01-03T00:10+01:00')]
    return {'id': uuid4(), 'expires_at': datetime(2031, 1, 10, tzinfo=timezone.utc), 'content': {'activities': [dict(start=a, end=b, line=(lines or ['20', '24'])[i]) for i, (a, b) in enumerate(intervals)]}}


def row(plan, **values):
    now = datetime(2031, 1, 1, tzinfo=timezone.utc)
    return dict(id=uuid4(), workday_id=plan['id'], revision=1, title='Incident', line_tags=['20', '24'], line_scope='selected', source_url=None, source_updated_at=None, valid_from=None, valid_until='2031-01-04T23:59:59+01:00', status='registered', entered_at=now, edited_at=now, checked_at=None, checked_revision=None, expires_at=plan['expires_at'], summary=None, description=None, source_note=None, **values)


def test_shared_separate_exact_tags_unknown_lines_and_all_scope():
    p = fixture(lines=[' 020 ', 'aB'])
    shared = row(p); shared['line_tags'] = ['020', 'aB']
    separate = row(p); separate['line_tags'] = ['020']
    heading = row(p); heading['line_tags'] = ['Linje 020 heading', '20', 'AB']
    all_lines = row(p); all_lines.update(line_scope='all', line_tags=[])
    result = NoticeReader(**project(p, [shared, separate, heading, all_lines]))
    assert [c.notice.id for c in result.candidates] == [shared['id'], separate['id'], all_lines['id']]
    assert result.candidates[0].matching_lines == ['020', 'aB']
    assert result.unmatched_notice_count == 1
    assert len(project(p, [shared, separate, heading, all_lines], 'aB')['candidates']) == 2
    p['content']['activities'][0]['line'] = None; p['content']['activities'][1]['line'] = None
    result = project(p, [shared, all_lines])
    assert result['unknown_line_count'] == 2 and result['candidates'][0]['notice']['id'] == all_lines['id']


@pytest.mark.parametrize('day,lower,upper', [('2031-03-30', '2031-03-29T23:00Z', '2031-03-30T22:00Z'), ('2031-10-26', '2031-10-25T22:00Z', '2031-10-26T23:00Z')])
def test_dst_oslo_calendar_exclusive_midnight(day, lower, upper):
    p = fixture([(lower, upper)], ['20'])
    n = row(p); n.update(valid_from=upper, valid_until=upper)
    assert project(p, [n], calendar_date=date.fromisoformat(day))['candidates'] == []
    n.update(valid_from=lower, valid_until=lower)
    assert len(project(p, [n], calendar_date=date.fromisoformat(day))['candidates']) == 1


def test_union_gaps_endpoints_partial_unknown_and_manual_end():
    p = fixture()
    rows = []
    for start, end in [('2031-01-02T23:10+01:00', '2031-01-02T23:10+01:00'), ('2031-01-02T23:11+01:00', '2031-01-02T23:59+01:00'), ('2031-01-03T00:00+01:00', '2031-01-03T00:00+01:00'), ('2032-01-01T00:00+01:00', None), (None, '2030-01-01T00:00+01:00'), (None, None)]:
        n = row(p); n.update(valid_from=start, valid_until=end, status='registered'); rows.append(n)
    result = project(p, rows)
    assert [c['notice']['id'] for c in result['candidates']] == [rows[i]['id'] for i in [0, 2]]
    assert [c['validity'] for c in result['candidates']] == ['known', 'known']
    assert len(project(p, rows, calendar_date=date(2031, 1, 2))['candidates']) == 1
    for kwargs in [dict(line='20 heading'), dict(calendar_date=date(2031, 1, 4))]:
        with pytest.raises(HTTPException) as error: project(p, rows, **kwargs)
        assert error.value.status_code == 422


def test_line_matching_is_independent_of_which_activity_supplies_time_overlap():
    # Broad planned-day candidates are not exact trip relevance: line 20 is
    # confirmed on the day, while only the line-24 interval overlaps validity.
    p = fixture()
    n = row(p); n.update(line_tags=['20', 'Copied heading'], valid_from='2031-01-03T00:05+01:00', valid_until='2031-01-03T00:06+01:00')
    result = project(p, [n], line='20', calendar_date=date(2031, 1, 3))
    assert len(result['candidates']) == 1
    candidate = result['candidates'][0]
    assert candidate['matching_lines'] == ['20'] and candidate['unmatched_tags'] == ['Copied heading']
    assert candidate['line_uncertain'] is True and result['unmatched_notice_count'] == 1


def test_reader_capacity_200_notices_lines_and_50_tags_without_truncation(client, users):
    from test_private_workdays import prepare, confirm, facts
    assert login(client, users).status_code == 200
    value = facts()
    lines = [f'{i:03}' for i in range(200)]
    value['activities'] = [{**value['activities'][0], 'id': str(uuid4()), 'line': line} for line in lines]
    draft, _, decisions = prepare(client, value)
    response = confirm(client, draft, decisions); assert response.status_code == 200
    plan = response.json()
    tags = lines[:49] + [lines[-1]]
    saved = send(client, plan, command(content=content(line_tags=tags))).json()['result']
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        conn.execute('INSERT INTO workday_notices(id,owner,workday_id,expires_at,revision,title,line_tags,source_url,source_updated_at,valid_from,valid_until,status,entered_at,edited_at,checked_at,checked_revision) SELECT gen_random_uuid(),owner,workday_id,expires_at,revision,title,line_tags,source_url,source_updated_at,valid_from,valid_until,status,entered_at,edited_at,checked_at,checked_revision FROM workday_notices CROSS JOIN generate_series(1,199) WHERE id=%s', (saved['id'],))
    def persisted():
        with database() as conn:
            return {table: conn.execute('SELECT * FROM ' + table + ' WHERE ' + ('id' if table == 'workdays' else 'workday_id') + '=%s ORDER BY ' + ('id' if table in {'workdays', 'workday_notices', 'workday_notice_operations'} else 'workday_id'), (plan['id'],)).fetchall() for table in ['workdays', 'workday_notices', 'workday_notice_operations', 'workday_selections', 'workday_lifecycles']}
    before = persisted()
    path = '/workdays/' + plan['id'] + '/notice-reader'
    for query in [{}, {'line': lines[-1]}, {'line': lines[-1], 'calendar_date': '2031-01-02'}]:
        reply = client.get(path, params=query); assert reply.status_code == 200
        result = reply.json()
        assert result['available_lines'] == lines and result['stored_count'] == 200
        assert len(result['candidates']) == len({c['notice']['id'] for c in result['candidates']}) == 200
        assert all(c['matching_lines'] == tags and c['notice']['line_tags'] == tags for c in result['candidates'])
    assert client.get(path, params={'line': lines[50]}).json()['candidates'] == []
    assert persisted() == before


def test_api_no_store_persistence_filters_and_privacy(client, users):
    _, plan = opened(client, users)
    path = '/workdays/' + plan['id'] + '/notice-reader'
    initial = client.get(path); assert initial.status_code == 200 and initial.headers['cache-control'] == 'no-store'
    assert initial.json()['stored_count'] == 0
    saved = send(client, plan, command(content=content(line_tags=['20', '24', 'Copied heading']))).json()['result']
    before = read(client, plan)
    result = client.get(path).json()
    assert result['candidates'][0]['notice'] == saved
    assert result['candidates'][0]['matching_lines'] == ['20', '24']
    assert result['candidates'][0]['unmatched_tags'] == ['Copied heading']
    assert result['candidates'][0]['line_uncertain'] is True and result['unmatched_notice_count'] == 1
    assert client.get(path, params={'line': '20'}).status_code == 200
    assert client.get(path, params={'line': '020'}).status_code == 422
    assert client.get(path, params={'calendar_date': '2031-01-04'}).status_code == 422
    assert client.get(path, params={'line': 'x' * 101}).status_code == 422
    assert read(client, plan) == before
    with httpx.Client(base_url=URL) as other:
        assert other.get(path).status_code == 401
        assert login(other, users, 1).status_code == 200
        assert other.get(path).status_code == 404
    with database() as conn: conn.execute('UPDATE workdays SET expires_at=clock_timestamp() WHERE id=%s', (plan['id'],))
    assert client.get(path).status_code == 410


def test_terminal_reader_never_changes_notice_or_lifecycle(client, users):
    _, plan = opened(client, users)
    saved = send(client, plan, command(content=content(line_tags=['20']))).json()['result']
    start(client, plan)
    assert client.post('/workdays/' + plan['id'] + '/close', headers=headers(client), json=closing()).status_code == 200
    before = read(client, plan)
    result = client.get('/workdays/' + plan['id'] + '/notice-reader')
    assert result.status_code == 200 and result.json()['candidates'][0]['notice']['id'] == saved['id']
    assert read(client, plan) == before


@pytest.mark.parametrize('boundary', ['plan', 'session'])
def test_reader_rechecks_authority_after_projection(client, users, monkeypatch, boundary):
    _, plan = opened(client, users)
    request = SimpleNamespace(cookies={auth.SESSION: client.cookies.get(auth.SESSION)})
    class Connection:
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            result = self.conn.execute(query, params)
            if query.startswith('SELECT * FROM workday_notices'):
                if boundary == 'plan': self.conn.execute('UPDATE workdays SET expires_at=clock_timestamp() WHERE id=%s', (plan['id'],))
                else: self.conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner=%s", (users[1][0],))
            return result
    @contextmanager
    def wrapped():
        with database() as conn: yield Connection(conn)
    monkeypatch.setattr(workday_notice_storage, 'database', wrapped)
    with pytest.raises(HTTPException) as error: workday_notice_storage.reader(request, UUID(plan['id']))
    assert error.value.status_code == (410 if boundary == 'plan' else 401)
