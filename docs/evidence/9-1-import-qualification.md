# Story 9.1: actual text-PDF qualification — 20 October 2026

Six examples qualify for automatic extraction of the approved source facts. Example 6 is **partial**: its owner-completed Travel to interpretation cannot be extracted from its single source time. All seven approved files / ten pages were tested; none is untested. This establishes a useful bounded envelope, so no failed-envelope scope decision is required. It does not approve a production import feature.

The [machine-readable comparisons](9-1-import-qualification.json) contain each expected/actual field, match, source/derived/unresolved attribution, separate owner assistance, PDF hashes, oracle/implementation/lock hashes, executable versions and per-document timing. The approved [independent fasit](../../Eksempelfiler/README.md) was mechanically transcribed into JSON **before PDF inspection/extraction**; duty occurrence positions were subsequently added directly from its descriptions, not from parser output. `scripts/transcribe-import-oracle.py` makes that transcription auditable. The adapter does not read the oracle, README, filenames or fixture-specific answers.

| Example | Pages | Source rows | Source mismatches | Owner assistance gaps | Classification |
| --- | ---: | ---: | ---: | ---: | --- |
| 1 | 4 | 33 | 0 | 0 | supported |
| 2 | 1 | 16 | 0 | 0 | supported |
| 3 | 1 | 6 | 0 | 0 | supported |
| 4 | 1 | 16 | 0 | 0 | supported |
| 5 | 1 | 5 | 0 | 0 | supported |
| 6 | 1 | 16 | 0 | 6 | partial |
| 7 | 1 | 21 | 0 | 0 | supported |

Totals: **113 explicit rows, 46 route trips, 30 numbered deadheads** automatically extracted. The independent total of **31 deadheads** includes owner-assisted Travel to. Required comparisons include headers and historical weekday text, ordered activity labels/types/times/identifiers/endpoints, source pages, explicit calendar instants, all repeated duty occurrences and their positions, three-digit suffixes, null actual bus, and field provenance. Stable source order distinguishes repeated trip numbers. Equal start/end survives for deadhead 75803. Four-page and two-column continuations remain one shift. Adjacent meal rows group without deleting rows; the two separated Coffee intervals remain separate.

Calendar instants are derived from the source service date, header start and stated Utstrekk. Candidate instants must fit the uniquely bounded interval; the adapter never infers a date solely from descending clocks. Example 4 retains service date 2030-01-05 and trip 6072 ending 2030-01-06T00:35:00+01:00. If the header duration cannot prove a unique interval, times remain unresolved. The qualified dates are January examples; daylight-saving transitions are unqualified.

Example 5 preserves paid header end **08:51**, work/span **2h00**, and last Sign-off **08:29** with five source rows. Its 22 minutes of paid free time remain an owner explanation, with no invented activity. Example 6 retains source `Travel to`, end **16:00**, unknown start/endpoints/trip ID, and an unresolved start. The six assistance gaps are start clock, deadhead classification, origin, destination, start calendar offset and start instant. The report separately records the owner's Skoglyst → Breivika / 15:33–16:00 interpretation. Even filling those fields manually cannot upgrade the automatic classification. Other Travel to rows retain their source meaning.

Negative results were retained during development: the first run found a missed deadhead in example 1 and unresolved `t`/`N` source annotations in examples 1/2/6/7. The parser now retains those unknown annotations separately and parses the adjacent clock/identifier; the fasit was not changed to fit results. The first rejection test exposed pdfplumber wrapping its encrypted-password exception; the safe error mapping was corrected and rerun. Example 6 remains partial and the final qualification CLI deliberately exits **1**. Missing inputs and changed fixture hashes are **untested**, never supported. Deliberately deleting a row or changing header/time/endpoint/duty/provenance causes comparison failure.

Executed from `D:/IBE160`, with approved PDFs mounted read-only:

```powershell
docker compose build api
docker compose run --rm --no-deps -v "D:/IBE160/Eksempelfiler:/fixtures:ro" api python -m pytest -q tests/test_pdf_import.py
docker compose run --rm --no-deps -v "D:/IBE160/Eksempelfiler:/fixtures:ro" -v "D:/IBE160/Docs/evidence:/evidence" api python -m app.qualify_imports /fixtures --output /evidence/9-1-import-qualification.json
docker compose up -d --wait api
docker compose exec -T api python -m pytest -q tests/test_assessment.py
docker compose run --rm --no-deps api pip check
git diff --check
```

Build succeeded. Import suite: **22 passed** (2.63 seconds in the final pre-documentation run). Existing real HTTP/PostgreSQL suite: **18 passed** (0.99 seconds). `pip check`: no broken requirements. Qualification completes in about two seconds for all seven files; exact final timing is in JSON. The first recorded execution clock was **2026-10-20T12:15:18 UTC**; final fixture runs were around **12:25 UTC**, under ten recorded minutes. Preparation, implementation and evidence took under twenty minutes, comfortably within the four-hour experiment ceiling. No fixture was omitted because of the timebox.

Executed Python **3.13.16**, pdfplumber **0.11.10**, pdfminer.six **20260107**, pypdfium2 **5.14.0**, Pillow **13.0.0**, charset-normalizer **3.5.2**, cryptography **50.0.2**, cffi **2.1.1**, pycparser **3.11**. Versions were resolved using `pip index versions pdfplumber` and `pip install --dry-run pdfplumber==0.11.10`, then installed from the pinned lock. The [official pdfplumber documentation](https://github.com/jsvine/pdfplumber) confirms machine-generated text as its intended strength, byte-stream inputs, cropping/text extraction and explicit resource closing. No OCR or layout-generalization claim follows from these executions.

The worker processes bytes in memory and closes PDF streams/pages on success and errors. The parent always closes pipes and joins/terminates the spawned worker on return, rejection, timeout, cancellation or interruption. Tests exercise size **10 MiB**, pages **20**, time **30 seconds** (shortened deadline for deterministic timeout testing), output **2 MiB**, corrupt/encrypted/empty-image inputs, pre-cancel and in-flight cancel, and confirm no active children remain. Worker diagnostics are suppressed; no raw text archives or original-PDF scratch files are written. These bounds are not a hardened sandbox for arbitrary hostile private files. No private input was processed.

Recommendation: downstream story 10.1 may build review/correction around this observed HASTUS header/two-column layout, with examples 1–5/7 as the supported source-fact regression set and example 6 as a mandatory partial/owner-assistance case. Keep review, uncertainty and provenance visible; preserve all source rows and actual bus as unknown. Extended header clocks (24:00 or later), intermediate stop completeness, other document layouts, OCR, DST and application/API/database integration remain unqualified. No UI/API/database behavior changed; no commit or push occurred.

## Targeted review corrections

Added field-by-field location validation against normalized document/header/body-row evidence, including the final source page for continuation endpoints. Computed calendar instants/day offsets now link to their source clock, service date, header start/span/end and owner-approved timezone. Independently transcribed all eight approved pause-table groups and their row membership; comparison includes labels, kind, complete interval and member rows. Exported source order is checked against each independent consecutive row index. Fact origins use explicit rules for extracted, derived, owner-approved and unresolved values.

Mutation tests reject individually missing/invalid field locations, unrelated row evidence, missing calendar derivation links, missing/changed pause groups and wrong/duplicate source order. An independent synthetic text PDF verifies both standalone and trailing `t`/`N` annotations in exact order with unknown meanings and source locations. Adjacent pause rows with a gap or unresolved boundaries cannot merge. Targeted execution: `docker compose run --rm --no-deps -v D:/IBE160/backend:/app:ro -v D:/IBE160/Eksempelfiler:/fixtures:ro api python -m pytest -q -p no:cacheprovider --tb=short tests/test_pdf_import.py` — **76 passed (5.33s)**. This correction pass runs only import tests; root owns final full verification. Machine evidence was refreshed after these corrections, retaining six supported examples and partial example 6. The earlier 22/18-test results above describe the initial implementation checks, not a new full regression run.

## Final root verification

After corrections, rebuilt the image successfully and executed the documented commands: **76 import tests passed (3.17s)**, **18 real HTTP/PostgreSQL tests passed (0.89s)**, and `pip check` found no broken requirements. All matrix rows have executed passing coverage. The final JSON was regenerated at **2026-10-20T12:52:49 UTC** in **1.768 seconds**; CLI exit **1** intentionally records partial example 6. Implementation and oracle SHA-256 values match the final files. From the first recorded experiment execution at 12:15:18 UTC through this qualification run was approximately 38 minutes, within the four-hour ceiling. The earlier under-twenty-minute statement describes initial implementation, not the complete review/correction cycle.

Independent blind, edge-case and verification-gap reviews have individual verdicts in the implementation spec. All retained findings were corrected, with no deferred finding or outstanding blocker. Sprint story 9.1 is **review**; the build spec is **done**. No downstream application import acceptance is implied. No commit or push was performed, as required by the approved spec.

## Owner acceptance — 20 October 2026

After the bmad-walkthrough covering purpose, implementation, risks and optional manual observations, Jonas approved the change: "Klar til godkjenning, ser bra ut." Sprint story 9.1 is now **done**, superseding the review handoff above. The accepted outcome remains six supported examples and partial example 6; production import is not accepted by this decision. No additional manual command execution or test result is inferred from the approval. This closure changes documentation/tracking only; no application tests rerun, commit, push or next story.
