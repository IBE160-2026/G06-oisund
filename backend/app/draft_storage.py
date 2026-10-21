"""Authorized transactional revisions and expiring idempotency acknowledgements."""
import hashlib
import json
from uuid import uuid4

from fastapi import HTTPException
from psycopg.types.json import Jsonb

from . import auth
from .draft_domain import DraftContent
from .private_storage import database


def authorized(conn, request):
    owner = auth.session(conn, request)['owner']
    conn.execute('SELECT id FROM accounts WHERE id=%s FOR UPDATE', (owner,))
    auth.session(conn, request)
    return owner


def deny():
    raise HTTPException(404, 'Tilgangen ble avvist.')


def owned(conn, owner, identifier, request):
    row = conn.execute('SELECT *, expires_at > clock_timestamp() AS live FROM drafts WHERE id=%s AND owner=%s FOR UPDATE',
                       (identifier, owner)).fetchone()
    auth.session(conn, request)
    if not row:
        deny()
    if not conn.execute('SELECT %s > clock_timestamp() AS live', (row['expires_at'],)).fetchone()['live']:
        raise HTTPException(410, 'Utkastet er utløpt og kan ikke åpnes igjen.')
    return row


def presentation(row):
    return {'id': str(row['id']), 'created_at': row['created_at'].isoformat(),
            'expires_at': row['expires_at'].isoformat(), 'revision': row['revision'], 'draft': normalize_content(row['content'])}


def normalize_content(content):
    return DraftContent.model_validate(content).model_dump(mode='json')


def normalize_result(result):
    return {**result, 'draft': normalize_content(result['draft'])}


def fingerprint(identifier, payload):
    return hashlib.sha256(json.dumps({'target': str(identifier), 'body': payload}, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def listing(request):
    with database() as conn:
        owner = authorized(conn, request)
        rows = conn.execute('SELECT id,created_at,expires_at,revision,content->>\'service_date\' AS service_date '
                            'FROM drafts WHERE owner=%s AND expires_at > clock_timestamp() ORDER BY created_at DESC LIMIT 200', (owner,)).fetchall()
        auth.session(conn, request)
        return {'drafts': rows}


def read(request, identifier):
    with database() as conn:
        owner = authorized(conn, request)
        row = owned(conn, owner, identifier, request)
        auth.session(conn, request)
        return presentation(row)


def issue(request, identifier):
    with database() as conn:
        owner = authorized(conn, request)
        draft = owned(conn, owner, identifier, request) if identifier else None
        auth.session(conn, request)
        # Bound unused operation admission per owner; expired work cannot be resurrected.
        count = conn.execute('SELECT count(*) AS n FROM draft_operations WHERE owner=%s AND expires_at > clock_timestamp() AND result IS NULL', (owner,)).fetchone()['n']
        if count >= 200:
            raise HTTPException(429, 'For mange uavklarte lagringer.')
        row = conn.execute("INSERT INTO draft_operations(id,owner,draft_id,expires_at) VALUES (%s,%s,%s,COALESCE(%s,statement_timestamp()+interval '7 days')) RETURNING id,expires_at",
                           (uuid4(), owner, identifier, draft['expires_at'] if draft else None)).fetchone()
        auth.session(conn, request)
        return {'operation_id': row['id'], 'expires_at': row['expires_at']}


def operation(conn, owner, identifier, request):
    # Follow cleanup's draft-before-operation lock order, including accepted creates.
    metadata = conn.execute('SELECT draft_id FROM draft_operations WHERE id=%s AND owner=%s', (identifier, owner)).fetchone()
    if not metadata:
        deny()
    if metadata['draft_id']:
        owned(conn, owner, metadata['draft_id'], request)
    row = conn.execute('SELECT * FROM draft_operations WHERE id=%s AND owner=%s FOR UPDATE', (identifier, owner)).fetchone()
    auth.session(conn, request)
    if not row:
        deny()
    if not conn.execute('SELECT %s > clock_timestamp() AS live', (row['expires_at'],)).fetchone()['live']:
        raise HTTPException(410, 'Lagringsforsøket er utløpt. Det kan ikke gjenopprettes.')
    return row


def lookup(request, identifier):
    with database() as conn:
        owner = authorized(conn, request)
        row = operation(conn, owner, identifier, request)
        auth.session(conn, request)
        return {'state': 'accepted' if row['result'] else 'pending', 'result': normalize_result(row['result']) if row['result'] else None}


def save(request, identifier, body):
    payload = body.model_dump(mode='json')
    payload['draft'] = normalize_content(payload['draft'])
    digest = fingerprint(identifier, payload)
    with database() as conn:
        owner = authorized(conn, request)
        # Lock drafts before operations consistently, including lookup paths.
        # A single owner lock also serializes requests using different sessions.
        conn.execute('SELECT id FROM accounts WHERE id=%s FOR UPDATE', (owner,))
        existing = owned(conn, owner, identifier, request) if identifier else None
        op = operation(conn, owner, body.operation_id, request)
        auth.session(conn, request)
        if op['result']:
            result = normalize_result(op['result'])
            # Older snapshots/fingerprints retain the previously editable value.
            # Compare normalized accepted facts without rewriting stored work.
            accepted_payload = {'operation_id': str(body.operation_id), 'expected_revision': result['revision'] - 1, 'draft': result['draft']}
            accepted_target = op['draft_id'] if result['revision'] > 1 else None
            if op['payload_hash'] != digest and fingerprint(accepted_target, accepted_payload) != digest:
                raise HTTPException(409, 'Lagringsforsøket har annet innhold. Behold dine lokale endringer.')
            return result
        if op['draft_id'] != identifier:
            deny()
        if (existing['revision'] if existing else 0) != body.expected_revision:
            raise HTTPException(409, 'Utkastet er endret. Sammenlign med lagret versjon før du fortsetter.')
        content = body.draft.model_dump(mode='json')
        if existing:
            row = conn.execute('UPDATE drafts SET content=%s,revision=revision+1 WHERE id=%s AND expires_at > clock_timestamp() RETURNING *', (Jsonb(content), identifier)).fetchone()
            if not row:
                raise HTTPException(410, 'Utkastet er utløpt.')
        else:
            row = conn.execute('INSERT INTO drafts(id,owner,revision,content) VALUES (%s,%s,1,%s) RETURNING *', (uuid4(), owner, Jsonb(content))).fetchone()
        result = presentation(row)
        conn.execute('UPDATE draft_operations SET draft_id=%s,expires_at=%s,payload_hash=%s,result=%s WHERE id=%s',
                     (row['id'], row['expires_at'], digest, Jsonb(result), body.operation_id))
        auth.session(conn, request)
        return result


def deletion(conn, owner, identifier, request):
    row = conn.execute('SELECT * FROM draft_deletions WHERE id=%s AND owner=%s FOR UPDATE', (identifier, owner)).fetchone()
    auth.session(conn, request)
    if row and not conn.execute('SELECT %s > clock_timestamp() AS live', (row['expires_at'],)).fetchone()['live']:
        raise HTTPException(410, 'Slettingsforsøket er utløpt.')
    return row


def deletion_lookup(request, operation_id):
    with database() as conn:
        owner = authorized(conn, request)
        row = deletion(conn, owner, operation_id, request)
        if not row:
            deny()
        return {'deleted_id': row['draft_id']}


def delete(request, identifier, body):
    with database() as conn:
        owner = authorized(conn, request)
        accepted = deletion(conn, owner, body.operation_id, request)
        if accepted:
            if accepted['draft_id'] != identifier or accepted['expected_revision'] != body.expected_revision:
                raise HTTPException(409, 'Slettingsforsøket har annet innhold.')
            return {'deleted_id': identifier}
        row = owned(conn, owner, identifier, request)
        if row['revision'] != body.expected_revision:
            raise HTTPException(409, 'Utkastet er endret. Sammenlign med lagret versjon før sletting.')
        inserted = conn.execute('INSERT INTO draft_deletions VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING RETURNING id',
                                (body.operation_id, owner, identifier, body.expected_revision, row['expires_at'])).fetchone()
        auth.session(conn, request)
        if not inserted:
            deny()
        if not conn.execute('DELETE FROM drafts WHERE id=%s AND expires_at > clock_timestamp() RETURNING id', (identifier,)).fetchone():
            raise HTTPException(410, 'Utkastet er utløpt.')
        auth.session(conn, request)
        return {'deleted_id': identifier}
