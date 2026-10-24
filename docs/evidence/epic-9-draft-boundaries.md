# E9-A2–E9-A5 — Draft boundary follow-up

## Current technical status

**Technically complete and accepted with the combined E9/10.4 delivery, 2026-10-24.** Jonas reports, "Test viser at det fungerer som ønsket." E9-A2–A5 are closed following recorded technical evidence and delivery acceptance; no manual expiry/admission/201-record test is inferred. Final root sequential verification on the reviewed/patched E9 tree exited 0: **219 backend/API tests (240.25s)** and **129 browser tests (7.7m)** passed, as did restart/migration equality and production build. Three fully mocked restoration/control tests passed separately. Local log: `tmp/e9-review-final.log`. Subsequent combined verification passed 236 backend/API and 157 browser tests. Earlier pending/running/failed entries below are historical.

Local operational API was upgraded to the tested code after review. Test/operational API filesystem layers match; the original database container was retained, and every existing table/secret digest matches the pre-test baseline. Disposable services are stopped. No ordinary-account test, reset, commit/push or owner-acceptance record occurred. E9-A5 continues as a process requirement through 10.4; A2/A3/A4 technical evidence is complete. The historical retro verdict remains unchanged.

## Authorization and baseline

On 2026-10-23 Jonas authorized E9-A2–E9-A5 remediation before 10.4. Initial HEAD: `6d07f74c4e4d2b172ef2e248ae8b3d54d1e64d77`. Existing local changes were only the 10.4 draft specification and log. Main matched recorded origin/main; no remote operation occurred.

The historical [Epic 9 retrospective](../../_bmad-output/implementation-artifacts/epic-9-retro-2026-10-21.md) and its rejected verdict remain historical evidence. E9-A1 was already owner-accepted. This follow-up does not record new human acceptance.

## Selected contracts

- E9-A2: check original creation-operation expiry during atomic acceptance, before replacing its deadline; roll back candidate draft and acknowledgement on failure.
- E9-A3: bounded cursor pagination exposes all live accepted drafts, including existing records beyond 200, without a new live-draft cap.
- E9-A4: verify draft-operation admission at 200 live unused operations, 429 without mutation, and exclusion of accepted/expired operations.
- E9-A5: sequential shared-service verification, cross-window identity/transaction inspection, and follow-up/story identifiers in later authorized commits; cross-story portion also applies to 10.4.

## Execution record

Implementation and verification are in progress. This document is not a completed test pass or owner acceptance.

Initial focused evidence: both deterministic E9-A2 cases failed against unchanged production with `DID NOT RAISE HTTPException` (2 failed, 52 deselected, 4.11s). After conditional insert/acceptance predicates, the four new backend cases passed (48.16s): expiry at insert/acceptance with rollback and accepted retry, 200/201 real HTTP creation/discovery/reopen, and pending-operation admission with exact no-mutation comparison. Commands/results retained locally in ignored `tmp/e9-draft-boundaries-focused.txt`.

First broad backend run: **217 passed in 247.33s**. Sequential restart/migration/session/snapshot/decision/operation/deletion/list/deadline equality passed; TypeScript/Vite production build passed. Browser and independent review remain pending at this point. Full local execution log: ignored `_bmad-output/implementation-artifacts/e9-draft-boundaries-verification.log`. Both fully mocked verifier restoration tests passed (0.123s).

The first browser run exposed existing test-fixture assumptions that the first same-date draft was always the newest. UUID pagination changes that incidental order. Each case already creates its own work; cleanup was tightened to only its random synthetic account's drafts/operations/deletion receipts before each case. This is a harness correction, not a product expectation change. The actual 201-item pagination test, including delayed-page suppression after refresh/deletion, passed. A clean broad browser rerun is required; intermediate failures are not represented as a complete pass. Root inspected the [actual 768px pagination render](e9-pagination-768.png).

Read-only operational baseline captured per-table counts/digests and secret-file digest, without emitting row contents or credentials. Tests use `ibe160-private-tests`; operational database/container/volume/secret are retained.

## Owner checks after technical completion

1. Open and resave a disposable manual draft. Reload/reopen; confirm facts and deadline survive apart from the intended correction/revision.
2. Check draft listing and the additional-page control using synthetic evidence; manually creating 201 ordinary drafts is unnecessary.
3. Confirm ordinary access still works. Automated isolated evidence covers expiry/admission races without changing your account or clock.

Final tests, review dispositions and runtime availability will be recorded before handoff. Owner acceptance remains pending.

## Clean implementation verification

The complete sequential rerun exited **0**: **217 backend/API tests passed (230.15s)**, exact PostgreSQL/API restart and repeated-migration equality passed, production build passed, and **all 124 browser tests passed in one run (7.3m)**. Local log: `tmp/e9-draft-boundaries-final.log`. This supersedes the initial browser failures for the corrected fixtures. No product code changed between the backend pass and browser pass. Independent review and local operational API upgrade remain the next technical steps; no human acceptance is inferred.

## Independent review and final root verification

All three BMAD review layers completed. Nine blind-review findings were individually triaged: six retained corrections, two low-impact proposals rejected with reasons, and one chronological-status claim refuted. Edge and verification reviewers filed no additional findings. The six corrections cover final-page focus, update expiry evidence, foreign/expired pagination boundaries, cursor-page identity switching, malformed later-page recovery and verifier cursor-progress/restoration. Root additionally corrected initial count wording and Day focus outline within the focus patch. Exact dispositions are in the specification's Review Triage Log.

Focused patch checks passed five backend cases, seven browser cases, two final keyboard/status cases and three fully mocked verifier controls. Blind reviewer re-inspected all six retained groups and confirmed resolution with no concrete remaining defect. Root read the patches and started complete sequential final verification on the patched tree. Its backend phase passed **219 tests (240.25s)**; restart/migration equality and production build passed. Browser phase and compatible local API rollout are still pending at this chronological entry. Local log: `tmp/e9-review-final.log`.

## Cross-story completion — 2026-10-24

The subsequent reviewed 10.4 combined run also passed all E9 regressions: **236 backend/API tests, restart/migration equality, build and all 157 browser tests**, plus five mocked verifier controls. E9-A5 was applied through 10.4: shared-service restart/browser phases ran sequentially; identity binding and atomic bus/session/plan/deletion boundaries were inspected and exercised, including both PostgreSQL contention orderings and silent two-window account switches. No new commits exist; future publication must retain relevant E9/story identifiers. Final tested local API layers match, original database container and every existing table/secret digest match baseline, ordinary services are healthy and disposable services stopped. E9-A2/A3/A4 technical status remains complete; E9-A5 technical follow-through is complete for this delivery. Human acceptance/action closure and the historical retrospective verdict remain separate and unchanged.
