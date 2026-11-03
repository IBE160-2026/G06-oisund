---
title: 'PM-E1 — v1.1.0 integration candidate'
type: chore
created: '2026-11-04'
status: in-review
route: dispatch
review_loop_iteration: 0
baseline_commit: b7af6b5ebbd1118e3c85fa164879ad68c4f86b4f
context:
  - final-readiness.md
  - operator-runbook.md
  - s4-evidence.md
  - ../planning/epics.md
  - ../../../../docs/evidence/o6-handover-20261103.md
  - ../../../../docs/evidence/v1.0.1-maintenance-20261104.md
---

<frozen-after-approval reason="Explicit owner authorization for autonomous integration and candidate preparation; no owner acceptance inferred">
## Intent
Resume implemented PM-E1 S1–S4 and qualify a v1.1.0 candidate incorporating v1.0.1 maintenance. Main15011042b1fe093becbe68177e6396e456b1f35f was merged in b7af6b5ebbd1118e3c85fa164879ad68c4f86b4f; both recovery CLI and maintenance functions/tests were preserved. Do not restart stories or overwrite historical evidence.

## Boundaries & Constraints
Keep own-password change, operator one-use recovery (including own account), all-session revocation and retained accounts/data. No email/admin dashboard/automatic ingestion. Only isolated synthetic data and local disposable runtimes. No real server/accounts/sessions/device/SSH/MFA, main merge, release/tag or deployment. Owner unavailable: record exact owner-dependent checks, never wait for dialogue or infer consent. Full O6 closure is not a blanket prerequisite; assess actual candidate changes against existing documented barriers. Parent handles commits/push/session log and independent final verification.

## I/O & Edge-Case Matrix
| Scenario | Input | Expected result | Failure |
|---|---|---|---|
| Integrated credentials | both existing password flows through updated gateway/API/PG | same accounts/data, revoked sessions/proofs, preserved Origin/CSRF/no-store | fail closed; static diagnostics, no secrets |
| Runtime barriers | updated images, nonroot/read-only/cap-drop/no-new-privileges, private_work NOSUPERUSER | CLI and app work within production-equivalent restrictions | do not relax production policy |
| Upgrade/restore | synthetic populated v1.0.1 pre015 and current snapshots | additive migration/repeat/restart, precise credential invalidation and old-hash handling while quiesced | no unauthorized production recovery claim |
| O6 interaction | fixed terminal CLI and merged helpers/gate | identify actual dependency/privilege/terminfo/ACL/FTS5 exposure changes | only concrete changed risks block; retain owner risk-acceptance scope |
| Owner field report | two separate bus days:24/42 then28, owner says worked | ordinary-operation owner report, date/device/version/functions unspecified | never label password acceptance |
</frozen-after-approval>

## Code Map
- `scripts/verify-password-s4.mjs`, `password-s4-probe.py`, `password-s4-gate.py`: existing unique-project qualification. Gate Dockerfile concatenation is broken by main's new multistage/pip-free build. Use actual runtime then test Dockerfile with GATE_IMAGE; production PG overlay now `deploy/ubuntu/Dockerfile.postgres`. Prior compatibility reference must be merged main1501104, not old5cee9e0. Keep prior source isolated via git archive.
- `deploy/ubuntu/compose.yaml`, `deploy/tablet/init-private-role.sql`: authoritative runtime restrictions and separate bootstrap/application roles. Adapt only synthetic harness; never its named production volumes/config/secrets. Capture assertions of actual user/cap/read-only/security settings and role privilege.
- `deploy/ubuntu/bussassistentctl.py`, `test_operations.py`, `test_gateway_maintenance.py`: merged source; fixed command/terminal/root/lock tests and maintenance preflight must coexist. Inspect concrete findings; do not invent host privileges or broad restore commands.
- `backend/app/recovery_terminal.py`: termios/fixed escape bytes, no terminfo lookup. O6 barriers and existing images/locks remain authoritative.
- `implementation/`: append new candidate evidence/manifest and current readiness links; retain original S4 manifests. `docs/evidence/`: factual owner field report.

## Tasks & Acceptance
- [x] Repair/reuse S4 harness for actual v1.0.1 images, gate build and production-equivalent restrictions/least-privileged app role; preserve reproducibility/secret-safe diagnostics and scoped shutdown. Capture exact source/image/build evidence.
- [x] Run focused harness checks and combined qualification; tests requiring root mocks run only in isolated containers with no Docker socket. Parent separately runs integrated103 backend/focused browser and maintenance/gate suites; avoid shared DB mutation lanes.
- [x] Inspect actual restore/rollback gap; prepare concrete reviewed future procedure within available primitives where possible. Do not implement a guessed credential policy/new administrative feature. Precisely retain any missing independent mechanism or owner prerequisite, distinguish compatible old code from migration guard authorization.
- [x] Write `v110-candidate.md` with main/merge identity, actual O6 impact, retained evidence vs new tests, failures/fixes, release prerequisites and short executable owner checklist. Update final-readiness/status/README/epic links without marking owner-dependent stories done.
- [x] Write `docs/evidence/owner-bus-use-reported-20261104.md`: first day lines24/42, second28; owner reports worked both days. Exact dates/device/appversion/tested functions not supplied. Report date only, no inferred password acceptance.

Acceptance: Given updated main, when candidate runs, then both password flows and maintenance boundaries remain verified on integrated sources. Given unchanged frontend/business sources, reuse applicable prior UI/legacy evidence with explicit scope. Given owner absence, all independent work proceeds and only specific personal/production prerequisites remain deferred. No production actions occur.

## Implementation Notes
No new product intent gap prevents integration. Footprint: qualification scripts, bounded fixes if demonstrated, candidate/runbook/status docs. Irreversible production operations excluded. Existing main merge was explicit user instruction, separate from this implementation baseline. Prior S1/S3 historical mixed-input/diagnostic incidents remain documented; select only synthetic tests, no credential-bearing traces/screenshots/raw logs.

## Spec Change Log

## Review Triage Log

All three context-free BMAD layers returned before triage. Review diff includes post-merge integration changes plus recovery-helper delta against main to inspect merge preservation. Blind floor:76932/1000=76.932kB; min(floor(sqrt(76.932)+1),10)=9. Eleven findings retained individually below.

| ID | Verdict | Evidence and disposition |
|---|---|---|
| B1 | medium | Verified `auth.provision`, recovery.resolve and app.manage sys.argv accept leading-hyphen names; outer helper alone rejects. Existing all-account compatibility defect exposed by integrated review. Bounded patch removes only startswith restriction and verifies fixed positional forwarding; no shell parsing/new option handling. |
| B2 | low | Windows Docker Desktop run passed; native Linux UID10001 cannot write ordinary host0755 scratch. Native Linux qualification was not performed. Patch explicit supported-host/precondition boundary rather than world-writable credential scratch or new privileged volume machinery. |
| B3 | medium | Docker runtime loop records PidsLimit but never compares it; missing setting would pass. Patch exact per-service limits. |
| B4 | low | Production init SQL creates role without grants; inspected current role is direct NOSUPERUSER but assertion is weaker than its least-privilege label. Patch BYPASSRLS/membership checks as bounded direct correction. |
| B5 | medium | Confirmed outer helper tests mock Docker while S4 tests inner CLI. No claim of actual SSH/outer-to-inner PTY qualification is justified. Preserve this concrete full-chain owner gate and name it in evidence; no host Docker socket or authentication bypass for simulation. |
| B6 | medium | Shared isolated network is different from production app/storage separation. Patch precise evidence boundary; production compose unchanged and no network-isolation equivalence claim. |
| B7 | medium | Separate production gate-runtime build not present in Compose image manifest. Patch its exact identity and tested overlay provenance. |
| B8 | false | Diff explicitly appended existing S2 recovery additions versus main for integration review; `git diff b7af6b5 -- deploy/ubuntu/bussassistentctl.py` was empty at review. No new product fix was needed for harness at that point. Clarify carried source; later B1 correction must be reported as new. |
| B9 | low | Parent checks/review were explicitly pending, not falsely marked complete. Add final exact commands/results/source links and task state as planned. No passing claim until results exist; rejected as a spec-only defect, evidence completion retained. |
| E1 | low | Same demonstrated native-Linux bind permission issue as B2; retain explicit Windows-only qualified boundary and native prerequisite. |
| V1 | medium | Preverified verification gap: actual service PID limits are not asserted. Patch same concrete assertion as B3; final combined run must execute it. |

Accepted bounded fixes re-engaged the same implementation agent. B5 remains explicit owner-dependent full-chain qualification; it is not presented as independently tested. No new restore policy or broader operator privilege inferred.

## Verification
Use unique task-owned Docker projects/images/volumes, no global prune. `node scripts/verify-password-s4.mjs` after patches. Preserve earlier evidence and publish sanitized new manifest separately. Verify source fingerprints, relative links, diff checks. Parent three-layer BMAD review precedes final commit/push. Physical/identity/handoff/SSH acceptance remains deferred.

## Parent final verification and independent completion

Parent read the actual integration/helper diffs, verified all11 triage rows, and inspected bounded patches. Final combined run4be993e0587f passed13 phases/20 scans/3 negative controls;148 source fingerprints match. Final27 mocked helper/maintenance tests passed0.099s; application103/backend,35 focused browser and33 gate tests remain valid because subsequent patch changed only helper forwarding and qualification assertions/docs. Reused legacy82 evidence is explicitly limited to unchanged sources. Reproduction and failures are in evidence/v110/parent-checks.md; final manifest is evidence/v110/runtime-parent-final.json.

Tasks checked here mean independent integration/preparation work only. Existing-deployment restore policy/interface and actual owner/device/SSH/handoff acceptance remain deferred in v110-candidate.md and deferred-work.md; no story/epic is marked done. Native Linux runner is explicitly unsupported pending correct task-state ownership qualification. No owner approval, O6 closure or release/deployment is inferred.
