# Decision register

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Updated 2026-10-26 from the latest user instruction. Status below concerns planning only; no implemented behavior has been approved.

| ID | Authority / status | Decision and consequence |
|---|---|---|
| PP-D1 | User-set planning decision; closes Q1/A1 | First delivery uses manual relevant-occurrence selection after interruption. The selection can skip several stops; none becomes an observed passage. Automatic multi-stop reacquisition stays later. |
| PP-D2 | User-set planning decision; closes Q2/A2 boundary | Reuse the saved stop only within the same workday/shift identity, including across midnight. Calendar rollover neither resets nor extends retention. A different workday requires manual start even on the same calendar date. |
| PP-D3 | User clarification; reaffirms U3 | Manual anchor is advisory over time. Protect fresh selection, then allow ordinary GPS progression/reassessment on new coherent reliable evidence without approval at each stop. Age alone is insufficient. Explicit Pause/Off suppresses sensing until user action. |
| PP-D4 | User clarification; reaffirms U1/U4/U5 | Start at the relevant driven occurrence. Remap saved stop identity into the newly confirmed dated trip/range; do not copy old sequence or treat old evidence as fresh. Missing/ambiguous mapping requires manual clarification. NSR is the proposed coordinate authority; StopPlace and Quay stay distinct. |
| PP-T1 | Technical proposal retained from specification | One latest server-owned stop record per workday; transient bounded raw-fix buffer; no trail or private browser persistence. Online revisions/operations, bounded receipts and fixed parent expiry. |
| PP-T2 | Technical proposal | Consume the existing route extension's frozen reference, add a versioned NSR coordinate binding here, and expose route health separately from measurement health. Reuse the current stack and authority patterns; no duplicate route catalogue. |
| PP-T3 | Technical proposal | Ordinary following moves to a supported next occurrence; far/backward contradictions require re-anchoring. Protect new manual assertions and collect only subsequent coherent evidence. Turning support off clears sensing/estimate memory but retains the acknowledged bounded anchor until normal parent expiry/deletion. |
| PP-A3 | Untested assumption, not an accepted limit | Illustrative protection/freshness/accuracy/coherence/buffer values in behavior.md require device and route qualification. Failed qualification keeps the affected case manual; never weaken gates to manufacture a pass. |

U1–U5 from the earlier request remain load-bearing in [scope](../../scope.md). PP-D1/PP-D2 supersede “recommended / awaiting Q1/Q2” wording. Historical memlog and research entries remain append-only evidence of prior proposals.

The first implementation gate is completed/tested V1 plus the necessary route functionality, followed by separate implementation authorization. Device/origin/coordinate qualification is required before a supported pilot claim. No new user decision is needed to draft these stories. Any qualification failure that demands broader product scope must return as a new, concrete decision; automatic recovery, cross-workday reuse and background tracking are not defaults.
