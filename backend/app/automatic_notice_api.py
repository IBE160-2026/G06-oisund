"""Private day projection and explicit, reversible automatic-notice decisions."""

from collections import Counter
from datetime import timedelta
import os
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import Field, field_validator, model_validator
from psycopg.types.json import Jsonb

from . import auth, draft_storage, workday_storage
from .automatic_notice_ingestion import CYCLE_SECONDS
from .automatic_notice_relevance import BINDING, PILOT_STOP_PLACE, city_scope, classify, operational_status, verified_pilot_stop_scope
from .automatic_notice_source import MAX_ID, revision, valid_situation
from .draft_domain import StrictModel
from .private_storage import database


router = APIRouter()
PLAN_PATH = '/workdays/{identifier}/automatic-notices'
PAGE_LIMIT = 10
MAX_DECISIONS = 200
MAX_OPERATIONS = 1000
FRESHNESS = timedelta(minutes=15)
RETENTION = timedelta(days=7)
PUBLIC_ITEM_COLUMNS = 'revision,content,first_seen,last_seen,fetched_at,response_at,last_complete_generation'
VISIBLE_IDENTITIES = ('SELECT item.situation FROM automatic_notice_identities AS item WHERE item.participant=%s '
                      'AND (item.last_complete_generation=%s OR item.last_seen>%s) '
                      'AND EXISTS (SELECT 1 FROM automatic_notice_sources AS source WHERE source.participant=item.participant '
                      'AND source.situation=item.situation AND source.current_revision)')


class ReviewCommand(StrictModel):
    operation_id: UUID
    situation: str = Field(max_length=MAX_ID, strict=True)
    expected_revision: int = Field(ge=0, strict=True)
    expected_plan_revision: int = Field(gt=0, strict=True)
    expected_lifecycle_revision: int = Field(ge=0, le=2, strict=True)
    expected_source_basis: str = Field(pattern=r'^[0-9a-f]{64}$')
    action: Literal['associate', 'day-context', 'dismiss', 'unresolved']
    activity_id: UUID | None = None
    reason: str | None = Field(default=None, max_length=300)
    manual_notice_id: UUID | None = None

    @field_validator('situation')
    @classmethod
    def canonical_situation(cls, value):
        if not valid_situation(value):
            raise ValueError('A bounded source identity is required')
        return value

    @model_validator(mode='after')
    def action_fields(self):
        if (self.action == 'associate') != (self.activity_id is not None):
            raise ValueError('An explicit activity is required for association')
        if (self.action == 'dismiss') != (self.reason is not None):
            raise ValueError('A dismissal requires a reason')
        if self.reason is not None and (not self.reason.strip() or any(ord(char) < 32 for char in self.reason)):
            raise ValueError('A plain-text reason is required')
        return self


def clock(conn):
    return conn.execute('SELECT clock_timestamp() AS ts').fetchone()['ts']


def access(conn, identifier, request):
    owner = draft_storage.authorized(conn, request)
    return owner, workday_storage.owned(conn, owner, identifier, request)


def lifecycle(conn, identifier):
    return conn.execute('SELECT state,revision FROM workday_lifecycles WHERE workday_id=%s', (identifier,)).fetchone() or {
        'state': 'unstarted', 'revision': 0}


def health(conn, now):
    row = conn.execute('SELECT status,attempt_at,result_at,generation,baseline_at,synchronized_at,baseline_count,'
                       'response_at,attempt_pages,attempt_count,failure FROM automatic_notice_feed FOR SHARE').fetchone()
    if row['status'] == 'collecting' and row['attempt_at'] + timedelta(seconds=CYCLE_SECONDS) <= now:
        row.update(status='partial' if row['attempt_pages'] else 'unavailable', failure='interrupted')
    return row | {'old': bool(row['synchronized_at'] and now - row['synchronized_at'] >= FRESHNESS),
                  'provider': 'Entur', 'dataset': 'TRO', 'stream': 'SIRI-SX',
                  'evidence_kind': 'synthetic' if os.getenv('PRIVATE_TEST_PROJECT') == 'ibe160-private-tests' else 'provider'}


def public_item(conn, situation, feed, now):
    key = ('TRO', situation, feed['generation'], now - RETENTION)
    identity = conn.execute('SELECT last_seen,last_complete_generation FROM automatic_notice_identities '
                            'WHERE participant=%s AND situation=%s AND (last_complete_generation=%s OR last_seen>%s)',
                            key).fetchone()
    if identity is None:
        return None
    rows = conn.execute(f'SELECT {PUBLIC_ITEM_COLUMNS},current_revision,conflicting FROM automatic_notice_sources '
                        'WHERE participant=%s AND situation=%s AND (current_revision '
                        'OR (conflicting AND (last_complete_generation=%s OR last_seen>%s))) '
                        'ORDER BY current_revision DESC,last_seen DESC,revision LIMIT 5', key).fetchall()
    if not rows or not rows[0]['current_revision']:
        return None
    source, *conflicts = rows
    basis = conn.execute('SELECT revision FROM automatic_notice_sources WHERE participant=%s AND situation=%s '
                         'AND conflicting AND (last_complete_generation=%s OR last_seen>%s) ORDER BY revision', key).fetchall()
    generation = source.pop('last_complete_generation')
    if feed['status'] != 'complete':
        attempt = feed['attempt_at'] or now
        observation = ('seen-partial' if source['last_seen'] >= attempt else
                       'other-revision-seen-partial' if identity['last_seen'] >= attempt else 'unknown')
    else:
        observation = ('seen' if generation == feed['generation'] else
                       'other-revision-seen' if identity['last_complete_generation'] == feed['generation'] else 'not-seen')
    basis_items = [source['revision'], *[item['revision'] for item in basis]]
    if verified_pilot_stop_scope(source['content']):
        basis_items.append('verified-pilot-stop-scope')
    return source | {
        'basis': revision(basis_items),
        'observation': observation, 'complete_generation': generation, 'conflict_count': len(basis),
        'identity_last_seen': identity['last_seen'],
        'conflicts': [{key: row[key] for key in ('revision', 'content', 'response_at', 'last_seen')} for row in conflicts],
    }


def city_stops(conn):
    rows = conn.execute(
        "SELECT DISTINCT q.quay_id, item->>'stop_place_id' AS stop_place_id "
        "FROM public_quay_versions q "
        "CROSS JOIN LATERAL jsonb_array_elements(COALESCE(q.record->'versions',jsonb_build_array(q.record))) item "
        "WHERE q.revision IN (SELECT DISTINCT provenance->>'nsr_revision' FROM public_route_days)"
    ).fetchall()
    return {PILOT_STOP_PLACE, *(row['quay_id'] for row in rows), *(row['stop_place_id'] for row in rows if row['stop_place_id'])}


def operational_sources(conn, feed, now):
    stops = city_stops(conn)
    rows = conn.execute(
        "SELECT i.situation,jsonb_build_object('progress',s.content->'progress','windows',s.content->'windows',"
        "'affects',s.content->'affects') AS content FROM automatic_notice_identities i "
        "JOIN automatic_notice_sources s USING(participant,situation) "
        "WHERE i.participant='TRO' AND s.current_revision "
        "AND (i.last_complete_generation=%s OR (%s <> 'complete' "
        "AND i.last_seen > GREATEST(COALESCE(%s,'-infinity'::timestamptz), %s))) "
        "ORDER BY i.situation",
        (feed['generation'], feed['status'], feed['synchronized_at'], now - RETENTION),
    ).fetchall()
    return [(row['situation'], state) for row in rows
            if (state := operational_status(row['content'], now)) and city_scope(row['content'], stops)]


def page_sources(conn, feed, now, cursor):
    matches = operational_sources(conn, feed, now)
    remaining = [(key, status) for key, status in matches if cursor is None or key > cursor]
    return remaining[:PAGE_LIMIT], len(matches), remaining[PAGE_LIMIT - 1][0] if len(remaining) > PAGE_LIMIT else None


@router.get('/operational-notices')
def operational_notices(request: Request, cursor: Annotated[str | None, Query(max_length=MAX_ID)] = None):
    if cursor is not None and not valid_situation(cursor):
        raise HTTPException(422, 'Kontroller sidegrunnlaget.')
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        now = clock(conn)
        feed = health(conn, now)
        page, total, next_cursor = page_sources(conn, feed, now, cursor)
        rows = conn.execute(
            "SELECT id,title,summary,description,line_tags,line_scope,valid_from,valid_until,checked_at,source_note "
            "FROM workday_notices WHERE owner=%s AND status='registered' "
            "AND valid_until>%s AND expires_at>%s ORDER BY valid_until,id",
            (owner, now, now),
        ).fetchall() if cursor is None else []
        entries = []
        for key, state in page:
            source = public_item(conn, key, feed, now)
            entries.append({'id': key, 'status': state, 'content': source['content'], 'observation': source['observation']})
        auth.session(conn, request)
        return {'server_now': now, 'manual': rows, 'automatic': entries, 'feed': feed['status'],
                'old': feed['old'], 'total': total, 'next_cursor': next_cursor}


def manual(conn, owner, identifier):
    if identifier is None:
        return None
    return conn.execute('SELECT id,title,summary,description,source_note,source_url,source_updated_at,valid_from,valid_until,'
                        'status,checked_at,ended_at,revision FROM workday_notices '
                        "WHERE id=%s AND owner=%s AND status='registered' AND valid_until>clock_timestamp() "
                        'AND expires_at>clock_timestamp()', (identifier, owner)).fetchone()


@router.get(PLAN_PATH)
def projection(identifier: UUID, request: Request, cursor: Annotated[str | None, Query(max_length=MAX_ID)] = None,
               history: bool = False):
    if cursor is not None and not valid_situation(cursor):
        raise HTTPException(422, 'Kontroller sidegrunnlaget.')
    with database() as conn:
        owner, plan = access(conn, identifier, request)
        now = clock(conn)
        feed = health(conn, now)
        stage = lifecycle(conn, identifier)
        reviews = {item['situation']: item for item in conn.execute('SELECT situation,revision,decision '
                   'FROM automatic_notice_reviews WHERE workday_id=%s AND owner=%s', (identifier, owner)).fetchall()}
        if history:
            entries, total, next_cursor = history_page(conn, feed, now, cursor, list(reviews))
        else:
            entries, total, next_cursor = page_sources(conn, feed, now, cursor)
        activities = draft_storage.normalize_content(plan['content'])['activities']
        dated_routes = {str(row['activity_id']): row['reference'] for row in conn.execute(
            "SELECT activity_id, reference FROM workday_route_references WHERE workday_id=%s "
            "AND reference->>'status'='compatible' AND reference->'provenance'->>'manifest_revision'='tromso-city'",
            (identifier,),
        ).fetchall()}
        results = []
        for situation, _ in entries:
            source = public_item(conn, situation, feed, now)
            saved = reviews.get(situation)
            decision = saved['decision'] if saved else None
            assessment = (classify(source['content'], activities, now, dated_routes) if source else
                          {'classification': 'review', 'reasons': ['retained-private-evidence'], 'matches': [], 'validity_expired': False})
            reassessment = bool(decision and (not source or decision['source_basis'] != source['basis']
                                             or decision['plan_revision'] != plan['source_revision']))
            results.append({'situation': situation, 'source': source, 'review_revision': saved['revision'] if saved else 0,
                            'decision': decision, 'needs_reassessment': reassessment,
                            'manual': manual(conn, owner, decision['manual_notice_id']) if decision else None, **assessment})
        # Recheck after assembling the projection. The parent lock excludes expiry changes and deletion.
        workday_storage.owned(conn, owner, identifier, request)
        return {'workday_id': identifier, 'plan_revision': plan['source_revision'], 'expires_at': plan['expires_at'],
                'server_now': now, 'lifecycle': stage, 'health': feed, 'binding': BINDING,
                'entries': results, 'total': total, 'page_counts': Counter(item['classification'] for item in results),
                'next_cursor': next_cursor}


def history_page(conn, feed, now, cursor, reviews):
    args = ('TRO', feed['generation'], now - RETENTION, reviews)
    entries = conn.execute(f'WITH keys AS ({VISIBLE_IDENTITIES} UNION SELECT unnest(%s::text[])) '
                           'SELECT situation,(SELECT count(*) FROM keys) AS total FROM keys '
                           'WHERE (%s::text IS NULL OR situation>%s) ORDER BY situation LIMIT %s',
                           (*args, cursor, cursor, PAGE_LIMIT + 1)).fetchall()
    total = entries[0]['total'] if entries else conn.execute(
        f'SELECT count(*) AS n FROM ({VISIBLE_IDENTITIES} UNION SELECT unnest(%s::text[])) keys', args).fetchone()['n']
    return ([(row['situation'], None) for row in entries[:PAGE_LIMIT]], total,
            entries[PAGE_LIMIT - 1]['situation'] if len(entries) > PAGE_LIMIT else None)


def receipt(conn, identifier, owner, operation_id):
    return conn.execute('SELECT payload_hash,result FROM automatic_notice_review_operations '
                        'WHERE workday_id=%s AND id=%s AND owner=%s AND expires_at>clock_timestamp()',
                        (identifier, operation_id, owner)).fetchone()


@router.get(PLAN_PATH + '/operations/{operation_id}')
def lookup(identifier: UUID, operation_id: UUID, request: Request):
    with database() as conn:
        owner, _ = access(conn, identifier, request)
        accepted = receipt(conn, identifier, owner, operation_id)
        if accepted is None:
            draft_storage.deny()
        workday_storage.owned(conn, owner, identifier, request)
        return accepted['result']


def conflict(detail='Gjennomgangen har endret seg. Hent dagens opplysninger og sammenlign.'):
    raise HTTPException(409, detail)


@router.post(PLAN_PATH + '/review')
def save(identifier: UUID, command: ReviewCommand, request: Request):
    with database() as conn:
        owner, plan = access(conn, identifier, request)
        workday_storage.require_mutable(conn, plan)
        digest = draft_storage.fingerprint(identifier, command.model_dump(mode='json'))
        accepted = receipt(conn, identifier, owner, command.operation_id)
        if accepted:
            if accepted['payload_hash'] != digest:
                conflict('Forsøks-ID er allerede brukt for et annet forslag.')
            workday_storage.owned(conn, owner, identifier, request)
            return accepted['result']
        now = clock(conn)
        feed = health(conn, now)
        stage = lifecycle(conn, identifier)
        if plan['source_revision'] != command.expected_plan_revision or stage['revision'] != command.expected_lifecycle_revision:
            conflict()
        saved = conn.execute('SELECT revision,decision FROM automatic_notice_reviews '
                             'WHERE workday_id=%s AND participant=%s AND situation=%s AND owner=%s',
                             (identifier, 'TRO', command.situation, owner)).fetchone()
        expected = saved['revision'] if saved else 0
        source = public_item(conn, command.situation, feed, now)
        # If the public record aged out, a driver may clear the already saved private choice.
        basis = source['basis'] if source else saved['decision']['source_basis'] if saved else None
        if expected != command.expected_revision or basis != command.expected_source_basis or (
            source is None and (command.action != 'unresolved' or command.manual_notice_id is not None)
        ):
            conflict()
        if command.activity_id is not None and str(command.activity_id) not in {
            item['id'] for item in draft_storage.normalize_content(plan['content'])['activities']
        }:
            raise HTTPException(422, 'Velg en aktivitet i dagens bekreftede plan.')
        if command.manual_notice_id is not None and not manual(conn, owner, command.manual_notice_id):
            draft_storage.deny()
        limits = conn.execute('SELECT (SELECT count(*) FROM automatic_notice_reviews WHERE workday_id=%s) AS reviews,'
                              '(SELECT count(*) FROM automatic_notice_review_operations WHERE workday_id=%s) AS operations',
                              (identifier, identifier)).fetchone()
        if limits['operations'] >= MAX_OPERATIONS or (not saved and limits['reviews'] >= MAX_DECISIONS):
            raise HTTPException(429, 'Grensen for lagrede gjennomganger er nådd.')
        workday_storage.owned(conn, owner, identifier, request)
        now = clock(conn)
        if now >= plan['expires_at']:
            raise HTTPException(410, 'Planen er utløpt.')
        decision = {'action': command.action, 'activity_id': str(command.activity_id) if command.activity_id else None,
                    'reason': command.reason, 'manual_notice_id': str(command.manual_notice_id) if command.manual_notice_id else None,
                    'plan_revision': plan['source_revision'], 'source_basis': basis, 'decided_at': now.isoformat(),
                    'source_revision': source['revision'] if source else saved['decision']['source_revision'],
                    'evidence': source['content'] if source else saved['decision']['evidence'],
                    'source_response_at': source['response_at'].isoformat() if source else saved['decision']['source_response_at'],
                    'source_observed_at': source['last_seen'].isoformat() if source else saved['decision']['source_observed_at'],
                    'source_generation': str(source['complete_generation']) if source and source['complete_generation'] else (
                        None if source else saved['decision']['source_generation']),
                    'source_conflicts': source['conflict_count'] if source else saved['decision']['source_conflicts']}
        conn.execute('INSERT INTO automatic_notice_reviews(workday_id,owner,expires_at,participant,situation,revision,decision) '
                     'VALUES(%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(workday_id,participant,situation) DO UPDATE SET '
                     'revision=EXCLUDED.revision,decision=EXCLUDED.decision',
                     (identifier, owner, plan['expires_at'], 'TRO', command.situation, expected + 1, Jsonb(decision)))
        result = {'workday_id': str(identifier), 'operation_id': str(command.operation_id), 'situation': command.situation,
                  'revision': expected + 1, 'decision': decision}
        conn.execute('INSERT INTO automatic_notice_review_operations(workday_id,id,owner,expires_at,payload_hash,result) '
                     'VALUES(%s,%s,%s,%s,%s,%s)', (identifier, command.operation_id, owner, plan['expires_at'], digest, Jsonb(result)))
        workday_storage.owned(conn, owner, identifier, request)
        return result
