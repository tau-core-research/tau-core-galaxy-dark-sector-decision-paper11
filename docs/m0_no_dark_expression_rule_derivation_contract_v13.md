# M0 No-Dark Expression Rule Derivation Contract v13

**Doc class:** no-dark M0 rule-derivation contract
**Status:** derivation contract ready; parent assumption basis blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_rule_derivation_contract.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_rule_derivation_contract_v13.csv
data/derived/m0_no_dark_expression_rule_derivation_contract_summary_v13.csv
```

This contract expands the `m0_no_dark_expression_rule_derivation_v13` blocker
into the minimum derivation-record slots required before any no-dark M0
source-rule derivation can be claimed.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_RULE_DERIVATION_CONTRACT_READY_PARENT_BASIS_BLOCKED
```

The rule-derivation contract exists, but zero derivation records and zero
numeric prediction rows are written. The first concrete missing artifact is:

```text
m0_no_dark_rule_parent_assumption_basis_v14
```

## Claim Boundary

This contract does not derive the M0 no-dark rule, does not define a source
rule or expression, does not compute predicted velocities, does not compare
M0/M1/M2, and does not make a dark-sector verdict. It only narrows the scoring
frontier from a missing rule derivation to the first missing parent-assumption
basis.
