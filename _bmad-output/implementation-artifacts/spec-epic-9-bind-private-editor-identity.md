---
title: 'Epic 9 follow-up — bind private work to its displayed session'
type: bugfix
created: 2026-10-21
status: done
route: oneshot
baseline_commit: 772287e29aeef889e8a01e06cc827501ddb7f5f7
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="User requested the account-switch fix and authorized proceeding with the existing retrospective changes preserved">

## Intent

**Problem:** Two simultaneously visible private windows can display different login/editor state while sharing one session cookie. A new unsaved draft displayed for account A can therefore be submitted under account B after the second window signs in. Existing record ownership checks cannot prevent that new-record mistake.

**Approach:** Bind private editor reads, mutations and PDF upload to the session identity displayed when the operation began. Revalidate that identity inside the existing browser-wide authentication lock before sending private work; reject stale asynchronous results. Notify other windows of successful login so old presentation clears promptly, while keeping correctness independent of notification delivery. A changed/expired identity clears the private workspace and requires deliberate access renewal. Same-session revalidation and transient failure preserve existing input as specified. Do not change server ownership, retention, revision/replay semantics, storage, provisioning or public-deployment scope. Only synthetic isolated test data may be created. Given two visible windows and an account change, saving A's new unsaved draft must never create B-owned work; this must remain true when login broadcasts are suppressed. Ordinary save/reopen, time resolution, upload and logout must still work.

</frozen-after-approval>

## Implementation Notes

- Small reversible fix, no unresolved intent gaps, migration or irreversible product action. Planned implementation: `frontend/src/PrivateAccess.tsx`; focused regressions in `frontend/tests/private-identity.spec.ts`; implementation evidence and retrospective follow-up documentation. No other retrospective findings are included.
- Reuse `private-auth-mutations` Web Lock, `/auth/session` presentation (`account_id`, `created_at`, `expires_at`), memory-only UI state and existing synthetic Docker/browser helpers. Login/logout must remain exempt from editor identity checks. Upload keeps its abort signal, lock and cancellation guarantees.
- Existing README/sprint/retrospective changes are preserved with user confirmation. Existing untracked `tmp/` is not implementation scope. No remote push is authorized.
- Three original two-account regression cases failed against the unchanged production frontend, then passed against the initial fix (21.1 seconds). These cover immediate login notification, missed-notification save rejection with zero operation/save POSTs, and missed-notification list refresh rejection. Tests use real UI login and actual isolated PostgreSQL/API; visibility is held visible to model separate visible windows and one test suppresses incoming BroadcastChannel handlers.
- Private mutations and PDF uploads now validate the expected account/creation-time identity within the existing shared auth lock, before CSRF/payload transmission. Reads validate before and after their request without holding the auth lock across a slow read, preserving the existing stale-list/save/logout concurrency contract. Synchronous identity/suspension references and generation checks prevent old closures from entering a new editor.
- Login notification contains only `session-changed`, no account/private facts. It clears an active workspace but leaves already open logged-out login forms usable. Missing notifications are covered by identity validation.
- Review corrections: obsolete errors are stripped of 401 status before reaching an older child; unavailable identity preflight suspends the workspace with input retained and offers explicit revalidation. Upload preflight uses the import abort signal. No backend API/schema or operational private storage was changed.
- The first full browser run exposed an inconsistent existing synthetic deadline fixture: `/auth/session` generated a different random account on each request and its draft list used an unauthenticated real server. New identity validation correctly rejected that fixture. Stabilize its mock account and empty mock list in `frontend/tests/private-access.spec.ts` so it isolates the original local-expiry timer behavior. An expired response for the expected identity is explicitly classified as expiry, rather than account change.
- The same run exposed a readiness race in the existing list-outage test: it installed a GET failure immediately after the separate save acknowledgement, before a populated list had been acknowledged. `frontend/tests/private-drafts.spec.ts` now explicitly waits for the saved revision's list button before inducing the later outage; all retained-list assertions remain unchanged.
- Independent Blind Hunter review returned four findings, all patched. The same reviewer re-inspected the corrections and the additional delayed-read/upload-preflight scenarios and found no remaining concrete flaw introduced by the corrections. No findings deferred.
- A subsequent broad run exposed the same readiness assumption in the existing delayed-list race test: its gate could intercept the first save's automatic refresh, rather than the deliberate later refresh. Wait for the first saved list entry before installing the gate. This keeps the original delayed-response/revision assertions and makes the intended sequence explicit; verify this changed case separately after the broad run. No product code was changed for either list test correction.

## Review Triage Log

| Finding | Verdict / route | Evidence |
|---|---|---|
| Blind 1: stale 401 can clear a same-session editor after hide/show | medium / patch | Confirmed: caller expiry callback formerly checked identity but not the captured generation. Normalize obsolete workspace errors before rethrow; regression holds a 401 read across successful hide/show revalidation and checks retained input. |
| Blind 2: unavailable identity validation leaves presentation enabled | medium / patch | Confirmed: new preflight error originally propagated without the existing restore suspension behavior. Suspend on current validation transport errors; recovery test verifies hidden form and restored unchanged input. |
| Blind 3: post-read validation lacks a gated account-change regression | medium / patch | Original refresh test only exercised preflight. Add a held real read across a second-window B login with notifications suppressed and verify response rejection. |
| Blind 4: new upload validation stage lacks cancellation/logout coverage | medium / patch | Prior upload tests gated CSRF/PDF only. Add gate at session preflight for cancel and logout, checking prompt lock release, no PDF transmission and no late review. |

## Verification

- Original unchanged production frontend: three new account-switch regressions failed as expected; initial corrected implementation: the same three passed (21.1 seconds).
- Final product build: `npm.cmd run build` and Docker frontend production build passed TypeScript/Vite. Backend source, dependencies and schema are unchanged, so no new backend-unit-test count is claimed for this repair.
- Broad final-product browser execution: **78 passed / 1 test-harness timeout** out of 79 (4.8 minutes). All ten new identity/preflight regressions passed, as did the existing expiry, outage, save/reopen, conflicts, replay, delete, Oslo-time, PDF and logout cases. The sole timeout was the delayed-list test's readiness/gate race described above; its test-only correction is verified separately below. This is not presented as a single clean 79-test run.
- Each browser run used disposable `ibe160-private-tests`, real API/PostgreSQL and synthetic accounts, and its finally block stopped disposable services and restored the operational private API. The two-window tests hold visibility visible; notification loss, delayed replies, expiry and transport failures are explicit simulations around actual application requests. No operational private record reset or account provisioning occurred.
- Corrected delayed-list regression: **1 passed** (9.6 seconds; test body 5.5 seconds) in a separate targeted run. Thus all 79 scenarios have passing evidence on the final product implementation across the broad run and this test-only follow-up. No product code changed after the broad run.
- The independent reviewer rechecked the expiry fixture/list readiness changes and matching-expired-session handling without identifying a concrete issue. Test-generated screenshot changes were restored; Git whitespace validation passed. Disposable services are stopped and the operational private API is healthy. Owner walkthrough/acceptance is separate; retrospective action statuses and machine verdict are retained.

## Owner acceptance — 2026-10-22

Jonas reported that walkthrough items 1 (ordinary save/reopen) and 2 (new login in another visible browser window) looked good. He skipped optional item 3 (manual network outage), explaining that he could not find Brave's offline setting. No owner-executed outage result is claimed; automated preflight/outage recovery evidence remains as recorded above.

Jonas explicitly accepted the repair: "Jeg godkjenner rettingen. Commit og push, ikke start en ny story." This closes F1/E9-A1 and authorizes publishing implementation commit `70ad45f` together with acceptance/tracking documentation. The instruction supersedes earlier no-push/pending-acceptance notes for this repair only. Other retrospective actions and the historical retrospective verdict are unchanged. No new story is created or started. Acceptance changes documentation/tracking only; no product code changed and no tests were rerun for publication.
