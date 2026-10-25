"""Parent-serialized notice writes and immutable bounded command receipts."""
from uuid import uuid5, NAMESPACE_URL
from fastapi import HTTPException
from psycopg.types.json import Jsonb
from . import auth, draft_storage, workday_storage, workday_lifecycle_storage, workday_outcome_storage
from .private_storage import database
from .workday_notice_domain import NoticeRecord


def record(row, plan):
    return {**row, 'expires_at': plan['expires_at']}


def member(conn, identifier, notice_id):
    row = conn.execute('SELECT * FROM workday_notices WHERE id=%s AND workday_id=%s', (notice_id, identifier)).fetchone()
    if not row:
        draft_storage.deny()
    return row


def read(request, identifier, notice_id=None, cursor=None):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        plan = workday_storage.owned(conn, owner, identifier, request)
        if notice_id:
            result = record(member(conn, identifier, notice_id), plan)
        else:
            rows = conn.execute('SELECT * FROM workday_notices WHERE workday_id=%s AND (%s::uuid IS NULL OR id>%s) ORDER BY id LIMIT 51', (identifier, cursor, cursor)).fetchall()
            result = {'workday_id': identifier, 'expires_at': plan['expires_at'], 'notices': [record(row, plan) for row in rows[:50]], 'next_cursor': rows[49]['id'] if len(rows) > 50 else None}
        auth.session(conn, request)
        workday_storage.owned(conn, owner, identifier, request)
        return result


def lookup(request, identifier):
    return workday_outcome_storage.lookup(request, identifier, 'notice')


def save(request, identifier, body, notice_id=None, action='save'):
    # Include action/target as well as the entire normalized body in identity.
    payload = body.model_dump(mode='json')
    # Preserve deployed fingerprints for content with additive defaults.
    if 'content' in payload:
        for key, default in [('summary', None), ('description', None), ('source_note', None), ('line_scope', 'selected')]:
            if payload['content'][key] == default:
                del payload['content'][key]
    digest = draft_storage.fingerprint(identifier, {'action': action, 'notice_id': str(notice_id) if notice_id else None, **payload})
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        plan = workday_storage.owned(conn, owner, identifier, request)
        previous = workday_outcome_storage.receipt(conn, owner, identifier, body.operation_id, digest, 'notice', request)
        if previous:
            return previous
        workday_storage.require_mutable(conn, plan)
        lifecycle = workday_lifecycle_storage.current(conn, plan)
        row = member(conn, identifier, notice_id) if notice_id else None
        if body.expected_lifecycle_revision != lifecycle['revision'] or body.expected_revision != (row['revision'] if row else 0):
            raise HTTPException(409, 'Lagret avvik eller skiftstatus er endret. Hent og gjennomgå på nytt.')
        if conn.execute('SELECT count(*) AS n FROM workday_notice_operations WHERE owner=%s AND expires_at>clock_timestamp()', (owner,)).fetchone()['n'] >= 2000:
            raise HTTPException(429, {'code': 'notice_receipt_capacity', 'message': 'For mange lagringsforsøk. Vent til tidligere planer utløper.'})
        now = conn.execute('SELECT clock_timestamp() AS now').fetchone()['now']
        if row is None:
            if conn.execute('SELECT count(*) AS n FROM workday_notices WHERE workday_id=%s', (identifier,)).fetchone()['n'] >= 200:
                raise HTTPException(429, {'code': 'notice_capacity', 'message': 'Dagen har allerede 200 avvik.'})
            notice_id = uuid5(NAMESPACE_URL, 'ibe160:notice:' + str(body.operation_id))
            values = body.content
            conn.execute('INSERT INTO workday_notices(id,workday_id,revision,title,line_tags,summary,description,source_note,line_scope,source_url,source_updated_at,valid_from,valid_until,status,entered_at,edited_at) VALUES(%s,%s,1,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\'registered\',%s,%s)', (notice_id, identifier, values.title, Jsonb(values.line_tags), values.summary, values.description, values.source_note, values.line_scope, values.source_url, values.source_updated_at, values.valid_from, values.valid_until, now, now))
        elif action == 'save':
            values = body.content
            conn.execute('UPDATE workday_notices SET title=%s,line_tags=%s,summary=%s,description=%s,source_note=%s,line_scope=%s,source_url=%s,source_updated_at=%s,valid_from=%s,valid_until=%s,revision=revision+1,edited_at=%s WHERE id=%s', (values.title, Jsonb(values.line_tags), values.summary, values.description, values.source_note, values.line_scope, values.source_url, values.source_updated_at, values.valid_from, values.valid_until, now, notice_id))
        elif action == 'check':
            conn.execute('UPDATE workday_notices SET checked_at=%s,checked_revision=revision+1,revision=revision+1 WHERE id=%s', (now, notice_id))
        elif action == 'end':
            if row['status'] == 'ended_manually':
                raise HTTPException(409, 'Avviket er allerede avsluttet manuelt.')
            conn.execute("UPDATE workday_notices SET status='ended_manually',revision=revision+1,edited_at=%s WHERE id=%s", (now, notice_id))
        result = NoticeRecord(**record(member(conn, identifier, notice_id), plan)).model_dump(mode='json')
        accepted = conn.execute('INSERT INTO workday_notice_operations(id,owner,workday_id,payload_hash,result,expires_at) SELECT %s,%s,id,%s,%s,expires_at FROM workdays WHERE id=%s AND expires_at>clock_timestamp() RETURNING id', (body.operation_id, owner, digest, Jsonb(result), identifier)).fetchone()
        if not accepted:
            raise HTTPException(410, 'Planen er utløpt.')
        auth.session(conn, request)
        workday_storage.owned(conn, owner, identifier, request)
        return {'operation_id': body.operation_id, 'result': result}
