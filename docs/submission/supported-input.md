# Supported input and interpretation

Use [Testskift-A.pdf](../../Eksempelfiler/Testskift-A.pdf), [B](../../Eksempelfiler/Testskift-B.pdf), [C](../../Eksempelfiler/Testskift-C.pdf), [D](../../Eksempelfiler/Testskift-D.pdf) and [E](../../Eksempelfiler/Testskift-E.pdf). These are completely synthetic documents. Their independent [JSON oracle](../../Eksempelfiler/Fasit-testskift.json) was authored separately from parser output. The reproducible demonstration does not need the older anonymized owner examples.

The bounded adapter in [pdf_import.py](../../backend/app/pdf_import.py) accepts the implemented two-column selectable-text shift layout, including its header, movement rows, places/clocks, known breaks and raw codes. The envelope is at most 10 MiB, 20 pages and 2 MiB extracted subprocess output, with a bounded parser process. This is not OCR and does not promise arbitrary operator layouts, screenshots, encrypted files or arbitrary tables. Invalid/unsupported input produces a visible error and a manual-draft route.

Import is transient. Choosing a PDF does not save its bytes, a draft or a confirmed plan. Saving persists structured facts and original-source metadata after an explicit action. Corrections retain the original extracted facts for comparison. Confirmation uses the reviewed saved revision; it does not approve unseen later edits. PDF extraction success does not certify operational correctness.

| Fact | Interpretation |
|---|---|
| Service date versus calendar date | Preserved separately, including overnight activity instants in Europe/Oslo |
| Unknown direction/place/clock/type | Remains unknown/raw; explicit classification/acknowledgement is required where the contract requires it |
| Vehicle duty | Source/entered duty; final three numeric digits derive the realtime duty when applicable |
| Physical bus | Separately entered value; never inferred from vehicle duty |
| Planned clocks | Schedule facts, never evidence of actual arrival, completion or current location |
| Notices | Manually entered, source-linked information; last source check differs from source update and validity |
| Manual activity status | User's explicit saved choice; no GPS or automatic advance |

Oslo local-time entry rejects spring gaps and requires an explicit occurrence for repeated autumn clocks. Source clocks beyond 24:00 are preserved with resolved calendar dates. The independent synthetic oracle plus parser/integration/UI checks give bounded facts, not a claim about all PDFs. [Current evidence](../evidence/12-5-reproduction.md) and [historical 12.4 extraction/flow evidence](../evidence/12-4-handoff.md) retain their separate revisions and limits.
