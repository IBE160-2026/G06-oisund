"""Plan-serialized manual start and immutable accepted-operation receipts."""
from fastapi import HTTPException
from psycopg.types.json import Jsonb
from . import auth, draft_storage, workday_storage
from .private_storage import database
from .workday_lifecycle_domain import LifecycleRecord


def current(conn, plan):
    row = conn.execute('SELECT state,started_at,revision FROM workday_lifecycles WHERE workday_id=%s', (plan['id'],)).fetchone()
    return {'workday_id': plan['id'], 'state': row['state'] if row else 'confirmed',
            'started_at': row['started_at'] if row else None, 'revision': row['revision'] if row else 0,
            'expires_at': plan['expires_at']}


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
        op = conn.execute('SELECT * FROM workday_start_operations WHERE id=%s AND owner=%s', (identifier, owner)).fetchone()
        if not op:
            draft_storage.deny()
        workday_storage.owned(conn, owner, op['workday_id'], request)
        if not conn.execute('SELECT %s > clock_timestamp() AS live', (op['expires_at'],)).fetchone()['live']:
            raise HTTPException(410, 'Lagringsforsøket er utløpt.')
        auth.session(conn, request)
        return {'operation_id': op['id'], 'result': op['result']}


def save(request, identifier, body):
    digest = draft_storage.fingerprint(identifier, body.model_dump(mode='json'))
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        plan = workday_storage.owned(conn, owner, identifier, request)
        op = conn.execute('SELECT * FROM workday_start_operations WHERE id=%s', (body.operation_id,)).fetchone()
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
        latest = current(conn, plan)
        # Different explicit attempts converge on the immutable first start.
        if body.expected_revision != latest['revision'] and not (latest['state'] == 'active' and body.expected_revision == 0):
            raise HTTPException(409, 'Skiftstatusen er endret. Last inn lagret status.')
        if conn.execute('SELECT count(*) AS n FROM workday_start_operations WHERE owner=%s AND expires_at > clock_timestamp()', (owner,)).fetchone()['n'] >= 2000:
            raise HTTPException(429, {'code': 'start_receipt_capacity', 'message': 'For mange lagringsforsøk. Vent til tidligere planer utløper.'})
        if latest['state'] == 'confirmed':
            row = conn.execute("INSERT INTO workday_lifecycles(workday_id,state,started_at,revision) SELECT id,'active',clock_timestamp(),1 FROM workdays WHERE id=%s AND expires_at > clock_timestamp() RETURNING started_at", (identifier,)).fetchone()
            if not row:
                raise HTTPException(410, 'Planen er utløpt.')
        result = LifecycleRecord(**current(conn, plan)).model_dump(mode='json')
        accepted = conn.execute('INSERT INTO workday_start_operations(id,owner,workday_id,payload_hash,result,expires_at) SELECT %s,%s,id,%s,%s,expires_at FROM workdays WHERE id=%s AND expires_at > clock_timestamp() RETURNING id',
                                (body.operation_id, owner, digest, Jsonb(result), identifier)).fetchone()
        if not accepted:
            raise HTTPException(410, 'Planen er utløpt.')
        auth.session(conn, request)
        workday_storage.owned(conn, owner, identifier, request)
        return {'operation_id': body.operation_id, 'result': result}
