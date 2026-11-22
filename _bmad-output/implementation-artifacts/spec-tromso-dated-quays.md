---
title: 'Dated platform versions for Tromsø'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: ['docs/v2-field-trial.md']
---

<frozen-after-approval reason="human-owned intent">

## Intent

**Problem:** The county snapshot lacks individual platform validity dates. A timetable call can identify its platform without establishing which coordinate version applies.

**Approach:** Use Entur's current-and-future export. A single version of the containing StopPlace may establish the interval for its embedded Quay when the Quay has no override. Resolve the correct version at the actual calendar instants of the planned call. Keep ambiguous or unverified calls available as manual stops.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Open end | Exact embedded Quay and unambiguous containing interval | Resolve the published version for the eligible call | A missing start remains unqualified |
| Change at midnight | Two versions and a service-day call after midnight | Match actual UTC arrivals and departures | Overlap or an arrival/departure spanning a change stays manual |
| Legacy workday | Previously pinned sources, including existing sidecars | Preserve previous eligibility and private evidence | New imports never mutate frozen references |

</frozen-after-approval>

## Implementation Notes

- The official GCS snapshot supplies current and future versions for the route dates. The importer streams the large XML member and stores version candidates under a separate revision namespace.
- Inherited validity is tied to the exact embedded Quay and reported explicitly in the coordinates response. Local timestamps are interpreted in Oslo, with ambiguous or nonexistent times left unresolved.

## Review Triage Log

- High, patched. Retain unusable coordinate versions as competitors and consider overlap across the whole arrival–departure interval.
- Medium, patched. Both direct and wrapped ValidBetween are accepted. Duplicate, empty, reversed and unsupported validity fields remain unknown locally.
- Medium, patched. A common verified parent preserves manual anchoring when the timetable provides only a Quay ID.
- Medium, patched. Reject archives containing none of the planned platforms and report unmatched IDs per date. The replay pins both source generations.
- Low, patched. Coordinate responses attribute inherited validity and the field guide records coverage and exact gaps.

## Verification

- Entur generation `1795345333303902` matched all 457 platform IDs. At the actual scheduled instants, 411,148 of 418,428 calls qualified and 7,280 calls at seven Quays stayed manual.
- The binary Ubuntu import format updated all 231 line-date rows in isolated PostgreSQL. The real 05:10 line 26 trip was frozen to a synthetic workday and accepted both a manual anchor and a subsequent GPS anchor.
- 81 targeted backend tests passed, including version overlap, rollover, existing position behavior, and V1 restore. Two pilot checks that require other historical artifacts were skipped.
