# M0 Global Parameter Inventory v10

**Doc class:** M0 global parameter inventory
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** inventory present; countability classification pending
**Canonical parent:** numeric count readiness closure v09

Script:

```text
scripts/build_m0_global_parameter_inventory.py
```

Derived outputs:

```text
data/derived/m0_global_parameter_inventory_v10.csv
data/derived/m0_global_parameter_inventory_summary_v10.csv
```

## Current Result

The inventory lifts the M0 no-dark coefficient-policy rows into a global
parameter-audit table. It records the slot classes that must be classified
before a numeric M0 global parameter count can be written.

The expected status is:

```text
M0_GLOBAL_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING
```

The next required artifact is:

```text
m0_global_parameter_count_classification_v11.csv
```

## Claim Boundary

This artifact writes no final numeric parameter count, no coefficient values,
no per-galaxy privilege count, no parsimony penalty, no endpoint scores, and no
dark-sector verdict. It only makes the M0 global slot inventory explicit so the
next artifact can classify which slots are fixed, free, disqualifying, or still
blocked for parameter counting.
