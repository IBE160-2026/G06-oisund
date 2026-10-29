"""Loopback synthetic HTTP only; no Cloudflare/MFA/device observations."""
import json
import threading
import time
import socket
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import jwt
import pytest

from gate import BoundedKeys, BoundedServer, handler_for
from test_gate import synthetic_fixture


@contextmanager
def serving(server):
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        yield 'http://127.0.0.1:' + str(server.server_port)
    finally:
        server.shutdown(); server.server_close(); worker.join(2)


def fetch(url, token, cookie=None):
    headers = {'Cf-Access-Jwt-Assertion': token}
    if cookie is not None:
        headers['Cookie'] = cookie
    try:
        with urllib.request.urlopen(urllib.request.Request(url + '/verify', headers=headers), timeout=4) as response:
            return response.status, response.headers
    except urllib.error.HTTPError as error:
        return error.code, error.headers


def test_http_signed_variants_are_payload_free_and_no_store():
    admission, tokens, *_ = synthetic_fixture()
    with serving(BoundedServer(('127.0.0.1', 0), handler_for(admission))) as url:
        status, headers = fetch(url, tokens['valid'], 'CF_Authorization=synthetic-edge; private_session=synthetic-session; tracking=discard; private_csrf=synthetic-proof')
        assert status == 204
        assert headers.get('X-Private-Cookie') is None
        assert headers['Cache-Control'] == 'no-store'
        for name, token in tokens.items():
            if name != 'valid':
                assert fetch(url, token)[0] == 403, name


def test_four_handlers_and_immediate_overload_without_queue():
    entered, release = threading.Event(), threading.Event()
    lock, active = threading.Lock(), [0, 0]
    class BlockingAdmission:
        def allows(self, token):
            with lock:
                active[0] += 1; active[1] = max(active)
                if active[0] == 4:
                    entered.set()
            try:
                release.wait(3)
                return False
            finally:
                with lock:
                    active[0] -= 1
    with serving(BoundedServer(('127.0.0.1', 0), handler_for(BlockingAdmission()))) as url:
        with ThreadPoolExecutor(max_workers=4) as pool:
            requests = [pool.submit(fetch, url, 'synthetic') for _ in range(4)]
            try:
                assert entered.wait(2)
                start = time.monotonic()
                assert fetch(url, 'synthetic')[0] == 503
                assert time.monotonic() - start < .5
                assert active[1] == 4
            finally:
                release.set()
            assert all(request.result()[0] == 403 for request in requests)


def test_header_timer_has_exited_before_handler_slot_release(monkeypatch):
    admission, tokens, *_ = synthetic_fixture()
    timers, released_with_live_timer = [], []
    original_timer = threading.Timer
    class SlowExitingTimer(original_timer):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            timers.append(self)
        def run(self):
            super().run()
            # Cancellation wakes the timer, but its thread has not exited yet.
            time.sleep(.02)
    monkeypatch.setattr(threading, 'Timer', SlowExitingTimer)
    server = BoundedServer(('127.0.0.1', 0), handler_for(admission))
    release_slot = server.slots.release
    def observed_release():
        released_with_live_timer.append(any(timer.is_alive() for timer in timers))
        release_slot()
    monkeypatch.setattr(server.slots, 'release', observed_release)
    with serving(server) as url:
        for _ in range(10):
            assert fetch(url, tokens['valid'])[0] == 204
            deadline = time.monotonic() + 1
            while server.slots._value != 4 and time.monotonic() < deadline:
                time.sleep(.005)
            assert server.slots._value == 4
        assert len(released_with_live_timer) == 10
        assert not any(released_with_live_timer)


def test_slow_header_trickles_release_four_slots_at_absolute_deadline():
    admission, tokens, *_ = synthetic_fixture()
    server = BoundedServer(('127.0.0.1', 0), handler_for(admission))
    stopped = threading.Event()
    sockets, writers = [], []
    def trickle(connection):
        try:
            connection.sendall(b'GET /verify HTTP/1.1\r\nHost: synthetic\r\nX-Slow: ')
            while not stopped.wait(.1):
                connection.sendall(b'x')
        except OSError:
            pass
    with serving(server) as url:
        try:
            started = time.monotonic()
            for _ in range(4):
                connection = socket.create_connection(('127.0.0.1', server.server_port), timeout=1)
                sockets.append(connection)
                writer = threading.Thread(target=trickle, args=(connection,), daemon=True)
                writers.append(writer); writer.start()
            # All four slow clients must consume admission capacity initially.
            deadline = time.monotonic() + 1
            while server.slots._value != 0 and time.monotonic() < deadline:
                time.sleep(.01)
            assert server.slots._value == 0
            assert fetch(url, tokens['valid'])[0] == 503
            # The clients keep sending until capacity has recovered. No fixture
            # release or service restart may free these slots for the assertion.
            deadline = started + 3.5
            while server.slots._value != 4 and time.monotonic() < deadline:
                time.sleep(.01)
            assert server.slots._value == 4
            assert time.monotonic() - started < 3.5
            assert fetch(url, tokens['valid'])[0] == 204
        finally:
            stopped.set()
            for connection in sockets:
                connection.close()
            for writer in writers:
                writer.join(1)


def test_actual_stalled_jwks_deadline_cached_latency_and_rotation():
    admission, _, token, jwk = synthetic_fixture()
    entered, release = threading.Event(), threading.Event()
    calls, stalled, data = [0], [False], [jwk]
    class JWKS(BaseHTTPRequestHandler):
        def do_GET(self):
            calls[0] += 1
            if stalled[0]:
                entered.set(); release.wait(5)
            body = json.dumps({'keys': data}).encode()
            try:
                self.send_response(200); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
            except OSError:
                pass
        def log_message(self, *args):
            pass
    with serving(ThreadingHTTPServer(('127.0.0.1', 0), JWKS)) as remote:
        admission.keys = BoundedKeys(remote + '/certs')
        assert admission.allows(token())
        admission.keys.last_attempt = time.monotonic() - 5
        stalled[0] = True
        with ThreadPoolExecutor(max_workers=1) as pool:
            start = time.monotonic()
            unknown = pool.submit(admission.allows, token(headers={'kid': 'unknown'}))
            try:
                assert entered.wait(1)
                cached_start = time.monotonic()
                assert admission.allows(token())
                assert time.monotonic() - cached_start < .5
                for _ in range(10):
                    assert not admission.allows(token(headers={'kid': 'other'}))
                assert not unknown.result(timeout=4)
                assert time.monotonic() - start < 4
                assert calls[0] == 2
            finally:
                release.set()
        stalled[0] = False
        # The timed-out transport must finish before a new transport can start.
        assert admission.keys.remote_slot.acquire(timeout=2)
        admission.keys.remote_slot.release()
        admission.keys.last_attempt = time.monotonic() - 5
        data[:] = [{**jwk, 'kid': 'rotated'}]
        assert admission.allows(token(headers={'kid': 'rotated'}))
        # A rotated set does not evict a still-live known key early.
        assert admission.allows(token())



def test_trickled_response_releases_transport_slot_at_absolute_deadline():
    # Independent regression originally reproduced by root before this fix.
    admission, _, token, jwk = synthetic_fixture()
    release, healthy = threading.Event(), threading.Event()
    class Trickle(BaseHTTPRequestHandler):
        def do_GET(self):
            if healthy.is_set():
                body = json.dumps({'keys': [jwk]}).encode()
                self.send_response(200); self.send_header('Content-Length', str(len(body)))
                self.end_headers(); self.wfile.write(body)
                return
            self.send_response(200)
            self.send_header('Content-Length', '1000')
            self.end_headers()
            try:
                while not release.wait(.2):
                    self.wfile.write(b' '); self.wfile.flush()
            except OSError:
                pass
        def log_message(self, *args):
            pass
    with serving(ThreadingHTTPServer(('127.0.0.1', 0), Trickle)) as remote:
        keys = BoundedKeys(remote)
        try:
            started = time.monotonic()
            with pytest.raises(jwt.PyJWKClientError):
                keys.fetch_data()
            assert time.monotonic() - started < 4
            free = keys.remote_slot.acquire(timeout=.5)
            if free:
                keys.remote_slot.release()
            assert free, 'Caller deadline returned but trickling response still monopolizes the only transport slot'
            assert keys.snapshot == {}, 'A failed or late response published key authority'
            # Recover while the old fixture would still trickle. It has not
            # been released manually; cancellation must have freed transport.
            healthy.set()
            admission.keys = keys
            assert admission.allows(token())
        finally:
            release.set()
