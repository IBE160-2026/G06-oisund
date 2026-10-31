---
title: 'PM-E1-S4 — Combined synthetic qualification'
type: feature
created: '2026-10-31'
status: in-review
route: dispatch
review_loop_iteration: 0
baseline_commit: 1c4ac7ce2621cb7ec4862231bfa10285bb31c255
context:
  - ../planning/epics.md
  - ../planning/technical-contract.md
  - ../planning/coverage.md
  - ../specs/spec-password-management/qualification.md
  - epic-PM-E1-context.md
  - operator-runbook.md
  - status.md
  - s3-evidence.md
---

<frozen-after-approval reason="Owner authorized independent synthetic qualification, explicitly deferring owner/device gates">
## Intent
Execute independent PM-E1-S4 work after S1–S3 technical verification/review. Produce reproducible combined evidence and a truthful readiness report for separate delivery, no version allocation. All S4-AC1..6 apply; mandatory personal operator/device qualification cannot be marked passed or waived.

## Boundaries & Constraints
Synthetic accounts AND synthetic generated data only. S1's inherited-reference-input deviation is documented; do not repeat anonymized-reference PDF cases, use the now-filtered browser config and synthetic backend allowlist. Never modify real accounts/data/passwords/sessions, production/server/SSH/Access settings, physical tablet, other runtime, branches/worktrees, merge/deploy/tag/release. No new feature, email/admin/registration/profile, automatic-notice integration. Parent handles reviewed commit/push/session log. Owner unavailable: practical identity/contact/code-handoff/no-recording, actual-device/keyboard/password-manager and owner acceptance are `utsatt – krever eier`. Overall S4/epic remain not complete while these mandatory gates remain.

## I/O & Edge-Case Matrix
| Scenario | Input | Outcome | Failure |
|---|---|---|---|
| Combined journey | existing synthetic accounts/data, real gateway/API/PostgreSQL | both flows,all-device logout,same data,all PM-A1..20 traced | distinguish automated pass from not-run owner gates |
| Migration/restart | preexisting synthetic records,repeated additive migration,service restart | IDs/hash/business content/ownership/retention preserved except intentional changes | capture exact before/after summaries without secrets |
| Rollback/restore | synthetic pre/post snapshots and old-compatible source | quiesce,restore/verify,revoke restored sessions/proofs before access resumes,handle restored old hashes explicitly | never claim zero-impact restore or silently restored authority |
| Operator routine | independent synthetic controlling-terminal invocation,no app login | own/teacher journeys simulated,unknown/failed handoff revoke/reissue,logs secret-free | real identity/handoff/SSH/outer Access remains owner gate |
</frozen-after-approval>

## Code Map
Inspect completed S1–S3 source/spec/evidence and runbook; do not infer completion from prior plans. Existing compose.password-tests.yaml and browser configs are synthetic direct-API harness. deploy/tablet/Dockerfile/nginx configuration, access_gate synthetic_fixture and scripts/verify-tablet-proxy.ps1 provide deployment-style ingredients. deploy/ubuntu contains production operational recipes to READ only. Reuse tested primitives, do not invoke real deployment tools against a host.

## Tasks & Acceptance
- [x] Create reproducible isolated deployment-style test recipe for real gateway + app API + PostgreSQL, with synthetic admission identity if outer gate is exercised. Use unique test project/images/volumes/loopback ports; verify availability and do not touch other containers. No bypass change to production configuration. Existing direct API tests alone are not claimed as complete gateway integration.
- [x] Execute both complete flows through this boundary with retained synthetic drafts/active and terminal days/account notices/receipts. Include operator own-account no-session issuance→app recovery→new login, A/B isolation, all-session/day authorization denial, old/new credentials, invalid proof matrix, racing submissions, unavailable/late replies and ordinary save/import/day/notices/fictional isolation regressions appropriate to current changes. Reuse existing passing evidence without redundant broad runs, but close any genuine missing independent scenario.
- [x] Rehearse additive migration/reapplication and rollback/restore in disposable DBs. Backups may contain only synthetic data and remain ignored temporary artifacts; don't commit dumps or secret material. Verify account IDs/content/ownership/deadlines and hash compatibility. Quiesce test traffic before restore; invalidate every restored app session and recovery proof before reopening. Explicitly demonstrate/report old password hashes from older snapshots and the recovery needed, not a zero-impact guarantee. Test compatible prior code without checking out/resetting shared branch (read-only archive into ignored temp is allowed).
- [x] Operator command qualification uses synthetic PTY/container only, no real SSH/handoff. Scan API/gateway/CLI/audit/DB surfaces for synthetic secret markers without emitting values or secret-bearing screenshots/traces. Show terminal display differs from stdout/stderr and recording limitations remain operational controls.
- [x] Maintain scenario evidence matrix PM-A1..20 with concrete test IDs/commands, exact source SHA/fingerprints, environment and pass/fail/not-run. Partial mixed scenarios must say which automated part passed and which owner part remains. Include build/tool versions, source-input deviation, failure corrections and remaining material limitations.
- [x] Complete operator-runbook.md and final-readiness.md with actual command syntax, identity/target/handoff routine, best-effort single operator support, self-app recovery, separate SSH/outer Access loss, migration/release/rollback checklist. These are future operational instructions, not approval to execute. No new operator appointment or service SLA.
- [ ] Record all personal/tablet/physical PC/virtual keyboard/password-manager/contact/recording/owner acceptance checks as `utsatt – krever eier`, with a concrete short checklist. Do not operate available tablet. No safety invariant may be waived; a technical failure blocks readiness and requires fix/review before claiming independent completion.
- [x] Update extension status/story evidence and coverage links only; retain V1/automatic-notices isolation. Parent final review and commits/push follow; no story/epic `done` if mandatory gates outstanding.

## Implementation Notes

## Spec Change Log

## Review Triage Log

All three context-free BMAD reviewers returned before triage. Blind floor: 92,923 bytes / 1,000 = 92.923 kB; min(floor(sqrt(92.923)+1),10)=10. Each finding is retained separately, including duplicate evidence. No product defect or new product decision was identified. Parent independently reran the prepatch recipe (project `ibe160-pm-s4-0c151dc9e20c`): all12 phases/final scans passed; this does not dismiss the verification weaknesses below.

| ID | Finding | Verdict and evidence | Route |
|---|---|---|---|
| B1 | Pre-existing gate image prevents clean reproduction | Medium: Compose references an unbuilt local tag | Patch unique pinned-source gate build |
| B2 | Restart probe can race startup | Medium: restart does not wait for health | Patch bounded health wait |
| B3 | Final-only DB scan misses state overwritten by restore | Medium: inspected runner scans after both restores | Patch intermediate DB scans after credential changes/before restores |
| B4 | Not every session token becomes a scan marker | Medium: inspected login/prior/resumed paths omit tokens | Patch centralized capture and persistence |
| B5 | Postrestore account comparison only checks inequality | Medium: a different incorrect state also passes | Patch exact post-account snapshot equality |
| B6 | Postbackup proof was already invalid | Medium: pre_code cannot demonstrate active postbackup proof revocation | Patch fresh active postbackup proof and specific rejection |
| B7 | Empty-table hashes do not prove populated preservation | Low: manifest already exposes row counts, but prose needs precision | Patch evidence wording to distinguish populated/empty tables; do not claim every data type populated |
| B8 | B has no business data/direct resource denial | Medium: current G2 checks only empty B draft listing | Patch small B-owned draft and known A-ID read/write denial |
| B9 | Same business state in pre/post snapshots; no new expiry-cleanup rehearsal | Low: S4 checks retention fields unchanged, not clock advancement; no product retention change. Adding broad retention scenarios duplicates existing regression scope and is not needed to demonstrate restored credentials | Reject test expansion; explicitly disclose identical business snapshot and no new expiry-cleanup execution, no zero-loss claim |
| B10 | Fingerprints omit executed fixture helpers/build inputs | Medium: Git base alone cannot identify uncommitted inputs | Patch complete relevant build/helper fingerprints |
| E1 | Internal HTTP transport drops timeout extensions | Medium: new Request omits extensions, losing client timeout propagation | Patch preserve extensions |
| E2 | Restart readiness race | Medium: independently confirms B2 | Patch same health wait |
| E3 | Static synthetic gate token expires after five minutes | Medium: fixture token has fixed expiry while restore can take longer | Patch signed fresh timestamps using existing synthetic key |
| E4 | Missing pre-existing gate image | Medium: independently confirms B1 | Patch same unique gate build |
| V1 | Secret scan cannot detect resumed-session leak | Medium, preverified by reading resumed/login and marker writes: freshly issued cookie is never appended | Patch B4 plus synthetic negative control using resumed token; never emit token |

Patches dispatched to the same implementation agent; parent full postpatch qualification and final disposition recorded below before commit. No story/epic completion or owner acceptance is inferred from review.

## Design Notes
This story is evidence and operational readiness, not permission to release. A production-like local container build is not a production deployment. Prefer bounded test scripts over manual steps that cannot be reproduced, and never run global prune/reset or reuse real backup/volumes. If test tooling needs an owner login/approval/MFA, defer that portion and continue the independent recipe.

## Verification
Select only isolated project names/loopback endpoints and generated synthetic fixtures. Use observed DB waiters for concurrency; never claim scheduler-only races. Backend existing synthetic guard marker must remain. No concurrent suites sharing cleanup fixtures. Preserve clean-up ownership for created containers/networks; stop only newly created qualification runtimes after evidence, retain needed synthetic volumes unless explicit scoped cleanup is safe. Full owner acceptance and practical identity/handoff remain release blockers regardless of automation. Parent runs BMAD three-layer review on this story's final diff.

## Integration preparation notes

The synthetic admission factory is a function in deploy/tablet/access_gate/test_gate.py, imported by scripts/tablet-proxy-probe.py; there is no synthetic_fixture.py. Existing isolated gateway probe uses real gate handler plus synthetic signed credentials, but its upstream is a stub: do not present it as real API/DB qualification. S4 must attach real private-api and its own synthetic PostgreSQL. Gateway strips forwarded IP/outer JWT before API and requires Host bus.owner-domain.no; canonical PRIVATE_ORIGIN for deployment mode is https://bus.owner-domain.no, with Secure cookies. If the synthetic transport reaches internal HTTP upstream, explicitly handle test cookie transport and label which TLS/outer-provider parts are simulated; never weaken product cookie/Origin policy to make a test pass. Use only local/internal endpoints and generated identities, no real DNS/SSH/IdP requests.

The previous helper tests run in Linux with mocked host roots/subprocess, no production socket; runpy plus unittest.mock.patch('os.chown') preserves non-root test behavior. Final S2 source includes bounded dialogue/signal cleanup and exact-candidate ACK; do not run unqualified real issuance. Its parent regression73 and helper18 passed after review. Actual app recovery comes from S3, inspect final handoff before combined tests.

Synthetic regression selection warning: do not run backend test_private_drafts.py or test_private_workdays.py wholesale. Reference-PDF cases are test_transient_import_save_reopen_replay_and_access, test_additional_import_save_reopen_replay and test_imported_source_corrections_duty_car_and_overnight_survive_confirmation. Select explicit generated/synthetic cases instead. Importing synthetic_text_pdf helper is acceptable; running reference cases in its containing module is not. test_retained_data.py and test_account_notices.py contain synthetic business fixtures; inspect actual selected test inputs before execution. Browser private-retention includes generated synthetic_text_pdf, which is acceptable.

Use updated origin/main5cee9e03d03d2c9c165c7f8fec64aa3e146959ab as read-only prior-code compatibility reference unless final S3/main inspection changes it. Do not checkout/reset this worktree or change another branch to run compatibility tests. Any archived prior source is ignored temporary data, used only against dedicated synthetic DBs. Compatibility testing is not selecting an actual rollback release or authorizing rollback. Explicitly distinguish a pre-change backup (older hash restored) from rolling code back while keeping current DB (current hash retained); invalidate restored session/proof authority before reopening either path as required.

S3 verification history includes generated synthetic-password values in failing test diagnostics (pytest fixture repr and a legacy browser assertion). No real account/credential/code was involved; values must not be repeated. Shared redacted fixture repr and equivalent boolean/static assertions were added. Read final S3 evidence for exact correction/results. PM-A16 must distinguish corrected final runtime/test checks from these historical incidents; do not claim zero secret-like test output over the entire session. The earlier S1 mixed reference-input deviation also remains documented and excluded, not erased by later clean runs.

During combined invalid-input checks, inspect escaped lone-surrogate JSON on both password routes. S3 now has explicit sanitized encoding handling; verify actual S1 boundary too rather than assuming Pydantic rejects it. This is a test question, not a confirmed defect: if an unhandled failure is demonstrated in a password flow, correct and review the bounded validation issue under the epic before claiming PM-A2/16 qualification. Never print submitted values while probing; only synthetic inputs and status/boolean outcomes.

Final documentation navigation: update extension README and implementation status to link final-readiness/scenario evidence. Keep planning-only history labelled historical and retain source-baseline findings; do not claim the planning kernel itself was a release approval. Existing README implementation-authorization section explicitly supersedes older planning-only prose. Epic/story overall status must stay in-review/owner pending while mandatory owner controls remain. No V1 sprint/epic state changes.

## Implementation and verification evidence

Implemented `scripts/verify-password-s4.mjs`, `password-s4-gate.py`, and `password-s4-probe.py`; reproducible unique-project build, real gateway/API/PostgreSQL, synthetic signing identity, populated pre015 reconstruction/migration, repeated migration/restart, pre/post pg_dump/restore, exact prior-code archive compatibility, quiesced authority invalidation and old-hash settlement before reopening. No product source/configuration changes were required; both actual password routes reject escaped lone-surrogate fields with sanitized422.

Historical agent pre-review run `node scripts/verify-password-s4.mjs`: all12 named phase checks plus four service-log/DB marker scans passed on projectibe160-pm-s4-1fd58ad0fbba, loopback61502, source base1c4ac7ce2621cb7ec4862231bfa10285bb31c255. This is superseded by parent postpatch verification below. Exact fingerprints/images/table summaries are in [runtime evidence](evidence/s4/runtime.json); [scenario evidence](s4-evidence.md) records reused reviewed races/browser/regression evidence, harness corrections, historical input/output deviations and limitations. Runtime stopped; unique synthetic volumes/ignored dumps retained. Parent final review and postpatch verification are recorded below.

[Operator runbook](operator-runbook.md) and [final readiness](final-readiness.md) now distinguish compatible prior-code testing from the host migration-equality rollback guard and unsupported existing-deployment restore. Every mandatory practical owner/device check remains **utsatt – krever eier**. S4 and epic overall stay in review/not complete; no release/version/merge/deploy or V1 status change.

## Parent final postpatch verification

Parent inspected all patches and independently ran `node scripts/verify-password-s4.mjs` against fresh project `ibe160-pm-s4-e57c2ff0d437`, loopback56762: exit0,12 phases,20 database/log scans and three resumed-token negative controls passed. 133 source fingerprints match executed sources;78 relative documentation links and diff check passed. All accepted review findings are resolved; B9 scope expansion is rejected with explicit limitations. No product source changed in S4, so reviewed S1–S3 tests remain applicable. Earlier prepatch run and agent run are historical, superseded by evidence/s4/runtime.json.

All independent work is complete; mandatory owner/physical/SSH/handoff checks and qualified production restore path remain **utsatt – krever eier**. Overall status remains in-review, not done. No release/production operation is authorized by these results.
