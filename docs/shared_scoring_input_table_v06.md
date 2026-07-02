# Shared Scoring Input Table v06

**Doc class:** shared scoring-input contract
**Status:** shared input policy ready; parameter counts blocked; no scoring

Script:

```text
scripts/build_shared_scoring_input_table.py
```

Derived outputs:

```text
data/derived/shared_scoring_input_table_v06.csv
data/derived/shared_scoring_input_table_summary_v06.csv
```

This artifact fills the `shared_scoring_inputs` slot as a family-independent
pre-scoring contract. It freezes the data-loader policy, radial-grid policy,
radial-mask policy, uncertainty-handling policy, baryonic-component policy, and
parameter-count handoff before any endpoint score can be computed.

## Current Result

The expected status is:

```text
SHARED_SCORING_INPUT_TABLE_READY_PARAMETER_COUNTS_BLOCKED
```

The next required artifact is:

```text
numeric_parameter_count_table_v06
```

## Claim Boundary

This table writes no numeric input values, writes no family prediction rows,
computes no endpoint scores, compares no families, and makes no dark-sector
verdict. It only freezes the shared input policy required before parameter
counts can be reviewed.
