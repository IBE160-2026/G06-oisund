"""Exact Quay mappings and dated coordinate eligibility on a frozen route."""
import json
import math
import re
from datetime import date, datetime
from functools import lru_cache
from hashlib import sha256
from pathlib import Path

from . import quay_catalogue, route_source
from .draft_storage import fingerprint


CONTRACT = 'nsr-quay-coordinate-v1'
MAX_CALLS = 250
MAX_STOPS = 32
PILOT_ROUTE_SHA = '03662d51c1438514d1695e632c598a7ea589d5384a19804658212fc4af0af8b9'
PILOT_REVISION = 'nsr-line20-2026-11-20-v1'
PILOT_MANUAL_REVISION = 'nsr-line20-2026-11-20-v2'
PILOT_MANUAL_STOPS = 120
PILOT_MANUAL_SIDECAR_SHA = '0bc1af486c3074861076b030c53a81215b22c5fd7c23d877f6fb582aa554abf9'
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


def is_pilot_timetable(reference):
    provenance = reference.get('provenance')
    return isinstance(provenance, dict) and provenance.get('sha256') == PILOT_ROUTE_SHA


def is_rechecked_timetable(reference):
    provenance = reference.get('provenance')
    if not isinstance(provenance, dict) or provenance.get(route_source.RECHECK_BASIS) != PILOT_ROUTE_SHA:
        return False
    digest = provenance.get('sha256')
    return isinstance(digest, str) and re.fullmatch(r'[0-9a-f]{64}', digest) is not None


def current_pilot_revision():
    # Select an available artifact for a new decision. Historical reads use
    # the frozen pin and its original timetable binding.
    return next((revision for revision in (PILOT_MANUAL_REVISION, PILOT_REVISION)
                 if sidecar(revision) is not None), None)


@lru_cache(maxsize=2)
def sidecar(revision):
    if revision == PILOT_REVISION:
        filename, max_bytes = 'nsr_position_sidecar.json', 64_000
    elif revision == PILOT_MANUAL_REVISION:
        filename, max_bytes = 'nsr_position_sidecar_v2.json', 100_000
    else:
        return None
    try:
        with Path(__file__).with_name(filename).open('rb') as file:
            raw = file.read(max_bytes + 1)
        if len(raw) > max_bytes:
            return None
        if revision == PILOT_MANUAL_REVISION and sha256(raw).hexdigest() != PILOT_MANUAL_SIDECAR_SHA:
            return None
        data = json.loads(raw)
        stops = data['stops']
        if data['contract'] != CONTRACT or data['revision'] != revision or not isinstance(stops, list):
            return None
        if revision == PILOT_MANUAL_REVISION and len(stops) == PILOT_MANUAL_STOPS:
            return data
        if revision == PILOT_REVISION and len(stops) <= MAX_STOPS:
            return data
    except (OSError, ValueError, TypeError, KeyError):
        pass
    return None


def validity_bounds(record, open_end):
    start, end = instant(record.get('valid_from')), instant(record.get('valid_until'))
    if start is None or end is None and not (open_end and record.get('valid_until') is None):
        return None
    return start, end


def valid_during(record, call_times, open_end=False):
    bounds = validity_bounds(record, open_end)
    if bounds is None:
        return 'validity-unknown'
    start, end = bounds
    if end is not None and start >= end or any(t < start or end is not None and t >= end for t in call_times):
        return 'validity-mismatch'
    return None


def call_validity(record, instants, open_end):
    for name in ('stop_place_validity', 'quay_validity'):
        reason = valid_during(record.get(name, {}), instants, open_end)
        if reason:
            return reason
    return None


def may_overlap_call(record, instants):
    bounds = [validity_bounds(record.get(name, {}), True) for name in ('stop_place_validity', 'quay_validity')]
    start = max((interval[0] for interval in bounds if interval), default=None)
    end = min((interval[1] for interval in bounds if interval and interval[1] is not None), default=None)
    return (not (start and end and start >= end)
            and (start is None or start <= max(instants))
            and (end is None or min(instants) < end))


def point_for(call, data, binding, manual_mapping):
    quay_id, scheduled_parent = call['quay_id'], call['stop_place_id']
    fallback_parent = None if manual_mapping else scheduled_parent
    if not public_id(quay_id, 'quay') or not bounded_text(call['scheduled_stop_point_id']):
        return None, None, 'mapping-unverified'
    if data is None:
        return None, fallback_parent, 'coordinate-version-missing'
    records = [item for item in data['stops'] if isinstance(item, dict) and item.get('quay_id') == quay_id]
    current_and_future = data.get('scope') == quay_catalogue.FUTURE_SCOPE
    if current_and_future and not manual_mapping and fallback_parent is None:
        parents = {record.get('stop_place_id') for record in records}
        if len(parents) == 1:
            parent = next(iter(parents))
            if public_id(parent, 'stop_place'):
                fallback_parent = parent
    instants = [instant(value['utc']) for value in (call['arrival'], call['departure']) if value is not None]
    verified_times = bool(instants and None not in instants)
    if current_and_future and len(records) > 1 and verified_times:
        records = [record for record in records if may_overlap_call(record, instants)]
        if not records:
            return None, fallback_parent, 'validity-mismatch'
    if len(records) != 1:
        return None, fallback_parent, 'coordinate-ambiguous' if records else 'coordinate-missing'
    record = records[0]
    parent = record.get('stop_place_id')
    if not public_id(parent, 'stop_place') or scheduled_parent not in (None, parent):
        return None, fallback_parent, 'mapping-unverified'
    versions = ('stop_place_version', 'quay_version', 'mapping_revision')
    if (any(not bounded_text(record.get(key), 100) for key in versions)
            or record.get('coordinate_kind') != 'Quay' or record.get('crs') != 'WGS84'):
        return None, None if manual_mapping else parent, 'mapping-unverified'
    try:
        lat, lon = record['latitude'], record['longitude']
        valid_coordinates = (type(lat) in (float, int) and type(lon) in (float, int)
                             and math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180)
    except KeyError:
        valid_coordinates = False
    if not valid_coordinates:
        return None, None if manual_mapping else parent, 'coordinate-invalid'
    if not binding:
        return None, parent, 'route-incompatible'
    if not verified_times:
        return None, parent, 'call-time-unverified'
    reason = call_validity(record, instants, current_and_future)
    if reason:
        return None, parent, reason
    if record.get('quality') != 'qualified' or not instant(data.get('fetched_at')):
        return None, parent, 'coordinate-unverified'
    return {
        'latitude': lat, 'longitude': lon, 'revision': data['revision'],
        'stop_place_version': record['stop_place_version'], 'quay_version': record['quay_version'],
        'mapping_revision': record['mapping_revision'],
        'stop_place_validity': record['stop_place_validity'], 'quay_validity': record['quay_validity'],
        **({'validity_basis': record['validity_basis']} if current_and_future else {}),
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


def view(reference, activity_id, catalogue_data=None):
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
    rechecked = is_rechecked_timetable(reference)
    legacy_revision = PILOT_REVISION if version == PILOT_ROUTE_SHA and not rechecked else None
    coordinate_revision = reference.get('position_coordinate_revision', legacy_revision)
    manual_mapping = coordinate_revision == PILOT_MANUAL_REVISION
    data = None
    if rechecked:
        bound = manual_mapping and reference.get('selection_mode') == 'explicit'
    elif manual_mapping:
        bound = is_pilot_timetable(reference)
    else:
        bound = coordinate_revision != PILOT_REVISION or version == PILOT_ROUTE_SHA
    if bounded_text(coordinate_revision, 100) and bound:
        data = catalogue_data if catalogue_data is not None else sidecar(coordinate_revision)
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
        coordinates, parent, issue = point_for(call, data, compatible, manual_mapping)
        result.append(call | {'stop_place_id': parent, 'coordinates': coordinates, 'coordinate_issue': issue})
    source = None if data is None else {key: data[key] for key in ('contract', 'revision', 'provider', 'source_url',
                                                                   'fetched_at', 'license_url')}
    return {'route': route, 'calls': result, 'reason': reason, 'source': source}
