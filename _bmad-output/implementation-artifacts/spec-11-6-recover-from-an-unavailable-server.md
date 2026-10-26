---
title: '11.6 — Recover from an unavailable server'
type: feature
created: 2026-10-26
status: done
route: dispatch
review_loop_iteration: 0
baseline_commit: aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed
story: '11.6'
story_key: 11-6-recover-from-an-unavailable-server
owner_acceptance: accepted
owner_accepted_on: 2026-10-26
context: []
---

<frozen-after-approval reason="Owner authorizes autonomous planning, implementation and verification without a separate approval stop">

## Intent

Recover honestly from an unavailable private server: preserve current proposals while the page remains open, distinguish rejected saves from unknown outcomes, reconcile the original operation with authoritative current state and reopen the last saved revision online. Integrate the existing draft, activity/lifecycle and notice recovery flows without general offline functionality.

## Boundaries & Constraints

**Always:** Keep input and immutable original commands in memory across safe navigation and temporary suspension. Show saving, unsaved, saved, unavailable, conflict and unresolved states truthfully even after list refreshes. A timeout, malformed response or failed lookup cannot establish rejection or success. Reconcile stable authorized operation status before a user retry; retry only the original identity/payload/target. Accepted historical receipts establish an effect, not necessarily the latest current revision. Fetch current state before adoption; preserve the proposal and offer explicit comparison when newer data exists. Expected revisions and server authority prevent silent overwrite, duplicate creation, expiry extension or resurrection. Warn before avoidable loss. Recheck account/session/ownership/retention; security invalidation wins over preservation. Saved notice check/status/validity remain independent; unavailable reader data must never masquerade as an empty or fresh result.

**Never:** No automatic resend/merge, force overwrite, persistent private browser content, service worker, offline queue or offline restart promise. No new source feeds, parser/demo expansion, next epic, manual acceptance, staging, commit or push. Preserve every pre-existing local change and historical artifact; keep any 11.5 correction/evidence distinct. Use disposable synthetic accounts for mutation tests and restore ordinary services/data/secret.

## I/O & Edge-Case Matrix

| Scenario | Input/state | Expected behavior | Failure handling |
|---|---|---|---|
| Normal save/reopen | Dirty proposal, online server | Saving then verified current saved revision; reopen server copy | Dirty is never labelled saved |
| Before acceptance | Request timeout/outage before commit | Proposal retained, unknown until authorized status; same-command retry | No new identity or duplicate |
| Lost acknowledgement | Commit then lost/malformed reply or unavailable status | Unknown outcome remains explicit; lookup finds accepted effect | No false not-saved claim |
| Newer data | Accepted receipt followed by another server edit, or stale revision | Retained proposal plus current comparison, explicit resolution | Never adopt stale receipt as current or overwrite newer data |
| Known rejection | Valid API validation/conflict response | Explain rejection and preserve input | Status-only/HTML proxy replies remain uncertain |
| Notices/reader | Save, source check or manual end during outage; navigate to reader | Original command retained; recover exactly once, refresh authoritative reader | No duplicate, false clearance, false source check or stale reader success |
| Suspension/loss | Server unavailable, account switch, reload/leave | Same-session recovery retains memory; loss warning; online reopen saved data | No private persistent storage; account/expiry clears access |

</frozen-after-approval>

## Code Map

- `frontend/src/PrivateDrafts.tsx`: `failed`, `send`, `save`, `settle`, `acknowledge`, dirty/loss guards. Main demonstrated gaps: failed lookup says not saved; direct historical receipt adoption; HTTP-status-only rejection; retry bypasses lookup. Reuse strict validators, comparison and server-issued draft operations.
- `frontend/src/PrivateAccess.tsx`: request deadlines, session-bound workspace, hide-without-unmount suspension and restore. Preserve identity rules; distinguish proven pre-dispatch failure if useful without assuming a dispatched timeout means rejection.
- `frontend/src/PrivateNotices.tsx`, `useWorkdayResource.ts`, `PrivateWorkdayProgress.tsx`: immutable commands, typed receipts, current read after receipt, terminal guards. Integrate status-first user retry while retaining ordinary first-send semantics and strict typed recovery.
- `frontend/src/PrivateNoticeReader.tsx`, `PrivateWorkdayView.tsx`: retained separate reader, stale response rejection and navigation; preserve selected member and notice proposals.
- `backend/app/draft_storage.py`, `workday_notice_storage.py`, `workday_outcome_storage.py`: atomic operation receipts, authorization and expected revision. Reuse existing contracts; no new migration is anticipated.
- `frontend/tests/private-drafts.spec.ts`, `private-notices.spec.ts`, `private-notice-reader.spec.ts`, `private-identity.spec.ts`, activity helpers: real disposable API/browser fixtures. New recovery tests may use route faults around real writes; include actual API stop/start on synthetic environment.

## Tasks & Acceptance

- [x] `frontend/src/PrivateDrafts.tsx` — correct unknown/rejected status, persistent semantic save status, status-first retry and current-state reconciliation with retained comparisons.
- [x] Existing private recovery controllers as needed — consistent status-first retry and retained original commands; preserve security/navigation semantics.
- [x] `frontend/tests/private-recovery.spec.ts` and affected suites — execute every matrix row, including before/after commit faults, proxy errors, repeated retries, newer revisions, loss guards, actual stop/start and 11.4–11.5 interplay. Record enlarged Day/Night recovery states under new 11-6 evidence names.
- [x] `docs/evidence/11-6-server-recovery.md`, implementation plan, README, development log, canonical story and sprint — exact results, independent review, reproducible environment and manual steps; owner acceptance pending.

Given an uncertain save, when status lookup also fails, then the original command and proposal remain and no text asserts that it was not saved.
Given a historical accepted receipt and newer server state, when recovery runs, then the proposal and latest comparison are visible and no newer record is overwritten.
Given notices during a server outage, when the server returns and the user explicitly recovers, then exactly one intended effect exists and the reader displays only refreshed saved facts.

## Implementation Notes

No unresolved intent gap. Existing backend contracts make this a frontend recovery integration with meaningful API/browser verification, rather than a new storage model. The owner explicitly authorizes continuing over the dirty 11.5 tree and skipping a separate plan approval; preserve that tree. The 106-file 11.5 checkpoint and actual logs are continuity evidence; no missing mandatory 11.5 automatic result is currently established. No 11.5 product correction is planned.

Implementation worker owns code/tests and focused sequential verification; do not invoke another Build workflow or delegate. Root owns independent review, broad final gate, ordinary rollout/preservation and final documentation. Coordinate test service operations: use `ibe160-private-tests` only, stop ordinary API to free 8001, restore it in finally. Save new test logs under tmp/11-6-*. Preserve existing docs/evidence files before tests rerender them; root has an initial tree backup under tmp/11-6-initial-tree. Build with npm.cmd run build; browser tests require built preview and disposable API. Ask root for service coordination before mutations. Keep test fixtures synthetic. No package/library changes are anticipated.

## Spec Change Log

## Verification

Run production build, focused recovery/affected browser cases, existing API regression gate and full sequential disposable verifier after review. Audit matrix against actually passing tests; preserve failures and report any bounded reruns honestly. Compare ordinary database/secret/container fingerprints and restore historical evidence. Inspect rendered recovery screenshots and measured keyboard/narrow/enlarged Day/Night layout. Planned physical acceptance testing uses Lenovo Pad with Android and Brave over the mobile network to the desktop server at home; this remains unperformed and separate from executed desktop Edge/Playwright automation. The owner's 2026-10-26 correction identifies iPad/Safari as outside the planned setup. No new tests are requested by this correction; both stories remain pending manual acceptance.



Root verification checkpoint: production build passes; 19 focused recovery/outcome cases pass in 1.5m, including literal 10-second timeout before dispatch and an actual disposable API stop/start. Four 390/768 Day/Night enlarged recovery renders pass measured contrast/focus/overflow checks and root visual inspection. Prior diagnostic failures remain documented separately; root extended notice/reader interruption assertions after this checkpoint and will run that exact case before full regression. Activity outcome proposals are retained when current saved target differs; original notices/draft comparisons and status-first retry remain intact. Full sequential gate and final preservation/rollout remain root-owned. Review uses the complete commit-baseline diff, with an incremental initial-worktree comparison retained to distinguish inherited 11.5 work.

## Review Triage Log

| ID | Verdict / route | Evidence and resolution target |
|---|---|---|
| B1 confirmation refresh claims no activity started | medium / patch | `list(false,true)` still overwrites recovery with an unverified lifecycle claim; replace with confirmation/current-plan-only copy. |
| B2 late confirmation current read lacks generation guard | medium / patch | Added async `accept()` checks only mount lifetime after current read; preserve the caller generation/epoch so expiry or supersession cannot adopt late data. |
| B3 maximum calendar date overflow | false / reject | The public reader only accepts persisted confirmed plans. `workday_domain.py:124,165` requires final-end-plus-seven-days; a plan containing 9999-12-31 cannot be confirmed. The direct projection can overflow for an artificial unreachable plan, but the cited valid-confirmed-plan trigger is disproved. No 11.5 product correction is needed. |
| B4 comparison reread can regress | medium / patch | `reopen(comparison.id,true)` validates ID only; add the shown comparison's revision/identity/deadline floor before discarding the proposal. |
| B5 timeout boundary naming / preflight case | low / patch | The test holds a browser-dispatched POST before backend forwarding. Name that boundary accurately and explicitly cover preflight failure with zero write dispatch. |
| B6 missing helper authorization-gate coverage | medium / patch | The draft protocol does not enter shared helper's absent-receipt branch. Add failed/malformed current-target authorization and no-resend assertions. |
| B7 missing absent-receipt revision-race coverage | medium / patch | The shared helper authorizes then resends original expected revision; prove another-window edit at that boundary conflicts and retains the proposal without overwrite. |
| B8 dirty notice through real suspension missing | medium / patch | Existing route faults cover committed commands, not edited notice text through genuine API/session suspension. Add a synthetic real API stop/start case retaining all entered fields and saved pre-edit content until explicit save. |
| B9 representative enlarged recovery coverage missing | medium / patch | New measurements are draft-only; add representative long notice and outcome recovery messages/controls at narrow enlarged Day/Night layouts, retaining old evidence. |
| B10 recovery contract description overgeneralizes | low / patch | Draft/confirmation use authorized pending operation rows, whereas client-created operation resources use absent receipt plus current target. Explain both contracts separately. |
| E1 confirmation lifecycle copy | medium / patch | Same independently verified defect as B1; the suggested neutral copy fits the confirmed-plan contract. |
| E2 plan deletion retry bypasses lookup | medium / patch | `PrivateConfirmation.remove` still posts directly for a retained deletion command. Apply status-first recovery with authorized parent on absent receipt; accepted receipt resolves without another POST. |
| V1 missing helper authorization-gate coverage | medium / patch | Pre-verified regression gap: removing `await authorize()` would pass current tests and allow resend after unavailable current-target authority. Same cause as B6. |
| V2 old accepted-retry POST assertions | medium / patch | Bus/selection/start/outcome/draft-deletion fixtures still require POST after acceptance. Update to prove no additional POST; preserve original same-command assertions for actual unaccepted retries and all server-state/identity checks. |
| V3 owner-feedback failed-lookup retry fixture | medium / patch | Start receipt route remains 503 while fixture expects success. First assert failed retry sends no POST, then restore lookup and verify accepted receipt settles without resend. |

All three review layers returned before triage. No intent ambiguity is introduced: every retained issue is a direct correctness, copy or regression correction within existing recovery contracts. Patch groups: confirmation copy/generation (B1/B2/E1); comparison floor (B4); boundary/authorization/race verification (B5/B6/B7/V1); notice suspension/enlargement (B8/B9); evidence precision (B10); deletion/status-first fixture alignment (E2/V2/V3). No finding is deferred. Root will independently inspect and execute covering tests after patch return.


### Patch reinspection

The original blind reviewer independently confirmed B1, B2 and B4–B10 addressed and withdrew B3 after verifying the public confirmation retention bound. The original edge reviewer confirmed neutral confirmation copy, status-first plan deletion and post-current-read generation/epoch protection. The original verification reviewer confirmed failed/malformed current-authority no-resend coverage, changed accepted-retry assertions and failed-lookup Start recovery. All reinspections were read-only; no unresolved concrete defect or deferred finding remains. Root execution is separate evidence: the post-review targeted gate and final full gate are recorded in the delivery report.

Root added a deterministic held-current-read/source-expiry regression: confirmed future plan and session remain live, but the source expiry changes the editor authority epoch before the held response returns. It must not adopt until a new explicit authorized lookup. The regression passed in the targeted run, proving the added epoch boundary rather than merely relying on component unmount or expired-plan validation.

### Root full-gate fixture findings

| ID | Verdict / route | Evidence and correction |
|---|---|---|
| R1 noncanonical 413 fixture | low / patch | The old draft fixture emits `Too large`, which the actual API never sends. Typed rejection correctly leaves that proxy-like reply uncertain. Use the actual `Forespørselen er for stor.` detail while retaining editable-input and corrected-save assertions. |
| R2 contradictory future timestamp fixture | medium / patch | The old fixture forges POST creation/expiry while the new current GET returns real timestamps. Current-state reconciliation correctly rejects the contradiction. Test real clock skew by keeping browser time 60 seconds behind the server and assert actual future server time plus consistent POST/current facts. |

The original blind reviewer independently confirmed both diagnoses and their smallest test-only corrections, with no product change or 11.5 correction required. Root retains the frozen full-run checkpoint before applying them; its complete result and subsequent corrective verification remain distinct in the evidence report.

| ID | Verdict / route | Evidence and correction |
|---|---|---|
| R3 proxy recovery fixture synchronization | medium / patch | Failed-lookup routing was removed before the lookup settled; a submit node could change from retry to normal save during the click. Wait for the actual aborted lookup, settled retry control and background refresh; count every draft mutation and assert the original record/revision exactly. The verification reviewer confirmed the reachable harness race and stronger assertions; the log does not establish automatic product redispatch. |

### Final closure — 2026-10-26

Full gate completed: 411 backend passes in 488.49s; populated restart/migration/raw-state preservation and build pass; browser 453/456 in 34.6m. R1–R3 changed only two test files, with no product source change. Eight affected cases (including the six variants sharing R3 synchronization) then passed three times each: 24/24 in 1.6m. Every browser case has passing coverage across these runs; the original full run is not relabelled green. No broad suite was repeated after the owner's continuation request. All retained review findings are resolved and reinspected; none is deferred.

Final preservation confirms all 23 ordinary tables, database identity and secret unchanged; 892 initial files retained, 293 historical render/measurement and 18 example/oracle/source files byte-identical. Served HTML/assets and 43 runtime backend/migration files match tested source. Ordinary services healthy, disposable services stopped. Full logs, exact failure classification, eight enlarged recovery captures, known limits and manual steps are in the [delivery report](../../docs/evidence/11-6-server-recovery.md). 11.5 needed no product correction. Technical work is complete; specification remains in-review and owner acceptance of both stories pending. No staging, commit/push, retrospective or next epic.


## Corrected 11.5 integration review — 2026-10-26

All three required independent layers reviewed the complete HEAD-to-working-tree diff, including untracked text additions (624,723 bytes). This table records every finding before grouping; speculative missing tests are distinguished from demonstrated product faults. Initial gate was deliberately interrupted after 78 backend progress dots when the recovery defect was established. It is incomplete, not a passing suite. Its finally restored ordinary services and preserved all 24 tables (three expired throttle rows removed by existing cleanup).

| ID | Verdict / route | Evidence and disposition |
|---|---|---|
| IB1 | medium / patch | PrivateNotices.send classifies bare POST proxy 409/422 as rejection and drops original identity after a committed create. Require canonical typed API rejection and preserve uncertain original commands. Add lost committed notice response proxy matrix. |
| IB2 | medium / patch | Bare 429 has undefined apiDetail; reading .code throws inside catch. Validate the exact capacity detail shape before reading it; unknown 429 remains uncertain. |
| IB3 | low / reject | New creation checks future ending at its server registration timestamp; a transaction crossing that ending stores an already-ended historical row, never extends or revives an incident. Reader excludes it and subsequent writes reject it. Unlike an extension, no previous incident deadline is bypassed. Adding a second creation rule is not needed for the requested no-resurrection contract. |
| IB4 | medium / patch | Anchoring server_now at response completion discards transit elapsed time and can display expired notices as active after a held reply. Anchor conservatively at request start, count elapsed time immediately, retain monotonic clock. Cover held reader and maintenance responses without device-time changes. |
| IB5 | medium / patch | Maintenance filters storage retention before fetching a later server_now; a crossing row contradicts the frontend validator and hides the whole register. Capture one database instant for both query and server_now and prove boundary behavior. |
| IB6 | false / reject | Cursor pages are separately authorized reads, not a promised atomic account snapshot. Another write after any read is inherently possible; expected revisions prevent overwrite, receipt identity/current revision validation prevents false receipt adoption, and explicit refresh obtains later state. No demonstrated unauthorized adoption or duplicate follows from the proposed interleaving. |
| IB7 | medium / patch | Add accepted source-check/lost-reply recovery across automatic ending: receipt resolves exactly once, history remains expired and no mutation control reappears. This closes a bounded integration qualification gap rather than a proven product defect. |
| IB8 | false / reject | Hypothesis of shortened retention causing redispatch is covered by terminal gone/retention browser cases and backend receipt-deadline/cleanup tests. All old receipts follow canonical retention; member/receipt authority denies and frontend terminal proof prevents resend. No distinct failing path established. |
| IB9 | false / reject | Existing legacy completion test preserves original lease until accepted completion then extends canonical/receipt metadata; terminal member lookup rejects expired unaccepted completion. Lost-reply handling uses the same receipt/current-state branches covered by deployed legacy recovery and terminal-proof browser tests. No distinct defect established. |
| IB10 | false / reject | App and PostgreSQL run on the same Docker host clock in the supported ordinary/test environments. Separate hypothetical host clocks are outside this deployment; no actual clock disagreement is established. Client skew remains explicitly tested. |
| IE1 | medium / patch | Receipt GET itself can return 409/422/429 before resend; !lookup does not mean a POST was dispatched. Track dispatch separately and require typed canonical rejection from that dispatch; failed status/current reads retain original. Test exact typed-looking rejection on lookup as well as HTML proxy statuses. |
| IV1 | medium / patch | Regression gap: absent unaccepted create crossing its ending is not covered. Add authoritative lookup/current-read/no-second-POST/discardable-proposal assertion after the deadline. |

Patch groups: rejection provenance/shape (IB1, IB2, IE1); elapsed clock (IB4); one database list instant (IB5); integration branches (IB7, IV1). Original implementation agent is unavailable in this resumed chat; root applies patches and original reviewers reinspect. These repairs affect accepted 11.5 at failure/latency boundaries: proxy failures retain unresolved attempts, and delayed replies cannot temporarily renew active display. Core cross-day/ending/extension behavior remains as approved; include affected behavior in owner testing. Story 11.5 acceptance is not recorded again on the owner's behalf.

Manual test environment selected by Jonas in this chat: desktop locally in a browser (browser/version to be observed, not invented). Planned later platform remains Lenovo Pad/Android/Brave over mobile network to desktop server at home. Owner schedules remote access between Epic 11 and Epic 12; no setup in this task. Retrospective finalization remains blocked on explicit manual acceptance of 11.6.


## Fresh 11.6 integration checkpoint — 2026-10-26

Jonas authorized verification against accepted corrected 11.5, fixes, full regression and local rollout, stopping before his manual results/explicit approval. Current HEAD remains `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed` on main with empty index; the dirty tree is identified by the 120-file source manifest SHA256 `1e0101380841d712125ce999a36d3f20dc43dfe66de253ae22016679111524e5` in `docs/evidence/11-6-integration-source-2026-10-26.json`. Earlier results remain historical.

Recovery now rejects only exact known write rejections after dispatch; HTML/proxy and failed receipt/current reads retain the original notice operation. Delayed reader/maintenance replies count request elapsed time immediately, conservatively hiding near-ending entries rather than prolonging validity. Maintenance uses one database instant for retention and server_now. These failure/latency repairs affect accepted 11.5 and are explicitly included in the manual checklist. Three independent review layers and their reinspection have no open retained finding.

**421 backend tests passed in 526.37s; all 479 browser cases passed in one invocation (38.9m)**. Populated restart, repeated migrations, exact raw state/receipt/deadline/session preservation, cleanup and TypeScript/Vite build passed. One existing TestClient dependency deprecation warning; no product/test failure.

Fresh focused results: 10 account API tests in 16.82s and 7 new browser regressions in 1.1m; 7 verifier restoration controls in 0.256s. The first full attempt was deliberately interrupted after 78 backend progress dots for the discovered defect, not relabelled a pass. Full final log: `tmp/11-6-integration-final-full.log`.

All 120 frozen implementation/test/build files unchanged. All 1004 initial files retained, 390 historical artifacts and 24 original fixture/source/oracle files byte-preserved; 26 frozen contract blocks unchanged. Original fields/rows of all **24 ordinary tables**, database identity and secret preserved; only three expired throttle rows were removed by existing startup cleanup. Ordinary services healthy, synthetic services stopped. Served HTML/assets and 44 backend/migration files match tested bytes. Retro draft unchanged.

Unchanged historical byte control passes; independent pre-11.6/pre-cross-day/resumption comparisons preserve all 24/25/26 frozen blocks. The earlier reported Historical frozen contract changed failure has no retained failing path/bytes/run snapshot and cannot be reproduced; its exact historical trigger is unestablished. No evidence supports changing a frozen contract or weakening the control.

Jonas selected local desktop browser testing; actual manual browser/version/results remain pending. Planned Lenovo Pad/Android/Brave/mobile-network testing remains unperformed. Owner schedules remote access between Epic 11 and Epic 12; none configured here. See the current integrated section of the delivery report for exact startup/actions/expected results. Story 11.6 remains in-review/review with manual acceptance pending; corrected 11.5 remains previously accepted/done. No retro finalization, Epic 11 closure, staging, commit, push or Epic 12 work.


## Owner acceptance - 2026-10-26

Jonas explicitly approved the integrated 11.6 delivery and instructed completion of the Epic 11 retrospective, including the preliminary work from the other chat. The accepted source manifest remains unchanged. Selected manual environment was local desktop browser; detailed scenario results/browser version were not supplied and are not invented. No physical Lenovo/Android/Brave/mobile-network test is inferred. Remote access is scheduled between Epic 11 and Epic 12. No commit/push or Epic 12 implementation is authorized. Earlier pending statements remain historical.


## Epic 11 final retrospective and closure - 2026-10-26

Jonas explicitly accepted integrated 11.6 and requested completion of the Epic 11 retrospective using the preliminary work from the other chat. All six stories are done; the script-backed pending list is empty. The continued retrospective is `_bmad-output/implementation-artifacts/epic-11-retro-2026-10-26.md`, verdict **accepted-with-open-items**. The original preliminary document is preserved byte-for-byte alongside it. Three fresh whole-epic review lenses ran; concrete bounded recovery/presentation findings and an expiry regression gap are proposed follow-ups, not auto-fixed. Twelve proposed items were appended open by the bundled comment-preserving status script; no prior action status changed. The project defines epic done as all stories completed, so Epic 11 and its retrospective are done; Epic 12 remains backlog.

The accepted 120-file source manifest SHA256 `1e0101380841d712125ce999a36d3f20dc43dfe66de253ae22016679111524e5` still matches. Existing 421 backend / 479 browser results retain that exact code identity and were not blindly rerun. Fresh exploratory real HTTP/API/PostgreSQL observations covered exact selection/explicit Start/outcome, one-effect receipt recovery, shared notices across days, source check/extension/stale denial, original-day close/delete, manual ending and real short expiry; only a new synthetic account was removed. All 24 ordinary tables, database identity and secret match the fresh before/after baseline; ordinary services healthy and synthetic stopped. The PowerShell host returned NativeCommandError/exit 1 for Docker informational stderr despite every flow/teardown/preservation PASS; this orchestration anomaly remains explicitly recorded, not relabelled as an aggregate green tool exit.

Owner-selected manual context is desktop local browser; specific scenario results and browser/version were not supplied. No physical Lenovo Pad/Android/Brave/mobile-network pass is inferred. Remote access is scheduled between Epic 11 and Epic 12 and is not configured here. Previous E10 theme/device items remain open with their original selectors; current tablet target is recorded separately. No application/test/build changes, commit, staging, push, remote setup or Epic 12 implementation.
