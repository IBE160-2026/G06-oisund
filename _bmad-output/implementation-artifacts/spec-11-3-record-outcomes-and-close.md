---
title: '11.3 — Record outcomes and close'
status: done
approved_on: 2026-10-25
type: feature
route: dispatch
review_loop_iteration: 0
created: 2026-10-25
epic: 11
story: '11.3'
story_key: 11-3-record-outcomes-and-close
alias: V1-12
implementationStarted: true
owner_acceptance: accepted
owner_accepted_on: 2026-10-25
baseline_commit: b42f1e8fa66ad5026f1751f31ddad50c3acbc7d6
context:
  - D:/IBE160/_bmad-output/specs/spec-11-3-record-outcomes-and-close/SPEC.md
  - D:/IBE160/_bmad-output/specs/spec-11-3-record-outcomes-and-close/implementation-plan.md
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-11-context.md
---

<frozen-after-approval reason="owner approved complete plan and active-only clarification on 2026-10-25">

## Intent

**Problem:** Accepted 11.2 supports separate day/activity screens, manual selection and Start, but no outcomes or terminal closure.

**Approach:** Implement active-only manual outcomes, explicit end/abort confirmation and retained read-only recap (FR-11/21/22/24, AC-08). The approved companion plan supplies detailed flows and tests.

## Boundaries & Constraints

**Always:** The owner requires Start before outcome registration. Before Start, day reading, selection and details stay available. Selecting/navigating never starts work or changes outcomes. Reuse original first server start. Record/correct exact-member completed/skipped/interrupted/unregistered before closure; absent is `Ikke registrert`, including every pause/non-passenger member. Keep source, bus and selection independent.

Separate primary screens: day → activity/outcome → day → end/abort confirmation → recap. Explicit Save for outcome, clear cancel and focus return. Preserve input and reachable uncertain-operation recovery. Closure reviews saved counts, requires active state/current lifecycle and outcome revisions, saves terminal reason/first server end/deadline atomically once and never fills unknowns. Terminal day/detail/recap are read-only, no Start/resume or bus/selection/outcome writes. View closing/deletion remain distinct existing actions.

Retain typed UUID/revision/receipt contracts, 2,000 live receipts/account/resource, same-body retry/authorized lookup, identity binding, no-store and atomic expiry checks. Workday locking serializes writes/closure/deletion. Old receipts never replace current authority. Shorten effective expiry to min(existing, planned end+7d, first server end+7d); preserve planned maximum/historical facts. Align metadata deadlines, immediate denial and startup/hourly purge. No renewal/resurrection.

**Never:** No notices/demo expansion, GPS/automatic completion/stops, offline private persistence, export/scores, post-end editing, replacement Start, commit, push or next story. Theme persistence/actual-device obligations remain 12.3/12.4.

## I/O & Edge-Case Matrix

| Scenario | Expected behavior |
|---|---|
| Unstarted | Read/select/detail allowed; outcome/close rejected; selection never Starts |
| Active exact member | Save/correct/clear changes only that ID; survives reload |
| Cancel closure | No mutation; return focus; unknowns unchanged |
| End/abort/replay | One terminal reason/time/shortened expiry; unknowns stay unknown |
| Stale/racing writes | Conflict/renewed review; no overwrite, partial close or later mutation |
| Lost/malformed/unavailable reply | Retain command; authorized lookup/retry; no false success |
| Terminal reopen/old receipts | Read-only recap; original start; no resumed state/longer deadline |
| Identity/expiry/deletion | Hide denied facts; immediate expiry; cascade/purge; no resurrection |
| Day/Night/enlargement | Separate screens, reachable controls, keyboard/focus and IR-01 |

</frozen-after-approval>

## Code Map

- `backend/migrations/private/004_workdays.sql` fixes exact expiry; `009_workday_selection.sql` fixes active/revision one. Extend additively, never edit applied migrations.
- `backend/app/workday_lifecycle_domain.py`, `workday_lifecycle_storage.py`: first Start, parent lock, receipts; extend terminal commands plus focused outcome modules/routes in `private_main.py`.
- `workday_domain.py`, `workday_storage.py`: current-vs-historical expiry validator/list/reopen/confirmation. Confirmation lookup dynamically presents the plan; do not invent immutable historical confirmation JSON.
- `workday_bus_storage.py`, `workday_selection_storage.py`, `private_storage.py`: terminal admission and cleanup.
- `frontend/src/PrivateConfirmation.tsx`, `PrivateShiftStart.tsx`, `useWorkdayResource.ts`: validators/parent guards/timers and mounted controllers; preserve independent old-plan/new-confirmation expiry.
- `PrivateActivitySelection.tsx`, `SelectedActivityDetails.tsx`, `PrivateDayOverview.tsx`, new outcome/closure/recap components: exact-member state, navigation/focus and read-only consultation.
- `scripts/verify-private-drafts.py`, `scripts/test_verify_private_drafts.py`: synthetic sequential gate, restart/migration and operational restoration. Ignored tmp/11-2 preservation scripts supply patterns, not new evidence.

## Tasks & Acceptance

- [x] Add additive schema/domain/API outcomes/terminal contracts preserving legacy data/policies.
- [x] Add terminal guards/deadlines across mutations/readers/receipts and cleanup.
- [x] Implement separate outcome/confirmation/recap screens and current-state propagation; preserve input/recovery/focus.
- [x] Execute API/PostgreSQL/browser tests for every matrix row and companion matrix.
- [x] Extend restart/verifier coverage; run focused then complete sequential verification/build; preserve ordinary state.
- [x] Inspect rendered browser journey/IR-01; record evidence, README/log/sprint/spec and independent review/fixes.

Given active/unknown members, saving correction then cancelling/confirming closure preserves exact-member values and read-only reload without inferred completion. Given competing windows/lost replies/expiry, no duplicate end, stale overwrite, resumed shift or extended deadline occurs. Given long/enlarged Day/Night content at 768/1024/1440, navigation/facts remain accessible.

## Implementation Notes
Implemented contracts: migration 010 preserves existing rows/first starts, adds lifecycle `ended_at` with active revision 1 / terminal revision 2, `workday_outcomes`, `workday_outcome_revisions`, `workday_outcome_operations` and `workday_close_operations`. Current `expires_at` may shorten below the preserved `final_end + 7d` planned maximum. Outcome GET `/outcomes` returns complete ordered membership; POST `/outcome` carries expected outcome (`expected_revision`) and lifecycle revisions. POST `/close` carries expected lifecycle (`expected_revision`) and outcome revisions plus ended/aborted action. Operation lookup preserves the existing receipt shape. Parent-locked GET `/recap` consistently projects plan/lifecycle/outcomes/bus. Live receipt metadata shortens atomically while accepted JSON remains historical; confirmation lookup stays dynamic. Frontend mounted controllers retain memory-only proposals/recovery, reconcile current shorter expiry and use transient terminal consultation without saved selection writes.

Worker focused checkpoints: 32 API/PostgreSQL tests passed in 65.03s; six isolated verifier controls passed; nine corrected browser cases passed including actual upload-to-recap, literal Oslo date/count and numeric IR-01 render checks. Final complete focused browser/affected legacy run is recorded in the evidence document. Independent review/full sequential gate/ordinary preservation comparison and final review status remain root-owned. See `docs/evidence/11-3-outcomes-and-close.md`; no owner acceptance or broad-gate pass inferred from focused results.

Owner approved complete plan, tests, browser walkthrough and fixes without another checkpoint. Existing dirty files are this story's planning artifacts/log; preserve them. One cohesive outcome/closure goal, additive migration and coordinated UI/API footprint justify dispatch; no unresolved intent gaps. Generic approval/staging/commit instructions are overridden by explicit authorization/stop. Stop in-review/sprint review pending owner acceptance, no staging/commit/push. Obtain temporary review diffs including untracked files without modifying the index.

Use disposable synthetic database/accounts only; preserve ordinary accounts/sessions/records/secret/volume. Capture pre-migration ordinary-table digests first, verify intended additive column/new-table changes separately, and restore ordinary API after tests. Worker runs focused checks and returns services restored; root owns independent review, complete sequential gate and served-build checks. Preserve historical images/failed logs. Full approved companion detail remains intact rather than splitting scope.

## Spec Change Log

## Review Triage Log

All three context-free BMAD layers completed before triage. The two instruction-file ACL failures were retried with authorized read-only escalation before actual reviews. Blind floor: 10; edge: 1; verification: 2. Each candidate is adjudicated separately below. No intent gap or public contract change is required.

| ID | Verdict / route | Evidence and disposition |
|---|---|---|
| B1 | low / patch (root artifact restoration) | Full legacy browser checks regenerated tracked historical PNGs. Initial evidence was clean; restore generated historical files and retain separately named 11.3 artifacts. The old unchanged claim must describe the final restored tree. |
| B2 | medium / patch | The measure helper restores focus immediately after Tab; this cannot establish actual keyboard traversal through the new flow. Add one real keyboard-only outcome/confirmation/recap journey with actual focus assertions. |
| B3 | low / patch | The new expandable summary is excluded from measurement selectors. Include summary and expanded unregistered content in actual contrast, size, focus and overflow evidence. |
| B4 | false / reject | The six viewport cases already use the long multiword fictional destination from openedPlan, long/enlarged scrollable recap and explicit overflow assertions. The claim that fixtures are short is false. Maximum-length identifiers/descriptions are not an additional source requirement; activity IDs are fixed UUIDs. B3 supplies expanded-list checks without inventing a new maximum-size qualification. |
| B5 | medium / patch | Recognized 429 capacity responses are normalized into generic review/retry copy, losing the known wait-until-receipts-expire explanation. Retain actionable validated capacity feedback and cancellable known-unaccepted proposals. |
| B6 | medium / patch | Shared identity wrappers are covered, but new pending outcome/closure surfaces lack held-response identity/session invalidation browser cases. Add them without weakening existing access guards. |
| B7 | medium / patch | New pending outcome/closure controllers need actual browser deletion/expiry coverage, beyond backend denial. Verify hidden facts, cleared expiry locks and no late recap resurrection. |
| B8 | low / patch | Close lookup is implemented and API-tested; browser failure cases resolve through POST retry only. Add lookup-only resolution with one original mutation and preserved terminal identity/time. |
| B9 | medium / patch | Known rejected stale outcomes preserve proposals in code but lack a browser comparison/new-explicit-save test. Cover newer saved value alongside retained proposal and no implicit overwrite. |
| B10 | medium / patch | Existing concurrency tests race outcomes with closure, not two outcome commands at the same expected revision. Add exactly-one-acceptance/conflict/revision/member assertions. |
| V1 | medium / patch | Pre-verified regression gap: repeated migrations run after fixtures are created on the current schema. Add a genuinely populated pre-010 upgrade case preserving plans, active first starts, historical receipts and deadlines; a migration that rewrites started_at must fail. |
| V2 | medium / patch | Pre-verified regression gap: lost outcome receipts are recovered with unchanged outcome revision. Add a newer same-member correction before lookup/same-body retry; the current correction must win and pending locks clear. This differs from B9's rejected unsaved proposal. |
| E1 | medium / patch | A failed/denied recap read clears snapshot, making terminal false; known-unsent proposals remain locked while their editor and terminal-only discard controls disappear. Offer explicitly local discard when facts are unavailable and no command is pending, with truthful unavailable copy; never discard an uncertain command. |
| R6 | medium / patch | Root follow-up: PrivateWorkdayView's request wrapper calls shorten from any body containing expires_at before the child validates identity/shape. A wrong-workday JSON reply with an earlier live expiry can expire the whole plan and destroy unsaved/recovery state. Remove the unvalidated duplicate propagation; existing bus/resource/progress readers already shorten after full validation. Add a malformed-current-reply regression preserving deadline/proposal through successful revalidation. |
| R7 | high / patch | Root follow-up: validated child reads can invoke shorten after their controller unmounts. The parent callback lacked originating-plan identity, so a held valid A reply could shorten currently open B and later clear B's proposal. Bind callback admission to captured plan.id and test B's rendered deadline/selection/unsent proposal across A release and virtual A expiry. This is an ordinary same-account late-read path. |
| E2 | medium / patch | Bounded edge reinspection found the bus validator parses expires_at without requiring a string. Numeric 2030 can be accepted as an earlier live date and shorten the parent. Require the declared string type and prove malformed bus current replies preserve the deadline and recoverable proposal. |
| V3 | medium / patch | Bounded verification reinspection found R7's arbitrary 50ms wait does not prove the old request's post-response session validation completed before virtual expiry. Add a deterministic completion barrier, assert B's deadline while A is live, and demonstrate failure with only the originating-plan guard removed before restoring it. |
| R8 | medium / patch (test setup) | The complete 334-case browser invocation finished 330 passed / 4 failed in 23.1m. Four existing near-expiry setups subtract calendar days in Europe/Oslo; the actual 2026-10-25 fallback makes the resulting elapsed seven-day retention deadline an hour expired, so draft creation truthfully returns 410. Calculate elapsed subtraction in UTC before rendering Oslo instants; retain all original expiry/guard/late-response assertions and rerun the four cases. No product correction is indicated. |

All retained changes are direct guard/copy/artifact corrections or meaningful verification of already required behavior; no finding is deferred. Root owns historical artifact restoration. The same implementation worker receives bounded patches; final complete verification follows reviewed fixes.

Retained fixes are applied. Two new backend tests passed (4.17s); the expanded browser run first had 36 passes/8 fixture failures. Six measurement failures came from traversing from a disabled/mouse-focused control through browser chrome and triggering current-authority refresh; numeric setup now establishes initial focus once and uses actual Tab/Shift+Tab back, while a separate keyboard-only journey verifies the complete interaction. Two virtual-clock cases now reopen after wall-clock movement to install matching expiry timers. Eleven corrected measurement/keyboard/capacity cases passed (58.1s), both held-expiry cases passed separately, and remaining new invalidation/recovery/discard cases passed in the earlier run. All failed contexts/logs are retained. Original blind, edge and verification reviewers re-inspected their retained scopes and reported no remaining concrete issue. Root restored 38 historical generated PNGs. At that intermediate checkpoint the complete gate was running on frozen source/test hashes: 322 API/PostgreSQL cases passed in 386.47s and browser results were pending. The final delivery section below supersedes this checkpoint.

## Verification

Run frontend production build, focused real PostgreSQL/API and Playwright matrix, isolated verifier controls and full `COMPOSE_PROJECT_NAME=ibe160-private-tests` sequential `scripts/verify-private-drafts.py` gate. Use independent literal Oslo dates/counts and inspect new renders/contrast. Actual iPad/Safari/touch/assistive tech remain unperformed unless tested. Record results/preservation in `docs/evidence/11-3-outcomes-and-close.md`.

## Final delivery verification — 2026-10-25

Final verification: **322 API/PostgreSQL tests passed in 386.47s**, six isolated verifier controls passed, and exact populated PostgreSQL/API restart, repeated migration, raw-state/receipt/deadline preservation, demo denial and production build passed. The complete **334-case browser invocation finished 330 passed / 4 failed in 23.1m**. The four failures were fixture creation returning 410 at the actual Oslo winter-time transition: two fixtures subtracted seven calendar days instead of seven elapsed days. Only those two test setup lines changed to UTC subtraction followed by Oslo conversion; all original behavioral assertions and five-second expiry scheduling remain. **All four affected cases then passed in 23.1s**. Thus all 334 cases have passing coverage, with 330 full-run passes plus four focused reruns; this is not a single all-green 334-case invocation. Frozen source hashes prove no product/backend change after the full run. Literal autumn/spring boundary checks also passed.

All three independent BMAD review layers completed. Every retained finding was fixed and re-inspected; one unsupported blind candidate was rejected with evidence, and nothing is deferred. Final deadline fixes reject malformed replies before propagation, bind late callbacks to the originating plan and require a string bus expiry. The deterministic held-response regression failed with only the plan-ID guard removed, then passed after byte-for-byte restoration. The final UTC fixture correction also passed bounded independent reinspection.

Ordinary local rollout is complete: additive migration 010 is recorded, existing lifecycle ended_at values remain null and the four new tables are empty. Every original business/account/session/security/secret digest and the original database container identity are preserved. The only baseline difference is exactly three already-expired login-throttle rows removed by unchanged startup cleanup; all subsequent comparisons equal that post-worker baseline. Ordinary API/database are healthy, synthetic services stopped, and /private plus both served assets exactly equal the tested frontend/dist build (`index-H35qqbYD.js`, `index-4vMeuoSd.css`). No ordinary account or record was used as a test target.

Owner acceptance remains pending. Actual iPad/Safari, touch hardware, assistive technology and browser chrome zoom were not tested; Edge/Playwright viewport, keyboard, 200% root-text and rendered-image evidence is recorded separately. Existing theme/device obligations remain in 12.3/12.4. No staging, commit, push or next story.

## Owner feedback in progress — 2026-10-25

The owner requests Aktivitetsstatus terminology (retain Fullført manuelt) and confirmed Start/End directly from the activity. Recap and the remaining tested behavior were reported good; full story acceptance remains pending. The [feedback specification](spec-11-3-owner-feedback.md) records execution and verification. Generated A–D import limitations are being investigated separately; no parser fix is claimed.

## Final owner-feedback delivery — 2026-10-25

Root final verification: **119 affected PDF/import tests passed in 13.01s**, **all 351 browser tests passed in one complete invocation (27.3m)**, six isolated verifier/restoration controls passed (0.288s), and the production TypeScript/Vite build passed. The 119-test result is reused with exact backend application/test/migration hashes unchanged; only the reviewed identity-test entry point changed before the final browser run. All nine original independent fixtures and all 65 A–E source activities / 34 movements are covered; actual A–E upload/adoption/save/reopen verifies source rows, endpoints, calendar dates, expected uncertainty and duty/CAR anchors. New actual keyboard journeys cover activity Start cancel/confirm, status Save, End/Abort cancel/confirm, exact member identity, request counts, terminal consultation and cross-window recovery.

All three independent BMAD layers completed and re-inspected the retained corrections with no remaining concrete issue. Thirteen review candidates were adjudicated individually: one 401 claim was rejected because the production workspace wrapper already clears session/presentation before the child catch; the other twelve technical/test/documentation findings were fixed. Root additionally corrected the three dynamic Start/account-switch fixture entry points (FR14), with unchanged zero/one-write/server-state assertions, six focused passes and bounded verification reinspection. Nothing is deferred. The continuation negative control failed exactly the three mismatched/no-current heading cases when only that guard was removed; byte-restored source passed all nine boundary cases.

The ordinary local API and frontend now serve the tested version. No new schema/API/storage migration was required by this feedback correction. The full 21-table preservation comparison passed: all business/account/session/security row fingerprints, including the owner’s newly tested activity statuses, start/closure records and receipts, are unchanged; the original database container identity and secret are unchanged. Exactly three expired login-throttle rows were removed by unchanged startup cleanup; all business/account/session/security records are preserved. Ordinary services are healthy and synthetic services are stopped. Private HTML and both served JS/CSS assets exactly match the tested dist build. Every original/generated PDF and independent fasit file remains byte-identical. Pre-feedback screenshots/contrast JSON, including uncommitted 11.3 artifacts, are restored from the preserved dirty-tree snapshot; current rerenders are archived and separately named feedback evidence remains.

Owner acceptance remains pending. B intentionally retains its unclassified 16:20 Travel to (start/end/type unknown); D retains two unstructured source-note warnings while all 16 activities/endpoints are imported. A/C/E have bounded-layout qualification with no unresolved source lines. The nine original interpretations retain their source uncertainties, including Example 6. Physical iPad/Safari, touch hardware, assistive technology and browser chrome zoom remain untested; viewport/keyboard/200% root-text evidence does not replace those later 12.3/12.4 obligations. No staging, commit, push or next story. Story 11.3 finishes in review for the owner.

The first root attempt passed the same 119 import cases/build and was deliberately stopped after 23 completed browser passes / zero failures when an audit found the three unadapted dynamic Start fixtures. Remaining cases were unrun. Only the identified descendant Playwright process was stopped; the Python finally restored ordinary services and the fresh 21-table comparison passed. Archived first logs: tmp/11-3-feedback-root-first-gate.log and tmp/11-3-feedback-root-first-browser.log. The corrected six-case identity subset passed in1.2m; an earlier grep-only command found no tests and is not counted as a test pass. The complete final 351-case run supersedes the interrupted browser checkpoint; all earlier product/fixture failures remain documented below.

## Owner acceptance and publication authorization — 2026-10-25

Jonas explicitly accepted story 11.3, including the activity-status/shift-action and generated-PDF owner-feedback corrections, on 2026-10-25 and instructed commit and push. Owner acceptance is accepted; implementation is done. The earlier pending/review/stop-before-publication statements are historical checkpoints superseded by this instruction. Stories 11.4 onward remain backlog and no next story is started. Publication is authorized; actual commit/push results are checked through Git after execution.
