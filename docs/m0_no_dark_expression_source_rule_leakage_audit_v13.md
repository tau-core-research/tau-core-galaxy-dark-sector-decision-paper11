# M0 No-Dark Expression Source-Rule Leakage Audit v13

**Doc class:** no-dark M0 expression source-rule leakage audit
**Status:** leakage audit ready; symbolic/formula expression still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_source_rule_leakage_audit.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_source_rule_leakage_audit_v13.csv
data/derived/m0_no_dark_expression_source_rule_leakage_audit_summary_v13.csv
```

This artifact audits whether the output-class handoff can remain source-side
and pre-endpoint before the no-dark M0 expression path advances. It checks the
source-domain state, no-dark family constraint, morphology/readout factor,
finite-local `U_read` marker, baryonic/source binding state, and failure-route
marker against endpoint residual, heldout score, family-winner, best-fit curve,
and post-hoc exception leakage.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_SOURCE_RULE_LEAKAGE_AUDIT_READY
```

Six leakage-audit rows are ready:

- source-domain leakage audit;
- no-dark constraint leakage audit;
- morphology/readout factor leakage audit;
- finite-local `U_read` marker leakage audit;
- baryonic/source binding leakage audit;
- failure-route leakage audit.

The next missing artifact is:

```text
m0_no_dark_expression_symbolic_form_v12
```

## Claim Boundary

This leakage audit does not define the M0 no-dark source rule, does not define
an expression, does not write a formula, does not compute predicted velocities,
does not score galaxies, and does not decide the dark-sector question. It only
closes the source-rule leakage-audit gate and authorizes the next construction
artifact: the symbolic or algorithmic expression form.
