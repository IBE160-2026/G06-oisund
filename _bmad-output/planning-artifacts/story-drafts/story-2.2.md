---
status: approved
created: 2026-09-25
epic: E2
story: '2.2'
type: qualification
approved: true
approvedOn: 2026-09-25
dependencies: []
---

## Epic 2: Prepare and Revise a Confirmed Whole Working Day

This early source qualification addresses dated timetable matching and whole-day preparation under AD-7. It is separate from OCR qualification (2.1), operational notice-source qualification in E4 and target-device qualification in E3/E8. Stories are reviewed sequentially; the investigations have no implementation dependency on one another.

### Story 2.2: Verify Dated Trip Matching and Whole-Day Timetable Coverage

As the pilot owner,
I want evidence that the selected timetable queries can identify my actual scheduled trips and supply their complete stop lists,
So that preparation does not silently select a similar trip or leave later parts of my day unavailable.

**Acceptance Criteria:**

**Given** representative anonymized shift facts and accessible timetable evidence,
**When** the bounded qualification case inventory is prepared,
**Then** it identifies service date, IANA timezone, route, direction, starting/ending stops and departure for expected passenger trips on pilot lines 20, 24, 28 and 42,
**And** explicitly includes overlapping 20/24 routes/shared stops, relevant service-calendar differences and a midnight/date-boundary case where available,
**And** expected facts are checked independently of the candidate query result, with evidence provenance; missing or ambiguous reference facts remain unresolved,
**And** real-source cases, synthetic edge cases and untested cases are labelled separately; lack of historic source data does not become evidence of incorrect shift facts.

**Given** the owner-confirmed distinction that Tide shifts use a service date and extended hours beyond 24:00, while Svipper displays ordinary clock time on the applicable calendar date,
**When** qualification translates a Friday 25:30 shift entry for matching,
**Then** its calendar representation is Saturday 01:30 in the applicable local timezone,
**And** the original Friday service date, original extended time and position in the working-day sequence remain available and are not rewritten as a Saturday-service shift,
**And** the report documents both representations and the translation, including checked cases around midnight; it does not infer a service date from calendar display time alone.

**Given** independently checked expected cases where multiple trips can be displayed as Saturday 01:30, including different service-day identities where source evidence permits,
**When** the candidate matcher compares the translated shift entry with returned journeys,
**Then** it uses supported service/calendar facts, trip identifiers, route, direction and endpoints rather than treating the shared displayed timestamp as unique,
**And** it retains and reports unresolved candidates when available evidence does not distinguish them, requiring driver choice rather than silently choosing a service day,
**And** the report records expected versus actual matches and whether each ambiguity case was exercised against real source responses or a labelled fixture.

**Given** those dated case facts and the targeted Entur API approach adopted in AD-7,
**When** candidate timetable queries are exercised,
**Then** record query strategy, source identifiers, service-calendar interpretation, retrieval time, returned candidate count and available stop/time ordering,
**And** inspect and document the actual Entur response date/time fields and trip identifiers, their documented meanings and observed values: distinguish explicit service-date evidence from calendar timestamps and derived/inferred values,
**And** do not assume Entur exposes a particular service-date field or that its displayed departure timestamp proves the journey's service date; absent semantics or identifiers are reported as gaps,
**And** compare results against the expected route, direction, date, departure and endpoints rather than accepting the first suggestion or line-number match,
**And** optimized journey-planner suggestions are never treated as a complete trip catalogue,
**And** record the source's applicable access limits, attribution/licensing conditions and the actual requests needed for representative day preparation without asserting untested throughput.

**Given** a query produces one supported match, multiple plausible matches, no match or source failure,
**When** results are classified,
**Then** the report distinguishes all four outcomes and provides evidence for automatic unique matching versus required driver choice,
**And** a successful no-match response is not conflated with unavailable, incomplete or failed retrieval,
**And** no alternate route/date/direction is silently substituted, and missing stop sequences are never fabricated,
**And** test ambiguous and failure behavior with labelled synthetic responses if no real example occurs; synthetic cases do not establish real-source coverage.

**Given** a representative complete working-day case, including later trips and separate work parts where available,
**When** all its passenger trips are resolved using the candidate strategy,
**Then** compare expected and retrieved trips/stops/times and list each supported, unresolved, unavailable or incomplete item,
**And** resolve pagination or other response-limiting behavior where applicable before claiming completeness,
**And** document what source data and identifiers a later OfflineBundle must retain for every available trip, not only the first active trip,
**And** non-passenger activities remain known shift activities; absence of an Entur trip does not erase or misclassify them,
**And** whole-day data coverage is kept separate from browser-asset readiness, access lifetime and real offline execution.

**Given** missing stop information or calendar/time ambiguity,
**When** the qualification evaluates recovery options,
**Then** identify any evidence-supported recovery from available timetable data and record its limits,
**And** preserve the established fallback: known trip facts plus Stoppinformasjon mangler, no automatic stop progression and permitted manual completion/abort/next activity in later implementation,
**And** the report never treats that fallback as proof the timetable source covers the trip or that an offline client can fetch previously unavailable data.

**Given** qualification findings and reproducible source evidence,
**When** the report concludes,
**Then** distinguish matching that works, cases requiring driver selection, missing/incomplete data and cases not tested,
**And** include the extended-service-time to calendar-time translation, retained shift ordering, actual Entur field/identifier evidence and unresolved temporal ambiguities in the conclusion,
**And** state whether targeted API queries have demonstrated the necessary day preparation for the tested cases, without generalizing beyond the sample,
**And** if the approach is insufficient, return a concrete gap and options to the owner at AD-7's NeTEx/GTFS reconsideration point instead of implementing a bulk pipeline or changing architecture independently,
**And** completing the report is distinct from passing the timetable capability gate; a negative result does not remove FR-3 or substitute simulated/manual schedules as acceptance evidence.

**Given** evidence is prepared for the repository or course assessment,
**When** the report and reproduction procedure are saved,
**Then** retain sanitized case IDs, methods, source references, aggregate outcomes and labelled generic/fictional edge fixtures,
**And** do not publish exact private shift/bus/vehicle-duty/trip identifiers or create a permanent operational quality dataset,
**And** temporary private case associations follow the existing handling/deletion boundaries; public source data is not mistaken for permission to retain private shift associations,
**And** the report states the tested dates/formats of responses and failure categories actually exercised, with remaining gaps rather than fabricated passes.

**Traceability:** FR-3, FR-4/5 activity/identity boundaries, foundational FR-17/20 whole-day data needs, NFR-2/3/4; UX-DR5/6/7/43; AD-7 targeted queries and qualified matches, AD-5/9 service-date/progression separation, AD-12 private evidence boundaries; PRD B-2 and the approved early source-qualification queue. Notice coverage FR-12–15 is not claimed here.

**Dependencies:** No implemented application or prior qualification story required. Needs representative anonymized case facts with a checked reference, source access and a small reproducible query procedure. E1/E2 implementation later consumes the conclusions; Story 2.1 need not be completed because known case facts may be entered directly for qualification. No source account/service provisioning, production adapter, import UI or full data warehouse is part of this story.

**Size boundary:** One bounded timetable/day-coverage investigation and decision report for the pilot configuration, not all Tromsø routes, a permanent feed ingestion system, notice-source evaluation or route calculation. Missing sample categories remain explicit; do not enlarge the investigation indefinitely or mark gaps passed.

**Evidence boundary:** Actual source queries establish only the recorded coverage at the tested time. Reproducible synthetic cases support E8-D behavior demonstration but do not qualify real matching. Later integrated preparation, OfflineBundle/restart and Lenovo/Brave tests remain required by E8-P. E8-E follows pilot qualification. No queries or tests were executed by drafting this story, and no readiness workflow or implementation has started.

**Approval:** Approved by the owner on 2026-09-25 with the explicit Tide service-date/extended-hour versus Svipper calendar-date/clock-time distinction. Friday 25:30 translates to Saturday 01:30 without losing Friday service identity or working-day position. Qualification must use checked expected cases including several Saturday 01:30 candidates, inspect actual Entur date fields/trip identifiers and document translation and ambiguities without assuming display time identifies service date. Approval concerns the planned investigation, not verified source behavior. The approved copy in epics.md is canonical.
