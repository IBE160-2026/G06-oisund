---
status: approved
created: 2026-09-25
epic: E3
story: '3.14'
type: implementation
approved: true
approvedOn: 2026-09-25
dependencies: ['3.5', '3.2']
---

## Epic 3: Follow and Correct the Actual Trip Safely

This slice implements the adopted persistent Day/Night and explicit Auto control. Automatic trigger capability must be resolved and qualified on Lenovo/Brave; lack of support is visible and never silently overrides a manual choice. Wake lock remains a separate required slice.

### Story 3.14: Control Day/Night Appearance with a Persistent Manual Choice

As the driver,
I want an always-available Day/Night toggle and an explicit Auto choice,
So that the display stays readable and my manual preference survives shifts and restarts until I choose otherwise.

**Acceptance Criteria:**

**Given** the tablet interface with Menu,
**When** the theme control renders,
**Then** place the adopted outlined control immediately left of Menu, showing the current appearance as sun for day or crescent for night and a separate Auto hit area,
**And** keep both hit areas operable at every speed and during GPS loss/Menu restrictions, without a menu visit or confirmation dialog,
**And** preserve clear keyboard focus, large forgiving targets and accessible current/selected labels; do not rely on color alone.

**Given** either current appearance, including while Auto is active,
**When** the driver presses the sun/moon area once,
**Then** select the opposite current appearance manually and disable Auto,
**And** apply the adopted DESIGN day/night surface, text, secondary and semantic tokens consistently without changing stop hierarchy,
**And** persist the manual preference independently of the current day; new shifts, ambient changes and restart cannot silently reset it.

**Given** a qualified automatic-theme trigger is available,
**When** the driver explicitly selects Auto,
**Then** enable automatic appearance based on that validated trigger and persist Auto preference,
**And** display green Auto text plus its small underline and an accessible selected state, while retaining the current sun/moon icon,
**And** repeated Auto activation is idempotent, not a toggle to manual mode; manual mode shows gray Auto text without the underline,
**And** do not activate Auto merely because a new shift starts or a previously unavailable capability returns after the user retained a manual preference.

**Given** Auto capability/trigger is unresolved, unsupported, denied or temporarily unavailable,
**When** Auto is requested or its input becomes unavailable,
**Then** preserve the current readable appearance and any persistent manual preference, and show an explicit unavailable status instead of claiming automatic adaptation works,
**And** leave manual toggling immediately usable and distinguish requested Auto preference from whether adaptation is currently functioning,
**And** do not presume an ambient-light sensor, reinterpret an unrelated GPS outage as darkness or silently substitute an unqualified trigger.

**Given** the actual target tablet/browser and candidate automatic trigger,
**When** implementation qualifies the trigger before claiming Auto support,
**Then** document the actual mechanism, permissions, observed capabilities, stability and behavior in bright/dark conditions and tunnels where safely testable,
**And** state what the mechanism can and cannot respond to; synthetic or desktop tests do not establish mounted-device adaptation,
**And** test unstable/alternating inputs without distracting flicker, using documented evidence-based stability rules rather than assumed sensor guarantees,
**And** unsupported adaptation remains a documented solution decision and E8-P gap, not an automatic V1 reduction or a completed Auto claim merely because the manual fallback works.

**Given** a theme change while a trip, outage countdown, manual pin, correction or notice state exists,
**When** appearance changes manually or automatically,
**Then** change appearance only: preserve trip/context/progress, planned/observed/manual distinctions, uncertainty, Menu permission and timer history,
**And** do not produce trip/outcome events, reset notice states or steal focus with a modal,
**And** test toggling while moving, before/after the five-minute outage boundary and during a pending permitted action without broadening that action's permission.

**Given** preference persistence succeeds, fails or cannot be read on restart,
**When** the setting is changed or restored,
**Then** restore the last reliably stored preference, with manual Day/Night surviving until explicit Auto,
**And** if persistence fails, keep current-session manual control usable but clearly report that the preference could not be saved; do not falsely promise restart persistence,
**And** missing/unreadable settings use a documented readable default with visible failure where applicable, without clearing operational data or presenting Auto as available by assumption.

**Given** the preference and rendered private screens,
**When** retention, logout or offline reopening occurs,
**Then** keep the nonpersonal appearance preference separate from private workday data and its AD-12 lifecycle, without hidden day associations or private copies in application-asset caches,
**And** changing theme never unlocks private content, renews authority or extends data expiry,
**And** no new backend table or per-toggle operational outbox event is required solely for this local preference; existing fullstack operational data and receipt contracts remain unchanged.

**Given** both adopted palettes and long/uncertain/missing-data content,
**When** the integrated tablet surfaces are inspected,
**Then** preserve readable contrast, stop-role emphasis, selected/disabled states and warnings across trip, preparation and non-passenger views,
**And** record actual mounted readability in sunlight/darkness separately from deterministic visual tests; no claim that changing CSS proves glance readability.

**Traceability:** NFR-1/2/4 and FR-16 appearance-control exception; UX-DR24/25/38, DESIGN tokens and EXPERIENCE Theme control/Responsive & Platform; AD-2 local persistence boundary, AD-9 no context/permission change, AD-10/12 access and separate settings lifecycle, AD-14 compatible preference recovery. No adopted automatic sensor/trigger is invented.

**Dependencies:** Implemented 3.5 display/palette foundation and 3.2 movement policy. Actual Lenovo/Brave evidence is required for Auto support; 3.1 position/speed qualification does not qualify an ambient sensor or theme trigger. No future wake-lock, notice engine or summary implementation is required for this control to work.

**Implementation evidence:** Manual toggle from each palette/Auto, persistent preference across shifts/restart, explicit/idempotent Auto, unsupported/denied/lost trigger, return of capability without overriding manual choice, unstable inputs, motion/outage independence, failed setting write/read, long names/contrast/focus. Device evidence qualifies actual Auto behavior; tests are planned, not run.

**Size boundary:** Adopted theme control, setting persistence and bounded trigger qualification/integration. No new UI framework, custom theme editor, brightness controller, extra sensor dependency, wake-lock feature or operational data migration unrelated to the setting.

**Pilot qualification:** Repeatable theme/state tests contribute to E8-D. E8-P requires actual trigger/stability/readability qualification; unresolved support is not passed by demonstrating fallback. E8-E remains later actual-shift evaluation.

**Approval:** Approved by the owner on 2026-09-25 with the described scope: manual preference lasts until explicit Auto, and working manual switching does not establish fulfillment of unsupported Auto. Planning approval only; the approved copy in epics.md is canonical.
