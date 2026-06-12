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
data/input/leakage_audit_evidence_v10_TEMPLATE.csv
data/input/leakage_audit_evidence_v10.csv
data/derived/leakage_audit_evidence_template_summary_v58.csv
review_packages/leakage_audit_v58_review_package/
review_packages/leakage_audit_v58_review_package.zip
review_packages/leakage_audit_v58_completed_review_response/
review_packages/leakage_audit_v58_completed_review_response.zip
data/derived/leakage_audit_review_response_intake_v60.csv
data/derived/leakage_audit_review_response_intake_summary_v60.csv
data/derived/leakage_prescore_artifact_work_order_v61.csv
data/derived/leakage_prescore_artifact_work_order_coverage_v61.csv
data/derived/leakage_prescore_artifact_work_order_summary_v61.csv
review_packages/leakage_prescore_artifact_v61_collection_package/
review_packages/leakage_prescore_artifact_v61_collection_package.zip
review_packages/leakage_prescore_artifact_v61_completed_collection_response/
review_packages/leakage_prescore_artifact_v61_completed_collection_response.zip
data/derived/leakage_prescore_artifact_collection_intake_v63.csv
data/derived/leakage_prescore_artifact_collection_intake_summary_v63.csv
data/derived/leakage_prescore_artifact_request_ledger_v64.csv
data/derived/leakage_prescore_artifact_request_coverage_v64.csv
data/derived/leakage_prescore_artifact_request_summary_v64.csv
review_packages/leakage_prescore_artifact_request_v64_review_package/
review_packages/leakage_prescore_artifact_request_v64_review_package.zip
review_packages/leakage_prescore_artifact_request_v64_completed_review_response/
review_packages/leakage_prescore_artifact_request_v64_completed_review_response.zip
data/derived/leakage_prescore_artifact_request_review_intake_v66.csv
data/derived/leakage_prescore_artifact_request_review_intake_summary_v66.csv
data/derived/leakage_prescore_artifact_candidate_ledger_v67.csv
data/derived/leakage_prescore_artifact_candidate_coverage_v67.csv
data/derived/leakage_prescore_artifact_candidate_summary_v67.csv
review_packages/leakage_prescore_artifact_candidate_v67_review_package/
review_packages/leakage_prescore_artifact_candidate_v67_review_package.zip
review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response/
review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response.zip
data/derived/leakage_prescore_artifact_candidate_review_intake_v69.csv
data/derived/leakage_prescore_artifact_candidate_review_intake_summary_v69.csv
data/derived/leakage_evidence_candidate_ingestion_gate_v70.csv
data/derived/leakage_evidence_candidate_ingestion_coverage_v70.csv
data/derived/leakage_evidence_candidate_ingestion_summary_v70.csv
data/derived/leakage_partial_candidate_sufficiency_policy_v71.csv
data/derived/leakage_partial_candidate_sufficiency_policy_summary_v71.csv
review_packages/leakage_partial_candidate_sufficiency_v71_review_package/
review_packages/leakage_partial_candidate_sufficiency_v71_review_package.zip
review_packages/leakage_partial_candidate_sufficiency_v71_completed_review_response/
review_packages/leakage_partial_candidate_sufficiency_v71_completed_review_response.zip
data/derived/leakage_partial_candidate_sufficiency_review_intake_v73.csv
data/derived/leakage_partial_candidate_sufficiency_review_intake_summary_v73.csv
data/derived/leakage_partial_candidate_sufficiency_preaudit_v74.csv
data/derived/leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv
data/derived/leakage_partial_candidate_sufficiency_response_draft_summary_v75.csv
data/derived/full_leakage_evidence_ingestion_gate_v76.csv
data/derived/full_leakage_evidence_ingestion_coverage_v76.csv
data/derived/full_leakage_evidence_ingestion_summary_v76.csv
data/derived/leakage_audit_evidence_v10_writer_coverage_v77.csv
data/derived/leakage_audit_evidence_v10_writer_summary_v77.csv
data/derived/leakage_audit_pass_review_gate_v78.csv
data/derived/leakage_audit_pass_review_coverage_v78.csv
data/derived/leakage_audit_pass_review_summary_v78.csv
review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package/
review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package.zip
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
data/input/source_import_raw_sparc_like_v15.csv
data/derived/active_v15_raw_sparc_like_input_writer_summary_v56.csv
data/input/source_import_real_values_write_authorization_v57.csv
data/derived/active_v12_real_values_write_authorization_summary_v57.csv
data/input/source_import_real_values_v12.csv
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
data/derived/scoring_dependency_closure_v24.csv
data/derived/scoring_dependency_closure_summary_v24.csv
data/derived/scoring_unblock_priority_v25.csv
data/derived/scoring_unblock_priority_summary_v25.csv
data/derived/scoring_frontier_status_v72.csv
data/derived/scoring_frontier_status_summary_v72.csv
data/derived/frontier_provenance_evidence_acceptance_v26.csv
data/derived/frontier_provenance_evidence_acceptance_summary_v26.csv
data/derived/frontier_provenance_evidence_work_order_v27.csv
data/derived/frontier_provenance_evidence_work_order_summary_v27.csv
data/derived/frontier_work_order_completion_gate_v28.csv
data/derived/frontier_work_order_completion_gate_summary_v28.csv
data/derived/frontier_evidence_write_authorization_v29.csv
data/derived/frontier_evidence_write_authorization_summary_v29.csv
data/derived/frontier_authorized_evidence_writer_v30.csv
data/derived/frontier_authorized_evidence_writer_summary_v30.csv
data/derived/frontier_post_writer_evidence_absence_audit_v31.csv
data/derived/frontier_post_writer_evidence_absence_audit_summary_v31.csv
data/derived/post_writer_evidence_gate_recheck_v32.csv
data/derived/post_writer_evidence_gate_recheck_summary_v32.csv
data/derived/post_writer_provenance_promotion_recheck_v33.csv
data/derived/post_writer_provenance_promotion_recheck_summary_v33.csv
data/derived/post_writer_raw_import_recheck_v34.csv
data/derived/post_writer_raw_import_recheck_summary_v34.csv
data/derived/post_writer_raw_adapter_recheck_v35.csv
data/derived/post_writer_raw_adapter_recheck_summary_v35.csv
data/derived/post_writer_real_values_gate_recheck_v36.csv
data/derived/post_writer_real_values_gate_recheck_summary_v36.csv
data/derived/post_writer_leakage_audit_recheck_v37.csv
data/derived/post_writer_leakage_audit_recheck_summary_v37.csv
data/derived/post_writer_scoring_activation_recheck_v38.csv
data/derived/post_writer_scoring_activation_recheck_summary_v38.csv
data/derived/post_writer_scoring_preflight_recheck_v39.csv
data/derived/post_writer_scoring_preflight_recheck_summary_v39.csv
data/derived/post_writer_scoring_dependency_closure_recheck_v40.csv
data/derived/post_writer_scoring_dependency_closure_recheck_summary_v40.csv
data/derived/post_writer_scoring_unblock_priority_recheck_v41.csv
data/derived/post_writer_scoring_unblock_priority_recheck_summary_v41.csv
data/derived/post_writer_frontier_evidence_acceptance_recheck_v42.csv
data/derived/post_writer_frontier_evidence_acceptance_recheck_summary_v42.csv
data/derived/post_writer_frontier_work_order_recheck_v43.csv
data/derived/post_writer_frontier_work_order_recheck_summary_v43.csv
data/derived/frontier_provenance_evidence_intake_contract_v44.csv
data/derived/frontier_provenance_evidence_intake_checklist_v44.csv
data/derived/frontier_provenance_evidence_intake_contract_summary_v44.csv
data/derived/frontier_provenance_source_candidate_ledger_v45.csv
data/derived/frontier_provenance_source_candidate_coverage_v45.csv
data/derived/frontier_provenance_source_candidate_ledger_summary_v45.csv
data/derived/frontier_provenance_evidence_payload_draft_v46.csv
data/derived/frontier_provenance_evidence_payload_draft_review_v46.csv
data/derived/frontier_provenance_evidence_payload_draft_summary_v46.csv
review_packages/frontier_provenance_v46_review_package/
review_packages/frontier_provenance_v46_review_package.zip
review_packages/frontier_provenance_v46_completed_review_response/
review_packages/frontier_provenance_v46_completed_review_response.zip
data/derived/frontier_provenance_review_response_intake_v48.csv
data/derived/frontier_provenance_review_response_intake_summary_v48.csv
data/derived/frontier_review_promotion_gate_v49.csv
data/derived/frontier_review_promotion_gate_summary_v49.csv
data/external/sparc_hash_audit_v50/
data/derived/frontier_external_hash_recompute_audit_v50.csv
data/derived/frontier_external_hash_recompute_audit_summary_v50.csv
data/derived/post_hash_frontier_review_promotion_recheck_v51.csv
data/derived/post_hash_frontier_review_promotion_recheck_summary_v51.csv
review_packages/frontier_post_hash_review_promotion_v51_review_package/
review_packages/frontier_post_hash_review_promotion_v51_review_package.zip
review_packages/frontier_post_hash_review_promotion_v51_completed_review_response/
review_packages/frontier_post_hash_review_promotion_v51_completed_review_response.zip
data/derived/post_hash_review_promotion_response_intake_v53.csv
data/derived/post_hash_review_promotion_response_intake_summary_v53.csv
data/derived/authorized_provenance_evidence_payload_v54.csv
data/derived/authorized_provenance_evidence_payload_summary_v54.csv
data/input/source_import_provenance_evidence_v21.csv
data/derived/active_v21_provenance_evidence_writer_summary_v55.csv
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
docs/leakage_audit_evidence_template_v58.md
docs/leakage_audit_review_package_v59.md
docs/leakage_audit_review_response_intake_v60.md
docs/leakage_prescore_artifact_work_order_v61.md
docs/leakage_prescore_artifact_collection_package_v62.md
docs/leakage_prescore_artifact_collection_intake_v63.md
docs/leakage_prescore_artifact_request_ledger_v64.md
docs/leakage_prescore_artifact_request_review_package_v65.md
docs/leakage_prescore_artifact_request_review_intake_v66.md
docs/leakage_prescore_artifact_candidate_ledger_v67.md
docs/leakage_prescore_artifact_candidate_review_package_v68.md
docs/leakage_prescore_artifact_candidate_review_intake_v69.md
docs/leakage_evidence_candidate_ingestion_gate_v70.md
docs/leakage_partial_candidate_sufficiency_review_package_v71.md
docs/leakage_partial_candidate_sufficiency_review_intake_v73.md
docs/leakage_partial_candidate_sufficiency_preaudit_v74.md
docs/leakage_partial_candidate_sufficiency_response_draft_v75.md
docs/full_leakage_evidence_ingestion_gate_v76.md
docs/leakage_audit_evidence_v10_writer_v77.md
docs/leakage_audit_pass_review_gate_v78.md
docs/source_import_values_v11.md
docs/source_import_real_values_gate_v12.md
docs/scoring_activation_gate_v13.md
docs/source_import_real_values_template_v14.md
docs/source_import_raw_adapter_v15.md
docs/active_v15_raw_sparc_like_input_writer_v56.md
docs/active_v12_real_values_write_authorization_v57.md
docs/source_import_write_authorization_v16.md
docs/source_import_authorized_writer_v17.md
docs/source_import_raw_template_v18.md
docs/source_import_provenance_manifest_v19.md
docs/source_import_provenance_audit_v20.md
docs/source_import_provenance_template_v21.md
docs/source_import_provenance_evidence_gate_v22.md
docs/source_import_provenance_promotion_gate_v23.md
docs/scoring_dependency_closure_v24.md
docs/scoring_unblock_priority_v25.md
docs/scoring_frontier_status_v72.md
docs/frontier_provenance_evidence_acceptance_v26.md
docs/frontier_provenance_evidence_work_order_v27.md
docs/frontier_work_order_completion_gate_v28.md
docs/frontier_evidence_write_authorization_v29.md
docs/frontier_authorized_evidence_writer_v30.md
docs/frontier_post_writer_evidence_absence_audit_v31.md
docs/post_writer_evidence_gate_recheck_v32.md
docs/post_writer_provenance_promotion_recheck_v33.md
docs/post_writer_raw_import_recheck_v34.md
docs/post_writer_raw_adapter_recheck_v35.md
docs/post_writer_real_values_gate_recheck_v36.md
docs/post_writer_leakage_audit_recheck_v37.md
docs/post_writer_scoring_activation_recheck_v38.md
docs/post_writer_scoring_preflight_recheck_v39.md
docs/post_writer_scoring_dependency_closure_recheck_v40.md
docs/post_writer_scoring_unblock_priority_recheck_v41.md
docs/post_writer_frontier_evidence_acceptance_recheck_v42.md
docs/post_writer_frontier_work_order_recheck_v43.md
docs/frontier_provenance_evidence_intake_contract_v44.md
docs/frontier_provenance_source_candidate_ledger_v45.md
docs/frontier_provenance_evidence_payload_draft_v46.md
docs/frontier_provenance_review_package_v47.md
docs/frontier_provenance_review_response_intake_v48.md
docs/frontier_review_promotion_gate_v49.md
docs/frontier_external_hash_recompute_audit_v50.md
docs/post_hash_frontier_review_promotion_recheck_v51.md
docs/post_hash_review_promotion_package_v52.md
docs/post_hash_review_promotion_response_intake_v53.md
docs/authorized_provenance_evidence_payload_v54.md
docs/active_v21_provenance_evidence_writer_v55.md
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
and numeric-count readiness ledgers. The next target is leakage audit, concrete
family formula tables, numeric parameter counts, and executable control
runners, not a response formula or physical readout claim. The v06 readiness
audit is executable and currently reports `ENDPOINT_SCORING_BLOCKED`. The v07
scoring preflight is also executable and currently reports `SCORING_NOT_READY`.
The v08 scoring-input scaffold declares the scoring row and observed-input
table shapes, but activates no rows.

The active source-side chain is now explicit. The active v21 input is present
via v55. With that input in place, v22 reports
`PROVENANCE_EVIDENCE_READY_FOR_PROMOTION`, v23 promotes all eighteen provenance
rows, and v20 reports `RAW_IMPORT_READY_BY_PROVENANCE`. The v56 active raw
SPARC-like input writer extracts 450 MassModels rows for the eighteen frozen
galaxies into `data/input/source_import_raw_sparc_like_v15.csv`. The v57
authorization records an explicit permission to write v12 real values from that
active v15 raw input. The v16 gate reports `WRITE_AUTHORIZATION_READY`, the v17
authorized writer writes 450 rows into
`data/input/source_import_real_values_v12.csv`, and the v12 real-value gate
reports `SOURCE_IMPORT_REAL_VALUES_READY_FOR_LEAKAGE`.

The v09 source-import/leakage audit now reports
`SOURCE_IMPORT_AND_LEAKAGE_READY`: source-side values, the v10 leakage-evidence
input, and the v78 leakage-pass review are present, but zero rows are
activated. The v13 scoring activation gate remains blocked with zero activated
rows. The v24 scoring dependency closure now has eight ready source-side
dependencies and five blocked downstream dependencies. The v25 scoring unblock
priority ledger identifies the first current frontier as
`SCD24_ROW_ACTIVATION`, with
`activated_scoring_rows_v10_or_activation_policy_after_leakage_pass` as the
next required artifact.
The legacy v26-v30 frontier-provenance work-order/writer path remains
review-only and write-blocked; it does not override the separate active v55
writer. The v31 audit records the active v55 provenance input as present, v32
allows evidence-gate promotion, v33 promotes all eighteen provenance rows on
recheck, and v34 allows raw import in principle while importing zero raw rows.
The v35 post-writer raw adapter recheck still records that the adapter itself
does not write v12, while the packaged v12 input may exist after the authorized
writer. The v36 recheck sees the real-value gate as ready, v37 confirms the
leakage pass after recheck, and v38-v39 keep scoring activation and preflight
blocked. The v40 recheck keeps all endpoint-scoring paths blocked because
preflight readiness is still zero, and v41 confirms the current frontier as
`SCD24_ROW_ACTIVATION`. The v42-v43 frontier-evidence rechecks remain
blocked/bypassed with respect to scoring because the active frontier is no
longer provenance evidence. The v44 frontier
provenance evidence intake contract defines nine review rules and eighteen
manual collection checklist rows for the missing provenance evidence input,
while creating zero evidence rows by itself. The v45 frontier provenance source
candidate ledger records SPARC Table1 and MassModels source candidates and
identifies candidate source rows for all eighteen frozen galaxies, while still
creating zero v21 evidence rows. The v46 frontier provenance evidence payload
draft converts those candidates into eighteen review-required draft rows with
the v21 column shape, while still writing zero v21 evidence rows. The v47
frontier provenance review package bundles the v44-v46 review artifacts into a
handoff directory and zip without creating active v21 evidence. The v48
frontier provenance review-response intake records the completed review
response as draft-only, with eighteen route/prescore passes,
`PASS_WITH_CAVEAT`, zero complete evidence rows authorized, and zero v21
evidence rows created. The v49 frontier review-promotion gate checks whether
that response can promote rows into active v21 provenance evidence. It blocks
all eighteen rows because the external SPARC hash was not independently
recomputed and the response did not explicitly authorize v21 copy or provenance
completion. The v50 external hash recompute audit closes the hash caveat by
matching both cached SPARC source files against the v45 ledger. The v51
post-hash promotion recheck then narrows the remaining block to explicit review
promotion authorization: all eighteen rows have primary hash support, but zero
rows may write v21 evidence or activate scoring. The v52 post-hash review
promotion package bundles the v46, v48, v49, v50, and v51 artifacts plus a
fillable authorization template for the next human review decision; it remains
review-only and does not create v21 evidence or allow scoring. The v53 completed
authorization response intake accepts all eighteen rows for later ingestion,
with v21 copy and provenance-complete authorization set to true while endpoint
scoring remains false. The v54 authorized provenance evidence payload converts
that authorization into an eighteen-row `PROVENANCE_EVIDENCE_COMPLETE` payload
under `data/derived/`; it is ready for a separate active v21 write gate but is
not yet active source input. The v55 active v21 provenance evidence writer
writes all eighteen complete provenance rows into
`data/input/source_import_provenance_evidence_v21.csv`. After rerunning the
source-side gates, v22, v23, and v20 are ready. The v56 active raw SPARC-like
input writer then writes 450 MassModels raw rows for the eighteen frozen
galaxies into `data/input/source_import_raw_sparc_like_v15.csv`. The scoring
unblock frontier moves to the leakage-pass review gate after v10 evidence;
endpoint scoring remains disabled. The v58 leakage-evidence template provides the 72-row
review shape for that frontier but creates zero leakage-pass rows. The v59
leakage review package bundles that template, contract, frontier summaries,
and a fillable response template; it is not active leakage evidence and still
creates zero activation/scoring rows. The v60 completed-review intake records
the received response as `NO_GO_EVIDENCE_REQUIRED_NOT_FILLED`: 72 no-go rows,
zero leakage-pass rows, zero activation rows, and no endpoint scoring. The v61
work order converts that no-go into 72 concrete prescore artifact tasks across
the four leakage checks; all remain open and non-scoring. The v62 collection
package turns those tasks into a fillable prescore artifact response template,
while still creating zero leakage evidence, zero activation rows, and zero
endpoint scores. The v63 intake gate records the completed v62 response as a
no-go response: it is present and readable, but provides zero reviewed prescore
artifact identifiers or hash/accession values. All 72 rows remain blocked.
The v64 request ledger converts those blocked rows into explicit row-level
requests with minimal required fields and forbidden endpoint-derived inputs.
The v65 review package turns that ledger into a fillable response template for
reviewed prescore artifact URI/id and hash/accession collection.
The v66 intake records the completed v65 response as present but blocked:
it supplies zero reviewed prescore artifacts and creates zero leakage-evidence
candidates.
The v67 candidate ledger maps all 72 open requests to existing repository
candidate artifacts for review. Source-route and observed-input candidates are
identified, while morphology-label and benchmark-policy candidates remain
partial; all rows still require review before leakage evidence can be created.
The v68 candidate review package turns those candidates into a fillable review
handoff; it remains review-only and creates zero leakage-evidence rows.
The v69 intake records the completed candidate review response: 36 full
source-route and observed-input candidates are accepted only for a later
leakage-evidence ingestion gate, while 36 partial morphology-label and
benchmark-policy candidates remain blocked. It creates zero active leakage
evidence rows, zero activation rows, and zero endpoint scoring rows.
The v70 ingestion gate converts those 36 accepted rows into draft evidence
candidates only. Since the morphology-label and benchmark-policy evidence
components remain blocked, no full four-component leakage pass is available;
the gate writes zero target evidence rows and still permits zero endpoint
scoring rows.
The v71 partial-candidate sufficiency policy fixes the scoring-facing minimum:
all four leakage components are required before endpoint scoring. It packages
the 36 blocked morphology-label and benchmark-policy rows for separate
sufficiency review, while creating zero evidence rows, zero activation rows,
and zero endpoint scores.
The v72 scoring-frontier status refines the next scoring blocker after v71:
the completed v71 sufficiency response is now ingested, so the first required
artifact moves to full leakage-evidence ingestion, followed only then by
activation recheck. It remains status-only and non-scoring.
The v73 sufficiency-response intake installs that first frontier as an
executable gate. The completed v71 response accepts all 36 partial sufficiency
rows for later leakage-evidence ingestion, but creates zero evidence rows, zero
leakage pass, zero activation rows, and zero scores.
The v74 preaudit checks those 36 partial rows against the local source/policy
manifests and marks all 36 as review-ready but not accepted. It is a reviewer
aid only: zero sufficiency rows are accepted and scoring remains disabled.
The v75 response-draft package turns the v74 preaudit into a proposed v71
sufficiency response for independent review. It proposes 36 accept rows, but it
is explicitly not a completed response and cannot be ingested or scored without
separate review.
The v76 full leakage-evidence ingestion gate combines the accepted v70
source/observed candidates with the accepted v73 morphology/benchmark
sufficiency rows. It marks 72 component rows and all 18 galaxies as ready for a
later v10 target evidence writer, while still creating zero target evidence
rows, zero leakage pass, zero activation rows, and zero scores.
The v77 leakage-audit evidence writer then writes
`data/input/leakage_audit_evidence_v10.csv` with 72 review-pending evidence
rows. It still authorizes zero leakage-pass rows, zero activation rows, and
zero endpoint scores. The v78 leakage-audit pass review gate authorizes all 72
component passes and all 18 galaxy-level leakage passes, but still authorizes
zero activation rows and zero endpoint scores; the next blocker is row
activation.
