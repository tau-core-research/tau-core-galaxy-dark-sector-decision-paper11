# M0 No-Dark Frozen Expression Body v14

**Doc class:** M0 no-dark frozen-expression body definition
**Reader role:** reviewer-facing scoring-frontier bridge
**Status:** expression body formulated; no velocity formula; no scoring
**Canonical parent:** family prediction frontier trace v81

Script:

```text
scripts/build_m0_no_dark_frozen_expression_body.py
```

Derived outputs:

```text
data/derived/m0_no_dark_frozen_expression_body_v14.csv
data/derived/m0_no_dark_frozen_expression_body_summary_v14.csv
```

## Body Statement

The M0 no-dark frozen expression body is fixed at definition level as:

```text
X_M0 = (source_state, baryonic_input, radius_grid, readout_operator, guard_state, assembly_order)

E_M0(X_M0) :=
  Assemble_M0[
    Readout_M0(source_state, readout_operator),
    Baryon(baryonic_input, radius_grid),
    Guard(guard_state),
    Order(assembly_order)
  ]
```

This is a frozen source-side expression body. It says what the M0 no-dark
candidate is allowed to assemble from, and what it is not allowed to use.

## No-Dark Constraint

The body forbids hidden dark-sector compensation inside M0:

```text
DarkCompensationTerm(E_M0) = forbidden
```

Unresolved, inadmissible, null, gauge, or missing-input cases must route to the
declared null/fallback states rather than adding rescue terms.

## Claim Boundary

This artifact does not define an executable velocity formula, does not assign
coefficient values, does not write `v_pred_km_s` rows, does not compute endpoint
scores, and does not decide whether a dark-sector component is physically
required. It only formulates the M0 no-dark expression body that a later kernel
expression review may accept, refine, or reject.
