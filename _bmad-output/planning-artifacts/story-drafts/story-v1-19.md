---
status: in-review
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-19
epic: 12
story: '12.4'
dependencies: [V1-15, V1-16, V1-17, V1-18]
implementationStarted: true
---

### Story 12.4: Verify the complete user flow

**Stable alias:** V1-19. **Status:** in-review; see [implementation specification](../../implementation-artifacts/spec-12-4-complete-user-flow.md) and [executed evidence](../../../docs/evidence/12-4-handoff.md). Owner acceptance remains pending.
**Depends on:** V1-15, V1-16, V1-17, V1-18.
**Traceability:** FR-1–25 active subset; NFR-2/3/4; AC-01–09/11/12; SCOPE-02.

**User outcome:** real PostgreSQL integration plus browser flow from supported PDF through corrections, saved plan, manual selection, notices, closure and reload; include failures and independent expected data.

**Acceptance criteria:**
- Run the actual API/PostgreSQL plus a browser happy/failure flow using independent fixture expectations. Include dates/identity, notices, stale/lost writes, closure, reload, authorization and expiry. Record passed/failed/not-run and precise build; do not mirror implementation as a substitute for expected outcomes.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
