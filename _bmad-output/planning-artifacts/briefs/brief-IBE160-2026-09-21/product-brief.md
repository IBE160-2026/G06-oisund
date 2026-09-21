---
title: "IBE160 Bus-Driver Assistant — Product Brief"
status: final
created: 2026-09-21
updated: 2026-09-21
---

# Product Brief: Bus-Driver Assistant

## Purpose and users

A bus-driver assistant designed primarily for a tablet mounted in the cab. It brings the day's work and relevant operational information into one view tailored to the shift, helping the driver prepare before departure and stay oriented throughout the day, with less searching during breaks.

The first user and evaluator is Jonas, a bus driver in Tromsø. The pilot covers lines 20, 24, 28 and 42; 20 and 24 remain distinct despite similar routes. The broader concept should support other routes and cities. It is decision support, not a replacement for traffic signs, official instructions or safe driving.

## Problem and evidence

Shift information and actual bus assignments are available through an app and Selfservice, while operational messages arrive through SMS, NavCon, websites and media. Jonas estimates that checking these sources consumes 20–30 minutes of an eight-hour day, including much of his breaks. He wants to relax rather than search for information he may have missed.

An early prototype showed promise in daily summaries and automatic trip switching, but supplied an incorrect diversion and missed known roadworks and a moved stop. These user-reported observations make information reliability the central risk. Supplied shift PDFs contain much of the planned work, but omit physical bus assignments and have variable layouts. In Jonas's experience, planned deviations appear on Svipper in time; acute events can lag.

## First-version scope

- **Shift preparation:** Import a Selfservice PDF and allow manual entry of the assigned bus. Present a daily overview of trips, breaks, start/end locations, bus changes and car-transfer activities. Car numbers are unnecessary. Direct Selfservice integration is excluded.
- **Active trip:** Show current line, trip, direction/destination and next stop in a glanceable view. Follow actual progress using GPS or real-time information; timetable-only switching is insufficient. Allow manual next/previous trip selection for skipped trips or incorrect detection.
- **Planned deviations:** Present Svipper-published deviations relevant to the shift and current trip, including applicable roadworks, closures, diversions and moved stops. Show validity, last update and a button to the original source. Live queue delays and acute cancellations are excluded.
- **Speed information:** Current speed limit plus warning of the next change when 100 metres or less remain is an important desired first-version capability. Data coverage and positioning reliability are unverified; this is an explicit delivery risk, not a guaranteed capability.
- **Demonstration and real use:** Provide a test/demo function with clearly labelled simulated data and support evaluation during actual shifts. Simulation alone cannot demonstrate operational usefulness.

The course project must demonstrate a full-stack solution and use a database. Technical architecture, frameworks and the source of speed-limit data remain undecided.

## Trust and failure behavior

When trip detection is uncertain, retain the last selected trip, clearly indicate uncertainty and allow manual correction. If deviation retrieval fails, retain previously retrieved messages with a clear warning that they may be outdated. If road identification or the speed limit is uncertain, show uncertainty rather than presenting an old limit or one from an adjacent road as valid, and withhold unverified change warnings. Distinguish the source's last update from the time the assistant retrieved it; do not invent missing metadata.

## Value and success criteria

The intended advantage is a single view filtered to the driver's actual work, with information that can be checked at its source. Existing tools remain relevant: NavCon already provides schedule deviation in minutes and seconds, so duplicating that display is outside the MVP.

The agreed target is to halve information-checking time to approximately 10–15 minutes per eight-hour day, including use of the assistant and source verification. Success means those checks are sufficient, without continued searching across channels, and relevant planned deviations are not overlooked in the evaluated cases.

Initial evaluation covers three actual working days using the shifts Jonas receives, not repeated identical shifts. After each day, record checking time, what worked, missing information and observed errors in trip selection or speed limits. Results are indicative: shifts vary and the baseline is recalled rather than measured. Demonstrated features and observed real-shift outcomes must be reported separately.

## Feasibility and broader vision

Jonas is working alone for approximately ten working weeks at 4–16 hours weekly (40–160 hours), with submission expected in mid-December 2026; the exact date is unconfirmed. The combined scope is ambitious, particularly at the lower end of that range. Reliable PDF interpretation, matching Svipper messages to trips, actual-progress detection on overlapping lines, and speed-limit data require early feasibility checks. If these fail, scope must be revisited explicitly; simulation must not be presented as live capability.

Approaching-bus awareness is the first proposed extension, followed by AI-based relevance prioritization and short alert generation. Weather now and for the next hour—temperature, wind, precipitation, cloud cover/sunshine and slippery-condition information—is also a future candidate, ranked below speed information. The broader vision is timely, relevant operational support across locations. Detailed source evidence, scenarios, course guidance and unresolved questions are preserved in [the addendum](addendum.md).
