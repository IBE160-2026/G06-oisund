---
status: approved
created: 2026-09-26
epic: E5
story: '5.5'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.4', '5.1', '5.2', '1.2']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

This slice checks the outer Cloudflare Access credential's actual lifetime during authorized preparation and provides deliberate renewal/recheck without changing application authority or operational state. It implements the AD-13 client/backend contract with controlled gate fixtures; actual hosting/policy provisioning and pilot qualification remain E8 work.

### Story 5.5: Check Access Coverage Before Duty and Renew Without Changing Day Authority

As the pilot owner,
I want preparation to show whether the verified outer access credential covers my granted day and settlement period,
So that I can address an access expiry before duty without mistaking a renewed gateway login for renewed application access or guaranteed connectivity.

**Acceptance Criteria:**

**Given** authorized preparation for a concrete confirmed day with an existing 5.1 grant,
**When** the app checks outer access coverage,
**Then** use the actual Access token expiry from backend-verified signature, expected issuer/audience and expiry, not the configured policy duration, cookie presence or an unverified browser-decoded claim,
**And** return only the necessary non-secret verified expiry/check time and scope-bound status through the authenticated same-origin backend; never expose or persist the raw token as application data or a browser service credential,
**And** compare against that day's bounded grant deadline including its permitted settlement interval plus an explicitly documented, tested clock margin; a policy labelled one month is not evidence of this request's remaining lifetime,
**And** keep the ordinary app deadline, day-grant deadline and AD-12 data deadline distinct; do not calculate a new grant from this check or silently extend an earlier applicable bound,
**And** failure to verify identity, token or scope returns unavailable/invalid coverage rather than success and cannot expose private day data.

**Given** verified expiry and the current coverage target,
**When** preparation displays the result,
**Then** distinguish sufficient, insufficient, expired and unverified/unavailable coverage with readable Norwegian text and relevant expiry/check time,
**And** test expiry below, equal to and above the required deadline plus margin; only coverage meeting the documented bound is sufficient,
**And** show confirmed plan, per-trip downloaded data, complete app assets, ordinary/day authority and current connectivity separately; sufficient Access lifetime alone means neither Hele dagen klargjort nor a promise of fresh sources or continuous online operation,
**And** cached verification keeps its original check time/expiry and is not presented as newly verified while offline; missing verification stays unknown,
**And** re-evaluate when the selected day, applicable grant/deadline or relevant identity changes, rejecting stale asynchronous results for another scope; re-evaluation changes no deadline,
**And** where ordinary access has expired for a merely prepared day, require application reauthorization before starting it regardless of Access coverage.

**Given** coverage is insufficient/expired or the gate requires renewal,
**When** the owner deliberately chooses renewal while the interaction policy permits,
**Then** preserve committed working state, outbox identities, manual choices, required build and existing deadlines before leaving/returning through the supported access flow,
**And** recheck the actual returned credential through backend verification; a completed login page, redirect or successful HTTP status is not evidence of sufficient lifetime,
**And** cancellation, failed renewal or an unchanged/shorter returned expiry leaves the result visibly unresolved or insufficient and allows a permitted retry without clearing data,
**And** a renewed Access credential does not update app_authenticated_at, create/extend a day grant, activate a day, transfer writer authority, resolve 5.4's unverified start timing or mark any pending work accepted,
**And** no automatic navigation or login demand interrupts driving; recovery reapplies the existing access and movement guards rather than restoring unrestricted detail.

**Given** an already authorized local day and an outer gate that expires, redirects or fails during operation,
**When** API/source-update attempts fail,
**Then** classify verified gate rejection separately from application expiry/revocation, ordinary network failure and source failure where evidence permits; when the cause cannot be established, show unavailable access/updates without inventing a diagnosis,
**And** HTML login/error pages, unexpected content types, redirects and CORS/network failures never become receipts, source success or cached app assets,
**And** preserve permitted local operation under 5.1–5.4 and show the access/update limitation; Access failure alone does not erase the local day or prove application logout,
**And** pause affected private update/sync attempts until actual usable access is re-established, avoiding navigation loops or indefinite in-progress status; renewed reachability alone does not clear failed source retrieval or acknowledge outbox events,
**And** genuinely known app revocation/local lock remains effective regardless of outer access. General reconnect orchestration and source-success warning clearance remain the following E5 integration.

**Given** local logout has locked private content and server revocation remains pending while Access blocks the request,
**When** the owner follows the permitted gate-renewal path,
**Then** keep private content locked throughout renewal and return, including history navigation and late callbacks,
**And** permit only the access recovery needed to reach revocation, sending pending application revocation before any other private traffic; no preparation/source/sync request runs first,
**And** show server logout as unconfirmed until its actual confirmation; lost response leaves the durable pending state and retry behavior from 1.2,
**And** request outer Access logout only after application revocation is confirmed; distinguish a subsequent outer logout failure from the already confirmed application revocation,
**And** Access login alone cannot recover retained work; apply 1.2/AD-10's settled revocation and fresh application login by the same owner, preserving original deletion deadlines,
**And** storage/read failure cannot silently drop the pending revocation or unlock private content after restart.

**Given** coverage checks, renewal callbacks or status persistence overlap with changed application context,
**When** a response is applied,
**Then** recheck the current owner/client/day and lock state and discard stale status from a previous scope rather than unlocking or overwriting it,
**And** a second tab cannot use renewal to alter the active writer, duplicate an operational transition or drop immutable batches,
**And** save only needed non-secret coverage metadata; private day associations follow existing AD-12 expiry and do not become a permanent access history,
**And** retain private/demo origin isolation, exact-origin/CSRF protections and no-store behavior; the public demo cannot obtain private coverage, cookies or renewal callbacks,
**And** reuse existing FastAPI/PostgreSQL authority records without adding a token vault, alternate login architecture or unrelated tables; failed status persistence is visible and never a false saved/verified result.

**Given** this implementation is evaluated before actual deployment,
**When** controlled browser/backend tests run,
**Then** exercise valid/invalid signatures, issuer/audience mismatch, absent/expired token, shorter-than-configured lifetime, margin boundaries and mismatched day scope,
**And** cover renewal success/cancel/failure/insufficient result, ordinary app expiry despite successful Access renewal, active local continuation, gate HTML/network ambiguity, stale callbacks and pending-logout renewal ordering,
**And** distinguish fixture-proven application behavior from actual Cloudflare policy/global-session/identity-provider behavior; simulated verification is labelled and cannot be enabled as a production bypass,
**And** document the measured/assumed clock margin and limits; E8-P must qualify the actual margin and returned token coverage on the intended route and Lenovo/Brave before real shifts,
**And** if the deployed route cannot provide the adopted lifetime/renewal behavior, report a solution decision under AD-13 rather than disabling expiry validation or certifying readiness.

**Traceability:** Access-readiness/renewal portions of FR-1/17/18/20 and private metadata FR-24; NFR-1–4; UX-DR3/14/23/38/39/44 and EXPERIENCE private access, data status and recovery. AD-2 separated readiness, AD-5 matching receipt status, AD-10 bounded app/day access and pending logout, AD-11 unchanged writer authority, AD-12 fixed retention, AD-13 verified token lifetime/renewal and AD-14 protected coherent boot. This does not qualify source coverage or supply a verifiable offline-start time for 5.4.

**Dependencies:** Implemented 5.1–5.4 authority/boot/continuity and 1.2 logout behavior; existing authenticated API and app/source response classification. Controlled Access fixtures can verify this slice without live service provisioning or future conflict-resolution UI. Actual private-route protection and policy configuration remain prerequisites for E8-P, not assumed implemented by these tests.

**Size boundary:** Verified coverage check, separate status and deliberate renewal/recheck including gate-blocked logout ordering. No Cloudflare provisioning/deployment, changes to adopted session durations, new identity provider, full synchronization engine, takeover, E6/E7 UI or inferred timing-proof mechanism.

**Pilot qualification:** Controlled browser/FastAPI validation and preserved PostgreSQL authority state contribute to E8-D. E8-P requires the real gate/identity sessions, tablet redirects/cookies, clock margin and private-route protection; E8-E remains later field evaluation. Tests are specified, not executed during story planning.

**Approval:** Approved by the owner on 2026-09-26 with sufficient coverage based on the actually verified Access expiry; renewal changes neither application sign-in nor day authority. Pending logout keeps private content locked while revocation is unresolved; subsequent recovery still follows AD-10 and 1.2. Planning approval only; the approved copy in epics.md is canonical.

**TIME-01 amendment (owner, 2026-09-27):** Preparation must show the distinct server E, final original grant issue time Tg and day/data bounds. A final grant intended for offline start must be issued within 24 hours before first planned activity; advance plan import is still allowed. Explain before offline entry that local activation may be rejected unless the server durably accepts it before E. Outer Access renewal does not move E/Tg or certify an offline start. Check stale grant, E before planned start, missing trusted time and unavailable server while the warning is visible; do not label the day ready for a guaranteed approved offline start.
