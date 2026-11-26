# Identity/time follow-up — round 2

Access date: 2026-10-26. Supplements identity-time-r1.md. No bulk data retrieval and no live API query. Claims below trace to official sources retrieved this run; same-publisher sources are not counted as independent confirmation.

## I9 — NeTEx DST semantics (closes round-1 normative gap)

URL: https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728563782/General%2Binformation%2BNeTEx
Official Entur Nordic profile general information. Publication/update date not captured; direct page extraction includes the section heading but not its full content. Full explanation was retrieved through indexed official-page variants with showComments and preview parameters.

Evidence: passing times for a ServiceJourney use the timezone in effect at noon on its OperatingDay, consistently across the journey, even when actual calls cross a DST change. The operating day need not equal the calendar date. The guidance explicitly distinguishes encoded times from passenger wall-clock times and includes positive and negative day-offset examples.

Confidence: high for the stated noon-reference rule, single normative source; independently aligns with the GTFS noon-minus-twelve-hours rule (I4). It is not evidence that every producer implements the rule correctly. Some complex example rows should be checked against the prose before treating them as executable fixtures.

Design inference: convert service-day values using the operating-day reference axis, then derive passenger-local display times. Preserve original encoded time, offset and operating date. Do not parse each passing time as an independent local wall-clock timestamp in a DST-aware timezone library.

## I10 — NeTEx Locale timezone

URL: https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728727624/framework
Official Nordic NeTEx framework profile. Publication/update date not captured. Retrieved through indexed official page.
Evidence: Locale.TimeZone is mandatory and names the timezone for local time. ServiceCalendarFrame defines days/types and relationships; TimetableFrame describes journeys and calendar references.
Confidence: high for profile contract; one source, same publisher as I9.
Inference: retain inherited Locale context during ingestion; do not hardcode a timezone merely from user location.

## I11 — Current Entur realtime interface and original/mapped IDs

URL: https://developer.entur.no/open-data/realtime
Official current developer portal. Last modified 2026-08-31.
Evidence: SIRI ET/VM/SX and GTFS-RT are offered, with coverage varying by codespace and stream. ET carries estimates, cancellations and changed stop patterns; SX messages associate with departures, lines and stops. Entur states that IDs returned by default are mapped to IDs in static route data; useOriginalId=true requests identifiers from the underlying system. This option is documented for SIRI REST and publish/subscribe/request-response. GTFS-RT is documented separately, refreshed every 15 seconds and filtered by datasource.
Confidence: high for documented API behavior; one source. This does not establish that useOriginalId applies to GTFS-RT or prove a specific NeTEx-to-GTFS trip-ID transformation.
Inference: persist identifier provenance/mapping mode; original-system and Entur/static IDs are distinct integration modes. Select a specific provider and verify its static/RT pair before implementing joins.

## I12 — SIRI-SX affected journey and scope

URL: https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370605/SIRI-SX
Official SIRI-SX profile. Updated 2024-12-02; profile version v1.1 last changed 2021-07-28.
Evidence: situations can affect networks, stop places, stop points or vehicle journeys. AffectedVehicleJourney selects VehicleJourneyRef, DatedVehicleJourneyRef or FramedVehicleJourneyRef; OriginAimedDepartureTime can carry the originally scheduled origin time. These reference planned timetable objects. Validity ranges include required StartTime with optional EndTime.
Confidence: high normative semantics; one source. Current GraphQL projections and actual producer completeness were not tested.
Inference: a situations adapter must preserve selector scope, date/framing, validity and source IDs; attach a journey situation only after resolving the same planned identity.

## I13 — Official dated situation example

URL: https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370806/SIRI%2BSX%2B-%2BMessage%2Bon%2Ba%2Bvehicle
Official example, updated 2019-03-26.
Evidence: examples attach a message to ServiceJourney plus OriginAimedDepartureTime, or to a framed ServiceJourney/date reference. The described result appears in journey suggestions using that dated journey.
Confidence: medium-high; same publisher as I12, practical illustration rather than independent validation. Examples may simplify mandatory fields (the profile explicitly cautions about examples).
Inference: dated scope matters even when the base journey ID recurs.

## I14 — Profile changelog clarifies stale embedded version label

URL: https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728662188
Official changelog. Entry 2026-09-23 identifies timetable v1.6 and adds replacedJourneys for NeTEx 2.0 compatibility. This differs from the timetable page's embedded v1.5 label recorded in round 1.
Confidence: high that the documentation contains inconsistent version labels; single publisher.
Inference: pin a schema/profile revision and validate representative data rather than treating an embedded page label as sufficient compatibility evidence.

## Remaining bounded unknowns

1. No evidence establishes universal equality of source driver-shift trip number, NeTEx entity ID, PrivateCode or GTFS trip_id.
2. No evidence establishes the exact Entur NeTEx-to-GTFS ID crosswalk or historical stability of the selected operator's IDs.
3. Actual source shift operating-day/DST conventions and its treatment of after-midnight activities must be obtained from source documentation or representative imports.
4. A small live set is still needed for repeated stops, short workings, midnight, both DST transitions, cancellations and replacement journeys.
5. GraphQL field availability, complete departure enumeration, archive coverage, and exact situations projection remain outside this evidence.

Decision recommendation (inference from both digests): require a dated, namespaced candidate with ordered-call/timing evidence and explicit ambiguity. Keep the imported identifier separately, record the crosswalk source if established, and make realtime/situations attachment a later adapter using the confirmed planned identity.

