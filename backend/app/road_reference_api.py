"""Read an approved public road snapshot only for its exact frozen journey."""

import json
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Request

from . import draft_storage, workday_storage
from .private_storage import database


router = APIRouter(prefix='/workdays/{identifier}/road-reference')
PUBLIC_SNAPSHOT = Path(__file__).with_name('road_data') / 'v2-approved.json'
MAX_BYTES = 2_000_000
IDENTITY_FIELDS = (
    'service_date', 'line_id', 'journey_id', 'journey_version', 'pattern_id', 'pattern_version',
    'direction', 'start_position', 'end_position',
)
QUALIFICATION = ('direction', 'coverage', 'topology', 'source', 'error_model')


def read_snapshot():
    try:
        with PUBLIC_SNAPSHOT.open('rb') as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            return None
        value = json.loads(raw)
    except (OSError, ValueError, RecursionError):
        return None
    if not isinstance(value, dict) or value.get('version') != 1:
        return None
    qualification = value.get('qualification')
    if not isinstance(qualification, dict) or any(
        not isinstance(qualification.get(key), str) or not qualification[key].strip() for key in QUALIFICATION
    ):
        return None
    if not isinstance(value.get('manifest'), dict):
        return None
    return value


def route_binding(reference):
    if not reference or reference.get('status') != 'compatible':
        return None
    if any(reference.get(field) is None for field in IDENTITY_FIELDS):
        return None
    provenance = reference.get('provenance')
    calls = reference.get('calls')
    if not isinstance(provenance, dict) or not isinstance(provenance.get('sha256'), str) or not isinstance(calls, list):
        return None
    start, end = reference['start_position'], reference['end_position']
    occurrences = [call['occurrence_id'] for call in calls if start <= call['position'] <= end]
    if not occurrences or len(set(occurrences)) != len(occurrences):
        return None
    return {**{field: reference[field] for field in IDENTITY_FIELDS},
            'route_source_sha256': provenance['sha256'], 'occurrence_ids': occurrences}


@router.get('/{activity_id}')
def road_reference(identifier: UUID, activity_id: UUID, request: Request):
    # Fixed packaged public data only. File I/O occurs outside the owner/plan lock.
    with database() as conn:
        owner = draft_storage.authorized(conn, request)
        workday_storage.owned(conn, owner, identifier, request)
        row = conn.execute(
            'SELECT reference FROM workday_route_references WHERE workday_id=%s AND activity_id=%s',
            (identifier, activity_id),
        ).fetchone()
    binding = route_binding(row['reference'] if row else None)
    if not binding:
        return {'status': 'route-unqualified'}
    snapshot = read_snapshot()
    if not snapshot:
        return {'status': 'road-unqualified'}
    if snapshot.get('binding') != binding:
        return {'status': 'road-unqualified'}
    return {'status': 'qualified', 'manifest': snapshot['manifest']}
