---
status: approved
created: 2026-09-25
epic: E3
story: '3.13'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.12', '2.7']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice records manual physical bus replacement, including fault-related replacement, separately from correction of an entered bus number. It reuses existing assignment, operational controls and persistence; no fleet system or physical verification is introduced.

### Story 3.13: Record a Physical Bus Replacement Without Changing Trip Context

As the driver,
I want to record the actual replacement bus or correct an incorrectly entered bus number,
So that the working day retains the correct physical assignment and a truthful history without changing the trip I am following.

**Acceptance Criteria:**

**Given** an owned, unexpired active own day,
**When** the driver opens the operational bus action through Menu,
**Then** show the current physical bus number or explicit unknown status and allow manual entry of the replacement number,
**And** distinguish reported physical replacement, including fault-related replacement, from correction of a mistaken number,
**And** never populate physical bus from Vogn, route, trip identity or a source-file revision; do not require a fleet-system lookup.

**Given** a replacement or number correction has been reviewed,
**When** the driver explicitly confirms it,
**Then** atomically update the current physical assignment and record old/new known values, action type, registration time and manual provenance,
**And** retain unknown prior values as unknown; do not backdate the physical change from schedule or sensor data,
**And** a number correction does not assert a physical replacement occurred, while a replacement is explicitly a driver's report rather than independently verified handover/inspection,
**And** cancellation preserves the current assignment and failed local commit cannot show a successful change.

**Given** a physical bus replacement is registered after it occurred,
**When** the driver supplies its reported occurrence time or leaves that time unknown,
**Then** store/display the reported replacement time separately from registration time and server receipt time, retaining its manual provenance and applicable date/timezone,
**And** unknown actual replacement time remains unknown; registration time is not substituted as actual occurrence time,
**And** do not guess a historical assignment boundary or silently reassign earlier observations to another bus; preserve original observation associations and uncertainty,
**And** test known/unknown occurrence time, an overnight reported time, delayed synchronization and reopening, with no rewritten earlier observations.

**Given** the reported replacement occurs during an unfinished trip,
**When** the bus assignment changes,
**Then** preserve active trip/context, manual pin, stop progress, observed portions, gaps and prior corrections,
**And** do not automatically interrupt, complete or skip that trip or select a new route,
**And** any necessary interruption/next-activity choice remains an explicit separate action under 3.12.

**Given** a planned Bussbytte activity, vehicle-duty change or plausible position/time observations,
**When** the display advances or data refreshes,
**Then** do not change actual physical bus or mark replacement/handover performed automatically,
**And** preserve the distinction between the planned activity, the current assignment and an explicit manual replacement report,
**And** the report provides manual evidence only for the reported replacement; it does not verify associated inspection, handover, break or other activity outcomes, nor automatically settle an ambiguous planned-activity match.

**Given** the replacement/number-correction form,
**When** it opens and commits,
**Then** use 3.2's shared movement permission, including reliable standstill and labelled startup/five-minute unknown-speed exceptions,
**And** reliable motion locks the action; the direct GPS-loss-arrow exception does not authorize bus replacement,
**And** losing permission before commit prevents the uncommitted change without losing permitted saved work or prompting the moving driver to finish it.

**Given** invalid/missing entry, unchanged number or a stale form,
**When** confirmation is attempted,
**Then** show clear validation instead of inventing a number or silently treating an unchanged assignment as a verified replacement,
**And** preserve meaningful identifier formatting rather than assuming every bus number is a numeric quantity,
**And** if the assignment/day/context changed since review, require renewed review before applying a conflicting edit,
**And** repeated callbacks/retries of the same action cannot create duplicate replacement reports.

**Given** the app is offline or a server response is lost,
**When** the driver records an authorized replacement/correction and later reopens or reconnects,
**Then** retain the locally committed assignment/report with clear local/pending versus server-confirmed status,
**And** reuse authenticated FastAPI/PostgreSQL ownership/writer/revision checks, immutable event/batch retries and matching receipts; preserve permitted local work on conflict,
**And** preserve earlier reports and their manual origin rather than rewriting historical observations to use the new number,
**And** recovery keeps movement/outage history and does not turn stored position into a new observation.

**Given** logout, storage failure, expired or terminal day,
**When** the action or its delayed result is processed,
**Then** enforce existing access/storage locks and state/expiry validation; no delayed response revives a day or alters another owner's assignment,
**And** private assignment/correction/event/receipt copies follow the existing AD-12 deadline with no new clock, permanent vehicle history or raw GPS archive.

**Given** the bus-change surface and persisted report,
**When** viewed with touch, keyboard or enlarged text,
**Then** show explicit physical-bus labels, before/after values, action type, errors and selected/disabled state without color-only distinctions,
**And** retain clear separation from trip interruption and whole-day ending; provide evidence for E7 without requiring a summary UI to demonstrate this story.

**Traceability:** FR-5 physical assignment/correction, FR-11 fault-related replacement, FR-16, evidence for FR-22 and foundational FR-20; NFR-2/3; UX-DR6/13/14/17/38; AD-2/5 persistence/provenance, AD-9 context preservation, AD-10/12 authority/privacy. Preserves the owner's approved 3.10 distinction between location/time and physical outcomes.

**Dependencies:** Implemented 3.12 operational-control foundation and 2.7 physical-assignment field, with inherited movement/access/persistence. No external fleet service, later summary screen or new sensor rules are required.

**Implementation evidence:** Known/unknown previous bus, fault-related replacement, typo correction distinct from replacement, cancellation/invalid/unchanged entry, active trip/pin/progress unchanged, planned Bussbytte and source refresh without automatic physical update, permission loss, stale assignment, duplicate request, failed write/lost receipt, offline reopen and expiry. PostgreSQL integration verifies transaction/receipt behavior; tests are planned, not run.

**Size boundary:** Current own-day physical bus and its minimal manual correction/replacement evidence. No fleet inventory, fault-diagnosis workflow, maintenance reporting, handover certification, historical vehicle registry or automatic plan-outcome settlement.

**Pilot qualification:** Repeatable report/assignment behavior contributes to E8-D. E8-P requires mounted-device permissions and integrated offline/summary behavior. A driver report remains manual evidence, not independent verification; E8-E remains separate evaluation.

**Approval:** Approved by the owner on 2026-09-25 with reported replacement time distinct from registration time for late entry. Unknown actual change time remains unknown; earlier observations are never reassigned by guessing. Planning approval only; the approved copy in epics.md is canonical.
