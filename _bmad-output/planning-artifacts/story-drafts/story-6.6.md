---
status: approved
created: 2026-09-26
epic: E6
story: '6.6'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['6.1', '6.4', '6.5', '3.10', '5.13']
---

### Story 6.6: Follow Classroom and Office Activities in My Own Instructor Day

As an INSTRUKTØR with classroom teaching or office work,
I want to follow my current and next own activity before, between or after accompaniment periods, including a day without accompaniment,
So that my own work remains usable and distinct from passenger-trip progression and the other person's outcomes.

**Acceptance Criteria:**

**Given** an accessible active own day with reviewed INSTRUKTØR classroom/office activities from 6.1,
**When** the owner views or explicitly selects one of those activities under the existing interaction policy,
**Then** show the current own activity, its type, known planned times/place and next known own activity with clear unknowns, the persistent clock and accessible Menu,
**And** retain service date, overnight ordering and each work part's reporting/depot context; a split-day gap remains a gap without inferring rest, transfer or completion,
**And** distinguish the planned sequence/preview from an explicitly selected actual activity context: passing a scheduled boundary cannot by itself replace active accompaniment, release a trip pin or declare classroom/office work started or performed,
**And** an instructor day containing only classroom/office activities works without importing another person's plan, selecting a fictitious person or showing a false missing-accompaniment error,
**And** classroom/office remains an own-plan activity, not a FADDER activity or a trip copied from another person's plan; unknown activity codes still require the existing review/correction flow.

**Given** an actual accompaniment period is active and the owner selects an eligible own classroom/office activity,
**When** the explicit context change is confirmed and committed,
**Then** atomically end the outgoing accompaniment context and select the own activity, preserving the outgoing observed portion, pin history, manual corrections and uncertain outcomes under their original context,
**And** this change neither completes nor aborts the other person's unfinished passenger trip, rewrites either confirmed plan nor ends the owner's combined day,
**And** remove active linked trip/stop progression and the guiding exception from the classroom/office context without deleting the still-needed imported plan or claiming that the owner has started driving,
**And** show the assignment and current activity clearly, for example INSTRUKTØR with Klasserom or Kontor, without presenting the assignment label as permission for unrestricted guiding controls,
**And** if review is cancelled or its target/revision becomes invalid before commit, preserve the prior complete context except for an independently committed safety/role change; do not partly end accompaniment and partly retain its active trip.

**Given** classroom or office is the current activity,
**When** the screen is displayed or observations and delayed responses arrive,
**Then** show own activity information without an active passenger trip, stop rail, stop-passage progression, fictitious accompanied person or passenger-trip completion,
**And** retained imported plans and prior trip evidence remain historical/prepared context, not active work; late callbacks from an exited linked context cannot advance it as if still accompanied or replace the current own activity,
**And** apply existing notice relevance, metadata and access rules where applicable to known own activity facts, preserving uncertainty instead of borrowing the former person's trip relevance. This state is not an ongoing actual trip and cannot trigger the 4.8 new-notice trip chime,
**And** preserve legitimate source/notice history and silent updates without fabricating a new notice/version, seen marker or sound from the context change,
**And** use the established current-role/movement guards for interactive actions; classroom/office is not a new movement exception. Jeg kjører still imposes driver restrictions immediately, and pending actions recheck role/access/context at commit as required by 6.4.

**Given** activity selection, elapsed time, position or transition to another activity supplies evidence,
**When** a classroom/office outcome is stored or displayed,
**Then** distinguish planned start/end, recorded context selection/change, known movement/location observations and any independently supported outcome, retaining each origin and uncertainty,
**And** neither being near a classroom/office, elapsed scheduled duration, choosing the activity nor leaving it alone proves that teaching or office work was completed; without outcome-specific evidence retain Gjennomføring usikker for the later E7 initial review,
**And** do not backfill a missing actual start/end from scheduled times or registration time; preserve a known actual event time separately from when it was recorded, and leave unknown actual times unknown,
**And** keep these own-activity outcomes separate from accompanied-driver trip completion, own planned driving and temporary takeovers in the evidence supplied to E7,
**And** this story supplies the activity view and honest evidence, not a new automatic completion rule, summary confirmation screen, attendance record, teaching assessment or payroll calculation.

**Given** the next own activity is another classroom/office task or a planned accompaniment block,
**When** the owner deliberately moves to the next appropriate context,
**Then** changing own tasks preserves the previous uncertain result rather than treating selection of the next task as completion,
**And** actual accompaniment entry reuses 6.4/6.5 with explicit person/portion confirmation and current link/revision validation; a return to the same person establishes trip/stop context afresh without inheriting its earlier pin or filling the classroom/office observation gap,
**And** missing or ambiguous next context stays visible and unresolved instead of selecting the nearest timetable match. An invalid next link cannot erase the current own activity or earlier evidence,
**And** if the next planned activity is own driving, identify it as an own-plan activity without automatically starting it; the full own-driving selection flow remains a subsequent story while the immediate Jeg kjører safety guard already applies,
**And** no next activity or reaching the final classroom/office planned end automatically closes the working day. Final own-day end/abort remains E7's explicit flow.

**Given** own activity state or its evidence is saved, synchronized, reopened or due for deletion,
**When** browser and backend process it,
**Then** extend existing own activity/context fields only as needed in owner/day-scoped IndexedDB and authenticated FastAPI/PostgreSQL, reusing atomic context/outbox transitions and validating plan identity, role, expected revision and current writer authority,
**And** local failure cannot report a successful transition; only a matching receipt confirms server storage. Immutable retries cannot duplicate selections or manufacture outcomes, and conflicts preserve local evidence for explicit review,
**And** recover the complete saved own context with pending status/uncertainty and no restored linked passenger progress; absent/corrupt context cannot infer guiding, fresh measurements or a new startup/GPS-loss exception,
**And** cached own activities remain usable offline under existing access rules, including a no-accompaniment instructor day. Missing optional location/source data stays unknown; this story neither starts a prepared day after ordinary expiry nor resolves 5.4's timing-evidence issue,
**And** apply logout/pending-revocation locks and AD-12 expiry/5.13 terminal guards to every private copy. Activity changes/reopen cannot renew retention, day authority or resurrect discarded linked data; preserve permitted own facts and actual accompanied evidence for the existing closure command,
**And** do not add permanent staff/student records, raw GPS tracks or private operational data in public demo access/logs. The own combined-day lifecycle continues to govern both own tasks and imported context.

**Given** anonymized/fictional plans, browser clients, controlled position/time/source inputs and real PostgreSQL,
**When** the slice is verified,
**Then** test a classroom/office-only instructor day with no linked plan, classroom before accompaniment, office between A and B, and classroom after the final accompaniment period,
**And** test departure from an unfinished accompanied trip, return to A after office with no inherited pin and a visible observation gap, two consecutive own tasks and an absent/ambiguous next activity,
**And** test schedule-only, location-only and combined location/time evidence without proof of teaching/work: each remains unconfirmed; choosing/leaving the activity cannot certify its outcome or invent actual times,
**And** test unknown location, overnight service date, split-day gap, FADDER classroom/office rejection and final planned activity ending without own-day closure,
**And** test current-role revalidation after Jeg kjører, stale linked callbacks, target revision changes, cancelled transition, crash before/after commit, offline reopen, failed local write, lost/mismatched receipt, wrong owner/writer, logout and fixed expiry,
**And** test readable activity/next-activity hierarchy, clock/Menu, long labels, enlarged text, keyboard focus and explicit unknown/disabled states; no precise gesture or action while driving is required,
**And** verify through existing closure fixtures that own uncertain outcomes and actual accompanied portions stay distinct while unaccompanied imported remainder is deleted from all affected copies. No E7 renderer is needed to verify this contract.

**Traceability:** UX UJ-4 extensions of FR-4/5/10/20 and evidence FR-22/24; shared FR-1/16/17. NFR-1–4; UX-DR7/12/14/17/18/26/27/28/29/31/36/38/39/44. EXPERIENCE classroom/office and no-accompaniment instructor states, explicit context changes and own-versus-accompanied outcome boundaries; DESIGN own activity hierarchy and role text. AD-2/4/5 atomic persistence/receipts, AD-8 notice state, AD-9 explicit context and honest non-passenger evidence, AD-10/11 authority and AD-12 retention. All AD-1–AD-14 remain unchanged.

**Dependencies:** 6.1 own instructor assignment, 6.4 actual accompaniment entry/end and commit-time role guards, 6.5 context switching, 3.10 non-passenger display/evidence and E5 access/recovery/closure through 5.13. A classroom/office-only day can be demonstrated without any linked plan. Later own-driving/takeover flows and E7 review/PDF are not prerequisites for this slice.

**Size boundary:** Adapt the existing own-activity display/state to classroom/office and integrate explicit context changes with existing accompaniment periods. Reuse the established engines; no new scheduler, completion inference, teaching/attendance administration, full own-driving selector, takeover/return flow, general linked-revision repair, full cross-device mentor recovery or summary renderer.

**Pilot qualification:** Controlled browser/FastAPI/PostgreSQL activity/evidence cases contribute to E8-D. E8-P requires actual tablet readability, representative instructor sequences and integrated role/context/recovery/closure behavior; location/time cannot qualify unobserved teaching/work as completed. E8-E remains field evaluation. No implementation or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 as scoped. Classroom and office are own instructor activities; context change documents neither completed work nor outcomes on the other person's trip. Planning approval only; the approved copy in epics.md is canonical.
