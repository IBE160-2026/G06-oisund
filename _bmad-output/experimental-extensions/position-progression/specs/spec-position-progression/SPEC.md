---
id: SPEC-position-progression
status: draft
approval: not-approved
version_target: V1.3.0
planning_stage: bounded-epic-draft
companions:
  - behavior.md
  - route-interface.md
  - fictional-example.md
  - decisions.md
  - technical-addendum.md
  - ../../research/technical-position-progression-2026-10-26/research.md
sources:
  - ../../scope.md
assumptions: [A3]
open_questions: []
---

# Position and stop progression

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

User clarifications U1–U5 and planning decisions PP-D1–D4 govern this draft. They do not accept implemented functionality. Research remains evidence for platform limits; contrary older product proposals are superseded.

## Why

Help the driver follow the relevant stop occurrence on a selected, confirmed dated trip, recover context after interruptions and reuse a last-known stop without inventing physical work or losing manual choices.

## Capabilities

- **CAP-1**
  - **intent:** Start assistance at the relevant occurrence of the trip being driven.
  - **success:** Example A starts at full-pattern occurrence 2; mid-trip start permits a selected later occurrence within the driven range.
- **CAP-2**
  - **intent:** Estimate relevant/next planned stop along the selected range.
  - **success:** Ordinary supported progression distinguishes repeated visits and needs no manual confirmation at each stop. No estimate or timetable event changes activity selection, outcomes or shift lifecycle.
- **CAP-3**
  - **intent:** Recover a useful progression estimate after a gap.
  - **success:** First delivery requires manual occurrence selection, which may jump 3→6 without recording observed passage at 4/5. Automatic multi-stop reacquisition remains later.
- **CAP-4**
  - **intent:** Correct the estimate while allowing later evidence to revise the advisory anchor.
  - **success:** A fresh manual choice survives immediate contradictory fixes; later coherent reliable evidence may support ordinary progression. Age alone never does, and explicit Pause/Off is respected.
- **CAP-5**
  - **intent:** Reuse the last-known stop as a proposal for another trip within the same workday.
  - **success:** Saved A:8 at 23:48 maps by Quay identity to B:3 at 00:08 across midnight in W1. Original time/provenance remain old; absent or ambiguous matches require manual choice. A different workday cannot inherit it.
- **CAP-6**
  - **intent:** Understand whether missing route facts or unreliable location prevents assistance.
  - **success:** Missing coordinate mapping produces a route-data status; old/poor fixes produce a separate measurement status. Both can coexist without guessing a stop.

## Constraints

- Implementation waits for completed/tested V1, required route functionality and separate authorization. Route P1 remains a draft dependency.
- Confirmed source association, imported/manual route facts and explicit activity outcomes stay separate from a mutable estimate.
- Foreground opt-in on Android Chromium; Brave/Chrome and trusted HTTPS on the actual device need separate qualification. Access revalidation, fixed expiry, Pause/Off and cleanup apply from the first sensing slice.
- NSR coordinates and bounded private anchor persistence are additions proposed here only. Retain StopPlace/Quay identity, mapping/source versions and dated validity; no name-only mapping.
- Workday identity governs anchor reuse across midnight. Access and existing deletion deadlines still apply; reuse, login and saving never extend them.
- All thresholds are untested experiment values. Repeated fixes can share error; ambiguity never becomes certainty through time alone.
- Preserve private/demo isolation, existing online owner/revision/retry rules, readable Day/Night/focus and user data. Interaction is intended while stopped.

## Non-goals

Automatic multi-stop reacquisition in first delivery; cross-workday anchor reuse; background continuity, full GPS history, maps/audio, notice/vehicle-feed dependencies or route implementation. This task excludes product execution, V1 changes and commit/push/merge; one extension epic and short stories are authorized planning only.

## Success signal

A later controlled demonstration reproduces all six first-delivery example steps, the overnight remapping and rejection cases while leaving outcomes unchanged. The automatic-reacquisition branch is a future target. No demonstration or GPS qualification has run.

## Assumptions

A3: illustrative measurement gates need device/layout qualification. Technical proposals are labelled in decisions.md and technical-addendum.md; they are not implementation acceptance.

## Open Questions

No unresolved product decision blocks this bounded epic. Q1/Q2 were settled by PP-D1/PP-D2. Device suitability, coordinate coverage, thresholds and the route handoff remain qualification gates in the stories.
