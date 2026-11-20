# Bussassistent V2 candidate

## Baseline

The candidate starts at local O6 merge `df3fc940a7f97bd632e230ddb38c2fa45e8d2bfb`. This merge combines the published main snapshot `26394835f27006d528a378a484485496d610f6e8` and the clean local O6 branch `b2ae125eab93d3964e2746a0efd13a3c03a369c6`. The O6 merge changed 29 documentation and evidence paths. Ninety new or modified local Markdown link destinations resolved; JSON, PowerShell parsing, the merge ancestry and unchanged product tree were checked. [Latest O6 source and risk disposition](evidence/o6-kernel-source-20261117.md).

The V2 worktree is `D:/IBE160/tmp/bussassistent-v2` on branch `codex/integrate-bussassistent-v2`. The requirements reconciliation pins the five historical plans. The isolated runtime uses fixed free subnets because Docker's default address pools were exhausted. The V2 test, regression and owner data stores are distinct from the assessment project. [Requirements and revisions](../_bmad-output/implementation-artifacts/v2-reconciliation.md).

## Current checkpoint

The product candidate is `6dea92d`. Its integration commits are password `755b6f9`, password review `86a56eb`, automatic notices `fe42645`, frozen line 20 route references `b73b095`, restore and password follow-up `0b5d6f8`, shared geolocation and GPS speed `9240eac`, stop progression `4cf4475`, road limits `f7ac3ab` and regression fixes `6dea92d`. The final test-only credential navigation change is `e396e45` and the local Windows launcher correction is `89f8d72`. The local implementation and scoped verification are complete. Owner trials and positive qualification of still-missing operational datasets remain open.

## Local start

From this worktree in PowerShell 7, with Docker Desktop running:

```powershell
pwsh -NoProfile -File scripts/v2-local.ps1 -Mode Owner
```

Open `http://127.0.0.1:19661/private` on the PC. The owner project has fictional API `19662` and private API `19663` on loopback. In a second terminal from the same worktree, provision a disposable owner-trial account once. The terminal prompts for a local test password.

```powershell
docker compose -p ibe160-v2-owner -f compose.v2.yaml exec private-api python -m app.manage provision v2-owner-trial
```

The exact Owner command above was verified on Windows, including package installation, build, private API origin, secure Edge login page and a local sign image. The V2 environments were stopped after the tests and their volumes retained. The test and owner modes have distinct databases, volumes, bridge networks, credentials and build directories. `-Mode Test -ApisOnly` prepares the synthetic stack. `npm run test:v2-motion` from `frontend` runs the deterministic motion, stop and road controls on Node 24. End the foreground preview with Ctrl+C before running `-Mode Owner -Stop`.

The scoped NeTEx source is read from `.private-runtime/route/troms-netex-1795129398375617.zip` in Owner mode. Its pinned SHA-256 is `03662d51c1438514d1695e632c598a7ea589d5384a19804658212fc4af0af8b9`. The local acquisition timestamp is retained separately from the two XML publication timestamps. The preview marks this observation stale from 21 November at 01:13:54 UTC. A fresh assessment during the 23–29 November operating window requires new source qualification.

Windows Edge Playwright supplies synthetic fixes on loopback. The Owner smoke check loaded the real local sign asset and private login, and confirmed a secure context and the geolocation API without starting it. The interactive browser integration could not attach in this session. An Android tablet needs its own secure origin plus its own Android and browser-profile permissions. Permission on Windows does not grant it on the tablet. For an already authorized USB debugging connection, reverse the local UI and private API ports with `adb reverse tcp:19661 tcp:19661` and `adb reverse tcp:19663 tcp:19663` and open the same loopback URL on the tablet. Verify a secure context and allow location on that origin in each chosen browser. A different mobile origin needs trusted HTTPS and its own configuration. No physical location was collected in this session.

## Verification status

- The final private PostgreSQL and API regression passed 648 tests. Six submission-only cases were skipped under their dedicated-environment gate. Fictional assessment and PDF checks passed 113 tests in the separate fictional database.
- Edge covered the 159-case regression set across the broad run and targeted follow-up on the same application build. The broad run passed 156 and found three password fixtures navigating before logout acknowledgement. After explicitly waiting for the server outcome and checking the cleared marker, all three passed. The nine new V2 browser cases passed in the broad run. A separate repeated-clock recap and route-recovery check both passed.
- TypeScript/Vite, 17 deterministic motion tests, 60 networkless Ubuntu helper/gateway tests and the marked restore commit/rollback test in real disposable PostgreSQL 17.11 passed. The tablet transport check covered 32 simulated browser cases earlier in the run. Real device behavior stays open.

| Area | Implementation | Evidence | Outstanding |
| --- | --- | --- | --- |
| O6 | Merged locally. V2 dependency and privilege review recorded. | 29 changed paths, 90 local links, JSON, PowerShell syntax and ancestry. Debian's exact util-linux source and applied patches were compared with the upstream advisory. | Four kernel findings plus open library and journal dispositions. Firmware remains deferred. [O6 source and V2 impact](evidence/o6-v2-source-reconciliation-20261120.md). |
| Password | Current 30-minute proof and SENDT workflow, password rotation, guarded recovery and resumable restore integrated. | Isolated HTTP/PostgreSQL, browser and gateway, 54 helper tests, PostgreSQL 17.11 marker commit/rollback with same rows and changed sequence. | Personal code handover, redemption and cross-device session invalidation. Installed SSH, systemd and actual maintenance-mount chain remain a separate gate. |
| Automatic notices | Read-only Entur collector and private association review. Source identities and exact revisions keep independent observations. | Owner live TRO cycle completed at 01:54:10 UTC on 20 November with eight situations over two pages. Focused tests cover durable request spacing and review safeguards. | Review against a representative workday, including source updates, manual notices and navigation. [Source and decisions](v2-automatic-notices.md). |
| Route network | Dated P1 route lookup, manual decision, immutable confirmation and version comparison. | Both directions, nine active patterns and all seven pinned dates. Journey counts 136, 136, 136, 136, 143, 109, 64. The Owner API froze a synthetic workday using the actual public 80-occurrence journey across midnight. | Fresh version for a later trial and independently labelled actual shift/departure pairs. P2 regional completeness stays outside the approved P1 plan. [Route evidence](v2-route-p1.md). |
| GPS speed | Shared foreground watch and independent own-speed display. | Deterministic and Edge controls use synthetic browser locations, including invalid/missing samples and watch lifecycle. | Physical Lenovo with Brave and Chrome for permission, stationary and moving behavior, accuracy and latency. |
| Position progression | Manual anchor, exact dated Quay gate, bounded evaluator and private operation receipts. | Synthetic end-to-end and PostgreSQL fixtures cover revision, interval and overnight handoff. The NSR archive had exact coordinates for all 120 expected Quays, with unverified service-date validity. | Automatic progression on real routes requires dated coordinate evidence, an independently labelled route and a physical trial. Closing the whole workday view clears the pending local operation. Reopening loads the authoritative anchor. [Progression evidence](evidence/v2-position-progression.md). |
| Road limits | Qualified directed manifest adapter, separate current sign and 300 m next-limit logic. | Synthetic engine and API controls, five official sign JPEGs with hashes, scoped NVDB R4 observation of 70→50. | Current directed lane/turn/bus-access coverage and a calibrated error model are still required before real road values and warnings can be activated. [Road evidence and packaging contract](../backend/app/road_data/README.md). |

## Owner trial order

1. On the PC, use the disposable account to change its password, verify the other signed-in tab loses access, and try recovery with one hand-delivered local proof. A second terminal can issue the proof with `docker compose -p ibe160-v2-owner -f compose.v2.yaml exec private-api python -m app.manage recovery-issue v2-owner-trial`. Complete `SENDT` only after handover and use the normal login form after redemption. Keep production credentials and proofs out of the sandbox.
2. Confirm a sample workday. Compare its manual notice register and automatic review, preserve a draft manual correction during navigation, and test that a review requires a fresh comparison when evidence changes. The verified automatic mapping covers line 20 and 24 for 23–24 November. Review a dated line 20 journey in both directions and check stop order, repeated occurrences, partial range and the frozen copy. Use source age to interpret the result.
3. On the tablet, grant or deny location in the intended browser profile. Try explicit start, stationary and moving speed, Pause/Off, tab background/return, app settings, selection change and logout. Verify missing native speed displays an em dash and preview does not resume acquisition on its own. Capture results for Brave and Chrome separately.
4. After qualifying data is available, compare manual and automatic stop progression on the same known route and re-anchor after a missing or implausible fix. Qualify the directed road manifest before checking the current sign and upcoming 300 m warning against physical signs. Examine the UI while stopped or have a passenger record observations.
