# Restore qualification — 2026-11-04

Status: independent implementation, isolated verification and three-layer BMAD review completed. This document is not owner acceptance or release approval.

## Authority and baseline

Owner approved the [mandatory fresh-code policy](restore-policy.md), then explicitly requested implementation, isolated tests and push to the password branch. Baseline e3874cce4894ecc0d092d2cbc010c2b733da71aa; fresh origin/main15011042b1fe093becbe68177e6396e456b1f35f is already integrated. No production operation, main merge, tag or release is authorized. Existing unrelated local V1 services remain untouched.

## Verification boundaries

The new mechanism must be verified with synthetic accounts and business data. Host helper command-order/failure tests mock systemd; actual database restoration, migration, credential quarantine and independent fresh-code redemption must execute against disposable PostgreSQL. Evidence for these layers is recorded separately. A mocked host does not prove actual installed SSH/systemd/Compose-PTY delivery.

Existing UI, rate limits, proof expiry/single-use and offline handling are reused. Any reused earlier evidence retains its original source and scope; new tests must establish the restore policy itself. Previous S4 synthetic old-hash settlement did not implement this policy and cannot substitute for these tests.

## Required matrix

| Case | Required observation | Evidence |
|---|---|---|
| Pre015 and current archives | migration succeeds; account IDs/business fingerprints retained | Passed; see final results below |
| All restored authority | old passwords, sessions and active codes rejected before reopening | Passed; see final results below |
| Independent users | fresh A code works while B waits; later B code works | Passed; see final results below |
| Ordinary restart | does not quarantine passwords | Passed; see final results below |
| Failure and retry | persistent closed state; no blind repeated replacement after completion | Passed; see final results below |
| Invalid source/release/schema | no destructive replacement | Passed; see final results below |
| Diagnostics | no plaintext passwords/codes/session tokens in DB/logs | Passed; see final results below |
| Runtime barriers | existing nonroot/read-only/cap/network boundaries retained | Passed; see final results below |

## Remaining owner qualification

Actual independent SSH → installed helper → Compose controlling terminal → code display, practical identity/contact/no-recording/handoff, physical device/password manager/offline/unsaved-work checks and explicit password acceptance remain open. No owner test can replace a missing technical safety check. Production deployment and any real restore require a separate explicit instruction.

## Executed initial checks (before three-layer review)

- Parent synthetic project ibe160-password-restore-parent-20261104:103 existing backend credential/access/cleanup tests passed155.80s;3 new restore tests passed7.62s. Later transaction-timeout hardening is covered by implementer's final3 tests8.02s. Existing app/auth/frontend sources remain unchanged.
- Initial helper suites41 passed0.156s; implementation completed44 cases after timeout/retention/real file-descriptor regression additions. Final parent post-review rerun remains pending.
- [Initial complete runtime manifest](evidence/restore/initial-runtime.json): project ibe160-pm-restore-e4773c16e701; actual PostgreSQL pre015/current archives, atomic failed replacement rollback, no leftover newer table, migration/business equivalence, all-account old authority rejection, A/B independent fresh-code recovery, nonroot guard shell checks and unsupported-schema probes.
- Parent executed the actual preflight_restore function against both synthetic archives from project86ce051f2953 using Python3.12.10 on Windows and Docker Desktop. Adapter only supplies an unused fcntl import stub, restores host PATH after module import, redirects compose to the unique synthetic project and CONFIG to its synthetic secret, and rejects non-Docker run calls. Actual disposable DB creation, SQL generation/import, source/migrated/schema comparison, quarantine and teardown execute. Both pre015/schema14 and current/schema15 passed. No systemd/root entrypoint or installed SSH chain was exercised.

Failures found and fixed before review: JSON-expression cast precedence caused2 new backend failures (1 passed); corrected and all3 passed. Parent actual preflight uncovered buffered SQL prefix written after child stdout, making the generated script drop restored tables at its end. Added flush before child descriptor handoff and a real subprocess-write regression; both full preflight archives then passed. A Python launcher/cache lookup failed locally; explicit installed Python3.12.10 was used. Sandbox per-call temporary directories disappear between tools, so the review diff is retained in ignored workspace tmp rather than an ephemeral system-temp path. No secret values were printed.

## Final post-review verification

- **103 existing backend tests passed155.80s**, unique project ibe160-password-restore-parent-20261104. Existing auth/recovery/session/browser/gate source remains unchanged; prior35 focused browser,82 selected synthetic legacy browser and33 gate evidence is reused within that unchanged scope.
- **3 restore backend tests passed6.92s** in the final runner. One harmless pytest cache warning reflects read-only application storage; no test skipped or failed.
- **54 host/maintenance tests passed0.184s**, parent independent network-none/read-only/cap-drop/no-new-privileges container, source bind read-only, no Docker socket. Includes27 new restore tests, initial import/quarantine/receipt success and failure, startup/crash/late tunnel failure, retry/retention, FIFO/source guards, timeout cleanup and real descriptor regression. Systemd/process-lifecycle outcomes are mocked, not an installed-host claim.
- **Final combined runner passed:** project ibe160-pm-restore-697a4cd98626. [Final runtime manifest](evidence/restore/final-runtime.json) records image identities, archive fingerprints and exact source hashes. Both populated pre015/current archives prove account/business preservation, atomic failed replacement rollback, no leftover newer tables, all old authority denied, independent A/B recovery, ordinary actual API restart and credential preservation. Three actual guard snippets execute as nonroot for missing/unreadable/pending/normal/local-start conditions and repeated invocation. Generated SQL retains a real five-second lock timeout. Newly generated codes/tokens join the scan markers; scans cover database rows plus captured diagnostics/service logs.
- **Actual preflight passed all3 cases:** valid14/15 migration archives accepted; supported-version archive missing a constraint and index rejected by schema comparison. Source database fingerprint and absence of pending state checked after each. Reproduce with the committed scripts/verify-password-restore-preflight.py and the final runner project id. [Preflight results](evidence/restore/preflight.json). No mocked preflight internals; only synthetic project/config transport and unused Windows fcntl import adaptation.
- **Actual replacement-client transport passed:** named one-off private-db client executes BEGIN/SELECT/ROLLBACK through production command shape and secret filename, with a synthetic Compose secret alias. No application data mutation; scoped client and DB stopped afterward. The full host state machine remains tested with mocks; its generated SQL and DB/preflight operations execute independently for real.
- Parent inspected actual Docker metadata: API UID10001:10001 and PostgreSQL userpostgres, both read-only roots, ALL capability drop, no-new-privileges and PID128. Production runtime barriers remain; no broad privilege/host mount or O6 risk acceptance change. Local readiness permit is a root-owned marker, not a new public endpoint.

All14 review findings have individual verdicts in [the spec](spec-pm-e1-restore.md).13 real findings corrected; B7's no-actual-preflight claim disproved by parent execution (which found the earlier buffering bug). Shared-root findings retain separate rows. Parent additionally closed the initial-restore authority bypass. No independent implementation defect remains identified. The initial manifest is historical pre-review evidence; final source fingerprints supersede it.

## Reproduction

Run from the repository root, using only synthetic data:

~~~text
node scripts/verify-password-restore.mjs
python scripts/verify-password-restore-preflight.py <printed ibe160-pm-restore-... id>
~~~

Qualified host: Windows Docker Desktop with Node24 and Python3.12.10 for the host adapter; Linux application/tests use Python3.13. Native-Linux host bind ownership for UID10001 scratch needs separate qualification; do not make credential-bearing scratch world-writable. Test resources have unique projects and finally-stop cleanup. Ignored synthetic scratch/volumes remain; no real secrets, raw dumps or code values are committed.

Production helper installation, actual systemd/reboot and SSH/terminal/handoff behavior remain owner/deployment qualification. Source-level guards and isolated shell/process tests do not claim those events happened on the server. PM-E1/S1–S4 stay in review. No production operation or merge/release performed.

Final artifact checks:103 relative documentation links validated; Python/Node syntax and diff checks passed. Generated synthetic passwords/codes/tokens were scanned against all28 proposed changed artifacts with no matches. All task-owned temporary services are stopped; only the pre-existing ibe160-v1-final-20261031 services remain running, unchanged.
