---
status: approved
created: 2026-09-25
epic: E3
story: '3.10'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.9', '2.9']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice renders and tracks own non-passenger activities using the confirmed combined-day order. It separates display transitions from evidence of completion; summary confirmation and final day ending remain E7.

### Story 3.10: Follow Non-Passenger Activities Without Inventing Completion

As the driver,
I want clear context for relocation, breaks, layover, bus changes, transfers and depot return,
So that I can follow the whole working day without treating a screen change or scheduled end as proof that work was performed.

**Acceptance Criteria:**

**Given** the next confirmed activity is not a passenger trip,
**When** 3.9's ordinary final-stop transition selects it,
**Then** render that activity rather than skipping ahead to a passenger trip, preserving known timing, location, part and provenance,
**And** retain the preceding Siste stopp period of ten seconds for observed and manual arrival; the same-route-return exception remains 3.9's separate behavior,
**And** display the next confirmed activity when known and explicit unknown/no-next status otherwise, with a persistent clock and movement-governed Menu.

**Given** relocation, meal or their supported combination,
**When** the activity view renders,
**Then** show Tomkjøring with the next starting-stop name for relocation, Matpause for a meal without relocation, and the adopted meal/Tomkjøring/first-stop-after-break composition for the combined case,
**And** preserve known paid/unpaid/unknown meal classification separately from the friendly label,
**And** never count relocation as break time, invent a meal location or infer employment/payment rules,
**And** unknown PDF codes retain their uncertainty; preserve the approved Travel to meaning when applicable rather than relabelling it as pilot-car transfer.

**Given** a planned bus change, pilot-car transfer, depot return or layover,
**When** the activity view renders,
**Then** use centered Bussbytte or Pilotbil, Returner til / Depot on two lines without the blue rail, or Reguleringstid with known timing and next activity, respectively,
**And** physical bus remains distinct from vehicle duty, and a planned change does not silently update the actual bus number or assert a handover occurred,
**And** no pilot-car number is required; unknown locations/times remain visible unknowns,
**And** unconfirmed dispatch changes remain unresolved until the E2 revision flow confirms them.

**Given** a non-passenger activity with known relevant location and timing,
**When** the shared state machine evaluates completion,
**Then** evaluate qualified position and timing together under documented activity-specific rules using 3.1 quality limits, distinguishing supported movement/location facts from the activity's actual outcome,
**And** scheduled end, entering the screen or reaching a location alone cannot certify completion,
**And** position and time alone cannot confirm that a break was taken, relocation was performed as planned, a bus was replaced or a handover occurred; retain Gjennomføring usikker unless evidence specific to that outcome exists,
**And** test all four cases with plausible position/time observations but no outcome-specific evidence: retain the movement/location facts and uncertainty without falsely marking the activity completed,
**And** if required position/location/timing evidence is missing or ambiguous, retain Gjennomføring usikker for later E7 manual summary confirmation rather than filling it in automatically.

**Given** the next activity becomes the displayed context while prior completion is uncertain,
**When** an explicit permitted context choice or supported normal transition advances the view,
**Then** preserve the earlier uncertain outcome and distinguish the context change from completion evidence,
**And** no timetable-driven display update may override an unfinished passenger trip or its manual pin,
**And** do not duplicate initial-trip selection or terminal logic; reuse the existing state-machine paths and 3.2 permissions for interactive actions.

**Given** a combined day contains an intermediate depot visit or a gap before a later work part,
**When** that interval is reached,
**Then** show the next part's reporting time and known depot with an explicit gap state,
**And** never infer rest, meal, transfer or day completion from the interval alone,
**And** keep one day identity and expiry basis; neither intermediate depot return nor arrival at final depot automatically ends the workday,
**And** supply final-depot context for E7's later explicit end/abort flow without claiming that action implemented here.

**Given** a pending observation/context update and a manual choice, plan revision or repeated callback,
**When** a transition or completion would commit,
**Then** validate current plan/activity/context identity and preserve performed evidence and corrections,
**And** reject stale work, apply a supported event once, and record no retroactive completion merely because an added activity's scheduled time has passed.

**Given** an activity state/outcome changes or is reopened offline,
**When** persistence and synchronization occur,
**Then** atomically save state and necessary event before showing success and retain manual/observed/uncertain distinctions after reopen,
**And** use inherited authenticated FastAPI/PostgreSQL ownership/revision validation, immutable retries and matching receipts; failed local writes cannot appear successful,
**And** downloaded plan facts remain usable without inventing missing source data or fresh position; preserve 3.2 movement/outage history,
**And** apply access/logout/storage-error locks and AD-12 expiry to all private copies; activity timing or reopen never renews authority or retention, and no raw GPS archive is introduced.

**Given** each activity composition,
**When** inspected on the target landscape layout, with long labels, keyboard and enlarged text,
**Then** maintain readable hierarchy, explicit activity/uncertainty labels, visible clock/Menu and accessible focus/disabled states,
**And** do not require precise gestures or a response while moving; sensor uncertainty does not silently open arbitrary controls.

**Traceability:** FR-4/5/10, non-passenger evidence for FR-22, foundational FR-17/20; NFR-1/2/3; UX-DR7/12/14/17/18/38/44; AD-2/5 committed evidence, AD-9 non-passenger position-plus-time rule, AD-10/12 authority/retention. Physical replacement correction, missing-list outcomes, E7 summary review and final ending retain separate ownership.

**Dependencies:** Implemented 3.9, E2 split-day model through 2.9 and inherited quality/movement/persistence foundations. E7 is not needed to demonstrate correct activity screens and retained uncertain outcomes; it later consumes that evidence for summary/manual confirmation.

**Implementation evidence:** Each adopted activity composition; relocation+meal versus meal only and unknown classification; missing location, stale position, timing-only and location-only cases; plausible position+timing without specific evidence for break/relocation/bus replacement/handover keeps each outcome uncertain; context change retaining uncertainty; split-day gap/different depots; intermediate/final depot without automatic ending; stale revision, failed write/lost receipt and offline reopen. Actual device tests must qualify activity-specific evidence rules; no tests run during drafting.

**Size boundary:** Existing confirmed own non-passenger activities, their display/context and supported/uncertain outcomes. No payroll/rest-rule engine, physical bus replacement form, new sensor engine, mentor classroom/office context, summary UI or day-end transaction.

**Pilot qualification:** Repeatable activity/display/evidence tests contribute to E8-D. E8-P requires mounted readability, actual position/timing behavior and integration with complete recovery/end/summary flows. Unprovable physical acts remain unverified; E8-E remains subsequent evaluation.

**Approval:** Approved by the owner on 2026-09-25 with position/time supporting movement/location only, not by themselves proof of a taken break, relocation performed as planned, bus replacement or handover. Those outcomes stay uncertain without their own evidence. This owner clarification governs interpretation of the completion criteria. Planning approval only; the approved copy in epics.md is canonical.
