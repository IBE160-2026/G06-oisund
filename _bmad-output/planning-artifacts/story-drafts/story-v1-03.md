---
status: backlog
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-03
epic: 9
story: '9.3'
dependencies: [V1-02]
implementationStarted: false
---

### Story 9.3: Access private work

**Stable alias:** V1-03. **Status:** backlog; approved scope, implementation/evidence not started.
**Depends on:** V1-02.
**Traceability:** FR-1; NFR-3; AC-09; SCOPE-02.

**User outcome:** provisioned private login/logout, server authorization, no public signup and no demo access to private records. Session expiry requires sign-in without changing saved data.

**Acceptance criteria:**
- Verify valid/invalid credentials, fixed 14-day session expiry, logout, direct unauthenticated/cross-owner requests, CSRF/origin handling and private/demo isolation. No public signup or offline day grant. No private state survives authorized logout in browser presentation; unreachable-server logout remains explicitly unconfirmed.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
