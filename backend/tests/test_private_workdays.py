"""Confirmation matrix against disposable PostgreSQL and guarded private HTTP."""
import concurrent.futures
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import UUID, uuid4

import httpx
import pytest
from fastapi import HTTPException

from app import auth, workday_storage
from app.private_storage import database, cleanup, migrate
from app.workday_domain import ConfirmRequest, DeleteWorkdayRequest
from test_private_access import client, headers, login, synthetic_only, users, URL
from test_private_drafts import save, content, wait_for_blocker


@pytest.fixture(autouse=True)
def teardown(users):
    yield
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        for table in ['workday_deletions','workday_operations', 'workdays', 'drafts', 'draft_operations', 'draft_deletions']:
            conn.execute(f'DELETE FROM {table} WHERE owner=ANY(%s)', (users[1],))


def facts():
    value = content()
    value['service_date'] = '2031-01-02'
    value['activities'][0].update(type='trip', start='2031-01-02T10:00+01:00', end='2031-01-02T11:00+01:00')
    return value


def review(client, draft):
    return client.post('/workday-reviews', headers=headers(client), json={'draft_id': draft['id'], 'expected_revision': draft['revision']})


def prepare(client, value=None):
    response, _ = save(client, value or facts())
    assert response.status_code == 200
    draft = response.json()
    response = review(client, draft)
    assert response.status_code == 200
    reviewed = response.json()
    body = {'operation_id': reviewed['operation_id'], 'expected_revision': draft['revision'],
            'acknowledgements': [item['id'] for item in reviewed['unknowns'] if item['id'].split(':')[0] not in reviewed['classifications_required']],
            'classifications': {key: 'manual' for key in reviewed['classifications_required']}}
    return draft, reviewed, body


def confirm(client, draft, body):
    return client.post('/drafts/' + draft['id'] + '/confirm', headers=headers(client), json=body)


@pytest.mark.parametrize('policy', [1, 2])
@pytest.mark.parametrize('bus', ['\ufeff', '\u001c', '\u0085'])
def test_review_policy_pins_pending_and_accepted_decisions(client, users, policy, bus):
    from psycopg.types.json import Jsonb
    assert login(client, users).status_code == 200
    draft = save(client, facts())[0].json()
    # Historical content must survive reads; neither the model nor migration normalizes it.
    value = {**draft['draft'], 'physical_bus': bus}
    with database() as conn:
        conn.execute('UPDATE drafts SET content=%s WHERE id=%s', (Jsonb(value), draft['id']))
    draft = client.get('/drafts/' + draft['id']).json()
    reviewed = review(client, draft).json()
    with database() as conn:
        conn.execute('UPDATE workday_operations SET assessment_policy_version=%s WHERE id=%s', (policy, reviewed['operation_id']))
        pending_before = conn.execute('SELECT * FROM workday_operations WHERE id=%s', (reviewed['operation_id'],)).fetchone()
    # Independent field oracle: Python strip treats U+001C as blank and FEFF
    # as meaningful; the explicit Unicode White_Space policy preserves U+001C.
    keys = {'day:physical_bus'} if bus == '\u0085' or bus == '\u001c' and policy == 1 else set()
    activity = value['activities'][0]
    prefix = activity['id'] + ':'
    keys |= {prefix + field for field in ['from_place', 'trip', 'direction']}
    keys.add(prefix + 'uncertainty')
    body = {'operation_id': reviewed['operation_id'], 'expected_revision': 1,
            'acknowledgements': sorted(keys), 'classifications': {}}
    migrate(); migrate()
    with database() as conn:
        assert conn.execute('SELECT * FROM workday_operations WHERE id=%s', (reviewed['operation_id'],)).fetchone() == pending_before
    response = confirm(client, draft, body)
    assert response.status_code == 200
    plan = response.json()
    assert {item['id'] for item in plan['unknowns']} == keys and plan['draft']['physical_bus'] == bus
    with database() as conn:
        assert conn.execute('SELECT assessment_policy_version FROM workdays WHERE id=%s', (plan['id'],)).fetchone()['assessment_policy_version'] == policy
        conn.execute('DELETE FROM drafts WHERE id=%s', (draft['id'],))
    migrate(); migrate()
    assert confirm(client, draft, body).json() == plan
    assert client.get('/workdays/' + plan['id']).json() == plan


def test_populated_pre007_tables_gain_only_pinned_defaults_without_rewriting_rows(client, users):
    from pathlib import Path
    assert login(client, users).status_code == 200
    draft, _, body = prepare(client)
    assert confirm(client, draft, body).status_code == 200
    prepare(client)  # Include pending draft and review operations alongside receipts.
    assert client.post('/draft-operations', headers=headers(client), json={}).status_code == 200
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        before = {}
        additions = {'draft_operations': ('normalize_physical_bus', False),
                     'workday_operations': ('assessment_policy_version', 1),
                     'workdays': ('assessment_policy_version', 1)}
        for table, (column, _) in additions.items():
            names = [row['column_name'] for row in conn.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name=%s AND column_name<>%s ORDER BY ordinal_position", (table, column)).fetchall()]
            fields = ','.join(names)
            # Temporary pre-007 tables shadow only this connection; public data
            # and the live API schema never change.
            conn.execute(f'CREATE TEMP TABLE {table} AS SELECT {fields} FROM public.{table} WHERE owner=%s', (users[1][0],))
            before[table] = conn.execute(f'SELECT * FROM {table} ORDER BY id').fetchall()
            assert before[table]
        sql = (Path(__file__).resolve().parent.parent / 'migrations/private/007_draft_contracts.sql').read_text(encoding='utf-8')
        conn.execute(sql); conn.execute(sql)
        for table, (column, default) in additions.items():
            after = conn.execute(f'SELECT * FROM {table} ORDER BY id').fetchall()
            assert all(row[column] == default for row in after)
            assert [{key: value for key, value in row.items() if key != column} for row in after] == before[table]


def test_populated_pre008_policy_constraints_widen_without_changing_any_row(client, users):
    from pathlib import Path
    assert login(client, users).status_code == 200
    draft, _, body = prepare(client)
    assert confirm(client, draft, body).status_code == 200
    prepare(client)
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        before = {}
        for table, policy in [('workdays', 1), ('workday_operations', 2)]:
            conn.execute(f'CREATE TEMP TABLE {table} AS SELECT * FROM public.{table} WHERE owner=%s', (users[1][0],))
            conn.execute(f'UPDATE {table} SET assessment_policy_version=%s', (policy,))
            conn.execute(f'ALTER TABLE {table} ADD CONSTRAINT {table}_assessment_policy_version_check CHECK (assessment_policy_version IN (1,2))')
            before[table] = conn.execute(f'SELECT * FROM {table} ORDER BY id').fetchall()
            assert before[table]
        sql = (Path(__file__).resolve().parent.parent / 'migrations/private/008_review_feedback.sql').read_text(encoding='utf-8')
        conn.execute(sql); conn.execute(sql)
        for table in before:
            assert conn.execute(f'SELECT * FROM {table} ORDER BY id').fetchall() == before[table]
            conn.execute(f'UPDATE {table} SET assessment_policy_version=3')


@pytest.mark.parametrize('kind', ['trip', 'deadhead', 'deadhead_car', 'CAR', 'Tomkjøring med CAR', 'manual', 'Sign-on', 'Sign-off', 'Coffee', 'MealBreak', 'Split break', 'Paid meal before', 'Paid meal after', 'Fadder', 'Instruktør', 'Travel to', 'Travel from', None])
def test_new_review_explicit_unknown_field_matrix(client, users, kind):
    assert login(client, users).status_code == 200
    value = facts()
    activity = value['activities'][0]
    activity.update(type=kind, trip=None, line=None, direction=None, from_place=None, to_place=None,
                    raw_code=None, source_start=None, source_end=None, provenance=None, uncertainty='Check source')
    draft, reviewed, body = prepare(client, value)
    keys = {item['id'] for item in reviewed['unknowns']}
    prefix = activity['id'] + ':'
    assert {prefix + field for field in ['from_place', 'to_place', 'uncertainty']} <= keys if kind in ['trip', None] else not keys
    assert {field for field in ['trip', 'line', 'direction'] if prefix + field in keys} == ({'trip', 'line', 'direction'} if kind in ['trip', None] else set())
    assert not any(prefix + field in keys for field in ['raw_code', 'source_start', 'source_end', 'provenance'])
    with database() as conn:
        pending = conn.execute('SELECT * FROM workday_operations WHERE id=%s', (body['operation_id'],)).fetchone()
        source = conn.execute('SELECT * FROM drafts WHERE id=%s', (draft['id'],)).fetchone()
    for omitted in body['acknowledgements']:
        incomplete = {**body, 'acknowledgements': [key for key in body['acknowledgements'] if key != omitted]}
        assert confirm(client, draft, incomplete).status_code == 422
        with database() as conn:
            assert conn.execute('SELECT * FROM workday_operations WHERE id=%s', (body['operation_id'],)).fetchone() == pending
            assert conn.execute('SELECT * FROM drafts WHERE id=%s', (draft['id'],)).fetchone() == source
            assert not conn.execute('SELECT id FROM workdays WHERE source_draft_id=%s', (draft['id'],)).fetchone()
    assert confirm(client, draft, body).status_code == 200


@pytest.mark.parametrize('classification', ['trip', 'manual', 'deadhead', 'Coffee'])
def test_v3_classification_controls_exact_effective_trip_set(client, users, classification):
    assert login(client, users).status_code == 200
    value = facts()
    activity = value['activities'][0]
    activity.update(type='Unmapped', trip=None, line=None, direction=None, from_place=None, to_place=None, uncertainty='Concrete note')
    draft, reviewed, body = prepare(client, value)
    body['classifications'] = {activity['id']: classification}
    expected = [activity['id'] + ':' + field for field in ['from_place', 'to_place', 'trip', 'line', 'direction', 'uncertainty']] if classification == 'trip' else []
    body['acknowledgements'] = expected
    with database() as conn:
        before = conn.execute('SELECT * FROM workday_operations WHERE id=%s', (body['operation_id'],)).fetchone()
        assert before['assessment_policy_version'] == 3
    for invalid in [[key for key in expected if key != omitted] for omitted in expected] + [expected + ['day:physical_bus'], expected + [activity['id'] + ':raw_code']]:
        assert confirm(client, draft, {**body, 'acknowledgements': invalid}).status_code == 422
        with database() as conn:
            assert conn.execute('SELECT * FROM workday_operations WHERE id=%s', (body['operation_id'],)).fetchone() == before
            assert not conn.execute('SELECT id FROM workdays WHERE source_draft_id=%s', (draft['id'],)).fetchone()
    response = confirm(client, draft, body)
    assert response.status_code == 200
    plan = response.json()
    assert plan['draft'] == draft['draft']
    assert {item['id'] for item in plan['unknowns']} == set(expected)
    assert client.get('/workday-operations/' + body['operation_id']).json()['result'] == plan


@pytest.mark.parametrize('suffix', ['', ' Concrete manual note.'])
def test_v3_only_exact_generated_marker_fragments_are_neutral(client, users, suffix):
    from app.private_import import interpret
    from app.pdf_import import parse_document
    from test_pdf_import import synthetic_text_pdf
    from app.import_issues import annotation_rows
    assert login(client, users).status_code == 200
    value = interpret(parse_document(synthetic_text_pdf())).model_dump(mode='json')
    metadata = value['import_metadata']
    # Retained provenance independently identifies the row receiving the old text.
    row_number, markers = next(iter(annotation_rows(metadata).items()))
    source = next(row for row in metadata['activities'] if row['source_order'] == row_number)
    target = next(row for row in value['activities'] if row['id'] == source['activity_id'])
    for index, activity in enumerate(value['activities']):
        activity.update(type='manual', start=f'2031-01-02T10:{index:02}+01:00', end=f'2031-01-02T10:{index:02}+01:00')
    target.update(type='trip', uncertainty=' '.join(f'Kildemerket {marker["value"]} har ukjent betydning (side {marker["provenance"]["page"]}).' for marker in markers) + suffix)
    draft, reviewed, body = prepare(client, value)
    notes = [item for item in reviewed['unknowns'] if item['id'] == target['id'] + ':uncertainty']
    assert len(notes) == bool(suffix)
    if suffix:
        assert notes[0]['label'].endswith('Concrete manual note.')
        assert 'Kildemerket' not in notes[0]['label']
    assert not any(item['id'].startswith('source:') for item in reviewed['unknowns'])
    assert confirm(client, draft, body).json()['draft'] == draft['draft']
    assert client.get('/drafts/' + draft['id']).json() == draft


@pytest.mark.parametrize('remainder', ['', 'Concrete manual note.', 'Kildemerket other har ukjent betydning (side 1).'])
def test_v3_legacy_null_marker_positions_do_not_invent_associations(client, users, remainder):
    from app.private_import import interpret
    from app.pdf_import import parse_document
    from app.draft_domain import DraftContent
    from app.import_issues import annotation_rows, marker_fragments
    from test_pdf_import import synthetic_text_pdf
    assert login(client, users).status_code == 200
    value = interpret(parse_document(synthetic_text_pdf())).model_dump(mode='json')
    for activity in value['activities']:
        activity.update(type='trip', start='2031-01-02T10:00+01:00', end='2031-01-02T11:00+01:00', uncertainty='Kildemerket t har ukjent betydning (side 1). ' + remainder)
    for source in value['import_metadata']['activities']:
        for points in source['provenance'].values():
            if isinstance(points, list):
                for point in points:
                    point['line'] = None
    value['import_metadata']['annotations'] = [{'value': 't', 'meaning': None, 'provenance': {'page': 1, 'column': 1, 'line': None}}]
    validated = DraftContent.model_validate(value)
    assert annotation_rows(validated.import_metadata.model_dump(mode='json')) == {}
    assert marker_fragments(validated) == ['Kildemerket t har ukjent betydning (side 1).']
    draft, reviewed, body = prepare(client, validated.model_dump(mode='json'))
    notes = [item for item in reviewed['unknowns'] if item['id'].endswith(':uncertainty')]
    assert len(notes) == (len(value['activities']) if remainder else 0)
    assert all(item['label'].split(': ', 1)[1] == remainder for item in notes)
    assert confirm(client, draft, body).json()['draft'] == draft['draft']


def test_plan_deletion_concurrent_receipt_preserves_source_other_records_and_denies_resurrection(client, users):
    assert login(client, users).status_code == 200
    draft, _, confirmation = prepare(client)
    pending = review(client, draft).json()
    plan = confirm(client, draft, confirmation).json()
    other_draft, _, other_body = prepare(client)
    other_plan = confirm(client, other_draft, other_body).json()
    body = {'operation_id': str(uuid4()), 'source_revision': plan['source_revision']}
    path = '/workdays/' + plan['id'] + '/delete'
    assert client.post(path, json=body).status_code == 403
    assert client.post(path, headers={**headers(client), 'Origin': 'http://evil.invalid'}, json=body).status_code == 403
    assert client.post(path, headers=headers(client), json={**body, 'source_revision': 2}).status_code == 409
    with httpx.Client(base_url=URL) as other:
        assert other.post(path, headers=headers(other), json=body).status_code == 401
        assert login(other, users, 1).status_code == 200
        assert other.post(path, headers=headers(other), json=body).status_code == 404
    proof, cookies = headers(client), dict(client.cookies)
    def send(_):
        return httpx.post(URL + path, headers=proof, cookies=cookies, json=body, timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        replies = list(pool.map(send, range(2)))
    expected = {'operation_id': body['operation_id'], 'deleted_id': plan['id'], 'source_revision': 1}
    assert all(reply.status_code == 200 and reply.json() == expected for reply in replies)
    assert client.get('/workday-deletions/' + body['operation_id']).json() == expected
    assert client.get('/workday-deletions/' + body['operation_id']).headers['cache-control'] == 'no-store'
    assert client.post(path, headers=headers(client), json=body).json() == expected
    assert client.post(path, headers=headers(client), json={**body, 'source_revision': 2}).status_code == 409
    assert client.post('/workdays/' + other_plan['id'] + '/delete', headers=headers(client), json=body).status_code == 409
    assert client.get('/workdays/' + plan['id']).status_code == 404
    assert client.get('/drafts/' + draft['id']).json() == draft
    assert client.get('/workdays/' + other_plan['id']).json() == other_plan
    assert confirm(client, draft, confirmation).status_code == 404
    assert confirm(client, draft, {**confirmation, 'operation_id': pending['operation_id']}).status_code == 409
    assert review(client, draft).status_code == 409
    with httpx.Client(base_url=URL) as other:
        assert login(other, users, 1).status_code == 200
        assert other.get('/workday-deletions/' + body['operation_id']).status_code == 404
    with database() as conn:
        receipt = conn.execute('SELECT * FROM workday_deletions WHERE id=%s', (body['operation_id'],)).fetchone()
        assert set(receipt) == {'id', 'owner', 'workday_id', 'source_revision', 'expires_at'}
        assert receipt['expires_at'] == datetime.fromisoformat(plan['expires_at'])
        assert conn.execute('SELECT confirmed FROM drafts WHERE id=%s', (draft['id'],)).fetchone()['confirmed']
        assert not conn.execute('SELECT 1 FROM workday_operations WHERE id=%s', (confirmation['operation_id'],)).fetchone()
        conn.execute('UPDATE workday_deletions SET expires_at=clock_timestamp() WHERE id=%s', (body['operation_id'],))
    assert client.get('/workday-deletions/' + body['operation_id']).status_code == 410
    cleanup()
    assert client.get('/workday-deletions/' + body['operation_id']).status_code == 404


@pytest.mark.parametrize('expiry', ['plan', 'session'])
def test_plan_deletion_expiry_at_acceptance_rolls_back_receipt_and_plan(client, users, monkeypatch, expiry):
    assert login(client, users).status_code == 200
    draft, _, confirmation = prepare(client)
    plan = confirm(client, draft, confirmation).json()
    body = DeleteWorkdayRequest(operation_id=uuid4(), source_revision=1)
    request = SimpleNamespace(cookies={auth.SESSION: client.cookies.get(auth.SESSION)})
    class Connection:
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            if query.startswith('DELETE FROM workdays WHERE id='):
                if expiry == 'plan': self.conn.execute("UPDATE workdays SET final_end=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (plan['id'],))
                else: self.conn.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days',expires_at=statement_timestamp() WHERE owner=%s", (users[1][0],))
            return self.conn.execute(query, params)
    @contextmanager
    def wrapped():
        with database() as conn: yield Connection(conn)
    monkeypatch.setattr(workday_storage, 'database', wrapped)
    with pytest.raises(HTTPException) as error:
        workday_storage.delete(request, UUID(plan['id']), body)
    assert error.value.status_code == (410 if expiry == 'plan' else 401)
    assert client.get('/workdays/' + plan['id']).json() == plan
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM workday_deletions WHERE id=%s', (body.operation_id,)).fetchone()


def test_plan_deletion_competing_distinct_operations_accepts_only_one_receipt(client, users):
    assert login(client, users).status_code == 200
    draft, _, confirmation = prepare(client)
    plan = confirm(client, draft, confirmation).json()
    other_draft, _, other_confirmation = prepare(client)
    other_plan = confirm(client, other_draft, other_confirmation).json()
    bodies = [{'operation_id': str(uuid4()), 'source_revision': 1} for _ in range(2)]
    proof, cookies = headers(client), dict(client.cookies)
    path = '/workdays/' + plan['id'] + '/delete'
    def send(body):
        return httpx.post(URL + path, headers=proof, cookies=cookies, json=body, timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        replies = list(pool.map(send, bodies))
    assert sorted(reply.status_code for reply in replies) == [200, 404]
    winner = next(reply.json() for reply in replies if reply.status_code == 200)
    loser = next(body for body, reply in zip(bodies, replies) if reply.status_code == 404)
    assert client.get('/workday-deletions/' + winner['operation_id']).json() == winner
    assert client.get('/workday-deletions/' + loser['operation_id']).status_code == 404
    assert client.post(path, headers=headers(client), json=loser).status_code == 404
    assert client.get('/drafts/' + draft['id']).json() == draft
    assert client.get('/drafts/' + other_draft['id']).json() == other_draft
    assert client.get('/workdays/' + other_plan['id']).json() == other_plan
    with database() as conn:
        receipts = conn.execute('SELECT id FROM workday_deletions WHERE workday_id=%s', (plan['id'],)).fetchall()
        assert [str(row['id']) for row in receipts] == [winner['operation_id']]


@pytest.mark.parametrize('source_removed', ['deleted', 'expired'])
def test_plan_deletion_without_surviving_source_replays_receipt_without_resurrection(client, users, source_removed):
    assert login(client, users).status_code == 200
    draft, _, confirmation = prepare(client)
    plan = confirm(client, draft, confirmation).json()
    if source_removed == 'deleted':
        assert client.post('/drafts/' + draft['id'] + '/delete', headers=headers(client), json={'operation_id': str(uuid4()), 'expected_revision': 1}).status_code == 200
    else:
        with database() as conn:
            conn.execute("UPDATE drafts SET created_at=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (draft['id'],))
        cleanup()
    assert client.get('/drafts/' + draft['id']).status_code == 404
    assert confirm(client, draft, confirmation).json() == plan
    body = {'operation_id': str(uuid4()), 'source_revision': 1}
    path = '/workdays/' + plan['id'] + '/delete'
    response = client.post(path, headers=headers(client), json=body)
    assert response.status_code == 200
    receipt = response.json()
    cleanup()
    assert client.post(path, headers=headers(client), json=body).json() == receipt
    assert client.get('/workday-deletions/' + body['operation_id']).json() == receipt
    assert client.get('/workdays/' + plan['id']).status_code == 404
    assert client.get('/workday-operations/' + confirmation['operation_id']).status_code == 404
    assert confirm(client, draft, confirmation).status_code == 404
    assert review(client, draft).status_code == 404
    with database() as conn:
        row = conn.execute('SELECT expires_at FROM workday_deletions WHERE id=%s', (body['operation_id'],)).fetchone()
        assert row['expires_at'] == datetime.fromisoformat(plan['expires_at'])
        assert not conn.execute('SELECT 1 FROM workday_operations WHERE workday_id=%s OR id=%s', (plan['id'], confirmation['operation_id'])).fetchone()


def test_exact_snapshot_replay_decisions_and_independent_source_retention(client, users):
    assert login(client, users).status_code == 200
    value = facts()
    value['vehicle_duty_changes'] = [{'from_activity_id': value['activities'][0]['id'], 'vehicle_duty': 'CAR - 1'}]
    value['activities'][0]['type'] = 'Unmapped'
    draft, reviewed, body = prepare(client, value)
    assert reviewed['draft'] == draft['draft'] and not reviewed['blockers']
    response = confirm(client, draft, body)
    assert response.status_code == 200
    plan = response.json()
    assert plan['draft'] == draft['draft'] and plan['state'] == 'confirmed'
    assert plan['source_revision'] == 1 and plan['source_draft_id'] == draft['id']
    assert plan['final_end'] == '2031-01-02T10:00:00Z'
    assert datetime.fromisoformat(plan['expires_at']) - datetime.fromisoformat(plan['final_end']) == timedelta(days=7)
    assert confirm(client, draft, body).json() == plan
    assert confirm(client, draft, {**body, 'classifications': {value['activities'][0]['id']: 'trip'}}).status_code == 409
    assert confirm(client, draft, {**body, 'acknowledgements': ['extra:decision']}).status_code == 409
    with database() as conn:
        conn.execute('DELETE FROM drafts WHERE id=%s', (draft['id'],))
    cleanup(); migrate(); migrate()
    assert confirm(client, draft, body).json() == plan
    assert client.get('/workday-operations/' + body['operation_id']).json() == {'state': 'accepted', 'result': plan}
    assert client.get('/workdays/' + plan['id']).json() == plan
    assert client.get('/workdays').json()['workdays'][0]['id'] == plan['id']


@pytest.mark.parametrize('change', ['date', 'empty', 'start', 'end', 'order', 'expired', 'ack', 'type', 'extra_class', 'duplicate_ack'])
def test_direct_invalid_confirmation_does_not_write(client, users, change):
    assert login(client, users).status_code == 200
    value = facts()
    if change == 'date': value['service_date'] = None
    if change == 'empty': value['activities'] = []
    if change == 'start': value['activities'][0]['start'] = None
    if change == 'end': value['activities'][0]['end'] = None
    if change == 'order': value['activities'].append({**value['activities'][0], 'id': str(uuid4()), 'start': '2031-01-02T09:00+01:00'})
    if change == 'expired': value['activities'][0].update(start='2020-01-01T10:00+01:00', end='2020-01-01T11:00+01:00')
    if change == 'type': value['activities'][0]['type'] = None
    draft, reviewed, body = prepare(client, value)
    if change == 'ack': body['acknowledgements'] = []
    if change == 'type': body['classifications'] = {}
    if change == 'extra_class': body['classifications'] = {str(uuid4()): 'manual'}
    if change == 'duplicate_ack': body['acknowledgements'] *= 2
    assert confirm(client, draft, body).status_code in {410, 422}
    assert client.get('/workdays').json() == {'workdays': [], 'next_cursor': None}
    assert client.get('/drafts/' + draft['id']).json() == draft
    assert client.get('/workday-operations/' + body['operation_id']).json() == {'state': 'pending', 'result': None}


def test_overlaps_gaps_zero_transfer_latest_end_and_separate_drafts(client, users):
    assert login(client, users).status_code == 200
    value = facts()
    first = value['activities'][0]
    first['end'] = '2031-01-02T14:00+01:00'
    value['activities'] += [{**first, 'id': str(uuid4()), 'start': '2031-01-02T11:00+01:00', 'end': '2031-01-02T11:00+01:00', 'type': 'deadhead'},
                            {**first, 'id': str(uuid4()), 'start': '2031-01-02T12:00+01:00', 'end': '2031-01-02T13:00+01:00'}]
    draft, _, body = prepare(client, value)
    plan = confirm(client, draft, body).json()
    assert plan['final_end'] == '2031-01-02T13:00:00Z'
    other, _, other_body = prepare(client, value)
    assert confirm(client, other, other_body).status_code == 200
    assert len(client.get('/workdays').json()['workdays']) == 2


def test_concurrent_operations_and_stale_edit_delete_are_rejected(client, users):
    assert login(client, users).status_code == 200
    draft, _, body = prepare(client)
    second = review(client, draft).json()
    other = {**body, 'operation_id': second['operation_id']}
    proof, cookies = headers(client), dict(client.cookies)
    def send(payload):
        return httpx.post(URL + '/drafts/' + draft['id'] + '/confirm', headers=proof, cookies=cookies, json=payload, timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(send, [body, other]))
    assert sorted(result.status_code for result in results) == [200, 409]
    assert len(client.get('/workdays').json()['workdays']) == 1
    stale, _, stale_body = prepare(client)
    assert save(client, facts(), stale['id'], 1)[0].status_code == 200
    assert confirm(client, stale, stale_body).status_code == 409
    deleted, _, deleted_body = prepare(client)
    assert client.post('/drafts/' + deleted['id'] + '/delete', headers=headers(client), json={'operation_id': str(uuid4()), 'expected_revision': 1}).status_code == 200
    assert confirm(client, deleted, deleted_body).status_code == 404


def test_routes_owner_session_origin_bounds_and_no_store(client, users):
    assert login(client, users).status_code == 200
    draft, reviewed, body = prepare(client)
    plan = confirm(client, draft, body).json()
    reads = ['/workdays', '/workdays/' + plan['id'], '/workday-operations/' + body['operation_id']]
    writes = [('/workday-reviews', {'draft_id': draft['id'], 'expected_revision': 1}), ('/drafts/' + draft['id'] + '/confirm', body)]
    for path, payload in writes:
        assert client.post(path, json=payload).status_code == 403
        assert client.post(path, headers={**headers(client), 'Origin': 'http://evil.invalid'}, json=payload).status_code == 403
    for path in reads:
        assert client.get(path).headers['cache-control'] == 'no-store'
    with httpx.Client(base_url=URL) as other:
        for path in reads: assert other.get(path).status_code == 401
        assert login(other, users, 1).status_code == 200
        assert other.get('/workdays').json() == {'workdays': [], 'next_cursor': None}
        for path in reads[1:]: assert other.get(path).status_code == 404
        for path, payload in writes: assert other.post(path, headers=headers(other), json=payload).status_code == 404
    assert client.post('/workday-reviews', headers=headers(client), content=b'x' * 4097).status_code == 413
    assert client.get('/workdays?cursor=invalid').status_code == 422


def test_unused_admission_200_rejection_has_no_mutation_and_accepted_expired_excluded(client, users):
    assert login(client, users).status_code == 200
    draft, _, body = prepare(client)
    assert confirm(client, draft, body).status_code == 200
    draft = save(client, facts())[0].json()
    expired = review(client, draft).json()['operation_id']
    with database() as conn:
        conn.execute('UPDATE workday_operations SET expires_at=clock_timestamp() WHERE id=%s', (expired,))
    # Accepted and expired operations do not consume unused-operation admission.
    for _ in range(200): assert review(client, draft).status_code == 200
    with database() as conn:
        before = conn.execute('SELECT * FROM workday_operations WHERE owner=%s ORDER BY id', (users[1][0],)).fetchall()
    assert review(client, draft).status_code == 429
    with database() as conn:
        assert conn.execute('SELECT * FROM workday_operations WHERE owner=%s ORDER BY id', (users[1][0],)).fetchall() == before


@pytest.mark.parametrize('expiry', ['operation', 'source', 'plan'])
def test_expiry_at_final_acceptance_rolls_back_insert(client, users, monkeypatch, expiry):
    from zoneinfo import ZoneInfo
    assert login(client, users).status_code == 200
    value = facts()
    if expiry == 'plan':
        ending = datetime.now(ZoneInfo('Europe/Oslo')).replace(microsecond=0) - timedelta(days=7) + timedelta(seconds=3)
        value['activities'][0].update(start=ending.isoformat(), end=ending.isoformat())
    draft, reviewed, body = prepare(client, value)
    request = SimpleNamespace(cookies={auth.SESSION: client.cookies.get(auth.SESSION)})
    real_database = database
    class Connection:
        def __init__(self, conn): self.conn = conn
        def execute(self, query, params=None):
            if query.startswith('UPDATE workday_operations SET workday_id='):
                # Inject expiration after the candidate INSERT, at the exact
                # acceptance boundary; production predicates must roll it back.
                if expiry == 'operation': self.conn.execute('UPDATE workday_operations SET expires_at=clock_timestamp() WHERE id=%s', (body['operation_id'],))
                if expiry == 'source': self.conn.execute("UPDATE drafts SET created_at=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (draft['id'],))
                if expiry == 'plan':
                    self.conn.execute('SELECT pg_sleep(GREATEST(0,extract(epoch FROM (%s::timestamptz-clock_timestamp()))+.05))', (reviewed['expires_at'],))
            return self.conn.execute(query, params)
    @contextmanager
    def wrapped():
        with real_database() as conn: yield Connection(conn)
    monkeypatch.setattr(workday_storage, 'database', wrapped)
    with pytest.raises(HTTPException) as error:
        workday_storage.confirm(request, UUID(draft['id']), ConfirmRequest.model_validate(body))
    assert error.value.status_code == 410
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM workdays WHERE source_draft_id=%s', (draft['id'],)).fetchone()
        assert conn.execute('SELECT workday_id FROM workday_operations WHERE id=%s', (body['operation_id'],)).fetchone()['workday_id'] is None


def test_expired_plan_purges_accepted_metadata_and_pending_source_expiry(client, users):
    assert login(client, users).status_code == 200
    draft, _, body = prepare(client)
    plan = confirm(client, draft, body).json()
    with database() as conn:
        conn.execute("UPDATE workdays SET final_end=statement_timestamp()-interval '7 days', expires_at=statement_timestamp() WHERE id=%s", (plan['id'],))
        conn.execute('UPDATE workday_operations SET expires_at=clock_timestamp() WHERE id=%s', (body['operation_id'],))
    assert client.get('/workdays/' + plan['id']).status_code == 410
    assert confirm(client, draft, body).status_code == 410
    cleanup()
    assert client.get('/workday-operations/' + body['operation_id']).status_code == 404
    draft = save(client, facts())[0].json()
    unused = review(client, draft).json()['operation_id']
    with database() as conn:
        conn.execute("UPDATE drafts SET created_at=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (draft['id'],))
    assert client.get('/workday-operations/' + unused).status_code == 410
    cleanup()
    assert client.get('/workday-operations/' + unused).status_code == 404


@pytest.mark.parametrize('number', [1, 8, 9])
def test_imported_source_corrections_duty_car_and_overnight_survive_confirmation(client, users, number):
    from pathlib import Path
    assert login(client, users).status_code == 200
    response = client.post('/imports/pdf', headers={**headers(client), 'Content-Type': 'application/pdf'}, content=Path(f'/fixtures/Eksempel-{number}-anonymisert.pdf').read_bytes())
    assert response.status_code == 200
    value = response.json()
    metadata = value['import_metadata']
    # Owner corrections establish a future, explicit overnight calendar without
    # changing the imported source clocks, IDs, CAR or duty anchors.
    value['service_date'] = '2031-01-02'
    for index, activity in enumerate(value['activities']):
        activity.update(start=f'2031-01-03T00:{index:02}+01:00', end=f'2031-01-03T00:{index:02}+01:00')
    value['activities'][0]['start'] = '2031-01-02T23:59+01:00'
    draft, reviewed, body = prepare(client, value)
    assert not reviewed['blockers']
    response = confirm(client, draft, body)
    assert response.status_code == 200
    plan = response.json()
    assert plan['draft'] == draft['draft']
    assert plan['draft']['import_metadata'] == metadata
    assert plan['draft']['physical_bus'] is None
    assert client.get('/workdays/' + plan['id']).json() == plan


def test_paginated_discovery_exposes_all_201_live_owned_plans(client, users):
    assert login(client, users).status_code == 200
    draft, _, body = prepare(client)
    original = confirm(client, draft, body).json()
    with database() as conn:
        for _ in range(200):
            conn.execute('INSERT INTO workdays(id,owner,source_draft_id,source_revision,final_end,expires_at,content,acknowledgements,classifications) SELECT %s,owner,%s,source_revision,final_end,expires_at,content,acknowledgements,classifications FROM workdays WHERE id=%s', (uuid4(), uuid4(), original['id']))
        expected = {str(row['id']) for row in conn.execute('SELECT id FROM workdays WHERE owner=%s', (users[1][0],)).fetchall()}
    seen, cursor, pages = [], None, 0
    while True:
        response = client.get('/workdays' + ('?cursor=' + cursor if cursor else ''))
        assert response.status_code == 200
        value = response.json()
        assert len(value['workdays']) <= 50
        seen.extend(item['id'] for item in value['workdays']); pages += 1
        cursor = value['next_cursor']
        if cursor is None: break
        assert pages < 10
    assert len(seen) == len(set(seen)) == 201 and set(seen) == expected and pages == 5


@pytest.mark.parametrize('action', ['review', 'confirm', 'read', 'lookup'])
def test_waiting_confirmation_boundaries_recheck_session_after_row_lock(client, users, action):
    assert login(client, users).status_code == 200
    draft, _, body = prepare(client)
    plan = confirm(client, draft, body).json() if action in {'read', 'lookup'} else None
    proof, cookies = headers(client), dict(client.cookies)
    with database() as blocker, concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        if plan: blocker.execute('SELECT id FROM workdays WHERE id=%s FOR UPDATE', (plan['id'],))
        else: blocker.execute('SELECT id FROM drafts WHERE id=%s FOR UPDATE', (draft['id'],))
        with database() as setup:
            expiry = setup.execute("UPDATE sessions SET created_at=statement_timestamp()-interval '14 days'+interval '1 second',expires_at=statement_timestamp()+interval '1 second' WHERE owner=%s RETURNING expires_at", (users[1][0],)).fetchone()['expires_at']
        def send():
            with httpx.Client(base_url=URL, cookies=cookies, timeout=10) as remote:
                if action == 'read': return remote.get('/workdays/' + plan['id'])
                if action == 'lookup': return remote.get('/workday-operations/' + body['operation_id'])
                if action == 'review': return remote.post('/workday-reviews', headers=proof, json={'draft_id': draft['id'], 'expected_revision': 1})
                return remote.post('/drafts/' + draft['id'] + '/confirm', headers=proof, json=body)
        future = pool.submit(send)
        try:
            wait_for_blocker(blocker.info.backend_pid)
            with database() as observer:
                observer.execute('SELECT pg_sleep(GREATEST(0,extract(epoch FROM (%s::timestamptz-clock_timestamp()))+.05))', (expiry,))
        finally: blocker.commit()
        assert future.result().status_code == 401


def test_largest_unknown_decision_set_fits_bounded_confirmation_contract(client, users):
    from app.private_import import interpret
    from app.pdf_import import parse_document
    from test_pdf_import import synthetic_text_pdf
    assert login(client, users).status_code == 200
    value = facts()
    base = value['activities'][0]
    value.update(vehicle_duty=None, physical_bus=None)
    value['activities'] = [{**base, 'id': str(uuid4()), 'type': None, 'from_place': None, 'to_place': None, 'trip': None, 'line': None, 'direction': None} for _ in range(200)]
    value['vehicle_duty_changes'] = [{'from_activity_id': activity['id'], 'vehicle_duty': None} for activity in value['activities']]
    metadata = interpret(parse_document(synthetic_text_pdf())).model_dump(mode='json')['import_metadata']
    metadata['unresolved'] = [{'code': 'synthetic-unknown', 'activity': None, 'field': None, 'provenance': None}] * 1000
    metadata['annotations'] = [{'value': 'synthetic-marker', 'meaning': None, 'provenance': {'page': 1}}] * 400
    value['import_metadata'] = metadata
    draft, reviewed, body = prepare(client, value)
    assert len(reviewed['unknowns']) == 1200
    body['classifications'] = {key: 'trip' for key in reviewed['classifications_required']}
    body['acknowledgements'] = [item['id'] for item in reviewed['unknowns']]
    response = confirm(client, draft, body)
    assert response.status_code == 200
    assert len(response.json()['acknowledgements']) == 1200


@pytest.mark.parametrize('kind', ['Fadder', 'Instruktør', 'Travel to', 'Travel from', 'Paid meal before', 'Paid meal after', 'CAR', 'Tomkjøring med CAR'])
def test_advertised_classifications_accept_previously_omitted_choices(client, users, kind):
    assert login(client, users).status_code == 200
    value = facts(); value['activities'][0]['type'] = None
    draft, reviewed, body = prepare(client, value)
    assert kind in reviewed['supported_types']
    body['classifications'] = {value['activities'][0]['id']: kind}
    response = confirm(client, draft, body)
    assert response.status_code == 200
    assert response.json()['draft'] == draft['draft']
    assert response.json()['classifications'] == body['classifications']


@pytest.mark.parametrize('duty', [None, '   '])
def test_unknown_activity_duty_anchor_is_source_fact_without_decision_and_survives(client, users, duty):
    assert login(client, users).status_code == 200
    value = facts()
    anchor = value['activities'][0]['id']
    value['vehicle_duty_changes'] = [{'from_activity_id': anchor, 'vehicle_duty': duty}]
    draft, reviewed, body = prepare(client, value)
    key = 'duty:' + anchor + ':vehicle_duty'
    assert not any(item['id'] == key for item in reviewed['unknowns'])
    assert confirm(client, draft, {**body, 'acknowledgements': body['acknowledgements'] + [key]}).status_code == 422
    response = confirm(client, draft, body)
    assert response.status_code == 200
    assert response.json()['draft'] == draft['draft']
    assert response.json()['draft']['vehicle_duty_changes'][0]['vehicle_duty'] == duty


def test_concurrent_identical_operation_returns_same_plan(client, users):
    assert login(client, users).status_code == 200
    draft, _, body = prepare(client)
    proof, cookies = headers(client), dict(client.cookies)
    def send(_):
        return httpx.post(URL + '/drafts/' + draft['id'] + '/confirm', headers=proof, cookies=cookies, json=body, timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        replies = list(pool.map(send, range(2)))
    assert [reply.status_code for reply in replies] == [200, 200]
    assert replies[0].json() == replies[1].json()
    assert len(client.get('/workdays').json()['workdays']) == 1


def test_confirmed_marker_rejects_review_and_confirmation_after_plan_purge_and_source_edit(client, users):
    assert login(client, users).status_code == 200
    draft, _, body = prepare(client)
    pending = review(client, draft).json()
    plan = confirm(client, draft, body).json()
    assert confirm(client, draft, body).json() == plan
    with database() as conn:
        count = conn.execute('SELECT count(*) AS n FROM workday_operations WHERE owner=%s', (users[1][0],)).fetchone()['n']
    assert review(client, draft).status_code == 409
    with database() as conn:
        assert conn.execute('SELECT count(*) AS n FROM workday_operations WHERE owner=%s', (users[1][0],)).fetchone()['n'] == count
        conn.execute("UPDATE workdays SET final_end=statement_timestamp()-interval '7 days',expires_at=statement_timestamp() WHERE id=%s", (plan['id'],))
    cleanup()
    assert confirm(client, draft, {**body, 'operation_id': pending['operation_id']}).status_code == 409
    updated = save(client, facts(), draft['id'], 1)[0]
    assert updated.status_code == 200
    assert review(client, updated.json()).status_code == 409
    assert confirm(client, updated.json(), {**body, 'operation_id': pending['operation_id'], 'expected_revision': 2}).status_code == 409
    assert client.get('/workdays').json() == {'workdays': [], 'next_cursor': None}
