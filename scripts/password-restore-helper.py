"""Execute actual host SQL assembler with transport-only doubles; no Docker socket.

Inputs are real pg_restore TOC/SQL output produced from the disposable DB dump.
The assembled transaction is executed against that real database by the runner.
"""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import subprocess
import sys

spec = importlib.util.spec_from_file_location('restore_helper', '/host-tests/bussassistentctl.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
state = Path('/state')
destination = state / 'replacement.sql'
destination.unlink(missing_ok=True)
archive = state / 'current.dump'


def transport(path, *args, **kwargs):
    if '--list' in args:
        return SimpleNamespace(stdout=(state/'toc.txt').read_bytes())
    if '--file=-' in args:
        # Real child descriptor writes preserve the buffering boundary of
        # pg_restore (a Python-buffer write double would conceal ordering bugs).
        return subprocess.run([sys.executable, '-c',
            "import sys;from pathlib import Path;sys.stdout.buffer.write(Path('/state/archive.sql').read_bytes())"],
            stdout=kwargs['stdout'], check=True)
    raise RuntimeError('Unexpected host transport')


with patch.object(helper, 'compose', side_effect=transport):
    helper.restore_sql(Path('/synthetic-release'), archive, destination)
