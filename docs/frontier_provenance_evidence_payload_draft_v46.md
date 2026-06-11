# Frontier Provenance Evidence Payload Draft v46

**Doc class:** frontier provenance evidence payload draft  
**Status:** draft ready; human review required; no v21 write; no endpoint scoring allowed  

Script:

```text
scripts/build_frontier_provenance_evidence_payload_draft.py
```

Derived outputs:

```text
data/derived/frontier_provenance_evidence_payload_draft_v46.csv
data/derived/frontier_provenance_evidence_payload_draft_review_v46.csv
data/derived/frontier_provenance_evidence_payload_draft_summary_v46.csv
```

This layer converts the v45 source-candidate coverage into a reviewable draft
with the same columns as `data/input/source_import_provenance_evidence_v21.csv`.
The draft remains under `data/derived` and every row is marked
`REVIEW_REQUIRED_NOT_COMPLETE`.

## Current Result

The expected status is:

```text
FRONTIER_EVIDENCE_PAYLOAD_DRAFT_READY_REVIEW_REQUIRED
```

The draft contains eighteen rows, but zero rows are marked
`PROVENANCE_EVIDENCE_COMPLETE`. It creates no v21 evidence input file and does
not allow promotion or scoring.

## Claim Boundary

This draft is not the v21 evidence input, not source import, not endpoint
scoring, and not a dark-sector verdict. It only prepares a reviewable payload
that may later be copied into v21 after source-row and leakage-evidence review.
