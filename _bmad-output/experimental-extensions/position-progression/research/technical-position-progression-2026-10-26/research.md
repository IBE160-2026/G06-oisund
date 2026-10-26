---
title: 'Position and stop progression: bounded technical research'
type: technical
topic: position-progression
decision: Propose the smallest useful advisory progression on a confirmed dated trip
source: native-run
status: complete
approval: not-approved
scope: EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE
preset: quick
validation: normal
created: '2026-10-26'
updated: '2026-10-26'
claims_verified: 2
claims_unverified: 5
---

# Technical research — position and stop progression

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## Recommendation

Propose standard web Geolocation with foreground-only, opt-in stop estimates, conservative uncertainty and explicit manual recovery. A qualified dated route reference and occurrence coordinates must exist first. Do not promise continuous background positioning or suitability of the Lenovo tablet. Browser lifecycle constraints support this limited scope; the hardware and matching quality remain untested. [1][2]

This research is complete as a bounded planning input, not a qualification result. No position data or live vehicle feed was collected, and no product test was run. Proposed behavior and thresholds are in [scope.md](../../scope.md); the sources below do not validate that algorithm.

## 1. Web API and measurement meaning

**Documented, single-specification details (medium; unverified independently):** watchPosition requires permission and a secure context. timestamp identifies acquisition time; accuracy reports a radius in metres at 95% confidence, not a guaranteed error bound. maximumAge limits accepted cache age; enableHighAccuracy is a hint that can cost power/time. timeout excludes waiting for visibility/permission. Callback cadence is not guaranteed, and heading/speed may be absent. The current W3C publication is a Candidate Recommendation Snapshot, not a tested browser matrix. [1]

**Corroborated constraint (high):** Chrome's secure-origin guidance agrees with W3C. A localhost development exception is not evidence that a tablet browsing a PC's plain HTTP LAN address has a secure context. [1][6]

**Proposal:** request permission only on explicit start; expose denied/unavailable/timeout separately and preserve the manual list. Reject stale, repeated, future or implausible fixes; reacquire after clock changes. Display measured age and reported accuracy separately from route-reference freshness. Several fixes and route context reduce susceptibility to one isolated error; they cannot prove correct location under persistent systematic error.

## 2. Lifecycle and actual-tablet qualification

**Documented constraints:** W3C restricts delivery to fully active visible documents. Chrome documents frozen/discarded states and unreliable mobile termination callbacks. Together these support the conservative no-background-continuity recommendation (high), not a prediction of exactly when any browser stops. [1][2]

Android documents Doze restrictions on network/tasks; its conditions and native-app guidance are not a guarantee for a moving, charging tablet's browser (medium, single publisher). Android also distinguishes app-level location permissions and approximate/precise access. Site permission alone therefore does not qualify the complete path (medium). [3][4]

Brave's official help documents site location prompts, but the inspected article is desktop-oriented and dated 2024. It cannot establish current Brave Android parity with Chrome (medium for the documented setting; Android compatibility unverified). No current primary-source evidence found in this bounded run qualifies this Lenovo/browser combination. [5]

**Proposal:** suspend when the page is hidden and invalidate stale callbacks. After an explicit resume, revalidate private-session/location access and the route reference, then require a fresh sequence of position fixes. A screen lock or battery restriction is an interruption, not permission to infer missed stops. Do not depend on wake lock, a PWA or a service worker to make background tracking reliable. The page's sample buffer is disposable; reload returns to manual mode.

**Later device checks — not executed:**

| Check | Evidence to record before accepting a pilot |
|---|---|
| Hardware and software | Exact Lenovo model/SKU, documented GNSS/location capabilities, Android/build and separate Brave/Chrome versions. Browser API existence does not identify its position source. |
| Permission and origin | Trusted HTTPS on the actual device; site grant/denial/revocation; OS location off/on; browser precise/approximate grant. No repeated permission nagging. |
| Measurement quality | Outdoor and mounted-in-bus behavior, stationary drift, fresh-fix delay, reported radius versus independently known stop/road position, sample gaps and network loss. Do not assume GNSS or offline fixes. |
| Interruptions | Tab switch, another app, screen lock, power saver, charging/unplugging, memory discard, reload and return. Record stale status and reacquisition without automatic jumps. |
| Difficult route sections | Repeated stops/loops, close opposing platforms, parallel roads, tunnels, diversion and injected jumps. Ambiguous sections must stay manual. |
| Practical fit | Battery/heat, readable Day/Night display, manual pause/correction, preserved selection and zero automatic outcome/lifecycle changes. No driver interaction required while moving. |

A future, separately authorized experiment should first use fictional trajectories and expected occurrence sequences, then controlled device observation. Aggregate error/cadence counts may suffice; any retained real track requires a separate purpose/retention decision.

## 3. Route data and optional Entur supplement

The route interface is a project dependency, not a finding that it is already delivered. It needs a selected dated journey, source direction, exact ordered occurrence range and coordinate provenance. A repeated quay must retain multiple occurrence keys. Geometry can help constrain a candidate later but cannot substitute for this identity. NSR documents stop places, quays, locations, mappings and versions; this supports a coordinate-qualification lead, not complete or date-correct coordinates for the selected route (medium, single publisher). [8]

Entur documents a vehicle-position GraphQL service with HTTP queries and WebSocket subscriptions; examples include vehicleId, lastUpdated and location, with maxDataAge filtering. Its legacy overview distinguishes vehicle monitoring from timetable estimates (medium, single publisher). [7][9]

**Inference/proposal:** later vehicle data could supplement tablet fixes only after separately verifying provider coverage, freshness, ID mapping, operating-date journey and physical-bus linkage. Line number, nearby vehicle, public journey or entered bus number alone is insufficient. The inspected documentation does not establish that linkage or an accuracy field suitable for treating vehicle data like tablet fixes. Keep sources/conflicts distinguishable and never silently substitute an unrelated bus. No Entur realtime or automatic-notice dependency belongs in the first delivery.

## 4. Privacy and combined implications

**Proposal:** compute estimates locally with a short bounded memory buffer; omit full history, storage, analytics and coordinate transmission by default. This follows W3C's purpose/disposal guidance. [1] Browser/OS providers may use network-derived location; the application policy cannot guarantee device-wide zero disclosure or offline positioning. Android documentation explicitly describes network/scanning inputs. [4]

The route snapshot can remain fixed while the estimate changes: this preserves user-confirmed/manual facts and keeps position separate from recorded work. Conversely, good location cannot repair a wrong dated journey. No formal red-team pass ran; contrary considerations are retained: foreground visibility alone does not guarantee accuracy/cadence, several fixes can share an error, and coordinate-only matching may stay ambiguous. These limit the recommendation to a qualified pilot.

## 5. Evidence status and remaining questions

Observed this run: repository/worktree status and published documentation only. No tablet or position behavior was observed. Compatibility, exact coordinate coverage, thresholds and private vehicle linkage remain open; device observation and the proposed route-interface review are the next evidence sources. A known-incompatible or ambiguous case remains manual, not silently accepted by lowering the thresholds.

Source digests record acquisition. Claim ledger uses **verified** only for independent-publisher corroboration; **unverified** includes an authoritative single-source claim and does not mean disproved. Exact browser-version support is not claimed. The research stopped once the planning questions were covered; empirical questions remain unqualified.

## Sources

All accessed **2026-10-26**. Unknown publication dates remain unknown. Dates below are page publication/update dates, not device observations.

| Ref | Supports | Publisher / source | Publication/update | Confidence |
|---|---|---|---|---|
| [1] | API semantics, visible delivery, privacy guidance | [W3C Geolocation](https://www.w3.org/TR/geolocation/) | 2026-03-26, Candidate Recommendation Snapshot | Medium alone; high corroborated constraints |
| [2] | Frozen/discarded pages and lifecycle recovery limits | [Chrome: Page Lifecycle API](https://developer.chrome.com/docs/web-platform/page-lifecycle-api) | 2026-10-16 update | Medium alone; high combined constraint |
| [3] | OS power-management restrictions, not browser guarantees | [Android: Doze and App Standby](https://developer.android.com/training/monitoring-device-state/doze-standby) | 2026-10-22 update | Medium |
| [4] | OS permissions, precision and network/scanning inputs | [Android Help: location permissions](https://support.google.com/android/answer/6179507?hl=en) | Unknown | Medium |
| [5] | Site permission control; desktop-specific limitation | [Brave Help: site permissions](https://support.brave.app/hc/en-us/articles/360018205431-How-do-I-change-site-permissions) | 2024-11-11 update | Medium documented setting; current Android unverified |
| [6] | Secure context and local development exception | [Chrome: secure-origin geolocation](https://developer.chrome.com/blog/geolocation-on-secure-contexts-only) | Historical Chrome 50 guidance; exact page date not extracted | Medium historical; corroborated by [1] |
| [7] | Possible later vehicle-position source | [Entur: Vehicle Positions](https://developer.entur.no/docs/open-services/vehicle-positions) | 2026-07-15 update | Medium; current integration unverified |
| [8] | Stop/quay location and version qualification lead | [Entur: Stop Place Register](https://developer.entur.no/apis/stop-place-v1-read) | Unknown | Medium |
| [9] | VM versus ET distinction | [Entur: legacy real-time overview](https://developer.entur.org/pages-real-time-intro/) | Unknown; portal migration notice | Medium; no current coverage claim |

## Freshness / re-check work order

The technical pack uses one month for compatibility and 24 months for API/pattern semantics. [checks/staleness.json](checks/staleness.json) calculates known-date checkpoints; unknown-date claims are listed separately in [claims.json](claims.json), never assigned the access date as publication date. Brave's compatibility source and Entur's vehicle integration documentation are already outside the one-month publication window: re-check before making current compatibility claims. This does not invalidate their narrowly stated documentation facts.

Re-check unknown-date sources before use, and all browser/OS behavior after upgrades. Actual-device qualification and verified vehicle linkage remain mandatory regardless of document freshness. The calculated oldest checkpoint is historical (Brave); it means review is due now, not that this run tested compatibility.

