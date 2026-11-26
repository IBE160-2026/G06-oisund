# Coverage and staged scope

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

P1/API-first is now supplied planning scope; A2/P2 and remaining defaults stay provisional, not approved implementation requirements. Supports CAP-1 and stage boundaries for CAP-2–7. Research basis: adopted research.md §§1, 5 and recommendations. Completeness is always relative to a named manifest revision and service-date interval.

## P1 — qualify matching, not a network-completeness claim

Current first-epic planning boundary: a bounded preparation/review experiment for **Svipper line 20**, both directions, including the published variants in a declared seven-consecutive-service-date interval. Select dates inside verified source coverage and record them literally for each run. The retained research observations for 2026-10-26 through 2026-11-01 are seed evidence, not a promise that a future live API retains those dates.

Use targeted Entur line/journey/date lookups and retained, attributed public evidence. Inspect planned calls, direction/destination and source provenance for a stable imported activity. Keep all outcomes reviewable and require user confirmation. Restrict the first association workflow to draft review; do not revise an active plan. No network-wide import, map, geometry or automatic progression is required.

P1 can begin as a later isolated reference-display/constructed-case experiment without a complete operator manifest, proven privateCode crosswalk or regional importer. Those absences must be labelled. Claims of correct matching to an actual imported shift require the independent dated pairs in QF-02. Constructed negatives cannot prove provider coverage. Unsupported cases remain unresolved, not silently supported.

## P2 — proposed complete four-line pilot

| Dimension | Concrete proposed definition | Evidence needed before a complete claim |
|---|---|---|
| Area | Existing public passenger journeys on selected Tromsø city-bus lines; include each selected journey's whole published pattern, including cross-boundary stops, branches and extensions. Do not clip at a municipal polygon. | Confirm published pilot membership and inclusion/exclusion list; geographic wording does not silently include every other Tromsø service. |
| Lines | Public lines **20, 24, 28 and 42**, both directions and all published variants and dated departures. | Explicit namespaced IDs and a dated authority-approved/reference manifest. Research observed IDs for 20/24/42; line 28 coverage/identity remains unqualified. |
| Authority/operators | Svipper authority (research observed `TRO:Authority:1`) plus every actual operator of the included journeys. | Enumerate exact operator IDs/names and exceptions from source; authority is not the operating company. Do not infer the list from branding. |
| Required content | Line identity/display code, authority/operator, source direction, destination displays, pattern, ordered occurrences, stop-place/platform references, boarding/alighting rules, planned passing times, valid service dates and exceptions, source validity/provenance. | Every required value or explicit legitimate unknown classified; unresolved required identity/order/time/calendars prevents that cell passing. Optional source metadata unknowns do not disappear. |
| Horizon | **28 consecutive service dates**, inclusive `D` through `D+27`, rolling from a named pilot check date in the applicable service timezone. Include calendar instants beyond the final date for services belonging to it. | Every line/date cell and variant/journey in scope checked against a source inventory; a min/max date range is not proof of continuity. |
| Geometry | Optional, separately reported dimension; not required for matching-complete pilot. | Never infer geographic trace completeness from a stop list or map picture. |
| Exclusions | Other lines/modes/operators outside the declared line set, private/non-public duties/deadheads, vehicle allocation and physical observations. | Publish explicit exclusions beside coverage; “complete four-line pilot” never means all Tromsø city buses. |

A request for all official Tromsø city-bus lines expands the manifest and qualification work; it is Q1, not an inferred commitment. General contracts use configuration and namespaced identities, so other areas/authorities can be added without embedding these line numbers in identity or matching rules.

## Coverage accounting

The manifest records revision, inclusion rules, authoritative source/retrieval date, explicit line and operator identities, service interval, dataset/snapshot versions and per-dimension status. A cell is a declared line/operator/date and its expected published journeys/patterns/calls; operator exceptions must not be hidden in a line-wide count.

Report supported/complete, partial, unknown and absent/not-applicable with reasons. A verified no-service calendar day is not a missing fetch. A failed API, truncated result, unresolved reference or missing calendar is not proof of no service. “Complete” requires all mandatory cells and dimensions to pass and no unresolved coverage gaps. Counts and IDs used as expectations must come from an independent inventory or checked extraction, not the matching implementation's output.

Do not combine multiple point-to-point travel suggestions into a claimed exhaustive inventory. Research's empty datedServiceJourneys response alongside valid static journeys is a specific counterexample to trusting one convenient query as completeness evidence.

## Acquisition progression — recommendation, not architecture adoption

P1: qualified targeted Entur queries with meaningful client identification, bounded fields/results, GraphQL error inspection, source timestamps and actual response quota handling. Only minimum public route/date/place facts leave the private boundary; no uploaded shift file, account/session identity or unnecessary private schedule is sent.

P2: qualify one controlled regional Troms NeTEx snapshot with the appropriate valid National Stop Registry (NSR) references, then compare coverage against the manifest. Record schema/profile/parser and referenced object versions. NeTEx is the research-preferred candidate because of source richness, not a committed library/database design. Regional acquisition must respect published access/download limits and avoid repeated full downloads.

GTFS remains an alternative after comparing every required datum, service calendar, destination/occurrence rule and identifier crosswalk. Document losses explicitly; adopt only if the agreed pilot semantics survive. Archive HEAD availability is not qualification. Svipper PDFs/maps/planner provide local discrepancy checks; neither identical content nor synchronized updates with Entur is assumed.


## Current P1 planning binding

The short epic is [CRN-E1](../../planning/epics.md). Its [revision1 manifest](pilot-manifest.md) names all seven service dates; it is historical/partial evidence, not promised future live coverage. P1 line20/draft/API-first is supplied planning scope; P2 remains unapproved and outside this epic. Implementation waits until V1 complete/tested for a while and separate owner authorization.
