# Source Import Provenance Promotion Gate v23

**Doc class:** provenance promotion gate  
**Status:** promotion blocked; no manifest mutation; no scoring allowed  

Script:

```text
scripts/run_source_import_provenance_promotion_gate.py
```

Inputs:

```text
data/derived/source_import_provenance_manifest_v19.csv
data/derived/source_import_provenance_evidence_gate_v22.csv
```

Derived outputs:

```text
data/derived/source_import_provenance_promotion_gate_v23.csv
data/derived/source_import_provenance_promotion_summary_v23.csv
```

This layer turns the v22 evidence-gate decision into an explicit promotion
decision for every candidate row. It does not edit the v19 provenance manifest.
It only states whether promotion would be allowed.

## Current Result

The expected status is:

```text
PROVENANCE_PROMOTION_BLOCKED
```

The v22 evidence gate does not allow provenance promotion, so all eighteen
candidate rows are blocked, zero provenance rows are promoted, raw import
remains disallowed, and endpoint scoring remains disabled.

## Claim Boundary

This gate does not mutate provenance, import observed data, pass leakage audit,
activate rows, compute scores, or compare model families.
