"""Validate reused receipts/source identity and index this bounded qualification."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
from night_controls import ROOT, OUT


def run(args):
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


if __name__ == '__main__':
    production = '5e521cbc658594a47c4568d352a50e46309573c4'
    assert not run(['git', 'diff', production, '--', 'backend', 'frontend',
        'deploy/tablet/nginx-main.conf', 'deploy/tablet/nginx.conf.template'])
    historical = ROOT/'docs/evidence/o6-execution-20261101/staged-http-families.txt'
    data = historical.read_bytes()
    receipt = json.loads(historical.with_suffix('.json').read_text())
    assert hashlib.sha256(data).hexdigest() == receipt['sha256']
    reused, _ = json.JSONDecoder().raw_decode(data.decode())
    assert reused['passed'] and len(reused['families']) == 15
    for family in reused['families']:
        assert len(family['negative_controls']) == 5
        assert all(row['status'] == 403 and row['all_non_session_tables_unchanged'] for row in family['negative_controls'])
        assert family['before_dispatch_loss_unchanged']
        assert family['receipt_recovered'] and family['exact_replay_no_second_effect']
        assert family['accepted_reply_dropped']['status'] == 200 and family['accepted_reply_dropped']['no_store']
    result = json.loads((OUT/'qualification-r6.json').read_text())
    assert result['exit'] == 0
    assert hashlib.sha256((OUT/'qualification-r6.txt').read_bytes()).hexdigest() == result['sha256']
    assert b'37 passed' in (OUT/'qualification-r6.txt').read_bytes()
    assert b'4 passed' in (OUT/'receipt-final.txt').read_bytes()
    assert b'Ran 20 tests' in (OUT/'operations-regression-linux-r2.txt').read_bytes()
    assert b'OK' in (OUT/'operations-regression-linux-r2.txt').read_bytes()
    images = {}
    refs = ['bussassistent-access-gate:'+production, 'ibe160-o5-gate:20261102', 'ibe160-o5-gate-tests:20261102']
    for image in refs:
        images[image] = dict(id=run(['docker','image','inspect','--format','{{.Id}}', image]),
            layers=json.loads(run(['docker','image','inspect','--format','{{json .RootFS.Layers}}', image])))
    base, candidate, tests = (images[ref] for ref in refs)
    assert candidate['layers'][:-1] == base['layers']
    assert tests['layers'][:len(candidate['layers'])] == candidate['layers']
    gate_sha = hashlib.sha256((ROOT/'deploy/tablet/access_gate/gate.py').read_bytes()).hexdigest()
    actual_sha = run(['docker','run','--rm','--pull','never','--name','ibe160-o5-source-identity',
        '--network','none','--read-only','--cap-drop','ALL',refs[1], 'sha256sum','/gate/gate.py']).split()[0]
    assert actual_sha == gate_sha
    assert not run(['docker','ps','-aq','--filter','name=ibe160-o5'])
    summary = dict(time_utc=datetime.now(timezone.utc).isoformat(),
        branch=run(['git','branch','--show-current']), origin_main=run(['git','rev-parse','origin/main']),
        production_release_read_only=production, v1_tag=run(['git','rev-parse','v1.0.0^{commit}']),
        unchanged_app_and_proxy_sources=True, reused_o3=dict(source=str(historical.relative_to(ROOT)),
            output_sha256=receipt['sha256'], families=15, negative_origin_csrf_controls=75,
            before_dispatch_and_after_commit_loss_receipt_replay=True, scope='isolated historical actual production runtime image'),
        images=images, candidate_exact_gate_source_sha256=gate_sha,
        new_gate_qualification_passed=37, final_receipt_tests_passed=4, linux_operations_tests_passed=20,
        own_test_containers_remaining=0, production_deployed=False,
        external_authenticated_matrix=False, independent_wan_vantage=False,
        firewall_read_requires_interactive_sudo=True, o6_closed=False)
    with (OUT/'qualification-summary-final.json').open('x', encoding='utf-8') as output:
        json.dump(summary, output, indent=2)
    paths = [*OUT.glob('*'), ROOT/'deploy/tablet/access_gate/gate.py',
        *ROOT.glob('deploy/tablet/access_gate/test*.py'),
        ROOT/'compose.tablet.yaml', ROOT/'deploy/ubuntu/compose.yaml',
        *ROOT.glob('scripts/operations-followup/*night*.py'), ROOT/'scripts/operations-followup/run_o5_tests.py']
    with (OUT/'index-final.json').open('x', encoding='utf-8') as output:
        json.dump({str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths if p.is_file() and p.name != 'index.json'}, output, indent=2)
    print('PASS reused O3, immutable runtime lineage, candidate source, qualification and cleanup')
