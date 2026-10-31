"""Real libc DNS timeout in an isolated network-none container, never host DNS.

Requires a private resolv.conf: nameserver 127.0.0.1; options timeout:5 attempts:2.
The UDP blackhole remains running throughout recovery. No getaddrinfo mocking.
"""
import json
import platform
import socket
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from gate import BoundedKeys
import jwt

assert 'nameserver 127.0.0.1' in Path('/etc/resolv.conf').read_text()
queries = []
dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dns.bind(('127.0.0.1', 53))
dns.settimeout(.2)
stop = threading.Event()
def blackhole():
    while not stop.is_set():
        try:
            data, _ = dns.recvfrom(4096)
            queries.append(time.monotonic())
        except socket.timeout:
            pass
worker = threading.Thread(target=blackhole, daemon=True)
worker.start()
keys = BoundedKeys('http://os-resolver-fixture.invalid/certs')
result = {'libc': platform.libc_ver(), 'python': platform.python_version(),
          'os_release': Path('/etc/os-release').read_text(),
          'resolv_conf': Path('/etc/resolv.conf').read_text()}
started = time.monotonic()
try:
    try:
        keys.fetch_data()
        raise AssertionError('Unexpected fetch success')
    except jwt.PyJWKClientError:
        pass
    result['caller_seconds'] = time.monotonic() - started
    assert 3 <= result['caller_seconds'] < 3.8
    frames = []
    for frame in sys._current_frames().values():
        stack = []
        while frame:
            stack.append(frame.f_code.co_name)
            frame = frame.f_back
        if 'getaddrinfo' in stack:
            frames.append(stack)
    result['workers_in_actual_getaddrinfo_after_caller_return'] = frames
    assert len(frames) == 1 and queries
    refused_at = time.monotonic()
    for _ in range(20):
        try:
            keys.fetch_data()
            raise AssertionError('Another fetch admitted')
        except jwt.PyJWKClientError:
            pass
    result['twenty_refusals_seconds'] = time.monotonic() - refused_at
    assert result['twenty_refusals_seconds'] < .5
    assert not keys.remote_slot.acquire(blocking=False)
    result['resolver_cancelled_by_caller_deadline'] = False
    while time.monotonic() - started < 18:
        if keys.remote_slot.acquire(blocking=False):
            keys.remote_slot.release()
            break
        time.sleep(.02)
    else:
        raise AssertionError('OS resolver did not return within fixture timeout')
    result['slot_released_seconds'] = time.monotonic() - started
    assert result['slot_released_seconds'] > 8
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            body = b'{"keys": []}'
            self.send_response(200)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        def log_message(self, *args):
            pass
    http = HTTPServer(('127.0.0.1', 0), Handler)
    http_worker = threading.Thread(target=http.serve_forever, daemon=True)
    http_worker.start()
    try:
        keys.uri = f'http://127.0.0.1:{http.server_port}/certs'
        assert keys.fetch_data() == {'keys': []}
        result['recovered_without_releasing_dns_blackhole_or_restart'] = True
    finally:
        http.shutdown(); http.server_close(); http_worker.join(2)
    result['dns_datagrams_dropped'] = len(queries)
    result['scope'] = 'Finite real libc timeout, not indefinite OS hang or production DNS test'
    print(json.dumps(result, indent=2))
finally:
    stop.set(); worker.join(2); dns.close()
