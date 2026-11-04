# Deferred qualification

**Restore follow-up — 2026-11-04:** The owner-approved policy is now implemented on the experimental branch with isolated qualification and three-layer review completed. See [restore evidence](restore-evidence.md) and [operator restore routine](restore-runbook.md). The policy decision is closed; actual production installation/execution and owner qualification remain separate. Earlier statements about missing policy/tooling below are historical, not the current decision state.

**Oppdatert beslutningsstatus 2026-11-04:** [Fast rutine for nye passord etter restore er vedtatt](restore-policy.md). Tidligere formuleringer nedenfor om uavklart valg av passordautoritet er historiske. Implementasjon og kvalifisering av mekanismen gjenstår; ingen produksjonshandling er godkjent.

- source_spec: `spec-pm-e1-v110-integration.md`
  summary: Qualify actual independent SSH → installed fixed helper → Docker Compose controlling PTY → inner recovery CLI with the owner.
  evidence: Review B5 confirms helper tests mock Docker while the synthetic S4 journey invokes the inner CLI directly. Both layers pass independently; the complete installed delivery chain, identity/no-recording and handoff controls require owner participation and are not claimed as passed. No production access or Docker socket was used to bypass this boundary.

- source_spec: `spec-pm-e1-v110-integration.md`
  summary: Implement and qualify a bounded existing-deployment restore/invalidation mechanism using the approved mandatory fresh-code/password policy before release.
  evidence: Existing helper verify-restore is a disposable copy test; restore-initial rejects an existing deployment; rollback requires equal migrations. Synthetic pre/post restore and quiesced credential settlement pass, but production replacement/invalidation tooling is absent. Owner decision 2026-11-04 now requires blocking restored passwords for all accounts and fresh-code recovery; unavailable users remain blocked individually. No separate current-hash preservation path is needed. This policy is approved, but production execution is not.

Resolution2026-11-04 for the second entry: independent restore implementation, isolated qualification and review completed; see [restore evidence](restore-evidence.md). Actual deployment/installed-host and owner checks remain separate from this closed technical gap.
