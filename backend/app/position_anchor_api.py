"""Owner-scoped last stop and frozen coordinate projection."""
from datetime import timedelta
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic import Field, field_validator
from psycopg.types.json import Jsonb

from . import draft_storage, position_coordinates, quay_catalogue, workday_lifecycle_storage, workday_storage
from .draft_domain import StrictModel
from .private_storage import database


router = APIRouter(prefix='/workdays/{identifier}')
MAX_RECEIPTS = 256
MIN_GPS_SAVE_GAP = timedelta(seconds=6)
STALE_ANCHOR = 'Lagret holdepunkt er endret. Hent lagret status.'


class SaveAnchor(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=0, le=MAX_RECEIPTS, strict=True)
    activity_id: UUID
    route_basis: str = Field(pattern=r'^[a-f0-9]{64}$')
    occurrence_id: str = Field(min_length=1, max_length=200)
    coordinate_revision: str | None = Field(max_length=100)
    origin: Literal['manual', 'gps']
    evidence_at: str = Field(min_length=20, max_length=48)
    carried_from_revision: int | None = Field(default=None, gt=0, le=MAX_RECEIPTS, strict=True)

    @field_validator('evidence_at')
    @classmethod
    def dated(cls, value):
        if position_coordinates.instant(value) is None:
            raise ValueError('An explicit evidence timestamp is required')
        return value


def access(conn, identifier, request):
    owner = draft_storage.authorized(conn, request)
    return owner, workday_storage.owned(conn, owner, identifier, request)


def coordinate_view(conn, identifier, activity_id):
    row = conn.execute('SELECT reference FROM workday_route_references WHERE workday_id=%s AND activity_id=%s',
                       (identifier, activity_id)).fetchone()
    reference = row['reference'] if row else None
    catalogue = quay_catalogue.load_for_reference(conn, reference) if reference else None
    return position_coordinates.view(reference, activity_id, catalogue)


@router.get('/position-coordinates/{activity_id}')
def coordinates(identifier: UUID, activity_id: UUID, request: Request):
    with database() as conn:
        owner, plan = access(conn, identifier, request)
        if str(activity_id) not in {item['id'] for item in plan['content']['activities']}:
            draft_storage.deny()
        result = coordinate_view(conn, identifier, activity_id)
        state = workday_lifecycle_storage.current(conn, plan)['state']
        workday_storage.owned(conn, owner, identifier, request)
        return {'workday_id': identifier, 'activity_id': activity_id, 'expires_at': plan['expires_at'],
                'terminal': state in ('ended', 'aborted'), **result}


def latest(conn, identifier):
    return conn.execute('SELECT * FROM workday_position_anchors WHERE workday_id=%s', (identifier,)).fetchone()


@router.get('/position-anchor')
def read(identifier: UUID, request: Request):
    with database() as conn:
        owner, plan = access(conn, identifier, request)
        anchor = latest(conn, identifier)
        state = workday_lifecycle_storage.current(conn, plan)['state']
        workday_storage.owned(conn, owner, identifier, request)
        return {'workday_id': identifier, 'expires_at': plan['expires_at'], 'revision': anchor['revision'] if anchor else 0,
                'terminal': state in ('ended', 'aborted'), 'anchor': anchor}


def operation(conn, operation_id):
    return conn.execute('SELECT o.*,w.owner FROM workday_position_anchor_operations o '
                        'JOIN workdays w ON w.id=o.workday_id WHERE o.id=%s', (operation_id,)).fetchone()


def accepted(row):
    return {'operation_id': row['id'], 'workday_id': row['workday_id'],
            'accepted_revision': row['anchor_revision'], 'accepted_at': row['accepted_at']}


@router.get('/position-anchor/operations/{operation_id}')
def lookup(identifier: UUID, operation_id: UUID, request: Request):
    with database() as conn:
        owner, _ = access(conn, identifier, request)
        prior = operation(conn, operation_id)
        if not prior or prior['owner'] != owner or prior['workday_id'] != identifier:
            draft_storage.deny()
        workday_storage.owned(conn, owner, identifier, request)
        return accepted(prior)


def remap(previous, route_view):
    return [call for call in route_view['calls'] if previous['quay_id'] == call['quay_id']]


@router.post('/position-anchor')
def save(identifier: UUID, body: SaveAnchor, request: Request):
    digest = draft_storage.fingerprint(identifier, body.model_dump(mode='json'))
    with database() as conn:
        owner, plan = access(conn, identifier, request)
        prior = operation(conn, body.operation_id)
        if prior:
            if prior['owner'] != owner:
                draft_storage.deny()
            if prior['workday_id'] != identifier or prior['payload_hash'] != digest:
                raise HTTPException(409, 'Lagringsforsøket har annet innhold.')
            workday_storage.owned(conn, owner, identifier, request)
            return accepted(prior)
        workday_storage.require_mutable(conn, plan)
        previous = latest(conn, identifier)
        if body.expected_revision != (previous['revision'] if previous else 0):
            raise HTTPException(409, STALE_ANCHOR)
        route_view = coordinate_view(conn, identifier, body.activity_id)
        route = route_view['route']
        call = next((value for value in route_view['calls'] if value['occurrence_id'] == body.occurrence_id), None)
        if not route or not route['compatible'] or route['basis'] != body.route_basis or not call:
            raise HTTPException(422, 'Velg en forekomst i den bekreftede kjøringen.')
        point = call['coordinates']
        quay, parent = call['quay_id'], call['stop_place_id']
        if (not position_coordinates.public_id(quay, 'quay') or not position_coordinates.public_id(parent, 'stop_place')
                or body.coordinate_revision != (point['revision'] if point else None)
                or (body.origin == 'gps' and not point)):
            raise HTTPException(422, 'Holdeplassen har ingen bekreftet plattformkobling for dette lagringsforsøket.')
        # Selection is read-only here. A stale tab cannot save on an activity
        # that another tab has already replaced.
        selection = conn.execute('SELECT activity_id FROM workday_selections WHERE workday_id=%s',
                                 (identifier,)).fetchone()
        if not selection or selection['activity_id'] != body.activity_id:
            raise HTTPException(409, 'Valgt aktivitet er endret. Åpne den valgte aktiviteten igjen.')
        now = conn.execute('SELECT clock_timestamp() AS now').fetchone()['now']
        evidence = position_coordinates.instant(body.evidence_at)
        if not plan['confirmed_at'] - timedelta(seconds=5) <= evidence <= now + timedelta(seconds=5):
            raise HTTPException(422, 'Tidspunktet for holdepunktet kunne ikke bekreftes.')
        if previous and evidence < (previous['asserted_at'] or previous['evidence_at']):
            raise HTTPException(409, STALE_ANCHOR)
        if body.carried_from_revision is not None:
            choices = remap(previous, route_view) if previous else []
            if (body.origin != 'manual' or not previous or body.carried_from_revision != previous['revision']
                    or previous['activity_id'] == body.activity_id or len(choices) != 1 or choices[0] != call
                    or previous['stop_place_id'] != parent or not point
                    or previous['coordinate_revision'] != point['revision']
                    or previous['mapping_revision'] != point['mapping_revision']
                    or previous['quay_version'] != point['quay_version']
                    or previous['stop_place_version'] != point['stop_place_version']):
                raise HTTPException(409, 'Det lagrede holdepunktet må velges manuelt i denne kjøringen.')
        if previous and body.origin == 'gps':
            before = next((value['position'] for value in route_view['calls']
                           if value['occurrence_id'] == previous['occurrence_id']), None)
            if (previous['activity_id'] != body.activity_id or previous['route_basis'] != body.route_basis
                    or before is None or before >= call['position']
                    or any(not value['coordinates'] for value in route_view['calls']
                           if before <= value['position'] <= call['position'])):
                raise HTTPException(409, 'Velg en ny forekomst manuelt før GPS-anslaget kan lagres.')
            if previous['origin'] == 'gps' and evidence - previous['evidence_at'] < MIN_GPS_SAVE_GAP:
                raise HTTPException(429, 'Det er for kort tid siden forrige GPS-holdepunkt ble lagret.')
        if not previous and body.origin == 'gps':
            raise HTTPException(409, 'Velg en forekomst manuelt før GPS-anslaget kan lagres.')
        if body.expected_revision >= MAX_RECEIPTS:
            raise HTTPException(429, 'Grensen for holdepunkt i denne arbeidsdagen er nådd.')
        revision = body.expected_revision + 1
        workday_storage.owned(conn, owner, identifier, request)
        receipt = conn.execute('INSERT INTO workday_position_anchor_operations '
                               '(id,workday_id,payload_hash,anchor_revision,accepted_at) VALUES(%s,%s,%s,%s,%s) '
                               'ON CONFLICT(id) DO NOTHING RETURNING *',
                               (body.operation_id, identifier, digest, revision, now)).fetchone()
        if not receipt:
            draft_storage.deny()
        fields = ('workday_id', 'activity_id', 'revision', 'route_revision', 'route_basis', 'source_version',
                  'coordinate_revision', 'mapping_revision', 'quay_version', 'stop_place_version', 'service_date',
                  'journey_id', 'pattern_id', 'occurrence_id', 'quay_id', 'stop_place_id', 'origin',
                  'evidence_at', 'asserted_at', 'saved_at', 'carried_from')
        asserted = evidence if body.origin == 'manual' else None
        carried = None
        if body.carried_from_revision is not None:
            # Preserve the offered evidence alongside the new assertion, with
            # at most one prior source and no nested handoff history.
            carried_fields = ('activity_id', 'revision', 'route_revision', 'route_basis', 'source_version',
                              'coordinate_revision', 'mapping_revision', 'quay_version', 'stop_place_version',
                              'service_date', 'journey_id', 'pattern_id', 'occurrence_id', 'quay_id',
                              'stop_place_id', 'origin', 'evidence_at')
            carried = Jsonb(jsonable_encoder({field: previous[field] for field in carried_fields}))
        conn.execute(f'INSERT INTO workday_position_anchors ({",".join(fields)}) VALUES '
                     f'({",".join(["%s"] * len(fields))}) ON CONFLICT(workday_id) DO UPDATE SET '
                     + ','.join(f'{field}=EXCLUDED.{field}' for field in fields[1:]),
                     (identifier, body.activity_id, revision, route['decision_revision'], route['basis'],
                      route['source_version'], body.coordinate_revision, point['mapping_revision'] if point else None,
                      point['quay_version'] if point else None, point['stop_place_version'] if point else None,
                      route['service_date'], route['journey_id'], route['pattern_id'], call['occurrence_id'],
                      quay, parent, body.origin, evidence, asserted, now, carried))
        workday_storage.owned(conn, owner, identifier, request)
        return accepted(receipt)
