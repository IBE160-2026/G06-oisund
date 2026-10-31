---
stepsCompleted: [1, 2, 3, 4]
status: in-progress
implementationAuthorized: true
baseline: 5cee9e03d03d2c9c165c7f8fec64aa3e146959ab
inputDocuments:
  - ../specs/spec-password-management/SPEC.md
  - ../specs/spec-password-management/brownfield.md
  - ../specs/spec-password-management/implementation-plan.md
  - ../specs/spec-password-management/qualification.md
  - ../../../planning-artifacts/prds/prd-IBE160-2026-09-21/prd.md
  - ../../../planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md
  - ../../../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/DESIGN.md
  - ../../../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md
---

# IBE160 — Password management epic breakdown

## Overview

Experimental extension for Jonas and the course teacher, with Jonas as sole recovery operator. Owner-approved scope: own-password change, operator-issued one-use code including recovery of Jonas's own app account using independent server/SSH access, new login on every device after either password replacement, preserved accounts/data, and separate delivery from automatic notices. No email, public registration, admin panel, profile system, version allocation or release action.

This document uses the installed BMAD CE template (requirements → coverage → epic → As a/I want/So that stories with Given/When/Then acceptance), supplemented with the project's implementation-spec Tasks & Acceptance, Code Map, evidence and handoff conventions. Stories are detailed enough for sequential implementation after a separate user instruction. Planning completion is not implementation permission, executed tests or owner acceptance of software. Read [technical contract](technical-contract.md) and [coverage](coverage.md) with each story.

## Requirements Inventory

### Functional Requirements

- PM-FR1: Signed-in users change only their own password after proving the current password.
- PM-FR2: Jonas issues/replaces/revokes account-bound, expiring one-use recovery codes via independent authenticated server access with explicit target confirmation.
- PM-FR3: A user enters username/code and selects a new password in the app without an app session; includes Jonas's own account.
- PM-FR4: Both replacements invalidate every app session and derived day access; saved data remains available after new login to the same account.
- PM-FR5: Failures, unavailable server, lost responses, expired/reused/revoked/wrong-account codes and concurrent actions have truthful, safe outcomes.
- PM-FR6: Preserve account IDs/hashes until actual replacement, usernames, owner relationships, business receipts and retention through migrations/rollback handling.
- PM-FR7: Provide a usable operator procedure and independent final qualification before any release; no public/admin/email expansion.

### NonFunctional Requirements

- PM-NFR1: Compatible salted password hashing, digest-only code persistence, no secret-bearing logs, command arguments, URLs or persistent browser storage.
- PM-NFR2: Strict server authority, existing Origin/CSRF/HTTPS/private-demo boundaries, bounded persistent attempt budgets and neutral public recovery failures.
- PM-NFR3: Atomic single-use replacement and revocation, consistent lock ordering across login/private traffic/cleanup; no post-reset stale-login session or deadlock.
- PM-NFR4: No offline credential action/outbox; discard obsolete replies and private presentation when access is revoked. Do not promise remote erasure of an offline display or preservation of unsaved edits after session loss.
- PM-NFR5: Additive migrations, actual PostgreSQL/API/gateway evidence and synthetic-only testing; no production account/data mutation for qualification.

### Additional Requirements

- Existing React/TypeScript → FastAPI → PostgreSQL modular system; no starter/bootstrap story or new dependency/service required.
- Use `auth.py`, `private_main.py`, `manage.py`, versioned private migrations and cleanup. Existing session-then-account lock order must change coherently, not by adding an inverted reset transaction.
- No separate day-grant token exists. Day permission is session + owner + live data. Revoke sessions without deleting workdays or resetting shift state.
- Server/SSH, outer Access and application accounts are distinct. App reset does not repair SSH or revoke outer Access. No password reset admin role/table needed.
- Parent artifacts contain older one-user/local-only wording; current owner decisions and completed Ubuntu handoff supersede those points only. Preserve parent files and unrelated operational issues.

### UX Design Requirements

- PM-UX1: Small “Brukerinnstillinger” entry near current account controls; separate “Endre passord” screen, not a profile dashboard or crowded day view.
- PM-UX2: “Glemt passord?” at login, operator-help text and username/code/new-password/confirmation form; no presumed email delivery. Current-password/new-password autocomplete, paste, clear labels and safe field validation.
- PM-UX3: Existing Day/Night tokens, starting 58px control height, 8px corners/2px borders, 200% text, portrait/landscape and keyboard/focus checks. IR-01 informative text ≥4.5:1, necessary non-text ≥3:1; focus area/contrast per DESIGN. No color-only state.
- PM-UX4: Save/cancel unsaved work and reconcile uncertain business commands before voluntary change; truthful pending/failure/success messages, explicit all-device logout warning, safe cancel/focus return, no secret replay or false save after timeout.

### FR Coverage Map

| Requirement | Epic | Primary stories |
|---|---|---|
| PM-FR1 | PM-E1 | S1 |
| PM-FR2 | PM-E1 | S2 |
| PM-FR3 | PM-E1 | S3 |
| PM-FR4 | PM-E1 | S1, S3 |
| PM-FR5 | PM-E1 | S1, S2, S3 |
| PM-FR6 | PM-E1 | S1, S2, S3, S4 |
| PM-FR7 | PM-E1 | S2, S4 |

## Epic List

### Epic PM-E1: Keep access to the existing account safely

Users can change a known password or recover a forgotten one without losing their account or saved work. All PM-FR1–7 are covered. Separate password-management delivery; no functional dependency on automatic notices.

## Epic PM-E1: Keep access to the existing account safely

**Goal and user needs:** distinguish voluntary password change from forgotten-password recovery. Jonas must recover either existing app account via server access even when he cannot sign in to the app. The teacher uses the code to choose a password privately. Both users regain access to their own retained data after reauthentication.

**Numbering:** main's active epic list uses 9–12. Experimental automatic-notices planning uses `AN-E1`/`AN-E1-S1…`. Use the established extension namespace `PM-E1`/`PM-E1-S1…S4`, previously unused in main and this extension. Do not assume Epic 13 is available or allocate V1 story aliases. The earlier PM-1…PM-4 work-package labels are superseded by the ordered stories below; they are not competing epic IDs.

**Dependencies:** accepted V1 and Ubuntu integration; available operator SSH access; existing synthetic integration recipe. Source baseline remains `5cee9e0` after fetch; no changed main files affect this plan. Inspect then-current main again before actual implementation without silently merging it into this planning branch.

**Order:** S1 → S2 → S3 → S4. S1 delivers complete own-password change with its required safety; S2 delivers a testable operator proof lifecycle; S3 adds end-user redemption; S4 qualifies the combined delivery. S2 is operationally complete and independently reviewable but not a promise of usable recovery until S3 is complete. No release of an unfinished reset journey.

**Definition of done:** all story ACs and PM-A1–20 pass with recorded evidence; synthetic existing accounts/data preserved; operator self-recovery and teacher-assisted recovery demonstrated; actual tablet/PC checks and owner acceptance; clean migration/restore/rollback rehearsal and release-readiness report. Product tests are not deferred wholesale to S4. A separate explicit release/deploy decision is still required after this evidence, with no version assigned here.

### Story PM-E1-S1: Change my password and end previous access

As a signed-in user,
I want to replace my password after proving the current one,
So that I can control access without changing my account or losing saved work.

**Readiness:** implemented and technically reviewed; mandatory owner/device qualification remains pending (in-review). **Depends on:** existing V1 only. **Scope/value:** complete change form + endpoint + necessary shared account serialization and revocation. No reset table, code issuance or email in this slice. This is the largest foundational slice because unsafe revocation cannot be postponed; keep it bounded to existing auth callers and the one new command. Follow the concrete lock protocol in technical-contract.md rather than redesigning every business operation.

**Traceability:** CAP-1/3, PM-FR1/4/5/6, PM-NFR1–5, PM-UX1/3/4.

**Acceptance Criteria:**

- **S1-AC1 — Given** a live session and correct current password, **when** the user submits a valid new password twice, **then** exactly that account receives a fresh salted hash and all its sessions are revoked atomically, **and** the current browser returns to login without automatic authentication; old password fails and new password succeeds.
- **S1-AC2 — Given** wrong current password, invalid length, mismatch, unexpected account field, missing/invalid CSRF or foreign Origin, **when** submitted, **then** the request makes no password/session/business change, **and** safe field or generic boundary errors contain no submitted values. Missing/expired sessions are 401; a wrong current password is a distinct authenticated validation error and must not masquerade as session expiry.
- **S1-AC3 — Given** two accounts and multiple sessions, **when** A changes password or B forges a target, **then** target authority comes only from the live session, **and** A's obsolete sessions cannot read/write days, drafts, notices or receipts while B remains unaffected. Same-account renewed login preserves UUID/content/ownership/expiry/lifecycle and still-authorized historical receipts.
- **S1-AC4 — Given** concurrent login, private read/write/import, cleanup, logout or two password changes, **when** replacement commits, **then** no old-password login can create a valid later session and no revoked-session mutation commits after it, **and** the documented common locking order completes without deadlock. A business action already committed before replacement remains saved history.
- **S1-AC5 — Given** repeated wrong-current-password submissions or random/parallel traffic, **when** budgets are reached, **then** persistent account/global/proxy limits bound hashing and storage across workers with a neutral 429/Retry-After response, **and** ordinary login budgets stay separate with no permanent account lockout.
- **S1-AC6 — Given** unsaved form changes or an uncertain business write, **when** opening/submitting change, **then** save/cancel or reconcile happens before voluntary logout and an all-device warning is visible, **and** cancel changes nothing and returns meaningful focus. A lost password-response clears secrets and gives an uncertain-result/login action; it never queues or retries credentials automatically.
- **S1-AC7 — Given** background tabs, late responses, BFCache, session loss or an offline device, **when** access can no longer be verified, **then** existing hide/revalidate and generation checks prevent restored obsolete content, **and** the next server check rejects revoked sessions. No claim of instant offline erasure, no persistent private cache and no guarantee of recovering unsaved browser-only input.
- **S1-AC8 — Given** the new settings/form in both themes on tablet/PC, **when** operated with touch/keyboard/password manager and 200% text, **then** labels, status, focus and controls meet PM-UX1/3/4 with current-password/new-password autocomplete and paste, **and** the main assistant view remains simple and Logg ut remains accessible.
- **S1-AC9 — Given** existing synthetic users and captured application/proxy/exception logs, **when** the new flow and legacy provisioning/login are exercised, **then** existing data and hash compatibility remain intact and secrets are absent from logs/DB plaintext, **and** the code introduces no unnecessary schema or secret persistence.

**Tasks & Acceptance:**

- [x] `backend/app/auth.py`, `draft_storage.py`, session callers and `private_storage.py` — implement the shared locking/revalidation protocol, account-wide session deletion and login race prevention; inventory direct session SQL in private routes, imports and cleanup before changes. Preserve global admission ordering and existing transactional business receipts. Prove S1-AC3/4 with real concurrent connections.
- [x] `backend/app/private_main.py` and a small auth-domain module if helpful — strict own-change DTO/response, current-password verification and separate bounded admission. Keep no-store, safe validation, Origin/CSRF and existing scrypt. No client-selected target or reset infrastructure.
- [x] `frontend/src/PrivateAccess.tsx` and a small password form component — settings entry, form, all-device confirmation, dirty/pending guards, password-state clearing, typed errors and cross-tab invalidation. Reuse existing private session identity and generation guards; do not pass a successful self-revoking response through a later live-session check that would falsely report failure.
- [x] Backend focused tests + `test_private_access.py`, relevant private storage/import/cleanup regressions; frontend focused tests + `private-access.spec.ts`, `private-identity.spec.ts`, `private-recovery.spec.ts`. Include before/after commit barriers rather than timing sleeps for races; HTML/malformed/lost responses and late reply guards.
- [x] Update the user guide with change flow, all-device logout and unsaved-data limitations; document the lock order and chosen limiter constants. Record actual test commands/results and rendered touch/focus/contrast evidence in extension-local evidence.

**Completion evidence:** working end-to-end change against real synthetic API/PostgreSQL, focused concurrency/regression results and rendered UI. S1 does not wait for S2–S4 to make its own safety tests pass. See [S1 implementation/review evidence](../implementation/spec-pm-e1-s1.md): final parent41 backend/18 focused browser passes,77 distinct synthetic regressions and isolated proxy checks. Mandatory S1-AC8 physical-device/password-manager/owner acceptance remains **utsatt – krever eier**; checked tasks indicate independent technical work only, not story completion.

### Story PM-E1-S2: Issue and revoke recovery codes through server access

As Jonas, the recovery operator,
I want to issue or revoke a code for an explicitly confirmed existing account using SSH,
So that I can authorize recovery for myself or the teacher without knowing the app password or adding an admin panel.

**Readiness:** implementation-ready specification; isolated execution authorized 2026-10-31. **Depends on:** S1 shared account lock/revocation boundary. **Scope/value:** operator command, minimal recovery schema, lifecycle/cleanup and a usable safe-handoff runbook. Redemption is S3; lifecycle is demonstrable without it. Do not distribute live-user codes until the full recovery journey is qualified.

**Traceability:** CAP-2, PM-FR2/5/6/7, PM-NFR1/2/3/5. No new web UI or administrator application account.

**Acceptance Criteria:**

- **S2-AC1 — Given** independent authenticated server access and an existing exact username, **when** Jonas requests issuance, **then** the CLI resolves the normalized username and displays that username plus immutable account UUID for explicit confirmation before mutation, **and** unknown/ambiguous target, mismatch, cancellation or noninteractive invocation issues nothing. No fuzzy, first-match or implicit current-app-account selection.
- **S2-AC2 — Given** confirmed identity and target, **when** issuance commits, **then** a CSPRNG code with at least 256 bits of entropy is bound to that UUID and recovery purpose for the documented TTL, **and** only its digest is persisted, only one active proof remains and prior proof is revoked. The password and sessions are unchanged by issuance.
- **S2-AC3 — Given** an active/expired/absent code, **when** explicit target-confirmed revocation or reissuance is requested, **then** revocation is idempotent and reissuance supersedes older proof atomically, **and** code/expiry status cannot be confused with the account password or session state.
- **S2-AC4 — Given** redirected output, missing controlling terminal, recorded/transcribed session, or unsafe transport, **when** issuance is attempted, **then** it fails closed or is stopped by the documented operator preflight before disclosure, **and** raw code never goes to stdout/stderr, ordinary logs, arguments, environment, shell history or persistent files. The approved interactive path displays it once on the controlling terminal after commit; capture limitations and interrupted-handoff revoke/reissue are explicit.
- **S2-AC5 — Given** Jonas is logged out of the app or forgot his own app password but retains SSH access, **when** he selects his own account, **then** issuance/revocation works without any app cookie/current app password, **and** the procedure does not change SSH keys, outer Access membership or grant a new app administrator role. Loss of SSH is a separate host recovery case.
- **S2-AC6 — Given** concurrent issue/revoke/change, limits, database failure or cleanup, **when** operations race, **then** they serialize by account, enforce the active-proof invariant and leave no partial credential mutation, **and** password change invalidates outstanding proof. Expired proof is unusable immediately, regardless of cleanup schedule.
- **S2-AC7 — Given** preexisting users/data, **when** the additive private migration is applied/reapplied and the API restarts, **then** IDs, hashes, business data, ownership and deadlines are unchanged, **and** old login and new provisioning work. Cleanup deletes only bounded recovery/audit metadata, never an account or business row to revoke access.
- **S2-AC8 — Given** operator issuance/revocation/failure, **when** audited, **then** minimal actor/action/target/time/result metadata is recorded without secret material, **and** the runbook explains identity check, best-effort support, single-operator absence, own-account recovery, code handoff and expired-code retry. Audit actor is the operator identity, never falsely attributed to an app session.

**Tasks & Acceptance:**

- [ ] `backend/app/manage.py` plus a bounded recovery service — exact-target resolution, explicit account confirmation, issue/revoke commands and separate operator audit. Reuse existing CLI/private DB mode and host secrets; no web admin endpoints, list-all-users export or direct manual SQL recipe.
- [ ] Next unused `backend/migrations/private/*.sql` and `private_storage.py` — create recovery proof/admission/audit structures only as needed here; UUID FK, digest uniqueness, state/expiry constraints, one active proof and expiry index. Integrate S1 change transaction with proof invalidation in this story. Keep migration numbering unallocated until implementation baseline check.
- [ ] Implement safe controlling-terminal output per technical-contract.md; reject non-TTY/redirected invocation, keep ordinary output secret-free, and test actual SSH/interactive container command behavior using synthetic secrets. Record residual session-recording controls; do not claim TTY detection proves no recording.
- [ ] Add CLI/storage integration tests for exact account selection, cancel/unknown target, repeated revoke, replace/races, cleanup, limit boundaries, failures and plaintext/log scans. Rehearse additive migration twice with retained synthetic records and compatible provisioning.
- [ ] Write `operator-runbook.md` under this extension's later evidence/docs area, with operator invocation in the existing Ubuntu layout, preflight, no-transcript rule, identity/handoff procedure and self-recovery rehearsal. Keep the command syntax documented as future until implemented; use no real secret examples.

**Completion evidence:** testable code lifecycle and safe operator handoff on disposable environment, migration preservation and draft runbook. No app password, mailbox or app login required for operator actions. S3 owns completion of user recovery.

### Story PM-E1-S3: Recover my existing account with the one-use code

As a user who forgot the app password,
I want to enter the operator's code and choose a new password,
So that I regain my own account and saved work without needing the forgotten password.

**Readiness:** implementation-ready specification; isolated execution authorized 2026-10-31. **Depends on:** S1 and S2. **Scope/value:** complete no-app-session redemption endpoint and login-adjacent flow, reusing S1 replacement/revocation and S2 proof state. No email link, public recovery request or general profile.

**Traceability:** CAP-2/3, PM-FR3/4/5/6, PM-NFR1–5, PM-UX2/3/4.

**Acceptance Criteria:**

- **S3-AC1 — Given** a valid active code bound to A and no app session, **when** A submits username/code/new-password/confirmation through the app, **then** one transaction verifies binding/expiry, replaces the hash, consumes/revokes all proofs and deletes all A sessions, **and** success returns to login without automatic sign-in. New login reopens the same still-retained account data.
- **S3-AC2 — Given** malformed, expired, consumed, replaced, revoked or incorrect code, unknown username or A's code with B's username, **when** redemption is attempted, **then** the same public status/error shape and generic code message are returned with comparable bounded processing, **and** no password/session/business data changes or account-existence detail is exposed. Expiry is invalid at the server deadline, not after a grace period.
- **S3-AC3 — Given** two simultaneous redeems, issue/revoke/password-change races or an old-password login in progress, **when** transactions contend, **then** at most one code redemption changes the password and all older proof/session authority remains invalid after commit, **and** no stale-credential session is created later. Rate-limit counters survive rejected transaction outcomes.
- **S3-AC4 — Given** repeated failures, random usernames or multiple workers/proxy clients, **when** limits are reached, **then** persistent account/global/proxy admission bounds CPU and rows and returns neutral throttling, **and** an anonymous reset failure never permanently locks the account's ordinary login. Recovery codes are never tested through a general login/session-issuing endpoint.
- **S3-AC5 — Given** bad/missing CSRF, foreign Origin, oversized/extra fields or invalid new-password input, **when** posted, **then** existing boundary controls reject safely, **and** validation/exception responses and logs contain no code/password. Code knowledge never authorizes a private-data read.
- **S3-AC6 — Given** a user at login or already signed in to another account, **when** opening “Glemt passord?”, **then** login offers support/code entry without account lookup or email promises, **and** an existing workspace must be explicitly exited with its dirty/pending protections before redemption. Neither UI nor API silently switches accounts; the no-session redemption contract is enforced server-side.
- **S3-AC7 — Given** a lost success response, HTML/malformed response, network outage or browser interruption, **when** recovering, **then** secrets are cleared and the result remains uncertain until explicit new-password login or operator reissue, **and** no code/password is persisted/replayed automatically. A code consumed before a lost response is not described as proof that no change happened.
- **S3-AC8 — Given** A's other devices/tabs have private views or unresolved writes, **when** reset commits and those clients next check access, **then** they lose old authority and clear/hide private state; late responses cannot resurrect it, **and** server-saved results remain available to renewed A login only. No promise of durable unsaved input or instant removal from an already offline screen; no offline day grant is introduced.
- **S3-AC9 — Given** the recovery form on tablet/PC in both themes, **when** typed/pasted and operated at 200% text with keyboard/virtual keyboard, **then** the code, username and new-password fields and nearby feedback meet PM-UX2/3/4, **and** cancel returns focus to login/help with no mutation. Never show an actual code in automated screenshots or artifacts.
- **S3-AC10 — Given** Jonas has no app session and completes the S2 SSH issuance for his own synthetic account, **when** he redeems in the app, **then** new login succeeds and old sessions fail exactly as for the teacher, **and** outer Access remains a separate prerequisite, with no bypass or claim that SSH/IdP credentials were changed.

**Tasks & Acceptance:**

- [ ] `private_main.py`, recovery/auth service — strict no-session DTO and canonical response; constant-time digest check, normalized username binding, bounded dummy path and rate-limit admission before expensive work. Reuse S1 account gate and current-password hashing policy; atomically consume proof and revoke every app session. Use DB time immediately before acceptance.
- [ ] `frontend/src/PrivateAccess.tsx` and small recovery form — login help, operator-code entry, support instructions, new password confirmation, explicit existing-session exit and uncertain completion. No reset token in URL or browser persistence. Reuse CSRF fetch and cookie transport without requiring app login.
- [ ] Add real DB/API tests for every code state including exact expiry, incorrect account, concurrent winners and stale login; validate generic public failure timing under a bounded comparative test rather than claiming perfectly constant network timing.
- [ ] Browser tests for no-session recovery, wrong-account workspace, all-device logout, back/visibility/stale replies, lost response and dirty/uncertain business writes; rendered Day/Night and tablet/PC evidence. Reuse existing synthetic setup and account-isolation fixtures.
- [ ] Update user instructions and operator runbook with end-to-end self/teacher recovery, no-auto-login, consumed-code/uncertain-result handling and limitations when SSH or outer Access is unavailable.

**Completion evidence:** full operator → app → new login journey for A/B, race and rejection evidence, preserved data and no secret logs. Security and usability checks pass here, not postponed to S4.

### Story PM-E1-S4: Qualify the combined account-management delivery

As the operator and owner,
I want reproducible evidence and a tested operating procedure for both password flows,
So that I can decide on a separate release without risking existing accounts or being dependent on app login for recovery.

**Readiness:** implementation-ready specification; isolated execution authorized 2026-10-31. **Depends on:** S1–S3 completion. **Scope/value:** combined regression, migration/rollback/restore rehearsal, operator walkthrough and release-readiness report. No new product feature, automatic-notices integration, production recovery or actual release/deploy in this story.

**Traceability:** all CAPs/FRs/NFRs/UX requirements, all PM-A scenarios. This is an integration gate, not a substitute for earlier story testing.

**Acceptance Criteria:**

- **S4-AC1 — Given** a clean disposable deployment-style build and preexisting synthetic accounts/data, **when** migrations, service restart and both complete journeys run through gateway/API/PostgreSQL, **then** every PM-A1–20 case has pass/fail/not-run evidence tied to exact build and test, **and** data identities/content/ownership/retention remain intact except deliberate password/proof/session changes.
- **S4-AC2 — Given** saved drafts, active/terminal days, account notices, concurrent requests and multiple clients, **when** both flows run across outages and reconnection, **then** authorization/revocation, pending-operation truthfulness and non-resurrection all hold, **and** ordinary import/save/day/notices/logout and fictional isolation regressions pass.
- **S4-AC3 — Given** a synthetic pre/post-change backup and compatible rollback candidate, **when** rollback and restore are rehearsed, **then** documented invalidation prevents restored/revoked sessions or recovery proofs regaining authority before traffic resumes, **and** any restoration of an older password hash is explicitly handled and reported without losing business data or presenting a zero-impact guarantee.
- **S4-AC4 — Given** the documented operator SSH/interactive execution path, **when** Jonas rehearses own-account recovery with no app session and teacher-account handoff using synthetic identities, **then** target confirmation, verification, one-time display, no logging and revoke/reissue are demonstrated, **and** SSH loss, outer Access loss and operator absence have separate actionable instructions. No additional administrator is silently appointed.
- **S4-AC5 — Given** actual target tablet/PC and Day/Night forms, **when** the owner performs touch, virtual keyboard, focus, cancel and 200% text checks, **then** usability observations and explicit owner acceptance are recorded separately from automation, **and** untested device/accessibility cases are not relabelled passed.
- **S4-AC6 — Given** all story evidence and remaining issues, **when** the final report is prepared, **then** it lists exact scope/build, tests, data-preservation proof, known limitations, operator routine and proposed deployment/rollback checklist, **and** a failing safety invariant blocks release readiness rather than being silently waived. No version, tag, merge or production deployment is performed by this story.

**Tasks & Acceptance:**

- [ ] Create a reproducible synthetic recipe using existing private/Ubuntu-style configuration, isolated volumes and loopback ports; never reuse live volumes or reset production accounts. Record build/dependency versions, actual commands and cleanup ownership.
- [ ] Execute [coverage](coverage.md) and selected established regression suites; link each scenario to concrete test IDs/results, include DB barriers for races and post-restart attempts. Explain any not-run or blocked case honestly.
- [ ] Rehearse additive migration and restore/rollback in isolated environments, including stale sessions/proofs and old password hashes; finish and independently walk through operator documentation with no real secrets in artifacts.
- [ ] Record physical tablet/PC observations and owner acceptance; ensure no dashboard/email/profile or public signup additions slipped into the final diff.
- [ ] Produce extension-local final-readiness report and release checklist. Keep automatic notices separate; if the owner later changes that decision, add the previously planned combined integration gate instead of assuming this evidence covers it.

**Completion evidence:** reproducible combined report, runbook, migration/rollback/restore and actual UX observations. All unresolved release blockers remain explicit; approval to execute a future release is distinct from the epic's technical completion.
