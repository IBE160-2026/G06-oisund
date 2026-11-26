# Proposed route/position handoff

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Conceptual contract v0, not a wire API or implemented schema. Technical integration and bounded persistence proposals are in [technical-addendum](technical-addendum.md); user-set boundaries are in [decisions](decisions.md). Read-only reference: complete-route-network SPEC, data-contract, matching, technical-addendum and CRN-E1 at commit 7cada9d2e66af9806358f582bc8ea459321a6563. They provide proposed draft association/frozen carry-forward, not this coordinate or anchor facility.

| Group | Required meaning |
|---|---|
| Binding | contract version; private workday/activity identity; reviewed association revision/status; source snapshot; selected inclusive occurrence range. All private identifiers stay private. |
| Dated journey | provider, namespace, mapping mode, line ID, journey ID, operating date, required source start discriminator, qualified dated-journey ID if available; calendar evidence and timezone. |
| Pattern | pattern ID/version, source direction and per-occurrence headsign; ordered distinct occurrence keys even when a Quay repeats. |
| Calls | occurrence key + sequence, original ScheduledStopPoint mapping where supplied, StopPlace and concrete Quay IDs, boarding/alighting flags; separate planned arrival/departure, original service-time/dayOffset and derived explicit instants. |
| Coordinates: added here | coordinateSource=Entur NSR; source URL, fetchedAt, source update time if known, NSR snapshot/mapping revision; separate StopPlace/Quay versions and validity; coordinate kind, WGS84 latitude/longitude, known/unknown quality. Bind each occurrence to a qualified coordinate reference. |
| Geometry | optional directed geometry ID/version and occurrence positions along it; absent geometry limits supported disambiguation, not stop order. |
| Route health | compatible dated binding and unique selected range, complete/partial/missing coordinate coverage, source age/validity and unresolved mappings. Unknowns remain explicit. |
| Transient fix | acquisition timestamp, receivedAt, lat/lon, reported accuracy, nullable movement bearing/speed, watch generation; no persistence requirement. |
| Estimate | journey+pattern revision+occurrence, evidence time, confidence/status, basis manual/GPS, interrupted/reacquired flag. It is advisory, not a service event. |
| Saved anchor | owner-derived workday/shift identity (independent of calendar date), revision/operation identity, StopPlace/Quay, source journey/date/pattern/version/occurrence, coordinate-reference version, evidence/assertion time, origin manual/GPS, savedAt and fixed expiresAt. Raw fix coordinates are unnecessary. |

NSR is the proposed authority for coordinate facts; the selected route snapshot owns occurrence order. Join scheduled quay/stop IDs through an explicit versioned mapping. Do not infer identity from names or substitute a StopPlace centroid for a Quay position. A different Quay in the same StopPlace is a broader candidate needing clarification. Renumbering/replaced IDs require a qualified crosswalk or manual choice.

Validate coordinate validity at the relevant dated call time and preserve its version together with the route snapshot. Refresh cannot silently replace a confirmed pattern or coordinate anchor. Unknown historical validity is a data qualification gap. These requirements are additions to this extension; no claim that route P1 already supplies them.

Eligibility requires an explicitly confirmed compatible dated reference, unique selected range and qualified coordinates for the portion being estimated. A user-confirmed unverified source choice stays labelled unverified; known contradictions block automatic support. Geometry, regional complete coverage, automatic notices and Entur live vehicles are optional later capabilities.

Anchor remapping returns unique-occurrence proposal, ambiguous-occurrences, no-match or unavailable/invalid-data; its input includes the new trip's range/version, never the old sequence as the join. A same-workday check precedes remapping, including across midnight; a different workday never receives the record. The new journey keeps its own operating date and explicit call instants. Measurements can be unavailable independently. No suitable range/map means manual mode, not a guessed fix.

Tablet access needs separately qualified trusted HTTPS and the existing online private lifecycle. Keep stable IDs, revisions, save recovery, retention, immutable imported facts and fictional/private separation. No new service, database migration or active-plan enrichment is specified for execution in this task.
