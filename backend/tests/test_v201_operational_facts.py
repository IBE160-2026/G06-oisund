from datetime import UTC, date, datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest

from app import import_route_matching as matching
from app.automatic_notice_relevance import city_scope, operational_status
from app.draft_domain import Activity


DAY = date(2026, 11, 30)
NOW = datetime(2026, 11, 30, 9, tzinfo=UTC)


def call(position, name, arrival, departure):
    def clock(value):
        return {'utc': value} if value else None
    return dict(position=position, name=name, arrival=clock(arrival), departure=clock(departure), headsign='Hamna via sentrum')


def journey():
    return dict(private_code='001036', direction='outbound', journey_id='TRO:ServiceJourney:example', headsign='Hamna',
                calls=[call(1, 'Solligården', None, '2026-11-30T22:51Z'),
                       call(2, 'Tromsø lufthavn', '2026-11-30T22:59Z', '2026-11-30T23:00Z'),
                       call(3, 'Hamna skole øst', '2026-11-30T23:06Z', None)])


@pytest.mark.parametrize(('change', 'catalogue', 'outcome'), [
    ({}, 'one', 'matched'),
    ({'trip': '1035'}, 'one', 'trip-not-found'),
    ({'to_place': 'Hamna skole nord'}, 'one', 'conflicting-facts'),
    ({'direction': 'Inngående'}, 'one', 'conflicting-facts'),
    ({}, 'two', 'ambiguous'),
    ({}, 'absent', 'catalogue-missing'),
    ({'direction': 'Manuelt angitt'}, 'one', 'matched'),
])
def test_match_requires_turn_number_and_ordered_endpoints_across_midnight(monkeypatch, change, catalogue, outcome):
    published = {'TRO:ServiceJourney:example': journey()}
    if catalogue == 'two':
        published['TRO:ServiceJourney:alternative'] = {**journey(), 'journey_id': 'TRO:ServiceJourney:alternative'}

    def lookup(_conn, day, _now, line):
        assert line == '28'
        if day == DAY and catalogue != 'absent':
            return {'coverage': 'complete', 'source_state': 'available', 'journeys': published}
        return {'coverage': 'unavailable', 'source_state': 'unavailable', 'journeys': {}}

    monkeypatch.setattr(matching.route_catalogue, 'lookup', lookup)
    values = dict(id=uuid4(), type='trip', direction=None, line='28', trip='1036',
                  from_place='Flyplassen', to_place='Hamna skole øst', start='2026-11-30T23:59+01:00', end='2026-12-01T00:06+01:00')
    activity = Activity(**(values | change))
    result, match = matching.activity_match(None, SimpleNamespace(service_date=DAY), activity, NOW, {})
    assert result == outcome
    if match:
        assert match[2:] == (2, 3)
        assert matching.direction_label(match[1], 2) == ('Utgående', 'Hamna via sentrum')
    else:
        assert match is None


def test_service_date_can_differ_from_the_calendar_date_of_the_started_trip(monkeypatch):
    published = journey()
    monkeypatch.setattr(matching.route_catalogue, 'lookup', lambda conn, day, now, line: {
        'coverage': 'complete', 'source_state': 'available',
        'journeys': {published['journey_id']: published} if day == DAY else {},
    })
    activity = Activity(id=uuid4(), type='trip', line='28', trip='1036', from_place='Flyplassen',
                        to_place='Hamna skole øst', start='2026-12-01T00:00+01:00', end='2026-12-01T00:06+01:00')
    assert matching.activity_match(None, SimpleNamespace(service_date=date(2026, 12, 1)), activity, NOW, {})[0] == 'matched'


@pytest.mark.parametrize(('selector', 'value', 'expected'), [
    ('LineRef', 'TRO:Line:1_28', True), ('LineRef', 'TRO:Line:1_150', False),
    ('StopPointRef', 'NSR:StopPlace:55902', True), ('QuayRef', 'NSR:Quay:90000', False),
    ('AllLines', 'true', True),
])
def test_scope_requires_city_line_stop_or_explicit_broad_scope(selector, value, expected):
    assert city_scope({'affects': [{'kind': selector, 'value': value, 'children': []}]}, {'NSR:StopPlace:55902'}) is expected


def test_source_end_is_exclusive_even_without_a_start_and_distinct_from_missing_end():
    end = NOW.isoformat()
    active = {'progress': 'open', 'windows': [{'start': '2026-11-30T08:00Z', 'end': '2026-11-30T10:00Z'}]}
    assert operational_status(active, NOW) == 'active'
    assert operational_status({**active, 'progress': 'closed'}, NOW) is None
    assert operational_status({'progress': 'open', 'windows': [{'start': None, 'end': end}]}, NOW) is None
    assert operational_status({'progress': 'open', 'windows': [{'start': '2026-11-30T08:00Z', 'end': None}]}, NOW) == 'uncertain'
    assert operational_status({'progress': 'open', 'windows': [{'start': '2026-11-30T10:00Z', 'end': '2026-11-30T11:00Z'}]}, NOW) == 'upcoming'
