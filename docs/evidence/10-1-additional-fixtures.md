# Story 10.1 — approved additional fixture baseline

**Approved by Jonas Øisund on 21 October 2026 (2026-10-21).** Examples 8 and 9 were added during testing/owner walkthrough of story 10.1. Approval covers their [independent source fasit](../../Eksempelfiler/README.md), including the owner's pilot-car explanation. It does not accept the story implementation or claim new extraction tests. The 20 October approval and previous seven-fixture results remain scoped to examples 1–7.

| Fixture | Pages | Explicit source activities | Main implementation checks |
| --- | ---: | ---: | --- |
| [8](../../Eksempelfiler/Eksempel-8-anonymisert.pdf) | 2 | 23 | Duty 960181 → 960176; pilot-car handover; repeated Wi-To intermediate stops; notes-only second page |
| [9](../../Eksempelfiler/Eksempel-9-anonymisert.pdf) | 1 | 8 | Fadder/Instruktør with three Coffee intervals; no trips/duty or final Sign-off |

Example 8 contains 11 route trips, five numbered deadheads, one separate CAR transition, four sign-on/off rows and two adjacent meal-break rows. Display the latter as matpause 09:38–10:23 (45 minutes), while retaining source rows. A route can pass Wi-To before its final Wi-To endpoint; do not truncate at the first occurrence. The second page has a repeated shift header and empty Notes section, not more activities.

The owner clarified **CAR - 1 through CAR - 4** as pilot-car designations. Another driver takes over the bus at the regulation point (Sentrum in this example), and this driver returns the car the other driver arrived in. Preserve `CAR / 76566` at 14:58–14:58 as a separate transition, followed by **deadhead 76567, 14:58–15:12, with the pilot car**. Preserve Wi-To as the PDF location; Sentrum and the handover explanation are owner-supplied facts. Do not infer a physical bus or a three-digit realtime-screen value from CAR. Keep ordinary full duties 960181/960176 and values 181/176 distinct from the physical bus.

Example 9 has Sign-on, three Fadder intervals, three Coffee intervals and Instruktør. Retain labels and expose unresolved internal mappings rather than treating it as an empty shift or inventing trips, duty, actual bus, final Sign-off or mentor-role features. Coffee intervals stay separate (18, 17 and 52 minutes). This fixture does not expand product scope.

All three new pages were read independently of the application parser and visually checked. The full source inventory is **nine PDFs, 13 pages and 144 activity rows**. No supported/partial/unsupported decision or import/save/reopen execution for examples 8–9 is established by this documentation. Compare the new cases with their independent facts before expanding the qualified envelope. The per-story spec, evidence and Epic 10 context also carry these obligations locally with the pending implementation changes.

Source identity at review:

- Example 8 SHA-256: `e44612caac1b676f1ea4d9bf88f8378960a0fb097ffe517a9e9d442f1edfa03d`.
- Example 9 SHA-256: `65b50ecb01c5372a17aa2a2e7db9d3bda88767db908448c3ba70cf540d666b18`.
