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

## 2026-09-23 – Step 5: Requirements and formal epics approved

- Used approved Brief, PRD, UX and AD-1–AD-14 to extract 25 FRs, four NFR groups and 44 in-scope UX requirements plus a deferred-scope marker into [epics.md](../_bmad-output/planning-artifacts/epics.md). Recorded supersessions, responsibility boundaries, dependencies and early source/OCR/device qualification.
- The owner approved workflow steps 1 and 2: eight formal epics, each responsible for its own access, persistence, error handling and privacy. E8-D (demonstrable delivery), E8-P (pre-pilot permission) and E8-E (field evaluation) remain separate.
- Corrected capacity assumptions: more than 40 hours is guaranteed, but no reliable remaining budget or delivery date exists. Neither 40 nor 160 hours is an available fixed budget; deferring a requirement needs a separate decision.
- Stopped before stories at the owner's request. The owner requested saving and GitHub publication for this session; that request is historical, not evidence that later local work is published.

## 2026-09-25 – E1–E3 story planning

| Epic | Approved stories | Main decisions and traceable details |
|---|---|---|
| E1 Private access and drafts | 1.1–1.4 (4) | Immediate private lock even with missing logout response; persistent pending revocation and fail-closed recovery; fixed AD-12 expiry; only a matching immutable-batch receipt establishes server confirmation. |
| E2 Prepare and revise a day | 2.1–2.12 (12) | Representative OCR/source investigations; Tide service date/extended hours versus calendar display time; explicit reviewed-revision confirmation; transient PDF/image originals, preserved corrections and partial coverage; combined-day split work/additions and scoped stale revision proposals. |
| E3 Actual trip and interaction | 3.1–3.15 (15) | Qualified separate position/speed, visible startup/five-minute exceptions, no network-only GPS fallback; independent passage/departure reference for 100 m; manual provenance, repeated-stop identity and visible gaps; distinct return start, uncertain physical outcomes, bus-change times, persistent manual theme and measured wake support. |

- Reviewed each story interactively and retained the owner's clarifications in its acceptance criteria and approval record. E3 coverage approval included focus/closure tests in 3.2 and meaningful announcement tests in 3.5.
- Recovered after a tool interruption by inspecting actual files: 3.5 approval was missing and 3.6 had not been saved. Recreated the agreed 3.6, registered both approvals once and verified canonical copies before continuing. This was a documentation repair, not tested application recovery.
- Closed E3 planning and paused before E4 at the owner's request. The owner requested commit/push for this checkpoint; Git outcomes are separate from approval and do not establish publication of subsequent work.

## 2026-09-26 – E4–E7 story planning

| Epic | Approved stories | Main decisions and traceable details |
|---|---|---|
| E4 Source-backed notices | 4.1–4.8 (8) | Actual source coverage versus metadata/fetch failure; evidence-based identity/version/closure and repeated-stop relevance; seen only after actual exact-version display; visible additional notices; acknowledgement changes only driver state; one eligible new-notice chime, no old-audio replay. |
| E5 Offline continuity | 5.1–5.13 (13) | Concrete active-day grant, coherent assets/reopen, independent Access/app/source/receipt states; explicit conflicts and planned/emergency transfer; preserved former-device work; retained-client compatibility; accepted update versus staging; terminal settlement/fences and all-copy expiry. **5.4 timing proof remains open.** |
| E6 Mentor roles and contexts | 6.1–6.10 (10) | Mentor confirms their copy, not the other person's confirmation; revision-specific links, separate A–B–A periods and activity contexts; immediate driver restrictions despite failed storage; manual takeover; active revision preserved; unknown actual role after recovery stays restricted. |
| E7 Closing and summary | 7.1–7.6 (6) | Explicit terminal ending and first-review completion, interrupted review continuation; honest summary and revision-bound local PDF; day-scoped retained access/expiry; factual varied greeting without permanent history. **7.1 unverified end time cannot extend the earliest binding deadline.** |

- The owner approved each story and the E4–E7 coverage summaries, retaining V1 and AD-1–AD-14. E8 was opened with a separate unapproved first draft; no operational gate was passed.
- Detailed clarification wording and test cases remain in [canonical epics and stories](../_bmad-output/planning-artifacts/epics.md) and [individual story files](../_bmad-output/planning-artifacts/story-drafts/).

## 2026-09-27 – E8 story planning and epic approval

| Stories | Approved responsibility |
|---|---|
| 8.1–8.2 | Isolated fictional PC demo, shared rules, independent failure scenarios and reset without old-run effects. |
| 8.3 | Actual client/FastAPI/PostgreSQL lifecycle evidence, separate from static demo and source/device qualification. |
| 8.4–8.5 | Portable protected runtime, Windows restart downtime, verified Access and provider handling before real files. |
| 8.6 | Assessable delivery/evidence/AI-reflection package and separate E8-D decision record. |
| 8.7–8.8 | Actual representative import/source and mounted Lenovo/Brave qualification; independent 100-m reference and honest measured/synthetic/untested distinctions. |
| 8.9–8.10 | Real-duration whole-day continuity, access/transfer/settlement/expiry, measured host downtime/resources/noise and a concrete old/new release preserving active/pending work. |
| 8.11 | Later dated owner E8-P decision requiring mandatory passes and resolved blockers, including 5.4/7.1. Story approval is not pilot permission. |
| 8.12 | Protocol agreed before first shift, three actual assigned days after positive E8-P, negative/interrupted days retained, planned/unobserved/measured behavior separated and independent E8-E outcome. |

- The owner approved all twelve E8 stories individually, then approved the coverage summary and closed E8 on the planning level. Totals: E1 4, E2 12, E3 15, E4 8, E5 13, E6 10, E7 6, E8 12 = **80 story plans across eight approved epics**.
- Coverage review found no missing E8 responsibility or need for a thirteenth story; declared dependencies exist and point backward. Controlled demo/fullstack, actual environment qualification and gate decisions retain different evidentiary roles. Early investigations are not deferred until E8.
- Dense qualification can require several observation sessions; the three-day trial is inherently multi-day. Story count is not a capacity estimate. No requirements or architecture choices were removed.

### Open risks and next step

- **OPEN — timing basis in [5.4](../_bmad-output/planning-artifacts/story-drafts/story-5.4.md) / [7.1](../_bmad-output/planning-artifacts/story-drafts/story-7.1.md):** a client timestamp alone cannot justify delayed server acceptance of offline activation after login expiry. An unverifiable end time cannot extend access/retention; enforce the earliest applicable limit. A separate solution decision plus necessary implementation/retest evidence is required before positive E8-P. Planning approval does not resolve this.
- Actual source/OCR coverage, mounted sensing/100-m/usability/Auto/wake/audio, full-day recovery, unknown-role restrictions, provider handling, host/noise and compatible releases remain unexecuted qualification obligations. Negative findings need explicit solutions, not silent scope reduction.
- Assessment dates/browser, evaluation protocol/scheduling, capacity and delivery time remain unresolved. Existing accepted limits (Windows sign-in before Docker, possible permanent loss without historical private backups) do not waive qualification.
- **Next substantive work: project step 6 / readiness control in a separate new chat.** Story creation, epic planning and internal step-5 final document validation are complete; readiness has not started or passed. E8-D, E8-P and E8-E are not execution approvals. Actual shifts still require the later positive dated E8-P decision.

### AI use, verification and log maintenance

OpenAI Codex used the BMAD Create Epics and Stories workflow to read actual planning documents, draft one story at a time, incorporate owner decisions and maintain traceability/coverage. The owner reviewed all 80 stories and epic boundaries; AI output did not substitute for approval or practical evidence.

At the owner's request on 2026-09-27, condensed repetitive story-by-story progress entries into the dated summaries above. The canonical story bodies, individual approval records and epic coverage/decision records remain in epics.md and all 80 story files. Earlier setup/Brief/PRD/UX/architecture log entries are preserved.

Document checks verified unique canonical story counts, saved approvals, dependency identifiers, resume state and whitespace. These are document checks, not application, sensor, source, database or pilot tests. No application implementation, actual qualification/field data collection, provisioning, deployment or BMAD Spec occurred in this planning stage. The condensation/approval update was initially saved locally; the subsequent authorized publication checkpoint is recorded below.

## 2026-09-27 – Step 5 closed; publication checkpoint

- At the owner's request, completed the internal epics/stories final document checks; [validation record](../_bmad-output/planning-artifacts/epics-final-validation.md) maps FR-1–25, UX/quality coverage, architecture, scope and dependency checks. All eight epics and 80 stories remain approved plans; no acceptance criteria were changed.
- The generic setup-only first-story instruction yields to the approved first vertical slice: 1.1 includes repeatable setup and private access. E1's equivalent scope headings are present; multi-session qualification is not falsely treated as a one-session coding promise. Adopted architecture and V1 scope are preserved.
- Checked canonical/individual acceptance text, counts, approvals, saved state, references and Git diff scope. Reviewed changed/new Markdown for accidental edits, credential/private-key/token patterns and operational identifiers; publication contains planning documents and the log, not application data or credentials. These are document checks, not executed product tests.
- The owner authorized committing and pushing these documents to the current branch. Publication outcome and commit hash are reported separately after Git verification; this record does not preclaim push success.
- Exact continuation: project step 6 in a separate chat using bmad-sprint-planning for readiness, with epics.md, the final-validation record, approved PRD/UX/Architecture Spine and this log. The completion hook is empty; no automatic next workflow was run. **5.4/7.1 remains OPEN.** No readiness, implementation, E8-D acceptance, actual pilot permission, provisioning or deployment occurred.
