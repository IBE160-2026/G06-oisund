# V2 automatic notices

The confirmed workday exposes Entur TRO SIRI-SX passenger information as possible relevance. It uses exact public line and authority bindings `TRO:Line:1_20` and `TRO:Line:1_24` under `TRO:Authority:1` for 23–29 November 2026. The projection uses planned Oslo instants and half-open validity windows. Stop, direction, journey and other unqualified scope remains visible for review. The meaning of each workday choice stays private.

## Collection and retention

The local V2 owner launcher enables the provider task. It uses the fixed TRO endpoint, one fresh UUID per complete collection and a page size of five. Only the fixed dataset, page size, continuity UUID and application identification go to Entur. The test launcher keeps live collection disabled.

| Limit | Value |
| --- | --- |
| Requests | At most four per rolling minute across writers and retries. PostgreSQL holds one advisory writer lock and stores a 25.1-second reservation before each request. A reply or timeout leaves a 15.1-second interval. A longer provider retry interval takes precedence. |
| Cycle | Maximum 12 pages and 210 seconds, five-minute refresh target |
| HTTP GET | 10 seconds, redirects disabled, plain XML only, no compressed response bodies |
| XML | 512 KiB per page, 32 levels, 5,000 elements, no DTD or external entities |
| Normalized data | Five items per page, 64 KiB per item, 16,384 characters per text field, 2,048 per source URL |
| Freshness | Old after 15 minutes since last complete synchronization, independently of an attempt failure |
| History | Seven days for unreferenced superseded or not-seen source records. Private review records and receipts inherit the workday deadline and cascade on shortening or removal. |

Complete promotion requires matching dataset and continuity echoes, distinct identities across usable pages and literal terminal `MoreData=false`. An incomplete attempt preserves the last complete generation and can add separately qualified observations. An explicit newer source close affects only its own source contribution. Disappearance, unknown observation, old data and expired validity remain distinct from closure. [Entur real-time API](https://developer.entur.no/open-data/realtime).

An observation of an older or conflicting revision updates the membership of its identity. The exact revision keeps its own observation clocks and generation. Migration 020 retains existing identity membership and removes prior generation labels that cannot identify a single observed revision. The stored receipt remains available for exact replay. A private proposal keeps the source and workday basis from the displayed version. After a change, the driver can explicitly compare the new information or start a fresh proposal.

Source text is normalized for presentation. Line and time relevance are local interpretations. The passenger information is provided by Entur AS under NLOD 2.0. Private decisions never send data to the provider. [Entur terms](https://developer.entur.no/terms-of-service), [NLOD 2.0](https://data.norge.no/nlod/no/2.0).

## Qualification boundaries

- The earlier provider check recorded five and four records from consecutive pages, with matching continuity echoes and an identical union from the independent large-page control. The original two-date binding has been extended to the seven exact pilot dates. The planned evaluation still uses two representative workdays. [V2 handoff](v2-handoff.md).
- The V2 owner smoke first found that Entur places the request UUID echo and literal continuation flag directly on `ServiceDelivery`. A bounded public check confirmed both fields and the matching HTTP echoes. After the parser correction, the owner sandbox promoted a complete live TRO baseline. The parser rejects duplicate or conflicting values across the delivery levels.
- The controlled test inputs cover parser failures, timeout, throttling, partial/restart behavior, rare close/version cases, and two dated workday examples. The tests use PostgreSQL timestamps to check persisted reservations and page spacing under controlled transport. Browser cases use the real private API and stored synthetic source data to check reply recovery, proposal comparison and preservation of the manual editor and selected activity.
- Ongoing provider behavior, a licensed-retention acceptance decision, paired manual Svipper checks where counterparts exist, and the owner's review-workload walkthrough remain pilot acceptance items. The Giæverbukta review group has the dated scope below. Other stop bindings remain available in general review.

## Pilot-week line provenance

The retained public Troms NeTEx archive has generation `1795129398375617` and SHA-256 `03662d51c1438514d1695e632c598a7ea589d5384a19804658212fc4af0af8b9`. Both exact `Line` objects have version `1947`, `TransportMode=bus`, their literal `PublicCode` and an explicit reference to `TRO:GroupOfLines:bus_1`. The shared data places that group in `TRO:Network:1` version `1947`, whose versioned `AuthorityRef` resolves to `TRO:Authority:1` version `1947` (Svipper). Each line and the shared member explicitly cover every pilot date. The bounded local calendar check resolves service-day assignments and counted the following scheduled journeys. [Entur timetable data](https://developer.entur.no/open-data/timetable).

| Printed line | Calendar counts for 23–29 November | Archive member and SHA-256 |
| --- | --- | --- |
| 20 | 136, 136, 136, 136, 143, 109, 64 | `TRO_TRO-Line-1_20_20_Skattora---sentrum---Kroken.xml`, `750aab1bb7eefe6bf3e1a7fe3910eb79d2ce43d9e20764f2ed3757072fcdc5a4` |
| 24 | 139, 139, 139, 139, 145, 80, 64 | `TRO_TRO-Line-1_24_24_Skognesvegen---Gieverbukta---sentrum---Skjelnan.xml`, `7a569eff194a5bb0a5cb33f2b48ed903eade59d29eeea7d43e65034709be3d96` |

To repeat the offline check, verify the ZIP and member hashes and load the three members with `app.route_source.xml_member`. Trace each line's `RepresentedByGroupRef` through the shared `Network` to its versioned `AuthorityRef`. Check the line and shared `AvailabilityCondition` against the seven dates. Gather the `dayTypes/DayTypeRef` values for each unique `ServiceJourney`, resolve them with `app.route_source.assigned_dates`, and count the union of each journey's active dates once per journey and date. Every referenced day type resolved in these two members. The `_TRO_shared_data.xml` SHA-256 is `9df3cef4eb4c8465130c20b076805b27a357bc2cc3e46a633143e676db1aeea0`.

This evidence qualifies the two exact printed line and authority bindings. Date matching is based on the Oslo calendar portion of an activity, including when it crosses midnight. If an otherwise eligible open notice overlaps only the 30 November portion of a plan, it stays in review. The line 24 count is evidence for notices only. [The separate line 20 route pilot](v2-route-p1.md).

## Dated Giæverbukta stop review

The retained NSR Troms archive, generation `1795125615869698` and SHA-256 `2c224106067c28de88b6e67e04d3a33c527ae629ee6b3103dcb309e430d8427a`, identifies Giæverbukta bussterminal as `NSR:StopPlace:55902` version 8. The pinned timetable's unique passenger assignments map `TRO:ScheduledStopPoint:19021442_2` to `NSR:Quay:95718` and `TRO:ScheduledStopPoint:19021442_4` to `NSR:Quay:95713`. Both Quays are children of the exact StopPlace in the registry extract. [Entur stop registry data](https://developer.entur.no/open-data/stops) · [Entur timetable data](https://developer.entur.no/open-data/timetable).

From 23 to 29 November, the numbers of dated line 24 journeys calling at either Quay are 139, 139, 139, 139, 144, 79 and 64. Seven active patterns call there. Both Quays have a local daytime departure with zero departure-day offset on each date. On 23 November, for example, `TRO:ServiceJourney:24_260928072285459_1103` leaves Quay 95713 at 16:14 and `TRO:ServiceJourney:24_260918105894529_1016` leaves Quay 95718 at 07:43. The retained line 20 pilot includes none of the StopPlace's Quays. Some line 24 journeys omit the stop, so the reviewed scope is a planned-line context. The offline archive test verifies exact identities, unique passenger assignments and calendar witnesses for both Quays on every pilot day.

The group **Pilotstopp til gjennomgang** covers open SIRI-SX messages with the observed sole `StopPoints/AffectedStopPoint/StopPointRef` selector containing `NSR:StopPlace:55902`. The scope must have a positively verified SIRI namespace and the observed attribute-free form. At least one valid source interval must overlap planned line 24 time on a qualified Oslo calendar date. The group provides review context and leaves activity matches empty. Additional selectors, platform-specific references and unreadable dates stay under the ordinary scope rules. The API retains the `review` classification and counts, with an optional field for the subgroup. The browser counts the entries it displays in each subgroup. [Entur SIRI-SX source description](https://developer.entur.no/open-data/realtime).

Earlier stored observations lack namespace evidence and stay in ordinary review. Re-observing the normalized content can verify or remove the local namespace evidence while preserving the publisher revision. For this exact selector shape, a change in that evidence changes the basis of a private review and preserves the earlier decision for comparison. Historical situation `TRO:SituationNumber:426`, which supplied the selector shape, was valid on 26–30 October. The November classifier and API verification therefore use controlled notices. [Svipper's October platform notice](https://svipper.no/nyheter/stengte-plattformer-pa-giaverbukta-terminal-fra-mandag-26-oktober.6992.aspx).
