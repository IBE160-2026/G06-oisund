# Requirements and acceptance coverage

References are to AC IDs in [epics.md](epics.md). Original PM-A definitions remain in [qualification.md](../specs/spec-password-management/qualification.md). This is **planned coverage**, not executed test results. S4 repeats the combined journey through the deployment-style boundary; earlier stories own their own passing tests.

| Scenario | Primary implementation acceptance | Final integration |
|---|---|---|
| PM-A1 correct current password, old/new login | S1-AC1 | S4-AC1 |
| PM-A2 wrong/mismatched/invalid input | S1-AC2, S3-AC5 | S4-AC1 |
| PM-A3 session/foreign target denial | S1-AC2/3 | S4-AC2 |
| PM-A4 Origin/CSRF/body limits | S1-AC2, S3-AC5 | S4-AC1 |
| PM-A5 issue/redeem/one-use | S2-AC1/2, S3-AC1/2 | S4-AC1/4 |
| PM-A6 exact expiry, used/replaced/revoked/malformed | S2-AC3/6, S3-AC2 | S4-AC1 |
| PM-A7 wrong account/unknown user/signed-in B | S2-AC1, S3-AC2/6 | S4-AC1/2 |
| PM-A8 competing redemption/issue/change | S2-AC6, S3-AC3 | S4-AC1/2 |
| PM-A9 repeated failures/random-name flood/multiple workers | S1-AC5, S2-AC6, S3-AC4 | S4-AC1 |
| PM-A10 all sessions rejected, B unaffected, retained A data | S1-AC3, S3-AC1/8 | S4-AC1/2 |
| PM-A11 login verified before reset resumes later | S1-AC4, S3-AC3 | S4-AC2 |
| PM-A12 private save/read/import/logout/cleanup races | S1-AC4, S2-AC6, S3-AC3/8 | S4-AC2 |
| PM-A13 tabs/late replies/BFCache/visibility/reconnect | S1-AC7, S3-AC8 | S4-AC2 |
| PM-A14 lost/malformed/timeout/DB failure response | S1-AC6, S2-AC4/6, S3-AC7 | S4-AC1/2 |
| PM-A15 offline/unsaved/uncertain business operation | S1-AC6/7, S3-AC7/8 | S4-AC2 |
| PM-A16 API/proxy/validation/operator/audit secret leakage | S1-AC9, S2-AC4/8, S3-AC5/9 | S4-AC4 |
| PM-A17 additive/repeated migration, legacy/provision/rollback | S1-AC9, S2-AC7 | S4-AC1/3 |
| PM-A18 tablet/keyboard/zoom/themes/focus | S1-AC8, S3-AC9 | S4-AC5 |
| PM-A19 independent outer Access/SSH boundaries | S2-AC5, S3-AC10 | S4-AC4 |
| PM-A20 wrong CLI target/failed identity/support unavailable | S2-AC1/4/5/8 | S4-AC4 |

## Requirements beyond the scenario labels

| Requirement | Coverage |
|---|---|
| CAP-1 / PM-FR1 | S1-AC1/2/8 |
| CAP-2 / PM-FR2 | S2-AC1–8 |
| CAP-2 / PM-FR3 | S3-AC1–10 |
| CAP-3 / PM-FR4 | S1-AC3/4/7, S3-AC1/3/8 |
| PM-FR5 | S1-AC2/4–7, S2-AC3/4/6, S3-AC2–8 |
| PM-FR6 | S1-AC3/9, S2-AC7, S3-AC1/8, S4-AC1/3 |
| PM-FR7 | S2-AC8, S4-AC4/6 |
| PM-NFR1 | S1-AC9, S2-AC2/4/8, S3-AC5/7/9 |
| PM-NFR2 | S1-AC2/3/5, S3-AC2/4/5/10 |
| PM-NFR3 | S1-AC4, S2-AC6, S3-AC3 |
| PM-NFR4 | S1-AC6/7, S3-AC7/8 |
| PM-NFR5 | S2-AC7, S4-AC1/3 |
| PM-UX1 | S1-AC8 |
| PM-UX2 | S3-AC6/9 |
| PM-UX3 | S1-AC8, S3-AC9, S4-AC5 |
| PM-UX4 | S1-AC6/7, S3-AC6/7/8/9 |
| Own-account recovery without app login | S2-AC5 + S3-AC10 + S4-AC4, with independent SSH and no app password |
| Operator code not in logs or plaintext database | S2-AC2/4/8; qualified non-recorded controlling-terminal path, no stdout/stderr or reusable plaintext store |
| No standalone day grants today | S1-AC3/7, S3-AC8; revoke derived access, preserve all business rows/deadlines |
| No admin panel/email/public signup/profile | Epic scope + S2 tasks + S4-AC6 and final diff review |
| Separate delivery, no version/merge/deploy action | Epic boundaries + S4-AC6 |

Conditional email/link tests remain outside selected scope. They are not missing mandatory cases for this epic. Tests for ordinary manual notices remain in regression; automatic-notice source ingestion is not a prerequisite.

## Evidence recording during implementation

For each PM-A row, record story/AC, concrete test name, build SHA, synthetic fixture, environment, result and evidence path. Use failures/not-run explicitly. Races need independent transactions and deterministic barriers; data preservation compares known identities/content and deadlines before/after. Secret-leak scans use synthetic markers with protected test failure output; avoid printing a marker that is meant to represent a secret in screenshots/log evidence. Physical device evidence and owner acceptance are separate from automated results.

## Executed independent qualification

The original table is the planned traceability map. Actual PM-A1–20 status, concrete tests, runtime/source fingerprints and mixed automated/owner-pending outcomes are now in [S4 scenario evidence](../implementation/s4-evidence.md). [Final readiness](../implementation/final-readiness.md) retains all mandatory owner gates and the deployment-specific restore-procedure prerequisite. Planning validation was never release approval; V1 and automatic notices remain separate.
