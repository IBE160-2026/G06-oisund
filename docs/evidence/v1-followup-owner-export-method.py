from pathlib import Path
import hashlib
import json
import shutil
root = Path(__file__).resolve().parents[1]
run = '20261029T165949935004Z-9456009d'
gate = json.loads((root/f'docs/evidence/v1-followup-browser-{run}.json').read_text(encoding='utf-8'))
assert gate['gate_exit_code'] == 0
folder = root/'docs/evidence/v1-followup-owner-final'
folder.mkdir(exist_ok=True)
items = []
for source in sorted((root/f'tmp/v1followup/{run}/results').rglob('*.png')):
    sha = hashlib.sha256(source.read_bytes()).hexdigest()
    assert sha in gate['durable_artifact_sha256'].values()
    name = sha[:12]+'-'+source.name
    target = folder/name
    if target.exists():
        assert target.read_bytes() == source.read_bytes()
    else:
        shutil.copyfile(source,target)
    items.append({'file':name,'sha256':sha,'source_result':str(source.relative_to(root)).replace('\\','/')})
(folder/'index.json').write_text(json.dumps({'gate':f'v1-followup-browser-{run}.json','images':items},indent=2)+'\n',encoding='utf-8')
lines = ['# Final candidate owner-review images','',f'Actual desktop screenshots from the23/23 passing run `{run}`, source-bound to candidate `3c2287ed68d0cbb1923439fc6ee00254395072a4`. Exact copied bytes match the archived per-entry hashes. These are automated rendering evidence, not human acceptance or physical touch observations.','', 'Review unknown/current versus rejected facts, explicit abandonment feedback, distinct repeated-hour offsets and the explicitly syntheticA7 examples. Full criteria and pending decisions are in the [qualification ledger](../../submission/v1-followup-qualification.md).','']
for name in dict.fromkeys(item['file'] for item in items):
    lines.append(f'- [{name.split("-",1)[1]}]({name})')
(folder/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f'Exported {len(items)} exact screenshot copies from final passing gate')
