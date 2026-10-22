"""Verifier control-flow tests; every subprocess is stubbed."""
import os
import io
import json
from pathlib import Path
import runpy
from types import SimpleNamespace
import unittest
from unittest.mock import patch


class RestorationTest(unittest.TestCase):
    def test_fictional_api_is_awaited_before_demo_denial_checks(self):
        calls = []
        started = False

        def subprocess_stub(args, **kwargs):
            nonlocal started
            calls.append(args)
            if 'ibe160-fictional-assessment' in args and args[-1] == 'api':
                self.assertIn('--wait', args)
                started = True
            return SimpleNamespace(returncode=0, stdout='{"activities":[]}' if 'model_dump_json' in (kwargs.get('input') or '') else '')

        def http_stub(request, **kwargs):
            if isinstance(request, str):
                self.assertIn(':8000/', request)
                self.assertTrue(started)
                raise RuntimeError('stop after prerequisite check')
            path = request.full_url
            if path.endswith('/auth/csrf'):
                value = {'csrf_token': 'synthetic'}
            elif path.endswith('/auth/login'):
                value = {'account_id': 'synthetic'}
            elif path.endswith('/draft-operations'):
                value = {'operation_id': 'synthetic'}
            elif path.endswith('/workday-reviews'):
                value = {'operation_id': 'synthetic', 'unknowns': [], 'classifications_required': []}
            elif path.endswith('/delete'):
                value = {'operation_id': 'synthetic', 'deleted_id': 'synthetic', 'source_revision': 1}
            else:
                value = {'id': 'synthetic', 'revision': 1, 'draft': {'realtime_duty': '007', 'physical_bus': 'Bus-0012'}}
            response = io.BytesIO(json.dumps(value).encode())
            response.headers = {'Cache-Control': 'no-store'}
            return response

        with patch.dict(os.environ, {'COMPOSE_PROJECT_NAME': 'ibe160-private-tests'}), patch('subprocess.run', subprocess_stub), patch('urllib.request.build_opener', return_value=SimpleNamespace(open=http_stub)):
            with self.assertRaisesRegex(RuntimeError, 'stop after prerequisite check'):
                runpy.run_path(str(Path(__file__).with_name('verify-private-drafts.py')))
        self.assertTrue(started)
        self.assertEqual(calls[-1][-4:], ['up', '-d', '--wait', 'private-api'])

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
