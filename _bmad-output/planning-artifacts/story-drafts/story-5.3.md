---
status: approved
created: 2026-09-26
epic: E5
story: '5.3'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.2', '5.1', '2.8', '3.2', '4.8']
---

## Epic 5: Continue a Prepared Day and Reconcile Recovery

This slice integrates same-client recovery of an already active own working day across closure/restart and network loss. It restores the committed E1–E4 state into the coherent build from 5.2, preserving bounded access and uncertainty. Starting a merely prepared day offline, generalized reconnect/conflict handling, writer transfer and release migrations remain separate E5 slices. E6/E7 extend the recovery contract for their own capabilities.

### Story 5.3: Resume the Already Active Working Day Offline Without Losing Choices

As the pilot owner,
I want to reopen my already active working day on the same tablet with its saved trips, corrections and notices,
So that an interruption does not require reimport or erase my decisions, and I can continue the available work through the rest of the loaded day without internet.

**Acceptance Criteria:**

**Given** an owned, already active day with locally committed state, applicable authority and a complete compatible build from 5.2,
**When** the browser reopens after closure or device restart with no usable server connection,
**Then** check local lock/pending revocation, owner/client/day identity, original authority/data deadlines and active lifecycle before rendering private information or starting operational effects,
**And** restore that day without PDF reupload, bus-number reentry or a required server round trip, including after ordinary fourteen-day expiry when 5.1's already-active continuation scope remains valid,
**And** reject a prepared/new, ended/aborted or expired day as an active-day resume target; cookie presence, scheduled departure or a guessed active flag cannot establish eligibility,
**And** history navigation and late callbacks cannot briefly expose locked/private content; unreliable lock/authority reads retain the AD-10 failure behavior rather than unlocking automatically,
**And** use ended/aborted fixtures to prove non-resumption without implementing E7 completion screens here.

**Given** a permitted recovery with retained E1–E4 state,
**When** the operational view is reconstructed,
**Then** read a consistent committed state and its outbox/revision references rather than combining a newer plan with unrelated older operational state,
**And** restore the combined-day identity and service dates, confirmed plan revision and activity order, physical bus and change-time provenance, actual trip and manual pin, exact stop occurrence, progress origin/uncertainty and recorded outcomes/corrections,
**And** preserve pending reviewed-plan changes as pending rather than auto-confirming them; restore the manual theme preference and existing source/notice version state without converting planned facts into observations,
**And** do not rerun initial automatic trip selection over an established actual trip or manually selected context,
**And** restore completed committed actions exactly once; actions interrupted before their local transaction committed remain uncompleted, with no orphan outbox event or invented successful save,
**And** publishing the restored view is not a new operational action and must not duplicate historical events, create a new batch identity or change the server revision.

**Given** a restored own day with multiple downloaded trips, intermediate activities and more than one work part,
**When** the owner continues while disconnected,
**Then** existing trip progression, permitted stop/trip corrections and actual transitions can use every available later trip's downloaded stop list and known activity facts, not just the trip active before closure,
**And** keep each work part's reporting time/depot and overnight service-date/calendar-date relationship, including Friday 25:30 displayed as Saturday 01:30 where appropriate,
**And** missing or never-downloaded stops/source data remain visibly missing with the approved manual fallback; a partial bundle never acquires whole-day-prepared status,
**And** retain actual manual selection until its approved release condition; current time alone cannot skip delayed work, select another trip or mark a break/bus change completed,
**And** commit each new permitted change and outbox event together locally before showing completion; quota/write failure preserves the last committed state and reports failure without pretending a correction was saved.

**Given** stored position/speed evidence and a period with no observations while the app was closed,
**When** sensing and movement controls resume,
**Then** retain the last known stop context as uncertain and show the observation gap; a stored fix or speed is not a new measurement or proof that the bus remained there,
**And** use 3.1's actual qualified signal states and 3.2's persisted history/timing: restart cannot manufacture the genuine first-start exception, reuse an obsolete zero speed as standstill, or reset/start a fresh five-minute outage period,
**And** a trustworthy already-elapsed qualifying outage may enable its explicitly labelled exception; incomplete or inconsistent history cannot infer that the exception has elapsed or that unrestricted controls are safe,
**And** direct previous/next controls require the qualified GPS-loss condition from 3.7, not network loss or unknown speed alone; each press still moves at most one known stop,
**And** resume qualified sensing through the existing engine; unambiguous later-stop recovery preserves the gap and never certifies the 100-metre target for unobserved passages or silently overwrites a conflicting manual correction,
**And** restore any ten-second display transition from its recorded final-arrival basis without inventing arrival/physical activity during the gap; same-route return still requires independent return-start evidence or the separate qualified-loss Next press.

**Given** previously received notices and saved driver interaction/audio state,
**When** the recovered day displays retained notices,
**Then** preserve exact source/version identity, source versus retrieval timestamps, relevance uncertainty, seen/registered/hidden state and confirmed-ending timing from E4,
**And** unchanged notices do not become new, unseen or newly audible merely through recovery; uncertain prior playback never causes old audio to replay,
**And** do not restore open detail before movement/access permission is established, or mark a version seen just because its state was loaded,
**And** derive time-limited presentation from the original recorded basis without resetting its timer or deleting summary evidence; passage of time alone is not source-confirmed resolution,
**And** display the prominent yellow-triangle connectivity/updates warning plus retained source freshness or unavailability, without implying fresh retrieval or all-clear conditions; later automatic reconnect orchestration remains a separate slice.

**Given** retained unsynchronized changes or an immutable batch whose server outcome is unknown,
**When** recovery opens the local working day,
**Then** preserve event/batch identities, payloads, writer epoch, expected revision, prior receipts and locally saved versus server-confirmed status under the existing AD-5/12 rules,
**And** no server response, elapsed time or successful local restore counts as acknowledgement; existing receipt handling may confirm only the matching batch,
**And** do not replace more recent local committed work with an older server snapshot or automatically submit pending events under another writer epoch,
**And** use existing same-origin writer coordination before operational side effects; another tab cannot run a second local progression/sound writer, and an observed lost writer authority cannot be bypassed by reopening,
**And** unseen remote takeover/revocation while disconnected is not claimed detectable; explicit cross-device transfer/conflict resolution remains subsequent E5 work,
**And** test a real FastAPI/PostgreSQL accepted baseline followed by offline local corrections and reopen, preserving the different local and server states without requiring a future reconciliation UI.

**Given** incomplete, inconsistent, corrupt or evicted private data, incompatible schema references or unreadable storage,
**When** reconstruction cannot establish a coherent authorized operational context,
**Then** show a bounded recovery failure/uncertainty state using only independently readable authorized facts, never fabricate an active trip, physical bus, completed action or unlocked role,
**And** preserve still-permitted recoverable work and offer non-destructive retry when interaction permits; do not clear private storage, fetch an older snapshot over unsynchronized changes or silently choose another day as repair,
**And** distinguish missing optional trip data with its existing fallback from broken identity/authority/critical operational state that prevents safe resumption,
**And** recheck original deadlines on startup, resume and while running; delete expired private copies before use as required by AD-12, never extend them for recovery or synchronization,
**And** state actual loss where data has been evicted; no claim of durable backup or recovery of unsaved work, and no additional raw GPS tracks/private diagnostic logs.

**Given** restoration is exercised in representative controlled scenarios,
**When** checking the result,
**Then** cover browser close/reopen, tablet restart as a target-device case, network-only loss, Access-blocked responses and simultaneous GPS loss separately,
**And** include a manually pinned delayed trip, repeated stop occurrence, an overnight later trip in a second work part, bus correction, changed/seen/hidden notice versions and an uncertain sound attempt,
**And** inject closure before/after local commit, an unresolved batch response, partial bundle, corrupt required state, logout/read failure, active-versus-prepared day-fourteen expiry and original data expiry,
**And** compare restored state with the committed pre-interruption facts and account explicitly for elapsed timers and new qualified observations; restoration itself supplies no observation evidence,
**And** require no mandatory dialogue or reentry while driving; expose uncertainty and unavailable controls using readable text/symbols and the existing movement policy.

**Traceability:** Same-client active-day FR-20 and E1–E4 whole-day continuity FR-17; bounded FR-1, retained evidence FR-6–16/19 and expiry FR-24. NFR-1–4; UX-DR3/7/14–24/38/44, with UX-DR31's recovery invariant extended by E6 rather than new mentor functionality here. AD-2 committed local authority, AD-3/9 single operational engine, AD-4/5 PostgreSQL and immutable synchronization state, AD-10 scope/locking, AD-11 writer identity, AD-12 fixed expiry, AD-13 gate failures and AD-14 coherent required build. FR-18 reconnect success/conflicts and full E6/E7 recovery are not claimed complete.

**Dependencies:** Implemented 5.1 authority, 5.2 coherent boot, 2.8 available day data and E1–E4 feature persistence/operational contracts, including 3.1 qualified sensing limits and 3.2 movement rules. Demonstrate the already active same-client path with an accepted baseline; no future offline-start reconciliation, takeover, migration, mentor or summary feature is a prerequisite.

**Size boundary:** Recovery coordinator and integration of existing own-day state into one consistent guarded view, plus continued existing offline operations through later activities. Reuse feature persistence and the operational engine. No new generic event-sourcing system, offline activation of a merely prepared day, generalized sync/conflict UI, Access lifetime preflight, writer transfer, migrations or E6/E7 implementation. Their V1 requirements remain assigned, not removed.

**Pilot qualification:** Controlled browser/fullstack recovery cases contribute to E8-D. E8-P must qualify actual Lenovo/Brave closure/tablet restart, surviving browser storage, real sensing freshness and access/offline behavior across the integrated day; fixtures do not prove these. E8-E remains later field evaluation. These tests are specified, not executed during planning.

**Approval:** Approved by the owner on 2026-09-26 with the stated scope: reopening restores the saved active day and driver choices while old measurements, missing data and pending synchronization retain their correct uncertainty. Planning approval only; the approved copy in epics.md is canonical.

**TIME-01 amendment (owner, 2026-09-27):** On offline restart, an unverified clock or elapsed interval requires a non-private lock before rendering any day metadata or allowing actions/export. Keep the local copy locked until trusted server time/status control, delete expired data before display, and never equate app lock with encryption or exact-time physical deletion. Recovery after E is permitted for an already server-approved active day with valid grant/data scope; a provisional local start needs a matching pre-E acceptance status before using that exception. Test lock-before-first-pixel, retained-unexpired recovery, expired-before-view deletion and lost receipt. Earlier unconditional offline-resume wording is subject to this amendment.
