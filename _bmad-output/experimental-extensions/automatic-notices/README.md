# Automatic notices — planning workspace

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Established: 2026-10-26. Norwegian initiative name: **Automatisk avviksinnhenting**.
This is provisional planning, not approved implementation requirements or a promised part of the course submission.

Investigate whether automatically retrieved traffic/public-transport notices can help the driver identify potentially relevant disruptions for a planned workday. The extension belongs to the IBE160 driver assistant but has its own planning lifecycle. Approved V1 continues to use manually maintained notices.

## Workspace identity

- Branch: `codex/plan-automatic-notices`.
- Worktree: `D:/IBE160-plan-automatic-notices`, a sibling of `D:/IBE160`.
- Starting commit: `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed` — `feat(11.4): maintain planned notices from web or SMS`.
- Starting point: local `main` and locally recorded `origin/main` pointed to that commit; no fetch was performed.
- Document root: `_bmad-output/experimental-extensions/automatic-notices/`.

The names were unused before creation. Existing uncommitted work in the main workspace was read as reference, not copied. The checkout includes the V1 baseline for context; its active artifacts are read-only for this initiative.

## Documents

- [scope.md](scope.md): intended benefit, provisional boundary, dependencies and unanswered questions.
- [source-map.md](source-map.md): inspected project sources, authority, historical conflicts and local differences.
- [bmad-workflow.md](bmad-workflow.md): recommended next steps and explicit output isolation for later BMAD runs.

Only these planning documents were authored during establishment. No product implementation, migration, research run, test run, service operation, deployment, sprint change, commit, merge or push belongs to this task.

## Continuing safely

Start future sessions in this worktree and read these four files first. Recheck Git state and source versions, especially before using the newer 11.5/11.6 reference material. Keep all extension outputs below this document root. A branch does not prevent path collisions after integration: follow the routing rules in [bmad-workflow.md](bmad-workflow.md).

An implementation or course-scope decision requires a separate explicit authorization. This workspace grants neither.

## Current planning handoff — 26 October 2026

The completed [research report](research/technical-automatic-notices-2026-10-26/research.md), [specification package](specs/spec-automatic-notices/SPEC.md) and [single AN-E1 epic with four stories](planning/epics.md) now form the extension-local planning handoff. [Product decisions](specs/spec-automatic-notices/product-decisions.md) distinguish supplied planning scope from provisional defaults and later acceptance choices. [Document validation](planning/validation.md) records qualification/readiness limits. No pilot/product implementation or V1 acceptance follows from these files.

The canonical technical companion is technical-addendum.md; technical-notes.md is retained only as a superseded working draft. The separate route-network worktree is not an output destination for this initiative.


## Current short epic plan — 26 October 2026

[AN-E1 epic and four stories](planning/epics.md) now follow the completed research/spec. See [technical addendum](specs/spec-automatic-notices/technical-addendum.md), [provisional product decisions](specs/spec-automatic-notices/product-decisions.md) and [document validation](planning/validation.md). technical-notes.md remains a superseded working draft. No implementation or final approval is implied.
