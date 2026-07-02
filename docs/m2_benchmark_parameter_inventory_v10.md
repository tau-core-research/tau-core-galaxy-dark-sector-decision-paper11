# M2 Benchmark Parameter Inventory v10

**Doc class:** M2 global benchmark-parameter inventory
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** inventory present; countability classification pending
**Canonical parent:** numeric count readiness closure v09

Script:

```text
scripts/build_m2_benchmark_parameter_inventory.py
```

Derived outputs:

```text
data/derived/m2_benchmark_parameter_inventory_v10.csv
data/derived/m2_benchmark_parameter_inventory_summary_v10.csv
```

## Current Result

The inventory lifts the M2 benchmark-profile and nuisance-policy rows into a
global benchmark-parameter audit table. It records the profile-family,
halo-parameter, prior, profile-switch, stellar mass-to-light, gas-scaling,
uncertainty, nuisance-prior, shared-fairness, and prediction-handoff slots that
must be classified before any M2 numeric benchmark-parameter count can be
written.

The expected status is:

```text
M2_BENCHMARK_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING
```

The next required artifact is:

```text
m2_benchmark_parameter_count_classification_v11.csv
```

## Claim Boundary

This artifact writes no final numeric parameter count, no benchmark/profile
value, no nuisance value, no M2 prediction row, no per-galaxy benchmark
privilege count, no parsimony penalty, no endpoint scores, and no dark-sector
verdict. It only makes the M2 global benchmark-parameter inventory explicit so
the next artifact can classify which slots are fixed, countable, disqualifying,
or still blocked.
