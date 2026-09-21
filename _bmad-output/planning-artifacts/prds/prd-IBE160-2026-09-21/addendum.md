# PRD Addendum

Current status: the product owner explicitly approved the final PRD on 2026-09-21. References below to pending finalization or approval describe earlier discovery stages.

Public version: Alex is a pseudonym. Personal routine details and unnecessary site-specific operational detail have been generalized; product decisions and supersession history are preserved. Private originals and the canonical append-only log remain local and are excluded from Git.

## Reading This Decision History

This addendum preserves discovery history rather than replacing the current requirements baseline. Within the discovery sections, phrases such as “remains open” describe the state at that point in the conversation; they are not a current task list. The PRD is the current normative document. Explicit SUPERSEDED markers identify earlier scope or unresolved-status wording replaced by later decisions; the original paragraphs remain for provenance. A PARTLY SUPERSEDED marker replaces only the identified clause, not the factual context or remaining limitations. Current open items are classified A/B/C in PRD section 10. Historical mentions of an open question do not independently reopen a resolved decision.

## Resolved Finalization Decisions

**Finalization decision A-7 — remembered sign-in, resolved:** The product owner selected 14 days of remembered sign-in and no interruption of an active shift merely to sign in again. Renew sign-in between shifts when the remembered period expires. This does not select an authentication technology or override explicit logout/access revocation. All planned A product decisions are now resolved; source reconciliation, findings treatment, editorial/privacy passes and explicit approval remain.

**Finalization decision A-6 — missing source timestamp, resolved:** Keep a notice visible when the source supplies no update time, explicitly labelled `Kildens oppdateringstid er ukjent` beside the assistant's last successful retrieval time. Never substitute retrieval time for source update time. This settles the product presentation; source metadata interpretation and freshness qualification are downstream validation, not a prerequisite for PRD approval.

**Finalization decision A-6 — return after manual removal:** A later changed version must reappear as updated, with the existing changed-notice emphasis and no chime. An unchanged version stays removed from the overview for the rest of the shift; retain this state across recovery/restart. This resolves the reappearance question without erasing the original display/removal evidence or treating a changed notice as newly created.

**Finalization decision A-6 — disappeared notice:** Retain a notice that disappears without confirmed end status, labelled `Status usikker – sjekk originalkilden`. The product owner requires manual removal from the overview after checking the original source. Preserve manual-removal and previously displayed-notice evidence in the daily summary; this is not a source-confirmed ending. Existing interaction restrictions apply. Reappearance was unresolved at this point; the later A-6 decision above and FR-14 now define it.

**Finalization decision A-5 — timer state, resolved:** Cancel the pending thirty-second collapse when reliable speed falls to at most 6 km/h; a new high-speed transition starts a fresh interval if content is open. Reliable GPS recovery resets/cancels the five-minute outage timer, and a subsequent loss begins a fresh interval wherever waiting is required. Obsolete timers must not override current access state. This resolves earlier timer-reset questions without changing free startup access or the approved outage exceptions; technical reliability criteria remain downstream work.

**Finalization decision A-4 — pilot evidence, resolved:** Private PDF exports together with the pilot user's external notes are sufficient for the course pilot. A separate retained anonymized test/quality dataset is deferred. This supersedes earlier permission to retain such a dataset as a current-MVP option: there is no pilot-archive exception to the seven-day deletion of application shift data. User-held PDFs and notes are outside application cleanup; material prepared for publication or assessment must still be anonymized.

**Finalization decision A-4 — never-ended shifts:** The product owner confirmed automatic deletion of the same associated data seven days after the planned end of a shift that was never explicitly ended. Expiry does not mark the shift, trips or activities completed. This resolves the earlier never-ended-shift retention question; planned end time is a retention reference, not evidence of actual completion.

**Finalization decision A-4 — completed/aborted shift deletion:** The product owner confirmed that the seven-day period applies to both completed and aborted shifts and all associated application data: summary, uploaded document, retained position data, corrections and notice history. Measure from confirmed completion/abortion; reopening or exporting does not reset it. User-held PDF exports remain outside application cleanup. This replaces ambiguous references to deleting only temporary recovery data. These retention questions were unresolved at this point; the later A-4 decisions above and FR-24 now settle both.

**Finalization decision A-3 — minimum offline scope:** The product owner confirmed that the whole fully loaded shift must remain usable without internet, including available stop lists, GPS-based progression while GPS works, trip/activity transitions, manual corrections and the daily summary, also after restart. New disruptions and other source updates wait for internet. This resolves earlier ambiguity about offline support for later trips and restart; it does not promise data that was never loaded or decide a storage technology. FR-17/20 carry the requirements.

**Finalization decision A-2 — undetected depot arrival:** The product owner approved `Avslutt skift` in the submenu as a fallback when depot arrival is not detected, particularly without GPS. Apply the normal confirmation and interaction rules, including their agreed exceptions. A normally finished shift need not be marked aborted simply because location detection failed. This resolves the FR-21 fallback.

**Finalization decision A-2 — no automatic candidate:** The product owner confirmed direct trip selection from the already confirmed shift if automatic selection finds no candidate. Existing interaction restrictions and startup/GPS-loss exceptions apply. Use the agreed timetable-recovery and missing-stop fallback for the selected trip when necessary. This replaces earlier no-candidate uncertainty; see FR-6.

**Finalization decision A-2 — missing stop list:** First attempt to recover a usable stop list from applicable timetable data. If unsuccessful, the product owner approved showing known trip information with `Stoppinformasjon mangler`, without automatic stop progression, and allowing manual completion/abortion and next-activity selection when interaction rules permit. Manual actions are not GPS-confirmed evidence. This settles the previously undefined operational behavior of an accepted trip without stop details; technical retrieval and matching choices remain downstream work.

**Finalization decision A-1 — current:** The product owner confirmed one ten-second `Siste stopp` indication before every transition to deadhead travel, meal break (with or without relocation), bus change, pilot-car transfer or depot return. Same-route return keeps the previously agreed GPS/manual trigger and does not start after a ten-second timer. This supersedes earlier wording limiting the timer to only some special displays. A break without relocation must not be labelled deadhead travel. FR-10 is the consolidated requirement.

## Source Detail Preserved for Downstream Work

- **PDF evidence:** The authoritative brief addendum records varied layouts, mixed columns, continuation pages and character-extraction errors in private shift samples. Those PDFs were not visually verified during the earlier extraction. Validate representative fixtures later; no private filenames, documents or identifiers are reproduced here. This supports FR-2–4 and B-2/B-5, not a claim that import already works.
- **Course evidence:** The authoritative course-context source records proposal approval, a 70% code/functionality and 30% reflection weighting, and documentation of AI use and quality assurance. These are inherited course-delivery context, not new product features or technology mandates. Keep delivery/reflection evidence during implementation; exact dates remain C-1/C-2. Consult the [original course-evidence section](../../briefs/brief-IBE160-2026-09-21/addendum.md#course-evidence-and-delivery-constraints) for provenance rather than copying private teaching material.
- **Deferred speed and AI detail:** The source's desired advance speed-limit-change warning within 100 metres is separate from FR-8's stop-progression distance. Any later speed feature must disclose uncertain road association and withhold unverified warnings rather than reuse a neighbouring road's limit. AI relevance sorting and short alerts remain future ideas with no newly agreed priority or selected technology. None is mandatory course-MVP scope.

## Journey Discovery: Before Duty and First Bus

Source: Alex's account during guided PRD discovery. This is a partial account of the current workflow, not a confirmed end-to-end journey or a list of assistant features. Exact operational identifiers are anonymized.

1. The evening before duty, Alex opens the Tide app to check which lines he will drive and whether pilot-car driving is scheduled before or after the shift to take over or hand over a bus.
2. Shortly before duty, he uses the same app to register arrival at the depot.
3. He checks which bus he will drive and whether he will use the same bus throughout the day or change buses during the shift.
4. He goes to the first (or only) bus and performs its safety inspection.
5. He acknowledges completion of the safety inspection in the app.

Alex confirmed that this is the Tide app, a different application from Selfservice. Selfservice can also be used to check shifts and buses, but Alex finds the Tide app more convenient. This describes his current use; it does not establish an available integration with either system.

At this stage, the boundary between the existing app and assistant was still being explored; PRD section 5 now excludes recreating Tide workflows. Arrival registration and safety-inspection acknowledgment are observed existing tasks, not approved assistant requirements. The relationship between pilot-car driving and other transfer activities also remains to be clarified; they must not be assumed equivalent.

## Journey Discovery: Preparation and Travel to the First Trip

After the safety inspection, Alex completes any required vehicle preparation, including winter equipment where needed, then travels to the first stop or a nearby holding area before the first scheduled passenger trip.

Alex reports that he must be at the first stop two to three minutes before the trip starts. This is recorded as his reported working practice, not an independently verified rule or an approved assistant alert requirement. The information used to decide whether chains are needed and to prepare for route conditions has not yet been elicited. These physical preparation tasks do not themselves imply assistant features.

## Journey Discovery: Information Gathered Before Leaving the Depot

Alex reports consulting several sources before departure:

- Norwegian Public Roads Administration (Statens vegvesen) web pages to check road closures.
- A daily ChatGPT morning report before duty covering road conditions/closures and route diversions. Its underlying sources, freshness and verification process have not yet been established in this discovery.
- His own observations of driving conditions during the journey from home to work in his private car. These observations do not establish conditions across the entire bus route.
- NavCon for route diversions.
- Svipper's website, which he usually checks for service disruption notices.
- Possible SMS messages from Tide about road closures, received that morning or the preceding day.
- The news and disruption sections of the Tide app, which he says should in theory cover road closures; actual coverage and consistency are not confirmed.

This account supplements the earlier timeline: these checks have already occurred by the time he leaves the depot, but their exact order is not yet established. The personal commute and its observations are distinct from operational pilot-car duties or passenger-car transfers.

These are reported current information sources, not verified integrations or additional MVP commitments. The morning report is a secondary summary, not established here as an authoritative or real-time source. The following account records route-closure escalation; source-failure behavior is consolidated in FR-13–19.

For uncertainty about road closures on his route, Alex can telephone the traffic controller to clarify the situation. This is an existing human escalation path. It does not establish a general precedence rule across all sources, guaranteed controller availability, or a requirement for in-app calling. Handling of other information conflicts remains open.

## Journey Discovery: Waiting and Starting the First Passenger Trip

Alex verifies departure time and whether to wait at a holding area or go directly to the first stop. He manages the bus while waiting, then goes to the first stop and departs on schedule.

Before departure, the driver also prepares the existing onboard systems. Their exact setup procedure is operational context, not an assistant feature or an instruction for operating those systems.

Alex uses NavCon for departure and passing times; these times are also available in the Tide app and the Selfservice PDF, with the PDF containing departure times and only selected passing times. This describes the available timing information, not proof that all sources are synchronized or equivalent.

If NavCon shows more than three minutes ahead of schedule on arrival, Alex goes to a holding area, provided one exists. This is his reported decision rule for the current workflow. It does not establish a requirement for the assistant to duplicate NavCon's timing display or automate this decision. Behavior in other arrival conditions and the source of holding-area knowledge have not yet been explored.

## Journey Discovery: Information Needs During a Passenger Trip

Alex identified four situations where he wants information beyond what NavCon currently provides:

- Uncertainty about the applicable speed limit.
- Approaching narrow road sections with room for roughly one bus or insufficient width for two buses to pass comfortably. He obtains information elsewhere to prepare and reports that NavCon warns only when the situation is very close.
- Weather awareness to prepare for potentially slippery sections, reduced braking effectiveness, or reduced visibility. Weather information must not be treated as confirmed local road-condition observations.
- Sudden road closures: NavCon may carry a message, but Alex reports that it can arrive later than he would prefer.

> **SUPERSEDED PRIORITY: Speed limits and weather are optional; meeting-bus warnings rank ahead of them subject to the simple-addition exception. See PRD section 5.**

These are user-reported needs and limitations, not independently verified claims about NavCon or commitments to new course MVP features. Earlier agreed scope remains in force: speed-limit information is a desired but feasibility-dependent first-version capability; meeting-bus support and weather are later candidates. The need for earlier sudden-closure information is captured without assuming that a sufficiently timely source exists or expanding the planned-disruption MVP boundary.

> **COMPLETED DISCOVERY: The example and subsequent confirmed journey below replace this earlier next-step statement.**

The next discovery step is to establish a concrete narrow-road episode, including what information Alex seeks, its source, when he checks it, and what decision it supports. Safe opportunities for interaction, useful warning lead time, and behavior when information is missing or uncertain remain open.

### Concrete Example: Meeting Buses on a Narrow Corridor

Alex describes the example corridor as having several narrow sections. On entering the road, he checks the time until approaching buses reach the stop he is passing. He makes an approximate calculation of where they are likely to meet and how long he expects to have passage before that meeting.

He proceeds toward the anticipated meeting location. Where additional real-time stop displays are available along the road, he checks them to confirm or revise his estimate. At the anticipated meeting location, he often stops completely and checks a real-time map or app to assess how far away the approaching bus is. If it is sufficiently close, he waits. If it is farther away than expected, he proceeds to the next place he considers safe for buses to pass and waits there until the approaching buses have passed.

Alex explicitly describes these as largely approximate judgments. This is a reported current practice, not driving guidance or a validated prediction method. His estimate of available passage is not confirmation that the road is clear. The map/app identity, freshness and coverage, treatment of multiple approaching buses, and basis for choosing safe meeting places remain unconfirmed.

This example adds user-contributed depth to the deferred meeting-bus capability; it does not move that capability into the course MVP. Any future requirements must preserve the distinction between an estimated encounter and confirmed observations. A complete user journey will be structured and confirmed after further discovery.

Alex clarified that, when stopped, he uses either the Svipper app, which shows estimated arrival time at the stop he is at, or kart.svipper.no. These are identified current-use sources, not verified integration options. An estimated arrival time must not be documented as a confirmed bus position. Their data freshness, coverage and behavior when information is missing have not been verified.

When a source is missing information or appears outdated, Alex first checks the other source, then closes and reopens them to see whether the information updates. If this does not help, he reports trying to see farther ahead and possibly proceeding slowly, depending on whether he is within a defined warning zone. This records his account of current practice, not a recommended driving procedure. Reopening a source does not by itself establish that its underlying data is current, and agreement between the two interfaces does not establish independent verification.

Alex reports one defined warning zone on the example corridor despite roughly three to four narrow obstacles along the road. This is reported coverage, not independently verified coverage. Missing information or the absence of a warning must not be interpreted as confirmation that no bus is approaching. The example reinforces the need to distinguish unavailable information, limited coverage and confirmed observations in any later meeting-bus capability.

## Journey Discovery: After a Trip and Vehicle Duties

Alex finds the next activity and its timing in NavCon. He describes a vehicle duty (Norwegian: vognløp) as covering the full day of work for the bus. During his own working day, he sometimes needs to change vehicle duty; he has identified this beforehand in the Tide app or the Selfservice PDF.

The driver's shift and a vehicle duty are distinct concepts. How breaks or transfer activities appear in this sequence remains to be elicited. No exact shift, vehicle-duty, bus or trip identifiers are recorded.

Alex described the vehicle-duty change in NavCon: open the menu, end the current vehicle duty, enter the new six-digit vehicle-duty identifier, select the trip, and confirm. The new vehicle duty then appears. If the touchscreen does not work, he must call the traffic controller to have the problem resolved. No actual identifier is retained here.

This describes an existing NavCon interaction and its human fallback, not a requirement for the assistant to control NavCon or replace that workflow.

Alex clarified that a vehicle-duty change can occur either in the same physical bus or alongside a bus change. Changing buses usually also means changing vehicle duty, but a replacement due to a bus fault may retain the existing vehicle duty. A physical bus and a vehicle duty must therefore remain distinct concepts; neither change universally implies the other.

## Journey Discovery: Break and Return to Service

Alex drives to the designated break location shown in the Tide app and Selfservice or its PDF. He describes this as usually a suitable break facility to either the previous trip's last stop or the next trip's first stop.

He parks, switches off the engine, opens the door, switches off the main power, closes the door, and goes into the break facility or a canteen if available to eat lunch. He returns to the bus shortly before the break ends to allow time to restart all systems and drive to the next trip in his shift.

This records his current practice, not an operating procedure or a requirement to shorten breaks. How the schedule accounts for restart time and travel after the break, how Alex judges when to return, and what happens when the preceding trip is delayed remain to be clarified. The distinction between scheduled break time and preparation or transfer activities must be established before defining timing-related requirements.

Alex reports that delays generally reduce the actual break available while the next scheduled departure remains unchanged. If a necessary pause does not fit the remaining time, he calls the traffic department to inform them and takes the break he needs. This is a description of current practice, not a determination of break entitlements or a requirement for the assistant to recommend reducing or skipping breaks. Scheduled break duration, actual time available and a driver's necessary pause must not be treated as interchangeable concepts.

## Journey Discovery: Physical Bus Change at the Depot

Alex reports that bus changes usually take place at the depot. He logs out, retrieves his driver card, checks the outgoing bus and secures it before leaving.

He locates the next bus through Tide, performs its safety inspection and prepares its systems before departure. This is reported current practice, not an operating checklist or a requirement for the assistant to perform those system interactions. The account confirms that taking over another physical bus includes a fresh safety inspection and setup; it is distinct from changing vehicle duty in NavCon.

Handling of an unavailable or faulty replacement bus and the sequence for transfers away from the depot remain unexplored.

## Journey Discovery: Pilot-Car Transfers for Driver Relief

When taking over a bus away from the depot, Alex goes to the traffic office and requests a pilot car for the required destination. He drives to the takeover location and takes over the bus after the finishing driver has logged out.

When another driver takes over his bus, Alex logs out of its systems, packs his belongings, finds the pilot car at the agreed location, drives back to the depot, and returns the keys to the traffic department.

These are two reported transfer directions associated with driver relief. The account does not establish how the agreed location is communicated, how changes or delays are handled, or the full inspection and login procedure for an off-depot takeover. Whether "pilot car" and "passenger-car transfer" are interchangeable terms in all relevant shift records remains unconfirmed. No additional integration or MVP capability is committed by recording this workflow.

Alex clarified that Tide provides the driver-change time and place. Pilot-car parking is designated at the depot and some other locations; elsewhere, drivers coordinate the actual parking position.

The scheduled handover location and the car's actual parking position are therefore distinct. The account does not establish that the app provides a precise car location, nor that every handover point has a designated space. This is a description of current coordination, not parking guidance or a vehicle-tracking requirement. Handling of changes, delays or a missing pilot car remains open.

## Journey Discovery: End of Shift

For the described return by pilot car, Alex considers the shift complete once he has delivered the keys to the traffic department and left its office. He did not describe an additional app acknowledgment at this point. This does not establish the end-of-shift procedure for every other kind of shift.

Alex subsequently clarified that the usual ending is to park the bus at the depot, shut it down and lock it. The pilot-car return and key handover are an alternative ending when the shift involves that form of driver relief.

## UJ-1: Alex Completes a Varied Scheduled-Service Shift — Confirmed Current Workflow

This is a representative composite of the activities Alex described, not a claim that every activity occurs on one specific shift. It describes the current workflow and needs, not a proposed assistant interaction flow.

Alex confirmed the summary, with the correction that returning and securing the bus at the depot is the usual ending and returning by pilot car is an alternative.

- **Context and preparation:** The evening before, Alex checks lines and any pilot-car transfer in the Tide app. Before departure, he gathers road and disruption information from several sources and can call the traffic controller about unclear route closures. At the depot he registers arrival in Tide, checks the assigned bus and any changes, inspects the first bus and acknowledges the inspection.
- **First departure:** He prepares the bus and its systems, checks timing in NavCon, and travels to the first stop or a holding area. He reports being at the first stop two to three minutes before departure; if NavCon shows more than three minutes ahead on arrival, he uses a holding area where one exists.
- **During trips:** He follows the vehicle duty in NavCon. Additional needs arise around uncertain speed limits, narrow sections, weather and timely closure information. On the example corridor, he combines stop-display estimates with Svipper app/map checks when stopped to judge possible bus encounters. Missing data leaves uncertainty; no warning does not establish a clear road.
- **Break and changes:** The app/PDF identifies the break location. He parks and powers down, then returns in time for system startup and travel to the next trip. Delays generally reduce his actual break; he informs the traffic department if a necessary pause cannot fit. A vehicle-duty change may occur in the same bus or alongside a physical bus change. A physical change includes logging out, retrieving his card, checking and securing the old bus, locating and inspecting the next bus, and logging in again.
- **Driver relief:** If taking over away from the depot, he obtains a pilot car at the traffic office and drives to the app-specified handover location. When relieved himself, he logs out, packs his belongings, finds the pilot car and returns to the depot.
- **Resolution:** Usually he finishes by parking the bus at the depot, shutting it down and locking it. Alternatively, following relief and return by pilot car, the shift is complete when he has returned the keys to the traffic department and left its office.

> **SUPERSEDED SCOPE STATUS: The current proposed MVP and acceptance criteria are in PRD sections 5 and 9.**

The candidate value of the assistant is a convenient overview across these activities and relevant information sources. The exact assistant-supported journey, MVP boundary and acceptance criteria remain to be agreed; the full operational workflow is not automatically assistant scope.

## Desired Assistant Behavior: Evening Before Duty

Alex wants to upload his shift the evening before and see the shift, reporting time and relevant disruptions. His desired disruption coverage includes both passenger-service routes and deadhead travel to the first stop and from the last stop. Identifying the actual deadhead route and matching notices to it remain unresolved; these must not be assumed to follow a passenger-service route.

Weather and potential driving conditions are desired additions if time permits. A suggestion to consider snow chains would be a bonus. Alex suggested weather forecasts as a possible basis, but the adequacy of forecasts for such advice is not established. Forecast conditions, observed road conditions and a driver's decision to fit chains are distinct. No chain recommendation capability or weather integration is committed for the course MVP.

> **SUPERSEDED DISCOVERY STATUS: Import review, correction and morning-notice behavior were subsequently decided; see FR-2 through FR-5 and FR-12 through FR-14.**

This establishes Alex's initial priority for the evening-before experience, not final approval of the complete course MVP. Upload validation, how uncertain extraction is presented, disruption matching and freshness on the following morning still require elicitation.

### Deadhead Route Choice and Reported Operating Guidance

Alex chooses the deadhead route himself, subject to operating guidance he describes as follows:

- Prefer the tunnel rather than the bridge when travelling toward the relevant operating area.
- Do not travel through locally restricted areas during rush hour.
- Avoid passenger-service routes as far as practicable.
- Do not detour via shops, petrol stations, home or other places for personal benefit.

These are user-reported operating constraints, not independently verified policy wording or a complete route-planning rule set. In particular, the account does not establish exact rush-hour windows or every applicable road restriction.

> **SUPERSEDED MVP QUESTION: Automatic deadhead routing is deferred. The limitations remain valid; fastest suitable route is a later-extension preference.**

The intended deadhead route cannot be inferred reliably from shift endpoints alone. How the assistant learns the driver's intended route, or communicates the limits of disruption relevance when that route is unknown, remains an open requirement decision. No route optimization or navigation capability has been approved.

Alex subsequently asked that the shortest/fastest road route be used as the logistical starting point for deadhead travel. He confirmed that shortest travel time takes precedence over shortest distance, provided the route is suitable for the bus and follows the previously reported operating guidance. This is a desired default basis for assessing relevant disruptions, not confirmation of the route actually driven. How bus suitability is established, feasibility within the course MVP, and how the driver can correct an unsuitable assumed route remain unresolved. This decision does not by itself commit turn-by-turn navigation or a particular routing technology.

## Desired Assistant Behavior: Morning Before Duty

When Alex opens the assistant before duty, he wants updated weather forecasts when available, visibility of disruptions that have appeared, changed or ended since the previous evening, and readiness to enter the assigned physical bus number manually. Consistent with the approved brief, the physical bus number is distinct from the vehicle-duty identifier.

> **PARTLY SUPERSEDED: Presentation and refresh-failure behavior were later decided in FR-14 and FR-17 through FR-19. Missing source metadata remains a source limitation.**

Weather remains a time-permitting extension under the earlier priority decision. A morning refresh does not by itself establish continuous real-time coverage. How changes are presented and how failed refreshes or missing source status are communicated remain to be specified. A notice disappearing from a feed must not silently be treated as verified resolution.

> **PARTLY SUPERSEDED: Opening marks seen, new/changed bold clears on opening, seen state persists, and ended notices remain for ten minutes. Color details belong to UX.**

Alex chose bold text to distinguish new disruption notices in the morning overview. He wants ended notices to remain visible briefly with strikethrough so their ended state is apparent. For changed notices, he wants color-coded text with bold emphasis until he has seen the change. The exact colors, whether color applies to the entire notice or the changed text, and the observable action that counts as seeing a change remain to be clarified. The retention duration for ended notices and when a new notice ceases to count as new also remain open. Strikethrough represents an ended notice, not a failed refresh or a notice merely missing from a source.

For marking a change as seen, Alex considered two alternatives:

- Keep notice headings visible and let the driver expand a notice to read its full content; opening it marks it as seen.
- Provide an explicit checkbox to mark the notice as seen; a subsequent update clears the checked state.

Alex selected the first alternative because it appears tidier: notice headings remain visible, and opening the content marks the notice as seen and clears its unread bold emphasis. A subsequent change is emphasized again until opened, consistent with his earlier requirement for changed notices. The explicit checkbox alternative is not selected. Opening records a viewing action rather than proof of comprehension.

### Notice State and Retention

Alex confirmed that opening a new notice clears its bold emphasis, just as opening an updated notice does. A later update restores emphasis until the updated version is opened. Seen-state behavior therefore applies consistently to new and changed notices; it does not imply removing the separate color coding for changes.

Alex confirmed that seen state should persist throughout the shift, including network outages and restart. Unchanged notices must not be treated as new or unseen again on recovery. Actual updates still regain bold emphasis, while existing audio rules prevent repeat chimes for unchanged notices. How the source supports stable notice identity and detection of real updates remains a feasibility check.

Alex set the visible retention of ended disruption notices to 10 minutes with strikethrough before removal from the overview. The interval is measured from the assistant registering ended status so the change remains observable when retrieved after the source's end time. This does not remove the notice from the daily summary or establish that disappearance from a source proves it ended.

### Message Interaction While Moving

Alex requires message interaction to be locked above walking speed so the interface does not encourage manipulation while driving. He permits interaction at walking speed or below. This is a requested product behavior, not a declaration that interaction at low speed is safe in every situation.

Alex selected 6 km/h as the upper interaction threshold: message opening is permitted at or below 6 km/h and locked above it. He specifically requires it to remain unavailable at 10 km/h, which he reports as the depot setting for the buses. The threshold is a product decision, not a physiological definition of walking or jogging speed.

> **SUPERSEDED OPEN-QUESTION STATUS: Subsequent movement decisions are consolidated in FR-16. Sensor-quality thresholds are downstream validation work.**

Behavior when speed is missing or unreliable and treatment of a message already open when the threshold is crossed remain to be agreed. The scope of this decision is message interaction; restrictions for other controls have not yet been elicited.

> **PARTLY SUPERSEDED: Five-minute unlocking, free startup access, recovery and thirty-second collapse were subsequently agreed; FR-16 is authoritative.**

For GPS loss, Alex confirmed that the same 6 km/h threshold applies: retain the locked state when the last recorded speed was above 6 km/h, and retain the unlocked state when it was at or below 6 km/h. Signal loss must not itself unlock a previously locked message interface. He proposed retaining the high-speed lock for five minutes or until GPS returns; behavior after five minutes without a new signal remains to be clarified. Handling before any reliable speed reading and evaluation when GPS returns also remain unresolved. Elapsed time alone does not establish that the bus has stopped, and a previous low-speed reading does not establish its current speed.

> **PARTLY SUPERSEDED: The unlocking decision remains valid; startup and recovery are no longer undecided. See FR-16.**

Alex subsequently decided that, if GPS remains unavailable, the lock must be released after five minutes even when the last measured speed exceeded 6 km/h. He rejected indefinite locking because prolonged signal loss, for example from possible jamming, could prevent access. This is an explicit availability exception to the normal speed-based lock, not evidence that the bus has stopped. The product must not be described as guaranteeing interaction prevention above 6 km/h under all conditions. Presentation of the unknown-speed state, handling before any reliable reading, and behavior on signal recovery remain to be specified.

> **SUPERSEDED OPEN CLAUSE: The already-open-message case was subsequently settled at approximately thirty seconds; automatic recovery remains valid.**

Alex confirmed that the normal speed-based lock resumes automatically when reliable GPS speed returns: opening messages is locked above 6 km/h and permitted at or below 6 km/h. This also applies after the five-minute outage timeout has unlocked messages. Treatment of content already open when locking resumes remains to be specified.

Alex specified that a message already open when the speed lock activates may remain visible for approximately 30 seconds before collapsing automatically to its heading. Opening any other message is blocked immediately, including when GPS returns with a speed above 6 km/h. This is a brief visibility allowance for existing content, not permission to open further content while locked. The speed-drop case was unresolved at this point; A-5 and FR-16 now cancel collapse when reliable speed falls to 6 km/h or below.

> **SUPERSEDED NARROW SCOPE: Free startup access was subsequently clarified to cover controls generally, not only messages; see FR-16.**

Alex chose to allow message opening at startup before any valid speed measurement is available. This means interaction is unlocked, not that all message bodies automatically expand. Once reliable speed becomes available, the normal 6 km/h rule applies. Unknown speed at startup is not confirmation that the bus is stationary; the lock is therefore conditional on available speed data, with the explicitly agreed startup and outage exceptions.

## Desired Assistant Behavior: Glanceable Driving View

Alex wants the main driving screen to show the stop "here and now," the next stop, applicable speed limit, local weather "here and now," relevant disruption headings, route and destination without opening messages or menus.

> **SUPERSEDED STOP QUESTION: Three-stop semantics were subsequently confirmed in FR-7. Weather/speed remain optional.**

The meaning of the current stop while between stops remains to be clarified. Weather retains its time-permitting extension status, and speed-limit display remains dependent on establishing sufficiently reliable data. This desired screen content does not itself expand the agreed course MVP. Whether local weather represents observations or a forecast must be explicit rather than implying live measurements. Disruption headings remain distinct from the expandable bodies governed by the message interaction rules.

Alex clarified a three-stop view: at a stop, show the previous stop, the current stop and the next stop. Upon departure, advance the view so that the departed stop is previous and the next two upcoming stops are shown while travelling between stops. A forthcoming stop must not be represented as a confirmed current location merely because it occupies a particular position in the display. Arrival/departure detection, stops passed without stopping, route endpoints and uncertain positioning remain to be specified.

Alex confirmed that passing a scheduled stop without stopping must advance the display in the same way as leaving that stop. Progression therefore follows actual progress along the active trip and must not require a stationary event at each stop. This does not decide how to treat stops bypassed by a diversion rather than physically passed, or how passage is detected when positioning is uncertain.

Alex set a maximum progression lag of 100 metres after passing or leaving a stop. This is distance travelled along the route after passage, not a 100-metre proximity radius around the stop. He reports that the shortest stop spacings are approximately 250 metres, so validation must include closely spaced consecutive stops and verify that progression does not skip or confuse them. The spacing is user-reported, not a verified network-wide minimum. Behavior with unavailable or unreliable positioning remains a separate fallback concern; simulated compliance does not establish real-device compliance.

Alex confirmed that, when GPS positioning is too uncertain to determine which stop was passed, the display must retain the last confirmed stop and clearly indicate uncertain position instead of guessing forward. The retained stop represents last confirmed progress, not a claim that the bus is currently there. The 100-metre progression criterion applies when positioning supports reliable progression; the uncertainty fallback must be evaluated separately and must not conceal positioning failures from pilot quality reporting.

For diversions, Alex wants the display to show the stops actually passed when the assistant has the relevant stop-sequence information. If that information is unavailable, it must recover when the bus reaches a later recognized stop on the active route, even if this means advancing by two or ten stops. Progression must not remain stuck waiting for each omitted stop to be visited.

Knowing that a diversion exists is not by itself knowledge of its replacement stop sequence. The source and reliability of that sequence, and the evidence needed to recognize a later stop on the correct trip and direction, remain unresolved. This requirement does not authorize inventing replacement stops or selecting a different line solely because nearby stops overlap.

> **PARTLY SUPERSEDED: Automatic progression after correction and later GPS-loss control exceptions were confirmed; see FR-9 and FR-16.**

If the stop display is wrong, Alex wants to open the stop overview and select the correct stop the next time he comes to a complete stop at a stop. This manual correction requires standstill, unlike the separate message-opening allowance at speeds up to 6 km/h. The behavior after selecting the stop, how standstill is established, and how correction is handled without reliable speed or position data remain to be specified. The GPS-loss exceptions for message opening are not automatically applicable to stop correction.

Alex confirmed that selecting the correct stop manually establishes the new progression point, after which automatic stop progression resumes as he drives on. This does not establish that unreliable positioning becomes reliable merely because a manual correction has been made. Standstill detection and unavailable-sensor behavior remain open.

### End of a Passenger Trip

Alex confirmed that registered arrival at the active trip's final stop counts the passenger trip as completed in the daily summary, unless it was manually aborted. Scheduled end time alone does not establish completion. This decision does not define completion evidence for non-passenger activities or for a trip whose final-stop arrival could not be confirmed.

For non-passenger activities such as meal breaks, bus changes and pilot-car transfers, Alex selected position and timing together as the basis for completion. Exact matching criteria and fallback when position or an activity location is missing remain unresolved, especially because the location field is optional. This is inferred activity progress, not independent verification of physical actions such as a bus handover.

Alex confirmed that, when GPS or the activity location is missing and completion cannot be established, the daily summary must show "Gjennomføring usikker" and allow him to confirm completion manually. The confirmation belongs in the correction evidence and must not be represented as sensor verification. Correcting summary evidence does not restart a completed shift. Exact automatic-completion thresholds remain open.

For initial activation, Alex wants the assistant to select the first trip automatically from the shift, position and current time, with manual override if it chooses incorrectly. He confirmed that, if the selection is ambiguous, the assistant must present the candidate trips for user selection before starting the driving view. This supplements, rather than replaces, the requirement to retain a delayed active trip until it actually ends. Existing standstill restrictions apply to manual trip selection. A case with no usable candidates remains distinct from multiple plausible candidates.

Alex confirmed that an ongoing trip must remain active until it actually ends, even if a delay means the next trip's scheduled start time has passed. Scheduled time alone must not start the next trip. This keeps planned timing distinct from actual progression; skipped or cancelled trips still need an explicit correction path rather than being inferred solely from elapsed time.

### Manual Changes and Early Termination

Alex requires a submenu offering selection of the next trip, interruption of the current trip, registration of a physical bus change due to a bus fault, and early termination of the shift, for example for personal reasons. A physical replacement must remain distinct from a vehicle-duty change, consistent with the previously confirmed domain distinction.

Interrupted or skipped activities must not be reported as completed in the daily summary. The exact outcome of each action, confirmation behavior and movement restrictions remain to be clarified. Mentioning illness as an example does not create a requirement to collect medical information or a free-text reason.

> **HISTORICAL RESTRICTION SCOPE: This entry predates free startup access and five-minute outage access for other controls. The later decisions below and FR-16 govern those exceptions.**

Alex confirmed that the manual-change submenu requires a complete stop. He clarified that by moving at speed he meant driving speed rather than walking speed: the previously agreed allowance to open messages at up to 6 km/h remains unchanged. He explicitly requires "Next stop" and "Previous stop" as the only controls permitted at driving speed when GPS-based progression gets stuck. These direct stop-correction buttons are distinct from opening the stop overview to select an arbitrary stop, which still requires a complete stop, and from next-trip selection in the submenu. The assistant recommendation to require standstill for these two buttons was not accepted. This is an intentional interaction exception, not evidence that operating the buttons is safe in every situation. Existing message-specific GPS-loss and startup exceptions remain separately recorded and do not extend permission to other controls.

Alex specified that the direct "Next stop" and "Previous stop" buttons appear when GPS is lost; they are not permanently visible during normal GPS operation. Otherwise, stop progression follows GPS automatically. He cited bus ticket machines as inspiration, not as a verified specification or an integration requirement. Loss of internet alone must not trigger these controls when positioning still works.

Alex confirmed that, when reliable GPS positioning returns, these buttons disappear and the stop display automatically realigns with the bus's actual position in the active trip. Manual progression during the outage must not prevent this recovery. A returned but still uncertain position does not satisfy the reliable-position condition, and recovery must not silently switch to a different trip or direction.

Alex confirmed that selecting "Avbryt skift" (abort shift) uses the same confirmation dialog and daily-summary flow as normal completion, with the shift clearly marked as aborted. Cancelling the confirmation leaves the shift active. Remaining trips and activities must not be reported as completed. The existing summary/export and temporary-retention requirements apply; this does not require recording a medical or other sensitive reason for the interruption.

> **SUPERSEDED STARTUP QUALIFICATION: The five-minute rule concerns loss after a valid signal. Later clarification grants free access before the first valid startup measurement.**

Alex subsequently specified that, without GPS, normally standstill-only functions such as trip changes and shift abortion become available after waiting five minutes. This is an explicit access exception despite unverified current speed. It supersedes the earlier unresolved fallback for those controls, but does not grant immediate access based on the message-specific startup or low-speed-loss rules.

Alex corrected the interpretation of startup access: before the first valid GPS measurement, free access applies to controls generally, including the operational-change submenu and stop selection, not just messages. There is no five-minute startup wait. Once valid speed is received, the normal movement restrictions apply; loss of a previously available signal follows the separately agreed outage rules. This supersedes the earlier narrow startup interpretation. Free access here concerns movement locking, not authentication or confirmation dialogs, and does not establish that the bus is stationary.

He also specified that using the manual stop arrows to advance to the final stop should permit trip transition. He clarified that, for a return trip on the same route, pressing "Next stop" again while at the final stop starts the next trip. Simply reaching the final stop does not start the return trip. Otherwise, the 10-second final-stop indication leads to the relevant special activity view. Such progress must be recorded as manually indicated rather than GPS-confirmed, and a display transition does not prove completion of the next physical activity.

### Between-Activity Displays

Alex wants a clear end-of-trip indication at the last stop, suggesting wording such as "End of the line" or "Last stop." In the turnaround case he described, it should remain until the assistant detects that the bus has turned around and is at the first stop again. Exact wording is not finalized.

> **SUPERSEDED DISCOVERY STATUS: Later activity-display decisions are consolidated in FR-10; A-1 is resolved and reflected in that requirement.**

This describes the turnaround case, not a universal assumption that every next trip retraces the route or starts at the same location. The transition when the next scheduled activity is a different line, deadhead travel, a break, a bus change or shift completion remains to be elicited. Detection must still distinguish the correct trip and direction rather than treating proximity to a shared stop as sufficient evidence.

Alex clarified the desired between-trip display by activity:

- If the next trip starts from the same place where the previous trip ends, retain "End of the line" until the bus reaches the starting stop again.
- If relocation is needed, show "Tomkjøring" (deadhead travel) on one line and the next trip's starting-stop name on the line below.
- For lunch or an activity labelled "unpaid mealbreak," show "Lunsj" or "Matpause." The choice between those two labels remains open; this display preference does not redefine the source activity's paid/unpaid classification.

> **PARTLY SUPERSEDED: Activity progression and special displays were later specified. A-1 now resolves transition consistency; sensing criteria remain downstream validation in B-2.**

The trigger for entering and leaving a break state remains to be elicited. A break and travel to or from its location are distinct activities and must not be conflated without an explicit decision. This clarification does not yet define the display for pilot-car transfers, bus changes or the end of the shift.

Alex clarified that the break indication appears when progression through the shift reaches the activity to be performed, rather than specifying a clock-only trigger. For deadhead travel followed by a meal break, he wants a combined overview with three lines: (1) "Lunsj" or "Matpause," (2) "Tomkjøring," and (3) the first stop of the passenger trip after the meal break, which he explicitly confirmed. This combined presentation does not by itself establish that travel time counts as break time. How activity progression is detected remains open.

For this deadhead-and-meal-break sequence, Alex requires "Siste stopp" (last stop) on arrival at the current trip's final stop. After 10 seconds, the display changes to the three-line overview above. This is a display transition after arrival, not confirmation that the bus has departed or that the meal break has begun. It does not replace the previously specified same-location turnaround behavior or establish timing for every other between-trip activity.

When the next activity is a physical bus change or a pilot-car transfer, Alex wants the same initial "Siste stopp" indication for 10 seconds, followed by "Bussbytte" or "Pilotbil" centered in this display. This communicates the next activity; elapsed display time does not confirm that the change or transfer has occurred. No physical bus identifier, destination or additional line of content was specified for this state.

When the final passenger trip is followed by a return to the depot to finish the shift, Alex wants "Siste stopp" for 10 seconds, followed by three lines: "Returner", "til", "Depot". This is the depot-return state, not confirmation that the shift is complete. It remains distinct from the pilot-car relief ending.

Alex wants a red button labelled "Avslutt skift" (end shift) to appear on arrival at the depot at the end of the shift. Completion is a manual action rather than automatic closure on arrival. In this end-of-shift context, a depot visit for an intermediate break or bus change must not be treated as shift completion. These questions were unresolved at this point. FR-16/21/22 now define interaction, undetected-depot completion and the summary flow; sensing criteria remain B-2 validation.

Alex initially described a thank-you message with an optional affirmation before returning to the main menu. He subsequently refined this into a short end-of-day summary, with "Takk for i dag" (thank you for today) and a daily affirmation based on that day's history at the bottom of the screen. This supersedes the earlier transient-message-only description. It does not select AI generation or any other implementation for the affirmation. FR-22 now requires return to the main menu; the exact control presentation belongs to UX under B-4.

## End-of-Day Summary and Data Retention

For the course MVP, Alex does not require permanent history of completed shifts. On shift completion, the assistant must be able to show a short summary containing:

- Completed trips and activities.
- Relevant disruption notices displayed during the shift.
- Manual corrections.
- Problems encountered with data sources.

> **SUPERSEDED COMPLETION QUESTION: FR-22 now defines passenger-trip arrival, position/time inference and manual confirmation of uncertain activities.**

The thank-you message and day-informed affirmation appear at the bottom. How completion is established for each trip or activity must be defined; planned work or elapsed time alone must not silently be reported as confirmed completion.

> **PARTLY SUPERSEDED: PDF is required, CSV optional and private PDF identifiers are allowed by the later decision. No automatic permanent history is implied.**

Alex confirmed that a user-initiated option to save or export the summary is a course MVP requirement because it supports pilot evaluation. Using the option is voluntary; providing it is mandatory. He selected PDF as the required initial export format; CSV is a time-permitting addition. The destination and treatment of identifying details remain to be clarified. This does not require a separate in-app saved-history mechanism or authorize automatic permanent shift history.

Alex clarified that the private PDF export does not need to anonymize exact shift, bus, vehicle-duty or trip identifiers because it will not be uploaded. This permission concerns the user-held summary only. Project documentation still requires anonymized operational identifiers, and any retained pilot test/quality dataset remains subject to the separate anonymization requirement. It does not authorize uploading or publishing the identifiable report.

> **PARTLY SUPERSEDED: Seven-day operational retention was subsequently selected. A-4 now defers a separate pilot-quality dataset beyond MVP; FR-24 governs application shift-data deletion.**

Raw GPS history, uploaded shift documents and detailed movement data must not be retained unnecessarily after the shift. Exact deletion timing, treatment of interrupted shifts and any user-requested saved summary remain to be specified. Limited anonymized test and quality evidence may be retained during the pilot, but the system must not build a driver performance profile. The permitted fields, anonymization method and retention period for this evidence remain to be agreed; removing identifiers alone must not be assumed sufficient to anonymize detailed location records.

> **SUPERSEDED RESUMPTION QUESTION: Confirmed ended shifts cannot resume; summaries may reopen. Active interrupted shifts recover. A-4 is resolved; FR-24 defines retention scope.**

Alex selected a one-week recovery period after shift completion because a user may finish too quickly and need to reopen the summary. The completed-shift summary and its retained shift document and detailed position data may therefore remain available for seven days, after which the assistant must automatically delete this temporary recovery data. This allows recovery, not permanent shift history, and does not require collecting raw movement data solely to retain it. A PDF already exported and held by the user is outside this automatic application cleanup. Separate pilot-quality retention was undecided at this point; A-4 later deferred that dataset beyond MVP. Handling of interrupted shifts and whether an accidentally completed shift can resume active operation remain open.

> **SUPERSEDED OPEN CLAUSE: Active-shift interruption recovery was subsequently approved in FR-20; the no-resumption rule remains.**

Alex explicitly ruled out resuming a completed shift. Pressing "Avslutt skift" must first display an "Er du sikker?" (are you sure?) confirmation dialog. Cancelling leaves the shift active; confirming completes it and proceeds to the daily summary. The seven-day recovery period permits reopening the summary, not resuming active shift operation. This does not determine recovery from an app interruption before a shift is completed.

> **PARTLY SUPERSEDED: Network-loss behavior was subsequently agreed in FR-17 through FR-19. A-3 is resolved: FR-17/20 cover the entire fully loaded shift, including restart.**

Alex confirmed that an active shift must be recoverable after the assistant closes or the tablet restarts, without re-uploading the shift PDF or re-entering the physical bus number. This is interruption recovery, distinct from resuming a deliberately completed shift, which is not permitted. Preserving an active shift does not establish that previously fetched disruptions or position readings are still current. Which capabilities remain available during a network outage remains to be elicited.

## Connectivity Loss During an Active Shift

Alex requires a clear notice at the top of the screen when internet connectivity is lost, using a yellow warning triangle containing an exclamation mark together with explanatory text. Existing displayed content must remain available rather than disappearing.

Stop progression must continue using available GPS even without internet connectivity. The assistant therefore needs the already-loaded active trip's stop information available during the outage; no particular storage technology is selected here. Previously retrieved disruption notices remain visible but are not refreshed. The warning must make this loss of updates clear so retained notices are not mistaken for newly verified information.

Internet loss and GPS loss are distinct states: continued GPS progression depends on a usable position signal and does not override the separately agreed GPS-loss behavior. Keeping content visible does not establish that all live fields remain current. Automatic refresh and status presentation when connectivity returns remain to be specified.

Alex confirmed that restored connectivity must trigger automatic data refresh. The warning about missing updates remains until retrieval actually succeeds; network availability alone is not evidence of refreshed data. Once connectivity is restored, the warning must accurately describe the remaining update problem rather than continue claiming there is no connection. Successful retrieval also does not establish that source-provided content is recent; source update time and application retrieval time remain distinct. Partial source failures remain to be addressed.

Alex requires a source-specific error to appear in the affected area of the assistant. For example, a failure of the disruption source is shown as its own system-status message within the disruption area. It must be distinguishable from an actual traffic disruption. This local indication identifies the affected information rather than implying that every source has failed.

> **SUPERSEDED FIRST-FETCH QUESTION: FR-19 now defines unavailable status and original-source link when no prior data exists.**

Alex explicitly confirmed that, after the internet connection returns but before synchronization has completed, the top notice must reflect that intermediate state. Suggested wording is "Nettforbindelsen er tilbake – oppdaterer data" (connection restored — updating data), not a continued claim of no connectivity. Exact wording remains editorial. A failed retrieval must be described as a failure rather than indefinitely presented as an update in progress. How the assistant presents a first-ever retrieval failure with no previous data remains to be elicited.

Alex proposed checking for disruption updates every two minutes during an active shift. He considers five minutes too infrequent, noting that most of his routes take around 45 minutes. Treat two minutes as the desired normal-operation retrieval interval, subject to source access and service limits being verified. This interval is not an end-to-end guarantee that a new road event reaches the driver within two minutes: source publication delay and connectivity remain separate factors. Faster polling does not expand the agreed planned-disruption scope into guaranteed acute-event coverage.

Alex approved a short, discreet chime when a new relevant disruption is retrieved while driving, accompanying the emphasized heading. The chime does not open the message or override the speed-based interaction lock. It is associated with a newly received relevant notice, not each unchanged polling result. Alex explicitly limited the chime to new notices: changes to existing notices receive bold emphasis without sound, retaining the previously agreed color coding and seen-state behavior.

During driving, Alex wants the disruption area limited to information relevant to the current trip or activity, not the entire remaining shift. Relevant information for the next trip may appear upon arrival at the current trip's final stop. This relevance transition occurs on arrival and is distinct from the 10-second activity-display transitions. It does not remove the previously requested whole-shift preparation overview before duty.

Alex clarified that the chime is only for a new notice arriving during an ongoing trip and relevant to that trip. Previously fetched notices becoming relevant at a trip transition appear without sound. Updates to existing notices also remain silent. This limits the earlier general new-notice chime preference to the active-trip context; preparation and next-trip previews do not trigger it.

For a disruption-source failure before any successful retrieval, Alex approved "Avviksinformasjon utilgjengelig – sjekk originalkilden" (disruption information unavailable — check the original source), with a link to that source. The assistant must not present this state as no disruptions. Providing a link does not guarantee that the source itself is reachable. Interaction with the source link remains subject to driving-interaction rules rather than providing a way around the message lock.

## Course MVP Priority Clarification

Alex reports that the only communicated submission timing is mid-December 2026 and that the instructor intends to assess the work over Christmas. No exact deadline is confirmed. Instructor demo access must accommodate assessment over Christmas rather than ending at submission; the precise availability end date remains to be agreed. This is user-reported course timing, not independently verified course policy.

Alex reconfirmed approximately ten working weeks at 4–16 hours per week, or roughly 40–160 hours total. Actual capacity will fall somewhere within that range; the upper bound is not a commitment. Feasibility and scope sequencing must account for this uncertainty rather than budgeting every optional capability against 160 available hours.

Alex confirmed that the course project is a website, not a separate installed app. The course MVP is therefore a tablet-adapted browser experience, retaining the approved fullstack and database requirement. An installed app may be considered after the course. This selects the delivery surface without choosing frameworks or detailed architecture. GPS access, recovery, offline progression and sound behavior must be validated in the intended tablet/browser environment; native-app capabilities must not be assumed.

Alex identified the intended pilot device as a Lenovo Idea Tab Plus WiFi tablet, 12/256 GB, with Lenovo Tab Pen, the selected variant. Brave is the expected browser. These are user-provided target-environment details, not verified hardware specifications. Operating-system/browser versions and actual position capabilities remain validation items; the next entry confirms phone tethering. The pen being included does not create a requirement for pen-based operation.

> **CURRENT DECISION: Phone tethering is confirmed; earlier wording that connectivity remains to be established is superseded.**

Alex confirmed that the tablet will receive internet through mobile-phone tethering. Pilot verification must therefore exercise the intended tablet, Brave and phone-shared connection, including loss and restoration of internet access. A connection to the phone does not by itself prove that upstream internet is available or provide evidence about the tablet's positioning capabilities.

> **SUPERSEDED ACCESS QUESTION: Private operational access and separate fictional instructor access were subsequently approved; see FR-1 and FR-25.**

Alex confirmed that he will be the only user initially. Multi-driver support with separate shifts is not a course MVP requirement. This narrows the audience without waiving protection of uploaded shift documents, operational identifiers or temporary summaries. Hosting exposure and the access-protection experience remain to be decided without selecting a technology stack.

> **SUPERSEDED PENDING STATUS: The recommendation was accepted. Preserve the rationale; authentication implementation is downstream work.**

Alex asked whether the tablet PIN is sufficient and requested a recommendation. For a remotely accessible website, the recommendation is one private pilot account with remembered login on his tablet, an explicit logout option and access checks protecting shift data and reports. The tablet lock protects local device access; it does not control requests to a remote website from other devices. [OWASP authorization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) recommends default-deny access and checks on every request. Remembered login requires bounded session lifetime and revocation, consistent with [OWASP session guidance](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html). This recommendation was pending at this point and was subsequently accepted below. It selects neither an authentication technology nor public registration.

> **SUPERSEDED ASSESSMENT QUESTION: Separate instructor login, fictional shift and desktop simulation were subsequently approved in FR-25.**

Alex accepted the recommended private sign-in, remembered tablet login, explicit logout and protected data access. He additionally requires the course instructor to be able to test the website in December. Alex remains the sole initial operational pilot user; instructor assessment is a separate required use case, not approval of general multi-driver support or public registration. The instructor's access arrangement, data scope and ability to test without a live bus shift remain to be agreed. No permission to expose Alex's real shift data to the instructor is inferred.

Alex approved a separate instructor test login with a fictional shift and simulated progression, enabling assessment without driving a bus or accessing his actual shift data. Demo/test status must remain explicit, and the instructor's test records must be isolated from operational pilot records. The fictional shift is to be prepared as an assessment fixture; it has not been generated during this PRD discovery. Repeatable failure scenarios and the instructor's test device/browser remain to be defined. Simulated progression is not evidence that real GPS tracking works, and simulated disruptions cannot satisfy the operational automatic-retrieval requirement.

Alex approved the ability to restart the demo shift and deliberately trigger simulated new disruption notices, internet loss and GPS loss. These controls support repeatable instructor assessment and must remain confined to the clearly labelled demo context. Restarting a demo is distinct from the prohibited resumption of a completed operational shift. Simulation demonstrates application behavior under test conditions, not actual source connectivity or the tablet's sensor performance. No additional scenario editor or general-purpose test platform is implied.

Alex requires the instructor demo to run in a browser on an ordinary PC without a tablet or physical GPS. Demonstration of progression, speed-based message locking and GPS-loss behavior must therefore work from clearly labelled simulated inputs without depending on physical location access. The instructor's exact browser is not yet specified. Desktop assessment does not replace validation of actual GPS, connectivity and interaction on Alex's Lenovo tablet with Brave.

Asked which capabilities must work to make the course MVP useful for evaluation on three actual working days, Alex identified the shift overview, stops and their associated behavior, and disruption information as the most important. These form the core evaluation priorities. He explicitly confirmed that speed-limit information and weather are optional additions after the core works and only if time permits; neither is required for course MVP acceptance.

This prioritization does not cancel previously agreed supporting requirements, including fullstack/database delivery, safe interaction behavior, reliability/fallback handling, import review and correction, active-shift recovery, or the required PDF daily-summary export. Detailed capability acceptance and feasibility gates remain to be established.

Among optional extensions, Alex prioritizes meeting-bus warnings ahead of both speed-limit information and weather, unless either of the latter proves very simple to implement. Meeting-bus warnings remain outside mandatory course MVP acceptance; this decision changes extension priority, not the core commitment. The relative order of weather versus speed-limit information is not specified. Ease of implementation does not waive data reliability or traffic-safety requirements. This explicit prioritization supersedes the brief's earlier treatment of speed-limit information as a desired first-version capability.

Alex explicitly rejected manually entered disruptions as a substitute for automatic retrieval in the course MVP: entering them himself would remove much of the project's value. Automatic retrieval is therefore an acceptance requirement and source feasibility is a delivery blocker until validated. Labelled test/demo data can exercise behavior but cannot demonstrate that this requirement works with real sources. This decision does not require any particular integration method or establish that source access is available.

> **SUPERSEDED DEADHEAD QUESTION: Limited Svipper coverage was accepted and automatic deadhead routing deferred; see PRD section 5.**

Alex selected Svipper as sufficient for the first implementation. Municipal excavation portals, county sources and Statens vegvesen are desired later integrations, with no relative priority specified. This narrows the initial source commitment without proving access or complete coverage. The implications for previously requested deadhead disruption information remain to be clarified: a single transit source must not be presented as covering every road on an inferred deadhead route.

> **SUPERSEDED ROUTING QUESTION: Automatic deadhead-route calculation was subsequently deferred.**

Alex accepted limiting initial deadhead disruption coverage to relevant Svipper notices, with a clear statement that other road events are not covered. He stressed that deadhead travel is a major reason for wanting Statens vegvesen as a later source. This is an accepted course-MVP limitation, not withdrawal of the broader deadhead-information need. It does not establish the feasibility of automatic deadhead-route calculation, which remains a separate scope question.

Alex subsequently deferred automatic deadhead-route calculation. The course MVP starts with the agreed deadhead activity and next-starting-stop display. Route calculation ranks after meeting-bus warnings and after both weather and speed-limit information. The earlier conditional exception for very simple weather/speed additions remains; no new relative order between weather and speed was specified. The previously discussed fastest suitable route preference and operating guidance are retained for the deferred capability, not imposed as a course-MVP routing requirement. Without a calculated or otherwise known route, precise road-level disruption matching must not be claimed.

## Shift Import Review and Correction

Alex wants a preview of the interpreted shift after PDF upload, asking the user to confirm that it is correct before use. If the user answers no, the user must be able to edit the misinterpreted information directly and then review and confirm the corrected shift. Alex selected direct editing for the course MVP because he considers it safer than describing an error in free text. The previously considered free-text correction alternative is not selected.

The preview is a review of extracted shift information, not an assumption that extraction succeeded. Editable fields and missing-activity handling were defined later below and in FR-2–4; validation details remain downstream work. No AI correction mechanism is required by this interaction choice.

Alex confirmed that the preview editor must also allow manual addition of an entire trip or activity omitted during PDF extraction. The resulting shift remains subject to user review and confirmation before use. Required fields, activity ordering and validation rules remain to be defined; adding a trip does not by itself establish its stop sequence or an external data-source match.

For a passenger trip, Alex identified route, starting stop, ending stop and departure time as the fields he wants to enter or edit. He hopes stored timetables can supply the remaining details and expressed a desire to load all timetables into the database. This is a desired capability and feasibility assumption, not evidence that those fields always identify a unique trip or that timetable coverage is available.

Matching must account for the shift date and applicable service calendar; planned timetable information must remain distinct from real-time observations. These questions were open at this stage. Later decisions below restrict initial coverage and define ambiguous/missing-match behavior; source validation remains B-1/B-2. This does not expand the agreed scheduled-service pilot beyond its existing boundary or select a database design. The later non-passenger activity decision below and FR-4 define these fields.

Alex clarified that his wider ambition is timetable coverage for all Tromsø city routes, but the course MVP starts with the four selected pilot lines: 20, 24, 28 and 42. Wider city coverage is deferred. This settles the initial coverage boundary, not the availability, completeness or update process of the timetable source.

Alex expects route, endpoints, departure time and day/date to identify a unique timetable trip. He considers multiple matches unlikely when the date is included, but confirmed that any multiple matches must be presented for user selection rather than silently choosing one. Uniqueness remains an expectation to validate against the actual timetable data, not a guaranteed property. Whether the date is inherited from the uploaded shift or entered separately remains a presentation detail; matching must use the relevant service date.

If no timetable match is found, Alex requires an explicit warning first that the assistant cannot find the trip. The trip may then remain in the shift overview with the user's entered information and a clear indication that stop details are missing. The assistant must not silently substitute a different trip or fabricate the missing stop sequence. A no-match result must remain distinct from an unavailable lookup source.

For activities without a timetable trip, such as meal breaks, bus changes and pilot-car driving, Alex requires activity type, start time and end time for manual entry or correction. He also approved an optional editable location field, for example a break facility or handover location. A missing optional location must not be replaced by an invented one.

History of earlier shifts is a later extension only if testing establishes an actual user need. These retention boundaries do not remove the approved fullstack and database requirement.

Alex asked whether the device accelerometer could detect movement during GPS loss. This is a feasibility candidate, not a selected implementation. [Android's motion-sensor documentation](https://developer.android.com/develop/sensors-and-location/sensors/sensors_motion) establishes that an accelerometer measures acceleration, not speed directly. Consequently, an absence of acceleration does not distinguish a stationary bus from one travelling steadily in a straight line. An accelerometer alone is not established as a reliable basis for unlocking at the 6 km/h threshold. Sensor availability and any combined estimation approach require later validation on the chosen platform; no platform or architecture is selected here. The subsequent five-minute unlocking decision does not depend on establishing accelerometer-based speed detection.


