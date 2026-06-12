# Family Prediction Table Contract v80

**Doc class:** family-prediction table contract
**Status:** prediction-table schema ready; formula slots blocked; no scoring

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
FAMILY_PREDICTION_TABLE_CONTRACT_READY_FORMULA_SLOTS_BLOCKED
```

The schema is ready, but zero formula slots are ready and zero numeric
prediction rows are written. The `m0_no_dark_formula_table_v06`,
`m0_no_dark_formula_body_v07`, `m0_no_dark_readout_equation_v08`,
`m0_no_dark_equation_kernel_v09`, `m0_no_dark_kernel_expression_v10`, and
`m0_no_dark_frozen_expression_v11` contracts are now present, so the first
concrete missing formula artifact is:

```text
m0_no_dark_expression_source_rule_v12
```

## Claim Boundary

This contract does not define a Tau response formula, does not compute
predicted velocities, does not compare families, and does not make a
dark-sector verdict. It only narrows the scoring frontier from the broad family
prediction table to the first missing source-side expression rule.
