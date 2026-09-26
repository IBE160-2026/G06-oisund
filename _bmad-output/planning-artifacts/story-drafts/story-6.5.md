---
status: approved
created: 2026-09-26
epic: E6
story: '6.5'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['6.3', '6.4', '5.7', '5.13']
---

### Story 6.5: Explicitly Switch Instructor Person or Accompaniment Block Without Transferring Trip Evidence

As an INSTRUKTØR accompanying different people or portions of their shifts,
I want to explicitly switch to a reviewed person and block, including returning to a previous person,
So that the app follows my actual accompaniment without carrying another period's trip lock, observations or completion into the new context.

**Acceptance Criteria:**

**Given** an accessible active own day with reviewed person-plan copies, resolved planned links and an actual accompaniment or neutral between-period state,
**When** the owner requests a change of accompanied person or block,
**Then** show the current person/period and proposed person/period separately, with own activity, imported plan identity/revision, service date and explicit accompanied scope sufficient to distinguish overlapping or identical-looking trips,
**And** require deliberate selection and confirmation of actual change; a next scheduled time, source response, position, completed passenger trip or available candidate cannot select a new person/block automatically,
**And** offer only valid links for the own assignment/day. A FADDER assignment cannot use this flow to switch to another person or a partial instructor scope; unresolved own-plan/link changes need explicit repair rather than automatic role conversion,
**And** reusing a previously reviewed person-plan does not require reimport, does not imply that the other person approved it and does not merge old and new periods,
**And** ambiguous/missing/overlapping links remain visibly unresolved, with cancellation preserving the current actual period and its pin; confirmed own and imported plans remain unchanged.

**Given** the owner reviews an eligible target and confirms actual accompaniment of that person and portion,
**When** the transition commits under current role/movement/access rules,
**Then** atomically close the outgoing actual tracking period if one is active and open the new period with its own context identity, person/plan/block references, reviewed revision basis, actual guiding role and ordered manual transition evidence,
**And** retain outgoing observations, manual pin history, gaps and uncertain outcomes under their original context; leaving it neither completes nor aborts the other person's unfinished passenger trip,
**And** the new period starts without inherited pin, passage/departure evidence or completion. Establish its actual trip and stop context through the existing 6.4/E3 rules rather than assuming the scheduled trip or resuming the previous visit's pin,
**And** a return A to B to A, or a change to another block for A, creates a distinct actual tracking period even when it references the same person-plan and same trip. Preserve the observed segments separately without filling the gap or counting an entire trip twice as completed,
**And** record the owner's explicit change and available timing basis separately from planned boundaries and later server receipt; it is not independent evidence of a physical handover before that recorded action,
**And** changing accompaniment does not end the own combined day, start own driving or create new app/day authority.

**Given** a change dialog, correction, gesture or asynchronous operation was opened against an earlier role/context/revision,
**When** it attempts to commit after Jeg kjører, another transition, a revision change or loss of authority,
**Then** revalidate current actual role, permitted movement state, access and exact source/target review basis at commit, using 6.4's guard; a stale action cannot switch the person, reopen locked details, acknowledge a notice or move a stop in the new context,
**And** Jeg kjører applies driver restrictions immediately even while the change dialog is open; discard/invalidate that stale guiding confirmation and require an explicit newly permitted review rather than treating it as consent to return to guiding,
**And** if the target becomes stale, disappears or becomes unresolved before commitment, leave the outgoing context unchanged except for an independently committed role/safety change. A failed proposed switch cannot roll that safety change back,
**And** legitimate previously committed events and their delayed receipts remain associated with their original context and immutable identity, without executing the user action again or reviving old permissions,
**And** source data received for an old context may be retained only within existing source/cache/expiry rules; it cannot silently retarget the active person or turn an old measurement into a new observation.

**Given** an actual switch has committed,
**When** the operational view, notices and next-activity information update,
**Then** visibly update the permitted person/block context and use the target linked plan for route, stops and trip progression, retaining the persistent actual guiding role label and the own plan as the workday sequence,
**And** do not flash the previous person's trip as the selected new trip while target selection is unresolved; show explicit pending/uncertain trip context instead,
**And** recompute notice relevance using documented target trip/date/stop identity and source evidence; context change is not a new notice receipt or a new source version and cannot replay prior sound,
**And** preserve legitimately shared notice version/seen/acknowledgement state through the established E4 identity rules, without copying unrelated notices or marking unseen content seen merely because the previous person's view showed another version,
**And** new trip establishment retains observation gaps and the existing quality limits; no A–B–A transition can claim the 100-metre goal for unobserved passages or infer completion of classroom/office work or another person's remainder.

**Given** local persistence, synchronization or restart interrupts a person/block switch,
**When** the system resumes or retries,
**Then** recover either the committed new context or the prior complete context, never a mix of the new role/person and old plan/block/pin; incomplete evidence remains restrictive/uncertain and cannot infer unrestricted guiding,
**And** use the shared IndexedDB/outbox transaction and authenticated FastAPI/PostgreSQL transition with current writer/expected revision, adding only the transition fields needed here; enforce same owner/day, assignment scope and references on the backend as well as in the UI,
**And** an unsuccessful local transaction never reports a saved switch; a lost server response leaves the locally committed result pending with unchanged batch/event IDs. Matching receipts alone establish server confirmation and duplicate delivery cannot create another period,
**And** conflicting or rejected changes preserve permitted local evidence for 5.7 review; neither a server reply nor an old tab can silently restore the former person as current, roll back Jeg kjører or switch writer authority,
**And** retain movement/outage history through switching and reload; neither a new block nor a return to A creates a new genuine-startup or five-minute exception,
**And** apply E1/E5 logout/access and AD-12 expiry/closure to every context, checkpoint, conflict copy and pending payload. Switching creates no new retention clock; own-day closure retains only actual accompanied portions and cannot resurrect the discarded remainder from old replies or tabs,
**And** private person/context data stays isolated from public demo access, logs and other accounts, with personal import details excluded from the active driving-style view.

**Given** anonymized/fictional linked plans, browser clients, controlled observations/notices and real PostgreSQL,
**When** the implementation is verified,
**Then** test actual A to B to A and A-block-1 to A-block-2, including the same trip on return, unfinished outgoing passenger trips, manual pins and an observation gap while away,
**And** test identical-looking routes/times, overnight service date, unresolved overlapping links, FADDER person-switch rejection, stale own/imported revision and cancel,
**And** begin the switch while guiding, invoke Jeg kjører in motion before save, and deliver stale confirmations/callbacks from the dialog and old view; verify the new role guard rejects now-locked effects. Contrast with a valid pre-change committed event whose later receipt only confirms its historical acceptance,
**And** test crash before/after local commit, concurrent tabs, local write failure, lost/mismatched receipt, stale writer, server conflict, logout and expiry, proving there is at most one current context with correctly partitioned historical periods,
**And** test an already received notice becoming relevant to B without new sound, legitimate same-version seen state across contexts, no falsely seen version and no copied trip completion/pin,
**And** use existing own-day closure commands to verify retained A/B accompanied evidence and removal of the unaccompanied remainder from all affected copies, including pending old-context responses. No future summary renderer is needed for these tests.

**Traceability:** UX UJ-4 extensions of FR-5/6/9/16/20 and accompanied evidence FR-22/24; shared FR-1 and E4 notice requirements. NFR-1–4; UX-DR8/14/16/19/22/26/27/28/29/30/31/36/38/39/44. EXPERIENCE FADDER and INSTRUKTØR assignment scope, Explicit tracking-context changes, Role and context recovery and accompanied-only summary scope. AD-2/4/5 atomic transition/receipts, AD-8 notice identity, AD-9 actual context/pin, AD-10/11 authority and AD-12 retention. All AD-1–AD-14 remain unchanged.

**Dependencies:** 6.3 reviewed planned links, 6.4 actual-period entry/end and commit-time role guards; shared E3/E4 operational/notice engines and E5 synchronization/conflict/closure contracts through 5.13. Tests can use already prepared A/B links and neutral between-period states. No later classroom/office execution, own-driving selector, full acute takeover/return, linked-revision repair UI or E7 summary is a prerequisite.

**Size boundary:** One explicit actual person/block transition coordinating existing period entry/end, target selection and atomic context persistence. Classroom/office execution and no-accompaniment instructor operation remain a separate slice; planned own driving, full takeover/return, linked-revision repair and full cross-device mentor recovery remain subsequent required work. No new importer, sensing or synchronization engine.

**Pilot qualification:** Controlled A–B–A browser/FastAPI/PostgreSQL cases contribute to E8-D. E8-P still requires actual device clarity, role-change races and integration across own tasks, mentoring, recovery and closure. E8-E remains field evaluation; explicit transition records do not establish outcomes during observation gaps. No implementation or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 as scoped. A–B–A uses separate actual accompaniment periods: history is preserved while trip/stop context must be established afresh on return. Atomic transition and commit-time role validation are retained. Planning approval only; the approved copy in epics.md is canonical.
