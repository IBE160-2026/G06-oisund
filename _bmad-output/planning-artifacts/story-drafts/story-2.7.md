---
status: approved
created: 2026-09-25
epic: E2
story: '2.7'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['2.3', '2.6']
---

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

This slice confirms the owner's initial plan before duty and presents its overview. Whole-day data preparation, split-part composition and revisions of already confirmed work remain separate required E2 slices.

### Story 2.7: Review and Explicitly Confirm the Initial Own Plan

As the pilot owner,
I want to review my own activities and actual bus assignment before explicitly confirming the plan,
So that the working-day overview reflects my checked intentions rather than an unreviewed import or timetable response.

**Acceptance Criteria:**

**Given** an owned, unexpired manual or imported draft and permitted ordinary application access,
**When** the owner opens final preparation review,
**Then** show the service date, reporting time, chronological trips and other activities, known start/end locations, breaks, bus changes and transfers,
**And** preserve known paid/unpaid/unknown break classification and distinguish unknown information from absent activities,
**And** show manual corrections, source discrepancies, unresolved matches and incomplete import coverage without presenting the plan as complete merely because extraction or lookup succeeded,
**And** Friday 25:30 retains Friday service identity and working-day position while calendar presentation uses Saturday 01:30.

**Given** the draft contains a vehicle-duty value labelled Vogn,
**When** the driver enters or corrects the actual physical bus number before duty,
**Then** store and display the manually entered physical bus separately from vehicle duty, shift and trip identity,
**And** never populate the physical bus automatically from Vogn; an unentered bus remains visibly unknown,
**And** save/reopen preserves the assignment and manual provenance without implying that a physical replacement has occurred.

**Given** the review contains uncertain fields, missing stop information or incomplete source coverage,
**When** the owner prepares to confirm,
**Then** provide correction and return-to-review actions with the affected activities/parts identifiable,
**And** do not require invented values or a successful source match to retain a known trip; unsupported matches remain unresolved and missing stop lists retain their explicit limitations,
**And** resolve temporal ambiguity needed to establish the service date, activity sequence and planned final end before confirmation; explain the affected fields instead of guessing a retention deadline,
**And** confirmation does not turn unknown facts, source gaps or manual choices into source-verified facts.

**Given** a reviewed trip has no source match but temporal ambiguities preventing a correct service date, sequence or planned final end have been resolved,
**When** the driver explicitly confirms the reviewed plan,
**Then** that trip may be included in the confirmed plan without a fabricated source association,
**And** missing timetable matches, stop data and physical bus number remain explicitly unknown/missing after confirmation and reopening, never labelled verified by the confirmation itself.

**Given** the owner has reviewed a specific current draft revision,
**When** the owner explicitly confirms that initial own plan,
**Then** atomically persist the confirmed plan/revision, its stable workday/plan/activity identities and the confirmation event before showing success,
**And** confirm exactly the reviewed revision; concurrent edits or late import/matching results cannot be silently included or overwrite it,
**And** if the draft changes during review, reject confirmation of the stale review and require the driver to review the changed revision before confirming; test a manual edit and an applied asynchronous result between review and confirmation,
**And** repeated taps/retries do not create duplicate plans, activities or confirmation events,
**And** cancelling review leaves the draft unconfirmed and creates no plan or active trip.

**Given** confirmation succeeds locally,
**When** the overview is displayed or reopened,
**Then** show the confirmed plan and physical bus with clear local/pending versus server-confirmed storage status,
**And** only a valid receipt matching the immutable submitted batch establishes server confirmation; use authorized PostgreSQL transactions and revision checks for backend changes,
**And** failed local commit shows no successful confirmation and retains a recoverable draft; uncertain server responses preserve the locally confirmed result and retry identity,
**And** plan confirmation starts neither an active trip nor an active-day access exception and does not assert any activity was performed.

**Given** the confirmed plan exists,
**When** preparation status is presented,
**Then** show plan confirmation separately from required downloaded day data and complete application-asset readiness,
**And** matching one or several trips or receiving a server receipt cannot produce a whole-day offline-ready claim,
**And** source notices not yet retrieved/implemented are unknown or unavailable, never an all-clear; notice ingestion remains E4,
**And** later sources cannot silently change the confirmed plan; subsequent changes require their own reviewed revision flow.

**Given** draft confirmation and its server synchronization,
**When** the draft becomes a confirmed plan,
**Then** remove redundant draft copies under AD-12 while retaining necessary plan facts, corrections, provenance and permissible pending synchronization evidence,
**And** apply the combined-day expiry from the established planned final end while the day remains unended; reopening, synchronization and refresh do not restart it,
**And** do not mutate an already submitted batch to perform cleanup or retain redundant private payloads as a hidden draft archive; preserve AD-5 receipt/retry and AD-12 deletion rules together,
**And** enforce ownership, pending-logout/storage-error locks and expiry before display/send on client and backend; late responses cannot recreate deleted/expired drafts or plans.

**Given** the preparation overview and confirmation controls,
**When** used with touch, keyboard or enlarged text,
**Then** use approved readable preparation layouts, explicit labels, visible focus and recoverable errors without relying on color alone,
**And** keep the persistent clock visible without using clock time as activity-completion evidence,
**And** identify the plan as the owner's own plan; no accompanied-person plan or operational mentor role is fabricated.

**Traceability:** FR-2 explicit confirmation; FR-4/5 overview and physical assignment; preparation portions of FR-17/24; NFR-2/3; UX-DR4/5/6/12/38/42/43, own-plan boundary of UX-DR26; AD-2/4/5 persistence and distinct readiness, AD-6 reviewed confirmation, AD-7 no silent plan changes, AD-10 ordinary access and AD-12 cleanup/expiry. All AD-1–AD-14 remain binding where applicable.

**Dependencies:** Implemented Stories 2.3 and 2.6 with their E1 foundation. A manual draft can demonstrate this independently of import; implemented 2.4/2.5 feed the same review. Source qualification under 2.2 remains a prerequisite for real matching claims. No future data-bundle, driving, mentor or revision story is required to demonstrate initial plan confirmation.

**Implementation evidence:** Checked manual/imported preparation, unknown values and incomplete coverage, time/stop discrepancies, Friday 25:30 ordering, Vogn versus physical bus, explicit confirm/cancel, stale review, duplicate submission, local write failure and lost/mismatched server receipts, reopen and expiry, redundant-draft cleanup and accessible overview. Use PostgreSQL integration evidence and distinguish fixture demonstrations from actual source/device qualification. Tests are specified, not executed here.

**Size boundary:** One initial own plan and its confirmation/overview. No whole-day download orchestration, split-part editing, active-plan reconciliation, operational bus replacement, active-trip selection, notices, mentor linking or active-day grant. These remain V1 obligations in their assigned stories; no capacity estimate or scope reduction is implied.

**Pilot qualification:** Demonstrable confirmation and persistence contribute to E8-D. Whole-day preparation, target-tablet storage/access behavior and complete operational integration remain E8-P checks before actual shifts; E8-E remains later field evaluation. Confirmation by the driver is not qualification for pilot use.

**Approval:** Approved by the owner on 2026-09-25: a reviewed unmatched trip can enter the confirmed plan once blocking temporal ambiguities are resolved; missing matches, stops and physical bus remain unknown/missing rather than verified. Any draft change during review requires a new review before confirmation. Planning approval only; the approved copy in epics.md is canonical.
