"""No production Docker/data access. Test archive and rollback failure boundaries."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

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

if __name__ == '__main__':
    unittest.main()
