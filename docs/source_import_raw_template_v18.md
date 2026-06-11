# Source Import Raw Template v18

**Doc class:** raw source-input template  
**Status:** template ready; not data; no scoring allowed  

Script:

```text
scripts/build_source_import_raw_template.py
```

Template output:

```text
data/input/source_import_raw_sparc_like_v15_TEMPLATE.csv
```

Derived outputs:

```text
data/derived/source_import_raw_template_columns_v18.csv
data/derived/source_import_raw_template_summary_v18.csv
```

This layer provides a fillable CSV shape for the raw SPARC-like source input
expected by the v15 adapter.

## Current Result

The expected status is:

```text
RAW_TEMPLATE_READY_NOT_DATA
```

The template contains placeholder rows only. It is not the raw input file and
must not be treated as observed data.

## Claim Boundary

This template does not import observed data, write the v12 target input, pass
leakage audit, activate rows, compute scores, or compare model families.
