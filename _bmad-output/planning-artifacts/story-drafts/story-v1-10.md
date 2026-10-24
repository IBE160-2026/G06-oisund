---
status: historical-planning-baseline
planningBaselineStatus: backlog
currentDeliveryTracking: ../../implementation-artifacts/sprint-status.yaml
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-10
epic: 11
story: '11.1'
dependencies: [V1-09]
planningBaselineImplementationStarted: false
---

### Story 11.1: Choose the intended activity

**Stable alias:** V1-10. **Historical planning baseline:** backlog; implementation/evidence had not started at scope approval. Current 11.1 implementation/review and owner-acceptance state is recorded in [sprint tracking](../../implementation-artifacts/sprint-status.yaml) and the [promoted specification](../../implementation-artifacts/spec-11-1-choose-the-intended-activity.md).
**Depends on:** V1-09.
**Traceability:** FR-6/10/11/20; AC-03; SCOPE-02.

**Owner-approved scope addition, 2026-10-24:** Include separate explicit `Start skift`, server-persisted start status/actual first start time and repeated/concurrent/lost-response recovery. Keep planned and actual start distinct. Consultation/selection works before start and never activates or completes work. Story 11.3 extends this lifecycle for outcomes/closure without duplicating Start. The promoted [11.1 specification](../../implementation-artifacts/spec-11-1-choose-the-intended-activity.md) records the approved details; this addition is not final product acceptance.

**User outcome:** direct and previous/next selection distinguish lines 20/24 and direction; selection persists online and never advances by clock or changes completion status.

**Acceptance criteria:**
- Include adjacent line 20/24 trips, opposite directions and overnight dates. Selection survives acknowledged online reload and does not change when scheduled time passes. Previous/next never sets outcomes and end boundaries have explicit disabled labels.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
