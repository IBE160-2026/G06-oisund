from app.automatic_notice_relevance import city_scope
from app.notice_geography import automatic_scope, manual_scope, scope_on_route


def stop(key):
    return {'ref': f'NSR:Quay:{key}', 'name': key}


def journey(keys, direction='outbound', first=1, last=None, variant='main'):
    return {
        'journey_id': f'TRO:ServiceJourney:{variant}', 'line_id': 'TRO:Line:1_28',
        'route_id': f'TRO:Route:{variant}', 'pattern_id': f'TRO:JourneyPattern:{variant}',
        'direction': direction, 'status': 'compatible', 'start_position': first,
        'end_position': last or len(keys),
        'calls': [{'position': index, 'quay_id': stop(key)['ref'],
                   'stop_place_id': f'NSR:StopPlace:{key}'}
                  for index, key in enumerate(keys, 1)],
    }


def node(kind, value=None, *children):
    return {'kind': kind, 'value': value, 'children': list(children)}


def test_section_with_skipped_stop_respects_order_slice_and_variant():
    direct = journey('AXBC')
    parallel = journey('AYBC', variant='tunnel')
    leaves_before_section = journey('APD', variant='turns_early')
    reverse = journey('CBXA', 'inbound', variant='reverse')
    variants = [direct, parallel, leaves_before_section, reverse]
    scope = {'kind': 'section', 'start': stop('A'), 'end': stop('B'), 'cancelled': [stop('X')]}
    assert scope_on_route(scope, direct, variants)['scope'] == 'uncertain'
    explicit = {'line_scope': 'selected', 'line_tags': ['28'], 'geography': {**scope, 'route_ref': direct['route_id']}}
    assert manual_scope(explicit, {'line': '28'}, direct, variants)['cancelled'] == [2]
    assert manual_scope(explicit, {'line': '28'}, parallel, variants) is None
    scope['via'] = [stop('X')]
    assert scope_on_route(scope, direct, variants) == {
        'scope': 'section', 'positions': [1, 2, 3], 'cancelled': [2], 'from': 'A', 'to': 'B',
    }
    for other in variants[1:]:
        assert scope_on_route(scope, other, variants) is None
    assert scope_on_route(scope, {**direct, 'start_position': 3}, variants) is None
    assert scope_on_route(scope, {**direct, 'start_position': 2}, variants)['positions'] == [2, 3]
    assert scope_on_route(scope, {**direct, 'route_id': None}, variants)['scope'] == 'uncertain'


def test_exact_platform_at_last_and_first_stop_and_qualified_direction():
    arriving = journey('AQ', 'inbound')
    departing = journey('QZ', variant='return')
    branch = node('AffectedStopPoint', None, node('QuayRef', stop('Q')['ref']))
    source = {'affects': [branch]}
    assert list(automatic_scope(source, arriving, ()))[0]['positions'] == [2]
    assert list(automatic_scope(source, departing, ()))[0]['positions'] == [1]
    assert list(automatic_scope(source, journey('YZ'), ())) == []
    source['affects'].append(node('DirectionRef', 'TRO:Direction:outbound'))
    assert list(automatic_scope(source, arriving, ())) == []
    assert list(automatic_scope(source, departing, ()))[0]['positions'] == [1]


def test_structured_entur_section_and_explicit_stop_consequence():
    route = journey('AXBC')
    alternative = journey('AYBC', variant='strict-parallel')
    def endpoint(kind, key):
        return node(kind, None, node('QuayRef', stop(key)['ref']))
    section = node('AffectedSection', None, endpoint('FromStop', 'A'), endpoint('ToStop', 'B'))
    consequence = node('Consequence', None, node('Condition', 'notServed'),
                       node('QuayRef', stop('X')['ref']), node('DirectionRef', 'TRO:Direction:outbound'))
    source = {'affects': [node('AffectedLine', None, node('LineRef', route['line_id']),
                               node('RouteRef', route['route_id']), section)], 'consequences': [consequence]}
    assert list(automatic_scope(source, route, (route, alternative))) == [
        {'scope': 'section', 'positions': [1, 2, 3], 'cancelled': [2], 'from': stop('A')['ref'], 'to': stop('B')['ref']},
    ]
    assert list(automatic_scope(source, alternative, (route, alternative))) == []


def test_area_without_a_stop_and_legacy_line_scope():
    source = {'affects': [node('AreaName', 'Tromsø sentrum')]}
    assert city_scope(source, set())
    assert list(automatic_scope(source, None, ())) == [
        {'scope': 'area', 'area': 'Tromsø sentrum', 'positions': [], 'cancelled': []},
    ]
    assert not city_scope({'affects': [node('LineRef', 'TRO:Line:1_150')]}, set())
    assert manual_scope({'line_scope': 'selected', 'line_tags': ['28']}, {'line': '28'}, None, ()) == {
        'scope': 'line', 'positions': [], 'cancelled': [],
    }
    assert manual_scope({'line_scope': 'selected', 'line_tags': ['28']}, {'line': '24'}, None, ()) is None
