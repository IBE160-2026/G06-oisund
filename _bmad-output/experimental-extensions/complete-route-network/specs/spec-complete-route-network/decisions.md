# Decisions, assumptions and source reconciliation

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

First draft, 2026-10-26. The user's scope/authority constraints are binding for this document task. New product defaults below are proposals requiring review; completed research recommendations do not automatically become architecture decisions.

## Prioritized owner decisions

| Question | Proposed answer and reason | Status / when it matters |
|---|---|---|
| Q1 — what is the complete pilot? | **A1/A2:** P1 line 20; P2 exactly lines 20/24/28/42, whole published journeys and extensions, all actual operators. This is a concrete, configurable pilot with lower qualification cost than all city lines. Expand only through an explicit manifest revision. | Proposed. Confirm first. Exact operator list and line 28 ID are QF-01 evidence tasks, not guessed values. Complete means this pilot, not all Tromsø buses. |
| Q2 — what horizon? | **A1/A2:** seven named consecutive service dates for P1; rolling 28 for complete P2, with calls after midnight carried beyond the last date. Covers weekdays/weekend while making completeness measurable. | Proposed, not a source guarantee. Confirm before claiming coverage; unavailable dates remain partial. |
| Q3 — how should suggestions enter the plan? | **A3:** first use draft review and require an explicit confirmation even for a unique proposal. Preserve manual values and carry a reviewed association forward read-only. This avoids silent changes and expansion of active-plan revision. | Proposed. Confirm before interaction/implementation design; no active/terminal enrichment approved. |
| Q4 — which acquisition progression? | **A4:** targeted Entur planned-service lookups to qualify matching; then assess regional NeTEx with appropriate NSR versions for P2. Keep GTFS if the required content/ID comparison finds no unacceptable loss. This follows research without adopting a parser/storage architecture. | Research-backed proposal. Confirm direction; exact technology/tool/storage decisions remain later. |
| Q5 — what establishes a match? | **A5:** date/coverage-qualified exact evidence first; privateCode is supporting evidence until QF-03. Never use number equality or nearest time alone. Permit explicit unverified manual references. Add visible tolerance/ranking only after representative examples justify it. | Proposed. Needed before automatic uniqueness claims, not to inspect public facts or constructed controls. |
| Q6 — how fresh is usable data? | **A6:** check when preparing; at most one scheduled regional download/day where permitted; mark new proposals stale after 24 hours without a successful check. Keep original source age separate and preserve prior choices. This is a simple conservative experiment default. | Proposed, not measured suitability or an Entur warranty. Confirm threshold/cadence before live matching claims; known validity gaps override age. |
| Q7 — how long to retain public evidence? | Separate public snapshots from private associations. Prefer current plus one prior public version for comparisons, with only the necessary selected public facts carried with a workday under its existing expiry. Do not create an indefinite private history. Exact public retention/storage and licence conditions require later architecture qualification. | Recommendation, not an implemented retention policy. Set before durable snapshot integration. No change to existing private limits. |
| Q8 — what can the notice extension consume? | Use the v0 read-only source/line/stop/dated-journey/occurrence vocabulary; no transport contract or bilateral dependency yet. Ratify field names/version and actual source crosswalks together only when a consumer is planned. | Open interface agreement; not a blocker for P1. Other extension remains unchanged. |

## Research facts versus proposals

Adopted research.md is the evidence entry point, with underlying public requests/digests available there. It establishes selected public IDs, ordered planned calls, per-occurrence destination displays and time/day-offset examples; it does not establish complete pilot coverage, universal ID stability or a source-shift number join. Its two verified conceptual claims are not two qualified implementation components. Preserve the single-publisher and common-upstream caveats.

API-first, regional NeTEx/NSR and GTFS fallback are evidence-backed recommendations. The four-line pilot, seven/28-day bounds, mandatory first-delivery user confirmation, exact-evidence default and 24-hour staleness rule are **A1–A6**, introduced for this draft and not yet owner-approved. They can be revised by appending decisions to the spec memlog and re-deriving the package with stable CAP IDs.

## Parent contract and conflicts

The adopted V1 architecture/UX pair governs unchanged parent behavior: stable activity identities, explicit lifecycle, planned/manual/unknown distinctions, revisions/retry, ownership, expiry, private/demo separation, readable Day/Night/focus and retained input. No V1 status or historical epic numbering changes.

The parent deliberately defers transit ports and stop displays **within approved V1**. This draft proposes them only in this separately labelled extension; that is a scope difference requiring a later approved extension design, not a silent override or a reason to edit the parent now. Automatic progression and active-plan revision remain outside the first increment. The parent UI wording against stop rails/maps prevents implying live location; a future extension stop overview must be visibly planned information and separately designed before UI integration.

The source-map records later main-only 11.5/11.6 notice/recovery amendments; these were not copied, revalidated or declared current implementation here. Before later integration, inspect the then-accepted parent baseline explicitly. Inherited mandatory notice-URL wording lags the accepted SMS correction described in that map; this route spec does not settle notice requirements or reproduce that stale field rule.

Research records: empty datedServiceJourneys is not absence of static service; observed date min/max is not continuous coverage; Svipper widget/PDF validity disagrees; its night-column alignment and map/planner content were not fully qualified; service-time examples do not qualify both DST transitions. Those remain QF-01/04/05/09 tasks, not silently filled assumptions.

## Continuation boundary

Resolve the highest-priority owner choices by updating this spec's append-only memory and re-deriving it. Do not run architecture, story breakdown, implementation or a new broad research workflow merely because another workflow recommends a next step. Any later authorized workflow must keep outputs in this extension and recheck actual routing; the separate branch alone does not prevent integration-path collisions.
