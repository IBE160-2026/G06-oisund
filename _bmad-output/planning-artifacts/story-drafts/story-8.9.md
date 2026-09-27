---
status: approved
created: 2026-09-27
epic: E8
story: '8.9'
type: qualification
approved: true
approvedOn: 2026-09-27
dependencies: ['5.13', '6.10', '7.5', '8.3', '8.5', '8.8']
---

### Story 8.9: Qualify Whole-Day Offline Continuity, Authority Recovery and Final Settlement

As the pilot owner,
I want observed evidence that a prepared day survives disconnection, interruption, authority changes and closure without losing permitted work or reviving deleted data,
So that operational continuity and its limits are established before actual-shift reliance.

**Acceptance Criteria:**

**Given** the implemented E1–E7 flows, actual Lenovo/Brave client, intended private ingress and real FastAPI/PostgreSQL 18 backend,
**When** the bounded continuity qualification inventory is prepared,
**Then** identify build/schema/configuration, devices and browser profiles, access/writer scopes, independently specified fictional day facts and expected state/receipt/deadline outcomes,
**And** reuse existing E5/E6/E7 and 8.3 evidence, testing the integration seams with an own-day path and a mentor path that include later trips, split work, an overnight boundary, manual corrections and uncertain outcomes,
**And** distinguish actual network/device/storage/backend observations from labelled source/sensor inputs and accelerated boundary fixtures. Use no real private shift files or permanent raw tracks for this controlled qualification,
**And** define a representative full-day duration from the chosen case, record actual elapsed offline duration and interruptions, and exercise later activities through summary/PDF. A fast-forwarded fixture or short outage cannot be reported as demonstrated full-duration offline use,
**And** keep this a controlled pre-pilot exercise with no required moving-driver interaction or reliance on an unqualified app. Actual source and sensor support remains evidenced separately by 8.7/8.8.

**Given** a confirmed day with verified compatible app assets, documented per-trip data coverage and valid authority,
**When** mobile internet/tethering or the route to the backend becomes unavailable and the browser/tablet is closed and restarted,
**Then** verify the entire available day remains usable through later trips/activities, manual corrections, explicit end/abort, preserved first-review continuation, summary and local PDF without reimport or bus-number reentry,
**And** compare recovery with committed pre-interruption facts: selected day/plan revision, active trip and repeated-stop occurrence, manual pin/bus, notice version/seen/hidden/audio state, role/person/block and outage history. Missing or corrupt critical context causes visible bounded failure, not guessed restoration,
**And** keep restored measurements old, missing stop data missing, unseen updates unavailable and pending batches unconfirmed; network loss alone cannot activate position-loss controls or infer motion/standstill,
**And** distinguish complete versus partial day data and complete versus missing app assets. Missing/evicted required storage cannot be repaired by silently clearing private work, mixing builds, choosing an older snapshot or inventing recoverable data,
**And** exercise a local write/read/quota failure and interruption before/after commit. Only an atomic saved state/event may appear locally completed; an unfinished action cannot be reported as saved or server-confirmed.

**Given** independent ordinary app access, a concrete-day grant and the actual verified Access expiry,
**When** access boundaries, offline start, renewal, logout and recovery are tested,
**Then** distinguish an already active day continuing after the fixed app_authenticated_at plus 14 days from a prepared/new day that cannot start after that expiry. Day scope never exposes another day's metadata or creates another ordinary-access period,
**And** test 5.4 activation just before/at/after expiry and later server submission. First durable server acceptance must occur strictly before E; at/after E reject first acceptance regardless of client time, event order, test clock or local active flag,
**And** if TIME-01 acceptance is unimplemented or unverified, keep local activation and server status distinct and report the affected requirement blocked. Do not manufacture a passed path or change V1 through qualification wording,
**And** exercise actual Access renewal/blocking behavior separately from labelled short-expiry fixtures. Verified token expiry determines coverage; renewal does not change app authority, writer epoch or data deadline, and HTML/redirect responses are neither cached app assets nor receipts,
**And** logout immediately locks private content even without a server reply. Pending revocation goes before other private traffic; gate renewal occurs while locked, and retained work requires a fresh same-owner app login after pending logout is settled,
**And** unreadable/unreliable lock storage, restart, history navigation, other tabs and delayed callbacks cannot automatically reopen private content or silently discard pending revocation. A disconnected client cannot claim instant knowledge of remote revocation.

**Given** locally committed work and source/transport/receipt outcomes that may differ,
**When** connectivity returns through actual client/backend/database paths,
**Then** verify network recovery, validated source refresh and confirmed server saving remain separate statuses; partial/failed source results preserve prior information and corrections,
**And** exercise lost/mismatched receipts, identical immutable retries, changed content under a reused identity, database failure and a revision conflict. Only a matching durably recorded receipt confirms the sent batch; actual PostgreSQL effects, deduplication and revision must match without partial writes,
**And** distinguish rejected changes, unresolved outcomes and revision conflicts, preserving still-permitted local work for explicit review against a valid server basis. An unexplained revision cannot be silently rebased or merged by arrival order,
**And** test permission/context changes during review and at commit. Manual trip/stop/role corrections retain provenance and cannot rewrite prior observations as source or GPS evidence; pending logout and expiry still take precedence.

**Given** two same-owner clients and permitted planned or emergency transfer,
**When** authority is moved and the former client later returns,
**Then** for planned transfer verify destination access and required app files before retiring the old writer; verify destination state against the post-transfer server revision before control. Failed verification requires explicit recovery, not automatic writer return,
**And** for emergency takeover expose last known server state and possible missing work. Keep the old client offline during transfer, make a further local change, then reconnect: old-epoch mutations are rejected, but permitted unsynchronized work remains for explicit review; the app must not claim the disconnected device already stopped,
**And** verify evidence intake is not application of corrections or operational acknowledgement. Chosen corrections use current authority and new events, with repeated/partial intake preserving original provenance, receipt state and deadlines,
**And** unknown actual mentor role on emergency recovery retains driver restrictions even if the server says guiding. No recorded Jeg kjører event is not proof of accompaniment; resolution is explicit and permitted,
**And** test lost transfer responses, concurrent tabs/replacement attempts and failed local recovery without two accepted backend writers or automatic takeover from timeout. A replacement's software authority does not qualify its hardware; actual operational replacement support needs its own applicable device evidence.

**Given** offline normal ending or abortion with pending original batches and linked-person data,
**When** the explicit end/review flow and later settlement execute,
**Then** preserve local terminal status and allowed facts/corrections in the minimal trimmed checkpoint, remove prohibited linked portions, and prevent another tab, old local copy or delayed response from restoring deleted content across restart,
**And** keep original batch outcomes unresolved until authorized payload-free lookup or transaction outcome establishes them. Retired identity is not acknowledgement; a matching old-batch or evidence-transport receipt cannot confirm the new closure settlement,
**And** exercise original-before-closure and closure-before-original transactions in PostgreSQL, failure/response loss and retry. Preserve accepted receipts, fence unaccepted retired IDs, reject resurrection under fresh IDs and confirm closure only with its own matching receipt,
**And** first review closes only by explicit confirmation after showing remaining uncertain activities. Navigation/crash does not consume continuation; later retained entry is read/export only, and neither path resumes the day or extends a deadline,
**And** test 7.1 locally reported ending time separately from verifiable timing evidence. An uncertain timestamp or later receipt cannot extend retention/access; enforce the earliest applicable binding limit pending evidenced resolution and apply adopted TIME-01 while reporting implementation and evidence gaps.

**Given** allowed private data exists in local/server revisions, checkpoints, outboxes, conflicts, receipts, grants and summaries,
**When** an applicable deadline is reached while active, closed, disconnected or suspended,
**Then** verify AD-12's non-sliding draft deadline and one combined-day data clock, with the separate AD-10 post-end authority cap and all earlier applicable limits. Viewing, export, confirmed additions, retry, server acknowledgement and recovery cannot reset an existing fixed deadline,
**And** exercise local startup/resume/while-open guards and server denial before periodic purge, deletion of all affected copies, expired receipt lookup and late uploads. A closed browser purges before use on return; newly learned earlier ending provides no grace period,
**And** expiration of a never-ended day never declares its activities completed. Pending settlement cannot delay expiry, and permitted review/export still requires current access,
**And** document accepted loss after eviction/device/volume failure without introducing historical backups, archived private WAL or a hidden recovery archive. Logical deletion is not forensic erasure; user-held PDFs remain outside app cleanup,
**And** accelerated expiry tests prove only the declared boundary logic; document their time basis and separately identify actual device observations. They do not prove TIME-01 on the actual device or elapsed full-day endurance.

**Given** the bounded scenarios finish with successful, failed or incomplete outcomes,
**When** the continuity report is compiled,
**Then** record passed, failed, blocked and not-run cases with actual duration, environment, fault origin, expected/observed state, receipt/database evidence and limitations, keeping observed versus synthetic evidence distinct,
**And** map gaps to owning stories and explicit decisions, especially TIME-01 implementation/actual-device proof and unknown-role recovery. A completed report does not qualify a failed capability or authorize actual shifts,
**And** retain sanitized evidence without private payloads, credentials or raw tracks, with no extra operational database/archive to support testing,
**And** state the tested build and compatibility assumptions. Host restart/resource/noise and actual release/migration qualification remain separate required evidence, not implicitly passed by same-version continuity,
**And** keep E8-D, E8-P and E8-E separate; no requirement or architecture choice is waived to obtain a positive result.

**Traceability:** E8-P durability/recovery and integrated access/expiry gates; FR-1/17–24, preserved FR-2–16 provenance and outcomes; NFR-1–4. UX-DR3/7/8/14–23/26–36/42–44 as exercised through the existing flows. AD-2/4/5 local atomicity and real PostgreSQL receipts, AD-8/9 notice/context integrity, AD-10/11 bounded authority/transfer, AD-12 closure/expiry/accepted loss, AD-13 Access separation and AD-14 coherent existing build. All AD-1–AD-14 remain unchanged.

**Dependencies:** Implemented E5 through 5.13, E6 through 6.10 and E7 end/review/summary/PDF/retained entry through 7.5, actual 8.3 fullstack harness, applicable 8.5 ingress/Access and 8.8 target-device evidence. Uses the current deployed test release and labelled nonprivate scenarios. No later E8 host/release report or actual pilot shift is needed to execute these checks; incomplete prerequisites are reported as blocked rather than assumed.

**Size boundary:** One bounded continuity qualification report using existing feature/fault harnesses, one full-duration prepared-day observation and selected two-client/closure boundary branches. No new synchronizer, transfer protocol, timing-proof design, all-feature regression rewrite or three-workday trial. Repairs remain with owning stories. Host recovery/resource/noise and old/new release compatibility are deliberately a separate upcoming story; no requirements are removed. Missing cases stay incomplete if observation needs another session.

**Qualification boundary:** Planning only. No actual endurance/access/database tests, destructive storage experiments, implementation, provisioning, deployment or readiness/final-validation workflow are executed now. E8-D/P/E outcomes remain pending.

**Approval:** Approved by the owner on 2026-09-27 as scoped: the actual full-day Lenovo/Brave test must document duration and observed outcomes; fast-forwarded cases cover separate failure paths. TIME-01 now supplies the policy; implementation and actual-device qualification remain unexecuted. Planning approval only; the approved copy in epics.md is canonical.

**TIME-01 E8-P qualification (owner, 2026-09-27):** On actual Lenovo/Brave, test fresh/stale/missing Tg, warning before and during unresolved offline start, strict durable server acceptance before E, rejection at E/after E regardless of client timestamp, pre-E acceptance with lost response and later status lookup, and approved-day continuation/post-end review after E within grant/D. Test offline end D from Tg with earlier limit and zero/short remaining review window; local end/closure receipt states remain distinct. Restart offline with unverifiable time and prove the lock precedes every private pixel/action/export; after trusted server control recover unexpired data or delete expired copies before view. Inspect OS PIN/storage protection and disabled uncontrolled backups/sync. Rehearse named custody, reconnect by 24 hours after planned end or supervised hand-in, controlled wipe if no trusted check by 24 hours after D with unsynced-work loss, and never-return scenario with server revocation, incident and pilot stop. Record actual observations, settings, timestamps and negative/not-run outcomes. This decision is not a test pass and overrides former open-policy wording.
