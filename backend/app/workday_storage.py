"""Owner-serialized confirmation, independent snapshots and bounded retry metadata."""
from uuid import uuid4

from fastapi import HTTPException
from psycopg.types.json import Jsonb

from . import auth, draft_storage
from .private_storage import database
from .draft_domain import DraftContent
from .workday_domain import SUPPORTED_TYPES, assessment


def presentation(row):
    content = DraftContent.model_validate(row['content'])
    return {'id': row['id'], 'source_draft_id': row['source_draft_id'],
            'source_revision': row['source_revision'], 'confirmed_at': row['confirmed_at'],
            'final_end': row['final_end'], 'expires_at': row['expires_at'], 'state': 'confirmed',
            'draft': draft_storage.normalize_content(row['content']),
            'acknowledgements': row['acknowledgements'], 'classifications': row['classifications'],
            'unknowns': assessment(content, row['classifications'], row['assessment_policy_version'])['unknowns']}


def owned(conn, owner, identifier, request):
    row = conn.execute('SELECT * FROM workdays WHERE id=%s AND owner=%s FOR UPDATE', (identifier, owner)).fetchone()
    auth.session(conn, request)
    if not row:
        draft_storage.deny()
    if not conn.execute('SELECT %s > clock_timestamp() AS live', (row['expires_at'],)).fetchone()['live']:
        raise HTTPException(410, 'Planen er utløpt.')
    return row


def require_mutable(conn, plan):
    row = conn.execute('SELECT state FROM workday_lifecycles WHERE workday_id=%s', (plan['id'],)).fetchone()
    if row and row['state'] in {'ended', 'aborted'}:
        raise HTTPException(409, 'Skiftet er avsluttet. Planen er skrivebeskyttet.')


def review(request, body):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        source = draft_storage.owned(conn, owner, body.draft_id, request)
        if source['revision'] != body.expected_revision:
            raise HTTPException(409, 'Utkastet er endret. Last inn og gjennomgå den lagrede versjonen.')
        if source['confirmed']:
            raise HTTPException(409, 'Utkastet har allerede en bekreftet plan. Åpne planen.')
        count = conn.execute('SELECT count(*) AS n FROM workday_operations WHERE owner=%s AND workday_id IS NULL AND expires_at > clock_timestamp()', (owner,)).fetchone()['n']
        if count >= 200:
            raise HTTPException(429, 'For mange uavklarte bekreftelser.')
        content = DraftContent.model_validate(source['content'])
        facts = assessment(content, policy_version=3)
        if facts['expires_at'] and not conn.execute('SELECT %s > clock_timestamp() AS live', (facts['expires_at'],)).fetchone()['live']:
            facts['blockers'].append('Planens slutt + sju dager er allerede utløpt. Rett og lagre tidspunktet.')
        row = conn.execute('INSERT INTO workday_operations(id,owner,draft_id,expected_revision,expires_at,assessment_policy_version) SELECT %s,%s,id,revision,expires_at,3 FROM drafts WHERE id=%s AND expires_at > clock_timestamp() RETURNING id,expires_at',
                           (uuid4(), owner, body.draft_id)).fetchone()
        if not row:
            raise HTTPException(410, 'Utkastet er utløpt.')
        auth.session(conn, request)
        return {**facts, 'operation_id': row['id'], 'operation_expires_at': row['expires_at'],
                'draft_id': source['id'], 'revision': source['revision'], 'draft': content,
                'supported_types': list(SUPPORTED_TYPES)}


def operation(conn, owner, identifier, request):
    metadata = conn.execute('SELECT draft_id,workday_id FROM workday_operations WHERE id=%s AND owner=%s', (identifier, owner)).fetchone()
    if not metadata:
        draft_storage.deny()
    # Match maintenance's source/plan-before-operation lock ordering. Accepted
    # retries never depend on a surviving source draft.
    source = None
    plan = None
    if metadata['workday_id']:
        plan = owned(conn, owner, metadata['workday_id'], request)
    else:
        source = draft_storage.owned(conn, owner, metadata['draft_id'], request)
    row = conn.execute('SELECT * FROM workday_operations WHERE id=%s AND owner=%s FOR UPDATE', (identifier, owner)).fetchone()
    auth.session(conn, request)
    if not row:
        draft_storage.deny()
    if not conn.execute('SELECT %s > clock_timestamp() AS live', (row['expires_at'],)).fetchone()['live']:
        raise HTTPException(410, 'Bekreftelsesforsøket er utløpt.')
    return row, source, plan


def confirm(request, identifier, body):
    payload = body.model_dump(mode='json')
    payload['acknowledgements'] = sorted(payload['acknowledgements'])
    digest = draft_storage.fingerprint(identifier, payload)
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        op, source, plan = operation(conn, owner, body.operation_id, request)
        if op['draft_id'] != identifier or op['expected_revision'] != body.expected_revision:
            raise HTTPException(409, 'Bekreftelsesforsøket gjelder en annen versjon.')
        if plan:
            if op['payload_hash'] != digest:
                raise HTTPException(409, 'Bekreftelsesforsøket har andre beslutninger.')
            return presentation(plan)
        if source['revision'] != body.expected_revision:
            raise HTTPException(409, 'Utkastet er endret. Gjennomgå den lagrede versjonen på nytt.')
        content = DraftContent.model_validate(source['content'])
        decisions = {str(key): value for key, value in body.classifications.items()}
        facts = assessment(content, decisions, op['assessment_policy_version'])
        if facts['blockers'] or set(decisions) != set(facts['classifications_required']):
            raise HTTPException(422, 'Rett blokkeringene og klassifiser alle ukjente aktivitetstyper.')
        if set(body.acknowledgements) != {item['id'] for item in facts['unknowns']}:
            raise HTTPException(422, 'Alle oppførte ukjente opplysninger må gjennomgås og godtas for denne versjonen.')
        if source['confirmed'] or conn.execute('SELECT id FROM workdays WHERE source_draft_id=%s', (identifier,)).fetchone():
            raise HTTPException(409, 'Utkastet har allerede en bekreftet plan. Åpne planen.')
        auth.session(conn, request)
        row = conn.execute('INSERT INTO workdays(id,owner,source_draft_id,source_revision,final_end,expires_at,content,acknowledgements,classifications,assessment_policy_version) '
                           'SELECT %s,%s,id,revision,%s,%s,%s,%s,%s,%s FROM drafts WHERE id=%s AND owner=%s AND revision=%s '
                           'AND expires_at > clock_timestamp() AND %s > clock_timestamp() '
                           'AND EXISTS (SELECT 1 FROM workday_operations WHERE id=%s AND expires_at > clock_timestamp()) RETURNING *',
                           (uuid4(), owner, facts['final_end'], facts['expires_at'], Jsonb(content.model_dump(mode='json')),
                            Jsonb(sorted(body.acknowledgements)), Jsonb(decisions), op['assessment_policy_version'], identifier, owner, body.expected_revision,
                            facts['expires_at'], body.operation_id)).fetchone()
        if not row:
            raise HTTPException(410, 'Utkastet, forsøket eller planens frist er utløpt.')
        conn.execute('UPDATE drafts SET confirmed=true WHERE id=%s', (identifier,))
        accepted = conn.execute('UPDATE workday_operations SET workday_id=%s,payload_hash=%s,expires_at=%s WHERE id=%s '
                                'AND expires_at > clock_timestamp() AND %s > clock_timestamp() '
                                'AND EXISTS (SELECT 1 FROM drafts WHERE id=%s AND revision=%s AND expires_at > clock_timestamp()) RETURNING id',
                                (row['id'], digest, row['expires_at'], body.operation_id, row['expires_at'], identifier, body.expected_revision)).fetchone()
        if not accepted:
            raise HTTPException(410, 'Utkastet, forsøket eller planens frist er utløpt.')
        auth.session(conn, request)
        return presentation(row)


def lookup(request, identifier):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        _, _, plan = operation(conn, owner, identifier, request)
        auth.session(conn, request)
        if plan:
            owned(conn, owner, plan['id'], request)
        return {'state': 'accepted' if plan else 'pending', 'result': presentation(plan) if plan else None}


def read(request, identifier):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        plan = owned(conn, owner, identifier, request)
        auth.session(conn, request)
        owned(conn, owner, identifier, request)
        return presentation(plan)


def listing(request, cursor=None):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        rows = conn.execute("SELECT id,source_draft_id,source_revision,content->>'service_date' AS service_date,expires_at FROM workdays WHERE owner=%s AND expires_at > clock_timestamp() AND (%s::uuid IS NULL OR id > %s) ORDER BY id LIMIT 51", (owner, cursor, cursor)).fetchall()
        auth.session(conn, request)
        return {'workdays': rows[:50], 'next_cursor': rows[49]['id'] if len(rows) > 50 else None}


def deletion(conn, owner, identifier, request):
    row = conn.execute('SELECT * FROM workday_deletions WHERE id=%s AND owner=%s FOR UPDATE', (identifier, owner)).fetchone()
    auth.session(conn, request)
    if row and not conn.execute('SELECT %s > clock_timestamp() AS live', (row['expires_at'],)).fetchone()['live']:
        raise HTTPException(410, 'Slettingsforsøket er utløpt.')
    return row


def deletion_result(row):
    return {'operation_id': row['id'], 'deleted_id': row['workday_id'], 'source_revision': row['source_revision']}


def deletion_lookup(request, identifier):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        row = deletion(conn, owner, identifier, request)
        if not row:
            draft_storage.deny()
        auth.session(conn, request)
        return deletion_result(row)


def delete(request, identifier, body):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        accepted = deletion(conn, owner, body.operation_id, request)
        if accepted:
            if accepted['workday_id'] != identifier or accepted['source_revision'] != body.source_revision:
                raise HTTPException(409, 'Slettingsforsøket gjelder en annen plan eller versjon.')
            auth.session(conn, request)
            return deletion_result(accepted)
        plan = owned(conn, owner, identifier, request)
        if plan['source_revision'] != body.source_revision:
            raise HTTPException(409, 'Planversjonen stemmer ikke. Åpne planen på nytt.')
        receipt = conn.execute('INSERT INTO workday_deletions(id,owner,workday_id,source_revision,expires_at) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING RETURNING *',
                               (body.operation_id, owner, identifier, body.source_revision, plan['expires_at'])).fetchone()
        if not receipt:
            draft_storage.deny()
        auth.session(conn, request)
        # Recheck the live deadline at acceptance, after receipt insertion. A
        # failed predicate raises inside the transaction and rolls back both.
        removed = conn.execute('DELETE FROM workdays WHERE id=%s AND owner=%s AND source_revision=%s AND expires_at > clock_timestamp() RETURNING id',
                               (identifier, owner, body.source_revision)).fetchone()
        if not removed:
            raise HTTPException(410, 'Planen er utløpt.')
        if not conn.execute('SELECT %s > clock_timestamp() AS live', (plan['expires_at'],)).fetchone()['live']:
            raise HTTPException(410, 'Planen er utløpt.')
        auth.session(conn, request)
        return deletion_result(receipt)
