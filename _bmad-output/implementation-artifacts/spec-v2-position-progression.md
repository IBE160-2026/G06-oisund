---
title: 'Progress advisory stop estimates on a qualified frozen route'
type: 'feature'
created: '2026-11-20'
status: 'in-progress'
route: 'dispatch'
baseline_commit: '755b6f9c43c13bcad1eef5555d9672c8f9f50456'
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md', '{project-root}/CLAUDE.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

Allow a driver to follow an explicitly selected occurrence, correct an advisory progression estimate and resume consciously. Save a bounded last stop for another trip in the same workday.

## Boundaries & Constraints

Load PP-E1-S1–S4, behavior, route-interface and fictional example from `D:/IBE160-plan-position-progression` at `df47a4e74ca982a2e04d6e5531e7744caf4f4717`. Require a compatible confirmed dated frozen route and versioned time-qualified NSR Quay coordinates for the chosen occurrence range. No name matching, centroid substitution, fabricated validity, automatic multi-stop reacquisition, position network traffic or GPS history. Use the shared PositionSource and separate stop opt-in. Edit only V2, no staging or commits.

| Scenario | Expected behavior |
| --- | --- |
| Start, correction and gaps | Explicitly choose an occurrence. Protect fresh manual correction. Require coherent reliable fixes for ordinary one-occurrence progression. After interruption, manual selection can move 3→6 without logging intervening passage. |
| Uncertain data | Missing route identity/range/coordinates and missing/poor/stale fixes give independent reasons and manual route behavior. GPS makes no changes to active selection, outcomes or workday lifecycle. |
| Same workday | Last stop A:8 maps by unique Quay to B:3 in the same workday across midnight. Preserve evidence time and provenance. Ambiguity or no match requires explicit selection. |
| Persistence | Private owner and session, parent lock, expected revision, exact retry receipt and fixed expiry. Cascade deletion, terminal read-only, no coordinates in anchors. |

</frozen-after-approval>

## Code Map

- CRN agent supplies `workday_route_references(workday_id uuid, activity_id uuid, reference jsonb)` and GET `/workdays/{id}/route-references`, with references containing activity_id, decision_revision, service_date, journey_id, line_id, pattern_id, direction, headsign, start_position, end_position, calls (position, occurrence_id, scheduled_stop_point_id, stop_place_id, quay_id, name, headsign, arrival, departure), provenance, status, selected_at. Require status compatible and in-range exact Quay.
- `frontend/src/positionSource.ts` and `PositionAssistance.tsx` provide the shared watch and `usePositionAssistance`, including `start('stops')`, `source.subscribe` and global Pause/Off. Create a new `PrivateStopProgression` component for the parent's later mount as child of PositionAssistance. Do not edit shared UI files during concurrent work.
- Add migration `018_position_anchor.sql` and a narrow new router/service file. Follow authorized parent/lock and idempotency patterns in `workday_storage`, `draft_storage` and `workday_selection_storage`. Ask parent to mount router; do not edit `private_main.py` concurrently.

## Tasks & Acceptance

- [ ] Build a bounded exact NSR coordinate sidecar and versioned eligibility contract. Give a control path for missing validity and demonstrate it, with current source rights and provenance. Do not mark the real coordinate data qualified without dated evidence.
- [ ] Build advisory one-step behavior, standalone frontend client and private anchor API, with deterministic synthetic controls for start/correction, contradictory fixes, repeated stops, expiry, interruptions, cross-midnight reuse and access.
- [ ] Verify using deterministic source/event tests and real PostgreSQL where runner available. Preserve evidence for remaining actual device/layout qualification.

## Implementation Notes

The parent owns test runtime rebuilds and shared integration. Send the exact component and router signatures as early as practical. Route work is concurrent. Read the existing source history and coordinate with the route agent if the response shape changes.

## Spec Change Log

## Review Triage Log
