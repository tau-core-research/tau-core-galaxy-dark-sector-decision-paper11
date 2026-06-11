# Source Import and Leakage Audit v09

**Doc class:** executable source-import/leakage gate  
**Status:** audit runner implemented; source import pending; no rows activated  

Script:

```text
scripts/run_source_import_leakage_audit.py
```

Derived outputs:

```text
data/derived/source_import_and_leakage_audit_v09.csv
data/derived/source_import_requirements_v09.csv
data/derived/leakage_audit_findings_v09.csv
data/derived/source_import_leakage_summary_v09.csv
```

This layer audits the v08 scoring-input scaffold. It does not import observed
data. It marks every row as blocked until source routes, numeric observed
inputs, and leakage evidence are present.

## Current Result

The expected status is:

```text
SOURCE_IMPORT_AND_LEAKAGE_BLOCKED
```

No row passes leakage audit and no row is activated for scoring.

## Claim Boundary

This audit does not compute scores, does not compare `M0`, `M1`, or `M2`, and
does not produce a dark-sector verdict.

Next honest target:

```text
SOURCE_IMPORT_TABLE_V10
```
