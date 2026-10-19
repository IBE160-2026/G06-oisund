---
title: Implementation Readiness — Reduced Course V1
date: 2026-10-19
workflow: bmad-sprint-planning
intent: sprint-planning
decision: SCOPE-02
gate: PASS
status: ready-for-bounded-implementation
---

# Implementation Readiness — SCOPE-02

**PASS: the reduced plan records the decisions needed to begin bounded implementation.** This is a planning verdict, not a claim that import, application, security or operational tests passed.

Jonas approved [SCOPE-02](sprint-change-proposal-2026-10-19.md) on 19 October. The [brief](briefs/brief-IBE160-2026-09-21/product-brief.md), [PRD](prds/prd-IBE160-2026-09-21/prd.md), [architecture](architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](ux-designs/ux-IBE160-2026-09-22/DESIGN.md) and [canonical backlog](epics.md) agree on the smaller contract. The September readiness report is preserved as a [raw historical snapshot](archive/pre-scope-02-2026-10-19/implementation-readiness.md.txt).

## Implementability findings

| Check | Finding |
|---|---|
| Authority and inventory | One active whole-document epic source; four new epics and 20 stories. Old 80 story approvals are historical, with explicit dispositions in SCOPE-02. No competing active spec or unrecorded owner choice is required. |
| Forward/backward traceability | Active FR-1–25 subset, NFR-1–4, S02-A–G and AC-01–12 map into the 20 stories. Deferred FR-7–9/15/23 and removed feature variants remain explicit. Every story has a user outcome, source mapping and declared dependencies. |
| Sequence and scope | All dependencies point backward; V1-01 and V1-02 are independent roots. No story depends on old E1–E8. Later verification integrates already-required quality rather than postponing basic error/privacy behavior. |
| Architecture | Backend-saved state, simple revision/idempotency contract, session/expiry, text import cleanup, manual notices and isolated fictional/fullstack paths are defined. No hidden GPS/offline/day-grant/mentor dependency remains. |
| UX | Draft → confirmation → overview → manual selection/outcome → terminal recap is specified, including failure, missing data, dates, notices and manual theme. Old mocks are explicitly historical; current spines take precedence. |
| Data boundaries | Vogn/bus and service/calendar dates remain distinct. Transient originals, server-based fixed expiry, no private persistent browser cache and demo isolation are stated. |
| Acceptance | Fixture/failure/domain cases, actual PostgreSQL/browser evidence, rendered UI and clean README are assigned. No source/device/field result is assumed. |
| Capacity | 60–80-hour owner estimate, approximately 60-hour planning basis, at least 12-hour reserve, early timebox and checkpoints are recorded; delivery is not guaranteed by story count. |

## Evidence still to obtain

- V1-01: 3–5 anonymized representative PDFs with independently checked expected facts. This is a bounded investigation, not a passed prerequisite. V1-05 starts only after its supported input envelope is established; inadequate results return for a scope decision. V1-02 can proceed using fictional data.
- Bootstrap: verify/pin compatible actual package versions and local tooling; old planning version numbers are not evidence.
- Implementation: execute AC-01–12, including authorization, no-store/back navigation, cleanup/expiry, stale/lost saves and actual UI measurements. None is passed here.
- Owner/course facts: exact December deadline, assessment browser and holiday schedule remain unknown. They affect scheduling/assessment checks but do not require invented product behavior to start the two roots.
- Field evaluation and external hosting remain deferred. A local demo cannot prove real notice coverage or time saving.

## Tracking and developer handoff

The four logical epics V1-E1–V1-E4 use fresh numeric IDs 9–12; V1-01–V1-20 use canonical 9.1–12.5. This is parser-compatible traceability, not a scope change. New stories remain backlog because planning copies are not implementation acceptance or ready-for-dev evidence.

Generate [sprint-status.yaml](../implementation-artifacts/sprint-status.yaml) from current epics.md only. Do not include archived snapshots or historical story files. Start V1-01 (9.1) and/or the independent V1-02 (9.2), refining one implementation story at a time. Preserve the testing reserve and review measured effort after 8–10 hours and around 30 hours.

No provisioning, application implementation, extraction qualification, field observation or pilot permission is produced by this readiness check.
