---
title: 'PM-E1-S2 — Operator recovery code lifecycle'
type: feature
created: '2026-10-31'
status: in-review
route: dispatch
review_loop_iteration: 0
baseline_commit: 3839f0d4b7cc8954da5f399d512565f8c91a9b7a
context:
  - ../planning/epics.md
  - ../planning/technical-contract.md
  - ../planning/coverage.md
  - epic-PM-E1-context.md
  - s1-locks-and-user-flow.md
---

<frozen-after-approval reason="Owner authorized sequential PM-E1 implementation with synthetic-only testing and deferred owner gates">
## Intent
Implement PM-E1-S2 only: Jonas issues/revokes a time-limited one-use recovery proof for an exactly confirmed account through independent server access, including his own app account without any app session/password. All S2-AC1..8 apply. No redemption endpoint/UI until S3.

## Boundaries & Constraints
Keep existing UUIDs, hashes, sessions and business records unchanged by issuance/revocation. Password replacement in S1 must invalidate outstanding proof atomically. Preserve S1 concurrency, admission, form and regression fixes. No email, admin panel, registration, production/real accounts, physical tablet, SSH/MFA interaction, merge/deploy/tag/release. Work only in this isolated checkout, codex/plan-password-management. Parent owns commits/push and consolidated session log; agent does not commit or push. Owner unavailable: mandatory practical identity/contact/handoff/no-recording qualification is `utsatt – krever eier`, not a technical coding blocker or a passed check. Do not mark story done.

## I/O & Edge-Case Matrix
| Scenario | Input | Outcome | Failure |
|---|---|---|---|
| Exact operator target | normalized exact username, resolved UUID and typed full username confirmation | issue/revoke that UUID without app credentials | unknown/mismatch/cancel/noTTY no mutation |
| Proof lifecycle | issue/reissue/revoke, timeout/cleanup | 256-bit random, digest only,30min DB TTL,one active,3 issues/account/hour,revoke always possible | idempotent revoke,expired unusable,old proof invalid |
| Terminal delivery | approved interactive nonrecorded controlling terminal | show code once only after DB commit, expiry/timezone,clear on ACK | redirect/nonTTY reject; delivery failure revoke or report uncertain, no code stdout/stderr/logs |
| Atomicity/concurrency | issue/revoke/change/cleanup/DBfailure | shared account-first gate, no partial state, change revokes proof in same tx | actual PostgreSQL contention evidence |
| Migration/data | existing synthetic users/drafts/days/notices/receipts | additive/repeatable migration,stable IDs/hash/deadlines and login/provision | restore/rollback operational gate recorded for S4 |
</frozen-after-approval>

## Code Map
- backend/app/manage.py: existing private-mode migrate/cleanup/provision CLI; add recovery-issue USERNAME and recovery-revoke USERNAME. No secret command args/env/files or fuzzy matching. Never render control characters in account names as terminal control sequences; fail safely for unconfirmable names without changing stored accounts. Use exact normalized username+immutable UUID display and full username confirmation. Separate host/operator context from app identity; don't invent verified SSH attribution from shared container user.
- backend/app/auth.py: account_lock, change_password, existing hash/admission. Reuse common transaction replacement helper if needed; integrate proof invalidation atomically with S1 and preserve all prior behavior.
- backend/migrations/private: inspect current numbering (baseline latest014); use next unused migration, minimal recovery proof+audit/issuance-limit structures. FK owner, purpose/state/expiry constraints, digest uniqueness, one active proof, expiry index. No account schema needed.
- backend/app/private_storage.py: bounded account-gated cleanup; integrate digest removal within24h and minimal audit30d without touching business retention. Avoid row/account lock inversion.
- Add bounded recovery service and terminal helper as justified; no dependency/service required. Generate proof only for valid confirmed target; use CSPRNG≥256bits and SHA256 digest, not a human password hash for code.
- backend/tests/test_password_recovery_operator.py: actual DB + PTY synthetic CLI tests; private test guard and fixture conventions in test_private_access.py. Terminal tests run inside Linux private-api container; capture synthetic output only internally and never print code on test failure.

## Tasks & Acceptance
- [x] Implement S2 CLI/service/migration/cleanup and S1 proof invalidation, preserving all S2-AC1..8 and S1 safety.
- [x] Reject noninteractive/stdin/out/err redirection and missing controlling terminal. Document recording detection limits; an explicit preflight acknowledgement can support operator routine but never proves capture-free execution. Code direct to controlling terminal after commit only, display once/clear on ACK, no retrieval API. Handle failed delivery/interrupt with safe revoke and secret-free uncertain status.
- [x] Persist minimal actor/action/target/time/result audit only. If host only supplies an OS/container context, label it honestly; trusted SSH attribution is a separate operational correlation. Don't accept unverified actor label as verified identity.
- [x] Execute exact selection/cancel/mismatch/unknown/repeated revoke/reissue/issuance caps and real contention tests, failure rollback and terminal output/log/DB-plaintext scans. Issuance works with no app cookie/password for own synthetic account. Include pipe/redirect negative cases and terminal commit/delivery ordering.
- [x] Apply/reapply migration against retained synthetic records, test login and provisioning; capture IDs/content/hash/deadlines before/after. No destructive command against any non-synthetic database; service tests use require_synthetic_accounts. Test cleanup clocks and active/expired proof behavior without waiting30min.
- [x] Write implementation/operator-runbook.md and concise implementation notes: actual command syntax, existing Ubuntu path as future operator instructions only, identity/target/handoff/no-transcript preflight, own-account SSH recovery, absent operator, expired/failed handoff revoke/reissue, independent outer Access/SSH loss. Explicitly prohibit live issuance until S3/full journey and owner qualification.
- [x] Run focused suite and relevant S1/access/cleanup regressions, record exact pass/fail commands and sources. Parent's isolated compose remains available; don't modify harness concurrently.

## Implementation Notes

Implemented on baseline `3839f0d4b7cc8954da5f399d512565f8c91a9b7a`, uncommitted agent changes for parent review. `015_password_recovery.sql` adds proof/audit tables only; account-first `password_recovery.py` handles exact target revalidation, three successful issues per rolling hour, atomic supersession, idempotent revoke and bounded cleanup. Proofs use 32 CSPRNG bytes and SHA-256; database time sets the 30-minute deadline. S1 password replacement invalidates active proof inside its existing transaction. Existing account/session/business schema and retained records are unchanged.

`recovery_terminal.py` requires all three standard descriptors to be the same foreground TTY plus an accessible controlling terminal. Exact normalized username + UUID confirmation and explicit no-recording/identity/handoff acknowledgement precede generation. Direct `/dev/tty` display follows commit, uses UTC expiry and an alternative screen, and clears on acknowledgement. Cancellation, signals and delivery/teardown failure compensate by a candidate UUID allocated before issuance, including ambiguous commit; compensation never revokes an older or newer different proof. Explicit recovery-revoke still revokes all outstanding proof. If compensation cannot commit, secret-free USIKKER status directs explicit revoke. Kernel UID is honestly labelled OS/container context, never verified SSH identity.

See [operator runbook](operator-runbook.md). No public redemption endpoint/UI, dependency, SSH interaction, real account, release, deploy, commit or push was added/performed. Parent owns consolidated session log and review. Story remains in progress: practical identity/contact/handoff/no-recording and device/owner qualification are **utsatt – krever eier**. S3/full journey and qualification prohibit live issuance; restore/rollback is S4's operational gate.

### Executed technical evidence — 2026-10-31

All commands use `docker compose -f compose.password-tests.yaml -p ibe160-password-tests`, separate synthetic volumes, API18441 and PRIVATE_TEST_PROJECT guard. No concurrent DB-mutating suite ran. `exec -T` here runs pytest, whose children create actual Linux PTYs; actual operator invocation itself rejects `-T`.

- `exec -T private-api python -m app.manage migrate`: passed, migration015 applied. Focused retained-business test replays first-addition SQL in a rollback transaction after dropping only S2 metadata tables, compares IDs/content/hash/ownership/deadlines for accounts/sessions/drafts/days/notices/receipts, then calls normal migration twice and tests issue/revoke preservation. Legacy login and newly provisioned synthetic accounts are covered.
- Initial direct `pytest` invocation: collection failed (`app` import path); corrected to `python -m pytest`. Initial focused run: 9 passed/5 failed; fixed incorrect `/dev/tty` alias-device identity comparison and microsecond mismatch in test-only expiry fixture.
- `exec -T private-api python -m pytest -q -p no:cacheprovider --tb=short tests/test_password_recovery_operator.py tests/test_password_change.py tests/test_private_access.py`: **51 passed**,95.22s (14 S2 tests at that point).
- `restart private-api`: passed, isolated service loaded updated S1 proof invalidation.
- `exec -T private-api python -m pytest -q -p no:cacheprovider --tb=short tests/test_password_recovery_operator.py tests/test_password_change.py tests/test_private_access.py tests/test_cleanup_observability.py`: **60 passed**,99.08s (19 S2 tests at collection). Covers real S1/API/access/cleanup regressions after restart.
- Final `exec -T private-api python -m pytest -q -p no:cacheprovider --tb=short tests/test_password_recovery_operator.py`: **23 passed**,31.93s. Includes PostgreSQL observed account-lock waiters for issue/revoke/change/cleanup, concurrent issuance cap, transactional rollback, atomic change invalidation, retained records, terminal commit-before-display, redirects on each descriptor, missing controlling terminal, interrupt, exact selection, cancel/mismatch, repeated revoke, one display/clear, failed delivery, failed compensation and teardown-after-ACK, candidate-only compensation preserving old/new concurrent proofs. No app credentials are supplied by PTY children.
- In-memory `logs --no-color private-api private-db` scan: **passed**, no `Engangskode:` disclosure prefix, synthetic new-password or delivery-failure marker. Initial sandbox Docker log read was denied; authorized isolated read with escalation passed. Raw logs and captured synthetic codes were not written to evidence. DB plaintext scan is inside `test_lifecycle_digest_limit_preservation`; PTY captures remain internal and assertions suppress codes.
- `git diff --check`: passed (existing line-ending warnings only).

Test source: `backend/tests/test_password_recovery_operator.py`; fixtures/guard from `test_private_access.py`. Counts overlap: final suite has23 S2 tests plus37 S1/access and4 cleanup tests in the combined run (64 distinct). Synthetic tests do not establish a capture-free real SSH session or owner handoff. SIGKILL/power loss cannot be trapped; operator revoke/TTL remain required. Cleanup's within24h digest-retention obligation requires the established scheduled job to remain healthy. Audit can be absent when the database itself is unavailable; absence is not proof of outcome.

## Spec Change Log

## Review Triage Log

| ID | Verdict | Evidence / route |
|---|---|---|
| B1 | medium | Blocking terminal read has no lifetime; secret remains on abandoned screen. Patch bounded read/dialogue and cleanup. |
| B2 | medium | Same abandoned dialogue holds existing host operations lock. Same patch as B1, retain release consistency. |
| B3 | medium | SIGTSTP can suspend with secret/echo state. Patch handled interruption and restoration. |
| B4 | medium | Acknowledgement checks target but not candidate validity. Patch locked active/expiry recheck. |
| B5 | medium | Explicit revoke DB failure reports only no-code; outcome may be uncertain. Patch explicit retry guidance. |
| B6 | low | Schema includes change action but change invalidation has no minimal audit. Patch atomic change/revoked event. |
| B7 | low | Direct resolve strips control whitespace before validation unlike host helper/runbook. Patch validate original string. |
| B8 | medium | PTY waitpid/finally can hang/leak children. Patch bounded wait and guaranteed reap. |
| B9 | medium | Missing rolling-window and fresh-proof cleanup oracles confirmed. Patch boundary/preservation tests. |
| E1 | medium | Same verified issue as B4; patch candidate check. |
| E2 | medium | Inline digest assertions can introspect code arguments on failure. Patch boolean-only assertion messages. |
| E3 | medium | Same verified issue as B8; bounded PTY helper. |
| V1 | medium | Preverified rolling-window gap; same patch as B9. |
| V2 | medium | Preverified active-proof cleanup gap; same patch as B9. |

All three context-free review layers completed before triage. Routes are bounded patches to demonstrated paths; no new public surface or product decision. Parent will verify affected suites after implementation-agent corrections.

## Design Notes
The technical contract supplies engineering defaults; no new product choices are needed. Operational capture/contact qualification remains owner-dependent. If a product choice unexpectedly blocks a point, record it and continue independent tasks without guessing.

## Verification
Use only compose.password-tests.yaml, project ibe160-password-tests, API18441/fictional18440/UI15440, separate volumes. Backend marker PRIVATE_TEST_PROJECT=ibe160-private-tests is already set for guard compatibility. Docker escalation may be required for these authorized isolated tests. No concurrent DB-mutating test suites. Use actual PTY inside disposable container; never invoke real SSH or tablet. Keep secrets out of artifacts and don't claim actual-owner handoff or deployment qualification from simulation. Parent conducts BMAD three-layer review before S3.


## Existing Ubuntu entry point — completion detail before review

Read-only inspection confirms the deployed operator role uses the root-owned `bussassistentctl` helper, not general Docker/sudo access. Merely documenting raw docker commands would leave the approved server-access capability without its established entry point. Implement the necessary bounded integration in repository source only: `deploy/ubuntu/bussassistentctl.py` accepts exactly `recovery-issue USERNAME` and `recovery-revoke USERNAME`, resolves the validated current release, uses the existing fixed project/config/service and invokes only `python -m app.manage` for that operation. No arbitrary command/flags/project/path passthrough and no shell interpolation. No sudoers/bootstrap/production configuration change, new administrator or broader host permission; the existing helper already carries the approved administrator/deployer role.

Before allocating Docker's inner TTY, the host helper must refuse noninteractive/redirected stdin/stdout/stderr and verify its controlling foreground terminal. Route the Docker client's streams explicitly to that controlling terminal, never captured/logged output or ordinary redirected stdout/stderr. The inner CLI guards remain. This closes the outer-Docker-redirection gap: a forced inner TTY otherwise hides host redirection from the app CLI. SSH-client/sudo recording cannot be proven absent by either check and remains manual owner qualification, not a claimed technical guarantee.

Add synthetic/no-production tests to `deploy/ubuntu/test_operations.py`: exact command/target args, extra args/invalid/control names refused, redirected/missing/foreign terminal refuses before Docker, streams routed to controlling terminal, helper's existing release/lock boundaries retained. Mock subprocess and filesystem roots or use private PTYs; never call the fixed production project during tests. Run the existing operations test suite in a disposable Linux environment with production subprocess calls mocked; preserve its non-root chown-testing pattern.

Update operator-runbook.md with the actual bounded helper invocation as a future deployment instruction, and record that this helper revision is NOT installed on the live host. Ordinary later reviewed helper installation/deployment and practical owner terminal/recording checks remain `utsatt – krever eier`; do not invent a new privileged-entry approval or bypass existing restrictions. Direct Docker commands may remain clearly synthetic-only test instructions. This is necessary implementation of the already approved administrative command via existing server access, not a new product decision or permission to deploy. Complete this before formal S2 review; preserve all passing S2 code/tests.

### Completion evidence — existing helper integration

Repository-only `bussassistentctl.py` now accepts exactly recovery-issue/recovery-revoke plus one normalized username. Invalid/control names and extra arguments fail before Docker; validated current release, fixed project/config/service and argument-array subprocess dispatch are retained. Host stdin/out/err must share a foreground controlling TTY before Compose's inner TTY allocation; all three Docker streams explicitly use the opened `/dev/tty` descriptor. No captured output or shell interpolation. Existing root check and exclusive `/run/lock/bussassistent.lock` boundary are unchanged, extracted into testable `entrypoint()`. No sudoers, bootstrap or production change.

`deploy/ubuntu/test_operations.py`: **18 passed**,0.084s, including all12 existing operations tests and6 new helper tests. Tests cover exact command routing and normalized target, rejected extra/invalid/control arguments, each redirected descriptor, missing/foreign/background terminal, invalid current-release target, root/lock boundary, and actual Linux PTY success plus each outer redirection. All operations subprocess calls are mocked; no production project is invoked. Non-root chown pattern is preserved by wrapping the test runner in `unittest.mock.patch('os.chown')`.

Executed only in disposable `ibe160-password-tests` private-api: created `/tmp/s2-helper`, copied the two repository helper/test files there using Compose cp, then `docker compose -f compose.password-tests.yaml -p ibe160-password-tests exec -T private-api python -c "import runpy,unittest.mock; p=unittest.mock.patch('os.chown'); p.start(); runpy.run_path('/tmp/s2-helper/test_operations.py',run_name='__main__')"`. No product/backend code changed during this completion detail, so previously passing S2/S1 suites were not repeated. Runbook now documents the actual future `sudo -n /usr/local/sbin/bussassistentctl recovery-issue USERNAME` / recovery-revoke entry point. Helper revision is not installed live; later reviewed deployment and owner no-recording qualification remain deferred.

### Implemented review corrections — focused evidence

Preserved the parent's14-finding triage above. The operator dialogue now has a five-minute whole-session alarm; at secret display its remaining deadline is additionally capped by the exact candidate's remaining database TTL. Timeout and SIGINT/SIGTERM/SIGHUP/SIGTSTP unwind clear/terminal restoration and candidate-only compensation instead of leaving an abandoned or suspended prompt. Explicit revoke records that it was attempted and returns secret-free USIKKER/retry-revoke guidance on ambiguous failure.

Before delivery audit success, the same account gate revalidates the exact candidate UUID as active and unexpired. Concurrent revoke/replacement/expiry cannot produce acknowledged delivery; newer proofs survive old-candidate compensation. Password change adds change/revoked audit in the same transaction with authenticated app-account UUID actor context. Original username controls are rejected before stripping/casefolding.

PTY tests now enforce a30-second overall child deadline, bounded termination/reaping in finally, and restored terminal modes. Secret-dependent digest/display/plaintext checks compare precomputed booleans with static assertion messages. Added rolling-hour admission recovery, preservation of fresh active proof/recent audit during cleanup, abandoned-prompt timeout, suspension, expiry-capped display, stale ACK and explicit-revoke failure tests.

After parent confirmed its combined suite was finished, executed only changed-file coverage in the isolated compose project:
- `docker compose -f compose.password-tests.yaml -p ibe160-password-tests exec -T private-api python -m pytest -q -p no:cacheprovider --tb=short tests/test_password_recovery_operator.py`: **32 passed**,42.91s.
- After final SIGINT consistency, secret-safe assertion and terminal-mode oracle adjustments: same command with `-k 'cli or redirect or change_invalidates'`: **12 passed,20 deselected**,25.44s.

No broader suite, host-helper change, production action, commit or push was performed in this correction pass. Parent owns final combined verification. Runbook records timeout/ACK/uncertain-revoke behavior. Owner contact/handoff/no-recording and actual device qualification remain **utsatt – krever eier**; story completion/release is not claimed.

### Parent final verification

After all review patches and isolated API restart: combined operator/change/access/cleanup command above **73 passed in125.52s**. Mocked Ubuntu helper suite independently **18 passed in0.082s**. Parent read implementation and tests, checked all14 findings, and git diff --check passed. Updated review diff includes corrections. No verified product finding remains; practical owner/SSH/handoff/device controls remain deferred and status remains in-review, not done. Technical task checks do not waive those mandatory controls. New fetch still shows main5cee9e03d03d2c9c165c7f8fec64aa3e146959ab; other V1 checkout remains clean.
