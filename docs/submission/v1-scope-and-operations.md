# Current V1 scope and operations — 31 October 2026

## Owner decision and status

Jonas explicitly confirmed that the completed Ubuntu integration is included in the final V1 delivery. This replaces the earlier decision to treat it as a separate bonus or possible v1.0.1. Those earlier instructions remain historical; they no longer define the current package. The five planned application extensions remain excluded.

| Area | Current status and source |
|---|---|
| Application, D1–D3, Epic12 | Complete and owner-accepted. [Personal acceptance](../evidence/v1-acceptance-2026-10-29.md), [main integration](../evidence/v1-main-integration-20261029.md). SCOPE-02 application scope is unchanged. |
| Ubuntu integration and handover | Complete, included in V1. [Operations guide](../ubuntu-server.md) and [dated operations log](../../.logs/jonas-oisund/990-2026-10-29-18-30-00-ubuntu-server.md). Jonas confirmed the integrated release's login/save test passed on 31 October. |
| Stability | Continue observation after the kernel update. Four successful boots and bounded recovery tests do not establish the earlier freeze's root cause or long-term stability. |
| Final delivery | Repository reflection approved; course confirmation, O3–O6 disposition, exact version freeze/recipe check and later tag/submission remain in [L1–L7](delivery-readiness.md). No tag/release or submission is performed by this decision. |

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
| Published main `5dc64000e1f42a550875146e28ac43b363332606` | Latest remote main fetched at reconciliation start. Includes handover/owner-test records and documented integrated-server-branch cleanup. Publishing this or later documentation does not deploy it. Use actual Git refs for subsequent publication; no final delivery SHA is assigned here. |

The integration log records 12 operations tests (only `os.chown` mocked in the non-root test), 23 gate tests, 4 cleanup tests, TypeScript/Vite, PowerShell parsing and actual Docker builds. Isolated restore initially failed, was corrected for ownership/readiness, then passed on old and new releases. Results retain their original environments/dates; no full application regression or renewed manual matrix is inferred. Earlier restore/recovery/reboot observations and their limits remain in the log.

## Remaining decisions versus operational observation

L2 repository reflection review is complete: [approved text](ai-reflection.md). L1 course requirements/access and separate course-report requirements remain unresolved; L4/L5 final source and necessary startup verification follow before later authorized tag/submission. Existing evidence does not establish a new blocking application or server-integration defect.

O3–O6 remain **open / not qualified**, and L3 cannot close without actual results or explicit disposition. They track external request/timing coverage, WAN/IPv6 observation, pre-socket DNS cancellation and bounded broader OS/dependency/security assurance. Follow-up is not evidence of failure and does not by itself establish a mandatory course-delivery gate. Determine any actual delivery impediment from a concrete failed control or confirmed course requirement; otherwise record the owner's explicit disposition as continuing operational follow-up. No deferral is approved here. Long-term stability remains observation, without an invented soak-duration requirement. Neither these open points nor the scope update reopens accepted D1–D3/Epic12 or completed server handover.
