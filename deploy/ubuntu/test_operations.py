"""No production Docker/data access. Test archive and rollback failure boundaries."""
import hashlib
import importlib.util
import io
import json
import os
import pty
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch
from contextlib import ExitStack

spec = importlib.util.spec_from_file_location('ops', Path(__file__).with_name('bussassistentctl.py'))
ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ops)
COMMIT = 'a' * 40


class OperationsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.root = root / 'app'
        self.uploads = root / 'uploads'
        (self.root / 'releases').mkdir(parents=True)
        self.uploads.mkdir()
        for name, value in [('ROOT', self.root), ('UPLOADS', self.uploads),
                            ('BACKUPS', root / 'backups')]:
            p = patch.object(ops, name, value)
            p.start()
            self.addCleanup(p.stop)

    def archive(self, names):
        target = self.uploads / (COMMIT + '.tar')
        with tarfile.open(target, 'w') as tar:
            for name, kind in names:
                entry = tarfile.TarInfo(name)
                if kind == 'link':
                    entry.type = tarfile.SYMTYPE
                    entry.linkname = '/etc/passwd'
                    tar.addfile(entry)
                else:
                    entry.size = 4
                    tar.addfile(entry, io.BytesIO(b'test'))
        return hashlib.sha256(target.read_bytes()).hexdigest()

    def test_rejects_revision_path_injection(self):
        for bad in ('../current', 'HEAD', 'a' * 39, 'a' * 40 + ';id'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                ops.release(bad)

    def test_rejects_digest_mismatch_before_extract(self):
        self.archive([('backend/Dockerfile', 'file')])
        with self.assertRaisesRegex(ValueError, 'digest mismatch'):
            ops.stage(COMMIT, '0' * 64)
        self.assertEqual(list((self.root / 'releases').iterdir()), [])

    def test_rejects_traversal_and_symlinks(self):
        for name, kind in [('../escape', 'file'), ('/absolute', 'file'), ('backend/link', 'link')]:
            with self.subTest(name=name):
                digest = self.archive([(name, kind)])
                with self.assertRaisesRegex(ValueError, 'unsafe entries'):
                    ops.stage(COMMIT, digest)
        self.assertEqual(list((self.root / 'releases').iterdir()), [])

    def test_rejects_incomplete_release(self):
        digest = self.archive([('backend/Dockerfile', 'file')])
        with self.assertRaisesRegex(ValueError, 'Incomplete release'):
            ops.stage(COMMIT, digest)
        self.assertEqual(list((self.root / 'releases').iterdir()), [])

    def test_stage_retry_preserves_immutable_identity(self):
        digest = self.archive([(p, 'file') for p in (
            'backend/Dockerfile', 'deploy/tablet/Dockerfile', 'deploy/ubuntu/compose.yaml')])
        with patch.object(ops, 'compose') as compose:
            ops.stage(COMMIT, digest)
            ops.stage(COMMIT, digest)
            self.assertEqual(compose.call_count, 4)
            with self.assertRaisesRegex(ValueError, 'identity mismatch'):
                ops.stage(COMMIT, '0' * 64)

    def test_failed_dump_never_published_as_completed(self):
        def fail(*args, **kwargs):
            kwargs['stdout'].write(b'partial')
            raise subprocess.CalledProcessError(1, 'pg_dump')
        with patch.object(ops, 'compose', side_effect=fail), self.assertRaises(subprocess.CalledProcessError):
            ops.backup(Path(COMMIT))
        self.assertEqual(list(ops.BACKUPS.glob('*.dump')), [])

    def test_rollback_refuses_schema_change_before_stopping_services(self):
        old = self.root / 'releases' / ('b' * 40)
        new = self.root / 'releases' / COMMIT
        for path in (old, new):
            (path / 'backend/migrations/private').mkdir(parents=True)
        (new / 'backend/migrations/private/001.sql').write_text('new schema')
        (self.root / 'current').symlink_to(new)
        with patch.object(sys, 'argv', ['ctl', 'rollback', old.name]), patch.object(ops, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'identical migration'):
                ops.main()
            run.assert_not_called()



    def test_restore_refuses_nonempty_database(self):
        path = self.root / 'releases' / COMMIT
        path.mkdir()
        with patch.object(ops, 'DATA_READY', self.root / 'data-ready'), patch.object(
                ops, 'compose', return_value=subprocess.CompletedProcess([], 0, stdout='3\n')) as compose:
            with self.assertRaisesRegex(ValueError, 'empty database'):
                ops.restore_initial(COMMIT, '0' * 64)
            self.assertEqual(compose.call_count, 1)

    def test_restore_refuses_corrupt_dump_before_pg_restore(self):
        (self.root / 'releases' / COMMIT).mkdir()
        (self.uploads / 'initial.dump').write_bytes(b'dump bytes')
        with patch.object(ops, 'DATA_READY', self.root / 'data-ready'), patch.object(
                ops, 'compose', return_value=subprocess.CompletedProcess([], 0, stdout='0\n')) as compose:
            with self.assertRaisesRegex(ValueError, 'digest mismatch'):
                ops.restore_initial(COMMIT, '0' * 64)
            self.assertEqual(compose.call_count, 1)

    def test_first_deploy_requires_verified_data_marker(self):
        (self.root / 'releases' / COMMIT).mkdir()
        with patch.object(ops, 'DATA_READY', self.root / 'data-ready'), patch.object(
                sys, 'argv', ['ctl', 'deploy', COMMIT]), patch.object(ops, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'verified restore'):
                ops.main()
            run.assert_not_called()

    def test_secrets_refuse_overwrite_before_any_install(self):
        secret_dir = self.uploads / 'secrets'
        secret_dir.mkdir()
        config_dir = self.root / 'config'
        (config_dir / 'secrets').mkdir(parents=True)
        for name in ('bootstrap-password', 'postgres-password', 'access-policy.json', 'tunnel-token'):
            (secret_dir / name).write_text('new-value')
        existing = config_dir / 'secrets/bootstrap-password'
        existing.write_text('preserve-old-value')
        with patch.object(ops, 'CONFIG', config_dir / 'server.env'):
            with self.assertRaisesRegex(ValueError, 'overwrite'):
                ops.install_secrets()
        self.assertEqual(existing.read_text(), 'preserve-old-value')
        self.assertFalse((config_dir / 'secrets/postgres-password').exists())

    def test_enable_does_not_wait_on_its_own_operation_lock(self):
        path = self.root / 'releases' / COMMIT
        path.mkdir()
        (self.root / 'current').symlink_to(path)
        with patch.object(sys, 'argv', ['ctl', 'enable']), patch.object(ops, 'ready'), patch.object(ops, 'run') as run:
            ops.main()
        calls = [call.args[0] for call in run.call_args_list]
        self.assertEqual(calls[0][0:2], ['systemctl', 'enable'])
        self.assertNotIn('--now', calls[0])
        self.assertIn('--no-block', calls[1])

    def recovery_release(self):
        path = self.root / 'releases' / COMMIT
        path.mkdir()
        (self.root / 'current').symlink_to(path)
        return path

    def terminal_mocks(self):
        stack = ExitStack()
        for name, value in [('isatty', True), ('ttyname', '/dev/pts/7'),
                            ('tcgetpgrp', 123), ('getpgrp', 123), ('open', 77)]:
            stack.enter_context(patch.object(ops.os, name, return_value=value))
        stack.enter_context(patch.object(ops.os, 'close'))
        return stack

    def test_recovery_fixed_command_and_terminal_streams(self):
        path = self.recovery_release()
        for action in ('recovery-issue', 'recovery-revoke'):
            with self.subTest(action=action), self.terminal_mocks(), patch.object(
                    ops.subprocess, 'run') as run, patch.object(sys, 'argv', ['ctl', action, ' SYNTHETIC-Owner ']):
                ops.main()
                args, kw = run.call_args
                self.assertEqual(args[0], ['docker', 'compose', '--project-name', 'bussassistent',
                    '--env-file', str(ops.CONFIG), '-f', str(path / 'deploy/ubuntu/compose.yaml'),
                    'exec', 'private-api', 'python', '-m', 'app.manage', action, 'synthetic-owner'])
                self.assertEqual({key: kw[key] for key in ('stdin', 'stdout', 'stderr')},
                                 dict(stdin=77, stdout=77, stderr=77))
                self.assertEqual(kw['env']['RELEASE_ID'], COMMIT)
                self.assertNotIn('shell', kw)
                self.assertNotIn('capture_output', kw)

    def test_recovery_invalid_args_fail_before_docker(self):
        for argv in (['ctl', 'recovery-issue'], ['ctl', 'recovery-revoke', 'synthetic-a', '--flag'],
                     *[['ctl', 'recovery-issue', value] for value in ('', '  ', '--help', 'a'*101,
                         'synthetic-\x1b[2J', 'synthetic-\n', 'synthetic-\u202e')]):
            with self.subTest(argv=argv), patch.object(sys, 'argv', argv), patch.object(ops, 'run') as run:
                with self.assertRaises(ValueError):
                    ops.main()
                run.assert_not_called()

    def test_recovery_rejects_redirect_missing_foreign_or_background_terminal(self):
        cases = [('isatty', [False, True, True]), ('isatty', [True, False, True]),
                 ('isatty', [True, True, False]), ('open', OSError('No controlling terminal')),
                 ('ttyname', ['/dev/pts/1', '/dev/pts/2', '/dev/pts/1']),
                 ('tcgetpgrp', [123, 123, 123, 456])]
        for name, effect in cases:
            with self.subTest(name=name, effect=effect), self.terminal_mocks(), patch.object(
                    ops.os, name, side_effect=effect), patch.object(ops, 'run') as run:
                with self.assertRaises((ValueError, OSError)):
                    ops.recovery('recovery-issue', 'synthetic-owner')
                run.assert_not_called()

    def test_recovery_rejects_invalid_current_release(self):
        (self.root / 'current').symlink_to(self.uploads)
        with self.terminal_mocks(), patch.object(ops, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'release path'):
                ops.recovery('recovery-revoke', 'synthetic-owner')
            run.assert_not_called()

    def test_recovery_entrypoint_keeps_root_and_lock_boundary(self):
        from unittest.mock import mock_open
        events = []
        with patch.object(ops.os, 'geteuid', return_value=1), patch.object(ops, 'main') as main:
            with self.assertRaises(SystemExit):
                ops.entrypoint()
            main.assert_not_called()
        with patch.object(ops.os, 'geteuid', return_value=0), patch('builtins.open', mock_open()) as opened, patch.object(
                ops.fcntl, 'flock', side_effect=lambda *args: events.append('locked')), patch.object(
                ops, 'main', side_effect=lambda: events.append('main')):
            ops.entrypoint()
            opened.assert_called_once_with('/run/lock/bussassistent.lock', 'w')
        self.assertEqual(events, ['locked', 'main'])

    def test_recovery_actual_pty_and_outer_redirects(self):
        self.recovery_release()
        # Child has an actual controlling PTY; subprocess is always mocked.
        # No Docker invocation or secret is generated by this host-boundary test.
        for redirect in (None, 0, 1, 2):
            pid, terminal = pty.fork()
            if pid == 0:
                try:
                    if redirect is not None:
                        null = os.open('/dev/null', os.O_RDWR)
                        os.dup2(null, redirect)
                        os.close(null)
                    called = []
                    def fake_run(args, **kwargs):
                        called.append(True)
                        fds = [kwargs[name] for name in ('stdin', 'stdout', 'stderr')]
                        assert len(set(fds)) == 1 and os.isatty(fds[0])
                        assert os.tcgetpgrp(fds[0]) == os.getpgrp()
                    with patch.object(ops.subprocess, 'run', side_effect=fake_run):
                        try:
                            ops.recovery('recovery-issue', 'synthetic-owner')
                            valid = redirect is None and called == [True]
                        except ValueError:
                            valid = redirect is not None and not called
                    os._exit(0 if valid else 1)
                except BaseException:
                    os._exit(2)
            try:
                _, status = os.waitpid(pid, 0)
                self.assertEqual(os.waitstatus_to_exitcode(status), 0)
            finally:
                os.close(terminal)

if __name__ == '__main__':
    unittest.main()
