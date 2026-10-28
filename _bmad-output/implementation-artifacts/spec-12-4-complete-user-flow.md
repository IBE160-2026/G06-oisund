---
title: '12.4 Verify the complete user flow (V1-19)'
type: chore
created: 2026-10-28
status: in-review
route: dispatch
baseline_commit: c3e5d66a7d9faa9af19a58c6002538610c163352
owner_acceptance: pending
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="Owner explicitly authorized complete autonomous implementation, review and push in the invocation">

## Intent

**Problem:** Accepted 12.1–12.3 and mobile upload need repeatable verification as one real browser/API/PostgreSQL journey, rather than disconnected simulated examples.

**Approach:** Add independently specified synthetic journeys, reuse relevant regressions and record exact executed outcomes/builds. Correct concrete defects within existing contracts; leave manual acceptance pending.

## Boundaries & Constraints

**Always:** Use branch `story/12-4-complete-user-flow` in its own worktree from freshly fetched main. Use synthetic accounts, independent expected facts, dedicated loopback ports15324/18325/18326 and project/database/volumes `ibe160-story124-tests`. Preserve mobile bounded byte reading and access restoration in either event order. Distinguish actual integration, fault injection, desktop automation, viewport emulation and physical testing. Keep failed attempts and precise source/build identity.

**Never:** Touch active website, tunnel, owner records, ordinary database or existing assessment stacks. Read or publish private originals. Infer acceptance or start12.5. Mock APIs in the successful full journey or use parser output as the sole oracle. Change product contracts without clarification. Merge main.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Real journey | Supported synthetic PDF, explicit correction/save | Independent dates, source/duty/trip facts; manual bus; saved reopening; manual selection/start/outcomes/notices/closure/reload | No automatic import save or inferred completion |
| Documents | Two synthetic documents, midnight/unknown fields | Separate identities/drafts/days; source facts retained alongside corrections | Unresolved classification/time blocks confirmation until resolved |
| Save integrity | Competing revision, lost accepted reply, same operation retry | Proposal retained, conflict explicit, original recovery creates exactly one effect | HTML/errors never establish saved state |
| Notices | Multi-line, partial validity, separate incident, ending boundary | Exact line/date scope; unknown source/check stays unknown; no revival | Retain dirty editor through tab hide/restore and safe navigation |
| Import failures | Unsupported input, interrupted access/read/transport/server | Confirmed work preserved; bytes unchanged on successful upload | Distinguish local read/access/transport/parser/response errors |
| Privacy/lifecycle | Foreign account, logout, switched/expired session, data expiry | Deny access/replay, clear private UI, no resurrection or persistent browser data | Renewed login never renews data lifetime |
| Durability | End/abort, reload and actual API/database restart | Fixed terminal recap with explicit/unknown outcomes; notice lifetime independent | No resume or duplicate closure |

</frozen-after-approval>

## Code Map

- `frontend/tests/private-owner-import.spec.ts`, `Eksempelfiler/Fasit-testskift.json`, `Testskift-A.pdf` through `E.pdf`: existing independently authored synthetic documents/expected facts; C crosses midnight. Reuse without altering oracle to match parser.
- `frontend/tests/private-activity-helpers.ts`: synthetic account lifecycle, API posting, setup and navigation helpers. Hardcoded8001/5173/project/file need disposable translations.
- `frontend/tests/private-notices.spec.ts`, `private-outcomes.spec.ts`, `private-recovery.spec.ts`, `private-retention.spec.ts`: actual integration and controlled fault patterns to reuse. Existing screenshots must be redirected to new evidence paths.
- `frontend/tests/tablet-transport.spec.ts`, `playwright.tablet.config.ts`: mobile boundary regressions use mocks and fresh tablet build; supplement, never substitute for actual journey.
- `scripts/verify-story123.py`, `verify-story12-integration.py`, `verify-story122.py`, `prepare-story123-tests.mjs`, `compose.story123.yaml`: isolation guards, real verification, source manifest and build identity patterns. New tooling owned by investigation agent; other implementation must not edit these new tooling files concurrently.
- `frontend/src/PrivateAccess.tsx`, `PrivateImport.tsx`, `pdfUpload.ts`, `PrivateDrafts.tsx`, `PrivateNotices.tsx`: actual access/import/provenance and dirty-editor behavior. Preserve existing authority and recovery contracts.

## Tasks & Acceptance

**Execution:**
- [x] `frontend/src/PrivateBus.tsx`, `frontend/src/useWorkdayResource.ts`, `frontend/src/PrivateActivitySelection.tsx`, `frontend/tests/private-current-adoption.spec.ts`: verify the known E11-A2 second-change race, and correct confirmed stale comparison adoption within existing current-authority/proposal-preservation contracts.
- [x] `compose.story124.yaml`, `scripts/verify-story124.py`, `scripts/prepare-story124-tests.mjs`, `frontend/playwright.story124.config.ts`: isolated reproducible actual runtime, fresh frontend build, raw evidence and effective API identity (tooling agent).
- [x] `frontend/tests/complete-user-flow.spec.ts`: independent full journeys and focused integration gaps, including real browser tab switch during dirty notice entry; fix any demonstrated existing-contract defects.
- [x] `docs/evidence/12-4-handoff.md`, `docs/story-12-4-manual-testing.md`: requirement/test matrix, actual expected/observed results, build/runtime identity, errors/fixes/limits and concrete remaining acceptance.
- [x] `_bmad-output/implementation-artifacts/sprint-status.yaml`, planning story/epics status and session logs: in-review/pending acceptance; work and log-only commits separately; push authorized branch.

**Acceptance Criteria:**
- Given synthetic documents and independently authored expectations, when the real journey executes, then source identity, calendar dates, corrected/manual/unknown facts, saved selection, notices and terminal recap match those expectations (FR1–6/10–14/17–22, AC01–08).
- Given retries, concurrent edits, loss of reply and access/retention boundaries, when commands/read/replay occur, then owner, revision, single-effect and fixed expiry invariants hold (NFR2/3, AC07/09).
- Given a dirty notice, when another browser tab receives focus and the original tab regains authorized access, then editing resumes with its unsaved proposal intact and no automatic save (FR20).
- Given final verification, when evidence is delivered, then actual API/PostgreSQL and mobile mock boundary results are separately identified with exact build/source/commands; device/manual checks remain explicitly pending (NFR4, AC11/12).

## Implementation Notes

- Fresh fetch verified origin/main at baseline above, including mobile correction `c0e809f6cd350c2661979557269d2ecc81f3dabd`. Worktree began clean; no prior12.4 work existed.
- User's explicit execute-to-review-ready instruction supersedes the generic workflow's intermediate approval checkpoint and no-push default. Product scope is approved; no unresolved intent gap or irreversible production operation is required.
- Executed455 backend tests,74 real HTTP/PostgreSQL checks,32 isolated mobile boundary cases,201/202 selected regressions followed by56/56 complete affected import/journey/demo cases. The sole broad failure was a stale pre-mobile-fix response-error expectation; assertions now distinguish response failure and forbid adoption/saving. Those gates preceded the focused E11-A2 frontend correction. Exact commands, source hashes, failures and limits are in the handoff.
- Actual tab blur/focus is verified with browser focus emulation disabled. This runtime supplies no native hidden/visible events; only C adds explicitly labelled lifecycle emulation using actual auth. A is a pristine real journey, including PostgreSQL/API restart and saved recap/selection. Physical/manual acceptance remains pending.
- Isolated additive preparation and source/build/runtime audit passed; only own frontend15324/APIs18325/18326 are used. The23 pre-existing container IDs/images/ports remain unchanged. No operational database or tunnel was modified.
- Root source review found comparison buttons adopting cached bus/selection directly. Add independent real-API second-change and failed-refresh tests before clearing the local proposal; correct this existing-contract defect if reproduced. Keep explicit cancellation of known rejected commands independent. Backend API/product contracts remain unchanged. Previous gates above qualify their exact earlier source snapshots, not an untested future fix.

## Spec Change Log

## Review Triage Log

Three independent reviewers read the complete baseline diff, including untracked files (binary evidence represented by Git binary markers). All three were launched before any result was handled. Verification-gap reviewer reported no gaps. Findings were individually classified before grouping:

| ID | Verdict | Evidence and disposition |
|---|---|---|
| Blind1 | false | Review-ready delivery had not been claimed: the handoff explicitly marked post-fix wider gates pending, and the 144-case affected regression was already running. Its actual result will be recorded before delivery. |
| Blind2 | medium | Copier writes every source basename regardless of prior manifest membership. A same-name unrelated destination is overwritten. Patch: refuse unowned collisions before any write. |
| Blind3 | medium | Directory realpath check does not reject file symlinks; writeFile follows an owned or unowned link. Patch: reject destination entry and manifest symlinks. |
| Blind4 | medium | The adapter evaluates translated shared definitions without checking the assumed upstream source. A changed shared template can silently retain original identifiers. Patch: verify immutable qualified template fingerprints before translation/execution. |
| Blind5 | medium | Browser mode calls runner.browser directly; helpers mutate accounts and restart services, while only backend mode explicitly calls guard_runtime. Patch: guard the exact runtime before browser execution, including the synthetic-account guard. |
| Blind6 | low | Renewed future deadlines are explicitly rejected in both new adoption paths but lack a focused case. Add the two direct failure cases and require unchanged proposals/no write/recovery. |
| Blind7 | low | New success cases only fetch revision C; unchanged B with a legitimately shorter deadline is not directly covered. Add focused same-revision valid adoption cases. |
| Blind8 | low | New adoption-specific tests omit a delayed response after account change. Existing PrivateAccess.workspace validates before and after read-only actions (including epoch/session/pending checks), and both adoption functions additionally check alive/generation. Existing private-identity cases cover delayed bus/selection replies and denied reads across account switch. Reject redundant extra lifecycle scaffolding: no newly unguarded authority path is demonstrated. |
| Blind9 | low | Audit exceptions discard completed checks and identity by constructing a new failure-only object. Patch: retain the accumulated record and phase in failure evidence. |
| Blind10 | false | Exact negative notice scope is covered by reused private-notice-reader 'shared and independent candidates filter exact lines and calendar gaps without changing saved state': nonmatching Heading tags, Midnight/Gap windows, count changes after line/date filters, and unchanged stored state. This was included in the executed 202-case gate. The full journey need not duplicate that integration matrix. |
| Edge1 | medium | Independently confirmed same missing browser guard as Blind5; actual backend path already shows the required guarded call. Same patch group. |
| Edge2 | medium | Independently confirmed unowned destination collision and linked file/manifest writes as Blind2/3. Same copier ownership patch group. |
| Root1 | medium | Post-patch staging inspection compared template bytes with canonical Git blobs: raw CRLF fingerprints reject a normal LF checkout. Patch: normalize only CRLF to LF before exact canonical SHA256 comparison; test both valid encodings and continued refusal of changed source. |

Grouped survivors: copier ownership/link refusal (Blind2/3, Edge2), immutable translation boundary (Blind4), browser runtime guard (Blind5, Edge1), focused deadline/same-revision cases (Blind6/7), retained audit failures (Blind9). Each routes to **patch**: a small internal correction with no public contract or new product state. No intent gap, contract decision or deferred product issue was introduced by this review.

Post-review patch inspection confirmed every retained root cause was corrected. Focused offline safety checks passed11/11 Python and5/5 Node, with transparent Windows junction fallback for unavailable file-symlink privileges. Product bytes are unchanged from the passing144-case gate;20 focused adoption cases and both journeys passed22/22 against the hardened runner; the fresh mobile boundary suite passed32/32. Exact records and limits are in the handoff. No deferred findings remain from these three reviews.

## Verification

- `python scripts/verify-story124.py up|build|browser|backend|verify`: actual isolated services and recorded results, expected exit0.
- Existing mobile/tablet transport suite: new run against freshly built dedicated tablet entry; clearly labelled boundary doubles.
- Manual acceptance checklist: owner decision and any physical-device rerun remain separate from desktop automation.

- E11-A2 confirmed on pristine product (expected GET1, observed0). Scoped fresh-adoption fix implemented;14/14 focused cases passed, with original red and subsequent green evidence retained. Existing known-rejection cancellation remains unchanged. Affected regression144/144 passed in13.7minutes, including both full journeys, stable source and no skipped/flaky cases. Review-only internal tooling patches and focused test additions follow; product bytes remain unchanged.

Delivery remains in-review/pending owner acceptance by explicit user instruction. This overrides the generic final-step done status; explicit user authorization also permits pushing this branch. No merge, deployment or12.5 work is authorized. Final runtime postflight will record the canonical implementation commit and compare every served build file plus the23 pre-existing container identities.

Root follow-up: canonical LF template pins accept equivalent LF/CRLF checkouts and reject changed source. Final targeted tooling checks12/12 Python and5/5 Node passed. Only EOF blank-line cleanup followed the22/32-case gates; product bytes are unchanged and a fresh served build has identical assets.

Canonical implementation commit `5ca3f7df73f4cf49f5244dbc97a0a3ebb8de9891` passed the post-commit runtime audit38/38 (`docs/evidence/12-4-runtime-20261028T081324378353Z.json`), including all23 preserved pre-existing containers. Later commits contain evidence/logs only; manual owner acceptance remains pending.

Physical USB follow-up28October2026: actual Lenovo/Brave against unchanged5ca3f7d. Native PDF cancellation/exact import, independent A/C correction/save, notice native tab/HOME preservation, second-change adoption, end/abort/reload/restart and logout/account checks passed after documented harness corrections. See `docs/evidence/12-4-device-testing-2026-10-28.md`;23 grouped records are15 passed/8 failed attempts, not23/23. Native picker emits hidden/visible; instrumented notice tab/HOME does not. Runtime audit38/38,23 pre-existing containers/four prior Brave targets preserved, no tunnel. Product unchanged; owner acceptance pending.
