"""Bounded, launch-time evidence for the seven-date Troms line 20 pilot."""

import argparse
from collections import defaultdict
from datetime import UTC, date, datetime, time, timedelta, timezone
from hashlib import sha256
from io import BytesIO
import os
from pathlib import Path
import re
from time import monotonic
from urllib.request import HTTPRedirectHandler, Request, build_opener
from xml.etree import ElementTree as XML
from zipfile import BadZipFile, ZipFile
from zoneinfo import ZoneInfo

LINE_ID = 'TRO:Line:1_20'
GENERATION = '1795129398375617'
ETAG = '5d5e931e207e5ccfc8b6dd2cae6314f8'
DIGEST = '03662d51c1438514d1695e632c598a7ea589d5384a19804658212fc4af0af8b9'
ARCHIVE_BYTES = 7_225_724
ARCHIVE_URL = 'https://storage.googleapis.com/marduk-production/outbound/netex/rb_tro-aggregated-netex.zip'
SHARED_MEMBER = '_TRO_shared_data.xml'
LINE_MEMBER = 'TRO_TRO-Line-1_20_20_Skattora---sentrum---Kroken.xml'
NS = {'': 'http://www.netex.org.uk/netex'}
DATES = tuple(date(2026, 11, day) for day in range(23, 30))
EXPECTED = dict(zip(DATES, (136, 136, 136, 136, 143, 109, 64), strict=True))
WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
OSLO = ZoneInfo('Europe/Oslo')
EMPTY = {'provenance': None, 'days': {}}
catalogue = EMPTY


class InvalidEvidence(ValueError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise InvalidEvidence('Unexpected redirect')


def download(archive):
    if os.environ.get('APP_MODE') != 'private-local' or os.environ.get('V2_ROUTE_SOURCE_REFRESH') != 'owner':
        raise InvalidEvidence('Public acquisition requires the owner sandbox')
    request = Request(f'{ARCHIVE_URL}?generation={GENERATION}', headers={
        'User-Agent': 'HIMolde-IBE160-Bussassistent-P1/1.0',
        'Accept-Encoding': 'identity',
    })
    deadline = monotonic() + 25
    with build_opener(NoRedirect()).open(request, timeout=5) as response:
        if (response.headers.get('ETag', '').strip('"') != ETAG
                or response.headers.get('X-Goog-Generation') != GENERATION
                or response.headers.get('Content-Length') != str(ARCHIVE_BYTES)):
            raise InvalidEvidence('Unexpected archive metadata')
        data = bytearray()
        while len(data) <= ARCHIVE_BYTES:
            if monotonic() >= deadline:
                raise InvalidEvidence('Archive download exceeded its deadline')
            chunk = response.read(min(65_536, ARCHIVE_BYTES + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
        raw = bytes(data)
    verify_archive(raw)
    # Refuse to overwrite provenance or silently replace the launch archive.
    with archive.open('xb') as output:
        output.write(raw)


def verify_archive(raw):
    if len(raw) != ARCHIVE_BYTES or sha256(raw).hexdigest() != DIGEST:
        raise InvalidEvidence('Pinned archive size or hash differs')


def xml_member(archive, name):
    with archive.open(name) as member:
        data = member.read(20_000_001)
    if len(data) > 20_000_000 or b'\x00' in data or re.search(rb'<!\s*(?:DOCTYPE|ENTITY)', data, re.I):
        raise InvalidEvidence('XML limit or unsupported declaration')
    root = XML.fromstring(data)
    if root.tag != '{' + NS[''] + '}PublicationDelivery' or sum(1 for _ in root.iter()) > 500_000:
        raise InvalidEvidence('Unexpected XML document')
    return root


def members(raw):
    verify_archive(raw)
    with ZipFile(BytesIO(raw)) as archive:
        items = archive.infolist()
        names = {item.filename for item in items}
        if (len(items) != 171 or len(names) != len(items)
                or sum(item.file_size for item in items) > 160_000_000
                or any(not re.fullmatch(r'[a-zA-Z0-9_.()-]{1,200}\.xml', item.filename)
                       or item.flag_bits & 1 or item.file_size > 20_000_000 for item in items)
                or not {LINE_MEMBER, SHARED_MEMBER} <= names):
            raise InvalidEvidence('Unexpected archive inventory')
        return xml_member(archive, LINE_MEMBER), xml_member(archive, SHARED_MEMBER)


def nodes(root, name):
    return root.findall('.//' + name, NS)


def children(root, path):
    return root.findall(path, NS)


def field(root, path):
    value = root.findtext(path, default='', namespaces=NS).strip()
    return value or None


def ref(root, path):
    element = root.find(path, NS)
    return element.get('ref') if element is not None else None


def index(root, name):
    result = {}
    for item in nodes(root, name):
        key = item.get('id')
        if not key or key in result:
            raise InvalidEvidence(f'Missing or duplicate {name} identity')
        result[key] = item
    return result


def date_field(item, path):
    value = field(item, path)
    if not value:
        raise InvalidEvidence('Missing calendar date')
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return date.fromisoformat(value)
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is not None or parsed.time() != time():
        raise InvalidEvidence('Unqualified calendar date format')
    return parsed.date()


def dates_between(item, start, end):
    first, last = date_field(item, start), date_field(item, end)
    if last < first:
        raise InvalidEvidence('Reversed source validity')
    return first, last


def boolean(item, field_name, default):
    value = field(item, field_name)
    if value is None:
        return default
    if value not in {'true', 'false', '0', '1'}:
        raise InvalidEvidence('Invalid Boolean in source')
    return value in {'true', '1'}


def known_id(value, namespace, kind):
    if not value or not re.fullmatch(rf'{namespace}:{kind}:[A-Za-z0-9_./-]{{1,200}}', value):
        raise InvalidEvidence(f'Unresolved {kind} identity')
    return value


def assigned_dates(shared, wanted):
    types = index(shared, 'DayType')
    periods = index(shared, 'OperatingPeriod')
    assignments = defaultdict(list)
    for assignment in nodes(shared, 'DayTypeAssignment'):
        target = ref(assignment, 'DayTypeRef')
        if target in wanted:
            assignments[target].append(assignment)
    result = {}
    for key in wanted:
        day_type = types.get(key)
        if day_type is None or not assignments[key]:
            result[key] = None
            continue
        active = defaultdict(list)
        overrides = {}
        try:
            properties = children(day_type, 'properties/PropertyOfDay')
            days = set()
            for part in properties:
                if len(part) != 1 or not field(part, 'DaysOfWeek'):
                    raise InvalidEvidence('Unsupported day type property')
                days.update(field(part, 'DaysOfWeek').split())
            days = (days - {'Weekdays', 'Weekend', 'Everyday'}) | (
                set(WEEKDAYS[:5]) if 'Weekdays' in days else set()) | (
                set(WEEKDAYS[5:]) if 'Weekend' in days else set()) | (
                set(WEEKDAYS) if 'Everyday' in days else set())
            if not days <= set(WEEKDAYS):
                raise InvalidEvidence('Unknown weekday')
            for assignment in assignments[key]:
                available = boolean(assignment, 'isAvailable', True)
                period_id = ref(assignment, 'OperatingPeriodRef')
                if period_id and field(assignment, 'Date') is None and days:
                    period = periods[period_id]
                    first, last = dates_between(period, 'FromDate', 'ToDate')
                    for date_ in DATES:
                        if first <= date_ <= last and WEEKDAYS[date_.weekday()] in days:
                            active[date_].append(available)
                elif not period_id and field(assignment, 'Date'):
                    date_ = date_field(assignment, 'Date')
                    if date_ in overrides and overrides[date_] != available:
                        raise InvalidEvidence('Conflicting date exceptions')
                    overrides[date_] = available
                else:
                    raise InvalidEvidence('Unsupported calendar assignment')
            if any(len(set(values)) > 1 for values in active.values()):
                raise InvalidEvidence('Conflicting calendar periods')
            result[key] = {date_ for date_ in DATES if overrides.get(date_, any(active[date_]))}
        except (ValueError, KeyError):
            result[key] = None
    return result


def passing_time(node, name, service_date):
    raw = field(node, name + 'Time')
    raw_offset = field(node, name + 'DayOffset')
    if raw is None and raw_offset is None:
        return None
    match = re.fullmatch(r'([0-9]{2}):([0-5][0-9]):([0-5][0-9])', raw or '')
    if not match or (raw_offset is not None and not re.fullmatch(r'[0-2]', raw_offset)):
        raise InvalidEvidence('Invalid passing time')
    hours, minute, second = map(int, match.groups())
    if hours >= 72 or (hours >= 24 and raw_offset is not None):
        raise InvalidEvidence('Unsupported or conflicting day offsets')
    offset = int(raw_offset) if raw_offset is not None else hours // 24
    wall = datetime.combine(service_date + timedelta(days=offset), time(hours % 24, minute, second))
    folds = {local.utcoffset() for fold in (0, 1) if (
        local := wall.replace(tzinfo=OSLO, fold=fold)
    ).astimezone(UTC).astimezone(OSLO).replace(tzinfo=None) == wall}
    if len(folds) == 1:
        axis = datetime.combine(service_date, time(12), OSLO).utcoffset()
        instant = wall.replace(tzinfo=timezone(axis)).astimezone(UTC)
        calendar_time = instant.astimezone(OSLO).isoformat()
        utc = instant.isoformat()
    else:
        calendar_time = utc = None
    return {'raw_time': raw, 'raw_day_offset': raw_offset, 'day_offset': offset,
            'calendar_time': calendar_time, 'utc': utc}


def pattern_facts(line, shared):
    routes = index(line, 'Route')
    places = index(shared, 'ScheduledStopPoint')
    displays = index(shared, 'DestinationDisplay')
    platforms = {}
    for assignment in nodes(shared, 'PassengerStopAssignment'):
        scheduled = ref(assignment, 'ScheduledStopPointRef')
        if scheduled in platforms:
            platforms[scheduled] = None
        else:
            platforms[scheduled] = (ref(assignment, 'QuayRef'), ref(assignment, 'StopPlaceRef'))
    result = {}
    for key, pattern in index(line, 'JourneyPattern').items():
        try:
            route_key = ref(pattern, 'RouteRef')
            route = routes[route_key]
            direction = field(route, 'DirectionType')
            if ref(route, 'LineRef') != LINE_ID or direction not in {'outbound', 'inbound'}:
                raise InvalidEvidence('Unknown route, line or direction')
            calls, headsign, display_id = [], None, None
            for pos, item in enumerate(children(pattern, 'pointsInSequence/StopPointInJourneyPattern'), 1):
                if item.get('order') != str(pos):
                    raise InvalidEvidence('Incomplete or inconsistent pattern order')
                stop = known_id(ref(item, 'ScheduledStopPointRef'), 'TRO', 'ScheduledStopPoint')
                quay, stop_place = platforms[stop]
                title = field(places[stop], 'Name')
                display = ref(item, 'DestinationDisplayRef')
                if display:
                    display_id = display
                    headsign = field(displays[display], 'FrontText')
                    if not headsign:
                        raise InvalidEvidence('Unresolved destination display')
                if not title or not headsign:
                    raise InvalidEvidence('Unresolved stop name or initial destination display')
                calls.append({
                    'position': pos,
                    'occurrence_id': known_id(item.get('id'), 'TRO', 'StopPointInJourneyPattern'),
                    'scheduled_stop_point_id': stop,
                    'stop_place_id': known_id(stop_place, 'NSR', 'StopPlace') if stop_place else None,
                    'quay_id': known_id(quay, 'NSR', 'Quay'),
                    'name': title, 'headsign': headsign, 'headsign_id': display_id,
                    'boarding': boolean(item, 'ForBoarding', True), 'alighting': boolean(item, 'ForAlighting', True),
                })
            if not 2 <= len(calls) <= 120 or len({call['occurrence_id'] for call in calls}) != len(calls):
                raise InvalidEvidence('Invalid pattern occurrence count or identity')
            result[key] = {'pattern_id': known_id(key, 'TRO', 'JourneyPattern'),
                           'pattern_version': pattern.get('version'), 'route_id': route_key,
                           'direction': direction, 'headsign': calls[0]['headsign'], 'calls': calls}
        except (ValueError, KeyError, TypeError):
            result[key] = None
    return result


def journey_on_date(journey, date_, pattern, day_type_ids, operator):
    times = children(journey, 'passingTimes/TimetabledPassingTime')
    if [ref(node, 'StopPointInJourneyPatternRef') for node in times] != [
        call['occurrence_id'] for call in pattern['calls']
    ]:
        raise InvalidEvidence('Passing times do not match ordered occurrences')
    calls = []
    previous = None
    for occurrence, node in zip(pattern['calls'], times, strict=True):
        values = {mode.lower(): passing_time(node, mode, date_) for mode in ('Arrival', 'Departure')}
        if all(value is None for value in values.values()):
            raise InvalidEvidence('Missing planned passing time')
        for value in values.values():
            if value and value['utc']:
                if previous is not None and value['utc'] < previous:
                    raise InvalidEvidence('Passing times run backwards')
                previous = value['utc']
        calls.append({**occurrence, **values})
    if not calls[0]['departure'] or not calls[-1]['arrival']:
        raise InvalidEvidence('No terminal timing evidence')
    return {**pattern, 'calls': calls, 'service_date': date_.isoformat(), 'line_id': LINE_ID,
            'journey_id': known_id(journey.get('id'), 'TRO', 'ServiceJourney'),
            'journey_version': journey.get('version'), 'private_code': field(journey, 'PrivateCode'),
            'operator_id': operator,
            'calendar': {'day_type_ids': day_type_ids, 'timezone': 'Europe/Oslo', 'time_axis': 'operating-day-noon-offset'}}


def normalize(line, shared, observed_at):
    if observed_at.tzinfo is None or observed_at > datetime.now(UTC) + timedelta(minutes=1):
        raise InvalidEvidence('Invalid observation timestamp')
    line_def = index(line, 'Line')
    if (set(line_def) != {LINE_ID} or field(line_def[LINE_ID], 'PublicCode') != '20'
            or any([field(item, 'TimeZone') for item in nodes(root, 'DefaultLocale')] != ['Europe/Oslo']
                   for root in (line, shared))):
        raise InvalidEvidence('Unexpected line or time zone')
    validities = [dates_between(item, 'FromDate', 'ToDate') for root in (line, shared)
                  for item in nodes(root, 'AvailabilityCondition')]
    if len(validities) != 2:
        raise InvalidEvidence('Missing or ambiguous archive validity')
    patterns = pattern_facts(line, shared)
    operators = index(shared, 'Operator')
    journeys = index(line, 'ServiceJourney')
    journey_types = {key: [item.get('ref') for item in children(journey, 'dayTypes/DayTypeRef')]
                     for key, journey in journeys.items()}
    calendar = assigned_dates(shared, {item for values in journey_types.values() for item in values})
    departures = {date_: {} for date_ in DATES}
    issues = {date_: set() for date_ in DATES}
    for key, journey in journeys.items():
        type_ids = journey_types[key]
        if not type_ids or any(calendar[item] is None for item in type_ids):
            for date_ in DATES:
                issues[date_].add('unresolved_calendar')
            continue
        active = set().union(*(calendar[item] for item in type_ids))
        for date_ in active:
            if not all(first <= date_ <= last for first, last in validities):
                issues[date_].add('outside_source_validity')
                continue
            try:
                operator = known_id(ref(journey, 'OperatorRef'), 'TRO', 'Operator')
                pattern = patterns.get(ref(journey, 'JourneyPatternRef'))
                if ref(journey, 'LineRef') != LINE_ID or operator not in operators or not pattern:
                    raise InvalidEvidence('Unresolved journey dependency')
                departure_item = journey_on_date(journey, date_, pattern, type_ids, operator)
            except (ValueError, KeyError):
                issues[date_].add('unresolved_journey')
                continue
            if any(value and value['utc'] is None for call in departure_item['calls']
                   for value in (call['arrival'], call['departure'])):
                issues[date_].add('unresolved_time')
            departures[date_][key] = departure_item
    days = {}
    for date_, items in departures.items():
        if len(items) != EXPECTED[date_]:
            issues[date_].add('count_mismatch')
        if not all(first <= date_ <= last for first, last in validities):
            issues[date_].add('outside_source_validity')
        days[date_] = {'coverage': 'partial' if issues[date_] else 'complete',
                       'reasons': sorted(issues[date_]), 'journeys': items}
    return {
        'provenance': {'provider': 'Entur / Troms', 'namespace': 'TRO', 'mapping': 'NeTEx static / NSR Quay',
                       'url': ARCHIVE_URL, 'generation': GENERATION, 'etag': ETAG, 'sha256': DIGEST,
                       'observed_at': observed_at.isoformat(), 'line_publication': field(line, 'PublicationTimestamp'),
                       'shared_publication': field(shared, 'PublicationTimestamp'), 'parser_revision': 1,
                       'manifest_revision': 'line20-2026-11-23--29', 'timezone': 'Europe/Oslo',
                       'members': [LINE_MEMBER, SHARED_MEMBER]},
        'days': days,
    }


def load(path, timestamp):
    with Path(path).open('rb') as file:
        raw = file.read(ARCHIVE_BYTES + 1)
    return normalize(*members(raw), datetime.fromisoformat(timestamp))


def at_launch():
    global catalogue
    path = os.environ.get('V2_ROUTE_ARCHIVE')
    observed = os.environ.get('V2_ROUTE_OBSERVED_AT')
    try:
        catalogue = load(path, observed) if path and observed else EMPTY
    except (OSError, ValueError, KeyError, RuntimeError, BadZipFile, XML.ParseError, OverflowError):
        catalogue = EMPTY


def lookup(service_date, now):
    if service_date not in DATES:
        return {'coverage': 'unavailable', 'source_state': 'outside_scope', 'reasons': ['outside_manifest'],
                'provenance': None, 'journeys': {}}
    day = catalogue['days'].get(service_date)
    if day is None:
        return {'coverage': 'unavailable', 'source_state': 'unavailable', 'reasons': ['archive_unavailable'],
                'provenance': None, 'journeys': {}}
    source = catalogue['provenance']
    stale = now - datetime.fromisoformat(source['observed_at']) >= timedelta(hours=24)
    return {**day, 'source_state': 'stale' if stale else 'available', 'provenance': source}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--observed-at', required=True)
    parser.add_argument('--download', action='store_true')
    options = parser.parse_args()
    if options.download:
        download(options.archive)
    evidence = load(options.archive, options.observed_at)
    for day, data in evidence['days'].items():
        print(day, len(data['journeys']), data['coverage'], ', '.join(data['reasons']))
    if any(data['coverage'] != 'complete' for data in evidence['days'].values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
