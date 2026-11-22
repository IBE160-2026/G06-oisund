"""Coordinate fresh, bounded Entur TRO baselines across private API workers."""

import asyncio
import logging
import os
from datetime import datetime, UTC, timedelta
from email.utils import parsedate_to_datetime
from time import monotonic
from uuid import uuid4

import httpx
import psycopg
from psycopg.types.json import Jsonb

from .automatic_notice_source import MAX_XML_BYTES, PAGE_SIZE, SourceError, instant, parse_page, source_revision
from .private_storage import database


ENDPOINT = 'https://api.entur.io/realtime/v1/rest/sx'
COORDINATOR = 1230197601
MAX_PAGES = 12
CYCLE_SECONDS = 210
REQUEST_SECONDS = 10
CYCLE_INTERVAL = 300
RECEIVE_TIMEOUT = 20
LOG = logging.getLogger('private.automatic_notices')


def enabled():
    return (os.getenv('V2_NOTICE_REFRESH') == 'on'
            and os.getenv('APP_MODE') == 'private-local'
            and os.getenv('PRIVATE_TEST_PROJECT') == 'disabled'
            and os.getenv('PRIVATE_ORIGIN') == 'http://127.0.0.1:19661'
            and os.getenv('PRIVATE_LOOPBACK_DEVELOPMENT') == '1')


def backoff(value):
    if not value:
        return 60
    try:
        seconds = int(value) if value.isascii() and value.isdigit() and len(value) <= 8 else (
            parsedate_to_datetime(value).astimezone(UTC) - datetime.now(UTC)).total_seconds()
        return max(60, int(seconds) + 1)
    except (TypeError, ValueError, OverflowError):
        return 60


async def download_page(requestor, remaining):
    try:
        async with asyncio.timeout(min(REQUEST_SECONDS, remaining)):
            async with httpx.AsyncClient(follow_redirects=False, trust_env=False) as client:
                async with client.stream(
                    'GET', ENDPOINT, params={'datasetId': 'TRO', 'maxSize': PAGE_SIZE, 'requestorId': str(requestor)},
                    headers={'ET-Client-Name': 'ibe160-bussassistent-v2', 'Accept': 'application/xml',
                             'Accept-Encoding': 'identity'},
                ) as response:
                    if response.status_code == 429:
                        raise SourceError('rate-limited', backoff(response.headers.get('Retry-After')))
                    if response.status_code == 503:
                        raise SourceError('http-unavailable', backoff(response.headers.get('Retry-After')))
                    if response.status_code != 200:
                        raise SourceError('http-status')
                    if response.headers.get('Content-Encoding', 'identity').lower() != 'identity':
                        raise SourceError('content-encoding')
                    if response.headers.get('Content-Type', '').split(';', 1)[0].strip().lower() not in (
                        'application/xml', 'text/xml',
                    ):
                        raise SourceError('content-type')
                    body = bytearray()
                    async for chunk in response.aiter_raw(chunk_size=16_384):
                        if len(body) + len(chunk) > MAX_XML_BYTES:
                            raise SourceError('xml-size')
                        body.extend(chunk)
                    headers = {name: response.headers.get(name) for name in ('datasetid', 'requestorid')}
                    return bytes(body), headers
    except (httpx.TimeoutException, TimeoutError):
        raise SourceError('timeout') from None
    except httpx.HTTPError:
        raise SourceError('network') from None


async def get_page(requestor, remaining):
    raw, headers = await download_page(requestor, remaining)
    return parse_page(raw, headers, requestor)


def reserve(conn, stop, deadline):
    # Persist the reservation before the GET, even if the process dies mid-call.
    # Spacing by >15 seconds is conservative for any rolling minute, across workers/restarts.
    with conn.transaction():
        wait = conn.execute("SELECT CASE WHEN next_request_at > clock_timestamp() "
                            "THEN extract(epoch FROM next_request_at-clock_timestamp()) ELSE 0 END AS seconds "
                            "FROM automatic_notice_feed").fetchone()['seconds']
    wait = max(0, float(wait))
    if monotonic() + wait >= deadline:
        raise SourceError('cycle-budget')
    if stop.wait(wait):
        raise SourceError('interrupted')
    with conn.transaction():
        conn.execute("UPDATE automatic_notice_feed SET next_request_at=clock_timestamp()+%s*interval '1 second'",
                     (REQUEST_SECONDS + 15.1,))


def finish_request(conn):
    # A fresh reservation survives a crash during I/O. A reply or timeout lets
    # us time the next GET from the latest possible start of this request.
    with conn.transaction():
        conn.execute("UPDATE automatic_notice_feed SET next_request_at=clock_timestamp()+interval '15.1 seconds'")


def ordering(incoming, current):
    versions = [item['version'] for item in (incoming, current)]
    if all(isinstance(value, str) and value.isascii() and value.isdigit() for value in versions):
        new, old = map(int, versions)
        return (new > old) - (new < old)
    new = instant(incoming['publisher_updated_at'])
    old = instant(current['publisher_updated_at'])
    if new is not None and old is not None:
        return (new > old) - (new < old)
    return 0


def keep_observation(conn, data, fetched_at, response_at, generation):
    key = (data['participant'], data['situation'])
    digest = source_revision(data)
    current = conn.execute('SELECT revision,content FROM automatic_notice_sources '
                           'WHERE participant=%s AND situation=%s AND current_revision', key).fetchone()
    same = current is not None and current['revision'] == digest
    order = ordering(data, current['content']) if current and not same else 0
    replace = not current or same or (order > 0 and (generation is not None or data['progress'] == 'closed'))
    if replace and not same:
        conn.execute('UPDATE automatic_notice_sources SET current_revision=false,superseded_at=%s '
                     'WHERE participant=%s AND situation=%s AND current_revision', (fetched_at, *key))
        if current:
            conflicts = conn.execute('SELECT revision,content FROM automatic_notice_sources '
                                     'WHERE participant=%s AND situation=%s AND conflicting', key).fetchall()
            for conflict in conflicts:
                if ordering(data, conflict['content']) > 0:
                    conn.execute('UPDATE automatic_notice_sources SET conflicting=false,superseded_at=%s '
                                 'WHERE participant=%s AND situation=%s AND revision=%s',
                                 (fetched_at, *key, conflict['revision']))
    conn.execute('INSERT INTO automatic_notice_sources(participant,situation,revision,content,first_seen,last_seen,'
                 'fetched_at,response_at,last_complete_generation,current_revision,conflicting,superseded_at) '
                 'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(participant,situation,revision) DO UPDATE SET '
                 "content=automatic_notice_sources.content || jsonb_build_object('verified_siri_scope',EXCLUDED.content->'verified_siri_scope'),"
                 'last_seen=EXCLUDED.last_seen,fetched_at=EXCLUDED.fetched_at,response_at=EXCLUDED.response_at,'
                 'last_complete_generation=COALESCE(EXCLUDED.last_complete_generation,automatic_notice_sources.last_complete_generation),'
                 'current_revision=EXCLUDED.current_revision,conflicting=EXCLUDED.conflicting,'
                 'superseded_at=EXCLUDED.superseded_at',
                 (*key, digest, Jsonb(data), fetched_at, fetched_at, fetched_at, response_at, generation,
                  replace, not replace and order >= 0, None if replace or order >= 0 else fetched_at))
    conn.execute('INSERT INTO automatic_notice_identities(participant,situation,last_seen,last_complete_generation) '
                 'VALUES(%s,%s,%s,%s) ON CONFLICT(participant,situation) DO UPDATE SET '
                 'last_seen=EXCLUDED.last_seen,last_complete_generation=COALESCE(EXCLUDED.last_complete_generation,'
                 'automatic_notice_identities.last_complete_generation)', (*key, fetched_at, generation))


def finish(conn, requestor, pages, observations, failure):
    generation = requestor if failure is None else None
    status = 'complete' if failure is None else 'partial' if pages else 'unavailable'
    with conn.transaction():
        conn.execute('SELECT id FROM automatic_notice_feed FOR UPDATE')
        for data, fetched_at, response_at in observations:
            keep_observation(conn, data, fetched_at, response_at, generation)
        conn.execute('UPDATE automatic_notice_feed SET status=%s,result_at=clock_timestamp(),attempt_pages=%s,'
                     'attempt_count=%s,failure=%s,response_at=%s,next_request_at=CASE WHEN %s>0 THEN '
                     "greatest(next_request_at,clock_timestamp()+%s*interval '1 second') ELSE next_request_at END",
                     (status, len(pages), len(observations), failure.code if failure else None,
                      pages[-1] if pages else None, failure.retry_after if failure else 0,
                      failure.retry_after if failure else 0))
        if generation:
            conn.execute('UPDATE automatic_notice_feed SET generation=%s,baseline_at=attempt_at,'
                         'synchronized_at=result_at,baseline_count=%s', (generation, len(observations)))


def run_cycle(stop, fetch=get_page):
    requestor = uuid4()
    with database() as conn:
        with conn.transaction():
            if not conn.execute('SELECT pg_try_advisory_lock(%s) AS writer', (COORDINATOR,)).fetchone()['writer']:
                return
            admitted = conn.execute("UPDATE automatic_notice_feed SET status='collecting',"
                                    "attempt_at=clock_timestamp(),result_at=NULL,response_at=NULL,"
                                    "attempt_pages=0,attempt_count=0,failure=NULL WHERE "
                                    "(attempt_at IS NULL OR attempt_at <= clock_timestamp()-%s*interval '1 second') "
                                    "AND next_request_at <= clock_timestamp() RETURNING id", (CYCLE_INTERVAL,)).fetchone()
        if admitted is None:
            return
        deadline = monotonic() + CYCLE_SECONDS
        identities = set()
        observations = []
        pages = []
        try:
            for _ in range(MAX_PAGES):
                reserve(conn, stop, deadline)
                try:
                    page = asyncio.run(fetch(requestor, deadline - monotonic()))
                finally:
                    finish_request(conn)
                keys = {(item['participant'], item['situation']) for item in page.items}
                if len(keys) != len(page.items) or identities & keys:
                    raise SourceError('repeated-identity')
                if not keys and (page.more or pages):
                    raise SourceError('stalled-page')
                if pages and page.response_at < pages[-1]:
                    raise SourceError('response-time-regression')
                fetched_at = datetime.now(UTC)
                identities.update(keys)
                pages.append(page.response_at)
                observations.extend((item, fetched_at, page.response_at) for item in page.items)
                with conn.transaction():
                    conn.execute('UPDATE automatic_notice_feed SET attempt_pages=%s,attempt_count=%s,response_at=%s',
                                 (len(pages), len(observations), page.response_at))
                if not page.more:
                    break
            else:
                raise SourceError('page-budget')
        except SourceError as failure:
            finish(conn, requestor, pages, observations, failure)
        else:
            finish(conn, requestor, pages, observations, None)


async def periodic(stop):
    while not stop.is_set():
        try:
            await asyncio.to_thread(run_cycle, stop)
        except psycopg.Error:
            LOG.warning('automatic_notice_database_unavailable')
        await asyncio.to_thread(stop.wait, RECEIVE_TIMEOUT)
