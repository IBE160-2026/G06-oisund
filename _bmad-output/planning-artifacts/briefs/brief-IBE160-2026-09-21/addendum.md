# Product Brief Addendum: Evidence and Scope Rationale

This companion preserves source evidence and detail behind the accepted [Product Brief](brief.md). It is not a PRD or technical architecture. The conversation history and decision audit remain in `.memlog.md`.

## Priorities and broader concept

The core is a complete working-shift overview: trips, breaks, start/end locations, bus changes, car transfers and relevant planned deviations. PDF import with manual bus entry is accepted; car numbers and direct Selfservice integration are unnecessary. Current-trip selection must follow actual progress, with manual next/previous controls. Current speed limit plus advance warning within 100 metres is important desired first-version scope, with feasibility unresolved.

Approaching-bus awareness is the first proposed extension. AI relevance sorting and generated short alerts follow it. Weather is a future candidate ranked below speed information; its order relative to meeting awareness and AI has not been agreed. NavCon already shows positive/negative schedule deviation in minutes and seconds, so duplicating that is excluded from the MVP.

The original brainstorming checklist remains useful as vision context:

- Vehicle/trip: current line and destination, position, next stop and schedule adherence.
- Road: current speed limit, next change and distance, roadworks, closures, diversions and incidents.
- Conditions ahead: weather, temperature, wind, precipitation and slippery conditions.
- Public transport: approaching buses and relevant operational deviations.
- AI: select what matters now and condense events into short alerts.

This checklist does not expand the agreed MVP. Product AI is separate from using AI during course development. No implementation or architecture is selected.

## Evidence from shift reports

Eleven privately stored shift-report PDFs were reviewed. The source files are not included in the public repository because they contain personal and operational information.

They contain shift date/number, start/end times and places, working time and shift span, route/trip identifiers, stop names and planned times. Labels include `tom`, `Sign-on`, `Sign-off`, `Coffee`, `MealBreak` and `Paid meal before/after`. No explicit live data, weather, roadworks, moved stops or explained diversions were found; notes appear empty. This does not prove that every trip follows its ordinary route.

Representative evidence:

- `15 august.pdf`, p. 1: shift 05:39–15:33 at Garasje Gimle; near the end, `Travel to 15:26 15:31`, followed by sign-off 15:31–15:33. Jonas explains that **Travel to means driving the assigned bus to the indicated place**, not pilot-car transport.
- `03 august.pdf`, p. 1, includes `MealBreak`; `26 juni.pdf`, p. 1, includes `Coffee`. `19 juni.pdf`, pp. 1–4, demonstrates a detailed stop listing across pages.
- The initial reports repeat the same `Vogn` value within each shift. These values must not be assumed to identify the physical bus. Jonas reports that his actual assigned bus number was missing from the report on the day he referred to and had to be obtained from the app or Selfservice.
- The later `18 sept 26.pdf` shows a numbered shift, 04:43–12:14 at Garasje Gimle, with earlier blocks marked by a `Vogn` work-block identifier. The final bus trip reaches Skognesvegen at 12:00, followed by a `Vogn` car-block identifier, a `CAR` activity with a trip identifier at 12:02 and a `tom` activity with a different trip identifier to Garasje Gimle at 12:02–12:11. Sign-off is 12:12–12:14. This supports Jonas's explanation that a car activity appears at the end, without identifying the physical car or explaining every activity code.
- `Selfservice eks.png` was visually inspected. Route 28 blocks show a work-block identifier alongside a physical bus number; a later car block from Solligården to Garasje Gimle shows a separate car assignment identifier. The date is not visible, so the screenshot is not assumed to depict the September report or the bus assignment Jonas described.

PDF layouts vary between one and two columns, with different row densities and page continuations. Text extraction can mix columns and misalign times and activities; Norwegian characters were also imperfectly represented. PDFs were not visually verified. Reliable import, including how the driver reviews and corrects it, remains a feasibility question. No authenticated Selfservice integration or screenshot import has been established.

## Operational information and trust

Jonas receives messages through SMS, an app, NavCon, media and Svipper's website. In his experience, all planned deviations appear on Svipper in time, whereas acute events such as partial cancellation from technical failure or delays from queues can lag. This is operational testimony, not independently verified coverage.

The MVP includes relevant planned Svipper deviations and excludes live queue delays and acute cancellations. Jonas notes that events affecting his own bus are already apparent to him. This does not imply that he knows about all acute events elsewhere.

Confirmed behaviors are distinct:

- Trip data missing or ambiguous: retain the last selected trip, mark uncertainty, allow manual correction.
- Deviation retrieval fails: retain previous messages with a warning that they may be outdated. A failed retrieval is not evidence that no deviations exist.
- Speed limit or road uncertain: indicate uncertainty rather than asserting an old or neighbouring-road limit; withhold unverified change warnings.

Deviation messages need validity, last update and access to the original source. Source-update time differs from retrieval time; missing metadata must not be fabricated. The behavior before any successful retrieval and detailed detection thresholds remain unspecified.

Initial bounded source research found documented Troms real-time feed availability through [Entur](https://developer.entur.no/open-data/realtime), public [Svipper traffic messages](https://svipper.no/meny/reise/trafikkmeldinger/trafikkmeldinger/) and registered access to [Vegvesen DATEX traffic information](https://www.vegvesen.no/fag/teknologi/apne-data/et-utvalg-apne-data/hva-er-datex/). No live feeds or individual incidents were tested. Automated access to Svipper messages, pilot-route coverage and correct matching remain unverified. These findings do not verify a speed-limit data source.

## Extension scenario: approaching buses

On narrow roads with limited visibility and buses in both directions, Jonas checks stop displays, a phone real-time map and NavCon meeting alerts to anticipate encounters. He reports that NavCon alerts cover only Svipper-defined zones, can show same-direction buses as oncoming, and cannot always zoom out far enough to show the situation beyond a bend or obstruction.

He describes unexpected encounters requiring a stop and manoeuvring onto a pavement occupied by pedestrians, causing delay, frightened people and stress. Earlier awareness could support planning, but no preventive outcome is established. These are his observations, not independently tested general claims about NavCon. Neither integration access nor reliable meeting prediction is established. The scenario supports the extension's value but does not displace the shift overview as the priority.

## Evaluation detail

Jonas estimates at least 20–30 minutes of searching and checking per eight-hour day, including at least a third of lunch and parts of shorter breaks. The estimate is recalled and uncertain. The accepted target is approximately 10–15 minutes total for checking the assistant and verifying sources, without continued searching across channels or missed relevant planned deviations in the evaluated cases.

The first field trial covers three actual workdays, for example Monday–Wednesday, with whichever shifts Jonas receives. After each day, note checking time, what worked, missing information and observed errors. Identical shifts are not required; Jonas rarely repeats one within a month. The days need not cover all pilot lines. Results indicate usefulness but cannot establish a controlled time-saving effect.

Pilot lines are 20, 24, 28 and 42. Jonas describes 20/24 as very similar, making them useful for evaluating confusion between lines, trips and directions. No geometry comparison was performed. A clearly labelled demo supports repeatable presentation; it cannot replace actual-shift evaluation. Actual data readiness and detailed trial procedures remain open.

## Course evidence and delivery constraints

The [official autumn 2026 course description](https://www.himolde.no/studier/emner/log/2026/host/ibe160.html), accessed 2026-09-21, requires an approved proposal and allocates 70% to project code/functionality and 30% to reflection. Documentation must explain AI use and code quality assurance; reflection covers the process, challenges, solutions, AI's influence and ethical/technological implications. Full-stack and database requirements are Jonas's explicit constraints, not explicit claims from that page.

Six privately stored teaching files were inspected:

| Source | Relevant guidance |
| --- | --- |
| `product-brief.pptx`, slides 2–5 | Mandatory `product-brief.md`, approximately two pages, explaining what, why, who and overall approach. Difficulty and quality both matter. Teams/GitHub arrangements and AI accounts are course logistics, not product features. |
| `BMAD_Product_Brief_Student_Template.pdf`, pp. 1–10 | An adaptable 1–2-page brief covering problem, value, users, success, scope and vision; technology choices come later. The exercise on p. 11 is not a course deadline. |
| `product-brief-template.md` | Eight suggested sections, including summary, problem, solution, differentiation, users, success, scope and vision. |
| `Prosjektforslag_ Programmering med KI.pdf`, pp. 1–4 | Original ideas allowed; balance time, quality, difficulty and risk. Example AI features are not universal product requirements. |
| `appendix-A.pdf`, pp. 1, 10–13, 17–23 | Tool and case-study guidance; does not mandate Python, Supabase, Docker or another stack. |
| `Appendix B.pdf`, pp. 2, 9–10, 17 | Installed BMAD workflows take precedence over outdated names; brief stays short, with supporting depth in an addendum. |

The presentation permits solo/1–4 members, while the webpage specifies 4±1. Jonas confirms solo work. Presentation dates are inconsistent with the current discussion: it lists 6 September registration, 13 September brief submission, a week-42 'now' marker and 5 December final delivery. Jonas expects mid-December; the exact applicable deadline remains unconfirmed.

Capacity is 4–16 hours weekly for approximately ten weeks, or 40–160 hours. This is not a commitment to the upper bound. Treat ten weeks as the provisional effort period rather than an exact calendar interval. The principal feasibility risks are PDF interpretation, relevant deviation retrieval, actual-progress detection and speed-limit data. No later planning phase or implementation has been started.
