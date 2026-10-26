# Qualification tasks and success criteria

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

These are future evidence tasks, not stories, an implementation plan or executed product tests. Supports CAP-1–7. All tasks are open in this first draft. No missing research answer blocks every smaller experiment.

## Gates apply to claims, not the whole initiative

- **Reference experiment:** may inspect retained public data and clearly labelled constructed cases. Requires truthful scope/provenance; no automatic shift-matching or completeness claim.
- **P1 matching qualification:** needs independently expected actual-date shift/departure examples for its supported cases, plus safe unresolved/manual paths. Unsupported edge cases can remain unresolved and outside supported claims.
- **P2 complete-pilot claim:** requires approved manifest/horizon and exhaustive required-content/calendar coverage. Four successful journeys cannot satisfy it.
- **Notice/progression integration:** separate later decisions. Neither is a prerequisite for first reference/matching value.

## Concrete missing-evidence tasks

| ID | Task and completion evidence | Claim blocked while open | Bounded work still possible |
|---|---|---|---|
| QF-01 | Approve exact lines/authority/operators, crossings and horizon; verify namespaced IDs including proposed line 28; compare independent expected service inventory with every manifest cell. | Complete pilot coverage (CAP-1/P2). | Line-20 reference samples and labelled partial coverage. |
| QF-02 | Obtain permitted, minimized actual-date shift/public-departure pairs with expected line, journey, service date, times and stop range checked independently of matcher output. Include unique, ambiguous and absent cases. Record any anonymization/date changes. | Correct automatic matching of real imported shifts (CAP-2/P1). | Constructed controls and explicit manual reference association. Shift fixtures shifted to 2030 do not validate current public journeys. |
| QF-03 | Establish source-system trip-number semantics with provider documentation or independently checked pairs across lines/dates/versions, including duplicate/private-code collisions and missing codes. Record crosswalk provenance. | A rule joining imported number to privateCode/entity ID. | Time/place/date-based candidate inspection or manual choice with unverified-number label. |
| QF-04 | Check service calendars/exceptions and source-shift time conventions; obtain expected extended-hour instants, both autumn repeated-hour occurrences and spring-gap cases. Verify each format's timezone/service-day axis. | Automatic resolution of unqualified calendar/DST cases (CAP-5). | Qualified ordinary dates/night samples; other cases unresolved. |
| QF-05 | Independently expected variant, changed-headsign, short-origin, repeated-platform/loop and partial-journey occurrence ranges; inspect full call order rather than PDF timing rows alone. | Supported automatic handling of unqualified pattern/subrange cases (CAP-4). | Ordinary supported patterns and explicit ambiguity/manual review. |
| QF-06 | Compare two source versions, including removed/replaced IDs, changed calendars and platform/headsign changes; demonstrate manual correction/confirmation stays attributable with no silent overwrite. | Production refresh preservation claims (CAP-6). | Frozen reference comparisons and labelled constructed update cases. |
| QF-07 | Confirm actual source terms/attribution and approved private-data handling; define public-snapshot retention, minimum external query facts and parent access/expiry controls. | Live private integration or redistribution outside allowed terms. | Existing permitted public observations and document/synthetic planning. |
| QF-08 | Check the notice producer's actual line/stop/journey/date selectors, static/original ID mapping and GTFS crosswalk; agree read-only vocabulary/version with its owner. Recheck current TRO streams. | Precise notice-to-departure joining or externally agreed identity API (CAP-7). | Documented v0 reference vocabulary and broad qualified relevance. |
| QF-09 | Inspect result closure/pagination/limits and active-date membership; exercise HTTP/GraphQL failures, quotas, unknown validity, stale source, no-service days and metadata/PDF discrepancies with independent expectations. | Reliable unique/not-found/network-absence claims for unqualified paths. | Labelled bounded lookup and honest unresolved/unavailable states. |

Research already supplies public schema/call examples, two PDF controls and archive HEAD metadata. It does not supply an approved shift crosswalk, parsed regional catalogue, all-city line manifest or qualified DST/loop/refresh implementation. Svipper/API agreement is a publication cross-check; independent upstream planning lineage is unknown. PDF/widget validity differs; the brief's old future-work language is not a substitute for the completed report.

## Proposed P1 casebook — twelve outcomes

Each case records input provenance/service date, candidate scope and snapshot, independent expected outcome, actual result and retained evidence. Use real public/sanitized pairs for positive source-matching claims; constructed negatives/control-flow cases are explicitly labelled. Expected results cannot be generated by the matcher. The following is a proposed acceptance corpus, not twelve tests run by this task.

| Case | Required example/expected behavior | Qualification focus |
|---|---|---|
| QC-01 | Ordinary outbound: correct dated journey/occurrence range; reviewable unique proposal only when the search scope is closed. | QF-02/09; CAP-2/3. |
| QC-02 | Ordinary inbound: destination display may differ from endpoint name; no reversed stop-list inference. | QF-02/05; CAP-2/4. |
| QC-03 | Two plausible departures or repeated-stop subranges: alternatives remain ambiguous until explicit choice. | QF-02/05; CAP-2/3/4. |
| QC-04 | No compatible journey in complete checked scope versus incomplete scope: not-found and unresolved remain different. | QF-02/09; CAP-1/2. |
| QC-05 | API/GraphQL/quota failure or stale data: unavailable/stale, retained input, no fabricated not-found or automatic retry loop. | QF-09; CAP-6. |
| QC-06 | Night departure: operating date, raw >24/dayOffset and next-calendar-day instants retained; non-active date yields no eligible match. | QF-04; CAP-5. |
| QC-07 | Longer/shorter variant with changing destination: select actual pattern and preserve occurrence headsigns/endpoints. | QF-05; CAP-4. |
| QC-08 | Partial journey with repeated platform visits: exact range or unresolved/ambiguous; no stop deduplication. | QF-05; CAP-4. |
| QC-09 | Holiday exception and DST ambiguity: independently justified date/instants, otherwise explicit unresolved rather than clock-order guessing. | QF-04; CAP-5. |
| QC-10 | User corrects/rejects/cancels: source baseline preserved, stale proposal invalidated, no silent manual-value overwrite or shift start. | QF-02/06; CAP-3/6. |
| QC-11 | Source changes after confirmation: compare versions; retain earlier confirmed facts within unchanged expiry; no replacement-ID reassignment. | QF-06/07; CAP-6. |
| QC-12 | Identity handoff: scoped line/stop/dated departure and optional occurrence retain provenance; no private fields leak and broad notice scope stays broad. | QF-08; CAP-7. |

P1 is qualified only for the declared supported cases when results agree with independent expectations and no unsupported automatic association, lost correction or private-data boundary breach occurs. Unqualified advanced cases may pass the **safe-unresolved behavior**, but that does not qualify positive matching for those cases. Record not-run separately from pass. QF-08 need not be complete to inspect the vocabulary; no external notice consumer is required.

P2 separately requires all approved manifest cells and required content dimensions to reconcile with independently checked extraction/inventory, calendars and exceptions. Report every residual gap as partial/unknown. Regional NeTEx/NSR versus GTFS comparison must show exactly which required facts survive; no format is adopted merely by downloading it.

## Document-task validation boundary

The installed bmad-spec coherence and preservation passes are recorded in validation.md and .memlog.md. They establish this draft's internal consistency and source coverage, not API behavior, full-network coverage, owner approval or operational acceptance. No product tests, ingestion or service actions are authorized by this file.
