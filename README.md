# G06 — Individuell

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

## Medlemmer

- Jonas Øisund

## Current project state

On 19 October 2026 the owner approved [SCOPE-02](./_bmad-output/planning-artifacts/sprint-change-proposal-2026-10-19.md): a smaller course V1 with supported text-PDF import and correction, a saved day overview, manual activity navigation, manually maintained source-linked notices and a local fullstack demonstration.

The [active plan](./_bmad-output/planning-artifacts/epics.md) contains four epics and 20 stories. [Sprint tracking](./_bmad-output/implementation-artifacts/sprint-status.yaml) records stories 9.1 and 9.2 as done and story 9.3 in review; [readiness](./_bmad-output/planning-artifacts/implementation-readiness.md) covers planning, not implemented or tested product behavior. The [earlier baseline](./_bmad-output/planning-artifacts/archive/pre-scope-02-2026-10-19/README.md) is historical.

Story 9.2 implements a real React/TypeScript → FastAPI → PostgreSQL assessment slice. It accepts only the exact fictional example. Story 9.3 adds separately provisioned private access and an empty workspace; draft editing remains story 9.4. Story 9.1 adds an independent local PDF qualification CLI; PDF import is not connected to the application yet.

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

There is no editable/revision UI, application PDF handling, navigation/notices, live feed, GPS, offline operation or cloud deployment. The fixed fictional owner is only for local assessment; private access uses its own runtime below. Browser automation is bounded development evidence; actual tablet hardware, assistive technology and a complete accessibility audit remain unqualified. The development log records the exact performed checks and limitations.

## Run private access locally

Verification commands below require a **disposable, synthetic-only private database**. They refuse before test mutations when any non-synthetic account exists; account, session and throttle metadata are then left unchanged. The CLI reserves the `synthetic-` account prefix for automated fixtures and refuses operator provisioning in that namespace. Tests clear throttle metadata, so never bypass their guard to run alongside real accounts. Once real accounts are provisioned, first stop the operational private API to free port 8001, then set `$env:COMPOSE_PROJECT_NAME = 'ibe160-private-tests'` and run `docker compose -f compose.private.yaml up -d --build --wait`. Keep this variable set while running all private tests, browser tests and verification scripts: Docker inherits it and selects a separate disposable volume/network. Stop the disposable project with `docker compose -f compose.private.yaml down`, clear the variable using `Remove-Item Env:COMPOSE_PROJECT_NAME`, then restart the operational private project. Do not delete the operational volume or its local database secret.

Authentication mutations use an origin-scoped browser Web Lock held through response completion. Logout stays pending behind earlier logins across tabs, so a delayed login cookie cannot arrive after confirmed revocation. Unsupported browsers fail closed. Visibility changes clear authenticated presentation while preserving unfinished login input.

Start the fictional project above for the frontend, then start the separate private project. No account or application password is preconfigured. Generate the private PostgreSQL bootstrap secret locally; it is ignored by Git and mounted as a Docker secret rather than stored in Compose or the API URL:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/initialize-private.ps1
docker compose -f compose.private.yaml config --quiet
docker compose -f compose.private.yaml up -d --build --wait
docker compose -f compose.private.yaml exec private-api python -m app.manage provision YOUR_USERNAME
```

Provisioning requires an interactive terminal and prompts twice with hidden input (12–256 characters). Do not use `-T`, password arguments or environment variables for account provisioning. Duplicate names fail safely; there is no public signup. Open **http://127.0.0.1:5173/private**. The empty Norwegian workspace supports sign-in and logout; it contains no draft CRUD. The default `/` remains the fictional demo. Private health is **http://127.0.0.1:8001/health**.

The dedicated project/cluster/network/volume is `ibe160-private-work` / `private_pg`; no database host port is published. Demo reset cannot reach private storage. The local generated database secret is a bootstrap cluster credential, distinct from provisioned accounts. Preserve `.private-runtime/postgres-password` while retaining the private volume; PostgreSQL bootstrap does not change the existing role password when a different file is generated. Do not remove or replace it to reset an account. `docker compose -f compose.private.yaml down` preserves the private volume and accounts. No private reset command is provided.

Only explicit loopback development is supported. `APP_MODE=private-local`, `PRIVATE_LOOPBACK_DEVELOPMENT=1`, the exact configured loopback frontend origin and the isolated private database identity are required. Public hosts/HTTPS/public deployment configuration fail closed; a public deployment needs a separately designed HTTPS/Secure-cookie configuration. Current cookies are host-only, HttpOnly and SameSite Strict, with insecure transport allowed solely for this explicit local configuration. The shared frontend origin is trusted application code.

Passwords use salted Python/OpenSSL `hashlib.scrypt` (N=32768, r=8, p=3); no new package is required. Parameters follow the documented scrypt alternatives in the [OWASP password storage guidance](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), using the [Python 3.13 API](https://docs.python.org/3.13/library/hashlib.html#hashlib.scrypt). Credentials fail generically, and PostgreSQL admits at most 10 attempts per normalized name, 20 per IP and 100 globally per fixed 15-minute window. A global admission cap bounds stored buckets to 201 and prevents unbounded random-name metadata. This intentionally conservative local policy can temporarily block all sign-ins during abuse.

Sessions are opaque 256-bit random tokens stored only as SHA-256 hashes; server deadlines are exactly 14 days from sign-in and never renew. Every private resource checks the server session/ownership and returns `no-store`; own/foreign profile checks distinguish 401 renewal from safe 404 denial. Startup/hourly cleanup removes expired sessions/throttle metadata; accounts are not seven-day drafts. Signed HttpOnly CSRF cookies and custom proof headers plus exact-origin checks protect login/logout, following the [OWASP CSRF guidance](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html). Concurrent tabs may safely receive a rejected mutation if their CSRF cookies rotate; retry obtains a fresh proof.

Private presentation/credentials stay in page memory. No localStorage, sessionStorage, IndexedDB, service worker or offline grants store private work. A security-only `private_logout_pending=1` host cookie persists the logout lock across reloads; it carries no account identity or private payload. Logout clears presentation immediately and explicitly remains unconfirmed until revocation is acknowledged. Reload settles revocation before session reads or sign-in. BroadcastChannel sends only logout state notifications so another open tab clears immediately; history/visibility transitions revalidate access and stale responses cannot restore the view. This security marker and the HttpOnly authentication/CSRF cookies are the necessary authentication state, not saved work.

```powershell
docker compose -f compose.private.yaml exec -T private-api python -m app.manage migrate
docker compose -f compose.private.yaml exec -T private-api python -m app.manage cleanup
docker compose -f compose.private.yaml exec -T private-api python -m pytest -q tests/test_private_access.py
uv run --no-project scripts/verify-private-access.py
cd frontend
npm.cmd run build
npx.cmd playwright test
cd ..
```

Tests provision random synthetic accounts and delete them afterward. The verification script sequentially restarts private PostgreSQL/API, reapplies migrations, runs cleanup and **resets fictional demo data**, comparing the original session and deadline after each step; it emits no credentials. Browser tests cover 768/1440px keyboard/focus/wrapping, expiry, back/reload, concurrent tabs, unconfirmed and lost logout replies, and stale responses. Synthetic transport/deadline tests are labeled separately from real server/database checks. Screenshots: [768px](Docs/evidence/9-3-768.png), [1440px](Docs/evidence/9-3-1440.png). These profile/access checks do not establish draft retention or draft acceptance; story 9.4 introduces that behavior.

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
