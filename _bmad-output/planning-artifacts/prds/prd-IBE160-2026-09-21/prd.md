---
title: "Bus Driver Assistant — Product Requirements Document"
status: final
approval: approved
created: 2026-09-21
updated: 2026-09-21
---

# Bus Driver Assistant

## 1. Purpose and Decision Status

This PRD defines the course MVP for the pilot driver and instructor, and supplies requirements for subsequent UX, architecture and implementation. Product decisions and finalization checks are complete. The product owner explicitly approved this PRD on 2026-09-21; its status is `final`. No stack or detailed architecture is selected, and feasibility checks do not imply that the full scope has been proven achievable within the available time.

Authoritative inputs are the [approved Product Brief](../../briefs/brief-IBE160-2026-09-21/product-brief.md), its [supporting addendum](../../briefs/brief-IBE160-2026-09-21/addendum.md), and subsequent explicit decisions in the [decision reconciliation](reconcile-decisions.md). The [PRD addendum](addendum.md) preserves discovery depth and alternatives. Later decisions supersede earlier preferences: speed limits are now optional, deadhead route calculation is deferred, and summary export is required. Source feasibility findings are in the [research note](research-source-feasibility.md).

## 2. Vision, Audience and Delivery Constraints

The assistant gathers the driver's shift and relevant information in one convenient place, reducing repeated searches across existing tools. It supports preparation and brief-glance awareness throughout work. It does not replace official instructions, road signs, driver judgment, Tide workflows or NavCon. Drivers must be able to complete the shift without it.

The broader vision includes scheduled services, tour buses and charter work: assignments, itineraries, road notices, weather, restrictions and necessary stops. Line numbers, fixed stops and Entur data are not universal prerequisites for future assignments. Tour/charter support is outside this MVP; no generalized assignment solution is required now.

The operational pilot has one user, represented here by the pseudonym Alex, and four Tromsø lines: **20, 24, 28 and 42**. Overlapping lines, especially 20 and 24, must remain distinguishable. The instructor is a separate assessment user with fictional data, not a second operational driver.

The course deliverable is a **tablet-adapted website with a backend and database**, explicitly required by Alex. His target is a Lenovo Idea Tab Plus WiFi 12/256 GB running Brave, connected through mobile-phone tethering. Exact device variant and browser/OS versions need confirmation. The included pen creates no pen-use requirement. Instructor assessment must work on an ordinary PC browser without physical GPS. A separately installed app is outside the course.

Available effort is approximately ten working weeks at 4–16 hours weekly: **40–160 hours in total; 160 hours must not be assumed available**. Actual capacity is expected somewhere within that range. Submission is provisionally mid-December 2026, with instructor assessment over Christmas. Exact dates remain open. This is a cautiously evaluated course prototype, not an operational dependency.

## 3. User Journeys

### UJ-1 — Alex Prepares, Drives and Finishes a Varied Shift

Alex confirmed the current workflow in the addendum. The assistant-supported sequence below assembles his requested behavior and remains subject to review as part of this draft.

The evening before, Alex uploads his shift PDF, checks its interpretation, corrects mistakes and confirms it. He sees reporting time, trips, breaks, changes and relevant disruptions. In the morning he checks new, changed and ended notices and enters the actual bus number. Arrival registration and inspection acknowledgment stay in the Tide app.

During a trip he sees route, destination and stop progression. Actual progress governs trip changes despite delays. Relevant disruption headings remain visible; opening content follows the movement restrictions. If GPS fails, uncertainty is explicit and the agreed direct stop controls appear. Internet loss preserves loaded content while identifying missing updates. Neither failure is represented as no disruptions or confirmed location.

At the last stop the overview moves to the appropriate next activity: turnaround, deadhead travel, break, bus change or pilot-car transfer. Physical bus and vehicle-duty changes remain distinct. Normally Alex finishes by parking at the depot, shutting down and locking the bus; alternatively he returns by pilot car and hands over its keys. He confirms completion in the assistant, views the summary, optionally exports PDF and returns to the main menu. The website does not certify physical shutdown or key handover.

### UJ-2 — The Instructor Assesses Repeatable Behavior

The instructor signs into a separate test account on a PC and runs a fictional shift with simulated progression. They can restart it and trigger new disruptions, internet loss and GPS loss. Demo status remains explicit throughout, including exported evidence. Actual automatic retrieval and GPS performance are evidenced separately by the operational pilot.

## 4. Terms and Information Types

| Term | Meaning |
|---|---|
| Shift | The driver's sequence of trips and other activities for a workday. |
| Trip | One passenger-service run, with route, direction, stop sequence and scheduled departure. |
| Vehicle duty / vognløp | The bus's work sequence; distinct from physical bus and driver shift. |
| Physical bus | Actual vehicle, identified by manually entered bus number. Fault replacement may preserve vehicle duty. |
| Activity | A trip, break, deadhead movement, bus change or pilot-car transfer. |
| Deadhead travel / tomkjøring | Non-passenger movement of the bus; not pilot-car transport. |
| Disruption notice | Source-provided operational change with its own applicability and provenance. |
| System-status message | Assistant/data-retrieval condition, distinguishable from a road event. |
| Seen notice | Content opened by the user, not proof of comprehension. An update makes that version unseen again. |
| Planned data | Shift/timetable information and planned notices; not observed vehicle progress. |
| Observed position | Device position with available accuracy/freshness evidence, not a scheduled-time inference. |
| Demo/test data | Fictional/simulated information, distinguishable from operational data. |

## 5. MVP Boundary and Later Extensions

The core is **shift overview, stop progression and relevant automatically retrieved disruptions**. The supporting requirements below also belong to the proposed MVP: import correction, database persistence, access protection, continuity, PDF summary and instructor demo. Their combined effort must be assessed; fitting everything into 40 hours has not been demonstrated.

Automatic disruption retrieval is essential. Manual entry removes too much of the product's value and cannot replace it in pilot acceptance. Svipper is sufficient for the first implementation. Initial coverage concerns planned changes such as works, closures, diversions and moved stops. This does not promise complete acute-event, congestion or cancellation coverage.

For deadhead travel, show the agreed activity and next starting stop. Relevant Svipper notices may be shown where relevance is established, with explicit limits: no other road-event coverage or precise road-by-road coverage is promised. No notice does not mean a clear road. **Do not calculate deadhead routes in the course MVP.**

Optional extensions follow a working core and available time:

1. Meeting-bus warnings.
2. Weather and speed limits; their relative order is unspecified. Either may precede meeting warnings if very simple to implement and verify.
3. Deadhead-route calculation, with fastest suitable travel within the reported operating guidance.

None is required for MVP acceptance. Reliability and interaction constraints still apply. Further extensions include wider Tromsø timetables, municipal excavation portals, county and Statens vegvesen sources (particularly valuable for deadhead travel), tour/charter support, demonstrated-need historical shifts, CSV export if time permits, and an installed app after the course. In-product AI is not required.

Non-goals include direct Selfservice integration, recreating Tide arrival/inspection workflows, duplicating NavCon's minute/second deviation display, public registration, general multi-driver operation, a driver performance profile and permanent automatic shift history.

## 6. Functional Requirements

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

## 7. Cross-Cutting Quality Requirements

**NFR-1 — Tablet usability.** Prioritize brief-glance route, destination, stops and relevant headings. Express important status with text/symbols as well as color. Verify legibility and control usability on the mounted tablet, without requiring the pen. Light/dark treatment and measurable visual checks are assigned to B-4 before pilot use. Continuing the shift must not depend on operating the website while driving.

**NFR-2 — Information integrity.** Distinguish planned, observed, manually corrected, stale, unavailable and simulated information across displays and reports. Never manufacture metadata, stop sequences, completion or coverage. Preserve useful correction/failure evidence without unnecessary movement tracking.

**NFR-3 — Privacy and access.** Protect all records and instructor separation, not merely menu visibility. Anonymize exact shift, bus, vehicle-duty and trip identifiers in project documentation and any pilot evidence prepared for publication or assessment. The private PDF exception does not authorize identifiable publication. Private exported PDFs and external notes support evaluation; a separate in-application pilot-quality archive is outside this MVP. Deletion and access outcomes must be verifiable without prescribing implementation.

**NFR-4 — Target-environment reliability.** Validate actual position/speed, foreground operation, tethering loss/recovery and sound on Lenovo/Brave. Simulations cannot substitute. Raise unavailable capabilities as blockers rather than silently substituting scheduled or simulated progress.

## 8. Sources and Feasibility Evidence

Documentation research identified a candidate, not a tested integration: Entur lists Troms SIRI-SX support and a SIRI Lite request limit compatible with the desired two-minute interval. Correspondence with Svipper's notices, completeness and update/end semantics remain untested. This does not select a transport or grant a two-minute event-delivery guarantee. [Entur real-time documentation](https://developer.entur.no/open-data/realtime).

Entur documents timetable datasets; exact pilot journeys, calendars and stop sequences remain uninspected. [Timetable documentation](https://developer.entur.org/stops-and-timetable-data/). Lenovo's platform specification lists satellite positioning for WLAN models, but the exact purchased variant and Brave behavior remain unverified. [Lenovo platform specification](https://psref.lenovo.com/syspool/Sys/PDF/Lenovo_Tablets/Idea_Tab_Plus/Idea_Tab_Plus_Spec.PDF).

The [research note](research-source-feasibility.md) preserves source conditions and required checks. No feed, device or integration was tested during this research. Source licensing, attribution and access limits must be respected in later implementation.

## 9. Success and Acceptance Evidence

Alex approved **three actual working days** using assigned shifts. Days need not be identical or cover all four lines. Private exported PDF summaries and the pilot user's external notes provide the evaluation evidence; no separate retained in-application quality dataset is required. Anonymize material prepared for publication or assessment. Record real observations separately from demo results.

| Measure | Target and evidence |
|---|---|
| SM-1 — Information effort | Approximately 10–15 minutes daily including assistant use and original-source verification, against recalled 20–30 minutes per eight-hour day. Record time and context; indicative comparison, not controlled proof. FR-5, FR-12–15. |
| SM-2 — Relevant planned notices | No missed relevant planned notices in evaluated cases, checked against source evidence. Record availability and relevance. A sample with no relevant notices provides no evidence of notice coverage. FR-12–14. |
| SM-3 — Stop progression | ≤100 metres after passage/departure with reliable positioning; include closely spaced stops (reported around 250 metres). Report uncertain periods and corrections separately rather than hiding them. FR-7–9. |
| SM-4 — Operational core | Demonstrate actual automatic retrieval, corrected import, recovery and PDF summary on the target environment. Manual/demo notices do not satisfy real retrieval. FR-2–5, FR-12, FR-17–24. |
| SM-5 — Assessability | Instructor repeats desktop demo and failures without actual shift data or GPS. FR-25. |
| SM-C1 — Distraction counter-metric | Do not achieve lower search time by encouraging driving interaction. Record unnecessary chimes, confusing transitions and manual interventions; report the explicit interaction exceptions. |
| SM-C2 — Trust counter-metric | Count irrelevant notices, false freshness, hidden outages, wrong progression and falsely completed activities alongside missed information. |

The detailed timing/observation procedure and remaining numerical quality thresholds must be agreed before actual-shift evaluation. The small sample and recalled baseline limit claims of general effectiveness.

## 10. Finalization Register: Product Decisions and Deferred Validation

Technical feasibility is not a prerequisite for finalizing product intent. B items are mandatory downstream checks, not permission to claim an untested capability works. If validation fails, return to the product owner for scope or behavior changes; do not silently substitute manual/demo data for required automatic retrieval. C items do not block PRD completion. A items below have explicit product decisions and require no further clarification before approval.

### A — Resolved Product Decisions

| ID | Decision | Related requirements / former open group |
|---|---|---|
| A-1 — Resolved | Ten seconds of `Siste stopp` precedes deadhead travel, meal breaks with/without relocation, bus changes, pilot-car transfers and depot return. Same-route return retains its GPS/manual exception. | Confirmed by product owner; FR-10/16 aligned. |
| A-2 — Resolved | Missing stop lists use timetable recovery then the agreed manual fallback. No automatic candidate permits direct confirmed-shift selection. Undetected depot arrival permits normal completion through `Avslutt skift` in the submenu with the same confirmation and interaction rules. | Confirmed by product owner; FR-3/6/21. |
| A-3 — Resolved | The entire fully loaded and confirmed shift remains usable offline, including available stop lists, usable GPS progression, trip/activity transitions, manual corrections, daily summary and restart recovery. New source information waits for connectivity. | Confirmed by product owner; FR-17/20. Mechanism is B-3. |
| A-4 — Resolved | Delete all associated data seven days after confirmed completion/abortion; for a never-ended shift, seven days after planned end, without inferring completion. User-held PDFs and external notes are sufficient pilot evidence and remain outside application cleanup. Separate anonymized quality-data retention is deferred. | Confirmed by product owner; FR-24 and NFR-3. |
| A-5 — Resolved | Cancel pending message collapse when reliable speed falls to at most 6 km/h; a new high-speed transition starts a fresh interval. Reliable GPS recovery resets outage waiting; subsequent loss starts a new five-minute interval where required. Obsolete timers cannot override current state. | Confirmed by product owner; FR-16. Sensor qualification remains B-2. |
| A-6 — Resolved | A disappeared notice without confirmed ending remains uncertain and can be manually removed after source check. Changed content reappears as updated without sound; unchanged content stays hidden for the shift. Missing source update time is explicitly labelled unknown alongside last successful retrieval time. | Confirmed by product owner; FR-13/14. Source semantics/qualification remain B-1. |
| A-7 — Resolved | Remember sign-in for 14 days. Expiry alone does not interrupt an active shift; renew sign-in between shifts before starting another when expired. Explicit logout/access revocation remain distinct. | Confirmed by product owner; FR-1/20. Mechanism is B-3. |

Already resolved: startup access without GPS is free until the first valid measurement; five-minute outage unlocking and manual stop buttons are approved exceptions; completion uses position/time with manual confirmation of uncertainty; ended notices remain ten minutes; seen state survives restart. These are not questions to repeat.

### B — Downstream UX, Architecture and Implementation Validation

| ID | Validation / choice | Owner, phase and required evidence |
|---|---|---|
| B-1 | Automatic Svipper-origin access, licensing/limits, two-minute retrieval target, notice identity/update/end evidence and relevance for four lines. | Implementation owner, source feasibility before pilot; compare actual retrieved notices with original-source evidence. Maps OQ-1/5. |
| B-2 | Timetable/calendar coverage, matching, shared stops/direction, device-specific position/speed quality and stop/arrival detection thresholds. | Architecture/implementation owner; verify on actual Lenovo/Brave and representative routes before pilot. User outcomes remain those in FR-6–9/22. Maps OQ-2/3/4. |
| B-3 | Offline persistence/recovery mechanism, database design, authentication implementation, secure deletion mechanism and technology stack. | Architecture/implementation owner after A decisions; demonstrate behavior without changing scope. No stack is selected by this PRD. |
| B-4 | Legibility, color, control dimensions, light/dark treatment, exact meal-break label and layout. | UX owner; validate brief-glance use and agreed interaction exceptions on target tablet. |
| B-5 | Effort decomposition against uncertain 40–160-hour capacity, test fixtures, observation methods, anonymization verification and regression checks. | Project/implementation owner before build/pilot; measure actual rather than simulated acceptance evidence. Maps OQ-8. |

Source assumptions, unique dated-trip matching and target-device positioning remain explicitly unverified. B work must preserve the distinction between unavailable, uncertain, planned, observed and simulated data. Recalled baseline and stop spacing remain user-reported context.

### C — External Course Information Not Yet Known

| ID | External fact | Owner and revisit condition |
|---|---|---|
| C-1 | Exact submission deadline; currently mid-December 2026. | Product owner confirms when course staff publish it; do not invent a date. |
| C-2 | End of instructor assessment-access period; assessment is expected over Christmas. | Product owner confirms with course staff before deployment/assessment scheduling. |
| C-3 | Instructor browser/environment; ordinary-PC browser use is already required. | Product owner obtains available details before assessment verification. |

Former OQ-1 through OQ-8 are mapped above, not discarded. Source/log reconciliation, findings disposition, consistency and language passes, and privacy treatment of this run's public support material are complete; see [finalization report](finalization-report.md). The product owner explicitly approved this PRD on 2026-09-21, completing the Create PRD workflow with `status: final`. B validation and C external facts remain assigned downstream work, not claims of verified implementation.


