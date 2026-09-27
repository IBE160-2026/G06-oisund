---
status: approved
created: 2026-09-26
epic: E8
story: '8.1'
type: implementation
approved: true
approvedOn: 2026-09-27
dependencies: ['1.1', '3.9', '4.8', '7.6']
---

### Story 8.1: Run and Restart an Isolated Fictional PC Demo Without Signing In

As the course assessor using an ordinary PC browser,
I want to open a clearly fictional demo without signing in and repeat a basic working-day scenario,
So that I can inspect the assistant's implemented behavior without private operational records or physical GPS.

**Acceptance Criteria:**

**Given** the public demo entry and private login page,
**When** the assessor selects the clearly labelled demo entry or opens the demo directly,
**Then** load the demo on its own origin without requiring private sign-in, a test account or pilot credentials, using the adopted separate static demo-web boundary,
**And** identify the experience as fictional simulation before starting and keep that indication visible throughout operational views, summary, closing and export. Demo assessor mode is distinct from the private operational INSTRUKTØR role,
**And** provide one versioned, wholly fictional basic own-day scenario with explicit starting facts and brief start/restart instructions. Do not use anonymized production imports as an automatic fallback or claim that the fixture was successfully extracted by OCR,
**And** normal use requires neither geolocation permission nor a live timetable/disruption source. A local two-origin setup can demonstrate this slice without provisioning a public hostname or tunnel.

**Given** the fictional scenario is initialized,
**When** the assessor starts it and supplies its scripted position/speed sequence through clearly separate simulation controls,
**Then** feed typed fictional inputs through the existing operational/source ports into the same E3 state engine and implemented E4/E7 behavior used by the private application; do not create a separate permissive demo engine or a slideshow of expected outcomes,
**And** exercise a bounded scenario from known plan/stop data through actual trip selection, simulated standstill/movement/progression, explicit final own-day ending, initial review and summary. Demonstrate the existing user-initiated 7.4 PDF export with simulation marking on every page,
**And** keep assessor simulation controls separate from in-scenario driver actions: changing simulated speed is a test input, not a driver-control exception. Reliable simulated motion must apply the same restrictions as equivalent qualified inputs in the operational engine,
**And** make simulated signal timestamps, quality and any scenario time advancement coherent across the shared engine. Do not reset operational timers or directly set completed/seen/confirmed state merely to advance the demonstration,
**And** use fictional source/stop identities and expected outcomes with a documented fixture baseline. Simulated measurements and notice facts remain visibly simulated; they do not establish real source coverage, sensor quality or achievement of the real 100-metre target,
**And** display any simulated synchronization/receipt result as simulated. A static demo cannot claim to have persisted private operational data through FastAPI/PostgreSQL or supply evidence of real server acceptance.

**Given** a scenario is running, ended or partially modified,
**When** the assessor explicitly restarts it,
**Then** reset only that demo run to its documented initial fixture and create a distinct run identity, with clean fictional plan/progression/manual-choice/notice/review state,
**And** discard or invalidate pending callbacks, queued simulated responses and timers from the former run so that they cannot alter the new run, replay old sound or complete a previously cancelled export,
**And** repeated execution of the same input sequence produces the same expected operational outcomes. Demo greeting variation remains isolated under 7.6 and does not imply an operational history,
**And** coordinate demo tabs so each run's state and reset outcome are unambiguous; duplicate restart requests cannot mix old and new state. Private tabs/data are never reset or affected,
**And** a browser reload is distinguished from an explicit fresh restart: recover a compatible saved demo run if supported by the existing persistence contract, or clearly explain that a new run is needed. Never present lost state as recovered or automatically resume an ended operational day,
**And** demo restart remains an explicit simulation facility, not a capability to resume a completed private shift.

**Given** the demo bundle, fictional fixtures, storage and network adapters,
**When** initialization, normal operation, export or restart runs,
**Then** keep demo storage, asset caches, configuration, selection history and adapters separate from the private origin. No private credentials, API tokens, original imports or operational payloads are shipped in the demo bundle or source maps,
**And** do not read/write the private FastAPI service, PostgreSQL, private browser storage or live source adapters. The no-login demo must not proxy or relay private requests, accept a private API target from a URL parameter, or import private data through cross-origin messages,
**And** test private API rejection with absent/invalid authority independently of hidden controls; host-only cookies and exact-origin/CORS protections from E1/AD-10 remain necessary even for sibling hosts. UI separation alone is insufficient,
**And** use existing domain contracts with isolated fictional persistence/adapters. No demo database or new private entities are needed by this static-demo slice; private fullstack/database delivery must be demonstrated separately in E8-D,
**And** keep fixture reset and simulation controls out of the private runtime. The later Compose/network/ingress qualification must verify the same boundary at deployment; this story does not claim that network topology or Cloudflare access is already qualified.

**Given** fixture loading, local storage, an app asset or a compatible schema is unavailable,
**When** the demo cannot safely initialize or continue,
**Then** remain visibly in the fictional context, explain what failed and offer a bounded retry or explicit fresh demo restart without loading private records or manufacturing successful progression,
**And** distinguish a real demo-loading/storage failure from a deliberately simulated operational failure. Any demo-only cleanup touches only demo state; it cannot clear the private client's unsynchronized work,
**And** maintain readable PC presentation, keyboard-operable controls, focus after start/restart/error and textual simulation/disabled-state labels rather than colour alone. Apply the accepted PC design responsively rather than assuming its reference frame is a fixed browser size,
**And** provide only controls whose shared behavior is implemented. New-notice, internet-loss and qualified GPS-loss scenario controls remain required subsequent E8 slices; this basic story must not display a misleading passed/working status for them.

**Given** a clean PC browser, fictional fixtures and local distinct demo/private origins,
**When** this slice is verified,
**Then** open the demo without a session or physical GPS, run the documented basic input sequence, end the fictional day, review/inspect its summary and generate a correctly labelled PDF using the actual shared features,
**And** compare intermediate and final domain states to the fixture expectations, including driver restrictions during movement and preserved uncertainty/manual origin, rather than checking only screenshots,
**And** repeat from an active run and an ended run, including duplicate restart, delayed old callback, multiple demo tabs and reload. Verify no old run state, sound or export reaches the new run and no private state changes,
**And** inspect network requests, storage, built assets/configuration and API rejection with a synthetic private sentinel to verify isolation, including when the private app is signed in in another tab. Never use real private operational records for this test,
**And** test missing/corrupt fixtures, denied storage and incompatible saved state, verifying clear fictional failure and no private fallback. Test keyboard traversal, readable layout and simulation labels on every exported page,
**And** record scenario/build identifiers, browser version, procedure and observed results as controlled demo evidence. A passing fixture run is not live-source/device qualification, private PostgreSQL evidence or permission for a real shift.

**Traceability:** First implementation slice of FR-25 and UX-DR37/UJ-2; private isolation FR-1/NFR-3, shared information-integrity NFR-2, PC usability NFR-1 and honest qualification boundary NFR-4. Demo export FR-23/UX-DR35, truthful summary/closing FR-22/UX-DR33/34 and shared operational/source rules are consumed, not reimplemented. EXPERIENCE no-login demo entry, simulation controls and failure paths; DESIGN separate PC simulation and persistent labels. AD-1 ports, AD-2 separated storage/assets, AD-3 one shared TypeScript engine, AD-7/8 fictional source adapters, AD-9 shared domain semantics, AD-10 separate origin/no credentials, AD-12 no private archive, AD-13 static demo-web isolation and AD-14 compatible builds. AD-4/5 private PostgreSQL/receipt requirements remain binding on the private application; simulated substitutes do not satisfy them. All AD-1–AD-14 remain unchanged.

**Dependencies:** E1 private access boundary, implemented shared E2/E3 plan and operational contracts through 3.9, E4 notice semantics through 4.8 and E7 terminal/review/summary/export/closing through 7.6. Uses a prepared fictional fixture rather than implementing import/OCR again. No future E8 story is required to run the basic demo locally; full failure-scenario suite, hosted assessment access and evidence gates remain subsequent work.

**Size boundary:** One no-login isolated demo entry, one basic fictional scenario, typed signal controls, shared-feature wiring, demo-only persistence/reset and boundary tests. No full scenario catalogue, new engine, live-source qualification, private fullstack proof, account system, DNS/tunnel provisioning or deployment. The agreed assessment period and exact assessor browser remain later scheduling/qualification clarifications, not blockers for this local slice.

**Qualification boundary:** Contributes to E8-D but does not pass that checkpoint alone. E8-D also requires private fullstack/real-PostgreSQL evidence and reproducible delivery documentation. E8-P remains actual source/OCR/device/access/host/lifecycle qualification before shifts; E8-E remains the subsequent three-workday evaluation. TIME-01 policy is adopted; its implementation and actual-device evidence cannot be supplied by simulated clocks. No implementation, execution of tests, provisioning or deployment occurs during story planning.

**Approval:** Approved by the owner on 2026-09-27 as scoped. The owner affirmed technical isolation from the private application and tests that prevent old-run events affecting a new run after restart. This story contributes to E8-D; E8-P and E8-E remain separate checkpoints. Planning approval only; the approved copy in epics.md is canonical.
