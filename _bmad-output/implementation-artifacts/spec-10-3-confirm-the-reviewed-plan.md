---
title: '10.3 — Confirm the reviewed plan'
type: feature
created: 2026-10-22
status: done
owner_accepted: 2026-10-22
route: dispatch
epic: 10
story: '10.3'
alias: V1-07
story_key: 10-3-confirm-the-reviewed-plan
baseline_commit: 6ed47e0d9a146474c8c7ea2a553cdeda6848e853
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-10-context.md
---

<frozen-after-approval reason="human-owned intent — changes require human approval">

## Intent

**Problem:** Corrected private drafts cannot become explicitly reviewed, saved plans.

**Approach:** Review an exact saved revision, display blockers/unknowns/expiry, explicitly confirm, then support authorized reopening and uncertain-response recovery.

## Boundaries & Constraints

**Always:** Save before review; edits invalidate review. Require service date, activities, resolved Oslo start/end instants, nonnegative intervals and chronological starts. Permit overlaps, gaps and zero-duration transfers. Final end is the latest activity end, never an inferred header extension. Unknown types need explicit supported/manual classification. Missing passenger line/direction/destination and other permitted nonessential unknowns require explicit revision-bound acknowledgement. Preserve IDs, source facts/corrections, duty anchors, CAR and nullable bus/places.

Before confirmation show complete reviewed facts, revision, uncertainty and final-end + seven days. Validate transactionally. One draft produces at most one separate confirmed snapshot; other drafts never replace existing plans. Snapshot retention is independent of source-draft expiry/deletion. Confirmation never activates/completes work. Reject already-expired deadlines.

**Never:** Add Start, outcomes, post-confirmation editing, bus workflows (10.4), full overview (10.5), parser expansion or historical backlog repairs. Preserve session-bound access, CSRF/origin, no-store and fixed retention. No ordinary-account testing, private resets, raw-file/browser persistence, payload logging or publication before owner acceptance.

## I/O & Edge-Case Matrix

| Scenario | Input/state | Result | Failure handling |
|---|---|---|---|
| Review | Clean saved revision | Exact facts, blockers, acknowledgements, expiry | Cancel changes nothing; edits invalidate review |
| Invalid | Missing date/time/type or unordered starts | Correction guidance | No plan; draft remains editable |
| Confirm | Reviewed revision/acknowledgements | One confirmed snapshot | No replacement |
| Retry | Duplicate/lost/invalid response | Same operation resolves same plan | Remain uncertain; changed payload conflicts |
| Race | Edit/delete/expiry/account switch | Atomic rejection or accepted result | No stale/cross-account confirmation/resurrection |
| Reopen | Authorized live plan | Same facts/state/deadline | Expiry/ownership denial; related metadata purged |

</frozen-after-approval>

## Code Map

- `backend/app/draft_domain.py`, `draft_storage.py`: reuse content normalization, `authorized`, `owned`, fingerprint and lock ordering. Draft retention cannot represent confirmed retention.
- `frontend/src/PrivateDrafts.tsx`, `draftInterpretation.ts`: reuse editing/comparison/duty contracts.
- `frontend/src/PrivateAccess.tsx`: all new traffic uses existing guarded props; preserve generation checks and notification-independent identity protection.

## Tasks & Acceptance

**Execution:**
- [x] New `backend/app/workday_domain.py`, `workday_storage.py`, `backend/migrations/private/004_workdays.sql`: review/confirm/read/paginated-list/operation contracts; additive owner-scoped storage unique per source draft, retaining reviewed revision and decisions. Stable server-issued operations bind draft/revision; fingerprint includes acknowledgements/classifications. Atomically check live operation/source/session/deadline. Accepted retries depend on live plan, not surviving source; unused metadata expires with source, accepted metadata with plan.
- [x] `backend/app/private_main.py`, `private_storage.py`: private routes, bounded requests, cleanup and repeatable migration; preserve existing records.
- [x] New `frontend/src/PrivateConfirmation.tsx`; `PrivateDrafts.tsx`, `style.css` in `frontend/src/`: review/cancel/confirm, acknowledgements/classification, strict response matching, retry/lookup and minimal reopen through guarded props.
- [x] New `backend/tests/test_private_workdays.py`, `frontend/tests/private-confirmation.spec.ts`; `frontend/tests/private-identity.spec.ts`: matrix coverage, direct invalid requests, concurrent operations, changed decisions, controlled atomic expiry, suppressed broadcasts and delayed responses. Extend synthetic teardown.
- [x] `scripts/verify-private-drafts.py`: add confirmation tests and record/operation/deadline comparisons across PostgreSQL/API restart and migration replay.
- [x] `README.md`, `Docs/development-log.md`, new `Docs/evidence/10-3-plan-confirmation.md`, sprint tracking: executed evidence, review dispositions and owner walkthrough; reconcile stale status wording.

**Acceptance Criteria:**
- Given imported/manual work, when confirmed/reopened, then reviewed facts and expiry survive without activation.
- Given blockers or unacknowledged unknowns, when UI/API confirmation is requested, then no plan is written.
- Given retries/concurrent windows/changed identity, when confirmation settles, then one plan per draft and private ownership hold.
- Given keyboard use at 768/1440px in Day/Night, when reviewing/cancelling/confirming, then labels, focus, wrapping and states remain usable.

## Implementation Notes

- Final owner acceptance, 2026-10-22: Jonas reports deletion walkthrough steps 1–4 work as expected and explicitly approves story 10.3. Together with the earlier original-flow steps 1–5, this accepts the complete story including the deletion amendment. Sprint status is done; earlier acceptance-pending notes are historical. No new implementation, runtime/data action or next-story start accompanies this recording.

- 2026-10-22: Jonas approved and requested continuing. Re-read from disk; no external changes. Approved intent is frozen. Initial changes are the specification and its planning devlog entry.

- 2026-10-22: Implementation handed back for independent review. Backend/API: 195 passed (164.31s); exact restart/migration/plan-operation/deadline comparisons and production build passed. Browser: 90/92 in broad run, then all 20 confirmation/identity cases passed (1.3m) after two harness-only assertion fixes. No product changes after backend run. Actual Day/Night renders inspected, prior-story screenshot churn restored, diff check passed. Evidence and concrete owner checks recorded in `Docs/evidence/10-3-plan-confirmation.md`. Formal review, owner acceptance and runtime handoff remain with coordinator; no commit/push or operational rebuild.

- Root read the complete staged unified diff, inspected 1440 Day review and 768 Night confirmed renders, and checked each matrix row against passing backend/browser output. Implementation tasks and acceptance behaviors have executed coverage; independent review follows. Local walkthrough runtime remains to be arranged after review.

- Final root verification, 2026-10-22: 207 backend/API tests passed (179.37s), PostgreSQL/API restart and migration replay preserved complete plan/operation/decision/deadline state, production build passed, and all 97 browser tests passed in one full run (5.2m). Both mocked verifier-control tests passed separately. Root re-read patches and inspected regenerated 768 Night review /1440 Day confirmed renders. All matrix rows have passing evidence on final code.
- All three independent review layers completed. Thirteen patch findings formed eleven fix groups; all fixed and checked. Two low-impact proposals rejected with reasons above; no finding deferred. Edge and verification reviewers re-inspected their affected patches and confirmed resolution. Approved intent remained unchanged.
- Local walkthrough runtime is available at http://127.0.0.1:5173/private. Existing account/draft/operation/deletion/session/security/throttle and secret hashes matched before tests, after tests and after local upgrade. Original database container retained; only 004_workdays.sql added. Tested and operational API filesystem layers match. Feature bundle, private health and unauthenticated workday denial passed; no ordinary-account test or private-content output. Earlier runtime-pending notes are superseded.
- Spec done denotes completed implementation; sprint remains review pending Jonas's acceptance. The approved no-publication-before-acceptance boundary overrides step-05's default local commit. No commit/push or next-story start.
- Owner walkthrough feedback, 2026-10-22: Jonas reports steps 1–5 work as expected. He requests deletion of an opened confirmed plan with a warning popup before deletion. Recorded the scoped addition in [the deletion amendment](spec-10-3-delete-confirmed-plan.md); it is draft pending specification approval, not implemented or verified by the earlier totals. Keep story 10.3 in review pending this addition and final acceptance; no commit/push or next-story start.

## Spec Change Log

- 2026-10-22 final amendment handoff: deletion addition implemented, independently reviewed and verified by 213 backend/API and 120 browser tests in one complete sequential run, plus restart/migration equality, build and two mocked restoration tests. Local runtime updated preserving ordinary data; see deletion amendment for preservation details and triage. Original walkthrough passes remain recorded; final owner acceptance, commit/push and next story remain pending.

- 2026-10-22: Owner approved the deletion amendment and requested implementation. It adds an opened-plan warning/cancel/delete flow, content-free retry receipts and stale-response protection while preserving the source draft's confirmed marker. Original steps 1–5 passed; the earlier verification totals cover the original feature only. Amendment review, final verification and owner acceptance remain pending; see [deletion amendment](spec-10-3-delete-confirmed-plan.md).

## Review Triage Log

| Finding | Verdict / route | Evidence |
|---|---|---|
| Blind 1: unresolved confirmation is absent from leave guards | medium / patch | Both beforeunload and link guards use dirty only; a clean saved draft with confirmationLocked can lose its retry identity without warning. Include the existing lock in those guards. |
| Blind 2: supported classification choices diverge | medium / patch | Review advertises recognized types that the existing classification selector/request cannot accept. Align existing type choices and validation; keep source facts unchanged. |
| Blind 3: cancelled reviews retain admission slots | low / reject | The explicit bounded pending-operation contract allows 200 live attempts. Reaching it through normal review/cancel would require hundreds of cycles within seven days; adding cancellation/reuse policy and lifecycle branches is disproportionate for this uncommon condition. Existing admission rejection stays tested. |
| Blind 4: accepted plan is absent from existing list | low / patch | Acceptance updates the open snapshot only; closing it leaves the earlier list unchanged until manual refresh. Refresh discovery after accepted confirmation without losing the confirmed result if refresh fails. |
| Blind 5: confirmed source still reaches final confirmation | medium / patch | The source marker is checked only in confirm. Reject a new review of an already-confirmed source with the existing conflict guidance; retain independent draft-edit semantics and accepted-operation retries. No new draft response field is needed. |
| Blind 6: same-date plan labels can coincide | low / reject | Identity-safe reopening uses the clicked summary ID and compares the returned source/revision/deadline. Same-date/revision/deadline labels can coincide, but distinguishable preview metadata would expand the summary contract for an uncommon duplicate-day selection; no wrong-plan load or loss of access was established. |
| Blind 7: reopened response can omit required classifications | medium / patch | validPlan checks entries present, not exact required activity keys. Require the classification key set derived from existing supported-type rules; add malformed-reopen coverage. |
| Blind 8: browser pagination lacks coverage | medium / patch | Confirmed by test inspection: only API pagination is executed. Add later-page accumulation/cursor/reopen browser coverage. |
| Blind 9: same-operation concurrent confirmation lacks coverage | medium / patch | Current concurrency test uses different operations; add identical concurrent submissions returning the same plan. |
| Blind 10: source marker after plan purge lacks coverage | medium / patch | Cleanup denial is checked but not a new confirmation after plan purge or source edit. Exercise both while retaining the original source marker. |
| Verification 1: imported facts are untested in confirmation UI | medium / patch | Pre-verified regression gap: all current browser confirmation fixtures omit import_metadata. Add corrected-import source assertions in review and reopened plan. |
| Verification 2: browser pagination can regress unnoticed | medium / patch | Pre-verified regression gap: changing list(true) to list() would evade current API-only coverage. Same defect as Blind 8. |
| Edge 1: unknown activity duty change is unacknowledged | medium / patch | Assessment checks only day duty; a null/blank activity anchor overrides known duty and appears unknown in reviewed facts without an acknowledgement. Include these existing anchors in assessment and test it. |
| Edge 2: unresolved operation can be lost through navigation | medium / patch | Same demonstrated leave-guard defect as Blind 1; include confirmationLocked and test navigation protection. |
| Root: verifier control-flow fixture no longer reaches its assertion | medium / patch | scripts/test_verify_private_drafts.py returns an empty imported model, but the expanded verifier indexes activities before its mocked fictional-API prerequisite check. Update the mock to cover confirmation setup and run both existing restoration unit tests. |

## Design Notes

Dispatch: additive schema/API/UI; no unresolved intent questions. Verify migration on disposable storage first.

Retrospective: E9-A1 done, preserve regression coverage. E9-A2 atomic-expiry lesson applies; old draft-create defect stays open. E9-A3 requires discoverable new plans; old draft-list repair stays open. E9-A4: verify new operation admission at 200, rejection without mutation, accepted/expired exclusion. E9-A5: inspect identity/transaction boundaries, sequential restart/browser verification and story-labelled future commits. No automatic action closure.

## Verification

Run `scripts/verify-private-drafts.py` with `COMPOSE_PROJECT_NAME=ibe160-private-tests`, `npm.cmd run build`, and `git diff --check`. Backend/restart/browser phases run sequentially with synthetic storage; restore operational availability preserving accounts/volume/secret. Inspect rendered states and browser-storage absence. Complete independent BMAD review layers, fix findings and provide owner checks before acceptance. No tests/runtime changes during planning.

## E10-A1–A3 maintenance follow-up — 2026-10-24

The approved draft-contracts bundle preserves the normalized original import baseline (including absence for manual drafts), shares fresh-write physical-bus semantics, and pins review policy to issued operations and confirmed plans. Missing deadhead/CAR trip numbers remain visible as unknown without a separate acknowledgement; passenger direction joins the draft unknown display. Historical acceptance above remains unchanged. See [the maintenance evidence](../../docs/evidence/epic-10-draft-contracts.md). Implementation checks and owner acceptance for this follow-up are tracked separately; E10-A1–A3 remain in-progress.

| Missing or uncertain fact | Required action for a new confirmation |
|---|---|
| Service date; at least one activity; explicit valid Oslo start/end; nonnegative intervals and ordered starts | Correct and save; acknowledgement cannot bypass these blockers. |
| Unsupported/missing original activity type | Choose an explicit supported classification for the saved revision. |
| From/to place, any supported type | Explicit acknowledgement for each missing place. |
| Passenger trip number, line or direction | Explicit acknowledgement for each missing identifier. |
| Trip number for supported deadhead/CAR movement | Visible “Ukjent”; no separate acknowledgement, per Jonas's 2026-10-24 choice. |
| Movement line/direction; identifiers for other supported non-passenger work | No dedicated missing-identifier acknowledgement. |
| Initially unsupported original type | Preserve the existing passenger-identifier acknowledgement superset, even after classification. |
| Day duty/bus; explicitly unknown duty-change anchor | Explicit acknowledgement. |
| Nonempty uncertainty note; retained unresolved source issue or source annotation | Explicit acknowledgement of each listed item. |
| Source clocks, original raw code or provenance | No new dedicated acknowledgement for absence; never invent a value. |

Existing issued reviews and confirmed plans retain their pinned historical policy and decisions. Activity absence presentation matches the existing assessment whitespace semantics; physical bus uses its separate explicit Unicode White_Space contract. These changes do not add activity activation, progress or later Epic 11 behavior.

## Owner review amendment — 2026-10-24

For newly issued reviews, the approved `spec-epic-10-review-feedback.md` narrows acknowledgements to effective passenger trip activities only: missing trip number, line, direction, from/to place or substantive current uncertainty. Classification changes remove obsolete candidates and checked decisions; returning to trip does not restore removed checks. Confirmation independently derives the exact effective set; missing/extra decisions reject atomically. Client acceptance compares the plan against frozen submitted classifications. Service date/activity/time/order/expiry blockers remain strict.

Existing v1/v2 operations/plans keep their original first-acceptance/replay/presentation semantics; policy 3 is pinned only on fresh issuance via migration 008. Original marker/source issues remain neutral source information, with exact generated marker text excluded from current warnings without rewriting saved facts. Recognized Trip/trip type/code display becomes tur. Original story acceptance remains historical; amendment owner acceptance is pending.
