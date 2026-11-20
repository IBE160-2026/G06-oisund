# Bussassistent V2 candidate

## Baseline

The candidate starts at local O6 merge `df3fc940a7f97bd632e230ddb38c2fa45e8d2bfb`. This merge combines the published main snapshot `26394835f27006d528a378a484485496d610f6e8` and the clean local O6 branch `b2ae125eab93d3964e2746a0efd13a3c03a369c6`. The O6 merge changed 29 documentation and evidence paths. Ninety new or modified local Markdown link destinations resolved; JSON, PowerShell parsing, the merge ancestry and unchanged product tree were checked. [Latest O6 source and risk disposition](evidence/o6-kernel-source-20261117.md).

The V2 branch is `codex/integrate-bussassistent-v2`. The independent [V2 requirements reconciliation](../_bmad-output/implementation-artifacts/v2-reconciliation.md) pins the source plans. Work is currently in the password integration and isolated regression stage. TypeScript/Vite passed on the integrated password source. The first Docker start exhausted its default subnet pool, resolved for V2 by allocating specific independent subnets.

## Local start

From this worktree in PowerShell 7, with Docker Desktop running:

```powershell
pwsh -NoProfile -File scripts/v2-local.ps1 -Mode Owner
```

Use the printed private application address on the PC. The owner project uses UI `19661`, fictional API `19662`, and private API `19663` on loopback. Create only disposable accounts using the isolated container's account management tool. The test and owner modes have distinct databases, volumes, bridge networks, credentials and static build directories. `-Mode Test -ApisOnly` prepares the separate synthetic test stack. `-Mode Owner -Stop` stops only the owner stack and retains its volumes.

The tablet needs its own secure test origin and permission on the device/profile used. Windows Edge Playwright proved synthetic geolocation on loopback. Physical tablet, native speed, operating-system location permission, actual road signage and GPS accuracy remain personal trials.

## Verification status

| Area | Implementation | Evidence | Outstanding |
| --- | --- | --- | --- |
| O6 | Merged locally | Document links, structural checks, evidence JSON, PowerShell syntax | Named kernel, library and journal residuals remain open, under the same scoped disposition. |
| Password | Reviewed source integrated in V2 | TypeScript/Vite passed. Isolated regressions in progress. | Personal SENDT and redemption, SSH/helper and full candidate acceptance. |
| Automatic notices | Preparing first story | Three public requests confirmed page continuity for one full TRO snapshot. Dated 20/24 identities confirmed for 23–24 November. | Product implementation and representative workday qualification. |
| Route network | Preparing P1 | Exact Troms NeTEx generation inspected; line-20 templates available on seven proposed dates. | Product implementation, calendar closure and separately labelled matching examples. |
| Position, road speed limit and GPS speed | Pending | Synthetic Edge geolocation smoke only. | Implementation and controlled physical owner trials. |
