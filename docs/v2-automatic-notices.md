# V2 automatic notices

The confirmed workday exposes Entur TRO SIRI-SX passenger information as possible relevance. It uses the exact public line and authority bindings `TRO:Line:1_20` and `TRO:Line:1_24` under `TRO:Authority:1` for 23–24 November 2026. The projection uses planned Oslo instants and half-open validity windows. Stop, direction, journey and other unqualified scope remains visible for review. The meaning of each workday choice stays private.

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

- The earlier provider check recorded five and four records from consecutive pages, with matching continuity echoes and an identical union from the independent large-page control. The current pilot bindings are limited to two checked dates. [V2 handoff](v2-handoff.md).
- The V2 owner smoke first found that Entur places the request UUID echo and literal continuation flag directly on `ServiceDelivery`. A bounded public check confirmed both fields and the matching HTTP echoes. After the parser correction, the owner sandbox promoted a complete live TRO baseline. The parser rejects duplicate or conflicting values across the delivery levels.
- The controlled test inputs cover parser failures, timeout, throttling, partial/restart behavior, rare close/version cases, and two dated workday examples. The tests use PostgreSQL timestamps to check persisted reservations and page spacing under controlled transport. Browser cases use the real private API and stored synthetic source data to check reply recovery, proposal comparison and preservation of the manual editor and selected activity.
- Ongoing provider behavior, a licensed-retention acceptance decision, paired manual Svipper checks where counterparts exist, a dated pilot-stop crosswalk, and the owner's review-workload walkthrough remain pilot acceptance items. Stop-only notices remain available with a review reason pending a qualified stop binding.
