---
status: approved
created: 2026-09-26
epic: E6
story: '6.1'
type: implementation
approved: true
approvedOn: 2026-09-26
dependencies: ['5.13', '2.7', '2.12', '3.2']
---

## Epic 6: Guide and Teach with Explicit Person and Driver Context

E6 extends the approved own-day workflows with private FADDER/INSTRUKTØR assignments, separately confirmed linked-person plans, accompaniment scope, own driving and explicit takeover/return. It reuses E2–E5 import, revision, operational, notice and recovery contracts. UX UJ-3/4 extend FR-2–11/16/20 and evidence/retention FR-22/24, with NFR-1–4 and AD-6/9/12 binding. UX-DR26–31/36 are primary E6 obligations; no new PRD FR number is invented.

This first slice adds the planned assignment and activity distinctions to the owner's own-plan review/confirmation. Linked-person import, actual accompaniment selection/progression and operational role transitions follow separately. A useful confirmed own plan is independently reviewable here, including an instructor day with no accompaniment.

### Story 6.1: Review My Own Mentor Assignment Before Linking Another Person's Plan

As the pilot owner preparing FADDER or INSTRUKTØR work,
I want to review my own assignment, own driving and other permitted activities in my own confirmed day,
So that another person's trips cannot silently become my planned driving or determine my work sequence.

**Acceptance Criteria:**

**Given** an owned unexpired own-plan draft imported or entered through the existing E2 flow,
**When** the owner reviews mentor assignment information,
**Then** show the own plan as Egen arbeidsplan and allow explicit review/correction of planned FADDER/INSTRUKTØR assignment and applicable own activities using the shared editor,
**And** retain original interpreted values and manual correction provenance; an unexplained source code, missing assignment or ambiguous activity is not classified as mentoring by guessing,
**And** preserve service date, extended overnight times, each work part's reporting time/depot, actual bus versus vehicle duty and one combined-day order,
**And** keep assignment role, actual driver/guiding role and account authentication as separate concepts; selecting a planned mentor assignment creates no new login role, simulated context or operational permission.

**Given** the reviewed planned assignment is FADDER,
**When** its own-plan activities and accompaniment requirement are validated,
**Then** represent the requirement to accompany one same person for that person's whole shift during the fadder assignment, with person/linked-plan selection visibly pending until explicitly established in the later linking flow,
**And** do not invent a person, truncate the whole-shift requirement to a convenient trip or silently allow person switching within the same fadder assignment,
**And** reject classroom/office activity as fulfilment of that fadder role rather than silently converting it to instructor work; keep the editable input and explanation,
**And** keep genuine own-driving trips separately owned by Egen arbeidsplan; a fadder activity without accompaniment cannot be marked fully linked/ready through a fictional person,
**And** missing timing/person data remains identified as unresolved where applicable, without supplying false actual accompaniment evidence.

**Given** the reviewed planned assignment is INSTRUKTØR,
**When** the owner reviews the own-day activity sequence,
**Then** distinguish planned accompaniment periods, classroom teaching, office work and own driving, with known times/places and explicit unknowns,
**And** permit an instructor day containing classroom/office work and optional own driving with no accompaniment and no linked-person plan,
**And** preserve one or several planned accompaniment periods as distinct own activities, without choosing their person/trip automatically; later explicit linking may support different people and return to a previous person,
**And** missing/overlapping activity timing that prevents correct own-day order/final end must be resolved under existing E2 rules before confirmation, while unknown optional locations stay unknown,
**And** classroom/office preparation creates neither an active passenger trip nor fabricated stop progression or completed teaching/office work.

**Given** own-driving trips and planned mentor activities coexist,
**When** the own-plan review or a prepared-day preview is shown,
**Then** planned own driving refers only to trips belonging to the owner's own confirmed plan or its explicit valid revision,
**And** identical route/time/stop values do not turn another person's trip into an own trip; keep stable target-plan/activity identity in the stored contract,
**And** expose absent own trips through the existing correction/addition path rather than filling them from a future linked list,
**And** the own plan governs reporting, activity sequence and final own-day end; a mentor label or accompaniment boundary does not replace that lifecycle,
**And** acute takeover remains a later explicit operational action, not an alternative way to plan own driving in this review.

**Given** a corrected own draft or a scoped revision of an already confirmed own plan,
**When** the owner confirms the reviewed assignment/activity result,
**Then** confirm only the exact revision actually reviewed through 2.7/2.12, committing the allowed plan change and outbox event atomically before reporting it locally saved,
**And** if the draft, base plan or relevant state changes during review, mark the review stale and require comparison/confirmation again; cancel preserves the prior confirmed plan,
**And** confirming the own plan does not confirm an unreviewed linked plan, select a person/block, assert actual accompaniment, activate a new day or change the current driver/guiding state,
**And** permit confirmation of an otherwise valid own plan with accompaniment links explicitly pending; own-plan confirmation and readiness to accompany are separate statuses,
**And** preserve active own trip/pin, performed evidence and unrelated plans. If existing links are affected in an integration fixture, mark them unresolved for explicit repair, never retarget by similarity; actual linked-revision UI remains a later E6 slice,
**And** late plan changes retain the existing AD-12 final-end/earlier-limit rules and cannot silently extend day authority.

**Given** the confirmed own mentor plan is saved and reopened,
**When** the preparation/overview surface renders it online or from permitted local storage,
**Then** retain planned role, activity types/order, own-trip ownership, provenance and pending-link state without reimport or invented linked-person data,
**And** use a clear text label for the planned assignment within the own-plan panel; never imply that a prominent FADDER/INSTRUKTØR assignment label means operational guiding controls are already enabled,
**And** show unsupported/unavailable linked preparation honestly in this slice without presenting the whole mentor day as ready; a valid no-accompaniment instructor day does not receive a false missing-person error,
**And** unknown/stale data remains visibly so, with readable text/symbols, keyboard focus and shared movement restrictions for editing/review,
**And** a planned role, resumed view or scheduled boundary cannot unlock driver controls, reset outage history or copy another context's manual pin. Actual operational role controls remain separate stories.

**Given** persistence, synchronization, access or expiry fails,
**When** this slice saves, reads or confirms own-plan assignment state,
**Then** use existing owner-scoped IndexedDB and authenticated FastAPI/PostgreSQL plan/revision contracts, adding only the necessary assignment/activity fields and validation,
**And** enforce the role/activity/plan-ownership rules on the backend as well as the UI; a forged linked-plan own-trip reference or foreign account scope cannot bypass them,
**And** local write failure never reports a saved/confirmed revision; server failure leaves valid local work pending and only a matching receipt changes server-confirmation status,
**And** preserve the E1/E5 lock, pending-revocation, conflict and original expiry behavior, including no new/prepared-day start after ordinary expiry via an assignment change,
**And** this is private operational preparation, distinct from the public fictional instructor demo; no access to another person's account, raw-file retention or permanent person directory is added.

**Given** representative anonymized/fictional own plans and real PostgreSQL,
**When** the implementation is verified,
**Then** test a fadder assignment with pending whole-shift link and separate own trip, an instructor day with several planned accompaniment periods, and an instructor day with only classroom/office and optional own driving,
**And** test prohibited classroom/office-as-fadder classification, unexplained source code, missing optional place, ambiguous order/end, split-day reporting/depot and Friday 25:30 ordering through save/reopen,
**And** include two identical-looking own/foreign-plan trip fixtures, stale review, scoped revision, local failure, lost/mismatched receipt, wrong-owner API access, logout and expiry,
**And** verify that own-plan confirmation/reopen changes neither actual driving role nor movement permission and does not manufacture person links or performed work,
**And** distinguish plan-review tests from actual accompaniment, role transitions, qualified tablet usability and integrated E6 recovery, which remain their later acceptance boundaries.

**Traceability:** Own-plan preparation extensions of FR-2/4/5 and FR-6 ownership boundary, shared FR-16/20/24 and future FR-22 provenance under UX UJ-3/4. NFR-1–4; UX-DR4/5/6/7/8/26/27/28/29/38/39/43/44, with operational portions of UX-DR29–31 remaining subsequent E6 stories. EXPERIENCE FADDER and INSTRUKTØR assignment scope and revision ownership; DESIGN separate own/linked panels and text role indication. AD-2/4/5 atomic local/server plan state, AD-6 shared reviewed import, AD-9 assignment versus actual context, AD-10 bounded access and AD-12 own combined-day retention. All AD-1–AD-14 remain unchanged.

**Dependencies:** Implemented E2 own editor/import/confirmation/revision, E3 movement and actual-context contracts, E5 persistence/access/recovery through 5.13. No later linked-person import, accompaniment engine, takeover UI or E7 report is required to demonstrate this own-plan review and persistence slice.

**Size boundary:** Own-plan planned role/activity distinctions, review/confirmation, protected persistence and honest pending-link/no-accompaniment states. No new OCR engine, linked-person import, actual accompaniment selection/progression, unrestricted guiding mode, acute takeover, classroom/office execution view or summary renderer.

**Pilot qualification:** Controlled own-plan/browser/FastAPI/PostgreSQL cases contribute to E8-D. E8-P needs the actual reviewed forms/data, mounted readability and integrated later E6 role/link/recovery behavior; assignment confirmation alone is not permission to use mentoring on a real shift. E8-E remains field evaluation. No implementation or actual tests occur during planning.

**Approval:** Approved by the owner on 2026-09-26 as scoped. An own plan may be confirmed with a visibly pending link without confirming accompaniment or making the other person's trip planned own driving. Planning approval only; the approved copy in epics.md is canonical.
