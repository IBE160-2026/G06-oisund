---
status: approved
created: 2026-09-25
epic: E3
story: '3.12'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.11', '3.3']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice extends the shared trip-outcome/selection path to deliberate interruption and explicit skipped-trip recording in the confirmed own plan, including when stop data is available. Physical bus replacement and final workday end remain separate actions/stories.

### Story 3.12: Record Interrupted or Skipped Trips and Continue with the Intended Activity

As the driver,
I want to explicitly record a trip as interrupted or skipped and select the intended next activity,
So that operational changes do not falsely count as completed work or erase what was actually observed.

**Acceptance Criteria:**

**Given** an owned, unexpired active own day with a confirmed plan,
**When** the driver opens operational changes through Menu,
**Then** distinguish interruption of the current trip, an explicitly skipped trip and selection/correction of tracking context,
**And** show the affected trip's route, direction, departure and service-date context before confirming an outcome,
**And** ordinary correction of an erroneous selection under 3.3 does not automatically assert interruption or skipping; it remains distinct from declaring work not performed.

**Given** the driver explicitly confirms interruption of the current nonterminal trip,
**When** the action commits,
**Then** record a manual interrupted/aborted trip outcome with actual action time and preserve observed portions, corrections and uncertainty,
**And** do not invent final-stop arrival, convert it to completed or erase earlier evidence,
**And** release that trip's active pin only as part of the committed explicit context exit, with no pin/progress inherited by another trip,
**And** cancellation leaves the active context/outcome intact and no medical details are required.

**Given** an eligible confirmed trip that was not performed,
**When** the driver explicitly confirms it as skipped,
**Then** record skipped as a distinct manual outcome rather than completed or interrupted-after-observed-work,
**And** do not silently relabel an already completed trip or one with conflicting actual-performance evidence; preserve that evidence and explain the conflict,
**And** choosing a later trip, passage of scheduled time or absence from an imported update alone cannot mark intervening work skipped.

**Given** the driver chooses the intended next confirmed activity after an operational change,
**When** the choice commits,
**Then** preserve the original plan order and identities while establishing the explicit actual context with manual provenance,
**And** retain every intervening activity with its existing outcome; no bulk completion, skipping or deletion is inferred,
**And** include non-passenger activities without claiming that a break, planned relocation, physical replacement or handover occurred,
**And** trip interruption/skip never ends the combined workday, starts completed-day retention or resumes a terminal day.

**Given** a trip has usable stops, missing stops, or the app is offline,
**When** an authorized manual operational change is requested,
**Then** reuse the same outcome/state engine and 3.11 fallback conventions; no successful source call is required for an explicit manual action,
**And** preserve source/missing-data uncertainty and manual provenance after the action; stop-list availability does not change its origin,
**And** future source recovery cannot silently reclassify the outcome or manufacture observed completion.

**Given** interruption, skipped-trip recording or next-activity selection,
**When** the action opens and commits,
**Then** enforce 3.2's shared permission at both points, with visible reasons and labelled unknown-speed exceptions,
**And** reliable motion blocks these actions; direct GPS-loss arrow availability grants no permission to interrupt, skip or choose an arbitrary activity,
**And** loss of permission before commit cancels the uncommitted action without losing prior state or demanding a response while moving.

**Given** pending confirmation races with final arrival, another manual choice, plan revision or repeated callbacks,
**When** the action reaches the commit boundary,
**Then** revalidate owner/day/activity/context, applicable revision and current outcome,
**And** reject a stale incompatible proposal for renewed review rather than recording contradictory completed/interrupted/skipped outcomes,
**And** apply one intentional action once with stable event/batch identities; deliberate later correction preserves history instead of mutating an old submitted event.

**Given** local changes, synchronization and reopening,
**When** storage or transport fails,
**Then** atomically persist outcome/context and necessary events before showing success, using inherited authenticated FastAPI/PostgreSQL ownership/writer/revision checks and matching receipts,
**And** failed local writes leave prior state intact; lost responses retry immutable batches and do not duplicate outcomes,
**And** restore outcome provenance, observation gaps, actual selection and movement history, without refreshing stale position or resetting outage timers,
**And** enforce access/logout/storage locks and AD-12 expiry on all private copies; no permanent GPS trace or new retention clock is introduced.

**Given** the operational-change surface,
**When** operated by touch, keyboard or enlarged text,
**Then** clearly distinguish trip interruption, skipped work, tracking correction and whole-day ending with accessible labels, focus and cancel paths,
**And** retain the clock, context and movement reason; whole-day ending and physical bus replacement remain their own later actions, not disguised as interruption.

**Traceability:** FR-11 interruption/next selection and correction evidence, FR-6 explicit selection, FR-16, outcome evidence for FR-22 and foundational FR-20; NFR-2/3; UX-DR13/14/16/17/38; AD-2/5 atomic persistence, AD-9 context/provenance, AD-10/12 authority/retention. E7 consumes these facts without needing to exist for this story to work.

**Dependencies:** Implemented 3.11 outcome/fallback foundation and 3.3 selection with their inherited movement, progression and persistence prerequisites. No future bus-replacement, summary UI or final-day workflow is needed to demonstrate these operational changes.

**Implementation evidence:** Interruption with observed portion, explicitly skipped unperformed trip, wrong-selection correction without false outcome, jump to later activity preserving intervening entries, source/offline failures, permission loss, final-arrival/plan-change race, duplicate actions, failed write/lost receipt and reopen/expiry. Verify manual provenance and no contradictory outcomes with PostgreSQL integration. Tests are planned, not run.

**Size boundary:** Explicit trip interruption/skip and selected next context via existing engine. No general historical outcome editor, medical-reason collection, physical bus replacement, plan-file reconciliation, mentor handover, summary rendering or final day-end transaction.

**Pilot qualification:** Repeatable operational-change scenarios contribute to E8-D. E8-P requires mounted-device interaction and integration with full offline recovery, summary and end flows; E8-E remains separate actual-shift evaluation.

**Approval:** Approved by the owner on 2026-09-25 with the described scope, retaining the distinction between erroneous selection, interrupted trip and explicitly skipped trip, and preserving previous observations. Planning approval only; the approved copy in epics.md is canonical.
