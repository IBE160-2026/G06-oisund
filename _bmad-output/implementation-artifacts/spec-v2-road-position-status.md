---
title: 'Explain interrupted road matching'
type: 'bugfix'
created: '2026-11-20'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent">

## Intent

**Problem:** A qualified road panel silently clears both values when position stops. Its driver cannot tell that the browser denied permission, the device service failed, or the last sample could not be used without reading the separate own-speed panel.

**Approach:** Announce shared position interruptions in the road panel when it requested position. Keep one watch, the existing global Pause and Off, and the separate road stop. Given an interrupted road request, show its cause and require explicit restart with fresh road evidence. Given speed alone after a deliberate road stop, leave road status untouched.

</frozen-after-approval>

## Implementation Notes

- `PrivateRoadLimits` keeps the last relevant position reason in its own live region. It records intent before checking workday access, clears that intent on terminal states and unmount, and drops the status on explicit global Off or local stop. `PositionAssistance` supplies the existing source wording.
- A malformed fix invalidates both signs and resets the matcher while its existing watch is still active. New valid fixes must pass the full road evidence window. A source interruption that ends the watch requires a deliberate new start and new samples.
- With the previous build and the new test, Edge reproduced the missing road-local status at the first permission denial. The local report is `tmp/v2-road-position-status-before.json`.
- TypeScript/Vite and all 18 deterministic motion tests passed. All 18 affected browser cases passed on Edge, Firefox and WebKit with no retries or skips. The tests used synthetic callbacks against isolated V2 test services. The local result is `tmp/v2-road-position-status-after.json`.

## Review Triage Log

- Medium, patched. Global Off now clears a preceding Pause status even after Pause removed the road request. The browser regression uses those controls in sequence.
- False, verified as two different source states. `invalid` leaves `PositionSource.running` true and clears the matching window. Terminal interruptions close the watch, and the regression checks the required explicit restart after a terminal timeout. The implementation notes make that distinction explicit.
- Medium, patched. The regression now removes two already visible signs at malformed and timed-out samples, exercises a callback after the former watch stopped, and requires three new fixes to regain a sign after explicit restart.
