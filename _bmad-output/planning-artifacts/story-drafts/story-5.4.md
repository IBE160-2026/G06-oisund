---
status: approved
created: 2026-09-26
epic: E5
story: '5.4'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.3', '5.1', '2.7', '2.8', '3.4', '1.4']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

This slice adds the missing prepared-to-active transition without a network round trip, and bounded server acceptance of that transition after reconnection. It reuses existing application authentication, prior server-issued day authority, local transactions and immutable receipts. It does not introduce offline login, authority creation or a new authentication architecture.

### Story 5.4: Start a Previously Prepared Day Offline Within Valid Ordinary Access

As the pilot owner,
I want to start my previously confirmed and prepared working day when the connection is unavailable,
So that loss of internet before departure does not prevent use of the available day, while expired sign-in cannot authorize a new day.

**Acceptance Criteria:**

**Given** a confirmed unexpired own day prepared on this client while authorized,
**When** the existing operational entry path is used without a reachable server,
**Then** require still-valid ordinary application authority, the existing server-issued owner/session/client/day grant, established writer scope and a coherent compatible local build before committing the prepared-to-active transition,
**And** validate the locally retained confirmed plan/revision and available bundle associations, showing missing data rather than assuming that plan confirmation proves complete preparation,
**And** missing/uncertain authority, pending logout, known revocation, another owner/client, terminal state or expiry cannot be bypassed by a cached login screen, cookie presence or an editable active flag,
**And** no grant, ordinary session, writer epoch or fresh fourteen-day period is created offline; this uses preparation completed under 5.1 and existing access rules.

**Given** an eligible prepared day and a valid actual entry into its operational lifecycle,
**When** the transition is performed through the existing E3 entry flow,
**Then** atomically persist the active-day transition and its typed outbox event before showing local activation as complete,
**And** retain the concrete day, confirmed plan revision, client/writer scope, original grant and access-deadline basis, event identity/sequence and necessary timing evidence for later validation,
**And** distinguish the transition's occurrence time from later server receipt time; keep uncertain timing explicitly uncertain rather than backdating it,
**And** creating a grant, viewing the plan, scheduled departure or a download completion alone cannot activate a day,
**And** activation itself does not confirm a trip match, departure, stop passage or completed activity; existing E3 ambiguity handling and movement restrictions govern trip choice,
**And** no extra mandatory driving-time confirmation or new trip-selection algorithm is introduced.

**Given** ordinary access expires at app_authenticated_at plus fourteen days,
**When** offline activation is attempted just before, at or after that boundary,
**Then** permit only a valid transition committed before expiry; at/after expiry leave a merely prepared day unstarted and require renewed ordinary application authorization before starting it,
**And** recheck access at commit: opening a screen before the deadline is insufficient if the transition commits after it,
**And** an already committed eligible active day continues within its unchanged day scope under 5.1 and can reopen through 5.3 even when server acknowledgement has not yet arrived,
**And** delayed synchronization, reopening, clock changes and Access renewal cannot move the original transition earlier, extend its grant/data deadline or create a new ordinary period,
**And** document and test the timing basis and its limits across suspension/restart/clock rollback; a caller-supplied occurred_at alone cannot prove eligibility. If timing/authority cannot be established, expose the uncertainty and require appropriate access recovery rather than inventing eligibility.

**Given** activation is interrupted by write failure, closure, repeated entry or simultaneous tabs,
**When** the app resumes or the operation is retried,
**Then** before-commit failure leaves the day prepared with no orphan activation event; after-commit recovery restores the same active transition/event without a duplicate start or reset of deadlines,
**And** reuse existing same-origin writer coordination and transactional state checks so only one transition is committed for this day,
**And** an unresolved start on one tab cannot be replaced by a later scheduled trip or a different active day on another tab,
**And** quota/read failure is visible and preserves permitted data; no automatic storage clearing, new identity or fabricated server acknowledgement repairs it,
**And** persist activation without resetting established movement history or manufacturing the genuine first-start exception.

**Given** a day validly activated locally and not yet accepted as active on the server,
**When** a controlled reconnection submits the transition through the existing immutable batch path,
**Then** FastAPI validates authenticated owner/client/day, the previously issued grant and its original bounds, plan/lifecycle context, current writer authority, expected revision and activation eligibility before PostgreSQL accepts the transition,
**And** accept a transition delivered after ordinary expiry only when a verifiable timing basis establishes that activation occurred during valid ordinary access, within the unchanged continuation grant; the client's own timestamp, active flag or event ordering alone is insufficient, and delayed delivery alone does not require a fresh login when that basis is established,
**And** validate the transition and relevant preceding persisted state/evidence, not a bare active flag or a backdated timestamp; document which evidence establishes eligibility and what the server cannot independently know about disconnected timing,
**And** if eligibility cannot be established or authority has been revoked, do not silently authorize broader access or label the transition server-confirmed; preserve permitted pending work and expose the specific unresolved access/reconciliation outcome,
**And** accept the activation and its deduplication/receipt/revision atomically under AD-5; subsequent events follow valid causal order without requiring a generic future conflict UI,
**And** test real PostgreSQL acceptance before expiry and, after expiry, only with an explicitly documented verifiable timing basis; separately test client-only timestamps, forged late activation and missing/unverifiable timing evidence. Without that basis the start remains locally recorded with unresolved server status, no acceptance receipt or activation mutation, and the limitation is raised for a separate owner solution decision; do not claim the requirement passed or change V1 automatically.

**Given** submission succeeds, loses its response or conflicts with newer server state,
**When** a retry or response is handled,
**Then** preserve the original immutable batch/event identity and payload, with one in-flight batch per day; only its valid matching receipt changes status to server-confirmed,
**And** identical authorized retry after a lost response returns the established receipt without another activation or revision increment; changed content under reused identity is rejected,
**And** stale writer/revision, terminal/expired day, unknown scope or incompatible payload cannot produce partial activation, silent overwrite, automatic takeover or re-upload of expired data,
**And** keep permitted local work and stop incompatible submission for explicit recovery under AD-10/11; generalized conflict resolution and writer-transfer UI remain later E5 work,
**And** learned logout/revocation takes precedence; pending revocation is settled before other private traffic, and fresh login cannot silently discard it,
**And** HTML login pages, redirects or Access/network failures leave server confirmation pending/failed with the correct reason, not accepted and not proof of application logout.

**Given** local activation succeeded while source retrieval is unavailable,
**When** the driver uses or reopens the day,
**Then** reuse 5.3's whole available-day continuity and honest uncertainty, including later trips, manual choices, bus identity and retained notice states,
**And** show local activation versus server-confirmation status separately from source freshness, GPS quality, per-trip data coverage, app assets and credential lifetime,
**And** missing source matches/stops do not become verified through activation; approved no-match/manual fallbacks remain usable where their own prerequisites hold, while incomplete data cannot be labelled Hele dagen klargjort,
**And** source fetch success cannot acknowledge activation, and activation acceptance cannot clear an outstanding missing-update warning,
**And** display understandable Norwegian text/symbols without exposing grant/epoch identifiers or demanding login while driving. Full automatic reconnect orchestration and actual Access lifetime preflight are subsequent slices.

**Given** acceptance evidence is prepared for this slice,
**When** the implementation is tested,
**Then** include confirmed versus unconfirmed plans, valid versus missing grant, complete versus partial data, prepared versus already active/terminal day and ordinary-access boundary cases,
**And** cover clock rollback/uncertain timing, closure on each side of commit, duplicate tabs, offline start followed by restart after ordinary expiry, delayed server delivery, lost receipt, stale writer/revision, revocation and original expiry,
**And** retain only the fields required for the activation/validation contract in existing local state and authenticated FastAPI/PostgreSQL scope; no generic event-sourcing system, alternate credential or private archive is added,
**And** apply AD-12 to every associated event, receipt and authority reference; retries or an unresolved eligibility decision do not extend retention. Keep private identifiers and payloads out of test publications and logs.

**Traceability:** Offline entry portion of FR-17, bounded FR-1, FR-20 continuation after local activation, shared FR-6/16/19 and expiry/receipt FR-24. NFR-1–4; UX-DR3/14/23/38/44 and EXPERIENCE private access, shift overview and movement states. AD-2 local atomic authority, AD-3/9 operational lifecycle, AD-4/5 PostgreSQL validation/receipts, AD-10 fixed ordinary access and concrete-day continuation, AD-11 writer scope, AD-12 expiry, AD-13 gated connectivity and AD-14 coherent prepared build. No change to AD-1–AD-14.

**Dependencies:** Implemented 5.1 server-issued day scope and online transition, 5.2 coherent assets, 5.3 same-client recovery, E2 confirmed dated plan/bundle, E3 operational entry/movement policy and existing E1–E4 synchronization primitives. The normal offline-start/delayed-acceptance case and protected rejection paths are testable here; future reconciliation UI, Access provisioning, E6 roles and E7 closing UI are not prerequisites.

**Size boundary:** One prepared-to-active transition, its durable local evidence and normal later server acceptance/retry. No offline sign-in, authority issuance, cross-device takeover, generalized conflict resolution, full preparation dashboard, release migration or E6/E7 implementation. An unresolved timing/evidence limitation is a delivery risk requiring an owner solution decision, not an automatic change to V1.

**Pilot qualification:** Controlled browser/FastAPI/PostgreSQL scenarios contribute to E8-D. E8-P must verify actual Lenovo/Brave time/storage/restart, credential behavior and the integrated prepared-day path before real-shift use. E8-E remains the later field evaluation. No tests or implementation are performed while drafting.

**Approval:** Approved by the owner on 2026-09-26 with post-expiry server acceptance requiring a verifiable timing basis, never the client timestamp alone. Without it the start remains locally recorded with unresolved server status and the limitation requires a separate solution decision. Planning approval only; the approved copy in epics.md is canonical.
