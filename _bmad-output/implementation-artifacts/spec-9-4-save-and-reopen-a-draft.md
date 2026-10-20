---
title: '9.4 — Save and reopen a draft'
type: feature
created: 2026-10-20
status: done
route: dispatch
epic: 9
story: '9.4'
alias: V1-04
story_key: 9-4-save-and-reopen-a-draft
baseline_commit: 76a663bc5644069b7d6667e20fde22225ee45548
review_loop_iteration: 0
context:
  - D:/IBE160/_bmad-output/implementation-artifacts/epic-9-context.md
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Private drafts cannot yet survive reload.

**Approach:** Add a Norwegian manual draft form, owned list, save/update and reopen in private PostgreSQL.

## Boundaries & Constraints

**Always:** Preserve existing accounts, data, secret and demo isolation. Use additive migrations. Check session-derived ownership and expiry transactionally. Reuse CSRF/origin, no-store, logout locks and 14-day sessions. Draft expiry is seven days after server creation, never extended by use/retry/sign-in. Purge drafts/operations on startup/hourly. Keep private input in memory; clear on logout/session expiry. Warn before avoidable unsaved navigation.

**Never:** Test against operational storage, reset private data, persist private browser content/logs, integrate PDF, confirm/activate days, assign buses or implement 10.2's full correction workflow.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Save/reopen | Manual service date and ordered activities | Stable draft/activity UUIDs; acknowledged revision reopens identically | Save success requires validated JSON acknowledgement |
| Dates/unknowns | Explicit Oslo calendar dates/offsets; nullable facts | Preserve service date, midnight/extended-hour meaning, unknown codes and provenance | Reject malformed/contradictory values; never guess dates or facts |
| Failed/unknown save | Outage, timeout, HTML or lost reply | Retain input and original operation in memory; show unsaved/unresolved | Authorized lookup/retry settles the same effect |
| Replay/stale | Same operation/payload; changed payload; old revision | Replay returns accepted result; changed payload/stale update conflicts | Preserve local input for comparison; no force overwrite |
| Access/expiry | Foreign/demo request, expired session/draft | Deny before reads/retries/writes; no resurrection | Distinct renewal, safe denial and owned-expiry presentation |
| Reload | Saved state plus unsaved edits | Restore server state after authorization | Warn unsaved input may be lost; no offline recovery |

</frozen-after-approval>

## Code Map

- `backend/app/private_main.py`, `auth.py` — reuse session/CSRF; current mutation ceiling is 4096 bytes.
- `backend/app/private_storage.py` — ordered migrations and cleanup; no draft tables exist.
- `backend/app/domain.py`, `storage.py` — fictional-only contracts; preserve. `pdf_import.py` remains adapter-only.
- `frontend/src/PrivateAccess.tsx` — security generation guards, Web Locks and expiry; mount workspace here.

## Tasks & Acceptance

**Execution:**
- [x] `scripts/verify-private-drafts.py`, `README.md` — use existing isolated setup: stop operational API, select `COMPOSE_PROJECT_NAME=ibe160-private-tests`, preserve secret/operational volume, run disposable project on 8001; restore operational API afterward. Refuse test mutations unless project selection and synthetic-account guard pass.
- [x] `backend/app/draft_domain.py`, `backend/migrations/private/002_drafts.sql` — nullable service date, vehicle duty and ordered activities: UUID, type/raw code, start/end, places, trip/line/direction, uncertainty/provenance. Preserve source clocks; physical bus stays unknown. Bound fields/rows; allow unresolved fields/zero durations, reject negative intervals/invalid Oslo offsets. Add revisions/operations.
- [x] `backend/app/draft_storage.py`, `private_storage.py` — atomic access/revision checks, idempotency and cascading expiry. Preissue creation operations; unused operations expire after seven days and accepted operations share draft expiry. Missing/expired operations cannot recreate work.
- [x] `backend/app/private_main.py` — owned list/read/create/update/operation lookup, safe errors, bounded draft requests; retain authentication limits.
- [x] `frontend/src/PrivateDrafts.tsx`, `PrivateAccess.tsx`, `style.css` — manual activity entry/field updates, list/reopen, save states, conflict comparison/reload. Preserve edits across visibility revalidation of the same valid session.
- [x] `backend/tests/test_private_drafts.py`, `frontend/tests/private-drafts.spec.ts` — matrix negatives, concurrent writes, deadline boundaries and restart evidence in isolated storage.
- [x] `README.md`, `Docs/development-log.md`, this spec, `sprint-status.yaml` — record commands, outcomes, review triage and walkthrough handoff; final owner approval closes the story.

**Acceptance Criteria:**
- Given two synthetic owners, when exercising every draft/operation route, then foreign/demo access and forged mutations fail without disclosure.
- Given midnight, unresolved and corrected facts, when saving and restarting API/PostgreSQL, then authorized reopen preserves values, IDs, revision and original deadline.
- Given 768/1440px keyboard use, when saving/reopening or encountering failures, then labels, focus, wrapping and textual statuses remain usable.

## Implementation Notes

- 2026-10-20: Owner approved the specification and requested continued implementation. Re-read from disk; no external edits. Approved intent is frozen.
- 2026-10-20: Implemented additive private drafts and operation snapshots, transactional session/owner/revision/expiry checks, validated API contracts and bounded manual Norwegian UI. Visibility revalidation hides private fields while retaining memory through an unavailable check; a confirmed invalid session or logout clears it. Conflict comparison uses labelled facts without exposing record identifiers. No PDF integration or activation flow.

## Spec Change Log

## Review Triage Log

| Finding | Verdict | Evidence and route |
|---|---|---|
| Blind 1: list capped at 200 | low | LIMIT 200 hides older entries beyond 200 live drafts. Ordinary daily use within seven-day retention is unlikely to reach this; pagination adds public surface/complexity. Rejected under the low-finding rule. |
| Blind 2: conflict requires replacing local input | false | The approved behavior is preservation for comparison followed by deliberate reload, without automatic merge/force overwrite. The form retains every local value and displays the remote facts. A merge/copy workflow is not required. |
| Blind 3: HTTP 413 loops unresolved | medium | send() treats definitive 413 as unknown and locks the form. Patch definitive size rejection to retain editable input. |
| Blind 4: Unicode exceeds body ceiling | medium | Per-field character bounds can exceed 1 MiB UTF-8. Same size-handling root cause: patch a byte-length preflight and actionable editable rejection. |
| Blind 5: abandoned operation cap | low | 200 unfinished attempts can exhaust the seven-day admission cap; ordinary use is unlikely to reach it. Cancellation/reuse machinery adds complexity; rejected under the low-finding rule. |
| Blind 6: browser clock behind server | medium | valid() rejects created_at later than Date.now(), although the server acknowledgement is valid. Patch removal of that unnecessary clock comparison. |
| Blind 7: cleanup lock inversion | medium | Requests lock sessions then drafts; cleanup currently does the reverse. Concurrent expiry can deadlock. Patch consistent session-before-draft cleanup ordering and concurrent verification. |
| Blind 8: session deadline across blocking locks | medium | Session is checked before draft/operation locks; a wait can cross its fixed deadline. Patch final authorization after blocking locks before read/result/write. |
| Blind 9: failed test stop skips restore | medium | The first finally command can throw before operational restoration. Patch nested finally and exercise shutdown-failure restoration. |
| Blind 10: historical Oslo offsets differ | low | Server accepts representable historical Oslo offsets; browser regex only accepts +01/+02. Directly align browser parsing with its existing Intl Oslo validation; patch with round-trip coverage. |
| Edge 1: list capped at 200 | low | Same verified LIMIT 200 behavior as Blind 1; separately rejected under the low-finding complexity rule. |
| Edge 2: browser clock skew | medium | Same created_at comparison as Blind 6; patch together. |
| Edge 3: datetime overflow | medium | astimezone() can overflow at supported datetime boundaries and escape validation. Patch conversion of overflow into a safe validation error. |
| Edge 4: failed stop skips restore | medium | Same finally ordering as Blind 9; patch together. |
| Verification 1: retry identity unasserted | medium | Pre-verified gap: browser retry test does not compare the committed request and retry. Patch complete payload/target/identity assertions after lost acknowledgement. |
| Verification 2: activity ordering unasserted | medium | Pre-verified gap: all editor fixtures have one activity, so reorder/remove handlers are untested. Patch a multi-activity save/reopen regression asserting order, identity and facts. |

All retained findings were patched and verified. No findings deferred. Historical browser/server timezone-data differences were reproduced: before 1970 the browser validates syntax/calendar/intervals while the backend authoritatively validates Oslo offsets; modern browser Oslo validation remains. Root additionally corrected synthetic login-throttle setup when the expanded browser file exceeded ten attempts; production limits are unchanged.

## Design Notes

No intent gaps. Footprint: private DB/API/UI and tests. Verify migration replay/account preservation before operational application. Planning performs no database actions.

## Verification

### Final root verification and matrix audit — 2026-10-20

- Root read the full implementation diff and review corrections and inspected both synthetic renders. The final isolated verifier passed **34 backend tests (62.34s)**, real PostgreSQL/API restart, repeated migrations, account/session/draft/operation/deadline equality, cleanup, and production TypeScript/Vite build. The first expanded browser run passed 33 and hit the account's ten-attempt login limit on test 11; error context confirmed rate limiting. Added guarded per-test synthetic throttle setup, then the full browser suite passed **34 tests (1.0m)**. No product code changed after the passing backend run.
- `uv run --no-project scripts/test_verify_private_drafts.py`: **1 passed**, with all subprocesses mocked; proves operational restore is attempted when disposable shutdown fails. Prior separate demo/import regressions passed 18/76 tests; those implementations are unchanged.
- Matrix coverage ran and passed: save/reopen and exact record equality; nullable/zero-duration/Oslo/overflow validation; HTML/malformed/lost acknowledgement with complete retry body/target equality; concurrent stale update and comparison; two-owner/forgery/demo denial; expiry before/after blocking locks, purge/no resurrection; reload and unsaved navigation/lifecycle clearing. Multi-activity order and UUID/fact preservation have real save/reopen browser coverage.
- Restored only regenerated 9.2/9.3 images; retained 9.4 evidence. Rebuilt the ordinary API from the verified final code and observed healthy status, preserving its database container/volume/secret. No operational tests/reset; no operational before/after snapshot claim. Disposable services stopped. Spec done means implementation complete; sprint stays review until owner walkthrough/final approval. No push or next story.

- Disposable project only: `$env:COMPOSE_PROJECT_NAME='ibe160-private-tests'; uv run --no-project scripts/verify-private-drafts.py`. Real HTTP/PostgreSQL backend matrix passed 27 tests, including prior authentication regressions. Sequential restart/migration/cleanup checks preserved complete draft content, identities, revision, operation result and original deadline; startup removed an expired unused operation and demo routes denied private identifiers.
- Final production TypeScript/Vite build passed. Full browser matrix passed 29 tests on the final implementation, including unavailable visibility-revalidation recovery. Synthetic 768/1440px screenshots inspected for labels, focus, readable wrapping and overflow. Browser tests check empty localStorage/sessionStorage/IndexedDB, unresolved acknowledgements, stale-write comparison, and session-expiry clearing. Separate fictional API regressions passed 18 tests; PDF adapter regressions passed 76 tests.
- After disposable verification, rebuilt the operational private API with the additive migration using `docker compose -p ibe160-private-work -f compose.private.yaml up -d --build --wait private-api`; it became healthy, retaining the existing DB container/volume/secret. No operational tests or resets. No operational before/after account-count snapshot was taken; migration/account/session preservation evidence comes from the disposable suite and the additive SQL inspection.
- Initial failures were test-only: an expiry helper tried to preissue an operation after the API correctly denied an expired session, and an old auth test used a status locator made ambiguous by the new draft status. Both were corrected and rerun. Independent BMAD review, triage and owner walkthrough remain pending; no final acceptance is inferred.

Run isolated private API/PostgreSQL suites, `npm.cmd run build`, `npx.cmd playwright test` and sequential restart/migration/cleanup verification. Run demo/import regressions separately. Inspect 768/1440px renders, browser storage and `git diff --check`. Record failures/limits, complete BMAD independent review, then user walkthrough before final approval. No tests run during planning.
