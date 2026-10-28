---
title: '12.5 Deliver a reproducible submission (V1-20)'
type: chore
created: '2026-10-28'
status: in-progress
route: dispatch
baseline_commit: 99c272b09abaa5ffecf3286b406fbf065a445c7c
review_loop_iteration: 0
owner_acceptance: pending
context: []
---

<frozen-after-approval reason="User explicitly authorized autonomous completion through review; product contract changes still require clarification">

## Intent

**Problem:** README mixes historical checkpoints and cannot establish that an independent reader can reproduce the accepted V1 without the owner's environment.

**Approach:** Deliver a coherent main recipe, isolated real React/FastAPI/PostgreSQL demonstration, synthetic fixtures, precise requirements/test links, executed clean-environment evidence and a factual AI-process reflection. Authority: Story 12.5 in `../planning-artifacts/epics.md` and `../planning-artifacts/story-drafts/story-v1-20.md`; FR-25, NFR-4, AC-11/12 and SCOPE-02. Stories 12.1–12.4 are accepted dependencies; this story remains pending owner review.

## Boundaries & Constraints

**Always:** Work only in `D:/IBE160/tmp/story-12-5`, branch `story/12-5-reproducible-submission` from freshly fetched main. Use dedicated loopback ports, explicit Compose project and new named database volumes. Generate ignored local synthetic secrets and account. Preserve the synthetic-only test guard and reserved-account CLI protection. Use only versioned content and freshly installed dependencies/builds for reproduction. Separate setup/download network requirements from runtime. Document migrations, initialization/seed, PDF import, optional correction, explicit save, confirmation, use, reopening, tests, stop/restart, fixed retention and isolated reset. Record actual commands, full source revision and dirty-source hashes where applicable, environment, expected/observed outcomes, failures and reruns. Distinguish parser, integration, UI, physical and unperformed field-benefit evidence. Reuse historical evidence with its original revision/limits.

**Never:** Stop/change existing services, tunnels, ports, accounts (including jonas), passwords or databases; inspect/copy private runtime or backups; reset shared data; weaken guards; infer owner acceptance; merge/deploy/submit to learning platform; close Epic12 or start any of the five planned extensions. Clarify before any required product-contract change. No private PDFs, secrets, tokens, database dumps or local archives in Git/package. Prefer versioned Git checkout as delivery; if packaging, inspect exact allowlisted contents. User authorizes final code/documentation/evidence commit and branch push; session log must have its own path-limited commit.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Clean setup | Versioned checkout, no node_modules/build/runtime/DB | Generate secrets, install/build, start actual API/PostgreSQL/frontend, migrate, synthetic seed/account, follow README | Clear prerequisites and nonzero failures |
| Repeat init/restart | Existing isolated demo data | Initialization is idempotent; acknowledged state and deadlines survive API/DB/container restart | No silent reseeding or renewal |
| Reset | Isolated demo with saved data plus unrelated environment | Only demonstration data reset; unrelated containers/volumes preserved | Refuse wrong project/config/storage and non-synthetic accounts before mutation |
| Supported PDF | Synthetic A–E and independent JSON facts | Import transiently, inspect/correct, explicitly save/confirm/use/reopen through actual API/PostgreSQL | Unknown fields stay unknown; unsupported input offers manual entry |
| Verification | Relevant automated suites against synthetic database | Honest executed result with source/environment and limitations | Preserve failures; don't relabel historical runs |

</frozen-after-approval>

## Code Map

- `../../README.md` — replace contradictory status accumulation with current delivery recipe; preserve history in linked reports.
- `../../compose.private.yaml`, `../../compose.story124.yaml` — established private-db/private-api configuration; new standalone submission Compose must use its own project, ports and volume, no operational overlays.
- `../../backend/app/private_storage.py` — exact private_work role/database and private-db host; migrate 001–014; startup/hourly retention cleanup.
- `../../backend/app/auth.py` — provision and require_synthetic_accounts; `app.manage provision` intentionally rejects synthetic namespace; do not change it.
- `../../backend/tests/test_private_access.py` and private suites — actual HTTP/PostgreSQL with existing synthetic guard; test marker remains ibe160-private-tests even for isolated project.
- `../../deploy/tablet/Dockerfile`, `../../frontend/vite.config.ts` — existing pinned build tooling; use a dedicated local frontend build and proxy or explicit local API settings.
- `../../frontend/tests/complete-user-flow.spec.ts`, `private-activity-helpers.ts` — reusable import/save/confirm/start/outcome/reopen assertions; never point historical hardcoded defaults at ordinary databases.
- `../../Eksempelfiler/Testskift-A.pdf` through E and `Fasit-testskift.json` — fully synthetic fixtures with independently authored expected facts; historical anonymized originals are not setup prerequisites.
- `../../docs/evidence/12-4-handoff.md`, `12-4-import-experience.md`, `12-4-main-integration.md`, `../../docs/tablet-production.md` — accepted history and protected operational environment.
- `../../.logs/jonas-oisund/issues.md`, `../../docs/development-log.md` — open limitations and factual human/AI process history.

## Tasks & Acceptance

**Execution:**
- [ ] `../../compose.submission.yaml`, `../../deploy/submission/`, `../../scripts/submission*` — provide bounded generated-secret setup, idempotent initialization, isolated seed/reset, health/start/stop/restart/test commands; no existing runtime dependencies.
- [ ] `../../README.md` — coherent clean-checkout recipe with commands, addresses, expected outcomes, actual demo journey and network needs; link preserved historical reports.
- [ ] `../../docs/submission/` — entry index, precise requirement-to-test traceability, supported input/limits, actual AI/human reflection, known issues and review checklist.
- [ ] `../../docs/evidence/12-5-*` — execute README from a separate clean versioned checkout, fresh dependencies and dedicated projects/volumes; record setup, UI/fullstack journey, migration/seed idempotence, restart/deadlines, reset isolation and safety-negative tests, failures and reruns.
- [ ] `sprint-status.yaml` and this spec — mark review ready only after verification; keep Epic12 in progress and acceptance pending.

**Acceptance Criteria:**
- Given only the versioned delivery and documented tools/network for installation, when a reader follows README, then the full local real API/PostgreSQL demonstration works without owner data/accounts/tunnel/paid services/live feeds.
- Given saved synthetic state, when stopping/restarting and rereading, then data and fixed deadlines remain unchanged; when resetting, then only isolated demo data changes and wrong-target/non-synthetic cases fail before mutation.
- Given the evidence entry, when reviewing FR-25/NFR-4/AC-11/12, then exact tests/results/source versions and limitations are reachable and simulation is distinct from actual integration and unperformed field benefit.

## Implementation Notes

Intent gaps: none after repository investigation. Irreversibles: authorized branch publication only; reset limited to explicitly disposable synthetic data. Footprint: delivery tooling/docs/tests; no product-contract changes planned. User's autonomous completion instruction supersedes intermediate plan approval.

## Spec Change Log

## Review Triage Log

## Verification

- Follow the new README exactly in a clean tracked-only clone/export; use no prior dependencies, built files or runtime volumes.
- Run relevant actual backend integration tests, bounded real-browser journey and reset/refusal/persistence controls. Record commands and exits instead of inventing counts.
- Inspect final tracked/staged file list and diff; keep private state ignored. Root independently reviews the diff and test results before final commits/push.
