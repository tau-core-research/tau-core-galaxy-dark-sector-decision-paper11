# Active v12 Real-Values Write Authorization v57

**Doc class:** active write-authorization artifact
**Status:** v12 write authorization granted; no leakage pass; no scoring allowed

## Script

```text
scripts/run_active_v12_real_values_write_authorization.py
```

## Outputs

```text
data/input/source_import_real_values_write_authorization_v57.csv
data/derived/active_v12_real_values_write_authorization_summary_v57.csv
```

## Purpose

This layer records an explicit machine-readable authorization to write the v12
real-values input from the reviewed v15 raw SPARC-like input. It separates the
authorization decision from the writer itself, so the v17 writer can be audited
as an authorized operation rather than as an implicit side effect of the raw
adapter.

## Current Result

The v57 authorization file grants
`AUTHORIZE_V12_WRITE_FROM_ACTIVE_V15_RAW` after the v15 raw adapter reports
`RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW`. The v57 artifact itself writes
zero v12 target rows and does not pass leakage audit.

## Claim Boundary

This authorization does not compute scores, pass leakage audit, activate
scoring rows, compare model families, or decide whether a Tau-derived dark
sector is required.
