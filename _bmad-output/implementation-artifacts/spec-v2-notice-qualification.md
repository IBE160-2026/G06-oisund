---
title: 'Verify automatic notice relevance on two controlled workdays'
type: 'chore'
created: '2026-11-20'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent">

## Intent

**Problem:** Existing automatic notice tests exercise individual rules and workflows. The original AN-E1-S4 plan also calls for an independently labelled sample spanning two workdays with explicit accuracy and review counts.

**Approach:** Publish controlled SIRI-SX messages through the existing ingestion fixture, read both confirmed workdays through the private API, and compare every observed classification to the case labels. Report recall and precision with their raw denominators, any unknown or out-of-subset nominations, and per-day review workload. Keep the personal workday and paired Svipper evaluation open.

</frozen-after-approval>

## Implementation Notes

- Reuse the synthetic-account and isolated-feed guards in `backend/tests/test_private_automatic_notices.py` and the SIRI-SX XML builders in `backend/tests/test_automatic_notice_rules.py`. Exercise both ingestion continuation and private API cursors. The test owns no live provider or browser state.
- Record overlapping exact line/time, exact nonmatching lines, boundary contact, cross-midnight dates, uncertainty, broad scope and stop-only handling separately. Use existing controlled cases for refresh failure, lifecycle and preservation.
- Before review, the isolated API measurement passed and the 90 rule/API regressions passed. After review, the same 90 passed with the revised catalogue. The measurement covered 36 pairs with recall 6/6, precision 6/6, no false or missed nominations, 14 unknown pairs and eight broad or excluded pairs. None of the last 22 were nominated. [Measurement and reproduction](../../docs/v2-automatic-notices.md#controlled-two-workday-measurement).

## Review Triage Log

- Medium, patched. Require raw `review` and literal `true` for the pilot-stop subgroup before counting it.
- Medium, patched. Assert each full match, including activity identity, exact line and authority references, and the expected Oslo date set across midnight.
- Medium, patched. Place the line 20 activity in the gap between distinct source windows while line 24 overlaps the later one.
- Medium, patched. Check source expiry independently of the planned interval and assert the explicit exclusion and uncertainty reasons for each applicable case.
- Low, patched. The handoff distinguishes the future comparison on representative owner workdays from the synthetic measurement.
- Low, patched. The measurement links the original qualification criteria to the corresponding technical evidence and distinguishes current results from earlier browser, provider and preservation evidence.
