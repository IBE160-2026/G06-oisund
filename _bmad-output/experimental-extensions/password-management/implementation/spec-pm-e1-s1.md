---
title: 'PM-E1-S1 — Change own password'
type: feature
created: '2026-10-31'
status: in-review
route: dispatch
review_loop_iteration: 1
baseline_commit: b352640c3cfb80b962db6056116e1c747cfb760a
context:
  - ../planning/epics.md
  - ../planning/technical-contract.md
  - ../planning/coverage.md
  - epic-PM-E1-context.md
---

<frozen-after-approval reason="Owner explicitly authorized sequential implementation of the finalized PM-E1 plan; owner-dependent checks are deferred">
## Intent
Implement only PM-E1-S1 from epics.md: a complete own-password-change flow with safe account-wide revocation and concurrency. Preserve the already approved scope and existing accounts/data. The owner has authorized continuing independent work without further checkpoints, not new product decisions.

## Boundaries & Constraints
Always use this isolated repository checkout on codex/plan-password-management. Synthetic tests only. Reuse scrypt, server sessions, Origin/CSRF, no-store, current design and transient browser state. All S1-AC1..9 apply. Implement shared account-first locking before private/session row locks, including login/logout/import/cleanup; avoid unnecessary credential-version migration. Password-change rate admission can reuse namespaced persistent login_limits buckets without changing existing login budgets. No S2/S3 features yet.
Never operate tablet, production, real accounts, SSH/Cloudflare access, other runtime/volumes, merge/deploy/tag/release. Do not commit or push from implementation agent: parent handles reviewed commits and session logs. Owner is unavailable: mark mandatory owner-dependent checks `utsatt – krever eier`, never fabricate pass or wait for input. Do not mark story done while mandatory owner checks remain.

## I/O & Edge-Case Matrix
| Scenario | Input | Outcome | Failure |
|---|---|---|---|
| Own change | live A session and correct old/new password | fresh hash; every A session revoked; login new; B unchanged | typed current-password validation, no input echo |
| Races | login/private save/logout/cleanup/change overlap | one common lock order, no stale credential session or post-revocation mutation | no deadlock, unchanged business retention |
| Access boundary | expired session/forged account/CSRF/Origin/body | safe denial, no mutation | generic boundary responses |
| Transport/UI | lost reply, dirty/pending edits, late response/offline | truthful uncertainty, clear secrets, no automatic replay | no private state resurrection |
</frozen-after-approval>

## Code Map
- backend/app/auth.py: password_hash/authenticate/session and persistent login admission. Introduce reusable account lock and password-change service without creating a login session.
- backend/app/private_main.py: strict DTO, mutation boundary, session cookie presentation, current logout/login direct SQL.
- backend/app/private_storage.py: cleanup session-before-business deletes; adjust consistently for account gate.
- backend/app/draft_storage.py and other auth.session callers: existing session then account/record order; audit all direct session paths including private_import.
- frontend/src/PrivateAccess.tsx: generation/session identity, navigator.locks, BroadcastChannel, dirty guard and typed request errors. Build a small separate form/settings screen; preserve main content state/cancel and required pending protection.
- frontend/src/PrivateDrafts.tsx, PrivateConfirmation.tsx and business controllers: reuse existing dirty/pending ownership; do not lose unconfirmed work for password navigation.

## Tasks & Acceptance
- [x] Complete S1 backend/code/locking tasks and tests defined in epics.md; no S2 schema.
- [x] Complete UI and all independent S1-AC1..9 checks; tests must exercise actual backend, not only mocked browser flow.
- [x] Add focused backend tests test_password_change.py, frontend password-change tests and concise user/lock documentation. Keep new test cleanup synthetic-only and avoid secret logs.
- [x] Run focused tests and relevant existing regressions; report exact commands/outcomes/skips. Parent prepares isolated compose.password-tests.yaml (project ibe160-password-tests; UI15440, private API18441, fictional API18440). Do not modify that harness concurrently. Test API env uses PRIVATE_TEST_PROJECT=ibe160-private-tests for existing safety marker.
- [x] Record implementation notes and incomplete owner checks here; do not claim physical-device/owner acceptance.

## Implementation Notes

- Implemented strict own-change endpoint and scrypt replacement with atomic all-session revocation; wrong-current-password is typed authenticated 400, expired authority remains 401. No migration or S2/S3 feature.
- Account-first advisory lock is shared by login, session authorization (all business callers), browser-session revocation and account-scoped cleanup. Import revalidates after extraction. Admission uses separate persistent change buckets (100 global / 20 proxy / 5 account / 15 minutes) before replacement locks; existing login windows remain separate.
- Separate settings form preserves mounted main view on cancel, uses current/new autocomplete, warns all-device logout and blocks dirty/pending/import/confirmation work. Secrets clear on submit; lost/malformed replies lock presentation and require explicit logout/new-password login without replay.
- User instructions: [docs/password-change.md](../../../../docs/password-change.md). Protocol and caller inventory: [s1-locks-and-user-flow.md](s1-locks-and-user-flow.md).
- Mandatory physical tablet/PC touch, virtual keyboard/password-manager and owner acceptance: **utsatt – krever eier**. Story remains in-progress, not done.

## Spec Change Log

- Loop 1: B1/B2/B4/E1/E2 exposed incomplete Unicode, import ownership, lifecycle outcome and contention detail. Added explicit non-frozen constraints above to avoid truncation, silent outcome loss, voluntary review loss and nondeterministic race evidence. KEEP working protocol/guards/tests/UI documented; frozen scope unchanged.

## Review Triage Log

| ID | Verdict | Evidence / route |
|---|---|---|
| B1 | medium | New form uses native UTF-16 limits whereas Python uses code points; valid supplementary-character passwords can be truncated. bad_spec; group E1. |
| B2 | medium | changePassword returns on generation change after visibility hide; submitted operation outcome guidance can vanish. bad_spec; preserve truthful uncertainty without reviving stale private content. |
| B3 | medium | No injected post-hash/pre-revocation database failure test; atomic rollback contract lacks a regression oracle. patch test, incorporated in loopback. |
| B4 | medium | Competitor events precede PostgreSQL lock entry, so scheduling can avoid actual contention. bad_spec; require observed blocked DB lock before releasing winner. |
| B5 | medium | Existing expiry test expires before initial authorization; post-hash recheck is untested. patch, same root as V1. |
| B6 | medium | Exhaustion is tested but deadline rollover is not; regression could permanently throttle. patch deterministic stored-deadline test. |
| B7 | low | No boundary/whitespace cases despite unchanged no-trim policy. Direct test addition is appropriate; patch. |
| B8 | false | Requirement PM-UX3 is 200% text; evidence explicitly says CSS root text200% and browser emulation, with physical-device checks deferred. It does not claim actual browser zoom. Existing text-scaling evidence satisfies this specific automated claim. |
| B9 | medium | Error paragraph lacks input association/focus; keyboard and assistive users cannot identify the invalid field programmatically. patch direct aria association/focus correction. |
| B10 | medium | New clean-checkout harness instructions omit creating ignored DB secret and compose startup. patch docs. |
| E1 | medium | Same verified UTF-16 mismatch as B1; bad_spec group B1. |
| E2 | high | PrivateImport owns busy/review state but does not propagate it to new settingsBlocked; reset can voluntarily discard unsaved PDF review. bad_spec; block until explicit adopt/cancel. |
| V1 | medium | Pre-verified regression gap: removing final session check is undetected by current tests. patch post-hash expiry test, group B5. |

### Review round 2 (all three layers collected)

| ID | Verdict | Evidence / route |
|---|---|---|
| R1-B1 | medium | Existing dispatch marker remains null on CSRF/session preflight failure, yet catch labels it unknown and locks logout. A never-dispatched request can safely retain recoverable form/access state; direct marker guard and focused test: patch. |
| R1-B2 | false | For the cited hide/show trigger, workspace's generation check throws before returning a result, so changePassword cannot process confirmed success there; both tests assert uncertainty. A lock independently received from another tab must not be blindly cleared by password outcome presentation. No demonstrated confirmed-success/hide-lock path as claimed. |
| R1-B3 | low | logout's message treats changed as unknown if a pending logout from another tab subsequently locks this page. Direct conditional wording can preserve known success without clearing shared logout authority; patch. |
| R1-B4 | medium | Helper navigation resets component refs, so immediate login after success lacks a regression oracle. Patch test using the already-rendered login form. |
| R1-B5 | medium | Existing separate-context reload proves server revocation only, not same-context notification. Patch same-context already-open tab and remote visibility/revalidation assertions; group R1-V1. |
| R1-B6 | false | carried B8: same CSS-root-text-versus-zoom claim; PM-UX3 requires 200% text and evidence explicitly labels CSS text resizing, with actual-device checks deferred. No browser-zoom pass is claimed. |
| R1-B7 | medium | Login winning gate tested; replacement-first stale-login recheck lacks its own regression. Patch real blocker test for that ordering/no session creation. |
| R1-B8 | medium | Counters are DB-backed but separate-worker admission lacks executable regression evidence. Patch independent process continuation of an exhausted quota, without secret arguments or production operations. |
| R1-B9 | low | Cleanup is O(accounts), but already paginated at100 and one account/transaction, with only two expected users and no signup. Scale optimization adds discovery complexity for a defect not met in everyday approved use; reject low under workflow rule. No unlimited-use scale claim. |
| R1-B10 | medium | Setup snippet uses .NET APIs absent in Windows PowerShell5.1; explicitly require PowerShell7 in its heading/instructions. Parent documentation patch. |
| R1-V1 | medium | Pre-verified missing same-context password-change BroadcastChannel oracle; patch test, group R1-B5. |

Edge-case layer returned no findings. All surviving entries are small direct corrections or targeted regression oracles using existing demonstrated state; no new public API, product intent or state model. Re-engage implementation agent for patches, then parent reruns affected verification. No new spec loopback required.

## Design Notes
No independent intent gap blocks S1. Footprint is auth/private session callers plus change form/tests; isolated synthetic data mutations are authorized and reversible. Production untouched. Keep lock granularity per account; do not implement a global auth mutex. Use existing dependencies.

## Verification
Use `docker compose -f compose.password-tests.yaml exec -T private-api python -m pytest ...` against the new isolated project only, plus frontend build and local headless Playwright. Request tool escalation if Docker sandbox blocks access; this is authorized local testing. Parent owns harness setup and can provide readiness. No use of physical tablet even if connected. Owner-dependent UX acceptance is deferred, not done.

### Executed verification (2026-10-31, isolated synthetic project)

Baseline b352640c3cfb80b962db6056116e1c747cfb760a plus uncommitted S1 implementation; parent records reviewed commit. No production, real accounts, physical tablet, SSH or other runtime used.

- `docker compose -f compose.password-tests.yaml exec -T private-api python -m pytest tests/test_password_change.py tests/test_private_access.py tests/test_private_drafts.py tests/test_private_import.py -q`: **118 passed**, 199.74s (initial focused6; one expected read-only pytest-cache warning).
- Expanded `... python -m pytest tests/test_password_change.py -q -p no:cacheprovider`: **10 passed**, 19.40s (account/global/proxy admission, independent transaction barriers around login verification and actual draft save/revocation, competing changes, cleanup).
- `npm run build`: TypeScript and Vite passed. Browser build explicitly sets VITE_PRIVATE_API=http://127.0.0.1:18441 and VITE_FICTIONAL_API=http://127.0.0.1:18440; npm start serves the built preview.
- `COMPOSE_PROJECT_NAME=ibe160-password-tests npx playwright test tests/password-change.spec.ts --config=playwright.password.config.ts`: **10 passed**, 54.8s; headless Edge, real API/PostgreSQL, synthetic fixtures. Four blank Day/Night200% renders at768/1440px; includes uncertain replies after actual commit and dirty/pending business guards.
- Harness-only first launches: unanchored testMatch accidentally selected653 tests and was interrupted after guard/origin failures; parent fixed basename matching. A build without VITE override failed at CSRF fetch before login; rebuilt against isolated ports. Focused initial8pass/2fail were test navigation during initial business-list loading; helper now waits actual loading completion, all10 pass. No product failure waived.

Remaining verification results and preserved render evidence are recorded below.

Additional verification notes:

- Required browser regressions first exposed an initial-loading logout prompt from reusing the dirty flag for settings safety. Fixed with separate settingsBlocked propagation; legacy logout dirty behavior remains unchanged. Acknowledgements/classes block settings only while an unconfirmed review exists. A focused real plan-confirmation test covers release of this guard after acceptance.
- Isolated private-api service log scan found no synthetic new/current password or password-field markers. API access logging and forwarded-header trust remain disabled in app/run.py. This direct-API harness has no gateway; no proxy runtime log capture is claimed.
- Four blank-form renders are preserved in [evidence/s1](evidence/s1/README.md), with separate explicit physical-device deferral.

Final independent verification:

- `COMPOSE_PROJECT_NAME=ibe160-password-tests npx playwright test private-access.spec.ts private-identity.spec.ts private-recovery.spec.ts --config=playwright.password-regression.config.ts`: **62 passed**, 6.0m after settings-only guard fix. Covers identity switches, missing broadcasts, late responses, logout, session expiry, HTML failures, uncertain business operations and real isolated API stop/start. The subsequent settings guard relaxation only excludes already-accepted review decisions; its focused acceptance test is included below.
- `docker compose -f compose.password-tests.yaml exec -T private-api python -m pytest tests/test_password_change.py tests/test_cleanup_observability.py -q -p no:cacheprovider`: **14 passed**, 22.45s. Final focused10 now also asserts retained draft/workday/notice IDs, content, deadlines and receipts after new login, expired/oversized change rejection and unchanged change-window deadlines across ordinary login. Cleanup observability4 pass.
- Parent independently built `ibe160-password-gateway:s1` (manifest0963468d7dfd8a8115e5d4c1b50b02515f92aa6736ce0927ae7172b8b0d28dc2) and ran `./scripts/verify-tablet-proxy.ps1 -PythonImage ibe160-v1followup-gate-tests:20261029-r1 -GatewayImage ibe160-password-gateway:s1`: **PASS**, including synthetic password route admission/rejection/forwarding/no-store, gateway/upstream body-log absence, existing5×24 gate variants and unavailable-gate behavior. Separate ephemeral internal network, no DB/published ports, cleaned by script. Parent records detailed evidence in evidence/s1/proxy.md; this complements the direct-API evidence above.

- Final focused browser rerun after accepted-review guard adjustment: **11 passed**, 1.0m. Includes real unconfirmed decision/accepted plan navigation, all earlier scenarios and computed contrast assertions. Day/Night text contrast minimum 10.01:1; necessary input boundaries minimum 5.89:1; focused input ring 3px and minimum 11.45:1. All four final renders/JSON files preserved under evidence/s1.
- Independent test/AC mapping and render limitations: [evidence/s1/README.md](evidence/s1/README.md). Parent gateway evidence: [evidence/s1/proxy.md](evidence/s1/proxy.md).

- Final focused backend after adding explicit logout/import gate contention: `docker compose -f compose.password-tests.yaml exec -T private-api python -m pytest tests/test_password_change.py -q -p no:cacheprovider`: **12 passed**, 22.80s. No skips.
- Final frontend built bundle: `dist/assets/main-C5Mdu3xx.js`; selected implementation/test source SHA-256 fingerprints are preserved in [source-manifest.json](evidence/s1/source-manifest.json). No implementation commit/push performed; parent owns review/commit/session logging.

## Review loop 1 — corrected implementation constraints

No new product decision. Amend non-frozen implementation detail to close review findings; frozen intent unchanged. Parent reverted only this run's product/test edits to the recorded clean baseline, retaining harness/docs/evidence. Positive KEEP snapshots are in ignored tmp/s1-keep/manifest.json and files named by replacing path separators with double underscores. These are implementation references, not instructions to preserve the defects.

KEEP: shared account-first locking and atomic revocation; separate bounded admission; strict DTO/no-store/CSRF; preserved identities/business receipts; separate settingsBlocked from existing logout dirty flag; current settings navigation/form and 58px theme styling; all existing passing tests and user/locking docs. Re-derive those working changes from baseline, using KEEP snapshots to avoid losing verified behavior, with the following corrections:

- Align password entry/validation with Python Unicode code-point lengths (Array.from). Do not silently truncate; preserve existing 12–256 and no-trim policy. Fix the login password input as needed so newly changed valid Unicode credentials can subsequently sign in. Cover non-BMP and whitespace/boundaries, including correct old-password verification.
- Propagate PDF import processing and unsaved review state to settingsBlocked, clear only on adoption/cancellation/unmount; do not alter unrelated navigation/logout behavior. Test processing and review before explicit cancellation/adoption.
- Track only nonsecret password-operation outcome state across visibility/generation invalidation. Hide/clear secrets and private presentation as before; after a possible dispatched commit, returning must show truthful uncertainty or confirmed outcome and explicit login/logout action, never silently invite retry, restore stale data or automatically replay credentials. Test delayed actual commit plus hide/show and lost response.
- Make current-password/mismatch feedback programmatically associated with affected fields, aria-invalid and meaningful correction focus. No secrets in messages.
- Add failure injection after hash update before session deletion; require rollback of hash and all session mutations. Add expiry-during-hashing rejection with other live sessions preserved. Add deterministic admission expiry/reset independent from login, whitespace and length-boundary verification.
- Replace scheduler-only concurrency barriers with proof of DB contention (e.g. pg_locks/pg_stat_activity waiter and held lock on identified connection) before releasing winner. Preserve both save/change orderings, login, cleanup/logout/import and two changes.

Parent owns harness setup documentation fix B10; implementation agent need not modify scripts/compose/config. Rerun focused backend/browser plus relevant regressions after corrections; no mandatory owner check can be marked passed. Prior evidence remains historical pre-review results; record new results distinctly and refresh source fingerprints. Return files stable for repeat three-layer review.

### Review loop 1 implementation and verification (2026-10-31)

Restored the verified KEEP implementation from baseline, then corrected the specified defects without S2/S3/schema expansion. Browser password validation and login now count Unicode code points without native UTF-16 truncation. Input errors are associated with the invalid field and receive correction focus. PDF processing and unsaved review own a settings-only guard; adoption transfers responsibility to the unsaved draft, and cancellation/unmount releases it. A nonsecret password-operation outcome survives hide/show/generation invalidation, clears private presentation and secrets, and requires explicit resolution without credential replay. Logout resolution is disabled until the original password request settles, preventing a late outcome from interrupting that resolution.

Backend concurrency tests now identify connections and observe their actual PostgreSQL advisory-lock waiters/blockers before releasing each winner. Added real SQL failure after hash update and partial session deletion (complete rollback), expiry during replacement hashing (no replacement, other live sessions preserved), deterministic stored-deadline admission rollover independent from login, and exact Unicode/whitespace/boundary round trips.

- Focused backend: `docker compose -f compose.password-tests.yaml exec -T private-api python -m pytest tests/test_password_change.py -q -p no:cacheprovider` — **21 passed**,41.14s, no skips.
- Build: `npm run build` with isolated18441/18440 VITE overrides — passed; final bundle `main-BwmFAias.js`.
- Focused browser: `COMPOSE_PROJECT_NAME=ibe160-password-tests npx playwright test tests/password-change.spec.ts --config=playwright.password.config.ts` — **15 passed**,1.5m. The first run's13pass/2fail exposed the pending-completion/logout sequencing issue described above; corrected and rerun without waived failures.
- API log scan: zero fixed synthetic secret/field marker matches, no matching content printed. Parent independently rebuilt/reran the gateway checks for loop1; all passed, recorded in [proxy.md](evidence/s1/proxy.md).
- Corrected source fingerprints, four blank renders/contrast measurements and review finding/test map: [review-loop1 evidence](evidence/s1/loop1/README.md). Prior source manifest and evidence remain historical. All four text200% Day/Night768/1440 renders were visually inspected, with no clipping or secret content.

Mandatory owner/device checks remain **utsatt – krever eier**. Story remains in-progress; no commit/push by implementation agent.

Execution deviation: the inherited broad browser import suite ran two bundled anonymized-reference PDF cases before their source was identified; these are excluded from synthetic qualification evidence. Read-only teardown confirmed zero remaining import-test accounts and zero orphan import-related rows. Parent identified similar mapped-source consumers in the historical118-pass backend run, so that prior run is mixed synthetic/anonymized-reference regression. Focused loop1 backend21/browser15 use generated synthetic inputs. Details and exclusions: [loop1 deviation record](evidence/s1/loop1/README.md#input-source-deviation-in-inherited-regression-tests). No source PDF or synced project file was changed.

Final relevant browser regressions: `COMPOSE_PROJECT_NAME=ibe160-password-tests npx playwright test private-access.spec.ts private-identity.spec.ts private-recovery.spec.ts private-import.spec.ts --config=playwright.password-regression.config.ts` (after the parent-owned adapter) returned **78 passed/1 failed**,9.4m. Excluding the two anonymized-reference passes,76 synthetic cases passed. The single failure was initial background reads being intercepted by the existing recovery test's broad session-failure injection before its save click; added observable initial-load completion waits in that test. Refreshed adapter, then `... npx playwright test private-recovery.spec.ts --grep 'fresh save preflight failure' --config=playwright.password-regression.config.ts`: **1 passed**,9.6s. Final total is **77 distinct synthetic regressions passed** across the broad and targeted runs; no application failure waived. Source fingerprints include this test correction; `git diff --check` passed. No further source-reference cases were run.

### Targeted review patch

Corrected the null-dispatch failure path to report **not sent**, retaining recoverable form/access state without overriding session suspension or expiry guards. Confirmed password-change wording now stays confirmed after shared logout locking. No other product behavior changed.

Added immediate new-password login without navigation, same-context broadcast-only revocation with zero requests, separate-context visibility/session revalidation without reload, failed-CSRF/session-preflight recovery without POST/replay, and confirmed-outcome/shared-lock coverage. Added replacement-first PostgreSQL contention with waiting old-password login rejected/no session created, and an independently started process proving persistent change quota plus ordinary-login independence (secrets stdin-only).

Targeted results: backend `tests/test_password_change.py -k 'replacement_wins_before_waiting or budget_persists_in_independent' -q -p no:cacheprovider` **2 passed/21 deselected**,5.84s; build passed (`main-stthgplt.js`); browser `tests/password-change.spec.ts --grep 'real change|password preflight|confirmed password outcome|typed rejection|uncertain|hide/show' --config=playwright.password.config.ts` **11 passed**,1.2m. Initial10pass/1fail revealed settings helper timing against initial draft loading; added observable loading completion and reran the same focused cases successfully. No wider suite rerun. Full commands, refreshed fingerprints and retained prior manifest: [targeted patch evidence](evidence/s1/loop1/README.md#targeted-review-patch-2026-10-31).

Owner/device checks remain **utsatt – krever eier**; source-input deviation remains recorded. Parent owns full verification and commits.

### Parent final verification and review outcome

After all round-2 patches, parent independently ran password/access/cleanup backend suites: **41 passed in75.07s**; full focused browser package: **18 passed in1.8m**, no skips. Exact commands: `docker compose -p ibe160-password-tests -f compose.password-tests.yaml exec -T private-api python -m pytest tests/test_password_change.py tests/test_private_access.py tests/test_cleanup_observability.py -q -p no:cacheprovider`; frontend `COMPOSE_PROJECT_NAME=ibe160-password-tests npx playwright test --config playwright.password.config.ts`. Only generated synthetic input, no reference-file mount. Parent read the changed product/test diff and checked matrix coverage, reviewed every finding from both three-layer rounds, verified all accepted patches and rejected findings with recorded evidence. Markdown links and git diff --check pass. No unresolved verified product defect remains from S1 review; physical/owner gates remain deferred, so status stays in-review. Technical dependencies are ready for S2.
