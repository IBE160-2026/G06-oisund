---
title: 'Requalify the road package on explicit start'
type: 'bugfix'
created: '2026-11-20'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent">

## Intent

**Problem:** The road panel can restart with the package read when the activity opened, even after the private road reference reports a replacement or withdraws qualification. This leaves the explicit resume and atomic package replacement cases in SL-E1-S6 uncovered.

**Approach:** Use a fresh private road response for every explicit start. Accept a structurally valid, current package only for an uncancelled attempt on the current activity. Given a changed package, qualify signs with new fixes for that package. Given an expired, unavailable or withdrawn package, leave road matching off and explain why. Global stops cancel a pending attempt. An independent speed consumer can keep using the shared watch while road matching waits or fails.

</frozen-after-approval>

## Implementation Notes

- `PrivateRoadLimits` uses the existing private GET. The browser request and private API already use `no-store`. The API reopens the fixed packaged source after exact frozen-journey binding and access control. This change needs no API route, storage change or new privilege.
- The initial request gives the user the qualification status. A retry of that check leaves sensing off. A separate explicit start obtains one full package, validates it before installing a new evaluator, and checks freshness again after workday access is verified. The road observer retains one request token on its current context. Cancellation invalidates it before any late candidate can start sensing.
- The operator can cancel from the panel while a request is pending. A global stop invalidates the same pending attempt. Road matching still shares the existing watch, and the package check uses server-anchored private time. Raw fix age remains on the native wall and monotonic clocks.
- Edge reproduced the prior-build failure at the first expired replacement response. The local red result is `tmp/v2-road-source-before.json`.
- TypeScript/Vite and all 18 deterministic motion tests passed. All 42 V2 browser cases passed with no retries or skips across Edge, Firefox and WebKit. The four specs cover automatic notices, route selection and recheck, GPS speed and road matching, and stop progression. The local report is `tmp/v2-road-source-after.json`.

## Review Triage Log

- Medium, patched. Initial unavailable and unqualified states offer an explicit qualification retry that does not start position.
- Medium, patched. A malformed sample from another consumer while a road request waits no longer hides the road-source result. The browser test injects an invalid speed callback during a pending withdrawal response.
- High, patched. A delayed callback acquired before the current road activation is excluded from the new evaluator. The browser test delivers a pre-activation fix only after the replacement starts and still requires three new fixes.
- Medium, patched. The server-anchored private clock now governs package validity before activation, on sample evaluation and when scheduling display expiry. The browser test moves the device clock back before requesting an expired package.
- Medium, patched. A pending road start reports progress and offers local cancellation even before the first shared watch starts.
- Medium, patched. The test now overlaps a cancelled request with a newer explicit attempt, delivers the old package first, checks that the newer attempt is still waiting, then qualifies only the new package.
