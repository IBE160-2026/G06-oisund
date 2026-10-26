---
status: done
scopeApproval: approved
decision: SCOPE-02
approvedOn: 2026-10-19
alias: V1-14
epic: 11
story: '11.5'
dependencies: [V1-09, V1-13]
implementationStarted: true
owner_acceptance: accepted
owner_accepted_on: 2026-10-26
---

### Story 11.5: Read line/date notices

**Stable alias:** V1-14. **Status:** done; Jonas explicitly accepted the corrected account registry and expiry/extension delivery on 2026-10-26 (`Godkjent.`). Final gate: 420 backend and all 472 browser cases passed; migration/runtime/data preservation verified locally. No commit/push or further work is authorized by this acceptance.
**Depends on:** V1-09, V1-13.
**Traceability:** FR-12/13/14/19; AC-04/05; SCOPE-02.

**User outcome:** register each account notice once and reuse it automatically across eligible days until its required ending date or earlier manual ending. Allow extension only before expiry; show each matching incident once, qualify unknown starts and coverage, and never imply precise stop relevance or clear roads.

**Acceptance criteria:**
- Owner correction 2026-10-26: one account-owned notice must appear automatically on later imported/confirmed days with matching lines/intervals. Require a future ending date; date-only means end of that Oslo date. Automatic Utløpt and earlier Avsluttet manuelt are distinct from source check. Extend only while live; reject resurrection after expiry/manual ending. Original-shift deletion/closure/expiry cannot remove a still-valid notice. Preserve legacy records/receipts and qualify missing end dates for explicit completion.
- Test shared 20/24 once, separate incidents, day A to B without re-entry, known non-overlap, unknown start, date-only/precise-clock/DST ending, pre-/at-/post-deadline extension and retention cleanup. Empty/unavailable/unchecked states stay distinct and never establish source completeness or road clearance.
- Apply the current PRD/architecture/UX rules for the data and controls this slice introduces; preserve manual/unknown/fictional distinctions and private ownership. Do not implement deferred features as prerequisites.
- Record meaningful executed evidence, failures and limits for this outcome. Planning text and mockups are not test results.

**Implementation handoff:** Resolve code-level fields/libraries within the recorded contracts. If evidence contradicts the supported scope, report the gap before changing the product contract.


Sources: [active epics](../epics.md), [PRD](../prds/prd-IBE160-2026-09-21/prd.md), [architecture](../architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [EXPERIENCE](../ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [DESIGN](../ux-designs/ux-IBE160-2026-09-22/DESIGN.md). The canonical acceptance block is identical to this planning copy. Promote/refine one story in implementation-artifacts when implementation begins; do not mark it done because this file exists.
