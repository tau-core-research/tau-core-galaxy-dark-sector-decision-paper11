# Source Import Provenance Audit v20

**Doc class:** executable provenance audit gate  
**Status:** raw import blocked by provenance; no scoring allowed  

Script:

```text
scripts/run_source_import_provenance_audit.py
```

Derived outputs:

```text
data/derived/source_import_provenance_audit_v20.csv
data/derived/source_import_provenance_audit_summary_v20.csv
```

This layer audits whether the v19 provenance manifest is complete enough to
allow any raw source import.

## Current Result

The expected status is:

```text
RAW_IMPORT_BLOCKED_BY_PROVENANCE
```

All candidate rows remain blocked because provenance is not filled.

## Claim Boundary

This audit does not import observed data, write the v12 target input, pass
leakage audit, activate rows, compute scores, or compare model families.
