"""Explain possible relevance using the qualified line/date crosswalk only."""

from datetime import date, datetime, time, timedelta, UTC
from zoneinfo import ZoneInfo

from .automatic_notice_source import instant


OSLO = ZoneInfo('Europe/Oslo')
QUALIFIED_DATES = tuple(date(2026, 11, day) for day in range(23, 30))
CROSSWALK = {
    '20': ('TRO:Line:1_20', 'TRO:Authority:1'),
    '24': ('TRO:Line:1_24', 'TRO:Authority:1'),
}
BINDING = {'version': 'entur-tro-2026-11-20-pilot-week', 'basis': 'Checked Entur NeTEx line, group and authority records',
           'archive_generation': '1795129398375617',
           'archive_sha256': '03662d51c1438514d1695e632c598a7ea589d5384a19804658212fc4af0af8b9',
           'dates': [value.isoformat() for value in QUALIFIED_DATES]}
REVIEW_QUALIFIERS = {'DirectionRef', 'AffectedDirection', 'AffectedRoute', 'AffectedStopPoint', 'AffectedStopPlace',
                     'StopPointRef', 'StopPlaceRef', 'QuayRef', 'AffectedVehicleJourney', 'VehicleJourneyRef',
                     'FramedVehicleJourneyRef', 'DatedVehicleJourneyRef', 'AffectedOnly', 'AffectedSection'}


def walk(nodes, ancestors=()):
    for node in nodes:
        yield node, ancestors
        yield from walk(node['children'], (*ancestors, node['kind']))


def valid_windows(source):
    windows = []
    uncertain = not source['windows']
    for window in source['windows']:
        start, end = instant(window['start']), instant(window['end'])
        if start is None or (window['end'] is not None and (end is None or end <= start)):
            uncertain = True
        else:
            windows.append((start, end))
    return windows, uncertain


def planned_interval(value):
    start, end = instant(value['start']), instant(value['end'])
    try:
        start = start if start and start.astimezone(OSLO).utcoffset() == datetime.fromisoformat(value['start']).utcoffset() else None
        end = end if end and end.astimezone(OSLO).utcoffset() == datetime.fromisoformat(value['end']).utcoffset() else None
    except (ValueError, OverflowError):
        return None
    if start is None or end is None or end < start:
        return None
    return start, end


def within_date(interval, day):
    start, end = interval
    lower = datetime.combine(day, time(), OSLO).astimezone(UTC)
    upper = datetime.combine(day + timedelta(days=1), time(), OSLO).astimezone(UTC)
    if start == end:
        return (start, end) if lower <= start < upper else ()
    return (max(lower, start), min(upper, end)) if start < upper and lower < end else ()


def overlaps(activity, window):
    start, end = activity
    begins, finishes = window
    if start == end:
        return begins <= start and (finishes is None or start < finishes)
    return begins < end and (finishes is None or start < finishes)


def classify(source, activities, now):
    reasons, matches = [], []
    windows, uncertain = valid_windows(source)
    expired = bool(windows) and not uncertain and all(end is not None and end <= now for _, end in windows)
    fields = list(walk(source['affects']))
    lines = {node['value'] for node, parents in fields if node['kind'] == 'LineRef' and node['value']
             and parents and parents[-1] == 'AffectedLine' and 'AffectedVehicleJourney' not in parents}
    authorities = {node['value'] for node, _ in fields if node['kind'] == 'AuthorityRef' and node['value']}
    operators = {node['value'] for node, _ in fields if node['kind'] == 'OperatorRef' and node['value']}
    modes = {node['value'] for node, _ in fields if node['kind'] in {'VehicleMode', 'TransportMode'} and node['value']}
    qualifiers = {node['kind'] for node, _ in fields if node['kind'] in REVIEW_QUALIFIERS or node['kind'].startswith('{')}
    confirmed_authority = not operators and not (authorities - {'TRO:Authority:1'})
    if uncertain:
        reasons.append('uncertain-validity')
    if any(end is None for _, end in windows):
        reasons.append('open-ended-validity')
    if qualifiers:
        reasons.append('unresolved-qualifiers')
    if source['progress'] not in {'open', 'closed'}:
        reasons.append('source-status-unknown')

    def result(kind):
        return {'classification': kind, 'reasons': reasons, 'matches': matches, 'validity_expired': expired}

    if source['progress'] == 'closed':
        reasons.append('source-closed')
    if expired:
        reasons.append('validity-expired')
    if source['progress'] == 'closed' or expired:
        return result('outside-scope')
    if modes and modes <= {'ferry', 'water', 'rail', 'tram', 'metro', 'air'}:
        reasons.append('other-mode')
        return result('outside-scope')
    if not lines:
        if any(node['kind'] in {'StopPointRef', 'StopPlaceRef', 'QuayRef'} and node['value'] for node, _ in fields):
            reasons.append('stop-scope-unverified')
            return result('review')
        networks = {node['value'] for node, _ in fields if node['kind'] == 'NetworkRef' and node['value']}
        if confirmed_authority and not qualifiers and not (networks - {'TRO:Network:1'}) and any(
            node['kind'] in {'AllLines', 'All'} and node['value'] == 'true' and
            ('AffectedNetwork' in parents or not parents) for node, parents in fields
        ):
            reasons.append('explicit-broad-scope')
            return result('broad-context')
        reasons.append('scope-unresolved')
        return result('review')
    if not confirmed_authority:
        reasons.append('authority-unverified')
        return result('review')
    mapped = {number: info for number, info in CROSSWALK.items() if info[0] in lines}
    if not mapped:
        reasons.append('line-binding-unavailable')
        return result('review')
    eligible = [activity for activity in activities if activity['line'] in mapped]
    if not eligible:
        reasons.append('no-matching-printed-line')
        return result('review')
    reliable_comparison = False
    for activity in eligible:
        interval = planned_interval(activity)
        if interval is None:
            if 'uncertain-planned-time' not in reasons:
                reasons.append('uncertain-planned-time')
            continue
        start, end = interval
        # For duration activities an endpoint at midnight belongs to the next
        # day but contributes no time there. Point activities use their instant.
        last = end - timedelta(microseconds=1) if end > start else end
        if any(value.astimezone(OSLO).date() not in QUALIFIED_DATES for value in (start, last)):
            if 'no-dated-binding' not in reasons:
                reasons.append('no-dated-binding')
        periods = [(day, within_date(interval, day)) for day in QUALIFIED_DATES]
        dates = [day.isoformat() for day, period in periods if period and any(overlaps(period, window) for window in windows)]
        if any(period for _, period in periods):
            reliable_comparison = True
        if dates:
            line_ref, authority = mapped[activity['line']]
            matches.append({'id': activity['id'], 'line': activity['line'], 'line_ref': line_ref,
                            'authority_ref': authority, 'dates': dates})
    if matches:
        reasons.insert(0, 'exact-line-planned-overlap')
        return result('possible-relevance')
    if reliable_comparison and not uncertain and not {'uncertain-planned-time', 'no-dated-binding'} & set(reasons):
        reasons.append('no-planned-overlap')
        return result('outside-scope')
    return result('review')
