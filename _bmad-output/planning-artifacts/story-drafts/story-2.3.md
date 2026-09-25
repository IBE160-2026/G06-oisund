---
status: approved
created: 2026-09-25
epic: E2
story: '2.3'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['1.1', '1.2', '1.3', '1.4']
---

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

This slice extends the protected minimal draft with direct manual trip/activity entry and correction. It works before OCR and timetable adapters are implemented; it is the shared correction foundation, not a substitute for required import or automatic source data. Final plan confirmation and active-day revision are separate later E2 slices.

### Story 2.3: Add and Correct Trips and Activities in an Unconfirmed Draft

As the pilot owner,
I want to add missing trips or activities and correct their fields directly,
So that incomplete or incorrect source interpretation need not become the plan I use for work.

**Acceptance Criteria:**

**Given** an owned, unexpired, unconfirmed draft and permitted application access,
**When** the owner adds a passenger trip,
**Then** the editor accepts route, starting stop, ending stop and departure using the draft's service-date context,
**And** the entry receives a stable activity identity and explicit manual provenance while retaining unknown/missing values as such,
**And** no timetable identity, stop list, direction or physical bus is invented; pending timetable completion is explicit and is not described as a successful no-match lookup.

**Given** the same draft,
**When** the owner adds a non-passenger activity,
**Then** the editor accepts type, start/end times and optional known location,
**And** unknown location or unexplained source classification remains unknown, Travel to retains its accepted bus-movement meaning and is not automatically pilot-car transfer,
**And** vehicle duty, physical bus, passenger trip and other activity identities remain distinct; this story does not infer completion or activate driving.

**Given** a Friday service date and an entered extended departure such as 25:30,
**When** the draft is saved and reopened,
**Then** preserve Friday service identity and 25:30 while deriving the corresponding Saturday 01:30 calendar representation in the applicable timezone,
**And** retain the activity's working-day order and distinguish it from another entry sharing that calendar display time,
**And** comparisons never merge activities solely by displayed time; date/time ambiguity or inconsistent end-before-start input prompts correction instead of an invented date rollover,
**And** checked tests cover midnight boundaries and duplicate Saturday 01:30 display times; timezone ambiguities remain explicit rather than guessing an instant.

**Given** a Friday-service draft with an incorrectly entered departure, known neighboring activities and visibly unknown fields,
**When** the driver manually corrects the departure to Friday 25:30, saves, closes and reopens the draft,
**Then** Friday remains the service date, the retained extended time is 25:30 and any calendar-date presentation shows Saturday 01:30,
**And** the corrected activity retains its identity and the correct working-day position according to the checked expected sequence, rather than sorting 01:30 ahead of Friday evening activities,
**And** manual-correction provenance survives saving/reopening and another activity sharing Saturday 01:30 is not merged with it,
**And** unknown route, direction, location, identifiers or other absent facts remain visibly unknown; neither manual correction nor persistence fills them by guessing.

**Given** an existing draft activity,
**When** the owner edits fields or adds an omitted activity at a chosen position and saves,
**Then** the editor shows the resulting draft sequence and distinguishes manually corrected facts from retained source/unknown values,
**And** stable identities, source provenance where present and unaffected activities are preserved; no silent duplicate, reordering by clock time alone or deletion results,
**And** cancellation before save leaves the committed draft unchanged, and validation errors preserve entered values for correction without falsely reporting a saved change.

**Given** a valid draft edit,
**When** it is committed,
**Then** the next draft state and its new typed edit event are persisted atomically in IndexedDB before showing completion,
**And** sync extends Story 1.4's protected PostgreSQL transaction/receipt path for this event, using new event/batch identities rather than changing an already submitted batch's payload,
**And** local save remains distinct from server confirmation; only a valid matching receipt acknowledges the change,
**And** a failed local/server transaction, response-loss retry or revision conflict cannot partially apply the edit, lose pending work or overwrite conflicting state automatically.

**Given** a saved draft with activities and corrections,
**When** it is reopened or synchronized after interruption,
**Then** restore its committed activity identities, order, both time representations, manual provenance and pending event state,
**And** Stories 1.1–1.4 still enforce owner-only access, durable logout/revocation ordering and failure-safe locking against actual activity payloads,
**And** draft edits, reopening and synchronization do not reset the original AD-12 expiry; every newly introduced activity/event/receipt copy shares the applicable deletion boundary,
**And** late results cannot expose locked data or resurrect expired draft content.

**Given** the review editor on the preparation surface,
**When** the owner enters/corrects activities by touch or keyboard and enlarges text,
**Then** field labels, error associations, focus order and save/cancel states are clear and use the approved preparation tokens,
**And** the service date, activity order, unknown values and unsynchronized status remain visible without color-only meaning,
**And** no precise gesture, free-text AI correction or GPS permission is required.

**Given** a successfully saved or server-acknowledged edited draft,
**When** its state is displayed,
**Then** it remains explicitly unconfirmed and cannot start an active trip,
**And** neither draft save nor server acknowledgement is presented as the driver's final plan confirmation,
**And** any later import/matching result must enter the shared review process without silently replacing manual corrections.

**Traceability:** FR-2 manual correction/omitted activities; FR-3 known passenger fields, FR-4 non-passenger fields, FR-5 identity distinctions; NFR-2/3; UX-DR2/4/5/38/42/43; AD-2/5 atomic changes and immutable events, AD-6 resumable editable drafts, AD-10/12 access/retention. The owner's approved Story 2.2 time-representation clarification is preserved. AD-7 matching remains a later implementation concern, not claimed by manual entry.

**Dependencies:** Approved E1 Stories 1.1–1.4. Add only draft activity/edit fields and persistence needed here, extending the existing contracts instead of a second editor or sync engine. Reports from 2.1/2.2 inform later adapters but their successful completion is not required to manually enter known facts. Actual Entur field semantics must be qualified before implementing source matching; this story does not invent them.

**Implementation evidence:** Add/edit/cancel/reopen browser scenarios for passenger/non-passenger/unknown fields; checked extended-time and duplicate-display-time cases; atomic local write failure and PostgreSQL rollback, immutable retry and revision conflict; logout/expiry with pending edits and owner isolation; keyboard/text-enlargement checks. Use fictional fixtures. These checks are planned, not executed here.

**Size boundary:** Direct editing of an unconfirmed draft only. No file extraction, live timetable retrieval, driver confirmation into a plan, active-day scoped revision, mentor linking, stop progression or activity completion. Those remain required later stories. No change to approved V1 scope or architecture.

**Pilot qualification:** Contributes repeatable editor/data-integrity evidence to E8-D; real OCR, source matching, mounted usability and complete preparation/offline integration remain E8-P. It is not a substitute for qualification or the three-day E8-E evaluation. No implementation/readiness workflow is started by this draft.

**Approval:** Approved by the owner on 2026-09-25 with an explicit manual cross-midnight correction/save/reopen test: Friday 25:30 retains Friday service identity, displays Saturday 01:30 where calendar representation is used and stays in the correct working-day position. Unknown facts remain visibly unknown, never guessed. Approval is planning only; the approved copy in epics.md is canonical.
