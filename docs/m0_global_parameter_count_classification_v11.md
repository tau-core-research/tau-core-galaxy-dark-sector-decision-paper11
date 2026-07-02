# M0 Global Parameter Count Classification v11

**Doc class:** M0 global parameter countability classification
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** countability classified; numeric count values pending
**Canonical parent:** M0 global parameter inventory v10

Script:

```text
scripts/build_m0_global_parameter_count_classification.py
```

Derived outputs:

```text
data/derived/m0_global_parameter_count_classification_v11.csv
data/derived/m0_global_parameter_count_classification_summary_v11.csv
```

## Current Result

The v11 classification assigns each M0 global slot a countability rule. It
distinguishes fixed source-side guards from adjustable parameters, explicit
per-galaxy or rescue privileges, and disqualifying hidden dark-compensation
routes.

The expected status is:

```text
M0_GLOBAL_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING
```

The next required artifact is:

```text
m0_global_parameter_count_value_ledger_v12.csv
```

## Claim Boundary

This artifact writes no final numeric parameter count, no coefficient values,
no per-galaxy privilege count, no parsimony penalty, no endpoint scores, and no
dark-sector verdict. It only classifies how each global M0 slot must be treated
by the later numeric count-value ledger.
