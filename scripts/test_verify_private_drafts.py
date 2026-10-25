"""Verifier control-flow tests; every subprocess is stubbed."""
import os
import ast
import io
import json
from pathlib import Path
import runpy
from types import SimpleNamespace
import unittest
from unittest.mock import patch


def activity_resource_stub():
    selection = {'workday_id': 'synthetic', 'activity_id': None, 'revision': 0, 'expires_at': 'synthetic'}
    lifecycle = {'workday_id': 'synthetic', 'state': 'confirmed', 'started_at': None, 'revision': 0, 'expires_at': 'synthetic'}
    def reply(request):
        if isinstance(request, str): return None
        path = request.full_url
        if path.endswith('/selection'):
            if request.data is not None:
                selection.update(activity_id='synthetic-activity', revision=1)
                return {'result': dict(selection)}
            return dict(selection)
        if path.endswith('/lifecycle'): return dict(lifecycle)
        if path.endswith('/start'):
            lifecycle.update(state='active', started_at='synthetic-server-time', revision=1)
            return {'result': dict(lifecycle)}
        return None
    return reply


class RestorationTest(unittest.TestCase):
    def test_terminal_verification_failure_restores_operational_api(self):
        calls = []
        resources = activity_resource_stub()
        def subprocess_stub(args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=0, stdout='{"activities":[]}' if 'model_dump_json' in (kwargs.get('input') or '') else '')
        def http_stub(request, **kwargs):
            import urllib.error
            path = request if isinstance(request, str) else request.full_url
            if ':8000/' in path:
                raise urllib.error.HTTPError(path, 404, 'synthetic denial', {}, None)
            if path.endswith('/close'):
                raise RuntimeError('synthetic terminal verification failure')
            if (value := resources(request)) is not None: pass
            elif path.endswith('/auth/csrf'): value = {'csrf_token': 'synthetic'}
            elif path.endswith('/auth/login'): value = {'account_id': 'synthetic'}
            elif path.endswith('/draft-operations'): value = {'operation_id': 'synthetic'}
            elif path.endswith('/workday-reviews'): value = {'operation_id': 'synthetic', 'unknowns': [], 'classifications_required': []}
            elif path.endswith('/physical-bus'):
                value = {'revision': 0, 'physical_bus': None, 'expires_at': 'synthetic'} if request.data is None else {'result': {'revision': 0, 'physical_bus': None, 'expires_at': 'synthetic'}}
            elif path.endswith('/delete'): value = {'operation_id': 'synthetic', 'deleted_id': 'synthetic', 'source_revision': 1}
            elif path.endswith('/drafts') and request.data is None: value = {'drafts': [], 'next_cursor': None}
            else: value = {'id': 'synthetic', 'expires_at': 'synthetic', 'revision': 1, 'draft': {'realtime_duty': '007', 'physical_bus': 'Bus-0012', 'activities': [{'id': 'synthetic-activity'}]}}
            response = io.BytesIO(json.dumps(value).encode()); response.headers = {'Cache-Control': 'no-store'}
            return response
        with patch.dict(os.environ, {'COMPOSE_PROJECT_NAME': 'ibe160-private-tests'}), patch('subprocess.run', subprocess_stub), patch('urllib.request.build_opener', return_value=SimpleNamespace(open=http_stub)):
            with self.assertRaisesRegex(RuntimeError, 'synthetic terminal verification failure'):
                runpy.run_path(str(Path(__file__).with_name('verify-private-drafts.py')))
        self.assertEqual(calls[-2][3], 'ibe160-private-tests')
        self.assertEqual(calls[-2][-1], 'stop')
        self.assertEqual(calls[-1][3], 'ibe160-private-work')
        self.assertEqual(calls[-1][-4:], ['up', '-d', '--wait', 'private-api'])

    def test_physical_bus_fictional_probes_use_valid_post_origin_and_body(self):
        source = Path(__file__).with_name('verify-private-drafts.py').read_text(encoding='utf-8')
        tree = ast.parse(source)
        definition = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'denied')
        requests = []
        def denied_request(request, **kwargs):
            import urllib.error
            requests.append(request)
            url = request if isinstance(request, str) else request.full_url
            raise urllib.error.HTTPError(url, 404, 'not found', {}, None)
        namespace = {'json': json, 'opener': SimpleNamespace(open=denied_request), 'urllib': __import__('urllib.request', fromlist=['request'])}
        # Use the real urllib package namespace expected by the verifier.
        namespace['urllib'] = __import__('urllib')
        exec(compile(ast.Module(body=[definition], type_ignores=[]), '<denial-probe>', 'exec'), namespace)
        payload = {'operation_id': '00000000-0000-4000-8000-000000000001', 'expected_revision': 0, 'physical_bus': '0012'}
        namespace['denied']('/workdays/00000000-0000-4000-8000-000000000002/physical-bus', 404, 8000)
        namespace['denied']('/workdays/00000000-0000-4000-8000-000000000002/physical-bus', 404, 8000, payload)
        namespace['denied']('/workday-bus-operations/' + payload['operation_id'], 404, 8000)
        self.assertEqual(requests[1].get_method(), 'POST')
        self.assertEqual(requests[1].get_header('Origin'), 'http://127.0.0.1:5173')
        self.assertEqual(json.loads(requests[1].data), payload)
        self.assertIn('denied(bus_path, 404, 8000)', source)
        self.assertIn('denied(bus_path, 404, 8000, bus_body)', source)
        self.assertIn("denied('/workday-bus-operations/' + bus_body['operation_id'], 404, 8000)", source)

    def test_bus_verification_failure_still_restores_operational_api(self):
        calls = []
        def subprocess_stub(args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=0, stdout='{"activities":[]}' if 'model_dump_json' in (kwargs.get('input') or '') else '')
        resources = activity_resource_stub()
        def http_stub(request, **kwargs):
            path = request.full_url
            if (value := resources(request)) is not None: pass
            elif path.endswith('/auth/csrf'): value = {'csrf_token': 'synthetic'}
            elif path.endswith('/auth/login'): value = {'account_id': 'synthetic'}
            elif path.endswith('/draft-operations'): value = {'operation_id': 'synthetic'}
            elif path.endswith('/workday-reviews'): value = {'operation_id': 'synthetic', 'unknowns': [], 'classifications_required': []}
            elif path.endswith('/physical-bus'):
                value = {'revision': 0, 'physical_bus': None, 'expires_at': 'synthetic'} if request.data is None else {'result': {'revision': 1, 'physical_bus': 'mismatched acknowledgement', 'expires_at': 'synthetic'}}
            else: value = {'id': 'synthetic', 'expires_at': 'synthetic', 'revision': 1, 'draft': {'realtime_duty': '007', 'physical_bus': 'Bus-0012', 'activities': [{'id': 'synthetic-activity'}]}}
            response = io.BytesIO(json.dumps(value).encode()); response.headers = {'Cache-Control': 'no-store'}
            return response
        with patch.dict(os.environ, {'COMPOSE_PROJECT_NAME': 'ibe160-private-tests'}), patch('subprocess.run', subprocess_stub), patch('urllib.request.build_opener', return_value=SimpleNamespace(open=http_stub)):
            with self.assertRaises(AssertionError): runpy.run_path(str(Path(__file__).with_name('verify-private-drafts.py')))
        self.assertEqual(calls[-2][-1], 'stop')
        self.assertEqual(calls[-2][3], 'ibe160-private-tests')
        self.assertEqual(calls[-1][3], 'ibe160-private-work')
        self.assertEqual(calls[-1][-4:], ['up', '-d', '--wait', 'private-api'])

    def test_nonprogressing_draft_cursors_fail_fast_and_restore_operational_api(self):
        for next_cursor in ['00000000-0000-4000-8000-000000000002', '00000000-0000-4000-8000-000000000001']:
            with self.subTest(next_cursor=next_cursor):
                calls, pages = [], []
                def subprocess_stub(args, **kwargs):
                    calls.append(args)
                    return SimpleNamespace(returncode=0, stdout='{"activities":[]}' if 'model_dump_json' in (kwargs.get('input') or '') else '')
                resources = activity_resource_stub()
                def http_stub(request, **kwargs):
                    path = request.full_url
                    if (value := resources(request)) is not None: pass
                    elif path.endswith('/auth/csrf'): value = {'csrf_token': 'synthetic'}
                    elif path.endswith('/auth/login'): value = {'account_id': 'synthetic'}
                    elif path.endswith('/draft-operations'): value = {'operation_id': 'synthetic'}
                    elif path.endswith('/workday-reviews'): value = {'operation_id': 'synthetic', 'unknowns': [], 'classifications_required': []}
                    elif path.endswith('/physical-bus'):
                        value = {'revision': 0, 'physical_bus': None, 'expires_at': 'synthetic'} if request.data is None else {'result': {'revision': 0, 'physical_bus': None, 'expires_at': 'synthetic'}}
                    elif path.endswith('/delete'): value = {'deleted_id': 'synthetic'}
                    elif '/drafts' in path and request.data is None:
                        pages.append(path)
                        self.assertLessEqual(len(pages), 2, 'Verifier followed an invalid cursor instead of failing fast')
                        cursor = '00000000-0000-4000-8000-000000000002' if len(pages) == 1 else next_cursor
                        value = {'drafts': [{'id': str(len(pages))}], 'next_cursor': cursor}
                    else: value = {'id': 'synthetic', 'expires_at': 'synthetic', 'revision': 1, 'draft': {'realtime_duty': '007', 'physical_bus': 'Bus-0012', 'activities': [{'id': 'synthetic-activity'}]}}
                    response = io.BytesIO(json.dumps(value).encode())
                    response.headers = {'Cache-Control': 'no-store'}
                    return response
                with patch.dict(os.environ, {'COMPOSE_PROJECT_NAME': 'ibe160-private-tests'}), patch('subprocess.run', subprocess_stub), patch('urllib.request.build_opener', return_value=SimpleNamespace(open=http_stub)):
                    with self.assertRaisesRegex(AssertionError, 'Draft pagination did not advance'):
                        runpy.run_path(str(Path(__file__).with_name('verify-private-drafts.py')))
                self.assertEqual(len(pages), 2)
                self.assertEqual(calls[-2][-1], 'stop')
                self.assertEqual(calls[-2][3], 'ibe160-private-tests')
                self.assertEqual(calls[-1][3], 'ibe160-private-work')
                self.assertEqual(calls[-1][-4:], ['up', '-d', '--wait', 'private-api'])

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

        resources = activity_resource_stub()
        def http_stub(request, **kwargs):
            if isinstance(request, str):
                self.assertIn(':8000/', request)
                self.assertTrue(started)
                raise RuntimeError('stop after prerequisite check')
            path = request.full_url
            if (value := resources(request)) is not None: pass
            elif path.endswith('/auth/csrf'):
                value = {'csrf_token': 'synthetic'}
            elif path.endswith('/auth/login'):
                value = {'account_id': 'synthetic'}
            elif path.endswith('/draft-operations'):
                value = {'operation_id': 'synthetic'}
            elif path.endswith('/workday-reviews'):
                value = {'operation_id': 'synthetic', 'unknowns': [], 'classifications_required': []}
            elif path.endswith('/physical-bus'):
                value = {'revision': 0, 'physical_bus': None, 'expires_at': 'synthetic'} if request.data is None else {'result': {'revision': 0, 'physical_bus': None, 'expires_at': 'synthetic'}}
            elif path.endswith('/delete'):
                value = {'operation_id': 'synthetic', 'deleted_id': 'synthetic', 'source_revision': 1}
            elif path.endswith('/drafts') and request.data is None:
                value = {'drafts': [], 'next_cursor': None}
            else:
                value = {'id': 'synthetic', 'expires_at': 'synthetic', 'revision': 1, 'draft': {'realtime_duty': '007', 'physical_bus': 'Bus-0012', 'activities': [{'id': 'synthetic-activity'}]}}
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
