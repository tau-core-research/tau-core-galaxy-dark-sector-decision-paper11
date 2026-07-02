# M0 No-Dark Rule Derivation Provenance and Leakage Audit v14

**Doc class:** no-dark M0 derivation provenance/leakage audit
**Status:** derivation provenance/leakage audit ready; source-basis construction still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_rule_derivation_provenance_leakage.py
```

Derived outputs:

```text
data/derived/m0_no_dark_rule_derivation_provenance_leakage_v14.csv
data/derived/m0_no_dark_rule_derivation_provenance_leakage_summary_v14.csv
```

This artifact audits the provenance and leakage boundary of the M0 no-dark
derivation preconditions. It records that the parent basis, selection map, term
generation, invariance/null checks, and dimensional precheck are source-side
protocol artifacts, not endpoint-selected formulas.

## Current Result

The expected status is:

```text
M0_NO_DARK_RULE_DERIVATION_PROVENANCE_LEAKAGE_READY
```

Six audit rows are ready:

- parent-basis provenance;
- rule-selection map provenance;
- term-generation provenance;
- invariance/null provenance;
- dimensional-precheck provenance;
- frontier handoff to source-basis construction.

The next missing artifact is:

```text
m0_no_dark_expression_source_basis_v13
```

## Claim Boundary

This audit does not define a source rule, does not define an expression, does
not write a formula, does not compute predicted velocities, does not score
galaxies, and does not decide the dark-sector question. It only closes the
derivation-precondition leakage audit and authorizes the next source-side
construction artifact: the M0 no-dark expression source basis.
