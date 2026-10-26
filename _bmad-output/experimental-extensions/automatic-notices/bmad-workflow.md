# BMAD continuation and output isolation

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

This is a proposed continuation, not workflows already run or approved implementation requirements. No BMAD configuration or active V1 artifact was changed during establishment.

## Recommended sequence

1. In a fresh context in this worktree, use **[RS] Deep Recon**, `bmad-deep-recon`, technical type, to frame a bounded source-feasibility decision. A Draft research brief is a useful first deliverable; agree research mode and effort before a full Run. Investigate access/terms, real coverage, representative payloads and minimum matching data. Keep project hypotheses separate from verified external evidence.
2. Use **[SPC] Spec**, `bmad-spec`, after evidence exists, to describe the smallest useful experiment and explicit non-goals. Include stop conditions and uncertainty; do not label it an approved V1 requirement.
3. Use **[CA] Architecture**, `bmad-architecture`, against that extension spec and the read-only parent spine. Preserve inherited decisions; surface conflicts before making a new ingestion/storage boundary. Re-adopt the extension spine as a spec companion.
4. When requirements/architecture are sufficiently settled, use `bmad-spec` Story Breakdown for extension-local `stories.yaml`. Keep identifiers in an extension namespace, e.g. `AN-...`, and retain the installed schema. Do not allocate new V1 epic/story numbers or feed these stories to the V1 dispatcher.

The catalogue also offers **[CE] Create Epics and Stories**; its collision needs special handling below. Sprint planning and Build are outside this establishment and are not the next action.

## Destination contract

Let `E = {project-root}/_bmad-output/experimental-extensions/automatic-notices`, with `project-root = D:/IBE160-plan-automatic-notices`.

| Later artifact | Explicit destination |
|---|---|
| Research brief/imports/digests/report/memlog | `E/research/<research-run>/` |
| Spec kernel, companions, memlog and eventual stories | `E/specs/spec-automatic-notices/` |
| Extension architecture spine and its memlog | `E/specs/spec-automatic-notices/architecture/` |
| Optional dedicated epic planning | `E/planning/epics.md` and extension-only story area |

These are reserved paths, not completed documents or pre-created research runs.

## Installed routing controls and limitations

- **Deep Recon:** `workflow.research_output_path` defaults to `{planning_artifacts}/research`; set its resolved value to `E/research` before activation, plus an initiative-specific `run_folder_pattern`. Its SKILL.md explicitly supports forwarded activation with pre-resolved fields. Confirm the actual `doc_workspace` is inside E before writes.
- **Spec:** `workflow.spec_output_path` defaults to `{output_folder}/specs`, `run_folder_pattern = spec-{slug}`. It writes `SPEC.md`, companions, `.memlog.md` and optional `stories.yaml` in that folder. Same slug resumes/updates in place. Bind the output path to `E/specs` and slug to `automatic-notices` before writes. An input-file path is not an output-path override.
- **Architecture:** `workflow.spine_output_path` defaults to `{planning_artifacts}/architecture`; its folder pattern normally uses project/date. Bind the output path to the extension spec folder and pattern to `architecture`, or another unique extension-only folder. Forwarded activation is explicitly supported. Parent AD IDs remain stable/read-only; extension decisions must be qualified by their document, never silently override V1.
- **Configuration caveat:** the central resolver has no general per-run output-override flag. It merges four TOML layers. Skill defaults expose output keys through `customize.toml`, and persistent overrides live under shared `_bmad/custom/`. None were installed here. Spec does not document the same forwarded-activation shortcut as Deep Recon/Architecture. A prompt containing an output path is therefore not proof that all workflows will honor it.
- **Safe fallback before a future run:** resolve the installed workflow and explicitly bind/verify every write destination. If the workflow cannot accept an invocation-scoped binding, prepare an extension-local, isolated planning runner root under E containing only the required BMAD tooling/config and a routed input set. Its resolver root and every planning/implementation/output path must stay under E; reference parent sources read-only. This is a later setup option, not an existing runner or a new supported CLI flag. Inspect hooks and hardcoded paths before running; do not run the default workflow and move files afterward.
- **CE collision:** its SKILL.md still loads `_bmad/bmm/config.yaml`; the first step initializes `{planning_artifacts}/epics.md`. The customization surface has hooks/facts but no dedicated epic-output key. Unmodified activation here targets V1. Prefer spec-local Story Breakdown; if CE is needed later, first isolate and verify both the legacy YAML and central-resolver destinations in the extension-local runner. Merely changing a TOML variable in the conversation is insufficient.
- **Other flows:** PRD/UX/catalogue scans and sprint/build dispatch may discover active V1 documents or use fixed tracking paths. Do not invoke them against this initiative until their inputs, outputs, hooks, companions and status writes are explicitly routed. Never use the inherited sprint-status file, whose story location points to the main workspace, for extension work.

Before each future run, inspect current Git status, resolved configuration/customization and the final absolute destination list. Scope discovery to extension inputs; whitelist parent references. Check the resulting diff contains only E paths. Keep any needed runner configuration inside E, so integrating planning files cannot alter global BMAD behavior or active V1 documents.

These controls must survive later integration: preserve the extension directory and its labels, and review the actual paths in the diff. A branch isolates concurrent editing; it does not isolate shared filenames after merge.
