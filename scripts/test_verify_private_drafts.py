"""Verifier control-flow tests; every subprocess is stubbed."""
import os
from pathlib import Path
import runpy
from types import SimpleNamespace
import unittest
from unittest.mock import patch


class RestorationTest(unittest.TestCase):
    def test_operational_restore_is_attempted_even_when_disposable_stop_fails(self):
        calls = []

        def subprocess_stub(args, **kwargs):
            calls.append(args)
            # Fail the initial work before any HTTP, then fail disposable stop too.
            return SimpleNamespace(returncode=0 if 'up' in args else 1, stdout='synthetic failure')

        with patch.dict(os.environ, {'COMPOSE_PROJECT_NAME': 'ibe160-private-tests'}), patch('subprocess.run', subprocess_stub):
            with self.assertRaises(RuntimeError):
                runpy.run_path(str(Path(__file__).with_name('verify-private-drafts.py')))
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[1][3], 'ibe160-private-tests')
        self.assertEqual(calls[1][-1], 'stop')
        self.assertEqual(calls[2][3], 'ibe160-private-work')
        self.assertEqual(calls[2][-4:], ['up', '-d', '--wait', 'private-api'])


if __name__ == '__main__':
    unittest.main()
