"""Synthetic DB/PTY evidence. Never include captured code in assertion output."""
import concurrent.futures
import fcntl
import termios
import os
import pty
import re
import select
import signal
import sys
import time
from types import SimpleNamespace

import pytest

from app import auth, password_recovery as recovery
from app.private_storage import database, migrate, cleanup
from test_private_access import synthetic_only, users, client, login, pytestmark


def target(users):
    return recovery.resolve(users[0][0])


def snapshot(owner):
    with database() as conn:
        return (conn.execute('SELECT * FROM accounts WHERE id=%s', (owner,)).fetchall(),
                conn.execute('SELECT * FROM sessions WHERE owner=%s', (owner,)).fetchall())


def test_lifecycle_digest_limit_preservation(users):
    account = target(users)
    auth.authenticate(users[0][0], users[2], 'synthetic-operator')
    before = snapshot(account['id'])
    codes = []
    for _ in range(3):
        code, proof = recovery.issue(account)
        codes.append(code)
        with database() as conn:
            active = conn.execute("SELECT * FROM recovery_proofs WHERE owner=%s AND state='active'", (account['id'],)).fetchall()
            assert len(active) == 1
            matches = active[0]['digest'] == auth.digest(code)
            assert matches, 'Recovery digest mismatch'
            assert (active[0]['expires_at'] - active[0]['created_at']).total_seconds() == 1800
            dump = str(conn.execute('SELECT * FROM recovery_proofs').fetchall()) + str(conn.execute('SELECT * FROM recovery_audit').fetchall())
            no_plaintext = not any(secret in dump for secret in codes)
            assert no_plaintext, 'Plaintext leak'
    with pytest.raises(recovery.RecoveryError):
        recovery.issue(account)
    recovery.revoke(account)
    recovery.revoke(account)
    assert snapshot(account['id']) == before
    with database() as conn:
        assert not conn.execute("SELECT 1 FROM recovery_proofs WHERE owner=%s AND state='active'", (account['id'],)).fetchone()


def test_change_invalidates_atomically_and_rollback(users, monkeypatch):
    account = target(users)
    token, _ = auth.authenticate(users[0][0], users[2], 'synthetic-change')
    recovery.issue(account)
    request = SimpleNamespace(cookies={auth.SESSION: token}, client=SimpleNamespace(host='synthetic-change'))
    before = snapshot(account['id'])
    original = recovery.invalidate
    def fail(conn, owner):
        original(conn, owner)
        conn.execute('SELECT missing_recovery_test_column')
    monkeypatch.setattr(recovery, 'invalidate', fail)
    with pytest.raises(Exception):
        auth.change_password(request, users[2], 'synthetic-new-password', 'synthetic-new-password')
    assert snapshot(account['id']) == before
    with database() as conn:
        assert conn.execute("SELECT 1 FROM recovery_proofs WHERE owner=%s AND state='active'", (account['id'],)).fetchone()
        assert not conn.execute("SELECT 1 FROM recovery_audit WHERE owner=%s AND action='change'", (account['id'],)).fetchone()
    monkeypatch.setattr(recovery, 'invalidate', original)
    auth.change_password(request, users[2], 'synthetic-new-password', 'synthetic-new-password')
    with database() as conn:
        assert not conn.execute("SELECT 1 FROM recovery_proofs WHERE owner=%s AND state='active'", (account['id'],)).fetchone()
        audit = conn.execute("SELECT actor,result FROM recovery_audit WHERE owner=%s AND action='change'", (account['id'],)).fetchone()
        assert audit == {'actor': 'app-account:' + str(account['id']), 'result': 'revoked'}


@pytest.mark.parametrize('operation', ['issue', 'revoke', 'cleanup', 'change'])
def test_real_account_gate_contention(users, operation):
    account = target(users)
    recovery.issue(account)
    token, _ = auth.authenticate(users[0][0], users[2], 'synthetic-contention')
    request = SimpleNamespace(cookies={auth.SESSION: token}, client=SimpleNamespace(host='synthetic-contention'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        with database() as blocker:
            auth.account_lock(blocker, account['id'])
            blocker_pid = blocker.info.backend_pid
            task = pool.submit({'issue': lambda: recovery.issue(account), 'revoke': lambda: recovery.revoke(account), 'cleanup': cleanup,
                                'change': lambda: auth.change_password(request, users[2], 'synthetic-new-password', 'synthetic-new-password')}[operation])
            deadline = time.monotonic() + 10
            waiting = False
            while time.monotonic() < deadline:
                with database() as observer:
                    waiting = bool(observer.execute('SELECT 1 FROM pg_stat_activity WHERE %s=ANY(pg_blocking_pids(pid))', (blocker_pid,)).fetchone())
                if waiting:
                    break
                time.sleep(.02)
            assert waiting, 'No observed PostgreSQL lock contention'
        task.result(timeout=15)
    if operation == 'change':
        with database() as conn:
            assert not conn.execute("SELECT 1 FROM recovery_proofs WHERE owner=%s AND state='active'", (account['id'],)).fetchone()


def test_cleanup_and_repeat_migration(users):
    account = target(users)
    before = snapshot(account['id'])
    recovery.issue(account)
    migrate()
    migrate()
    assert snapshot(account['id']) == before
    with database() as conn:
        conn.execute("UPDATE recovery_proofs SET created_at=statement_timestamp()-interval '2 days',expires_at=statement_timestamp()-interval '47 hours 30 minutes' WHERE owner=%s", (account['id'],))
        conn.execute("UPDATE recovery_audit SET occurred_at=clock_timestamp()-interval '31 days' WHERE owner=%s", (account['id'],))
    fresh = recovery.resolve(users[0][1])
    recovery.issue(fresh)
    with database() as conn:
        fresh_proof = conn.execute('SELECT * FROM recovery_proofs WHERE owner=%s', (fresh['id'],)).fetchall()
        fresh_audit = conn.execute('SELECT * FROM recovery_audit WHERE owner=%s', (fresh['id'],)).fetchall()
    cleanup()
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM recovery_proofs WHERE owner=%s', (account['id'],)).fetchone()
        assert not conn.execute('SELECT 1 FROM recovery_audit WHERE owner=%s', (account['id'],)).fetchone()
        assert conn.execute('SELECT * FROM recovery_proofs WHERE owner=%s', (fresh['id'],)).fetchall() == fresh_proof
        assert conn.execute('SELECT * FROM recovery_audit WHERE owner=%s', (fresh['id'],)).fetchall() == fresh_audit
    auth.authenticate(users[0][0], users[2], 'synthetic-after-migration')


def cli(name, replies, action='recovery-issue', redirect=None, interrupt=False,
        no_controlling=False, timeout_seconds=None):
    pid, terminal = pty.fork()
    if pid == 0:
        if no_controlling:
            signal.signal(signal.SIGHUP, signal.SIG_IGN)
            controlling = os.open('/dev/tty', os.O_RDWR)
            fcntl.ioctl(controlling, termios.TIOCNOTTY)
            os.close(controlling)
        if redirect is not None:
            fd = os.open('/dev/null', os.O_RDWR)
            os.dup2(fd, redirect)
        if timeout_seconds is not None:
            script = "from app import recovery_terminal as t; import sys; t.DIALOGUE_SECONDS=float(sys.argv[1]); t.run(sys.argv[2],sys.argv[3])"
            os.execv(sys.executable, [sys.executable, '-c', script, str(timeout_seconds), action, name])
        os.execv(sys.executable, [sys.executable, '-m', 'app.manage', action, name])
    captured = b''
    original_modes = termios.tcgetattr(terminal)
    deadline = time.monotonic() + 30
    reaped = False
    def remaining():
        left = deadline - time.monotonic()
        if left <= 0:
            pytest.fail('CLI overall deadline exceeded', pytrace=False)
        return min(left, 5)
    def wait_child(until):
        nonlocal reaped
        while time.monotonic() < until:
            child, status = os.waitpid(pid, os.WNOHANG)
            if child:
                reaped = True
                return status
            time.sleep(.01)
        return None
    try:
        for prompt, response in replies:
            received = b''
            while prompt not in received:
                if not select.select([terminal], [], [], remaining())[0]:
                    continue
                try:
                    received += os.read(terminal, 4096)
                except OSError:
                    pytest.fail('CLI exited before expected prompt', pytrace=False)
            captured += received
            if prompt == b'MOTTATT':
                # Delivery is after committed DB insert, independently observable.
                with database() as conn:
                    assert conn.execute("SELECT 1 FROM recovery_proofs p JOIN accounts a ON a.id=p.owner WHERE a.username=%s AND p.state='active'", (name,)).fetchone()
            if response is not None:
                os.write(terminal, response.encode() + b'\n')
        if interrupt:
            os.kill(pid, signal.SIGTERM if interrupt is True else interrupt)
        while True:
            if not select.select([terminal], [], [], remaining())[0]:
                continue
            try:
                data = os.read(terminal, 4096)
            except OSError:
                break
            if not data:
                break
            captured += data
        status = wait_child(deadline)
        if status is None:
            pytest.fail('CLI exit deadline exceeded', pytrace=False)
        restored = termios.tcgetattr(terminal) == original_modes
        assert restored, 'CLI did not restore terminal modes'
        return os.waitstatus_to_exitcode(status), captured
    finally:
        os.close(terminal)
        if not reaped:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            if wait_child(time.monotonic() + 2) is None:
                try:
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                if wait_child(time.monotonic() + 2) is None:
                    pytest.fail('CLI child could not be reaped within cleanup deadline', pytrace=False)


@pytest.mark.parametrize('redirect', [0, 1, 2])
def test_redirect_rejected(users, redirect):
    status, captured = cli(users[0][0], [], redirect=redirect)
    assert status != 0
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM recovery_proofs WHERE owner=%s', (users[1][0],)).fetchone()


@pytest.mark.parametrize('confirmation', ['', 'wrong'])
def test_cli_cancel_mismatch(users, confirmation):
    status, captured = cli(users[0][0], [(b'bekrefte', confirmation)])
    assert status != 0
    undisclosed = b'Engangskode:' not in captured
    assert undisclosed, 'Unexpected code disclosure'
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM recovery_proofs WHERE owner=%s', (users[1][0],)).fetchone()


def test_cli_own_account_display_clear_revoke(users):
    name = users[0][0]
    status, captured = cli(name, [(b'bekrefte', name), (b'TRYGT:', 'TRYGT'), (b'MOTTATT', 'MOTTATT')])
    assert status == 0
    displayed_once = captured.count(b'Engangskode:') == 1
    cleared_with_timezone = b'\x1b[2J' in captured and b'+00:00' in captured
    assert displayed_once, 'Expected exactly one code display'
    assert cleared_with_timezone, 'Expected clear and UTC expiry'
    match = re.search(rb'Engangskode: ([A-Za-z0-9_-]{43})', captured)
    matched = bool(match)
    assert matched, 'Expected one synthetic code'
    with database() as conn:
        digest = conn.execute("SELECT digest FROM recovery_proofs WHERE owner=%s AND state='active'", (users[1][0],)).fetchone()['digest']
        matches = auth.digest(match.group(1).decode()) == digest
        assert matches, 'Recovery digest mismatch'
    for _ in range(2):
        status, _ = cli(name, [(b'bekrefte', name)], action='recovery-revoke')
        assert status == 0


def test_cli_failed_handoff(users):
    name = users[0][0]
    status, captured = cli(name, [(b'bekrefte', name), (b'TRYGT:', 'TRYGT'), (b'MOTTATT', '')])
    assert status != 0
    with database() as conn:
        assert not conn.execute("SELECT 1 FROM recovery_proofs WHERE owner=%s AND state='active'", (users[1][0],)).fetchone()


def test_cli_interrupt_and_missing_controlling_terminal(users):
    name = users[0][0]
    status, captured = cli(name, [], no_controlling=True)
    undisclosed = b'Engangskode:' not in captured
    assert status != 0 and undisclosed, 'Missing-terminal path disclosed code'
    status, captured = cli(name, [(b'bekrefte', name), (b'TRYGT:', 'TRYGT'), (b'MOTTATT', None)], interrupt=True)
    assert status != 0
    with database() as conn:
        assert not conn.execute("SELECT 1 FROM recovery_proofs WHERE owner=%s AND state='active'", (users[1][0],)).fetchone()


def test_unknown_and_control_names(users):
    for name in ['synthetic-absent', 'synthetic-\x1b[2J', 'synthetic-\u202e', '\n' + users[0][0], users[0][0] + '\t']:
        with pytest.raises(recovery.RecoveryError):
            recovery.resolve(name)
    assert recovery.resolve('  ' + users[0][0].upper() + ' ') == target(users)


def test_concurrent_issue_cap_and_failure_rollback(users, monkeypatch):
    account = target(users)
    original = recovery.audit
    def broken(conn, owner, action, result):
        conn.execute('SELECT synthetic_missing_column')
    monkeypatch.setattr(recovery, 'audit', broken)
    with pytest.raises(Exception):
        recovery.issue(account)
    with database() as conn:
        assert not conn.execute('SELECT 1 FROM recovery_proofs WHERE owner=%s', (account['id'],)).fetchone()
    monkeypatch.setattr(recovery, 'audit', original)
    def attempt(_):
        try:
            recovery.issue(account)
            return True
        except recovery.RecoveryError:
            return False
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(attempt, range(4)))
    assert sum(results) == 3
    with database() as conn:
        assert conn.execute("SELECT count(*) AS n FROM recovery_proofs WHERE owner=%s AND state='active'", (account['id'],)).fetchone()['n'] == 1


@pytest.mark.parametrize('revoke_fails', [False, True])
def test_terminal_delivery_failure_safe_or_uncertain(users, monkeypatch, revoke_fails):
    from app import recovery_terminal
    name = users[0][0]
    class BrokenTerminal:
        def __enter__(self):
            return self
        def __exit__(self, *_):
            pass
        def read(self, prompt):
            return name if 'brukernavnet' in prompt else 'TRYGT'
        def begin_secret(self):
            pass
        def write(self, message):
            if 'Engangskode:' in message:
                raise OSError('synthetic delivery failure')
    monkeypatch.setattr(recovery_terminal, 'Terminal', BrokenTerminal)
    if revoke_fails:
        def fail(*args):
            raise OSError('synthetic revoke failure')
        monkeypatch.setattr(recovery, 'revoke', fail)
    with pytest.raises(SystemExit) as result:
        recovery_terminal.run('recovery-issue', name)
    assert ('USIKKER' in str(result.value)) == revoke_fails
    with database() as conn:
        active = bool(conn.execute("SELECT 1 FROM recovery_proofs WHERE owner=%s AND state='active'", (users[1][0],)).fetchone())
    assert active == revoke_fails


def test_terminal_restore_failure_after_ack_revokes_truthfully(users, monkeypatch):
    from app import recovery_terminal
    class RestoreFailure:
        def __enter__(self):
            return self
        def __exit__(self, *_):
            raise OSError('synthetic restore failure')
        def read(self, prompt):
            if 'brukernavnet' in prompt:
                return users[0][0]
            return 'MOTTATT' if 'MOTTATT' in prompt else 'TRYGT'
        def begin_secret(self):
            pass
        def clear(self):
            pass
        def write(self, message):
            pass
    monkeypatch.setattr(recovery_terminal, 'Terminal', RestoreFailure)
    with pytest.raises(SystemExit) as result:
        recovery_terminal.run('recovery-issue', users[0][0])
    assert 'tilbakekalt' in str(result.value) and 'Ingen kode vist' not in str(result.value)
    with database() as conn:
        assert not conn.execute("SELECT 1 FROM recovery_proofs WHERE owner=%s AND state='active'", (users[1][0],)).fetchone()


def test_retained_business_records_migration_and_issue(client, users):
    from test_private_drafts import save
    from test_private_workdays import prepare, confirm
    from test_account_notices import send, command, content
    assert login(client, users).status_code == 200
    assert save(client)[0].status_code == 200
    draft, _, decisions = prepare(client)
    assert confirm(client, draft, decisions).status_code == 200
    assert send(client, command(content=content())).status_code == 200
    tables = ['accounts', 'sessions', 'drafts', 'draft_operations', 'workdays', 'workday_operations', 'workday_notices', 'account_notice_operations']
    def records():
        with database() as conn:
            return {table: conn.execute('SELECT * FROM ' + table + ' ORDER BY 1').fetchall() for table in tables}
    before = records()
    # Rehearse additive first application against retained records in a rollback
    # transaction. Only the newly introduced metadata tables are replaced.
    from pathlib import Path
    with database() as conn:
        auth.require_synthetic_accounts(conn)
        conn.execute('DROP TABLE recovery_proofs, recovery_audit')
        conn.execute(Path('/app/migrations/private/015_password_recovery.sql').read_text())
        for table in tables:
            assert conn.execute('SELECT * FROM ' + table + ' ORDER BY 1').fetchall() == before[table]
        conn.rollback()
    migrate()
    migrate()
    recovery.issue(target(users))
    recovery.revoke(target(users))
    assert records() == before


@pytest.mark.parametrize('commit_lost', [False, True])
def test_issue_compensation_targets_candidate_only(users, monkeypatch, commit_lost):
    from app import recovery_terminal
    account = target(users)
    _, previous = recovery.issue(account)
    expected = previous['id']
    original_issue, original_audit = recovery.issue, recovery.audit
    class QuietTerminal:
        def __enter__(self):
            return self
        def __exit__(self, *_):
            pass
        def read(self, prompt):
            return users[0][0] if 'brukernavnet' in prompt else 'TRYGT'
        def write(self, message):
            pass
    def uncertain(target, proof_id):
        nonlocal expected
        if commit_lost:
            original_issue(target, proof_id)
            # Another operator wins before compensation begins.
            _, newer = original_issue(target)
            expected = newer['id']
            raise OSError('synthetic lost commit acknowledgement')
        def broken(conn, *args):
            conn.execute('SELECT synthetic_missing_column')
        monkeypatch.setattr(recovery, 'audit', broken)
        try:
            return original_issue(target, proof_id)
        finally:
            monkeypatch.setattr(recovery, 'audit', original_audit)
    monkeypatch.setattr(recovery_terminal, 'Terminal', QuietTerminal)
    monkeypatch.setattr(recovery, 'issue', uncertain)
    with pytest.raises(SystemExit):
        recovery_terminal.run('recovery-issue', users[0][0])
    with database() as conn:
        active = conn.execute("SELECT id FROM recovery_proofs WHERE owner=%s AND state='active'", (account['id'],)).fetchone()
        assert active['id'] == expected


def test_rolling_hour_issuance_recovers(users):
    account = target(users)
    for _ in range(3):
        recovery.issue(account)
    with pytest.raises(recovery.RecoveryError):
        recovery.issue(account)
    with database() as conn:
        conn.execute("UPDATE recovery_audit SET occurred_at=clock_timestamp()-interval '1 hour 1 second' WHERE id=(SELECT min(id) FROM recovery_audit WHERE owner=%s AND result='issued')", (account['id'],))
    recovery.issue(account)
    with pytest.raises(recovery.RecoveryError):
        recovery.issue(account)


@pytest.mark.parametrize('mode', ['before-confirmation', 'after-display', 'suspend'])
def test_cli_bounded_timeout_and_suspend(users, mode):
    name = users[0][0]
    replies = [(b'bekrefte', None)] if mode == 'before-confirmation' else [(b'bekrefte', name), (b'TRYGT:', 'TRYGT'), (b'MOTTATT', None)]
    started = time.monotonic()
    status, captured = cli(name, replies, timeout_seconds=2,
                           interrupt=signal.SIGTSTP if mode == 'suspend' else False)
    assert status != 0 and time.monotonic() - started < 10
    cleared = b'\x1b[?1049l' in captured
    assert mode == 'before-confirmation' or cleared, 'Secret screen was not cleared'
    with database() as conn:
        assert not conn.execute("SELECT 1 FROM recovery_proofs WHERE owner=%s AND state='active'", (users[1][0],)).fetchone()


class QuietDialogue:
    def __init__(self, name, on_ack=None):
        self.name, self.on_ack = name, on_ack
        self.cleared = False
    def __enter__(self):
        return self
    def __exit__(self, *_):
        self.clear()
    def read(self, prompt):
        if 'brukernavnet' in prompt:
            return self.name
        if 'MOTTATT' in prompt:
            if self.on_ack:
                self.on_ack()
            return 'MOTTATT'
        return 'TRYGT'
    def write(self, message):
        pass
    def clear(self):
        self.cleared = True
    def begin_secret(self):
        pass


@pytest.mark.parametrize('invalidation', ['revoke', 'replace', 'expire'])
def test_ack_refuses_concurrently_invalidated_candidate(users, monkeypatch, invalidation):
    from app import recovery_terminal
    account = target(users)
    def invalidate():
        if invalidation == 'revoke':
            recovery.revoke(account)
        elif invalidation == 'replace':
            recovery.issue(account)
        else:
            with database() as conn:
                recovery.confirmed(conn, account)
                conn.execute("UPDATE recovery_proofs SET created_at=statement_timestamp()-interval '30 minutes',expires_at=statement_timestamp()-interval '1 second' WHERE owner=%s", (account['id'],))
    terminal = QuietDialogue(users[0][0], invalidate)
    monkeypatch.setattr(recovery_terminal, 'Terminal', lambda: terminal)
    with pytest.raises(SystemExit) as result:
        recovery_terminal.run('recovery-issue', users[0][0])
    assert 'utsted ny kode' in str(result.value) and terminal.cleared
    with database() as conn:
        assert not conn.execute("SELECT 1 FROM recovery_audit WHERE owner=%s AND result='acknowledged'", (account['id'],)).fetchone()
        active = bool(conn.execute("SELECT 1 FROM recovery_proofs WHERE owner=%s AND state='active'", (account['id'],)).fetchone())
        assert active == (invalidation == 'replace')


def test_explicit_revoke_failure_reports_uncertainty(users, monkeypatch):
    from app import recovery_terminal
    monkeypatch.setattr(recovery_terminal, 'Terminal', lambda: QuietDialogue(users[0][0]))
    def fail(*args):
        raise OSError('synthetic ambiguous commit')
    monkeypatch.setattr(recovery, 'revoke', fail)
    with pytest.raises(SystemExit) as result:
        recovery_terminal.run('recovery-revoke', users[0][0])
    assert 'USIKKER tilbakekalling' in str(result.value) and 'recovery-revoke' in str(result.value)


def test_secret_display_deadline_never_exceeds_proof_expiry(users, monkeypatch):
    from app import recovery_terminal
    original = recovery.issue
    def short_issue(account, proof_id):
        code, proof = original(account, proof_id)
        with database() as conn:
            recovery.confirmed(conn, account)
            proof['expires_at'] = conn.execute("UPDATE recovery_proofs SET expires_at=clock_timestamp()+interval '0.15 seconds' WHERE id=%s RETURNING expires_at", (proof_id,)).fetchone()['expires_at']
        return code, proof
    terminal = QuietDialogue(users[0][0], lambda: time.sleep(3))
    monkeypatch.setattr(recovery_terminal, 'Terminal', lambda: terminal)
    monkeypatch.setattr(recovery, 'issue', short_issue)
    started = time.monotonic()
    with pytest.raises(SystemExit):
        recovery_terminal.run('recovery-issue', users[0][0])
    assert terminal.cleared and time.monotonic() - started < 2
    with database() as conn:
        assert not conn.execute("SELECT 1 FROM recovery_proofs WHERE owner=%s AND state='active'", (users[1][0],)).fetchone()
