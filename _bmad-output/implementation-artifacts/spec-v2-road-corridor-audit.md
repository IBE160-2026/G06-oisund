---
title: 'Verify the dated road corridor offline from archived NVDB pages'
type: 'feature'
created: '2026-11-20'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem**. The operator has a versioned NVDB archive, but the route and direct speed-coverage comparison still depends on a local one-off script. Its unmatched-span output can omit an unresolved part of the chain.

**Approach**. Add an offline command that verifies the archive and reconstructs every declared ordered corridor span using exact sequence positions and nodes. Emit a research report with source identities, geometry and chainage. Distinguish complete direct general speed coverage, gaps and conflicting values. Keep observations about specific lanes separate. A report remains outside runtime approval and does not infer physical driving, direction applicability or legal regulation.

</frozen-after-approval>

## Implementation Notes

Use `road_evidence` record validators and limits at the archive boundary. Read the existing historical `source-bound-route.json` as scope data and allow exact 1-to-0 ring wraps at the same node. Reconstruct across benign changes to segmentation, checking both endpoints of every span and all internal nodes. Preserve one occurrence row for each use of a segment. Maintain exact relative fractions and sum source lengths. For type 105, only empty lane lists count toward direct general coverage. Keep recorded source orientation as evidence and compare values over subintervals.

The isolated offline suite passed 67 audit and collector cases. It checks archive digests and missing pages, changed sequence and topology, wraps, historical merges, repeated occurrences, field-specific coverage, conflicting overlaps and decompression failure. The live 20 November archive was processed without provider traffic against the historical scope. An independent check confirmed every chainage and node join, all three direct-gap groups, the R4 arc length and the sole interior node identity change. Current detail-to-parent evidence stays separate from this direct-coverage output. [CLI and output fields](../../backend/app/road_data/README.md#offline-corridor-audit) · [Dated audit](../../docs/evidence/v2-road-source-20261120.md#offline-corridor-reconstruction).

## Review Triage Log

- Medium, patched. Every direct speed interval now lists its clipped bounds and recorded values so gaps and overlaps are located explicitly.
- Medium, patched. A type 105 record now retains its original source placement bounds alongside the intersection with the segment.
- Medium, patched. The audit reports preserved or replaced interior node identities and absent historical boundaries separately from required span endpoints. The replacement at `0.8495006` is visible and joins the refreshed neighbouring segments.
- Medium, patched. Geometry must be a syntactically valid, non-empty two- or three-dimensional LINESTRING with finite coordinates. Network rows also require a source start date and the expected CRS.
- Medium, patched. The CLI handles decompression corruption with a controlled failure and no partial output. A test corrupts a compressed member directly.
- Low, patched. Tests cover legitimate historical merges and a source segment reused as separate corridor occurrences.
- Low, patched. The report records the municipal and sequence scope and the observation interval. The documented invocation uses the retained dated archive and explains the output fields.
