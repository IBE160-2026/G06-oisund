"""Failure evidence must survive launch errors and timeouts; no real processes run."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('integration_checks', Path(__file__).with_name('verify-story12-checks.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class ExecutionEvidence(unittest.TestCase):
    def exercise_failure(self, failure, expected):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            logs = root/'tmp/test-run'
            logs.mkdir(parents=True)
            (root/'docs/evidence').mkdir(parents=True)
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'LOGS', logs), patch.object(runner, 'hashes', return_value={'source.py': 'unchanged'}), patch.object(runner.subprocess, 'check_output', return_value='synthetic-revision'), patch.object(runner.subprocess, 'run', side_effect=failure), patch.object(sys, 'argv', ['runner', 'checks']):
                with self.assertRaises(SystemExit) as stopped:
                    runner.execute(['synthetic-missing-command'])
                self.assertEqual(stopped.exception.code, expected)
            files = list((root/'docs/evidence').glob('*.json'))
            self.assertEqual(len(files), 1)
            evidence = json.loads(files[0].read_text())
            self.assertEqual(evidence['exit_code'], expected)
            self.assertEqual(evidence['failure_type'], type(failure).__name__)
            self.assertTrue(evidence['source_unchanged'])
            self.assertTrue((logs/'command.log').exists())

    def test_missing_executable_records_failed_gate(self):
        self.exercise_failure(FileNotFoundError('synthetic'), 1)

    def test_timeout_records_failed_gate(self):
        self.exercise_failure(subprocess.TimeoutExpired('synthetic', 7200), 124)

    def test_removed_executed_input_preserves_failed_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            logs = root/'tmp/test-run'
            logs.mkdir(parents=True)
            (root/'docs/evidence').mkdir(parents=True)
            selected = root/'executed-test.ts'
            selected.write_text('synthetic assertion')
            def remove_input(*args, **kwargs):
                selected.unlink()
                return subprocess.CompletedProcess(args[0], 0)
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'LOGS', logs), patch.object(runner, 'hashes', return_value={}), patch.object(runner.subprocess, 'check_output', return_value='synthetic-revision'), patch.object(runner.subprocess, 'run', side_effect=remove_input), patch.object(sys, 'argv', ['runner', 'checks']):
                with self.assertRaises(SystemExit) as stopped:
                    runner.execute(['synthetic'], executed_inputs=[selected])
                self.assertEqual(stopped.exception.code, 2)
            evidence = json.loads(next((root/'docs/evidence').glob('*.json')).read_text())
            self.assertEqual(evidence['gate_exit_code'], 2)
            self.assertFalse(evidence['executed_inputs_unchanged'])
            self.assertIsNone(evidence['executed_input_sha256_after']['executed-test.ts'])


if __name__ == '__main__':
    unittest.main()
