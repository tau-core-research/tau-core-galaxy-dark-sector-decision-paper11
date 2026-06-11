# Scoring Input Scaffold v08

**Doc class:** executable scoring-input scaffold  
**Status:** input tables created; no rows activated; observed data missing  

Script:

```text
scripts/build_scoring_input_scaffold.py
```

Derived outputs:

```text
data/derived/activated_scoring_rows_v08.csv
data/derived/scoring_observed_input_schema_v08.csv
data/derived/scoring_observed_inputs_v08.csv
data/derived/scoring_input_scaffold_summary_v08.csv
```

This layer creates the tables the scoring runner will eventually consume. It
does not import real observed data and does not activate endpoint scoring.

## Current Result

The expected status is:

```text
INPUT_SCAFFOLD_READY_DATA_MISSING
```

All galaxy rows are still `NOT_ACTIVATED`, and all observed numeric fields are
`PENDING_SOURCE_IMPORT`.

## Claim Boundary

This scaffold does not compute scores, does not validate any family, and does
not produce a dark-sector verdict.

Next honest target:

```text
SOURCE_IMPORT_AND_LEAKAGE_AUDIT_V09
```
