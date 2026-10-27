# Story 12.1 implementation plan

Base: `0bae54833f38dc3dbf041d54c324c220618c21da`; branch `story/12-1-retained-data-boundary`; worktree `D:/IBE160-story-12-1`.

## Execution contract

All writes and commands belong to this worktree. Sandbox cannot read/execute the existing WinGet uv; read-only unsandboxed checks verified uv 0.12.10, SHA256 A8BF95637BA520491DE06713D718A55B90F18D127980B9531FD8FC5A8E99DC1D. Exact required Build renderer then succeeded. No global PATH/security/ACL changes. Use task-scoped commands only, requesting tool escalation where necessary. Do not rerun the Build renderer or invoke a nested Build workflow.

Owner authorizes autonomous specification, implementation, tests and review; no intermediate approval. No staging/commits/push/merge, even logs. No ordinary services/data or other worktrees. English product/evidence docs, Norwegian session log/user communication. Root handles final logging/review. Subagent should implement and verify all spec tasks except final root review/log. Return incomplete checks honestly. Do not create additional agents while implementing.

## Decisions and retrospective routing

Accepted corrected 11.5 specification overrides old 12.1/PRD shorthand about associated notices: day expiry removes day outcomes/commands, never independently retained account incidents. Seven days after effective notice ending remains authoritative. No legacy grace removal.

E11-A6 implement deterministic extension crossing valid_until after initial validation and delayed-read retention tests. E11-A7 carry SMS/no URL, shared link, long multiline/all-line and two-day/original-parent-removal expectations from accepted tests. E11-A8 capture process exit/UTF-8 logs, per-run hashes and isolate synthetic data. E11-A11 fix timer overflow with bounded rescheduling without changing lease. E11-A12 map identity/manual/terminal/receipt invariants to named executed tests. A1–5 remain unrelated recovery/focus/time-presentation followups; A9/A10 and E10 theme/device work remain parallel/deferred and are no prerequisite to isolated privacy verification. Existing notice terminal-abandonment behavior must survive.

## Implementation order

1. Server-issued notice creation admission, additive migration 014, cleanup. POST `/notice-operations` with empty body returns `{operation_id, expires_at}`. New `/notices` create must reference a live owned admission. Known accepted receipt replays continue before admission validation. No unknown-ID auto issuance. Bound unused admissions per owner (200) and expiry at issuance+7d. Associate accepted admission with notice or delete after acceptance if accepted receipt authorizes retries; do not keep payload indefinitely. Both initial and final acceptance guard required against crossing admission expiry. Purged/unknown original UUID remains denied. Edit/check/end existing resource authority unchanged. Existing accepted and legacy receipts remain immutable and recoverable under own notice retention.
2. Frontend obtains and validates admission before preparing create command. Issuance failure keeps local proposal and enables explicit retry, sends no create. Once create may have dispatched, retain original operation ID, use existing lookup protocol. Add tests for lost issuance response, expired admission, lost create receipt, and same-command retry.
3. Final read guards for drafts/detail/lists and notices/detail/lists/reader: final session/plan authorization then fresh DB timestamp/filter. Projection time must correspond to final captured DB instant. Repeat single-resource authority after expensive final validation. Strengthen stale-list test rather than deleting it; retain existing no invalid server_now/payload consistency checks.
4. Clamp/recheck long expiry timers (PrivateAccess and draft if needed); browser extreme clock regression plus existing expiry/Back guards.
5. Tests cover complete lifecycle and metadata cleanup, no sliding deadlines, late writes/reads, notice replay after early-end purge with future validity, independent original-day deletion, ownership/admission cap and absence of raw originals. Originals currently only BytesIO and spawned process; preserve that design unless execution reveals defect.

## Isolated verification

Use dedicated Compose name `ibe160-story121-tests` (private) and optionally `ibe160-story121-demo` (fictional). Reserve private API 18121, frontend 15121, fictional API 18122; verify free before use. Unique project volumes/network. Database name/user stay `private_work` as guarded application contract, in a brand new isolated cluster; never point to ordinary database. Secret generated only under this worktree `.private-runtime`. Test guards expect PRIVATE_TEST_PROJECT=ibe160-private-tests marker independently of actual Compose project. Host backend tests use container execution with PRIVATE_TEST_API=http://private-api:8000 and fixtures read-only mounted from worktree Eksempelfiler. Do not use scripts/verify-private-drafts.py orchestration because it stops ordinary API. New isolated runner can reuse safe assertion logic only.

Existing frontend hardcodes API 8001 and tests hardcode 5173/8001. Add optional VITE_PRIVATE_API and VITE_FICTIONAL_API build values with existing defaults. For tests use task-only local Playwright config/browser routing and environment-driven shared helper API/compose parameters, preserving production defaults. All independently hardcoded fixtures/routes need consistent isolated adaptation or use task-only routing that rewrites browser API requests plus test API constants. Never bind ordinary ports. Use process-local env only.

Run full backend suite (all currently covered 421 tests plus additions) in isolated private image with fixtures; build frontend; targeted relevant browser suite includes new retention, access/import, crossday and original-command recovery. Prefer new root runner capturing subprocess exit and UTF-8 log via Python, not PowerShell stream redirection. Preserve source hashes, no private payload in committed evidence, historical renders untouched (archive fresh captures under tmp or 12-1). Startup/restart and repeat migrations on synthetic state must preserve live records/immutable receipts and purge due rows. Stop only this task's services after verification unless manual handoff needs them; leave volumes for acceptance. Do not delete any other resource.

## Integration and handoff

Document migration 014 plus POST /notice-operations prerequisite and helper changes for 12.2. Production defaults unchanged; code not deployed to ordinary services. Root reads diff, runs required independent review, fixes retained findings and checks matrix coverage before status in-review/review. Owner acceptance remains pending. Final evidence includes exact source/build hashes, commands/counts/failures, limits, manual steps at isolated ports and session log without commit per explicit user constraint.
