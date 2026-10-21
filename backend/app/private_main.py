import asyncio
from contextlib import asynccontextmanager, suppress
from uuid import UUID

import psycopg
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from . import auth
from . import draft_storage
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
                   allow_methods=['GET', 'POST'], allow_headers=['Content-Type', 'X-CSRF-Token'])


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
                limit = 1048576 if request.url.path == '/drafts' or request.url.path.startswith('/drafts/') else 4096
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
def drafts(request: Request):
    return draft_storage.listing(request)


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
