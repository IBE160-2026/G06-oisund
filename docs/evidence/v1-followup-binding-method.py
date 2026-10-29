"""Bind an actually executed dirty-source manifest to a later immutable commit.
Run from the candidate checkout: python tmp/bind-candidate.py COMMIT EVIDENCE.json
No test is rerun or relabelled as a clean-commit execution.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

root = Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
commit = subprocess.check_output(['git','rev-parse',sys.argv[1]+'^{commit}'],cwd=root,text=True).strip()
evidence = root/sys.argv[2]
gate = json.loads(evidence.read_text(encoding='utf-8'))
assert gate['gate_exit_code'] == 0 and gate['source_unchanged'] and gate['executed_inputs_unchanged']
tree = {}
for row in subprocess.check_output(['git','ls-tree','-rz',commit],cwd=root).split(b'\0'):
    if row:
        metadata,name = row.split(b'\t',1)
        tree[name.decode()] = metadata.split()[2].decode()
matched = {}
for name, captured in gate['source_sha256_before'].items():
    raw = (root/name).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == captured, 'captured bytes changed: '+name
    # Let Git apply its own path-specific text/binary filters; do not normalize
    # arbitrary binary fixtures or pretend CRLF materialization is a code edit.
    blob = subprocess.check_output(['git','hash-object','--path='+name,name],cwd=root,text=True,stderr=subprocess.DEVNULL).strip()
    assert tree.get(name) == blob, 'commit source differs: '+name
    matched[name] = {'executed_worktree_sha256':captured,'committed_git_blob':blob}
record = {
 'at':datetime.now(timezone.utc).isoformat(), 'candidate_commit':commit,
 'gate':str(evidence.relative_to(root)).replace('\\','/'), 'actual_HEAD_at_execution':gate['revision'],
 'claim':'The recorded dirty worktree input bytes are unchanged and Git-filter-identical to the named later commit. This is source binding, not a claim that the tests ran from a clean checkout of that commit.',
 'gate_exit_code':gate['gate_exit_code'], 'source_unchanged_during_gate':True,
 'matched_source_files':matched,
 'method_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(root/'docs/evidence/v1-followup-candidate-binding-20261029.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(f'PASS {len(matched)} exact captured inputs bound to candidate {commit}')
