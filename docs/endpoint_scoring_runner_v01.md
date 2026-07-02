# Endpoint Scoring Runner v01

**Doc class:** raw M0 adequacy diagnostic runner
**Status:** raw M0 diagnostic values written; endpoint verdict remains blocked

Script:

```text
scripts/run_endpoint_scoring_runner.py
```

Derived outputs:

```text
data/derived/endpoint_scoring_runner_v01.csv
data/derived/endpoint_scoring_runner_summary_v01.csv
```

This runner is the first numeric post-preflight artifact. It joins the frozen
M0 prediction rows with imported SPARC observed velocity rows by galaxy and
radial index, then writes per-galaxy raw adequacy diagnostics.

The diagnostic formula is:

```text
raw_m0_adequacy_diagnostic =
  chi2_full_raw + 0.5 * chi2_inner_raw + 0.5 * chi2_outer_raw
  + parsimony_penalty_raw
```

where each chi2 term is the mean of `((v_obs - v_pred) / sigma_v)^2` on the
declared radial region. The inner and outer regions use the first and last
third of the sorted radial rows. The current M0 parsimony penalty is read from
the frozen numeric parameter-count table.

## Claim Boundary

This artifact does not compare M0 against M1 or M2, does not execute controls,
does not claim any control pass, does not authorize endpoint scoring, and does
not make a dark-sector necessity verdict. The word "runner" names the scaffold
that can compute raw diagnostics after preflight; it is not an endpoint verdict.
