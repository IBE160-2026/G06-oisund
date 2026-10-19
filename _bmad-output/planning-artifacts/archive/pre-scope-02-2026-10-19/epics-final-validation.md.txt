# Epics and Stories — Internal Final Validation

Date: 2026-09-27. Scope: the final document checks inside project step 5, `bmad-create-epics-and-stories`. The owner authorized completing remaining step-5 formalities and publishing the approved plans. Project step 6 / implementation readiness is explicitly deferred to a separate chat; this report is not that assessment.

## Result

Planning document validation completed: eight approved epics, 80 individually approved stories, matching canonical and individual acceptance text, requirement allocation and backward declared dependencies. No scope or architecture change was made. This records documentary completeness, not implementation readiness, tested capability, E8-D acceptance or permission for actual shifts.

## Functional requirement check

The approved requirement inventory, supersession register and epic coverage summaries were checked against the following owning stories. E8's integrated evidence does not replace the functional owners.

| FR | Primary story coverage and controlling check |
|---|---|
| 1 | 1.1–1.2, 5.1/5.4/5.5: fixed session, durable logout, concrete active-day scope and separate Access gate. |
| 2 | 2.1/2.3–2.7: real import, transient original, unknowns, correction and explicit reviewed-revision confirmation. |
| 3 | 2.2/2.6/2.8, 3.11: dated identity/matching, complete available stop data and honest missing-list fallback. |
| 4 | 2.3/2.7/2.9–2.12: other activities, service/calendar date, order and explicit plan revision. |
| 5 | 2.7–2.10, 3.13: whole-day/part overview and physical bus distinct from duty/trip identity. |
| 6 | 3.3–3.4/3.12: actual trip selection, ambiguity, preserved manual pin and distinct correction/abort/skip. |
| 7 | 3.5–3.6: adopted UX stop ordering/emphasis and actual progression including nonstopping passage. |
| 8 | 3.1/3.6/3.8: independent 100-m measurement and supported diversion/reacquisition with visible gaps. |
| 9 | 3.2/3.7–3.8: uncertainty, qualified direct arrows, one-stop action and manual origin. |
| 10 | 3.9–3.10: final-stop interval, separate return start and non-passenger displays without false completion. |
| 11 | 3.11–3.13, 7.1: allowed manual outcomes, trip changes, actual bus changes and explicit early ending. |
| 12 | 4.1–4.4/4.6: actual automatic source ingestion, contextual relevance and source-dependent cadence. |
| 13 | 4.2–4.5: source metadata versus retrieval, unknown freshness and coverage limits. |
| 14 | 4.3–4.7: evidence-supported lifecycle and exact-version shown/seen/registered/hidden state. |
| 15 | 4.8: new relevant ongoing-trip receipt only, durable attempt identity and no old-audio replay. |
| 16 | 3.1–3.2 plus E4/E6 consumers: approved zero-speed rule, explicit exceptions and role/commit checks. |
| 17 | 2.8, 5.1–5.6, 7.1–7.4: prepared whole-day data/assets, offline use/restart/end/summary/PDF. |
| 18 | 4.2, 5.6–5.10: separate connection/source/receipt results and explicit conflict/transfer recovery. |
| 19 | 4.2/4.5: no initial notice data distinct from no notices, source access under movement restrictions. |
| 20 | 5.3/5.6–5.12, 6.10: saved active context, authority, roles and coherent-version recovery. |
| 21 | 7.1: explicit normal end/abort, confirmation/cancel and terminal local state. |
| 22 | 7.2–7.3/7.6: explicit initial-review closure, honest evidence and factual varied greeting. |
| 23 | 7.4–7.5: revision-bound local offline PDF and truthful file-handoff/retained-access status. |
| 24 | 1.3, 2.10, 5.13, E6/E7: original/earlier deadlines, permitted closure projection, fences and all-copy deletion. |
| 25 | 8.1–8.2/8.5–8.6: isolated repeatable PC demo, failure scenarios, actual external access and delivery evidence. |

NFR-1–4 and UX-DR1–44 are covered in the approved inventory/story traceability and epic summaries: mounted usability and accessibility, honest provenance, private access/deletion and actual target reliability remain explicit. UX-DR45 is the recorded out-of-V1 marker, not a missing implementation. The owner's later UX-DR33/34 review/greeting clarifications are preserved. E6 carries the adopted mentor extensions; E8 carries SM-1–5 and distraction/trust evidence with separate D/P/E decisions.

## Architecture, structure and dependencies

- Starter: AD-3 adopts the small React/Vite starter. Story 1.1 includes repeatable clean-checkout setup in the first private-access vertical slice. The generic workflow suggests renaming the first story to a setup-only milestone; the owner's explicitly approved E1 boundary and Story 1.1 take precedence. No extra technical-only epic/story or unapproved rename is introduced.
- Database: E1 creates only access/minimal draft/receipt needs as introduced; E2–E7 extend their own contracts. Real PostgreSQL is required for integration evidence. No whole application schema is created upfront and no SQLite substitute is accepted.
- Quality: all 80 stories contain user value and Given/When/Then criteria, requirement references, approved boundaries and dependencies. E1 uses equivalent `Remaining coverage`, `Integration boundary` or combined dependency/scope headings; these are not missing scope. Qualification/field stories explicitly span observation sessions or three days, rather than falsely promising one coding session. Dense work may use scoped implementation tasks without changing approved criteria.
- Dependencies: all declared IDs exist and point to earlier stories/epics. References to later evidence gates are not prerequisites for delivering an earlier bounded feature. E1–E7 own their access, persistence, privacy and errors when introduced; E8 qualifies rather than supplies missing implementations.
- Overlap: no application files yet exist for a measured file-churn claim. The known shared areas are deliberate: E2/E6 import/revisions, E3/E6 operational state, E1/E5 access/storage and E5/E7 settlement. Their user outcomes and staged risk/feedback boundaries justify the eight approved epics; shared logic must not be duplicated.
- AD-1–AD-14 remain adopted. No new provider, architecture, retention exemption, background guarantee, account-sharing feature or permanent private archive is added by this validation.

## Open matters carried into the separate readiness chat

**OPEN: 5.4/7.1 timing basis.** Client time alone cannot establish post-expiry delayed offline-start eligibility. Unverifiable end time cannot extend storage/access; the earliest applicable limit remains binding. Separate solution decision and required implementation/retest evidence are prerequisites for positive E8-P, not resolved by plan approval or this check.

Actual OCR/source/device/provider/host/compatibility tests, unknown-role recovery evidence, assessment dates/browser, field protocol/scheduling and capacity/delivery remain unresolved. More than 40 hours is known; neither 40 nor 160 hours is a fixed available budget. No requirement has been silently deferred. Readiness may assess these concerns; it has not been run here.

## Completion and handoff

The owner's request to finish remaining step-5 formalities authorizes closing this internal validation and the epics/stories workflow. Its completion hook is empty; the help catalog points to `bmad-sprint-planning` for the later readiness/sprint-planning work. No such workflow was opened or invoked. Next: a new chat for project step 6/readiness, starting from epics.md, this report, the approved source documents and the shortened development log. Do not start implementation or grant E8-D/P/E approval from this status.
