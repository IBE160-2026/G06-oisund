---
title: '10.1 — Review a text PDF'
type: feature
created: 2026-10-21
status: done
route: dispatch
epic: 10
story: '10.1'
alias: V1-05
story_key: 10-1-review-a-text-pdf
baseline_commit: 6fc1eb71a8d56774c1bb64a5bdaf859d3500b53d
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-10-context.md
  - D:/IBE160/Docs/evidence/9-1-import-qualification.md
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Qualified extraction is disconnected from private drafts.

**Approach:** Review a transient text-PDF interpretation, then explicitly save a separate private draft through 9.4. Show source/mapped facts, page/field uncertainty and limits.

**Owner walkthrough amendment (2026-10-21):** Jonas reported that imported mid-day vehicle-duty changes (960181 to 960176) are retained in extraction but absent from the editable plan. Preserve and edit duty changes from the affected activity onward, including derived three-digit values; never infer physical bus changes. Populate meaningful uncertainty notes and expose source issues next to affected activities and in a compact summary after adoption/reopen. Collapse PDF source facts after adoption and reopening, retaining explicit access. Keep direction enrichment deferred. This is authorized refinement during the ongoing 10.1 walkthrough, not story acceptance; preserve existing account/data and the authorized local rollout workflow.

## Boundaries & Constraints

**Always:** Reuse 9.1 extraction and 9.4 access/revision/replay, seven-day expiry and Oslo controls. Preserve order, UUIDs, field locations/origins, headers, annotations, duties and pause rows. Keep full duties/three-digit suffixes; bus starts null. Retain interpreted facts only; release originals/copies after success/failure/cancel/interruption. Clear memory on logout/expiry; protect edits.

**Never:** Use runtime oracles, fill gaps silently, claim arbitrary PDFs qualified, archive raw text/files/filenames, persist browser content, replace work, confirm/activate, implement 10.2, add OCR/live feeds, test operational data, deploy, commit or push.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Qualified layout | Examples 1–5/7 | Ordered unconfirmed review with provenance | No completeness claim |
| Partial | Example 6 Travel to | Label/end 16:00; start/places/type unresolved | No automatic owner-assisted 15:33 Skoglyst–Breivika deadhead |
| Meaning | Overnight, repeated IDs/duties, zero duration, pauses | Dates/order/zeros retained; matpause/kaffepause/deltskiftpause | Unknown stays unknown |
| Header end | Example 5 | 08:51 header versus 08:29 Sign-off | No invented free-time row |
| Invalid/bounded | Scan/type/corruption/encryption/limits/timeout/saturation | Visible failure/partial; manual entry | No silent loss/raw errors |
| Lifecycle | Cancel/disconnect/logout/interruption | Stop worker; discard late replies/bytes | Earlier work protected |
| Save/reopen | Lost reply/stale revision | Same operation/facts/metadata/deadline | No false success/duplicate/resurrection |

</frozen-after-approval>

## Code Map

- `backend/app/pdf_import.py`: `extract_pdf`, cancellation, limits, `group_pauses`; qualification stays offline.
- `backend/app/draft_storage.py`: JSONB, normalization, fingerprints, ownership; preserve legacy replay.
- `backend/app/private_main.py`: 4096-byte non-draft ceiling; CSRF/origin/no-store.
- `frontend/src/PrivateAccess.tsx`, `PrivateDrafts.tsx`: security guards, 10-second timeout, strict validation/acknowledgements.

## Tasks & Acceptance

**Execution:**
- [x] `backend/app/draft_domain.py`, new `backend/app/private_import.py` — bounded typed metadata, whitelisted headers excluding driver/employer/raw archives. Link rows to UUIDs; retain source values/duty occurrences. Unqualified calendars remain unresolved/rejected.
- [x] `backend/app/private_main.py`, `pdf_import.py` — transient raw PDF POST; incremental 10 MiB cap; authorize before parsing/revalidate before response. Retain 20-page/30-second/2 MiB-output limits; bound concurrency. Wire abort/disconnect/shutdown cleanup; no long DB locks or preview persistence.
- [x] `frontend/src/PrivateAccess.tsx`, new `frontend/src/PrivateImport.tsx`, `PrivateDrafts.tsx`, `style.css` — cancellable upload/adequate timeout; Norwegian review/error states. Release bytes after processing; show structured source facts. Guard edits before separate-draft adoption; preserve metadata across editing/reset/reopen/validation. Reuse save recovery; group pauses visually only.
- [x] `backend/app/draft_storage.py` — compatible reads/save/replay normalization; no data rewrite/migration/expiry extension.
- [x] New `backend/tests/test_private_import.py`, `backend/tests/test_private_drafts.py`, new `frontend/tests/private-import.spec.ts`, `scripts/verify-private-drafts.py` — disposable coverage of every matrix row, independent fixture mapping/save/reopen, legacy replay, access/CSRF, resource limits and interruption.
- [x] `Docs/evidence/10-1-import-review.md`, `README.md`, `Docs/development-log.md` — executed results/limits, synthetic 768/1440px renders, BMAD review and owner-walkthrough handoff. Owner acceptance remains pending.

**Acceptance Criteria:**
- Given seven fixtures, when importing/saving/reopening, then independent facts/uncertainty survive; example 6 stays partial.
- Given foreign/demo/expired access, when previewing/saving/replaying, then private reads/writes fail.
- Given cancellation/interruption, when cleanup finishes, then no workers/raw residue remain and earlier work is unchanged.
- Given 768/1440px keyboard use, when reviewing/errors occur, then labels/focus/wrapping/uncertainty remain usable.

## Implementation Notes

- Owner acceptance, 2026-10-21: Jonas explicitly approved the walkthrough of 10.1 and authorized commit/push with devlog. He accepted leaving the false t-marker warning at example 8 activity 13 (a crop fragment of right-column tom / 76567). Sprint 10.1 is done. This publication authorization supersedes earlier no-commit/no-push boundaries for 10.1 only; no next story is authorized or started. Final verification and preserved operational data are recorded in the additional-import evidence.

- Local rollout authorization and verification, 2026-10-21: Jonas explicitly requested making implemented 10.1 available in the local app while preserving his existing account/data. This supersedes the frozen no-deploy boundary only for this requested local rollout; no commit/push is authorized. Built private API and frontend, then used explicit project names and `up -d --no-deps --wait` for those services only. Read-only in-memory checksums before/after matched for accounts, drafts, operations, deletion acknowledgements, sessions, security settings and migration history (1 account, 0 drafts). Database container, named volume and secret mount remained identical. Local page/assets returned HTTP200, private health was ok, and the live API contains POST /imports/pdf. No operational import/save tests or private payload inspection; owner browser walkthrough remains pending.

- Final root verification, 2026-10-21: inspected the review corrections and updated synthetic renders; full guarded disposable verifier passed 148 backend tests (102.15s), actual PostgreSQL/API restart and exact state/deadline preservation, production build and all 65 browser tests (2.6m). Separate fictional backend regressions passed 18 tests (1.07s); mocked verifier controls passed 2 tests (0.140s). All retained review findings patched; none deferred. Root confirmed disposable services stopped and existing operational API/database healthy. Restored only regenerated prior-story screenshots. No product change after final verification. Spec done denotes implementation; sprint remains review awaiting owner walkthrough/acceptance. Approved no-deploy/no-commit/no-push boundary supersedes the workflow's default local commit.

- Root audit: product and test diff read; synthetic 768/1440/error renders inspected. Matrix coverage passed: qualified/partial/meaning/header = independent seven-fixture mapping plus all-seven API save/reopen; invalid/bounded = adapter rejection/output/timeout tests and admission checks; lifecycle = real-child disconnect/task/shutdown and browser cancel/logout; save/reopen = replay/conflict/expiry suites, browser lost-response recovery and actual restart equality. Final executed results: 143 backend tests, latest focused import 8 tests, verifier controls 2 tests, browser 59 tests and production build. Independent review and owner acceptance pending.

- 2026-10-21: Jonas approved the specification with "Godkjenn og fortsett". Re-read from disk; no external edits. Approved intent is frozen.

## Spec Change Log

- Additional fixture baseline, 2026-10-21: Jonas added anonymized examples 8 and 9 during testing/owner walkthrough of 10.1. The [fasit extension](../../Eksempelfiler/README.md) independently records 23 and eight source rows, respectively. Example 8 covers 960181 → 960176, CAR - 1 / CAR / 76566 (owner-clarified pilot-car handover, followed by pilot-car return on deadhead 76567; CAR - 1 through CAR - 4 may occur), repeated Wi-To endpoints and a second notes-only page. Example 9 has Fadder/Instruktør plus Coffee, no trips/duty and no final Sign-off. Preserve source codes/rows; no invented bus, ordinary duty suffix for CAR or mentor-role functionality. The previous seven-fixture results and approval do not qualify these additions. Jonas approved the example 8–9 fasit on 2026-10-21; see the [dated fixture handoff](../../docs/evidence/10-1-additional-fixtures.md). No new extraction execution or acceptance of the story implementation is implied.

- Owner walkthrough refinement, 2026-10-21: added optional activity-ID-anchored vehicle duty changes with derived suffixes, import mapping and editable per-activity inheritance. Explicit empty overrides survive save/reopen; legacy records omit the new field and derive UI boundaries from immutable source metadata without rewriting storage. Added readable uncertainty notes/marker attribution and a persistent issue summary with activity navigation; source facts collapse on adoption/reopen. Direction enrichment remains deferred. Full disposable backend verification passed 151 tests (112.25s), real restart/migration/state/deadline checks and production build. The first browser run passed 66 and caught an accessible-label regression caused by help text inside a label; fixed explicit field naming/description, then final production build and all 67 browser tests passed (3.4m). Root read the amendment diff and inspected the synthetic amended-editor render. The synthetic 960181-to-960176 scenario and all seven approved fixtures were tested; the owner's additional private PDF was not read or used as a repository fixture. No product changes after final tests.
- Applied the verified amendment to the already-authorized local app. Existing database container/volume/secret remained; read-only checksums before/after matched accounts, drafts, operations, deletion acknowledgements, sessions, security settings and migration history (1 account, 0 drafts). Page200 and served duty/uncertainty/collapsed-source controls checked; API healthy and disposable services stopped. No migration, commit/push or acceptance. Story remains sprint review for continued owner walkthrough.

## Review Triage Log

| Finding | Verdict / route | Evidence |
|---|---|---|
| Blind 1: CSRF rotation outside lock | medium / patch | Upload fetches a rotating signed double-submit proof outside the existing mutation Web Lock; another tab can replace its cookie. Use the same lock and cancellation guard. |
| Blind 2: omitted adapter source_rows | false / reject | The retained source activities preserve all qualified activity rows and field locations; independent fixtures compare all 113. Adapter source_rows additionally contains intermediate stop fragments; intermediate-stop completeness is explicitly unqualified, and raw evidence archives are excluded. No qualified source activity is dropped. |
| Blind 3: invisible header provenance | medium / patch | Header field locations are stored but SourceFacts renders only their values. Display their existing source references. |
| Blind 4: invisible calendar derivations | medium / patch | SourceFacts filters derivation objects from per-field provenance. Show stored field-specific source links/rules in readable form. |
| Blind 5: repeated cancellation releases admission early | medium / patch | A second cancellation can interrupt shielded cleanup, be suppressed, and release tracking before the worker finishes. Keep awaiting worker completion before releasing its slot/event. |
| Blind 6: stalled upload shutdown delay | low / reject | A stream waiting for a chunk sees shutdown only on progress or its fixed 30-second deadline. This bounded delay during rare local shutdown is negligible; additional upload-task orchestration adds branches. Normal disconnect/request cancellation already closes the stream. |
| Blind 7: metadata cross-reference validation | low / reject | Forged API metadata can reference source positions outside its own list; generated metadata cannot. Source UUIDs intentionally survive manual row removal. Current consumers only display source metadata; extra guards for manually forged metadata add complexity outside everyday use. |
| Blind 8: omitted unknown code/column/line | medium / patch | Unknown uncertainty codes lose their identity and available column/line in presentation. Display existing code and full location. |
| Blind 9: hidden/expired pending-import coverage | medium / patch | Browser tests exercise cancel/logout but not hide/revalidation or session expiry with delayed replies. Add focused coverage for existing guards. |
| Blind 10: slow/concurrent upload coverage | medium / patch | Upload tests yield immediately and manually acquire slots; add stalled deadline and overlapping-request recovery tests. Shared root cause with Verification 1. |
| Blind 11: checklist claims review/walkthrough complete | low / reject | Evidence explicitly records pending owner checkpoints. The checklist wording is ambiguous, but the proposed fix edits this build spec; rejected under the review workflow's explicit spec-edit rule. Owner acceptance remains pending. |
| Verification 1: slow-upload deadline/recovery | medium / patch | Pre-verified: deleting the upload timeout leaves every existing test passing. Test 408, no extraction, slot/event cleanup and subsequent admission. |
| Verification 2: unresolved browser presentation | medium / patch | Pre-verified: synthetic browser fixture has no partial Travel to. Test known 16:00 end and unknown start/places/type before adoption and after save/reopen. |

Edge-case layer returned no findings. All three layers ran; no deferred finding.

All patch entries were implemented and passed targeted tests followed by the final full verifier. Added coverage includes real overlapping admission, stalled-upload 408 and recovery, repeated cancellation, visible provenance/derivations, unknown-code locations, delayed hide/expiry, CSRF lock ownership, prompt logout and partial Travel to save/reopen. The first targeted partial browser assertion expected minute precision; corrected its test expectation to the existing explicit seconds representation, then the complete final 65-test suite passed.

## Design Notes

No intent gaps. Cross-layer dispatch; no migration/deployment. 9.4/Epic 9 are owner-approved done; no same-epic predecessor. Story 10.1 is in sprint review pending owner walkthrough/acceptance; Epic 10 remains in progress.

## Verification

Extend guarded disposable verification with read-only fixtures: private API/PostgreSQL/browser suites, restart/reopen, adapter/fictional regressions. Run `npm.cmd run build`, `git diff --check`; inspect renders/cleanup. No application tests or operational mutations during planning.
