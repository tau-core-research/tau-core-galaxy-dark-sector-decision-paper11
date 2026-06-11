# Active v15 Raw SPARC-like Input Writer v56

**Doc class:** active raw source input writer  
**Status:** raw SPARC-like input written; no v12 real-values write; no scoring allowed  

Script:

```text
scripts/run_active_v15_raw_sparc_like_input_writer.py
```

Inputs:

```text
data/external/sparc_hash_audit_v50/MassModels_Lelli2016c.mrt
data/input/source_import_provenance_evidence_v21.csv
data/derived/activated_scoring_rows_v08.csv
```

Outputs:

```text
data/input/source_import_raw_sparc_like_v15.csv
data/derived/active_v15_raw_sparc_like_input_writer_summary_v56.csv
```

This layer extracts the frozen Paper 11 galaxy rows from the cached SPARC
MassModels file and writes them into the v15 raw adapter input shape. It writes
raw source rows only; it does not write `source_import_real_values_v12.csv`.

## Current Result

The expected status is:

```text
ACTIVE_V15_RAW_SPARC_LIKE_INPUT_WRITTEN
```

The current output contains 450 radial rows covering all eighteen frozen
galaxies. Endpoint scoring remains disabled.

## Claim Boundary

This writer closes the raw-input-file-missing frontier only. It is not a v12
real-values import, not leakage clearance, not endpoint scoring, and not a
dark-sector verdict. The next blocker is explicit authorization to write the
v12 real-values target.
