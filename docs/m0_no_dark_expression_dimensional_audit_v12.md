# M0 No-Dark Expression Dimensional Audit v12

**Doc class:** no-dark M0 expression dimensional-audit record
**Status:** dimensional audit ready; machine form still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_dimensional_audit.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_dimensional_audit_v12.csv
data/derived/m0_no_dark_expression_dimensional_audit_summary_v12.csv
```

This artifact audits the unit-route discipline required before the M0 no-dark
expression can be serialized. It blocks post-hoc unit rescaling, hidden
dark-response-like units, endpoint-repaired baryonic normalizations, and
unit-bearing rescue terms.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_DIMENSIONAL_AUDIT_READY
```

Six dimensional-audit rows are ready:

- source-state unit audit;
- no-dark constraint unit audit;
- baryonic/source input unit audit;
- readout-operator unit audit;
- failure-route unit audit;
- assembly unit audit.

The next missing artifact is:

```text
m0_no_dark_expression_machine_form_v12
```

## Claim Boundary

This dimensional audit does not define a complete expression, does not write a
velocity formula, does not assign numeric coefficients, does not compute
predicted velocities, does not score galaxies, and does not decide the
dark-sector question. It only authorizes the next construction artifact:
machine-form serialization.
