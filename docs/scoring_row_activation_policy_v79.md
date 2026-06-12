# Scoring Row Activation Policy v79

**Doc class:** row-activation policy gate  
**Status:** rows activated for later scoring prerequisites; endpoint scoring still blocked  

Script:

```text
scripts/run_scoring_row_activation_policy.py
```

Derived outputs:

```text
data/derived/activated_scoring_rows_v10.csv
data/derived/scoring_row_activation_policy_summary_v79.csv
```

This policy consumes the v12 real-value gate, the v09 source/leakage audit, and
the v78 leakage-pass review. A row can be marked `ACTIVATED` only if real
values are present and the galaxy has a reviewed leakage pass.

## Current Result

The expected status is:

```text
SCORING_ROW_ACTIVATION_POLICY_READY_GLOBAL_SCORING_BLOCKED
```

All eighteen galaxy rows are written to `activated_scoring_rows_v10.csv` with
`activation_status = ACTIVATED`.

This does not allow endpoint scoring. The next blocker is:

```text
family_prediction_tables_v08.csv
```

## Claim Boundary

This gate is not endpoint scoring, not a model comparison, not empirical
validation, and not a dark-sector verdict. It only clears the row-activation
blocker after the leakage pass and hands the protocol to the global scoring
prerequisites: family prediction tables, parameter counts, control outputs,
and decision thresholds.
