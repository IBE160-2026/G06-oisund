---
status: approved
created: 2026-09-27
epic: E8
story: '8.11'
type: qualification-decision
approved: true
approvedOn: 2026-09-27
dependencies: ['8.5', '8.7', '8.8', '8.9', '8.10']
---

### Story 8.11: Record the Evidence-Based E8-P Decision Before Actual-Shift Use

As the pilot owner,
I want one traceable decision showing whether the required qualification gates have passed for the intended release and equipment,
So that permission to begin actual-shift use is explicit and cannot be inferred from approved plans, a demonstration or completed reports.

**Acceptance Criteria:**

**Given** the approved V1 requirements, UX decisions, AD-1–AD-14 and available executed qualification reports,
**When** the E8-P decision packet is assembled,
**Then** identify the candidate client/backend/build/schema versions, source/provider configuration, actual Lenovo/Brave and Windows host, and intended pilot use within the adopted scope,
**And** map each mandatory gate item to its requirement, owning story, dated evidence and tested conditions, separating implementation status from passed, failed, blocked and not-run verification results,
**And** preserve the difference between actual observations, documented provider semantics, synthetic faults, accelerated boundaries and unknowns. A report's completion or a story's planning approval is not a capability pass,
**And** check that the evidence still applies to this exact candidate and its relevant configuration; changed contracts, hardware/settings or source semantics require affected revalidation rather than inheriting an old pass automatically,
**And** keep E8-D demonstrability status separately visible without making assessor acceptance or an affirmative E8-D result a substitute for operational evidence. The three-workday E8-E evaluation is subsequent work, not a prerequisite used to justify starting an unqualified pilot.

**Given** the five adopted architecture release gates,
**When** their coverage is checked,
**Then** include representative import and actual timetable/notice-source evidence from 8.7, including dated matching, full-day/per-trip coverage, explicit driver confirmation, transient-file cleanup and source metadata/lifecycle limitations,
**And** include 8.8 actual mounted-device position/speed and 100-m progression results against independent passage/departure references, movement/role restrictions, readability/touch, Auto, observed screen-wake and actual audio evidence,
**And** include 8.9 full-duration offline/restart, local/database atomicity, receipt/conflict/transfer, unknown-role recovery, terminal settlement and all-copy expiry evidence. Report actual duration separately from fast-forwarded failure cases,
**And** include 8.5/8.9/8.10 private access, actual Access expiry/renewal/logout, HTTPS, demo isolation and documented provider upload/cache/logging handling before real files, plus measured Windows downtime, home-network recovery and resource/noise evidence with the owner's acceptability decision,
**And** include 8.10's concrete retained-client/new-backend and local migration/activation evidence through affected data expiry, with active days, pending work, logout and immutable receipts preserved,
**And** identify missing or contradictory evidence at item level. Do not average passing items across gates, treat zero observed notices as source coverage or count a working manual fallback as a passed automatic requirement.

**Given** negative findings, accepted architectural limitations or unresolved solution questions,
**When** their disposition is prepared for owner review,
**Then** distinguish an already adopted limitation (such as sign-in before Docker startup and possible permanent loss without historical backups) from a newly failed capability, missing evidence or proposed requirement change,
**And** record what the accepted limitation permits and its observed consequences; it does not waive the tests or extend access/retention. A new exception cannot be inferred from the existence of an older accepted risk,
**And** keep 5.4/7.1 explicitly unresolved until its separate solution decision, with affected behavior/status and earliest applicable deadlines shown. Client timestamps, host uptime and successful receipt transport cannot serve as disconnected-time proof,
**And** a solution decision alone is not a passed implementation or test: link the adopted resolution and the required implemented/retested evidence before closing the affected gate item,
**And** keep material source/OCR/device/privacy/recovery/release failures and mandatory blocked/not-run cases open. Do not silently narrow the pilot to avoid them, substitute simulation/manual entry, revise AD-1–AD-14 or remove V1 requirements,
**And** any proposed scope/architecture change goes to a separate explicit owner decision and subsequent affected planning/evidence update; this checkpoint does not enact such a change or label a waived test passed.

**Given** the versioned packet and item-level findings,
**When** the owner reviews the formal E8-P checkpoint,
**Then** present an explicit recommendation with reasons and record the owner's dated outcome as permission granted, not granted, or decision pending, linked to the exact evidence/candidate version,
**And** an affirmative outcome requires recorded applicable passes for all mandatory gates and resolved blocking decisions with evidence, explicitly including the 5.4/7.1 timing basis. No conditional pass may hide a mandatory failed, blocked or not-run item,
**And** if evidence is insufficient or contradictory, record what must be resolved/tested and retain no-permission/pending status without erasing the negative result. A completed negative decision packet can complete this documentation task while E8-P remains unpassed,
**And** obtain explicit owner confirmation for the actual gate outcome; acceptance of this story plan, silence, a deployment URL or automatic checklist completion is never permission for real shifts,
**And** state the qualified release, equipment/configuration and tested limitations. A later material change or discovered invalidating fault requires affected requalification and an explicit updated decision before renewed reliance; unrelated evidence need not be rerun without reason,
**And** do not call E8-E complete, all V1 requirements satisfied or instructor assessment passed merely because E8-P permits the bounded actual-shift pilot.

**Given** an E8-P decision is recorded,
**When** the handoff to later evaluation is prepared,
**Then** keep the decision, evidence index, unresolved actions and applicable operating limitations readable and versioned, with a clear distinction between permission granted and work still needed before it can be granted,
**And** link existing preparation, known-failure and recovery instructions, preserving the adopted rules for offline readiness, source uncertainty, access and no required interaction while driving. Do not create a new operational policy or instruct a driver to troubleshoot while moving,
**And** state that the later E8-E protocol and three actual assigned workdays remain separate; neither scheduling nor execution of those days occurs in this decision story,
**And** retain only sanitized decision/evidence references, not private shift originals, raw GPS, secrets or database snapshots. No pilot archive or new service/database entity is needed,
**And** keep capacity/delivery uncertainty explicit without using it to pass missing requirements. Unresolved assessment scheduling may remain an E8-D issue but cannot conceal an operational E8-P blocker.

**Given** the packet and decision rules are checked for correctness,
**When** missing, failed, stale or contradictory evidence is encountered,
**Then** verify the packet would retain no-permission/pending status for cases such as only simulated GPS evidence, no representative source example, unknown provider handling, unresolved timing eligibility, untested noise acceptability or a required retained-client failure,
**And** verify that a completed negative report and an owner-approved proposed fix remain distinct from implemented/retested success, and that an outdated pass does not cover a materially changed candidate,
**And** verify the affirmative record is possible only with the mandatory evidence and explicit owner decision. Any labelled examples used to check this document's logic must remain examples, never an actual permission record,
**And** record omissions/corrections without inventing test execution or overwriting earlier evidence. This is a qualification-decision check, not activation of BMAD implementation readiness or step-04 final validation.

**Traceability:** Formal E8-P boundary and all five architecture pre-pilot gates; FR-1–24 operational requirements, NFR-1–4 and the applicable approved UX inventory. FR-25/E8-D remains separately reported; SM-1–4 and distraction/trust evaluation belong to subsequent E8-E. AD-1–AD-14 remain binding, particularly AD-6/7/9 actual capability, AD-10/11/12 authority/time/privacy and AD-13/14 operating/release evidence. This story consolidates decisions; owning stories still implement and test their functions.

**Dependencies:** Executed reports/evidence from 8.5 and 8.7–8.10 with relevant underlying E1–E7 results, plus the owner for the eventual formal decision. The packet can honestly record absent evidence or a negative outcome; absence cannot support permission. No future E8-E story or actual-shift observation is needed to record E8-P, and no future story is relied on to supply a missing mandatory pre-pilot pass.

**Size boundary:** One traceable versioned E8-P packet, discrepancy/action list, owner decision and handoff references. Reuse existing reports; no new test campaign, feature implementation, architecture change, automated approval system, pilot execution or readiness workflow. Resolving a blocker remains separately owned work followed by an updated evidence-based gate decision.

**Qualification boundary:** This is an approved story plan only. No actual E8-P assessment/outcome, permission for shifts, implementation, tests, provisioning, deployment or BMAD readiness/final-validation step is performed now. E8-D/P/E remain separate pending checkpoints.

**Approval:** Approved by the owner on 2026-09-27 as the plan for the decision basis, not E8-P permission. Actual shifts require a later dated owner decision based on passed mandatory gates and resolved blockers, explicitly including the 5.4/7.1 timing basis. Planning approval only; the approved copy in epics.md is canonical.
