"""Verify and publish public, dated Tromsø road areas from offline NVDB receipts."""

import argparse
from collections import defaultdict
from datetime import UTC, date, datetime, time, timedelta
from hashlib import sha256
from io import BytesIO
import json
from math import isfinite
from pathlib import Path
import sys
from urllib.parse import parse_qs, urlsplit
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile
from zoneinfo import ZoneInfo

from .road_area_evidence import (
    BASE, NETWORK, MAX_PAGE_BYTES, MAX_PAGES, PAGE_SIZE, TYPES,
    by_sequence, edges, reject_json_constant, unique_json_members,
)
from .road_situation_source import bounds as geometry_bounds, road_number

BOX = [18.70, 69.59, 19.14, 69.77]
AREAS = {'kvaloya': (18.70, 18.93), 'tromsoya': (18.86, 19.05), 'fastlandet': (18.92, 19.14)}
OSLO = ZoneInfo('Europe/Oslo')
MAX_ARCHIVE = 20_000_000
MAX_UNCOMPRESSED = 160_000_000
MAX_REVIEW = 5_000_000


def read_bounded(path, limit):
    with Path(path).open('rb') as stream:
        return read_stream(stream, limit)


def read_stream(stream, limit):
    raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise ValueError('Public road input exceeds its byte limit')
    return raw


def document(raw):
    return json.loads(raw, object_pairs_hook=unique_json_members, parse_constant=reject_json_constant)


def utc_stamp(value):
    stamp = datetime.fromisoformat(value)
    if stamp.utcoffset() != timedelta(0):
        raise ValueError('Public road timestamps require UTC')
    return stamp


def source_member(archive, page):
    raw = archive.read(page['file'])
    if sha256(raw).hexdigest() != page['sha256']:
        raise ValueError('NVDB page checksum mismatch')
    return document(raw)


def read_series(archive, pages, kind, day):
    endpoint = NETWORK if kind == 'network' else f'/vegobjekter/api/v4/vegobjekter/{kind}'
    filters = {
        'kommune': ['5501'], 'kartutsnitt': [','.join(map(str, BOX))], 'srid': ['4326'],
        'tidspunkt': [day.isoformat()], 'antall': [str(PAGE_SIZE)], 'inkluderAntall': ['true'],
    }
    filters.update({'trafikantgruppe': ['K']} if kind == 'network'
                   else {'inkluder': ['egenskaper,metadata,lokasjon']})
    if not 1 <= len(pages) <= MAX_PAGES:
        raise ValueError(f'Missing or oversized NVDB series for {kind}')
    rows, cursors = {}, set()
    total, cursor = None, None
    for number, page in enumerate(pages):
        uri = urlsplit(page['url'])
        expected = filters if number == 0 else {**filters, 'start': [cursor]}
        if (page['file'] != f'{kind}-{number:02}.json' or f'{uri.scheme}://{uri.netloc}' != BASE
                or uri.path != endpoint or uri.fragment or parse_qs(uri.query, keep_blank_values=True) != expected):
            raise ValueError(f'Wrong NVDB query or cursor for {kind}')
        response = source_member(archive, page)
        metadata, objects = response['metadata'], response['objekter']
        count = metadata['antall']
        if (type(count) is not int or not 0 <= count <= PAGE_SIZE * MAX_PAGES or total not in (None, count)
                or len(objects) != metadata['returnert'] or len(objects) > PAGE_SIZE or len(rows) + len(objects) > count):
            raise ValueError(f'Inconsistent NVDB counts for {kind}')
        total = count
        for row in objects:
            identifier = row['referanse' if kind == 'network' else 'id']
            if identifier in rows:
                raise ValueError(f'Duplicate NVDB record in {kind}')
            rows[identifier] = row
        if len(rows) == total:
            if number != len(pages) - 1:
                raise ValueError(f'Unexpected extra NVDB pages for {kind}')
            return list(rows.values())
        cursor = (metadata.get('neste') or {}).get('start')
        if not objects or not isinstance(cursor, str) or not 0 < len(cursor) <= 2048 or cursor in cursors:
            raise ValueError(f'Invalid NVDB cursor in {kind}')
        cursors.add(cursor)
    raise ValueError(f'Incomplete NVDB series for {kind}')


def read_source(raw, now):
    with ZipFile(BytesIO(raw)) as archive:
        inventory = archive.infolist()
        names = {entry.filename for entry in inventory}
        if (len(names) != len(inventory) or len(names) > 2 + MAX_PAGES * (1 + len(TYPES))
                or sum(entry.file_size for entry in inventory) > MAX_UNCOMPRESSED
                or any(entry.flag_bits & 1 or entry.compress_type not in (ZIP_STORED, ZIP_DEFLATED)
                       or entry.file_size > (90_000_000 if entry.filename == 'directed-edges.json' else MAX_PAGE_BYTES)
                       for entry in inventory)):
            raise ValueError('Unexpected NVDB archive inventory')
        receipt = document(archive.read('receipt.json'))
        day = date.fromisoformat(receipt['effective_date'])
        pages = receipt['pages']
        members = {page['file'] for page in pages}
        if (receipt['status'] != 'research' or receipt['requested_box'] != BOX or len(members) != len(pages)
                or members | {'receipt.json', 'directed-edges.json'} != names
                or members & {'receipt.json', 'directed-edges.json'}):
            raise ValueError('NVDB archive must cover the full Tromsø box')
        observations = sorted(utc_stamp(page['observed_at']) for page in pages)
        if not observations or observations[-1] > now or observations[-1] - observations[0] > timedelta(hours=1):
            raise ValueError('Inconsistent NVDB observation times')
        series = {}
        for kind in ('network', *map(str, TYPES)):
            series[kind] = read_series(archive, [p for p in pages if p['file'].startswith(kind + '-')], kind, day)
        if sum(len([p for p in pages if p['file'].startswith(kind + '-')]) for kind in series) != len(pages):
            raise ValueError('Unexpected source receipt member')
        graph, _ = edges(series['network'], by_sequence(series['105'], 105), by_sequence(series['721'], 721),
                         BOX, day, direction_index=by_sequence(series['977'], 977))
    return day, observations[0], observations[-1], graph, pages


def approved_limits(review, digest, day, last_observation, next_day, now, graph):
    if review is None:
        return last_observation, next_day, {}, {}
    if review['source_sha256'] != digest or review['effective_date'] != day.isoformat():
        raise ValueError('Road review must identify the exact NVDB archive and date')
    checked = utc_stamp(review['checked_at'])
    until = utc_stamp(review['valid_until'])
    if not last_observation <= checked <= now or not checked < until <= next_day or until - checked > timedelta(days=1):
        raise ValueError('Road review must establish a bounded observation window')
    if not isinstance(review['limits'], dict) or not review['limits']:
        raise ValueError('Road review must include at least one limit')
    candidates = {edge['id']: edge for edge in graph}
    values = {}
    for identifier, decision in review['limits'].items():
        edge = candidates.get(identifier)
        value, basis, evidence = decision['kmh'], decision['basis'], decision['evidence']
        if (not edge or not edge['direction_verified'] or type(value) is not int or not 1 <= value <= 130
                or not isinstance(evidence, str) or not evidence.strip() or len(evidence) > 1500
                or basis not in ('registered', 'urban-default', 'temporary', 'sign')
                or basis == 'registered' and edge['kmh'] != value
                or basis == 'urban-default' and (value != 50 or edge['speed_basis'] != 'incomplete-limit'
                                                or edge['speed_evidence'] or edge['parent_evidence'] is not None)):
            raise ValueError(f'Unsupported road limit decision for {identifier}')
        if basis == 'temporary':
            restriction = decision.get('restriction')
            if not isinstance(restriction, dict) or restriction.get('segment') != identifier:
                raise ValueError(f'Temporary road limit lacks exact directional placement: {identifier}')
            start, end = (utc_stamp(restriction[key]) for key in ('starts_at', 'ends_at'))
            records = restriction.get('record_revisions', {})
            if (not start < end or not start < until or not checked < end or not isinstance(records, dict)
                    or len(records) > 25 or any(not isinstance(key, str) or not 0 < len(key) <= 180 or not key.isprintable()
                                                or not isinstance(value, str) or len(value) != 64
                                                or any(character not in '0123456789abcdef' for character in value)
                                                for key, value in records.items())):
                raise ValueError(f'Temporary road limit lacks exact validity or a known record: {identifier}')
        values[identifier] = value
    changes = {}
    transitions = review.get('transitions', {})
    if not isinstance(transitions, dict):
        raise ValueError('Road review transitions must be keyed by source and destination edge')
    for origin, destinations in transitions.items():
        if origin not in values or not isinstance(destinations, dict) or not destinations:
            raise ValueError(f'Unsupported road transition from {origin}')
        for destination, evidence in destinations.items():
            if (destination not in values or destination not in candidates[origin]['successors']
                    or values[origin] == values[destination] or not isinstance(evidence, str)
                    or not evidence.strip() or len(evidence) > 1500):
                raise ValueError(f'Unsupported road transition from {origin} to {destination}')
        changes[origin] = sorted(destinations)
    return checked, until, values, changes


def registered_interiors(graph):
    directed = {edge['id']: edge for edge in graph}
    incoming = defaultdict(list)
    for edge in graph:
        for successor in edge['successors']:
            incoming[successor].append(edge['id'])
    result = {}
    for identifier, edge in directed.items():
        value = edge['kmh']
        predecessors, successors = incoming[identifier], edge['successors']
        road = road_number(edge['road_reference'])
        if (edge['speed_basis'] == 'registered-static' and value is not None and not edge['unresolved_at_start']
                and len(predecessors) == len(successors) == 1 and road is not None
                and all(other in directed and directed[other]['speed_basis'] == 'registered-static'
                        and directed[other]['kmh'] == value and road_number(directed[other]['road_reference']) == road
                        for other in (*predecessors, *successors))):
            result[identifier] = value
    return result


def prepare(archive_path, review_path=None, *, now=None):
    raw = read_bounded(archive_path, MAX_ARCHIVE)
    review_bytes = read_bounded(review_path, MAX_REVIEW) if review_path is not None else b''
    if review_path is not None and not review_bytes:
        raise ValueError('A road review must contain JSON')
    return prepare_bytes(raw, review_bytes, now=now)


def prepare_bundle(stream):
    maximum = MAX_ARCHIVE + MAX_REVIEW + 4096
    with ZipFile(BytesIO(read_stream(stream, maximum))) as archive:
        entries = archive.infolist()
        sizes = {'nvdb.zip': MAX_ARCHIVE, 'review.json': MAX_REVIEW}
        names = {entry.filename for entry in entries}
        if (names not in ({'nvdb.zip'}, {'nvdb.zip', 'review.json'}) or len(names) != len(entries)
                or any(entry.flag_bits & 1 or entry.compress_type not in (ZIP_STORED, ZIP_DEFLATED)
                       or not 0 < entry.file_size <= sizes[entry.filename] for entry in entries)):
            raise ValueError('Road bundle must contain nvdb.zip and optionally review.json')
        return prepare_bytes(archive.read('nvdb.zip'), archive.read('review.json') if 'review.json' in names else b'')


def prepare_bytes(raw, review_bytes, *, now=None):
    now = datetime.now(UTC) if now is None else now
    review = document(review_bytes) if review_bytes else None
    if review_bytes and not isinstance(review, dict):
        raise ValueError('A road review must be a JSON object')
    digest = sha256(raw).hexdigest()
    day, observed, last_observation, graph, pages = read_source(raw, now)
    start_day = datetime.combine(day, time(), OSLO).astimezone(UTC)
    next_day = datetime.combine(day + timedelta(days=1), time(), OSLO).astimezone(UTC)
    checked, until, values, changes = approved_limits(review, digest, day, last_observation, next_day, now, graph)
    if until <= start_day:
        raise ValueError('Road review must cover part of the effective Oslo date')
    revision = sha256(digest.encode() + review_bytes).hexdigest()
    source = {'sha256': digest, 'revision': revision, 'date': day.isoformat(), 'box': BOX,
              'pages': pages, 'review': review}
    registered = registered_interiors(graph)
    result = {}
    for area, (west, east) in AREAS.items():
        usable = []
        boundaries = set()
        for edge in graph:
            shape = edge['shape']
            if max(point[0] for point in shape) < west or min(point[0] for point in shape) > east:
                continue
            if (not 2 <= len(shape) <= 1024 or not isfinite(edge['length']) or not 0 < edge['length'] <= 100_000
                    or len(edge['successors']) > 32):
                raise ValueError(f'NVDB area edge exceeds the supported geometry limits: {edge["id"]}')
            item = {'id': edge['id'], 'from': str(edge['from']), 'to': str(edge['to']),
                    'length': edge['length'], 'shape': shape, 'kmh': values.get(edge['id']),
                    'successors': edge['successors'], 'roadReference': edge['road_reference']}
            if edge['id'] in registered:
                item['registeredKmh'] = registered[edge['id']]
            if edge['id'] in changes:
                item['confirmedTransitions'] = changes[edge['id']]
            decision = review['limits'].get(edge['id']) if review else None
            if decision and decision['basis'] == 'temporary':
                restriction = decision['restriction']
                starts, ends = (utc_stamp(restriction[key]).isoformat() for key in ('starts_at', 'ends_at'))
                item['temporaryRestriction'] = {'start': starts, 'end': ends,
                                                'records': restriction.get('record_revisions', {})}
                boundaries.update((starts, ends))
            usable.append(item)
        if not usable or len(usable) > 20_000 or sum(len(edge['shape']) for edge in usable) > 350_000:
            raise ValueError(f'NVDB graph falls outside the road area budget for {area}')
        result[area] = {
            'id': area, 'revision': revision, 'checkedAt': checked.isoformat(), 'retrievedAt': observed.isoformat(),
            'validFrom': start_day.isoformat(), 'validUntil': until.isoformat(),
            'uncertaintyM': 10, 'profile': 'NVDB-AREA-1', 'path': [],
            'roadNumbers': sorted({number for edge in usable if (number := road_number(edge['roadReference']))}),
            'situationBounds': geometry_bounds(point for edge in usable for point in edge['shape']),
            'temporaryBoundaries': sorted(boundaries),
            'registeredInteriors': any('registeredKmh' in edge for edge in usable),
            'packages': [{'id': area, 'revision': revision, 'edges': usable}],
        }
    return day, observed, checked, source, result


def publish(day, observed, checked, source, areas):
    from psycopg.types.json import Jsonb
    from .private_storage import database

    with database() as conn:
        for area, manifest in areas.items():
            row = conn.execute(
                '''INSERT INTO public_road_area_versions VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (effective_date, area_id, observed_at, checked_at) DO UPDATE
                       SET source = EXCLUDED.source, manifest = EXCLUDED.manifest
                       WHERE public_road_area_versions.revision = EXCLUDED.revision
                   RETURNING revision''',
                (day, area, observed, checked, source['sha256'], source['revision'], Jsonb(source), Jsonb(manifest)),
            ).fetchone()
            if row is None:
                raise ValueError(f'Conflicting public road archive or review for {day} / {area}')


def current_day_ready(now):
    from .private_storage import database

    local = now.astimezone(OSLO)
    day = local.date()
    midnight = datetime.combine(day, time(), OSLO)
    with database() as conn:
        row = conn.execute("""SELECT count(DISTINCT area_id) AS areas FROM public_road_area_versions
                               WHERE effective_date=%s AND observed_at >= %s AND observed_at <= %s
                                 AND manifest ? 'registeredInteriors'""", (day, midnight, now)).fetchone()
    return row['areas'] == len(AREAS)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path, nargs='?')
    parser.add_argument('--review', type=Path)
    parser.add_argument('--bundle-stdin', action='store_true')
    parser.add_argument('--ready-day', action='store_true')
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    if args.ready_day:
        print(json.dumps({'ready': current_day_ready(datetime.now(UTC))}))
        return
    if args.bundle_stdin:
        if args.archive or args.review:
            parser.error('Use --bundle-stdin without archive paths')
        prepared = prepare_bundle(sys.stdin.buffer)
    else:
        if not args.archive:
            parser.error('Supply an archive path or --bundle-stdin')
        prepared = prepare(args.archive, args.review)
    if args.publish:
        publish(*prepared)
    day, _, _, source, areas = prepared
    print(json.dumps({'date': day.isoformat(), 'revision': source['revision'], 'published': args.publish,
                      'areas': {area: {'edges': len(manifest['packages'][0]['edges']),
                                       'confirmed': sum(edge['kmh'] is not None for edge in manifest['packages'][0]['edges'])}
                                for area, manifest in areas.items()}}, indent=2))


if __name__ == '__main__':
    main()
