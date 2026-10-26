# Access focused follow-up
Accessed 2026-10-26. This follows access-r1.md and access-r2.md. No data archives downloaded.

## Retrieved evidence
Official deployed page https://developer.entur.no/open-data/timetable references https://developer.entur.no/assets/entry.client-BMl0nV0L.js . That entry explicitly imports TimetableTable from https://developer.entur.no/assets/TimetableTable-BjVlbSJI.js . Retrieved component saved as imports/access-TimetableTable-BjVlbSJI.js. These asset names identify the observed deployment, not publication dates; publication date unverified. Inspect that saved component for exact provider URL construction. The component response and file were obtained from the official site, rather than an unverified third-party mirror. No archive existence/size/content claim is established by a link expression.

## New root evidence to reconcile
Root reports live import-info TRO response saved separately as imports/import-info-TRO.json, timestamp 2026-10-23T12:01:39. This supersedes the older cached timetable-table timestamp for freshness. This follow-up does not independently reread the root import, so provenance remains that saved root evidence.

## Unresolved
Repository identity was not established by focused search. Exact archive contents, coverage horizons, identity drift and city-bus subset still require actual scoped dataset validation. Source asset inspection is evidence of offered URLs, not of archive availability.

## Verified URL construction from retrieved component
The official deployed component maps the key tro to Troms (Troms fylkestrafikk), then constructs the provider download links by interpolating that key. Therefore the exact offered Troms archive URLs are:
- NeTEx: https://storage.googleapis.com/marduk-production/outbound/netex/rb_tro-aggregated-netex.zip
- GTFS: https://storage.googleapis.com/marduk-production/outbound/gtfs/rb_tro-aggregated-gtfs.zip
The same table offers national NeTEx, GTFS and GTFS Basic, but individual provider rows have no GTFS Basic link. The component retrieves import dates from the documented public metadata endpoint. URLs are verified as current UI offerings, not HEAD-tested objects. No ZIP request made.
