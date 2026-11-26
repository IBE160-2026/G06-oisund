# Entur realtime situations — round 1

EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE

Research date/access date: 2026-10-26. Only retrieved official documentation and an actual bounded API response are evidence here; no project files were used as evidence. Publication dates below are page modification dates where available.

## Decision

Prefer a read-only SIRI-SX pilot for Tromsø passenger notices. Official documentation lists TRO coverage for SIRI-SX; the TRO GTFS-RT Service Alerts cell is blank. Actual TRO SX messages were retrieved today, including a Svipper-linked Giæverbukta platform change and Tromsdalen stop changes. This verifies examples, not feed completeness, notification latency, or every Troms service. Confidence: high for these observations; unknown for comprehensive coverage.

## Retrieved sources

| ID | Publisher and URL | Publication/modification | Access |
|---|---|---|---|
| E1 | Entur, https://developer.entur.no/open-data/realtime | 2026-08-31 | 2026-10-26 |
| E2 | Entur, https://developer.entur.no/docs/getting-started | 2026-10-21 | 2026-10-26 |
| E3 | Entur, https://developer.entur.no/terms-of-service | 2026-09-28 | 2026-10-26 |
| E4 | Entur, https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370605/SIRI-SX | Page updated 2024-12-02; states profile v1.1 last changed 2021-07-28 | 2026-10-26 |
| E5 | Entur, https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370694/SIRI-SX+-+Validity+of+a+message | 2019-03-19 | 2026-10-26 |
| E6 | GTFS specification / MobilityData, https://gtfs.org/documentation/realtime/reference/ | Not stated in retrieved page | 2026-10-26 |
| E7 | Entur, https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370420/Norwegian+SIRI+profile | 2022-05-30 | 2026-10-26 |
| E8 | Entur API, https://api.entur.io/realtime/v1/rest/sx?datasetId=TRO&maxSize=3 | Actual response 2026-10-26T08:47:15Z | 2026-10-26 |

## Access and ingestion contract

E1: SIRI Lite supports GET /realtime/v1/rest/sx with datasetId=TRO. No requestorId gives full data; a stable unique UUID tracks changes, with short-lived sessions (example timeout five minutes). maxSize bounds pages, defaults to 1500 and creates/returns a requestor session; MoreData signals more pages. Documented limit is four requests per minute. ID mapping defaults to static-route identifiers; useOriginalId changes that. GTFS-RT GET /realtime/v1/gtfs-rt/alerts?datasource=TRO is the documented filtered form, but TRO alerts support is not claimed by its matrix. GTFS datasets are full snapshots refreshed every 15 seconds. SX is passenger-facing text; ET supplies estimates, cancellations and stop-pattern changes, VM positions/deviation. These streams do not supply base timetable data. Confidence: high documentation; no actual ET/VM/GTFS call made.

E2/E3: Application identification is required in ET-Client-Name using company-application, lowercase/no spaces. Open services require no OAuth/partnership; partner services do. The request used ibe160-automatic-notices-research as an honest task/application identifier, not an impersonated operator. Terms prohibit fabricated/random identifiers and limit evasion. Open data uses NLOD with attribution to Entur, licence link and modification disclosure, without implied endorsement. Data accuracy/completeness/availability are not warranted. Confidence: high documentation. No separate archival retention or local database caching policy was established.

## Actual bounded payload (E8), distinct from schema

A single read-only GET with maxSize=3 returned HTTP 200, application/xml, datasetid=TRO and MoreData=true. It is an incomplete page, not a complete snapshot. No subscription or other external mutation was performed. Network DNS failed in restricted shell; an approved narrowly scoped read-only network escalation succeeded.

ResponseTimestamp was 2026-10-26T09:47:15.6389651+01:00. All three messages had ParticipantRef=TRO, CreationTime, SituationNumber, SourceType, Progress=open, StartTime, severity normal, ReportType general, Summary, Description and Affects. None had Version or VersionedAtTime. Thus do not require those optional fields or use CreationTime as update timestamp.

| Actual situation ID | Observed scope and timing | Other observations |
|---|---|---|
| TRO:SituationNumber:426 | NSR:StopPlace:55902; validity 2026-10-26T04:45:22.805+01:00 to 2026-10-30T03:00:00+01:00 | Giæverbukta platform relocation; InfoLink URI https://svipper.no/nyheter/stengte-plattformer-pa-giaverbukta-terminal-fra-mandag-26-oktober.6992.aspx ; xml:lang NO |
| TRO:SituationNumber:TX1063335 | TRO:Network:1, TRO:Line:1_191; open-ended from 2026-10-23 | Replacement ferry/capacity notice; Language en despite Norwegian prose |
| TRO:SituationNumber:TX1062813 | Lines TRO:Line:1_20, 1_24 and 1_450; nested AffectedRoute/AffectedOnly=true with NSR:Quay:96986 and NSR:Quay:88834; open-ended from 2026-08-17 | Tromsdalen church/Otium roadwork stop changes; Language en despite Norwegian prose |

No direction or dated-journey selector was present in this page. Do not infer absent fields are unsupported. StopPointRef carried both StopPlace and Quay identifier types: inspect identifier type instead of assuming field name determines stop granularity. No public phone number from the response was retained here.

Observed HTTP Cache-Control: no-store, must-revalidate, no-cache, max-age=0; Pragma no-cache; Expires 0. HTTP intermediaries must respect these; this is not evidence of a blanket prohibition on application state needed for reconciliation. Rate headers reported allowed=5 and available=4 per-minute, differing from documented four/minute: retain the stricter documented cadence. Confidence: high actual observation, one time only. No ETag or Last-Modified was observed.

## SX schema and lifecycle, not verified TRO fields (E4/E5)

The profile defines SituationNumber with source codespace, CreationTime, optional Version and VersionedAtTime, Progress open/closed, one or more validity periods, Summary/Description/Advice, optional InfoLinks/InfoLink/Uri, and affected networks/stops/journeys. Publication ResponseTimestamp describes the response/dataset; it is distinct from creation and optional update time. Open validity can omit EndTime. Closed messages must be hidden immediately and retained in the distribution stream until their EndTime, at least five hours in the future; after expiry redistribution stops. Thus closure and disappearance are different lifecycle signals. No deletion event was observed. Affects may target lines, stops, or trips; SX does not prove internal dispatch/driver instructions exist. The profile distinguishes general information from incidents, but actual stop-disruption sample used general: do not filter operational relevance solely by ReportType. Confidence: high profile; actual closure handling untested. E7 identifies the profile and examples; those are illustrative rather than coverage evidence.

## GTFS comparison (E6), specification only

Alert supports active periods, affected entities, URL, translated header/body and optional severity/cause/effect. Feed header has creation timestamp and incrementality; FULL_DATASET replaces previous state. is_deleted is for DIFFERENTIAL, which the reference describes as unsupported/unspecified. Entity IDs are feed-unique; affected selectors must separately identify their targets and resolve against a static GTFS feed. No GTFS payload was fetched and no conversion parity with SX was established. Confidence: high schema, unknown TRO availability.

## Pilot consequences and open gates (engineering inference)

- Key by provider plus SituationNumber; preserve source fields and hash normalized content when update version/time is absent. Deduplicate repeated observations rather than treating response timestamp as a notice edit.
- Maintain validity and closed-state rules; a missed poll, session expiry, error or incomplete page must not become an all-clear. Recover with a complete baseline and finish MoreData pages before reconciling absence. The exact requestor session return location was not found in this bounded response; verify before relying on delta paging.
- Keep notices as passenger information with source URL where supplied. Do not claim coverage of driver rostering, dispatch, internal incidents, guaranteed all-clear or operational authority.
- Resolve line and stop identifiers against static data before deterministic route/direction matching. Direction and dated-journey field forms still need schema/example retrieval plus live examples. Avoid assuming public line number equals canonical LineRef.
- Confirm feed coverage/completeness with operator/Entur, closure examples, maximum permitted polling/paging traffic, freshness thresholds, session-recovery behavior, and how long a missing item should stay stale before suppression. A single live sample cannot settle these.

## Round 2 — selector evidence and remaining limit

Additional official sources accessed 2026-10-26:

| ID | Publisher and URL | Modification date |
|---|---|---|
| E9 | Entur, https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370744/SIRI-SX+-+Message+on+a+Line | 2019-03-22 |
| E10 | Entur, https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370814/SIRI+SX+-+Message+on+multiple+vehicles+on+multiple+dates | 2019-03-26 |
| E11 | Entur, https://raw.githubusercontent.com/entur/profile-examples/master/siri/siri-sx-outline.xml | Not stated; retrieved successfully via shell after web cache miss |

E9 illustrates a line-specific message being selected only when the relevant line serves the searched journey. E10 gives two dated-journey selector forms: AffectedVehicleJourney/VehicleJourneyRef plus OriginAimedDepartureTime, or AffectedVehicleJourney/FramedVehicleJourneyRef with DataFrameRef and DatedVehicleJourneyRef. These are example-schema evidence only, with railway examples; neither form appeared in the actual three TRO messages. E11 is a minimal delivery envelope and gives no direction-selector evidence. Confidence: high examples, unknown use in Troms.

E6 additionally specifies that EntitySelector fields within one selector are ANDed; separate informed_entity selectors can express alternatives. Selectors include agency_id, route_id, route_type, direction_id, trip and stop_id. direction_id requires route_id and is marked experimental in the retrieved reference; trip references need a uniquely resolved instance. GTFS schema direction support is therefore established, but Troms GTFS-alert delivery remains unverified. SIRI direction selector field and TRO usage remain unresolved; do not invent or promise a direct direction mapping.

Research boundary: two rounds completed. No second live poll, page draining, GTFS sample, subscription creation or authenticated partner-service access was attempted. No implementation was changed. Findings support a separately approved experiment, not incorporation into approved V1.
