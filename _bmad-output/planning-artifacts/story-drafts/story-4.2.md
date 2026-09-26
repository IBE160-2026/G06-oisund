---
status: approved
created: 2026-09-26
epic: E4
story: '4.2'
type: implementation
authorizedForImplementation: false
approved: true
approvedOn: 2026-09-26
dependencies: ['4.1', '1.4', '2.7', '3.2']
---

## Epic 4: Understand Relevant Notices and Their Sources

This slice delivers central automatic source ingestion, persistent retrieval continuity and an honest source-status surface in the existing private shift overview. It does not yet supply an operational notice list, trip relevance, lifecycle presentation or audio. Later stories consume the captured source facts without requiring this slice to wait for them.

### Story 4.2: Retrieve Notice Source Data Automatically and Show Honest Retrieval Status

As the driver preparing a confirmed working day,
I want the application to retrieve the qualified notice source automatically and show whether retrieval is complete, partial, failed or never successful,
So that I can distinguish available source information from missing updates without manually supplying notices.

**Acceptance Criteria:**

**Given** actual 4.1 evidence supports an adopted source configuration and its retrieval semantics,
**When** the backend starts or resumes eligible pilot-area retrieval,
**Then** fetch through the disruption-data adapter in the existing FastAPI application and centrally schedule checks per source/pilot area, normally around two minutes during active work subject to qualified provider limits,
**And** preparation initiates or joins the shared retrieval without requiring a manually entered notice; multiple views/clients cannot multiply provider polling or create overlapping fetches for the same source scope,
**And** document when polling starts, stops and resumes based on current preparation/active-work demand, keeping that demand separate from operational authority or day completion,
**And** secrets remain server-side; neither browser polling nor an unauthenticated/demo caller can directly trigger uncontrolled provider requests,
**And** missing/negative 4.1 evidence is a blocking qualification/solution decision, not permission to claim live support from fixtures.

**Given** a qualified response contains source notice observations,
**When** the adapter validates and stores them,
**Then** retain the minimum necessary source-namespaced identity, supplied version/order evidence, content, relevance references, validity periods, original-source access and nullable source update time without inventing missing values,
**And** record source observation/fetch metadata separately from operational revisions and client receipt time; no poll changes the confirmed plan, active trip, manual corrections or movement history,
**And** retain sparse closure/expiry evidence without treating this ingestion slice as the completed canonical lifecycle reducer or an operational active-notice list,
**And** do not replace a stored observation solely because a later request returned it later; preserve source ordering evidence for the later lifecycle story, with repeated delivery handled without duplicate ingestion records and no fingerprint-as-order assumption.

**Given** initial baseline loading, delta retrieval or a paginated response,
**When** pages/changes are fetched,
**Then** distinguish collecting/incomplete data from a completely validated retrieval unit according to 4.1's verified source protocol,
**And** atomically commit the accepted observations and corresponding resumable cursor/baseline state in PostgreSQL; never advance the committed resume point past data that was not saved,
**And** an empty delta means no changes in that response, not an empty set of active notices; a full empty source result establishes absence only for its verified source scope/time and coverage, never a general all-clear,
**And** missing/failed pages or invalid records leave the affected result visibly incomplete/failed and cannot clear prior observations or establish closure,
**And** complete-source retrieval does not mean a complete prepared working day or complete real-world disruption coverage.

**Given** a crash, database failure, lost response or backend restart during retrieval,
**When** retrieval resumes,
**Then** continue from the last committed protocol state or perform the qualified baseline rebuild, retaining previously accepted observations and deduplicating safe replay,
**And** persist source state in the actual PostgreSQL database using repeatable migrations limited to this slice's source observations and retrieval state,
**And** reject stale concurrent completion/cursor writes; overlapping startup or retry paths cannot regress a newer committed source generation,
**And** database commit failure cannot advance the successful-retrieval timestamp or be presented as saved source data,
**And** bounded incomplete staging cannot become an indefinite raw response archive.

**Given** timeout, throttling, denied source access, invalid content or a failed refresh after prior success,
**When** automatic retrieval handles the failure,
**Then** record a source-specific failure/partial status, retain the last successful retrieval time and useful prior source facts, and schedule bounded retry/backoff consistent with the qualified provider rules,
**And** report the attempt as failed or delayed rather than indefinitely in progress; a redirect/login document or arbitrary HTTP success with invalid payload is not a successful source refresh,
**And** recovery automatically retries/resumes; network reachability alone or completion of only some pages cannot clear the missing-update warning,
**And** a later completely validated and committed retrieval may update last-success status without claiming that the provider itself is current or comprehensive.

**Given** an authorized owner opens the existing confirmed-shift overview,
**When** source status is requested through the private FastAPI API,
**Then** React displays a concise status for never loaded, retrieval pending, partial/failed, or successful retrieval, with the last successful source retrieval time when known and visible coverage limitations,
**And** before any usable successful retrieval, show Avviksinformasjon utilgjengelig – sjekk originalkilden with a verified source link where available; do not render an empty notice area as no disruptions,
**And** missing source update time cannot be replaced with the retrieval time; successful fetching alone does not create a Senest oppdatert claim for source content,
**And** this slice labels notice relevance/presentation as not yet available and does not publish raw unprocessed observations as operational warnings or imply that a successful fetch makes the whole day ready,
**And** show ordinary Norwegian text/symbols rather than technical cursors, database terms or source exceptions.

**Given** retained source status and a failed client-to-backend refresh, including an access-gate HTML response,
**When** the source-status surface refreshes or reopens,
**Then** keep last known status visibly retained/possibly stale and distinguish its source retrieval time from the client's last successful receipt; an unreachable backend cannot establish current provider health,
**And** a response returning after logout, owner/day change or a newer status cannot expose private context or overwrite the newer view,
**And** reuse IndexedDB for the minimal private day-associated status snapshot if retained; commit before claiming local saving and report storage failure without destroying prior permitted data,
**And** source-status reads do not create operational outbox events or renew authentication, day grants or retention. Full offline shell/day recovery remains E5.

**Given** the status surface, source link or an already-open overview is used in driver context,
**When** shared movement permission changes or a user invokes a restricted action,
**Then** reuse 3.2's permission and approved unknown-speed exceptions; movement closes restricted detail and source access cannot bypass the lock,
**And** automatic status changes never open detail/external pages, steal focus, sound a notice chime or request acknowledgement while driving,
**And** provide labelled status/failure/retry feedback without color alone or repeated announcements for unchanged polling results; preserve the existing focus restoration rules,
**And** this overview status does not implement later active-driving notice placement, staged stop warnings or mentoring exceptions.

**Given** source persistence, private status access and cleanup,
**When** access and lifecycle checks run,
**Then** reuse authenticated server-derived owner/day authority for private views/API responses and reject unauthenticated/demo access; arbitrary request source URLs/configurations cannot become a provider-fetch proxy,
**And** public source cache has a documented bounded refresh/pruning lifecycle separate from AD-12 private-day retention; keep private day associations out of that public cache,
**And** every introduced private snapshot/association follows existing logout locks and the applicable original expiry, without a new clock or permanent history,
**And** retain only source facts needed for this slice/future lifecycle consumption, no private shift payloads or credentials in logs/fixtures; do not delete evidence already required by an unexpired private day through public-cache pruning.

**Traceability:** Automatic retrieval portion of FR-12; source/fetch separation FR-13; source-refresh FR-18 and first-fetch failure FR-19; shared FR-16 for overview/source access. NFR-2/3/4 and relevant NFR-1 status readability; UX-DR14/23/38/39/44. AD-1/3 adapter/backend, AD-4 PostgreSQL, AD-5 source versus operational revisions, AD-7 central qualified polling, AD-8 preserved identity/order evidence, AD-10/12 access/retention and AD-13/14 restart/compatible response boundaries. Full notice lifecycle, relevance and FR-15 audio remain separate required slices.

**Dependencies:** Executed 4.1 with sufficient actual source evidence for the chosen path; approval of its report story is not that evidence. Implemented E1 access/PostgreSQL foundation through 1.4, E2 confirmed overview through 2.7, and 3.2 shared movement/focus rules. No later E4 lifecycle, relevance, audio or E5 full offline story is needed to demonstrate source ingestion and honest overview status. No new provider/host/service is provisioned by this planning step.

**Implementation evidence:** Qualified live-source retrieval separately from labelled fixtures; full/empty/delta/paged/partial/malformed responses, nullable metadata, sparse closure evidence and duplicate/out-of-order delivery; crash before/after cursor commit, failed PostgreSQL write, competing callbacks and restart; throttling/backoff, first failure then recovery, success followed by failure; source versus client outage, late response/logout and storage/expiry faults. Verify central request counts with multiple clients, actual PostgreSQL transactions, private API isolation and accessible movement-governed overview status. Tests are planned, not run.

**Size boundary:** One adapter retrieval path, central scheduling/resume, minimal source observation/status persistence and the existing overview's source-status surface. No lifecycle reduction, material-change/seen/hidden state, per-trip relevance, operational notice list, audio, general synchronization engine or full offline capability. If the qualified source protocol makes this too large for one implementation session, split retrieval/status from cursor/restart work before implementation while preserving the atomic-cursor acceptance boundary; no V1 requirement is removed.

**Pilot qualification:** Repeatable fullstack/PostgreSQL behavior with labelled source fixtures contributes to E8-D. Actual successful retrieval is required evidence in its own right; synthetic/manual data cannot meet that acceptance criterion. E8-P additionally needs qualified coverage and integrated lifecycle/relevance/device/offline/host behavior. E8-E remains later field evaluation. A successful poll or this story's completion is not pilot permission.

**Approval:** Approved by the owner on 2026-09-26 with successful retrieval, complete coverage and actual freshness kept distinct. Partial responses or failures cannot erase previously accepted information. Planning approval only; the approved copy in epics.md is canonical.
