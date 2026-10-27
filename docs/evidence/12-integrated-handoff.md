# Story 12.1 + 12.2 local integration — 27 October 2026

Jonas har ikke gjennomført manuell/fysisk akseptansetest av Story 12.1 eller Story 12.2. Teknisk integrasjon og automatiske tester innebærer ikke brukeraksept. Begge avventer Jonas sin testing.

Both stories are integrated in local main. Required affected checks pass after the recorded corrections; the broad-run and rerun results are distinguished below. Both stories retain review/in-review and pending owner acceptance. [Manual checklist and startup](../story-12-manual-testing.md).

## Preserved work and conflict decisions

- Main began clean at `85bf56e` (the previous status log); both story branches still pointed at `0bae548` with implementation and logs uncommitted. Actual status and requirements were read again.
- 12.1 implementation secured as `8428b87`, original log as `533ca88`; 12.2 implementation as `8be5ccd`, original log as `e8221ff`. Story worktrees remain present and clean after these commits.
- Integration branch `integration/story-12-1-and-12-2` was created from main. 12.1 was merged first (`94f9a20`), then 12.2 (`b54246f`). No destructive reset, force push, worktree deletion or remote mutation.
- `issues.md` append conflicts were resolved by preserving both sides, including historical entries. No existing log text was deleted.
- Sprint conflicts retain `epic-12: in-progress` and both story keys in `review`; neither story was reset to backlog by the other's branch. The 12.1 technical follow-up resolutions remain distinct from story acceptance.
- The add/add cached Epic 12 context uses the more detailed 12.2 version covering simulation, private isolation and independent notice lifetime. Current authorization/dependency facts are updated separately; no product contract changed through this cached summary.
- `frontend/src/main.tsx` merged automatically; root checked that both the demo link/dispatch and 12.1's VITE_FICTIONAL_API override remain. Vite keeps separate main/demo production entries. Private creation uses server-issued admission, fixed original identity and lookup-first recovery.
- Discovered integration defect: fictional backend CORS/write boundary was hardcoded to 5173 despite configurable frontend API endpoints. `FICTIONAL_ORIGIN` now configures both boundaries, preserving the existing 5173 default. A real HTTP regression checks configured-origin preflight/write acceptance and unrelated-origin denial.
- All new execution uses project `ibe160-story12-integration`, frontend15312, fictional18312, private18313, separate databases/volumes and ignored secrets. Existing ordinary, tablet and prior story services are preserved.

## Current execution record

Previous 441 backend / 479 private browser / 14 demo browser / 18 fictional backend passes belong to the old separate story runs. They are historical evidence only. Fresh `12-integrated-*` and `12-integration-real-*` files record this run independently, including source hashes, exact commands and exit codes. Raw regression output is retained under ignored `tmp/story12/<run>/command.log`.

- Integrated TypeScript/Vite production build passed, exit0, source unchanged (`12-integrated-build-20261027T064448323119Z-56a80416.json`).
- Runner unit gate: first attempt failed with sandbox TEMP permission errors (not a product failure); rerun outside sandbox passed all11, exit0 and source unchanged (`12-integrated-checks-20261027T064527545201Z-69ac5f3e.json`). Original failure retained.
- Fresh isolated runtime startup passed (`12-integration-real-20261027T064728151092Z-86b370a42d03.json`).

## Verification commands

Use the local Python312 executable shown in the checklist. Commands executed in `D:\IBE160`:

```powershell
& $py scripts/verify-story12-integration.py up
& $py scripts/verify-story12-integration.py verify
& $py scripts/verify-story12-checks.py checks
& $py scripts/verify-story12-checks.py build
& $py scripts/verify-story12-checks.py backend
& $py scripts/verify-story12-checks.py fictional
& $py scripts/verify-story12-checks.py serve
& $py scripts/verify-story12-checks.py demo
& $py scripts/verify-story12-checks.py browser
& $py scripts/verify-story12-integration.py prepare
```

The final results section will distinguish completed commands from commands still pending. Demo and private tests use disposable copies with only endpoints, Compose project, fixture-relative paths and capture destinations translated. Original assertions and historical evidence are preserved. No automatic desktop browser result constitutes Jonas' manual test or physical device qualification.

## Known limits and acceptance

The simulation has a fixed three-activity sample, edits duty/bus and does not perform actual PDF extraction or full activity authoring. Legacy missing-ending illustration has no completion action in the simulation. Actual notice API checks are separate from simulated receipts. Broader theme persistence, physical Lenovo/Android/Brave/mobile-network and full later-story acceptance are not claimed here. Seven-day retention and late-write races use deterministic synthetic boundaries; no seven-day wall-clock soak is claimed.

Both stories await Jonas' testing. No push is authorized by this request.

### Actual notice integration — fresh results

`12-integration-real-20261027T064911344742Z-b902dce83cff.json`: all74 checks passed,31 commands, exit0, unchanged source. Tests use real HTTP/PostgreSQL, not the simulation adapter. They establish owned server admission, original replay/receipt equality, altered/unknown/foreign/expired rejection, lost accepted acknowledgement recovery, exactly two notices/receipts for two original operations, original-day deletion independence, real database/API restart, fictional reset/reseed preserving private fingerprints and notice receipts, retained notice expiry, purge and original-command non-resurrection.

The first actual attempt (`12-integration-real-20261027T064755822109Z-63726a89efd0.json`) closed the socket before commit. The server cancelled the disconnected request, so lookup correctly remained unknown. The corrected test keeps the request connection alive without reading until separate authorized lookup proves commit, then discards the acknowledgement connection and verifies original recovery/replay. It does not describe pre-dispatch cancellation as a lost accepted save. Both runs are preserved.

### Final source-stable gate results so far

- Private backend/domain/PDF:441 passed, one existing TestClient deprecation warning,578.69s, exit0, unchanged source. Evidence `12-integrated-backend-20261027T064948493354Z-f202adce.json`.
- Actual fictional API/PostgreSQL:19 passed in1.27s, including configured-origin CORS/write rejection; exit0, unchanged source. Evidence `12-integrated-fictional-20261027T065950321183Z-6a3239e7.json`.
- Final runner safety/failure evidence:29 passed, exit0, unchanged source. Evidence `12-integrated-checks-20261027T070258481916Z-d56ce628.json`. Includes wrong config/workspace/volume/non-synthetic refusal, interrupted preparation, survivor preservation, failure cleanup, missing input, launch error and timeout recording.
- Final production build: exit0, unchanged source, `12-integrated-build-20261027T070007620473Z-1c649eae.json`. Root preserved existing keyboard save order by moving the new demo link after the controls.
- Simulation + actual fictional browser:27 passed in19.6s, exit0, unchanged source and actual executed-copy/config hashes; `12-integrated-demo-20261027T070259848595Z-23226e76.json`. Fourteen are no-network/GPS/persistence demo cases; thirteen exercise the actual fictional API, saved reload, same-ID recovery, malformed responses and expiry.
- Final patched actual verifier:73 checks passed,31 commands, exit0, unchanged source; cleanup passed for both invocation-owned accounts. Evidence `12-integration-real-20261027T070322665523Z-0d84a62f41ae.json`. Reset now compares complete rows of all24 private tables rather than only selected fields.
- Independent review: all three reviewers reinspected. Negative refusal tests were hardened after reinspection to assert the precise boundary failure; deletion mutation probes confirm each guard's test fails. No retained review finding remains.

Historical integrated browser attempts remain visible: the first run passed13 actual fictional cases but failed14 demo navigations because the copied demo allowlist still named15222; only the disposable endpoint translation changed. The second passed all27 but returned gate2 because the negative-test file changed concurrently. The final unchanged-source27-case run above is the qualifying evidence. No original assertion or historical screenshot was replaced.

### Canonical Git references

| Work | Full commit |
|---|---|
| Original shared base | `0bae54833f38dc3dbf041d54c324c220618c21da` |
| Main at integration start | `85bf56ef48271868df2c486d883c43081180f2ff` |
| 12.1 implementation | `8428b8724c64ce67638ed32665af455566bcd2da` |
| 12.1 original session log | `533ca88dc2c99533eb5c11f6bb58d6ee4fe7bde8` |
| 12.2 implementation | `8be5ccde2ffca671366e1e1a1a836bd504b73e65` |
| 12.2 original session log | `e8221ff3a61a86beaa5d42c91b9a4c4df69e28f6` |
| First integration merge (12.1) | `94f9a2006457c7196322804276b95226a12dce01` |
| Second integration merge (12.2) | `b54246fdb4fc6cc6318c63b4705de4961586f41c` |

The current integrated product has no backend source changes after the stable441-case gate; subsequent changes were frontend link placement and verification/evidence tooling. Those affected surfaces were rebuilt and covered by final19 fictional API,29 runner and27 fictional browser cases. Final private browser source/config/test hashes are recorded separately on completion.

### Broad private browser gate and corrected readiness regression

The unchanged-source complete private gate ran all479 cases:477 passed,2 failed in42.7minutes, exit1 (`12-integrated-browser-20261027T070429483741Z-c2e3abf1.json`). Both failures were actual API stop/start cases in `private-recovery.spec.ts` (202 and287). The application correctly kept private content hidden when the restarted API was not yet reachable; the integration Compose configuration lacked API healthchecks, so `start --wait` returned on Running instead of HTTP/DB readiness.

Root added the same HTTP health probe used by the original private Compose configuration to both integration APIs. The original edge reviewer reinspected and retained no concern. No application code or assertion changed. Root recreated only the integration services, then reran the entire affected27-case `private-recovery.spec.ts` suite:27 passed in2.2minutes, exit0, source and executed inputs unchanged (`12-integrated-browser-20261027T074751748130Z-d6a9f226.json`). Both prior failures now show `private-api Healthy` before access revalidation succeeds.

This is477 passes from the broad run plus successful requalification of the complete affected suite after the readiness fix. It is not a claim that one subsequent479-case invocation was green. The remaining477 cases' product/fixture/test inputs are unchanged; the only later runtime change adds API readiness waiting. The failed broad run is retained in full.

### Final repeated recovery and preparation

The two formerly failing restart cases were each repeated three times:6 passed in1.1minutes, exit0, unchanged source/actual executed inputs (`12-integrated-browser-20261027T075109651895Z-29e1f512.json`). This directly qualifies the newly added readiness semantics under repeated real container suspension/startup. No test expectations were weakened.

After that, the actual integration verifier passed all73 checks again, cleanup passed for both temporary accounts (`12-integration-real-20261027T075218361742Z-f830090568b7.json`). `prepare` passed all22 checks and created the synthetic manual account and two line20 plans (`12-integration-real-20261027T075246959307Z-1d98f0b7e4bd.json`). Credentials remain only in ignored `.private-runtime/story12-manual-credentials.json` and were not emitted to evidence. Preparation is additive and preserves existing plans/edits on repetition.

Runtime/build audit passed after the final readiness configuration:61 backend/migration/test files in each actual API equal host SHA256; their writes predate API startup. Served main/demo HTML and referenced JS/CSS equal the built files. API Date and no-store are present. Evidence `12-integrated-runtime-20261027T075328678549Z.json`.

Technically complete within12.1/12.2. No retained product/review defect remains. Broader private coverage is the documented477 broad passes plus all27 affected recovery cases requalified and both restart cases repeated6times; a second complete479-case invocation was not run. Later12.3/12.4 device/theme/end-to-end obligations are not marked complete. Jonas' manual/physical testing of both stories remains open. The checklist is ready at `docs/story-12-manual-testing.md`; the prepared runtime is loopback15312/18312/18313, not the ordinary or tablet deployment.

## Final local main handoff

- Integrated implementation/evidence commit: `4d678513267eeb16ca35f5646401ccab80885ddd`.
- Local main merge: `f13d28991ac85934826f0da7b7b81fbc09181f24`. Git ancestry checks confirm both story tips and the integrated implementation are contained in main. Both original story worktrees are still clean and present; no worktree was deleted. origin/main remains `0bae54833f38dc3dbf041d54c324c220618c21da`. Nothing pushed.
- Final checks were rerun from main itself:29 runner cases (`12-integrated-checks-20261027T075808010055Z-3e276d3e.json`), production build (`12-integrated-build-20261027T075809865447Z-91a668a2.json`),19 fictional API cases (`12-integrated-fictional-20261027T075815182833Z-fe8266db.json`) and27 fictional browser cases (`12-integrated-demo-20261027T075818122580Z-b53434a4.json`) all passed, exit0 and unchanged inputs. The final bundle filenames/hashes match the qualified pre-merge build.
- Actual main API/PostgreSQL verification passed73 checks again, including reset preservation of the already prepared private manual data (`12-integration-real-20261027T075841579333Z-4115139dc3aa.json`). Additive preparation recheck passed17 checks and preserved the two existing plans (`12-integration-real-20261027T075910401880Z-9b71b3d7ad80.json`). No manual account password was reset.
- After actual API restart, main runtime/build audit passed:61 files per API match host bytes, source writes predate startup, and served main/demo HTML/JS/CSS match dist (`12-integrated-runtime-20261027T075918536192Z.json`). The preview is running on15312 (verified task-owned process49248); both isolated APIs are ready on18312/18313.
- Final technical status:12.1 and12.2 are `review` / `in-review`, owner acceptance pending. No outstanding technical integration or retained review defect within these stories. The documented simulation scope limits and later device/theme work remain. Session log and issues preserve the still-open manual/physical acceptance.

Use the checklist, not the ordinary5173/8000/8001 or old tablet deployment, for this integrated build. Start at <http://127.0.0.1:15312/demo> or <http://127.0.0.1:15312/private>. Read credentials locally from the ignored file named in the checklist.
