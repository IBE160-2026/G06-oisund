# Password management — experimental extension

2026-10-31. **Isolated implementation authorized and in progress; owner qualification and release remain pending.** No version number is allocated. V1, including Ubuntu integration, remains the accepted baseline.

Start with [SPEC](specs/spec-password-management/SPEC.md), then its companions and the [epic/story package](planning/epics.md). [Implementation plan](specs/spec-password-management/implementation-plan.md) records the owner's Q1–Q4 decisions and remaining operational details. [Qualification](specs/spec-password-management/qualification.md) separates future tests from checks actually performed.

Branch: `codex/plan-password-management`, based on fetched `origin/main` `5cee9e03d03d2c9c165c7f8fec64aa3e146959ab`. Independent local clone `password-management-planning`; the desktop worktree tool rejected the source repository subdirectory, so a separate clone was used. Existing checkouts, changes and branches were not switched, reset or cleaned. The automatic-notices branch was read only.

## Owner decisions — 2026-10-31

Initial users are Jonas and the course teacher. Jonas handles resets and administration. Administrative one-use codes and a separate password-management delivery are selected; both password flows require new login on all devices. Self-service email and opening the application to the public are outside initial scope. No commitment to public operation or round-the-clock support is inferred. These decisions do not approve implementation or every technical proposal.

## Established workflow and isolation

Read root AGENTS.md, CLAUDE.md and `.claude/skills/sesjonslogg/SKILL.md`. Follow the extension isolation pattern in `origin/codex/plan-automatic-notices` (`bmad-workflow.md`). Applied installed `bmad-spec` in headless express mode with slug `password-management`, its five-field template, append-only memory and two-pass document validation. This task is a bounded brownfield plan; no research/architecture/UX/build workflow is claimed executed.

The extension-local `planning/.bmad-runner` resolves core configuration and spec customization; its `{project-root}/../../specs` resolves inside this extension. Activation hooks, persistent facts and completion hooks are empty. Global BMAD files, V1 epics, sprint status, implementation artifacts and existing extension files are unchanged. Artifact prose follows configured English; session log, questions to the owner and proposed UI wording use Norwegian.

## Epic and story planning — 2026-10-31

[PM-E1 and four ordered stories](planning/epics.md) are implementation-ready specifications after document validation, with execution still unauthorized. Read the [technical contract](planning/technical-contract.md), [20-scenario coverage](planning/coverage.md), [validation](planning/validation.md) and [workflow/routing record](planning/workflow.md). Own-account recovery through independent SSH is explicit; no admin panel is needed. Updated origin/main is unchanged at the original baseline. V1 numbering/status remain untouched.

The spec and companions derive from `.memlog.md` plus cited inspected sources. Future answers must be appended to memory before re-derivation. Story breakdown now lives in planning/epics.md with PM-E1-S1..S4; future architecture or dispatch remains extension-local. Do not dispatch V1 stories. Review unresolved decisions and obtain separate implementation authorization first. Planning readiness is not product acceptance, permission to build or a sprint-status change.

## Implementation authorization — 2026-10-31

The owner subsequently authorized sequential implementation of PM-E1-S1 through S4 on this experimental branch in this isolated checkout, including synthetic tests, BMAD review, commits and push. This supersedes the historical planning-only authorization statements above; it does not approve release, production operations or new product decisions. origin/main was fetched and remains 5cee9e03d03d2c9c165c7f8fec64aa3e146959ab. Other branches/worktrees remain untouched.

Implementation evidence is tracked under [implementation](implementation/status.md). The owner is unavailable: identity/handoff qualification, actual tablet/PC acceptance and any new product decision are **utsatt – krever eier**. No physical tablet operation is authorized in this run. Technical dependencies may progress after their independent tests/review pass; mandatory owner checks still prevent marking the stories or epic complete.
