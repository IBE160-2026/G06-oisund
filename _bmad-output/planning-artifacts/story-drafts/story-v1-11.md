---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-11
epic: 11
story: '11.2'
dependencies: [V1-10]
implementationStarted: false
---

### Story 11.2: Understand the selected activity

**Stable alias:** V1-11. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-10.
**Traceability:** FR-3/10; NFR-2; AC-03; SCOPE-02.

**User outcome:** show trip or non-passenger type, planned times and known places; missing stop data has no fabricated current/next stop. Boundary controls clearly show no previous/next.

**Owner-approved refinement, 2026-10-24:** Separate upload, interpretation control/editing, day and selected activity screens. Select/open a member from the day, consult only that member with previous/next, and return without losing registered data or selection. Preserve unsaved/recovery state and access guards. Navigation does not Start or record outcomes. Notices and end/recap have planned day-linked destinations but remain 11.3–11.5 work. Intermediate stops are post-V1; demo expansion remains later work. This file retains the original backlog baseline; use the promoted 11.2 specification and sprint status for current execution state.

**Acceptance criteria:**
- Render selected trip or non-passenger type with planned dates/times and known places. Label manual selection; never render an invented current/next stop or GPS-confirmed location. Known missing information is distinct from no previous/next activity.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
