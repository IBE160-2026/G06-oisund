# Current V1 scope and operations — 31 October 2026

## Owner decision and status

Jonas explicitly confirmed that the completed Ubuntu integration is included in the final V1 delivery. This replaces the earlier decision to treat it as a separate bonus or possible v1.0.1. Those earlier instructions remain historical; they no longer define the current package. The five planned application extensions remain excluded.

| Area | Current status and source |
|---|---|
| Application, D1–D3, Epic12 | Complete and owner-accepted. [Personal acceptance](../evidence/v1-acceptance-2026-10-29.md), [main integration](../evidence/v1-main-integration-20261029.md). SCOPE-02 application scope is unchanged. |
| Ubuntu integration and handover | Complete, included in V1. [Operations guide](../ubuntu-server.md) and [dated operations log](../../.logs/jonas-oisund/990-2026-10-29-18-30-00-ubuntu-server.md). Jonas confirmed the integrated release's login/save test passed on 31 October. |
| Stability | Continue observation after the kernel update. Four successful boots and bounded recovery tests do not establish the earlier freeze's root cause or long-term stability. |
| Final delivery | Repository reflection preserved; [final control](../evidence/v1-final-control-20261031.md) qualifies the source/package/local recipe. Annotated `v1.0.0` is authorized. Open O3–O6 have explicit owner-approved follow-up after V1. Complete course submission remains separate; no GitHub release/deploy. |

## Two runtime setups

**Independent local assessment:** use the [root README](../../README.md) and `scripts/submission.mjs` from the exact delivery checkout. This creates isolated API/PostgreSQL services, synthetic data and a locally generated assessment login. The assessor needs no Jonas server, owner account, private documents/data, SSH credentials or Cloudflare access. Installation downloads the documented dependencies; runtime uses local loopback services. Including Ubuntu tooling does not make deploying it an assessment prerequisite.

**Integrated operational Ubuntu setup:** use [docs/ubuntu-server.md](../ubuntu-server.md). It describes the actual server, protected HTTPS/Cloudflare route, systemd services, Windows administration, backup, isolated restore and guarded deploy/rollback. Deployment credentials and production data are private and excluded from the repository. Do not apply the assessment seed/reset to production. Reading this documentation does not authorize operational actions.

## Source, deployment and evidence boundaries

| Reference | What it actually establishes |
|---|---|
| Historical `c067fdbb20150219c041588ed4e990e7b0ef6b94` | Accepted 12.5 snapshot, preserved unchanged. |
| C1 `3c2287ed68d0cbb1923439fc6ee00254395072a4` | Accepted corrected application and original test/tooling reference. Not the complete final delivery package. |
| `64f91a70f51b87188de9a3b68ca8ab7fa94c9dfb` | Application/main basis incorporated into Ubuntu integration in `6f845fa`; backend, frontend and tablet gate preserved, per the operations log. Ubuntu files/administrative scripts are additions, so the full tree is not identical to C1. |
| Operational `eb0eee3496d8999fb28615b49d4bf60124b6158f` | Earlier deployed release: [O1 and bounded O2](../evidence/access-operations-20261029.md), earlier reboot/crash/lid/network/Windows-off observations. Not rerun on later source by this document. |
| Operational `addd27b14fe4b26ef24d488d847d1c0d59a98946` | Last documented deployed integrated release: successful deploy → rollback to eb0eee3 → deploy, fresh isolated restore and health/backup checks. Jonas's integrated login/save acceptance was recorded on 31 October. |
| Published main `5dc64000e1f42a550875146e28ac43b363332606` | Historical remote main fetched at the earlier scope reconciliation. Includes handover/owner-test records and documented integrated-server-branch cleanup. Publishing this or later documentation does not deploy it. Use actual Git refs for subsequent publication; no final delivery SHA is assigned here. |

The integration log records 12 operations tests (only `os.chown` mocked in the non-root test), 23 gate tests, 4 cleanup tests, TypeScript/Vite, PowerShell parsing and actual Docker builds. Isolated restore initially failed, was corrected for ownership/readiness, then passed on old and new releases. Results retain their original environments/dates; no full application regression or renewed manual matrix is inferred. Earlier restore/recovery/reboot observations and their limits remain in the log.

## Final control source

Latest fetched main for the31October final control was `8e590735c495808ae51bf65523d7ab19c6dfb0fd`. Current tests/image proofs bind to that source. The selected final `v1.0.0` adds documentation/evidence and session logging only; resolve its full SHA from the annotated tag and verified remote peeled ref. The server was independently read as still `addd27b14fe4b26ef24d488d847d1c0d59a98946`; no deploy was performed. [Full checks and evidence](../evidence/v1-final-control-20261031.md).

## Remaining decisions versus operational observation

L2 repository reflection review is complete and the approved text is unchanged. L3 disposition and L4/L5 source/package/recipe checks are complete. Jonas authorizes annotated `v1.0.0` after the publication checks; L1/L7 course logistics, proposal/solo approval, assessor access and later complete submission remain open. See [current checklist](delivery-readiness.md).

O3–O6 remain **open within their documented residual limits, with explicit owner-approved operational follow-up after V1**. Concrete bounded passes are distinguished from unverified external timing, WAN/IPv6, actual OS DNS cancellation and broader security assurance. No concrete V1-blocking defect was found. The server's libc6 reboot-required marker and long-term stability remain operational maintenance/observation. No new application/server acceptance or invented soak-duration gate is introduced.
