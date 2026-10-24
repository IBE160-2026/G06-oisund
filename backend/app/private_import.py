"""Transient private PDF interpretation. Nothing in this module writes storage."""
import asyncio
from threading import BoundedSemaphore, Event
from uuid import uuid4

from fastapi import HTTPException, Request

from . import auth
from .draft_domain import DraftContent, SourceHeader
from .pdf_import import MAX_BYTES, ImportFailure, extract_pdf
from .private_storage import database
from .import_issues import issue_text

slots = BoundedSemaphore(2)
active: set[Event] = set()
UPLOAD_TIMEOUT = 30


def authorize(request):
    # Short read-only transaction; extraction never holds an account/session lock.
    with database() as conn:
        return auth.session(conn, request)['owner']


def interpret(source):
    header = {key: value for key, value in source['header'].items() if key in SourceHeader.model_fields}
    # Extended headers and DST dates have no qualification evidence.
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    day = datetime.fromisoformat(header['service_date']).replace(tzinfo=ZoneInfo('Europe/Oslo'))
    finish = datetime.fromisoformat(header['end_instant']) if header['end_instant'] else day
    if int(header['start'].split(':')[0]) >= 24 or day.utcoffset() != (day + timedelta(days=1)).utcoffset() or day.utcoffset() != finish.utcoffset():
        raise ImportFailure('unqualified_calendar')
    rows, source_rows = [], []
    for row in source['activities']:
        identifier = str(uuid4())
        unknown = [issue_text(item) for item in source['unresolved'] if item.get('activity') == row['source_order']]
        if row['kind'] == 'Travel to' and not row['start_instant']:
            unknown.append('Aktivitetstypen er uavklart. Travel to er beholdt fra kilden.')
        rows.append(dict(id=identifier, type=None if row['kind'] == 'Travel to' and not row['start_instant'] else 'Tomkjøring med CAR' if row['kind'] == 'deadhead_car' else row['kind'],
                         raw_code=row['label'], start=row['start_instant'], end=row['end_instant'],
                         source_start=row['start'], source_end=row['end'], from_place=row['origin'],
                         to_place=row['destination'], trip=row['trip_id'], line=row['line'], direction=None,
                         uncertainty=' '.join(dict.fromkeys(unknown))[:1000] or None, provenance='PDF: kildefakta; kalender avledet fra oppgitt skiftintervall.'))
        origins = {key: 'unresolved' if value is None else 'derived' if key in ('kind', 'start_instant', 'end_instant', 'start_day', 'end_day') else 'extracted'
                   for key, value in row.items() if key not in ('provenance', 'pages', 'source_order')}
        if row['kind'] == 'Travel to' and not row['start_instant']:
            origins['kind'] = 'unresolved'
        source_rows.append({**row, 'activity_id': identifier, 'origins': origins})
    metadata = dict(version=1, qualification='partial' if source['unresolved'] else 'bounded-layout',
                    timezone='Europe/Oslo', header=header,
                    header_provenance={key: value for key, value in source['provenance']['header'].items() if key in header},
                    activities=source_rows, duties=source['duties'], annotations=source['annotations'],
                    unresolved=source['unresolved'], pause_groups=source['pause_groups'])
    duty = source['duties'][0]['value'] if source['duties'] else None
    changes = []
    previous = duty
    for occurrence in source['duties']:
        if occurrence['value'] != previous and occurrence['after_activity'] < len(rows):
            changes.append(dict(from_activity_id=rows[occurrence['after_activity']]['id'], vehicle_duty=occurrence['value']))
            previous = occurrence['value']
    return DraftContent.model_validate(dict(service_date=header['service_date'], vehicle_duty=duty,
                                            physical_bus=None, activities=rows, import_metadata=metadata,
                                            vehicle_duty_changes=changes or None))


async def preview(request: Request):
    owner = await asyncio.to_thread(authorize, request)
    if request.headers.get('content-type', '').split(';')[0] != 'application/pdf':
        raise HTTPException(415, 'Velg en tekst-PDF. Du kan også opprette et manuelt utkast.')
    if not slots.acquire(blocking=False):
        raise HTTPException(429, 'Import er opptatt. Prøv igjen eller opprett et manuelt utkast.')
    cancel = Event()
    active.add(cancel)
    data = bytearray()
    worker = None
    try:
        async with asyncio.timeout(UPLOAD_TIMEOUT):
            async for chunk in request.stream():
                if cancel.is_set():
                    raise HTTPException(499, 'Importen ble avbrutt.')
                if len(data) + len(chunk) > MAX_BYTES:
                    raise HTTPException(413, 'PDF-en er større enn 10 MiB. Opprett et manuelt utkast.')
                data.extend(chunk)
        worker = asyncio.create_task(asyncio.to_thread(extract_pdf, bytes(data), cancel=cancel))
        data.clear()
        while not worker.done():
            if await request.is_disconnected():
                cancel.set()
                raise HTTPException(499, 'Importen ble avbrutt.')
            await asyncio.sleep(.05)
        source = await worker
        try:
            result = interpret(source)
        except (ValueError, OverflowError):
            raise ImportFailure('unsupported_facts') from None
        source.clear()
        if cancel.is_set() or await request.is_disconnected():
            raise HTTPException(499, 'Importen ble avbrutt.')
        if await asyncio.to_thread(authorize, request) != owner:
            raise HTTPException(401, 'Logg inn på nytt.')
        return result
    except ImportFailure:
        raise HTTPException(422, 'PDF-en kunne ikke tolkes innenfor støttede grenser. Velg en kvalifisert tekst-PDF eller opprett et manuelt utkast.') from None
    except TimeoutError:
        raise HTTPException(408, 'Opplastingen tok for lang tid. Prøv igjen eller opprett et manuelt utkast.') from None
    finally:
        data.clear()
        cancel.set()
        cancelled_during_cleanup = False
        if worker:
            # Repeated request cancellation must not release admission while the
            # thread still owns a PDF process. Only actual completion frees it.
            while not worker.done():
                try:
                    await asyncio.shield(worker)
                except asyncio.CancelledError:
                    cancelled_during_cleanup = True
                except Exception:
                    break
            with __import__('contextlib').suppress(Exception, asyncio.CancelledError):
                worker.result()
        active.discard(cancel)
        slots.release()
        if cancelled_during_cleanup:
            raise asyncio.CancelledError


async def shutdown():
    for event in tuple(active):
        event.set()
    while active:
        await asyncio.sleep(.05)
