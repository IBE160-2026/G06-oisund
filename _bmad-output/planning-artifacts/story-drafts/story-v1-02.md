---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-02
epic: 9
story: '9.2'
dependencies: []
implementationStarted: false
---

### Story 9.2: Run a persisted fictional day locally

**Stable alias:** V1-02. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** none.
**Traceability:** FR-20/25; NFR-4; AC-11; SCOPE-02.

**User outcome:** documented local startup opens the frontend; a real API saves/reads a fictional day in PostgreSQL and preserves it after service restart.

**Acceptance criteria:**
- Document startup, migrations, fictional seed and teardown; demonstrate an actual API write/read in PostgreSQL and persistence after service restart. Bind private development services to loopback and record executable versions. No static-only demo can pass this slice.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
