---
status: approved
created: 2026-09-26
epic: E5
story: '5.8'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.7', '5.6', '5.3', '5.2', '5.1']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

This slice implements planned transfer of an active own day between two available clients of the same owner. The old client stops mutations and drains accepted work, the backend transfers writer/day-grant authority atomically, and the destination verifies recovery against the post-transfer revision. Emergency takeover and recovery of an unavailable old client's unsynchronized work remain separate.

### Story 5.8: Transfer an Active Day Deliberately to a Verified Replacement Device

As the pilot owner,
I want to transfer my active working day to another authenticated device after synchronizing the current one,
So that the replacement continues the correct state without two authorized writers, lost corrections or renewed deadlines.

**Acceptance Criteria:**

**Given** an active unexpired own day, its current writer and an available replacement client,
**When** the owner begins a planned transfer under the existing movement policy,
**Then** identify the concrete day and intended destination explicitly, require the destination to be authenticated as the same owner, and validate applicable source/destination access on the backend,
**And** require usable backend connectivity for the transfer itself; a locally cached plan or grant cannot authorize an offline ownership transfer,
**And** show preparation, sending remaining work, transfer outcome and destination readiness as distinct steps without exposing technical epoch/session identifiers,
**And** no missed heartbeat, network timeout, new login or opening the day on another device triggers takeover,
**And** no mandatory transfer interaction occurs while driving; source links/detail and transfer controls retain access/movement restrictions.

**Given** the owner deliberately prepares the source client for handover,
**When** transfer preparation starts,
**Then** stop new operational mutations on that client and its coordinated tabs, including automatic progression/notice interaction or audio-attempt effects that would create unsynchronized operational state,
**And** persist the handover-pending guard so reopening cannot silently resume as writer during an unresolved transfer; show that normal tracking/writing is paused and preserve an honest observation gap,
**And** drain already committed work using 5.6 and matching receipts, resolving any unknown outcome/conflict through the existing paths before planned transfer can proceed,
**And** verify that the server has the necessary current recovery state, plan/bundle references, manual choices, movement/outage history and notice-version/receipt/attempt state; an apparently empty queue alone is not proof of a complete recovery basis,
**And** reuse necessary existing checkpoint/event contracts rather than mirroring every internal client field or copying cookies/credentials,
**And** a failed write/drain, unresolved 5.4 activation or unresolved conflict leaves transfer incomplete and preserves permitted work; it cannot silently become emergency takeover.

**Given** an explicitly identified destination before the authority transfer,
**When** pre-transfer readiness is checked,
**Then** verify valid same-owner destination access and the actual complete compatible app-file set required for this day before retiring the source writer/day-grant authority,
**And** bind the result to this destination, required build and handover attempt; a generic cached ready flag, another client or an unverified server assumption about local files is insufficient,
**And** missing/corrupt files, failed local verification, unavailable destination or invalid access prevents transfer, leaving the source authority unchanged; a source already paused resumes only under the existing verified cancellation rules,
**And** recheck applicable access at the transfer transaction and invalidate obsolete preparation evidence when the required build/destination changes,
**And** this precheck does not replace post-transfer state/revision verification or guarantee that browser storage cannot subsequently be evicted.

**Given** source changes are stopped, required work is confirmed and the destination has passed access/app-file verification for this transfer,
**When** FastAPI accepts the planned transfer request,
**Then** verify current owner/day/client authority, source writer epoch, final expected server revision, active lifecycle and unexpired grant/data limits,
**And** in one PostgreSQL transaction increment writer_epoch, bind the existing bounded day authority to the new authenticated client/session, retire the former client's day grant and persist the retry-safe transfer result with its post-transfer server revision,
**And** preserve existing grant/data deadlines and the destination's ordinary authentication clock; transfer creates neither a new fourteen-day period nor an automatic grant extension,
**And** authorization extension, if ever requested separately, follows AD-10 fresh application authorization rather than being bundled into transfer,
**And** a mismatched revision/epoch, wrong owner/destination, missing access, terminal day or expired scope causes no partial transfer; preserve source work and require explicit correction/review,
**And** requests racing from the former writer are ordered by transaction checks: an earlier accepted mutation invalidates a stale transfer basis, while a new mutation after transfer is rejected under the old epoch. Existing authorized receipt reads remain distinct from new writes.

**Given** a transfer request or its response may be lost,
**When** either permitted client retries or checks its outcome,
**Then** use the same persisted operation identity and immutable request content; identical authorized retry/status lookup returns the established result without another epoch increment or deadline change,
**And** distinguish not completed, confirmed transferred and unknown outcome; timeout or a missing response alone never reactivates the source or makes the destination ready,
**And** preserve expiry and read-access checks for lookup; retirement of the old grant does not itself confer status/private-read authority. Use an authorized destination or appropriate application access recovery where the old client no longer has scope,
**And** restarting either device restores the pending/confirmed handover state and continues outcome verification without guessing from its old local snapshot,
**And** test database failure before commit, lost response after commit, changed-content retries and concurrent attempts to two different destinations; only the valid serialized transfer succeeds.

**Given** the backend confirms the transfer with a post-transfer revision,
**When** the destination prepares to control the day,
**Then** load or verify the required recovery state and day data against that returned revision, under the new day authority and current writer epoch, before operational mutation or audio/progression side effects start,
**And** verify the compatible complete app assets and required data references from 5.2; previously downloaded state alone cannot establish destination readiness,
**And** a state/revision mismatch, missing critical recovery data, local write failure or superseding authority change keeps the destination not ready, preserving data without reverting ownership by guesswork,
**And** persist the verified recovered state and authority references before showing ready-to-continue; verify current authority again if intervening activity makes the transfer result stale,
**And** preserve manual trip pin, exact stop occurrence, bus-change provenance, plan/service date, notice seen/registered/hidden and audio-attempt state; partial optional stop/source data remains explicitly incomplete under existing fallbacks,
**And** positions/speeds from the source are historical, not live destination observations. Preserve the observation gap and established movement history; changing device does not create a genuine-first-start exception, restart a five-minute period, replay old audio or certify unobserved progression.

**Given** transfer is confirmed or remains uncertain,
**When** the source receives the result, reconnects or reopens,
**Then** keep it from operational writing once authority has moved, and reject new old-epoch mutations on the backend even if its UI has stale information,
**And** retain only permitted local data within original deadlines, with read visibility governed by current access; do not describe grant retirement as global account logout or erase all source data as a transfer side effect,
**And** unexpected retained/new local work is shown for explicit 5.7 review rather than silently submitted under the destination epoch,
**And** do not promise physical prevention of all disconnected edits on an uninformed device; the prepared source guard and server authority checks are the bounded guarantees,
**And** source content, app version, source freshness and actual bus identity do not change merely because device ownership changed.

**Given** the owner cancels preparation or the destination cannot complete recovery,
**When** the workflow exits or retries,
**Then** allow source writing to resume only if the transfer is established not to have occurred and current authority is verified, lifting the local pause without resetting operational history,
**And** cancellation after a possibly committed request cannot be treated as rollback; establish its outcome first,
**And** after confirmed transfer, destination recovery failure does not automatically give the source authority back. Retry destination recovery or use a new explicit valid transfer; no timeout-based fallback,
**And** an unavailable source or undrainable work explains why planned transfer cannot finish; emergency takeover remains a separately reviewed story,
**And** keep pending revocation ahead of all private transfer traffic, invalidate late callbacks after logout, and apply original expiry before resume/read/send. Renewal or retry never extends retention.

**Given** this planned handover is tested with two isolated browser clients and real PostgreSQL,
**When** verification exercises the workflow,
**Then** cover successful drain/transfer/recovery, changes racing with source freeze, old queued requests, wrong-owner destination, stale revision, competing destinations, lost transfer response and source/destination restart at each boundary,
**And** test old ordinary authentication expired with a valid active-day grant and an authenticated destination, preserving the old grant bound while distinguishing receipt/status read permissions,
**And** test invalid destination access and missing/corrupt app files before transfer, verifying no authority retirement; separately test files lost after the precheck, stale destination state, post-transfer revision mismatch, missing critical state, partial optional data and destination write failure, all requiring explicit recovery without automatic transfer back,
**And** include manual stop/bus corrections, notice version/audio state and a pre-existing GPS outage so restoration proves both continuity and absence of a fresh-start permission bypass,
**And** verify one current backend writer, atomic grant retirement/rebinding, identical-retry results and unchanged deadlines; no claim of success from device UI alone,
**And** store only minimal transfer/recovery metadata in existing local and FastAPI/PostgreSQL scope, protected by ownership/CSRF/no-store and original AD-12 deletion; no public pairing links, credential export or permanent private handover archive.

**Traceability:** Planned device continuation within FR-18/20 and FR-17; bounded FR-1, shared FR-6/9/14/16 and retention FR-24. NFR-1–4; UX-DR3/14/16/19/23/38/39/44. AD-2 local authority, AD-4/5 atomic persistence/receipts, AD-8 retained notice state, AD-9 operational continuity, AD-10 client-bound day authority, AD-11 planned transfer and post-transfer verification, AD-12 deadlines, AD-13 usable gated access and AD-14 compatible recovery. Role/terminal extensions remain E6/E7.

**Dependencies:** Implemented 5.1–5.7 grants, coherent build, same-client recovery, normal synchronization and conflict handling; existing E1–E4 recovery contracts. Two authenticated same-owner clients can demonstrate this slice. No emergency takeover, device transport of unsynchronized conflict copies or future E6/E7 UI is required.

**Size boundary:** One online planned handover with source freeze/drain, atomic authority transfer, retry-safe outcome and verified destination recovery. No cross-account sharing, automatic ownership expiry, emergency takeover, broad pairing platform or credential migration. Remaining unavailable-device recovery is a separate slice.

**Pilot qualification:** Repeatable two-client/FastAPI/PostgreSQL races contribute to E8-D. E8-P requires actual target-device stop/resume, usable replacement-device capability, compatible cached assets, gate/session and signal-state recovery; software authority alone does not qualify replacement hardware. E8-E remains later field evaluation. Tests are specified, not executed during planning.

**Approval:** Approved by the owner on 2026-09-26 with destination access and required app files verified before the old writer authority is retired. Post-transfer state must still be verified against the server revision before controlling the day; failure requires explicit recovery and never automatic transfer back. Planning approval only; the approved copy in epics.md is canonical.
