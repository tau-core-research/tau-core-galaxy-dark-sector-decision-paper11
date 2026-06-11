# Frontier Provenance Source Candidate Ledger v45

**Doc class:** frontier provenance source-candidate ledger  
**Status:** source candidates ready for human review; not evidence; no promotion; no endpoint scoring allowed  

Script:

```text
scripts/build_frontier_provenance_source_candidate_ledger.py
```

Derived outputs:

```text
data/derived/frontier_provenance_source_candidate_ledger_v45.csv
data/derived/frontier_provenance_source_candidate_coverage_v45.csv
data/derived/frontier_provenance_source_candidate_ledger_summary_v45.csv
```

This layer applies the v44 intake contract to concrete public SPARC source
candidates. It records the official SPARC landing page, candidate table files,
source hashes observed during local source-candidate audit, and row-selection
rules for the eighteen frozen galaxies.

## Current Result

The expected status is:

```text
FRONTIER_PROVENANCE_SOURCE_CANDIDATES_READY_NOT_EVIDENCE
```

The ledger records two SPARC source candidates and identifies candidate source
rows for all eighteen frozen galaxies. It creates zero v21 evidence rows and
does not allow promotion by itself.

## Claim Boundary

This ledger is not `data/input/source_import_provenance_evidence_v21.csv`, not
source import, not endpoint scoring, and not a dark-sector verdict. It only
records review candidates that can later be used to fill the v21 evidence input
after human review.
