---
title: 'Deliver current Tromsø public sources to the private application'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: ['docs/v2-field-trial.md']
---

<frozen-after-approval reason="human-owned intent">

## Intent

**Problem:** The private production network cannot collect SIRI and dated road data directly. Static NVDB facts can also become uncertain at an unverified boundary or during a reported regulation.

**Approach:** Use short-lived public collectors, validate bundles again inside the private importer, and keep the private API on its existing networks. Publish current-day directed NVDB interiors only where the same registered limit continues along a single named road and the supplemental situation snapshot is fresh.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Entur | Complete, bounded TRO SIRI cycle | Publish through the existing source revision writer | Preserve the last complete baseline after partial or failed cycles |
| Road interior | One continuous directed road and fresh supplemental observation | A registered limit may display on a qualified GPS match | Expired data, unresolved approaches and published works suppress it |
| Review already active | A fresh same-day area package is already published | The scheduled import preserves it | A forced refresh may replace it with a new version that needs review |
| Worker failure | Timeout or unrelated environment state | The specific public worker stops | Private traffic and storage stay on the existing networks |

</frozen-after-approval>

## Implementation Notes

- Ubuntu runs each public fetch in a short-lived, unprivileged worker without a mounted secret or a private-network interface. A bounded stream is validated again before private storage accepts it.
- The SIRI writer reserves each attempt before outbound traffic, applies the existing atomic revision writer and preserves the provider cooldown.

## Review Triage Log

- High, patched. The client enforces the source lease and upcoming published regulation times. Stable updates can renew the lease without reloading road geometry.
- High, patched. Automatic static values require a continuous, unambiguous direction on the same numbered road and skip unresolved endpoints.
- Medium, patched. The daily job preserves an existing same-day area and retries transient failures. Timeout cleanup targets only the uniquely named public worker.
- Medium, patched. The SIRI transport preserves long rate limits. A real disposable PostgreSQL test covers reservation, replay rejection, partial ingestion and complete baseline preservation.
- Medium, patched. Revision checks tolerate a relevant parent rerender and publishing a more recent full manifest between checks.

## Verification

- A complete real Entur TRO snapshot produced four records in one page and rejected replay in isolated PostgreSQL.
- The real authenticated test API showed 459, 1,199 and 1,084 direction-qualified registered edges in the overlapping Kvaløya, Tromsøya and Fastlandet packages with current WFS leases.
- Local motion replay on one distinct real edge in each sub-area displayed 60, 30 and 30 km/h respectively. Synthetic matcher cases verified the 300 m threshold, suppression and unaffected transitions.
