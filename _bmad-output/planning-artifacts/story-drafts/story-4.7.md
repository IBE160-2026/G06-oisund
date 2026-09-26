---
status: approved
created: 2026-09-26
epic: E4
story: '4.7'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['4.6']
---

## Epic 4: Understand Relevant Notices and Their Sources

This slice adds two distinct optional, version-specific user actions: Registrert reduces driving-message prominence; manual removal after original-source checking hides an uncertain-disappearance entry from the day overview. Neither action changes source facts, proves understanding or substitutes for actual content display. Existing source, relevance, overview and driving contracts remain authoritative.

### Story 4.7: Register a Notice or Hide an Uncertain Overview Entry Without Changing Source Facts

As the driver,
I want to reduce a selected notice's prominence or explicitly remove an uncertain overview entry after checking the original source,
So that I can manage already considered information without erasing evidence or claiming that the source incident has ended.

**Acceptance Criteria:**

**Given** a prominent notice version in the driving view and permitted interaction,
**When** the driver selects its large Registrert button or completes its optional forgiving swipe-to-dismiss,
**Then** record registration for that exact incident/version in the combined working day and remove only its prominent driving message,
**And** restore ordinary stop emphasis where no other prominent notice needs that area, preserving unrelated messages and the accurate indication of additional notices from 4.6,
**And** retain the applicable stop-warning triangle and the notice in Skiftdetaljer; registration is not incident resolution, source confirmation, overview hiding or proof of comprehension,
**And** provide equally usable labelled button/keyboard access so swipe is never the only action; incomplete or cancelled swipes change nothing,
**And** registration is optional and never required to continue driving, progress stops or change an otherwise permitted context.

**Given** two or more eligible notices, including more than two important concurrent warnings,
**When** one version is registered,
**Then** affect only that selected version, not the entire incident family, all visible rows or all notices at a stop,
**And** keep other prominent/remaining notices and their additional-notice indication correct; registering one cannot silently discard an undisplayed eligible notice,
**And** the retained marker remains tied to supported source/occurrence relevance, including multiple affected visits; registration cannot invent or remove source applicability,
**And** if an unchanged registered version becomes relevant again later in the same day, preserve its registration rather than reintroducing its prominent message merely because the trip/context changed.

**Given** reliable movement, genuine startup, or qualified speed loss/recovery,
**When** either registration or manual overview hiding is opened, gestured or committed,
**Then** use 3.2's shared permission at invocation and commit, including distinct labelled unknown-speed startup and elapsed-five-minute exceptions,
**And** all reliable speed above zero locks these actions; unknown speed is not standstill and the direct GPS-loss stop-arrow exception does not authorize notice dismissal,
**And** movement/revocation before commit cancels the incomplete action and keeps the previous committed state; movement after a completed commit does not undo its evidence,
**And** immediately close restricted detail and leave focus in visible permitted UI, without resetting movement/outage history or requiring acknowledgement while moving.

**Given** a retained overview notice marked Status usikker – sjekk originalkilden because it disappeared without confirmed ending,
**When** the driver has checked the original source and explicitly chooses to remove that version from the overview,
**Then** require an explicit indication that the source was checked and record the chosen exact version, manual removal and applicable day/context,
**And** explain that this hides the overview entry without confirming resolution; cancellation leaves it visible and no free-text or sensitive reason is required,
**And** offering/following a source link or receiving an HTTP success cannot automatically prove the driver checked the source; preserve the manual origin of that indication,
**And** source-link use obeys movement policy; if the source has not actually been checked, retain the uncertain entry rather than silently hiding it on a failed link,
**And** the app may record the driver's explicit report of an external source check without requiring a new online round trip to certify it,
**And** distinguish this action from Registrert and the automatic ten-minute removal of a source-confirmed ended notice; it does not silently register a driving message or alter source lifecycle.

**Given** the selected version is registered or manually hidden,
**When** identical content is fetched again, relevance changes, or the compatible view/app restarts,
**Then** preserve the same day/version-specific registration and hidden state, including while offline,
**And** an unchanged manually hidden version stays out of the overview for the rest of that combined day; polling, a new retrieval timestamp, a later work part or context switch cannot bring it back,
**And** preserve prior source/display/interaction evidence and the original day expiry; neither action deletes history or starts a new retention period,
**And** seen, registered and hidden are independent facts: neither action marks detail seen unless that exact content was actually displayed with valid access under 4.5,
**And** normal confirmed source closure still removes active markers/warnings according to 4.3/4.6, regardless of local registration.

**Given** a genuinely changed source version arrives after the previous version was seen, registered or hidden,
**When** 4.3 accepts it and 4.4 evaluates relevance,
**Then** keep the earlier actions attached only to the earlier version; the changed version is unseen until its actual authorized detail display,
**And** an applicable changed version returns to the overview as updated with changed/bold treatment even when the earlier version was manually hidden,
**And** reassess its driving prominence under 4.6 rather than inheriting the old registration or forcing a warning outside its supported relevance/stage,
**And** this is an update, not a newly received incident: expose that distinction to the later audio story and emit no chime here,
**And** uncertain source ordering cannot be bypassed by inventing a new version solely to clear registration/hiding.

**Given** an action started for version A while version B, source closure, plan/context change or logout arrives,
**When** a button/gesture callback would commit,
**Then** validate current access, permitted interaction, day, target version and action applicability; never retarget A's action silently to B,
**And** if A remains a valid target, only A may receive the action; otherwise reject/cancel visibly without hiding/registering B or unrelated notices,
**And** a closed notice cannot be turned back into an active one by a stale callback, and the client closure timer is not reset by registration/manual hiding,
**And** duplicate taps, swipe/button overlap and immutable retry produce one effect and one necessary event, not contradictory or duplicated corrections.

**Given** a permitted registration or manual-hide action is committed,
**When** local persistence and later synchronization run,
**Then** atomically save the exact-version interaction state and outbox evidence before showing the action as completed,
**And** preserve the notice snapshot, original source status/uncertainty and prior display evidence needed by E7, distinguishing registration from manual overview removal and source-confirmed ending,
**And** a local write failure leaves the previously committed presentation/state authoritative, reports that the action was not saved and permits a safe retry,
**And** use inherited FastAPI/PostgreSQL owner/day/revision checks, immutable batches and valid matching receipts; network failure does not discard a local commit and only a matching receipt marks server confirmation,
**And** source polling cannot overwrite these client-owned facts; competing/stale synchronization preserves permitted local work for existing explicit conflict handling.

**Given** retained interaction state is unavailable, unreadable or expired,
**When** the view reopens or tries to restore notice presentation,
**Then** explain the storage/state uncertainty rather than silently resetting versions to new or claiming a registration/removal succeeded,
**And** do not infer a new source receipt, new-notice sound entitlement or fresh source content from the missing marker,
**And** honor private access/logout/expiry locks and existing recovery behavior, keeping full active-day offline boot/authority and cross-client recovery in E5,
**And** apply the existing AD-12 deadline to every private local/server/outbox copy; source-cache cleanup cannot erase the unexpired day's required version evidence.

**Given** notice actions are tested with touch, keyboard, text enlargement and assistive technology,
**When** controls render or an action changes prominence/visibility,
**Then** expose the selected notice/version context, action purpose, permitted/disabled state and visible reason without color or gesture alone,
**And** preserve a clear distinction between Registrert and removal from overview, with a cancel-preserving source-check/removal flow,
**And** move focus to an appropriate remaining visible control after removal; never leave focus in a disappeared row or hidden motion-closed detail,
**And** announce meaningful committed changes without poll repetition, automatic source opening or demands for driver interaction,
**And** actual mounted touch/glove usability remains target-device qualification; fixtures cannot establish safe real-world interaction.

**Traceability:** FR-14 uncertain-disappearance manual removal, version lifecycle and persistent interaction state; FR-16 movement policy; bounded FR-17/20 recovery and FR-22 manual correction evidence. NFR-1–4; UX-DR19/20/22/23/38/39/40/44 and EXPERIENCE notice acknowledgement/manual removal. AD-2/4/5 atomic client state, PostgreSQL receipts and evidence; AD-7/8 unchanged source facts/exact versions; AD-9 shared policy; AD-10/12 access/retention; AD-14 compatible recovery. FR-15 audio implementation remains separate.

**Dependencies:** Implemented 4.6 and inherited 4.3–4.5 source/version/relevance/list/evidence contracts plus E1/E3 permission/persistence. No later audio, summary UI, mentor workflow or complete E5 recovery is required to demonstrate these two version-scoped actions. Tests distinguish source-check self-report from automated verification without introducing a new verification service.

**Implementation evidence:** Button/swipe/cancel; selected notice among two and three-plus; preserved marker/overview after registration; unknown-speed exceptions versus real motion and motion mid-gesture; uncertain disappearance with source-check indication/cancel/unreachable source; seen independence; unchanged replay/context/restart versus changed-version return; A-action/B-update, closure/logout races, duplicate actions; failed local commit, lost/mismatched receipt, offline restore/storage failure and expiry. Verify actual PostgreSQL persistence and exact-version events with labelled fixtures. Tests are planned, not run.

**Size boundary:** Version-specific Registrert and manual uncertain-overview removal with their persistence, evidence and accessibility. No source editing, inferred incident resolution, new sound mechanism, movement policy changes, mentor exceptions, summary/PDF UI, bulk dismiss-all or permanent notice archive.

**Pilot qualification:** Repeatable action/persistence/failure evidence contributes to E8-D. E8-P requires actual mounted interaction, qualified source versions and integrated offline/access behavior; optional acknowledgement never becomes required driving work. E8-E remains subsequent field evaluation.

**Approval:** Approved by the owner on 2026-09-26 with the stated scope: Registrert and manual hiding affect only the selected version in the driver's day-specific interaction state; neither changes source facts or proves comprehension. Planning approval only; the approved copy in epics.md is canonical.
