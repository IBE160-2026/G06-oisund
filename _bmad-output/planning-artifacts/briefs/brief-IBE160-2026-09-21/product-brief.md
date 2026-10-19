---
title: "IBE160 Bus Driver Assistant — Product Brief"
status: approved
decision: SCOPE-02
created: 2026-09-21
updated: 2026-10-19
---

# Product Brief: Bus Driver Assistant

## Purpose and users

A tablet-adapted website that helps a bus driver prepare and consult a clear overview of the day's work while stopped. The first user is Jonas in Tromsø; lines 20, 24, 28 and 42 provide initial examples. A course assessor uses fictional data on an ordinary PC. The website supports the driver without replacing official instructions, signs, Tide or NavCon.

## Problem and evidence

Shift information, bus assignments and operational messages are spread across Selfservice, an app, SMS, NavCon and websites. Jonas estimates 20–30 minutes of information checking per eight-hour day. Eleven previously examined shift reports contain useful planned activities but variable layouts; extraction can mix columns, times and activities. Physical bus assignments must not be inferred from vehicle-duty identifiers.

The earlier prototype reportedly missed relevant notices and supplied an incorrect diversion. Reliability and honest uncertainty remain important. The [supporting evidence](addendum.md) is historical research, not a claim of implemented or verified capability.

## Approved course V1

On 19 October Jonas approved [SCOPE-02](../../sprint-change-proposal-2026-10-19.md) in response to [instructor feedback](tilbakemelding-product-brief.md). This replaces the earlier first-version scope.

- Import supported text-based Selfservice PDFs into an unconfirmed draft; inspect, directly correct, add, remove and order activities before confirmation.
- Enter the physical bus manually and show reporting time, planned trips, breaks, known locations, bus changes and transfers in a chronological overview.
- Select an activity directly or with previous/next controls. Selection and planned time do not establish observed location or completion.
- Maintain a simple source-linked notice list manually, with line tags, nullable validity/source-update time and separate entered/checked time. Filter by the day's lines and dates, identifying uncertainty. This version does not automatically fetch Svipper notices.
- Save and reopen plans through a real backend and database while connected. Record manual outcomes, explicitly end/abort and read a small recap.
- Run a resettable local fictional fullstack demonstration without live feeds, GPS, paid accounts or real shift files.

Retain basic private access, transient input files, bounded retention and readable tablet/PC interfaces. Existing confirmed work is not replaced by another upload. Draft edits precede activation; complex in-day revisions are deferred.

## Trust and failure behavior

Extraction stays unconfirmed until reviewed. Missing fields, unsupported layouts and unknown activity codes remain visible; manual entry is available but does not count as successful PDF extraction. Imported Vogn is not the physical bus, and Travel to is not automatically pilot-car travel.

Separate planned, manually corrected, unknown and fictional information. Source-update time is not entry/check time. No manually registered notices does not mean no disruptions. Failed or uncertain saves stay visibly unresolved until checked against the server. No GPS, live next-stop, movement-lock or offline restart guarantee is made. End/abort never silently completes unrecorded work.

## Success criteria

The functional acceptance contract is in [PRD section 8](../../prds/prd-IBE160-2026-09-21/prd.md):

1. For 3–5 independently checked anonymized PDFs, supported extraction preserves expected known activities and fields; errors/unsupported categories are reported separately. Corrections and confirmed results match a checked expected plan after save/reload.
2. Manual selection distinguishes line, direction and date, including midnight; it never marks an activity complete.
3. Notice filtering, source metadata, empty/unavailable states and manual maintenance labels are testable against fixed examples.
4. Real frontend/API/PostgreSQL persistence, private/demo isolation, explicit closure, expiry, failed saves and readable included interfaces have executed evidence.
5. The assessor can follow a clean local README and repeat fictional scenarios. A static browser mock alone is insufficient.

Reducing checking time toward 10–15 minutes remains a longer-term hypothesis. Count manual notice upkeep and source verification in that time. A demo does not prove real-world time saving, source completeness or operational usefulness; a three-workday field trial belongs to a separately scoped later evaluation.

## Feasibility and later increments

Jonas estimates 60–80 remaining hours, including a holiday week potentially providing about 40 hours. Submission is expected in December 2026; the exact date remains unconfirmed. Plan against approximately 60 hours with at least 12 hours reserved for correction and delivery. The first PDF experiment is timeboxed to roughly 3–4 hours. An inadequate supported input set requires a documented scope decision, not a false pass.

V1 uses a frontend, backend and database. The adopted stack is React/TypeScript, FastAPI and PostgreSQL; actual versions are verified during bootstrap.

Automatic notices and timetable enrichment, GPS/stop progression, speed information, offline execution, FADDER/operational INSTRUKTØR, advanced revisions and PDF export are deferred. Weather, meeting-bus awareness, AI and direct Selfservice integration remain later candidates. None is an implicit semester commitment.
