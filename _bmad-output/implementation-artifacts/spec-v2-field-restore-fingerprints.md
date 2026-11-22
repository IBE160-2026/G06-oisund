---
title: 'Bound memory for field-catalogue restore verification'
type: 'bugfix'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent">

## Intent

**Problem:** PostgreSQL restored the full V2 field catalogue, then Docker killed the isolated verifier at its 512 MiB limit while it aggregated complete row JSON for a table fingerprint.

**Approach:** Compare complete rows via ordered fixed-size row digests so verification can keep the existing container limit and output shape. Rehearse before/after equality and full-catalogue restore with PostgreSQL 17.11 before publishing the operations-only fix.

</frozen-after-approval>

## Implementation Notes

- Hash each complete row with SHA-256 before ordering. Keep the existing table name, row count, and 32-character digest output. Journal entries record which algorithm was used. A journal without the version field uses the original algorithm when resuming.
- PostgreSQL 17.11 restored a 35,174,959-byte archive with 231 line/date rows and 36 road packages under the existing 512 MiB limit. All 40 table fingerprints matched. The test also checked insertion-order independence and rejected a same-count mutation in a fixture with duplicates, a null, and Unicode. The original fingerprint was killed by Docker's memory limiter for the same catalogue after restore.
- All 65 Ubuntu operations tests passed in network-isolated Linux, including the new journal version check. The host Windows interpreter lacks the POSIX modules these tests use.

## Review Triage Log

- Medium, patched. An old helper can create a journal before the new helper resumes it. New journals store the algorithm version. Older journals keep the original comparison, and the resume test verifies both versions.
- Low, accepted within scope. Aggregation uses 32 bytes per row, with 231 records in the largest public route table and 36 road records in the full restore test. The verification limit was exercised without changing it.
- Medium, documented. Manual comparisons across versions need fresh captures on both sides from the same helper version. The deployment check captures both sides with the new helper.
- Patched. The synthetic PostgreSQL test verifies row order and same-count changes, and the full archive test compares all 40 tables.
