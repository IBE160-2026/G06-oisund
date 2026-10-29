import hashlib
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

root = Path(__file__).resolve().parents[1]
baseline = '6d1259628c5fc7cec2d649e4097331d1606d9574'
names = subprocess.check_output(['git','ls-tree','-r','--name-only',baseline,'--','docs/evidence'],cwd=root,text=True).splitlines()
raw_identical = 0
crlf_only = 0
for name in names:
    candidate = (root/name).read_bytes()
    preserved = (Path('D:/IBE160')/name).read_bytes()
    if candidate == preserved:
        raw_identical += 1
    else:
        assert candidate.replace(b'\r\n',b'\n') == preserved.replace(b'\r\n',b'\n'), name
        crlf_only += 1
subprocess.run(['git','diff','--exit-code',baseline,'--','docs/evidence'],cwd=root,check=True,capture_output=True)
before = json.loads((root/'tmp/preservation-before.json').read_text(encoding='utf-8'))
after = json.loads((root/'tmp/preservation-after.json').read_text(encoding='utf-8'))
fields = ['worktrees','otherContainers','otherVolumes']
assert all(before[field] == after[field] for field in fields)
result = {
 'at': datetime.now(timezone.utc).isoformat(), 'baseline': baseline,
 'historical_evidence_tracked_files_unchanged_in_git_diff': len(names),
 'raw_bytes_identical_to_main_worktree': raw_identical,
 'only_checkout_CRLF_representation_differs': crlf_only,
 'checkout_representation': 'core.autocrlf=true; differing worktree text bytes normalize only CRLF to LF. No historical tracked evidence diff; original Git blobs and binary artifacts preserved.',
 'other_worktrees': len(after['worktrees']), 'other_containers': len(after['otherContainers']), 'other_volumes': len(after['otherVolumes']),
 'preservation': 'unchanged stable identities/state/start/PID/mounts/volume metadata and other worktree HEAD/status',
 'not_claimed': 'RestartCount was not captured at baseline; rolling health logs are not compared. No content-level database audit or global Docker-start neutrality is claimed. Owner manually started Docker after explicit restart-policy disclosure/authorization.',
 'before_at': before['at'], 'after_at': after['at'],
 'before_sha256': hashlib.sha256((root/'tmp/preservation-before.json').read_bytes()).hexdigest(),
 'after_sha256': hashlib.sha256((root/'tmp/preservation-after.json').read_bytes()).hexdigest(),
 'method_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(root/'docs/evidence/v1-followup-preservation-20261029.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
