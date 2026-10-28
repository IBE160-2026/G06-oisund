---
title: '12.4 Owner follow-up: a direct shift preparation flow'
type: bugfix
created: 2026-10-28
status: in-review
route: dispatch
baseline_commit: c884ade743edcc3739086703748ac22d45d2a695
owner_acceptance: explicitly-not-approved
review_loop_iteration: 1
context: []
---

<frozen-after-approval reason="Owner explicitly requested these corrections within Story12.4; original autonomous implementation and branch delivery authorization persists">

## Intent

**Problem:** All six guided device checks passed, but the owner explicitly refused Story12.4 acceptance because preparing a shift repeats the same document review three or four times, forces editing even when correct, hides bus saving, and sends the user to the page top after saving.

**Approach:** Present one import summary with an explicit correct-as-is save/continue action and an explicit correction/addition path. Separate editing from final decisions so users reach approval directly. Provide a dedicated save button beside bus editing in both draft and confirmed-day contexts. Keep save feedback local and preserve the editing position.

## Boundaries & Constraints

**Always:** Continue `story/12-4-complete-user-flow` in `D:/IBE160/tmp/story-12-4`. Use only isolated synthetic accounts/data on15324/18325/18326, compose project `ibe160-story124-tests`. Preserve imported source facts, corrections, unknowns, ownership, fixed retention, explicit persistence, revision checks, original-operation recovery and explicit start. Unknowns/classification remain explicit decisions; final saved revision remains server-authoritative. Keep the original12.4 specification/evidence as historical context. Owner acceptance is withheld.

**Never:** Modify active site/tunnel/operational database, private PDFs or owner's device test records; merge, deploy, start12.5 or mark acceptance. Do not auto-save on upload, navigation, access restore, errors or render. Do not auto-check unknown acknowledgements or automatically start a shift. No backend contract/migration change is required.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Correct PDF | Imported synthetic facts, no corrections | Summary offers explicit save-and-continue; no editor traversal; final decisions reached directly, full facts available on demand | Upload alone writes no draft; failed save never confirms or advances |
| Correction | User chooses editing | Edit then explicitly save; retain scroll/focus position and local saved feedback; direct action reaches separate approval | Dirty/unresolved times cannot bypass save; changing saved revision invalidates old review |
| Approval | Saved current revision | No mandatory repeated full detail list; show compact identity and required unknown/type decisions with optional full details | Existing blockers, expiry, stale revision and lost confirmation preserve original recovery |
| Draft bus | Dedicated button by field | Explicitly save bus with honest scope; do not silently persist unrelated edited fields or lose their values | If other edits prevent bus-only persistence, explain locally and require explicit whole-draft save; errors retain input and recovery |
| Confirmed bus | Existing independent bus registration | Dedicated save remains adjacent/obvious and keeps revision/recovery protection | Ended/read-only cannot save; conflict never discards proposal |
| Interrupted session | Either file/access order, logout/switch/expiry | Existing bounded bytes and denied continuation remain intact | No hidden auto-save; private state clearing remains authoritative |

</frozen-after-approval>

## Code Map

- `frontend/src/PrivateImport.tsx`: current SourceFacts summary and one adopt-only action. Preserve file read/access/error code; add explicit action intent without treating import response as saved.
- `frontend/src/PrivateDrafts.tsx`: screen union, adopt(), save()/acknowledge()/settle() and dirty/time state. adopt() currently always focuses top heading. Keep reopen focus, remove save-induced top jump. Split approval presentation from form while retaining reachable pending/comparison controls.
- `frontend/src/PrivateConfirmation.tsx`: server review validates saved draft and obtains original confirmation operation. Currently repeats Facts fully below editor. Reuse all validation and recovery; show optional full facts and keep required decisions visible.
- `frontend/src/PrivateBus.tsx`: existing independent confirmed bus save. Keep authority, read-only and second-change checks.
- `frontend/src/PrivateWorkdayView.tsx`: preserve the existing notice-reader entry/ref and ordinary day placement; during activity consultation place it after activity facts to satisfy the unchanged768px geometry bound.
- `frontend/tests/complete-user-flow.spec.ts`, `private-import.spec.ts`, `private-confirmation.spec.ts`, `private-drafts.spec.ts`, `private-bus.spec.ts`, `private-recovery.spec.ts`, `tablet-transport.spec.ts`: reuse real-API tests; adapt selectors only where intended UI changes, preserve semantic assertions. Add focused actual integration coverage for new direct and correction paths/scroll/bus-save/failed save; use independently authored fixture facts, not parser as sole oracle.
- `scripts/verify-story124.py`, `scripts/prepare-story124-tests.mjs`, `frontend/playwright.story124.config.ts`: existing guarded disposable test translation; do not change immutable source templates or touch other stacks. Explicit spec arguments required when passing browser flags.

## Tasks & Acceptance

- [x] `frontend/src/PrivateImport.tsx`, `PrivateDrafts.tsx`, `PrivateConfirmation.tsx`, `PrivateBus.tsx`: implement cohesive flow above without changing persistence contracts.
- [x] `frontend/tests/shift-preparation.spec.ts` and affected existing tests: cover matrix behavior against actual API/PostgreSQL; build and run focused tests with existing guarded runner. Never use/reset device accounts; existing test helper manages its own isolated account.
- [x] `docs/evidence/12-4-import-experience.md`, main12.4 spec, manual checklist and session log/issues: record exact new results, failures, builds, owner refusal and remaining retest. Root handles final documentation, review and delivery; implementation agent may append its notes here and owns frontend changes/tests only.

**Acceptance Criteria:**
- Given a correct PDF summary, when the user explicitly saves and continues, then approval is reachable without entering the editor and nothing is saved before that action.
- Given corrections, when a draft is saved, then the current position is retained and approval is reachable directly without a long scroll or mandatory repeated facts.
- Given either bus editing location, when shown, then a dedicated adjacent save action clearly explains what persists and preserves unrelated proposals.
- Given failure, stale state, session change or unknown facts, when continuing, then existing explicit authority/recovery/decision requirements still hold.

## Implementation Notes

No unresolved intent gap or irreversible operation. User offered two acceptable solutions (separate page or direct approval navigation); choose distinct approval screen. Footprint is frontend presentation plus meaningful integration tests and documentation. Preserve existing test/physical evidence as qualifications of earlier source, not this new UI. All six owner checks passed on the earlier build; the story is expressly not approved.

## Spec Change Log

Review loop1: owner intent is unchanged. Blind1/Edge3 expose an underspecified intermediate presentation: the correct-as-is path must use a compact saving/recovery view throughout, never reveal/focus the full editor while waiting. Re-derive the new frontend changes after retaining the patch snapshot; do not revert pre-follow-up committed12.4 implementation. KEEP the working compact summary, explicit action intent, fresh/new-draft semantics, separate server-authoritative approval, optional full facts, required unchecked decisions, adjacent bus action/refusal, original command recovery, source validation, mobile upload/access code and all semantic regression assertions. KEEP the epoch ordering fix (invalidate before beginning review; wait for clean after saving). KEEP existing independently specified new tests and add the meaningful gaps below.

Additional implementation decisions: retain source disclosure identity through first save; restore replaced time-field focus by stable activity/field identity and preserve viewport; disable normalized unchanged bus saves; approval navigation must reset notice presentation just as existing screen navigation does. Keep direct recovery controls reachable in its compact view. Hide redundant retry while a valid review exists. Group import choices using existing controls spacing. These are presentation corrections within approved behavior, with no persistence/API change.

Additional verification: direct save with an existing selected draft; committed/lost direct response then explicit same-operation resolution; bus refusal with an already saved draft plus unrelated content/dirty time; independent confirmed bus read/reopening; stale revision before review and before confirmation; tablet source-disclosure/position and time-input keyboard focus. Update legacy tests that explicitly expected the now-rejected heading jump to require retained originating focus instead; do not change persistence/authority expectations.

## Review Triage Log

Three context-free reviewers launched before any result was handled; each finding classified individually before grouping.

| ID | Verdict | Evidence / route |
|---|---|---|
| Blind1 | medium | Direct callback calls setScreen(editor) before awaiting save; slow transport exposes the very editing flow the shortcut avoids. bad_spec: specify compact intermediate state and re-derive. |
| Blind2 | medium | Source details key changes from new to persisted ID on first acknowledgement, collapsing an open disclosure and changing height. patch after re-derivation: stable identity. |
| Blind3 | medium | resetTimes remounts PrivateTimeInput; returnTo.isConnected fails for a submitted time input and skips focus/scroll restoration. patch: stable activity/field replacement target. |
| Blind4 | low | Bus action enabled for normalized equal saved bus, calling ordinary save creates another revision unnecessarily. Direct correction: disable unchanged action. |
| Blind5 | medium | New fresh=true callback closes over prior saved selection; all direct tests start empty. Removing fresh flag passes them while overwriting prior draft. Add actual second-import test. |
| Blind6 | medium | Direct failure test aborts before acceptance; no direct-continuation case exercises a committed receipt lost in transport. Add explicit original-operation resolution/single-effect case. |
| Blind7 | medium | Existing confirmation case covers local invalidation, not a competing saved revision before/after the new approval navigation. Add actual competing-update rejection and reachable recovery. |
| Blind8 | medium | Only bottom-button/default-viewport position test exists; first-save disclosure collapse and adjacent saved-draft paths are untested. Add tablet position/disclosure/refusal cases. |
| Blind9 | medium | Confirmed bus test checks status and unchanged source draft only; an independent saved bus/read/reopen assertion is missing. Add actual persisted bus revision/value assertions. |
| Blind10 | false | Evidence doc explicitly says work and broader verification are in progress, accurately scoped when review was staged. It does not claim delivery complete; final actual outcomes will be appended before delivery. |
| Edge1 | medium | Approval nav lacks registryNavigation increment; an open clean notice registry leaves approval hidden behind notices.screen. Reset notice presentation on approval navigation. |
| Edge2 | medium | Independently confirms disconnected time input skips save focus restoration, same defect as Blind3. |
| Edge3 | medium | Independently confirms transient full editor on direct save, same defect as Blind1. |
| Verification1 | medium | Pre-verified regression gap independently confirms fresh direct path lacks prior selected-draft test (Blind5). |
| Verification2 | medium | Bus refusal test's !saved guard short-circuits before unrelated-edits/time guards; saved-draft bus-only success cannot detect silent whole-draft persistence. Add both saved-draft refusal variants. |

Grouped survivors: compact direct intermediary (Blind1/Edge3) routes bad_spec; all other retained issues route test/presentation patches after re-derivation. No intent gap or deferred product issue. Existing working implementation is preserved in ignored tmp/import-experience-review.diff before reverting only the four new frontend source diffs and re-engaging the implementation agent. Broader gate already in flight must finish before source changes; it qualifies only its captured snapshot and is never treated as post-review verification.

Second review: edge-case reviewer returned no findings; verification-gap reviewer found no gaps. Blind review findings were checked independently before grouping:

| ID | Verdict | Evidence / route |
|---|---|---|
| R2-1 | medium | Auto begin can run again after leaving/returning while its first request is held, because no in-flight review guard exists. Deduplicate the proven same-version request and test held-response navigation; patch. |
| R2-2 | medium | Collapsing Facts leaves required type decisions identified only by activity number; raw code and date/place facts already present in the validated draft must remain visible beside that specific decision. Small relocation of existing facts, patch. |
| R2-3 | medium | send() and save() can capture the old selected saved draft when fresh direct saving begins. A terminal operation rejection after suspension/expiry calls terminalSave using that stale selection and clears the new unpersisted import. Make terminal handling follow actual operation target, not captured prior selection; patch and focused terminal test. |
| R2-4 | low | busMessage is unchanged across adopt/edit/reset, retaining an old refusal under a different draft or after a successful save. Direct text reset/derivation patch. |
| R2-5 | low | Retained keyboard input can be far from both visible save-status placements. Screenreader announcement remains active and ordinary explicit save controls have local feedback. Reject under low-finding rule: implicit submission from the middle of a long form is less likely in the owner's touch/save flow, and a new sticky overlay/origin-message state would add complexity without correcting the requested save-position behavior. No claim of comprehensive visual feedback for every implicit-submit location. |
| R2-6 | medium | A remounted ambiguous-time occurrence selector no longer exists after acknowledgement; indexed replacement is undefined and loses focus. Use the already-proven same time container's date/time input as fallback; patch/test. |
| R2-7 | false | Dirty-adoption confirmation is the same unchanged guard before either intent branch. Existing actual import tests exercise both accept/dismiss of that guard; removing it fails those assertions. New selected-draft direct test independently protects fresh semantics after acceptance. Duplicating identical guard coverage per button is unnecessary. |
| R2-8 | medium | Direct recovery has a distinct no-pending-operation branch when admission fails; only POST failure/accepted-receipt loss is tested. Add admission failure/explicit retry/single-effect case; patch. |
| R2-9 | false | New direct screen is inside the same suspended-hidden PrivateDrafts subtree. Every admission/save/review still uses PrivateAccess.workspace before/after authority checks; account switch/logout unmounts workspace. Existing queued operation/account-switch and delayed accepted-confirmation tests exercise these shared guards. No unguarded direct authority path or automatic retry effect was added; auto review is read preparation for the already-explicit successful save. |
| R2-10 | medium | Compact summary hides header start/end calendar dates and places; C's rollover cannot be assessed without opening the long details. Move those existing source facts into the compact identity and assert independent C dates/places; patch. |
| Root2 | medium | Synthetic owner-import A–E tests still resolved the initially collapsed source region without opening it. Add the explicit disclosure action while retaining all independent fixture assertions; all5 cases then passed in01e4534d. |

Survivors R2-1/2/3/4/6/8/10 route to small internal guard/presentation/test patches using already demonstrated state and existing facts. No intent gap, new API contract or public capability is introduced.13/13 focused integration cases (`9bc72fa9`) and32/32 mobile boundaries (`dc615abc`) passed on the source before these final patches; final affected gates must qualify patched source.

All retained patches were inspected against actual code: review reads are keyed by saved identity/generation; classification context uses existing validated facts and aria-describedby; create/update target controls terminal clearing; bus scope feedback is derived; disappeared occurrence controls fall back inside the same activity/time container; compact identity exposes source dates/places. Root also caught and corrected the missed initial source disclosure in the synthetic owner-import test. No retained finding is deferred.

Final focused execution selected18 new cases plus5 existing independent synthetic A–E imports. Record `01e4534d` passed21/23; two new assertions incorrectly required zero-padded nb-NO display dates and explicit zero seconds. Tests now accept optional leading zeros/zero seconds while preserving independently expected8/9February2030 and first-Oslo-occurrence `2030-10-27T02:30+02:00`. The two affected cases passed in `3872dba1`. Both records have stable source/input/build/API checks; root compared frontend/backend product hashes and proved identical between those runs. This is21 unchanged passing cases plus2 corrected passing cases, not a claimed23/23 single run. Final product asset is `main-DbTshW9R.js`; wider regression is in progress on that source.

Broad gate `a0cfe7e7` completed with317 passed,5 failed,4 not run (35.4minutes). Preliminary progress updates based only on log tails missed earlier recorded failures; final counts supersede them. Do not claim326/326. Each failure is triaged below; retain raw record and failing assertions.

| ID | Verdict | Evidence / route |
|---|---|---|
| Regression1/2 | medium test | Both private-import keyboard cases use unscoped getByText for the unknown-save message; new local bus feedback intentionally duplicates that text near the bus action, causing strict locator ambiguity. Scope to the authoritative Lagringsstatus role; preserve full unknown-save/recovery assertions. |
| Regression3 | medium test | Held import returns503; legacy selected-activity test expects a parser rejection. Accepted mobile error classifier correctly says service temporarily unavailable. Assert that category, no parser/adoption result, unchanged draft/focus and retained failure after return. No product error mapping change. |
| Regression4/5 | medium product | At768px the existing notice-reader entry above selected activity pushes planned start to480.56px, violating the existing <450 bound. Initial suspicion of approval-nav wrapping was disproved by the rendered trace: consultation already hides that nav. Historical c884ade has the same notice placement. Move the same notice entry below selected activity only during consultation; preserve its ref/access behavior, ordinary day placement and every geometry, contrast, enlargement and focus threshold. |

These route to direct presentation/test patches. Re-engage the same implementation agent, then root verifies all cases in the two affected suites, both actual journeys and all18 new preparation cases on final source; run fresh mobile32 afterward.317 prior passing cases qualify their captured snapshot; final report must distinguish them from targeted post-patch reruns and the four previously unrun cases.

## Verification

- Existing guarded runner build plus focused new shift-preparation integration, complete real journeys and affected draft/confirmation/bus/recovery regressions.
- Fresh mobile boundary32 cases, preserving actual byte/access sequencing. These use intentional test doubles and do not replace real integration.
- Root inspects actual rendered tablet/desktop flow; further personal device acceptance remains the owner's decision.

Re-derivation checkpoint: only the four uncommitted frontend source changes were restored to HEAD after preserving them in ignored `tmp/preparation-before-review-source.patch` and the complete staged review diff. The5-test stable focused gate passed (`3f43ed26`); the broader326-case pre-review run (`68b5099b`) was deliberately stopped via its exact verified npx PID14092/tree after review identified necessary changes. It is incomplete, never326/326. Root retains the evidence and will rerun affected verification after the final freeze. Agent may reapply the preserved working patch as a starting point, then implement every reviewed correction/test requirement and report source freeze. No other source changes or manual-account mutation are authorized.

Final technical qualification:64/64 affected actual-API/browser cases (`427d7a87`) and32/32 fresh mobile boundary cases (`f3e6ccfa`) passed on unchanged source with matching executed inputs/build/API identity. Fresh served build (`f92bb74f`) is `main-BRJ12oLt.js`. Both complete journeys and all18 new cases passed in the64-case gate. All retained review findings are addressed; no technical finding is deferred. The explicitly rejected low finding remains documented above. Keep status in-review because the owner expressly withheld Story12.4 acceptance; generic workflow auto-done does not override that instruction. The four-point physical/personal retest and explicit decision remain open. Delivery/source/runtime details are in the evidence report and session log.
