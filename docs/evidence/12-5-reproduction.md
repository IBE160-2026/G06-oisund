# Story 12.5 — executed clean reproduction

Technical delivery is ready for owner review; **owner acceptance is pending**. Epic 12 remains in progress. No merge, deployment, tunnel change, course-platform submission or extension work is part of this delivery.

## Source and clean environment

Fresh `git fetch origin` on 28 October 2026 resolved `origin/main` to **`99c272b09abaa5ffecf3286b406fbf065a445c7c`**, newer than the owner's last observed `4c8eb80`. No existing 12.5 branch/worktree was found. Implementation branch: `story/12-5-reproducible-submission`, worktree `D:/IBE160/tmp/story-12-5`.

The reproduction used a separate source-only Git clone, not a copy of the development directory:

```powershell
git clone --no-local --branch story/12-5-reproducible-submission D:/IBE160/tmp/story-12-5 D:/IBE160/tmp/submission-clean-20261028
cd D:/IBE160/tmp/submission-clean-20261028
git rev-parse HEAD
git status --porcelain
Test-Path frontend/node_modules
Test-Path frontend/dist
Test-Path .private-runtime
docker volume ls --filter label=com.docker.compose.project=ibe160-submission --format '{{.Name}}'
```

Observed initial source: `a0f417f5b789e2e78fd2d7877eec4ce3a25b3ddc`; Git status empty; all three paths absent; zero matching volumes. Only versioned Git content entered the clone. Corrections were committed and brought into it with `git pull --ff-only`. Each failed setup's **new submission-only** containers/volumes was identity-checked and removed before the next full uncached `init`; its generated secrets were moved to ignored `tmp/failed-*-runtime`, then new secrets were generated. Neither an operational runtime nor an existing database was reused.

Successful fresh installation/build source: `046de86c1b8b97e58506600bf8a06fa83cdce14e`. Backend launcher correction: `7339e561ae68c34e19de278d248a8ad5887505fc`; final backend invocation launched from `c14010e62ee25635e311aa12e979b11e5d3b74ed`. Browser, lifecycle/reset and final identity used **`f5037cbdf7de1790aeb222c0d937fe656ed8b061`**. Documentation/browser/tooling-only pulls during backend execution did not change its loaded backend tests or product inputs. Git comparison confirms `backend/app`, migrations, locked backend dependencies, `frontend/src` and locked frontend dependencies are unchanged from the accepted main baseline. Later evidence/review/log commits do not relabel these runs as executions of those later commits.

Observed environment: Windows amd64; Node 24.19.0/npm 11.17.0; Docker 29.7.2, Compose 5.5.1; API Python 3.13.16/FastAPI 0.149.0/psycopg 3.3.6/pytest 9.0.3; PostgreSQL 17.11; newly downloaded Playwright Chromium **156.0.8078.4**, desktop viewport 1280×720. [Identity record](12-5-identity.json) captures the OS release, five exact container/image/config/mount identities, 120 source-file SHA256 values and three served JS/CSS hashes. Every served asset equals its built image's bytes. [Read-only capture method](12-5-identity-method.mjs).

## Actual commands and outcomes

Run from the clean clone root. Logs preserve subprocess output; new text transcripts are UTF-8 conversions of PowerShell's redirected output. The original first two setup logs retain their original UTF-16 encoding.

| Command | Expected | Observed / evidence |
|---|---|---|
| `node scripts/submission.mjs init` | Generate secrets, fresh locked installs/builds, five healthy services, migrations, account and fictional seed | Final exit 0; uncached npm/Python installs and build, migrations 001–014, synthetic login and fictional day UUID. [Successful full init](12-5-init-final.txt) |
| `node scripts/submission.mjs status` | Exact isolated project, config, storage and account | Exit 0; five healthy services on frontend 15325, fictional API 18327, private API 18328; DBs publish no host port. [Identity](12-5-identity.json) |
| `node --test scripts/test-submission.mjs` | Config/storage/foreign-checkout refusal | **3/3 passed**, zero skipped. [Node log](12-5-node-tests.txt) |
| `node scripts/submission.mjs test-backend` | Private tests against private API; assessment/parser tests against fictional API | Exit 0: **367/367 private-mode backend cases** in 594.03s; **113/113 assessment/parser cases** in 8.25s; zero skipped. [Final backend log](12-5-backend-final.txt) |
| `node scripts/submission.mjs install-browser` | Fresh host npm install and Chromium download | Exit 0; 26 packages installed, browser/headless/FFmpeg downloads recorded. [Installation](12-5-install-browser.txt) |
| `node scripts/submission.mjs test-browser` | Actual rendered private fullstack journeys, no API mocks | **3/3 passed** in 50.4s; zero skipped/flaky. [Console](12-5-browser-initial.txt), [Playwright result](12-5-browser.json) |
| `node scripts/verify-submission-runtime.mjs` | Exact retained rows/deadlines after stop/start and restart; only demo reset | Exit 0, all four recorded checks passed. [Machine result](12-5-runtime.json), [console](12-5-runtime.txt), [versioned method](../../scripts/verify-submission-runtime.mjs) |
| `node scripts/submission.mjs reset` from the other implementation worktree | Refuse before database mutation | Expected exit 1: project belongs to another checkout/config. [Negative control](12-5-foreign-checkout-refusal.txt) |
| `COMPOSE_PROJECT_NAME=ibe160-tablet-prep` and `COMPOSE_FILE=compose.private.yaml`, then `node scripts/submission.mjs status` | Ignore inherited Compose selection and retain exact demo target | Exit 0, only the five submission services shown. [Selector control](12-5-inherited-selector.txt) |

The focused fictional-wrapper checks also ran in a disposable `--network none` Python container with the pinned Python image, read-only `deploy/submission` mount and `python -m unittest -v test_fictional`: **3/3 passed**. [Log](12-5-wrapper-tests.txt), [test source](../../deploy/submission/test_fictional.py). A preliminary agent invocation omitted `python` and failed before tests; the corrected invocation and root's independent repetition passed. That failed invocation is not a product-test result.

### Evidence categories

- **Extraction:** the successful 113-case selected run comprises **94 parser cases** and **19 fictional HTTP/PostgreSQL cases**. [Exact collection](12-5-collection.txt) distinguishes them. Parser cases include independent fixture expectations, supported/partial/rejected inputs and bounded worker/cancellation behavior. This is not a universal PDF success rate. Fully synthetic A–E and the independently authored [JSON facts](../../Eksempelfiler/Fasit-testskift.json) are versioned; no private original is required.
- **Functional/backend:** the 367 private-mode cases include real HTTP/PostgreSQL integration, domain/controlled ASGI checks and six new actual-database submission guard/idempotence cases. Those six compare all table rows when checking repeated initialization, four wrong-target settings and an ordinary-account reset refusal. The temporary ordinary guard account/session/throttle rows are removed by the test; real accounts are never used.
- **Rendered UI:** A and C verify exact uploaded bytes and independent activity/calendar facts, corrected destination/provenance, explicit save/reopen, saved-revision approval, separately entered bus, source-linked notice, explicit Start/outcome and ended/aborted read-only recap. A additionally restarts the database/API stack and compares recap, saved draft and session including deadlines. B saves a correct import directly into distinct saved-version approval. Test accounts are unique and cleaned by owner ID; the manual demonstration account/data are not reused as fixtures. [A synthetic records](12-5-journey-A.json), [C records](12-5-journey-C.json), [A screenshot](12-5-journey-A.png), [C screenshot](12-5-journey-C.png). Root visually inspected both recaps: A has one manually completed/four unregistered; C has one interrupted/fourteen unregistered and explicit next-calendar-day times. Screenshots do not establish physical usability or accessibility compliance.
- **Runtime/network boundary:** A/C requested only the local frontend/private API origins; the fictional source links are displayed and not downloaded. Installed-image `start`/`restart` use `--no-build --pull never`. Installation/rebuild/browser downloads need internet; ordinary application runtime needs local services. This does not claim an OS-level air-gap test.

## Durability, reset and preserved operation

The runtime verifier first clears disposable suite leftovers, creates an acknowledged synthetic draft/session through actual HTTP, then compares deterministic hashes of **every row in all 25 private tables and both fictional tables** after `stop`/`start` and `restart`. All match, including original expiry instants and migrations/security settings. This is a short real restart check, not a natural seven-day soak. Accelerated expiry/no-resurrection tests are separately in the backend suite.

Positive reset leaves one freshly provisioned synthetic account, 14 migration rows and the unchanged security setting; private business rows, receipts, sessions and throttle rows are zero. Generated database/account secret bytes stay identical. The fictional reset produces exactly one new day/creation operation. The actual ordinary-account negative test refuses before mutation; the two-table reset is not claimed as a distributed transaction against arbitrary infrastructure failures.

All **30 pre-existing containers** retain identical IDs, image IDs, start times and states from the [before record](12-5-protected-baseline.json) to the [after record](12-5-protected-final.json). The runtime verifier independently repeats the comparison around its lifecycle/reset actions. No command addresses the existing operational databases or account `jonas`; no private database snapshot, account/password change, tunnel process or production service operation is used. This is container/source preservation evidence, not an invented before/after comparison of private business rows.

## Failures, corrections and remaining limits

1. Initial `init` at `a0f417f5b789e2e78fd2d7877eec4ce3a25b3ddc` failed after successful fresh builds because Vite preview's unprivileged user could not write `/app/node_modules/.vite-temp`. `docker logs ibe160-submission-frontend-1 --tail 40` observed `EACCES`. The dedicated Dockerfile now grants that temporary directory to `node`. [Original failed init](12-5-init-initial.txt).
2. Fresh rerun at `86259102cabc5dbd6eb82edf0c0e3a858688ff90` reached five healthy services and the synthetic account, then failed fictional CLI migration: its `DATABASE_URL` existed only inside the server launcher process. The bounded fictional wrapper now supplies the generated secret to server/manage/test processes. [Second failed init](12-5-init-second.txt). Full fresh setup at `046de86c1b8b97e58506600bf8a06fa83cdce14e` passed.
3. Original broad backend command at `2bcbdede3c13918bf45dcf72862ffb2832b6d360` ran assessment cases against the private API: **14 failed, 466 passed**, aggregate exit 1. It is preserved in [original backend log](12-5-backend.txt). Explicit per-mode selectors corrected this delivery-tool error; the complete corrected command then passed 367+113. Earlier passing cases are not added to the final count.

One existing Starlette TestClient deprecation warning remains. Windows npm/npx launching also reports Node DEP0190 for fixed shell arguments; no user-supplied command text is passed. These warnings did not change exit status or assertions.

This new reproduction is Windows/desktop Chromium evidence. Linux prerequisites are documented but not newly executed; physical Lenovo/Pixel observations, accepted 12.3/12.4 results and the owner's published-version confirmation remain historical at their recorded revisions/routes. No field time saving, road safety benefit, live-source completeness, seven-day wall-clock soak or full accessibility conformance is asserted. [Complete requirement/test matrix](../submission/traceability.md), [supported envelope](../submission/supported-input.md), [AI/human reflection](../submission/ai-reflection.md), [open limits](../submission/known-issues.md) and [reader checklist](../submission/review-checklist.md).

The delivery is versioned Git content; no ad-hoc archive is needed. Local runtime secrets, node_modules/builds, failed-run runtime directories, databases and private archives remain outside Git. The five separately planned extensions remain outside approved V1. The isolated review environment is left healthy at **http://127.0.0.1:15325/private**; generated login is only in `D:/IBE160/tmp/submission-clean-20261028/.private-runtime/submission/account.json`.
