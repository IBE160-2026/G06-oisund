"""Offline verifier safety controls; no Docker or HTTP requests are executed."""
import importlib.util
import json
import re
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


def module():
    spec = importlib.util.spec_from_file_location('integration_verifier', Path(__file__).with_name('verify-story12-integration.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class RuntimeRefusal(unittest.TestCase):
    def refusal(self, defect):
        m = module()
        calls = []
        def run(args, **kwargs):
            calls.append((args, kwargs.get('input', '')))
            output = ''
            if args[:3] == ['docker', 'ps', '-aq']:
                output = 'api db private-api private-db'
            elif args[:2] == ['docker', 'inspect']:
                service = args[2]
                labels = {'com.docker.compose.project': m.PROJECT,
                          'com.docker.compose.project.config_files': str(m.CONFIG),
                          'com.docker.compose.project.working_dir': str(m.ROOT),
                          'com.docker.compose.service': service}
                if defect == 'config':
                    labels['com.docker.compose.project.config_files'] = 'C:/wrong/compose.yaml'
                if defect == 'workspace':
                    labels['com.docker.compose.project.working_dir'] = 'C:/wrong'
                output = json.dumps([{'Config': {'Labels': labels}, 'Mounts': [{'Type': 'volume', 'Name': 'volume'}]}])
            elif args[:3] == ['docker', 'volume', 'inspect']:
                output = json.dumps([{'Labels': {'com.docker.compose.project': 'foreign' if defect == 'volume' else m.PROJECT}}])
            elif args[:3] == ['docker', 'volume', 'ls']:
                output = ''
            elif 'exec' in args:
                self.assertIn('require_synthetic_accounts(conn)', kwargs['input'])
                if defect == 'accounts':
                    return subprocess.CompletedProcess(args, 1, '', 'synthetic guard refusal')
                # Valid downstream guard commands succeed. A missing production
                # guard must reach startup, never an accepted mock assertion.
            elif args[:2] == ['git', 'check-ignore']:
                output = 'ignored-secret'
            return subprocess.CompletedProcess(args, 0, output, '')
        messages = {'config': 'container belongs to exact project/config/workspace',
                    'workspace': 'container belongs to exact project/config/workspace',
                    'volume': 'attached volume belongs to integration project',
                    'accounts': 'Subprocess failed; see evidence command exit code'}
        error = RuntimeError if defect == 'accounts' else AssertionError
        with patch.object(m.subprocess, 'run', side_effect=run), patch.object(m, 'ready'), patch.object(m, 'SECRET') as secret:
            secret.exists.return_value = True
            with self.assertRaisesRegex(error, '^'+re.escape(messages[defect])+'$'):
                m.up()
        self.assertFalse(any('up' in args or 'restart' in args for args, _ in calls))
        self.assertFalse(any('DELETE ' in (program or '') or 'provision(' in (program or '') for _, program in calls))

    def test_wrong_config(self): self.refusal('config')
    def test_wrong_workspace(self): self.refusal('workspace')
    def test_wrong_volume(self): self.refusal('volume')
    def test_non_synthetic_account(self): self.refusal('accounts')

    def test_timeout_and_failure_recorded_without_sensitive_output(self):
        m = module()
        with patch.object(m.subprocess, 'run', side_effect=subprocess.TimeoutExpired(['fake'], 120, output='secret')):
            with self.assertRaises(RuntimeError): m.command(['fake'], program='secret', sensitive=True)
        self.assertEqual(m.record['commands'][-1]['status'], 'timeout')
        self.assertNotIn('secret', json.dumps(m.record))
        with patch.object(m.subprocess, 'run', return_value=subprocess.CompletedProcess(['fake'], 3, 'secret', 'secret')):
            with self.assertRaises(RuntimeError): m.command(['fake'], sensitive=True)
        self.assertEqual(m.record['commands'][-1]['exit_code'], 3)
        self.assertNotIn('secret', json.dumps(m.record))


class Preparation(unittest.TestCase):
    def setUp(self):
        self.m = module()
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.temp.cleanup)
        self.m.CREDENTIALS = Path(self.temp.name) / 'credentials.json'
        self.plans = []
        self.present = False
        self.provisions = []
        outer = self
        class Client:
            def __init__(self, port): pass
            def ok(self, path, body=None):
                if path == '/auth/login': return {}
                if path == '/workdays': return {'workdays': [{'id': str(i)} for i in range(len(outer.plans))], 'next_cursor': None}
                return outer.plans[int(path.rsplit('/', 1)[1])]
        self.m.Client = Client
        self.m.guard_runtime = lambda: None
        self.m.command = lambda *a, **k: 'ignored'
        self.m.private_python = lambda *a, **k: json.dumps(self.present)
        def provision(username, password):
            saved = json.loads(self.m.CREDENTIALS.read_text())
            self.assertEqual(saved['password'], password)
            self.provisions.append(username)
            self.present = True
        self.m.provision = provision
        def create(client, day):
            self.plans.append({'draft': {'service_date': day, 'activities': [{'line': '20'}], 'vehicle_duty': 'preserved edit'}})
        self.m.create_day = create

    def test_interrupted_fixture_creation_resumes_only_missing_day(self):
        create = self.m.create_day
        def interrupted(client, day):
            create(client, day)
            raise RuntimeError('interrupted')
        self.m.create_day = interrupted
        with self.assertRaises(RuntimeError): self.m.prepare()
        first = self.plans[0]
        self.m.create_day = create
        self.m.prepare()
        self.m.prepare()
        self.assertEqual(len(self.plans), 2)
        self.assertIs(self.plans[0], first)
        self.assertEqual(len(self.provisions), 1)

    def test_interrupted_provision_keeps_recoverable_credentials(self):
        provision = self.m.provision
        self.m.provision = lambda *args: (_ for _ in ()).throw(RuntimeError('interrupted'))
        with self.assertRaises(RuntimeError): self.m.prepare()
        password = json.loads(self.m.CREDENTIALS.read_text())['password']
        self.m.provision = provision
        self.m.prepare()
        self.assertEqual(json.loads(self.m.CREDENTIALS.read_text())['password'], password)

    def test_invalid_existing_password_does_not_provision_or_reset(self):
        self.present = True
        self.m.Client = lambda port: type('Client', (), {'ok': lambda *args: (_ for _ in ()).throw(AssertionError('login denied'))})()
        with self.assertRaises(AssertionError): self.m.prepare()
        self.assertEqual(self.provisions, [])

    def test_missing_deleted_plan_recreated_without_changing_survivor(self):
        self.m.prepare()
        first = self.plans.pop(0)
        survivor = self.plans[0]
        self.m.prepare()
        self.assertEqual(len(self.plans), 2)
        self.assertIs(self.plans[0], survivor)

    def test_unexpected_date_or_line_refused_without_additions(self):
        self.plans = [{'draft': {'service_date': '2031-01-04', 'activities': [{'line': '20'}]}}]
        with self.assertRaises(AssertionError): self.m.prepare()
        self.assertEqual(len(self.plans), 1)


class CleanupAndFingerprint(unittest.TestCase):
    def test_cleanup_after_failure_preserves_original_error(self):
        m = module()
        original = ValueError('original failure')
        def verify(names):
            names.append('synthetic-story12-verify-owned')
            raise original
        with patch.object(m, '_verify', side_effect=verify), patch.object(m, 'cleanup_accounts', side_effect=RuntimeError('cleanup failed')) as cleanup:
            with self.assertRaises(ValueError) as raised: m.verify()
        self.assertIs(raised.exception, original)
        cleanup.assert_called_once_with(['synthetic-story12-verify-owned'])
        self.assertEqual(m.record['cleanup']['status'], 'failed')

    def test_cleanup_runs_after_success(self):
        m = module()
        with patch.object(m, '_verify', side_effect=lambda names: names.append('synthetic-story12-foreign-owned')), patch.object(m, 'cleanup_accounts') as cleanup:
            m.verify()
        cleanup.assert_called_once_with(['synthetic-story12-foreign-owned'])

    def test_cleanup_failure_after_success_is_failure(self):
        m = module()
        with patch.object(m, '_verify', side_effect=lambda names: names.append('synthetic-story12-verify-owned')), patch.object(m, 'cleanup_accounts', side_effect=RuntimeError('cleanup failed')):
            with self.assertRaises(RuntimeError): m.verify()
        self.assertEqual(m.record['cleanup']['status'], 'failed')

    def test_manual_account_cannot_enter_cleanup(self):
        m = module()
        with patch.object(m, 'private_python') as private:
            with self.assertRaises(ValueError): m.cleanup_accounts(['synthetic-story12-manual'])
        private.assert_not_called()

    def test_fingerprint_covers_complete_lifecycle_and_receipt_rows(self):
        m = module()
        with patch.object(m, 'sql', return_value='fingerprint') as sql:
            self.assertEqual(m.private_fingerprint(), 'fingerprint')
        query = sql.call_args.args[0]
        for table in m.PRIVATE_TABLES:
            self.assertIn('FROM '+table+' t', query)
        self.assertIn('row_to_json(t)', query)
        self.assertNotIn('SELECT id,owner,content', query)


if __name__ == '__main__':
    unittest.main()
