---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-14
epic: 11
story: '11.5'
dependencies: [V1-09, V1-13]
implementationStarted: false
---

### Story 11.5: Read line/date notices

**Stable alias:** V1-14. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-09, V1-13.
**Traceability:** FR-12/13/14/19; AC-04/05; SCOPE-02.

**User outcome:** show each applicable notice once with all matching lines; separate incidents remain separate; unknown validity is qualified and no entries does not mean no disruptions. No current-stop matching claim.

**Acceptance criteria:**
- Test shared line 20/24 notice once with both matching lines, a separate event on line 20, known non-overlap and unknown/partial validity. Use planned date intervals, not current-trip certainty. Empty/unavailable/unchecked states are distinct, and no list state claims full source coverage.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
