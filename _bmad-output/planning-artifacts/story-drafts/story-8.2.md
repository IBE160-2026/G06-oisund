---
status: approved
created: 2026-09-27
epic: E8
story: '8.2'
type: implementation
approved: true
approvedOn: 2026-09-27
dependencies: ['8.1', '3.2', '3.7', '3.8', '4.8', '5.6']
---

### Story 8.2: Repeat Notice, Network and Positioning Failure Scenarios in the Isolated Demo

As the course assessor,
I want to trigger fictional new notices, network loss and positioning loss independently and observe recovery,
So that I can repeat and inspect the implemented restrictions and uncertainty rules without mistaking simulation for real qualification.

**Acceptance Criteria:**

**Given** the isolated demo from 8.1 and its known fictional starting state,
**When** the assessor selects a notice, connection or positioning scenario,
**Then** show the selected scenario, required starting context and clearly labelled simulation controls with brief steps and expected observations,
**And** provide independent controls for fictional source delivery, simulated connectivity and position/speed inputs; a single generic failure toggle cannot silently turn all three off or on,
**And** feed versioned scripted inputs through the existing adapters and shared E3/E4/E5 behavior rather than setting UI labels, permissions, completion or acknowledgement states directly,
**And** bind every injected event and delayed callback to the current demo run. Invalid triggers explain the missing prerequisite rather than silently changing the selected trip, role or operational history,
**And** keep simulation visible in screens, summaries and exported evidence, with actual browser/loading failures distinguished from intentional scenario inputs. Assessor controls do not give the fictional driver extra permissions.

**Given** an ongoing fictional trip and a known source baseline,
**When** the assessor triggers a genuinely new relevant notice through the fictional source adapter,
**Then** apply the existing source identity/version, relevance, source-time versus retrieval-time and display rules, including acute display from receipt/relevance assessment rather than simulated source publication,
**And** expose documented fictional provenance and unknown metadata where the fixture omits it; source error or partial response cannot erase useful notices or claim there are none,
**And** demonstrate the existing one-attempt chime eligibility for a new relevant receipt during the ongoing trip, plus silent duplicate delivery, material update and an already received notice becoming relevant later,
**And** use the real browser audio path with truthful blocked/failed/uncertain playback status; the simulator cannot label an unobserved sound as heard or replay old sound after later audio permission,
**And** include a controlled update and explicit source-supported ending for that same incident so repeated runs show version emphasis and lifecycle behavior without inventing an ending from absence alone,
**And** retained summary/PDF evidence includes only presentation actually recorded by the shared view, not every scripted notice or every injection attempt. Seen/registered/hidden states retain their distinct meanings.

**Given** usable simulated positioning and an ongoing prepared fictional day,
**When** the assessor enables simulated network loss,
**Then** make the fictional remote adapters unavailable while local plan, downloaded stop lists, prior notices and permitted corrections remain usable; show loss of updates without making retained data appear fresh,
**And** continue sensor-driven progression and movement restrictions while qualified simulated observations continue. Network loss alone neither enables GPS-loss arrows nor creates a speed-outage exception,
**And** source events scripted while disconnected cannot arrive through a hidden bypass. On recovery, distinguish a genuinely first-received incident from replay of an incident received before the outage,
**And** recovering connectivity first shows checking/pending updates; successful source refresh and any simulated receipt state remain separate. Include a case where connectivity returns but source retrieval still fails/returns only part of its response,
**And** preserve active trip, manual corrections and pending fictional work; restoration is not a fresh position, new day or blanket server confirmation. The static demo still makes no actual private API/database calls,
**And** explicitly identify this as injected connectivity failure. It is not evidence of actual tethering loss, full offline asset readiness, Access recovery or PostgreSQL settlement; those remain separate delivery/qualification tests.

**Given** the signal-quality contract from 3.1/3.2 and the shared progression engine,
**When** the assessor selects the positioning/speed scenarios,
**Then** demonstrate separately: genuine startup before first valid speed, speed loss with usable position, qualified position loss with usable speed, and combined signal loss after a valid measurement,
**And** use the adopted signal-quality rules and explicitly record their configuration/version in the fixture; do not invent unqualified sensor thresholds or treat a simulated successful threshold as real-device evidence,
**And** missing/stale speed remains unknown, not zero. After a previous valid speed including zero, show the five-minute restriction from established outage onset and test immediately before, at and after its expiry; visible startup/outage exceptions explain availability without claiming standstill,
**And** unknown speed alone does not enable direct stop arrows. Only qualified position loss exposes them, with each press moving at most one known stop in the selected trip; manual correction stays manual evidence,
**And** restored valid speed immediately applies its own permission rule. Reliable motion stays locked even after the five-minute exception; restored position alone cannot establish standstill,
**And** recovered positioning uses the correct stop occurrence within the selected trip, preserves the manual pin/history and keeps ambiguity visible. An observation gap remains visible and cannot count as proof that unobserved passages met the 100-metre target.

**Given** outage timing, manual correction or pending fictional notice events exist,
**When** the scenario advances time, reloads, recovers or explicitly restarts,
**Then** any time-step control advances a clearly simulated clock coherently across observation ages, outage timers and source lifecycle; it must not directly unlock controls or refresh an old zero sample,
**And** reload within a run preserves established startup/history/outage timing under the existing compatible recovery contract. Stale observations remain stale; unreadable timing state yields honest restricted uncertainty rather than a new startup exception or guessed elapsed time,
**And** distinguish an explicit new-run restart from same-run reload. Only the former intentionally resets the fixture under 8.1; neither action can affect private data or operational sessions,
**And** inject combinations in both recovery orders: network returns while positioning remains lost, and positioning returns while source access is still unavailable. Recovery of one channel cannot clear the other's warning or grant its permissions,
**And** late callbacks, audio attempts and scheduled source events from the old run are cancelled or rejected after restart, including when they arrive at the same simulated time as a new-run event,
**And** simulated clocks never establish trustworthy timing for 5.4/7.1 server eligibility or alter the adopted access/retention rules.

**Given** scripted scenario definitions and per-run state,
**When** they are saved, replayed or fail,
**Then** reuse 8.1's separated demo storage and existing domain contracts, recording only fictional run state and the bounded metadata needed for repeatability; no private data, credentials, endpoints or cross-origin relay is introduced,
**And** demo controls/adapters remain excluded from private runtime. The same operational engine must handle equivalent typed inputs without a demo-only exception in its business rules,
**And** fixture load, storage or adapter failures produce a visible fictional error with retry/restart and no private fallback. Reset never clears another origin's data,
**And** keep controls keyboard accessible and separate from the operational view, with explicit selected-state and failure labels; countdown accessibility announces meaningful permission changes rather than every second,
**And** do not add a demo database or claim real FastAPI/PostgreSQL evidence. Existing fullstack behavior must be tested with the private application's authorized fictional fixtures in a separate E8 slice.

**Given** the versioned fixtures, shared implementation and ordinary PC browser,
**When** this slice is verified,
**Then** record starting state, injected sequence, expected and observed domain/UI results for each of the three scenario groups and the two combined-recovery orders, and repeat each from a fresh run,
**And** test new versus duplicate/updated/ended notices, irrelevant-before-relevant receipt, source partial/failure, browser audio blocked/uncertain and the exact actually displayed versions retained in summary/PDF,
**And** test network-only failure, speed-only loss, position-only loss and combined loss, including valid zero before loss, stale zero after reload, invalid sample bursts, five-minute boundaries, one-step correction and ambiguous return to a repeated stop,
**And** explicitly restart with pending source replies, an outage timer and an audio attempt; deliver the old callbacks and verify that none affects the new run. Test reload separately so it cannot reset an ongoing outage,
**And** inspect isolated network/storage behavior and simulation labels, preserving a synthetic private sentinel unchanged. Record actual browser/build/fixture identifiers and failures; do not premark scenarios passed or treat screenshots alone as evidence of engine behavior,
**And** a failure against the adopted rules is an implementation finding requiring correction or an explicit owner decision; it cannot be hidden by changing the expected fixture or silently weakening V1 behavior.

**Traceability:** Required FR-25 failure/recovery scenario portion and UX-DR37/UJ-2, using FR-9/12–20 behavior, FR-22/23 labelled evidence and NFR-1–4. UX-DR14/15/19–23/33/35/38/39/44 as consumed by shared views. EXPERIENCE repeatable new-notice/internet/GPS loss, qualified exceptions and honest recovery; DESIGN distinct simulation controls and uncertainty labels. AD-1/3 shared ports/engine, AD-2 isolated local persistence, AD-7/8 source semantics, AD-9 independent position/speed and manual authority, AD-10/13 demo isolation and AD-14 compatible recovery. AD-4/5 real backend evidence and AD-12 private expiry remain binding elsewhere, never satisfied by a simulated acknowledgement. All AD-1–AD-14 remain unchanged.

**Dependencies:** 8.1 isolated entry/reset/basic scenario; implemented 3.1/3.2 quality/permission, 3.7/3.8 correction/recovery, E4 source/display/audio through 4.8 and 5.6 reconnect behavior, plus the existing E7 summary/export. No future E8 story is required to run these fictional scenarios locally.

**Size boundary:** Three bounded failure-scenario groups plus their interaction/recovery cases over existing engines. No generic scenario-authoring UI, new operational/source engine, live-source/device qualification, complete mentor scenario catalogue, deployment or private fullstack evidence package. Scenario definitions and controls are fictional adapters, not production bypasses.

**Qualification boundary:** Contributes repeatable evidence to E8-D without passing that checkpoint alone. E8-P still requires actual source/OCR/Lenovo/Brave/access/host/offline/lifecycle qualification; E8-E remains the subsequent three-workday evaluation. TIME-01 implementation and qualification remain open. No application implementation, actual scenario execution, readiness/final validation, provisioning or deployment occurs during this planning step.

**Approval:** Approved by the owner on 2026-09-27 as scoped. The owner emphasized independent network, position and speed cases and that simulated outcomes must never be presented as actual source or sensor evidence. Planning approval only; the approved copy in epics.md is canonical.
