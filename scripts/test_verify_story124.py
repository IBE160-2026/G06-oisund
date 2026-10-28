"""Offline isolation rejection tests. Never invokes Docker or HTTP."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


def adapter():
    spec = importlib.util.spec_from_file_location('story124', Path(__file__).with_name('verify-story124.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Isolation(unittest.TestCase):
    def refusal(self, defect):
        namespace = adapter().load_guard()
        calls = []
        def command(args, program=None, sensitive=False):
            calls.append(args)
            if args[:3] == ['docker', 'ps', '-aq']:
                return 'api db private-api private-db'
            if args[:2] == ['docker', 'inspect']:
                labels = {
                    'com.docker.compose.project': namespace['PROJECT'],
                    'com.docker.compose.project.config_files': str(namespace['CONFIG']),
                    'com.docker.compose.project.working_dir': str(namespace['ROOT']),
                    'com.docker.compose.service': args[2],
                }
                if defect in ('project', 'config_files', 'working_dir'):
                    labels['com.docker.compose.' + ('project' if defect == 'project' else 'project.' + defect)] = 'foreign'
                return json.dumps([{'Config': {'Labels': labels}, 'Mounts': [{'Type': 'volume', 'Name': 'isolated'}]}])
            if args[:3] == ['docker', 'volume', 'inspect']:
                return json.dumps([{'Labels': {'com.docker.compose.project': 'foreign' if defect == 'volume' else namespace['PROJECT']}}])
            self.fail('Unexpected external command')
        namespace['command'] = command
        message = ('attached volume belongs to integration project' if defect == 'volume'
                   else 'container belongs to exact project/config/workspace')
        with self.assertRaisesRegex(AssertionError, '^' + message + '$'):
            namespace['guard_runtime']()
        self.assertFalse(any('up' in args or 'restart' in args or 'exec' in args for args in calls))

    def test_foreign_project(self): self.refusal('project')
    def test_foreign_config(self): self.refusal('config_files')
    def test_foreign_worktree(self): self.refusal('working_dir')
    def test_foreign_volume(self): self.refusal('volume')

    def test_backend_guard_account_assertion_precedes_program(self):
        namespace = adapter().load_guard()
        observed = []
        def command(args, program=None, sensitive=False):
            observed.append(program)
            raise RuntimeError('synthetic guard denied')
        namespace['command'] = command
        with self.assertRaises(RuntimeError):
            namespace['private_python']('MUTATION')
        self.assertLess(observed[0].index('require_synthetic_accounts(conn)'), observed[0].index('MUTATION'))

    def test_build_settings_reject_inherited_api_targets(self):
        with patch.object(Path, 'mkdir'), patch.dict(os.environ, {
            'VITE_PRIVATE_API_BASE': 'https://wrong.invalid/base',
            'VITE_PRIVATE_API': 'https://wrong.invalid/private',
            'VITE_FICTIONAL_API': 'https://wrong.invalid/fictional',
        }):
            runner = adapter().load_runner()
            desktop = runner['effective_api_settings'](runner['build_environment']())
            tablet = runner['effective_api_settings'](runner['build_environment'](True))
        self.assertEqual(desktop, {
            'VITE_PRIVATE_API_BASE': None,
            'VITE_PRIVATE_API': 'http://127.0.0.1:18326',
            'VITE_FICTIONAL_API': 'http://127.0.0.1:18325',
        })
        self.assertEqual(tablet, {
            'VITE_PRIVATE_API_BASE': '/private-api',
            'VITE_PRIVATE_API': 'https://legacy.invalid/forbidden',
            'VITE_FICTIONAL_API': 'http://127.0.0.1:18325',
        })

    def test_failed_fresh_build_prevents_browser_or_mobile_runner_launch(self):
        for mode in ('browser', 'mobile'):
            with self.subTest(mode=mode):
                module = adapter()
                with patch('sys.argv', ['verify-story124.py', mode]), patch.object(
                    module.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, ['build'])
                ) as build, patch.object(module, 'load_runner') as launch:
                    with self.assertRaises(subprocess.CalledProcessError):
                        module.main()
                self.assertTrue(build.call_args.kwargs['check'])
                self.assertEqual(build.call_args.args[0][-1], 'tablet-build' if mode == 'mobile' else 'build')
                launch.assert_not_called()

    def test_browser_runtime_guard_denial_prevents_launch(self):
        module = adapter()
        launched = []
        def denied(): raise RuntimeError('synthetic runtime denied')
        with patch('sys.argv', ['verify-story124.py', 'browser']), patch.object(module, 'fresh_build'), patch.object(
            module, 'load_runner', return_value={'browser': lambda: launched.append(True)}
        ), patch.object(module, 'load_guard', return_value={'guard_runtime': denied}):
            with self.assertRaisesRegex(RuntimeError, 'synthetic runtime denied'):
                module.main()
        self.assertEqual(launched, [])

    def test_browser_runtime_guard_precedes_launch(self):
        module = adapter()
        order = []
        with patch('sys.argv', ['verify-story124.py', 'browser']), patch.object(module, 'fresh_build'), patch.object(
            module, 'load_runner', return_value={'browser': lambda: order.append('browser')}
        ), patch.object(module, 'load_guard', return_value={'guard_runtime': lambda: order.append('guard')}):
            module.main()
        self.assertEqual(order, ['guard', 'browser'])

    def test_lf_and_crlf_shared_templates_are_qualified_before_exec(self):
        module = adapter()
        canonical = {name: (module.ROOT/name).read_bytes().replace(b'\r\n', b'\n')
                     for name in module.QUALIFIED_TEMPLATES}
        for newline in (b'\n', b'\r\n'):
            with self.subTest(newline=newline), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for name, source in canonical.items():
                    (root/name).parent.mkdir(parents=True, exist_ok=True)
                    (root/name).write_bytes(source.replace(b'\n', newline))
                with patch.object(module, 'ROOT', root), patch.object(module, 'exec', create=True) as execute:
                    self.assertEqual(module.qualified_templates(), {name: source.decode('utf-8') for name, source in canonical.items()})
                    module.load_runner()
                    module.load_guard()
                    self.assertEqual(execute.call_count, 2)

    def test_changed_shared_templates_are_rejected_before_exec(self):
        module = adapter()
        for changed in module.QUALIFIED_TEMPLATES:
            for loader in ('load_runner', 'load_guard'):
                with self.subTest(changed=changed, loader=loader), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    for name in module.QUALIFIED_TEMPLATES:
                        (root/name).parent.mkdir(parents=True, exist_ok=True)
                        (root/name).write_bytes((module.ROOT/name).read_bytes())
                    with (root/changed).open('ab') as stream:
                        stream.write(b'\nraise RuntimeError("unqualified source executed")\n')
                    with patch.object(module, 'ROOT', root), patch.object(module, 'exec', create=True) as execute:
                        with self.assertRaisesRegex(RuntimeError, 'Qualified shared template changed'):
                            getattr(module, loader)()
                        execute.assert_not_called()

    def test_audit_exception_retains_checks_identity_and_phase(self):
        path = Path(__file__).with_name('audit-story124-runtime.py')
        spec = importlib.util.spec_from_file_location('story124_audit', path)
        audit = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(audit)
        def fail_after_check(record):
            record.update(revision='synthetic-revision', api_containers={'api': {'id': 'synthetic-container'}}, phase='served build: synthetic.js')
            record['checks'].append({'name': 'earlier source identity', 'passed': True})
            raise RuntimeError('synthetic interrupted audit')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'docs/evidence').mkdir(parents=True)
            with patch.object(audit, 'ROOT', root), patch.object(audit, 'main', side_effect=fail_after_check):
                with self.assertRaisesRegex(RuntimeError, 'synthetic interrupted audit'):
                    audit.run()
            record = json.loads(next((root/'docs/evidence').glob('12-4-runtime-failed-*.json')).read_text())
            self.assertEqual(record['revision'], 'synthetic-revision')
            self.assertEqual(record['api_containers']['api']['id'], 'synthetic-container')
            self.assertEqual(record['phase'], 'served build: synthetic.js')
            self.assertEqual(record['checks'], [{'name': 'earlier source identity', 'passed': True}])
            self.assertEqual(record['failure_type'], 'RuntimeError')
            self.assertFalse(record['passed'])


if __name__ == '__main__':
    unittest.main()
