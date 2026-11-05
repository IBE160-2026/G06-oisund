# Asynchronous SENDT qualification — 2026-11-05

The owner clarified manual email/direct Teams sending and requested SENDT only in the operator terminal, with no acknowledgement coordination in the recipient form. Baseline: adac1ce99df48aa00bb818d8bd47c27feba0c44a. See [spec and review triage](spec-sent-recovery-handoff.md). No two-hour expiry decision was made; TTL remains 30 minutes. No messaging service, actual message, production account or production operation was introduced.

## Change and invariants

The operator confirms sending/own transfer with SENDT, not recipient receipt. Recipient UI has no MOTTATT/SENDT or wait instruction. Manual email/direct Teams goes only to the previously known institutional recipient after identity/account checks; message history can retain the code. Capture-free terminal and clipboard controls remain. A message includes expiry/timezone and ordinary app URL, never the new password or code in a URL. Actual channel/identity qualification remains an owner gate.

Display still requires active/unexpired proof. Acknowledgement uses the account lock and exact proof: active/unexpired or consumed can be recorded; consumed is reported as already used. ACK does not revive authority, change passwords/sessions or touch a newer proof. The internal named DeliveryStatus separates time remaining from consumed state. Consumed metadata now survives cleanup only until original expiry, within the existing 24-hour cleanup bound; it confers no redemption authority. Revoked proofs remain promptly removable and stale/expired-active acknowledgement remains rejected. Terminal cancellation/restoration failure describes possible prior redemption truthfully instead of claiming credential rollback. The 5-minute operator-dialogue deadline, 30-minute code expiry and all attempt limits remain.

## Isolated verification

Reused task-owned project ibe160-pm-code-format-20261105, separate volume/network, API19441 and frontend16440; no owner synthetic credential was used. Existing ignored browser adapter replaces only project/port literals, preserving assertions. No traces/videos/screenshots of credentials. Test syntax/build/diff checks pass.

Initial pre-review backend: 75 passed in 111.14s. Final targeted recovery/operator/cleanup/restore run: 84 passed and one new test-fixture failure in 121.79s. Two independent clock_timestamp calls made a synthetic expiry one microsecond over the 30-minute database check; replaced with statement_timestamp in the fixture only. The sole failing real-PTY/HTTP/cleanup/SENDT test then passed in 3.53s. Thus all 85 distinct targeted backend cases are verified; this is not claimed as a single 85-pass run. Existing other password-change/access/gateway evidence is reused for unchanged scope.

New cases include recipient consumption before SENDT, cleanup before ACK, exact consumed proof with newer active proof, successful ACK followed by terminal-restoration failure, and interrupted sending after consumption. Real controlling PTY and HTTP boundaries are exercised together, then expired consumed metadata removal is checked. Neither actual SSH nor a real Teams/email recipient is implied.

Browser: all 17 recovery cases passed in 1.9m; source fingerprints and results are in [the manifest](evidence/sent-handoff/verification.json). Covers normal terminal→app recovery, new help text absence of operator instructions, masked/cleared fields, independent login, session revocation, errors/limits and uncertain-response no-replay. Unchanged 18 password-change cases retain previous evidence.

## Review and remaining gates

BMAD short route used read-only investigation and independent blind review. All seven findings were individually triaged/patched; follow-up verified them without a new actionable finding. Fresh physical asynchronous handoff/redemption and actual SSH/helper qualification remain; stories/epic are not completed. No main merge, release/tag or production deployment. Final cleanup/local-owner preparation is recorded below.


## Local handoff preparation

Fresh origin/main remains15011042b1fe093becbe68177e6396e456b1f35f and is already integrated. Automatic test containers/network were stopped/removed; isolated volume retained. The owner test frontend was rebuilt for15440/API18441, and its API recreated with the existing volume. Frontend200/APIhealthok verified; unrelated services preserved. No owner password/code action or real email/Teams message was performed. Owner services remain available for the ongoing guided trial. Refresh the recipient form before continuing; it no longer mentions operator acknowledgement. PM-E1 and mandatory practical gates remain in review.
