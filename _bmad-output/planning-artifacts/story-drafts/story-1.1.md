---
status: approved
created: 2026-09-25
epic: E1
story: '1.1'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: []
---

## Epic 1: Access and Recover a Private Working-Day Draft

The owner can sign in, save/reopen a protected minimal draft and log out through the adopted fullstack application. This first story delivers ordinary online access only; it does not complete E1 or FR-1 as a whole.

### Story 1.1: Sign In to and Sign Out of the Private Application

As the pilot owner,
I want to sign in to the private application and explicitly end my session,
So that access is controlled by the application rather than by hidden menus or the device lock alone.

**Acceptance Criteria:**

**Given** a clean development checkout and an operator-provisioned fictional pilot account,
**When** the documented local setup runs and the owner submits valid credentials through React,
**Then** FastAPI verifies the password hash and persists a server-managed session in PostgreSQL 18 before returning success,
**And** the browser displays a private main-menu shell based on authenticated server identity, with explicit logout and no public-registration action or endpoint,
**And** the official React/Vite TypeScript starter seeds the frontend; the Full Stack FastAPI template is reference material, not an inherited auth/admin application.

**Given** successful authentication on the shared web/API origin,
**When** the session is established,
**Then** the server sends an opaque session identifier in a host-only Secure, HttpOnly, explicitly SameSite=Lax cookie,
**And** credentials are absent from browser application storage, URLs, repository files and logs; private/auth responses use no-store,
**And** repeatable database migrations introduce only account/session and necessary access-control storage, not future workday/notice/role tables.

**Given** ordinary authentication and no active-day grant,
**When** the owner reloads or reopens the browser before app_authenticated_at plus 14 days,
**Then** the valid session permits entry without another password,
**And** polling/requests do not extend the deadline,
**And** at or after that deadline protected ordinary access requires renewed authentication even if a cookie remains; changing the browser clock does not extend server authority.

**Given** missing, forged, expired or server-revoked session authority,
**When** a caller directly requests protected main-menu session data,
**Then** the API denies access with the defined authentication/access outcome and no private payload,
**And** submitted owner fields confer no authority; account revocation invalidates all that account's sessions on subsequent requests.

**Given** login/logout and protected application requests,
**When** a writing request fails CSRF validation or exact-origin checks, including a sibling/demo origin,
**Then** it produces no unauthorized state change or authenticated session,
**And** credentialed cross-origin access is not enabled for the demo; malformed requests fail backend validation without partial writes.

**Given** invalid credentials or an unavailable API/database,
**When** sign-in is attempted,
**Then** the UI reports failure in ordinary Norwegian without claiming success or exposing credentials/internal errors,
**And** invalid credentials do not disclose account existence,
**And** repeated failures invoke a documented bounded rate-limit policy tested at its configured threshold and recovery boundary,
**And** database failure cannot produce an authenticated success response or usable session cookie.

**Given** a private view is open,
**When** the owner selects Logg ut,
**Then** the client immediately hides/locks the private view before waiting for the server response,
**And** server revocation remains visibly unconfirmed until an authoritative response confirms it; an absent or failed response leaves the view locked and offers retry.

**Given** a logout request reaches the server and its success is confirmed,
**When** the client processes that confirmation,
**Then** the server session is invalidated, its cookie is cleared and the client shows confirmed logout and private sign-in,
**And** replay of the old cookie is denied; browser-back cannot restore authenticated private content; repeated logout never renews authority.

**Given** this story's application has no locally retained working-day data,
**When** a logout request or response fails,
**Then** the private UI locks for the current page and explains that server logout is unconfirmed, with a retry action,
**And** hiding the menu is not represented as confirmed server revocation,
**And** durable offline locking/pending revocation is required before any later story introduces private local drafts; this story makes no offline-logout or retained-data recovery claim.

**Given** the sign-in and main-menu surfaces,
**When** the owner uses keyboard navigation, touch or enlarged text,
**Then** labelled fields/actions, visible focus, pending/disabled state and errors remain understandable without color alone or obscured actions,
**And** applicable approved DESIGN palette/typography/control tokens are reused,
**And** no unimplemented draft/demo action is presented as working and authentication requires neither GPS nor camera.

**Traceability:** FR-1 (ordinary private access/online logout subset), NFR-3, UX-DR1/2 (access-surface subset), UX-DR3 (private entry/logout subset), UX-DR38; AD-1/3/4/10 and AD-13 same-origin/cookie/no-store rules. AD-12 prohibits sensitive logging; AD-14 requires pinned build/dependency identity. All adopted decisions remain binding as their domains are introduced.

**Dependencies:** No previous application story. The future implementation supplies repeatable local setup, operator-only fictional account provisioning and trusted local HTTPS for Secure-cookie testing. Credentials remain outside source control. No public registration/admin feature, external account, domain, tunnel or deployment is needed for this local slice. PostgreSQL integration evidence cannot use SQLite. Password hashing and rate-limit implementation choices are documented and tested within this story.

**Implementation evidence:** Browser sign-in/reopen/logout against FastAPI/PostgreSQL; direct API negative tests for missing/forged/revoked/expired authority, CSRF/origins and rate limits; controlled-clock tests before/at/after day 14 with repeated requests; database failure and lost-logout-response cases; keyboard/text-enlargement inspection. Record versions and fictional fixtures. These checks are proposed, not executed during story drafting.

**Remaining coverage:** Before storing private local drafts, later E1 work must supply durable logout/reload locking, pending revocation and applicable retention. Active-day grants and post-end settlement remain E5 integrations; public fictional demo remains E8. The ordinary-session deadline must not become a global forced-logout/navigation rule for future authorized active days. No future story is needed to exercise this story's bounded online access outcome.

**Pilot qualification:** Contributes implementation evidence to E8-D, but does not pass E8-P. Actual private ingress/Access JWT checks, outer-session expiry/renewal, offline pending logout through a blocked gate, private/demo isolation and Lenovo/Brave behavior require later qualification. E8-E remains subsequent three-workday evaluation. No deployment or readiness decision is made here.

**Approval:** Approved by the owner on 2026-09-25 with immediate client hiding/locking at logout, before any server response; server revocation remains unconfirmed until confirmed, with retry. The fixed 14-day deadline and later active-day/durable-offline boundaries remain unchanged. Approval is for planning, not implementation. The approved copy in epics.md is the canonical story.
