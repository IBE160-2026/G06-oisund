"""Authenticated, dated lookups for the Tromsø road network."""

from datetime import datetime, time, timedelta
import gzip
from hashlib import sha256
import json
from typing import Literal

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response

from . import draft_storage, road_situation_source
from .private_storage import database
from .road_area_catalogue import AREAS, OSLO


router = APIRouter(prefix='/road-areas')
Area = Literal['kvaloya', 'tromsoya', 'fastlandet', 'pilot']


def area_rows(conn, area, day, columns):
    if area != 'pilot':
        return conn.execute(
            f'''SELECT {columns} FROM public_road_area_versions WHERE effective_date=%s AND area_id=%s
                ORDER BY observed_at DESC, checked_at DESC LIMIT 1''', (day, area),
        ).fetchall()
    return conn.execute(
        f'''WITH publication AS (
                SELECT observed_at, checked_at, revision FROM public_road_area_versions
                WHERE effective_date=%s AND area_id=ANY(%s)
                GROUP BY observed_at, checked_at, revision HAVING count(*)=%s
                ORDER BY observed_at DESC, checked_at DESC LIMIT 1
            )
            SELECT {columns} FROM public_road_area_versions
            JOIN publication USING (observed_at, checked_at, revision)
            WHERE effective_date=%s AND area_id=ANY(%s) ORDER BY area_id''',
        (day, list(AREAS), len(AREAS), day, list(AREAS)),
    ).fetchall()


def joint_values(items, name):
    return sorted({value for item in items for value in (item.get(name) or ())})


def joint_bounds(bounds):
    if not all(bounds):
        return None
    return [min(box[0] for box in bounds), min(box[1] for box in bounds),
            max(box[2] for box in bounds), max(box[3] for box in bounds)]


def pilot_row(rows):
    if len(rows) != len(AREAS):
        return None
    manifests = [row['manifest'] for row in rows]
    first = manifests[0]
    for name in ('retrievedAt', 'checkedAt', 'validFrom', 'validUntil', 'profile', 'uncertaintyM'):
        if any(item.get(name) != first.get(name) for item in manifests):
            return None
    edges = {}
    for manifest in manifests:
        for edge in manifest['packages'][0]['edges']:
            if edges.setdefault(edge['id'], edge) != edge:
                return None
    if not edges or len(edges) > 20_000 or sum(len(edge['shape']) for edge in edges.values()) > 350_000:
        return None
    revision = rows[0]['revision']
    combined = {
        **first, 'id': 'pilot',
        'roadNumbers': joint_values(manifests, 'roadNumbers') if all(item.get('roadNumbers') is not None for item in manifests) else None,
        'situationBounds': joint_bounds([item.get('situationBounds') for item in manifests]),
        'registeredInteriors': any(item.get('registeredInteriors') for item in manifests),
        'packages': [{'id': 'pilot', 'revision': revision, 'edges': list(edges.values())}],
    }
    if any('temporaryBoundaries' in manifest for manifest in manifests):
        combined['temporaryBoundaries'] = joint_values(manifests, 'temporaryBoundaries')
    return {**rows[0], 'manifest': combined}



def relevant_situations(conn, area_bounds, roads, now):
    events, lease = road_situation_source.latest(conn, now)
    relevant = [event for event in events
                if road_situation_source.affects(event, None, area_bounds or road_situation_source.FIELD)
                or event['bounds'] is None and (roads is None or event['road'] in roads)]
    starts = (road_situation_source.instant(event['start']) for event in relevant)
    upcoming = min((stamp for stamp in starts if stamp is not None and stamp > now), default=None)
    return road_situation_source.active(relevant, now), lease, upcoming


def effective_revision(base, current_situations, boundaries, now, registered_ready, upcoming, legacy_review):
    crossed = sum(datetime.fromisoformat(value) <= now for value in boundaries or ())
    if not current_situations and not crossed and not registered_ready and upcoming is None and not legacy_review:
        return base
    geometry_policy = 'bounded-datex' if current_situations else None
    material = json.dumps([base, current_situations, crossed, registered_ready,
                           upcoming.isoformat() if upcoming else None, legacy_review, geometry_policy],
                          sort_keys=True, separators=(',', ':'))
    return sha256(material.encode()).hexdigest()


@router.get('/{area}')
def road_area(area: Area, request: Request):
    now = datetime.now(OSLO)
    day = now.date()
    with database() as conn:
        draft_storage.authorized(conn, request)
        rows = area_rows(conn, area, day, "revision, manifest, source->'review'->'limits' AS review")
        row = pilot_row(rows) if area == 'pilot' else next(iter(rows), None)
        if row is None:
            return {'status': 'road-unqualified'}
        current_situations, lease, upcoming = relevant_situations(
            conn, row['manifest'].get('situationBounds'), row['manifest'].get('roadNumbers'), now,
        )
    manifest = row['manifest']
    manifest.pop('roadNumbers', None)
    manifest.pop('situationBounds', None)
    legacy_review = 'temporaryBoundaries' not in manifest and isinstance(row['review'], dict)
    boundaries = manifest.pop('temporaryBoundaries', ())
    registered_ready = bool(manifest.pop('registeredInteriors', False) and lease)
    manifest['revision'] = effective_revision(row['revision'], current_situations, boundaries, now, registered_ready,
                                              upcoming, legacy_review)
    review = row['review'] or {}
    edges = manifest['packages'][0]['edges']
    budget = road_situation_source.GeometryBudget(road_situation_source.MAX_LOOKUP_WORK)
    for edge in edges:
        road = edge.pop('roadReference', None)
        registered = edge.pop('registeredKmh', None)
        restriction = edge.pop('temporaryRestriction', None)
        if edge['kmh'] is None and registered_ready:
            edge['kmh'] = registered
        if edge['kmh'] is None:
            continue
        reviewed = restriction['records'] if restriction else {}
        unavailable = (not restriction and review.get(edge.get('id'), {}).get('basis') == 'temporary'
                       or restriction and not datetime.fromisoformat(restriction['start']) <= now < datetime.fromisoformat(restriction['end']))
        edge_bounds = road_situation_source.bounds(edge['shape']) if current_situations and not unavailable and budget.remaining else None
        if unavailable or current_situations and any(
            road_situation_source.affects_edge(event, road, edge['shape'], edge_bounds=edge_bounds,
                                              budget=budget, reviewed=reviewed)
            for event in current_situations
        ):
            edge['kmh'] = None
            edge.pop('confirmedTransitions', None)
    confirmed = sum(edge['kmh'] is not None for edge in edges)
    if confirmed:
        checked, observed, valid_until = (datetime.fromisoformat(manifest[key]) for key in ('checkedAt', 'retrievedAt', 'validUntil'))
        if not (timedelta() <= now - checked <= timedelta(days=1)
                and timedelta() <= now - observed <= timedelta(days=7) and now < valid_until):
            for edge in edges:
                edge['kmh'] = None
                edge.pop('confirmedTransitions', None)
            confirmed = 0
        else:
            next_boundary = next((datetime.fromisoformat(value) for value in boundaries
                                  if datetime.fromisoformat(value) > now), None)
            manifest['validUntil'] = min(stamp for stamp in (valid_until, next_boundary, upcoming) if stamp is not None).isoformat()
            if registered_ready:
                manifest['situationLeaseUntil'] = lease.isoformat()
    if not confirmed and 'validUntil' in manifest:
        manifest['validUntil'] = datetime.combine(day + timedelta(days=1), time(), OSLO).isoformat()
    response = JSONResponse({'status': 'qualified', 'manifest': manifest, 'confirmed': confirmed},
                            headers={'Vary': 'Accept-Encoding'})
    encodings = request.headers.get('accept-encoding', '').lower().split(',')
    # This response contains only public road data and no session or owner fields.
    if any(value.strip() == 'gzip' for value in encodings):
        return Response(gzip.compress(response.body, compresslevel=3), media_type='application/json',
                        headers={'Content-Encoding': 'gzip', 'Vary': 'Accept-Encoding'})
    return response


@router.get('/{area}/revision')
def road_area_revision(area: Area, request: Request):
    now = datetime.now(OSLO)
    with database() as conn:
        draft_storage.authorized(conn, request)
        rows = area_rows(conn, area, now.date(),
                         """revision, manifest->'roadNumbers' AS roads, manifest->'temporaryBoundaries' AS boundaries,
                            manifest->'registeredInteriors' AS registered, manifest->'situationBounds' AS extent,
                            jsonb_typeof(source->'review'->'limits') = 'object' AS reviewed""")
        row = next(iter(rows), None)
        if area == 'pilot' and len(rows) == len(AREAS):
            row = {**rows[0], 'roads': joint_values(rows, 'roads') if all(item['roads'] is not None for item in rows) else None,
                   'boundaries': joint_values(rows, 'boundaries') if any(item['boundaries'] is not None for item in rows) else None,
                   'extent': joint_bounds([item['extent'] for item in rows]),
                   'registered': any(item['registered'] for item in rows)}
        if row is None:
            return {'revision': None}
        events, lease, upcoming = relevant_situations(conn, row['extent'], row['roads'], now)
        registered_ready = bool(row['registered'] and lease)
        revision = effective_revision(row['revision'], events, row['boundaries'], now, registered_ready, upcoming,
                                      row['boundaries'] is None and bool(row['reviewed']))
    return {'revision': revision, **({'situationLeaseUntil': lease.isoformat()} if registered_ready else {})}
