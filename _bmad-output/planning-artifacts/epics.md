---
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics]
currentStep: step-03-create-stories
status: paused-by-owner-before-e4
currentEpic: E4
completedEpicPlanning: [E1, E2, E3]
currentStory: null
approvedStories: ['1.1', '1.2', '1.3', '1.4', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9', '2.10', '2.11', '2.12', '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10', '3.11', '3.12', '3.13', '3.14', '3.15']
storyDraft: null
created: 2026-09-23
updated: 2026-09-25
epicStructure: eight-formal-epics-approved
epicsApproved: true
requirementsApproved: true
capacity: unresolved-more-than-40-hours-no-fixed-total
deliveryDate: unresolved
storiesWritten: partial
inputDocuments:
  - briefs/brief-IBE160-2026-09-21/product-brief.md
  - briefs/brief-IBE160-2026-09-21/addendum.md
  - prds/prd-IBE160-2026-09-21/prd.md
  - prds/prd-IBE160-2026-09-21/addendum.md
  - ux-designs/ux-IBE160-2026-09-22/DESIGN.md
  - ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md
  - architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md
  - ../../Docs/development-log.md
---

# IBE160 - Epic Breakdown

## Overview

Steps 1 and 2 were explicitly approved with C on 2026-09-23: requirements, responsibility boundaries and all eight formal epic boundaries. Each epic must provide access, persistence, error handling and privacy for its own functions. Early source/OCR/device qualification and E8-D, E8-P and E8-E remain approved, without changing V1 scope. The user resumed on 2026-09-25. Step 3 is open: E1 Stories 1.1–1.4 and E2 Stories 2.1–2.12 are approved; E3 Stories 3.1–3.15, its coverage summary and the incorporated accessibility-test clarifications are approved. E3 planning is complete. The owner paused work before E4, the next continuation point; E4 has not started. No implementation, readiness check, provisioning, deployment or BMAD Spec is authorized in this step.

The approved PRD contains 25 functional requirements and four quality groups. Explicit later UX decisions supersede affected PRD wording; adopted AD-1–AD-14 bind implementation. Older discovery questions do not reopen adopted decisions. Requirement allocation and the formal delivery boundaries below are approved. Candidate smaller slices remain planning material, not formal stories.

Current capacity decision: the project is highly prioritized and the owner guarantees more than 40 hours, but has no reliable remaining budget. Capacity and delivery time are unresolved. Neither 40 nor 160 hours is an available planning budget; the old PRD range is historical context, not a current commitment. Do not defer requirements without a separate explicit owner decision. This uncertainty does not block epic design.

Sources: [PRD](prds/prd-IBE160-2026-09-21/prd.md), [DESIGN](ux-designs/ux-IBE160-2026-09-22/DESIGN.md), [EXPERIENCE](ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [Architecture Spine](architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [development log](../../Docs/development-log.md). Input paths are relative to this file. The identical brief.md alias is not a second requirement source.

## Requirements Inventory

### Functional Requirements

The following is the complete PRD section 6 extraction, retained for traceability. It is historical baseline text where the explicit supersession register below applies; do not implement superseded values from this extraction.

### 6.1 Access and Preparation

**FR-1 — Private access.** Provide private sign-in remembered for 14 days on the pilot tablet and explicit logout. Expiry alone must not interrupt an active shift or force mid-shift sign-in; request renewed sign-in between shifts before starting another shift when the remembered period has expired. This does not bypass explicit logout or access revocation. Protect documents, records and reports from unauthorized access. Instructor access must not expose operational records. No public registration. Authentication implementation is downstream work under B-3. Realizes UJ-1 and UJ-2.

**FR-2 — Import and confirmation.** After PDF upload, preview the interpreted shift for explicit confirmation before use. Permit direct editing and addition of omitted trips/activities, then review the corrected result. Unknown fields and extraction failures must not silently become authoritative values. No free-text/AI correction interpreter is required. Realizes UJ-1.

**FR-3 — Timetable completion.** Accept route, starting stop, ending stop and departure time for a trip, using the shift's applicable service date to find timetable details. Cover lines 20, 24, 28 and 42 initially. Multiple matches require selection; no match first produces a warning, then permits retention of entered details with missing-stop status. A source failure is distinct from no match. Never silently substitute another trip.

If a trip lacks a usable stop list, first attempt recovery from available timetable data for the applicable trip and service date. Only use a supported match; route similarity alone is insufficient. If recovery fails, retain known trip details and show `Stoppinformasjon mangler`. Disable automatic stop progression for that trip, and allow manual completion or abortion and selection of the next activity when the interaction rules permit. Record these actions as manual. Do not fabricate stops or claim GPS-confirmed final-stop arrival. Timetable recovery does not assume a new online retrieval is possible during an outage.

**FR-4 — Other activities.** Allow activity type, start time and end time, plus optional location, to be entered/corrected. Preserve known locations and timing. Do not invent missing locations or assume meanings for unexplained PDF codes. For example, `Travel to` in the supplied context is movement using the assigned bus, not pilot-car transfer. Validation and overnight date/time interpretation are assigned to B-2/B-4; preserve the confirmed service date and activity sequence rather than silently changing them.

**FR-5 — Day overview and assignment.** Show reporting time, trips, breaks, known start/end locations, bus changes and transfers. Allow manual actual bus-number entry before duty and correction on physical replacement. Keep physical bus, vehicle duty and trip identity separate; PDF `Vogn` must not automatically become the bus number.

### 6.2 Actual Trip and Stop Progression

**FR-6 — Active trip.** Automatically select the first trip using the confirmed shift, position and current time together. If selection is ambiguous, present the candidate trips and require the user to choose before starting the trip's driving view. Allow manual override when an automatic selection is wrong, through trip-selection controls that require standstill, subject to the startup/GPS-loss exceptions in FR-16. Show route and destination of the actual active trip and distinguish direction at shared stops. A delayed trip remains active until actually ended; the next scheduled time alone cannot trigger a change. Missing position evidence must not be presented as a confident match. Detailed sensing criteria are deferred to B-2; missing-data product behavior is tracked in A-2.

If automatic selection produces no candidate, allow direct selection of a trip from the confirmed shift, subject to the agreed interaction rules and their startup/GPS-loss exceptions. Apply FR-3 timetable recovery and missing-stop handling where needed. An absent automatic match must not prevent the user from selecting an existing confirmed trip.

**FR-7 — Three-stop view.** At a stop show previous/current/next; between stops show the departed stop and next two. Do not label an upcoming stop as confirmed current location. Advance on passing without stopping too. At route boundaries do not fabricate unavailable stops; exact empty-slot treatment is a UX detail.

**FR-8 — Progression accuracy and diversion recovery.** With reliable positioning, advance no later than 100 metres travelled after passing/leaving a stop, not a 100-metre proximity radius. With a supported diversion sequence show actual stops; a general notice alone does not establish that sequence. Without it, recover at a later recognized stop on the active trip, even two or ten stops ahead. Do not invent replacement stops or change lines based solely on proximity.

**FR-9 — Uncertainty and manual stop control.** Retain last confirmed progress with explicit uncertainty when position is unreliable; do not claim the bus is still there. Allow arbitrary correct-stop selection and resume progression at full standstill, subject to the startup/GPS-loss exceptions in FR-16. On GPS loss, show direct previous/next-stop buttons, permitted at driving speed as the explicit user-selected exception. Hide them and realign automatically within the active trip when reliable GPS returns. Internet loss alone does not activate them.

**FR-10 — Between-trip displays.** Show `Siste stopp` for 10 seconds after registered final-stop arrival before transitioning to deadhead travel, a meal break (with or without relocation), a bus change, a pilot-car transfer or depot return. Apply the same rule to GPS-confirmed and manually indicated final-stop arrival. A same-route return trip is the exception described below. Display transitions are not confirmation of physical actions or actual break time.

| Situation | Behavior |
|---|---|
| Same-route return | End-of-line indication remains until the bus reaches the starting stop again with reliable GPS. During GPS loss, pressing `Next stop` once more from the final stop starts the return trip. No automatic ten-second transition to the return trip. |
| Relocation to another trip | After the 10-second indication, show `Tomkjøring`, with the next starting-stop name beneath. |
| Meal break without relocation | After the 10-second indication, show `Lunsj` or `Matpause`; do not label it as deadhead travel. |
| Deadhead followed by meal break | `Siste stopp` for 10 seconds after arrival; then `Lunsj` or `Matpause` / `Tomkjøring` / first stop after the break. |
| Bus change or pilot-car transfer | `Siste stopp` for 10 seconds, then centered `Bussbytte` or `Pilotbil`. |
| Depot return at shift end | `Siste stopp` for 10 seconds, then `Returner` / `til` / `Depot` on three lines. |

The exact meal-break label is deferred to UX. The ten-second transition applies to every non-return activity listed above, regardless of GPS or manual progression. Travel time is not classified as break time by this display.

**FR-11 — Operational changes.** At full standstill, subject to the startup/GPS-loss exceptions in FR-16, provide a submenu for next-trip selection, current-trip interruption, fault-related physical bus change and early shift termination. Include corrections in the summary; do not label skipped/interrupted work completed. Illness is an example, not a requirement to store medical information.

### 6.3 Disruption Information

**FR-12 — Retrieval and relevance.** Automatically retrieve relevant Svipper planned notices. During active shifts, target a normal check every two minutes, subject to source validation. Before duty show shift-relevant information; during driving limit the view to the current trip/activity. Next-trip notices may appear upon arrival at the last stop, independently of the 10-second activity transition. Match applicable route/direction, affected stops/area and validity where available; ambiguous relevance is not certainty.

**FR-13 — Provenance and freshness.** Expose the original source, validity and source update time where supplied, and distinguish them from last successful retrieval. If the source provides no update timestamp, keep the notice visible with `Kildens oppdateringstid er ukjent` alongside the assistant's last successful retrieval time. Do not substitute retrieval time for a missing source timestamp. Other missing metadata remains unknown. A successful fetch does not establish current, complete or real-time source content. Retained notices and limited deadhead coverage must not imply all-clear conditions. Source-dependent freshness qualification is downstream validation under B-1; it must preserve these explicit unknown/stale states.

**FR-14 — Notice lifecycle.** Keep headings visible; open content on demand. Both new and changed notices use bold text until opened; opening marks that version seen and removes the bold emphasis. Changed notices also use color-coded text. A subsequent update restores bold emphasis until the updated version is opened. Retain ended notices with strikethrough for 10 minutes after the assistant registers their ended status, then remove them from the overview. This does not remove their record from the daily summary. Disappearance from a feed is not proof of resolution. Detailed visual treatment is assigned to B-4.

Preserve notice identity, seen-version state and prior receipt throughout the active shift, including internet outages and app/tablet restarts. An unchanged notice must not become new or unseen merely because it is retrieved again or the assistant restarts; genuinely updated content still regains emphasis. Source identity/version evidence must be verified rather than assumed.

If a previously retrieved notice disappears from the source without confirmed ended status, retain it with `Status usikker – sjekk originalkilden` and source access. After checking the original source, the user can manually remove it from the overview when interaction rules permit. Record the manual removal in daily-summary correction evidence; do not label it a source-confirmed ending or erase its display history. The action is distinct from automatic ten-minute removal of a confirmed ended notice. If the source later supplies a changed version, show it again as updated, with color coding and bold until opened, without a chime. An unchanged version remains hidden for the rest of the shift, including after restart or retrieval recovery.

**FR-15 — Audio.** A short discreet chime occurs only for a new notice arriving during, and relevant to, the ongoing trip. Changes, unchanged fetches and previously retrieved notices becoming relevant at transition remain silent. Sound never opens content or bypasses restrictions.

### 6.4 Movement Restrictions

**FR-16 — Movement and interaction policy.** Apply the agreed policy below. It is a conditional restriction with explicit availability exceptions, not guaranteed prevention of interaction during motion. Source-link use must not bypass it.

| Condition | Message behavior |
|---|---|
| Reliable speed ≤6 km/h | Opening allowed. |
| Reliable speed >6 km/h | Immediately block further opening; already-open content collapses after approximately 30 seconds. |
| GPS lost after speed >6 km/h | Keep locked for five minutes, then unlock if still absent. |
| GPS lost after speed ≤6 km/h | Remain unlocked. |
| Startup without valid speed | Opening allowed. |
| Reliable speed returns | Reapply the 6 km/h rule immediately, even after timeout-based unlocking. |

Unknown speed is not standstill. GPS-loss stop buttons are a separate driving-speed exception. At startup before the first valid GPS speed measurement, controls are freely accessible without a movement lock or a five-minute wait, including arbitrary stop selection and the operational-change submenu. Once valid speed is available, normal restrictions apply: arbitrary stop selection and the operational-change submenu require full standstill, while messages follow the 6 km/h rule. A subsequent GPS outage permits normally standstill-only controls after five minutes even though standstill cannot then be verified. Startup without a first measurement is therefore distinct from loss of a previously available signal. Free startup access does not bypass sign-in, confirmations or other non-movement requirements.

During GPS loss, advancing manually to the final stop establishes manually indicated final-stop arrival. If the next scheduled trip is the return journey on the same route, pressing `Next stop` once more from the final stop starts that return trip; merely selecting the final stop does not start it. For other next activities, show `Siste stopp` for 10 seconds and then the applicable special activity view. This advances the display, not proof that the next physical activity is complete. Preserve the manual origin in summary/correction evidence rather than describing the transition as GPS-confirmed.

Timers follow the current state. Cancel a pending thirty-second message collapse if reliable speed falls to 6 km/h or below; a later new transition above 6 km/h starts a fresh interval if content is open. Reliable GPS recovery cancels and resets the five-minute outage timer and immediately restores normal movement restrictions. A subsequent loss starts a fresh five-minute interval for controls whose outage policy requires waiting. An old timer must never unlock controls or close content contrary to the current state. Mere receipt of an unreliable reading is not reliable recovery; measurement qualification is downstream validation in B-2.

### 6.5 Continuity and Failures

**FR-17 — Internet loss.** Once the whole shift has been loaded and confirmed, preserve its overview, all available trip stop lists and previously retrieved notices without internet. Support GPS progression where positioning is usable, transitions to later trips/activities, manual corrections and the daily summary across the entire loaded shift, including after app closure or tablet restart. Apply existing interaction restrictions and missing-stop fallbacks. New disruptions and other source updates wait for connectivity; the application must not imply that unavailable or never-loaded information is present. Show a prominent top notice with a yellow exclamation triangle and explanatory text about lost connectivity and updates. Retained data must not look freshly verified.

**FR-18 — Recovery and partial failure.** Restored internet triggers automatic refresh. Update the notice to say connection restored but synchronization pending. Keep the missing-update warning until retrieval succeeds. Show source-specific failures locally, distinct from traffic notices. A failed refresh is not indefinitely described as in progress.

**FR-19 — No initial data.** If the first disruption fetch fails, show `Avviksinformasjon utilgjengelig – sjekk originalkilden` with a source link, never an empty-list implication of no disruptions. The external source may also be unreachable; interaction restrictions still apply.

**FR-20 — Active-shift recovery.** Restore an active, fully loaded shift after closure/restart without reuploading the PDF or reentering bus number, including while offline. Preserve manual corrections and seen-notice state. Resume the whole-shift offline capabilities in FR-17, not only the trip that was active before interruption. Preserved position/notices do not become fresh merely by recovery. Confirmed completed shifts cannot resume; this is recovery from interruption only.

### 6.6 Completion and Data Lifecycle

**FR-21 — End or abort.** At final depot arrival, offer a red `Avslutt skift` button, with `Er du sikker?` confirmation. Also make `Avslutt skift` available in the submenu when depot arrival cannot be detected, including GPS loss at the depot, under the same confirmation and interaction rules. This permits normal completion without falsely marking the shift aborted. Intermediate depot visits are not automatic completion. Cancel leaves the shift active. Early termination follows the same confirmation/summary flow with aborted status. Confirmed ended shifts cannot resume.

**FR-22 — Daily summary.** Include completed trips/activities, relevant notices displayed, manual corrections and data-source problems; distinguish skipped, aborted and uncertain work. Count a passenger trip as completed when the assistant registers arrival at its final stop, unless the trip was manually aborted. Use position and timing together to infer completion of other activities, including meal breaks, bus changes and pilot-car transfers. Scheduled end time alone is insufficient. When GPS or the activity location is missing and completion cannot be established, show `Gjennomføring usikker` and allow manual confirmation in the summary. Preserve that the confirmation was manual in correction evidence; it does not resume the completed shift. These signals do not independently verify physical handover or other unobserved actions. At the bottom show `Takk for i dag` and a day-informed affirmation, without requiring AI generation or driver scoring. Permit return to the main menu ready for the next shift. Automatic-completion sensing thresholds are assigned to B-2; uncertain completion keeps the explicit manual-confirmation fallback.

**FR-23 — PDF export.** Require user-initiated PDF export; using it is optional. The private PDF may retain actual operational identifiers and is not automatically uploaded/published. Mark demo exports accordingly. CSV is optional if time permits. Export does not require permanent in-app history.

**FR-24 — Retention.** For both completed and aborted shifts, retain associated application data for seven days from confirmed completion or abortion, then automatically delete all shift-associated data: the summary, uploaded shift document, retained position/movement data, corrections and notice history. If a shift is never explicitly ended, delete the same data seven days after its planned end time, without marking the shift or its activities completed. Reopening or exporting a summary does not restart the retention period or resume the shift. Do not collect extra raw tracks simply to retain them. User-held exported PDFs and the pilot user's external notes are outside application cleanup and are sufficient pilot evidence. A separate retained anonymized test/quality dataset is deferred beyond the course MVP; there is no pilot-archive exception to deletion of application shift data. No driver performance profile.

### 6.7 Instructor Assessment

**FR-25 — Repeatable desktop demo.** Provide separate test access, fictional shift, simulated progression and speed without physical GPS. Allow restart and new-notice, internet-loss and GPS-loss scenarios. Keep simulation explicit and isolated from operational data. Demo restart is not real-shift resumption. Keep access available for Christmas assessment; exact end date is open. Realizes UJ-2.

### NonFunctional Requirements

**NFR-1 — Tablet usability.** Prioritize brief-glance route, destination, stops and relevant headings. Express important status with text/symbols as well as color. Verify legibility and control usability on the mounted tablet, without requiring the pen. Light/dark treatment and measurable visual checks are assigned to B-4 before pilot use. Continuing the shift must not depend on operating the website while driving.

**NFR-2 — Information integrity.** Distinguish planned, observed, manually corrected, stale, unavailable and simulated information across displays and reports. Never manufacture metadata, stop sequences, completion or coverage. Preserve useful correction/failure evidence without unnecessary movement tracking.

**NFR-3 — Privacy and access.** Protect all records and instructor separation, not merely menu visibility. Anonymize exact shift, bus, vehicle-duty and trip identifiers in project documentation and any pilot evidence prepared for publication or assessment. The private PDF exception does not authorize identifiable publication. Private exported PDFs and external notes support evaluation; a separate in-application pilot-quality archive is outside this MVP. Deletion and access outcomes must be verifiable without prescribing implementation.

**NFR-4 — Target-environment reliability.** Validate actual position/speed, foreground operation, tethering loss/recovery and sound on Lenovo/Brave. Simulations cannot substitute. Raise unavailable capabilities as blockers rather than silently substituting scheduled or simulated progress.

### Additional Requirements

The architecture source remains normative in full. The table assigns implementation responsibility rather than allocating an architecture decision exclusively to one epic. E8 verifies combined evidence; it does not postpone obligations introduced by earlier epics.

| Source | Binding implementation work | Primary epic / contributing epics |
|---|---|---|
| AD-1 | Modular monolith; real import/transit/disruption ports; inward dependencies; configured pilot geography; no speculative integrations. | E1 / E2, E4, all domain work |
| AD-2 | Atomic IndexedDB state plus outbox before UI acknowledgement; verified nonpersonal assets; separate plan/data/assets readiness; whole prepared-day operation and local PDF; eviction limitations and explicit competing-client reconciliation. | E5 / E1 foundations; E2 bundles; E3, E4, E6, E7 consumers |
| AD-3 | React/Vite/TypeScript client; Python/FastAPI validation and OpenAPI; one TypeScript operational engine. Official React/Vite starter is the E1 first-story seed. Full Stack FastAPI template is reference only, without inherited registration/auth/admin/deployment scope. | E1 / all epics |
| AD-4 | PostgreSQL 18 for development, pilot and integration evidence; ownership/uniqueness/revisions/atomic writes enforced in DB; bounded typed JSON; no SQLite integration substitute. | E1 / E2, E4, E5, E7 |
| AD-5 | Six contracts; immutable batches, one stable batch in flight per day; authorization/expiry before deduplication; receipt lookup independent of old writer authority; atomic changes/dedup/receipt/revision; same-ID different-content rejection and cross-batch event dedup; source polling never changes operational revision. | E5 / E1 transactional foundation, all state writers |
| AD-6 | Backend text/OCR behind import port; qualify pdfplumber/Tesseract, render every relevant scanned page; editable resumable interpreted draft; manual failure path; explicit confirmation. All own/linked originals, browser previews and processing copies transient; cleanup on success/failure/cancel/crash, no raw OCR archive. | E2 / E6 linked-plan UX, E8 evidence |
| AD-7 | Targeted Entur queries prepare the whole day; unique evidence-supported matching, explicit ambiguity/no-match/source failure; do not mistake journey-planner suggestions for a catalogue. Central candidate SX/TRO polling around two minutes; persist baseline/cursor, resolve pagination and separate deltas/full absence/partial/failure. Qualify coverage, IDs, limits, updates/endings and original links. | E2 transit; E4 notices / E5 recovery, E8 real-source qualification |
| AD-8 | Backend source truth versus local day/version seen/acknowledged/hidden state; material updates unread and silent; identical polls/context switches not new versions. Distinguish closure/expiry/uncertain disappearance; ordering and sparse closures/multiple validity intervals; no stale resurrection. Closure removes active markers immediately, keeps struck-through entry ten minutes from persisted first registration, then summary only. | E4 / E5 persistence, E7 history |
| AD-9 | One UI-independent operational state machine; position and speed quality separate; no schedule/proximity-only proof; manual authority; travel-after-passage target; genuine startup versus persisted outage. Role/plan/block/pin atomicity; return-trip/final-stop/missing-list rules; end/abort terminal. | E3 / E6 role extensions, E5 recovery, E7 terminal review |
| AD-10 | Provisioned pilot account, password hashing/rate limiting, opaque server session and secure host-only cookie, CSRF/exact origin. Fixed 14-day ordinary authorization, bounded owner/client/day grant for already-active continuation; limited post-end settlement. Logout/revocation and offline pending revocation before private traffic; same-owner fresh login recovery. Public fictional demo on separate origin with no private authority. | E1 / E5 continuation/logout recovery, E8 demo and access qualification |
| AD-11 | Web Locks within origin; server epoch/revision between devices; no timeout transfer. Planned drain and atomic transfer with day-grant rebinding; explicit emergency transfer with last-server-state warning; verified recovery revision; preserve old-client pending work for explicit resolution, never automatic replay under new authority. | E5 / E1 identifiers/authorization |
| AD-12 | Non-sliding draft expiry seven days after creation or earlier with day; combined-day expiry seven days after actual end/abort or planned final end if never ended. Delete every private copy, including outbox/conflicts/receipts/grants; no historical private backups. End-of-day linked-plan trimming preserves only accompanied evidence. Pending-payload trimming uses minimal checkpoint, payload-free receipt reconciliation, retired IDs and atomic fencing/closure; retirement is not acknowledgement. Expiry guards deny late access/re-upload before asynchronous cleanup; exported user PDFs outside cleanup; accepted device/volume-loss risk. | E7 lifecycle integration / E1 expiry guards; E2 transient import/drafts; E5 settlement protocol; E6 accompanied evidence |
| AD-13 | Portable five-service Compose on Windows desktop; stable private and separate demo origins, named Tunnel, owner-only Access before publishing private route and independent app login; JWT validation, no exposed private ports/demo relay. Actual Access-expiry preflight and renewal distinct from offline readiness/connectivity; gate failure pauses updates without forced driving login. Private no-store/edge-cache bypass, provider handling qualification, secrets/network isolation, one OCR job, resource/noise and restart-after-sign-in evidence. | E8 delivery/qualification / E1 access boundaries, E2 processing, E5 gate-failure behavior |
| AD-14 | Separate build/API/event/local-schema/domain revisions; verified staged successor and active-day coherent build through offline/Access-expired close/reopen. Compatible backend contracts through actual data expiry, not arbitrary release count. Non-destructive coordinated migrations, immutable batches and pending logout preserved; missing-assets recovery without clearing private work; rollback only with compatible storage. | E5 client/recovery compatibility / E1 version foundations, E8 release/migration evidence |

Contract ownership: ImportDraft → E2; Workday/PlanRevision → E2 with E6 linked-context extensions; OperationalState → E3 with E6 roles; NoticeVersion/SourceStatus → E4; OfflineBundle → E2 construction/E5 readiness and recovery; SyncBatch/SyncReceipt → E5 with E1 foundations. Preserve opaque IDs, source-namespaced external IDs, separate plan/server/source revisions and writer epoch, UTC instants, local service date/IANA timezone and explicit dates across midnight. API accepted/already_applied, 409 conflict/retired, 422 validation/schema, 401/403 authority and 410 expiry outcomes follow the spine; Access HTML/redirects are never receipts or app assets.

Fullstack/database is a user requirement in PRD section 2, not an inferred institutional stack mandate. The public static demo cannot alone evidence the private React → FastAPI → PostgreSQL application. Architecture-selected libraries/tools not yet locked remain story-level choices; qualifying a candidate is not a new architecture approval.

### UX Design Requirements

Derived IDs below provide traceability for the approved UX contract; they do not introduce new scope. Source anchors refer to EXPERIENCE (X) and DESIGN (D). Every numbered item has a primary delivery owner; shared consumers retain the same behavior.

| ID | Actionable requirement | Source section | Owner |
|---|---|---|---|
| UX-DR1 | Implement Day A/Night C semantic palette, text/symbol status and verified foreground pairings; preserve warning outline, not yellow alone. | D Colors | E1 tokens; E3 integration; E8 device verification |
| UX-DR2 | Implement approved typography, spacing, control geometry and long-name/text-enlargement behavior; do not shrink critical text to fit. | D Typography, Layout & Spacing | E1 tokens; E2–7 screens; E8 verification |
| UX-DR3 | Access/navigation: private main menu, explicit logout, active-day recovery, no public registration and prominent no-login fictional demo entry. | X Information Architecture, Component Patterns | E1 / E5, E8 |
| UX-DR4 | Shared import review editor for PDF/JPG/PNG with side-by-side transient source, uncertainty, direct correction, missing activities and explicit confirmation; interpreted edits resume, originals must be reselected. | X Upload/shared review; D Import review editor; AD-6 | E2 |
| UX-DR5 | Activity/trip selector distinguishes route, direction, service date and time; ambiguity/no match/source failure distinct; non-passenger type/times/optional place. | X Component Patterns | E2; E3 active choice |
| UX-DR6 | Shift overview shows reporting time, chronological activities, known places, physical bus separate from vehicle duty and all shift-relevant notices. | X Shift overview | E2 / E4 |
| UX-DR7 | Shift part header has each part's own reporting time/depot; gap is not inferred rest, transfer or final completion; one combined day. | X Split shifts and revisions | E2 |
| UX-DR8 | Shift revision review exposes file/manual paths, target plan and whole/part/additions scope; compare added/changed/proposed-removed/unchanged future activities; resolve ambiguity before confirmation. Preserve performed evidence, active manual trip and all out-of-scope plans. | X Split shifts; Revision ownership | E2 / E6 linked links |
| UX-DR9 | Shift disruption list keeps distinct incidents separate, shared incident once with all supported line/trip/time associations and attached source metadata. | X Shift disruption list | E4 |
| UX-DR10 | Driving focus emphasizes current stop at stop, next between stops; route/direction/destination persist, personal import details excluded. | X Driving focus; D Typography | E3 |
| UX-DR11 | Three-stop sequence is vertical, upcoming first: later/next/CURRENT at stop, later/NEXT/departed between; no previous at-stop baseline. Boundaries use dash and explicit no-more/no-previous label, distinct from unavailable data. | X Three-stop sequence; Validation | E3 |
| UX-DR12 | Persistent clock remains visible on tablet screens without becoming completion evidence. | X Persistent clock; D tokens | E3 / E2, E6, E7 |
| UX-DR13 | Always-visible driving Menu contains trip choice and Skiftdetaljer; disabled text/reason and GPS countdown remain visible. Stop-sequence tap uses the same arbitrary-selection policy. | X Driving menu, Operational role states | E3 |
| UX-DR14 | Driver detail/source/acknowledgement requires reliable standstill; motion immediately collapses details. Genuine startup before first valid speed is exempt; later GPS loss waits five minutes, including after zero/low speed; persist timer/history across restart and reset only on qualified recovery. | X Approved movement policy | E3 / E4, E5 |
| UX-DR15 | Direct GPS-loss previous/next stops remain allowed in motion; network loss alone does not show them; reliable return hides and realigns within chosen trip. | X Stop correction controls | E3 |
| UX-DR16 | Trip transition/correction: permitted menu choice and undo, one/two-tap goal including menu, distinguish overlapping lines; manual pin persists until actual completion or explicit context change, never time/proximity. | X Corrected trip selection; Explicit tracking-context changes | E3 / E6 |
| UX-DR17 | Operational-change controls distinguish interruption, skipping, physical replacement and ending; preserve provenance and never infer completion. | X Operational-change controls | E3 / E7 end action |
| UX-DR18 | Between-activity display: ten-second final-stop state except same-route return; Matpause preserves paid/unpaid/unknown source facts, relocation not break time. Reguleringstid and next activity; centered Bussbytte/Pilotbil and two-line Returner til/Depot without blue rail. | X Between-activity transitions; D Layout | E3 |
| UX-DR19 | Notice heading/detail preserves version-specific unseen/changed/ended treatment, original validity/source/fetch times and uncertain missing metadata, independently of acknowledgment. | X Notice heading and detail | E4 |
| UX-DR20 | Staged planned-stop warning: triangle after name two ahead; prominent heading only after departure from preceding stop; retain through dwell and clear after onward passage, preserving source lifecycle/history. | X Staged stop-related disruption display | E4 / E3 progression |
| UX-DR21 | Newly received applicable acute notice displays inline immediately with stop context; two important headings simultaneously, no carousel/modal/focus theft. This does not promise acute source coverage. | X Newly received acute disruptions | E4 |
| UX-DR22 | Stationary Registrert and optional forgiving swipe dismiss only selected version's prominence; retain marker and overview, unchanged content stays dismissed across restart. Cancel incomplete dismissal on motion; updated version reconsidered without chime. | X Notice acknowledgement while stationary | E4 / E3 movement policy |
| UX-DR23 | Data status: prominent connectivity warning and local source failures; returned connection is pending until successful retrieval; stale, unknown, missing and simulated states distinguishable. | X Data status, State Patterns | E5 / E4 source status |
| UX-DR24 | Theme control: adjacent to Menu, icon plus separate Auto hit area, always enabled. Persistent manual Day/Night across sessions/shifts until explicit Auto; Auto underline and accessible selection; unavailable Auto preserves appearance/preference and explains unavailability. | X Theme control; D tokens | E3 |
| UX-DR25 | Keep active-trip screen awake where supported; qualify browser GPS/speed, sound, wake and automatic-theme trigger without assuming native/background/sensor guarantees. | X Interaction Primitives; Responsive & Platform | E3 / E8 qualification |
| UX-DR26 | Mentor assignment/role: review own plan first, link separately confirmed person plans; permanent FADDER/INSTRUKTØR badge and visually separate own/linked panels. Imported copies private within own account. | X FADDER and INSTRUKTØR assignment scope; D components | E6 / E2 plan identity |
| UX-DR27 | FADDER accompanies one same person's whole shift during fadder assignment; own driving remains solely own plan; no fictitious person or classroom/office fadder activities. | X FADDER and INSTRUKTØR assignment scope | E6 |
| UX-DR28 | INSTRUKTØR supports selected portions, several person changes and returning to same person, classroom/office and valid no-accompaniment day. Explicit block/person confirmation; no schedule-only handover or inherited pin/evidence. | X FADDER and INSTRUKTØR assignment scope | E6 |
| UX-DR29 | Mentor driving/role switch keeps guiding controls open; Jeg kjører applies driver restrictions before any further choice. Planned own-trip selection contains only own trips. Acute FADDER takeover retains linked current trip/progress/pin; Jeg sitter på igjen explicit and permitted. | X Acute FADDER takeover, Role states | E6 / E3 shared engine |
| UX-DR30 | Revised linked plan leaves affected accompaniment links visibly unresolved for explicit repair; matching never crosses target plan. | X Revision ownership and linked contexts | E6 / E2 revision engine |
| UX-DR31 | Recover role, assignment, person/plan/block, pin, takeover and outage history atomically. Incomplete recovery never infers unrestricted guidance or genuine-startup exemption. | X Role and context recovery | E6 / E5 storage/recovery |
| UX-DR32 | End-shift confirmation red action and cancel-preserving dialog; normal fallback in menu, final own-day only; end/abort terminal and intermediate depot/gap/block never ends day. | X End-shift confirmation | E7 / E3 transitions |
| UX-DR33 | Summary/export distinguishes completed/skipped/aborted/uncertain, displayed notices, corrections and source issues. Initial completion review can manually confirm uncertainty; later retained entry is read/export with date/expiry. | X Initial and retained summary permissions | E7 |
| UX-DR34 | Closing message Takk for i dag plus eligible varied factual affirmation; avoid previous day's variant where possible, neutral fallback, no invented success/scoring/AI or permanent history; demo rotation isolated. | X Latest navigation and closing decisions | E7 |
| UX-DR35 | PDF document is user-initiated local export, portrait A4 with outcomes/provenance/page numbering and demo marking on every demo page, not a tablet screenshot or two-page limit. Export failure preserves ended summary and retry without extending expiry. | X PDF document; Recoverable defaults; D tokens | E7 / E8 demo |
| UX-DR36 | Mentor summary/PDF retains only actually accompanied evidence, separates own planned activities and actual takeovers, never completes another person's remainder. Show file-deletion explanation at import and own-day expiry; discard unaccompanied context at own-day end. | X Accompanied-person imports and summary scope; AD-6/12 | E6 evidence / E7 output and trimming |
| UX-DR37 | Instructor simulation controls: separate no-login origin, fictional shifts/speed/progression, repeatable restart/new-notice/network/GPS scenarios and explicit simulated exports; load failure cannot fall back to private records. | X UJ-2, Instructor simulation controls | E8 |
| UX-DR38 | Keyboard order follows reading order; action labels, selected/disabled state and no hover/color/swipe-only essential operation. | X Accessibility Floor | E1 shared controls / E2–8 |
| UX-DR39 | Dialog focus moves in and returns to invoker; cancel preserves data; movement-triggered closure leaves no focus in hidden detail. | X Accessibility Floor | E3 / E2, E4, E6, E7 |
| UX-DR40 | Accessible stop roles and associated warning descriptions; meaningful state announcements without each poll/second, focus theft or repeated alarms. | X Accessibility Floor | E3 / E4, E5 |
| UX-DR41 | Tablet landscape and ordinary-PC adaptation, long names, simultaneous notices, text enlargement, sunlight/night/tunnel contrast and touch/glove checks. Mock frame sizes are not product breakpoints; portrait/breakpoints remain implementation work. | X Responsive & Platform; D Layout | E8 evidence / E2–7 implementation |
| UX-DR42 | Failed/cancelled file selection or extraction preserves confirmed plan and known unconfirmed draft, allows manual correction/retry; camera permission not required for existing image. | X Recoverable interaction defaults | E2 |
| UX-DR43 | Matching-service failure preserves entered date/facts/manual edits, distinguish from successful no-match; retry non-destructive. | X Recoverable interaction defaults | E2 |
| UX-DR44 | Unavailable capabilities explained at affected surface, only approved fallback; never operational substitution of simulated data. | X Recoverable interaction defaults | E3 / E2, E4, E5, E8 |
| UX-DR45 | Optional support information is outside V1; do not create speed/weather/meeting widgets or treat optional four-stop layout/lunar phase as adopted baseline. | X Optional support; D Components | Deferred, no V1 implementation owner |

### Supersession register

| Older wording | Governing adopted clarification | Epic |
|---|---|---|
| FR-2 PDF only | UX shared PDF/JPG/PNG import, plus AD-6 transient originals for every plan, resumable interpreted drafts only. | E2 |
| FR-7 previous/current/next at stop | UX upcoming-first later/next/current at stop. | E3 |
| FR-10 Lunsj/three-line depot | UX Matpause and two-line Returner til/Depot. Ten-second and same-route-return semantics remain. | E3 |
| FR-16 <=6 km/h detail, thirty-second collapse, low-speed-loss unlocked | UX reliable motion means headings only/immediate collapse; any subsequent qualified speed outage uses five-minute exception. Genuine startup, direct stop arrows and theme exceptions retained; mentoring exception explicit. | E3, E4, E6 |
| PRD UJ-2 separate teacher login | UX/AD-10 separate public fictional demo without login; operational INSTRUKTØR is private and distinct. | E1, E6, E8 |
| FR-24 seven-day uploaded-original retention | AD-6 deletes all originals/processing copies after interpretation ends, fails or is cancelled, plus crash cleanup. Seven-day rules apply to permitted derived data/drafts as AD-12 defines. | E2, E7 |
| Earlier brief first-version speed limits | PRD/architecture defer speed/weather/meeting and routing; no V1 epic. | None |

These are settled decisions, not unresolved contradictions requiring renewed user approval.

### FR Coverage Map

Primary means ownership of the user outcome. Contributors build prerequisite/shared behavior; E8 holds qualification evidence, not duplicate implementations. Coverage is planning coverage only, not acceptance or test success.

| Requirement | Primary | Contributors / exact seam |
|---|---|---|
| FR-1 Private access | E1 | E5 active-day continuation/offline logout; E8 separate demo/Access evidence |
| FR-2 Import confirmation | E2 | E6 uses same engine for linked copies; UX-DR4/42; AD-6 |
| FR-3 Timetable completion | E2 | E3 runtime recovery from available data, then manual completion/abort if no stops; E5 downloaded data |
| FR-4 Other activities | E2 | E3 progression without false completion; E7 uncertainty review |
| FR-5 Day overview/assignment | E2 | E3 actual physical replacement; E4 day-relevant notices |
| FR-6 Active trip | E3 | E2 confirmed candidates; E6 tracking-context scope |
| FR-7 Three-stop view | E3 | UX-DR11 supersedes at-stop ordering |
| FR-8 Progression/diversion | E3 | E2 supported stop sequences; E8 measured <=100 m after passage |
| FR-9 Uncertainty/manual stops | E3 | E5 persistence; network loss never masquerades as GPS loss |
| FR-10 Between trips | E3 | E7 consumes outcomes, never treats display transition as physical completion |
| FR-11 Operational changes | E3 | E2 plan revision; E7 end/abort flow and evidence |
| FR-12 Retrieval/relevance | E4 | E2 whole-day identity; E3 actual context; E8 real retrieval qualification |
| FR-13 Provenance/freshness | E4 | E5 cached-state qualification; E7 report evidence |
| FR-14 Notice lifecycle | E4 | E5 exact-version persistence; E7 history; closure differs from expiry/disappearance |
| FR-15 Audio | E4 | E3 ongoing-trip context; E8 real browser sound check |
| FR-16 Movement policy | E3 | E4 details/source/dismissal; E6 role exceptions; E5 persisted history; UX governs |
| FR-17 Internet loss | E5 | E2 whole-day bundle; E3 local progress; E4 retained notices; E7 local PDF |
| FR-18 Recovery/partial failure | E5 | E4 source refresh success/failure, separate from outbox acknowledgement and network reachability |
| FR-19 No initial notice data | E4 | E3 source-link restriction; E5 honest availability status |
| FR-20 Active-shift recovery | E5 | E1 authorization; E2 plan/bus; E3 pin/progress; E4 notice versions; E6 role/block |
| FR-21 End/abort | E7 | E3 permitted entry/final-depot fallback; E5 terminal sync/settlement |
| FR-22 Summary | E7 | E3 outcomes, E4 displayed notice versions, E6 accompanied portions; evidence recorded at origin |
| FR-23 PDF | E7 | E5 offline assets/data; E8 labelled fictional export |
| FR-24 Retention | E7 | E1 access/expiry guards, E2 drafts/originals, E5 outbox/conflict/receipt trimming and fences, E6 linked context |
| FR-25 Desktop demo | E8 | Shared operational engine E3/E6 and presentation E2/E4/E7; fictional adapters only, no private backend |

| Quality requirement | Delivery ownership | Qualification |
|---|---|---|
| NFR-1 Tablet usability | E3 driving policy/composition; E1 shared tokens/accessibility; E2/E4/E6/E7 relevant surfaces | E8 mounted readability, touch/gloves, no required driving interaction |
| NFR-2 Information integrity | E2 import provenance; E3 observed/manual progress; E4 source facts; E5 freshness; E6 context; E7 reports; E8 simulation labels | Each epic tests its semantics; E8 cross-flow evidence |
| NFR-3 Privacy/access | E1 access; E2 transient originals; E5 authority/conflicts; E6 own-account linked copies; E7 deletion; E8 isolation/anonymized evidence | Cross-origin/backend isolation, all-copy expiry, publication anonymization |
| NFR-4 Target reliability | E3 sensors, E5 continuity, E4 retrieval/audio | E8 actual Lenovo/Brave/tethering; simulation never substitutes |

PRD non-numbered obligations: fullstack/database → E1 and private end-to-end evidence in E8; no installed app/public registration/permanent history → all boundaries; initial lines 20/24/28/42 → E2/E4/E8; real automatic retrieval cannot be replaced by manual/demo data → E4/E8. SM-1 information effort and SM-2 missed notices → E8 field observations/E4; SM-3 progression → E3/E8; SM-4 operational core → E2–7/E8; SM-5 assessability → E8. SM-C1 distraction and SM-C2 trust are recorded with field outcomes, not optimized away. Three actual varying workdays and external notes/private PDFs remain the evaluation plan; no new retained pilot archive.

PRD downstream register: B-1 → early E4 source qualification; B-2 → early E2 matching/E3 device; B-3 → adopted architecture plus E1/E5/E7 verification; B-4 → approved UX plus E8 mounted checks; B-5 → this capacity/slicing checkpoint and subsequent story estimates/evaluation protocol. C-1 exact deadline, C-2 assessment access end and C-3 instructor environment remain external facts to obtain from the owner; do not invent them. A-1–A-7 are resolved, with later UX/AD supersessions applied above.

## Epic List

All eight formal epic boundaries were explicitly approved at step 2. Each delivers a usable outcome in its own domain using earlier capabilities; an intermediate epic is not a claim of full V1 or pilot readiness. The table gives natural dependencies, not a rigid calendar: early qualification and fictional test fixtures start before final E8 verification.

| ID | User outcome | Dependency boundary |
|---|---|---|
| E1 | Private access and a persisted minimal working-day draft through client, backend and PostgreSQL | Starts the fullstack slice; includes basic local commit/outbox, authority/expiry and version identity, not a separate infrastructure-only project |
| E2 | Import, review, confirm and revise a complete own working day | E1; uses shared identity/contracts ready for linked plans |
| E3 | Follow actual trip/stops and change activities under movement policy | E2; source-independent progression fixtures can qualify behavior early |
| E4 | Receive relevant source-backed notices | E2 for preparation; E3 for driving relevance; source qualification starts before finished driving UI |
| E5 | Continue offline, recover and reconcile authority/conflicts | E1 foundations and E2–4 feature state; their local persistence is built with them, not deferred to E5 |
| E6 | Work as FADDER/INSTRUKTØR with explicit role/person/plan changes | E2–5 shared engines, no duplicate importer/state machine/synchronizer |
| E7 | End day, inspect evidence, export locally and expire data | E3–6 emit evidence; own-driver end/PDF slice can start before all mentor UI, final mentor acceptance depends on E6 |
| E8 | Demonstrate the solution and qualify/evaluate real-shift use with separate evidence | Demo/test fixtures and qualification begin early; completed system evidence aggregates E1–7 |

### Epic 1: Access and Recover a Private Working-Day Draft

The owner can sign in, create/save/reopen a minimal draft and log out through a working client/backend/PostgreSQL flow. Draft access, expiry and committed local changes work at delivery; this is not just scaffolding.

**FRs covered:** FR-1; foundational portions of FR-20/24. NFR-3 and AD-1–5/10/12 apply as introduced.

**Depends on:** none. **Boundary:** E2 adds import and confirmation; E5 adds full active-day recovery/conflict scenarios. Neither is required to save/reopen a protected draft. Use the adopted React/Vite seed without inheriting the unrelated FastAPI template features.

### Epic 2: Prepare and Revise a Confirmed Whole Working Day

The owner can import PDF/images, correct unknowns, resolve dated timetable matches, confirm own activities and physical bus, prepare available day data and review scoped revisions/split work without losing existing facts.

**FRs covered:** FR-2–5; preparation portions of FR-17/24. UX split-day and revision requirements apply.

**Depends on:** E1. **Boundary:** preparation is independently usable before live progression or notices. E4 later adds source-backed notices; their absence must not be presented as clear conditions. All original/draft cleanup and persisted plan revision rules are part of this delivery, not deferred to E7.

### Epic 3: Follow and Correct the Actual Trip Safely

The driver can select the actual trip, see qualified stop progression, correct uncertainty and follow final-stop/return/non-passenger transitions under the adopted movement rules. Evidence of manual and observed outcomes is recorded immediately.

**FRs covered:** FR-6–11/16; runtime fallback portion of FR-3 and outcome evidence for FR-22. NFR-1/2/4 apply.

**Depends on:** E1–2. **Boundary:** the active-driving domain can be exercised without notices, mentoring or a report UI. End/abort requests retain E7 ownership and cannot be presented as completed functionality before implemented. E4 consumes the shared movement/progression rules; no second movement engine.

### Epic 4: Understand Relevant Notices and Their Sources

The driver can inspect automatically retrieved day/trip-relevant notices with source, freshness, version lifecycle and approved heading/detail/acknowledgement/sound behavior, including initial and partial source failures.

**FRs covered:** FR-12–15/19; source-refresh portion of FR-18 and shared FR-16 restrictions. AD-7/8 apply.

**Depends on:** E2 for preparation and E3 for driving presentation. **Boundary:** actual retrieval and persistent notice-version behavior are delivered here; E8 does not supply a missing production adapter. Source qualification starts early and failure remains visible rather than replaced by demo notices.

### Epic 5: Continue a Prepared Day and Reconcile Recovery

The owner can continue the available prepared-day capabilities through network loss/restart, preserve explicit choices, resolve conflicts and transfer writer authority deliberately. Access expiry and compatible application recovery preserve bounded active-day continuation.

**FRs covered:** FR-17/18/20; active-day FR-1, retention protocol FR-24 and continuity of preceding features. AD-2/5/10/11/14 apply.

**Depends on:** E1–4. **Boundary:** basic local durability has already shipped with each feature. This epic completes cross-feature recovery, retries, authority/conflicts and coherent app boot. E6/E7 reuse these contracts as they introduce roles, terminal review and PDF; their later features are not prerequisites for recovery of E1–4. Full V1 offline acceptance includes their subsequent integration tests.

### Epic 6: Guide and Teach with Explicit Person and Driver Context

The owner can operate as FADDER or INSTRUKTØR with separate own/linked plans, accompaniment blocks, classroom/office work, own driving and explicit acute takeover/return. Recovery preserves the actual role and tracking context; accompanied evidence remains bounded to observed portions.

**FRs covered:** UX UJ-3/4 extend FR-2–11/16/20 and evidence/lifecycle aspects of FR-22/24; no invented new PRD FR number. AD-6/9/12 apply.

**Depends on:** E2–5. **Boundary:** use the shared import/revision/progression/sync engines. Required linked-data privacy and accompanied evidence are implemented when introduced, not left as a dependency on a future report screen. E7 consumes this evidence and integrates final-day trimming/settlement with its end flow.

### Epic 7: Close the Day, Inspect Outcomes and Export a Summary

The owner can explicitly end/abort one combined day, settle uncertain outcomes in the initial review, export a local PDF offline and later reopen only for reading/export until fixed expiry. Own and accompanied evidence remain distinct, and all-copy terminal cleanup cannot resurrect work.

**FRs covered:** FR-21–24; summary/PDF portions of FR-17/20 and UX closing/mentor-output requirements.

**Depends on:** E3–6 evidence and recovery contracts. **Boundary:** data protection/expiry obligations already apply in earlier epics; this epic completes the end-to-end day lifecycle, report and closure settlement. The own-driver report slice may be developed earlier, but final acceptance includes mentor evidence. No dependency on E8 to function.

### Epic 8: Demonstrate, Qualify and Evaluate the Delivered Assistant

The course assessor can repeat clearly fictional PC scenarios without private access or physical GPS; the owner can distinguish demonstrated capability, verified readiness for actual shifts and measured pilot outcomes.

**FRs covered:** FR-25; integrated evidence for FR-1–24, NFR-1–4 and the PRD success/counter-metrics, without moving their implementation out of owning epics.

**Depends on:** E1–7 for complete system evidence; fixture/scenario work and source/OCR/device qualification start earlier. **Boundary:** preserve E8-D (demonstrable delivery), E8-P (pre-pilot qualification) and E8-E (three actual workdays) as separate approved checkpoints, in that logical evidence order. E8-D alone is not full V1 acceptance or permission to use real shifts.

### Shared Components and Dependency Check

No application files exist to justify a file-level merge recommendation. Conceptual overlap is known: E2/E6 share plan/import/revision logic; E3/E6 share the state machine; E1/E5 share persistence/access; E5/E7 share terminal settlement. Keep one implementation per contract, extended in ordered slices. These boundaries represent distinct user outcomes and qualification risks, so retain eight epics rather than invent technical-layer epics.

References to later epics in the coverage map identify later consumers or system-wide verification, not permission to leave a current epic's required behavior broken. Each epic must deliver its own data safety, provenance, error paths and available-domain persistence. No placeholder UI may claim a future function works. Independent domain delivery does not mean the partial application is ready for real-shift pilot use; E8-P remains binding.

## Checkpoint Findings

| ID / type | Finding | Proposed disposition / decision status |
|---|---|---|
| F1 Coverage | All 25 FRs, four NFR groups and 14 ADs have explicit owners. UX adds substantial V1 beyond PRD IDs; 44 in-scope UX entries plus one deferred-scope marker are mapped. | Mapping approved at step 1; not evidence of implementation or exhaustive acceptance criteria. |
| F2 Missing seam in earlier overview | FR-3 runtime missing-stop recovery was implicit, and could be lost between import and driving. | E2 owns matching/preparation; E3 retries supported available timetable data then disables automatic progress and offers permitted manual completion/abort/next activity. No new requirement. |
| F3 Overlap | E1/E5 both mention persistence and synchronization; E5/E8 both mention release compatibility. | E1 establishes minimal transactions/access/version IDs. E5 owns retries/conflicts/continuity/coherent client boot. E8 owns release/deployment qualification evidence; no second sync engine. |
| F4 Missing seam | E7 cannot reconstruct notices, physical corrections or accompanied evidence after the fact. | E3/E4/E6 record provenance when events occur; E7 consumes it. Initial summary uncertainty review versus later read-only access explicit. |
| F5 Overlap / high risk | E2/E6/E7 all delete data; AD-12 closure trimming intersects immutable pending E5 batches. | Transient originals E2; accompanied scope E6; day/draft expiry integration E7; checkpoint/retired-ID/receipt/fence protocol E5. Add explicit combined closure/retry/late-request checks, no conflicting independent cleanup paths. |
| F6 Supersession | Old PRD movement, stop ordering, demo login and original-retention wording differs from accepted UX/AD. | Apply supersession register; no repeated product approval needed. |
| F7 Delivery distinction | Previous E8 mixed demonstration, readiness and three-shift evaluation. | Owner approved E8-D/P/E as separate checkpoints within E8; no ninth epic or removed V1 obligation. |
| F8 Capacity | E2, E3 and E6 need smaller implementation slices. Owner confirms high priority and more than 40 hours, but no reliable remaining budget or delivery time. | Capacity and delivery time unresolved; assume neither 40 nor 160 available hours. Estimate after early qualifications; no requirement deferred without a separate owner decision. |
| F9 Open implementation detail | Numeric sensor thresholds, Auto trigger, responsive breakpoints, DTOs/tables/indexes, migration tooling and precise failure copy remain story-level decisions. | Resolve/test before affected implementation; return to owner only if evidence requires changing adopted behavior/architecture. |
| F10 External/owner facts | Exact submission date, assessment access end/browser and realistic remaining capacity are not established. Evaluation timing/observation protocol remains to agree before field evaluation. | Need owner facts as available; no fabricated dates or assumption of 160 hours. These do not block requirement mapping. |

## Candidate Smaller Slices — Not Detailed Stories

These are provisional, testable slice boundaries requested by the user, without story IDs, estimates, acceptance-criteria sets or implementation authorization. Shared contracts, access, local commit, provenance, retention and relevant movement policy apply to every slice. Steps 1 and 2 are approved; step 3 now processes E1 first. E2/E3/E6 candidates remain unchanged until their sequential story checkpoints.

### E2 candidates

| Candidate | Observable check |
|---|---|
| Manual draft and explicit confirmation | Enter/correct a trip and non-passenger activity, reload, then confirm; unconfirmed facts never activate. Preserve service date and overnight ordering. |
| Text-PDF interpretation into the shared draft | Representative columns/page continuations produce reviewable fields/unknowns; cancel/failure never changes confirmed day; original cleanup verified. |
| Scanned PDF and JPG/PNG into the same draft | Every relevant scanned page processed; photo/screenshot uncertainty exposed; failure retains manual path and cleans processing copies. |
| Dated timetable matching | Unique/ambiguous/none/source-failure scenarios for pilot lines; choose among candidates, preserve known details if no supported match. |
| Whole-day overview and readiness | Reporting/activities/physical bus distinct from Vogn; all available trips/stops prepared, missing data identified separately from assets/authority readiness. |
| Split-day preparation | Separate reporting times/depots and gap; one final end reference, no invented transfer or premature completion. |
| Manual extra-work revision | Review and confirm remaining-work addition while preserving performed activities and active pin; cancel is non-destructive. |
| Scoped revised-file reconciliation | Whole/part/additions scope, ambiguous identity and explicit future removal; repeat import does not duplicate or silently delete work. Shared target-plan identity prepares E6. |

### E3 candidates

| Candidate | Observable check |
|---|---|
| Explicit active-trip choice and correction | Qualified initial match, ambiguous/no-candidate fallback, route/direction distinct, manual pin and permitted undo remain authoritative. |
| Driving display and theme | Correct at-stop/between-stop hierarchy, clock, boundaries and long names; persistent manual Day/Night, explicit Auto and unavailable fallback. |
| Movement access policy | Speed zero/moving, genuine startup, post-valid-signal outage/countdown and reliable recovery; restart never grants a new startup exception. |
| Qualified normal stop progression | Actual departure/passage, including no stop, drives sequence; delayed timetable alone never switches trip; measure target separately on device. |
| Uncertain positioning and manual controls | Last confirmed progress labelled uncertain; GPS-loss arrows and arbitrary-choice restrictions correct; reliable recovery stays in chosen trip. |
| Diversion and missing-stop recovery | Supported alternate sequence or recognized later stop on same trip; missing-list failure disables automatic progression with manual outcome fallback. |
| Final-stop and same-route return | Manual/GPS final arrival provenance, ordinary ten seconds, return waits for separate qualified or extra-manual trigger. |
| Non-passenger transitions | Deadhead/meal/layover/bus change/pilot car/depot display and next activity, no false physical completion or travel-as-break. |
| Operational corrections and evidence | Interrupted/skipped trip and fault-related bus replacement recorded distinctly; end entry delegates terminal confirmation to E7. |

### E6 candidates

| Candidate | Observable check |
|---|---|
| Separate own and accompanied-plan preparation | Same import engine, independently confirmed copies, visible ownership, no cross-account access or copied own driving. |
| One-person FADDER guidance | Correct linked route/progress/notices and permanent role; own plan still governs workday and open guiding controls. |
| Acute FADDER takeover and return | Jeg kjører locks immediately without losing pin/progress; explicit permitted return, no planned-ownership rewrite. |
| Instructor classroom/office and no-accompaniment day | Own activities work without fabricated passenger progress/person, correct uncertain completion evidence. |
| Instructor blocks/person changes and revisits | Explicit scope, overlapping/missing links unresolved, context change never completes/aborts unfinished linked trip or transfers old pin. |
| Planned own driving and revision-link repair | Select only own confirmed trips after driver restriction; linked revision invalidates affected links for explicit repair, never similar-trip relinking. |
| Mentor recovery and accompanied evidence | Reload preserves role/block/pin/outage; record actual accompanied portions and takeovers, validate E7 summary trimming with E5 pending settlement. |

Eight + nine + seven candidates expose 24 slices within these three epics alone. They are not necessarily one-session stories: scoped reconciliation, sensor progression and closure/recovery may need further splitting after qualification. This count is not an effort estimate. There is no evidence-based total yet. Do not derive schedule certainty from a small story label. Qualification failure, review, integration, tests and course reflection consume the same limited capacity as coding.

## E8 — Demonstration, Pilot Qualification and Evaluation

| Checkpoint | Evidence and allowed claim | What it does not establish |
|---|---|---|
| E8-D Demonstrable IBE160 delivery | Running private fullstack flow with fictional fixtures/anonymized evidence through React, FastAPI and real PostgreSQL; implemented import review, operational behavior, failures and PDF demonstrated. Isolated no-login PC demo uses same operational rules, simulated inputs and labelled exports. Reproducible run instructions, source/code/test evidence, AI-use/development log and reflection material; ordinary-PC assessment access for agreed period. Report each V1 item as implemented/verified/pending/blocked. | Static demo alone does not satisfy fullstack/database. Fictional source/sensor inputs do not establish live retrieval, sensor quality or operational usefulness. This is a delivery/evidence checkpoint, not a claim of instructor acceptance or completed V1 if requirements remain pending. |
| E8-P Permission to begin actual-shift pilot | Recorded passes for representative import + actual timetable/notice sources; mounted Lenovo/Brave positioning/interaction; full-day offline/restart/sync/conflicts/deletion; private access/Access expiry/logout, HTTPS, demo isolation/provider handling; Windows restart/resource/noise/network recovery; coherent updates and migrations through data expiry. Verify required capability in the target environment before relying on a pilot run for evidence. | Architecture approval, screenshots, desktop simulations or a deployed URL do not pass these gates. Missing essential source/device capability can block the pilot even when E8-D is demonstrable. |
| E8-E Completed field evaluation | After E8-P: three actual assigned workdays, agreed observation protocol, effort/notice/progression results and distraction/trust counter-metrics; private PDFs/external notes, anonymized publication. Separate measured results, uncertainty and corrections from simulation. | Not a pre-pilot prerequisite, controlled causal proof or permission to retain a permanent in-app pilot archive. |

All three are planning/evidence boundaries within E8; no provisioning or pilot activity occurs during this requirements checkpoint. A demonstration may be delivered with honestly documented operational blockers, but calling it completed approved V1 would require satisfying the existing requirements or a later explicit scope decision. General privacy/security requirements apply whenever private data is used, not only at E8-P.

## Early Qualification Queue

| Order / home | Small investigation and evidence needed | Consequence if unsuccessful |
|---|---|---|
| 1 — E2/E4 sources, before elaborate screens | Actual dated trips/stops/directions for 20/24/28/42 including overlapping 20/24, calendar/overnight and full-day completeness. Compare actual SX/TRO results to Svipper originals: stable IDs, links, line/stop/direction/validity, pagination/deltas, changes/closures/missing entries and feasible polling limits. A sample with no applicable notices proves no coverage. | Automatic retrieval remains mandatory. If targeted queries insufficient, return to the adopted bulk-data reconsideration point. Coverage failure is an explicit product/architecture decision, not permission for manual/demo substitution. |
| 2 — E2 OCR, before tool lock-in | Representative anonymized text PDFs, multi-column/multipage/scanned PDFs, JPG/PNG screenshots/photos and poor-quality examples; compare extracted facts/unknowns, Norwegian text and page coverage. Exercise manual fallback, cancellation/failure/crash cleanup, temporary/swap behavior and single-job resource use. | Qualify candidates rather than assume adoption. Manual correction remains supported but does not prove the promised import formats work. Material gap returns to owner. |
| 3 — E3/E8 device, before automatic progression claims | Confirm actual tablet/OS/Brave; trusted HTTPS/permission, position and speed availability/age/accuracy separately, foreground cadence, passage lag and reported close-stop scenario; movement/GPS-loss policy, touch/readability, sound/wake/theme capability and tethering interruption/recovery. | Tune thresholds within AD-9; show honest uncertainty/manual fallback. If usable GPS/progression target cannot be met, report blocker and request explicit decision, not schedule-only progress. |
| 4 — E1/E5/E8 delivery boundaries, early enough to avoid late surprise | Fixture-based transactions/retry, access clocks and isolated demo; prototype compatible offline boot/reopen and pending-update recovery before accumulating private state. Later verify actual Access/provider handling and desktop behavior before real uploads/pilot. | Fix defects within adopted architecture; material access/retention/host limitation returns to owner at the existing fallback decision point. |

These are bounded qualification tasks within the relevant epic, not extra product features or tests already performed. Source/technology documentation in the approved spine is evidence of candidates only; no new web/source/device research was run at this checkpoint.

## Saved Resume Point

Steps 1 and 2 are complete. Requirements, responsibilities, eight formal epic boundaries, early source/OCR/device qualification and E8-D/P/E are approved and are not being reopened. Capacity and delivery time remain unresolved by explicit owner direction; no fixed 40- or 160-hour budget and no automatic requirement deferral.

On 2026-09-25 the owner approved the E3 coverage summary and the UX-DR39/40 test clarifications, now incorporated into Stories 3.2 and 3.5 and their canonical copies. All 15 E3 stories and the epic-completion checkpoint are approved; E3 planning is complete. Work is paused at the owner's request. Resume with the E4 overview and first individual story under the current step-03-create-stories workflow when the owner resumes; no E4 story has been drafted and no E4 work is authorized tonight. Step 3 remains open. No implementation, readiness check or final workflow validation has started. The owner authorized committing and pushing the planning documents and development log before this pause.

### Preliminary Story Counts — 2026-09-25

Requested by the owner, this is a provisional decomposition forecast, not approved future stories, a fixed total or a time estimate. Counts may change during individual review; capacity/delivery remain unresolved and no requirements are deferred through this forecast.

| Epic | Current forecast | Basis |
|---|---|---|
| E1 Private access and draft | 4 approved | Current completed story breakdown. |
| E2 Preparation and revision | 12 approved | Current completed story breakdown, including two qualification stories. |
| E3 Actual trip and safe progression | 15 individually approved | Epic planning and coverage approved; two approved test clarifications incorporated, no additional story needed. |
| E4 Source-backed notices | 7–9 | Source qualification, ingestion/relevance, lifecycle, overview/driving presentation, acknowledgement/sound and failures. |
| E5 Offline continuity and recovery | 8–11 | Day authority, coherent assets, restart, synchronization, planned/emergency transfer, conflicts and compatibility. |
| E6 FADDER/INSTRUKTØR | 8–11 | Seven original candidates with separate linked-plan revision/repair and context/recovery slices where needed. |
| E7 Closing, summary and PDF | 6–8 | End/abort, uncertain outcomes, combined summary, offline PDF, retained access and all-copy cleanup/settlement. |
| E8 Demonstration and qualification | 6–9 | Fictional isolated demo/scenarios plus separate E8-D evidence, E8-P qualification and E8-E evaluation; gates are not collapsed into one acceptance. |

### E3 Story Coverage Summary — Approved 2026-09-25

E3 has 15 individually approved stories: one focused sensing qualification (3.1) and fourteen implementation slices (3.2–3.15), with actual-device checks retained where needed. This is planning coverage, not completed implementation or passed qualification. No sixteenth story is needed for the approved E3 boundary; the owner approved this summary and the two accessibility-test clarifications below on 2026-09-25.

| Approved requirement / E3 responsibility | Stories and bounded result |
|---|---|
| FR-6 actual trip, ambiguity, delay and manual authority | 3.3 manual selection/correction and pin; 3.4 qualified initial selection; 3.5 route/direction; 3.9 actual end/return. |
| FR-7 three-stop presentation, including passage without stopping | 3.5 adopted UX ordering and uncertainty; 3.6 observed progression. |
| FR-8 measured progression and diversion/gap recovery | 3.1 sensor feasibility; 3.6 independent passage/departure reference for the 100-m target; 3.8 correct stop occurrence, supported sequence and visible gaps. |
| FR-9 uncertain position and manual stop controls | 3.2 distinct speed/position quality and permissions; 3.5 retained uncertain context; 3.7 bounded GPS-loss arrows/arbitrary selection; 3.8 qualified recovery without fabricated observations. |
| FR-10 final-stop, return and non-passenger displays | 3.9 ten-second ordinary transition and separate return-start evidence/action; 3.10 every adopted activity composition and uncertain physical outcomes. |
| FR-11 operational changes | 3.3 tracking correction; 3.11 missing-list manual outcome; 3.12 interrupted/skipped work; 3.13 actual bus replacement versus typo. Whole-day end/abort stays in E7 as explicitly approved. |
| FR-16 adopted movement policy | 3.1 evidence-backed quality rules; 3.2 shared zero-speed/startup/five-minute policy and persisted history; 3.3–3.13 action-time checks; 3.7 and 3.14 retain approved direct-arrow/theme exceptions. E4/E6 consume the same engine. |
| FR-3 runtime fallback | 3.3 selection with missing data and 3.11 supported recovery/manual outcome; unavailable source never blocks a permitted explicit manual outcome. |
| Shared FR-4/5/17/20/22/24 | 3.10 activity facts, 3.13 physical assignment, each state-changing story's local persistence and origin-time evidence for E7; E5 still owns whole-day offline boot/authority/reconciliation, E7 terminal/report lifecycle. |
| NFR-1/2/3/4 and fullstack/database | Shared permission, readable honest state, access/expiry/failure handling and atomic local evidence; applicable mutations use inherited authenticated FastAPI/PostgreSQL validation and matching receipts. Theme preferences and ephemeral wake resources do not justify unrelated backend tables. Real-device claims remain conditional. |

UX coverage: UX-DR5/7/8 preparation-to-driving seams use 3.2–3.4/3.10; UX-DR10/11/12/13 use 3.3–3.5/3.9/3.10; UX-DR14/15/16 use 3.1–3.4/3.6–3.9/3.11/3.12; UX-DR17/18 use 3.9–3.13, with end/abort in E7. UX-DR24 uses 3.14, and E3's UX-DR25 portion uses 3.1/3.14/3.15; sound remains E4/E8. UX-DR1/2/23/38/43/44 apply in the relevant palette, uncertainty, provenance, accessible-control and fallback criteria. Notice markers/announcements and mentor/terminal integration (UX-DR20/22/29/32) retain E4/E6/E7 ownership; their E3 context/permission evidence is supplied here.

Two test-level gaps were closed by explicit owner approval and incorporated into the existing stories, without new V1 scope or a separate story:

- **Approved clarification to 3.2 (UX-DR39):** Given restricted detail/selection/review is opened, focus enters the opened surface and returns to its invoker on cancellation/closure. If movement closes it, focus must move to a visible appropriate control and never remain in hidden content; cancellation preserves saved data. Test keyboard focus before/after motion-triggered closure and cancelled review. The story now explicitly tests focus restoration alongside immediate closure/accessibility.
- **Approved clarification to 3.5 (UX-DR40):** Given supported current/next/departed or uncertain stop state changes, expose meaningful accessible role/status changes without announcing every sensor poll, moving focus or repeating unchanged announcements. Test fresh change versus identical repeat and restored uncertain context. Associated notice-warning descriptions remain E4 integration. The story now explicitly tests this announcement behavior alongside roles/uncertainty.

Both clarifications are approved and incorporated into the individual story files and this canonical document. The existing story approvals remain in force.

Dependencies follow the approved sequence: early 3.1 evidence informs 3.2; selection/view 3.3–3.5 precede progression and transitions 3.6–3.10, then explicit operational outcomes 3.11–3.13. Theme 3.14 depends on 3.2/3.5; wake 3.15 on 3.5/3.9. No declared E3 story dependency points to a later E3 story. E1/E2 supply access, confirmed dated plans, qualified source data and persistence. Later epics consume E3 output rather than becoming prerequisites for its bounded demonstrations. AD-1–AD-14 remain binding in their applicable domains, especially AD-2/3/5 persistence/shared engine, AD-7 source identity, AD-9 evidence, AD-10/12 authority/expiry and AD-14 compatible recovery.

Remaining delivery risks are qualification and integration, not permission to remove requirements: actual position/speed freshness and outage behavior (3.1), measured 100-m performance (3.6), supported diversion data (2.2/3.8), mounted readability, reliable Auto behavior (3.14) and actual screen wake (3.15). A browser acquisition flag does not prove the screen remained awake. Negative findings require an explicit solution decision; unknown/unqualified conditions stay visible. Capacity and delivery time remain unresolved, with more than 40 hours guaranteed but no assumed fixed total.

E8-D uses repeatable, labelled fictional scenarios plus real fullstack/database evidence where required. E8-P requires integrated real Lenovo/Brave/source/authority/offline behavior before use on actual shifts; no simulation, manual fallback or approved story can pass that gate by itself. E8-E remains the separate three-workday evaluation after pilot qualification. No tests, implementation or readiness workflow have run here.

**Checkpoint:** Approved by the owner on 2026-09-25, including both test clarifications. E3 planning is complete with 15 approved stories. The owner requested a pause before E4; E4 is the next continuation point and has not started. Step 3 remains open, with no implementation or pilot qualification implied.

### E2 Story Coverage Summary

E2 has twelve approved stories: 2.1 OCR qualification, 2.2 source qualification, 2.3 manual editor, 2.4 text PDF, 2.5 OCR/images, 2.6 dated matching, 2.7 own-plan confirmation, 2.8 whole-day transit data, 2.9 split-day preparation, 2.10 manual additions, 2.11 scoped file comparison and 2.12 atomic revision application.

FR-2 is covered by 2.1/2.3–2.5/2.7/2.10–2.12; FR-3 by 2.2/2.3/2.6/2.8; FR-4 by 2.3/2.7/2.9–2.12; FR-5 by 2.3/2.7–2.12. Preparation portions of FR-17/20 are covered by 2.8/2.9 and each feature's persistence; FR-24 draft/original/revision lifecycle by 2.3–2.12. NFR-2/3, UX-DR4–8/38/42/43, preparation clock UX-DR12 and relevant AD-1–7/10–12/14 boundaries are represented. Qualification approval does not mean tests passed.

Shared requirements remain explicitly allocated: live missing-stop fallback and movement/protected-state integration to E3; notices to E4; full active-day authority, offline boot/recovery/conflicts to E5; linked-person contexts to E6; terminal cleanup/summary to E7; real-device/host integration and evaluation to E8. E2's bounded preparation/revision outcomes are independently testable without claiming those later capabilities. No V1 requirement or adopted decision is changed. The owner's approval of 2.12 and request for the next individual story authorizes continuation into E3; final step-3 validation remains outstanding.

### E1 Story Coverage Summary

E1 has four approved stories in dependency order: 1.1 private ordinary access/online logout; 1.2 durable local logout/pending-revocation recovery; 1.3 protected local unconfirmed draft and expiry; 1.4 authenticated PostgreSQL synchronization, atomic receipts and safe retries. They cover E1's complete bounded user outcome of accessing, saving and reopening a protected minimal draft, with a verifiable server copy after acknowledgement.

FR-1 ordinary access/logout is covered; its active-day exception remains explicitly allocated to E5, not removed. E1's foundational portions of FR-2/18/20/24 are covered by draft recovery, status and retention, without claiming full import, whole-day offline recovery or completed-day lifecycle. NFR-2/3, E1 access-surface UX-DR1/2/3/23/38 and the required initial AD-1–5/10/12/14 boundaries are represented in the stories. Full visual/sensor/offline/release qualification retains its approved later ownership. No future story is required to demonstrate these bounded E1 outcomes; no implementation or pilot qualification is claimed. Story 1.4 remains deliberately limited to the minimal draft create event, rather than absorbing general E5 synchronization.

## Epic 1: Access and Recover a Private Working-Day Draft

The owner can sign in, save/reopen a protected minimal draft and log out through the adopted fullstack application. This first story delivers ordinary online access only; it does not complete E1 or FR-1 as a whole.

### Story 1.1: Sign In to and Sign Out of the Private Application

As the pilot owner,
I want to sign in to the private application and explicitly end my session,
So that access is controlled by the application rather than by hidden menus or the device lock alone.

**Acceptance Criteria:**

**Given** a clean development checkout and an operator-provisioned fictional pilot account,
**When** the documented local setup runs and the owner submits valid credentials through React,
**Then** FastAPI verifies the password hash and persists a server-managed session in PostgreSQL 18 before returning success,
**And** the browser displays a private main-menu shell based on authenticated server identity, with explicit logout and no public-registration action or endpoint,
**And** the official React/Vite TypeScript starter seeds the frontend; the Full Stack FastAPI template is reference material, not an inherited auth/admin application.

**Given** successful authentication on the shared web/API origin,
**When** the session is established,
**Then** the server sends an opaque session identifier in a host-only Secure, HttpOnly, explicitly SameSite=Lax cookie,
**And** credentials are absent from browser application storage, URLs, repository files and logs; private/auth responses use no-store,
**And** repeatable database migrations introduce only account/session and necessary access-control storage, not future workday/notice/role tables.

**Given** ordinary authentication and no active-day grant,
**When** the owner reloads or reopens the browser before app_authenticated_at plus 14 days,
**Then** the valid session permits entry without another password,
**And** polling/requests do not extend the deadline,
**And** at or after that deadline protected ordinary access requires renewed authentication even if a cookie remains; changing the browser clock does not extend server authority.

**Given** missing, forged, expired or server-revoked session authority,
**When** a caller directly requests protected main-menu session data,
**Then** the API denies access with the defined authentication/access outcome and no private payload,
**And** submitted owner fields confer no authority; account revocation invalidates all that account's sessions on subsequent requests.

**Given** login/logout and protected application requests,
**When** a writing request fails CSRF validation or exact-origin checks, including a sibling/demo origin,
**Then** it produces no unauthorized state change or authenticated session,
**And** credentialed cross-origin access is not enabled for the demo; malformed requests fail backend validation without partial writes.

**Given** invalid credentials or an unavailable API/database,
**When** sign-in is attempted,
**Then** the UI reports failure in ordinary Norwegian without claiming success or exposing credentials/internal errors,
**And** invalid credentials do not disclose account existence,
**And** repeated failures invoke a documented bounded rate-limit policy tested at its configured threshold and recovery boundary,
**And** database failure cannot produce an authenticated success response or usable session cookie.

**Given** a private view is open,
**When** the owner selects Logg ut,
**Then** the client immediately hides/locks the private view before waiting for the server response,
**And** server revocation remains visibly unconfirmed until an authoritative response confirms it; an absent or failed response leaves the view locked and offers retry.

**Given** a logout request reaches the server and its success is confirmed,
**When** the client processes that confirmation,
**Then** the server session is invalidated, its cookie is cleared and the client shows confirmed logout and private sign-in,
**And** replay of the old cookie is denied; browser-back cannot restore authenticated private content; repeated logout never renews authority.

**Given** this story's application has no locally retained working-day data,
**When** a logout request or response fails,
**Then** the private UI locks for the current page and explains that server logout is unconfirmed, with a retry action,
**And** hiding the menu is not represented as confirmed server revocation,
**And** durable offline locking/pending revocation is required before any later story introduces private local drafts; this story makes no offline-logout or retained-data recovery claim.

**Given** the sign-in and main-menu surfaces,
**When** the owner uses keyboard navigation, touch or enlarged text,
**Then** labelled fields/actions, visible focus, pending/disabled state and errors remain understandable without color alone or obscured actions,
**And** applicable approved DESIGN palette/typography/control tokens are reused,
**And** no unimplemented draft/demo action is presented as working and authentication requires neither GPS nor camera.

**Traceability:** FR-1 (ordinary private access/online logout subset), NFR-3, UX-DR1/2 (access-surface subset), UX-DR3 (private entry/logout subset), UX-DR38; AD-1/3/4/10 and AD-13 same-origin/cookie/no-store rules. AD-12 prohibits sensitive logging; AD-14 requires pinned build/dependency identity. All adopted decisions remain binding as their domains are introduced.

**Dependencies:** No previous application story. The future implementation supplies repeatable local setup, operator-only fictional account provisioning and trusted local HTTPS for Secure-cookie testing. Credentials remain outside source control. No public registration/admin feature, external account, domain, tunnel or deployment is needed for this local slice. PostgreSQL integration evidence cannot use SQLite. Password hashing and rate-limit implementation choices are documented and tested within this story.

**Implementation evidence:** Browser sign-in/reopen/logout against FastAPI/PostgreSQL; direct API negative tests for missing/forged/revoked/expired authority, CSRF/origins and rate limits; controlled-clock tests before/at/after day 14 with repeated requests; database failure and lost-logout-response cases; keyboard/text-enlargement inspection. Record versions and fictional fixtures. These checks are proposed, not executed during story drafting.

**Remaining coverage:** Before storing private local drafts, later E1 work must supply durable logout/reload locking, pending revocation and applicable retention. Active-day grants and post-end settlement remain E5 integrations; public fictional demo remains E8. The ordinary-session deadline must not become a global forced-logout/navigation rule for future authorized active days. No future story is needed to exercise this story's bounded online access outcome.

**Pilot qualification:** Contributes implementation evidence to E8-D, but does not pass E8-P. Actual private ingress/Access JWT checks, outer-session expiry/renewal, offline pending logout through a blocked gate, private/demo isolation and Lenovo/Brave behavior require later qualification. E8-E remains subsequent three-workday evaluation. No deployment or readiness decision is made here.

**Approval:** Approved by the owner on 2026-09-25 with immediate client hiding/locking at logout, before any server response; server revocation remains unconfirmed until confirmed, with retry. The fixed 14-day deadline and later active-day/durable-offline boundaries remain unchanged. Approval is for planning, not implementation. This is the canonical approved story.

### Story 1.2: Keep Private Access Locked Until Pending Logout Is Settled

As the pilot owner,
I want my explicit logout to remain effective locally when the network fails or the browser restarts,
So that the application does not silently reopen private access while server revocation is still pending.

**Acceptance Criteria:**

**Given** a signed-in private view, regardless of network availability,
**When** the owner selects Logg ut,
**Then** the client immediately hides/locks private content before waiting for the server,
**And** it atomically persists the local lock and pending-revocation intent in IndexedDB before reporting the local lock as durably saved,
**And** it records only necessary non-secret scope/status metadata; the session credential remains in the HttpOnly cookie,
**And** while revocation is pending the UI distinguishes local lock from unconfirmed server logout and offers retry.

**Given** a saved local lock and pending revocation,
**When** the browser reloads, closes/reopens or restores a page from history,
**Then** private content is not rendered and ordinary private requests are not started before the lock state has been checked,
**And** a still-present cookie or previously rendered authenticated page cannot unlock access,
**And** if online validation of access state is unavailable in this no-active-day slice, the application remains locked rather than asserting authentication or confirmed revocation.

**Given** pending revocation and a network that appears connected,
**When** the client retries automatically after connectivity returns or the owner selects retry,
**Then** it attempts the session revocation before ordinary private traffic,
**And** connectivity alone, timeout, HTML/redirect response or unexpected content type is not accepted as proof of revocation,
**And** a failure keeps the durable lock/pending state with an accurate retryable status, not indefinite success or fabricated progress.

**Given** the server applied logout but its response was lost, or the targeted session has already expired or been revoked,
**When** the client retries using Story 1.1's protected logout protocol,
**Then** the server can confirm that the targeted authority is no longer usable without renewing or creating a session,
**And** the client clears pending status only on an explicit authoritative outcome, never on an arbitrary 401, redirected login page or missing cookie alone,
**And** the local lock stays in place after settlement until fresh application login succeeds.

**Given** a settled logout and a locally locked application,
**When** the owner supplies fresh valid application credentials,
**Then** only a confirmed successful login unlocks private access and establishes a new ordinary authentication timestamp,
**And** restored network access, an old cookie, server polling or an outer access-gate login alone cannot unlock the application,
**And** while logout is still pending a new application login is not used to overwrite or bypass that pending revocation,
**And** ordinary access continues to use the fixed 14-day deadline without automatic renewal.

**Given** another same-origin tab or a request already in flight when logout begins,
**When** a logout notification or late authenticated response is received,
**Then** tabs apply the shared local lock, checking it on resume and before protected requests/rendering,
**And** late responses cannot display private content, clear the lock or replace the pending-revocation state,
**And** a stale response from the old session cannot undo a subsequently completed fresh login,
**And** no assertion is made that a client can retract requests already accepted by the server before logout.

**Given** local lock storage is unavailable, unreadable or fails to commit,
**When** logout is requested or the application restarts, resumes or restores a page from history,
**Then** private content is not shown automatically, including a brief render before access checks finish,
**And** a clearly labelled storage/access-state error explains that the durable local lock and pending revocation cannot be trusted; no saved-lock or server-revocation success is claimed,
**And** server revocation is still attempted when reachable and failures remain explicitly retryable,
**And** an absent or unreadable marker after a failed write is not treated as evidence that no logout is pending,
**And** recovery follows AD-10: resolve the outstanding revocation through authoritative server evidence and require fresh application login by the same owner before restoring any retained private work,
**And** new login must not silently discard, overwrite or bypass unresolved revocation; if the relevant authority cannot be identified or settlement cannot be established, keep private content locked and report that recovery remains unresolved,
**And** recovery neither clears unrelated browser data as a repair nor promises survival after browser storage eviction.

**Given** a test injects a failed lock/intent transaction, a lock-store read failure or unreadable access metadata,
**When** the tester separately exercises immediate logout, reload, browser close/reopen and history restoration, then attempts fresh login with pending revocation unresolved,
**Then** every case keeps private content hidden, reports the error and refuses to treat new credentials alone as settlement,
**And** after reliable storage access is restored and authoritative revocation settlement is obtained, only the same owner's fresh application authentication permits recovery,
**And** a different authenticated owner cannot recover the affected owner's retained work; this access boundary is tested with fictional owner identities, not public registration.

**Given** explicit logout, known server revocation or ordinary-session expiry,
**When** the client handles the corresponding outcome,
**Then** explicit logout/known revocation invokes the local lock and is kept distinct from ordinary expiry,
**And** there is no blanket destructive storage reset or global expiry handler that would invalidate the adopted future active-day exception,
**And** status and retry controls are labelled, keyboard accessible and understandable without color alone.

**Traceability:** FR-1 (explicit logout/revocation), NFR-2/3, UX-DR3/23/38, AD-2 (local persistence), AD-10 (offline lock, ordered pending revocation, fresh login), AD-13 (outer-gate failure is not app logout), AD-14 (preserve pending logout). This supplies the bounded logout prerequisite for later private draft storage, without claiming whole-day FR-17/20 coverage.

**Dependencies:** Approved Story 1.1, including server sessions, CSRF/exact-origin controls and confirmed online logout. Add only local access-lock metadata and the minimum idempotent logout confirmation behavior needed here. No workday model, import, GPS, role engine, live Cloudflare account or future story is required. Local tests use the existing app and PostgreSQL, simulated transport failures and browser reloads.

**Implementation evidence:** Browser tests for offline logout, delayed/lost responses, reload/history, repeated retries, fresh login ordering and two tabs; storage-transaction, read-failure and unreadable-metadata fault injection across reload/close-reopen/history; API tests for already-revoked/expired session settlement preserving CSRF/origin protection; negative checks for HTML/redirect/error responses. Assert no private rendering before checks, no interpretation of missing/unreadable lock state as cleared intent, no pending-intent replacement by new login and same-owner-only recovery after settlement. Use fictional access-scope fixtures here; test actual retained draft payloads when introduced in Story 1.3. These tests are planned, not executed here.

**Integration boundary:** There are no private workday payloads in this story. When later E1 stories introduce local drafts, they must prove that logout retains unexpired unsynchronized work without exposing it, only the same freshly authenticated owner can recover it, and all copies keep their original deletion deadline. E5 integrates the same lock with active-day grants/outbox and E8 qualifies actual Access renewal while locked, app revocation before Access logout and target-device recovery. These remain required, not waived or implemented by mocks. A stub data fixture is not evidence that full retention or active-day continuation works.

**Pilot qualification:** Automated local failure evidence contributes to E8-D. It does not pass E8-P's real Lenovo/Brave, gate-blocked logout, private/demo isolation or whole-day continuity checks; E8-E remains later field evaluation. No implementation, provisioning or readiness check is authorized by this planning draft.

**Approval:** Approved by the owner on 2026-09-25 with explicit storage-failure behavior: no automatic private rendering on restart/history when lock/intent storage is unreliable, clear error, AD-10 same-owner recovery and no silent disposal of unresolved revocation during fresh login. Approval concerns planning only. This is the canonical approved story.

### Story 1.3: Create and Reopen a Protected Local Working-Day Draft

As the pilot owner,
I want to create a dated working-day draft and reopen it without re-entering its saved details,
So that I have a private, recoverable starting point for preparing my day.

**Acceptance Criteria:**

**Given** a valid ordinary application session from Story 1.1 and no unresolved lock/revocation or access-storage error from Story 1.2,
**When** the owner opens Forbered neste skift, enters a valid service date and saves the initial draft,
**Then** the app creates an owner-scoped unconfirmed draft with a stable opaque UUID, service date, applicable IANA timezone, creation time, fixed expiry and schema identity,
**And** ownership comes from authenticated identity, not a user-editable owner field,
**And** no passenger trip, physical bus, location, confirmed plan or active-day grant is invented or activated; import and activity editing are not presented as implemented features.

**Given** the initial draft is ready to save,
**When** local persistence succeeds,
**Then** IndexedDB commits the draft and its pending typed creation event in one transaction before the UI reports saved state,
**And** the event has a stable identity and payload sufficient for subsequent synchronization without requiring future import/activity records,
**And** the UI explicitly says the draft is saved on this device and not synchronized; it never claims a PostgreSQL copy, whole-day offline readiness or backup exists,
**And** repeated submission while the save is in progress cannot create duplicate drafts/events for the same action.

**Given** an invalid or missing service date, unavailable local storage, insufficient storage space or injected transaction abort,
**When** the owner attempts to save,
**Then** an understandable error is shown, no successful save is announced and entered values remain available in the current view for correction/retry,
**And** a failed transaction leaves neither a draft without its event nor an event without its draft,
**And** retry after failure produces one committed draft/event, not a silent duplicate,
**And** the failure does not clear other local records, locks or pending revocations.

**Given** an unexpired saved local draft and valid application access for its owner,
**When** the owner reloads or closes/reopens the application and selects that draft,
**Then** the same draft UUID, service date, timezone, creation time, expiry and pending event are restored from committed storage,
**And** the initial list/detail shows unconfirmed and locally unsynchronized status plus expiry; reopening creates no extra creation event and does not extend retention,
**And** absent or unreadable data is shown as unavailable rather than replaced with an invented recovered draft,
**And** this slice does not claim offline cold-start assets or full-day recovery; browser/device qualification remains separate.

**Given** one or more local private drafts, including unsynchronized work,
**When** the owner logs out, encounters known revocation, or resumes with uncertain lock/intent storage,
**Then** Story 1.2 hides/locks draft lists and details before rendering and preserves permitted unexpired draft/event data within its existing deadline,
**And** a new login cannot discard or bypass unresolved revocation,
**And** after authoritative settlement only fresh application login by the same owner allows those drafts to be read again,
**And** another authenticated owner cannot list/read/relabel/adopt them, including by changing a draft ID or owner field in a request/action; fictional second-owner tests do not add multi-driver product scope.

**Given** an unconfirmed draft with no associated confirmed day,
**When** seven days from its original creation are reached,
**Then** the draft and its associated event/payload copies are inaccessible and deleted under the non-sliding draft-expiry rule,
**And** checks run before displaying or queuing its data at startup/resume and while the app is running; a closed browser deletes expired content before use when reopened,
**And** viewing, retrying a save, logging in or later preparing synchronization does not restart this deadline,
**And** expiry of unsynchronized work is visible in advance and expiry never marks work confirmed/completed or recreates an expired draft under a new identity.

**Given** the draft is associated with a day whose applicable AD-12 expiry is earlier than draft creation plus seven days,
**When** the effective deadline is calculated or rechecked before display, reopening or synchronization,
**Then** use the earlier deadline for the draft and all its associated payload/event copies,
**And** derive day expiry from confirmed actual end/abort or, for a never-ended day, its established planned final end interpreted with service date, timezone and explicit overnight dates,
**And** a service date alone does not justify inventing an unknown final-end timestamp; unresolved source facts stay explicit,
**And** reopening never restarts either clock and knowledge of an earlier day expiry creates no new grace period,
**And** controlled-clock tests cover the earlier-day deadline, the standalone seven-day deadline and reopening immediately before/at/after each; linked-day cases use fixtures until a real day association is introduced in E2.

**Given** two same-origin tabs saving or reopening drafts and a logout or expiry occurring concurrently,
**When** an operation resumes after a competing access/lifecycle change,
**Then** it rechecks applicable ownership, lock and expiry before exposing or committing private state,
**And** draft/event writes are atomic, identities are not reused for different content, and late UI responses do not resurrect expired data or unlock a logged-out view,
**And** this does not implement multi-device writer transfer or merge conflicts belonging to E5.

**Given** the preparation entry, draft list and draft detail,
**When** the owner uses touch, keyboard or enlarged text,
**Then** labels, focus order, pending/disabled states and validation errors follow the approved access/preparation visual and accessibility rules,
**And** unknown, unconfirmed and unsynchronized information is explicit through text rather than color alone,
**And** only interpreted/manual draft fields and access metadata are stored in IndexedDB; no source file, raw OCR, credentials or private payload appears in application-asset caches, URLs, logs or test artifacts.

**Traceability:** E1's approved minimal draft outcome; FR-1, foundational FR-2/20/24 portions, NFR-2/3; UX-DR2/3/4 (minimal unconfirmed draft subset), UX-DR23/38. AD-2 atomic local state/event, AD-5 identity/event conventions, AD-6 resumable draft fields, AD-10 ownership/logout recovery, AD-12 seven-day draft expiry and AD-14 schema identity. No claim of completed import review, full active-day recovery or complete V1 retention coverage.

**Dependencies:** Approved Stories 1.1 and 1.2. Create only the local unconfirmed draft/event stores needed for this result; no future trip/notice/mentor tables or generic event-sourcing framework. This is the minimal manually initiated unconfirmed draft supported by E1, not a seventh system-wide architecture contract. Existing authenticated server identity is used; no backend draft replica or sync receipt is claimed until the subsequent synchronization story. Local creation/reopening is independently demonstrable now.

**Implementation evidence:** Browser create/reopen/reload tests; IndexedDB transaction-abort/quota fault injection; repeated-save and two-tab cases; logout/failed lock reads/same-owner versus other-owner recovery with actual fictional draft payloads; controlled-clock tests immediately before/at/after draft expiry, including unsynchronized events and closed-browser return. Verify no unauthorized first-frame rendering and no deadline renewal. No tests are run as part of writing this draft.

**Remaining E1 and integration coverage:** A subsequent E1 story will deliver the first authenticated PostgreSQL draft synchronization with matching durable acknowledgement, retry and expiry protection; the current story remains explicitly local-only. E2 adds editable trips/activities, imported content and explicit plan confirmation. E5 expands full-day recovery and active-day authority. When a draft is associated with a day, earlier day expiry also bounds it under AD-12. This slice creates no confirmed day and does not alter that rule.

**Pilot qualification:** Local fixture evidence contributes to E8-D. It is not proof of device storage durability, whole-day offline operation, OCR accuracy or real-shift readiness. Those remain E8-P qualification, with E8-E after pilot readiness. Browser eviction can destroy unsynchronized local data; the app must not imply guaranteed durability or a server backup.

**Approval:** Approved by the owner on 2026-09-25, preserving the described scope and criteria and clarifying that the earlier applicable AD-12 day deadline takes precedence over draft creation plus seven days. Service-date interpretation must preserve known final-end facts rather than inventing an end time. Reopening never renews retention. Approval concerns planning only; this is the canonical approved story.

### Story 1.4: Synchronize a Private Draft with a Durable Server Receipt

As the pilot owner,
I want my locally saved draft to receive a verifiable server acknowledgement,
So that I can distinguish a draft stored only on this device from one also accepted by the backend without losing work after a connection failure.

**Acceptance Criteria:**

**Given** an unexpired local draft/event from Story 1.3, valid ordinary application authentication and no unresolved logout or access-storage error,
**When** the client connects or the owner retries synchronization,
**Then** the app submits the original committed draft event in a versioned immutable batch through the shared-origin FastAPI API,
**And** the envelope follows AD-5: schema version, batch ID, workday scope ID, client ID, writer epoch, expected server revision and ordered typed event identity/sequence/time/payload,
**And** at most one stable batch is in flight for the scope; the client persists its immutable identity/payload before sending and distinguishes pending, failed and acknowledged states.

**Given** this is the first server synchronization of an unconfirmed local draft,
**When** its minimal server scope and initial authority are established,
**Then** ownership is derived from authentication and the server binds the stable scope/client identity to initial writer authority and an explicit initial revision,
**And** initialization is retry-safe, bounded by the draft's existing expiry and rejects attempts to claim another owner's identity or an existing scope under different content/authority,
**And** the developer documents and tests initial-scope/epoch/revision handling before the first mutation; no arbitrary caller-supplied epoch grants authority,
**And** this technical scope creates no confirmed plan, active day or active-day grant; ordinary authentication is required and only necessary draft/control/receipt tables are introduced.

**Given** a valid initial draft batch,
**When** FastAPI accepts the mutation,
**Then** it checks authenticated ownership, scope, expiry, schema, current writer authority and expected revision under AD-5,
**And** PostgreSQL 18 atomically commits the draft, event/batch deduplication, matching receipt and next server revision,
**And** an injected failure before commit leaves none of those domain effects partially applied,
**And** success is returned only after the database commit; a UI-only saved flag cannot stand in for a server receipt.

**Given** the server committed a batch but the response was lost, or the browser closed before locally recording it,
**When** the client reloads and retries under valid access before expiry,
**Then** it retries the same persisted batch ID, event IDs, schema and payload,
**And** an identical authorized retry returns the original durable receipt even if its originally expected revision is now behind,
**And** no duplicate draft, duplicate event effect or extra revision increment results,
**And** reusing an ID with different content is rejected as idempotency_key_reused; an already accepted event cannot be applied again through another batch.

**Given** the client receives a synchronization response,
**When** it processes the response,
**Then** only a valid matching receipt for the submitted batch and accepted events marks those events acknowledged in a local transaction,
**And** local saving, a successful HTTP status, a server read or an unmatched receipt alone cannot change status from locally saved/pending to server-confirmed,
**And** the draft keeps its original identity, unconfirmed status and expiry, with a clear server-accepted indicator and receipt time distinct from creation time,
**And** missing/mismatched receipts, HTML/login redirects, unexpected content types, network errors and timeouts leave permitted local work unacknowledged and retryable,
**And** failure to commit acknowledgement locally leaves the original immutable batch available for safe retry.

**Given** accepted, still-unexpired draft data,
**When** its owner requests that draft through an authenticated server read,
**Then** the returned fields and revision match the committed PostgreSQL data,
**And** another authenticated identity cannot read/list/adopt the draft or obtain its receipt by changing IDs,
**And** a server read does not silently replace local pending work, count as new authentication, renew expiry or activate a workday,
**And** read/receipt authorization remains separate from the current writer authority required for new mutations.

**Given** a conflicting writer/revision, reused ID with changed payload, invalid/unsupported schema or expired/revoked ordinary access,
**When** the backend rejects synchronization,
**Then** it returns the applicable documented 409, 422, 401 or 403 outcome without partial domain writes,
**And** the client preserves unexpired local work, explains the failure and stops incompatible retries rather than overwriting revisions, minting replacement IDs or claiming success,
**And** authentication recovery follows Stories 1.1/1.2 without discarding unresolved logout,
**And** full multi-device conflict resolution and writer transfer remain E5; this story must expose a blocked conflict honestly without depending on that future UI to preserve work.

**Given** the draft's original creation time and any earlier associated-day expiry known under AD-12,
**When** upload, receipt lookup, read or periodic cleanup occurs,
**Then** the server independently enforces the earliest applicable deadline before deduplication or access, using the original creation instant rather than first upload/receipt time,
**And** invalid/inconsistent temporal metadata cannot extend retention; service date alone never invents an unknown final end,
**And** expired data cannot be uploaded/recreated through an old retry or new batch ID, and an authorized expiry response triggers corresponding local cleanup without a grace-period reset,
**And** all associated private draft, payload, control, event and receipt copies are covered by idempotent startup/periodic deletion while access guards already deny use at expiry,
**And** receipt/identity records used for retry do not become a permanent private archive.

**Given** synchronization or a server read is in flight when explicit logout, local access-storage failure or expiry occurs,
**When** the request later succeeds or the network returns,
**Then** the response cannot unlock/render private content, renew a deadline or resurrect expired payloads,
**And** pending revocation is settled before any new ordinary private traffic; already committed remote effects are reconciled only under valid authority and retention,
**And** unexpired local pending work is preserved for the same owner's permitted recovery, not discarded to make server/client status appear consistent.

**Given** the owner checks the draft's storage status,
**When** data is only local, awaiting a response, failed or acknowledged,
**Then** the UI describes that state in ordinary Norwegian with text and a permitted retry where meaningful,
**And** a server acknowledgement is described as a synchronized working copy, not a historical backup or guarantee against device/volume failure,
**And** private API responses use no-store and private payloads, credentials and original documents are absent from logs, asset caches, repository and CI artifacts.

**Traceability:** E1 fullstack/database and persisted-draft outcome; FR-1 and foundational FR-2/18/20/24 portions; NFR-2/3; UX-DR3/23/38; AD-1–5, AD-6 draft-only data, AD-10 authority/logout, AD-11 initial writer authority (not transfer), AD-12 retention, AD-13 response/origin boundaries, AD-14 immutable schema/build compatibility foundations. This is the first bounded SyncBatch/SyncReceipt path, not acceptance of all E5 recovery scenarios.

**Dependencies and size boundary:** Approved Stories 1.1–1.3. Support only create/synchronize/read of the minimal immutable unconfirmed draft; no concurrent draft editing or merge, file import, source polling, plan confirmation, active driving or mentor data. Use real PostgreSQL 18 transactions and constraints for integration evidence. Initial scope/epoch/receipt DTOs and exact endpoints are story-level design within the six adopted contracts, documented before coding. No whole application schema or generic event-sourcing framework is required. This story is more technically demanding than 1.3; keep the single create-event scope instead of broadening it into E5.

**Implementation evidence:** End-to-end fictional draft creation → sync → authenticated server read; PostgreSQL rollback injection; response-loss retry after reload; acknowledgement-write failure; duplicate event across batches and changed-payload ID reuse; owner/epoch/revision/schema rejection tests; expiry before/at/after deadline including delayed initial upload and earlier day deadline; logout/expiry while response is delayed; purge coverage of every introduced private table/store. Tests are proposed, not run during planning.

**Pilot qualification:** Evidence contributes to E8-D's actual React/FastAPI/PostgreSQL flow. E8-P still requires real target-device/access-gate tests, full-day recovery, all event types, transfer/conflict handling, retention integration and compatible releases. E8-E remains subsequent field evaluation. No historical private-data backups, deployment, implementation or readiness check is authorized by drafting this story.

**Approval:** Approved by the owner on 2026-09-25, preserving scope and criteria and explicitly requiring a valid receipt matching the sent batch before server-confirmed status. Local storage and server acknowledgement remain distinct. The owner instructed proceeding to the next individual story review. Approval concerns planning, not implementation; this is the canonical approved story.

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

The owner can import PDF/images, correct unknowns, resolve dated timetable matches, confirm own activities and physical bus, prepare available day data and review scoped revisions/split work without losing existing facts. FR-2–5 are the primary requirements; NFR-2/3, UX-DR4–8/42/43 and AD-6/7 govern import and preparation. Stories 1.1–1.4 supply the approved private draft foundation for later implementation stories.

This first E2 story is the early OCR qualification already required by AD-6, not an implemented import feature or a complete E8-P pass. It can run independently of E1 implementation; the result informs the later import adapter and review stories. Live transit-source qualification and device qualification remain separate early work, not assumed satisfied by this test.

### Story 2.1: Establish Which Import Cases the Extraction Candidates Can Support

As the pilot owner,
I want representative evidence of how PDF/image extraction handles my shift layouts and failures,
So that the import implementation exposes uncertainty and supports correction rather than relying on untested OCR assumptions.

**Acceptance Criteria:**

**Given** owner-supplied representative anonymized material is available for permitted local qualification,
**When** the qualification set is prepared,
**Then** its case inventory covers text PDF, two-column layout, multipage continuation, scanned multipage PDF, JPG/PNG screenshot/photo and poor-quality or unreadable input,
**And** the expected relevant pages, activity sequence, dates/times, Norwegian text and known ambiguous/missing fields are recorded for comparison,
**And** representative anonymized shifts have a checked answer key for dates, times, activities and ordering; the report lists the formats and failure types actually exercised, separately from planned or missing cases,
**And** missing representative categories are explicitly marked unqualified rather than replaced with fictional evidence presented as real-layout coverage,
**And** no exact operational identifiers, private original or raw OCR transcript is committed to the public repository.

**Given** a documented candidate configuration for pdfplumber and Tesseract behind the intended backend import boundary,
**When** each case is processed through a bounded local qualification harness,
**Then** text extraction is distinguished from OCR and every relevant scanned PDF page is rendered and processed,
**And** the evidence records tool versions, preprocessing, page coverage, duration and errors, with results traceable to sanitized case IDs,
**And** field/row ordering errors, mixed columns, broken Norwegian characters and omitted/duplicated activities are compared with the expected case facts rather than hidden by a successful process exit.

**Given** extracted fields are compared with expected facts,
**When** the qualification report is produced,
**Then** it distinguishes correct, incorrect, missing and uncertain values for service date, activity type, time, route/endpoints and vehicle-duty labels where supplied,
**And** it records which errors were detected by validation and which would require human correction; it does not claim unmeasured certainty or invent a previously unapproved accuracy threshold,
**And** ambiguous source codes remain unresolved, and Vogn is not interpreted as a physical bus assignment,
**And** the report identifies the minimum provenance/uncertainty information the later editable ImportDraft must expose, without making a confirmed plan from extraction alone.

**Given** unreadable input, an extraction failure, cancellation or interrupted processing,
**When** the harness exercises the failure and cleanup paths,
**Then** no output is treated as a confirmed shift and no existing confirmed plan is changed,
**And** the report identifies the direct manual-entry/correction path required by FR-2 and gaps the later review implementation must address,
**And** temporary originals, rendered pages and processing copies are removed after success/failure/cancellation and by recovery cleanup after interruption,
**And** temporary-storage/swap exposure is assessed and recorded as verified, limited or unresolved; deleting a file alone is not claimed as forensic erasure.

**Given** the accepted desktop-first constraints,
**When** representative extraction is measured with one OCR job at a time,
**Then** record processing duration and CPU/memory observations on the measured host, along with any blocking/resource issue,
**And** do not assume these measurements qualify final Docker/Windows restart behavior, acceptable desktop noise or the complete hosted processing chain,
**And** no continuous batch service, external OCR provider or source-file archive is introduced for this investigation.

**Given** all available cases have been investigated,
**When** the report concludes,
**Then** each required format/layout has a supported, conditional, unsupported or not-tested disposition with reproducible evidence and specific limitations,
**And** the conclusion explicitly separates what works, what requires the driver's checking/correction and what does not currently work; even supported extraction still requires the approved explicit driver confirmation,
**And** pdfplumber/Tesseract remain candidates unless the evidence justifies locking them for the intended import cases; partial success never certifies all formats,
**And** a material capability gap returns to the owner for an explicit decision without removing PDF/JPG/PNG from V1 or claiming manual-only input satisfies import,
**And** completing this story means completing the honest qualification result even if it is negative; passing the import gate is recorded separately and is not automatic.

**Given** qualification is complete,
**When** its retained artifacts are prepared,
**Then** keep the sanitized case inventory, expected generic/fictional examples where useful, aggregate findings, versions and reproducible procedure,
**And** retain no uploaded private originals, raw OCR archive or separate permanent anonymized operational quality dataset in the application/repository,
**And** explicitly separate source documents held by the owner from transient copies used by the harness; no deletion of the owner's external originals is implied,
**And** the report lists follow-up implementation and pilot evidence still required, without claiming import UI, driver confirmation, backend crash cleanup in production or provider handling has been implemented.

**Traceability:** FR-2 (PDF review/correction feasibility, extended to JPG/PNG by approved UX), FR-3/4/5 field interpretation boundaries, NFR-2/3; UX-DR4/42; AD-6 mandatory representative-file qualification and transient originals, AD-12 no private archive, AD-13 single OCR job/resource qualification; PRD B-2/B-5. This does not fulfill the functional import stories themselves.

**Dependencies:** No application-story prerequisite for the bounded qualification harness. Requires representative anonymized samples with enough expected facts to evaluate them and a local environment capable of running the candidate tools. Missing samples/tool access are explicit evidence gaps, not permission to mark a case passed. Subsequent import implementation consumes this report together with approved E1 access/draft storage. No real external service provisioning or Cloudflare upload is necessary.

**Evidence boundary:** Qualification is scheduled early within E2. Fictional fixtures may prove deterministic failure handling but cannot establish actual source-layout coverage. The evidence contributes only to the import portion of E8-P and supports honest demonstration claims under E8-D. Actual implemented import/confirmation/cleanup must later pass integrated checks; source coverage, tablet behavior and E8-E remain separate. No qualification work or implementation has been performed by drafting this story.

**Size boundary:** One bounded report and reproducible candidate evaluation, not construction of the complete importer, a generalized parser, an annotation platform or a new retained dataset. No estimate or delivery date is committed. If representative coverage is too broad for one development session, split case execution while preserving one explicit consolidated qualification decision rather than silently dropping cases.

**Approval:** Approved by the owner on 2026-09-25 with representative anonymized shifts and checked answer keys, actual format/failure coverage reported explicitly, and conclusions separating working behavior, required driver checking and current failures. Negative findings require an explicit further-solution decision and never automatically reduce V1. Approval is of the planned qualification story, not a test result. This is the canonical approved story.

### Story 2.2: Verify Dated Trip Matching and Whole-Day Timetable Coverage

As the pilot owner,
I want evidence that the selected timetable queries can identify my actual scheduled trips and supply their complete stop lists,
So that preparation does not silently select a similar trip or leave later parts of my day unavailable.

**Acceptance Criteria:**

**Given** representative anonymized shift facts and accessible timetable evidence,
**When** the bounded qualification case inventory is prepared,
**Then** it identifies service date, IANA timezone, route, direction, starting/ending stops and departure for expected passenger trips on pilot lines 20, 24, 28 and 42,
**And** explicitly includes overlapping 20/24 routes/shared stops, relevant service-calendar differences and a midnight/date-boundary case where available,
**And** expected facts are checked independently of the candidate query result, with evidence provenance; missing or ambiguous reference facts remain unresolved,
**And** real-source cases, synthetic edge cases and untested cases are labelled separately; lack of historic source data does not become evidence of incorrect shift facts.

**Given** the owner-confirmed distinction that Tide shifts use a service date and extended hours beyond 24:00, while Svipper displays ordinary clock time on the applicable calendar date,
**When** qualification translates a Friday 25:30 shift entry for matching,
**Then** its calendar representation is Saturday 01:30 in the applicable local timezone,
**And** the original Friday service date, original extended time and position in the working-day sequence remain available and are not rewritten as a Saturday-service shift,
**And** the report documents both representations and the translation, including checked cases around midnight; it does not infer a service date from calendar display time alone.

**Given** independently checked expected cases where multiple trips can be displayed as Saturday 01:30, including different service-day identities where source evidence permits,
**When** the candidate matcher compares the translated shift entry with returned journeys,
**Then** it uses supported service/calendar facts, trip identifiers, route, direction and endpoints rather than treating the shared displayed timestamp as unique,
**And** it retains and reports unresolved candidates when available evidence does not distinguish them, requiring driver choice rather than silently choosing a service day,
**And** the report records expected versus actual matches and whether each ambiguity case was exercised against real source responses or a labelled fixture.

**Given** those dated case facts and the targeted Entur API approach adopted in AD-7,
**When** candidate timetable queries are exercised,
**Then** record query strategy, source identifiers, service-calendar interpretation, retrieval time, returned candidate count and available stop/time ordering,
**And** inspect and document the actual Entur response date/time fields and trip identifiers, their documented meanings and observed values: distinguish explicit service-date evidence from calendar timestamps and derived/inferred values,
**And** do not assume Entur exposes a particular service-date field or that its displayed departure timestamp proves the journey's service date; absent semantics or identifiers are reported as gaps,
**And** compare results against the expected route, direction, date, departure and endpoints rather than accepting the first suggestion or line-number match,
**And** optimized journey-planner suggestions are never treated as a complete trip catalogue,
**And** record the source's applicable access limits, attribution/licensing conditions and the actual requests needed for representative day preparation without asserting untested throughput.

**Given** a query produces one supported match, multiple plausible matches, no match or source failure,
**When** results are classified,
**Then** the report distinguishes all four outcomes and provides evidence for automatic unique matching versus required driver choice,
**And** a successful no-match response is not conflated with unavailable, incomplete or failed retrieval,
**And** no alternate route/date/direction is silently substituted, and missing stop sequences are never fabricated,
**And** test ambiguous and failure behavior with labelled synthetic responses if no real example occurs; synthetic cases do not establish real-source coverage.

**Given** a representative complete working-day case, including later trips and separate work parts where available,
**When** all its passenger trips are resolved using the candidate strategy,
**Then** compare expected and retrieved trips/stops/times and list each supported, unresolved, unavailable or incomplete item,
**And** resolve pagination or other response-limiting behavior where applicable before claiming completeness,
**And** document what source data and identifiers a later OfflineBundle must retain for every available trip, not only the first active trip,
**And** non-passenger activities remain known shift activities; absence of an Entur trip does not erase or misclassify them,
**And** whole-day data coverage is kept separate from browser-asset readiness, access lifetime and real offline execution.

**Given** missing stop information or calendar/time ambiguity,
**When** the qualification evaluates recovery options,
**Then** identify any evidence-supported recovery from available timetable data and record its limits,
**And** preserve the established fallback: known trip facts plus Stoppinformasjon mangler, no automatic stop progression and permitted manual completion/abort/next activity in later implementation,
**And** the report never treats that fallback as proof the timetable source covers the trip or that an offline client can fetch previously unavailable data.

**Given** qualification findings and reproducible source evidence,
**When** the report concludes,
**Then** distinguish matching that works, cases requiring driver selection, missing/incomplete data and cases not tested,
**And** include the extended-service-time to calendar-time translation, retained shift ordering, actual Entur field/identifier evidence and unresolved temporal ambiguities in the conclusion,
**And** state whether targeted API queries have demonstrated the necessary day preparation for the tested cases, without generalizing beyond the sample,
**And** if the approach is insufficient, return a concrete gap and options to the owner at AD-7's NeTEx/GTFS reconsideration point instead of implementing a bulk pipeline or changing architecture independently,
**And** completing the report is distinct from passing the timetable capability gate; a negative result does not remove FR-3 or substitute simulated/manual schedules as acceptance evidence.

**Given** evidence is prepared for the repository or course assessment,
**When** the report and reproduction procedure are saved,
**Then** retain sanitized case IDs, methods, source references, aggregate outcomes and labelled generic/fictional edge fixtures,
**And** do not publish exact private shift/bus/vehicle-duty/trip identifiers or create a permanent operational quality dataset,
**And** temporary private case associations follow the existing handling/deletion boundaries; public source data is not mistaken for permission to retain private shift associations,
**And** the report states the tested dates/formats of responses and failure categories actually exercised, with remaining gaps rather than fabricated passes.

**Traceability:** FR-3, FR-4/5 activity/identity boundaries, foundational FR-17/20 whole-day data needs, NFR-2/3/4; UX-DR5/6/7/43; AD-7 targeted queries and qualified matches, AD-5/9 service-date/progression separation, AD-12 private evidence boundaries; PRD B-2 and the approved early source-qualification queue. Notice coverage FR-12–15 is not claimed here.

**Dependencies:** No implemented application or prior qualification story required. Needs representative anonymized case facts with a checked reference, source access and a small reproducible query procedure. E1/E2 implementation later consumes the conclusions; Story 2.1 need not be completed because known case facts may be entered directly for qualification. No source account/service provisioning, production adapter, import UI or full data warehouse is part of this story.

**Size boundary:** One bounded timetable/day-coverage investigation and decision report for the pilot configuration, not all Tromsø routes, a permanent feed ingestion system, notice-source evaluation or route calculation. Missing sample categories remain explicit; do not enlarge the investigation indefinitely or mark gaps passed.

**Evidence boundary:** Actual source queries establish only the recorded coverage at the tested time. Reproducible synthetic cases support E8-D behavior demonstration but do not qualify real matching. Later integrated preparation, OfflineBundle/restart and Lenovo/Brave tests remain required by E8-P. E8-E follows pilot qualification. No queries or tests were executed by drafting this story, and no readiness workflow or implementation has started.

**Approval:** Approved by the owner on 2026-09-25 with the explicit Tide service-date/extended-hour versus Svipper calendar-date/clock-time distinction. Friday 25:30 translates to Saturday 01:30 without losing Friday service identity or working-day position. Qualification must use checked expected cases including several Saturday 01:30 candidates, inspect actual Entur date fields/trip identifiers and document translation and ambiguities without assuming display time identifies service date. Approval concerns the planned investigation, not verified source behavior. This is the canonical approved story.

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

**Approval:** Approved by the owner on 2026-09-25 with an explicit manual cross-midnight correction/save/reopen test: Friday 25:30 retains Friday service identity, displays Saturday 01:30 where calendar representation is used and stays in the correct working-day position. Unknown facts remain visibly unknown, never guessed. Approval is planning only; this is the canonical approved story.

### Story 2.4: Review a Text-PDF Shift as an Editable Unconfirmed Draft

As the pilot owner,
I want to upload a text-based shift PDF and inspect its interpreted activities beside the source,
So that I can identify errors and missing work before any interpretation becomes my confirmed plan.

**Acceptance Criteria:**

**Given** permitted private application access and the preparation entry,
**When** the owner selects a supported text-based PDF for a new import,
**Then** the authenticated backend validates the upload against documented type/size/processing limits and invokes the import adapter qualified by Story 2.1,
**And** it creates an owner-scoped unconfirmed import attempt/draft, not an active day or confirmed plan,
**And** cancelling file selection returns to the preceding state without altering another draft or confirmed work,
**And** unsupported, corrupt or over-limit input produces an understandable failure without a false successful import or exposure to another owner.

**Given** a qualified text PDF with multiple columns or page continuations,
**When** interpretation completes,
**Then** process all relevant pages and produce editable known fields and activities in source-supported order,
**And** preserve minimal page/field provenance, missing/uncertain markers and unexplained source codes without retaining a raw OCR/text archive,
**And** Vogn is not treated as a physical bus number, and Travel to is not automatically classified as pilot-car transport,
**And** incomplete extraction identifies the specific missing/unreadable pages or parts using available page/section references; when the extent cannot be established it explicitly says coverage is unknown rather than presenting a complete plan,
**And** this coverage status is retained with the draft so it survives saving/reopening; unsupported portions never silently disappear from the review.

**Given** a Friday-service entry containing 25:30 and neighboring activities,
**When** extracted data is shown, corrected, saved and reopened,
**Then** retain the source Friday service date, extended time and activity identity/order, deriving Saturday 01:30 only for calendar-date presentation,
**And** do not merge it with another same-display-time activity or infer an Entur service-date match,
**And** missing source date/time or ambiguous ordering stays visible for correction instead of invented midnight rollover or silently assigning today's date.

**Given** a completed or partially interpreted unconfirmed draft,
**When** the shared review screen opens,
**Then** the PDF and interpreted activities are shown side by side in the approved source/review composition while the transient original is available,
**And** the driver can use Story 2.3's direct field correction and missing-activity addition, with extracted/manual/unknown facts distinguishable,
**And** saving or server acknowledgement does not confirm the plan or enable an active trip,
**And** processing/layout failures retain available interpreted facts as unconfirmed and expose another-file/manual-correction paths rather than inventing a complete shift.

**Given** an unexpired interpreted draft is reopened after its transient original preview has been released,
**When** the shared review screen is displayed under permitted access,
**Then** the saved editable activities, manual corrections and page/part coverage warnings remain available,
**And** the source area explicitly states that the original PDF must be selected again to compare with it, with a labelled file-selection action rather than an empty or apparently loading preview,
**And** reselecting a file for comparison does not silently reimport it, overwrite corrections, confirm the plan or reset expiry,
**And** tests cover side-by-side review before closure, source-unavailable messaging after reopening and retained warnings identifying missing pages/parts.

**Given** an upload/interpretation attempt is retried or its response is lost,
**When** the owner resumes that same authorized unexpired attempt,
**Then** a stable attempt identity permits recovery of any persisted interpreted result without producing duplicate activities/drafts or reusing a changed payload under the same identity,
**And** retry cannot require the backend to retain the original after processing has ended,
**And** if no interpreted result survived, the UI explains that the file must be selected again; a new attempt is explicit,
**And** late or cancelled results never overwrite intervening manual corrections, another draft or confirmed work; mismatched revisions are preserved as a visible conflict rather than silently applied.

**Given** interpretation finishes, fails or is cancelled,
**When** processing cleanup runs,
**Then** backend originals and processing copies are deleted on each outcome, with interrupted-process cleanup verified on restart,
**And** originals never enter IndexedDB, service-worker caches, persistent job payloads, logs, repository or CI artifacts,
**And** the browser preview remains transient for the current review, is released on leaving/cancelling the review, logout or expiry, and is unavailable after reload unless the owner selects the source again,
**And** only necessary interpreted fields/provenance/corrections remain under the existing draft retention boundary; the UI explains the distinction between the transient file and retained interpreted information.

**Given** interpreted data is committed and manually corrected,
**When** local persistence, synchronization or reopening occurs,
**Then** reuse the approved atomic state/event and immutable batch/receipt behavior, preserving field provenance, activity IDs/order and unresolved values,
**And** clearly distinguish local saving from server confirmation; an extraction response alone is not a matching SyncReceipt,
**And** draft expiry is non-sliding from draft creation or an earlier applicable associated-day deadline, not completion/retry time,
**And** every introduced interpreted result, import-attempt private association, pending payload and receipt is included in ownership checks and expiry cleanup.

**Given** logout, unreliable local lock storage, permission loss or expiry occurs during upload or interpretation,
**When** the browser receives a late response or reopens the application,
**Then** private source previews and interpreted contents remain hidden until the applicable Story 1.2/AD-10 recovery conditions are met,
**And** no late result renews retention, bypasses pending revocation or resurrects an expired draft,
**And** server processing still cleans transient originals even when the client disconnects; disconnection is not permission to retain private files indefinitely.

**Given** the import/review UI,
**When** it is used with touch, keyboard or enlarged text,
**Then** upload progress, failure, partial-page coverage, unknown values and save states are clearly labelled with focus/error handling and the approved preparation tokens,
**And** no camera/GPS permission, AI correction interpreter or precise gesture is required,
**And** scanned/image-only input is explicitly identified as requiring the later OCR path rather than represented as a successful empty text import; V1 support for that path remains mandatory.

**Traceability:** FR-2, FR-3/4/5 interpretation and identity boundaries, NFR-2/3; UX-DR2/4/5/38/39/42; AD-1 import boundary, AD-2/5 persistence, AD-6 backend interpretation/transient originals, AD-10 access, AD-12 retention and AD-13 bounded processing/private no-store handling. Preserve the approved service-date/extended-time clarification from Stories 2.2/2.3.

**Dependencies:** Approved implementation Stories 1.1–1.4 and 2.3, plus completed Story 2.1 evidence supporting the intended text-PDF cases. Story 2.1's approval as a plan is not passing extraction evidence; a material negative qualification result requires the owner's further-solution decision before locking a parser. No timetable integration from 2.2 is required to review known extracted fields. Exact processing limits are documented/tested implementation choices, not a silent reduction of supported representative V1 inputs.

**Implementation evidence:** Representative qualified text fixtures with checked dates/times/activities/order; multipage/column coverage; Friday 25:30 correction/reopen; missing-field/code cases; invalid/oversized/cancelled file selection; partial extraction, crash cleanup, duplicate retry/lost response and late-result/manual-edit conflict; source-preview loss after reload; logout/expiry while processing; local/PostgreSQL fault cases and owner isolation. Test private sample handling without publishing operational originals. These checks are proposed, not executed here.

**Size boundary:** New unconfirmed text-PDF import into one shared editor, not replacement of an active plan, scoped day revisions, OCR, timetable matching or final plan confirmation. Build only the import attempt/result handling needed for this path. Existing drafts remain intact when another file is selected; no silent merge/overwrite is introduced.

**Pilot qualification:** Implemented fixture evidence contributes to E8-D and the text-import portion of E8-P. Actual hosted handling/cleanup, remaining PDF/image formats and end-to-end driver confirmation still require their own integration evidence; this story cannot establish the whole pilot gate or E8-E. No implementation or readiness workflow is started by this draft.

**Approval:** Approved by the owner on 2026-09-25 with side-by-side PDF/activity review while the transient original is available, preserved editable draft and explicit original-reselection guidance on reopening, and specific missing-page/part warnings for incomplete extraction. Import remains unconfirmed. Approval concerns planning only; this is the canonical approved story.

### Story 2.5: Review Scanned PDFs and Images Through the Shared Import Flow

As the pilot owner,
I want to import a scanned shift PDF, screenshot or photograph into the same editable review,
So that I can check and correct my shift even when its source has no usable text layer.

**Acceptance Criteria:**

**Given** permitted private access and representative scanned PDF/JPG/PNG cases qualified under Story 2.1,
**When** the owner selects an existing supported file through the shared upload entry,
**Then** the backend validates the input and uses the qualified OCR adapter behind the existing import port,
**And** selecting an existing photograph/screenshot requires no camera permission, live-camera capture, GPS or separate installed application,
**And** cancelling selection preserves the existing draft and invalid/corrupt/over-limit files produce an understandable error without a false successful import.

**Given** one shift is split across several JPG/PNG files,
**When** the driver selects the files or adds another image to the same unconfirmed draft,
**Then** show an ordered file list with clear source references and accessible controls to inspect and change the order rather than relying silently on filename or upload completion order,
**And** show the proposed combined activity sequence before applying additions, preserving existing activity identities and manual corrections,
**And** repeated selection/retry or overlapping content must not create duplicate activities; uncertain overlaps require explicit resolution rather than silently merging or dropping potentially distinct activities,
**And** adding a file cannot remove activities absent from that file, overwrite earlier corrections or become an active-plan revision,
**And** changing source order does not silently rewrite corrected activity order; any conflict remains visible for driver resolution.

**Given** a multi-image import with out-of-order files, overlapping rows, a later-added file and an already corrected activity,
**When** the driver reviews the order, applies additions, saves and reopens the draft,
**Then** the checked expected activity sequence and prior correction are retained without duplicates, with minimal file/part provenance and coverage warnings,
**And** cropped, unreadable or known missing parts remain explicitly uncertain/unknown; success on the available files is not proof the whole shift is present,
**And** only minimal source-reference/order metadata persists, not original image files or permanent thumbnails; unavailable originals must be reselected for comparison,
**And** an unreadable or cancelled individual file cannot erase successfully saved activities from the other files, and the draft remains unconfirmed regardless of OCR success.

**Given** a PDF containing scanned pages, optionally alongside usable text pages,
**When** the import adapter processes it,
**Then** every relevant scanned page is rendered and OCR-processed, with explicit per-page text/OCR/error/uncertain coverage,
**And** text and OCR paths cannot duplicate activities merely because the same page has both a text layer and image content,
**And** page continuations and source-supported activity order are preserved; neither empty text extraction nor completion of one page is evidence that the whole document was interpreted.

**Given** a screenshot/photo or an uncertain OCR result,
**When** extracted activities are prepared for review,
**Then** retain supported values with minimal source/page provenance and visible unknown/uncertain states,
**And** do not invent cropped, unreadable or missing text; identify affected pages/parts when known and explicitly mark unknown coverage where the missing extent cannot be established,
**And** common tested recognition failures in Norwegian characters, times, columns and row order are exposed for checking rather than silently normalized into confident facts,
**And** Vogn, physical bus, passenger trips and other activities keep their approved distinct meanings.

**Given** a scanned/image Friday-service entry reading 25:30, or an ambiguous recognition of it,
**When** the owner reviews/corrects, saves and reopens the draft,
**Then** supported or manually corrected Friday 25:30 retains Friday service identity and working-day position, with Saturday 01:30 used for calendar presentation,
**And** uncertainty between possible time readings remains explicit until corrected; OCR cannot infer the service date from a calendar-time rendering alone,
**And** identical display times never merge distinct activities or discard their provenance.

**Given** a transient original and an interpreted result are available,
**When** the shared review opens,
**Then** display the source PDF/image beside the interpreted activities using the same correction/add-activity controls and unknown/partial-coverage labels as Story 2.4,
**And** import and save remain unconfirmed regardless of extraction success or server acknowledgement,
**And** reopening retains editable activities, manual corrections and coverage warnings while the source area clearly requests reselection of the original for comparison,
**And** source reselection alone does not reimport, overwrite corrections, confirm work or extend retention.

**Given** a processing error, cancellation, client disconnection or interrupted OCR process,
**When** the request ends or the backend recovers,
**Then** remove uploaded originals, rendered pages and temporary preprocessing copies under the same success/failure/cancel/crash cleanup rules as Story 2.4,
**And** no raw file, rendered-page archive or raw OCR transcript persists in IndexedDB, asset caches, persistent job payloads, logs, repository or CI artifacts,
**And** retain only permissible interpreted fields/provenance within existing draft expiry, offering correction/reselection without pretending the missing result was saved,
**And** one OCR job runs at a time with tested bounded input/resource handling; waiting or interrupted work cannot create a hidden persistent original-file queue.

**Given** an OCR result is retried, arrives after a manual edit or is received during logout/expiry,
**When** the result would be applied,
**Then** reuse Story 2.4's owner/attempt/revision checks and reject silent replacement of newer edits, another draft or confirmed work,
**And** result application and its event use the existing atomic storage/synchronization path without mutating an already submitted batch,
**And** only a valid receipt matching the sent batch changes local/pending status to server-confirmed,
**And** late results cannot unlock private content, bypass unresolved revocation, reset the earliest AD-12 deadline or resurrect expired draft data.

**Given** an OCR import has partial or no usable results,
**When** the owner sees the outcome,
**Then** the review explains what was extracted and which pages/parts remain missing or uncertain, with accessible error/status labels and manual correction/another-file actions,
**And** failure does not silently substitute a fictional shift or mark an empty extraction complete,
**And** unsupported required representative cases remain reported as capability gaps requiring a solution decision, not removed from V1 merely because manual entry exists.

**Traceability:** FR-2 with the approved PDF/JPG/PNG extension; FR-3/4/5 interpretation boundaries; NFR-2/3; UX-DR4/5/38/42/44; AD-1/6 import port/backend OCR, AD-2/5 persistence, AD-10/12 access and retention, AD-13 bounded single-job processing. Carry forward the approved temporal clarification and Story 2.4 side-by-side/reselection/page-coverage behavior.

**Dependencies:** Implemented Story 2.4 and completed Story 2.1 qualification supporting the intended scanned/image cases. Their planning approval is not evidence that OCR works. The existing editor/access/sync stores are reused through 2.4's dependencies. OCR-tool adoption must follow actual qualification; materially negative findings return to the owner before silently changing tools or supported scope.

**Implementation evidence:** Checked representative scanned multipage PDFs, mixed text/scanned pages, JPG and PNG screenshots/photos, unreadable/cropped input and Norwegian text; multi-image shifts with changed file order, overlapping rows, later additions, repeated files, missing/failed parts and prior manual corrections through save/reopen; page coverage and duplicate suppression; Friday 25:30 correction/reopen; failed/cancelled/interrupted processing and restart cleanup; response-loss retry, late-result conflict, logout/expiry; retained draft without original preview. Record actual case coverage and remaining gaps, not an invented universal OCR-accuracy claim. Tests are planned, not run here.

**Size boundary:** Add one OCR adapter path and page/format dispatch to the existing flow, not a new import system or general image editor. No camera-capture UI, automatic plan activation, timetable lookup, active-day revision or mentor workflow. Detailed preprocessing choices follow the qualified evidence; additional unsupported image formats are not introduced.

**Pilot qualification:** Local integrated tests contribute to E8-D and the import portion of E8-P. Representative real-layout evidence, actual host cleanup/resource behavior and the complete driver-confirmation flow still require their respective checks. E8-E remains later actual-shift evaluation. No implementation or readiness check is performed by drafting this story.

**Approval:** Approved by the owner on 2026-09-25 with multi-JPG/PNG shifts, inspectable/controllable file order, additive import into the same unconfirmed draft without duplicates or lost corrections, and explicit uncertainty for cropped/unreadable/missing parts. OCR success is never driver confirmation. Approval concerns planning only; this approved copy is canonical.

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

**Approval:** Approved by the owner on 2026-09-25 with explicit time/stop-discrepancy tests: preserve driver corrections, expose source values and differences, and prevent fresh or delayed responses from silently replacing corrections. A unique match requires identity and service-date evidence, not just line number and clock time. Planning approval only; this approved copy is canonical.

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

**Approval:** Approved by the owner on 2026-09-25: a reviewed unmatched trip can enter the confirmed plan once blocking temporal ambiguities are resolved; missing matches, stops and physical bus remain unknown/missing rather than verified. Any draft change during review requires a new review before confirmation. Planning approval only; this approved copy is canonical.

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

**Approval:** Approved by the owner on 2026-09-25 with per-trip coverage remaining visible for partial-day downloads; partial data must never produce a whole-day-prepared status. Planning approval only; this approved copy is canonical.

### Story 2.9: Prepare Split Work as One Combined Day

As the pilot owner,
I want to review each work part with its own reporting time and depot within one combined day,
So that I can prepare for later work without treating the intervening gap as a completed day or an invented transfer.

**Acceptance Criteria:**

**Given** an owned, unexpired draft contains split work,
**When** the driver reviews or corrects its work parts before initial confirmation,
**Then** allow activities to be assigned to explicit ordered parts with stable identities within the same own plan/workday,
**And** each part exposes its own reporting time and known reporting location/depot for checking and correction,
**And** a time gap or separate source file alone does not silently create a part boundary; source-supported interpretations remain reviewable and ambiguous grouping requires driver resolution,
**And** regrouping existing activities does not duplicate them, discard corrections or change their service-date/source identities.

**Given** two parts have different depots, or the later reporting location is unknown,
**When** the combined overview is displayed,
**Then** show each part's own reporting time and depot separately, leaving the unknown location explicitly unknown,
**And** show the interval between parts and the next reporting information without inventing travel, rest, meal or paid/unpaid classification,
**And** retain explicitly entered or source-supported transfers and other activities instead of replacing them with a generic gap,
**And** do not imply that the same physical bus continues into the next part merely because the plan or vehicle duty is shared.

**Given** a later part or activity crosses calendar midnight,
**When** the driver reviews, confirms, saves and reopens the combined plan,
**Then** preserve the confirmed service date and activity order with explicit calendar dates where needed,
**And** test Friday 25:30 displayed as Saturday 01:30 within its correct part without moving it to another working day,
**And** temporal/grouping ambiguity that prevents a correct sequence or planned final end requires correction before confirmation; unknown depot, bus or source match alone does not require guessed values.

**Given** the driver reviews the complete split-day draft,
**When** initial confirmation is requested,
**Then** use Story 2.7's explicit reviewed-revision confirmation for the combined plan, preserving all parts and their activities,
**And** keep every part's reporting time and depot visible in the review while confirmation, day-data coverage and the expiry deadline apply to the combined working day,
**And** a change to a part, reporting detail or activity during review requires a new review before confirmation,
**And** cancellation preserves the unconfirmed draft, and failed confirmation leaves no partially confirmed collection of parts,
**And** a confirmed unmatched trip remains permitted with its missing-data labels; confirmation cannot verify unknown facts.

**Given** the combined plan contains multiple parts,
**When** Story 2.8 prepares its data and renders coverage,
**Then** include every part's trips in the same revisioned day manifest and show coverage per trip within each part,
**And** successfully downloading the first part cannot mark the whole day prepared if a later part lacks required data,
**And** retained available data and part/reporting information can be inspected without new requests in the already available compatible application, with explicit missing/stale states.

**Given** the plan includes an intermediate depot return or the interval before a later part,
**When** preparation/overview evaluates the combined-day structure and planned end,
**Then** that boundary is not a terminal workday state, does not mark later work complete and does not start a separate completed-day retention clock,
**And** derive the never-ended day's planned final end from the final activity of the reviewed combined plan, not the first part's end,
**And** expose one workday identity for the later final end/abort and daily summary; no summary or actual completion is fabricated here,
**And** runtime entry into the gap and final end/abort behavior remain E3/E7 integration obligations, not functionality claimed by this preparation slice.

**Given** a part edit, initial confirmation or retry,
**When** local storage and server synchronization occur,
**Then** atomically persist the affected grouping/reporting facts and event using the existing local storage and authenticated PostgreSQL path,
**And** preserve stable identities through retry/reopen; only a matching valid receipt changes synchronization status to server-confirmed,
**And** test failed local writes and lost responses without duplicate parts or lost activities,
**And** apply ownership, pending-logout/storage locks and AD-12 expiry to every private part/association/event; regrouping or reopening never resets retention or revives expired data.

**Given** the split-day review and overview,
**When** used with touch, keyboard or enlarged text,
**Then** part headings, reporting times/locations, gaps and per-trip warnings remain distinguishable with accessible text and focus handling,
**And** moving an activity between parts is possible without drag-only controls,
**And** the overview retains the approved persistent clock and separates confirmed-plan, local-data and app-asset status.

**Traceability:** FR-2/4/5; preparation portions of FR-17/20/24; UX-DR6/7/12/38 and the split-day ownership boundary of UX-DR8; approved UJ-1 split-work extension; AD-2/4/5 persistence/identities, AD-6 reviewed plan changes, AD-7 whole-day data, AD-10 access and AD-12 one combined-day deadline. E3/E7 retain actual transitions, final end and summary behavior.

**Dependencies:** Implemented Stories 2.3, 2.7 and 2.8 with their prerequisites. Manual split-day entry demonstrates this independently; existing import paths feed the same editable grouping. No future revision editor, operational progression or summary implementation is required to test the initial confirmed split plan and complete manifest enumeration.

**Implementation evidence:** Two parts with different depots; unknown later depot; explicit transfer versus unclassified interval; source-file boundaries that do not equal work-part boundaries; regrouping without duplicates/lost corrections; Friday 25:30; stale-review rejection; first-part-only download; save/reopen, failed write/lost receipt, ownership/logout/expiry and accessible grouping. Check the combined planned final end and absence of intermediate terminal state in domain fixtures. Tests are specified, not run.

**Size boundary:** Initial own-day part composition and overview, reusing editor, confirmation and manifest. No active-day revision, new import engine, payroll/rest-rule inference, physical transfer verification, live progression, mentor plans or summary generation. All later V1 obligations remain assigned, with no capacity estimate or deferral implied.

**Pilot qualification:** Repeatable preparation contributes to E8-D. E8-P must integrate actual later-part continuation, offline restart, final end/retention and one combined summary on the target device before actual-shift use. E8-E remains separate field evaluation.

**Approval:** Approved by the owner on 2026-09-25 with each part's reporting time and depot visible during review, while confirmation, data coverage and expiry apply to the combined working day. Planning approval only; this approved copy is canonical.

### Story 2.10: Review and Confirm Manual Extra Work in the Existing Own Day

As the pilot owner,
I want to add extra trips or activities through an explicit comparison with my confirmed plan,
So that additional work joins the correct day without replacing existing work or silently changing my active trip.

**Acceptance Criteria:**

**Given** an owned, unexpired, nonterminal confirmed own plan and permitted access,
**When** the owner opens manual extra-work entry from the shift overview,
**Then** show the target own day/plan and an additions-only scope throughout editing, comparison and confirmation,
**And** create a separate unconfirmed revision draft against its base plan revision, using existing activity fields and stable proposed identities,
**And** never create a new workday merely because work is added later or to another part; unrelated plans remain untouched.

**Given** proposed additional trips or other activities,
**When** the driver edits and reviews them,
**Then** preserve service date, explicit overnight representation, placement in the combined day and intended work part,
**And** use the existing matching and unknown-data rules: retain manual corrections and source discrepancies, allow reviewed unmatched trips and never fabricate stops, locations or physical bus,
**And** resolve ambiguity preventing correct identity, sequence or planned final end before confirmation,
**And** show possible overlap with an existing activity for explicit resolution rather than silently duplicating or merging it; equal line number/time alone cannot prove identity.

**Given** a manual additions draft ready for comparison,
**When** the driver opens review,
**Then** clearly distinguish added activities from unchanged existing activities and show their placement with each affected part's reporting time/depot,
**And** this additions-only operation cannot propose removals or silently modify existing activities, reporting facts, manual corrections or performed evidence,
**And** show any proposed change to the combined planned final end and resulting never-ended-day expiry before confirmation,
**And** cancel or failed matching leaves the currently confirmed plan in force and the driver's permitted draft recoverable.

**Given** the driver has reviewed the additions against a specific base plan revision,
**When** explicit confirmation occurs,
**Then** atomically apply only the reviewed additions, increment the plan revision and persist the typed revision event with its provenance before showing local success,
**And** if the proposal or relevant base plan changes during review, require a new comparison/review; no last-write-wins replacement,
**And** repeated confirmation/retry uses stable identities and cannot apply the additions twice,
**And** rejection or failed local commit leaves the prior confirmed plan intact.

**Given** an operational-state fixture with performed activities and a manually selected active trip,
**When** the revision is applied,
**Then** preserve performed evidence, active activity/tracking identity, manual pin, progression and corrections; adding an earlier scheduled trip is not an automatic context switch,
**And** no added activity is marked performed merely because its scheduled time has passed,
**And** terminal or expired days reject additions without resurrecting the day,
**And** operational entry and confirmation must ultimately use E3's shared movement permission; no UI path may bypass it. Before that integration exists, demonstrate this slice in preparation and domain fixtures, not as a qualified in-vakt feature.

**Given** the new revision is locally confirmed,
**When** data coverage is displayed or refreshed,
**Then** bind coverage to the new plan revision, preserve still-valid downloaded data for unchanged activities and expose missing data for additions,
**And** previous whole-day coverage cannot remain complete merely because the old revision was prepared,
**And** offline manual additions can be saved when existing access permits, but never-downloaded source data stays missing; source retrieval waits for connectivity,
**And** expose the revision for later notice-relevance integration without fabricating notices or resetting unchanged source-version acknowledgement state.

**Given** local confirmation, synchronization and reopening,
**When** the existing authenticated FastAPI/PostgreSQL path accepts or rejects the revision batch,
**Then** enforce owner, writer authority, expected server revision and atomic domain/event/receipt updates under AD-5,
**And** distinguish local confirmation from server confirmation; only a matching valid receipt acknowledges the immutable batch,
**And** lost responses retry unchanged identities/payload; conflicts preserve permitted local work for explicit resolution rather than overwriting server state,
**And** reopen preserves the revision, draft or pending state that actually committed, including local storage-failure and pending-logout protections.

**Given** a pending or confirmed addition affects the last planned activity,
**When** retention is evaluated,
**Then** apply AD-12 exactly: derived day data expires seven days after confirmed actual end/abort, or seven days after planned final end if the day is never ended; only a confirmed plan revision may change that unended day's planned final end,
**And** never calculate expiry as seven days from addition, confirmation, retry or synchronization time; a revised planned end changes only the permitted day-level reference, not the retention duration or an independent fixed draft deadline,
**And** each unconfirmed revision/import draft expires at the earlier of its original creation plus seven days and the associated day's applicable expiry; reopening, editing, copying old work into a revision or confirming another revision cannot reset that creation time or renew an already applicable earlier fixed deadline,
**And** an unconfirmed proposal or a change not affecting the final planned end cannot move day expiry; confirmed actual end/abort takes precedence over planned end and does not acquire a new grace period when learned on reconnect,
**And** check existing expiry before accepting the revision, so already expired data cannot be revived by a later proposed end; confirmation removes redundant draft copies and all older private revisions/events/receipts remain governed by the same applicable AD-12 day deadline, not new per-revision lifetimes,
**And** plan revision never automatically extends AD-10 access authority or an active-day grant; expired authority follows its separate authorization rules.

**Given** late-in-shift additions, an older unconfirmed draft and retained earlier plan data,
**When** the addition is proposed, confirmed, retried and reopened near the applicable deadlines,
**Then** tests verify the original draft-creation deadline remains fixed, any earlier applicable deadline wins and expired draft/day data cannot reappear under fresh identities,
**And** test a confirmed later final end, a confirmed earlier final end, an unchanged final end and an actual end learned on reconnect against AD-12's respective reference times; the later-end case must not reset draft age or start a seven-day clock from revision time,
**And** active trip, manual pin, performed work and progression are unchanged in every accepted addition case.

**Given** the manual revision surface,
**When** used by touch, keyboard or enlarged text,
**Then** target plan, additions, unchanged work, uncertainties, changed final end and confirm/cancel actions have clear accessible labels and visible focus,
**And** no distinction relies on color alone or requires drag-only ordering.

**Traceability:** FR-2/3/4/5; preparation portions of FR-17/20/24; UX-DR7/8/38/43 and approved split-work/revision ownership extension; FR-6/16 preservation and integration boundary; AD-2/4/5 atomic revisions, AD-6 explicit review, AD-7 no silent plan change, AD-10/11 authority and conflict boundaries, AD-12 retention. E3 owns live movement/progression, E4 notice relevance, E5 complete conflict recovery, E7 final summaries.

**Dependencies:** Implemented Stories 2.3, 2.6, 2.7, 2.8 and 2.9 with inherited foundations. No future story is required to demonstrate additions to a confirmed plan, honest coverage and preservation invariants. Active-driving integration is separately required in E3 before this entry is enabled operationally; source matching remains qualified under 2.2.

**Implementation evidence:** Extra passenger/non-passenger activity in the same day and a later part; Friday 25:30; unmatched addition, duplicate/ambiguous candidate, cancellation, stale base/proposal, concurrent revision rejection, double confirmation, lost response and local write failure; immutable active-pin/performed-state fixtures; partial data after additions; changed final activity/deadline versus unconfirmed proposal and unchanged intermediate parts; closed/expired/unauthorized rejection. Tests are planned, not executed.

**Size boundary:** Additions-only revision transaction and review using existing editors. No file reconciliation, replacement/deletion of existing activities, general conflict-resolution UI, movement engine, linked-person revision or summary rendering. These remain required later scopes; no V1 reduction or capacity commitment.

**Pilot qualification:** Demonstrable revision/preservation evidence contributes to E8-D. E8-P still requires real mounted-device operation through E3's movement policy, offline recovery/sync, notice relevance and final summary/retention integration. E8-E remains actual-shift evaluation. Planning approval does not qualify live updates during a shift.

**Approval:** Approved by the owner on 2026-09-25 with the exact AD-12 retention distinction and late-addition tests: a confirmed revision may change the unended day's planned final end, but cannot restart retention from revision time, renew an earlier fixed draft deadline or resurrect expired/old data under new identities. Active trip, performed work and progression remain unchanged. Planning approval only; this approved copy is canonical.

### Story 2.11: Compare an Updated Shift File Within an Explicit Scope

As the pilot owner,
I want to compare an updated shift file with the correct plan and explicitly chosen scope,
So that I can see additions, changes and possible removals without losing existing work or mistaking a partial file for a complete replacement.

**Acceptance Criteria:**

**Given** an owned, unexpired, nonterminal confirmed own plan and permitted access,
**When** an updated PDF/JPG/PNG is selected from the shift overview,
**Then** visibly identify the target own workday/plan and its base revision, keeping that target visible through import, scope selection and comparison,
**And** require explicit whole-day replacement, replacement of selected work part(s), or additions-only scope before producing removal proposals,
**And** do not infer whole-day replacement from filename, file count or apparent extraction success; other plans remain untouched.

**Given** text/scanned PDFs or a shift spread over several JPG/PNG files,
**When** the updated source is interpreted,
**Then** reuse the qualified shared import/editor flow, transient originals and side-by-side comparison while originals are available,
**And** preserve controllable file order, prior manual draft corrections and duplicate protection when files are added or retried,
**And** expose missing/unreadable/cropped pages or parts and unknown coverage; success on available pages does not establish complete replacement evidence,
**And** incomplete or unknown coverage cannot silently turn unseen activities into proposed removals; show the affected reconciliation as unresolved until explicitly clarified.

**Given** interpreted activities and the selected target scope,
**When** matching them to the confirmed plan,
**Then** use supported activity/source identity, service date, direction, departure and existing provenance, not line number/clock time alone,
**And** preserve Friday 25:30 versus Saturday 01:30 and working-day ordering,
**And** present ambiguous matches for explicit selection, keeping genuinely distinct same-time activities separate,
**And** retain driver corrections and visibly compare source values; no new or delayed result silently overwrites a correction or establishes an unsupported unique match.

**Given** a comparison proposal,
**When** the driver reviews it,
**Then** distinguish added, changed, proposed-removed and unchanged future activities with before/after values and uncertainty,
**And** show affected parts' reporting times/depots, the target scope and any proposed final-end/AD-12 deadline effect,
**And** additions-only never proposes removals; selected-part replacement cannot propose changes/removals outside those parts,
**And** absence from a partial file is not deletion evidence; removal can only be proposed within an explicitly established replacement scope after coverage ambiguity is resolved,
**And** a repeated upload reconciles against existing identities rather than automatically proposing duplicate trips.

**Given** performed work, a manually selected active trip or activities outside the chosen scope,
**When** comparison runs,
**Then** preserve performed evidence, active trip/pin/progression, corrections and out-of-scope activities exactly,
**And** distinguish source disagreement from an authorized change; a source's omission cannot erase performed work or replace the active context,
**And** proposals that would affect protected active/performed state remain visibly unresolved rather than silently applied or reassigned to a similar activity,
**And** all comparisons remain non-operational proposals, with no plan revision or activity-completion event emitted.

**Given** a pending import/match or an existing saved proposal,
**When** the target plan or proposal changes, a response arrives late, or the view is reopened,
**Then** check owner/day/target/base revision and attempt/input identity before using the result,
**And** mark stale comparisons for new reconciliation and review rather than displaying them as current,
**And** save/reopen retains permissible interpreted fields, chosen scope, corrections and unresolved matches, while explaining that originals must be selected again for source comparison,
**And** persist the selected scope, target plan identity and exact compared base plan revision together with the proposal, and display them on reopening so the comparison basis remains explicit,
**And** if the current base plan has since changed, label the proposal stale and prohibit its use until comparison and review against the current plan are repeated; do not silently rebind its stored base revision,
**And** cancellation/failure leaves the confirmed plan in force; no automatic activation or implicit confirmation is offered by this slice.

**Given** proposal persistence and cleanup,
**When** local storage, synchronization, retry, logout or expiry occurs,
**Then** atomically store draft changes/events, use the inherited authenticated PostgreSQL path and acknowledge only matching immutable batch receipts,
**And** retain recoverable input on permissible failures without reporting a failed save as successful,
**And** enforce ownership, pending-revocation locks and the earlier applicable AD-12 draft/day deadline from Story 2.10; proposed later final ends cannot extend the draft or current day deadline,
**And** delete transient originals on success/failure/cancel/interrupted processing and remove redundant/expired private copies without resurrecting them through retry.

**Given** target, scope and comparison controls,
**When** used with touch, keyboard or enlarged text,
**Then** added/changed/removed/unchanged states have explicit labels, readable before/after values and accessible focus/error handling,
**And** target/scope changes visibly invalidate affected comparison results and require re-review,
**And** operational entry later uses E3's shared movement policy; until integrated, demonstrate in preparation and protected-state fixtures rather than claiming safe live-shift use.

**Traceability:** FR-2/3/4/5; NFR-2/3; UX-DR4/7/8/38/42/43 and revision ownership; AD-1/6 import boundary/transient files, AD-2/4/5 protected persistence/identities, AD-7 qualified matching, AD-10/12 access/retention. Preserves FR-6/20 operational-context boundaries without implementing live progression or full recovery.

**Dependencies:** Implemented 2.4/2.5 import, 2.6 matching, 2.9 part identity and 2.10 revision-draft/comparison foundations with their qualifications. Applying replacements/removals is not needed to demonstrate a correct, saved scoped proposal and is deliberately excluded here; it remains required in the subsequent E2 story.

**Implementation evidence:** Whole-day/selected-part/additions scope; incomplete and unknown source coverage; multi-image overlap/retry; same-line/time distinct journeys; manual/source disagreement; repeated upload; changed/removed/unchanged future activities; immutable performed/active/out-of-scope fixtures; stale base/late responses, cancel, reload/reselection, receipt/write faults and expiry. Tests are planned, not run.

**Size boundary:** Scoped comparison and recoverable proposal only, reusing existing extraction/matching/editor code. No replacement/removal commit, linked-person revisions, general merge engine, movement engine or automatic operational changes. The next slice supplies explicit confirmation and atomic application; no V1 requirement is removed.

**Pilot qualification:** Repeatable comparison contributes to E8-D. E8-P requires subsequent apply/preservation integration, actual import layouts and real tablet/movement/offline behavior before use during actual shifts. E8-E remains separate evaluation.

**Approval:** Approved by the owner on 2026-09-25 with scope and compared base revision persisted/displayed with the proposal. A changed base plan makes the proposal stale and requires fresh comparison before use. Absence from a partial file alone never justifies proposed deletion. Planning approval only; this approved copy is canonical.

### Story 2.12: Confirm and Atomically Apply a Scoped Own-Plan Revision

As the pilot owner,
I want to explicitly confirm the reviewed changes to my own plan,
So that the intended remaining work becomes authoritative without partial replacement, lost evidence or an unintended change of active trip.

**Acceptance Criteria:**

**Given** an owned, unexpired proposal with stored target, scope and base revision,
**When** final review opens or resumes,
**Then** display that comparison basis, additions, changed before/after values, proposed removals and unchanged work with affected parts' reporting times/depots,
**And** check that the base revision is still current; a stale proposal cannot be confirmed until it has been compared and reviewed again,
**And** changed proposal content, scope or target invalidates the review rather than silently retaining confirmation eligibility.

**Given** the proposal contains ambiguity, missing source coverage or a proposed removal,
**When** the driver prepares to confirm,
**Then** require resolution of identity, scope and temporal ambiguity necessary to apply the changes safely,
**And** unknown source matches/stops/bus remain permitted with explicit missing labels once blocking ambiguity is resolved; confirmation is not source verification,
**And** require explicit confirmation of the displayed removals within the established replacement scope; additions-only cannot remove anything and absence from a partial file alone never authorizes removal,
**And** keep the current confirmed plan in force if required resolution or confirmation is missing.

**Given** a current, resolved, reviewed proposal,
**When** the driver explicitly confirms it,
**Then** validate the exact target, base and proposal revisions and protected activity state inside the local commit boundary,
**And** atomically apply only the reviewed in-scope future changes, advance the plan revision and persist the typed revision event before showing local success,
**And** retain identity for matched existing activities and assign stable identities only to actual additions; preserve manual/source provenance of explicitly accepted field changes,
**And** no failure may leave some proposed replacements/removals applied and others unapplied; cancellation and failed local commit preserve the prior plan.

**Given** performed work, active trip/pin/progression, manual corrections or out-of-scope plans/activities,
**When** confirmation runs, including after operational state changed since review,
**Then** recheck protection and preserve those facts and active context; a formerly future activity that is now active/performed cannot be silently replaced or removed,
**And** require fresh comparison for affected conflicts rather than silently skipping protected changes while claiming the whole reviewed proposal was applied,
**And** only explicitly reviewed changes to eligible future fields may replace their prior values; refresh or matching alone never overrides manual corrections,
**And** a missing active trip in the uploaded source cannot switch the selected trip or falsify completed/aborted work; tests use protected-state fixtures before E3 integration.

**Given** duplicate confirmation, repeated upload or an uncertain response,
**When** application/synchronization is retried,
**Then** use stable proposal/application and immutable event/batch identities so the revision and its effects occur once,
**And** reopening distinguishes a committed local revision awaiting server acknowledgement from an unapplied proposal; do not apply an already committed revision again,
**And** authenticated FastAPI/PostgreSQL acceptance atomically validates ownership, writer authority and expected server revision with domain changes, deduplication and matching receipt under AD-5,
**And** a matching receipt alone marks server confirmation; backend conflicts preserve permitted local work for explicit resolution without partial backend writes, silent rollback or blind overwrite.

**Given** a revision changes remaining work,
**When** coverage is updated,
**Then** publish the new plan and its honest coverage relationship consistently, preserving still-applicable data while invalidating changed/removed associations for current-plan use,
**And** identify added/changed trips needing downloads; an old complete manifest cannot make the revised day complete,
**And** offline confirmation is possible only with permitted access and sufficient reviewed local facts; missing external data remains missing and cannot be fetched by implication,
**And** record the applied revision and necessary before/after provenance for later summary and notice-relevance integration without creating source notices or resetting unchanged notice-version states.

**Given** a proposed change affects the combined planned final end,
**When** the revision is confirmed,
**Then** use Story 2.10's exact AD-12 criteria: only a confirmed revision changes a never-ended day's planned-end reference; no seven-day clock starts at revision time,
**And** fixed draft creation deadlines and any earlier applicable limits remain enforced; no expired data can be revived under fresh identities and redundant proposal/draft copies are removed under AD-12,
**And** actual end/abort overrides planned end, terminal days cannot be revised, and old revisions/events/receipts share their applicable day deadline rather than independent new lifetimes,
**And** no retention change automatically extends AD-10 access/grant authority; late responses, logout and storage failures cannot bypass lock/expiry checks.

**Given** final review is operated by touch, keyboard or enlarged text,
**When** the driver inspects and confirms/cancels,
**Then** clearly identify the target, scope, removals, changed values, final-end effects, local/server status and recoverable errors with accessible labels and focus,
**And** before enabling use during an actual shift, E3 must connect both entry and confirmation to the shared movement permission, cancelling/preventing an uncommitted action when permission is lost; no second movement engine is introduced.

**Traceability:** FR-2/4/5 and preservation aspects of FR-6/17/20/24; NFR-2/3; UX-DR7/8/38/42/43 and revision ownership; AD-2/4/5 atomic changes/receipts, AD-6 explicit confirmation, AD-7 no silent plan change, AD-10/11 authority/conflicts, AD-12 cleanup/expiry. E3 retains runtime permission/progression, E4 relevance, E5 full conflict recovery, E6 linked plans, E7 summary rendering.

**Dependencies:** Implemented 2.10 revision application foundation and 2.11 persisted comparison, including their prerequisites. Preparation UI and domain fixtures demonstrate this slice without a future story. Operational driving and linked-plan integrations remain separately required before those uses are available.

**Implementation evidence:** Whole-day/part replacement and additions-only; explicit removal, partial-file omission rejection, stale proposal/base/scope, activity becoming active/performed during review, preserved pin/progression; partial-write fault injection, duplicate tap/retry/reupload, lost receipt, backend conflict, reopen of unapplied versus locally applied proposal; changed data coverage, offline missing facts, final-end/old-draft expiry and terminal/owner/logout rejection. PostgreSQL integration evidence is required; no tests run during planning.

**Size boundary:** Extend the existing revision transaction to reviewed eligible replacements/removals and their commit-time checks. No new importer, general merge/conflict-resolution UI, runtime movement engine, linked-plan repair or summary UI. These remain assigned V1 obligations, not deferred requirements.

**Pilot qualification:** Repeatable end-to-end own-plan revision supports E8-D. E8-P still requires actual file/layout coverage, mounted-device movement restrictions and integrated recovery, relevance and summary/retention checks. E8-E remains subsequent actual-shift evaluation.

**Approval:** Approved by the owner on 2026-09-25 with the described result, scope and acceptance criteria. The owner requested continuation to the next individual story. Planning approval only; this approved copy is canonical.

## Epic 3: Follow and Correct the Actual Trip Safely

The driver can select and correct the actual trip, follow qualified progression and use controls under the shared movement policy. FR-6–11/16, runtime FR-3 fallback and FR-22 evidence apply with NFR-1/2/4 and AD-9. Early device qualification precedes evidence-dependent implementation; E3 does not claim completed E5 recovery or E7 ending.

### Story 3.1: Qualify Position and Speed Observations on the Pilot Tablet

As the pilot owner,
I want evidence of the position and speed observations actually available on the intended tablet/browser,
So that driving behavior uses realistic quality rules and explicit uncertainty rather than assumed sensor capabilities.

**Acceptance Criteria:**

**Given** the actual pilot Lenovo tablet and Brave browser,
**When** a minimal foreground diagnostic probe is run in a browser context that can exercise the required permissions,
**Then** record the actual device/OS/browser versions, mount/location, permission settings, network arrangement and test conditions,
**And** distinguish unavailable hardware/browser access from permission denial, missing values, stale observations and failed acquisition,
**And** do not assume a native app, accelerometer, background operation or that a desktop simulation qualifies the tablet.

**Given** controlled stationary and moving observations with independently identified reference events,
**When** position and speed are sampled,
**Then** evaluate their quality separately, recording observed age, reported accuracy, delivery intervals and plausible sequence, including null/unknown speed versus a valid zero,
**And** report availability and observed limitations without treating a reported accuracy figure or speed value alone as proof of reliability,
**And** derive evidence-backed candidate quality/freshness rules for later AD-9 implementation, with units, rationale and unresolved cases; do not invent thresholds or change adopted movement-policy boundaries.

**Given** reproducible cases for initial acquisition, denied/revoked permission, loss after valid zero/low/moving speed, recovery, network loss and page/device interruption,
**When** the probe exercises those cases where feasible,
**Then** report which cases actually ran and what observations the browser delivered,
**And** distinguish network loss from loss of usable position/speed; retain the approved rule that unknown speed is not standstill,
**And** identify evidence needed to persist first-valid-speed history and outage timing across restart without giving a fresh startup exception,
**And** label induced or synthetic failures separately from real signal-loss evidence; untested cases remain explicitly unqualified.

**Given** a valid position and speed observation followed by at least five minutes without a new usable observation,
**When** the diagnostic probe records the outage and subsequent recovery,
**Then** document separately the last valid sample time, when position and speed each become too old under the evaluated quality rules, and what the browser actually reports throughout (including silence, errors, null values or repeated stale values),
**And** distinguish the freshness limit from the approved five-minute interaction exception; five minutes never makes the old position/speed usable again,
**And** use independently observed departures/passages as ground truth, with no driver operation while moving, to assess whether the available position evidence realistically supports progression within 100 metres after passage,
**And** report unsupported/uncertain progression during the outage explicitly, including any recovery limits; do not infer observed passage from schedule or elapsed time.

**Given** an observable route segment with independently marked actual stop departure/passage events,
**When** field sampling can be performed safely with a separate observer or unattended capture,
**Then** assess whether observed accuracy/frequency plausibly supports the later stop-progression requirement and record tested conditions and counterexamples,
**And** treat the at-most-100-m target as distance travelled after actual passage/departure, never a proximity radius proving passage,
**And** include the reported approximately 250-m stop-spacing scenario where representative conditions are available, without presenting it as a verified network minimum,
**And** make clear that this probe cannot pass the finished progression requirement: integrated state-machine/device evaluation is still required under E8-P.

**Given** a field observation involves a vehicle,
**When** the test is arranged and conducted,
**Then** it requires no driver interaction with diagnostics while moving and does not rely on an unqualified app for operational decisions,
**And** use consented, anonymized test material and avoid passenger/employee identifiers or real shift documents,
**And** keep only the minimum temporary observation data necessary for analysis, delete raw position traces after analysis and retain sanitized timing/error summaries rather than a permanent GPS track in the app, repository or CI artifacts.

**Given** collected observations and gaps,
**When** the qualification report is completed,
**Then** provide a reproducible case matrix, actual results, limitations and candidate quality rules for position and speed separately,
**And** explicitly conclude what works, what needs uncertain/manual fallback and what is currently unsupported or untested,
**And** negative evidence triggers an owner decision on the further solution; it neither silently removes V1 requirements nor changes AD-9 or the approved startup/five-minute movement policy,
**And** state which follow-up implementation/device cases are still necessary before claiming safe interaction gating or compliant stop progression.

**Traceability:** FR-6/7/8/9/16 sensing prerequisites; NFR-1/2/4; UX-DR14/15/25/44 and EXPERIENCE Responsive & Platform; AD-9 separate position/speed quality and field target, AD-12 no permanent raw GPS track. Wake lock, sound and automatic-theme capability remain separate required device checks; this focused report does not qualify them.

**Dependencies:** Actual target tablet/browser and safe test access, not a future application story. A minimal diagnostic probe may be created during implementation of this qualification task; no production progression/movement engine or service provisioning is required. If the device or safe reference observations are unavailable, report the unqualified cases and obtain the necessary evidence later rather than claiming completion of those tests.

**Evidence boundary:** A report with negative findings can complete the investigation while leaving capability qualification failed. This early E3 work informs implementation and contributes evidence to E8-P; synthetic cases may support E8-D but cannot replace actual device evidence. E8-E remains the later three-workday evaluation. No tests, probe implementation, provisioning or readiness workflow were run while drafting this story.

**Size boundary:** Position/speed acquisition quality and diagnostic evidence only. No automatic trip selection, passage detection engine, operational controls, full recovery, raw tracking feature, browser migration or assumed platform guarantees. Other device capabilities remain explicit subsequent qualification/integration work.

**Approval:** Approved by the owner on 2026-09-25 with a five-minute outage after valid position/speed, separate documentation of sample expiry and browser output, and an honest 100-m feasibility assessment against independently observed passages without driver interaction while moving. Planning approval only; this approved copy is canonical.

### Story 3.2: Apply Movement Restrictions with Honest Startup and Outage States

As the driver,
I want restricted controls to clearly reflect reliable movement or the approved unknown-speed exception,
So that their availability is predictable and an unavailable speed is never presented as confirmed standstill.

**Acceptance Criteria:**

**Given** permitted access to a confirmed own day in driver context,
**When** qualified browser observations arrive or age out,
**Then** evaluate position and speed quality separately using evidence-supported rules from 3.1 in the shared React-independent TypeScript state machine,
**And** null, stale, rejected or missing speed is unknown rather than zero; retained observations do not become fresh on reload,
**And** quality rejection, loss and recovery transitions are explicit and testable; no schedule or proximity inference substitutes for reliable speed.

**Given** reliable speed is zero, above zero up to 6 km/h, or above 6 km/h,
**When** Menu and the existing Skiftdetaljer/revision actions are rendered or invoked,
**Then** allow the restricted driver actions only at reliable zero, and visibly lock them at every reliable speed above zero,
**And** keep Menu visible with a textual reason; movement immediately closes restricted detail/review access while preserving its saved draft,
**And** recheck permission when a confirmation commits, cancelling/preventing an uncommitted action if permission was lost; do not roll back an action already atomically committed,
**And** publish this same permission for future arbitrary trip/stop selection, notice details/source/acknowledgement and operational submenu consumers, without claiming those features already exist.

**Given** genuine startup before the first valid speed observation,
**When** restricted controls are used,
**Then** allow the adopted startup exception without a five-minute wait, clearly labelling speed unknown,
**And** the first valid speed permanently ends that startup exception for the ongoing context, including a valid zero,
**And** the exception never bypasses sign-in, pending logout, confirmed-plan requirements or expiry.

**Given** usable speed is lost after a previous valid observation, including valid zero/low speed,
**When** the shared policy enters the qualified outage state,
**Then** lock restricted controls for five minutes from the established outage onset and show the remaining time beside Menu,
**And** at five minutes with speed still unknown, enable only the controls permitted by the adopted outage exception without labelling the vehicle stationary,
**And** sample freshness thresholds remain separate from this timer: expiry of five minutes does not validate old speed/position or claim usable progression,
**And** an internet outage alone does not start a GPS-loss exception when usable sensor observations continue.

**Given** an ongoing outage, invalid sample bursts or reliable recovery,
**When** observations change,
**Then** stale/invalid samples do not repeatedly reset the outage or manufacture recovery,
**And** reliable recovery immediately cancels the countdown and applies the current speed rule; recovered movement stays locked with a movement reason,
**And** a subsequent qualifying outage starts a new interval; usable position without usable speed cannot assert standstill,
**And** document the qualified onset/recovery rule from 3.1 rather than inventing unsupported sensor thresholds.

**Given** first-valid-speed history and an established outage interval,
**When** the view closes/reopens or the compatible application restarts,
**Then** restore the minimal history/timing so restart neither grants a fresh startup exception nor restarts an existing five-minute interval,
**And** restored speed is not trusted as a fresh observation; evaluate its age before determining permissions,
**And** unreadable/failed state storage produces explicit uncertainty and cannot grant startup or an elapsed-outage exception without a trustworthy basis,
**And** qualify elapsed-time handling across suspension/restart and clock changes; unsupported timing remains explicitly unresolved rather than enabling controls by guessed elapsed time.

**Given** the policy changes or an E2 revision is confirmed through its guarded entry,
**When** required local persistence and synchronization occur,
**Then** persist only minimal operational recovery facts under the existing atomic state/event conventions, preserving manual work and the immutable outbox,
**And** protect any synchronized private recovery facts with authenticated FastAPI/PostgreSQL ownership/revision checks and matching receipts; do not stream raw sensor observations to the backend,
**And** enforce logout, expiry and AD-12 cleanup on all introduced copies without storing a permanent GPS track,
**And** sensor updates do not require a server response to restrict controls; persistence failure cannot leave movement-sensitive actions enabled based on obsolete state.

**Given** the visible Menu/countdown and shared permission output,
**When** tested with keyboard, touch and assistive technology,
**Then** display readable reason/countdown text, no color-only state, and announce availability changes rather than every countdown second,
**And** preserve the separate approved exceptions for always-available theme controls and direct GPS-loss previous/next-stop actions in the permission contract; their actual controls remain later stories,
**And** no obsolete 6-km/h detail threshold or 30-second collapse grace period overrides the adopted zero-speed rule.

**Given** genuine startup or an elapsed qualified outage,
**When** an otherwise restricted action is available,
**Then** test distinct visible startup-exception and outage-exception states, both labelled Hastighet ukjent with an explanation of why the action is available,
**And** neither label implies confirmed standstill; reliability is determined by the actual quality limits established in 3.1, not hardcoded unqualified assumptions,
**And** tests restore an ongoing outage and replay a stale zero sample across restart: neither restart nor that sample opens controls by itself, resets the existing five-minute interval or creates a fresh one,
**And** a valid already-elapsed outage may still permit its labelled exception after recovery of trustworthy history; only genuinely reliable new observations establish a new recovery/outage cycle.

**Given** restricted detail, selection or review opens under the shared movement policy,
**When** it opens, is cancelled or closes because movement resumes,
**Then** move keyboard focus into the opened surface and return it to its invoker on ordinary cancellation/closure,
**And** after movement-triggered closure move focus to an appropriate visible control; focus must never remain in hidden content,
**And** cancellation preserves saved data; test focus before and after motion-triggered closure and cancelled review.

**Traceability:** FR-16; movement prerequisite for FR-6/9/11 and revisions; NFR-1/2; UX-DR13/14/15/38/39 and relevant UX-DR8/23/24 boundaries; AD-2/3/9 one local engine, AD-5 minimal persistence, AD-10/12 access/retention. E5 still owns full offline boot/authority/recovery integration.

**Dependencies:** Actual 3.1 quality evidence sufficient to define tested observation validity; planning approval alone is insufficient. Implemented E2 through 2.12 supplies the confirmed-plan overview/revision actions and E1 foundations. Negative qualification findings require an owner solution decision, not invented reliable sensing. No later trip-selection or notice implementation is needed to demonstrate the shared permission and guarded existing actions.

**Implementation evidence:** Valid zero/low/high speed, null/stale/rejected speed, startup, five-minute loss after each valid-speed category, just-before/at/after expiry, invalid bursts, separate position/speed loss, network-only outage, recovery and new outage; reload/suspend/clock/storage faults, motion between review and commit, preserved draft, access/expiry and accessible countdown. Deterministic fixtures verify the state machine; actual tablet tests verify browser behavior. Tests are specified, not executed here.

**Size boundary:** Shared movement permission and existing Menu/overview/revision integration only. No active-trip matching, stop progression, new notice or theme UI, mentor roles, active-day grant or full recovery engine. Later consumers must reuse the same policy rather than duplicate it.

**Pilot qualification:** Integrated fixture tests support E8-D. E8-P requires real mounted Lenovo/Brave behavior and later full driving/notice/recovery integration; no guarantee of absolute prevention of driver interaction is made. E8-E remains subsequent field evaluation.

**Approval:** Approved by the owner on 2026-09-25 with distinct labelled startup/outage exceptions, both explicitly showing unknown speed and the reason controls are available. Restart/stale-zero tests must neither manufacture access nor reset/start a new five-minute period. Actual 3.1 quality limits determine reliability. The owner also approved the explicit UX-DR39 focus entry/restoration and movement-triggered closure tests at the E3 checkpoint on 2026-09-25. Planning approval only; this approved copy is canonical.

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

**Approval:** Approved by the owner on 2026-09-25 with the described result, scope and acceptance criteria. Planning approval only; this approved copy is canonical.

### Story 3.4: Select the Initial Trip from Qualified Plan, Position and Time Evidence

As the driver,
I want the assistant to select the initial trip only when the confirmed plan, usable position and current time support one candidate,
So that starting is simple without a confident-looking guess when trips overlap or evidence is missing.

**Acceptance Criteria:**

**Given** an owned, unexpired confirmed own day with authority to start it and no active trip in its current tracking context,
**When** initial selection is evaluated,
**Then** consider the confirmed plan, qualified position and current time together, using the existing service-date/source identities and downloaded trip evidence,
**And** use actual 3.1 quality limits and the shared AD-9 state machine; nearby stops, line number or scheduled departure alone are insufficient,
**And** document/test the selection criteria and evidence that distinguish candidates rather than silently choosing the first or nearest result,
**And** exclude unconfirmed drafts, other plans and ineligible completed/aborted activities; an initial passenger-trip choice does not mark preceding non-passenger work performed.

**Given** the combined evidence supports exactly one eligible initial trip,
**When** automatic selection commits,
**Then** reuse Story 3.3's atomic selection/persistence path with automatic provenance, retaining the relevant minimal evidence basis and plan revision,
**And** show the actual selected route and destination/direction only after commit,
**And** selection itself does not prove stop arrival/passage or start fabricated progression,
**And** retain the manual correction path through Menu under 3.2; automatic selection requires no driver interaction while moving.

**Given** several candidates remain plausible, including overlapping lines or opposite directions at shared stops,
**When** initial selection is presented,
**Then** show distinguishable candidates with route, destination/direction, departure and applicable date context and require an explicit choice before starting the trip's driving view,
**And** use the shared movement permission for opening/committing the interactive choice; if locked, keep a concise unresolved status and visible Menu/reason rather than demanding interaction,
**And** test multiple candidates while choice is locked: show a simple explicit status that the active trip must be selected when controls become available; do not start an arbitrary trip's driving view or prompt the driver to resolve ambiguity while driving,
**And** record the chosen candidate as manual selection with the same pin/provenance as 3.3; cancelling leaves no falsely selected trip.

**Given** no supported candidate, missing/stale position, insufficient trip data or an untrustworthy time basis,
**When** initial matching cannot establish a supported unique trip,
**Then** explain the limitation distinctly from a multiple-candidate result and offer direct selection from the confirmed plan under 3.3/3.2,
**And** do not substitute timetable-only certainty, simulated location or a source journey outside the confirmed plan,
**And** missing stops retain the approved recovery/missing-list handling and do not prevent permitted manual selection,
**And** retained observations do not become fresh when reopening, and connectivity alone does not establish position quality.

**Given** Friday service time 25:30 or a delayed initial trip near another scheduled departure,
**When** the candidate set is evaluated,
**Then** preserve Friday service identity and Saturday 01:30 calendar representation with the confirmed working-day order,
**And** test multiple similarly timed trips and shared-stop directions against checked expected candidates,
**And** no simplistic closest-departure or proximity rule may silently discard a plausible delayed trip; unresolved evidence requires choice.

**Given** a trip has already been selected automatically or manually,
**When** a new observation, scheduled departure, source refresh or initial-selection result arrives,
**Then** initial selection cannot replace that active trip; a delayed trip remains active until actual end or explicit permitted context change,
**And** manual correction stays authoritative and later-trip selection remains a separate state-machine transition, not a rerun of startup matching,
**And** reopening the existing context restores selection rather than treating it as an empty startup.

**Given** the candidate computation is pending while the plan, authority or selection context changes,
**When** it would commit or a displayed candidate is chosen,
**Then** revalidate owner/day/plan revision, current context, activity eligibility and evidence freshness at commit,
**And** a newer manual choice wins over stale automatic work; changed relevant inputs require reevaluation instead of silently using the stale result,
**And** double callbacks/retries cannot create duplicate selection events or overwrite committed state.

**Given** local selection and subsequent synchronization/reopen,
**When** storage fails, a server response is lost or a conflict occurs,
**Then** reuse 3.3's atomic state/event storage, authenticated PostgreSQL transaction, immutable retries and matching receipt rules,
**And** failed local commit does not display an active selection; server uncertainty remains distinct from locally committed selection,
**And** preserve the selected trip, provenance and movement history under existing access/logout/expiry rules with minimal evidence and no permanent raw GPS track,
**And** an expired ordinary login cannot authorize starting a prepared/new day through the existing-day continuation exception.

**Traceability:** FR-6 initial automatic/ambiguous/no-candidate selection, FR-3 missing-data fallback, FR-16 interactive choice and foundational FR-20 recovery; NFR-1/2/3; UX-DR5/10/13/14/16/38/44; AD-2/5 atomic state, AD-7 dated identity, AD-9 qualified observations/manual authority, AD-10/12 authority/retention.

**Dependencies:** Implemented 3.3 and its inherited 3.1/3.2/E2 foundations. Actual sensor/source qualification must support the selected criteria; negative findings require the established owner decision, not guessed reliability. No future stop-progression or automatic-transition story is needed to demonstrate initial choice and manual fallback.

**Implementation evidence:** Unique/multiple/no supported candidate; missing/stale position and incomplete data; overlapping 20/24 and opposite directions; Friday 25:30; delayed trip versus later departure; valid time/position separately insufficient; movement-locked choice; manual selection racing automatic result; changed plan, duplicate callback, failed local commit/lost receipt and reopen. Separate deterministic fixtures from actual target-device validation. Tests are planned, not run.

**Size boundary:** Initial trip selection only, reusing existing selector/display/persistence. No later-trip switching, full stop display, arrival/departure detection, interruption/skip actions, mentor context or new access-grant implementation.

**Pilot qualification:** Repeatable initial-selection scenarios support E8-D. Real target-device accuracy, mounted interaction and full progression/recovery integration remain E8-P requirements; E8-E remains subsequent field evaluation.

**Approval:** Approved by the owner on 2026-09-25 with a simple explicit waiting status when ambiguous candidates exist and movement rules lock selection. No arbitrary driving view or request to resolve ambiguity while driving. Planning approval only; this approved copy is canonical.

### Story 3.5: Read the Active Trip and Three-Stop Sequence Without False Location Claims

As the driver,
I want the relevant current or next stop to dominate a stable driving view,
So that I can understand the actual trip and supported stop context with a brief glance.

**Acceptance Criteria:**

**Given** a committed actual trip selection,
**When** its driving view opens,
**Then** persistently display its route, destination/direction and clock using the accepted DESIGN hierarchy and readable landscape-tablet layout,
**And** exclude personal imported details; physical bus, vehicle duty and passenger-trip identity remain distinct,
**And** retain the always-visible Menu with 3.2's lock/reason/countdown and its existing trip-selection and Skiftdetaljer actions,
**And** trip selection alone supplies no current-stop or passage evidence; show unknown progression until supported state exists.

**Given** explicit supported at-stop state for the selected trip,
**When** the three-stop view renders,
**Then** make the current stop dominant and show the vertical sequence top-to-bottom as stop after next, next, CURRENT highlighted,
**And** omit the previous stop from this adopted at-stop baseline; do not implement the exploratory four-stop alternative,
**And** distinguish upcoming stops from current location through text roles and hierarchy, not color alone.

**Given** explicit supported between-stop state,
**When** the view renders,
**Then** make the next stop dominant and show the vertical sequence top-to-bottom as stop after next, NEXT highlighted, departed stop,
**And** identify the departed stop as past context rather than current location,
**And** rendering the state never infers departure/passage from the clock, scheduled time or a visual animation.

**Given** a confirmed sequence boundary, short route or unusable/missing stop data,
**When** the corresponding slot renders,
**Then** use the adopted dash and explicit no-more/no-previous label where the sequence boundary is actually known,
**And** distinguish that from missing/unknown information with an unavailable-data label, retaining Stoppinformasjon mangler where applicable,
**And** never invent stops, wrap the sequence to another trip or present a next-trip stop as an available stop in the current trip.

**Given** last known progress becomes uncertain or is restored without fresh evidence,
**When** the view renders,
**Then** show retained context with explicit uncertainty/manual provenance as applicable, never claiming the bus is still at the last known stop,
**And** test that retained context under unknown progression is labelled uncertain and never presented as a new position observation; preserve the adopted ordering and visual emphasis for supported at-stop/between-stop states,
**And** distinguish selected-trip certainty from location/progress certainty; a manual trip choice does not establish current position,
**And** keep route/destination and control restrictions visible through unknown-position/offline states; connectivity alone cannot refresh position or retained data,
**And** do not implement a new quality or progression engine in the view.

**Given** several initial candidates with movement-locked selection or no actual trip yet,
**When** the entry surface renders,
**Then** retain 3.4's simple unresolved/waiting status and visible permitted route to selection,
**And** do not display any candidate as the active trip or populate its driving stop sequence before selection,
**And** no modal, focus-stealing prompt or required interaction asks the moving driver to resolve it.

**Given** long Norwegian stop names, short/terminal sequences, enlarged text and day/night design tokens,
**When** the view is inspected at the intended landscape-tablet viewport,
**Then** preserve legibility, route/direction and stop-role distinction without overlapping controls, clipped essential names or confusing rearrangement,
**And** use the accepted typography/contrast and forgiving touch-target defaults; keyboard focus and accessible role labels remain understandable,
**And** validate one-to-two-second glance readability separately on the mounted device rather than claiming screenshot tests prove it,
**And** this story tests both adopted palettes but leaves persistent theme selection/Auto behavior to its own required story.

**Given** logout, expiry, a failed state read or a restored active-trip view,
**When** rendering attempts to show private context,
**Then** honor existing access/storage locks and AD-12 checks before displaying private information, preserving the established recoverable-error behavior,
**And** render the existing committed plan/selection/progress state without creating duplicate operational events, changing revisions or resetting retention,
**And** introduce no private asset-cache copy, screenshot archive or redundant database table for presentation; retain E1/E2/E3 authoritative persistence and receipt semantics.

**Given** supported current/next/departed stop state changes or retained context becomes uncertain,
**When** the accessible view communicates that change,
**Then** expose meaningful stop-role/status changes without moving focus, announcing every sensor poll or repeating unchanged announcements,
**And** test a fresh state change, identical repeated observations and restored uncertain context separately,
**And** associated notice-warning descriptions remain required E4 integration; this view does not invent a notice or its source status.

**Traceability:** FR-7 as explicitly superseded by approved UX, display portions of FR-6/9/16; NFR-1/2/3; UX-DR10/11/12/13/23/38/40/44; DESIGN typography/layout/tokens; AD-2 committed-state rendering, AD-9 shared operational state and honest evidence, AD-10/12 access/privacy. Runtime FR-8 progression and notice-driven emphasis under E4 remain later integration.

**Dependencies:** Implemented 3.3/3.4 and their shared movement/plan foundations. At-stop/between-stop/manual/uncertain states are verified with labelled isolated test fixtures; the live operational surface remains unknown until actual progression evidence is available. No future story is required to implement and test the presentation contract.

**Implementation evidence:** At-stop and between-stop role/order assertions, first/last/one-/two-stop routes, missing list versus true boundary, long names/enlargement/palettes, manual/uncertain/restored context, locked ambiguous selection, permission/status visibility and logout/expiry/read failure. Component checks verify rendering causes no operational mutation. Device glance qualification remains outstanding; no tests are run while drafting.

**Size boundary:** Active-trip/stop presentation and existing Menu integration only. No passage detection, arbitrary/manual stop controls, final-stop timer, non-passenger transitions, theme persistence/Auto, wake lock or notice ingestion. Those remain required subsequent stories.

**Pilot qualification:** Deterministic presentation evidence contributes to E8-D. Actual mounted readability in sun/darkness, live progression and integrated notices/controls/recovery require E8-P; E8-E remains subsequent field evaluation.

**Approval:** Approved by the owner on 2026-09-25 with the adopted ordering and visual emphasis preserved. Retained context under unknown progression is explicitly uncertain, never a new position observation. Registration recovered after the tool interruption. The owner also approved the explicit UX-DR40 meaningful stop-state announcement and unchanged-poll suppression tests at the E3 checkpoint on 2026-09-25. Planning approval only; this approved copy is canonical.

### Story 3.6: Advance the Stop Sequence from Qualified Actual Movement

As the driver,
I want the stop display to follow actual arrival, departure and passage within my selected trip,
So that it remains useful during delays and when passing without stopping.

**Acceptance Criteria:**

**Given** an active trip with a supported stop sequence,
**When** observations are evaluated,
**Then** use the actual quality limits established in 3.1 within the shared AD-9 state machine,
**And** scheduled time or proximity alone never proves arrival, departure or passage; position and speed quality remain distinct.

**Given** observations support actual arrival or departure within the selected trip,
**When** progression is committed,
**Then** update the state consumed by 3.5 with supported stop identity and observed provenance,
**And** preserve the adopted at-stop/between-stop hierarchy without making an upcoming stop a confirmed current location.

**Given** passage without stopping is supported by qualified observations,
**When** progression advances,
**Then** do not require a zero-speed observation or invent dwell,
**And** remain within the supported sequence of the selected trip without fabricating boundary stops.

**Given** independently observed actual departure or passage, including passage without stopping,
**When** the implemented progression is measured on the target device,
**Then** measure distance travelled from that reference event to the updated display and test the at-most-100-m requirement,
**And** use a separate observer or unattended capture without driver operation while moving; neither proximity nor the algorithm's own detection serves as independent ground truth,
**And** record tested conditions, actual distances and deviations; if the target is not achieved, document the failure and do not mark the requirement fulfilled,
**And** actual qualification remains an E8-P obligation, distinct from deterministic logic tests and planning approval.

**Given** stale measurements, position jumps, noisy or otherwise insufficient evidence,
**When** progression cannot be established,
**Then** retain the last committed stop context explicitly uncertain rather than guessing advancement,
**And** retained context is not a new observation, and noise/repeated observations must not produce false advancement or duplicate events.

**Given** an active trip selected automatically or manually,
**When** delays, other departure times or nearby lines occur,
**Then** keep progression within that trip and preserve the manual choice,
**And** reject stale results evaluated for a superseded trip/context rather than transferring its stop index to the current trip.

**Given** a supported progression change,
**When** local storage and rendering occur,
**Then** atomically save state and its necessary event before showing the new progression,
**And** a failed local write cannot appear as successful advancement; retain committed context with explicit failure/uncertainty,
**And** reopening restores context without renewing observation freshness or retention, preserving movement history and access locks.

**Given** committed progress is synchronized,
**When** the backend accepts a batch or its response is lost,
**Then** reuse the inherited authenticated FastAPI/PostgreSQL ownership/revision checks, atomic receipt handling and immutable retries,
**And** only a valid matching receipt changes server-confirmation status; server/network failure does not discard locally committed progress,
**And** preserve minimal necessary evidence under AD-12 without a permanent raw GPS track; downloaded data supports local operation without implying new source retrieval.

**Traceability:** FR-7/8 normal progression, foundational FR-9 uncertainty and FR-6 active-trip authority; NFR-1/2/4; UX-DR10/11/15/16; AD-2/3/5 committed local state and fullstack persistence, AD-9 qualified shared state machine, AD-10/12 access/privacy. All adopted decisions remain binding.

**Dependencies:** Implemented 3.5 with its trip/permission/data prerequisites and actual quality evidence from 3.1. Story approval is not proof of qualified sensor behavior. Deterministic normal-route progression is independently testable before the later fallback/transition stories.

**Implementation evidence:** Supported arrival/departure and passage without stopping, delays and adjacent lines, stale/noisy/jumping observations, duplicate samples, trip-context changes, failed writes/receipts and uncertain reopen. Independently observed field passages/departures measure the 100-m outcome and explicitly record failures. No tests were performed during drafting.

**Size boundary:** Normal supported progression within the selected trip. Manual stop correction, diversion recovery and final-stop/same-route-return transitions remain subsequent required stories; no requirement is removed or marked implemented by this approval.

**Pilot qualification:** Repeatable logic contributes to E8-D. Actual 100-m performance requires E8-P evidence against independent observations, with failure recorded honestly. E8-E remains subsequent actual-shift evaluation.

**Approval:** Approved by the owner on 2026-09-25 with the presented scope/criteria and explicit independent-ground-truth testing including nonstopping passage; missed 100-m targets must be documented, never marked fulfilled. Registration recovered after the tool interruption. Planning approval only; this approved copy is canonical.

### Story 3.7: Correct Stop Progress Manually When Position Is Uncertain

As the driver,
I want to correct the stop context under the approved interaction rules,
So that the selected trip remains usable when positioning is unavailable or progression is wrong, without presenting my correction as GPS evidence.

**Acceptance Criteria:**

**Given** an active trip with a usable stop sequence and lost usable positioning under the actual 3.1 quality rules,
**When** the driving view reflects the outage,
**Then** retain the last committed context with explicit uncertainty and expose direct previous/next-stop controls,
**And** these direct controls follow the approved GPS-loss exception, including while moving and during the five-minute restriction on arbitrary selection,
**And** internet loss alone does not expose them when positioning remains usable; position and speed quality remain separate.
**And** GPS loss is determined by the qualified signal states established in 3.1; unknown speed alone never exposes direct arrows. Test usable position with unknown speed, network-only failure and actual qualified position loss separately.

**Given** the direct GPS-loss controls are available,
**When** the driver intentionally presses previous or next,
**Then** move the manual stop context one supported sequence step within the selected trip, using the existing operational state contract,
**And** each press moves at most one stop within that trip's known list; no repeated callback, long press or boundary condition may turn a single press into a multiple-stop jump,
**And** clearly mark manual provenance without asserting a fresh position, GPS-confirmed arrival or observed dwell,
**And** preserve the active trip/manual trip pin and prior observed/manual evidence; correction does not erase historical events or mark intervening work GPS-observed,
**And** no route-boundary press fabricates a stop or wraps to another trip. Final-stop registration and the special extra Next action for a same-route return must integrate through the subsequent terminal-transition story, not a generic index increment.

**Given** the driver wants to choose an arbitrary correct stop,
**When** the stop sequence is tapped or the stop selector is opened and a choice committed,
**Then** use the same 3.2 permission at entry and commit: reliable standstill, genuine startup exception or elapsed five-minute outage exception,
**And** reliable motion locks arbitrary choice even though direct GPS-loss previous/next may remain available,
**And** unknown-speed exceptions visibly show Hastighet ukjent and why access is allowed; stale zero/restart never bypasses that policy,
**And** cancellation or permission loss before commit preserves the prior committed context and explains the restriction without demanding action while driving.

**Given** an eligible stop in the selected trip is explicitly chosen,
**When** the correction commits,
**Then** update only that trip's stop context with manual origin and clear current/next roles in the 3.5 view,
**And** distinguish repeated stop names/occurrences by sequence and trip context, rather than conflating identical names,
**And** do not infer other-line selection, activity completion, GPS-confirmed passage or actual physical actions from the choice.

**Given** usable position returns after manual corrections,
**When** the observations satisfy the qualified recovery rules,
**Then** hide the direct GPS-loss controls and let the shared engine realign within the currently selected trip using supported fresh evidence,
**And** retain manual correction history and the manual trip pin; recovery cannot choose another line or treat old observations as current,
**And** if returned data is insufficient to identify a stop unambiguously, keep progress uncertain instead of choosing the nearest stop; farther-along/diversion recovery remains the separate required slice,
**And** apply 3.2's independently evaluated speed restrictions immediately; restored position alone does not prove standstill.

**Given** a pending manual action races with reliable position return, trip change or plan/sequence change,
**When** the action reaches its atomic commit boundary,
**Then** revalidate the action's availability, target trip/context and sequence identity,
**And** reject stale actions without applying them to a new context or double-advancing; a callback/retry of the same action applies once while distinct intentional presses remain distinct actions,
**And** preserve deterministic ordering and provenance of committed manual actions and subsequent observations.

**Given** correction, synchronization and reopening,
**When** state is saved or recovered,
**Then** atomically persist corrected context and its typed event before displaying success; failed local writes retain the previous context with an explicit error,
**And** preserve manual origin, trip pin, last observation freshness and 3.2 startup/outage history across reopen; reopening neither refreshes location nor restarts the five-minute interval,
**And** reuse authorized FastAPI/PostgreSQL transactions, immutable batches and matching receipts; server failure does not discard a locally committed correction,
**And** enforce ownership, pending logout/storage locks and AD-12 expiry on every copy, with minimal evidence and no permanent raw GPS track.

**Given** no usable stop list or a known sequence boundary,
**When** stop correction is rendered,
**Then** do not enable a fictitious stop choice or create stop identifiers; show the missing-list or actual boundary reason,
**And** missing-list completion/abort/next-activity remains a separate required fallback story, not falsely claimed as available here.

**Given** the manual controls and selector,
**When** inspected with touch, keyboard and enlarged text,
**Then** use large labelled targets, visible focus and explicit enabled/disabled reasons without color-only distinctions or precise gestures,
**And** keep route/destination, uncertainty and Menu/countdown visible; do not add an automatic modal or require correction while driving,
**And** isolate simulated fault scenarios from operational data during tests.

**Traceability:** FR-9 manual correction/uncertainty/recovery, FR-16 interaction rules, FR-6 manual trip authority and foundational FR-20; NFR-1/2/3; UX-DR11/13/14/15/16/38/44; AD-2/3/5 atomic state and persistence, AD-9 shared operational engine, AD-10/12 access/retention.

**Dependencies:** Implemented 3.2 and 3.6 with inherited 3.1 quality evidence, selected-trip and 3.5 view foundations. Nonterminal manual correction and qualified normal-sequence realignment are independently demonstrable; future terminal/diversion/fallback stories integrate at their boundaries without changing these movement rules.

**Implementation evidence:** GPS loss at reliable zero/low/high speed, direct arrows before/after five minutes, network-only outage, arbitrary selection locked/allowed under each approved state, stale-zero/restart, repeated stop names, boundaries/missing list, intentional multiple presses versus retry, return-of-position/action race, new trip/sequence race, manual history preserved after realignment, failed write/lost receipt and uncertain reopen. Tests are specified, not run.

**Size boundary:** Manual correction within a usable selected-trip stop sequence and normal qualified recovery. No diversion engine, stop-list fabrication, trip switching, terminal completion/return timers, missing-list outcome controls or duplicate movement engine.

**Pilot qualification:** Deterministic exception/correction cases contribute to E8-D. E8-P must qualify actual tablet loss/recovery, mounted controls and integrated terminal/fallback/recovery behavior before actual shifts; E8-E remains subsequent evaluation. The approved in-motion arrow exception is preserved, not a claim of absolute interaction safety.

**Approval:** Approved by the owner on 2026-09-25: GPS loss follows qualified 3.1 signal states; unknown speed alone or network loss does not expose direct arrows. Each press moves at most one stop within the selected trip's known list. Manual corrections remain non-GPS evidence and ambiguous recovery cannot silently overwrite them. Planning approval only; this approved copy is canonical.

### Story 3.8: Recover Stop Progress Within the Selected Trip After a Diversion or Gap

As the driver,
I want the assistant to use supported diversion stops or recognize a later stop on my current trip,
So that progression recovers without inventing a route, switching lines or treating unobserved stops as visited.

**Acceptance Criteria:**

**Given** a selected trip and available evidence for an alternate stop sequence,
**When** the transit adapter evaluates that sequence,
**Then** verify source identity, applicable service date/direction, validity and its supported association with the selected trip using existing qualified contracts,
**And** keep source/version/fetch provenance and unknown metadata explicit,
**And** a general disruption text, nearby line or inferred road path alone cannot establish replacement stops; source failure cannot create a supported diversion.

**Given** a supported applicable alternate sequence,
**When** it is adopted for operational stop tracking,
**Then** retain the confirmed plan/activity identity, active trip and manual trip pin while updating the applicable source-backed stop sequence,
**And** keep the distinction between operational source sequence and a confirmed plan revision; do not rewrite driver-entered facts or confirmed activity scope through a source refresh,
**And** map existing progress only where evidence supports correspondence; ambiguous mapping preserves manual correction/context as uncertain instead of silently selecting a new stop,
**And** feed supported sequence/progress to the existing 3.5/3.6 engine and view, without a second progression engine.

**Given** no supported alternate sequence, or an interval with unobserved progression,
**When** fresh qualified evidence identifies a later stop of the same selected trip,
**Then** permit re-acquisition beyond the immediately next stop, explicitly testing two and ten stops ahead,
**And** use the actual 3.1 quality rules and plausible direction/sequence evidence; proximity or scheduled time alone is insufficient,
**And** resolve repeated stop occurrences, loops and shared/opposite-direction stops using trip/sequence identity rather than names alone,
**And** test a trip that visits the same physical stop multiple times: unambiguous recognition must identify the correct occurrence in the selected trip's sequence; name, stop identifier or proximity alone is insufficient when multiple occurrences remain plausible,
**And** do not require the driver to press through every intervening stop when recovery is unambiguous.

**Given** a supported later-stop recovery,
**When** it commits,
**Then** record the observed recovery and preserve the earlier observed/manual history,
**And** do not backfill skipped-over stops as GPS-observed visits, infer dwell or manufacture completed work during the gap,
**And** display the newly supported context and any remaining uncertainty without erasing prior manual provenance,
**And** visibly indicate the observation gap even after a later stop is recognized, retaining minimal gap/recovery evidence through save/reopen without inventing exact boundaries where unknown,
**And** a jump to a later stop is not evidence that the 100-m target was met for unobserved departures/passages; test two-/ten-stop recovery with gap visibility and no backfilled compliance claim,
**And** automatic evidence-based recovery may span multiple stops, while each direct manual arrow press still obeys 3.7's at-most-one-stop rule.

**Given** fresh but ambiguous observations, an implausible jump, stale source data or conflicting candidates,
**When** recovery cannot establish a supported same-trip location,
**Then** retain the selected trip and the previous context explicitly uncertain; do not pick the nearest stop/line or silently overwrite a manual correction,
**And** keep 3.7's permitted manual path available according to its qualified signal state and 3.2 movement rules, without demanding interaction during motion,
**And** distinguish source-data uncertainty from actual GPS loss: unknown speed or network failure alone never exposes direct GPS-loss arrows.

**Given** the device is offline or a source update fails,
**When** diversion/recovery is evaluated,
**Then** use only available downloaded sequences with honest provenance/freshness and preserve usable prior data,
**And** do not fabricate an alternate sequence or claim a fresh verification; a later recognized stop may still support local recovery on the selected known sequence,
**And** no usable stop list keeps automatic progression disabled with Stoppinformasjon mangler; manual outcome fallback remains a separate required slice.

**Given** source/observation processing overlaps a new manual correction, trip choice or plan change,
**When** an update would commit,
**Then** revalidate current trip/context/sequence revision and qualified evidence against the latest committed state,
**And** a delayed computation cannot overwrite newer manual work or apply to another trip; recompute against current context where supported,
**And** apply sequence/progress changes and necessary events atomically without duplicate recovery effects or partial identity mapping.

**Given** committed recovery and synchronization/reopen,
**When** storage or transport fails,
**Then** inherit local atomic state/event writes, authenticated FastAPI/PostgreSQL ownership/revision checks and immutable matching-receipt retries,
**And** failed local writes leave the prior committed context with explicit uncertainty/error; lost server responses do not discard locally committed recovery,
**And** separate source version updates from operational revisions; source polling alone does not advance the latter,
**And** persist minimal evidence under access/logout and AD-12 expiry rules, never a permanent raw GPS track; reopening does not refresh evidence or restart movement timers.

**Given** recovery reaches a sequence boundary or data ceases to support the selected trip,
**When** the result is presented,
**Then** preserve honest boundary/missing-data states and never switch to another trip as a recovery shortcut,
**And** final-stop completion and same-route-return triggers remain the separately required transition behavior; this slice must not invent them.

**Traceability:** FR-8 diversion/later-stop recovery, FR-9 uncertainty/manual evidence, FR-6 selected-trip authority, FR-3 source/missing-list boundary; NFR-1/2/4; UX-DR11/15/16/23/38/43/44; AD-1/7 qualified source boundary, AD-2/5 atomic state and source separation, AD-9 evidence-based single engine, AD-10/12 access/retention.

**Dependencies:** Implemented 3.7 and its progression/quality foundations plus 2.6/2.8 qualified transit data. Supported alternate-sequence availability must be evidenced through the existing adapter; a fixture demonstrates logic but does not establish real source coverage. Missing provider support returns a documented solution decision without removing V1 scope or adopting bulk ingestion independently. No future notice-ingestion story is required: notice text is not sequence evidence.

**Implementation evidence:** Supported/unsupported alternate sequence; two-/ten-stop recovery, loops/repeated names/shared directions, manual correction versus ambiguous return, source and GPS failures separately, offline known sequence, stale update races, atomic write/receipt faults, reopen/expiry. Use checked reference cases and actual source/device evidence for qualification. The existing 100-m target remains measured against independently observed passage/departure under reliable positioning; unexplained gaps do not justify fabricated compliance. Tests are planned, not run.

**Size boundary:** Selected-trip sequence validation and re-acquisition using existing adapter/state engine. No general road routing/map-matching service, notice-text route inference, new source pipeline, trip switching, manual missing-list outcomes or final-stop transitions.

**Pilot qualification:** Repeatable recovery cases contribute to E8-D. Actual alternate-sequence source support and observed recovery accuracy/latency require E8-P evidence; failures remain recorded gaps rather than passed requirements. E8-E remains subsequent actual-shift evaluation.

**Approval:** Approved by the owner on 2026-09-25 with correct stop-occurrence identity required for repeated visits and a visible retained observation gap. Later-stop recovery does not establish 100-m compliance for unobserved departures/passages. Planning approval only; this approved copy is canonical.

### Story 3.9: Register Final-Stop Arrival and Apply the Correct Next-Activity Trigger

As the driver,
I want final-stop arrival and the transition to subsequent work to follow actual evidence or my explicit manual action,
So that the trip ends correctly without starting a return trip from schedule or arrival alone.

**Acceptance Criteria:**

**Given** a selected non-aborted passenger trip with a known final-stop occurrence,
**When** qualified observations establish final-stop arrival or a permitted explicit manual stop action registers arrival there,
**Then** atomically record passenger-trip completion with trip/stop occurrence, actual registration time and observed or manual provenance,
**And** preserve manual origin without claiming GPS confirmation; a manually registered final arrival counts as completion under the approved rule,
**And** scheduled end, mere proximity, a missing stop list or an ambiguous occurrence cannot establish final arrival,
**And** repeated callbacks/retries record completion only once; an aborted trip is not silently relabelled completed.

**Given** registered final-stop arrival and a next confirmed activity that is not the special same-route return,
**When** the completion commits,
**Then** show Siste stopp for ten seconds for both observed and manual arrival, retaining completed trip identity and the next activity context,
**And** after that interval select the next activity according to the confirmed ordered plan; do not skip a break, transfer, bus change or other non-passenger entry to reach a later passenger trip,
**And** the selected next activity appears with its known type/timing/location and honest unknowns; this transition does not certify that a physical handover, break or travel has occurred,
**And** schedule alone cannot trigger this transition before registered completion. Detailed non-passenger layouts/evidence are a later slice, not an excuse to omit non-passenger entries here.

**Given** the next confirmed activity is an evidence-supported same-route return,
**When** final-stop arrival commits,
**Then** keep the last-stop state instead of starting the return after ten seconds,
**And** require a separate qualified detection of the return trip's starting-stop occurrence before automatic return activation,
**And** line number alone does not establish return identity; use the confirmed activity, direction/service-date and supported stop sequence,
**And** test co-located outbound-final/return-start stops: the original arrival event or its replay cannot simultaneously count as the separate return-start trigger; unresolved evidence keeps the waiting state.
**And** test sustained position while waiting, GPS jitter, scheduled departure and expiry of ten seconds at that shared stop: none can establish an independent return start; retain the waiting state until a separate qualified return-start registration exists,
**And** during qualified GPS loss require the separate intentional Next press after committed final arrival, never reuse the arrival press or infer it from elapsed time.

**Given** qualified GPS loss under 3.1 and a manually registered or retained final-stop state with a supported same-route return,
**When** the driver intentionally presses Next once more after the final arrival has committed,
**Then** start that return trip through the explicit approved manual return action, with manual provenance and no fabricated GPS arrival,
**And** the press that first reaches/registers the final stop cannot also start the return,
**And** distinguish this terminal return action from 3.7's ordinary one-stop progression; no generic list wrap or multiple-stop jump is allowed,
**And** unknown speed alone or internet loss does not enable this GPS-loss action; the existing direct-control movement exception and access checks still apply.

**Given** a completion, a ten-second timer or a return-start event races with correction, plan revision or context change,
**When** the transition would commit,
**Then** revalidate the selected context, completion identity, current confirmed next activity and permission for any manual action,
**And** stale timers/events cannot replace a newer explicit selection or start an activity removed from the applicable plan,
**And** actual completion releases the completed trip's manual pin for the established next-activity flow, but never copies the old pin/progress to the new trip,
**And** preserve prior correction/completion evidence; permitted undo/correction remains through 3.3's selector rather than rewriting history silently.

**Given** the application reopens during Siste stopp or the same-route-return wait,
**When** compatible committed state is restored,
**Then** retain completion provenance and original transition timing; reopening cannot restart the ten seconds, duplicate completion or invent a return trigger,
**And** use trustworthy elapsed-time handling and current context checks; unresolved timing/evidence stays explicit rather than granting a guessed transition,
**And** restored position remains stale until qualified new evidence arrives, preserving movement/outage history.

**Given** the final-stop event follows recovery across an observation gap,
**When** completion and subsequent context are displayed/recorded,
**Then** retain the gap and earlier uncertain/manual evidence; final arrival does not backfill unobserved stop visits,
**And** do not claim the 100-m target was met for unobserved departures/passages,
**And** identify the actual final occurrence when the same stop appears several times in the selected trip.

**Given** no next confirmed activity, uncertain return identity or no known final stop,
**When** the boundary is evaluated,
**Then** show a clear no-next/uncertain/missing-data state as applicable without inventing a trip or final-stop identifier,
**And** do not automatically end the combined workday, start its completed-day deletion clock or resume a terminal day,
**And** missing-list manual completion/abort/next selection and E7's explicit day end remain required separate functions.

**Given** completion or next-context changes are persisted and synchronized,
**When** local writes or backend transport fail,
**Then** use atomic state/event writes before showing success, stable transition identities and authenticated FastAPI/PostgreSQL receipt/revision handling,
**And** lost replies retry immutable batches and only a valid matching receipt marks server confirmation; partial writes cannot leave a completed trip with a contradictory active context,
**And** preserve permitted local facts on conflicts and apply ownership, pending logout, AD-10 authority and AD-12 retention to all copies,
**And** passenger completion or timer progress does not renew authority/retention or store a permanent GPS trace.

**Given** last-stop/waiting/next-context presentation,
**When** shown with touch, keyboard or enlarged text,
**Then** retain route/direction, clock, Menu and movement reasons, with explicit manual/uncertain status and accessible labels,
**And** make a committed context change evident without a blocking prompt while moving; notice presentation must later coexist without altering transition timing.

**Traceability:** FR-10 terminal/return transition, FR-6/11 selected-trip correction boundaries, passenger completion evidence for FR-22; NFR-1/2/3; UX-DR12/14/15/16/18/38; AD-2/5 atomic evidence, AD-9 final-stop/manual/return invariants, AD-10/12 authority/retention. Detailed non-passenger completion and E7 workday end/summary remain separate.

**Dependencies:** Implemented 3.8 and inherited 3.1–3.7 qualified observation, manual controls, selection, view and persistence foundations. E2 supplies confirmed next-activity order. Passenger completion, timer, minimal next-context presentation and return activation can be demonstrated without future non-passenger or summary stories.

**Implementation evidence:** Observed/manual final arrival, duplicate events, aborted-trip rejection, ordinary ten-second transition, intervening non-passenger entry, no next activity, same-route wait beyond ten seconds, qualified separate start detection, co-located/repeated stops, two distinct manual actions at the terminal, speed-only/network-only failures, stale timer versus manual correction/plan change, observation-gap preservation, reopen/time/storage/receipt faults. Tests are planned, not run.

**Size boundary:** Passenger final arrival/completion and next-context trigger with minimal display. No new source/progression engine, full non-passenger screen suite, inferred physical completion, missing-list outcomes, mentor handovers or terminal workday closure.

**Pilot qualification:** Repeatable transition evidence contributes to E8-D. E8-P requires target-device terminal/return behavior and integration with later non-passenger, offline recovery and summary flows; uncertain real-world return detection remains an explicit qualification gap. E8-E remains separate field evaluation.

**Approval:** Approved by the owner on 2026-09-25 with arrival/waiting distinguished from independent return-start registration at co-located final/start stops. Sustained position, GPS noise, schedule or ten-second expiry cannot start the return; qualified GPS loss requires a separate Next press after registered final arrival. Planning approval only; this approved copy is canonical.

### Story 3.10: Follow Non-Passenger Activities Without Inventing Completion

As the driver,
I want clear context for relocation, breaks, layover, bus changes, transfers and depot return,
So that I can follow the whole working day without treating a screen change or scheduled end as proof that work was performed.

**Acceptance Criteria:**

**Given** the next confirmed activity is not a passenger trip,
**When** 3.9's ordinary final-stop transition selects it,
**Then** render that activity rather than skipping ahead to a passenger trip, preserving known timing, location, part and provenance,
**And** retain the preceding Siste stopp period of ten seconds for observed and manual arrival; the same-route-return exception remains 3.9's separate behavior,
**And** display the next confirmed activity when known and explicit unknown/no-next status otherwise, with a persistent clock and movement-governed Menu.

**Given** relocation, meal or their supported combination,
**When** the activity view renders,
**Then** show Tomkjøring with the next starting-stop name for relocation, Matpause for a meal without relocation, and the adopted meal/Tomkjøring/first-stop-after-break composition for the combined case,
**And** preserve known paid/unpaid/unknown meal classification separately from the friendly label,
**And** never count relocation as break time, invent a meal location or infer employment/payment rules,
**And** unknown PDF codes retain their uncertainty; preserve the approved Travel to meaning when applicable rather than relabelling it as pilot-car transfer.

**Given** a planned bus change, pilot-car transfer, depot return or layover,
**When** the activity view renders,
**Then** use centered Bussbytte or Pilotbil, Returner til / Depot on two lines without the blue rail, or Reguleringstid with known timing and next activity, respectively,
**And** physical bus remains distinct from vehicle duty, and a planned change does not silently update the actual bus number or assert a handover occurred,
**And** no pilot-car number is required; unknown locations/times remain visible unknowns,
**And** unconfirmed dispatch changes remain unresolved until the E2 revision flow confirms them.

**Given** a non-passenger activity with known relevant location and timing,
**When** the shared state machine evaluates completion,
**Then** evaluate qualified position and timing together under documented activity-specific rules using 3.1 quality limits, distinguishing supported movement/location facts from the activity's actual outcome,
**And** scheduled end, entering the screen or reaching a location alone cannot certify completion,
**And** position and time alone cannot confirm that a break was taken, relocation was performed as planned, a bus was replaced or a handover occurred; retain Gjennomføring usikker unless evidence specific to that outcome exists,
**And** test all four cases with plausible position/time observations but no outcome-specific evidence: retain the movement/location facts and uncertainty without falsely marking the activity completed,
**And** if required position/location/timing evidence is missing or ambiguous, retain Gjennomføring usikker for later E7 manual summary confirmation rather than filling it in automatically.

**Given** the next activity becomes the displayed context while prior completion is uncertain,
**When** an explicit permitted context choice or supported normal transition advances the view,
**Then** preserve the earlier uncertain outcome and distinguish the context change from completion evidence,
**And** no timetable-driven display update may override an unfinished passenger trip or its manual pin,
**And** do not duplicate initial-trip selection or terminal logic; reuse the existing state-machine paths and 3.2 permissions for interactive actions.

**Given** a combined day contains an intermediate depot visit or a gap before a later work part,
**When** that interval is reached,
**Then** show the next part's reporting time and known depot with an explicit gap state,
**And** never infer rest, meal, transfer or day completion from the interval alone,
**And** keep one day identity and expiry basis; neither intermediate depot return nor arrival at final depot automatically ends the workday,
**And** supply final-depot context for E7's later explicit end/abort flow without claiming that action implemented here.

**Given** a pending observation/context update and a manual choice, plan revision or repeated callback,
**When** a transition or completion would commit,
**Then** validate current plan/activity/context identity and preserve performed evidence and corrections,
**And** reject stale work, apply a supported event once, and record no retroactive completion merely because an added activity's scheduled time has passed.

**Given** an activity state/outcome changes or is reopened offline,
**When** persistence and synchronization occur,
**Then** atomically save state and necessary event before showing success and retain manual/observed/uncertain distinctions after reopen,
**And** use inherited authenticated FastAPI/PostgreSQL ownership/revision validation, immutable retries and matching receipts; failed local writes cannot appear successful,
**And** downloaded plan facts remain usable without inventing missing source data or fresh position; preserve 3.2 movement/outage history,
**And** apply access/logout/storage-error locks and AD-12 expiry to all private copies; activity timing or reopen never renews authority or retention, and no raw GPS archive is introduced.

**Given** each activity composition,
**When** inspected on the target landscape layout, with long labels, keyboard and enlarged text,
**Then** maintain readable hierarchy, explicit activity/uncertainty labels, visible clock/Menu and accessible focus/disabled states,
**And** do not require precise gestures or a response while moving; sensor uncertainty does not silently open arbitrary controls.

**Traceability:** FR-4/5/10, non-passenger evidence for FR-22, foundational FR-17/20; NFR-1/2/3; UX-DR7/12/14/17/18/38/44; AD-2/5 committed evidence, AD-9 non-passenger position-plus-time rule, AD-10/12 authority/retention. Physical replacement correction, missing-list outcomes, E7 summary review and final ending retain separate ownership.

**Dependencies:** Implemented 3.9, E2 split-day model through 2.9 and inherited quality/movement/persistence foundations. E7 is not needed to demonstrate correct activity screens and retained uncertain outcomes; it later consumes that evidence for summary/manual confirmation.

**Implementation evidence:** Each adopted activity composition; relocation+meal versus meal only and unknown classification; missing location, stale position, timing-only and location-only cases; plausible position+timing without specific evidence for break/relocation/bus replacement/handover keeps each outcome uncertain; context change retaining uncertainty; split-day gap/different depots; intermediate/final depot without automatic ending; stale revision, failed write/lost receipt and offline reopen. Actual device tests must qualify activity-specific evidence rules; no tests run during drafting.

**Size boundary:** Existing confirmed own non-passenger activities, their display/context and supported/uncertain outcomes. No payroll/rest-rule engine, physical bus replacement form, new sensor engine, mentor classroom/office context, summary UI or day-end transaction.

**Pilot qualification:** Repeatable activity/display/evidence tests contribute to E8-D. E8-P requires mounted readability, actual position/timing behavior and integration with complete recovery/end/summary flows. Unprovable physical acts remain unverified; E8-E remains subsequent evaluation.

**Approval:** Approved by the owner on 2026-09-25 with position/time supporting movement/location only, not by themselves proof of a taken break, relocation performed as planned, bus replacement or handover. Those outcomes stay uncertain without their own evidence. This owner clarification governs interpretation of the completion criteria. Planning approval only; this approved copy is canonical.

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

**Approval:** Approved by the owner on 2026-09-25: recovery is attempted when the source is available, but source failure/offline status cannot block an explicit manual outcome. Manual origin and underlying uncertainty persist. Planning approval only; this approved copy is canonical.

### Story 3.12: Record Interrupted or Skipped Trips and Continue with the Intended Activity

As the driver,
I want to explicitly record a trip as interrupted or skipped and select the intended next activity,
So that operational changes do not falsely count as completed work or erase what was actually observed.

**Acceptance Criteria:**

**Given** an owned, unexpired active own day with a confirmed plan,
**When** the driver opens operational changes through Menu,
**Then** distinguish interruption of the current trip, an explicitly skipped trip and selection/correction of tracking context,
**And** show the affected trip's route, direction, departure and service-date context before confirming an outcome,
**And** ordinary correction of an erroneous selection under 3.3 does not automatically assert interruption or skipping; it remains distinct from declaring work not performed.

**Given** the driver explicitly confirms interruption of the current nonterminal trip,
**When** the action commits,
**Then** record a manual interrupted/aborted trip outcome with actual action time and preserve observed portions, corrections and uncertainty,
**And** do not invent final-stop arrival, convert it to completed or erase earlier evidence,
**And** release that trip's active pin only as part of the committed explicit context exit, with no pin/progress inherited by another trip,
**And** cancellation leaves the active context/outcome intact and no medical details are required.

**Given** an eligible confirmed trip that was not performed,
**When** the driver explicitly confirms it as skipped,
**Then** record skipped as a distinct manual outcome rather than completed or interrupted-after-observed-work,
**And** do not silently relabel an already completed trip or one with conflicting actual-performance evidence; preserve that evidence and explain the conflict,
**And** choosing a later trip, passage of scheduled time or absence from an imported update alone cannot mark intervening work skipped.

**Given** the driver chooses the intended next confirmed activity after an operational change,
**When** the choice commits,
**Then** preserve the original plan order and identities while establishing the explicit actual context with manual provenance,
**And** retain every intervening activity with its existing outcome; no bulk completion, skipping or deletion is inferred,
**And** include non-passenger activities without claiming that a break, planned relocation, physical replacement or handover occurred,
**And** trip interruption/skip never ends the combined workday, starts completed-day retention or resumes a terminal day.

**Given** a trip has usable stops, missing stops, or the app is offline,
**When** an authorized manual operational change is requested,
**Then** reuse the same outcome/state engine and 3.11 fallback conventions; no successful source call is required for an explicit manual action,
**And** preserve source/missing-data uncertainty and manual provenance after the action; stop-list availability does not change its origin,
**And** future source recovery cannot silently reclassify the outcome or manufacture observed completion.

**Given** interruption, skipped-trip recording or next-activity selection,
**When** the action opens and commits,
**Then** enforce 3.2's shared permission at both points, with visible reasons and labelled unknown-speed exceptions,
**And** reliable motion blocks these actions; direct GPS-loss arrow availability grants no permission to interrupt, skip or choose an arbitrary activity,
**And** loss of permission before commit cancels the uncommitted action without losing prior state or demanding a response while moving.

**Given** pending confirmation races with final arrival, another manual choice, plan revision or repeated callbacks,
**When** the action reaches the commit boundary,
**Then** revalidate owner/day/activity/context, applicable revision and current outcome,
**And** reject a stale incompatible proposal for renewed review rather than recording contradictory completed/interrupted/skipped outcomes,
**And** apply one intentional action once with stable event/batch identities; deliberate later correction preserves history instead of mutating an old submitted event.

**Given** local changes, synchronization and reopening,
**When** storage or transport fails,
**Then** atomically persist outcome/context and necessary events before showing success, using inherited authenticated FastAPI/PostgreSQL ownership/writer/revision checks and matching receipts,
**And** failed local writes leave prior state intact; lost responses retry immutable batches and do not duplicate outcomes,
**And** restore outcome provenance, observation gaps, actual selection and movement history, without refreshing stale position or resetting outage timers,
**And** enforce access/logout/storage locks and AD-12 expiry on all private copies; no permanent GPS trace or new retention clock is introduced.

**Given** the operational-change surface,
**When** operated by touch, keyboard or enlarged text,
**Then** clearly distinguish trip interruption, skipped work, tracking correction and whole-day ending with accessible labels, focus and cancel paths,
**And** retain the clock, context and movement reason; whole-day ending and physical bus replacement remain their own later actions, not disguised as interruption.

**Traceability:** FR-11 interruption/next selection and correction evidence, FR-6 explicit selection, FR-16, outcome evidence for FR-22 and foundational FR-20; NFR-2/3; UX-DR13/14/16/17/38; AD-2/5 atomic persistence, AD-9 context/provenance, AD-10/12 authority/retention. E7 consumes these facts without needing to exist for this story to work.

**Dependencies:** Implemented 3.11 outcome/fallback foundation and 3.3 selection with their inherited movement, progression and persistence prerequisites. No future bus-replacement, summary UI or final-day workflow is needed to demonstrate these operational changes.

**Implementation evidence:** Interruption with observed portion, explicitly skipped unperformed trip, wrong-selection correction without false outcome, jump to later activity preserving intervening entries, source/offline failures, permission loss, final-arrival/plan-change race, duplicate actions, failed write/lost receipt and reopen/expiry. Verify manual provenance and no contradictory outcomes with PostgreSQL integration. Tests are planned, not run.

**Size boundary:** Explicit trip interruption/skip and selected next context via existing engine. No general historical outcome editor, medical-reason collection, physical bus replacement, plan-file reconciliation, mentor handover, summary rendering or final day-end transaction.

**Pilot qualification:** Repeatable operational-change scenarios contribute to E8-D. E8-P requires mounted-device interaction and integration with full offline recovery, summary and end flows; E8-E remains separate actual-shift evaluation.

**Approval:** Approved by the owner on 2026-09-25 with the described scope, retaining the distinction between erroneous selection, interrupted trip and explicitly skipped trip, and preserving previous observations. Planning approval only; this approved copy is canonical.

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

**Approval:** Approved by the owner on 2026-09-25 with reported replacement time distinct from registration time for late entry. Unknown actual change time remains unknown; earlier observations are never reassigned by guessing. Planning approval only; this approved copy is canonical.

### Story 3.14: Control Day/Night Appearance with a Persistent Manual Choice

As the driver,
I want an always-available Day/Night toggle and an explicit Auto choice,
So that the display stays readable and my manual preference survives shifts and restarts until I choose otherwise.

**Acceptance Criteria:**

**Given** the tablet interface with Menu,
**When** the theme control renders,
**Then** place the adopted outlined control immediately left of Menu, showing the current appearance as sun for day or crescent for night and a separate Auto hit area,
**And** keep both hit areas operable at every speed and during GPS loss/Menu restrictions, without a menu visit or confirmation dialog,
**And** preserve clear keyboard focus, large forgiving targets and accessible current/selected labels; do not rely on color alone.

**Given** either current appearance, including while Auto is active,
**When** the driver presses the sun/moon area once,
**Then** select the opposite current appearance manually and disable Auto,
**And** apply the adopted DESIGN day/night surface, text, secondary and semantic tokens consistently without changing stop hierarchy,
**And** persist the manual preference independently of the current day; new shifts, ambient changes and restart cannot silently reset it.

**Given** a qualified automatic-theme trigger is available,
**When** the driver explicitly selects Auto,
**Then** enable automatic appearance based on that validated trigger and persist Auto preference,
**And** display green Auto text plus its small underline and an accessible selected state, while retaining the current sun/moon icon,
**And** repeated Auto activation is idempotent, not a toggle to manual mode; manual mode shows gray Auto text without the underline,
**And** do not activate Auto merely because a new shift starts or a previously unavailable capability returns after the user retained a manual preference.

**Given** Auto capability/trigger is unresolved, unsupported, denied or temporarily unavailable,
**When** Auto is requested or its input becomes unavailable,
**Then** preserve the current readable appearance and any persistent manual preference, and show an explicit unavailable status instead of claiming automatic adaptation works,
**And** leave manual toggling immediately usable and distinguish requested Auto preference from whether adaptation is currently functioning,
**And** do not presume an ambient-light sensor, reinterpret an unrelated GPS outage as darkness or silently substitute an unqualified trigger.

**Given** the actual target tablet/browser and candidate automatic trigger,
**When** implementation qualifies the trigger before claiming Auto support,
**Then** document the actual mechanism, permissions, observed capabilities, stability and behavior in bright/dark conditions and tunnels where safely testable,
**And** state what the mechanism can and cannot respond to; synthetic or desktop tests do not establish mounted-device adaptation,
**And** test unstable/alternating inputs without distracting flicker, using documented evidence-based stability rules rather than assumed sensor guarantees,
**And** unsupported adaptation remains a documented solution decision and E8-P gap, not an automatic V1 reduction or a completed Auto claim merely because the manual fallback works.

**Given** a theme change while a trip, outage countdown, manual pin, correction or notice state exists,
**When** appearance changes manually or automatically,
**Then** change appearance only: preserve trip/context/progress, planned/observed/manual distinctions, uncertainty, Menu permission and timer history,
**And** do not produce trip/outcome events, reset notice states or steal focus with a modal,
**And** test toggling while moving, before/after the five-minute outage boundary and during a pending permitted action without broadening that action's permission.

**Given** preference persistence succeeds, fails or cannot be read on restart,
**When** the setting is changed or restored,
**Then** restore the last reliably stored preference, with manual Day/Night surviving until explicit Auto,
**And** if persistence fails, keep current-session manual control usable but clearly report that the preference could not be saved; do not falsely promise restart persistence,
**And** missing/unreadable settings use a documented readable default with visible failure where applicable, without clearing operational data or presenting Auto as available by assumption.

**Given** the preference and rendered private screens,
**When** retention, logout or offline reopening occurs,
**Then** keep the nonpersonal appearance preference separate from private workday data and its AD-12 lifecycle, without hidden day associations or private copies in application-asset caches,
**And** changing theme never unlocks private content, renews authority or extends data expiry,
**And** no new backend table or per-toggle operational outbox event is required solely for this local preference; existing fullstack operational data and receipt contracts remain unchanged.

**Given** both adopted palettes and long/uncertain/missing-data content,
**When** the integrated tablet surfaces are inspected,
**Then** preserve readable contrast, stop-role emphasis, selected/disabled states and warnings across trip, preparation and non-passenger views,
**And** record actual mounted readability in sunlight/darkness separately from deterministic visual tests; no claim that changing CSS proves glance readability.

**Traceability:** NFR-1/2/4 and FR-16 appearance-control exception; UX-DR24/25/38, DESIGN tokens and EXPERIENCE Theme control/Responsive & Platform; AD-2 local persistence boundary, AD-9 no context/permission change, AD-10/12 access and separate settings lifecycle, AD-14 compatible preference recovery. No adopted automatic sensor/trigger is invented.

**Dependencies:** Implemented 3.5 display/palette foundation and 3.2 movement policy. Actual Lenovo/Brave evidence is required for Auto support; 3.1 position/speed qualification does not qualify an ambient sensor or theme trigger. No future wake-lock, notice engine or summary implementation is required for this control to work.

**Implementation evidence:** Manual toggle from each palette/Auto, persistent preference across shifts/restart, explicit/idempotent Auto, unsupported/denied/lost trigger, return of capability without overriding manual choice, unstable inputs, motion/outage independence, failed setting write/read, long names/contrast/focus. Device evidence qualifies actual Auto behavior; tests are planned, not run.

**Size boundary:** Adopted theme control, setting persistence and bounded trigger qualification/integration. No new UI framework, custom theme editor, brightness controller, extra sensor dependency, wake-lock feature or operational data migration unrelated to the setting.

**Pilot qualification:** Repeatable theme/state tests contribute to E8-D. E8-P requires actual trigger/stability/readability qualification; unresolved support is not passed by demonstrating fallback. E8-E remains later actual-shift evaluation.

**Approval:** Approved by the owner on 2026-09-25 with the described scope: manual preference lasts until explicit Auto, and working manual switching does not establish fulfillment of unsupported Auto. Planning approval only; this approved copy is canonical.

### Story 3.15: Keep the Active-Trip Screen Awake Where Supported

As the driver,
I want the active-trip screen to remain awake where the tablet/browser supports it,
So that I do not need to repeatedly wake the display to read the assistant.

**Acceptance Criteria:**

**Given** an authorized active trip displayed in the foreground,
**When** the view becomes eligible for browser screen-wake support,
**Then** request the available supported capability and report its actual result rather than claiming success from the request alone,
**And** distinguish acquisition pending, confirmed held, released and unavailable/failed states,
**And** selecting a prepared day without an active trip does not falsely claim an active-trip wake session.

**Given** wake support is absent, denied, fails or is released by the browser/device,
**When** the application learns that state,
**Then** show a concise understandable status that keeping the screen awake is unavailable/not active, retaining the readable trip view and operational data,
**And** do not repeatedly prompt, steal focus or demand driver action while moving,
**And** never substitute hidden media playback, artificial touches or a claimed native/background capability for the approved browser feature,
**And** retry only through supported lifecycle/action paths with bounded failure handling, not an endless tight request loop.

**Given** an active trip survives a tab switch, screen lock, app suspension or foreground return,
**When** the visible authorized view resumes,
**Then** re-evaluate actual wake support and reacquire where supported, without treating a previous held state as proof of a current lock,
**And** do not bypass an explicit device lock or private application lock,
**And** retain selected trip, manual pin, progress, uncertainty, theme and movement/outage history; return to foreground does not create fresh GPS evidence or a startup exception.

**Given** a trip ends, is interrupted, changes to another active trip, or the private view is locked,
**When** wake eligibility changes,
**Then** release obsolete wake resources and avoid duplicate holders/listeners; re-evaluate for a genuinely active successor trip,
**And** retain eligibility while the current passenger trip remains active despite delay or GPS loss, independently of Menu permission,
**And** test final-stop completion, same-route-return waiting and subsequent activation against actual trip state rather than a schedule-only timer,
**And** no wake lifecycle action can end the day, change trip outcomes or extend authority/retention.

**Given** a wake request resolves after logout, a hidden/closed view or a context change,
**When** the asynchronous result is processed,
**Then** verify current eligibility before retaining the resource and release stale acquisitions,
**And** a late success cannot unlock private content or leave the UI claiming the wrong context is protected,
**And** repeated callbacks/retries are idempotent and do not mutate operational events or synchronization batches.

**Given** network loss, sensor uncertainty or a theme change during an active visible trip,
**When** wake behavior is evaluated,
**Then** keep connectivity, position, theme and wake capability states distinct; none by itself proves that another is working,
**And** use available browser support without requiring a backend round trip,
**And** never present screen-awake success as evidence of continued sensor delivery or whole-day offline readiness.

**Given** the actual pilot Lenovo tablet and Brave browser,
**When** the implemented feature is qualified,
**Then** record actual device/OS/browser versions, relevant power/display settings, foreground duration and observed display-sleep behavior,
**And** test acquisition/release, foreground return, screen lock, trip changes, network loss, unavailable support and relevant power-saving conditions where feasible,
**And** distinguish browser-reported acquisition from observed screen behavior; report exact tested conditions and untested cases,
**And** base the capability/support status on actual observed Lenovo/Brave screen behavior under those conditions; a browser-reported held resource alone cannot establish qualified screen-awake operation or background support,
**And** document unsupported/unreliable operation as a qualification gap requiring a solution decision, not a pass because the UI exposes a fallback; no driver interaction is required during moving tests.

**Given** wake status is rendered or private data is reopened,
**When** persistence/privacy rules apply,
**Then** keep the browser-held resource state ephemeral and revalidate it after restart; never persist a boolean as proof that the resource remains held,
**And** reuse existing access/storage/expiry handling for the private view with no new private day copies, backend wake table or per-retry operational outbox events,
**And** sanitized qualification evidence excludes private trip identifiers and raw GPS traces.

**Given** status changes are shown to the driver,
**When** inspected by touch, keyboard or assistive technology,
**Then** use clear text and non-color status cues without obscuring current/next stop, route/destination, clock or Menu,
**And** avoid repeated announcements for repeated identical failures; any manual retry follows its own supported browser requirements without overriding operational movement controls.

**Traceability:** NFR-1/2/4; UX-DR25/38/44 and EXPERIENCE active-trip wake requirement; AD-2 local runtime distinction, AD-9 unchanged operational/movement state, AD-10/12 private access/lifecycle and AD-14 coherent recovery boundary. Source/notice audio qualification remains E4/E8, separate from wake support.

**Dependencies:** Implemented 3.5 active view and 3.9 trip lifecycle, with inherited access and state foundations. Actual target-device access is needed for qualification; neither desktop simulation nor 3.1 GPS qualification proves wake support. Verify browser API details during implementation without changing adopted architecture.

**Implementation evidence:** Lifecycle/failure fixtures for pending/held/released/unavailable and stale promise cleanup; active versus prepared/no-trip/locked view, context changes, foreground return and repeated events; independent network/GPS/theme states. Record actual tablet duration/power/display results separately. Tests are planned, not run.

**Size boundary:** Browser screen-wake lifecycle and target-device qualification only. No background tracking, native wrapper, display-brightness controller, operating-system policy changes, media workaround or new cloud service.

**Pilot qualification:** Repeatable lifecycle tests contribute to E8-D. E8-P requires actual device behavior and honest gap reporting; support remains conditional rather than assumed. E8-E remains subsequent real-shift evaluation.

**Approval:** Approved by the owner on 2026-09-25 with support status grounded in actual Lenovo/Brave screen behavior, without promises of background execution or other unqualified support. Planning approval only; this approved copy is canonical. E3's coverage/continuation checkpoint remains separate; no implementation or readiness workflow has started.
