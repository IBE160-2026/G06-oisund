---
title: '12.5 Deliver a reproducible submission (V1-20)'
type: chore
created: '2026-10-28'
status: done
route: dispatch
baseline_commit: 99c272b09abaa5ffecf3286b406fbf065a445c7c
review_loop_iteration: 0
owner_acceptance: accepted
accepted_on: '2026-10-28'
context: []
---

**Current decision:** Jonas explicitly accepted Story12.5 in full on28October2026 after all ten guided assessment parts. [Acceptance record](../../docs/evidence/12-5-owner-acceptance-2026-10-28.md). The frozen starting intent and earlier review notes retain historical pending wording; current status is done/accepted. Epic12 remains in progress by explicit instruction.

<frozen-after-approval reason="User explicitly authorized autonomous completion through review; product contract changes still require clarification">

## Intent

> Historical tracking checkpoint before C1 acceptance/final closure (see current V1 closeout):
> Owner clarification,29October2026: the prior Epic12 done publication was a misunderstanding; only Story12.5 was to be marked done. All accepted story results and the completed retrospective remain unchanged. Epic12 stays open pending the closure basis and owner decisions.

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
- [x] `../../compose.submission.yaml`, `../../deploy/submission/`, `../../scripts/submission*` — provide bounded generated-secret setup, idempotent initialization, isolated seed/reset, health/start/stop/restart/test commands; no existing runtime dependencies.
- [x] `../../README.md` — coherent clean-checkout recipe with commands, addresses, expected outcomes, actual demo journey and network needs; link preserved historical reports.
- [x] `../../docs/submission/` — entry index, precise requirement-to-test traceability, supported input/limits, actual AI/human reflection, known issues and review checklist.
- [x] `../../docs/evidence/12-5-*` — execute README from a separate clean versioned checkout, fresh dependencies and dedicated projects/volumes; record setup, UI/fullstack journey, migration/seed idempotence, restart/deadlines, reset isolation and safety-negative tests, failures and reruns.
- [x] `sprint-status.yaml` and this spec — mark review ready only after verification; keep Epic12 in progress and acceptance pending.

**Acceptance Criteria:**
- Given only the versioned delivery and documented tools/network for installation, when a reader follows README, then the full local real API/PostgreSQL demonstration works without owner data/accounts/tunnel/paid services/live feeds.
- Given saved synthetic state, when stopping/restarting and rereading, then data and fixed deadlines remain unchanged; when resetting, then only isolated demo data changes and wrong-target/non-synthetic cases fail before mutation.
- Given the evidence entry, when reviewing FR-25/NFR-4/AC-11/12, then exact tests/results/source versions and limitations are reachable and simulation is distinct from actual integration and unperformed field benefit.

## Implementation Notes

Intent gaps: none after repository investigation. Irreversibles: authorized branch publication only; reset limited to explicitly disposable synthetic data. Footprint: delivery tooling/docs/tests; no product-contract changes planned. User's autonomous completion instruction supersedes intermediate plan approval.

Clean reproduction completed with actual API/PostgreSQL, 480 selected backend/parser cases, 3 real-browser cases, 3 Node and 3 wrapper checks; exact row/deadline stop/start/restart and guarded reset passed. Source product/dependency files remain identical to baseline. See ../../docs/evidence/12-5-reproduction.md for canonical revisions, failures and limits. Independent review follows; owner acceptance remains pending.

Post-review source8d50684338b4f74430cd387dabba9e55edc4b7fd passed6 Node groups on Windows and Linux,3 actual browser cases,6 actual database safety cases and the expanded5-check populated lifecycle/reset probe (30 unrelated containers/14 volumes preserved). Two missing-audit-input controls passed. Exact receipts and remaining sequential-bootstrap boundaries are in the reproduction report.

## Spec Change Log

## Review Triage Log

Focused reinspection by the three original reviewers closed all retained findings after patches and affected reruns. B6/E2 remain rejected low unsupported-use boundaries, explicitly documented. README pins c067fdbb20150219c041588ed4e990e7b0ef6b94; the clean copy checked out that immutable snapshot and passed current status guards. User review/acceptance remains pending.

| Finding | Verdict | Verified evidence / route |
|---|---|---|
| Blind B1: Linux paths differing only in case pass ownership | medium | Original normalization lowercased all platforms. Patch native path comparison; Windows and Linux regression branches. |
| Blind B2: status omits frontend/health | medium | Original loop inspected four services and no health. Patch exact five-service healthy runtime checks; negative missing/unhealthy frontend cases. |
| Blind B3: HTTP test target may diverge from guarded SQL | medium | Original desired/live validators omitted PRIVATE_TEST_API/ORIGIN. Patch both configured and running environment checks before tests. |
| Blind B4: actual published ports are unchecked | medium | Original live validator checked networks/storage only. Patch actual Docker port bindings and database no-publication checks. |
| Blind B5: configured database mount target unchecked | medium | Original validator checked mount source/type but not destination. Patch exact PostgreSQL data target and negative test. |
| Blind B6: retained volume ownership after all containers removed | low | Requires reusing/copied runtime secrets in another checkout, outside the clean recipe explicitly requested. Reject complex persistent ownership registry; document original-checkout/secrets boundary. Existing containers and fresh checkouts remain guarded. |
| Blind B7: all-table restart probe has empty dependent tables | medium | Initial probe populated draft/session; UI A separately proved populated recap restart. Patch representative API-created bus/selection/start/outcome/closure/notice/receipts before all-table comparison. |
| Blind B8: unrelated volume inventory absent | medium | Initial probe compared container metadata only. Patch volume creation identities and container-volume mount relationships around reset. |
| Blind B9: audit may pass with zero secret inputs | medium | Initial one-off method silently skipped absent hardcoded directories. Patch mandatory explicit synthetic-runtime directories and missing-input refusal. |
| Blind B10: mutable branch clone lacks immutable checkout | medium | Branch is mutable and printing HEAD alone does not select delivered source. Patch README to pin the final reviewed source/evidence commit after checks; no tag or deployment required. |
| Edge E1: same Linux case collision | medium | Same verified cause as B1; carried into the native-path patch and Linux test. |
| Edge E2: concurrent first initialization before containers exist | low | Concurrent bootstrap is outside the sequential reader recipe and was not exercised. Reject a new global lock/recovery protocol as disproportionate for this bounded delivery; document sequential lifecycle use. No original production project shares this new project name. |
| Gap G1: whole-command ordinary-account refusal does not cover fictional DB | medium | Direct Python negative test could miss reordered Node reset calls. Patch actual Node command refusal and exact unchanged fingerprints of both databases, then remove only temporary guard rows. |

## Verification

- Follow the new README exactly in a clean tracked-only clone/export; use no prior dependencies, built files or runtime volumes.
- Run relevant actual backend integration tests, bounded real-browser journey and reset/refusal/persistence controls. Record commands and exits instead of inventing counts.
- Inspect final tracked/staged file list and diff; keep private state ignored. Root independently reviews the diff and test results before final commits/push.
