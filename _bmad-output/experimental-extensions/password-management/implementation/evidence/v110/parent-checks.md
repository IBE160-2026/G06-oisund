# Parent verification — 2026-11-04

Integrated source baseline `b7af6b5ebbd1118e3c85fa164879ad68c4f86b4f`, containing main `15011042b1fe093becbe68177e6396e456b1f35f` (v1.0.1 commit). Tests use generated synthetic accounts/data only. No production socket, account, SSH or device operation. Windows Docker Desktop engine29.7.2, Node24.19.0, local headless Edge. Later helper-only review patch does not alter application/frontend/gate sources tested here.

## Backend and browser

Unique project `ibe160-password-rc-20261104`, loopback18440/18441, UI15440. Base `compose.password-tests.yaml` plus ignored `tmp/pm-rc-overlay.yaml` overrides both DB images/builds to `deploy/ubuntu/Dockerfile.postgres` using tag `ibe160-password-rc-pg:20261104`. The override uses root build context `.` (Compose paths are relative to the first file). Volumes are unique to this project. Existing ignored synthetic infrastructure password reused, never printed. This direct-API test lane is not the restricted-runtime proof: that is the separate S4 combined run.

```
docker compose -p ibe160-password-rc-20261104 -f compose.password-tests.yaml -f tmp/pm-rc-overlay.yaml up -d --build --wait --wait-timeout 180
docker compose -p ibe160-password-rc-20261104 -f compose.password-tests.yaml -f tmp/pm-rc-overlay.yaml exec -T private-api python -m pytest -q -p no:cacheprovider --tb=short tests/test_password_recovery.py tests/test_password_change.py tests/test_password_recovery_operator.py tests/test_private_access.py tests/test_cleanup_observability.py
```

Result: **103 passed in174.39s**, no skips. No reference-PDF tests selected. Run DB-mutating suites sequentially.

Frontend build: set `VITE_PRIVATE_API=http://127.0.0.1:18441` and `VITE_FICTIONAL_API=http://127.0.0.1:18440` before `npm run build` in frontend. TypeScript/Vite passed, unchanged bundle `main-DnQxIuR2.js`.

The tracked focused tests require exact project name `ibe160-password-tests`; initial direct use of the new name failed both beforeAll guards (2 failed,33 not run), before account mutation. Reproduction adapter copies only `frontend/tests/password-change.spec.ts` and `password-recovery.spec.ts` into ignored `frontend/.password-regression-tests`, replacing only the literal `'ibe160-password-tests'` with `'ibe160-password-rc-20261104'`. All assertions and `require_synthetic_accounts` checks are unchanged. An ignored config imports `frontend/playwright.password.config.ts`, overrides testDir to those copies, outputDir to ignored tmp and webServer.cwd to frontend. Set `COMPOSE_PROJECT_NAME=ibe160-password-rc-20261104`; run from frontend:

```
npx playwright test --config ../tmp/pm-rc-playwright.config.ts password-change.spec.ts password-recovery.spec.ts
```

Result: **35 passed in3.5m**. Trace/video/automatic screenshots disabled; existing blank-form screenshot cases contain no credentials. Earlier82 selected synthetic legacy regressions and reviewed S1–S3 race/UI evidence are reused for unchanged application/business/frontend/lockfile sources; `git diff 8fd6da2..b7af6b5 -- backend/app backend/migrations frontend/src frontend/package-lock.json backend/requirements.lock` is empty.

## Maintenance helper and gate

Helper suite runs in the built API image, network none, read-only root, cap-drop ALL, no-new-privileges, tmpfs /tmp and readonly bind of deploy/ubuntu to /ops. No Docker socket. Python unittest discovery runs all test_*.py under /ops with `os.chown` mocked; all production subprocess calls are already mocked by tests. Initial native --mount quoting failed before execution; corrected full quoted mount string succeeded. **26 tests passed in0.109s** before review; final postpatch combined suite: **27 passed in0.099s**, including both actions with leading-hyphen usernames and --help treated only as positional account text.

Gate builds use actual runtime Dockerfile, then actual Dockerfile.test with `GATE_IMAGE=ibe160-password-rc-gate:20261104`. Test command: `python -m pytest -q -p no:cacheprovider /gate-test`, readonly bind of deploy/tablet/access_gate, PYTHONPATH=/gate-test, user10001:10001, read-only root, cap-drop ALL, no-new-privileges, pids-limit32, tmpfs /tmp size1m, network none. **32 passed,1 skipped in32.18s**. The opt-in real libc DNS case was then run separately with the same barriers plus `--dns 127.0.0.1 --dns-option timeout:30 --dns-option attempts:5 -e O5_LIBC_DNS=1`, selecting test_libc_dns.py: **1 passed in7.64s**. Total33 distinct gate tests passed; no skipped required case remains. DNS namespace is container-local, never host configuration.

Observed parent image identities (Docker image inspect .Id):

| Image | Identity |
|---|---|
| private-api | sha256:22bc12298b1c38cb7ce0ffb912e594cf11875ef3d1be98280091b148c52a56db |
| gate runtime | sha256:143123c7861f8f621d577860db639b57426590dd143d502e32d4c484e87c6c56 |
| gate test overlay | sha256:fae2a5c7867043b5ab3b05fd9bf8d8c85d646d3b21359a01cb425bb8bf6921a2 |
| PostgreSQL overlay | sha256:c1f1abaa7051a0df0c413092ea8e68f1443929505c443a9e7069adcc3600d20b |

Exact combined-run sources/runtime assertions and post-review results are linked from [candidate report](../../v110-candidate.md). Final combined parent run:13 phases,20 scans,3 negative controls,148 matching fingerprints; [runtime manifest](runtime-parent-final.json).

These local tests do not qualify actual SSH → host helper → Compose PTY → inner CLI delivery, real no-recording controls, external TLS/IdP or physical owner acceptance. Those remain explicit owner checks.
