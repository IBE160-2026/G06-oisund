"""Public SIRI batches preserve the established evidence and completion checks."""

import asyncio
from contextlib import contextmanager
from datetime import datetime, timedelta
from io import BytesIO
import json
import os
from zipfile import ZipFile

import pytest

from app import public_notice_bundle as bundle
from app.automatic_notice_source import SourceError
from test_automatic_notice_rules import NOW, envelope, situation


def capture(monkeypatch, results, start=NOW):
    wall = start
    iterator = iter(results)
    monkeypatch.setattr(bundle, 'now', lambda: wall)

    async def fetch(requestor, _):
        result = next(iterator)
        if isinstance(result, SourceError):
            raise result
        name, more = result
        return envelope(situation(name), more, requestor, wall.isoformat()), {
            'datasetid': 'TRO', 'requestorid': str(requestor),
        }

    async def sleep(seconds):
        nonlocal wall
        wall += timedelta(seconds=seconds)

    return asyncio.run(bundle.collect(start, fetch, sleep)), wall


def test_transport_revalidates_complete_pages(monkeypatch):
    raw, receive = capture(monkeypatch, [('first', 'true'), ('second', 'false')])
    requestor, started, pages, items, failure = bundle.read_bundle(raw, receive)
    assert started == NOW and len(pages) == 2 and failure is None
    assert [item[0]['situation'] for item in items] == ['TRO:SituationNumber:first', 'TRO:SituationNumber:second']
    assert str(requestor)


def test_partial_and_rate_limited_results_are_visible(monkeypatch):
    raw, receive = capture(monkeypatch, [('first', 'true'), SourceError('rate-limited', 172_800)])
    _, _, pages, items, failure = bundle.read_bundle(raw, receive)
    assert len(pages) == len(items) == 1
    assert failure.code == 'rate-limited' and failure.retry_after == 172_800


def test_transport_rejects_corrupted_metadata_or_old_receipts(monkeypatch):
    raw, receive = capture(monkeypatch, [('first', 'false')])
    with pytest.raises(ValueError, match='observation time'):
        bundle.read_bundle(raw, receive + timedelta(minutes=10))
    tampered = BytesIO()
    with ZipFile(BytesIO(raw)) as incoming, ZipFile(tampered, 'w') as outgoing:
        receipt = json.loads(incoming.read('receipt.json'))
        receipt['pages'][0]['headers']['requestorid'] = 'unknown'
        outgoing.writestr('receipt.json', json.dumps(receipt))
        outgoing.writestr('page-00.xml', incoming.read('page-00.xml'))
    with pytest.raises(SourceError, match='continuity'):
        bundle.read_bundle(tampered.getvalue(), receive)


@pytest.mark.skipif(os.environ.get('APP_MODE') != 'private-local'
                    or os.environ.get('PRIVATE_TEST_PROJECT') != 'ibe160-private-tests',
                    reason='Disposable private PostgreSQL required')
def test_database_reservation_replay_and_partial_publication(monkeypatch):
    from app import auth, private_storage

    with private_storage.database() as conn, conn.transaction(force_rollback=True):
        auth.require_synthetic_accounts(conn)

        @contextmanager
        def isolated_connection():
            yield conn

        monkeypatch.setattr(private_storage, 'database', isolated_connection)
        conn.execute("UPDATE automatic_notice_feed SET attempt_at=NULL,next_request_at='-infinity'")
        started = datetime.fromisoformat(bundle.reserve())
        assert bundle.reserve() is None
        raw, when = capture(monkeypatch, [('complete', 'false')], started)
        receipt = bundle.read_bundle(raw, when)
        assert bundle.publish(receipt)['complete']
        with pytest.raises(ValueError, match='replay'):
            bundle.publish(receipt)
        conn.execute("UPDATE automatic_notice_feed SET attempt_at=clock_timestamp()-interval '6 minutes',next_request_at='-infinity'")
        started = datetime.fromisoformat(bundle.reserve())
        partial_raw, when = capture(monkeypatch, [('partial', 'true'), SourceError('rate-limited', 172_800)], started)
        assert not bundle.publish(bundle.read_bundle(partial_raw, when))['complete']
        state = conn.execute('SELECT status,generation,next_request_at FROM automatic_notice_feed').fetchone()
        assert state['status'] == 'partial' and state['generation'] == receipt[0]
        assert state['next_request_at'] > started + timedelta(days=1)
