---
epic: 11
date: 2026-10-26
status: preliminary-draft
criteria: declared
acceptance_decision: pending-manual-owner-testing
final_retrospective: false
---

# Epic 11 retrospective — PRELIMINARY DRAFT

**Subsequent owner result, 26 October 2026:** Jonas rejected 11.5's per-shift notice behavior after manual use. The [cross-day corrective specification](spec-11-5-cross-day-notice-register.md) and [execution report](../../docs/evidence/11-5-crossday-register.md) supersede the earlier notice-scope assessment below. Preserve this preliminary retrospective as historical evidence; it has not been finalized, and no owner acceptance or epic closure is inferred from the corrective delivery.

This is preparation for the retrospective, not a completed retrospective or an acceptance decision. Stories 11.5 and 11.6 are implemented and independently reviewed, but Jonas has not accepted them. Their forthcoming manual results must be added below before finalizing this document. Epic 11 remains in-progress; its retrospective remains optional; Epic 12 remains backlog. No story, epic or action-item status is changed by this document.

## Scope, instructions and evidence

The owner explicitly requested this unfinished-epic review and restricted this session to reading evidence and writing this draft: preserve all existing local changes; no product/test edits, new tests, runtime exercise, approval, epic closure, Epic 12 work, commit or push. These restrictions supersede the retrospective skill's normal fresh behavior check, new diff review and final status-update workflow. Consequently this is an evidence synthesis with scoped static inspection, not a new complete code review or a newly executed behavioral qualification. No agents were delegated.

Project instructions consulted: repository README, BMAD retrospective skill and its evidence/document/acceptance references, `_bmad/bmm/config.yaml` and `_bmad/core/config.yaml`. No applicable AGENTS.md was found in the repository or checked D:/ ancestor. Configuration requires Norwegian communication and English documents. The customization resolver encountered a sandbox temporary-file access problem; the documented fallback read the base customization directly. Its hooks/persistent facts/on-complete values are empty; no project retrospective override files were found. No status-detection/update script was used; completeness is read directly from the existing sprint file, not claimed as script-validated.

Evidence inventory (paths below are relative to this document unless stated otherwise):

- [Active epics and declared acceptance criteria](../planning-artifacts/epics.md), story planning copies `story-v1-10.md` through `story-v1-15.md`, [PRD](../planning-artifacts/prds/prd-IBE160-2026-09-21/prd.md), [architecture](../planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), and UX `DESIGN.md` / `EXPERIENCE.md` under `../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/`.
- Promoted specifications `spec-11-1-choose-the-intended-activity.md`, `spec-11-2-understand-the-selected-activity.md`, and canonical `SPEC.md` companions for 11.3/11.4; the promoted 11.5/11.6 specifications contain their contracts and individual review triage. Corrective delivery evidence for 11.3 owner feedback and 11.4 real sources is included. There is no `SPEC.md` in the 11.5/11.6 companion folders: their promoted specifications are the contract entry points, not missing implementations.
- [Development log](../../docs/development-log.md), especially the Epic 11 entries and latest platform correction; [Epic 11 context](epic-11-context.md); [sprint status](sprint-status.yaml); [previous retrospective](epic-10-retro-2026-10-24.md).
- Story reports under `../../docs/evidence/11-*.md`, with direct log checks for 11.5/11.6 below. Historical screenshots and measurement records are delivery evidence; they were not freshly rendered or visually requalified in this session. Raw conversation transcripts were not independently audited. Process findings rely on the development log, review triage and recorded failures, not inferred agent motives.

## Actual Git and local delivery boundary

Read-only checks of status, history, index and local diffs establish:

- HEAD is `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed` (`feat(11.4): maintain planned notices from web or SMS`). The index is empty. No live remote lookup was performed; this draft makes no claim about current remote publication.
- Accepted story commits are `5160fee` (11.1), `b42f1e8` (11.2), `cdcf281` (11.3) and `aa0fcfb` (11.4). Their committed range is `81f1a54..aa0fcfb` (the parent of the first story commit is included as baseline).
- The existing tracked working-tree diff contains 29 files, 374 insertions and 101 deletions. This excludes untracked additions. It spans README/planning/status/log changes, reader API/storage wiring, recovery controllers, test adaptations and the verifier timestamp fixture. Untracked additions include 11.5/11.6 specifications/plans/evidence, `notice_reader_domain.py`, `PrivateNoticeReader.tsx`, `recoverOperation.ts` and new test files.
- Thus a HEAD-only retrospective would omit 11.5/11.6. The working-tree changes are part of the evidence, not disposable noise. The recovery report and initial-tree comparison attribute the new read-only backend projection to 11.5; 11.6 reuses backend contracts and changes frontend recovery without a migration.

The static inspection checked reader route/storage wiring and recovery integration diffs, the shared recovery helper, and test/fixture changes against their documented purposes. It did not establish an exhaustive architecture, duplication or security audit. Existing report claims about healthy services, served assets and database preservation remain historical delivery checks; no fresh service/database inspection was performed here.

## What was delivered and accepted

| Story | Delivered outcome | Current acceptance evidence |
|---|---|---|
| 11.1 | Stable exact-member manual choice, previous/next across passenger/pause/other activities, persisted online choice and independent explicit first shift Start. Planned facts, actual Start, bus and selection remain separate. | Done; Jonas accepted 2026-10-24. [Report](../../docs/evidence/11-1-activity-selection.md); commit `5160fee`. |
| 11.2 | Separate upload, interpretation/editor, day and selected-activity screens; both planned calendar instants, known/unknown facts, retained input and reachable recovery. No invented stops or automatic progression. | Done; Jonas accepted 2026-10-25, reporting that it works well and is much clearer. [Report](../../docs/evidence/11-2-selected-activity.md); commit `b42f1e8`. |
| 11.3 | Explicit exact-activity statuses, correction before closure, confirmed End/Abort, fixed terminal authority/expiry and retained read-only recap. Owner amendment adds activity-level shift controls and bounded A–E import support. | Done; Jonas accepted the amended delivery 2026-10-25. [Initial report](../../docs/evidence/11-3-outcomes-and-close.md), [feedback report](../../docs/evidence/11-3-owner-feedback.md); commit `cdcf281`. |
| 11.4 | Separate manual notice maintenance, revisioned editing, explicit source check/manual ending; corrected title/short/deep text, optional SMS/source URL and explicit selected/all-line scope, with compatible migration. | Done; corrected delivery accepted 2026-10-25. [Report, including real-source correction](../../docs/evidence/11-4-manual-notices.md); commit `aa0fcfb`. |
| 11.5 | Read-only server projection and retained line/Oslo-calendar-date reader: shared notice once, separate incidents retained, exact line identifiers, actual planned interval union/gaps, qualified unknown/partial validity and distinct empty/unavailable states. | Review; manual owner acceptance pending. [Report](../../docs/evidence/11-5-line-date-notices.md), [specification](spec-11-5-read-line-date-notices.md). Local, uncommitted delivery. |
| 11.6 | Status-first original-command recovery, honest unresolved/rejected feedback, current-state reconciliation, retained proposals and explicit comparison across draft/notice/activity/bus/lifecycle/confirmation/deletion controllers. | Review; manual owner acceptance pending. [Report](../../docs/evidence/11-6-server-recovery.md), [specification](spec-11-6-recover-from-an-unavailable-server.md). Local, uncommitted delivery. |

## Verification ledger — historical executions, no new tests

Counts are overlapping suite snapshots, not additive totals. A corrective subset is not a complete rerun.

| Delivery checkpoint | Backend / other checks | Browser evidence and qualification |
|---|---|---|
| 11.1 final | 302 API/PostgreSQL; restart/migration/build; five verifier controls | 257 passed in one final full run. Earlier genuine non-passenger labels and subsequent fixture synchronization were corrected. |
| 11.2 final | 302 API/PostgreSQL; restart/migration/build; five controls | First complete gate 272 passed / 12 failed; corrections and 13 affected passes, then 284 passed in one final full run. |
| 11.3 before owner amendment | 322 API/PostgreSQL; restart/migration/build; six controls | 330/334, followed by four corrected DST-sensitive expiry fixture cases passing; not one green 334-case run. |
| 11.3 accepted owner amendment | 119 affected import tests, reused on unchanged backend hashes; build; six controls | All 351 passed in one final invocation. This is not a claim of a newly repeated complete backend suite after the amendment. |
| 11.4 initial post-review | 393 API/PostgreSQL; restart/migration/build; seven controls | All 395 passed; historical contract before SMS/all-lines correction. |
| 11.4 accepted real-source correction | 61 notice API/PostgreSQL; populated 011→012 upgrade, restart/repeated migration/build; seven controls | All 49 notice browser cases passed. A focused corrected-contract gate, not a new full 395-case gate. |
| 11.5 reviewed local delivery | 411 backend in 478.66s; populated restart, repeated migrations/raw-state/build; seven controls | Full invocation 424/426 in 31.0m, including all 26 reader cases. Shared-helper correction then eight affected cases × three repetitions = 24/24 in 2.5m. |
| 11.6 reviewed local delivery | **411 backend in 488.49s**; populated restart/repeated migrations/raw state/receipt/deadline/session preservation, cleanup/build; seven controls | **Full invocation 453/456 in 34.6m. Three test fixture/synchronization failures, then eight affected cases × three repetitions = 24/24 in 1.6m. No single green 456/456 invocation.** |

Directly checked local stdout: `tmp/11-6-root-full-gate.log:10` (411 backend), `:610–614` (three failures / 453 passes), `tmp/11-6-root-corrective-browser.log:35` (24 passes); `tmp/11-5-root-final-gate.log:9,515–518` and `tmp/11-5-harness-rerun.log:53` corroborate 11.5. These logs are ignored local evidence, not versioned delivery artifacts.

11.6 R1 used a noncanonical 413 detail; R2 forged receipt timestamps contradictory to current data; R3 had failed-lookup/submit-control synchronization problems. Only two test files changed after the broad run; product source stayed unchanged. All scenarios have passing coverage across runs according to the report, but suite-wide green execution on the final test tree is not established. The six proxy variants share R3 synchronization, explaining the eight-case corrective scope. [Failure classification](../../docs/evidence/11-6-server-recovery.md#final-verification-and-failure-classification) explicitly says the old log does not prove R3's exact ordering or automatic product redispatch.

Desktop Edge/Playwright, viewport emulation, keyboard and 200% root-text enlargement are executed evidence. Root-text enlargement is not browser chrome zoom. Physical testing is **not performed**. The planned platform is **Lenovo Pad, Android, Brave, over mobile network to the desktop server at home**. Historical iPad/Safari statements do not define this target. Touch hardware, actual assistive technology and mobile-network behavior remain unqualified.

## Findings, lessons and proposed improvements

All actions below are proposals for later agreement, not changes performed in this review. Resolved delivery defects remain historical findings, not reopened product bugs.

| ID | Documented finding and disposition | Lesson / concrete proposed action and completion evidence |
|---|---|---|
| F1 | **Worked:** explicit manual actions and separate server authorities survived the epic: selection never completes work; closure leaves unknowns unknown; reading/editing notices never checks a source. Sources: 11.1/11.3 reports, 11.5 specification and PRD AC-03/04/08. Preserve as-is. | **A1 — Developer/QA:** carry a cross-story invariant checklist into 12.1/12.4 covering exact member identity, planned/actual times, source checks, terminal writes and original receipt/current-state distinction. Completion: requirement → named test/result → build mapping, including failure paths. |
| F2 | **Worked:** owner feedback made the separate activity screen clearer; retained mounted controllers preserve proposals. **Problems resolved:** held Next replies overriding Back, old-plan expiry affecting another confirmation, and late denial leaving unreachable navigation. Sources: 11.2 report and specification B1/B5/E3; development log 833–873. | **A2 — Developer/QA:** review each async screen transition against user intent, resource generation, session/authority epoch and independent deadlines. Completion: named held-response and independent-expiry cases; retain existing business/security assertions while adapting navigation. |
| F3 | **Problems resolved:** the initial notice form's mandatory URL/tags and distant validation did not fit real SMS, place-based notices, long headings or shared links. The first feedback-only correction was insufficient. Exact rejected owner input was unavailable, so its precise reproduction is not claimed. Source: 11.4 report, real-source correction sections. | **A3 — Jonas/Developer:** validate the next input contract using representative real source shapes before implementation: SMS without URL, shared web link, specific/all-line choice, long multiline text and unknown times. Completion: agreed example-to-field mapping and manual walkthrough; do not convert examples into automatic ingestion scope. |
| F4 | **Problems resolved:** screen helper races recur in 11.2/11.5; timestamp/DST and proxy rejection fixtures can contradict the actual API. 11.6 R1–R3 required test-only corrections. Sources: reports and directly checked logs above. | **A4 — Developer/QA:** make helpers wait for stable observable destinations and settled fault requests; use literal independent expected dates and canonical typed rejection details. Classify failures as product, fixture, environment or orchestration and record the changed files. Completion: corrected assertions plus retained original failures and bounded affected-case rationale. Do not relabel earlier invocations. |
| F5 | **Worked, but cross-story complexity required corrections:** lookup-first retry and current-state reconciliation reuse existing server contracts. Review found missing deletion lookup, comparison regression guards, authorization-gate tests and confirmation generation guards; all are reported resolved. Sources: 11.6 specification B1/B2/B4/B6/B7/E2/V1 and current recovery integration/helper. | **A5 — Developer/QA:** preserve two explicit recovery protocols: server-issued pending operations versus client-issued receipt lookup plus authorized live target. Completion in 12.4 evidence: unavailable/malformed lookup sends no mutation, accepted lookup sends no extra POST, original retry conflicts safely with a newer revision. No general recovery rewrite proposed. |
| F6 | **Worked:** isolated synthetic mutation suites, sequential service handoffs, manifests, raw-state comparisons and restoration preserved ordinary data and historical evidence in delivery reports. **Problems:** broad tests rerender old artifacts; remote-tool stalls can obscure a completed failing gate. Sources: 11.5 final preservation and 11.6 preservation/failure-classification sections. | **A6 — Developer:** retain per-run source/build identity, separate historical/new captures, restoration outcome and durable result summaries. On resume inspect existing process/log state before launching another run. Completion: a reproducible evidence index for 12.5; no private payload or secret publication. Fresh runtime preservation was not rechecked here. |
| F7 | **Open:** desktop evidence does not qualify Lenovo/Android/Brave/mobile use; theme persistence remains planned work. Sources: platform corrections, previous retro E10-A4/A5, PRD NFR-4 and 12.3/12.4. | **A7 — Jonas/QA; Developer for theme:** fill the manual record below; carry actual device findings to 12.3/12.4. Completion: actual versions/orientation/touch/theme/enlargement/recovery observations, plus separate later theme reload/privacy evidence. Owner approval alone is not a device-test result. |
| F8 | **Open documentation/deployment dependency:** the combined guide refers to an existing remote address; README supports loopback-only private development and architecture requires separately verified access/HTTPS for external tablet use. No current remote configuration was inspected. This is an evidence gap, not proof of unsafe exposure. | **A8 — Jonas/Developer:** identify and verify the existing remote access route/origin/HTTPS/session configuration before interpreting a mobile failure as an 11.5/11.6 defect. Completion: configuration/evidence reference and successful authorized access from the intended setup. No deployment changes are authorized by this draft. |

## Previous-retro follow-through

Sprint tracking and the Epic 10 retrospective's owner-acceptance appendix record A1–A3 done: preserved import baseline, bus representability and the passenger-only acknowledgement policy. Their acceptance preceded Epic 11; no status transition is proposed.

Two exact existing selectors remain open:

- `epic-10-retro-item-4-verify-theme-persistence`: no completion evidence established; retain open for 12.3. Current EXPERIENCE explicitly requires a non-private theme preference, and 12.3 owns its verification.
- `epic-10-retro-item-5-record-ipad-verification`: retain open, but reconcile the historical iPad/Safari wording with Jonas's corrected Lenovo/Android/Brave target. No device pass exists. This draft proposes updating the future task's wording when authorized, without rewriting historical evidence or changing tracking now.

## Open dependencies before Epic 12

1. **Manual acceptance of 11.5 and 11.6:** add observations and explicit separate decisions. Receipt of reports is not acceptance. Route any new failures through normal correction/review/appropriate verification before closure; no corrections are authorized in this session.
2. **Mobile access and device qualification:** resolve F8 and record F7. Distinguish reachability/session configuration from reader or recovery behavior. This draft does not start remote deployment work.
3. **12.1 retention integration:** use delivered lifecycle/notices/receipts as inputs for end-to-end expiry, deletion, startup/hourly cleanup and non-resurrection checks. Existing story tests support this work but do not mark the complete later privacy slice passed.
4. **12.2 assessment/demo:** the limited no-login demo is unchanged by 11.5/11.6. A repeatable fictional journey and isolated reset are still planned; private fullstack tests are not evidence that the public demo already covers it.
5. **12.3/12.4:** retain theme persistence and actual device/browser observations; include complete supported import → correction → confirmation → activity/notices → closure → reload and failure journeys with independent expectations. Reader limits remain 200 notices and 400 planned calendar dates; the latter produces unavailable rather than truncated results. Exact line identifiers may leave copied headings unmatched; preserve the visible qualification.
6. **12.5 evidence/submission:** preserve ignored raw logs or extract durable non-private summaries before handoff. Reconcile older planning-copy backlog and append-only pending statements with authoritative current sprint/spec acceptance and actual Git. Record whether any later complete suite is run; this draft neither requires nor authorizes one now. Clean-setup README qualification remains later work.

No new blocking product defect was established by this preparatory scope. This does not certify absence of defects: there was no fresh behavioral run, exhaustive review or physical test. The documented accepted review findings are reported resolved; the open items above are acceptance/qualification/evidence dependencies.

## Reserved for Jonas's manual test results — NOT PERFORMED

**Planned setup:** Lenovo Pad / Android / Brave / mobile network → desktop server at home. Do not prefill expected outcomes as observed results. The [combined walkthrough](../../docs/evidence/11-6-server-recovery.md#manual-test-steps-and-expected-results) supplies detailed steps. A stopped API before saving cannot prove a committed write with lost acknowledgement; record that boundary as not manually tested unless actually controlled. Automated proxy evidence remains separate.

| Test context | Actual value to enter |
|---|---|
| Date/tester | Pending |
| Lenovo model, Android and Brave versions | Pending |
| Desktop build/assets/revision and local-change checkpoint | Pending; delivery reports identify `index-KEcKN3rM.js` / `index-8lnBnkIq.css`, not a new observation here |
| Mobile network and remote route/configuration evidence (no secrets) | Pending |
| Orientation, theme, text setting and touch/keyboard method | Pending |
| Test draft/day (non-private reference), prior saved state | Pending |

| Scenario | Actual result: pass / fail / not run | Observation / evidence / follow-up |
|---|---|---|
| 11.5 shared notice once with all matching lines; separate incident retained | Not run | Pending |
| 11.5 line/date, midnight/gap/non-overlap and unknown/partial validity | Not run | Pending |
| Empty stored / empty filtered / unavailable / unchecked distinctions | Not run | Pending |
| Reader → maintenance → activity, retained text/selection, no incidental write | Not run | Pending |
| 11.6 normal save and authorized online reopen | Not run | Pending |
| Actual outage before acceptance; retained input and unresolved status | Not run | Pending |
| Restore access without refresh; explicit original-operation recovery | Not run | Pending |
| Controlled lost reply after commit; one effect/no extra revision | Not run | Pending; distinguish from merely stopping API before save |
| Two-window newer draft/notice/activity status, explicit comparison/no overwrite | Not run | Pending |
| Notice create/check/manual end → unavailable reader → current refresh | Not run | Pending |
| Leave/reload warning and deliberate page-memory loss; saved online copy only | Not run | Pending; browser warning support may differ |
| Day/Night, portrait/landscape, long text, enlargement, touch/control reachability | Not run | Pending |

Record each failure with steps, expected versus actual behavior, relevant time/build, whether the server accepted the command, and a non-private screenshot/log reference if available. Do not include credentials, raw private plans or secrets.

**Jonas's separate decisions:**

- Story 11.5: **pending** — decision, date and any conditions: ____________________
- Story 11.6: **pending** — decision, date and any conditions: ____________________
- New findings and agreed actions: ____________________
- Final retrospective discussion/decision: **not conducted**.

## Finalization gate and current decision

Acceptance is **pending**, not granted or rejected by this draft. A final machine acceptance verdict is deliberately omitted because the owner requested preparation only; the normal skill's final verdict/status workflow was not run. Current unfinished keys are `11-5-read-line-date-notices` and `11-6-recover-from-an-unavailable-server`, both review. If the normal retrospective verdict were evaluated while either remains unfinished, its completeness rule would force `rejected`; that would indicate incomplete acceptance, not a newly proven product defect.

To finalize later: incorporate actual manual results and explicit owner decisions, resolve/route any failures and the remote/device evidence gap, agree owners/dispositions for A1–A8, reconcile previous follow-ups, and reassess the final accepted build and evidence. Only a later authorized finalization may set a final verdict or update tracking. This document does not approve 11.5/11.6, close Epic 11, mark its retrospective done, authorize publication or start Epic 12.

Owner acceptance update, 26 October 2026: Jonas explicitly accepted corrected story 11.5 (`Godkjent.`). Its account-owned cross-day/expiry delivery is done; existing 11.6 remains review. Earlier pending-acceptance statements describe historical checkpoints. This does not authorize commit/push or further work, finalize the retrospective, close Epic 11, or establish physical-device qualification.
