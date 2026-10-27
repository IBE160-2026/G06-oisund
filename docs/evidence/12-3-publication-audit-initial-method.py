from pathlib import Path
import json,hashlib,subprocess,tarfile,datetime
root=Path('.').resolve();story=Path('D:/IBE160/tmp/story-12-3');h=lambda b:hashlib.sha256(b).hexdigest()
merge=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],text=True).strip();branch=subprocess.check_output(['git','rev-parse','story/12-3-tablet-pc-accessibility'],text=True).strip();assert tree==subprocess.check_output(['git','rev-parse','story/12-3-tablet-pc-accessibility^{tree}'],text=True).strip()
assert subprocess.check_output(['git','diff','--name-only','8ca318b','HEAD','--','frontend','backend','scripts','deploy','compose.story123.yaml','compose.tablet.yaml','.dockerignore'],text=True).strip()==''
manifest=json.loads((story/'.private-runtime/story123-build.json').read_text(encoding='utf-8'))
for p,digest in manifest['source'].items():assert h((root/p).read_bytes())==digest,p
for p,digest in manifest['built'].items():assert h((story/p).read_bytes())==digest,p
raw={};requests=[];expected={}
for name in ['12-3-device-20261027T200011Z','12-3-device-final-20261027T205355Z']:
 base=root/'docs/evidence'/name;idx=json.loads(base.with_suffix('.index.json').read_text(encoding='utf-8'));assert h((root/idx['archive']).read_bytes())==idx['archive_sha256']
 with tarfile.open(root/idx['archive']) as arc: assert {m.name:h(arc.extractfile(m).read()) for m in arc.getmembers() if m.isfile()}==idx['entries']
 for file,digest in idx['entries'].items():
  p=f'docs/evidence/{name}/{file}';assert h((root/p).read_bytes())==digest,p;requests.append('HEAD:'+p);expected['HEAD:'+p]=digest
 raw[name]={'entries':len(idx['entries']),'archive_sha256':idx['archive_sha256'],'working_and_archive_bytes':'identical'}
proc=subprocess.run(['git','cat-file','--batch'],input=('\n'.join(requests)+'\n').encode(),stdout=subprocess.PIPE,check=True);data=proc.stdout;offset=0
for request in requests:
 end=data.index(b'\n',offset);header=data[offset:end].split();assert header[1]==b'blob';size=int(header[2]);blob=data[end+1:end+1+size];assert h(blob)==expected[request],request;offset=end+size+2
status=(root/'_bmad-output/implementation-artifacts/sprint-status.yaml').read_text(encoding='utf-8');assert '12-3-use-the-included-views-on-tablet-and-pc: done' in status and '12-4-verify-the-complete-user-flow: backlog' in status
runtime=json.loads((root/'docs/evidence/12-3-publication-runtime.json').read_text());assert runtime['mainMerge']==merge
result={'observed':datetime.datetime.now(datetime.timezone.utc).isoformat(),'main_merge':merge,'story_commit':branch,'accepted_tree':tree,'merge_tree_exactly_equals_story_tree':True,'product_diff_since_8ca318b':[],'main_source_hashes_match_tested_manifest':len(manifest['source']),'isolated_test_build_hashes_unchanged':len(manifest['built']),'raw_evidence':raw,'git_committed_raw_blobs_match_indices':len(requests),'fresh_final_tests':{'typescript_no_emit':'passed','python_build_environment':'4/4','node_tooling_configuration':'2/2'},'runtime':'12-3-publication-runtime.json','story_status':'done/accepted','next_story':'12.4 backlog','qualification_scope':'Unchanged product tree; prior accepted story and physical tests retained. No new broad browser/backend run; no rewrite of historical477/479.'}
(root/'docs/evidence/12-3-publication-final.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result))
