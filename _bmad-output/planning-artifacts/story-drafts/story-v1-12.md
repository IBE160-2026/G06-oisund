---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-12
epic: 11
story: '11.3'
dependencies: [V1-11]
implementationStarted: false
---

### Story 11.3: Record outcomes and close

**Stable alias:** V1-12. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-11.
**Traceability:** FR-11/21/22/24; AC-08; SCOPE-02.

**User outcome:** manually mark completed/skipped/interrupted/unknown, confirm normal end or abort, then read a short recap. Cancel preserves the day; ending cannot silently complete remaining activities or resume afterwards.

**Acceptance criteria:**
- Default outcomes remain unknown until explicitly recorded. Allow manual completion/skipped/interrupted before terminal closure; confirm/cancel normal end or abort. Atomically persist terminal status/server time/expiry once. No post-end editing, silent completion or resumption. Recap is read-only within expiry.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
