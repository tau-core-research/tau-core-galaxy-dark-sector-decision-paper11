# Family Prediction Table Contract v80

**Doc class:** family-prediction table contract
**Status:** prediction-table schema ready; parameter counts blocked; no scoring

Script:

```text
scripts/build_family_prediction_table_contract.py
```

Derived outputs:

```text
data/derived/family_prediction_table_schema_v80.csv
data/derived/family_prediction_table_slot_requirements_v80.csv
data/derived/family_prediction_table_contract_summary_v80.csv
```

This contract defines the table shape required before any `M0`, `M1`, or `M2`
prediction rows can be scored. It also expands the eight formula-table slots
from `family_formula_table_v05.csv` into explicit blocking requirements.

## Current Result

The expected status is:

```text
FAMILY_PREDICTION_TABLE_CONTRACT_READY_PARAMETER_COUNTS_BLOCKED
```

The schema is ready, all eight formula slots are ready, and 450 M0 no-dark
prediction rows are written without endpoint
scores. The `m0_no_dark_formula_table_v06`,
`m0_no_dark_formula_body_v07`, `m0_no_dark_readout_equation_v08`,
`m0_no_dark_equation_kernel_v09`, `m0_no_dark_kernel_expression_v10`, and
`m0_no_dark_frozen_expression_v11` contracts are now present, and the v12
source-rule contract is declared. The `m0_label_rule_table_v06`,
`m1_tau_response_formula_table_v06`, and `m1_admissibility_table_v06`
contracts are also present. The M1 response and admissibility tables are only
pre-scoring contracts: they claim no `Response_tau` formula, write no response
values, and write no M1 prediction rows. The `m2_benchmark_profile_table_v06`
contract is present too and freezes only the benchmark-profile policy, not
numeric profile values or M2 prediction rows. The `m2_nuisance_policy_table_v06`
contract is present too and freezes only nuisance-policy handling, not numeric
nuisance values or M2 prediction rows. The `shared_scoring_input_table_v06`
contract is present too and freezes only shared input policy, not numeric input
values or endpoint scores. The first concrete missing
count artifact is:

```text
numeric_parameter_count_table_v08.csv
```

## Claim Boundary

This contract does not compute endpoint scores, does not compare families, and
does not make a dark-sector verdict. It only narrows the scoring frontier from
the broad family prediction table to final numeric parameter counts.
