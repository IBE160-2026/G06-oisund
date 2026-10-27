"""Actual bounded owned-child timeout and failed-command evidence probes."""
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('story123', Path(__file__).with_name('verify-story123.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class BuildEnvironmentTests(unittest.TestCase):
    def test_standard_build_clears_inherited_relative_tablet_api(self):
        with patch.dict(os.environ, {'VITE_PRIVATE_API_BASE': '/private-api', 'VITE_PRIVATE_API': 'https://wrong.invalid'}):
            env = runner.build_environment()
        self.assertNotIn('VITE_PRIVATE_API_BASE', env)
        self.assertEqual(env['VITE_PRIVATE_API'], 'http://127.0.0.1:18324')
        self.assertEqual(env['VITE_FICTIONAL_API'], 'http://127.0.0.1:18323')

    def test_dedicated_tablet_build_has_explicit_relative_base(self):
        with patch.dict(os.environ, {'VITE_PRIVATE_API_BASE': 'https://wrong.invalid'}):
            env = runner.build_environment(True)
        self.assertEqual(env['VITE_PRIVATE_API_BASE'], '/private-api')
        self.assertEqual(env['VITE_PRIVATE_API'], 'https://legacy.invalid/forbidden')

    def test_identity_records_only_allowlisted_api_settings_and_rejects_wrong_mode(self):
        env = dict(runner.build_environment(), PASSWORD='never-record', VITE_OTHER_SECRET='never-record')
        settings = runner.effective_api_settings(env)
        self.assertEqual(set(settings), {'VITE_PRIVATE_API_BASE', 'VITE_PRIVATE_API', 'VITE_FICTIONAL_API'})
        normal = runner.build_identity({'source': 'hash'}, {'asset': 'hash'}, settings)
        tablet = runner.build_identity({'source': 'hash'}, {'asset': 'hash'}, runner.effective_api_settings(runner.build_environment(True)))
        self.assertNotEqual(normal, tablet)
        self.assertNotIn('never-record', json.dumps(normal))
        self.assertNotEqual({'source': normal['source'], 'built': normal['built']}, normal)

    def test_tablet_build_uses_checked_npm_script_with_dedicated_config(self):
        self.assertEqual(runner.build_command(True)[1:], ['run', 'build', '--', '--config', 'vite.story123-tablet.config.ts'])



class OwnedExecutionTests(unittest.TestCase):
    def run_command(self, mode, command, timeout, inputs):
        runner.MODE = mode
        runner.RUN = runner.ROOT/'tmp/story123'/f'{runner.STAMP}-{mode}'
        runner.RUN.mkdir(parents=True)
        with self.assertRaises(SystemExit) as result:
            runner.execute(command, timeout=timeout, inputs=inputs)
        record = json.loads((runner.ROOT/f'docs/evidence/12-3-{mode}-{runner.STAMP}.json').read_text())
        self.assertEqual(result.exception.code, record['gate_exit_code'])
        archive_path = runner.ROOT/record['durable_bundle']
        self.assertEqual(hashlib.sha256(archive_path.read_bytes()).hexdigest(), record['durable_bundle_sha256'])
        with tarfile.open(archive_path) as archive:
            self.assertIn('raw/command.log', archive.getnames())
            self.assertIn('record.json', archive.getnames())
            for name, digest in record['durable_artifact_sha256'].items():
                self.assertEqual(hashlib.sha256(archive.extractfile(name).read()).hexdigest(), digest)
        self.assertFalse((runner.RUN/'bundle-staging').exists())
        return record

    def test_failed_command_preserves_utf8_log_and_prelaunch_inputs(self):
        directory = runner.ROOT/'tmp/story123'/f'{runner.STAMP}-failed-input'
        directory.mkdir(parents=True)
        program = directory/'probe.py'
        program.write_text("print('Feil med æ ø å', flush=True)\nraise SystemExit(7)\n", encoding='utf-8')
        record = self.run_command('probe-failed', [sys.executable, '-X', 'utf8', str(program)], 5, [program])
        self.assertEqual(record['exit_code'], 7)
        self.assertEqual(record['gate_exit_code'], 7)
        with tarfile.open(runner.ROOT/record['durable_bundle']) as archive:
            self.assertIn('Feil med æ ø å', archive.extractfile('raw/command.log').read().decode('utf-8'))
            self.assertEqual(archive.extractfile('executed-inputs/'+str(program.relative_to(runner.ROOT)).replace('\\', '/')).read(), program.read_bytes())

    def test_actual_owned_child_is_terminated_and_awaited_on_timeout(self):
        directory = runner.ROOT/'tmp/story123'/f'{runner.STAMP}-timeout-input'
        directory.mkdir(parents=True)
        child_file = directory/'child.pid'
        program = directory/'parent.py'
        program.write_text("import subprocess,sys,time\nfrom pathlib import Path\nchild=subprocess.Popen([sys.executable,'-c','import time; time.sleep(90)'])\nPath("+repr(str(child_file))+").write_text(str(child.pid))\nprint('Owned child started',flush=True)\ntime.sleep(90)\n", encoding='utf-8')
        record = self.run_command('probe-timeout', [sys.executable, str(program)], 2, [program])
        self.assertEqual(record['exit_code'], 124)
        self.assertEqual(record['failure_type'], 'TimeoutExpired')
        self.assertTrue(record['timeout_cleanup']['all_observed_exited'])
        child_pid = int(child_file.read_text())
        if os.name == 'nt':
            self.assertIn(child_pid, record['timeout_cleanup']['observed_pids'])
            self.assertTrue(record['timeout_cleanup']['awaited_pids'][str(child_pid)])
        else:
            try: os.kill(child_pid, 0)
            except ProcessLookupError: pass
            else: self.fail('Owned child survived timeout cleanup')

    @unittest.skipUnless(os.name == 'nt', 'CIM/retained-handle parent-exit race is Windows-specific')
    def test_parent_exits_during_cleanup_but_retained_child_handle_is_terminated(self):
        directory = runner.ROOT/'tmp/story123'/f'{runner.STAMP}-parent-exit-input'
        directory.mkdir(parents=True)
        child_file, parent_file, signal_file = (directory/name for name in ['child.pid', 'parent.pid', 'parent-exit.signal'])
        program = directory/'parent.py'
        program.write_text("import os,subprocess,sys,time\nfrom pathlib import Path\nchild=subprocess.Popen([sys.executable,'-c','import time; time.sleep(90)'])\nPath("+repr(str(child_file))+").write_text(str(child.pid))\nPath("+repr(str(parent_file))+").write_text(str(os.getpid()))\nprint('Owned child alive; parent waits for cleanup signal',flush=True)\nwhile not Path("+repr(str(signal_file))+").exists(): time.sleep(.01)\nprint('Parent exits during cleanup',flush=True)\n", encoding='utf-8')
        original_run = runner.subprocess.run
        snapshot_observed = []

        def snapshot_then_parent_exit(command, *args, **kwargs):
            completed = original_run(command, *args, **kwargs)
            if command[0] == 'powershell' and 'Get-CimInstance Win32_Process' in command[-1]:
                # The real CIM snapshot saw the owned child; deterministically
                # end its actual parent before cleanup consumes that snapshot.
                snapshot_observed.append(json.loads(completed.stdout))
                kernel = ctypes.WinDLL('kernel32', use_last_error=True)
                kernel.OpenProcess.restype = ctypes.c_void_p
                kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
                kernel.CloseHandle.argtypes = [ctypes.c_void_p]
                handle = kernel.OpenProcess(0x00100000, False, int(parent_file.read_text()))
                self.assertTrue(handle)
                try:
                    signal_file.write_text('exit')
                    self.assertEqual(kernel.WaitForSingleObject(handle, 5000), 0)
                finally: kernel.CloseHandle(handle)
            return completed

        with patch.object(runner.subprocess, 'run', side_effect=snapshot_then_parent_exit):
            record = self.run_command('probe-parent-exit', [sys.executable, str(program)], 2, [program])
        child_pid = int(child_file.read_text())
        self.assertEqual(len(snapshot_observed), 1)
        self.assertEqual(record['exit_code'], 124)
        self.assertEqual(record['failure_type'], 'TimeoutExpired')
        cleanup = record['timeout_cleanup']
        self.assertEqual(cleanup['root_returncode'], 0)
        self.assertTrue(cleanup['pid_tree_kill_skipped_root_exited'])
        self.assertTrue(cleanup['terminated_survivors_by_retained_handle'][str(child_pid)])
        self.assertTrue(cleanup['awaited_pids'][str(child_pid)])
        self.assertTrue(cleanup['all_observed_exited'])


if __name__ == '__main__': unittest.main()
