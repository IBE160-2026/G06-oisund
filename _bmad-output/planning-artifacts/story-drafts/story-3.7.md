---
status: approved
created: 2026-09-25
epic: E3
story: '3.7'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.2', '3.6']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice adds manual stop correction and qualified return to automatic progression within the selected trip. It reuses the shared movement policy and progression engine; diversion recovery and final-stop/return transitions remain subsequent slices.

### Story 3.7: Correct Stop Progress Manually When Position Is Uncertain

As the driver,
I want to correct the stop context under the approved interaction rules,
So that the selected trip remains usable when positioning is unavailable or progression is wrong, without presenting my correction as GPS evidence.

**Acceptance Criteria:**

**Given** an active trip with a usable stop sequence and lost usable positioning under the actual 3.1 quality rules,
**When** the driving view reflects the outage,
**Then** retain the last committed context with explicit uncertainty and expose direct previous/next-stop controls,
**And** these direct controls follow the approved GPS-loss exception, including while moving and during the five-minute restriction on arbitrary selection,
**And** internet loss alone does not expose them when positioning remains usable; position and speed quality remain separate.
**And** GPS loss is determined by the qualified signal states established in 3.1; unknown speed alone never exposes direct arrows. Test usable position with unknown speed, network-only failure and actual qualified position loss separately.

**Given** the direct GPS-loss controls are available,
**When** the driver intentionally presses previous or next,
**Then** move the manual stop context one supported sequence step within the selected trip, using the existing operational state contract,
**And** each press moves at most one stop within that trip's known list; no repeated callback, long press or boundary condition may turn a single press into a multiple-stop jump,
**And** clearly mark manual provenance without asserting a fresh position, GPS-confirmed arrival or observed dwell,
**And** preserve the active trip/manual trip pin and prior observed/manual evidence; correction does not erase historical events or mark intervening work GPS-observed,
**And** no route-boundary press fabricates a stop or wraps to another trip. Final-stop registration and the special extra Next action for a same-route return must integrate through the subsequent terminal-transition story, not a generic index increment.

**Given** the driver wants to choose an arbitrary correct stop,
**When** the stop sequence is tapped or the stop selector is opened and a choice committed,
**Then** use the same 3.2 permission at entry and commit: reliable standstill, genuine startup exception or elapsed five-minute outage exception,
**And** reliable motion locks arbitrary choice even though direct GPS-loss previous/next may remain available,
**And** unknown-speed exceptions visibly show Hastighet ukjent and why access is allowed; stale zero/restart never bypasses that policy,
**And** cancellation or permission loss before commit preserves the prior committed context and explains the restriction without demanding action while driving.

**Given** an eligible stop in the selected trip is explicitly chosen,
**When** the correction commits,
**Then** update only that trip's stop context with manual origin and clear current/next roles in the 3.5 view,
**And** distinguish repeated stop names/occurrences by sequence and trip context, rather than conflating identical names,
**And** do not infer other-line selection, activity completion, GPS-confirmed passage or actual physical actions from the choice.

**Given** usable position returns after manual corrections,
**When** the observations satisfy the qualified recovery rules,
**Then** hide the direct GPS-loss controls and let the shared engine realign within the currently selected trip using supported fresh evidence,
**And** retain manual correction history and the manual trip pin; recovery cannot choose another line or treat old observations as current,
**And** if returned data is insufficient to identify a stop unambiguously, keep progress uncertain instead of choosing the nearest stop; farther-along/diversion recovery remains the separate required slice,
**And** apply 3.2's independently evaluated speed restrictions immediately; restored position alone does not prove standstill.

**Given** a pending manual action races with reliable position return, trip change or plan/sequence change,
**When** the action reaches its atomic commit boundary,
**Then** revalidate the action's availability, target trip/context and sequence identity,
**And** reject stale actions without applying them to a new context or double-advancing; a callback/retry of the same action applies once while distinct intentional presses remain distinct actions,
**And** preserve deterministic ordering and provenance of committed manual actions and subsequent observations.

**Given** correction, synchronization and reopening,
**When** state is saved or recovered,
**Then** atomically persist corrected context and its typed event before displaying success; failed local writes retain the previous context with an explicit error,
**And** preserve manual origin, trip pin, last observation freshness and 3.2 startup/outage history across reopen; reopening neither refreshes location nor restarts the five-minute interval,
**And** reuse authorized FastAPI/PostgreSQL transactions, immutable batches and matching receipts; server failure does not discard a locally committed correction,
**And** enforce ownership, pending logout/storage locks and AD-12 expiry on every copy, with minimal evidence and no permanent raw GPS track.

**Given** no usable stop list or a known sequence boundary,
**When** stop correction is rendered,
**Then** do not enable a fictitious stop choice or create stop identifiers; show the missing-list or actual boundary reason,
**And** missing-list completion/abort/next-activity remains a separate required fallback story, not falsely claimed as available here.

**Given** the manual controls and selector,
**When** inspected with touch, keyboard and enlarged text,
**Then** use large labelled targets, visible focus and explicit enabled/disabled reasons without color-only distinctions or precise gestures,
**And** keep route/destination, uncertainty and Menu/countdown visible; do not add an automatic modal or require correction while driving,
**And** isolate simulated fault scenarios from operational data during tests.

**Traceability:** FR-9 manual correction/uncertainty/recovery, FR-16 interaction rules, FR-6 manual trip authority and foundational FR-20; NFR-1/2/3; UX-DR11/13/14/15/16/38/44; AD-2/3/5 atomic state and persistence, AD-9 shared operational engine, AD-10/12 access/retention.

**Dependencies:** Implemented 3.2 and 3.6 with inherited 3.1 quality evidence, selected-trip and 3.5 view foundations. Nonterminal manual correction and qualified normal-sequence realignment are independently demonstrable; future terminal/diversion/fallback stories integrate at their boundaries without changing these movement rules.

**Implementation evidence:** GPS loss at reliable zero/low/high speed, direct arrows before/after five minutes, network-only outage, arbitrary selection locked/allowed under each approved state, stale-zero/restart, repeated stop names, boundaries/missing list, intentional multiple presses versus retry, return-of-position/action race, new trip/sequence race, manual history preserved after realignment, failed write/lost receipt and uncertain reopen. Tests are specified, not run.

**Size boundary:** Manual correction within a usable selected-trip stop sequence and normal qualified recovery. No diversion engine, stop-list fabrication, trip switching, terminal completion/return timers, missing-list outcome controls or duplicate movement engine.

**Pilot qualification:** Deterministic exception/correction cases contribute to E8-D. E8-P must qualify actual tablet loss/recovery, mounted controls and integrated terminal/fallback/recovery behavior before actual shifts; E8-E remains subsequent evaluation. The approved in-motion arrow exception is preserved, not a claim of absolute interaction safety.

**Approval:** Approved by the owner on 2026-09-25: GPS loss follows qualified 3.1 signal states; unknown speed alone or network loss does not expose direct arrows. Each press moves at most one stop within the selected trip's known list. Manual corrections remain non-GPS evidence and ambiguous recovery cannot silently overwrite them. Planning approval only; the approved copy in epics.md is canonical.
