# Local control round 1: Svipper Tromsø

Access date: 2026-10-26. Scope: two official timetable PDFs, official timetable/map landing pages, and public planner entry point. No Entur comparison was performed in this workstream.

## Evidence rules

1. Never conclude from training data alone. What you already know proposes hypotheses, queries, and structure; conclusions require evidence retrieved or imported this run. A claim you cannot evidence is stated as an unverified belief or not at all.
2. The research firewall. Project context shapes what to ask, never what is true. It is inadmissible as evidence: every claim in a research artifact traces to a digest or import file with a source.

## Source register

- S1: https://svipper.no/meny/reise/rutetabeller-og-kart/rutetabeller-buss/ . Retrieved HTML and web extraction. Published 2024-07-03, modified 2026-07-13. Explains searchable PDFs and links to planner/map. Its static extraction omits actual timetable results.
- S2: https://svipper.no/regtopp/api/route/search . Public widget POST bodies {"phrase":"20"} and {"phrase":"42"}. Exact responses: ../imports/local-search-20.json and ../imports/local-search-42.json. Widget discovery: GET https://svipper.no/regtopp/api/route/app and https://svipper.no/regtopp/rutetabeller/js/main.0a5461d1.chunk.js . Script identifies the search and download endpoints.
- S3: https://svipper.no/regtopp/api/route/download/pdf/20_010926.pdf . Exact downloaded file ../imports/local-20_010926.pdf, 2,964,657 bytes, 14 pages. Web PDF extraction read pp. 1, 3, 8, 9 (1-based), with surrounding text. Local Python extraction unavailable.
- S4: https://svipper.no/regtopp/api/route/download/pdf/42_010926.pdf . Exact downloaded file ../imports/local-42_010926.pdf, 2,873,197 bytes, 16 pages. Web PDF extraction read pp. 1, 4, 10, 11 (1-based), with surrounding text.
- S5: https://svipper.no/meny/reise/rutetabeller-og-kart/linjekart/ . Published 2024-07-03, modified 2026-03-02. Lists Tromsø area line map as a 2025 PNG (4 MB), and a 2024 stop map PDF. Linked PNG URL https://svipper.no/_f/p3/i5b905075-d1ff-41fd-852d-8ae76c2ba426/linjekart-tromso-og-omegn-2025.png was not successfully inspected: web fetch used a malformed relative expansion and reported unsupported octet-stream. Map topology therefore remains unverified here.
- S6: https://kart.svipper.no/reise . Official linked journey planner. Web extraction yielded zero lines. No journey query/result, planner horizon, stop identifiers, or timetable agreement was observed. Dynamic-source limitation.

## Bounded observations

### Line 20 (S2, S3)

Widget coverage: 2026-09-01 to 2026-12-31. PDF coverage: 2026-09-01 to 2026-11-01. Preserve both; later coverage is unestablished.

Directions: Stakkevollan and Kroken. Weekday p.1 example: Malmvegen snuplass 05:16 to Skattøra Borettslag 06:09. Reverse example p.9: 09:20 to 10:11.

On p.1 early columns serve Breivika and Seminarbakken; later columns substitute Tromsdalen Bruvegen. Footnote T signifies the tunnel variant. These timing rows are not verified exhaustive stops.

Night p.3: Friday-marked departures 01:57 and 03:01 arrive 02:50 and 03:54. A separate 01:30 departure begins at Fr. Langes gate F1, arriving 01:50: a short-origin candidate. Service-day interpretation needs verification.
### Line 42 (S2, S4)

Widget metadata period is 2026-09-01 through 2026-12-31; PDF headers instead end 2027-01-03. This is another observable metadata/document mismatch, not evidence of Entur disagreement.

Directions include Eidkjosen and Stakkevollan. Weekday p.1 example departs Skattøra Borettslag at 05:15, calls at Tromsø lufthavn at 05:53 and Kvaløysletta terminal at 05:58, then arrives at the first named destination at 06:13. Reverse-direction timing rows on p.10 include Killengreens gate, Skippergata, and Varden. Directional rows differ; reconstructing the reverse by simply reversing one list would be unsupported.

Night p.4 has Friday-marked departures from the origin at 02:07 and 03:07, with destination arrivals 02:57 and 03:57. A 01:30 trip begins at Bankgata and reaches the destination at 01:59. The ordinary 23:55 trip crosses midnight and arrives 00:53. These are concrete tests for service-day association and short-origin variants, not a full night-service inventory.

## Matching and completeness implications (inference from observations)

- Official documents expose line, direction, day category, notes, times, and selected timing rows. The inspected rows show no internal trip number usable as a cross-source join key. This is a scoped non-observation, not proof no identifiers exist anywhere.
- Candidate matching should use service date/day interpretation, line, direction/endpoints, timing and ordered observed calls, then report uncertainty. Never equate a printed time column or line number with an Entur journey identifier.
- PDFs supply useful independent passenger-facing spot checks and reveal variants. They do not establish a complete machine-readable route-pattern catalogue, full stop lists, complete horizon, or live disruption state.
- A date disagreement between widget metadata and the linked official PDF is directly supported. Entur/Svipper synchronization, disagreement, and update lag remain untested; no such claim is justified by this sample.

## Retrieval limits

Two PDFs downloaded, no bulk crawl. Searches that returned third-party transport pages were excluded as evidence. The public planner and image topology could not be examined through static extraction. Screenshot calls returned citation-only wrappers in this environment, so no visual table-alignment verification is claimed. Night alignment is based on extracted columns and Friday footnotes; verify the original PDFs visually before treating the short-origin examples as acceptance fixtures.