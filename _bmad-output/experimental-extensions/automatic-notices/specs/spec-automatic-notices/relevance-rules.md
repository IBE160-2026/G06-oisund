# Relevance and review rules

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Draft behavior for CAP-2,3,7. Automatic nomination establishes possible relevance, never dispatch authority or confirmed travel on a road.

## Identity and planned time

P: Use the currently authorized confirmed plan revision. Compare provider/codespace and reviewed canonical line binding against exact printed line; mappings have provenance, version and applicable dates. Never fabricate LineRefs from numbers. Keep 20, 020, X20, 20E distinct unless a reviewed alias explicitly binds them; same number under a different operator cannot match.

P: Use planned activity instants/calendar dates in Europe/Oslo, not service-date-only, actual start, selected activity or GPS. Evaluate every validity window. Q-4 proposes half-open intervals: touching endpoints alone do not overlap; a point-time activity uses its instant. Missing/ambiguous offset/DST, reversed intervals or missing times yield uncertain-time results. An absent end is open-ended validity, not indefinite freshness. Preserve nested stop/line/journey qualifiers.

P: Only reliable explicit incompatibility can exclude by line/time/direction. Unknown direction, printed trip/destination or proximity cannot justify exact matching or automatic rejection. A plan's direction text is not a provider direction key. Unsupported selectors remain explicit uncertainty.

## Classifications

| Class | Evidence | User-visible claim |
|---|---|---|
|Line/time candidate| Qualified exact line and known overlap | Possible relevance; unresolved direction/stop qualifiers shown |
|Review required| Missing/ambiguous field, mapping or qualifier | Explain why relevance is undecidable |
|Broad context| Explicit compatible network/area/all-line scope | Day-level context without exact trip assignment |
|Known outside scope| Reliable incompatible pilot identity/mode/geography/time | Excluded with inspectable reason |
|User-associated| Explicit action for activity/source revision/plan revision | User-confirmed association, not provider-confirmed applicability |

P: All automatic nominations remain possible even with exact line/time. Explicit association records user/time and revisions; it does not mark source checked, select/complete an activity or change actual facts. Material source/plan changes preserve the earlier association but require reassessment; never silently carry its confirmed badge onto changed facts.

## Stop-only and broad review flow

P: Evaluate scope before line filtering. Stop-only messages with verified pilot-stop/endpoint bindings enter review. Giæverbukta situation 426 demonstrates why no LineRef cannot mean irrelevant. StopPlace and Quay are distinct; names alone do not merge them. Line messages with nested stop restrictions stay conditional when today's plan lacks stop sequences.

P: Explicit compatible all-network/all-line messages become broad context. Empty line lists mean unknown scope, not all lines. Large-area messages remain broad/uncertain unless a qualified geography binding excludes them. TRO includes more than urban Tromsø; ferry line 191 is outside only after reviewed pilot mode/identity evidence establishes incompatibility.

P/Q-2: Proposed inbox includes mapped pilot-stop notices, compatible explicit broad notices, and a separate unresolved-scope TRO group with counts, reasons, source and time. Unknown area/line/stop items remain reachable rather than silently discarded for noise control. Grouping/paging is allowed with honest totals/continuation. Known outside-pilot items may be separated with reasons.

P: Review actions are open original source, inspect affected facts, associate with named planned activities, keep day context, dismiss for this plan with reason, or leave unresolved. Dismissal is reversible/local, not source closure. Store content/plan revision context. Material changes prompt reassessment while preserving old dismissal and any manual ending. No decision means unresolved, never implicitly irrelevant.

## Overlap and conflict

P: Similar titles alone do not merge events. Explicit source links/IDs plus compatible time/place/scope may propose a group. Linking manual records requires explicit user action; every contribution keeps identity/content/clocks. Show contradictions side by side; last fetched is not automatically true. Unlink without data loss. One contribution's closure cannot close the others.
