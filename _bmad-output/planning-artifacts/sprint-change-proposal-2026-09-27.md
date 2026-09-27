---
title: Sprint Change Proposal — TIME-01
date: 2026-09-27
workflow: bmad-correct-course
status: adopted-by-product-owner
decision: TIME-01
---

# TIME-01 — Strict V1 offline time and pilot custody rule

## 1. Issue summary

Implementation readiness found that Stories 5.4 and 7.1 could not positively establish a prepared day's pre-expiry offline activation or a seven-day period after an unverified offline ending from a browser timestamp. The product owner selected the strict V1 rule on 2026-09-27, including the two user-result rules and locked-copy pilot procedure. This record supersedes the older post-expiry timing-proof option; it records a planning decision, not implemented behavior or passed evidence.

## 2. Impact analysis

- **Epics:** E5 owns original day-grant Tg, fixed E, provisional start, pre-E durable server acceptance, receipt lookup, rejection and recovery. E7 owns conservative offline-end D, approved/unknown/rejected result distinction and marked local export. E8 owns actual Lenovo/Brave and pilot-procedure qualification. No new epic or story number is needed.
- **Requirements and UX:** PRD FR-1/17/20/23/24 and NFR-3; PRD A-4/A-7; EXPERIENCE access, offline recovery, result and retention behavior; DESIGN status, lock and PDF marking.
- **Architecture:** AD-10/12 now define E, Tg, strict server cutoff, scoped post-E access, uncertain-time lock, effective D and inability to guarantee exact-time physical deletion on a closed/unreachable device. AD-5 receipt atomicity remains the required mechanism.
- **Interfaces:** The activation receipt must expose durable acceptance status/time without trusting client occurrence time; status lookup must be authorized but may recover a pre-E receipt after E. Summary/export consumes activation and closure statuses separately. A rejected activation cannot be replayed as an accepted day.
- **Risks:** Late synchronization can reject genuine earlier local work. Tg may leave less than seven days, or zero time, for post-end review/export. Locking protects application views but is not encryption. If the tablet never returns, local deletion cannot be verified. The accepted pilot control requires OS protection, named custody and a wipe/incident route.

## 3. Adopted approach

Direct adjustment of existing E5/E7/E8 stories and approved PRD/UX/architecture. No rollback, new epic, automatic scope deferral or post-E grace period. The original final grant must be server-issued within 24 hours before first planned activity, with immutable Tg. The server must durably accept activation strictly before `E = app_authenticated_at + 14 × 24 hours`; first acceptance at/after E is rejected regardless of client time. Lost pre-E receipts are recoverable by scoped lookup. For unverifiable offline end, `D = min(Tg + 7 × 24 hours, earlier binding data deadlines)`. On offline restart with unverified time, block every private view/action/export, retain the local copy locked, and delete expired data before display after trusted control.

The pilot holder reconnects at the first safe opportunity and by 24 hours after planned end, or hands in the device for supervised control. If no trusted check is possible by 24 hours after D, controlled wipe may lose unsynchronized work. A never-returning device leads to server revocation, an incident record and pilot suspension; no local deletion claim. Implementation effort and schedule remain unestimated pending story-level planning and early qualification.

## 4. Specific changes and supersession

| Earlier wording | Adopted TIME-01 rule | Updated source |
|---|---|---|
| 5.4 could accept a delayed post-E activation on an additional timing-proof basis. | First durable server acceptance must precede E; a lost pre-E response can be looked up. Warn before and during unresolved offline start that it can be rejected. | [5.4](story-drafts/story-5.4.md), [AD-10](architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [FR-1/17](prds/prd-IBE160-2026-09-21/prd.md) |
| 7.1/FR-24 suggested seven days after an offline-reported end and exact-time local cleanup. | Unverifiable end uses original server Tg plus seven days or earlier bound. Uncertain-time restart locks a retained copy; physical deletion at D on a closed/unreachable device is not guaranteed. | [7.1](story-drafts/story-7.1.md), [AD-12](architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [FR-24](prds/prd-IBE160-2026-09-21/prd.md) |
| Local versus confirmed result and post-E retained access needed an explicit user rule. | Approved day has bounded post-E review/export after trusted control; rejected local start has only distinct post-login, clearly marked local review/export while permitted. Unknown remains unknown until status lookup. | [EXPERIENCE](ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](ux-designs/ux-IBE160-2026-09-22/DESIGN.md), [7.3–7.5](epics.md) |

The [canonical epics and stories](epics.md) carry the same amendment as the individual story drafts. Their TIME-01 section governs historical step-5 open-decision language. The [readiness report](implementation-readiness.md) marks the policy decision closed and implementation/evidence open.

## 5. Handoff and success criteria

This is a moderate cross-cutting backlog adjustment with unchanged eight-epic, 80-story structure. The implementation owner builds and tests E5/E7 against the amended criteria; the UX owner applies the adopted warning, states and export marking; the pilot owner/operator establishes registered-device protection, custody, reconnect/hand-in and wipe/incident instructions. Story 8.9 gathers actual Lenovo/Brave results and procedure rehearsal. Story 8.11 records a later dated E8-P decision only if all mandatory gates pass. No E8 test was run or passed by this proposal. IR-01 remains a separate unresolved contrast decision.

The correct-course checklist covered the trigger, E5/E7/E8 impacts, PRD/UX/architecture conflict, direct adjustment versus rollback/scope change, and explicit owner approval. Sprint status needs no entry changes because no epic or story was added, removed or renumbered.

## Later readiness status — 2026-09-27

The IR-01 contrast decision was adopted after this TIME-01 proposal. References above to IR-01 as unresolved describe the proposal's earlier state; the amended PRD NFR-1, UX, stories and [readiness report](implementation-readiness.md) now govern. IR-01 measurements, Lenovo/Brave observations and E8 gates remain unexecuted. No sprint-status file was generated by this readiness-only work.
