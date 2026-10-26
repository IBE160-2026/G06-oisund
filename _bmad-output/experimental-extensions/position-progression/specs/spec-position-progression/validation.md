# Document validation

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

2026-10-26 continuation. Document coherence and preservation review: pass as a planning draft, subject to the accompanying mechanical [result](validation.json). This supersedes the previous report's open Q1/Q2 and no-epics continuation point. No implementation, product test, real position collection or GPS suitability evidence.

## Coherence and workflow

Six stable capabilities retain intent/success, explicit constraints/non-goals and a fictional demonstration target. PP-D1/PP-D2 are user-set planning choices; PP-D3/PP-D4 preserve advisory anchors/remapping. A3 and PP-T1–T3 remain untested assumptions/technical proposals, not user acceptance.

Installed BMAD steps were followed in sequence: prerequisites and requirements → one user-requested epic → four stories → final validation. Existing SPEC supplied the product requirements instead of a new PRD; inherited architecture plus the short technical addition supplied the design context. The explicit user instruction authorizes completion without asking again at workflow menus. It does not approve the drafted stories or authorize implementation. The terminal help/catalog check leads to no further workflow under the current implementation gate.

One epic delivers driver value across four slices. S1 is useful as route inspection/manual reference without GPS; S2 supports ordinary following and safe stopping without S3/S4; S3 adds manual recovery without persistence; S4 adds the complete saved handoff. Dependencies point only to earlier slices and the external route function. No foundation-only database/backend/frontend stories, starter template or new service. The anchor resource and minimal receipts enter only in S4; safe watch cleanup is already in S2.

## Preservation and coverage

| Load-bearing source rule | Contract and story coverage |
|---|---|
| Relevant start, not full-pattern first stop | CAP-1; behavior; example A-o2/range2..8; S1-AC1/2, S2-AC1 |
| Distinct repeated Quay visits; qualified dated route and coordinate source | CAP-1/2/6; route-interface/technical-addendum; A-o2/A-o5; S1-AC1/3/4/5 |
| Manual post-gap recovery first; arbitrary manual jump, no invented passages | PP-D1; CAP-3; example step3; S3-AC1/2/3/6 |
| Fresh manual protection, later coherent GPS reassessment, age insufficient | PP-D3; CAP-4; behavior; example step4/rejections; S2-AC3/4 |
| Same workday across midnight, not calendar-day reuse | PP-D2; CAP-5; example step6 and W2 rejection; S4-AC2/4 |
| New confirmed trip/range maps by identity, old evidence/sequence not fresh | PP-D4; route-interface; example A8→B3; S4-AC2/3 |
| Explicit Pause/Off, no visibility-driven restart | behavior/technical-addendum; example rejection; S2-AC6, S3-AC4/5, S4-AC7 |
| Separate missing route facts and uncertain measurements | CAP-6; route-interface; example rejection; S1-AC4, S2-AC1/5 |
| Existing online access/revisions/retry and fixed expiry/deletion | SPEC constraints; technical-addendum; S1-AC6, S3-AC5, S4-AC5–8 |
| Preserve manual outcomes, user data, frozen route and private/demo boundary | scope/behavior; example invariant; S1-AC5/6, S2-AC2/7, S4-AC8 |
| Small device, quality and threshold qualification tasks; no empirical claim | Every story's qualification tasks, PP-NFR4; research evidence remains historical |
| No route reimplementation, V1 edits or execution | Epic prerequisites/exclusions; short technical addition; all outputs extension-local |

All eight functional, five nonfunctional and three concrete UI requirements map to stories. Twenty-nine uniquely identified Given/When/Then criteria cover successful behavior and failure cases; semantic review finds no omitted first-epic topic. Broad uncertainty/geometry/background/vehicle-feed work remains outside this bounded increment.

## Mechanical checks and limits

[validate-planning.py](../../.bmad-runner/validate-planning.py) checks local Markdown links and frontmatter input/companion paths, marker/template completeness, stable capabilities, epic/story/criterion IDs, declared FR/NFR/UI coverage, fictional coordinate/occurrence mapping, overnight interval and parent maximum expiry, resolved TOML/YAML routing, Git whitespace and changed-path boundary. It writes only validation.json in this extension and runs no product imports or tests.

The scenario uses two dated trips on November2/3 in W1. A8/G evidence at23:48 is twenty minutes old when B3/G is proposed at00:08; B has its own operating date. W1 planned end Nov3 00:20 and maximum expiry Nov10 00:20 preserve the seven-day bound, subject to earlier closure. All source IDs, coordinates and measurements are explicitly synthetic; the scenario assumes qualification and cannot establish it.

Review also checked that receipts do not become a hidden stop history, Off cannot claim cancellation of a possibly committed save, and stale callbacks cannot revive explicit stopped intent. These are proposed acceptance rules, not observed behavior.

## Isolation and remaining gates

Workdir/repository root: D:/IBE160-plan-position-progression. Branch: codex/plan-position-progression. Initial local changes from the prior specification round were preserved; the index was empty. All changed files remain inside this extension; shared/global configuration, V1, product code and other worktrees were not written. No stage, commit, push or merge occurred. Route reference remains the read-only 7cada9d2e66af9806358f582bc8ea459321a6563 snapshot.

No material product decision remains open for this epic. Completed/tested V1, required route functionality and separate implementation authorization remain prerequisites. Actual device/HTTPS support, NSR dated mapping and threshold suitability are unresolved evidence gates assigned to the stories. Historical research validation and source freshness were not rerun or upgraded to current test evidence.
