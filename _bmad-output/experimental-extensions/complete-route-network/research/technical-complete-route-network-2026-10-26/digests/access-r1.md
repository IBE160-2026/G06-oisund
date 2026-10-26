# Access research round 1
Accessed 2026-10-26. Primary-source documentation only; no bulk datasets downloaded. Source publication dates are unknown unless stated; dates below are page last-modified dates.

## Epistemics
1. Never conclude from training data alone. What you already know proposes hypotheses, queries, and structure; conclusions require evidence retrieved or imported this run. A claim you cannot evidence is stated as an unverified belief or not at all.
2. The research firewall. Project context shapes what to ask, never what is true. It is inadmissible as evidence: every claim in a research artifact traces to a digest or import file with a source. Distinguish documented support from observations/inference.

## Findings and evidence
[A1] Entur timetable documentation (modified 2026-05-21), https://developer.entur.no/open-data/timetable . NeTEx is Entur's most complete format; downstream GTFS provides a subset and can lose text important to planning. Dumps have permanent URLs; relevant regional and national datasets refresh following provider uploads and nightly re-export. Nightly processing removes expired data beyond a maximum 48 hours in the past. CompositeFrame created records original import/source change timing. Entur expects most users need at most one download daily; excessive downloads can cause IP blocking. Extended/basic GTFS distinction concerns route types. Observed: rendered timetable table remained Loading; exact regional archive URLs and Troms coverage not yet established. No guaranteed future horizon or historical archive documented here.

[A2] Stop Place Data (modified 2026-05-21), https://developer.entur.no/open-data/stops . Daily permanent downloads include Norway current stops (NeTEx/GTFS), Norway current+future and all versions including outdated (NeTEx), regional current NeTEx, and rail stations. Stop identifiers are unique across data sources/datasets. Troms link resolves to https://storage.googleapis.com/marduk-production/tiamat/55_Troms_latest.zip . This is a stop registry dump, not a timetable. Richness depends on source. No assertion of eternal ID stability follows from uniqueness.

[A3] Authentication (modified 2026-09-01), https://developer.entur.no/docs/authentication . All APIs need ET-Client-Name; partner APIs additionally need OAuth2 credentials. This does not establish that public static storage URLs require OAuth2.

[A4] Journey Planner (modified 2026-06-08), https://developer.entur.no/docs/open-services/journey-planner . Open NLOD Transmodel GraphQL endpoint POST https://api.entur.io/journey-planner/v3/graphql requires JSON and ET-Client-Name in company-application format, lowercase without spaces. Service combines national stops/timetables with realtime feeds. Point-to-point output contains Pareto-optimal journey options and filters undesirable alternatives. Inference: accumulating trip-search answers cannot prove exhaustive network/service coverage. Deprecated TariffZone references ceased updating 2025-05-01 in favor of FareZone references. Documentation does not establish bulk extraction completeness or fixed future/past query horizons.

[A5] Rate Limiting (modified 2026-03-30), https://developer.entur.no/docs/open-services/journey-planner/rate-limiting . Identified clients: trip queries 500/minute, spike 150/second; other queries 1000/minute, spike 200/second. HTTP 429 indicates policy violation. Monitor Rate-Limit-* response headers. Quota violations require waiting until Rate-Limit-Expiry-Time; only spike arrest warrants conservative retry. These are distinct request policies, not a guarantee that any single deeply nested query is accepted.

[A6] Terms (modified 2026-09-28), https://developer.entur.no/terms-of-service . Entur states NLOD permits commercial reuse, subject to attribution/exceptions. Attribute Entur, link licence, mark modifications, imply no endorsement. No accuracy/completeness/availability warranty. Stable API breaking changes get notice and at least 12 months parallel old version; beta features can change without that period. This is API compatibility, not a guarantee about data identifiers. No circumvention or invented/random client identities.

[A7] Examples (modified 2026-03-30), https://developer.entur.no/docs/open-services/journey-planner/examples . Official examples cover departure boards, stop lookup, authority filtering and local-bus filtering. This establishes useful focused API checks, not exhaustive route export.

[A8] Official Entur GitHub organization, https://github.com/entur . Observed official links include marduk (timetable import pipeline), damu (NeTEx-to-GTFS conversion) and nordic-netex-documentation. Repository dates are not documentation publication dates. No implementation conclusions drawn yet.

## Provisional decision (inference)
Use a regional NeTEx snapshot as canonical planned-service input, plus stop registry versions appropriate to timetable validity, if Troms archive coverage is confirmed. Use GraphQL for targeted inspection, current passenger-facing answers, and reconciliation; do not call trip results a route inventory. GTFS is an easier optional projection only if its losses meet requirements. Preserve dated local snapshots, hashes, source timestamps, parser/schema version and provenance before filtering into the pilot; live exports trim history and mutable endpoints cannot reproduce prior snapshots.

## Unverified issues
Exact timetable download granularity/URLs, Troms provider/codespace and city-bus boundary; actual current validity horizon; line/journey/stop ID drift guarantees; API nested-query or result-size limits; current download metadata. No raw archive downloaded. A shell HTTPS request failed DNS; browser-independent web retrieval succeeded. No endpoint availability conclusion follows from that local failure.

