# PM-E1 final readiness

**Not ready for live use or release. PM-E1 and S1–S4 remain in review / owner pending, not complete.** Independent synthetic qualification is recorded in [S4 evidence](s4-evidence.md) and its exact runtime manifest. No version, release/tag, merge, deployment or production account operation was performed. Parent three-layer final review and postpatch verification are complete;15 findings were individually triaged.

The implemented scope is own-password change and operator-issued, one-use recovery for existing accounts, including the operator's own app account without app login. Both require a new login on every device. Retained account IDs, ownership, content, deadlines and receipts survive. No email/public signup/admin dashboard/profile expansion or automatic-notices integration is included. Accepted V1 remains separate.

Synthetic evidence covers real gateway/API/PostgreSQL journeys, canonical cookie/Origin policy with simulated TLS termination, generated imports and retained active/terminal days/notices/receipts, repeated/additive migration, API restart, pre/post dump restoration with authority invalidation, and prior-code hash/schema compatibility. Reviewed S1–S3 provide actual PostgreSQL waiter races, invalid-proof/rate/rollback matrices and browser late/offline/uncertain-result handling. Exact results, source fingerprints, tool/image versions and corrections are linked in the scenario evidence; emulated UI evidence does not replace devices.

## Mandatory owner checklist — all utsatt – krever eier

- [ ] Jonas confirms an independently established contact/identity check and capture-free direct code handoff with the teacher; verify clipboard history/cloud sync, terminal/SSH/sudo/screen recordings and failed-delivery revoke/reissue.
- [ ] Perform own-app recovery from actual independent SSH without app session/password; verify exact account+UUID and separate SSH/MFA/outer Access loss routines.
- [ ] Confirm best-effort sole-operator support and what the teacher does while Jonas is unavailable; no replacement administrator or SLA is appointed.
- [ ] Actual tablet portrait/landscape and physical PC: touch, virtual/physical keyboard, password manager, paste/autocomplete, focus/cancel/status, Day/Night and200% text; verify all controls remain reachable.
- [ ] Actual second device: discover revoked sessions on reconnect, safe handling of unsaved work and no automatic credential replay; do not promise immediate offline screen erasure.
- [ ] Prepare and review the deployment-specific recovery/restore path below, then record explicit owner acceptance. No invariant can be waived by signing this checklist.

## Future release/migration/recovery checklist — not execution authorization

1. Complete all owner gates; select a separate release only after explicit approval. Inspect then-current source/configuration and keep automatic notices separate.
2. Confirm actual backup integrity, retention implications and maintenance window; quiesce ingress and application writes. Preserve a verified current snapshot plus previous release and inventory exact migration files.
3. Run the additive migration with normal startup; compare account IDs/hash compatibility, business ownership/content/deadlines/receipts and provision/login behavior. Verify actual deployed HTTPS, cookie/CSRF/Access boundaries and the approved operator helper installation.
4. For code-only rollback, use the host helper only when its migration-equality guard accepts the chosen installed candidate. The tested V1 source lacks015 and is **not** eligible through ordinary helper rollback. Do not bypass the guard.
5. If restore is required, keep ingress and application traffic stopped. Use a separately reviewed and authorized production restoration procedure; current `verify-restore` is only a copy test and `restore-initial` cannot replace an existing deployment. This procedure is an unresolved release prerequisite, not an undocumented SQL workaround.
6. Verify restored business data and deadlines, run required expiry/cleanup, invalidate **every** restored app session and recovery proof before reopening. Identify every restored older password hash; settle or explicitly owner-accept its authority for every affected account under the reviewed recovery procedure while traffic remains closed. If contact or identity cannot be qualified, keep traffic closed. A backup can lose later business changes and resurrect old credentials: no zero-impact guarantee.
7. Recheck that stale sessions/proofs and superseded passwords fail, same-account new login sees the expected retained data, B remains isolated and fresh proofs obey normal limits. Reopen only after verified state and explicit authorization; report any lost post-backup business records truthfully.

The isolated S4 maintenance process proves feasibility with synthetic data only. It is not a deployed administrative interface or an approved production restore command. Real unsupported recovery tooling, external TLS/IdP/SSH controls and personal acceptance remain material blockers even when every independent synthetic check passes.
