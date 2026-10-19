---
title: IBE160 — Approved Course V1 Backlog
status: planning-complete
decision: SCOPE-02
approved: true
approvedOn: 2026-10-19
epics: 4
stories: 20
implementationStatus: not-started
---

# IBE160 — Active Course V1 Backlog

## Authority and numbering

Jonas approved [SCOPE-02](sprint-change-proposal-2026-10-19.md) on 19 October. This is the sole active epic/story source. [PRD](prds/prd-IBE160-2026-09-21/prd.md), [architecture](architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md) and [DESIGN](ux-designs/ux-IBE160-2026-09-22/DESIGN.md) supply shared rules.

Four new epics use numeric IDs **9–12** for the BMAD parser, with aliases **V1-E1–V1-E4**. Stories retain the approved stable aliases **V1-01–V1-20**, mapped below. No old ID is reused for different work. The previous eight epics/80 stories are historical, including their approvals; see the [archive](archive/pre-scope-02-2026-10-19/README.md) and the proposal's exhaustive old-to-new map.

No application feature is implemented or accepted by planning approval. All new stories start in backlog. Plans here and under story-drafts are planning definitions, not executable completion evidence. First implementation tasks are V1-01 and V1-02; the second can run if representative PDFs are unavailable.

## Delivery boundary

60–80 remaining hours are estimated, not guaranteed; plan against approximately 60 and reserve at least 12 for correction/delivery. Text-PDF qualification is timeboxed to 3–4 hours. Review capacity after 8–10 hours and around 30 hours. December deadline remains unconfirmed.

Include reviewed text PDF, manual plan/bus/activity/outcomes, manually maintained source-linked notices, online server persistence and isolated fictional fullstack assessment. No automatic source/GPS, private offline persistence, mentor workflows, advanced active-plan revisions, PDF export or mandatory field trial. Shared access, expiry, validation, uncertainty and error behavior are implemented with each feature; later verification does not postpone them.

## Traceability and sequence

| Alias | Canonical ID | Requirement coverage | Acceptance | Dependencies |
|---|---|---|---|---|
| V1-01 | 9.1 | FR-2; NFR-2 | AC-01 | None |
| V1-02 | 9.2 | FR-20/25; NFR-4 | AC-11 | None |
| V1-03 | 9.3 | FR-1; NFR-3 | AC-09 | V1-02 |
| V1-04 | 9.4 | FR-4/17/20/24; NFR-2/3 | AC-02/07/09 | V1-03 |
| V1-05 | 10.1 | FR-2/24; NFR-2/3 | AC-01/06 | V1-01, V1-04 |
| V1-06 | 10.2 | FR-2/4; NFR-2 | AC-02/06 | V1-04, V1-05 |
| V1-07 | 10.3 | FR-2/4/5/24 | AC-02/07 | V1-06 |
| V1-08 | 10.4 | FR-5/11 | AC-02 | V1-07 |
| V1-09 | 10.5 | FR-4/5 | AC-02/03 | V1-07, V1-08 |
| V1-10 | 11.1 | FR-6/10/11/20 | AC-03 | V1-09 |
| V1-11 | 11.2 | FR-3/10; NFR-2 | AC-03 | V1-10 |
| V1-12 | 11.3 | FR-11/21/22/24 | AC-08 | V1-11 |
| V1-13 | 11.4 | FR-12/13/14/24 | AC-04/09 | V1-03 |
| V1-14 | 11.5 | FR-12/13/14/19 | AC-04/05 | V1-09, V1-13 |
| V1-15 | 11.6 | FR-17/18/20; NFR-2 | AC-07 | V1-04, V1-12, V1-14 |
| V1-16 | 12.1 | FR-1/2/24; NFR-3 | AC-06/09 | V1-05, V1-12, V1-13 |
| V1-17 | 12.2 | FR-25; NFR-2/3 | AC-11 | V1-12, V1-14, V1-15 |
| V1-18 | 12.3 | NFR-1/4; IR-01 | AC-10 | V1-09, V1-11, V1-14 |
| V1-19 | 12.4 | FR-1–25 active subset; NFR-2/3/4 | AC-01–09/11/12 | V1-15, V1-16, V1-17, V1-18 |
| V1-20 | 12.5 | FR-25; NFR-4 | AC-11/12 | V1-19 |

FR-7–9, FR-15 and FR-23 are deferred; the remaining original FRs are narrowed as stated in PRD section 6. S02-A–G and IR-01 apply across the relevant slices. Functional/fullstack acceptance is separate from benefit hypotheses and unperformed operational evaluation.

## Epic 9: Save a Private Working-Day Draft

**Alias:** V1-E1. The owner can run a real local fullstack slice, sign in and save/reopen a private draft. The independent PDF experiment establishes the supported input envelope.

**Depends on:** none; V1-01 and V1-02 are independent roots.

### Story 9.1: Establish supported imports

**Stable alias:** V1-01. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** none.
**Traceability:** FR-2; NFR-2; AC-01; SCOPE-02.

**User outcome:** 3–5 anonymized PDFs with independently checked expected activities, dates and uncertainty; record exact/partial/unsupported extraction and a pass/fail decision.

**Acceptance criteria:**
- Use independently checked expected facts rather than deriving expected results from the parser output. Classify each fixture/layout as supported, partial or unsupported. Stop the 3–4-hour experiment with evidence and a recommendation; a failed useful input set triggers an explicit scope decision. V1-02 can proceed independently with fictional data.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract. This bounded experiment can finish with negative evidence; downstream PDF acceptance still requires a useful supported envelope.

**Planning copy:** [V1-01](story-drafts/story-v1-01.md).

### Story 9.2: Run a persisted fictional day locally

**Stable alias:** V1-02. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** none.
**Traceability:** FR-20/25; NFR-4; AC-11; SCOPE-02.

**User outcome:** documented local startup opens the frontend; a real API saves/reads a fictional day in PostgreSQL and preserves it after service restart.

**Acceptance criteria:**
- Document startup, migrations, fictional seed and teardown; demonstrate an actual API write/read in PostgreSQL and persistence after service restart. Bind private development services to loopback and record executable versions. No static-only demo can pass this slice.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-02](story-drafts/story-v1-02.md).

### Story 9.3: Access private work

**Stable alias:** V1-03. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-02.
**Traceability:** FR-1; NFR-3; AC-09; SCOPE-02.

**User outcome:** provisioned private login/logout, server authorization, no public signup and no demo access to private records. Session expiry requires sign-in without changing saved data.

**Acceptance criteria:**
- Verify valid/invalid credentials, fixed 14-day session expiry, logout, direct unauthenticated/cross-owner requests, CSRF/origin handling and private/demo isolation. No public signup or offline day grant. No private state survives authorized logout in browser presentation; unreachable-server logout remains explicitly unconfirmed.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-03](story-drafts/story-v1-03.md).

### Story 9.4: Save and reopen a draft

**Stable alias:** V1-04. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-03.
**Traceability:** FR-4/17/20/24; NFR-2/3; AC-02/07/09; SCOPE-02.

**User outcome:** validated activities and explicit service/calendar dates survive reload; stale revision is rejected visibly; draft expiry and no-store private responses apply from introduction.

**Acceptance criteria:**
- Validate service/calendar dates, overnight offsets and unknown fields according to PRD section 4. Persist the draft with a fixed expiry and stable identity. Failed and stale writes preserve input and never overwrite a newer revision; expiry is checked before retry.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-04](story-drafts/story-v1-04.md).

## Epic 10: Review and Confirm a Supported Shift

**Alias:** V1-E2. The driver can review text-PDF output, correct it, confirm a day, assign the actual bus and inspect its chronological overview.

**Depends on:** earlier included slices, as explicitly declared below. No dependency on an old deferred epic.

### Story 10.1: Review a text PDF

**Stable alias:** V1-05. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-01, V1-04.
**Traceability:** FR-2/24; NFR-2/3; AC-01/06; SCOPE-02.

**User outcome:** supported files produce an unconfirmed draft with page/field uncertainty; original/temporary files are transient and cleaned after success/failure/cancel, including interrupted-job cleanup.

**Acceptance criteria:**
- Compare every supported fixture against independent expected activities/fields. Reject unsupported scans/images visibly; clean originals after success/failure/cancel and interrupted processing. Existing confirmed work remains intact. No raw files or extracted-text archives persist in logs/client storage.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-05](story-drafts/story-v1-05.md).

### Story 10.2: Correct the draft

**Stable alias:** V1-06. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-04, V1-05.
**Traceability:** FR-2/4; NFR-2; AC-02/06; SCOPE-02.

**User outcome:** edit/add/remove/order trips and other activities; unresolved fields remain visible, invalid times are rejected and cancelling leaves saved data unchanged.

**Acceptance criteria:**
- Test wrong-time correction, omitted activity addition, removal/reordering, unknown codes and cancel. Invalid required dates/type block confirmation; nullable places remain visibly unknown. Source/manual provenance remains distinguishable after saving.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-06](story-drafts/story-v1-06.md).

### Story 10.3: Confirm the reviewed plan

**Stable alias:** V1-07. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-06.
**Traceability:** FR-2/4/5/24; AC-02/07; SCOPE-02.

**User outcome:** explicit review/confirmation creates one saved confirmed plan; errors/duplicate clicks cannot activate a partial or duplicated plan. Required route/time facts must be resolved or explicitly unknown where permitted.

**Acceptance criteria:**
- Show the exact reviewed revision and fixed planned-final-end expiry before explicit confirmation. Invalid required fields are resolved first. A repeated confirmation returns the same saved plan; an uncertain response is not shown as successful. New draft confirmation never silently replaces an active day.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-07](story-drafts/story-v1-07.md).

### Story 10.4: Record the physical bus

**Stable alias:** V1-08. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-07.
**Traceability:** FR-5/11; AC-02; SCOPE-02.

**User outcome:** manual entry/correction preserves route and vehicle duty; imported Vogn never becomes an assumed physical bus.

**Acceptance criteria:**
- Preserve leading zeros/meaningful bus identifier formatting. A bus correction changes no route, activity ID or vehicle-duty identity. Imported Vogn cannot prefill an assumed physical bus.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-08](story-drafts/story-v1-08.md).

### Story 10.5: Read the day

**Stable alias:** V1-09. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-07, V1-08.
**Traceability:** FR-4/5; AC-02/03; SCOPE-02.

**User outcome:** reporting time and ordered trips/breaks/transfers/bus changes match the confirmed plan; separate known parts/locations and overnight dates remain visible.

**Acceptance criteria:**
- Compare the displayed order, reporting time, breaks, transfers and known locations with the saved expected plan. Include overnight and separated work-period cases; no invented transfer, later depot or completion. Missing bus remains unassigned.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-09](story-drafts/story-v1-09.md).

## Epic 11: Consult Activities and Manually Maintained Notices

**Alias:** V1-E3. The driver can select activities, record explicit outcomes, maintain source-linked notices and recover honestly from failed online saves.

**Depends on:** earlier included slices, as explicitly declared below. No dependency on an old deferred epic.

### Story 11.1: Choose the intended activity

**Stable alias:** V1-10. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-09.
**Traceability:** FR-6/10/11/20; AC-03; SCOPE-02.

**User outcome:** direct and previous/next selection distinguish lines 20/24 and direction; selection persists online and never advances by clock or changes completion status.

**Acceptance criteria:**
- Include adjacent line 20/24 trips, opposite directions and overnight dates. Selection survives acknowledged online reload and does not change when scheduled time passes. Previous/next never sets outcomes and end boundaries have explicit disabled labels.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-10](story-drafts/story-v1-10.md).

### Story 11.2: Understand the selected activity

**Stable alias:** V1-11. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-10.
**Traceability:** FR-3/10; NFR-2; AC-03; SCOPE-02.

**User outcome:** show trip or non-passenger type, planned times and known places; missing stop data has no fabricated current/next stop. Boundary controls clearly show no previous/next.

**Acceptance criteria:**
- Render selected trip or non-passenger type with planned dates/times and known places. Label manual selection; never render an invented current/next stop or GPS-confirmed location. Known missing information is distinct from no previous/next activity.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-11](story-drafts/story-v1-11.md).

### Story 11.3: Record outcomes and close

**Stable alias:** V1-12. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-11.
**Traceability:** FR-11/21/22/24; AC-08; SCOPE-02.

**User outcome:** manually mark completed/skipped/interrupted/unknown, confirm normal end or abort, then read a short recap. Cancel preserves the day; ending cannot silently complete remaining activities or resume afterwards.

**Acceptance criteria:**
- Default outcomes remain unknown until explicitly recorded. Allow manual completion/skipped/interrupted before terminal closure; confirm/cancel normal end or abort. Atomically persist terminal status/server time/expiry once. No post-end editing, silent completion or resumption. Recap is read-only within expiry.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-12](story-drafts/story-v1-12.md).

### Story 11.4: Maintain a planned notice

**Stable alias:** V1-13. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-03.
**Traceability:** FR-12/13/14/24; AC-04/09; SCOPE-02.

**User outcome:** private editor stores title, explicit line tags, source URL, nullable source update/validity and separate entered/checked-at time; demo uses fictional records.

**Acceptance criteria:**
- Require title, explicit line tags and an HTTP(S) original-source link for real notices. Workday ownership/expiry applies. Source-update and validity are nullable; entry/edit time is not source check. Only an explicit check action sets checked-at. Fictional records remain isolated.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-13](story-drafts/story-v1-13.md).

### Story 11.5: Read line/date notices

**Stable alias:** V1-14. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-09, V1-13.
**Traceability:** FR-12/13/14/19; AC-04/05; SCOPE-02.

**User outcome:** show each applicable notice once with all matching lines; separate incidents remain separate; unknown validity is qualified and no entries does not mean no disruptions. No current-stop matching claim.

**Acceptance criteria:**
- Test shared line 20/24 notice once with both matching lines, a separate event on line 20, known non-overlap and unknown/partial validity. Use planned date intervals, not current-trip certainty. Empty/unavailable/unchecked states are distinct, and no list state claims full source coverage.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-14](story-drafts/story-v1-14.md).

### Story 11.6: Recover from an unavailable server

**Stable alias:** V1-15. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-04, V1-12, V1-14.
**Traceability:** FR-17/18/20; NFR-2; AC-07; SCOPE-02.

**User outcome:** show unsaved/unavailable status, preserve current form input while the page remains open, reconcile a retry with server state and reopen the last saved revision when connected. No offline restart guarantee or silent lost-save claim.

**Acceptance criteria:**
- Exercise timeout before commit, lost response after commit, stale revision and backend unavailable on save. Resolve stable operation ID/status before retrying; no duplicates or force overwrite. Keep form input while open and warn before avoidable loss; online reopen recovers last server-saved revision, never an invented offline copy.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-15](story-drafts/story-v1-15.md).

## Epic 12: Verify and Deliver the Assessable Application

**Alias:** V1-E4. The assessor can repeat an isolated fictional assessment and inspect executed privacy, UI, integration and reproducibility evidence.

**Depends on:** earlier included slices, as explicitly declared below. No dependency on an old deferred epic.

### Story 12.1: Enforce the retained-data boundary

**Stable alias:** V1-16. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-05, V1-12, V1-13.
**Traceability:** FR-1/2/24; NFR-3; AC-06/09; SCOPE-02.

**User outcome:** end-to-end expiry and deletion across drafts, plans, outcomes and associated private notices; no uploaded originals in logs/caches/repository. Late/stale requests cannot recreate expired work.

**Acceptance criteria:**
- Verify draft creation+7d and confirmed min(planned-end+7d, server-end+7d) deadlines without sliding renewal. Deny immediately, purge at startup/hourly, remove associated outcomes/notices/operation metadata and prevent late recreation. Inspect original cleanup, private no-store/back behavior and absence of private persistent browser/log/repository data.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-16](story-drafts/story-v1-16.md).

### Story 12.2: Repeat a fictional assessment

**Stable alias:** V1-17. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-12, V1-14, V1-15.
**Traceability:** FR-25; NFR-2/3; AC-11; SCOPE-02.

**User outcome:** reset fictional data and exercise import uncertainty, missing metadata and failed save without network services or geolocation. Reset cannot affect private data.

**Acceptance criteria:**
- Exercise included failures only: unsupported import, unknown notice metadata, unavailable/stale/lost save and terminal closure. Demo reset affects only fictional configuration/store. No GPS/live feed required; no-login demo cannot authenticate to private API. Keep a separate documented actual fullstack evidence path.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-17](story-drafts/story-v1-17.md).

### Story 12.3: Use the included views on tablet and PC

**Stable alias:** V1-18. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-09, V1-11, V1-14.
**Traceability:** NFR-1/4; IR-01; AC-10; SCOPE-02.

**User outcome:** labelled controls, keyboard focus, manual Day/Night, text enlargement and applicable IR-01 contrast across actual states; record actual browser/device limitations.

**Acceptance criteria:**
- Measure actual included foreground/background/icon/focus states in both manual themes against IR-01. Check keyboard dialog focus/return, long Norwegian text, enlargement, disabled boundaries and tablet/PC layout. Persist manual theme without private data. No Auto, wake, GPS or PDF pass inferred.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-18](story-drafts/story-v1-18.md).

### Story 12.4: Verify the complete user flow

**Stable alias:** V1-19. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-15, V1-16, V1-17, V1-18.
**Traceability:** FR-1–25 active subset; NFR-2/3/4; AC-01–09/11/12; SCOPE-02.

**User outcome:** real PostgreSQL integration plus browser flow from supported PDF through corrections, saved plan, manual selection, notices, closure and reload; include failures and independent expected data.

**Acceptance criteria:**
- Run the actual API/PostgreSQL plus a browser happy/failure flow using independent fixture expectations. Include dates/identity, notices, stale/lost writes, closure, reload, authorization and expiry. Record passed/failed/not-run and precise build; do not mirror implementation as a substitute for expected outcomes.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-19](story-drafts/story-v1-19.md).

### Story 12.5: Deliver a reproducible submission

**Stable alias:** V1-20. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-19.
**Traceability:** FR-25; NFR-4; AC-11/12; SCOPE-02.

**User outcome:** test README from a clean local environment, bundle fictional fixtures and test evidence, describe AI use/limitations and trace implemented requirements to tests.

**Acceptance criteria:**
- Execute README from a clean local setup, including seed/reset/test/start, with no external owner secrets, paid account, real file or runtime live feed. Include versioned evidence, supported input envelope, remaining limitations and AI-process reflection. Report extraction/functional/UI results separately from unperformed field benefit.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-20](story-drafts/story-v1-20.md).
