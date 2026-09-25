---
status: approved
created: 2026-09-25
epic: E2
story: '2.6'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['2.2', '2.3']
---

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

This slice enriches a reviewed unconfirmed passenger-trip entry with evidence-supported timetable identity, ordered stops and planned times. It uses the same draft editor for manual or imported entries; no source-file import is required to demonstrate it. Whole-day preparation/readiness and final driver confirmation follow separately.

### Story 2.6: Match a Draft Trip to the Correct Dated Timetable Journey

As the pilot owner,
I want timetable details for my entered trip with explicit choice when matching is ambiguous,
So that the draft contains the correct journey and stops without silently substituting a similar service.

**Acceptance Criteria:**

**Given** a permitted, unexpired passenger-trip draft with route, endpoints, departure and service date,
**When** timetable completion is requested,
**Then** the backend transit adapter uses the targeted Entur query strategy qualified in Story 2.2 for pilot lines 20, 24, 28 and 42,
**And** it validates the request and uses the applicable service/calendar context, source-namespaced identifiers and direction evidence rather than line number or nearby stops alone,
**And** optimized journey suggestions or partial responses are not treated as an exhaustive catalogue; incomplete retrieval cannot establish a unique match or a definitive no-match result.

**Given** Friday service date and departure 25:30,
**When** lookup translates that entry to a calendar-date query/result presentation,
**Then** Saturday 01:30 is used where calendar representation is required while Friday service identity, extended departure and working-day sequence remain intact,
**And** actual Entur date fields and journey identifiers are interpreted according to Story 2.2's qualified evidence, never by assuming the displayed timestamp identifies a service day,
**And** several Saturday 01:30 candidates remain distinct; tests with checked expected facts cover correct unique resolution and unresolved temporal ambiguity.

**Given** complete applicable query evidence supports exactly one matching dated journey,
**When** timetable completion is applied,
**Then** the draft links to that source journey and retains its supported ordered stops and planned times with provenance,
**And** uniqueness is supported by source journey identity and the applicable service date; matching line number and clock time alone never establishes a unique dated journey,
**And** source facts remain distinguishable from manual corrections and observations; no stop arrival, departure or actual progress is asserted,
**And** any contradiction with manually corrected fields is shown for resolution rather than silently overwriting them,
**And** the draft remains unconfirmed and no active trip is started.

**Given** a manually corrected departure time or stop differs from the timetable source,
**When** a new or delayed matching response arrives and the draft is saved/reopened,
**Then** retain the driver's correction and its manual provenance, showing the source value and the discrepancy clearly alongside it,
**And** neither a fresh unique-match result nor a delayed response silently replaces that correction,
**And** if the correction invalidates the journey association, show it as unresolved for explicit review while preserving both the correction and source evidence,
**And** checked tests cover both a time discrepancy and a stop discrepancy, including a response requested before the correction and a new request made afterward.

**Given** multiple supported candidates or unresolved service-day/direction ambiguity,
**When** the owner opens the candidate selection,
**Then** each candidate exposes the known route, direction/destination, endpoints, calendar departure and available service-date/identity evidence in distinguishable form,
**And** the driver must explicitly select a candidate before its timetable details are linked; cancellation preserves the previous draft,
**And** unknown metadata remains unknown and a choice records manual origin rather than claiming the source proved uniqueness,
**And** candidate selection is not final confirmation of the working-day plan.

**Given** a successfully completed lookup has no supported match, or a supported match lacks a usable stop sequence,
**When** the outcome is presented,
**Then** show a clear warning and retain the driver's known trip facts with Stoppinformasjon mangler where applicable,
**And** attempt evidence-supported recovery from available timetable data for the same trip/service date before declaring the list unavailable,
**And** do not substitute another journey, fabricate stops, infer a final-stop identifier or delete the trip because source data is missing,
**And** record that automatic stop progression is unavailable for the missing-list trip; later driving behavior must use the approved manual completion/abort/next-activity fallback.

**Given** the source times out, fails, returns an incomplete response or is unavailable offline,
**When** lookup or recovery is attempted,
**Then** display a source/availability failure distinct from a successful no-match result,
**And** retain entered service date, activity identity/order, manual corrections and any previously supported linked data, qualifying its availability/freshness appropriately,
**And** offer retry without silently choosing a different trip or pretending never-downloaded data is present,
**And** no simulated response is substituted into an operational draft.

**Given** the driver changes matching-relevant draft fields while a request is pending, or an old candidate list is reused,
**When** a result or selection is applied,
**Then** verify the target owner/draft/activity and the matching input revision,
**And** a stale result cannot overwrite current input or link a journey based on superseded values; explain that matching must be checked again,
**And** later edits that invalidate a previously selected match visibly mark its link/details unresolved rather than continuing to present them as confirmed for the edited trip.

**Given** a valid match or explicit candidate choice is saved,
**When** local persistence, synchronization and reopening occur,
**Then** preserve activity/source identities, ordering, both time representations, selected candidate provenance and missing/uncertain status using atomic state/event storage,
**And** only a matching valid receipt changes the event to server-confirmed, with immutable retries and protected PostgreSQL mutation as in prior stories,
**And** pending logout, storage failures, ownership and earliest AD-12 expiry apply to every introduced private association/event/receipt; late responses cannot unlock or resurrect data,
**And** public source cache lifecycle is separate and cannot retain expired private shift associations.

**Given** the matching/candidate surface,
**When** used by touch, keyboard or enlarged text,
**Then** loading, candidate differences, unknown metadata, warnings and retry/cancel/selection actions use clear labels and approved preparation controls,
**And** focus/error handling preserves context and no distinction relies on color alone,
**And** non-passenger activities bypass passenger-trip matching without being erased or assigned fictitious timetable journeys.

**Traceability:** FR-3, FR-4/5 identity preservation, NFR-2/3; UX-DR5/38/39/43/44; AD-1 transit port, AD-5 service-date/source identity conventions, AD-7 qualified targeted matching, AD-2/10/12 persistence/access/retention. Preserve the owner's extended-time/calendar-time decision in approved Story 2.2. This does not implement FR-6 live initial-trip selection or whole-day offline readiness.

**Dependencies:** Implemented Story 2.3 with its E1 foundations and completed Story 2.2 qualification establishing the chosen query/field semantics. A negative or inconclusive qualification finding is not cured by accepting a first API suggestion; material gaps require the explicit solution decision already specified. Imported drafts from 2.4/2.5 use this same contract, but those import paths are not required to demonstrate lookup for manually entered facts.

**Implementation evidence:** Checked unique/multiple/no-match/source-failure cases, partial responses, 20/24 overlap and service-calendar boundaries; Friday 25:30 and competing Saturday 01:30 candidates; missing stop sequence and available-data recovery; cancellation, stale result after manual edit, invalidated prior match, retry/reload; atomic write/receipt faults, ownership/logout/expiry and accessible candidate selection. Separate actual-source qualification from labelled synthetic fault tests. No tests run during drafting.

**Size boundary:** One draft trip's matching/selection/persistence path using the qualified adapter, not bulk feed ingestion, whole-day bundle orchestration, active-driving progression, plan confirmation or scoped active-day revisions. Source query implementation must not silently adopt an alternative architecture. All V1 preparation and fallback requirements remain in scope across their assigned stories.

**Pilot qualification:** Repeatable implemented matching contributes to E8-D. Actual source coverage must be backed by 2.2 evidence, and full-day data completeness, offline transitions and target-device behavior still require E8-P integration checks. E8-E remains later field evaluation. This is a story draft, not implementation or a readiness decision.

**Approval:** Approved by the owner on 2026-09-25 with explicit time/stop-discrepancy tests: preserve driver corrections, expose source values and differences, and prevent fresh or delayed responses from silently replacing corrections. A unique match requires identity and service-date evidence, not just line number and clock time. Planning approval only; the approved copy in epics.md is canonical.
