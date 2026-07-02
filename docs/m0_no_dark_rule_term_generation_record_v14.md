# M0 No-Dark Rule Term Generation Record v14

**Doc class:** no-dark M0 term-generation record
**Status:** term-generation record ready; invariance/null checks still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_rule_term_generation_record.py
```

Derived outputs:

```text
data/derived/m0_no_dark_rule_term_generation_record_v14.csv
data/derived/m0_no_dark_rule_term_generation_record_summary_v14.csv
```

This artifact records which source-side term classes may be generated from the
ready rule-selection map before endpoint residuals, held-out scores, family
winners, or best-fit curves are available. It does not choose coefficients,
write equations, compute velocities, or score families.

## Current Result

The expected status is:

```text
M0_NO_DARK_RULE_TERM_GENERATION_RECORD_READY
```

Six term-generation rows are ready:

- input-domain placeholders;
- M0 no-dark exclusion flags;
- morphology/readout symbolic source-term classes;
- finite-local `U_read` admissibility markers;
- frozen source-input binding classes;
- no-promotion failure-route markers.

The next missing artifact is:

```text
m0_no_dark_rule_invariance_null_checks_v14
```

## Claim Boundary

This term-generation record does not define the M0 no-dark expression, does
not choose coefficients, does not perform dimensional closure, does not compute
predicted velocities, does not score galaxies, and does not decide the
dark-sector question. It only authorizes the next source-side artifact:
pre-endpoint invariance, null, gauge, and fallback checks.
