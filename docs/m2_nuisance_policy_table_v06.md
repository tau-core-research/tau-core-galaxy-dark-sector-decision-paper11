# M2 Nuisance Policy Table v06

**Doc class:** M2 nuisance-policy table contract
**Status:** nuisance policy ready; shared scoring inputs blocked; no scoring

Script:

```text
scripts/build_m2_nuisance_policy_table.py
```

Derived outputs:

```text
data/derived/m2_nuisance_policy_table_v06.csv
data/derived/m2_nuisance_policy_table_summary_v06.csv
```

This artifact fills the M2 `benchmark_nuisance_policy` slot as a pre-scoring
contract. It freezes the stellar mass-to-light policy, gas scaling policy,
uncertainty policy, nuisance prior policy, shared baryonic fairness policy, and
prediction handoff before endpoint scoring.

## Current Result

The expected status is:

```text
M2_NUISANCE_POLICY_TABLE_READY_SHARED_INPUTS_BLOCKED
```

The next required artifact is:

```text
shared_scoring_input_table_v06
```

## Claim Boundary

This table does not validate the standard dark sector, does not prove an M2
endpoint result, writes no numeric nuisance values, writes no M2 prediction
rows, computes no endpoint scores, and makes no dark-sector verdict.
