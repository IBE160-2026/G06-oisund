---
title: 'Show advisory road limits and the next change near 300 metres'
type: 'feature'
created: '2026-11-20'
status: 'in-review'
route: 'dispatch'
baseline_commit: '755b6f9c43c13bcad1eef5555d9672c8f9f50456'
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md', '{project-root}/CLAUDE.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

Show the current registered road speed limit and the next change separately when directed topological and position evidence support them. Use the same core for multiple qualified road manifests.

## Boundaries & Constraints

Use SL-S1–S7, AC-01–14 and SL-LAB-1 from `D:/IBE160-plan-speed-limits` at `5adc6fb2c0137a3a6519d4f7ba42dd57f0e02f1c`. Start inside the named surface corridor, but keep corridor identity out of the engine. Use one shared foreground position source. Qualify separate road and confirmed-route binding, directed lane/turn coverage, source validity, signs and physical GPS independently. Unknown states must clear old values. Use fixed 300 m and do not use own speed as progress.

| Scenario | Expected behavior |
| --- | --- |
| Qualified current edge | Three fresh coherent fixes over at least two seconds, conservative calibrated interval, unique directed segment and one applicable limit. |
| Next change | Show nearest change at the first completely positive interval with upper bound ≤300 m. Preserve a supported active warning until 320 m with no duplicate animation. |
| Crossing and ambiguity | Show no current value while interval overlaps a boundary; switch after three coherent new fixes beyond the boundary margin. Competing outgoing arm or coverage hole independently removes upcoming value. |
| Lifecycle and sources | Stale, invalid package, wrong context or unsupported fixes clear relevant evidence. Same outputs with compatible package partition/order and a second manifest. |

</frozen-after-approval>

## Code Map

- `frontend/src/positionSource.ts` supplies serialized foreground fixes. Add a pure road manifest validator/matcher/evaluator and a child of `PositionAssistance`. Route reference contributes only a reviewed binding and known forward path.
- Add a private read-only road manifest projection based on authorized, compatible frozen route in `workday_route_references`. The manifest source is a bounded, explicitly qualified snapshot. The historical October export is evidence for the corridor, with field/turn, age and physical ambiguities recorded.
- Original Vegvesen 362 JPEGs 30/40/50/60/70 and rights/file hashes are in `frontend/public/assets/road-signs/source.json`.

## Tasks & Acceptance

- [x] Implement directed matching and fixed-distance evaluation separately from GPS speed.
- [x] Display distinct current and next limits with official assets and explicit evidence gaps.
- [x] Exercise independent synthetic manifests, gaps, transitions, overlapping packages and exact private API binding.
- [ ] Qualify the real directed corridor, bus-access and turn data, uncertainty profile and declared physical pilot.

## Implementation Notes

Product GPS display relies on qualified road data and calibrated conservative intervals. Synthetics establish implementation behavior separately. This checkout will not silently promote the historical corridor or any public HTTP success to operational qualification.

## Spec Change Log

- Bind a road package to exact archived SHA, route direction, planned journey/pattern versions and ordered occurrence range.

## Review Triage Log

- Patched the per-fix uncertainty floor and the independent road-source timer. The private API control changes individual binding fields to test fail-closed behavior. [Actual source and unqualified conditions](../../backend/app/road_data/README.md).
