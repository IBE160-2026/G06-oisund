"""Controlled Entur page sequence against the isolated V2 API and PostgreSQL."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, UTC
import os
from pathlib import Path
from threading import Event
from uuid import uuid4

import httpx
import pytest
from psycopg import sql

from app import auth, automatic_notice_ingestion as ingest
from app.automatic_notice_source import MAX_ID, SITUATION_PREFIX, SourceError
from app.private_storage import cleanup, database, migrate
from test_account_notices import send as manual_send
from test_automatic_notice_rules import BROAD, LINE24, STOP, EVENING, MORNING, page, situation
from test_private_access import URL, client, headers, login, synthetic_only, users
from test_private_workdays import confirm, facts, prepare


def reset():
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        conn.execute('DELETE FROM automatic_notice_sources')
        conn.execute('DELETE FROM automatic_notice_identities')
        conn.execute('DELETE FROM automatic_notice_feed')
        conn.execute('INSERT INTO automatic_notice_feed DEFAULT VALUES')


@pytest.fixture
def isolated_feed():
    if (os.getenv('PRIVATE_TEST_PROJECT') != 'ibe160-private-tests'
            or os.getenv('PRIVATE_TEST_ORIGIN') != 'http://127.0.0.1:19651'
            or os.getenv('V2_NOTICE_REFRESH') != 'off'):
        pytest.skip('Only the disposable local V2 test stack may run this fixture')
    reset()
    yield
    reset()


@pytest.fixture
def fixture_feed(isolated_feed, monkeypatch):
    # Transport and elapsed time are controlled. The actual database writer,
    # continuity checks, atomic publications and reader run unmodified.
    monkeypatch.setattr(ingest, 'CYCLE_INTERVAL', 0)
    monkeypatch.setattr(ingest, 'reserve', lambda *_: None)
    monkeypatch.setattr(ingest, 'finish_request', lambda *_: None)


def collect(*replies):
    queue = iter(replies)
    requestors = []

    async def fetch(requestor, _):
        requestors.append(requestor)
        reply = next(queue)
        if isinstance(reply, SourceError):
            raise reply
        items, more = reply
        return page(items, more, requestor)

    with database() as conn:
        conn.execute("UPDATE automatic_notice_feed SET next_request_at='-infinity'")
    ingest.run_cycle(Event(), fetch)
    assert len(requestors) > 0 and len(set(requestors)) == 1
    return requestors[0]


def planned(client, users, when=23, account=0):
    assert login(client, users, account).status_code == 200
    value = facts()
    value['service_date'] = f'2026-11-{when:02d}'
    start, end = EVENING if when == 23 else MORNING
    value['activities'][0].update(start=start, end=end, line='20' if when == 23 else '24')
    draft, _, body = prepare(client, value)
    accepted = confirm(client, draft, body)
    assert accepted.status_code == 200, accepted.text
    return accepted.json()


def get(client, plan):
    response = client.get(path(plan))
    assert response.status_code == 200 and response.headers['cache-control'] == 'no-store', response.text
    return response.json()


def path(plan):
    return '/workdays/' + plan['id'] + '/automatic-notices'


def entry(snapshot, name):
    return next(item for item in snapshot['entries'] if item['situation'] == 'TRO:SituationNumber:' + name)


def operation(snapshot, item, **overrides):
    return {'operation_id': str(uuid4()), 'situation': item['situation'], 'expected_revision': item['review_revision'],
            'expected_plan_revision': snapshot['plan_revision'], 'expected_lifecycle_revision': snapshot['lifecycle']['revision'],
            'expected_source_basis': item['source']['basis'], 'action': 'day-context', **overrides}


def save(client, plan, op):
    return client.post(path(plan) + '/review', headers=headers(client), json=op)


def test_complete_partial_unknown_recovery_and_lifecycle(client, users, fixture_feed):
    plan = planned(client, users)
    never = get(client, plan)
    assert never['health']['status'] == 'never-qualified' and never['health']['baseline_count'] is None
    assert never['health']['evidence_kind'] == 'synthetic'
    line = situation('line20', version='1')
    generation = collect((line, 'true'), (situation('stop', STOP) + situation('broad', BROAD), 'false'))
    complete = get(client, plan)
    h = complete['health']
    assert h['generation'] == str(generation) and h['status'] == 'complete' and h['baseline_count'] == 3
    assert h['attempt_pages'] == 2 and h['synchronized_at'] and h['baseline_at']
    assert entry(complete, 'line20')['classification'] == 'possible-relevance'
    assert entry(complete, 'stop')['classification'] == 'review'
    assert entry(complete, 'broad')['classification'] == 'broad-context'
    assert entry(complete, 'line20')['source']['content']['publisher_updated_at'] is None
    for failure in [SourceError('timeout'), SourceError('xml-invalid'), SourceError('rate-limited', 60),
                    SourceError('xml-continuity'), ('', 'true'), (line, 'false')]:
        assert collect((line, 'true'), failure) != generation
        partial = get(client, plan)
        assert partial['health']['status'] == 'partial' and partial['health']['attempt_pages'] == 1
        assert partial['health']['generation'] == str(generation) and partial['health']['synchronized_at'] == h['synchronized_at']
        assert entry(partial, 'stop')['source']['observation'] == 'unknown'
        assert entry(partial, 'line20')['source']['content']['progress'] == 'open'
    collect(SourceError('timeout'))
    unavailable = get(client, plan)
    assert unavailable['health']['status'] == 'unavailable' and unavailable['health']['baseline_count'] == 3
    assert entry(unavailable, 'line20')['source']['observation'] == 'unknown'
    collect((situation('line20', status='closed', version='2'), 'true'), SourceError('timeout'))
    partial_close = get(client, plan)
    assert partial_close['health']['status'] == 'partial'
    assert 'source-closed' in entry(partial_close, 'line20')['reasons']
    collect((line, 'true'), SourceError('timeout'))
    assert entry(get(client, plan), 'line20')['source']['observation'] == 'other-revision-seen-partial'
    new_generation = collect((line, 'false'))
    lost = get(client, plan)
    assert entry(lost, 'stop')['source']['observation'] == 'not-seen'
    assert entry(lost, 'line20')['source']['content']['version'] == '2'
    assert entry(lost, 'line20')['source']['observation'] == 'other-revision-seen'
    assert entry(lost, 'line20')['source']['complete_generation'] is None
    with database() as conn:
        snapshots = conn.execute("SELECT content->>'version' AS version,last_complete_generation FROM automatic_notice_sources "
                                 "WHERE situation='TRO:SituationNumber:line20'").fetchall()
        assert {row['version']: row['last_complete_generation'] for row in snapshots} == {'1': new_generation, '2': None}
    collect(('', 'false'))
    empty = get(client, plan)
    assert empty['health']['status'] == 'complete' and empty['health']['baseline_count'] == 0
    assert entry(empty, 'line20')['source']['observation'] == 'not-seen'
    assert entry(empty, 'stop')['source']['content']['progress'] == 'open'
    with database() as conn:
        conn.execute("UPDATE automatic_notice_feed SET synchronized_at=clock_timestamp()-interval '16 minutes'")
    assert get(client, plan)['health']['old']


def test_private_replay_revision_isolation_manual_and_expiry(client, users, fixture_feed):
    plan = planned(client, users, 24)
    sms = {'title': 'Syntetisk SMS', 'line_tags': ['24'], 'description': 'Original SMS og korreksjon',
           'source_note': 'Sjekket manuelt', 'valid_until': '2026-11-29T23:59:59+01:00'}
    record = manual_send(client, {'operation_id': str(uuid4()), 'expected_revision': 0, 'content': sms}).json()['result']
    checked = manual_send(client, {'operation_id': str(uuid4()), 'expected_revision': 1}, record['id'], 'check').json()['result']
    ended = manual_send(client, {'operation_id': str(uuid4()), 'expected_revision': 2}, record['id'], 'end').json()['result']
    assert ended['checked_at'] == checked['checked_at'] and ended['status'] == 'ended_manually'
    initial = client.get('/workdays/' + plan['id'] + '/selection').json()
    lift = situation('line24', LINE24, windows=(MORNING,))
    collect((lift, 'false'))
    snapshot = get(client, plan)
    item = entry(snapshot, 'line24')
    op = operation(snapshot, item, action='associate', activity_id=plan['draft']['activities'][0]['id'], manual_notice_id=record['id'])
    assert client.post(path(plan) + '/review', json=op).status_code == 403
    assert save(client, plan, op | {'expected_lifecycle_revision': 1}).status_code == 409
    receipt = save(client, plan, op)
    assert receipt.status_code == 200, receipt.text
    receipt = receipt.json()
    assert save(client, plan, op).json() == receipt
    assert save(client, plan, op | {'action': 'day-context', 'activity_id': None}).status_code == 409
    assert save(client, plan, op | {'operation_id': str(uuid4())}).status_code == 409
    lookup = path(plan) + '/operations/' + op['operation_id']
    assert client.get(lookup).json() == receipt
    stored = entry(get(client, plan), 'line24')
    assert stored['manual']['id'] == record['id'] and stored['manual']['status'] == 'ended_manually'
    assert stored['decision']['activity_id'] == op['activity_id']
    assert stored['decision']['source_observed_at'] == item['source']['last_seen']
    with httpx.Client(base_url=URL, timeout=20) as other:
        other_plan = planned(other, users, 24, account=1)
        foreign = other.get(path(plan))
        assert foreign.status_code == 404 and 'Syntetisk SMS' not in foreign.text
        assert other.get(lookup).status_code == save(other, plan, op).status_code == 404
        other_snapshot = get(other, other_plan)
        other_item = entry(other_snapshot, 'line24')
        assert other_item['decision'] is other_item['manual'] is None
        assert save(other, other_plan, operation(other_snapshot, other_item, manual_notice_id=record['id'])).status_code == 404
    changed = situation('line24', LINE24, windows=(MORNING,), text='<Summary>Annet innhold</Summary>')
    collect((changed, 'false'))
    latest = get(client, plan)
    revised = entry(latest, 'line24')
    assert revised['needs_reassessment'] and revised['source']['conflict_count'] == 1
    assert revised['decision']['evidence']['summary'][0]['text'] == 'Kontrollert eksempel'
    assert revised['source']['conflicts'][0]['content']['summary'][0]['text'] == 'Annet innhold'
    assert save(client, plan, operation(snapshot, stored)).status_code == 409
    dismiss = operation(latest, revised, action='dismiss', reason='Lokal vurdering')
    assert save(client, plan, dismiss).status_code == 200
    latest = get(client, plan)
    assert save(client, plan, operation(latest, entry(latest, 'line24'), action='unresolved')).status_code == 200
    assert client.get('/notices/' + record['id']).json() == ended
    assert client.get('/workdays/' + plan['id'] + '/selection').json() == initial
    parent = '/workdays/' + plan['id']
    assert client.post(parent + '/start', headers=headers(client), json={'operation_id': str(uuid4()), 'expected_revision': 0}).status_code == 200
    assert client.post(parent + '/close', headers=headers(client), json={'operation_id': str(uuid4()), 'expected_revision': 1,
                       'expected_outcome_revision': 0, 'action': 'ended'}).status_code == 200
    assert get(client, plan)['lifecycle']['state'] == 'ended'
    assert save(client, plan, op).status_code == 409 and client.get(lookup).json() == receipt
    with database() as conn:
        # The database foreign keys must cascade on parent shortening as well as removal.
        conn.execute("UPDATE workdays SET expires_at=clock_timestamp()-interval '1 second' WHERE id=%s", (plan['id'],))
        for table in ['automatic_notice_reviews', 'automatic_notice_review_operations']:
            actual = conn.execute(f'SELECT DISTINCT expires_at FROM {table} WHERE workday_id=%s', (plan['id'],)).fetchall()
            assert len(actual) == 1 and actual[0]['expires_at'] < datetime.now(UTC)
    assert client.get(path(plan)).status_code == save(client, plan, op).status_code == client.get(lookup).status_code == 410
    migrate()
    cleanup()
    with database() as conn:
        for table in ['automatic_notice_reviews', 'automatic_notice_review_operations']:
            assert not conn.execute(f'SELECT 1 FROM {table} WHERE workday_id=%s', (plan['id'],)).fetchone()
    assert client.get('/notices/' + record['id']).json() == ended


def test_exact_unicode_identifier_is_usable_for_reviews_and_cursor(client, users, fixture_feed):
    plan = planned(client, users)
    suffix = 'ø\n' + '🚌' * (MAX_ID - len(SITUATION_PREFIX) - 2)
    identifier = SITUATION_PREFIX + suffix
    collect((situation(suffix, STOP), 'false'))
    snapshot = get(client, plan)
    observed = entry(snapshot, suffix)
    assert observed['source']['content']['situation'] == identifier and len(identifier) == MAX_ID
    response = save(client, plan, operation(snapshot, observed))
    assert response.status_code == 200 and response.json()['situation'] == identifier
    assert entry(get(client, plan), suffix)['review_revision'] == 1
    response = client.get(path(plan), params={'cursor': identifier})
    assert response.status_code == 200 and response.json()['entries'] == []
    assert client.get(path(plan), params={'cursor': identifier + 'x'}).status_code == 422
    assert save(client, plan, operation(snapshot, observed, situation=SITUATION_PREFIX + '\0')).status_code == 422


def test_identity_migration_retains_membership_and_clears_ambiguous_stamp(fixture_feed):
    collect((situation('legacy', version='2') + situation('historic'), 'false'))
    generation = collect((situation('legacy', version='1') + situation('unique'), 'false'))
    migration = Path(__file__).resolve().parent.parent / 'migrations/private/020_automatic_notice_identity.sql'
    schema = sql.Identifier('automatic_migration_' + uuid4().hex)
    with database() as conn:
        # Exercise the exact upgrade against a populated 016-shaped schema.
        # Roll back the disposable schema and leave the API schema untouched.
        conn.execute(sql.SQL('CREATE SCHEMA {}').format(schema))
        conn.execute(sql.SQL('SET LOCAL search_path TO {}').format(schema))
        conn.execute('CREATE TABLE automatic_notice_sources AS TABLE public.automatic_notice_sources')
        conn.execute('CREATE TABLE automatic_notice_feed AS TABLE public.automatic_notice_feed')
        conn.execute("UPDATE automatic_notice_sources SET last_complete_generation=%s WHERE current_revision "
                     "AND situation='TRO:SituationNumber:legacy'", (generation,))
        before = conn.execute('SELECT revision,content,first_seen,last_seen,fetched_at,response_at '
                              'FROM automatic_notice_sources ORDER BY revision').fetchall()
        conn.execute(migration.read_text(encoding='utf-8'))
        after = conn.execute('SELECT revision,content,first_seen,last_seen,fetched_at,response_at '
                             'FROM automatic_notice_sources ORDER BY revision').fetchall()
        assert after == before
        identities = conn.execute('SELECT situation,last_complete_generation FROM automatic_notice_identities').fetchall()
        assert {item['situation']: item['last_complete_generation'] for item in identities} == {
            SITUATION_PREFIX + 'legacy': generation, SITUATION_PREFIX + 'unique': generation, SITUATION_PREFIX + 'historic': None}
        exact = conn.execute('SELECT situation,last_complete_generation FROM automatic_notice_sources').fetchall()
        assert [item for item in exact if item['last_complete_generation']] == [
            {'situation': SITUATION_PREFIX + 'unique', 'last_complete_generation': generation}]
        conn.rollback()


def test_real_postgres_reservations_precede_and_space_controlled_gets(isolated_feed):
    starts = []
    requestors = []

    async def unadmitted(*_):
        pytest.fail('Another writer crossed the persisted source budget')

    async def fake_get(requestor, remaining):
        assert remaining > 0
        requestors.append(requestor)
        with database() as conn:
            status = conn.execute('SELECT clock_timestamp() AS before_request,next_request_at,status '
                                  'FROM automatic_notice_feed').fetchone()
        starts.append(status['before_request'])
        assert status['status'] == 'collecting'
        # The reservation commits before transport can start, with a 10-second
        # crash margin on top of the 15.1-second spacing.
        assert 24 <= (status['next_request_at'] - starts[-1]).total_seconds() <= 26
        if len(starts) == 1:
            with ThreadPoolExecutor(max_workers=1) as contender:
                contender.submit(ingest.run_cycle, Event(), unadmitted).result(timeout=3)
            return page(situation('reserved-first'), 'true', requestor)
        return page(situation('reserved-last'), 'false', requestor)

    with database() as conn:
        conn.execute("UPDATE automatic_notice_feed SET next_request_at=clock_timestamp()+interval '1 minute'")
    ingest.run_cycle(Event(), unadmitted)
    with database() as conn:
        assert conn.execute('SELECT attempt_at FROM automatic_notice_feed').fetchone()['attempt_at'] is None
        conn.execute("UPDATE automatic_notice_feed SET next_request_at=clock_timestamp()-interval '1 second'")
    ingest.run_cycle(Event(), fake_get)
    assert len(starts) == 2 and len(set(requestors)) == 1
    assert (starts[1] - starts[0]).total_seconds() >= 15.1
    with database() as conn:
        final = conn.execute('SELECT status,next_request_at,result_at FROM automatic_notice_feed').fetchone()
        assert final['status'] == 'complete'
        # The final response lowers the crash margin while retaining request spacing.
        assert 14 <= (final['next_request_at'] - final['result_at']).total_seconds() <= 15.1
        conn.execute("UPDATE automatic_notice_feed SET attempt_at=clock_timestamp()-interval '10 minutes'")
    ingest.run_cycle(Event(), unadmitted)
