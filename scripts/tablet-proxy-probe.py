"""Synthetic upstream/client for an isolated Nginx probe; never connects to a DB."""
import json
import sys
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

TOKENS = {}
UPSTREAM_CALLS = 0


class Upstream(BaseHTTPRequestHandler):
    def do_GET(self):
        global UPSTREAM_CALLS
        if self.path == '/fixture-tokens':
            value = TOKENS
        elif self.path == '/probe-count':
            value = {'count': UPSTREAM_CALLS}
        else:
            UPSTREAM_CALLS += 1
            value = {'path': self.path, 'headers': dict(self.headers)}
        body = json.dumps(value).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Set-Cookie', 'probe=synthetic; Path=/; Secure; HttpOnly; SameSite=Strict')
        self.end_headers()
        self.wfile.write(body)

    do_POST = do_GET

    def log_message(self, *args):
        pass


def probe():
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args):
            return None

    opener = urllib.request.build_opener(NoRedirect)

    with urllib.request.urlopen('http://private-api:8000/fixture-tokens') as response:
        tokens = json.load(response)

    def request(path, method='GET', headers=None, authenticated=True):
        admission_header = {'Cf-Access-Jwt-Assertion': tokens['valid']} if authenticated else {}
        req = urllib.request.Request('http://gateway:8080' + path, method=method,
                                     headers={'Host': 'bus.owner-domain.no', **admission_header, **(headers or {})})
        try:
            return opener.open(req, timeout=3)
        except urllib.error.HTTPError as error:
            return error

    for attempt in range(30):
        try:
            with request('/private') as response:
                assert response.status == 200
            break
        except (OSError, AssertionError):
            if attempt == 29:
                raise
            time.sleep(0.2)
    for path, method in [('/', 'GET'), ('/private', 'GET'), ('/assets/probe.js', 'GET'),
                         ('/private-api/auth/session', 'GET'), ('/private-api/drafts', 'POST')]:
        with request(path, method, authenticated=False) as response:
            assert response.status == 403, ('missing', path, response.status)
        for name, token in tokens.items():
            if name == 'valid':
                continue
            with request(path, method, {'Cf-Access-Jwt-Assertion': token}) as response:
                assert response.status == 403, (name, path, response.status)
    with urllib.request.urlopen('http://private-api:8000/probe-count') as response:
        assert json.load(response)['count'] == 0, 'Rejected calls reached the private upstream'
    with request('/') as response:
        assert response.status == 200
    headers = {'Origin': 'https://bus.owner-domain.no', 'X-CSRF-Token': 'synthetic-proof',
               'Cookie': 'private_session=synthetic', 'X-Forwarded-Proto': 'http',
               'X-Forwarded-Host': 'evil.no', 'X-Forwarded-For': '1.2.3.4', 'Forwarded': 'host=evil.no'}
    with request('/private-api/auth/login', 'POST', headers) as response:
        assert response.status == 200
        data = json.load(response)
        assert data['path'] == '/auth/login'
        actual = {key.lower(): value for key, value in data['headers'].items()}
        assert actual['origin'] == headers['Origin']
        assert actual['x-csrf-token'] == 'synthetic-proof'
        assert actual['cookie'] == 'private_session=synthetic'
        assert actual['host'] == 'bus.owner-domain.no'
        assert not any(key in actual for key in ('forwarded', 'x-forwarded-for', 'x-forwarded-proto', 'x-forwarded-host'))
        assert response.headers['Cache-Control'] == 'no-store'
        assert "connect-src 'self'" in response.headers['Content-Security-Policy']
        assert 'Secure' in response.headers['Set-Cookie']
    for path in ['/demo', '/days', '/auth/session', '/private-api', '/index.html', '/_access_verify']:
        with request(path) as response:
            assert response.status == 404, (path, response.status)
    try:
        request('/private', headers={'Host': 'evil.no'})
    except OSError:
        pass
    else:
        raise AssertionError('Unknown host reached the application')
    print('PASS: 5 protected page/asset/API cases x ' + str(len(tokens)) + ' missing/invalid-token variants; zero rejected calls reached upstream; valid identity, Origin/CSRF/cookies, paths/Host and no-store/CSP verified')


def unavailable_probe():
    for path in ['/private', '/assets/probe.js', '/private-api/auth/session']:
        req = urllib.request.Request('http://gateway:8080' + path, headers={'Host': 'bus.owner-domain.no'})
        try:
            urllib.request.urlopen(req, timeout=8)
        except urllib.error.HTTPError as error:
            assert error.code >= 500, (path, error.code)
        else:
            raise AssertionError('Missing admission service allowed access')
    print('PASS: pages/assets/API fail closed when admission service is stopped')


if __name__ == '__main__':
    if sys.argv[1] == 'server':
        from gate import handler_for
        from test_gate import synthetic_fixture
        admission, TOKENS, *_ = synthetic_fixture()
        Thread(target=HTTPServer(('0.0.0.0', 8081), handler_for(admission)).serve_forever, daemon=True).start()
        HTTPServer(('0.0.0.0', 8000), Upstream).serve_forever()
    elif sys.argv[1] == 'down':
        unavailable_probe()
    else:
        probe()
