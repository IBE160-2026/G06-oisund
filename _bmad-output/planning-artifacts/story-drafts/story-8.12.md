---
status: approved
created: 2026-09-27
epic: E8
story: '8.12'
type: field-evaluation
approved: true
approvedOn: 2026-09-27
dependencies: ['8.11', '7.3', '7.4']
---

### Story 8.12: Evaluate Three Actual Working Days and Record the E8-E Outcome

As the pilot owner,
I want a bounded evaluation of the assistant on three actual assigned working days, including effort, missed information, progression, distraction and trust,
So that its observed usefulness and shortcomings are documented honestly, separately from a demonstrable delivery and pre-pilot qualification.

**Acceptance Criteria:**

**Given** the intended release/equipment and the recorded E8-P decision,
**When** actual-shift evaluation is prepared,
**Then** require a later dated affirmative owner decision under 8.11, backed by passed mandatory gates and resolved blockers including the 5.4/7.1 timing basis with required implementation/retest evidence; approval of this or earlier story plans cannot authorize the shifts,
**And** check that the evaluated build/configuration and equipment remain covered by that decision. A material change or new invalidating finding requires affected requalification and an updated decision before renewed operational reliance,
**And** planning the protocol may proceed while E8-P is pending, but no actual-shift trial is executed or counted as authorized evaluation to supply missing pre-pilot evidence,
**And** use three actual assigned working days rather than fabricated/repeated demo days. They need not be identical, consecutive or cover all four pilot lines; record the actual variation without selecting only successful cases,
**And** do not infer dates, remaining hours or a delivery commitment from this three-day plan. Scheduling is agreed later with the owner and actual assignments.

**Given** the adopted PRD SM-1–4 and SM-C1/C2 measures,
**When** the owner agrees the observation protocol before the first evaluation day,
**Then** define the timing method, categories of checking effort, notice reference/comparison method, independent progression observation method and uncertainty handling, plus the already qualified quality limits used to classify reliable positioning,
**And** include assistant use, original-source verification and continued searching elsewhere in total checking effort, identifying preparation/checking versus evaluation-only note-taking and recording uncertainty rather than hiding time outside the app,
**And** retain the approximate 10–15 minutes daily target and the recalled 20–30 minutes per eight-hour day baseline with their limitations. Record actual workday length and context; any normalized comparison must show its method and cannot become a measured baseline or controlled time-saving claim,
**And** agree any remaining observation detail or numerical criterion before using it for judgement; do not invent new success thresholds or relax existing ones after seeing results. Changes during the trial are dated with their effect on comparability,
**And** arrange independent passage/departure references without driver input while moving; observer or unattended methods must respect AD-12. If a reference cannot be obtained, mark that field measure unmeasured rather than use the app's own detection as ground truth,
**And** use brief external notes at a safe permitted time and optional user-initiated private PDF exports. Observation must not require moving-driver taps, source browsing or deliberately induced operational failures; controlled fault evidence stays in earlier qualification reports.

**Given** each authorized assigned working day,
**When** the assistant is used and the day is reviewed,
**Then** record actual use duration, relevant working conditions and activities, usable/unavailable features, checking-time observations and their measurement uncertainty using a pseudonymous day reference for shareable reporting,
**And** record what worked, missing information, failures, manual interventions, interrupted use and reason, alongside successful operation. Do not count scheduled activities as performed or infer physical actions from display transitions,
**And** capture actual corrected import/driver confirmation, automatic source retrieval, recovery when it actually occurs and summary/PDF outcome for SM-4; an unencountered recovery event remains unobserved in the field, linked separately to prior qualification evidence,
**And** distinguish source and sensor observations, manually reported facts, local saved state and server confirmation. A PDF or notes cannot turn a pending receipt, uncertain activity or observation gap into verified completion,
**And** note changes of build/device/configuration and interruptions, retaining the applicable permission basis. No update, export or evaluation entry extends app access or data retention.

**Given** source evidence relevant to the actually driven trips and times,
**When** planned-notice outcomes are assessed for SM-2 and trust,
**Then** compare received/displayed notices with independently checked original-source evidence, documenting applicability, source availability, observation/publication/update/fetch times where known and missed, irrelevant or uncertain notices,
**And** distinguish a notice unavailable from the source during the relevant period from an app retrieval/relevance/display failure, and retain unknowns where historic source state cannot be established; a later webpage cannot automatically prove what existed earlier,
**And** a day with no applicable notice provides no positive coverage evidence. Report the evaluated sample and missing categories rather than generalizing to all lines or promising acute-event coverage,
**And** record false freshness, hidden outages and source-checking effort alongside successful delivery. A displayed/seen/registered notice is not proof of comprehension, and later receipt does not retroactively count as timely display,
**And** preserve notice/source references in sanitized evidence without publishing private shift associations or exact operational identifiers.

**Given** independently observed passage/departure events during actual use and the qualified sensing basis,
**When** SM-3 progression is evaluated,
**Then** compare the actual event with the displayed progression change using distance travelled afterward, including passage without stopping and close-stop cases where encountered; report reference method, sample size and uncertainty against the at-most-100-m target,
**And** record delayed, wrong or missed progression, manual corrections and unreliable-position periods separately. Do not drop failures from the denominator or treat a proximity radius as passage evidence,
**And** a later-stop reacquisition preserves the observation gap and does not certify the unobserved passages. Repeated-stop occurrence, manual correction and actual trip identity remain distinct,
**And** if no sufficiently independent/precise reference exists for a case, leave the field result inconclusive; prior 8.8 qualification can be cited separately but cannot be relabelled as that day's observation,
**And** do not claim the 100-m goal met when measured deviations show otherwise; negative findings return to the existing solution/qualification decision process.

**Given** time/coverage/progression results and the driver's observations,
**When** distraction and trust counter-metrics are compiled,
**Then** record unnecessary/missed/repeated chimes, confusing transitions, manual interventions and pressure to interact while driving, explicitly acknowledging the adopted startup, outage, direct-stop and theme exceptions,
**And** record irrelevant notices, false freshness, hidden outages, wrong progression and falsely completed activities alongside missed information; lower checking time cannot hide these costs,
**And** distinguish observed events, the driver's subjective experience and missing observations; no driver score, medical inference or unsupported causal safety claim is introduced,
**And** if a new finding invalidates required capability or safe reliance, record interruption/non-reliance and return it for the affected E8-P decision rather than continuing just to reach three days. Do not troubleshoot or stage failures while driving,
**And** retain partial/aborted days and negative outcomes in the report. Do not silently replace or exclude them; any additional/replacement day and its counting rationale require an explicit owner decision without rewriting the original evidence.

**Given** private summaries, optional exported PDFs and external notes support analysis,
**When** the evaluation report is produced,
**Then** preserve the existing distinction between private user-held evidence and material prepared for repository/course sharing; anonymize exact shift, bus, vehicle-duty, trip and person identifiers and avoid reconstructable private day associations,
**And** use external notes and only voluntarily exported PDFs; missing export or browser download uncertainty remains an evidence gap, not permission to reconstruct or retain prohibited data,
**And** app data, originals, pending work, grants and all other copies still expire under AD-6/12. Three-day evaluation creates no archive exception, new telemetry database or reason to delay cleanup,
**And** discard temporary raw positioning after the necessary analysis and retain sanitized distance/timing/error summaries. A shareable evidence summary is not a permanent anonymized operational quality dataset,
**And** explain that user-held PDFs/external notes are outside automatic app deletion; do not publish or delete those external originals automatically as part of this story.

**Given** the actual three-day evidence and its limitations,
**When** the owner reviews E8-E,
**Then** present day-by-day and combined outcomes for SM-1–4 and SM-C1/C2, separating planned behavior/tests, actually measured behavior and observed achievement, missed targets, inconclusive/unobserved cases and separately cited controlled qualification/demo results,
**And** discuss varying assignments/conditions, small sample and recalled baseline; no claim of controlled causal improvement, universal coverage, certified traffic safety or permanent production readiness follows from three days,
**And** record a dated owner-reviewed E8-E outcome, evidence/protocol versions and follow-up decisions. Completed evaluation is distinct from every product target being achieved: an honest negative result can complete the agreed evaluation,
**And** fewer than three actual evaluation days or missing agreed observations remain explicitly incomplete unless an owner-approved protocol change is separately recorded; do not declare the original three-day plan fulfilled or fabricate results,
**And** keep E8-D assessment/demonstration and E8-P permission as separate records. Completing E8-E neither retroactively authorizes unqualified use nor closes unrelated V1 defects, timing questions or course-assessment requirements by implication,
**And** carry material gaps into explicit solution decisions without silently changing scope or architecture. No new actual-shift evaluation or broader rollout is authorized by the report itself.

**Traceability:** E8-E agreed three-workday field evaluation; PRD section 9 SM-1–4, SM-C1/C2 and Product Brief/addendum evaluation agreement. Operational evidence FR-2–5/7–9/12–24, NFR-1–4 and UX provenance/uncertainty/movement/summary rules; FR-25/SM-5 remain E8-D. AD-6/9/10/12 govern transient originals, independent movement evidence, permission/access and no retained private archive; all AD-1–AD-14 remain unchanged. Earlier brief speed-limit references do not add a deferred feature to this V1 evaluation.

**Dependencies:** A later actual affirmative 8.11 E8-P decision for the evaluated candidate, existing E7 summary/PDF behavior and external owner notes, and an owner-agreed observation protocol/actual assignments. Story-plan approval of 8.11 is insufficient. No later story or new app feature is required; unavailable permission or evaluation opportunities block field execution and leave its outcomes unclaimed.

**Size boundary:** One agreed bounded three-day protocol, collection using existing outputs/external notes, sanitized analysis and an E8-E decision. The three-day observation duration is inherent, not a one-session implementation estimate. No new instrumentation platform, permanent history, extra product feature, controlled causal study or automatic publication. Defect repair and any extra evaluation days are explicit separate work, not hidden inside a successful-result requirement.

**Qualification boundary:** This is only an approved story plan. No actual shifts are authorized, scheduled or evaluated now; no protocol execution, data collection, implementation, deployment, readiness or workflow final validation is started. E8-D/P/E remain separate pending checkpoints.

**Approval:** Approved by the owner on 2026-09-27 as a story plan only: agree the three-day protocol before the first shift, include negative/interrupted days, and distinguish planned, unobserved and actually measured behavior. Actual shifts still require a later positive dated E8-P owner decision. The approved copy in epics.md is canonical; E8 coverage approval remains a separate checkpoint.
