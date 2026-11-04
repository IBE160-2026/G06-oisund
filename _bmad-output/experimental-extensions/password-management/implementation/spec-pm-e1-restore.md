---
title: 'PM-E1 — safe database restore with mandatory fresh recovery'
type: feature
created: '2026-11-04'
status: in-review
route: dispatch
review_loop_iteration: 0
baseline_commit: e3874cce4894ecc0d092d2cbc010c2b733da71aa
context:
  - '{project-root}/AGENTS.md'
  - '{project-root}/_bmad-output/experimental-extensions/password-management/implementation/restore-policy.md'
  - '{project-root}/_bmad-output/experimental-extensions/password-management/implementation/operator-runbook.md'
---

<frozen-after-approval reason="Owner approved restore policy and explicitly authorized implementation/testing/push; production execution excluded">
## Intent
Implement the approved all-account fresh-code policy after actual database restoration, closing the existing-deployment restore gap. Existing accounts/data survive; Jonas and teacher recover independently through existing operator code issuance and app redemption. Ordinary updates/restarts do not reset passwords.

## Boundaries & Constraints
Always keep ingress/writes closed until restored data and invalidation are verified. Destroy every restored password's authority, invalidate all restored sessions/proofs, preserve IDs/business data/retention. No saved current-hash fallback. No temporary passwords, email, dashboard, account recreation or new general-purpose admin shell. Independent SSH remains operator authority. Only unique isolated synthetic test resources; never production, real accounts/data/devices/SSH, main merge, deploy/tag/release. Preserve unrelated environments. Parent handles session log, commits/push and three-layer review. Practical identity/handoff/device/installed SSH chain remain owner gates, not simulated acceptance.

## I/O & Edge-Case Matrix
| Scenario | Input/state | Expected behavior | Failure handling |
|---|---|---|---|
| Restore | supported trusted archive, expected release/digest | preserve business rows/IDs; all old passwords/sessions/codes fail before reopening | closed persistent maintenance state |
| Independent recovery | A/B restored, fresh A code | A chooses password/logs in; B remains blocked until own fresh code | existing generic errors, expiry/single-use/rate limits |
| Interrupted operation | any restore/check/start failure or process restart | no ingress or normal startup; bounded retry/verification possible | never silently repeat completed replacement or resurrect credentials |
| Invalid source | traversal/symlink/tamper/wrong release/unsupported schema | reject before destructive mutation | static secret-free diagnostics |
| Ordinary operation | restart/migration/update without restore | current passwords/rows unchanged | existing behavior retained |
</frozen-after-approval>

## Code Map
- backend/app/auth.py: valid hash is 16-byte salt:64-byte digest; account_lock first; replace_password already revokes proofs/sessions. Destroy authority using independently random valid-format salt/digest per account (no generated plaintext, no new account flag). Avoid schema migration and old-code flag bypass.
- backend/app/private_storage.py: migrate/cleanup; strict private_work connection boundary must remain. backend/app/manage.py: fixed actions; add bounded offline quarantine/verification operation. password_recovery.py and recovery_terminal.py retain identity, issuance, one-use redemption and no-secret logging.
- deploy/ubuntu/bussassistentctl.py: fixed release/Compose/project/database, root operation lock, backup and verification. Current restore-initial refuses established deployments; clean-only restore can leave newer tables. Current rollback migration equality must remain.
- deploy/ubuntu/{bussassistent,cloudflared}.service, compose.yaml: persistent fail-closed restart guard must cover systemd and Docker restart paths, not only current process. Do not weaken nonroot/read-only/cap/PID/network restrictions.
- deploy/ubuntu/test_operations.py and test_gateway_maintenance.py: mocked host lifecycle tests; backend/tests/test_password_recovery.py: real synthetic PostgreSQL account tests.
- scripts/verify-password-s4.mjs and password-s4-probe.py: reusable synthetic production-image/data journey patterns; historical evidence must not be overwritten. Add dedicated restore qualification with no production mounts/socket supplied to tested helper.

## Tasks & Acceptance
- [x] backend/app/auth.py or focused restore module, app/manage.py: one transaction with deterministic account-lock order replaces all restored hashes with independent random valid-format values, removes sessions, revokes all active proofs, verifies results. No plaintext or emitted hash; retry cannot affect accounts after completed reopening. Existing recovery stays unchanged. Keep rate/audit history and document bounded waits.
- [x] deploy/ubuntu/bussassistentctl.py and required unit/Compose guards: fixed narrow restore command selecting trusted backup basename, digest and expected release; securely snapshot source before downtime; preflight images/archive/schema; preserve pre-replacement backup without pruning source. Durable root-owned operation state binds release/archive/stage and survives crash/reboot; inhibit every reopening path while pending. Stop/verify writers without nested helper-lock deadlock. Use transactional replacement or staged verified replacement; never leave leftover tables from older snapshots. Support documented v1.0.1 pre015 and current schema, reject unknown/newer schemas. Migrate offline, quarantine, verify business equivalence before retention cleanup, then explicit separately checked reopening. Retain source/prior backup on failure; bounded resume cannot blindly redo completed restore. No broad paths/SQL/command flags or automatic fallback to old passwords.
- [x] backend/tests and deploy/ubuntu tests plus scripts/verify-password-restore.mjs (or equivalent): actual isolated PostgreSQL dump/restore/migration/quarantine/recovery journey, both users, failed replacement/transaction, wrong-source/retry/state guards, source/backup retention and no-secret scans. Host systemd calls mocked; clearly separate those from executed database/container behavior. No real systemd/SSH or production helper execution.
- [x] implementation/restore-evidence.md, restore-policy.md, operator-runbook.md, deferred-work.md, status.md, final-readiness.md, v110-candidate.md and docs/ubuntu-server.md: exact commands, safe interrupted-state recovery, supported archives, evidence/limits and updated remaining owner gates. Do not mark PM-E1 or owner-dependent stories complete.

Acceptance: Given a restored two-user snapshot, when quarantine completes and app reopens, then all old credentials fail and fresh A recovery preserves A's workspace while B waits safely. Given any incomplete operation, when start/deploy/rollback/tunnel/restart is attempted, then ingress stays closed. Given an invalid archive/release, when restore is attempted, then preserved data is not replaced. Given normal restart/update, credentials remain valid. Given pre015/current archives, upgrade and business fingerprints are verified before opening.

## Design Notes
No intent gaps: approved policy fixes visible behavior. Irreversible mutation occurs only in disposable tests now; future production command requires separate authorization. This is one cohesive recovery goal across application and operations. Implementation may refine internal state/storage within these constraints, never broaden public scope. Source backups are sensitive/trusted operator artifacts, not arbitrary user uploads. Snapshot acquisition must reject symlinks/nonregular files and writable ownership surprises. Failures report static stage labels, not SQL/archive/raw subprocess output.

## Implementation Notes
BMAD investigation performed read-only; clean branch e3874cc; fresh origin/main15011042b1fe093becbe68177e6396e456b1f35f already ancestor. Prior approval checkpoint is satisfied by explicit policy acceptance and this implementation request; no new product decision or claimed extra approval. Parent uses required session-log skill at completion. Keep temporary test services scoped and stop them in finally.

## Spec Change Log

## Review Triage Log

All three layers returned before triage; blind floor min(floor(sqrt(91.592)+1),10)=10. Findings are recorded separately even when sharing a correction.

| ID | Verdict | Evidence and disposition |
|---|---|---|
| B1 | high | Actual pg_restore script resets timeout settings to0, overriding prefix. Patch generated settings so the demonstrated replacement transaction retains bounded lock/statement/transaction lifetime; execute real SQL test. |
| B2 | medium | Compose client timeout does not itself stop exec psql. B1 server transaction bound plus existing zero-client quiescence check must be verified before any continuation; patch cancellation/confirmed completion where needed. |
| B3 | medium | completed.json journals authorization, so interval is not wholly unjournaled, but pending removal precedes readiness and process death can leave incomplete opening uninhibited. Patch durable opening/retry within existing helper lifecycle; no new user choice. |
| B4 | high | Tunnel can accept traffic before wait_tunnel fails; reinstating verified can lock out reopening after legitimate sessions/writes. Patch final ingress commit boundary so postcommit connectivity failure never resets quarantine expectations; test late accepted traffic. |
| B5 | medium | Failed/preflight and completed operations leave copied dump/SQL indefinitely outside48h backup policy. Patch cleanup of nonpending sensitive copies with bounded retention; preserve pending recovery material and original backups. |
| B6 | medium | Actual preflight one-off API containers are unnamed; client timeout can orphan them. Patch unique scoped cleanup as offline already uses. |
| B7 | false | Parent independently executed actual preflight_restore for both valid archives; it found/fixed real SQL buffering defect and now passes. Evidence adapter only changes transport/project/config, no preflight logic. Commit reproducible safe harness/evidence; structural rejection coverage separately V2. |
| B8 | medium | Guard probe selects first command only; gateway/access-gate actual guard behavior is not executed. Patch all3 and ordinary/restart scenarios, keeping existing barriers. |
| B9 | medium | Probe scans logs only and omits newly issued recovery codes/tokens. Patch marker collection and DB plus diagnostic scans with static failure messages. |
| B10 | medium | Generic restore failure instructs inspecting stage but status does not expose it. Extend existing read-only status action with safe operation/stage/attempt/next-action metadata; no new public command required. |
| E1 | medium | Stopped DB after reboot/stop prevents close_restore query while normal start is inhibited. Patch bounded start of only fixed private-db before resume checks; test. |
| E2 | low | O_RDONLY FIFO open blocks before fstat. Trusted root source still permits accidental wrong file type; direct O_NONBLOCK addition makes rejection bounded, no interface expansion. |
| V1 | medium | Preverified mutation demonstration confirms first-guard-only gap; same patch as B8, independently retained. |
| V2 | medium | Preverified missing schema-shape negative test: valid preflight and unknown table/migration tests do not exercise equality rejection for missing index/constraint. Add real altered-schema archive preflight rejection. |

Accepted corrections remain within existing fixed restore/status interfaces and demonstrated states. Parent must rerun affected checks; no owner acceptance is inferred.

## Verification
Run focused backend credential/recovery tests in unique synthetic Compose project, isolated Linux mocked helper/maintenance suite, and new real restore qualification (pre015/current, repeat/failure/independent recovery). Reuse unchanged browser/gate evidence explicitly; rerun where changed surfaces require it. Capture sanitized counts, source fingerprints and exact image identities in restore-evidence.md. Parent independently reads full diff, audits matrix coverage and runs three BMAD review layers before final checks/push. Never claim actual owner/production execution.

## Parent final verification

All independent tasks and matrix rows are complete; actual owner/installed-host gates are explicitly outside this completed isolated scope. Parent inspected full baseline diff and post-review patches. Final106 backend tests (103 reused unchanged credential/access paths plus3 new),54 helper tests, both complete restore journeys, actual3-case preflight, runtime metadata and named-client transaction passed. See restore-evidence.md for commands, failures/fixes and exact limits.14 review rows retained; bounded corrections re-engaged the same implementation agent. P1 parent follow-up: initial restore could resurrect credentials through confirm-data; now quarantine receipt gates confirmation and initial deployment, with positive/failure tests.

New internal opening/ingress-committed stages preserve the frozen fail-closed intent before explicit external opening; postcommit connectivity retries never repeat restore/quarantine. No product decision was added. Review diff used ignored workspace tmp because tool-owned system-temp directories are destroyed between calls. No production action, owner acceptance, main merge or release occurred.
