import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request
from datetime import datetime, timezone

root = Path('D:/IBE160')
def command(args):
    return subprocess.check_output(args, cwd=root, text=True, encoding='utf-8').strip()
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def containers():
    ids = command(['docker','ps','-q']).split()
    fmt = '{{json .Id}}|{{json .Name}}|{{json .Image}}|{{json .State.StartedAt}}|{{json .RestartCount}}|{{json .Config.Labels}}'
    return sorted(command(['docker','inspect','--format',fmt,*ids]).splitlines())

before = containers()
tested = '62a0cf4f67f2ce1ea2b0da78c76858a10d7adf11'
head = command(['git','rev-parse','HEAD'])
assert command(['git','branch','--show-current']) == 'main'
changes = command(['git','diff','--name-only',tested,head]).splitlines()
assert all(n.startswith(('docs/','.logs/')) for n in changes)
evidence = list((root/'docs/evidence').glob('12-integrated-*20261027T15*.json'))
verified = []
for path in evidence:
    item = json.loads(path.read_text(encoding='utf-8-sig'))
    assert item['revision'] == tested and item['gate_exit_code'] == 0
    assert item['source_unchanged'] and item['executed_inputs_unchanged']
    hashes = item['source_sha256']
    assert all((root/n).is_file() and sha(root/n) == value for n,value in hashes.items())
    assert sha(root/item['log']) == item['log_sha256']
    assert all(sha(root/n) == value for n,value in item['executed_input_sha256'].items())
    verified.append({'file':path.name,'input_count':len(hashes),'sha256':sha(path)})
assert {json.loads((root/'docs/evidence'/v['file']).read_text())['mode'] for v in verified} == {'build','checks','backend','fictional','demo','browser'}

# Reuse the read-only source/HTTP audit, with a distinct output: retain historical evidence.
audit = (root/'tmp/story12-refresh/audit.py').read_text(encoding='utf-8')
audit = audit.replace('12-after-access-runtime.json','12-current-main-runtime.json')
exec(compile(audit, 'read-only-runtime-audit', 'exec'))
runtime = json.loads((root/'docs/evidence/12-current-main-runtime.json').read_text())
prior = json.loads((root/'docs/evidence/12-after-access-runtime.json').read_text())
assert runtime['api_files'] == prior['api_files'] and runtime['assets'] == prior['assets']
served = {}
for path in (root/'frontend/dist').rglob('*'):
    if path.is_file():
        relative = path.relative_to(root/'frontend/dist').as_posix()
        with urllib.request.urlopen('http://127.0.0.1:15312/'+relative,timeout=10) as response:
            assert response.read() == path.read_bytes()
        served[relative] = sha(path)

compose = ['docker','compose','-p','ibe160-story12-integration','-f','compose.story12-integration.yaml']
program = """import json
from app.auth import require_synthetic_accounts
from app.private_storage import database
with database() as conn:
 conn.execute('SET TRANSACTION READ ONLY')
 require_synthetic_accounts(conn)
 rows=conn.execute("SELECT w.content->>'service_date' AS service_date FROM workdays w JOIN accounts a ON a.id=w.owner WHERE a.username=%s AND w.expires_at>clock_timestamp() ORDER BY service_date", ('synthetic-story12-manual',)).fetchall()
 print(json.dumps(rows,default=str))
"""
result = subprocess.run(compose+['exec','-T','private-api','python','-'],input=program,cwd=root,capture_output=True,text=True)
assert result.returncode == 0, 'Read-only fixture check failed'
dates = [row['service_date'] for row in json.loads(result.stdout)]
assert dates == ['2031-01-02','2031-01-03']
assert (root/'.private-runtime/story12-manual-credentials.json').is_file()
after = containers()
assert before == after
record = {'checked_at':datetime.now(timezone.utc).isoformat(),'main_at_check':head,'tested_revision':tested,'changes_since_test':changes,'classification':'documentation-and-logs-only','existing_evidence_still_applicable':True,'rebuild_required':False,'regression_rerun_required':False,'verified_evidence':verified,'runtime_matches_prior':True,'served_files':served,'manual_fixture_dates':dates,'container_metadata_unchanged':True,'container_count':len(before),'container_metadata':before,'acceptance':'Jonas sin manuelle/fysiske akseptansetest av Story 12.1 og 12.2 gjenstår. Automatiske tester innebærer ikke brukeraksept.'}
(root/'docs/evidence/12-current-main-readiness.json').write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
print(f'Readiness passed: {head[:7]}, {len(verified)} evidence records, {len(before)} unchanged containers; no data mutations.')
