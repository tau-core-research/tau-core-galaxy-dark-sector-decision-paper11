# M0 No-Dark Expression Output Class v13

**Doc class:** no-dark M0 expression output-class record
**Status:** output class ready; source-rule leakage audit still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_output_class.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_output_class_v13.csv
data/derived/m0_no_dark_expression_output_class_summary_v13.csv
```

This artifact declares what kind of object the M0 no-dark expression path may
hand forward after the null/fallback policy. It does not write the source rule
or formula. It only classifies allowed output shapes so the next audit can check
that the source rule is not selected from endpoint residuals.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_OUTPUT_CLASS_READY
```

Six output classes are ready:

- source-domain evidence state;
- no-dark family constraint state;
- typed morphology/readout factor;
- finite-local `U_read` admissibility marker;
- source-input binding state;
- blocked-route failure marker.

The next missing artifact is:

```text
m0_no_dark_expression_source_rule_leakage_audit_v13
```

## Claim Boundary

This output-class record does not define the M0 no-dark source rule, does not
define an expression, does not write a formula, does not compute predicted
velocities, does not score galaxies, and does not decide the dark-sector
question. It only authorizes the next source-side construction artifact: the
source-rule leakage audit.
