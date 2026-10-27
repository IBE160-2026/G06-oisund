"""Pure unit checks: never starts/stops an actual service or accesses the DB."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location('retained_runner', Path(__file__).with_name('verify-retained-data.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class PreviewOwnership(unittest.TestCase):
    def identity(self):
        return {'pid': 12345, 'created': 'synthetic-creation', 'command': f'node "{runner.VITE}" preview --host 127.0.0.1 --port 15121 --strictPort'}

    def test_occupied_port_refuses_before_launch(self):
        probe = Mock()
        probe.bind.side_effect = OSError('in use')
        with patch.object(runner.socket, 'socket') as socket, patch.object(runner.subprocess, 'Popen') as launch:
            socket.return_value.__enter__.return_value = probe
            with self.assertRaisesRegex(RuntimeError, 'occupied'):
                runner.serve_preview()
            launch.assert_not_called()

    def test_changed_pid_identity_never_stops_process(self):
        original = self.identity()
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory)/'preview.json'
            record.write_text(json.dumps({'root': str(runner.ROOT), 'vite': str(runner.VITE), 'identity': original}))
            with patch.object(runner, 'PREVIEW', record), patch.object(runner, 'process_identity', return_value={**original, 'created': 'different'}), patch.object(runner.subprocess, 'run') as stop:
                with self.assertRaisesRegex(RuntimeError, 'identity changed'):
                    runner.stop_preview()
                stop.assert_not_called()

    def test_owned_preview_stops_only_verified_pid_tree(self):
        original = self.identity()
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory)/'preview.json'
            record.write_text(json.dumps({'root': str(runner.ROOT), 'vite': str(runner.VITE), 'identity': original}))
            with patch.object(runner, 'PREVIEW', record), patch.object(runner, 'process_identity', return_value=original), patch.object(runner.subprocess, 'run') as stop:
                runner.stop_preview()
                self.assertEqual(stop.call_args.args[0], ['taskkill.exe', '/PID', '12345', '/T', '/F'])
                self.assertFalse(record.exists())

    def test_child_failure_is_not_reported_as_ready(self):
        original = self.identity()
        child = Mock(pid=12345)
        child.poll.return_value = 1
        probe = Mock()
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory)/'preview.json'
            with patch.object(runner, 'PREVIEW', record), patch.object(runner.socket, 'socket') as socket, patch.object(runner.subprocess, 'Popen', return_value=child), patch.object(runner, 'process_identity', return_value=original), patch.object(runner, 'stop_preview') as stop:
                socket.return_value.__enter__.return_value = probe
                with self.assertRaisesRegex(RuntimeError, 'startup failed'):
                    runner.serve_preview()
                stop.assert_called_once()


if __name__ == '__main__':
    unittest.main()
