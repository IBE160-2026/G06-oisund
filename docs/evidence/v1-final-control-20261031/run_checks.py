"""Read-only source checks and isolated host tests; no runtime or production writes."""
from pathlib import Path
from datetime import datetime, timezone
import subprocess, hashlib, json, os

root = Path(__file__).resolve().parents[3]
out = Path(__file__).resolve().parent
python = 'D:/IBE160/tmp/v1-remediation/.venv-followup/Scripts/python.exe'
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root)
def sha(data):
    return hashlib.sha256(data).hexdigest()
source = git('rev-parse','HEAD').decode().strip()
record = {'started_utc':datetime.now(timezone.utc).isoformat(), 'source_commit':source,
          'reused_interpreter':python, 'commands':[]}
temporary = root/'tmp/v1-final-control'
temporary.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
           PYTHONPATH=str(root/'backend')+';'+str(root/'deploy/tablet/access_gate'),
           PRIVATE_ORIGIN='http://127.0.0.1:15326', PRIVATE_LOOPBACK_DEVELOPMENT='1',
           TEMP=str(temporary),TMP=str(temporary),TMPDIR=str(temporary))
commands = [
    ('environment',[python,'-c',"import sys,jwt,pytest,cryptography;print(sys.version);print('PyJWT',jwt.__version__,'pytest',pytest.__version__,'cryptography',cryptography.__version__)"],15),
    ('host',[python,'-m','pytest','-q','-p','no:cacheprovider','backend/tests/test_cleanup_observability.py','deploy/tablet/access_gate/test_gate.py','deploy/tablet/access_gate/test_bounded_gate.py','deploy/tablet/access_gate/test_gate_http.py','scripts/test_verify_v1followup.py','--tb=short'],180),
    ('dns-fixture',[python,str(out/'dns_fixture.py')],20),
    ('submission-guards',['node','--test','scripts/test-submission.mjs'],60),
    ('preparation',['pwsh','-NoProfile','-File','scripts/test-prepare-tablet-parity.ps1'],40),
]
for name, command, timeout in commands:
    with (out/(name+'.txt')).open('wb') as stream:
        proc = subprocess.run(command,cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=timeout)
    record['commands'].append({'name':name,'command':command,'exit_code':proc.returncode,'output_sha256':sha((out/(name+'.txt')).read_bytes())})
record['inputs'] = {p:sha(git('show',source+':'+p)) for p in git('ls-tree','-r','--name-only',source,'--','backend','frontend','deploy','scripts','compose.submission.yaml').decode().splitlines()}
record['all_commands_passed'] = all(x['exit_code']==0 for x in record['commands'])
record['finished_utc'] = datetime.now(timezone.utc).isoformat()
record['method_sha256'] = sha(Path(__file__).read_bytes())
(out/'checks.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k!='inputs'},indent=2))
raise SystemExit(0 if record['all_commands_passed'] else 1)
