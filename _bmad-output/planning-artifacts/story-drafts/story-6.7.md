---
status: approved
created: 2026-09-26
epic: E6
story: '6.7'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['6.4', '6.5', '6.6', '2.12', '3.4', '3.11', '3.12', '5.13']
---

### Story 6.7: Switch to Planned Own Driving Using Only My Confirmed Own Trips

As the pilot owner assigned FADDER or INSTRUKTØR work with separate own driving,
I want Jeg kjører to apply driver restrictions immediately and then select my planned own trip from my own confirmed shift,
So that my actual role and trip ownership stay correct even if selection is delayed, cancelled or fails.

**Acceptance Criteria:**

**Given** an accessible active own day in guiding, classroom/office or another permitted mentor context,
**When** the owner chooses Jeg kjører for planned own driving,
**Then** immediately apply the existing driver movement restrictions and show FØRER instead of an active guiding-role badge before any trip selection, source request or server response,
**And** collapse prohibited details and invalidate pending guiding-only actions through 6.4's commit-time role guard; selecting this action never waits for a route match before restricting interaction,
**And** persist actual-role change with its origin and available timing basis, retaining a restrictive recovery guard if persistence fails; never report the change saved when it is not,
**And** keep assignment role separate from actual driving role. This action alone selects no own trip, changes no planned ownership and proves neither actual departure nor completion of any work,
**And** retain the current trip/context/pin until a valid explicit context transition. If it belongs to the linked plan, keep that ownership clear and indicate that a planned own trip has not yet been selected; do not relabel it as own driving merely because the role changed,
**And** observations after the role change retain their actual role and current context, not a continued guiding label or retroactive allocation to a subsequently selected own trip.

**Given** driver restrictions are in force and the owner opens the planned-own-trip selector,
**When** the current E3 movement/access policy permits selection,
**Then** list only eligible trips belonging to the owner's confirmed own plan or a valid explicitly confirmed revision of it, with route/direction, service date and time sufficient to distinguish candidates,
**And** exclude linked-person trips even when route, stops and departure time match an own trip; use stable plan/trip identity and validate ownership on the backend as well as the client,
**And** never copy or offer the linked trip as a fallback when the own trip is absent. Explain the missing own trip and use the existing permitted own-plan correction/addition and confirmation path before it becomes selectable,
**And** preserve source failure versus no match and manual corrections; do not require a source match where the reviewed own trip is valid under E2's missing-data rules,
**And** when selection is locked, show a concise pending-selection status without asking the driver to resolve it while moving. Unknown speed and approved startup/GPS-loss exceptions follow the existing qualified E3 rules; the role change resets none of their history.

**Given** an exact own-plan revision and trip have been reviewed for selection,
**When** the owner confirms the choice under current role/movement/access rules,
**Then** revalidate the plan/trip, expected context/revision and writer authority at commit, then atomically exit the prior tracking/activity context and establish the selected own-trip context in driver role,
**And** preserve prior accompanied observations, pin history and uncertain own-activity outcomes under their original identities; leaving a linked trip does not complete or abort it, and leaving classroom/office does not certify work performed,
**And** initialize the own trip through existing E3 selection/progression rules without importing another context's pin, stop passage, completion or old observation as a fresh measurement,
**And** retain the explicit selection's manual provenance and applicable pin behavior. Trip selection alone is not GPS-confirmed start-stop arrival, actual departure or evidence that earlier stops were passed,
**And** use the selected own trip for stops, notices and progression while preserving the own combined-day sequence/lifecycle. Source relevance and sound follow E4; selecting a context cannot replay already received notice sound,
**And** a stale/removed trip or changed relevant revision requires a fresh review; no similar linked or own trip is substituted silently.

**Given** trip selection is cancelled, fails, remains locked or has an uncertain result,
**When** the owner returns to the operational view or reopens the app,
**Then** preserve FØRER restrictions and the last durably established context with honest pending/uncertain status; cancellation of trip selection cannot undo the preceding Jeg kjører action or restore guiding permission,
**And** a failed context transaction cannot leave a new own-plan label with an old linked pin, or discard the earlier role change; restore a complete committed context or a restrictive unresolved state,
**And** open selectors, delayed source matches, stale tabs and callbacks must recheck current role, access and target context/revision before applying an effect; they cannot select a now-invalid trip or reopen locked details,
**And** distinguish a valid pre-change committed event's later receipt from a new stale action: preserve historical event identity without replaying it into the current context,
**And** a stopped bus, scheduled mentor activity or assignment label cannot automatically return the owner to guiding. A later actual guidance entry requires the existing explicit permitted 6.4/6.5 transition, with a newly established context; same-context acute takeover/return remains the separate next slice.

**Given** Jeg kjører was requested but local role/guard storage fails, its outcome is uncertain, or the app restarts before own-trip selection is complete,
**When** controls are rendered or state is restored from any local/server copy,
**Then** keep driver restrictions until the actual role is reliably resolved through the existing permitted recovery/explicit role path; an older guiding snapshot, missing marker or a successful read of old state cannot by itself establish current guiding permission,
**And** the safety rule must work even if the write that would record the restrictive guard never commits: unresolved role/recovery validity defaults to restricted controls, not the older FADDER/INSTRUKTØR role,
**And** show the storage/role uncertainty without claiming the role event or own-trip selection was saved; retry or a late receipt cannot lift restrictions or require interaction while driving,
**And** preserve known context/evidence without inventing a successful transition, new authority, fresh measurements or an automatic return to guidance.

**Given** the own trip is selected and has incomplete data or reaches an operational boundary,
**When** the existing engine processes evidence or a permitted manual action,
**Then** use E3's qualified stop/progression, manual pin, missing-stop recovery/fallback, correction/abort/skip and final-stop/return-start rules unchanged,
**And** offline/source failure cannot fabricate stops or block the approved explicit manual outcome; retain unknown progression, historical readings and observation gaps honestly,
**And** completion of an own trip or its scheduled end cannot start another person's accompaniment, change actual role or end the combined day automatically,
**And** own trip outcomes remain distinct from accompanied-driver outcomes and temporary takeover evidence. This own-trip flow cannot convert the acute FADDER current-trip exception into planned own ownership.

**Given** role/own-trip state or evidence is stored, synchronized, recovered or deleted,
**When** browser and backend process the transition,
**Then** reuse owner/day-scoped IndexedDB and authenticated FastAPI/PostgreSQL role/context transactions, outbox identities, expected revision and writer validation, adding only the necessary transition state,
**And** keep the immediate restrictive role transition independent from successful trip selection; local failure is not success, server failure leaves committed work pending and only a matching receipt confirms server storage,
**And** immutable retries do not duplicate role events or periods; conflicts retain allowed evidence for explicit review and cannot silently restore old guiding permissions or change writer authority,
**And** recover actual role, own/linked plan identity, selected context/pin, pending selection and movement/outage history consistently. Incomplete recovery cannot infer guiding or a new startup/outage allowance,
**And** apply existing access/logout, AD-12 fixed expiry and 5.13 all-copy closure/retirement guards. No role/trip change extends authority or retention; retained own-driving facts and actual accompanied portions remain separate while unaccompanied imported remainder is removed at own-day closure,
**And** keep private plans/evidence isolated from other accounts, public demo and logs; no persistent raw GPS history or new person directory is introduced.

**Given** anonymized/fictional FADDER and INSTRUKTØR days, controlled observations/source replies, browser clients and real PostgreSQL,
**When** the slice is verified,
**Then** test transition from guiding and from classroom/office, including an instructor day with no linked plan and a FADDER day with distinct own trips,
**And** test immediate restriction in motion before any selection, old guiding actions completing late, cancelled/locked/missing own-trip choice and reload: none may restore guiding permission,
**And** test identical-looking own and linked trips, a forged linked reference, Friday 25:30 and multiple calendar-time candidates, explicit own-plan addition, changed revision and a missing-stop own trip offline,
**And** test prior unfinished linked trip and manual pin preservation without transfer, prior uncertain classroom outcome, context selection without invented departure/passage and no old notice sound replay,
**And** test local failure before/after the restrictive role transition and before/after own-context commit, concurrent tabs, delayed callbacks, lost/mismatched receipts, stale writer, logout, fixed expiry and terminal cleanup of all relevant copies,
**And** force role and restrictive-guard writes to fail or remain uncertain, terminate/restart before own-trip choice, and supply an older guiding local/server copy: verify controls remain restricted until a permitted role resolution. Include failure before any new marker is committed, delayed stale response and repeated restart,
**And** verify safe context/permission recovery and readable FØRER/pending-selection state without requiring a driver response while moving. Controlled tests do not establish mounted tablet or sensor performance.

**Traceability:** UX UJ-3/4 extensions of FR-5/6/9/16/20, shared FR-1/3 and evidence FR-22/24. NFR-1–4; UX-DR5/8/14/16/26/27/28/29/31/36/38/39/43/44. EXPERIENCE planned own-driving ownership, immediate Jeg kjører restriction, explicit tracking-context change and role recovery; DESIGN FØRER replacing the guiding badge. AD-2/4/5 atomic persistence/receipts, AD-8 notice identity, AD-9 actual-role/context invariants, AD-10/11 authority and AD-12 retention. All AD-1–AD-14 remain unchanged.

**Dependencies:** 6.4 immediate role restriction/commit-time guards, 6.5 explicit context transition, 6.6 own instructor activity state, E2 reviewed own-plan revision, E3 own-trip engine, E4 notices and E5 persistence/recovery/closure through 5.13. No future full acute takeover/return, linked-revision repair UI or E7 report is required to demonstrate this own-trip flow.

**Size boundary:** Complete the planned-own-driving role/selection transition using existing guards, selector, context engine and storage. No copied linked trips, automatic role return, acute FADDER current-trip takeover/return UI, new matching/sensing/synchronization engine, full cross-device mentor recovery or summary renderer. Immediate driver restriction survives cancellation and failed selection within this slice.

**Pilot qualification:** Controlled browser/FastAPI/PostgreSQL role/ownership/race tests contribute to E8-D. E8-P requires mounted role clarity, permitted selection, real device/source behavior and integration with subsequent takeover/recovery/closure. E8-E remains field evaluation. No implementation or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 with restrictive recovery after Jeg kjører: guiding controls stay locked despite failed/uncertain storage or restart before trip selection; keep driver restrictions until role resolution and never reopen guiding from an older copy. Planning approval only; the approved copy in epics.md is canonical.
