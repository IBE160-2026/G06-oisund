---
status: approved
created: 2026-09-27
epic: E8
story: '8.4'
type: implementation
approved: true
approvedOn: 2026-09-27
dependencies: ['8.3', '5.11', '5.12', '5.13']
---

### Story 8.4: Run the Adopted Portable Service Stack with Controlled Restart and Data Preservation

As the project owner operating the delivered assistant,
I want a reproducible, versioned service setup that starts and recovers predictably on the Windows desktop,
So that I can run the private application and isolated demo without depending on development servers or losing stored work during ordinary service restarts.

**Acceptance Criteria:**

**Given** the implemented application and the adopted AD-13 host choice,
**When** the runtime package is built and configured,
**Then** supply versioned images and a portable Compose definition for exactly the adopted service roles: cloudflared, private-web, demo-web, api and db, using Docker Desktop Linux containers on the Windows desktop and PostgreSQL 18,
**And** build the production frontend/backend artifacts with pinned dependencies and identify image/build, API/event and schema versions. Do not run continuous development watchers or rebuild loops as normal service operation,
**And** separate environment configuration, externally supplied secrets and named working volumes from images/source. Do not bake credentials, uploaded files, private database snapshots or hardcoded owner-specific Windows paths into release artifacts,
**And** document the required host/software prerequisites and a reproducible configure/start/status/stop procedure, keeping ordinary stop/restart distinct from destructive test-volume reset,
**And** keep the tunnel route disabled/unpublished until the later protected-ingress work has verified its prerequisites. Missing credentials or route configuration must not trigger an unprotected direct-port fallback. This story's runnable local service package does not depend on provisioning a domain, account or public route.

**Given** the five service roles and their configured networks,
**When** private and demo requests are routed in the isolated verification setup,
**Then** private-web serves the private client and its same-origin API route; only api connects to the PostgreSQL working database, while demo-web serves static fictional assets with no private backend or database access,
**And** restrict the connector to intended web ingress services and reject unmatched host routes. Demo requests cannot use the private API proxy or reach api/db through container networks,
**And** do not expose pilot database/API/private HTTP host ports as a way around the future Access boundary. Use the isolated qualification setup for local probes without enabling production exposure,
**And** verify allowed and denied paths through actual requests/network checks, not just Compose declarations or hidden UI controls. Retain host-only cookies and exact-origin/CORS protections; no demo-to-private credential relay is introduced,
**And** document that actual named-tunnel, JWT, provider handling and browser-trusted external HTTPS evidence remains the subsequent ingress qualification, not a pass inferred from local connectivity.

**Given** a fresh empty test working volume or an existing compatible database,
**When** services start,
**Then** enforce database and schema readiness before the API accepts dependent traffic; apply the existing versioned migration procedure without racing multiple migration attempts or claiming ready after failure,
**And** missing/invalid configuration, unavailable database or unsupported schema yields clear operator diagnostics without credentials/private payloads. Partial startup cannot report the complete application healthy,
**And** use the adopted unless-stopped policy for long-running services and distinguish service liveness from useful readiness. A health check alone must not be described as automatically restarting a hung process,
**And** provide an explicit documented diagnosis/restart procedure for a running but unresponsive service; never clear the database or browser storage as the standard repair step,
**And** reconnect application services after temporary database/network interruption using existing idempotency and source-state contracts, without a second source poller, duplicate operational effects or manual-choice overwrite.

**Given** fictional retained work, an immutable pending/accepted batch and persisted source/cleanup state,
**When** the API, web services, database container or Docker runtime is stopped and restarted without deleting working volumes,
**Then** preserve the PostgreSQL working data and resume the existing receipt/revision semantics. Retry of the same accepted batch returns its original authorized receipt, rather than applying another change,
**And** restore polling/cleanup from their stored state; expired data is denied before use independently of scheduled purge. A container restart cannot restart day retention, ordinary login, a grant or notice freshness,
**And** preserve the separation between a client still running offline and the unavailable host. Host recovery does not manufacture a source update or immediately establish that pending client work is confirmed,
**And** test recovery using the actual packaged services and 8.3's fictional evidence path, including database unavailability, delayed response and service restart. Record missing or failed recovery rather than treating container status as proof of application correctness,
**And** keep normal PostgreSQL transaction/recovery machinery while excluding historical private backups, archived WAL and snapshot-based rollback. Working-volume loss remains the adopted accepted data-loss risk, not something this restart story claims to solve.

**Given** a package update or rollback is prepared,
**When** the owner follows the deployment procedure in the isolated environment,
**Then** reuse 5.11/5.12 and AD-14 compatibility checks: identify supported retained clients, required old assets/contracts and migration compatibility before switching server images,
**And** an image change cannot authorize a browser build switch or force a new-day login into an existing active day. Staged client assets remain distinct from accepted activation,
**And** failed migration or incompatible rollback stops with preserved data and an explicit recovery path; never automatically downgrade storage, reset volumes or restore a historical private snapshot,
**And** document the ordinary between-days update check including pending work. This packages the existing release contracts; complete old-client/target-device qualification remains an E8-P obligation.

**Given** the owner intends to operate on the Windows desktop,
**When** the host starts or undergoes a full reboot,
**Then** document and test the adopted limitation that Windows sign-in is required before Docker Desktop starts, and verify application-service recovery after sign-in rather than promising unattended pre-login availability,
**And** record the interval from full Windows restart through sign-in and Docker Desktop startup as service downtime, extending it until the required application services are actually ready. Record observed restart/unavailability, sign-in, runtime-start and application-ready milestones with their time basis; a missing observation remains unknown rather than zero downtime,
**And** on recovery retain the original source update/retrieval timestamps and show pending/failed freshness until an actual qualifying fetch supports a new retrieval status. Resume polling, pending work and cleanup without extending login/day/data deadlines, including deadlines that passed during the interruption,
**And** document host-awake requirements and verify that an ordinary screen lock does not itself stop the tested service setup. Sleep/shutdown or home-network loss invokes existing prepared-client offline behavior, not continuous-server availability,
**And** apply explicit CPU/memory bounds and one OCR job at a time, without inventing a throughput/noise guarantee. Record configured limits and any initialization/resource failure,
**And** leave measured resource/noise acceptability, full home-network failure/recovery and actual Lenovo/Brave behavior for their target-environment qualification, retaining failures as open blockers where relevant,
**And** portable configuration must not require an acquired Linux host or paid server. Preserve the stable-origin/single-operational-database rule for any later migration; this story performs no host migration.

**Given** runtime volumes, temporary files, logs and build artifacts,
**When** their configuration and ordinary recovery are inspected,
**Then** keep private data in the intended working/temporary locations only, use existing original-file cleanup on success/failure/interruption, and avoid persistent request-body dumps or raw OCR/GPS archives,
**And** preserve the AD-12 all-copy deletion behavior through packaged restarts; neither logs, images, crash diagnostics nor test artifacts become an undeclared private archive,
**And** use fictional fixtures for verification and scrub secret-bearing diagnostics before documenting them. Keep test helpers and fault controls out of the production runtime,
**And** do not claim local cleanup proves Cloudflare/provider erasure or forensic erasure. Provider upload/logging handling still requires the separate adopted qualification before real files.

**Given** a clean isolated test setup and a documented Windows desktop configuration,
**When** the package is verified,
**Then** demonstrate reproducible build/start, schema readiness, a real private request through FastAPI/PostgreSQL and isolated demo access using 8.3 fixtures,
**And** test missing configuration, unavailable database, failed migration, allowed/denied network paths, restart with retained volume, an unresponsive-service recovery procedure and rejected destructive/incompatible recovery,
**And** test service startup after Windows sign-in/reboot, screen lock, configured resource bounds and single OCR concurrency; record the environment and observed outcomes without extrapolating to an untested host,
**And** deliberately delay sign-in after a full Windows restart and record the full interruption through actual application readiness. Retain old source data, pending work and a deadline crossing the outage; verify no fresh-data claim from restart, no receipt claim from process startup and no grace period or deadline extension. Test recovery while the source remains unavailable as well as after a successful qualifying refresh,
**And** provide a concise runbook, version manifest and passed/failed/blocked/not-run report with links to sanitized evidence. Never report a route published, Access configured, noise acceptable or E8-P passed based solely on this package,
**And** report any conflict with the adopted topology or runtime limitations for an explicit owner decision; do not silently change hosting/security/backup choices to make startup pass.

**Traceability:** AD-13 portable five-service runtime and desktop restart/resource obligations; AD-3/4 actual application/PostgreSQL packaging, AD-2/5/7/8 stored-state and receipt continuity, AD-6 temporary import handling, AD-10/11 private scope/writer preservation, AD-12 cleanup/no private backups and AD-14 compatible releases. Supporting FR-1/17/18/20/24/25 and NFR-2/3/4, fullstack/database delivery and E8-D reproducibility; UX-DR23/37/44 remain preserved by the packaged features. All AD-1–AD-14 remain unchanged.

**Dependencies:** Implemented application and separate demo, 8.3 repeatable fictional fullstack evidence, E5 release/recovery/settlement contracts through 5.13 and E7 full lifecycle. An isolated local setup suffices without later public ingress or assessment scheduling. Host/software availability is an execution prerequisite to record explicitly, not permission to simulate a successful reboot test.

**Size boundary:** The adopted service package, local network boundaries and operator start/restart/update runbook with bounded fictional recovery evidence. No DNS/tunnel/Access provisioning, live publication, provider-policy approval, full resource/noise qualification, field evaluation or new business/synchronization logic. Protected external ingress and assessment availability remain separate required E8 slices; no pilot permission is granted here.

**Qualification boundary:** Contributes runtime/reproducibility evidence to E8-D and specific recorded host cases to later E8-P assessment; neither gate passes automatically. Actual private ingress, provider handling, target-device recovery, source behavior and release qualification remain mandatory before pilot use; E8-E follows afterward. The 5.4/7.1 timing decisions remain open. This is a planning draft only: no services, accounts, containers, migrations, provisioning or deployment are started in this step.

**Approval:** Approved by the owner on 2026-09-27 with the full-Windows-restart interval through sign-in and Docker Desktop startup explicitly documented as downtime; actual service readiness determines the end of the interruption. Recovery must resume work without presenting retained source data as fresh or extending deadlines. Added delayed-sign-in, unavailable-source and deadline-crossing test cases with observed timing milestones. Planning approval only; the approved copy in epics.md is canonical.
