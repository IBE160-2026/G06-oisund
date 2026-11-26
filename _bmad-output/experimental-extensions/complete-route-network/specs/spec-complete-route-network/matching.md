# Matching and review rules

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Draft A3/A5, supporting CAP-2–6. Basis: research.md §§2–5; no real shift-to-public crosswalk has been established.

## Input and evidence

Match the stable imported activity, not its current list index, public line number or vehicle duty. Keep imported raw line/trip number, source/date interpretation, known planned times and places, field uncertainty and subsequent manual corrections. Passenger trips are eligible; breaks, bus changes, transfers and private deadheads are not forced into a public departure.

A candidate identifies source namespace/mapping mode, scoped public line, ServiceJourney (or equivalent source journey), service date, snapshot and ordered occurrence range. Compare known planned start/end instants and mapped places/occurrences, source direction/destination where available, calendar applicability and relevant variant. Evaluate aimed/planned times; real-time estimates do not repair a planned-time mismatch.

The observed Entur privateCode is a **qualification lead**. Neither equality with a shift trip number nor an ID suffix proves a mapping. Retain the two identifiers separately and record the evidence for any crosswalk. A missing crosswalk does not prevent an explicitly labelled manual reference choice or evidence-based candidate search; it prevents treating the number as an authoritative join rule.

A5 proposes exact agreement on the available qualified planned-time and mapped-occurrence evidence before calling a candidate unique. No silent fuzzy place mapping, tolerance window or nearest-time automatic choice. Unknown facts remain unknown and lower the supported claim. If exact matching is too restrictive, Q5 may approve a visible bounded ranking/tolerance policy later; ranking still does not confirm identity.

## Outcome vocabulary

| Outcome | Required meaning | Driver path |
|---|---|---|
| Unique proposal | One compatible journey **and occurrence range** in a closed, recorded line/operator/date search scope; no unresolved contradictory known facts. | Show source, date, endpoints, headsign and evidence; explicit confirm, reject or correct. |
| Ambiguous | Multiple plausible journeys, variants or occurrence ranges. | Present distinguishing facts; choose one explicitly or leave unresolved. No first-result default confirmation. |
| Not found within checked scope | Search completed against adequate known coverage; no compatible departure. | State the checked interval/source; correct input or retain manual/unknown facts. Never claim the whole network has no service. |
| Unresolved | Date/ID/place/calendar semantics or search completeness insufficient; one result from an incomplete search is still unresolved. | Explain missing evidence; allow manual input or an explicit unverified reference choice. |
| Unavailable | Source or validation failed, including GraphQL errors in an HTTP-success response. | Keep existing input/confirmed association, expose retry/source status. Do not convert failure into not-found. |
| Stale reference | Source evidence is outside its declared freshness or validity policy. | Show age/reason; a prior confirmed association remains traceable, while new matching is qualified as stale/unresolved. |

“User confirmed association” is a separate review status, not a claim that the source crosswalk, network completeness or actual driving is independently verified. Store whether the user confirmed a unique proposal, selected an alternative or accepted an explicitly unverified reference. A hard known calendar/time/occurrence contradiction cannot be hidden by that label; correct the input/evidence or keep the reference separate and incompatible.

## Review behavior — proposed first-delivery boundary

In draft review, show imported, externally proposed and manually corrected facts distinctly. Provide confirmation even for a unique proposal (A3). A choice may suggest direction, destination and stops; it must not erase the imported baseline or an existing manual value. Show differences and let the driver keep, replace or leave a field unknown. Reject/cancel preserves saved facts and input according to existing navigation/recovery guards.

Editing a match-driving fact (service date, scoped line, time or occurrence mapping) makes the previous proposal stale and requires new comparison; the old evidence remains explainable. Confirming a proposal does not start a shift, select a physical location, complete an activity or guarantee source freshness. Keep the source-derived association distinct from overall plan confirmation.

For P1, confirm the association before overall plan confirmation. Carry that reviewed evidence forward as a read-only reference for the workday. Do not enrich an activated or terminal plan in place. A missing match does not block the existing manual import/confirmation path by itself; existing V1 validation still applies to the manually entered plan. Later active-plan enrichment requires a separate product/lifecycle decision.

## Variants, loops and partial journeys

Use the selected journey's actual pattern, not a union of the line's stops. A shift segment records first and last occurrence positions in the full pattern; it is not automatically a different departure. If a repeated stop pair admits more than one subrange, keep the match ambiguous until time/order or user choice resolves it.

Preserve both stop-place and scheduled platform IDs, and repeated visits to the same platform. Do not reverse the other direction's list or deduplicate stops. Source inbound/outbound labels are not compass bearings. Destination displays may change along the journey and need not equal the last stop's name: the observed Stakkevollan display with Skattøra endpoint is a concrete seed case. A partial segment may have a local end while the vehicle headsign names the onward destination.

## Changes after source refresh

A refreshed catalogue yields a proposed comparison, not a rewritten choice. Preserve the chosen snapshot, operating date and occurrence range. A removed ID, changed calendar, cancellation, replacement or changed stop pattern is an explicit difference; do not silently transfer confirmation to a replacement. Retain manual corrections and explain unresolved links within the workday's original retention bound. Confirmation of newer evidence is a new attributable user action where the permitted lifecycle allows it.
