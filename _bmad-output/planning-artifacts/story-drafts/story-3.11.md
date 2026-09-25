---
status: approved
created: 2026-09-25
epic: E3
story: '3.11'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.10', '2.6']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice completes the approved missing-stop-list fallback: supported recovery first, then explicit manual trip completion/abort and next-activity selection. It does not end the combined day or fabricate final-stop evidence.

### Story 3.11: Resolve a Trip Without a Usable Stop List Manually

As the driver,
I want to complete or abort a trip and choose the next activity when its stops cannot be recovered,
So that missing source data does not trap the working day or create fictional GPS-confirmed progress.

**Acceptance Criteria:**

**Given** a selected confirmed trip lacks a usable stop sequence,
**When** the missing-data fallback is entered,
**Then** attempt supported timetable recovery for that exact trip/service date using the existing 2.6 adapter when the source is available, or supported locally available data when offline,
**And** distinguish source failure, successful no-match and an unusable returned list; neither similar route/time nor a different trip's list is a substitute,
**And** source failure or offline status cannot block an explicit permitted manual outcome; do not require a successful lookup or restored connectivity before completing/aborting manually,
**And** test failed source, offline with cached data and offline without usable cached data; preserve the manual outcome's origin and the underlying missing-data/observation uncertainty through synchronization and reopening.

**Given** no usable supported list is recovered,
**When** the trip remains active,
**Then** show Stoppinformasjon mangler with known route/destination/timing, preserving the selected trip and prior evidence,
**And** disable automatic stop progression and direct/arbitrary stop selection that lacks actual stop identities,
**And** offer clearly distinct manual complete-trip, abort-trip and next-activity paths through the movement-governed Menu; do not require a fictitious final stop to proceed.

**Given** the driver chooses manual completion or abortion,
**When** the action is explicitly confirmed for the displayed current trip,
**Then** atomically record the selected trip outcome, actual action timestamp and manual provenance before reporting success,
**And** completion is recorded as manually reported trip completion, never GPS-confirmed final arrival, an inferred stop visit or proof of the 100-m target,
**And** abortion remains distinct from completion and preserves any observed/uncertain earlier portion; no medical explanation is required,
**And** cancellation leaves the trip and its evidence unchanged.

**Given** a next-activity choice would leave the unresolved current trip,
**When** the driver selects the next confirmed activity,
**Then** require an explicit disposition of the current trip instead of silently marking it completed through selection; allow cancel/back without loss,
**And** retain confirmed activity order, parts and existing evidence, including non-passenger activities, without fabricating performed work for skipped-over entries,
**And** after manual completion/abort release only the resolved trip's active pin and establish the chosen context with its own identities/provenance,
**And** do not invent a Siste stopp arrival/timer or same-route-return GPS trigger in the absence of a known final-stop registration; this is an explicit manual missing-list transition.

**Given** any fallback action or next-activity selector,
**When** it opens or commits,
**Then** enforce the shared 3.2 permission, including reliable standstill and the labelled startup/five-minute unknown-speed exceptions,
**And** reliable motion locks these actions; the direct GPS-loss-arrow exception does not authorize arbitrary trip outcomes or next-activity selection,
**And** a permission change before commit prevents the uncommitted action, preserving the current trip with a clear reason and no demand to act while moving.

**Given** a recovery response, manual outcome or selection races with another context/plan change,
**When** it would apply,
**Then** validate owner/day/trip/context/revision and outcome state at commit,
**And** late source data cannot reopen or reclassify a manually completed/aborted trip, overwrite a newer choice or turn manual history into GPS evidence,
**And** if a valid list arrives while the trip is still unresolved/current, adopt it only under existing qualified identity/context checks; cancel or refresh stale fallback choices,
**And** retries/double taps of one action apply once, with no contradictory completed-and-aborted result.

**Given** the action commits locally, synchronizes or is reopened offline,
**When** storage or network faults occur,
**Then** reuse atomic state/event persistence and authenticated FastAPI/PostgreSQL ownership/writer/revision checks, immutable batches and matching receipts,
**And** failed local commit cannot show a successful outcome; lost server replies retain the local manual result and retry safely,
**And** preserve the missing-data reason, outcome provenance, earlier gaps, selected next activity and 3.2 movement history through reopening,
**And** apply access/logout/storage-error locks and AD-12 expiry to every copy without new retention periods or raw GPS logs.

**Given** no next confirmed activity or a combined-day gap/depot boundary,
**When** the manual trip is resolved,
**Then** show the appropriate no-next/gap/context state without automatically ending or aborting the whole workday,
**And** never restart a terminal/expired day; E7 retains the explicit final-day confirmation and summary review,
**And** any subsequent non-passenger outcome obeys approved 3.10: movement/location facts alone do not prove breaks, planned relocation, replacement or handover.

**Given** the fallback surface,
**When** used by touch, keyboard or enlarged text,
**Then** distinguish missing stops, manual completion, abortion, cancellation and next activity with clear labels, focus and restriction reasons,
**And** do not use color alone or hide the difference between ending a trip and ending the day.

**Traceability:** FR-3 missing-list recovery/manual fallback; bounded FR-11 interruption/next selection, FR-16, outcome evidence for FR-22 and foundational FR-20; NFR-2/3; UX-DR13/14/17/38/43/44; AD-2/5 persistence, AD-7 supported identity, AD-9 missing-list rules, AD-10/12 access/retention. E7 owns day ending/summary, other operational corrections remain later E3 work.

**Dependencies:** Implemented 3.10 and inherited selection/movement/persistence foundations, with 2.6 recovery. Uses the same operational state machine. No future summary/end/physical-bus feature is necessary to demonstrate the fallback and its retained manual evidence.

**Implementation evidence:** Missing list, same-trip recovery success, no-match versus failure, offline cache/no-cache, manual complete versus abort/cancel, next activity after explicit disposition, movement lock/unknown-speed exception and permission lost at commit, late recovery after manual outcome, double submission, failed write/lost receipt, reopen/gap/expiry. Fixtures and PostgreSQL integration verify behavior; actual-source/tablet evidence remains qualification. No tests run during drafting.

**Size boundary:** Selected trip without a usable list: supported recovery, manual outcome and next context. No fabricated final stop, general skipped-trip editor, physical replacement form, terminal workday flow or retrospective summary correction UI.

**Pilot qualification:** Repeatable failure/manual-fallback cases contribute to E8-D. E8-P requires actual source failure, mounted-device permissions and integrated offline/summary behavior before real shifts; E8-E remains separate evaluation.

**Approval:** Approved by the owner on 2026-09-25: recovery is attempted when the source is available, but source failure/offline status cannot block an explicit manual outcome. Manual origin and underlying uncertainty persist. Planning approval only; the approved copy in epics.md is canonical.
