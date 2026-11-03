# Deferred qualification

- source_spec: `spec-pm-e1-v110-integration.md`
  summary: Qualify actual independent SSH → installed fixed helper → Docker Compose controlling PTY → inner recovery CLI with the owner.
  evidence: Review B5 confirms helper tests mock Docker while the synthetic S4 journey invokes the inner CLI directly. Both layers pass independently; the complete installed delivery chain, identity/no-recording and handoff controls require owner participation and are not claimed as passed. No production access or Docker socket was used to bypass this boundary.

- source_spec: `spec-pm-e1-v110-integration.md`
  summary: Choose restored-credential policy and authorize a bounded existing-deployment restore/invalidation mechanism before release.
  evidence: Existing helper verify-restore is a disposable copy test; restore-initial rejects an existing deployment; rollback requires equal migrations. Synthetic pre/post restore and quiesced credential settlement pass, but production replacement/invalidation tooling is absent. Preserving trustworthy current hashes versus requiring qualified recovery when those hashes are unavailable has user-visible consequences. No new forced-reset/account-lock or generic privileged interface is inferred while the owner is unavailable.
