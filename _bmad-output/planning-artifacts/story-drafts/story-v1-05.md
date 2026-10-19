---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-05
epic: 10
story: '10.1'
dependencies: [V1-01, V1-04]
implementationStarted: false
---

### Story 10.1: Review a text PDF

**Stable alias:** V1-05. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-01, V1-04.
**Traceability:** FR-2/24; NFR-2/3; AC-01/06; SCOPE-02.

**User outcome:** supported files produce an unconfirmed draft with page/field uncertainty; original/temporary files are transient and cleaned after success/failure/cancel, including interrupted-job cleanup.

**Acceptance criteria:**
- Compare every supported fixture against independent expected activities/fields. Reject unsupported scans/images visibly; clean originals after success/failure/cancel and interrupted processing. Existing confirmed work remains intact. No raw files or extracted-text archives persist in logs/client storage.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
