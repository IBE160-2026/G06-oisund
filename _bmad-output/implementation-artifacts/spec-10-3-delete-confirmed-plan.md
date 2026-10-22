---
title: '10.3 amendment — Delete a confirmed plan'
type: feature
created: 2026-10-22
status: done
owner_accepted: 2026-10-22
route: dispatch
epic: 10
story: '10.3'
story_key: 10-3-confirm-the-reviewed-plan
baseline_commit: 6ed47e0d9a146474c8c7ea2a553cdeda6848e853
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-10-context.md
  - D:/IBE160/_bmad-output/implementation-artifacts/spec-10-3-confirm-the-reviewed-plan.md
---

<frozen-after-approval reason="owner-requested addition to the reviewed 10.3 behavior">

## Intent

**Problem:** Opened confirmed plans cannot be deleted.

**Approach:** Add **Slett bekreftet plan** to the opened confirmed plan, with a mandatory confirmation popup before any deletion request. Suggested wording: “Slette denne bekreftede planen? Dette kan ikke angres. Kildeutkastet beholdes.”

## Boundaries & Constraints

**Always:** Cancel preserves everything. Confirmation deletes only the selected owner's live plan and its confirmation metadata. Preserve the source draft and its confirmed marker: no late recreation from that draft. A new plan requires a separate draft. Other records and deadlines remain unchanged.

Use displayed-session guards, CSRF/origin, no-store and server ownership. Bind deletion to the selected plan ID, source revision and a stable operation ID. Atomically authorize, check expiry/version, record a content-free acknowledgement and delete. Identical retries return that acknowledgement; changed target/version conflicts. A receipt expires at the original plan deadline and never contains plan facts. Recheck live deadlines at acceptance; roll back if they expire. No deleted content may reappear through an old confirmation retry or delayed browser response.

While a reply is uncertain, keep the operation for lookup/retry and protect navigation/replacement; never claim deletion from HTML, malformed JSON or a network error. After a valid acknowledgement clear the open plan, remove its summary and invalidate older reads. Explain that source drafts already used for confirmation require a new draft for another plan.

**Never:** Delete an ordinary private record during automated tests, reset storage, add bulk/account deletion, restore deleted plans, change draft/confirmation contracts, start 10.4, or commit/push before owner acceptance.

## I/O & Edge-Case Matrix

| Scenario | Input/state | Behavior | Failure handling |
|---|---|---|---|
| Cancel | Open plan, dismiss popup | No mutation; plan remains | Preserve current presentation |
| Delete | Explicit popup acceptance | Only selected plan disappears after reload | Source/other records remain |
| Retry | Double click or lost/invalid reply | Same operation settles one deletion | Uncertain until valid reply/lookup |
| Reject | Other owner, changed version/target, expired session/plan | No unauthorized mutation | Explicit denial/conflict; fixed deadlines |
| Late traffic | Old list/read/confirmation after deletion | Cannot restore display or storage | Discard stale response; deny resurrection |

</frozen-after-approval>

## Code Map

- `backend/app/workday_storage.py`: reuse `owned`, `draft_storage.authorized` and owner serialization; accepted confirmation operations cascade with the plan.
- `backend/app/draft_storage.py`: existing `delete`, `deletion`, `deletion_lookup` provide the receipt/retry pattern.
- `backend/app/workday_domain.py`, `private_main.py`, `private_storage.py`: strict models, private routes and startup/hourly cleanup.
- `frontend/src/PrivateConfirmation.tsx`: opened `plan`, summaries, guarded props and async state. Extend parent `lock` so unresolved deletion gets existing leave protection.

## Tasks & Acceptance

**Execution:**
- [x] New `backend/migrations/private/005_workday_deletions.sql`; `backend/app/workday_domain.py`, `workday_storage.py`, `private_main.py`, `private_storage.py` — additive minimal receipts, delete/lookup contracts, atomic expiry/session/version checks and cleanup. Preserve existing records and source marker.
- [x] `frontend/src/PrivateConfirmation.tsx` — opened-plan button, warning/cancel, strict matching, uncertain retry/lookup, stale-response invalidation and source-reuse guidance. Reuse guarded traffic and parent lock.
- [x] `backend/tests/test_private_workdays.py`, `frontend/tests/private-confirmation.spec.ts`, `frontend/tests/private-identity.spec.ts` — execute every matrix row with synthetic data, including concurrent identical deletion, expiry at acceptance, changed identity and delayed read/list races. Extend synthetic teardown for receipts.
- [x] `scripts/verify-private-drafts.py`, `scripts/test_verify_private_drafts.py` — verify deletion receipts/retries across actual restart and migration replay; preserve restoration unit tests. Final root sequential run and both mocked restoration tests passed.
- [x] `Docs/evidence/10-3-plan-confirmation.md`, `Docs/development-log.md`, `README.md`, original 10.3 spec and sprint tracking — record feedback, amendment evidence/review and popup/cancel/delete/reload walkthrough.

**Acceptance Criteria:**
- Given an opened confirmed plan, when deletion is requested, then the warning appears and cancellation changes nothing.
- Given explicit acceptance, when deletion settles, then that plan stays absent after reload and other records remain unchanged.
- Given uncertain replies or late traffic, when retry/lookup settles, then deletion is acknowledged safely without resurrection or cross-account access.
- Given keyboard use in Day/Night at 768/1440px, when opening/cancelling/accepting the popup, then controls and resulting status remain usable.

## Implementation Notes

- Final owner acceptance, 2026-10-22: Jonas confirms deletion walkthrough steps 1–4 work as expected and explicitly approves story 10.3. Amendment and original flow are accepted; sprint status is done. This supersedes earlier acceptance-pending notes.

- 2026-10-22: Jonas explicitly approved and requested continuing. Re-read from disk; no external changes. Approved intent is frozen. Preserve all previously staged 10.3 work and documentation; ordinary private plans are not test targets.
- Final root verification: 213 backend/API tests passed (198.92s), exact plan/operation/deletion-receipt/source-marker/deadline state survived PostgreSQL/API restart and migration replay, production build passed, and all 120 browser tests passed in one clean run (7.6m). Both mocked restoration tests passed separately (0.094s). Log: local ignored `tmp/10-3-deletion-final-verification.log`. Every matrix row and all acceptance behaviors have executed coverage on final code; actual tablet qualification is not claimed.
- Three independent review layers completed; seven patch groups resolved and relevant reviewers re-inspected. No finding deferred. Root read all patches and inspected four Day/Night deletion result renders. Earlier-story screenshot churn restored; intended 10.3 images retained.
- Local walkthrough is available at http://127.0.0.1:5173/private. Existing accounts/drafts/plans/operations/deletions/sessions/security settings and secret hashes matched before and after tests and local upgrade. Routine startup cleanup removed three expired login-throttle rows; all other existing hashes were identical. Same database container retained; only 005_workday_deletions.sql added. Tested and operational API filesystem layers match; frontend bundle, private health and unauthenticated receipt denial passed. Disposable services stopped.
- Done denotes implementation completion. Sprint stays review pending Jonas's deletion walkthrough and final acceptance. The approved no-publication-before-acceptance boundary overrides the generic step-05 local commit instruction. No commit/push or 10.4 work.

- 2026-10-22 implementation handoff: three focused backend deletion tests passed (7.28s); all thirteen focused deletion browser cases passed on final rebuilt code in one run (1.0m); both mocked verifier restoration tests passed (0.126s); final TypeScript/Vite production build and diff check passed. Browser matrix covers cancellation/reload, five uncertain-response variants, navigation/replacement guards, stale list/read responses and silent account switches before mutation/after acceptance. A matching guarded receipt read revalidates displayed identity before accepting a mutation reply. Actual 768 Night and 1440 Day result images inspected; all four viewport/theme renders saved. Exact focused logs are in the system temp directory as `ibe160-deletion-backend.log` and `ibe160-deletion-browser.log`. Independent review, full sequential verifier/restart replay and owner acceptance remain with coordinator; no commit/push or next-story work.

## Spec Change Log

## Review Triage Log

| Finding | Verdict / route | Evidence |
|---|---|---|
| Blind 1: deletion removes pagination continuation | low / patch | Acceptance clears cursor while retaining a partial list. The UUID continuation remains valid after deletion; retain it and verify later-page access. |
| Blind 2: another window's deletion leaves an unresolved attempt | low / reject | A distinct operation cannot claim another operation's acceptance. Keeping uncertainty is intentional; the existing navigation warning allows leaving/reloading and the fixed deadline clears it. Adding an absence-reconciliation contract for this uncommon competing-window case adds public/state complexity and could mistake proxy 404 for proof. |
| Blind 3: failed reopen retains the affected old snapshot | medium / patch | A same-ID reopen returning 404/410 currently leaves that snapshot labelled confirmed. Clear that affected presentation on denial without claiming deletion or clearing a different open plan. |
| Blind 4: expiry can strand busy after invalidating a read | medium / patch | Expiry advances reading generation; list/reopen finally then skips setBusy(false). Clear busy in the existing expiry reset and exercise a held response. |
| Blind 5: delayed confirmation lacks post-response session validation | high / patch | The mutation wrapper validates before sending only; send can accept an old-account response after a silent cookie change. Reuse the existing guarded operation lookup before accepting mutation results, with a delayed-ack identity regression. No new surface/state is needed. |
| Blind 6: generic deletion popup lacks distinguishing date | false / reject | The only deletion control belongs to the single opened plan; its Facts already displays Tjenestedato and all distinguishing facts immediately above. Popup targets that captured immutable ID/revision. No wrong-target path was established; the approved warning text is present. |
| Blind 7: a different window can delete a snapshot before an old read arrives | low / reject | Snapshot reads have no cross-window freshness subscription. Explicit refresh/reopen checks authority; same-component deletion invalidates old reads. Adding cross-window synchronization/revalidation for same-account snapshots is more than a direct correction for this uncommon freshness interval. Ownership and cross-account guards remain enforced. |
| Blind 8: different-operation competing deletions lack coverage | medium / patch | Same-operation concurrency is covered; distinct IDs are not. Add a server regression proving one acceptance/receipt and one denial, preserving source and unrelated records. Recovery retains the approved uncertain-until-own-receipt contract. |
| Blind 9: deletion after source disappearance lacks coverage | medium / patch | Independent reads/retries exist, but deletion tests retain the source. Add source-deleted and source-expired/cleaned deletion/replay checks, fixed receipt deadline and cascading accepted metadata. |
| Blind 10: mandatory receipt read failures lack coverage | medium / patch | Existing corrupt-reply cases alter POST, leaving its later guarded GET healthy. Cover failed/malformed/mismatched and delayed receipt reads; retain stable identity and recover only the selected plan. |
| Verification 1: unresolved deletion expiry lacks browser coverage | medium / patch | Pre-verified gap: existing clock case expires a summary only. Add a clock-driven uncertain deletion that expires, clears facts/retry/navigation locks and discards a released response; also cover the busy reset above. |

- All three review layers completed; edge-case layer returned no findings. The arithmetic/finding-floor line is not a defect. Findings were individually classified before grouping. Patch groups: pagination; affected-reopen presentation; expiry reset/coverage; confirmation identity; competing server operations; missing-source deletion; receipt-read failures. No bad-spec or intent gap was found; approved intent is unchanged. No finding deferred.
- All seven patch groups implemented. Three new backend cases passed (6.77s). All thirteen selected browser scenarios have passing evidence across focused runs; four setup races/formats and transport-versus-retention clock interactions were corrected in tests only. No clean single thirteen-case run is claimed. Production build/diff check passed. Blind reviewer reinspection confirmed all four production fixes; verification reviewer confirmed expiry assertions cover facts, controls, busy/navigation lock release and delivered late responses. Final root sequential verification follows on the patched tree.

## Design Notes

Dispatch: additive migration/API/UI; no intent gaps. Preserve authorized staged 10.3 work. Original walkthrough passes are recorded; final acceptance awaits this addition. No runtime action during planning.

## Verification

Use `COMPOSE_PROJECT_NAME=ibe160-private-tests` with `scripts/verify-private-drafts.py`, mocked verifier tests, `npm.cmd run build` and `git diff --check`. Keep phases sequential. Complete independent BMAD review, inspect popup/result states, preserve ordinary data/volume/secret and provide owner checks. Earlier totals do not verify this addition.
