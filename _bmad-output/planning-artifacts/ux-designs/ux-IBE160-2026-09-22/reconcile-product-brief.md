# Product-brief reconciliation

Compared `product-brief.md` with DESIGN.md, EXPERIENCE.md, `.working/source-extract.md` and the latest `.memlog.md` decisions. The brief supplies background; the PRD and subsequent explicit user decisions govern. This is input reconciliation, not a reviewer gate or implementation validation.

## Retained qualitative needs

- **Purpose and users / Problem and evidence:** A mounted-tablet view brings the actual day's work together, reduces searching during breaks and supports a Tromsø pilot without making those routes permanent boundaries. EXPERIENCE Foundation preserves route/direction distinctions and actual operational context.
- **First-version scope:** Preparation retains reviewed shift import, manual physical-bus assignment, trips and non-passenger activities. Driving retains glanceable orientation, actual-progress transitions and permitted manual correction. Planned notices remain source-backed and relevant to the shift/trip. Separate instructor simulation complements actual use.
- **Trust and failure behavior:** Uncertainty preserves last-confirmed context; retained notices do not become fresh after outages. Source update and retrieval times stay distinct. Optional speed information cannot imply verified road identification. DESIGN's information hierarchy and EXPERIENCE's failure states directly carry these needs.
- **Value and success criteria / Feasibility and broader vision:** Reduced checking effort, missed-notice prevention and honest separation of demonstration from actual-device evidence remain the rationale. Quantitative evaluation, schedule and capacity belong to the governing requirements/evaluation plan, rather than duplicated interface specifications.

## Intentionally superseded aspects

- **First-version scope:** PDF-only preparation is expanded by explicit user decision to PDF plus JPG/PNG, with shared review. Later decisions additionally cover split days and reviewed full/partial shift revisions or manual overtime.
- **First-version scope / Feasibility and broader vision:** Speed information is optional after the core under the PRD; the older first-version emphasis and warning at 100 metres or less are superseded by optional support and the later approximately 300-metre preference. This does not change the separate stop-progression distance.
- **First-version scope:** Next-stop emphasis becomes current-stop dominance at a stop and next-stop dominance between stops, in the accepted vertical sequence.
- **Purpose and users:** The operational pilot uses the PRD's privacy-preserving pseudonym Alex.

## Genuinely dropped ideas

No unexplained loss of a qualitative core need was found. **Feasibility and broader vision** mentions AI relevance prioritization and short-alert generation; these are not carried as UX capabilities because the governing source expressly has no in-product AI requirement. Meeting buses and weather remain optional, not discarded.
