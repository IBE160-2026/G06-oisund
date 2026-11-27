"""Private route inspection, immutable decision receipts and confirmation handoff."""

from datetime import datetime
from typing import Annotated, Literal
import unicodedata
from uuid import UUID, uuid4

from fastapi import HTTPException
from psycopg.types.json import Jsonb
from pydantic import Field, model_validator

from . import route_catalogue, auth, draft_storage, import_route_matching, position_coordinates, route_source
from .draft_domain import DraftContent, StrictModel
from .private_storage import database

MAX_DECISIONS = 2000
MAX_RANGES = 20
ROUTE_CHANGED = 'Rutevalget er endret. Last inn og gjennomgå den lagrede versjonen.'
Position = Annotated[int, Field(ge=1, le=120, strict=True)]
JourneyID = Annotated[str, Field(pattern=r'^TRO:ServiceJourney:[A-Za-z0-9_./-]{1,200}$')]
Digest = Annotated[str, Field(pattern=r'^[a-f0-9]{64}$')]


class FieldChoice(StrictModel):
    mode: Literal['keep', 'source', 'manual', 'unknown']
    manual: str | None = Field(default=None, min_length=1, max_length=300)

    @model_validator(mode='after')
    def explicit_value(self):
        if self.mode == 'manual':
            if not self.manual or not self.manual.strip():
                raise ValueError('Enter a manual value')
        elif self.manual is not None:
            raise ValueError('Unexpected manual value')
        return self


class FieldDecisions(StrictModel):
    direction: FieldChoice
    destination: FieldChoice
    stops: FieldChoice


class SelectedRoute(StrictModel):
    line_code: str | None = Field(default=None, pattern=r'^(?:X?[0-9]{2}|26B)$')
    journey_id: JourneyID
    source_sha256: Digest
    start_position: Position
    end_position: Position
    field_decisions: FieldDecisions

    @model_validator(mode='after')
    def forward_range(self):
        if self.start_position >= self.end_position:
            raise ValueError('Select an ordered range with two different occurrences')
        return self


class SaveRoute(StrictModel):
    operation_id: UUID
    expected_draft_revision: int = Field(ge=1, strict=True)
    expected_route_revision: int = Field(ge=0, strict=True)
    activity_id: UUID
    selection: SelectedRoute | None


def route_revision(conn, draft_id):
    return conn.execute('SELECT COALESCE(max(revision),0) AS revision FROM draft_route_decisions WHERE draft_id=%s',
                        (draft_id,)).fetchone()['revision']


def saved_decisions(conn, draft_id):
    return conn.execute(
        'SELECT DISTINCT ON (activity_id) revision,draft_revision,activity_id,reference '
        'FROM draft_route_decisions WHERE draft_id=%s ORDER BY activity_id,revision DESC',
        (draft_id,),
    ).fetchall()


def current_references(conn, draft):
    return [row['reference'] for row in saved_decisions(conn, draft['id'])
            if row['draft_revision'] == draft['revision'] and row['reference'] is not None]


def resolve_imported(conn, draft, previous=None):
    content = DraftContent.model_validate(draft['content'])
    if content.import_metadata is None or draft['confirmed']:
        return
    saved = {row['activity_id']: row for row in saved_decisions(conn, draft['id'])}
    previous_activities = (
        {activity.id: activity for activity in DraftContent.model_validate(previous['content']).activities}
        if previous is not None else {}
    )
    now, days = now_for(conn), {}
    revision = route_revision(conn, draft['id'])
    for activity in import_route_matching.imported_trips(content):
        existing = saved.get(activity.id)
        old_reference = existing['reference'] if existing else None
        if existing and (not old_reference or old_reference.get('selection_mode') != 'automatic'
                         or existing['draft_revision'] == draft['revision']):
            continue
        previous_activity = previous_activities.get(activity.id)
        if (old_reference and previous_activity and previous['content']['service_date'] == draft['content']['service_date']
                and all(getattr(previous_activity, field) == getattr(activity, field) for field in
                        ('line', 'trip', 'start', 'end', 'from_place', 'to_place', 'direction'))):
            reference = {**old_reference, 'decision_revision': revision + 1}
        else:
            _, match = import_route_matching.activity_match(conn, content, activity, now, days)
            if not match:
                continue
            day, journey, first, last = match
            reference = {
                **journey, 'activity_id': str(activity.id), 'decision_revision': revision + 1,
                'start_position': first, 'end_position': last,
                'field_decisions': {'direction': {'mode': 'source', 'manual': None},
                                    'destination': {'mode': 'source', 'manual': None},
                                    'stops': {'mode': 'source', 'manual': None}},
                'provenance': day['provenance'], 'source_state': day['source_state'],
                'status': 'compatible', 'selection_mode': 'automatic', 'selected_at': now.isoformat(),
                'position_coordinate_revision': day['provenance'].get('nsr_revision'),
            }
        if revision >= MAX_DECISIONS:
            break
        revision += 1
        conn.execute(
            'INSERT INTO draft_route_decisions(draft_id,revision,draft_revision,activity_id,operation_id,payload_hash,reference) '
            'VALUES(%s,%s,%s,%s,%s,%s,%s)',
            (draft['id'], revision, draft['revision'], activity.id, uuid4(),
             draft_storage.fingerprint(draft['id'], reference), Jsonb(reference)),
        )


def effective_content(content, references):
    directions = {}
    for reference in references:
        if reference['status'] == 'incompatible':
            continue
        choice = reference['field_decisions']['direction']
        if choice['mode'] == 'manual':
            directions[reference['activity_id']] = choice['manual'][:100]
        elif choice['mode'] == 'source':
            directions[reference['activity_id']] = import_route_matching.direction_label(reference, reference['start_position'])[0]
    if not directions:
        return content
    return content.model_copy(update={'activities': [
        activity.model_copy(update={'direction': directions[str(activity.id)]})
        if not (activity.direction or '').strip() and str(activity.id) in directions else activity
        for activity in content.activities
    ]})


def freeze(conn, workday_id, references):
    for reference in references:
        conn.execute('INSERT INTO workday_route_references(workday_id,activity_id,reference) VALUES (%s,%s,%s)',
                     (workday_id, UUID(reference['activity_id']), Jsonb(reference)))


def require_current(source, expected_revision, mutable=False):
    if source['revision'] != expected_revision:
        raise HTTPException(409, 'Utkastet er endret. Last inn den lagrede versjonen.')
    if mutable and source['confirmed']:
        raise HTTPException(409, 'Utkastet har en bekreftet plan. Åpne lagret rutereferanse i planen.')


def activity_facts(draft, activity_id):
    content = DraftContent.model_validate(draft['content'])
    activity = next((item for item in content.activities if item.id == activity_id), None)
    if activity is None:
        draft_storage.deny()
    if activity.type != 'trip':
        raise HTTPException(422, 'Ruteoppslag er tilgjengelig for lagrede passasjerturer.')
    return content, activity


def label(value):
    return ' '.join(unicodedata.normalize('NFC', value or '').casefold().split())


def utc_of(value):
    return datetime.fromisoformat(value['utc']) if value and value['utc'] else None


def exact_ranges(journey, activity):
    start = datetime.fromisoformat(activity.start)
    end = datetime.fromisoformat(activity.end)
    first = [call['position'] for call in journey['calls'] if call['boarding']
             and label(call['name']) == label(activity.from_place) and utc_of(call['departure']) == start]
    last = [call['position'] for call in journey['calls'] if call['alighting']
            and label(call['name']) == label(activity.to_place) and utc_of(call['arrival'] or call['departure']) == end]
    return [[begin, finish] for begin in first for finish in last if begin < finish]


def comparable(activity, code):
    return (route_catalogue.code_for(activity.line) == code and activity.start and activity.end
            and label(activity.from_place) and label(activity.to_place))


def selection_status(journey, selection, activity, day):
    first = journey['calls'][selection.start_position - 1]
    last = journey['calls'][selection.end_position - 1]
    from_time = utc_of(first['departure'])
    to_time = utc_of(last['arrival'] or last['departure'])
    if ((activity.start and from_time and datetime.fromisoformat(activity.start) != from_time)
            or (activity.end and to_time and datetime.fromisoformat(activity.end) != to_time)
            or not first['boarding'] or not last['alighting']):
        return 'incompatible'
    if (day['coverage'] == 'complete' and day['source_state'] == 'available' and comparable(activity, route_catalogue.code_for(journey['line_id']))
            and [selection.start_position, selection.end_position] in exact_ranges(journey, activity)):
        return 'compatible'
    return 'unverified'


def source_comparison(reference, day):
    if day['source_state'] in {'unavailable', 'outside_scope'}:
        return 'unavailable'
    journey = day['journeys'].get(reference['journey_id'])
    if journey is None:
        return 'missing' if day['coverage'] == 'complete' else 'unavailable'
    if any(reference.get(key) != journey[key] for key in (
        'calendar', 'journey_version', 'pattern_version', 'pattern_id', 'direction', 'headsign', 'calls',
    )):
        return 'changed'
    if day['source_state'] == 'stale':
        return 'stale'
    current_digest = day['provenance'].get('sha256')
    same_version = current_digest and current_digest == reference['provenance'].get('sha256')
    return 'same_version' if same_version or reference['provenance'] == day['provenance'] else 'same_facts'


def state(conn, draft, now):
    data = saved_decisions(conn, draft['id'])
    activity_ids = {str(activity.id) for activity in DraftContent.model_validate(draft['content']).activities}
    result = {'draft_id': draft['id'], 'draft_revision': draft['revision'],
              'route_revision': route_revision(conn, draft['id']), 'references': [], 'outdated': []}
    for row in data:
        reference = row['reference']
        if reference is None or reference['activity_id'] not in activity_ids:
            continue
        key = 'references' if row['draft_revision'] == draft['revision'] else 'outdated'
        origin = datetime.fromisoformat(reference['service_date']).date()
        status = source_comparison(reference, route_catalogue.lookup(conn, origin, now, route_catalogue.code_for(reference['line_id'])))
        result[key].append({**reference, 'comparison': status})
    content = DraftContent.model_validate(draft['content'])
    decided = {UUID(reference['activity_id']) for reference in result['references']}
    decided.update(row['activity_id'] for row in data
                   if not row['reference'] or row['reference'].get('selection_mode') != 'automatic')
    result['import_matches'] = import_route_matching.summaries(conn, content, now, decided)
    return result


def now_for(conn):
    return conn.execute('SELECT clock_timestamp() AS now').fetchone()['now']


def read_draft(request, identifier, revision):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        draft = draft_storage.owned(conn, owner, identifier, request)
        require_current(draft, revision, mutable=True)
        result = state(conn, draft, now_for(conn))
        draft_storage.owned(conn, owner, identifier, request)
        return result


def resolve_draft(request, identifier, revision):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        draft = draft_storage.owned(conn, owner, identifier, request)
        require_current(draft, revision, mutable=True)
        resolve_imported(conn, draft)
        result = state(conn, draft, now_for(conn))
        draft_storage.owned(conn, owner, identifier, request)
        return result


def departure_summary(item, ranges=()):
    first, last = item['calls'][0], item['calls'][-1]
    return {key: item[key] for key in ('journey_id', 'pattern_id', 'direction', 'headsign')} | {
        'start': first['departure'], 'end': last['arrival'],
        'from_name': first['name'], 'to_name': last['name'],
        'matching_ranges': list(ranges[:MAX_RANGES]), 'ranges_truncated': len(ranges) > MAX_RANGES,
    }


def departure_order(item):
    return (not bool(item['matching_ranges']), item['start']['day_offset'],
            item['start']['utc'] or item['start']['raw_time'], item['journey_id'])


def browse(request, service_date, code, journey_id, source_sha256):
    with database() as conn:
        draft_storage.authorized(conn, request)
        day = route_catalogue.lookup(conn, service_date, now_for(conn), code)
        result = {key: day[key] for key in ('coverage', 'source_state', 'reasons', 'provenance')}
        result.update(service_date=service_date, line_code=code)
        if journey_id is None:
            result['journeys'] = sorted(map(departure_summary, day['journeys'].values()), key=departure_order)
        else:
            journey = day['journeys'].get(journey_id)
            if not journey or not day['provenance'] or day['provenance']['sha256'] != source_sha256:
                raise HTTPException(409, 'Avgangen eller rutekilden er endret. Søk på nytt.')
            result['journey'] = journey
        draft_storage.authorized(conn, request)
        return result


def activity_line(activity, service_date):
    return '20' if service_date in route_source.DATES else route_catalogue.code_for(activity.line)


def public_snapshot(request, identifier, revision, activity_id, journey_id=None, line_code=None):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        draft = draft_storage.owned(conn, owner, identifier, request)
        require_current(draft, revision, mutable=True)
        content, activity = activity_facts(draft, activity_id)
        code = line_code or activity_line(activity, content.service_date)
        day = route_catalogue.lookup(conn, content.service_date, now_for(conn), code)
        result = {key: day[key] for key in ('coverage', 'source_state', 'reasons', 'provenance')}
        result.update(draft_id=identifier, draft_revision=revision, activity_id=activity_id,
                      service_date=content.service_date, line_id=route_catalogue.LINE_IDS.get(code), line_code=code,
                      expected_count=(route_source.EXPECTED.get(content.service_date)
                                      if code == '20' and day['provenance'] and day['provenance'].get('parser_revision') == 1 else None))
        if journey_id is not None:
            item = day['journeys'].get(journey_id)
            if item is None:
                raise HTTPException(409, 'Avgangen finnes ikke i denne daterte kilden.')
            result['journey'] = item
        else:
            compare = comparable(activity, code)
            items = []
            range_count = 0
            for item in day['journeys'].values():
                ranges = exact_ranges(item, activity) if compare else []
                range_count += len(ranges)
                items.append(departure_summary(item, ranges))
            checked = compare and day['source_state'] == 'available' and day['coverage'] == 'complete' and bool(day['journeys'])
            # A checked result is bounded to literal names and planned-clock equality.
            # It never establishes a trip-number identity or automatic association.
            result['outcome'] = ('alternatives' if range_count > 1 else 'possible' if range_count else 'not_found') if checked else 'insufficient'
            result['journeys'] = sorted(items, key=departure_order)
        draft_storage.owned(conn, owner, identifier, request)
        return result


def receipt(conn, draft_id, operation_id):
    return conn.execute(
        'SELECT operation_id,revision,draft_revision,activity_id,payload_hash,reference FROM draft_route_decisions '
        'WHERE draft_id=%s AND operation_id=%s',
        (draft_id, operation_id),
    ).fetchone()


def receipt_value(conn, draft_id, row):
    return {'operation_id': row['operation_id'], 'draft_id': draft_id,
            'draft_revision': row['draft_revision'], 'route_revision': row['revision'],
            'activity_id': row['activity_id'], 'reference': row['reference'],
            'current_route_revision': route_revision(conn, draft_id)}


def lookup(request, identifier, operation_id):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        draft_storage.owned(conn, owner, identifier, request)
        row = receipt(conn, identifier, operation_id)
        result = {'state': 'accepted' if row else 'pending',
                  'result': receipt_value(conn, identifier, row) if row else None}
        draft_storage.owned(conn, owner, identifier, request)
        return result


def save(request, identifier, body):
    payload = body.model_dump(mode='json')
    if body.selection is not None and body.selection.line_code is None:
        # Pre-catalogue receipts hashed the same selection without this field.
        del payload['selection']['line_code']
    digest = draft_storage.fingerprint(identifier, payload)
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        draft = draft_storage.owned(conn, owner, identifier, request)
        existing = receipt(conn, identifier, body.operation_id)
        if existing:
            if existing['payload_hash'] != digest:
                raise HTTPException(409, 'Dette rutevalget ble allerede lagret med andre opplysninger.')
            draft_storage.owned(conn, owner, identifier, request)
            return receipt_value(conn, identifier, existing)
        require_current(draft, body.expected_draft_revision, mutable=True)
        revision = route_revision(conn, identifier)
        if revision != body.expected_route_revision:
            raise HTTPException(409, ROUTE_CHANGED)
        if revision >= MAX_DECISIONS:
            raise HTTPException(429, 'Grensen for ruteendringer i dette utkastet er nådd.')

        selection = body.selection
        reference = None
        if selection is not None:
            content, activity = activity_facts(draft, body.activity_id)
            observed = now_for(conn)
            code = selection.line_code or activity_line(activity, content.service_date)
            day = route_catalogue.lookup(conn, content.service_date, observed, code)
            if not day['provenance'] or day['provenance']['sha256'] != selection.source_sha256:
                raise HTTPException(409, 'Rutens kildegrunnlag er endret eller utilgjengelig. Søk på nytt.')
            journey = day['journeys'].get(selection.journey_id)
            if not journey or selection.end_position > len(journey['calls']):
                raise HTTPException(422, 'Velg start og slutt blant avgangens faktiske stoppforekomster.')
            reference = {
                **journey, 'activity_id': str(activity.id), 'decision_revision': revision + 1,
                'start_position': selection.start_position, 'end_position': selection.end_position,
                'field_decisions': selection.field_decisions.model_dump(mode='json'),
                'provenance': day['provenance'], 'source_state': day['source_state'],
                'status': selection_status(journey, selection, activity, day),
                'selection_mode': 'explicit', 'selected_at': observed.isoformat(),
            }
            if day['provenance'].get('nsr_revision'):
                reference['position_coordinate_revision'] = day['provenance']['nsr_revision']
            elif position_coordinates.is_rechecked_timetable(reference):
                manual = position_coordinates.PILOT_MANUAL_REVISION
                reference['position_coordinate_revision'] = manual if position_coordinates.sidecar(manual) else None
            elif position_coordinates.is_pilot_timetable(reference):
                reference['position_coordinate_revision'] = position_coordinates.current_pilot_revision()
        elif not any(row['activity_id'] == body.activity_id and row['reference'] is not None
                     for row in saved_decisions(conn, identifier)):
            raise HTTPException(422, 'Det finnes ikke et rutevalg å fjerne for denne aktiviteten.')

        row = conn.execute(
            'INSERT INTO draft_route_decisions(draft_id,revision,draft_revision,activity_id,operation_id,payload_hash,reference) '
            'SELECT id,%s,revision,%s,%s,%s,%s FROM drafts WHERE id=%s AND revision=%s AND NOT confirmed '
            'AND expires_at > clock_timestamp() ON CONFLICT (operation_id) DO NOTHING '
            'RETURNING operation_id,revision,draft_revision,activity_id,reference',
            (revision + 1, body.activity_id, body.operation_id, digest, Jsonb(reference) if reference else None,
             identifier, body.expected_draft_revision),
        ).fetchone()
        draft_storage.owned(conn, owner, identifier, request)
        if not row:
            draft_storage.deny()
        return receipt_value(conn, identifier, row)
