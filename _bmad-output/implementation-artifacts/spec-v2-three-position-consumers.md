---
title: 'Verify the three V2 position consumers on one watch'
type: 'chore'
created: '2026-11-20'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent">

## Intent

**Problem:** Existing browser coverage observes position consumers in pairs. It has no integrated evidence that a single watch can qualify own speed, a road limit and warning, and stop progression at the same time.

**Approach:** Extend the existing stop-authority browser scenario with a synthetic road package on the same synthetic trace. Given three explicit opt-ins, expect both road signs, a measured speed and an acknowledged GPS stop assertion on one watch. Given the road-only stop, expect cleared signs and renewed speed and stop progression on that existing watch. Keep the lost-write recovery, global interruption, explicit re-anchoring and raw-position privacy checks. Use disposable local services and synthetic position callbacks.

</frozen-after-approval>

## Implementation Notes

- `frontend/tests/v2-stop-progression.spec.ts` adds a qualified synthetic road package and numeric fixes to the existing loss and recovery scenario. Intermediate samples preserve the original approach points and fit the position consumers' different evidence windows. A paused virtual clock makes those intervals deterministic.
- The independently simulated trace reaches `A-o3` with measured 54 km/h, current 50 and next 30 at roughly 140 m on one watch. After stopping road matching, the same watch still reaches `A-o4` and reports a newly measured 45 km/h, with both road signs empty. The protected route, road reference and receipt fixtures are synthetic. These assertions exercise the real browser code against the isolated application APIs while the scenario's sources and receipts are controlled by the test.
- TypeScript/Vite and all 18 deterministic motion tests passed. The first browser version passed across all three engines. The two existing synthetic Edge password cases also passed with this product build. They cover password change, terminal `SENDT` issuance, redemption, separate login and revocation of a second session.
- After review, all 24 targeted lifecycle cases passed across Edge, Firefox and WebKit without retries or skips. The product files match `6470885`, the build used in the previous 42-case V2 regression. Local reports are `tmp/v2-three-position-consumers-final.json` and `tmp/v2-latest-password-smoke.json`.

## Review Triage Log

- Medium, patched. The negative opt-in assertions now follow three valid numeric samples while only stop progression is enrolled.
- Medium, patched. Current 50 and upcoming 30 are asserted in their respective definition fields. The warning distance belongs to the upcoming value.
- Medium, patched. The mock rejects a stale write revision with HTTP 409 and returns the recorded operation receipt only for its exact identifier.
- Medium, patched. Request and browser storage assertions use both synthetic coordinate values, including a measured longitude absent from the stop and road fixtures.
- Medium, patched. A new watch resumes after a deliberate stop selection. Old-watch fixes delivered while the new watch is running leave speed unknown. Two fixes on the new watch then produce a measured speed.
