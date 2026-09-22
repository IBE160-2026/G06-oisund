# Targeted source check: notices, split shifts and active-day amendments

Date: 2026-09-22. Read order: PRD, PRD addendum, product brief, brief.md, brief addendum. PRD and its addendum govern over briefs; the PRD addendum explicitly preserves historical superseded decisions (line 9). Latest user requirements extend the baseline below.

## Already settled

- **Whole-day, multi-route relevance:** PRD FR-5 (line 94) includes all trips, breaks, known start/end locations, bus changes and transfers. FR-12 (125) requires shift-relevant notices before duty, only current-trip/activity relevance while driving, next-trip notices at final-stop arrival, and route/direction/stop/validity matching. FR-13 (127) preserves source/freshness uncertainty. Thus several relevant notices across several routes are inherent in the baseline; one morning notice was only an illustrative mock.
- **Notice identity must persist:** FR-14 (129–133), FR-15 (135), PRD addendum 239–243 and 418–422 require version-specific seen state, no repeated new status/chimes for the same notice, and persistent state through restart/outage. Source identity remains subject to verification. A shared notice across routes fits these rules; merging unrelated notices merely because their headings are similar does not follow from them.
- **Activities and locations:** FR-4 (92) allows type, start/end times and optional location; do not invent locations. FR-5 (94) retains known start/end places and keeps actual bus, vehicle duty and trip distinct. FR-10 (108–119) handles breaks, bus changes, transfers and return, but does not define a split-duty interruption lifecycle.
- **Intermediate depot is not end of shift:** FR-21 (168) explicitly says intermediate depot visits do not complete a shift. Ending requires confirmation; completed shifts cannot resume. PRD addendum 359–361 supports this distinction.
- **Recovery/history:** FR-17/20 (158/164) retains the whole confirmed shift, manual corrections and seen notices offline/across restart. FR-22 (170) preserves displayed notices, corrections and completed/skipped/uncertain evidence. FR-24 (174) defines seven-day retention after completion/abortion, or planned end for a never-ended shift.
- **Initial import correction:** FR-2 (86), FR-3 (88–90), addendum 478–494 require explicit preview/confirmation, direct editing and addition of trips omitted by extraction; route, endpoints, departure time and service date support timetable matching, with explicit ambiguous/no-match/source-failure handling. This is **not an established mid-shift replacement/merge policy**.
- **Operational corrections:** FR-11 (121) includes selecting/interruption of trips, fault-related bus change and early ending. It does **not explicitly include reimporting an updated shift or adding overtime to an already active shift**. FR-16 (139–152) governs movement restrictions and startup/GPS-loss exceptions; amended-shift actions should preserve this baseline, not silently redefine it.

## Background corroboration

- product-brief.md 14/24–25: four pilot routes, broader assistant ambition, daily trips/breaks/start/end locations and actual-progress selection.
- brief.md 20/24/26: variable source layouts, complete daily overview and shift/current-trip relevant planned notices.
- brief addendum 7/35/45: complete shift overview, difficult PDF extraction, uncertainty/manual recovery. Its old statement that screenshot import was unestablished is superseded by the user's explicit PDF+image UX decision.

## New user decisions to capture

1. Support several notices on one route and across a multi-route day. A single source notice affecting multiple lines may show those lines on the same message.
2. Represent split shifts, including different starting depots for different parts.
3. During the day, permit both an updated shift upload and manual addition of one or more extra/overtime trips.

## Genuine design gaps, not previously answered

- Split shift: one continuing day/shift with separate duty parts versus separately ended shifts and summaries. PRD does not decide this. An intermediate depot visit must not silently finalize anything either way. The user should choose whether the gap pauses the same shift and later resumes it; consequent notice retrieval/wake behavior in the gap also needs a stated rule or explicitly labelled proposal.
- Active-day update: preview additions/changes/removals and their placement among remaining activities; reconciliation with completed history, active trip, prior manual changes and duplicate trips. Neither initial import nor omitted-trip entry settles these conflicts. A proposed merge should preserve evidence and require confirmation before affecting the live plan; uncertain matching should remain unresolved rather than erase/relabel completed work.
- Different depots: known start location belongs to each duty part, not one global depot. Unknown locations remain unknown. Whether travel between parts is assigned work cannot be inferred just from different depots.
- Multiple files: whole-day replacement versus a file containing only a later duty part needs explicit interpretation in the confirmation flow; no source decides that every new upload replaces all future work.

No source establishes separate split-shift accounts, payroll computation, automatic travel arrangements, automatic overtime approval, or a new trip-data provider. These must not be inferred from this request.
