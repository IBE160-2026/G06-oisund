---
status: approved
created: 2026-09-26
epic: E7
story: '7.1'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['3.2', '3.10', '5.13', '6.10']
---

## Epic 7: Close the Day, Inspect Outcomes and Export a Summary

E7 implements explicit normal end/early abort of one combined day, the initial review of uncertain outcomes, distinct own/accompanied summary evidence, user-initiated local offline PDF and subsequent read/export-only retention until fixed expiry. FR-21–24, summary/export portions of FR-17/20 and UX-DR32–36 apply. It consumes E3/E4/E6 evidence and integrates E5/AD-12 settlement and all-copy cleanup. This first story delivers the actual terminal action and retained result boundary; detailed outcome review, complete summary, PDF and closing-message presentation remain separate stories.

### Story 7.1: Explicitly End or Abort the Combined Working Day Without Inventing Completed Work

As the pilot owner finishing or terminating my working day,
I want to confirm normal ending or early abortion and retain the permitted result even offline,
So that the day cannot resume accidentally and unfinished or uncertain work is not presented as completed.

**Acceptance Criteria:**

**Given** an accessible active own combined day,
**When** final own-depot arrival is supported or the owner needs to end without detectable arrival,
**Then** offer the red Avslutt skift action in the final-depot context and the existing Menu fallback for normal ending under the same confirmation and current interaction rules,
**And** allow normal ending through Menu when GPS/depot evidence is missing or the day ends in a valid non-driving instructor activity; absence of depot detection does not force aborted status or fabricate depot arrival,
**And** keep early termination an explicit distinct aborted choice through the same confirmation/result flow, with the chosen normal/aborted outcome unambiguous before confirmation. Do not request medical details or introduce a mandatory reason collection,
**And** identify the concrete own combined day and show relevant remaining work/parts so an intermediate depot visit, split-day gap, ended accompaniment block or other person's shift end cannot appear to end the whole day automatically,
**And** scheduled final time, current location, closed browser and final passenger-stop registration are not substitutes for explicit own-day ending. An ended/expired day cannot be a fresh end target.

**Given** the owner invokes normal end or abort,
**When** the Er du sikker? dialog is shown and confirmed or cancelled,
**Then** identify the day, normal/aborted choice and consequence that the whole day will end without resumption; explain that activity uncertainty is retained for the subsequent review,
**And** cancel leaves the day, current context, role, pin, evidence and pending work unchanged; opening the dialog creates no terminal event,
**And** recheck access, current writer/revision, actual-role/movement permission and the relevant review basis at commit. A stale dialog, independently changed role or terminal state cannot authorize an invalid close or a different outcome,
**And** use E3's actual qualified movement rules and E6's role guards: unknown recovered role uses driver restrictions until a permitted explicit clarification, while a verified actual guiding role retains only its adopted permissions. End confirmation itself cannot resolve role uncertainty or bypass logout,
**And** if motion or Jeg kjører removes permission, close/invalidate prohibited confirmation with accessible focus handling. A delayed click/response cannot complete the now-locked action; no mandatory driver response is required.

**Given** a valid explicit end/abort confirmation,
**When** the local closing transaction commits,
**Then** integrate the actual E3/E4/E6 day with 5.13's terminal protocol: atomically record the chosen terminal state and confirmed ending event, preserve the minimal allowed result/checkpoint, apply prohibited-content trimming, retire affected original payload identities and persist the closure/deletion guard before reporting local success,
**And** use the original committed end/abort time and available timing provenance consistently on retry; do not substitute planned end, GPS arrival, server receipt time or a later reopen as a new ending time,
**And** end operational continuation for the whole combined day and its active context, without rewriting a pinned unfinished trip as completed/aborted merely because the day ended. Preserve existing trip/activity outcomes and mark unresolved remaining work honestly for later review,
**And** retain own tasks/own driving, actual accompanied portions and temporary takeover evidence separately, with manual/observed/unknown provenance and gaps. Do not keep the other person's unaccompanied remainder in old revisions, outboxes or recovery copies,
**And** preserve only necessary context/revision facts for those retained outcomes; an active R1 with a newer R2/unresolved link cannot be silently merged or remapped as part of ending,
**And** a failed local transaction cannot claim successful ending or partially delete data while presenting an active day. An uncertain commit outcome requires guarded state recovery before either reattempting the same intent or allowing active operation; do not assume failure and restart a possibly ended day.

**Given** local closure succeeded online or offline,
**When** the post-end result view opens or the app restarts,
**Then** show normal-ended versus aborted status, own-day identity, committed ending time/provenance, applicable expiry and local closure versus server settlement status, with an entry into the initial post-end review area and a main-menu route,
**And** retain the permitted outcome data for subsequent E7 review/summary stories. This slice may expose the basic retained-result view without implementing full outcome editing, summary composition, PDF or affirmation selection,
**And** neither missing server acknowledgement nor unavailable summary/export functionality can resume the day, delete permitted pending work or make an ended day active through back/history navigation,
**And** do not report every trip/activity as completed because normal end was selected; missing work and uncertainty remain visible as such in the retained result boundary, with no false GPS/depot evidence,
**And** normal completion without position is recorded as the owner's explicit normal end, not a detected arrival or forced abort. Closing one combined day creates no authority or automatic start for a next prepared day.

**Given** original pending batches, receipts, source callbacks, other tabs or server settlement race with closure,
**When** the existing E5 settlement path processes the day,
**Then** use 5.13 unchanged: payload-free old-outcome lookup, new immutable closure identities, expected-revision validation and atomic PostgreSQL receipt/fence/terminal cleanup. An old-batch unknown outcome is not the new closure receipt,
**And** mark server-confirmed closure only after its matching receipt is durably recorded locally. Lost/failed replies leave a terminal local day with settlement pending; retry does not create a new end or extend its deadline,
**And** all stale-tab, old-copy and late-response writes/renders/enqueues respect terminal/deletion state, preventing resumption and prohibited-content resurrection. Local closure cannot claim that disconnected devices or all server copies were already erased,
**And** authenticated FastAPI/PostgreSQL validates owner/day, writer authority, end kind and actual permitted projection using E3/E4/E6 data, not an arbitrary client claim that fields may be retained,
**And** pending logout/revocation and conflict review remain mandatory. A locally ended day whose activation is still `Uavklart` retains local terminal evidence within TIME-01 limits but does not become server-approved through closure. If first activation acceptance missed E, reject it; a matching pre-E acceptance with lost response may be recovered by narrow status lookup. Server-approved activation does not by itself confirm closure.

**Given** the day is ended/aborted or has never been explicitly ended,
**When** retention and access deadlines are evaluated,
**Then** use TIME-01/AD-12 with earlier binding limits: server-verified actual end/abort plus seven days for verifiable ended data; for an offline ending without verifiable actual time, `D = min(Tg + 7 × 24 hours, earlier binding data deadlines)` using the immutable server issuance time of the original grant; confirmed planned final end plus seven days for never-ended data; and existing non-sliding draft rules,
**And** preserve AD-10's separate post-end authority cap at the earliest of the existing day-grant deadline, effective data deadline and any earlier applicable access cap. After E, only an already server-approved day has this bounded post-end scope; trusted time control is required before summary/export. Do not present data retention as guaranteed read/edit permission,
**And** no retry, server acceptance, review, export, reopen or device recovery resets those clocks; a never-ended expiry deletes data without declaring the day or activities completed,
**And** use existing expiry guards across client/server/recovery/conflict/receipt/grant copies even when settlement is pending. User-held exported files remain outside app deletion, but no private archive or backup is introduced,
**And** detailed initial-review permissions and later retained read/export UI remain subsequent E7 work under these boundaries, not a general post-end editing or resume capability.

**Given** the day is ended offline with a locally reported ending time whose trustworthy timing basis is not established,
**When** the client/server presents the end event or computes access and retention deadlines,
**Then** distinguish the user's locally reported time, its registration and verifiable timing evidence/status; a committed local end event or matching transport receipt alone does not make the reported clock value independently verified,
**And** uncertainty cannot extend storage or authority: enforce D from Tg and every earlier binding limit. A future-skewed client clock, later receipt or retry cannot grant extra lifetime; the post-end review/export window may be shorter than seven days or zero,
**And** keep local terminal status separate from unresolved timing/server settlement; do not resume the day while waiting, infer an exact physical end from receipt time or silently turn a local timestamp into proof,
**And** a missing, stale or unprovable Tg blocks offline start under 5.4; for an exceptional pre-existing local copy with no trustworthy anchor, keep it locked until trusted server control and apply supervised disposition without inventing D. On uncertain-time offline restart lock private views/actions/export, retain the local copy, and delete expired data before display after trusted control. A closed/unreachable tablet cannot guarantee physical deletion at D. TIME-01 is the adopted solution, not a completed implementation test.

**Given** anonymized/fictional own-only, split and mentor days, browser clients and real PostgreSQL,
**When** this terminal-action integration is verified,
**Then** test final-depot prompt, normal Menu fallback with GPS loss, no-depot instructor day, explicit early abort, cancel, intermediate depot/gap/block ending and scheduled end without automatic closure,
**And** test locked confirmation during reliable driver motion, role changing after the dialog opens, unknown role after emergency recovery and stale queued confirmation; accepted closure never bypasses the current policy,
**And** test active unfinished trip/manual pin, uncertain classroom/office work, A–B–A observations, temporary takeover and active R1/newer R2: ending preserves origins and incomplete results while trimming only prohibited imported remainder,
**And** test local failure/uncertain outcome before/after the atomic close, double confirmation, restart/history navigation, offline closure, lost/mismatched settlement receipts, concurrent/suspended tabs and delayed old batches/source replies,
**And** inspect actual IndexedDB/PostgreSQL retained copies with existing 5.13 race tests adapted to these real E6 projections, including forged trim content, old writer, pending logout, conflict and 5.4 unresolved server eligibility,
**And** test original end-time/deadline stability through retries and earlier limits, expiry while settlement is pending and never-ended deletion without false completion. Verify readable red action, explicit end kind, keyboard/dialog focus, enlarged text and clear local/server/error labels,
**And** test an offline end with forward/backward clock changes, unverifiable reported time, delayed receipt, restart and an earlier grant/data deadline; calculate D from original Tg, preserve earlier binding limits, distinguish local end/closure status from server receipts, and verify lock before any private pixel and expired deletion before view after trusted control,
**And** distinguish this story's terminal contract and basic post-end result from later summary/manual-review/PDF acceptance and real device qualification.

**Traceability:** Primary FR-21, integrated terminal portions of FR-24, offline ending/recovery FR-17/20 and preserved evidence for FR-22; shared FR-1/11/16. NFR-1–4; UX-DR7/14/17/23/31/32/33/36/38/39/41/44. EXPERIENCE end/abort confirmation, split-day and initial-versus-retained summary permissions, mentor evidence and retention; DESIGN red end action and explicit confirmation. AD-2/4/5 atomic local/backend closure and receipts, AD-9 terminal operational state, AD-10/11 authority and conflicts, AD-12 trimming/deadlines, AD-13/14 access/build recovery. All AD-1–AD-14 remain unchanged.

**Dependencies:** E3 permitted actions/non-passenger context, E4 recorded display/source evidence, E5 terminal settlement through 5.13 and actual E6 state/projections through 6.10. Existing protocol commands now receive real end UI and E6 data integration. Subsequent summary review/PDF screens are not prerequisites for explicit terminal action, protected retention and basic ended-state display.

**Size boundary:** One end-to-end normal-end/abort command and confirmation UI for the own combined day, integrating the existing settlement protocol and actual evidence projection. No second settlement engine, full summary composition, manual outcome editing, retained-summary browser, PDF rendering or closing-affirmation bank. Those are required later E7 slices; final lifecycle evidence will include them.

**Pilot qualification:** Controlled browser/FastAPI/PostgreSQL closure and fault evidence contributes to E8-D. E8-P requires mounted end-action usability, actual role/access/recovery conditions, Tg deadline, locked offline restart, supervised custody/wipe procedure and whole E7 review/export/cleanup integration before real shifts. E8-E remains field evaluation. TIME-01 resolves the policy choice; no implementation or actual tests occur during this planning update.

**Approval:** Original story approved 2026-09-26. TIME-01 adopted by the owner 2026-09-27: unverifiable offline end uses original Tg as conservative pre-end anchor and earlier binding limits; uncertain-time restart locks until trusted control, with no exact-time physical deletion claim. Planning approval only; the approved copy in epics.md is canonical.
