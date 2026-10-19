---
title: Implementation Readiness Check — IBE160 Bus Driver Assistant
date: 2026-09-27
workflow: bmad-sprint-planning
intent: readiness
gate: PASS
status: betinget-implementeringsklar
---

# Implementation Readiness Check

## Gate decision

**PASS at the BMAD planning gate; status: betinget implementeringsklar for avgrenset oppstart after the owner's TIME-01 and IR-01 decisions (2026-09-27).** The cross-cutting time policy in 5.4/7.1 and the measurable visual acceptance floor are now recorded in the approved requirements, UX and affected stories. First durable server activation acceptance must precede E; original server-issued Tg bounds unverifiable offline-end retention; uncertain-time offline restart locks the local copy pending trusted control. IR-01 sets 4.5:1 informative text, 3:1 necessary non-text and the specified focus area/contrast in Day, Night and both Auto outcomes, with rendered-PDF and semantic-icon checks. These are approved requirements, not implemented or tested capabilities. PASS here means the recorded plan can be implemented without inventing these decisions; it is not a full-V1 or pilot pass.

**Bounded implementation may start:** Story 1.1's private fullstack vertical slice and the independent early investigations in 2.1, 2.2, 3.1 and 4.1 have recorded scope and prerequisites. TIME-01 and IR-01 affected stories may now be implemented against the amended criteria in declared dependency order; positive acceptance still needs executed evidence. UI, semantic-icon, focus and rendered-PDF contrast measurements, mounted Lenovo/Brave readability and the E8-D/P/E gates remain unexecuted. This gate result does not authorize actual working shifts or treat planned tests as passed.

This report began as a readiness-only check. On 2026-09-27 the product owner separately adopted TIME-01 and IR-01 and authorized synchronized source-artifact amendments; this revision records their effect. No sprint tracking file, implementation or qualification result is generated here.

## Authoritative input and completed checkpoints

| Input | Role in this check |
|---|---|
| [Final PRD](prds/prd-IBE160-2026-09-21/prd.md) and [PRD addendum](prds/prd-IBE160-2026-09-21/addendum.md) | Approved requirements, decision register, downstream validation and external facts. Historical addendum questions do not reopen resolved PRD decisions. |
| [DESIGN](ux-designs/ux-IBE160-2026-09-22/DESIGN.md), [EXPERIENCE](ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md) and [UX validation](ux-designs/ux-IBE160-2026-09-22/validation-report.md) | Adopted visual and interaction rules; the validation claim checked in IR-01. |
| [Architecture Spine](architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md) | Adopted AD-1–AD-14, contracts, deferred story-level choices and five pre-pilot release gates. |
| [Canonical epics and stories](epics.md), 80 files in [story-drafts](story-drafts/), and [step-5 final validation](epics-final-validation.md) | Approved allocation, individual acceptance/dependency boundaries and prior document-only validation. |
| [Product Brief](briefs/brief-IBE160-2026-09-21/product-brief.md) and [development log](../../Docs/development-log.md) | Intent, precedence and known unexecuted work. |

| Mandatory readiness checkpoint | Result |
|---|---|
| Artifact inventory | The current approved PRD, two UX spines, Architecture Spine and canonical epics/80 individual stories are identified. No missing main artifact or competing current version was found. |
| Forward/backward traceability | FR-1–25, NFR-1–4, UX-DR1–44 and AD-1–14 are allocated in the inventory and individual story traceability. Each of the 80 story files has approval, acceptance criteria and a source trace. UX-DR45 is explicitly outside V1. No orphan requirement or story was identified. |
| Epic/story dependencies and bounded completion | The 80 stories declare 299 edges; every edge points to an existing earlier story. The five independent roots are 1.1 and early qualification stories 2.1, 2.2, 3.1 and 4.1. No cycle or unowned interface was found. E1/E5, E2/E6, E3/E4/E6 and E5/E7 seams have explicit owners and bounded tests. TIME-01 supplies the formerly missing policy for 5.4/7.1; positive acceptance still requires implementation and tests. |
| Architecture and UX decisions | AD-1–AD-14 and the principal interaction, privacy, offline, source, release and presentation rules are recorded. Detailed DTOs, tested sensor thresholds, Auto trigger and responsive breakpoints are assigned to affected stories; material evidence failures return for an owner decision. IR-01 now supplies the missing measurable contrast floor; measurements remain open. |
| Conflicts between artifacts | TIME-01 is recorded in PRD FR-1/17/20/23/24 and NFR-3, UX DESIGN/EXPERIENCE, architecture AD-10/12 and the canonical and individual affected stories. IR-01 is recorded in PRD NFR-1, UX DESIGN/EXPERIENCE and affected stories; UX validation R2's former completion claim is explicitly corrected. Historical step-5/validation passages remain under the explicit epics supersession register. |
| Practical implementability and evidence | Early investigations, real fullstack demonstration, five pre-pilot gates and later field evaluation have distinct owners and evidence requirements. They are planned, not passed. External inputs and scheduling remain visible. |

## Closed policy decisions and open verification

### TIME-01 — Disconnected-time policy selected (high impact; decision closed)

**Adopted decision and trace.** The owner selected a strict V1 rule in [FR-1/17/20/23/24](prds/prd-IBE160-2026-09-21/prd.md), [EXPERIENCE TIME-01](ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md), [AD-10/12](architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md), [5.4](story-drafts/story-5.4.md) and [7.1](story-drafts/story-7.1.md). Fixed server E is app_authenticated_at plus fourteen days. The activation transaction and receipt must durably commit before E; first acceptance at/after E is rejected regardless of claimed offline start. A matching pre-E receipt whose response was lost can be retrieved. Original server-issued Tg, from a final grant within 24 hours before first planned activity, gives conservative `D = min(Tg + 7 days, earlier binding data deadlines)` for unverifiable offline end. An offline uncertain-time restart locks private view/actions/export until trusted control; expired copies are deleted before view. A never-returning tablet has no verified local deletion. The pre-start and persistent unresolved-state warning, approved-day post-E review/export, rejected-work marked local export and pilot custody/reconnect/hand-in/wipe procedure are assigned to amended stories and E8-P tests.

**Decision owner and route.** Product owner decision recorded 2026-09-27. The change is a direct adjustment to E5/E7/E8 without a new epic or a claim of completed implementation. Earlier 5.4 post-E timing-proof acceptance and PRD/UX exact seven-days-after-unverified-offline-end wording are superseded. The app lock is not encryption or exact-time physical deletion.

**Required follow-up.** Implement and test activation, delayed/lost receipt, strict E, Tg/D, clock change, offline ending, uncertain-time lock, expiry before display, rejected-result export and pilot device procedure in 5.4/7.1 and their E5/E7 integrations. [8.9](story-drafts/story-8.9.md) must report passed, failed, blocked and not-run actual-device evidence; [8.11](story-drafts/story-8.11.md) cannot grant E8-P permission without applicable passes and a later dated owner decision. [8.12](story-drafts/story-8.12.md) cannot begin actual-shift evaluation before a positive E8-P decision. No test is claimed passed by adopting TIME-01.

### IR-01 — Numerical contrast acceptance floor (medium impact; decision closed, evidence open)

**Original finding and resolution.** [UX validation R2](ux-designs/ux-IBE160-2026-09-22/validation-report.md) had claimed numerical requirements were already added; [DESIGN](ux-designs/ux-IBE160-2026-09-22/DESIGN.md) contained only selected base-palette calculations. The owner has now set the V1 project floor in [NFR-1](prds/prd-IBE160-2026-09-21/prd.md), [DESIGN](ux-designs/ux-IBE160-2026-09-22/DESIGN.md) and [EXPERIENCE](ux-designs/ux-IBE160-2026-09-22/EXPERIENCE.md): at least 4.5:1 for every informative text pair; 3:1 for necessary non-text information; and a visible focus indicator with at least a 2 CSS-pixel-perimeter-equivalent area, 3:1 focused/unfocused pixel change and 3:1 against necessary adjacent colors, without total obscuring. Day, Night, both Auto outcomes and relevant states apply; color alone cannot convey state. This is not a claim of overall WCAG AAA conformance.

**Decision owner and route.** Product owner decision recorded 2026-09-27. The original missing-threshold/document-mismatch question is closed. Bounded implementation checks belong to [1.1](story-drafts/story-1.1.md), [1.3](story-drafts/story-1.3.md), [3.5](story-drafts/story-3.5.md), [3.14](story-drafts/story-3.14.md) and [7.4](story-drafts/story-7.4.md); [8.8](story-drafts/story-8.8.md) owns separate mounted-device observation. The identical amendments are in canonical [epics.md](epics.md).

**Required follow-up.** Measure actual rendered UI pairs/states and necessary semantic icons. DESIGN calculates the bare yellow sun token against white at 1.59:1; the static driving SVG adds a dark under-stroke/outline calculated at 17.93:1 against white, but its implemented silhouette/edge has not been measured across states and requires correction if it fails 3:1. Measure focus area and both contrast relationships. Check every page/variant of the **rendered PDF separately** from browser CSS or token calculations. Record raw ratios, states, build and pass/fail/blocked/not-measured outcomes. Actual Lenovo/Brave legibility/glare/glance and applicable E8 gates need later observed evidence. None is passed by this decision.

## Work that can start versus later gates

| Stage | Permitted claim and current limit |
|---|---|
| Start of implementation | Begin 1.1 and independent 2.1/2.2/3.1/4.1 investigations; continue other stories only after recorded prerequisites. TIME-01 gives 5.4/7.1 implementable behavior; IR-01 supplies measurable visual criteria. Source/OCR/device failures may require a later explicit solution decision. |
| Affected story acceptance | Full positive 5.4/7.1 acceptance requires implemented and executed TIME-01 tests. Positive 1.1/1.3/3.5/3.14/7.4 visual acceptance requires executed IR-01 checks, including rendered PDF in 7.4. Mounted 8.8 requires actual-device observation. None is supplied by the policy decisions alone; partial implementation and honest negative/blocked evidence remain possible. |
| E8-D demonstrable delivery | [8.3](story-drafts/story-8.3.md) requires the actual private React/FastAPI/PostgreSQL chain; [8.6](story-drafts/story-8.6.md) records the versioned delivery, repeatable fictional PC demo and limitation matrix. A static demo or planned test is not fullstack evidence, and E8-D is not pilot permission. |
| E8-P permission before real shifts | [Architecture's five release gates](architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md) require actual import/source, mounted-device, durability/recovery, access/deployment and compatible-release evidence. [8.7–8.10](epics.md) gather it; 8.11 requires applicable passes, resolved blockers and an explicit dated owner decision for the exact candidate. No such results or decision exist yet. |
| E8-E field evaluation | 8.12 follows only a positive E8-P decision and an agreed protocol, then records three actual assigned days and measured/uncertain/negative outcomes. It is not an implementation-start prerequisite. |

## Known external prerequisites and unexecuted qualification

| Item | Owner / needed by | Current treatment |
|---|---|---|
| Representative anonymized PDF/image cases and checked shift facts; real timetable and Svipper reference/source access | Product owner and implementation owner; 2.1, 2.2, 4.1, then 8.7 | Inputs/evidence not established by document approval. Missing categories and source updates/closures remain unqualified, not passing samples. |
| Actual Lenovo/Brave, mount and safe observations; trusted HTTPS; source/device capability | Product owner and implementation owner; 3.1, 3.14/3.15, then 8.8 | Device reliability, 100-m progression, Auto, wake, audio, readability and touch remain untested. A manual fallback does not pass an automatic capability. |
| Owned domain/account/identity, secrets, provider upload/cache/logging handling, Windows host and controlled restart/resource observations | Product owner/operator and implementation owner; 8.5 and 8.10 before real private files/pilot | Provisioning and provider/host evidence remain open. The adopted Windows sign-in and no-historical-backup limitations do not waive their tests. |
| Exact course submission date, assessment access end and browser/environment | Product owner via course staff; PRD C-1–C-3, 8.5/8.6 delivery scheduling | Unknown external facts; no invented dates or browser claim. |
| Field protocol, assigned days and realistic remaining effort/delivery plan | Product owner and implementation owner; protocol before 8.12, estimates after early qualification | More than 40 hours is known; neither 40 nor 160 hours is a fixed available budget. No silent requirement deferral or schedule assurance. |

No application implementation, actual source/OCR/device/provider/host/compatibility tests, provisioning, deployment or field evaluation was performed during planning. Planned checks in stories are obligations, not passed evidence.

## Controlled documentation deviations

The [epics supersession register](epics.md) identifies the governing decisions for earlier PRD wording on import formats, stop order, activity labels, movement policy, demo login and original-file retention, plus TIME-01's override of older timing/retention language. AD-6's transient originals govern older UX retention wording. [Story 7.2](story-drafts/story-7.2.md) governs explicit initial-review closure. Historical step-5 validation and dated approval notes describe the state before the later TIME-01/IR-01 decisions; the amended approved sources govern implementation. UX validation R2's former completion claim is preserved as corrected history, not measured evidence.

## Next decision sequence

1. Run the early bounded investigations and begin authorized implementation slices, including TIME-01 and IR-01 criteria in their owning stories; record negative or unavailable evidence honestly.
2. Execute TIME-01 controlled tests and IR-01 rendered UI, semantic-icon, focus and PDF measurements. Gather actual Lenovo/Brave and pilot-procedure evidence through 8.8/8.9/8.11.
3. Perform E8-D, E8-P and E8-E only at their separate later evidence stages; reassess any failed or blocked gate before the relevant owner decision.
