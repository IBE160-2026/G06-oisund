---
status: approved
created: 2026-09-26
epic: E4
story: '4.6'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['4.5', '3.5', '3.8', '3.9']
---

## Epic 4: Understand Relevant Notices and Their Sources

This slice integrates qualified notices into the adopted active-driving composition, using the existing relevance, source lifecycle, version state and operational progression. Planned stop-specific warnings and newly received acute warnings have distinct presentation triggers. It supplies display evidence but no new movement engine, acknowledgement/manual hiding or audio behavior.

### Story 4.6: Show Relevant Driving Warnings at the Correct Actual Progression State

As the driver,
I want relevant warning headings to appear alongside the actual trip and stop context at the agreed moment,
So that I can notice the information with a brief glance without opening content or operating the website while moving.

**Acceptance Criteria:**

**Given** an authorized actual active trip/activity with qualified source and relevance state,
**When** the driving notice area renders,
**Then** show only supported current-context notices and explicitly labelled uncertain relevance where appropriate, preserving source/freshness limitations,
**And** retain route/destination, the correct current/next stop roles, clock, always-visible Menu/reason/countdown and always-available Day/Night/Auto control,
**And** use the accepted notice/stop side-by-side composition and hierarchy; notice prominence may temporarily dominate without erasing stop context or altering trip/progression,
**And** exclude personal imported details and never display an unfiltered whole-day/regional notice list as current-trip warnings,
**And** respect 4.5's version-specific bold/changed cues; showing a heading or warning triangle alone does not mark the detail version seen.

**Given** a planned stop-specific notice with a supported affected occurrence in the selected trip,
**When** actual committed progression changes,
**Then** show the outlined yellow warning triangle immediately after the affected stop name when it is two stops ahead,
**And** while at the preceding stop, retain the triangle but do not automatically show the prominent message merely because the affected stop is next,
**And** after supported departure/passage from the preceding stop, while approaching the affected next stop, automatically show the concise warning heading,
**And** retain that message through arrival/dwell at the affected stop, with its current-stop context visible,
**And** after supported onward departure/passage of that occurrence, clear its prominent message and restore ordinary stop focus without ending the source incident or deleting overview/history evidence,
**And** test all five states including passage without stopping; scheduled times, animations and a proximity value alone cannot trigger them.

**Given** unknown position, manual stop correction or recovery after an observation gap,
**When** presentation evaluates approach, dwell or onward passage,
**Then** use only supported E3 committed state and its observed/manual/uncertain provenance; do not create a separate inferred progression engine,
**And** unknown position alone cannot establish an approach or clearing trigger; retained context remains visibly uncertain rather than pretending a new measurement,
**And** a permitted manual correction can update the displayed context under the approved E3 semantics without becoming GPS evidence,
**And** a qualified later-stop recovery may update current presentation but must preserve the observation gap; never backfill warning displays at unobserved earlier stops or claim the 100-m target was met there,
**And** at sequence boundaries or missing stop lists, retain relevant trip-level headings and honest missing/uncertain stop context without inventing a preceding stop or staged trigger.

**Given** the selected trip visits the same physical stop more than once,
**When** a source notice could refer to several occurrences,
**Then** use 4.4's documented-time/other-source-evidence rule before assigning an occurrence-specific warning trigger,
**And** without that evidence keep the association explicitly uncertain, with no guessed occurrence, precise approach claim or automatic clearing at an arbitrarily chosen visit,
**And** if source evidence explicitly supports all visits, apply the relevant occurrence context to each supported visit rather than treating the first passage as source closure,
**And** test first-versus-later visit, ambiguous association and explicit all-visits scope separately; repeated exposure never creates a new source version or new receipt.

**Given** a newly received acute notice is supported as relevant to the ongoing trip,
**When** the app has received the notice and assessed it as relevant to the ongoing trip,
**Then** show its concise heading immediately in the right-hand information area, retaining stop context to the left and route/destination above,
**And** immediate presentation is measured from that app receipt/relevance decision, not source publication; separately record source publication/update time where supplied, app receipt/relevance decision and actual display for the test,
**And** test delayed provider delivery and delayed polling: no source-to-screen immediacy is claimed, while the accepted relevant notice is shown without waiting for the planned-stop trigger,
**And** do not wait for an affected stop to become next or require the planned-stop approach trigger,
**And** use no covering modal, animation, focus theft, required acknowledgement or automatic detail/source opening,
**And** preserve explicitly uncertain relevance where source evidence is incomplete; a line-number match alone cannot become certain trip applicability,
**And** acute classification must be supported by qualified source semantics, not guessed from dramatic wording; this behavior does not promise a working or complete acute-event feed,
**And** a route-wide acute warning remains governed by its relevance/source lifecycle, not removed merely because one stop was passed; a supported stop-specific message follows its onward-passage clearing rule.

**Given** two important applicable notices are simultaneously eligible for prominent display,
**When** the driving composition updates,
**Then** show both short headings together without rotation/carousel, modal overlap or hiding route/stop/control context,
**And** keep their identities, sources, uncertainty and version state distinct; a shared incident is not duplicated per affected line,
**And** preserve readable titles and essential text rather than shrinking them merely to fit or requiring the moving driver to scroll/respond,
**And** when more than two important notices are simultaneously applicable, visibly indicate that additional notices exist, with an accurate count or equally clear text; they cannot silently disappear from the driving view,
**And** keep the additional notices available through the existing movement-governed overview/detail path without requiring interaction while moving, automatic rotation or hiding the overflow indication,
**And** test three or more notices, new arrivals, closure and context changes so the additional-notice indication stays accurate; assess long names/layout capacity without inventing severity from unavailable source data.

**Given** source closure/update, onward stop passage, a context correction or final-stop next-trip eligibility,
**When** visible warnings are reconciled,
**Then** use the current source version, plan revision and committed actual/preview context; stale rendering callbacks cannot restore an obsolete warning,
**And** confirmed source closure removes its active heading and stop markers immediately on accepted state, while 4.5 separately manages its ten-minute struck-through overview entry,
**And** clearing one stop-specific message does not resolve the incident, clear unrelated warnings or erase prior displays,
**And** next-trip notices may appear from 4.4's separately labelled preview at registered final arrival before ten seconds without activating that trip or starting a same-route return,
**And** retain intervening non-passenger activity context and limited deadhead coverage; source/context changes do not silently switch actual trip or reset its pin,
**And** updates, later relevance and repeated displays do not by themselves become new-notice events; this story emits no chime.

**Given** the driver attempts notice detail or original-source access from the driving view,
**When** the action is invoked or reliable movement returns,
**Then** reuse 4.5's exact-version detail/seen handling and 3.2's shared standstill/startup/outage permission at invocation and display, with immediate restricted-detail collapse on motion,
**And** only actual authorized display of that version's content can record seen; a rejected press, heading-only presentation or view closed before content appears cannot do so,
**And** return focus to a visible appropriate control after closure; source access cannot bypass movement restrictions,
**And** automatic warning presentation never opens detail, marks understanding or offers a supposedly working Registrert/swipe action before its later story.

**Given** a warning or marker is actually rendered, updated or removed from the driving surface,
**When** display evidence is recorded,
**Then** extend 4.5's day evidence with the exact version, actual/preview context, display kind and supported observed/manual/uncertain progression needed by the later summary,
**And** distinguish receipt, eligibility, marker, heading and authorized detail display; an eligible item that was never rendered is not recorded as shown,
**And** do not infer the driver read or acted on a displayed warning; no raw GPS archive or per-render/per-poll event stream is introduced,
**And** persist the minimal state/evidence and required outbox events atomically, using inherited FastAPI/PostgreSQL ownership/revision checks and matching receipts,
**And** local or server failure is reported honestly: unsaved evidence is not labelled saved and a server error cannot discard an accepted local event or reset version state.

**Given** retained notices during source/network loss, compatible reopen or storage/access failure,
**When** driving presentation recovers,
**Then** retain useful permitted information with source-specific stale/unavailable status and uncertain restored position, never treating reconnect/reopen as fresh evidence,
**And** preserve existing seen state and context, with no new startup exception, receipt, source version or forced detail opening,
**And** absent initial data retains the unavailable-source warning rather than implying no disruptions; a failed source does not erase unaffected warnings,
**And** honor private access/logout/expiry before rendering; storage failure cannot fabricate current progress or confirmed display history,
**And** whole-day offline boot/authority/reconciliation remain E5 integration, and full source/device recovery remains E8-P qualification.

**Given** the active-driving layouts in day/night, long Norwegian names, two warnings and retained uncertainty,
**When** accessibility and target-device checks run,
**Then** expose accessible stop roles and associated warning descriptions with meaningful state announcements rather than every sensor tick or duplicate poll,
**And** keep essential labels readable without color alone, preserve keyboard focus and avoid automatic scrolling/attention-stealing transitions,
**And** verify actual mounted Lenovo/Brave glance readability and layout fit separately from screenshot/component checks, with no driver interaction required during moving observations,
**And** use approved DESIGN tokens and keep manual theme/wake behavior independent; a notice cannot reset those controls or the movement/outage timer,
**And** all private snapshots/evidence retain the existing AD-12 deadline, source-cache separation and no-private-data-in-demo/logs rules; display/clear/reopen never extends retention.

**Traceability:** FR-12 current/next relevance presentation; FR-13 source/uncertainty; FR-14 heading/version and closure integration; FR-16 safe interaction; bounded FR-17–20 retained/failure state and FR-22 display evidence. NFR-1–4; UX-DR10/11/12/13/14/19/20/21/23/38/39/40/41/44 and adopted DESIGN driving composition. AD-2/5 local evidence/receipts, AD-7/8 source facts/lifecycle, AD-9 one actual-progression engine, AD-10/12 access/expiry and AD-14 recovery. FR-15 sound and UX-DR22 registration/dismissal remain later stories.

**Dependencies:** Implemented 4.5 and its source/relevance/version foundations; E3 display through 3.5, manual/qualified progression and gap recovery through 3.8, terminal/preview context through 3.9 (non-passenger context inherited through 4.4). Actual source applicability/acute classification and sensor quality must be qualified rather than assumed. No future acknowledgement, sound or summary screen is needed to demonstrate the warning composition and evidence.

**Implementation evidence:** Planned five-stage sequence including non-stop passage, manual versus uncertain progress, gap recovery without backfilled display, repeated stop occurrence with/without source evidence; immediate acute versus staged planned notices and unsupported acute classification; two simultaneous warnings/long names; route-wide versus stop-specific clearing, closure versus overview timer, update/context races and final-arrival preview without return start; rejected/opened detail version tests, actual-render versus merely eligible evidence, local commit/receipt faults, offline reopen/access/expiry, accessible focus/announcements and real mounted glance checks. Tests are specified, not run.

**Size boundary:** Driving composition and presentation triggers using existing source/relevance/progression contracts, with its display evidence and permitted detail reuse. No new source, new sensor rules, operational-engine duplication, acknowledgement/manual hiding, audio, mentoring UI, report UI or general recovery engine. Actual target-device limits are qualification findings, not silently relaxed V1 requirements.

**Pilot qualification:** Labelled progression/source fixtures and fullstack evidence contribute to E8-D. E8-P needs integrated actual source, mounted readability, sensor/progression and offline/authority behavior; acute-feed availability is not established by a working fixture. E8-E remains subsequent real-shift evaluation.

**Approval:** Approved by the owner on 2026-09-26 with immediate acute presentation measured from app receipt and relevance assessment, not source publication. More than two simultaneous important notices must have a visible additional-notices indication and cannot disappear silently. Planning approval only; the approved copy in epics.md is canonical.
