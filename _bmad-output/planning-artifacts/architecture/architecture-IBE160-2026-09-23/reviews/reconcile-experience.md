# EXPERIENCE reconciliation

Verdict: **Pass with two small consistency clarifications recommended.** No contradiction requiring a new user decision was found. The spine expressly retains EXPERIENCE as the detailed behavior contract; the findings below promote only rules that cross module boundaries.

Compared `ARCHITECTURE-SPINE.md` (draft, 2026-09-23) with final `EXPERIENCE.md` (2026-09-22), honoring the later adopted AD corrections.

## 1. Make the manual pin's tracking-context scope explicit

- Spine: AD-9, particularly the role/context bullet; `OperationalState` boundary.
- UX: EXPERIENCE lines 271–273, “Explicit tracking-context changes,” and lines 220–227, revision ownership/recovery.
- Risk: a progression implementation can preserve a manually pinned trip until completion while a mentor-context implementation switches person/block. Without an explicit release rule, these compliant pieces can either carry the previous person's pin into the new context or incorrectly complete/abort the former trip to release it.
- Suggested compact rule: “A confirmed person/block/activity change exits the tracking context without completing or aborting its unfinished trip; keep its evidence and determine the trip afresh in each later context. Acute takeover preserves the existing context and pin.”
- This is an already-approved UX rule, not a new architecture choice.

## 2. Make revision target and broken-link handling explicit

- Spine: `Workday / PlanRevision` conceptual contract, currently line 156.
- UX: EXPERIENCE lines 220–222, “Revision ownership and linked contexts.”
- Risk: import reconciliation and accompaniment-context recovery can disagree about whether similar trips in own/linked plans may be matched or whether a removed referenced trip can be replaced automatically.
- Suggested compact addition: “Every revision targets one named own/linked plan; match only within that plan. Changes affecting accompaniment references leave broken links explicitly unresolved for repair, never silently rebound.”
- This is an already-approved UX rule, suitable for the contract boundary rather than detailed DTO design.

## Coverage observations

- The spine correctly carries movement restrictions, unknown-speed handling, outage continuity, final-stop/return transitions, active-role recovery, terminal ending, summary/export, notice versioning and retention. Detailed staged warning presentation, guiding controls, theme behavior and simulation controls can remain in the referenced UX.
- Own-source raw-file retention and immediate post-import preview availability differ from older UX wording intentionally: AD-6/AD-12 and the latest explicit user instructions govern.
- Keep source incident lifecycle distinct from local driving-message visibility during implementation; EXPERIENCE line 148 explicitly states that passing a stop or clearing a driving message never closes the source incident. AD-8's existing backend/client ownership already supports this separation.

No application/device tests were performed; this is document reconciliation only.
