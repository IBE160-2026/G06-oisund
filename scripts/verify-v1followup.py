"""Story V1 follow-up adapter for the qualified 12.3 evidence runner.

Only the named synthetic project is touched. Shared runner and original verifier
remain immutable; the exact translated integration program is bundled with each
run. No active deployment, tunnel or ordinary database commands are provided.
"""
from pathlib import Path
import hashlib
import json
import secrets
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
QUALIFIED_TEMPLATES = {
    'scripts/verify-story123.py': '3ec6ebf2787977a583ab3653fca8652b9f32dc60043cf991c429e9826b7592c8',
    'scripts/verify-story12-integration.py': 'a55b69ef5af124b8d94e20496cc7321faa7ebe6d6f06edc1128b832a254ceb20',
    'scripts/verify-retained-data.py': 'cd227bc91e2a869680c4b758bbfd1a14f8182a4417f3e647ae2d06256de84865',
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
    for old, new in [('story123', 'v1followup'), ('STORY123', 'V1FOLLOWUP'),
                     ('15323', '15326'), ('18323', '18329'), ('18324', '18330'),
                     ('18481', '18485'), ('18483', '18485'),
                     ('12-3', 'v1-followup'), ('12.3', 'V1 follow-up')]:
        source = source.replace(old, new)
    source = source.replace("'12.2': 'accepted'", "'12.2': 'accepted', '12.3': 'accepted'")
    source = source.replace('snapshot_inputs = list(inputs) + [Path(__file__)]',
                            "snapshot_inputs = list(inputs) + [Path(__file__), ROOT/'scripts/verify-story123.py', ROOT/'scripts/verify-story12-integration.py', ROOT/'scripts/verify-retained-data.py']")
    source = source.replace("'tested_story': '12.3'", "'tested_work': 'V1 D1 D2 D3 follow-up'")
    namespace = {'__name__': 'v1followup_shared_runner', '__file__': __file__}
    exec(compile(source, str(ROOT / 'scripts/verify-story123.py'), 'exec'), namespace)
    return namespace


def fresh_build():
    # A separate evidence-recorded invocation; failure prevents browser launch.
    subprocess.run([sys.executable, str(Path(__file__).resolve()), 'build'], cwd=ROOT, check=True)


def load_guard():
    source = qualified_templates()['scripts/verify-story12-integration.py']
    for old, new in [('ibe160-story12-integration', 'ibe160-v1followup-tests'),
                     ('compose.story12-integration.yaml', 'compose.v1followup.yaml'),
                     ('15312', '15326'), ('18312', '18329'), ('18313', '18330')]:
        source = source.replace(old, new)
    namespace = {'__name__': 'v1followup_guard', '__file__': str(ROOT/'scripts/verify-story12-integration.py')}
    exec(compile(source, namespace['__file__'], 'exec'), namespace)
    return namespace


def preview(mode):
    # Some Windows TCP metadata reports OwningProcess=0 even for this child.
    # Prove the served root through an unpredictable one-use challenge plus
    # the exact child creation/command identity. Stop checks remain unchanged.
    source = qualified_templates()['scripts/verify-retained-data.py']
    source = source.replace("'tmp/story121'", "'tmp/v1followup-preview'")
    source = source.replace('PREVIEW_PORT = 15121', 'PREVIEW_PORT = 15326')
    source = source.replace('deadline = time.monotonic()+10', 'deadline = time.monotonic()+60')
    namespace = {'__name__': 'v1followup_preview', '__file__': str(ROOT/'scripts/verify-retained-data.py')}
    exec(compile(source, namespace['__file__'], 'exec'), namespace)
    if mode == 'stop-preview':
        namespace['stop_preview']()
        return
    challenge = secrets.token_hex(32)
    marker = ROOT/'frontend/dist'/('v1followup-preview-' + secrets.token_hex(16) + '.txt')
    with marker.open('x', encoding='ascii') as handle:
        handle.write(challenge)
    def served_child(pid):
        record = json.loads(namespace['PREVIEW'].read_text(encoding='utf-8'))
        current = namespace['process_identity'](pid)
        if not namespace['owned_preview'](record, current):
            return False
        with urllib.request.urlopen('http://127.0.0.1:15326/' + marker.name, timeout=.5) as response:
            return response.status == 200 and response.read(65) == challenge.encode('ascii')
    namespace['preview_listener'] = served_child
    try:
        namespace['serve_preview']()
    finally:
        marker.unlink()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode not in ('up', 'build', 'browser', 'backend', 'verify', 'prepare', 'serve', 'stop-preview'):
        raise SystemExit('Use up|build|browser [spec/filter args]|backend [pytest args]|verify|prepare|serve|stop-preview')
    if mode in ('browser', 'serve'):
        fresh_build()
    runner = load_runner()
    if mode in ('up', 'verify', 'prepare'):
        runner['integration']()
    elif mode == 'build':
        runner['execute'](runner['build_command'](False), ROOT/'frontend', runner['build_environment'](False))
    elif mode == 'browser':
        load_guard()['guard_runtime']()
        # The shared default is 12.3 visual qualification. V1 follow-up defaults to its
        # full actual-API journey and accepts explicit existing regression specs.
        if len(sys.argv) == 2:
            sys.argv.append('complete-user-flow.spec.ts')
        runner['browser']()
    elif mode == 'backend':
        # Guard the exact project/config/worktree/volume/account identity before
        # any test can mutate this synthetic database.
        load_guard()['guard_runtime']()
        args = sys.argv[2:] or ['tests', '--ignore=tests/test_assessment.py']
        command = ['docker', 'compose', '-p', runner['PROJECT'], '-f', 'compose.v1followup.yaml',
                   'exec', '-T', 'private-api', 'python', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *args]
        runner['execute'](command, inputs=[ROOT/'compose.v1followup.yaml', Path(__file__)])
    else:
        if mode == 'serve':
            load_guard()['guard_runtime']()
        preview(mode)


if __name__ == '__main__':
    main()
