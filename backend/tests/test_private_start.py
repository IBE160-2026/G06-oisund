"""First accepted explicit start is one-way and independent of selection."""
import concurrent.futures
from datetime import datetime, timezone
from uuid import uuid4
import httpx
from app.private_storage import database, migrate
from test_private_access import client, headers, synthetic_only, users, URL
from test_private_workdays import teardown
from test_private_selection import opened, body, routes


def test_legacy_unstarted_selection_then_start_replay_and_second_start(client, users):
    draft, plan = opened(client, users)
    path, read = routes(plan, 'start'); selection = '/workdays/' + plan['id'] + '/selection'
    initial = {'workday_id': plan['id'], 'state': 'confirmed', 'started_at': None, 'ended_at': None, 'revision': 0, 'expires_at': plan['expires_at']}
    # Existing confirmed plans have no lifecycle row: no eager backfill/rewrite.
    with database() as conn: assert not conn.execute('SELECT 1 FROM workday_lifecycles WHERE workday_id=%s', (plan['id'],)).fetchone()
    migrate(); migrate(); assert client.get(read).json() == initial
    selected = client.post(selection, headers=headers(client), json=body(plan, 'selection')).json()['result']
    assert client.get(read).json() == initial
    start = body(plan, 'start'); before = datetime.now(timezone.utc)
    receipt = client.post(path, headers=headers(client), json=start).json(); after = datetime.now(timezone.utc)
    actual = receipt['result']; assert actual['state'] == 'active' and actual['revision'] == 1
    assert before <= datetime.fromisoformat(actual['started_at']) <= after
    assert actual['started_at'] != plan['draft']['activities'][0]['start']
    assert client.get(read).json() == actual
    assert client.post(path, headers=headers(client), json=start).json() == receipt
    for revision in [0, 1]:
        again = body(plan, 'start', revision)
        second = client.post(path, headers=headers(client), json=again)
        assert second.status_code == 200 and second.json()['result'] == actual
    assert client.post(path, headers=headers(client), json=body(plan, 'start', 2)).status_code == 409
    assert client.get(selection).json() == selected
    assert client.get('/workdays/' + plan['id']).json() == plan
    assert client.get('/drafts/' + draft['id']).json() == draft


def test_simultaneous_distinct_and_same_operation_start_converge_without_selection(client, users):
    _, plan = opened(client, users); path, read = routes(plan, 'start')
    proof, cookies = headers(client), dict(client.cookies)
    first = body(plan, 'start'); payloads = [first, first, body(plan, 'start'), body(plan, 'start')]
    def send(p): return httpx.post(URL + path, headers=proof, cookies=cookies, json=p, timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: replies = list(pool.map(send, payloads))
    assert all(r.status_code == 200 for r in replies)
    actual = replies[0].json()['result']
    assert all(r.json()['result'] == actual for r in replies)
    assert replies[0].json() == replies[1].json()
    assert client.get(read).json() == actual and actual['revision'] == 1
    assert client.get('/workdays/' + plan['id'] + '/selection').json()['activity_id'] is None
    with database() as conn:
        rows = conn.execute('SELECT * FROM workday_lifecycles WHERE workday_id=%s', (plan['id'],)).fetchall()
        assert len(rows) == 1 and rows[0]['revision'] == 1
    for payload, response in zip(payloads, replies):
        assert client.get('/workday-start-operations/' + payload['operation_id']).json() == response.json()
