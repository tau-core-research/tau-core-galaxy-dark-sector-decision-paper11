# M0 No-Dark Rule Parent Assumption Basis v14

**Doc class:** no-dark M0 parent-assumption basis
**Status:** parent basis ready; rule-selection map still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_rule_parent_assumption_basis.py
```

Derived outputs:

```text
data/derived/m0_no_dark_rule_parent_assumption_basis_v14.csv
data/derived/m0_no_dark_rule_parent_assumption_basis_summary_v14.csv
```

This artifact closes only the first source-side prerequisite in the M0 no-dark
rule-derivation chain. It records the parent assumptions that a later
rule-selection map may use before endpoint residuals, held-out scores, family
winners, or best-fit curves are available.

## Current Result

The expected status is:

```text
M0_NO_DARK_RULE_PARENT_ASSUMPTION_BASIS_READY
```

Six parent-basis rows are ready:

- source-freeze boundary;
- no-dark response exclusion for the M0 family;
- morphology/readout source basis;
- restricted local `U_read` closure-diagnostic basis;
- baryonic/source input boundary;
- non-circular failure policy.

The next missing artifact is:

```text
m0_no_dark_rule_selection_map_v14
```

## Claim Boundary

This basis does not derive the M0 no-dark rule, does not choose a formula, does
not generate terms, does not compute predicted velocities, does not score
galaxies, and does not decide the dark-sector question. It only authorizes the
next source-side artifact: a pre-endpoint rule-selection map.
