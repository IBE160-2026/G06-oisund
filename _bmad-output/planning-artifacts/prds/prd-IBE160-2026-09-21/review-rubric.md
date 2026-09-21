# PRD Quality Review — Bus Driver Assistant

## Overall verdict

The PRD is ready for explicit product-owner review: its core, supporting commitments and exceptions are concrete, and its acceptance evidence distinguishes real operation from simulation. Technical feasibility and course scheduling remain honestly deferred rather than disguised as completed work. Two low-severity editorial issues could cause mistakes when downstream readers extract individual requirements; neither requires reopening a resolved product decision.

Review basis: the full quality rubric, [PRD](prd.md) and [addendum](addendum.md). This review does not approve the draft or establish source/device feasibility.

## Decision-readiness — strong

Sections 5 and 10 distinguish mandatory automatic disruption retrieval from optional meeting warnings, weather, speed limits and routing. FR-16 openly records the availability trade-off of startup access and five-minute outage unlocking rather than promising universal motion locking. FR-24 defines both deliberately ended and never-ended retention cases.

All A decisions are resolved. B items have downstream owners and validation expectations; C items identify external facts. Their deferral is appropriate for approving product intent and must not be mistaken for permission to pass operational acceptance without evidence.

## Substance over theater — strong

The journeys represent two actual use cases: operational assistance and repeatable instructor assessment. The document avoids invented market differentiation, general-purpose multi-user features and mandatory AI. Quality requirements are grounded in the actual tablet, phone tethering, source uncertainty and record lifecycle. Its promise is reduced searching while preserving independent operational practice, not novelty for its own sake.

## Strategic coherence — strong

The central argument in sections 2 and 5 connects shift context, actual progression and relevant automatically retrieved notices. Section 9 measures information effort and missed notices, while SM-C1/2 check distraction and false confidence. Required PDF export and isolated demonstration serve pilot evidence and course assessment. The optional-extension order is explicit and does not redefine the core around easy features.

## Done-ness clarity — adequate

FR-2/3 make import confirmation, ambiguous matches and missing stops observable. FR-8 supplies a distance bound; FR-14/16 give lifecycle and timer rules; FR-17/20 specify whole-shift offline recovery; FR-21–24 define completion, export and deletion outcomes. These support meaningful downstream acceptance scenarios.

Some thresholds and mechanisms intentionally remain with B-1–5, including source qualification, sensor confidence, visual criteria and evaluation procedure. These are implementation/pilot prerequisites, not new blockers to PRD approval. The two-minute retrieval target is correctly not a guarantee of incident-publication latency.

## Scope honesty — strong

Section 5 explicitly excludes native-app delivery, routing and replacement of existing operator workflows. FR-25 and section 9 prevent demo evidence from satisfying live retrieval or device tracking. Sections 2 and 10 do not assume the upper effort estimate is available. Missing metadata, manually indicated progression and imperfect source coverage remain visible throughout.

No unapproved technology stack or architecture is selected. The larger mandatory supporting scope remains ambitious, but B-5 requires effort assessment and explicit reconsideration rather than silent removal of accepted features.

## Downstream usability — adequate

The glossary distinguishes driver shift, vehicle duty, physical bus, trip and activity. FR, NFR and success-measure identifiers allow focused extraction. Current requirements and discovery history are separated, and source research is identified as documentation evidence rather than a verified integration.

### Findings

- **low — Movement exceptions need local references** (§6.2, FR-6/9/11; §6.4, FR-16). Phrases such as “At full standstill” and “standstill-only trip-selection controls” can be read as absolute if these requirements are extracted alone. FR-16 explicitly allows free startup access and delayed access during GPS loss. *Fix:* Add “subject to FR-16 startup/GPS-loss exceptions” to these local restrictions, and broaden the FR-16 title beyond “Message interaction” because its body governs other controls too. Preserve all approved behavior.
- **low — Historical status markers still sound current** (addendum, “End-of-Day Summary and Data Retention” and activity-transition markers). Some editorial markers say “remains product decision A-4,” “being consolidated under A-4,” or “remaining transition consistency is A-1” although the opening current-decision notes and PRD register resolve them. The addendum's global history disclaimer prevents a normative contradiction, but isolated extraction can still recreate closed questions. *Fix:* Mark those local status clauses explicitly as historical/resolved and point to FR-10/16/24; preserve the underlying decision history.

## Shape fit — adequate

The grouped capability structure fits a single-operator course prototype that feeds later UX and implementation. Two short journeys are useful because operational use and instructor demonstration have different data and device constraints. Detailed source and discovery material stays in the addendum. The resolved-decision register adds length, but earns its place by showing which choices are closed and which validations remain downstream.

## Mechanical notes

- FR-1 through FR-25 and NFR-1 through NFR-4 are contiguous and unique; UJ-1/2 and SM-1–5 plus SM-C1/2 are distinct.
- No inline assumption-tag index is required: unverified matters are explicitly placed in the B/C register rather than hidden as confirmed requirements.
- The operational journey uses an explicitly declared pseudonym; the instructor is a concrete assessment role. Inventing a personal identity for that role would add no useful requirement context.
- Norwegian interface labels within the English document preserve user-specified content and are not glossary conflicts.
- Status remains draft pending explicit approval. This review changes no requirement and does not finalize the PRD.

Finding totals: 0 critical, 0 high, 0 medium, 2 low.
