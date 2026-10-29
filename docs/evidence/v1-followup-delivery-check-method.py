import hashlib
import json
import re
import subprocess
import tarfile
from pathlib import Path
from datetime import datetime, timezone

root = Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
indices = list((root/'docs/evidence/v1-followup-bundles').glob('*.index.json'))
entries = 0
for index in indices:
    expected = json.loads(index.read_text(encoding='utf-8'))
    archive = root/expected['archive']
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == expected['archive_sha256'], str(index)
    with tarfile.open(archive,'r:gz') as bundle:
        files = {member.name: member for member in bundle.getmembers() if member.isfile()}
        assert set(files) == set(expected['entries']), str(index)
        for name, sha in expected['entries'].items():
            assert hashlib.sha256(bundle.extractfile(files[name]).read()).hexdigest() == sha, str(index)+':'+name
            entries += 1
names = set(subprocess.check_output(['git','diff','--name-only','6d1259628c5fc7cec2d649e4097331d1606d9574'],cwd=root,text=True).splitlines())
names.update(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=root,text=True).splitlines())
links = 0
for name in sorted(names):
    path = root/name
    if path.suffix != '.md' or not path.is_file():
        continue
    for match in re.finditer(r'\[[^\]\n]*\]\(([^)\n]+)\)',path.read_text(encoding='utf-8')):
        target = match[1].strip().strip('<>')
        if '://' in target or target.startswith(('mailto:','#')):
            continue
        target,_,anchor = target.partition('#')
        candidate = (path.parent/target).resolve()
        assert candidate.is_file(), f'{name}: {target}'
        if re.fullmatch(r'L\d+',anchor):
            assert int(anchor[1:]) <= len(candidate.read_text(encoding='utf-8').splitlines()), f'{name}: {target}#{anchor}'
        links += 1
record = {'at':datetime.now(timezone.utc).isoformat(),'verified_bundles':len(indices),'verified_entries':entries,'checked_changed_markdown_links':links,'method_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'result':'passed; no extraction or external network'}
(root/'docs/evidence/v1-followup-delivery-check-20261029.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record))
