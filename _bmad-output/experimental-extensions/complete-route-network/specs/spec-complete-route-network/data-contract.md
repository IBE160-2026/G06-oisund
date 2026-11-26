# Data, service time and identity interface

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Conceptual draft supporting CAP-1/2/4/5/6/7. This defines information to preserve and observable meaning, not tables, HTTP endpoints, framework selection or a shared architecture decision. Basis: research.md §§2, 4, 6–7 and its referenced specifications.

## Information distinctions

| Concept | Facts that must remain distinguishable |
|---|---|
| Source/snapshot | Provider, namespace, identifier mapping mode, source URL, retrieval time, original source-import/update time (nullable), generation/ETag/hash where available, profile/parser revision, validity and coverage manifest revision. File generation is not provider planning freshness. |
| Line and responsibility | Namespaced line identity versus public number; authority versus operating company. Retain operator exceptions at journey level. Preserve leading zeros/case in source identifiers. |
| Journey and pattern | Generic ServiceJourney/equivalent identity versus concrete operating-date instance; pattern identity/version; optional public/private codes and their distinct provenance. Include source start-time discriminator if required by that format. |
| Stop occurrence | Pattern position plus scheduled platform/quay, parent stop-place, original scheduled-stop-point reference/mapping where available, names, boarding/alighting permission and source destination display. Repeated platform visits retain different positions. |
| Planned time | Original encoded time or service-day seconds, day offset, operating date, source timezone/context, calendar/exception evidence and separately derived calendar instant with offset. Arrival and departure remain distinct. |
| Reviewed association | Stable private activity identity, selected public journey/date/snapshot and occurrence range, matching evidence/outcome, explicit review status/actor/time, imported baseline and manual corrections. These are private data, not part of the public identity interface. |

Unknown optional metadata is explicit; do not invent a source timestamp, operator or platform. Mandatory unresolved identity/order/calendar references prevent completeness or automatic unique-match claims for the affected part. A geometry/polyline can reference a pattern but never substitutes for ordered calls. Geometry is optional in P1 and a separately reported dimension later.

## Operating date and calendar rules

A journey instance belongs to a declared **operating/service date**, which may differ from the calendar date of a call. Preserve 25:30 or time 01:30/dayOffset 1 as source facts instead of normalizing away their service-day meaning. Do not infer a day from clock order. Apply weekday patterns, explicit additions/removals, validity limits and calendar exceptions before declaring a date eligible.

Follow each input format's service-time axis and inherited timezone. Research documents Nordic noon-reference rules and GTFS's service-day-noon-minus-twelve-hours origin; do not independently parse every passing time as a local wall clock or assume source-shift time semantics match either format. Europe/Oslo is the pilot context, not a universal hardcoded timezone. Retain explicit offsets for derived instants, including after-midnight calls beyond the final horizon date.

The retained night case is time 01:30/dayOffset 1 on service date 2026-10-31, calendar departure 2026-11-01 01:30+01. The 2026-10-24 instance leaves 2026-10-25 01:30+02, before the autumn repeated hour. These observations do not qualify spring gaps or both autumn 02:xx occurrences. Until QF-04 supplies independently expected instants, such cases remain visibly unresolved; ordinary well-qualified dates may still be used in a bounded experiment.

## Updates, confirmation and retention

Keep public reference evidence and private workday links under separate ownership/retention. Preserve enough public facts to explain a confirmed choice even if live exports no longer contain that date. Research's latest exports trim history; no historical availability guarantee follows from a URL. Public retention duration and storage implementation remain Q7, not an implicit permanent archive.

Private association/correction copies follow existing owner checks and fixed workday expiry. Parent draft expiry is creation plus seven days; confirmation fixes at most planned final end plus seven days, and closure may shorten that bound. Viewing, login, retry and catalogue refresh cannot extend it or recreate expired work. Do not retain raw shift originals or private payload logs, send full shift documents to public APIs, create a persistent private browser cache or expose real records through fictional demonstration.

A6 proposes checking source metadata when preparing and at most one scheduled regional download per day where allowed, fetching changed/needed data rather than repeatedly re-downloading it. A successful check timestamp is separate from file generation and original provider update. After 24 hours without a successful catalogue check, new proposals are labelled stale; known validity gaps can make them unusable sooner. A check does not make old provider data newly published. This default is awaiting Q6; it is not an Entur freshness guarantee or a live disruption policy.

## Proposed read-only identity vocabulary v0

This is a minimal information contract for a future notice consumer, not an implemented API or agreement binding the other extension. Field names/version and wire representation remain Q8. No transport or database design is selected.

| Reference | Required meaning | Unknown/partial behavior |
|---|---|---|
| Context | Provider/source namespace, mapping mode (for example mapped-static versus original), snapshot/reference revision and applicable validity. | Do not compare raw IDs from incompatible modes without a qualified crosswalk. |
| Line | Namespaced line ID; public line code is a separate display value. | A broad manual line tag alone does not establish a precise source line ID. |
| Stop | Stop-place ID and optional scheduled platform/quay ID; occurrence index only when tied to a pattern/journey. | Stop-place scope stays broader than platform scope. Repeated occurrences are not collapsed. |
| Departure | Generic journey ID plus operating date and any required source start discriminator; optional qualified dated-journey ID and pattern/occurrence range. | No generic journey-to-current-calendar-day guess; unresolved mapping remains unresolved. |
| Association evidence | Scope (line/stop/journey/occurrence), mapping status, provenance and optional source crosswalk version. | Consumer keeps broad candidates broad; no exact relevance or “no disruptions” claim from missing matches. |

Illustrative research identity: provider TRO, line `TRO:Line:1_20`, journey `TRO:ServiceJourney:20_260918105162575_6600`, operating date 2026-10-31, scheduled origin `NSR:Quay:95300`, parent `NSR:StopPlace:55683`. This is one observed dated reference, not an ID construction rule.

Do not include private workday IDs, shift numbers, driver identity, corrections or account/session credentials in this public reference vocabulary. A notice association still needs its own source selectors/validity and qualified static-to-realtime mapping; GTFS, NeTEx and original-system IDs are not assumed equivalent. Research lists TRO SIRI-SX support but not TRO GTFS-RT alerts in that table; those claims require rechecking before an actual notice adapter. Neither extension depends on the other for its first useful increment.

## Position/progression boundary

Planned calls, current clock time and a realtime schedule flag cannot establish location. A later progression proposal would need vehicle/GPS observations with identity, observation timestamp, accuracy, age, mapping uncertainty, failure behavior and user correction in the same scope decision. No such behavior or positioning stream is included in this draft's first delivery.


## Current P1 update policy

The short CRN-E1 plan narrows A6 to preparation/explicit bounded API checks and the provisional24-hour new-proposal age rule. Earlier scheduled regional-download advice is for deferred P2, not a background P1 feature. [Technical addendum](technical-addendum.md) and [decisions](decisions.md) define bounded public query evidence versus selected private copies; Q7 rights/actual retention limits remain pre-persistence checks. No private lifetime is extended.
