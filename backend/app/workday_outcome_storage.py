"""Parent-locked outcomes and terminal commands; historical receipts are not authority."""
from datetime import timedelta
from fastapi import HTTPException
from psycopg.types.json import Jsonb
from . import auth, draft_storage, workday_storage, workday_lifecycle_storage, workday_bus_storage
from .private_storage import database
from .workday_outcome_domain import OutcomeRecord
from .workday_lifecycle_domain import LifecycleRecord


def current(conn, plan):
    revision = conn.execute('SELECT revision FROM workday_outcome_revisions WHERE workday_id=%s', (plan['id'],)).fetchone()
    rows = conn.execute('SELECT activity_id,outcome FROM workday_outcomes WHERE workday_id=%s', (plan['id'],)).fetchall()
    values = {str(row['activity_id']): row['outcome'] for row in rows}
    return {'workday_id': plan['id'], 'revision': revision['revision'] if revision else 0,
            'outcomes': [{'activity_id': member['id'], 'outcome': values.get(member['id'], 'unregistered')} for member in plan['content']['activities']],
            'expires_at': plan['expires_at']}


def read(request, identifier, recap=False):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        plan = workday_storage.owned(conn, owner, identifier, request)
        result = current(conn, plan)
        if recap:
            result = {'plan': workday_storage.presentation(plan), 'lifecycle': workday_lifecycle_storage.current(conn, plan),
                      'outcomes': result, 'bus': workday_bus_storage.current(conn, plan)}
        auth.session(conn, request)
        workday_storage.owned(conn, owner, identifier, request)
        return result


def receipt(conn, owner, identifier, operation_id, digest, resource, request):
    row = conn.execute('SELECT * FROM workday_' + resource + '_operations WHERE id=%s', (operation_id,)).fetchone()
    if not row:
        return None
    if row['owner'] != owner:
        draft_storage.deny()
    if row['workday_id'] != identifier or row['payload_hash'] != digest:
        raise HTTPException(409, 'Lagringsforsøket har annet innhold.')
    if not conn.execute('SELECT %s > clock_timestamp() AS live', (row['expires_at'],)).fetchone()['live']:
        raise HTTPException(410, 'Lagringsforsøket er utløpt.')
    auth.session(conn, request)
    workday_storage.owned(conn, owner, identifier, request)
    return {'operation_id': row['id'], 'result': row['result']}


def lookup(request, identifier, resource):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        metadata = conn.execute('SELECT workday_id FROM workday_' + resource + '_operations WHERE id=%s AND owner=%s', (identifier, owner)).fetchone()
        if not metadata:
            draft_storage.deny()
        workday_storage.owned(conn, owner, metadata['workday_id'], request)
        row = conn.execute('SELECT * FROM workday_' + resource + '_operations WHERE id=%s AND owner=%s', (identifier, owner)).fetchone()
        if not conn.execute('SELECT %s > clock_timestamp() AS live', (row['expires_at'],)).fetchone()['live']:
            raise HTTPException(410, 'Lagringsforsøket er utløpt.')
        auth.session(conn, request)
        workday_storage.owned(conn, owner, metadata['workday_id'], request)
        return {'operation_id': row['id'], 'result': row['result']}


def save(request, identifier, body, close=False):
    resource = 'close' if close else 'outcome'
    digest = draft_storage.fingerprint(identifier, body.model_dump(mode='json'))
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        plan = workday_storage.owned(conn, owner, identifier, request)
        previous = receipt(conn, owner, identifier, body.operation_id, digest, resource, request)
        if previous:
            return previous
        lifecycle = workday_lifecycle_storage.current(conn, plan)
        outcomes = current(conn, plan)
        if lifecycle['state'] != 'active':
            raise HTTPException(409, 'Skiftet må være startet og aktivt.')
        expected_lifecycle = body.expected_revision if close else body.expected_lifecycle_revision
        expected_outcome = body.expected_outcome_revision if close else body.expected_revision
        if lifecycle['revision'] != expected_lifecycle or outcomes['revision'] != expected_outcome:
            raise HTTPException(409, 'Lagret status er endret. Hent og gjennomgå den på nytt.')
        if conn.execute('SELECT count(*) AS n FROM workday_' + resource + '_operations WHERE owner=%s AND expires_at > clock_timestamp()', (owner,)).fetchone()['n'] >= 2000:
            raise HTTPException(429, {'code': resource + '_receipt_capacity', 'message': 'For mange lagringsforsøk. Vent til tidligere planer utløper.'})
        if close:
            ending = conn.execute('SELECT clock_timestamp() AS now').fetchone()['now']
            deadline = min(plan['expires_at'], plan['final_end'] + timedelta(days=7), ending + timedelta(days=7))
            conn.execute('UPDATE workday_lifecycles SET state=%s,ended_at=%s,revision=2 WHERE workday_id=%s', (body.action, ending, identifier))
            conn.execute('UPDATE workdays SET expires_at=%s WHERE id=%s', (deadline, identifier))
            # Operation metadata follows current retention; immutable JSON stays historical.
            for table in ['workday_operations', 'workday_start_operations', 'workday_bus_operations', 'workday_selection_operations', 'workday_outcome_operations', 'workday_close_operations']:
                conn.execute('UPDATE ' + table + ' SET expires_at=LEAST(expires_at,%s) WHERE workday_id=%s', (deadline, identifier))
            plan = {**plan, 'expires_at': deadline}
            result = LifecycleRecord(**workday_lifecycle_storage.current(conn, plan)).model_dump(mode='json')
        else:
            if str(body.activity_id) not in {member['id'] for member in plan['content']['activities']}:
                raise HTTPException(422, 'Aktiviteten tilhører ikke planen.')
            conn.execute('INSERT INTO workday_outcomes(workday_id,activity_id,outcome) VALUES(%s,%s,%s) ON CONFLICT(workday_id,activity_id) DO UPDATE SET outcome=EXCLUDED.outcome', (identifier, body.activity_id, body.outcome))
            conn.execute('INSERT INTO workday_outcome_revisions VALUES(%s,1) ON CONFLICT(workday_id) DO UPDATE SET revision=workday_outcome_revisions.revision+1', (identifier,))
            result = OutcomeRecord(**current(conn, plan)).model_dump(mode='json')
        accepted = conn.execute('INSERT INTO workday_' + resource + '_operations(id,owner,workday_id,payload_hash,result,expires_at) SELECT %s,%s,id,%s,%s,expires_at FROM workdays WHERE id=%s AND expires_at > clock_timestamp() RETURNING id',
                                (body.operation_id, owner, digest, Jsonb(result), identifier)).fetchone()
        if not accepted:
            raise HTTPException(410, 'Planen er utløpt.')
        auth.session(conn, request)
        workday_storage.owned(conn, owner, identifier, request)
        return {'operation_id': body.operation_id, 'result': result}
