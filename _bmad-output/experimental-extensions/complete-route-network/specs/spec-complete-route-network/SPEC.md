---
id: SPEC-complete-route-network
status: draft
approval: not-approved
scope: EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE
created: 2026-10-26
updated: 2026-10-26
planning_stage: P1-epic-draft
companions:
  - coverage.md
  - matching.md
  - data-contract.md
  - qualification.md
  - decisions.md
  - pilot-manifest.md
  - technical-addendum.md
  - ../../research/technical-complete-route-network-2026-10-26/research.md
  - ../../../../planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md
  - ../../../../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/DESIGN.md
  - ../../../../planning-artifacts/ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md
sources:
  - ../../scope.md
assumptions: [A1, A2, A3, A4, A5, A6]
open_questions: [Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8]
---

# Complete route network — first specification draft

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

This kernel and its companions form the proposed specification package. Validation checks document coherence and preservation; it does not approve implementation or add course-delivery commitments. Parent V1 contracts remain read-only; extension-specific differences and pending decisions are explicit in decisions.md.

## Why

Drivers reviewing imported shifts need to identify the intended dated departure and its direction, destination and ordered stops without repeated manual lookup or invented certainty. Research demonstrates useful public route facts but leaves shift-number equivalence and complete coverage unqualified. A bounded matching experiment should establish that evidence before a complete pilot catalogue is claimed.

## Capabilities

- **CAP-1**
  - **intent:** The driver can inspect the existing planned services available within a declared pilot.
  - **success:** Coverage identifies its lines, operators, dates and required content as complete, partial or unknown; a sample cannot satisfy the complete-pilot criterion in coverage.md.
- **CAP-2**
  - **intent:** An imported activity can be associated with a specific public departure on its operating date.
  - **success:** Outcomes distinguish a unique proposal within a closed search scope, alternatives, absence within known coverage, and unresolved/unavailable data, with supporting facts under matching.md.
- **CAP-3**
  - **intent:** The driver can confirm, reject or correct proposed direction, destination and stops.
  - **success:** No proposal becomes confirmed merely by lookup; cancellation preserves prior facts, manual correction remains attributable, and an unmatched activity retains its manual path.
- **CAP-4**
  - **intent:** The driver can inspect the correct variant and relevant part of its stop pattern.
  - **success:** Ordered occurrences, subranges and changing destination displays remain distinct from endpoint names and optional geometry, including repeated visits to one stop.
- **CAP-5**
  - **intent:** Departure identity and planned times retain their operating-day meaning across midnight and calendar changes.
  - **success:** Raw time/day-offset and timezone/calendar evidence support explicit calendar instants; unresolved exceptions or DST cases stay unresolved rather than receiving guessed dates.
- **CAP-6**
  - **intent:** Reference information can be updated without silently rewriting reviewed work.
  - **success:** Source versions and user-confirmed/manual layers remain traceable; failed or changed sources expose comparison/staleness and preserve prior confirmed facts within existing access/expiry bounds.
- **CAP-7**
  - **intent:** A future notice consumer can refer to the same line, stop or dated departure.
  - **success:** The conceptual identity interface in data-contract.md preserves source namespace, mapping status, date and optional occurrence scope without exporting private shift content or claiming exact notice relevance.

## Constraints

- Current planning scope is P1 line20, seven named dates and explicit draft review. Remaining A1–A6/Q1–Q8 defaults are provisional; P2 and external integrations stay deferred. Qualification gates only the claim affected.
- Implementation waits until V1 is complete and has been tested for a while, followed by explicit owner readiness/implementation authorization. This run authorizes planning documents and their publication only.
- A shift number, privateCode, line number or nearest departure time alone cannot establish a dated match. Retain ambiguity and imported/source/manual distinctions.
- Selection, schedule and stop order never establish physical position, shift activation or completion. Geometry and progression are separate capabilities.
- Keep stable activity identity, physical bus and vehicle duty separate; enrichment cannot silently alter an activated/terminal plan or extend private retention.
- Preserve parent ownership, revisions/retry, online persistence, transient originals, private/demo isolation and applicable readable Day/Night/focus behavior. No private payloads in public requests or repository evidence.

## Non-goals

- New network generation or optimization of lines, frequencies, fleet or driver schedules; reconstructing private operational duties from public service data.
- GPS/automatic stop progression, driving qualification, live positions, maps/geometry delivery in the first increment, notice ingestion or exact disruption matching.
- Expanding V1, offline continuity, cloud deployment, mentor roles or export; implementation, full architecture/UX workflows or V1 tracking changes in this task; short extension epic/story planning and document publication are authorized.

## Success signal

A later P1 demonstration distinguishes the twelve declared example outcomes without an unsupported automatic match or lost manual correction. A later P2 claim of completeness is allowed only when every manifest cell in the approved pilot/horizon and required data dimensions passes its coverage checks. Neither signal has been demonstrated by this document task.

## Assumptions

A1 follows the supplied seven-date line-20 planning boundary, with literal historical casebook dates in pilot-manifest.md; A2 remains a deferred proposal for complete coverage of lines20/24/28/42 over28 service dates. A3 requires explicit user confirmation in draft review; A4 follows API-first qualification with NeTEx/NSR and a GTFS alternative. A5 proposes conservative exact evidence rules; A6 proposes preparation-time checks and a24-hour staleness label for P1; regional daily acquisition remains deferred with P2. Full boundaries and exceptions are in the companions.

## Open Questions

Q1/Q2 now supply P1 planning scope; literal dates/any later replacement window and P2 approval remain distinct. Q3/Q4 follow the requested draft/API-first boundary. Q5 conservative matching and Q6/Q7 freshness/retention are provisional checkpoints; Q8 external vocabulary agreement is deferred. V1 completion/testing and later implementation authorization are mandatory before execution. See decisions.md and qualification.md.
