# UX Source Extraction

Extracted 2026-09-22. This is a source aid, not a new product decision or a finalized UX contract.

## Sources and precedence

Read sequentially as requested:

1. `../../../prds/prd-IBE160-2026-09-21/prd.md`
2. `../../../prds/prd-IBE160-2026-09-21/addendum.md`
3. `../../../briefs/brief-IBE160-2026-09-21/product-brief.md`
4. `../../../briefs/brief-IBE160-2026-09-21/brief.md`
5. `../../../briefs/brief-IBE160-2026-09-21/addendum.md`

The PRD is the normative baseline. Its addendum expressly preserves historical discovery, including superseded questions, rather than overriding the consolidated PRD. PRD and current addendum decisions take precedence over the briefs. The two brief files have identical visible contents. All five remain referenced; brief duplication is not independent corroboration. Latest user UX statements are recorded separately below, including differences requiring scope reconciliation.

## Foundation and scope already resolved

- General bus-driver assistant; one operational pilot, documented as Alex, in Tromsø on lines 20, 24, 28 and 42. The design must distinguish overlapping lines and directions, especially 20/24. Wider routes/cities are a vision, not extra MVP data coverage.
- Tablet-adapted website with backend and database. Target: Lenovo Idea Tab Plus WiFi 12/256 GB, Brave, phone tethering; exact hardware/browser versions and capabilities remain unverified. Pen is not required. Separately installed app is outside the course.
- Separate instructor test account on an ordinary PC browser, fictional shift, simulated progression and speed, restart and deliberate disruption/internet-loss/GPS-loss scenarios, without physical GPS. Instructor account must not expose operational data.
- No UI framework or design system selected. Technology and architecture are downstream choices; do not silently select one while drafting UX.
- Core: shift overview, stop progression and automatically retrieved relevant planned disruptions. Svipper suffices initially. Manual or demo notices cannot substitute for operational retrieval.
- Optional after the core: meeting-bus warnings first; weather and speed limits follow with no order between them, except either may precede meeting warnings if very simple to implement and verify. Deadhead-route calculation is deferred after these.
- No direct Selfservice integration, Tide arrival/inspection duplication, NavCon schedule-deviation display, public registration, general multi-driver operation, driver performance profile or permanent shift history. No chatbot or in-product AI requirement.
- Actual use/evaluation over three working days; simulated results remain separate. Approximately 40–160 hours total capacity, not a guaranteed 160-hour budget.

## Exact journey names

Mirror PRD names verbatim in EXPERIENCE.md:

1. **UJ-1 — Alex Prepares, Drives and Finishes a Varied Shift**
2. **UJ-2 — The Instructor Assesses Repeatable Behavior**

The historical confirmed current-workflow name in the PRD addendum is **UJ-1: Alex Completes a Varied Scheduled-Service Shift — Confirmed Current Workflow**. It is context, not a replacement for the PRD assistant-supported journey title. Alex is the privacy-preserving pilot pseudonym; no fictional instructor personal name is provided by the source.

UJ-1 source sequence: evening upload/review/correction/confirmation; morning changes and actual bus-number entry; trip selection and actual progress; relevant notices and explicit failure states; last stop and next activity; depot or pilot-car return; manual completion; summary, optional use of PDF export, main menu. Physical Tide registration, inspection, shutdown and key handover remain external actions, not app certification.

UJ-2 sequence: separate test sign-in; fictional shift with explicit simulation; repeatable progress and failure scenarios; restart; clearly labelled exported evidence. The source does not prescribe a narrative climax sentence; derive it from already captured outcomes rather than inventing new requirements.

## Required surfaces and their source basis

These are required interaction destinations, not a prescribed navigation structure or page count.

| Surface or mode | Required content/actions | Basis |
|---|---|---|
| Private sign-in and main menu | Remember sign-in 14 days; logout; active recovery; start preparation; no public registration | FR-1/20/22 |
| Shift upload and interpretation review | PDF upload; explicit preview/confirmation; unknown/error state; direct correction and add omitted trip/activity | FR-2–4 |
| Trip matching and correction | Route, endpoints, departure and applicable service date; candidate choice for multiple matches; warning and retain known data if no match; source failure distinct | FR-3 |
| Shift overview/preparation | Reporting time, trips, breaks, known locations, changes/transfers, shift-relevant notices, actual bus number | FR-5/12 |
| Initial trip choice | Supported automatic match, ambiguity candidates, no-candidate direct confirmed-shift selection | FR-6 |
| Active driving | Actual route and destination, three-stop progression, relevant notice headings, explicit uncertainty/failures | FR-6–9/12–19 |
| Notice details and original source | Validity, source update and successful retrieval distinguished, source access, seen-version action; manual uncertain-notice removal after source check | FR-13–16 |
| Stop overview/correction | Arbitrary correct-stop selection under movement rules; GPS-loss direct previous/next controls | FR-9/16 |
| Operational-change submenu | Next trip, interrupt trip, physical bus replacement, early termination; normal completion fallback if depot undetected | FR-11/21 |
| Between-activity display | Last stop; same-route turnaround; deadhead; meal break; bus change; pilot car; depot return | FR-10 |
| End/abort confirmation | `Avslutt skift`, `Er du sikker?`, cancellation keeps active; aborted outcome distinct | FR-21 |
| Daily summary | Completed/skipped/aborted/uncertain activities, displayed notices, manual corrections/removals and source failures; uncertain activity manual confirmation; thank-you/affirmation; PDF; main menu | FR-22/23 |
| Instructor demo | Explicit fictional mode, simulated progression/speed, failure triggers and restart, isolated evidence | FR-25 |

A retained-summary reopening route is not prescribed. PRD allows reopening/exporting within retention without restarting the clock or resuming the shift; decide the minimal discoverable access if exposed, without creating permanent history.

## Preparation and domain distinctions

- Confirm interpreted shift before use. Direct field editing was explicitly chosen over AI/free-text correction. Permit entirely omitted trips/activities to be added.
- Non-passenger activity fields: type, start/end times, optional location. Preserve date/order; do not invent locations or meanings for unexplained source codes.
- `Travel to` means travel using the assigned bus in the supplied context, not pilot-car transport.
- Shift, passenger trip, vehicle duty (`vognløp`) and physical bus are separate identities. PDF `Vogn` is not automatically the physical bus number. Manual bus assignment and fault replacement must preserve this distinction. No pilot-car number required.
- A missing stop list triggers supported timetable recovery for the service date; if unavailable, retain known trip facts, show `Stoppinformasjon mangler`, disable automatic stop progression and permit manual completion/abortion/next activity subject to interaction rules. Never fabricate a stop sequence.

## Active progress and between-activity states

- Initial selection uses confirmed shift, time and position jointly. Ambiguity requires selection before driving view. No candidate permits direct shift-trip choice. Manual override remains available under the agreed movement policy.
- Delays do not advance to the next trip by scheduled time alone.
- At a stop: previous/current/next. Between stops: departed stop and next two upcoming stops. Upcoming is not confirmed current location. Route-boundary empty-slot treatment is an explicit UX choice.
- Advance on passing without stopping. Reliable-position target: no later than 100 metres travelled after passing/leaving, not a radius. This is separate from speed-limit warning distance.
- Unreliable position retains last confirmed progress labelled as such; it does not claim the bus is still there.
- Diversions use supported actual sequences only. Otherwise recover at a later recognized stop on the active trip, even several stops ahead. Do not invent replacements or change lines through proximity alone.
- GPS loss shows direct previous/next stop buttons; internet loss alone does not. Reliable GPS return hides them and realigns automatically within the active trip.
- Registered final-stop arrival marks a passenger trip complete unless manually aborted. Manual final-stop arrival is recorded as manual evidence.
- Show `Siste stopp` for 10 seconds before non-return activities. Same-route return is an exception: retain last-stop state until reliable GPS detects starting stop again; during GPS loss, an extra Next stop press from final stop starts return. Merely reaching final stop does not start it.
- Relocation: `Tomkjøring` with next starting stop below. Meal break without relocation: `Lunsj` or `Matpause`, not deadhead. Deadhead then meal: meal label / `Tomkjøring` / first stop after break. Bus change or transfer: centered `Bussbytte` or `Pilotbil`. Final depot return: `Returner` / `til` / `Depot` on three lines.
- Display transitions do not prove travel, actual break start or physical handover. Physical bus replacement is not vehicle-duty change.

## Interaction policy already approved: do not re-elicit

| Condition | Message/source opening | Arbitrary stop choice and operational submenu |
|---|---|---|
| Reliable speed zero | Allowed | Allowed |
| Reliable speed >0 and ≤6 km/h | Allowed | Require full standstill |
| Reliable speed >6 km/h | Immediately block new opening; existing content collapses after about 30 seconds | Locked |
| Startup before first valid speed | Allowed | Allowed, no five-minute wait |
| GPS lost after speed >6 | Locked five minutes then available if still absent | Available after five minutes despite unverified standstill |
| GPS lost after speed ≤6 | Message opening remains available | Normally standstill-only controls become available after five-minute outage exception |
| Reliable GPS returns | Reapply speed rule immediately | Restore normal restriction |

Direct previous/next-stop buttons during GPS loss are a separate explicit driving-speed exception. Unknown speed never means confirmed standstill. Source links do not bypass policy. Startup access does not bypass sign-in or confirmation.

Cancel pending message collapse on reliable speed ≤6; a later crossing starts a fresh interval. Reliable GPS recovery resets the outage timer; subsequent loss starts a new timer where required. Obsolete timers cannot change current state. Reliable measurement qualification is implementation validation, not a new UX choice.

## Disruption, freshness and failure behavior

- During preparation, filter to shift. During driving, filter to actual trip/activity. Next-trip notices may appear on final-stop arrival, separately from the 10-second activity transition.
- Planned Svipper notices include applicable works, closures, diversions and moved stops. Ambiguous applicability is not certain relevance; absence is not all-clear, especially for limited deadhead coverage.
- Target two-minute retrieval during active shifts, subject to source validation; not guaranteed two-minute event delivery or live completeness.
- Keep headings visible. New and updated versions are bold until opened. Updated versions also have color-coded text. Opening marks version seen, not understood. Preserve identity/seen state across retrieval, outages and restart.
- Ended notice: strikethrough for ten minutes after assistant registers confirmed ending, then remove from overview; preserve summary history.
- Disappeared without confirmed ending: retain `Status usikker – sjekk originalkilden`; allow manual overview removal after source check under interaction rules; record manual removal. Changed version returns with updated emphasis, no sound; unchanged version stays hidden for shift, including restart.
- Source update timestamp and retrieval timestamp are distinct. Missing source time: `Kildens oppdateringstid er ukjent` beside last successful retrieval. Missing metadata stays unknown. Successful retrieval does not certify content freshness.
- Discreet chime only for a newly received relevant notice during ongoing trip. Updates, unchanged polls and previously fetched notices becoming relevant are silent. Chime never opens details.
- No initial successful disruption fetch: `Avviksinformasjon utilgjengelig – sjekk originalkilden` plus source link, not an empty no-events implication.
- Internet loss: prominent top warning with yellow exclamation triangle and text. Whole loaded/confirmed shift remains usable offline, including available lists, usable GPS, transitions/corrections/summary and restart. No newly fetched updates are implied. Never-loaded data stays unavailable.
- Connection restored: change warning to synchronization pending; keep missing-update warning until success. Failed retrieval must not remain indefinitely described as pending. Partial/source failure belongs in affected area and is distinguishable from a road notice.
- Recovery retains trip/bus/corrections/seen states without upload/reentry, but retained positions and notices do not become fresh. Completed shifts cannot resume.

## Completion, summary, retention and demo

- Final depot arrival offers red `Avslutt skift`; submenu fallback permits normal completion if undetected. `Er du sikker?` confirmation; cancel leaves active. Intermediate depot visits do not finish shift.
- Early termination shares confirmation/summary flow, with aborted status; no medical-reason collection requirement. Skipped/interrupted work is never completed by default.
- Non-passenger completion uses position and timing together. If unestablished due to missing location/GPS, `Gjennomføring usikker` plus summary manual confirmation; preserve manual origin. Does not certify physical actions or resume ended shift.
- Summary bottom: `Takk for i dag` plus day-informed affirmation, without scoring or AI requirement; return to main menu ready for next shift.
- User-initiated PDF export is required; using it is optional. Private PDF may retain actual identifiers, but publication/assessment evidence must anonymize. Demo PDF unmistakably labelled. CSV optional.
- Delete all shift-associated app data seven days after confirmed end/abort, or seven days after planned end if never ended. Reopen/export does not restart retention. User-held PDF/external notes outside app cleanup. No permanent profile/history or pilot-archive exception.

## Prior prototype and background worth preserving

- User reports promising automatic trip switching and daily summaries, but incorrect diversion, missed roadworks and a missed moved stop. This supports trust/relevance emphasis, not reproduction of an uninspected prototype layout.
- No prototype image, design file, typography or color tokens are supplied in these five sources.
- Shift PDFs vary in columns, density, continuation pages and character extraction. Earlier review did not visually verify PDFs. Import needs review/correction, not blind confidence.
- Checking scattered sources reportedly costs 20–30 minutes/day including breaks. Goal is approximately 10–15 minutes including source verification, without encouraging more driving interaction.
- Meeting-bus scenario supports a deferred optional feature: approaching estimates are not confirmed position or clear-road assurance. Weather forecast is not an observed local road condition.

## Latest user vision captured separately

- Mounted tablet first, primarily landscape; one-to-two-second glance; calm, trustworthy, professional, predictable operational instrument.
- Large high-contrast type and touch targets; one dominant fact and few secondary elements. Exact dominant fact and spatial ordering are not explicitly chosen.
- Restrained transport-oriented appearance; red critical, yellow/orange attention, blue information, green confirmed/normal. Day/night modes. Exact tokens, typeface, sizes, spacing, surfaces and mode switching are unspecified.
- Clear separation of preparation, driving and summary. No chat-led UI, equal-weight competing cards, small/hidden controls, precision swipes, extensive active-view scrolling, irrelevant/repetitive alerts, driving text entry, map-dominated main view, needless animation/gamification/glassmorphism/showy AI treatment.
- Distinguishable fresh/old/uncertain/simulated data, source metadata and original-source access. Normal operation must not depend on active interaction while moving.
- User now says upload a picture of the shift; source MVP specifies PDF only. Photo/screenshot import was not established. This is a genuine import-scope difference to resolve, not grounds to silently omit PDF or promise OCR beyond source scope.
- User now wants speed-limit warning around 300 m; earlier brief says 100 m or less. Latest explicit distance can supersede older desired distance for the optional feature; it does not alter 100 m stop-progression criterion.
- User mentions speed, weather next hour and relevant meeting buses, but also explicitly gives PRD precedence. Preserve optional status unless the user explicitly changes MVP boundary. Do not silently promote optional features to acceptance requirements.
- User says automatically advance at endpoint; preserve precise PRD same-route-return and ten-second behavior, not clock-only switching.
- User says no designs assuming active driving operation. This is compatible with default automatic behavior; existing GPS-loss button and startup/outage exceptions remain explicit. Do not silently remove approved exceptions or describe interaction prevention as absolute.

## Genuine outstanding UX choices and validation

### Product clarification required if desired scope changes

1. Is image upload additional first-version scope, a replacement for PDF, or informal wording for existing PDF import? Sources do not establish photo import.
2. Treat speed/weather/meeting buses as optional per PRD unless user explicitly requests scope change; avoid re-asking broad priorities already settled.

### Visual/experience choices not settled by source or latest message

- Dominant driving datum and arrangement of route/destination/three stops/notices; allocation for optional data without competing equal cards.
- Exact visual tokens, typeface and concrete readable sizes, spacing/touch dimensions, day/night surfaces and switch behavior. No current UI system to inherit.
- Meal label: `Lunsj` versus `Matpause` (explicit PRD B-4 choice).
- Endpoint empty slots in three-stop view.
- Exact changed-notice color placement and readable non-color state cues; missing/stale/simulation presentation consistent with user's semantic colors.
- Responsive behavior outside primary landscape, including tablet portrait and desktop assessment; keyboard/focus/accessibility details.
- No supplied visual prototype to reproduce; any visual reference would need user input or a user-chosen direction.

### Downstream evidence, not questions to reopen

Source identity/update/end semantics and relevance; actual timetable coverage; position/speed/arrival qualification; offline/auth/data deletion mechanisms; target mounted-device readability and control tests; actual-device signal/connectivity/sound; capacity and evaluation method. UX must represent unresolved capabilities honestly, not claim validation. Exact course/assessment dates and instructor browser remain external facts.
