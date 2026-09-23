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
