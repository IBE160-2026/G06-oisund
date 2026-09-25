---
status: approved
created: 2026-09-25
epic: E3
story: '3.4'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.3']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice adds automatic initial selection to the manual actual-trip path. It does not implement automatic later-trip transitions or stop progression.

### Story 3.4: Select the Initial Trip from Qualified Plan, Position and Time Evidence

As the driver,
I want the assistant to select the initial trip only when the confirmed plan, usable position and current time support one candidate,
So that starting is simple without a confident-looking guess when trips overlap or evidence is missing.

**Acceptance Criteria:**

**Given** an owned, unexpired confirmed own day with authority to start it and no active trip in its current tracking context,
**When** initial selection is evaluated,
**Then** consider the confirmed plan, qualified position and current time together, using the existing service-date/source identities and downloaded trip evidence,
**And** use actual 3.1 quality limits and the shared AD-9 state machine; nearby stops, line number or scheduled departure alone are insufficient,
**And** document/test the selection criteria and evidence that distinguish candidates rather than silently choosing the first or nearest result,
**And** exclude unconfirmed drafts, other plans and ineligible completed/aborted activities; an initial passenger-trip choice does not mark preceding non-passenger work performed.

**Given** the combined evidence supports exactly one eligible initial trip,
**When** automatic selection commits,
**Then** reuse Story 3.3's atomic selection/persistence path with automatic provenance, retaining the relevant minimal evidence basis and plan revision,
**And** show the actual selected route and destination/direction only after commit,
**And** selection itself does not prove stop arrival/passage or start fabricated progression,
**And** retain the manual correction path through Menu under 3.2; automatic selection requires no driver interaction while moving.

**Given** several candidates remain plausible, including overlapping lines or opposite directions at shared stops,
**When** initial selection is presented,
**Then** show distinguishable candidates with route, destination/direction, departure and applicable date context and require an explicit choice before starting the trip's driving view,
**And** use the shared movement permission for opening/committing the interactive choice; if locked, keep a concise unresolved status and visible Menu/reason rather than demanding interaction,
**And** test multiple candidates while choice is locked: show a simple explicit status that the active trip must be selected when controls become available; do not start an arbitrary trip's driving view or prompt the driver to resolve ambiguity while driving,
**And** record the chosen candidate as manual selection with the same pin/provenance as 3.3; cancelling leaves no falsely selected trip.

**Given** no supported candidate, missing/stale position, insufficient trip data or an untrustworthy time basis,
**When** initial matching cannot establish a supported unique trip,
**Then** explain the limitation distinctly from a multiple-candidate result and offer direct selection from the confirmed plan under 3.3/3.2,
**And** do not substitute timetable-only certainty, simulated location or a source journey outside the confirmed plan,
**And** missing stops retain the approved recovery/missing-list handling and do not prevent permitted manual selection,
**And** retained observations do not become fresh when reopening, and connectivity alone does not establish position quality.

**Given** Friday service time 25:30 or a delayed initial trip near another scheduled departure,
**When** the candidate set is evaluated,
**Then** preserve Friday service identity and Saturday 01:30 calendar representation with the confirmed working-day order,
**And** test multiple similarly timed trips and shared-stop directions against checked expected candidates,
**And** no simplistic closest-departure or proximity rule may silently discard a plausible delayed trip; unresolved evidence requires choice.

**Given** a trip has already been selected automatically or manually,
**When** a new observation, scheduled departure, source refresh or initial-selection result arrives,
**Then** initial selection cannot replace that active trip; a delayed trip remains active until actual end or explicit permitted context change,
**And** manual correction stays authoritative and later-trip selection remains a separate state-machine transition, not a rerun of startup matching,
**And** reopening the existing context restores selection rather than treating it as an empty startup.

**Given** the candidate computation is pending while the plan, authority or selection context changes,
**When** it would commit or a displayed candidate is chosen,
**Then** revalidate owner/day/plan revision, current context, activity eligibility and evidence freshness at commit,
**And** a newer manual choice wins over stale automatic work; changed relevant inputs require reevaluation instead of silently using the stale result,
**And** double callbacks/retries cannot create duplicate selection events or overwrite committed state.

**Given** local selection and subsequent synchronization/reopen,
**When** storage fails, a server response is lost or a conflict occurs,
**Then** reuse 3.3's atomic state/event storage, authenticated PostgreSQL transaction, immutable retries and matching receipt rules,
**And** failed local commit does not display an active selection; server uncertainty remains distinct from locally committed selection,
**And** preserve the selected trip, provenance and movement history under existing access/logout/expiry rules with minimal evidence and no permanent raw GPS track,
**And** an expired ordinary login cannot authorize starting a prepared/new day through the existing-day continuation exception.

**Traceability:** FR-6 initial automatic/ambiguous/no-candidate selection, FR-3 missing-data fallback, FR-16 interactive choice and foundational FR-20 recovery; NFR-1/2/3; UX-DR5/10/13/14/16/38/44; AD-2/5 atomic state, AD-7 dated identity, AD-9 qualified observations/manual authority, AD-10/12 authority/retention.

**Dependencies:** Implemented 3.3 and its inherited 3.1/3.2/E2 foundations. Actual sensor/source qualification must support the selected criteria; negative findings require the established owner decision, not guessed reliability. No future stop-progression or automatic-transition story is needed to demonstrate initial choice and manual fallback.

**Implementation evidence:** Unique/multiple/no supported candidate; missing/stale position and incomplete data; overlapping 20/24 and opposite directions; Friday 25:30; delayed trip versus later departure; valid time/position separately insufficient; movement-locked choice; manual selection racing automatic result; changed plan, duplicate callback, failed local commit/lost receipt and reopen. Separate deterministic fixtures from actual target-device validation. Tests are planned, not run.

**Size boundary:** Initial trip selection only, reusing existing selector/display/persistence. No later-trip switching, full stop display, arrival/departure detection, interruption/skip actions, mentor context or new access-grant implementation.

**Pilot qualification:** Repeatable initial-selection scenarios support E8-D. Real target-device accuracy, mounted interaction and full progression/recovery integration remain E8-P requirements; E8-E remains subsequent field evaluation.

**Approval:** Approved by the owner on 2026-09-25 with a simple explicit waiting status when ambiguous candidates exist and movement rules lock selection. No arbitrary driving view or request to resolve ambiguity while driving. Planning approval only; the approved copy in epics.md is canonical.
