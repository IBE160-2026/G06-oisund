# G06 — Individuell: reproducible V1

IBE160 Programmering med KI, Høgskolen i Molde, autumn 2026. Author: Jonas Øisund.

This V1 imports a supported text-PDF shift, permits correction and explicit saving, confirms a saved plan, and supports manual activity selection, shift status and source-linked notices. React/TypeScript talks to actual FastAPI and PostgreSQL. Planned times never establish real progress or road clearance. Stories 12.1–12.4 are accepted; delivery story 12.5 awaits owner review. [Submission index](docs/submission/README.md).

## Clean checkout and startup

Install Git, Node.js 24 with npm, Docker Desktop with Linux containers and Compose v2. Use a desktop Chromium browser. Exact tested versions/source are in the [reproduction record](docs/evidence/12-5-reproduction.md). Run commands in the checkout root in PowerShell or a POSIX terminal:

```powershell
git clone --branch story/12-5-reproducible-submission https://github.com/IBE160-2026/G06-oisund.git ibe160-submission
cd ibe160-submission
git rev-parse HEAD
node scripts/submission.mjs init
node scripts/submission.mjs status
```

The delivery is versioned Git content; no local archive is needed. `init` generates ignored local database/account secrets, pulls pinned base images, freshly installs locked npm/Python dependencies with an uncached build, builds the frontend, starts five services, applies versioned migrations and idempotently seeds the fictional day and synthetic account. Expect healthy containers, a fictional day UUID and synthetic-account confirmation. Every failed subprocess exits nonzero; resolve the failure before continuing.

Installation requires internet access to Git, Docker registries, npm and PyPI. Browser-test installation also downloads Playwright Chromium. Once installed, runtime requires only local loopback connections between browser/frontend/APIs/PostgreSQL, with no CDN, owner account, tunnel, paid service, private PDF, backup or live feed.

The fixed project is `ibe160-submission`; its new volumes are `ibe160-submission_submission_fictional` and `ibe160-submission_submission_private`. PostgreSQL publishes no host port. Scripts explicitly select the exact project/file and refuse an existing project owned by another checkout. Leave occupied ports and existing services alone; the recipe fails rather than reclaiming them. Do not use operational Compose overlays.

| Entry | Address | Evidence type |
|---|---|---|
| Private workspace | http://127.0.0.1:15325/private | Actual authenticated API/PostgreSQL, generated synthetic account |
| Fixed fictional assessment | http://127.0.0.1:15325/ | Actual fictional save/reopen, separate database |
| No-login simulation | http://127.0.0.1:15325/demo.html | Labelled in-memory scenarios/failures; no persistence claim |
| Private / fictional health | http://127.0.0.1:18328/health / http://127.0.0.1:18327/health | Database-backed health |

## Actual application journey

Read `.private-runtime/submission/account.json` locally for the generated `synthetic-submission` login. This ignored file is never part of the submission. Preserve both secret files while retaining the volumes. Ordinary `app.manage provision` still refuses the reserved `synthetic-` namespace; only the bounded demonstration initializer provisions this account.

1. Open `/private`, sign in and choose `Eksempelfiler/Testskift-A.pdf` under **Velg tekst-PDF**. A–E and the independent [expected facts](Eksempelfiler/Fasit-testskift.json) are fully synthetic. Import is transient: inspect the summary before saving.
2. For correct input choose **Alt stemmer – lagre og fortsett**. To exercise correction choose **Rett eller legg til opplysninger**, edit **Til sted** and **Kilde / manuell rettelse**, then **Lagre utkast** and inspect the acknowledgement. PDF facts remain separately available; missing facts stay unknown. A first draft's bus is saved with the whole draft; a clean saved draft offers **Lagre buss/vogn**.
3. Continue to **Gjennomgå lagret utkast** when offered. Inspect the saved-version approval, explicitly classify activities when required and acknowledge listed unknowns. Select **Bekreft gjennomgått plan**. Confirmation does not start work: the day shows no selected activity and **Ikke startet**.
4. **Velg aktivitet …**, inspect details, return to the day and explicitly **Start skift** / **Bekreft skiftstart**. Manually select and save an **aktivitetsstatus**. The confirmed plan's bus has its own **Lagre fysisk buss** action.
5. Optionally open **Manuelt vedlikeholdte avvik**, register a synthetic source-linked notice with a future ending date and explicitly save. Source checking, validity, manual ending and automatic expiry are distinct. **Les avvik for linjer og datoer** filters by exact line and planned Oslo calendar date; an empty list proves no source coverage.
6. Reload and reopen the saved plan; check acknowledged activity/status/bus. End or abort with explicit confirmation; inspect the recap and reopen. Import C separately for midnight/date rollover; E exercises sparse/unknown facts. [Review checklist](docs/submission/review-checklist.md).

Unsupported/scanned/malformed PDFs offer manual entry. This is a bounded two-column text-layout parser; [supported input and limits](docs/submission/supported-input.md).

## Stop, restart, retention and reset

```powershell
node scripts/submission.mjs stop
node scripts/submission.mjs start
node scripts/submission.mjs restart
node scripts/submission.mjs status
```

Stop/start/restart preserve volumes, sessions and saved records. Repeated initialization neither changes an existing password nor reseeds an unexpired fictional day. Reads/retries/restarts never renew server deadlines. Sessions last 14 days; private drafts/plans have seven-day retention, with dependent records following the parent deadline. Qualified notices have separate storage retention seven days after effective ending; validity is not road clearance. Expired access is immediately refused; startup/hourly cleanup removes expired records. The [evidence](docs/evidence/12-5-reproduction.md) separates restart checks from accelerated expiry tests.

Unsaved private work lives in page memory; refresh/closing/logout/expiry can lose it. Keep the page open during an unresolved save and use its explicit check/retry controls. Reconnecting alone never saves.

Erase **only** disposable submission data and seed a new fictional day plus the same generated login:

```powershell
node scripts/submission.mjs reset
```

Reset checks project/config ownership, running network/volume identities, exact database identity and synthetic-only accounts before mutation. A non-synthetic account refuses the entire reset before either database changes. It preserves generated passwords and migration history; saved synthetic plans/notices/sessions are removed, so sign in again. Never substitute operational databases or delete secrets while retaining volumes. `stop` is sufficient to leave the demo; no global cleanup is required.

## Repeat verification

```powershell
node --test scripts/test-submission.mjs
node scripts/submission.mjs test-backend
node scripts/submission.mjs install-browser
node scripts/submission.mjs test-browser
```

Backend verification runs actual private HTTP/PostgreSQL tests, then fictional/parser tests in their respective containers. Opposite-mode suites are intentionally skipped; actual counts/source belong to the [current evidence](docs/evidence/12-5-reproduction.md). The existing `PRIVATE_TEST_PROJECT=ibe160-private-tests` marker and non-synthetic refusal remain unchanged despite the separate Compose name. Browser tests use freshly installed Playwright Chromium and the actual APIs. Linux may additionally need system libraries: from `frontend`, run `npx playwright install --with-deps chromium`, then return to the root. Generated browser output is ignored under `tmp/`; selected evidence is versioned separately.

[Traceability](docs/submission/traceability.md), [AI/human reflection](docs/submission/ai-reflection.md) and [known limits](docs/submission/known-issues.md) distinguish extraction, integration, UI, historical physical observations and unperformed field benefit. No real-world time savings or complete accessibility conformance is claimed.

## Preserved history

Current scope: [SCOPE-02](_bmad-output/planning-artifacts/sprint-change-proposal-2026-10-19.md), [requirements](_bmad-output/planning-artifacts/prds/prd-IBE160-2026-09-21/prd.md), [stories](_bmad-output/planning-artifacts/epics.md), [sprint](_bmad-output/implementation-artifacts/sprint-status.yaml). The earlier accumulated README remains in Git at `99c272b09abaa5ffecf3286b406fbf065a445c7c`.

Preserved reports: [12.1/12.2 integration](docs/evidence/12-integrated-handoff.md), [12.3 physical acceptance](docs/evidence/12-3-device-acceptance-2026-10-27.md), [12.4 handoff](docs/evidence/12-4-handoff.md), [12.4 corrected import](docs/evidence/12-4-import-experience.md), [12.4 main integration](docs/evidence/12-4-main-integration.md), [development log](docs/development-log.md). Their original revisions, failures and pending statements remain historical. [Tablet operations](docs/tablet-production.md) describes a separate protected environment and is not a recipe prerequisite.
