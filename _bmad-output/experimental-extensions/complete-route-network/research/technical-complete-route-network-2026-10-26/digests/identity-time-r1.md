# Identity, operating date, stop occurrence and matching — round 1

Access date: 2026-10-26. Research purpose: determine how a driver-shift activity can be matched to a dated public departure. No feed was downloaded; no endpoint availability or operator-specific mapping was tested.

## Epistemic rules

1. Never conclude from training data alone. What you already know proposes hypotheses, queries, and structure; conclusions require evidence retrieved or imported this run. A claim you cannot evidence is stated as an unverified belief or not at all.
2. The research firewall. Project context shapes what to ask, never what is true. It is inadmissible as evidence: every claim in a research artifact traces to a digest or import file with a source.

## Retrieved evidence

### I1 — Nordic/Norwegian NeTEx timetable profile
URL: https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728760393
Authority: official Entur Håndbok N801, Nordic NeTEx profile document. Page updated 2026-09-23; embedded version label says v1.5, last changed 2022-07-28 (metadata discrepancy; do not silently reconcile).
Evidence: VehicleJourney.PrivateCode is an optional internal planner identifier, with train/trip number as examples. PublicCode is a different optional public identifier, used for journey-level overrides. Passing times reference PointInJourneyPattern. ArrivalDayOffset and DepartureDayOffset are integer offsets relative to the operating date, including previous/next days. A DatedServiceJourney represents a ServiceJourney on one OperatingDay and derives details from a referenced generic journey.
Confidence: high for documented semantics, single normative source. Direct extracted page ended before passing-time and dated sections; those were retrieved in this run through the official page's indexed search result. No claim about actual provider completeness.
Implication/inference: a number imported from a planner is a candidate PrivateCode, not proof of entity-ID equality; preserve its source namespace.

### I2 — Nordic NeTEx data-model explanation
URL: https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728596522
Authority: official Entur conceptual guidance. Updated 2024-06-24; explicitly simplified rather than complete UML.
Evidence: JourneyPattern describes detailed stop/timing points. ServiceJourney supplies passing times and links to DayType. ServiceCalendar links OperatingDay and DayType through DayTypeAssignment. DayType may express weekday patterns; properties describe holidays. Exceptions can make particular operating days unavailable. DatedServiceJourney supplies a persistent dated representation when needed.
Confidence: high for conceptual distinctions; same publisher as I1, therefore corroboration rather than independent confirmation.
Implication/inference: resolving a departure requires calendar expansion/exception handling, not merely selecting a recurring journey ID or matching line/time.

### I3 — Nordic NeTEx network profile
URL: https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728563886/network
Authority: official Entur profile. Publication/update date not captured.
Evidence: JourneyPattern.pointsInSequence is a sorted list; StopPointInJourneyPattern references ScheduledStopPoint and carries boarding/alighting permissions. DestinationDisplayRef belongs to stop occurrences: the minimum is one for a linear route, two for a circular route, and it should change wherever destination text changes.
Confidence: high, one normative source. Detailed rows retrieved through indexed official search content because direct extraction was incomplete.
Implication/inference: retain ordered stop occurrences, not a deduplicated stop set. Destination is not safely one fixed property per line, and a loop cannot be represented by endpoint equality alone.

### I4 — GTFS Schedule reference
URL: https://gtfs.org/documentation/schedule/reference/
Authority: official GTFS reference. Revised 2026-04-27.
Evidence: trip_id identifies a trip; IDs are internal values. service_id selects operating dates; calendar_dates modifies calendar, adding/removing dates. stop_times is keyed by trip_id plus stop_sequence; a stop may occur repeatedly. sequence values increase but need not be consecutive. shape_id describes travel geometry separately. Trip headsign may be overridden per stop_time; direction_id is optional and should not drive routing. Service-day times may exceed 24h. Times use agency_timezone, not stop timezone, and their origin is service-day noon minus twelve hours, with DST relevance.
Confidence: high for GTFS semantics, one normative source. Independently aligns with I1–I3 on recurring/daily identity, ordered calls and separate geometry.
Implication/inference: retain raw service-day seconds/date and timezone, plus derived instants; avoid naive midnight arithmetic on DST days. Namespace GTFS identities to feed provenance/version; this last policy is a design inference, not a promise about Entur IDs.

### I5 — GTFS Realtime reference
URL: https://gtfs.org/documentation/realtime/reference/
Authority: official GTFS-RT reference. Publication/revision date not captured.
Evidence: TripDescriptor resolves one trip instance. Frequency trips require trip_id, start_date and start_time. start_date also disambiguates services lasting over 24 hours or delays colliding with the next day's service. If trip_id is unavailable, route, direction, date and start time are required to identify the instance. stop_sequence distinguishes repeated occurrences. Selectors refer to IDs from the corresponding static feed; realtime can describe cancellations, replacement and new trips.
Confidence: high for specification; single normative source, independently consistent with dated NeTEx identity.
Implication/inference: preserve the original static identity plus date/start and occurrence order as an integration boundary. Do not attach realtime by public line number alone.

### I6 — Norwegian SIRI common components
URL: https://enturas.atlassian.net/wiki/spaces/PUBLIC/pages/637370373/
Authority: official Entur Norwegian SIRI profile, legacy hostname. Search metadata published approximately 2020; exact publication date not captured.
Evidence: FramedVehicleJourneyRef combines a local-date DataFrameRef with DatedVehicleJourneyRef; this journey reference must equal the corresponding NeTEx VehicleJourney ID.
Confidence: high for documented contract; single source and legacy endpoint documentation, requires current-provider verification.
Implication/inference: maintain an explicit adapter/crosswalk for these namespaces, including operating date. A raw imported planner number cannot be substituted.

### I7 — Norwegian SIRI-ET profile
URL: https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370392/SIRI-ET
Authority: official Entur profile. Updated 2026-08-25; embedded profile version v1.1 dated 2022-07-28.
Evidence: SIRI-ET exchanges same-operating-day deviations, linked to planned objects by IDs. It supports a DatedServiceJourney reference or a framed journey/date reference. Replacement departures require a new codespace-unique identifier. JourneyPatternRef can identify the pattern. Cancellation can affect an entire journey or individual calls.
Confidence: high for profile semantics; same publisher as I6, not independent validation of feed behavior.
Implication/inference: distinguish planned identity and current execution state; don't remove a matched planned departure merely because it is cancelled or replaced.

### I8 — Entur Journey Planner
URL: https://developer.entur.no/docs/open-services/journey-planner
Authority: official Entur current developer portal. Last modified 2026-06-08.
Evidence: v3 is a Transmodel-based GraphQL service using OpenTripPlanner, combining national static timetable/stops with realtime. The documented endpoint is POST https://api.entur.io/journey-planner/v3/graphql and requires ET-Client-Name.
Confidence: high for published service description; no live schema or query exercised.
Implication/inference: it can support bounded candidate queries, but this page alone does not establish field-level ID mappings, historical coverage, exhaustive departure enumeration or matching guarantees.

## Decision implications (inferences from I1–I7)

A matching record should preserve imported activity identity and raw number, source/operator namespace, actual operating date, public candidate identity, scheduled timing evidence, ordered stop occurrences and confidence/status. Confirm a mapping using date, scoped line/operator, planned start/end times and stop occurrence pattern. Treat an internal number as supporting evidence until a documented provider crosswalk is obtained. Ambiguous candidates remain ambiguous; do not choose a departure from line plus nearest time alone.

Ordered stop patterns and map geometry serve distinct purposes (I3, I4): use occurrence references and passing times for identity/matching; use geometry for drawing. A short working or partial shift must be checked against the actual journey/pattern and subrange rather than a line-wide union of stops. This is a design inference; no operator short-working sample was inspected.

## Open questions for round 2 / bounded validation

- What exact field and namespace does the source shift's trip number represent, and is a provider-supported crosswalk available? No universal equality has been established.
- Does the selected Entur dataset expose PrivateCode and stable journey IDs through the chosen access path? What happens to them between timetable versions?
- Which timezone/context properties govern NeTEx local times and DST in the chosen feed? GTFS rules are explicit; equivalent NeTEx conversion rules have not yet been evidenced.
- Does Entur's GTFS conversion preserve ServiceJourney IDs verbatim or transform them, and which static feed must accompany its GTFS-RT?
- What are current SIRI-SX/situations selector scopes and exact GraphQL situation association fields? Not yet evidenced; retain space for stop/line/journey/date associations without implementing a join.
- Need bounded examples of loops, repeated stops, partial/short workings, night services and DST transition dates to test actual data semantics.

No unsupported claim is made about historical API coverage, complete network enumeration, operator-number uniqueness or ID permanence across releases.

