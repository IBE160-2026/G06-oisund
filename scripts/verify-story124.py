"""Story 12.4 adapter for the qualified 12.3 evidence runner.

Only the named synthetic project is touched. Shared runner and original verifier
remain immutable; the exact translated integration program is bundled with each
run. No active deployment, tunnel or ordinary database commands are provided.
"""
from pathlib import Path
import hashlib
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
QUALIFIED_TEMPLATES = {
    'scripts/verify-story123.py': '3ec6ebf2787977a583ab3653fca8652b9f32dc60043cf991c429e9826b7592c8',
    'scripts/verify-story12-integration.py': 'a55b69ef5af124b8d94e20496cc7321faa7ebe6d6f06edc1128b832a254ceb20',
}


def qualified_templates():
    sources = {}
    for name, expected in QUALIFIED_TEMPLATES.items():
        # Git's canonical blobs use LF; Windows worktrees may materialize CRLF.
        # Normalize that representation alone, preserving every other byte.
        data = (ROOT/name).read_bytes().replace(b'\r\n', b'\n')
        if hashlib.sha256(data).hexdigest() != expected:
            raise RuntimeError('Qualified shared template changed: ' + name)
        sources[name] = data.decode('utf-8')
    return sources


def load_runner():
    # Execute definitions only; substituting before evaluation keeps even the
    # run-directory creation and evidence naming in our own namespace.
    source = qualified_templates()['scripts/verify-story123.py']
    for old, new in [('story123', 'story124'), ('STORY123', 'STORY124'),
                     ('15323', '15324'), ('18323', '18325'), ('18324', '18326'),
                     ('18481', '18484'), ('18483', '18484'),
                     ('12-3', '12-4'), ('12.3', '12.4')]:
        source = source.replace(old, new)
    source = source.replace("'12.2': 'accepted'", "'12.2': 'accepted', '12.3': 'accepted'")
    source = source.replace('snapshot_inputs = list(inputs) + [Path(__file__)]',
                            "snapshot_inputs = list(inputs) + [Path(__file__), ROOT/'scripts/verify-story123.py', ROOT/'scripts/verify-story12-integration.py']")
    namespace = {'__name__': 'story124_shared_runner', '__file__': __file__}
    exec(compile(source, str(ROOT / 'scripts/verify-story123.py'), 'exec'), namespace)
    return namespace


def fresh_build(tablet=False):
    # A separate evidence-recorded invocation; failure prevents browser launch.
    subprocess.run([sys.executable, str(Path(__file__).resolve()), 'tablet-build' if tablet else 'build'], cwd=ROOT, check=True)


def load_guard():
    source = qualified_templates()['scripts/verify-story12-integration.py']
    for old, new in [('ibe160-story12-integration', 'ibe160-story124-tests'),
                     ('compose.story12-integration.yaml', 'compose.story124.yaml'),
                     ('15312', '15324'), ('18312', '18325'), ('18313', '18326')]:
        source = source.replace(old, new)
    namespace = {'__name__': 'story124_guard', '__file__': str(ROOT/'scripts/verify-story12-integration.py')}
    exec(compile(source, namespace['__file__'], 'exec'), namespace)
    return namespace


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode not in ('up', 'build', 'tablet-build', 'mobile', 'browser', 'backend', 'verify', 'prepare', 'serve', 'stop-preview'):
        raise SystemExit('Use up|build|browser [spec/filter args]|mobile [filter args]|backend [pytest args]|verify|prepare|serve|stop-preview')
    if mode in ('browser', 'serve'):
        fresh_build()
    if mode == 'mobile':
        fresh_build(True)
        sys.argv[1] = 'tablet-browser'
    runner = load_runner()
    if mode in ('up', 'verify', 'prepare'):
        runner['integration']()
    elif mode in ('build', 'tablet-build'):
        tablet = mode == 'tablet-build'
        runner['execute'](runner['build_command'](tablet), ROOT/'frontend', runner['build_environment'](tablet))
    elif mode == 'mobile':
        runner['browser'](True)
    elif mode == 'browser':
        load_guard()['guard_runtime']()
        # The shared default is 12.3 visual qualification. 12.4 defaults to its
        # full actual-API journey and accepts explicit existing regression specs.
        if len(sys.argv) == 2:
            sys.argv.append('complete-user-flow.spec.ts')
        runner['browser']()
    elif mode == 'backend':
        # Guard the exact project/config/worktree/volume/account identity before
        # any test can mutate this synthetic database.
        load_guard()['guard_runtime']()
        args = sys.argv[2:] or ['tests', '--ignore=tests/test_assessment.py']
        command = ['docker', 'compose', '-p', runner['PROJECT'], '-f', 'compose.story124.yaml',
                   'exec', '-T', 'private-api', 'python', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *args]
        runner['execute'](command, inputs=[ROOT/'compose.story124.yaml', Path(__file__)])
    else:
        runner['preview']()


if __name__ == '__main__':
    main()
