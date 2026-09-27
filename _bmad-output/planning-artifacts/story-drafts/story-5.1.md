---
status: approved
created: 2026-09-26
epic: E5
story: '5.1'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['4.8', '1.2', '2.7', '3.3']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

E5 completes whole-day continuity, bounded authority, coherent offline boot, synchronization/reconciliation and explicit writer transfer. It owns FR-17/18/20, the active-day part of FR-1 and applicable FR-24 protocols; AD-2/5/10/11/14 govern these boundaries. E1–E4 already own their basic feature persistence/access/errors. E6/E7 later extend recovery for roles and terminal summaries; E8 qualifies the complete result. This first slice establishes day-scoped continuation authority and its integration with existing own-day actions, not all E5 recovery capabilities.

### Story 5.1: Continue an Already Active Day When Ordinary Sign-In Expires

As the pilot owner,
I want my already active working day to retain its explicitly granted access after ordinary sign-in expires,
So that the fixed fourteen-day sign-in period does not interrupt the shift or silently authorize another day.

**Acceptance Criteria:**

**Given** valid ordinary application authentication and an owned confirmed combined day with a known planned final end,
**When** preparation requests day authority,
**Then** create the server-managed grant bound to authenticated owner, application session/client and that concrete day, persisting it in PostgreSQL before confirming issuance,
**And** bound its deadline by the then-confirmed planned final end plus seven days, retaining the issue-time basis and any earlier applicable day-grant/data limit; the ordinary fourteen-day deadline remains a separate scope rule,
**And** retries of the same request return the established grant without silently extending it; polling, receipt lookup or merely revisiting preparation cannot refresh authorization,
**And** an unconfirmed/expired day, forged owner/client/day reference or missing ordinary authority cannot obtain a new grant,
**And** grant issuance and plan confirmation alone do not mark the day active, start a trip or prove any work performed.

**Given** the browser has ordinary and/or day-scoped authority,
**When** the session cookie and authorization response are handled,
**Then** preserve a credential able to identify the granted scope after ordinary day fourteen using the existing opaque, host-only Secure/HttpOnly/SameSite cookie model,
**And** a longer cookie lifetime preserves identification only; it never extends app_authenticated_at plus fourteen days or confers general access,
**And** retain only necessary non-secret grant scope/deadline/status metadata in the existing private local store; do not replace the adopted session model with a JavaScript bearer token,
**And** keep CSRF/exact-origin protection, authenticated server-derived ownership and private no-store behavior for grant and operational endpoints.

**Given** a granted prepared day and still-valid ordinary authority,
**When** the existing operational entry path actually starts that day in this slice's online scenario,
**Then** record the active-day transition atomically with its required operational evidence and preserve the distinct prepared-versus-active lifecycle,
**And** require that transition to belong to the authorized day/client and current writer/context; do not infer it from grant creation, elapsed schedule time or a client-submitted active flag alone,
**And** a failed transition cannot be reported as server-confirmed active; local/server confirmation remains subject to existing matching-receipt rules,
**And** preserve actual trip/manual pin, plan revision and movement history; starting day scope creates no GPS/progression evidence,
**And** offline start/reconciliation of a properly prepared day remains required in later E5 recovery work; this online test path does not introduce a permanent requirement for server acknowledgement of every local operational transition.

**Given** a day already active under its valid grant before ordinary authentication expires,
**When** app_authenticated_at plus fourteen days is reached,
**Then** continue that day's authorized E1–E4 operations within the granted scope/deadline without forced logout/navigation or a mid-shift password prompt solely because ordinary access expired,
**And** validate the concrete day/client and permitted endpoint operation on the backend, including existing scoped plan corrections, operational events, notice retrieval and receipt lookup as applicable,
**And** retain active trip, corrections, stop progress, notice interaction state and pending work; do not reset them through a global ordinary-session-expiry handler,
**And** explain between-day renewal requirements without modal interruption or required driver action while moving,
**And** test ordinary expiry in the running authorized view both online and during a network interruption: expiry alone does not lock the already active locally available day. This does not claim complete offline boot or future whole-day recovery.

**Given** ordinary authentication has expired and the cookie still identifies a valid day grant,
**When** the caller tries to start a prepared/new day, obtain a new grant, access another day or invoke unrelated ordinary-account operations,
**Then** deny that broader scope and require fresh ordinary application authorization before starting another day,
**And** test a granted but never-started prepared day separately from the already active day; possession of its grant cannot convert it to active after ordinary expiry,
**And** a different client/owner, a guessed day ID, altered local metadata or direct API call cannot reuse the active day's exception for another scope,
**And** preserve explicit logout and access-status/recovery controls without treating them as authority for broader private data access,
**And** initial selection of another trip within the same active day stays distinct from starting a different day.

**Given** a confirmed later plan revision changes an unended day's planned final end,
**When** access and data deadlines are re-evaluated,
**Then** apply AD-12's data-expiry rule separately from the existing grant deadline: a changed planned end does not silently extend the previously granted authority,
**And** preserve any earlier applicable deadline; reopening, synchronization, delayed work or client clock changes cannot restart either clock,
**And** an authority extension requires separate fresh application authorization under AD-10, not an automatic consequence of a source/plan update,
**And** test late additions with a later planned end and a revision with an earlier data expiry, including overnight dates; neither can resurrect expired data,
**And** show the effective relevant deadlines and unresolved authority where necessary without claiming complete-day access coverage from a cookie alone.

**Given** an ended/aborted day or a grant/data deadline reached,
**When** authorization evaluates a request,
**Then** deny resumed operational activity for a terminal day and permit only bounded completion-review/outstanding-settlement scope where applicable,
**And** after end/abort cap that scope at the earliest of the existing grant deadline, actual end plus seven days and data expiry,
**And** expiry checks deny protected read/write/export/settlement outside its valid authority before deduplication or scheduled purge; an old receipt/batch ID cannot bypass expiry,
**And** use terminal-state fixtures to test this authorization contract without implementing E7's actual end/review/PDF flows here,
**And** local cleanup and server removal include this slice's grant/private metadata at existing expiry, without extending storage or reviving data to complete synchronization.

**Given** explicit logout, known server revocation or account revocation,
**When** this slice's granted day is open or a request arrives,
**Then** reuse 1.2's immediate local lock and durable pending-revocation behavior; ordinary expiry and explicit revocation remain different outcomes,
**And** server logout/revocation invalidates the applicable session and its grants; account revocation invalidates all affected sessions/grants,
**And** on connectivity recovery resolve pending revocation before other private requests; retained unexpired work requires settled revocation and fresh same-owner app login before recovery,
**And** new login cannot silently discard pending revocation, and lost server responses cannot be shown as confirmed logout,
**And** disconnected clients cannot instantly learn an unseen remote revocation; once learned, lock rather than using the active-day exception to bypass it.

**Given** grant/session storage failure, a stale asynchronous response, corrupted local authority metadata or unreliable timing evidence,
**When** authority is issued, read, resumed or applied,
**Then** show a specific access/state failure instead of fabricating grant issuance, confirmed activity or a renewed deadline,
**And** late responses cannot unlock logout-locked content or replace a newer owner/day/client scope,
**And** do not trust arbitrary browser-clock rollback or an unverified local active flag as proof of authorization; test clock changes and preserve original deadlines,
**And** if valid scope cannot be established, do not grant broader access or silently reset private storage; preserve permitted recoverable data within its original expiry and explain the unresolved state,
**And** make ordinary expiry, explicit revocation, invalid scope and unavailable validation distinguishable so a generic 401 handler cannot destroy valid active-day continuation.

**Given** outer Access failure/expiry or a login HTML/redirect response while the application grant remains valid,
**When** existing requests fail,
**Then** treat the response as unavailable gated connectivity, not successful data/receipt, app reauthorization or proof of app logout,
**And** do not force navigation to login while driving; preserve the already authorized local active view and show unavailable updates,
**And** Access renewal alone cannot create/extend app/day authority or unlock a pending logout,
**And** this story tests response classification with controlled fixtures only; actual Access-token lifetime preflight, coherent offline boot and gate-blocked renewal/logout integration remain later E5/E8 work under AD-13.

**Given** the access status and renewal/deadline information is presented,
**When** inspected with keyboard, touch or enlarged text,
**Then** use clear Norwegian distinctions between continued access to this active day, expired ordinary access and the need to sign in before another day,
**And** preserve the shared movement policy, focus and non-color error cues; no technical grant/session identifiers are exposed as product instructions,
**And** retain private identifiers/credentials outside logs, source control and demo assets; all day metadata follows the existing AD-12 retention rather than a new permanent access history.

**Traceability:** FR-1 active-day exception and explicit revocation; prerequisites for FR-17/18/20; authority/expiry portion of FR-24. NFR-2/3/4 and safe status NFR-1; UX-DR3/23/38/39/44 and EXPERIENCE private-access continuity. AD-2 local authority boundaries, AD-4/5 authenticated transactions/receipts, AD-9 prepared/active/terminal distinction, AD-10 bounded day grants, AD-11 client/writer binding, AD-12 expiry, AD-13 outer-gate separation and AD-14 retained-client access compatibility. All approved architecture remains in force.

**Dependencies:** Existing E1 access/logout/persistence, E2 confirmed dated day model, E3 operational activation/context and E4 scoped source/notice operations through 4.8. Online active-day authorization and in-place expiry handling are independently testable. Full offline activation/restart proof, coherent assets, gate-lifetime readiness, generic outbox recovery and writer transfer/conflict handling are explicit subsequent E5 obligations, not claimed complete here. No E6/E7 production UI or real deployment is required for this slice's authorization tests.

**Implementation evidence:** Real FastAPI/PostgreSQL and browser tests for grant issuance/retry/failure, cookie lifetime versus fixed app expiry, before/at/after day fourteen for active versus prepared day, same-day versus new-day operations and direct unauthorized API requests; client/owner mismatch, plan-end revisions with unchanged grant, terminal minimum deadlines, expiry-before-dedup/purge, online/offline running-view expiry, logout/pending revocation/new login, late responses, corrupt state/clock changes and Access HTML fixtures. Separate actually executed evidence from planned tests; none run while drafting.

**Size boundary:** Bounded day-grant issuance and enforcement, the online active-day transition path and ordinary-expiry continuation of existing operations. No new auth product, full offline shell, complete offline activation/reconciliation, writer transfer UI, generalized sync/conflict engine, E7 terminal UI or Cloudflare provisioning. Existing feature-local persistence remains in force; subsequent stories complete the whole-day recovery contract.

**Pilot qualification:** Local fullstack authority tests contribute to E8-D. E8-P requires actual Lenovo/Brave cookie/restart behavior, outer Access expiry/renewal, complete offline activation/recovery and bounded settlement integration. E8-E remains later actual-shift evaluation. Passing the online slice alone does not authorize a real shift.

**Approval:** Approved by the owner on 2026-09-26 with the stated scope: the continuation grant is limited to the already active concrete day, creates no new fourteen-day period and cannot start a prepared/new day after ordinary expiry. Planning approval only; the approved copy in epics.md is canonical.

**TIME-01 amendment (owner, 2026-09-27):** The final original concrete-day grant used for offline start has immutable server issuance time Tg and must be issued within 24 hours before the first planned activity. A start is server-approved only if its activation transaction and matching receipt are durably committed strictly before fixed E. A prepared grant or local start is insufficient. A lost response may be established by narrow authorized status lookup after E, without new activation. At/after E, only an already server-approved active day continues under the grant; a prepared or unapproved local day cannot gain continuation scope. Online activation in this slice must meet the same pre-E boundary. Test fresh/stale grant, pre-E acceptance, exactly-E rejection, lost response, and distinct local/server state. This amendment governs earlier broad use of already active.
