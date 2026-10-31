# PM-E1 implementation status

2026-10-31. Isolated implementation authorized; no release authorization. BMAD Build rendered once using extension-local configuration. Main baseline unchanged at `5cee9e03d03d2c9c165c7f8fec64aa3e146959ab`; implementation starts from `b352640c3cfb80b962db6056116e1c747cfb760a`.

| Story | Technical work | Mandatory owner qualification | Overall |
|---|---|---|---|
| PM-E1-S1 | Implemented; two three-layer review rounds, fixes, final41 backend +18 browser passed | Actual device/owner UX: utsatt – krever eier | In review, not complete |
| PM-E1-S2 | Implemented; three-layer review and patches, final73 backend +18 helper passed | Identity/handoff/recording controls: utsatt – krever eier | Not complete |
| PM-E1-S3 | Next after reviewed S2; independent work authorized | Actual device/owner UX: utsatt – krever eier | Not complete |
| PM-E1-S4 | Independent qualification after S1–S3 | Owner operator walkthrough and acceptance: utsatt – krever eier | Not complete |

## Isolation

`compose.password-tests.yaml` owns only project `ibe160-password-tests`, loopback ports 18440/18441 and separate PostgreSQL volumes. UI preview uses 15440. `.private-runtime/password_tests-postgres-password` is ignored, randomly generated locally and never included in evidence. Existing final-control runtime and production are not operated. Test marker `PRIVATE_TEST_PROJECT=ibe160-private-tests` is the existing backend synthetic-data safety marker, not a volume/project selection.

Browser evidence uses synthetic data only, no traces/videos and no credential/code screenshots. Operator tests must capture synthetic terminal traffic internally only to assert behavior, never emit codes to test reports.

## Reproducing browser verification

Build-time Vite settings are required because `npm run start` serves the built output. In PowerShell, set `VITE_PRIVATE_API=http://127.0.0.1:18441` and `VITE_FICTIONAL_API=http://127.0.0.1:18440`, then run `npm run build` in frontend. Set `COMPOSE_PROJECT_NAME=ibe160-password-tests` before Playwright. Run focused cases with `npx playwright test --config playwright.password.config.ts`. The config matches only password test basenames, not the containing checkout name.

For established browser regressions, run `node scripts/prepare-password-tests.mjs` from the repository root, then select the required specs explicitly with `playwright.password-regression.config.ts`. Generated sources live in ignored frontend/.password-regression-tests; historical fixtures are unchanged and screenshots/metrics are redirected to ignored tmp/password-regression-evidence. Do not run DB-mutating suites concurrently against these synthetic fixtures.

## Clean-checkout startup — PowerShell 7 (review B10/R1-B10)

Run from this isolated checkout in PowerShell 7 (`pwsh`), not Windows PowerShell 5.1. The local random secret is disposable test infrastructure, never a production credential; do not print or commit it. Refuse to replace an existing file. Explicit project selection prevents a surrounding Compose environment from choosing another runtime.

```powershell
$env:COMPOSE_PROJECT_NAME = 'ibe160-password-tests'
New-Item -ItemType Directory -Force .private-runtime | Out-Null
$pmSecretPath = Join-Path (Get-Location) '.private-runtime/password_tests-postgres-password'
if (-not (Test-Path -LiteralPath $pmSecretPath)) {
    $pmBytes = [Security.Cryptography.RandomNumberGenerator]::GetBytes(32)
    [IO.File]::WriteAllText($pmSecretPath, [Convert]::ToHexString($pmBytes))
}
docker compose -p ibe160-password-tests -f compose.password-tests.yaml up -d --build --wait
```

Check all four services healthy with the same explicit project/file. This creates only the two password-tests volumes and ports listed above. Never substitute existing production/final-control volumes or passwords. Install pinned frontend dependencies with `npm ci --no-audit --no-fund` in frontend, then use the build-time variables and commands above. The regression adapter requires Node and Git; Docker Desktop and local headless Edge are used on Windows. Containers start the versioned private migrations automatically against their isolated database.

After all tests, stop only this runtime with `docker compose -p ibe160-password-tests -f compose.password-tests.yaml stop`. Retain its synthetic volumes for reproducibility unless a separate explicit cleanup task removes them. Do not use global container/volume pruning.

## Input-source restriction

The historical import regression package includes anonymized reference PDFs. Those are not synthetic input and are excluded from future qualification: the password regression config filters `approved example` browser cases. Backend commands must select synthetic-only cases; the broad reference-file mount is removed before subsequent story runs. Earlier mixed-source run results remain recorded as such, not relabelled synthetic. Existing repository reference files are unchanged.

S1 evidence: [dispatch/review/verification](spec-pm-e1-s1.md), [render/test map](evidence/s1/loop1/README.md), [proxy](evidence/s1/proxy.md). Required regression coverage comprises77 distinct synthetic cases; earlier anonymized-reference executions are separately recorded and excluded. Physical acceptance remains open. Other checkout v1-final-control was checked again and remains clean.
