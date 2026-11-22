---
title: 'Preserve unresolved connections in the dated NVDB area graph'
type: 'bugfix'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

The Tromsø NVDB area reconstruction drops lane-free connections. At Flyplassvegen this turns a two-arm choice into an apparently unique continuation and can allow an unjustified 300 m warning. Preserve each geometrically usable unresolved connection as a possible road in both directions. Preserve usable endpoints as blockers when geometry cannot be used. Join successors by exact NVDB node identity.

A graph edge with undecided direction carries no speed value. A known direction may carry a candidate registered limit only when dated, unrestricted type 105 intervals cover the entire edge with one value and no relevant source conflict. Keep internal changes, variable limits and uncertain field applicability explicit. Store the source identities and distinguish research output from a runtime-approved package. The rest of the Tromsø field objective remains in scope.

</frozen-after-approval>

## Implementation Notes
- The source graph now retains both possible orientations of valid lane-free geometry. It carries unresolved endpoint references through graph joins when the geometry cannot be used.
- Dated scope checks use NVDB version dates and the explicit effective-date properties. General type 105 placements can provide a registered candidate value for a fully covered edge. Field-specific placements, internal transitions, gaps, conflicts and overlapping type 721 remain identifiable as unresolved.
- Replayed the 30 November and 10 December public archives against their page hashes. Each graph contains 19,667 directed candidates. It preserves both outgoing arms at node 3251245 and records the Flyplassvegen connector as unresolved. The coverage audit also found six geometries above the browser's 256-point limit.
- The data remains an offline research graph. Deployment, versioned area packages, live temporary restrictions and browser access through the authorised app are separate outstanding checks in the field objective.
- Re-collected both endpoint dates with type 977. Each archive contains 830 direction objects. The compiled graphs are identical with 18,615 directed candidates and 17,168 fully covered static records. R4 keeps both choices. The explicit, fully dated one-way placement makes the Flyplassvegen exit forward-only, and the child speed remains unresolved while carrying the exact parent's registered 50 km/h as evidence. A parent limit or the normal tunnel value does not establish the position of a sign or the current variable limit.
- Final verification passed 86 NVDB/road tests in an isolated container, 19 motion tests and the TypeScript/Vite build. Offline replay checked each response page digest, all successor node joins, unresolved speed results, the airport branch and the single-interval self-loop in both archived dates.

## Review Triage Log

- Medium, fixed. The collector includes type 977. Complete, consistent dated link placements establish one-way travel. Partial, contradictory or field-specific results retain both possibilities without a speed value.
- Medium, fixed. Child edges carry exact parent placement, source version and speed evidence. Incompatible or unresolved parent evidence masks a direct candidate. The parent value stays distinct from the child display candidate.
- Medium, fixed. A same-direction self-loop remains a continuation. Its exact reverse is excluded from forward lookahead.
- Medium, fixed. Invalid source fractions are rejected before clipping. A malformed active placement leaves the affected edge unresolved.
- Medium, fixed. The matcher test includes both orientations of a geometric unknown exit and continuous fixes past the decision. It also exercises an exit retained as an unavailable successor in a partial package.
