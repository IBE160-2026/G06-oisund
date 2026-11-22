# Epic PM-E1 Context: Keep access to the existing account safely

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Let Jonas and the teacher change a known password or recover a forgotten one while retaining the same account and saved work. Jonas is the sole recovery operator, using independent SSH/server access even for his own app account. Both replacement flows end all application sessions and require fresh login. Deliver this extension separately from automatic notices.

## Stories

- Story PM-E1-S1: Change my password and end previous access
- Story PM-E1-S2: Issue and revoke recovery codes through server access
- Story PM-E1-S3: Recover my existing account with the one-use code
- Story PM-E1-S4: Qualify the combined account-management delivery

## Requirements & Constraints

The current user instruction authorizes sequential S1–S4 implementation, testing and review, superseding older planning-only execution restrictions. The owner is unavailable: do not ask for decisions; record owner-dependent checks as deferred. No physical tablet work, production access, real accounts, deployment, merge or release. Keep extension routing and PM identifiers; do not allocate V1 stories or a release version. Exclude email recovery, public signup, admin dashboard, profile expansion and automatic-notices integration.

Change targets only the authenticated account and requires its current password. Recovery accepts username, one-use code and user-chosen password without an app session. A live session requires explicit logout before recovery; code possession never grants private-data access. Preserve UUIDs, ownership, business data, receipts and retention deadlines; revoke derived day authority by revoking sessions, not deleting workdays.

Use synthetic fixtures and actual PostgreSQL/API/gateway evidence for concurrency, migration and regression. Record pass/fail/not-run with test identity, build, environment and artifact; planning validation is not executed evidence. Preserve explicit blockers for operator qualification, physical-device checks and owner acceptance. These may be deferred during implementation but cannot be represented as passed or as release approval.

## Technical Decisions

Reuse React/TypeScript, FastAPI and PostgreSQL; no additional service or starter project. The technical contract supplies engineering defaults, not additional owner-approved product policy. Keep existing 12–256-character scrypt policy without trimming, fresh salt on replacement, and no plaintext persistence. Recovery proof uses at least 256 random bits and digest-only storage, bound to account and recovery purpose.

Use one transaction-scoped, stable namespaced account advisory lock before session/account/business row locks across login, authorization, replacement, operator lifecycle and cleanup. Session discovery may read an owner without locking but must revalidate after taking the gate. Verify login's current stored hash and create its session under that gate; no stale verification may create authority after reset. Avoid arbitrary multi-account locking. Prove ordering and races with independent PostgreSQL transactions, not mocks alone.

Replacement admits the request, takes the account gate, revalidates authority/proof, updates the hash, invalidates all proofs when present, deletes every account session and commits before acknowledging. Recovery checks database time immediately at acceptance, including after waiting or hashing; at most one redemption wins. Issuance leaves passwords and sessions unchanged. S1 allows atomic proof invalidation integration; introduce recovery schema only in S2. Migrations remain additive and preserve provisioning compatibility.

Proposed endpoints are POST `/auth/password/change` and `/auth/password/recover`; both return bounded acknowledgment, clear obsolete caller cookies where applicable and never sign in. Preserve no-store, cookie protections, Origin/CSRF and secret-safe validation. Code failures share a generic 400 response; use 401 for required authentication, 403 for CSRF, 422 for validation, 429 for throttling and 503 for unavailability. Do not expose raw validation input or trust forwarded client IP through the gateway.

Initial bounds: proof lifetime 30 minutes; one active proof per account; separate change/recovery admission of five submissions/account/15 minutes, global 100 and proxy-address 20 per purpose/15 minutes; issuance three/account/hour. Valid submissions consume budget. Admission commits separately before account locking so rejected credential transactions cannot roll counters back. Bound unknown-account work/storage, compare failure timing, and preserve separate login budgets. Remove expired/consumed/revoked digests within 24 hours and minimal audit after 30 days; expiry never depends on cleanup.

Operator issue/revoke uses existing independent host authority with exact normalized username plus UUID display and typed full-username confirmation. Do not invent app-admin authority or verified per-person audit identity from a shared OS account. Reveal a code once, after commit, only to the controlling terminal; refuse redirects/noninteractive execution and keep secrets out of stdout/stderr, arguments, environment, logs, URLs and files. Recording/transcription preflight is required because TTY detection cannot establish capture safety. Failed handoff requires revoke/reissue; failed delivery after commit attempts safe revocation and reports uncertainty. Qualify actual identity/contact and capture-free handoff before real use; SSH loss and outer Access loss remain separate procedures.

Restore/rollback rehearsal must quiesce traffic, preserve business data, invalidate restored sessions/proofs before reopening and explicitly handle restored old password hashes. Older-code compatibility must be demonstrated. Rehearsal uses isolated synthetic resources only.

## UX & Interaction Patterns

Provide small “Brukerinnstillinger” access to a separate “Endre passord” screen and “Glemt passord?” at login with operator-help/code entry. Use clear labels, paste and appropriate password autocomplete. Preserve Day/Night styling, 58px starting controls, 8px corners, 2px borders, keyboard/focus behavior and 200% text. Informative text contrast is at least 4.5:1 and necessary non-text 3:1; do not communicate state by color alone.

Before voluntary change, save/cancel dirty work and reconcile uncertain business commands. Warn about all-device logout. After confirmed commit, return to login; self-revocation must not turn success into a spurious failed post-request session check. Lost/malformed responses remain uncertain: clear secrets, never persist/replay them, and offer explicit new-password login or operator reissue. Security revocation clears private state when detected; late replies, BFCache and visibility/reconnect cannot resurrect it. Same-origin tab signaling does not reach remote devices, and offline screens cannot be erased immediately. Do not promise preservation of unsaved edits after session loss.

## Cross-Story Dependencies

Execute S1 → S2 → S3 → S4. S1 establishes safe replacement and shared authorization ordering; S2 adds proof lifecycle and integrates invalidation; S3 completes redemption using both. Each story owns its security and usability evidence. S4 integrates the PM-A1–20 matrix, regression and isolated migration/restore/rollback evidence, while distinguishing deferred operator/owner/device qualification from automation. Automatic notices are not a prerequisite.
