# Source feasibility — PRD discovery

Research date: 2026-09-21. Documentation research only: no production feed, route dataset, device or integration was tested. This note establishes candidates and unknowns; it does not select architecture or a technology stack.

## Automatic disruptions

Svipper publishes a public traffic-message page for changes and delays in Troms. Its text rendering in this research did not expose individual messages or a documented Svipper API. This is not evidence that messages or a feed are absent. [Svipper traffic messages](https://svipper.no/meny/reise/trafikkmeldinger/trafikkmeldinger/).

Entur's current open-data documentation lists Troms under codespace TRO with SIRI SX, ET and VM support. TRO's GTFS-RT Service Alerts cell is blank, so equivalent disruption coverage across formats must not be assumed. SIRI SX carries textual messages associated with departures, lines or stops. The documented SIRI Lite SX endpoint supports a dataset-provider filter and is limited to four requests per minute. A two-minute refresh target is below this documented request-frequency limit, but this says nothing about source publication delay or actual coverage. [Entur real-time data, updated 2026-08-31](https://developer.entur.no/open-data/realtime).

Entur requires an identifying ET-Client-Name header on open and partner APIs; missing identification can cause rate limiting or blocking. Its partner authoring services must not be confused with reading open data. [Getting started](https://developer.entur.no/docs/getting-started).

**PRD implication:** automatic Svipper-origin disruption retrieval has a documented candidate via Entur, but remains an unverified delivery dependency. Before pilot acceptance, establish correspondence with Svipper's published notices for the four lines, coverage of planned changes, validity times, updates and withdrawn/ended notices. Do not claim complete coverage, a tested integration, or a direct public Svipper API. No source-specific availability guarantee was established here.

## Scheduled stops and journeys

Svipper identifies lines 20, 24, 28 and 42 as Tromsø/Tide routes. [Official route overview](https://svipper.no/menu/help-and-contact/lost-property/route-overview/).

Entur documents downloadable timetable and stop datasets in NeTEx and GTFS, under NLOD, with updates after provider uploads and nightly processing. It warns that excessive downloading can result in blocking and expects most consumers to need at most one download per 24 hours. Data richness depends on the originating provider. This page remains on the old portal; the new portal explicitly retains that portal while migration is incomplete. [Timetable documentation](https://developer.entur.org/stops-and-timetable-data/), [portal migration notice](https://developer.entur.no/).

**PRD implication:** scheduled data is a credible candidate for filling in stops after matching line, service date, endpoints and departure time. Exact pilot-line records, direction variants, operating calendars, changed stop patterns and stable identifiers have not been inspected. Source attribution and licence conditions must be met. A schedule match is not evidence that a vehicle is currently at a stop; actual device position and external estimates remain distinct.

## Tablet positioning

Lenovo's Idea Tab Plus platform specification lists GPS, GLONASS and Galileo for WLAN models, with A-GPS additionally listed for WWAN models. Thus WiFi-only does not, for this platform, imply absence of satellite positioning. [Lenovo PSREF platform specification](https://psref.lenovo.com/syspool/Sys/PDF/Lenovo_Tablets/Idea_Tab_Plus/Idea_Tab_Plus_Spec.PDF).

**Unverified:** the user's exact 12/256 GB regional model number was not identified. Platform specifications do not verify permissions, location/speed accuracy, GPS loss recovery or screen/background behaviour in Brave on the actual tablet. These remain pilot-device checks before accepting automatic stop progression and speed-based interaction behaviour.

## Open evidence needed before pilot acceptance

- Compare actual automatically retrieved messages against Svipper notices for the selected service dates and four lines; distinguish a successful empty result from unavailable or stale data.
- Verify timetable coverage and matching on representative route variants and dates.
- Verify the 100-metre stop-advance requirement, uncertainty indication and signal-recovery behaviour on the actual tablet/browser, including mobile-hotspot loss while positioning remains available.
- Record each source's publication/validity information separately from the assistant's last successful retrieval; two-minute polling is not a two-minute end-to-end warning guarantee.

