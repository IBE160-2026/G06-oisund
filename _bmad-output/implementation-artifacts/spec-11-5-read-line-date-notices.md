---
title: '11.5 — Read line/date notices'
type: feature
created: 2026-10-25
status: in-review
route: dispatch
review_loop_iteration: 0
baseline_commit: aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed
story: '11.5'
story_key: 11-5-read-line-date-notices
owner_acceptance: pending
context: []
---

Owner rejected the per-shift notice behavior on 2026-10-26. This frozen contract and its test results are historical and superseded on scope/ending/retention by the [cross-day register correction](spec-11-5-cross-day-notice-register.md). No owner acceptance has been recorded.

<frozen-after-approval reason="Owner authorizes autonomous planning, implementation and verification without another approval checkpoint">

## Intent

Read saved manual notices relevant to confirmed-day lines and explicit calendar intervals in a separate day-linked reader, with line/date filters. Preserve the accepted 11.4 maintenance/editor and its proposals. Each notice appears once with every matching line; separately recorded incidents remain separate.

## Boundaries & Constraints

**Always:** Server-owned projection and authorized no-store reads. Exact explicit line identifiers (trim surrounding whitespace, preserve leading zeros/case; never extract numbers from route headings). Explicit all-line scope matches all known confirmed lines and remains visible if lines are unknown. Default all planned dates/lines; offer confirmed line and Oslo calendar-date choices. Compare fully known notice validity to the union of confirmed planned activity intervals clipped to the selected calendar date, independently of selected activity or wall clock. Inclusive interval endpoints; calendar days end exclusively at next Oslo midnight. Exclude fully known non-overlap. Retain unknown/partial validity as visibly qualified candidates, without treating missing endpoints as unlimited certainty. Warn about unknown lines/unmatched headings and source coverage. Retain manually ended candidates with their explicit status; status/check/edit timestamps never infer relevance, clearance or freshness. Display complete source facts using 11.4 NoticeFacts, including explicit check versus prior check/unchecked state.

**Never:** No migrations, new stored fields, source fetch, exact trip/stop relevance, inferred closure, offline storage, demo expansion or 11.6 recovery redesign. No manual acceptance, staging, commit, push or next story. Tests target disposable synthetic data only; preserve ordinary services, records, secret, evidence and local changes.

## I/O & Edge-Case Matrix

| Scenario | Input/state | Expected behavior | Failure handling |
|---|---|---|---|
| Shared/separate | Shared 20/24 and another 20 incident | Shared once with both matches; separate remains | No title-based dedup |
| Date/line | Midnight, gaps, offset/DST, exact tags | Explicit planned intervals/date clipping, known non-overlap excluded | Unknown line/date clearly qualified |
| Uncertain validity | No endpoints or one endpoint | Retained candidate, visibly unknown/partial | No invented endpoint |
| Status/source | Unchecked, checked then edited, manually ended | Independent status/check/source facts | Never infer current clearance |
| Empty/unavailable | Zero stored, zero matches, failed/malformed/late read | Distinct honest states; no coverage claim | Hide untrusted/stale reader results; retry bounded read |
| Navigation/access | Dirty editor, chosen activity, terminal, expiry/account change | Separate views; proposals/selection/recovery retained; terminal reader usable | Existing authority/loss guards win |

</frozen-after-approval>

## Code Map

- `backend/app/workday_notice_storage.py`: existing bounded notice rows, parent locking/authorization/rechecks; additive reader function reuses these.
- `backend/app/workday_notice_domain.py`, `private_main.py`: NoticeRecord source-Oslo serializer and typed route patterns. New `notice_reader_domain.py` owns pure filtering/projection schemas; avoid divergent browser matching.
- `frontend/src/PrivateNotices.tsx`: retained maintenance controller, strict record validation and NoticeFacts; export reuse, preserve mutation/recovery semantics.
- `frontend/src/PrivateWorkdayView.tsx`: separate screens above mounted day/activity controllers; integrate retained read-only reader with clear reader/day/maintenance navigation and focus.
- `frontend/tests/private-activity-helpers.ts`: disposable account and confirmed 20/24 midnight fixture. `backend/tests/test_private_notices.py`: API fixtures/expiry/ownership; new reader tests reuse them.
- `scripts/verify-private-drafts.py`: full sequential disposable gate/restoration. Existing `tmp/11-4-feedback-preservation.py` demonstrates read-only ordinary fingerprints; create fresh 11.5 baseline and use new evidence names.

## Tasks & Acceptance

- [x] `backend/app/notice_reader_domain.py`, `workday_notice_storage.py`, `private_main.py` — typed read-only server projection, bounded filters and authority rechecks.
- [x] `frontend/src/PrivateNoticeReader.tsx`, `PrivateWorkdayView.tsx`, `PrivateNotices.tsx` — retained reader, filters, complete facts, navigation, explicit empty/unavailable states and accessible focus.
- [x] `backend/tests/test_notice_reader.py`, `frontend/tests/private-notice-reader.spec.ts` — matrix tests, API persistence/privacy, rendered Day/Night, keyboard/narrow/enlarged screens and unchanged saved state.
- [x] `docs/evidence/11-5-line-date-notices.md`, `README.md`, `docs/development-log.md`, epic/story/spec/sprint — actual verification, choices, review and owner walkthrough, pending manual acceptance.

Given saved 20/24 notices, when the reader/filter opens, then one shared candidate lists both matching lines and independent incidents remain distinct.
Given known non-overlap or uncertain validity, when filtering planned intervals, then only proven non-overlap is excluded and uncertainty stays explicit.
Given navigation/failure/closure, when consulting, then saved selection, proposals and manual states remain unchanged and failed reads cannot assert an empty successful result.

## Implementation Notes

No intent gaps remain. No irreversible change or storage migration is required; footprint is additive API/domain/UI/tests. Full dispatch is appropriate because server filtering, authority and multi-screen navigation need coordinated verification. Root owns the workflow, final independent review, memlog/documentation and final gate. Worker implements and runs focused checks sequentially, preserving services/data/evidence; do not launch another Build workflow. Escalated Docker/browser commands may be necessary in this Windows sandbox. Preserve old screenshots; use 11-5 filenames. Root will handle ordinary rollout after review. Read the companion [implementation plan](../specs/spec-11-5-read-line-date-notices/implementation-plan.md).

## Spec Change Log

## Review Triage Log

All three BMAD layers completed on the stable 69-API/19-browser checkpoint. Two snapshot instruction reads initially failed under the sandbox; read-only escalation succeeded and both layers then completed. Edge tracing returned no findings. Each finding is classified separately before grouping below; no product intent gap remains.

| ID | Verdict / route | Verification and resolution |
|---|---|---|
| B1 retained choices during suspension | false / reject | PrivateDrafts.tsx hides the entire retained subtree synchronously when access is suspended, and PrivateAccess keys/clears it on identity loss. `available=false` can mean a failed bus/start/selection resource read, not revoked plan ownership; disabled choices describe immutable confirmed plan facts. Reader denial clears choices, and account/session tests remove the whole plan. The alleged exposed private choices on suspension are not user-visible. |
| B2 non-trip missing-line warning | low / patch | The counter includes Coffee/MealBreak and other intentionally line-free activities; wording incorrectly calls every blank an unknown line. Directly describe activities without an entered line, without inventing classification or missing-fact obligations. Same as root's observed wording issue. |
| B3 400-date capacity | low / reject | Confirmation can admit an activity spanning over 400 dates, and projection safely reports 422. Such a multi-year workday is outside everyday consultation; replacing the bounded date selection requires more than a direct correction. Keep the explicit bounded unavailable result and document this technical limit; no silently partial date list. |
| B4 contradictory candidate metadata | medium / patch | `valid()` currently permits a selected-scope candidate with empty matches or matches excluding the requested line. Add direct consistency checks on the existing fields before trusting success; no browser recomputation of temporal relevance. |
| B5 manual ending caveat absent in UI | low / patch | The reader shows manual-ended status and generic coverage warnings but the explicit road-clearance qualification appears only in README. Add a short visible qualification beside the reader's scope explanation. |
| B6 independent line/time behavior unprotected | medium / patch | Projection intentionally compares exact day lines independently of the union of day intervals, so a line-20 notice may overlap only a line-24 interval. Add an explicit regression demonstrating this day-level candidate contract without precise-trip implications. |
| B7 all-lines on no-known-lines browser gap | medium / patch | Pure projection covers it but no actual saved/API/browser journey exercises the no-known-lines response and visible fallback. Add that focused synthetic flow. |
| B8 maximum reader capacity gap | medium / patch | The new bounded single read bypasses maintenance pagination. Add a real API/serialization/filter regression at 200 notices, 200 exact plan lines and 50 notice tags to detect accidental truncation. |
| B9 complete malformed candidate gap | medium / patch | The existing malformed payload only lacks fields. Add a complete contradictory candidate case alongside B4 and assert old results are hidden with honest unavailable status. |
| B10 per-control focus gap | medium / patch | Render measurement verifies back-button focus and every control's text/border, but not each reachable filter/refresh/maintenance/summary/source-link focus. Extend keyboard/focus measurements to each enabled control/link and retain unavailable-state coverage. |
| V1 mixed-tag candidate warning gap | medium / patch | Pre-verified gap: neither pure/API nor browser tests assert candidate `line_uncertain`/`unmatched_tags` when one tag matches and another does not. Extend existing filter test with a retained mixed-tag notice and assert exact matching line, unmatched heading and warning. |

Patch groups: B2; B4/B9; B5; B6; B7; B8; B10; V1. All are direct copy/validation corrections or tests of demonstrated existing states; no new public surface, lifecycle or filtering rule is introduced. B1 is refuted; B3 is rejected under the workflow's rare-low-complexity rule, with its bound recorded as a limitation. No finding is deferred.

### Patch reinspection

The original blind reviewer re-inspected B2 and B4–B10 and confirmed every accepted finding resolved, with no introduced defect. The original verification reviewer confirmed that forcing false mixed-tag uncertainty or removing its candidate warning now fails the expanded assertions. Both reinspections were read-only. Root inspected the patched validation, keyboard fragment measurement, capacity regression and complete malformed payload cases. Focused patch evidence: 10 reader backend tests passed; unaffected browser cases passed, then all nine corrected/matrix cases passed after fixing the multiline-link measurement geometry. Root's complete sequential verifier is the final source-stable gate; its outcome is recorded below after execution. All matrix rows map to executed reader/API/browser tests; no criterion relies on planning text or owner acceptance.

Root gate finding R1: low / direct verifier-fixture correction. The first full gate passed 411 API tests, then exposed the existing lexical timestamp comparison against a minute-precision input and second-precision accepted serializer. Change only the synthetic input to its canonical second precision, keeping the exact metadata assertion intact. The original blind reviewer independently confirmed the same instant/accepted serializer, unchanged assertion strength and no product behavior change. Seven restoration controls and ordinary preservation passed after the failed run; repeat the complete gate under a fresh log/source manifest. This is a test-fixture fix, not deferred product work.

Root gate finding R2: medium / direct browser-harness correction. Full browser run passed 424/426 cases; both failures were the pre-existing `activityScreen()` check-then-click race before the actual held-account/outcome or enlarged-owner scenario. Saved selection auto-opens details in an effect, removing the transient open button between `isVisible()` and `click()`. All 106 captured files and 18 original fixture/oracle files were unchanged through the full run; all 26 reader cases passed. The only later source delta is the shared test helper: bounded retry handles the view transition and always asserts actual selected details. The original blind reviewer confirmed unchanged business/security assertions, access/navigation guards and saved selection. Root reruns the eight affected scenarios three times; product code/build remains unchanged.

### Final executed result

411 backend tests passed in 478.66s; populated PostgreSQL/API restart, repeated migrations, exact raw state/receipts/deadlines/session preservation, cleanup and production build passed. Complete browser run: 424/426 in 31.0m, including all 26 new reader cases. After R2's test-helper correction, all eight affected scenarios passed three times (24/24, 2.5m). Seven verifier restoration controls passed. No accepted finding remains unresolved or deferred. This reports the failed full-run setup cases and scoped correction honestly; it does not relabel the 31-minute run green.

Final ordinary rollout is healthy, all 23 raw tables/secret/original database identity preserved; synthetic services stopped. All 106 files are stable after the documented helper-only checkpoint, all 18 source/oracle/PDF files are unchanged, and 277 pre-existing evidence files remain byte-identical after archiving/restoring 134 broad rerenders. Served private HTML/assets and 42 runtime backend/migration files match tested dist/source. Assets: index-ormeQgnH.js / index-8lnBnkIq.css. See [final evidence and owner walkthrough](../../docs/evidence/11-5-line-date-notices.md). Implementation is complete; specification stays in-review and sprint review pending manual owner acceptance. No staging, commit, push or next story.

## Verification

Target-platform correction from the owner, 2026-10-26: physical acceptance testing is planned on Lenovo Pad with Android and Brave, over the mobile network to the server on the desktop at home. This physical test remains unperformed; executed desktop Edge/Playwright results below are preserved and do not qualify that device/network. iPad/Safari is not the planned setup. Both stories still await manual acceptance. This documentation correction adds no product changes or test executions.

Focused real PostgreSQL/API and browser tests; production build; broad sequential disposable verifier and its restoration controls. Inspect rendered Day/Night at 768/1024/1440 and 200% text, plus narrow viewport. Record actual failures and hardware limitations. Preserve ordinary raw table fingerprints, database identity and secret, then serve tested assets locally. Pending owner acceptance is not done.

Owner acceptance update, 26 October 2026: Jonas explicitly accepted corrected story 11.5 (`Godkjent.`). Its account-owned cross-day/expiry delivery is done; existing 11.6 remains review. Earlier pending-acceptance statements describe historical checkpoints. This does not authorize commit/push or further work, finalize the retrospective, close Epic 11, or establish physical-device qualification.
