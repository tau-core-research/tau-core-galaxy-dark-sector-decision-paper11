# M2 Benchmark Parameter Count Value Ledger v12

**Doc class:** M2 benchmark-parameter count-value ledger
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** partial slot values ready; benchmark-slot resolution pending
**Canonical parent:** M2 benchmark parameter count classification v11

Script:

```text
scripts/build_m2_benchmark_parameter_count_value_ledger.py
```

Derived outputs:

```text
data/derived/m2_benchmark_parameter_count_value_ledger_v12.csv
data/derived/m2_benchmark_parameter_count_value_ledger_summary_v12.csv
```

## Current Result

The v12 ledger converts the v11 M2 benchmark-slot countability classes into
slot-level count-value rows. Protocol handoff, prediction handoff, and
shared-input guard rows receive zero slot values. Profile-family, halo/profile,
prior, switch, stellar mass-to-light, gas, uncertainty, and nuisance-prior
slots remain conditional until a later benchmark-slot resolution proves whether
each freedom is fixed, absent, or countable.

The expected status is:

```text
M2_BENCHMARK_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING
```

The next required artifact is:

```text
m2_benchmark_parameter_adjustable_slot_resolution_v13.csv
```

## Claim Boundary

This artifact writes no final M2 global parameter count, no benchmark/profile
value, no nuisance value, no M2 prediction row, no per-galaxy benchmark
privilege count, no parsimony penalty, no endpoint scores, and no dark-sector
verdict. It only records slot-level count-value rules and the remaining
benchmark-slot evidence needed before a final M2 global count can be formed.
