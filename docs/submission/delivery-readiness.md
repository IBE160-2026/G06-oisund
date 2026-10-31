# V1 freeze and remaining course delivery

Updated 31 October 2026. Application/D1–D3/Epic12 and Ubuntu integration/handover are complete and owner-accepted. The approved repository reflection is unchanged. Steps 4 and 5 are qualified in the [final control report](../evidence/v1-final-control-20261031.md). No concrete V1-blocking defect was found. Jonas explicitly authorizes an annotated `v1.0.0` on the controlled commit and its push, without another confirmation. O3–O6 remain open within the limits below, with approved operational follow-up after V1.

## Version and package

The tested start/source is `8e590735c495808ae51bf65523d7ab19c6dfb0fd`, the fetched latest main. Final publication adds only documentation/evidence/byte attributes and a separate session-log commit. The selected immutable delivery reference is **`v1.0.0^{commit}`**; obtain its exact full SHA with `git rev-parse 'v1.0.0^{commit}'` and verify the remote peeled tag. The publication receipt/final response supplies that SHA. A tag cannot embed its target commit's own hash inside that commit.

The accepted application/original tooling remain Git-identical to C1 `3c2287ed68d0cbb1923439fc6ee00254395072a4`. Ubuntu additions are included and equal their accepted deployed-source files; Access diagnostics are a separately reviewed addition. The full package is not identical to C1. Last observed server release remains **`addd27b14fe4b26ef24d488d847d1c0d59a98946`**; tagging/pushing does not deploy. Historical `c067fdb` and original results remain unchanged. [Version map](v1-scope-and-operations.md).

Only tracked source/locks/migrations, examples, documentation and evidence belong in the package. A–E/facts are synthetic; the nine established anonymized historical fixtures are retained with their explicit privacy limits. Private originals, course PDFs, the separate Norwegian report, generated credentials, runtime state, database dumps/backups, dependency/build directories and local checkouts are excluded. [Inventory and bounded history audit](../evidence/v1-final-control-20261031/inventory.json). Sensor startup generates an independent local synthetic account and requires no Jonas server/account/Cloudflare access.

## Delivery checklist

| ID | Actual status | Evidence / remaining responsibility |
|---|---|---|
| L1 | **Partly confirmed; course logistics remain open.** Original project-suggestion PDF and Part 1 assessment guide read in full. | [Original-source mapping](../evidence/v1-final-control-20261031.md#original-course-material-actually-available) confirms the seven criteria, 70/30 split and clean-environment README expectation. Exact deadline, channel/attachments, approved proposal/solo permission and assessor-account Git access are not established by those files. No date or approval invented; these remain course-submission follow-up, not a demonstrated project-V1 defect. |
| L2 | **Complete.** Approved English repository reflection incorporated unchanged in e861625. | [ai-reflection.md](ai-reflection.md) unchanged in this work. Historical text/proposal preserved; separate Norwegian report neither edited nor declared accepted. |
| L3 | **Disposition complete; operational proof limits remain open.** | Concrete O3–O6 controls and limitations below. Jonas explicitly allows remaining evidence limits without a demonstrated V1-blocking defect to continue after V1. This does not mark them passed. |
| L4 | **Controlled source and package complete.** | Full input manifest, approved reflection equality, Ubuntu-source equality, tracked-file/history checks and final staged identity check. `v1.0.0` selects the final docs/log commit; exact SHA comes from Git/remote receipt. |
| L5 | **Bounded current recipe check complete.** | Fresh separate 8e59073 clone, four explicit project/port translations, uncached init, five healthy services, generated login/B import/save/reload/reopen, actual image/served-file proof. 44 existing containers and 20 volumes unchanged. [Results](../evidence/v1-final-control-20261031.md#delivery-content-and-current-recipe). Historical C1 lifecycle/reset/full journeys reused at their own version; no new restart/reset performed. |
| L6 | **Annotated v1.0.0 authorized for this controlled snapshot.** | Local/remote name must be free; fast-forward main push, annotated tag push and remote peeled-SHA equality are the publication gate/receipt. No moving/replacing an existing tag, force-push or GitHub release. |
| L7 | **Open: complete course submission later.** | Use actual course channel/format and deadline, verify assessor access and retain receipt. V1 tag does not claim coursework submission, report completion or teacher approval. |

## Unperformed operational checks — separate chat

This stable heading is retained for existing links. The current status is the following concrete register, superseding earlier unapproved-deferral wording without changing historical outcomes.

| ID | Status and observed scope | Remaining boundary / disposition |
|---|---|---|
| O1 | **Passed at Cloudflare edge**, 29 October, operational `eb0eee3`: same genuine token passed before expiry and was redirected after actual expiry. | [Original report](../evidence/access-operations-20261029.md). No independent origin-gate observation or newer-source rerun. |
| O2 | **Passed for active member excluded by exact email policy**, operational `eb0eee3`, with documented team-domain change and fresh owner MFA. | Original report; no positive allow-B or general MFA matrix. |
| O3 | **Partial bounded passes; open after V1.** Four current unauthenticated edge GETs, fresh local generated-login/save/reopen and three local Origin/CSRF refusals; historical C1 proxy/recovery evidence retained. | Authenticated external cookie/cache/error combinations, physical device/network-loss and actual write/receipt timing remain unverified. [Cases and exact versions](../evidence/v1-final-control-20261031.md#o3--admission-app-protection-writes-and-recovery). Owner-approved follow-up; no exhaustive matrix claimed. |
| O4 | **Bounded read-only observations; independent WAN/IPv6 remains open after V1.** | Local listeners/public-DNS/HTTPS and Ubuntu ULA/no-default-route observation do not prove router/firewall/direct-origin WAN exposure. No external scanning vantage used. [Scope](../evidence/v1-final-control-20261031.md#o4--network-exposure). |
| O5 | **Synthetic pre-socket bound/recovery passed; actual OS DNS cancellation remains open after V1.** | Caller about3.265s, one worker, recovery after explicit resolver release. A truly stuck resolver's slot is not proven cancellable. [Fixture and measurements](../evidence/v1-final-control-20261031.md#o5--resolver-before-socket-ownership). |
| O6 | **Bounded checks passed; broad assurance remains open after V1.** | npm/OSV advisory lookups and heuristic history scan found no matches; no full OS/image/supply-chain/penetration certification. Server `libc6` reboot-required marker and long-term stability remain maintenance follow-up. [Boundaries](../evidence/v1-final-control-20261031.md#o6--bounded-assurance-not-exhaustive-closure). |

All open O3–O6 boundaries have Jonas's explicit 31 October disposition as operational follow-up after V1. No concrete finding currently prevents V1. A future actual failure must be evaluated on its own facts; this disposition is not approval to ignore a demonstrated defect. Completed application/server acceptance is not reopened by missing exhaustive proof. No deployment, restart, router/access-rule change or production-data write occurred in this work.
