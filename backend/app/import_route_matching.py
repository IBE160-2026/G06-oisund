"""Match a PDF activity to an exact range of a dated Entur departure."""

from datetime import date, timedelta
import re
import unicodedata

from . import route_catalogue
from .position_coordinates import instant


# Stop-name variants in the operator and public timetable. Time and turn number
# are still required, and repeated occurrences must resolve to one range.
ALIASES = {
    'tromso lufthavn': 'flyplassen',
    'tromso lufthavn langnes': 'flyplassen',
    'langnes lufthavn': 'flyplassen',
    'tromso lufthavn flyplassen': 'flyplassen',
    'universitetssykehuset nord norge': 'unn',
    'universitetssykehuset': 'unn',
}


def stop_name(value):
    value = unicodedata.normalize('NFKD', (value or '').casefold().replace('ø', 'o').replace('æ', 'ae'))
    tokens = re.findall(r'[a-z0-9]+', ''.join(char for char in value if not unicodedata.combining(char)))
    value = ' '.join(tokens)
    return ALIASES.get(value, value)


def trip_code(value):
    value = (value or '').strip().casefold()
    return (value.lstrip('0') or '0') if re.fullmatch(r'[0-9]+', value) else value


def matching_positions(calls, expected, clock):
    return [call['position'] for call in calls if stop_name(call['name']) == expected and any(
        instant(value['utc']) == clock for value in (call['arrival'], call['departure']) if value and value['utc']
    )]


def activity_match(conn, content, activity, now, days):
    line = route_catalogue.code_for(activity.line)
    start, end = instant(activity.start), instant(activity.end)
    origin, destination = stop_name(activity.from_place), stop_name(activity.to_place)
    code = trip_code(activity.trip)
    if not all((content.service_date, line, start, end, origin, destination, code)):
        return 'missing-facts', None
    if line not in route_catalogue.LINE_IDS:
        return 'catalogue-missing', None

    local_start = date.fromisoformat(activity.start[:10])
    if not 0 <= (local_start - content.service_date).days <= 1:
        return 'conflicting-facts', None
    dates = [content.service_date]
    if local_start != content.service_date:
        dates.append(local_start)
    elif local_start > date.min and activity.start[11:13] < '06':
        dates.append(local_start - timedelta(days=1))
    matches, have_catalogue, found_code = [], False, False
    for service_day in dates:
        key = service_day, line
        if key not in days:
            days[key] = route_catalogue.lookup(conn, service_day, now, line)
        day = days[key]
        if day['coverage'] != 'complete' or day['source_state'] != 'available':
            continue
        have_catalogue = True
        for journey in day['journeys'].values():
            if trip_code(journey.get('private_code')) != code:
                continue
            found_code = True
            calls = journey['calls']
            first = matching_positions(calls, origin, start)
            last = matching_positions(calls, destination, end)
            matches.extend((day, journey, a, b) for a in first for b in last if a < b)
    if len(matches) == 1:
        day, journey, first, last = matches[0]
        manual_direction = stop_name(activity.direction)
        if manual_direction in {'utgaende', 'inngaende', 'outbound', 'inbound'} and manual_direction not in (
            ('utgaende', 'outbound') if journey['direction'] == 'outbound' else ('inngaende', 'inbound')
        ):
            return 'conflicting-facts', None
        return 'matched', (day, journey, first, last)
    if len(matches) > 1:
        return 'ambiguous', None
    if not have_catalogue:
        return 'catalogue-missing', None
    return ('conflicting-facts' if found_code else 'trip-not-found'), None


def imported_trips(content):
    if content.import_metadata is None:
        return ()
    source_ids = {source.activity_id for source in content.import_metadata.activities}
    return (activity for activity in content.activities if activity.id in source_ids and activity.type == 'trip')


def direction_label(journey, first):
    direction = {'outbound': 'Utgående', 'inbound': 'Inngående'}[journey['direction']]
    return direction, journey['calls'][first - 1]['headsign'] or journey['headsign']


def summary(activity_id, outcome, match):
    result = {'activity_id': str(activity_id), 'outcome': outcome}
    if match:
        _, journey, first, last = match
        direction, destination = direction_label(journey, first)
        result.update(direction=direction, destination=destination, journey_id=journey['journey_id'],
                      start_position=first, end_position=last)
    return result


def summaries(conn, content, now, existing=()):
    days = {}
    return [summary(activity.id, *activity_match(conn, content, activity, now, days))
            for activity in imported_trips(content) if activity.id not in existing]
