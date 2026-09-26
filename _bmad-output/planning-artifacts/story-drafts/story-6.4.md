---
status: approved
created: 2026-09-26
epic: E6
story: '6.4'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['6.3', '3.2', '3.4', '3.8', '3.9', '3.11', '4.8', '5.13']
---

### Story 6.4: Explicitly Start and End One Actual Accompaniment Period

As the pilot owner accompanying someone as FADDER or INSTRUKTØR,
I want to explicitly start guidance for a reviewed person and block, use that person's route context, and end my accompaniment separately,
So that the app supports the person I am actually accompanying without mistaking a planned assignment for my actual role or claiming unobserved work.

**Acceptance Criteria:**

**Given** an already active, accessible own day and a resolved planned accompaniment link from 6.3,
**When** the owner requests actual accompaniment entry,
**Then** show the intended person, assignment role, own activity, imported copy/revision and planned scope for explicit confirmation that the owner is now accompanying rather than driving,
**And** require the existing actual-role/movement policy to permit the entry action before enabling any guiding exception; selecting an assignment or requesting the entry screen cannot itself unlock driver controls,
**And** revalidate the reviewed link, both plan revisions, current own-day authority and absence of an unresolved competing actual accompaniment context before committing; stale/missing/ambiguous targets remain unresolved and cancellation preserves prior state,
**And** schedule, position, imported assignment, source update or reopening alone cannot start accompaniment. This transition does not activate a merely prepared day, issue authority or resolve 5.4's delayed-start timing risk,
**And** if entry leaves another active tracking context, preserve its observations and manual correction as history without completing/aborting its unfinished trip; explain the context change in the confirmation rather than silently replacing it.

**Given** the owner confirms permitted entry,
**When** the local transition is committed,
**Then** atomically persist actual guiding role, assignment, own activity, person/plan/revision, block and new tracking-context identity, the owner's explicit start event and the corresponding outbox event,
**And** record entry with its manual origin and available timing basis, separate from planned block time and any later server receipt; it does not prove a prior physical handover, an earlier unrecorded start or GPS-confirmed passage,
**And** initialize trip/progression state only for this context, with no inherited manual pin or completion evidence from another block/person or an earlier visit to this person,
**And** a failed local commit does not show guidance as active or unlock controls; a lost server response leaves a valid locally committed entry explicitly pending, with stable retry identity and no duplicate period,
**And** the imported plan remains a mentor-reviewed copy, not approval by the other person, own planned driving or access to their account.

**Given** one actual accompaniment context is active,
**When** the operational view and controls render,
**Then** display persistent FADDER or INSTRUKTØR role text that clearly identifies guiding, and expose Menu, trip/stop choice, notice details and acknowledgement while guiding despite vehicle movement or qualified GPS loss,
**And** use the same E3 state machine and E4 source/notice rules with the selected linked plan as route/stop/notice/trip context; own plan still governs own activities and final day end,
**And** keep required route/destination, stop emphasis, uncertainty and source provenance; personal imported details stay out of the active driving-style view, while permitted context details clearly identify the selected person and block,
**And** provide the immediate safety effect of Jeg kjører: apply driver restrictions and collapse prohibited details before any subsequent plan choice, preserving current trip/context/pin. Persist the actual-role change or retain a restrictive recovery state if persistence fails; do not leave guiding controls enabled after the owner says they are driving,
**And** actual role, not assignment label, controls permissions. Full planned-own-driving selection and acute-takeover/return workflows remain separate later stories; this slice's common role guard must work without them.

**Given** a guiding-only action or detail view was opened before Jeg kjører changed the actual role,
**When** an action attempts to commit or a delayed callback/response attempts to apply its user effect,
**Then** recheck the current actual role, movement policy, access and target context at the guarded mutation boundary, not only when the view was opened; reject an action now locked and explain that the role changed,
**And** close/cancel prohibited detail and pending gestures; an old view, queued click, asynchronous validation or source response cannot perform a newly prohibited correction, acknowledgement or context change, reopen locked detail or mark undisplayed content seen,
**And** reuse ordered role/context state and backend transition validation; never authorize a new action from a stale guiding flag supplied by the client,
**And** distinguish a new delayed action from later synchronization/receipt of an action already validly committed before the role change: preserve the latter's original context and immutable identity as history without replaying it into the current view or granting permission again. Ordinary permitted source refresh is not itself a guiding action.

**Given** actual trip or stop context must be established or changes within the same accompanied plan,
**When** the shared operational engine evaluates qualified evidence or an explicit permitted correction,
**Then** apply E3 candidate, pin, service-date, stop-occurrence, final-stop and return-trip rules within the selected person-plan and current tracking context; no arbitrary trip is selected when candidates are ambiguous,
**And** keep guidance role and unresolved-trip status distinct so the owner can explicitly select a trip from the appropriate reviewed linked plan; route/time similarity cannot choose another person's or an own-plan trip,
**And** on missing stop data attempt supported recovery when available, otherwise retain known facts and missing-stop status with manual outcomes under existing rules; offline/source failure cannot invent stops or block the permitted manual fallback,
**And** preserve manual correction origin, qualified sensing history and observation gaps. Entering midway or finding a later stop cannot certify earlier passages, the whole trip or the 100-metre target for unobserved portions,
**And** retain notice source/version/seen/acknowledgement and sound semantics: a context selection or previously received notice becoming relevant is not a new receipt and cannot replay old sound; seen requires that exact version's content to be displayed with valid access,
**And** a scheduled block boundary cannot switch person, end guidance or release a pin while actual context is unchanged. An unresolved mismatch between actual accompaniment and planned scope must be visible, without manufacturing a plan revision or trimming observed facts to make the schedule appear correct.

**Given** this actual accompaniment period is ongoing,
**When** the owner explicitly ends accompaniment through the permitted action,
**Then** close only that actual period/tracking context and record the explicit end with its origin; preserve bounded observations, gaps, manual corrections and uncertainty for the accompanied portion,
**And** ending accompaniment does not complete or abort the other person's unfinished passenger trip, assert that all planned scope was accompanied, finish the owner's combined day, or choose the next person/activity automatically,
**And** remove the active guiding exception and show a neutral next-activity/uncertain state governed by driver-safe interaction restrictions, without claiming that the owner has begun driving,
**And** do not infer actual ending from planned time, end of the imported person's shift or lost position/network. A retry/reload cannot create another ending event or restart the ended period,
**And** cancellation preserves the current period. Local failure must not claim that the end was saved; any immediate withdrawal of guiding permission remains restrictive rather than silently re-enabling it on recovery.

**Given** the active or ended period is saved, reopened, synchronized or subject to deletion,
**When** browser and backend process it,
**Then** extend existing owner/day-scoped IndexedDB and authenticated FastAPI/PostgreSQL contracts only with required actual-period/context fields and evidence; validate link, revision, writer authority and transition legality on both sides,
**And** reopen this same period with actual role, person/plan/block/context and pin together. Restored measurements remain historical and interrupted observation remains a gap; incomplete recovery cannot infer guiding from the assignment or start a new startup/GPS-loss exception,
**And** retain separate local/pending/server-confirmed status, immutable retries, conflict review and E1/E5 access/revocation guards; no denied or obsolete writer can create a valid operational transition,
**And** expose accompanied evidence with explicit manual/observed/unknown provenance for later E7 consumption, separating it from own work and retaining no inferred results for the other person's unaccompanied remainder,
**And** integrate evidence with existing AD-12/5.13 own-day closure, trimming and all-copy expiry now: retain only permitted accompanied facts, discard unused imported context, prevent stale-tab/response resurrection and preserve original deadlines; no independent period/person retention clock,
**And** keep private operational state isolated from public fictional demo data and prevent personal payloads or permanent GPS tracks from entering logs. Cross-device mentor recovery and all later role transitions remain separate integration slices.

**Given** anonymized/fictional FADDER and INSTRUKTØR plans, controlled source/sensor inputs, browser clients and real PostgreSQL,
**When** this slice is verified,
**Then** test explicit entry/end, no entry from schedule/reopen/position, rejected stale/ambiguous link and cancellation, and start controls locked in actual driver motion before guiding is confirmed,
**And** test visible guiding role with open controls in motion/GPS loss, immediate driver restriction when Jeg kjører is requested, local failure during role change, and no assignment-based permission restoration,
**And** begin trip/stop correction, notice acknowledgement and detail loading while guiding, select Jeg kjører while moving, then complete them from a stale view/delayed callback: assert no now-locked mutation, detail reopening or false seen marker. Also test the opposite ordering, with a valid pre-change committed event receiving its delayed receipt without replay,
**And** test entry midway, ambiguous linked trips, missing stop data offline, repeated stop occurrences, manual pin, observation gap and same-stop return-start rules through the reused engines,
**And** test an old notice becoming relevant without sound, exact-version content display, separate source/receipt status, preservation of valid existing seen state, no falsely marked seen version and no copied completion/pin state,
**And** test ending before a passenger trip finishes, planned end passing while guidance continues, saved/reopened actual context, no automatic next-person choice, local failure, lost receipt, stale writer, logout and fixed expiry,
**And** test terminal trimming with accompanied evidence plus an unaccompanied remainder, including pending batches and stale tab/delayed replies. Controlled fixtures do not establish real source/sensor or tablet performance.

**Traceability:** UX UJ-3/4 extensions of FR-6–11/16/20 and bounded FR-22/24 evidence, shared FR-1 and source FR-12–15/19 through E4. NFR-1–4; UX-DR10–23/26–29/31/36/38/39/44. EXPERIENCE Operational role and plan states, FADDER and INSTRUKTØR assignment scope, Explicit tracking-context changes and Accompanied-person imports and summary scope; DESIGN persistent role badge and driving focus. AD-2/3/4/5 storage and shared engine, AD-7/8 source and driver state, AD-9 actual role/context, AD-10/11 authority and AD-12 evidence/retention. All AD-1–AD-14 remain binding; remaining transitions/recovery/output are not claimed complete here.

**Dependencies:** 6.3 resolved planned link and 6.1–6.2 reviewed plans; implemented E3 operational/movement engine, E4 notices and E5 same-client recovery, synchronization and terminal guards through 5.13. Requires no later multi-person switching, classroom/office execution, own-driving selector, full acute takeover/return or E7 report UI to demonstrate one actual period and its bounded evidence.

**Size boundary:** One continuous accompaniment period with entry, shared operational view, explicit end and minimal safe role/context/evidence persistence. Reuse existing sensing, trip progression, notices, access and storage engines. Multi-block/person orchestration, classroom/office execution, complete own-driving/acute-takeover flows, linked-revision repair and full cross-device mentor recovery remain separate stories. Immediate driver restriction and same-period safe recovery cannot be deferred.

**Pilot qualification:** Controlled browser/FastAPI/PostgreSQL behavior contributes to E8-D. E8-P must qualify actual mounted role readability, control access, person/trip context, source/sensor behavior and integrated remaining E6 transitions/recovery before real mentoring use. E8-E remains field evaluation; manual entry/end alone cannot establish that the whole planned shift was observed or that progression targets were met. No actual tests or implementation are performed during planning.

**Approval:** Approved by the owner on 2026-09-26 with commit-time role revalidation: after Jeg kjører, started guiding actions must be checked against the new role when saved; delayed responses and open views cannot complete an action that is now locked. Planning approval only; the approved copy in epics.md is canonical.
