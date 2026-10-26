# Provisional scope — Automatic notices

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Status: exploratory planning, 2026-10-26. These are questions and investigation boundaries, not accepted requirements or a delivery commitment.

## Intended benefit

Reduce repetitive source checking by collecting relevant traffic/public-transport notices and presenting qualified candidates against the workday's planned trips. Evaluate the actual benefit including manual verification, false positives, missed notices and maintenance effort. No coverage or time-saving result has been established.

## Candidate investigation

- Identify viable sources, actual geographic/operator/line coverage, access methods and terms of use.
- Investigate matching by line, validity interval, stop and, where supported, direction or route alignment. Preserve uncertainty when plan/source identifiers or details are missing.
- Distinguish confident candidates, uncertain candidates, unavailable sources and missing data. An empty result must not imply that roads are clear.
- Preserve provenance and distinguish source publication/update time, retrieval time and explicit human source checks.
- Investigate stable identities, changed messages, duplicates, expiry, withdrawal and disappearance. A missing message or failed fetch cannot by itself establish resolution.
- Determine how automatic candidates coexist with manually maintained web/SMS notices, including overlap, corrections and conflicting information. Automatic import must not silently overwrite manual content or mark it checked.

No source, polling interval, storage model, provider, matching threshold or UI solution is selected here.

## Inherited boundaries and dependencies

SCOPE-02 remains the approved V1 contract. Preserve explicit manual activity selection, planned versus actual facts, unknown values, server authority, private/demo isolation and truthful failure states. An extension architecture must explicitly assess any new source-integration boundary; the current V1 spine deliberately defers that boundary.

Use confirmed planned line/date/activity facts as the starting point. Determine whether these facts support any useful matching without additional route data. Stop-level matching may need dated line/stop identifiers and trip-pattern or direction mappings that the imported plan does not contain. Record that dependency and its cost before choosing a narrower or broader experiment.

Complete route datasets, GPS, automatic stop progression and live vehicle tracking are separate potential developments. Do not make them implicit deliverables or prerequisites. No offline guarantee, driving alert, deployment expansion or real-shift permission follows from this initiative.

## Open decisions for the next planning stage

1. Which initial operator/geography, notice types and example workdays should bound the investigation? Existing Tromsø lines 20/24/28/42 are project context, not verified source coverage.
2. Which official sources are accessible, licensed for the intended use and sufficiently structured? Are authentication, rate limits, redistribution, caching or attribution restrictions relevant?
3. What is the minimum useful match? How should leading zeros, line aliases, service versus calendar date, overnight times, Oslo DST, gaps and unknown validity be treated?
4. Which stop/direction facts exist in both the planned trip and source? When must the result remain a broad candidate or be withheld as unmatchable?
5. How will representative independent examples establish correct matches, missed events and false matches? What would justify stopping the experiment?
6. How should freshness, changed/ended notices, stale retained results and total/partial source failures be explained?
7. Who owns manual versus automatic records, deduplication, corrections, source checks and retention? How will private planned trips be kept out of unnecessary external requests?
8. What effort limit and later acceptance decision would justify proceeding without consuming the V1 completion reserve?

## Establishment boundary

This task creates the planning area and reads the project baseline only. Source verification, external research, specification approval, architecture decisions, story creation and implementation are later work. Existing V1 epics 9–12 and aliases V1-01–V1-20 remain unchanged.
