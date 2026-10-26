"""Account-serialized incidents and immutable receipts independent of plans."""
from datetime import datetime, timedelta, timezone
from uuid import uuid5, NAMESPACE_URL
from fastapi import HTTPException
from psycopg.types.json import Jsonb
from . import auth, draft_storage, workday_storage
from .private_storage import database
from .workday_notice_domain import NoticeRecord


def record(row, plan=None):
    return {key: row[key] for key in NoticeRecord.model_fields}


def member(conn, owner, notice_id):
    row = conn.execute('SELECT * FROM workday_notices WHERE id=%s AND owner=%s FOR UPDATE', (notice_id, owner)).fetchone()
    if not row:
        draft_storage.deny()
    if not conn.execute('SELECT %s>clock_timestamp() AS live', (row['expires_at'],)).fetchone()['live']:
        raise HTTPException(410, 'Avvikets lagringstid er utløpt.')
    return row


def read(request, identifier=None, notice_id=None, cursor=None):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        if identifier:
            workday_storage.owned(conn, owner, identifier, request)
        if notice_id:
            result = record(member(conn, owner, notice_id))
        else:
            listed_at = conn.execute('SELECT clock_timestamp() AS now').fetchone()['now']
            rows = conn.execute('SELECT * FROM workday_notices WHERE owner=%s AND expires_at>%s AND (%s::uuid IS NULL OR id>%s) ORDER BY id LIMIT 51', (owner, listed_at, cursor, cursor)).fetchall()
            result = {'server_now': listed_at, 'notices': [record(row) for row in rows[:50]], 'next_cursor': rows[49]['id'] if len(rows)>50 else None}
            if identifier:
                plan = workday_storage.owned(conn, owner, identifier, request)
                result = {k: v for k, v in result.items() if k != 'server_now'} | {'workday_id': identifier, 'expires_at': plan['expires_at']}
        auth.session(conn, request)
        return result


def operation(conn, owner, identifier, request, digest=None):
    row = conn.execute('SELECT * FROM account_notice_operations WHERE id=%s', (identifier,)).fetchone()
    legacy = False
    if not row:
        row = conn.execute('SELECT * FROM workday_notice_operations WHERE id=%s', (identifier,)).fetchone()
        legacy = True
    if not row or row['owner'] != owner:
        draft_storage.deny()
    if not conn.execute('SELECT %s>clock_timestamp() AS live', (row['expires_at'],)).fetchone()['live']:
        raise HTTPException(410, 'Lagringsforsøket er utløpt.')
    member(conn, owner, row['result']['id'])
    if digest is not None and (legacy or row['payload_hash'] != digest):
        raise HTTPException(409, 'Lagringsforsøket har annet innhold eller tidligere versjon. Kontroller originalforsøket.')
    auth.session(conn, request)
    member(conn, owner, row['result']['id'])
    if not conn.execute('SELECT %s>clock_timestamp() AS live', (row['expires_at'],)).fetchone()['live']:
        raise HTTPException(410, 'Lagringsforsøket er utløpt.')
    return {'operation_id': row['id'], 'result': row['result']}


def lookup(request, identifier):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        return operation(conn, owner, identifier, request)


def reader(request, identifier, line=None, calendar_date=None):
    from .notice_reader_domain import project
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        plan = workday_storage.owned(conn, owner, identifier, request)
        # Migration preserves incidents formerly bounded per workday. Aggregate
        # discovery must include every retained row, even above the new-create cap.
        rows = conn.execute('SELECT * FROM workday_notices WHERE owner=%s AND expires_at>clock_timestamp() ORDER BY id', (owner,)).fetchall()
        result = project(plan, rows, line, calendar_date)
        auth.session(conn, request)
        workday_storage.owned(conn, owner, identifier, request)
        return result


def save(request, identifier, body, notice_id=None, action='save'):
    digest = draft_storage.fingerprint('account-notices', {'action': action, 'notice_id': str(notice_id) if notice_id else None, **body.model_dump(mode='json')})
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        if identifier is not None:
            previous = conn.execute('SELECT * FROM workday_notice_operations WHERE id=%s', (body.operation_id,)).fetchone()
            if previous:
                if previous['owner'] != owner:
                    draft_storage.deny()
                legacy_payload = body.model_dump(mode='json')
                if 'content' in legacy_payload:
                    for key, default in [('summary', None), ('description', None), ('source_note', None), ('line_scope', 'selected')]:
                        if legacy_payload['content'][key] == default:
                            del legacy_payload['content'][key]
                legacy_digest = draft_storage.fingerprint(identifier, {'action': action, 'notice_id': str(notice_id) if notice_id else None, **legacy_payload})
                if previous['payload_hash'] != legacy_digest or previous['result']['workday_id'] != str(identifier):
                    raise HTTPException(409, 'Lagringsforsøket har annet innhold.')
                return operation(conn, owner, body.operation_id, request)
            raise HTTPException(409, 'Avvik er nå kontofelles. Hent registeret og gjennomgå forslaget på nytt.')
        if conn.execute('SELECT 1 FROM account_notice_operations WHERE id=%s UNION ALL SELECT 1 FROM workday_notice_operations WHERE id=%s', (body.operation_id, body.operation_id)).fetchone():
            return operation(conn, owner, body.operation_id, request, digest)
        row = member(conn, owner, notice_id) if notice_id else None
        now = conn.execute('SELECT clock_timestamp() AS now').fetchone()['now']
        if row and (row['status'] != 'registered' or row['valid_until'] is not None and row['valid_until'] <= now):
            raise HTTPException(409, 'Avviket er utløpt eller avsluttet manuelt og er skrivebeskyttet.')
        if body.expected_revision != (row['revision'] if row else 0):
            raise HTTPException(409, 'Lagret avvik er endret. Hent og gjennomgå på nytt.')
        if action != 'end' and conn.execute('SELECT count(*) AS n FROM account_notice_operations WHERE owner=%s AND expires_at>clock_timestamp()', (owner,)).fetchone()['n']>=2000:
            raise HTTPException(429, {'code': 'notice_receipt_capacity', 'message': 'For mange lagringsforsøk. Vent til tidligere avvik utløper.'})
        if action == 'save':
            values = body.content
            if not values.valid_until or datetime.fromisoformat(values.valid_until).astimezone(timezone.utc)<=now:
                raise HTTPException(422, 'Oppgi en fremtidig sluttdato for avviket.')
            try:
                deadline = datetime.fromisoformat(values.valid_until) + timedelta(days=7)
            except OverflowError:
                raise HTTPException(422, 'Sluttdatoen gir lagringstid utenfor støttet kalender.') from None
            fields = (values.title, Jsonb(values.line_tags), values.summary, values.description, values.source_note, values.line_scope, values.source_url, values.source_updated_at, values.valid_from, values.valid_until)
            if row is None:
                if conn.execute('SELECT count(*) AS n FROM workday_notices WHERE owner=%s AND expires_at>clock_timestamp()', (owner,)).fetchone()['n']>=200:
                    raise HTTPException(429, {'code': 'notice_capacity', 'message': 'Registeret har allerede 200 avvik.'})
                notice_id = uuid5(NAMESPACE_URL, 'ibe160:account-notice:'+str(owner)+':'+str(body.operation_id))
                conn.execute("INSERT INTO workday_notices(id,owner,revision,title,line_tags,summary,description,source_note,line_scope,source_url,source_updated_at,valid_from,valid_until,status,entered_at,edited_at,expires_at) VALUES(%s,%s,1,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'registered',%s,%s,%s)", (notice_id, owner, *fields, now, now, deadline))
            else:
                conn.execute('UPDATE workday_notices SET title=%s,line_tags=%s,summary=%s,description=%s,source_note=%s,line_scope=%s,source_url=%s,source_updated_at=%s,valid_from=%s,valid_until=%s,revision=revision+1,edited_at=%s,expires_at=%s WHERE id=%s', (*fields, now, deadline, notice_id))
        elif action == 'check':
            conn.execute('UPDATE workday_notices SET checked_at=%s,checked_revision=revision+1,revision=revision+1 WHERE id=%s', (now, notice_id))
        elif action == 'end':
            conn.execute("UPDATE workday_notices SET status='ended_manually',ended_at=%s,revision=revision+1,edited_at=%s,expires_at=%s WHERE id=%s", (now, now, min(row['expires_at'], now+timedelta(days=7)), notice_id))
        # Check after the write too: waiting or work within this transaction may
        # have crossed the original deadline. Raising rolls back every effect.
        if row and not conn.execute('SELECT %s>clock_timestamp() AS live', (row['valid_until'] or row['expires_at'],)).fetchone()['live']:
            raise HTTPException(409, 'Avviket er utløpt og er skrivebeskyttet.')
        result = NoticeRecord(**record(member(conn, owner, notice_id))).model_dump(mode='json')
        conn.execute('INSERT INTO account_notice_operations(id,owner,notice_id,payload_hash,result,expires_at) VALUES(%s,%s,%s,%s,%s,%s)', (body.operation_id, owner, notice_id, digest, Jsonb(result), result['expires_at']))
        conn.execute('UPDATE account_notice_operations SET expires_at=%s WHERE notice_id=%s', (result['expires_at'], notice_id))
        conn.execute("UPDATE workday_notice_operations SET expires_at=%s WHERE owner=%s AND result->>'id'=%s", (result['expires_at'], owner, str(notice_id)))
        auth.session(conn, request)
        member(conn, owner, notice_id)
        if row and not conn.execute('SELECT %s>clock_timestamp() AS live', (row['valid_until'] or row['expires_at'],)).fetchone()['live']:
            raise HTTPException(409, 'Avviket er utløpt og er skrivebeskyttet.')
        return {'operation_id': body.operation_id, 'result': result}
