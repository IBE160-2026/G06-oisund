---
title: '10.2 — Correct the draft'
type: feature
created: 2026-10-22
status: done
route: dispatch
epic: 10
story: '10.2'
alias: V1-06
story_key: 10-2-correct-the-draft
baseline_commit: 3e564d967fc9c76ee3fd620bb169fe3bb1e918d5
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-10-context.md
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Editing already works, but source facts and manual corrections require manual comparison. Empty places and historical warnings obscure current unknowns.

**Approach:** Complete the correction flow: expose original/current values, manual changes, added activities and unknowns. Preserve these distinctions through save/reopen using activity identity and existing source metadata.

## Boundaries & Constraints

**Always:** Allow incomplete drafts; reject invalid entered dates/times and negative intervals. Preserve UUIDs, Oslo dates, source order/clocks/codes, nullable places and original metadata. Show differences from original interpretation, not edit history; restoring an original value removes its correction marker. Without source metadata, label facts as manual. Keep duty anchors with their activities, materializing legacy anchors before structural edits; removal removes the anchor. Preserve bus/duty separation, CAR, expiry, revisions, recovery and session-bound access.

**Never:** Confirm/activate, infer missing facts/gap activities/bus changes, erase source uncertainty, persist raw documents/browser private data, migrate records or test ordinary accounts. Authoritative confirmation validation belongs to 10.3. No implementation deployment, commit or push is included.

## I/O & Edge-Case Matrix

| Scenario | Input | Result | Failure behavior |
|---|---|---|---|
| Correct | Imported time/type/trip/place | Original interpretation and manual difference visible after reopen | Invalid times retain input and prevent save |
| Structure | Added/removed/reordered rows | Manual origin, stable IDs and duty anchors preserved | Removal confirmation; original source retained |
| Unknown | Missing place/time/type or unknown code | Current unknowns explicit; historical source warnings retained separately | No inferred resolution/readiness claim |
| Cancel | Local edits | Discard restores saved facts/order/duties | Dismissal preserves input; no mutation |
| Recover | Conflict/lost reply/account switch | Existing safe recovery and isolation | No overwrite, duplication or resurrection |

</frozen-after-approval>

## Code Map

- `frontend/src/PrivateDrafts.tsx`: reuse edit/time/reset/remove/save and recovery; add/order controls already exist.
- `frontend/src/draftInterpretation.ts`: add source/current comparison by activity ID; preserve existing duty/issue helpers. Normalize mapped types and equivalent times to prevent false differences.
- `frontend/src/PrivateImport.tsx`, `backend/app/private_import.py`: source display and interpretation define original mappings, including CAR/partial Travel to.
- `frontend/src/PrivateTimeInput.tsx`, `backend/app/draft_domain.py`: reuse Oslo/interval/null validation.
- `backend/app/draft_storage.py`, `frontend/src/PrivateAccess.tsx`: preserve normalization/replay and displayed-session guards.

## Tasks & Acceptance

**Execution:**
- [x] `frontend/src/draftInterpretation.ts`, `frontend/src/PrivateDrafts.tsx`, `frontend/src/style.css` — display original/current field differences, manual activity origin and explicit unknown places/current missing required facts. Retain historical warnings without claiming they are resolved. Use existing persisted facts; no correction schema. Preserve raw time state, IDs and legacy duty anchors through structural edits; no automatic sorting.
- [x] `frontend/tests/private-import.spec.ts`, `frontend/tests/private-drafts.spec.ts`, `backend/tests/test_private_drafts.py` — cover correction/add/remove/order/cancel and save/reopen together; assert unchanged source metadata, unknowns, legacy duties, overnight/invalid times, no false correction markers and existing recovery/identity boundaries.
- [x] `backend/tests/test_private_import.py`, new `Docs/evidence/10-2-draft-corrections.md` — compare supported activity-level A–E facts with independent JSON fasit. Cover A header/end mismatch, B partial Travel to/gaps/zero duration, C overnight, D CAR transfer, E work-only/no invented Sign-off. Report import gaps before changing contracts. Intermediate-stop duplication, distance and arbitrary layouts remain unqualified; no full-fasit or runtime-oracle claim.
- [x] `README.md`, `Docs/development-log.md`, new `Docs/evidence/10-2-768.png` and `Docs/evidence/10-2-1440.png` — record executed evidence, limits and walkthrough handoff.

**Acceptance Criteria:**
- Given imported/manual work, when corrected and structurally edited then saved/reopened, then identities/order, facts, source/manual distinctions and fixed expiry survive together.
- Given partial/invalid input, when editing/saving, then unknowns remain explicit, invalid times cannot save and input remains. Incomplete drafts remain unconfirmed.
- Given saved work, when edits are discarded, then stored revision/content remain unchanged; dismissing discard preserves local input.
- Given keyboard use at 768/1440px in Day/Night modes, when correcting/reviewing, then labels, focus, wrapping and text distinctions remain usable.

## Implementation Notes

- Publication authorization, 2026-10-22: Jonas explicitly requested commit and push of completed story 10.2, including the development log. This supersedes earlier no-commit/no-push instructions for this story only. Include the accepted wording amendment, evidence and tracking; no next story is started.

- Owner acceptance, 2026-10-22: Jonas explicitly approved story 10.2 after the walkthrough and requested discard wording amendment. Sprint 10.2 is done. This supersedes earlier pending-acceptance notes; no commit/push or next-story start is authorized by this acceptance. Documented A–D import limits remain unchanged.

- Owner walkthrough follow-up, 2026-10-22: Jonas found corrections and reopen understandable, unknowns clear and readability acceptable, but requested clearer discard scope. Updated only the saved-draft discard confirmation to explicitly include changed fields, added/removed activities and reordering, while stating that the last saved version is retained. No behavioral change or story acceptance is inferred.

- 2026-10-22: Jonas approved the specification and requested continuing. Re-read from disk; no external changes. The approved intent is frozen.
- Implemented source/current comparison, explicit manual/unknown labels, legacy duty anchor materialization and memory-only Night mode. No parser, schema or access-code change. Root read the staged unified diff and inspected both regenerated renders.
- Verification: 167 backend/API tests, restart/migration/state/deadline and build passed; final focused A–E 5 passed and affected browser files 59 passed (3.9m). Earlier broad browser run passed the other 23 cases. Initial four A–E comparison failures exposed documented import gaps; A–D remain unqualified. Matrix rows covered by executed correction/structure/cancel, invalid-time, unknown, conflict/lost-response and account-switch cases. No ordinary-account test mutations.

## Spec Change Log

## Review Triage Log

| Finding | Verdict / route | Evidence |
|---|---|---|
| Blind 1: Night focus on pale warning panels | medium / patch | Pale yellow outline on pale warning background lacks contrast on reachable activity-navigation buttons and uncertainty inputs. Add a dark focus override inside these light panels. |
| Blind 2: notes incorrectly called manual | medium / patch | Importer populates uncertainty/provenance automatically; current comparison text attributes them to manual entry. Correct the wording without changing storage. |
| Blind 3: unresolved time described as unknown correction | medium / patch | Time entry writes null while raw input remains unresolved in PrivateTimeInput. Comparison reads that null and can claim a completed correction. Pass existing unresolved state to distinguish pending input and suppress its correction marker until resolved. |
| Blind 4: A–E supported-row types not compared | medium / patch | Supported work-row labels/times are asserted but mapped types generally are not. Compare every supported type against its independent event expectation. |
| Blind 5: reopened place/trip field markers unasserted | medium / patch | Simultaneous type change satisfies the aggregate marker; per-field comparisons could disappear without failure. Add independent place/trip values, marker and restoration assertions. |
| Blind 6: both modes not exercised at both widths | medium / patch | Current loop covers Night768 and Day1440 only; light-panel keyboard focus must be checked in both modes at both widths. Extend existing scenarios. |
| Blind 7: extract legacy transition helper | low / reject | Dense expression is harder to read, but no incorrect transition or divergent caller was identified; existing executed cases cover identity/anchor transitions. Extra abstraction is unnecessary for this cosmetic observation. |
| Verification 1: place/trip comparisons lack independent assertions | medium / patch | Pre-verified gap: removing their sourceFields entries leaves current type-only comparison assertions green. Same cause as Blind 5; test each field and restoration independently. |

Edge-case layer returned no findings. All three layers ran. Patch entries are grouped only where the same comparison-test defect produced Blind 5 and Verification 1.

All six patch groups were fixed and passed targeted checks. Final root verification passed 167 backend/API tests (112.70s), restart/migration/replay/state/deadline, production build and all 82 browser cases (4.8m). Both fixture sets remain covered with A–D import gaps recorded. Root inspected regenerated renders and patched diff. No review finding deferred. Sprint remains review for owner acceptance; spec done denotes implementation only. Approved no-commit/no-push boundary overrides the workflow's default commit.

## Design Notes

Dispatch: coordinated presentation and integration evidence. No unresolved intent choice or migration. Dependencies 9.4/10.1 and identity repair are accepted. Epic-9 actions E9-A2–A5 remain open. A–E were committed/pushed at owner request before planning; their presence does not qualify extraction.

## Verification

Run `scripts/verify-private-drafts.py` with `COMPOSE_PROJECT_NAME=ibe160-private-tests`: disposable API/PostgreSQL, restart, build and browser checks. Run `npm.cmd run build` and `git diff --check`. Inspect new renders, contrast/focus and absence of browser storage. Keep runtime checks sequential and restore operational API availability without changing ordinary account/data. Record actual failures and coverage limits; no application tests during planning.

## E10-A1–A3 maintenance follow-up — 2026-10-24

The approved draft-contracts bundle preserves the normalized original import baseline (including absence for manual drafts), shares fresh-write physical-bus semantics, and pins review policy to issued operations and confirmed plans. Missing deadhead/CAR trip numbers remain visible as unknown without a separate acknowledgement; passenger direction joins the draft unknown display. Historical acceptance above remains unchanged. See [the maintenance evidence](../../docs/evidence/epic-10-draft-contracts.md). Implementation checks and owner acceptance for this follow-up are tracked separately; E10-A1–A3 remain in-progress.
