---
title: 'Integrate the reviewed password candidate into V2'
type: 'feature'
created: '2026-11-20'
status: 'in-review'
route: 'dispatch'
baseline_commit: 'df3fc940a7f97bd632e230ddb38c2fa45e8d2bfb'
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md', '{project-root}/CLAUDE.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

Bring the previously qualified password implementation into the V2 candidate based on the new local O6 merge, with code and evidence traceable to the password branch. The remaining personal and server acceptance stays pending.

## Boundaries & Constraints

Keep the O6 status and previous V1 architecture and PRD revisions. Integrate exactly the reviewed password delta from `15011042b1fe093becbe68177e6396e456b1f35f` to `29a77ff95cc7607b81c3351375771b6b23d2d1dd`. No real credentials, remote writes, production runtime, or edits to main or another checkout. Use the existing test recipes with isolated resources.

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
| --- | --- | --- | --- |
| Change password | Existing account and browser sessions | New password works on the same account and old sessions are invalidated | Rejected or ambiguous requests preserve the existing handling |
| Recovery | Current valid test proof | One redemption; latest SENDT behavior and 30-minute authority | Expired, replaced, revoked or used proof cannot establish new authority |
| Restore | Previously saved database with business data and old authority | Business data retained with the approved invalidation policy | Restore stays closed where the policy requires it |

</frozen-after-approval>

## Code Map

- Password source branch has the same pre-change product tree as V2. Its scope covers `.gitignore`, `backend`, `frontend`, `deploy`, `scripts`, and `compose.password-tests.yaml`. Supporting specifications and machine-readable evidence live under `_bmad-output/experimental-extensions/password-management`.
- Password source includes migration `015_password_recovery.sql`, separate operator and browser flows, and the most recent asynchronous handoff in `a14f515246a5d419277f1c2909fc85432c3ae79c`. Existing O6 deployment hardening comes from the common base.

## Tasks & Acceptance

**Execution**

- [x] Apply the product and password evidence delta with Git's three-way support to the V2 checkout only. Generate an ignored patch file using the full revisions. Keep existing branch logs separate for later reconciliation.
- [x] Verify every integrated product/evidence path matches the imported source tip, with no main change. Leave changes staged for the coordinator to inspect and commit. Do not commit or start services.

**Acceptance Criteria**

- Given the approved V2 base, when the scoped delta is staged, then all its product and evidence paths match the exact reviewed password branch and the O6 documents remain intact.
- Given isolated synthetic fixtures, when the coordinator runs backend, browser, gateway and restore checks, then results are recorded against this V2 tree and remaining device and operator acceptance stays open.

## Implementation Notes

The coordinator owns the Compose/Playwright environment and execution. Set the shell working directory explicitly to this V2 worktree. If Git index writes require approval, ask for the exact scoped apply operation with the shell escalation tool.

## Spec Change Log

- V2 imported the exact password source first. Integration then added the separate reviewed session, operator, restore and data migration fixes recorded in the handoff.

## Review Triage Log

- Patched identical-current password changes, late/reloaded credential replies, dispatch and login guards, legacy account-name handling, and restore interruption with identical business rows and changed sequence state. Incompatible restore schemas and mount paths fail closed.

## Verification

- Real PostgreSQL, the isolated browser suite, networkless Ubuntu tests and the registered physical-PG marker verifier cover the technical changes. Personal proof delivery and redemption, production-like Ubuntu operations and owner acceptance stay open. [Integrated verification](../../docs/v2-handoff.md).
