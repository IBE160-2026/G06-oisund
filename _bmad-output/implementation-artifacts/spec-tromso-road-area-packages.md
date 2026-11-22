---
title: 'Dated road areas for Tromsø'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: ['docs/v2-field-trial.md']
---

<frozen-after-approval reason="human-owned intent">

## Intent

**Problem:** The private workspace has no dated NVDB road graph that can be used independently of a workday and departure.

**Approach:** Import versioned snapshots to PostgreSQL, expose the selected area for the current Oslo day after authentication, and reuse on-device road matching and GPS speed. Retain alternative successors and represent unresolved limits explicitly. An exact, dated review may add confirmed limits to the public graph.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Training | Authenticated user opens the GPS screen without a workday | Independent speed control and explicit area selector | GPS works without published road data |
| Branch | Multiple feasible successors, including an unresolved edge | No next-limit warning until the direction is established | Current matched limit remains individually qualified |
| Source | Archive without applicable reviewed values | Directed geometry is stored and limits remain unknown | Reject invalid receipts or reviews before publishing |
| Access | Tab hidden, session lost or switching GPS views | Active watch is cleared and restarting is explicit | Package requests carry only area selection |

</frozen-after-approval>

## Implementation Notes

- Migration 023 stores observations and dated area manifests. The importer reconstructs the graph from hash-checked source pages and retains references to successors beyond the selected area. The Ubuntu command passes a bounded public bundle over stdin to the private importer.
- The private owner can enable speed independently. The area selector sends one fixed area ID and shares the device watch with speed. A change in the public revision clears road readings during use.
- Geometry has an Oslo date window. Positive speeds retain their source age and review lease. A 300 m warning requires a confirmed change location at the source edge's exit node.

## Review Triage Log

- Medium, patched. Multi-fix direction supports movement below one uncertainty radius per sample. The motion suite covers opposite edges during 6 m/s movement.
- High, patched. Geometry-only areas are available on their effective date. API responses with expired reviews remove numeric limits and retain the dated geometry.
- High, patched. The importer validates an explicit reviewed transition between two adjacent, approved directed edges. Warnings stay unknown when its location is unavailable.
- High, patched. The active panel checks the area revision and clears its readings on change. Speed can continue independently.
- Medium, patched. The workday endpoint still requires the original qualification profile.
- Medium, patched. A suspended workspace restores visibility of public departures and gives the user a route back.
- Medium, patched. Unknown limits and uncertain location now have distinct explanations. Short edges can still conservatively remain unresolved near a boundary.
- Medium, patched. The database test covers a conflict after insertion of the first area. Both complete NVDB archives are used in an isolated end-to-end import.

## Verification

- All eleven production-source dates produced the same 18,615-edge directed graph and 33 manifests in isolated PostgreSQL.
- 59 targeted backend tests, 55 Ubuntu operation tests with 47 subtests, and 21 motion tests passed. Edge, Firefox and WebKit passed the standalone and activity GPS tests. The TypeScript/Vite build passed.
