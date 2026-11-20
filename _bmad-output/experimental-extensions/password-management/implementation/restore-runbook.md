# Database restore with fresh account recovery

Independent implementation/qualification and review completed. Do not use against production before the reviewed candidate is installed under a separately authorized deployment and owner qualification is complete.

## Scope

This routine restores a trusted application database backup into the existing deployment. It replaces the database's business state with the selected snapshot: later work may be absent. It preserves the restored account identities and ownership. Every restored password is made unusable; every restored app session and active recovery proof is invalidated. Each user subsequently chooses a new password through a freshly issued administrative code. Ordinary restart/update never invokes this routine.

The mechanism does not preserve a separate copy of current password hashes and never generates a temporary plaintext password. Jonas can recover his own app account using independent server access; loss of SSH or outer Access requires their separate recovery processes.

## Before an authorized restore

1. Confirm the exact backup and expected current release, the possible loss of post-backup business changes, and a maintenance window. Use only trusted backups; never treat an arbitrary uploaded PostgreSQL archive as safe input.
2. The installed candidate must include the persistent maintenance guards in both systemd and the running Compose services. The helper refuses an older deployment lacking those guards. Installing this candidate is a separate deployment action, not part of issuing a restore command.
3. Keep a safe copy of the selected backup. Verify its SHA-256 and identify its exact basename. Commands accept fixed backup storage and full expected release identity; they do not accept arbitrary paths or SQL.
4. Do not record passwords, one-use codes, cookie values or database contents in logs, tickets or chat. Restore diagnostics should contain only operation/stage identities and aggregate checks.

## Intended operator command sequence

From the independent controlled SSH session, after separate authorization:

~~~sh
sudo -n /usr/local/sbin/bussassistentctl restore BACKUP_BASENAME SHA256 EXPECTED_CURRENT_RELEASE
~~~

The helper snapshots the source, establishes durable maintenance state, closes ingress and stops writers, retains a pre-replacement backup, restores/migrates offline, destroys restored credential authority and verifies retained business state. Successful preparation is not permission to bypass reopening checks.

If interrupted, inspect safe operation metadata through the existing status action:

~~~sh
sudo -n /usr/local/sbin/bussassistentctl status
~~~

This reports stage and supported next step, never credentials or database contents. Correct the underlying condition, then use the bounded continuation:

~~~sh
sudo -n /usr/local/sbin/bussassistentctl restore-resume
~~~

Never manually remove maintenance state, delete data-ready markers, repoint volumes, start old code, or rerun raw database commands. The saved operation identity and stage govern continuation; do not repeat replacement after a user has recovered.

After the helper has completed verification, explicitly reopen using:

~~~sh
sudo -n /usr/local/sbin/bussassistentctl restore-reopen
~~~

Before the durable ingress-commit boundary, failures/interruption keep external traffic closed across helper calls, service restart and reboot. During opening, a narrowly scoped local-start permit lets the application reach readiness while the tunnel stays inhibited. After ingress is committed, a tunnel/connectivity failure is an ordinary connectivity problem: retry opening as directed by status, without restoring old business fingerprints or invalidating newly recovered credentials.

Stages record preparation, closed writers and prior backup, replacement, migration and quarantine, retention, verification, local opening and ingress commitment. V2 records a database operation marker in the same transaction as replacement. Resume checks the exact marker along with row fingerprints. Old journals with ambiguous equal fingerprints remain closed for investigation. Retry is bounded. Retention is idempotent and runs after replacement. Status records completion after the tunnel check. Actual installed-host qualification remains separate from mocked local lifecycle tests.

## Recover users independently

Use the existing [operator routine](operator-runbook.md) to confirm identity and exact account, then issue a fresh code through the controlling terminal. The user opens «Glemt passord?», chooses their own password and logs in separately. Jonas follows the same flow for his own account; app login is not required for code issuance.

The teacher may wait: that account's old password remains unusable while Jonas uses his recovered account. No requirement to recover both users before opening. Each code still expires, is single-use and is subject to existing limits. Restored recent issuance audit and attempt counters may cause their documented bounded wait; never erase audit to bypass limits.

Old devices must sign in again. An offline screen cannot be remotely erased immediately; its next authorization fails. Unsaved work can be lost and must not be silently replayed. Restored saved work remains subject to ordinary retention and snapshot age.

## Evidence and release gate

See [restore qualification](restore-evidence.md) for executed tests, supported backup schemas, source/runtime identities and limits. Practical identity/contact, capture-free handoff, actual SSH/helper/Compose terminal chain, physical device checks and explicit owner acceptance remain required before real use. This routine itself authorizes no production restore or release.

## Supported archives, storage and bootstrap

Supported schemas begin at the v1.0.1 set through 014 and include exact, gap-free migration prefixes known to the selected V2 release. Isolated preflight compares the resulting schema with a fresh migrated database and rejects unknown migrations, tables or altered schema. External or offsite backups must first be installed by the trusted server administrator into the fixed root-owned backup storage under the required timestamp/full-SHA basename.

Failed preflight copies are removed without touching original backups. Pending operation source/prior/SQL material is protected for recovery. Completed or abandoned operation copies are pruned after48hours during normal backup maintenance, alongside the established backup policy; offline/failed scheduling cannot promise wall-clock deletion. Metadata receipts remain separate from sensitive dump/SQL copies.

For a new server, `restore-initial` validates the archive in isolation before importing. Repeat `restore-initial` with the same release and digest to resume an exact, recognized import. It migrates, quarantines and verifies before writing the receipt required by `confirm-data` and first deployment. An unrecognized nonempty database stays closed for investigation. Existing-deployment recovery uses the three commands above.

During separately authorized installation, ensure the updated helper itself runs install-tools for the candidate, creating the root-owned searchable maintenance directory and reloading the unit guards, before deploying guard-enabled containers. Merely copying new unit files or running only the old helper's install-tools body does not establish this prerequisite. Inspect actual installed guards before live restore.
