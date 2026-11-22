---
title: 'Apply public road situations to dated Tromsø areas'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: ['docs/v2-field-trial.md']
---

<frozen-after-approval reason="human-owned intent">

## Intent

**Problem:** A reviewed limit can conflict with a new public roadwork or regulation notice during a field session.

**Approach:** Use the authorized public SituationSimple WFS as supplemental evidence. Preserve dated source observations, suppress numeric limits and warnings on potentially affected edges, and keep other qualified edges available. A temporary numeric decision requires a reviewed limit, directed segment and explicit validity window from an applicable source.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Reported roadworks | Active WFS geometry intersects a reviewed road | The intersecting edge is unknown | Retain known limits on unaffected edges |
| Temporary limit | Independent approval covers an exact direction and a bounded interval | Retain that reviewed value for its resolved situation | A WFS notice alone supplies no value |
| Replaced report | The active event set changes while the area is open | Revision recheck clears previous road readings | GPS own-speed control is independent |
| Feed failure | Invalid or incomplete response | Retain the last validated observation and its reported dates | Never publish partial records as a complete snapshot |

</frozen-after-approval>

## Implementation Notes

- Migration 024 records versioned public snapshots. The source reader validates timestamps, complete result counts, WGS84 and typed geometry.
- The API checks the event polyline after a bounded extent check. Geometry-less evidence uses a reported road where available. The geographically filtered source cannot establish coverage of unlocated reports.
- Temporary decisions have a per-segment validity window. A speed-management exemption requires the reviewed record fingerprint and never applies to another record in the same situation. Existing reviews without this proof return an unknown temporary limit.

## Review Triage Log

- High, patched. Unresolved or changed temporary records cannot retain the old speed. Legacy proof changes the effective revision.
- High, patched. The active browser clears stale readings and loads the new package through its shared watch. It can accept a fresher manifest published during the reload.
- Medium, patched. Sampling bounds cover the full published shapes crossing area strips. Typed linework avoids masking an untouched road merely because it is inside a diagonal bounding rectangle.
- Medium, patched. Freshness is reported to the operator. The production timer refreshes every three minutes and malformed observations cannot replace valid data.
- Medium, documented limitation. The source query filters on published geometry and can omit unlocated records. No authoritative replacement source was available under the approved scope.
- Medium, patched. Tests cover the 300 m output on each side of a masked edge and preserve an unrelated qualified warning.

## Verification

- Ubuntu reached SituationSimple without credentials and received nine records in four situations. The isolated transport stored a new live nine-record snapshot.
- Synthetic input verified an amended record suppresses the previous temporary number, while verified far-away data stay available.
- Frontend, restore and Ubuntu operation checks are shared with the public source delivery verification.
