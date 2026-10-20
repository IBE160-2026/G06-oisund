# G06 — Individuell

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

## Medlemmer

- Jonas Øisund

## Current project state

On 19 October 2026 the owner approved [SCOPE-02](./_bmad-output/planning-artifacts/sprint-change-proposal-2026-10-19.md): a smaller course V1 with supported text-PDF import and correction, a saved day overview, manual activity navigation, manually maintained source-linked notices and a local fullstack demonstration.

The [active plan](./_bmad-output/planning-artifacts/epics.md) contains four epics and 20 stories. [Sprint tracking](./_bmad-output/implementation-artifacts/sprint-status.yaml) records stories 9.1 and 9.2 as done and the remaining stories in backlog; [readiness](./_bmad-output/planning-artifacts/implementation-readiness.md) covers planning, not implemented or tested product behavior. The [earlier baseline](./_bmad-output/planning-artifacts/archive/pre-scope-02-2026-10-19/README.md) is historical.

Story 9.2 implements a real React/TypeScript → FastAPI → PostgreSQL assessment slice. It accepts only the exact fictional example; private access and editing remain later stories. Story 9.1 adds an independent local PDF qualification CLI; PDF import is not connected to the application yet.

## Run the fictional assessment

Requires Docker Desktop with Linux containers and Compose v2. Start Docker Desktop first. Run these commands from this repository root in PowerShell:

```powershell
docker compose config --quiet
docker compose up -d --build --wait
docker compose exec -T api python -m app.manage migrate
docker compose exec -T api python -m app.manage seed
```

Open **http://127.0.0.1:5173**. Select **Lagre fiktiv dag**, then **Åpne lagret dag på nytt**, or reload the saved URL. Seed prints an example UUID; `http://127.0.0.1:5173/?day=<UUID>` opens it. The screen always labels `Fiktive demodata`, planned times, explicit calendar dates, Europe/Oslo and unknown facts. It contains an overnight example with separate service/calendar dates. Controls work with Tab and Enter.

API health: http://127.0.0.1:8000/health. Both published ports bind to loopback; PostgreSQL has no host port. Compose creates a dedicated fictional-only PostgreSQL cluster. Its fixed bootstrap credentials are a cluster superuser, not a role restricted to one database. Private or operational data must never share this cluster. Do not publish these services publicly. This slice has no login or private API.

The versioned initial SQL migration runs automatically before API startup and can be rerun explicitly. The persistent volume is `ibe160-fictional-assessment_fictional_pg`; stopping/rebuilding containers preserves acknowledged data. Server-issued operation UUIDs exist before sending a day, serialize concurrent attempts and return the same accepted record on identical retry. Changed values for an accepted operation conflict. Only the fixed fixture may be created. Ownership is server-assigned to the fictional assessment owner.

Seven-day retention starts at the server's first successful day creation and never moves on read/retry. An unused operation also expires in seven days; successful creation aligns its expiry with the day. Expired access is immediately denied; startup and hourly cleanup purge the day and operation together. Unknown/removed operation IDs cannot recreate expired days. No browser storage or recovery cache stores the day; the URL contains only a fictional record UUID. A failed save retains the displayed example in page memory and requires explicit retry; no acknowledgement is claimed for timeout, HTML or malformed results.

## Reset, tests and persistence

Reset affects only this Compose assessment database and reseeds the fixed example. Wrong mode, database name, database user or external database host is rejected before connecting:

```powershell
docker compose exec -T api python -m app.manage reset --fictional-only
docker compose exec -T api python -m app.manage cleanup
docker compose exec -T api python -m pytest -q
powershell -ExecutionPolicy Bypass -File scripts/verify-persistence.ps1
powershell -ExecutionPolicy Bypass -File scripts/verify-unavailable.ps1
```

The API tests run against actual HTTP/PostgreSQL, create only fictional examples and simulate expiry by moving test deadlines in the assessment database. They verify replay/concurrency, exact payload equality, validation/no mutation, fixed retention, expiry/purge/no resurrection, origin checks and configuration denial. The restart script creates a day, restarts **both PostgreSQL and API**, waits for database-backed health, compares the entire returned record and checks replay identity.

For local browser development tests, install Node.js (verified 24.19.0, npm 11.17.0):

```powershell
cd frontend
npm.cmd ci
npm.cmd run build
npx.cmd playwright test
cd ..
```

On Windows the browser tests use installed Microsoft Edge. On Linux install Chromium first with `npx playwright install --with-deps chromium`. Tests use real save/reload at 1440/768 pixels with Oslo overnight date assertions, keyboard/focus checks, overflow checks and no localStorage. They forward a save to the real API, discard its acknowledgement, and verify that browser retry retains the operation and accepted record identity. Bounded response tests reject invalid dates/identities and clear expired presentation after 410 or the known deadline. Screenshots are written to `Docs/evidence/9-2-1440.png` and `9-2-768.png`. Synthetic response/transport failures are identified separately from actual database outage checks.

To inspect a real outage, load a fresh example, run `docker compose stop db`, then save; expect an unconfirmed/unavailable status and the example to remain visible. Restart with `docker compose up -d --wait db api`, then retry the same button. `docker compose stop api` similarly permits checking a failed reopen. Restore with `docker compose up -d --wait`.

```powershell
docker compose down
# To delete only the fictional assessment volume as well:
docker compose down --volumes
```

## Executable versions and limits

Resolved and executed from the actual package/image registries on 19 October 2026: Python **3.13.16**, PostgreSQL **17.11**, Node **24.19.0**, FastAPI **0.149.0**, uvicorn **0.54.0**, psycopg **3.3.6**, React/React DOM **19.3.1**, TypeScript **7.0.2**, Vite **8.3.4**, Playwright **1.64.1**. Docker server: **29.7.2**. Container base images are pinned by immutable digest, Python transitive versions by `backend/requirements.lock`, and npm dependencies/integrities by `frontend/package-lock.json`. Registry versions may differ from documentation pages; these are observed executable versions, not a claim about future latest releases.

There is no login, private input, editable/revision UI, application PDF handling, navigation/notices, live feed, GPS, offline operation or cloud deployment. The fixed fictional owner is only for local assessment. Browser automation is bounded development evidence; actual tablet hardware, assistive technology and a complete accessibility audit remain unqualified. The development log records the exact performed checks and limitations.

## Qualify the approved text-PDF examples

The independent [approved facts](Eksempelfiler/README.md) and [JSON oracle](backend/tests/fixtures/import_expected.json) cover seven anonymized PDFs / ten pages. From the repository root in PowerShell:

```powershell
docker compose build api
docker compose run --rm --no-deps -v "${PWD}/Eksempelfiler:/fixtures:ro" api python -m pytest -q tests/test_pdf_import.py
docker compose run --rm --no-deps -v "${PWD}/Eksempelfiler:/fixtures:ro" api python -m app.qualify_imports /fixtures
# To save normalized field comparisons, explicitly mount the evidence destination:
docker compose run --rm --no-deps -v "${PWD}/Eksempelfiler:/fixtures:ro" -v "${PWD}/Docs/evidence:/evidence" api python -m app.qualify_imports /fixtures --output /evidence/9-1-import-qualification.json
```

The qualification command deliberately exits **1** when any example is partial, unsupported, mismatched or untested. On 20 October, examples **1–5 and 7** matched every qualified source fact; example **6 is partial** because its Travel to row lacks the owner-completed start, endpoints and deadhead interpretation. All **113 source activities, 46 route trips and 30 numbered deadheads** were extracted; the 31st deadhead is owner-assisted. The [evidence report](Docs/evidence/9-1-import-qualification.md) records comparisons, negative results and the supported envelope. Manual completion never upgrades automatic completeness.

The adapter accepts PDF bytes with a `.pdf` filename and PDF signature, up to **10 MiB / 20 pages / 30 seconds per document**, with a **2 MiB result ceiling** in a terminable worker. It rejects corrupt, encrypted and image-only inputs; OCR is excluded. Originals stay in memory and are never included in the image or persisted. Qualification requires the approved SHA-256 values; missing or changed fixtures remain untested. Dependencies are pinned to executed pdfplumber **0.11.10** and its complete transitive set. The official [pdfplumber documentation](https://github.com/jsvine/pdfplumber) describes byte-stream input, cropping, text extraction and resource closing.

Downstream story 10.1 receives `app.pdf_import.extract_pdf` / `ImportDraft`, a separate nullable contract retaining source order, labels, per-field page/column/line provenance, unknown annotations, repeated duty occurrences and source pause rows. Derived calendar instants use Europe/Oslo service date, header start and stated Utstrekk; clock ordering alone does not establish a date. Duty suffixes and pause groups are derived, and actual bus remains null. Owner facts stay in the qualification layer. Only these HASTUS January examples with the observed header and body columns are qualified; extended header clocks (24:00 or later), intermediate stops, other layouts, DST transitions, private input and production integration remain unqualified.
