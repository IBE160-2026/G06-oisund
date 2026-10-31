"""Privileged operator lifecycle. No public redemption interface in S2."""
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
