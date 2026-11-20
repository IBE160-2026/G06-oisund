---
title: 'Make qualified automatic notices available to private workdays'
type: 'feature'
created: '2026-11-20'
status: 'in-review'
route: 'dispatch'
baseline_commit: '755b6f9c43c13bcad1eef5555d9672c8f9f50456'
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md', '{project-root}/CLAUDE.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

Collect Entur TRO SIRI-SX and let the driver inspect why an observation may be relevant to a confirmed workday. Keep manual notices independent.

## Boundaries & Constraints

Use the bounded AN-E1 scope in `D:/IBE160-plan-automatic-notices` at `da867072a8a17249032c00efa51bd61979d41428`. Load the SPEC, source lifecycle, relevance rules, provisional product decisions and epics before coding. Use existing FastAPI/PostgreSQL/React. Only V2's owner sandbox explicitly enables periodic provider access. Public calls carry fixed provider/dataset/continuity parameters, never private content or positions. Preserve source attribution and manual records. No edits to production configuration. Work only in this V2 worktree and do not stage or commit.

| Scenario | Expected behavior |
| --- | --- |
| Complete | Every page is validated with continuity and terminal MoreData=false. Exact dated line and half-open time overlap yield possible relevance. |
| Partial or unavailable | Repeated/stalled/invalid/mixed pages or timeout retain the last complete baseline and show partial/unknown or unavailable. Missing or old never implies absence or closure. |
| Review | Unresolved, stop-only and broad messages remain reachable with reasons. Explicit reversible association, day context and dismissal are private decisions, separate from source and manual records. |
| Mutation | Owner, CSRF, expected revision, exact replay, parent lifecycle and expiry checks protect writes. Other accounts and expired or terminal workdays cannot mutate. |

</frozen-after-approval>

## Code Map

- `backend/app/private_main.py` owns auth, Origin/CSRF and no-store plus app lifespan. Add a narrow automatic-notices router and separate task. Keep manual routes and `notice_reader_domain.py` intact.
- `backend/app/workday_storage.py`, `draft_storage.py`, and `workday_notice_storage.py` show authorization, parent lock/recheck, revisions and operation receipts. Do external I/O outside private locks.
- `frontend/src/PrivateWorkdayView.tsx` and its private request helpers provide the separate day view. Preserve the selected activity and manual controls.
- Public live qualification used a fresh requestor ID and maxSize=5. Pages returned 5 then 4, exact union equalled a maxSize=1000 control, with no repeated identities and MoreData true/false. Use literal MoreData, explicit UUID echo and a shared maximum of four GETs/minute. Bind public `TRO:Line:1_20` / `1_24` to `TRO:Authority:1` on the checked dates 2026-11-23 and 24 only. Source identity uses participant and situation; version is independent.

## Tasks & Acceptance

- [x] Add migration `016_automatic_notices.sql` with separate public source state and private review records/receipts, keyed to the owning workday and constrained by its fixed expiry.
- [x] Add bounded, atomic, coordinated ingestion with documented XML limits, explicit timestamps and stable lifecycle state. Keep refresh opt-in.
- [x] Implement the authenticated projection and review through normal workday entry points.
- [ ] Conduct personal trial on a representative workday and record the real overlap, handoffs and usability.

## Implementation Notes

Coordinate edits to `PrivateWorkdayView.tsx` and `private_main.py` with the parent before writing. Use only the V2 fixture guard for tests. Keep original planning defaults unless already superseded in `v2-reconciliation.md`.

## Spec Change Log

- Migration 020 separates current identity membership from exact revision evidence. The live parser accepts Entur's direct `ServiceDelivery` envelope with exact response ID and explicit page continuation.

## Review Triage Log

- Patched silent basis changes, late replies across navigation, fabricated revision stamps and Unicode identifier shape. Added real PostgreSQL request spacing and migration checks. Existing manual registry remains reachable while a review is open or an activity changes.

## Verification

Run unit/relevance tests using independently labelled examples and real API/DB tests in the isolated V2 environment. Record any provider/owner-dependent acceptance separately.
