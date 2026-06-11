# Scoring Preflight v07

**Doc class:** executable scoring preflight  
**Status:** scoring input contract built; scoring not ready; no endpoint scores  

Script:

```text
scripts/run_scoring_preflight.py
```

Derived outputs:

```text
data/derived/scoring_input_requirements_v07.csv
data/derived/scoring_formula_components_v07.csv
data/derived/scoring_preflight_summary_v07.csv
```

This layer moves Paper 11 toward scoring without running scoring. It names the
exact artifacts required before `M0`, `M1`, and `M2` can be compared.

## Current Result

The expected status is:

```text
SCORING_NOT_READY
```

The scoring formula policy exists, but the scoring run is blocked by missing
activated rows, observed input tables, family prediction tables, numeric
parameter counts, control outputs, and numeric decision thresholds.

## Claim Boundary

This preflight does not compute scores, does not rank families, and does not
produce a dark-sector verdict.

Next honest target:

```text
ACTIVATED_SCORING_ROWS_AND_OBSERVED_INPUT_SCHEMA_V08
```
