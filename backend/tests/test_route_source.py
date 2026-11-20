"""Independent controls for bounded NeTEx calendar, time and occurrence resolution."""

from datetime import date, datetime, timezone
from hashlib import sha256
from xml.etree import ElementTree as XML
from zipfile import ZipFile

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


def test_launch_loads_a_configured_archive_with_dated_departures(monkeypatch, tmp_path):
    operating = date(2026, 11, 23)
    monkeypatch.setattr(source, 'DATES', (operating,))
    monkeypatch.setattr(source, 'EXPECTED', {operating: 1})
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
        <DayType id="fixture"/><DayTypeAssignment><DayTypeRef ref="fixture"/><Date>2026-11-23</Date></DayTypeAssignment>
        <DestinationDisplay id="TRO:DestinationDisplay:last"><FrontText>Control destination</FrontText></DestinationDisplay>'''
    for stop, quay in [('first', '1'), ('last', '2')]:
        shared += f'''<ScheduledStopPoint id="TRO:ScheduledStopPoint:{stop}"><Name>{stop}</Name></ScheduledStopPoint>
            <PassengerStopAssignment><ScheduledStopPointRef ref="TRO:ScheduledStopPoint:{stop}"/>
              <QuayRef ref="NSR:Quay:{quay}"/></PassengerStopAssignment>'''
    path = tmp_path / 'fixture.zip'
    with ZipFile(path, 'w') as archive:
        for name, content in ((source.LINE_MEMBER, line), (source.SHARED_MEMBER, shared)):
            archive.writestr(name, XML.tostring(document(common + content)))
        for number in range(169):
            archive.writestr(f'unrelated-{number}.xml', '<unused/>')
    raw = path.read_bytes()
    monkeypatch.setattr(source, 'ARCHIVE_BYTES', len(raw))
    monkeypatch.setattr(source, 'DIGEST', sha256(raw).hexdigest())
    monkeypatch.setenv('V2_ROUTE_ARCHIVE', str(path))
    monkeypatch.setenv('V2_ROUTE_OBSERVED_AT', '2026-11-19T12:00:00Z')
    source.at_launch()
    result = source.lookup(operating, datetime(2026, 11, 20, 6, tzinfo=timezone.utc))
    assert (result['coverage'], result['source_state']) == ('complete', 'available')
    calls = result['journeys']['TRO:ServiceJourney:control']['calls']
    assert [call['quay_id'] for call in calls] == ['NSR:Quay:1', 'NSR:Quay:2']
    assert result['provenance']['sha256'] == source.DIGEST
    assert source.lookup(operating, datetime(2026, 11, 20, 12, tzinfo=timezone.utc))['source_state'] == 'stale'
