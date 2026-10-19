---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-01
epic: 9
story: '9.1'
dependencies: []
implementationStarted: false
---

### Story 9.1: Establish supported imports

**Stable alias:** V1-01. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** none.
**Traceability:** FR-2; NFR-2; AC-01; SCOPE-02.

**User outcome:** 3–5 anonymized PDFs with independently checked expected activities, dates and uncertainty; record exact/partial/unsupported extraction and a pass/fail decision.

**Acceptance criteria:**
- Use independently checked expected facts rather than deriving expected results from the parser output. Classify each fixture/layout as supported, partial or unsupported. Stop the 3–4-hour experiment with evidence and a recommendation; a failed useful input set triggers an explicit scope decision. V1-02 can proceed independently with fictional data.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract. This bounded experiment can finish with negative evidence; downstream PDF acceptance still requires a useful supported envelope.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
