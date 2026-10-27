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

spec = importlib.util.spec_from_file_location('story123', Path(__file__).with_name('verify-story123.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


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


if __name__ == '__main__': unittest.main()
