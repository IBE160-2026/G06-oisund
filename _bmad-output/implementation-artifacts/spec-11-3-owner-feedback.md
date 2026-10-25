---
title: '11.3 owner feedback — activity status and shift actions'
status: done
approved_on: 2026-10-25
type: fix
route: dispatch
review_loop_iteration: 0
created: 2026-10-25
story: '11.3'
story_key: 11-3-record-outcomes-and-close
implementationStarted: true
owner_acceptance: accepted
owner_accepted_on: 2026-10-25
baseline_commit: b42f1e8fa66ad5026f1751f31ddad50c3acbc7d6
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/spec-11-3-record-outcomes-and-close.md
  - D:/IBE160/_bmad-output/specs/spec-11-3-record-outcomes-and-close/SPEC.md
  - D:/IBE160/_bmad-output/specs/spec-11-3-record-outcomes-and-close/implementation-plan.md
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-11-context.md
  - D:/IBE160/_bmad-output/planning-artifacts/ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md
  - D:/IBE160/_bmad-output/planning-artifacts/ux-designs/ux-IBE160-2026-09-22/DESIGN.md
---

<frozen-after-approval reason="owner requested these corrections after hands-on testing, 2026-10-25">

## Intent

The owner found the recap good and other exercised behavior working. The outcome label is confusing with network outage: use **Aktivitetsstatus** in the Norwegian UI, retaining **Fullført manuelt** because completion is explicit. Since selection automatically opens the activity screen, provide explicit Start and End shift there, with confirmation. Preserve selection, Start and status saving as separate actions; no automatic completion/start. This is a scoped correction to delivered 11.3, not owner acceptance of the final story.

## Boundaries and constraints

Retain all prior active-only recording, exact-member correction/unknowns, current-authority/expiry, receipts, identity, unsaved/recovery, terminal read-only, separate-screen and privacy contracts. Keep the existing recap and its data/content. Use clear Norwegian ordinary copy: activity status, save activity status, registered/unregistered status; internal outcome enum/API/storage names remain unchanged. Do not confuse an activity's Avbrutt status with aborting a whole shift.

Start and End/Abort must be naturally accessible from the selected activity, alongside enough current lifecycle context. Starting must require explicit confirmation/cancel with no request on cancel; day and activity entry points should have consistent confirmation. Reuse one mounted lifecycle controller and existing receipt recovery, never independent competing Start state. End/Abort uses the existing separate closure review/counts/unknowns/cancel/recap. Cancel restores the invoking activity and focus, rather than forcing day navigation; confirm still opens recap. Keep these actions behind current authority, pending/unsaved guards and terminal restrictions. Long/enlarged Day/Night activity screens must wrap and scroll, with one primary screen visible. No notices, parser expansion, database migration, persistent private browser storage, commit, push or next story.

## I/O and edge-case matrix

| Scenario | Expected behavior |
|---|---|
| Before Start | Read/select/details; activity Start opens confirmation; cancel sends no mutation; no status save |
| Explicit confirmed Start | Original server Start accepted once; remain on selected activity, status saving now available; selection unchanged |
| Active activity | Explicit save/correct with Aktivitetsstatus wording; End/Abort enters existing separate confirmation |
| Cancel closure from activity | No close request; return to exact activity with focus on invoking control and retained proposals |
| Accepted closure | Existing unchanged recap; no restart/edit; terminal activity consultation stays read-only |
| Dirty/pending/unavailable | Reachable original recovery, no bypass/lost proposal/assumed authority, late responses do not reopen another screen |
| Keyboard/long/enlarged Day/Night | Visible labeled actions, focus returns, scrolling/no clipping, original contrast/control floors retained |

</frozen-after-approval>

## Code map and plan

Current lifecycle controller is `frontend/src/PrivateShiftStart.tsx`, mounted inside a day-only hidden div in `PrivateWorkdayView.tsx`; its fresh Start calls send immediately. Do not create two controllers. Share/reposition the existing controller or expose its view safely across day/activity presentation. `PrivateActivitySelection.tsx` owns activity detail/navigation; `PrivateWorkdayProgress.tsx` owns status editor, close confirmation and recap. The existing close hook stores returnTo focus but navigates back to day; preserve actual origin across close/cancel. Shared locks originate in PrivateConfirmation/PrivateDrafts; keep original aggregate protection.

Terminology is visible in the progress hook/editor/screens, day labels/paused groups, view copy and accessible status/region names; update affected test selectors semantically without weakening assertions. Public protocol outcome names and saved values are intentionally unchanged. `Fullført manuelt` remains exactly that.

Baseline source is already dirty from the uncommitted 11.3 implementation. Preserve it. A byte-preserving snapshot of 742 existing tracked/untracked files is in ignored `tmp/11-3-feedback-baseline`; original HEAD/index are unchanged. Root owns current ordinary-state fingerprints, test service admission/restoration and final served-build verification. Coordinate shared services sequentially. Read and edit source freely, but wait for root's admission message before service changes or private tests. Only disposable `ibe160-private-tests` accounts/database may be test targets. Ordinary data includes the owner's latest hands-on changes and must be fingerprinted anew before test/service changes. Do not reuse the old migration-before baseline or assume outcome tables are empty.

Owner import decision, 2026-10-25 (explicit reply): **extend import to the existing generated test files**. This authorized amendment supersedes the initial parser-expansion exclusion in the frozen UI block, whose bytes remain preserved as historical approval. Do not replace or edit PDFs or independent fasit. Existing 10.2 evidence and tests explicitly document A=2/5 partial, B=conflicting_headers rejected, C=6/15 partial, D=conflicting_headers rejected, E=8 work rows; these are the starting defects, not acceptance expectations for this correction. Nine originals remain the approved realistic fixture set.

Extend actual bounded parsing in `backend/app/pdf_import.py` and mapping only as necessary. Inspect the actual PDF layouts/text and trace dropped rows/header conflicts. Read `Eksempelfiler/Fasit-testskift.json` as an independent TEST oracle and `Eksempelfiler/Fasit-testskift.pdf` / source PDFs as needed. Runtime must never read fasit, fixture filenames, expected IDs or hardcode their rows. Preserve no-store/transient file boundaries, limits, safety and source provenance. Accept genuinely repeated page headers; do not weaken rejection of genuinely conflicting shift/date/start/end/source identities. Preserve zero-duration rows, unknown one-ended Travel to, gaps without invented activities, header end versus last actual activity, adjacent and repeated trip identities, CAR handover/return and overnight dates. Import must include ALL source activity/movement rows and correct movement endpoints, route/trip identities and proved calendar instants. Unsupported uncertainty remains explicit, not guessed to make fixtures pass. Intermediate-stop extraction/display and distance qualification remain outside V1; endpoints still must include the actual last stop without duplication. No new schema or production data rewrite.

Add independent assertions for all A–E source activity rows/endpoints/dates against fasit, replacing prior assertions that merely preserved known A–D rejection/partial behavior. Keep robust malformed/conflicting-header/unsupported-layout denials. Run the nine original independent source/provenance fixtures and their mapping regressions with this parser change; previously qualified facts must remain identical and Example 6's genuine source uncertainty must remain truthful. Browser-upload all generated A–E using the actual private import route; show full row counts/critical facts and adopt/save/reopen at least the previously rejected and overnight cases, keeping selection/start/status separate. Keep all real/private owner accounts out of testing. Update README/evidence to distinguish new supported source rows/endpoints from unqualified OCR/arbitrary layouts/stops.

## Tasks and acceptance

- [x] Replace user-facing outcome terminology with Aktivitetsstatus while preserving Fullført manuelt, receipt/enum/backend contracts and recap content.
- [x] Expose consistent confirmed Start and existing End/Abort from activity with one mounted lifecycle owner; preserve current authority, selected member, unsaved/pending protection.
- [x] Restore exact origin/focus after cancelling Start/closure, leave selection unchanged, preserve terminal read-only behavior.
- [x] Extend bounded PDF import for existing A–D files and independently verify all A–E activities/endpoints/dates, preserving all nine original fixtures, true header-conflict denials, source provenance/unknowns and original files.
- [x] Add meaningful real API browser coverage for activity pre-start/cancel/confirm/save, activity End/Abort cancel/confirm, known/uncertain failure/locks and terminal consultation; adapt affected existing Start helpers to explicitly confirm.
- [x] Build, run focused affected suites, inspect new enlarged Day/Night screens and record exact results; root performs independent review, relevant broader regression, new ordinary preservation and verified local runtime handoff.

Given an unstarted selected activity, starting opens a review with Cancel/Confirm and sends zero Start requests until confirmed. Given cancellation from the activity, exact selection and focus remain; confirming Start records only original Start once, stays on activity and enables activity status. Given an active selected member, cancelling closure preserves server state and returns focus; confirming closure uses existing read-only recap with unknowns unchanged. Given uncertain writes or denied facts, activity actions cannot bypass original guards or lose recovery. The UI correction requires no lifecycle API/storage/schema change; bounded parser changes are separately owner-authorized above.

## Verification

Run only affected checks during implementation; root owns the relevant broader pass after review. Include keyboard-only activity→Start confirmation→cancel/confirm→status Save→End confirmation→cancel/confirm→recap, selection/Start/close request counts, exact selection and retained state. Test pending Start/failed lookup and status/bus dirty guards across screens; original operation identity/retry behavior survives. Render at narrow/wide Day/Night with 200% text and long activity labels; inspect no clipping/focus and existing IR-01 numerical floors. No claim of physical tablet/Safari/assistive-tech testing. All private tests use the isolated synthetic project, finally stop it and restore ordinary services. Record exact passed/failed/not-run and preserve earlier evidence. Owner acceptance remains pending; stop before commit/push/next story.

## Implementation notes

The owner authorized these corrections directly; no additional approval checkpoint is required. Root may update documentation/specification/UX tracking from actual results; do not edit either approved frozen block. Independent reviewers receive the delta against the preserved feedback baseline and the frozen main story context remains intact. Keep failed logs and separate new screenshots under 11.3 feedback names; restore only newly regenerated historical artifacts.

## Spec change log

2026-10-25: Owner feedback adds terminology and direct activity shift actions with confirmation. KEEP: recap, active-only status, selection independence, existing Start/closure receipts and privacy/recovery, all original ordinary records and local implementation.

## Review triage log

All three required independent layers completed before triage: blind floor10 candidates, edge0, verification1 gap plus2 other findings. The verification instruction initially hit a read ACL; its authorized read-only escalated retry succeeded before the actual review. Each finding is adjudicated below; no candidate is silently merged or omitted.

| ID | Verdict / route | Evidence and disposition |
|---|---|---|
| FB1 | medium / patch | Active consultation can retain proposals for multiple members while the day only shows saved values and a generic lock message. Reuse the existing exact-member local-proposal summary/discard surface during active consultation, with honest copy and no discarding uncertain commands. |
| FB2 | medium / patch | Outcome recovery remains reachable after navigating to another member, but generic retry/check labels omit the original command member/value. Show that immutable local intent next to recovery and prove retry still targets the original member. |
| FB3 | false / reject | The claimed leaked 401 is disproved by the sole production request caller: PrivateAccess.tsx workspace wraps every private read and clears the current session/presentation on 401 before rethrowing (lines94–100 and240). Stale epochs are separately guarded. The child bare catch cannot preserve an authenticated workspace after this read; no duplicate expiry branch is added. |
| FB4 | medium / patch | Current snapshot comparison checks lifecycle/outcome revisions but omits bus. Include the bus monotonic invariant against a stale otherwise-valid current projection so recap cannot replace an already acknowledged higher bus revision; add focused stale-projection verification. |
| FB5 | medium / patch | The new footer continuation-notice branch silently ignores a line/trip mismatch or absent current movement. Validate its identity before suppressing it; contradictory source evidence must be rejected/preserved, not hidden. |
| FB6 | medium / patch | New-format first-time-column semantics depend on a separate movement heading in that same column. A matching continuation document/column with only activity rows can incorrectly turn an unclassified clock into an end. Retain proven format across relevant columns/pages and test this case while preserving original6 legacy one-ended behavior. |
| FB7 | low / patch | Browser import evidence writes qualification/codes without independently asserting them. Assert the expected A/C/E empty uncertainty, B time uncertainty and D note uncertainty before save/reopen. Existing backend coverage does not replace this consumer check. |
| FB8 | medium / patch | New generated browser checks compare source rows and saved equality, but not independent expected vehicle-duty boundaries/CAR attachment. Derive expected anchors from source fasit and verify them after adoption/save/reopen; do not use parser output as oracle. |
| FB9 | medium / patch (root documentation) | The active Epic context contains literal question marks in Fullført/A–D/owner's because a root stdin documentation write used the wrong character encoding. Repair the affected current planning/documentation text with UTF-8-safe writes, preserving approved frozen blocks. |
| FB10 | low / patch (root documentation) | The enclosing section is already labelled pre-feedback, but its bare final sprint statement can still be mistaken for current status. Prefix that statement explicitly as historical; final current status will be synchronized from actual results. |
| FV1 | medium / patch | Pre-verified gap: matching B continuation is covered, but mismatched line/trip or a continuation without current movement is not. Add genuine PDF negative cases; an unconditional acceptance mutation must fail them. |
| FV2 | medium / patch | private-outcomes.spec.ts:505 expects a substring not rendered by the renamed local-proposal summary. Correct the stale copy assertion while preserving unavailable/deleted no-write, discard and lock-release behavior. |
| FV3 | medium / patch | unclassified_time is mapped in import review/backend, but draftInterpretation.importIssues lacks the known code. Adopted B displays an internal unknown-code warning. Add the readable shared-consumer mapping and assert it after adoption/reopen. |
| FR14 | medium / patch | Root audit found three existing dynamic Start/account-switch fixtures only click the new local Start-review opener. They never reach mutation preflight/held POST/current-read and would fail or wait indefinitely. Open/review Start before route installation/identity change, then test Confirm with unchanged zero/one-write and server-state assertions. The first root gate passed119 affected import checks in13.01s/build, then was deliberately stopped after23 browser passes/0 failures; all remaining cases are unrun, not passed. Logs are archived. No product correction is required. |

All retained findings are bounded corrections or meaningful verification of the approved activity/recovery and generated-import contracts. No new API, schema, notices or arbitrary-layout feature is required; none is deferred. The existing implementation worker receives the technical patches; root owns documentation repair, broader verification and runtime handoff.

## Focused implementation checkpoint

Worker completed the authorized UI and parser corrections. Current affected import suites:110passed10.99s; new browser matrix13passed1.2m and final terminal-refresh Start-review regression1passed7.6s. Build passed. Root read the new source/test delta and rendered enlarged narrow Night activity screen, and fresh ordinary-state comparison passed after worker restoration. Original PDFs/fasit hashes are unchanged. Product source is frozen in tmp/11-3-feedback-worker-final-source-hashes.json. Broader regression and independent review remain pending; see docs/evidence/11-3-owner-feedback.md for retained failures and exact limits.

## Retained review patch verification — 2026-10-25

The active proposal summary now identifies each known-unsent member/value and allows independent local discard; source details appear only while facts are authorized. Uncertain commands remain undiscardable and their recovery surface names the immutable original activity/value after navigation. Current recap admission also preserves acknowledged bus revision monotonicity. The renamed unavailable/deleted-proposal assertion uses the actual copy, with no-write, hidden-facts and lock-release checks retained.

Continuation headings and footer notices now require a matching preceding movement identity. Separated-heading format admission is retained across document columns/pages, while original Example 6 semantics remain unchanged. Genuine PDF tests cover valid and wrong-line/wrong-trip/no-current evidence independently for heading and footer, plus activity-only columns/pages. Adopted/reopened B warnings use readable unclassified-time copy. Browser imports independently assert A/C/E clean qualification, B's three genuine unknown-time codes, D's two source-note codes and source-event-derived vehicle/CAR boundary anchors through adoption/save/reopen.

Exact focused results: edited PDF suite **94 passed in 6.60s** (`tmp/11-3-feedback-review-pdf-final.log`). An intentional heading-only unconditional-acceptance mutation produced **3 expected failures / 1 pass** in 0.92s; the three failures were mismatched line, mismatched trip and no preceding movement. Parser source was restored byte-for-byte, rebuilt, and all **9 continuation/format cases passed in 1.45s** (`tmp/11-3-feedback-review-pdf-restored.log`). Focused browser run **10 passed in 53.6s**, including all five strengthened generated imports (`tmp/11-3-feedback-review-browser-first.log`). After the final availability gate for identifying source details, the five progress/privacy cases passed again: **5 passed in 28.5s** (`tmp/11-3-feedback-review-progress-final.log`). Production build and diff whitespace check passed. The first PDF run's 92 passes / 2 failures came from the synthetic font mapping `å` to an unmapped glyph; genuine fixtures now declare WinAnsi encoding. Failed log retained.

No wider suites were run by the worker. Root owns bounded reinspection, broader verification and final ordinary preservation/served-build checks. Owner acceptance remains pending; no commit/push/next story.

## Final owner-feedback delivery — 2026-10-25

Root final verification: **119 affected PDF/import tests passed in 13.01s**, **all 351 browser tests passed in one complete invocation (27.3m)**, six isolated verifier/restoration controls passed (0.288s), and the production TypeScript/Vite build passed. The 119-test result is reused with exact backend application/test/migration hashes unchanged; only the reviewed identity-test entry point changed before the final browser run. All nine original independent fixtures and all 65 A–E source activities / 34 movements are covered; actual A–E upload/adoption/save/reopen verifies source rows, endpoints, calendar dates, expected uncertainty and duty/CAR anchors. New actual keyboard journeys cover activity Start cancel/confirm, status Save, End/Abort cancel/confirm, exact member identity, request counts, terminal consultation and cross-window recovery.

All three independent BMAD layers completed and re-inspected the retained corrections with no remaining concrete issue. Thirteen review candidates were adjudicated individually: one 401 claim was rejected because the production workspace wrapper already clears session/presentation before the child catch; the other twelve technical/test/documentation findings were fixed. Root additionally corrected the three dynamic Start/account-switch fixture entry points (FR14), with unchanged zero/one-write/server-state assertions, six focused passes and bounded verification reinspection. Nothing is deferred. The continuation negative control failed exactly the three mismatched/no-current heading cases when only that guard was removed; byte-restored source passed all nine boundary cases.

The ordinary local API and frontend now serve the tested version. No new schema/API/storage migration was required by this feedback correction. The full 21-table preservation comparison passed: all business/account/session/security row fingerprints, including the owner’s newly tested activity statuses, start/closure records and receipts, are unchanged; the original database container identity and secret are unchanged. Exactly three expired login-throttle rows were removed by unchanged startup cleanup; all business/account/session/security records are preserved. Ordinary services are healthy and synthetic services are stopped. Private HTML and both served JS/CSS assets exactly match the tested dist build. Every original/generated PDF and independent fasit file remains byte-identical. Pre-feedback screenshots/contrast JSON, including uncommitted 11.3 artifacts, are restored from the preserved dirty-tree snapshot; current rerenders are archived and separately named feedback evidence remains.

Owner acceptance remains pending. B intentionally retains its unclassified 16:20 Travel to (start/end/type unknown); D retains two unstructured source-note warnings while all 16 activities/endpoints are imported. A/C/E have bounded-layout qualification with no unresolved source lines. The nine original interpretations retain their source uncertainties, including Example 6. Physical iPad/Safari, touch hardware, assistive technology and browser chrome zoom remain untested; viewport/keyboard/200% root-text evidence does not replace those later 12.3/12.4 obligations. No staging, commit, push or next story. Story 11.3 finishes in review for the owner.

The first root attempt passed the same 119 import cases/build and was deliberately stopped after 23 completed browser passes / zero failures when an audit found the three unadapted dynamic Start fixtures. Remaining cases were unrun. Only the identified descendant Playwright process was stopped; the Python finally restored ordinary services and the fresh 21-table comparison passed. Archived first logs: tmp/11-3-feedback-root-first-gate.log and tmp/11-3-feedback-root-first-browser.log. The corrected six-case identity subset passed in1.2m; an earlier grep-only command found no tests and is not counted as a test pass. The complete final 351-case run supersedes the interrupted browser checkpoint; all earlier product/fixture failures remain documented below.

## Owner acceptance and publication authorization — 2026-10-25

Jonas explicitly accepted story 11.3, including the activity-status/shift-action and generated-PDF owner-feedback corrections, on 2026-10-25 and instructed commit and push. Owner acceptance is accepted; implementation is done. The earlier pending/review/stop-before-publication statements are historical checkpoints superseded by this instruction. Stories 11.4 onward remain backlog and no next story is started. Publication is authorized; actual commit/push results are checked through Git after execution.
