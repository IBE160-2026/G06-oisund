---
status: approved
created: 2026-09-27
epic: E8
story: '8.5'
type: implementation
approved: true
approvedOn: 2026-09-27
dependencies: ['8.4', '1.2', '5.5', '5.6']
---

### Story 8.5: Establish Protected External Access and Verify the Private/Demo Trust Boundary

As the project owner accessing the assistant from an ordinary browser,
I want the private host protected by the adopted outer access gate and independent app login, with the fictional demo separate,
So that remote access does not expose operational records or undermine offline access and deletion rules.

**Acceptance Criteria:**

**Given** the tested 8.4 package and owner-confirmed domain/account/private identity choices,
**When** the external route is prepared in a later authorized implementation/deployment phase,
**Then** configure the adopted named Cloudflare Tunnel with stable distinct private and demo hostnames, intended service destinations and an explicit unmatched-route rejection,
**And** protect the entire private hostname, including API, auth, import and asset paths, with an owner-only Access application before enabling/publishing its route. Verify the expected Access enforcement at the private tunnel route; a protected login page alone is insufficient,
**And** use the owner's explicit identity restriction with the adopted email-OTP candidate, not a permissive email-domain rule or public registration. Keep account/domain/identity values unresolved until supplied; do not invent them or buy a service as part of story planning,
**And** preserve the separate public no-login fictional demo. It has no private backend/database route, shared credentials or authenticated relay, including through alternate paths/hostnames,
**And** do not expose pilot database/API/private HTTP host ports, add browser service tokens or disable the gate as a workaround. Missing prerequisites or failed access checks leave the affected route unavailable rather than silently public.

**Given** a request reaches the private service boundary,
**When** access claims and app authority are evaluated,
**Then** validate the Access JWT signature, expected issuer, intended application audience and expiry before relying on its claims, while retaining the separate E1 app session, CSRF/exact-origin controls and owner/day authorization,
**And** reject absent/invalid/expired/wrong-audience credentials, spoofed identity headers and direct-origin bypass attempts without disclosing private payloads. Passing Access alone does not sign in to the app, authorize another day or restore revoked authority,
**And** keep host-only secure app cookies and no credentialed demo-to-private CORS. Neither successful demo access nor a sibling hostname is private authority,
**And** verify browser-trusted HTTPS from an ordinary external PC browser and the intended tablet/browser over its mobile connection without certificate-warning bypasses. A trusted secure context does not by itself prove usable positioning or wake behavior,
**And** record observed allowed/denied results against the actual route, not only dashboard configuration or local mocks, using fictional test data before any real operational files.

**Given** the actual Access application/policy and global identity session configuration,
**When** the owner prepares a concrete test day and evaluates access coverage,
**Then** start from the adopted one-month policy/session target with compatible identity settings, inspect hidden shorter overrides and test the actual backend-verified token expiry through 5.5,
**And** compare actual remaining lifetime with the existing bounded day/settlement deadline and tested margin, keeping plan/data/assets readiness, current connectivity, app-session expiry and data expiry distinct. Configuration labelled one month is not proof of sufficient coverage,
**And** exercise deliberate renewal, cancellation, failure and insufficient returned lifetime. Renewal cannot change app_authenticated_at, grant/writer authority, stored deadlines or the validity of 5.4/7.1 timing evidence,
**And** keep cached verification labelled with its original check time. Gate/host restart cannot refresh it, create a grace period or turn an old source result into fresh information.

**Given** an authorized prepared active test day and an actual gate expiry/rejection or host/network interruption,
**When** client source/synchronization requests fail and later recover,
**Then** exercise existing 5.5/5.6 handling of Access redirects, HTML login responses, unexpected content types, network/CORS uncertainty and genuine application responses. None of these error pages may become an app asset or successful receipt,
**And** preserve permitted local operation, manual choices, pending work and original expiry; show unavailable updates and distinguish network restoration, valid source refresh and matching server acceptance,
**And** do not force login navigation during driving. Deliberate renewal waits for permitted interaction and does not interpret unknown role/speed as standstill,
**And** test logout ordering: revoke the app session before Access logout; if a closed gate prevents pending revocation, renew Access while private content remains locally locked, then process revocation before other private traffic. Access login alone never unlocks retained work,
**And** include a second tab, stale callback and lost response so renewal/logout cannot drop pending revocation, duplicate accepted work or restore locked content,
**And** use 8.4's recorded downtime distinction when testing host restart: sign-in/runtime wait is a real interruption, and a restored route does not establish fresh sources or extend any deadline.

**Given** private data would traverse Cloudflare and local services,
**When** provider handling is assessed before using real files,
**Then** inventory the actual upload/TLS path, edge caching, request/body logging, diagnostics, archival and relevant retention/configuration for the selected service/account; support conclusions with dated authoritative provider documentation, actual settings and controlled fictional probes where observable,
**And** bypass edge caching for the private host, apply no-store to private/API/auth responses, and disable private body capture/archival. Preserve AD-2's separately verified nonpersonal offline assets without caching auth redirects or private API bodies as assets,
**And** distinguish observed configuration and documented provider commitments from properties the project cannot inspect or verify. Successful local deletion and a no-store header do not prove provider erasure,
**And** record whether AD-6/AD-12 can be met for real uploads and retained metadata, with any unresolved limitations explicit. Do not send real operational files until this boundary is adequately established for the adopted requirements,
**And** if the requirements cannot be met or evidence is insufficient, block real-file/pilot use and raise a separate owner solution decision about the route, including the adopted Tailscale fallback candidate. Do not silently switch architecture, relax deletion requirements or claim that fictional testing qualified private processing,
**And** keep tokens, OTPs, private owner identity and request payloads out of repository/screenshots/log excerpts; use sanitized references to configuration evidence.

**Given** the external private/demo routes are enabled for controlled fictional verification,
**When** the owner operates or disables the ingress,
**Then** provide a runbook for credential placement/rotation, allowed identities, hostname-to-service mapping, status checks and closing the route without deleting working data,
**And** a failed tunnel/gate or maintenance action leaves prepared-client offline behavior intact within existing authority; no alternate unprotected URL or automatic second operational database is introduced,
**And** keep deployment status separate from application and pilot readiness. Record exact browser/environment and observed downtime/recovery rather than promising uninterrupted access,
**And** demonstrate ordinary no-login PC demo access externally without exposing private configuration or requiring the assessor to authenticate as the pilot owner. The assessment availability period and full delivery package remain later work.

**Given** the configured route, fictional fixtures and actual gate/client behavior,
**When** the story is verified,
**Then** report passed, failed, blocked and not-run cases for owner Access plus app login, unauthorized identity, invalid/expired/mismatched JWT, spoofed headers, private API paths, unmatched hosts, direct bypass and demo-to-private attempts,
**And** test actual HTTPS on PC and target mobile-connected tablet, actual token lifetime/renewal and expiry while local work exists, blocked pending logout, HTML responses and stale callbacks; inspect private cache behavior without retaining sensitive evidence,
**And** distinguish controlled short-lived expiry testing from observation of the production policy's actual returned expiry. No altered client clock counts as proof of token renewal or 5.4/7.1 timing eligibility,
**And** attach the provider-handling conclusion, unresolved findings, route-disable procedure and prerequisites still needed for E8-P. An accessible URL and a successful login are not sufficient to mark the whole story or pilot gate passed,
**And** run verification using the existing app/backend/database contracts without adding an alternate session scheme, token vault or unrelated database entities; fixes to 5.5/5.6 remain in those shared implementations.

**Traceability:** AD-13 named tunnel, whole-host owner-only Access before publication, provider trust boundary, cache policy, external HTTPS and ordinary-browser delivery; AD-10 independent app authority/logout and public demo isolation; AD-2/5 offline assets and receipt correctness; AD-6/12 upload handling, original deadlines and no private archives; AD-11 writer preservation and AD-14 coherent offline builds. FR-1/17/20/24/25, NFR-2/3/4 and UX-DR23/37/38/44; 5.5/5.6 supply client behavior while this story establishes and exercises the actual outer gate. All AD-1–AD-14 remain unchanged.

**Dependencies:** 8.4 packaged service/network boundaries, E1 session/revocation behavior through 1.2, 5.5 verified access coverage and 5.6 reconnect, plus 8.1/8.2 isolated demo. Actual owner account/domain/identity, target equipment and later deployment authorization are execution prerequisites. No later E8 story is required to verify the protected route with fictional data; missing prerequisites remain visibly blocked rather than guessed.

**Size boundary:** One protected external ingress and its private/demo/provider boundary, with actual Access lifetime/logout integration. No replacement authentication system, alternate-host migration, all-source/device qualification, full day field trial or final E8-D/P/E approval. Public assessment scheduling and complete delivery documentation are separate required work. Implementation tasks may separate configuration, application wiring and evidence without weakening the single boundary.

**Qualification boundary:** Supports externally accessible E8-D delivery and supplies the access/provider subset of E8-P evidence. Full E8-P still requires actual import/sources, sensor/interaction, whole-day recovery/expiry, resources/noise and releases; E8-E follows after E8-P. TIME-01 implementation/evidence remain open. This is only story planning: no account, DNS, route, Access policy, service, upload, provisioning or deployment is created or changed now.

**Approval:** Approved by the owner on 2026-09-27 as scoped, emphasizing that provider handling of uploaded files must be documented before real shifts are used; a functioning Access route alone does not qualify pilot use. Planning approval only; the approved copy in epics.md is canonical.
