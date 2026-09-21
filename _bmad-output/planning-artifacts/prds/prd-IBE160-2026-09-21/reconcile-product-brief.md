# Product Brief Reconciliation

Source: the approved [Product Brief](../../briefs/brief-IBE160-2026-09-21/product-brief.md), reconciled against the current [PRD](prd.md), its [addendum](addendum.md) and decision history. Later explicit product decisions govern superseded preferences. This note contains no private operational identifiers.

**Verdict:** No blocking source-reconciliation gap. The approved direction is retained, with explicit later scope changes. Resolved A decisions remain resolved; B validation and C course information remain deferred as recorded.

## Captured

| Source intent | Current disposition |
|---|---|
| One convenient shift-specific view; reduce repeated searching without replacing official instructions or driver judgment | PRD sections 2–3; FR-5, FR-12; NFR-1/2. Existing operator workflows remain outside scope. |
| PDF preparation, actual bus entry, trips, breaks, changes and transfers | FR-2–5. Review and direct correction extend the brief. Physical bus and vehicle duty remain distinct. |
| Actual-progress trip selection, direction and manual correction | FR-6–11/16. Timetable alone cannot advance an unfinished trip; missing data and manual progression remain distinguishable. |
| Relevant planned disruptions with provenance, validity and freshness | FR-12–15/18–19. Automatic retrieval is mandatory; missing data never implies no disruptions. Source time and retrieval time remain distinct. |
| Retain useful information on failure and make uncertainty visible | FR-3/9/13/16–20; NFR-2/4. Whole-shift offline recovery is an explicit later requirement. |
| Fullstack website with database; no selected stack | PRD section 2 and B-3. Technical choices remain downstream. |
| Clearly labelled demonstration plus actual-shift evaluation | FR-25; section 9. Simulated behavior does not prove operational retrieval or positioning. |
| Three actual workdays, reduced checking time and no missed relevant planned notices in evaluated cases | Section 9, SM-1/2; FR-5/12–15/23. Recalled baseline and variable shifts limit causal claims. |
| Limited solo capacity and provisional December delivery | Sections 2 and 10, B-5/C-1/2. Upper capacity is not guaranteed; instructor assessment extends over Christmas. |

## Explicitly Changed or Deferred

- Speed limits and weather are optional after a working core. Meeting-bus awareness has priority over them unless an addition is very simple; deadhead-route calculation follows. This replaces the brief's earlier first-version emphasis on speed information, rather than losing a mandatory requirement.
- The earlier speed-change warning within 100 metres and its uncertainty fallback remain extension detail in the authoritative source; they are not FR-8's mandatory stop-progression criterion. Future speed-feature planning must recover that source detail and validate its data before commitment.
- Initial automatic disruption coverage is limited to the selected transit source. Wider road sources and precise deadhead routing are deferred explicitly; FR-12/13 must not imply complete road coverage.
- The broader vision now includes tour and charter duties without universal fixed-route assumptions. Generalized support is deferred, preserving a bounded scheduled-service MVP.
- AI relevance sorting and short alerts remain source-backed future ideas, not mandatory capabilities or an implementation choice. Their ordering was not reaffirmed by the later extension decisions.
- PDF summaries, private access, temporary retention and isolated instructor assessment were added during discovery: FR-1/21–25. The retention decision in FR-24 supersedes earlier open-ended quality-data retention.

## Gaps and Follow-up

No new product decision is required by this reconciliation. The brief's prototype-error evidence explains why relevance and freshness matter; it remains supporting evidence rather than an additional feature. Source access and coverage, dated timetable matching, device positioning and capacity remain B-1/2/5 validation work. Exact course dates remain C items. None should be presented as already verified, and failure must trigger explicit scope reconsideration rather than substituting simulation for the operational core.
