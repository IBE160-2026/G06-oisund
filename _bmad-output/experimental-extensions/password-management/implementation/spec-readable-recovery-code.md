---
title: 'Readable recovery codes for manual tablet handoff'
type: 'bugfix'
created: '2026-11-05'
status: 'in-review'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

The owner could not reliably transfer the existing 43-character case-sensitive recovery code from the terminal to a tablet. Implement the requested20-character code displayed as five groups of four, omit digit0 entirely and explain that exclusion. Make characters unambiguous for manual input while retaining administrative identity/terminal safeguards, expiry, one use, account binding, attempt limits, session invalidation and digest-only storage. No production changes, new administration surface or release. Qualify with isolated synthetic tests and prepare a fresh owner handoff trial; do not call that manual trial passed in advance.

</frozen-after-approval>

## Implementation Notes

- Investigation/route: no unresolved intent gap, no migration or irreversible external action. Bounded internal representation change across password_recovery.py, recovery_terminal.py and PasswordRecovery.tsx, with dependent tests/probes/documentation. Existing API/DB contracts retained. Prior 20-character owner feedback and explicit implementation request authorize this work. Base bb4fe7c5f1ae4456c659babfcd16e8d33a9b741d; fresh main15011042b1fe093becbe68177e6396e456b1f35f already integrated.
- Use 32 ASCII symbols ABCDEFGHJKMNOPQRSTUVWXYZ23456789: uppercase letters except I/L, digits2–9. Twenty independent CSPRNG choices provide 100 bits, not the previous 256. O is allowed; 0,1,I,L are not generated. At most 5 admitted account guesses/15 min and 30 min TTL remain. SHA256 only over canonical code; no plaintext persistence/logging. Offline digest guessing still requires searching a100-bit uniform space; document reduction honestly.
- issue returns canonical 20 to preserve internal digest contracts; terminal alone groups4 with hyphens. Redemption accepts ASCII case variants and ASCII spaces/hyphens, bounded by existing 256-character DTO. Reject non-ASCII before uppercase, invalid alphabet and incorrect canonical length; no O/0 guessing. Continue admission and neutral failures for malformed input. Support old exactly 43-character base64url proofs unchanged/case-sensitive until existing TTL; do not normalize that legacy branch.
- Existing account gates, atomic consume/password/session transaction, TTY/ack/compensation, audit cleanup, redaction, password 12–256/no trimming, CSRF/Origin and no-session rule are unchanged. No state mutation of the owner's synthetic account during automated tests.
- Tests: deterministic alphabet/length/grouping and normalized digests; lowercase/grouped/compact redemption; malformed/Unicode/0/wrong-code generic rejection and attempt budgets; legacy exact/case-sensitive proof; expiry/revoke/used/wrong-account/concurrent use and all-session invalidation via existing recovery regression suite. Update PTY extractors and browser adapters without weakening assertions. Add UI help/accessibility verification; keep masked input/off autocomplete and clearing behavior.
- Read-only investigation delegated per BMAD. One-shot blind review required after implementation; physical handoff remains pending regardless of automated success. Use distinct synthetic Compose project/volumes; preserve owner candidate services/data and other workloads. Update active contract/operator/user docs; preserve historical evidence and frozen story intent with supersession note rather than silently rewriting history.

## Review Triage Log

- R1 medium, patched: legacy-first parsing rejected normalized new codes when extra hyphens made total length 43. Parse new normalized form first and perform both canonical/exact-legacy SHA256 and constant-time comparisons for every admitted attempt. Added 43-length new/legacy regression variants; no legacy mutation or new public endpoint.
- R2 medium, patched: form/terminal omitted acknowledgement order, exposing the existing consume-before-ACK ambiguity. Both now instruct MOTTATT after entry and before submission; browser assertion covers the help text.
- R3 medium, patched: browser log scan omitted the actual lowercase spaced submission. Scan that exact representation plus grouped and compact uppercase secrets and passwords.
- R4 medium, patched: alphabet-only test could miss accidental repeated single-choice generation. New deterministic monkeypatch test checks twenty choice calls and preservation of each selection; real issued-code tests still cover shape/redemption.
- R5 low, patched: new user guide language and glued numbers hindered use. Translate the user guide addition to Norwegian and separate numbers in appended engineering/operator notes. Existing historical text is preserved.


Final independent qualification: 116 backend tests passed in 196.33s, 35 focused browser tests passed in 3.5m; TypeScript/Vite, Python AST and diff checks passed. See [evidence](readable-code-evidence.md) and [source manifest](evidence/readable-code/verification.json). All five review findings were patched; follow-up found no additional functional issue. The owner test UI/API were rebuilt on their original loopback ports with the existing volume; no credential command was run against the owner account. The automated project was stopped/removed (volume retained). Existing unrelated services were not operated. This spec remains in-review under the owner's instruction not to close mandatory practical qualification prematurely; the technical correction is finished, but fresh physical handoff is pending.
