# Readable recovery code qualification — 2026-11-05

This bounded correction follows the failed manual handoff recorded in [the owner journal](owner-tests-20261104.md). It changes generation/representation and user guidance, not credential policy or recovery authority. The [specification and review triage](spec-readable-recovery-code.md) record the scope. Product baseline is bb4fe7c5f1ae4456c659babfcd16e8d33a9b741d; main15011042b1fe093becbe68177e6396e456b1f35f was freshly fetched and already integrated.

## Security and compatibility

Each new code contains 20 independently selected symbols from a 32-symbol ASCII alphabet: 100 bits of entropy. Terminal display groups by four; canonical uppercase is hashed with SHA-256. No plaintext code is stored in the database. New-code input accepts ASCII case, spaces and hyphens, but does not guess lookalikes or accept Unicode folding. Digit 0 is excluded; O is a letter. I, L and 1 are also excluded. Existing 43-character codes retain exact case-sensitive redemption and original expiry. Both digests are always computed/compared for admitted attempts, including malformed and unknown-account requests, to support overlapping legacy/new input shapes without an early digest-success return.

All prior account binding, one-active-proof, account transaction locking, one-use consumption, 30-minute DB expiry, admission limits, password hashing, session invalidation, CSRF/Origin and controlling-terminal guards remain. No migration, account reset, new external service or dependency is introduced. This is honestly 100-bit rather than the old 256-bit generation default. Code entry remains masked and is cleared on submission/abort; no new clipboard, logging or persistence feature is added.

## Verification boundary

Unique project ibe160-pm-code-format-20261105 and fresh private volume; no owner-account or production tests. Backend uses the candidate source read-only and the previously qualified PG image. Test API is loopback19441, frontend16440. The browser adapter copies the existing focused tests into ignored scratch, replacing only project/port literals; assertions are preserved. Traces, screenshots and video remain off. This synthetic bridge network does not claim production storage-network isolation or external HTTPS/SSH qualification.

Backend command: docker compose -p ibe160-pm-code-format-20261105 -f tmp/readable-code-tests/compose.yaml exec -T private-api python -m pytest -q -p no:cacheprovider --tb=short tests/test_password_recovery.py tests/test_password_recovery_operator.py tests/test_password_change.py tests/test_private_access.py tests/test_cleanup_observability.py tests/test_password_restore.py

Final backend: 116 passed in196.33s. Ten new cases cover generation calls, shape/normalization, uppercase/lowercase/grouped/spaced and 43-length-separated input, exact legacy compatibility, replay and malformed-attempt throttling. Existing tests cover expiry/revoke/wrong-account, concurrency, data preservation, session revocation, restore invalidation, controlling PTY, compensation and secret-safe audit storage. Earlier pre-review run:113 passed191.07s, historical only.

Browser command from frontend: COMPOSE_PROJECT_NAME=ibe160-pm-code-format-20261105 npx playwright test --config .password-regression-tests/format.config.ts. Final browser result: 35 passed in 3.5m, recorded with source fingerprints in [the verification manifest](evidence/readable-code/verification.json). Expanded operator-to-app test submits lowercase spaced code and scans logs for the exact submitted, displayed and canonical variants. Help text association and MOTTATT order are asserted. TypeScript/Vite and five-file Python AST checks passed. Old full gateway/preflight/helper/legacy evidence is reused only for unchanged scope; the revised S4 secret scanner is syntax-checked, not claimed as a new full S4 run.

## Review and encountered failures

BMAD one-shot blind review returned five findings. All were individually verified and patched: ambiguous43-character parsing, missing visible ACK order, incomplete log-marker coverage, missing deterministic generator assertion and guide readability. Follow-up review found no additional functional digest-handling issue; final documentation spacing/alphabet rendering was corrected. No known independent implementation defect is deferred.

Initial test-edit script used Windows default encoding and failed on a Unicode fixture; the affected test file was reconstructed from the exact HEAD version and reapplied with explicit UTF-8, then syntax/regressions passed. Docker automatic address pools were exhausted; inspected existing ranges and assigned only this project10.247.250.0/28, leaving other networks untouched. Initial browser run failed at login because internal-only Docker networking suppressed the published API port (Failed to fetch); stopped that run after three failures/next case starting. Recreated only this test network as a bridge with loopback API exposure; health200 verified before the full repeat. No product fix or owner-data mutation was used to mask that setup failure.

## Remaining owner qualification

The shorter code still requires a new capture-free physical handoff and redemption on the tablet. The failed long-code trial remains failed in history. Exact SSH → installed helper → Compose PTY, independent access/identity and remaining release gates are not replaced by local CLI or automated success. PM-E1 and S1–S4 remain in review. No production change, merge to main, deployment, tag or release occurred.


## Local handoff preparation

After final tests, stopped/removed only the automated test project's containers/network; synthetic volume remains ignored. Rebuilt the owner test frontend for15440/API18441 and recreated its API against the existing private volume. Frontend200 and APIhealthok verified. Unrelated ibe160-v1-final services were untouched. The owner test service remains running for the ongoing guided trial; no production deployment occurred. Refresh the tablet test page before issuing a new code. Original test-account passwords/data were not reset by this work.


## Subsequent owner clarification — asynchronous sending

The owner clarified that manual email/Teams sending must not require simultaneous contact or recipient knowledge of the operator acknowledgement. The later [SENDT correction](spec-sent-recovery-handoff.md) supersedes earlier MOTTATT/order guidance in this historical format qualification. Code format, generation, TTL and ordinary redemption authority are unchanged. Preserve earlier evidence as executed; use the current operator/user routine for the next trial.
