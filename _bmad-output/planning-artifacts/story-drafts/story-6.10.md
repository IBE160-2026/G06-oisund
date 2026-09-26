---
status: approved
created: 2026-09-26
epic: E6
story: '6.10'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['6.9', '5.3', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13']
---

### Story 6.10: Recover the Complete Actual Mentor Context Across Restart and Authorized Device Transfer

As the pilot owner using FADDER or INSTRUKTØR workflows,
I want restart and authorized device recovery to restore my actual role, person, period and precise plan/trip basis together,
So that I can continue the same day without reopening unsafe controls, following the wrong plan revision or losing the distinction between my work and accompanied observations.

**Acceptance Criteria:**

**Given** an accessible retained mentor day and the existing E5 recovery flows,
**When** the recovery coordinator loads E6 state,
**Then** validate and restore one coherent committed view of assignment and actual role, own activity/plan, selected person/imported plan, planned block and actual period, active tracking context/trip/manual pin, takeover/return evidence and restrictive role-recovery status,
**And** include the exact active plan revision and necessary retained facts, latest confirmed plan revision, unresolved-link reasons/review basis and pending revision/repair status as distinct fields; a newer plan is not automatically the active trip's basis,
**And** restore associated observations/gaps, movement/outage history, source/data coverage, notice version/interaction/audio state, local/server receipt state and current writer authority through the shared engines rather than rebuilding them from schedule or position,
**And** restore only a compatible owner/day-scoped set. Missing, inconsistent or unsupported relationships show a restricted unresolved state without assembling a new person/role/plan combination from unrelated snapshots,
**And** preserve the mentor-as-reviewer meaning of person-plan confirmation and keep planned links, actual accompaniment and source/GPS verification separate.

**Given** the same browser reopens an already active day online or offline,
**When** current bounded access and required app/data checks permit recovery,
**Then** resume the committed actual E6 context through 5.3, including guiding, classroom/office, planned own driving or acute FADDER takeover, without requiring reimport or activating another prepared day,
**And** an active context bound to revision R1 remains on R1 when R2 is confirmed and its link is unresolved; if R1's necessary data is missing, show the missing basis rather than silently substituting R2, guessing stop identities or fabricating progress,
**And** a temporary driver takeover remains FØRER until a valid explicit return is established. Apply 6.7/6.8's restrictive recovery when writes or outcomes are uncertain, including failure before any restrictive marker committed; an older guiding copy cannot resolve that uncertainty,
**And** retain A–B–A as separate historical actual periods, current own activity and each context's pin/evidence. Reopening the current period differs from entering a new one: recovery keeps its valid pin, whereas a later explicit new period establishes trip/stop context afresh,
**And** measurements remain historical and any observation interruption stays a gap. Restore qualified sensing history without a new first-start or five-minute allowance; no recovery certifies unobserved passages or the 100-metre target,
**And** preserve no-accompaniment instructor days without inventing a linked person, passenger progression or completed classroom/office work.

**Given** the owner initiates planned device handover under 5.8,
**When** the existing transfer protocol freezes/drains the source and validates the recipient,
**Then** include all required E6 role/context/revision/link/evidence state in the synchronized recovery basis, and check that the recipient's authorized app build can interpret these fields and has the needed verified app files before retiring source authority,
**And** after the existing atomic writer/grant transfer, verify the recipient's complete recovery set against the returned post-transfer server revision before allowing control; a previously downloaded mentor snapshot is insufficient,
**And** preserve original grant/data deadlines and exact active-plan revision, pin and pending link repair. Do not silently choose the latest imported revision, discard role uncertainty or recreate a period during transfer,
**And** if required data/state verification fails after transfer, keep the recipient non-controlling/restricted for explicit recovery; source writer rights do not automatically return,
**And** distinguish a transferred historical role state from current physical role where the recovery interval leaves it uncertain. Do not infer permission to guide merely from the imported assignment or an unverified copy.

**Given** the former device is unavailable, disconnected or unable to drain and the owner uses explicit emergency device takeover under 5.9,
**When** the recipient reviews and accepts the last server-held recovery basis,
**Then** show the server timestamp/revision and possible missing E6 changes, specifically including an unreceived Jeg kjører, person/context transition, takeover/return or plan/link revision,
**And** use the existing destination prerequisites and atomic writer/grant transfer, followed by verified recovery; neither the FADDER driver-takeover action nor a role label is a substitute for this device-authority protocol,
**And** when emergency takeover lacks up-to-date state from the former device, actual role is unknown even if the server copy says guiding and contains no Jeg kjører event. Absence of that event proves neither that the mentor is still accompanying nor that no driver change occurred,
**And** show unknown actual role separately from the enforced driver restrictions, and retain those restrictions until the role is explicitly clarified through a permitted action against the valid retained basis. Do not label the physical role confirmed merely because the safer permission policy is applied,
**And** do not invent the missing transition, actual time, current person or stop. Preserve last-known facts and gap/unknown statuses; current role clarification is manual evidence, not reconstruction of the old device's observations,
**And** the disconnected old device cannot know immediately that authority moved. The backend rejects later new mutations under its old writer epoch, while its permitted local unsynchronized work remains for explicit review; do not claim the old device has already stopped.

**Given** old-device E6 work returns or recovery reveals a revision conflict or unknown receipt outcome,
**When** it is received and reviewed through 5.10/5.7,
**Then** retain original client/epoch/event identities, person/plan/revision/block/context, actual-role origins, known occurrence versus registration times, receipt state and original expiry. Intake for review does not apply operational changes,
**And** compare against the verified current basis without merging periods by person/route/time, transferring pins across periods or letting arrival order select the current actual role,
**And** preserve legitimate prior acceptance via authorized receipt lookup. Any chosen new correction uses current authority and exact reviewed context, and does not replay an old batch or silently restore an earlier guiding role,
**And** manual recovery cannot become GPS/source evidence, certify unobserved work or retroactively move observations to another person/revision by guessing; unresolved differences stay explicit,
**And** keep 6.9 affected-link review separate from accepting a recovered file/plan. Restoring R2 or repairing its link cannot silently rebind an active R1 context,
**And** old-device disposition never returns writer rights automatically, extends deadlines or restores content removed by terminal closure.

**Given** recovery, an app-version transition or a delayed response races with current operations,
**When** state would be rendered, mutated or confirmed,
**Then** enforce existing access/logout/expiry and 6.4 commit-time role/context guards before the effect; pending revocation is handled before other private traffic, and recovery cannot unlock private data or guiding from a stale view,
**And** validate E6 recovery fields through the existing 5.11 retained-client/backend and 5.12 local migration contracts for their actual data lifetime. Missing role/revision fields cannot default to guiding or latest-plan substitution; active-day build pinning remains unchanged,
**And** a late receipt only updates the original operation's acceptance; old state responses, suspended tabs or callbacks cannot switch role/person/active revision or mark a current version seen without its content being shown,
**And** preserve notice identity, legitimate seen/registered state and audio-attempt uncertainty across devices. Missing old-device sound evidence never causes playback of an old notice; recovering a context is not a new notice receipt,
**And** reuse owner/day-scoped IndexedDB and authenticated FastAPI/PostgreSQL recovery contracts and transactional validation, adding only required E6 fields/integrity checks rather than a second synchronizer or authority model.

**Given** a recovered day has ended, been aborted or reached its applicable expiry,
**When** recovery or old-device work intake attempts to restore it,
**Then** apply the existing terminal/retention rules before use: an ended day never resumes, expired data is deleted before display/send, and received terminal/deletion state prevents stale-copy resurrection,
**And** within the permitted completion-review/settlement window retain only minimal allowed own facts, actual accompanied portions and temporary driver segments with their origins/gaps, separated for E7; discard the unaccompanied imported remainder from all local/server/recovery/conflict/pending copies using 5.13,
**And** preserve active/historical revision facts only as needed within the existing deadline, never as a permanent archive or a new seven-day clock from recovery/device transfer,
**And** no synthetic reconstruction replaces irretrievably lost data. Report missing work honestly under AD-12's accepted loss risk, without storing private backups, raw originals or a permanent GPS track,
**And** private E6 context remains isolated from other accounts and public fictional demo access; no recovery payload, credential or personal operational data enters logs or assessment artifacts.

**Given** two isolated same-owner browser clients, compatible and retained builds, controlled inputs and real PostgreSQL,
**When** this E6 recovery integration is verified,
**Then** test same-client offline restart and planned transfer in guiding, classroom/office, pending own-trip selection and acute FADDER takeover/return states, including A–B–A history, manual pin, qualified GPS outage and missing data,
**And** test active R1 plus confirmed R2 with unresolved link before/after repair, missing R1 facts and delayed R2 replies: no recovery path may swap the active basis or label the link resolved without review,
**And** test emergency transfer with an old-device unsynchronized Jeg kjører but server snapshot still guiding, failed role/guard writes, uncertain return, changed person and plan revisions: missing evidence stays explicit and permissions restrictive pending permitted resolution,
**And** test emergency takeover with no current old-device state and no Jeg kjører event in any available record, while the server says guiding: actual role remains explicitly unknown, driver restrictions remain active, and absence of an event cannot unlock guiding. Verify that only a current explicit permitted role clarification resolves it, including after recipient restart,
**And** test recipient missing/incompatible app files before transfer, verification failure after transfer, lost transfer/ordinary receipts, conflicting devices, suspended old tabs and returning old work without authority restoration,
**And** test E6 fields through a real retained-client contract and one local migration interruption using the existing E5 harness, including pending logout and role uncertainty, without changing the adopted update policy,
**And** test bounded conflict intake, unknown old notice audio, earlier own-day closure/expiry, no replay/resurrection and preserved permitted evidence partitions. Record demonstrated versus missing recovery evidence rather than claiming recovery of absent data,
**And** these are integration acceptance criteria for implemented E6 data paths, not implementation-readiness validation or evidence that pilot/device qualification has already passed.

**Traceability:** FR-17/18/20 extended to UX UJ-3/4, shared FR-1/6/9/16 and FR-22/24 evidence/retention. NFR-1–4; UX-DR8/14/16/19/22/23/26–31/36/38/39/44. EXPERIENCE Role and context recovery, revision ownership, acute takeover and accompanied-only evidence. AD-2/4/5 recovery/receipts, AD-8 notice state, AD-9 coherent actual role/context, AD-10/11 bounded authority and transfer, AD-12 expiry/accepted loss, AD-13 access failures and AD-14 compatible retained contracts/builds. All AD-1–AD-14 remain unchanged.

**Dependencies:** Implemented E6 state/evidence through 6.9 and E5 same-client recovery, explicit conflicts, planned/emergency transfer, old-device intake, compatible releases and terminal settlement through 5.13. Uses existing E5 flows with E6 payload/validation extensions. No E7 end/review/PDF UI is needed for recovery/terminal command fixtures.

**Size boundary:** Integrate the existing E6 state set with established E5 recovery/transfer/contracts and verify its identity/role/revision invariants end to end. No new transfer protocol, synchronization engine, event-sourcing framework, backup, cross-account sharing, automatic role inference or summary renderer. Earlier stories retain their feature-level recovery ownership; this slice closes the cross-feature/device integration seam.

**Pilot qualification:** Controlled recovery/transfer/browser/FastAPI/PostgreSQL evidence contributes to E8-D. E8-P requires actual Lenovo/Brave behavior, qualified replacement setup, access/file readiness and integrated role/revision/closure tests before real shifts. E8-E remains field evaluation. Data loss remains possible under AD-12; planning approval does not establish device support or solve 5.4's timing risk.

**Approval:** Approved by the owner on 2026-09-26 with unknown actual role after emergency takeover lacking up-to-date former-device state, even if the server says guiding. Driver restrictions remain until explicit permitted role clarification; absence of a Jeg kjører event does not prove continued accompaniment. Planning approval only; the approved copy in epics.md is canonical.
