"""Receipt failure paths; never connects to production."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import runpy
import sys
from unittest.mock import patch

import night_controls as controls


class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p = patch.object(controls, 'OUT', Path(self.tmp.name))
        p.start(); self.addCleanup(p.stop)
        p = patch.object(controls, 'EXIT_CODES', [])
        p.start(); self.addCleanup(p.stop)

    def test_partial_timeout_is_preserved(self):
        with patch.object(subprocess, 'run', side_effect=subprocess.TimeoutExpired('fixture', 90, output=b'partial')):
            controls.capture('timeout', ['fixture'])
        self.assertEqual((controls.OUT/'timeout.txt').read_bytes(), b'partial')
        result = json.loads((controls.OUT/'timeout.json').read_text())
        self.assertTrue(result['timed_out']); self.assertEqual(result['exit'], 124)
        self.assertEqual(controls.EXIT_CODES, [124])

    def test_orphan_metadata_is_not_overwritten(self):
        (controls.OUT/'existing.json').write_text('original')
        with patch.object(subprocess, 'run') as runner:
            with self.assertRaises(RuntimeError): controls.capture('existing', ['fixture'])
            runner.assert_not_called()
        self.assertEqual((controls.OUT/'existing.json').read_text(), 'original')

    def test_remote_failures_are_not_masked_by_later_success(self):
        result = subprocess.run(['sh', '-c', controls.remote_controls(['false', 'true'])], capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn(b'CONTROL_EXIT 0=1', result.stdout)
        self.assertIn(b'CONTROL_EXIT 1=0', result.stdout)

    def test_qualification_timeout_always_cleans_unique_container(self):
        with patch.object(controls, 'capture', side_effect=subprocess.TimeoutExpired('fixture', 90)), \
                patch.object(subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, b'removed', b'')) as runner, \
                patch.object(sys, 'argv', ['run_o5_tests.py', 'timeout-runner']):
            with self.assertRaises(subprocess.TimeoutExpired):
                runpy.run_path(str(Path(__file__).with_name('run_o5_tests.py')), run_name='__main__')
        args = runner.call_args.args[0]
        self.assertEqual(args[:3], ['docker', 'rm', '-f'])
        self.assertTrue(args[3].startswith('ibe160-o5-night-qualification-'))
        self.assertEqual(len(args[3].rsplit('-', 1)[1]), 32)
        result = json.loads((controls.OUT/'timeout-runner-cleanup.json').read_text())
        self.assertEqual(result['container'], args[3])
