---
title: 'Operator-only sent acknowledgement for asynchronous code handoff'
type: 'bugfix'
created: '2026-11-05'
status: 'in-review'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

The owner wants to send a recovery code manually through email or Teams without staying in live contact with the recipient. Replace the operator's MOTTATT confirmation with SENDT and remove that operational concept from recipient-facing instructions. The recipient uses the code independently before its expiry. Keep identity/account verification, the readable code, one use, limits and secret-safe application storage/logging. Do not add a mail service or send actual messages. Preserve the existing 30-minute expiry; the proposed two-hour change was not approved. No production changes or release.

</frozen-after-approval>

## Implementation Notes

- Baseline adac1ce99df48aa00bb818d8bd47c27feba0c44a, clean password branch. Bounded one-shot: no remaining intent gap, no migration/irreversible action. Small changes in recovery_terminal.py, password_recovery.py and PasswordRecovery.tsx plus corresponding tests and current operator/user documentation. Existing owner test data is preserved; automated tests use separate project.
- Investigation: delivery(...acknowledge=True) currently requires an active proof, so a recipient consuming the code first produces a false failure. Under the existing account lock allow acknowledgement of the exact consumed proof without changing it or any other proof. Return a distinct consumed result; say already used, not that passwords/sessions are unchanged. Display checks still require active, unexpired proofs. Revoked/missing/expired-active ACK stays rejected. No reactivation/TTL extension. Cancellation compensation must not falsely claim a consumed code was revoked.
- Existing delivery/acknowledged audit means the operator reports sending, not verified receipt. No new audit enum or personal recipient data needed. SENDT confirmation is not a prerequisite for redemption; codes are live after issue commit. Keep terminal deadline and unsuccessful-send revocation. Document that failed/uncertain sending requires explicit revoke; after the terminal closes use recovery-revoke for wrong recipient or delivery failure.
- Current operator routine permits direct Teams message or email to the already established institutional recipient after independent identity/account check. Include expiry time and normal app address, never the new password or a code-bearing URL. No shared channels/CC or this AI chat. Message retention is an explicit consequence, not claimed secret-free messaging; code authority ends on use/revoke/expiry. Terminal/SSH/screen recording controls remain.
- Tests: existing operator lifecycle/PTy interruption/stale ACKs; added consume-before-SENDT, exact-proof/newer-proof preservation, truthful success and cancellation. Browser verifies recipient help contains neither MOTTATT nor SENDT nor a waiting requirement. Existing generation/entropy/restore/lifecycle evidence is reused where code is unchanged. BMAD blind review and owner trial remain required. No generic profile or admin interface.

## Review Triage Log

- R1 medium, patched: cleanup could delete a consumed proof before SENDT. Keep consumed metadata until its original expiry, without granting authority or extending TTL. Tests cover cleanup before ACK and removal after expiry.
- R2 low, patched: terminal omitted point-of-use expiry/app-address instructions. It now tells the operator to include expiry with timezone and ordinary app address, without code in URL.
- R3 medium, patched: latest owner journal still had actionable old ordering. Explicit supersession points to SENDT procedure and preserves historical evidence.
- R4 medium, patched: recipient clipboard-history/cloud-sync advice was lost when manual messaging became permitted. Restored concise recipient guidance.
- R5 medium, patched: mock-only early-redemption coverage did not exercise real terminal ordering. Added real controlling PTY → HTTP redemption → cleanup → SENDT, with successful exit/terminal restoration assertions. This is not an actual SSH or physical-device claim.
- R6 medium, patched: consumed proof plus terminal-restoration failure after ACK lacked coverage. Added with/without newer proof; credentials/new proof survive and message never claims rollback.
- R7 low, patched: duration sentinel was a maintainability risk. Internal named DeliveryStatus has explicit remaining/consumed fields; both callers updated. No external API change.

Follow-up independent read-only review verified all seven corrections and found no new actionable issue. No production, owner credential or actual message was used by reviewers. Existing 116-backend/35-browser format evidence remains valid for unchanged scope; final targeted results are recorded below.


Final independent qualification: all85 distinct targeted backend cases verified (84 passed in the broad final run; one synthetic timestamp-fixture correction then passed separately),17 browser cases passed1.9m, build/AST/diff passed. See [evidence](sent-handoff-evidence.md). Automatic test services stopped; local owner UI/API updated without changing credentials or sending messages. Keep in-review under the owner's instruction not to complete mandatory physical qualification prematurely. Actual async sending/identity and full SSH/helper remain owner gates;30-minute TTL is unchanged.
