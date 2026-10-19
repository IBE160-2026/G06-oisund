import asyncio
from contextlib import asynccontextmanager, suppress
from datetime import datetime
from uuid import UUID, uuid4

import psycopg
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from psycopg.types.json import Jsonb

from .domain import CreateDay, FIXTURE, FictionalDay, StrictModel
from .storage import OWNER, cleanup, database


async def maintenance():
    while True:
        await asyncio.sleep(3600)
        try:
            await asyncio.to_thread(cleanup)
        except psycopg.Error:
            pass  # No private payloads or credentials in logs; health exposes failure.


@asynccontextmanager
async def lifespan(app):
    cleanup()  # Also validates assessment configuration, failing closed on startup.
    task = asyncio.create_task(maintenance())
    yield
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task


class SavedDay(StrictModel):
    id: UUID
    day: FictionalDay
    created_at: datetime
    expires_at: datetime


class Empty(StrictModel):
    pass


app = FastAPI(title='Fiktive demodata', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=['http://127.0.0.1:5173'],
                   allow_methods=['GET', 'POST'], allow_headers=['Content-Type'])


@app.middleware('http')
async def boundary(request: Request, call_next):
    if request.method == 'POST' and request.headers.get('origin') not in {None, 'http://127.0.0.1:5173'}:
        return JSONResponse({'detail': 'Origin denied'}, status_code=403, headers={'Cache-Control': 'no-store'})
    try:
        response = await call_next(request)
    except psycopg.Error:
        response = JSONResponse({'detail': 'Fictional database unavailable'}, status_code=503)
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.get('/health')
def health():
    with database() as conn:
        conn.execute('SELECT 1')
    return {'status': 'ok', 'mode': 'fictional-assessment'}


@app.get('/fixture', response_model=FictionalDay)
def fixture():
    return FIXTURE


@app.post('/operations')
def operation(body: Empty | None = None):
    identifier = uuid4()
    with database() as conn:
        conn.execute('INSERT INTO creation_operations (id, owner) VALUES (%s,%s)', (identifier, OWNER))
    return {'operation_id': identifier}


def saved(row):
    return SavedDay(id=row['id'], day=row['payload'], created_at=row['created_at'], expires_at=row['expires_at'])


@app.post('/days', response_model=SavedDay)
def create_day(body: CreateDay):
    payload = body.day.model_dump(mode='json')
    with database() as conn:
        op = conn.execute('SELECT * FROM creation_operations WHERE id=%s AND owner=%s '
                          'AND expires_at > clock_timestamp() FOR UPDATE', (body.operation_id, OWNER)).fetchone()
        if not op:
            raise HTTPException(410, 'Operation unknown or expired; no replay accepted')
        previous = conn.execute('SELECT * FROM fictional_days WHERE operation_id=%s AND owner=%s',
                                (body.operation_id, OWNER)).fetchone()
        if previous:
            if previous['expires_at'] <= conn.execute('SELECT clock_timestamp() AS now').fetchone()['now']:
                raise HTTPException(410, 'Fictional day expired')
            if previous['payload'] != payload:
                raise HTTPException(409, 'Operation already accepted with different values')
            return saved(previous)
        if payload != FIXTURE.model_dump(mode='json'):
            raise HTTPException(422, 'Only the fixed fictional example is accepted')
        row = conn.execute('INSERT INTO fictional_days (id,operation_id,owner,payload,created_at,expires_at) '
                           "VALUES (%s,%s,%s,%s,statement_timestamp(),statement_timestamp()+interval '7 days') RETURNING *",
                           (uuid4(), body.operation_id, OWNER, Jsonb(payload))).fetchone()
        conn.execute('UPDATE creation_operations SET expires_at=%s WHERE id=%s',
                     (row['expires_at'], body.operation_id))
        return saved(row)


@app.get('/days/{identifier}', response_model=SavedDay)
def read_day(identifier: UUID):
    with database() as conn:
        row = conn.execute('SELECT * FROM fictional_days WHERE id=%s AND owner=%s '
                           'AND expires_at > clock_timestamp()', (identifier, OWNER)).fetchone()
        if not row:
            raise HTTPException(410, 'Fictional day unknown or expired')
        return saved(row)
