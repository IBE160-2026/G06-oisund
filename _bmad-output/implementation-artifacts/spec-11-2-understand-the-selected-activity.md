---
title: '11.2 — Understand the selected activity'
type: feature
created: 2026-10-24
status: done
owner_acceptance: accepted
owner_accepted_on: 2026-10-25
approved_on: 2026-10-24
route: dispatch
review_loop_iteration: 0
epic: 11
story: '11.2'
alias: V1-11
story_key: 11-2-understand-the-selected-activity
baseline_commit: 5160feeba20bb2d5730d37aa96b130a6fd23e86c
implementationStarted: true
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-11-context.md
---

<frozen-after-approval reason="human-owned intent — changes require human approval">

## Intent

**Problem:** The compact selected summary omits planned end, missing non-passenger places and current uncertainty.

**Approach:** Expand the selected activity using confirmed facts and separate preparation, day and activity screens: FR-3/10, NFR-2, AC-03, SCOPE-02; reuse accepted 11.1. Owner approved implementation with the screen-separation amendment on 2026-10-24; no further approval checkpoint for this amendment.

## Boundaries & Constraints

**Always:** Keep `Valgt tur` / `Valgt aktivitet`, `Manuelt valgt` and activity ordinal. Resolve the exact saved activity ID and confirmed classification. Show type, separately labelled `Planlagt start` and `Planlagt slutt`, both with calendar date/time in Europe/Oslo. Keep service date distinct in the existing day heading.

Use separate, clearly navigable screens: upload document → inspect/edit interpretation and explicitly confirm → open chronological day → select/open an individual activity → return to day. Import, editor, full day list and selected detail must never form one long combined visible page. Day may scroll. Activity prioritizes only that member, planned facts and previous/next; long/enlarged content remains accessible by scrolling. Direct choice opens the activity screen after acknowledgement; opening an already saved selected activity requires no write. Back to day preserves the saved choice and all registered data. Opening another screen must not discard unsaved draft input or unresolved mutation/recovery state: keep necessary controllers mounted or explicitly guard destructive transitions. Never hide the only recovery action behind an inaccessible screen. Show a meaningful heading/focus on screen transitions, and keep keyboard/touch navigation and access revalidation intact. No private persistent route/payload cache.

Keep existing bus and Start controls naturally accessible from the day, separate from selecting/consulting. Preparation remains reachable without destroying the open plan; keep plan/draft lists accessible through clear navigation. Place future notices (11.4/11.5) as a secondary day-linked screen and future end/abort/recap (11.3) in day/shift navigation; document destinations without fake working controls or implementing those stories. Intermediate-stop extraction/display is post-V1. Preserve the limited working demo; its expansion stays later work.

Passenger trips show line, trip number, direction and `Fra` / `Til`. Non-passenger activities show their actual type and `Fra` / `Til`; preserve any supplied identifiers, but omit absent irrelevant line/direction fields. Missing deadhead/CAR trip number remains neutral `Ukjent`. Missing places display `Ukjent` for each endpoint, without borrowing another activity's depot or interpreting Travel to as CAR.

Show current uncertainty and associated neutral source markers; never attach unlocated markers. Keep historical issues and source/correction details in the day list. Explain `Stoppdata er ikke tilgjengelig i denne visningen.` separately from disabled `Ingen forrige aktivitet` / `Ingen neste aktivitet`; no stop placeholders.

Reuse acknowledgement, comparison, retry, identity/access and expiry guards. Proposals never become authoritative. Retain `Ingen aktivitet valgt` and existing unavailable states. Consultation works before/after `Start skift`, changing no lifecycle, outcomes, bus, source facts or retention.

**Later:** 11.3 owns outcomes/end/abort/recap and extends existing start; 11.4–11.5 own notices; 11.6 integrates recovery. No new start, API/schema, enrichment, GPS/current-next stop, timer, automatic progression or private browser persistence. Theme persistence/device qualification remain 12.3/12.4 obligations.

## I/O & Edge-Case Matrix

| State | Expected consultation |
|---|---|
| Lines 20/24, opposite direction, identical facts | Exact saved member, ordinal and distinguishing facts |
| Midnight / extended source clock | Explicit start/end calendar dates; no reinterpretation of service date |
| Pause group | Selected member's type/times/places, never group's aggregate interval |
| Null/blank facts | Field-specific `Ukjent`; no inferred place or new acknowledgement |
| Corrected classification/source uncertainty | Confirmed facts and current uncertainty; historical issues stay historical |
| First/last/single activity | Missing facts and navigation boundaries remain distinct |
| Failed/stale choice, denial/expiry/account change | Existing guarded recovery; no proposed or stale private detail promoted |
| Upload → edit → confirm → day → activity → day | One primary screen at a time; correct acknowledgement, preserved data/selection and no implicit start/outcome |
| Navigate with unsaved input or unresolved command | Preserve memory and recovery; no silent loss, false success or bypass of existing guards |

</frozen-after-approval>

## Code Map

- `frontend/src/PrivateActivitySelection.tsx`: current `.selected-activity` summary and authoritative visibility gate; integrate detail here.
- `frontend/src/SelectedActivityDetails.tsx` (new): read-only selected-member presentation, no resource ownership.
- `frontend/src/activityChoiceLabel.ts`: preserve compact labels and per-type applicability.
- `frontend/src/dayOverview.ts`: reuse `dayTypeLabels`, `osloDateTime`, `projectDay` member identity/classification.
- `frontend/src/draftInterpretation.ts`: reuse absence/uncertainty/source helpers; preserve passenger-only policy.
- `frontend/src/PrivateDayOverview.tsx`: retain chronological list, grouped members and source details.
- `frontend/src/PrivateConfirmation.tsx`, `PrivateShiftStart.tsx`, `useWorkdayResource.ts`: preserve guards/start/recovery.
- `frontend/src/PrivateDrafts.tsx`, `PrivateImport.tsx`, `PrivateAccess.tsx`: preparation/import/edit/confirmed-plan screen ownership, transient input and security boundaries; keep mounted state safe during internal navigation.

## Tasks & Acceptance

**Execution after owner approval:**
- [x] `frontend/src/PrivateDrafts.tsx`, `PrivateImport.tsx`, `PrivateConfirmation.tsx`, `PrivateActivitySelection.tsx` — separate upload, control/edit, day and activity screens with clear forward/back navigation, focus and retained state; preserve mutation/access guards. Add a small shared navigation component only if useful; no routing dependency required.
- [x] `frontend/src/SelectedActivityDetails.tsx`, `PrivateActivitySelection.tsx` — replace compact saved summary with labelled details; preserve selector behavior and `.selected-activity` hooks.
- [x] `frontend/src/style.css` — readable fact hierarchy, long-name wrapping and both themes; keep navigation discoverable.
- [x] `frontend/tests/private-selected-activity.spec.ts` (new), `private-activity-helpers.ts` — synthetic real-API/rendered coverage for each matrix row; preserve helper defaults.
- [x] `frontend/tests/private-selection.spec.ts`, `private-day.spec.ts`, `private-start.spec.ts`, `private-identity.spec.ts` — retain regressions.
- [x] `docs/evidence/11-2-selected-activity.md` (new), `docs/development-log.md`, `README.md`, sprint/spec — record actual results, failures, limitations and acceptance separately.

**Acceptance criteria:**
- Given a confirmed selection, when opened/reloaded or navigated, then exact member facts and both planned instants match the server snapshot, including midnight and grouped pauses.
- Given missing or corrected facts, when consulted, then unknown/current/historical information remains distinguishable without fabricated stops or inherited places.
- Given unstarted/started or unresolved/denied state, when consulting, then existing start and recovery semantics persist without extra writes or stale disclosure.
- Given Day/Night, keyboard, long names and 200% enlargement at 768/1024/1440px, when consulted/navigated, then essential facts/controls remain visible, wrap without overflow and meet IR-01.
- Given an uploaded synthetic document, when editing/confirming/opening day/choosing an activity/returning, then only the intended screen is visible, corrections and registered bus/start/selection survive, navigation alone creates no start/outcome, and reload reopens authorized saved data.
- Given unsaved draft/time input or unresolved selection/start/bus response, when moving between screens, then input/recovery remains available and stale or unauthorized content cannot reappear.

## Implementation Notes

Owner explicitly authorizes the integrated navigation change, implementation, tests and routine fixes without another specification approval, overriding generic size/approval checkpoints. Existing dirty files are exactly this draft and the development log; preserve both. This is one selected-activity consultation goal with necessary flow separation. Root owns independent BMAD review, final sequential verification, evidence and handoff; implementation worker runs focused tests and restores services before returning. All automation uses disposable synthetic accounts only; preserve ordinary data, sessions, secret and volumes. No staging, commit, push, next story or time estimate. End in review for owner testing, not done. Keep approved intent unchanged during implementation; improvements within the specified UX are authorized.

Implemented mounted transient screens, compact signed-in/consultation chrome and read-only detail. `frontend/tests/private-screen-helpers.ts` adds explicit visible screen transitions for existing tests; historical evidence is preserved with separately named 11.2 outputs. Root's pre-review checks found and corrected terminal draft recovery, selection/bus aggregate-lock and late import/parent-read navigation races, and verified both normal and enlarged viewport composition. Final selected suite: 20 passed; bounded legacy samples: 12 passed; full reviewed gate is pending. No backend/API/schema changes. Ordinary-state comparison preserves every monitored digest except exactly three expired throttle rows removed by unchanged startup cleanup; subsequent comparisons must equal the restored post-worker baseline.

## Spec Change Log

## Review Triage Log

All three context-free BMAD layers completed before triage; instruction ACL failures were retried with approved read-only escalation before the actual edge/verification reviews. Blind floor: 10; edge: 3; verification: 1. Each candidate is adjudicated below. No owner intent gap or public API change is needed.

| ID | Verdict / route | Evidence and disposition |
|---|---|---|
| B1 | medium / patch | Back leaves requestedOpen true during a held next/previous save; acknowledgement overrides explicit return. Clear navigation intent on Back and cover held reply. |
| B2 | medium / patch | activityOpen makes every message change focus status, including loading/recovery; success can also steal a concurrent bus editor's focus. Restrict focus to intentional entry/completion without disturbing another active controller. |
| B3 | low / patch | A long day offers no read-only open at its current selected row, forcing a return to the top. Add a clearly distinct Open action at that row, with no selection write; retain the selected/disabled selection cue. |
| B4 | low / patch | Forced day-heading focus scrolls a long day away from its selected member after consultation. Restore meaningful focus at that member's read-only Open action, opening its pause disclosure if necessary; retain heading focus for first day entry. |
| B5 | high / patch | Retaining an old plan exposed the original single-deadline arbitration: plan expiry can clear a different pending confirmation/review and its operation identity. Independently expire retained plan and review/confirmation. |
| B6 | medium / patch | New detail time assertions use the same formatter as production. Add independent literal Oslo start/end calendar expectations, including midnight and an offset transition. |
| B7 | maybe-false (low if true) / reject | No narrow reflow defect is demonstrated; new grid uses min(100%, 15rem), min-width:0 and anywhere wrapping. The requested primary device coverage is tablet/PC. Extra phone qualification is not justified by a hypothetical low-impact gap. |
| B8 | low / patch | Enlarged visual cases use 1100px height; actual landscape is tested only at normal text. Exercise enlarged 1024×768 and assert scrolling reaches long facts and controls. Browser chrome zoom is distinct from CSS text enlargement; do not claim it was run. |
| B9 | medium / patch | Delayed parent denial has an ordinary reachable trap (E3); successful-reply tests do not cover it. Add delayed denial/failure after screen navigation, preserving input, screen and actionable recovery. |
| B10 | false / reject | Evidence explicitly labels full verification pending and intermediate failures as failures; it makes no final verified claim. Complete final gate and replace pending wording during the already-required documentation task. |
| E1 | high / patch | Same demonstrated deadline defect as B5. Retained plan and pending confirmation must retain independent expiry and recovery. |
| E2 | medium / patch | Same held acknowledgement/Back defect as B1; the explicit Back action must revoke auto-open intent. |
| E3 | high / patch | A held reopen 404 can clear the displayed plan after entering its retained detail, leaving activityOpen/consulting true and global navigation hidden. Clear orphaned detail mode and return to reachable preparation when the displayed plan disappears. Preserve different open plans and editor navigation. |
| G1 | medium / patch | Pre-verified missing coverage: passenger unknown line/trip/direction rows could disappear while current tests pass. Add an acknowledged missing-passenger-identifiers detail case. |

Shared-root patch groups: B1/E2; B5/E1; E3/B9. Remaining retained candidates are direct presentation/focus/test corrections. No finding is deferred; B7/B10 are rejected with the evidence above. Full reviewed regression gate remains outstanding.

All retained patches are applied. The changed selected suite passed 27 cases (1.7m); original blind/edge/verification reviewers re-inspected the fixes with no concrete remaining defect in those scopes. The passenger-identifier mutation now fails three explicit unknown-row assertions. Old-plan expiry, explicit Back and late denial paths are independently covered. Refined deterministic acknowledgement/failure observations are rerun before the final complete gate; no approval or intent change is inferred.

Root's first complete gate passed 302 API tests, exact restart/migration/state equality and build, then failed the browser gate: 272 passed / 12 failed. Retain the failed log and archived contexts. R1 (medium / patch): splitting expiry omitted immediate busy/read invalidation for a held old-plan read; restore that release without discarding an unrelated pending confirmation. R2 (low / patch): ten legacy confirmation/draft/identity assertions need actual navigation to their now-separate visible screen; preserve their data/security assertions. R3 (low / patch): the prior group-toggle test closes a disclosure already expanded by intentional Back focus; ensure it is open before checking the actual member marker. Final full browser verification follows these bounded corrections. Backend/scripts remain unchanged, so the API/restart evidence remains applicable.

## Verification

Root verification is complete: **302 PostgreSQL/API tests passed (353.71s)**, exact populated restart/repeated-migration/state preservation, production build and **all 284 browser tests passed in one complete run (18.1m)**, one worker and no retries. Five isolated verifier controls passed (0.146s). The original whole-browser failure (272/12) remains retained; 13 affected cases then passed before the successful complete browser rerun. Backend/API/verifier code stayed unchanged, preserving the successful API/restart evidence.

Assert snapshot/selection/lifecycle/bus/deadline equality before/after consultation. Inspect new synthetic 11.2 renders; preserve historical images. Measure text ≥4.5:1, boundaries ≥3:1 and focus ≥2px perimeter/3:1. Actual iPad/Safari stays not run unless performed.

Every matrix/acceptance row has executed passing coverage, including full uploaded-document navigation, retained input/data/selection, literal midnight/offset dates, source distinctions, pending/denied/expired states, read-only Open, focus and 768/1024/1440 Day/Night/enlargement. Root inspected final normal landscape and enlarged renders; numeric measurements are retained in evidence. Actual iPad/Safari, hardware touch, assistive technology and browser chrome zoom remain not run.

Original monitored business/source/policy/selection/lifecycle/receipt/session/security/secret state and database identity are preserved. The only initial-baseline difference is three expired throttle rows removed by unchanged startup cleanup; all later snapshots match the restored post-worker baseline exactly. Ordinary API/database are healthy, disposable services stopped, frontend source unchanged during the final gate and served entry/assets byte-equal to the tested build. No historical evidence image changed. See [executed evidence and owner steps](../../docs/evidence/11-2-selected-activity.md).

Jonas explicitly accepted 11.2 on 2026-10-25, reporting that it works well and is much clearer. Specification and sprint story are done. This acceptance supersedes the earlier review stop. Jonas subsequently authorized commit/push on 2026-10-25; this supersedes the earlier publication stop for 11.2 only. Do not start the next story. Actual device checks are not inferred from acceptance.
