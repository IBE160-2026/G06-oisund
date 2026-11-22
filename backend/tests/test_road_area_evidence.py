from datetime import date

import pytest

from app.road_area_evidence import edges, registered_speed


DAY = date(2026, 12, 10)
BOX = (18.7, 69.59, 19.14, 69.77)


def span(speed=70, start=0, end=1, kind=105, lanes=None, **validity):
    return {'type': kind, 'start': start, 'end': end, 'speed': speed,
            'lanes': [] if lanes is None else lanes, 'orientation': 'MOT',
            'valid_from': '2024-07-08', 'valid_until': None, **validity}


def road(reference, sequence, origin, destination, fields, **changes):
    return {'referanse': reference, 'veglenkesekvensid': sequence, 'startnode': origin, 'sluttnode': destination,
            'startposisjon': 0, 'sluttposisjon': 1, 'feltoversikt': fields, 'lengde': 12,
            'geometri': {'srid': 4326, 'wkt': 'LINESTRING (69.68 18.92, 69.6801 18.9201)'},
            'metadata': {'startdato': '2024-07-08'}, **changes}


def test_airport_roundabout_keeps_lane_free_exit_and_both_directions():
    rows = [road('1125950-1-10', 1125950, '3251244', '3251245', ['1', '3']),
            road('1125950-11-10', 1125950, '3251245', '1138789', ['1', '3']),
            road('1126506-1-8', 1126506, '3251245', '2834984', [], lengde=4.042,
                 superstedfesting={'veglenkesekvensid': 1125938, 'startposisjon': 0,
                                   'sluttposisjon': .05021067, 'retning': 'MED'})]
    result, rejected = edges(rows, {1125950: [span()], 1125938: [span(50)]}, {}, BOX, DAY)
    assert not rejected
    by_id = {row['id']: row for row in result}
    incoming = by_id['1125950-1-10-med']
    assert incoming['kmh'] == 70
    assert incoming['successors'] == ['1125950-11-10-med', '1126506-1-8-med']
    outward, reverse = (by_id['1126506-1-8-' + suffix] for suffix in ('med', 'mot'))
    assert (outward['from'], outward['to'], reverse['from'], reverse['to']) == ('3251245', '2834984', '2834984', '3251245')
    assert not outward['direction_verified'] and not reverse['direction_verified']
    assert outward['kmh'] is None and reverse['kmh'] is None
    assert outward['parent_evidence']['kmh'] == 50
    assert outward['id'] not in reverse['successors']


def test_unusable_geometry_preserves_the_connection_at_known_endpoints():
    rows = [road('main', 1, 'a', 'b', ['1']), road('onward', 2, 'b', 'c', ['1']),
            road('exit', 3, 'b', 'd', [], geometri={'srid': 4326, 'wkt': 'LINESTRING (69.68 18.92)'}),
            road('unrelated', 4, 'e', 'f', ['2K'])]
    result, rejected = edges(rows, {1: [span()], 2: [span(50)], 4: [span(30)]}, {}, BOX, DAY)
    by_id = {row['id']: row for row in result}
    assert rejected == {'unresolved_geometry_or_endpoints': 1}
    assert by_id['main-med']['successors'] == ['exit-unresolved', 'onward-med']
    assert by_id['main-med']['kmh'] == 70
    assert by_id['unrelated-mot']['kmh'] == 30


def test_self_loop_is_a_possible_continuation_even_with_an_exit():
    rows = [road('loop', 1, 'junction', 'junction', ['1']), road('exit', 2, 'junction', 'out', ['1'])]
    graph, _ = edges(rows, {1: [span(50)], 2: [span(30)]}, {}, BOX, DAY)
    assert graph[0]['successors'] == ['exit-med', 'loop-med']


def test_parent_variable_limit_disables_current_child_candidate():
    rows = [road('child', 1, 'a', 'b', ['1'], superstedfesting={
        'veglenkesekvensid': 2, 'startposisjon': .3, 'sluttposisjon': .5, 'retning': 'MOT',
    })]
    graph, _ = edges(rows, {1: [span()], 2: [span()]}, {2: [span(60, start=.4, kind=721)]}, BOX, DAY)
    assert graph[0]['direction_verified']
    assert graph[0]['kmh'] is None
    assert graph[0]['speed_basis'] == 'parent-variable-limit'


def test_exact_dated_direction_rule_can_resolve_a_lane_free_link():
    rows = [road('connector', 1, 'a', 'b', [])]
    rule = dict(span(kind=977), orientation='MED')
    graph, _ = edges(rows, {1: [span(50)]}, {}, BOX, DAY, direction_index={1: [rule]})
    assert [(edge['id'], edge['direction_basis'], edge['kmh']) for edge in graph] == [
        ('connector-med', 'registered-direction-rule', 50),
    ]


@pytest.mark.parametrize('rules', [
    [dict(span(kind=977, end=.5), orientation='MED')],
    [dict(span(kind=977), orientation='MED'), span(kind=977)],
    [span(kind=977)],
])
def test_partial_or_conflicting_restriction_keeps_both_possible_directions(rules):
    rows = [road('connector', 1, 'a', 'b', ['1'])]
    graph, _ = edges(rows, {1: [span(50)]}, {}, BOX, DAY, direction_index={1: rules})
    assert {edge['id'] for edge in graph} == {'connector-med', 'connector-mot'}
    assert all(edge['kmh'] is None and edge['direction_basis'] == 'unresolved-direction-rule' for edge in graph)


@pytest.mark.parametrize('records,expected', [
    ([span(end=.5), span(start=.5)], (70, 'registered-static')),
    ([span(end=.5), span(50, start=.5)], (None, 'change-within-edge')),
    ([span(end=.4), span(start=.5)], (None, 'incomplete-limit')),
    ([span(), span(50, start=.5)], (None, 'conflicting-limits')),
    ([span(), span(60, kind=721)], (None, 'variable-limit')),
    ([span(), span(60, lanes=['2'])], (None, 'field-specific')),
    ([span(), span(60, valid_until='2026-12-10')], (70, 'registered-static')),
    ([span(50, effective_dates=['2026-12-11'])], (None, 'incomplete-limit')),
    ([span(valid_from=None)], (None, 'unresolved-validity')),
    ([span(start=-.1, end=1.1)], (None, 'invalid-placement')),
    ([span(), span(start=None)], (None, 'invalid-placement')),
])
def test_registered_speed_requires_exact_dated_general_coverage(records, expected):
    assert registered_speed(0, 1, records, DAY) == expected
