"""Origin admission only. No database, login, cookies or token logging."""
import json
import re
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import jwt


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
        self.keys = jwt.PyJWKClient(self.issuer + '/cdn-cgi/access/certs',
                                   lifespan=300, timeout=3, cache_keys=False)

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
    server = HTTPServer(('0.0.0.0', 8081), handler_for(admission))
    server.serve_forever()
