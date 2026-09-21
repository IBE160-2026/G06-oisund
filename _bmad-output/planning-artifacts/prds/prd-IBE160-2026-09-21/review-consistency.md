# Final Behavioral Consistency Review

Review date: 2026-09-21. Scope: current [PRD](prd.md) and [addendum](addendum.md), checked against the resolved product decisions. This is a document consistency gate, not integration, device or operational safety validation.

**Verdict: no unresolved product contradictions found in the reviewed behaviors.** No critical or high findings and no new necessary product decisions. Two low-severity editorial findings remain; existing B validation and C external facts stay deferred.

## Behavioral checks

| Review issue | Result and references |
|---|---|
| Ten-second transitions | Consistent. FR-10 and FR-16 apply the ten-second indication to all listed non-return activities for GPS/manual arrival; the same-route return has its separate GPS/manual trigger. A-1 matches. A display change does not certify physical completion. |
| Missing stops and absent automatic candidates | Consistent. FR-3 first attempts supported timetable recovery, then retains details without fabricated stops or automatic progression and allows manual handling. FR-6 permits direct confirmed-shift selection if no candidate is found. FR-21 supplies undetected-depot completion. A-2 matches. |
| Entire-shift offline use | Consistent. FR-17/20 cover the entire fully loaded confirmed shift, available stop lists, later activities, corrections, summary and restart; no new source data is promised offline. A-3 matches. |
| All-data deletion | Consistent. FR-24 deletes all associated application records seven days after confirmed completion/abortion or, if never ended, planned end. Reopening/export does not reset the clock. User-held exports/notes remain outside application cleanup. A-4 and NFR-3 match. |
| GPS startup, recovery and timers | Consistent. FR-16 permits free startup access before the first valid measurement, distinguishes later signal loss, preserves approved exceptions, resets outage waiting on reliable recovery and cancels collapse on reliable speed at or below the threshold. FR-9 hides outage-only controls on reliable recovery. A-5 matches. These are explicit product choices, not new approval questions. |
| Notice lifecycle | Consistent. FR-13/14 distinguish missing timestamps, disappeared versus ended notices, manual removal, changed reappearance, persistent seen state and silent updates. FR-15 limits sound to new relevant notices during the ongoing trip. A-6 matches. |
| Access expiry | Consistent. FR-1 gives 14-day remembered access without expiry-only interruption of an active shift; renewed sign-in occurs between shifts. Explicit logout/revocation remain separate. FR-20 and A-7 do not contradict this. |

## Low-severity editorial findings

1. **Historical pending wording persists beside resolved summaries.** In the addendum's “Reading This Decision History,” the earlier disappeared-notice entry still says reappearance needs clarification, and the earlier retention entry says never-ended shifts/quality evidence need decisions. Later entries immediately resolve both. Further historical annotations refer to A-1, A-3 and A-4 as pending. The addendum explicitly declares the PRD normative, so these are editorial drift rather than active contradictions. Replace pending-language annotations with links to the resolved A entries or label them clearly as historical; do not ask these questions again.

2. **Local standstill shorthand could point more clearly to exceptions.** FR-6, FR-9 and FR-11 describe normal standstill-only controls, while FR-16 expressly overrides that restriction at startup and after the agreed outage interval. Reading the whole PRD yields a consistent policy. Adding “subject to FR-16 exceptions” to the local descriptions would prevent isolated excerpts from obscuring the approved behavior. This is a cross-reference fix, not a policy change.

## Gate boundaries

Source semantics, device accuracy, offline mechanism and other B items require downstream evidence but are not newly reopened product decisions. Exact course dates and assessment details remain C facts. The document remains draft pending the user's explicit final approval; this review does not authorize finalization or publication.
