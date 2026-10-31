# Human and AI process reflection

*Prepared with AI assistance from Jonas’s account of his decisions and experiences, and reviewed and approved by Jonas. This document supports the repository’s process documentation; the separate Norwegian course reflection report has its own structure and requirements.*

## Responsibilities and working method

Jonas proposed the project and its practical use case, drawing on his experience as a bus driver. He described the desired structure and behaviour, supplied source documents and his interpretation of them, and contributed requirements. Throughout development, he made decisions about requirements and corrections and gave acceptance after testing and reviewing documentation.

AI assisted with analysis, specifications, architecture, implementation, automated tests, documentation and review. Jonas’s independent assessment primarily concerned whether the application met the practical need and worked as expected. He relied on AI for programming and technical diagnosis and does not claim to have independently verified the code’s quality.

The application was developed with AI assistance but does not use AI at runtime. PDF import uses `pdfplumber` and programmed interpretation rules; documents are not sent to a language model as part of that import flow.

## Scope and priorities

The original idea included a driving view with stops, speed limits and notices linked to GPS position. During planning, the project grew to eight epics and 80 stories. Jonas did not recognise the excessive scope at the time and considers that he gave AI more freedom to expand it than he should have.

Following teacher feedback, the project was reduced to four epics and 20 stories. Jonas’s deciding consideration was to retain enough complexity to support his ambition for a good course grade while making completion realistic within his limited available working hours.

The most difficult feature to postpone was the position-based driving view. Much of that functionality now has separate planning documents for possible extensions after full V1 approval. These plans do not establish implemented functionality.

The delivered core focuses on importing supported text PDFs, reviewing and correcting extracted information, explicitly saving and confirming a plan, manually selecting activities and recording status, and consulting manually maintained notices. The completed Ubuntu server integration is included in V1 and has its own evidence and operational limits.

PostgreSQL provides persistent storage for accounts, sessions, drafts, confirmed shifts, progress and notices. It runs in a separate Docker container on the Ubuntu server. The database is central to the application’s handling of ownership, saved state and data retention.

One concrete lesson has already influenced Jonas’s approach elsewhere: in another project started to explore an idea, he has imposed clearer limits on AI’s freedom to expand the scope.

## Testing and practical acceptance

The project demonstrated that passing automated tests does not establish that the application will work satisfactorily in its intended environment.

During the first external Android trial, file upload failed despite the preceding tests having passed. For Jonas, this made testing on the actual target device a concrete requirement rather than an optional final check. Automated tests remained useful, but their results had to be considered alongside the conditions they actually exercised.

Story 12.4 exposed a different limitation. The tested functions appeared to work, but Jonas found the preparation flow repetitive and frustrating. Correct imports still led through editing, and the activities had to be scrolled through repeatedly before confirmation.

He withheld acceptance and identified the sources of friction. The subsequent changes made editing optional, separated review and confirmation into distinct pages, and allowed the review to be reopened when needed instead of forcing it into the confirmation path. Saving the physical bus from the upload page also removed an unnecessary visit to the editor.

These changes substantially improved his experience. A correct import could be reviewed once and taken to confirmation. Editing a whole day still involves considerable scrolling, but Jonas accepted this as an occasional exception rather than part of every successful import.

Jonas had noticed the awkward workflow earlier, but let it pass because he expected a later stage in the process to provide a natural opportunity for improvement. By Story 12.4, all tests had passed without him having found what felt like the right point to address it. He therefore paused the acceptance process and requested the changes. In hindsight, the lesson was to raise observed usability problems explicitly when they appeared, rather than assume that a suitable improvement stage would follow.

The lesson was that human acceptance requires its own assessment. Automated checks can establish specific behaviour, while practical use reveals whether that behaviour forms a satisfactory workflow.

## Evidence and uncertainty

The repository records source versions, test environments, failures, corrections and acceptance decisions. Parser checks against independently prepared expected facts, actual API/database tests, browser automation and personal device observations provide different kinds of evidence. Their counts overlap and should not be combined into a single coverage score.

AI also required correction in its test guidance and tooling. Such incidents reinforce the need to inspect what actually ran and what was observed rather than treating an agent’s statement that a test is ready or successful as sufficient evidence.

The project does not establish measured time savings, improved driving safety, complete accessibility compliance or comprehensive security assurance.

## Practical use and privacy

The current assistant provides an overview of a preplanned shift composed of multiple activities and brings it together with registered notices for the relevant lines. Similar use by tram drivers etc. may be possible, but has not been evaluated.

Users must check imported details before confirming a plan. Notices currently require manual maintenance, so users cannot assume that the information is current or complete. Planned times do not establish actual progress, and a manually recorded status does not independently prove that work took place.

Checking a notice against its source, ending it and deleting it are separate actions. Ended or expired notices leave the relevant-notice view but remain available as read-only history for a bounded period, normally up to seven days after their effective ending. An earlier deletion deadline is not extended. After the retention deadline, access is refused and the record is removed by scheduled cleanup. This concerns the active application database; it does not establish that all copies have disappeared from backups.

The application limits what it retains from uploaded documents. The original PDF is processed temporarily rather than archived, and the driver header field is filtered out before persistence. Explicit saving retains interpreted shift details, source references and corrections.

Saved shifts nevertheless remain linked to a user account and are not anonymous. Account separation and access tests address unauthorised access through the application; they do not protect against someone who gains sufficient control of the database or server. There is also no general anonymisation guarantee for personal information entered into other text fields.

## Main learning

For Jonas, AI made it possible to develop an application he could not have implemented independently with his current programming knowledge. It also required more active planning, limitation and follow-up than he initially expected.

His strongest lessons are to constrain the first version earlier, test on the intended devices, and address observed usability problems explicitly rather than assume they will be resolved at a later stage. His professional knowledge helped him identify practical needs and unsuitable workflows, while technical implementation and diagnosis continued to depend heavily on AI.

The resulting application therefore demonstrates both the opportunity provided by AI-assisted development and the continuing need for human direction, documented verification and explicit acknowledgement of the limits of that verification.

## Documentation references and approval record

Jonas supplied the approved English text through the local reflection handover and explicitly requested its incorporation on 31 October 2026. The reflection body above is reproduced unchanged. Its canonical repository filename remains `docs/submission/ai-reflection.md`, as linked by the README and AC-12 traceability; the handover filename is not the delivery document name. The separate Norwegian course reflection report has not been changed or approved by this repository update.

- [Scope reduction and original eight-epic inventory](../../_bmad-output/planning-artifacts/sprint-change-proposal-2026-10-19.md); [four-epic, twenty-story backlog](../../_bmad-output/planning-artifacts/epics.md).
- [Actual Android upload failure and correction](../evidence/mobile-pdf-upload.md).
- [12.4 workflow correction](../evidence/12-4-import-experience.md) and [owner acceptance](../evidence/12-4-owner-acceptance-2026-10-28.md).
- [D1–D3 actual tests and personal assessment](../evidence/v1-acceptance-2026-10-29.md), [main integration](../evidence/v1-main-integration-20261029.md) and [requirement/test traceability](traceability.md).
- [Retained-data behaviour](../evidence/12-1-retained-data.md), [PDF interpretation](../../backend/app/pdf_import.py) and [private import header filtering](../../backend/app/private_import.py).
- [Included Ubuntu scope, deployed/source identities and operational evidence](v1-scope-and-operations.md); [operations guide](../ubuntu-server.md).
- [Remaining delivery work and open O3–O6](delivery-readiness.md). Reflection approval closes repository-text review only; it does not qualify missing controls, settle the course rubric or authorize tagging/submission.
- [Historical 12.5 reflection](ai-reflection-12-5.md) and [superseded proposal](ai-reflection-proposal.md).
