# Tau Core Galaxy Dark-Sector Decision Paper 11

This repository is the initial private scaffold for Paper 11:

**A source-frozen decision protocol for dark-sector necessity in Tau Core galaxy rotation**

The paper is designed as a narrow decision protocol built on Paper 10-style
freeze discipline and Paper 9/10 galaxy-readout experience. It asks whether
galaxy-rotation endpoints require a dark-sector response layer, or whether a
no-dark Tau morphology/readout endpoint can remain sufficient under held-out
tests and wrong-family controls.

## Main Claim

The repository defines a reproducible decision scaffold for comparing three
model families:

```text
M0: no-dark Tau morphology/readout endpoint
M1: Tau base-substrate / Tau dark-sector response endpoint
M2: standard dark-sector benchmark endpoint
```

The decision is galaxy-scope only and must be made from source-frozen inputs,
held-out endpoint tests, and controls that prevent residual leakage.

## Does Not Claim

- It does not claim that dark matter does not exist.
- It does not claim that Tau Core replaces the standard dark sector.
- It does not claim that a Tau dark-sector response field has been proved.
- It does not claim a `Response_tau` formula.
- It does not claim lensing, CMB, BAO, supernova, growth, or cosmological validation.
- It does not claim a galaxy-rotation endpoint result.

## Included Data

Only compact protocol manifests are included:

```text
data/source_manifest/model_family_decision_protocol.csv
data/source_manifest/policy_bundle_freeze_requirements.csv
data/source_manifest/decision_outcome_ladder.csv
data/source_manifest/frozen_policy_bundle_instance_v01.csv
data/source_manifest/galaxy_decision_endpoint_manifest_v01.csv
data/source_manifest/galaxy_sample_freeze_v01.csv
data/source_manifest/scoring_rule_freeze_v01.csv
data/source_manifest/control_manifest_v01.csv
data/source_manifest/decision_threshold_v01.csv
data/source_manifest/galaxy_list_freeze_v02.csv
data/source_manifest/scoring_formula_freeze_v02.csv
data/source_manifest/family_parameter_count_freeze_v03.csv
data/source_manifest/control_implementation_freeze_v03.csv
data/source_manifest/source_field_completeness_v04.csv
data/source_manifest/family_formula_registry_v04.csv
data/source_manifest/control_runner_contract_v04.csv
data/source_manifest/source_row_audit_v05.csv
data/source_manifest/family_formula_table_v05.csv
data/source_manifest/numeric_count_readiness_v05.csv
data/derived/activation_blockers_v06.csv
data/derived/formula_and_count_blockers_v06.csv
data/derived/control_runner_blockers_v06.csv
data/derived/readiness_summary_v06.csv
data/derived/scoring_input_requirements_v07.csv
data/derived/scoring_formula_components_v07.csv
data/derived/scoring_preflight_summary_v07.csv
data/derived/activated_scoring_rows_v08.csv
data/derived/scoring_observed_input_schema_v08.csv
data/derived/scoring_observed_inputs_v08.csv
data/derived/scoring_input_scaffold_summary_v08.csv
```

These are source-side decision artifacts. They contain no endpoint residuals
and no fitted galaxy results.

The first frozen-reference bundle is:

```text
docs/frozen_policy_bundle_instance_v01.md
```

The first galaxy decision endpoint manifest is:

```text
docs/galaxy_decision_endpoint_manifest_v01.md
```

The first pre-registration manifests are:

```text
docs/galaxy_sample_freeze_v01.md
docs/scoring_rule_freeze_v01.md
docs/control_manifest_v01.md
docs/decision_threshold_v01.md
docs/galaxy_list_freeze_v02.md
docs/scoring_formula_freeze_v02.md
docs/family_parameter_count_freeze_v03.md
docs/control_implementation_freeze_v03.md
docs/source_field_completeness_v04.md
docs/family_formula_registry_v04.md
docs/control_runner_contract_v04.md
docs/source_row_audit_v05.md
docs/family_formula_table_v05.md
docs/numeric_count_readiness_v05.md
docs/readiness_audit_v06.md
docs/scoring_preflight_v07.md
docs/scoring_input_scaffold_v08.md
```

## Reproduce

```bash
python scripts/reproduce.py
```

The reproduction script validates the protocol manifests, compiles the
manuscript with `tectonic`, builds `arxiv_submission_source.zip`, and runs
pytest smoke tests.

## arXiv Source Package

`arxiv_submission_source.zip` is generated from `paper11_submission_source/`
and excludes `main.pdf` plus TeX build byproducts.

## Scope

Paper 11 should remain a decision paper:

```text
Paper 10 provides galaxy-readout and freeze-method foundations.
Paper 11 compares no-dark, Tau dark-sector response, and standard dark-sector
benchmark families under the same endpoint-blind decision protocol.
```

The current honest status is a frozen-reference policy bundle, v01
sample/scoring/control/threshold pre-registration, v02 galaxy-role plus
scoring-formula freeze, and v03 family-budget plus control-implementation
freeze, plus v04 source-field, formula-registry, and control-runner contracts.
It also includes v05 row-level source-audit, family formula-table readiness,
and numeric-count readiness ledgers. The next target is source import, leakage
audit, concrete family formula tables, numeric parameter counts, and executable
control runners, not a response formula or physical readout claim. The v06
readiness audit is executable and currently reports `ENDPOINT_SCORING_BLOCKED`.
The v07 scoring preflight is also executable and currently reports
`SCORING_NOT_READY`. The v08 scoring-input scaffold declares the scoring row
and observed-input table shapes, but activates no rows and imports no observed
numeric data.
