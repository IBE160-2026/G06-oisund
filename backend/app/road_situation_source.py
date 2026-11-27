"""Bounded ingest of the public SituationSimple publication for Tromsø."""

import argparse
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from hashlib import sha256
import json
from math import hypot, isfinite
import re
import sys
from urllib.parse import urlencode
from urllib.request import Request, build_opener

from .road_evidence import NoRedirect, reject_json_constant, unique_json_members


BASE = 'https://ogckart-sn1.atlas.vegvesen.no/datex_3_1/ows'
MAX_BYTES = 4_194_304
MAX_FEATURES = 300
# The documented Tromsø sample was 12 features / 31,923 bytes. These limits
# leave room for long detours while bounding geometry independently of JSON size.
MAX_EVENT_POINTS = 2_048
MAX_SNAPSHOT_POINTS = 16_384
MAX_LOOKUP_WORK = 1_000_000
LEASE = timedelta(minutes=5)
GEOMETRIES = {
    'Point': (), 'LineString': (2,), 'MultiPoint': (1,), 'MultiLineString': (1, 2),
    'Polygon': (1, 4), 'MultiPolygon': (1, 1, 4),
}
ROAD = re.compile(r'^([ERFKSP])V?([1-9][0-9]{0,6})(?=\s|$)')
FIELD = (18.70, 69.59, 19.14, 69.77)


class GeometryBudget:
    def __init__(self, remaining):
        self.remaining = remaining

    def take(self, amount):
        if amount > self.remaining:
            return False
        self.remaining -= amount
        return True


class GeometryLimit(ValueError):
    pass


def url():
    west, south, east, north = FIELD
    points = ((west, south), (east, south), (east, north), (west, north), (west, south))
    ring = ', '.join(f'{lon:.2f} {lat:.2f}' for lon, lat in points)
    return BASE + '?' + urlencode({
        'service': 'WFS', 'version': '1.0.0', 'request': 'GetFeature',
        'typeName': 'datex_3_1:SituationSimple', 'outputFormat': 'application/json',
        'srsName': 'EPSG:4326', 'maxFeatures': MAX_FEATURES,
        'CQL_FILTER': f'Intersects(geometry, POLYGON(({ring})))',
    })


def instant(value):
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    return parsed.astimezone(UTC) if parsed.utcoffset() is not None else None


def road_number(value):
    if not isinstance(value, str):
        return None
    match = ROAD.match(value.upper().strip())
    return ''.join(match.groups()) if match else None


def geometry_points(coordinates, levels):
    if not isinstance(coordinates, list):
        raise ValueError('Unsupported DATEX coordinates')
    if not levels:
        if len(coordinates) not in (2, 3) or any(type(value) not in (int, float) or not isfinite(value) for value in coordinates):
            raise ValueError('Unsupported DATEX coordinate position')
        lon, lat = coordinates[:2]
        if not (-180 <= lon <= 180 and -90 <= lat <= 90):
            raise ValueError('DATEX coordinates outside WGS84')
        yield lon, lat
        return
    if len(coordinates) < levels[0]:
        raise ValueError('Unsupported DATEX coordinate sequence')
    for child in coordinates:
        yield from geometry_points(child, levels[1:])


def bounds(points):
    west = south = float('inf')
    east = north = float('-inf')
    for lon, lat in points:
        west, south = min(west, lon), min(south, lat)
        east, north = max(east, lon), max(north, lat)
    return west, south, east, north


def bounded_points(points, snapshot_budget):
    event_budget = GeometryBudget(MAX_EVENT_POINTS)
    for point in points:
        if not snapshot_budget.take(1) or not event_budget.take(1):
            raise GeometryLimit
        yield point


def linework_size(linework, limit):
    size = 0
    for line in linework or ():
        size += max(1, len(line))
        if size > limit:
            return None
    return size


def bounded_events(events):
    """Apply the current bounds to snapshots recorded by older API images."""
    remaining = MAX_SNAPSHOT_POINTS
    result = []
    for event in events:
        limit = min(remaining, MAX_EVENT_POINTS)
        size = linework_size(event.get('linework'), limit)
        if size is None:
            remaining -= limit
            result.append(dict(event, linework=None, geometry_unqualified=True))
        else:
            remaining -= size
            result.append(dict(event, geometry_points=size) if size else event)
    return result


def parse(raw, header_date, now):
    if not 0 < len(raw) <= MAX_BYTES:
        raise ValueError('DATEX response exceeds its byte limit')
    try:
        receipt = parsedate_to_datetime(header_date)
    except (TypeError, ValueError):
        raise ValueError('Missing DATEX transport time') from None
    value = json.loads(raw, object_pairs_hook=unique_json_members, parse_constant=reject_json_constant)
    observed = instant(value.get('timeStamp'))
    if (observed is None or receipt.utcoffset() != timedelta(0)
            or abs(receipt - observed) > timedelta(seconds=60)
            or not now - LEASE <= observed <= now + timedelta(seconds=5)):
        raise ValueError('DATEX snapshot is outside the freshness window')
    features = value['features']
    count = value.get('numberMatched')
    if (value.get('type') != 'FeatureCollection' or type(count) is not int
            or not 0 <= count < MAX_FEATURES or type(features) is not list
            or count != len(features) or count != value.get('numberReturned') or count != value.get('totalFeatures')
            or value.get('crs') != {'type': 'name', 'properties': {'name': 'urn:ogc:def:crs:EPSG::4326'}}):
        raise ValueError('DATEX snapshot is incomplete or has the wrong spatial reference')
    IDs = set()
    events = []
    snapshot_budget = GeometryBudget(MAX_SNAPSHOT_POINTS)
    payload_digest = sha256(raw).hexdigest()
    for feature in features:
        properties = feature['properties']
        record, situation = properties['recordId'], properties['situationId']
        if (feature.get('type') != 'Feature' or properties.get('@featureType') != 'geoJsonSituationSimple'
                or not all(isinstance(item, str) and 0 < len(item) <= 180 and item.isprintable() for item in (record, situation))
                or record in IDs):
            raise ValueError('DATEX feature has an invalid identity')
        IDs.add(record)
        geometry = feature.get('geometry')
        bbox = None
        linework = None
        geometry_unqualified = False
        if geometry is not None:
            if geometry.get('type') not in GEOMETRIES:
                raise ValueError('Unsupported DATEX geometry')
            coordinates = geometry['coordinates']
            points = geometry_points(coordinates, GEOMETRIES[geometry['type']])
            try:
                bbox = bounds(bounded_points(points, snapshot_budget))
            except GeometryLimit:
                # A prefix cannot establish where the rest of the line goes.
                bbox, geometry_unqualified = FIELD, True
            if bbox[2] < FIELD[0] or bbox[0] > FIELD[2] or bbox[3] < FIELD[1] or bbox[1] > FIELD[3]:
                raise ValueError('DATEX geometry lies outside the requested field area')
            if not geometry_unqualified:
                match geometry['type']:
                    case 'Point':
                        linework = [[coordinates]]
                    case 'MultiPoint':
                        linework = [[point] for point in coordinates]
                    case 'LineString':
                        linework = [coordinates]
                    case 'MultiLineString':
                        linework = coordinates
        start, end = instant(properties.get('startTime')), instant(properties.get('endTime'))
        if start is not None and end is not None and start >= end:
            start = end = None
        event = {'record': record, 'situation': situation, 'road': road_number(properties.get('roadNumber')),
                 'bounds': bbox, 'point': bool(geometry and geometry['type'] in ('Point', 'MultiPoint')),
                 'speed_management': properties.get('situationType') == 'SpeedManagement',
                 'linework': linework, 'start': start.isoformat() if start else None,
                 'end': end.isoformat() if end else None}
        # Tie approval to the exact publisher record as well as its normalized location.
        properties_basis = {key: item for key, item in properties.items()
                            if key not in ('_id', 'pubId', 'startJsonTime', 'endJsonTime')}
        if geometry_unqualified:
            event['geometry_unqualified'] = True
            geometry = {'unqualified_snapshot': payload_digest}
        event['revision'] = sha256(json.dumps([properties_basis, geometry], sort_keys=True, ensure_ascii=False,
                                               separators=(',', ':')).encode()).hexdigest()
        events.append(event)
    return {'url': url(), 'sha256': payload_digest, 'observed_at': observed.isoformat(),
            'events': sorted(events, key=lambda event: event['record'])}


def active(events, now):
    result = []
    for event in events:
        start, end = instant(event['start']), instant(event['end'])
        if (start is None or start <= now) and (end is None or now < end):
            result.append(event)
    return result


def affects(event, road_reference, edge_bounds):
    if event['bounds'] is None:
        return event['road'] is None or road_number(road_reference) == event['road']
    west, south, east, north = event['bounds']
    # Include close roads and connecting arms when the publisher supplies a
    # point or a line without a directional NVDB placement.
    margin_lon, margin_lat = (.007, .0025) if event['point'] else (.002, .0007)
    return (edge_bounds[0] <= east + margin_lon and edge_bounds[2] >= west - margin_lon
            and edge_bounds[1] <= north + margin_lat and edge_bounds[3] >= south - margin_lat)


def point_distance(point, start, end):
    dx, dy = end[0] - start[0], end[1] - start[1]
    px, py = point[0] - start[0], point[1] - start[1]
    square = dx * dx + dy * dy
    ratio = max(0, min(1, (px * dx + py * dy) / square)) if square else 0
    return hypot(px - ratio * dx, py - ratio * dy)


def cross(first, second, point):
    return (second[0] - first[0]) * (point[1] - first[1]) - (second[1] - first[1]) * (point[0] - first[0])


def segment_distance(a, b, c, d):
    if (max(min(a[0], b[0]), min(c[0], d[0])) <= min(max(a[0], b[0]), max(c[0], d[0]))
            and max(min(a[1], b[1]), min(c[1], d[1])) <= min(max(a[1], b[1]), max(c[1], d[1]))
            and cross(a, b, c) * cross(a, b, d) <= 0 and cross(c, d, a) * cross(c, d, b) <= 0):
        return 0
    return min(point_distance(a, c, d), point_distance(b, c, d), point_distance(c, a, b), point_distance(d, a, b))


def metric(points):
    return [(lon * 38_600, lat * 111_200) for lon, lat, *_ in points]


def affects_edge(event, road_reference, shape, *, edge_bounds=None, budget=None):
    if budget is not None and not budget.take(1):
        return True
    if not affects(event, road_reference, edge_bounds if edge_bounds is not None else bounds(shape)):
        return False
    linework = event.get('linework')
    if not linework:
        return True
    if budget is not None:
        points = event.get('geometry_points')
        if points is None:
            points = linework_size(linework, MAX_EVENT_POINTS)
        if points is None or not budget.take(len(shape) * points):
            return True
    segments = metric(shape)
    radius = 280 if event['point'] else 80
    for line in linework:
        reported = metric(line)
        for start, end in zip(segments, segments[1:]):
            if len(reported) == 1 and point_distance(reported[0], start, end) <= radius:
                return True
            if any(segment_distance(start, end, left, right) <= radius for left, right in zip(reported, reported[1:])):
                return True
    return False


def publish(snapshot, now):
    from psycopg.types.json import Jsonb
    from .private_storage import database

    with database() as conn:
        row = conn.execute(
            '''INSERT INTO public_road_situation_snapshots VALUES (%s, %s, %s, %s)
               ON CONFLICT (observed_at) DO UPDATE SET sha256 = public_road_situation_snapshots.sha256
               WHERE public_road_situation_snapshots.sha256 = EXCLUDED.sha256 RETURNING observed_at''',
            (instant(snapshot['observed_at']), snapshot['sha256'], snapshot['url'], Jsonb(snapshot['events'])),
        ).fetchone()
        if row is None:
            raise ValueError('Conflicting DATEX snapshot at the same timestamp')
        conn.execute('DELETE FROM public_road_situation_snapshots WHERE observed_at < %s', (now - timedelta(days=2),))


def latest(conn, now):
    row = conn.execute('SELECT events, observed_at FROM public_road_situation_snapshots WHERE observed_at <= %s '
                       'ORDER BY observed_at DESC LIMIT 1', (now,)).fetchone()
    if row is None:
        return [], None
    expires = row['observed_at'] + LEASE
    return bounded_events(row['events']), expires if now < expires else None


def status(now):
    from .private_storage import database

    with database() as conn:
        row = conn.execute('SELECT observed_at, sha256, events FROM public_road_situation_snapshots '
                           'WHERE observed_at <= %s ORDER BY observed_at DESC LIMIT 1', (now,)).fetchone()
    if row is None:
        return {'state': 'missing', 'observed_at': None, 'records': 0}
    observed = row['observed_at']
    return {'state': 'fresh' if now - observed <= LEASE else 'old', 'observed_at': observed.isoformat(),
            'sha256': row['sha256'], 'records': len(row['events']),
            'record_revisions': {event['record']: event['revision'] for event in row['events']}}


def fetch():
    request = Request(url(), headers={'Accept': 'application/json', 'Accept-Encoding': 'identity',
                                      'User-Agent': 'IBE160-Bussassistent-road-situations'})
    with build_opener(NoRedirect()).open(request, timeout=15) as response:
        if (response.status != 200 or response.headers.get_content_type() != 'application/json'
                or response.headers.get('Content-Encoding', 'identity').lower() != 'identity'):
            raise ValueError('Unexpected DATEX transport')
        raw = response.read(MAX_BYTES + 1)
        header = response.headers['Date']
    parse(raw, header, datetime.now(UTC))
    return {'http_date': header, 'geojson': raw.decode('utf-8')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument('--fetch', action='store_true')
    actions.add_argument('--publish-stdin', action='store_true')
    actions.add_argument('--status', action='store_true')
    args = parser.parse_args()
    if args.fetch:
        json.dump(fetch(), sys.stdout, ensure_ascii=False)
        return
    if args.status:
        print(json.dumps(status(datetime.now(UTC))))
        return
    limit = MAX_BYTES * 2 + 4096
    raw = sys.stdin.buffer.read(limit + 1)
    if len(raw) > limit:
        raise ValueError('DATEX transport bundle exceeds its byte limit')
    bundle = json.loads(raw, object_pairs_hook=unique_json_members)
    now = datetime.now(UTC)
    snapshot = parse(bundle['geojson'].encode(), bundle['http_date'], now)
    publish(snapshot, now)
    print(json.dumps({'observed_at': snapshot['observed_at'], 'records': len(snapshot['events'])}))


if __name__ == '__main__':
    main()
