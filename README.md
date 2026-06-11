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
data/derived/source_import_and_leakage_audit_v09.csv
data/derived/source_import_requirements_v09.csv
data/derived/leakage_audit_findings_v09.csv
data/derived/source_import_leakage_summary_v09.csv
data/derived/source_import_table_v10.csv
data/derived/observed_input_contract_v10.csv
data/derived/leakage_evidence_contract_v10.csv
data/derived/source_import_contract_summary_v10.csv
data/derived/source_import_values_v11.csv
data/derived/observed_numeric_values_v11.csv
data/derived/leakage_evidence_values_v11.csv
data/derived/source_import_values_summary_v11.csv
data/derived/source_import_real_values_schema_v12.csv
data/derived/source_import_real_values_gate_v12.csv
data/derived/source_import_real_values_summary_v12.csv
data/derived/scoring_activation_gate_v13.csv
data/derived/scoring_activation_global_blockers_v13.csv
data/derived/scoring_activation_summary_v13.csv
data/input/source_import_real_values_v12_TEMPLATE.csv
data/derived/source_import_template_columns_v14.csv
data/derived/source_import_template_summary_v14.csv
data/derived/source_import_raw_adapter_schema_v15.csv
data/derived/source_import_raw_adapter_gate_v15.csv
data/derived/source_import_raw_adapter_summary_v15.csv
data/derived/source_import_write_authorization_v16.csv
data/derived/source_import_write_authorization_summary_v16.csv
data/derived/source_import_authorized_writer_v17.csv
data/derived/source_import_authorized_writer_summary_v17.csv
data/input/source_import_raw_sparc_like_v15_TEMPLATE.csv
data/derived/source_import_raw_template_columns_v18.csv
data/derived/source_import_raw_template_summary_v18.csv
data/derived/source_import_provenance_manifest_v19.csv
data/derived/source_import_provenance_columns_v19.csv
data/derived/source_import_provenance_summary_v19.csv
data/derived/source_import_provenance_audit_v20.csv
data/derived/source_import_provenance_audit_summary_v20.csv
data/input/source_import_provenance_evidence_v21_TEMPLATE.csv
data/derived/source_import_provenance_template_columns_v21.csv
data/derived/source_import_provenance_template_summary_v21.csv
data/derived/source_import_provenance_evidence_gate_v22.csv
data/derived/source_import_provenance_evidence_gate_summary_v22.csv
data/derived/source_import_provenance_promotion_gate_v23.csv
data/derived/source_import_provenance_promotion_summary_v23.csv
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
docs/source_import_leakage_audit_v09.md
docs/source_import_contract_v10.md
docs/source_import_values_v11.md
docs/source_import_real_values_gate_v12.md
docs/scoring_activation_gate_v13.md
docs/source_import_real_values_template_v14.md
docs/source_import_raw_adapter_v15.md
docs/source_import_write_authorization_v16.md
docs/source_import_authorized_writer_v17.md
docs/source_import_raw_template_v18.md
docs/source_import_provenance_manifest_v19.md
docs/source_import_provenance_audit_v20.md
docs/source_import_provenance_template_v21.md
docs/source_import_provenance_evidence_gate_v22.md
docs/source_import_provenance_promotion_gate_v23.md
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
numeric data. The v09 source-import/leakage audit currently reports
`SOURCE_IMPORT_AND_LEAKAGE_BLOCKED`. The v10 source-import contract is present,
but all source routes, observed numeric values, and leakage evidence are still
unfilled. The v11 value ledger exists, and every value remains
`VALUE_REQUIRED_NOT_FILLED`. The v12 real-value import gate is executable and
currently reports `SOURCE_IMPORT_REAL_VALUES_BLOCKED`, because the package does
not yet include `data/input/source_import_real_values_v12.csv`. The v13 scoring
activation gate is also executable and currently reports
`SCORING_ACTIVATION_BLOCKED`: zero rows are activated, and formula tables,
numeric counts, controls, and thresholds remain blocked. The v14 source-import
template is present as `data/input/source_import_real_values_v12_TEMPLATE.csv`,
but it is not data and cannot activate scoring rows. The v15 raw adapter
declares a machine-readable path from a SPARC-like raw input into the v12 real
input shape, and currently reports `RAW_ADAPTER_READY_INPUT_MISSING`. The v16
write-authorization gate currently reports `WRITE_AUTHORIZATION_BLOCKED`, so no
real v12 input file is written. The v17 authorized writer path is implemented
but currently reports `AUTHORIZED_WRITER_BLOCKED` and writes zero rows. The v18
raw-input template is present as `data/input/source_import_raw_sparc_like_v15_TEMPLATE.csv`,
but it is not data and cannot be used for scoring. The v19 provenance manifest
currently reports `PROVENANCE_REQUIRED_NOT_FILLED`, so raw import remains
blocked before any observed value can enter the scoring path. The v20
provenance audit currently reports `RAW_IMPORT_BLOCKED_BY_PROVENANCE`. The v21
provenance evidence template is present, but it is not evidence and cannot
allow raw import. The v22 provenance evidence gate currently reports
`PROVENANCE_EVIDENCE_INPUT_MISSING`, so provenance promotion remains blocked.
The v23 provenance promotion gate makes that downstream block explicit:
`PROVENANCE_PROMOTION_BLOCKED`, zero provenance rows are promoted, and no
source import or scoring path is activated.
