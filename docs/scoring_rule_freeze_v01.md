# Scoring Rule Freeze v01

**Doc class:** scoring-policy manifest  
**Status:** scoring components declared; no formulas, no numeric thresholds, no endpoint scoring  

Machine-readable manifest:

```text
data/source_manifest/scoring_rule_freeze_v01.csv
```

This manifest declares the scoring components that must be defined before any
model family is evaluated:

- full-curve fit quality;
- inner/rising-zone diagnostic;
- flat/outer-zone diagnostic;
- held-out generalization;
- parsimony penalty;
- control penalty.

## Claim Boundary

This manifest does not provide scoring formulas or weights. It prevents the
score from being chosen after seeing which model family performs best.

Next honest target:

```text
SCORING_FORMULA_FREEZE_V02
```
