"""Focused wrapper checks without Docker networking or real secrets."""
import os
import unittest
from unittest.mock import patch

from fictional import main


class FictionalWrapperTests(unittest.TestCase):
    def test_all_supported_commands_receive_generated_url(self):
        commands = [['app.run'], ['app.manage', 'migrate'], ['app.manage', 'seed'],
                    ['app.manage', 'reset', '--fictional-only'], ['pytest', '-q']]
        for command in commands:
            with self.subTest(command=command), patch.dict(os.environ, {'APP_MODE': 'fictional-assessment', 'SUBMISSION_PROJECT': 'ibe160-submission'}, clear=True), patch('fictional.Path.read_text', return_value='synthetic:@/ secret\n'), patch('fictional.runpy.run_module') as run:
                main(command)
                self.assertEqual(os.environ['DATABASE_URL'], 'postgresql://fictional:synthetic%3A%40%2F%20secret@db/fictional_assessment')
                run.assert_called_once_with(command[0], run_name='__main__')

    def test_wrong_target_or_command_refuses_before_reading_secret(self):
        for mode, project, command in [('private-local', 'ibe160-submission', ['app.run']), ('fictional-assessment', 'ordinary', ['pytest', '-q']), ('fictional-assessment', 'ibe160-submission', ['app.manage', 'provision', 'jonas'])]:
            with self.subTest(mode=mode, project=project, command=command), patch.dict(os.environ, {'APP_MODE': mode, 'SUBMISSION_PROJECT': project}, clear=True), patch('fictional.Path.read_text') as read:
                with self.assertRaises(RuntimeError):
                    main(command)
                read.assert_not_called()

    def test_empty_secret_refuses_before_import(self):
        with patch.dict(os.environ, {'APP_MODE': 'fictional-assessment', 'SUBMISSION_PROJECT': 'ibe160-submission'}, clear=True), patch('fictional.Path.read_text', return_value='\n'), patch('fictional.runpy.run_module') as run:
            with self.assertRaises(RuntimeError):
                main(['app.run'])
            run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
