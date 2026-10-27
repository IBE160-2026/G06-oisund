---
title: '12.1 and 12.2 local integration pending owner testing'
type: chore
created: 2026-10-27
status: in-review
route: dispatch
review_loop_iteration: 0
baseline_commit: b54246fdb4fc6cc6318c63b4705de4961586f41c
owner_acceptance: pending
context:
  - D:/IBE160/AGENTS.md
  - D:/IBE160/docs/evidence/12-1-retained-data.md
  - D:/IBE160/_bmad-output/implementation-artifacts/spec-12-2-repeat-a-fictional-assessment.md
---

<frozen-after-approval reason="Jonas explicitly authorizes completing both stories, synthetic tests, separate story commits and local merges before his acceptance test">

## Intent

Complete the integration of retained-data enforcement and the repeatable fictional assessment in local main, with executed actual API/PostgreSQL notice creation, replay and lost-response evidence. Preserve both implementations and all prior evidence. Make the combined application ready for Jonas to test at home; technical success never constitutes owner acceptance.

## Boundaries & Constraints

Always use isolated synthetic databases, loopback endpoints and fresh evidence. Keep stories in review/in-review and owner acceptance pending. Preserve independent account notice retention, original operation identity, lookup-before-retry, manual actions, unknown facts and no-login demo isolation. Record this exact sentence in both stories, status and session log: «Jonas har ikke gjennomført manuell/fysisk akseptansetest av Story 12.1 eller Story 12.2. Teknisk integrasjon og automatiske tester innebærer ikke brukeraksept. Begge avventer Jonas sin testing.»

Never push, deploy, change ordinary services/data, reset other projects, delete worktrees, weaken assertions, claim previous tests ran now, or mark stories accepted/done. Local merges are authorized. All original work remains on its branches.

## I/O & Edge-Case Matrix

| Scenario | Input | Expected behavior | Failure handling |
|---|---|---|---|
| Actual notice create/replay | Server-issued admission and unchanged command | One stored notice, original immutable receipt | Changed payload, foreign/unknown/expired ID denied |
| Actual lost acknowledgement | Server commits response discarded at transport boundary | Authorized lookup recovers original receipt; same-ID replay creates no duplicate | Preserve uncertainty until lookup; no substitute ID |
| Retention/isolation | Original day deleted; fictional reset executed | Independent live notice and private data survive | Expired retained resources inaccessible and cannot resurrect |
| Combined build | /demo, /, /private on isolated ports | Demo no network/GPS/persistence; actual paths use configured APIs | No fallback to ordinary services |

</frozen-after-approval>

## Code Map

- `compose.story122.yaml`, `scripts/verify-story122.py`: reuse actual fixture/reset/restart checks, but a fresh integration project and ports avoid existing task resources. Prior script deliberately defers the required notice checks.
- `compose.story121.yaml`, `scripts/verify-retained-data.py`: existing backend gate, safe preview lifecycle and disposable browser-test copies; root adapts these for integrated verification.
- `frontend/src/main.tsx`: merged demo dispatch/link and VITE_FICTIONAL_API must both survive. Private controllers already acquire notice admission and preserve pending identity.
- `frontend/tests/private-retention.spec.ts`, `private-notice-recovery-integration.spec.ts`: actual API-backed browser transport-abort coverage. Root executes affected suites and complete private regression gate.
- `backend/tests/test_account_notices.py`, `test_retained_data.py`: reusable real API setup, contracts, cleanup and retention tests. Keep production code unchanged unless an actual failure proves a defect.

## Tasks & Acceptance

- [x] `compose.story12-integration.yaml`, `scripts/verify-story12-integration.py` — implementation delegate owns these two files only. Build a new isolated project `ibe160-story12-integration`, frontend origin 15312, fictional API 18312, private API 18313, unique volumes/ignored password file. Mount backend and fixtures read-only. Include private test env markers matching existing guarded tests. Provide `up`, `verify`, `prepare` modes; refuse non-synthetic accounts and attach only matching compose project/config. Do not run services or tests from the delegate; root executes them.
- [x] The verifier uses actual HTTP/PostgreSQL to check fictional persistence/replay/conflict, restart and fictional reset isolation plus private notice admission/create/exact replay/altered replay/receipt lookup/lost response. Simulate lost response by sending the real request then closing the socket without reading, resolve via receipt polling, and prove one row and immutable original identity. Record honest per-check statuses, exits, source hashes and unique evidence; never serialize credentials or csrf/session cookies. On failure preserve evidence and nonzero exit. Preparation creates only a synthetic manual account and two line-20 days for 2031-01-02/03, with credentials stored only under ignored `.private-runtime/story12-manual-credentials.json` and no password output.
- [x] Root owns browser orchestration, combined build/tests, conflict documentation, status/README/test checklist, review triage, commits and final local main merge. The delegate must not edit other files, invoke nested skills/agents, commit, or merge.

Given the integrated code, when actual and browser checks run, then all required matrix behaviors pass with fresh evidence and no ordinary data mutation. Given a completed local merge, when Jonas opens the checklist, then setup/data/actions/expected results/limits are concrete and both stories still await his testing.

## Implementation Notes

No unresolved intent gaps. Only disposable synthetic data is mutated. Prior story commits are secured and both merged on the integration branch. Root resolved issues by union, selected the more comprehensive 12.2 epic context, kept both review statuses and the 12.1 API configuration. Existing frozen historical scope is preserved; this explicit new authorization supersedes its prior no-commit/no-merge limit.

## Spec Change Log

## Review Triage Log

## Verification

Root executes the fresh integration Compose runtime, full private backend suite, existing fictional API tests, production build, full private Playwright gate, demo gate and runner unit checks. Run fresh actual notice/replay/lost-response/reset verifier and prepare manual fixtures after tests. Inspect served bundle and runtime source identity. Preserve raw output and exact commands in a new report. Independent review follows implementation; owner testing remains pending.

### Integration review triage — 2026-10-27

| Finding | Verdict / route | Evidence and disposition |
|---|---|---|
| B1 current-date ending versus 2031 plan | false / reject | The checklist expiry step exercises account maintenance status, not overlap in the day reader. Notices are account-wide and maintenance has no plan-date matching prerequisite. Clarify that expected display is maintenance. |
| B2 prepare after manual plan deletion | medium / patch | Existing preparation requires exactly both dates; the checklist intentionally removes one. Provide additive re-preparation of missing synthetic dates, preserving existing plans and edits. |
| B3 credential file after provisioning | medium / patch | A file-write interruption loses the only password before rerun. Persist recoverable local credentials before provisioning and distinguish absent account from invalid existing credentials; never reset an existing account password. |
| B4 executed-copy identity | medium / patch | Ignored translated tests/config are absent from source manifest. Record their actual hashes and selection in browser evidence. |
| B5 stale generated tests | medium / patch | Persistent generated directory includes deleted originals on later runs. Use a unique owned run directory. |
| B6 fixture manifest | medium / patch | Regression source manifest omits consumed Eksempelfiler. Include fixture hashes. |
| B7 launch exception evidence | medium / patch | Subprocess launch exception bypasses evidence output. Always record evidence and failure type in finally. |
| B8 unbounded subprocess wait | medium / patch | Docker/test subprocesses can stall indefinitely. Bound them with explicit suitable command timeouts and record timeout status. |
| B9 reset fingerprint scope | medium / patch | Current reset fingerprint covers content/deadline of drafts/plans but omits lifecycle/outcome/selection/bus and other owned tables. Fingerprint full rows of relevant private tables before/after fictional-only reset. |
| B10 cleanup only on success | medium / patch | Failed verification leaves newly provisioned synthetic accounts. Cleanup only the invocation-owned accounts in finally; retain original failure and separately record cleanup failure. |
| E1 interrupted prepare | medium / patch | Independently confirms B2/B3; save recoverable provisioning state and resume missing dates while preserving existing plans. |
| E2 launch exception evidence | medium / patch | Independently confirms B7; record source/execution failure in finally. |
| V1 wrong-runtime refusal untested | medium / patch | Existing unit gate only imports old runners; matching-runtime evidence cannot detect deleted config/workspace checks. Add stubbed negative tests asserting refusal before Compose startup/database access. |

Root applies bounded runner/evidence patches and re-engages the original implementation delegate for its owned verifier. No change of user-facing scope or acceptance criteria is required. No retained product defect is identified by this review.

### Review reinspection

All three original reviewers reinspected the patches. Edge reviewer retained none. Verification reviewer detected and root corrected a false-positive negative test (the stub itself raised an accepted assertion); exact refusal messages and successful valid downstream mocks now distinguish each guard. Three mutation probes proved removing each config/workspace/volume check fails its specific test. Blind reviewer found missing executed-input files could still interrupt final evidence; root records null missing-input hashes and gate exit2, with a passed regression test. All29 runner tests pass. No review finding remains unresolved.

Additional root corrections: preserved the old fictional save keyboard order by placing the new demo link after the existing controls; actual keyboard/reload cases passed in the27-case fiktive browser gate. First integrated demo attempt used its old15222 allowlist in disposable copies; root also translates that endpoint to15312. Original assertions are unchanged. The27-case rerun was source-stable and passed. One intermediate27-pass run is historical only because the negative-test file changed concurrently; the final source-stable run supersedes it. Both original attempts remain recorded.

| Reinspection finding | Verdict / route | Evidence and disposition |
|---|---|---|
| V2 refusal-test false positive | medium / patch | Broad assertRaises accepted the downstream mock's own assertion. Exact boundary messages and successful valid downstream mocks now distinguish each refusal; all15 verifier unit tests pass and three guard-deletion mutation probes fail their corresponding test. Original reviewer reinspected and retained none. |
| B11 deleted executed input interrupts finalization | medium / patch | Reading a removed generated test inside finally could prevent evidence. input_hashes now records null missing files, preserves evidence and returns gate2; a direct deletion regression passed in the29-case gate. Original reviewer retained none. |
| N1 fictional save keyboard order | medium / patch | The added link before controls displaced the existing two-Tab save path. Moving the link after controls preserves the path without removing discovery. Both1440/768 keyboard-save/reload cases passed on the combined build. |
| N2 demo-copy origin translation | medium / patch | The demo's static-only allowlist used15222, so integrated navigation15312 was intentionally blocked. Translate that origin in disposable copies along with the other endpoints, retaining the zero-network assertions. Final27-case gate passed unchanged. |

| Executed regression finding | Verdict / route | Evidence and disposition |
|---|---|---|
| N3 integration API readiness absent | medium / patch | The479-case gate returned477 passes/2 failures, both recovery tests using compose start --wait. Unlike the original private Compose config, integration APIs lacked healthchecks, so revalidation could race startup. Added existing HTTP health probe to both isolated APIs, changed no assertions/product code. Recreated own services and all27 affected recovery cases passed unchanged; reviewer reinspected and retained none. |
