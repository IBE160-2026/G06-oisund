# Fictional dated journey and anchor handoff

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

**FICTIONAL ONLY.** All identifiers, names, coordinates, times, fixes and confidence assertions below are invented for specification review. They are not Entur IDs, fetched NSR data, route coverage evidence or observations of a person/bus. No location has been collected.

## Common context

Contract v0; fictional owner/workday W1, activities A1/A2; reviewed associations RA1/r1 and RB1/r1 explicitly confirmed, compatible. Provider/namespace FIX; mapping mode fictional-mapped; line FIX:Line:L; snapshot FIX:routes:r1; timezone Europe/Oslo; operating dates A=2026-11-02 and B=2026-11-03 within the same workday W1. Coordinate authority proposed in production: Entur NSR. Here coordinateSource=synthetic-NSR-shaped, snapshot FIX:coords:c1, mapping revision m1, sourceUrl=null, sourceUpdatedAt=null, fetchedAt=null. Every StopPlace/Quay version is 1; synthetic validity [2026-11-01T00:00:00+01:00, 2026-12-01T00:00:00+01:00); quality=unqualified-synthetic. Production eligibility would reject these as unqualified; the walkthrough assumes qualification solely to illustrate decisions.

Coordinate catalogue, WGS84, kind=Quay (no parent-centroid substitution):

| StopPlace | Quay | Latitude | Longitude |
|---|---|---:|---:|
| FIX:SP:A | FIX:Q:A | 69.0000 | 18.0000 |
| FIX:SP:B | FIX:Q:B | 69.0010 | 18.0100 |
| FIX:SP:C | FIX:Q:C | 69.0040 | 18.0200 |
| FIX:SP:D | FIX:Q:D | 69.0060 | 18.0120 |
| FIX:SP:E | FIX:Q:E | 69.0030 | 18.0300 |
| FIX:SP:F | FIX:Q:F | 69.0040 | 18.0400 |
| FIX:SP:G | FIX:Q:G | 69.0050 | 18.0500 |

Trip A: journey FIX:J:A, dated key (FIX:J:A,2026-11-02,23:20:00+01:00), pattern FIX:P:A/v1, source direction outbound, headsign Demo G. Full pattern 1..8; selected driven range **2..8**. Quay references resolve through catalogue/m1/c1. Each call has boarding/alighting allowed; source stop-point FIX:SSP:<occurrence key>. For brevity each row's planned arrival=departure at the shown clock; date 2026-11-02, offset +01:00, raw HH:MM:00 and dayOffset=0 are explicit conventions for every row.

| Occurrence key | Sequence | Quay | Planned clock |
|---|---:|---|---|
| A-o1 | 1 | FIX:Q:A | 23:20 |
| A-o2 | 2 | FIX:Q:B | 23:24 |
| A-o3 | 3 | FIX:Q:C | 23:28 |
| A-o4 | 4 | FIX:Q:D | 23:32 |
| A-o5 | 5 | FIX:Q:B | 23:36 |
| A-o6 | 6 | FIX:Q:E | 23:40 |
| A-o7 | 7 | FIX:Q:F | 23:44 |
| A-o8 | 8 | FIX:Q:G | 23:48 |

Trip B: activity A2, journey FIX:J:B, dated key (FIX:J:B,2026-11-03,00:00:00+01:00), pattern FIX:P:B/v1, direction inbound, headsign Demo C, same snapshot/mapping. Full pattern **E,F,G,D,C**, occurrence keys B-o1..B-o5, clocks 00:00/00:04/00:08/00:12/00:16, selected driven range **3..5**. B calls use calendar and operating date 2026-11-03, offset +01:00, raw clock as shown and dayOffset=0. Other call conventions match A; W1 is unchanged. Thus G is B-o3, not B-o8 or necessarily B's full-pattern first stop.

## One scenario, with an explicit future branch

| Step | Invented input/context | First-delivery result | Later automatic option |
|---|---|---|---|
| 1 Start, 23:24 | User selects A and chooses A-o2 at the first stop actually driven. | Manual start anchor A-o2, not A-o1; watch begins on explicit start. | Same. |
| 2 Ordinary following | Fresh coherent approach/departure evidence supports A-o3 by 23:28. | Estimate progresses 2→3. A-o2 and A-o5 remain separate visits to Q:B. | Same. |
| 3 Gap, 23:29–23:40 | Page becomes hidden; scenario assumes vehicle passes A-o4 and A-o5 unseen. The later branch assumes a fresh trajectory can uniquely support E/A-o6 after return; first delivery still waits for manual selection before new acquisition. | Old estimate3 is stale; user chooses A-o6 to resume. No observed passage is assigned to4/5. | Qualified reacquisition may set estimate3→6 directly, flagging the gap. No one-at-a-time catch-up or fabricated passage. |
| 4 Correction and reassessment | At23:40 user explicitly confirms/corrects to A-o6. Immediate fix near F is isolated. Later23:43:50/54/58 fixes approach F: (69.0037,18.0370), (69.0039,18.0390), (69.0040,18.0400), reported radii8/7/8m, received one second after acquisition. | Keep6 on initial contradictory point. Later new sequence spanning8s, continuity from E and absence of competing candidate can support estimate7. Anchor age alone, or three correlated bad fixes, cannot. Manual assertion6/time remains distinct from estimate7. | Same evidence principle; wider relocation still needs separate qualification. |
| 5 Save last stop, 23:48 | Supported arrival estimate at A-o8/G; acknowledged online save23:48:02. | Replace bounded record with Q:G, SP:G, A/date/P:A-v1/o8, snapshot r1/coords c1/m1, evidence23:48, origin GPS, savedAt23:48:02, owner W1. No raw trajectory. | Same. |
| 6 Next trip, 00:08 | After midnight on November3, user explicitly selects confirmed B in W1. Map saved Q:G into B range3..5. | Propose B-o3, showing old GPS basis and age20min. User acceptance is a new manual assertion00:08; original23:48 evidence remains old. Never copy index8. | Same. |

Illustrative W1 confirmed planned end is 2026-11-03T00:20:00+01:00; maximum expiry is 2026-11-10T00:20:00+01:00. Earlier terminal closure can shorten it. Both trips belong to W1 despite their different operating/calendar dates. The anchor's original evidence is 2026-11-02T23:48:00+01:00, acknowledged at 23:48:02; B acceptance creates a new assertion at 2026-11-03T00:08:00+01:00. Midnight neither invalidates nor refreshes the old evidence. Reuse never renews the deadline; expiry/deletion denies later proposals.

Step4 deliberately distinguishes ordinary 6→7 reassessment (first delivery) from arbitrary multi-stop relocation (future). The synthetic fixes do not validate numerical gates or error probabilities.

## Rejection variations on this same example

- At Q:B, point proximity alone cannot distinguish A-o2 from A-o5; keep uncertainty/manual choice unless ordered trajectory resolves it.
- If new B range excludes o3, G has no match. If G occurs twice inside a revised B range, propose alternatives. If B uses another Quay under SP:G, require explicit clarification; no name/parent-only join.
- Remove Q:E coordinate or make its version expired: route-data missing/invalid, even with precise fresh fixes. Restore mapping but supply a 2-minute-old fix: measurement stale, route data still valid. Both failures can coexist.
- At23:40:25 protection has expired but only a stale point exists: keep6. Freshness/continuity/uniqueness remain required.
- Failed anchor save: label unconfirmed, do not claim reload recovery; a late old-generation write cannot overwrite a newer manual anchor.
- If B belongs to another workday W2, do not propose W1’s anchor even if both occur on the same calendar date. If W1 is terminal, expired or unauthorized, no assistance/anchor write is allowed; the existing read-only lifecycle still governs.
- After explicit Pause/Off, new callbacks or a return to visibility cannot restart support. Resume/Start and manual occurrence choice are required; outcomes and saved user data are preserved.
- In every branch, intermediate actual stop events remain unknown and activity outcomes/shift lifecycle are unchanged.
