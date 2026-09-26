---
status: approved
created: 2026-09-26
epic: E7
story: '7.6'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['7.1', '7.2', '7.3', '7.5']
---

### Story 7.6: Close with a Varied Factual Greeting and Clear Next Actions

As the pilot owner finishing an ended or aborted working day,
I want a calm closing screen with a brief relevant greeting and clear summary/main-menu actions,
So that I can leave the day without confusing encouragement with verified completion or resuming ended work.

**Acceptance Criteria:**

**Given** the combined own day has a valid locally committed normal-end or abort result from 7.1,
**When** its closing screen is shown,
**Then** display `Takk for i dag`, one short eligible greeting and clear actions for the daily summary and main menu, following DESIGN's centered restrained closing composition, readable type and accessible focus/labels,
**And** distinguish normal end from abort and retain the existing local/server status and relevant access/expiry information. A greeting never certifies server settlement, physical shutdown, rest, handover or completion of uncertain activities,
**And** do not show a final-day closing state solely because a part ended, an intermediate depot was reached, a planned time passed or a pending end action was cancelled/failed,
**And** an unverified locally reported end time remains qualified under 7.1; a clock shown on this screen is not additional timing evidence.

**Given** a static bank of preapproved formulations and permitted retained facts for the specific day,
**When** a greeting is selected,
**Then** select or assemble the greeting only from preapproved formulations with explicit, testable eligibility rules using recorded facts such as split work parts, confirmed plan changes, a recorded guiding assignment or an aborted day. Any allowed combination must remain coherent and supported as a whole; no free generation or AI service is introduced,
**And** treat the accepted gallery's ten samples as the starting bank subject to their factual predicates, not as unconditional text. A plan can establish a planned structure/assignment, but cannot establish that every part or the guiding work was performed,
**And** claims about actual duration, completed work or an ended assignment require corresponding evidence; abort alone cannot establish an exact shorter duration when timing is unknown. Choose a neutral alternative if the available evidence does not support the wording,
**And** never infer that driving was good/safe, all tasks succeeded, a break was taken, the user feels a particular way or has no work left elsewhere. No score, performance assessment or completion praise for uncertain work is produced,
**And** keep plan, observed and manual provenance intact. A manually confirmed fact is not promoted to independent GPS/source evidence to qualify a stronger claim,
**And** provide multiple preapproved, meaningfully different formulations also for neutral days, including days with no usable specific category. Uncertainty or source failure does not force an invented positive outcome, and variation cannot consist only of punctuation, dates or other substituted identifiers.

**Given** more than one eligible greeting and a permitted record of the preceding day's actually shown variant,
**When** selecting for a newly ended day,
**Then** avoid that previous variant and distribute selections across eligible alternatives over a series of similar days, using neutral alternatives when the specific category offers too few choices. Merely alternating the same two texts is insufficient when more suitable preapproved formulations are available; do not map every day of one type to the same sentence,
**And** use stable day identity rather than the date label alone, so two different working days with the same date cannot overwrite each other's choice. Reopening an older day must not make it the preceding day for a newer day's rotation,
**And** retain the selected variant for the same day across ordinary rerenders/reopening while it remains supported by the permitted current facts. A relevant evidence change that invalidates the wording requires a truthful replacement, without rewriting operational evidence,
**And** distinguish selecting a variant from actually showing it with valid access. A blocked or failed display is not recorded as shown; retries and concurrent tabs cannot manufacture repeated completed days or advance rotation as though a new day occurred,
**And** if earlier selection/display state is unavailable, expired or lost, use an eligible neutral/available choice without claiming a guaranteed non-repeat. Never retrieve deleted day data or create permanent history just to recover variation.

**Given** the closing screen is used before initial review was explicitly finished, after it was finished, or while its phase is unresolved,
**When** the owner navigates to summary, review or main menu,
**Then** preserve the 7.2 review phase: viewing the greeting or choosing main menu is not explicit review completion. Offer continuation through the existing permitted open-review flow rather than silently consuming it,
**And** only the existing confirmation showing remaining uncertain activities closes editing. Once completed, summary access is read/export-only; unresolved phase keeps editing restricted until resolved,
**And** Back, restart, a stale closing screen or repeated navigation cannot resume the ended day, start a prepared day, change another active day's role/trip/writer state or replay an export,
**And** main menu may expose the existing preparation path, but starting another day still requires its own confirmation and valid access. The closing screen supplies neither a new login period nor a new day grant,
**And** preserve existing movement and unknown-role restrictions on actions. An ended day or a positive greeting does not establish standstill or resolve physical role.

**Given** the client is offline or selection/rotation state cannot be saved or recovered,
**When** the closing flow renders,
**Then** use the verified local text bank and permitted retained day facts without requiring server/source access. A recoverable greeting-state failure must not undo terminal state or block summary/main-menu navigation,
**And** degrade to factual neutral text if the specific basis is unavailable. Preserve actual day/access/storage error status where relevant; never claim that a selection, review completion or server update was saved when it was not,
**And** reuse owner/day-scoped IndexedDB and existing authenticated FastAPI/PostgreSQL retained-result contracts for only the minimal choice/display metadata needed for stable recovery and variation; changes require existing authority/revision rules and cannot mutate immutable operational batches,
**And** treat reading a retained closing screen as reading, not as a writer takeover or a new closure event. If a client lacks permission to save presentation metadata, it cannot bypass that restriction merely to record a greeting,
**And** apply AD-10/12 logout, scope and original expiry to day-linked greeting metadata, derived facts, replies and caches. Do not hide private day/category associations in permanent account settings, logs, backups or a cross-day archive,
**And** stop private fact-based display on lock/expiry and prevent old tabs or delayed callbacks restoring it. Neither selection, reopening nor synchronization extends the earliest applicable deadline. Generic text does not retain expired private facts.

**Given** the same closing component is exercised with fictional/demo data,
**When** simulated days end or restart,
**Then** keep simulation visible and use a separate demo selection/display state. Demo choices never affect operative variation and never access private facts or credentials,
**And** fixture-based verification of the component is sufficient for this story; the complete public demo remains E8 integration work.

**Given** fictional/anonymized day fixtures and the existing browser/FastAPI/PostgreSQL contracts,
**When** the story is verified,
**Then** test normal end, abort, split parts, confirmed changes, planned-but-unperformed guiding, unknown outcomes/timing and manual confirmation against explicit expected eligible/ineligible variants; ensure unsupported samples fall back to neutral wording,
**And** run a controlled series of six otherwise equivalent working days with permitted retained selection state, and separately six neutral-only days. With at least three suitable preapproved formulations available in each case, require at least three meaningfully distinct greetings across the series, no adjacent repeat and no simple two-text alternation; inspect the actual wording as well as variant IDs. Dates, punctuation and variable identifiers alone do not count as variation,
**And** reopen/restart each same-day result during those series and verify the original choice is unchanged unless its factual basis becomes invalid. Inspect bounded storage, then expire earlier days and repeat selection without retrieving or retaining deleted shift history; no guaranteed non-repeat is claimed when prior state has legitimately disappeared,
**And** test two own days sharing a date, only one category-specific variant with neutral alternatives, no preceding-day record, rereading an older day, simultaneous tabs and a blocked display. Verify no false shown record, new-day event or permanent private rotation history,
**And** test offline restart, failed metadata save, incompatible/missing selection state, logout/expiry while open and delayed responses; preserve terminal status, truthful local/server status and fixed deadlines,
**And** test open/closed/unresolved initial review and navigation into a menu with another active day. No screen visit closes review or changes operational context,
**And** verify readable day/night presentation and keyboard focus, plus demo/operative separation. Record controlled evidence for E8-D; actual Lenovo/Brave readability and integrated closing/navigation behavior remain E8-P qualification.

**Traceability:** Closing portion of FR-22, preserved FR-21 terminal state, offline/recovery FR-17/20, bounded FR-1/24 and isolated demo boundary FR-25. NFR-1–4; UX-DR32/33/34/38/39/44. EXPERIENCE Latest navigation and closing decisions and Closing message; accepted gallery screens 26/37; DESIGN centered closing composition. The explicit 7.2 review-completion amendment governs navigation. AD-2 local assets/state, AD-3/4/5 existing fullstack persistence, AD-9 terminal/context semantics, AD-10/11 current authority, AD-12 short retention and AD-13/14 demo/build isolation. All AD-1–AD-14 remain unchanged.

**Dependencies:** 7.1 terminal result, 7.2 review phase, 7.3 factual summary basis and 7.5 retained/menu navigation, with existing E1/E5 access/assets/recovery and E3/E6 role guards. No future story is required for the closing component to function.

**Size boundary:** One closing screen, static eligible-text selection and minimal bounded choice/display persistence integrated with existing navigation. No AI service, performance analysis, new operational engine, new summary/PDF renderer, permanent history or independent synchronization mechanism. No new schema beyond metadata actually needed by this slice.

**Pilot qualification:** Controlled factual-selection/navigation/storage cases contribute to E8-D. E8-P still requires actual target-device behavior and integrated lifecycle evidence; E8-E remains field evaluation. Role uncertainty and the open 5.4/7.1 timing-evidence risks are not solved by a closing message. No implementation or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 with factual composition from multiple preapproved formulations, including neutral alternatives; test a series of equivalent working days for noticeable variation beyond avoiding yesterday's text. Same-day choice remains stable, no permanent shift history or unsupported work claims are introduced, and greeting/navigation changes neither initial-review phase nor closure receipt status. The controlled series criterion uses six similar days and at least three meaningfully distinct eligible texts, separately for neutral days. Planning approval only; the approved copy in epics.md is canonical.
