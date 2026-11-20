"""Independent controls for bounded NeTEx calendar, time and occurrence resolution."""

from datetime import UTC, date, datetime, timedelta, timezone
from email.utils import format_datetime
from hashlib import sha256
from http.client import HTTPMessage
from io import BytesIO
from ssl import SSLError
from xml.etree import ElementTree as XML
from zipfile import ZIP_LZMA, ZipFile

import pytest

from app import route_source as source


def document(xml):
    return XML.fromstring('<PublicationDelivery xmlns="http://www.netex.org.uk/netex">' + xml + '</PublicationDelivery>')


def clock(tag, value, offset=None):
    return document(f'<{tag}Time>{value}</{tag}Time>' + (f'<{tag}DayOffset>{offset}</{tag}DayOffset>' if offset is not None else ''))


@pytest.mark.parametrize(('operating', 'time', 'encoded', 'day_offset', 'expected'), [
    ('2026-11-29', '25:30:00', None, 1, '2026-11-30T00:30:00+00:00'),
    ('2026-11-29', '01:30:00', '1', 1, '2026-11-30T00:30:00+00:00'),
    ('2026-10-24', '01:30:00', '1', 1, '2026-10-24T23:30:00+00:00'),
    ('2026-10-31', '01:30:00', '1', 1, '2026-11-01T00:30:00+00:00'),
    ('2026-10-24', '02:30:00', '1', 1, None),
    ('2026-03-29', '02:30:00', None, 0, None),
])
def test_raw_and_service_day_noon_axis(operating, time, encoded, day_offset, expected):
    parsed = source.passing_time(clock('Departure', time, encoded), 'Departure', date.fromisoformat(operating))
    assert (parsed['raw_time'], parsed['raw_day_offset'], parsed['day_offset'], parsed['utc']) == (time, encoded, day_offset, expected)
    assert (parsed['calendar_time'] is None) == (expected is None)


@pytest.mark.parametrize(('time', 'offset'), [('24:00:00', '1'), ('12:00:00', '-1'), ('12:61:00', '0'), ('99:00:00', None)])
def test_invalid_time_is_not_guessed(time, offset):
    with pytest.raises(source.InvalidEvidence):
        source.passing_time(clock('Arrival', time, offset), 'Arrival', date(2026, 11, 23))


def test_calendar_weekday_period_and_literal_calendar_overrides():
    shared = document("""
      <DayType id="ordinary"><properties><PropertyOfDay><DaysOfWeek>Weekdays</DaysOfWeek></PropertyOfDay></properties></DayType>
      <DayType id="broken"/>
      <DayType id="unknownWeekday"><properties><PropertyOfDay><DaysOfWeek>DayEight</DaysOfWeek></PropertyOfDay></properties></DayType>
      <OperatingPeriod id="week"><FromDate>2026-11-23T00:00:00</FromDate><ToDate>2026-11-27T00:00:00</ToDate></OperatingPeriod>
      <DayTypeAssignment><OperatingPeriodRef ref="week"/><DayTypeRef ref="ordinary"/></DayTypeAssignment>
      <DayTypeAssignment><Date>2026-11-25</Date><DayTypeRef ref="ordinary"/><isAvailable>false</isAvailable></DayTypeAssignment>
      <DayTypeAssignment><Date>2026-11-29</Date><DayTypeRef ref="ordinary"/></DayTypeAssignment>
      <DayTypeAssignment><Date>2026-02-30</Date><DayTypeRef ref="broken"/></DayTypeAssignment>
      <DayTypeAssignment><OperatingPeriodRef ref="week"/><DayTypeRef ref="unknownWeekday"/></DayTypeAssignment>
    """)
    result = source.assigned_dates(shared, {'ordinary', 'broken', 'missing', 'unknownWeekday'})
    assert result == {'ordinary': {date(2026, 11, number) for number in (23, 24, 26, 27, 29)},
                      'broken': None, 'missing': None, 'unknownWeekday': None}


def test_out_of_scope_and_archive_failure_are_unavailable(monkeypatch, tmp_path):
    monkeypatch.setenv('V2_ROUTE_ARCHIVE', str(tmp_path / 'invalid.zip'))
    monkeypatch.setenv('V2_ROUTE_OBSERVED_AT', '2026-11-20T01:13:54Z')
    (tmp_path / 'invalid.zip').write_bytes(b'not an archive')
    source.at_launch()
    now = datetime(2026, 11, 20, 8, tzinfo=timezone.utc)
    assert source.lookup(date(2026, 11, 23), now)['source_state'] == 'unavailable'
    assert source.lookup(date(2026, 11, 22), now)['source_state'] == 'outside_scope'
    assert source.lookup(date(2026, 10, 31), now)['coverage'] == 'unavailable'


def zipped(line, shared, comment=b'', *, compression=0):
    output = BytesIO()
    with ZipFile(output, 'w', compression=compression) as archive:
        archive.comment = comment
        for name, content in ((source.LINE_MEMBER, line), (source.SHARED_MEMBER, shared)):
            archive.writestr(name, XML.tostring(document(content)))
        for number in range(169):
            archive.writestr(f'unrelated-{number}.xml', '<unused/>')
    return output.getvalue()


@pytest.fixture
def pinned(monkeypatch, tmp_path):
    monkeypatch.setattr(source, 'EXPECTED', dict.fromkeys(source.DATES, 1))
    monkeypatch.setattr(source, 'catalogue', source.EMPTY)
    common = '''<DefaultLocale><TimeZone>Europe/Oslo</TimeZone></DefaultLocale>
        <AvailabilityCondition><FromDate>2026-11-20</FromDate><ToDate>2026-11-30</ToDate></AvailabilityCondition>'''
    line = '''<Line id="TRO:Line:1_20"><PublicCode>20</PublicCode></Line>
        <Route id="TRO:Route:out"><LineRef ref="TRO:Line:1_20"/><DirectionType>outbound</DirectionType></Route>
        <JourneyPattern id="TRO:JourneyPattern:out" version="1"><RouteRef ref="TRO:Route:out"/><pointsInSequence>
          <StopPointInJourneyPattern id="TRO:StopPointInJourneyPattern:first" order="1">
            <ScheduledStopPointRef ref="TRO:ScheduledStopPoint:first"/><DestinationDisplayRef ref="TRO:DestinationDisplay:last"/>
          </StopPointInJourneyPattern>
          <StopPointInJourneyPattern id="TRO:StopPointInJourneyPattern:last" order="2">
            <ScheduledStopPointRef ref="TRO:ScheduledStopPoint:last"/>
          </StopPointInJourneyPattern>
        </pointsInSequence></JourneyPattern>
        <ServiceJourney id="TRO:ServiceJourney:control" version="1"><LineRef ref="TRO:Line:1_20"/>
          <OperatorRef ref="TRO:Operator:control"/><JourneyPatternRef ref="TRO:JourneyPattern:out"/>
          <dayTypes><DayTypeRef ref="fixture"/></dayTypes><passingTimes>
            <TimetabledPassingTime><StopPointInJourneyPatternRef ref="TRO:StopPointInJourneyPattern:first"/>
              <DepartureTime>08:00:00</DepartureTime></TimetabledPassingTime>
            <TimetabledPassingTime><StopPointInJourneyPatternRef ref="TRO:StopPointInJourneyPattern:last"/>
              <ArrivalTime>08:10:00</ArrivalTime></TimetabledPassingTime>
          </passingTimes></ServiceJourney>'''
    shared = '''<Operator id="TRO:Operator:control"/>
        <DayType id="fixture"><properties><PropertyOfDay><DaysOfWeek>Everyday</DaysOfWeek></PropertyOfDay></properties></DayType>
        <OperatingPeriod id="fixture-period"><FromDate>2026-11-20</FromDate><ToDate>2026-11-30</ToDate></OperatingPeriod>
        <DayTypeAssignment><DayTypeRef ref="fixture"/><OperatingPeriodRef ref="fixture-period"/></DayTypeAssignment>
        <DestinationDisplay id="TRO:DestinationDisplay:last"><FrontText>Control destination</FrontText></DestinationDisplay>'''
    for stop, quay in [('first', '1'), ('last', '2')]:
        shared += f'''<ScheduledStopPoint id="TRO:ScheduledStopPoint:{stop}"><Name>{stop}</Name></ScheduledStopPoint>
            <PassengerStopAssignment><ScheduledStopPointRef ref="TRO:ScheduledStopPoint:{stop}"/>
              <QuayRef ref="NSR:Quay:{quay}"/></PassengerStopAssignment>'''
    path = tmp_path / 'fixture.zip'
    line = common + '<PublicationTimestamp>2026-11-18T23:00:00</PublicationTimestamp>' + line
    shared = common + '<PublicationTimestamp>2026-11-18T22:00:00</PublicationTimestamp>' + shared
    raw = zipped(line, shared)
    path.write_bytes(raw)
    bundle = tmp_path / 'current-line20.bundle'
    monkeypatch.setattr(source, 'ARCHIVE_BYTES', len(raw))
    monkeypatch.setattr(source, 'DIGEST', sha256(raw).hexdigest())
    monkeypatch.setenv('V2_ROUTE_ARCHIVE', str(path))
    timestamp = '2026-11-19T12:00:00Z'
    monkeypatch.setenv('V2_ROUTE_OBSERVED_AT', timestamp)
    monkeypatch.setenv('V2_ROUTE_RECHECK_BUNDLE', str(bundle))
    monkeypatch.setenv('APP_MODE', 'private-local')
    monkeypatch.setenv('V2_ROUTE_SOURCE_REFRESH', 'owner')
    return path, timestamp, bundle, line, shared


def test_launch_loads_a_configured_archive_with_dated_departures(pinned):
    source.at_launch()
    operating = source.DATES[0]
    result = source.lookup(operating, datetime(2026, 11, 20, 6, tzinfo=timezone.utc))
    assert (result['coverage'], result['source_state']) == ('complete', 'available')
    calls = result['journeys']['TRO:ServiceJourney:control']['calls']
    assert [call['quay_id'] for call in calls] == ['NSR:Quay:1', 'NSR:Quay:2']
    assert result['provenance']['sha256'] == source.DIGEST
    assert source.RECHECK_BASIS not in result['provenance']
    assert source.lookup(operating, datetime(2026, 11, 20, 12, tzinfo=timezone.utc))['source_state'] == 'stale'


@pytest.fixture
def public_archive(monkeypatch):
    connections = []

    def supply(raw, *, status=200, replace=None, failure=None, on_read=None):
        headers = {'Content-Length': str(len(raw)), 'ETag': '"provider-etag"', 'X-Goog-Generation': '1795129398375999',
                   'Age': '0', 'Date': format_datetime(datetime.now(UTC), usegmt=True)}
        headers.update(replace or {})

        class Response(BytesIO):
            def read1(self, size=-1):
                if on_read is not None:
                    on_read()
                return super().read1(size)

        response = Response(raw)
        response.status = status
        response.headers = HTTPMessage()
        for key, value in headers.items():
            for entry in value if isinstance(value, list) else [value]:
                if entry is not None:
                    response.headers[key] = entry

        class Connection:
            def __init__(self, host, *, timeout):
                assert host == 'storage.googleapis.com' and timeout == 5

            def request(self, method, path, *, headers):
                connections.append((method, path, headers))

            def getresponse(self):
                if failure:
                    raise failure
                return response

            def close(self):
                pass

        monkeypatch.setattr(source, 'HTTPSConnection', Connection)
        return connections

    return supply


@pytest.mark.parametrize('byte_distinct', [False, True])
def test_explicit_current_archive_records_fresh_observation_and_reloads_offline(pinned, public_archive, byte_distinct):
    original, timestamp, bundle, line, shared = pinned
    original_evidence = source.load(original, timestamp)
    raw = original.read_bytes()
    if byte_distinct:
        # Provider publication clocks and out-of-domain bounds can change without changing dated pilot facts.
        raw = zipped(line.replace('T23:00:00', 'T23:59:00').replace('2026-11-20', '2026-11-22'),
                     shared.replace('T22:00:00', 'T22:59:00').replace('2026-11-20', '2026-11-21'), b'new bytes')
        assert sha256(raw).hexdigest() != source.DIGEST
        with pytest.raises(source.InvalidEvidence, match='Pinned archive'):
            candidate = original.with_name('different.zip')
            candidate.write_bytes(raw)
            source.load(candidate, timestamp)
    calls = public_archive(raw)
    started = datetime.now(UTC)
    evidence = source.recheck(original, timestamp, bundle)
    provenance = evidence['provenance']
    checked = datetime.fromisoformat(provenance['checked_at'])
    observed = datetime.fromisoformat(provenance['observed_at'])
    assert started <= checked <= datetime.now(UTC)
    assert observed == datetime.fromisoformat(provenance['response_date']) <= checked
    assert provenance['cache_age_seconds'] == 0
    assert len(calls) == 1
    verb, target, headers = calls[0]
    assert verb == 'GET' and target == '/marduk-production/outbound/netex/rb_tro-aggregated-netex.zip'
    assert headers['Cache-Control'] == 'no-cache'
    assert set(headers) == {'Cache-Control', 'User-Agent', 'Accept-Encoding'}
    assert evidence['days'] == original_evidence['days']
    assert set(evidence['days']) == set(source.DATES)
    assert provenance['sha256'] == sha256(raw).hexdigest() and provenance[source.RECHECK_BASIS] == source.DIGEST
    assert (provenance['etag'], provenance['generation'], provenance['archive_bytes']) == (
        'provider-etag', '1795129398375999', len(raw))
    assert provenance['line_publication'] == ('2026-11-18T23:59:00' if byte_distinct else '2026-11-18T23:00:00')
    assert provenance['shared_publication'] == ('2026-11-18T22:59:00' if byte_distinct else '2026-11-18T22:00:00')
    assert original_evidence == source.load(original, timestamp)
    source.at_launch()
    assert len(calls) == 1 and source.catalogue == evidence
    for operating in source.DATES:
        assert source.lookup(operating, observed + timedelta(hours=24, microseconds=-1))['source_state'] == 'available'
        assert source.lookup(operating, observed + timedelta(hours=24))['source_state'] == 'stale'


def test_cache_age_and_http_date_bound_freshness_without_resetting_the_check_time(pinned, public_archive):
    original, timestamp, bundle, *_ = pinned
    raw = original.read_bytes()
    for age, seconds_ago in [(82, 83), (82, 70)]:
        response_date = (datetime.now(UTC) - timedelta(seconds=seconds_ago)).replace(microsecond=0)
        public_archive(raw, replace={'Age': str(age), 'Date': format_datetime(response_date, usegmt=True)})
        provenance = source.recheck(original, timestamp, bundle)['provenance']
        checked = datetime.fromisoformat(provenance['checked_at'])
        observed = min(checked - timedelta(seconds=age), response_date)
        assert datetime.fromisoformat(provenance['observed_at']) == observed
        assert provenance['response_date'] == response_date.isoformat() and provenance['cache_age_seconds'] == age
        source.at_launch()
        assert source.lookup(source.DATES[0], observed + timedelta(hours=24))['source_state'] == 'stale'


@pytest.mark.parametrize(('document_name', 'before', 'after', 'failure'), [
    ('line', '<ArrivalTime>08:10:00', '<ArrivalTime>08:11:00', 'changes dated'),
    ('line', '<DepartureTime>08:00:00</DepartureTime>',
     '<DepartureTime>08:00:00</DepartureTime><DepartureTime>08:01:00</DepartureTime>', 'complete coverage'),
    ('line', 'ServiceJourney:control" version="1', 'ServiceJourney:control" version="2', 'changes dated'),
    ('line', 'JourneyPattern:out', 'JourneyPattern:new', 'changes dated'),
    ('line', 'JourneyPatternRef ref="TRO:JourneyPattern:out"',
     'JourneyPatternRef ref="TRO:JourneyPattern:out" version="99"', 'Unresolved version'),
    ('shared', 'NSR:Quay:2', 'NSR:Quay:3', 'changes dated'),
    ('shared', '<DayType id="fixture"', '<DayType id="fixture" version="2"', 'changes dated'),
    ('shared', 'OperatingPeriod id="fixture-period"', 'OperatingPeriod id="fixture-period" version="2"', 'changes dated'),
    ('shared', '2026-11-30', '2026-11-28', 'complete coverage'),
])
def test_recheck_rejects_changed_and_partial_archives_without_overwriting_receipt(
        pinned, public_archive, document_name, before, after, failure):
    original, timestamp, bundle, line, shared = pinned
    public_archive(original.read_bytes())
    previous = source.recheck(original, timestamp, bundle)
    retained = bundle.read_bytes()
    if document_name == 'line':
        assert before in line
        line = line.replace(before, after)
    else:
        assert before in shared
        shared = shared.replace(before, after)
    calls = public_archive(zipped(line, shared))
    with pytest.raises(source.InvalidEvidence, match=failure):
        source.recheck(original, timestamp, bundle)
    assert len(calls) == 2 and bundle.read_bytes() == retained
    source.at_launch()
    assert source.catalogue == previous and len(calls) == 2


@pytest.mark.parametrize(('status', 'metadata', 'failure', 'raw_body', 'expected'), [
    (302, {}, None, None, 'HTTP status 302'),
    (304, {}, None, None, 'HTTP status 304'),
    (200, {'Content-Length': '16000001'}, None, None, 'metadata'),
    (200, {'Content-Length': ['30', '30']}, None, None, 'metadata'),
    (200, {'Content-Encoding': 'gzip'}, None, None, 'metadata'),
    (200, {'X-Goog-Generation': 'not-a-generation'}, None, None, 'metadata'),
    (200, {'X-Goog-Generation': source.GENERATION}, None, None, 'original archive generation'),
    (200, {'ETag': None}, None, None, 'metadata'),
    (200, {'ETag': 'W/"weak"'}, None, None, 'metadata'),
    (200, {'Age': '3601'}, None, None, 'metadata'),
    (200, {'Age': '-1'}, None, None, 'metadata'),
    (200, {'Date': 'invalid response date'}, None, None, 'metadata'),
    (200, {'Date': None}, None, None, 'metadata'),
    (200, {'Content-Length': '10'}, None, b'abc', 'body size'),
    (200, {}, SSLError('certificate failed'), None, 'certificate failed'),
])
def test_recheck_rejects_invalid_transport(pinned, public_archive, status, metadata, failure, raw_body, expected):
    original, timestamp, bundle, *_ = pinned
    raw = original.read_bytes()
    calls = public_archive(raw)
    previous = source.recheck(original, timestamp, bundle)
    retained = bundle.read_bytes()
    calls = public_archive(raw if raw_body is None else raw_body, status=status, replace=metadata, failure=failure)
    with pytest.raises((source.InvalidEvidence, SSLError), match=expected):
        source.recheck(original, timestamp, bundle)
    assert len(calls) == 2 and bundle.read_bytes() == retained
    source.at_launch()
    assert source.catalogue == previous and len(calls) == 2


@pytest.mark.parametrize('defect', ['archive', 'checksum', 'size', 'future', 'older', 'offset', 'digest', 'generation',
                                    'etag', 'response-future', 'response-old', 'cache-age'])
def test_launch_falls_back_to_original_if_retained_receipt_is_invalid(pinned, public_archive, defect):
    original, timestamp, bundle, _, _ = pinned
    raw = original.read_bytes()
    calls = public_archive(raw)
    source.recheck(original, timestamp, bundle)
    if defect in {'archive', 'checksum'}:
        saved = bytearray(bundle.read_bytes())
        saved[-1 if defect == 'archive' else 0] ^= 1
        bundle.write_bytes(saved)
    else:
        now = datetime.now(UTC)
        receipt = {'checked_at': now.isoformat(), 'response_date': now.replace(microsecond=0).isoformat(),
                   'cache_age_seconds': 0, 'sha256': source.DIGEST,
                   'size': len(raw), 'etag': 'provider-etag', 'generation': '1234'}
        field, value = {
            'size': ('size', len(raw) + 1), 'future': ('checked_at', (now + timedelta(days=1)).isoformat()),
            'older': ('checked_at', '2026-11-18T12:00:00+00:00'), 'offset': ('checked_at', '2026-11-20T12:00:00+01:00'),
            'digest': ('sha256', 'a' * 64), 'generation': ('generation', 'bad'), 'etag': ('etag', '\n'),
            'response-future': ('response_date', (now + timedelta(minutes=2)).isoformat()),
            'response-old': ('response_date', (now - timedelta(hours=2)).isoformat()), 'cache-age': ('cache_age_seconds', True),
        }[defect]
        receipt[field] = value
        source.write_recheck(bundle, raw, receipt)
    source.at_launch()
    assert len(calls) == 1
    assert source.catalogue == source.load(original, timestamp)


def test_recheck_requires_owner_and_complete_pinned_archive(pinned, public_archive, monkeypatch):
    original, timestamp, bundle, _, _ = pinned
    calls = public_archive(original.read_bytes())
    monkeypatch.delenv('V2_ROUTE_SOURCE_REFRESH')
    with pytest.raises(source.InvalidEvidence, match='owner sandbox'):
        source.recheck(original, timestamp, bundle)
    monkeypatch.setenv('V2_ROUTE_SOURCE_REFRESH', 'owner')
    monkeypatch.setattr(source, 'EXPECTED', dict.fromkeys(source.DATES, 2))
    with pytest.raises(source.InvalidEvidence, match='Pinned archive does not have complete coverage'):
        source.recheck(original, timestamp, bundle)
    assert calls == [] and not bundle.exists()


def test_launch_rejects_changed_facts_even_if_the_retained_archive_matches_its_receipt(pinned, public_archive):
    original, timestamp, bundle, line, shared = pinned
    calls = public_archive(original.read_bytes())
    receipt = source.recheck(original, timestamp, bundle)['provenance']
    raw = zipped(line.replace('<ArrivalTime>08:10:00', '<ArrivalTime>08:11:00'), shared)
    metadata = {key: receipt[key] for key in ('checked_at', 'response_date', 'cache_age_seconds', 'etag', 'generation')}
    source.write_recheck(bundle, raw, {**metadata, 'sha256': sha256(raw).hexdigest(), 'size': len(raw)})
    source.at_launch()
    assert len(calls) == 1
    assert source.catalogue == source.load(original, timestamp)


def test_recheck_records_header_clock_before_receiving_the_body(pinned, public_archive, monkeypatch):
    raw = pinned[0].read_bytes()
    at_headers = datetime(2026, 11, 20, 12, tzinfo=UTC)
    current = at_headers

    class Clock(datetime):
        @classmethod
        def now(cls, timezone):
            return current.astimezone(timezone)

    def transfer():
        nonlocal current
        current = at_headers + timedelta(seconds=20)

    monkeypatch.setattr(source, 'datetime', Clock)
    public_archive(raw, replace={'Age': '60', 'Date': format_datetime(at_headers, usegmt=True)}, on_read=transfer)
    _, receipt = source.download_current()
    assert current > at_headers and receipt['checked_at'] == at_headers.isoformat()


def test_older_recheck_and_concurrent_writer_preserve_the_retained_bundle(pinned, public_archive):
    original, timestamp, bundle, *_ = pinned
    raw = original.read_bytes()
    calls = public_archive(raw)
    source.recheck(original, timestamp, bundle)
    retained = bundle.read_bytes()
    with bundle.with_suffix('.lock').open('a+b') as lock:
        source.lock_recheck(lock)
        with pytest.raises(source.InvalidEvidence, match='already being checked'):
            source.recheck(original, timestamp, bundle)
    assert len(calls) == 1
    earlier = (datetime.now(UTC) - timedelta(minutes=5)).replace(microsecond=0)
    public_archive(raw, replace={'Age': '300', 'Date': format_datetime(earlier, usegmt=True)})
    with pytest.raises(source.InvalidEvidence, match='older than the retained'):
        source.recheck(original, timestamp, bundle)
    assert len(calls) == 2 and bundle.read_bytes() == retained


def test_recheck_rejects_unexpected_compression_with_a_readable_error(pinned, public_archive):
    original, timestamp, bundle, line, shared = pinned
    public_archive(zipped(line, shared, compression=ZIP_LZMA))
    with pytest.raises(source.InvalidEvidence, match='Unexpected archive inventory'):
        source.recheck(original, timestamp, bundle)
    assert not bundle.exists()
