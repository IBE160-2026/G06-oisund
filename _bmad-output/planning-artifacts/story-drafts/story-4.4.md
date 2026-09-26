---
status: approved
created: 2026-09-26
epic: E4
story: '4.4'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['4.3', '2.12', '3.9', '3.10']
---

## Epic 4: Understand Relevant Notices and Their Sources

This slice determines evidence-backed relevance to the confirmed whole day, actual active context and the separately eligible next-trip preview. It returns a locally usable, testable relevance contract; the following presentation stories consume it. It does not introduce a second operational engine or claim that the production notice list, seen-state, staged driving warnings or audio are already implemented.

### Story 4.4: Match Notices to the Confirmed Day and Actual Trip with Explicit Uncertainty

As the driver,
I want notice relevance to follow my confirmed work and actual trip using supported source references,
So that a shared line number or scheduled change does not confidently attach a notice to the wrong trip or hide uncertainty.

**Acceptance Criteria:**

**Given** canonical source versions from 4.3 and a confirmed own working-day revision,
**When** relevance is evaluated,
**Then** use qualified source-namespaced route/trip/direction/stop/area references and validity evidence, with the E2 service-date and transit-identity mapping,
**And** return supported associations, potentially applicable but uncertain associations, and evidence-backed exclusions distinctly, recording what evidence or missing fact supports each decision,
**And** separate relationship certainty, source lifecycle, coverage and freshness; a precise match to stale source data is not fresh verification,
**And** equal display line numbers, nearby stops or roadworks text alone cannot establish exact trip/direction/trajectory applicability,
**And** distinguish an explicitly source-defined route-wide/all-direction scope from an absent direction field; do not require a stop restriction when the source explicitly applies to the whole route,
**And** unsupported mappings remain unknown rather than guessed or silently excluded as irrelevant.

**Given** several trips, split work parts and multiple notices across lines 20, 24, 28 and 42,
**When** the preparation/whole-day relevance result is assembled,
**Then** include distinct applicable incidents across the combined confirmed day with all supported activity/trip/time associations,
**And** one source incident affecting 20 and 24 appears once with both associations; a separate moved-stop incident remains distinct even with a similar title,
**And** associate only the time/direction/stop portions actually supported rather than implying an all-day line tag affects every trip,
**And** an unconfirmed draft or removed future activity cannot supply confirmed relevance; performed/history evidence is not erased by recomputing remaining-plan associations,
**And** notices with no defensible day connection do not all become driving warnings; retain the relevant coverage/mapping gap without presenting an unfiltered regional feed as applicable.

**Given** explicit source validity intervals and dated trips spanning midnight,
**When** planned-day or active-trip relevance is assessed,
**Then** preserve the shift service date and order while comparing appropriate calendar instants with the source's qualified timezone/boundary semantics,
**And** test Friday 25:30 as Saturday 01:30, including multiple trips displayed as Saturday 01:30 with different identities/service dates; display time alone cannot merge or select them,
**And** preparation uses known planned intervals with their planned provenance, whereas an actually delayed active trip is reassessed against actual current context/time without being replaced by the next scheduled trip,
**And** unknown actual passage time cannot establish that a narrow validity interval definitely included or excluded an unobserved passage,
**And** handle multiple validity periods and gaps through 4.3's lifecycle/validity facts, not by declaring the incident closed or changing source versions.

**Given** a selected actual trip, retained manual pin or uncertain progress,
**When** the active relevance result is evaluated,
**Then** use the committed E3 trip/context rather than selecting another trip from schedule, proximity or a notice's line number,
**And** trip-level relevance can remain supported while current stop/approach is unknown; missing GPS does not itself remove a route-wide applicable notice,
**And** stop references map to the correct supported occurrence(s) within the selected trip; repeated visits to the same stop cannot be reduced to the first occurrence by name/proximity alone,
**And** choosing a particular occurrence requires a documented applicable time or other source evidence that distinguishes it; without that evidence retain an uncertain association and never select one occurrence by guessing,
**And** where source evidence explicitly supports all visits, preserve that scope rather than arbitrarily narrowing it; otherwise repeated-stop ambiguity remains visible,
**And** test two visits to the same physical stop with (a) source evidence selecting one occurrence and (b) no distinguishing evidence: only (a) yields that specific occurrence, while (b) stays uncertain through save/reopen and recomputation,
**And** this contract supplies supported scope/occurrence evidence but does not itself fire the later approach/departure presentation triggers.

**Given** E3 registers final-stop arrival, including a manual arrival with its provenance,
**When** next-trip notice eligibility is evaluated,
**Then** make the confirmed next-trip relevance result available as a separately labelled preview scope immediately, without waiting for the ordinary ten-second display transition,
**And** do not change active trip, release its pin, complete the workday or start the return trip merely to make notices available,
**And** same-route return waiting still requires 3.9's independent start evidence or separate qualified-loss Next action; schedule, sustained position and timer expiry cannot activate it,
**And** preserve any intervening non-passenger activity and distinguish current-activity notices from later passenger-trip preview; do not pretend the passenger trip is underway,
**And** missing/ambiguous next-trip context remains unknown, and a corrected final-arrival/context invalidates an obsolete preview rather than showing stale results,
**And** exposing an already retrieved notice in this preview creates neither a new source version nor new-notice eligibility for sound.

**Given** deadhead, meal/layover, bus change, pilot-car transfer or depot activity,
**When** current-activity relevance is assessed,
**Then** include only associations supported by the known activity location/time and qualified source scope, with uncertainty where those facts are insufficient,
**And** a warning for the next passenger starting stop may be associated with that stop/next trip without asserting that it lies on the actual deadhead road path,
**And** no source notice or empty result proves a clear road, completed physical action or precise road-by-road coverage,
**And** do not calculate a deadhead route, infer an unprovided trajectory or add other road-event providers; those remain outside adopted V1 integration.

**Given** a source update, confirmed scoped plan revision, manual trip correction or context change,
**When** relevance is recomputed or a pending calculation returns,
**Then** bind the result to the owner/day, confirmed plan revision, source material version and active/preview context used to compute it,
**And** reject a stale result that would replace associations for newer committed inputs; plan/source changes cannot overwrite driver corrections, actual trip or prior evidence,
**And** local context or plan changes can change relevance but cannot manufacture a source version, reset future seen/registered/hidden state for unchanged versions or reclassify an old receipt as a new notice,
**And** a confirmed source closure removes active-warning eligibility immediately when accepted; retained overview/history eligibility remains distinct for later client lifecycle handling,
**And** source disappearance/ordering uncertainty retains its explicit status and applicable uncertainty rather than being silently treated as no warning.

**Given** source data was downloaded and relevance can be computed locally,
**When** connectivity is lost or a compatible view reopens,
**Then** reuse the shared React-independent TypeScript domain boundaries and committed E2/E3 context to evaluate available data without a backend round trip,
**And** persist the minimum source snapshot and revision/context references in the existing private IndexedDB day store before claiming local availability; derived associations may be recomputed from those exact inputs,
**And** retain explicit missing data, source/client receipt freshness and uncertain restored position; reconnect or reopen does not make facts fresh or restart movement exceptions,
**And** failed reads/writes produce an unavailable/stale-result state, not an empty successful match set or a falsely saved result,
**And** authenticated FastAPI/PostgreSQL source retrieval remains 4.2/4.3's responsibility; derived relevance alone does not create operational outbox events, a duplicate backend operational engine or an unrelated database table,
**And** full offline boot, authority and cross-client reconciliation remain E5; this bounded local evaluation does not claim that entire capability.

**Given** relevance outputs are consumed by later overview/driving surfaces or test fixtures,
**When** the contract is inspected,
**Then** expose stable incident/version identity, association scope, user-understandable applicability/uncertainty reasons and original-source metadata sufficient for honest presentation,
**And** keep active warning eligibility, upcoming preview and retained overview/history distinct; no consumer should need to infer source closure or trip activation from an empty list,
**And** make no client seen/acknowledgement, popup, sound, focus or operational state change merely by computing/recomputing relevance,
**And** verify results with labelled reference cases before the later UI stories, without routing simulated source or movement data into the operational app.

**Given** private plan-to-notice associations or stored input snapshots,
**When** access, cleanup or recovery runs,
**Then** use existing owner/day access and pending-logout locks before reading or exposing private associations; a public source cache does not receive private plans or day links,
**And** apply the existing AD-12 deadline to private copies without extending it on recomputation, download or reopen; source-cache pruning cannot silently remove facts already retained for an unexpired day,
**And** retain no permanent notice-to-driver profile, raw GPS archive or private identifiers in public test artifacts,
**And** ordinary source polling/read success cannot renew day authority or bypass E5's remaining continuation controls.

**Traceability:** FR-12 day/current/next-trip relevance; FR-13 honest source metadata/coverage; FR-14/15 no false newness on context changes; bounded FR-17/20 local-data use. NFR-2/3/4; UX-DR9/19/20/21/23/44 and EXPERIENCE split-day/last-stop notice rules. AD-1/2/3 local domain and available data, AD-5 revision/identity separation, AD-7 qualified references, AD-8 source versus local state, AD-9 actual-trip authority, AD-10/12 access/retention and AD-14 compatible recovery. Movement-restricted presentation remains the later UI's required reuse of 3.2.

**Dependencies:** Implemented 4.3 canonical source contract and actual 4.1 evidence; E2 confirmed dated plans and scoped revisions through 2.12; E3 committed selection/terminal/non-passenger context through 3.9/3.10. The bounded own-day relevance contract is independently testable before future E4 lists/detail/driving/audio. E6 later extends explicit linked-person/block context without treating a linked plan as an own trip or changing source facts.

**Implementation evidence:** Reference matrix with positive/negative/uncertain source matches across pilot lines, explicit broad scope versus missing metadata, overlapping directions, one multi-line incident versus separate incidents; split work and midnight collisions; multiple validity periods, delayed trip and unknown passage; repeated stop occurrences; final-arrival preview before ten seconds and return wait; non-passenger/limited deadhead scope; source/plan/context races, closure and uncertain disappearance; local available/missing/stale data, storage failure, logout and expiry. Expected associations must have source/reference ground truth; report unsupported cases. Tests are planned, not run.

**Size boundary:** Own-day/active/preview relevance rules and minimal persisted inputs, exposed as a tested domain contract. No full notice list, detail/seen/registered/hidden state, ten-minute display timer, staged/immediate driving rendering, audio, mentor UI, new source integration, routing or general offline engine. The following stories deliver the user-facing notice presentation; no future story is a prerequisite to test this contract.

**Pilot qualification:** Labelled deterministic relevance fixtures contribute to E8-D. E8-P requires actual source mappings and integrated target-device notice presentation/recovery; correct synthetic matches do not prove live coverage or freshness. E8-E remains later field evaluation. No V1 requirement or qualification gate is waived.

**Approval:** Approved by the owner on 2026-09-26 with an explicit repeated-stop constraint: a particular occurrence requires documented time or other distinguishing source evidence. Without it the association remains uncertain; no occurrence is selected by guessing. Planning approval only; the approved copy in epics.md is canonical.
