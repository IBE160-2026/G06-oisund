"""Real HTTP and PostgreSQL checks; run inside the assessment API container."""
import concurrent.futures
import os
from uuid import uuid4

import httpx
import pytest

from app.storage import cleanup, database

URL = 'http://127.0.0.1:8000'


@pytest.fixture
def client():
    with httpx.Client(base_url=URL, timeout=10) as client:
        yield client


def new_request(client):
    return {'operation_id': client.post('/operations').json()['operation_id'], 'day': client.get('/fixture').json()}


def test_roundtrip_replay_and_real_postgres(client):
    body = new_request(client)
    result = client.post('/days', json=body)
    assert result.status_code == 200
    saved = result.json()
    assert saved['day'] == body['day']
    assert result.headers['cache-control'] == 'no-store'
    assert client.get('/days/' + saved['id']).json() == saved
    assert client.post('/days', json=body).json() == saved
    with database() as conn:
        rows = conn.execute('SELECT * FROM fictional_days WHERE operation_id=%s', (body['operation_id'],)).fetchall()
        assert len(rows) == 1
        assert rows[0]['owner'] == 'fictional-assessment-owner'
        assert rows[0]['payload'] == body['day']
        assert (rows[0]['expires_at'] - rows[0]['created_at']).total_seconds() == 7 * 86400
    body['day']['physical_bus'] = 'changed'
    assert client.post('/days', json=body).status_code == 409


def test_concurrent_replays(client):
    body = new_request(client)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda _: httpx.post(URL + '/days', json=body).json(), range(4)))
    assert len({r['id'] for r in results}) == 1


@pytest.mark.parametrize('mutation', ['extra', 'date', 'fictional', 'numeric-fictional', 'private', 'timezone', 'unknown-operation'])
def test_invalid_no_mutation(client, mutation):
    body = new_request(client)
    if mutation == 'extra':
        body['owner'] = 'someone'
    elif mutation == 'date':
        body['day']['service_date'] = '2026-02-30'
    elif mutation == 'fictional':
        body['day']['fictional'] = False
    elif mutation == 'numeric-fictional':
        body['day']['fictional'] = 1
    elif mutation == 'private':
        body['day']['activities'][0]['place'] = 'Non-example input'
    elif mutation == 'timezone':
        body['day']['activities'][0]['start'] = '2026-10-19T23:30:00'
    else:
        body['operation_id'] = str(uuid4())
    response = client.post('/days', json=body)
    assert response.status_code == (410 if mutation == 'unknown-operation' else 422)
    with database() as conn:
        assert conn.execute('SELECT count(*) AS n FROM fictional_days WHERE operation_id=%s', (body['operation_id'],)).fetchone()['n'] == 0


def test_expiry_no_resurrection(client):
    body = new_request(client)
    identifier = client.post('/days', json=body).json()['id']
    with database() as conn:
        conn.execute("UPDATE fictional_days SET expires_at=clock_timestamp()-interval '1 second' WHERE id=%s", (identifier,))
        conn.execute("UPDATE creation_operations SET expires_at=clock_timestamp()-interval '1 second' WHERE id=%s", (body['operation_id'],))
    assert client.get('/days/' + identifier).status_code == 410
    assert client.post('/days', json=body).status_code == 410
    cleanup()
    with database() as conn:
        assert conn.execute('SELECT count(*) AS n FROM creation_operations WHERE id=%s', (body['operation_id'],)).fetchone()['n'] == 0
        assert conn.execute('SELECT count(*) AS n FROM fictional_days WHERE id=%s', (identifier,)).fetchone()['n'] == 0
    assert client.post('/days', json=body).status_code == 410


def test_origins_and_non_assessment_denial(client, monkeypatch):
    assert client.post('/operations', headers={'Origin': 'https://untrusted.example'}).status_code == 403
    monkeypatch.setenv('APP_MODE', 'private')
    with pytest.raises(RuntimeError):
        database()
    monkeypatch.setenv('APP_MODE', 'fictional-assessment')
    monkeypatch.setenv('DATABASE_URL', os.environ['DATABASE_URL'].replace('/fictional_assessment', '/private'))
    with pytest.raises(RuntimeError):
        database()


def test_malformed_identifiers(client):
    assert client.get('/days/not-a-uuid').status_code == 422
    assert client.post('/operations', json={'private': 'unsupported'}).status_code == 422


def test_day_expiry_purges_its_operation(client):
    body = new_request(client)
    identifier = client.post('/days', json=body).json()['id']
    with database() as conn:
        conn.execute("UPDATE fictional_days SET expires_at=clock_timestamp()-interval '1 second' WHERE id=%s", (identifier,))
    assert client.post('/days', json=body).status_code == 410
    cleanup()
    assert client.post('/days', json=body).status_code == 410


@pytest.mark.parametrize('url', [
    'postgresql://fictional:example@db/fictional_assessment?host=private.example',
    'postgresql://fictional:example@db/fictional_assessment?user=private',
    'postgresql://fictional:example@db/fictional_assessment?dbname=private',
    'postgresql://fictional:example@db/fictional_assessment#override',
    'https://fictional:example@db/fictional_assessment',
])
def test_database_overrides_rejected_before_connect(monkeypatch, url):
    def forbidden_connect(*args, **kwargs):
        pytest.fail('Rejected URL must never reach psycopg.connect')
    monkeypatch.setattr('app.storage.psycopg.connect', forbidden_connect)
    monkeypatch.setenv('APP_MODE', 'fictional-assessment')
    monkeypatch.setenv('DATABASE_URL', url)
    with pytest.raises(RuntimeError):
        database()
