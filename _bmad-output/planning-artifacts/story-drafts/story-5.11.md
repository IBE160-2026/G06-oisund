---
status: approved
created: 2026-09-26
epic: E5
story: '5.11'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.10', '5.2', '5.1', '1.4']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

This slice preserves the required server contract for retained application builds and their unexpired work across a backend update. It covers both request acceptance and responses the actual retained client can use. Browser build activation/local migrations and AD-12 terminal settlement remain separate slices. No deployment occurs in this planning step.

### Story 5.11: Keep Retained Working Days Compatible with a New Backend

As the pilot owner,
I want the app version holding my working day and pending changes to remain usable with an updated backend through the affected data's expiry,
So that a server update does not strand valid work, break logout or force me to replace the active day's app.

**Acceptance Criteria:**

**Given** retained E1–E5 work and its required application build/contracts,
**When** a successor backend is prepared,
**Then** identify the builds, API/event formats and recovery/response contracts still required by that work, separately from local storage schema, plan revision, server revision and writer epoch,
**And** pin and record the tested release artifacts/dependency versions so the tested old client and new backend can be reproduced with fictional fixtures,
**And** retain support through the affected data's actual AD-12 expiry, not merely the last two releases, seven days after deployment or time since the last heartbeat,
**And** account for disconnected clients and pending work; absence of recent traffic is not proof that the required contract is unused. Document what establishes safe retirement and leave it unsupported as a retirement decision when relevant expiry/usage bounds are unresolved,
**And** compatibility metadata/code retention must not extend private data retention, duplicate private payloads into an archive or grant broader authority.

**Given** an actual retained coherent client and valid existing owner/day authority,
**When** it calls the successor backend in a controlled compatibility test,
**Then** preserve the contracts it needs for retained draft/plan/day recovery, data/source/notice updates, immutable event submission, receipts, errors, day access and logout/revocation,
**And** verify old-client interpretation and resulting state, not only successful HTTP status or a backend parser accepting its request,
**And** preserve meaningful distinctions for conflict, pending/unknown outcome, invalid payload, expired work, application access failure and outer-gate failure; no generic success/error fallback may erase their handling,
**And** newer responses cannot silently omit information needed for old-client manual choices, uncertainty, exact notice versions or access scope,
**And** source retrieval remains separate from operational revisions and update success cannot acknowledge pending events.

**Given** an immutable batch was saved before the backend update or accepted before a lost response,
**When** the retained client submits/retries it against the new backend,
**Then** interpret its original supported schema without changing batch/event IDs, payload content, ordering, hashes or expected-revision meaning to make it fit the new format,
**And** under current authorization return an existing identical receipt for prior acceptance without applying effects or incrementing revisions again, including when the original expected revision is behind,
**And** reject changed content under a reused identity, unauthorized old-epoch mutations and invalid/unsupported payloads without partial writes; read-only receipt lookup retains its separate authorization rule,
**And** maintain one stable in-flight batch per day and preserve unresolved work on error; an update cannot turn transport receipts from 5.10 into operational acknowledgements,
**And** 5.4's unverifiable post-expiry start remains unresolved across the update rather than being reclassified as accepted by a new decoder.

**Given** the backend schema or stored representation changes for the successor,
**When** the controlled migration and compatibility checks run against PostgreSQL,
**Then** preserve ownership, original grant/data deadlines, domain identities, event/receipt deduplication, writer epochs and necessary recovery/conflict references,
**And** introduce only schema changes needed by the concrete version transition and use transactional migration where possible, with documented/tested recovery for multi-step exceptions,
**And** old-contract reads/writes operate correctly against the resulting schema while required; a database migration cannot silently change operational meaning or reset client-visible revision relationships,
**And** injected interruption/failure does not publish a partially compatible backend as ready or require clearing private data as repair,
**And** do not introduce historical private database backups/snapshots/archived WAL as the rollback mechanism; code rollback is allowed only against a verified compatible storage schema, otherwise stop and use an explicit non-destructive recovery path.

**Given** an ordinary-sign-in expiry, explicit logout/revocation or data expiry occurs around a version transition,
**When** either supported client version invokes the relevant operation,
**Then** continue only the already active authorized day under the original 5.1 bounds, while denying a prepared/new-day start after ordinary expiry without renewed authorization,
**And** preserve immediate private locking and pending revocation across old/new logout contracts; an update cannot unlock retained work or process other private traffic first,
**And** authenticate and apply scope/expiry checks before deduplication/receipt retrieval; compatibility support never permits resurrection of expired or terminal work,
**And** retain protected API outcomes understood by the retained client so it can distinguish required cleanup from temporary unavailability without deleting recoverable unexpired work,
**And** test expiry before/at/after its real boundary independently of release date; return the correct authorized expired/gone outcome rather than using contract removal as a substitute for retention enforcement.

**Given** a newer client accesses retained work through the successor backend,
**When** contract-level recovery is requested,
**Then** recover permitted existing drafts, current-day state, pending/receipt/conflict evidence and retained read-only representations with original identities and deadlines intact,
**And** preserve legacy unknown values and source/manual provenance instead of filling new required-looking fields by guessing,
**And** use controlled terminal/read-only fixtures where E7 screens do not yet exist; the test proves API semantics, not completed E7 summary or PDF functionality,
**And** local stored-format migration and owner-accepted app activation remain a later story; backend recovery success alone is not evidence that browser migration worked,
**And** never replace newer unsynchronized local work through a generic server refresh while testing either client generation.

**Given** a required retained contract is unsupported or cannot pass compatibility checks,
**When** an ordinary successor release is evaluated or a runtime mismatch is encountered,
**Then** do not qualify that release for replacing the backend serving the affected retained work until compatibility is restored or an explicit owner solution decision is made within adopted boundaries,
**And** report unsupported scope clearly without silently discarding work, dropping fields, creating replacement identities, forcing an active-day client upgrade or pretending a blocked release passed,
**And** a minimum new client may be required before authorizing a new day, but that check must not revoke existing authorized active-day continuation or bounded settlement,
**And** keep actual release activation between days with a pending-work check under AD-14; this story defines/tests the compatibility prerequisite and does not deploy or implement the browser activation flow,
**And** keep support bounded to actually required contracts; no generic multi-version platform or speculative future adapters are added.

**Given** reproducible old/new artifacts and a real PostgreSQL database,
**When** compatibility evidence is produced,
**Then** run the retained actual client contract against the successor backend/schema and test the newer client against retained data; a new test client using only new DTOs is insufficient,
**And** cover unchanged and materially changed notices, null metadata, old-format immutable batches, receipt loss across upgrade, same-ID changed content, stale writer/revision, review-intake versus operational receipt and pending logout,
**And** include ordinary expiry with valid active-day grant, denied new-day start, original data expiry, multiple retained releases still legitimately needed, and work outliving seven days from a deployment,
**And** inject migration interruption and test declared code/schema rollback combinations, recording which combinations passed, failed or remain untested,
**And** verify actual client behavior and PostgreSQL effects with anonymized/fictional data, without logging private payloads or claiming fixture success establishes live source/device compatibility.

**Traceability:** Version-continuity portions of FR-1/17/18/20/24 and retained feature contracts FR-2–16/19; NFR-2/3/4 and readable errors NFR-1. UX-DR3/19/23/38/44; AD-2 durable local work, AD-3/4 client/backend and PostgreSQL boundary, AD-5 immutable schemas/receipts, AD-8 notice versions, AD-10/11 access/authority, AD-12 actual expiry/no private historical backups, AD-13 portable protected backend and AD-14 compatibility through expiry. Source/device and future E6/E7 behavior remain separately qualified.

**Dependencies:** Implemented E1–E5 contracts through 5.10 and 5.2 required-build metadata. Use the existing working build as the retained artifact and a controlled concrete successor transition for compatibility evidence. Browser migration/activation UI and E6/E7 production screens are not prerequisites; later new features must extend this contract suite when introduced.

**Size boundary:** Compatibility support and evidence for one concrete old/new backend transition, covering the existing required client contracts. No deployment, release orchestration platform, browser migration/activation UI, new feature families, blanket lifetime support or private disaster-recovery archive.

**Pilot qualification:** Reproducible actual-client/FastAPI/PostgreSQL compatibility tests contribute to E8-D. E8-P requires the actual retained tablet build against the release candidate, including gated access, pending work and integrated recovery. E8-E remains later field evaluation. No implementation, migrations, deployment or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 with compatibility tied to actual data lifetime and verified using a real retained client, including lost receipts and pending logout. Required contract failures block release. Planning approval only; the approved copy in epics.md is canonical.
