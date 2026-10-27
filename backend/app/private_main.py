import asyncio
from contextlib import asynccontextmanager, suppress
from uuid import UUID
from datetime import date
from typing import Annotated

import psycopg
from fastapi import FastAPI, HTTPException, Request, Response, Query
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from . import auth
from . import draft_storage
from . import workday_storage
from . import workday_bus_storage, workday_selection_storage, workday_lifecycle_storage
from .workday_selection_domain import SaveSelection, SelectionRecord, SelectionReceipt
from .workday_lifecycle_domain import StartWorkday, LifecycleRecord, StartReceipt
from .workday_lifecycle_domain import CloseWorkday
from .workday_outcome_domain import SaveOutcome, OutcomeRecord, OutcomeReceipt, WorkdayRecap
from . import workday_outcome_storage
from . import workday_notice_storage
from .workday_notice_domain import SaveNotice, NoticeCommand, NoticeRecord, NoticeList, NoticeReceipt, AccountNoticeCommand, SaveAccountNotice, AccountNoticeList
from .notice_reader_domain import NoticeReader
from .workday_bus_domain import SaveBus, BusRecord, BusReceipt
from .workday_domain import ConfirmRequest, ReviewRequest, Review, WorkdayRecord, WorkdayList, WorkdayOperation, DeleteWorkdayRequest, DeletedWorkday
from . import private_import
from .draft_time import LocalTime, TimeResolution, resolve as resolve_time
from .draft_domain import DeleteDraft, DeletedDraft, DraftContent, DraftList, DraftRecord, IssueOperation, IssuedOperation, OperationResult, SaveDraft
from .private_storage import cleanup, database


async def maintenance():
    while True:
        await asyncio.sleep(3600)
        try:
            await asyncio.to_thread(cleanup)
        except psycopg.Error:
            pass


@asynccontextmanager
async def lifespan(app):
    auth.configuration()
    cleanup()
    task = asyncio.create_task(maintenance())
    try:
        yield
    finally:
        await private_import.shutdown()
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


app = FastAPI(title='Privat arbeidsrom', lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(CORSMiddleware, allow_origins=[auth.configuration()], allow_credentials=True,
                   allow_methods=['GET', 'POST'], allow_headers=['Content-Type', 'X-CSRF-Token'], expose_headers=['Date'])


@app.middleware('http')
async def boundary(request, call_next):
    try:
        if request.method not in {'GET', 'HEAD', 'OPTIONS'}:
            await asyncio.to_thread(auth.check_mutation, request)
            if request.url.path == '/imports/pdf':
                response = await call_next(request)
                response.headers['Cache-Control'] = 'no-store'
                response.headers['Pragma'] = 'no-cache'
                response.headers['X-Content-Type-Options'] = 'nosniff'
                return response
            # Consume incrementally before JSON decoding; Content-Length is untrusted.
            body = bytearray()
            async for chunk in request.stream():
                limit = 1048576 if request.url.path == '/drafts' or request.url.path.startswith('/drafts/') else 32768 if '/notices' in request.url.path else 4096
                if len(body) + len(chunk) > limit:
                    raise HTTPException(413, 'Forespørselen er for stor.')
                body.extend(chunk)
            request._body = bytes(body)
        response = await call_next(request)
    except HTTPException as error:
        response = JSONResponse({'detail': error.detail}, status_code=error.status_code, headers=error.headers)
    except psycopg.Error:
        response = JSONResponse({'detail': 'Tjenesten er utilgjengelig.'}, status_code=503)
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.exception_handler(RequestValidationError)
async def validation_error(request, error):
    # FastAPI's default validation response echoes invalid inputs, including passwords.
    return JSONResponse({'detail': 'Kontroller feltene.'}, status_code=422)


def cookie(response, name, value, age):
    response.set_cookie(name, value, max_age=age, httponly=True, secure=False, samesite='strict', path='/')


def presentation(row):
    return {'account_id': row['owner'], 'created_at': row['created_at'], 'expires_at': row['expires_at']}


@app.get('/health')
def health():
    with database() as conn:
        conn.execute('SELECT 1')
    return {'status': 'ok', 'mode': 'private-local'}


@app.get('/auth/csrf')
def csrf(response: Response):
    token = auth.csrf_token()
    cookie(response, auth.CSRF, token, 3600)
    return {'csrf_token': token}


class Credentials(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=256)


@app.post('/auth/login')
def login(body: Credentials, request: Request, response: Response):
    token, row = auth.authenticate(body.username.strip().casefold(), body.password, request.client.host)
    # Revoke the existing browser session when changing identity.
    with database() as conn:
        conn.execute('DELETE FROM sessions WHERE token_hash=%s', (auth.digest(request.cookies.get(auth.SESSION, '')),))
    cookie(response, auth.SESSION, token, 14 * 86400)
    return presentation(row)


@app.get('/auth/session')
def current(request: Request):
    with database() as conn:
        return presentation(auth.session(conn, request))


@app.get('/accounts/{identifier}')
def profile(identifier: UUID, request: Request):
    with database() as conn:
        owner = auth.session(conn, request)['owner']
        if owner != identifier:
            raise HTTPException(404, 'Tilgangen ble avvist.')
        return {'account_id': owner}


@app.post('/auth/logout')
def logout(request: Request, response: Response):
    with database() as conn:
        conn.execute('DELETE FROM sessions WHERE token_hash=%s', (auth.digest(request.cookies.get(auth.SESSION, '')),))
    response.delete_cookie(auth.SESSION, path='/', httponly=True, samesite='strict')
    return {'revoked': True}


@app.get('/drafts', response_model=DraftList)
def drafts(request: Request, cursor: UUID | None = None):
    return draft_storage.listing(request, cursor)


@app.post('/imports/pdf', response_model=DraftContent)
async def import_pdf(request: Request):
    return await private_import.preview(request)


@app.get('/drafts/{identifier}', response_model=DraftRecord)
def draft(identifier: UUID, request: Request):
    return draft_storage.read(request, identifier)


@app.post('/draft-operations', response_model=IssuedOperation)
def issue_operation(body: IssueOperation, request: Request):
    return draft_storage.issue(request, body.draft_id)


@app.get('/draft-operations/{identifier}', response_model=OperationResult)
def find_operation(identifier: UUID, request: Request):
    return draft_storage.lookup(request, identifier)


@app.post('/drafts', response_model=DraftRecord)
def create_draft(body: SaveDraft, request: Request):
    return draft_storage.save(request, None, body)


@app.post('/drafts/{identifier}', response_model=DraftRecord)
def update_draft(identifier: UUID, body: SaveDraft, request: Request):
    return draft_storage.save(request, identifier, body)


@app.post('/drafts/{identifier}/delete', response_model=DeletedDraft)
def delete_draft(identifier: UUID, body: DeleteDraft, request: Request):
    return draft_storage.delete(request, identifier, body)


@app.get('/draft-deletions/{identifier}', response_model=DeletedDraft)
def find_deletion(identifier: UUID, request: Request):
    return draft_storage.deletion_lookup(request, identifier)


@app.post('/draft-times/resolve', response_model=TimeResolution)
def local_time(body: LocalTime, request: Request):
    with database() as conn:
        draft_storage.authorized(conn, request)
        try:
            result = resolve_time(body)
        except (ValueError, OverflowError):
            raise HTTPException(422, 'Kontroller dato og klokkeslett.') from None
        auth.session(conn, request)
        return result


@app.post('/workday-reviews', response_model=Review)
def review_workday(body: ReviewRequest, request: Request):
    return workday_storage.review(request, body)


@app.post('/drafts/{identifier}/confirm', response_model=WorkdayRecord)
def confirm_workday(identifier: UUID, body: ConfirmRequest, request: Request):
    return workday_storage.confirm(request, identifier, body)


@app.get('/workday-operations/{identifier}', response_model=WorkdayOperation)
def find_workday_operation(identifier: UUID, request: Request):
    return workday_storage.lookup(request, identifier)


@app.get('/workdays', response_model=WorkdayList)
def workdays(request: Request, cursor: UUID | None = None):
    return workday_storage.listing(request, cursor)


@app.get('/workdays/{identifier}', response_model=WorkdayRecord)
def workday(identifier: UUID, request: Request):
    return workday_storage.read(request, identifier)


@app.post('/workdays/{identifier}/delete', response_model=DeletedWorkday)
def delete_workday(identifier: UUID, body: DeleteWorkdayRequest, request: Request):
    return workday_storage.delete(request, identifier, body)


@app.get('/workday-deletions/{identifier}', response_model=DeletedWorkday)
def find_workday_deletion(identifier: UUID, request: Request):
    return workday_storage.deletion_lookup(request, identifier)


@app.get('/workdays/{identifier}/physical-bus', response_model=BusRecord)
def physical_bus(identifier: UUID, request: Request):
    return workday_bus_storage.read(request, identifier)


@app.post('/workdays/{identifier}/physical-bus', response_model=BusReceipt)
def save_physical_bus(identifier: UUID, body: SaveBus, request: Request):
    return workday_bus_storage.save(request, identifier, body)


@app.get('/workday-bus-operations/{identifier}', response_model=BusReceipt)
def find_bus_operation(identifier: UUID, request: Request):
    return workday_bus_storage.lookup(request, identifier)


@app.get('/workdays/{identifier}/selection', response_model=SelectionRecord)
def activity_selection(identifier: UUID, request: Request):
    return workday_selection_storage.read(request, identifier)


@app.post('/workdays/{identifier}/selection', response_model=SelectionReceipt)
def save_activity_selection(identifier: UUID, body: SaveSelection, request: Request):
    return workday_selection_storage.save(request, identifier, body)


@app.get('/workday-selection-operations/{identifier}', response_model=SelectionReceipt)
def find_selection_operation(identifier: UUID, request: Request):
    return workday_selection_storage.lookup(request, identifier)


@app.get('/workdays/{identifier}/outcomes', response_model=OutcomeRecord)
def activity_outcomes(identifier: UUID, request: Request):
    return workday_outcome_storage.read(request, identifier)


@app.post('/workdays/{identifier}/outcome', response_model=OutcomeReceipt)
def save_activity_outcome(identifier: UUID, body: SaveOutcome, request: Request):
    return workday_outcome_storage.save(request, identifier, body)


@app.get('/workday-outcome-operations/{identifier}', response_model=OutcomeReceipt)
def find_outcome_operation(identifier: UUID, request: Request):
    return workday_outcome_storage.lookup(request, identifier, 'outcome')


@app.post('/workdays/{identifier}/close', response_model=StartReceipt)
def close_workday(identifier: UUID, body: CloseWorkday, request: Request):
    return workday_outcome_storage.save(request, identifier, body, close=True)


@app.get('/workday-close-operations/{identifier}', response_model=StartReceipt)
def find_close_operation(identifier: UUID, request: Request):
    return workday_outcome_storage.lookup(request, identifier, 'close')


@app.get('/workdays/{identifier}/recap', response_model=WorkdayRecap)
def workday_recap(identifier: UUID, request: Request):
    return workday_outcome_storage.read(request, identifier, recap=True)


@app.get('/workdays/{identifier}/lifecycle', response_model=LifecycleRecord)
def workday_lifecycle(identifier: UUID, request: Request):
    return workday_lifecycle_storage.read(request, identifier)


@app.post('/workdays/{identifier}/start', response_model=StartReceipt)
def start_workday(identifier: UUID, body: StartWorkday, request: Request):
    return workday_lifecycle_storage.save(request, identifier, body)


@app.get('/workday-start-operations/{identifier}', response_model=StartReceipt)
def find_start_operation(identifier: UUID, request: Request):
    return workday_lifecycle_storage.lookup(request, identifier)


@app.get('/workdays/{identifier}/notice-reader', response_model=NoticeReader)
def notice_reader(identifier: UUID, request: Request, line: Annotated[str | None, Query(min_length=1, max_length=100)] = None, calendar_date: date | None = None):
    return workday_notice_storage.reader(request, identifier, line, calendar_date)


@app.get('/notices', response_model=AccountNoticeList)
def account_notices(request: Request, cursor: UUID | None = None):
    return workday_notice_storage.read(request, cursor=cursor)


@app.get('/notices/{notice_id}', response_model=NoticeRecord)
def account_notice(notice_id: UUID, request: Request):
    return workday_notice_storage.read(request, notice_id=notice_id)


class NoticeAdmission(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


@app.post('/notice-operations', response_model=IssuedOperation)
def issue_notice_operation(body: NoticeAdmission, request: Request):
    return workday_notice_storage.issue(request)


@app.post('/notices', response_model=NoticeReceipt)
def create_account_notice(body: SaveAccountNotice, request: Request):
    return workday_notice_storage.save(request, None, body)


@app.post('/notices/{notice_id}', response_model=NoticeReceipt)
def edit_account_notice(notice_id: UUID, body: SaveAccountNotice, request: Request):
    return workday_notice_storage.save(request, None, body, notice_id)


@app.post('/notices/{notice_id}/check', response_model=NoticeReceipt)
def check_account_notice(notice_id: UUID, body: AccountNoticeCommand, request: Request):
    return workday_notice_storage.save(request, None, body, notice_id, 'check')


@app.post('/notices/{notice_id}/end', response_model=NoticeReceipt)
def end_account_notice(notice_id: UUID, body: AccountNoticeCommand, request: Request):
    return workday_notice_storage.save(request, None, body, notice_id, 'end')


@app.get('/workdays/{identifier}/notices', response_model=NoticeList)
def notices(identifier: UUID, request: Request, cursor: UUID | None = None):
    return workday_notice_storage.read(request, identifier, cursor=cursor)


@app.get('/workdays/{identifier}/notices/{notice_id}', response_model=NoticeRecord)
def notice(identifier: UUID, notice_id: UUID, request: Request):
    return workday_notice_storage.read(request, identifier, notice_id)


@app.post('/workdays/{identifier}/notices', response_model=NoticeReceipt)
def create_notice(identifier: UUID, body: SaveNotice, request: Request):
    return workday_notice_storage.save(request, identifier, body)


@app.post('/workdays/{identifier}/notices/{notice_id}', response_model=NoticeReceipt)
def edit_notice(identifier: UUID, notice_id: UUID, body: SaveNotice, request: Request):
    return workday_notice_storage.save(request, identifier, body, notice_id)


@app.post('/workdays/{identifier}/notices/{notice_id}/check', response_model=NoticeReceipt)
def check_notice(identifier: UUID, notice_id: UUID, body: NoticeCommand, request: Request):
    return workday_notice_storage.save(request, identifier, body, notice_id, 'check')


@app.post('/workdays/{identifier}/notices/{notice_id}/end', response_model=NoticeReceipt)
def end_notice(identifier: UUID, notice_id: UUID, body: NoticeCommand, request: Request):
    return workday_notice_storage.save(request, identifier, body, notice_id, 'end')


@app.get('/workday-notice-operations/{identifier}', response_model=NoticeReceipt)
def find_notice_operation(identifier: UUID, request: Request):
    return workday_notice_storage.lookup(request, identifier)
