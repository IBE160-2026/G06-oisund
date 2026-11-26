# Svipper evidence digest — round 1

EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE

Access date: 2026-10-26. Publisher: Svipper on all substantive sources below. Small read-only web sample; no external mutations. No project files were used as evidence. Facts are restricted to material retrieved in this run. No API, feed, licence, refresh guarantee or complete driver coverage established.

## Sources and observed evidence

S1. https://svipper.no/meny/reise/trafikkmeldinger/trafikkmeldinger/
Title: Trafikkmeldinger. Published 31.07.2024 13.20; changed 31.03.2025 12.55. Direct web retrieval on access date returned heading, description and metadata, with no notice rows. Snippet: “Her finner du trafikkmeldinger om endringer og forsinkelser i kollektivtrafikken i Troms.” Page-level modification is not evidence of notice freshness.

S2. https://svipper.no/menu/travel/service-disruption/service-disruption-information-ny/
Title: Trafikkmeldinger. Same page publication/change metadata as S1. Direct retrieval also returned shell only. A search-index result retrieved today (reported crawl last month) exposed a historical list, NOT verified current state. Observed fields: route number/name or stop-place heading, summary, free text, affected origin/departure clock times, optional Period start/end, Last updated. No stable item ID/per-notice URL or machine direction ID visible in that excerpt.
Sample notice: line 28 Hamna–Sentrum–Solligården, bridge-related cancellations 28 September–1 October 2026; update 25 September 09:56. Origins Hamna skole øst 07:34, 10:29, 15:09, 15:39; Solligården 09:45, 14:25, 14:55, 16:05. Rendered Period 28 September 06:34–1 October 17:53, with no explicit timezone. The hour mismatch between departure and period is observed, not resolved. Snippet: “Innstilt grunnet stengt bru.” Other excerpt notices omitted Period and used open-ended language. Excerpt cannot prove retirement or live completeness.

S3. https://svipper.no/nyheter/apningen-av-tromsobrua-utsatt.6548.aspx
Title: Åpningen av Tromsøbrua utsatt. Published/changed 20.10.2026 13.32. URL contains article number 6548; this is an observed article identifier, not demonstrated canonical disruption ID. Bridge reopening postponed to no later than 27 November; phase 3 runs 17 August–27 November. Ordinary buses can cross 07:00–17:00; tunnel diversion otherwise. Line 20 has separate origin headings Skattøra and Malmvegen with route paths and unserved stops. It also covers 24, 26, X27, 28, 450 and regional lines. Some local exceptions are open-ended. Article includes route links/PDFs, not a structured notice lifecycle or history. Snippet: “Bruåpningen er satt til senest 27. november.” Specific driver-useful details exist, but this public article does not establish operational dispatch authority or completeness.

S4. https://svipper.no/nyheter/omkjoring-og-midlertidig-holdeplass-ved-uit.6988.aspx
Title: Omkjøring og midlertidig holdeplass ved UIT. Search-index official text retrieved; reported crawl six days ago. Published 19.10.2026 12.54; no changed timestamp shown in excerpt. Article number 6988. Hansine Hansens veg closure begins 19 October 21:00, includes 20 October, planned reopening early 21 October with explicit uncertainty. Segment Huginbakken–Muninbakken; diversion Klokkargårdsbakken. UIT platform 1 from centre moved south; platform 2 toward centre moved north. No exact route-number scope or guaranteed reopening time in retrieved text. Snippet: “Plattform 2 (mot sentrum) flyttes lenger nord.” This planned end predates access, but does not prove closure resolved.

S5. https://svipper.no/robots.txt
Direct web tool retrieval failed as inaccessible. No robots directives established; failure is not permission or prohibition.

S6. https://svipper.no/meny/hjelp-og-kontakt/personvern-og-vilkar/
Privacy/conditions index retrieved; no publication dates visible. It links ticket terms, website/app/map privacy, transport terms and accessibility. No automation/reuse permission found in inspected index. No claim that the entire site lacks such terms.

S7. https://svipper.no/meny/hjelp-og-kontakt/personvern-og-vilkar/transportvilkar/
Published 08.07.2024 13.05; changed 06.09.2024 10.57. Retrieved text links passenger transport rules, ferry rules and other legislation. It does not supply notice ingestion licence, polling contract or API entitlement. Snippet: “Her finner du informasjon om ulike transportvilkår.”

S8. https://svipper.no/meny/hjelp-og-kontakt/personvern-og-vilkar/personvern-svipper-no/
Website privacy link fetch failed (cache miss). No substantive privacy/automation conclusion drawn.

## Facts versus pilot inferences

Facts: static page retrieval does not reveal live rows in this tool; historical indexed list has route/stop/departure/update/optional validity fields; public news provides richer paths and direction prose. Generic route headings and free text coexist. Publication/change dates belong to pages/articles, while list items have Last updated.

Inference: an allowed pilot should preserve source URL, access time, retrieval mode, page and item dates separately, raw temporal wording, explicit line/origin/platform evidence, and nullable end/direction fields. A page/article number can identify an article but cannot safely deduplicate separate live notices. A content-derived key would be a local provisional key, not publisher identity. Confirm source access method and reuse conditions before unattended collection.

Inference: never auto-resolve because an item disappears, an estimated end passes, or an old shell metadata timestamp exists. Distinguish scheduled validity, last update, fetched time and confirmed resolution. Unknown route mapping or ambiguous temporal text needs review. Keep direct source link and evidence snippet available.

Coverage boundary: observed material is public collective-transport information with some driver-useful rerouting details. No retrieved evidence establishes vehicle restrictions, operator-only orders, exact duty/run applicability, safety clearance or complete driver operational coverage. Absence from these public pages cannot establish absence of an operational notice.

## Remaining gaps / next bounded checks

Need independently verified live rendered notice sample, stable item identifiers if any, provider-confirmed supported access/reuse/polling policy, timezone semantics, item update/deletion/end semantics, and operational driver coverage. Search-index historical notices cannot meet these requirements. No endpoint inferred from page layout.

## Round 2 — bounded source accessibility verification

Direct HTTP reads on 2026-10-26, after a sandbox DNS failure and narrowly scoped read-only network escalation:

- S1 official notice HTML returned HTTP 200. It contains an empty client widget and loads same-origin React assets. Observed CSS class js-trafikkmeldinger and widget instance a1396144-9841-41be-a784-fc4f49bd29bb. This instance is not a demonstrated disruption identifier. No iframe observed in extracted script/iframe tags. Snippet: “client-content-widget--trafikkmeldinger”. This explains why a static text extraction can miss notices; it does not verify rendered rows or completeness.
- S9 https://svipper.no/ClientApp/reactjs-front/client-content/build/static/js/trafikkmeldingerWidget.8b0692bd.chunk.js?v=18.0.5032 returned HTTP 200. Publisher Svipper (same-origin served asset); publication/change date not exposed in inspected output. Code references POST /api/presentation/v2/clientcontent/getwidgetdata/{widget-instance}/init and /update; init sends pageNumber, update adds transportType, sortField, pageNumber and pageSize. Snippet: “/api/presentation/v2/clientcontent/getwidgetdata/”. This is observed internal presentation machinery, NOT a supported public API contract. No POST or undocumented endpoint was invoked. Response schema, pagination guarantees, underlying transport provider, identities, timestamps and reuse entitlement remain unverified.
- S5 robots.txt succeeded HTTP 200 via direct request. Publisher Svipper; publication/change date not inspected. It has User-agent * and disallows selected administrative, file and legacy paths. The inspected directives do not disallow the requested /meny/reise/trafikkmeldinger/ path, the linked /ClientApp/ asset path or /api/ path. Snippet: “User-agent: *”. Robots directives are not an ingestion/republication licence or service commitment. Earlier web-tool failure was an access-tool limitation, not evidence of missing robots.txt.

Updated conclusion: official HTML and its linked rendering asset are fetchable in this bounded test; static HTML alone does not expose notice rows. A supported ingestion mechanism has not been established. Prefer provider clarification rather than operational dependence on this private presentation interface. The source page remains suitable as a provenance/manual-reference link. No retrieved evidence justifies current-state notice automation yet.
