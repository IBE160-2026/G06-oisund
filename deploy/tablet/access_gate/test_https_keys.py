"""Synthetic TLS trust and rejection through the actual disposable worker."""
from datetime import datetime, timedelta, timezone
import ipaddress
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from gate import BoundedKeys
from test_gate import synthetic_fixture
from test_gate_http import serving


def test_https_worker_trust_validation_and_authenticated_rotation(monkeypatch, tmp_path):
    import json
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'synthetic-loopback')])
    now = datetime.now(timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
        .public_key(key.public_key()).serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=1)).not_valid_after(now + timedelta(hours=1))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(x509.SubjectAlternativeName([x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]), critical=False)
        .sign(key, hashes.SHA256()))
    cert_path, key_path = tmp_path/'cert.pem', tmp_path/'key.pem'
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(key.private_bytes(serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    admission, _, token, jwk = synthetic_fixture()
    data = [{'keys': [jwk]}]
    class Keys(BaseHTTPRequestHandler):
        def do_GET(self):
            body = json.dumps(data[0]).encode()
            self.send_response(200); self.send_header('Content-Length', str(len(body)))
            self.end_headers(); self.wfile.write(body)
        def log_message(self, *args): pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), Keys)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_path, key_path)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    with serving(server) as url:
        admission.keys = BoundedKeys(url.replace('http:', 'https:'))
        # System trust must reject our self-signed synthetic authority.
        monkeypatch.delenv('SSL_CERT_FILE', raising=False)
        monkeypatch.delenv('SSL_CERT_DIR', raising=False)
        assert not admission.allows(token())
        assert admission.keys.snapshot == {} and admission.keys.remote_slot._value == 1
        monkeypatch.setenv('SSL_CERT_FILE', str(cert_path))
        admission.keys.last_attempt -= 5
        assert admission.allows(token())
        deadline = admission.keys.snapshot['synthetic-key'][0]
        data[0] = {'keys': [{**jwk, 'kid': 'rotated'}]}
        admission.keys.last_attempt -= 5
        assert admission.allows(token(headers={'kid': 'rotated'}))
        assert admission.keys.snapshot['synthetic-key'][0] == deadline
        assert admission.allows(token())
        assert admission.keys.remote_slot._value == 1
