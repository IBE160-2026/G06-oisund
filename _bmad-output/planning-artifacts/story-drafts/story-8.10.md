---
status: approved
created: 2026-09-27
epic: E8
story: '8.10'
type: qualification
approved: true
approvedOn: 2026-09-27
dependencies: ['5.11', '5.12', '5.13', '6.10', '8.4', '8.5', '8.9']
---

### Story 8.10: Qualify Host Recovery, Resource Use and Compatible Release Changes

As the owner operating the pilot service,
I want measured evidence that the actual Windows host recovers predictably and a concrete release transition preserves retained work on Lenovo/Brave,
So that host interruptions and updates have known limits without exposing private data, losing pending work or silently extending authority.

**Acceptance Criteria:**

**Given** the implemented 8.4 package, 8.5 ingress and 5.11/5.12 release contracts,
**When** the bounded qualification setup is recorded,
**Then** identify the actual Windows hardware, OS/Docker versions, five-service Compose configuration, resource/power settings, home-network path and actual tablet/browser, with versioned old/new client, server, image and storage-schema artifacts,
**And** use an isolated permitted test deployment with fictional retained work and the real PostgreSQL 18 engine; keep fault controls and fixtures out of the operational service. Do not run two independent operational databases behind the same live route,
**And** reuse valid prior evidence, stating actual versus induced conditions, tested duration and missing prerequisites. Pin one concrete old/new release and storage transition rather than claiming generic future compatibility,
**And** distinguish planned test steps from performed observations. This story neither changes the adopted host/provider choice nor requires a new hosting platform or historical private backup.

**Given** retained day state, source cursor/baseline, pending or accepted-but-unacknowledged batches and original deadlines,
**When** the actual host undergoes a full Windows restart with deliberately delayed sign-in,
**Then** record observed service-unavailability, Windows sign-in, Docker startup and actual application-ready milestones with their time basis, counting the entire interval as downtime; missing observations remain unknown,
**And** verify application/database/schema readiness and a working authenticated request/receipt path, not just a running container or open port. Document the accepted lack of unattended pre-sign-in startup,
**And** test a locked screen separately from sleep/shutdown, and exercise home-network/tunnel interruption and recovery independently of mobile-client connectivity. The prepared tablet must show actual offline/access/source/sync status rather than claim continuous server availability,
**And** verify retained database facts, immutable receipts and source baseline survive ordinary restart; polling and cleanup resume without duplicate effects or a second unintended poller,
**And** preserve original source update/retrieval times until a qualifying fetch occurs, distinguishing a source still unavailable from successful refresh. Process startup cannot mark client work server-confirmed,
**And** cross an applicable expiry during interruption: deny expired data before use even before background purge, and never restart ordinary login, day grants, data deadlines or notice freshness as a recovery grace period.

**Given** an unavailable database, partial startup or running but unresponsive service,
**When** the operator follows the actual diagnosis/recovery runbook,
**Then** verify failure is visible, readiness is withheld appropriately and the documented bounded restart/reconnect procedure recovers compatible services without clearing working volumes or browser storage,
**And** distinguish configured restart policy from observed recovery; a health check alone is not an automatic hung-process restart mechanism,
**And** verify provider protection and private/demo isolation remain effective during partial startup/recovery. No exposed private host port, Access bypass or demo relay becomes a repair path,
**And** inspect interruption cleanup of temporary import/OCR copies, logs and artifacts without retaining private payloads or claiming forensic/provider erasure from local deletion,
**And** record permanent volume/device loss as the accepted possible loss of unsynchronized or unbacked-up work; no private snapshot, archived WAL or recreated old state is introduced to make recovery appear successful.

**Given** the actual desktop with explicit CPU/memory limits and one OCR job at a time,
**When** idle operation, representative polling/synchronization/demo traffic and a bounded representative anonymized OCR workload are observed,
**Then** record actual duration, workload/input size, CPU/memory use, request/processing delays and failures, including the effect on the owner's ordinary desktop use under stated conditions,
**And** verify one-job concurrency, bounded resource behavior, no continuous builds/watchers and continued status/cleanup handling during resource pressure. Successful work may not conceal dropped requests, duplicated jobs or retained temporary originals,
**And** document noise observations, ambient conditions, measurement method and its limits, separating any instrument measurement from the owner's listening/usability judgement. Do not invent a decibel limit, throughput guarantee or acceptable result from configured limits alone. Any reviewer assessment must be grounded in the stated method and actual observations, distinct from the owner acceptability decision,
**And** record the owner's explicit judgement of acceptable desktop noise/resource impact against the stated use conditions. If acceptability is unassessed or disputed, keep that part unresolved; an efficient-looking metric is not owner acceptance,
**And** resource/availability/noise failure requires a separate solution decision within AD-13, not automatic Linux/cloud migration, loosened security, increased retention or a passed host gate.

**Given** an actual retained client with unexpired work and a concrete successor backend/schema,
**When** compatibility is exercised through the actual protected path and PostgreSQL,
**Then** run the older executable client, not merely new tests emitting old-looking requests, and verify both its response interpretation and the resulting database/state/receipt effects,
**And** cover old immutable batches including a lost receipt across update, source/notice versions and unknown metadata, recovery/errors, stale writer/revision, pending logout and payload-free original-outcome lookup versus new closure receipt,
**And** retain E6 role/person/block/pin and permitted accompanied evidence plus E7 terminal/review/summary semantics; a representation change cannot invent provenance, open guiding controls, resume a terminal day or restore trimmed information,
**And** preserve original supported IDs/payloads, deadlines, writer scope and deduplication across server migration. Required contracts stay supported through the affected data's actual expiry, not a fixed release count or seven days from deployment; lack of recent traffic does not prove an offline client is gone,
**And** include declared retention-boundary cases and multiple still-required client formats where applicable, marking accelerated expiry tests as such rather than actual elapsed observations,
**And** a required contract failure blocks rollout to the affected retained work. A minimum client for a new day cannot revoke continuation/settlement for an already authorized day, and a new decoder cannot resolve 5.4/7.1 timing uncertainty.

**Given** a complete staged successor on Lenovo/Brave and an active day requiring its existing build,
**When** all tabs close, a waiting Service Worker activates and the app/tablet reopens offline or with Access expired,
**Then** verify the active day still boots its required coherent build without an unapproved app/schema switch. Worker activation, downloaded assets and user-accepted version change remain separate facts,
**And** test partial/wrong-build assets, login HTML in place of an asset and missing/evicted required files: show the appropriate bounded failure and preserve private work; never run a mixed build or clear storage as repair,
**And** between days, test accepting, postponing and blocking the specific verified update after checking pending work, locks, active days in other tabs, transfer state and a supported migration path. Planned finishing time or another tab's main menu does not prove the day ended,
**And** preserve private access guards and pending revocation before any retained content or traffic, including history navigation and late callbacks. Update or Access renewal alone cannot unlock the old day or discard an unresolved logout,
**And** separately verify the ordinary-PC fictional demo still loads and resets after the package change without gaining private access. This is bounded release regression, not a new assessment-availability or E8-D decision.

**Given** an accepted local/backend migration or a proposed rollback,
**When** interruption, quota/write failure, a blocked database upgrade or competing tabs occurs at its persisted boundaries,
**Then** verify documented transactional recovery or the explicit recoverable states of a necessary multi-step transition, without reporting a partially migrated combination as ready,
**And** compare preserved facts before/after: manual choices, actual role/context, notice seen/hidden/audio state, movement history, immutable batches, conflicts/intake, pending logout, grants/writer epochs, closure fences, first-review state and original expiry,
**And** ensure repeated callbacks/restart cannot migrate twice, invent a new startup exemption, replay old sound or turn pending work into acknowledged work. Expired copies are removed before use, including bounded migration staging,
**And** allow code rollback only with verified storage/contract compatibility. An incompatible downgrade is blocked with an explicit non-destructive recovery path; do not restore a private historical snapshot or claim a missing executable path exists,
**And** retain complete nonpersonal assets/formats still required by actual unexpired work, normally one selected build and a staged successor. Additional necessary code retention does not authorize extra private data retention,
**And** a failed compatibility/migration result remains a release blocker until repaired and rechecked or addressed through an explicit solution decision consistent with adopted boundaries.

**Given** host/resource and release cases have observed outcomes,
**When** the consolidated report/runbook update is completed,
**Then** list passed, failed, blocked and not-run cases, actual outage/workload durations, measured observations versus fixtures, tested version combinations and remaining operator actions/limitations,
**And** tie each finding to its requirement, owning implementation story and any owner decision, with targeted revalidation required after relevant host/configuration/build changes,
**And** retain sanitized results and reproducible procedures, not private originals, credentials, database dumps or a permanent operational archive,
**And** keep 5.4/7.1 expressly unresolved until its own evidenced solution decision. Host timestamps, a changed clock or successful deployment do not establish disconnected activation/end timing,
**And** provide evidence for the host/deployment and release parts of E8-P only. Report completion, successful startup or a compatible release alone does not grant actual-shift permission; E8-D/P/E remain separate decisions.

**Traceability:** E8-P access/deployment and release gates; AD-13 Windows/Docker startup, private/demo boundary, resource/noise and portable operation; AD-14 retained-client support, coherent boot, accepted activation, migration and compatible rollback. AD-2/4/5/6/7/8/9/10/11/12 preservation, cleanup, authority and expiry remain binding. Supporting FR-1/17–25 and retained E1–E7 behavior, NFR-1–4, UX-DR3/14/19/23/24/26–39/44. No AD-1–AD-14 choice is changed.

**Dependencies:** Implemented 8.4 runtime, 8.5 protected access, 5.11/5.12 release paths, 5.13 closure protocol, full E6/E7 retained-state extensions and the existing 8.9 continuity harness/evidence. Actual Windows host, Lenovo/Brave, controlled network/reboot access and reproducible old/new artifacts are execution prerequisites. No future E8-P decision or actual pilot shift is needed for controlled testing; missing artifacts or test access remain blocked.

**Size boundary:** One bounded host/resource report and qualification of one concrete old/new release transition, reusing existing test/runbook material. No new deployment platform, update engine, monitoring service, backup scheme, host migration or full replay of 8.7–8.9. Functional repairs remain with owning stories. Predetermine representative workloads and observation windows; retain missing required evidence as incomplete if another session is needed.

**Qualification boundary:** Story planning only. No host restart, network disruption, service change, migration, deployment, hardware test, provisioning or readiness/final-validation workflow is performed now, and no E8-D/P/E outcome is issued.

**Approval:** Approved by the owner on 2026-09-27 as scoped: document measured downtime and the concrete release transition, including active-day and pending-work outcomes. Noise assessment must use the stated measurement method and actual observations, with owner acceptability separately recorded. Planning approval only; the approved copy in epics.md is canonical.
