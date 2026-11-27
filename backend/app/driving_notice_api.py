"""Driver-facing notice projection against a selected, frozen departure."""
from datetime import date
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Query, Request

from . import auth, automatic_notice_api as notices, draft_storage, route_catalogue, workday_storage
from .automatic_notice_source import instant
from .notice_geography import automatic_scope, manual_scope, notice_stop_options, has_section, segments
from .private_storage import database

router = APIRouter()


@router.get('/notice-stop-options')
def stop_options(request: Request, query: Annotated[str, Query(min_length=2, max_length=80)],
                 mode: Literal['stop', 'platform'] = 'stop', day: date | None = None,
                 line: Annotated[str | None, Query(max_length=12)] = None):
    from .automatic_notice_relevance import OSLO

    with database() as conn:
        auth.session(conn, request)
        now = notices.clock(conn)
        candidates = notice_stop_options(conn, day or now.astimezone(OSLO).date(), query.strip(), mode,
                                         route_catalogue.code_for(line))
        auth.session(conn, request)
        return {'stops': candidates}


@router.get('/notice-route-options')
def route_options(request: Request, day: date, line: Annotated[str, Query(max_length=12)],
                  start: Annotated[str, Query(max_length=180)], end: Annotated[str, Query(max_length=180)],
                  direction: Literal['inbound', 'outbound'] | None = None):
    code = route_catalogue.code_for(line)
    with database() as conn:
        auth.session(conn, request)
        chosen = conn.execute(
            "SELECT service_date FROM public_route_days WHERE line_code=%s "
            "AND service_date BETWEEN %s::date - 14 AND %s::date + 14 "
            "ORDER BY ABS(service_date - %s::date),service_date DESC LIMIT 1", (code, day, day, day),
        ).fetchone()
        now = notices.clock(conn)
        journeys = route_catalogue.lookup(conn, chosen['service_date'] if chosen else day, now, code)['journeys']
        available = {}
        for journey in journeys.values():
            route_id = journey.get('route_id')
            calls = journey['calls']
            if route_id in available or not route_id or direction and journey['direction'] != direction:
                continue
            for first, last in segments(calls, start, end):
                middle = calls[first+1:last]
                via = ', '.join(dict.fromkeys(call['name'] for call in middle[:3]))
                available[route_id] = {'ref': route_id, 'name': journey['headsign'], 'via': via,
                                       'direction': journey['direction']}
                break
        auth.session(conn, request)
        return {'routes': sorted(available.values(), key=lambda item: (item['name'], item['ref']))[:35]}


def title_of(content):
    for field in ('summary', 'description'):
        items = content.get(field, ())
        preferred = next((item for item in items if (item.get('language') or '').lower() in {'no', 'nb', 'nn'}), None)
        if preferred or items:
            return (preferred or items[0])['text'][:300]
    return 'Melding fra Entur'


def active_end(content, now):
    ends = [end for period in content['windows']
            if (start := instant(period['start'])) and (end := instant(period['end'])) and start <= now < end]
    return max(ends, default=None)


def narrowest(scopes):
    priority = {'section': 0, 'stops': 1, 'line': 2, 'area': 3, 'network': 4, 'uncertain': 5}
    result = min(scopes, key=lambda scope: priority[scope['scope']], default=None)
    if result and result['scope'] == 'stops':
        points = [scope for scope in scopes if scope['scope'] == 'stops']
        result = {**result, 'positions': sorted({p for scope in points for p in scope['positions']}),
                  'cancelled': sorted({p for scope in points for p in scope['cancelled']})}
    return result


@router.get('/workdays/{identifier}/driving-notices/{activity_id}')
def driving_notices(identifier: UUID, activity_id: UUID, request: Request):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        plan = workday_storage.owned(conn, owner, identifier, request)
        activity = next((a for a in plan['content']['activities'] if a['id'] == str(activity_id)), None)
        if not activity:
            draft_storage.deny()
        now = notices.clock(conn)
        feed = notices.health(conn, now)
        frozen = conn.execute('SELECT reference FROM workday_route_references WHERE workday_id=%s AND activity_id=%s',
                              (identifier, activity_id)).fetchone()
        route = frozen['reference'] if frozen else None
        variants = None

        def dated_variants():
            nonlocal variants
            if variants is None:
                variants = route_catalogue.lookup(conn, date.fromisoformat(route['service_date']), now,
                                                   route_catalogue.code_for(route['line_id']))['journeys'].values() if route else ()
            return variants

        rows = conn.execute(
            """SELECT id,title,summary,source_note,line_scope,line_tags,geography,valid_until FROM workday_notices
            WHERE owner=%s AND status='registered' AND valid_until>%s AND expires_at>%s
            AND (valid_from IS NULL OR valid_from<=%s) ORDER BY valid_until,id""", (owner, now, now, now),
        ).fetchall()
        result = []
        for row in rows:
            geo = row['geography']
            scoped = manual_scope(row, activity, route, dated_variants() if geo and geo['kind'] == 'section' else ())
            if scoped:
                result.append({**scoped, 'id': str(row['id']), 'title': row['title'], 'valid_until': row['valid_until'],
                               'source': 'manual', 'urgent': False})
        for key, state in notices.operational_sources(conn, feed, now, route):
            if state != 'active':
                continue
            source = notices.public_item(conn, key, feed, now)
            content = source['content']
            end = active_end(content, now)
            if not end or source['conflict_count']:
                continue
            fields = has_section(content['affects'])
            scoped = narrowest(list(automatic_scope(content, route, dated_variants() if fields else ())))
            if scoped:
                result.append({**scoped, 'id': key, 'title': title_of(content), 'valid_until': end,
                               'source': 'entur', 'urgent': content.get('severity') in {'severe', 'verySevere'}})
        auth.session(conn, request)
        return {'workday_id': identifier, 'activity_id': activity_id, 'server_now': now, 'notices': sorted(result, key=lambda item: (not item['urgent'], item['valid_until'], item['id']))[:1000],
                'feed': feed['status'], 'old': feed['old']}
