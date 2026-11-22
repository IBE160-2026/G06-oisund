"""An authenticated lookup for a manually selected road area."""

from datetime import datetime, time, timedelta
import gzip
from hashlib import sha256
import json
from typing import Literal

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response

from . import draft_storage, road_situation_source
from .private_storage import database
from .road_area_catalogue import OSLO


router = APIRouter(prefix='/road-areas')
Area = Literal['kvaloya', 'tromsoya', 'fastlandet']


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
    material = json.dumps([base, current_situations, crossed, registered_ready,
                           upcoming.isoformat() if upcoming else None, legacy_review],
                          sort_keys=True, separators=(',', ':'))
    return sha256(material.encode()).hexdigest()


@router.get('/{area}')
def road_area(area: Area, request: Request):
    now = datetime.now(OSLO)
    day = now.date()
    with database() as conn:
        draft_storage.authorized(conn, request)
        row = conn.execute(
            '''SELECT revision, manifest, source->'review'->'limits' AS review FROM public_road_area_versions
               WHERE area_id = %s AND effective_date = %s
               ORDER BY observed_at DESC, checked_at DESC LIMIT 1''',
            (area, day),
        ).fetchone()
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
        if unavailable or current_situations and any(
            not (event['speed_management'] and reviewed.get(event['record']) == event['revision'])
            and (event['bounds'] is None and road is None
                 or road_situation_source.affects_edge(event, road, edge['shape'])) for event in current_situations
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
        row = conn.execute(
            '''SELECT revision, manifest->'roadNumbers' AS roads, manifest->'temporaryBoundaries' AS boundaries,
                      manifest->'registeredInteriors' AS registered, manifest->'situationBounds' AS extent,
                      jsonb_typeof(source->'review'->'limits') = 'object' AS reviewed
               FROM public_road_area_versions
               WHERE area_id = %s AND effective_date = %s
               ORDER BY observed_at DESC, checked_at DESC LIMIT 1''',
            (area, now.date()),
        ).fetchone()
        if row is None:
            return {'revision': None}
        events, lease, upcoming = relevant_situations(conn, row['extent'], row['roads'], now)
        registered_ready = bool(row['registered'] and lease)
        revision = effective_revision(row['revision'], events, row['boundaries'], now, registered_ready, upcoming,
                                      row['boundaries'] is None and bool(row['reviewed']))
    return {'revision': revision, **({'situationLeaseUntil': lease.isoformat()} if registered_ready else {})}
