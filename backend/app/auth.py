"""Bounded persistent authentication, opaque sessions and signed double-submit CSRF."""
import hashlib
import hmac
import os
import re
import secrets
import time
from urllib.parse import urlparse
from uuid import uuid4

from fastapi import HTTPException

from .private_storage import database

SESSION = 'private_session'
CSRF = 'private_csrf'
INVALID = 'Ugyldig brukernavn eller passord.'


def configuration():
    origin = os.environ.get('PRIVATE_ORIGIN', '')
    parsed = urlparse(origin)
    if os.environ.get('PRIVATE_HTTPS_DEPLOYMENT') == '1':
        # Explicit deployment choice; never infer transport trust from request headers.
        host = parsed.hostname or ''
        if (os.environ.get('PRIVATE_LOOPBACK_DEVELOPMENT')
                or parsed.scheme != 'https' or parsed.username or parsed.password
                or parsed.path or parsed.query or parsed.fragment
                or origin != f'https://{host}' or len(host) > 253
                or not re.fullmatch(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{0,62}', host)
                or host.endswith(('.localhost', '.local', '.invalid', '.test', '.example'))
                or host in {'localhost', 'example.com', 'example.net', 'example.org'}):
            raise RuntimeError('Explicit canonical public HTTPS origin required')
        return origin
    if os.environ.get('PRIVATE_HTTPS_DEPLOYMENT'):
        raise RuntimeError('Invalid HTTPS deployment flag')
    if (os.environ.get('PRIVATE_LOOPBACK_DEVELOPMENT') != '1'
            or parsed.scheme != 'http' or parsed.hostname not in {'127.0.0.1', 'localhost'}
            or parsed.username or parsed.password or parsed.path or parsed.query or parsed.fragment
            or origin != f'http://{parsed.hostname}:{parsed.port}'):
        raise RuntimeError('Explicit loopback development configuration required')
    return origin


def secure_cookies():
    return configuration().startswith('https://')


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def password_hash(password, salt=None):
    salt = salt or secrets.token_hex(16)
    hashed = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=2**15, r=8, p=3, maxmem=64*1024*1024)
    return salt + ':' + hashed.hex()


DUMMY = password_hash('synthetic-unused-password', '00' * 16)


def provision(username, password):
    username = username.strip().casefold()
    if not 1 <= len(username) <= 100 or not 12 <= len(password) <= 256:
        raise ValueError('Username must be 1–100 characters and password 12–256 characters')
    with database() as conn:
        row = conn.execute('INSERT INTO accounts VALUES (%s,%s,%s) RETURNING id',
                           (uuid4(), username, password_hash(password))).fetchone()
    return row['id']


def require_synthetic_accounts(conn):
    """Destructive test setup must never operate alongside provisioned real accounts."""
    if conn.execute("SELECT 1 FROM accounts WHERE username NOT LIKE 'synthetic-%%' LIMIT 1").fetchone():
        raise RuntimeError('Verification requires a disposable synthetic-only private database')


def csrf_token():
    payload = str(int(time.time())) + '.' + secrets.token_hex(24)
    with database() as conn:
        key = conn.execute('SELECT csrf_key FROM security_settings WHERE id=1').fetchone()['csrf_key']
    return payload + '.' + hmac.new(key.encode(), payload.encode(), hashlib.sha256).hexdigest()


def check_mutation(request):
    if request.headers.get('origin') != configuration():
        raise HTTPException(403, 'Forespørselen ble avvist.')
    token = request.cookies.get(CSRF, '')
    proof = request.headers.get('x-csrf-token', '')
    if not token or len(token) > 256 or not token.isascii() or not proof.isascii() or not hmac.compare_digest(token, proof):
        raise HTTPException(403, 'Forespørselen ble avvist.')
    try:
        timestamp, nonce, signature = token.split('.')
        age = time.time() - int(timestamp)
        with database() as conn:
            key = conn.execute('SELECT csrf_key FROM security_settings WHERE id=1').fetchone()['csrf_key']
        expected = hmac.new(key.encode(), f'{timestamp}.{nonce}'.encode(), hashlib.sha256).hexdigest()
        if not 0 <= age < 3600 or not hmac.compare_digest(expected, signature):
            raise ValueError()
    except (ValueError, TypeError):
        raise HTTPException(403, 'Forespørselen ble avvist.') from None


def authenticate(username, password, address):
    # One global cap bounds storage and CPU even under distributed/random-name attempts.
    # The advisory lock serializes admission across workers, without rolling back failed attempts.
    allowed = True
    with database() as conn:
        conn.execute('SELECT pg_advisory_xact_lock(903002)')
        conn.execute("UPDATE login_limits SET expires_at=g.expires_at FROM "
                     "(SELECT expires_at FROM login_limits WHERE bucket='global') g WHERE bucket LIKE 'ip:%%' OR bucket LIKE 'user:%%'")
        conn.execute('DELETE FROM login_limits WHERE expires_at <= clock_timestamp()')
        deadline = None
        for bucket, maximum in [('global', 100), ('ip:' + digest(address), 20), ('user:' + digest(username), 10)]:
            row = conn.execute("INSERT INTO login_limits VALUES (%s,1,COALESCE(%s,clock_timestamp()+interval '15 minutes')) "
                               'ON CONFLICT (bucket) DO UPDATE SET attempts=LEAST(login_limits.attempts+1,101), '
                               "expires_at=CASE WHEN login_limits.bucket='global' THEN login_limits.expires_at ELSE EXCLUDED.expires_at END RETURNING attempts,expires_at",
                               (bucket, deadline)).fetchone()
            deadline = row['expires_at']
            allowed = allowed and row['attempts'] <= maximum
            if bucket == 'global' and not allowed:
                break
    if not allowed:
        raise HTTPException(429, INVALID, headers={'Retry-After': '900'})
    with database() as conn:
        account = conn.execute('SELECT * FROM accounts WHERE username=%s', (username,)).fetchone()
        if account:
            account_lock(conn, account['id'])
            account = conn.execute('SELECT * FROM accounts WHERE id=%s', (account['id'],)).fetchone()
        stored = account['password_hash'] if account else DUMMY
        if not hmac.compare_digest(password_hash(password, stored.split(':')[0]), stored) or not account:
            raise HTTPException(401, INVALID)
        token = secrets.token_urlsafe(32)
        row = conn.execute('INSERT INTO sessions(token_hash,owner) VALUES (%s,%s) RETURNING *',
                           (digest(token), account['id'])).fetchone()
        return token, row


def session(conn, request):
    token = request.cookies.get(SESSION, '')
    if not token or len(token) > 128:
        raise HTTPException(401, 'Logg inn på nytt.')
    discovered = conn.execute('SELECT owner FROM sessions WHERE token_hash=%s', (digest(token),)).fetchone()
    if not discovered:
        raise HTTPException(401, 'Logg inn på nytt.')
    account_lock(conn, discovered['owner'])
    row = conn.execute('SELECT *, expires_at > clock_timestamp() AS live FROM sessions WHERE token_hash=%s FOR UPDATE', (digest(token),)).fetchone()
    if not row or not conn.execute('SELECT %s > clock_timestamp() AS live', (row['expires_at'],)).fetchone()['live']:
        raise HTTPException(401, 'Logg inn på nytt.')
    return row


def account_lock(conn, owner):
    """First lock in every account-authorized transaction; stable across workers."""
    key = int.from_bytes(hashlib.sha256(('private-account:' + str(owner)).encode()).digest()[:8], 'big', signed=True)
    conn.execute('SELECT pg_advisory_xact_lock(%s)', (key,))


def revoke_browser(conn, request):
    token_hash = digest(request.cookies.get(SESSION, ''))
    row = conn.execute('SELECT owner FROM sessions WHERE token_hash=%s', (token_hash,)).fetchone()
    if row:
        account_lock(conn, row['owner'])
        conn.execute('DELETE FROM sessions WHERE token_hash=%s', (token_hash,))


def change_admission(owner, address):
    # Separate committed admission: failed credentials cannot roll back attempts.
    allowed = True
    with database() as conn:
        conn.execute('SELECT pg_advisory_xact_lock(903003)')
        conn.execute("DELETE FROM login_limits WHERE bucket LIKE 'change:%%' AND expires_at <= clock_timestamp()")
        deadline = None
        for bucket, maximum in [('change:global', 100), ('change:ip:' + digest(address), 20), ('change:user:' + digest(str(owner)), 5)]:
            row = conn.execute("INSERT INTO login_limits VALUES (%s,1,COALESCE(%s,clock_timestamp()+interval '15 minutes')) "
                               'ON CONFLICT (bucket) DO UPDATE SET attempts=LEAST(login_limits.attempts+1,101) RETURNING attempts,expires_at',
                               (bucket, deadline)).fetchone()
            deadline = row['expires_at']
            if row['attempts'] > maximum:
                allowed = False
                break
    if not allowed:
        raise HTTPException(429, 'For mange forsøk. Prøv igjen senere.', headers={'Retry-After': '900'})


def change_password(request, current_password, new_password, confirmation):
    if not 1 <= len(current_password) <= 256 or not 12 <= len(new_password) <= 256 or new_password != confirmation:
        raise HTTPException(422, 'Kontroller feltene.')
    with database() as conn:
        owner = session(conn, request)['owner']
    change_admission(owner, request.client.host)
    with database() as conn:
        owner = session(conn, request)['owner']
        stored = conn.execute('SELECT password_hash FROM accounts WHERE id=%s', (owner,)).fetchone()['password_hash']
        if not hmac.compare_digest(password_hash(current_password, stored.split(':')[0]), stored):
            raise HTTPException(400, {'code': 'current_password', 'message': 'Gjeldende passord er feil.'})
        replacement = password_hash(new_password)
        session(conn, request)  # Expiry may have passed during hashing.
        conn.execute('UPDATE accounts SET password_hash=%s WHERE id=%s', (replacement, owner))
        from .password_recovery import invalidate, audit
        invalidate(conn, owner)
        audit(conn, owner, 'change', 'revoked', actor='app-account:' + str(owner))
        conn.execute('DELETE FROM sessions WHERE owner=%s', (owner,))
