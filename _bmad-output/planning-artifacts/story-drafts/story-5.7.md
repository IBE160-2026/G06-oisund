---
status: approved
created: 2026-09-26
epic: E5
story: '5.7'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.6', '5.4', '1.4', '2.12', '3.13', '4.8']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

This slice provides explicit review of retained E1–E4 operational conflicts against verified server state and applies selected valid corrections under current authority. It reuses feature-specific validation and immutable receipts. Planned/emergency writer transfer and transport of work between devices remain separate stories; terminal/mentor reconciliation is extended with E6/E7.

### Story 5.7: Review Conflicting Local Work Before Applying or Discarding It

As the pilot owner,
I want to compare preserved local changes with the server's accepted state and explicitly choose their outcome,
So that reconnecting cannot silently overwrite my work or apply an obsolete device's changes as current authority.

**Acceptance Criteria:**

**Given** 5.6 detects an operational revision/writer conflict or unexplained server-state change,
**When** the conflict is retained for review,
**Then** stop affected automatic submission, preserving the local committed state, immutable pending events/batches and the accepted baseline/revision known to this client within their original expiry,
**And** distinguish confirmed conflict, unknown submission outcome, rejected payload and lost writer authority; do not present every failure as a choice between two equally confirmed versions,
**And** create only the minimal conflict/review references needed to avoid overwriting the surviving work, not a permanent duplicate archive,
**And** show a concise review-needed status without opening a comparison or demanding driver action while moving; local operations remain subject to actual access/writer restrictions.

**Given** a batch may already have committed but its response was lost,
**When** review obtains the authorized server state and receipt/status information,
**Then** establish the known batch outcome before proposing its effects as new corrections; an existing valid matching receipt acknowledges only its original accepted events,
**And** authorized receipt retrieval is read-only and does not require the original writer epoch to remain current, but still requires valid owner/day scope and unexpired data,
**And** a timeout, failed lookup or simple absence of a receipt while an original request may still commit is not proof of rejection or permission to duplicate/discard its effects,
**And** leave unresolved outcomes visibly unresolved and preserve pending identities; never mint a replacement batch merely to escape a lost receipt,
**And** source generations, retrieval timestamps and client clock order are not evidence of an operational server revision or a winner.

**Given** authorized access to a coherent accepted server state and identifiable retained local changes,
**When** the owner opens review under the existing movement policy,
**Then** show the compared day/plan, server revision and last server-received time, retained local change origins, receipt status and relevant original deadlines in understandable terms,
**And** compare the current server result with local intended changes and the known baseline where available; missing baseline/facts remain unknown rather than reconstructed by guessing,
**And** persist the exact comparison inputs, local change-set identity and server revision with the review selections so reopening does not silently compare a different basis,
**And** permit explicit choices to retain a valid local correction for application, keep the server result/discard the identified local proposal, or leave an item unresolved; no preselected bulk winner or last-write-wins merge,
**And** show dependent items as a coherent group where independent selection would violate plan/context/event invariants, and explain what the chosen result will change before confirmation,
**And** cancel/close preserves saved review choices without applying them. Keyboard focus and touch controls follow the existing accessible review and movement restrictions.

**Given** proposed corrections affect existing own-day operations,
**When** a selected result is validated,
**Then** use the same domain rules as its existing feature and preserve original evidence separately from the new manual correction: actual/manual/uncertain origin does not become GPS or source evidence,
**And** distinguish actual bus-change time from registration time, unknown times from supplied times, exact stop occurrence from stop name, and skipped/interrupted work from completed work,
**And** retain source notice facts and exact-version seen/registered/hidden meanings; a review choice cannot create a source-confirmed ending, mark unseen content seen or replay an old sound,
**And** preserve confirmed plan scope, service date, activity order, manual trip pin and recorded outcomes unless an explicit valid domain action authorizes the particular change,
**And** a required plan revision uses the existing E2 comparison/confirmation rules rather than accepting a whole conflicting plan as an unrestricted overwrite,
**And** unsupported/dependent corrections stay unresolved with a reason; do not loosen movement, access, terminal or data-quality rules to make a conflict disappear.

**Given** the owner confirms selected valid corrections while holding current write authority,
**When** the resolution is committed and submitted,
**Then** recheck current permission, day/plan context, the reviewed local change set, expected server revision and writer epoch; commit the new local correction proposal and its new outbox events atomically before reporting it locally saved,
**And** create new correction events/batch identities under current authority with minimal provenance linking to the reviewed conflict; never edit or resubmit the old immutable batch under a new epoch,
**And** FastAPI/PostgreSQL validate the current authority, expected revision, eligible original outcomes and domain invariants before atomically accepting corrections, deduplication, receipt and next revision,
**And** server changes or newly discovered original acceptance invalidate the stale proposal rather than silently rebasing it; preserve the review and require comparison again,
**And** do not claim resolved-on-server until the matching correction receipt is durably recorded locally; a lost response retries the same new batch unchanged without applying the correction twice,
**And** do not let a delayed old request duplicate, undo or contradict the accepted resolution; test original acceptance before review and delayed requests rejected by the established revision/epoch/outcome checks. If an original outcome is still unsafe to resolve, keep it pending rather than claiming a race was settled.

**Given** local or server facts change while review is open, or an item is explicitly discarded,
**When** confirmation or reopening occurs,
**Then** compare the saved review basis with current facts; a new local correction, new server revision, changed plan or authority invalidates affected choices and requires renewed review,
**And** explicit discard names the affected unsynchronized proposal and its consequences, without labelling that proposal server-accepted or deleting an already accepted historical fact,
**And** do not discard an unknown-outcome submission as though it was rejected; resolve its status first or retain the uncertainty,
**And** atomically record the valid local decision and update only its eligible queue/review references, leaving unrelated pending work and newer corrections intact,
**And** clean up redundant applied/discarded conflict copies once their outcome is established, retaining only necessary correction/receipt evidence until the original AD-12 expiry; there is no new conflict-retention period.

**Given** this client has lost writer authority or lacks usable access/current server evidence,
**When** it opens or attempts to apply a review,
**Then** allow only review/read operations actually authorized by current owner/day access; loss of a day grant does not automatically grant read access, and local lock still hides private content,
**And** never let review itself increment writer_epoch, rebind a grant or take control; application requires established current authority, with transfer handled separately,
**And** an old client preserves permitted pending work for later explicit review and stops acting as writer once it learns of takeover; it cannot auto-submit old work under the replacement epoch,
**And** offline saved review is labelled against its last verified basis and cannot be declared server-resolved without validation; access recovery follows AD-10 and pending revocation remains first,
**And** a generic conflict choice cannot solve 5.4's missing verifiable start-time basis, resurrect expired/terminal work or authorize a new day after ordinary expiry.

**Given** storage failure, expiry, logout or interrupted resolution,
**When** review/resolution is saved, sent or recovered,
**Then** preserve the last committed permitted state and immutable batches, with explicit failure rather than silent reset or false completion,
**And** restart restores review inputs/decisions and distinguishes locally saved resolution, server-confirmed resolution and unresolved originals without applying anything twice,
**And** check original access/data deadlines before private display, status lookup and submission; expiration deletes affected private copies and forbids replay rather than extending them for review,
**And** use authenticated FastAPI and real PostgreSQL transactions for required resolution metadata, introducing only fields/entities needed by this slice; no private payloads in logs, public demo or diagnostic exports.

**Given** representative operational conflict fixtures and an actual PostgreSQL backend,
**When** verification runs,
**Then** test a same-writer stale revision, a former writer with authorized read but no write, lost-original receipt, accepted original discovered during review and an original still of unknown outcome,
**And** test local/server changes during review, grouped dependent corrections, explicit retain/discard/defer, cancel/reopen, transaction failure, resolution receipt loss and delayed old requests,
**And** include a manual stop correction at a repeated stop, a bus-change registration with unknown actual time, a notice version that changed and a plan revision requiring E2 confirmation,
**And** verify no silent overwrite, false acknowledgement, duplicate effect, unauthorized takeover or new expiry; fixture-established current authority makes these tests independent of future transfer UI.

**Traceability:** Explicit recovery/conflict portions of FR-18/20 and preservation FR-17; shared FR-1/6/9/11/14/16 and FR-24 expiry. NFR-1–4; UX-DR8/14/16/17/19/22/23/38/39/44. AD-2 preserved local work, AD-4/5 transactional receipts and immutable batches, AD-8 source versus driver state, AD-9 operational invariants, AD-10 read/write access and logout, AD-11 explicit review/new corrections under current authority, AD-12 conflict-copy cleanup and original expiry. E6/E7 extend their specific role/terminal invariants later.

**Dependencies:** Implemented 5.6 conflict detection, E1 immutable receipt/status support and E2–E4 domain validation/provenance, plus 5.1–5.5 access and recovery. Same-client revision conflicts are independently resolvable; former/current-writer fixtures verify boundaries without a future transfer flow. Ingesting another physical device's retained work accompanies the later explicit transfer/recovery story, not an implicit cross-account capability here.

**Size boundary:** One preserved-conflict comparison and explicit correction/discard/defer flow using existing domain commands. No generic merge engine, automatic rebase, writer transfer, device-to-device transport, mentor workflow, terminal trimming/settlement or clock-proof solution. Domain-specific failures remain explicit rather than creating unrestricted edits.

**Pilot qualification:** Controlled client/FastAPI/PostgreSQL race and recovery tests contribute to E8-D. E8-P needs integrated actual-device disconnect/reconnect and later writer-transfer behavior with readable, movement-governed review. E8-E remains field evaluation. Tests are specified, not executed in planning.

**Approval:** Approved by the owner on 2026-09-26 with revision conflict, rejected change and unknown lost-receipt outcome kept distinct. Review requires a valid basis; driver choices cannot overwrite history or give manual corrections false source/GPS evidence. Planning approval only; the approved copy in epics.md is canonical.
