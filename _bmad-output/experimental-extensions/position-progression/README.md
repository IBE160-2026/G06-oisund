# Position and stop progression — Posisjon og holdeplassprogresjon

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Status: preliminary V1.3.0 planning, 26 October 2026. Version number is a planning label, not an approved release commitment. Recommended first delivery: an opt-in, foreground-only estimate of the relevant/next stop occurrence on one user-confirmed dated trip. Manual anchors are protected when fresh and may later be reassessed using qualified measurements.

## Workspace and provenance

| Item | Verified value |
|---|---|
| Actual working directory / repository root | `D:/IBE160-plan-position-progression` |
| Branch | `codex/plan-position-progression` |
| Exact local main starting commit | `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed` |
| Starting subject | `feat(11.4): maintain planned notices from web or SMS` |
| Document area | `_bmad-output/experimental-extensions/position-progression/` |
| Remote, inspected only | `origin`: https://github.com/IBE160-2026/G06-oisund.git |
| Route plan inspected | `D:/IBE160-plan-complete-route-network`, `codex/plan-complete-route-network`, HEAD `7cada9d2e66af9806358f582bc8ea459321a6563` |

Branch/path were absent; created from the exact local commit without switching main or copying its uncommitted work. That initial setup performed no fetch, commit, push or merge. The research baseline was subsequently published at 854d038ec185aa8d75c27d91dcc1c9910a4ab6c8; the specification and this epic continuation remain local/uncommitted. Main and both other extension worktrees were read-only references; shared Git worktree registration is the intended setup change.

## Read next

1. [Current specification and fictional example](specs/spec-position-progression/SPEC.md), with behavior and route-interface companions.
2. [One epic and four proposed stories](epics.md), in recommended order PP-E1-S1 → S2 → S3 → S4.
3. [Scope and settled planning decisions](scope.md).
4. [Short technical research](research/technical-position-progression-2026-10-26/research.md), with source digests and document checks alongside it.
5. [Source map and authority](source-map.md).

BMAD Run uses [extension-local configuration](.bmad-runner/resolved-config.json) and [workflow settings](.bmad-runner/resolved-workflow.json). The epic continuation uses [verified local routing](.bmad-runner/epics-routing.json) and the installed bmad-create-epics-and-stories workflow. No global/shared configuration changed. Working notes are support material, not additional specifications.

## Continuation point

The latest user decisions settle Q1/Q2: manual recovery after interruption and anchor reuse within the same workday/shift, including midnight. [Decision register](specs/spec-position-progression/decisions.md) separates these from technical proposals and untested thresholds. [Technical addition](specs/spec-position-progression/technical-addendum.md) reuses the existing architecture and proposes only the necessary route/coordinate and anchor additions. The [fictional example](specs/spec-position-progression/fictional-example.md) covers the overnight handoff; it is not GPS evidence.

PP-E1 plans four slices: inspect route/start anchor → foreground progression/advisory correction → interruption/manual recovery → saved same-workday next-trip anchor. All remain proposed. [Document validation](specs/spec-position-progression/validation.md) covers links, requirements, chronology, safety/lifecycle boundaries and routing. No material product decision remains open for this bounded plan; device, coordinate and threshold qualification belongs to the stories.

Implementation must wait for approved V1 completion and testing, the required route functionality and coordinate qualification, then separate authorization. This task performs planning and document checks only: no product tests, implementation, live location collection, database or service changes, or changes to V1/other extension backlogs.
