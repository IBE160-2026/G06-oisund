"""Synthetic pre-socket resolver stall. Does not emulate OS DNS cancellation."""
import json
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest.mock import patch
import jwt
from gate import BoundedKeys

entered, release = threading.Event(), threading.Event()
calls = []
real_resolver = socket.getaddrinfo
def stalled(host, *args, **kwargs):
    if host == 'resolver-fixture.invalid':
        calls.append(host)
        entered.set()
        if not release.wait(10):
            raise AssertionError('fixture release missing')
        raise socket.gaierror(socket.EAI_AGAIN, 'synthetic resolver failure')
    return real_resolver(host, *args, **kwargs)

class Keys(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'{"keys": []}'
        self.send_response(200)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *args):
        pass

keys = BoundedKeys('http://resolver-fixture.invalid/certs')
result = {'fixture': 'Python getaddrinfo barrier, Windows host; no system DNS change'}
with patch('socket.getaddrinfo', stalled):
    try:
        started = time.monotonic()
        try:
            keys.fetch_data()
            raise AssertionError('stalled fetch accepted')
        except jwt.PyJWKClientError:
            pass
        result['first_caller_seconds'] = time.monotonic() - started
        assert entered.is_set() and result['first_caller_seconds'] < 3.75
        started = time.monotonic()
        for _ in range(20):
            try:
                keys.fetch_data()
                raise AssertionError('second worker accepted')
            except jwt.PyJWKClientError:
                pass
        result['twenty_refused_callers_seconds'] = time.monotonic() - started
        result['resolver_entries_while_stalled'] = len(calls)
        assert len(calls) == 1 and result['twenty_refused_callers_seconds'] < .5
        free = keys.remote_slot.acquire(blocking=False)
        if free:
            keys.remote_slot.release()
        result['slot_remains_occupied_until_resolver_returns'] = not free
        assert not free
    finally:
        release.set()
    until = time.monotonic() + 2
    while time.monotonic() < until:
        if keys.remote_slot.acquire(blocking=False):
            keys.remote_slot.release()
            break
        time.sleep(.01)
    else:
        raise AssertionError('worker failed to release after resolver returned')
    server = HTTPServer(('127.0.0.1', 0), Keys)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        keys.uri = f'http://127.0.0.1:{server.server_port}/certs'
        assert keys.fetch_data() == {'keys': []}
        result['transport_recovers_after_explicit_resolver_release'] = True
    finally:
        server.shutdown()
        server.server_close()
        thread.join(2)
result['bounded_fixture_passed'] = True
result['actual_os_resolver_cancellation_verified'] = False
print(json.dumps(result, indent=2))
