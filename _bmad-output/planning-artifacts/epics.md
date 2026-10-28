---
title: IBE160 — Approved Course V1 Backlog
status: planning-complete
decision: SCOPE-02
approved: true
approvedOn: 2026-10-19
epics: 4
stories: 20
implementationStatus: historical-planning-baseline
currentDeliveryTracking: ../implementation-artifacts/sprint-status.yaml
---

# IBE160 — Active Course V1 Backlog

## Authority and numbering

Jonas approved [SCOPE-02](sprint-change-proposal-2026-10-19.md) on 19 October. This is the sole active epic/story source. [PRD](prds/prd-IBE160-2026-09-21/prd.md), [architecture](architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md) and [DESIGN](ux-designs/ux-IBE160-2026-09-22/DESIGN.md) supply shared rules.

Four new epics use numeric IDs **9–12** for the BMAD parser, with aliases **V1-E1–V1-E4**. Stories retain the approved stable aliases **V1-01–V1-20**, mapped below. No old ID is reused for different work. The previous eight epics/80 stories are historical, including their approvals; see the [archive](archive/pre-scope-02-2026-10-19/README.md) and the proposal's exhaustive old-to-new map.

No application feature is implemented or accepted by planning approval. At the approved planning baseline, all new stories started in backlog. That baseline is historical; current delivery is recorded in [sprint tracking](../implementation-artifacts/sprint-status.yaml) and promoted implementation specifications. Plans here and under story-drafts are planning definitions, not executable completion evidence. First implementation tasks are V1-01 and V1-02; the second can run if representative PDFs are unavailable.

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
- Fixture baseline approved by Jonas Øisund on 2026-10-20: use all seven anonymized PDFs and the [approved fasit](../../Eksempelfiler/README.md) as independent expected facts. Fixture preparation and owner approval are complete; extraction classification and pass/fail evidence remain open. Preserve source rows while checking allowed pause grouping, vehicle duty versus physical bus, three-digit realtime values with leading zeros, example 5 paid free time and example 6 clarified deadhead. Record the tested subset explicitly if the timebox covers fewer than seven PDFs.
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
- Use the [owner-approved PDF baseline (2026-10-20)](../../Eksempelfiler/README.md). Parse Vogn as vehicle duty, retain full 960xxx and its final three-character realtime-screen value (including leading zeros), and leave physical bus unknown. Preserve source activity/provenance when adjacent pauses are grouped; apply the documented meal/coffee/split-duty labels. Check the explained paid free time in example 5 and 15:33–16:00 Skoglyst–Breivika deadhead in example 6. Do not generalize that Travel to interpretation to unrelated rows.
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
- Apply the [owner-approved vehicle-duty/bus distinction (2026-10-20)](../../Eksempelfiler/README.md): Vogn 960xxx is a collection of trips, and xxx is the three-character realtime-screen input (e.g. 006 or 090), never a physical bus identifier. None of the seven PDFs contains the actual bus; it must be obtained externally and entered manually. A changed vehicle duty does not establish a physical bus change; no automatic/live integration is added by this clarification.
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
- Apply the [owner-approved display rules (2026-10-20)](../../Eksempelfiler/README.md): adjacent pause types may form one pause spanning their combined interval; any MealBreak makes it matpause, Coffee alone is kaffepause, and Split break is split break/deltskiftpause. Check example 2 matpause 12:01–12:43 and example 7 matpause 08:52–09:28 while retaining source rows/provenance. Show vehicle duty separately from manually assigned actual bus, preserve three-digit realtime values including zeros, and do not infer a physical bus change from a duty change.
- Compare the displayed order, reporting time, breaks, transfers and known locations with the saved expected plan. Include overnight and separated work-period cases; no invented transfer, later depot or completion. Missing bus remains unassigned.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-09](story-drafts/story-v1-09.md).

## Epic 11: Consult Activities and Manually Maintained Notices

**Alias:** V1-E3. The driver can select activities, record explicit outcomes, maintain source-linked notices and recover honestly from failed online saves.

**Depends on:** earlier included slices, as explicitly declared below. No dependency on an old deferred epic.

**Owner-approved allocation, 2026-10-24:** Story 11.1 additionally owns explicit `Start skift`, persisted start status and first server-accepted actual start time, with repeated/concurrent/lost-response recovery. Activity consultation/selection is available before start and never activates or completes work. Planned and actual start stay distinct. Story 11.2 reuses the selected activity and current lifecycle. Story 11.3 extends that lifecycle for outcomes/end/abort/recap and must reuse the existing start action/time rather than duplicate it; terminal guards and shortened expiry belong there. Story 11.6 integrates recovery without postponing 11.1 write integrity. This allocation changes scope, not implementation or final acceptance status; use sprint tracking and the promoted 11.1 specification for current delivery state.

### Story 11.1: Choose the intended activity

**Stable alias:** V1-10. **Historical planning baseline:** backlog; implementation/evidence had not started at scope approval. Current 11.1 implementation/review and owner-acceptance state is recorded in [sprint tracking](../implementation-artifacts/sprint-status.yaml) and the [promoted specification](../implementation-artifacts/spec-11-1-choose-the-intended-activity.md).
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

**Stable alias:** V1-11. **Historical planning baseline:** backlog. Current implementation/acceptance is tracked in [sprint status](../implementation-artifacts/sprint-status.yaml) and the [11.2 specification](../implementation-artifacts/spec-11-2-understand-the-selected-activity.md).
**Depends on:** V1-10.
**Traceability:** FR-3/10; NFR-2; AC-03; SCOPE-02.

**User outcome:** show trip or non-passenger type, planned times and known places; missing stop data has no fabricated current/next stop. Boundary controls clearly show no previous/next.

**Owner-approved refinement, 2026-10-24:** Separate upload, interpretation control/editing, day and selected activity screens. Select/open a member from the day, consult only that member with previous/next, and return without losing registered data or selection. Preserve unsaved/recovery state and access guards. Navigation does not Start or record outcomes. Notices and end/recap have planned day-linked destinations but remain 11.3–11.5 work. Intermediate stops are post-V1; demo expansion remains later work.

**Acceptance criteria:**
- Render selected trip or non-passenger type with planned dates/times and known places. Label manual selection; never render an invented current/next stop or GPS-confirmed location. Known missing information is distinct from no previous/next activity.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-11](story-drafts/story-v1-11.md).

### Story 11.3: Record outcomes and close

**Stable alias:** V1-12. **Historical planning baseline:** backlog. Current implementation/review and owner acceptance are tracked in [sprint status](../implementation-artifacts/sprint-status.yaml) and the [11.3 specification](../implementation-artifacts/spec-11-3-record-outcomes-and-close.md).
**Depends on:** V1-11.
**Traceability:** FR-11/21/22/24; AC-08; SCOPE-02.

**User outcome:** manually mark completed/skipped/interrupted/unknown, confirm normal end or abort, then read a short recap. Cancel preserves the day; ending cannot silently complete remaining activities or resume afterwards.

**Owner-approved refinement, 2026-10-25:** Outcome registration requires an explicitly started active shift. Before Start, the day, activity selection and details remain available. Selection/navigation never Starts or records outcomes. Keep separate activity/outcome, day-linked closure confirmation and read-only recap screens, preserving input and reachable recovery. The complete plan and implementation are approved; final owner acceptance is a separate recorded event.

**Acceptance criteria:**
- Default outcomes remain unknown until explicitly recorded. Allow manual completion/skipped/interrupted before terminal closure; confirm/cancel normal end or abort. Atomically persist terminal status/server time/expiry once. No post-end editing, silent completion or resumption. Recap is read-only within expiry.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-12](story-drafts/story-v1-12.md).

### Story 11.4: Maintain a planned notice

**Stable alias:** V1-13. **Status:** done; Jonas accepted the corrected SMS/text/all-lines delivery on 2026-10-25 and authorized commit/push. Final 61 notice API / 49 browser passes and local rollout/data preservation verified. The original 393 API / 395 browser gate is historical. See [delivery evidence](../../docs/evidence/11-4-manual-notices.md).
**Depends on:** V1-03.
**Traceability:** FR-12/13/14/24; AC-04/09; SCOPE-02.

**User outcome:** private editor stores title, short and detailed explanations, explicit selected/all-line scope, optional source description/URL, nullable source update/validity and separate entered/checked-at time; SMS-only sources need no URL; demo uses fictional records.

**Acceptance criteria:**
- Owner correction on 2026-10-25: require title and explicit selected/all-line scope. Selected scope requires tags; all-lines is an explicit choice, never inferred. Support short/deep explanation text and optional source description/link, including SMS-only notices. Validate any supplied link as HTTP(S); no website address is mandatory. Workday ownership/expiry applies. Source-update and validity are nullable; entry/edit time is not source check. Only an explicit check action sets checked-at. Fictional records remain isolated. See the corrective dispatch specification for current implementation/verification status.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-13](story-drafts/story-v1-13.md).

### Story 11.5: Read line/date notices

**Stable alias:** V1-14. **Status:** done; Jonas explicitly accepted the corrected account registry and expiry/extension delivery on 2026-10-26 (`Godkjent.`). Final gate: 420 backend and all 472 browser cases passed; migration/runtime/data preservation verified locally. No commit/push or further work is authorized by this acceptance.
**Depends on:** V1-09, V1-13.
**Traceability:** FR-12/13/14/19; AC-04/05; SCOPE-02.

**User outcome:** register each account notice once and reuse it automatically across eligible days until its required ending date or earlier manual ending. Allow extension only before expiry; show each matching incident once, qualify unknown starts and coverage, and never imply precise stop relevance or clear roads.

**Acceptance criteria:**
- Owner correction 2026-10-26: one account-owned notice must appear automatically on later imported/confirmed days with matching lines/intervals. Require a future ending date; date-only means end of that Oslo date. Automatic Utløpt and earlier Avsluttet manuelt are distinct from source check. Extend only while live; reject resurrection after expiry/manual ending. Original-shift deletion/closure/expiry cannot remove a still-valid notice. Preserve legacy records/receipts and qualify missing end dates for explicit completion.
- Test shared 20/24 once, separate incidents, day A to B without re-entry, known non-overlap, unknown start, date-only/precise-clock/DST ending, pre-/at-/post-deadline extension and retention cleanup. Empty/unavailable/unchecked states stay distinct and never establish source completeness or road clearance.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-14](story-drafts/story-v1-14.md).

### Story 11.6: Recover from an unavailable server

**Stable alias:** V1-15. **Status:** done; Jonas explicitly accepted the integrated delivery on 2026-10-26. Fresh final gate: 421 backend tests and all 479 browser cases passed; current source manifest recorded. See the [execution specification](../implementation-artifacts/spec-11-6-recover-from-an-unavailable-server.md) and [delivery evidence](../../docs/evidence/11-6-server-recovery.md).
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

**Stable alias:** V1-16. **Status:** done/accepted; Jonas explicitly approved on 27 October 2026.
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

**Stable alias:** V1-17. **Status:** done/accepted; Jonas approved the corrected integrated delivery on 27 October 2026.
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

**Stable alias:** V1-18. **Status:** done/accepted,27 October2026. Jonas' conditional approval became effective after remaining required physical checks passed; [final acceptance evidence](../../docs/evidence/12-3-device-acceptance-2026-10-27.md). No main merge/commit/push;12.4 remains backlog.
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

**Stable alias:** V1-19. **Status:** in-review; [implementation specification](../implementation-artifacts/spec-12-4-complete-user-flow.md) and [executed evidence](../../docs/evidence/12-4-handoff.md), owner acceptance pending.
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

**Stable alias:** V1-20. **Status:** done/accepted by Jonas on28October2026; [implementation specification](../implementation-artifacts/spec-12-5-reproducible-submission.md), [executed evidence](../../docs/evidence/12-5-reproduction.md) and [explicit owner decision](../../docs/evidence/12-5-owner-acceptance-2026-10-28.md). Epic12 closure remains separate.
**Depends on:** V1-19.
**Traceability:** FR-25; NFR-4; AC-11/12; SCOPE-02.

**User outcome:** test README from a clean local environment, bundle fictional fixtures and test evidence, describe AI use/limitations and trace implemented requirements to tests.

**Acceptance criteria:**
- Execute README from a clean local setup, including seed/reset/test/start, with no external owner secrets, paid account, real file or runtime live feed. Include versioned evidence, supported input envelope, remaining limitations and AI-process reflection. Report extraction/functional/UI results separately from unperformed field benefit.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.

**Planning copy:** [V1-20](story-drafts/story-v1-20.md).
