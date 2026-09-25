# Development log

## 2026-09-21 – Project setup

### Work completed

- Cloned the assigned GitHub repository.
- Configured Git identity and verified the remote repository.
- Installed BMAD v6.12.0 according to Appendix B.
- Installed BMAD Core and BMad Method (BMM).
- Configured 29 BMAD skills for OpenAI Codex.
- Verified that the installation did not modify the existing README or `.gitignore`.
- Committed and pushed the setup to the `main` branch.

### AI use

OpenAI Codex was used to inspect Appendix B, run the BMAD installer, and verify the resulting files and Git status. All commands requiring changes were approved by the student.

### Verification

- BMAD installation completed without errors.
- Local branch was synchronized with `origin/main`.
- Working tree was clean after push.
- Setup commit: `23d620d`.

## 2026-09-21 – Product Brief

### Work completed

- Completed the BMAD Product Brief workflow for the bus-driver assistant.
- Defined the problem, users, MVP scope, success criteria, risks and broader vision.
- Separated the concise Product Brief from supporting evidence in an addendum.
- Sanitized supporting documentation before publication in the public repository.

### AI use

OpenAI Codex and the BMAD Product Brief workflow were used to facilitate structured discovery, inspect supplied course material and shift-report samples, draft the documents and perform editorial and privacy checks. Product decisions and scope priorities were approved by the student.

### Verification

- `brief.md` and `product-brief.md` were verified as identical.
- No code, PRD or architecture was created.
- Local paths and private operational identifiers were removed before publication.

## 2026-09-21 – Product Requirements Document

### Work completed

- Completed the guided BMAD Create PRD workflow for the bus-driver assistant.
- Defined and approved 25 functional requirements and four non-functional requirement groups.
- Clarified the course MVP, deferred capabilities and downstream technical validation.
- Reconciled the PRD with the Product Brief, source research and recorded decisions.
- Completed consistency, editorial and privacy reviews.
- Approved the PRD as final.

### AI use

OpenAI Codex with GPT-6 Astra and the BMAD PRD workflow facilitated requirements discovery, source research, drafting, adversarial review, reconciliation and privacy checks. Product decisions were reviewed and approved by the student.

### Time spent

Approximately 4.5 hours on guided PRD development and finalization.

## 2026-09-22 – UX design and validation

### Work completed

- Completed and approved the BMAD UX workflow using all five source documents, with the PRD and its addendum taking precedence over the briefs.
- Finalized English `DESIGN.md` and `EXPERIENCE.md`, five approved HTML references including a navigable 43-screen gallery, consolidated HTML/Markdown validation reports, reviewer reports, source reconciliation and decision history.
- Established landscape tablet layouts in Day A/Night C, vertical upcoming-first stops, current/next-stop emphasis, a persistent clock, relevant disruption headings and explicit data uncertainty.
- Confirmed PDF/image import, split working days with one summary, partial shift updates, persistent manual theme selection and an underlined active Auto control. Menu restrictions and the five-minute GPS-loss countdown remain explicit.
- Defined separate FADDER/INSTRUKTØR assignments, own driving and accompanied plans, explicit driver takeover, and accompanied-only summary/PDF evidence. Accompanied-person source files are deleted after import; necessary interpreted information remains in the mentor's working day.

### AI use

OpenAI Codex and the BMAD UX workflow supported iterative sketches, document drafting, source reconciliation and three user-selected validation lenses: document consistency/coverage, driver-position readability/interaction, and operational edge cases/role changes/data trust. The student reviewed the sketches, made product decisions and approved the completed UX and validation.

### Verification

- All 11 distinct validation findings were addressed; original reviewer reports and resolution records are preserved.
- Static checks verified token references, local/source links, paired component names and sketch navigation. Browser inspection checked clock placement and the active Auto underline.
- Mounted-device readability, touch, browser/sensor support and implemented behavior still require practical verification.
- Temporary browser profiles/caches, preview images and one-off working files are excluded from Git. Final documents, approved sketches, validation/reviewer reports, source tracing and the UX memlog are retained.
- No architecture or application implementation was started.

## 2026-09-23 – Step 4: Architecture completed

### Work completed

- Finalized the [Architecture Spine](../_bmad-output/planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md) using the approved Product Brief, PRD and UX as authoritative inputs.
- The student approved architecture decisions AD-1–AD-14 through the interactive BMAD Architecture workflow.
- Defined the V1 boundaries, modular monolith, React/TypeScript client, Python/FastAPI backend, PostgreSQL, six conceptual contracts and local operational authority with offline synchronization.
- Recorded import, source uncertainty, notice lifecycle, access, writer transfer, retention and compatible-release rules, together with portable Docker Compose delivery on the Windows desktop, Cloudflare access and an isolated fictional demo.
- Retained the decision log, source reconciliation and independent review reports with the finalized architecture.

### AI use

OpenAI Codex and the BMAD Architecture workflow supported interactive decisions, official-source research, document drafting, source reconciliation and independent architecture reviews. The student approved the architecture decisions and their constraints.

### Verification and remaining pilot prerequisites

- Reconciled the architecture with Product Brief, PRD, DESIGN and EXPERIENCE. Addressed the independent reviewers' findings; the final document lint reported zero findings.
- Architecture approval does not establish pilot readiness. OCR on representative anonymized files, actual Entur/Svipper-origin coverage and relevance, Lenovo/Brave GPS and interaction behavior, offline recovery, synchronization/conflicts, deletion and release compatibility still require implementation tests.
- Cloudflare Access renewal/expiry, trusted HTTPS over mobile networks, private/demo isolation, Windows restart recovery and acceptable desktop resource use/noise must also be tested before real-shift pilot use.
- No application implementation, external service provisioning or deployment was performed in this step.

### Next step

**Step 5: Epics & Stories**, based on the approved Product Brief, PRD, UX and Architecture Spine. Step 4 is complete. Neither BMAD Spec nor Epics & Stories is started in this session.

## 2026-09-23 – Step 5: Requirements checkpoint started

### Work completed

- Started the interactive BMAD Create Epics and Stories workflow using the approved planning documents and this development log. The student provisionally retained the proposed eight epics.
- Created [epics.md](../_bmad-output/planning-artifacts/epics.md) as a requirements-checkpoint draft: complete PRD functional/quality extraction, individual coverage for 25 FRs and four NFR groups, AD-1–AD-14 ownership, and 44 in-scope UX entries plus one deferred-scope marker.
- Recorded settled supersessions, ownership overlaps and previously implicit integration work. Proposed smaller testable slices for E2, E3 and E6 without writing detailed stories or removing V1 requirements.
- Separated demonstrable course delivery, pre-pilot qualification and subsequent three-working-day evaluation inside E8. Identified early source, OCR and target-device qualification work and unresolved capacity/course facts.

### AI use and verification

OpenAI Codex and the BMAD workflow supported source tracing, decomposition and documentation. Static checks verified exact PRD section extraction, requirement identifier coverage and local document links. No source feeds, OCR tooling, device behavior or application capability were tested; no application implementation, provisioning or deployment was performed.

### Current checkpoint

Awaiting the student's review of requirements, allocation and proposed evidence checkpoints. Step 1 is not marked complete, the epic structure remains provisional, and detailed stories have not been written. Full V1 fit within the reported 40–160-hour range remains unproven; realistic remaining capacity is needed before a delivery commitment. No BMAD Spec was started and no adopted architecture decision changed.

## 2026-09-23 – Step 5: Requirements approved; formal epic checkpoint

- The student explicitly approved the requirements, responsibility boundaries and eight epics as the basis for the next workflow step. Marked `step-01-validate-prerequisites` complete in [epics.md](../_bmad-output/planning-artifacts/epics.md).
- Preserved the approved E8-D demonstration, E8-P pre-pilot qualification and E8-E field-evaluation checkpoints inside E8, without changing V1 scope.
- Recorded the student's capacity correction: high priority and guaranteed more than 40 hours, but no reliable remaining budget. Capacity and delivery time are unresolved; neither 40 nor 160 hours is an assumed available budget. Requirements may only be deferred by a separate explicit decision.
- Opened step 2 and documented all eight formal epic outcomes, FR coverage, dependencies and shared-component boundaries. Earlier epics must deliver their own necessary access, persistence and privacy behavior; later integration/verification ownership is not a reason to leave earlier functionality incomplete.
- Awaiting the formal epic checkpoint response before story creation. Step 2 remains open; step 3 has not been opened. No detailed stories, implementation, provisioning, deployment or new architecture decisions were created. The saved checkpoint can be resumed on the next day.

OpenAI Codex and the BMAD workflow supported this documentation update. Static checks verify workflow state, eight epic entries and retained requirement mappings; these are not application or pilot test results.

## 2026-09-23 – Step 5: Formal epics approved; stopped before stories

- The student explicitly approved all eight formal epic boundaries and each epic's responsibility for access, persistence, error handling and privacy for its own functions.
- Marked workflow steps 1 and 2 complete in [epics.md](../_bmad-output/planning-artifacts/epics.md). Retained early source/OCR/tablet qualification and E8-D/P/E without changing approved V1 scope or architecture.
- Saved the next step as `step-03-create-stories`, unstarted. At the student's explicit request, stopped before opening that step or writing detailed stories; continuation is planned for tomorrow.
- Capacity and delivery time remain unresolved: more than 40 hours is confirmed, but neither 40 nor 160 hours is an assumed budget. Requirements cannot be deferred without a separate decision.
- No application implementation, provisioning or deployment was performed. OpenAI Codex recorded the approval and resume point; this is workflow status, not implementation or pilot evidence.

### Session close

The student requested saving today's Epics and Stories work and publishing the planning document and development log to the project's GitHub repository. Today's completed scope is requirements extraction/traceability and approval of the eight formal epics. Detailed stories remain unstarted; resume at `step-03-create-stories` when the student returns. This closes today's planning session without starting implementation.

## 2026-09-25 – Step 5: Interactive story creation resumed

- Resumed the approved requirements and eight epics; loaded the BMAD story-creation step. E8-D/P/E, architecture and unresolved capacity/delivery time remain unchanged.
- Drafted [Story 1.1](../_bmad-output/planning-artifacts/story-drafts/story-1.1.md) for individual review: private online sign-in/sign-out through React, FastAPI and PostgreSQL, with Given/When/Then criteria, requirement references, dependencies and implementation-versus-pilot evidence boundaries.
- The draft is separate from approved stories, following the workflow's per-story review requirement. Step 3 remains in progress at E1/Story 1.1; no story is approved yet.
- OpenAI Codex prepared this planning draft from the saved state and relevant requirements. No implementation, actual qualification tests, readiness check, provisioning or deployment occurred.

### Story 1.1 approved; Story 1.2 drafted

- The owner approved Story 1.1 with immediate client hiding/locking when logout is selected, before any server response. Unconfirmed server revocation remains explicit and retryable; success is never inferred from hiding the view.
- Updated the story and appended its approved version to epics.md. The fixed 14-day ordinary-access deadline remains unchanged; active-day and durable offline behavior retain the adopted architecture boundaries.
- Prepared Story 1.2 for individual review: persist local logout locking and pending revocation across reload/reconnect, settle revocation before ordinary private traffic and require fresh application login to unlock. It depends only on Story 1.1 and precedes private local draft data.
- Step 3 remains open; Story 1.2 is unapproved. These are planning changes only, without implementation or readiness testing.

### Story 1.2 approved; Story 1.3 drafted

- The owner approved Story 1.2 with testable storage-failure recovery: failed/unreadable lock or revocation storage must not automatically expose private content on restart/history; show an explicit error, follow AD-10 same-owner recovery and never silently discard unresolved revocation on fresh login.
- Updated and promoted Story 1.2 to epics.md with fault-injection cases for writes, reads, reload/reopen/history and fresh-login ordering. Stories 1.1 and 1.2 are approved; the workflow remains in step 3.
- Drafted Story 1.3 for individual review: create/reopen an unconfirmed local dated draft, atomically store its pending event, enforce ownership/logout locks and fixed seven-day draft expiry. Server synchronization is explicitly not claimed by this slice and remains subsequent E1 work.
- No implementation, actual tests, readiness check, provisioning or deployment was performed. Capacity, V1 scope, AD-1–AD-14 and E8-D/P/E remain unchanged.

### Story 1.3 approved; Story 1.4 drafted

- Approved Story 1.3 with the owner's AD-12 clarification: earliest applicable draft/day deadline, with known day-end facts interpreted using service date/timezone and no reset on reopening. A date alone does not invent an unknown planned end. Added explicit boundary tests and promoted the approved story into epics.md.
- Drafted Story 1.4 for individual review: synchronize the minimal unconfirmed draft to PostgreSQL, atomically commit its receipt, retry identical batches after lost responses, and enforce ownership, pending-logout ordering and expiry on all copies.
- Story 1.4 depends on approved Stories 1.1–1.3 and is limited to the first draft creation event; multi-device transfer, general conflicts and active-day recovery remain their adopted later scopes. E1 and workflow step 3 remain open.
- OpenAI Codex updated planning documents only. No implementation, qualification tests, readiness check, provisioning or deployment occurred.

### Story 1.4 approved; E1 summarized and Story 2.1 drafted

- The owner approved Story 1.4 and explicitly reiterated that only a valid receipt matching the sent batch can change local/pending status to server-confirmed. Promoted the approved story into epics.md.
- Summarized the four individually approved E1 stories and their bounded FR/UX/architecture coverage. Used the owner's instruction to proceed to the next individual review to continue to E2; no repeated approval of already accepted boundaries was requested.
- Drafted Story 2.1 as the early OCR qualification required by AD-6: representative formats/layouts, extraction errors/uncertainty, transient-copy cleanup, resource observations and a sanitized evidence report. A negative report completes investigation but does not pass the import gate or remove V1 formats.
- E2/Story 2.1 awaits review. Step 3 is not complete. No application implementation, actual OCR/source/device tests, readiness workflow, provisioning or deployment has started.

### Story 2.1 approved; Story 2.2 drafted

- The owner approved OCR qualification Story 2.1 with representative anonymized shifts and checked expected dates, times, activities and ordering. The report must identify actual tested formats/failure categories and distinguish what works, what requires driver checking and what currently fails.
- Recorded negative findings as explicit further-solution decisions, not automatic V1 reductions; approved and appended Story 2.1 to epics.md.
- Prepared Story 2.2 for individual review: targeted Entur query qualification for dated pilot-trip matching and complete day-data coverage, with explicit ambiguous/no-match/source-failure cases and the adopted bulk-data reconsideration boundary.
- No OCR/source/device tests or implementation were performed. Story 2.2 is unapproved and step 3 remains open; scope, architecture and E8-D/P/E are unchanged.

### Story 2.2 approved with service-time clarification; Story 2.3 drafted

- The owner clarified Tide's service date/extended-hour representation versus Svipper's calendar-date/ordinary-clock display: Friday 25:30 corresponds to Saturday 01:30 without changing the original service date or working-day order.
- Added checked temporal cases, including several trips sharing Saturday 01:30, and explicit investigation of actual Entur date fields, identifier semantics and unresolved ambiguities. No source field or service-day inference is assumed from display time alone. Promoted Story 2.2 as approved.
- Drafted Story 2.3 for review: direct addition/correction of unconfirmed draft trips and other activities, preserving both time representations, provenance, ordering, access and fixed expiry. File interpretation, timetable lookup and final plan confirmation remain later slices.
- This records qualification requirements, not completed Entur research or tests. No implementation, readiness check, provisioning or deployment occurred; workflow step 3 remains open.

### Story 2.3 approved; Story 2.4 drafted

- The owner approved Story 2.3 with a manual cross-midnight correction/save/reopen test: Friday 25:30 retains Friday service date, appears as Saturday 01:30 in calendar representation and remains in its expected working-day position. Unknown fields remain visibly unknown without guessed values.
- Added those criteria and promoted Story 2.3 into epics.md. Prepared Story 2.4 for individual review: text-PDF interpretation into the shared unconfirmed draft editor, with qualified extraction, transient originals, source provenance and protected failure/retry handling.
- Scanned PDF/images, timetable completion, final driver confirmation and active-plan revisions remain required later E2 slices. Qualification-story approval does not establish that extraction tests have passed.
- No implementation, actual tests or readiness workflow occurred; Story 2.4 and step 3 remain open.

### Story 2.4 approved; Story 2.5 drafted

- The owner approved Story 2.4 with side-by-side transient PDF/activity review, a preserved editable draft on reopening and explicit guidance to select the original again for comparison.
- Added retained missing-page/part coverage warnings so incomplete extraction cannot resemble a complete plan; comparison-file reselection cannot silently reimport, overwrite corrections or confirm work. Promoted Story 2.4 to epics.md.
- Drafted Story 2.5 for review: extend the same unconfirmed flow to scanned PDF and JPG/PNG, processing relevant scanned pages with qualified OCR, visible uncertainty and transient-copy cleanup.
- No implementation, actual OCR tests or readiness check occurred. Story 2.5 and step 3 remain open; V1 and architecture are unchanged.

### Story 2.5 approved; Story 2.6 drafted

- The owner approved Story 2.5 with shifts spread across multiple JPG/PNG files: visible and controllable file order, additive import into the same unconfirmed draft, and protection against duplicate activities and lost manual corrections.
- Added checked cases for out-of-order/overlapping files, later additions, retries, failed/missing parts and save/reopen. Cropped, unreadable and missing content stays uncertain/unknown; OCR success never confirms the plan. Promoted Story 2.5 to epics.md.
- Drafted Story 2.6 for individual review: match one unconfirmed draft trip to a supported dated timetable journey, explicitly select ambiguous candidates, preserve service/calendar representations and distinguish no match from source failure. Dependencies are implemented Story 2.3 and actual source qualification under Story 2.2.
- OpenAI Codex updated planning documents and saved the resume point at Story 2.6. No implementation, source/OCR tests, readiness check, provisioning or deployment occurred. Step 3 remains open; V1, AD-1–AD-14 and E8-D/P/E remain unchanged.

### Story 2.6 approved; Story 2.7 drafted

- The owner approved Story 2.6 with explicit tests for manually corrected times/stops differing from the source: retain the correction, display the source value and discrepancy, and prevent fresh or delayed matching responses from silently replacing it. Unique matching requires journey identity and service-date evidence, not just matching line number and clock time.
- Updated and promoted Story 2.6 into epics.md. Drafted Story 2.7 for individual review: initial own-plan overview, physical bus assignment separate from Vogn, and explicit revision-specific driver confirmation with atomic persistence and draft cleanup.
- Kept confirmed-plan status separate from downloaded day data, complete application assets, server acknowledgement and pilot qualification. Whole-day data preparation, split parts and active-plan revisions remain subsequent required E2 slices.
- OpenAI Codex saved the resume point at unapproved Story 2.7. No implementation, qualification tests, readiness workflow, provisioning or deployment occurred; scope, architecture, unresolved capacity and E8-D/P/E remain unchanged.

### Story 2.7 approved; Story 2.8 drafted

- The owner approved Story 2.7 with reviewed unmatched trips permitted in a confirmed plan once blocking service-date, sequence and planned-final-end ambiguities are resolved. Missing source matches, stops and physical bus remain explicitly unknown/missing rather than verified by confirmation.
- Added testable rejection of stale review: any draft change during review requires a new review before confirmation. Promoted the approved Story 2.7 into epics.md.
- Drafted Story 2.8 for individual review: whole-confirmed-day transit-data preparation, locally verified per-trip coverage in a revisioned OfflineBundle manifest, partial download/retry and storage failures, preserved corrections, stale-revision handling and privacy/expiry. Plan confirmation, local data, application assets and pilot qualification remain distinct.
- OpenAI Codex saved the resume point at unapproved Story 2.8. No implementation, actual source/device tests, readiness workflow, provisioning or deployment occurred. E2/step 3 remain open; V1, architecture, unresolved capacity and E8-D/P/E are unchanged.

### Story 2.8 approved; Story 2.9 drafted

- The owner approved Story 2.8 with visible per-trip coverage even when only part of the day downloads. Partial data cannot produce a whole-day-prepared status. Added the explicit criterion and promoted Story 2.8 into epics.md.
- Drafted Story 2.9 for individual review: initial split-day composition and confirmation, each part's reporting time/depot, explicit gaps without invented rest/transfers, whole-day manifest coverage and one combined-day identity/planned-final-end deadline.
- Runtime gap transitions, final end/abort and one combined summary retain E3/E7 ownership. Active-plan revisions remain later E2 work. The preparation slice reuses existing editor, confirmation and data-manifest contracts.
- OpenAI Codex saved the resume point at unapproved Story 2.9. No implementation, actual tests, readiness workflow, provisioning or deployment occurred; V1, architecture, unresolved capacity and E8-D/P/E remain unchanged.

### Story 2.9 approved; Story 2.10 drafted

- The owner approved Story 2.9 with each work part's reporting time and depot visible in review, while confirmation, day-data coverage and expiry apply to the combined working day. Added this explicitly and promoted Story 2.9 into epics.md.
- Drafted Story 2.10 for individual review: additions-only manual revision of the confirmed own plan, visible target/scope and comparison, explicit current-revision confirmation, preserved performed evidence/manual active-trip context, revised data coverage and reviewed planned-final-end/retention effects.
- Bounded implementation to the revision action and preparation UI with operational-state fixtures. E3 must integrate the shared movement policy before operational use; file replacement/reconciliation, linked plans and full conflict resolution remain their assigned later scopes. No second movement or revision engine is introduced.
- OpenAI Codex saved the resume point at unapproved Story 2.10. No implementation, tests, readiness workflow, provisioning or deployment occurred; E2/step 3 remain open, with V1, architecture, unresolved capacity and E8-D/P/E unchanged.

### Story 2.10 approved with AD-12 clarification; Story 2.11 drafted

- Read the exact adopted AD-12 rule and clarified Story 2.10: draft expiry is original creation plus seven days or earlier associated-day expiry; derived day data uses actual end/abort plus seven days, or planned final end for a never-ended day. Only a confirmed revision can change the latter planned reference. Revision time never starts a new seven-day period, renews a fixed earlier draft deadline or resurrects expired data.
- Added late-addition cases covering later/earlier/unchanged planned final end, old drafts, prior expiry and actual ending learned on reconnect. Active trip, performed evidence and progression remain unchanged. Recorded owner approval and promoted Story 2.10 into epics.md without modifying AD-12.
- Drafted Story 2.11 for individual review: explicit target and whole-day/selected-part/additions scope, updated-file comparison with visible changes/ambiguities and protected existing work. Split proposal construction from subsequent replacement/removal confirmation to keep each result testable.
- OpenAI Codex saved the resume point at unapproved Story 2.11. No implementation, actual tests, readiness workflow, provisioning or deployment occurred. V1, architecture, unresolved capacity and E8-D/P/E remain unchanged; E2 and step 3 stay open.

### Story 2.11 approved; Story 2.12 drafted

- The owner approved Story 2.11 with selected scope and compared base revision persisted/displayed with the proposal. A changed base plan marks the proposal stale and requires new comparison before use. Partial-file absence alone never justifies proposed deletion. Promoted the updated approved story into epics.md.
- Drafted Story 2.12 for individual review: explicit current-proposal confirmation and atomic application of in-scope future changes/removals. Commit-time checks preserve active/performed state even when it changes during review; failure never produces a partially applied plan.
- Included immutable retries/receipts, reopened applied-versus-unapplied status, backend conflict preservation, revised data coverage and the approved exact AD-12 boundaries. E3 movement integration and E6 linked-plan behavior retain their separate ownership.
- OpenAI Codex saved the resume point at unapproved Story 2.12. No implementation, actual tests, readiness workflow, provisioning or deployment occurred; E2/step 3 remain open, with V1, architecture, unresolved capacity and E8-D/P/E unchanged.

### Story 2.12 approved; E2 summarized and Story 3.1 drafted

- Recorded approval of Story 2.12 without scope changes and promoted it into epics.md. Summarized all twelve E2 stories and their FR/UX/architecture coverage, preserving later integration responsibilities.
- Used the owner's explicit next-story instruction to proceed into E3, following the E1 transition precedent. Drafted Story 3.1 for individual review: early real Lenovo/Brave position/speed qualification, separate quality evidence, loss/recovery cases and honest field-target limitations. No production sensor engine or pilot readiness is claimed.
- Added the requested provisional counts: E1 4 approved, E2 12 approved, E3 12–15, E4 7–9, E5 8–11, E6 8–11, E7 6–8, E8 6–9. Counts can change during review and are neither time estimates nor approved future story lists. E8-D/P/E remain separate.
- OpenAI Codex saved the resume point at unapproved Story 3.1. No implementation, actual tests, readiness workflow, provisioning or deployment occurred; step 3 remains open and V1/architecture/capacity decisions are unchanged.

### Story 3.1 approved; Story 3.2 drafted

- The owner approved Story 3.1 with a five-minute outage after valid position/speed. Added separate evidence for sample freshness limits, actual browser output and realistic 100-m progression feasibility against independently observed passages without driver interaction while moving. Promoted the approved story into E3 in epics.md; qualification tests have not been run.
- Drafted Story 3.2 for individual review: shared movement permission, visible Menu/reasons/countdown and guarded existing overview/revision actions. Preserve unknown-versus-zero, initial-startup history and five-minute outage/recovery rules across reopening, with storage/timing failure cases and no second movement engine.
- OpenAI Codex saved the resume point at unapproved Story 3.2. No implementation, actual tests, readiness workflow, provisioning or deployment occurred; E3/step 3 remain open and V1, architecture, E8-D/P/E and unresolved capacity remain unchanged.

### Story 3.2 approved; Story 3.3 drafted

- Approved Story 3.2 with separate visible startup/outage-exception states labelled unknown speed and an explanation of available actions. Added explicit restart/stale-zero cases that cannot create access or reset/start the outage interval; reliability follows actual 3.1 quality limits. Promoted the approved story into epics.md.
- Drafted Story 3.3 for individual review: manual actual-trip choice/correction through Menu, using the shared movement policy, retaining the selected trip against time/proximity changes, preserving prior evidence and avoiding false stop/completion claims.
- Kept automatic initial selection and progression separate so the manual fallback is independently demonstrable. Missing-stop selection and existing authority/storage/receipt/expiry rules remain explicit; complete offline authority and operational fallback integration are not claimed.
- OpenAI Codex saved the resume point at unapproved Story 3.3. No implementation, actual tests, readiness workflow, provisioning or deployment occurred; E3/step 3 remain open and V1, architecture, E8-D/P/E and capacity decisions are unchanged.

### Story 3.3 approved; Story 3.4 drafted

- Recorded owner approval of Story 3.3 with its described result, scope and criteria and promoted the approved manual-selection story into epics.md.
- Drafted Story 3.4 for individual review: initial automatic trip selection using confirmed plan, qualified position and current time together. Unique evidence permits selection; ambiguity requires permitted explicit choice and inadequate evidence retains direct manual fallback.
- Added overlap/direction, overnight, delay, stale-result/manual-choice race and reopen cases. Existing active selection cannot be replaced by rerunning initial matching; later progression/transitions remain separate required stories.
- OpenAI Codex saved the resume point at unapproved Story 3.4. No implementation, actual tests, readiness workflow, provisioning or deployment occurred; E3/step 3 remain open, and V1, architecture, E8-D/P/E and unresolved capacity are unchanged.

### Story 3.4 approved; Story 3.5 drafted

- Approved Story 3.4 with explicit simple waiting status for ambiguous candidates while movement locks choice. No arbitrary driving view or prompt to resolve ambiguity while driving. Promoted the updated approved story into epics.md.
- Drafted Story 3.5 for individual review: adopted three-stop hierarchy, persistent route/destination/clock and Menu, truthful unknown/restored progress, and known sequence boundaries distinct from missing data. At-stop order follows the approved UX supersession, not the older PRD wording.
- Kept progression generation separate from presentation, using isolated labelled test fixtures without simulated operational substitution. Theme behavior, wake lock and notice integration remain later required stories; mounted glance readability remains actual-device qualification.
- OpenAI Codex saved the resume point at unapproved Story 3.5. No implementation, actual tests, readiness workflow, provisioning or deployment occurred; E3/step 3 remain open and V1, architecture, E8-D/P/E and unresolved capacity remain unchanged.

### Stories 3.5 and 3.6 approved — recovery after tool interruption

- At the owner's request, inspected actual files before continuing. Story 3.5 still had draft/unapproved status, story-3.6.md did not exist, epics.md stopped at approved Story 3.4, and neither later approval was in this log. The tool connection was working during recovery.
- Recorded the previously given 3.5 approval with preserved stop ordering/emphasis and an explicit criterion that uncertain retained context is not a fresh position observation.
- Recreated 3.6 from the proposal actually presented and approved in conversation, recording the latest clarification: measure the 100-m target against independently observed departure/passage, including passage without stopping and without driver interaction while moving. Document deviations and never claim fulfillment when the target is missed.
- Promoted each approved story once into epics.md and updated approval metadata/resume status. Next is Story 3.7, not yet drafted at this repair checkpoint; no approval of that story is implied.
- OpenAI Codex repaired planning records only. No implementation, actual tests, readiness workflow, provisioning, deployment or GitHub upload occurred. E3/step 3 remain open and V1, architecture, E8-D/P/E and unresolved capacity are unchanged.

### Story 3.7 drafted for individual review

- Read the saved E3 state, approved 3.6, current BMAD step and exact UX movement rules. Drafted 3.7 as manual stop correction and qualified return to normal progression within the selected trip.
- Kept direct GPS-loss previous/next controls separate from arbitrary selection: direct controls retain the approved in-motion exception during the five-minute lock; arbitrary choice uses 3.2's shared permission, including labelled unknown-speed exceptions. Network loss alone does not expose GPS-loss arrows.
- Included manual provenance, preserved trip pin/history, stale-action/recovery races, repeated stop occurrences, local/server persistence, restart and expiry. Terminal/return behavior, diversion recovery and missing-list outcome fallback remain separate required integration slices.
- Saved unapproved story-drafts/story-3.7.md and updated the resume pointer only; approvedStories remains through 3.6 and no canonical 3.7 was appended. No implementation, actual tests, readiness workflow, provisioning or deployment occurred. E3/step 3 and the individual review remain open.

### Story 3.7 approved; Story 3.8 drafted

- Registered the owner's 3.7 approval with qualified GPS-loss states from 3.1, no direct arrows for unknown speed alone/network failure, and at most one known stop per press. Preserved manual provenance and protection against ambiguous automatic overwrite; promoted the approved story once into epics.md.
- Drafted 3.8 for individual review: source-supported diversion sequences or qualified recovery at later stops (including two/ten ahead) within the same selected trip. No inferred replacement stops from generic notices, no backfilled visits and no proximity-based line change.
- Preserved shared movement/persistence/retention rules, explicit source qualification gaps and separate terminal/missing-list outcomes. Saved the resume point at unapproved 3.8. No implementation, actual tests, readiness workflow, provisioning or deployment occurred; V1, architecture, capacity and E8-D/P/E are unchanged.

### Story 3.8 approved with occurrence identity and visible observation gaps

- Registered owner approval with a repeated-visit test requiring the correct stop occurrence in the selected trip; name, physical stop identity or proximity alone cannot disambiguate repeated occurrences.
- Added visible observation-gap preservation through recovery/save/reopen. Two-/ten-stop jumps do not backfill observed passages or establish that the 100-m target was met for the unobserved interval.
- Updated the approved story file and promoted its exact body once into epics.md. Saved the next-story pointer at 3.9, which is not yet drafted. No implementation, actual tests, readiness workflow, provisioning or deployment occurred; E3/step 3 remain open and V1/architecture/E8-D/P/E are unchanged.

### Story 3.9 drafted for individual review

- Read the adopted UX/AD-9 terminal rules and drafted 3.9: registered observed/manual final arrival completes a non-aborted passenger trip; ordinary transition follows ten seconds, while same-route return waits for separate qualified start evidence or an extra manual Next action during qualified GPS loss.
- Included repeated/co-located stop occurrences, separate manual final-arrival/return actions, protected context/timer races, non-passenger next entries, observation-gap preservation, atomic persistence and retained provenance. Passenger completion does not end the combined workday or renew retention/authority.
- Saved unapproved story-drafts/story-3.9.md and updated the resume point. Approved stories remain through 3.8; detailed non-passenger, missing-list outcomes and day-end integration remain later required work. No implementation, actual tests, readiness workflow, provisioning or deployment occurred.

### Story 3.9 approved; Story 3.10 drafted

- Registered 3.9 approval with explicit co-located-stop cases: arrival/waiting, sustained position, GPS jitter, schedule and ten-second expiry do not independently start a return. Qualified GPS loss requires the separate intentional Next press after registered final arrival. Promoted the approved story once into epics.md.
- Drafted 3.10 for individual review: adopted non-passenger displays and context, position-plus-time completion evidence versus Gjennomføring usikker, preserved meal classification, split-day gaps and no automatic day ending at depot.
- Kept actual physical actions unverified, manual summary confirmation/final ending in E7 and operational bus replacement/missing-list outcomes separate. Saved the resume point at unapproved 3.10. No implementation, tests, readiness workflow, provisioning or deployment occurred; V1, architecture, E8-D/P/E and capacity decisions are unchanged.

### Story 3.10 approved; Story 3.11 drafted

- Registered approval with the owner's evidentiary clarification: position/time can support movement/location, but alone do not prove a taken break, relocation performed as planned, bus replacement or handover. Updated completion criteria and tests so all four stay uncertain without outcome-specific evidence; promoted the approved story once into epics.md.
- Drafted 3.11 for individual review: supported stop-list recovery first, followed by explicit manual trip completion/abort and next-activity selection when no usable list exists. No invented final-stop/GPS evidence or automatic workday closure; Menu movement rules apply separately from direct GPS-loss arrows.
- Included cancellation, late recovery after manual outcome, atomic persistence, retries, offline reopen and provenance for later summaries. Saved the resume point at unapproved 3.11. No implementation, actual tests, readiness workflow, provisioning or deployment occurred; E3/step 3 remain open and V1/architecture/E8-D/P/E/capacity decisions remain in force.

### Story 3.11 approved; Story 3.12 drafted

- Registered 3.11 approval with recovery attempted when the source is available; source failure/offline status cannot block an explicit permitted manual outcome. Added source-failure/offline cases preserving manual origin and uncertainty through sync/reopen; promoted the approved story once into epics.md.
- Drafted 3.12 for individual review: explicit interrupted/skipped-trip outcomes and next-activity selection through the shared engine, distinguishing these from correction of an erroneous tracking choice. Later selection never automatically completes/skips intervening work.
- Included movement/authority checks, preserved observed portions, late-event races, atomic persistence and manual evidence for E7. Saved the resume point at unapproved 3.12. No implementation, tests, readiness workflow, provisioning or deployment occurred; E3/step 3 remain open and adopted scope/architecture/E8-D/P/E/capacity decisions remain unchanged.

### Story 3.12 approved; Story 3.13 drafted

- Registered owner approval of 3.12 with its described scope, retaining erroneous-selection/interrupted/skipped distinctions and prior observations. Promoted the approved story once into epics.md.
- Drafted 3.13 for individual review: manual physical bus replacement (including fault-related replacement) versus correction of a mistyped number, with preserved active trip/pin/progression and truthful manual evidence. Planned bus change, Vogn and source refresh cannot update actual assignment automatically.
- Included shared movement rules, stale-form/duplicate handling, atomic persistence, offline recovery and expiry. A reported replacement does not certify inspection/handover or settle an ambiguous planned activity. Saved the resume point at unapproved 3.13; no implementation, tests, readiness workflow, provisioning or deployment occurred.

### Story 3.13 approved; Story 3.14 drafted

- Registered 3.13 approval with reported replacement occurrence time separate from registration/server receipt times. Unknown actual change time remains unknown and earlier observations cannot be reassigned by guessing. Added known/unknown/overnight/delayed-sync cases and promoted the approved story once into epics.md.
- Drafted 3.14 for individual review: always-available adopted Day/Night and Auto control, persistent manual preference, independent movement/timer/context state and explicit unavailable Auto handling. Actual automatic trigger/stability requires Lenovo/Brave qualification; manual fallback does not pass that requirement.
- Saved the resume point at unapproved 3.14. No implementation, tests, readiness workflow, provisioning or deployment occurred; E3/step 3 remain open and adopted scope/architecture/E8-D/P/E/capacity decisions remain in force.

### Story 3.14 approved; Story 3.15 drafted

- Registered approval of 3.14 with persistent manual preference until explicit Auto and no false Auto fulfillment from working manual fallback; promoted the approved story once into epics.md.
- Drafted 3.15 for individual review: browser-supported active-trip screen wake, honest pending/held/released/unavailable states, resource cleanup and foreground recovery without altered trip/movement state. Actual Lenovo/Brave duration/power/display tests distinguish reported acquisition from observed behavior.
- Preserved separate wake/GPS/network/theme status and no native/background guarantees or media workarounds. Saved the resume point at unapproved 3.15; E3 coverage review remains pending. No implementation, tests, readiness workflow, provisioning or deployment occurred; adopted scope/architecture/E8-D/P/E/capacity decisions are unchanged.

### Story 3.15 approved; E3 coverage checkpoint presented

- Registered owner approval of 3.15 with capability status grounded in actual Lenovo/Brave screen behavior; browser-reported acquisition is separate evidence and no background or unqualified support is promised. Promoted the approved body once into epics.md.
- Checked the E3 requirement allocation, adopted UX/AD-9 boundaries and story dependencies. Saved the 15-story coverage summary, preserving E7 whole-day end/abort ownership, E4 notices, E5 full offline authority/recovery and E6 roles. No additional E3 story is currently proposed.
- Identified two narrow test-level gaps in existing approved UX requirements: explicit dialog focus restoration/motion closure in 3.2 (UX-DR39), and meaningful stop-state announcements without poll/repeat noise in 3.5 (UX-DR40). Proposed the clarifications in the summary for owner approval; did not silently amend the approved stories.
- Preserved actual-device/source/100-m/Auto/wake qualification risks and distinct E8-D/P/E gates. Saved status at E3 coverage/continuation awaiting owner confirmation, with no pending individual story and no E4 draft. All 15 E3 stories are individually approved; step 3 remains open.
- OpenAI Codex changed planning documents only. No implementation, actual tests, readiness workflow, provisioning, deployment or GitHub upload occurred. V1, AD-1–AD-14, eight epic boundaries and unresolved capacity/delivery remain unchanged.

### E3 planning approved and paused before E4 — 2026-09-25

- The owner approved the E3 coverage summary and both accessibility-test clarifications. Incorporated UX-DR39 focus entry/restoration, cancellation and movement-triggered closure into 3.2; incorporated UX-DR40 meaningful stop-state announcements without repeated-poll noise into 3.5. Updated their individual files and canonical copies in epics.md, retaining prior approvals.
- E3 planning is complete with 15 individually approved stories and an approved epic-completion checkpoint. Saved E4 as the next continuation point in step-03-create-stories and explicitly paused at the owner's request. E4 has not started; no E4 story was created.
- The owner requested a commit and push of the planning documents and development log. This checkpoint records the complete approved E1–E3 story work accumulated locally; Git publication is performed after document verification, with its outcome reported separately.
- Planning approval remains distinct from implementation and actual qualification. No application implementation, device/source testing, readiness workflow, final workflow validation, provisioning or deployment occurred. V1, AD-1–AD-14, eight epics, E8-D/P/E and unresolved capacity/delivery remain unchanged.
