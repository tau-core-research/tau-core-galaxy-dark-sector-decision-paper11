# Shared Input Count-Discount Policy v10

**Doc class:** shared input count-discount policy
**Status:** shared-input discount policy frozen at zero; final numeric counts pending
**Canonical parent:** Shared scoring input table v06

Script:

```text
scripts/build_shared_input_count_discount_policy.py
```

Derived outputs:

```text
data/derived/shared_input_count_discount_policy_v10.csv
data/derived/shared_input_count_discount_policy_summary_v10.csv
```

This artifact closes the shared-input count-discount blocker. It audits the six
family-independent shared input components and freezes the discount value at
zero for each component:

```text
RESOLVED_ZERO_NO_SHARED_INPUT_COUNT_DISCOUNT
```

The rule is intentionally conservative: common input policies do not receive a
negative parameter discount, and any later family-specific loader, mask, grid,
uncertainty, or component exception must be counted or must block scoring.

The next required artifact is:

```text
numeric_parameter_count_table_final_values_v10.csv
```

## Claim Boundary

This policy writes only shared-input discount-policy rows. It writes no final numeric parameter counts,
computes no parsimony penalty, computes no endpoint scores, compares no families,
and makes no dark-sector verdict.

Claim boundary:

```text
shared_input_count_discount_policy_only_no_discount_no_final_counts_no_parsimony_no_scores
```
