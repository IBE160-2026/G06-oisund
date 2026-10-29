"""Pure unit cleanup failure/recovery; never connects to a database."""
import asyncio
import logging
import pytest
import psycopg
from contextlib import contextmanager
from app import private_main


def test_hourly_cleanup_continues_after_failure_and_reports_recovery(monkeypatch, caplog):
    waits, calls = [], []
    async def tick(seconds):
        waits.append(seconds)
        if len(waits) > 2:
            raise asyncio.CancelledError()
    def cleanup():
        calls.append(True)
        if len(calls) == 1:
            raise psycopg.OperationalError('SQL secret payload')
    async def worker(function):
        return function()
    monkeypatch.setattr(private_main.asyncio, 'sleep', tick)
    monkeypatch.setattr(private_main.asyncio, 'to_thread', worker)
    monkeypatch.setattr(private_main, 'cleanup', cleanup)
    with caplog.at_level(logging.INFO, logger='private.maintenance'):
        with pytest.raises(asyncio.CancelledError):
            private_main.maintenance().send(None)
    assert waits == [3600, 3600, 3600]
    assert len(calls) == 2
    assert [record.message for record in caplog.records] == ['private_cleanup_failed', 'private_cleanup_ok']
    assert 'SQL secret payload' not in caplog.text


def test_cleanup_failure_and_recovery_are_payload_free(monkeypatch, caplog):
    monkeypatch.setattr(private_main, 'cleanup', lambda: (_ for _ in ()).throw(psycopg.OperationalError('SQL secret payload')))
    with caplog.at_level(logging.INFO, logger='private.maintenance'):
        assert private_main.run_cleanup() is False
        assert private_main.cleanup_health() == {'status': 'failed', 'consecutive_failures': 1}
        monkeypatch.setattr(private_main, 'cleanup', lambda: None)
        assert private_main.run_cleanup() is True
    assert private_main.cleanup_health() == {'status': 'ok', 'consecutive_failures': 0}
    assert [record.message for record in caplog.records] == ['private_cleanup_failed', 'private_cleanup_ok']
    assert 'SQL secret payload' not in caplog.text


def test_cleanup_failure_counter_is_bounded(monkeypatch):
    monkeypatch.setattr(private_main, 'cleanup', lambda: (_ for _ in ()).throw(psycopg.OperationalError('secret')))
    for _ in range(105):
        private_main.run_cleanup()
    assert private_main.cleanup_health() == {'status': 'failed', 'consecutive_failures': 99}
    monkeypatch.setattr(private_main, 'cleanup', lambda: None)
    private_main.run_cleanup()


def test_failed_cleanup_does_not_relabel_database_connectivity(monkeypatch):
    queries = []
    class Connection:
        def execute(self, query):
            queries.append(query)
    @contextmanager
    def database():
        yield Connection()
    monkeypatch.setattr(private_main, 'database', database)
    monkeypatch.setattr(private_main, 'cleanup', lambda: (_ for _ in ()).throw(psycopg.OperationalError('secret')))
    private_main.run_cleanup()
    value = private_main.health()
    assert queries == ['SELECT 1']
    assert value['status'] == 'ok' and value['mode'] == 'private-local'
    assert value['cleanup'] == {'status': 'failed', 'consecutive_failures': 1}
    monkeypatch.setattr(private_main, 'cleanup', lambda: None)
    private_main.run_cleanup()
