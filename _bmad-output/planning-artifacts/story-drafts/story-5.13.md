---
status: approved
created: 2026-09-26
epic: E5
story: '5.13'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.12', '5.11', '5.7', '5.6', '5.1']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

This slice implements AD-12's closure settlement protocol when privacy trimming affects pending payloads: one minimal local recovery checkpoint, payload-free original-outcome reconciliation and atomic server closure with retired-ID fences. It is testable with validated close/abort commands and representative retention fixtures. E7 owns the driver-facing end confirmation, initial summary review/PDF and final integrated lifecycle; E6 supplies actual accompaniment scope. Those future interfaces are not prerequisites for this protocol test.

### Story 5.13: Settle a Closed Day Without Replaying Deleted Work

As the pilot owner,
I want permitted final facts and pending corrections preserved and settled when closing my day requires other data to be deleted,
So that closure neither loses the allowed result nor reintroduces private information through a retry or delayed request.

**Acceptance Criteria:**

**Given** a valid explicitly confirmed own-day end/abort command and an applicable retention projection,
**When** closure affects local state and pending payloads,
**Then** validate owner/day/context, applicable authority and the command's confirmed actual end/abort basis, keeping it distinct from scheduled end or an intermediate work-part/accompaniment ending,
**And** retain only the final facts/corrections permitted by the established domain/privacy rules; unknown outcomes/times stay unknown and retained manual/source/GPS provenance does not change,
**And** test the retention projection with explicit accompanied-versus-unaccompanied fixture portions: keep allowed accompanied evidence and exclude the linked plan's unaccompanied remainder, without implementing E6's assignment UI or inventing actual accompaniment,
**And** a missing/inconsistent retention basis is a visible failure, not permission to preserve the entire private day indefinitely or guess which evidence is permitted,
**And** this protocol does not auto-confirm ending from position, schedule, depot arrival or elapsed time. E7 later invokes it through its approved confirmation flow.

**Given** affected private payloads occur in operational state, pending batches or conflict/review copies,
**When** the local closing transaction commits,
**Then** atomically preserve permitted final facts and unsynchronized corrections in one minimal trimmed recovery checkpoint, record the terminal local state and delete prohibited payloads from the affected local copies,
**And** retire the original affected batch/event identities rather than modifying their immutable payloads; if a batch mixes permitted and prohibited content, retain the permitted result in the checkpoint instead of resending a modified original,
**And** keep only permitted checkpoint content plus necessary payload-free identity/hash/status metadata for original-outcome lookup, within the original applicable deadline,
**And** retirement means no more payload replay, not acknowledgement, proof of rejection or successful server deletion,
**And** coordinate tabs and outgoing work so no new original payload is queued after closing; already transmitted requests may still arrive and must be handled by the server transaction below,
**And** a transaction failure does not present closure/trimming as committed or discard the only permitted correction; stop unsafe sending, expose the failure and retry the validated local transaction. Original expiry/locking guards still apply.

**Given** local closure/deletion has committed while another tab, stale local copy or delayed request still holds the former content,
**When** any tab/worker tries to persist, restore, render again or enqueue that content, including after restart,
**Then** check the durable current day closure/deletion state and applicable expiry within the guarded write/recovery path before accepting the result; a stale in-memory active flag or cached snapshot cannot override it,
**And** persist the minimal payload-free closure/deletion guard with the local closing transaction, and coordinate/invalidate stale views and writers; cross-tab notification alone is insufficient if a tab was suspended or missed it,
**And** reject or trim prohibited late content without saving it back into the day, outbox, review intake or migration/recovery copies, preserving only permitted checkpoint/receipt-status outcomes,
**And** unreadable/missing authoritative recovery state cannot be interpreted as permission to recreate the old day; retain locking/error behavior and original expiry rather than manufacture fresh scope,
**And** the guard follows the existing retention boundary and contains no prohibited payload or permanent private history; expiry/existence guards still prevent resurrection after normal cleanup,
**And** test two simultaneous tabs with an old queued save, suspended/resumed tabs missing notifications, stale snapshot recovery on restart and a delayed source/server response after local closure but before server settlement; none can restore deleted content or queue its replay.

**Given** local closure succeeded without confirmed server settlement,
**When** the app closes/reopens, reconnects or a late callback arrives,
**Then** recover the same minimal checkpoint and retired-ID metadata with the day still terminal locally, distinguishing locally closed from server settlement pending/failed,
**And** never reconstruct deleted content from caches, old responses, review intake, migration staging or another retained snapshot, and never use the original retired batch as a retry payload,
**And** keep checkpoint identity/content stable across retries; closure does not restore an active trip, restart timers or authorize new operational activity,
**And** local trimming does not claim that already transmitted/server-held or disconnected other-device copies were simultaneously erased; server settlement and later guarded device recovery must enforce the corresponding deletion,
**And** any existing minimal retained result remains available only within its authorized post-end scope; actual summary/PDF rendering and subsequent read-only entry remain E7 work.

**Given** retired originals may have been accepted before the closing request,
**When** authorized reconciliation reaches the backend,
**Then** use payload-free receipt/status lookup keyed by the preserved identities/integrity metadata to discover existing acceptance without uploading deleted content,
**And** preserve valid existing receipts and compare known outcomes with the actual server revision; unexplained revision changes require explicit 5.7/AD-11 review,
**And** a missing receipt or an in-flight original is not labelled rejected; retain the distinction until the closure transaction resolves the ordering/fence outcome,
**And** old-epoch receipt lookup is read-only and still requires valid owner/day access and unexpired data; it does not restore old writer authority,
**And** returned status/receipt data must not echo prohibited original payloads or rehydrate deleted linked-person context. Accepted IDs/status remain evidence only within their retention bounds.

**Given** a valid minimal closure checkpoint, reconciled known outcomes and current writer/expected revision,
**When** the client submits the checkpoint for settlement,
**Then** use new batch/event IDs distinct from all retired originals; the checkpoint records the retained result and terminal state rather than replaying old event effects,
**And** authorize current owner/day scope, current writer, expected revision, schema, terminal intent and the allowed retained projection on FastAPI/PostgreSQL; a caller cannot declare arbitrary prohibited fields allowed,
**And** in one PostgreSQL transaction preserve existing accepted receipts, fence still-unaccepted retired identities, accept the checkpoint/result, close the day and remove prohibited linked data from all relevant server-held copies,
**And** include source/day associations, revisions, checkpoints, outboxes/review intake/conflict copies and receipt content as applicable, without deleting unrelated public source facts or other owners' work,
**And** atomically commit the closure receipt and next revision with those effects; any injected database failure leaves no partial acceptance, fencing or server closure claimed,
**And** keep a single stable closure batch in flight; it supersedes retired payload submission without reviving or treating retired batches as acknowledged.

**Given** an original request races with closure settlement,
**When** the backend serializes their transactions,
**Then** if the original committed first, retain its authorized prior receipt and account for the resulting revision before a valid checkpoint can commit; do not apply its effects twice through checkpoint replay,
**And** if closure commits first, fence unaccepted retired IDs so later original submissions return batch_retired without inserting their effects or deleted payloads into retained day state,
**And** authorized retries of already accepted originals return their prior receipt rather than being misclassified as newly rejected, even though their prohibited payload content has been removed,
**And** terminal-state validation also prevents resurrection through fresh batch/event IDs, not merely the listed retired identities,
**And** distinguish permitted bounded post-end review corrections from operational resumption; this protocol does not create unrestricted post-end editing or implement E7's review decisions,
**And** test each ordering with real PostgreSQL transactions, including an original accepted between lookup and settlement, which makes the expected revision stale and requires reconciliation again.

**Given** settlement commits but its response is lost, or writer/revision/access changes before acceptance,
**When** retry/status handling runs,
**Then** retry the same new closure IDs and unchanged payload within valid access/expiry, returning the existing matching receipt without another close, revision increment or repeated domain effects,
**And** mark server-confirmed settlement only after a matching closure receipt is durably recorded locally; HTTP success, local deletion, an original receipt or a transport receipt from 5.10 is insufficient,
**And** stale epoch/revision preserves only the allowed trimmed checkpoint for explicit review; do not restore prohibited originals, silently rebase, mint replacement IDs or take over automatically,
**And** pending logout/revocation retains priority, and 5.5 Access recovery leaves private content locked as required; no retention extension or access bypass is granted to finish settlement,
**And** update/migration uses 5.11/5.12 contracts to preserve the same closure/retirement meanings across supported builds.

**Given** a closed/aborted day and its pending checkpoint/status records,
**When** deadlines or remote earlier ending information are evaluated,
**Then** apply the one combined-day AD-12 data clock and any earlier applicable limit, with post-end authority capped at the earliest of existing day-grant deadline, actual end/abort plus seven days and data expiry,
**And** distinguish that data deadline from authority expiry; no lookup, retry, review, export, reopening or new receipt restarts either clock,
**And** expire/delete all affected private checkpoint, receipt, retired-ID, conflict and grant copies when due even if settlement never succeeded; server checks deny expired access independently of periodic purging,
**And** a returning closed/offline device deletes expired data before private use and never uploads it to recreate the day; a newly learned earlier ending creates no grace period,
**And** absent explicit ending, the existing planned-end expiry remains applicable without fabricating a completed shift; fixtures test this boundary separately from actual confirmed closure,
**And** no historical private backup or retained prohibited payload is introduced to make retry easier.

**Given** the protocol is exercised before E6/E7 user interfaces exist,
**When** acceptance evidence is produced,
**Then** use explicit validated close and abort command fixtures with a minimal allowed-result schema and mixed allowed/prohibited linked-data fixtures, not a production bypass that accepts arbitrary client trim claims,
**And** include unsent originals, accepted originals with lost receipts, mixed batches, lookup failure, original-before-closure and closure-before-original races, fresh-ID resurrection attempts and unknown revision changes,
**And** inject failure before/after local closing commit, at each server atomic effect, before/after closure receipt delivery, on local receipt save and during restart/expiry,
**And** inspect IndexedDB and actual PostgreSQL copies to verify permitted final facts/corrections survive while prohibited data cannot be replayed or recovered from secondary copies,
**And** keep local-closure, retired-original outcome and server-settlement status separately readable, with movement-governed error/retry feedback and no forced driver interaction,
**And** leave E7 end confirmation, actual accompaniment-derived scope, initial summary review, PDF and final whole-lifecycle acceptance as explicit integration obligations rather than claiming these fixtures completed them.

**Traceability:** E5 settlement/retention protocol FR-24, recovery FR-18/20 and offline final-result preservation FR-17; bounded FR-1 and consumed terminal/summary FR-21/22 without their UI implementation. NFR-1–4; UX-DR23/31/32/33/35/36/38/44 where applicable to recovery/terminal scope. AD-2 atomic local state, AD-4/5 PostgreSQL receipts/revisions, AD-10 bounded post-end authority, AD-11 conflicts/current writer, AD-12 minimal closure checkpoint, payload retirement, atomic fences/cleanup and original expiry, AD-13 gate failures and AD-14 compatible retained-client settlement. E6/E7 own actual role/summary/closing integration.

**Dependencies:** Existing 5.1 authority, 5.6 retry, 5.7 review, 5.10 copy tracking and 5.11/5.12 compatible recovery. Concrete protocol schemas and validated fixtures make closure settlement independently testable; it must not wait for E6/E7 screens to supply its transaction, retirement or fencing behavior. Later features provide their real permitted-content projection and extend all-copy integration tests.

**Size boundary:** One end-to-end AD-12 settlement protocol, including its inseparable local retirement/server fence race. Reuse existing identity, receipt, conflict and expiry infrastructure. No end-shift UI, mentor assignment engine, summary/PDF renderer, general event compaction, archive or new authentication model.

**Pilot qualification:** Deterministic client/FastAPI/PostgreSQL race and all-copy deletion tests contribute to E8-D. E8-P requires integration with actual E6/E7 closing/retention, device restart, gate failure, source/old-device responses and supported app updates. E8-E remains later field evaluation. Tests are specified, not executed during planning.

**Approval:** Approved by the owner on 2026-09-26 with durable deletion/closure state preventing another tab, old local copy or delayed response from restoring deleted content after local closure, tested through restart and concurrent tabs. Unknown original-batch outcome remains distinct from the new closure receipt. Planning approval only; the approved copy in epics.md is canonical.

**TIME-01 amendment (owner, 2026-09-27):** Closure settlement consumes 5.4's server-approved versus unresolved/rejected start status; closure cannot approve a rejected activation or certify a locally reported end time. For unverifiable offline end, preserve original server-issued Tg and enforce `D = min(Tg + 7 days, earlier binding data deadlines)` for the minimal checkpoint, old IDs, receipts, conflicts and grants. A later closure receipt does not extend D. An uncertain-time offline restart keeps the private result app-locked until trusted control and deletes expired copies before view; closed/unreachable tablets do not guarantee physical deletion at D. Test both orderings of original activation acceptance/rejection and closure settlement.
