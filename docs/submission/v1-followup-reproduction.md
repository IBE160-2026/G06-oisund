# Historical C1 qualification recipe

> Current-scope note, 31 October 2026: Jonas includes completed Ubuntu integration in final V1. [Superseding scope/status and version-specific evidence](v1-scope-and-operations.md). Earlier bonus/v1.0.1 exclusions or no-deployment statements below describe their original checkpoint. Application/D1–D3/Epic12 acceptance is unchanged; original tests are not relabelled later-code runs. O3–O6 remain open; final freeze, reflection review and course submission remain pending.

For the assessor's self-contained final delivery, use [the current README](../../README.md) and remain in its exact checkout. This file preserves the separate C1 qualification commands/configuration. The named follow-up branch was subsequently integrated and deleted; C1 remains available as immutable main history. Optional historical checkouts below deliberately reproduce old inputs and are not final-delivery startup steps. [Outstanding delivery/operational work](delivery-readiness.md) is tracked separately.

This is the **owner-accepted corrected V1 product candidate** on `followup/v1-d1-d2-d3`, based on main `6d1259628c5fc7cec2d649e4097331d1606d9574`. Exact product/test/tooling candidate is `3c2287ed68d0cbb1923439fc6ee00254395072a4`; [binding of229 executed inputs](../evidence/v1-followup-candidate-binding-20261029.json) and [qualified results](v1-followup-qualification.md) establish its source identity. Later branch commits contain associated evidence/documentation/logs. The accepted course snapshot `c067fdbb20150219c041588ed4e990e7b0ef6b94` and original12.5 instructions remain historical. This recipe does not deploy, migrate ordinary data, merge or submit anything.

## Local synthetic runtime

Use a separate checkout of the published candidate with Docker Desktop already available, Node/npm and Python3.12 or compatible installed. The manual-preview recipe is qualified on Windows/PowerShell and uses exact Win32 process metadata for safe stopping; no cross-platform manual-preview result is claimed. Keep the project name/ports and use only the included guarded runner. No `down -v`, prune, production Compose or existing account password reset is required.

An existing follow-up project owned by another checkout is deliberately refused. Use the original prepared checkout or a separate Docker context/machine; do not detach its volumes or silently attach a new checkout. The initial work freshly installed locked dependencies and rebuilt/qualified the final source. A later separate-checkout delivery reproduction and actual Lenovo22-case execution are recorded [here](../evidence/v1-acceptance-2026-10-29.md); neither alone means a second clean machine or owner acceptance; the separate explicit owner decision is now recorded.

## Corrected delivery snapshot and executed recipe

The new tested **product delivery snapshot is C1 `3c2287ed68d0cbb1923439fc6ee00254395072a4`**. It contains the D1–D3 fixes and original guarded `scripts/submission.mjs` recipe; `c067fdb` remains the accepted historical12.5 snapshot. Jonas explicitly accepted C1 and the local V1 basis on29October2026; see the owner record. No release/tag is created.

On a machine/context without an existing project/occupied ports, use a separate checkout detached at C1, then `node scripts/submission.mjs init`, `status`, and the actual user journey in the [root README](../../README.md). Default project/ports remain `ibe160-submission`,15325/18327/18328; generated test login is in that checkout's ignored `.private-runtime/submission/account.json`. `stop`, `start`, `restart`, guarded `reset`, and `test-browser` retain their original meaning. Never use production overlays.

On this host the older submission project already exists, so it was preserved. A **config-only isolated instance** at `D:/IBE160/tmp/v1-delivery-candidate` uses project `ibe160-v1-delivery` and UI/API ports15327/18331/18332. [Exact method](../evidence/v1-acceptance-methods/prepare-final-reproduction.py) and [per-file original/instance hashes](../evidence/v1-acceptance-reproduction-instance.json) specify all four literal substitutions and refuse unrelated edits. No application source changes or bonus server files are included. This translated instance is not a pristine-config C1 checkout.

Executed `init` freshly built uncached images/locked dependencies and started five healthy services; `verify-submission-runtime.mjs` passed data/deadline preservation, reset/refusal and unrelated-resource checks; locked host npm install followed by `test-browser` passed all3 existing actual API/PostgreSQL journeys. Existing Playwright Chromium cache was reused instead of downloading it again. [Results, logs, source/asset proof and limits](../evidence/v1-acceptance-2026-10-29.md#fresh-delivery-reproduction) bind this recipe execution to C1 and the exact configuration. UI `http://127.0.0.1:15327/private` is for delivery reproduction; the active Lenovo walkthrough remains on15326 with its own dedicated credentials/account. Do not reset either retained environment during owner assessment.

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
