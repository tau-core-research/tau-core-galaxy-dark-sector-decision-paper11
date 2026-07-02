# Numeric Parameter Count Table v06

**Doc class:** numeric parameter-count contract
**Status:** count-rule ledger ready; final numeric counts blocked; no scoring

Script:

```text
scripts/build_numeric_parameter_count_table.py
```

Derived outputs:

```text
data/derived/numeric_parameter_count_table_v06.csv
data/derived/numeric_parameter_count_table_summary_v06.csv
```

This artifact fills the `numeric_parameter_count_table` slot as a pre-scoring
count-rule ledger. It imports the frozen family count policies and exposes the
families/components that must receive final numeric counts before endpoint
scoring.

## Current Result

The expected status is:

```text
NUMERIC_PARAMETER_COUNT_TABLE_CONTRACT_READY_FINAL_COUNTS_BLOCKED
```

The next required artifact is:

```text
numeric_parameter_count_table_v08.csv
```

## Claim Boundary

This table writes no final numeric count values, computes no parsimony penalty,
computes no endpoint scores, compares no families, and makes no dark-sector
verdict. It only closes the count-rule contract slot and hands off to the
final numeric count artifact.
