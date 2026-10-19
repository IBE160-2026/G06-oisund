---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-04
epic: 9
story: '9.4'
dependencies: [V1-03]
implementationStarted: false
---

### Story 9.4: Save and reopen a draft

**Stable alias:** V1-04. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-03.
**Traceability:** FR-4/17/20/24; NFR-2/3; AC-02/07/09; SCOPE-02.

**User outcome:** validated activities and explicit service/calendar dates survive reload; stale revision is rejected visibly; draft expiry and no-store private responses apply from introduction.

**Acceptance criteria:**
- Validate service/calendar dates, overnight offsets and unknown fields according to PRD section 4. Persist the draft with a fixed expiry and stable identity. Failed and stale writes preserve input and never overwrite a newer revision; expiry is checked before retry.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
