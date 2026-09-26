---
status: approved
created: 2026-09-26
epic: E5
story: '5.2'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.1', '2.8']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

This slice makes one complete verified nonpersonal application build available locally and routes boot to the build required by retained work. It supplies the app-assets part of preparation status. Actual whole-day state restoration/offline activation and complete access-lifetime readiness are subsequent E5 slices, so successful asset verification alone cannot advertise the day as fully offline-ready.

### Story 5.2: Keep a Complete Compatible App Build Available for Offline Opening

As the pilot owner,
I want the application files needed for my prepared or active day verified and available on this device,
So that reopening does not silently depend on a missing file, a login page cached as code or a mixture of incompatible app versions.

**Acceptance Criteria:**

**Given** the current supported application build and permitted preparation,
**When** its local asset set is prepared,
**Then** enumerate the actual nonpersonal resources required by that build, including entry/bootstrap code, dependent/lazy modules, styles, fonts/icons and any implemented runtime assets required by the day flows,
**And** identify build ID, required API/event contract and local storage schema separately from plan/source/server revisions,
**And** use the deployed build's trusted manifest/validation basis rather than declaring success because the current screen happens to load,
**And** cache verified nonpersonal resources in Service Worker/Cache Storage; private plans, notices, source responses, session data, originals and outbox payloads remain outside that asset cache.

**Given** an asset download succeeds, fails, redirects or returns unexpected content,
**When** the staged set is validated,
**Then** check the expected resource identity/build, response type/content and integrity using the documented build validation scheme before accepting it,
**And** reject missing/truncated/wrong-build resources and HTML login/error pages returned in place of code, including misleading HTTP success responses,
**And** resolve the complete resource set before publishing its verified-ready marker; one successful request or a backend cache hit is not local completeness,
**And** retain the preceding usable verified set on interruption, quota failure or validation error; show specific missing/incomplete status and a non-destructive retry,
**And** do not expose raw cache names, hashes or internal exception text as driver instructions.

**Given** downloads/staging and readiness publication span separate browser storage operations,
**When** the browser closes or a write fails at any boundary,
**Then** recovery cannot treat a partial staged cache or an orphaned marker as a complete set,
**And** verify the referenced assets before selecting a build for boot, publishing selection only once the referenced set is complete and valid,
**And** retries reuse valid compatible staged resources without mixing unrelated builds or discarding private day data,
**And** test interrupted download, last-asset failure, failure before/after marker publication and missing resources after an earlier successful verification; readiness must reflect the currently available set.

**Given** a day is prepared and later actually activated through the existing path,
**When** its required application identity is persisted,
**Then** bind the day/recovery record to the verified compatible build it requires without changing its plan, authority, operational outcome or retention,
**And** preserve that required build for an active day and retained pending work; scheduled departure, refresh or a newer network response cannot silently change it,
**And** do not advertise complete app assets if the required build cannot be identified/verified from trustworthy version/schema metadata,
**And** storing the build reference does not itself start the day or create a new day grant, and a grant is not proof that the assets exist locally.

**Given** a complete retained required build and network loss or an outer Access login response,
**When** the browser reopens the application,
**Then** route to that one coherent locally verified build without requiring fresh network resources, including lazy routes/resources needed by the implemented flows,
**And** before private rendering apply existing local logout/revocation/storage/expiry and 5.1 day-scope checks; cached executable code is not authority to expose private content,
**And** the bounded test here proves coherent application entry and guarded access, not full active-day restoration, offline start or successful future synchronization,
**And** test browser close/reopen offline and controlled Access-blocked responses separately; reconnect cannot replace a selected required build with a login document or mixed newer assets,
**And** app-entry success cannot be used as evidence that GPS, source updates, sound, private data coverage or access lifetime is sufficient.

**Given** a successor build/worker becomes installed or active while a retained day still requires the previous build,
**When** all tabs close and the browser opens again,
**Then** worker installation/activation alone must not switch that day's app version, run a new incompatible schema migration or delete its required files,
**And** use explicit build-aware boot routing to retain one coherent required version; do not rely solely on a waiting-worker assumption or absence of a force-reload call,
**And** coordinate concurrent tabs/workers for publication/selection so one cannot invalidate the resources another retained active context requires,
**And** test a labelled old/new build pair with differing assets/contracts and a newly activated worker; retained work still boots its required build,
**And** controlled between-day release activation, backend compatibility/migration/rollback and writer transfer remain later E5 work under AD-11/14; this slice supplies their necessary retention/routing invariant.

**Given** required assets are missing, corrupted, evicted or incompatible,
**When** offline opening cannot safely select a complete compatible build,
**Then** use the available minimal recovery entry to explain unavailable application files and preserve private data rather than running a random old/new mixture or clearing storage as repair,
**And** a permitted retry can replenish the exact required compatible set when reachable; it cannot silently substitute an incompatible build or extend data/authority deadlines,
**And** report the limits honestly: total browser storage/worker eviction may also remove the recovery entry, so do not promise an offline recovery screen when no executable resources remain,
**And** test partial eviction separately from complete browser-data loss; do not fabricate recovered private work when that data has also been removed,
**And** browser storage remains evictable; a successful preparation check is not a guarantee of future physical storage survival.

**Given** preparation presents plan, data, application and access information,
**When** readiness is refreshed or a plan revision adds later activities,
**Then** show separately confirmed plan status, per-trip downloaded data coverage from 2.8, source/notice availability and freshness, verified app-file status, and known authority/deadline limitations from 5.1,
**And** a partial day's data never yields Hele dagen klargjort even when the app asset set is complete,
**And** changed plan/build references invalidate affected coverage claims without silently deleting still-usable data or overriding manual corrections,
**And** app-assets success alone gives no global offline-ready/pilot-ready claim; full day activation/recovery and actual Access-token lifetime coverage remain unqualified until their later integration,
**And** verify the independent cases complete assets/incomplete data, complete data/incomplete assets, confirmed plan/unknown source coverage and valid grant/ordinary access expired with prepared-versus-active scope,
**And** retain readable text/symbol statuses, keyboard access and shared movement restrictions without a modal demand to repair preparation during driving.

**Given** obsolete staging/resources or private build references are cleaned up,
**When** pruning runs,
**Then** preserve resources still required by active/unexpired retained work and compatible pending recovery; do not prune merely because two releases exist or seven days elapsed since deployment,
**And** keep one selected build and a staged successor normally, with additional nonpersonal code retained only when existing work actually requires it,
**And** private day/build associations follow their original AD-12 expiry, while nonpersonal app-code cache has its separate bounded lifecycle,
**And** cleanup/retry cannot remove pending logout, immutable outboxes, manual choices, notice state or data as a workaround for cache failure,
**And** do not introduce private historical backups, mirrored raw files or a permanent private recovery archive.

**Given** preparation/boot status is persisted or served,
**When** fullstack/access checks apply,
**Then** retain non-secret device-local asset verification metadata locally; a server receipt cannot assert that a browser resource is actually present,
**And** reuse the existing authenticated FastAPI/PostgreSQL day/version scope for any synchronized private association, introducing only fields needed by this slice and preserving matching-receipt semantics,
**And** allow no credentialed demo-to-private cache/API reuse, and never save credentials, Access pages or private responses as app assets,
**And** report failed local or backend writes without false durable/server confirmation; no per-asset operational event spam, new service or new authentication model is required.

**Traceability:** Asset/readiness prerequisites of FR-17/20, continuity FR-1 and source/availability portion of FR-18/19, private metadata FR-24. NFR-2/3/4 and readable status NFR-1; UX-DR3/23/38/44. AD-2 separated readiness and nonpersonal assets/private IndexedDB, AD-5 separate build/domain identities, AD-10 access before private rendering, AD-11 tab/worker coordination, AD-12 retention/eviction limits, AD-13 Access-response separation and AD-14 required-build coherent boot/retention. Full source/device qualification is not supplied by asset tests.

**Dependencies:** Implemented 5.1 bounded authority and existing E1–E4 private app/data/version state; 2.8 per-trip bundle coverage. Uses the built app's actual resource graph, with controlled second-build fixtures for routing tests. Does not require a future migration UI, generalized state recovery, writer transfer or E6/E7 implementation; later features must extend the required resource set when introduced. No live provisioning/deployment is needed for local controlled boot tests.

**Implementation evidence:** Complete/missing/lazy assets, wrong build/type/hash, login HTML, network and quota failures, staging/marker crash boundaries, old/new worker activation after all tabs close, parallel tab selection, partial eviction and complete storage-loss distinction; guarded offline entry, logout and expiry, preserved private/outbox data, independent plan/data/assets/access status and reference-aware cleanup. Actual Lenovo/Brave storage/restart and outer-gate behavior remain separate target qualification. Tests are specified, not executed during planning.

**Size boundary:** Verified nonpersonal build preparation, required-build boot routing and separate app-assets status. No complete day-state restoration/offline activation, Access renewal preflight, new release activation UX, generalized migrations/rollback, sync reconciliation, writer transfer or new PDF/mentor functionality. The existing V1 offline requirement remains assigned to the subsequent integrated slices rather than claimed by a cached shell.

**Pilot qualification:** Repeatable local build/cache failure tests contribute to E8-D. E8-P needs actual Lenovo/Brave close/restart/eviction behavior, integrated whole-day state/authority and Access-expiry recovery; a verified asset manifest alone is insufficient. E8-E remains subsequent field evaluation.

**Approval:** Approved by the owner on 2026-09-26 with the stated scope: readiness requires a complete, verified compatible asset set; updates or repair cannot delete private work or bypass access rules. Planning approval only; the approved copy in epics.md is canonical.
