# Frontier External Hash Recompute Audit v50

**Doc class:** external source hash recomputation audit  
**Status:** hash recomputed and matched; no evidence written; no scoring allowed  

Script:

```text
scripts/run_frontier_external_hash_recompute_audit.py
```

Inputs:

```text
data/derived/frontier_provenance_source_candidate_ledger_v45.csv
data/external/sparc_hash_audit_v50/SPARC_Lelli2016c.mrt
data/external/sparc_hash_audit_v50/MassModels_Lelli2016c.mrt
```

Derived outputs:

```text
data/derived/frontier_external_hash_recompute_audit_v50.csv
data/derived/frontier_external_hash_recompute_audit_summary_v50.csv
```

This layer closes the v48/v49 hash caveat by computing SHA-256 hashes from the
cached external SPARC source files and comparing them with the v45 source
candidate ledger.

## Current Result

The expected status is:

```text
FRONTIER_EXTERNAL_HASH_RECOMPUTED_MATCHED
```

Both SPARC source candidate hashes match the v45 ledger:

- `SPARC_Lelli2016c.mrt`
- `MassModels_Lelli2016c.mrt`

The primary Table1 source used for the eighteen frontier provenance rows is
therefore hash-matched after external recomputation.

## Claim Boundary

This audit is not active v21 provenance evidence, not observed scoring input,
and not a dark-sector verdict. Hash agreement alone cannot authorize v21 copy
or endpoint scoring.
