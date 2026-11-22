"""Audit an ordered corridor against an offline NVDB research archive."""

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from datetime import date, datetime
from decimal import Decimal, DecimalException
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
from urllib.parse import parse_qsl, urlsplit
from zipfile import BadZipFile, ZipFile
from zlib import error as ZlibError

from . import road_evidence as evidence


InvalidEvidence = evidence.IncompleteEvidence
SERIES = {'network', *(str(type_id) for type_id in evidence.OBJECT_TYPES)}
ENVELOPE_BYTES = 100_000
PAGE_NAME = re.compile(r'(network|[0-9]+)-(0|[1-9][0-9]?)\.json')
LINESTRING = re.compile(r'LINESTRING(?:\s+(Z))?\s*\(([^()]*)\)')
COORDINATE = re.compile(r'[-+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][-+]?[0-9]+)?')


def decode(raw):
    return json.loads(raw, parse_float=Decimal, object_pairs_hook=evidence.unique_json_members,
                      parse_constant=evidence.reject_json_constant)


def bounded_read(stream, limit):
    raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise InvalidEvidence('Input exceeds the audit byte limit')
    return raw


def known_scope(receipt):
    municipality, effective_date = receipt.get('municipality'), receipt.get('effective_date')
    if not isinstance(effective_date, str) or date.fromisoformat(effective_date).isoformat() != effective_date:
        raise InvalidEvidence('Invalid archive effective date')
    if not isinstance(municipality, str) or not re.fullmatch(r'[0-9]{4}', municipality):
        raise InvalidEvidence('Invalid archive municipality')
    return {'kommune': municipality, 'tidspunkt': effective_date, 'antall': str(evidence.PAGE_SIZE),
            'inkluderAntall': 'true', 'veglenkesekvens': ','.join(map(str, sorted(receipt['sequences'])))}


def check_request_url(url, series, scope, cursor):
    if not isinstance(url, str):
        raise InvalidEvidence('Missing archived NVDB request URL')
    parsed = urlsplit(url)
    if series == 'network':
        path = evidence.NETWORK
        filters = dict(scope, srid=str(evidence.SRID), trafikantgruppe='K')
    else:
        path = f'/vegobjekter/api/v4/vegobjekter/{series}'
        filters = dict(scope, inkluder='egenskaper,metadata,lokasjon')
    if cursor is not None:
        filters['start'] = cursor
    if (f'{parsed.scheme}://{parsed.netloc}' != evidence.BASE or parsed.path != path or parsed.fragment
            or sorted(parse_qsl(parsed.query, strict_parsing=True)) != sorted(filters.items())):
        raise InvalidEvidence(f'Archive request does not match the declared scope for {series}')


def archive_rows(raw):
    with ZipFile(BytesIO(raw)) as archive:
        names = archive.namelist()
        if not 2 <= len(names) <= evidence.MAX_ATTEMPTS + 1 or len(set(names)) != len(names) or 'receipt.json' not in names:
            raise InvalidEvidence('Invalid research archive member list')
        with archive.open('receipt.json') as stream:
            receipt = decode(bounded_read(stream, ENVELOPE_BYTES))
        if (not isinstance(receipt, dict) or receipt.get('format') != 'nvdb-v4-road-evidence'
                or type(receipt.get('version')) is not int or receipt['version'] != 1 or receipt.get('status') != 'research'
                or receipt.get('srid') != evidence.SRID):
            raise InvalidEvidence('Expected an NVDB version 1 research archive in the collector CRS')
        pages, counts, selected = receipt.get('pages'), receipt.get('counts'), receipt.get('sequences')
        if not isinstance(pages, list) or len(pages) != len(names) - 1:
            raise InvalidEvidence('Receipt pages and archive members disagree')
        if (not isinstance(counts, dict) or set(counts) != SERIES
                or any(type(count) is not int or count < 0 for count in counts.values())
                or counts['network'] > evidence.MAX_SEGMENTS or counts['105'] > evidence.MAX_LIMITS):
            raise InvalidEvidence('Invalid archive series counts')
        if (not isinstance(selected, list) or not 1 <= len(selected) <= evidence.MAX_SEGMENTS
                or any(type(sequence) is not int or sequence < 1 for sequence in selected)
                or len(set(selected)) != len(selected)):
            raise InvalidEvidence('Invalid archive sequence scope')
        selected = set(selected)
        scope = known_scope(receipt)
        returned = set()
        collected = defaultdict(list)
        identities = defaultdict(set)
        next_page = Counter()
        cursors = {}
        seen_cursors = defaultdict(set)
        completed = set()
        remaining = set(names) - {'receipt.json'}
        observed = []
        total = 0
        for page in pages:
            if not isinstance(page, dict) or not isinstance(page.get('file'), str):
                raise InvalidEvidence('Invalid archive page receipt')
            name = page['file']
            match = PAGE_NAME.fullmatch(name)
            if not match or match[1] not in SERIES or name not in remaining or int(match[2]) != next_page[match[1]]:
                raise InvalidEvidence(f'Unexpected archive page {name}')
            series = match[1]
            if series in completed:
                raise InvalidEvidence(f'Archive page follows a terminal page for {series}')
            cursor_in = cursors.get(series)
            check_request_url(page.get('url'), series, scope, cursor_in)
            stamp = page.get('observed_at')
            observation = datetime.fromisoformat(stamp) if isinstance(stamp, str) else None
            if observation is None or observation.utcoffset() is None:
                raise InvalidEvidence(f'Missing zoned observation time for {name}')
            observed.append(observation)
            remaining.remove(name)
            next_page[series] += 1
            with archive.open(name) as stream:
                body = bounded_read(stream, min(evidence.MAX_PAGE_BYTES, evidence.MAX_TOTAL_BYTES - total))
            total += len(body)
            if len(body) != page.get('bytes') or sha256(body).hexdigest() != page.get('sha256'):
                raise InvalidEvidence(f'Archive page hash or byte tally mismatch for {name}')
            document = decode(body)
            metadata = document.get('metadata') if isinstance(document, dict) else None
            rows = document.get('objekter') if isinstance(document, dict) else None
            if (not isinstance(metadata, dict) or not isinstance(rows, list) or len(rows) > evidence.PAGE_SIZE
                    or type(metadata.get('returnert')) is not int or metadata['returnert'] != len(rows)
                    or type(metadata.get('antall')) is not int or metadata['antall'] != counts[series]
                    or len(collected[series]) + len(rows) > counts[series]):
                raise InvalidEvidence(f'Invalid archive page counts for {name}')
            for row in rows:
                if not isinstance(row, dict):
                    raise InvalidEvidence(f'Invalid archive row in {name}')
                identity = (evidence.network_reference(row, selected, returned) if series == 'network'
                            else evidence.object_reference(row, int(series), selected))
                if identity in identities[series]:
                    raise InvalidEvidence(f'Duplicate row in {name}')
                identities[series].add(identity)
            collected[series].extend(rows)
            cursor_out = evidence.page_cursor(metadata, name)
            if not rows or cursor_out is None:
                if len(collected[series]) != counts[series] or cursor_out not in (None, cursor_in or '0:0'):
                    raise InvalidEvidence(f'Invalid terminal archive page for {series}')
                completed.add(series)
            else:
                if cursor_out in seen_cursors[series]:
                    raise InvalidEvidence(f'Repeated archive cursor for {series}')
                seen_cursors[series].add(cursor_out)
                cursors[series] = cursor_out
        if (completed != SERIES or total != receipt.get('raw_bytes')
                or receipt.get('missing_network_sequences') != sorted(selected - returned)):
            raise InvalidEvidence('Incomplete archive series')
        return receipt, collected['network'], collected['105'], (min(observed), max(observed))


def decimal_number(value):
    if type(value) not in (Decimal, int):
        raise InvalidEvidence('Expected a numeric position or length')
    result = Decimal(value)
    if not result.is_finite():
        raise InvalidEvidence('Non-finite position or length')
    return result


@dataclass(frozen=True)
class Span:
    link: int
    start: Decimal
    end: Decimal
    from_node: str
    to_node: str
    intermediate: tuple = ()

    def __post_init__(self):
        if not 0 <= self.start < self.end <= 1 or type(self.link) is not int or self.link < 1:
            raise InvalidEvidence('Invalid directed sequence interval')
        if any(not isinstance(node, str) or not node for node in (self.from_node, self.to_node)):
            raise InvalidEvidence('Missing corridor node identity')


def scope_spans(scope):
    rows = scope.get('segments') if isinstance(scope, dict) else None
    if not isinstance(rows, list) or not 1 <= len(rows) <= evidence.MAX_SEGMENTS:
        raise InvalidEvidence('Expected a bounded ordered scope in segments')
    spans = []
    for occurrence, row in enumerate(rows, 1):
        if not isinstance(row, dict) or row.get('occurrence') != occurrence:
            raise InvalidEvidence('Unordered scope occurrence')
        piece = Span(row.get('link'), decimal_number(row.get('start')), decimal_number(row.get('end')),
                     row.get('from_node'), row.get('to_node'))
        if spans:
            previous = spans[-1]
            if previous.to_node != piece.from_node:
                raise InvalidEvidence(f'Scope node continuity failed at occurrence {occurrence}')
            if previous.link == piece.link:
                if previous.end == piece.start:
                    intermediate = previous.intermediate + ((previous.end, previous.to_node),)
                    spans[-1] = replace(previous, end=piece.end, to_node=piece.to_node, intermediate=intermediate)
                    continue
                if previous.end != 1 or piece.start != 0:
                    raise InvalidEvidence(f'Scope sequence continuity failed at occurrence {occurrence}')
        spans.append(piece)
    return spans


def resolved_spans(spans, network):
    edges = defaultdict(list)
    for row in network:
        edge = Span(row['veglenkesekvensid'], decimal_number(row.get('startposisjon')),
                    decimal_number(row.get('sluttposisjon')), row.get('startnode'), row.get('sluttnode'))
        edges[edge.link].append((edge, row))
    for number, scope in enumerate(spans, 1):
        candidates = sorted(((edge, row) for edge, row in edges[scope.link]
                             if edge.start < scope.end and edge.end > scope.start), key=lambda candidate: candidate[0].start)
        position, node = scope.start, scope.from_node
        for edge, row in candidates:
            if edge.start != position or edge.from_node != node or edge.end > scope.end:
                raise InvalidEvidence(f'Archive gap, overlap or node mismatch at span {number} (sequence {scope.link})')
            position, node = edge.end, edge.to_node
        if position != scope.end or node != scope.to_node:
            raise InvalidEvidence(f'Archive endpoint mismatch at span {number} (sequence {scope.link})')
        yield scope, candidates


def speed_locations(limits):
    by_link = defaultdict(list)
    for row in limits:
        properties = row.get('egenskaper')
        if not isinstance(properties, list):
            raise InvalidEvidence('Missing speed-limit properties')
        values = [field.get('verdi') for field in properties if isinstance(field, dict) and field.get('id') == 2021]
        if len(values) != 1 or type(values[0]) is not int or values[0] < 1:
            raise InvalidEvidence(f'Invalid registered speed value for object {row["id"]}')
        for location in row['lokasjon']['stedfestinger']:
            if not isinstance(location, dict) or location.get('type') != 'Linje':
                raise InvalidEvidence(f'Unsupported location for speed object {row["id"]}')
            link = location.get('veglenkesekvensid')
            start, end = decimal_number(location.get('startposisjon')), decimal_number(location.get('sluttposisjon'))
            fields = location.get('kjørefelt')
            if (type(link) is not int or link < 1 or not 0 <= start < end <= 1 or not isinstance(fields, list)
                    or any(not isinstance(field, str) or not field for field in fields)):
                raise InvalidEvidence(f'Invalid placement for speed object {row["id"]}')
            by_link[link].append((start, end, {'id': row['id'], 'version': row['metadata']['versjon'],
                                              'kmh': values[0], 'fields': fields, 'orientation': location.get('retning')}))
    return by_link


def coverage(edge, placements):
    events = defaultdict(Counter, {edge.start: Counter(), edge.end: Counter()})
    records = []
    for start, end, registered in placements:
        lo, hi = max(start, edge.start), min(end, edge.end)
        if lo >= hi:
            continue
        records.append(dict(registered, source_start=str(start), source_end=str(end), start=str(lo), end=str(hi)))
        if not registered['fields']:
            events[lo][registered['kmh']] += 1
            events[hi][registered['kmh']] -= 1
    current = Counter()
    intervals = []
    gap = conflict = False
    boundaries = sorted(events)
    for point, end in zip(boundaries, boundaries[1:]):
        current += events[point]
        gap |= not current
        conflict |= len(current) > 1
        intervals.append({'start': str(point), 'end': str(end), 'values_kmh': sorted(current)})
    return {'direct_gap': gap, 'direct_conflict': conflict, 'direct_intervals': intervals, 'records': records}


def valid_linestring(value):
    match = LINESTRING.fullmatch(value.strip()) if isinstance(value, str) else None
    if not match:
        return False
    points = match[2].split(',')
    dimensions = 3 if match[1] else 2
    if len(points) < 2:
        return False
    try:
        for point in points:
            coordinates = point.split()
            if len(coordinates) != dimensions or any(not COORDINATE.fullmatch(coordinate)
                                                       or not Decimal(coordinate).is_finite() for coordinate in coordinates):
                return False
    except DecimalException:
        return False
    return True


def dated_geometry(row, srid):
    geometry, metadata, lanes = row.get('geometri'), row.get('metadata'), row.get('feltoversikt')
    start_date = metadata.get('startdato') if isinstance(metadata, dict) else None
    if (not isinstance(geometry, dict) or type(geometry.get('srid')) is not int or geometry['srid'] != srid
            or not valid_linestring(geometry.get('wkt')) or not isinstance(lanes, list)
            or not isinstance(start_date, str) or date.fromisoformat(start_date).isoformat() != start_date):
        raise InvalidEvidence(f'Incomplete geometry or metadata for {row["referanse"]}')
    return geometry, metadata, lanes


def audit(archive_raw, scope_raw):
    receipt, network, limits, observations = archive_rows(archive_raw)
    spans = scope_spans(decode(scope_raw))
    locations = speed_locations(limits)
    length = Decimal(0)
    segments = []
    previous_nodes = []
    for span_number, (scope, candidates) in enumerate(resolved_spans(spans, network), 1):
        current_nodes = {edge.end: edge.to_node for edge, _ in candidates}
        for position, node in scope.intermediate:
            current = current_nodes.get(position)
            previous_nodes.append({'span': span_number, 'sequence': scope.link, 'position': str(position),
                                   'scope_node': node, 'archive_node': current})
        for edge, row in candidates:
            if len(segments) == evidence.MAX_SEGMENTS:
                raise InvalidEvidence('Expanded corridor exceeds segment budget')
            distance = decimal_number(row.get('lengde'))
            if distance <= 0:
                raise InvalidEvidence(f'Invalid source length for {row["referanse"]}')
            geometry, metadata, lanes = dated_geometry(row, receipt['srid'])
            segments.append({'occurrence': len(segments) + 1, 'reference': row['referanse'], 'sequence': edge.link,
                             'start': str(edge.start), 'end': str(edge.end), 'from_node': edge.from_node,
                             'to_node': edge.to_node, 'length_m': str(distance), 'chainage_m': str(length),
                             'geometry': geometry, 'source_metadata': metadata, 'fields': lanes,
                             'speed': coverage(edge, locations[edge.link])})
            length += distance
    direct = sum(not row['speed']['direct_gap'] and not row['speed']['direct_conflict'] for row in segments)
    return {'format': 'nvdb-v4-corridor-audit', 'version': 1, 'status': 'research',
            'archive_sha256': sha256(archive_raw).hexdigest(), 'scope_sha256': sha256(scope_raw).hexdigest(),
            'effective_date': receipt['effective_date'], 'srid': receipt['srid'], 'municipality': receipt['municipality'],
            'archive_sequences': receipt['sequences'], 'archive_observed_from': observations[0].isoformat(),
            'archive_observed_through': observations[1].isoformat(), 'scope_intermediate_nodes': previous_nodes,
            'spans': len(spans), 'length_m': str(length), 'direct_general_segments': direct, 'segments': segments}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--scope', type=Path, required=True)
    args = parser.parse_args()
    try:
        with args.archive.open('rb') as stream:
            archive_raw = bounded_read(stream, evidence.MAX_TOTAL_BYTES + ENVELOPE_BYTES)
        with args.scope.open('rb') as stream:
            scope_raw = bounded_read(stream, 2_000_000)
        report = audit(archive_raw, scope_raw)
        rendered = json.dumps(report, indent=2, default=str, allow_nan=False)
    except (ValueError, OSError, BadZipFile, RuntimeError, DecimalException, ZlibError) as error:
        parser.exit(1, f'Corridor audit incomplete: {error}\n')
    print(rendered)


if __name__ == '__main__':
    main()
