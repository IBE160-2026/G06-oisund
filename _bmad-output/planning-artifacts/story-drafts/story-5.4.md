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

This slice adds a provisional prepared-to-active transition without a network round trip and server acceptance only when durably committed before ordinary expiry E. It reuses existing authentication, a fresh original server-issued day grant with immutable Tg, local transactions and receipts. TIME-01 (owner, 2026-09-27) supersedes this story's former post-E timing-proof acceptance language.

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
**And** require the original final grant to have been issued by the server within 24 hours before first planned activity with immutable Tg; older preparation may be retained but a stale/missing final grant cannot authorize offline start,
**And** no grant, ordinary session, writer epoch or fresh fourteen-day period is created offline; this uses preparation completed under 5.1 and existing access rules,
**And** show before committing the offline start that it may be rejected unless the server durably approves it before E, with trusted remaining time only if available; do not present the warning as a successful server decision.

**Given** an eligible prepared day and a valid actual entry into its operational lifecycle,
**When** the transition is performed through the existing E3 entry flow,
**Then** atomically persist the active-day transition and its typed outbox event before showing local activation as complete,
**And** retain the concrete day, confirmed plan revision, client/writer scope, original grant, immutable Tg and E, event identity/sequence and local time provenance for display/audit, without treating client timing as authorization proof,
**And** distinguish local occurrence from server durable acceptance time; keep the state `Uavklart` until a matching pre-E server receipt is established, and repeat the possible-rejection warning throughout that state,
**And** creating a grant, viewing the plan, scheduled departure or a download completion alone cannot activate a day,
**And** activation itself does not confirm a trip match, departure, stop passage or completed activity; existing E3 ambiguity handling and movement restrictions govern trip choice,
**And** no extra mandatory driving-time confirmation or new trip-selection algorithm is introduced.

**Given** ordinary access expires at app_authenticated_at plus fourteen days,
**When** offline activation is attempted just before, at or after that boundary,
**Then** permit a provisional local transition only while ordinary authority can be verified before E; at/after expiry leave a merely prepared day unstarted and require renewed application sign-in and a new server-confirmed start,
**And** recheck access at commit: opening a screen before the deadline is insufficient if the transition commits after it,
**And** after E only an already server-approved active day has 5.1 continuation scope. A provisional local start with no established pre-E acceptance stays unresolved and cannot claim that exception; use narrowly scoped status lookup after reconnect before permitting further private operation,
**And** delayed synchronization, reopening, clock changes and Access renewal cannot move the original transition earlier, extend its grant/data deadline or create a new ordinary period,
**And** test suspension/restart/clock rollback; a caller-supplied occurred_at cannot prove eligibility. Offline restart with unverifiable time locks private view/actions/export until trusted control under TIME-01, preserving the local copy until deletion or recovery.

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
**And** accept the activation only when the server transaction durably commits its domain change, deduplication and receipt strictly before E. Mere request arrival, queued work, client `occurred_at`, local active flag and event order cannot establish pre-E server acceptance,
**And** reject first acceptance at or after E regardless of claimed offline start time; fresh sign-in may authorize a new prospective server-confirmed start if the day remains valid, but cannot retroactively approve earlier local work,
**And** if a matching activation was accepted before E but the response was lost, use an authorized narrow receipt/status lookup to recover that fact without a second mutation; a later lookup time does not move acceptance time,
**And** when acceptance is unknown show `Uavklart`, preserve only still-permitted local work and do not imply server approval. On a known rejection stop operations and show `Oppstart ikke servergodkjent`; after fresh same-owner sign-in and trusted time/status check offer only separately marked review/export of unexpired own local work under FR-23,
**And** accept the activation and its deduplication/receipt/revision atomically under AD-5; subsequent events follow valid causal order without requiring a generic future conflict UI,
**And** test real PostgreSQL acceptance strictly before E, rejection at/after E regardless of client time, lost pre-E receipt recovered after E, forged activation, missing Tg, revocation and no partial writes. Keep rejected versus unknown local results distinct; this TIME-01 decision resolves the policy question, not its implementation or tests.

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
**And** cover clock rollback/uncertain timing, closure on each side of commit, duplicate tabs, offline start followed by restart before/after E, pre-E acceptance with lost receipt, first arrival at/after E, stale writer/revision, revocation and original expiry; assert the pre-start and persistent pending-state warning,
**And** retain only the fields required for the activation/validation contract in existing local state and authenticated FastAPI/PostgreSQL scope; no generic event-sourcing system, alternate credential or private archive is added,
**And** apply AD-12 to every associated event, receipt and authority reference; retries or an unresolved eligibility decision do not extend retention. Keep private identifiers and payloads out of test publications and logs.

**Traceability:** Offline entry portion of FR-17, bounded FR-1, FR-20 continuation after local activation, shared FR-6/16/19 and expiry/receipt FR-24. NFR-1–4; UX-DR3/14/23/38/44 and EXPERIENCE private access, shift overview and movement states. AD-2 local atomic authority, AD-3/9 operational lifecycle, AD-4/5 PostgreSQL validation/receipts, AD-10 fixed ordinary access and concrete-day continuation, AD-11 writer scope, AD-12 expiry, AD-13 gated connectivity and AD-14 coherent prepared build. No change to AD-1–AD-14.

**Dependencies:** Implemented 5.1 server-issued day scope and online transition, 5.2 coherent assets, 5.3 same-client recovery, E2 confirmed dated plan/bundle, E3 operational entry/movement policy and existing E1–E4 synchronization primitives. The normal offline-start/delayed-acceptance case and protected rejection paths are testable here; future reconciliation UI, Access provisioning, E6 roles and E7 closing UI are not prerequisites.

**Size boundary:** One provisional prepared-to-active transition, immutable Tg/E references, pre-E server acceptance or explicit rejection, status lookup/retry and visible warning. No offline sign-in, authority issuance, cross-device takeover, generalized conflict resolution, full preparation dashboard, release migration or E6/E7 implementation. TIME-01 is approved policy; implementation and E8-P evidence remain pending.

**Pilot qualification:** Controlled browser/FastAPI/PostgreSQL scenarios contribute to E8-D. E8-P must verify actual Lenovo/Brave time/storage/restart, credential behavior and the integrated prepared-day path before real-shift use. E8-E remains the later field evaluation. No tests or implementation are performed while drafting.

**Approval:** Original story approved 2026-09-26. TIME-01 was adopted by the owner on 2026-09-27 and supersedes post-E acceptance based on offline timing proof: first durable server acceptance must precede E; rejected/unknown local work stays distinct. Planning approval only; the approved copy in epics.md is canonical.
