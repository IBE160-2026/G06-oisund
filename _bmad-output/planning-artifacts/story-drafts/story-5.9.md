---
status: approved
created: 2026-09-26
epic: E5
story: '5.9'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.8', '5.7', '5.6']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

This slice provides explicit emergency takeover when planned handover cannot drain the previous device. It reuses 5.8's atomic authority transfer, destination precheck, retry-safe outcome and post-transfer verification, while exposing the possible gap in server-held work. Returning-device detection preserves unsynchronized work; moving that evidence to the current writer for cross-device review is a separate subsequent slice.

### Story 5.9: Take Over an Unavailable Device's Day with Explicit Missing-Work Awareness

As the pilot owner,
I want to deliberately take over my active day from an unavailable or undrainable device using the last verified server state,
So that I can continue on a replacement while knowing that unsynchronized old-device work may be missing and will not silently merge later.

**Acceptance Criteria:**

**Given** planned transfer cannot finish because the former device is unavailable or cannot drain its work,
**When** the same owner opens the separate emergency takeover path,
**Then** require valid authenticated access on the replacement and reachable authorized backend state for the concrete active unexpired day,
**And** show the last server-received operational timestamp/revision and its available recovery basis, clearly stating that later work on the old device may be missing,
**And** distinguish server receipt time from actual activity/observation time and from source retrieval time; none proves when the old device last operated,
**And** require an explicit owner confirmation of the named day/destination and possible missing work, under existing movement restrictions; timeout, login or missing heartbeat alone cannot trigger takeover,
**And** cancellation leaves authority unchanged, and the old device's cooperation is not a hidden prerequisite for this emergency path.

**Given** a takeover warning is presented against a specific server revision,
**When** the owner confirms it,
**Then** verify the review basis still matches the authoritative day/writer/revision before transfer; newly accepted old-device work or another takeover invalidates a stale confirmation and requires refreshed review,
**And** show known available/missing context without claiming the backend can enumerate events never received from an offline device,
**And** verify the replacement's same-owner access and actual required complete compatible app-file set before retiring old authority, following 5.8's destination-bound precheck,
**And** invalid access, missing app files or an ineligible day prevents transfer rather than weakening the precheck because the action is labelled emergency,
**And** unavailable critical recovery context is explicit; emergency takeover cannot turn a merely prepared or unverified active flag into an authorized active day. In particular, unresolved 5.4 timing evidence is not repaired by choosing takeover.

**Given** the owner confirms an eligible unchanged takeover basis and destination readiness,
**When** the backend commits takeover,
**Then** atomically increment writer_epoch, rebind the existing bounded day grant to the authenticated replacement/session, retire the old client's grant and save the post-transfer revision and operation result in PostgreSQL,
**And** preserve all existing authority/data limits; neither emergency selection, fresh destination login nor missing old-device work automatically extends the old grant or data deadline,
**And** no old-client drain is claimed, and no fabricated completion/acknowledgement is added for work that never reached the server,
**And** racing old-device writes either commit before the checked takeover basis, causing review to become stale, or are rejected as new mutations under the old epoch afterward; there is no arrival-order merge,
**And** use 5.8's stable request identity/status lookup for lost responses and repeated attempts, respecting current read authorization and expiry; unknown outcome is not permission to start a second takeover or return authority automatically.

**Given** takeover is confirmed,
**When** the replacement recovers the day,
**Then** load/verify permitted recovery state and data against the returned post-transfer revision and current authority before controlling the day, using 5.8 rather than trusting a previously downloaded copy,
**And** show that restored context is the last server-accepted basis with possible missing old-device work; do not label the reconstruction a complete record of actual driving,
**And** preserve known manual pins, bus identity/provenance, stop occurrence, corrections and notice-version states, retaining unknown/missing values rather than inferring later outcomes from the schedule,
**And** old position/speed and source information remain historical with an observation gap; transfer provides no new GPS evidence, full standstill, first-start exemption or proof of the 100-metre target,
**And** if actual context needs correction, use existing movement-permitted E3 actions and manual provenance; absent critical state cannot silently choose an arbitrary trip or unrestricted control state,
**And** revision mismatch, local persistence failure, subsequently evicted files or changed authority keeps the replacement not ready and requires explicit recovery, never automatic transfer back.

**Given** unsynchronized old-device work may include notice receipt/audio-attempt state,
**When** retained notices are reconstructed on the replacement,
**Then** preserve known source identity/version and confirmed interaction state, but do not infer that unknown old-device seen/registered/audio results were absent,
**And** treat the retained backlog as recovery, not newly arriving notices that deserve catch-up chimes; an indeterminate old playback outcome remains silent,
**And** genuinely new receipts after takeover use existing 4.8 eligibility under the actual current trip, not takeover itself as an audio trigger,
**And** do not mark notice content seen merely by downloading it or erase a known hidden/registered version; missing interaction evidence remains explicitly uncertain where material to the displayed result.

**Given** the former device returns with retained local work,
**When** it learns from an authorized authority/status check or rejected request that takeover occurred,
**Then** stop its writer activity and coordinated tabs, preserve permitted immutable events/batches and last local context, and explain that the day is controlled elsewhere,
**And** do not adopt the new epoch, retry old events under new identities, overwrite the replacement's state or discard old work as if acknowledged,
**And** read/review access still follows AD-10: retired day authority is not a new read grant; settle pending logout and require appropriate same-owner application authorization where needed,
**And** use authorized original receipt/status lookup to distinguish already accepted events from rejected or unresolved ones, including lost responses from before takeover, without resubmitting operational effects,
**And** a still-disconnected former device cannot know immediately that takeover occurred and may continue accumulating local changes; takeover status must say that backend authority moved, not that the old device has already stopped. The backend rejects later new writes under its old authority, and all permitted local changes remain possible unsynchronized work for explicit review once the device returns,
**And** retain local work for the separate explicit cross-device review path with 5.7's provenance/outcome rules; this slice does not claim that retained old-device changes have already reached the current writer.

**Given** account revocation, pending logout, terminal state, original expiry or an unsafe recovery condition,
**When** takeover, lookup or return-device recovery is attempted,
**Then** apply access/lifecycle checks before any private read or write; an emergency label bypasses none of them,
**And** enforce original AD-12 expiry on both devices and server-held copies, including transfer metadata and pending conflict references; do not extend retention to wait for the old device,
**And** after expiry no late upload may recreate the day; if the old device/storage is permanently lost, report that its never-synchronized work may be unrecoverable rather than inventing a backup,
**And** preserve useful permitted state through transaction/local-write failure and distinguish local preservation from server acceptance,
**And** store only necessary authenticated takeover/confirmation/revision metadata in existing local and FastAPI/PostgreSQL scope, with private/demo isolation and no private payloads or credentials in logs.

**Given** two isolated clients and a real PostgreSQL backend,
**When** verification exercises emergency takeover,
**Then** cover an offline/lost old device, an available but undrainable device, explicit cancel/confirm, wrong-owner caller, expired/terminal/prepared day, missing destination assets and unknown activation eligibility,
**And** test old writes arriving before/after the takeover transaction, two competing replacements, a changing confirmation basis, database failure, lost response, retry and replacement restart/recovery failure,
**And** retain unsynchronized manual trip/stop/bus changes and notice/audio state on the former device; verify the replacement exposes the possible gap and its return neither duplicates accepted work nor silently merges rejected/unknown work,
**And** keep the former device disconnected through confirmed takeover, make another local correction, then reconnect: the UI never claimed it had already stopped, new old-epoch writes are rejected and the local correction survives for explicit review; separately verify unchanged deadlines, pending-logout lock, no fresh-start exemption, no old audio replay and one current backend writer,
**And** use authoritative fixtures to test grant/epoch behavior, not to claim real replacement-device sensing or actual source coverage.

**Traceability:** Emergency recovery FR-18/20 and continuity FR-17, bounded FR-1, shared actual-context/manual/notice FR-6/9/11/14/15/16 and expiry FR-24. NFR-1–4; UX-DR3/14/16/17/19/23/25/38/39/44. AD-2 local work and offline limits, AD-4/5 atomic authority/receipt outcome, AD-8 notice provenance, AD-9 context, AD-10 access, AD-11 explicit emergency takeover and former-writer preservation, AD-12 accepted loss/expiry, AD-13 gated access and AD-14 compatible recovery. E6/E7 later extend their role/terminal evidence rules.

**Dependencies:** Implemented 5.8 transfer transaction/prechecks/result recovery, 5.7 conflict outcome/provenance rules, 5.6 reconnect detection and E1–E4 persistence/sensing/notice contracts. This slice demonstrates takeover and preserved former-device work without a future cross-device evidence transport UI. That remaining integration will feed 5.7 under current authority.

**Size boundary:** Explicit emergency takeover from the last server-held basis and safe returning-old-client behavior, reusing planned-transfer primitives. No automatic failover, cross-account collaboration, new credential architecture, private backup, full evidence transport/reconciliation UI, E6/E7 functionality or timing-proof workaround.

**Pilot qualification:** Controlled two-client/FastAPI/PostgreSQL cases contribute to E8-D. E8-P requires integrated actual-device takeover/restart, honest missing-work presentation, qualified replacement capabilities and later cross-device review. E8-E remains later field evaluation. No implementation or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 with a disconnected former device unable to learn takeover immediately. Server authority transfer must not claim the old device already stopped; later old-authority writes are rejected and permitted local changes remain possible unsynchronized work for explicit review. Planning approval only; the approved copy in epics.md is canonical.
