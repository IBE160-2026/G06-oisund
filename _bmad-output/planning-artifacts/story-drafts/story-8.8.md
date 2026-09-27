---
status: approved
created: 2026-09-27
epic: E8
story: '8.8'
type: qualification
approved: true
approvedOn: 2026-09-27
dependencies: ['3.1', '3.2', '3.6', '3.7', '3.8', '3.9', '3.14', '3.15', '4.8', '6.10', '8.5']
---

### Story 8.8: Qualify the Implemented Driving Experience on the Mounted Lenovo Tablet

As the pilot owner,
I want observed evidence of sensing, interaction, readability, theme, screen-wake and sound behavior on the actual mounted Lenovo/Brave setup,
So that the device portion of pilot qualification reflects the delivered application and its real limits rather than desktop simulations or browser API success alone.

**Acceptance Criteria:**

**Given** the actual target tablet and implemented release, with existing 3.1, E3, E4 and E6 evidence,
**When** a bounded device qualification protocol is prepared,
**Then** record actual tablet variant, OS/Brave/app versions, mount/viewing position, viewport/text scale, permissions, display/power/audio settings, trusted HTTPS and tethering arrangement, plus the case inventory and conditions actually available,
**And** reuse earlier evidence only where its environment/contracts still apply, and record the configured position/speed quality rules and their 3.1 evidence; planning approval alone is not qualified sensor evidence,
**And** separate actual browser observations, independent physical observations, controlled injected conditions and unavailable/not-run cases. Fictional plans/notice inputs may test the actual UI but cannot establish source coverage or real sensor performance,
**And** conduct pre-pilot controlled observation without operational reliance on the unqualified app and without requiring the driver to operate it while moving. Use a separate observer or unattended capture; test taps/gestures while stationary or in an explicitly labelled controlled setup. This is not an actual-shift E8-E trial.

**Given** reliable observations or loss of usable position and/or speed on the target device,
**When** the implemented adapter and shared movement policy process acquisition, ageing, interruption and recovery,
**Then** test permission denial/revocation, genuine initial startup, valid zero/low/moving speed, null/stale/rejected values, separate position/speed loss and network-only loss, recording what the browser actually delivers,
**And** include at least five minutes without a new usable observation after valid position and speed. Record last valid sample time, separate position/speed freshness expiry, qualified outage onset, browser reports or silence and recovery; the five-minute exception never makes an old value usable,
**And** verify immediate driver restriction for reliable speed above zero, distinct visibly labelled startup/outage exceptions with Hastighet ukjent, the existing five-minute boundary and immediate current-speed rules on reliable recovery. Unknown speed is not standstill,
**And** verify that reload, suspension, clock changes, stale zero or unreliable storage cannot manufacture startup eligibility or reset an established outage interval. Unsupported elapsed-time evidence remains explicit and cannot unlock by guesswork,
**And** qualify direct previous/next buttons only under the 3.1-defined position-loss conditions: unknown speed alone and network loss alone cannot enable them. Each press moves at most one stop within the selected trip's known list, with manual provenance retained.

**Given** an active trip with a checked ordered stop list and independently observed actual departures/passages,
**When** the integrated progression display is measured on the mounted device,
**Then** measure distance travelled from the independent reference event to the displayed progression change, including passage without stopping, and report individual distances and deviations against the at-most-100-m target,
**And** document the reference method, timing alignment and measurement uncertainty. Neither the app's own detection nor its unqualified position stream can independently validate itself; insufficient reference precision leaves the case inconclusive rather than passed,
**And** include representative close stops (the reported approximately 250-m scenario where available), shared/nearby stops, repeated occurrences of one stop, noise and delays. Do not claim that the sample covers every route or that 250 m is a verified network minimum,
**And** test loss/recovery and a later-stop reacquisition: preserve the visible observation gap and manual corrections, identify the correct occurrence with supported evidence, and never count unobserved passages as having met the 100-m target,
**And** test final arrival separately from return start when both use the same physical stop. Waiting, repeated position, noise, timetable and ten seconds cannot start the return; qualified GPS loss requires the separate Next press after registered final arrival,
**And** report false advancement, missed/delayed advancement and unsupported cases alongside successful ones. A failed target remains failed even when uncertain/manual fallback works.

**Given** the approved driving, notice and mentor views on the mounted tablet,
**When** glance/readability and controlled interaction checks are performed,
**Then** check the one-to-two-second glance requirement under stated conditions, preserving at-stop/between-stop ordering and dominant stop, route/destination, clock, Menu and uncertainty; static screenshots or calculated contrast alone cannot establish glance readability,
**And** cover daylight/direct sun, darkness and tunnel/light transitions where safely available, long names, text enlargement, landscape fit, missing/uncertain data, two important headings and a visible indication of additional notices. Untested lighting/fit conditions remain explicit gaps; mock-frame dimensions are not fixed breakpoints,
**And** test forgiving touch targets with the actual mounting and relevant gloves/vibration conditions without requiring precise gestures or moving-driver operation. Report missed/accidental actions and clipped critical content, not only visual preferences,
**And** check keyboard/focus and accessible labels/stop roles, warning descriptions, non-color status and meaningful announcements without announcing every poll/countdown second. Movement closes restricted content immediately and never leaves focus hidden,
**And** verify action permission again at commit, including a role change to Jeg kjører while a guiding action is pending. Failed/uncertain persistence and emergency recovery with unknown actual role retain driver restrictions; an old guiding copy is not permission to reopen controls,
**And** mentor A–B–A/context changes preserve separate periods and require fresh trip/stop context; no display or role transition proves a physical activity was completed. Reuse the owning E6 case matrix rather than invent a new role policy.

**Given** implemented manual Day/Night, Auto and active-trip screen-wake support,
**When** their behavior is observed across bright/dark conditions, foreground return, lock, restart and relevant power-saving settings,
**Then** document the actual Auto mechanism, permissions, response and stability, including flicker or unavailable support. Manual choice persists until explicit Auto; a working manual fallback cannot qualify unsupported automatic adaptation,
**And** keep theme controls available under the adopted policy without changing trip, movement locks, countdown, notice state or private access,
**And** measure actual display-awake behavior over a stated duration, distinguishing a browser-reported wake lock from a screen that actually stays awake. Record release, reacquisition, unavailable support and late callbacks after lock/context change,
**And** foreground return cannot turn saved measurements into fresh data or create startup eligibility; a held wake resource does not prove continued GPS delivery,
**And** do not claim background tracking/audio, native support, ambient sensing or uninterrupted operation from a foreground test, and do not introduce hidden-media or OS-policy workarounds.

**Given** implemented notice sound behavior and clearly labelled test receipts on the actual device,
**When** eligible new notices and silent control cases are exercised,
**Then** distinguish new relevant receipt during the ongoing trip from updates, replay, preparation/next-trip context and old notices becoming relevant later; only the approved new-receipt case is eligible for a short discreet chime,
**And** compare browser playback outcome with independently observed audibility under stated output/volume and representative ambient conditions, including blocked/denied audio and more than one eligible notice. Record missed, duplicate or distracting sounds without inferring driver hearing or understanding,
**And** test activation before use, suspend/foreground return, restart and uncertain playback outcome: later activation or recovery cannot replay old audio or produce a catch-up burst,
**And** verify visual warnings remain available, sound never opens detail or changes seen/registered state, and device sound results do not establish live source coverage. An API success, visual fallback or untested audio path cannot be counted as an audible pass.

**Given** the measured device results and unresolved cases,
**When** the qualification report is completed,
**Then** provide passed, failed, blocked and not-run outcomes per case with environment, expected/observed behavior and evidence type; separately state demonstrated support, conditional support, unsupported behavior and remaining uncertainty,
**And** link failures to their owning requirements/stories and require an explicit owner solution decision for material sensor, progression, Auto, wake, sound or usability gaps. An honest completed report is not a passed device gate, and fallback never silently removes an adopted requirement,
**And** retain sanitized timing/distance/error summaries and necessary nonprivate screenshots, remove temporary raw position observations after analysis and create no permanent GPS, private shift or performance archive under AD-12,
**And** identify which device/build/settings the evidence qualifies and which changes invalidate affected checks. Apply adopted TIME-01; device-clock tests do not prove pre-E server acceptance or Tg/D enforcement,
**And** contribute only the operational-device portion of E8-P. Source evidence, full-day durability/access/host/release checks and the explicit E8-P decision remain separate; E8-E follows permission to begin actual-shift evaluation.

**Traceability:** E8-P operational-device gate; FR-6–11/15/16 and device integration of FR-12–14/17/20, with NFR-1–4. UX-DR10–25/26–31/38–41/44 and DESIGN mounted contrast/fit/touch requirements. AD-9 sensing, one operational engine and role rules; AD-2/5/10/11/12 state, access, uncertain recovery and minimal evidence; AD-13 target HTTPS and AD-14 compatible recovery. All AD-1–AD-14 remain unchanged. Source completeness and server-timing proof are not supplied by this report.

**Dependencies:** Executed 3.1 quality investigation and implemented E3 driving/theme/wake, E4 presentation/audio through 4.8 and E6 roles/recovery through 6.10, with their existing E5 foundations; applicable 8.5 trusted private access. Actual tablet/mount and a safe observation opportunity are required. Use known test plans/labelled notices where appropriate without pretending they are live source observations. No later E8 story or actual pilot shift is a prerequisite for this bounded pre-pilot report.

**Size boundary:** One consolidated device qualification report and targeted integrated checks using existing probes/harnesses and prior feature evidence; no new sensing/role engine, browser migration, native wrapper, all-feature regression rewrite or three-workday trial. Fixes remain with owning stories. Set a bounded case inventory and observation sessions; unavailable conditions remain gaps. If execution needs splitting, retain every requirement and the consolidated device decision rather than expanding the test campaign indefinitely or dropping cases.

**Qualification boundary:** Planning only. No hardware observations, moving tests, implementation, provisioning, deployment or readiness/final-validation workflow are performed now, and no E8-D/P/E outcome is issued.

**Approval:** Approved by the owner on 2026-09-27 as scoped, emphasizing measurement of the 100-m target against independently observed passage/departure and a clear distinction between actual mounted Lenovo/Brave behavior and simulated states. Planning approval only; the approved copy in epics.md is canonical.

**IR-01 amendment (owner, 2026-09-27):** On the actual mounted Lenovo/Brave build, separately observe readability/glare, focus visibility, status/icon recognition and glance performance in Day, Night and both Auto outcomes, with relevant default, selected, warning, error and unavailable states. Cite the deterministic contrast measurements from owning UI stories and rendered-PDF measurements from 7.4, but do not infer device readability from numerical ratios or static references. Record environment, expected/observed result and passed/failed/blocked/not-run evidence; unresolved visual failures block the applicable E8-P device gate. This story does not itself qualify all exported-PDF variants unless the 7.4 page-level evidence exists.
