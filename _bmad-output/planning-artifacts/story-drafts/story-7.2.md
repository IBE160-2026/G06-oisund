---
status: approved
created: 2026-09-26
epic: E7
story: '7.2'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['7.1', '3.10', '5.7', '5.13', '6.10']
---

### Story 7.2: Manually Confirm Uncertain Activities During the Initial Post-End Review

As the pilot owner reviewing an ended or aborted day,
I want to inspect uncertain activity outcomes and explicitly confirm only what I can attest to during the initial review,
So that the retained result reflects my manual confirmation without pretending that it was observed automatically or reopening the day.

**Acceptance Criteria:**

**Given** the combined own day has been locally ended/aborted through 7.1 and bounded access permits the initial post-end review,
**When** the initial review opens,
**Then** identify the ended day and show eligible uncertain activities with known planned facts, relevant retained observations/corrections and the reason completion remains uncertain, without mixing planned, observed, manual or unknown status,
**And** distinguish own activities/own driving, actually accompanied portions and temporary takeover evidence using retained identities and revisions; the reviewed person-plan is still the mentor's copy, not the other person's attestation,
**And** show end status, local/server status and applicable retention/access limits, including unresolved end-time provenance from 7.1; the review remains possible offline only within existing authority and retained-data rules,
**And** never require confirmation of all uncertain entries to leave the review. Unselected or unanswered entries stay uncertain, including an interrupted or skipped activity that cannot legitimately be counted complete,
**And** this is an outcome-review list using the retained result, not yet the complete daily summary, notice-history composition, PDF or closing-affirmation renderer.

**Given** an eligible uncertain activity is shown and the owner can attest to its completion,
**When** the owner explicitly confirms that particular reviewed outcome,
**Then** record a manual confirmation against its stable own-day/activity/context identity and exact reviewed evidence basis, preserving the prior uncertain state and its supporting facts as provenance,
**And** present the resulting status as manually confirmed, not GPS-confirmed, source-verified or confirmed by the accompanied person; no location/stop/source measurement is manufactured,
**And** preserve confirmation registration time and any known actual occurrence time separately; an unknown actual start/end remains unknown and is not copied from planned time or the time of clicking confirmation,
**And** confirmation concerns only the eligible retained outcome. It cannot rewrite skipped/aborted work, create a passenger final-stop arrival, certify the whole of a partially observed trip, change physical bus/person attribution by guessing or add the other person's deleted/unaccompanied remainder,
**And** passenger-trip completion still follows the adopted registered-final-stop/abort rules. This slice does not introduce an arbitrary mark-everything-complete control or post-end operational stop correction,
**And** missing optional timing/location does not force invented values; leaving the entry uncertain remains a valid explicit choice with no penalty or score.

**Given** a review confirmation is attempted or cancelled,
**When** the guarded local mutation runs,
**Then** validate the exact retained outcome/evidence revision, initial-review-open state, current writer/day authority, current interaction permission and expiry before atomically saving the manual event/result and its outbox record,
**And** if a relevant correction, recovered old-device item, context basis or review phase changes while the entry is open, invalidate the stale confirmation and require review again; do not silently apply it to a newer or different outcome,
**And** cancellation leaves that entry unchanged; a failed local save never shows it confirmed. Double-click/retry of the same confirmation has one effect and a matching receipt alone establishes server confirmation,
**And** unknown actual role retains driver restrictions under 6.10, and a delayed dialog cannot bypass a newly applicable restriction. A terminal day or a review screen does not itself prove standstill or resolve role uncertainty,
**And** do not alter terminal normal/aborted status, final end time, original plan, active-trip history or any deadline. No confirmation restarts operations, creates a new active day or changes an unknown reported end time into verified timing evidence.

**Given** manual confirmation is saved while closure settlement is pending or its receipt is lost,
**When** local recovery or synchronization processes review events,
**Then** preserve them as separate bounded post-end correction events using the existing 5.13/AD-5 protocol and immutable identities; never mutate an in-flight closure checkpoint/batch payload or revive retired original events,
**And** submit/apply them only in a valid ordered terminal-review sequence under current authorization/revision, retaining local/pending/unresolved status if the server cannot yet accept the closing basis,
**And** FastAPI/PostgreSQL validates that each field/outcome change is allowed during initial review and preserves the distinction between old receipt outcome, closure receipt and review-confirmation receipt,
**And** server rejection/conflict or unknown acceptance preserves only permitted local work for explicit resolution, without silently rewriting a confirmed fact, backdating an event to gain authority or using a client timestamp alone to bypass an expired scope,
**And** 5.4 activation timing and 7.1 unverifiable ending time remain separate open evidence/decision issues. Review cannot establish their missing proof or extend the earliest applicable deadline.

**Given** the initial review remains open and the owner requests to finish it,
**When** the app presents the finish-review confirmation,
**Then** show which activities still have uncertain outcomes and explain that confirming closes editing while those outcomes remain uncertain; do not require the owner to attest to them,
**And** only an explicit confirmation against the current review revision closes the phase. Cancel, Back, accidental navigation, tab closure or a crash alone never consumes the opportunity to continue review,
**And** if outcomes or the review basis change while the confirmation is open, refresh the remaining-uncertainty list and require confirmation again; an unseen newer revision cannot be closed using an older dialog,
**And** on permitted confirmation, atomically persist closed-for-new-edits state and invalidate outstanding edit capabilities. Later retained-summary access is read/export-only; older open snapshots, tabs, back/history navigation and delayed responses cannot reopen editing,
**And** an edit not validly committed before explicit closure cannot save afterward; committed review events may still synchronize under their original ordered basis without granting new edit permission,
**And** before explicit completion, interrupted review can resume from the durable current open phase within existing access and retention limits, including after Back, menu navigation, tab closure or restart. No operational day is resumed and no deadline is extended,
**And** if an explicit completion save fails definitively, preserve the open phase and explain the failure; if its commit outcome is unknown, restrict editing while the phase is resolved against authoritative durable state. Recover open review when no closure committed, and read-only access when closure did commit. Neither navigation nor an uncertain result alone establishes permanent closure or permission to edit,
**And** preserve permitted pending confirmations throughout recovery. The complete closing presentation and retained-summary browser remain later E7 slices.

**Given** retained review state/confirmations are stored, recovered or expire,
**When** client and backend process them,
**Then** extend existing owner/day-scoped IndexedDB and authenticated FastAPI/PostgreSQL result/event contracts only with necessary review-phase and manual-confirmation data; coordinate tabs and enforce monotonic closed-review state, writer/revision validation and allowed post-end changes,
**And** preserve manual origin, original evidence/context revision, timing uncertainty and distinct local/server status across offline restart, conflict handling and compatible builds, without carrying one activity's confirmation to another,
**And** apply current access/logout and AD-10/12/7.1 deadline rules to result, pending corrections, review metadata, conflicts and receipts. Locally reported uncertain time cannot renew authority or retention; the earliest applicable limit is enforced while timing remains unresolved,
**And** expiry still deletes permitted retained work even if a confirmation never obtained a receipt; review-open status cannot pause cleanup. Existing terminal/deletion guards prevent old tabs, intake or replies restoring prohibited content,
**And** no private source file, deleted linked remainder, extra raw movement archive, driver rating or cross-account editing capability is introduced. Demo/public access remains isolated.

**Given** anonymized/fictional ended and aborted own/mentor days, browser clients and real PostgreSQL,
**When** this slice is verified,
**Then** test uncertain break/deadhead/bus-change/office/classroom outcomes with missing evidence, individual manual confirmation and leaving entries uncertain without inventing occurrence times,
**And** test normal end versus aborted day, partial accompanied periods, takeover segments, active-old/latest-new revision provenance and rejected attempts to confirm unaccompanied remainder, rewrite skipped/aborted work or fabricate final-stop arrival,
**And** test cancellation, stale evidence during review, current-role restriction, failed local save, duplicate confirmation, lost/mismatched review receipt, closure still pending, wrong owner/writer and explicit conflict handling,
**And** test the finish dialog listing remaining uncertain activities, cancellation and an outcome/revision change requiring refreshed confirmation. Explicitly finish with pending saved events, then try Back, another tab, restart, stale edits and late replies: new edits stay barred while committed events retain their synchronization status,
**And** separately test Back, accidental navigation, main-menu navigation, tab closure and crash before explicit completion: review remains resumable within authority/expiry. Test definitive completion-save failure and lost commit outcome resolved both as open and as closed, including concurrent tabs; never infer closure just from leaving a screen,
**And** test offline review, pending logout, original/earlier expiry and forward-skewed unverifiable ending time without extended permission,
**And** inspect IndexedDB/PostgreSQL to verify immutable closure payloads, allowed post-end event ordering, retained manual provenance and all-copy cleanup; test readable uncertainty/manual labels, keyboard/dialog focus and no forced confirmation. No complete PDF/summary renderer is needed for these cases.

**Traceability:** Manual uncertain-outcome portion of FR-22, bounded post-end FR-1/17/20/24 and preserved FR-21 terminal status. NFR-1–4; UX-DR14/17/23/31/32/33/36/38/39/41/44. Owner clarification of 2026-09-26 supersedes navigation-as-closure wording in EXPERIENCE: only explicit finish confirmation closes editing. EXPERIENCE Initial and retained summary permissions, activity completion uncertainty, mentor accompanied-only evidence and retention; DESIGN distinct outcomes/manual origin. AD-2/4/5 atomic local/server events, AD-9 no operational resumption, AD-10 bounded review authority, AD-11 explicit conflicts, AD-12 retained projection/expiry and AD-14 compatible review state. All AD-1–AD-14 remain unchanged.

**Dependencies:** 7.1 real terminal result and time-provenance guards, E3/E6 outcome evidence through 6.10 and E5 post-end settlement/conflict contracts through 5.13. The review list, per-outcome confirmation and explicitly confirmed review-completion boundary work without later complete summary/PDF/closing screens; a minimal main-menu/closing entry is sufficient.

**Size boundary:** Initial-review outcome list, explicit individual uncertain-activity confirmation, bounded persistence and durable explicit-completion-to-read-only boundary. No generic post-end editor, passenger stop reconstruction, new proof of physical events, full daily-summary composition, PDF, affirmation bank or permanent archive. Detailed retained-summary navigation remains later, but it cannot reopen editing established closed here.

**Pilot qualification:** Controlled browser/FastAPI/PostgreSQL review/explicit-completion/receipt cases contribute to E8-D. E8-P requires mounted review usability, actual role/access behavior and full end/review/export/expiry integration. E8-E remains field evaluation. Manual attestation is not independent evidence of physical completion; role uncertainty and 5.4/7.1 timing issues remain test/decision points. No implementation or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 with explicit review completion required after showing remaining uncertain activities. Back, accidental navigation, tab closure or crash alone cannot consume review continuation; phase recovery preserves access/expiry limits. Planning approval only; the approved copy in epics.md is canonical.
