---
status: approved
created: 2026-09-26
epic: E6
story: '6.3'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['6.1', '6.2', '3.2', '5.13']
---

### Story 6.3: Explicitly Link a Planned Accompaniment Activity to the Reviewed Person and Shift Scope

As the pilot owner preparing FADDER or INSTRUKTØR work,
I want to review and confirm which person-plan and portion each own accompaniment activity refers to,
So that the intended accompaniment is clear without silently selecting a person, starting guidance or changing planned trip ownership.

**Acceptance Criteria:**

**Given** an accessible unexpired own day, its confirmed mentor assignment and separately reviewed person-plan copies from 6.2,
**When** the owner prepares a link for an own accompaniment activity,
**Then** show the own activity/assignment, intended person, imported plan and its revision in separate clearly labelled contexts, including service date, relevant times and the proposed scope,
**And** require explicit selection and review rather than choosing by matching name, line, departure time, current position or scheduled boundary,
**And** preserve stable owner/day/activity/person/plan identities and the own and imported plan revisions used for the comparison; a reused person-plan remains the same private copy while each distinct accompaniment block has its own identity,
**And** describe imported-plan confirmation as the mentor's review of their copy, never the accompanied person's approval or a live link to their account,
**And** do not offer classroom/office or planned own-driving trips as accompaniment activities, and do not turn imported trips into own planned driving.

**Given** the selected own assignment is FADDER,
**When** the owner reviews its proposed accompaniment link,
**Then** require one same person's whole shift during that fadder assignment, displaying the linked shift's known boundaries and work parts rather than silently narrowing the link to one convenient trip,
**And** disallow another person or an instructor-style partial scope within that fadder assignment; explain the unresolved mismatch without changing the assignment type automatically,
**And** if a known missing section, ambiguous shift boundary or conflict with the own assignment prevents establishing whole-shift scope, keep the link visibly unresolved for correction instead of claiming the whole shift is linked,
**And** distinguish completeness of the reviewed plan scope from availability of source matches or downloadable stop data: a missing route match alone does not prove that the plan scope is partial, and whole-shift linking does not certify source/data completeness.

**Given** the selected own assignment is INSTRUKTØR,
**When** the owner defines planned accompaniment scope,
**Then** support one trip, part of a day or a shorter/longer interval within the selected reviewed plan, with explicit boundaries sufficient to identify the intended portion,
**And** retain service date and calendar-date translation across midnight; a time-only label or repeated stop name cannot identify a unique trip/activity/stop occurrence where several exist,
**And** allow separate blocks for different people and a later return to an already reviewed person-plan, without merging the blocks or copying completion, manual pin or actual accompaniment evidence between them,
**And** preserve intervening classroom/office/own-driving activities in the own sequence; a valid no-accompaniment instructor day requires no artificial block or person,
**And** a selected interval is a planned boundary, not evidence that an entire boundary trip or activity was actually accompanied or completed.

**Given** proposed links have missing targets, ambiguous portions, overlaps or incompatible own/person-plan timing,
**When** the owner reviews or attempts to confirm the affected link,
**Then** identify the affected activity, person and boundary and retain the editable proposal with a clear unresolved status rather than choosing or truncating a scope automatically,
**And** require resolution of ambiguity that prevents identifying the intended person and portion; optional unknown location or missing stop/source data remains explicitly unknown without inventing a value,
**And** highlight competing/overlapping links and keep their ambiguity unresolved until explicit correction; never let a scheduled time select the actual person or grant guiding controls,
**And** cancellation preserves the previous confirmed link, own plan and imported copies. Planned-link changes cannot rewrite an already active tracking context or historical evidence; operational switching and affected-link repair are separate later slices.

**Given** the owner has reviewed an unambiguous proposed link against its exact own and imported plan revisions,
**When** the owner explicitly confirms the planned link,
**Then** atomically persist the block identity, person/plan/activity references, reviewed revisions, explicit scope and owner confirmation provenance with the required outbox event,
**And** if either reviewed revision, the target activity, scope or relevant authority changes before commitment, retain the proposal as stale/unresolved and require review again; do not silently rebase or retarget a similar trip,
**And** show planned-link confirmation separately from mentor-reviewed person-plan confirmation, data coverage, server receipt and actual accompaniment; partial downloaded coverage cannot become whole-day readiness,
**And** confirmation changes no actual driver/guiding role, active trip, manual pin, performed-work evidence or own-day lifecycle; clock passage, GPS proximity and reopening cannot turn the planned link into actual accompaniment,
**And** full linked-plan revision/repair UI is not required here, but consumers can detect stale references from the stored revision basis rather than silently treating them as current.

**Given** a planned link is reopened, synchronized or becomes subject to locking, closure or expiry,
**When** the client and backend recover or process it,
**Then** preserve the selected scope, identities, reviewed revisions, confirmation attribution and unresolved/pending statuses through the shared E5 persistence/recovery contracts,
**And** implement only necessary link fields/validation in owner/day-scoped IndexedDB and authenticated FastAPI/PostgreSQL; reject cross-owner/day, forged plan/activity relationships, invalid FADDER scope and stale writer/revision on the backend as well as the UI,
**And** local failure cannot report a saved link; only a matching receipt confirms server acceptance, with immutable retries and preserved proposals on conflict or unknown outcome,
**And** reuse the existing movement policy for preparation/editing and existing access, pending-revocation and fixed-expiry guards; a planned mentor link creates no unrestricted-control exception or new first-start/GPS-loss period,
**And** the link shares the own day's existing retention and closure rules and creates no separate clock from the other person's shift or a block ending. Planned-only linked context is removed through 5.13 at own-day closure when no actual accompaniment evidence exists; stale tabs, pending payloads and delayed replies cannot recreate it,
**And** private person/link information remains excluded from public demo access, logs and active-driving personal detail; no cross-account authority or permanent person history is added.

**Given** anonymized/fictional own and imported plans, browser clients and real PostgreSQL,
**When** this slice is verified,
**Then** test one whole-shift same-person FADDER link, rejected partial/person-switch FADDER scope, known incomplete imported shift and conflicting own assignment boundaries,
**And** test INSTRUKTØR with a single trip, a bounded interval, people A then B then A around classroom/office activities, and a valid day without accompaniment,
**And** test Friday 25:30 as Saturday 01:30, multiple trips sharing that display time, repeated stop occurrences, identical-looking trips in different plans, missing optional data, ambiguous boundaries and overlapping links,
**And** test stale own/imported revision during review, cancel, local failure, lost/mismatched receipt, forged scope/owner, logout, expiry, reload and terminal cleanup across concurrent tabs/delayed replies,
**And** verify that confirming/reopening a planned link or passing its scheduled boundary never selects the actual person/trip, unlocks guiding controls, completes work or inherits another block's pin/evidence.

**Traceability:** UX UJ-3/4 extensions of FR-2/4/5, FR-6 plan ownership/context boundary, shared FR-1/16/20/24 and future FR-22 evidence attribution. NFR-1–4; UX-DR5/7/8/26/27/28/30/36/38/39/44. EXPERIENCE FADDER and INSTRUKTØR assignment scope, Revision ownership and linked contexts and Explicit tracking-context changes; DESIGN separate own/linked panels. AD-2/4/5 atomic state and receipts, AD-6 reviewed copies, AD-9 planned versus actual role/context, AD-10/11 bounded access/writer authority and AD-12 retention. Operational portions of these requirements remain later E6 stories; no AD-1–AD-14 decision changes.

**Dependencies:** 6.1 own assignment, 6.2 separately mentor-reviewed person copies, existing E3 interaction policy and E1/E5 persistence/access/closure through 5.13. Stale-reference, active-context and terminal cleanup behavior can be verified with existing commands and fixtures, without a future operational mentor or summary screen.

**Size boundary:** One planned-link editor/review/confirmation path with FADDER/INSTRUKTØR scope validation, protected storage and recovery. No active accompaniment entry/exit, guiding controls, live trip/notice progression, own-driving/takeover transition, linked-revision repair UI or summary renderer. Those remain required later slices, not removed requirements.

**Pilot qualification:** Controlled linking/browser/FastAPI/PostgreSQL cases contribute to E8-D. E8-P still requires representative whole/partial shifts, device readability and integrated explicit operational context changes, recovery and closure. E8-E remains field evaluation; planned whole-shift scope cannot certify actual whole-shift accompaniment. No implementation or actual qualification tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 as scoped. Linking uses specific plan revisions and explicit scope; actual accompaniment still requires separate entry. Tests include incomplete FADDER shifts and INSTRUKTØR periods A to B and back to A. Planning approval only; the approved copy in epics.md is canonical.
