---
status: approved
created: 2026-09-25
epic: E2
story: '2.8'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['2.2', '2.6', '2.7']
---

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

This slice constructs and persists the transit-data portion of the revisioned OfflineBundle for the entire confirmed own plan. It reports actual local coverage without claiming full application/offline readiness. E4 owns notice ingestion; E5 owns integrated readiness and recovery.

### Story 2.8: Prepare Available Timetable Data for the Whole Confirmed Day

As the pilot owner,
I want the available timetable details for all trips in my confirmed day stored on the device with visible gaps,
So that later trips do not unexpectedly depend on a new download and I know which information is missing.

**Acceptance Criteria:**

**Given** an owned, unexpired confirmed plan and permitted application access,
**When** the owner prepares its day data,
**Then** enumerate every activity in that exact plan revision, including later trips and trips after midnight, rather than only the first/current trip or journey-planner suggestions,
**And** use the targeted transit adapter qualified under Story 2.2 and Story 2.6's identity/service-date rules to retrieve available ordered stops and planned times for supported associations,
**And** preserve all non-passenger activities and known plan facts without assigning them fictitious passenger journeys,
**And** preparation does not start a trip, confirm performed work or change the confirmed plan.

**Given** complete, partial, missing or unresolved timetable data for different trips,
**When** the bundle manifest and preparation overview are built,
**Then** record the covered plan revision, activity/source identities, relevant source versions where supplied, fetch/last-success times and available/missing requirements per trip,
**And** distinguish no supported match, missing stops, failed/incomplete retrieval and data not downloaded; unknown source metadata remains unknown,
**And** the whole-day transit-data status cannot say complete when any required trip data is missing, even if all requests finished successfully,
**And** when only part of the day downloads, keep coverage visible for every trip, including those without data, and never show Hele dagen klargjort for that partial result,
**And** retain the driver's confirmed unmatched trips, missing-bus state and known facts without making them source-verified or undoing plan confirmation.

**Given** a confirmed trip has a manual time/stop correction or an unresolved source association,
**When** preparation receives new source data,
**Then** preserve the correction and show source differences with provenance,
**And** do not silently select another candidate or rewrite the confirmed plan; matching ambiguity or a proposed association change remains explicit for later reviewed revision,
**And** Friday 25:30 and Saturday 01:30 retain their distinct service/calendar meaning, with similarly timed candidate journeys kept separate.

**Given** the plan contains both supported trip data and gaps,
**When** data is downloaded to the client,
**Then** atomically publish a locally consistent manifest with the corresponding available data in IndexedDB before marking those items stored on this device,
**And** a backend cache hit or successful HTTP response alone is not local availability,
**And** a failed/quota-limited local write cannot leave a manifest claiming absent payloads are available; preserve the last valid stored set and expose the failed items,
**And** server-held private bundle metadata uses authenticated FastAPI validation and PostgreSQL ownership/revision constraints; client-local download state is not inferred from a server receipt.

**Given** a partial download, timeout or interrupted preparation attempt,
**When** the driver retries or reopens preparation,
**Then** retain successfully committed compatible data and identify remaining gaps rather than discarding the day or creating duplicate activities,
**And** the UI reports the actual failure and offers retry instead of remaining indefinitely in progress,
**And** failed refresh retains previous data labelled with its last successful retrieval and uncertainty; retry does not overwrite corrections or advance the operational server revision merely because source facts were fetched.

**Given** preparation targets one plan revision and another revision becomes current before a result is applied,
**When** that response is processed,
**Then** do not advertise the old manifest as covering the new plan,
**And** preserve usable existing data with its actual revision/identity provenance and mark current-plan coverage pending or incomplete until verified,
**And** also reject cross-owner/day results and expired responses; test this through a controlled revision-change fixture without requiring the later revision-editor UI.

**Given** available transit data has been committed for an entire representative day,
**When** network access is removed and the preparation view is reopened in the already available compatible application,
**Then** every stored later trip's stops/times and known activity facts can be inspected from local storage, including overnight trips, without another source request,
**And** never-downloaded data remains explicitly unavailable and retained source data is not marked freshly verified,
**And** this test demonstrates stored day-data coverage only; cold boot after browser/tablet restart, active-day authority, driving progression, notices and PDF remain their assigned integrated stories and qualification checks.

**Given** preparation status is displayed,
**When** the driver inspects it using touch, keyboard or enlarged text,
**Then** distinguish confirmed plan, locally stored day data and complete application assets with accessible text and identifiable missing items,
**And** show notice coverage as unavailable/unknown until supplied by E4, never no-disruption evidence,
**And** do not display a global offline-ready or pilot-ready claim based only on this transit-data result; access authority and app-asset verification remain separate.

**Given** private bundle associations, downloaded data and preparation attempts,
**When** logout, storage-lock failure, expiry or cleanup occurs,
**Then** apply prior ownership/AD-10 locking and AD-12 combined-day deadlines to every private copy, including partial/staged copies and metadata,
**And** no download/retry/reopen extends retention or revives an expired day,
**And** public source cache may follow its separate lifecycle but cannot retain expired private day associations; no originals, private payload logs or GPS traces are introduced.

**Traceability:** Preparation portions of FR-3/5/17/20/24; NFR-2/3; UX-DR5/6/23/38/43/44; AD-1 transit boundary, AD-2 separate readiness/local storage, AD-4/5 PostgreSQL and revision/source separation, AD-7 whole-day targeted retrieval, AD-10/12 access/retention, AD-14 compatibility boundary. This is E2's OfflineBundle construction responsibility, not complete E5 recovery or E4 notice coverage.

**Dependencies:** Implemented Stories 2.6 and 2.7 plus actual Story 2.2 source qualification and inherited E1 storage/access. Material source-coverage gaps return to the owner under AD-7; no automatic bulk-feed adoption or V1 reduction. Later notices/revision UI/active driving are not prerequisites for demonstrating this slice.

**Implementation evidence:** Representative full-day manifest with several early/later/overnight trips and non-passenger activities; all-supported, unmatched, missing-stop and partial-source cases; failed local write, interrupted download/retry, stale plan response, manual-source discrepancy, offline inspection, ownership/logout/expiry and accessible per-item status. Separate actual-source coverage evidence from synthetic failure fixtures. Tests are planned, not run here.

**Size boundary:** One confirmed own plan's transit-data preparation and manifest, reusing the qualified adapter. No bulk feed pipeline, independent matching engine, notice polling, coherent cold-boot asset system, active-day grant, whole-application recovery or split-plan editing. Those V1 requirements remain assigned to their later slices.

**Pilot qualification:** Repeatable whole-day download/gap behavior contributes to E8-D. E8-P must verify actual source completeness and real tablet/storage/network/boot behavior with E3–E5 and subsequent features integrated. E8-E remains actual-shift evaluation. A stored bundle alone does not pass either gate.

**Approval:** Approved by the owner on 2026-09-25 with per-trip coverage remaining visible for partial-day downloads; partial data must never produce a whole-day-prepared status. Planning approval only; the approved copy in epics.md is canonical.
