---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-07
epic: 10
story: '10.3'
dependencies: [V1-06]
implementationStarted: false
---

### Story 10.3: Confirm the reviewed plan

**Stable alias:** V1-07. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-06.
**Traceability:** FR-2/4/5/24; AC-02/07; SCOPE-02.

**User outcome:** explicit review/confirmation creates one saved confirmed plan; errors/duplicate clicks cannot activate a partial or duplicated plan. Required route/time facts must be resolved or explicitly unknown where permitted.

**Acceptance criteria:**
- Show the exact reviewed revision and fixed planned-final-end expiry before explicit confirmation. Invalid required fields are resolved first. A repeated confirmation returns the same saved plan; an uncertain response is not shown as successful. New draft confirmation never silently replaces an active day.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
