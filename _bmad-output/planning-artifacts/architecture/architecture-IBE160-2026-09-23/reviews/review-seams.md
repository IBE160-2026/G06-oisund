# Architecture Reviewer Gate — independent implementation seams

Reviewed: 2026-09-23. Lens: construct independently implemented units that satisfy the written decisions but disagree at their boundary. Scope: current `ARCHITECTURE-SPINE.md`, checked against the adopted decision record where necessary. No implementation or source/device tests were performed.

**Final verdict: pass after focused recheck.** The four findings below have been resolved in the spine. This recheck inspected only their fixes; it was not a new broad review. No implementation or device-test success is implied. Detailed DTOs, tables, cache-routing code, and numerical thresholds remain valid story-level work.

## Resolution record

Rechecked 2026-09-23 after the parent applied the changes:

| Finding | Disposition and inspected evidence |
| --- | --- |
| 1. Trimming versus immutable retry | Resolved. AD-12 defines the closure-only trimmed checkpoint, local retirement without acknowledgement, payload-free receipt/status reconciliation, new checkpoint batch/event IDs, current writer/revision checks, atomic fencing and terminal cleanup. Late original requests cannot restore deleted facts; unresolved conflicts preserve the permitted checkpoint. The API outcomes now include `409 batch_retired`. The mixed pending-batch/lost-response case remains an implementation qualification obligation. |
| 2. Grant rebinding on transfer | Resolved. AD-11 atomically rebinds the scoped grant to the new authenticated client/session while advancing the epoch, retires the former grant and preserves deadlines; emergency transfer uses the same rule. |
| 3. Receipt access versus mutation authority | Resolved. AD-5 authenticates day scope and expiry before deduplication, permits authorized read-only retrieval of an existing receipt without a current original epoch, and requires current writer/revision authority for new mutations. |
| 4. Revision isolation and one in-flight batch | Resolved. AD-5 explicitly keeps one stable batch in flight per day and excludes external polling from the operational revision clock. |

The following original findings are retained as review history, not open blockers.

## 1. Linked-plan trimming needs an explicit exception to the ordinary immutable retry path

**Priority: high. References: AD-5, AD-12; SyncBatch/SyncReceipt.**

Concrete trace: an immutable batch contains both an own-day correction that must survive and linked-person material that is not actually accompanied. Its response is lost. The day then ends offline. AD-12 requires the unaccompanied material to be removed immediately from every local copy, including pending payloads. AD-5 requires the same immutable batch after an uncertain response, forbids altered content under its ID, and acknowledges only receipted events.

A privacy component can correctly remove the prohibited bytes and leave a non-payload tombstone. A synchronization component can correctly refuse to submit an altered/incomplete original batch and wait for its original receipt. Neither component has a specified way to release the surviving own-day work. Keeping the original bytes violates AD-12; dropping the entire mixed batch silently loses retained work; altering its body under the old ID violates AD-5.

The sentence saying stories must cover this boundary acknowledges the problem but does not state which protocol supersedes normal retry. This is a cross-component lifecycle rule, rather than a request for detailed endpoint fields.

**Required clarification:** define privacy-triggered retirement of the original retry payload, without calling it acknowledged. Preserve only permitted surviving evidence and minimal IDs/hash/outcome metadata. Require a non-payload receipt/status reconciliation path and a fresh submission identity for surviving work when submission is still needed, preserving event deduplication and current epoch/revision checks. Server ending/cleanup must also prevent a late original request from restoring removed linked material. A concrete API can be designed in stories, but the guarantee must cover both originally accepted and originally unaccepted lost-response cases. Add this mixed-batch ending case to qualification.

**Decision classification:** clarification within the adopted immediate-trimming, immutable-ID and no-silent-loss policies. Any alternative that keeps forbidden payloads longer would be a new user decision and should not be inferred.

## 2. Writer transfer must transfer the client-bound continuation grant as well

**Priority: high. References: AD-10, AD-11. Already reported by rubric reviewer.**

AD-10 binds the day grant to owner, client and concrete day. AD-11's distilled transfer transaction changes `writer_epoch` and returns the post-transfer revision, but omits the corresponding grant operation. An access module can enforce the original client binding exactly, while a writer module legitimately grants control to a new client. The new client then cannot use continuation when ordinary access expires; issuing a new grant independently can instead slide its original deadline.

**Required clarification:** include the new client's appropriately scoped day permission in the atomic ownership transfer, preserving the original authority and retention bounds unless a separately authorized extension occurs. Ensure the old client cannot exercise the transferred writer authority. The decision log already says transfer occurs “with the appropriate scoped day permission”; restore that guarantee to the spine. Lost transfer responses need a coherent status result for both writer and grant, not a half-transferred state.

**Decision classification:** restoration of adopted AD-10/AD-11 intent, no new user choice. The parent has already queued this fix.

## 3. Distinguish authorization for a prior receipt from authority to make a new write

**Priority: medium. References: AD-5 first synchronization paragraph, AD-11 handover/recovery.**

The distilled AD-5 order can be implemented as ownership/expiry, then current writer check, then deduplication. A different implementation reads “valid identical retry returns its original receipt” as authorizing receipt retrieval before the current writer check. Both are plausible readings, especially because the paragraph separately names current authorization/expiry but does not distinguish write authority from receipt-read scope.

Concrete trace: batch B commits under epoch 2, its response is lost, then explicit emergency takeover assigns epoch 3. An authenticated owner later resolves B. The first implementation returns `writer_conflict`; the second returns the durable receipt without making a write. The latter is explicitly allowed in the adopted AD-11 decision record. This distinction matters for classifying preserved work as already applied rather than proposing a duplicate manual correction.

**Required clarification:** after authenticating owner, authorized day/read scope and expiry, resolve a matching existing receipt before applying current-epoch or expected-revision checks for **new mutations**. An existing receipt never restores writer rights. If a dedicated receipt lookup is chosen instead, give it the same distinction. Retain the prohibition on automatic submission of old pending work under a new epoch.

**Decision classification:** clarification of adopted idempotency/handover semantics, not permission for an old client to keep writing.

## 4. Explicitly exclude source polling from the operational revision clock

**Priority: medium. References: AD-5, AD-7, Consistency Conventions.**

The spine distinguishes source versions, plan revisions and server revisions but no longer explicitly states that source polling must not advance the operational day revision. A source module can update the day's recovered notice/bundle view and increment `server_revision` for consistency; the sync client can legitimately use its last accepted operational revision. An otherwise uncontested driver action then fails every time a poll intervenes, entering AD-11 conflict resolution despite no competing operational edit. Neither module has silently overwritten manual work, and distinct source version identifiers alone do not prohibit this behavior.

**Required clarification:** restore the adopted rule that external-source polling/versioning has its own state and does not increment the operational day revision. Define that revision as the concurrency token for accepted private operational changes, with plan and source dependencies represented separately. Also retain the logged one-stable-in-flight-batch-per-day rule so the same client does not create avoidable races against its own expected revision. These are ordering guarantees, not endpoint or table design.

**Decision classification:** restoration of the adopted AD-5 synchronization conventions.

## Examined seams without an additional finding

- Access expiry remains distinct from application expiry/revocation; prepared local continuation, blocked logout and pending revocation have an explicit ordering. The review does not propose an Access bypass.
- Service Worker activation is expressly separated from active-build/schema activation. Close/reopen, missing assets and preservation of local data have binding failure behavior; implementation details can remain in stories. The rubric review's additional old-response-contract clarification complements this.
- Notice content version, source ordering and local per-version interaction state are separated. Sparse closure, incomplete responses and identical fetches have conservative invariants. Adapter ordering implementation still needs its specified source qualification, but no new contradictory architectural choice was found.
- Late uploads and private data retention have explicit server-side guards independent of cleanup scheduling. No historical private backup is silently required by recovery or release policy.

## Finalization recommendation

The inspected clarifications preserve the adopted privacy, access-duration, transfer and no-loss rules; no AD-15 or new product tradeoff is required. Keep the implementation-level details deferred and include the mixed retained/prohibited pending-batch test when implementing closure settlement. This reviewer has no remaining blocker to document finalization.
