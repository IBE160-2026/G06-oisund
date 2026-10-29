# Reproduce the D1–D3 follow-up candidate

This is an **unaccepted follow-up candidate** on `followup/v1-d1-d2-d3`, based on main `6d1259628c5fc7cec2d649e4097331d1606d9574`. Exact product/test/tooling candidate is `3c2287ed68d0cbb1923439fc6ee00254395072a4`; [binding of229 executed inputs](../evidence/v1-followup-candidate-binding-20261029.json) and [qualified results](v1-followup-qualification.md) establish its source identity. Later branch commits contain associated evidence/documentation/logs. The accepted course snapshot `c067fdbb20150219c041588ed4e990e7b0ef6b94` and original12.5 instructions remain historical. This recipe does not deploy, migrate ordinary data, merge or submit anything.

## Local synthetic runtime

Use a separate checkout of the published candidate with Docker Desktop already available, Node/npm and Python3.12 or compatible installed. The manual-preview recipe is qualified on Windows/PowerShell and uses exact Win32 process metadata for safe stopping; no cross-platform manual-preview result is claimed. Keep the project name/ports and use only the included guarded runner. No `down -v`, prune, production Compose or existing account password reset is required.

An existing follow-up project owned by another checkout is deliberately refused. Use the original prepared checkout or a separate Docker context/machine; do not detach its volumes or silently attach a new checkout. The recorded work freshly installed locked dependencies in this new worktree and rebuilt/qualified the final source. It does not claim a second clean-machine bootstrap or a fresh physical-device acceptance of the final candidate.

```powershell
git checkout --detach 3c2287ed68d0cbb1923439fc6ee00254395072a4
npm.cmd ci --prefix frontend
python -m venv .venv-followup
& .venv-followup/Scripts/python.exe -m pip install -r backend/requirements.lock -r deploy/tablet/access_gate/requirements.lock
& .venv-followup/Scripts/python.exe scripts/verify-v1followup.py up
& .venv-followup/Scripts/python.exe scripts/verify-v1followup.py prepare
& .venv-followup/Scripts/python.exe scripts/verify-v1followup.py serve
```

Own project is `ibe160-v1followup-tests`; loopback UI15326, fictional API18329, private API18330. `up` checks the synthetic runtime identity and rebuilds only this project's services. `prepare` provides the local synthetic manual account in ignored `.private-runtime/v1followup-manual-credentials.json`; do not commit, paste or send its password. It creates controlled January2031 plans for inspection. `serve` freshly builds with those API settings, refuses an existing listener and verifies exact child identity plus an unpredictable one-use HTTP challenge from the built root. This avoids unreliable TCP metadata returning PID0 while retaining precise creation/command identity for stopping. Open `http://127.0.0.1:15326/private` locally. Stop only that owned preview with `verify-v1followup.py stop-preview`. No external Access/MFA route is started.

## Targeted verification

Install the browser selected by `frontend/playwright.v1followup.config.ts` (Edge on Windows; Chromium on other platforms). The recorded Windows run used the installed Playwright browser cache. Each browser invocation freshly builds and prepares isolated test copies; every result retains source/build hashes, raw log and verified archive/index in `docs/evidence/v1-followup-*`. Avoid editing product/test/tooling inputs while a gate runs. Backend tests mutate only this synthetic project after its guard succeeds.

```powershell
& .venv-followup/Scripts/python.exe scripts/verify-v1followup.py browser private-d1-remediation.spec.ts private-d2-qualification.spec.ts
& .venv-followup/Scripts/python.exe scripts/verify-v1followup.py backend tests/test_cleanup_observability.py tests/test_retained_data.py tests/test_account_notices.py tests/test_private_access.py
$env:PRIVATE_ORIGIN='http://127.0.0.1:15326'
$env:PRIVATE_LOOPBACK_DEVELOPMENT='1'
$env:PYTHONPATH='backend;deploy/tablet/access_gate'
& .venv-followup/Scripts/python.exe -m pytest -q -p no:cacheprovider backend/tests/test_cleanup_observability.py deploy/tablet/access_gate/test_gate.py deploy/tablet/access_gate/test_bounded_gate.py deploy/tablet/access_gate/test_gate_http.py
pwsh -NoProfile -File scripts/test-prepare-tablet-parity.ps1
```

The qualification ledger identifies the exact additional integrated selectors actually executed. Do not interpret these commands as a claim that every historical test or physical-device case was rerun.

## Bounded access probes

Build distinct candidate tags; never overwrite operational tablet tags. The test Dockerfile differs only by its `FROM` image. The actual executed build commands and output are archived in the gate-image, gate-test-image and gateway-image evidence.

```powershell
docker build -f deploy/tablet/access_gate/Dockerfile -t ibe160-v1followup-gate:20261029-r1 .
$candidateDockerfile = (Get-Content deploy/tablet/access_gate/Dockerfile.test -Raw).Replace('FROM ibe160-tablet-access-gate:11-6','FROM ibe160-v1followup-gate:20261029-r1')
New-Item -ItemType Directory -Path tmp -Force | Out-Null
[IO.File]::WriteAllText((Join-Path (Get-Location) 'tmp/Dockerfile.gate-tests'), $candidateDockerfile)
docker build -f tmp/Dockerfile.gate-tests -t ibe160-v1followup-gate-tests:20261029-r1 .
docker build -f deploy/tablet/Dockerfile -t ibe160-v1followup-gateway:20261029-r1 .
pwsh -NoProfile -File scripts/verify-tablet-proxy.ps1 -PythonImage ibe160-v1followup-gate-tests:20261029-r1 -GatewayImage ibe160-v1followup-gateway:20261029-r1
pwsh -NoProfile -File scripts/verify-tablet-api.ps1 -ApiImage ibe160-v1followup-tests-private-api
```

The proxy probe creates/removes its UUID internal network/containers with no host ports/database/volumes. The API probe uses a separate UUID internal network and temporary in-memory PostgreSQL with a restricted role and synthetic accounts; it deletes its generated credential after cleanup. Do not substitute a running operational service or image built from a different source. A current candidate image is built by the guarded `up` above.

These are isolated signed-JWT/Nginx/API tests. They cannot certify actual Cloudflare member-MFA policies, replay a genuine expired Access token or establish external WAN/IPv6 exposure. The [qualification ledger](v1-followup-qualification.md) gives the remaining owner/access checklist and exact proof boundaries.
