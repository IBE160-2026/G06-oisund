---
title: 'Qualify automatic notice relevance for the complete V2 pilot week'
type: 'feature'
created: '2026-11-20'
status: 'done'
route: 'oneshot'
baseline_commit: '8c84173a7f231f721c45b73dc95523bdd59bf811'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

Automatic notice relevance uses a two-day historical crosswalk while the integrated V2 pilot spans 23–29 November. Extend the versioned local crosswalk for printed lines 20 and 24 to those exact seven calendar dates, justified by the retained Entur export. Preserve exact line and authority checks, planned-time semantics, existing manual decisions, uncertain and out-of-scope handling, the independent collector, and the two owner trial workdays from the plan.

</frozen-after-approval>

## Implementation Notes

- The change touches the static crosswalk, dated controls and handoff. The archived timetable establishes line/authority links by a versioned `Network` and its explicit group. This establishes the date scope for the existing two exact printed codes.
- The independent review reproduced both calendar count sets from the archive. Tests cover all seven exact Oslo dates for each line, both outside dates, overnight overlap, and a real private projection for a controlled confirmed-workday fixture spanning the upper boundary.
- The isolated regression passed 97 backend and PostgreSQL controls. The Windows Edge review suite passed three cases and TypeScript/Vite built successfully. The two representative personal trials remain open.

## Review Triage Log

- Medium. The fixed calendar endpoint could expire in a later test run. The disposable fixture now has its own current authorization lifetime and injects the archived planned facts only. Open-ended source data isolates the line-date boundary.
- Medium. The source evidence needed exact member names and a repeatable calendar count. Recorded both along with independently reproduced counts and exact hashes.
- Low. Qualified the statement about 30 November to an otherwise eligible open notice with only out-of-window overlap.
- Medium. The handoff now specifies two representative workdays with line 20 and line 24 examples.
