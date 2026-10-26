# Behavior and authority

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## User direction versus proposed delivery

U1: start at the first stop of the trip/range actually driven, with relevant occurrence selection for mid-trip start/resume. U2: desired automatic reacquisition may skip multiple occurrences in the estimate, never manufacture observations. U3: manual correction is advisory evidence, protected when fresh and reassessable later. U4: save a bounded last-known stop for next-trip proposals. U5: NSR is the proposed authoritative coordinate source.

PP-D1 fixes manual post-interruption reacquisition for first delivery; this limits gap recovery, not ordinary GPS progression after a manual anchor. PP-D2 fixes reuse within one authorized workday/shift identity, including across midnight. These are user-set planning decisions, not implementation acceptance. A3 still covers untested tuning and mapping assumptions.

## Anchor and estimate

Keep immutable confirmed route reference, most recent manual assertion and mutable estimate separate. A manual choice sets occurrence and assertion time, resets evidence accumulation and briefly protects the estimate. It does not automatically pause indefinitely or require approval at every later stop. Explicit Pause remains available and suppresses sensing until Resume; Off requires a new explicit Start. Page visibility alone never reverses either user choice.

Only measurements acquired after that assertion contribute to overruling it. Reject old, duplicate, out-of-order, future-dated or implausibly jumping fixes; check uncertainty against the actual stop layout. During initial protection, collect bounded evidence without replacing the chosen occurrence. After protection, require several temporally distinct, coherent fixes and route order/direction context that clearly favor another occurrence over the anchor and other candidates. A growing mismatch weakens the old anchor; age reduces its weight but is never positive evidence for a new location. Correlated fixes, close roads or repeated Quays can remain unresolved.

Ordinary first-delivery following advances a supported next occurrence using approach/departure hysteresis; it never chooses a trip by nearest time/line/point. A far-away or backwards contradiction enters uncertain/re-anchor-needed status, retaining the manual assertion and offering correction. Qualified automatic relocation across multiple occurrences is the later U2 capability. Reassessment changes only the estimate; preserve the manual assertion's origin/time until its bounded replacement, without an indefinite audit trail.

Illustrative A3 seeds: initial manual protection 20 seconds, fix age at most 15 seconds, radius at most 50 metres, at least 3 distinct fixes spanning 6 seconds, sample buffer at most 6 fixes/30 seconds. These values do not qualify accuracy; tighter layout-specific limits may be needed. Protection expiry does not bypass evidence gates. Entry/exit distances, plausibility limits and confidence margin remain qualification parameters, not fixed product promises.

## Interruptions

On hidden page, material measurement gap, screen lock or access loss, invalidate the watch generation and stop using the prior sequence. Show old estimate with evidence age only while access remains authorized; otherwise hide private presentation. Clear transient fixes and discard late callbacks. First delivery: after authorized return/explicit Resume, require a relevant occurrence and acquire fresh fixes. Do not automatically continue on becoming visible or from fresh fixes alone. It may be any occurrence in the selected range, with no one-at-a-time catch-up requirement for that manual choice.

Later automatic reacquisition: search the whole selected range, compare repeated occurrences using fresh trajectory, direction and qualified geometry if available. Require one clearly supported candidate; clock/anchor age/one nearby point cannot disambiguate a loop. Relocation 3→6 is allowed, with gap flag and no observed-passages record for 4/5. If evidence remains ambiguous, request manual selection. End of range never selects another trip or closes work.

## Saved last-stop proposal

First delivery uses the PP-D2 same-workday boundary. PP-T1 proposes one server-owned latest-stop record per workday. Save an explicit manual choice or a qualified estimated stop change, replacing the bounded record rather than appending a trajectory. Stop identity/time/provenance is still sensitive private workday data. It follows owner/session/expiry checks, expected revision and operation retry semantics. Do not send it to public APIs or store it in private browser persistence.

Persist stop identity, occurrence/trip/reference context and evidence/assertion time, plus savedAt separately. A delayed save must not make an old observation appear fresh or overwrite a newer anchor. Bound/coalesce estimate writes; an uncertain save keeps the original operation for lookup/retry and is visibly unconfirmed. On unavailable service, only in-memory state remains; after reload only acknowledged saved anchor can be proposed.

Offer the saved anchor when the user explicitly selects the next confirmed trip. Resolve identity into that trip's selected occurrence range and ask the user to accept a unique proposal. Preserve original origin/time; user acceptance creates a new manual assertion time without changing the old measurement time. Duplicate matches need occurrence choice; no match keeps manual start. The previous sequence number has no authority in the new pattern.

Anchor expiry cannot exceed its owning workday's fixed deadline (including closure shortening); switching trips, saving again, login or retries never extend it. No writes after terminal closure; access denial clears presentation and stops assistance. Deletion/expiry purges the anchor and related receipts. The same workday identity remains eligible across midnight while authorized and nonterminal; the calendar date is not a reset or extension trigger. A different workday cannot reuse it, even on the same calendar date. Cross-workday reuse is outside first delivery; no copying to extend a lifetime.

## Failure states

Route validity, dated identity, occurrence range, quay mapping and coordinate validity are independent of permission, fix age, accuracy and trajectory confidence. Show both dimensions when relevant. No route coordinates: manual-only affected portion even with an excellent fix. Good route data plus stale fixes: frozen old estimate with measurement warning. Source refresh compares changes; it never rewrites frozen route facts. A location-derived estimate never marks a planned/actual stop as served, or records completed/skipped/interrupted work.

Reuse foreground permission/start/stop and access behavior from the existing research. Buffer clears on pause, trip change, logout and terminal closure. No raw fix history on the server, in analytics or persistent browser storage; the bounded saved stop record is the explicit exception to the original session-only proposal. Off stops the watch, invalidates callbacks and clears transient fixes/estimate immediately. It retains only the already acknowledged anchor under the workday deadline and cannot initiate new saves; an already-sent uncertain operation is resolved through existing authority checks, never treated as canceled solely by Off. No saved anchor restarts sensing on reload. User-data deletion/expiry remains the existing parent action, not an incidental effect of Off.
