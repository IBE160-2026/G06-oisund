---
title: 'Collect bounded NVDB evidence for a dated road corridor'
type: 'feature'
created: '2026-11-20'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem**. SL-E1-S1 requires bounded, auditable road-source acquisition. The historical attempts were one-off research and do not provide a repeatable collector that preserves a completed result if acquisition fails.

**Approach**. Add an explicit local command for a dated, named public NVDB scope. Check complete, stable pagination and row identities under the SL-LAB-1 request, retry, byte and record budgets. Write raw pages and a versioned receipt in one atomic evidence archive. Road, route, lane and physical qualification remain separate requirements for any runtime package.

</frozen-after-approval>

## Implementation Notes

Use the paged V4 network and object series from the retained 20 November probe. The observed fields are `antall`, `returnert`, `objekter` and `neste.start`. Empty pages can repeat a cursor after the full declared count has been read. Rebuild the fixed query with only the cursor. The upstream `href` omits the versioned API path. Validate the segment reference and selected link ID. For objects, validate type, version, unique identity, and at least one scoped direct or turn placement. Other placements of the same object remain in the raw page identified by the receipt. The command accepts public municipality and sequence IDs, uses Python's standard library, and writes an explicit ZIP path. It is separate from the existing `road_reference_api` loader and introduces no new dependency or service permission.

All 34 collector tests passed with the network disabled. The offline replay checked 16 originals in `tmp/road-qualification-20261120` using the matching JSONL ledger. The local `tmp/nvdb-collector-verification/verify-replay.py` reproduces the replay and validates page digests and scoped counts. In the temporary Linux API image, set the workdir and `PYTHONPATH` to the mounted `backend` directory. Mount the replay working directory at `/out`, invoke `python /out/verify-replay.py`, and use `--network none`. `verify-bundles.py` in the same directory checks both ZIPs and compares the decoded pages and their continuation URLs. The live command, time, archive hash and surviving operational gates are recorded with the source evidence. All 18 deterministic frontend motion controls passed. [Collector command](../../backend/app/road_data/README.md#local-source-refresh) · [Live comparison](../../docs/evidence/v2-road-source-20261120.md#repeatable-bounded-nvdb-collection).

## Review Triage Log

- Medium, patched. An empty terminal page accepts an absent cursor, the exact request cursor on a subsequent page, or `0:0` on the first page. Tests reject malformed cursors and unexpected continuation after a complete empty page.
- Medium, patched. Segment identity must bind the selected sequence, link number and segment number to the declared reference. A mismatched reference has a negative control.
- Medium, patched. The parser rejects duplicate members and non-JSON numeric constants. Both fail without installing an archive.
- Medium, patched. Body failures have an explicit incomplete diagnosis. Only transient opening failures are retried, since a failed body read may already have consumed bytes. A test verifies the previous archive survives a body timeout and no uncounted retry occurs.
- Medium, patched. The Linux operator command applies an overall 240-second acquisition deadline. The portable socket timeout remains 12 seconds. Cancellation and timer restoration passed an offline test.
- Low, patched. Missing network sequences are included in the receipt and the terminal output.
- Low, patched. The retained inputs, replay procedure, hash comparison and live command are documented above.
- Low, patched. Additional placements of scoped objects are located in the original page, with a page pointer in the receipt.
