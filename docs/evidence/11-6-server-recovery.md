# 11.6 — Recover from an unavailable server

## Current integrated delivery — 26 October 2026

This section supersedes the older current-status statements below. They remain historical evidence. Corrected 11.5 was explicitly accepted by Jonas; 11.6 is **done and owner-accepted on 26 October 2026**. Epic 11 is done with a completed accepted-with-open-items retrospective; detailed manual observations remain unreported. No acceptance, physical-device pass, commit, push or Epic 12 work is inferred.

The accepted 11.5 correction changed notice ownership, lifetime and operation authority. A notice belongs to the account; its original day is optional provenance. Recovery therefore uses account receipt/current-record authority across day switches, day deletion/expiry and legacy provenance becoming NULL. Validity ending, seven-day historical retention, source checking and manual ending remain distinct. Receipt lookup proves a historical effect; it cannot overwrite a newer revision or revive a terminal incident. The existing cross-day/legacy/current-comparison regressions are included in the fresh combined run.

Integration inspection found and repaired three product boundaries:

- HTML/proxy 409/422 responses could discard an uncertain original notice command after a committed save; a malformed 429 could throw in the error handler. Only exact known API write rejections now settle rejection. Failure of the receipt/current read preserves the original operation and proposal, including repeated attempts.
- A delayed response previously restarted notice validity from response arrival. Maintenance and reader now count request elapsed time immediately against the returned server timestamp, using a monotonic clock. The conservative estimate can hide a near-ending notice slightly early by up to request duration; it never grants extra validity. The server remains authoritative for writes.
- Maintenance filtering and returned server_now now share one database instant, avoiding a page contradicting its own retention timestamp at a boundary.

**Effect on already accepted 11.5:** proxy failure and delayed-response behavior is corrected, including the brief expired-active display. Cross-day identity, required ending, pre-expiry extension, separate source checking and terminal history remain as accepted. Include the corrected failure and expiry behavior in the owner's manual check; no new acceptance is recorded here.

### Exact version and fresh execution

Git HEAD: `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed`, branch `main`, empty index. Results apply to the complete dirty working tree identified by [the integration source manifest](11-6-integration-source-2026-10-26.json), not to HEAD alone. Manifest SHA256: `1e0101380841d712125ce999a36d3f20dc43dfe66de253ae22016679111524e5`. It freezes application, migration, test, verifier and build configuration bytes. Product/test/build files are not changed after this checkpoint. Documentation updates are separate. Served frontend: `index-DE5vJ8Ms.js` / `index-8lnBnkIq.css`.

| Execution | Observed result |
|---|---|
| Initial integrated gate | Deliberately interrupted after 78 backend progress dots for the established review defect; incomplete, not a pass. Finally restored services/data. Log: `tmp/11-6-integration-full.log`. |
| Verifier restoration controls | 7 passed in 0.256s; synthetic stubs, no ordinary data mutations. |
| Focused corrected account API/PostgreSQL | 10 passed in 16.82s; existing TestClient dependency deprecation warning. |
| New browser integration regressions | 7 passed in one 1.1m invocation. HTML 409/422/429 after real commit; repeated typed-looking lookup rejection; one original effect; absent create across ending with no resend; lost accepted check after automatic ending; held reader/maintenance response across ending. Log: `tmp/11-6-integration-focused.log`. |
| Fresh final complete gate | **421 backend tests passed in 526.37s; all 479 browser cases passed in one invocation (38.9m)**. Populated restart, repeated migrations, exact raw state/receipt/deadline/session preservation, cleanup and TypeScript/Vite build passed. One existing TestClient dependency deprecation warning; no product/test failure. |
| Review | All three required independent BMAD layers completed; every finding individually triaged in the 11.6 specification. Original reviewers reinspected the patches/tests. No retained finding remains open or deferred. The previously recorded extreme device-clock session timer limitation remains separate. |
| Preservation and local runtime | All 120 frozen implementation/test/build files unchanged. All 1004 initial files retained, 390 historical artifacts and 24 original fixture/source/oracle files byte-preserved; 26 frozen contract blocks unchanged. Original fields/rows of all **24 ordinary tables**, database identity and secret preserved; only three expired throttle rows were removed by existing startup cleanup. Ordinary services healthy, synthetic services stopped. Served HTML/assets and 44 backend/migration files match tested bytes. Retro draft unchanged. |

Fresh complete log: `tmp/11-6-integration-final-full.log`. Earlier 411/456 and 420/472 outcomes below and in the 11.5 report remain their own historical code checkpoints. They are not used as passes for this tree.

Fresh current-run captures, separately named while historical originals remain byte-preserved: [11-5-crossday-register-390-day](11-6-integration-11-5-crossday-register-390-day.png), [11-5-crossday-reader-night-768](11-6-integration-11-5-crossday-reader-night-768.png). Root inspected the Day register, Night reader and narrow Night recovery renders; automated geometry/contrast/focus checks remain separate from physical qualification.

### Historical frozen-contract control

The existing byte-sensitive control in `tmp/11-5-crossday-final-checks.py` remains unchanged. Independent comparisons against the pre-11.6, pre-cross-day and current-resumption copies found **24/25/26 frozen blocks respectively, with no mismatches**, including line endings. Thus no current historical contract needs repair. The earlier reported message `Historical frozen contract changed` cannot be reproduced from the preserved checkpoints. No failing filename, divergent bytes or failed-run snapshot was retained with that earlier report, so its precise historical trigger cannot be established; it would be unsupported to call it a product defect or assert a newline explanation. The control checks documentation bytes, not runtime acceptance. It has neither been removed nor weakened.

### Current manual environment and short test list

Jonas selected **desktop locally in a browser** in this chat. Browser name/version and actual results remain to be recorded by Jonas. Automated evidence uses Windows desktop Edge **156.0.4314.42**, Playwright **1.64.1** and Node **24.19.0**; it is not a manual result. Planned later platform remains **Lenovo Pad / Android / Brave / mobile network → desktop server at home**. Jonas schedules remote-access setup **between Epic 11 and Epic 12**. No remote access is configured or required for this local acceptance test.

Preserve unsaved input in old tabs before switching to this build. Docker Desktop must be running. From PowerShell:

```powershell
Set-Location D:\IBE160
docker compose -p ibe160-fictional-assessment up -d --wait
docker compose -p ibe160-private-work -f compose.private.yaml up -d --wait
```

Open **http://127.0.0.1:5173/private** and use the existing account. Existing database volumes and the local secret are retained; no reset/reprovisioning is needed.

1. **Normal save:** use a clearly named test draft, save, close/reopen and refresh online. Expect exactly the saved fields/revision. Editing again must show unsaved state; activity selection, source check and shift Start/End must not happen automatically.
2. **Actual outage:** enter a distinct change and leave the page open. Run `docker compose -p ibe160-private-work -f compose.private.yaml stop private-api`, then attempt saving. Expect retained input and unavailable/unresolved feedback. Run `docker compose -p ibe160-private-work -f compose.private.yaml up -d --wait private-api`. Without reloading, explicitly check/retry the original attempt. Expect one saved effect, retained intended fields and no duplicate. Stopping before save tests outage; the controlled committed-lost-reply case is covered by automation above, not inferred from this step.
3. **Newer data in two windows:** open the same saved draft or notice in two windows. Retain a local proposal in the first and save a different value in the second. Try saving/recovering the first. Expect a comparison/conflict, both values retained and no silent overwrite. Deliberately adopt the newer saved value or explicitly compare and save the reviewed proposal.
4. **Cross-day notices:** register one test notice with an ending after two relevant confirmed days. Consult both days. Expect one shared notice where exact line/interval filters match. Edit/check it once; both days consult the same updated entry. Switch days with unsaved notice text: it must remain available when returning to maintenance.
5. **Ending and extension:** for a separate test notice use an exact Oslo ending a few minutes ahead. Save an extension before the old ending and verify it on both days. For another short-lived notice, let its ending pass: the reader hides it, maintenance shows **Utløpt**, and no edit/check/extension can revive it. A reader plan must overlap the validity interval; a future plan correctly does not match a notice ending today. Repeated refresh/recovery must not restore active display.
6. **Check/manual ending during outage:** repeat the outage/recovery step from notice maintenance with an edited notice, then separately with **Kontrollerte kilden nå** and **Avslutt avvik manuelt**. Expect explicit original-attempt recovery, one effect and refreshed facts. Manual ending remains terminal and separate from source checking; neither certifies road clearance. Unavailable reading must say unavailable rather than imply an empty fresh result.
7. **Leave warning:** with unsaved text, try leaving/reloading and cancel the browser warning. Expect text retained. If you deliberately leave, only the server-saved copy can be reopened. Check Day/Night, enlarged text and reachable controls in the actual desktop browser.

Record browser/version, scenario pass/fail/not-run, expected versus actual result, and any error text. **Manual acceptance of 11.6 is pending.** Send the observations and a separate explicit approval when satisfied. Retrospective finalization waits for that response.

---


**Subsequent owner feedback, 26 October 2026:** The owner rejected 11.5's per-shift notice scope. The statements below that no correction was needed describe the earlier checkpoint, before that feedback. The [11.5 cross-day correction and current notice test steps](11-5-crossday-register.md) supersede notice ownership/ending instructions here: register once for the account, require an ending, extend before expiry, and distinguish automatic expiry from manual ending/source checking. Existing 11.6 recovery work is preserved; this correction does not restart that story or record owner acceptance.

Implemented, independently reviewed and served locally. Technical verification is complete; story/sprint is **review**, and manual owner acceptance remains **pending** for both 11.5 and 11.6. The existing 11.5 delivery remains separately documented in [11.5 evidence](11-5-line-date-notices.md); no 11.5 product correction was needed.

Final evidence: **411 API/PostgreSQL tests passed**, populated restart/repeated migration and build passed, and all **456 browser scenarios have passing coverage**. The full browser invocation was **453/456**; three test-fixture/harness failures were corrected without changing product code, then all eight affected cases passed three times (**24/24**). This is explicitly not a claim of one all-green 456-case invocation. All retained review findings are resolved; none is deferred. Ordinary services are healthy, disposable services stopped, and data/secrets/historical evidence are preserved. No staging, commit, push, retrospective or next epic.

For hands-on testing, start with [environment startup](#start-the-correct-local-environment-for-manual-testing-115-and-116) and [concrete walkthroughs](#manual-test-steps-and-expected-results). [Final verification and failure classification](#final-verification-and-failure-classification) records exact results and remaining limits.

[Specification](../../_bmad-output/implementation-artifacts/spec-11-6-recover-from-an-unavailable-server.md) · [Implementation plan](../../_bmad-output/specs/spec-11-6-recover-from-an-unavailable-server/implementation-plan.md)

## Previous-story continuity (11.5)

Before changing product code, the 106-file final 11.5 manifest matched source exactly. Actual logs confirm 411 backend passes, 424/426 browser cases including all 26 reader cases, followed by 24/24 corrective checks of eight scenarios affected by the documented helper race. No missing automatic evidence or unresolved blocking defect was found. No 11.5 correction was necessary. Pending manual acceptance remains yours.

## Preservation baseline

The initial local tree is retained in ignored `tmp/11-6-initial-tree` with a SHA256 manifest for 892 files. Fresh ordinary-state fingerprints cover all 23 tables, database container identity and secret without emitting private records. Mutation fixtures use only `ibe160-private-tests` synthetic data. Final restoration and verification results are recorded below.

## Start the correct local environment for manual testing (11.5 and 11.6)

The planned physical platform is **Lenovo Pad, Android, Brave**, using **the mobile network to reach the server on the desktop at home**. This physical/device/network test is still **not performed**. Existing automated browser results use desktop Edge/Playwright and do not qualify this setup. iPad/Safari is not the planned acceptance platform; earlier references to it remain historical untested-device statements.

Run the startup commands below on the desktop at home. On the tablet, use the existing configured remote address for that server and the private workspace; desktop `localhost` addresses in this guide are local checks, not addresses that reach the desktop from the tablet. Remote ingress configuration is not changed or verified by this documentation correction. Follow the normal/outage/retry/recovery steps below from Brave over the mobile network and record actual observations separately. Report receipt does not constitute acceptance of either story.

Use PowerShell from `D:\IBE160` with Docker Desktop running. Use the private workspace, not the no-login fictional page:

```powershell
Set-Location D:\IBE160
docker compose -p ibe160-private-tests -f compose.private.yaml stop
docker compose -p ibe160-private-work -f compose.private.yaml up -d --build --wait
docker compose -p ibe160-fictional-assessment up -d --build --wait frontend
docker compose -p ibe160-private-work -f compose.private.yaml ps
```

Open **http://127.0.0.1:5173/private** and use your existing private login. The private API is **http://127.0.0.1:8001/health**; port 8000 belongs to the separate fictional assessment. Explicit `-p` selects the intended project even if an old `COMPOSE_PROJECT_NAME` variable is present. Keep the ordinary database volume and `.private-runtime/postgres-password`. Before refreshing an older tab, copy any unsaved text you want to keep: recovery is in page memory only.

For manual mutation checks, use a clearly marked test draft/day with future planned dates, or an existing retained test day. Do not use an expired plan. Keep this guide open separately. Test while stopped.

## Manual test steps and expected results

### Normal use and 11.5 reader

1. Open or create a test draft. Change a field and save. Expect a saving state followed by a verified saved state. Reopen the saved draft online and check the saved value.
2. Open a confirmed test day. Choose an activity, then **Manuelt vedlikeholdte avvik**. Register a notice with a title, two exact confirmed lines (for example `20, 24` only if those lines exist in the plan), a short/detailed explanation and an SMS source description; leave URL and validity unknown. Expect one saved notice, unknown validity and **Ikke kontrollert**.
3. From the day choose **Les avvik for linjer og datoer**. Expect one shared row listing both matching lines. Filter line and planned Oslo calendar date; expand the complete source facts. A separate incident with the same title must remain separate. A known non-overlapping validity stays in maintenance but is excluded from this reader. Unknown or partial validity stays qualified. Empty results never establish clear roads.
4. Return to the day. Expect the same manual activity choice. Repeat in Night mode and at a narrow window size. Navigation and reading must not Start, complete an activity, check a source or end a notice.

### Server unavailable before saving

1. In an open draft, type a recognizable test change. Keep the page open. In another PowerShell window run:

   ```powershell
   docker compose -p ibe160-private-work -f compose.private.yaml stop private-api
   ```

2. Try saving. Allow the request deadline to expire. Expect unavailable/unconfirmed feedback, or private content hidden because session authority cannot be checked. Never expect a saved claim. The page retains memory; do not refresh or sign out.
3. Restore the server:

   ```powershell
   docker compose -p ibe160-private-work -f compose.private.yaml up -d --wait private-api
   ```

4. If shown, choose **Kontroller tilgang igjen**. Expect the same session's retained input. If the save never dispatched, save explicitly. If a pending command exists, use its check/retry controls. Expect one saved result and the correct value after online reopen. Merely restarting the server must not automatically save.

### Unknown result and retry

A stopped API before saving demonstrates an outage; it cannot reliably produce a committed write with a lost acknowledgement. The automated recovery tests deliberately forward a real write and discard its response to test that case deterministically.

1. For an unresolved command, keep the page open and use its **Kontroller …** control. If the server is still unavailable, expect **uavklart**, retained input and the same pending attempt. A failed lookup must never claim **ikke lagret**.
2. Once connected, choose **Prøv samme … igjen**. The application checks the original operation before sending it again. If already accepted, expect recovery without another effect; otherwise only the original identity and content may be retried. Confirm exactly one notice/draft and no extra revision/check/ending.
3. For a stale revision, open the same draft/notice in two windows. Save a change in window A, then attempt to save the older proposal in B. Expect rejection/conflict with B's text retained and newer saved facts available for comparison. Compare explicitly before adopting a saved version or submitting a reviewed proposal. Do not expect an automatic merge or force overwrite.

### Notice outage, source check, manual ending and reader recovery

1. In notice maintenance, open a new or edited notice and enter text. Stop only the private API as above. Try saving, then restore it without refreshing. Recover access/operation explicitly. Expect retained text and exactly one saved effect.
2. Open the line/date reader while the API is unavailable. Expect an unavailable state, without stale candidate results presented as current and without an empty-list success claim. Restart the API, recover access if needed, then refresh the reader. Expect current saved facts and unchanged activity selection.
3. Repeat a controlled interruption around **Kontrollerte kilden nå** and **Avslutt avvik manuelt** on a test notice. Only a verified explicit check may set the source-check time; manual ending must not imply road clearance. Recover the original attempt, then refresh maintenance and reader. Expect one check/ending effect, truthful status and retained unknown validity. The automated lost-response tests cover the exact after-commit boundary.
4. With an unsaved proposal or unresolved attempt, try reloading/leaving. Expect the browser's loss warning where supported. Cancel to retain it. Deliberately refreshing after confirmation loses page-only input; online reopen must show the last server-saved version. No offline recovery copy is promised.

## Troubleshooting

- If port 8001 is occupied, check both explicit projects with `docker compose -p <project> -f compose.private.yaml ps`; stop the disposable API before starting ordinary services.
- If the private page hides content, restore the API then choose **Kontroller tilgang igjen**. Do not reload just to reconnect. A changed/expired login legitimately clears private presentation.
- If saving remains unresolved, check service health and use the original operation's check control. Do not create a replacement record to guess whether the first one saved.
- To reproduce automated faults, select only the disposable project and run the commands recorded with final test results below. The test guard refuses databases containing ordinary accounts. Do not bypass it.

## Known limits and manual acceptance

Private input survives only in the still-open page, under the same authorized session. Reload, tab closure, browser/process crash, session expiry/account change and deliberate discard may lose it. No offline restart, automatic retry, source feed, automatic conflict merge or tablet-hardware guarantee is included. Browser failure injection and actual server stop/start are distinguished in the test results. Physical iPad/Safari, touch hardware, assistive technology and browser chrome zoom remain untested unless explicitly recorded later. The inherited 11.5 reader bound is 400 planned calendar dates and 200 saved notices. Manual acceptance of both 11.5 and 11.6 remains pending; no acceptance is recorded for the owner.

## Verification checkpoints and corrections

- Continuity: 106/106 final 11.5 source/test/verifier hashes match. No separate 11.5 correction was required.
- Isolated verifier control tests: `uv run --no-project python -m unittest scripts/test_verify_private_drafts.py` — **7 passed in 0.208s**; subprocesses are stubbed, so this is restoration-control evidence rather than a product/browser test.
- The initial combined worker tool invocation stalled before launching tests. Root interrupted it, inspected service/process/test state and took over sequential command execution; no unknown test process remained. The disposable API/frontend were healthy and ordinary API was stopped for the port handoff.
- First focused browser diagnostic (`tmp/11-6-focused-recovery-first.log`) passed the first immutable-command recovery case, then exposed a new test locator attempting to find the hidden upload-screen refresh button through an accessibility-role lookup. Root stopped the repeated variants after confirming that shared harness failure. This interrupted diagnostic is not counted as a completed suite; its failures are retained. Product status/command assertions were not weakened.

## Implementation decisions

The recovery integration reuses existing server operation and revision contracts; no migration or private persistent browser storage was added. Drafts check original operation status before retry, validate known rejection details and fetch current data after a valid receipt. A historical receipt followed by newer data retains the form proposal for comparison; adopting a server version rereads it online. Draft-list failures have their own visible list error and cannot overwrite save semantics.

Draft and confirmation saves use server-issued operation identities: recovery checks their authorized operation status, and only a valid pending status permits an explicit retry of the original command. Notice, activity/lifecycle, selection, bus and deletion commands use client-created identities: recovery checks the receipt first; an authoritative absent-receipt response permits an explicit retry only after a valid live current-target read. Failed or malformed lookup/current responses do not permit resend. Existing expected revisions and same-command identity remain the final protection against races. Reconnecting alone sends no mutation. Valid acceptance followed by failed current/receipt reads remains unconfirmed rather than a claimed rejection.

Newly edited notice content cannot retain a previous saved status message. When a recovered outcome has subsequently been corrected elsewhere, the saved outcome and original local proposal remain available for comparison; cancelling that proposal accepts the displayed newer saved value without a write. Existing tests now expect no second POST when status lookup already finds acceptance. Before-acceptance tests still assert exact original payload/identity on actual resend.

The 17-case focused checkpoint passed **15**, including the literal 10-second request deadline, six committed-write proxy failures, newer-draft comparison, typed rejection and four enlarged recovery renders. Two new harness issues were corrected: an actual stopped API correctly hides unauthorized content, so the test must assert the visible access state before restoration; and notice retry tests must wait for each request to settle before removing a fault route. The failed run remains in `tmp/11-6-focused-recovery.log`. A complete corrected focused run follows; these 15 passes do not relabel that checkpoint green.

## Focused gate before independent-review patches

- `tmp/11-6-focused-final.log`: **19 passed in 1.5m** across the new recovery matrix and both newer-outcome recovery variants.
- `tmp/11-6-reader-recovery-extension.log`: **1 passed in 11.2s**, proving create/check/manual-end recovery followed by unavailable reader refresh, hidden stale results, restored current facts and exact saved-notice invariance.
- `tmp/11-6-affected-contracts.log`: **15 passed in 1.0m**, covering malformed draft listing with retained form status and existing lost create/check/end notice cases under lookup-first retry.
- Production build passed after outcome-proposal preservation. Runtime assets at this checkpoint: `index-48KBwT8q.js` / `index-8lnBnkIq.css`.

Four recovery captures use 390/768 CSS-pixel widths, Day/Night and 200% root text. Root visually inspected Night 390 and Day 768: messages, wrapping, disabled fields and recovery controls are readable with visible focus and no horizontal page overflow. Measured text contrast is at least 10.0056; recovery-control text/boundary and focus checks pass with a 3px outline. Measurements describe desktop Edge automation, not physical hardware. Later review adds representative notice/outcome states before the final gate.

All three independent BMAD layers completed on the recorded full diff. The [specification's review triage](../../_bmad-output/implementation-artifacts/spec-11-6-recover-from-an-unavailable-server.md) records every finding individually. Accepted copy, async/revision guard and test gaps were corrected within scope; no finding is deferred. The suggested maximum-date reader trigger requires an impossible confirmed plan because confirmation requires final-end-plus-seven-days, so it is refuted for the public path. No 11.5 product correction was necessary.

## Independent reinspection

All three original reviewers inspected their corrections and confirmed resolution. The blind reviewer withdrew the maximum-date reader finding after checking the confirmation retention constraint, and found no remaining concrete defect. The edge reviewer confirmed confirmation copy, deletion status lookup and generation/epoch protection. The verification reviewer confirmed the added authorization-gate tests and aligned retry expectations. No finding is deferred. Root separately runs actual tests; static review alone is not a test pass.

A new held-current-plan test keeps the future confirmed plan and session live while source expiry changes the editor's authority epoch. The old response cannot open the plan; a new explicit lookup can. This covers the added async guard without depending on logout/unmount or expiry of the returned plan itself.

## Post-review focused gate

Root executed **64 cases, all passed in 5.1m**, on the reviewed source: `tmp/11-6-root-review-patches.log`. This includes all new recovery cases, failed/malformed current-target authorization, the exact-payload revision race, fresh preflight failure with zero write dispatch, contradictory/regressed comparison reads, source-expiry authority change during confirmation, actual API restart with dirty notice input, accepted-receipt recovery without extra POST across existing controllers, and enlarged notice/outcome renders. The original reviewers independently confirmed their retained findings resolved. No finding is deferred.

Root also visually inspected the new Night 390 notice recovery and Day 390 outcome recovery images. Long messages wrap; form/command states remain distinct; recovery controls and focus stay available. Measurements under the eight `11-6-recovery-*.json` files cover the four draft states and representative notice/outcome Day/Night states; final minima and bounds follow the complete gate.

## Full-gate reproduction

The canonical full disposable gate can be run from `D:\IBE160`:

```powershell
$env:COMPOSE_PROJECT_NAME = 'ibe160-private-tests'
try {
    uv run --no-project python -u scripts/verify-private-drafts.py
} finally {
    Remove-Item Env:COMPOSE_PROJECT_NAME -ErrorAction SilentlyContinue
}
```

It stops the ordinary private API while port 8001 is needed, uses synthetic-only disposable data, runs API/PostgreSQL and populated restart/migration checks, builds frontend, runs all Playwright tests, then stops disposable services and restores ordinary private services in `finally`. It refuses ordinary-account fixtures. Before a broad rerender, preserve existing `docs/evidence` PNG/JSON files if you need to keep historical screenshots byte-identical.

Root's delivery run uses ignored `tmp/11-6-full-gate.py` to freeze source hashes and archive/restore historical renders around this same gate. Its scratch copy changes only the final browser command's stdout capture to inherited streaming output, with identical `npx.cmd playwright test` arguments and unchanged checks/finally restoration. The tracked verifier is unchanged by 11.6. Full output: `tmp/11-6-root-full-gate.log`. Results and ordinary-state comparisons are recorded after actual completion below.

## Additional two-window activity-status recovery check

On a synthetic active shift, select one activity and save a manual outcome. Use a second window to record a different saved outcome for that same stable activity. If the first window has an unresolved earlier save, recover that original operation after reconnecting. Expect the latest saved value to be shown separately from the retained original proposal. Compare them explicitly: **Avbryt ulagret aktivitetsstatus** keeps the newer server value without another write; a deliberate later save submits the reviewed proposal against the current revision. Neither selecting another activity nor reconnecting may automatically register an outcome, start or end the shift.

## Final verification and failure classification

On resuming after the mobile application's external-run warning, root inspected the existing process and logs first. The full gate had completed with exit 1; it was not still running. The warning alone does not identify a product failure. No completed broad suite was restarted.

| Layer | Actual result |
|---|---|
| Agent/remote execution | Earlier delegated tool calls stalled before tests started; root took over sequential execution. The completed full-gate log and its exit status were recovered successfully. No test process remains active. |
| Test environment | Disposable API/PostgreSQL tests, populated restart, repeated migrations, exact raw state/receipt/deadline/session preservation, cleanup and production build passed. Ordinary services were restored in `finally`; disposable services are stopped. |
| Product and test assertions | Full gate passed **411 backend tests in 488.49s** and **453/456 browser cases in 34.6m**. Three browser assertions required fixture/synchronization corrections described below. No product source changed after that full run. |
| Corrective verification | The eight affected browser cases passed three times each: **24/24 in 1.6m**. Together with the full-run passes, all 456 cases have passing coverage; there was no single all-green 456-case invocation. |

Full output is retained in [the full-gate log](../../tmp/11-6-root-full-gate.log); original failed-browser artifacts are retained in `tmp/11-6-full-gate-failures`. Corrective output is in [the corrective log](../../tmp/11-6-root-corrective-browser.log). These ignored local logs accompany this working tree and are not committed artifacts.

The three failures were distinguished from product defects and independently reinspected:

- **R1:** the old 413 fixture supplied `Too large` instead of the API's exact known rejection detail. The uncertain classification was correct. The fixture now uses the real API detail and still checks editable input and a corrected save.
- **R2:** the old future-time fixture forged receipt timestamps while the current read supplied contradictory real timestamps. The corrected test puts the browser clock 60 seconds behind the server, keeps timers running and verifies real, consistent receipt/current data.
- **R3:** the proxy-404 test removed its failed-lookup fault before that request had settled and could target a submit control as it changed from retry to normal save. This is a reachable harness interleaving; the log alone does not prove its exact ordering, and no automatic product redispatch was established. The test now waits for the aborted lookup and settled retry state, waits for background refresh, counts every draft-create/update POST and asserts one original ID, revision 1 and the exact saved record.

Only `private-drafts.spec.ts` and `private-recovery.spec.ts` changed after the full run. All six proxy variants share the corrected synchronization, which is the concrete reason to repeat five previously passing variants alongside the three failed cases. Backend, production build and the other browser cases were not rerun. All 102 frozen source/test/migration/script files stayed unchanged during each gate; the manifests differ only in these two test files. Independent review has no unresolved or deferred finding.

| Recovery contract | Executed evidence |
|---|---|
| Ordinary save and reopen | Existing full draft/notice/lifecycle suites; editable dirty state cannot claim saved. |
| Timeout and preflight failure | Real 10-second browser request deadline before backend forwarding; failed preflight with zero write POSTs. |
| Accepted write with lost reply | Real committed writes followed by proxy 409/422/404/410/413/503; failed status lookup, explicit recovery, one original effect and no extra POST. |
| Safe original-command retry | Absent receipt requires a successful valid authorized current read; failed/malformed reads forbid resend; a competing revision conflicts without overwriting. |
| Newer data and authority changes | Retained draft/outcome proposals, regressed/contradictory comparison rejection and held confirmation read across source-expiry authority change. |
| Notices from 11.4–11.5 | Lost create/check/manual-end replies, actual API stop/start retaining dirty notice fields, unavailable reader refresh then restored current facts and unchanged saved records. |
| Access and loss | Same-session suspension/recovery, identity/expiry guards, page-loss warning and explicit cancellation; no persistent private browser recovery copy. |

Final read-only preservation checks confirm all **23 ordinary tables**, original PostgreSQL container identity and secret unchanged. All **892 initial files** remain present; **293 historical render/measurement files** and **18 example/oracle/source files** are byte-identical. The broad run archived/restored 150 rerendered files. Served public/private HTML and all dist assets match the tested build (`index-KEcKN3rM.js`, `index-8lnBnkIq.css`); **43 runtime backend/migration files** match source. HEAD remains `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed`, with an empty index. No staging, commit or push occurred.

Eight new recovery PNG/JSON pairs cover draft 390/768 Day/Night and notice/outcome 390 Day/Night at 200% root text. Measured minima: text/control text **6.1263:1**, focus **11.4501:1**, control boundary **4.7814:1**, control height **90.59375px**, outline **3px**, with no horizontal overflow. Root visually inspected representative draft, notice and outcome images; keyboard focus remains visible and unobscured. Browser root-text enlargement is not browser chrome zoom. Physical iPad/Safari, touch and assistive technology remain untested. Theme persistence remains an existing Epic 12 follow-up; no next-epic work was started.

11.5 continuity required no product correction; its prior results and pending manual acceptance remain separately recorded in its delivery report. 11.6 technical work is complete and locally served. Specification remains **in-review**, story/sprint **review**, and owner acceptance of both stories remains **pending**. No retrospective was performed.

Owner acceptance update, 26 October 2026: Jonas explicitly accepted corrected story 11.5 (`Godkjent.`). Its account-owned cross-day/expiry delivery is done; existing 11.6 remains review. Earlier pending-acceptance statements describe historical checkpoints. This does not authorize commit/push or further work, finalize the retrospective, close Epic 11, or establish physical-device qualification.


## Owner acceptance - 2026-10-26

Jonas explicitly approved the integrated 11.6 delivery and instructed completion of the Epic 11 retrospective, including the preliminary work from the other chat. The accepted source manifest remains unchanged. Selected manual environment was local desktop browser; detailed scenario results/browser version were not supplied and are not invented. No physical Lenovo/Android/Brave/mobile-network test is inferred. Remote access is scheduled between Epic 11 and Epic 12. No commit/push or Epic 12 implementation is authorized. Earlier pending statements remain historical.
