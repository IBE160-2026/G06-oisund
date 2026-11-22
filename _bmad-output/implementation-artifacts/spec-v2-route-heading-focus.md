---
title: 'Keep focus when a dated route opens'
type: 'bugfix'
created: '2026-11-20'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Both original and rechecked route-source scenarios render the selected departure in headless WebKit without focusing its heading. The route has been requested explicitly, and the focus move is needed to find the new review panel.

**Approach:** Tie the focus move to the committed heading for an accepted departure. Keep existing focus assertions, explicit range selection and recovery from an unknown save outcome. Verify both source variants across Edge, Firefox and WebKit.

</frozen-after-approval>

## Implementation Notes

- Both WebKit cases failed on the previous build with the original test clock and with a fixed date that preserved native animation frames. The heading rendered in all four runs and stayed unfocused. This isolated the failure from the use of a simulated frame scheduler.
- `DraftRouteReview` focuses the heading in a layout effect keyed to the accepted journey. Existing request-generation checks govern which response may publish a journey. Changing the selected range alone does not rerun the effect. The test fixes only the date and retains the focus assertion.
- The isolated three-engine run passed 27 cases on Windows. Each engine ran two source variants, four GPS/road cases, two stop progression cases and a native secure-origin API shape check that did not start location acquisition. Edge was 157.0.4341.60, Firefox 157.0 and WebKit 27.2. The TypeScript/Vite build and 18 deterministic motion tests also passed.
- All six route cases passed again through the tracked configuration. Repeat from `frontend` after building the V2 test preview and running `node ../scripts/prepare-v2-tests.mjs`. Set `PLAYWRIGHT_BROWSERS_PATH` to the local Playwright browser cache, set `COMPOSE_PROJECT_NAME=ibe160-v2-tests` and `PLAYWRIGHT_V2_MULTI_ENGINE=1`, then run `npx --no-install playwright test v2-route-reference -c playwright.v2.config.ts`. Firefox and WebKit require the Playwright builds for the pinned package version. The default config still uses Edge on Windows and Chromium elsewhere.

## Review Triage Log

- Medium, deferred. Both the previous animation callback and the new layout effect move focus after an accepted response. A separate focus-intent policy would address the existing case where the user moves to an unrelated control during a slow request. The deferred item records this case.
- False as an explanation for the fixed failure. Both WebKit variants failed with fixed time on the previous product build and passed with the identical fixed-time fixture on the corrected build. The assertion and workflow sequence were retained.
- Low, patched. The tracked test configuration now exposes the three engines as an opt-in run. The command above targets both source variants across the three projects.
