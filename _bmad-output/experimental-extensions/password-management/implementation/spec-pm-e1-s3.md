---
title: 'PM-E1-S3 — Redeem operator code in the app'
type: feature
created: '2026-10-31'
status: in-review
route: dispatch
review_loop_iteration: 0
baseline_commit: 273e5b701e5e8fe866009ae6e38bf7c326d379d4
context:
  - ../planning/epics.md
  - ../planning/technical-contract.md
  - ../planning/coverage.md
  - epic-PM-E1-context.md
  - s1-locks-and-user-flow.md
  - operator-runbook.md
---

<frozen-after-approval reason="Owner authorized sequential PM-E1 implementation; independent checks must pass before next story">
## Intent
Complete PM-E1-S3: user without app session redeems the operator code for the exact existing account and chooses a new password. All S3-AC1..10 apply, including Jonas's own app recovery without forgotten app password. S2 supplies proof lifecycle; S1 supplies shared locking/replacement/all-device revocation. No email/public recovery request/admin/profile additions.

## Boundaries & Constraints
Preserve UUIDs/owner data/retention and S1/S2 safeguards. Both flows require separate new login; no reset session or automatic login. Never operate production, real identities, SSH/MFA/outer Access, physical tablet, other runtime, merge/deploy/tag/release. Isolated synthetic tests only, existing experimental checkout/branch. Parent owns reviewed commit/push and session log. No new product decision on owner's behalf. Mandatory physical-device/identity/handoff/owner acceptance is `utsatt – krever eier`; don't mark story done.

## I/O & Edge-Case Matrix
| Scenario | Input | Outcome | Failure |
|---|---|---|---|
| Recovery | no live app session, username/active code/new password/confirmation | one atomic hash replacement, proof consumption, all sessions revoked, same account data, login separately | neutral failure, no automatic session |
| Invalid proof | malformed/unknown/wrong account/expired/replaced/revoked/used | same generic status/body and bounded comparable processing | no credential/session/business mutation |
| Races | redeem/redeem,issue/revoke/change/old-password login | at most one win; no later obsolete authority | actual DB blockers and rollback evidence |
| Request boundary | live other-user session,CSRF/Origin,oversize/extrafield,limits | reject safely; separate recovery budget | no secret/username existence details/log echo |
| Browser lifecycle | uncertain response,hide/show/BFCache,tabs,offline,dirty B workspace | clear secrets,truthful outcome,explicit logout/login, no replay/private resurrection | retained server data only; no guarantee of offline erasure/unsaved input |
</frozen-after-approval>

## Code Map
- Existing S2 recovery service/schema/operator command/runbook: inspect exact implementation first; reuse without alternate proof format or duplicate lifecycle logic.
- backend/app/auth.py and private_main.py: strict POST /auth/password/recover DTO, canonical bounded response. Live app session returns neutral conflict requiring explicit logout; expired cookie grants nothing. Reuse Origin/CSRF/no-store/safe validation; never call authenticate to replace credentials.
- Recovery service: separate committed admission before account gate, normalized username binding, constant-time digest comparison with bounded dummy path. At acceptance recheck proof expiry using DB clock after password hashing; consume/revoke all proofs and sessions in same transaction. Reuse S1 replacement primitive and existing scrypt/no-trim12–256 code-point policy.
- frontend/src/PrivateAccess.tsx plus small recovery form: login-adjacent Glemt passord? help with operator instructions and username/code/new password/confirmation. Preserve corrected S1 lifecycle/Unicode/error association/focus/dirty/import guards. A live workspace must be explicitly logged out through existing guard before recovery; server also enforces this. Never place code in URL/storage/clipboard helper/trace/log.
- Backend focused tests and frontend password-recovery.spec.ts: actual synthetic PostgreSQL/API plus operator→app journey. Use shared safe fixture guards and real database contention proof patterns from S1; avoid scheduler-only race claims.

## Tasks & Acceptance
- [x] Implement no-session recovery endpoint and reusable service, all S3-AC1..10. Code knowledge never grants private read or app session. Issued proof validity/replacement/revocation remains S2's single source of truth.
- [x] Implement separate persistent recovery admission5/account,100/global,20/proxy per15min, global before new account bucket, independent ordinary login. Failed outcomes commit counters. Use bounded normalized-name/digest buckets even unknown users; no permanent lockout.
- [x] Test exact expiry and expiry while hashing, consumed/replaced/revoked/malformed/wrong-account/unknown cases, live B session denial, strict input and CSRF/body limits. Same public invalid-code shape and controlled comparable processing; don't claim perfect network timing.
- [x] Test true PostgreSQL concurrent redeem winner, issue/revoke/change races, stale login prevention and rollback after partial replacement. Verify accounts/data/receipts/deadlines preserved and all A sessions fail while B remains unaffected. Counter expiry/reset and rejection transactions remain persistent.
- [x] Build simple accessible themed form with paste, code-point password policy and associated errors/focus/cancel. No email promise. Clear secret fields on submission and interruption, handle lost/malformed/HTML/timeout replies truthfully even across visibility changes; no auto-replay/credential storage. Preserve all-device notification/revalidation behavior.
- [x] Execute synthetic operator issuance for own app account with no app password/session, followed by app redemption and new login; never invoke real SSH or handle real code. Capture terminal synthetic code internally without test-report disclosure. Test wrong-account signed-in UI must explicitly logout with dirty/pending protections.
- [x] Run focused backend/browser and relevant S1/S2/access/identity/recovery/import regressions appropriate to edited surfaces. Preserve blank-form renders and computed contrast, not screenshots/traces containing codes/passwords. Record exact source/test evidence and owner deferrals.
- [x] Update user guide and operator-runbook.md for full journey, uncertain result/consumed-code retry, SSH and outer Access boundaries. No live-use readiness until practical owner identity/handoff qualification and S4.

## Implementation Notes

Technical implementation and isolated evidence: [s3-evidence.md](s3-evidence.md). Recovery reuses S2 proof lifecycle and shared S1 credential replacement, with independent committed recovery admission and no-session UI/API. Parent review and mandatory owner/device qualification remain outstanding; story is not done.

## Spec Change Log

## Review Triage Log

| ID | Verdict | Evidence / route |
|---|---|---|
| B1 | medium | Visibility while pending creates shared logout lock; later success leaves it intentionally conservative but text only says log in, which is hidden. Patch truthful locked-success guidance and delayed-success test; never blindly clear another tab shared pending logout. Existing S1 explicit-logout safety remains. |
| B2 | false | Public recovery uses the same strip/casefold username normalization as existing login and approved contract. Raw control rejection is an operator terminal safety requirement, not a new public whitespace policy. Valid code remains necessary; normalized outer whitespace does not grant extra authority. |
| B3 | medium | Any string400 is accepted as definitive invalid-code response. Patch exact canonical detail matching; unrelated400 after dispatch remains uncertain. Add regression. |
| B4 | low | All fields are cleared yet invalid-code guidance does not say all require re-entry. Direct UX correction: explicit re-entry guidance, focus first required empty field while retaining code error association. |
| B5 | medium | Transport/admission errors currently mark username invalid despite no username validation failure. Patch separate form feedback/focus from field validation. |
| B6 | low | Correcting an invalid field retains stale aria-invalid/message. Direct correction on relevant field edit. |
| B7 | medium | Server409 is covered, browser409 restoration branch is not. Patch missed-broadcast/live-cookie test with target unchanged. |
| B8 | false | test_full_recovery_preserves_data_sessions_receipts already submits mixed case plus surrounding spaces and asserts original UUID. Admission and lookup use the same normalized name variable; claimed absence of successful normalization coverage is disproven. |
| B9 | medium | Invalid-state tests snapshot accounts/sessions but not proofs. Patch unchanged proof state/digest/owner/expiry oracle. |
| B10 | medium | Recovery audit actor/action/target and rollback not asserted explicitly. Patch committed audit and rollback assertions. |
| E1 | medium | Same demonstrated UX mismatch as B1. Patch conservative locked-success guidance plus delayed-success visibility test, preserve existing shared logout safety. |
| V1 | medium | Preverified missing real429 browser branch oracle. Patch real budget exhaustion and cleared form/wait status/no uncertainty controls. |

All three review layers completed before triage. The confirmed state/messaging defects and verification gaps have bounded patches, no new public surface or product choice. Shared pending logout cannot safely be erased merely because one credential operation later succeeds; the correction must preserve that established S1 boundary.

## Design Notes
Use the established engineering defaults, not a new auth architecture. Hash only human passwords with scrypt; code digest comparison uses SHA256 constant-time compare. All DB credential mutations serialize under the existing per-account gate. Live B session check must not hold B's gate while acquiring A's gate; use separate committed authorization check and revalidate relevant conditions safely, with no silent account switch. Refuse any owner-dependent task and record concrete deferral.

## Verification
Only compose.password-tests.yaml project ibe160-password-tests, direct API18441/UI15440/fictional18440; backend synthetic guard marker ibe160-private-tests. Parent handles gateway harness if needed. Build-time VITE_PRIVATE_API and VITE_FICTIONAL_API must point to isolated ports before preview. No parallel DB-mutating suites. Use updated actual operator syntax from S2, not invented CLI flags. No prod/device operation. Parent runs three-layer BMAD review before S4 independent qualification.

## Handoff from reviewed S2

Existing schema is migration015 recovery_proofs/recovery_audit; service is backend/app/password_recovery.py, terminal module recovery_terminal.py. The existing bounded Ubuntu helper is repository source only (deploy/ubuntu/bussassistentctl.py); no live installation is authorized. Preserve candidate-only compensating revocation, terminal timeout/signal handling and atomic S1 proof invalidation/audit. Do not perform raw Docker as a future production operator workaround.

For secret-bearing tests, store comparisons in a boolean then assert a static message; pytest assertion introspection must not print synthetic codes/passwords. Avoid logs or browser traces, and only blank-form screenshots may enter artifacts. No existing reference PDFs: synthetic regression adapter filters approved-example cases. Read previous focused tests as patterns, but do not rerun mixed-input suites. Parent will independently verify after implementation. Check actual API loaded source by restarting only isolated private-api when necessary; code mounts do not reload an already running interpreter.

## Parent completion of independent S3 work

Three review layers completed; all12 findings individually triaged, two disproven and the remaining bounded patches verified. Parent final103 backend tests passed156.73s and35 focused browser tests passed3.3m; prior82 selected synthetic regressions, build, blank renders/contrast, source fingerprints and links passed. See s3-evidence.md. Mandatory physical/operator/owner controls remain **utsatt – krever eier**; status remains in-review, not done. S4 may proceed with independent qualification. No release/production authorization inferred.
