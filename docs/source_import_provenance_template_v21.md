# Source Import Provenance Template v21

**Doc class:** provenance evidence template  
**Status:** template ready; not data; no raw import allowed  

Script:

```text
scripts/build_source_import_provenance_template.py
```

Template output:

```text
data/input/source_import_provenance_evidence_v21_TEMPLATE.csv
```

Derived outputs:

```text
data/derived/source_import_provenance_template_columns_v21.csv
data/derived/source_import_provenance_template_summary_v21.csv
```

This layer provides the fillable CSV shape for provenance evidence that could
later satisfy the v19 manifest and v20 audit.

## Current Result

The expected status is:

```text
PROVENANCE_TEMPLATE_READY_NOT_DATA
```

The template contains placeholder rows only. It is not provenance evidence and
does not allow raw import.

## Claim Boundary

This template does not provide source provenance, import observed data, pass
leakage audit, activate rows, compute scores, or compare model families.
