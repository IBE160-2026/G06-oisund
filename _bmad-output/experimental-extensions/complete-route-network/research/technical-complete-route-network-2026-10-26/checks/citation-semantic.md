# Citation semantic check

Checked 2026-10-26 in fresh context. Scope: research.md, all seven digests, relevant saved API/query/summary/widget imports and source component. No project-context files read and no report/product edits.

## Result

No concrete load-bearing numerical or source-to-claim contradiction found. One confidence qualification: the Svipper PDF and Entur API are independently published artifacts, but independent upstream timetable generation has not been established. The evidence supports cross-publication agreement for one dated weekday endpoint/time pair, not an independent real-world operational oracle. The report already bounds this to one sample; preserve that boundary when assigning high confidence or saying different underlying sources.

## Priority checks

- **Observation:** Independently recounted raw line20 response: 799 templates, 136 with activeDates containing 2026-10-26; min/max dates 2026-10-19 and 2027-02-28. Eleven request-response imports excluding derived summary. Selected calls independently counted 42/43/79/25. Their endpoint instants and privateCode values match the report; all four publicCode values are null. No continuous/full-network horizon is inferred.
- **Observation versus normative support:** Raw night passingTimes records 01:30:00/dayOffset=1; selected calls use operating date 2026-10-31 and calendar 2026-11-01T01:30+01. Boundary response uses operating date 2026-10-24 and calendar 2026-10-25T01:30+02, with zero calls for 2026-10-26. This does not exercise the autumn repeated hour or spring gap, as the report states. Normative noon-reference guidance is recorded in identity-time-r2; current direct official page extraction reaches only the section heading, so this check did not independently re-extract its full DST prose.
- **Inference/recommendation:** NeTEx+NSR is explicitly conditional on archive qualification and pilot scope; GTFS remains viable after loss assessment. No archive content/completeness conclusion is drawn from HEAD. PrivateCode capability is not promoted into a proven source-shift crosswalk. These boundaries match digests.
- **Observation/control:** Official PDF20 spot check confirms weekday Malmvegen 05:16 to Skattora 06:09 and header end 2026-11-01. Saved widget line20 metadata ends 2026-12-31. Saved line42 widget metadata also ends 2026-12-31; its PDF end 2027-01-03 is supported by local-control digest, not independently re-extracted here. No Entur defect or synchronization lag follows. Night columns remain unqualified.
- **Normative/licence:** Official Entur terms explicitly require Entur attribution, licence link, modification indication and no implied endorsement, subject to NLOD exceptions, and disclaim completeness/availability. Report paraphrase is supported. Original-supplier attribution is conditional on the applicable licence, rather than asserted as a separately verified Entur requirement; settle actual supplier wording in the later qualification gate.

## External checks and limits

Three official-source spot checks only:

1. https://developer.entur.no/terms-of-service (licence and disclaimer prose read).
2. https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728563782/General%2Binformation%2BNeTEx (profile/version context read; full DST section not exposed by direct extraction).
3. https://svipper.no/regtopp/api/route/download/pdf/20_010926.pdf (ordinary first-column endpoint times and header read from PDF text).

Other normative citations were traced to the saved research digests rather than independently reopened. No visual PDF table qualification, archive parsing, cross-version identity comparison, actual shift mapping or exhaustive independent URL audit was performed. This is a semantic citation check, not legal clearance or operational acceptance.
