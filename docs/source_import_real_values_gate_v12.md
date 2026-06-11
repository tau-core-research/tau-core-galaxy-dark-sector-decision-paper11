# Source Import Real Values Gate v12

**Doc class:** executable source-value import gate  
**Status:** input file missing; no real values imported; no scoring allowed  

Script:

```text
scripts/run_source_import_real_values_gate.py
```

Derived outputs:

```text
data/derived/source_import_real_values_schema_v12.csv
data/derived/source_import_real_values_gate_v12.csv
data/derived/source_import_real_values_summary_v12.csv
```

Expected external input:

```text
data/input/source_import_real_values_v12.csv
```

This gate defines the exact file shape required before Paper 11 can import
real radial-grid, observed-velocity, baryonic-component, source-route, and
leakage-evidence values.

## Current Result

The expected status is:

```text
SOURCE_IMPORT_REAL_VALUES_BLOCKED
```

The reproducibility package intentionally contains no real observed galaxy
values. The v12 gate therefore imports zero numeric rows, activates zero rows,
and keeps endpoint scoring disabled.

## Claim Boundary

This gate does not import SPARC data, pass leakage audit, activate rows,
compute scores, compare model families, or decide whether the Tau dark-sector
response layer is necessary.

Next honest target:

```text
data/input/source_import_real_values_v12.csv
```
