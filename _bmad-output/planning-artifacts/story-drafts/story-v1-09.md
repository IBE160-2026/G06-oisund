---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-09
epic: 10
story: '10.5'
dependencies: [V1-07, V1-08]
implementationStarted: false
---

### Story 10.5: Read the day

**Stable alias:** V1-09. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-07, V1-08.
**Traceability:** FR-4/5; AC-02/03; SCOPE-02.

**User outcome:** reporting time and ordered trips/breaks/transfers/bus changes match the confirmed plan; separate known parts/locations and overnight dates remain visible.

**Acceptance criteria:**
- Compare the displayed order, reporting time, breaks, transfers and known locations with the saved expected plan. Include overnight and separated work-period cases; no invented transfer, later depot or completion. Missing bus remains unassigned.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
