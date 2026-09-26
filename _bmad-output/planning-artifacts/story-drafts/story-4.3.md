---
status: approved
created: 2026-09-26
epic: E4
story: '4.3'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['4.2']
---

## Epic 4: Understand Relevant Notices and Their Sources

This slice turns accepted source observations into trustworthy canonical notice versions and source lifecycle facts. It supplies the private read API with stable identity and evidence, independently testable before later relevance and presentation stories. Client seen/registered/hidden state, its ten-minute closure display and audio are separate required slices, not backend source facts.

### Story 4.3: Preserve Notice Identity and Source Lifecycle Without False Updates or Closure

As the driver,
I want the application to distinguish genuine source changes and confirmed endings from repeated, old or missing source records,
So that notices do not falsely become new, disappear as resolved or return as active after closure.

**Acceptance Criteria:**

**Given** validated observations committed by 4.2 and identity/version rules supported by actual 4.1 evidence,
**When** the backend normalizes them,
**Then** represent each supported source incident with stable source-namespaced identity and distinguish its material versions from individual fetch observations,
**And** repeated delivery and backend restart preserve that identity; separate incidents are not merged merely because title, line, stop or validity looks similar,
**And** a shared incident with several affected lines remains one incident with its supported references, not one invented incident per line,
**And** missing/ambiguous identity or apparent identifier reuse follows documented qualified handling and retains explicit uncertainty; never silently merge unrelated incidents by guessing.

**Given** an existing incident and a later source record with qualified ordering evidence,
**When** content, supplied applicability references, validity or lifecycle facts materially change,
**Then** produce a stable identifiable material version with the supporting source evidence and retain the previous version as needed by unexpired consumer evidence,
**And** specify/test material-change rules from the qualified provider semantics; a new provider revision with unchanged material facts does not itself force a new unread content version,
**And** identical content re-fetches, fetch-time changes, serialization/formatting-only differences and local trip/context switches do not manufacture a new material version,
**And** keep any internal database revision distinct from source ordering and client operational revisions. A newer local sequence number does not prove the provider record is newer.

**Given** duplicate, older, out-of-order or conflicting records,
**When** they are compared with the accepted incident state,
**Then** use only qualified source ordering evidence to replace current facts; arrival time, client clock, content hash or numerically-looking opaque IDs cannot substitute for source ordering,
**And** an older record cannot replace a newer version or resurrect a confirmed closed incident,
**And** if ordering cannot be established, preserve the last supported facts with explicit unresolved source-state uncertainty, rather than claiming the incoming content is newest, unchanged or confirmed active,
**And** retain only the evidence necessary to diagnose that uncertainty and raise an unresolved provider limitation through the established solution-decision path.

**Given** an explicit source-confirmed closure, including a sparse closure record,
**When** its incident identity and ordering are supported,
**Then** persist confirmed closure and stable closure-transition identity without requiring a repeated full title/body,
**And** retain prior descriptive facts with their provenance; a sparse message does not invent a new source update time or erase the previous description,
**And** expose that the incident is no longer an active warning to consumers in the same committed result; duplicate closure observations keep the same transition identity,
**And** a genuinely newer source-supported reopening/correction may change status only with that evidence; otherwise retain closure or explicit uncertainty, never reopen from stale replay,
**And** source closure time where supplied, backend registration time and future client registration time remain separate.

**Given** one or more source validity periods, missing bounds or a gap between periods,
**When** validity is evaluated using explicit timezone/calendar dates,
**Then** distinguish future, currently applicable, between-period and elapsed validity as supported by the source, without labelling elapsed validity alone a source-confirmed ending,
**And** retain later known periods rather than declaring the whole incident ended at the first interval's end,
**And** missing or ambiguous times stay unknown; local trip service date and a similarly displayed time do not replace a source validity instant,
**And** test before/at/after qualified interval boundaries, overnight intervals and gaps; use the source's evidenced boundary semantics rather than assuming them.

**Given** a previously retrieved incident is absent from a later response,
**When** response completeness and full-versus-delta semantics are evaluated,
**Then** omission from an empty delta, partial page set or failed fetch supplies no incident-ending evidence,
**And** disappearance from a complete comparable source snapshot without explicit confirmed ending retains the incident with Status usikker – sjekk originalkilden and original-source access where supplied,
**And** preserve earlier closure/validity evidence rather than downgrading a known closure to active/uncertain merely because it is absent,
**And** source-wide fetch failure remains a retrieval-status fact; it does not fabricate individual updates, confirmed disappearances or closures,
**And** the driver's later manual removal from an overview cannot mutate this source status or erase source/display history.

**Given** a canonical incident/version is returned through the authenticated private read API,
**When** an authorized caller requests it,
**Then** return stable identity, material version, lifecycle/uncertainty, supported references, all applicable validity periods and original-source link/identifier with the required metadata,
**And** keep nullable source update time, source retrieval time and backend registration time distinct; missing source update time remains suitable for Kildens oppdateringstid er ukjent, never filled with fetch time,
**And** response completeness/coverage and source health remain separate from each incident's lifecycle; successful fetching does not certify fresh real-world conditions,
**And** this is source-scoped data, not a claim that every returned incident applies to the current trip or should be shown as an operational warning; later relevance and UI stories consume the contract,
**And** polling/reading cannot mark a version seen, registered or hidden or emit a user-facing new-notice sound.

**Given** multiple processing attempts, a stale worker result or a PostgreSQL failure,
**When** the normalized state is committed or retried,
**Then** atomically store the accepted material version, incident lifecycle/ordering evidence and processed-observation position, with no partially applied closure/update,
**And** repeated processing of the same accepted observation produces the same result without duplicate versions/transitions; stale work cannot regress the current committed state,
**And** failure preserves the preceding committed state and a retryable processing status; 4.2 source retrieval success remains distinguishable from incomplete/failed normalization,
**And** extend the existing source-status surface with a concise processing-unavailable/pending state if needed, without raw technical errors or an all-clear implication,
**And** apply repeatable migrations only for this slice's canonical source-version/lifecycle data, using real PostgreSQL rather than a substituted database.

**Given** restart, source-cache pruning or a later re-fetch of older content,
**When** retained source data is recovered or pruned,
**Then** keep the qualified minimum ordering/closure evidence needed to prevent stale resurrection, and document the bounded retention/rebaseline rule supported by 4.1's source protocol,
**And** pruning cannot turn an unverified old replay into a confidently new active incident; if safe ordering cannot be recovered, expose uncertainty and require qualification/solution resolution,
**And** source-cache cleanup cannot erase exact notice versions already required by an unexpired private day's evidence; day-associated copies retain their original AD-12 expiry,
**And** keep public source cache and private day associations separate; introduce no permanent private archive or unlimited raw provider history.

**Given** client interaction and overview lifecycle will be implemented in subsequent stories,
**When** this source contract exposes a confirmed closure or new material version,
**Then** provide stable identities so those stories can persist exact-version seen/registered/hidden state and the first client registration of closure,
**And** do not start the client's ten-minute struck-through display timer at source publication, backend receipt or API read; repeated polls/restarts cannot manufacture a new closure transition,
**And** do not encode the driver's acknowledgement, manual hiding or later trip relevance as source closure or source version changes,
**And** those client behaviors remain required and unimplemented by this story; fixture/API tests can verify this contract without a future notice screen.

**Given** normalization inputs, API requests and retained evidence,
**When** authorization/privacy checks run,
**Then** only the trusted backend ingestion path may establish source facts; client-submitted versions, status or owner fields cannot forge them,
**And** reuse existing private authentication/access/expiry and demo isolation; source reads cannot renew a session/day grant or change operational state,
**And** validate provider content as data, not executable markup, and reject unsafe original-source URL schemes while preserving an unavailable-link explanation and source identifier,
**And** protect private day references and keep credentials/private shifts/raw GPS out of logs, fixtures and source cache; use sanitized evidence for implementation tests.

**Traceability:** Source identity/change/closure portions of FR-14; metadata FR-13; prerequisites for relevance FR-12 and new-versus-updated FR-15; source failures FR-18/19. NFR-2/3/4; source-fact prerequisites for UX-DR9/19/20/21/22/23/44. AD-1/3 source-domain boundary, AD-4/5 PostgreSQL and distinct identities/revisions, AD-7 qualified source evidence, AD-8 version/lifecycle responsibility, AD-10/12 access/retention and AD-14 compatible recovery. The approved UX movement policy remains inherited for the existing status surface.

**Dependencies:** Implemented 4.2 ingestion/status/API/persistence and its E1/E2/3.2 foundations, plus actual 4.1 identity/order/closure evidence. No future relevance, notice list, acknowledgement, audio, summary UI or general offline engine is needed to verify the bounded canonical source contract. If actual provider evidence cannot support reliable ordering/identity, retain the qualification gap and request the established explicit solution decision rather than guessing it away.

**Implementation evidence:** Stable identity across repeated fetch/restart, distinct similar incidents and one multi-line incident; material versus nonmaterial updates; delayed older versions, ambiguous order and explicit supported reopening; sparse/duplicate closure; multiple/overnight validity intervals; empty delta versus missing complete snapshot versus partial/failure; processing transaction failure/retry/race; pruning/rebaseline stale replay; private API and input/URL validation. Verify real PostgreSQL persistence and source/status contract independently from later UI with labelled reference sequences derived from qualified source examples. Tests are specified, not executed here.

**Size boundary:** Canonical source identity, material versions and source lifecycle with a private read contract and minimal existing-status feedback. No client seen/registered/hidden state, ten-minute display implementation, per-trip relevance, stop-marker rendering, notice detail, sound, general synchronization or report generation. This source normalization boundary is one testable prerequisite; it does not claim full FR-14 completion.

**Pilot qualification:** Deterministic/reference-source sequences and PostgreSQL integration contribute to E8-D. E8-P still requires actual provider semantics, integrated client lifecycle/relevance and target-device/offline behavior; source or ordering uncertainty remains a real qualification gap. E8-E remains subsequent field evaluation.

**Approval:** Approved by the owner on 2026-09-26 with the stated scope: source evidence is required for changes, closure or reopening, and uncertain order/status remains explicit when source responses cannot establish it. Planning approval only; the approved copy in epics.md is canonical.
