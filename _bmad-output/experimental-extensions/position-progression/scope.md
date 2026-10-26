# First-delivery boundary and route interface

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Proposals for V1.3.0, not approved behavior. This document owns scope, dependencies and product choices; [research](research/technical-position-progression-2026-10-26/research.md) owns external evidence and device uncertainties.

## Small useful delivery

On a manually selected passenger activity with a user-confirmed, compatible dated route association, the user explicitly starts position assistance and chooses an initial stop occurrence. Show a compact ordered stop list and an advisory “Anslått ved / Neste planlagte holdeplass” marker. Identify service date, direction and selected range. “Next planned” is not an assertion of actual arrival, boarding, departure or work performed. No map, audio or interaction while driving is required; preparation and correction are intended while stopped.

Keep three separate values: the confirmed route reference, the user's manual anchor/selection, and the computed estimate. Location can move only the last of these. It cannot select another activity, confirm another departure, start/end/abort a shift or record/alter completed, skipped, interrupted or unknown outcomes. Schedule time is context only. Reaching the last occurrence ends the estimate's range; it never selects a return trip or closes work.

First pilot: one qualified dated line-20 trip/range at a time, using the route extension's bounded P1 output. Its seven research-era dates are examples, not a promise of future coverage. Select a new named date window after V1 when needed. Full regional coverage, all variants and reliable loop tracking are not prerequisites: ambiguous cases must remain manual.

## Route dependency and proposed read-only contract

Current route SPEC/data-contract/matching/technical-addendum and CRN-E1 are drafts. They propose saved draft review and a frozen reference carried into the workday; no consumer interface is implemented. Do not mutate an active plan to attach new route evidence. An eligible previously reviewed reference is required; otherwise show manual mode.

| Input group | Minimum information required by progression | Missing/conflicting behavior |
|---|---|---|
| Private binding | Stable activity identity; authorized workday and reviewed reference revision; association review status and selected source snapshot. | Do not start against a stale selection, revoked access or a changed reference. No private identifiers leave for public lookup. |
| Dated identity | Provider/namespace/mapping mode, line ID, generic journey ID plus operating date and any required start discriminator; qualified dated ID if available. | Line number, current clock or privateCode alone cannot choose a trip. Known calendar/identity contradiction blocks assistance. |
| Direction/pattern | Selected pattern revision, source direction and per-occurrence destination display; inclusive first/last occurrence positions. | Do not reverse/deduplicate the opposite direction or equate headsign with final stop. |
| Ordered occurrences | Stable occurrence key within the versioned pattern, sequence, StopPlace and scheduled Quay/mapping where available; planned arrival/departure with service-day offsets and explicit instants. | Repeated visits to one quay remain distinct. Unqualified ordering/range/date stays manual. Timetable estimates cannot replace planned identity. |
| Position anchors — proposed addition | WGS84 latitude/longitude for each used occurrence, mapped quay/stop identity, coordinate kind, source/version/validity and quality/unknown status. | Route P1 does not guarantee these. Qualify Journey Planner/NSR mapping; a parent stop centroid is not silently treated as the boarding position. Missing/unsuitable coordinates disable automatic estimates for that portion. |
| Geometry — optional later | Directed geometry tied to this exact pattern/version and occurrence measures along it. | No map-matching claim without qualified geometry. Geometry never replaces stop order or resolves every parallel-road ambiguity. |
| Reference health | Source snapshot/retrieval/validity, matching evidence and user-confirmed versus unverified-reference status. | Expose stale source status separately from stale position. Unknown physical suitability or changed pattern requires manual mode/review, not automatic rematching. |

This is a proposed information contract, not field-name/API/database agreement. A user-confirmed unverified public reference remains unverified; assistance additionally requires a compatible date, unique selected occurrence range and qualified position anchors. Route's conceptual notice vocabulary is insufficient by itself. Its QF-02/04/05/09 outcomes qualify relevant identity/time/order claims; coordinate qualification is an additional gap. CRN-E1 draft review/carry-forward is the functional dependency; automatic notices, P2 catalogues and Entur live vehicles are not.

Approved V1's local loopback runtime does not establish a reachable, trusted HTTPS origin on the tablet. A later tablet experiment needs an explicitly qualified access/HTTPS configuration. Do not expose services or change deployment as part of this planning task.

## Conservative estimation proposal

1. On explicit start, bind a session generation to the selected reference and manual anchor. Feature-check secure context and Geolocation; request permission then use watchPosition. Clear the watch on pause/hidden/exit/access loss and reject callbacks from earlier generations.
2. Validate timestamp, reported accuracy and coordinate bounds before evaluating progress. Reject duplicate/out-of-order timestamps, stale/future-dated fixes, implausible jumps and a recent callback carrying an old measurement. Recompute freshness on every callback and visibility/resume, not solely with a timer. Detect device-clock discontinuity and reacquire.
3. Evaluate only nearby sequential occurrences within the selected range. Require several distinct fresh measurements, plausible displacement over elapsed time and consistent route context. Repeated measurements may share the same error; count alone is not proof of correctness. Use approach/departure hysteresis and optional reliable movement bearing. Source inbound/outbound is not a compass bearing.
4. Advance an estimate by at most one supported occurrence transition. Never jump to the nearest stop anywhere in the line or advance because the timetable says it is due. An observed approach followed by departure supports only an estimated passage. If stop regions overlap, another route segment fits, or passage evidence is absent, freeze the estimate and show uncertainty.
5. After a gap, tunnel, position jump or apparent detour, retain the last estimate as explicitly old and acquire a new sequence. Do not fill missed stops with assumed progress. A large re-anchor requires the user's explicit choice. Stops-only evidence cannot distinguish every parallel road; qualify suitable pilot sections and suppress ambiguous estimates.

Illustrative tuning seeds only: reject observations older than 15 seconds or with reported radius above 50 metres; require at least three distinct fixes spanning six seconds; hold at most six fixes and no more than 30 seconds in memory. These are proposed ceilings/windows for later experiments, not measured performance or universal acceptance thresholds. Even a 10-metre reported radius can be insufficient between close platforms. Define entry/exit distances from the qualified stop layout and field observations; no universal arrival radius is chosen now. Sparse updates may keep the display uncertain indefinitely, which is preferable to invented progress.

## Manual control, interruption and privacy

| Situation | Proposed visible behavior |
|---|---|
| Not started / permission denied / source unavailable | Manual list remains usable; explain the cause without repeatedly requesting permission. |
| Waiting / weak / stale / ambiguous | Text status plus measurement age/reported radius when known; no confident current-position marker and no transition. |
| Manual correction | Set the chosen occurrence, stop following, and retain that anchor until explicit “Fortsett posisjonsstøtte”. Do not undo it on the next callback. |
| Hidden page, screen lock, user pause | Stop assistance; on return revalidate access/reference and offer explicit resume with fresh measurements. No background continuity claim. |
| Reload / discarded page | Recover only authorized server-saved work and manual activity selection; assistance is off. Session-only stop anchor and estimate are lost, so request a new anchor and say so. Never reset to an inferred stop. |
| Activity/trip switch, expiry, logout, terminal closure | Stop watching and clear sample buffer; invalidate old callbacks. Preserve saved user facts under their existing lifecycle, never extend expiry. |

Process fixes in page memory; discard rejected fixes immediately, expire the bounded buffer and clear it on pause/session end. No default coordinate history, analytics payload, server upload, public API position query or private browser persistence. Saved manual route corrections remain in the route/workday layer; no sensor output overwrites them. “Local processing” describes this application's policy: browser/OS location providers may still use network services. No device-wide offline or zero-disclosure promise follows.

## Five material product choices

| Choice | Recommended provisional answer | Tradeoff / checkpoint |
|---|---|---|
| First operating mode | Foreground, opt-in advisory estimate on one confirmed trip. | Background/screen-off continuity is excluded; qualify Brave and Chrome separately. |
| Authority and recovery | Manual selection wins; correction pauses; explicit resume and fresh reacquisition. | More conservative recovery, no silent movement of manual choices. |
| Eligible route data | Require dated binding, ordered occurrences and qualified coordinates; geometry optional. | Some routes/sections stay manual. Review contract with route planning before implementation. |
| Persistence | Session-only samples/estimate/stop anchor; retain existing saved route/activity facts. | Reload needs a new anchor. Persistent stop-anchor recovery would be a separate scoped decision. |
| Accuracy policy | Prefer visible uncertainty and fewer advances; tune gates on the actual tablet. | No reliability/latency target claimed until measured. Reject the pilot if the device cannot separate its selected stops. |

Later possibilities: geometry-assisted disambiguation, wider route qualification, saved manual anchor, optional screen wake support, verified Entur vehicle supplement and separately researched background/native behavior. None is needed for this first increment. No epics/stories, navigation engine or full PRD/UX/architecture round is created here.
