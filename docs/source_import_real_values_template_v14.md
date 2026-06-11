# Source Import Real Values Template v14

**Doc class:** source-input template  
**Status:** template ready; not data; no scoring allowed  

Script:

```text
scripts/build_source_import_real_values_template.py
```

Template output:

```text
data/input/source_import_real_values_v12_TEMPLATE.csv
```

Derived outputs:

```text
data/derived/source_import_template_columns_v14.csv
data/derived/source_import_template_summary_v14.csv
```

This layer provides a fillable CSV shape for the real source-value import
expected by the v12 gate.

## Current Result

The expected status is:

```text
SOURCE_IMPORT_TEMPLATE_READY_NOT_DATA
```

The template contains one placeholder row per candidate galaxy. Those rows are
not observed values and must not be copied into scoring without replacement by
real source-native radial-grid rows.

## Claim Boundary

This template does not import observed data, pass leakage audit, activate rows,
compute scores, or compare model families.
