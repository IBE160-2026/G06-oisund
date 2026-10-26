# Tentative scope

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Status: preliminary planning foundation, 2026-10-26. Nothing here approves implementation or promises inclusion in the submission.

## Intended benefit

Reduce manual lookup and ambiguity when reviewing an imported shift. A driver should eventually be able to inspect the existing service, identify the correct dated departure and its ordered stops, and understand which facts come from the shift, an external timetable or a human decision. Expected benefit has not been measured.

## Candidate capabilities for later specification

| Planning topic | Intended behavior and unresolved boundary |
|---|---|
| Acquisition and updates | Evaluate suitable existing sources and update approaches. API lookup, GTFS and NeTEx are candidates, not selected technologies. Establish actual coverage, access, terms, update cadence and failure behavior before choosing. |
| Service representation | Distinguish line identity/display number, operator/authority, direction, destination, route variant, ordered stop occurrences and departures valid on a specific operating date. Similar names and shared line numbers do not establish identity. |
| Dated shift matching | Match a stable imported activity to a concrete dated departure and stop pattern. Investigate available trip identifiers, operating date, times, direction, endpoints and source namespace/version. Line number alone is insufficient; never invent missing evidence. |
| Assisted completion | Propose direction, destination and stops when the match is unambiguous under an agreed rule. Ambiguous alternatives need visible evidence and user resolution; no match remains explicitly unresolved. Whether a unique proposal is applied automatically or requires confirmation remains open. |
| Provenance and corrections | Preserve imported facts, external facts, user corrections and confirmation separately. Record enough source identity/version, retrieval time, validity and matching evidence to explain a proposal. Refresh must not silently replace corrections or treat an external update as human confirmation. Raw-data retention and licensing remain open; private originals retain their existing transient boundary. |
| Service time | Preserve operating/service date separately from calendar date, timezone and extended-hour source notation. Friday service at `25:30` can fall on Saturday at `01:30` without becoming Saturday service. Later specification must settle source semantics, offset conversion and DST ambiguity; clock sorting alone cannot infer dates. |
| Data quality and availability | Distinguish missing coverage, stale data, absent departures, changed/cancelled services and source outage. Define last successful retrieval separately from source validity/update time. Do not claim a complete or current service from an empty result. Decide how reviewed matches behave across feed versions and expired coverage. |

## Define “complete” before claiming coverage

No coverage promise is established. Define a measurable coverage contract with at least:

- Geographic boundary and transport modes, including services crossing the boundary.
- Operators/authorities and the handling of overlaps or missing operators.
- Required content: lines, variants, destinations, stop places versus boarding points, ordered stop occurrences and dated departures; explicitly state whether geometry, accessibility and cancellations belong.
- Historical/future operating-date horizon, publication validity, update frequency and permitted staleness.
- A way to report supported, partial, unknown and absent coverage, rather than one unconditional completeness label.

Tromsø may be a pilot. Geography and operator selection must not be hardcoded into the general model. V1's example lines 20/24/28/42 are context, not a definition of a complete network.

## Overview/matching versus actual driving

This planning track initially concerns timetable overview and matching. An ordered stop pattern describes scheduled service; it does not establish actual location, next stop or completed work. Preserve manual activity selection, explicit Start/End and manually registered outcomes.

Automatic stop progression is a separate possible scope decision. If later included, specify the GPS/realtime observation source, timestamps, accuracy, missing/stale observations, map/stop matching uncertainty, user correction and failure behavior together with progression. Scheduled time alone is never evidence of physical position. No GPS or realtime integration is selected here.

## Dependencies and integration questions

The existing assistant supplies stable activity/workday identity, reviewed import facts, manual corrections, online revisions/retry, access control and private/demo separation. Future architecture must decide whether timetable enrichment is a proposal in draft review, a separate linked reference or another explicitly approved lifecycle change. It must not silently mutate an activated or terminal plan. A public route catalogue and private shift associations may need different ownership/retention; the current private seven-day bounds cannot be expanded by assumption.

Potential shared concepts with Automatic Notice Retrieval are namespaced operator/authority IDs, line IDs, stop/place IDs, dated journey IDs, validity intervals, source versions and retrieval/freshness evidence. These are candidate contracts, not verified common identifiers. Keep display line numbers separate from external IDs and retain mapping provenance. Neither extension is an assumed prerequisite of the other: route matching should be useful without notices; notices may continue using qualified line/date relevance without a full network. Shared adapters or registries need an explicit owner and justified dependency direction later.

## Explicit exclusions

No new network generation, route/line/frequency optimization, fleet allocation, driver scheduling or replacement of the shift source. No implementation, bulk ingestion, database design/migration, source selection, precise disruption matching or operational driving qualification in this establishment. No reinstatement of offline continuity, mentor workflows, export, cloud deployment or deferred V1 requirements.

## Open questions for the next planning step

1. What exact geographic/operator/mode/content/date envelope makes the pilot complete, and what partial coverage is useful?
2. Which authoritative sources actually offer that envelope, at what access/usage terms, quotas, update cadence and cost?
3. Which identifiers survive source updates and connect a shift activity to a dated departure? What evidence is available when source trip IDs are absent?
4. How are route variants, directions, destinations, platform/stop-place differences, loops, repeated stop visits and short workings represented without false merging?
5. How will service dates, extended-hour times, calendars/exceptions, DST, cancellations and changed departure patterns be reconciled across sources?
6. What establishes an unambiguous match? How are alternatives, user confirmation, manual overrides and later source conflicts presented?
7. What data may be retained for provenance, for how long, and how is public reference data separated from private workday links and expired work?
8. What happens offline or during a source outage without accidentally promising offline private execution? What staleness threshold is useful?
9. Which contracts can be shared with Automatic Notice Retrieval after that extension has its own planning documents?
10. Is automatic progression excluded from the first extension increment? If reconsidered, what observational evidence and operational qualification would justify it?

Resolve the coverage and evidence questions before binding a source technology or deriving implementation stories. No answers are silently assumed by this document.
