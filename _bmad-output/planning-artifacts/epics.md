---
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics]
currentStep: step-02-design-epics
nextStep: step-03-create-stories
status: paused-by-user-before-story-creation
created: 2026-09-23
updated: 2026-09-23
epicStructure: eight-formal-epics-approved
epicsApproved: true
requirementsApproved: true
capacity: unresolved-more-than-40-hours-no-fixed-total
deliveryDate: unresolved
storiesWritten: false
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

Steps 1 and 2 were explicitly approved with C on 2026-09-23: requirements, responsibility boundaries and all eight formal epic boundaries. Each epic must provide access, persistence, error handling and privacy for its own functions. Early source/OCR/device qualification and E8-D, E8-P and E8-E remain approved, without changing V1 scope. The user requested stopping after saving approval and resuming tomorrow. Step 3 has not been opened and detailed stories have not been written. No implementation, provisioning, deployment or BMAD Spec is authorized in this step.

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

These are provisional, testable slice boundaries requested by the user, without story IDs, estimates, acceptance-criteria sets or implementation authorization. Shared contracts, access, local commit, provenance, retention and relevant movement policy apply to every slice. Steps 1 and 2 are approved; story creation remains unstarted at the user's requested stopping point.

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

The user's latest C approved the formal epic checkpoint and explicitly requested saving status and stopping before detailed stories, with continuation planned for tomorrow. Do not open step 3 or write stories until the user resumes. On resumption, read `.agents/skills/bmad-create-epics-and-stories/steps/step-03-create-stories.md` and follow its interactive checkpoints using this approved inventory and epic list. No repeated approval of steps 1–2 is needed. `currentStep` records the last processed step; `nextStep` identifies the unstarted continuation.
