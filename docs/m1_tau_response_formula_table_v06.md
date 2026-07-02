# M1 Tau Response Formula Table v06

**Doc class:** M1 response-formula table contract
**Status:** response slot table ready; admissibility blocked; no Response_tau formula

Script:

```text
scripts/build_m1_tau_response_formula_table.py
```

Derived outputs:

```text
data/derived/m1_tau_response_formula_table_v06.csv
data/derived/m1_tau_response_formula_table_summary_v06.csv
```

This artifact fills the M1 `tau_response_formula` formula-table slot as a
pre-scoring contract. It freezes the required response components: activation
rule, carrier slot, amplitude policy, scale policy, channel handoff, and
zero-response policy.

## Current Result

The expected status is:

```text
M1_TAU_RESPONSE_FORMULA_TABLE_READY_ADMISSIBILITY_BLOCKED
```

The next required artifact is:

```text
m1_admissibility_table_v06
```

## Claim Boundary

This table does not claim a `Response_tau` formula, does not claim a physical
Tau response field, writes no numeric response values, writes no M1 prediction
rows, computes no endpoint scores, and makes no dark-sector verdict.
