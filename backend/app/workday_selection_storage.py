"""Plan-serialized selection revisions and immutable accepted-operation receipts."""
from fastapi import HTTPException
from psycopg.types.json import Jsonb
from . import auth, draft_storage, workday_storage
from .private_storage import database
from .workday_selection_domain import SelectionRecord


def current(conn, plan):
    bus = conn.execute('SELECT activity_id,revision FROM workday_selections WHERE workday_id=%s', (plan['id'],)).fetchone()
    value = bus['activity_id'] if bus else None
    return {'workday_id': plan['id'], 'activity_id': value,
            'revision': bus['revision'] if bus else 0, 'expires_at': plan['expires_at']}


def read(request, identifier):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        plan = workday_storage.owned(conn, owner, identifier, request)
        result = current(conn, plan)
        auth.session(conn, request)
        workday_storage.owned(conn, owner, identifier, request)
        return result


def lookup(request, identifier):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        op = conn.execute('SELECT * FROM workday_selection_operations WHERE id=%s AND owner=%s', (identifier, owner)).fetchone()
        if not op:
            draft_storage.deny()
        workday_storage.owned(conn, owner, op['workday_id'], request)
        if not conn.execute('SELECT %s > clock_timestamp() AS live', (op['expires_at'],)).fetchone()['live']:
            raise HTTPException(410, 'Lagringsforsøket er utløpt.')
        auth.session(conn, request)
        workday_storage.owned(conn, owner, op['workday_id'], request)
        return {'operation_id': op['id'], 'result': op['result']}


def save(request, identifier, body):
    digest = draft_storage.fingerprint(identifier, body.model_dump(mode='json'))
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        plan = workday_storage.owned(conn, owner, identifier, request)
        op = conn.execute('SELECT * FROM workday_selection_operations WHERE id=%s', (body.operation_id,)).fetchone()
        if op:
            if op['owner'] != owner:
                draft_storage.deny()
            if op['workday_id'] != identifier or op['payload_hash'] != digest:
                raise HTTPException(409, 'Lagringsforsøket har annet innhold.')
            if not conn.execute('SELECT %s > clock_timestamp() AS live', (op['expires_at'],)).fetchone()['live']:
                raise HTTPException(410, 'Lagringsforsøket er utløpt.')
            auth.session(conn, request)
            workday_storage.owned(conn, owner, identifier, request)
            return {'operation_id': op['id'], 'result': op['result']}
        workday_storage.require_mutable(conn, plan)
        if current(conn, plan)['revision'] != body.expected_revision:
            raise HTTPException(409, 'Aktivitetsvalget er endret. Sammenlign med lagret verdi.')
        if conn.execute('SELECT count(*) AS n FROM workday_selection_operations WHERE owner=%s AND expires_at > clock_timestamp()', (owner,)).fetchone()['n'] >= 2000:
            raise HTTPException(429, {'code': 'selection_receipt_capacity', 'message': 'For mange lagringsforsøk. Vent til tidligere planer utløper.'})
        value = body.activity_id
        if str(value) not in {a['id'] for a in plan['content']['activities']}:
            raise HTTPException(422, 'Aktiviteten tilhører ikke planen.')
        row = conn.execute('INSERT INTO workday_selections(workday_id,activity_id,revision) SELECT id,%s,1 FROM workdays WHERE id=%s AND expires_at > clock_timestamp() '
                           'ON CONFLICT(workday_id) DO UPDATE SET activity_id=EXCLUDED.activity_id,revision=workday_selections.revision+1 RETURNING revision', (value, identifier)).fetchone()
        if not row:
            raise HTTPException(410, 'Planen er utløpt.')
        result = SelectionRecord(workday_id=identifier, activity_id=value, revision=row['revision'], expires_at=plan['expires_at']).model_dump(mode='json')
        accepted = conn.execute('INSERT INTO workday_selection_operations(id,owner,workday_id,payload_hash,result,expires_at) SELECT %s,%s,id,%s,%s,expires_at FROM workdays WHERE id=%s AND expires_at > clock_timestamp() RETURNING id',
                                (body.operation_id, owner, digest, Jsonb(result), identifier)).fetchone()
        if not accepted:
            raise HTTPException(410, 'Planen er utløpt.')
        auth.session(conn, request)
        workday_storage.owned(conn, owner, identifier, request)
        return {'operation_id': body.operation_id, 'result': result}
