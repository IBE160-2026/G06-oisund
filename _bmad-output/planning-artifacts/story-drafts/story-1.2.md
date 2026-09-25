---
status: approved
created: 2026-09-25
epic: E1
story: '1.2'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['1.1']
---

## Epic 1: Access and Recover a Private Working-Day Draft

This slice makes explicit logout survive reload and reconnect before subsequent stories introduce private local draft data. It extends Story 1.1 without implementing the active-day engine, workday outbox or Cloudflare deployment.

### Story 1.2: Keep Private Access Locked Until Pending Logout Is Settled

As the pilot owner,
I want my explicit logout to remain effective locally when the network fails or the browser restarts,
So that the application does not silently reopen private access while server revocation is still pending.

**Acceptance Criteria:**

**Given** a signed-in private view, regardless of network availability,
**When** the owner selects Logg ut,
**Then** the client immediately hides/locks private content before waiting for the server,
**And** it atomically persists the local lock and pending-revocation intent in IndexedDB before reporting the local lock as durably saved,
**And** it records only necessary non-secret scope/status metadata; the session credential remains in the HttpOnly cookie,
**And** while revocation is pending the UI distinguishes local lock from unconfirmed server logout and offers retry.

**Given** a saved local lock and pending revocation,
**When** the browser reloads, closes/reopens or restores a page from history,
**Then** private content is not rendered and ordinary private requests are not started before the lock state has been checked,
**And** a still-present cookie or previously rendered authenticated page cannot unlock access,
**And** if online validation of access state is unavailable in this no-active-day slice, the application remains locked rather than asserting authentication or confirmed revocation.

**Given** pending revocation and a network that appears connected,
**When** the client retries automatically after connectivity returns or the owner selects retry,
**Then** it attempts the session revocation before ordinary private traffic,
**And** connectivity alone, timeout, HTML/redirect response or unexpected content type is not accepted as proof of revocation,
**And** a failure keeps the durable lock/pending state with an accurate retryable status, not indefinite success or fabricated progress.

**Given** the server applied logout but its response was lost, or the targeted session has already expired or been revoked,
**When** the client retries using Story 1.1's protected logout protocol,
**Then** the server can confirm that the targeted authority is no longer usable without renewing or creating a session,
**And** the client clears pending status only on an explicit authoritative outcome, never on an arbitrary 401, redirected login page or missing cookie alone,
**And** the local lock stays in place after settlement until fresh application login succeeds.

**Given** a settled logout and a locally locked application,
**When** the owner supplies fresh valid application credentials,
**Then** only a confirmed successful login unlocks private access and establishes a new ordinary authentication timestamp,
**And** restored network access, an old cookie, server polling or an outer access-gate login alone cannot unlock the application,
**And** while logout is still pending a new application login is not used to overwrite or bypass that pending revocation,
**And** ordinary access continues to use the fixed 14-day deadline without automatic renewal.

**Given** another same-origin tab or a request already in flight when logout begins,
**When** a logout notification or late authenticated response is received,
**Then** tabs apply the shared local lock, checking it on resume and before protected requests/rendering,
**And** late responses cannot display private content, clear the lock or replace the pending-revocation state,
**And** a stale response from the old session cannot undo a subsequently completed fresh login,
**And** no assertion is made that a client can retract requests already accepted by the server before logout.

**Given** local lock storage is unavailable, unreadable or fails to commit,
**When** logout is requested or the application restarts, resumes or restores a page from history,
**Then** private content is not shown automatically, including a brief render before access checks finish,
**And** a clearly labelled storage/access-state error explains that the durable local lock and pending revocation cannot be trusted; no saved-lock or server-revocation success is claimed,
**And** server revocation is still attempted when reachable and failures remain explicitly retryable,
**And** an absent or unreadable marker after a failed write is not treated as evidence that no logout is pending,
**And** recovery follows AD-10: resolve the outstanding revocation through authoritative server evidence and require fresh application login by the same owner before restoring any retained private work,
**And** new login must not silently discard, overwrite or bypass unresolved revocation; if the relevant authority cannot be identified or settlement cannot be established, keep private content locked and report that recovery remains unresolved,
**And** recovery neither clears unrelated browser data as a repair nor promises survival after browser storage eviction.

**Given** a test injects a failed lock/intent transaction, a lock-store read failure or unreadable access metadata,
**When** the tester separately exercises immediate logout, reload, browser close/reopen and history restoration, then attempts fresh login with pending revocation unresolved,
**Then** every case keeps private content hidden, reports the error and refuses to treat new credentials alone as settlement,
**And** after reliable storage access is restored and authoritative revocation settlement is obtained, only the same owner's fresh application authentication permits recovery,
**And** a different authenticated owner cannot recover the affected owner's retained work; this access boundary is tested with fictional owner identities, not public registration.

**Given** explicit logout, known server revocation or ordinary-session expiry,
**When** the client handles the corresponding outcome,
**Then** explicit logout/known revocation invokes the local lock and is kept distinct from ordinary expiry,
**And** there is no blanket destructive storage reset or global expiry handler that would invalidate the adopted future active-day exception,
**And** status and retry controls are labelled, keyboard accessible and understandable without color alone.

**Traceability:** FR-1 (explicit logout/revocation), NFR-2/3, UX-DR3/23/38, AD-2 (local persistence), AD-10 (offline lock, ordered pending revocation, fresh login), AD-13 (outer-gate failure is not app logout), AD-14 (preserve pending logout). This supplies the bounded logout prerequisite for later private draft storage, without claiming whole-day FR-17/20 coverage.

**Dependencies:** Approved Story 1.1, including server sessions, CSRF/exact-origin controls and confirmed online logout. Add only local access-lock metadata and the minimum idempotent logout confirmation behavior needed here. No workday model, import, GPS, role engine, live Cloudflare account or future story is required. Local tests use the existing app and PostgreSQL, simulated transport failures and browser reloads.

**Implementation evidence:** Browser tests for offline logout, delayed/lost responses, reload/history, repeated retries, fresh login ordering and two tabs; storage-transaction, read-failure and unreadable-metadata fault injection across reload/close-reopen/history; API tests for already-revoked/expired session settlement preserving CSRF/origin protection; negative checks for HTML/redirect/error responses. Assert no private rendering before checks, no interpretation of missing/unreadable lock state as cleared intent, no pending-intent replacement by new login and same-owner-only recovery after settlement. Use fictional access-scope fixtures here; test actual retained draft payloads when introduced in Story 1.3. These tests are planned, not executed here.

**Integration boundary:** There are no private workday payloads in this story. When later E1 stories introduce local drafts, they must prove that logout retains unexpired unsynchronized work without exposing it, only the same freshly authenticated owner can recover it, and all copies keep their original deletion deadline. E5 integrates the same lock with active-day grants/outbox and E8 qualifies actual Access renewal while locked, app revocation before Access logout and target-device recovery. These remain required, not waived or implemented by mocks. A stub data fixture is not evidence that full retention or active-day continuation works.

**Pilot qualification:** Automated local failure evidence contributes to E8-D. It does not pass E8-P's real Lenovo/Brave, gate-blocked logout, private/demo isolation or whole-day continuity checks; E8-E remains later field evaluation. No implementation, provisioning or readiness check is authorized by this planning draft.

**Approval:** Approved by the owner on 2026-09-25 with explicit storage-failure behavior: no automatic private rendering on restart/history when lock/intent storage is unreliable, clear error, AD-10 same-owner recovery and no silent disposal of unresolved revocation during fresh login. Approval concerns planning only. The approved copy in epics.md is canonical.
