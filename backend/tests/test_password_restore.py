"""Real synthetic PostgreSQL checks for the offline all-account transaction."""
from pathlib import Path

import pytest
from app import auth, restore, password_recovery as recovery
from app.private_storage import database
from test_private_access import users, synthetic_only, pytestmark
from test_password_recovery import anonymous, outcome


def test_inspect_accepts_only_known_migration_prefixes(users, tmp_path, monkeypatch):
    original = sorted((Path(restore.__file__).parent.parent / 'migrations/private').glob('*.sql'))
    for path in original:
        destination = tmp_path / 'migrations/private' / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(path.read_bytes())
    appended = {f'{len(original) + offset:03d}_synthetic_v2.sql': f'CREATE TABLE synthetic_v2_{offset} (id integer)'
                for offset in (1, 2)}
    for name, statement in appended.items():
        (tmp_path / 'migrations/private' / name).write_text(statement, encoding='utf-8')
    monkeypatch.setattr(restore, 'Path', lambda _: tmp_path / 'app/restore.py')
    with database() as conn:
        with conn.transaction(force_rollback=True):
            current = restore.inspect(conn)
            assert current['schema'] == len(original)
            notices_identity = ', automatic_notice_identities' if '020_automatic_notice_identity.sql' in {path.name for path in original} else ''
            if len(original) >= 18:
                conn.execute('DROP TABLE workday_position_anchor_operations, workday_position_anchors, '
                             'workday_route_references, draft_route_decisions, automatic_notice_review_operations, '
                             'automatic_notice_reviews, automatic_notice_sources, automatic_notice_feed' + notices_identity)
                conn.execute('ALTER TABLE workdays DROP CONSTRAINT automatic_notice_workday_parent')
                conn.execute('ALTER TABLE workday_operations DROP COLUMN route_revision')
                conn.execute("DELETE FROM private_migrations WHERE name >= '016'")
                older = restore.inspect(conn)
                assert older['schema'] == 15 and older['business'] == current['business']
                for path in original[15:]:
                    conn.execute(path.read_text(encoding='utf-8'))
                    conn.execute('INSERT INTO private_migrations VALUES (%s)', (path.name,))
                assert restore.inspect(conn) == current
                conn.execute('DROP TABLE workday_position_anchor_operations, workday_position_anchors, '
                             'workday_route_references, draft_route_decisions, automatic_notice_review_operations, '
                             'automatic_notice_reviews, automatic_notice_sources, automatic_notice_feed' + notices_identity)
                conn.execute('ALTER TABLE workdays DROP CONSTRAINT automatic_notice_workday_parent')
                conn.execute('ALTER TABLE workday_operations DROP COLUMN route_revision')
                conn.execute("DELETE FROM private_migrations WHERE name >= '016'")
            conn.execute('DROP TABLE recovery_proofs, recovery_audit')
            conn.execute("DELETE FROM private_migrations WHERE name='015_password_recovery.sql'")
            assert restore.inspect(conn)['schema'] == 14
            conn.execute("DELETE FROM private_migrations WHERE name='014_notice_creation_admissions.sql'")
            with pytest.raises(ValueError, match='Unsupported restore schema'):
                restore.inspect(conn)
        with conn.transaction(force_rollback=True):
            for expected, (name, statement) in enumerate(appended.items(), start=len(original) + 1):
                conn.execute(statement)
                conn.execute('INSERT INTO private_migrations VALUES (%s)', (name,))
                assert restore.inspect(conn)['schema'] == expected
            conn.execute("UPDATE private_migrations SET name='999_unknown.sql' WHERE name=%s", (next(iter(appended)),))
            with pytest.raises(ValueError, match='Unsupported restore schema'):
                restore.inspect(conn)
            conn.execute("DELETE FROM private_migrations WHERE name='999_unknown.sql'")
            with pytest.raises(ValueError, match='Unsupported restore schema'):
                restore.inspect(conn)


def test_all_accounts_wait_for_independent_fresh_codes(users):
    codes = [recovery.issue(recovery.resolve(name))[0] for name in users[0]]
    for name in users[0]:
        auth.authenticate(name, users[2], 'synthetic-restore')
    with database() as conn:
        before = restore.inspect(conn)
        old = conn.execute('SELECT password_hash FROM accounts ORDER BY id').fetchall()
        history = conn.execute('SELECT * FROM recovery_audit ORDER BY id').fetchall()
        limits = conn.execute('SELECT * FROM login_limits ORDER BY bucket').fetchall()
    result = restore.quarantine()
    assert result['business'] == before['business'], 'Business fingerprint changed'
    with database() as conn:
        new = conn.execute('SELECT password_hash FROM accounts ORDER BY id').fetchall()
        assert all(a != b for a, b in zip(old, new)), 'Old authority survived'
        assert len({r['password_hash'] for r in new}) == len(new), 'Random values shared'
        assert conn.execute('SELECT * FROM recovery_audit ORDER BY id').fetchall() == history
        assert conn.execute('SELECT * FROM login_limits ORDER BY bucket').fetchall() == limits
    assert restore.checked()['authority_fingerprint'] == result['authority_fingerprint']
    for name, code in zip(users[0], codes):
        assert outcome(lambda: auth.authenticate(name, users[2], 'synthetic-old')) == 401
        assert outcome(lambda: recovery.redeem(anonymous(), name, code, users[2], users[2])) == 400
    new_password = 'synthetic-restored-new-password'
    for i, name in enumerate(users[0]):
        fresh, _ = recovery.issue(recovery.resolve(name))
        recovery.redeem(anonymous(), name, fresh, new_password, new_password)
        _, session = auth.authenticate(name, new_password, 'synthetic-fresh')
        assert session['owner'] == users[1][i]
        if i == 0:
            assert outcome(lambda: auth.authenticate(users[0][1], users[2], 'synthetic-waiting')) == 401
    assert restore.snapshot()['business'] == before['business']


def test_quarantine_failure_rolls_back_every_account(users, monkeypatch):
    for name in users[0]:
        auth.authenticate(name, users[2], 'synthetic-before')
        recovery.issue(recovery.resolve(name))
    tables = ['accounts', 'sessions', 'recovery_proofs', 'recovery_audit', 'login_limits']
    def rows():
        with database() as conn:
            return [conn.execute('SELECT row_to_json(t)::text AS r FROM ' + t + ' t ORDER BY 1').fetchall() for t in tables]
    before = rows()
    def fail(conn):
        raise ValueError('synthetic final verification failure')
    monkeypatch.setattr(restore, 'verify', fail)
    with pytest.raises(ValueError):
        restore.quarantine()
    assert rows() == before, 'Quarantine transaction partially committed'


def test_ordinary_migration_does_not_quarantine(users):
    from app.private_storage import migrate
    with database() as conn:
        before = conn.execute('SELECT * FROM accounts ORDER BY id').fetchall()
    migrate()
    with database() as conn:
        assert conn.execute('SELECT * FROM accounts ORDER BY id').fetchall() == before
    for name in users[0]:
        auth.authenticate(name, users[2], 'synthetic-ordinary')
