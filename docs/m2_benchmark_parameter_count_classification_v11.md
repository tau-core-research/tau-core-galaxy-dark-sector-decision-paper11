# M2 Benchmark Parameter Count Classification v11

**Doc class:** M2 benchmark-parameter countability classification
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** countability classified; count-value ledger pending
**Canonical parent:** M2 benchmark parameter inventory v10

Script:

```text
scripts/build_m2_benchmark_parameter_count_classification.py
```

Derived outputs:

```text
data/derived/m2_benchmark_parameter_count_classification_v11.csv
data/derived/m2_benchmark_parameter_count_classification_summary_v11.csv
```

## Current Result

The v11 classification assigns countability rules to the twelve M2 benchmark
profile and nuisance slots. It separates fixed protocol/shared-input guards
from profile, halo, nuisance, prior, uncertainty, component, and switch
privileges that count if they become adjustable.

The expected status is:

```text
M2_BENCHMARK_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING
```

The next required artifact is:

```text
m2_benchmark_parameter_count_value_ledger_v12.csv
```

## Claim Boundary

This artifact writes no final numeric parameter count, no benchmark/profile
value, no nuisance value, no M2 prediction row, no per-galaxy benchmark
privilege count, no parsimony penalty, no endpoint scores, and no dark-sector
verdict. It only classifies how M2 benchmark slots must be treated by the later
count-value ledger.
