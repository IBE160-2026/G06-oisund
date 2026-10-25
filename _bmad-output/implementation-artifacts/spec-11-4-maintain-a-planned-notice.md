---
title: '11.4 — Maintain a planned notice'
type: feature
route: dispatch
created: 2026-10-25
approved_on: 2026-10-25
review_loop_iteration: 0
baseline_commit: cdcf2816b86772e559f33ded5807e8cb5a4473bc
story: '11.4'
story_key: 11-4-maintain-a-planned-notice
alias: V1-13
status: done
implementationStarted: true
owner_acceptance: accepted
accepted_on: 2026-10-25
context:
  - D:/IBE160/_bmad-output/specs/spec-11-4-maintain-a-planned-notice/SPEC.md
  - D:/IBE160/_bmad-output/specs/spec-11-4-maintain-a-planned-notice/implementation-plan.md
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-11-context.md
---

# Story 11.4 — implementation specification

Canonical BMAD contract: [SPEC.md](../specs/spec-11-4-maintain-a-planned-notice/SPEC.md).

Read the [implementation plan](../specs/spec-11-4-maintain-a-planned-notice/implementation-plan.md) and the adopted companions listed in SPEC.md. The canonical append-only decision log lives beside the specification.

Owner-directed correction: [real web/SMS sources](spec-11-4-real-notice-sources.md) is the active corrective dispatch for optional URL, short/deep explanations and explicit specific/all-line scope. The frozen block below records the originally approved delivery contract; it is preserved as history and superseded on these points by the owner's explicit 2026-10-25 directions. Read the current canonical specification/plan and latest evidence before implementation or owner testing.

<frozen-after-approval reason="Jonas approved the complete plan and authorized implementation, testing and browser verification on 2026-10-25">

## Intent

Add source-linked manual notice maintenance to the delivered 11.3 day. Implement the approved canonical specification and companion plan as one cohesive feature, with separate management/editor screens and retained data, choices and proposals.

## Boundaries & Constraints

**Always:** Require title, explicit line tags and HTTP(S) original source. Retain nullable source-update and partial/unknown validity; use Oslo server resolution. Keep registration/edit timestamps separate from explicit source checking. Only `Kontrollerte kilden nå` records server checked-at for saved revision; later edits qualify the prior check. Initial status is Registrert; only deliberate confirmed ending gives Avsluttet manuelt. Preserve separate screens, selected activity, bus, Aktivitetsstatus, unsaved drafts/time/input and reachable pending recovery. Before Start/active maintenance is allowed; terminal workdays are read-only. Reuse server ownership, workday locks, expected revisions, stable bounded receipts, effective parent expiry and private wrappers. Add migration 011, cascade/cleanup and atomic closure receipt shortening, preserving all existing records/receipts.

**Never:** No 11.5 line/date relevance filtering, 11.6 recovery redesign, source fetch, inferred resolution/check/coverage, automatic progression, private persistent cache, parser/demo expansion, notice delete/reopen, commit, push or next story. Do not test ordinary owner records, delete volumes or change secrets. Preserve frozen intent and historical evidence.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected behavior | Failure handling |
|---|---|---|---|
| Create/edit/reopen | Explicit valid metadata; optional null/partial times | One stable notice, exact saved fields/tags, no incidental selection/Start/status change | Invalid fields/schemes/bounds reject without mutation |
| Check versus edit | Saved current record or later edited record | Explicit server check only; later edit qualifies earlier check | Dirty/stale/pending check cannot silently verify |
| Manual ending | Confirm or cancel | Confirm ends only notice; cancel sends no mutation; no clock ending | Repeated/racing commands remain revision-safe |
| Navigate | Day/list/editor/day/activity, other dirty resources | One primary screen, retained proposals/selection, meaningful focus, reachable recovery | Avoidable loss guarded; unresolved command never discarded as failed |
| Lost/stale response | Timeout, HTML, malformed, lost accepted reply, competing edit | Preserve original proposal/command; authorized lookup/same-body retry, explicit comparison | No duplicate, false saved or force overwrite |
| Terminal/access/expiry | Closure, delete, identity/session change or expiry race | Current authority wins; read-only terminal, no resurrection or deadline extension | Fresh writes denied atomically; stale replies cannot restore presentation |
| Persistence/privacy/render | Real synthetic PostgreSQL/API/restart and Day/Night browser | Preserved facts/receipts/deadlines, isolation, readable enlarged controls | Record actual failures and device limits honestly |

</frozen-after-approval>

## Code Map

- `backend/app/workday_storage.py`: owned parent lock, require_mutable and effective deadline; reuse unchanged authority.
- `workday_outcome_storage.py`: closure explicitly shortens receipt tables; include notice receipts. `private_storage.py` owns cleanup.
- `backend/app/private_main.py`, `backend/migrations/private/011_manual_notices.sql`: routes/new schema; focused notice domain/storage follow existing command conventions.
- `frontend/src/PrivateConfirmation.tsx`: lockRef/guardChild; add notice guard without locking away recovery. `PrivateWorkdayView.tsx`: retain mounted controllers, separate notice screens. `PrivateWorkdayProgress.tsx`: closure/navigation integration.
- `PrivateTimeInput.tsx`: Start/Slutt label union needs safe generalization for optional notice times. `useWorkdayResource.ts` and private wrappers provide binding/recovery conventions.
- `backend/tests/test_private_outcomes.py`, `frontend/tests/private-outcomes.spec.ts` and helpers: reuse synthetic setup; new focused notice suites. `scripts/verify-private-drafts.py`: sequential disposable gate/restoration, extend raw state/deadline/receipt proof.

## Tasks & Acceptance

- [x] Notice schema/domain/storage/routes and closure/cleanup integration per companion.
- [x] Mounted notice controller, separate management/editor/detail, dates and aggregate guards per companion.
- [x] Meaningful API/PostgreSQL, concurrency/recovery/privacy/retention and browser tests covering every matrix row.
- [x] Extend sequential verifier/restart/migration preservation and controls; production build and required broad regression gate.
- [x] Browser renders/flow inspection, independently reviewed fixes, README/evidence/log/spec/sprint handoff.

Given a confirmed day, when the owner saves/edits/checks/ends a notice explicitly, then exact metadata and separate source-check/status semantics survive authorized reload. Given navigation or failed writes, when returning or reconciling, then existing data/selection/proposals survive and only acknowledged effects appear saved. Given terminal/expiry/identity races, when any command/read/retry executes, then current access and retention win. Given enlarged Day/Night screens, when using keyboard and long content, then controls/focus/text remain reachable at IR-01 floors.

## Implementation Notes

The approved planning files are the only pre-existing dirty tree; the current explicit implementation instruction authorizes building on them. No new intent gaps; additive schema and ordinary local rollout require preservation checks. Footprint spans new backend/DB/frontend/tests and existing parent guards/verifier. Retain approved companion detail; no rescoping checkpoint is needed. Worker performs sequential focused implementation/tests and restores ordinary services on existing image; root owns final independent review/broad gate/preservation/rollout. No staging despite generic workflow staging direction: user requires stop before publication and complete diff can include untracked files without touching index.

## Spec Change Log

## Review Triage Log

Root classified each finding before grouping, after all three independent layers returned. All retained changes are direct corrections to demonstrated states or test-only coverage; they add no endpoint or product goal and do not change frozen intent. No finding is deferred.

| ID / layer | Verdict | Evidence and route |
|---|---|---|
| B1 blind: saved title absent in comparison | medium | NoticeFacts renders metadata but no title; the comparison heading is generic while the competing title can differ. Patch: display the actual saved title before deliberate overwrite. |
| B2 blind: lifecycle review without lifecycle facts | medium | The current lifecycle is loaded but only terminal status is shown. A create conflict after Start offers review without showing active state/start. Patch: present current saved state and relevant times. |
| B3 blind: comma tag roundtrip | medium | API plain tags permit commas; join(', ') then split(',') changes an accepted single identifier on edit. Patch: preserve exact individual identifiers while retaining ordinary comma-separated entry; verify quoted delimiters/quotes. |
| B4 blind: incompatible URL validators | medium | urlsplit accepts `%` and invalid dotted numeric hosts while browser URL rejects them. Such API-accepted rows poison the whole current list. Patch: use browser-compatible HTTP(S) validation without fetching sources or rewriting original strings. |
| B5 blind: stale load catch/finally | medium | current() rejects an old generation, but load catch/finally still changes availability/busy after a newer successful load. Patch: bind all load completion effects to its originating generation. |
| B6 blind: reversed validity feedback | medium | Both clocks can resolve but save() has no ordered-interval check; the server rejects correctly and the UI offers unrelated comparison guidance. Patch: explicit relation feedback and no send until corrected, preserving input. |
| B7 blind: capacity guidance lost | low | The known 429 branch discards the existing bounded backend message and suggests refresh/comparison, which cannot free capacity. Patch is direct copy correction within the existing known-rejection state; no new state or flow. |
| B8 blind: permissive timestamps | medium | stamp() accepts timezone-free and normalized invalid-calendar Date.parse inputs, so malformed current reads may establish trusted facts. Patch: strict calendar/explicit-zone timestamp validation plus malformed-read/ack coverage. |
| B9 blind: browser pagination coverage | medium | The backend follows four pages, but browser scenarios only create one row and do not verify current() aggregation. Patch: at least 51 distinguishable rows, second-page maintenance and later-page failure/recovery. |
| B10 blind: lost check/end browser replies | medium | The controller has separate acknowledgement branches but transport-loss tests exercise create only. Patch: both lookup and same-body retry for accepted check/end, one revision/effect and reachable recovery across navigation. |
| E1 edge: denied follow-up after known rejection | high | The nested current() catch at the known-rejection branch only clears available; it omits denied/shortening/parent refresh. A subsequent list view can retain facts after 404/410. Patch: apply the existing denial/expiry treatment consistently and reproduce the rejection→deletion/expiry read. |
| E2 edge: superseded reads | medium | Independently confirms B5's missing generation checks in load completion. Same patch group; preserve this separate finding record. |
| E3 edge: invalid numeric host | medium | Independently confirms B4 with `https://999.999.999.999`, another accepted-server/rejected-browser hostname. Same patch group and explicit test vector. |
| V1 verification: management pagination | medium | Pre-verified regression gap: first-page-only controller mutation would evade current browser tests, while the backend's independent pagination test still passes. Test-only patch group with B9. |
| R1 root: historical Oslo roundtrip | medium | Existing server test accepts 1894-01-01T12:00+00:43 (UTC11:17); local Intl formats it as12:17+01:00. Current editor reconstruction creates an offset the server rejects on title-only edit. Patch: retain authoritative server Oslo source instants through display/edit, including old accepted receipt semantics; add a literal historical regression alongside autumn-fold coverage. |

Patch groups: B1; B2; B3; B4/E3; B5/E2; B6; B7; B8; B9/V1; B10; E1; R1. The three independent layers completed at the original full-green checkpoint: 384 API tests/495.67s, 377 browser tests/29.9m, restart/repeated migration/raw-state preservation, build and seven verifier controls/0.177s. These results precede the patches; subsequent verification must identify its actual scope.

### Patch reinspection — 2026-10-25

The same blind reviewer independently re-inspected B1–B10 and confirmed each resolved. The same edge reviewer confirmed E1–E3 resolved, including the nested denial helper and generation guards. The verification reviewer confirmed B9/V1 now exercises 51 distinguishable browser records, later-page failure/recovery, second-page editing and independent revision checks. No concrete introduced issue remains. Root separately inspected the server-authoritative historical source representation, strict timestamp/calendar checks and unchanged older UTC receipt semantics (R1); its pre-fix browser regression failed at 12:17 versus expected 12:00 before the fix passed.

Focused patch evidence: 53 API tests passed in 79.02s; all 44 notice browser cases have passing coverage (43 passes in 3.8m, plus the exact visible-comparison locator correction passing in 9.0s). No product code changed for that locator correction. Build passes. The final complete root gate is required after these patches; the earlier 384/377 results are historical until the new gate is recorded. No finding is deferred and the frozen intent is unchanged.

## Verification

Focused synthetic notice API/PostgreSQL/browser checks first. `uv run --no-project scripts/verify-private-drafts.py` with COMPOSE_PROJECT_NAME=ibe160-private-tests runs the complete sequential disposable gate; `uv run --no-project scripts/test_verify_private_drafts.py` validates controls; `npm.cmd run build` in frontend. Preserve ordinary state with read-only fingerprints before/after; never target ordinary data. Inspect separately named 11.4 Day/Night renders; distinguish emulation from actual hardware. Stop in-review for owner testing before commit/push/next story.

## Final verified delivery — 2026-10-25

Final complete post-patch gate passed **393 API/PostgreSQL tests in 458.81s** and **all 395 browser tests in one 27.9m invocation**, including all 53 notice API cases and 44 notice browser cases. Real populated PostgreSQL/API restart, repeated migrations, exact raw-state/receipt/deadline preservation, fictional denial and production build passed. Seven independent stubbed verifier/restoration controls passed in 0.191s. All 101 application/test/migration/verifier source paths and SHA256 hashes remained unchanged through this gate. A PowerShell wrapper initially treated the JSON manifest as one nested array and falsely reported a mismatch; an independent Python comparison checked every path/hash and proved no source drift.

All three review layers completed and independently re-inspected their retained fixes; root verified R1's literal historical regression and unchanged raw older UTC receipt semantics. No finding is deferred. Root inspected final narrow/wide editor/saved/conflict/unavailable renders; 24 measured states / 414 controls pass the applicable floors: informative text minimum 6.126:1, boundaries 4.391:1, focus 11.450:1 / 3px, controls ≥58px, no horizontal overflow and unobscured focus. Actual hardware/assistive-tech/browser chrome zoom remain not run under existing 12.3/12.4 obligations.

Ordinary local rollout is verified. Migration 011 adds only its migration marker and two empty tables; every original business/account/session/security/migration row, secret and database container identity is preserved. The three expired login-throttle rows removed by unchanged startup cleanup at the initial worker restoration are the only original-baseline maintenance difference; subsequent comparisons equal that post-worker baseline except the planned additive schema. Ordinary services are healthy and synthetic services stopped. Private HTML and both served JS/CSS assets exactly match the tested dist build (`index-CrxO5lQG.js`, `index-BElU2L01.css`). Restored all 99 historical evidence files changed by the gate byte-for-byte; separately named 11.4 evidence remains.

The approved stop-in-review contract overrides generic Build step 5's done/commit/PR directions: both specifications and sprint remain review/in-review for owner testing, no staging/commit/push, no next story. The [delivery evidence and owner walkthrough](../../docs/evidence/11-4-manual-notices.md) record exact results and intermediate failures. Owner acceptance is pending; the implementation tasks are complete.

## Owner acceptance and publication authorization — 2026-10-25

Jonas explicitly approved the corrected story 11.4 delivery, then instructed commit and push. Owner acceptance is accepted and story/sprint status is done. The technical final gate remains 61 API/PostgreSQL and 49 browser passes with verified migration/restart/data preservation. Earlier pending-acceptance and stop-before-publication statements are historical and superseded by these owner messages. Record the accepted work in Git and push to origin/main; do not start 11.5 or any other story.
