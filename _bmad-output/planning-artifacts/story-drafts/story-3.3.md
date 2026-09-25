---
status: approved
created: 2026-09-25
epic: E3
story: '3.3'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.2', '2.6', '2.8']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice provides explicit selection/correction of the actual own passenger trip from a confirmed plan. Automatic initial selection is a subsequent slice that will reuse this committed selection path; automatic progression and completion remain separate.

### Story 3.3: Select and Preserve the Actual Trip from the Confirmed Plan

As the driver,
I want to select or correct the actual trip through Menu,
So that route and direction reflect the trip I am driving and remain authoritative despite delays or nearby services.

**Acceptance Criteria:**

**Given** an owned, unexpired confirmed own plan and ordinary application authority to start the day, or valid existing authority to continue it,
**When** the driver opens trip choice through the always-visible Menu,
**Then** show the eligible confirmed trips with route, destination/direction, departure and working-day order, distinguishing shared stops and overlapping lines,
**And** service-date/extended-time identity remains intact across midnight; similarly displayed times cannot collapse distinct trips,
**And** no unconfirmed draft, other plan or source suggestion becomes selectable as confirmed work,
**And** lack of an automatic candidate or unavailable position does not remove direct selection from the confirmed plan.

**Given** a trip choice is requested,
**When** the selector opens and a selection is committed,
**Then** use Story 3.2's shared movement permission at both points, with visible restriction reasons or labelled unknown-speed exceptions,
**And** preserve the current selection if cancelled or if permission is lost before commit,
**And** keep trip selection under Menu rather than adding a standalone driving-view correction button; assess the one/two-tap correction goal including the Menu tap, documenting cases where list size prevents it.

**Given** an eligible confirmed trip is explicitly chosen,
**When** local persistence succeeds,
**Then** atomically commit actual trip/tracking identity, manual selection provenance/pin and the event before rendering that trip as active,
**And** display its route and destination/direction prominently in a minimal active-trip view, with missing metadata visibly unknown and no personal import details,
**And** selection does not assert GPS location, stop arrival/passage, completion of the old trip or performance of the new trip,
**And** a failed local write leaves the prior committed selection authoritative and explains the failure.

**Given** a manually selected active trip,
**When** time advances, another trip's scheduled departure passes, nearby routes are observed or timetable/plan data refreshes,
**Then** retain that trip and manual pin; those events cannot silently select a different trip,
**And** active-trip identity remains separate from vehicle duty and physical bus,
**And** the pin persists until an explicit permitted correction/context change or actual completion supplied by later progression stories; schedule alone never releases it.

**Given** a wrong selection is corrected through the permitted selector,
**When** the driver selects the intended trip or returns to the prior trip,
**Then** record the explicit change and preserve prior observed/manual evidence without declaring an unfinished trip complete or aborted,
**And** do not copy the former trip's stop index or progress into the newly selected trip; use only applicable retained evidence with its uncertainty,
**And** show the resulting route/direction immediately after the atomic commit, retaining an accessible selected-state indication.

**Given** the selected confirmed trip lacks a usable stop list,
**When** supported same-trip/service-date recovery is available under Story 2.6,
**Then** attempt that recovery without substituting another trip; failure retains known facts and Stoppinformasjon mangler,
**And** selection remains possible but automatic stop progression is unavailable and no fictitious final stop or GPS evidence is created,
**And** offline use relies only on downloaded facts; the later manual completion/abort/next-activity fallback remains required and is not falsely presented as implemented here.

**Given** the plan/selection changes while a choice or recovery request is pending,
**When** its result would be applied,
**Then** validate the current owner/day/plan revision, target activity and selection context,
**And** reject stale results that would overwrite a newer manual selection or select a removed/ineligible activity, preserving the committed context and prompting a fresh choice where needed.

**Given** local selection, synchronization and reopen,
**When** recovery reads committed state or the backend accepts its batch,
**Then** preserve the actual trip/pin, provenance and movement-history state without reimport or a fresh startup exception,
**And** use authenticated FastAPI/PostgreSQL validation and atomic event/receipt handling; only a matching valid receipt marks server confirmation and lost responses retry unchanged batches,
**And** conflicts preserve permitted local work without silent overwrite; ownership, pending logout and AD-12 expiry apply to all introduced state/events,
**And** never start a new/prepared day after ordinary access expires by treating a continuation grant as general access. Full E5 continuation/boot qualification remains separate.

**Traceability:** Manual-selection/correction portions of FR-6/11, FR-3 missing-stop selection, FR-16, foundational FR-20; NFR-1/2/3; UX-DR10/13/14/16/38; AD-2/4/5 atomic persistence, AD-7 qualified identity, AD-9 manual authority/context, AD-10/12 access/retention. No claim of automatic initial selection, completed FR-7/8 progression or full FR-20 recovery.

**Dependencies:** Implemented 3.2 shared permission with actual 3.1 qualification, plus E2 confirmed plan/matching/download foundations. The manual path is independently demonstrable before automatic selection and progression. E1 ordinary authority supports demonstration; no new active-day exception is invented to bypass E5's remaining implementation.

**Implementation evidence:** Distinguishable 20/24 overlap and opposite directions, Friday 25:30, no position/no automatic candidate, missing stops, permitted versus locked selection, permission lost at commit, cancellation, wrong-trip correction/return, delayed active trip past another departure, stale recovery response, local write/receipt faults and reopen preserving pin/outage history. Use real PostgreSQL integration and labelled synthetic observations; tests are planned, not run.

**Size boundary:** Manual actual-trip selection and correction with minimal route/destination display, persistence and protected context. Automatic initial matching, full three-stop presentation, progression/final-stop transitions, interruption/skip controls and mentor contexts remain later stories.

**Pilot qualification:** Repeatable manual selection supports E8-D. E8-P requires mounted-device interaction, integrated progression/fallback and complete authority/offline recovery before actual shifts. E8-E remains separate evaluation.

**Approval:** Approved by the owner on 2026-09-25 with the described result, scope and acceptance criteria. Planning approval only; the approved copy in epics.md is canonical.
