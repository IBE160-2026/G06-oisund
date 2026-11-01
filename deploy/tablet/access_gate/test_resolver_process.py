"""Only child-local DNS fault injection; no system or production DNS changes."""
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import jwt
import pytest

from gate import BoundedKeys
from test_gate import synthetic_fixture
from test_gate_http import serving
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def inject_stuck_resolver(monkeypatch, tmp_path):
    """Launch real workers, replacing getaddrinfo only inside each test child.

    A marker proves the hang reached DNS, and is never released. SIGTERM is
    ignored on POSIX so passing requires an actual kill, not cooperative exit.
    """
    real_popen = subprocess.Popen
    children = []
    enabled = [True]
    marker = tmp_path / 'resolver-entered'
    fixture = tmp_path / 'stuck.py'
    fixture.write_text(
        "import runpy, socket, sys, time, signal\n"
        "from pathlib import Path\n"
        "if hasattr(signal, 'SIGTERM'): signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
        "def stuck(*args, **kwargs):\n"
        f"    Path({str(marker)!r}).write_text('entered')\n"
        "    while True: time.sleep(3600)\n"
        "socket.getaddrinfo = stuck\n"
        "target = sys.argv.pop(1)\n"
        "runpy.run_path(target, run_name='__main__')\n"
    )
    def launch(args, **kwargs):
        if enabled[0]:
            args = [*args[:2], str(fixture), *args[2:]]
        child = real_popen(args, **kwargs)
        children.append(child)
        return child
    monkeypatch.setattr(subprocess, 'Popen', launch)
    return children, enabled, marker


def test_repeated_permanent_dns_hangs_reap_and_recover(monkeypatch, tmp_path):
    children, enabled, marker = inject_stuck_resolver(monkeypatch, tmp_path)
    keys = BoundedKeys('http://resolver-fixture.invalid/certs')
    threads_before = {t.ident for t in threading.enumerate()}
    fd_before = len(os.listdir('/proc/self/fd')) if Path('/proc/self/fd').exists() else None
    elapsed = []
    for _ in range(3):
        marker.unlink(missing_ok=True)
        start = time.monotonic()
        with ThreadPoolExecutor(max_workers=1) as pool:
            request = pool.submit(keys.fetch_data)
            deadline = start + 2
            while not marker.exists() and time.monotonic() < deadline:
                time.sleep(.01)
            assert marker.exists(), 'The fixture must actually reach getaddrinfo'
            with ThreadPoolExecutor(max_workers=12) as callers:
                rejected = list(callers.map(lambda _: refused(keys), range(24)))
            assert all(rejected)
            assert len([p for p in children if p.poll() is None]) == 1
            with pytest.raises(jwt.PyJWKClientError):
                request.result(timeout=4)
        assert 2.5 <= time.monotonic() - start < 3.75
        elapsed.append(round(time.monotonic() - start, 3))
        assert all(p.poll() is not None for p in children)
        assert keys.remote_slot._value == 1
        assert keys.snapshot == {}
    assert {t.ident for t in threading.enumerate()} == threads_before
    if fd_before is not None:
        assert len(os.listdir('/proc/self/fd')) == fd_before
    enabled[0] = False
    class Healthy(BaseHTTPRequestHandler):
        def do_GET(self):
            body = b'{"keys": []}'
            self.send_response(200)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        def log_message(self, *args): pass
    with serving(ThreadingHTTPServer(('127.0.0.1', 0), Healthy)) as remote:
        keys.uri = remote
        assert keys.fetch_data() == {'keys': []}
    assert all(p.poll() is not None for p in children)
    print(json.dumps({'dns_hang_seconds': elapsed, 'concurrent_refusals': 72,
        'children_reaped': len(children), 'new_threads': 0,
        'fd_count_before': fd_before, 'fd_count_after': len(os.listdir('/proc/self/fd')) if fd_before is not None else None,
        'recovery': True}))


def refused(keys):
    try:
        keys.fetch_data()
    except jwt.PyJWKClientError:
        return True
    return False


def test_dns_failure_never_authorizes_and_rotation_keeps_deadlines(monkeypatch, tmp_path):
    admission, _, token, jwk = synthetic_fixture()
    admission.keys = BoundedKeys('http://resolver-fixture.invalid/certs')
    children, enabled, marker = inject_stuck_resolver(monkeypatch, tmp_path)
    assert not admission.allows(token())
    assert marker.exists() and all(p.poll() is not None for p in children)
    assert admission.keys.snapshot == {}
    enabled[0] = False
    data = [{'keys': [jwk]}]
    class Healthy(BaseHTTPRequestHandler):
        def do_GET(self):
            body = json.dumps(data[0]).encode()
            self.send_response(200); self.send_header('Content-Length', str(len(body)))
            self.end_headers(); self.wfile.write(body)
        def log_message(self, *args): pass
    with serving(ThreadingHTTPServer(('127.0.0.1', 0), Healthy)) as remote:
        admission.keys.uri = remote
        assert not admission.allows(token())  # Five-second failure cooldown.
        admission.keys.last_attempt -= 5
        assert admission.allows(token())
        deadline = admission.keys.snapshot['synthetic-key'][0]
        data[0] = {'keys': [{**jwk, 'kid': 'rotated'}]}
        admission.keys.last_attempt -= 5
        assert admission.allows(token(headers={'kid': 'rotated'}))
        assert admission.keys.snapshot['synthetic-key'][0] == deadline
        assert admission.allows(token())
        assert not admission.allows(token({'exp': int(time.time()) - 1}))
    assert all(p.poll() is not None for p in children)


def test_spawn_failure_releases_slot(monkeypatch):
    keys = BoundedKeys('http://resolver-fixture.invalid')
    def unavailable(*args, **kwargs):
        raise OSError('synthetic resource limit')
    monkeypatch.setattr(subprocess, 'Popen', unavailable)
    assert refused(keys)
    assert keys.remote_slot._value == 1


def test_delayed_reap_is_reconciled_before_next_spawn(monkeypatch):
    finished, launches = [False], []
    class Delayed:
        returncode = None
        def poll(self): return -9 if finished[0] else None
        def kill(self): pass
        def wait(self, timeout):
            if not finished[0]: raise subprocess.TimeoutExpired('synthetic', timeout)
            return -9
    class Success:
        returncode = 0
        def poll(self): return 0
        def wait(self, timeout): return 0
    def launch(args, **kwargs):
        launches.append(1)
        if len(launches) == 1: return Delayed()
        kwargs['stdout'].write(b'{"keys": []}')
        return Success()
    monkeypatch.setattr(subprocess, 'Popen', launch)
    keys = BoundedKeys('http://resolver-fixture.invalid')
    assert refused(keys)
    assert keys.remote_slot._value == 0
    assert refused(keys) and len(launches) == 1
    finished[0] = True
    assert keys.fetch_data() == {'keys': []}
    assert len(launches) == 2 and keys.pending_process is None
    assert keys.remote_slot._value == 1


@pytest.mark.parametrize('body,status', [(b'x' * 65537, 200), (b'{bad', 200), (b'{}', 503)])
def test_bad_transport_responses_fail_closed_and_release(body, status):
    class Invalid(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(status); self.send_header('Content-Length', str(len(body)))
            self.end_headers(); self.wfile.write(body)
        def log_message(self, *args): pass
    with serving(ThreadingHTTPServer(('127.0.0.1', 0), Invalid)) as remote:
        keys = BoundedKeys(remote)
        assert refused(keys)
        assert keys.snapshot == {}
        assert keys.remote_slot._value == 1


def test_key_set_and_retained_cache_caps_are_preserved():
    admission, _, token, jwk = synthetic_fixture()
    data = [{'keys': [{**jwk, 'kid': str(i)} for i in range(65)]}]
    admission.keys.fetch_data = lambda: data[0]
    assert not admission.allows(token(headers={'kid': '0'}))
    assert admission.keys.snapshot == {}
    for batch in range(2):
        data[0] = {'keys': [{**jwk, 'kid': str(batch * 64 + i)} for i in range(64)]}
        admission.keys.last_attempt -= 5
        assert admission.allows(token(headers={'kid': str(batch * 64)}))
    assert len(admission.keys.snapshot) == 128
    original = dict(admission.keys.snapshot)
    data[0] = {'keys': [{**jwk, 'kid': 'overflow'}]}
    admission.keys.last_attempt -= 5
    assert not admission.allows(token(headers={'kid': 'overflow'}))
    assert admission.keys.snapshot == original
