---
title: 'Verify expiry and proposal recovery after an invalid lifecycle reply'
type: 'chore'
created: '2026-11-20'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem**. The broad regression checks for the plan deadline while the V1 access guard deliberately hides plan facts after an invalid lifecycle reply. The check stops before verifying recovery.

**Approach**. Exercise the existing access guard for both invalid replies, advance the clock past the supplied invalid expiry, and verify that the local proposal survives and that a valid read restores the original deadline and selection. Keep the original server-state assertions.

</frozen-after-approval>

## Implementation Notes

- The original cases failed in the broad Edge run on `c4f0474335adc36bfcb79605f8e3c463037cf316`. Both failed at the same assertion in a fresh build of the `df3fc940a7f97bd632e230ddb38c2fa45e8d2bfb` frontend, backed by an isolated V2 API and synthetic PostgreSQL database. Commit `3c2287ed68d0cbb1923439fc6ee00254395072a4` introduced the access guard that hides the plan when lifecycle validation fails.
- Both response variants keep the server-state assertions for the original expiry, outcome revision and selection. The revised cases check that the deadline is absent while plan access is unconfirmed, that the proposal and navigation guard survive beyond the supplied expiry, and that a valid retry restores the visible original deadline and original proposal.
- The final reviewed version passed both cases on the archived main frontend and both on the V2 frontend. The disposable comparison reports are stored in `tmp/v2-lifecycle-baseline/frontend`.

## Review Triage Log

- Medium, patched. A running clock could make a slow request fail on expiry and mask a missing lifecycle identity check. The clock is paused while the reply is evaluated. The cases verify that the proposed deadline follows the actual start, precedes the saved expiry, and is crossed only after the guard has rejected the reply.
- Low, patched. The recovered deadline must be visible before navigating back to the activity. A hidden element with matching text cannot satisfy that check.
