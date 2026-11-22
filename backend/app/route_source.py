"""Bounded, launch-time evidence for the seven-date Troms line 20 pilot."""

import argparse
from collections import defaultdict
from datetime import UTC, date, datetime, time, timedelta, timezone
from email.utils import format_datetime, parsedate_to_datetime
from hashlib import sha256
from http.client import HTTPException, HTTPSConnection
from io import BytesIO
import json
import os
from pathlib import Path
import re
import signal
from tempfile import NamedTemporaryFile
from time import monotonic
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from xml.etree import ElementTree as XML
from zipfile import BadZipFile, ZIP_DEFLATED, ZIP_STORED, ZipFile
from zlib import error as ZipDecodeError
from zoneinfo import ZoneInfo

LINE_ID = 'TRO:Line:1_20'
GENERATION = '1795129398375617'
ETAG = '5d5e931e207e5ccfc8b6dd2cae6314f8'
DIGEST = '03662d51c1438514d1695e632c598a7ea589d5384a19804658212fc4af0af8b9'
ARCHIVE_BYTES = 7_225_724
ARCHIVE_URL = 'https://storage.googleapis.com/marduk-production/outbound/netex/rb_tro-aggregated-netex.zip'
MAX_RECHECK_BYTES = 16_000_000
MAX_RECEIPT_BYTES = 2_048
RECHECK_SECONDS = 25
MAX_CACHE_AGE = 3_600
HTTP_CLOCK_SKEW = timedelta(minutes=1)
RECHECK_BASIS = 'qualified_against_sha256'
UTC_ISO = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?\+00:00')
STRONG_ETAG = re.compile(r'[!#-~]{1,128}')
GENERATION_ID = re.compile(r'[1-9][0-9]{0,19}')
SHARED_MEMBER = '_TRO_shared_data.xml'
LINE_MEMBER = 'TRO_TRO-Line-1_20_20_Skattora---sentrum---Kroken.xml'
NS = {'': 'http://www.netex.org.uk/netex'}
DATES = tuple(date(2026, 11, day) for day in range(23, 30))
EXPECTED = dict(zip(DATES, (136, 136, 136, 136, 143, 109, 64), strict=True))
PILOT_COUNTS = object()
WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
OSLO = ZoneInfo('Europe/Oslo')
EMPTY = {'provenance': None, 'days': {}}
EVIDENCE_ERRORS = (OSError, ValueError, LookupError, RuntimeError, BadZipFile, ZipDecodeError, XML.ParseError,
                   OverflowError, EOFError)
catalogue = EMPTY


class InvalidEvidence(ValueError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise InvalidEvidence('Unexpected redirect')


def require_owner():
    if os.environ.get('APP_MODE') != 'private-local' or os.environ.get('V2_ROUTE_SOURCE_REFRESH') != 'owner':
        raise InvalidEvidence('Public acquisition requires the owner sandbox')


def download(archive):
    require_owner()
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


def archive_members(raw, *, pinned):
    if pinned:
        verify_archive(raw)
    with ZipFile(BytesIO(raw)) as archive:
        items = archive.infolist()
        names = {item.filename for item in items}
        if ((pinned and len(items) != 171) or len(items) > 512 or len(names) != len(items)
                or sum(item.file_size for item in items) > 160_000_000
                or any(not re.fullmatch(r'[a-zA-Z0-9_.()-]{1,200}\.xml', item.filename)
                       or item.flag_bits & 1 or item.file_size > 20_000_000
                       or item.compress_type not in (ZIP_STORED, ZIP_DEFLATED) for item in items)
                or not {LINE_MEMBER, SHARED_MEMBER} <= names):
            raise InvalidEvidence('Unexpected archive inventory')
        return xml_member(archive, LINE_MEMBER), xml_member(archive, SHARED_MEMBER)


def nodes(root, name):
    return root.findall('.//' + name, NS)


def children(root, path):
    return root.findall(path, NS)


def single_child(root, path):
    matches = children(root, path)
    if len(matches) > 1:
        raise InvalidEvidence(f'Duplicate {path} field')
    return matches[0] if matches else None


def field(root, path):
    element = single_child(root, path)
    value = (element.text or '').strip() if element is not None else None
    return value or None


def ref(root, path):
    element = single_child(root, path)
    return element.get('ref') if element is not None else None


def require_reference_version(element, target):
    target_version = target.get('version') if target is not None else None
    if element is not None and element.get('version') not in (None, 'any', target_version):
        raise InvalidEvidence(f'Unresolved version of {element.get("ref")}')


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


def assigned_dates(shared, wanted, qualifications=None, *, dates=None):
    dates = DATES if dates is None else dates
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
        rules = set()
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
                require_reference_version(single_child(assignment, 'DayTypeRef'), day_type)
                available = boolean(assignment, 'isAvailable', True)
                period_id = ref(assignment, 'OperatingPeriodRef')
                if period_id and field(assignment, 'Date') is None and days:
                    period = periods[period_id]
                    require_reference_version(single_child(assignment, 'OperatingPeriodRef'), period)
                    first, last = dates_between(period, 'FromDate', 'ToDate')
                    covered = tuple(date_ for date_ in dates if first <= date_ <= last)
                    if covered:
                        rules.add(('period', period_id, period.get('version'), covered, available,
                                   assignment.get('id'), assignment.get('version')))
                    for date_ in covered:
                        if WEEKDAYS[date_.weekday()] in days:
                            active[date_].append(available)
                elif not period_id and field(assignment, 'Date'):
                    date_ = date_field(assignment, 'Date')
                    if date_ in overrides and overrides[date_] != available:
                        raise InvalidEvidence('Conflicting date exceptions')
                    overrides[date_] = available
                    if date_ in dates:
                        rules.add(('date', date_, available, assignment.get('id'), assignment.get('version')))
                else:
                    raise InvalidEvidence('Unsupported calendar assignment')
            if any(len(set(values)) > 1 for values in active.values()):
                raise InvalidEvidence('Conflicting calendar periods')
            result[key] = {date_ for date_ in dates if overrides.get(date_, any(active[date_]))}
            if qualifications is not None:
                qualifications[key] = (day_type.get('version'), days, rules)
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


def pattern_facts(line, shared, *, line_id=LINE_ID):
    routes = index(line, 'Route')
    places = index(shared, 'ScheduledStopPoint')
    displays = index(shared, 'DestinationDisplay')
    platforms = {}
    for assignment in nodes(shared, 'PassengerStopAssignment'):
        scheduled = ref(assignment, 'ScheduledStopPointRef')
        if scheduled in platforms:
            platforms[scheduled] = None
        else:
            platforms[scheduled] = assignment
    result = {}
    for key, pattern in index(line, 'JourneyPattern').items():
        try:
            route_key = ref(pattern, 'RouteRef')
            route = routes[route_key]
            direction = field(route, 'DirectionType')
            if ref(route, 'LineRef') != line_id or direction not in {'outbound', 'inbound'}:
                raise InvalidEvidence('Unknown route, line or direction')
            calls, headsign, display_id = [], None, None
            for pos, item in enumerate(children(pattern, 'pointsInSequence/StopPointInJourneyPattern'), 1):
                if item.get('order') != str(pos):
                    raise InvalidEvidence('Incomplete or inconsistent pattern order')
                stop = known_id(ref(item, 'ScheduledStopPointRef'), 'TRO', 'ScheduledStopPoint')
                assignment = platforms[stop]
                if assignment is None:
                    raise InvalidEvidence('Ambiguous platform assignment')
                require_reference_version(single_child(assignment, 'ScheduledStopPointRef'), places[stop])
                quay = ref(assignment, 'QuayRef')
                stop_place = ref(assignment, 'StopPlaceRef')
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


def journey_on_date(journey, date_, pattern, day_type_ids, operator, *, line_id=LINE_ID):
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
    return {**pattern, 'calls': calls, 'service_date': date_.isoformat(), 'line_id': line_id,
            'journey_id': known_id(journey.get('id'), 'TRO', 'ServiceJourney'),
            'journey_version': journey.get('version'), 'private_code': field(journey, 'PrivateCode'),
            'operator_id': operator,
            'calendar': {'day_type_ids': day_type_ids, 'timezone': 'Europe/Oslo', 'time_axis': 'operating-day-noon-offset'}}


def verify_line_reference_versions(line, shared):
    for kind in ('Line', 'Route', 'JourneyPattern', 'StopPointInJourneyPattern',
                 'DayType', 'ScheduledStopPoint', 'Operator', 'DestinationDisplay'):
        targets = index(line, kind) | index(shared, kind)
        for element in nodes(line, kind + 'Ref'):
            if element.get('version') not in (None, 'any'):
                require_reference_version(element, targets.get(element.get('ref')))


def normalize(line, shared, observed_at, *, qualifications=None, line_id=LINE_ID,
              public_code='20', dates=None, expected=PILOT_COUNTS):
    dates = DATES if dates is None else dates
    expected = EXPECTED if expected is PILOT_COUNTS else expected
    if observed_at.tzinfo is None or observed_at > datetime.now(UTC) + timedelta(minutes=1):
        raise InvalidEvidence('Invalid observation timestamp')
    line_def = index(line, 'Line')
    if (set(line_def) != {line_id} or field(line_def[line_id], 'PublicCode') != public_code
            or any([field(item, 'TimeZone') for item in nodes(root, 'DefaultLocale')] != ['Europe/Oslo']
                   for root in (line, shared))):
        raise InvalidEvidence('Unexpected line or time zone')
    validity_by_member = tuple(tuple(dates_between(item, 'FromDate', 'ToDate')
                                     for item in nodes(root, 'AvailabilityCondition')) for root in (line, shared))
    validities = [limits for member in validity_by_member for limits in member]
    if len(validities) != 2:
        raise InvalidEvidence('Missing or ambiguous archive validity')
    if qualifications is not None:
        verify_line_reference_versions(line, shared)
    patterns = pattern_facts(line, shared, line_id=line_id)
    operators = index(shared, 'Operator')
    journeys = index(line, 'ServiceJourney')
    journey_types = {key: [item.get('ref') for item in children(journey, 'dayTypes/DayTypeRef')]
                     for key, journey in journeys.items()}
    calendar_rules = {} if qualifications is not None else None
    scoped_validity = tuple(tuple(tuple(date_ for date_ in dates if first <= date_ <= last)
                                  for first, last in member) for member in validity_by_member)
    calendar = assigned_dates(shared, {item for values in journey_types.values() for item in values}, calendar_rules, dates=dates)
    departures = {date_: {} for date_ in dates}
    issues = {date_: set() for date_ in dates}
    for key, journey in journeys.items():
        type_ids = journey_types[key]
        if not type_ids or any(calendar[item] is None for item in type_ids):
            for date_ in dates:
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
                if ref(journey, 'LineRef') != line_id or operator not in operators or not pattern:
                    raise InvalidEvidence('Unresolved journey dependency')
                departure_item = journey_on_date(journey, date_, pattern, type_ids, operator, line_id=line_id)
            except (ValueError, KeyError):
                issues[date_].add('unresolved_journey')
                continue
            if any(value and value['utc'] is None for call in departure_item['calls']
                   for value in (call['arrival'], call['departure'])):
                issues[date_].add('unresolved_time')
            departures[date_][key] = departure_item
    days = {}
    for date_, items in departures.items():
        if expected is not None and len(items) != expected[date_]:
            issues[date_].add('count_mismatch')
        if not all(first <= date_ <= last for first, last in validities):
            issues[date_].add('outside_source_validity')
        days[date_] = {'coverage': 'partial' if issues[date_] else 'complete',
                       'reasons': sorted(issues[date_]), 'journeys': items}
        if qualifications is not None:
            active_types = {key for journey in items.values() for key in journey['calendar']['day_type_ids']}
            qualifications[date_] = (scoped_validity, {key: calendar_rules[key] for key in active_types})
    return {
        'provenance': {'provider': 'Entur / Troms', 'namespace': 'TRO', 'mapping': 'NeTEx static / NSR Quay',
                       'url': ARCHIVE_URL, 'generation': GENERATION, 'etag': ETAG, 'sha256': DIGEST,
                       'observed_at': observed_at.isoformat(), 'line_publication': field(line, 'PublicationTimestamp'),
                       'shared_publication': field(shared, 'PublicationTimestamp'), 'parser_revision': 1,
                       'manifest_revision': 'line20-2026-11-23--29', 'timezone': 'Europe/Oslo',
                       'members': [LINE_MEMBER, SHARED_MEMBER]},
        'days': days,
    }


def load(path, timestamp, *, qualifications=None):
    with Path(path).open('rb') as file:
        raw = file.read(ARCHIVE_BYTES + 1)
    return normalize(*archive_members(raw, pinned=True), datetime.fromisoformat(timestamp), qualifications=qualifications)


def check_transport(response):
    if response.status != 200:
        raise InvalidEvidence(f'Unexpected archive HTTP status {response.status}')
    headers = response.headers
    size = headers.get_all('Content-Length')
    tags = headers.get_all('ETag')
    generations = headers.get_all('X-Goog-Generation')
    ages = headers.get_all('Age', ['0'])
    dates = headers.get_all('Date')
    if (not size or len(size) != 1 or not re.fullmatch(r'[1-9][0-9]{0,7}', size[0])
            or int(size[0]) > MAX_RECHECK_BYTES
            or not tags or len(tags) != 1 or not tags[0].startswith('"') or not tags[0].endswith('"')
            or not STRONG_ETAG.fullmatch(tags[0][1:-1])
            or not generations or len(generations) != 1 or not GENERATION_ID.fullmatch(generations[0])
            or headers.get_all('Content-Encoding') not in (None, ['identity'])
            or headers.get_all('Transfer-Encoding') is not None
            or len(ages) != 1 or not re.fullmatch(r'[0-9]{1,10}', ages[0]) or int(ages[0]) > MAX_CACHE_AGE
            or not dates or len(dates) != 1):
        raise InvalidEvidence('Unexpected archive transport metadata')
    try:
        response_date = parsedate_to_datetime(dates[0])
        if format_datetime(response_date, usegmt=True) != dates[0]:
            raise ValueError('Expected an HTTP date in GMT')
    except (TypeError, ValueError):
        raise InvalidEvidence('Invalid HTTP Date in archive transport metadata') from None
    return int(size[0]), tags[0][1:-1], generations[0], response_date, int(ages[0])


def check_deadline(*_):
    raise InvalidEvidence('Archive request exceeded its deadline')


def download_current():
    require_owner()
    url = urlsplit(ARCHIVE_URL)
    connection = HTTPSConnection(url.hostname, timeout=5)
    deadline = monotonic() + RECHECK_SECONDS
    try:
        connection.request('GET', url.path, headers={'User-Agent': 'HIMolde-IBE160-Bussassistent-P1/1.0',
                                                       'Accept-Encoding': 'identity', 'Cache-Control': 'no-cache'})
        with connection.getresponse() as response:
            # Age represents the response at the header boundary, before body transfer.
            checked = datetime.now(UTC)
            size, etag, generation, response_date, age = check_transport(response)
            data = bytearray()
            while len(data) < size:
                if monotonic() >= deadline:
                    check_deadline()
                chunk = response.read1(min(65_536, size - len(data)))
                if not chunk:
                    break
                data.extend(chunk)
            if monotonic() >= deadline:
                check_deadline()
    finally:
        connection.close()
    raw = bytes(data)
    if len(raw) != size:
        raise InvalidEvidence('Archive body size differs from Content-Length')
    receipt = {'checked_at': checked.isoformat(), 'response_date': response_date.isoformat(), 'cache_age_seconds': age,
               'sha256': sha256(raw).hexdigest(), 'size': size, 'etag': etag, 'generation': generation}
    return raw, receipt


def qualify_recheck(raw, receipt, original, original_qualifications):
    text_fields = ('checked_at', 'response_date', 'sha256', 'etag', 'generation')
    if (not isinstance(receipt, dict) or receipt.keys() != {*text_fields, 'cache_age_seconds', 'size'}
            or any(not isinstance(receipt[key], str) for key in text_fields)
            or not re.fullmatch(r'[0-9a-f]{64}', receipt['sha256'])
            or not STRONG_ETAG.fullmatch(receipt['etag'])
            or not GENERATION_ID.fullmatch(receipt['generation'])
            or type(receipt['size']) is not int or not 0 < receipt['size'] <= MAX_RECHECK_BYTES
            or type(receipt['cache_age_seconds']) is not int or not 0 <= receipt['cache_age_seconds'] <= MAX_CACHE_AGE
            or not UTC_ISO.fullmatch(receipt['checked_at']) or not UTC_ISO.fullmatch(receipt['response_date'])):
        raise InvalidEvidence('Invalid recheck receipt metadata')
    if len(raw) != receipt['size'] or sha256(raw).hexdigest() != receipt['sha256']:
        raise InvalidEvidence('Recheck archive size or hash differs from its receipt')
    if (receipt['generation'] == GENERATION
            and (receipt['sha256'], receipt['size'], receipt['etag']) != (DIGEST, ARCHIVE_BYTES, ETAG)):
        raise InvalidEvidence('Recheck metadata differs from the original archive generation')
    checked = datetime.fromisoformat(receipt['checked_at'])
    response_date = datetime.fromisoformat(receipt['response_date'])
    observed = min(checked - timedelta(seconds=receipt['cache_age_seconds']), response_date)
    if (checked > datetime.now(UTC) or response_date > checked + HTTP_CLOCK_SKEW
            or checked - observed > timedelta(seconds=MAX_CACHE_AGE) + HTTP_CLOCK_SKEW
            or observed < datetime.fromisoformat(original['provenance']['observed_at'])):
        raise InvalidEvidence('Invalid recheck observation time')
    qualifications = {}
    evidence = normalize(*archive_members(raw, pinned=False), observed, qualifications=qualifications)
    require_complete(evidence, 'Current archive')
    if evidence['days'] != original['days'] or qualifications != original_qualifications:
        raise InvalidEvidence('Current archive changes dated line 20 facts and requires a separately reviewed pin')
    evidence['provenance'].update(generation=receipt['generation'], etag=receipt['etag'], sha256=receipt['sha256'],
                                  archive_bytes=receipt['size'], checked_at=receipt['checked_at'],
                                  response_date=receipt['response_date'], cache_age_seconds=receipt['cache_age_seconds'],
                                  **{RECHECK_BASIS: DIGEST})
    return evidence


def require_complete(evidence, label):
    if (set(evidence['days']) != set(DATES)
            or any(day['coverage'] != 'complete' for day in evidence['days'].values())):
        raise InvalidEvidence(f'{label} does not have complete coverage of all seven line 20 dates')


def load_recheck(bundle, original, qualifications):
    require_complete(original, 'Pinned archive')
    with Path(bundle).open('rb') as file:
        header = file.readline(MAX_RECEIPT_BYTES + 1)
        checksum, _, metadata = header[:-1].partition(b' ')
        if (len(header) > MAX_RECEIPT_BYTES or not header.endswith(b'\n')
                or checksum != sha256(metadata).hexdigest().encode('ascii')):
            raise InvalidEvidence('Corrupt recheck receipt metadata')
        receipt = json.loads(metadata)
        raw = file.read(MAX_RECHECK_BYTES + 1)
    return qualify_recheck(raw, receipt, original, qualifications)


def write_recheck(bundle, raw, receipt):
    metadata = json.dumps(receipt, sort_keys=True, separators=(',', ':')).encode('ascii')
    header = sha256(metadata).hexdigest().encode('ascii') + b' ' + metadata + b'\n'
    temporary = None
    try:
        with NamedTemporaryFile(dir=bundle.parent, prefix='.line20-', delete=False) as file:
            temporary = Path(file.name)
            file.write(header)
            file.write(raw)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary, bundle)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def timed_download():
    if not hasattr(signal, 'SIGALRM'):
        return download_current()
    # The explicit Linux container also bounds DNS, TLS and response headers.
    previous = signal.signal(signal.SIGALRM, check_deadline)
    signal.alarm(RECHECK_SECONDS)
    try:
        return download_current()
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


def lock_recheck(file):
    try:
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(file.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as error:
        raise InvalidEvidence('Route source is already being checked') from error


def recheck(original_path, original_time, bundle):
    require_owner()
    qualifications = {}
    original = load(original_path, original_time, qualifications=qualifications)
    require_complete(original, 'Pinned archive')
    with bundle.with_suffix('.lock').open('a+b') as lock:
        lock_recheck(lock)
        raw, receipt = timed_download()
        evidence = qualify_recheck(raw, receipt, original, qualifications)
        try:
            previous = load_recheck(bundle, original, qualifications)
        except EVIDENCE_ERRORS:
            previous = original
        if (datetime.fromisoformat(evidence['provenance']['observed_at'])
                < datetime.fromisoformat(previous['provenance']['observed_at'])):
            raise InvalidEvidence('Current archive observation is older than the retained observation')
        write_recheck(bundle, raw, receipt)
        return evidence


def at_launch():
    global catalogue
    path = os.environ.get('V2_ROUTE_ARCHIVE')
    observed = os.environ.get('V2_ROUTE_OBSERVED_AT')
    bundle = os.environ.get('V2_ROUTE_RECHECK_BUNDLE')
    qualifications = {} if bundle else None
    try:
        evidence = load(path, observed, qualifications=qualifications) if path and observed else EMPTY
    except EVIDENCE_ERRORS:
        evidence = EMPTY
    if bundle and evidence['provenance']:
        try:
            evidence = load_recheck(bundle, evidence, qualifications)
        except EVIDENCE_ERRORS:
            # A missing or rejected receipt leaves the original observation intact.
            pass
    catalogue = evidence


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
    acquisition = parser.add_mutually_exclusive_group()
    acquisition.add_argument('--download', action='store_true')
    acquisition.add_argument('--recheck-bundle', type=Path)
    options = parser.parse_args()
    if options.recheck_bundle:
        try:
            evidence = recheck(options.archive, options.observed_at, options.recheck_bundle)
        except EVIDENCE_ERRORS + (HTTPException,) as error:
            raise SystemExit(f'Route source recheck failed: {error}') from None
        provenance = evidence['provenance']
        print(f"Route source checked at {provenance['checked_at']}, effective observation {provenance['observed_at']} "
              f"(SHA-256 {provenance['sha256']})")
    else:
        if options.download:
            download(options.archive)
        evidence = load(options.archive, options.observed_at)
    for day, data in evidence['days'].items():
        print(day, len(data['journeys']), data['coverage'], ', '.join(data['reasons']))
    if any(data['coverage'] != 'complete' for data in evidence['days'].values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
