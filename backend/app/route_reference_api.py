"""Authorized route-reference resources separate from strict draft/workday DTOs."""

from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, Request

from . import draft_storage, route_reference_storage as routes, workday_storage
from .private_storage import database

router = APIRouter()
Revision = Annotated[int, Query(ge=1)]
LineCode = Annotated[str, Query(pattern=r'^(?:X?[0-9]{2}|26B)$')]
JourneyId = Annotated[str, Query(pattern=r'^TRO:ServiceJourney:[A-Za-z0-9_./-]{1,200}$')]
SourceDigest = Annotated[str, Query(pattern=r'^[a-f0-9]{64}$')]


@router.get('/route-catalogue')
def browse(request: Request, service_date: date, line_code: LineCode,
           journey_id: JourneyId | None = None, source_sha256: SourceDigest | None = None):
    return routes.browse(request, service_date, line_code, journey_id, source_sha256)


@router.get('/drafts/{identifier}/route-references')
def draft_references(identifier: UUID, revision: Revision, request: Request):
    return routes.read_draft(request, identifier, revision)


@router.post('/drafts/{identifier}/route-references/resolve')
def resolve_references(identifier: UUID, revision: Revision, request: Request):
    return routes.resolve_draft(request, identifier, revision)


@router.get('/drafts/{identifier}/route-departures')
def departures(identifier: UUID, revision: Revision, activity_id: UUID, request: Request,
               journey_id: JourneyId | None = None, line_code: LineCode | None = None):
    return routes.public_snapshot(request, identifier, revision, activity_id, journey_id, line_code)


@router.post('/drafts/{identifier}/route-references')
def save_reference(identifier: UUID, body: routes.SaveRoute, request: Request):
    return routes.save(request, identifier, body)


@router.get('/drafts/{identifier}/route-reference-operations/{operation_id}')
def route_operation(identifier: UUID, operation_id: UUID, request: Request):
    return routes.lookup(request, identifier, operation_id)


@router.get('/workdays/{identifier}/route-references')
def frozen_references(identifier: UUID, request: Request):
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        workday_storage.owned(conn, owner, identifier, request)
        references = conn.execute('SELECT reference FROM workday_route_references WHERE workday_id=%s ORDER BY activity_id',
                                  (identifier,)).fetchall()
        workday_storage.owned(conn, owner, identifier, request)
        return {'workday_id': identifier, 'references': [row['reference'] for row in references]}
