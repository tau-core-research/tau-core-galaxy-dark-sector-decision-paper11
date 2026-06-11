# Source Import Raw Adapter v15

**Doc class:** raw source-import adapter gate  
**Status:** raw input present for validation review; no target input written

Script:

```text
scripts/run_source_import_raw_adapter.py
```

Expected raw input:

```text
data/input/source_import_raw_sparc_like_v15.csv
```

Target real input:

```text
data/input/source_import_real_values_v12.csv
```

Derived outputs:

```text
data/derived/source_import_raw_adapter_schema_v15.csv
data/derived/source_import_raw_adapter_gate_v15.csv
data/derived/source_import_raw_adapter_summary_v15.csv
```

This layer defines the machine-readable path from a SPARC-like raw source file
to the v12 real-value input shape.

## Current Result

The expected status is:

```text
RAW_ADAPTER_READY_VALIDATION_PENDING_REVIEW
```

The active v15 raw input is present and validates 450 rows across eighteen
frozen galaxies. The adapter still does not write
`data/input/source_import_real_values_v12.csv`.

## Claim Boundary

This adapter does not import observed data, pass leakage audit, activate rows,
compute scores, compare model families, or decide dark-sector necessity.
