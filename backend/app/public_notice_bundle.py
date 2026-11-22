"""Carry a bounded public Entur SIRI-SX observation across the private network boundary."""

import argparse
import asyncio
from datetime import UTC, datetime, timedelta
from io import BytesIO
import json
import sys
from time import monotonic
from uuid import UUID, uuid4
from zipfile import ZIP_STORED, ZipFile

from .automatic_notice_ingestion import (
    COORDINATOR, CYCLE_INTERVAL, CYCLE_SECONDS, MAX_PAGES, MAX_XML_BYTES, download_page, finish,
)
from .automatic_notice_source import SourceError, instant, parse_page


PAGE_SPACING = 15.1
MAX_BUNDLE_BYTES = MAX_PAGES * MAX_XML_BYTES + 24_000
MAX_RETRY = 100_000_000
FAILURES = {
    'rate-limited', 'http-unavailable', 'http-status', 'content-encoding', 'content-type',
    'xml-size', 'timeout', 'network', 'cycle-budget', 'page-budget', 'repeated-identity',
    'stalled-page', 'response-time-regression', 'source-invalid',
}


def now():
    return datetime.now(UTC)


def validate_page(page, identities, previous_response, fetched):
    if abs(page.response_at - fetched) > timedelta(minutes=5):
        raise SourceError('source-invalid')
    keys = {(item['participant'], item['situation']) for item in page.items}
    if len(keys) != len(page.items) or identities & keys:
        raise SourceError('repeated-identity')
    if not keys and (page.more or previous_response is not None):
        raise SourceError('stalled-page')
    if previous_response is not None and page.response_at < previous_response:
        raise SourceError('response-time-regression')
    identities.update(keys)


async def collect(started, fetch=download_page, sleep=asyncio.sleep):
    requestor = uuid4()
    buffer = BytesIO()
    elapsed = (now() - started).total_seconds()
    if not -5 <= elapsed <= 30:
        raise ValueError('SIRI cycle reservation expired before collection')
    deadline = monotonic() + CYCLE_SECONDS - max(0, elapsed)
    metadata, identities = [], set()
    previous_response = None
    failure = None
    with ZipFile(buffer, 'w', compression=ZIP_STORED) as output:
        try:
            for index in range(MAX_PAGES):
                remaining = deadline - monotonic()
                if remaining <= 0:
                    raise SourceError('cycle-budget')
                body, headers = await fetch(requestor, remaining)
                fetched = now()
                page = parse_page(body, headers, requestor)
                validate_page(page, identities, previous_response, fetched)
                name = f'page-{index:02}.xml'
                output.writestr(name, body)
                metadata.append({'file': name, 'headers': headers, 'observed_at': fetched.isoformat()})
                previous_response = page.response_at
                if not page.more:
                    break
                if deadline - monotonic() <= PAGE_SPACING:
                    raise SourceError('cycle-budget')
                await sleep(PAGE_SPACING)
            else:
                raise SourceError('page-budget')
        except SourceError as error:
            failure = {'code': error.code if error.code in FAILURES else 'source-invalid',
                       'retry_after': min(MAX_RETRY, error.retry_after)}
        output.writestr('receipt.json', json.dumps({
            'dataset': 'TRO', 'requestor': str(requestor), 'started_at': started.isoformat(),
            'pages': metadata, 'failure': failure,
        }))
    return buffer.getvalue()


def read_bundle(raw, observed):
    if not 0 < len(raw) <= MAX_BUNDLE_BYTES:
        raise ValueError('SIRI bundle exceeds its byte limit')
    with ZipFile(BytesIO(raw)) as archive:
        inventory = archive.infolist()
        members = {item.filename for item in inventory}
        if (not 1 <= len(inventory) <= MAX_PAGES + 1 or len(members) != len(inventory) or 'receipt.json' not in members
                or any(item.flag_bits & 1 or item.compress_type != ZIP_STORED or not 0 < item.file_size <=
                       (16_000 if item.filename == 'receipt.json' else MAX_XML_BYTES) for item in inventory)):
            raise ValueError('Unexpected SIRI bundle inventory')
        receipt = json.loads(archive.read('receipt.json'))
        started, requestor = instant(receipt['started_at']), UUID(receipt['requestor'])
        if (receipt['dataset'] != 'TRO' or started is None
                or not observed - timedelta(seconds=CYCLE_SECONDS + 60) <= started <= observed + timedelta(seconds=5)):
            raise ValueError('SIRI bundle has the wrong scope or observation time')
        records, responses = [], []
        identities = set()
        pages = receipt['pages']
        if not isinstance(pages, list) or len(pages) != len(members) - 1:
            raise ValueError('SIRI receipt does not match the page inventory')
        payload_failure = receipt['failure']
        failure = None
        if payload_failure is not None:
            code, retry = payload_failure['code'], payload_failure['retry_after']
            if code not in FAILURES or type(retry) is not int or not 0 <= retry <= MAX_RETRY:
                raise ValueError('Invalid SIRI failure metadata')
            failure = SourceError(code, retry)
        if not pages and failure is None:
            raise ValueError('SIRI bundle lacks a completed first page')
        previous_fetch = started
        for index, entry in enumerate(pages):
            name = f'page-{index:02}.xml'
            fetched = instant(entry['observed_at'])
            if (entry['file'] != name or name not in members or fetched is None
                    or not previous_fetch <= fetched <= min(observed + timedelta(seconds=5), started + timedelta(seconds=CYCLE_SECONDS + 1))):
                raise ValueError('SIRI bundle page has an invalid observation')
            if index and (fetched - previous_fetch).total_seconds() < PAGE_SPACING - .1:
                raise ValueError('SIRI bundle exceeded its allowed request cadence')
            page = parse_page(archive.read(name), entry['headers'], requestor)
            validate_page(page, identities, responses[-1] if responses else None, fetched)
            if page.more != (index < len(pages) - 1 or failure is not None):
                raise ValueError('SIRI bundle has an invalid completion sequence')
            records.extend((item, fetched, page.response_at) for item in page.items)
            responses.append(page.response_at)
            previous_fetch = fetched
    return requestor, started, responses, records, failure


def reserve():
    from .private_storage import database

    with database() as conn:
        row = conn.execute("""UPDATE automatic_notice_feed SET status='collecting', attempt_at=clock_timestamp(),
                                next_request_at=clock_timestamp()+%s*interval '1 second',
                                result_at=NULL, response_at=NULL, attempt_pages=0, attempt_count=0, failure=NULL
                              WHERE (attempt_at IS NULL OR attempt_at <= clock_timestamp()-%s*interval '1 second')
                                AND next_request_at <= clock_timestamp() RETURNING attempt_at""",
                           (CYCLE_INTERVAL, CYCLE_INTERVAL)).fetchone()
    return row['attempt_at'].isoformat() if row else None


def publish(prepared):
    from .private_storage import database

    requestor, started, responses, records, failure = prepared
    with database() as conn:
        if not conn.execute('SELECT pg_try_advisory_xact_lock(%s) AS writer', (COORDINATOR,)).fetchone()['writer']:
            raise ValueError('A SIRI writer is already active')
        admitted = conn.execute("""SELECT id FROM automatic_notice_feed
                                    WHERE status='collecting' AND attempt_at=%s FOR UPDATE""", (started,)).fetchone()
        if admitted is None:
            raise ValueError('SIRI receipt is a replay or within the cycle cooldown')
        finish(conn, requestor, responses, records, failure)
    return {'dataset': 'TRO', 'records': len(records), 'pages': len(responses), 'complete': failure is None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument('--fetch', action='store_true')
    actions.add_argument('--publish-stdin', action='store_true')
    actions.add_argument('--reserve', action='store_true')
    parser.add_argument('--started-at', type=instant)
    args = parser.parse_args()
    if args.fetch:
        if args.started_at is None:
            parser.error('--fetch requires an explicit UTC reservation timestamp')
        sys.stdout.buffer.write(asyncio.run(collect(args.started_at)))
    elif args.reserve:
        print(json.dumps({'started_at': reserve()}))
    else:
        print(json.dumps(publish(read_bundle(sys.stdin.buffer.read(MAX_BUNDLE_BYTES + 1), now()))))


if __name__ == '__main__':
    main()
