"""The public road situation feed contributes restrictions, never numeric limits."""

from datetime import UTC, datetime, timedelta
from copy import deepcopy
from email.utils import format_datetime
import json

import pytest

from app import road_situation_source as situations


NOW = datetime(2026, 11, 30, 8, tzinfo=UTC)


def snapshot():
    return {
        'type': 'FeatureCollection', 'numberMatched': 1, 'numberReturned': 1, 'totalFeatures': 1,
        'timeStamp': NOW.isoformat(),
        'crs': {'type': 'name', 'properties': {'name': 'urn:ogc:def:crs:EPSG::4326'}},
        'features': [{'type': 'Feature', 'geometry': {'type': 'LineString',
                                                     'coordinates': [[18.925, 69.668], [18.945, 69.645]]},
                      'properties': {'@featureType': 'geoJsonSituationSimple', 'recordId': 'report-1',
                                     'situationId': 'public-roadwork-1', 'roadNumber': 'F862',
                                     'startTime': (NOW - timedelta(days=1)).isoformat(),
                                     'endTime': (NOW + timedelta(hours=1)).isoformat(), 'speedLimit': 30}}],
    }


def parse(value, now=NOW):
    return situations.parse(json.dumps(value).encode(), format_datetime(NOW, usegmt=True), now)


def test_dated_bounds_are_local_even_on_a_shared_road():
    result = parse(snapshot())
    event, = result['events']
    assert event['road'] == 'F862'
    assert 'speedLimit' not in event and 'kmh' not in event
    assert situations.active([event], NOW) == [event]
    assert situations.active([event], NOW + timedelta(hours=1)) == []
    assert situations.affects(event, 'FV862 S1D1 m1234', [18.93, 69.66, 18.94, 69.67])
    assert not situations.affects(event, 'FV862 S1D1 m3210', [18.73, 69.63, 18.75, 69.65])


def test_incomplete_or_stale_receipt_is_rejected():
    with pytest.raises(ValueError, match='incomplete'):
        parse({**snapshot(), 'numberMatched': 2})
    with pytest.raises(ValueError, match='freshness'):
        parse(snapshot(), NOW + timedelta(minutes=6))
    value = snapshot()
    value['features'][0]['geometry']['coordinates'] = [[69.668, 18.925], [69.645, 18.945]]
    with pytest.raises(ValueError, match='outside the requested'):
        parse(value)
    value['features'][0]['geometry']['coordinates'] = [18.925, 69.668]
    with pytest.raises(ValueError, match='coordinates'):
        parse(value)


def test_reported_line_excludes_distant_roads_inside_its_box():
    event, = parse(snapshot())['events']
    assert situations.affects_edge(event, 'FV862', [[18.926, 69.666], [18.927, 69.666]])
    assert not situations.affects_edge(event, 'FV862', [[18.926, 69.646], [18.927, 69.646]])


def test_geometry_budgets_mark_unknown_and_preserve_ordinary_matching(monkeypatch):
    monkeypatch.setattr(situations, 'MAX_EVENT_POINTS', 2)
    monkeypatch.setattr(situations, 'MAX_SNAPSHOT_POINTS', 4)
    feature = snapshot()['features'][0]
    normal, = parse(snapshot())['events']
    near = [[18.926, 69.666], [18.927, 69.666]]
    far = [[18.926, 69.646], [18.927, 69.646]]
    assert situations.affects_edge(normal, 'FV862', near, budget=situations.GeometryBudget(5))
    assert not situations.affects_edge(normal, 'FV862', far, budget=situations.GeometryBudget(5))
    assert situations.affects_edge(normal, 'FV862', far, budget=situations.GeometryBudget(4))

    value = snapshot() | {'numberMatched': 3, 'numberReturned': 3, 'totalFeatures': 3}
    extra = deepcopy(feature)
    extra['properties']['recordId'] = 'report-2'
    extra['geometry']['coordinates'].append([18.95, 69.65])
    final = deepcopy(feature)
    final['properties']['recordId'] = 'report-3'
    value['features'] = [feature, extra, final]
    original, oversized, beyond_total = parse(value)['events']
    assert original == normal
    for event in (oversized, beyond_total):
        assert event['geometry_unqualified']
        assert event['bounds'] == situations.FIELD
        assert event['linework'] is None
        assert situations.affects_edge(event, 'FV862', far)


def test_legacy_geometry_uses_saved_bounds_when_over_budget(monkeypatch):
    normal, = parse(snapshot())['events']
    monkeypatch.setattr(situations, 'MAX_EVENT_POINTS', 1)
    event, = situations.bounded_events([normal])
    assert event['geometry_unqualified'] and event['linework'] is None
    assert event['bounds'] == normal['bounds']
    assert situations.affects_edge(event, 'FV862', [[18.926, 69.646], [18.927, 69.646]])
    assert not situations.affects_edge(event, 'FV862', [[18.73, 69.63], [18.75, 69.64]])
