# Bounded live observations and verification

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Accessed 2026-10-26, root researcher. Primary service: POST https://api.entur.io/journey-planner/v3/graphql, ET-Client-Name ibe160-complete-route-network-research. Exact query/status/response headers/body saved as imports/api-*.json; query files retained. No product endpoints or private data were queried. Eleven GraphQL requests were made, including discovery and one rejected schema query; no retries of identical queries, no trip-search query, no national export. The one-line template response was bounded at 1.5MB and was 918898 bytes including metadata. All numeric observations below can be regenerated from summarize-observations.py without network access.

## Observed facts (single publisher, not independently verified completeness)

- Authority TRO:Authority:1 is Svipper. Public pilot line IDs returned: TRO:Line:1_20, TRO:Line:1_24, TRO:Line:1_42. Names match the local place vocabulary; no complete line manifest was requested.
- datedServiceJourneys for lines20/42 on 2026-10-26 returned an empty list. In contrast line20.serviceJourneys returned 799 templates, 136 active on that date. Thus an empty datedServiceJourneys query must not be interpreted as absence of static service. Exact underlying reason was not verified.
- Those 136 templates group by direction/endpoints into 68 inbound Malmvegen→Skattøra, 67 outbound reverse, and one outbound Skattøra→Steinnes. Counts are observed response contents, not independently certified complete service.
- Dates present across the returned line20 templates span 2026-10-19 through 2027-02-28. This is observed min/max, not continuous all-lines coverage or a promised API horizon.
- Four sampled journeys expose privateCode, distinct full ServiceJourney and JourneyPattern IDs, ordered calls with positions 0..N, scheduled NSR quay and parent StopPlace IDs, per-call destinationDisplay, date, aimed arrival/departure, cancellation and realtime flags. No repeated quay IDs occurred within these four samples; loop handling is normative, not empirically qualified here.

| Sample | Identity suffix/privateCode | Operating date | Scheduled calendar times | Ordered calls | Finding |
|---|---|---|---|---|---|
| Ordinary outbound | 20_260918104872543_1009 / 1009 | 2026-10-26 | 06:35–07:25 +01 | 42 | Skattøra→Malmvegen; Kroken via sentrum→Kroken display. |
| Ordinary inbound | 20_260918105148184_1000 / 1000 | 2026-10-26 | 05:16–06:09 +01 | 43 | Malmvegen→Skattøra; displays Stakkevollan via sentrum, via UNN, then Stakkevollan. |
| Extended destination | 20_260918104886042_1133 / 1133 | 2026-10-26 | 23:03→2026-10-27 00:21 +01 | 79 | Skattøra→Steinnes, changing headsign. realtime=true on returned calls does not establish observed physical position; only aimed times used. |
| Short-origin night | 20_260918105162575_6600 / 6600 | 2026-10-31 | 2026-11-01 01:30–01:50 +01 | 25 | Fr. Langes gate→Skattøra; raw departure.time=01:30:00, dayOffset=1. |

The night journey on operating date 2026-10-24 yields calendar 2026-10-25 01:30 +02. It returns zero estimatedCalls for non-active operating date 2026-10-26. These checks cover midnight and pre-transition DST offset, not both occurrences in the repeated autumn hour, spring gaps or all producer encodings.

Independent local control: Svipper PDF20 weekday row Malmvegen 05:16→Skattøra 06:09 agrees with the sampled API inbound aimed times/endpoints. This verifies one passenger-facing timetable case, not all intermediate stops, publication lag, operator internal numbering or all future dates. Local night columns were not visually qualified and are not exact acceptance fixtures.

## Access/update observations

Live GET https://api.entur.io/timetable-public/v1/timetable-import-info/import_date/TRO returned 2026-10-23T12:01:39. This source timestamp has no offset in the body; do not invent its timezone. Exact status/headers/body in imports/import-info-TRO.json.

Official deployed TimetableTable component constructs public Troms URLs. HEAD only (no archive body):
- https://storage.googleapis.com/marduk-production/outbound/netex/rb_tro-aggregated-netex.zip :200, 7718133 bytes, Last-Modified 2026-10-25T23:27:17Z, generation1792970837742987.
- https://storage.googleapis.com/marduk-production/outbound/gtfs/rb_tro-aggregated-gtfs.zip :200, 14346274 bytes, Last-Modified 2026-10-25T23:27:55Z, generation1792970875012487.

Do not treat modification as new provider planning input. HEAD proves reachable objects/metadata, not parsed validity or contents. In this sample GTFS archive is larger; no general size/performance conclusion follows. No regional timetable or stop archive was downloaded.

## Failures and limits

One query containing two __type fields was rejected as BadFaithIntrospection with HTTP200; a single-type follow-up succeeded. Consumers must inspect GraphQL errors as well as HTTP. Local PowerShell JSON projection initially rejected differently cased header keys; -AsHashtable fixed local reading without refetch. Exact rejected response is retained. The live headers reported a quota window unlike the documentation's per-minute presentation; future clients must honor actual response headers and 429 policy rather than hardcode observed quotas.

## Project context only (not external evidence)

Read relevant sections of Eksempelfiler/README.md to understand available matching inputs. It describes anonymized fixtures dated2030, identifiers formatted line/trip, separate vehicle duty and non-passenger activities; it is explicitly not a complete intermediate-stop oracle. Those dates cannot validate current2026 public departures. No real source shift or provider-approved internal-number crosswalk was obtained; no claim that privateCode equals shift trip number is supported.

## Stop condition

Documentation and bounded samples answer feasible access/model choices. Remaining work needs a scoped regional import and independent shift mapping oracle, outside this research run's data limits. No point-to-point planner result, geometry, realtime position, network completeness or cross-version stability claim is made.
