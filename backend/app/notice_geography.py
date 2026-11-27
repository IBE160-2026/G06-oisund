"""Structured applicability of a traffic notice to a frozen Entur departure."""

from typing import Literal

from pydantic import Field, model_validator

from .draft_domain import StrictModel
from .import_route_matching import stop_name
from .route_catalogue import code_for


class NoticeStop(StrictModel):
    ref: str = Field(pattern=r'^(?:NSR:(?:StopPlace|Quay)|TRO:ScheduledStopPoint):[A-Za-z0-9_.:/-]{1,140}$')
    name: str = Field(min_length=1, max_length=180)


class NoticeGeography(StrictModel):
    kind: Literal['stops', 'section', 'area']
    direction: Literal['outbound', 'inbound'] | None = None
    stops: list[NoticeStop] = Field(default_factory=list, max_length=24)
    cancelled: list[NoticeStop] = Field(default_factory=list, max_length=24)
    start: NoticeStop | None = None
    end: NoticeStop | None = None
    via: list[NoticeStop] = Field(default_factory=list, max_length=12)
    route_ref: str | None = Field(default=None, pattern=r'^TRO:Route:[A-Za-z0-9_./-]{1,200}$')
    area: str | None = Field(default=None, min_length=1, max_length=120)

    @model_validator(mode='after')
    def valid_shape(self):
        if self.kind == 'area':
            valid = self.area and self.area.strip() and not (self.stops or self.cancelled or self.start or self.end or self.via or self.direction)
        elif self.kind == 'stops':
            valid = self.stops and not (self.area or self.start or self.end or self.via)
            valid = valid and {stop.ref for stop in self.cancelled} <= {stop.ref for stop in self.stops}
        else:
            valid = self.start and self.end and self.start.ref != self.end.ref and not (self.area or self.stops)
        if not valid or self.route_ref and self.kind != 'section' or any(len({stop.ref for stop in stops}) != len(stops) for stops in (self.stops, self.cancelled, self.via)):
            raise ValueError('Choose a consistent set of stops, a section or a named area')
        return self


CITY_AREAS = {'tromso', 'tromso sentrum', 'tromso bybuss', 'tromsoya', 'kvaloya', 'tromsdalen',
              'kvaloysletta', 'fastlandet'}


def route_call_refs(call):
    return {call.get(key) for key in ('quay_id', 'stop_place_id', 'scheduled_stop_point_id', 'occurrence_id')} - {None}


def segments(calls, start, end, via=()):
    references = [route_call_refs(call) for call in calls]
    for first, first_refs in enumerate(references):
        if start not in first_refs:
            continue
        remaining = iter(via)
        expected = next(remaining, None)
        for last in range(first + 1, len(references)):
            if end in references[last] and expected is None:
                yield first, last
            if expected in references[last]:
                expected = next(remaining, None)


def ordered_shape(route, first, last):
    # A NeTEx RouteRef is stronger evidence than geographic proximity. Keep the
    # ordered calls as well, so variants on a shared RouteRef stay distinct.
    return route.get('route_id'), tuple(
        call.get('quay_id') or call.get('stop_place_id') or call.get('scheduled_stop_point_id')
        for call in route['calls'][first:last + 1]
    )


def positions(calls, refs, first, last):
    return [call['position'] for call in calls[first:last + 1] if refs & route_call_refs(call)]


def scope_on_route(scope, route, variants=(), route_refs=(), pattern_refs=(), journey_refs=()):
    if not route or route.get('status') == 'incompatible':
        return None
    if (scope.get('direction') and route.get('direction') != scope['direction']
            or route_refs and route.get('route_id') not in route_refs
            or pattern_refs and route.get('pattern_id') not in pattern_refs
            or journey_refs and route.get('journey_id') not in journey_refs):
        return None
    calls = route['calls']
    left = route.get('start_position', 1) - 1
    right = route.get('end_position', len(calls)) - 1
    cancelled_refs = {stop['ref'] for stop in scope.get('cancelled', ())}
    if scope['kind'] == 'stops':
        affected = positions(calls, {stop['ref'] for stop in scope['stops']}, left, right)
        if affected:
            return {'scope': 'stops', 'positions': affected, 'cancelled': positions(calls, cancelled_refs, left, right)}
        return None
    start, end = scope['start'], scope['end']
    via = [stop['ref'] for stop in scope.get('via', ())]
    bounds = [(first, last) for first, last in segments(calls, start['ref'], end['ref'], via)
              if max(first, left) < min(last, right)]
    if not bounds:
        return None
    if len(bounds) != 1:
        return {'scope': 'uncertain', 'positions': [], 'cancelled': []}
    origin, destination = bounds[0]
    if not (route_refs or pattern_refs or journey_refs):
        same_direction = [variant for variant in variants if variant.get('direction') == route.get('direction')]
        expected = ordered_shape(route, origin, destination)
        if not same_direction or any(
            ordered_shape(variant, first, last) != expected
            for variant in same_direction for first, last in segments(variant['calls'], start['ref'], end['ref'], via)
        ):
            return {'scope': 'uncertain', 'positions': [], 'cancelled': []}
    return {'scope': 'section', 'positions': list(range(max(origin, left) + 1, min(destination, right) + 2)),
            'cancelled': positions(calls, cancelled_refs, max(origin, left), min(destination, right)),
            'from': start['name'], 'to': end['name']}


def manual_scope(row, activity, route, variants):
    scope = row.get('geography')
    code = code_for(activity.get('line'))
    if row['line_scope'] != 'all' and code not in {code_for(value) for value in row['line_tags']}:
        return None
    if scope is None:
        return {'scope': 'line' if row['line_scope'] != 'all' else 'network', 'positions': [], 'cancelled': []}
    if scope['kind'] == 'area':
        return {'scope': 'area', 'area': scope['area'], 'positions': [], 'cancelled': []}
    route_refs = {scope['route_ref']} if scope.get('route_ref') else ()
    return scope_on_route(scope, route, variants, route_refs=route_refs)


STOP_REFS = {'StopPointRef', 'StopPlaceRef', 'QuayRef', 'ScheduledStopPointRef'}
START_REFS = {'FirstStopPointRef', 'StartStopPointRef', 'FromStopPointRef', 'StartStopPlaceRef', 'FromStopPlaceRef', 'StartQuayRef', 'FromQuayRef'}
END_REFS = {'LastStopPointRef', 'EndStopPointRef', 'ToStopPointRef', 'EndStopPlaceRef', 'ToStopPlaceRef', 'EndQuayRef', 'ToQuayRef'}
JOURNEY_REFS = {'VehicleJourneyRef', 'DatedVehicleJourneyRef', 'ServiceJourneyRef'}
BRANCHES = {'AffectedLine', 'AffectedVehicleJourney', 'AffectedRoute'}
SECTION_NODES = {'AffectedSection', 'AffectedRouteSection'}
SECTION_KEYS = SECTION_NODES | START_REFS | END_REFS


def endpoint_refs(nodes, kinds, containers):
    refs = values(nodes, kinds)
    for node in walk(nodes):
        if node['kind'] in containers:
            refs |= values(node['children'], STOP_REFS)
    return refs


def has_section(nodes):
    return any(node['kind'] in SECTION_KEYS for node in walk(nodes))


def matches_direction(choices, route):
    if not choices:
        return True
    direction = route.get('direction') or ''
    return bool(choices & {direction, route.get('direction_id'), 'TRO:Direction:' + direction})


def walk(nodes):
    for node in nodes:
        yield node
        yield from walk(node['children'])


def values(nodes, kinds):
    return {node['value'] for node in walk(nodes) if node['kind'] in kinds and node['value']}


def recognized_area(source):
    candidates = values(source.get('affects', []), {'AreaName', 'PlaceName', 'AffectedAreaName', 'LocationName'})
    explicit = next((value for value in sorted(candidates) if stop_name(value) in CITY_AREAS), None)
    named_summary = (item.get('text', '') for item in source.get('summary') or ())
    return explicit or next((name for name in named_summary if stop_name(name) in CITY_AREAS), None)


def scopes(nodes, ancestors=None):
    # Each affected line/route/journey is a separate branch. A sibling's
    # stop/direction qualifier cannot widen another branch.
    current = []
    children = []
    for node in nodes:
        if node['kind'] in BRANCHES:
            children.append(node['children'])
        elif any(child['kind'] in BRANCHES for child in walk(node['children'])):
            children.append(node['children'])
        else:
            current.append(node)
    bound = [*(ancestors or ()), *current]
    if children:
        for branch in children:
            yield from scopes(branch, bound)
    elif bound:
        yield bound


def automatic_scope(source, route, variants):
    area = recognized_area(source)
    branches = list(scopes(source.get('affects', [])))
    if not branches and area:
        yield {'scope': 'area', 'area': area, 'positions': [], 'cancelled': []}
        return
    for branch in branches:
        lines = values(branch, {'LineRef'})
        directions = values(branch, {'DirectionRef', 'DirectionName', 'Direction'})
        route_refs = values(branch, {'RouteRef'})
        pattern_refs = values(branch, {'JourneyPatternRef'})
        journey_refs = values(branch, JOURNEY_REFS)
        qualifiers = lines or directions or route_refs or pattern_refs or journey_refs
        if qualifiers and (not route or lines and route.get('line_id') not in lines
                           or route_refs and route.get('route_id') not in route_refs
                           or pattern_refs and route.get('pattern_id') not in pattern_refs
                           or journey_refs and route.get('journey_id') not in journey_refs):
            continue
        if not matches_direction(directions, route or {}):
            continue
        affected = set()
        cancelled = set()
        sections = [node for node in walk(branch) if node['kind'] in SECTION_NODES]
        for group in walk(branch):
            if group['kind'] not in {'AffectedStopPoint', 'AffectedStopPlace', 'AffectedQuay'}:
                continue
            refs = values([group], STOP_REFS)
            affected.update(refs)
            conditions = values([group], {'StopCondition', 'StopStatus', 'Cancellation'})
            if {value.lower().replace('-', '') for value in conditions} & {'notserved', 'cancelled', 'closed', 'true', 'notstopping'}:
                cancelled.update(refs)
        def label(ref):
            return next((call.get('name') for call in (route or {}).get('calls', ()) if ref in route_call_refs(call)), None) or ref

        for consequence in source.get('consequences') or ():
            tree = [consequence]
            impacts = values(tree, {'Condition', 'StopCondition', 'StopStatus'})
            if not {item.lower().replace('-', '') for item in impacts} & {'notserved', 'cancelled', 'notstopping', 'stopclosed'}:
                continue
            if not route:
                continue
            if any(choices and route.get(key) not in choices for choices, key in (
                (values(tree, {'LineRef'}), 'line_id'), (values(tree, {'RouteRef'}), 'route_id'),
                (values(tree, {'JourneyPatternRef'}), 'pattern_id'), (values(tree, JOURNEY_REFS), 'journey_id'),
            )):
                continue
            directions = values(tree, {'DirectionRef', 'DirectionName', 'Direction'})
            if not matches_direction(directions, route):
                continue
            exact = values(tree, STOP_REFS)
            affected.update(exact)
            cancelled.update(exact)

        if sections or values(branch, START_REFS | END_REFS):
            for section in sections or [{'children': branch}]:
                nodes = section['children']
                first = endpoint_refs(nodes, START_REFS, {'FirstStop', 'FromStop', 'StartStop'})
                last = endpoint_refs(nodes, END_REFS, {'LastStop', 'ToStop', 'EndStop'})
                if len(first) != 1 or len(last) != 1:
                    continue
                start, end = next(iter(first)), next(iter(last))
                via = [node['value'] for node in walk(nodes) if node['kind'] in {'ViaStopPointRef', 'ViaQuayRef'} and node['value']]
                result = scope_on_route({'kind': 'section', 'start': {'ref': start, 'name': label(start)},
                                         'end': {'ref': end, 'name': label(end)}, 'via': [{'ref': ref} for ref in via],
                                         'cancelled': [{'ref': ref} for ref in cancelled]},
                                        route, variants, route_refs, pattern_refs, journey_refs)
                if result:
                    yield result
            continue
        affected.update(values(branch, STOP_REFS))
        if affected:
            result = scope_on_route({'kind': 'stops', 'stops': [{'ref': ref} for ref in affected],
                                     'cancelled': [{'ref': ref} for ref in cancelled]}, route, variants)
            if result:
                yield result
        elif area and not qualifiers:
            yield {'scope': 'area', 'area': area, 'positions': [], 'cancelled': []}
        elif qualifiers or values(branch, {'All', 'AllLines'}) & {'true'}:
            yield {'scope': 'line' if qualifiers else 'network', 'positions': [], 'cancelled': []}


def notice_stop_options(conn, day, query, mode, line):
    # Search one dated publication, or the nearest one when planning ahead.
    # The labels are display text. Identity always comes from the structured ID.
    ref = "call->>'quay_id'" if mode == 'platform' else "call->>'stop_place_id'"
    return conn.execute(
        f"""WITH chosen AS (
            SELECT service_date FROM public_route_days
            WHERE (%s::text IS NULL OR line_code=%s) AND service_date BETWEEN %s::date - 14 AND %s::date + 14
            GROUP BY service_date ORDER BY ABS(service_date - %s::date),service_date DESC LIMIT 1
        ), candidates AS (
            SELECT {ref} AS ref, call->>'name' AS name
            FROM public_route_days d JOIN chosen USING (service_date)
            CROSS JOIN LATERAL jsonb_each(d.journeys) AS journey
            CROSS JOIN LATERAL jsonb_array_elements(value->'calls') AS call
            WHERE (%s::text IS NULL OR d.line_code=%s) AND strpos(lower(call->>'name'),lower(%s)) > 0
        )
        SELECT ref, min(name) AS name FROM candidates WHERE ref IS NOT NULL GROUP BY ref ORDER BY name,ref LIMIT 35
        """, (line, line, day, day, day, line, line, query),
    ).fetchall()
