---
title: 'Distinguish a documented pilot stop in automatic notice review'
type: 'feature'
created: '2026-11-20'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

Give AN-E1-S3 a dated stop-review group for a source message scoped solely to the exact Giæverbukta StopPlace. It requires the observed SIRI selector shape and a qualified Oslo-date overlap with a planned line 24 activity. The group prompts an explicit local review. Activity matches, specific platform applicability and user decisions require their own evidence. Preserve the general review path for uncertain scope and the existing treatment of mixed line and stop selectors. Use the pinned public timetable and NSR records to check provenance. Exercise the distinction through the private API and in the browser with controlled messages.

</frozen-after-approval>

## Implementation Notes

- The pinned timetable and NSR extracts establish dated planned visits to the exact StopPlace on line 24. Line 20 supplies a negative check. The archived October notice supplies the shape and an expired-case control. [Evidence and limits](../../docs/v2-automatic-notices.md#dated-giæverbukta-stop-review).
- The private projection adds an optional `pilot_stop_review` flag to an ordinary `review` row. The group renders from page entries and leaves activity matches empty. Saving day context remains an explicit private decision.
- The parser records local verification of the observed XML scope. A repeated observation can update that proof at the same publisher revision. A changed proof for the exact mapped scope updates the private review basis, preserves the previous choice, and requires a fresh review.
- The affected backend regression passed 257 cases before the final attribute check. The final parser, source archive and API checks passed 99 cases. TypeScript/Vite and all 18 deterministic motion tests passed.
- The final build passed all 36 selected V2 browser cases across Edge, Firefox and WebKit. The initial run passed all 12 Edge cases. Firefox and WebKit stopped at executable lookup in the default cache for 24 cases. The separate rerun with `PLAYWRIGHT_BROWSERS_PATH` set to `tmp/playwright-browsers` passed those 24. The original report is retained at `tmp/v2-pilot-stop-edge-and-setup-report.json`.

## Review Triage Log

- Medium, patched. Qualified and unqualified XML previously normalized to the same shape. The classifier requires positive namespace and attribute evidence. Legacy, unqualified and `xsi:nil` controls all stay in ordinary review.
- Medium, patched. The new API and browser cases keep real current authorization while supplying historical pilot facts in the synthetic store. Open-ended fixture validity keeps the exercise reproducible after the pilot. Deterministic unit cases cover bounded expiry and calendar edges.
- Low, patched. The base API enum and page counters preserve older clients. The browser recognizes only a valid optional flag on an existing review row with zero activity matches and a source observation.
- Low, patched. The source guide and readiness matrix now record the exact stop, operating dates and manual-review scope.
