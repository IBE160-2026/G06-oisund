"""Bounded fictional submission entry for server, management and test processes."""
import os
import runpy
import sys
from pathlib import Path
from urllib.parse import quote


def main(arguments):
    allowed = (arguments == ['app.run']
               or arguments in [['app.manage', 'migrate'], ['app.manage', 'seed'],
                                ['app.manage', 'reset', '--fictional-only'], ['pytest', '-q']])
    if (not allowed or os.environ.get('APP_MODE') != 'fictional-assessment'
            or os.environ.get('SUBMISSION_PROJECT') != 'ibe160-submission'):
        raise RuntimeError('Bounded fictional submission command required')
    password = Path('/run/secrets/submission_password').read_text().strip()
    if not password:
        raise RuntimeError('Generated submission database secret required')
    # Set the environment before importing app/tests; child Python processes
    # inherit it too. Never place this URL in command arguments or output.
    os.environ['DATABASE_URL'] = 'postgresql://fictional:' + quote(password, safe='') + '@db/fictional_assessment'
    sys.argv = arguments
    runpy.run_module(arguments[0], run_name='__main__')


if __name__ == '__main__':
    main(sys.argv[1:])
