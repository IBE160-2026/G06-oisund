# Story 12.3 — implementation and verification handoff

> Historical pre-main-sync checkpoint. Its outcomes, original commands and earlier pending-acceptance statements describe that version. Jonas subsequently accepted 12.1 and 12.2 (done/accepted) on 27 October 2026; only 12.3 remains pending. See the [current-main integration handoff](12-3-main-sync-handoff.md) for new sources and fresh verification. No old pass or physical observation is relabelled as qualification of the integrated build.


Technical verification is complete: production build, 34/34 task browser cases, 37/37 selected post-review regression cases and 74/74 actual API/database controls passed. All retained findings from three review layers are closed. Owner acceptance is pending. Jonas has not manually/physically accepted Story 12.1, 12.2 or 12.3. This report distinguishes desktop automation from actual-device evidence.

## Git and isolation

- Clean local main at `ce0669f6f75f337a2df9471860be1b66efb171f0`; ancestry confirms integration `f13d28991ac85934826f0da7b7b81fbc09181f24` is contained. No existing 12.3 branch/worktree was found.
- Created `story/12-3-tablet-pc-accessibility` and worktree `D:/IBE160/tmp/story-12-3`. Planning commit `a5b7ca4c830e75c67bb1b4b568a3fa7b9270ee95` records the implementation specification and context. Product/evidence commits are recorded below after final gates.
- Local origin/main already equalled local main at start; the earlier session log records a subsequently authorized push of previous work. This session performed no remote operation, push or main merge.
- New Compose project `ibe160-story123-tests`, frontend 15323, fictional API 18323, private API 18324, separate named volumes and ignored secrets/manual credentials. Existing 15312/18312/18313 services and ordinary services are outside every new command's target.

## Delivered behavior and decisions

A shared, allowlisted `ibe160-theme=day|night` preference covers all production entries, login and workspace. Day is deterministic on first visit; only an explicit choice writes storage. Invalid/denied storage remains usable. Theme survives demo reset, logout and reload while existing private/demo content boundaries remain. There is no Auto mode.

The Night palette covers shell, links, comparisons, controls and bright warning surfaces. Labelled controls wrap and retain the 58px control floor; fact columns reflow. Keyboard focus remains visible as the browser scrolls, including native date/time field focus. Notice maintenance returns to the actual visible invoker from day or preparation, including recreated preparation buttons.

No backend API/schema/parser/lifecycle/retention contract changed. No 12.4 complete-system/device qualification, external access activation, GPS, wake or private offline persistence was added. Actual tablet/mobile-network qualification and Jonas acceptance remain pending.

The requirement-to-behavior/evidence matrix and manual steps are in [the checklist](../story-12-3-manual-testing.md). The implementation specification is [spec-12-3-tablet-pc.md](../../_bmad-output/implementation-artifacts/spec-12-3-tablet-pc.md).

## Execution record

All new `12-3-*` JSON records identify commands, revision, source hashes before/after, actual translated test/verifier input hashes, exits and raw log hashes. Build gates record dist hashes; browser gates require built artifacts to match the current product sources. Raw UTF-8 logs and reports remain under ignored `tmp/story123/<run>/` and are now preserved in the durable `12-3-recorded-raw-through-regression.tar.gz` archive. All 29 actual input files for each qualifying 29/184 run were preserved with exact recorded SHA256 equality; see `12-3-recorded-raw-index.json`. Earlier exploratory browser copies were overwritten and remain hash-only; their available raw reports/logs are preserved. Future final gates snapshot actual inputs before execution and archive them durably. Original failure records are preserved; a later successful subset does not rewrite an earlier result.

- Initial offline npm install hit sandbox EPERM; explicitly escalated offline installation succeeded (26 packages). Initial Docker read was blocked by sandbox pipe access; escalated read succeeded. These are environment restrictions, not product failures.
- Initial runtime startup passed 11 ownership/configuration/volume guards but failed its source-stability gate because implementation was still changing. The recorded failure is retained.
- Initial 7-case desktop task attempt: 3 passed, 4 failed. Storage tests passed; focus viewport assumptions and unresolved conflict journey were corrected. Source changes during this development attempt also made the stable-source gate fail.
- Expanded 20-case attempt: 3 passed, 17 failed. Eight private cases used a creation admission ID for an update (404, corrected fixture); preparation focus return still failed and was fixed; focus outline clipping at viewport edges was exposed and corrected. The explicit failed measurements are retained.
- Subsequent bounded attempts and final qualifying results are recorded below. No unexecuted test is counted as passed.

## Historical evidence preserved

12.1/12.2's broad private run remains 477/479, followed by successful requalification of its affected 27-case suite and 6 repeated restart cases. No new complete 479-case pass is inferred from those results or this story's targeted regression gates. Their integration/historical evidence is unchanged.

## Final gates and review

Three independent review layers examined the complete baseline diff: blind, edge-case and verification-gap. Each finding was classified separately before grouping. Eleven retained rows (including two independent findings about the same focus-measurement defect) received bounded corrections; one reading-order finding was rejected using literal existing keyboard-order assertions exercised in the 184-case run. Full triage and the post-correction outcome are recorded in the specification. Native controls, browser/OS zoom, physical touch, target-device versions and owner approval are identified as measured or not-run, never inferred from viewport emulation.

### Pre-review-patch qualifying gates

- Complete task matrix: 29/29 passed in 260.268s; stable source/actual inputs/current build, exit0. Evidence `12-3-browser-20261027T085409659655Z-0057a88f.json`.
- Actual HTTP/PostgreSQL: 74/74 controls passed, exit0, source stable. Evidence `12-3-real-20261027T090138701036Z-533c4013e63a.json` and wrapper `12-3-verify-20261027T090138067002Z-964b76d0.json`.
- Affected regression: 184/184 passed in 13.0 minutes, exit0, source/actual inputs/current build stable. Exact selected files/command: `12-3-browser-20261027T090233692258Z-3ce40a03.json`. This is the named subset, not a complete 479-case invocation.
- These runs precede bounded review patches to verification/tooling and the storage-clear listener. Final post-patch gates follow below; earlier results are not relabelled.

### Review corrections

The focus checker now pairs unfocused/focused rendered pixels and checks the required perimeter area, with a negative permanent-outline probe. Text measurement composites supported alpha layers, restricts native modal measurements to active contents, checks inner clipping and reports unsupported surfaces explicitly. Checked native indicators use the measured dominant fill and a non-boundary glyph component rather than arbitrary palette pairs. Private Start/outcome/reader/recap focus traversal is extended. Individual calendar/time-picker/select/disclosure pixels remain unmeasured.

Generated test copies track owned names for stale-file pruning. Cross-tab storage clear returns other tabs to Day. The command runner snapshots actual inputs before launch, preserves durable raw evidence and cleans only its owned process tree on timeout. Original exploratory evidence and its recovery limits remain recorded above.

The first bounded post-review probes passed 4/5: native hover darkened the actual checked fill relative to declared accent, so the helper now uses the measured dominant fill and glyph rather than claiming exact accent equality. The isolated native positive/negative probe then passed 1/1. The next three representative journeys passed 1/3: a private editor button's focus ring was partly covered by its next opaque neighbor, and a disabled demo select had an unsupported opacity layer. Added vertical button spacing and an explicit opaque disabled-select palette; thresholds remain unchanged. These failed records remain intact. Subsequent complete requalification is recorded below.

Preservation observation: `12-3-preserved-runtime.json` records the original four healthy 12.1/12.2 container IDs and equal served demo HTML after normalizing line endings/trailing whitespace introduced by the original PowerShell capture. No exact old-database byte fingerprint was captured or inferred.

Reinspection found two residual verification defects: field-host clipping shared the internal-content exemption, and observed children could survive if the parent exited during cleanup. Both were classified separately as medium/patch. Commit `93293117199d6a2c2066b836af9b4d0b0cd9bc5c` fixes them with a clipped-host negative probe and creation-time-verified retained handles, including a deterministic real parent-exit test. All three original reviewers confirmed the bounded fixes and reported no new concrete issue. No technical review finding is deferred.

The earlier final-matrix attempt was intentionally interrupted at its verified owned launcher to apply these residual corrections; `12-3-browser-20261027T093740410315Z-828acca6.json` retains exit 1 and available partial raw results. It is not counted as a completed 34-case run.

### Final post-review gates

- Product implementation commit: `e66d80f8639bdccc7b81165f3b840342943d194c`; final verification corrections: `93293117199d6a2c2066b836af9b4d0b0cd9bc5c`. Final build/API/browser gates use the latter revision.
- Production TypeScript/Vite build: gate0, `12-3-build-20261027T094611979878Z-f682a751.json`.
- Actual HTTP/PostgreSQL: 74/74 passed, stable source, exit0, `12-3-real-20261027T094614581571Z-c5304066b095.json` and wrapper `12-3-verify-20261027T094614091424Z-076ff7b9.json`.
- Root tooling requalification: 3/3 passed, including an actual parent exit during cleanup; expected command exits 124/7 stay failures in the preserved records. See `12-3-tooling-final-after-review.log` and `12-3-probe-parent-exit-20261027T094630896379Z-2a365e0d.json`. Generator rename/pruning/preservation: 1/1 passed at e66d80f (`12-3-generator-final.log`); that generator is unchanged by 9329311.

No fresh complete backend-unit or 479-case private-browser run is claimed: backend sources are unchanged. The fresh 74 actual API/database controls and named browser selections verify the affected boundary; the 184-case pre-review regression and historical 477/479 record remain separate.

Visual inspection: root inspected the corrected actual focused button PNG (`12-3-focus-ring-fixed.png`) extracted from the recorded bounded run; the perimeter is fully visible. Earlier actual modal, recap and checkbox renders were also inspected. These are rendered desktop captures, not physical-device observations.

- Complete post-review task matrix: 34/34 passed in 628.356s, no skipped/unexpected/flaky cases, exit0; source, actual inputs and current build all match. Command: `python scripts/verify-story123.py browser tablet-pc.spec.ts tablet-pc-private.spec.ts tablet-pc-measurement-probes.spec.ts theme-clear.spec.ts`. Evidence `12-3-browser-20261027T094643980763Z-d69cbde3.json`; raw reports, focused/unfocused PNG pairs, actual copied tests/config and built assets have a verified durable bundle/index.
- Positive product measurements (deliberate negative probes excluded):312 states, 24,952 text observations (minimum 6.126:1), 6,584 boundaries (minimum 4.781:1), 5,880 keyboard-census observations and 5,600 hosts with actual unfocused signatures. 1,953 actual same-pixel pairs plus 3,647 explicitly representative cache results; minimum changed/required focus-area ratio 1.291, adjacent ratio 5.987:1, 3px width. No unmeasured product layers or critical clipping were reported.
- Native choices: 80 distinct checked/unchecked samples, edge minimum 10.131:1, 40 checked glyph components with pixels selected at >=3:1 against actual fill (minimum component area 63px). The earlier draft count 160 counted individual and aggregate attachments twice; raw records remain unchanged and the historical checkpoint now labels 80 distinct samples explicitly. The old arbitrary palette contrast is not used as final glyph evidence.
- Summary and reproducible aggregation: `12-3-measurement-summary.json`, `12-3-summary-method.py` (run from the worktree root with the browser manifest path). Desktop Edge 156, root text 16/32px, widths 800/1440px. Native calendar/time-picker/select/disclosure pixels, browser/OS zoom, assistive technology and actual Lenovo/Android/Brave remain unmeasured.

- Final affected regression: 37/37 passed in 43.137s, no skipped/unexpected/flaky cases, stable source/actual inputs/current build, gate0. Exact selected files: `fictional-assessment.spec.ts fictional-day.spec.ts private-access.spec.ts`. Evidence `12-3-browser-20261027T095721103382Z-836082f1.json`. This covers shared-theme entry, reset/privacy/no-network, keyboard order, real fictional save/reopen, login/logout/expiry/revalidation. The broader 184-case pre-review run remains separately identified.
- Final additive manual preparation: 17/17 passed without overwriting existing manual plans/edits (`12-3-real-20261027T100023374521Z-562920dd47b4.json`, wrapper `12-3-prepare-20261027T100022885739Z-5b66e626.json`).
- Verified preview PID 39552 serves 15323; final runtime 18/18 passed (`12-3-final-runtime.json`): served files match dist/source identity, own APIs/containers healthy, original four containers healthy with unchanged IDs, 15312 normalized HTML unchanged, local main unchanged and clean. Original DB-byte equality is not claimed. Credentials remain only in ignored local files; scanning all new evidence/archive members found neither manual nor database password.

## Exact final gate invocations

Run from the story worktree in PowerShell. Actual subprocess commands, paths, revisions, source/input/build hashes and raw exits are in the linked manifests.

```powershell
$py = 'C:/Users/Jonas/AppData/Local/Programs/Python/Python312/python.exe'
& $py scripts/verify-story123.py build
& $py scripts/verify-story123.py verify
& $py scripts/verify-story123.py browser tablet-pc.spec.ts tablet-pc-private.spec.ts tablet-pc-measurement-probes.spec.ts theme-clear.spec.ts
& $py scripts/verify-story123.py browser fictional-assessment.spec.ts fictional-day.spec.ts private-access.spec.ts
& $py -X utf8 scripts/test_verify_story123.py
node --test scripts/test-prepare-story123-tests.mjs
& $py scripts/verify-story123.py prepare
& $py scripts/verify-story123.py serve
```

Node's generator self-test ran at e66d80f; that file is unchanged by 9329311. Root tooling 3/3 ran at 9329311. `git diff --check` and local document-link/JSON checks passed. No complete fresh 479-case browser run, physical acceptance, main merge or push was performed.

## Remaining acceptance

Jonas must run [the short manual checklist](../story-12-3-manual-testing.md) and explicitly accept 12.3. 12.1/12.2 were subsequently accepted by Jonas on 27 October 2026; their checklist and historical results remain preserved. Actual Lenovo Pad/Android/Brave/mobile-network, native picker/marker pixels, OS/browser zoom and assistive-technology qualification remain open. Loopback 15323 is ready on this PC; no external route was activated. 12.4 remains backlog. E10-A4 persistence and E11-A4 visible-invoker focus are technically resolved, with no owner approval inferred.
