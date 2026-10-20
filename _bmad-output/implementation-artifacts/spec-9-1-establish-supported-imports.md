---
title: '9.1 — Establish supported imports'
type: feature
created: 2026-10-20
status: done
route: dispatch
epic: 9
story: '9.1'
alias: V1-01
story_key: 9-1-establish-supported-imports
baseline_commit: e8c0cf22ea8016e63da6aa0dd1e981fd61db1273
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-9-context.md
  - D:/IBE160/Eksempelfiler/README.md
---

<frozen-after-approval reason="human-owned intent — approved by Jonas on 2026-10-20">

## Intent

**Problem:** Approved fixtures have no executed extraction evidence (V1-01; FR-2, NFR-2, AC-01).

**Approach:** Qualify all seven PDFs against the independent 2026-10-20 fasit. Stop within four hours of experiment work with elapsed time, tested subset, classifications, failures and a recommendation, including negative results.

## Boundaries & Constraints

**Always:** Preserve source order, labels, page/field provenance, unknowns, identifiers, service date and explicit Europe/Oslo calendar instants. Compare header facts, activity types/times/trips/endpoints and duty occurrences. Keep full duty and three-digit suffix; actual bus stays null. Separate extracted, derived, owner-clarified and unresolved facts. Preserve rows when grouping pauses. Parser cannot read the oracle or substitute fixture-specific answers. Preserve historical weekday text despite fictional dates.

**Never:** Credit manual completion as extraction; invent gap activities; infer dates solely from clock ordering; generalize example 6 Travel to. No API/UI/database changes, private input, OCR, realtime integration, deferred features, commit or push. Do not change the fasit to fit results.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Qualification | Seven PDFs/ten pages | Field comparisons and classifications | Mismatches fail; untested remains untested |
| Continuations | Columns/pages/repeated headers | One shift; zero-minute trip, repeated IDs, X-lines retained | Flag ambiguity |
| Overnight | Example 4 | Jan 5 service date; trip 6072 ends Jan 6 | Flag unproven dates |
| Owner facts | Examples 5/6 | Paid end 08:51 distinct from Sign-off 08:29; Travel to label/unknown trip ID | Attribute free time/deadhead to owner; expose extraction gaps |
| Pauses/duties | All examples | Rows retained; meal/coffee/split grouping; 006/090 | No invented places/waits/bus |
| Invalid input | Wrong type, corrupt/encrypted/image-only, excessive size/pages, timeout/cancel | Explicit rejection/unsupported; resource cleanup | No raw logs/residue/false pass |

</frozen-after-approval>

## Code Map

- `backend/app/domain.py`: fictional-only model rejects zero-duration rows; use separate contract.
- `backend/app/main.py`, `storage.py`, `migrations/001_initial.sql`: fictional HTTP/PostgreSQL slice; keep unchanged.
- `backend/requirements.in`, `requirements.lock`, `Dockerfile`: pin qualified pdfplumber dependencies; read-only fixture mount, no originals in images.
- `Eksempelfiler/README.md`: 113 rows, 46 trips, 31 deadheads including owner-clarified Travel to. Intermediate stops unqualified.

## Tasks & Acceptance

**Execution:**
- [x] `backend/tests/fixtures/import_expected.json` — transcribe README before extraction; record approval/hashes/provenance; reconcile rows 33/16/6/16/5/16/21.
- [x] `backend/requirements.in`, `backend/requirements.lock` — verify pdfplumber using primary docs/execution; pin dependencies.
- [x] `backend/app/pdf_import.py` — implement adapter/separate contract; inspect PDF content; cap at 10 MiB, 20 pages and 30 seconds/document in a terminable worker with bounded output. Process in memory; close resources on success/error/cancel.
- [x] `backend/app/qualify_imports.py` — implement CLI/comparison. Supported requires zero required source-fact mismatches or unresolved fields; partial means usable incomplete extraction; unsupported means no reliable structure. Separate owner assistance; it cannot pass automatic completeness.
- [x] `backend/tests/test_pdf_import.py` — test matrix, oracle integrity/counts, resource/cancellation behavior and deliberate missing/changed facts.
- [x] `Docs/evidence/9-1-import-qualification.json`, `Docs/evidence/9-1-import-qualification.md` — record commands/versions/hashes/timing, per-fixture status, failures and recommendation; no raw archives. Failed useful envelope requires an explicit scope decision.
- [x] `README.md`, `Docs/development-log.md` — document reproducible commands, limits and downstream handoff; synchronize only this story using the build workflow.

**Acceptance Criteria:**
- Given the baseline, when qualification runs, then tested fixtures have traceable comparisons/classifications; untested inputs cannot pass.
- Given owner interpretations, when reporting accuracy, then automatic and assisted facts remain separate.
- Given the deadline, when work ends, then evidence/recommendation exist even with negative results.

## Implementation Notes

- Publication authorization, 2026-10-20: Jonas subsequently requested "commit og push, oppdater devlog." This explicit instruction supersedes the earlier no-commit/no-push restriction for this completed story only. No implementation scope or test result changes.

- Owner acceptance, 2026-10-20: Jonas completed the bmad-walkthrough decision with "Klar til godkjenning, ser bra ut." Story 9.1 is now done in sprint tracking; this supersedes the earlier review handoff. Acceptance covers the bounded qualification outcome, including partial example 6, not production import. No additional owner-executed commands or tests are inferred. No commit, push or next story authorized by this acceptance.

- Independent oracle transcribed before extraction, including 113 rows and approved hashes. Separate adapter/CLI installed with pinned pdfplumber 0.11.10. Root reran all 22 import tests successfully (2.46s); implementation run also passed all 18 existing HTTP/PostgreSQL tests. Six fixtures supported, example 6 partial with six owner-assisted gaps; no automatic completion credited. No API/UI/database changes.
- All retained review findings patched and verified. Final root image build passed; 76 import tests passed (3.17s), 18 real HTTP/PostgreSQL regressions passed (0.89s), pip check clean. Regenerated machine report at 2026-10-20T12:52:49 UTC: all seven tested, 113 rows, zero source mismatches, six supported and example 6 partial. Implementation/oracle hashes match final files. No deferred findings or unresolved blocker; no commit/push under the approved boundary.
- Matrix audit: qualification = test_all_actual_fixtures_compare_every_required_fact; continuations = test_continuations_zero_duration_identity_and_unknowns and test_continuation_endpoint_provenance; overnight/owner facts = test_calendar_and_owner_facts and test_manual_owner_completion_cannot_pass_automatic_completeness; pauses = test_pause_groups_retain_rows_and_do_not_fill_gaps plus mutation/unresolved-boundary tests; invalid/bounded input = test_explicit_rejections, test_timeout_and_cancellation_terminate_worker and test_bounded_worker_output. All covering tests executed and passed in the final 76-test run.

## Spec Change Log

## Review Triage Log

| Finding | Verdict / route | Evidence |
|---|---|---|
| BH1: unrecognized line text omitted | low / reject | Such lines produce explicit unresolved locations and prevent supported classification. All approved rows are retained. Retaining arbitrary raw text for a future review UI adds contract complexity outside everyday qualification use; source references remain available. |
| BH2: incomplete/invalid field provenance passes | medium / patch | Comparator checks only dict truthiness; removing destination/end entries or changing page coordinates survives. Validate required field locations and continuation endpoints. |
| BH3: calendar fields lack derivation links | medium / patch | Added instants/day offsets have no provenance entries. Link existing clock/header provenance in the same metadata dictionary. |
| BH4: pause group output not qualified | medium / patch | Approved pause table is absent from oracle comparisons. Transcribe its intervals/labels/row memberships independently and compare them. |
| BH5: annotation loss not detected | medium / patch | Existing assertion checks only nonempty example 1 annotations. Add independent synthetic source-marker preservation checks; annotation completeness is outside the approved oracle, so do not invent fixture expectations from parser output. |
| BH6: source_order unchecked | medium / patch | Array comparisons can pass with corrupted exported source_order. Compare each value with its independent row index. |
| BH7: extended header clocks unsupported | false / reject | Qualified headers use clocks below 24; other inputs fail explicitly or remain unresolved, never silently pass. Extended-hour layouts are not qualified by the seven fixtures. Document that limit. |
| BH8: null pause boundaries merge | medium / patch | None equals None in the existing guard; require resolved matching boundary instants. |
| BH9: content outside fixed body crop | low / reject | All approved source rows match and input hashes gate qualification; changed layouts remain untested. No actual approved loss is demonstrated. General geometry detection adds branches for explicitly unqualified layouts. |
| BH10: origin labels inferred from field names | medium / patch | Timezone is owner-approved, not extracted. Header pages and duty positions are derived. Replace the heuristic with explicit field-origin rules. |
| VG1: per-field provenance verification gap | medium / patch | Pre-verified: whole-dict deletion test cannot detect individual destination/end location loss. Same root cause as BH2; add focused mutations and continuation assertions. |
| VG2: unknown annotation verification gap | medium / patch | Pre-verified: filtering out N can escape current subset assertion. Same root cause as BH5; independently generated source content must cover values/order/location, without treating parser output as oracle. |
| EC1: individual missing field provenance | medium / patch | Same demonstrated truthy-dict defect as BH2/VG1; preserve all outcomes in the shared validation correction. |
| EC2: null boundaries join pauses | medium / patch | Same proven None-equality defect as BH8; a resolved-instant guard fixes the demonstrated state. |

## Design Notes

No unresolved intent gaps or irreversible actions. Dispatch covers adapter, oracle, CLI, dependencies, tests and evidence. Production integration belongs to 10.1; resource limits do not promise layout support.

## Verification

- `docker compose build api` — installation succeeds.
- `docker compose run --rm --no-deps -v "D:/IBE160/Eksempelfiler:/fixtures:ro" api python -m pytest -q tests/test_pdf_import.py` — oracle and meaningful edge-case checks pass.
- Same read-only mount, `python -m app.qualify_imports /fixtures` — actual report; nonzero for incomplete/mismatched qualification.
- `docker compose up -d --wait api`; `docker compose exec -T api python -m pytest -q tests/test_assessment.py` — existing regressions pass.
- `git diff --check`; inspect evidence against README exceptions/coverage.
