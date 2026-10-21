# Story 10.1: additional PDF probes, 21 October 2026

Owner acceptance: Jonas approved the 10.1 walkthrough on 2026-10-21 and authorized commit/push with devlog. He explicitly accepted leaving the false t-marker warning at example 8 activity 13: the leading t of right-column tom / 76567 is captured in the left crop and attached to the preceding Sign-on. This diagnostic was reproduced read-only after the final tests; no product code changed. The earlier pending-acceptance statements below are historical. Story 10.1 is done; 10.2 is not started.

## Correction after owner feedback

The initial failures below were reproduced and corrected under [the amendment specification](../../_bmad-output/implementation-artifacts/spec-10-1-additional-import-fix.md). Fadder/Instruktør now remain typed, timed activities. CAR designations remain separate from numeric duties with null numeric suffix; the zero-duration CAR transition and following Tomkjøring med CAR remain separate. No physical bus is inferred. Source facts still collapse after adoption/reopening.

The independent post-fix probe reports **23/23 and 8/8 ordered source rows, no missing/extra rows, no unresolved source lines**, and equal typed JSON round trips. Both now return bounded-layout for these exact files. All three ordinary/CAR duty occurrences and anchors, numeric 181/176 values, null CAR suffix, all clocks/endpoints, full headers/calendar values and provenance are covered by new regressions. The original seven-fixture source is preserved as an exact historical snapshot with its existing SHA-256; its approval hash was not changed to match the expanded README.

Final backend verification: **161 backend/API/PostgreSQL tests in 107.74s**, including actual import/save/reopen/replay for both new fixtures; real PostgreSQL/API restart and migration replay with identical synthetic account/session/draft/operation/deadline; production build. All 96 parser/mapping regressions also passed against final source in 15.97s, including eight focused additional/unknown-designation cases. The provenance test initially omitted nullable typed-location fields in its comparison; corrected the test to compare source page/column/line, without product changes.

The first complete browser run passed 67 and failed the two new cases while reading genuine API bodies through Edge's inspector cache (`Network.getResponseBody`: response evicted). Corrected the harness to read the real API response in a pass-through route handler before fulfilling it; no mock facts or product changes. Both additional examples then passed the focused browser run (2 tests, 15.3s), including review, adoption, actual save and reload/reopen with exact API record equality. The final complete browser run passed **69 tests in 3.0 minutes**. Root visually inspected the reopened [CAR return](10-1-example-8-activity.png) and [Fadder interval](10-1-example-9-activity.png). No application code changed after these final results.

Verified local rollout: existing operational database container/volume/secret retained, all before/after read-only checksums/counts equal for accounts, drafts, operations, deletion acknowledgements, sessions, security settings and migrations. Live backend file hashes match the tested source, health returns 200, and the live frontend serves the final production bundle. Disposable services are stopped. No operational test mutations, migration, commit/push or story acceptance. Local link: http://127.0.0.1:5173/private?review=10.1-eksempel-8-9 . Earlier-story generated screenshots were restored; only 10.1 evidence retained.

One independent Blind Hunter review completed. All four findings were patched: unknown nonnumeric vehicle designations now stay partial; the standalone probe no longer mistakes CAR for a route line; new source/header checks cover the extra fixtures; source review displays readable pilot-car text. No findings deferred. Story acceptance remains with the owner.

## Initial exploratory result before correction

Initial result: **both examples were partial; neither passed the complete source expectations.** The [approved additional fixture baseline](10-1-additional-fixtures.md) establishes expected facts, not a passing implementation or story acceptance.

All three new pages were rendered with pypdfium2 and visually inspected. Expected rows were read from the independently prepared `Eksempelfiler/README.md` tables before production extraction. The probe used the existing disposable test image, bounded spawned-process `extract_pdf`, production `interpret`, typed validation and a JSON/model round trip. It had no database connection. No operational account, session or draft was read or modified; no product code or deployment changed.

| Check | Example 8 | Example 9 |
| --- | --- | --- |
| Source / mapped activities | 23 / 23 | 8 / 4: fails |
| Ordered labels, clocks, endpoints, line/trip identifiers and page numbers | All 23 match | Four retained rows match; four missing |
| Header | 90000008, 2030-01-10, 06:17–15:15, work 8h28, span 8h58, two pages | 90000009, 2030-01-14, 04:40–14:00, work/span 9h20, one page |
| Ordinary duties | 960181/181 initially; 960176/176 from activity 14, after second Sign-on | No duty or physical bus invented |
| Pause grouping | Rows 11–12, meal 09:38–10:23, 45 minutes; source rows retained | Three separate Coffee rows: 18, 17, 52 minutes |
| Application qualification | partial: one unrecognized source line | partial: four unrecognized source lines |
| Typed JSON round trip | Equal | Equal, including omissions |

Example 8 preserves the final Wi-To endpoint of trip 1006 at **07:45**, rather than intermediate 07:22. The empty Notes page produces no extra activity. Zero-duration CAR/76566 remains at 14:58–14:58 with both Wi-To endpoints.

## Gaps before qualification

1. **Pilot-car designation is lost.** `Vogn CAR - 1` becomes an unrecognized-line issue (page 1, column 2, line 49). CAR/76566 is mapped as an ordinary `trip` with line `CAR`; deadhead 76567 lacks the owner-clarified pilot-car mode. The only mapped duty change is to 960176, so the editor's effective duty continues as 960176 through the pilot-car return. CAR and return rows have no individual uncertainty note; only a global source issue indicates the missing interpretation. Preserve CAR separately, without an invented numeric suffix or physical bus.
2. **Four work activities disappear in example 9.** Missing: Fadder 04:43–06:40, 06:58–08:21 and 08:38–10:08; Instruktør 11:00–14:00. Only Sign-on and three Coffee rows survive. Four global warnings identify unrecognized source lines (page 1, column 1, lines 2/4/6/8), but the missing labels/times are absent from adopted source activities. Saving cannot recover them. Preserve exact labels/times even if internal classification remains unresolved; do not infer product roles.

During that initial exploratory probe, no browser, API save/reopen or PostgreSQL restart test was run for these files. A model JSON round trip is not a storage test. The correction results above supersede these initial failures. The original seven-fixture oracle was not regenerated from the updated README.

## Reproduction

From the project root, using the already built disposable image and an existing temporary output directory:

```powershell
docker compose -p ibe160-private-tests -f compose.private.yaml run --rm --no-deps -e PYTHONPATH=/app -v D:/IBE160/Eksempelfiler:/fixtures:ro -v D:/IBE160/scripts/probe-additional-imports.py:/probe.py:ro -v D:/IBE160/tmp/pdfs/10-1-additional:/render private-api python /probe.py
```

The probe writes `probe-result.json` under the temporary render directory and prints measured discrepancies. Exit 0 means execution completed, **not** qualification passed. Its first attempt lacked PYTHONPATH and failed before extraction; the corrected run completed.

Source SHA-256:

- Example 8: `e44612caac1b676f1ea4d9bf88f8378960a0fb097ffe517a9e9d442f1edfa03d`
- Example 9: `65b50ecb01c5372a17aa2a2e7db9d3bda88767db908448c3ba70cf540d666b18`
