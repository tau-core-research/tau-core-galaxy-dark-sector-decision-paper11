# Control Runner Outputs v08

**Doc class:** control-runner output-contract scaffold
**Status:** control output contracts ready; no control results or scores written
**Canonical parent:** Control runner contract v04

Script:

```text
scripts/build_control_runner_outputs.py
```

Derived outputs:

```text
data/derived/control_runner_outputs_v08.csv
data/derived/control_runner_outputs_summary_v08.csv
```

This artifact closes the global control-runner output-contract blocker without
claiming that numerical control runs have been executed. It materializes the
six declared control output contracts from `control_runner_contract_v04.csv`
as run-ready output-contract rows.

No shuffled-label, wrong-family, null-source, leakage, radial, parity, endpoint,
or family-comparison scores are written here.

The next required artifact is:

```text
numeric_decision_thresholds_v08.csv
```

## Claim Boundary

This artifact writes control output-contract rows only. It writes no control result rows,
computes no control scores, authorizes no endpoint scoring, compares no families,
and makes no dark-sector verdict.

Claim boundary:

```text
control_runner_outputs_v08_contract_only_no_control_results_no_scores_no_verdict
```
