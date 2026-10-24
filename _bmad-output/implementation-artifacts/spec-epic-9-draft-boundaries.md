---
title: 'E9-A2–E9-A5 — Harden draft acceptance and discovery'
type: bugfix
created: 2026-10-23
status: done
owner_acceptance: accepted
accepted_on: 2026-10-24
route: dispatch
baseline_commit: 6d07f74c4e4d2b172ef2e248ae8b3d54d1e64d77
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-9-context.md
---

<frozen-after-approval reason="owner authorized preparation, implementation and routine decisions on 2026-10-23">

## Intent

**Problem:** Draft creation can accept an operation that expired after initial validation; listing silently hides accepted live drafts beyond 200. Pending-operation admission lacks direct boundary evidence.

**Approach:** Make original operation validity part of atomic acceptance, paginate draft discovery, and establish deterministic draft-specific regression evidence. Complete this follow-up technically before story 10.4.

## Boundaries & Constraints

**Always:** Preserve E9-A1 identity protection, session/owner locking, CSRF/origin, no-store, fixed retention, normalized replay and existing private records. Original operation expiry must be checked before its deadline is replaced; failure rolls back both candidate draft and acknowledgement. Verify unused operation expiry before insertion and after candidate insertion. Retrying accepted operations returns the original accepted result without extending retention. Changed payload conflicts. Updates remain revision-bound.

Every accepted live draft must remain discoverable. Use bounded UUID-cursor pagination, matching the existing confirmed-plan pattern, rather than rejecting new drafts at 200. Existing records beyond that boundary must also remain reachable. Invalid cursors fail validation. The frontend accumulates pages without duplicates, rejects malformed replies and invalidates stale page responses after refresh/deletion/identity changes.

200 live unused draft operations reject the next issuance with 429 and no mutation. Accepted/expired operations are excluded. All tests are isolated and synthetic. Shared-service restart/browser verification runs sequentially. Preserve historical retrospective verdict; distinguish technical completion from human acceptance. Use E9/story identifiers in any future commit subjects.

**Never:** Alter ordinary accounts/data/secrets, reset private storage, close E9-A1 again, infer owner acceptance, implement 10.4 before these checks pass, or start 10.5. No commit/push before owner acceptance.

## I/O & Edge-Case Matrix

| Scenario | Input/state | Expected | Failure |
|---|---|---|---|
| Atomic expiry | Operation expires after initial check | 410, no draft/result/hash committed | Roll back candidate insert |
| Retry | Same accepted payload | Same accepted snapshot/deadline | Changed payload 409 |
| Discovery | 200 then 201 live owned drafts | All reachable over bounded pages | No silent truncation |
| Admission | 200 live unused operations | Next 429, rows unchanged | Accepted/expired excluded |
| Identity/race | Two windows or stale page | Correct owner/current generation only | Preserve E9-A1 clearing |

</frozen-after-approval>

## Code Map

- `backend/app/draft_storage.py`: `save` currently replaces operation expiry unconditionally; `listing` uses LIMIT 200; `issue` already checks pending admission. Reuse owner locks and fingerprint normalization.
- `backend/app/draft_domain.py`, `private_main.py`: strict list/route contracts.
- `frontend/src/PrivateDrafts.tsx`: `refresh`, list sequence/deletion epoch and strict summary validator; reuse workday pagination pattern without changing draft editing semantics.
- `backend/tests/test_private_drafts.py`: real HTTP/PostgreSQL fixtures. `test_private_workdays.py` demonstrates wrapped-connection expiry injection; plan tests are not draft evidence.

## Tasks & Acceptance

- [x] `backend/tests/test_private_drafts.py`: add deterministic expiry test first; run against unchanged production code and record failure, then assert rollback and accepted retry. Add 200/201 discovery and pending-200 admission/no-mutation/exclusion tests.
- [x] `backend/app/draft_storage.py`: conditional live-operation acceptance with rollback; bounded cursor listing with next cursor.
- [x] `backend/app/draft_domain.py`, `private_main.py`, `frontend/src/PrivateDrafts.tsx`: matching bounded list API/UI and recoverable page validation, refresh/deletion invalidation.
- [x] `frontend/tests/private-drafts.spec.ts`, affected regression expectations: prove later-page reopen and preserve input/identity protections.
- [x] `scripts/verify-private-drafts.py`: preserve sequential restart/build/browser verification; update response expectations as necessary. Run restoration-control tests.
- [x] `Docs/evidence/epic-9-draft-boundaries.md`, `Docs/development-log.md`, `README.md`, retrospective and sprint actions: executed proof, triage and pending owner acceptance; retain historical verdict.

**Acceptance Criteria:**
- Given an initially live creation operation, when it expires at acceptance, then no draft or successful receipt commits.
- Given 201 live drafts, when pages are followed and the last draft reopened, then all accepted identities remain reachable.
- Given 200 pending operations plus accepted/expired ones, when another is requested, then 429 leaves state unchanged.
- Given existing identity/regression flows, when the sequential verifier runs, then tests and restart equality pass with operational availability restored.

## Implementation Notes

- Owner acceptance of the combined E9/10.4 delivery, 2026-10-24: Jonas reports, "Test viser at det fungerer som ønsket." Close E9-A2–A5 after the recorded technical verification and this delivery acceptance. Deterministic expiry, 201-draft and admission evidence remains automated; no manual boundary test is claimed. Historical retro verdict unchanged. E9-A5's identifier rule still applies to later authorized commits; none is created here.

- 2026-10-24 final technical handoff: root sequential verifier passed 219 backend/API tests (240.25s), exact restart/migration/list/plan/receipt/deadline equality, production build and all 129 browser tests (7.7m), exit 0. Three mocked verifier controls passed separately. All six retained review groups re-inspected as resolved; no retained finding deferred. Historical tracked PNG churn restored and final 768px keyboard-focus render inspected/preserved. Local operational API upgraded to tested layers; same database container and all existing data/secret hashes preserved. Spec done denotes technical implementation only; human acceptance remains pending and sprint actions stay in-progress for that distinction. E9-A5 carries into 10.4. No commit/push or 10.5.

- 2026-10-23: Owner explicitly authorized both sequential parts, necessary specifications and routine choices without another start checkpoint. Existing 10.4 spec/log changes inspected and retained. This follow-up is first; 10.4 stays unstarted until its technical gate passes. Implementer may arrange isolated services and verification under the existing synthetic-only guards, restoring operational API afterward. Report evidence and changed paths; do not commit, publish, or record owner acceptance.
- 2026-10-24: All three independent BMAD review layers completed. Six retained blind-review groups corrected; two low-impact proposals rejected and one chronological-status claim refuted, with individual evidence below. Root additionally corrected initial unavailable-count wording and Day focus styling in the same focus/status patch. Focused checks passed: five backend cases, seven browser cases, two final keyboard/status cases and three mocked verifier controls; build/diff check passed. Blind reviewer re-inspected all six groups and confirmed resolution without a remaining concrete defect. Root final complete sequential verification is running; no 10.4 implementation or owner acceptance yet.

## Spec Change Log

## Review Triage Log

| Finding | Verdict / route | Evidence |
|---|---|---|
| Blind 1: owner/id index | low / reject | Existing owner index bounds each owner's rows; no measured regression at 201 or expected seven-day use. Another migration/query-plan work adds complexity for unusual scale. |
| Blind 2: expanded-list navigation | low / reject | Original UI already rendered up to 200 entries above the editor. Pagination improves initial size; a new scrolling/collapse/navigation system is disproportionate for rare 201-item use. |
| Blind 3: final pagination button loses focus | medium / patch | The focused button is removed on the final page and no successor receives focus. Add persistent live count/status after the list, transfer final-page keyboard focus there and assert it. |
| Blind 4: update expiry boundary untested | medium / patch | The update predicate also changed; existing update tests do not expire the operation between checks and final acceptance. Extend deterministic rollback/retry coverage to updates. |
| Blind 5: multi-page owner/expiry filtering untested | medium / patch | New traversal uses one owner; the foreign check is empty. Add interleaved foreign/expired rows and prove exclusions across boundaries. |
| Blind 6: delayed query-page account-switch coverage | medium / patch | Existing identity intercepts cover the base list but not cursor traffic. Exercise delayed pagination across silent shared-cookie identity change through the existing guards. |
| Blind 7: malformed later pages untested | medium / patch | Current malformed tests return an empty first page. Cover duplicate/order/before-cursor/inconsistent continuation later replies, preserving prior rows/cursor/input and successful retry. |
| Blind 8: verifier can loop on cursor regression | medium / patch | listed_drafts has no visited-cursor guard; a responding API can prevent verifier restoration indefinitely. Assert advancing, unrepeated cursors before continuing. |
| Blind 9: mixed current/historical status | false / reject | Execution entries are chronological; final clean-run entry supersedes running/failed intermediate observations. Independent review and runtime upgrade remain genuinely pending despite test success. Final handoff will state current status explicitly. |
| Edge review | no findings | Reviewer returned an empty findings array after tracing the complete diff and claims. |
| Verification review | no findings | Reviewer completed the lens after sandbox-read escalation; no verified gaps filed. Blind review's additional concrete coverage improvements are retained above. |
| Root: initial count after failed load | medium / patch | The new persistent count initially says zero loaded even if no list was acknowledged. Preserve the paragraph but distinguish loading/unavailable from a successful count; extend the existing honest-empty regression. |
| Root: Day focus indicator on count paragraph | medium / patch | Day outline selectors cover buttons/headings/controls, not the new paragraph. Include its class in the existing 3px focus rule and assert keyboard activation/focus/outline. Same final-page focus correction. |

## Design Notes

No intent gaps. Pagination is the smallest option that also preserves discovery of existing records beyond 200; it avoids a new user capacity restriction. Existing authorized local changes are yesterday's spec/log and must be preserved.

## Verification

Use `COMPOSE_PROJECT_NAME=ibe160-private-tests` and `uv run --no-project scripts/verify-private-drafts.py`. First retain failing deterministic E9-A2 evidence on original code. Then run new focused tests, complete regressions/restart/build/browser sequentially, restoration unit tests and `git diff --check`. Complete independent BMAD review layers and fix/retest findings before moving to 10.4. No ordinary-account tests or private payload output.

Executed 2026-10-23:
- Original production code, deterministic expiry at candidate INSERT and acceptance UPDATE: **2 failed**, 52 deselected, 4.11s; both failed because no HTTPException was raised.
- Conditional live-operation predicates plus draft discovery/admission tests: **4 passed**, 52 deselected, 48.16s. Both expiry cases prove transaction rollback and accepted retry equality; discovery covers 200/201 accepted drafts; admission proves 429 without mutation with accepted/expired exclusions.
- Full sequential verifier backend matrix: **217 passed**, 247.33s. Restart, migration replay, session preservation, draft/plan/decision/receipt/deadline and draft-list equality passed. TypeScript/Vite production build passed. Browser verification is running; no owner acceptance is implied.
- Restoration-control tests: **2 passed**, 0.123s, all subprocesses stubbed. `git diff --check` has no whitespace errors.
- Retained focused execution record: `tmp/e9-draft-boundaries-focused.txt`; complete verifier output: `_bmad-output/implementation-artifacts/e9-draft-boundaries-verification.log` (both ignored local evidence).
- Initial browser matrix: **118 passed, 6 failed**, 8.8m. All six failures came from previously shared per-suite fixtures opening the first same-date draft and assuming newest-first ordering. The required UUID ordering exposed those assumptions. Draft and import browser fixtures now clear only their own synthetic owner's draft state before each case; every case seeds/saves its own work. This failed full run is retained at `tmp/e9-draft-boundaries-initial.log`; it is not counted as a successful sequential run. A clean full verifier rerun is in progress at `tmp/e9-draft-boundaries-final.log`.
- Clean sequential verifier rerun completed successfully (exit 0): **217 backend tests passed**, 230.15s; PostgreSQL/API restart, migration replay, preservation/equality checks and production build passed; **124 browser tests passed**, 7.3m. Final complete output is retained at `tmp/e9-draft-boundaries-final.log`. New browser proof covers 201-row accumulation/final reopen, malformed pagination recovery and suppression of delayed later pages after refresh/deletion; existing identity regressions passed.
- Final restoration controls: **2 passed**, 0.140s. Operational API and existing DB are healthy on their original loopback service; disposable services are stopped. Historical tracked screenshots regenerated by tests were restored; the new pagination evidence image is preserved. Final `git diff --check` passes.
- Root retains responsibility for independent review layers, documentation finalization and matching the operational API image to the tested frontend contract after review. No ordinary-account requests/tests, storage reset, commit/push or owner-acceptance record was made by the implementer.
