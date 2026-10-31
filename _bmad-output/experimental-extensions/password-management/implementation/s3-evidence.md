# PM-E1-S3 — implementation and isolated evidence

Baseline: `273e5b701e5e8fe866009ae6e38bf7c326d379d4`, experimental checkout `password-management-planning`. Parent owns reviewed commit/push and final review. This records technical work, not owner acceptance or live readiness.

## Implementation

`POST /auth/password/recover` accepts only username/code/new_password/confirmation, with strict DTO and existing Origin, signed double-submit CSRF, bounded body, safe validation and no-store boundary. A live cookie produces neutral409 and requires explicit logout. Its authorization transaction releases any B account gate before recovery admission/A gate; an opaque rejected/expired token cannot change owner or revive. No reset session or automatic login is created.

`password_recovery.redeem` uses S2's one-active-proof state and purpose, normalized username binding, fixed-size SHA-256 constant-time comparison and one scrypt hash on every admitted attempt (including malformed/unknown/wrong-account). Expiry uses the DB clock after hashing. Under S1's account gate it consumes the candidate, calls shared `auth.replace_password`, invalidates remaining active proofs and deletes every account session in one transaction. Existing change audit records truthful `recovery-proof:<UUID>` actor for this code-authorized change; no operator identity is fabricated. No migration, account recreation, retention or business-data changes.

Recovery admission uses independently committed `recover:` buckets in existing login_limits: global100 → proxy20 → normalized-name digest5 /15min, separate from login/change. Global/proxy rejection cannot allocate a new user bucket. Failed credential/rollback transactions retain attempts; expired windows reset without permanent ordinary-login lockout. Invalid proof outcomes share400 and the same neutral text. Controlled repeated timings test comparable work, not identical network timing.

The small login-adjacent form supports paste, code-point lengths, associated feedback, correction focus, cancel/focus return and current themes. Submission clears fields. Visibility/BFCache or session-change notifications unmount recovery fields. Only nonsecret pending/unknown/changed metadata survives lifecycle interruption; HTML/malformed/lost/timeout replies produce uncertainty and explicit logout/new-password login/operator reissue, never automatic credential replay. Existing signed-in dirty/pending/import protection and all-device revalidation remain in place. A wrong-account workspace exposes recovery only after explicit logout.

## Tests and preserved evidence

All DB work uses `compose.password-tests.yaml -p ibe160-password-tests`, `PRIVATE_TEST_PROJECT=ibe160-private-tests`; synthetic-account guard runs before fixtures. No DB-mutating suites overlap. API18441/UI15440/fictional18440 only. Final build uses `VITE_PRIVATE_API=http://127.0.0.1:18441` and `VITE_FICTIONAL_API=http://127.0.0.1:18440`; isolated private-api restarted after Python changes. Browser execution requires sandbox escalation for Windows loopback/Edge. Trace/video/automatic screenshots are disabled. Only blank form screenshots and numeric contrast JSON are generated under `tmp/password-recovery-evidence/`; the final four renders/metrics and source fingerprints are retained in tracked [evidence/s3](evidence/s3/README.md).

Backend source: `backend/tests/test_password_recovery.py`:

- `test_full_recovery_preserves_data_sessions_receipts`: UUID, draft/workday/notice content, original deadlines and authorized historical receipts survive; all A sessions fail, B remains live, separate new login required; digest-only persistence.
- `test_generic_invalid_states_no_mutation`: malformed, wrong, unknown, control-name, wrong-account, exact-deadline/expired, replaced, revoked, consumed; identical public shape and no mutation.
- `test_boundaries_and_live_other_session`, `test_expired_cookie_has_no_authority`: strict input/extra fields, CSRF/Origin/body, no private read, live B conflict and expired cookie.
- `test_expiry_while_hashing`: real deadline crosses during hash; proof remains unused.
- `test_true_database_contention`, `test_obsolete_code_waits_for_preceding_mutation`, `test_login_committed_before_recovery_is_revoked`: actual pg_stat_activity/pg_blocking_pids account-lock blockers; two redeemers and both issue/revoke/change/login orderings use actual lifecycle services. No scheduler-only race claims.
- `test_rollback_after_partial_replacement`: real SQL failure after replacement restores hash/proof/sessions while committed admission remains.
- `test_persistent_parallel_budget_and_expiry`, `test_global_and_proxy_precede_bounded_unknown_buckets`: concurrent limits, stored rollover, global-before-new-name bound, ordinary login independent.
- `test_controlled_failure_processing`: three samples/class, one hash each, bounded median comparison for known malformed/unknown/wrong-account; no perfect-latency claim.
- `test_operator_terminal_to_app_own_account_without_app_password`: actual synthetic PTY command and app API redemption/new login, no app password/session used to obtain recovery authority; captured code compared only in memory.

Browser source: `frontend/tests/password-recovery.spec.ts`: terminal→browser→new login, remote-device revocation, wrong-code focus/clearing/cancel, lost/HTML/malformed/timeout/hide-lost uncertainty, BFCache/visibility clearing, code-point/whitespace policy, explicit wrong-account dirty logout, offline preflight/no replay, sibling-tab login invalidation, blank Day/Night tablet/PC200% renders/contrast. API logs are captured internally and checked for synthetic secrets without printing them.

Shared regressions: S1 real-gate tests additionally cover private read/write/import/logout/cleanup common lock ordering and rollback; S2 covers issue/revoke/cleanup/TTY safeguards. Existing synthetic browser adapter excludes approved-example PDF tests. No synced reference PDF is used.

## Test-run history

- Initial S3 backend:18 passed/4 failed due test fixture timestamp drift, duplicate helper parameter, and an unrealistic expiry mutation after service snapshot. Corrected tests; no production credential state involved. Verbose pytest fixture rendering exposed a generated synthetic fixture password in tool output (not a real secret or stored evidence artifact). Subsequent runs use `--tb=short`, and Shared backend fixture repr now redacts credentials; no value is reproduced here.
- Combined backend (`python -m pytest -q --tb=short -p no:cacheprovider tests/test_password_recovery.py tests/test_password_change.py tests/test_password_recovery_operator.py tests/test_private_access.py`):91 passed in147.31s before added opposite-order/control-name cases.
- Expanded S3 backend:27 passed in40.85s before replacing opposite-order fixture writes with actual lifecycle calls; final rerun recorded below.
- Initial focused S3 browser:11 passed in1.1m. Combined browser:28 passed/1 failed due intermittent recovery error focus attempted before input re-enabled. Fixed with post-render focus effect; final rerun recorded below.
- Blank render review found test-only mismatched theme label from direct DOM theme mutation. Test now uses the actual ThemeControl toggle; final renders regenerated below. SSH/Access operational detail was removed from the small form and remains in user/operator docs.

## Owner and release deferrals

Physical tablet/PC touch and virtual keyboard, real password-manager behavior, real independent SSH/MFA/outer Access, identity/contact/capture-free handoff, operator absence practical routine and owner acceptance are **utsatt – krever eier**. Synthetic PTY/browser checks do not qualify these. Gateway harness is parent-owned and S4 combined restore/rollback qualification remains separate. No production, actual identities, physical devices, deployment, merge, tag or release. Do not mark story done or live-use ready.

Runbook explains code consumption before MOTTATT: operator ACK rejection is not proof the app reset failed; check app/new login first, do not issue a new code automatically. The existing S2 candidate-only compensation remains unchanged.

## Final verification

- Final build: `VITE_PRIVATE_API=http://127.0.0.1:18441 VITE_FICTIONAL_API=http://127.0.0.1:18440 npm run build` — TypeScript and Vite pass; bundle `main-FSk_H7M3.js`.
- Final S3 backend: `docker compose -f compose.password-tests.yaml -p ibe160-password-tests exec -T private-api python -m pytest -q --tb=short -p no:cacheprovider tests/test_password_recovery.py` — **27 passed in41.39s**, including actual opposite-order services, redacted fixture and normalized-name safeguards.
- Combined S1/S3 browser before final legacy-integration correction: `COMPOSE_PROJECT_NAME=ibe160-password-tests npx playwright test --config playwright.password.config.ts` — **31 passed in3.0m**, including actual terminal→browser, log absence check, corrected focus, offline preflight and sibling-tab invalidation.
- Final regenerated blank tablet Night and PC Day renders were visually inspected by implementer and parent: correct theme label, legible focus/text/controls, no visible clipping at200%. All four numeric contrast files pass ≥4.5 text and ≥3 necessary nontext; 3px outline and ≥58px controls. This is emulated/automated evidence only.
- `git diff --check` passes (line-ending normalization warnings only).

### Legacy integration correction and verification-output incident

The first selected legacy browser regression run exposed two real integration regressions: a session-change notification overwritten settled logout status, and ordinary unfinished login password input being cleared on hide. The run was stopped after these failures. Final implementation scopes the additional notification clearing to an open recovery form and preserves pre-existing ordinary-login hide behavior. Recovery form unmounting still clears its secrets. The corrected delayed-login/logout and unfinished-login tests pass in the rerun.

Verification-output incident (both occurrences): initial pytest fixture rendering and a legacy Playwright value assertion each echoed a generated synthetic fixture password in tool output. Neither was a real credential or recovery code; values are deliberately omitted here. Shared backend fixture repr is now redacted, pytest uses `--tb=short`, and the legacy unfinished-password assertion now compares a boolean with a static message while preserving the same expected behavior. No claim is made that earlier test failures were universally secret-free. No credential-bearing screenshot/trace/video or tracked evidence artifact was created; prior failed-run scratch output was replaced by the next Playwright run.

- Final selected legacy browser regressions: `COMPOSE_PROJECT_NAME=ibe160-password-tests npx playwright test --config playwright.password-regression.config.ts private-access.spec.ts private-identity.spec.ts private-recovery.spec.ts private-import.spec.ts private-owner-import.spec.ts` — **82 passed in7.6m** after the scoped lifecycle fixes; synthetic adapter regenerated, approved-reference PDF examples excluded. Includes real isolated API stop/start, identity races and generated-PDF journeys.
- Final S3 browser on the corrected build with secret-safe polling oracles: `COMPOSE_PROJECT_NAME=ibe160-password-tests npx playwright test --config playwright.password.config.ts password-recovery.spec.ts` — **13 passed in1.2m**. Blank four-theme/viewport artifacts regenerated and copied to tracked evidence.

## Final handoff snapshot

- **99 backend tests passed in157.46s**: final combined S3/S1/S2/access command above, with the shared redacted fixture and all S3 secret-dependent assertions evaluated into booleans before static assertions.
- **82 existing browser regressions passed in7.6m**, **13 S3 browser tests passed in1.2m**, on final bundle `main-FSk_H7M3.js`. The legacy unfinished-login assertion was subsequently changed to the equivalent retrying boolean poll; its targeted rerun passed1/1 in5.7s. No product behavior changed in that assertion adjustment.
- A real API JSON-escape probe confirmed lone-surrogate username, code and new-password fields each receive sanitized422 before recovery admission (Pydantic rejects invalid Unicode). Tightened `test_escaped_surrogate_is_bounded_safe_api_rejection` then passed3/3 in2.98s, asserting exact422/body and zero recovery buckets/sessions. Service-side guards also remain bounded for direct callers.
- Source/test SHA-256 fingerprints are retained in [evidence/s3/source-sha256.json](evidence/s3/source-sha256.json). Final blank renders/contrast are tracked alongside them.
- No suites remain active at handoff. Parent owns independent review, gateway harness, reviewed commit/push and session log. Physical/operator/owner qualification remains **utsatt – krever eier**, and S4 is still required.

## Review correction pass (parent triage preserved)

Applied bounded corrections for B1/B3–B7/B9/B10/E1 and the real429 coverage request; parent-owned triage rows, including B2/B8 dispositions, are unchanged.

- Confirmed recovery after visibility retains the shared pending logout safety lock. If that lock remains, success explicitly directs «Prøv utlogging igjen» before new login; it does not clear another tab's logout request.
- Only the exact canonical invalid-code400 detail is treated as definite rejection. Unrelated400 after a committed recovery stays uncertain, without credential replay.
- Recovery field-error association and correction focus are separate. API clearing explains full re-entry and focuses the first required empty field; invalid-code feedback remains associated with code. Transport/rate feedback is form-level, and editing the invalid field clears its stale error/aria-invalid state. Local validation retains its affected-field focus.
- Browser tests now exercise actual409 with a live B cookie and missed broadcast (A hash/proof unchanged, B restored, explicit logout still needed), actual429 after exhausting the persistent recovery budget, unrelated400 after commit, and delayed confirmed success through explicit logout/new login.
- Invalid-state backend snapshots now include every proof field and audit row; success asserts exact target/action/result/recovery-proof actor; SQL-failure rollback compares audit/proof/account/session snapshots. Secret-bearing comparisons remain boolean/static assertions.

Scoped verification only, after parent released the DB/UI lane:

- Build/TypeScript pass; preview bundle `main-DnQxIuR2.js`, isolated18441/18440 build-time API values.
- `python -m pytest -q --tb=short -p no:cacheprovider tests/test_password_recovery.py -k 'generic_invalid_states or full_recovery_preserves or rollback_after_partial'` — **11 passed,19 deselected in15.58s**.
- `COMPOSE_PROJECT_NAME=ibe160-password-tests npx playwright test --config playwright.password.config.ts password-recovery.spec.ts` — **17 passed in1.6m**.
- Blank render/contrast case reran; copied evidence only if content changed, refreshed source fingerprints. No credential-filled render or wider verification run. Parent owns full independent verification.

## Parent final verification after review patches

Parent inspected every patch and its test oracle. Combined `docker compose -f compose.password-tests.yaml -p ibe160-password-tests exec -T private-api python -m pytest -q -p no:cacheprovider --tb=short tests/test_password_recovery.py tests/test_password_change.py tests/test_password_recovery_operator.py tests/test_private_access.py tests/test_cleanup_observability.py`: **103 passed in156.73s**. This includes final S3, S1, S2, access and cleanup on synthetic data only. All nine recorded source fingerprints match; four S3/operator/evidence Markdown documents have no broken relative links. New origin/main fetch remains5cee9e03d03d2c9c165c7f8fec64aa3e146959ab and the other V1 checkout is clean. Parent final focused browser result follows after its run; no parallel DB-mutating suites.

Parent final focused browser command: COMPOSE_PROJECT_NAME=ibe160-password-tests npx playwright test --config playwright.password.config.ts — **35 passed in3.3m** on final reviewed build (18 S1 +17 S3). No new verified product finding remains after all12 review items were triaged and patches inspected. Earlier82 selected legacy regressions remain applicable; review patches affect bounded recovery feedback and shared confirmed-outcome wording, covered by the final35. Owner/SSH/handoff/device controls and S4 remain pending.
