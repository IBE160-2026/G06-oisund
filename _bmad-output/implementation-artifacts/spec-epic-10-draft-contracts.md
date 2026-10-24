---
title: 'E10-A1–A3 — Preserve draft source, bus and review contracts'
type: bugfix
created: 2026-10-24
status: done
route: dispatch
baseline_commit: 2e90c507eb3c58669a01d1f6a5ab12734ac65755
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-10-context.md
  - D:/IBE160/_bmad-output/implementation-artifacts/spec-10-3-confirm-the-reviewed-plan.md
---

<frozen-after-approval reason="human-owned intent — changes require human approval">

## Intent

**Problem:** Draft updates can replace original source facts; draft/current bus entry differs; confirmation and reading disagree about some unknown fields.

**Approach:** Complete the authorized E10-A1–A3 maintenance together. Preserve established records, acknowledgements and retry identities while enforcing the corrected contracts for new work.

## Boundaries & Constraints

**Always:** Freeze the normalized import_metadata baseline after first save, including absence for a manual draft. Reject changes/removal/addition on updates without mutation. A separate import creates a new draft. First creation remains allowed; ordinary field/structure correction preserves original metadata. Check accepted replay before comparing the current baseline, so an older accepted operation still returns its historical result.

Use the existing current-bus contract for new draft/current writes: all explicit Unicode White_Space means null; otherwise preserve exact formatting/zeros/FEFF, up to 100 code points. Reject NUL with useful validation. Do not use trim/strip substitutes. Preserve historical raw records/results/fingerprints and pending retry bodies; do not normalize stored reads or old receipts.

Keep service date, activities, explicit Oslo times/order and supported classification mandatory; permitted missing places, passenger identifiers, day duty/bus, duty anchors, source issues/annotations and uncertainty require the existing explicit decisions. Source clocks/raw codes/provenance have no new missing-field requirement. Initially unknown types retain the conservative passenger-field acknowledgement superset. Align passenger direction display. Preserve every existing account/session/CSRF/origin/no-store, concurrency, expiry, deletion and leave/recovery guard.

**Owner decision (2026-10-24):** Missing trip number for supported deadhead/CAR movement stays visible as “Ukjent” without a dedicated acknowledgement. Narrow confirmation copy to the actual explicit decision set; do not imply that every visible unknown receives an individual checkbox. Missing movement line/direction and non-passenger identifiers have no new dedicated acknowledgement. Trip numbers remain optional. Unsupported original types retain the existing conservative superset.

**Never:** Modify the retrospective's historical verdict, rewrite old private content/decisions, reset ordinary data, persist private browser content, add new stories, change parser/layouts or implement A4/A5. No staging, commit, push or advance owner acceptance.

## I/O & Edge-Case Matrix

| Scenario | Expected | Rejection/compatibility |
|---|---|---|
| Baseline update | Same source survives correction/reorder | Alter/remove/add source rejected atomically |
| Manual/legacy draft | Missing/null metadata equivalent | No synthetic import provenance |
| Bus inputs | Shared null/whitespace/Unicode rules | NUL rejects before storage; input preserved |
| Retry | Accepted historical result unchanged | Changed operation payload still conflicts |
| Review evolution | New rule pinned per issued operation/plan | Old plans and pending/accepted reviews keep legacy decisions |
| Identity/expiry/delete race | Existing protections remain | No cross-owner mutation or resurrection |

</frozen-after-approval>

## Open Questions

None. The owner selected visible unknown without a separate acknowledgement for missing movement trip numbers.

## Code Map

- `backend/app/draft_storage.py`: guard after replay/revision checks; fresh-write bus normalization only. `draft_domain.py` also serves historical reads, so no whitespace-normalizing model validator.
- `workday_domain.py`, `workday_storage.py`: assessment/presentation/review/replay currently recompute unknowns. Pin internal policy version to both pending operations and plans; preserve legacy v1 exactly.
- `workday_bus_domain.py`, `workday_bus_storage.py`, `frontend/src/PrivateBus.tsx`: reuse explicit whitespace/NUL/length semantics. Extract dependency-light helpers without domain import cycles.
- `frontend/src/PrivateDrafts.tsx`: exact acknowledgement/request comparison; normalize only newly issued payloads, preserve old pending bodies and permissive historical reads. `draftInterpretation.ts`, `PrivateConfirmation.tsx`: unknown presentation/copy.

## Tasks & Acceptance

**Execution:**
- [x] `backend/app/draft_storage.py`, existing `draft_domain.py` read compatibility, new `bus_value.py`; frontend new `busValue.ts`, `PrivateDrafts.tsx`, `PrivateBus.tsx`: baseline guard and shared fresh-write validation/normalization, preserving historical replay.
- [x] `backend/app/workday_domain.py`, `workday_storage.py`, `frontend/src/draftInterpretation.ts`, `PrivateConfirmation.tsx`; additive `007_draft_contracts.sql`: explicit field matrix; internal legacy/new assessment policy version on workday operations and plans plus fresh-write normalization flag on draft operations, no response-key expansion.
- [x] Backend draft/bus/workday and frontend draft/bus/confirmation/identity regressions: source mutations, absence/null, replay, Unicode/NUL/limits, legacy/new policies. Focused 36 API and 39 browser cases passed; initial broader API run's one legacy fixture failure was corrected and passed on rerun. Historical F1/F2 probes are pre-fix reproductions; no new red-baseline run is claimed.
- [x] Sequential verifier includes raw legacy/new draft/review/plan/receipt/deadline fixtures and migration/restart assertions; restoration controls pass. Final combined execution remains root-owned after review.
- [x] Existing specs, historical retro appendix, README, sprint actions and development log updated; [maintenance evidence](../../docs/evidence/epic-10-draft-contracts.md) records checks and owner handoff separately.

**Acceptance Criteria:**
- Given an imported baseline, when altered/removed or attached to an already saved manual draft, then validation rejects with exact content/revision/operation/deadline preservation; unchanged-source edits still save.
- Given either bus entry, when blank/Unicode/meaningful/NUL text is submitted, then fresh writes use the same semantics and invalid input is retained with feedback; old saved facts and accepted results remain identical.
- Given old plans, accepted retries or an issued pre-upgrade review, when reopened/retried/confirmed after migration, then its exact original decisions/result/deadline survive independently of source expiry.
- Given a newly issued review, when required facts/classification/acknowledgements are absent, then confirmation rejects; the approved matrix and displayed unknowns agree without invented facts.
- Given account changes, conflicts, expiry/deletion or lost responses, when a delayed request settles, then existing protection and unresolved identities remain intact.

## Implementation Notes

User authorizes the three-fix bundle and implementation/tests/reviews; this is existing-action maintenance, not a new story. The known dirty retro documents are explicitly authorized and preserved; fingerprints are recorded in ignored `tmp/e10-followup-local-baseline.json`. No additional start approval is needed after resolving the specific product question. Original story/epic done statuses and retro verdict remain historical; A1–A3 stay in-progress until owner acceptance, A4/A5 remain open for 12.3/12.4.

## Spec Change Log

- 2026-10-24: Owner resolved movement-trip acknowledgement choice; scope finalized before implementation. Estimated total 2–4 hours including automated verification and review, excluding owner waiting.

## Review Triage Log

Root read the complete 118,707-byte tracked/untracked diff without staging. Initial matrix audit: baseline header/source-row/removal/addition and absent/null cases passed in the 36 API selection; shared bus boundaries passed in that selection plus browser input retention and existing current-bus Unicode cases; legacy retry/changed-body and policy-pinning cases passed; identity/delayed-response cases passed among the 39 browser selection, while affected broad API suites cover existing expiry/deletion/concurrency guards. Full combined run remains pending at review entry.

All three context-free layers completed before triage. The protected verification instruction initially required an escalated read; the same reviewer retried successfully. Edge-case and verification-gap returned no findings within their instructed scopes. Blind floor: 119,263 bytes / 1,024 = 116.47 KiB; min(floor(sqrt(116.47)+1),10)=10 candidates, each adjudicated below.

| ID | Verdict | Evidence and disposition |
|---|---|---|
| B1 evidence path case | low | Physical `Docs` spelling produces uppercase untracked paths although tracked evidence is canonical `docs/`. New lowercase links would fail if those paths were published as-is. Patch workspace directory spelling to canonical lowercase without staging or content loss; no historical file moves in the resulting Git diff. |
| B2 direction absence semantics | low | New direction detection uses JS trim while assessment uses Python strip; FEFF/U+001C produce opposite displayed decisions. Direct patch: use explicit assessment-compatible absence semantics in current unknown presentation, with boundary tests; bus retains its separate contract. |
| B3 blank movement trip facts | medium | Review Facts renders only null as unknown, so allowed empty/whitespace trip strings produce blank movement facts. Direct patch to show an explicit unknown marker under the existing absence rule; preserve meaningful strings and stored content. |
| B4 CR/LF single-line bus editing | low | Single-line input sanitation predates this bundle in both editors. Accepted raw state is retained on read and on unrelated draft saves; no new automatic loss established. Rare multiline bus editing would need a new editing strategy/guards beyond direct correction. Reject under low-impact/complexity rule; no broader bus editor rebuild authorized. |
| B5 invalid bus association | low | Newly retained invalid text is explained by general live status only. Direct markup patch associates an error and aria-invalid with each affected bus field; no new workflow or server surface. |
| B6 source 422 explanation | low | Existing generic 422 mapping hides the new detail, but normal correction/import UI always retains metadata or creates a separate draft; no ordinary UI trigger exists. A specific public error code/new response branch would add complexity for a non-UI mutation. Reject under low-impact/complexity rule; API rejection already carries actionable detail. |
| B7 old pending browser proof | low | Backend old-body/receipt coverage exists and frontend chooses pending bodies verbatim, normalizing only fresh issuance. An old loaded page executes its unchanged bundle; refreshed pages deliberately do not persist private pending bodies. A cross-bundle upgrade fixture is disproportionate without a demonstrated client failure. Reject under low-impact/complexity rule; do not claim a fresh old-bundle browser run. |
| B8 individual acknowledgement omission | low | Existing empty-ack rejection and exact unknown-key assertions cover the rule, but field-specific omission checks provide inexpensive additional evidence. Patch the existing matrix to reject each omitted required decision without accepted mutation before the successful confirm. |
| B9 imported row removal | false | Existing `private-import.spec.ts` structural-correction flow removes an imported activity, saves and asserts unchanged source metadata and duty anchors (lines 161–166). The final full run includes it; no duplicate test needed. |
| B10 source-marker mock | low | New AST substring assertions can pass with ineffective runtime checks and mirror implementation text. Delete the added test; actual guarded migration/restart/API execution verifies these fixtures. Retain the five existing restoration controls. |

Surviving patch groups: B1 canonical workspace case, B2/B3 shared presentation absence rule, B5 field association, B8 negative matrix, B10 redundant test deletion. No intent gap, deferred story, historical verdict change or new product decision is required.

All retained patches completed. Physical directory case was normalized with all 66 paths/content hashes preserved and no staging. Activity absence now matches assessment across draft/review/day values; field errors are associated and individual omitted decisions reject without mutation. Removed only the new source-marker test; five existing controls remain. Patch checks passed: 7 API (11.96s), 9 browser (35.7s), 5 verifier controls (0.171s), build and whitespace checks. Root read the changed code/tests and updated complete diff. Original blind reviewer re-inspected all retained patches, confirmed the existing row-removal case and reported no remaining concrete issue in that patch scope. Final combined run is in progress, separately from owner acceptance.

Final root run completed, exit 0: **267 backend/API tests (307.60s), exact restart/repeated-migration state preservation, production build and all 198 Playwright tests (11.7m)**. Five existing restoration controls passed again (0.116s). Root matrix audit is complete: every row runs in this combined selection, including legacy/new pending/accepted state, absence/null, source/header mutations, structural removal/reorder, input retention, immutable replay/conflicts, identity/expiry/delete races. Fresh synthetic 768px Day/Night review images were inspected and retained under new names; historical generated PNGs were restored.

Ordinary business/security/secret fingerprints match before/after tests and after compatible local API/migration rollout, excluding only documented additive policy columns whose legacy defaults were separately checked. Original private database container retained; API/database/frontend healthy, test services stopped. Served frontend asset `/assets/index-DBiot179.js` matches the production build; backend source hashes match reviewed files. No ordinary-account automated test or data/volume/secret reset.

User's explicit acceptance/publication restrictions override the generic completion/commit step: this maintenance spec remains **in-review**, A1–A3 remain **in-progress**, no story acceptance changes, staging, commit, push, new story or retrospective restart. No retained review finding remains unresolved. Owner manual acceptance and actual-device qualification are distinct and pending; A4/A5 retain existing 12.3/12.4 assignments.

## Design Notes

Use internal v1 defaults for existing operations/plans and explicit new-policy values only for new reviews; confirmation copies the operation policy to the plan. Keep response shape unchanged. Storing confirmed unknowns alone would not protect pending reviews. Compare operational hashes excluding only newly added policy columns, reporting those additions separately.

An internal `draft_operations.normalize_physical_bus boolean NOT NULL DEFAULT false` preserves already-issued pending operations from old clients, whose receipt check expects exact bus text. New issuance explicitly writes true. First acceptance normalizes only true operations, after accepted replay/revision/baseline guards. Fingerprint the raw request in either mode; preserve stored results and pending bodies. Old pending operations may finish under their pinned legacy bus behavior. No public fields or general support promise for obsolete clients issuing new work.

## Verification

Representability validation (NUL/length) applies to every first acceptance, including legacy pending draft operations; only whitespace canonicalization is version-pinned. JSONB cannot contain an accepted historical NUL. Keep current-bus response/receipt validation at least as strict as before; fresh-write sharing is not permission to weaken malformed-response guards.

Policy tests need an independent oracle: legacy v1 requires bus acknowledgement for U+001C, fresh v2 does not; FEFF is meaningful under both, and U+0085 is unknown under both. Do not derive the only expected result from the assessment helper under test. Exercise the additive migration on populated pre-007 synthetic tables (a disposable transaction/schema is sufficient), proving existing pending/accepted rows acquire false/v1 defaults without changing their original columns; repeated migration/restart tests alone are not a first-upgrade proof. Include source-row baseline alteration as well as header alteration/removal/addition in rejection coverage.

Run affected synthetic backend/browser checks first, production build, then the sequential verifier with COMPOSE_PROJECT_NAME=ibe160-private-tests: `uv run --no-project python scripts/verify-private-drafts.py`; mocked restoration controls: `uv run --no-project python scripts/test_verify_private_drafts.py`; `git diff --check`. Root owns final combined run, independent three-layer review, ordinary-data fingerprint comparison and compatible local runtime update after review. Worker restores services after each run, uses no ordinary accounts and does not upgrade operational API independently.

Manual: edit/save/reopen corrected imported facts and compare original source; enter/clear bus with zeros and meaningful whitespace; inspect new-review unknowns/classification and old-plan reopening; test failed input/cancel/conflict by keyboard in Day/Night. Record actual checks, not iPad acceptance.

## Owner review amendment — 2026-10-24

The approved `spec-epic-10-review-feedback.md` supersedes the earlier A3 matrix for newly issued reviews only. Policy 3 requires decisions solely for effective passenger `trip` activities: missing trip/line/direction/from/to and substantive current uncertainty. Non-trip facts, day duty/bus, duty anchors and original source issues/markers have no dedicated decision. Unsupported types still require explicit classification. Historical v1/v2 issued operations, plans, decisions and replay retain their exact policy and stored facts. Migration 008 widens existing constraints without updating rows.

Exact old generated marker fragments are filtered using retained source/provenance for current presentation only; substantive/manual text remains. New imports stop injecting marker warnings. Recognized Trip/trip presentation uses Norwegian tur, retaining stored types/source. Both bus editors disable fresh invalid saves and expose explicit unsaved clear proposals with existing save/cancel/recovery semantics. Source guards, fixed expiry, identity and receipt protections remain. Root owns full verification, independent review and runtime rollout; owner acceptance remains pending.

## Owner acceptance — 2026-10-24

Jonas explicitly replied “Godkjent” to the final review-feedback handoff. This accepts the E10-A1–A3 maintenance bundle as amended by the passenger-only policy-3 feedback. Both maintenance specifications and actions A1–A3 are now done. Earlier pending-acceptance statements are historical and superseded by this entry. Final evidence remains 288 backend/API tests, 220 browser tests, restart/migration/build and five verifier controls; no additional manual scenario or actual iPad/Safari pass is inferred from the approval. A4/A5 remain open under existing 12.3/12.4. Historical retrospective verdict and original story acceptance are unchanged. Commit/push remain unauthorized; no product code, runtime or private data changes in this acceptance update.
