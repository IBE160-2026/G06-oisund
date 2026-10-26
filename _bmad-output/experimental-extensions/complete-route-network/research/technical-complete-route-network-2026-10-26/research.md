---
title: Complete route network — technical source research
type: technical
topic: complete-route-network
decision: How to acquire represent refresh and match existing dated services
source: native-run
status: complete
preset: standard
validation: normal
claims_verified: 2
claims_unverified: 10
created: 2026-10-26
updated: 2026-10-26
---

# Complete route network — technical source research

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## Decision summary

**Recommended planning direction:** first test matching with small Entur Journey Planner lookups, then use the regional Troms NeTEx export plus appropriate National Stop Registry (NSR) references as the candidate canonical catalogue for a complete pilot. Keep GTFS as a simpler alternative if a field-by-field loss assessment accepts its limits. This is a research recommendation, not an approved architecture or implementation requirement. NeTEx retains the richest Norwegian source model; point-to-point journey planning deliberately filters alternatives and cannot establish a complete inventory. [1][2][3]

The immediate feasibility result is positive but bounded: live queries exposed namespaced line/journey/pattern IDs, internal private codes, dated planned calls, NSR platforms/stop places and changing destination displays. One ordinary line 20 departure agrees with a separately published Svipper timetable. A night departure preserves its Saturday service date while leaving on Sunday at 01:30. These cases support a reviewable matching experiment; they do not prove all city services, calendars or internal shift numbers can be linked. [4][5][6]

Svipper and Entur may share upstream planning data; their agreement is a useful publication check, not independently generated ground truth.

The principal unresolved issue is the crosswalk from a shift's internal trip number to a public ServiceJourney. The normative model permits a PrivateCode, but no provider-approved mapping or representative dated shift/public-feed pair was obtained. Do not auto-confirm from number equality or nearest departure time. Full pilot coverage and cross-version ID stability also remain unqualified. [7][8]

## Evidence and scope

Research accessed official sources on **2026-10-26**. Documents are English; the user-facing summary is Norwegian. Worktree: `D:/IBE160-plan-complete-route-network`; branch: `codex/plan-complete-route-network`; starting commit: `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed`. All new outputs are within this run. The installed Deep Recon technical pack guided three research dimensions and normal verification. User explicitly authorized Run and reasonable bounded choices. No global configuration changed.

Evidence labels used below:

- **Documented:** a primary source states the capability/semantics. Medium confidence when one publisher supports it; not empirical coverage.
- **Observed:** retained request/response or inspected public document. Medium confidence for that observation; no general completeness inference.
- **Cross-checked:** separately published sources agree on a narrow claim. High confidence requires independent underlying evidence; agreement between Svipper and Entur alone does not establish independent data lineage.
- **Recommendation / inference:** proposed design derived from evidence; not a fact about an existing integration.
- **Unverified:** missing evidence, including cross-source equivalence and coverage. The ledger's `unverified` includes credible single-publisher claims that lack independent confirmation; it does not mean those observations failed.

Three researcher streams examined access/formats, identity/time and local controls. The lead performed 11 small GraphQL requests including schema discovery and one rejected query, one TRO import-metadata GET and two archive HEAD requests. No regional timetable/stop archive was downloaded. Two local timetable PDFs were retained; there was no bulk crawl. Source digests, exact query files, public responses and file hashes are in `digests/` and `imports/`. [4][5][6][9]

## 1. Access choices and completeness

### A measurable definition of complete

**Proposed qualification contract:** published passenger city-bus services in an explicitly approved Tromsø pilot boundary, from identified authorities/operators, across an explicitly chosen operating-date interval. Include every published line, dated service, pattern and stop occurrence in that interval, with calendar exceptions and boarding/alighting semantics. Geometry is a separately declared coverage dimension. Configure this manifest; never bake line 20 or TRO into general identity rules.

Obtain an independent city-bus line manifest, cross-boundary policy and desired horizon before claiming completeness. A provider archive may contain other modes/regions. Public data must not be presumed to include all deadheading, duty blocks or private operational movements: the separate timetable-management documentation describes additional restricted material. Here, “complete” concerns published passenger services, not complete driver scheduling. [15]

### Access comparison

| Approach | Documented/observed strengths | Limits and operational burden | Recommended role |
|---|---|---|---|
| Targeted Entur GraphQL | Open endpoint; query line, ServiceJourney and date-specific calls with exact fields. Live pilot responses include IDs, privateCode, calendars, ordered quays and destinations. [2][4] | Remote dependency, quotas, query validation and finite loaded horizon. A selected response is not a provider archive. Point-to-point `trip` returns selected travel options. Live `datedServiceJourneys` was empty while static journeys existed. [2][4][10] | First matching qualification and focused passenger-facing verification; a bounded selected-journey lookup, not proof of complete network enumeration. |
| Regional NeTEx | Entur's richest public format; separates network, service calendars, journey patterns and passing times. Current official Troms ZIP link exists. [1][7][9] | XML references, inherited context/validity, versions, calendar expansion and schema evolution require careful ingestion. Region/provider is broader than city pilot. Actual contents have not been parsed here. [7][8][9] | Candidate canonical full-catalogue input, subject to scoped dataset qualification. |
| Regional GTFS | Familiar tabular routes/trips/stops/stop_times/calendars/shapes model; easier bounded importer. Current Troms ZIP offered and reachable. [3][9] | Entur warns of conversion loss, particularly text. Public/internal journey semantics and provider mappings must be checked. Basic versus extended route types is a separate issue from completeness. [1][3] | Viable simpler alternative where every required field and matching key survives; optional downstream projection. |
| Svipper PDFs/maps/planner | Independent passenger-facing locality check, notes and variants. PDF sample gives timetable times matching one API case. [5][6][11] | Dynamic interfaces, selected timing rows, document/metadata validity mismatch and unverified map/planner results. Not an authoritative machine-readable stop-pattern catalogue. [5][6][11] | Control samples and discrepancy investigation, not primary bulk acquisition. |

### Access, licence and freshness

Journey Planner uses POST `https://api.entur.io/journey-planner/v3/graphql` with JSON and a meaningful `ET-Client-Name`; open access does not require the partner OAuth contract. Reuse under the Norwegian Licence for Open Government Data (NLOD) requires attribution and observing exceptions/modification notices; the service terms give no completeness/availability warranty. Attribute Entur and original suppliers as required by the actual applicable licence before distribution. [2][12]

Entur documents separate trip/other-request rate policies and HTTP 429 handling. Observe response quota/expiry headers; do not hammer a quota failure. The live header window differed from the documentation's per-minute presentation. A schema request with two `__type` fields returned HTTP 200 plus `BadFaithIntrospection`; successful HTTP alone is insufficient. This is a query guard, not evidence of an outage. [4][10]

Exports refresh on provider submission and nightly. Entur discourages excessive downloading, normally expecting no more than one download per 24 h. Exports trim expired service beyond 48 h, so a mutable latest ZIP cannot reproduce an old confirmed workday. Nightly archive timestamps and original provider import time answer different questions. [1][13]

Current offered links, resolved from the official deployed table component and checked with HEAD only: [9]

| Object | URL | Observed metadata on 2026-10-26 |
|---|---|---|
| Troms NeTEx | `https://storage.googleapis.com/marduk-production/outbound/netex/rb_tro-aggregated-netex.zip` | HTTP 200; 7,718,133 bytes; modified 2026-10-25 23:27:17Z; generation 1792970837742987. |
| Troms GTFS | `https://storage.googleapis.com/marduk-production/outbound/gtfs/rb_tro-aggregated-gtfs.zip` | HTTP 200; 14,346,274 bytes; modified 2026-10-25 23:27:55Z; generation 1792970875012487. |
| Original TRO import metadata | `https://api.entur.io/timetable-public/v1/timetable-import-info/import_date/TRO` | HTTP 200; body `2026-10-23T12:01:39`, without a timezone suffix. |

These sizes do not establish general format efficiency. HEAD establishes object availability, not parsed contents or date coverage. The stop registry separately offers current Troms stops, plus national current/future/historical version options; timetable matching may need the version valid at the departure date. [9][14]


## 2. Representation, identity and stop patterns

**Documented:** NeTEx distinguishes Line, Route/JourneyPattern, ServiceJourney, operating calendars and dated instances. ScheduledStopPoint/PointInJourneyPattern references and NSR StopPlace/Quay have different roles. GTFS independently distinguishes route/trip, service_id, ordered stop_times and optional shape geometry. [3][7][8][16]

**Recommended conceptual separation:** retain namespaced source entity IDs and versions; public line code as display data; journey identity plus operating date; pattern identity plus ordered stop occurrences; platform and parent stop-place IDs; original service times and derived dated instants; destination display at each relevant occurrence. This is an input for a later specification, not a database schema.

A stop list is an ordered sequence, not a set. Keep occurrence index even when the same platform is visited twice. GTFS uses trip_id plus stop_sequence; sequence need not be consecutive. Geometry describes the path between stops and is neither a substitute for call order nor evidence that every shape exists. The four sampled journeys had no repeated quay IDs; ringline/repeated-stop behavior is supported by specifications but still needs actual pilot fixtures. [3][4][16]

Headsign belongs to the selected journey/occurrence. Nordic rules explicitly support changing destination displays and circular services; GTFS supports stop-level headsign overrides. `inbound/outbound` or direction_id are source conventions, not universal compass directions. Do not derive the destination by reversing the other direction's stops or by taking a line-wide default. [3][16]

## 3. Matching an imported shift activity

NeTEx VehicleJourney PrivateCode may hold a planner trip/train number; PublicCode and the full entity ID are distinct. The live API exposes all three fields; sampled publicCode was null while privateCode 1000, 1009, 1133 and 6600 were populated. An ID suffix resembling a number is not a documented crosswalk. [4][7]

**Recommended candidate evidence:** source/operator namespace, explicit service date, scoped line identity, known scheduled origin/departure and destination/arrival, and ordered endpoint/intermediate occurrences where supplied. Prefer a verified provider journey crosswalk when available. Retain the raw imported trip number independently. A partial shift segment may cover only a subrange of a public journey; retain first/last occurrence positions instead of inventing a new full departure.

A later matching contract should separate:

1. **Confirmed identity:** supported crosswalk or user-confirmed candidate, valid on that operating date, with compatible planned timing/stops.
2. **Unique proposal:** exactly one candidate within the declared source/date/coverage bounds and agreed evidence rules. It can suggest direction, destination and stops; automatic application versus explicit confirmation remains a product decision.
3. **Ambiguous:** multiple plausible departures, patterns or occurrence ranges. Show differences and request a choice; nearest-time ranking is not confirmation.
4. **Unresolved:** insufficient source coverage, missing date/ID mapping or incompatible facts. Preserve unknowns and manual entry.

Project input context only: the existing anonymized fixture oracle `Eksempelfiler/README.md` distinguishes line/trip numbers, vehicle duty and non-passenger movements, but its shifted 2030 dates and partial stop oracle cannot validate 2026 public journeys. No private shift payload was sent externally. Real shift-to-public matching remains unverified; a provider explanation and independently expected example pairs are needed. This contextual source is not counted as external research evidence.

## 4. Time, dates and exceptions

**Cross-checked normative support:** both Nordic NeTEx and GTFS distinguish service-day time from calendar display and allow service beyond midnight. NeTEx encodes time plus day offset; GTFS can encode 25:30 directly. Calendars require weekday rules plus additions/removals and validity; a recurring template alone does not establish operation on a requested date. [3][7][8]

Daylight saving time (DST) is more subtle than attaching a timezone to each clock time. Nordic passing times use the timezone in effect at operating-day noon consistently; GTFS defines its time origin as service-day noon minus 12 h. Preserve the source representation and inherited timezone/context, resolve instants on that axis, then derive passenger wall time. These standards align on the need for a service-day reference; do not assume every input format or provider applies identical conversion rules. [3][17]

Observed night raw departure `01:30:00, dayOffset=1` on 2026-10-31 becomes 2026-11-01 01:30+01. The same journey on 2026-10-24 becomes 2026-10-25 01:30+02. The query for 2026-10-26, when this service did not operate, returned zero calls. This confirms one ordinary post-midnight case and one offset before the autumn fold, not repeated 02:xx times or the spring gap. Those, holiday exceptions and the shift source's own time convention require independent examples before implementation. [4]

## 5. Actual Tromsø samples

The selection deliberately covers both directions, a longer destination variant, midnight and a short-origin night service. The API returned Svipper authority `TRO:Authority:1` and line IDs `TRO:Line:1_20`, `1_24`, `1_42`; only line 20 received journey-level enumeration. Its response contained 799 templates and 136 active on 2026-10-26, with active dates across templates ranging 2026-10-19–2027-02-28. This is a response observation, not guaranteed continuous or all-line horizon. [4]

| Sample | Operating date and public identity | Observed planned calls/result |
|---|---|---|
| Ordinary outbound | 2026-10-26; `TRO:ServiceJourney:20_260918104872543_1009` |42 calls; Skattøra 06:35 → Malmvegen 07:25+01; display Kroken via sentrum then Kroken. |
| Ordinary inbound | 2026-10-26; `TRO:ServiceJourney:20_260918105148184_1000` |43 calls; Malmvegen 05:16 → Skattøra 06:09+01; display includes Stakkevollan via sentrum/via UNN. |
| Destination variant | 2026-10-26; `TRO:ServiceJourney:20_260918104886042_1133` |79 calls; Skattøra 23:03 → Steinnes 00:21 next calendar day; distinct JourneyPattern. |
| Short-origin night | 2026-10-31; `TRO:ServiceJourney:20_260918105162575_6600` |25 calls; Fr. Langes gate → Skattøra, next calendar day 01:30–01:50; dayOffset 1. |

All table values are retained observations. [4] Example NSR distinction: Malmvegen is StopPlace 54782, with different scheduled quays 93604 and 100583 in the sampled directions. A destination label such as Stakkevollan need not equal the final quay's literal name. Some returned calls had realtime=true; this report uses aimed times and makes no physical-position claim. [4]

**Local publication cross-check:** Svipper PDF 20 weekday Malmvegen 05:16 → Skattøra 06:09 agrees with the inbound API sample. Other inspected PDF rows expose tunnel-marked variants and short-origin/night columns. PDF 42 shows opposite directions and an ordinary 23:55 → 00:53 crossing. Those extracted night columns were not visually qualified, so they are leads rather than acceptance fixtures. [5][6]

**Observed official-source disagreement:** widget metadata gives 2026-09-01–12-31 for both PDFs; PDF 20 header ends 2026-11-01, while PDF 42 ends 2027-01-03. Preserve document and metadata validity separately. Neither discrepancy establishes an Entur defect or a measured publication lag. [5][6][18]

**Counter-evidence and access limits:** the datedServiceJourneys query for lines 20/42 on 2026-10-26 was empty despite valid static journeys/calls. The dynamic Svipper planner yielded no readable journey result, and the linked 2025 line-map topology was not verified. No all-line inventory, geographic geometry or ringline sample was qualified. [4][11] No red-team pass was configured; these are discrepancies found during ordinary acquisition.

## 6. Refresh, storage and confirmed workdays

**Recommended lifecycle:** fetch public catalogue snapshots into a separately owned reference area; validate before activation; record URL, retrieval time, provider import time, object generation/ETag/hash, profile/parser version, validity and coverage manifest. Compare entity versions and semantic content; retain last known good reference with explicit staleness if refresh fails. Removed or changed entities are not silently reassigned. Entur's profile includes versioning; its documentation currently has inconsistent embedded version labels and evolving DatedServiceJourney structure, so pin the actual exchange/profile revision. [9][13][17][19]

For a confirmed workday, retain the selected source journey ID and operating date, snapshot identity, ordered call subset/positions, source time representation, timezone and derived planned instants, shown destination facts, matching evidence and who confirmed/corrected them. Keep imported, external and manual values distinguishable. A refresh should produce a reviewable difference or unresolved association, not silently rewrite confirmed/manual facts. A cancelled/replaced departure remains traceable to the originally selected plan. [7][20]

Public source snapshots and private workday links need separate retention rules. The recommendation does not authorize longer private retention, permanent raw shift originals or an offline private cache. Public archive retention rights/attribution and disposal policy must be settled in the extension spec. API availability and loaded history are not durable storage; a separate partner raw-data version API exists, but its access/retention was not qualified as a public fallback. [1][12][21]

## 7. Boundary with automatic notice retrieval and progression

The current Entur realtime documentation lists TRO support for SIRI ET/VM/SX and GTFS-RT trip updates/positions; its TRO GTFS-RT Service Alerts cell is blank. Do not infer that GTFS-RT alerts are the correct Troms notice stream. Default SIRI IDs are mapped to static route data; `useOriginalId=true` switches to underlying-system IDs in the documented SIRI modes. Choose and record a mapping mode. [22]

Proposed interface to the separate notice extension: namespaced line ID, NSR stop-place/quay ID, ServiceJourney ID plus operating date/origin planned time, optional dated ID, ordered call index, source snapshot and validity interval. SIRI-SX supports network/stop/journey scope; preserve broad scope when exact journey matching is unavailable. GTFS-RT selectors refer to the corresponding static feed and can need date/start time; exact NeTEx↔GTFS ID conversion still needs qualification. [20][23][24]

No other extension was edited and no shared schema/dependency was adopted. Route matching can operate without notices; notice retrieval can deliver qualified line/date candidates without a complete network. Position/progression remains a separate observation contract: GPS/vehicle ID, observation timestamp, accuracy, age, uncertainty and manual correction. Timetable calls, direction and realtime schedule flags alone do not establish actual physical position. [22]

## Recommendations and next BMAD step

1. **[SPC] `bmad-spec` next:** distill this report with scope/source-map into the smallest useful extension experiment. Define the pilot line/operator/date manifest, proposal/confirmation behavior, failure states and stop conditions. Keep output under `complete-route-network/specs/`; do not modify V1 or run Build. Evidence basis: feasible bounded API calls, one cross-publication timetable match, unresolved crosswalk/full coverage. [4][5]
2. **API qualification before regional ingestion:** obtain provider-supported internal-number semantics and a small independent oracle covering unique, ambiguous, absent, partial and overnight matches. Query exact known journeys/dates with planned fields; never use point-to-point travel options as exhaustive matching candidates. [2][4][7]
3. **Then qualify regional NeTEx+NSR:** one controlled snapshot and an explicit city subset; validate calendars, references, destinations and occurrence order. Prefer this for complete provenance-rich catalogue; choose GTFS instead if the agreed subset loses no required meaning. Preserve the option to switch through source-specific adapters, without prebuilding a large integration framework. [1][3][14]
4. **[CA] `bmad-architecture` after the spec:** decide snapshot ownership, immutable workday associations, refresh/version policy, calendar/time conversion and the notice interface. Re-adopt the extension spine into SPEC companions. Then define extension-local stories; no V1 epic/story renumbering or sprint-status writes.

All are proposed next steps, not implementation approval.

## Open qualification gates

- Obtain approved complete city-bus line/operator/geographic manifest and required rolling horizon; quantify partial coverage and crossings.
- Parse one permitted regional snapshot and appropriate NSR versions. HEAD/API samples do not establish archive contents or continuous dates.
- Obtain a supported internal-number crosswalk and actual-date anonymized matching pairs; establish tolerances and ambiguity rules independently of the matcher.
- Compare at least two provider versions for journey/pattern/stop ID drift, changed calendars, destination changes, deletions and manual overrides.
- Qualify repeated stops/ringlines, short workings, shift subranges, holiday additions/removals, spring gap and both autumn-fold occurrences against independent expected times.
- Resolve PDF/widget validity discrepancies with Svipper; visually qualify table columns and inspect an actual planner/map result if needed. No synchronization assumption.
- Establish notice identifier mapping and TRO SX coverage on actual examples before linking messages to a departure; no realtime/position stream was ingested.
- Set licence attribution, public/private retention boundaries, update cadence and source-outage/staleness policy in the extension spec. Recheck changing docs/schema before implementation.

## Source appendix

All accessed 2026-10-26. Dates are publisher-modified/revision dates where available; unknown means not established. Confidence reflects scope, not a warranty. The independent-check ledger is separate from source credibility.

| Ref | Supports | Publisher and source | Published / modified | Confidence |
|---|---|---|---|---|
| [1] | Export formats, updates and history trim | [Entur timetable data](https://developer.entur.no/open-data/timetable) |2026-05-21 |Medium, documented |
| [2] | GraphQL access and filtered trip planning | [Entur Journey Planner](https://developer.entur.no/docs/open-services/journey-planner) |2026-06-08 |Medium, documented |
| [3] | GTFS identity, dates, occurrences and geometry | [GTFS Schedule reference](https://gtfs.org/documentation/schedule/reference/) |2026-04-27 |High for cross-checked concepts; medium for GTFS-only details |
| [4] | Actual schema, IDs, dates, calls and errors | [Entur live GraphQL endpoint](https://api.entur.io/journey-planner/v3/graphql); saved `imports/api-*.json` |Observed 2026-10-26 |Medium observed; upstream independence unverified |
| [5] | Line 20 times, variants and header validity | [Svipper PDF 20](https://svipper.no/regtopp/api/route/download/pdf/20_010926.pdf) |Validity starts 2026-09-01; publication unknown |Medium; narrow ordinary row cross-checked |
| [6] | Line 42 timing/night rows and header validity | [Svipper PDF 42](https://svipper.no/regtopp/api/route/download/pdf/42_010926.pdf) |Validity starts 2026-09-01; publication unknown |Medium; night alignment unqualified |
| [7] | PrivateCode, calendars, passing-time offsets | [Entur Nordic timetable profile](https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728760393) |2026-09-23 page; embedded label older |Medium documented |
| [8] | ServiceCalendar/DayType/model distinctions | [Entur NeTEx data models](https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728596522) |2024-06-24 |Medium documented |
| [9] | Current archive links/availability/metadata | [Entur deployed table component](https://developer.entur.no/assets/TimetableTable-BjVlbSJI.js); exact ZIP URLs and HEADs in `imports/archive-head-metadata.json` |Observed 2026-10-26 |Medium observed |
| [10] | Quotas and retry policy | [Entur rate limiting](https://developer.entur.no/docs/open-services/journey-planner/rate-limiting) |2026-03-30 |Medium documented; headers observed separately |
| [11] | Local timetable/map/planner entry points | [Svipper timetable page](https://svipper.no/meny/reise/rutetabeller-og-kart/rutetabeller-buss/), [line maps](https://svipper.no/meny/reise/rutetabeller-og-kart/linjekart/), [planner](https://kart.svipper.no/reise) |2026-07-13 page; 2026-03-02 maps; planner unknown |Medium for links; results/topology unverified |
| [12] | Reuse, attribution and service limitations | [Entur terms](https://developer.entur.no/terms-of-service) |2026-09-28 |Medium documented; not legal qualification |
| [13] | Original import-date semantics | [Entur import metadata API](https://developer.entur.no/apis/timetable-import-info/timetable-import-info); exact TRO response in `imports/import-info-TRO.json` |Unknown docs; observed 2026-10-26 |Medium documented/observed |
| [14] | NSR identity and versioned stop exports | [Entur stop data](https://developer.entur.no/open-data/stops) |2026-05-21 |Medium documented |
| [15] | Public versus restricted operational content | [Entur timetable datasets](https://developer.entur.no/apis/timetable-management/datasets) |Unknown |Medium documented; access not exercised |
| [16] | Ordered pattern and changing destinations | [Entur Nordic network profile](https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728563886/network) |Unknown |Medium documented; concepts corroborated by GTFS |
| [17] | NeTEx time axis, versions and validity | [Entur NeTEx general information](https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728563782/General%2Binformation%2BNeTEx) |2025-11-05 |High for cross-checked service-day/DST concepts; medium details |
| [18] | Actual PDF widget metadata | [Svipper public search endpoint](https://svipper.no/regtopp/api/route/search); POST phrase 20/42 saved locally |Observed 2026-10-26 |Medium observed |
| [19] | Profile revision changes | [Entur profile changelog](https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728662188) |Entry 2026-09-23 |Medium documented |
| [20] | Planned/replaced/cancelled journey references | [Entur SIRI-ET profile](https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370392/SIRI-ET) |2026-08-25 |Medium documented |
| [21] | Separate partner version/history offering | [Entur raw timetable API](https://developer.entur.no/apis/raw-timetable-data/raw-timetable-data) |Unknown |Medium documented; access/history unqualified |
| [22] | TRO streams and static/original ID modes | [Entur realtime data](https://developer.entur.no/open-data/realtime) |2026-08-31 |Medium documented |
| [23] | Situation selectors and validity | [Entur SIRI-SX profile](https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370605/SIRI-SX) |2024-12-02 |Medium documented |
| [24] | Dated realtime/static identity and occurrences | [GTFS Realtime reference](https://gtfs.org/documentation/realtime/reference/) |Unknown |Medium documented; dated-identity concepts corroborate NeTEx |

## Staleness map

| Tracked claim | Class | Source/observation date | Computed recheck | State |
|---|---|---|---|---|
| Claim [1] | landscape | 2026-05-21 | 2027-05-21 | Within window |
| Claim [2] | patterns | 2026-06-08 | 2028-06-08 | Within window |
| Claim [3] | patterns | 2026-04-27 | 2028-04-27 | Within window |
| Claim [4] | live-observation | 2026-10-26 | 2026-11-26 | Within window |
| Claim [5] | live-observation | 2026-10-26 | 2026-11-26 | Within window |
| Claim [7] | patterns | 2026-09-23 | 2028-09-23 | Within window |
| Claim [9] | live-observation | 2026-10-26 | 2026-11-26 | Within window |
| Claim [13] | live-observation | 2026-10-26 | 2026-11-26 | Within window |
| Claim [14] | landscape | 2026-05-21 | 2027-05-21 | Within window |
| Claim [17] | patterns | 2025-11-05 | 2027-11-05 | Within window |
| Claim [22] | versions-compatibility | 2026-08-31 | 2026-09-30 | Due |
| Claim [23] | patterns | 2024-12-02 | 2026-12-02 | Within window |

Computed with the installed `recon_kit.py staleness` helper: landscape 12 months, patterns 24 months, versions/compatibility 1 month, and live observations 1 month (a conservative run-specific freshness cap). Source publication dates are preserved; observed data uses its actual observation date. Earliest computed recheck is **2026-09-30**, already due for the realtime compatibility claim. Its current page was reread during this run, but independent feed qualification is still missing; recheck it before implementing the notice adapter. Live observations next reach the one-month cap on **2026-11-26**, and should be refreshed sooner when planning data changes. This table is a refresh work order, not a source availability guarantee.

## Validation and delivery boundary

Mechanical citation check resolves all 24 source markers with no missing or orphaned rows. Fresh-context semantic checking found no load-bearing mismatch and identified the shared-upstream confidence caveat, now reflected above. Structure/prose findings were applied; exact observations and identifiers were preserved. Source digests and checks document remaining extraction limits. No red-team pass or product test was run.

The ledger counts are generated by the installed helper: **2 independently verified conceptual claims and 10 unverified claims**, where unverified includes single-publisher documented/observed facts and does not mean falsified. Cross-publication agreement for the Svipper sample is retained without claiming independent underlying data. Research is complete within these bounds; the open qualification gates remain open. No implementation, V1 edits, database/service actions, merge, push or commit occurred.


