"""Eligibility for dated Quay positions on a frozen route."""
import json
import math
import re
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path

from .draft_storage import fingerprint


CONTRACT = 'nsr-quay-coordinate-v1'
MAX_CALLS = 250
MAX_STOPS = 32
PILOT_ROUTE_SHA = '03662d51c1438514d1695e632c598a7ea589d5384a19804658212fc4af0af8b9'
PILOT_REVISION = 'nsr-line20-2026-11-20-v1'
LICENSE_URL = 'https://data.norge.no/nlod/en/2.0'
ID_PATTERNS = {
    'quay': re.compile(r'NSR:Quay:[0-9]{1,24}\Z'),
    'stop_place': re.compile(r'NSR:StopPlace:[0-9]{1,24}\Z'),
}


def instant(value):
    if not isinstance(value, str) or len(value) > 48 or 'T' not in value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.utcoffset() is not None else None


def bounded_text(value, limit=200):
    return isinstance(value, str) and 0 < len(value) <= limit and value.isprintable()


def public_id(value, kind):
    return isinstance(value, str) and ID_PATTERNS[kind].fullmatch(value) is not None


def source_version(reference):
    provenance = reference.get('provenance')
    if not isinstance(provenance, dict):
        return None
    return provenance.get('sha256') or provenance.get('snapshot')


def pin_coordinate_revision(reference):
    # This association is immutable. A later sidecar must receive a new
    # revision and be selected in a freshly reviewed route preparation.
    return PILOT_REVISION if source_version(reference) == PILOT_ROUTE_SHA else None


@lru_cache(maxsize=1)
def sidecar(revision):
    if revision != PILOT_REVISION:
        return None
    path = Path(__file__).with_name('nsr_position_sidecar.json')
    try:
        if path.stat().st_size > 64_000:
            return None
        data = json.loads(path.read_bytes())
        if data['contract'] == CONTRACT and data['revision'] == revision and len(data['stops']) <= MAX_STOPS:
            return data
    except (OSError, ValueError, TypeError, KeyError):
        pass
    return None


def valid_during(record, call_times):
    start, end = instant(record.get('valid_from')), instant(record.get('valid_until'))
    if start is None or end is None:
        return 'validity-unknown'
    if start >= end or any(t < start or t >= end for t in call_times):
        return 'validity-mismatch'
    return None


def point_for(call, data, binding):
    quay_id, scheduled_parent = call['quay_id'], call['stop_place_id']
    if not public_id(quay_id, 'quay') or not bounded_text(call['scheduled_stop_point_id']):
        return None, None, 'mapping-unverified'
    if data is None:
        return None, scheduled_parent, 'coordinate-version-missing'
    records = [item for item in data['stops'] if item['quay_id'] == quay_id]
    if len(records) != 1:
        return None, scheduled_parent, 'coordinate-ambiguous' if records else 'coordinate-missing'
    record = records[0]
    parent = record.get('stop_place_id')
    if not public_id(parent, 'stop_place') or scheduled_parent not in (None, parent):
        return None, scheduled_parent, 'mapping-unverified'
    versions = ('stop_place_version', 'quay_version', 'mapping_revision')
    if (any(not bounded_text(record.get(key), 100) for key in versions)
            or record.get('coordinate_kind') != 'Quay' or record.get('crs') != 'WGS84'):
        return None, parent, 'mapping-unverified'
    try:
        lat, lon = record['latitude'], record['longitude']
        valid_coordinates = (type(lat) in (float, int) and type(lon) in (float, int)
                             and math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180)
    except KeyError:
        valid_coordinates = False
    if not valid_coordinates:
        return None, parent, 'coordinate-invalid'
    if not binding:
        return None, parent, 'route-incompatible'
    instants = [instant(value['utc']) for value in (call['arrival'], call['departure']) if value is not None]
    if not instants or None in instants:
        return None, parent, 'call-time-unverified'
    for object_name in ('stop_place_validity', 'quay_validity'):
        reason = valid_during(record.get(object_name, {}), instants)
        if reason:
            return None, parent, reason
    if record.get('quality') != 'qualified' or not instant(data.get('fetched_at')):
        return None, parent, 'coordinate-unverified'
    return {
        'latitude': lat, 'longitude': lon, 'revision': data['revision'],
        'stop_place_version': record['stop_place_version'], 'quay_version': record['quay_version'],
        'mapping_revision': record['mapping_revision'],
        'stop_place_validity': record['stop_place_validity'], 'quay_validity': record['quay_validity'],
        'source_updated_at': record.get('source_updated_at'),
    }, parent, None


def call_time(raw):
    if raw is None:
        return None
    if isinstance(raw, str):
        return {'utc': raw if instant(raw) else None, 'calendar_time': raw if instant(raw) else None}
    if not isinstance(raw, dict):
        return {'utc': None, 'calendar_time': None}
    return {key: raw.get(key) if instant(raw.get(key)) else None for key in ('utc', 'calendar_time')}


def view(reference, activity_id):
    if not reference:
        return {'route': None, 'calls': [], 'reason': 'route-missing', 'source': None}
    start, end, calls = (reference.get(key) for key in ('start_position', 'end_position', 'calls'))
    if (type(start) is not int or type(end) is not int or not 1 <= start <= end <= MAX_CALLS
            or not isinstance(calls, list) or len(calls) > MAX_CALLS):
        return {'route': None, 'calls': [], 'reason': 'range-invalid', 'source': None}
    calls = [call for call in calls if isinstance(call, dict) and type(call.get('position')) is int
             and start <= call['position'] <= end]
    if ([call['position'] for call in calls] != list(range(start, end + 1))
            or any(not bounded_text(call.get('occurrence_id')) for call in calls)
            or len({call['occurrence_id'] for call in calls}) != len(calls)):
        return {'route': None, 'calls': [], 'reason': 'range-invalid', 'source': None}
    decision = reference.get('decision_revision')
    version = source_version(reference)
    try:
        dated = (bounded_text(reference.get('service_date'), 10)
                 and date.fromisoformat(reference['service_date']).isoformat() == reference['service_date'])
    except ValueError:
        dated = False
    identity = (reference.get('activity_id') == str(activity_id) and type(decision) is int and decision > 0
                and dated and bounded_text(version)
                and all(bounded_text(reference.get(key)) for key in ('journey_id', 'pattern_id', 'line_id')))
    status = reference.get('status')
    if status not in ('compatible', 'unverified', 'incompatible'):
        status = 'unverified'
    compatible = identity and status == 'compatible'
    reason = ('route-identity-unverified' if not identity else
              'route-incompatible' if status != 'compatible' else None)
    # Legacy reference rows can only resolve the published sidecar pinned to
    # their exact archive digest. An explicit null pin remains manual-only.
    coordinate_revision = reference.get('position_coordinate_revision', pin_coordinate_revision(reference))
    data = sidecar(coordinate_revision) if bounded_text(coordinate_revision, 100) else None
    route = {key: reference.get(key) if bounded_text(reference.get(key)) else None for key in (
        'activity_id', 'service_date', 'journey_id', 'line_id', 'pattern_id', 'direction', 'headsign')}
    route.update(start_position=start, end_position=end, status=status,
                 decision_revision=decision if type(decision) is int and decision > 0 else None,
                 source_version=version if bounded_text(version) else None,
                 basis=fingerprint(activity_id, reference), compatible=bool(compatible))
    result = []
    for raw in calls:
        call = {key: raw.get(key) if bounded_text(raw.get(key)) else None for key in (
            'occurrence_id', 'scheduled_stop_point_id', 'stop_place_id', 'quay_id', 'name', 'headsign')}
        call.update(position=raw['position'], arrival=call_time(raw.get('arrival')), departure=call_time(raw.get('departure')))
        coordinates, parent, issue = point_for(call, data, compatible)
        result.append(call | {'stop_place_id': parent, 'coordinates': coordinates, 'coordinate_issue': issue})
    source = None if data is None else {key: data[key] for key in ('contract', 'revision', 'provider', 'source_url',
                                                                   'fetched_at', 'license_url')}
    return {'route': route, 'calls': result, 'reason': reason, 'source': source}
