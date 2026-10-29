"""Focused adapter tests; no service or process operations."""
import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch
import pytest

spec = importlib.util.spec_from_file_location('followup_adapter', Path(__file__).with_name('verify-v1followup.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


@pytest.mark.parametrize('mode', ['mobile', 'tablet-build'])
def test_unsupported_modes_refuse_before_build_or_runtime(mode):
    with patch.object(runner.sys, 'argv', ['verify-v1followup.py', mode]), patch.object(runner, 'load_runner') as load, patch.object(runner, 'fresh_build') as build:
        with pytest.raises(SystemExit):
            runner.main()
        load.assert_not_called(); build.assert_not_called()


def test_serve_refuses_when_runtime_guard_fails_before_preview():
    guard = Mock(side_effect=RuntimeError('synthetic guard refused'))
    with patch.object(runner.sys, 'argv', ['verify-v1followup.py', 'serve']), patch.object(runner, 'load_runner', return_value={}), patch.object(runner, 'fresh_build'), patch.object(runner, 'load_guard', return_value={'guard_runtime': guard}), patch.object(runner, 'preview') as preview:
        with pytest.raises(RuntimeError, match='guard refused'):
            runner.main()
        guard.assert_called_once(); preview.assert_not_called()


def test_serve_checks_guard_before_preview_and_stop_does_not_need_apis():
    order = []
    with patch.object(runner, 'load_runner', return_value={}), patch.object(runner, 'fresh_build'), patch.object(runner, 'load_guard', return_value={'guard_runtime': lambda: order.append('guard')}), patch.object(runner, 'preview', side_effect=lambda mode: order.append(mode)):
        with patch.object(runner.sys, 'argv', ['verify-v1followup.py', 'serve']):
            runner.main()
        assert order == ['guard', 'serve']
        with patch.object(runner.sys, 'argv', ['verify-v1followup.py', 'stop-preview']), patch.object(runner, 'load_guard', side_effect=RuntimeError('APIs unavailable')):
            runner.main()
        assert order == ['guard', 'serve', 'stop-preview']
