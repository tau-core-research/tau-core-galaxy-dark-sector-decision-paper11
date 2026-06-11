# Source Import Provenance Evidence Gate v22

**Doc class:** provenance evidence input gate  
**Status:** evidence input missing; no promotion; no scoring allowed  

Script:

```text
scripts/run_source_import_provenance_evidence_gate.py
```

Expected evidence input:

```text
data/input/source_import_provenance_evidence_v21.csv
```

Derived outputs:

```text
data/derived/source_import_provenance_evidence_gate_v22.csv
data/derived/source_import_provenance_evidence_gate_summary_v22.csv
```

This layer checks whether external provenance evidence is present and shaped
well enough to support a later promotion step into the v19 provenance manifest.

## Current Result

The expected status is:

```text
PROVENANCE_EVIDENCE_INPUT_MISSING
```

No evidence input file is present, no evidence rows are validated, and
provenance promotion remains blocked.

## Claim Boundary

This gate does not promote provenance, import observed data, pass leakage audit,
activate rows, compute scores, or compare model families.
