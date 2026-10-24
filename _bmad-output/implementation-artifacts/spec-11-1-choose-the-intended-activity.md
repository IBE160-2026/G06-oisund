---
title: '11.1 — Choose the intended activity'
type: feature
created: 2026-10-24
status: done
approved_on: 2026-10-24
owner_acceptance: accepted
owner_accepted_on: 2026-10-24
route: dispatch
review_loop_iteration: 0
epic: 11
story: '11.1'
alias: V1-10
story_key: 11-1-choose-the-intended-activity
baseline_commit: 81f1a54efbfb2ba8c14da0c9017a1e9f5614d9d9
implementationStarted: true
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-11-context.md
---

<frozen-after-approval reason="human-owned intent — changes require human approval">

## Intent

**Problem:** The confirmed day has no saved manual activity selection or explicit shift start.

**Approach:** Add direct and previous/next choice by stable activity ID, plus a separate `Start skift` action. Restore both acknowledged selection and start status online. Implements FR-6/10/11/20, AC-03 and the explicit UX activation contract after accepted 10.5. Owner chose alternative 2 on 2026-10-24 and authorized implementation, verification, independent review and routine fixes; stop in review for final acceptance, without commit, push or next story.

## Boundaries & Constraints

**Always:** Initially show `Ingen aktivitet valgt`. Identify choices by type, line, direction/destination and planned Oslo date/time; missing facts stay `Ukjent`. Show one prominent `Valgt tur`/`Valgt aktivitet`, `Manuelt valgt` and a textual list marker. Previous/next follows confirmed activity order, including non-passenger rows and individual grouped-pause members. Gaps are not activities. Preserve equal-time order and overnight dates.

Choice attempts online saving; mark proposals until acknowledged. Lock further choices while unresolved; offer check/retry. Boundaries: `Velg en aktivitet først`, `Ingen forrige aktivitet`/`Ingen neste aktivitet`. Selecting the saved ID is a no-op.

Preserve immutable snapshots, source/policy decisions, bus, deadlines and identity guards. Selection never starts, completes, skips or closes work. No clock-driven choice, location claim or private browser persistence.

`Start skift` is available independently of selection: consultation and saved selection work before and after start. Initially display `Ikke startet`; explicit acknowledged start changes it to `Startet manuelt` with authoritative server `started_at`. Display `Planlagt start` separately using the first confirmed activity start; label it planned, preserving existing reporting/source distinctions. Actual start is the time of first accepted explicit start, never scheduled departure, selection time or proof of physical driving. Start does not select or complete anything, modify bus, start another plan, or extend retention. No one-active-plan exclusivity is introduced.

Start is one-way in this story. Same-operation retry returns its immutable receipt. A second start operation on an already started live plan returns the original actual start/status without advancing lifecycle revision or changing time. Changed payload/target for an operation conflicts. Concurrent start attempts converge on one server timestamp. A lost reply remains unresolved until checked/retried; never show success from local intent. Reopening/reloading reads current lifecycle state, including starts from another window.

**Later:** 11.2 adds expanded consultation using this selected ID and lifecycle read. 11.3 owns outcomes/end/abort/recap and extends this lifecycle resource, reusing the existing start action/timestamp without implementing another Start. It must define closure/shortened retention and terminal write guards across selection/bus/start. No outcome/closure/undo-start control here. 11.4–11.5 own notices; 11.6 integrated recovery. Truthful failures apply now. E10-A4/A5 remain in 12.3/12.4.

## I/O & Edge-Case Matrix

| State | Result / recovery |
|---|---|
| Direct/previous/next | Save exact member ID; reload restores it; no other facts change |
| Foreign-plan/invalid activity ID | Reject without state or receipt mutation |
| Stale revision | Keep proposal, show saved selection for comparison; explicit reload, no overwrite |
| Lost/HTML/malformed reply | Unresolved; retain original operation/body in memory; lookup or same retry |
| Older receipt than current selection | Report accepted attempt separately; never revert newer state |
| Start without selection / selection before start | Save start independently / leave lifecycle unstarted |
| Repeated/concurrent start | Same first server time and lifecycle revision; no duplicate start effect |
| Planned time passes / start before or after planned time | Planned facts unchanged; only explicit start sets actual timestamp |
| Start reply lost or reload | Same-attempt recovery / authorized current lifecycle read; no guessed status |
| Denial/expiry/deletion/session change | Hide authoritative presentation, revalidate or clear; stale replies cannot restore it |

</frozen-after-approval>

## Code Map

- `frontend/src/PrivateConfirmation.tsx`: aggregate independent bus/selection locks and availability; one child cannot unlock/unhide another.
- `frontend/src/PrivateBus.tsx`, `PrivateAccess.tsx`: reuse guarded requests, identity validation, recovery and leave protection.
- `frontend/src/PrivateDayOverview.tsx`, `dayOverview.ts`, `draftInterpretation.ts`: reuse members, labels, classifications, Oslo/unknown helpers; preserve grouping/details.
- `backend/app/workday_bus_storage.py`, `workday_bus_domain.py`: resource/receipt pattern; reuse `draft_storage.authorized`, `workday_storage.owned` locks/access.
- `frontend/src/useWorkdayResource.ts`, `activityChoiceLabel.ts`: introduced shared in-memory recovery and per-type choice descriptions; both selected/direct views reuse the same fact applicability without changing bus writes.

## Tasks & Acceptance

**Execution (after approval):**
- [x] `backend/migrations/private/009_workday_selection.sql`: add selection, lifecycle and respective receipt tables with parent-delete cascades; preserve existing rows/contracts. Missing lifecycle means confirmed/not started, revision 0; first start creates active/revision 1/server timestamp. Keep historical WorkdayRecord/confirmation receipts compatible; current lifecycle is separate authority.
- [x] New `backend/app/workday_selection_domain.py`, `workday_selection_storage.py`: strict UUID/revision/membership validation, atomic writes and final session/expiry checks. Initially null/revision 0; writes require an ID. Cap live receipts at 2000/account; accepted retries bypass admission.
- [x] `backend/app/private_main.py`: GET/POST `/workdays/{id}/selection`, GET `/workday-selection-operations/{id}`; return workday/activity ID, revision, fixed expiry and operation receipt. `private_storage.py`: expire receipts in existing cleanup.
- [x] New `backend/app/workday_lifecycle_domain.py`, `workday_lifecycle_storage.py`; `private_main.py`: GET `/workdays/{id}/lifecycle`, POST `/workdays/{id}/start`, GET `/workday-start-operations/{id}`. Strict start body: operation_id and expected_revision (nonnegative strict integer). Return workday_id, state confirmed/active, started_at null/server timestamp, revision and fixed expiry. Reject revision mismatch except already-active expected 0/current revision retries, which return original state without mutation; cap live receipts at 2000/account. Apply selection-equivalent ownership, fingerprint, transaction, expiry, postwrite session, cascade and cleanup protections.
- [x] New `frontend/src/PrivateActivitySelection.tsx`; `PrivateConfirmation.tsx`, `PrivateDayOverview.tsx`, `style.css`: selector, member actions/markers, aggregate guards, retained proposals/operations and accessible feedback.
- [x] New `frontend/src/PrivateShiftStart.tsx`; `PrivateConfirmation.tsx`: current lifecycle presentation and separate Start/status/check/retry, planned/actual labels, validated current-state reconciliation and combined selection/start/bus availability/locks. Replace misleading unconditional current `Status: bekreftet` with lifecycle status, retaining historical confirmation information. An unavailable lifecycle is unknown/unavailable, never assumed unstarted. No new user gesture is needed to inspect/select before start.
- [x] New `backend/tests/test_private_selection.py`, `test_private_start.py`, `frontend/tests/private-selection.spec.ts`, `private-start.spec.ts`; extend `private-identity.spec.ts`, `scripts/verify-private-drafts.py`: every matrix row for both writes, start concurrency/replay with exact time/revision equality, restart/migration equality for raw state and receipts, legacy-unstarted plan compatibility and demo denial.
- [x] `docs/evidence/11-1-activity-selection.md`, `docs/development-log.md`, `README.md`, sprint: actual results, limitations and owner checks.

**Acceptance Criteria:**
- Given 20/24, repeated lines, opposite directions and midnight, when selecting/reloading or scheduled time passes, then exact expected ID/date remains selected.
- Given pauses/transfers/single-member/boundary cases, when navigating, then all members are reachable with correct disabled labels and unchanged outcomes/lifecycle/bus/snapshot.
- Given concurrency, atomic expiry, denial or uncertain replies, when recovering, then only live authorized effects persist without resurrection/rollback.
- Given both themes, keyboard, long names and enlargement, when selecting/recovering at tablet/PC widths, then rendered states meet IR-01 without clipping.
- Given an unstarted confirmed plan, when selecting/viewing/previous/next or planned time passes, then start remains unregistered and no activity outcome is recorded.
- Given any or no selection, when explicitly starting and reopening/reloading, then active state and original server actual start persist separately from unchanged planned times and selected ID.
- Given repeated clicks, simultaneous windows, lost responses or a new start attempt after success, when retrying/reconciling, then exactly one actual start timestamp/revision persists, with truthful acknowledgement and unchanged expiry.

## Implementation Notes

- 2026-10-24: User explicitly expanded/approved scope with separate Start and authorized implementation through review handoff. Existing dirty files are only this story's preparation context/spec/log and are retained. No additional start approval or spec-size gate is required by this owner-approved scope. Product acceptance remains pending. Keep shared-service verification sequential and synthetic-only; preserve operational data/security/secret/volume. Do not deploy unverified backend code. Root owns final broad verification, ordinary-state preservation check and manual handoff; implementation worker restores services before returning. No staging, commit, push or next story. The owner overrides generic workflow staging/completion/commit steps.

## Spec Change Log

## Review Triage Log

All three context-free layers completed before triage. Blind hunter filed ten candidates; edge hunter returned no findings after its sandbox read was retried with approved access; verification-gap filed one pre-verified regression gap. Each candidate is retained individually below. Ten findings form nine direct patch groups; one unreachable hardening proposal is rejected. No intent change or new public API is required.

| Finding | Verdict / route | Evidence and disposition |
|---|---|---|
| B1: direct-choice accessible context | medium / patch | Member buttons expose only an ordinal action name; nearby route/direction/time prose is not associated. Bind distinguishing facts through an accessible description while preserving per-type applicability. Shares the presentation correction with B4. |
| B2: identical-member selected summary | medium / patch | Two distinct UUID members can have identical rendered facts; the selected summary has no ordinal. Add a user-facing activity number and verify otherwise-identical members retain distinct selected identity. |
| B3: programmatic selected relationship | low / patch | Current state is adjacent prose and disabled presentation only. Add the direct current-member relationship and an assertion; one attribute is a direct correction. |
| B4: repeated choice facts | low / patch | The new helper paragraph repeats type/start/places/identifiers already visible in the row, increasing enlarged-list scrolling. Consolidate visible facts and associate the choice description without losing information. |
| B5: refresh revision regression | false / reject | Reviewer clarification found no ordinary reachable path and withdrew the actionable claim. It requires an injected syntactically valid stale server record: busy/sending/generation guards prevent overlapping UI adoption, reads lock the same PostgreSQL owner/plan, and request/response are no-store. Optional high-water state is not added for this undemonstrated runtime path. |
| B6: direct-choice contrast/focus evidence | medium / patch | Existing measurements enumerate selector/start controls but omit `.day-member button`. Extend actual enabled/current-disabled/focused direct-choice checks in both themes; disabled controls are not focusable. |
| B7: malformed current-record evidence | medium / patch | Mutation receipts have malformed tests; initial/refreshed resource reads lack independent foreign-ID/deadline/member/lifecycle-invariant cases. Add bounded-response regressions for both current resources, preserving unknown/unavailable feedback. |
| B8: account-wide receipt-capacity evidence | medium / patch | Current cap fixture occupies one plan only; a per-plan query regression could pass. Add cross-plan saturation with a separate-account control and no accepted mutation on rejection for both resources. |
| B9: historical screenshot churn | medium / patch | Broad tests regenerated accepted 9.x/10.x PNGs. Root restores those tracked artifacts, retaining separately named synthetic 11.1 evidence; repeat restoration after final tests. |
| B10: stale canonical planning status | low / patch | The new allocation is followed by an unqualified backlog/not-started statement. Label the 11.1 planning baseline as historical and link current sprint/spec state, without changing later stories. |
| G1: actual-start display equality | medium / patch | Pre-verified: API/storage assertions would pass if actual-time rendering used plannedStart. Assert rendered planned and actual Oslo timestamps independently against the server value before and after reopen/reload. |

Root's earlier per-type label regression, truthful resolution feedback, collapsed-group identity and acknowledged-action focus corrections passed 44 affected browser cases plus all six unchanged day-overview regressions before this review. The approved frozen block remains unchanged. Final patch results and broad verification follow below.

Review corrections passed two new cross-plan/account PostgreSQL cases, six unchanged day-overview regressions, all 30 edited selection/start cases and three final caption/identity/IR-01 cases after the last frontend rebuild. Original blind and verification-gap reviewers re-inspected the fixes and found no remaining concrete defect in those scopes; edge review had no findings. Direct descriptions/current state, ordinal identity, per-type visibility, resolved feedback/focus and rendered actual timestamp equality are verified. All retained findings are resolved; none deferred. Root's final verification passed as recorded below. Jonas explicitly accepted story 11.1 on 2026-10-24 after positive manual feedback.

## Design Notes

Separate state preserves historical receipts/bus revisions. Bind receipts to owner/plan/body; verify current state before success. No dependency change. Migration/persistent effects occur only after authorization.

## Verification

Root verification is complete: 302 PostgreSQL/API tests passed (361.44s), exact populated restart/repeated-migration comparisons and demo denial passed, production TypeScript/Vite build passed, and the final complete Edge browser suite passed 257 tests (15.3m). Five isolated verifier controls passed (0.147s). The reviewed combined run's earlier single timing-observation failure is retained honestly in the log; bounded polling preserves the same guard assertions. A deterministic DST fixture test now checks exact UTC elapsed offsets. These last changes are test-only; the successful final whole-browser run uses unchanged reviewed production code.

Every approved matrix/acceptance row has executable backend/browser coverage: exact ordered identity and non-selection gaps; independent pre-start/post-start choice; unchanged outcomes/snapshot/source/bus/expiry; server actual/planned display equality through reopen/reload; repeated/concurrent first-start equality; receipt/current conflicts; malformed/uncertain/current-denied states; session/expiry/deletion no-resurrection; and Day/Night keyboard/enlargement/IR-01. All four final 768/1440 Day/Night renders were visually inspected without observed clipping. Actual iPad/Safari and actual assistive-technology use remain unperformed; E10-A4/A5 stay assigned to 12.3/12.4.

The local API filesystem matches the tested backend image and served frontend assets match tested output byte-for-byte. Additive migration 009 is registered; no ordinary account was used for automated testing. Original business/policy/session/security/secret digests and database container/volume are preserved, apart from exactly three expired throttle rows removed by unchanged startup cleanup; post-test and post-upgrade digests equal the restored post-worker baseline. Ordinary services are healthy, disposable services stopped, and regenerated historical PNGs restored. See [executed evidence and owner checks](../../docs/evidence/11-1-activity-selection.md).

Jonas explicitly accepted 11.1 on 2026-10-24 and subsequently authorized commit and push. Specification and sprint story are now done; Epic 11 remains in-progress and later stories stay backlog. This later authorization supersedes the earlier review/publication stop without changing approved frozen intent. Actual-device follow-up is unchanged; no next story is started.
