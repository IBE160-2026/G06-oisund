---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-08
epic: 10
story: '10.4'
dependencies: [V1-07]
implementationStarted: false
---

### Story 10.4: Record the physical bus

**Stable alias:** V1-08. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-07.
**Traceability:** FR-5/11; AC-02; SCOPE-02.

**User outcome:** manual entry/correction preserves route and vehicle duty; imported Vogn never becomes an assumed physical bus.

**Acceptance criteria:**
- Apply the [owner-approved vehicle-duty/bus distinction (2026-10-20)](../../../Eksempelfiler/README.md): Vogn 960xxx is a collection of trips, and xxx is the three-character realtime-screen input (e.g. 006 or 090), never a physical bus identifier. None of the seven PDFs contains the actual bus; it must be obtained externally and entered manually. A changed vehicle duty does not establish a physical bus change; no automatic/live integration is added by this clarification.
- Preserve leading zeros/meaningful bus identifier formatting. A bus correction changes no route, activity ID or vehicle-duty identity. Imported Vogn cannot prefill an assumed physical bus.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
