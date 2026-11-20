# S1 browser evidence

Review loop 1 corrections and fresh verification are recorded separately in [loop1/README.md](loop1/README.md), including updated source fingerprints. The results and original renders below are historical pre-review evidence.

Synthetic project ibe160-password-tests; frontend preview http://127.0.0.1:15440, private API18441, PostgreSQL isolated volume. Headless Microsoft Edge on Windows, 768×1000 and1440×1000 viewports, CSS root text 200%, Day/Night. These are browser emulations, not physical device acceptance.

`settings-*-200.png` contains blank password fields, labels, all-device warning, submit/cancel and Logg ut. The implementation agent inspected768px Night and1440px Day; the parent independently inspected 768px Night and 1440px Day. Readable content, visible focused new-password ring, no horizontal clipping or secrets. Automated checks require no horizontal overflow, input targets≥58px, correct autocomplete and keyboard Tab progression. Computed contrast evidence is recorded separately by the same focused tests.

Actual tablet/PC touch, virtual keyboard/password manager and owner acceptance: **utsatt – krever eier**.

## Acceptance map

| AC | Independent evidence |
|---|---|
| S1-AC1 | test_change_revokes_all_sessions_keeps_identity_and_data; browser real change/all-device/new login |
| S1-AC2 | test_validation_boundaries_do_not_mutate (wrong current, lengths/mismatch/extra target, Origin/CSRF, oversized, missing/expired session); legacy access boundary tests |
| S1-AC3 | Same retained draft/workday/notice and operation receipts after new login; revoked A reads denied, B unaffected |
| S1-AC4 | test_login_verification_holds_gate_until_session_commit; test_actual_draft_save_serializes_with_change[save/change]; test_two_password_changes_only_one_wins; test_revocation_before_waiting_authorization_and_cleanup[session/logout/import]; private draft/import regressions |
| S1-AC5 | test_persistent_parallel_change_budget_separate_from_login; test_change_cpu_and_storage_caps[proxy/global] |
| S1-AC6 | Focused browser typed rejection/cancel, lost/html/malformed reply, dirty/uncertain write and unconfirmed decision/accepted plan guard tests |
| S1-AC7 | 62 existing private access/identity/recovery browser checks: late replies, missing broadcasts, account switches, visibility, pending commands and actual API interruption |
| S1-AC8 | Four render/contrast files and keyboard/autocomplete/overflow checks. Physical touch/virtual keyboard/password-manager and owner checks remain **utsatt – krever eier** |
| S1-AC9 | Real salted-hash/identity/data tests, legacy access/provision/migration regression, service marker scan and [parent proxy test](proxy.md) |

Computed contrast (same in both widths): Day text 14.39:1, input boundary 5.89:1, button text 11.09:1, focus 21:1; Night text 12.86:1, input text 10.01:1, boundary 8.37:1, button text 11.65:1, focus 11.45:1. Focus ring 3px; controls at least58px. See JSON for exact values. Physical accessibility acceptance is not inferred from these checks.
