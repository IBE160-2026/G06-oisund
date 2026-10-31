# Password management — experimental planning

2026-10-31. **Scope decisions recorded; technical plan remains draft and implementation is not authorized.** No version number is allocated. V1, including Ubuntu integration, remains the accepted baseline.

Start with [SPEC](specs/spec-password-management/SPEC.md), then its three companions. [Implementation plan](specs/spec-password-management/implementation-plan.md) records the owner's Q1–Q4 decisions and remaining operational details. [Qualification](specs/spec-password-management/qualification.md) separates future tests from checks actually performed.

Branch: `codex/plan-password-management`, based on fetched `origin/main` `5cee9e03d03d2c9c165c7f8fec64aa3e146959ab`. Independent local clone `password-management-planning`; the desktop worktree tool rejected the source repository subdirectory, so a separate clone was used. Existing checkouts, changes and branches were not switched, reset or cleaned. The automatic-notices branch was read only.

## Owner decisions — 2026-10-31

Initial users are Jonas and the course teacher. Jonas handles resets and administration. Administrative one-use codes and a separate password-management delivery are selected; both password flows require new login on all devices. Self-service email and opening the application to the public are outside initial scope. No commitment to public operation or round-the-clock support is inferred. These decisions do not approve implementation or every technical proposal.

## Established workflow and isolation

Read root AGENTS.md, CLAUDE.md and `.claude/skills/sesjonslogg/SKILL.md`. Follow the extension isolation pattern in `origin/codex/plan-automatic-notices` (`bmad-workflow.md`). Applied installed `bmad-spec` in headless express mode with slug `password-management`, its five-field template, append-only memory and two-pass document validation. This task is a bounded brownfield plan; no research/architecture/UX/build workflow is claimed executed.

The extension-local `planning/.bmad-runner` resolves core configuration and spec customization; its `{project-root}/../../specs` resolves inside this extension. Activation hooks, persistent facts and completion hooks are empty. Global BMAD files, V1 epics, sprint status, implementation artifacts and existing extension files are unchanged. Artifact prose follows configured English; session log, questions to the owner and proposed UI wording use Norwegian.

The spec and companions derive from `.memlog.md` plus cited inspected sources. Future answers must be appended to memory before re-derivation. Future architecture or story breakdown must remain extension-local with `PM-` identifiers; do not dispatch V1 stories. Review unresolved decisions and obtain separate implementation authorization first. No ready-for-dev, accepted or done status is assigned to product work.
