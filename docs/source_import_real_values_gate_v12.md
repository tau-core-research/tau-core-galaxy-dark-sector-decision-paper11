# Source Import Real Values Gate v12

**Doc class:** executable source-value import gate
**Status:** real values present; leakage pending; no scoring allowed

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
SOURCE_IMPORT_REAL_VALUES_READY_FOR_LEAKAGE
```

The authorized writer has populated
`data/input/source_import_real_values_v12.csv` from the active v15 raw input.
The v12 gate imports 450 numeric rows for eighteen frozen galaxies and marks
all value gates as ready for leakage review. It activates zero rows and keeps
endpoint scoring disabled.

## Claim Boundary

This gate does not pass leakage audit, activate rows, compute scores, compare
model families, or decide whether the Tau dark-sector response layer is
necessary.

Next honest target:

```text
data/derived/source_import_leakage_summary_v09.csv
```
