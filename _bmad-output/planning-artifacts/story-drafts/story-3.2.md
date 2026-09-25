---
status: approved
created: 2026-09-25
epic: E3
story: '3.2'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.1', '2.12']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice implements the shared driver-interaction permission state and visible Menu/countdown, connecting the existing own-plan overview/revision actions. It does not select an active trip or implement stop progression. Later driving/notice/mentor surfaces consume the same permission state.

### Story 3.2: Apply Movement Restrictions with Honest Startup and Outage States

As the driver,
I want restricted controls to clearly reflect reliable movement or the approved unknown-speed exception,
So that their availability is predictable and an unavailable speed is never presented as confirmed standstill.

**Acceptance Criteria:**

**Given** permitted access to a confirmed own day in driver context,
**When** qualified browser observations arrive or age out,
**Then** evaluate position and speed quality separately using evidence-supported rules from 3.1 in the shared React-independent TypeScript state machine,
**And** null, stale, rejected or missing speed is unknown rather than zero; retained observations do not become fresh on reload,
**And** quality rejection, loss and recovery transitions are explicit and testable; no schedule or proximity inference substitutes for reliable speed.

**Given** reliable speed is zero, above zero up to 6 km/h, or above 6 km/h,
**When** Menu and the existing Skiftdetaljer/revision actions are rendered or invoked,
**Then** allow the restricted driver actions only at reliable zero, and visibly lock them at every reliable speed above zero,
**And** keep Menu visible with a textual reason; movement immediately closes restricted detail/review access while preserving its saved draft,
**And** recheck permission when a confirmation commits, cancelling/preventing an uncommitted action if permission was lost; do not roll back an action already atomically committed,
**And** publish this same permission for future arbitrary trip/stop selection, notice details/source/acknowledgement and operational submenu consumers, without claiming those features already exist.

**Given** genuine startup before the first valid speed observation,
**When** restricted controls are used,
**Then** allow the adopted startup exception without a five-minute wait, clearly labelling speed unknown,
**And** the first valid speed permanently ends that startup exception for the ongoing context, including a valid zero,
**And** the exception never bypasses sign-in, pending logout, confirmed-plan requirements or expiry.

**Given** usable speed is lost after a previous valid observation, including valid zero/low speed,
**When** the shared policy enters the qualified outage state,
**Then** lock restricted controls for five minutes from the established outage onset and show the remaining time beside Menu,
**And** at five minutes with speed still unknown, enable only the controls permitted by the adopted outage exception without labelling the vehicle stationary,
**And** sample freshness thresholds remain separate from this timer: expiry of five minutes does not validate old speed/position or claim usable progression,
**And** an internet outage alone does not start a GPS-loss exception when usable sensor observations continue.

**Given** an ongoing outage, invalid sample bursts or reliable recovery,
**When** observations change,
**Then** stale/invalid samples do not repeatedly reset the outage or manufacture recovery,
**And** reliable recovery immediately cancels the countdown and applies the current speed rule; recovered movement stays locked with a movement reason,
**And** a subsequent qualifying outage starts a new interval; usable position without usable speed cannot assert standstill,
**And** document the qualified onset/recovery rule from 3.1 rather than inventing unsupported sensor thresholds.

**Given** first-valid-speed history and an established outage interval,
**When** the view closes/reopens or the compatible application restarts,
**Then** restore the minimal history/timing so restart neither grants a fresh startup exception nor restarts an existing five-minute interval,
**And** restored speed is not trusted as a fresh observation; evaluate its age before determining permissions,
**And** unreadable/failed state storage produces explicit uncertainty and cannot grant startup or an elapsed-outage exception without a trustworthy basis,
**And** qualify elapsed-time handling across suspension/restart and clock changes; unsupported timing remains explicitly unresolved rather than enabling controls by guessed elapsed time.

**Given** the policy changes or an E2 revision is confirmed through its guarded entry,
**When** required local persistence and synchronization occur,
**Then** persist only minimal operational recovery facts under the existing atomic state/event conventions, preserving manual work and the immutable outbox,
**And** protect any synchronized private recovery facts with authenticated FastAPI/PostgreSQL ownership/revision checks and matching receipts; do not stream raw sensor observations to the backend,
**And** enforce logout, expiry and AD-12 cleanup on all introduced copies without storing a permanent GPS track,
**And** sensor updates do not require a server response to restrict controls; persistence failure cannot leave movement-sensitive actions enabled based on obsolete state.

**Given** the visible Menu/countdown and shared permission output,
**When** tested with keyboard, touch and assistive technology,
**Then** display readable reason/countdown text, no color-only state, and announce availability changes rather than every countdown second,
**And** preserve the separate approved exceptions for always-available theme controls and direct GPS-loss previous/next-stop actions in the permission contract; their actual controls remain later stories,
**And** no obsolete 6-km/h detail threshold or 30-second collapse grace period overrides the adopted zero-speed rule.

**Given** genuine startup or an elapsed qualified outage,
**When** an otherwise restricted action is available,
**Then** test distinct visible startup-exception and outage-exception states, both labelled Hastighet ukjent with an explanation of why the action is available,
**And** neither label implies confirmed standstill; reliability is determined by the actual quality limits established in 3.1, not hardcoded unqualified assumptions,
**And** tests restore an ongoing outage and replay a stale zero sample across restart: neither restart nor that sample opens controls by itself, resets the existing five-minute interval or creates a fresh one,
**And** a valid already-elapsed outage may still permit its labelled exception after recovery of trustworthy history; only genuinely reliable new observations establish a new recovery/outage cycle.

**Given** restricted detail, selection or review opens under the shared movement policy,
**When** it opens, is cancelled or closes because movement resumes,
**Then** move keyboard focus into the opened surface and return it to its invoker on ordinary cancellation/closure,
**And** after movement-triggered closure move focus to an appropriate visible control; focus must never remain in hidden content,
**And** cancellation preserves saved data; test focus before and after motion-triggered closure and cancelled review.

**Traceability:** FR-16; movement prerequisite for FR-6/9/11 and revisions; NFR-1/2; UX-DR13/14/15/38/39 and relevant UX-DR8/23/24 boundaries; AD-2/3/9 one local engine, AD-5 minimal persistence, AD-10/12 access/retention. E5 still owns full offline boot/authority/recovery integration.

**Dependencies:** Actual 3.1 quality evidence sufficient to define tested observation validity; planning approval alone is insufficient. Implemented E2 through 2.12 supplies the confirmed-plan overview/revision actions and E1 foundations. Negative qualification findings require an owner solution decision, not invented reliable sensing. No later trip-selection or notice implementation is needed to demonstrate the shared permission and guarded existing actions.

**Implementation evidence:** Valid zero/low/high speed, null/stale/rejected speed, startup, five-minute loss after each valid-speed category, just-before/at/after expiry, invalid bursts, separate position/speed loss, network-only outage, recovery and new outage; reload/suspend/clock/storage faults, motion between review and commit, preserved draft, access/expiry and accessible countdown. Deterministic fixtures verify the state machine; actual tablet tests verify browser behavior. Tests are specified, not executed here.

**Size boundary:** Shared movement permission and existing Menu/overview/revision integration only. No active-trip matching, stop progression, new notice or theme UI, mentor roles, active-day grant or full recovery engine. Later consumers must reuse the same policy rather than duplicate it.

**Pilot qualification:** Integrated fixture tests support E8-D. E8-P requires real mounted Lenovo/Brave behavior and later full driving/notice/recovery integration; no guarantee of absolute prevention of driver interaction is made. E8-E remains subsequent field evaluation.

**Approval:** Approved by the owner on 2026-09-25 with distinct labelled startup/outage exceptions, both explicitly showing unknown speed and the reason controls are available. Restart/stale-zero tests must neither manufacture access nor reset/start a new five-minute period. Actual 3.1 quality limits determine reliability. The owner also approved the explicit UX-DR39 focus entry/restoration and movement-triggered closure tests at the E3 checkpoint on 2026-09-25. Planning approval only; the approved copy in epics.md is canonical.
