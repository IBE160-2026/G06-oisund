from pathlib import Path
root=Path('.')
def edit(path, old, new):
 p=root/path
 s=p.read_text(encoding='utf-8')
 if old not in s: raise RuntimeError(f'Missing expected text in {path}: {old[:60]}')
 p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
report='docs/evidence/12-3-device-acceptance-2026-10-27.md'
for name in ['spec-12-3-tablet-pc.md','spec-12-3-current-main-sync.md']:
 p='_bmad-output/implementation-artifacts/'+name
 edit(p,'status: in-review','status: done')
 edit(p,'owner_acceptance: pending','owner_acceptance: accepted\naccepted_on: 2026-10-27\nacceptance_evidence: ../../'+report)
 s=(root/p).read_text(encoding='utf-8'); pos=s.index('\n---',4)+4
 s=s[:pos]+'\n\n> Final owner decision, 27 October 2026: **done/accepted**. Jonas approved personal Lenovo/Brave readability and touch comfort and conditionally granted overall acceptance. All remaining required checks passed; see [final device acceptance](../../'+report+'). Earlier frozen scope/pending statements below are historical. His latest no-commit/no-push instruction overrides earlier publication permissions; no main merge or12.4 work.\n'+s[pos:]
 (root/p).write_text(s,encoding='utf-8',newline='\n')
edit('_bmad-output/planning-artifacts/story-drafts/story-v1-18.md','status: review','status: done')
edit('_bmad-output/planning-artifacts/story-drafts/story-v1-18.md',"**Stable alias:** V1-18. **Status:** review; technical implementation and evidence recorded; Jonas' manual acceptance is pending.","**Stable alias:** V1-18. **Status:** done/accepted, 27 October 2026. Jonas approved physical readability/touch comfort and conditional overall acceptance; remaining required checks passed. See [final acceptance evidence](../../../"+report+"). No commit/push/main merge;12.4 remains backlog.")
edit('_bmad-output/planning-artifacts/epics.md',"**Stable alias:** V1-18. **Status:** review; technical implementation/evidence in [12.3 specification](../implementation-artifacts/spec-12-3-tablet-pc.md); Jonas' manual acceptance and physical qualification remain pending.","**Stable alias:** V1-18. **Status:** done/accepted,27 October2026. Jonas' conditional approval became effective after remaining required physical checks passed; [final acceptance evidence](../../"+report+"). No main merge/commit/push;12.4 remains backlog.")
p='_bmad-output/implementation-artifacts/sprint-status.yaml'
edit(p,'12-3-use-the-included-views-on-tablet-and-pc: review # Current-main integration; Jonas acceptance pending.','12-3-use-the-included-views-on-tablet-and-pc: done # Jonas conditional acceptance effective 2026-10-27 after remaining required Lenovo checks passed; device-acceptance report. No merge/commit/push.')
edit(p,'last_updated: 10-27-2026 11:02','last_updated: 10-27-2026 22:02')
s=(root/p).read_text(encoding='utf-8').replace('status: done # Technically verified in 12.3; Jonas story acceptance remains pending.','status: done # Technically verified; Jonas accepted 12.3 on 2026-10-27 after required Lenovo checks.')
for item in ['epic-10-retro-item-5-record-ipad-verification','epic-11-retro-item-9-reconcile-tablet-qualification']:
 start=s.index('  - id: "'+item+'"'); end=s.find('  - id:',start+1)
 if end<0: end=len(s)
 block=s[start:end].replace('status: open','status: done # Current Lenovo/Brave included-view obligation satisfied; final device acceptance report. Wider deployment/12.4 remain separate.')
 s=s[:start]+block+s[end:]
s=s.replace('# Jonas accepted Story 12.1 and 12.2 on 2026-10-27 after manual testing and correction retest. Story 12.3 remains review/pending; current physical qualification remains separate.','# Jonas accepted 12.1/12.2 on 2026-10-27. Conditional 12.3 acceptance became effective after remaining required Lenovo checks passed; see docs/evidence/12-3-device-acceptance-2026-10-27.md. Broader deployment/AT limits remain explicit;12.4 backlog.')
(root/p).write_text(s,encoding='utf-8',newline='\n')
p='docs/story-12-3-manual-testing.md'
edit(p,"**Story 12.3 owner acceptance: pending.** Jonas accepted 12.1 and 12.2 on 27 October 2026; both are done/accepted. 12.3 remains in review until his explicit approval. Automated desktop results do not qualify physical Lenovo Pad / Android / Brave use.","**Story 12.3: done/accepted,27 October2026.** Jonas approved personal Lenovo/Brave readability and touch comfort, and granted conditional overall acceptance. The remaining required device checks passed, making that approval effective; see [final decision and evidence](evidence/12-3-device-acceptance-2026-10-27.md). No further mandatory owner action.12.1/12.2 remain accepted;12.4 backlog. Latest instruction prohibits commit/push; no merge was performed.")
edit(p,'These are partial device results, not overall owner acceptance.','That report is the earlier partial checkpoint; the [final private-flow/glyph/focus follow-up](evidence/12-3-device-acceptance-2026-10-27.md) now completes the required scope and records owner acceptance.')
edit(p,"Do not repeat the generic checklist below wholesale: use the report's completed-scope table. Remaining owner work is personal reading/touch comfort and explicit12.3 acceptance; if relevant, assistive technology/OS magnification/hardware keyboard. Private review/terminal recap and individual native glyph-contrast limits are explicitly unperformed. Earlier desktop-only limitations below describe that checkpoint and are superseded only for the exact scopes recorded in the device report. USB reverse15323/18323/18324 accesses this build, independently of the older remote pilot.","Do not repeat completed checks. Private review/confirmation, ended/aborted private recap, native glyph pixels in both themes, actual keyboard focus and final logout/privacy now passed on the same8ca318b product. TalkBack/hardware keyboard/OS magnification/Brave text-size settings remain untested compatibility coverage, not extra prerequisites under the actual story criteria. Earlier pending/hardware limits below describe prior checkpoints; only specifically evidenced coverage is superseded. USB reverse15323/18323/18324 accesses this build independently of the old remote pilot. No ordinary HTTPS/mobile-network deployment qualification is inferred.\n\nFor optional later inspection: log in to the existing synthetic account in `/private`; open5January2031 for ended recap (one completed/one unregistered) or6January2031 for aborted recap (both unregistered), switch Day/Night and reload/reopen. Expect the same server facts, read-only controls and theme. These additive device fixtures leave2/3January manual plans intact. Credentials remain in the ignored local file described below; do not put them in reports.")
edit(p,'## Short checklist','## Reusable replay checklist (not outstanding acceptance work)\n\nThe unchecked boxes below are a blank template for a future independent replay. They do not supersede the completed scope/evidence above and are not a request for Jonas to repeat it.')
p='README.md'
edit(p,"This story is implemented on its separate story branch and awaits Jonas' manual acceptance.","Story12.3 is done/accepted on its separate story branch: Jonas' conditional approval became effective after the remaining required physical checks passed on27October2026. See the [final Lenovo acceptance report]("+report+"). Latest instruction: no commit/push; no merge to main.")
edit(p,'Personal use/owner acceptance, assistive-technology and individual native-glyph limits remain explicit.','The final follow-up adds private review/confirmation, ended/aborted recap, native glyph contrast and keyboard focus; Jonas approves subjective readability/touch comfort. Untested assistive-technology/OS settings and ordinary deployment limits remain explicit.')
edit(p,'Story 12.3 remains review/pending and 12.4 remains backlog.','Story12.3 is now accepted under the final device decision;12.4 remains backlog. Main is unchanged and no story-to-main merge occurred.')
for p in ['docs/evidence/12-3-main-sync-handoff.md','docs/evidence/12-3-device-testing-2026-10-27.md']:
 s=(root/p).read_text(encoding='utf-8'); i=s.index('\n')
 s=s[:i]+'\n\n> Later final decision,27 October2026: [remaining required device checks passed and conditional owner approval became effective](12-3-device-acceptance-2026-10-27.md).12.3 is done/accepted. Pending/unperformed statements below describe this earlier checkpoint; original results/failures remain unchanged. No commit/push/main merge in the final follow-up.\n'+s[i:]
 (root/p).write_text(s,encoding='utf-8',newline='\n')
p='.logs/jonas-oisund/issues.md';s=(root/p).read_text(encoding='utf-8');lines=s.splitlines()
for i,line in enumerate(lines):
 if line.startswith('- [ ]') and any(x in line for x in ['— E11-A9:','— E10-A5:','— Jonas sin samlede personlige vurdering']):
  lines[i]=line.replace('- [ ]','- [x]',1)+' (løst2026-10-27 for12.3: Jonas godkjente lesbarhet/treffkomfort og betinget samlet aksept; resterende påkrevde private flyter/native glyfer/fokus bestod. Akseptvilkårene er oppfylt, se docs/evidence/12-3-device-acceptance-2026-10-27.md. Tidligere gjenstår-tekst er historikk; uprøvd hjelpeteknologi/OS-innstillinger og ordinær deploy er ikke registrert som bestått.12.4 forblir backlog.)'
 if line.startswith('- [x]') and any(x in line for x in ['— E11-A4:','— E10-A4:']):
  lines[i]=line+' (samlet12.3-aksept registrert2026-10-27 etter at betingede vilkår ble oppfylt.)'
(root/p).write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
print('Updated acceptance, checklist, status, handoffs and existing issue closures; no Git mutation.')
