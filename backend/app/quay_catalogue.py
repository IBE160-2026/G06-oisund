"""Extract public Quay versions without inferring dates from publication time."""

from datetime import datetime
from hashlib import sha256
from io import BytesIO
from math import isfinite
from pathlib import Path
import re
from xml.etree import ElementTree as XML
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile
from zoneinfo import ZoneInfo

from . import route_source as netex

SOURCE_URL = 'https://storage.googleapis.com/marduk-production/tiamat/55_Troms_latest.zip'
FUTURE_SOURCE_URL = 'https://storage.googleapis.com/marduk-production/tiamat/CurrentAndFuture_latest.zip'
FUTURE_SCOPE = 'current-and-future'
MAX_ARCHIVE_BYTES = 60_000_000
OSLO = ZoneInfo('Europe/Oslo')
STOP_PLACE = f'{{{netex.NS[""]}}}StopPlace'
PUBLICATION = f'{{{netex.NS[""]}}}PublicationTimestamp'
DELIVERY = f'{{{netex.NS[""]}}}PublicationDelivery'
VALID_BETWEEN = f'{{{netex.NS[""]}}}ValidBetween'
CONDITION_TAGS = ('ValidBetween', 'ValidityCondition', 'AvailabilityCondition', 'validityConditions')


def validity(node):
    intervals = netex.children(node, 'ValidBetween')
    if len(intervals) != 1:
        return {}
    return {'valid_from': netex.field(intervals[0], 'FromDate'),
            'valid_until': netex.field(intervals[0], 'ToDate')}


def zoned(value):
    if value is None or 'T' not in value:
        return None
    try:
        stamp = datetime.fromisoformat(value)
    except ValueError:
        return None
    if stamp.tzinfo is None:
        local = stamp.replace(tzinfo=OSLO)
        if local.utcoffset() != local.replace(fold=1).utcoffset():
            return None
        stamp = local
    return stamp.isoformat()


def dated_interval(node):
    direct = [child for name in CONDITION_TAGS[:-1] for child in netex.children(node, name)]
    wrapped = netex.children(node, 'validityConditions')
    intervals = list(wrapped[0]) if len(wrapped) == 1 and not direct else direct if not wrapped else []
    if len(intervals) != 1 or intervals[0].tag != VALID_BETWEEN:
        return {}
    starts, ends = (netex.children(intervals[0], name) for name in ('FromDate', 'ToDate'))
    if len(starts) != 1 or len(ends) > 1:
        return {}
    start = zoned((starts[0].text or '').strip())
    end = zoned((ends[0].text or '').strip()) if ends else None
    if start is None or ends and end is None:
        return {}
    if end is not None and datetime.fromisoformat(start) >= datetime.fromisoformat(end):
        return {}
    return {'valid_from': start, 'valid_until': end}


class SourceXML:
    """Read provider XML incrementally and reject DTDs and expanded entities."""

    def __init__(self, stream):
        self.stream = stream
        self.tail = b''

    def read(self, size):
        data = self.stream.read(size)
        content = (self.tail + data).upper()
        if b'\x00' in data or b'<!DOCTYPE' in content or b'<!ENTITY' in content:
            raise ValueError('Unexpected NSR XML declaration')
        self.tail = content[-8:]
        return data


def future_records(stream, wanted, revision):
    records = {}
    publication = None
    stack = []
    open_stops = 0
    for event, node in XML.iterparse(SourceXML(stream), events=('start', 'end')):
        if event == 'start':
            if not stack and node.tag != DELIVERY:
                raise ValueError('Unexpected NSR XML document')
            stack.append(node)
            open_stops += node.tag == STOP_PLACE
            continue
        if len(stack) == 2 and node.tag == PUBLICATION:
            if publication is not None:
                raise ValueError('Repeated NSR publication timestamp')
            publication = node.text
        if node.tag == STOP_PLACE:
            quays = [quay for quay in netex.children(node, 'quays/Quay') if quay.get('id') in wanted]
            parent_interval = dated_interval(node) if quays else None
            for quay in quays:
                identifier = quay.get('id')
                record = quay_record(node, quay, revision)
                if record is None:
                    # A competing version with no usable coordinates is still
                    # evidence of ambiguity during its own validity.
                    record = {'quay_id': identifier, 'stop_place_id': node.get('id'),
                              'quay_version': quay.get('version'), 'stop_place_version': node.get('version'),
                              'mapping_revision': revision, 'coordinate_kind': 'Quay', 'crs': 'WGS84'}
                has_conditions = any(netex.children(quay, name) for name in CONDITION_TAGS)
                record.update(stop_place_validity=parent_interval,
                              quay_validity=dated_interval(quay) if has_conditions else parent_interval,
                              validity_basis='quay' if has_conditions else 'containing-stop-place')
                versions = records.setdefault(identifier, {'versions': []})['versions']
                versions.append(record)
                if len(versions) > 32:
                    raise ValueError(f'Too many NSR versions of {identifier}')
            open_stops -= 1
        if len(stack) > 1 and (open_stops == 0 or node.tag == STOP_PLACE):
            stack[-2].remove(node)
            node.clear()
        stack.pop()
    return publication, records


def quay_record(parent, quay, revision):
    try:
        lat = float(netex.field(quay, 'Centroid/Location/Latitude'))
        lon = float(netex.field(quay, 'Centroid/Location/Longitude'))
        if not (isfinite(lat) and 67 < lat < 72 and isfinite(lon) and 14 < lon < 24):
            return None
        parent_id = netex.known_id(parent.get('id'), 'NSR', 'StopPlace')
        parent_version, quay_version = parent.get('version'), quay.get('version')
        if not parent_version or not quay_version or len(parent_version) > 100 or len(quay_version) > 100:
            return None
    except (ValueError, TypeError):
        return None
    return {
        'quay_id': quay.get('id'), 'stop_place_id': parent_id,
        'quay_version': quay_version, 'stop_place_version': parent_version,
        'mapping_revision': revision, 'coordinate_kind': 'Quay', 'crs': 'WGS84',
        'latitude': lat, 'longitude': lon, 'quality': 'qualified',
        'source_updated_at': quay.get('changed'),
    }


def read(path, generation, wanted, fetched_at):
    if not netex.GENERATION_ID.fullmatch(generation):
        raise ValueError('Missing NSR archive generation')
    with Path(path).open('rb') as stream:
        raw = stream.read(MAX_ARCHIVE_BYTES + 1)
    if len(raw) > MAX_ARCHIVE_BYTES:
        raise ValueError('NSR archive too large')
    digest = sha256(raw).hexdigest()
    with ZipFile(BytesIO(raw)) as archive:
        members = archive.infolist()
        if len(members) != 1 or members[0].flag_bits & 1 or members[0].compress_type not in (ZIP_DEFLATED, ZIP_STORED):
            raise ValueError('Unexpected NSR archive')
        future = re.fullmatch(r'tiamat-export-CurrentAndFuture-[0-9]+\.xml', members[0].filename)
        if future:
            if not 0 < members[0].file_size <= 450_000_000:
                raise ValueError('Current-and-future NSR XML exceeds its byte limit')
            revision = f'nsr-future-{generation}-{digest}'
            with archive.open(members[0]) as stream:
                publication, records = future_records(stream, wanted, revision)
            if zoned(publication) is None:
                raise ValueError('Current-and-future NSR archive lacks its publication timestamp')
            return source_metadata(revision, generation, digest, fetched_at, publication, FUTURE_SOURCE_URL) | {
                'scope': FUTURE_SCOPE,
            }, records
        if (len(raw) > 5_000_000 or not re.fullmatch(r'tiamat-export-55_Troms-[0-9]+\.xml', members[0].filename)):
            raise ValueError('Unexpected Troms NSR archive')
        with archive.open(members[0]) as stream:
            payload = stream.read(45_000_001)
    if len(payload) > 45_000_000 or b'\x00' in payload or re.search(rb'<!\s*(?:DOCTYPE|ENTITY)', payload, re.I):
        raise ValueError('Invalid NSR XML')
    root = XML.fromstring(payload)
    if root.tag != DELIVERY:
        raise ValueError('Unexpected NSR XML document')

    revision = f'nsr-troms-{generation}-{digest}'
    records = {}
    ambiguous = set()
    for parent in root.iter(STOP_PLACE):
        for quay in netex.children(parent, 'quays/Quay'):
            identifier = quay.get('id')
            if identifier not in wanted:
                continue
            if identifier in records:
                ambiguous.add(identifier)
                continue
            record = quay_record(parent, quay, revision)
            if record is not None:
                record.update(stop_place_validity=validity(parent), quay_validity=validity(quay))
                records[identifier] = record
    for identifier in ambiguous:
        records.pop(identifier, None)
    return source_metadata(revision, generation, digest, fetched_at, netex.field(root, 'PublicationTimestamp'), SOURCE_URL), records


def source_metadata(revision, generation, digest, fetched_at, publication, url):
    return {'contract': 'nsr-quay-coordinate-v1', 'revision': revision, 'provider': 'Entur NSR',
            'source_url': url + '?generation=' + generation, 'fetched_at': fetched_at.isoformat(),
            'license_url': 'https://data.norge.no/nlod/en/2.0', 'sha256': digest, 'publication': publication}


def load_for_reference(conn, reference):
    key = reference.get('position_coordinate_revision')
    if not isinstance(key, str) or not re.fullmatch(r'nsr-(?:troms|future)-[0-9]{1,20}-[a-f0-9]{64}', key):
        return None
    provenance = reference.get('provenance') or {}
    if provenance.get('nsr_revision') != key:
        return None
    quays = list({call.get('quay_id') for call in reference['calls'] if call.get('quay_id')})
    rows = conn.execute('SELECT source, record FROM public_quay_versions WHERE revision=%s AND quay_id=ANY(%s)',
                        (key, quays)).fetchall()
    if not rows:
        return None
    source = rows[0]['source']
    stops = [entry for row in rows for entry in row['record']['versions']] if source.get('scope') == FUTURE_SCOPE else [
        row['record'] for row in rows]
    return {**source, 'stops': stops}
