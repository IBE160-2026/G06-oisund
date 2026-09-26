---
status: approved
created: 2026-09-26
epic: E6
story: '6.8'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['6.4', '6.7', '3.2', '3.8', '3.9', '5.13']
---

### Story 6.8: Take Over the Current Linked Trip as FADDER and Explicitly Return to Guiding

As a FADDER who temporarily needs to drive the accompanied person's current trip,
I want to apply driver restrictions immediately while keeping the current trip context, then explicitly return to guiding when I am accompanying again,
So that a temporary actual driver change neither loses progress nor rewrites planned trip ownership.

**Acceptance Criteria:**

**Given** an accessible active own day with an actual FADDER accompaniment context and its current linked trip,
**When** the owner selects Jeg kjører for the acute current-trip takeover,
**Then** immediately show FØRER and enforce E3 driver restrictions before any persistence response, route request or additional choice, using 6.4/6.7's safety and stale-action guards,
**And** retain the same person/linked plan, accompaniment block, tracking-context identity, current trip/direction, stop progress, manual pin and notice context. A change of driver alone neither starts a new tracking context nor reinitializes progression,
**And** require no creation of a planned own trip, own-trip selection, new route match or plan revision to apply the restriction and retain current context,
**And** record this as temporary actual driving on the linked trip, distinct from 6.7's planned own-driving flow. Neither imported plan changes ownership or content, and the linked trip never appears as a newly planned own trip,
**And** this exception is the adopted FADDER current-trip case, not an implicit extension to INSTRUKTØR takeover or a general linked-trip own-driving selector. The universal immediate restriction from Jeg kjører still applies even when a takeover target is invalid or unresolved,
**And** unresolved current trip/progression remains visibly unresolved: the safety action cannot invent a trip or stop, release a manual pin or authorize an arbitrary substitute.

**Given** the acute role change is recorded or retried,
**When** its evidence and later observations are persisted,
**Then** store the actual role transition and its manual origin against the existing context, with registration time, available event-time basis and retained uncertainty, using the existing atomic local/outbox contract,
**And** distinguish a known actual takeover time from registration time; if an earlier physical takeover time is unknown, leave it unknown rather than assigning it from schedule, position or an old measurement,
**And** preserve previous guiding observations and attribute subsequent known observations to their actual role/context without relabelling the whole trip as driven by the fadder or rewriting earlier observations,
**And** repeated delivery of the same action is idempotent and does not create several takeovers. A later distinct explicit takeover after a valid return creates its own role segment within the appropriate existing context,
**And** role change alone is not evidence of GPS-confirmed movement, stop passage, passenger-trip completion, physical bus replacement or completed own work; no permanent raw GPS track is added.

**Given** FØRER is the actual role after takeover,
**When** the ongoing trip receives observations, notices or a valid operational transition,
**Then** continue the existing E3 progression, manual-pin, final-stop/return-start and missing-stop fallback rules with the retained context and actual driver interaction policy,
**And** retain qualified speed/position history, outages and uncertainty; role switching never creates a first-start exemption, restarts the five-minute interval, treats unknown speed as zero or hides an observation gap,
**And** preserve E4 source/version/seen/acknowledgement state and recompute only genuinely changed relevance. Takeover or return is not a new notice receipt and cannot replay old audio,
**And** a normal supported trip transition does not return the owner to guiding or copy the previous trip's pin into the next trip. Actual role remains FØRER until an explicit permitted return,
**And** stale guiding dialogs, gestures, validation callbacks or source replies cannot commit now-locked actions or reopen prohibited details. A receipt for a valid earlier committed action only confirms its original history.

**Given** a temporary takeover is active and the owner is now accompanying again,
**When** the owner uses Jeg sitter på igjen through the permitted Menu path,
**Then** evaluate permission using the current driver-role movement/access rules before granting any guiding exception, and require an explicit current-context return action,
**And** revalidate actual role, takeover/context identity, current trip state, revision and authority at commit; a stale dialog from another trip/context cannot return the app to guiding or restore an old trip snapshot,
**And** only after a valid local commit show active FADDER guidance/open controls and record the manual return against the same tracking context, preserving its then-current trip/direction, progression, pin and notices,
**And** a stopped bus, planned time, end of a trip, app reopen or assignment label cannot confirm that someone else is driving. Return requires the owner's explicit action, and nothing in this flow authorizes lifting restrictions while the owner is still driving,
**And** cancel, locked controls, invalid target or failed/uncertain local return storage leaves driver restrictions in force. If the return was durably committed but server acknowledgement is missing, retain its explicit local/pending status under existing offline rules rather than claiming server confirmation,
**And** if the former accompaniment context has been exited, ended or changed to another person/own activity, do not resurrect it through the old return action; use the existing explicit context-entry path with fresh validation.

**Given** takeover/return persistence fails, the app restarts or recovery presents older guiding data,
**When** the operational view is restored,
**Then** restore actual role and current context together, with a recorded unresolved takeover recovering as FØRER until a valid explicit return is established,
**And** inherit 6.7's restrictive recovery even if the role/guard write never committed: an older local/server guiding copy, absent marker, lost response or imported FADDER label cannot establish current guiding permission when the outcome is uncertain,
**And** retain driver-safe controls and clearly indicate role/storage uncertainty until permitted role resolution; do not invent saved role events, exact physical handover times or fresh sensor evidence,
**And** a late takeover/return receipt updates only the appropriate historical acceptance status and cannot roll the current role backward or replay a transition; a stale tab cannot lift restrictions by writing its older guiding state,
**And** a return committed before a crash must be distinguishable from a merely requested return; contradictory or incomplete evidence cannot be resolved by choosing the less restrictive role.

**Given** these role segments and observations are saved, synchronized, reviewed for conflict or become due for deletion,
**When** client and backend process them,
**Then** extend existing owner/day-scoped IndexedDB and authenticated FastAPI/PostgreSQL context/event contracts only with needed takeover/return fields, validating current writer, expected revision, role/context sequence and FADDER eligibility,
**And** keep immediate restrictive behavior independent of successful server storage; local failure is not saved success and only a matching receipt confirms server acceptance. Immutable retries cannot duplicate transitions or remap observations,
**And** distinguish the mentor's actual temporary driving from planned own trips and guiding portions in evidence supplied to E7, retaining manual/observed/uncertain origin and observation gaps; neither role segment asserts whole-trip completion,
**And** apply E1/E5 access/revocation and AD-12/5.13 own-day retention/closure to all copies. Preserve permitted takeover/accompanied evidence, discard the unaccompanied remainder and prevent stale-tab/delayed-response resurrection. No new clock, authority or permanent person/driver performance history is created,
**And** preserve private/demo/account separation and existing conflict review; no silent merge can convert uncertain role evidence into a confirmed return or bypass the safety guard.

**Given** anonymized/fictional FADDER fixtures, browser clients, controlled observations/source replies and real PostgreSQL,
**When** this slice is verified,
**Then** test takeover during a manually pinned linked trip with exact trip/direction/stop/context preservation, including missing stop data and an ambiguous progression state without fabricated certainty,
**And** test rejection of linked-to-own ownership conversion and INSTRUKTØR acute-takeover classification, while immediate driver restriction remains available without a valid takeover target,
**And** test permitted explicit return, return locked by reliable motion, cancelled return, stale return after context/trip change, repeated takeover/return cycles and normal trip completion without automatic guiding restoration,
**And** test local role/guard write failure before any new marker, crash before/after takeover or return commit, old guiding copies, concurrent tabs and delayed receipts. Unknown outcomes remain restrictive; a proven locally committed return remains distinct from missing server acknowledgement,
**And** test outdated guiding actions after Jeg kjører, no reset of outage/startup history, no old sound replay, retained manual pin, historical measurement age and preserved gaps,
**And** test known/unknown physical takeover time versus registration time, unchanged prior observations, wrong owner/writer, stale revision, logout, expiry and terminal trimming of permitted role segments versus unaccompanied remainder across pending copies,
**And** verify readable FØRER/FADDER and uncertainty labels with no required driver interaction while moving. Tests are controlled evidence, not proof of actual physical handover or qualified tablet behavior.

**Traceability:** UX UJ-3 explicit acute FADDER exception extending FR-6/9/16/20 and FR-22/24 evidence, shared FR-1 and E3/E4 operational requirements. NFR-1–4; UX-DR14/16/19/22/26/27/29/31/36/38/39/44. EXPERIENCE Acute FADDER takeover, Explicit tracking-context changes, Role and context recovery and accompanied-only evidence; DESIGN FØRER role treatment and preserved route/stops. AD-2/4/5 atomic state/receipts, AD-8 notice identity, AD-9 same-context actual-role transition, AD-10/11 authority and AD-12 retention. All AD-1–AD-14 remain unchanged.

**Dependencies:** 6.4 actual accompaniment and commit-time role guards, 6.7 immediate/restart-safe restrictive role state and own-driving distinction, existing E3/E4 operational engine and E5 synchronization/conflict/closure through 5.13. No future linked-revision repair, full cross-device mentor recovery or E7 report is needed to demonstrate one takeover/return cycle and its bounded evidence.

**Size boundary:** One same-context FADDER takeover/return cycle and its persistence/evidence, reusing existing engine, driver restrictions and recovery guards. No new planned trip, role model for other takeover cases, person switching, plan revision, sensing engine, generic synchronization system or summary renderer. Full cross-device role recovery remains a later integration slice; safe same-client restart is required here.

**Pilot qualification:** Controlled browser/FastAPI/PostgreSQL takeover/race/retention tests contribute to E8-D. E8-P requires actual tablet role clarity, current-context retention, permitted return controls and integrated remaining recovery/closure behavior before real use. E8-E remains field evaluation. No implementation or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 as scoped. Acute FADDER takeover retains the ongoing trip and records the driver change as a distinct manually reported event. Return requires an explicit permitted action; uncertain storage retains driver restrictions. Planning approval only; the approved copy in epics.md is canonical.
