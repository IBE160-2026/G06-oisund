---
title: "Bus Driver Assistant — Product Requirements Document"
status: final
approval: approved
decision: SCOPE-02
created: 2026-09-21
updated: 2026-10-19
---

# Bus Driver Assistant — Course V1

## 1. Authority and delivery boundary

Jonas explicitly approved [SCOPE-02](../../sprint-change-proposal-2026-10-19.md) on 19 October 2026. This PRD implements that decision and supersedes the September V1 contract. The [brief](../../briefs/brief-IBE160-2026-09-21/product-brief.md), current UX and architecture govern alongside this PRD. Earlier addenda, decisions, mockups and story approvals are historical wherever they conflict. The [historical index](../../archive/pre-scope-02-2026-10-19/README.md) preserves the previous baseline.

Build one tablet-adapted fullstack website with a database: supported text-PDF import, human correction/confirmation, day overview, manual navigation, manually maintained notices, online saving and a small recap. Keep the product useful for preparation and consultation while stopped. It does not certify standstill or provide live driving guidance.

## 2. Users, capacity and non-goals

One private driver, initially using Tromsø lines 20/24/28/42; a course assessor on a PC uses fictional data. Operational mentor roles are deferred and distinct from the assessor. Target tablet remains Lenovo/Brave; actual included UI behavior must be checked, not inferred from mocks.

Remaining effort is estimated at 60–80 hours; approximately 60 is the initial planning basis with at least 12 reserved for fixes/delivery. December is the expected submission month, exact date unknown. Fullstack/database is an explicit owner requirement. No paid account, external feed or GPS is required during local demo runtime; setup may require dependency downloads.

Deferred: OCR/scans/images, transit lookup, GPS/stop progression, movement locks/timers, automatic notices and precise trip/stop matching, offline private persistence, device transfer, mentor roles, advanced in-day revision, PDF export, audio, Auto theme, wake lock, external hosting and three-day field evaluation. Speed/weather/meeting buses, route calculation and AI are also outside V1.

## 3. User journeys

**UJ-1 — Prepare and consult:** sign in; upload supported text PDF or enter manually; inspect uncertainty and correct activities; confirm; enter actual bus; view chronological day and manually maintained line/date notices; select activity while stopped; optionally record manual outcomes; explicitly end or abort; read recap. Reload recovers server-saved state after authorization.

**UJ-2 — Assess locally:** follow README, start the actual frontend/API/PostgreSQL environment seeded with fictional data; run import/correction/navigation/notices/closure and failure cases; reset the isolated fictional context. No private account or record is exposed by the no-login demo. The no-login demo may share UI logic but cannot replace real fullstack assessment evidence.

## 4. Domain and interpretation rules

A workday contains ordered activities; trip, physical bus and vehicle duty are separate. Activities include passenger trip, break, deadhead, bus change and pilot-car transfer, plus explicitly unresolved types. Keep source text for an unknown code. Travel to is not automatically pilot-car travel. Vogn is not automatically physical bus.

Use a confirmed service date plus explicit local calendar dates/times in Europe/Oslo; preserve source extended-hour notation where present. An overnight time needs an explicit date/offset; never guess the day from clock order. Do not reinterpret a Friday 25:30 service as Saturday service merely because its calendar time is Saturday 01:30. Invalid/ambiguous required times must be resolved before confirmation. Locations may be unknown. Preserve separate work periods and known reporting times/depots in the ordered plan without inventing transfers or paid/unpaid classifications.

An activity ID, not a line number, identifies selection. A plan is draft, confirmed, active, ended or aborted. Only explicit actions activate/close it; time, next/previous and page navigation do not. Outcome is unknown until explicitly recorded as manually completed, skipped or interrupted. A manually completed activity is not independently verified physical work.

## 5. Approved scope supersessions

SCOPE-02 decisions S02-A–G replace automatic GPS progression with manual selection; mandatory automatic retrieval with manual notice maintenance; offline/day-grant authority with online saved state; image/OCR input with qualified text PDF; mentor workflows with own-driver work; detailed reports/PDF/mandatory field evaluation with a small recap/local acceptance; mandatory public hosting with reproducible local fullstack delivery.

TIME-01 remains historical guidance for any future offline design, not an active V1 mechanism. IR-01 contrast/focus values remain active for included interfaces. Old numeric FR identifiers below preserve traceability; deferred rows are not implementation requirements.

## 6. Functional requirements

| ID | Active V1 requirement / disposition |
|---|---|
| FR-1 | Provisioned private sign-in, explicit logout, fixed server session expiry 14 days after authentication, no public registration. Each private API operation checks session, owner and retention. Expiry requires renewed sign-in; no day-grant exception. Demo cannot access private data. |
| FR-2 | Supported text PDF produces a reviewable unconfirmed draft with field/page uncertainty. Correct directly and add omitted items before explicit confirmation. Unsupported/scanned input offers manual entry without being labelled successful extraction. Preserve the previous confirmed plan on import failure/cancel. |
| FR-3 | External timetable enrichment deferred. Preserve entered service/calendar dates, route, direction, endpoints and departure; no fabricated stops. |
| FR-4 | Edit activity type, start/end dates/times and optional known place; add/remove/reorder before confirmation. Preserve unknown codes and meaningful source classifications. |
| FR-5 | Show reporting time and chronological activities, gaps/known parts, locations and bus changes/transfers. Enter/correct physical bus separately from vehicle duty and trip. |
| FR-6 | Direct and previous/next manual activity selection. Preserve selected activity after acknowledged save/reload. No automatic selection by schedule or proximity. |
| FR-7–9 | Three-stop view, GPS progression, diversion recovery and manual stop controls deferred. |
| FR-10 | Manual activity-to-activity navigation with visible boundaries; no arrival detection, ten-second transition or return-trip trigger. |
| FR-11 | While stopped, select activity, record explicit outcome, correct bus or end/abort. No sensed movement restriction is claimed. |
| FR-12 | Private manual notice editor and line/date list. Store explicit source-backed line tags; do not infer exact trip/stop relevance or claim automatic Svipper coverage. |
| FR-13 | Show title, source link, nullable source-update time and validity, and separate entered/last-checked time. Missing source time is labelled unknown. Editing/reading a record does not automatically verify it at source. |
| FR-14 | Simple current manual notice records with explicit status. No versioned seen/hidden lifecycle, ten-minute removal, automatic ending or inferred resolution on disappearance. |
| FR-15 | Audio deferred. |
| FR-16 | Interactions are intended while stopped; no speed sensor, automatic lock or GPS-outage exception. No required interaction during driving. |
| FR-17–18 | Online saves only. Show unavailable, unsaved, saving, saved and unresolved-response states correctly. Deliberate retry/status lookup/reload preserves server truth without duplicate creation or silent stale overwrite. |
| FR-19 | Distinguish unavailable list, no manually registered notices and stale/unknown check state. None means clear roads/no disruptions. Source links remain available when known. |
| FR-20 | On authorized online reload recover last saved plan, bus, selection and outcomes. Unsaved form input survives a failed request while the page remains open, but may be lost on closure; warn before avoidable navigation. No offline restart/private persistent-cache promise. |
| FR-21 | Explicit normal end/abort with confirmation and cancellation. Closure is terminal and saved once; repeat requests do not change end time. Do not infer depot arrival or completion of remaining activities. |
| FR-22 | Small read-only recap of planned activities and explicit manual/unknown outcomes. Outcomes are corrected before terminal closure; no post-end editing phase. No driver scoring or varied greeting bank. |
| FR-23 | PDF/CSV export deferred. |
| FR-24 | Transient originals and bounded server-owned retention, as defined below. Expiry is not renewed by use/retry/sign-in. |
| FR-25 | Clearly fictional resettable local assessment of included flows and failures, without GPS/live feeds. No-login demo and private records are isolated. |

### Confirmation, save and failure rules

Draft fields may be unknown. Before confirmation require a service date, explicit calendar times sufficient to establish planned final end, ordered activities and a resolved passenger-trip line/direction/destination or a clearly acknowledged missing nonessential fact. Unknown source codes cannot silently become a confirmed supported activity type. Show unresolved issues and require the driver to correct or explicitly classify them; do not discard unreadable pages.

Creating another draft never replaces an active/confirmed day. Once active, the plan structure is fixed in V1; bus assignment, selection and manual outcomes remain editable. Changed work requiring a plan revision is outside this version, not a hidden overwrite action. Read-only historical recap remains within expiry.

Use stable operation/record identifiers and expected revisions. A response lost after commit is resolved by authorized lookup of the same operation; retry does not duplicate effects. A stale tab receives an explicit conflict and may reload; no automatic merge or force-overwrite is required. Do not clear unsaved form input merely because a request failed.

### Manual notice filtering

Each manual notice belongs to a workday; fictional shared examples are copied into the isolated demo. Required fields: title, at least one explicit line tag and an original-source URL for a real notice. Validity and source-update time may be unknown. Source URL is an ordinary HTTP(S) link; reject executable schemes.

Match tags against lines in the confirmed day and intersect known validity with that day's planned service intervals using explicit dates. Known non-overlap is excluded. Unknown/partial validity remains a visibly uncertain candidate. Show a multi-line notice once listing all matched lines; keep separately entered incidents distinct. No notice becomes verified current-trip/stop guidance. Display last source check only after an explicit check action, separate from entry/edit timestamps. No automatic freshness threshold or completeness claim is invented.

### Retention and access

Unconfirmed drafts expire seven days after server creation. A confirmed plan's fixed maximum is its confirmed planned final end plus seven days; after verified server end/abort use the earlier of that maximum and end/abort plus seven days. Use server UTC for deadlines and deny access immediately when expired; purge on backend startup and periodically (at least hourly while running). Use one transaction for terminal closure and its deadline. No late request may recreate expired data.

Delete uploaded originals and processing copies after success, failure or cancellation, including cleanup after process interruption. Retain interpreted fields/uncertainty, not raw text/OCR archives or originals. Day-associated notices/outcomes share the day's expiry. Use no persistent private browser store or service worker; private responses are no-store. Logout/session expiry clears private UI memory and guards Back/reload from stale private views. No historical private backups, private payload logs, operational repository fixtures or permanent driver history. Ordinary database storage is not forensic erasure.

## 7. Quality requirements

- **NFR-1:** tablet/PC layouts, labelled forgiving controls, keyboard operation, text enlargement, visible focus and manual Day/Night. Preserve IR-01: all informative text at least 4.5:1; necessary non-text at least 3:1; focus area equivalent to a 2 CSS-pixel perimeter, 3:1 focused/unfocused change and necessary adjacent contrast, not entirely obscured. Verify actual included states. No color-only meaning.
- **NFR-2:** distinguish planned/manual/unknown/unavailable/stale/fictional; never invent metadata, location, completion or completeness.
- **NFR-3:** backend owner authorization, no-login demo isolation, transient originals, bounded retention and anonymized publication/test data.
- **NFR-4:** verify included browser behavior and server/database restart; actual tablet/PC usability observations are separate from static designs. GPS/audio/Auto/offline/pilot measurements are deferred with their features.

## 8. Acceptance and benefit evidence

The approved [SCOPE-02 acceptance table AC-01–12](../../sprint-change-proposal-2026-10-19.md) is incorporated unchanged, subject to the explicit operational details above.

| Criteria | Required evidence / owning new stories |
|---|---|
| AC-01 supported extraction | 3–5 anonymized PDFs with independently checked expected facts; supported/partial/unsupported outcomes, not fabricated pass: V1-01/05/19. |
| AC-02 corrected saved overview | Wrong time, omitted break, distinct Vogn/bus and save/reload against expected plan: V1-06–09/19. |
| AC-03 manual navigation | Line 20/24, direction, midnight and boundary cases; no inferred completion: V1-10/11/19. |
| AC-04–05 notice semantics | Multi-line dedup, distinct incidents, nullable validity/source time, unavailable/empty/stale states: V1-13/14/19. |
| AC-06 import failure | Invalid/scanned file and interrupted processing preserve confirmed plan and clean input copies: V1-05/06/19. |
| AC-07 save integrity | Failed/stale/lost-response writes cannot duplicate or overwrite silently: V1-04/15/19. |
| AC-08 terminal outcomes | Explicit cancel/end/abort; unknown remains unknown; no resumption: V1-12/19. |
| AC-09 privacy/lifecycle | Unauthorized/demo denial, logout/expiry/cache and no resurrection: V1-03/16/19. |
| AC-10 included UI | Rendered contrast/focus, keyboard, manual Day/Night, tablet/PC and long/error content: V1-18. |
| AC-11 local fullstack | Clean README run using actual API/PostgreSQL, persistence/restart and isolated demo reset: V1-02/17/20. |
| AC-12 traceability | Requirement/story/test matrix, actual outcomes and AI reflection: V1-19/20. |

SM-3 now means correct manual selection; SM-4 means confirmed import and actual fullstack saving/closure; SM-5 remains assessability. SM-1 information time (10–15 minutes) and SM-2 real notice coverage remain unproven field hypotheses, not course-V1 acceptance. Count notice maintenance/source checking and manual interventions in later benefit evaluation. No mandatory three-day trial or old E8-P/E8-E pass is implied.

## 9. Delivery and open evidence

First timebox PDF feasibility to 3–4 hours; actual fixtures and expected results still need to be established. V1-02 may proceed independently using fictional data. No extraction/library/source result is already passed. If the useful input envelope fails, record evidence and seek a narrower product decision rather than claiming manual entry passed extraction.

Exact December deadline, assessor environment and available holiday schedule remain open. These do not block the first implementation slice. At 8–10 hours and approximately 30 hours, compare actual remaining work with the 60-hour planning basis and protect the testing reserve. Public hosting and real operational use require later decisions.
