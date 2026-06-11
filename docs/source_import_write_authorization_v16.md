# Source Import Write Authorization v16

**Doc class:** guarded write-authorization gate  
**Status:** write blocked; no target input written; no scoring allowed  

Script:

```text
scripts/run_source_import_write_authorization.py
```

Derived outputs:

```text
data/derived/source_import_write_authorization_v16.csv
data/derived/source_import_write_authorization_summary_v16.csv
```

This layer separates raw-source validation from writing the real v12 input
file. It requires both a valid raw adapter state and explicit write
authorization before any target file may be written.

## Current Result

The expected status is:

```text
WRITE_AUTHORIZATION_BLOCKED
```

The current package has a valid raw input file, but no explicit write
authorization. The next required authorization is
`PAPER11_ALLOW_REAL_SOURCE_IMPORT_WRITE=1`, and no
`data/input/source_import_real_values_v12.csv` file is written.

## Claim Boundary

This gate does not import observed data, pass leakage audit, activate rows,
compute scores, compare model families, or decide dark-sector necessity.
