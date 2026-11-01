"""Opt-in libc resolver test: requires a disposable network=none container.

Docker --dns 127.0.0.1 --dns-option timeout:30 --dns-option attempts:5,
O5_LIBC_DNS=1. Never run on a host or ordinary application container.
"""
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from gate import BoundedKeys
from test_gate import synthetic_fixture
from test_gate_http import serving


@pytest.mark.skipif(os.environ.get('O5_LIBC_DNS') != '1', reason='disposable DNS namespace only')
def test_real_libc_dns_blackhole_is_killed_and_resolution_recovers():
    assert Path('/.dockerenv').is_file(), 'Disposable Docker container required'
    assert {p.name for p in Path('/sys/class/net').iterdir()} == {'lo'}, 'network=none required'
    assert 'nameserver 127.0.0.1' in Path('/etc/resolv.conf').read_text()
    assert 'timeout:30' in Path('/etc/resolv.conf').read_text()
    ready, received, stop = threading.Event(), threading.Event(), threading.Event()
    dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns.bind(('127.0.0.1', 53)); dns.settimeout(.1)
    requests = []
    def serve_dns():
        while not stop.is_set():
            try:
                query, source = dns.recvfrom(4096)
            except socket.timeout:
                continue
            requests.append(time.monotonic()); received.set()
            if not ready.is_set():
                continue  # Deliberate silence within this disposable namespace.
            offset = 12
            while query[offset]:
                offset += query[offset] + 1
            offset += 1
            qtype, _ = struct.unpack('!HH', query[offset:offset+4])
            question = query[12:offset+4]
            answer = (b'\xc0\x0c' + struct.pack('!HHIH', 1, 1, 0, 4) + socket.inet_aton('127.0.0.1')) if qtype == 1 else b''
            dns.sendto(query[:2] + struct.pack('!HHHHH', 0x8180, 1, bool(answer), 0, 0) + question + answer, source)
    thread = threading.Thread(target=serve_dns)
    thread.start()
    control = None
    try:
        # Positive control proves libc itself stays blocked beyond our budget.
        control = subprocess.Popen([sys.executable, '-I', '-c',
            "import socket; socket.getaddrinfo('resolver-fixture.test', 80)"],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        assert received.wait(2)
        with pytest.raises(subprocess.TimeoutExpired):
            control.wait(timeout=3.5)
        control.kill(); control.wait(timeout=.25)
        admission, _, token, jwk = synthetic_fixture()
        class Keys(BaseHTTPRequestHandler):
            def do_GET(self):
                body = json.dumps({'keys': [jwk]}).encode()
                self.send_response(200); self.send_header('Content-Length', str(len(body)))
                self.end_headers(); self.wfile.write(body)
            def log_message(self, *args): pass
        with serving(ThreadingHTTPServer(('127.0.0.1', 0), Keys)) as remote:
            admission.keys = BoundedKeys(remote.replace('127.0.0.1', 'resolver-fixture.test'))
            start = time.monotonic()
            assert not admission.allows(token())
            duration = time.monotonic() - start
            assert 2.5 < duration < 3.75
            assert admission.keys.remote_slot._value == 1
            assert admission.keys.snapshot == {}
            assert not Path('/proc/self/task/' + str(os.getpid()) + '/children').read_text().strip()
            ready.set()
            admission.keys.last_attempt -= 5
            assert admission.allows(token())
            assert not Path('/proc/self/task/' + str(os.getpid()) + '/children').read_text().strip()
            print(json.dumps({'libc_control_still_blocked_after_seconds': 3.5,
                'gate_refusal_seconds': round(duration, 3), 'dns_datagrams': len(requests),
                'children_remaining': 0, 'dns_recovery_authenticated': True}))
    finally:
        if control is not None and control.poll() is None:
            control.kill(); control.wait(timeout=.25)
        stop.set(); thread.join(1); dns.close()
        assert not thread.is_alive()
