---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-06
epic: 10
story: '10.2'
dependencies: [V1-04, V1-05]
implementationStarted: false
---

### Story 10.2: Correct the draft

**Stable alias:** V1-06. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-04, V1-05.
**Traceability:** FR-2/4; NFR-2; AC-02/06; SCOPE-02.

**User outcome:** edit/add/remove/order trips and other activities; unresolved fields remain visible, invalid times are rejected and cancelling leaves saved data unchanged.

**Acceptance criteria:**
- Test wrong-time correction, omitted activity addition, removal/reordering, unknown codes and cancel. Invalid required dates/type block confirmation; nullable places remain visibly unknown. Source/manual provenance remains distinguishable after saving.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
