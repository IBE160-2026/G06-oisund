# G06 — Individuell: reproducible V1

IBE160 Programmering med KI, Høgskolen i Molde, autumn 2026. Author: Jonas Øisund.

This V1 imports a supported text-PDF shift, permits correction and explicit saving, confirms a saved plan, and supports manual activity selection, shift status and source-linked notices. React/TypeScript talks to actual FastAPI and PostgreSQL. Planned times never establish real progress or road clearance. Stories 12.1–12.5 are accepted; [12.5 owner decision](docs/evidence/12-5-owner-acceptance-2026-10-28.md) records the completed final assessment. Epic12 and consolidated local V1 are complete after [accepted D1–D3 main integration](docs/evidence/v1-main-integration-20261029.md). [Submission index](docs/submission/README.md).

## Exact delivery checkout and startup

Use the **full delivery commit SHA provided with the course delivery**. Run directly from that checkout so this README and the final evidence stay alongside the product. Do not switch back to C1 or c067fdb as part of startup. During preparation no final delivery SHA/tag has been assigned; [remaining work](docs/submission/delivery-readiness.md) includes course requirements, owner review of the [reflection proposal](docs/submission/ai-reflection-proposal.md) and the operational checks to be executed/documented in a separate chat. No tag/release/submission is performed here. Server setup is separate bonus work and excluded.

The accepted product/test/tooling reference is C1 **`3c2287ed68d0cbb1923439fc6ee00254395072a4`**. The eventual delivery commit includes the same accepted product plus later documentation/evidence. C1 alone has an older README and does not contain the complete final documentation. The accepted historical12.5 snapshot `c067fdbb20150219c041588ed4e990e7b0ef6b94` remains unchanged.

Install Git, Node.js24 with npm, Docker Desktop with Linux containers and Compose v2. Use a desktop Chromium browser. Commands below are PowerShell. [Actually observed versions/configuration and evidence](docs/evidence/v1-acceptance-2026-10-29.md#fresh-delivery-reproduction) identify the tested Windows setup; no complete Linux-host qualification is inferred.

For a new checkout, obtain the **published final commit SHA** from the delivery reference, then run:

```powershell
$v1DeliveryCommit = (Read-Host 'Full 40-character delivery commit SHA').Trim().ToLowerInvariant()
if ($v1DeliveryCommit -notmatch '^[0-9a-f]{40}$') { throw 'Use the full delivery commit SHA.' }
git clone --no-checkout https://github.com/IBE160-2026/G06-oisund.git ibe160-v1
if ($LASTEXITCODE -ne 0) { throw 'Clone failed; do not reuse another checkout.' }
Set-Location -LiteralPath ibe160-v1
git checkout --detach $v1DeliveryCommit
if ($LASTEXITCODE -ne 0) { throw 'Delivery commit is unavailable; stop here.' }
$actualV1Commit = git rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $actualV1Commit -ne $v1DeliveryCommit) { throw 'Wrong delivery checkout.' }
if (-not (Test-Path -LiteralPath docs/submission/delivery-readiness.md)) { throw 'Final delivery documentation is missing.' }
node scripts/submission.mjs init
if ($LASTEXITCODE -ne 0) { throw 'Initialization failed; inspect the error before continuing.' }
node scripts/submission.mjs status
```

If you already opened this README in the supplied exact checkout, stay there: record `git rev-parse HEAD`, then run `node scripts/submission.mjs init` and `node scripts/submission.mjs status` in its root. Do not run initialization from an unrelated worktree. If the final SHA has not yet been published/supplied, the delivery freeze is still pending; do not substitute a moving main branch or guess a tag.

`init` generates ignored local database/account secrets, pulls pinned base images, installs locked npm/Python dependencies with an uncached build, builds the frontend, starts five services, applies versioned migrations and idempotently seeds the fictional day and synthetic account. Expect five healthy containers, a fictional day UUID and synthetic-account confirmation. A failed subprocess exits nonzero; resolve the failure before continuing. Installation needs access to Git, Docker registries, npm and PyPI; browser-test installation downloads Chromium. Runtime then needs only local loopback services, with no owner account, private PDF, tunnel, live feed or server bonus.

`start` and `restart` use installed images with `--no-build --pull never`. After changing source version, use `init` to build that version. The fixed project is `ibe160-submission`; volumes are `ibe160-submission_submission_fictional` and `ibe160-submission_submission_private`. PostgreSQL publishes no host port. The scripts refuse a project owned by another checkout. If a required port/project is occupied, stop and use an unused machine/Docker context; do not reclaim existing services, copy secrets between checkouts or apply production overlays. [The earlier same-host C1 qualification](docs/submission/v1-followup-reproduction.md) used an explicitly recorded namespace/port translation, not the default recipe below.

| Entry | Address | Evidence type |
|---|---|---|
| Private workspace | http://127.0.0.1:15325/private | Actual authenticated API/PostgreSQL; generated synthetic login |
| Fictional assessment | http://127.0.0.1:15325/ | Actual fictional save/reopen; separate database |
| No-login simulation | http://127.0.0.1:15325/demo.html | Labelled in-memory scenarios; no persistence claim |
| Private / fictional health | http://127.0.0.1:18328/health / http://127.0.0.1:18327/health | Database-backed health; private cleanup status is separate |

## Actual application journey

Read `.private-runtime/submission/account.json` locally for the generated `synthetic-submission` login. This ignored file is never part of the submission. Preserve both secret files while retaining the volumes. Ordinary `app.manage provision` still refuses the reserved `synthetic-` namespace; only the bounded demonstration initializer provisions this account.

1. Open `/private`, sign in and choose `Eksempelfiler/Testskift-A.pdf` under **Velg tekst-PDF**. A–E and the independent [expected facts](Eksempelfiler/Fasit-testskift.json) are fully synthetic. Import is transient: inspect the summary before saving.
2. For correct input choose **Alt stemmer – lagre og fortsett**. To exercise correction choose **Rett eller legg til opplysninger**, edit **Til sted** and **Kilde / manuell rettelse**, then **Lagre utkast** and inspect the acknowledgement. PDF facts remain separately available; missing facts stay unknown. A first draft's bus is saved with the whole draft; a clean saved draft offers **Lagre buss/vogn**.
3. A correct import already reaches the distinct saved-version approval. After editing/saving, choose **Fortsett til godkjenning** (the editor also offers **Gjennomgå lagret utkast**). Inspect the saved version, explicitly classify activities when required and acknowledge listed unknowns. Select **Bekreft gjennomgått plan**. Confirmation does not start work: the day shows no selected activity and **Ikke startet**.
4. **Velg aktivitet …**, inspect details, return to the day and explicitly **Start skift** / **Bekreft skiftstart**. Manually select and save an **aktivitetsstatus**. The confirmed plan's bus has its own **Lagre fysisk buss** action.
5. Optionally open **Manuelt vedlikeholdte avvik**, register a synthetic notice with **Kildebeskrivelse**, an optional fictional link such as `https://example.invalid/submission`, a future ending date and explicitly save. No source download is needed. Source checking, validity, manual ending and automatic expiry are distinct. **Les avvik for linjer og datoer** filters by exact line and planned Oslo calendar date; treat an empty list as a stored-data filter result, with source coverage still unknown.
6. Reload and reopen the saved plan; check acknowledged activity/status/bus. End or abort with explicit confirmation; inspect the recap and reopen. Import C separately for midnight/date rollover; E exercises sparse/unknown facts. [Review checklist](docs/submission/review-checklist.md).

Unsupported/scanned/malformed PDFs offer manual entry. This is a bounded two-column text-layout parser; [supported input and limits](docs/submission/supported-input.md).

## Stop, restart, retention and reset

```powershell
node scripts/submission.mjs stop
node scripts/submission.mjs start
node scripts/submission.mjs restart
node scripts/submission.mjs status
```

Stop/start/restart preserve volumes, sessions and saved records. Repeated initialization neither changes an existing password nor reseeds an unexpired fictional day. Reads/retries/restarts never renew server deadlines. Sessions last 14 days. Drafts expire seven days after their server creation. Confirmed plans expire seven days after the planned final end; an earlier server-recorded closure shortens the deadline to seven days after that closure. The earlier applicable bound is retained without renewal, and dependent records follow the parent deadline. Qualified notices have separate storage retention seven days after effective ending; validity is not road clearance. Expired access is immediately refused; startup/hourly cleanup removes expired records. The [evidence](docs/evidence/12-5-reproduction.md) separates restart checks from accelerated expiry tests.

Unsaved private work lives in page memory; refresh/closing/logout/expiry can lose it. Keep the page open during an unresolved save and use its explicit check/retry controls. Reconnecting alone never saves.

Erase **only** disposable submission data and seed a new fictional day plus the same generated login:

```powershell
node scripts/submission.mjs reset
```

Reset checks project/config ownership, running network/volume identities, exact database identity and synthetic-only accounts before mutation. A non-synthetic account refuses the entire reset before either database changes. It preserves generated passwords and migration history; saved synthetic plans/notices/sessions are removed, so sign in again. Never substitute operational databases or delete secrets while retaining volumes. `stop` is sufficient to leave the demo; no global cleanup is required.

To automate the stop/start, exact row/deadline persistence and positive reset checks, run `node scripts/verify-submission-runtime.mjs`. This intentionally resets demonstration data and records results under `tmp/submission-runtime-check.json`; run it after inspecting any manual demo work you want to keep.

## Optional verification commands

```powershell
node --test scripts/test-submission.mjs
node scripts/submission.mjs test-backend
node scripts/submission.mjs install-browser
node scripts/submission.mjs test-browser
```

Backend verification runs private HTTP/PostgreSQL tests with explicit exclusions `--ignore=tests/test_assessment.py --ignore=tests/test_pdf_import.py`, then runs only `tests/test_assessment.py tests/test_pdf_import.py` in the fictional container. Test selection is explicit for each mode; actual counts/source belong to the [versioned evidence map](docs/submission/README.md#evidence-and-source-map). The12.5 report retains its own historical source; none of these commands is a claim that it was rerun for a documentation-only delivery commit. The existing `PRIVATE_TEST_PROJECT=ibe160-private-tests` marker and non-synthetic refusal remain unchanged despite the separate Compose name. Browser tests use freshly installed Playwright Chromium and the actual APIs. Linux may additionally need system libraries: from `frontend`, run `npx playwright install --with-deps chromium`, then return to the root. Generated browser output is ignored under `tmp/`; selected evidence is versioned separately.

[Traceability](docs/submission/traceability.md), [AI/human reflection](docs/submission/ai-reflection.md) and [known limits](docs/submission/known-issues.md) distinguish extraction, integration, UI, historical physical observations and unperformed field benefit. No real-world time savings or complete accessibility conformance is claimed.

## Preserved history

[Completed Epic12 retrospective](_bmad-output/implementation-artifacts/epic-12-retro-2026-10-29.md) retains its original accepted-with-open-items verdict. Subsequent D1–D3 work, explicit acceptance and [main integration](docs/evidence/v1-main-integration-20261029.md) completed local V1 and Epic12. Tag/course preparation remains a separate [open register](docs/submission/delivery-readiness.md), now including owner-requested operational checks in another chat. No unperformed test or proposed postponement is marked approved by this distinction.

Current scope: [SCOPE-02](_bmad-output/planning-artifacts/sprint-change-proposal-2026-10-19.md), [requirements](_bmad-output/planning-artifacts/prds/prd-IBE160-2026-09-21/prd.md), [stories](_bmad-output/planning-artifacts/epics.md), [sprint](_bmad-output/implementation-artifacts/sprint-status.yaml). The earlier accumulated README remains in Git at `99c272b09abaa5ffecf3286b406fbf065a445c7c`.

Preserved reports: [12.1/12.2 integration](docs/evidence/12-integrated-handoff.md), [12.3 physical acceptance](docs/evidence/12-3-device-acceptance-2026-10-27.md), [12.4 handoff](docs/evidence/12-4-handoff.md), [12.4 corrected import](docs/evidence/12-4-import-experience.md), [12.4 main integration](docs/evidence/12-4-main-integration.md), [development log](docs/development-log.md). Their original revisions, failures and pending statements remain historical. [Tablet operations](docs/tablet-production.md) describes a separate protected environment and is not a recipe prerequisite.
