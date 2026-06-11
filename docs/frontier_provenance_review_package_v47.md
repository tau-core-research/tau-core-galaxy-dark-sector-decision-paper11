# Frontier Provenance Review Package v47

**Doc class:** reviewer handoff package  
**Status:** review package built; not evidence; no v21 write; no endpoint scoring allowed  

Script:

```text
scripts/build_frontier_provenance_review_package.py
```

Package outputs:

```text
review_packages/frontier_provenance_v46_review_package/
review_packages/frontier_provenance_v46_review_package.zip
```

This layer packages the v44 intake contract, v45 source-candidate ledger, and
v46 review-required payload draft into a reviewer handoff bundle. It is intended
to make the next human review step concrete without writing the active v21
evidence input.

## Current Result

The package contains:

```text
README.md
DO_NOT_COPY_WITHOUT_REVIEW.md
REVIEW_MANIFEST.csv
data/frontier_provenance_evidence_intake_contract_v44.csv
data/frontier_provenance_evidence_intake_checklist_v44.csv
data/frontier_provenance_source_candidate_ledger_v45.csv
data/frontier_provenance_source_candidate_coverage_v45.csv
data/frontier_provenance_evidence_payload_draft_v46.csv
data/frontier_provenance_evidence_payload_draft_review_v46.csv
data/frontier_provenance_evidence_payload_draft_summary_v46.csv
templates/source_import_provenance_evidence_v21_TEMPLATE.csv
```

## Claim Boundary

This package is not `data/input/source_import_provenance_evidence_v21.csv`, not
source import, not endpoint scoring, and not a dark-sector verdict. It only
hands reviewers the files needed to decide whether a later gate may promote the
draft into active v21 evidence.
