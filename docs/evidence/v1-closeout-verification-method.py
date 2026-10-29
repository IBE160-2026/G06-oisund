"""Documentation-only closeout audit. Run from repo root; never operates services."""
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path.cwd()
OUTPUT = ROOT / 'docs/evidence/v1-closeout-verification-2026-10-29.json'
BASELINE = ROOT / 'tmp/v1-closeout/baseline.json'
DOCUMENTS = [
    'README.md',
    '_bmad-output/planning-artifacts/epics.md',
    '_bmad-output/planning-artifacts/prds/prd-IBE160-2026-09-21/prd.md',
    '_bmad-output/implementation-artifacts/epic-12-context.md',
    '_bmad-output/implementation-artifacts/epic-12-retro-2026-10-29.md',
    '_bmad-output/implementation-artifacts/deferred-work.md',
    'docs/submission/README.md',
    'docs/submission/traceability.md',
    'docs/submission/known-issues.md',
    'docs/submission/v1-closeout.md',
]


def git(*args):
    return subprocess.check_output(['git', '--no-optional-locks', *args], encoding='utf-8').strip()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
    checked = []
    for name in DOCUMENTS:
        file = ROOT / name
        for target in re.findall(r'\]\(([^)]+)\)', file.read_text(encoding='utf-8')):
            if target.startswith(('http:', 'https:', '#')):
                continue
            location, _, fragment = target.partition('#')
            path = (file.parent / location).resolve()
            assert path == OUTPUT or path.exists(), (name, target)
            if re.fullmatch(r'L\d+', fragment):
                assert int(fragment[1:]) <= len(path.read_text(encoding='utf-8').splitlines()), (name, target)
            checked.append({'document': name, 'target': target})

    yaml = YAML(typ='safe')
    status = yaml.load((ROOT / '_bmad-output/implementation-artifacts/sprint-status.yaml').read_text(encoding='utf-8'))
    stories = {k: v for k, v in status['development_status'].items() if re.match(r'^\d+-\d+-', k)}
    assert len(stories) == 20 and set(stories.values()) == {'done'}
    assert status['development_status']['epic-12'] == 'in-progress'
    assert status['development_status']['epic-12-retrospective'] == 'done'
    actions = {a['id']: a for a in status['action_items']}
    expected = {
        'epic-11-retro-item-2-refresh-comparison-adoption': 'done',
        'epic-11-retro-item-12-carry-cross-story-invariants': 'done',
        'epic-11-retro-item-7-validate-source-and-lifetime-journeys': 'in-progress',
        'epic-11-retro-item-8-retain-execution-evidence': 'in-progress',
        'epic-12-retro-item-1-reconcile-current-documentation': 'done',
        'epic-12-retro-item-2-review-whole-flow-before-final-gate': 'open',
    }
    assert all(actions[k]['status'] == value for k, value in expected.items())
    original = yaml.load(git('show', baseline['head'] + ':_bmad-output/implementation-artifacts/sprint-status.yaml'))
    original_actions = {a['id']: a for a in original['action_items']}
    assert set(actions) == set(original_actions) | {
        'epic-12-retro-item-1-reconcile-current-documentation',
        'epic-12-retro-item-2-review-whole-flow-before-final-gate',
    }
    for key, before in original_actions.items():
        wanted = dict(before)
        if key in expected:
            wanted['status'] = expected[key]
        assert actions[key] == wanted, key
    for k in ('epic-11-retro-item-1-terminal-plan-recovery', 'epic-11-retro-item-3-settle-known-rejections', 'epic-11-retro-item-5-disambiguate-oslo-notice-times'):
        assert actions[k]['status'] == 'open'

    unchanged_history = all(sha(ROOT / name) == digest for name, digest in baseline['historicalEvidence'].items())
    assert unchanged_history
    other_worktrees = []
    for before in baseline['worktrees']:
        after = {'path': before['path'], 'head': git('-C', before['path'], 'rev-parse', 'HEAD'), 'status': git('-C', before['path'], 'status', '--porcelain=v1')}
        assert after == before, before['path']
        other_worktrees.append(after)

    executable_paths = ['backend', 'frontend', 'scripts', 'deploy', 'Eksempelfiler', 'compose.submission.yaml', '.dockerignore']
    changed_executable = git('diff', '--name-only', 'c067fdbb20150219c041588ed4e990e7b0ef6b94', '--', *executable_paths)
    assert not changed_executable, changed_executable
    result = {
        'at': datetime.now(timezone.utc).isoformat(),
        'checkedHead': git('rev-parse', 'HEAD'),
        'fetchedOriginMainAtStart': baseline['originMain'],
        'sourceSnapshot': 'c067fdbb20150219c041588ed4e990e7b0ef6b94',
        'all20StoriesDone': True,
        'epic12HeldInProgress': True,
        'retroDone': True,
        'confirmedAndDocumentationStatuses': expected,
        'allOtherEarlierActionFieldsUnchanged': True,
        'pendingDecisions': ['D1', 'D2', 'D3', 'formal-closure'],
        'noDeferralsApprovedByAssessment': True,
        'localLinksChecked': len(checked),
        'allLocalLinksAndLineBoundsExist': True,
        'historicalEvidenceFilesUnchanged': len(baseline['historicalEvidence']),
        'otherWorktreesUnchanged': other_worktrees,
        'executableFixtureAndConfigDifferencesFromSnapshot': [],
        'freshProductTestsExecuted': [],
        'serviceOrDatabaseCommandsExecuted': [],
        'runtimeQualification': 'No current runtime-state claim; no service, database, tunnel or account operated.',
        'documentationHashes': {p: sha(ROOT / p) for p in DOCUMENTS},
        'e12A1StatusUpdate': json.loads((ROOT / 'tmp/v1-closeout/status-update.json').read_text(encoding='utf-8')),
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['all20StoriesDone', 'epic12HeldInProgress', 'localLinksChecked', 'historicalEvidenceFilesUnchanged', 'noDeferralsApprovedByAssessment']}))


if __name__ == '__main__':
    main()
