# M0 No-Dark Expression Machine Form v12

**Doc class:** no-dark M0 expression machine-form serialization contract
**Status:** machine form ready; formula and scoring still blocked

Script:

```text
scripts/build_m0_no_dark_expression_machine_form.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_machine_form_v12.csv
data/derived/m0_no_dark_expression_machine_form_summary_v12.csv
```

This artifact serializes the source-side M0 no-dark expression contract into
machine-readable slots that a later formula-body writer can consume. It records
source-state, no-dark constraint, baryonic-input, readout-operator,
failure-route, and assembly contracts.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_MACHINE_FORM_READY
```

Six machine-form rows are ready:

- source-state serialization;
- no-dark constraint serialization;
- baryonic/source input serialization;
- readout-operator serialization;
- failure-route serialization;
- assembly serialization.

The next required artifact is:

```text
family_prediction_tables_v08.csv
```

## Claim Boundary

This machine form is not a velocity formula, not a callable prediction engine,
not a fitted response model, and not an endpoint score. It does not decide the
dark-sector question. It only closes the serialization slot of the M0 no-dark
frozen-expression contract and hands the remaining work to formula/prediction
table construction.
