# Scoring Formula Freeze v02

**Doc class:** scoring-formula manifest  
**Status:** formula policy frozen; no endpoint scoring; no verdict thresholds  

Machine-readable manifest:

```text
data/source_manifest/scoring_formula_freeze_v02.csv
```

This manifest fixes the first shared scoring formula policy for Paper 11. The
same formula family applies to `M0`, `M1`, and `M2`.

## Frozen Formula Policy

The v02 score has four parts:

- full-curve chi-square-like fit quality;
- inner/rising-zone diagnostic on the lowest third of radial-grid points;
- outer/flat-zone diagnostic on the highest third of radial-grid points;
- BIC-like parsimony penalty using predeclared endpoint parameter counts.

The per-galaxy score is:

```text
score(f,g) = chi2_full(f,g)
           + 0.5 * chi2_inner(f,g)
           + 0.5 * chi2_outer(f,g)
           + penalty(f,g)
```

Held-out family comparison uses the median over the frozen held-out role set.
Control failures veto verdict eligibility.

## Claim Boundary

This manifest does not provide:

- numerical scores;
- family parameter counts;
- executed controls;
- decision thresholds;
- a dark-sector verdict.

Next honest target:

```text
FAMILY_PARAMETER_COUNT_AND_CONTROL_IMPLEMENTATION_V03
```
