# Bussassistent V2 candidate

## Baseline

The candidate starts at local O6 merge `df3fc940a7f97bd632e230ddb38c2fa45e8d2bfb`. This merge combines the published main snapshot `26394835f27006d528a378a484485496d610f6e8` and the clean local O6 branch `b2ae125eab93d3964e2746a0efd13a3c03a369c6`. The O6 merge changed 29 documentation and evidence paths. Ninety new or modified local Markdown link destinations resolved; JSON, PowerShell parsing, the merge ancestry and unchanged product tree were checked. [Latest O6 source and risk disposition](evidence/o6-kernel-source-20261117.md).

The V2 worktree is `D:/IBE160/tmp/bussassistent-v2` on branch `codex/integrate-bussassistent-v2`. The requirements reconciliation pins the five historical plans. The isolated runtime uses fixed free subnets because Docker's default address pools were exhausted. The V2 test, regression and owner data stores are distinct from the assessment project. [Requirements and revisions](../_bmad-output/implementation-artifacts/v2-reconciliation.md).

## Current checkpoint

The product candidate adds pilot-week notice binding `ad6d93d`, explicit Owner route recheck `33a29b1` and full line 20 manual stop coverage `19e8fa2` on top of integration baseline `6dea92d`. Its integration commits are password `755b6f9`, password review `86a56eb`, automatic notices `fe42645`, frozen line 20 route references `b73b095`, restore and password follow-up `0b5d6f8`, shared geolocation and GPS speed `9240eac`, stop progression `4cf4475`, road limits `f7ac3ab` and regression fixes `6dea92d`. The final test-only credential navigation change is `e396e45` and the local Windows launcher correction is `89f8d72`. The local implementation and scoped verification are complete. Owner trials and positive qualification of still-missing operational datasets remain open.

## Local start

From this worktree in PowerShell 7, with Docker Desktop running.

```powershell
pwsh -NoProfile -File scripts/v2-local.ps1 -Mode Owner
```

Open `http://127.0.0.1:19661/private` on the PC. The owner project has fictional API `19662` and private API `19663` on loopback. In a second terminal from the same worktree, provision a disposable owner-trial account once. The terminal prompts for a local test password.

```powershell
docker compose -p ibe160-v2-owner -f compose.v2.yaml exec private-api python -m app.manage provision v2-owner-trial
```

The exact Owner command above was verified on Windows, including package installation, build, private API origin, secure Edge login page and a local sign image. The V2 environments were stopped after the tests and their volumes retained. The test and owner modes have distinct databases, volumes, bridge networks, credentials and build directories. `-Mode Test -ApisOnly` prepares the synthetic stack. `npm run test:v2-motion` from `frontend` runs the deterministic motion, stop and road controls on Node 24. End the foreground preview with Ctrl+C before running `-Mode Owner -Stop`.

The Owner preview reads the scoped Troms NeTEx source offline. The original observation expires on 21 November at 01:13:54 UTC. The verified 20 November recheck expires on 21 November at 03:14:38 UTC. For a fresh assessment of the 23–29 November operating dates, run an explicit check when starting the Owner trial.

```powershell
pwsh -NoProfile -File scripts/v2-local.ps1 -Mode Owner -RecheckRouteSource
```

The one-off check verifies the current public archive against the original seven-day corpus. Changed or incomplete facts require a separately reviewed pin. If the check fails, it reports the reason and preserves the last qualified receipt. Start Owner mode with the ordinary command to use retained evidence and view its age. Test mode rejects the switch. [Route qualification and verification](v2-route-p1.md).

Windows Edge Playwright supplies synthetic fixes on loopback. The Owner smoke check loaded the real local sign asset and private login, and confirmed a secure context and the geolocation API without starting it. The interactive browser integration could not attach in this session. An Android tablet needs its own secure origin plus its own Android and browser-profile permissions. Permission on Windows does not grant it on the tablet. For an already authorized USB debugging connection, reverse the local UI and private API ports with `adb reverse tcp:19661 tcp:19661` and `adb reverse tcp:19663 tcp:19663` and open the same loopback URL on the tablet. Verify a secure context and allow location on that origin in each chosen browser. A different mobile origin needs trusted HTTPS and its own configuration. No physical location was collected in this session.

## Verification status

- The final private PostgreSQL and API regression passed 648 tests. Six submission-only cases were skipped under their dedicated-environment gate. Fictional assessment and PDF checks passed 113 tests in the separate fictional database.
- Edge covered the 159-case regression set across the broad run and targeted follow-up on the same application build. The broad run passed 156 and found three password fixtures navigating before logout acknowledgement. After explicitly waiting for the server outcome and checking the cleared marker, all three passed. The nine new V2 browser cases passed in the broad run. A separate repeated-clock recap and route-recovery check both passed.
- TypeScript/Vite, 17 deterministic motion tests, 60 networkless Ubuntu helper/gateway tests and the marked restore commit/rollback test in real disposable PostgreSQL 17.11 passed. The tablet transport check covered 32 simulated browser cases earlier in the run. Real device behavior stays open.
- The manual stop coverage follow-up passed 31 targeted backend tests, four restore tests, TypeScript/Vite, 18 deterministic motion and projection tests, and seven Edge cases. The live API check with disposable credentials confirmed a manual anchor at call 80 and rejected a GPS write for that call. An initial test asserted a hash before applying the DTO's existing default fields. The corrected check passed against PostgreSQL. The earlier broad regression covers the integration baseline.
- The route recheck follow-up passed a broad private run of 605 tests with six submission-only skips before review fixes. After the fixes, 83 targeted backend tests, eight Edge cases and TypeScript/Vite passed. The actual live recheck observed the original archive generation. Byte-distinct equivalent and changed archives were verified offline. [Recheck implementation and review](../_bmad-output/implementation-artifacts/spec-v2-route-requalification.md).
- The pilot-week notice binding passed 97 targeted backend and PostgreSQL tests, three Edge cases and TypeScript/Vite. An independent XML count confirmed all seven dates for both lines. [Notice date qualification and review](../_bmad-output/implementation-artifacts/spec-v2-notice-pilot-dates.md).

| Area | Implementation | Evidence | Outstanding |
| --- | --- | --- | --- |
| O6 | Merged locally. V2 dependency and privilege review recorded. | 29 changed paths, 90 local links, JSON, PowerShell syntax and ancestry. Debian's exact util-linux source and applied patches were compared with the upstream advisory. | Four kernel findings plus open library and journal dispositions. Firmware remains deferred. [O6 source and V2 impact](evidence/o6-v2-source-reconciliation-20261120.md). |
| Password | Current 30-minute proof and SENDT workflow, password rotation, guarded recovery and resumable restore integrated. | Isolated HTTP/PostgreSQL, browser and gateway, 54 helper tests, PostgreSQL 17.11 marker commit/rollback with same rows and changed sequence. | Personal code handover, redemption and cross-device session invalidation. Installed SSH, systemd and actual maintenance-mount chain remain a separate gate. |
| Automatic notices | Read-only Entur collector and private association review. Source identities and exact revisions keep independent observations. | Owner live TRO cycle completed at 01:54:10 UTC on 20 November with eight situations over two pages. Verified pilot-week binding for lines 20 and 24. | Review against two representative workdays, including source updates, manual notices and navigation. [Source and decisions](v2-automatic-notices.md). |
| Route network | Dated P1 route lookup, manual decision, immutable confirmation, version comparison and explicit Owner recheck. | Both directions, nine active patterns and all seven dates. Journey counts 136, 136, 136, 136, 143, 109, 64. The live Owner recheck confirmed the original SHA-256. The Owner API froze a synthetic workday using the actual public 80-occurrence journey across midnight. | Run the check during the trial and label actual shift/departure pairs independently. P2 regional completeness stays outside the approved P1 plan. [Route evidence](v2-route-p1.md). |
| GPS speed | Shared foreground watch and independent own-speed display. | Deterministic and Edge controls use synthetic browser locations, including invalid/missing samples and watch lifecycle. | Physical Lenovo with Brave and Chrome for permission, stationary and moving behavior, accuracy and latency. |
| Position progression | Manual anchor, exact dated Quay gate, bounded evaluator and private operation receipts. New line 20 references pin exact manual mappings for all 120 Quays. | Synthetic fixtures cover revision, interval and overnight handoff. The public 80-call journey supported a manual save from the new mapping and rejected a GPS write. | Automatic progression on real routes requires dated coordinate evidence, an independently labelled route and a physical trial. Closing the whole workday view clears the pending local operation. Reopening loads the authoritative anchor. [Progression evidence](evidence/v2-position-progression.md). |
| Road limits | Qualified directed manifest adapter, separate current sign and 300 m next-limit logic. | Synthetic engine and API controls, five official sign JPEGs with hashes, 145-segment source recheck and 70→50 at R4. The dated archive compares the selected arc with the filter arm and identifies a line 42 negative control. | Obtain an independently confirmed journey through the selected arm or agree a separate test context for it. Lane and bus-turn evidence, temporary regulation and physical position uncertainty remain open. [Road source recheck](evidence/v2-road-source-20261120.md) · [Packaging contract](../backend/app/road_data/README.md). |

## Owner trial order

1. On the PC, use the disposable account to change its password, verify the other signed-in tab loses access, and try recovery with one hand-delivered local proof. A second terminal can issue the proof with `docker compose -p ibe160-v2-owner -f compose.v2.yaml exec private-api python -m app.manage recovery-issue v2-owner-trial`. Complete `SENDT` only after handover and use the normal login form after redemption. Keep production credentials and proofs out of the sandbox.
2. For automatic notices, confirm two representative workdays with line 20 and line 24 examples. Compare the manual notice register and automatic review, preserve a draft manual correction during navigation, and test that a review requires a fresh comparison when evidence changes. The verified automatic mapping covers 23–29 November. On the line 20 workday, review a dated journey in both directions and check stop order, repeated occurrences, partial range and the frozen copy. Use a new explicit route selection to check manual anchors with the full pilot mapping. Read the source age before evaluating the route outcome.
3. On the tablet, grant or deny location in the intended browser profile. Try explicit start, stationary and moving speed, Pause/Off, tab background/return, app settings, selection change and logout. Verify missing native speed displays an em dash and preview does not resume acquisition on its own. Capture results for Brave and Chrome separately.
4. After qualifying data is available, compare manual and automatic stop progression on the same known route and re-anchor after a missing or implausible fix. Test the road warning separately with a dated route that passes the selected arm and a qualified directed manifest. Compare the current sign and upcoming 300 m warning with physical signs while stopped or have a passenger record observations.
