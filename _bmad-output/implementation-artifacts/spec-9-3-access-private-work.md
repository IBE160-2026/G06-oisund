---
title: '9.3 — Access private work'
type: feature
created: 2026-10-20
status: done
route: dispatch
epic: 9
story: '9.3'
alias: V1-03
story_key: 9-3-access-private-work
baseline_commit: 6800ed893b6a1c4e69f977cc3f585c6aec20fb82
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-9-context.md
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The fictional-only application needs private access before introducing private drafts.

**Approach:** Add provisioned login, protected empty workspace and logout with isolated PostgreSQL accounts/sessions. Preserve separate demo access.

## Boundaries & Constraints

**Always:** Hidden CLI password input, password hashing, persistent bounded throttling and generic credential errors. Opaque hashed server sessions expire exactly 14 days after sign-in without renewal. Host-only HttpOnly/SameSite cookies, CSRF and exact-origin checks protect private mutations including login/logout. Insecure cookies require explicit loopback development; unsupported public configuration fails closed. Server-derived ownership and no-store protect every private resource. Purge expired security metadata at startup/hourly. Private presentation stays in memory and clears on expiry/logout. Unconfirmed logout locks presentation until revocation is settled, including after reload. Use Norwegian accessible forms.

**Never:** Public signup, default passwords, private data in the demo cluster, private browser persistence, offline grants, public deployment, draft CRUD, PDF integration or push.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Provision/sign in | Operator-created account; correct credentials | New opaque session; protected empty workspace | Invalid credentials disclose no account existence; bounded attempts |
| Direct access | Missing/invalid session or another account UUID | Deny without private disclosure | Distinguish renewal from safe resource denial |
| Expiry | Session reaches original 14-day deadline | Immediate denial and cleared private presentation | Reauthentication creates a new session; no saved-data lifetime extension |
| Forgery | Wrong/missing origin or CSRF proof | No private mutation | Explicit denial, including credentialed requests |
| Logout | Live session; acknowledged invalidation | Session revoked and private presentation cleared | Back/reload cannot restore private presentation |
| Lost logout reply | Server unreachable or acknowledgement lost | Local presentation locked; logout explicitly unconfirmed | Retry/settle revocation before authentication or private reads |
| Isolation | Demo reset, demo request or private identifier on demo API | No access to or mutation of private storage | Fail closed on crossed runtime/database configuration |

</frozen-after-approval>

## Code Map

- `backend/app/main.py`, `storage.py`, `domain.py`, `backend/migrations/001_initial.sql` — fictional-only contracts/guards; preserve and add separate private app/storage.
- `backend/app/manage.py`, `run.py` — migration/provisioning entry points; preserve fictional reset.
- `compose.yaml` — demo cluster; separate private project/volume and loopback API 8001 required.
- `frontend/src/main.tsx`, `style.css` — preserve default demo/keyboard order; add `/private` entry.
- `Docs/evidence/9-1-import-qualification.md` — six supported examples; example 6 partial with separate owner assistance. Other layouts, OCR, extended clocks, DST and application integration remain unqualified. Preserve adapter/evidence.

## Tasks & Acceptance

**Execution:**
- [x] `backend/app/private_storage.py`, `backend/migrations/private/` — accounts, sessions, bounded login metadata, transactional ordered migrations and cleanup.
- [x] `backend/app/auth.py`, `private_main.py`, `manage.py`, `run.py` — provisioning, authentication, revocation, CSRF/origin and ownership guard. Use an owned account-profile endpoint for cross-owner checks without draft CRUD.
- [x] `compose.private.yaml`, `backend/requirements.in`, `requirements.lock` — isolated runtime; verify/pin added dependencies using official documentation and executable checks. No added packages: pinned Python 3.13/OpenSSL provides scrypt, HMAC and cryptographic randomness; existing locks unchanged.
- [x] `frontend/src/PrivateAccess.tsx`, `main.tsx`, `style.css` — login, empty workspace, expiry and confirmed/unconfirmed logout; suppress stale responses and settle revocation after reload.
- [x] `backend/tests/test_private_access.py`, `frontend/tests/private-access.spec.ts` — matrix coverage with synthetic users, actual HTTP/PostgreSQL and browsers, concurrency and secret-free errors.
- [x] `README.md`, `Docs/development-log.md`, this spec and sprint tracking — setup, provisioning, evidence and limitations without credentials. Implementation handoff retains in-progress tracking until parent review synchronization.

**Acceptance Criteria:**
- Given two synthetic accounts, when requesting own/foreign profiles, then ownership permits only authorized access and demo cannot bypass it.
- Given expiry, logout, response loss or reload, when presentation changes, then it follows server state without claiming unconfirmed logout succeeded.
- Given private restart and demo reset, when sessions reopen, then original deadlines and private storage remain unchanged.
- Given keyboard operation at 768px/1440px, when signing in/out, then labels, focus, wrapping and status remain usable; demo/import regressions pass.

## Implementation Notes

No intent gaps. Additive migrations/provisioning affect selected private storage only; no deployment or existing-data deletion. Footprint spans database, API, CLI, configuration and UI. Accounts are not seven-day drafts. Draft retention/authorization becomes executable in 9.4; profile tests do not claim draft acceptance.

## Spec Change Log

## Review Triage Log

| Finding | Verdict | Verified evidence and route |
|---|---|---|
| Blind 1: late login after logout | high | Login can commit/set a cookie after another tab has confirmed logout; generation guards only presentation. Patch existing browser mutation ordering and add delayed-response regression. |
| Blind 2: staggered throttle windows | medium | Global expiry precedes later name/IP expiries, so successive windows can exceed the documented 201 rows. Patch all admitted buckets to the global deadline; boundary regression. |
| Blind 3: non-ASCII CSRF | medium | Root reproduced HTTP 500 with a byte-valued non-ASCII proof. compare_digest raises TypeError before the guarded parser. Patch ASCII validation; expect no-store 403. |
| Blind 4: tests clear operational throttles | medium | API/browser fixtures delete all login_limits in the private runtime. Patch tests to refuse non-synthetic accounts before mutation and reserve their account namespace from operator provisioning; document separate synthetic-only verification use. |
| Blind 5: bootstrap database superuser | low | API uses this dedicated local cluster bootstrap role, explicitly documented. No SQL injection, cross-cluster access or untrusted SQL execution exists in current callers. Restricted runtime/migration roles would add machinery for a hypothetical vulnerability; reject under low-finding complexity rule. |
| Blind 6: focus after logout/expiry | low | The input ref is absent until React commits the form; immediate focus calls do nothing. Patch focus in an effect and assert both transitions. |
| Blind 7: visibility clears credentials | medium | hide calls clear on every visibility change, losing partially typed credentials when using another window/password manager. Patch presentation clearing to preserve unfinished form input; browser regression. |
| Blind 8: blocking middleware | medium | Async boundary directly calls synchronous PostgreSQL-backed CSRF validation, blocking the event loop during database waits. Patch with thread offload; targeted liveness regression. |
| Blind 9: oversized request bodies | medium | Credentials lengths are validated after full JSON parsing; no body-size boundary exists. Patch bounded private mutation reads and explicit 413/no-store, including streamed bodies. |
| Edge 1: late login after logout | high | Same reachable authentication response ordering as Blind 1. Patch with that correction and test. |
| Edge 2: staggered throttle windows | medium | Same independent expiry calculation as Blind 2. Patch with shared window deadline. |
| Edge 3: non-ASCII CSRF | medium | Same root-reproduced 500 as Blind 3. Patch explicit denial. |
| Verification 1: IP cap regression | medium | Pre-verified: changing IP maximum20 to100 passes current tests. Patch distinct-name HTTP attempts20/21 below global threshold. |
| Verification 2: CSRF signature/age gap | medium | Pre-verified: current negatives fail at inequality before signature/age checks. Patch matching invalid-signature and signed expired/future cookie/header cases, preserving session state. |
| Root 1: pending marker lifetime | medium | Pending marker is a session cookie but authentication lasts14days; closing the browser can discard the unresolved-logout lock before the session expires. Patch marker lifetime to cover the session and verify its expiry/clearance. |

Implementation corrections for the accepted findings are complete: authentication mutations use a shared Web Lock through response consumption; staggered throttle rows share the global deadline; CSRF rejects non-ASCII before comparison; synthetic-only test guards precede mutations and operator CLI reserves their namespace; focus runs after form commit; visibility preserves unfinished input; CSRF validation is offloaded; streamed mutation bodies are bounded to 4096 bytes. Root finding15 (pending marker lifetime, table Root1) now persists the lock for14days and clears it only on acknowledgement. Targeted verification: private API suite14 passed (30.67s), private browser suite10 passed (20.0s), frontend TypeScript/Vite build passed. A further targeted safety-guard rerun passed1 test with13 deselected after adding nonempty security metadata to refusal assertions. Parent owns broad final verification; no demo/import/restart suites rerun in this correction cycle.

## Verification

Build/configure both Compose projects; run private HTTP/PostgreSQL tests, existing assessment and fixture-mounted import regressions, frontend build/typecheck and Playwright suites. Sequentially verify private restart, migration reapplication, cleanup and isolated demo reset. Check browser storage, secret-free logs and git diff --check. Record actual commands/results and limits.

### Implementation evidence — 2026-10-20

- Read this spec and every frontmatter context file before implementing. Added isolated Compose/private PostgreSQL schema, ordered advisory-locked transactional migrations, security cleanup, server-derived profile ownership, provisioned accounts and hashed fixed-deadline sessions. No draft CRUD or PDF integration.
- `powershell -ExecutionPolicy Bypass -File scripts/initialize-private.ps1`: passed; cryptographically generated database secret is ignored by Git and mounted through Docker secrets. No default account/password. Both `docker compose up -d --build --wait` and `docker compose -f compose.private.yaml up -d --build --wait`: passed. Private Compose `config --quiet`: passed. Existing requirements unchanged; Python/OWASP documentation and actual scrypt execution checked; private `python -m pip check`: no broken requirements.
- `docker compose -f compose.private.yaml exec -T private-api python -m pytest -q tests/test_private_access.py`: **8 passed (19.02s)**. Actual HTTP/PostgreSQL covers two owners, fixed deadlines, hashed storage, session/profile denials, origin/CSRF forgery, logout/replay/expiry/purge, concurrent throttling and bounded random-name metadata. A PTY verifies CLI prompts never echo the generated synthetic password. Validation errors do not echo submitted secrets.
- `docker compose exec -T api python -m pytest -q tests/test_assessment.py`: **18 passed (0.97s)**. Read-only fixture-mounted `tests/test_pdf_import.py`: **76 passed (3.22s)**. Qualified six-supported/example-6-partial envelope unchanged.
- `npm.cmd run build`: passed TypeScript/Vite; latest Docker frontend build also passed. Final `npx.cmd playwright test`: **21 passed (23.8s)**, including eight private tests and 13 demo regressions. Covers keyboard/focus/wrapping at 768/1440px, no local/session storage, session restoration/expiry, history, unreachable logout, lost acknowledgement/reload settlement, immediate cross-tab clearing and late-response suppression. New screenshots visually inspected at 768px; demo screenshot rewrites restored to baseline.
- `uv run --no-project scripts/verify-private-access.py`: passed sequential real private DB/API restart, unchanged original session/deadline and throttle metadata, migration reapplication twice, cleanup, fictional demo reset, crossed identifiers and revocation. Tests use random synthetic accounts and clean up their accounts/sessions. No credentials emitted. Final private API log inspection contained startup/shutdown and an earlier bootstrap-password transition failure, with no credentials/private request payloads; access logging is disabled.
- Negative execution evidence: the first generated-secret transition correctly failed authentication until the existing synthetic PostgreSQL role was changed to the generated secret; clean bootstrap instructions generate it before initial startup. One verification run accidentally overlapped container restart and browser tests, causing a container-exec interruption and changed throttle snapshot. Repeated sequentially, both the full browser suite and restart script passed. Windows Store `python.exe` was unavailable; the documented `uv run --no-project` command executed successfully.
- Authentication and CSRF cookies plus a security-only logout-pending cookie are necessary protocol state; the latter stores only `1`, never account/private content, and survives reload until revocation acknowledgement. BroadcastChannel carries logout state only. Concurrent CSRF rotation may safely deny a mutation; explicit retry obtains fresh proof. No public deployment, real hardware/assistive-technology audit or draft acceptance is claimed. Parent independent review/status synchronization remains outstanding at implementation handoff. No commit/push.

### Final root verification and review completion — 2026-10-20

- Root read the complete application diff, security/schema/configuration changes, both private test suites and scripts, and visually inspected both 768/1440px screenshots. Fifteen findings received individual verdicts above: thirteen independent findings plus one low bootstrap-role finding and one root marker-lifetime finding. All retained findings were patched; the low hypothetical privilege-hardening finding was rejected under the workflow rule. Nothing deferred; no retained blocker.
- Final root runs: private HTTP/PostgreSQL **14 passed (27.33s)**; existing assessment **18 passed (1.03s)**; approved fixture-mounted import regressions **76 passed (3.22s)**. Frontend production build/typecheck passed. Full Playwright **23 passed (23.3s)**: thirteen demo and ten private tests, including committed delayed login before another tab's logout, retry/reload settlement, fixed expiry, focus, input preservation and persistent pending marker.
- Sequential `uv run --no-project scripts/verify-private-access.py` passed real private DB/API restart, unchanged original session/deadline and throttle metadata, repeated migrations, cleanup, isolated demo reset, crossed identifiers and revocation. Both Compose configuration checks passed; private `pip check` found no broken requirements. Sandbox denied uv/Docker/instruction-file access on some first attempts; required escalated retries succeeded. These environment denials are not product failures.
- Matrix audit: provisioning/sign-in and generic failures have real API/CLI plus browser coverage; direct/cross-owner access has real API tests; expiry is tested before purge and in browser presentation; forgery includes matching invalid-signature/expired/future/non-ASCII proofs; logout tests revocation/replay/back/reload; lost replies and concurrent delayed login have browser regressions; runtime/database guards and actual demo reset establish isolation. Every retained matrix row ran and passed.
- Root restored only test-generated 9.2 screenshot rewrites. Final whitespace checks passed. The private access slice is complete; build spec is done and sprint story 9.3 is review under BMAD's terminal synchronization rule. Stories 9.1/9.2 remain done, 9.4 remains backlog. A local conventional commit is created at workflow completion; no push, next story or draft/PDF application integration is included. Loopback-only, synthetic verification and hardware/accessibility limitations remain as documented.

### Owner walkthrough observations and navigation correction — 2026-10-20

- Jonas confirmed successful account provisioning/sign-in, then reported that private signed-in/signed-out and fictional-demo presentations are clearly distinguishable and logout messages provide sufficient confidence. This is owner-observed usability evidence, not a claim of manually exercising expiry or network failures, nor final story acceptance.
- Owner identified the missing route from demo back to private access. Added a visible `Gå til privat tilgang` link and clarified that visiting demo does not revoke an existing private session; private access restores a valid workspace or shows sign-in. Returning to demo is not evidence of logout.
- Root verified production build/typecheck and healthy rebuilt frontend. One-off installed-Edge checks passed demo/private navigation in both directions and keyboard activation at768/1440px without overflow. Used fresh browser contexts and did not provision accounts, clear throttle metadata, reset private storage or run synthetic-only private suites against the owner's account. No new persistent test was needed for this small link correction. Sprint remains review; walkthrough decision is pending. No commit/push for this follow-up.

### Owner manual observations — walkthrough testing, 2026-10-20

- Jonas reported synchronized sign-in/sign-out behavior across browser tabs and a comprehensible wrong-password error. He explicitly regarded not disclosing whether username or password was wrong as the desired behavior.
- Together with the earlier provisioning, state-distinction and corrected demo-navigation observations, this completes the owner's reported manual walkthrough observations. No network-outage, elapsed-retention or other unreported manual execution is inferred. Explicit final walkthrough decision is pending; sprint remains review. No new automated tests, commit or push in this observation-recording step.

### Owner acceptance and closure — 2026-10-20

- After completing the BMAD walkthrough and the demo-navigation correction, Jonas explicitly chose approval: "godkjenn". Story 9.3 is accepted and its sprint status is now done; this supersedes earlier review/pending-decision statements. Epic 9 remains in-progress and story 9.4 remains backlog.
- Acceptance includes recorded automated verification and owner observations of provisioning/sign-in, distinct private/demo/logout presentations, improved return navigation, synchronized tab behavior and understandable generic credential errors. No unreported manual test or new full regression run is inferred.
- The follow-up navigation change passed production build/typecheck and fresh-context Edge navigation/keyboard checks at 768/1440px before approval. This closure updates tracking/documentation only. Implementation commit b42bef09ab1de671bb4dcde37892b6ad3ffd557c remains local; the navigation correction and walkthrough/closure documentation remain uncommitted. No commit, push or next story is performed by this closure.
- Walkthrough workflow.on_complete resolved successfully to an empty value; no additional completion action applies.
