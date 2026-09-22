---
name: IBE160 Bus Driver Assistant
status: final
updated: 2026-09-22
sources:
  - ../../prds/prd-IBE160-2026-09-21/prd.md
  - ../../prds/prd-IBE160-2026-09-21/addendum.md
  - ../../briefs/brief-IBE160-2026-09-21/product-brief.md
  - ../../briefs/brief-IBE160-2026-09-21/brief.md
  - ../../briefs/brief-IBE160-2026-09-21/addendum.md
source_precedence: PRD and PRD addendum govern; briefs provide background.
---

# IBE160 — Experience Spine

## Foundation

**Accepted extended reference:** the [43-screen gallery](mockups/remaining-screens.html) establishes operative FADDER/INSTRUKTØR with separate own and linked plans, open guiding controls and explicit Jeg kjører. This is distinct from the public fictional PC demo. The gallery also covers persistent clock, stop-tap entry, two-line depot return and dedicated closing. Static acceptance is not implementation or mounted-device validation.

A general bus-driver assistant delivered as a tablet-adapted website. The primary surface is a mounted landscape tablet, initially Lenovo Idea Tab Plus WiFi 12/256 GB running Brave with phone tethering. The PC demo uses fictional shifts and explicit simulation, reached from a prominent login-page button without authentication. This latest user decision supersedes the former separate test-login requirement. No UI framework or design system is selected. [DESIGN.md](DESIGN.md) owns visual identity. Day A and Night C and the vertical driving composition are approved. DESIGN.md extracts driving typography and geometry from the accepted reference; actual-device validation and unillustrated failure/responsive variants remain open.

The five sources above are inherited rather than duplicated. PRD and current PRD-addendum decisions govern over brief background; historical superseded addendum questions do not overturn the consolidated PRD. The latest user decisions in `.memlog.md` explicitly extend first-pilot import to PDF **and** JPG/PNG, including photographs and screenshots, with one shared confirmation flow. Conversation is Norwegian; the spines are English and established Norwegian interface labels are preserved.

The first operational pilot is represented by the source pseudonym Alex in Tromsø. Lines 20, 24, 28 and 42 provide initial test coverage, not permanent product boundaries. Shift, passenger trip, vehicle duty and physical bus are distinct. The design does not require active operation while moving; the explicitly approved movement exceptions below remain part of the contract.

## Information Architecture

These are interaction destinations/modes, not a prescribed page count or navigation layout. Every destination is reached by the Key Flows below, including operational mentor journeys.

Preparation discovery reference: [shared import review and confirmed-shift overview](mockups/preparation.html). The ordinary-day source/review split and morning overview were accepted as a starting point; the shared PDF/JPG/PNG confirmation flow is already decided.

The user accepted the ordinary-day source/review layout. The [accepted shift-overview and revision reference](mockups/shift-updates.html) adds multiple notices, split parts with separate depots and both update-entry paths. One combined day/summary and whole-or-partial upload support are confirmed; the expanded composition, scope choice, change comparison and ambiguity controls are now accepted as visual/behavioral references; the static mock does not implement them.

| Surface | Entry and purpose | Exit or recovery | Flow |
|---|---|---|---|
| Operational mentor preparation | Forbered neste skift → role → own shift/assignment → separate person-plan links and accompaniment scope. | Confirm plans independently; unresolved links stay unresolved. | UJ-3, UJ-4 |
| Operational guiding | Permanent FADDER/INSTRUKTØR with linked current trip and open controls. | Explicit role/activity/person change; preserve record provenance. | UJ-3, UJ-4 |
| Mentor-to-driver handover | Jeg kjører immediately applies driver restrictions; distinguish own planned trip from acute FADDER takeover. | Explicit permitted return to guiding; no timer-based role change. | UJ-3, UJ-4 |
| Post-completion closing | Final combined day confirmed ended/aborted. | Retained summary/export or main menu; no resume. | UJ-1 step 10; UJ-3, UJ-4 |
| Private access and main menu | Private sign-in, active-shift recovery, preparation, logout; no public registration. | Prepare next shift, recover active shift; a separate login-page entry opens the fictional demo without authentication. | UJ-1 steps 1, 11; UJ-2 step 1 |
| Upload and shared review | PDF or JPG/PNG; inspect, directly correct and add omitted trips/activities. | Explicitly confirm corrected shift before activation. | UJ-1 steps 1–3 |
| Timetable match | Recover trip details using route, endpoints, departure and service date. | Select candidate; retain known details with warning if no match. | UJ-1 step 2 |
| Shift overview/preparation | Reporting time, ordered trips/activities, breaks, known locations, bus changes/transfers, actual bus number and shift-relevant notices. | Select initial trip or correct preparation. | UJ-1 steps 3–4 |
| Trip choice/correction | Ambiguous automatic candidates or direct confirmed-shift selection; correction/undo after wrong selection. | Return to actual trip under movement policy. | UJ-1 steps 4, 7 |
| Active driving | Current-stop focus at a stop and next-stop focus between stops, persistent route/destination, three-stop progress and relevant notice headings. | Automatic actual-progress transitions; permitted detail/correction; preserve state through outages. | UJ-1 steps 5–8 |
| Notice detail/source | Validity, update time, retrieval time, original link and seen-version state. | Return/collapse according to speed; uncertain removal after source check. | UJ-1 steps 5–6 |
| Stop overview/correction | Arbitrary stop selection when permitted; direct previous/next controls during GPS loss. | Resume progression within actual trip. | UJ-1 step 7 |
| Operational-change submenu | Next trip, interruption, physical bus replacement, early termination, normal end fallback at undetected depot. | Resume corrected activity or end confirmation. | UJ-1 steps 7–9 |
| Between activities | Deadhead, layover, break, bus change, pilot car, dispatch-directed changes and depot return. | Show the next actual activity without assuming passenger trips are adjacent. | UJ-1 step 8 |
| Theme controls | Automatic day/night with manual override, including changing light conditions. | Preserve operational context. Manual Day/Night persists across shifts and sessions until the user selects Auto. A direct toggle is always available immediately left of Menu, including during motion. | UJ-1 step 5 |
| End/abort confirmation | `Avslutt skift` and `Er du sikker?`; distinguish normal completion from early termination. | Cancel keeps active; confirm leads to summary and prevents resumption. | UJ-1 step 9 |
| Daily summary/export | Outcomes, displayed notices, corrections, failures, uncertain-completion confirmation and optional use of required PDF export. | Main menu; retention does not become permanent history. Retained summaries open read/export-only from the main menu, with date and expiry. | UJ-1 steps 10–11 |
| Instructor simulation | Fictional shift, simulated position/speed, failure triggers and restart. | Repeat a scenario or export explicitly simulated evidence. | UJ-2 steps 1–5 |
| Split-shift overview | Show each work part with its own reporting time, known start depot/location and ordered activities; distinguish the gap between parts from an ordinary activity. | Prepare or resume the relevant part; do not infer final shift completion from the gap or an intermediate depot return. | UJ-1 extension below |
| Active-shift update review | While stopped, upload an updated PDF/JPG/PNG or manually add extra/overtime trips. | Review changes and confirm before they affect the remaining plan; cancellation preserves the active plan. | UJ-1 extension below |

### Latest navigation and closing decisions

`Forbered neste skift` is the entry for operative driver, FADDER and INSTRUKTØR role selection. The no-login demo is a separate entry on the login page and never provides operational shift access. The closing screen selects one short, warm affirmation from a varied text bank, based on recorded facts from that day, such as split parts or confirmed plan changes. Select an eligible variant not shown on the preceding day; rotate among eligible alternatives rather than repeating one sentence for each type of day. Neutral alternatives remain available when a specific category has too few variants. Unknown outcomes do not qualify for completion praise. Demo selections must not affect operative rotation; do not create permanent shift history to support text variation. Do not invent success, assess driving performance, assume an emotional state or treat uncertain work as completed. The accepted gallery supplies ten sample texts as a starting bank; this does not require an AI service.

## Voice and Tone

Concise operational language. State what is known, what is missing and what the driver may do when permitted. Do not expose technical errors, exaggerate certainty or use chatbot conversation as navigation. No typing is required during driving.

| Situation | Established copy or rule |
|---|---|
| Stop list unavailable | `Stoppinformasjon mangler` |
| Notice disappeared without confirmed ending | `Status usikker – sjekk originalkilden` |
| Missing source update timestamp | `Kildens oppdateringstid er ukjent`, beside last successful retrieval |
| Initial notice retrieval failed | `Avviksinformasjon utilgjengelig – sjekk originalkilden` |
| Unproven activity completion | `Gjennomføring usikker` |
| Registered final stop | `Siste stopp` |
| Completion | `Avslutt skift` → `Er du sikker?` |
| Summary closing | `Takk for i dag` and day-informed affirmation without scoring or an AI requirement |

Freshness, certainty and simulation labels must be understandable without technical vocabulary. Use the accepted `Matpause` label while preserving known paid/unpaid source classification.

## Component Patterns

Visual constraints for every component below are in DESIGN.md.Components.

| Component | Behavioral rules |
|---|---|
| Persistent clock | Consistent time on tablet screens, including active driving; time is orientation, never evidence of activity completion. |
| Mentor assignment and role | Forbered neste skift offers Fører, Fadder and Instruktør. Review own shift/assignment first, then separately link each required accompanied person's reviewed shift. No-driving assignments are valid; an instructor-only teaching/office day needs no linked shift. |
| Mentor driving and role switch | Guiding keeps Menu, stop/trip choice, notice details and acknowledgement open despite vehicle motion/GPS loss. Permanent FADDER/INSTRUKTØR marks this exception. Jeg kjører restores driver restrictions immediately, before any further plan choice. |
| Closing message | Final end/abort shows Takk for i dag, one eligible varied affirmation and summary/main-menu actions. Never resume ended work or praise uncertain outcomes. |
| PDF document | Export dated combined-day outcomes, manual/uncertain provenance, notice/source evidence and page numbering. Fictional exports remain labelled. The two-page reference is an example, not a page limit. |
| Access and navigation controls | Remember sign-in 14 days. Expiry alone cannot interrupt an active shift; renewal occurs between shifts before another starts. Explicit logout/access revocation remain distinct. Public demo access never exposes operational records; operative FADDER/INSTRUKTØR access remains separate. |
| Driving menu | Always present in active driving, including notice, offline and GPS-loss states. Replaces standalone trip selection; Menu contains the confirmed-shift trip choices, operational actions and `Skiftdetaljer`. This opens the shift overview with all relevant shift notices. It replaces the direct `Oppdater skift` menu action; both file and manual update paths remain available from the shift overview. Reliable motion locks it visibly; reliable standstill enables it. Apply the established startup/GPS-outage exceptions rather than treating unknown speed as standstill. GPS-outage countdown stays next to Menu. Direct GPS-loss previous/next stop controls remain separate. |
| Import review editor | PDF and JPG/PNG converge on preview, direct field correction, omitted-activity addition and explicit confirmation. Unknown or failed extraction remains unknown; no free-text/AI correction requirement. Preserve confirmed service date/order and unexplained source codes. |
| Activity and trip selector | Use confirmed shift, time and position together. Require a choice for ambiguity before driving view; allow direct confirmed-shift selection for no candidate. Do not silently substitute a timetable trip. Non-passenger entries contain type, start/end and optional known location. |
| Shift overview | Show known sequence, reporting time and relevant notices. Enter actual physical bus manually; do not treat imported `Vogn` as bus number. `Travel to` retains its source meaning of travel with the assigned bus. |
| Driving focus | Current stop dominates at a stop; next stop dominates between stops; route/destination remains persistent. Important approaching disruption/action may temporarily dominate, then return focus to the appropriate current/next stop. No mandatory acknowledgement or automatic opening of detail. Planned stop-related message timing follows the staged rule below; the message remains through the affected stop and clears after onward departure/passage. For two important notices affecting the approaching stop, show both short headings together without automatic alternation. Other activity reminders keep their established context. Exclude personal import data. |
| Three-stop sequence | Vertical sequence, future at top. Three-stop baseline top-to-bottom at a stop: stop after next / next / CURRENT highlighted; between stops: stop after next / NEXT highlighted / departed. This latest user decision changes the source at-stop roles: omit previous and show two upcoming stops. A four-stop alternative with previous always at bottom is allowed for exploration, not adopted. Current stop dominates at a stop and next stop dominates between stops. Upcoming is not current location. Advance when passing without stopping too; reliable-position target is within 100 metres travelled after passing/leaving. Never invent route-boundary entries or unsupported diversion stops. |
| Trip transition and correction controls | Follow actual progress, not next scheduled time alone. Make automatic change evident and allow undo/correct trip when interaction rules permit. Preserve delay and direction at shared stops. A manual selection governs until that trip actually completes; normal stop progression continues within it, and time/proximity alone must not reselect another trip. At completion, resume automatic next-activity selection under the established transition/return rules. Deliberate further correction or interruption remains available under movement policy. Use the permitted previous-trip selector, preserving manual correction evidence. |
| Notice heading and detail | Opening marks only that version seen, not understood. Preserve identity/seen state across polls, outage and restart. Updated version restores unseen emphasis. Source links follow the same movement restrictions. Confirmed ended notices remain struck through for ten minutes after registered ending, then leave overview but remain in summary. |
| Data status | Distinguish planned/observed/manual/stale/unavailable/simulated data. Keep source timestamp distinct from retrieval; unknown metadata stays unknown. Offline and recovery do not refresh retained evidence. Source failures are not road notices. |
| Stop correction controls | Arbitrary stop choice normally requires standstill; approved exceptions below apply. GPS loss exposes direct previous/next even at driving speed. Internet loss alone does not. Reliable GPS return hides buttons and realigns within the active trip. |
| Operational-change controls | Standstill policy with explicit exceptions. Next trip, interrupted trip, fault-related physical replacement and early termination are distinct actions; record corrections and do not mark skipped work complete. No medical-reason collection is required. |
| Between-activity display | Honor the transition rules below. Known pilot-car transfer may show the requested reminder to finish the trip and switch to pilot car. A display transition does not prove actual travel, handover or break start. Use the accepted Reguleringstid presentation; unconfirmed dispatch changes remain unresolved. |
| Theme control | Active Auto additionally has a small underline, providing a non-color selected cue; manual Auto has no underline.  Automatic day/night and persistent manual override. The always-visible button immediately left of Menu shows the CURRENT mode (sun for day, crescent for night); one tap selects the other mode. It remains operable in motion and during GPS/menu restrictions, without a confirmation dialog. The same outlined control contains an Auto hit area: pressing Auto enables automatic mode and makes Auto text green; manual mode shows it gray. Pressing sun/moon selects the opposite current appearance manually and disables Auto. Keep the current sun/moon visible in Auto. No menu visit or confirmation is required. Repeated Auto activation is idempotent; pressing Auto again does not silently select a manual appearance. Day uses {colors.surface-base} with {colors.ink-primary}; night uses {colors.surface-base-dark} with {colors.ink-primary-dark}, plus the corresponding secondary and semantic tokens in DESIGN.md. Do not presume an available ambient sensor; automatic trigger and supported capabilities need resolution/validation. Manual Day/Night is a persistent preference until explicitly disabled by selecting Auto. New shifts, restart and ambient changes must not silently reset it. |
| End-shift confirmation | Offer normal end at final depot and submenu fallback if arrival cannot be detected. Intermediate depot visits do not complete the shift. Cancel preserves active state; early ending records aborted status. |
| Summary and export | Distinguish completed/skipped/aborted/uncertain work; preserve manual confirmations/corrections/removals and source failures. User initiates PDF; no automatic upload/publication. Return to main menu without resuming ended work. |
| Instructor simulation controls | No-login demo entry from the login page, fictional shift and simulated speed/progression without physical GPS. Deliberate notice/network/GPS-loss scenarios and restart; explicit simulation in screen and PDF. Restart is not real-shift recovery. |
| Optional support information | After core: meeting buses, then weather/speed with the source's simple-to-verify exception. Desired speed-limit warning is approximately 300 m before known change; road signs/conditions prevail. Next-hour weather is forecast, meeting estimates are not confirmed positions or clear-road assurance. No automatic promotion to MVP acceptance scope. |
| Shift disruption list | Show all distinct applicable notices for the shift, including several on the same line. A shared notice appears once with all affected shift lines and trip/time associations. Do not merge separate events solely because headings or line numbers match. Source, validity and update/retrieval metadata belong to each notice. During driving, actual-trip relevance governs; planned stop notices follow staged display, while newly received applicable acute notices follow the immediate-display rule below. |
| Shift part header | Each part has its own known reporting time and starting depot/location. Do not copy the first depot or bus assignment to later parts as fact. Missing values remain unknown. A split gap does not certify rest, physical transfer or completion. Parts belong to one working day with an inter-part gap and one final daily summary; an intermediate part ending does not finalize the day. |
| Shift revision review | Both updated-file import and manual extra-trip entry are available during the day while stopped. Existing shared interpretation review applies. Show changes before confirmation; preserve performed work and the current trip context. Use the accepted scope and change-review flow below. |

### Initial and retained summary permissions

Immediately after confirming final end/abort, the initial summary review permits the existing manual confirmation of uncertain activities, preserving manual origin and actual timestamp. This does not resume operations or change the final end/expiry. Leaving that initial review for the closing/main-menu flow makes subsequent retained-summary access read/export-only. Unconfirmed outcomes stay uncertain rather than becoming complete by omission.

## State Patterns

Accepted visual reference: [daily summary and degraded-data compositions](mockups/summary-recovery.html) illustrate one combined-day summary, network loss with reliable GPS, and first-minute GPS loss after movement above 6 km/h. The summary and error-state compositions are accepted. GPS-loss controls additionally show the requested visible countdown; its example value is a static illustration of the existing five-minute rule.

Accepted visual reference: [vertical driving composition](mockups/driving.html) compares between-stop, at-stop and important-notice states with explicitly fictional data. It illustrates the confirmed current/next focus and staged stop-notice rule. The depicted always-visible Menu placement is accepted as a visual reference; its accepted menu, stop-choice and role variants are shown in the consolidated gallery. Stop-related messages persist through the affected stop and clear after onward departure/passage.

| Surface(s) | State | Required treatment / unresolved detail |
|---|---|---|
| Private access/main menu | First visit; expired between shifts; recovered active shift; logout/revocation | Operational records require private access; the fictional demo requires no login. Preserve active shift on remembered-sign-in expiry alone. Invalid-credential and revoked-access copy/recovery are not yet specified. |
| Upload/shared review | Empty; interpreting; failed extraction; unknown fields; corrected; confirmed | Never activate unconfirmed interpretation. Keep PDF/image paths equivalent. Apply Recoverable interaction defaults below for file/extraction failure and cancellation; never fabricate content. Exact processing layout remains open. |
| Timetable match/trip choice | Loading; single match; multiple; none; source failure | Ambiguity choice; no-match warning with retained facts; source failure distinct. Recover stop list for service date where supported. |
| Shift overview | Confirmed; actual bus unassigned/corrected; offline | Keep known activity order, show missing facts honestly; whole loaded confirmed shift remains available offline. No invented location or vehicle identity. |
| Active driving/three-stop sequence | At stop; between; delayed; uncertain position; missing list; diversion | Retain labelled last-confirmed progress on uncertainty. Missing list disables automatic stop progression but permits manual completion/abort/next activity under policy. Supported diversion sequence only; otherwise recover at later recognized stop within same trip. |
| Trip choice/stop correction/operational submenu | Permitted; speed-restricted; startup; GPS outage; recovery | Apply exact movement table below. Unknown speed is never evidence of standstill. Corrections remain recorded and active trip stays explicit. |
| Notice headings/detail | Unseen; seen; changed; ended; disappeared; manually hidden | Lifecycle in Component Patterns and Information trust. Unacknowledged headings remain visible; opening and dismissal are version-specific. Disappearance never establishes resolution. |
| Notice and optional-data areas | Never loaded; stale; unavailable metadata; source-specific failure | Show explicit unknown/unavailable/old state, last successful retrieval where known and original source where supplied. Optional support cannot look current when unavailable. |
| Whole active shift | Internet lost; restart offline; internet returned; refresh failed | Top warning; cached whole-shift operation and usable GPS continue. Returned connection means synchronization pending until retrieval succeeds; failures cannot remain indefinitely pending. Restore bus/trip/corrections/seen state without reimport. |
| Between activities | Final stop; same-route return; relocation; break; bus change; pilot car; depot | Apply table below; no assertion of unobserved physical actions. Use the accepted Reguleringstid presentation and show dispatch changes as confirmed or unresolved. |
| Theme control | Active Auto additionally has a small underline, providing a non-color selected cue; manual Auto has no underline.  Automatic day/night; manual override | Preserve chosen trip/data during theme changes. Manual Day/Night survives new shifts and restarts until explicitly disabled. Direct toggling remains enabled while moving; Menu locking does not affect it. Automatic trigger needs device validation; unavailable Auto preserves the current appearance and persistent manual preference, with an explicit unavailable label. |
| End confirmation | Awaiting choice; cancel; confirmed normal end; confirmed abort | Cancel leaves active; confirmed ending opens summary and disallows resumption. No implicit completion at intermediate depot. |
| Summary/export | Completed; skipped; aborted; uncertain; manually confirmed; retained; deleted | Summary confirmation preserves manual origin. Seven-day deletion applies. Export failure preserves the summary and permits retry under Recoverable interaction defaults; retained summaries are reached from the main menu for reading/export; detailed loading feedback remains an implementation task. |
| Instructor simulation | Ready; running; fault scenario; restart; export | Fictional and isolated throughout; restart reproducible; no physical-GPS requirement. Load failure stays within test context and offers retry; access-error copy remains open. |
| All interactive surfaces | Keyboard focus; denied device permission; unavailable capability | Apply the Accessibility Floor and Recoverable interaction defaults below; exact capability-specific fallback still needs validation. If sensor permission is denied or a capability is unavailable, do not silently substitute scheduled or simulated progress for observed operational progress. |
| Split-shift overview | Upcoming part; gap between parts; changed or unknown depot | Keep each part's reporting time/location distinct. Missing location stays unknown. Use an inter-part gap state with the next reporting time/location. End the combined day only through the existing final end/abort flow; produce one daily summary. |
| Shift disruption list | Several incidents; one incident affecting several lines; partial source failure | One item per distinct notice with multiple applicability links as needed. A failed source cannot turn the rest of the list into an all-clear or erase cached notices. |
| Active-shift update review | Parsing; manual add; proposed change; ambiguous match; cancel; confirmed; failed | Preserve confirmed plan and performed work until accepted changes are applied. Expose unresolved matching explicitly; do not silently reset active selection or duplicate imported trips. Apply accepted scope selection, comparison and explicit confirmation; cancellation keeps the prior plan. |

### Newly received acute disruptions

Display a newly received acute disruption affecting the active trip immediately in the right-hand information area, keeping stop context to the left and route/destination visible. This is an inline update without a covering modal, animation, focus theft, required acknowledgement or automatic source opening. Check the available line, direction, location and validity evidence; a matching line number alone does not prove applicability to the current trip. Label uncertain relevance explicitly rather than asserting certainty.

Do not delay an applicable acute warning until its affected stop becomes next. The staged rule below remains for planned stop-specific warnings. Keep two important simultaneous notices as short headings together, without rotation. Apply the existing notification/deduplication policy; repeated retrieval is not a new alert. Preserve source, validity, update and retrieval metadata, with original-source access under movement policy. This UX rule does not establish that an acute live-data source is available.

A route-wide acute warning follows its actual relevance and source lifecycle; passing one stop does not clear a still-applicable closure. A stop-specific approach message remains through the affected stop and clears after onward departure/passage. Clearing a driving message never asserts that the source incident has ended; relevant records remain in the shift overview.
### Staged stop-related disruption display

| Actual progress | Presentation |
|---|---|
| Affected stop is two stops ahead | Yellow warning triangle immediately after its name; do not automatically display its disruption message yet. |
| Bus is at the preceding stop; affected stop is next | Current stop remains dominant. Keep the upcoming warning triangle; being next alone does not trigger the message. |
| Bus has left the preceding stop and is between it and the affected next stop | Automatically show the relevant concise disruption message. Preserve route/destination and stop context. This is not automatic opening of source/detail content. |
| Bus arrives at or dwells at the affected stop | Keep the disruption message visible; current stop is highlighted in the secondary stop sequence. |
| Bus drives onward from or passes the affected stop | Clear its prominent message and restore ordinary stop focus; preserve notice history and independent source status. |

Use supported actual progress, not scheduled time alone, to establish the approach and onward departure/passage. Unknown position cannot establish either trigger; uncertainty and manual-progress rules still apply. Manual detail access, preparation notices and the source-defined chime policy remain separate. Later display of an already fetched notice does not create a new-notice chime. This table governs planned stop warnings; newly received acute warnings follow their separate relevance rule.

### Split shifts and revisions during the day

These requirements extend the initial-import scope in the source PRD. The user's latest decisions govern; do not treat a midday upload as a new empty shift or a destructive replacement.

Preparation shows multiple work parts and all distinct applicable notices across their lines. A shared roadwork notice may list lines 20 and 24 together; a separate moved-stop notice on line 20 remains another item. Display trip/time associations so an all-day line tag does not imply every trip is affected. Reassess relevance when the confirmed remaining plan changes, without manufacturing a new source version or resetting seen-state for unchanged notices.

The active-shift update accepts a revised PDF/JPG/PNG through the same interpretation review, or direct manual entry of extra/overtime trips using the existing trip fields. Both need an explicit review/confirmation step and must preserve current/finished activity evidence. The current confirmed plan remains in force if parsing, matching or confirmation fails.

Updated uploads may contain the whole day, a single part or additions only. Never infer deletion from absence in a partial file. Accepted reconciliation flow: explicitly establish import scope before applying changes; preserve all activities outside that scope. Separate added, changed, proposed-removed and unchanged future activities; match against service date, route, direction and departure rather than line number alone. Ambiguous matches require a choice and a re-upload must not silently duplicate the day. Only an explicitly scoped replacement can propose removal of a missing future activity, and that removal still requires confirmation. A partial/additions file does not propose removals. No upload is evidence that performed work never happened. Do not replace a manual active-trip selection through file matching alone. Record confirmed revisions for the daily summary and apply the existing privacy/retention rules; use one final end/abort and one daily summary for all parts. Intermediate gaps do not start completed-day retention. Only a confirmed revision changing the final activity changes the planned end used for never-ended-day cleanup; it never resets completed-day retention.

### Between-activity transitions

A non-aborted passenger trip completes at registered final-stop arrival; manual arrival keeps its manual evidence. Non-passenger completion requires position and timing together. Scheduled end alone cannot certify completion: when the required evidence is missing, retain `Gjennomføring usikker` for explicit manual confirmation in the summary. A display transition does not certify a physical handover, inspection or break start.

Preserve known paid/unpaid meal classification from the shift independently of the friendly `Matpause` label. Unknown classification stays unknown. A combined deadhead/meal display does not count travel time as break time or infer employment/payment rules.

| Situation | Display and progression |
|---|---|
| Final stop before non-return activity | `Siste stopp` for 10 seconds after registered arrival, whether GPS-confirmed or manually indicated. Next-trip notices may appear immediately and independently. |
| Same-route return | Keep last-stop state until reliable GPS detects starting stop again. With GPS loss, an additional Next stop press from final stop starts return. Arrival alone does not start return. |
| Relocation | `Tomkjøring`, with next starting stop below. |
| Meal without relocation | `Matpause` for a known meal activity. Do not call this deadhead. |
| Deadhead followed by meal | Meal label / `Tomkjøring` / first stop after break. |
| Bus change or pilot-car transfer | Centered `Bussbytte` or `Pilotbil`. Physical bus replacement remains distinct from vehicle-duty change. No pilot-car number required. |
| Final depot return | Centered `Returner til` / `Depot` on two lines, without a blue rail. End action offered on final depot arrival or manually through submenu. |
| Layover or dispatch-directed change | Show Reguleringstid with known timing and next activity. Preserve dispatch changes as confirmed or unresolved; time alone is not completion evidence. |

### Operational role and plan states

| State | Required treatment |
|---|---|
| Own assignment unconfirmed; missing linked plan | Review each plan separately; preserve known values without inventing accompanied trips or activating unresolved links. |
| Guiding FADDER / INSTRUKTØR | Persistent role text and open guiding controls. Linked person's plan drives stops, notices and trip progression; own plan governs work activities. |
| Instructor classroom/office | Current and next own activity; no passenger progression or fictitious accompanied person. |
| Instructor person/portion change | Confirm link/scope explicitly; never transfer another person's manual trip lock or completion evidence. |
| Planned own driving | Jeg kjører immediately activates driver restrictions; permitted selection contains only own confirmed trips. |
| Acute FADDER takeover | Retain linked current trip/stops/notices; record actual temporary driver change without copying planned ownership. Explicit return to guiding. |
| Ended combined day | Initial post-end review permits manual confirmation of uncertain activities; subsequently reopened summaries are read/export-only. Neither path resumes the ended day or resets expiry. Intermediate accompaniment endings do not end the day. |

Tapping the stop sequence opens arbitrary stop selection only when current role and movement rules permit it. Reliable-motion driver mode locks that entry; guiding permits it. GPS-loss direct previous/next controls remain a separate exception.

### FADDER and INSTRUKTØR assignment scope

Both roles have their own confirmed shift, including their own driving trips and the activities labelled FADDER or INSTRUKTØR. Planned own driving comes only from that own shift or an explicit manual correction/addition to it. Never copy or select planned own driving from the accompanied person's trip list. The acute FADDER takeover exception below changes who drives the current trip without changing planned ownership. This latest user correction supersedes the earlier gallery's mixed accompaniment/own-driving selector.

| Concern | FADDER | INSTRUKTØR |
|---|---|---|
| Accompaniment | During the fadder activity, accompany one same person for that person's whole shift. | Accompany a selected portion: one trip, part of a day, or a longer/shorter interval. |
| Person changes | No changes to another accompanied person within the fadder assignment. | One or several changes in a day; may return to a previously accompanied person. |
| Other role activities | No classroom or office activities as part of the fadder role. | Classroom teaching and office work may occur before, between or after accompaniment blocks. |
| Planned own driving | Separate trips on the fadder's own shift, never taken from the accompanied person's shift. | Separate trips on the instructor's own shift, never taken from the accompanied person's shift. |
| No accompaniment today | Not a fadder activity; do not create a fictitious accompanied person. | Valid instructor day with classroom/office and optional own driving; no other person's shift is required. |

The mentor’s own shift governs the sequence of work activities. Each accompaniment activity references the relevant person's separately confirmed shift; that linked shift governs route, stop progression, relevant notices and automatic trip changes only while accompanying that person. Several linked shifts remain distinct, even if routes or times overlap. Changing the linked person must visibly change the plan context and must not inherit the previous person's manual trip lock or completion evidence. A previously confirmed imported shift may be linked again when returning to the same person, without merging records.

Classroom and office states show the current activity and next known activity, without an active passenger trip or stop progression. The end of an accompaniment block is not the end of the own working day. Scheduled time alone must not assert that a physical handover, person change or own driving has occurred. Missing or overlapping assignments remain visibly unresolved rather than choosing a person automatically. Use the accepted explicit linking and confirmation controls to establish current person and accompanied portion; a scheduled boundary alone cannot confirm the change.

Guiding still retains the persistent role label and open controls. `Jeg kjører` restores ordinary driver restrictions immediately; planned own-trip confirmation selects only from the user's own confirmed shift. Ending guidance never automatically switches to unrestricted driving or silently imports another person's trip as an own trip. If a planned own trip is missing, use the existing stopped correction/update path. Classroom, office and own-driving completion remain distinct from the accompanied driver's outcomes in the eventual daily summary.

### Revision ownership and linked contexts

Before applying an updated file or manual revision, explicitly identify the target own shift or named imported linked copy. Keep that owner visible through file-scope selection, matching, comparison and confirmation. Match only within the target plan. Other plans, performed evidence and the active trip context are preserved. If a revision changes or removes a trip/portion referenced by accompaniment blocks, show those affected links and retain unresolved links for explicit repair; never silently move them to a similar trip or another person's plan.

### Role and context recovery

Recover current driver/guiding role, assignment role, own/linked plan identity, accompaniment block, active trip/manual pin and actual takeover/return events together with existing cached data. An acute takeover recovers as FØRER until an explicit permitted return, even if the imported assignment says FADDER. Restore established GPS-outage timing; restarting an active day does not create the genuine first-start exception. Incomplete recovery shows last-confirmed/uncertain context and must not infer unrestricted guiding from an assignment label.

## Interaction Primitives

Use clear taps, with large targets. Necessary stationary corrections aim for one or two taps. No precision swipe requirement, long driving scroll, required driving text input, unnecessary popup, animated attention capture or repeated alarm.

### Corrected trip selection

The always-visible `Meny` opens a menu that includes trip selection from the confirmed shift. There is no standalone driving-view `Velg riktig tur` button. Keep the trip choice discoverable under Menu; exact menu arrangement must preserve the one/two-tap correction goal where feasible. The correction identifies route, destination/direction and departure so overlapping routes do not become indistinguishable choices. Selecting the intended trip returns to its driving context under the movement policy. The one/two-tap goal is measured from the driving view, including opening Menu; long lists must not hide alternatives behind ambiguous route numbers.

The selected trip remains authoritative until actual completion. Continue GPS-supported stop progression within that trip, preserving uncertainty where necessary. Scheduled time or proximity to another line cannot undo the driver's correction. After completion, resume the established automatic next-activity flow, including non-passenger activities and the special same-route-return trigger. Further deliberate corrections and interruptions remain possible. Offer the prior trip through the same permitted correction selector; preserve manual origin for completion corrections.

The direct Day/Night toggle is explicitly exempt from Menu/movement restrictions: it stays enabled at all speeds and during GPS loss. It changes only appearance, not trip selection, data state or movement-lock timers. Both icon and Auto hit areas remain available. The current-mode icon, Auto selected state and accessible labels update together; do not announce the mode through color alone. The manual setting persists until explicit Auto.

### Notice acknowledgement while stationary

While moving, show only concise notice headings, retaining essential uncertainty/stale/simulation status without body text or source metadata. Details and original-source access require standstill under reliable speed, with the explicit startup and five-minute GPS-outage exceptions in the movement table. When motion resumes, collapse details immediately; do not preserve the old 30-second grace period. The same restriction applies to notice content reached through Skiftdetaljer.

At confirmed standstill, or under the explicit unknown-speed exceptions below, allow optional acknowledgement of an individual notice using a forgiving swipe-to-dismiss and an equally available large `Registrert` button; swiping must not be the only way. Acknowledgement removes that version's prominent driving message and restores stop focus. It does not resolve the incident, remove the stop-warning triangle, delete the notice from Skiftdetaljer or assert understanding. Preserve acknowledgement across polling, offline recovery and restart; unchanged data must not make the message reappear. A changed source version regains unseen emphasis and is assessed for display under the existing relevance rules. Opening detail marks a version seen but does not itself dismiss it. With two notices, dismiss only the selected one. Cancel an in-progress dismissal if motion starts before it commits.

This explicit stationary dismissal is an exception to keeping an unacknowledged planned stop message visible through dwell. Without dismissal, the previously agreed departure/passage clearing rule still applies. Acknowledgement is never mandatory to continue driving.
### Approved movement policy

| Condition | Notice details, source links and acknowledgement | Arbitrary stop/trip choice and operational submenu |
|---|---|---|
| Reliable speed zero | Available | Available |
| Reliable speed above zero and at most 6 km/h | Headlines only; details/source/acknowledgement locked | Require full standstill |
| Reliable speed above 6 km/h | Headlines only; immediately collapse open detail and lock detail/source/acknowledgement | Locked |
| Startup before first valid speed | Available under the existing startup exception before first valid speed; do not label speed as confirmed zero | Available without five-minute wait |
| GPS lost after speed above 6 km/h | Locked for five minutes after GPS loss, then available while speed remains unknown | Available after five-minute outage exception despite unverified standstill |
| GPS lost after speed at most 6 km/h | Locked for five minutes after GPS loss, then available while speed remains unknown | Standstill-only controls become available after five-minute outage exception |
| Reliable GPS returns | Immediately apply current speed rule | Restore normal restrictions |

During the five-minute GPS-outage restriction, show a visible remaining-time countdown adjacent to the always-visible restricted Menu control, for example `Tilgjengelig om 4:12 uten GPS`. Derive remaining time from the existing outage interval; reopening a view or restarting must not reset an established timer. At expiry with GPS still absent, enable the controls permitted by the outage exception without implying confirmed standstill. Do not announce each second to assistive technology; announce the transition to availability. Reliable GPS return cancels the countdown immediately and restores current speed rules; if controls stay locked due to motion, show the motion reason rather than an obsolete countdown. Startup with no first valid speed has no five-minute countdown. A subsequent qualifying outage starts a fresh interval.

GPS-loss direct previous/next buttons remain a separate driving-speed exception. These policies do not promise absolute interaction prevention. Startup does not bypass authentication or confirmed import. The stationary notice rule supersedes the former 6 km/h detail threshold and 30-second collapse grace period; obsolete timers cannot override the current state.

Keep the screen awake during an active trip. Actual browser/device wake support must be verified; no working capability is claimed by this document. New relevant notice during an ongoing trip may sound one discreet short chime. Updates, unchanged polls and previously fetched notices newly becoming relevant are silent. Sound never opens detail or bypasses restrictions.

### Acute FADDER takeover

The user explicitly permits an unplanned FADDER takeover of the accompanied person's current trip. This is separate from planned own trips. Offer a clear `Jeg kjører` action for this current-trip case; restore normal driver restrictions immediately while preserving the active linked trip, direction, stop position and notice context. Do not require creating a new planned own trip, selecting a different route or losing progress to apply the driver restrictions.

Record the temporary change of driver as an actual event, not a rewrite of either imported plan or evidence that the whole trip was completed by the fadder. Return to guiding is explicit through Jeg sitter på igjen in the permitted Menu path, never time-triggered; do not lift restrictions while the user is still driving. The current user clarification establishes this case for FADDER; it does not silently broaden the planned own-trip selector.

### Explicit tracking-context changes

A manual trip pin governs within its active tracking context. A confirmed block/person/activity change exits that context without declaring an unfinished passenger trip complete or aborted. Preserve the historical correction and observed portion; establish the actual trip afresh for each later block, including a return to the same person. Time/proximity alone still never releases a pin within an unchanged active block. Acute takeover retains the same tracking context and pin because the trip continues; changing who drives alone does not select a new trip.

## Accessibility Floor

Established requirements: essential information readable in a one-to-two-second side glance; large text, high contrast and large forgiving targets; text/symbols accompany status colors; no required precise gestures, pen or operation while driving. Day/night readability must cover direct sun, winter darkness and tunnels. Preserve clarity when attention is split across several instruments.

Draft implementation defaults derived from the confirmed accessibility and information-trust requirements:

- Keyboard traversal follows the visible reading order. Label controls by action and expose disabled/selected states. No essential action depends on hover, color or a swipe.
- Opening a permitted dialog moves focus into it; closing returns focus to its invoking control. Cancel must not commit a correction or end a shift. Movement-triggered closure must not leave focus in hidden content.
- A warning triangle has an accessible description associated with its stop name. Stop names expose their role (current, next, later or departed), so visual emphasis is not the only distinction.
- Data refresh does not steal focus or announce every poll. Announce meaningful state changes without repeating unchanged warnings. Existing chime rules remain controlling.
- Text enlargement preserves names and actions; do not silently truncate a critical instruction. Mounted-device checks must establish readable sizes and the amount that actually fits before implementation is accepted.

These defaults were included in document/reference validation. This specification does not claim accessibility conformance or mounted-device validation. Visual contrast and control dimensions belong in DESIGN.md. The always-visible driving Menu uses {components.driving-menu.minHeight} minimum height and {typography.control.fontSize} text, with {rounded.control} corners. These are reference values requiring mounted-device verification.

### Recoverable interaction defaults

These defaults apply the existing requirements to common failures; they do not add a new product capability.

| Failure | Preserve and recover |
|---|---|
| Import cannot be interpreted | Keep known extracted values marked as unconfirmed. Offer another PDF/JPG/PNG and the existing direct correction/add-activity path. Never activate invented trips or silently replace an active confirmed shift. |
| File selection is cancelled | Return to the previous preparation state without changing its data. Camera access is not a prerequisite for selecting an existing image. |
| Matching service fails | Preserve the entered service date and trip facts. Distinguish service failure from a successful search with no match; retry must not erase manual corrections. |
| PDF export fails | Keep the ended shift and its summary; allow export retry. Do not claim a file was saved, resume the shift or reset retention. |
| A capability or permission is unavailable | Explain the missing capability in ordinary language at the affected surface. Use only the already defined fallback; never substitute demo data into an operational shift. |
| Instructor scenario fails to load | Remain in the isolated, labelled test context and offer retry. Never fall back to operational records. |

## Information Trust, Privacy and Retention

Retrieve operational planned notices automatically, initially from Svipper, filtered to shift during preparation and actual trip/activity during driving. Target a normal two-minute retrieval interval during active shifts, subject to source validation; do not claim guaranteed event delivery or complete real-time coverage. Manual/demo notices cannot substitute for this operational retrieval.

Expose original source, validity and source update time where supplied alongside last successful retrieval. Never replace a missing source timestamp with retrieval time. Ambiguous relevance is uncertain, and absent notices or limited deadhead coverage do not certify clear conditions.

If a notice disappears without confirmed ending, retain `Status usikker – sjekk originalkilden`. Permit manual removal from overview after source check under movement policy and record the removal. Unchanged content stays hidden for the rest of the shift, including restart; a changed version returns as updated without sound.

The active driving view excludes personal information from imported shifts. Operational records and fictional PC demo data remain isolated beyond menu visibility; operational mentor imports are private copies within the mentor’s own working day, not cross-account links or authority to edit another person’s records. Private PDF may retain operational identifiers; documents/evidence prepared for publication or assessment must anonymize exact shift, bus, vehicle-duty and trip identifiers. No automatic publication occurs.

Delete all shift-associated application data seven days after confirmed completion or early termination. For a never-ended shift, delete seven days after planned end without declaring completion. For split work, completion/abort applies to the combined day; ending an intermediate part or entering its gap does not start a separate completed-shift deletion clock. This includes the own uploaded PDF/image, summary, retained movement data, corrections and notice history. Accompanied-person source files are an explicit exception: delete them immediately after successful import, as specified below. Reopening/export does not reset retention or resume a shift. User-held PDF and external notes are outside app cleanup. No permanent history, driver performance profile, extra raw tracking for retention, or pilot-archive exception.

### Accompanied-person imports and summary scope

Delete the accompanied person’s uploaded PDF/image immediately after successful import. Keep only the extracted information needed to support the mentor’s work inside the mentor’s own working day, retaining separate plan/person/block identities. File deletion must not erase the interpreted review, confirmed route context or evidence required for the approved accompaniment flow. These are private imported data, not a live link to another account; importing provides no access to or editing rights over that person’s account or original records.

The mentor’s daily summary and PDF include only portions actually accompanied, with observed or uncertain outcomes. Keep own activities, planned own driving and actual temporary takeovers separate. Do not include the other person’s unaccompanied remainder or infer its completion. At final own-day ending, retain the accompanied evidence needed for that summary and discard the remaining imported operational context. The retained summary/evidence follows the mentor’s combined-day seven-day deletion clock (or planned final end for never-ended work); the other person’s shift ending does not start a separate clock. Export and reopening do not extend retention.

Import review explains that the uploaded file is deleted after import while necessary interpreted information stays in this working day. Mentor summary/export identifies the included accompanied portions and their evidence status, and shows the own-day expiry. User-held exported PDFs remain outside app cleanup.

## Responsive & Platform

Primary: mounted landscape tablet with touch, vibration and possible gloves. Secondary: instructor PC browser with fictional data and simulation controls. Do not assume a native app, ambient sensor, working GPS/speed, reliable wake lock or sound support. Verify actual Lenovo/Brave behavior, tethering loss/recovery and foreground operation; simulated evidence cannot replace this.

Validate stop progression with the approximately 250 m spacing between stops reported in the source. Also verify that progression updates within 100 m of travel after passing or leaving a stop. This is a reported test scenario, not a verified network minimum or a replacement trigger distance.

Tablet portrait behavior, desktop layout adaptation and exact breakpoints remain open. No unsupported phone-specific surface or UI framework is implied.

## Inspiration & Anti-patterns

The desired reference is a restrained modern driver instrument or operational information system. The earlier prototype's automatic trip switching and daily summary are reported inspiration; no prototype visual artifact has been supplied or inspected. Its reported missed roadworks/moved stop and incorrect diversion reinforce source fidelity and uncertainty handling.

Reject chatbot-led navigation, equal-weight card grids, tiny controls, hidden functions, precise swipes, extensive driving scrolling, irrelevant/repeated alerts, technical errors, typing while moving, map-dominated layout, needless animation, gamification, glassmorphism and showy AI styling. Old, uncertain and simulated information must not resemble fresh operational data.

## Key Flows

### UJ-1 — Alex Prepares, Drives and Finishes a Varied Shift

1. Alex signs in privately and uploads the next shift as PDF or JPG/PNG, including a screenshot/photo. Both open the shared interpretation review. Remembered sign-in lasts 14 days; expired access is renewed between shifts, not forced mid-shift. (FR-1/2)
2. Alex corrects fields directly and adds omitted trips/activities. Timetable completion uses route, endpoints, departure and confirmed service date. Multiple candidates require a choice; no match retains known facts with missing-stop warning; source failure is separate. Non-passenger activities keep known type, time and optional location. (FR-2–4)
3. Alex explicitly confirms the corrected shift. Before duty, Alex checks changes, reporting time, activities and relevant notices, and enters the actual bus number without confusing it with vehicle duty. No physical Tide inspection/registration is certified by the app. (FR-5/12)
4. The assistant proposes the actual initial trip from confirmed shift/time/position. Alex resolves ambiguity or directly chooses a confirmed trip if no candidate exists. Driving view shows the selected direction explicitly. (FR-6)
5. Alex sees the dominant current stop while at a stop, or dominant next stop between stops, persistent route/destination and three-stop context with a brief side glance. Progress follows actual movement, including passed stops, not the timetable alone. In Auto, day/night adapts automatically; manual Day/Night persists until Alex explicitly restores Auto; active trip keeps the screen awake where supported. (FR-7/8; latest user decisions)
6. **Climax:** Alex first sees a yellow triangle immediately after the name of an affected stop two ahead. The stop-related message appears automatically only after leaving the preceding stop, when the affected stop is next and Alex is travelling toward it; no interaction is required. Alex can act on the actual road situation, with uncertainty honestly marked; the appropriate current/next stop regains focus afterward. When permitted, Alex opens source-backed detail; only genuinely new relevant notices during the trip chime. (FR-12–16; latest user hierarchy)
7. If data or automatics are wrong, Alex uses permitted stop/trip correction or transition undo. A manually chosen trip stays selected until actual completion; stop progression continues and the assistant then resumes automatic next-activity selection. GPS loss exposes direct previous/next; arbitrary changes use the exact policy above. Fault-related physical bus change and interrupted/skipped work remain distinct and recorded. Offline operation/restart retains the whole confirmed loaded shift, bus, corrections and seen state; restored connectivity refreshes without pretending retained data is fresh. (FR-9/11/16–20)
8. At registered final stop, Alex sees the specified final-stop transition and appropriate next activity, including deadhead, break, layover, bus change or pilot car. Same-route return waits for its separate trigger. The assistant does not assume adjacent passenger trips or claim that a physical handover happened. (FR-10)
9. After final depot return, Alex chooses `Avslutt skift` and answers `Er du sikker?`. If arrival is undetected, the submenu permits the same normal ending. Cancel keeps the shift active; early termination records an aborted shift. Ended work cannot resume. (FR-21)
10. Alex checks the daily summary: completed, skipped, aborted and uncertain activities, displayed notices, corrections and source problems. Unproven non-passenger completion can be manually confirmed with manual origin preserved. Alex may initiate private PDF export and sees `Takk for i dag` with a day-informed affirmation. (FR-22/23)
11. Alex returns to the main menu ready for another shift. Retained data follows the fixed seven-day deletion rule; reopening/export never resumes ended work or restarts retention. Retained summaries open read/export-only from the main menu, with date and expiry. (FR-24)

**Failure paths:** failed extraction remains reviewable uncertainty and cannot activate silently; missing stop sequence remains unavailable with manual completion/abort/next-activity fallback; initial disruption failure displays the source warning instead of no-events reassurance. Unreliable position retains last-confirmed progress; unsupported diversion recovers only at a later recognized stop on the same trip. An interruption/restart recovers only active work. Unavailable device capabilities require implementation resolution, not simulated operational substitutes. Import/export errors follow Recoverable interaction defaults; exact loading and feedback layout remains open.

### UJ-1 extension — Alex handles split work and added overtime

1. Alex reviews the confirmed work parts, each with its reporting time and known starting depot. One part may start at a different depot; the app does not infer travel between them.
2. Alex checks all applicable notices across the day's trips. A shared incident lists the affected lines in one message, while separate incidents on a line remain separate.
3. After the first work part, Alex enters the gap before the later part. The gap and intermediate depot return do not automatically establish that the whole day's work is complete; the day remains open until its final end/abort.
4. While stopped, Alex receives extra work and either imports an updated PDF/image or adds the overtime trips manually.
5. **Climax:** Alex sees the proposed changes alongside the already confirmed plan, resolves ambiguous matches and confirms the intended remaining work without losing completed activities or manual corrections.
6. The assistant follows the confirmed plan, recalculates notice relevance and preserves evidence for the eventual summary. All parts contribute to one final daily summary.

**Failure paths:** import/matching failure or cancellation leaves the confirmed plan active; missing depot remains unknown; a partial revision must not silently remove completed work, duplicate trips or redirect the active manual selection. Use the accepted scope-selection and change-review controls to resolve ambiguous matches before confirmation.

### UJ-2 — The Instructor Assesses Repeatable Behavior

1. The Instructor opens the clearly labelled fictional demo from the login page on a PC browser, without signing in. No operational records are exposed. (FR-1/25; latest user override)
2. The Instructor opens a fictional shift with unmistakable simulation labelling, then exercises simulated progression and speed without physical GPS. (FR-25)
3. **Climax:** The Instructor triggers a relevant new notice, internet loss and GPS loss and can observe the same explicit restrictions, retained-data states and recovery behavior repeatably. Simulation remains visible so the demonstration is never evidence of live sensor or notice coverage. (FR-25; NFR-2/4)
4. The Instructor restarts the fictional scenario and repeats it. This is demo restart, not resumption of a completed real shift. (FR-25)
5. The Instructor may export explicitly marked demo evidence. Test data stays separate and assessment evidence contains no real operational identifiers. The no-login demo remains isolated from private operational access. (FR-23/25; NFR-3)

**Failure paths:** deliberate source/network/GPS failures show the defined failure states, not silent fabricated progress. Failed demo initialization must not expose real data; load retry follows Recoverable interaction defaults; access-error copy remains open. Actual-device verification is a separate operational activity and cannot be satisfied by this flow.

### UJ-3 — Alex Guides One Driver and May Take Over Acutely

1. Under `Forbered neste skift`, Alex selects FADDER and reviews the own shift, including separate own planned driving and the fadder activity.
2. Alex reviews and links the accompanied person's shift separately. The assignment covers that same person's whole shift; own planned driving is never copied from it.
3. Permanent FADDER identifies the operational view. The linked trip drives stops, notices and trip changes; guiding controls remain open while the bus moves.
4. **Climax:** an acute takeover is needed. Alex selects `Jeg kjører`; ordinary driver restrictions apply immediately while current trip/progress is retained. The actual temporary driver change does not rewrite either plan.
5. When no longer driving, Alex explicitly returns to guiding through the permitted role-change path. A later own planned trip is selected only from the own confirmed shift under driver restrictions.
6. Final own-day completion leads to summary and closing; an accompaniment boundary alone cannot end the day.

**Failure paths:** unresolved linking stays visible; import cancellation preserves each confirmed plan. Neither scheduled time nor missing GPS silently changes role, person or ownership. Imported copies and accompanied evidence follow Accompanied-person imports and summary scope.

### UJ-4 — Alex Teaches, Accompanies Different People and Drives Own Trips

1. Alex selects INSTRUKTØR and reviews the own assignment: own trips, classroom teaching, office work and accompaniment blocks, or no accompaniment at all.
2. Each accompaniment block links a separately reviewed person's shift and only the accompanied portion. Selecting another person's trips never creates planned own driving.
3. Teaching/office show own activity without passenger progression. During accompaniment, permanent INSTRUKTØR marks the linked operational view and open controls.
4. **Climax:** after office work, Alex confirms a block with another person. Context visibly changes; previous-person corrections/evidence do not silently transfer. A later block may link the first person again.
5. Planned own driving begins with `Jeg kjører` and a permitted own-trip choice, restoring driver restrictions. Final summary/closing distinguish own activities from accompanied outcomes.

**Failure paths:** overlaps or missing links stay unresolved; cancellation keeps the confirmed assignment. No-accompaniment days require no fictitious linked shift. Time alone cannot establish physical person change, completed teaching or actual role handover.

## Validation and Implementation Verification

The accepted [43-screen gallery](mockups/remaining-screens.html) closes requested visual coverage, including Matpause, retained-summary entry, mentor workflows and closing. [Coverage inventory](.working/mock-coverage.md) maps every IA surface. Static acceptance does not establish implemented behavior.

Carry these derived completion defaults into validation: confirmed sequence boundaries use an em dash and no-more/no-previous label distinct from missing data; only confirmed plan revisions change a never-ended day's planned end; unavailable Auto preserves appearance/manual preference; transition undo uses the permitted previous-trip selector without rewriting evidence silently.

- All three user-selected lenses completed; all 11 distinct findings are addressed. Structure and prose polish are complete. See the [validation report](validation-report.md) for original findings and dispositions, and [final static checks](.working/final-verification.md) for reference verification.
- Verify simultaneous headings, long names and control fit without losing stop context; mounted readability/touch, offline/auth recovery and accessibility require actual-device checks.
- Verify browser wake/GPS capabilities, automatic-theme trigger/stability and responsive tablet/PC behavior; simulation is not evidence of capability.
- Mentor source-file deletion and accompanied-only summary/export are settled in Accompanied-person imports and summary scope. Verify implementation against that boundary.
- Unillustrated failure copy/loading feedback must preserve established recovery and uncertainty rules.

See [.working/coverage-draft.md](.working/coverage-draft.md) for inherited source mapping. Original review reports remain available through the validation report; they describe the pre-fix document state.
