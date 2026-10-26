---
title: 'Technical research: Automatic notices'
type: technical
topic: automatic-notices
decision: 'Select a bounded source and matching pilot outside approved V1'
source: native-run
status: complete
preset: standard
validation: normal
created: 2026-10-26
updated: 2026-10-26
verified_claims: 0
unverified_claims: 6
---

# Automatic notices: source feasibility and bounded pilot

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## Decision and evidence strength

Recommend an experimental **Entur TRO SIRI-SX candidate feed, with Svipper as the local reference and enrichment source**. First qualify collection completeness and a small, dated line-ID crosswalk; then nominate potentially relevant notices by exact line and planned time. Preserve manual web/SMS records and corrections separately. Do not promise complete operational coverage, exact trip applicability or automatic all-clear.

Svipper was investigated first: useful local detail exists, but its notice page renders through a JavaScript widget and no supported public ingestion contract was established. Entur documents TRO SIRI-SX and returned actual Tromsø notices, including a link back to Svipper. Vegvesen needs registered access and geographical route bindings before adding useful precision. These findings favor the supported structured feed over immediate dependence on the website presentation interface. [1][4][5][6][7]

This is completed source research, not permission to implement or accept new V1 scope. Evidence labels used below: **D** documented provider/standard behavior; **O** observed response/example; **P** planning recommendation; **U** unresolved. Provider facts have medium confidence unless corroborated; observations establish only the observed sample. The BMAD ledger has six single-provider load-bearing claims marked `unverified`: that means no independent-publisher verification, not that the documented behavior or HTTP observation was absent. Entur and Svipper may share upstream reporting, so their consistency cannot establish independent event truth.

## Recommended first delivery and implementation gates

1. **Extension-local spec:** define an Entur TRO SX experiment for a small reviewed Tromsø urban-line set, provisionally 20/24/28/42. These are scope candidates; the sample confirms structured 20/24, while Svipper has 28/42 detail. Require a reviewed crosswalk for every chosen line. Candidate display and source links supplement manual records; no operational alerting guarantee.
2. **Qualification before coding:** confirm complete collection/paging and restart recovery, permission/retention/attribution, and at least one changed, closed and withdrawn/missing sequence. Confirm local source coverage and relationship with Svipper. Obtain supported Svipper access if automatic enrichment is required; otherwise retain direct human links.
3. **Bounded evaluation:** use independent expected examples for exact 20 vs 020/X20, cross-operator collisions, wrong direction, stop-only/all-network, unknown validity, midnight/DST, open-ended/changed/closed, partial page/outage and manual correction. Measure missed/false candidates and stale-state comprehension against the source record, not the matcher output. Select thresholds and an effort cap with the owner in the spec; no benefit percentage is established.
4. **Stop conditions:** cannot obtain complete qualified collection, uncertain IDs are presented as exact, disappearance is required as proof of resolution, or maintenance exceeds the agreed cap. Narrow to a source-linked manual aid or stop the experiment. Vegvesen remains deferred until authenticated evidence and route-corridor bindings justify its cost.

The strongest limitation is counterevidence to over-broad automation: stop-only structured messages need extra mappings, detailed local prose can exceed the feed, and no current source demonstrates full driver operational coverage. No separate red-team pass was enabled; this limitation comes from the retrieved evidence itself.

## Source comparison

| Source | Access actually established | Coverage and limits | Pilot role |
|---|---|---|---|
| Svipper | D/O public pages; O JavaScript rendering and presentation paths found in one widget asset; U supported public API/reuse contract | O diversions, moved stops/platforms, bridge work, cancellations in historical indexed list. Public passenger information contains driver-useful paths, not verified dispatch authority | Local reference and human enrichment; seek supported access before unattended extraction [5][7][8] |
| Entur | D open SIRI Lite GET with application header; O HTTP 200 TRO XML page | D TRO SX listed; TRO GTFS-RT alerts cell blank. O stop/line messages and one regional ferry notice. No complete coverage or update-latency guarantee | First structured candidate source; filter by qualified geography/mapping locally [1][3][4] |
| Vegvesen | D registered DATEX XML access; O unauthenticated snapshot HTTP 401 | D national planned/ongoing road conditions. U live Tromsø content and transit applicability. Location is not a bus-line selector | Defer; later bounded road-corridor supplement [6][9] |

Entur SX carries end-user messages; cancellation/stop-pattern changes can also exist in ET, a separate stream. Do not equate an SX-only pilot with complete cancellation detection. Delay estimates, vehicle positions and ET ingestion are outside the proposed first slice. No retrieved source establishes comprehensive operator-only instructions, vehicle restrictions, driver duty applicability or safety clearance. [1]

Svipper's shell HTML contained a widget instance and React assets. One asset referenced POST presentation `getwidgetdata/.../init` and `/update` paths with paging/filter parameters. These are implementation observations, not a documented public API, stable schema or permission to use it. Robots allowed the sampled paths through absence of matching disallows; this is not an ingestion licence. Direct shell/JavaScript parsing is brittle: rendering revisions, pagination/filter changes, missing dates, and empty containers need explicit failure detection and maintenance ownership. Prefer provider-confirmed access; browser extraction would require qualified rendered-item samples, complete traversal and reuse terms before adoption. [5]

Entur requires an honest `ET-Client-Name`; open access does not require partner OAuth. Its current terms specify NLOD attribution, licence link and indication of modifications, with no endorsement or accuracy/completeness/availability guarantee. Documented SIRI Lite limit is four requests/minute; the sampled rate header differed, so retain the stricter documented rate. A five-minute pilot poll is a proposed starting budget, not a provider SLA; paging must share that budget. Retry with backoff and respect throttling. HTTP no-cache/no-store was observed; do not use intermediary caching contrary to those headers. Confirm application history/retention policy separately. [1][3][4]

## Actual messages and fields

Only three actual SX records were sampled, in one page at `2026-10-26T08:47:15Z`; **MoreData=true**. This is deliberately not a complete snapshot. [4]

| Example | Actually available | Missing or uncertain |
|---|---|---|
| `TRO:SituationNumber:426` | Participant TRO, creation time, open progress, summary/body, StopPlace `NSR:StopPlace:55902`, validity 26 October 04:45:22.805+01:00 to 30 October 03:00+01:00, Svipper article URL | No line/direction/journey selector observed in this record; article contains more detail [4][7] |
| `TRO:SituationNumber:TX1062813` | Tromsdalen roadwork; lines `TRO:Line:1_20`, `1_24`, `1_450`; nested affected route with `AffectedOnly=true`; quays `NSR:Quay:96986`, `88834`; open-ended from 17 August | No direction/dated journey in sample. Do not discard nested qualifiers or treat every line trip as definitely affected [4] |
| `TRO:SituationNumber:TX1063335` | Replacement ferry/capacity notice; network 1, line `TRO:Line:1_191`; open-ended from 23 October | Regional, not a qualified Tromsø urban match; shows TRO geography alone is too broad [4] |

All three had CreationTime, SituationNumber, SourceType, Progress, StartTime, severity, ReportType, Summary, Description and Affects. Version and VersionedAtTime were absent. ResponseTimestamp is response time, not notice edit time. StopPointRef contained both StopPlace and Quay ID types. Some Norwegian prose was tagged English. Preserve raw language metadata but do not rely on it to suppress content. No direction/dated journey observed does not mean the schema cannot support them. [4]

Svipper article 6992 gives platform arrangements for 26–29 October, planned normal service 30 October, exact public lines and direction prose, including line 24 airport versus Skjelnan, 28 Solligården versus Hamna and 42 both ways. Published 23 October 16:07, edited 16:26. This corroborates a cross-channel event link, and also demonstrates unequal detail. Do not replace structured validity with the article's undated-time prose or claim that either channel updates first. [7]

Bridge article 6548, edited 20 October, contains directions, detour paths and unserved stops; UIT article 6988 describes platform moves and an estimated reopening. The historical indexed line28 cancellation list includes departures and a period with an unresolved hour discrepancy. Historical search excerpts and planned reopening dates are not current resolution evidence. [8]

| Field | Entur sample | Svipper evidence | Vegvesen |
|---|---|---|---|
| Stable identity | SituationNumber + ParticipantRef | Article ID/URL observed; live-item identity U | D situation/record IDs and versions, current payload U |
| Title/body/link | Summary/Description; InfoLink in one example | Article title/body/URL; list excerpt text | D descriptions; current fields U |
| Published/updated/fetched | CreationTime; no notice update/version in sample; response/fetch separate | Page/article publish/edit; list Last updated, different clocks | Historical docs publicationTime/Last-Modified; current contract U |
| Validity | Offset start, optional end | Prose and optional list period, timezone ambiguity | D standard validity; Norwegian populated fields U |
| Lines/directions/stops/departures | Actual line/stop refs; no direction/journey in page | Prose line/direction/platform/departure examples | Road location; transit selector coverage U |

Schema capability is not field-population evidence. Entur's dated-journey examples describe VehicleJourneyRef plus origin departure, or framed dated-journey refs. They are not TRO observations. The GTFS comparator offers time periods and affected selectors, but it does not establish a usable TRO alert feed or identical SIRI conversion. [4][10][11]

## Matching with today's workday

**P:** Begin with exact operator/codespace + public line + known planned interval. Project context permits nullable line/trip/direction strings and explicit Oslo activity timestamps; it does not guarantee canonical transit IDs, stop sequences or geometry. A printed trip number is not automatically an Entur journey ID. These are project constraints, not provider findings (`digests/project-context.md`).

Use a small reviewed crosswalk from the pilot's confirmed printed lines to canonical LineRefs, dated and scoped by operator. The observed `TRO:Line:1_20` is one verified example, not permission to generate IDs by string concatenation. Preserve `020`, `20`, `X20` and `20E` as distinct unless an explicit sourced alias binding says otherwise. Avoid substring/number-only matching. A line collision across operators must not match.

Compare explicit intervals as instants; display Europe/Oslo. Use activity calendar times across midnight, not only the service-date header. Preserve DST ambiguity and missing timestamps. Unknown source timezone/end/direction stays unknown: an explicit line with incomplete validity can be a review candidate, never a confident exact trip match. Open-ended validity means no supplied end, not perpetual freshness. Multiple validity windows and nested scope restrictions must survive normalization. A stop qualifier unsupported by today's plan keeps the result conditional.

Suggested candidate tiers:

- Exact reviewed line binding + known overlapping interval: **line/time candidate**, with direction/stop limitations shown.
- Missing mapping, validity or direction: **uncertain candidate**, with the specific reason; do not silently drop it or invent the missing fact.
- Stop-only event: nominate at day level only if a confirmed endpoint/stop binding exists; otherwise show a separately labelled local-area notice for review. Giæverbukta illustrates this limitation.
- Explicit all-network/all-line message: retain broad scope for the qualified operator/area. Empty affected-line list means unknown scope unless the source explicitly says all. A city/road-area match alone is broad context, not all lines or precise trip relevance.

With complete route data later, add versioned NSR StopPlace/Quay, route pattern, direction mapping, ServiceJourney/dated journey, stop order and geometry. This improves precision but is not necessary to evaluate the first line/time slice. Road proximity and free-text destinations cannot establish a route intersection.

## Updates, closure, duplicates and failure

**D:** Entur SIRI uses full versus requestor-session delta behavior and MoreData paging. Its profile describes explicit `Progress=closed`, immediately removed from journey search but redistributed until EndTime, at least five hours ahead. This is documented behavior, not a closure transition observed in TRO. [1][2]

**P:** Namespace identity by source/participant/SituationNumber, preserve versions when supplied, and compare a normalized payload fingerprint when update/version is missing. Keep creation, publisher update, response, first/last observation and last complete successful collection separately. Fetch time is never a manual check or a source edit. Reject older regressions/out-of-order records; versionless contradictory updates need traceable ordering and review.

Before delta use, qualify baseline completion, session identity, timeout recovery and page continuation. The bounded sample did not establish the returned cursor location. A partial page or failed page must leave collection incomplete. A last complete baseline plus later deltas needs explicit completeness/freshness state. A disappeared result is **not seen**, not **resolved**. Expired published validity can stop active candidate display while retaining an explicit expired-validity reason; it does not prove road reopening. Explicit source closure ends that source's claim, not a user's manual record.

Cross-source deduplication should create a reviewable event group, leaving immutable source contributions distinct. Strong anchors: explicit source link/foreign ID plus compatible place/time/scope. Similar titles alone are insufficient. Retain disagreements, both timestamps, links and scope; avoid silently selecting the newest scrape as truth. Article6992 and situation 426 justify a proposed link, not deleting either source. Corrections must be detachable if a group later proves wrong. [4][7]

Suggested collection states: complete-success, partial, unavailable, stale and never-qualified; separately track zero matching candidates. Show last attempt, last complete success and source age. HTTP 200 with an empty shell, MoreData or parse failure is not complete-success. HTTP 401 is unavailable, not zero notices. Retain previous observations with stale/incomplete labels and a route to source verification. Proposed five-minute collection and fifteen-minute collection-age warning require pilot validation; neither measures publisher latency. Old CreationTime alone must not stale an actively republished open notice.

## Manual records and the route-network extension

**P:** Keep source message, locally computed relevance, and user additions as separate conceptual records. Manual web/SMS content, user correction, manual end and manual checked-at remain user-owned. Source updates must not overwrite them, mark them checked or reactivate a manually ended record. Link an overlapping manual record by explicit user decision and preserve its original evidence. Recompute relevance against the confirmed plan revision; a changed plan must not retain an unexplained old match.

The route-network extension should remain independently planned. Proposed common interface: codespace/provider; dated network dataset version; canonical LineRef and public code; typed StopPlace/Quay; route-pattern/direction and dated-journey bindings; provenance and validity of mappings. The automatic-notice extension consumes a read-only identifier resolver, initially a small qualified crosswalk. Later it can consume the network extension's versioned route/stop resolver without importing its roadmap. It should not own timetable ingestion twice.

The automatic-notice boundary owns source snapshots, lifecycle, provenance, candidate reasons and collection health; the network boundary owns route identities/topology. GPS, automatic stop progression, vehicle tracking and complete timetables are excluded. Precise stop/direction/road-corridor matching requires additional validated mappings; do not quietly make those deliverables prerequisites for a simpler line/time experiment.

## Open questions and next BMAD step

| Question | Evidence/action required before dependent implementation |
|---|---|
| Svipper supported access and reuse? | Provider documentation/contact, qualified live widget result, rate/pagination/lifecycle contract; no contact sent in this run |
| TRO completeness and lag versus Svipper? | Provider confirmation and small paired observations over time; one sample cannot estimate latency or missed events |
| SX closure/retraction/session recovery? | Actual transitions, cursor/page tests under limits, missed-close and full-resync rules |
| Pilot line/direction/stop bindings? | Dated official ID crosswalk and independent examples, no invented numeric ID formula |
| Retention and stale UX? | Agreed application history policy, privacy/expiry alignment, owner comprehension criteria; HTTP cache headers alone insufficient |
| Vegvesen worth adding? | Registered current payload/profile, Tromsø examples, cancellation/rate rules and route geometry; currently no live event evidence |
| V1 baseline compatibility? | Reconcile later accepted committed baseline explicitly; do not adopt main-workspace uncommitted 11.5/11.6 by implication |

Next: **[SPC] `bmad-spec`**, in a fresh context, consuming this report and the preserved scope. Bind output to `automatic-notices/specs/spec-automatic-notices/` and verify all destinations before writing, following `bmad-workflow.md`. Record unresolved gates and non-goals. Then **[CA] `bmad-architecture`** can decide the new ingestion/retention boundary against the read-only V1 spine. Do not run V1 sprint planning or Build. This follows the installed BMAD catalogue, not an implementation authorization.

## Method and isolation

Access date: **26 October 2026**. Standard technical Run: three source dimensions, at most eight sources per dimension/round, two rounds; stop on coverage or exhausted useful leads. Official documentation, small public article samples and one bounded Entur GET were used. No subscriptions, authenticated Vegvesen collection or Svipper presentation API invocation occurred. Main and route-network worktrees were not changed. No product code, database, service, test, active V1 artifact, commit, merge or push was touched.

Repository/root and working directory: `D:/IBE160-plan-automatic-notices`; branch `codex/plan-automatic-notices`; HEAD `aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed`. Initial status contained only the existing untracked extension area. Existing four planning files are preserved. No AGENTS.md was found in the worktree scan; the establishment source-map also records absence at the parent. Newer main-workspace 11.5/11.6 and Epic 11 retrospective remain background references, not accepted requirements or copied inputs.

All new files are in this run. Resolved BMAD defaults were inspected; research output was bound per invocation, with no configuration edit. `digests/project-context.md` records read-only project-field evidence; provider digests record URLs, dates, access failures and observation boundaries. `brief.md` is the run plan, not its final deliverable. `research.md` is the report. Rounds stopped after source feasibility was established and remaining gaps required provider confirmation or a later controlled experiment.

## Source appendix

All accessed **2026-10-26**. Extended evidence and other source URLs are in the named digest. Unknown publication dates remain unknown. Medium means primary but single-publisher; observed means sample-only, not a coverage guarantee.

| Ref | Supports | Publisher/source | Publication/update | Confidence |
|---|---|---|---|---|
| [1] | Streams, TRO matrix, access, paging/rate | [Entur realtime](https://developer.entur.no/open-data/realtime) | 2026-08-31 per researcher | Medium D |
| [2] | Explicit closure and validity | [Entur SX validity](https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370694/SIRI-SX+-+Validity+of+a+message) | 2019-03-19 | Medium D; TRO transition U |
| [3] | Application identity and licence | [Entur terms](https://developer.entur.no/terms-of-service) | 2026-09-28 | Medium D |
| [4] | Three actual SX records and missing fields | [Entur bounded TRO GET](https://api.entur.io/realtime/v1/rest/sx?datasetId=TRO&maxSize=3), digests/entur-r1.md | Response 2026-10-26 | O; incomplete |
| [5] | Widget shell/access and robots investigation | [Svipper traffic notices](https://svipper.no/meny/reise/trafikkmeldinger/trafikkmeldinger/), digests/svipper-r1.md | Page edited 2025-03-31; assets observed 2026-10-26 | O; supported contract U |
| [6] | DATEX registration/types | [Vegvesen overview](https://www.vegvesen.no/fag/teknologi/apne-data/et-utvalg-apne-data/hva-er-datex/), digests/vegvesen-r1.md | Not stated | Medium D; actual unauthenticated HTTP 401 |
| [7] | Same linked event, richer local fields | [Svipper Giæverbukta article 6992](https://svipper.no/nyheter/stengte-plattformer-pa-giaverbukta-terminal-fra-mandag-26-oktober.6992.aspx) | 2026-10-23 edited 16:26 | O; cross-channel consistent |
| [8] | Local detour detail; bounded historical samples | [Svipper bridge article 6548](https://svipper.no/nyheter/apningen-av-tromsobrua-utsatt.6548.aspx), digests/svipper-r1.md also lists UIT6988 and indexed list | 2026-10-20; other dates in digest | O; indexed material explicitly historical |
| [9] | Road access/lifecycle gaps | [Vegvesen production snapshot](https://datex-server-get-v3-1.atlas.vegvesen.no/datexapi/GetSituation/pullsnapshotdata), digests/vegvesen-r1.md | Probe 2026-10-26 | O401; no event payload |
| [10] | Comparator fields/full-feed semantics | [GTFS realtime specification](https://gtfs.org/documentation/realtime/reference/) | Not stated | Medium D; TRO feed U |
| [11] | Journey selector examples, not TRO field proof | [Entur dated-journey example](https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370814/SIRI+SX+-+Message+on+multiple+vehicles+on+multiple+dates), digests/entur-r1.md | 2019-03-26 | Medium D |

## Staleness and refresh

`claims.json` is derived from the six ledger claims. `staleness.json` is computed by the installed helper using one month for access/licence, 24 months for documented lifecycle, and immediate recheck for live examples. Unknown original publication dates for access observations use observation date explicitly, never a fabricated publication date. This is a refresh work order, not notice validity or a freshness SLA. Historical lifecycle evidence already needs reconfirmation; live samples must be refreshed before implementation. The computed earliest recheck is 19 March 2021 for the old lifecycle reference: revalidate it before implementation. The live sample recheck is 26 October 2026; Svipper/Vegvesen access observations are due 26 November 2026. Access documentation is already outside its one-month publication-age window; the terms recheck is 28 October 2026. The helper uses publication age, even when a page was visited today; a stale flag does not claim today’s access failed. Exact dates supplement the month-precision ledger from source digests, with date_basis recording observation versus publication. Regenerate when the ledger changes.
