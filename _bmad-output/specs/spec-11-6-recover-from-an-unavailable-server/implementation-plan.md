# 11.6 implementation plan

Current manual test target (owner correction, 2026-10-26): Lenovo Pad with Android and Brave, over the mobile network to the server on the desktop at home. Physical testing remains unperformed; executed desktop Edge/Playwright automation and historical results remain separate. iPad/Safari is not the planned setup. Manual acceptance of 11.5 and 11.6 remains pending; this documentation correction runs no tests.

1. Establish continuity: preserve the dirty 11.5 tree; compare its 106 source/test/verifier files to the final test manifest, inspect actual logs and capture fresh read-only ordinary data/secret/container fingerprints. Do not require pending manual acceptance.
2. Reuse existing stable operation contracts. Correct draft status classification, status-before-retry and current-state reconciliation. Integrate the same retry principle in notice and activity/lifecycle controllers where missing. Keep forms/commands in memory and retain security/loss guards.
3. Execute synthetic browser/API cases for normal saves/reopen, timeout before acceptance, committed lost reply, unavailable lookup, stale/newer revision, malformed proxy responses and repeated retry. Cover notice save/check/manual end plus reader refresh, navigation and authority loss. Add actual disposable server stop/start and Day/Night enlarged recovery captures.
4. Independently review through all three rendered BMAD layers, triage every finding, fix in-scope defects and rerun relevant checks.
5. Run the sequential full disposable verification gate, preserve and restore old evidence, verify ordinary data/services/runtime and deliver exact logs and manual testing guide. Keep 11.5 and 11.6 outcomes separate. Stop in review pending owner acceptance, before staging/commit/push/retrospective/next epic.

## Decisions

- No migration, offline cache or new backend operation type is needed unless executed evidence reveals a contract gap.
- Unknown response is not proof of rejection. An accepted receipt is historical until current state is reconciled.
- Recovery is explicit; reconnecting alone does not send mutations.
- Original same-payload retry remains idempotent even if a pending/absent operation races with an in-flight request.
- All pre-existing local work remains part of the handoff; 11.5 is not accepted on the owner's behalf.

## Completion — 2026-10-26

All five steps are complete. The 106-file 11.5 continuity check found no missing mandatory test or blocking product error; no 11.5 correction was needed. Existing operation contracts support the frontend recovery integration without migrations or offline storage. Three independent BMAD reviews completed; retained findings were fixed and reinspected, with none deferred.

Verification: seven isolated restoration controls, focused 19 + 1 reader extension + 15 affected-contract checks, post-review 64/64, and the sequential full gate (411 backend passes, restart/migration/preservation/build pass, browser 453/456). Three test-only fixture/synchronization corrections were independently inspected; eight affected cases passed three times, 24/24. Product code did not change after the full gate. Completed passing broad tests were not repeated on continuation.

Ordinary data/identity/secret and historical evidence are preserved; the tested build is served locally, disposable services stopped. Eight enlarged Day/Night recovery captures and concrete startup/manual steps are in [delivery evidence](../../../docs/evidence/11-6-server-recovery.md). Specification is in-review and story/sprint review. Manual owner acceptance of 11.5 and 11.6 remains pending; no staging, commit/push, retrospective or next epic.


## Fresh 11.6 integration checkpoint — 2026-10-26

Jonas authorized verification against accepted corrected 11.5, fixes, full regression and local rollout, stopping before his manual results/explicit approval. Current HEAD remains `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed` on main with empty index; the dirty tree is identified by the 120-file source manifest SHA256 `1e0101380841d712125ce999a36d3f20dc43dfe66de253ae22016679111524e5` in `docs/evidence/11-6-integration-source-2026-10-26.json`. Earlier results remain historical.

Recovery now rejects only exact known write rejections after dispatch; HTML/proxy and failed receipt/current reads retain the original notice operation. Delayed reader/maintenance replies count request elapsed time immediately, conservatively hiding near-ending entries rather than prolonging validity. Maintenance uses one database instant for retention and server_now. These failure/latency repairs affect accepted 11.5 and are explicitly included in the manual checklist. Three independent review layers and their reinspection have no open retained finding.

**421 backend tests passed in 526.37s; all 479 browser cases passed in one invocation (38.9m)**. Populated restart, repeated migrations, exact raw state/receipt/deadline/session preservation, cleanup and TypeScript/Vite build passed. One existing TestClient dependency deprecation warning; no product/test failure.

Fresh focused results: 10 account API tests in 16.82s and 7 new browser regressions in 1.1m; 7 verifier restoration controls in 0.256s. The first full attempt was deliberately interrupted after 78 backend progress dots for the discovered defect, not relabelled a pass. Full final log: `tmp/11-6-integration-final-full.log`.

All 120 frozen implementation/test/build files unchanged. All 1004 initial files retained, 390 historical artifacts and 24 original fixture/source/oracle files byte-preserved; 26 frozen contract blocks unchanged. Original fields/rows of all **24 ordinary tables**, database identity and secret preserved; only three expired throttle rows were removed by existing startup cleanup. Ordinary services healthy, synthetic services stopped. Served HTML/assets and 44 backend/migration files match tested bytes. Retro draft unchanged.

Unchanged historical byte control passes; independent pre-11.6/pre-cross-day/resumption comparisons preserve all 24/25/26 frozen blocks. The earlier reported Historical frozen contract changed failure has no retained failing path/bytes/run snapshot and cannot be reproduced; its exact historical trigger is unestablished. No evidence supports changing a frozen contract or weakening the control.

Jonas selected local desktop browser testing; actual manual browser/version/results remain pending. Planned Lenovo Pad/Android/Brave/mobile-network testing remains unperformed. Owner schedules remote access between Epic 11 and Epic 12; none configured here. See the current integrated section of the delivery report for exact startup/actions/expected results. Story 11.6 remains in-review/review with manual acceptance pending; corrected 11.5 remains previously accepted/done. No retro finalization, Epic 11 closure, staging, commit, push or Epic 12 work.


## Owner acceptance - 2026-10-26

Jonas explicitly approved the integrated 11.6 delivery and instructed completion of the Epic 11 retrospective, including the preliminary work from the other chat. The accepted source manifest remains unchanged. Selected manual environment was local desktop browser; detailed scenario results/browser version were not supplied and are not invented. No physical Lenovo/Android/Brave/mobile-network test is inferred. Remote access is scheduled between Epic 11 and Epic 12. No commit/push or Epic 12 implementation is authorized. Earlier pending statements remain historical.
