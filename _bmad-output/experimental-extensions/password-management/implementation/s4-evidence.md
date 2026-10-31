# PM-E1-S4 combined scenario evidence

Source base: `1c4ac7ce2621cb7ec4862231bfa10285bb31c255`; prior-code reference: `5cee9e03d03d2c9c165c7f8fec64aa3e146959ab`. Exact source-input fingerprints and observed image IDs are in [evidence/s4/runtime.json](evidence/s4/runtime.json). This is independent synthetic qualification, not completed owner acceptance or a release approval.

## Reproduction and boundary

From the repository root, with Node 24, Git, tar and Docker Desktop available:

```sh
node scripts/verify-password-s4.mjs
```

The runner generates a unique `ibe160-pm-s4-<random>` Compose project, unique built API/gateway images, internal network and private PostgreSQL volume. It checks a random loopback port is available before binding; a subsequent collision fails startup. No existing runtime is reused. PostgreSQL uses the pinned17 image. The gateway is built from the actual tablet Dockerfile/frontend and unchanged Nginx configuration; API is built from the actual backend. Gate admission uses the real handler with in-memory synthetic RSA identity and keys, no DNS/IdP/SSH call. The gate image is uniquely tagged and built by composing the existing pinned runtime Dockerfile with the existing pinned test-dependency recipe; no pre-existing local gate image is required.

The probe's `InternalTransport` retains canonical HTTPS request URLs for the HTTPX cookie jar, then forwards over the isolated internal HTTP hop to Nginx with the canonical Host. Actual API Secure/HttpOnly/SameSite cookies, canonical Origin/CSRF and gateway admission remain enforced. This simulates TLS termination; it does not qualify external TLS, Cloudflare or actual browser transport. S1/S3 browser evidence remains the source for UI lifecycle behavior. Direct API tests alone are not called gateway integration.

Only generated synthetic users, manual business fixtures and `synthetic_text_pdf()` are used. The synthetic DB guard and project marker run before each probe phase. No reference PDFs are mounted or executed. Restore dumps, generated credentials, captured synthetic PTY bytes and state stay in ignored `tmp/<project>`; PTY bytes stay in memory. Only sanitized table counts/content hashes, booleans, image/tool metadata and source fingerprints are retained as evidence. Do not publish scratch files or dumps.

Runner stops only its own Compose services in `finally`, including on failure. Its stopped containers/network, unique images and synthetic volumes remain for audit; it does not globally prune or remove volumes. Recorded exploratory projects are `ibe160-pm-s4-635cbcb4caa9`, `ibe160-pm-s4-26645a097afd`, and `ibe160-pm-s4-19f5ac3ff159`, and `ibe160-pm-s4-7279eb45b0b8`; final run is identified in runtime.json. All are task-owned, stopped after their runs.

## Concrete independent phases

- G1: gateway login A/A2/B; save draft, confirm/start active and terminal days, account notice/receipt, generated PDF import. Capture every business table's ordered JSON SHA-256 and count, plus account UUID/hash state privately.
- M1/M2: while API/gateway stopped, reconstruct the populated pre015 schema by removing only015 metadata tables/ledger entry. Normal API startup applies015; repeated normal migration preserves accounts/hashes and every business table. This is explicitly reconstructed legacy state, not a claim initial clean startup migrated populated users.
- G2: both new POST routes reject missing/invalid outer identity and admitted missing/foreign Origin/bad CSRF; successful flows retain no-store and Secure/HttpOnly/SameSite cookie deletion. Change through gateway; old credentials fail/new work; stale A sessions/read/write denied; B unaffected; retained rows equal. Independent controlling-terminal issuance with no app session/password, app API redemption, one-use rejection and separate login. Wrong account/unknown/malformed proof rejects. All seven escaped lone-surrogate fields across both routes return sanitized422; no S1 defect reproduced.
- R1: pg_dump pre/post snapshots; stop API/gateway before pg_restore. Verify business hashes, remove all restored sessions and revoke all active proofs before access resumes. Pre snapshot restores the exact original account hashes; post snapshot retains changed hashes.
- R2: exact prior source archived with `git archive` into ignored scratch, mounted read-only in a separate one-shot process. Prior `migrate`/`authenticate` reads the additive DB and verifies old/current hashes and account owner; removes its test session. No checkout/reset/branch change. This is source/schema/hash compatibility, not a complete older-release UI test or authorization to bypass the host rollback guard.
- R4: with traffic still stopped, synthetic PTY issuance plus current recovery service settles the restored older A hash. Verify no sessions or active proofs before reopening. This trusted disposable maintenance process is **not** an installed production maintenance command.
- R3: repeat migration after API restart/restore; gateway login and retained reads pass. Restored stale session/proof rejected after reopening; old A password rejected after guarded settlement. B's deliberately unchanged password remains unchanged.
- Secret scan: runner captures API/gateway/gate/PostgreSQL logs into memory and passes them on stdin to a guarded in-container scan, adding account/session/proof/audit rows. Every successful login token is registered centrally, including prior-code and resumed logins; a resumed-token negative control must make the scanner reject without emitting its value. DB surfaces are scanned after issuance/password mutation and before each restore, as well as in the final service scans. Generated password/code/session markers must be absent; values/raw logs never printed. CLI display intentionally contains the synthetic code on the controlling terminal; S2's redirect/TTY tests distinguish this from stdout/stderr, not a claim that a PTY cannot be recorded.

## PM-A1–20 matrix

`S1`, `S2`, `S3` references below denote the already reviewed evidence linked at the end, reused without redundant broad suites. Their exact commands/results are retained there. `G/M/R` refer to the independent script phases above. Partial cases explicitly retain their unrun owner component.

| Scenario | Concrete automated evidence | Result / remaining qualification |
|---|---|---|
| A1 | G2; S1 `test_change_revokes_all_sessions_keeps_identity_and_data` | Automated pass |
| A2 | G2 seven escaped-surrogate fields; S1 `test_validation_boundaries_do_not_mutate`; S3 boundary tests | Automated pass; physical paste/password manager owner pending |
| A3 | G2 stale A mutation/B retained; S1 validation and ownership tests | Automated pass |
| A4 | G2 both actual POSTs missing/invalid admission, Origin/CSRF/no-store/cookie deletion; S1 validation/S3 `test_boundaries_and_live_other_session`; S1 proxy admission suite | Automated pass; external transport owner pending |
| A5 | G2 PTY→gateway recovery→separate login/reuse rejection | Automated pass; real identity/handoff owner pending |
| A6 | S3 `test_generic_invalid_states_no_mutation`, `test_expiry_while_hashing`; G2 malformed/reuse, R3 restored proof | Automated pass |
| A7 | G2 wrong-account/unknown/B isolation; S3 boundaries/live409/browser dirty logout | Automated pass |
| A8 | S3 `test_true_database_contention`, `test_obsolete_code_waits_for_preceding_mutation`; S2 real gate contention | Automated pass; actual PostgreSQL waiters, not scheduler-only races |
| A9 | S1 persistent parallel change budget; S3 persistent parallel/global/proxy budgets and real429 browser | Automated pass |
| A10 | G1/G2 all business hashes incl active/terminal lifecycle and receipts; S3 full recovery test | Automated pass |
| A11 | S1 login-verification gate/opposite-order tests; S3 committed-before-recovery and opposite-order services | Automated pass with observed PostgreSQL blockers |
| A12 | S1 actual draft-save/change and read/import/logout/cleanup races; G1 generated import/save/day/notices | Automated pass |
| A13 | S1/S3 browser late reply, BFCache, visibility, sibling invalidation;82 selected legacy regressions | Automated pass; actual remote/offline device owner pending |
| A14 | S3 rollback-after-partial-replacement and browser lost/HTML/timeout/unrelated400; R3 real API restart | Automated pass; no immediate-offline-erasure guarantee |
| A15 | S1/S3 offline/dirty/pending browser cases; legacy identity/import/recovery suites | Automated pass; physical network/device walkthrough owner pending |
| A16 | S4 in-memory gateway/API/gate/DB scan, sanitized422 and PTY; S2 redirect/recording safeguards | Corrected automated checks pass; historical synthetic diagnostic incidents below; real no-recording control owner pending |
| A17 | M1/M2, R1/R2/R3/R4; S2 provision/migration tests | Automated pass; live restore tooling/rollback procedure owner gate |
| A18 | S1/S3 blank Day/Night tablet/PC200% renders, contrast/focus browser tests | Automated/emulated pass only; actual tablet/PC/keyboard/password manager/acceptance **utsatt – krever eier** |
| A19 | G2 synthetic outer-admission denial; S1 fail-closed gate suite; runbook separation | Synthetic pass; actual SSH/MFA/outer Access/loss walkthrough **utsatt – krever eier** |
| A20 | G2 independent synthetic PTY; S2 wrong/unknown/cancel/failed handoff/revoke/reissue/timeout tests | Synthetic pass; identity/contact/operator absence practical qualification **utsatt – krever eier** |

## Corrections and limitations

Two initial harness runs failed because the generated PDF probe used multipart instead of the established raw application/pdf contract. Corrected the probe, no product change. An exploratory restore run first demonstrated old-hash acceptance after reopening, then recovered it; parent review required settlement before reopening. The final recipe performs that settlement while traffic remains stopped. Exploratory outcomes are not promoted to safe operational readiness.

S1 historically executed some anonymized reference inputs; those results are excluded from synthetic qualification and were not repeated. S3 historically echoed generated synthetic passwords in failed pytest/Playwright diagnostics. Redacted fixture representations and boolean/static assertions corrected that; values are not repeated. Do not claim the entire historical session was secret-free. No real account/credential was used.

Existing host helper rejects rollback when migration files differ; V1 lacks015. Thus tested old-code compatibility does not enable ordinary host rollback to V1. `verify-restore` validates a disposable copy only; `restore-initial` refuses an already deployed database. A reviewed production recovery procedure, authority invalidation and old-hash settlement path must be prepared before release; no new host privilege/command or production bypass was introduced.

Sources: [S1](spec-pm-e1-s1.md), [S2](spec-pm-e1-s2.md), [S3](s3-evidence.md), [final readiness](final-readiness.md), [operator routine](operator-runbook.md). S3 parent final103 backend/35 focused browser and82 prior selected synthetic legacy regressions remain the reviewed regression baseline. S4 does not rerun reference cases or unrelated broad suites.

Final environment: Windows host, Docker Desktop Linux engine29.7.2, Compose5.5.1, Node24.19.0; API Python3.13.16/FastAPI0.149.0/Pydantic2.14.1/Psycopg3.3.6/HTTPX0.28.1/pytest9.0.3. See [package versions](evidence/s4/tool-versions.json), pinned Dockerfiles/lockfile fingerprints and runtime image IDs. Final parent post-review frozen-script run: project `ibe160-pm-s4-e57c2ff0d437`, loopback56762;12 phases,20 database/log scans and three resumed-token negative controls passed (exit0). All 133 source fingerprints match;78 relative documentation links and git diff --check passed.

## Preservation coverage boundaries

Populated S4 business tables: account_notice_operations, draft_operations, drafts (including a B-owned draft), workday_close_operations, workday_lifecycles, workday_notices, workday_operations, workday_start_operations and workdays. B can still read its own draft and is denied both reading and mutating A's known draft ID. Exact nonzero counts belong to the final runtime manifest.

Empty-table equality only: draft_deletions, notice_creation_admissions, workday_bus_operations, workday_buses, workday_deletions, workday_notice_operations, workday_outcome_operations, workday_outcome_revisions, workday_outcomes, workday_selection_operations and workday_selections. Their zero-row hashes prove only absence of unexpected rows; populated behavior for other business types is reused from the reviewed S1–S3 regression evidence, not newly rehearsed by S4.

Pre/post backup business state is deliberately identical; only credential/session/proof authority changes. The post snapshot now includes a specifically captured active proof, which must be revoked and rejected after restore; all account rows must equal the exact privately captured post-account snapshot. S4 does not newly rehearse expiry cleanup across a restore or loss of later business writes; expiry/cleanup evidence comes from existing reviewed regressions. This is no zero-loss or general arbitrary-database restore guarantee.

Three-layer parent review completed:15 individually triaged findings, bounded harness/documentation patches verified, one low-value test expansion rejected with explicit coverage limits. Parent independently ran both prepatch and final postpatch recipes successfully. Final runtime manifest identifies the postpatch sources; all its containers are stopped. Earlier reviewed-source run1fd58ad0fbba and parent prepatch run0c151dc9e20c are historical evidence, not the final build.
