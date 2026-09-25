---
status: approved
created: 2026-09-25
epic: E3
story: '3.15'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.5', '3.9']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice provides and qualifies browser-supported screen wake behavior during an active trip. It does not promise background execution, uninterrupted GPS or a native application.

### Story 3.15: Keep the Active-Trip Screen Awake Where Supported

As the driver,
I want the active-trip screen to remain awake where the tablet/browser supports it,
So that I do not need to repeatedly wake the display to read the assistant.

**Acceptance Criteria:**

**Given** an authorized active trip displayed in the foreground,
**When** the view becomes eligible for browser screen-wake support,
**Then** request the available supported capability and report its actual result rather than claiming success from the request alone,
**And** distinguish acquisition pending, confirmed held, released and unavailable/failed states,
**And** selecting a prepared day without an active trip does not falsely claim an active-trip wake session.

**Given** wake support is absent, denied, fails or is released by the browser/device,
**When** the application learns that state,
**Then** show a concise understandable status that keeping the screen awake is unavailable/not active, retaining the readable trip view and operational data,
**And** do not repeatedly prompt, steal focus or demand driver action while moving,
**And** never substitute hidden media playback, artificial touches or a claimed native/background capability for the approved browser feature,
**And** retry only through supported lifecycle/action paths with bounded failure handling, not an endless tight request loop.

**Given** an active trip survives a tab switch, screen lock, app suspension or foreground return,
**When** the visible authorized view resumes,
**Then** re-evaluate actual wake support and reacquire where supported, without treating a previous held state as proof of a current lock,
**And** do not bypass an explicit device lock or private application lock,
**And** retain selected trip, manual pin, progress, uncertainty, theme and movement/outage history; return to foreground does not create fresh GPS evidence or a startup exception.

**Given** a trip ends, is interrupted, changes to another active trip, or the private view is locked,
**When** wake eligibility changes,
**Then** release obsolete wake resources and avoid duplicate holders/listeners; re-evaluate for a genuinely active successor trip,
**And** retain eligibility while the current passenger trip remains active despite delay or GPS loss, independently of Menu permission,
**And** test final-stop completion, same-route-return waiting and subsequent activation against actual trip state rather than a schedule-only timer,
**And** no wake lifecycle action can end the day, change trip outcomes or extend authority/retention.

**Given** a wake request resolves after logout, a hidden/closed view or a context change,
**When** the asynchronous result is processed,
**Then** verify current eligibility before retaining the resource and release stale acquisitions,
**And** a late success cannot unlock private content or leave the UI claiming the wrong context is protected,
**And** repeated callbacks/retries are idempotent and do not mutate operational events or synchronization batches.

**Given** network loss, sensor uncertainty or a theme change during an active visible trip,
**When** wake behavior is evaluated,
**Then** keep connectivity, position, theme and wake capability states distinct; none by itself proves that another is working,
**And** use available browser support without requiring a backend round trip,
**And** never present screen-awake success as evidence of continued sensor delivery or whole-day offline readiness.

**Given** the actual pilot Lenovo tablet and Brave browser,
**When** the implemented feature is qualified,
**Then** record actual device/OS/browser versions, relevant power/display settings, foreground duration and observed display-sleep behavior,
**And** test acquisition/release, foreground return, screen lock, trip changes, network loss, unavailable support and relevant power-saving conditions where feasible,
**And** distinguish browser-reported acquisition from observed screen behavior; report exact tested conditions and untested cases,
**And** base the capability/support status on actual observed Lenovo/Brave screen behavior under those conditions; a browser-reported held resource alone cannot establish qualified screen-awake operation or background support,
**And** document unsupported/unreliable operation as a qualification gap requiring a solution decision, not a pass because the UI exposes a fallback; no driver interaction is required during moving tests.

**Given** wake status is rendered or private data is reopened,
**When** persistence/privacy rules apply,
**Then** keep the browser-held resource state ephemeral and revalidate it after restart; never persist a boolean as proof that the resource remains held,
**And** reuse existing access/storage/expiry handling for the private view with no new private day copies, backend wake table or per-retry operational outbox events,
**And** sanitized qualification evidence excludes private trip identifiers and raw GPS traces.

**Given** status changes are shown to the driver,
**When** inspected by touch, keyboard or assistive technology,
**Then** use clear text and non-color status cues without obscuring current/next stop, route/destination, clock or Menu,
**And** avoid repeated announcements for repeated identical failures; any manual retry follows its own supported browser requirements without overriding operational movement controls.

**Traceability:** NFR-1/2/4; UX-DR25/38/44 and EXPERIENCE active-trip wake requirement; AD-2 local runtime distinction, AD-9 unchanged operational/movement state, AD-10/12 private access/lifecycle and AD-14 coherent recovery boundary. Source/notice audio qualification remains E4/E8, separate from wake support.

**Dependencies:** Implemented 3.5 active view and 3.9 trip lifecycle, with inherited access and state foundations. Actual target-device access is needed for qualification; neither desktop simulation nor 3.1 GPS qualification proves wake support. Verify browser API details during implementation without changing adopted architecture.

**Implementation evidence:** Lifecycle/failure fixtures for pending/held/released/unavailable and stale promise cleanup; active versus prepared/no-trip/locked view, context changes, foreground return and repeated events; independent network/GPS/theme states. Record actual tablet duration/power/display results separately. Tests are planned, not run.

**Size boundary:** Browser screen-wake lifecycle and target-device qualification only. No background tracking, native wrapper, display-brightness controller, operating-system policy changes, media workaround or new cloud service.

**Pilot qualification:** Repeatable lifecycle tests contribute to E8-D. E8-P requires actual device behavior and honest gap reporting; support remains conditional rather than assumed. E8-E remains subsequent real-shift evaluation.

**Approval:** Approved by the owner on 2026-09-25 with support status grounded in actual Lenovo/Brave screen behavior, without promises of background execution or other unqualified support. Planning approval only; the approved copy in epics.md is canonical. E3's coverage/continuation checkpoint remains separate; no implementation or readiness workflow has started.
