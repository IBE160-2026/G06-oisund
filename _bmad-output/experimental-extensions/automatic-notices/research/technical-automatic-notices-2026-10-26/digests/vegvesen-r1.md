# Vegvesen evidence digest — round 1

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Research/access date: 2026-10-26. Primary official sources only. No repository/project files used as research evidence. Two bounded search rounds; ten web calls plus one unsuccessful shell fetch. No credentials requested or used.

## Documented findings

- The official overview describes a free DATEX II 3.1 XML pull service, nationally covering ongoing and planned conditions affecting public roads: roadwork, closures, accidents, severe weather, landslide and flooding. It says information is received, verified and distributed continuously, while timing, position and content accuracy are stated as well as possible. This is not a quantified freshness/completeness SLA. Attribution to Statens vegvesen is requested. Registration is required. [S1]
- The traffic-message catalog identifies the production XML endpoint and NLOD license. The more general DATEX catalog also surfaced a different api.vegvesen.no hostname/JSON description; that is insufficient evidence to replace the specific GetSituation endpoint without checking with the provider. [S2]
- Provider documentation retrieved through its indexed official README diff says pull services publish all active situations, HTTP GET returns XML, and Basic Authentication uses a provider-issued username/password per registered client. Conditional GET can use If-Modified-Since; a changed response contains available data, unchanged data yields HTTP304; Last-Modified follows publicationTime. This is a historical diff, not a verified current contract. [S3]
- Indexed provider WFS documentation describes polygon and attribute CQL filtering (including combined filters). Situation and situationRecord have unique IDs; the example record includes version. Documented example fields include situationId, situationType, secondaryTypes, severity, probability, description, roadNumber, locationDescription, display longitude, startJsonTime, endTime, confidentiality and isMainRecord. activePeriodAtLastUpdate is documented counterintuitively as active=0/inactive=1: verify against actual payloads before implementation. It describes expiry when an end time has passed and indefinite validity without an end time. Some inline field names are lost in search extraction. [S4]
- The DATEX II 3.1 standard describes stable record identity with changing version, validity status (active/suspended/time-period-based), mandatory overallStartTime, optional overallEndTime, validity/exception periods and overrunning. A forecast start time arriving does not itself prove an event occurred. These are standard capabilities, not confirmation of fields populated by the Norwegian profile. [S5]
- NLOD's official summary permits copying, modification, combinations and commercial use; attribution must not imply endorsement, and use must not mislead or distort. It also states the licensor disclaims responsibility for quality/use. This is a summary, not a legal review of the full license. [S6]

## Actual observations and limits

- The documented GetSituation snapshot endpoint returned **HTTP401 Unauthorized** without credentials on this run. No current Tromsø incident, complete snapshot, current cancellation example, feed update cadence or line-linked event was obtained. HTTP401 is an access result, not an empty-feed result. [S7]
- The public repository lists a roadTrafficInformation/situations.xml sample of 29.09 MB. Its raw contents could not be fetched by the web tool; shell fetch also failed DNS. File existence/size alone is not evidence for payload semantics. [S8]
- Current README pages rendered only their Bitbucket chrome; indexed official diffs/search content supplied the details above. Historical documentation and general standard details must be revalidated against authenticated current feed/schema.

## Pilot implications — inferences, not source guarantees

Use this as a candidate road-condition signal for a small Tromsø bus pilot, with attribution and reviewable provenance. Geographic proximity/road intersection can nominate potentially affected routes; it cannot establish that a transit line or departure is disrupted. None of the retrieved provider evidence promises transit line identifiers or guaranteed bus relevance. The standard itself can represent transit information, which does not establish Norwegian-feed population of it.

Persist source IDs/versions, publication/retrieval times, validity periods, geography and raw source text. Deduplicate by provider identity and version, preserving audit history. Evaluate direction/road geometry against a known route path rather than city-name matching alone. These are implementation proposals requiring validation.

Cancellation remains a critical evidence gap: no retrieved current NPRA contract establishes tombstone flags, disappearance semantics, explicit cancellation versus expiry, or whether a filtered result disappearing means cancellation. Do not turn HTTP errors, stale snapshots or filter exits into resolved notices. Before automatic publication, obtain credentials and schema, bounded Tromsø examples, update/end/cancel sequences, and provider guidance on polling/rate limits, snapshot completeness, time zones and filter semantics.

## Sources (all accessed 2026-10-26)

S1. [Statens vegvesen — DATEX trafikkinformasjon](https://www.vegvesen.no/fag/teknologi/apne-data/et-utvalg-apne-data/hva-er-datex/). Publication/update date not stated. Full overview read. Short excerpt: “Tjenesten er gratis å bruke.”

S2. [Statens vegvesen Dataportalen — Trafikkmeldinger API](https://dataut.vegvesen.no/nb/dataservice/trafikkmeldinger-api). Publication/update date not stated; official catalog search content retrieved. Excerpt: “Man må bestille tilgang”.

S3. [Provider README diff, commit ab928698d6126eeed283fec2a57c460cbcc74aaf](https://git.vegvesen.no/projects/DATEX2/repos/datex2-spesifications/diff/3.1/README.md?at=ab928698d61&autoSincePath=false&until=ab928698d6126eeed283fec2a57c460cbcc74aaf). Commit publication date not established. Official indexed diff content retrieved. Excerpt: “HTTP Get returns data in XML.”

S4. [Provider WFS/WMS documentation, pinned b4fb01bc0333bc46269f4f96d39954ac72118e51](https://git.vegvesen.no/projects/DATEX2/repos/datex2-spesifications/browse/3.1/wfs-wms?at=b4fb01bc0333bc46269f4f96d39954ac72118e51). Publication date not established; search index says published approximately 1.1 years ago. Detailed indexed provider text retrieved; direct open yielded directory only. Excerpt: “Each situation has a unique id”.

S5. [DATEX II official 3.1 user documentation — Situation and SituationPublication](https://docs.datex2.eu/v3.1/level2user/situationPublication.html). Publication/update date not stated. Full page read. Excerpt: “Each situation record has a unique versioned identifier.”

S6. [Digitaliseringsdirektoratet/data.norge.no — NLOD summary](https://data.norge.no/nlod/no). Page updated 2023-03-07. Full summary read. Excerpt: “å benytte datasettet kommersielt”.

S7. [Production GetSituation snapshot endpoint](https://datex-server-get-v3-1.atlas.vegvesen.no/datexapi/GetSituation/pullsnapshotdata). Live probe 2026-10-26: HTTP401. Publication date not applicable. No event payload.

S8. [Provider public roadTrafficInformation sample directory](https://git.vegvesen.no/projects/DATEX2/repos/datex2-spesifications/browse/3.1/samples/roadTrafficInformation). Publication/update date not stated. Directory read; situations.xml 29.09 MB listed; sample content unavailable.
