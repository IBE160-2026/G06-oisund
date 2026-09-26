---
status: approved
created: 2026-09-26
epic: E4
story: '4.8'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['4.7']
---

## Epic 4: Understand Relevant Notices and Their Sources

This slice adds the adopted discreet new-notice chime with persisted receipt/attempt identity, honest unsupported-audio behavior and actual Lenovo/Brave qualification. It does not change relevance, source versions, seen/registered/hidden state, visual-warning timing or movement permissions.

### Story 4.8: Sound One Discreet Chime Only for a Newly Received Relevant Notice During the Ongoing Trip

As the driver,
I want a short discreet chime for a genuinely new notice received during and relevant to my ongoing trip,
So that new information can draw brief attention without repeated sounds for updates, replay or later changes of context.

**Acceptance Criteria:**

**Given** an authorized ongoing actual trip and a newly accepted source incident in the combined day's receipt history,
**When** receipt is committed and 4.4 assesses the incident as relevant to that ongoing trip,
**Then** make one short discreet chime eligible, using stable incident/receipt and actual-trip context rather than merely a newly rendered heading or unseen flag,
**And** qualification of relevance and source identity is required; uncertain identity/relevance remains visually explicit but cannot be guessed into a definite audible trigger,
**And** use actual receipt and relevance during the ongoing trip, not source publication time, timetable activation or receipt of a backend synchronization acknowledgement,
**And** preserve the distinction between source/publication/update time, app receipt, relevance assessment and playback attempt; delayed source delivery is not a claim of immediate publication-to-sound delivery,
**And** this policy applies to eligible new notices, not only acute ones: a newly received relevant planned notice may chime before its later staged prominent display, which must not chime again.

**Given** an updated version, unchanged poll, source closure, supported reopening of a known incident or an already received notice becoming relevant later,
**When** the view, source state or actual/preview trip changes,
**Then** remain silent; new bold emphasis, new material version or restored visibility after manual hiding is not a newly received incident,
**And** preparation-to-driving transition, final-stop next-trip preview, same-route return activation, plan revisions, manual trip correction and approaching a warned stop cannot reclassify an old receipt as new,
**And** fetching/receiving a notice before an ongoing trip or while it is irrelevant does not queue a chime for when it later becomes relevant,
**And** distinguish a genuinely first-received incident during reconnect from replay of a previously received one; only the former can qualify if current trip/relevance requirements still hold,
**And** inability to recover trustworthy receipt history is uncertainty, not permission to sound cached notices as new.

**Given** a qualifying receipt, duplicate callbacks or repeated render/poll events,
**When** the audio side effect is scheduled,
**Then** durably identify and claim the single attempt for that day/incident receipt before invoking playback, using existing atomic local state/event conventions,
**And** a repeated receipt, callback, reopen or retry cannot invoke the same chime again; multiple views/tabs must not each play it for the same controlling-day event,
**And** test crash points before and after the durable claim and before/after the playback request: do not promise atomic exactly-once audible output across a browser/device crash,
**And** if a crash leaves the outcome indeterminate, retain that uncertainty and do not replay an old sound on recovery; visual notice availability remains independent,
**And** a failed/unreliable local claim or lost receipt history cannot produce a falsely deduplicated success; report the audio/state limitation rather than guessing it is safe to replay.

**Given** more than one distinct new relevant incident arrives together,
**When** eligible playback attempts are handled,
**Then** avoid overlapping chimes and repeated alarm loops, preserving a distinct bounded attempt identity for each qualifying receipt,
**And** recheck actual context, current applicability and access immediately before each attempt; cancel stale pending attempts if the trip ends/changes, source closure makes them inapplicable or private access locks,
**And** do not replay queued sounds as a catch-up burst after suspension, browser activation, reopening or a later trip,
**And** keep all notices and the 4.6 additional-notices indication visible as applicable; audio scheduling does not silently remove a notice,
**And** qualify observed multi-notice sound behavior for distraction and document any inability to meet the short/discreet requirement before pilot acceptance.

**Given** browser audio is unsupported, blocked, suspended, denied or fails,
**When** an eligible playback is attempted or capability changes,
**Then** retain the visual notice and show a concise honest audio-unavailable/not-confirmed status without opening a modal or asking for driver action while moving,
**And** distinguish eligible, attempted, browser-reported playback success/failure and indeterminate outcomes; a resolved API call does not prove the driver heard or understood the sound,
**And** any browser-required activation/setup occurs through a deliberate permitted interaction before operational reliance, following the existing movement/access rules and actual platform requirements,
**And** later audio activation/recovery prepares future eligible notices only; it does not replay an earlier blocked or missed chime,
**And** do not add hidden media loops, native/background guarantees, OS-volume overrides or a new notification service; failed support is a qualification gap, not a passed requirement because visual fallback works.

**Given** a chime is attempted, succeeds or fails,
**When** the application applies its result,
**Then** leave detail collapsed, keyboard focus and active trip/progression unchanged, and preserve all movement locks including source/detail/acknowledgement restrictions,
**And** no sound action marks the notice seen, registered, hidden, source-confirmed or understood,
**And** sound eligibility is independent of the stop-approach visual trigger; a heard chime does not prove that the notice heading was rendered,
**And** a late playback callback after context change cannot trigger another sound, reopen private content or write success into the wrong day/version; cancel remaining playback where supported without pretending already emitted sound can be undone,
**And** unavailable audio cannot block stop progression, manual fallback or later permitted notice review.

**Given** receipt, attempt and outcome evidence is retained or synchronized,
**When** local state is reopened or the backend acknowledges its immutable batch,
**Then** persist only the minimum linked incident/version/receipt, context, attempt identity and observed outcome needed for duplicate prevention and honest day evidence,
**And** reuse authenticated FastAPI/PostgreSQL owner/day/revision validation, atomic outbox handling and matching receipts; only a matching receipt marks server confirmation,
**And** server/network failure does not reset a local attempt or become a replay trigger; backend ingestion remains source state and cannot mark audio played on the tablet,
**And** record browser outcome separately from actual audibility established by controlled qualification; do not store a per-frame audio log or infer comprehension,
**And** private records follow the existing AD-12 expiry, logout locks and source-cache separation without a permanent notice/sound archive; retries/reopen never extend authority or retention.

**Given** the actual mounted Lenovo tablet and Brave browser,
**When** the implemented audio behavior is qualified,
**Then** record device/OS/browser versions, permissions, required interaction/activation, relevant audio-output/volume settings and tested foreground/power conditions,
**And** test an eligible new notice, silent updates/old-notice transitions, denied/blocked playback, multiple eligible receipts, network loss/recovery, tab/app foreground return and restart,
**And** distinguish browser-reported playback from independently observed audible output, including short duration/discreet character under stated representative conditions,
**And** perform controlled observations without requiring driver interaction while moving; no operating-system mute or unusable audio path is silently treated as audible success,
**And** report exact cases passed, failed or untested, including missed/duplicate/unnecessary chimes and recovery limitations; unsupported capability returns a solution decision and cannot pass E8-P through desktop simulation,
**And** no background sound delivery or reliable background execution is claimed by a foreground test.

**Given** visual status and capability/setup feedback,
**When** inspected with keyboard, touch or assistive technology,
**Then** retain a complete visual route to the same notice information; audio is never the sole representation of a warning,
**And** label unavailable/uncertain status without color alone, avoid repeated status announcements on unchanged polls and preserve focus,
**And** any controlled audio test used for qualification is clearly a test, not a source incident or fabricated operational notice receipt,
**And** use sanitized qualification evidence with no private shift identifiers or raw GPS traces.

**Traceability:** FR-15 chime eligibility/silence; FR-12 ongoing-trip relevance; FR-14 persistent receipt/version history; FR-16 no interaction bypass; bounded FR-17/20 restart and FR-22 provenance. NFR-1–4 and SM-C1 unnecessary-chime/distraction evidence; UX-DR19/23/25/38/40/44 and EXPERIENCE sound rules. AD-2/5 durable identity/outbox, AD-7 qualified relevance, AD-8 source newness versus updates, AD-9 actual context, AD-10/12 access/expiry and AD-14 compatible recovery. Source and device evidence remain separate.

**Dependencies:** Implemented 4.7 and inherited 4.3–4.6 stable identity/relevance/receipt/display state, E1 persistence and E3 actual-context/movement foundations. Actual Lenovo/Brave access is required for audio qualification; position/speed or wake qualification does not establish sound support. Verify current browser API requirements when implementing; no future E5/E7 screen is required to demonstrate this bounded chime policy and persisted attempt behavior.

**Implementation evidence:** Eligibility/silence reference matrix, preparation/current/next-trip transitions, new-versus-replayed reconnect data, planned chime versus later visual approach, exact-version updates/hidden return; duplicate callbacks/views, storage failure and crash boundaries, stale queue/context/logout, blocked playback then activation without catch-up, outcome/receipt faults and expiry. Real PostgreSQL tests cover synchronized records; actual device tests separately establish audibility and limitations. Tests are planned, not run.

**Size boundary:** One short browser chime, its new-receipt eligibility/deduplication, minimal outcome status and real-device qualification. No speech, recurring alarms, sound library/settings suite, native/background notifications, volume override, source substitutions, new operational engine or general offline recovery.

**Pilot qualification:** Repeatable labelled receipt/context fixtures contribute to E8-D but do not prove audible tablet behavior. E8-P requires actual Lenovo/Brave audio evidence and integrated source/receipt/recovery behavior, with failures honestly reported. E8-E remains subsequent real-shift evaluation including unnecessary-chime/distraction observations.

**Approval:** Approved by the owner on 2026-09-26 with sound tied to a newly received relevant notice during the actual ongoing trip. Updates/later context changes remain silent, and uncertain playback outcomes do not replay old audio. Planning approval only; the approved copy in epics.md is canonical. E4 epic-level confirmation remains a separate checkpoint.
