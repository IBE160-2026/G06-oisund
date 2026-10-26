# Source map and baseline reconciliation

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Inspected: 2026-10-26. Paths below are repository-relative unless an absolute path is given. Main-workspace references mean `D:/IBE160`; committed baseline means `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed`. Inspection covered relevant text/sections and Git differences, not an exhaustive product-code audit or external source investigation.

## Instructions and tooling inspected

- No `AGENTS.md` was found in the original repository, including hidden paths searched excluding Git/dependencies; neither `D:/AGENTS.md` nor repository-root `AGENTS.md` exists.
- `README.md`: SCOPE-02 project state, local fullstack/private boundaries and limitations. Local changes add 11.5/11.6 delivery information.
- `_bmad/config.toml`, `config.user.toml`, `custom/config.toml`, `custom/config.user.toml`: English documents, Norwegian conversation; standard output paths. The merged config was checked with the installed resolver.
- `_bmad/bmm/config.yaml`: legacy workflow config still points at active V1 planning/implementation areas.
- `_bmad/_config/bmad-help.csv` and `.agents/skills/bmad-help/SKILL.md`: installed routing and sequencing guidance.
- `.agents/skills/{bmad-deep-recon,bmad-spec,bmad-architecture,bmad-create-epics-and-stories}/SKILL.md` and their `customize.toml` files: output/workspace contracts inspected for later planning.
- `bmad-deep-recon/references/draft.md`, `bmad-create-epics-and-stories/steps/step-01-validate-prerequisites.md` (output-related instructions), and `_bmad/scripts/resolve_config.py`: confirm research workspace and fixed epic destination. These workflows were inspected, not executed.

## Decision and project sources

| Source | Current interpretation |
|---|---|
| `_bmad-output/planning-artifacts/sprint-change-proposal-2026-10-19.md` | Adopted SCOPE-02, especially S02-A/B/C/G. Manual navigation, manual line/date notices, online saving and local fullstack delivery govern. Automatic retrieval and precise trip/stop relevance are deferred. The earlier statement that manual entry cannot replace automatic retrieval is explicitly superseded. |
| `planning-artifacts/prds/prd-IBE160-2026-09-21/prd.md` under `_bmad-output/` | Active course-V1 section, FR-12–14 and notice acceptance semantics: manual records, uncertainty, separate timestamps, no automatic source/version lifecycle. The later historical divider prevents earlier mandatory language from reactivating scope. |
| `planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md` | Backend authority; React/TypeScript, FastAPI, PostgreSQL; ownership/revisions/retention; no private persistent browser cache. Old AD-7/8 transit/automatic ingestion is deferred. New integrations require explicit product/architecture reconsideration. |
| `planning-artifacts/ux-designs/ux-IBE160-2026-09-22/DESIGN.md` and `EXPERIENCE.md` | Current spines and 24–25 October owner refinements govern separate upload/editor/day/activity screens, retained proposals, explicit lifecycle, manual Day/Night and IR-01 readability/focus. Selection is not GPS location/completion. Local reader refinement separates reader from maintenance and preserves uncertainty/recovery. |
| `planning-artifacts/epics.md`, `story-drafts/story-v1-14.md`, `story-v1-15.md`; `implementation-artifacts/sprint-status.yaml` and `epic-11-context.md` | Active backlog is epics 9–12, 20 stories. Epics 9/10 and 11.1–11.4 accepted; local 11.5/11.6 are review with owner acceptance pending. Epic 11 remains in progress, Epic 12 backlog. Planning copies and old acceptance wording alone do not prove delivery. |
| `implementation-artifacts/epic-9-retro-2026-10-21.md` | Historical verdict remains rejected; later accepted corrective work is recorded separately. Preserve account identity, operation expiry and honest evidence. Do not reinterpret the historical verdict as current unfinished repairs. |
| `implementation-artifacts/epic-10-retro-2026-10-24.md` | Accepted with open items. Subsequent acceptance records A1–A3 done; theme/device qualification remains open. Preserve source facts and independent expected examples. |
| `implementation-artifacts/epic-11-retro-2026-10-26.md` — main workspace only | Preliminary draft, not final acceptance. Highlights representative SMS/web input, exact line/date semantics, source checks separate from reads, reachable recovery, and unqualified physical-device/remote access. It does not close 11.5/11.6 or authorize Epic 12. |
| `planning-artifacts/archive/pre-scope-02-2026-10-19/README.md`; earlier proposal `sprint-change-proposal-2026-09-27.md` (header); UX `reconcile-prd-addendum.md` | Historical context. Old 80-story plan, automatic Svipper/GPS/offline requirements, TIME-01 mechanisms and 43-screen gallery are not active V1 requirements. Do not use older reconciliation assertions as precedence over SCOPE-02/current spines. |

Table paths abbreviated as `planning-artifacts/` and `implementation-artifacts/` are beneath `_bmad-output/`.

## Main workspace versus branch baseline

Git initially had only local `main` at the chosen commit and one worktree. The new branch/worktree did not exist. The main workspace had 29 modified tracked files plus untracked 11.5/11.6 specifications, source/test files, delivery evidence and a preliminary Epic 11 retrospective. No stash, reset, cleanup, commit or copy of that work was performed.

Material differences:

- Baseline includes accepted 11.4 web/SMS notice behavior. Local architecture and PRD wording catches up with optional URL/source description, short/deep text and explicit selected/all-line scope. Treat the older mandatory-link wording as stale relative to accepted 11.4; this establishment does not edit V1.
- Baseline tracks 11.5/11.6 as backlog. Local sprint/story/epic records mark both review, with manual owner acceptance pending; their implementation/evidence is not present in this checkout.
- Local EXPERIENCE adds a separate reader, exact line identifiers, independent line and planned-interval/date filtering, all-line candidates, gap/midnight/DST handling and qualified empty/unavailable states. These are reference inputs, not automatic matching approval.
- Local README/context/development log and product/test changes accompany those deliveries. The new retrospective is preliminary and uncommitted.
- Older planning statements about pending fixture qualification or historical UI acceptance are not current implementation evidence. Use current delivery/acceptance records when planning resumes.

Reconcile a later committed V1 baseline explicitly before specification/implementation. Do not assume a future merge will import these references or settle contradictions. Refresh this map with commit/path/status evidence rather than copying the main workspace wholesale.

## Research still outstanding

No provider documentation, feed/API, licence, live coverage or sample external notice was verified here. Later research must establish source access/terms, real coverage, stable identifiers, validity/update/withdrawal semantics, line/stop/direction mapping and source-outage behavior. Then qualify representative examples and manual-record coexistence. Provider names in historical plans are hypotheses, not verified integrations.
