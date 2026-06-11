# Source Import Authorized Writer v17

**Doc class:** guarded target-input writer
**Status:** writer authorized; v12 target input written; no scoring allowed

Script:

```text
scripts/run_source_import_authorized_writer.py
```

Derived outputs:

```text
data/derived/source_import_authorized_writer_v17.csv
data/derived/source_import_authorized_writer_summary_v17.csv
```

This layer contains the guarded writer path from a valid raw source file into
the v12 real-value target input.

## Current Result

The expected status is:

```text
AUTHORIZED_WRITER_WROTE_TARGET_INPUT
```

The current package has a valid raw input and explicit v57 write authorization.
The writer writes 450 rows into `data/input/source_import_real_values_v12.csv`.
This does not pass leakage audit or activate scoring rows.

## Claim Boundary

This writer does not pass leakage audit, activate rows, compute scores, compare
model families, or decide dark-sector necessity.
