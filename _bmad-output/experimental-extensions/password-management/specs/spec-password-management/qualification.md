# Acceptance and verification plan

**All product tests below are future tests, not executed results.** Test only isolated synthetic accounts A/B, sessions A1/A2/B1 and retained drafts/workdays; no production DB, real passwords or actual account recovery in this planning task.

| ID / capability | Scenario | Required result |
|---|---|---|
| PM-A1 / CAP-1 | A1 changes password with correct current password; login old/new | Old rejected, new accepted; account UUID/data unchanged; fresh salt. |
| PM-A2 / CAP-1 | Wrong current password, mismatch, too short/long, extra fields, Unicode, paste | Clear safe errors; no mutation/session revocation on failure; policy enforced on server, no secret echo. |
| PM-A3 / CAP-1 | Unauthenticated, expired session, forged account ID, B attempts A change | No authority beyond session owner; reject forged input and preserve both accounts. |
| PM-A4 / CAP-1/2 | Missing/foreign Origin, missing/invalid/expired CSRF, oversized body | Rejected before mutation; no CORS relaxation or input leakage. |
| PM-A5 / CAP-2 | Operator verifies A, issues proof, A completes and then reuses it | Exactly one password change; second attempt rejected; operator never knows chosen password. |
| PM-A6 / CAP-2 | Expired boundary before/at/after TTL; changed client clock; used/replaced/revoked/malformed proof | Server expiry authoritative; all invalid forms get same safe error; GET does not consume. |
| PM-A7 / CAP-2 | A proof with username B; invented username; authenticated B opening A recovery | Wrong binding rejected without account disclosure; no implicit mutation of B or silent workspace/account switch. |
| PM-A8 / CAP-2 | Two simultaneous completions; replacement issuance racing completion; change racing reset | At most one valid winner under serialization; older proof invalid; transaction atomic. |
| PM-A9 / CAP-1/2 | Repeated current-password and recovery failures; random username flood; multiple workers | Persistent per-account/global caps and bounded storage/CPU; neutral rate-limit response; no permanent anonymous lockout of ordinary login. |
| PM-A10 / CAP-3 | After success, A1/A2 access session, drafts, days, notices, mutation and receipt lookup; B1 operates | A sessions rejected; B unaffected. New A login sees same retained rows/receipts and original expiry; no shifted deadlines or restarted shift. |
| PM-A11 / CAP-3 | Old-password login pauses after hash verification, reset commits, login resumes | No valid stale-credential session can be inserted/returned. Test multiple workers, not just mocked order. |
| PM-A12 / CAP-3 | Reset competes with private save/read/import, logout and cleanup | No deadlock; documented transaction ordering; no old-session operation commits after reset. Earlier committed business result remains reconcilable. |
| PM-A13 / CAP-3 | Multiple tabs, late successful response/401, BFCache/back, visibility return, device reconnect | No resurrected old workspace/account; generation guards and server recheck apply; cross-device revocation discovered on next check. |
| PM-A14 / CAP-1/2/3 | Response lost after commit, timeout before commit, malformed response, DB restart | UI says uncertain, clears secrets, never auto-replays password; new login/reissue resolves state. No false success/failure claim. |
| PM-A15 / CAP-3 | Network unavailable, unsaved plan/notice proposal, unresolved business command | Password operation unavailable offline; normal change requires save/cancel/reconcile first. No durable secrets/private cache; do not silently resubmit unresolved command as another account. |
| PM-A16 / CAP-1/2 | Capture API/validation/exception, gateway/error, operator session, audit and test logs using synthetic secret markers | Zero passwords/codes/recovery URLs/cookies in logs or artifacts. Code handoff recording disabled/verified; no real secret used to test this. |
| PM-A17 / all | Migrate an existing synthetic database; rerun migration; provision after migration; rollback/restore rehearsal | UUIDs/ownership/content/deadlines preserved; legacy passwords work until changed; explicit-column provision works; no revived revoked authority after rollback/restore. |
| PM-A18 / all | Tablet portrait/landscape, touch, virtual keyboard, Day/Night, 200% zoom, keyboard and focus/status | Controls reachable and readable, correct autocomplete/paste, focus returns on cancel, no crowded primary assistant view. Owner personally accepts final UX. |
| PM-A19 / CAP-2/3 | Outer Access denied/expired or lost; application reset succeeds on an allowed device | No bypass of Access; app reset does not claim to revoke outer sessions; support runbook covers the distinct failure. |
| PM-A20 / CAP-2 | Operator targets wrong account, cannot verify identity, needs revoke/reissue; support unavailable | Explicit target confirmation, no issuance without verification, neutral instructions, documented escalation/coverage limit. |

Conditional email tests: no send to unverified/newly typed address; old accounts continue without email; verification/reset proofs cannot cross purposes; address change invalidates stale recovery; unknown/known/unverified requests have equivalent public status/content and comparable timing; provider failure/retry/throttling/duplicate delivery do not change password or create multiple valid proofs; controlled egress, sender configuration and mounted-secret rotation work. For a link variant test scanners, referrer/history/log leakage, canonical origin/host injection and outer Access redirects. These tests are not required to pretend email is implemented in the assisted minimum.

## Existing regression suites to extend/select

Backend: `backend/tests/test_private_access.py`, `test_private_drafts.py`, `test_private_workdays.py`, `test_account_notices.py`, `test_retained_data.py`, `test_cleanup_observability.py`, `test_tablet_transport.py`. Frontend: `frontend/tests/private-access.spec.ts`, `private-identity.spec.ts`, `private-recovery.spec.ts`, `private-retention.spec.ts`, `private-notice-recovery-integration.spec.ts`, `tablet-transport.spec.ts`, and complete private-flow tests. Add focused change/reset/concurrency suites; preserve synthetic-only setup guards. Qualify through real API/PostgreSQL and deployed-style gateway in addition to component tests. Exact test selection is reassessed against the final code diff.

## Epic/story planning — 2026-10-31

All PM-A1–20 scenarios map to explicit story ACs in [coverage](../../planning/coverage.md). [Epic PM-E1](../../planning/epics.md) defines S1 own change, S2 operator lifecycle, S3 redemption and S4 combined qualification. Own-account recovery without app login is mandatory, not an open choice. The 58px/IR-01 parent UX contract applies. Product tests below remain unexecuted; planning readiness is recorded in [validation](../../planning/validation.md).

## Decision-update validation — 2026-10-31

Owner choices now govern the baseline: two expected users (Jonas and teacher), Jonas as operator, administrative code, all-device login after both flows, and separate delivery. Q2–Q4 are resolved; Q1 retains only operational contact/verification and response details. Extend PM-A20 runbook review to sole-operator self-recovery and unavailability. Public rollout and email are outside initial scope. No product test or implementation was started by this update. Capability IDs and existing acceptance scenarios remain unchanged.

## Initial planning validation performed

- Read repository instructions, session-log workflow, installed BMAD Spec workflow/template/customization and extension routing precedent.
- Fetched origin/main; created isolated planning branch at recorded SHA; read automatic-notices planning only.
- Inspected auth/account/session/private authorization, frontend/recovery and committed Ubuntu/gateway configuration; did not query production data.
- Cross-checked relevant OWASP pages; recommendations remain distinct from repository facts and owner decisions.
- Coherence pass: CAP-1..3 have intent/success, explicit non-goals/constraints, provisional policy and actionable questions at initial drafting; the owner decisions above supersede those questions where answered.
- Preservation pass: request A maps to brownfield; B–D to implementation plan; E to work packages/migration/delivery and PM-A1..20. Existing users, day access/offline limits, email secrets, version deferral and independent integration control are covered.
- Final document path/whitespace and changed-file checks are recorded in the session log. No product tests, runtime validation, UI rendering, migration, deploy or security certification is claimed for a documentation-only change.
