# Epic/story planning validation — 2026-10-31

**Verdict: implementation-ready specifications for PM-E1-S1…S4, in order, after separate implementation authorization.** No unresolved product decision blocks S1. S2/S3/S4 have explicit prior-story dependencies; readiness does not mean they can run before those are met. Real operator handoff and identity/contact qualification are pre-use/release gates, not silently accepted facts. No software was implemented or tested by this planning task.

## CE validation results

| Check | Result / evidence |
|---|---|
| Prerequisites and scope reconciliation | PASS: existing SPEC/companions and explicit owner decisions provide extension requirements; parent PRD/architecture/both UX spines supply inherited constraints. Own-account SSH recovery is mandatory; dashboard/email/public registration excluded. |
| Updated main | PASS: fetched origin/main unchanged at 5cee9e03d03d2c9c165c7f8fec64aa3e146959ab; no source diff from initial baseline. Existing planning HEAD matched remote before changes. |
| Numbering | PASS: active V1 9–12 retained; AN-E1 extension precedent used for new PM-E1/S1–S4. No assumed free V1 number, no sprint-status or dispatcher modification. |
| FR coverage | PASS: PM-FR1–7 mapped to epic/stories/ACs. CAP-1–3 preserved. |
| NFR/UX coverage | PASS: PM-NFR1–5 and PM-UX1–4 mapped to explicit ACs; parent 58px/IR-01 replaces earlier generic 44px minimum. No new theme/profile system. |
| Scenario coverage | PASS: all PM-A1–20 mapped in coverage.md, including code state/account races, operators, stale login, offline/unsaved state, migration and secret logging. Email/link-only scenarios correctly excluded. |
| Architecture | PASS: existing stack/CLI/auth/migrations/private wrappers reused. No starter service or all-tables-upfront story; proof schema belongs to S2. Shared authorization correction belongs inside the first complete password-change slice. |
| Story quality/size | PASS: four bounded user/operational outcomes with Given/When/Then ACs, tasks, files, tests, docs and completion evidence. S1 is the largest due to required locking regression; no unrelated auth redesign. S2 proves operator lifecycle independently; no end-user recovery completion claimed before S3. |
| Dependency and file churn | PASS: S1 uses V1; S2 uses S1; S3 uses S1/S2; S4 integrates S1–S3. One epic avoids repeated competing auth epics. No automatic-notice dependency. |
| Operational readiness distinction | PASS: S2/S4 must qualify actual capture-free terminal and contact/identity process. SSH loss/outer Access loss/operator absence covered without inventing a second administrator or SLA. |
| Release boundary | PASS: final qualification and owner acceptance precede a separate release/deploy decision. No version number, merge, production operation or release is performed or implied. |

## Review findings resolved before finalization

1. Old PM-1…PM-4 packages did not give independent end-to-end change value; replaced with PM-E1-S1 own change (including shared security), S2 operator lifecycle, S3 redemption, S4 qualification, with backward-only dependencies.
2. Parent UX starts with 58px controls and IR-01 measurements; reconciled the initial plan's generic 44px floor and mapped actual rendered checks to S1/S3/S4.
3. Earlier version-column language left competing concurrency mechanisms; selected a concrete engineering proposal using account-first gates and locked current-hash verification, avoiding an unnecessary migration. Alternate optimization requires a locked version/hash recheck, not a new owner decision claimed as approved.
4. “Terminal display” alone does not prevent recording. Added refusal of redirects/noninteractive execution, no stdout/stderr secret output, preflight for transcription/session capture and interrupted-handoff revoke/reissue. Actual path qualification remains mandatory before live issuance.
5. Existing app mutation wrappers can recheck a session after a successful self-revoking command; S1 tasks explicitly prevent misclassifying committed success as failure. Lost-response handling remains uncertain, without replaying secrets.
6. Original unanswered Q1 wording included own-account recovery despite the user's clarification. Updated the plan/overview to make it explicit; only concrete operational qualification remains. Technical TTL/limits remain labelled engineering defaults, not owner-approved product policy.

## Remaining matters

- No new product decision is required to begin the first story once the owner authorizes implementation.
- Before real use, Jonas must confirm the practical identity/contact and safe handoff procedure. If safe terminal output cannot be qualified, S2/S4 are blocked for operational acceptance; do not silently add a web admin surface or email instead.
- During implementation, prove the proposed lock protocol and bounds through real concurrent PostgreSQL/API tests. Failure requires correcting the story implementation/design, not claiming planning validation is execution evidence.
- Before delivery, pass the full matrix, isolated migration/restore/rollback, actual device checks and owner acceptance. These are planned tasks, not already passed gates.

Structural/link/coverage checks are recorded in validation.json. Two document-review passes covered coherence and preservation of the user request; no independent-agent review or security certification is claimed. Workflow/menu adaptation is recorded in workflow.md.
