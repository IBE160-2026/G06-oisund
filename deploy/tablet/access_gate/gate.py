"""Origin admission only. No database, login, cookies or token logging."""
import json
import re
import socket
import threading
import time
import http.client
from urllib.parse import urlsplit
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import jwt


class BoundedKeys(jwt.PyJWKClient):
    """One nonwaiting refresher, global cooldown, immutable verified-key snapshot."""
    def __init__(self, uri):
        super().__init__(uri, lifespan=300, timeout=3, cache_keys=False)
        self.refresh_lock = threading.Lock()
        self.last_attempt = float('-inf')
        self.snapshot = {}
        self.remote_slot = threading.BoundedSemaphore(1)

    def fetch_data(self):
        # Socket timeouts alone allow indefinite trickling. Retain ownership
        # of the actual socket so the caller can interrupt headers/body at
        # the absolute deadline, without closing a buffered reader cross-thread.
        if not self.remote_slot.acquire(blocking=False):
            raise jwt.PyJWKClientError('Remote fetch already active')
        done, result = threading.Event(), {}
        ownership = threading.Lock()
        owned = {'socket': None, 'cancelled': False}
        deadline = time.monotonic() + 3
        def cancel():
            with ownership:
                owned['cancelled'] = True
                transport = owned['socket']
                owned['socket'] = None
            if transport is not None:
                try:
                    transport.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                transport.close()
        def fetch():
            connection = None
            try:
                url = urlsplit(self.uri)
                connection_type = http.client.HTTPSConnection if url.scheme == 'https' else http.client.HTTPConnection
                connection = connection_type(url.hostname, url.port, timeout=max(.001, deadline - time.monotonic()))
                connection.connect()
                transport = connection.sock
                with ownership:
                    owned['socket'] = transport
                    cancelled = owned['cancelled']
                if cancelled or time.monotonic() >= deadline:
                    raise TimeoutError()
                connection.request('GET', url.path or '/', headers={'Accept': 'application/json'})
                with connection.getresponse() as response:
                    if response.status != 200:
                        raise ValueError('Key endpoint refused')
                    payload = bytearray()
                    while True:
                        if response.isclosed():
                            break
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            raise TimeoutError()
                        transport.settimeout(remaining)
                        chunk = response.read1(min(4096, 65537 - len(payload)))
                        if not chunk:
                            break
                        payload.extend(chunk)
                        if len(payload) > 65536:
                            raise ValueError('Key response too large')
                    result['data'] = json.loads(payload)
            except Exception:
                result['failed'] = True
            finally:
                cancel()
                if connection is not None:
                    connection.close()
                self.remote_slot.release()
                done.set()
        try:
            threading.Thread(target=fetch, daemon=True).start()
        except Exception:
            self.remote_slot.release()
            raise
        if not done.wait(max(0, deadline - time.monotonic())) or time.monotonic() >= deadline or result.get('failed'):
            cancel()
            done.wait(.25)
            raise jwt.PyJWKClientError('Remote keys unavailable')
        return result['data']

    def get_signing_key_from_jwt(self, token):
        kid = jwt.get_unverified_header(token)['kid']
        def cached():
            deadline, key = self.snapshot.get(kid, (float('-inf'), None))
            # Also honor explicit cache invalidation used by qualification.
            return key if time.monotonic() < deadline and self.jwk_set_cache.get() is not None else None
        key = cached()
        if key is not None:
            return key
        if not self.refresh_lock.acquire(blocking=False):
            raise jwt.PyJWKClientError('Refresh in progress')
        try:
            key = cached()
            if key is not None:
                return key
            now = time.monotonic()
            if now - self.last_attempt < 5:
                raise jwt.PyJWKClientError('Refresh cooldown')
            self.last_attempt = now
            data = self.fetch_data()
            if not isinstance(data, dict) or not isinstance(data.get('keys'), list) or not 1 <= len(data['keys']) <= 64:
                raise jwt.PyJWKClientError('Invalid key set')
            parsed = jwt.PyJWKSet.from_dict(data)
            keys = {key.key_id: key for key in parsed.keys if key.key_type == 'RSA' and key.algorithm_name == 'RS256' and key.public_key_use in (None, 'sig')}
            if len(keys) != len(parsed.keys) or not all(isinstance(k, str) and 1 <= len(k) <= 256 for k in keys):
                raise jwt.PyJWKClientError('Invalid signing keys')
            self.jwk_set_cache.put(data)
            now = time.monotonic()
            retained = {name: entry for name, entry in self.snapshot.items() if entry[0] > now}
            # A partial rotation response must not evict previously verified
            # live keys or renew their original deadlines.
            for name, key in keys.items():
                if name not in retained:
                    retained[name] = (now + 300, key)
            if len(retained) > 128:
                raise jwt.PyJWKClientError('Key cache capacity')
            self.snapshot = retained
            if kid not in keys:
                raise jwt.PyJWKClientError('Unknown signing key')
            return keys[kid]
        finally:
            self.refresh_lock.release()


class BoundedServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    request_queue_size = 4

    def __init__(self, *args, **kwargs):
        self.slots = threading.BoundedSemaphore(4)
        super().__init__(*args, **kwargs)

    def process_request(self, request, address):
        if not self.slots.acquire(blocking=False):
            try:
                # Consume a bounded GET header before closing; otherwise an
                # unread request can turn the intended HTTP refusal into RST.
                deadline, header = time.monotonic() + .1, bytearray()
                while b'\r\n\r\n' not in header and len(header) < 16384:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        break
                    request.settimeout(remaining)
                    chunk = request.recv(min(4096, 16384 - len(header)))
                    if not chunk:
                        break
                    header.extend(chunk)
                request.settimeout(.1)
                request.sendall(b'HTTP/1.1 503 Service Unavailable\r\nContent-Length: 0\r\nCache-Control: no-store\r\nConnection: close\r\n\r\n')
            except OSError:
                pass
            finally:
                self.shutdown_request(request)
            return
        try:
            super().process_request(request, address)
        except Exception:
            self.slots.release()
            raise

    def process_request_thread(self, request, address):
        try:
            super().process_request_thread(request, address)
        finally:
            self.slots.release()


class Admission:
    def __init__(self, policy):
        if set(policy) != {'team', 'audience', 'owner_email'}:
            raise ValueError('Explicit owner policy required')
        team, audience, owner = (policy[k] for k in ('team', 'audience', 'owner_email'))
        if not all(isinstance(v, str) for v in (team, audience, owner)):
            raise ValueError('Invalid policy types')
        if (not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', team)
                or not re.fullmatch(r'[a-f0-9]{64}', audience)
                or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', owner)
                or not owner.isascii() or owner != owner.lower()
                or any(c in owner for c in ('*', ',', ';', '<', '>'))
                or owner.endswith(('.invalid', '.example', '.test'))
                or team.startswith('replace-') or audience == '0' * 64):
            raise ValueError('Replace placeholders with one approved identity')
        self.issuer = 'https://' + team + '.cloudflareaccess.com'
        self.audience, self.owner = audience, owner
        # Fixed operator-controlled URL. Never use token jku/x5u/iss as a URL.
        self.keys = BoundedKeys(self.issuer + '/cdn-cgi/access/certs')

    def allows(self, token):
        if not isinstance(token, str) or not 1 <= len(token) <= 16384:
            return False
        try:
            header = jwt.get_unverified_header(token)
            if (header.get('alg') != 'RS256' or header.get('crit')
                    or not isinstance(header.get('kid'), str)
                    or not 1 <= len(header['kid']) <= 256):
                return False
            key = self.keys.get_signing_key_from_jwt(token)
            claims = jwt.decode(token, key.key, algorithms=['RS256'],
                                issuer=self.issuer, audience=self.audience, leeway=0,
                                options={'require': ['iss', 'aud', 'exp', 'iat', 'sub', 'email', 'type']})
            return (claims['type'] == 'app' and claims['email'] == self.owner
                    and isinstance(claims['sub'], str) and bool(claims['sub'])
                    and type(claims['iat']) is int and type(claims['exp']) is int
                    and claims['exp'] > claims['iat'])
        except (jwt.PyJWTError, ValueError, TypeError, KeyError, OverflowError, OSError):
            # Fail closed; do not return exception details, headers or claims.
            return False


def handler_for(admission):
    class Handler(BaseHTTPRequestHandler):
        server_version = 'Admission'
        sys_version = ''

        def setup(self):
            super().setup()
            self.connection.settimeout(5)
            self.header_expired = threading.Event()
            self.header_deadline = time.monotonic() + 3
            def expire_headers():
                self.header_expired.set()
                try:
                    self.connection.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
            self.header_timer = threading.Timer(3, expire_headers)
            self.header_timer.daemon = True
            self.header_timer.start()

        def parse_request(self):
            try:
                parsed = super().parse_request()
                return parsed and not self.header_expired.is_set() and time.monotonic() < self.header_deadline
            finally:
                self.header_timer.cancel()

        def finish(self):
            self.header_timer.cancel()
            self.header_timer.join()
            super().finish()

        def do_GET(self):
            tokens = self.headers.get_all('Cf-Access-Jwt-Assertion', [])
            allowed = self.path == '/verify' and len(tokens) == 1 and admission.allows(tokens[0])
            self.send_response(204 if allowed else 403)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', '0')
            self.end_headers()

        def do_POST(self):
            self.send_error(403)

        def log_message(self, *args):
            pass

    return Handler


if __name__ == '__main__':
    # Mounted read-only. No alternate issuer, bypass flag or development mode.
    admission = Admission(json.loads(Path('/run/secrets/tablet_access_policy').read_text()))
    server = BoundedServer(('0.0.0.0', 8081), handler_for(admission))
    server.serve_forever()
