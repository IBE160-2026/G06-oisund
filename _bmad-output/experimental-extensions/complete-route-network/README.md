# Complete Route Network — Fullstendig rutenettverk

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Status: preliminary planning foundation, established 2026-10-26. These documents are not approved implementation requirements or a promised part of the course submission.

## Purpose and relationship to the project

Explore integrating existing public transport services into the driver assistant: lines, route variants, directions/destinations, stops, ordered stop patterns and departures on specific operating dates. Later planning should establish how an imported shift activity can be linked to the correct concrete departure and stop pattern. The extension does not generate or optimize transport networks or staffing plans.

The approved course V1 remains governed by SCOPE-02 (2026-10-19), its revised PRD, architecture, UX and active backlog. Timetable enrichment, automatic ingestion and stop progression were deferred. This workspace reopens their planning only; it does not reinstate the superseded September requirements or change V1 acceptance.

## Workspace provenance

| Item | Recorded value |
|---|---|
| Planning branch | `codex/plan-complete-route-network` |
| Worktree | `D:/IBE160-plan-complete-route-network` |
| Main workspace, read-only reference | `D:/IBE160` on `main` |
| Explicit starting commit | `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed` |
| Commit description | `feat(11.4): maintain planned notices from web or SMS`, 2026-10-25 |
| Other extension reference | `codex/plan-automatic-notices`, `D:/IBE160-plan-automatic-notices`, same starting commit |

The chosen commit is the existing local main HEAD after accepted 11.1–11.4 work. No remote fetch or publication check was performed. Branch and target directory did not exist before creation. Main contains newer uncommitted project and product work, notably 11.5/11.6. It was read as reference and was not copied into this branch; see source-map.md. The branch's inherited V1 tracking therefore does not describe those newer local deliveries.

## Documents and reading order

1. [scope.md](scope.md): tentative capabilities, exclusions, dependencies and open questions.
2. [source-map.md](source-map.md): inspected project evidence, authority, local differences, research gaps and the proposed BMAD output contract.

The establishment originally produced these three documents. The later native technical Run is now complete: [research report](research/technical-complete-route-network-2026-10-26/research.md), with [evidence and checks](research/technical-complete-route-network-2026-10-26/README.md). Other future destinations in source-map.md remain reserved. Research completion does not approve the extension or resolve all qualification gates.

## Continuation boundary

Start future work in this worktree and read all three documents. Keep all extension outputs beneath this directory, including working memory and supporting research files. Confirm resolved paths before any workflow writes; the separate branch alone does not prevent conflicts after integration. Do not edit active V1 artifacts, global BMAD settings, other extensions or existing epic/story identifiers.

This establishment performed no product changes, database/service actions, full external research, data ingestion, tests, deployment, merge, push or commit. Future implementation and any change to the approved delivery boundary require a separate decision.



## Current P1 planning handoff — 26 October2026

[Specification](specs/spec-complete-route-network/SPEC.md), [decisions](specs/spec-complete-route-network/decisions.md), [seven-date manifest](specs/spec-complete-route-network/pilot-manifest.md), [technical addition](specs/spec-complete-route-network/technical-addendum.md), [CRN-E1/four stories](planning/epics.md), [isolation audit](planning/isolation.md) and [document checks](planning/validation.md) are the current short handoff. P1 line20/draft matching excludes P2/GPS/progression/notices. Implementation waits until V1 complete and tested for a while, then separate owner authorization. Research-era dates do not promise future live coverage; defaults remain provisional. Runner proof: planning/.bmad-runner/resolved.json. Stories remain draft/not approved despite publication. The user attributes the earlier detour to a wrong prompt in this chat; notice work remains preserved, not route requirements.
