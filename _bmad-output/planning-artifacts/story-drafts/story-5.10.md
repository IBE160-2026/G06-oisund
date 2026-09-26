---
status: approved
created: 2026-09-26
epic: E5
story: '5.10'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.9', '5.8', '5.7', '5.6']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

This slice brings surviving old-device changes into the current writer's explicit 5.7 review through a bounded same-owner private recovery flow. Receiving evidence is separate from accepting operational effects. It neither returns writer authority to the former device nor creates a private backup/export system.

### Story 5.10: Bring Surviving Old-Device Work into Explicit Current-Writer Review

As the pilot owner,
I want permitted unsynchronized changes surviving on a former device made available for review on the device now controlling my day,
So that I can recover valid corrections without replaying obsolete batches or silently replacing newer work.

**Acceptance Criteria:**

**Given** a former device returns after 5.8/5.9 with possible unsynchronized work,
**When** the owner opens recovery under valid access and movement permission,
**Then** preserve the original day/client/epoch, event/batch identities and immutable content, the known baseline and available receipts, including changes made while the device was unaware of takeover,
**And** distinguish accepted, definitively rejected and unknown-outcome work using authorized status lookup; missing receipt alone does not prove rejection,
**And** show what remains only on the old device, what has been received for review and what is actually resolved, without labelling every surviving change lost or unaccepted,
**And** retired day authority alone is insufficient to view/send retained private work; apply same-owner access recovery and pending-revocation rules before private traffic,
**And** the old device stays out of operational writer mode and cannot submit original effects under a replacement epoch.

**Given** an authorized former device and an authorized current writer for the same concrete unexpired day,
**When** the owner explicitly requests transfer of the identified retained work for review,
**Then** provide a bounded authenticated private recovery path through the existing application/backend, with the destination and source work set explicitly identified,
**And** require current-writer authorization for creating/accepting the review intake and revalidate its current day/epoch/revision scope on the backend; the former client's retired authority cannot authorize operational or unrestricted server mutations,
**And** the former device may supply only the identified evidence to that authorized isolated review intake under valid same-owner access; document/test this narrow request/response authorization contract without adding a bearer login, public upload link, credentials exchange or cross-account sharing,
**And** stage it as conflict/recovery evidence, not as an operational SyncBatch execution: receipt for review transport is explicitly distinct from an AD-5 receipt acknowledging original event effects,
**And** receiving the work cannot change the confirmed plan, active trip, progress, source facts, notice seen/audio state, writer epoch or day grant,
**And** cancellation or unavailable destination leaves permitted source work intact; there is no automatic background merge or takeover-back.

**Given** a retained work set is offered for review transfer,
**When** it is validated and persisted,
**Then** bind its stable identity to owner/day, source client/epoch, original event identities, content integrity and necessary plan/context/baseline references, preserving original origins, occurrence/registration times and unknown values,
**And** include only the minimal allowed payload and context needed for interpretation and 5.7 review; exclude raw import originals, credentials, raw GPS tracks and unrelated days/people,
**And** validate schema, size, identities, references and original expiry before treating the set as complete; imported client metadata is a provenance claim, not independent proof of GPS, source truth or an eligible pre-expiry start,
**And** reject mixed-owner/day, altered-content identity reuse, unsupported or truncated sets without partially applying domain effects; retain recoverable input with a clear reason where still permitted,
**And** partial transfer is visibly incomplete and cannot be used as a complete comparison; failure of some items never silently discards the remainder or describes the whole set as recovered,
**And** use existing IndexedDB/FastAPI/PostgreSQL infrastructure with only the necessary bounded review-intake metadata and payloads, not a generic file-sync/archive service.

**Given** transfer is interrupted, duplicated or its receipt is lost,
**When** the source/current writer retries or checks status,
**Then** use the same review-set identity/content and stable intake outcome so retries do not create duplicate proposals or apply events,
**And** show server-received-for-review only after validated complete intake is committed; show available-on-current-device only after that device has received and saved the applicable set,
**And** neither transport status acknowledges old operational batches or permits silent deletion of unresolved source work,
**And** restart recovers partial/complete/status distinctions, and a false success or local write failure leaves the set retryable without changing its content/expiry,
**And** a writer change, logout or stale authorization invalidates the affected intake authorization; require a new explicit authorized destination/basis rather than delivering private work to an obsolete context.

**Given** the current writer has a complete permitted review set,
**When** the owner inspects or applies it,
**Then** feed it into 5.7's comparison against the verified current server state, showing the former-device origin and any unknown original outcomes,
**And** deduplicate by original event/batch identity and accepted receipt evidence before proposing new effects; repeated transfer or a late original receipt cannot make an already accepted effect apply twice,
**And** persist the exact received set and server/local comparison basis with retain/discard/defer choices; subsequent local/server/plan/authority changes invalidate affected review and require comparison again,
**And** selected valid corrections become new events under the current writer, with original evidence and manual correction provenance distinguishable; do not rewrite old batches or history,
**And** bus actual time stays unknown when unknown, stop identity includes the trip occurrence, notice state remains version-specific, and no imported action produces a new chime or fresh GPS evidence merely by being received,
**And** unresolved 5.4 time evidence, terminal restrictions and rejected domain invariants remain unresolved/protected rather than becoming valid through a generic recovery approval.

**Given** the current writer applies, explicitly discards or defers reviewed items,
**When** the corresponding resolution status is recorded and returned to the former device,
**Then** bind the disposition to the exact reviewed set/items and the established original outcomes; applied corrections require their own matching operational receipt before server-confirmed resolution,
**And** distinguish received for review, applied as a new correction, explicitly discarded and still unresolved; discarding does not manufacture an original acceptance receipt,
**And** remove only redundant applied/discarded conflict copies once the exact permitted outcome is established, preserving unrelated/newer source changes and necessary correction/receipt evidence under the original deadline,
**And** a lost disposition response leaves the former device's status unresolved and safely repeatable; it cannot prompt duplicate application or broad deletion,
**And** a delayed old request remains governed by the old epoch and original receipt rules: read-only acknowledgement of prior acceptance is distinct from permission to mutate the current day,
**And** the old device cannot infer all its work was handled from one item's success or from a newer server revision alone.

**Given** retained work or a staged review set reaches its original retention deadline, loses access or cannot be recovered,
**When** display, sending, status lookup or cleanup occurs,
**Then** apply AD-10/12 to every source, staged, destination and review copy, including any earlier known applicable day deadline; intake/review/retry never starts a new retention period,
**And** prevent expired-day re-upload/recreation even if the current writer would like to recover it, and remove expired copies before use when a closed/offline client returns,
**And** preserve only permitted trimmed content when a terminal/privacy restriction is already in force; this transport cannot revive payloads retired under AD-12 or implement E7's closing protocol by replaying them,
**And** permanent loss of the former device's only copy is reported as potentially unrecoverable; the feature does not promise an archive, historical backup or offline peer-to-peer transfer,
**And** failed storage/status operations retain allowed work without false durable success; logs and demo fixtures contain no private payloads or credentials.

**Given** two isolated same-owner clients with actual PostgreSQL persistence,
**When** recovery-transfer tests run,
**Then** include an old device that changed a stop/bus after an unobserved takeover, an accepted event with lost receipt, a rejected old-epoch event and an unknown outcome,
**And** cover exact replay, changed content under reused identity, partial/malformed set, wrong owner/day/destination, expired grant/data, pending logout and a second takeover during intake,
**And** test interruption before/after staging and destination save, lost transport/disposition responses, reopened review, edits during review and late original receipts,
**And** verify receipt meanings and current-authority checks independently: evidence transport never increments operational progress or changes writer authority, while chosen corrections require the existing authenticated atomic mutation/receipt path,
**And** demonstrate one retained correction selected for application and another explicitly deferred/discarded, with no false source/GPS provenance, duplicate effects or deletion of unrelated work.

**Traceability:** Cross-device reconciliation portion of FR-18/20 and preservation FR-17; bounded FR-1, existing manual/notice FR-9/11/14/16 and expiry FR-24. NFR-1–4; UX-DR3/14/16/17/19/23/38/39/44. AD-2 preserved local evidence, AD-4/5 isolated persisted review versus immutable operational receipts, AD-8 notice version state, AD-9 domain validity, AD-10 owner access, AD-11 old-device review and new current-authority corrections, AD-12 all-copy retention/accepted loss, AD-13 private ingress and AD-14 compatible schemas. E6/E7 extend permitted role/terminal content later.

**Dependencies:** Implemented 5.7 explicit review, 5.8/5.9 authority transfer and former-device preservation, 5.6 status/receipt checks and existing feature provenance. This adds the missing bounded cross-device intake/disposition integration; it does not require future migration or E6/E7 UI.

**Size boundary:** One same-owner review evidence transfer feeding 5.7 and returning exact resolution status. No operational merge engine, new account-sharing model, general file export/import, automatic authority return, archival backup or terminal-state reconstruction. Normal operational mutations still require current writer authority and expected revision.

**Pilot qualification:** Controlled two-client/FastAPI/PostgreSQL cases contribute to E8-D. E8-P must verify actual device interruption/storage/access behavior and readable explicit review with 5.8/5.9 integrated. E8-E remains later field evaluation. No implementation, provisioning or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 with review intake distinct from applying corrections, no return of old-device writer authority, and preserved provenance, receipt status and original deadlines through partial/repeated transfer. Planning approval only; the approved copy in epics.md is canonical.
