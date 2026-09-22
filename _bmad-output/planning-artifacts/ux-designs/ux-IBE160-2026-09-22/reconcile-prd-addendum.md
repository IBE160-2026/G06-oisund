# PRD addendum input reconciliation

Compared the PRD addendum with current DESIGN.md, EXPERIENCE.md and `.memlog.md`. This is source reconciliation, not the optional reviewer gate. Current consolidated requirements and later explicit user decisions govern; historical “open” clauses do not reopen settled decisions.

## Retained qualitative specifics

- **Resolved Finalization Decisions:** remembered access, unknown source timestamps, disappeared/removed notice versions, timer resets, whole-loaded-shift offline recovery, missing-stop fallback, manual final ending and seven-day deletion are represented in EXPERIENCE's flows, movement policy and trust/retention rules.
- **Morning Before Duty / Notice State and Retention / Connectivity Loss:** source and retrieval times remain distinct; opening marks a version seen rather than understood; changed versions regain emphasis; ended notices persist ten minutes; source failures stay separate from traffic notices; new-trip notices and changed notices remain silent. DESIGN preserves bold, changed-color and strike-through distinctions.
- **Glanceable Driving View / Manual Changes / Between-Activity Displays:** actual progress, passed stops, uncertain position, same-trip diversion recovery, physical-bus versus vehicle-duty distinctions, GPS-only direct arrows, intentional movement exceptions, ten-second activity displays and separate same-route-return triggers survive.
- **Course MVP / Import Review:** tablet website, Brave/tethering validation, separate fictional desktop assessment, automatic Svipper retrieval, direct correction, service-date matching, ambiguity choice and missing-match honesty remain explicit.

## Superseded or intentionally inherited

- `.memlog.md` extends PDF-only import to PDF/JPG/PNG, adds confirmed whole/partial active-day revisions, and defines one combined split day and summary.
- Later user decisions replace the source at-stop previous/current/next arrangement with future-above/current-bottom; current dominates at a stop and next between stops. Staged warnings, simultaneous headings, persistent theme override and GPS countdown are newer decisions.
- The desired speed-warning distance is now approximately 300 m; the separate 100 m progression criterion remains.
- Operational routines, narrow-corridor observations, reported deadhead constraints, course weighting and capacity remain source background, not missing mandatory screens. Historical routing, authentication, first-fetch and retention questions are superseded. Optional CSV and deferred routing/weather/meeting-bus specifics need not become core UX commitments.

## Genuinely dropped detail to restore or explicitly reference

- **End of a Passenger Trip:** state the completion evidence directly: registered final-stop arrival completes a non-aborted passenger trip; non-passenger completion uses position **and timing**, with uncertain/manual fallback. Current summary language preserves uncertainty but does not specify both automatic rules.
- **Glanceable Driving View:** retain the reported approximately 250 m close-stop spacing as a validation scenario for the 100 m progression rule; it is absent from the spines and is not a verified network minimum.
- **Between-Activity Displays:** preserve paid/unpaid meal classification despite the friendly meal label; the combined deadhead/meal display does not count travel as break time. These distinctions are not explicit in the current spines.

Resolution: EXPERIENCE.md now explicitly carries completion evidence and paid/unpaid meal versus travel distinctions in Between-activity transitions, and the reported close-stop validation scenario in Responsive & Platform. These restored source details introduce no new user choices.
