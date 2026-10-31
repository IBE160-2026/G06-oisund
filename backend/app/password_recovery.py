"""Operator proof lifecycle and no-session redemption."""
import os
import secrets
import unicodedata
from uuid import uuid4

from . import auth
from .private_storage import database


class RecoveryError(Exception):
    pass


def host_actor():
    # Kernel UID is host context, NOT verified SSH/person attribution.
    return 'os-context:uid=' + str(os.getuid())


def resolve(username):
    name = username.strip().casefold()
    if not 1 <= len(name) <= 100 or any(unicodedata.category(c).startswith('C') for c in username):
        raise RecoveryError('Brukernavnet kan ikke bekreftes trygt.')
    with database() as conn:
        row = conn.execute('SELECT id,username FROM accounts WHERE username=%s', (name,)).fetchone()
    if not row:
        raise RecoveryError('Fant ikke en nøyaktig konto.')
    return row


def audit(conn, owner, action, result, actor=None):
    conn.execute('INSERT INTO recovery_audit(owner,actor,action,result) VALUES (%s,%s,%s,%s)',
                 (owner, actor or host_actor(), action, result))


def delivery(target, proof_id, acknowledge=False):
    """Check exactly this candidate at display/ACK; never acknowledge stale proof."""
    with database() as conn:
        confirmed(conn, target)
        row = conn.execute("SELECT EXTRACT(EPOCH FROM expires_at-clock_timestamp()) AS remaining FROM recovery_proofs WHERE owner=%s AND id=%s AND state='active' AND expires_at > clock_timestamp()", (target['id'], proof_id)).fetchone()
        if not row or row['remaining'] <= 0:
            raise RecoveryError('Koden er utløpt eller tilbakekalt/erstattet. Kontroller kontoen og utsted ny kode ved behov.')
        if acknowledge:
            audit(conn, target['id'], 'delivery', 'acknowledged')
        return float(row['remaining'])


def confirmed(conn, target):
    auth.account_lock(conn, target['id'])
    row = conn.execute('SELECT id,username FROM accounts WHERE id=%s', (target['id'],)).fetchone()
    if row != target:
        raise RecoveryError('Kontoen er endret. Avbrutt.')


def invalidate(conn, owner):
    # Caller already holds the common account gate.
    conn.execute("UPDATE recovery_proofs SET state='revoked' WHERE owner=%s AND state='active'", (owner,))


def issue(target, proof_id=None):
    limited = False
    with database() as conn:
        confirmed(conn, target)
        count = conn.execute("SELECT count(*) AS n FROM recovery_audit WHERE owner=%s AND action='issue' AND result='issued' AND occurred_at > clock_timestamp()-interval '1 hour'", (target['id'],)).fetchone()['n']
        if count >= 3:
            audit(conn, target['id'], 'issue', 'limited')
            limited = True
        else:
            code = secrets.token_urlsafe(32)
            invalidate(conn, target['id'])
            row = conn.execute("INSERT INTO recovery_proofs(id,owner,digest,created_at,expires_at) SELECT %s,%s,%s,t,t+interval '30 minutes' FROM (SELECT clock_timestamp() AS t) stamp RETURNING id,expires_at", (proof_id or uuid4(), target['id'], auth.digest(code))).fetchone()
            audit(conn, target['id'], 'issue', 'issued')
    if limited:
        raise RecoveryError('Maksimalt tre utstedelser per konto per time. Tilbakekalling er fortsatt mulig.')
    return code, row  # Context manager committed before secret can be displayed.


def revoke(target, proof_id=None, action='revoke', result='revoked'):
    with database() as conn:
        confirmed(conn, target)
        if proof_id is None:
            invalidate(conn, target['id'])
        else:
            # Failed delivery must not revoke a newer concurrent issuance.
            conn.execute("UPDATE recovery_proofs SET state='revoked' WHERE owner=%s AND id=%s AND state='active'", (target['id'], proof_id))
        audit(conn, target['id'], action, result)


def cleanup_account(conn, owner):
    conn.execute("DELETE FROM recovery_proofs WHERE id IN (SELECT id FROM recovery_proofs WHERE owner=%s AND (state <> 'active' OR expires_at <= clock_timestamp()) ORDER BY expires_at LIMIT 1000)", (owner,))
    conn.execute("DELETE FROM recovery_audit WHERE id IN (SELECT id FROM recovery_audit WHERE owner=%s AND occurred_at <= clock_timestamp()-interval '30 days' ORDER BY occurred_at LIMIT 1000)", (owner,))

# Public redemption shares S2 proof state and S1 credential replacement.
INVALID_CODE = 'Koden kunne ikke brukes. Kontroller opplysningene eller kontakt operatøren.'


def admission(name, address):
    from fastapi import HTTPException
    allowed = True
    with database() as conn:
        conn.execute('SELECT pg_advisory_xact_lock(903004)')
        conn.execute("DELETE FROM login_limits WHERE bucket LIKE 'recover:%%' AND expires_at <= clock_timestamp()")
        deadline = None
        for bucket, maximum in [('recover:global', 100), ('recover:ip:' + auth.digest(address), 20), ('recover:user:' + auth.digest(name.encode('utf-8', errors='backslashreplace').decode('utf-8')), 5)]:
            row = conn.execute("INSERT INTO login_limits VALUES (%s,1,COALESCE(%s,clock_timestamp()+interval '15 minutes')) "
                               'ON CONFLICT (bucket) DO UPDATE SET attempts=LEAST(login_limits.attempts+1,101) RETURNING attempts,expires_at',
                               (bucket, deadline)).fetchone()
            deadline = row['expires_at']
            if row['attempts'] > maximum:
                allowed = False
                break
    if not allowed:
        raise HTTPException(429, 'For mange forsøk. Prøv igjen senere.', headers={'Retry-After': '900'})


def require_no_session(request):
    from fastapi import HTTPException
    # Release any B gate before acquiring A. Opaque tokens cannot change owners
    # or become live again, so no cross-account gate recheck is necessary.
    with database() as conn:
        try:
            auth.session(conn, request)
        except HTTPException as error:
            if error.status_code == 401:
                return
            raise
    raise HTTPException(409, 'Logg ut før du gjenoppretter tilgang.')


def redeem(request, username, code, new_password, confirmation):
    import hmac
    import re
    from fastapi import HTTPException
    if not 12 <= len(new_password) <= 256 or new_password != confirmation:
        raise HTTPException(422, 'Kontroller feltene.')
    try:
        new_password.encode('utf-8')
    except UnicodeEncodeError:
        raise HTTPException(422, 'Kontroller feltene.') from None
    require_no_session(request)
    name = username.strip().casefold()
    admission(name, request.client.host)
    with database() as conn:
        account = conn.execute('SELECT id FROM accounts WHERE username=%s', (name,)).fetchone() if not any(unicodedata.category(c).startswith('C') for c in name) else None
        if account:
            auth.account_lock(conn, account['id'])
        proof = conn.execute("SELECT id,digest,expires_at FROM recovery_proofs WHERE owner=%s AND purpose='password-recovery' AND state='active'", (account['id'],)).fetchone() if account else None
        # Every admitted attempt performs one hash and a fixed-size digest compare,
        # including malformed and unknown accounts. No network-time guarantee.
        valid_shape = re.fullmatch(r'[A-Za-z0-9_-]{43}', code) is not None
        matches = hmac.compare_digest(auth.digest(code if valid_shape else 'invalid-recovery-code'), proof['digest'] if proof else '0' * 64)
        replacement = auth.password_hash(new_password)
        live = conn.execute('SELECT %s > clock_timestamp() AS live', (proof['expires_at'],)).fetchone()['live'] if proof else conn.execute('SELECT false AS live').fetchone()['live']
        if not (proof and matches and valid_shape and live):
            raise HTTPException(400, INVALID_CODE)
        conn.execute("UPDATE recovery_proofs SET state='consumed' WHERE id=%s", (proof['id'],))
        auth.replace_password(conn, account['id'], replacement, actor='recovery-proof:' + str(proof['id']))
