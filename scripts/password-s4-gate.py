"""Disposable S4 admission only: real handler, generated signing key, no IdP I/O."""
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from gate import BoundedServer, handler_for
from test_gate import synthetic_fixture

admission, tokens, sign, _ = synthetic_fixture()
class Fixture(BaseHTTPRequestHandler):
    def do_GET(self):
        # Same generated key, fresh timestamps; no provider/network lookup.
        now = int(time.time())
        body = json.dumps({**tokens, 'valid': sign({'iat': now-10, 'exp': now+300})}).encode()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *_):
        pass
Thread(target=BoundedServer(('0.0.0.0', 8081), handler_for(admission)).serve_forever, daemon=True).start()
HTTPServer(('0.0.0.0', 8082), Fixture).serve_forever()
