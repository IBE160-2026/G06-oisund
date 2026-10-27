---
status: review
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-18
epic: 12
story: '12.3'
dependencies: [V1-09, V1-11, V1-14]
implementationStarted: true
---

### Story 12.3: Use the included views on tablet and PC

**Stable alias:** V1-18. **Status:** review; technical implementation and evidence recorded; Jonas' manual acceptance is pending.
**Depends on:** V1-09, V1-11, V1-14.
**Traceability:** NFR-1/4; IR-01; AC-10; SCOPE-02.

**User outcome:** labelled controls, keyboard focus, manual Day/Night, text enlargement and applicable IR-01 contrast across actual states; record actual browser/device limitations.

**Acceptance criteria:**
- Measure actual included foreground/background/icon/focus states in both manual themes against IR-01. Check keyboard dialog focus/return, long Norwegian text, enlargement, disabled boundaries and tablet/PC layout. Persist manual theme without private data. No Auto, wake, GPS or PDF pass inferred.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.

Implementation and executed evidence: [12.3 specification](../../implementation-artifacts/spec-12-3-tablet-pc.md), [handoff](../../../docs/evidence/12-3-handoff.md), [manual checklist](../../../docs/story-12-3-manual-testing.md). Physical qualification remains pending; 12.1/12.2 also remain in review.
