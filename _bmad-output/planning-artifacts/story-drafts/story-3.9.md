---
status: approved
created: 2026-09-25
epic: E3
story: '3.9'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.8']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice completes a non-aborted passenger trip at registered final-stop arrival and implements the ordinary ten-second last-stop state and the distinct same-route-return trigger. Detailed non-passenger screens/completion, missing-list outcome controls and final workday ending remain separate required slices.

### Story 3.9: Register Final-Stop Arrival and Apply the Correct Next-Activity Trigger

As the driver,
I want final-stop arrival and the transition to subsequent work to follow actual evidence or my explicit manual action,
So that the trip ends correctly without starting a return trip from schedule or arrival alone.

**Acceptance Criteria:**

**Given** a selected non-aborted passenger trip with a known final-stop occurrence,
**When** qualified observations establish final-stop arrival or a permitted explicit manual stop action registers arrival there,
**Then** atomically record passenger-trip completion with trip/stop occurrence, actual registration time and observed or manual provenance,
**And** preserve manual origin without claiming GPS confirmation; a manually registered final arrival counts as completion under the approved rule,
**And** scheduled end, mere proximity, a missing stop list or an ambiguous occurrence cannot establish final arrival,
**And** repeated callbacks/retries record completion only once; an aborted trip is not silently relabelled completed.

**Given** registered final-stop arrival and a next confirmed activity that is not the special same-route return,
**When** the completion commits,
**Then** show Siste stopp for ten seconds for both observed and manual arrival, retaining completed trip identity and the next activity context,
**And** after that interval select the next activity according to the confirmed ordered plan; do not skip a break, transfer, bus change or other non-passenger entry to reach a later passenger trip,
**And** the selected next activity appears with its known type/timing/location and honest unknowns; this transition does not certify that a physical handover, break or travel has occurred,
**And** schedule alone cannot trigger this transition before registered completion. Detailed non-passenger layouts/evidence are a later slice, not an excuse to omit non-passenger entries here.

**Given** the next confirmed activity is an evidence-supported same-route return,
**When** final-stop arrival commits,
**Then** keep the last-stop state instead of starting the return after ten seconds,
**And** require a separate qualified detection of the return trip's starting-stop occurrence before automatic return activation,
**And** line number alone does not establish return identity; use the confirmed activity, direction/service-date and supported stop sequence,
**And** test co-located outbound-final/return-start stops: the original arrival event or its replay cannot simultaneously count as the separate return-start trigger; unresolved evidence keeps the waiting state.
**And** test sustained position while waiting, GPS jitter, scheduled departure and expiry of ten seconds at that shared stop: none can establish an independent return start; retain the waiting state until a separate qualified return-start registration exists,
**And** during qualified GPS loss require the separate intentional Next press after committed final arrival, never reuse the arrival press or infer it from elapsed time.

**Given** qualified GPS loss under 3.1 and a manually registered or retained final-stop state with a supported same-route return,
**When** the driver intentionally presses Next once more after the final arrival has committed,
**Then** start that return trip through the explicit approved manual return action, with manual provenance and no fabricated GPS arrival,
**And** the press that first reaches/registers the final stop cannot also start the return,
**And** distinguish this terminal return action from 3.7's ordinary one-stop progression; no generic list wrap or multiple-stop jump is allowed,
**And** unknown speed alone or internet loss does not enable this GPS-loss action; the existing direct-control movement exception and access checks still apply.

**Given** a completion, a ten-second timer or a return-start event races with correction, plan revision or context change,
**When** the transition would commit,
**Then** revalidate the selected context, completion identity, current confirmed next activity and permission for any manual action,
**And** stale timers/events cannot replace a newer explicit selection or start an activity removed from the applicable plan,
**And** actual completion releases the completed trip's manual pin for the established next-activity flow, but never copies the old pin/progress to the new trip,
**And** preserve prior correction/completion evidence; permitted undo/correction remains through 3.3's selector rather than rewriting history silently.

**Given** the application reopens during Siste stopp or the same-route-return wait,
**When** compatible committed state is restored,
**Then** retain completion provenance and original transition timing; reopening cannot restart the ten seconds, duplicate completion or invent a return trigger,
**And** use trustworthy elapsed-time handling and current context checks; unresolved timing/evidence stays explicit rather than granting a guessed transition,
**And** restored position remains stale until qualified new evidence arrives, preserving movement/outage history.

**Given** the final-stop event follows recovery across an observation gap,
**When** completion and subsequent context are displayed/recorded,
**Then** retain the gap and earlier uncertain/manual evidence; final arrival does not backfill unobserved stop visits,
**And** do not claim the 100-m target was met for unobserved departures/passages,
**And** identify the actual final occurrence when the same stop appears several times in the selected trip.

**Given** no next confirmed activity, uncertain return identity or no known final stop,
**When** the boundary is evaluated,
**Then** show a clear no-next/uncertain/missing-data state as applicable without inventing a trip or final-stop identifier,
**And** do not automatically end the combined workday, start its completed-day deletion clock or resume a terminal day,
**And** missing-list manual completion/abort/next selection and E7's explicit day end remain required separate functions.

**Given** completion or next-context changes are persisted and synchronized,
**When** local writes or backend transport fail,
**Then** use atomic state/event writes before showing success, stable transition identities and authenticated FastAPI/PostgreSQL receipt/revision handling,
**And** lost replies retry immutable batches and only a valid matching receipt marks server confirmation; partial writes cannot leave a completed trip with a contradictory active context,
**And** preserve permitted local facts on conflicts and apply ownership, pending logout, AD-10 authority and AD-12 retention to all copies,
**And** passenger completion or timer progress does not renew authority/retention or store a permanent GPS trace.

**Given** last-stop/waiting/next-context presentation,
**When** shown with touch, keyboard or enlarged text,
**Then** retain route/direction, clock, Menu and movement reasons, with explicit manual/uncertain status and accessible labels,
**And** make a committed context change evident without a blocking prompt while moving; notice presentation must later coexist without altering transition timing.

**Traceability:** FR-10 terminal/return transition, FR-6/11 selected-trip correction boundaries, passenger completion evidence for FR-22; NFR-1/2/3; UX-DR12/14/15/16/18/38; AD-2/5 atomic evidence, AD-9 final-stop/manual/return invariants, AD-10/12 authority/retention. Detailed non-passenger completion and E7 workday end/summary remain separate.

**Dependencies:** Implemented 3.8 and inherited 3.1–3.7 qualified observation, manual controls, selection, view and persistence foundations. E2 supplies confirmed next-activity order. Passenger completion, timer, minimal next-context presentation and return activation can be demonstrated without future non-passenger or summary stories.

**Implementation evidence:** Observed/manual final arrival, duplicate events, aborted-trip rejection, ordinary ten-second transition, intervening non-passenger entry, no next activity, same-route wait beyond ten seconds, qualified separate start detection, co-located/repeated stops, two distinct manual actions at the terminal, speed-only/network-only failures, stale timer versus manual correction/plan change, observation-gap preservation, reopen/time/storage/receipt faults. Tests are planned, not run.

**Size boundary:** Passenger final arrival/completion and next-context trigger with minimal display. No new source/progression engine, full non-passenger screen suite, inferred physical completion, missing-list outcomes, mentor handovers or terminal workday closure.

**Pilot qualification:** Repeatable transition evidence contributes to E8-D. E8-P requires target-device terminal/return behavior and integration with later non-passenger, offline recovery and summary flows; uncertain real-world return detection remains an explicit qualification gap. E8-E remains separate field evaluation.

**Approval:** Approved by the owner on 2026-09-25 with arrival/waiting distinguished from independent return-start registration at co-located final/start stops. Sustained position, GPS noise, schedule or ten-second expiry cannot start the return; qualified GPS loss requires a separate Next press after registered final arrival. Planning approval only; the approved copy in epics.md is canonical.
