"""Collect dated NVDB area geometry and candidate speed facts for review.

The output preserves research evidence for offline qualification.
"""

import argparse
from collections import Counter, defaultdict
from datetime import UTC, date, datetime
from hashlib import sha256
import json
from math import isfinite
from pathlib import Path
import re
from urllib.parse import urlencode
from urllib.request import Request, build_opener
from zipfile import ZIP_DEFLATED, ZipFile

from app.road_evidence import BASE, NETWORK, NoRedirect, unique_json_members, reject_json_constant


PAGE_SIZE = 700
MAX_PAGES = 40
MAX_PAGE_BYTES = 12_000_000
TYPES = (105, 721, 977)
SPEED_PROPERTY = {105: 2021, 721: 7023}
EFFECTIVE_PROPERTY = {105: 5127, 721: 9400}
WKT = re.compile(r'LINESTRING(?: Z)?\s*\(([^()]+)\)')
MOTOR_FIELD = re.compile(r'([1-9][0-9]*)(?:K|[HV][1-9][0-9]*)?')


def fetch_series(archive, kind, endpoint, filters):
    rows = {}
    pages = []
    declared = None
    cursor = None
    seen_cursors = set()
    open_request = build_opener(NoRedirect()).open
    for page_number in range(MAX_PAGES):
        params = dict(filters, antall=PAGE_SIZE, inkluderAntall='true')
        if cursor is not None:
            params['start'] = cursor
        url = BASE + endpoint + '?' + urlencode(params)
        request = Request(url, headers={'Accept': 'application/json', 'X-Client': 'IBE160-Bussassistent-area-evidence'})
        with open_request(request, timeout=18) as response:
            if response.status != 200:
                raise ValueError(f'NVDB HTTP {response.status}')
            payload = response.read(MAX_PAGE_BYTES + 1)
            response_date = response.headers.get('Date')
        if len(payload) > MAX_PAGE_BYTES:
            raise ValueError('NVDB page exceeded the byte limit')
        document = json.loads(payload, object_pairs_hook=unique_json_members, parse_constant=reject_json_constant)
        metadata, objects = document['metadata'], document['objekter']
        total = metadata['antall']
        if (type(total) is not int or not 0 <= total <= PAGE_SIZE * MAX_PAGES
                or declared not in (None, total) or len(objects) != metadata['returnert']
                or len(rows) + len(objects) > total or len(objects) > PAGE_SIZE):
            raise ValueError(f'Inconsistent NVDB page counts for {kind}')
        declared = total
        for row in objects:
            key = row['referanse'] if kind == 'network' else row['id']
            if key in rows:
                raise ValueError(f'Duplicate NVDB identity in {kind}')
            rows[key] = row
        name = f'{kind}-{page_number:02}.json'
        archive.writestr(name, payload)
        pages.append({'file': name, 'url': url, 'sha256': sha256(payload).hexdigest(), 'response_date': response_date,
                      'observed_at': datetime.now(UTC).isoformat()})
        if len(rows) == declared:
            return list(rows.values()), pages
        cursor = (metadata.get('neste') or {}).get('start')
        if not objects or not isinstance(cursor, str) or not 0 < len(cursor) <= 2048 or cursor in seen_cursors:
            raise ValueError(f'Incomplete NVDB cursor series for {kind}')
        seen_cursors.add(cursor)
    raise ValueError(f'NVDB page budget exceeded for {kind}')


def by_sequence(objects, kind):
    indexed = defaultdict(list)
    for row in objects:
        metadata = row['metadata']
        properties = row['egenskaper']
        speeds = [prop.get('verdi') for prop in properties if prop['id'] == SPEED_PROPERTY.get(kind)]
        effective = [prop.get('verdi') for prop in properties if prop['id'] == EFFECTIVE_PROPERTY.get(kind)]
        for span in row['lokasjon']['stedfestinger']:
            if span['type'] != 'Linje':
                continue
            indexed[span['veglenkesekvensid']].append({
                'id': row['id'], 'version': metadata['versjon'], 'type': kind,
                'valid_from': metadata.get('startdato'), 'valid_until': metadata.get('sluttdato'),
                'start': span['startposisjon'], 'end': span['sluttposisjon'], 'orientation': span.get('retning'),
                'lanes': span.get('kjørefelt'), 'speed': speeds[0] if len(speeds) == 1 else None,
                'effective_dates': effective,
            })
    return indexed


def validity_for(record, effective_date):
    try:
        start = date.fromisoformat(record['valid_from'])
        end = date.fromisoformat(record['valid_until']) if record.get('valid_until') is not None else None
        reported_dates = record.get('effective_dates', [])
        if len(reported_dates) > 1:
            return None
        if reported_dates:
            start = max(start, date.fromisoformat(reported_dates[0]))
        if end is not None and end <= start:
            return None
    except (KeyError, TypeError, ValueError):
        return None
    return start <= effective_date and (end is None or effective_date < end)


def valid_interval(start, end):
    return all(type(value) in (int, float) for value in (start, end)) and 0 <= start < end <= 1


def overlapping_evidence(sequence, start, end, static, variable):
    return [span for span in [*static.get(sequence, ()), *variable.get(sequence, ())]
            if not valid_interval(span['start'], span['end']) or span['start'] < end and span['end'] > start]


def registered_speed(start, end, evidence, effective_date):
    intervals = []
    for row in evidence:
        valid = validity_for(row, effective_date)
        if valid is None:
            return None, 'unresolved-validity'
        if not valid:
            continue
        if not valid_interval(row['start'], row['end']):
            return None, 'invalid-placement'
        if row['type'] == 721:
            return None, 'variable-limit'
        if row['lanes'] != []:
            return None, 'field-specific'
        speed = row['speed']
        if type(speed) is not int or not 1 <= speed <= 130:
            return None, 'invalid-limit'
        low, high = max(start, row['start']), min(end, row['end'])
        if low < high:
            intervals.append((low, high, speed))
    points = sorted({start, end, *(point for low, high, _ in intervals for point in (low, high))})
    values = set()
    for low, high in zip(points, points[1:]):
        applicable = {speed for left, right, speed in intervals if left <= low and high <= right}
        if not applicable:
            return None, 'incomplete-limit'
        if len(applicable) > 1:
            return None, 'conflicting-limits'
        values.update(applicable)
    if len(values) != 1:
        return None, 'change-within-edge'
    return values.pop(), 'registered-static'


def parent_evidence(mapping, static, variable, effective_date):
    parent = mapping.get('veglenkesekvensid')
    start, end = mapping.get('startposisjon'), mapping.get('sluttposisjon')
    if type(parent) is not int or not valid_interval(start, end) or mapping.get('retning') not in ('MED', 'MOT'):
        return {'placement': mapping, 'speed_basis': 'invalid-placement', 'kmh': None, 'speed_evidence': []}
    evidence = overlapping_evidence(parent, start, end, static, variable)
    limit, basis = registered_speed(start, end, evidence, effective_date)
    return {'placement': mapping, 'speed_basis': basis, 'kmh': limit, 'speed_evidence': evidence}


def geometry_points(row):
    geometry = row.get('geometri') or {}
    if not isinstance(geometry, dict):
        return None
    wkt = geometry.get('wkt')
    match = WKT.fullmatch(wkt) if isinstance(wkt, str) else None
    if not match or geometry.get('srid') != 4326:
        return None
    try:
        points = [tuple(map(float, point.split())) for point in match[1].split(',')]
    except ValueError:
        return None
    # NVDB's EPSG:4326 WKT uses latitude, longitude, optional height.
    if (len({point[:2] for point in points}) < 2
            or any(len(point) not in (2, 3) or not 67 < point[0] < 72 or not 14 < point[1] < 24
                   or any(not isfinite(value) for value in point) for point in points)):
        return None
    return points


def lane_directions(fields):
    if not isinstance(fields, list):
        return set(), {0, 1}
    directions, uncertain = set(), False
    for field in fields:
        match = MOTOR_FIELD.fullmatch(field) if isinstance(field, str) else None
        if match:
            directions.add(int(match[1]) % 2)
        else:
            uncertain = True
    return directions, ({0, 1} if uncertain or not directions else directions)


def allowed_directions(fields, start, end, evidence, effective_date):
    known, possible = lane_directions(fields)
    placements = []
    for row in evidence:
        dated = validity_for(row, effective_date)
        if dated is False:
            continue
        if (dated is None or not valid_interval(row['start'], row['end'])
                or row['lanes'] != [] or row['orientation'] not in ('MED', 'MOT')):
            return set(), {0, 1}, 'unresolved-direction-rule'
        placements.append(row)
    if not placements:
        return known, possible, 'lane-inventory'

    directions = {int(row['orientation'] == 'MED') for row in placements}
    if len(directions) != 1 or (known and not directions <= possible):
        return set(), {0, 1}, 'unresolved-direction-rule'
    covered = start
    for row in sorted(placements, key=lambda item: (item['start'], item['end'])):
        if row['start'] > covered:
            return set(), {0, 1}, 'unresolved-direction-rule'
        covered = max(covered, row['end'])
    if covered < end:
        return set(), {0, 1}, 'unresolved-direction-rule'
    return directions, directions, 'registered-direction-rule'


def edges(rows, static, variable, bbox, effective_date, *, direction_index=None):
    recorded = []
    rejected = Counter()
    unresolved_at_node = defaultdict(set)
    for row in rows:
        key = row['referanse']
        nodes = (row.get('startnode'), row.get('sluttnode'))
        points = geometry_points(row)
        length = row.get('lengde')
        start, end = row.get('startposisjon'), row.get('sluttposisjon')
        if (points is None or not all(nodes) or type(length) not in (int, float) or not isfinite(length) or length <= 0
                or not valid_interval(start, end)):
            rejected['unresolved_geometry_or_endpoints'] += 1
            for node in filter(None, nodes):
                unresolved_at_node[node].add(key + '-unresolved')
            continue
        west, south, east, north = bbox
        if (max(p[1] for p in points) < west or min(p[1] for p in points) > east
                or max(p[0] for p in points) < south or min(p[0] for p in points) > north):
            rejected['outside_box'] += 1
            for node in nodes:
                unresolved_at_node[node].add(key + '-outside')
            continue
        sequence = row['veglenkesekvensid']
        direction_evidence = overlapping_evidence(sequence, start, end, direction_index or {}, {})
        directions, possible, direction_basis = allowed_directions(
            row.get('feltoversikt') or [], start, end, direction_evidence, effective_date,
        )
        related = overlapping_evidence(sequence, start, end, static, variable)
        if directions:
            limit, basis = registered_speed(start, end, related, effective_date)
        else:
            limit, basis = None, 'unresolved-direction'
        parent = row.get('superstedfesting')
        parent_facts = None
        if parent is not None:
            parent_facts = parent_evidence(parent if isinstance(parent, dict) else {}, static, variable, effective_date)
            if limit is not None and parent_facts['kmh'] != limit:
                basis = ('conflicting-parent-limit' if parent_facts['kmh'] is not None else
                         'parent-' + parent_facts['speed_basis'])
                limit = None
        validity = row.get('metadata') or {}
        dated = validity_for({'valid_from': validity.get('startdato'), 'valid_until': validity.get('sluttdato')},
                             effective_date) is True
        for forward in sorted(possible if dated else {0, 1}):
            direction_verified = dated and forward in directions
            source_shape = points if forward else reversed(points)
            recorded.append({
                'id': key + ('-med' if forward else '-mot'), 'reference': key, 'sequence': sequence,
                'orientation': 'MED' if forward else 'MOT', 'start': start, 'end': end,
                'from': nodes[0 if forward else 1], 'to': nodes[1 if forward else 0],
                'shape': [[lon, lat] for lat, lon, *_ in source_shape], 'length': length,
                'level': row.get('detaljnivå'), 'road_type': row.get('typeVeg_sosi'),
                'road_reference': (row.get('vegsystemreferanse') or {}).get('kortform'),
                'validity': validity, 'speed_evidence': related,
                'parent_evidence': parent_facts,
                'direction_evidence': direction_evidence, 'direction_basis': direction_basis,
                'direction_verified': direction_verified, 'kmh': limit if direction_verified else None,
                'speed_basis': ('unresolved-network-validity' if not dated else
                                basis if direction_verified else 'unresolved-direction'),
            })
    outgoing = defaultdict(list)
    for edge in recorded:
        outgoing[edge['from']].append(edge)
    for edge in recorded:
        destination = edge['to']
        edge['unresolved_at_start'] = bool(unresolved_at_node.get(edge['from']))
        edge['successors'] = sorted(unresolved_at_node[destination] | {
            item['id'] for item in outgoing[destination]
            if item['reference'] != edge['reference'] or item['id'] == edge['id']
        })
    return recorded, rejected


def collect_area(day, box, output):
    bounds = {'kommune': 5501, 'kartutsnitt': ','.join(map(str, box)), 'srid': 4326,
              'tidspunkt': day.isoformat()}
    with ZipFile(output, 'x', compression=ZIP_DEFLATED) as archive:
        roads, pages = fetch_series(archive, 'network', NETWORK, dict(bounds, trafikantgruppe='K'))
        objects = {}
        for kind in TYPES:
            values, receipt = fetch_series(archive, str(kind), f'/vegobjekter/api/v4/vegobjekter/{kind}',
                                           dict(bounds, inkluder='egenskaper,metadata,lokasjon'))
            objects[kind] = values
            pages.extend(receipt)
        graph, rejected = edges(roads, by_sequence(objects[105], 105), by_sequence(objects[721], 721),
                                box, day, direction_index=by_sequence(objects[977], 977))
        report = {'status': 'research', 'effective_date': day.isoformat(), 'requested_box': box,
                  'network_rows': len(roads), 'directed_edges': len(graph), 'rejected': rejected,
                  'speed_basis': Counter(edge['speed_basis'] for edge in graph),
                  'object_counts': {kind: len(objects[kind]) for kind in TYPES}}
        archive.writestr('directed-edges.json', json.dumps(graph, ensure_ascii=False, allow_nan=False))
        archive.writestr('receipt.json', json.dumps({**report, 'pages': pages}, indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', required=True, type=date.fromisoformat)
    parser.add_argument('--box', nargs=4, type=float, default=[18.70, 69.59, 19.14, 69.77],
                        metavar=('WEST', 'SOUTH', 'EAST', 'NORTH'))
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    west, south, east, north = args.box
    if not 18 < west < east < 20 or not 69 < south < north < 70:
        parser.error('Expected a bounded box in Tromsø')
    print(json.dumps(collect_area(args.date, args.box, args.output), indent=2))


if __name__ == '__main__':
    main()
