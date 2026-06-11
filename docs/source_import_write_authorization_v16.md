# Source Import Write Authorization v16

**Doc class:** guarded write-authorization gate
**Status:** write authorization ready; no scoring allowed

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
WRITE_AUTHORIZATION_READY
```

The current package has a valid raw input file and an explicit v57 write
authorization. The v16 gate authorizes the v17 writer path but does not itself
write `data/input/source_import_real_values_v12.csv`.

## Claim Boundary

This gate does not import observed data, pass leakage audit, activate rows,
compute scores, compare model families, or decide dark-sector necessity.
