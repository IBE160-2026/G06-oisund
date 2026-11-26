# Standards spot-check

> EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE

Publisher: GTFS specification / MobilityData. Source https://gtfs.org/documentation/realtime/reference/ . Publication date not stated; accessed 2026-10-26 using web open/find. Evidence class: documented schema, not TRO feed observation. Confidence medium, no independent deployment confirmation.

The GTFS-RT reference defines feed-unique entity ID, FULL_DATASET replacement and optional alert periods and selectors. A disappeared entity in a verified full snapshot is absent from current feed state; this does not establish a real-world incident has ended. DIFFERENTIAL behavior is currently unspecified. Alert selectors may constrain route, stop or trip; omitted details do not justify invented precision. This is a comparator only: it does not establish TRO GTFS alerts availability. Key limitation: standard capability does not prove producer field population.

Entur official realtime documentation https://developer.entur.no/open-data/realtime accessed 2026-10-26 independently by lead: TRO row has SIRI SX marked, GTFS-RT Service Alerts blank. SIRI Lite documents full data without requestorId, delta session with requestorId, paging/MoreData/maxSize and 4 GET requests/minute. The official page describes SX as end-user messages. This is provider documentation, not independent coverage evidence. Detailed live sample belongs to entur-r1.md.

Verification result: generic schema corroborates the need for explicit feed mode and selector handling; it does not independently verify Entur-specific coverage, licence, update latency or closure semantics. Keep those load-bearing claims single-publisher/unverified in the BMAD ledger. No performance benchmarks or version compatibility promises made.
