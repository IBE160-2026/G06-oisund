"""Synthetic fixtures only: independently specified V1 admission budgets."""
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import jwt
from test_gate import synthetic_fixture


def test_unknown_kids_share_one_five_second_refresh_window(monkeypatch):
    admission, _, token, jwk = synthetic_fixture()
    clock = [1000.0]
    monkeypatch.setattr('time.monotonic', lambda: clock[0])
    calls = []
    admission.keys.fetch_data = lambda: calls.append(clock[0]) or {'keys': [jwk]}
    assert admission.allows(token())
    for i in range(20):
        assert not admission.allows(token(headers={'kid': 'unknown-' + str(i)}))
    assert len(calls) == 1
    clock[0] += 5
    assert not admission.allows(token(headers={'kid': 'unknown'}))
    assert len(calls) == 2


def test_cached_valid_token_does_not_wait_for_stalled_unknown_refresh():
    admission, _, token, jwk = synthetic_fixture()
    assert admission.allows(token())
    admission.keys.last_attempt = time.monotonic() - 5
    entered, release = threading.Event(), threading.Event()
    def stalled():
        entered.set(); release.wait(2); return {'keys': [jwk]}
    admission.keys.fetch_data = stalled
    with ThreadPoolExecutor(max_workers=2) as pool:
        unknown = pool.submit(admission.allows, token(headers={'kid': 'unknown'}))
        try:
            assert entered.wait(1)
            start = time.monotonic()
            assert admission.allows(token())
            assert time.monotonic() - start < .5
            start = time.monotonic()
            assert not admission.allows(token(headers={'kid': 'another-unknown'}))
            assert time.monotonic() - start < .5
        finally:
            release.set()
        assert not unknown.result()


def test_expired_cache_and_rotation_recover_after_cooldown(monkeypatch):
    admission, _, token, jwk = synthetic_fixture()
    clock = [1000.0]
    monkeypatch.setattr('time.monotonic', lambda: clock[0])
    assert admission.allows(token())
    clock[0] += 300
    def unavailable():
        raise jwt.PyJWKClientError('private synthetic failure text')
    admission.keys.fetch_data = unavailable
    assert not admission.allows(token())
    rotated = {**jwk, 'kid': 'rotation'}
    admission.keys.fetch_data = lambda: {'keys': [rotated]}
    assert not admission.allows(token(headers={'kid': 'rotation'}))
    clock[0] += 5
    assert admission.allows(token(headers={'kid': 'rotation'}))


def test_unknown_refresh_does_not_evict_or_renew_live_verified_keys(monkeypatch):
    admission, _, token, jwk = synthetic_fixture()
    clock = [1000.0]
    monkeypatch.setattr('time.monotonic', lambda: clock[0])
    assert admission.allows(token())
    for payload in [{'keys': []}, {'keys': [{**jwk, 'kid': 'rotation'}]}, {'keys': [None]}]:
        clock[0] += 5
        admission.keys.fetch_data = lambda: payload
        assert not admission.allows(token(headers={'kid': 'unknown'}))
        assert admission.allows(token())
    clock[0] = 1300
    admission.keys.fetch_data = lambda: {'keys': [{**jwk, 'kid': 'rotation'}]}
    assert not admission.allows(token())

