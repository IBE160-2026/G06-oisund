# Specification self-validation

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Date: 2026-10-26. Verdict: **PASS AS FIRST DRAFT; owner decisions pending; not implementation-ready or accepted V1 scope.** This is bmad-spec's own two-pass document validation plus mechanical consistency checks, not a code review, architecture exercise or product test run.

## Pass1 — Coherence

| Spec Law | Result |
|---|---|
|1 Intent and success| PASS: CAP-1 through CAP-7 each have both |
|2 WHAT, not HOW| PASS: kernel describes behavior; protocol/evidence and mapping details sit in companions; no database/API architecture selected |
|3 Constraints bend decisions| PASS: authority/expiry, exact identity, uncertain completeness and source/manual separation rule out silent inference/overwrite |
|4 Non-goals| PASS: complete routes/GPS and other sources deferred; implementation/architecture/stories excluded from this run |
|5 Concrete success| PASS as draft: invariant demonstrations and independently labelled evaluation defined; Q-6 numeric thresholds remain proposed |
|6 Stable unique IDs| PASS: seven new IDs, no prior spec or retired IDs to reconcile |
|8 Lean contract| PASS: kernel and five content-named siblings; operational detail isolated in .bmad-runner |

Correction made during validation: narrative spacing; no behavioral meaning or capability identity changed. Pending Q-1–Q-7 are explicit, not silently filled. Pilot source choice is proposed, not accepted by research or draft existence.

## Pass2 — Preservation

| Load-bearing input | Contract destination / disposition |
|---|---|
| User: existing workspace/isolation,experimental status,no V1 promotion | SPEC constraints/non-goals; compatibility; .bmad-runner routing evidence |
| Completed research: Entur documented support vs three partial observations | source-lifecycle evidence boundary; adopted research and its referenced digests |
| Complete pagination,updates,recovery;MoreData not completeness | CAP-1,6; source-lifecycle; G-1/G-2 |
| Exact line identities,planned calendar validity,unknown direction/DST | CAP-2; relevance-rules; catalogue and Q-4 |
| Stop-only,broad,no-line,uncertain scope | CAP-3; explicit review actions/inbox and Q-2; G-5 |
| Source fields/clocks,not-seen/expired/closed/withdrawal | CAP-4; source-lifecycle; catalogue; research preserves unverified TRO transitions |
| Manual web/SMS,corrections,checks,manual end | CAP-5; compatibility; G-4 |
| Partial/unavailable/stale retained data | CAP-6; source-lifecycle; Q-3 |
| Duplicates/conflicts/provenance | CAP-7; relevance-rules; compatibility |
| Small future mapping boundary,no automatic full-network dependency | compatibility; SPEC non-goals; deferred precise route matching |
| Independent measurement,benefit uncertainty,effort/stop conditions | qualification; Q-6/Q-7 |
| SCOPE-02 and committed manual baseline;later local11.5/11.6 not accepted | compatibility; scope absorbed as sources entry, no source edits |
| Research broad pre-coding/contact/coverage recommendations | Deliberately narrowed by current user: dependent gates allow controlled examples and targeted contact; no regional-completeness gate. Research is evidence, not product approval. |
| Other provider/format findings and uncertainty | Adopted research retains GTFS/ET/VM,Vegvesen,source-access/terms and staleness evidence; source extensions deferred |

**Wrapper-only content:** establishment and research execution chronology, greeting/output ceremony, research-brief scaffolding and old next-step advice do not define product behavior. README/source-map/bmad-workflow are read for authority/routing but not listed as contract companions. Existing files remain untouched. Current task ends after spec validation, without architecture/story invocation.

## Mechanical checks and limitations

validation.json records exact destination, branch/HEAD, capability structure, companion/source paths, marker coverage, original-input hashes and Git path isolation. The runner uses only extension-local TOML and read-only installed resolvers; actual resolved spec destination was checked before SPEC writes. No official bmad-spec validator CLI exists in the installed instructions: the required validation is the two judgment passes above. Qualification gates are future work, not falsely reported as passed. Open numeric/product choices prevent a final pilot-acceptance verdict.


## Epic-planning update — 26 October 2026

The earlier report describes the initial spec run. Current continuation passes both Spec validation passes as draft. Seven capabilities and adopted research are preserved. See [planning validation](../../planning/validation.md) for four stories/32 criteria and remaining gates. No final owner approval or ready-for-dev claim.
