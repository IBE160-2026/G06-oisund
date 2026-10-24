---
title: 'Epic 10 review feedback: meaningful trip decisions and bus controls'
type: bugfix
created: 2026-10-24
status: done
route: dispatch
baseline_commit: 2e90c507eb3c58669a01d1f6a5ab12734ac65755
baseline_snapshot: tmp/e10-feedback-before
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-10-context.md
---

<frozen-after-approval reason="owner feedback and explicit boundary decision, 2026-10-24">

## Intent

**Problem:** Review demands irrelevant acknowledgements, treats raw source markers as deviations and exposes English Trip; invalid bus save remains enabled and clearing lacks a button.

**Approach:** Apply the owner's approved boundary to new reviews, improve bus controls, and preserve historical records and pending work.

## Boundaries & Constraints

**Owner decision:** Only effective passenger/routed `trip` activities require checkboxes: missing trip number, line, direction, from/to place, or concrete current trip uncertainty. Other activity types, day duty/bus, duty anchors and original source markers/issues have no dedicated checkbox. Unsupported types still require explicit classification; selecting non-trip must remove candidate trip decisions. Required service date, activities, valid explicit Oslo start/end, nonnegative intervals/order and fixed expiry remain blockers, never checkboxes.

Raw annotations (including `t`) are preserved as neutral source information, never assigned an invented meaning or presented as actionable uncertainty merely for existing. Stop injecting marker-warning text on new imports. Existing exact generated marker fragments must not trigger current warnings/checkboxes, while substantive remaining/manual notes stay visible/actionable. Do not rewrite existing saved facts, operation bodies, source metadata or accepted decisions to accomplish this.

Use Norwegian `tur` for recognized user-facing Trip/trip type/code presentation; canonical stored types/raw source facts remain unchanged. Disable and grey fresh draft/current-bus save when the bus value is invalid; preserve useful associated errors/input and same-operation recovery. Add explicit clear buttons beside both bus fields, setting an unsaved empty proposal just like clearing duty; saving/cancelling retains existing semantics. Preserve `000x`, meaningful spaces and the 100-code-point/NUL contract.

Never alter existing source guards, identity/session/CSRF, concurrency, expiry, receipts, private browser-storage prohibitions or A4/A5. No new stories, parser qualification, theme persistence, commit/push/staging or inferred final owner acceptance.

## I/O & Edge-Case Matrix

| State | Expected | Compatibility |
|---|---|---|
| Non-trip with absent fields/notes | No checkbox; facts remain readable | Date/time/type blockers stay |
| Trip missing fields or meaningful note | Exact relevant decisions required | Missing/extra decisions reject atomically |
| Unknown type → trip/non-trip → back | Candidate set follows classification; removed checks do not return automatically | Frozen pending decisions govern retry/accept |
| Marker only / marker plus note | Neutral source marker; only substantive note actionable | Saved raw text and source unchanged |
| Bus 102/100 code points, 000x | Invalid save disabled; valid exact value persists | Pending retry not disabled/replaced |
| Clear draft/current bus | Empty local proposal, explicit save/cancel, reopen unknown | Other facts/expiry unchanged |
| Existing v1/v2 plans/operations | Exact old presentation/replay/first acceptance | No policy reinterpretation |

</frozen-after-approval>

## Code Map

- `backend/app/workday_domain.py`, `workday_storage.py`: add v3 assessment for fresh review issuance; keep v1/v2 branches exact. Review can expose trip candidates for unclassified rows; confirmation independently derives the effective set.
- New `backend/migrations/private/008_review_feedback.sql`: atomically widen existing policy CHECK constraints to allow 3, preserving all current version values. Never edit already applied 007.
- `backend/app/private_import.py`, `import_issues.py`: existing mapper copies annotations into activity uncertainty. Reconstruct exact generated marker fragments using retained metadata/provenance; remove only their presentation/actionable role. Global original issues remain source information, not duplicate decisions.
- `frontend/src/PrivateConfirmation.tsx`: filter candidate decisions by classifications; prune obsolete checked IDs, bind acceptance to frozen submitted classifications, retain exact plan validation. New pages issue v3 reviews; old issued operations retain their policy. Reload is required for old bundles beginning new work after rollout; no general old-client support added.
- `draftInterpretation.ts`, `PrivateImport.tsx`, `PrivateDayOverview.tsx`, `PrivateDrafts.tsx`: neutral source markers, filtered current uncertainty and recognized Norwegian labels; no underlying fact mutation during display/unrelated save.
- `PrivateDrafts.tsx`, `PrivateBus.tsx`, `busValue.ts`: reuse validation; fresh-save disabled and clear controls obey existing locks.

## Tasks & Acceptance

- [x] Backend assessment/storage, migration 008 and source-uncertainty helpers: v3 implemented; v1/v2 operation/plan semantics and imported baseline retained.
- [x] Frontend files above: classification-filtered decisions, neutral markers, Norwegian display and disabled/clear bus controls implemented.
- [x] Backend/frontend regressions and sequential verifier fixtures added; focused selections passed. Only owner-superseded expectations changed. Final combined execution remains root-owned after review.
- [x] Existing maintenance/10.3/10.4 specs/evidence, retrospective appendix, development log and existing sprint action notes amended; historical verdict and prior work preserved. Final root results are appended after execution.

Given the approved matrix, when a new plan is confirmed/reopened, then only relevant effective-trip decisions are recorded and all strict receipt/ownership/deadline checks hold. Given historical records, when migrated/read/retried, then every original fact/decision/hash/version/deadline remains unchanged. Given malformed/missing replies or account/expiry changes, when controls settle, then unsaved text and pending identities retain existing protections.

## Implementation Notes

User explicitly requested these review corrections and approved the concrete passenger-only boundary. This authorizes implementation without another start checkpoint. This is amendment work, not a new story. Existing dirty work is intentionally preserved under the ignored repository snapshot/manifest `tmp/e10-feedback-before` and `tmp/e10-feedback-baseline.json`; current operational baseline is `tmp/e10-feedback-operational-before.json`. Original A1/A2 fixes and prior review evidence remain valid history; new policy supersedes A3 only for new reviews. Owner acceptance/publication remain pending.

## Spec Change Log

## Review Triage Log

Root audited the complete 238,095-byte tracked/untracked diff without staging and the subsequent targeted corrections. Matrix coverage ran in the 102-case API selection, 5 supplemental checks, 16 browser scenarios and 3 direct marker cases. Root's latest classification-response guard selection passed 11 browser cases (31.6s) on the served build. Root audit identified a pure-marker/null-position mismatch and the older disabled-button test expectation; both were corrected before independent review. Final affected selection passed 11 API cases (15.33s) and 6 browser cases (33.2s), plus build/whitespace checks. No claim of final combined verification or owner acceptance at this checkpoint.

All three context-free layers completed before triage. Blind floor: 241,649 / 1,024 = 235.99 KiB; min(floor(sqrt(235.99)+1),10)=10 candidates. Edge supplied two concrete findings; verification supplied the editor-space defect under Other findings. Each is adjudicated separately below.

| ID | Verdict | Checked evidence and disposition |
|---|---|---|
| BH1 movement unknown display | low | `identifiers` filters absent movement trip numbers and `currentUnknowns` no longer lists them, removing the previously requested visible unknown in the overview. Direct patch: normal `Tur: Ukjent` for supported movements, no checkbox and no warning classification. |
| BH2 earlier owner checklist | low | The earlier maintenance evidence still instructs movement-place acknowledgements and a post-classification superset. Those are no longer current. Patch the actionable checklist/pointer to policy 3, retaining historical execution results. |
| BH3 final amendment evidence pending | false | The amendment evidence accurately says root final verification/review/rollout are pending; no final amendment result was inferred from the earlier run. Actual final results/manual steps remain an explicit root completion task, not a false pass to repair. |
| BH4 README readiness scope | low | The concluding 267/198 readiness paragraph reads as current although amendment code changed afterward. Directly label that checkpoint historical and link the pending/new amendment results; append actual final results only when run. |
| BH5 sprint stale retro comment | low | `epic-10: done` still says no retrospective requested, while retro is done. Direct comment correction; retain story acceptance and historical verdict. |
| BH6 historical plan browser proof | low | Real v1/v2 payload/replay is covered in backend tests, but the new UI projection also filters historical Facts' stored notes. Preserve raw note text in explicitly historical details (plain facts, not an active warning) and add real legacy-plan reopen coverage alongside neutral current projection/exact JSON decisions. |
| BH7 literal raw-code correction | false | The preservation branch only avoids rewriting an unchanged translated alias. Clearing/retyping, or ordinary sequential replacement, stores literal `tur` because the intermediate current value no longer displays as that alias. No explicit correction is blocked; unrelated display must preserve raw Trip/trip as requested. |
| BH8 misleading candidate labels | medium | `validCandidates` compares only IDs. Correct IDs with swapped labels pass review and can send a confirmation before final receipt comparison rejects the label mismatch. Validate labels against verified draft/field facts before displaying decisions; exercise tampered/swapped labels. Small extension of the existing private validator, no new public surface. |
| BH9 original source warning style | low | Confirmed-day historical source issues share `day-uncertainty` styling with current uncertainty, despite explicit historical captions. Direct neutral presentation for historical source issues; retain their complete text and current substantive-warning styling. |
| BH10 unrelated-save roundtrip | low | Existing marker tests check saved equality after initial display/confirmation, not an unrelated editor change/save/reopen. Add that narrow integration proof to ensure the raw mixed marker/manual note remains identical until explicitly edited. |
| E1 editable note separators | medium | Controlled uncertainty input calls the trimming projection on each render; typing a trailing separator removes it before the next character. Preserve editable whitespace, trim only assessment/read-only presentation; add sequential multiword typing/save/reopen proof. |
| E2 invalid whitespace bus guard | medium | With saved null, >100 whitespace characters normalize to null, so `editing.current` becomes false while invalid text remains. Cancel/navigation protection is released. Invalid input must count as editing until corrected/cleared/cancelled; test the saved-null path and no-write behavior. |
| V1 editable note separators | medium | Independently verified same input/helper path and absence of character-by-character tests; same direct correction as E1, with its own finding retained here. |

Patch groups: editor projection/roundtrip (E1/V1/BH10); invalid bus dirty guard (E2); movement unknown visibility (BH1); historical Facts/browser proof (BH6); candidate label contract (BH8); neutral historical source presentation (BH9); current documentation/status supersession (BH2/BH4/BH5). No intent gap, new story or deferred implementation is required. BH3/BH7 are rejected on the specific refutations above.

All seven patch groups were implemented by the original worker and inspected by root. The 22 affected browser scenarios passed across the initial run and four corrected-fixture reruns; production build passed. The original edge reviewer re-inspected E1/E2 read-only and found no remaining concrete issue; root checked the label validator, historical raw-note path, movement display and associated integration regressions. No retained finding is deferred. Complete final execution is recorded separately below when finished.

## Verification

Build retained-marker associations once per assessed/displayed content where possible, rather than traversing every source row/provenance point for every passenger activity. Filtering must use the same nearest-preceding-row/tie rule as existing `annotation_rows`; marker stripping is evidence-based, never a general natural-language heuristic.

Classification filtering may remove legitimate inapplicable candidates, not silently accept malformed/unassociated candidate IDs. Fresh v3 review candidates must identify an existing potentially passenger activity and a declared decision field. Keep exact frozen-receipt checks after this validation. Inspect translated source activity headings as well as current fields; raw source data remains unchanged.

SourceLocation line/column are nullable in the existing saved-content contract. Retained metadata association must tolerate absent/null positions without TypeError or invented row attachment; test the validated legacy shape as well as fully located markers. Unassociated markers remain neutral original information.

A literal old marker-warning fragment that matches a retained document annotation remains neutral even when its row position is unavailable. Do not turn that annotation-only phrase into a required passenger decision merely because association fails. Filter the exact known document fragment without inventing an activity attachment; retain every substantive/manual remainder and the original stored note. The nullable-position regression must expect no marker-only uncertainty decision, not treat the known raw marker as a real deviation.

Worker runs only sequential focused disposable checks/build and restores services; no ordinary accounts or operational upgrade. Root owns final complete `COMPOSE_PROJECT_NAME=ibe160-private-tests` run of `uv run --no-project python scripts/verify-private-drafts.py`, five restoration controls, full diff/matrix audit and three independent reviews/fixes. Root then verifies original data/security/secret and policy values unchanged, upgrades compatible local runtime, restores historical generated PNGs and records concrete manual checks. Keep the original private database/volume/secret. No product code changes after final verification without appropriate retesting.

## Final execution

Root's final sequential verifier passed **288 backend/API tests (324.07s)**, exact restart/repeated-migration preservation, production build and **220 Playwright tests (12.3m)**, exit 0. Five verifier/restoration controls passed (0.131s). No product code changed afterward. All retained review findings are corrected; none deferred. Fresh synthetic 768px Day/Night review renders were inspected and retained separately; actual iPad/Safari remains not run.

Ordinary full-row hashes, including policy values, match the original baseline except three expired login-throttle rows removed by the existing startup cleanup. The exact investigated difference is documented in [current evidence](../../docs/evidence/epic-10-review-feedback.md); no broad security/policy exclusion is used. After compatible migration 008/API rollout, all hashes also match the post-test restoration snapshot exactly. Original database/volume/secret and A1/A2 guards are retained, running backend hashes and served final asset match tested code, ordinary services are healthy and disposable services stopped.

The current manual checklist is in the linked evidence. Owner instructions override generic BMAD spec-done/commit steps: this amendment stays in-review, A1–A3 stay in-progress pending final owner acceptance, A4/A5 retain 12.3/12.4 assignment, and no staging/commit/push/new story is performed. Historical retrospective verdict and accepted-story status remain unchanged.

## Owner acceptance — 2026-10-24

Jonas explicitly replied “Godkjent” to the final review-feedback handoff. This accepts the E10-A1–A3 maintenance bundle as amended by the passenger-only policy-3 feedback. Both maintenance specifications and actions A1–A3 are now done. Earlier pending-acceptance statements are historical and superseded by this entry. Final evidence remains 288 backend/API tests, 220 browser tests, restart/migration/build and five verifier controls; no additional manual scenario or actual iPad/Safari pass is inferred from the approval. A4/A5 remain open under existing 12.3/12.4. Historical retrospective verdict and original story acceptance are unchanged. Commit/push remain unauthorized; no product code, runtime or private data changes in this acceptance update.
