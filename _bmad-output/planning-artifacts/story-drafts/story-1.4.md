---
status: approved
created: 2026-09-25
epic: E1
story: '1.4'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['1.1', '1.2', '1.3']
---

## Epic 1: Access and Recover a Private Working-Day Draft

This slice synchronizes the minimal unconfirmed draft from Story 1.3 to PostgreSQL and proves that acceptance and retries do not lose or duplicate it. It does not implement draft editing, plan confirmation, active-day grants, multi-device transfer or a generic synchronization framework.

### Story 1.4: Synchronize a Private Draft with a Durable Server Receipt

As the pilot owner,
I want my locally saved draft to receive a verifiable server acknowledgement,
So that I can distinguish a draft stored only on this device from one also accepted by the backend without losing work after a connection failure.

**Acceptance Criteria:**

**Given** an unexpired local draft/event from Story 1.3, valid ordinary application authentication and no unresolved logout or access-storage error,
**When** the client connects or the owner retries synchronization,
**Then** the app submits the original committed draft event in a versioned immutable batch through the shared-origin FastAPI API,
**And** the envelope follows AD-5: schema version, batch ID, workday scope ID, client ID, writer epoch, expected server revision and ordered typed event identity/sequence/time/payload,
**And** at most one stable batch is in flight for the scope; the client persists its immutable identity/payload before sending and distinguishes pending, failed and acknowledged states.

**Given** this is the first server synchronization of an unconfirmed local draft,
**When** its minimal server scope and initial authority are established,
**Then** ownership is derived from authentication and the server binds the stable scope/client identity to initial writer authority and an explicit initial revision,
**And** initialization is retry-safe, bounded by the draft's existing expiry and rejects attempts to claim another owner's identity or an existing scope under different content/authority,
**And** the developer documents and tests initial-scope/epoch/revision handling before the first mutation; no arbitrary caller-supplied epoch grants authority,
**And** this technical scope creates no confirmed plan, active day or active-day grant; ordinary authentication is required and only necessary draft/control/receipt tables are introduced.

**Given** a valid initial draft batch,
**When** FastAPI accepts the mutation,
**Then** it checks authenticated ownership, scope, expiry, schema, current writer authority and expected revision under AD-5,
**And** PostgreSQL 18 atomically commits the draft, event/batch deduplication, matching receipt and next server revision,
**And** an injected failure before commit leaves none of those domain effects partially applied,
**And** success is returned only after the database commit; a UI-only saved flag cannot stand in for a server receipt.

**Given** the server committed a batch but the response was lost, or the browser closed before locally recording it,
**When** the client reloads and retries under valid access before expiry,
**Then** it retries the same persisted batch ID, event IDs, schema and payload,
**And** an identical authorized retry returns the original durable receipt even if its originally expected revision is now behind,
**And** no duplicate draft, duplicate event effect or extra revision increment results,
**And** reusing an ID with different content is rejected as idempotency_key_reused; an already accepted event cannot be applied again through another batch.

**Given** the client receives a synchronization response,
**When** it processes the response,
**Then** only a valid matching receipt for the submitted batch and accepted events marks those events acknowledged in a local transaction,
**And** local saving, a successful HTTP status, a server read or an unmatched receipt alone cannot change status from locally saved/pending to server-confirmed,
**And** the draft keeps its original identity, unconfirmed status and expiry, with a clear server-accepted indicator and receipt time distinct from creation time,
**And** missing/mismatched receipts, HTML/login redirects, unexpected content types, network errors and timeouts leave permitted local work unacknowledged and retryable,
**And** failure to commit acknowledgement locally leaves the original immutable batch available for safe retry.

**Given** accepted, still-unexpired draft data,
**When** its owner requests that draft through an authenticated server read,
**Then** the returned fields and revision match the committed PostgreSQL data,
**And** another authenticated identity cannot read/list/adopt the draft or obtain its receipt by changing IDs,
**And** a server read does not silently replace local pending work, count as new authentication, renew expiry or activate a workday,
**And** read/receipt authorization remains separate from the current writer authority required for new mutations.

**Given** a conflicting writer/revision, reused ID with changed payload, invalid/unsupported schema or expired/revoked ordinary access,
**When** the backend rejects synchronization,
**Then** it returns the applicable documented 409, 422, 401 or 403 outcome without partial domain writes,
**And** the client preserves unexpired local work, explains the failure and stops incompatible retries rather than overwriting revisions, minting replacement IDs or claiming success,
**And** authentication recovery follows Stories 1.1/1.2 without discarding unresolved logout,
**And** full multi-device conflict resolution and writer transfer remain E5; this story must expose a blocked conflict honestly without depending on that future UI to preserve work.

**Given** the draft's original creation time and any earlier associated-day expiry known under AD-12,
**When** upload, receipt lookup, read or periodic cleanup occurs,
**Then** the server independently enforces the earliest applicable deadline before deduplication or access, using the original creation instant rather than first upload/receipt time,
**And** invalid/inconsistent temporal metadata cannot extend retention; service date alone never invents an unknown final end,
**And** expired data cannot be uploaded/recreated through an old retry or new batch ID, and an authorized expiry response triggers corresponding local cleanup without a grace-period reset,
**And** all associated private draft, payload, control, event and receipt copies are covered by idempotent startup/periodic deletion while access guards already deny use at expiry,
**And** receipt/identity records used for retry do not become a permanent private archive.

**Given** synchronization or a server read is in flight when explicit logout, local access-storage failure or expiry occurs,
**When** the request later succeeds or the network returns,
**Then** the response cannot unlock/render private content, renew a deadline or resurrect expired payloads,
**And** pending revocation is settled before any new ordinary private traffic; already committed remote effects are reconciled only under valid authority and retention,
**And** unexpired local pending work is preserved for the same owner's permitted recovery, not discarded to make server/client status appear consistent.

**Given** the owner checks the draft's storage status,
**When** data is only local, awaiting a response, failed or acknowledged,
**Then** the UI describes that state in ordinary Norwegian with text and a permitted retry where meaningful,
**And** a server acknowledgement is described as a synchronized working copy, not a historical backup or guarantee against device/volume failure,
**And** private API responses use no-store and private payloads, credentials and original documents are absent from logs, asset caches, repository and CI artifacts.

**Traceability:** E1 fullstack/database and persisted-draft outcome; FR-1 and foundational FR-2/18/20/24 portions; NFR-2/3; UX-DR3/23/38; AD-1–5, AD-6 draft-only data, AD-10 authority/logout, AD-11 initial writer authority (not transfer), AD-12 retention, AD-13 response/origin boundaries, AD-14 immutable schema/build compatibility foundations. This is the first bounded SyncBatch/SyncReceipt path, not acceptance of all E5 recovery scenarios.

**Dependencies and size boundary:** Approved Stories 1.1–1.3. Support only create/synchronize/read of the minimal immutable unconfirmed draft; no concurrent draft editing or merge, file import, source polling, plan confirmation, active driving or mentor data. Use real PostgreSQL 18 transactions and constraints for integration evidence. Initial scope/epoch/receipt DTOs and exact endpoints are story-level design within the six adopted contracts, documented before coding. No whole application schema or generic event-sourcing framework is required. This story is more technically demanding than 1.3; keep the single create-event scope instead of broadening it into E5.

**Implementation evidence:** End-to-end fictional draft creation → sync → authenticated server read; PostgreSQL rollback injection; response-loss retry after reload; acknowledgement-write failure; duplicate event across batches and changed-payload ID reuse; owner/epoch/revision/schema rejection tests; expiry before/at/after deadline including delayed initial upload and earlier day deadline; logout/expiry while response is delayed; purge coverage of every introduced private table/store. Tests are proposed, not run during planning.

**Pilot qualification:** Evidence contributes to E8-D's actual React/FastAPI/PostgreSQL flow. E8-P still requires real target-device/access-gate tests, full-day recovery, all event types, transfer/conflict handling, retention integration and compatible releases. E8-E remains subsequent field evaluation. No historical private-data backups, deployment, implementation or readiness check is authorized by drafting this story.

**Approval:** Approved by the owner on 2026-09-25, preserving scope and criteria and explicitly requiring a valid receipt matching the sent batch before server-confirmed status. Local storage and server acknowledgement remain distinct. The owner instructed proceeding to the next individual story review. Approval concerns planning, not implementation; the approved copy in epics.md is canonical.
