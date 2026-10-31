# PM-E1-S1 implementation and lock protocol

Scope: own-password change only. No new schema, recovery proof, automatic login or account recreation. The API derives the owner from a live session, accepts only current_password/new_password/confirmation, uses existing salted scrypt without trimming, and returns `{changed:true}` only after commit. Incorrect current password is authenticated 400 detail.code=current_password; session loss is 401. Existing Origin/CSRF, body bounds, safe validation and no-store controls cover the route.

## Shared lock inventory

Every authorized transaction takes `pg_advisory_xact_lock` on the signed first 64 bits of SHA-256(`private-account:` + canonical account UUID) before session/account/business row locks. Collisions only serialize extra accounts. Discovery reads are unlocked and grant no authority; sessions are re-read after the gate, and expiry is checked with database time. Repeated `auth.session` calls inside a business transaction reacquire the already-held transaction lock and revalidate expiry.

- auth.authenticate resolves the account, gates, rereads its stored hash, verifies and creates its session before releasing the gate.
- auth.session is the common gate for draft_storage.authorized and all workday, selection, bus, lifecycle, outcome and notice storage paths. Existing account/business ordering remains after that gate.
- login's previous-browser-session deletion and idempotent logout use auth.revoke_browser. Login creates the new session in its own transaction, then revokes the previous browser session in another: it never holds two owners' gates.
- private_import authorizes before and after extraction; extraction has no private writes and holds no DB lock. Its final authorization uses the same gate.
- cleanup discovers accounts in UUID pages of 100, then uses one gated transaction per account and the same existing expiration/orphan predicates. Limits cleanup is a separate transaction.
- password change briefly validates the session, commits separate rate admission, then reacquires account/session authority, verifies current password, hashes replacement, rechecks session expiry, updates hash and deletes all account sessions atomically. S2 will integrate proof invalidation into this same transaction; there is no S2 table in S1.

No account gate is acquired while holding global rate-admission locks; no global admission is reacquired while holding account authority. No transaction arbitrarily holds several account gates. A login committed before replacement may return late, but its token is revoked. A private mutation holding the gate commits before replacement; a later mutation must revalidate and fails.

## Admission bounds

The existing persistent login_limits table has separate `change:` buckets: global 100, proxy address 20, account UUID digest 5 admitted requests per 15 minutes. Global precedes proxy and account; failed global/proxy admission creates no account bucket. All admitted credential attempts (including success) consume quota. Counters commit independently of password rejection, expire automatically, and produce 429 with Retry-After:900. Login retains its own 100/20/10 budgets and window; its legacy window alignment now excludes change buckets. The trusted request.client.host is used, never forwarded headers.

## Browser boundary

A separate settings component uses existing themes, password autocomplete, labels, 58px controls and 8px radii. The assistant remains mounted but hidden for cancel; dirty/import/confirmation/uncertain operation ownership prevents opening/submitting. Successful self-revocation is not followed by a live-session check. Existing navigator.locks, generation checks, BroadcastChannel, visibility/BFCache and server checks apply. Lost/HTML/malformed replies clear secrets and lock private presentation until explicit logout; no credential outbox/retry exists.

Review loop 1: password lengths use Unicode code points (`Array.from`) in the form and login, matching Python. Native UTF-16 maxlength/minlength do not truncate valid supplementary characters. Current-password and mismatch feedback associates the message with the affected input, marks it invalid and returns correction focus. PDF processing and unsaved review report a settings-only guard; adopting transfers responsibility to the draft and cancelling releases it without changing logout/navigation policy.

A dispatched password operation retains only a nonsecret pending/unknown/changed outcome across visibility/generation invalidation. It clears private presentation and secrets on hide, then presents uncertainty or confirmed completion on return rather than reopening a retry form. Explicit logout waits until the in-flight password operation settles; credentials are never replayed. An uncertain outcome survives subsequent revalidation within this mounted access controller.

Concurrency tests identify each connection before its account gate and query `pg_stat_activity`/`pg_blocking_pids` until the competitor is visibly waiting on the winner's advisory lock before releasing the winner. This covers login, both draft-save orderings, logout/import/session authorization, cleanup and two changes. Separate regressions inject a real SQL failure after hash update and one session deletion, observe rollback, and let the session deadline pass during replacement hashing while preserving other sessions. Stored-deadline rollover tests check the independent admission windows.

User instructions: [password change](../../../../docs/password-change.md).

## Qualification status

Actual physical tablet/PC touch, virtual keyboard, password-manager integration and owner acceptance: **utsatt – krever eier**. Automated browser rendering is separate evidence and cannot mark S1 done.
