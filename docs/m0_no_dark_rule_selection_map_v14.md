# M0 No-Dark Rule Selection Map v14

**Doc class:** no-dark M0 rule-selection map
**Status:** rule-selection map ready; term-generation record still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_rule_selection_map.py
```

Derived outputs:

```text
data/derived/m0_no_dark_rule_selection_map_v14.csv
data/derived/m0_no_dark_rule_selection_map_summary_v14.csv
```

This artifact maps the ready v14 parent-basis rows to pre-endpoint rule roles.
It does not generate expression terms, choose coefficients, define a velocity
formula, or compare candidate families.

## Current Result

The expected status is:

```text
M0_NO_DARK_RULE_SELECTION_MAP_READY
```

Six selection rows are ready:

- source-freeze basis to input-domain constraints;
- no-dark response exclusion to M0-family exclusion constraints;
- morphology/readout basis to source-term classes;
- restricted local `U_read` basis to finite-local admissibility ordering;
- baryonic/source boundary to input-binding candidates;
- failure policy to a no-promotion blocked route.

The next missing artifact is:

```text
m0_no_dark_rule_term_generation_record_v14
```

## Claim Boundary

This selection map does not derive the M0 no-dark expression, does not generate
terms, does not define a formula, does not compute predicted velocities, does
not score galaxies, and does not decide the dark-sector question. It only
authorizes the next source-side artifact: a pre-endpoint term-generation
record.
