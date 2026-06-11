# Source Import Provenance Manifest v19

**Doc class:** source provenance manifest  
**Status:** provenance required; not filled; no raw import allowed  

Script:

```text
scripts/build_source_import_provenance_manifest.py
```

Derived outputs:

```text
data/derived/source_import_provenance_manifest_v19.csv
data/derived/source_import_provenance_columns_v19.csv
data/derived/source_import_provenance_summary_v19.csv
```

This layer defines the provenance evidence required before any raw source input
can be accepted for the scoring path.

## Current Result

The expected status is:

```text
PROVENANCE_REQUIRED_NOT_FILLED
```

No row has complete catalog, file/table, row identity, hash/accession, source
route, or leakage-evidence provenance. Raw import remains blocked.

## Claim Boundary

This manifest does not import observed data, write the v12 target input, pass
leakage audit, activate rows, compute scores, or compare model families.
