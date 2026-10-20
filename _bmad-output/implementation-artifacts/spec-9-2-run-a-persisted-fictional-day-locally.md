---
title: '9.2 — Run a persisted fictional day locally'
type: feature
created: 2026-10-19
status: done
route: dispatch
epic: 9
story: '9.2'
alias: V1-02
story_key: 9-2-run-a-persisted-fictional-day-locally
baseline_commit: f53f17b59c58bbf2bdd04fe505eb84e336393316
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-9-context.md
---

<frozen-after-approval reason="Owner authorized preparing and implementing one story without intermediate approval in the 2026-10-19 request">

## Intent

**Problem:** The repository contains approved SCOPE-02 plans but no executable application. The assessor needs a real local frontend/API/PostgreSQL flow with fictional data and repeatable setup.

**Approach:** Implement V1-02 / 9.2 as the first available independent slice. V1-01 cannot run because representative PDFs and independent expected data are absent; the active backlog explicitly permits this fallback. Save and reopen one fictional working day through React and FastAPI into PostgreSQL and demonstrate survival across service restart.

## Boundaries & Constraints

**Always:** React/TypeScript, Python/FastAPI and real PostgreSQL; loopback-published endpoints; exclusively fictional assessment runtime and storage; visible Norwegian fictional-data label; validated typed records, UUIDs, server-assigned fictional owner, explicit service/calendar dates and unknown facts; no-store responses; stable creation operation ID and replay handling; fixed seven-day retention for introduced draft records. Seed/reset must target fictional storage only. Pin verified executable dependency versions and document migrations, seed, tests, restart and teardown.

**Never:** Accept private/operational input in this no-login slice, expose private APIs or claim private access is implemented. Do not implement login (9.3), general draft editing/revision UI (9.4), PDF, confirmation/navigation/notices or deferred GPS/offline/cloud features. Do not substitute SQLite or static mock data for database verification. No commit or push. If this spec misses required implementation detail, resolve it within current contracts and record the choice; stop for a genuine product contradiction.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Save/reopen | Fixed fictional day; explicit save then reload | API validates and saves PostgreSQL record; same values return | Saved state only after valid acknowledged response |
| Repeated save | Same operation and same fictional payload | Same stable record, no duplicate | Changed payload for same operation returns conflict |
| Invalid request | Unsupported fields, malformed dates, non-fictional payload | No database mutation | Typed 422 or denial |
| API unavailable | Database/API stopped during save or load | Visible unavailable/unconfirmed status; no false saved claim | Retry remains explicit |
| Restart | Saved fictional day, services restarted | Previously acknowledged day reopens unchanged | Database health failure is visible |
| Isolation/reset | Fictional reset requested | Only this isolated assessment store is reset and reseeded | Non-assessment runtime refuses startup/reset |
| Expiry | Introduced record past fixed deadline | Read/retry denied; cleanup removes related state | No resurrection on old operation replay |

</frozen-after-approval>

## Code Map

- `../planning-artifacts/epics.md` and `../planning-artifacts/story-drafts/story-v1-02.md` — canonical story and planning copy; preserve acceptance and backlog history.
- `epic-9-context.md` — current architecture, UX and scope constraints; historical mockups are not executable requirements.
- `../../README.md`, `../../.gitignore`, `../../Docs/development-log.md` — existing handoff, ignore rules and append-only development evidence.
- No application or package manifests exist. Docker Desktop 29.7.2 and Node 24.19.0 are installed; Desktop was stopped and has been started. Use `npm.cmd` on PowerShell because npm.ps1 execution is disabled. Sandbox denies uv; use approved escalation when required.

## Tasks & Acceptance

**Execution:**
- [x] `../../compose.yaml`, container definitions and lockfiles — implement loopback-only reproducible assessment runtime with health checks and persistent PostgreSQL volume.
- [x] `../../backend/` — implement validated fictional-day create/read boundary, idempotent creation, migrations, deterministic seed/reset and expiry; reject non-assessment configuration.
- [x] `../../frontend/` — implement Norwegian fictional-day save/reopen UI and honest failure states with labelled keyboard-accessible controls.
- [x] `../../backend/tests/` and `../../scripts/` — verify matrix cases against actual PostgreSQL/API and provide repeatable restart/persistence verification; add browser verification where practical.
- [x] `../../README.md` — document exact start, migration, seed/reset, local URL, tests, persistence check, teardown, versions and scope limitations.
- [x] This spec, sprint tracking and `../../Docs/development-log.md` — record actual results and limitations; leave other stories unchanged.

**Acceptance Criteria:**
- Given a local Docker installation, when documented setup is executed, then the React frontend and actual FastAPI/PostgreSQL flow run without paid accounts, live feeds or private data.
- Given the fictional day displayed in the frontend, when saved and reopened, then persisted values equal the known input and survive backend/database service restart.
- Given introduced controls and errors, when used by keyboard or on PC/tablet width, then labels, focus, readable wrapping and fictional/planned/unknown distinctions remain visible.
- Given executed checks, when handing off, then commands, versions, failures and limitations are recorded truthfully and the status does not claim unperformed acceptance.

## Implementation Notes

Plan prepared under the owner's explicit authorization to prepare and implement this one story without intermediate approval. No unresolved product questions. Initial migration affects only new isolated fictional storage. Runtime tooling and dependency downloads require ordinary environment permissions.

## Spec Change Log

- 2026-10-19: Implemented the bounded fictional-only slice. Server issues an operation UUID before first save; unused operations expire after seven days. First successful day creation fixes both record/operation deadlines at server creation plus exactly seven days. Unknown purged operation IDs are denied, preventing replay resurrection without retaining tombstones. Only the canonical fixed payload is accepted. Seed/reset repeat the same fixture values, with server-generated identities/timestamps.
- Resolved actual package/image registry versions and pinned image digests/full dependency versions. Initial older pins were replaced before final checks. No product scope or frozen acceptance text changed.

## Review Triage Log

| Finding | Verdict | Evidence and route |
|---|---|---|
| Blind 1: database URI overrides | high | storage.py validates parsed path/host but passes the original query to libpq, which supports overriding dbname/host/user. Patch rejects override-bearing URIs before connecting. |
| Blind 2: bootstrap credentials | medium | POSTGRES_USER creates a cluster superuser. Cluster is exclusively fictional and isolated; the README database-exclusive privilege claim is false. Patch corrects that claim; no private data may share this cluster. |
| Blind 3: acknowledgement deadlines | medium | validSaved only checks parseability, accepting reversed/already-expired deadlines. Patch validates deadline order, exact introduced lifetime and expiry. |
| Blind 4: reopen identity | medium | reopen assigns any valid-looking returned ID without comparing the requested ID. Patch enforces equality and adds a regression. |
| Blind 5: coerced fictional flag | low | Pydantic Literal True accepts numeric 1 before canonical comparison. Direct input-type correction and real API regression. |
| Blind 6: committed response loss | medium | Existing browser abort prevents the first request reaching PostgreSQL. Patch forwards commit then drops acknowledgement and checks retry identity. |
| Blind 7: migration runner | low | Only initial version exists and rerunning its idempotent SQL is valid for every schema this implementation creates. Incompatible externally created tables and future migrations are not current callers. Reject added migration machinery for this hypothetical state; later schema changes must add ordered migrations. |
| Blind 8: hidden cleanup failure | maybe-false | SELECT 1 would not detect a permission-specific DELETE failure, but current dedicated bootstrap owner is superuser and no code revokes grants or drops tables. Both calls fail for actual exercised database outage. No reachable independent purge failure established; a live denied-DELETE/healthy-read case would settle it. Reject low-impact hypothetical instrumentation here. |
| Blind 9: script timeout | low | Invoke-RestMethod/WebRequest without TimeoutSec may wait indefinitely on a stalled response. Direct patch bounds all calls. |
| Blind 10: expired presentation | medium | 410 only changes message; saved footer/day persist and elapsed expiry has no UI transition. Patch clears known-expired saved presentation with browser regression. |
| Edge 1: database URI overrides | high | Same effective libpq override reproduced by independent tracing; patch with Blind 1. |
| Verification 1: retry identity gap | medium | Pre-verified: changing browser retry to a new operation would pass existing pre-commit-abort test and duplicate a committed save. Patch with Blind 6. |
| Verification 2: date rendering gap | medium | Pre-verified: UTC display would pass existing tests while losing overnight dates. Patch adds exact Oslo/calendar assertions before and after reload. |

## Verification

- `docker compose config` — valid loopback-only fictional configuration.
- Documented build/start, migration and seed commands — successful real database initialization.
- `docker compose exec -T api python -m pytest -q` — 12 passed against actual HTTP/PostgreSQL (0.85s), including concurrency, validation, no mutation, isolation and expiry/purge/replay denial.
- `scripts/verify-persistence.ps1` — actual DB/API restart retained the entire acknowledged record `5b874fbc-6c61-403e-bf4d-c569375e8842` and identical retry identity.
- `scripts/verify-unavailable.ps1` — actual DB stop returned 503; explicit retry recovered. Stopped API could not return a day; all services restored healthy.
- Frontend production build/typecheck passed with TypeScript 7.0.2/Vite 8.3.4. `npx.cmd playwright test` — 4 passed in 4.1s using installed headless Edge: keyboard save/reload at 1440/768px, no horizontal overflow, visible focus, failed fetch/retry/reopen, HTML/malformed acknowledgement rejection. Screenshots: `Docs/evidence/9-2-1440.png` and `9-2-768.png`.
- `npm ci` audit — zero vulnerabilities; `pip check` — no broken requirements. Initial Vite audit finding was resolved by upgrading; initial CSS-module type error was corrected before final successful build.
- `git diff --check` — no whitespace errors.

Limitations: browser connector had no available browser surface; development browser automation used installed Edge instead. Actual tablet hardware, assistive technology and exhaustive accessibility testing are not claimed. Current completion status is recorded in the closure entry below; earlier verification and handoff entries retain their dated historical meaning.



### Final root verification and completion — 2026-10-19

- All three independent review layers completed. Thirteen individual findings were triaged above; direct corrections are verified. No retained blocker or deferred implementation item for this story. The initial migration remains intentionally limited to version 1; future schema changes require ordered pending migrations. Cleanup-specific failure without database-health failure was not established in this dedicated superuser cluster.
- Root read the complete application sources, migration, Compose configuration, tests and both verification scripts, inspected the diff and both rendered screenshots. No git staging, commit or push occurred.
- Final `docker compose config --quiet`: passed. Final `docker compose exec -T api python -m pytest -q`: **18 passed in 0.90s**. Final `npm.cmd run build`: production build and typecheck passed. Final `npx.cmd playwright test`: **13 passed in 6.7s**.
- Final `scripts/verify-persistence.ps1`: passed after real DB/API restart with identical saved record `8caae39b-59a6-449e-982c-3d596e976579` and replay identity. Final `scripts/verify-unavailable.ps1`: passed real database-down 503, deliberate retry, API stop and complete recovery.
- Matrix audit: save/reopen, replay/concurrency, invalid requests, isolated configuration/reset and expiry have passing PostgreSQL/HTTP tests; lost committed acknowledgement and valid retry have passing browser tests; outage/restart have passing real-service scripts; browser tests cover 410 and elapsed expiry, identity/lifetime rejection and explicit overnight rendering at the two tested widths.
- Two targeted browser checks briefly collided with root's deliberate API outage. Root then serialized the service checks and reran the entire browser suite successfully; no failed or skipped case remains in the final run.
- Spec is done. Sprint story remains review per build's terminal synchronization rule, with epic 9 in-progress and every other story backlog. Missing anonymized PDFs/fasit keep 9.1 unstarted; the approved independent 9.2 fallback was used. Actual tablet hardware/comprehensive accessibility qualification remain outside this slice's evidence. No next story was started.

### Owner closure and status reconciliation — 2026-10-20

- The owner reported successful local use on 19 October and requested reconciliation to completed status on 20 October. All acceptance tasks are checked; the final 18 API/PostgreSQL tests, 13 browser tests, production build/typecheck, actual restart/outage checks and independent review are recorded above. No blocking implementation finding remains for this slice.
- Both this implementation spec and sprint story 9.2 are now done. Epic 9 remains in-progress; every other story remains backlog. The approved planning copy retains its original scope/acceptance definition; implementation evidence and live status are held here and in sprint tracking.
- Implementation was committed and pushed on 19 October as `040170eed4e043ecb899e39547270e0de6acf82a`. This closure changes documentation/tracking only; it does not rerun application tests, start another story, commit or push. PDF fixtures/fasit and later device/accessibility qualification remain separate outstanding work.
