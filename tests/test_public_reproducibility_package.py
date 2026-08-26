from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_4d_subfamily_remains_blocked() -> None:
    tex = (ROOT / "paper11_submission_source/main.tex").read_text()
    assert "Blocked Full-4D Readout Subfamily" in tex
    assert "This subfamily is blocked" in tex
    assert "changes no activation row, family score, or decision status" in tex


def test_required_files_exist() -> None:
    required = [
        "README.md",
        "DATA_NOTICE.md",
        "CITATION.cff",
        "LICENSE",
        "paper11_submission_source/main.tex",
        "paper11_submission_source/refs.bib",
        "docs/frozen_policy_bundle_instance_v01.md",
        "docs/galaxy_decision_endpoint_manifest_v01.md",
        "docs/galaxy_sample_freeze_v01.md",
        "docs/scoring_rule_freeze_v01.md",
        "docs/control_manifest_v01.md",
        "docs/decision_threshold_v01.md",
        "docs/galaxy_list_freeze_v02.md",
        "docs/scoring_formula_freeze_v02.md",
        "docs/family_parameter_count_freeze_v03.md",
        "docs/control_implementation_freeze_v03.md",
        "docs/source_field_completeness_v04.md",
        "docs/family_formula_registry_v04.md",
        "docs/control_runner_contract_v04.md",
        "docs/source_row_audit_v05.md",
        "docs/family_formula_table_v05.md",
        "docs/numeric_count_readiness_v05.md",
        "docs/readiness_audit_v06.md",
        "docs/scoring_preflight_v07.md",
        "docs/scoring_input_scaffold_v08.md",
        "docs/source_import_leakage_audit_v09.md",
        "docs/source_import_contract_v10.md",
        "docs/leakage_audit_evidence_template_v58.md",
        "docs/leakage_audit_review_package_v59.md",
        "docs/leakage_audit_review_response_intake_v60.md",
        "docs/leakage_prescore_artifact_work_order_v61.md",
        "docs/leakage_prescore_artifact_collection_package_v62.md",
        "docs/leakage_prescore_artifact_collection_intake_v63.md",
        "docs/leakage_prescore_artifact_request_ledger_v64.md",
        "docs/leakage_prescore_artifact_request_review_package_v65.md",
        "docs/leakage_prescore_artifact_request_review_intake_v66.md",
        "docs/leakage_prescore_artifact_candidate_ledger_v67.md",
        "docs/leakage_prescore_artifact_candidate_review_package_v68.md",
        "docs/leakage_prescore_artifact_candidate_review_intake_v69.md",
        "docs/leakage_evidence_candidate_ingestion_gate_v70.md",
        "docs/leakage_partial_candidate_sufficiency_review_package_v71.md",
        "docs/leakage_partial_candidate_sufficiency_review_intake_v73.md",
        "docs/leakage_partial_candidate_sufficiency_preaudit_v74.md",
        "docs/leakage_partial_candidate_sufficiency_response_draft_v75.md",
        "docs/full_leakage_evidence_ingestion_gate_v76.md",
        "docs/leakage_audit_evidence_v10_writer_v77.md",
        "docs/leakage_audit_pass_review_gate_v78.md",
        "docs/scoring_row_activation_policy_v79.md",
        "docs/m0_no_dark_rule_parent_assumption_basis_v14.md",
        "docs/m0_no_dark_rule_selection_map_v14.md",
        "docs/m0_no_dark_rule_term_generation_record_v14.md",
        "docs/m0_no_dark_rule_invariance_null_checks_v14.md",
        "docs/m0_no_dark_rule_dimensional_precheck_v14.md",
        "docs/m0_no_dark_rule_derivation_provenance_leakage_v14.md",
        "docs/m0_no_dark_expression_source_basis_v13.md",
        "docs/m0_no_dark_expression_admissibility_rule_v13.md",
        "docs/m0_no_dark_expression_null_fallback_policy_v13.md",
        "docs/m0_no_dark_expression_output_class_v13.md",
        "docs/m0_no_dark_expression_source_rule_leakage_audit_v13.md",
        "docs/m0_no_dark_expression_symbolic_form_v12.md",
        "docs/m0_no_dark_expression_input_domain_v12.md",
        "docs/m0_no_dark_expression_coefficient_freeze_v12.md",
        "docs/m0_no_dark_expression_dimensional_audit_v12.md",
        "docs/m0_no_dark_expression_machine_form_v12.md",
        "docs/m0_no_dark_expression_rule_derivation_contract_v13.md",
        "docs/m0_no_dark_expression_source_rule_contract_v12.md",
        "docs/m0_no_dark_frozen_expression_contract_v11.md",
        "docs/m0_no_dark_kernel_expression_contract_v10.md",
        "docs/m0_no_dark_kernel_expression_interface_v10.md",
        "docs/m0_no_dark_frozen_expression_payload_v11.md",
        "docs/m0_no_dark_frozen_expression_statement_v12.md",
        "docs/m0_no_dark_source_side_expression_statement_v13.md",
        "docs/m0_no_dark_statement_term_list_v13.md",
        "docs/m0_no_dark_statement_argument_signature_v13.md",
        "docs/m0_no_dark_statement_constraint_guards_v13.md",
        "docs/m0_no_dark_statement_pre_dimensional_proof_v13.md",
        "docs/m0_no_dark_statement_freeze_provenance_v13.md",
        "docs/m0_no_dark_payload_symbol_binding_table_v12.md",
        "docs/m0_no_dark_payload_constant_policy_v12.md",
        "docs/m0_no_dark_payload_dimensional_trace_v12.md",
        "docs/m0_no_dark_payload_machine_form_v12.md",
        "docs/m0_no_dark_payload_leakage_certificate_v12.md",
        "docs/m0_no_dark_frozen_expression_body_v14.md",
        "docs/m0_no_dark_equation_kernel_contract_v09.md",
        "docs/m0_no_dark_equation_kernel_interface_v09.md",
        "docs/m0_no_dark_readout_equation_contract_v08.md",
        "docs/m0_no_dark_readout_equation_interface_v08.md",
        "docs/m0_no_dark_formula_body_interface_v08.md",
        "docs/m0_no_dark_formula_table_contract_v06.md",
        "docs/m0_no_dark_formula_body_contract_v07.md",
        "docs/m0_no_dark_coefficient_policy_v07.md",
        "docs/m0_no_dark_scale_policy_v07.md",
        "docs/m0_no_dark_fallback_policy_v07.md",
        "docs/family_prediction_tables_v08.md",
        "docs/family_prediction_comparability_v09.md",
        "docs/m0_no_dark_prediction_row_writer_v08.md",
        "docs/m0_no_dark_executable_prediction_kernel_v08.md",
        "docs/m0_no_dark_velocity_readout_formula_v08.md",
        "docs/m0_no_dark_source_to_rotation_equation_body_v08.md",
        "docs/m0_no_dark_source_to_velocity_coupling_rule_v08.md",
        "docs/m0_no_dark_velocity_unit_lift_rule_v08.md",
        "docs/m0_no_dark_velocity_dimension_anchor_rule_v08.md",
        "docs/m0_no_dark_velocity_anchor_source_law_v08.md",
        "docs/m0_no_dark_velocity_anchor_candidate_basis_v08.md",
        "docs/m0_no_dark_velocity_anchor_selection_rule_v08.md",
        "docs/m0_no_dark_velocity_anchor_value_freeze_v08.md",
        "docs/m0_no_dark_velocity_anchor_unit_normalization_v08.md",
        "docs/m0_no_dark_velocity_anchor_component_combination_rule_v08.md",
        "docs/m0_no_dark_velocity_anchor_component_weight_policy_v08.md",
        "docs/m0_no_dark_velocity_anchor_component_weight_value_freeze_v08.md",
        "docs/m0_no_dark_velocity_anchor_combined_anchor_rule_v08.md",
        "docs/m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08.md",
        "docs/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08.md",
        "docs/m0_no_dark_velocity_readout_formula_body_freeze_v08.md",
        "docs/m0_no_dark_prediction_row_value_freeze_v08.md",
        "docs/m0_no_dark_family_prediction_row_emission_v08.md",
        "docs/m0_label_rule_table_v06.md",
        "docs/m1_tau_response_formula_table_v06.md",
        "docs/m1_admissibility_table_v06.md",
        "docs/m1_response_parameter_inventory_v10.md",
        "docs/m1_response_parameter_count_classification_v11.md",
        "docs/m1_response_parameter_count_value_ledger_v12.md",
        "docs/m1_response_parameter_adjustable_slot_resolution_v13.md",
        "docs/m1_response_parameter_final_count_candidate_v14.md",
        "docs/m1_response_parameter_final_count_freeze_v15.md",
        "docs/m1_per_galaxy_response_privilege_count_audit_v10.md",
        "docs/m1_per_galaxy_response_privilege_count_freeze_v11.md",
        "docs/m2_benchmark_parameter_inventory_v10.md",
        "docs/m2_benchmark_parameter_count_classification_v11.md",
        "docs/m2_benchmark_parameter_count_value_ledger_v12.md",
        "docs/m2_benchmark_parameter_adjustable_slot_resolution_v13.md",
        "docs/m2_benchmark_parameter_final_count_candidate_v14.md",
        "docs/m2_benchmark_parameter_final_count_freeze_v15.md",
        "docs/m2_per_galaxy_benchmark_privilege_count_audit_v10.md",
        "docs/m2_per_galaxy_benchmark_privilege_count_freeze_v11.md",
        "docs/m2_benchmark_profile_table_v06.md",
        "docs/m2_nuisance_policy_table_v06.md",
        "docs/shared_scoring_input_table_v06.md",
        "docs/shared_input_count_discount_policy_v10.md",
        "docs/numeric_parameter_count_table_v06.md",
        "docs/numeric_parameter_count_table_v08.md",
        "docs/numeric_parameter_count_table_final_values_v10.md",
        "docs/control_runner_outputs_v08.md",
        "docs/control_execution_readiness_v09.md",
        "docs/endpoint_scoring_runner_v01.md",
        "docs/numeric_decision_thresholds_v08.md",
        "docs/m0_global_parameter_inventory_v10.md",
        "docs/m0_global_parameter_count_classification_v11.md",
        "docs/m0_global_parameter_count_value_ledger_v12.md",
        "docs/m0_global_adjustable_slot_resolution_v13.md",
        "docs/m0_global_final_count_candidate_v14.md",
        "docs/m0_global_final_count_freeze_v15.md",
        "docs/m0_per_galaxy_privilege_count_audit_v10.md",
        "docs/m0_per_galaxy_privilege_count_freeze_v11.md",
        "docs/numeric_count_readiness_closure_v09.md",
        "docs/family_prediction_table_contract_v80.md",
        "docs/family_prediction_frontier_trace_v81.md",
        "docs/source_import_values_v11.md",
        "docs/source_import_real_values_gate_v12.md",
        "docs/scoring_activation_gate_v13.md",
        "docs/source_import_real_values_template_v14.md",
        "docs/source_import_raw_adapter_v15.md",
        "docs/active_v15_raw_sparc_like_input_writer_v56.md",
        "docs/active_v12_real_values_write_authorization_v57.md",
        "docs/source_import_write_authorization_v16.md",
        "docs/source_import_authorized_writer_v17.md",
        "docs/source_import_raw_template_v18.md",
        "docs/source_import_provenance_manifest_v19.md",
        "docs/source_import_provenance_audit_v20.md",
        "docs/source_import_provenance_template_v21.md",
        "docs/source_import_provenance_evidence_gate_v22.md",
        "docs/source_import_provenance_promotion_gate_v23.md",
        "docs/scoring_dependency_closure_v24.md",
        "docs/scoring_unblock_priority_v25.md",
        "docs/scoring_frontier_status_v72.md",
        "docs/theory_side_scoring_anchor_v81.md",
        "docs/upstream_results_scoring_impact_v82.md",
        "docs/frontier_provenance_evidence_acceptance_v26.md",
        "docs/frontier_provenance_evidence_work_order_v27.md",
        "docs/frontier_work_order_completion_gate_v28.md",
        "docs/frontier_evidence_write_authorization_v29.md",
        "docs/frontier_authorized_evidence_writer_v30.md",
        "docs/frontier_post_writer_evidence_absence_audit_v31.md",
        "docs/post_writer_evidence_gate_recheck_v32.md",
        "docs/post_writer_provenance_promotion_recheck_v33.md",
        "docs/post_writer_raw_import_recheck_v34.md",
        "docs/post_writer_raw_adapter_recheck_v35.md",
        "docs/post_writer_real_values_gate_recheck_v36.md",
        "docs/post_writer_leakage_audit_recheck_v37.md",
        "docs/post_writer_scoring_activation_recheck_v38.md",
        "docs/post_writer_scoring_preflight_recheck_v39.md",
        "docs/post_writer_scoring_dependency_closure_recheck_v40.md",
        "docs/post_writer_scoring_unblock_priority_recheck_v41.md",
        "docs/post_writer_frontier_evidence_acceptance_recheck_v42.md",
        "docs/post_writer_frontier_work_order_recheck_v43.md",
        "docs/frontier_provenance_evidence_intake_contract_v44.md",
        "docs/frontier_provenance_source_candidate_ledger_v45.md",
        "docs/frontier_provenance_evidence_payload_draft_v46.md",
        "docs/frontier_provenance_review_package_v47.md",
        "docs/frontier_provenance_review_response_intake_v48.md",
        "docs/frontier_review_promotion_gate_v49.md",
        "docs/frontier_external_hash_recompute_audit_v50.md",
        "docs/post_hash_frontier_review_promotion_recheck_v51.md",
        "docs/post_hash_review_promotion_package_v52.md",
        "docs/post_hash_review_promotion_response_intake_v53.md",
        "docs/authorized_provenance_evidence_payload_v54.md",
        "docs/active_v21_provenance_evidence_writer_v55.md",
        "data/derived/activation_blockers_v06.csv",
        "data/derived/formula_and_count_blockers_v06.csv",
        "data/derived/control_runner_blockers_v06.csv",
        "data/derived/readiness_summary_v06.csv",
        "data/derived/scoring_input_requirements_v07.csv",
        "data/derived/scoring_formula_components_v07.csv",
        "data/derived/scoring_preflight_summary_v07.csv",
        "data/derived/activated_scoring_rows_v08.csv",
        "data/derived/scoring_observed_input_schema_v08.csv",
        "data/derived/scoring_observed_inputs_v08.csv",
        "data/derived/scoring_input_scaffold_summary_v08.csv",
        "data/derived/source_import_and_leakage_audit_v09.csv",
        "data/derived/source_import_requirements_v09.csv",
        "data/derived/leakage_audit_findings_v09.csv",
        "data/derived/source_import_leakage_summary_v09.csv",
        "data/derived/source_import_table_v10.csv",
        "data/derived/observed_input_contract_v10.csv",
        "data/derived/leakage_evidence_contract_v10.csv",
        "data/derived/source_import_contract_summary_v10.csv",
        "data/input/leakage_audit_evidence_v10_TEMPLATE.csv",
        "data/input/leakage_audit_evidence_v10.csv",
        "data/derived/leakage_audit_evidence_template_summary_v58.csv",
        "review_packages/leakage_audit_v58_review_package/README.md",
        "review_packages/leakage_audit_v58_review_package/DO_NOT_COPY_WITHOUT_COMPLETED_REVIEW.md",
        "review_packages/leakage_audit_v58_review_package/REVIEW_MANIFEST.csv",
        "review_packages/leakage_audit_v58_review_package/templates/leakage_audit_evidence_v10_TEMPLATE.csv",
        "review_packages/leakage_audit_v58_review_package/templates/leakage_audit_review_response_TEMPLATE.csv",
        "review_packages/leakage_audit_v58_review_package/data/leakage_audit_evidence_template_summary_v58.csv",
        "review_packages/leakage_audit_v58_review_package/data/leakage_evidence_contract_v10.csv",
        "review_packages/leakage_audit_v58_review_package/data/source_import_leakage_summary_v09.csv",
        "review_packages/leakage_audit_v58_review_package/data/source_import_real_values_summary_v12.csv",
        "review_packages/leakage_audit_v58_review_package/data/scoring_unblock_priority_summary_v25.csv",
        "review_packages/leakage_audit_v58_review_package.zip",
        "review_packages/leakage_audit_v58_completed_review_response.zip",
        "review_packages/leakage_audit_v58_completed_review_response/leakage_audit_v58_review_response.csv",
        "review_packages/leakage_audit_v58_completed_review_response/leakage_audit_v58_review_completed_summary.csv",
        "review_packages/leakage_audit_v58_completed_review_response/leakage_audit_v58_review_notes.md",
        "review_packages/leakage_audit_v58_completed_review_response/leakage_audit_v58_review_validation_log.txt",
        "data/derived/leakage_audit_review_response_intake_v60.csv",
        "data/derived/leakage_audit_review_response_intake_summary_v60.csv",
        "data/derived/leakage_prescore_artifact_work_order_v61.csv",
        "data/derived/leakage_prescore_artifact_work_order_coverage_v61.csv",
        "data/derived/leakage_prescore_artifact_work_order_summary_v61.csv",
        "review_packages/leakage_prescore_artifact_v61_collection_package/README.md",
        "review_packages/leakage_prescore_artifact_v61_collection_package/DO_NOT_COPY_WITHOUT_COMPLETED_ARTIFACT_REVIEW.md",
        "review_packages/leakage_prescore_artifact_v61_collection_package/REVIEW_MANIFEST.csv",
        "review_packages/leakage_prescore_artifact_v61_collection_package/data/leakage_prescore_artifact_work_order_v61.csv",
        "review_packages/leakage_prescore_artifact_v61_collection_package/data/leakage_prescore_artifact_work_order_coverage_v61.csv",
        "review_packages/leakage_prescore_artifact_v61_collection_package/data/leakage_prescore_artifact_work_order_summary_v61.csv",
        "review_packages/leakage_prescore_artifact_v61_collection_package/data/leakage_audit_review_response_intake_summary_v60.csv",
        "review_packages/leakage_prescore_artifact_v61_collection_package/data/leakage_audit_evidence_template_summary_v58.csv",
        "review_packages/leakage_prescore_artifact_v61_collection_package/templates/leakage_prescore_artifact_collection_response_TEMPLATE.csv",
        "review_packages/leakage_prescore_artifact_v61_collection_package.zip",
        "review_packages/leakage_prescore_artifact_v61_completed_collection_response.zip",
        "review_packages/leakage_prescore_artifact_v61_completed_collection_response/leakage_prescore_artifact_v61_collection_response.csv",
        "review_packages/leakage_prescore_artifact_v61_completed_collection_response/leakage_prescore_artifact_v61_collection_completed_summary.csv",
        "review_packages/leakage_prescore_artifact_v61_completed_collection_response/leakage_prescore_artifact_v61_collection_notes.md",
        "review_packages/leakage_prescore_artifact_v61_completed_collection_response/leakage_prescore_artifact_v61_collection_validation_log.txt",
        "data/derived/leakage_prescore_artifact_collection_intake_v63.csv",
        "data/derived/leakage_prescore_artifact_collection_intake_summary_v63.csv",
        "data/derived/leakage_prescore_artifact_request_ledger_v64.csv",
        "data/derived/leakage_prescore_artifact_request_coverage_v64.csv",
        "data/derived/leakage_prescore_artifact_request_summary_v64.csv",
        "review_packages/leakage_prescore_artifact_request_v64_review_package/README.md",
        "review_packages/leakage_prescore_artifact_request_v64_review_package/DO_NOT_COPY_WITHOUT_COMPLETED_REQUEST_REVIEW.md",
        "review_packages/leakage_prescore_artifact_request_v64_review_package/REVIEW_MANIFEST.csv",
        "review_packages/leakage_prescore_artifact_request_v64_review_package/data/leakage_prescore_artifact_request_ledger_v64.csv",
        "review_packages/leakage_prescore_artifact_request_v64_review_package/data/leakage_prescore_artifact_request_coverage_v64.csv",
        "review_packages/leakage_prescore_artifact_request_v64_review_package/data/leakage_prescore_artifact_request_summary_v64.csv",
        "review_packages/leakage_prescore_artifact_request_v64_review_package/data/leakage_prescore_artifact_collection_intake_summary_v63.csv",
        "review_packages/leakage_prescore_artifact_request_v64_review_package/templates/leakage_prescore_artifact_request_review_response_TEMPLATE.csv",
        "review_packages/leakage_prescore_artifact_request_v64_review_package.zip",
        "review_packages/leakage_prescore_artifact_request_v64_completed_review_response.zip",
        "review_packages/leakage_prescore_artifact_request_v64_completed_review_response/leakage_prescore_artifact_request_v64_review_response.csv",
        "review_packages/leakage_prescore_artifact_request_v64_completed_review_response/leakage_prescore_artifact_request_v64_review_completed_summary.csv",
        "review_packages/leakage_prescore_artifact_request_v64_completed_review_response/leakage_prescore_artifact_request_v64_review_notes.md",
        "review_packages/leakage_prescore_artifact_request_v64_completed_review_response/leakage_prescore_artifact_request_v64_review_validation_log.txt",
        "data/derived/leakage_prescore_artifact_request_review_intake_v66.csv",
        "data/derived/leakage_prescore_artifact_request_review_intake_summary_v66.csv",
        "data/derived/leakage_prescore_artifact_candidate_ledger_v67.csv",
        "data/derived/leakage_prescore_artifact_candidate_coverage_v67.csv",
        "data/derived/leakage_prescore_artifact_candidate_summary_v67.csv",
        "review_packages/leakage_prescore_artifact_candidate_v67_review_package/README.md",
        "review_packages/leakage_prescore_artifact_candidate_v67_review_package/DO_NOT_COPY_WITHOUT_COMPLETED_CANDIDATE_REVIEW.md",
        "review_packages/leakage_prescore_artifact_candidate_v67_review_package/REVIEW_MANIFEST.csv",
        "review_packages/leakage_prescore_artifact_candidate_v67_review_package/data/leakage_prescore_artifact_candidate_ledger_v67.csv",
        "review_packages/leakage_prescore_artifact_candidate_v67_review_package/data/leakage_prescore_artifact_candidate_coverage_v67.csv",
        "review_packages/leakage_prescore_artifact_candidate_v67_review_package/data/leakage_prescore_artifact_candidate_summary_v67.csv",
        "review_packages/leakage_prescore_artifact_candidate_v67_review_package/data/leakage_prescore_artifact_request_review_intake_summary_v66.csv",
        "review_packages/leakage_prescore_artifact_candidate_v67_review_package/templates/leakage_prescore_artifact_candidate_review_response_TEMPLATE.csv",
        "review_packages/leakage_prescore_artifact_candidate_v67_review_package.zip",
        "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response.zip",
        "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response/leakage_prescore_artifact_candidate_v67_review_response.csv",
        "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response/leakage_prescore_artifact_candidate_v67_review_completed_summary.csv",
        "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response/leakage_prescore_artifact_candidate_v67_review_notes.md",
        "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response/leakage_prescore_artifact_candidate_v67_review_validation_log.txt",
        "data/derived/leakage_prescore_artifact_candidate_review_intake_v69.csv",
        "data/derived/leakage_prescore_artifact_candidate_review_intake_summary_v69.csv",
        "data/derived/leakage_evidence_candidate_ingestion_gate_v70.csv",
        "data/derived/leakage_evidence_candidate_ingestion_coverage_v70.csv",
        "data/derived/leakage_evidence_candidate_ingestion_summary_v70.csv",
        "data/derived/leakage_partial_candidate_sufficiency_policy_v71.csv",
        "data/derived/leakage_partial_candidate_sufficiency_policy_summary_v71.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v71_review_package/README.md",
        "review_packages/leakage_partial_candidate_sufficiency_v71_review_package/DO_NOT_COPY_WITHOUT_COMPLETED_SUFFICIENCY_REVIEW.md",
        "review_packages/leakage_partial_candidate_sufficiency_v71_review_package/REVIEW_MANIFEST.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v71_review_package/data/leakage_evidence_candidate_ingestion_gate_v70.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v71_review_package/data/leakage_evidence_candidate_ingestion_coverage_v70.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v71_review_package/data/leakage_evidence_candidate_ingestion_summary_v70.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v71_review_package/data/leakage_partial_candidate_sufficiency_policy_v71.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v71_review_package/data/leakage_partial_candidate_sufficiency_policy_summary_v71.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v71_review_package/templates/leakage_partial_candidate_sufficiency_v71_review_response_TEMPLATE.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v71_review_package.zip",
        "review_packages/leakage_partial_candidate_sufficiency_v71_completed_review_response/leakage_partial_candidate_sufficiency_v71_review_response.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v71_completed_review_response/leakage_partial_candidate_sufficiency_v71_completed_review_summary.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v71_completed_review_response/leakage_partial_candidate_sufficiency_v71_review_notes.md",
        "review_packages/leakage_partial_candidate_sufficiency_v71_completed_review_response/leakage_partial_candidate_sufficiency_v71_validation_log.txt",
        "review_packages/leakage_partial_candidate_sufficiency_v71_completed_review_response.zip",
        "data/derived/leakage_partial_candidate_sufficiency_review_intake_v73.csv",
        "data/derived/leakage_partial_candidate_sufficiency_review_intake_summary_v73.csv",
        "data/derived/leakage_partial_candidate_sufficiency_preaudit_v74.csv",
        "data/derived/leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv",
        "data/derived/leakage_partial_candidate_sufficiency_response_draft_summary_v75.csv",
        "data/derived/full_leakage_evidence_ingestion_gate_v76.csv",
        "data/derived/full_leakage_evidence_ingestion_coverage_v76.csv",
        "data/derived/full_leakage_evidence_ingestion_summary_v76.csv",
        "data/derived/leakage_audit_evidence_v10_writer_coverage_v77.csv",
        "data/derived/leakage_audit_evidence_v10_writer_summary_v77.csv",
        "data/derived/leakage_audit_pass_review_gate_v78.csv",
        "data/derived/leakage_audit_pass_review_coverage_v78.csv",
        "data/derived/leakage_audit_pass_review_summary_v78.csv",
        "data/derived/activated_scoring_rows_v10.csv",
        "data/derived/scoring_row_activation_policy_summary_v79.csv",
        "data/derived/m0_no_dark_rule_parent_assumption_basis_v14.csv",
        "data/derived/m0_no_dark_rule_parent_assumption_basis_summary_v14.csv",
        "data/derived/m0_no_dark_rule_selection_map_v14.csv",
        "data/derived/m0_no_dark_rule_selection_map_summary_v14.csv",
        "data/derived/m0_no_dark_rule_term_generation_record_v14.csv",
        "data/derived/m0_no_dark_rule_term_generation_record_summary_v14.csv",
        "data/derived/m0_no_dark_rule_invariance_null_checks_v14.csv",
        "data/derived/m0_no_dark_rule_invariance_null_checks_summary_v14.csv",
        "data/derived/m0_no_dark_rule_dimensional_precheck_v14.csv",
        "data/derived/m0_no_dark_rule_dimensional_precheck_summary_v14.csv",
        "data/derived/m0_no_dark_rule_derivation_provenance_leakage_v14.csv",
        "data/derived/m0_no_dark_rule_derivation_provenance_leakage_summary_v14.csv",
        "data/derived/m0_no_dark_expression_source_basis_v13.csv",
        "data/derived/m0_no_dark_expression_source_basis_summary_v13.csv",
        "data/derived/m0_no_dark_expression_admissibility_rule_v13.csv",
        "data/derived/m0_no_dark_expression_admissibility_rule_summary_v13.csv",
        "data/derived/m0_no_dark_expression_null_fallback_policy_v13.csv",
        "data/derived/m0_no_dark_expression_null_fallback_policy_summary_v13.csv",
        "data/derived/m0_no_dark_expression_output_class_v13.csv",
        "data/derived/m0_no_dark_expression_output_class_summary_v13.csv",
        "data/derived/m0_no_dark_expression_source_rule_leakage_audit_v13.csv",
        "data/derived/m0_no_dark_expression_source_rule_leakage_audit_summary_v13.csv",
        "data/derived/m0_no_dark_expression_symbolic_form_v12.csv",
        "data/derived/m0_no_dark_expression_symbolic_form_summary_v12.csv",
        "data/derived/m0_no_dark_expression_input_domain_v12.csv",
        "data/derived/m0_no_dark_expression_input_domain_summary_v12.csv",
        "data/derived/m0_no_dark_expression_coefficient_freeze_v12.csv",
        "data/derived/m0_no_dark_expression_coefficient_freeze_summary_v12.csv",
        "data/derived/m0_no_dark_expression_dimensional_audit_v12.csv",
        "data/derived/m0_no_dark_expression_dimensional_audit_summary_v12.csv",
        "data/derived/m0_no_dark_expression_machine_form_v12.csv",
        "data/derived/m0_no_dark_expression_machine_form_summary_v12.csv",
        "data/derived/m0_no_dark_equation_kernel_interface_v09.csv",
        "data/derived/m0_no_dark_equation_kernel_interface_summary_v09.csv",
        "data/derived/m0_no_dark_equation_kernel_contract_v09.csv",
        "data/derived/m0_no_dark_equation_kernel_contract_summary_v09.csv",
        "data/derived/m0_no_dark_readout_equation_contract_v08.csv",
        "data/derived/m0_no_dark_readout_equation_contract_summary_v08.csv",
        "data/derived/m0_no_dark_readout_equation_interface_v08.csv",
        "data/derived/m0_no_dark_readout_equation_interface_summary_v08.csv",
        "data/derived/m0_no_dark_formula_body_interface_v08.csv",
        "data/derived/m0_no_dark_formula_body_interface_summary_v08.csv",
        "data/derived/m0_no_dark_formula_body_contract_v07.csv",
        "data/derived/m0_no_dark_formula_body_contract_summary_v07.csv",
        "data/derived/m0_no_dark_formula_table_contract_v06.csv",
        "data/derived/m0_no_dark_formula_table_contract_summary_v06.csv",
        "data/derived/family_prediction_table_schema_v80.csv",
        "data/derived/family_prediction_table_slot_requirements_v80.csv",
        "data/derived/family_prediction_table_contract_summary_v80.csv",
        "data/derived/family_prediction_frontier_trace_v81.csv",
        "data/derived/family_prediction_frontier_trace_summary_v81.csv",
        "data/derived/m0_no_dark_coefficient_policy_v07.csv",
        "data/derived/m0_no_dark_coefficient_policy_summary_v07.csv",
        "data/derived/m0_no_dark_scale_policy_v07.csv",
        "data/derived/m0_no_dark_scale_policy_summary_v07.csv",
        "data/derived/m0_no_dark_fallback_policy_v07.csv",
        "data/derived/m0_no_dark_fallback_policy_summary_v07.csv",
        "data/derived/family_prediction_tables_v08.csv",
        "data/derived/family_prediction_tables_summary_v08.csv",
        "data/derived/family_prediction_comparability_v09.csv",
        "data/derived/family_prediction_comparability_summary_v09.csv",
        "data/derived/m0_no_dark_prediction_row_writer_v08.csv",
        "data/derived/m0_no_dark_prediction_row_writer_summary_v08.csv",
        "data/derived/m0_no_dark_executable_prediction_kernel_v08.csv",
        "data/derived/m0_no_dark_executable_prediction_kernel_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_readout_formula_v08.csv",
        "data/derived/m0_no_dark_velocity_readout_formula_summary_v08.csv",
        "data/derived/m0_no_dark_source_to_rotation_equation_body_v08.csv",
        "data/derived/m0_no_dark_source_to_rotation_equation_body_summary_v08.csv",
        "data/derived/m0_no_dark_source_to_velocity_coupling_rule_v08.csv",
        "data/derived/m0_no_dark_source_to_velocity_coupling_rule_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_unit_lift_rule_v08.csv",
        "data/derived/m0_no_dark_velocity_unit_lift_rule_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_dimension_anchor_rule_v08.csv",
        "data/derived/m0_no_dark_velocity_dimension_anchor_rule_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_source_law_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_source_law_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_candidate_basis_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_candidate_basis_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_selection_rule_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_selection_rule_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_value_freeze_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_value_freeze_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_unit_normalization_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_unit_normalization_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_component_combination_rule_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_component_combination_rule_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_component_weight_policy_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_component_weight_policy_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_component_weight_value_freeze_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_component_weight_value_freeze_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_combined_anchor_rule_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_combined_anchor_rule_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08.csv",
        "data/derived/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_summary_v08.csv",
        "data/derived/m0_no_dark_velocity_readout_formula_body_freeze_v08.csv",
        "data/derived/m0_no_dark_velocity_readout_formula_body_freeze_summary_v08.csv",
        "data/derived/m0_no_dark_prediction_row_value_freeze_v08.csv",
        "data/derived/m0_no_dark_prediction_row_value_freeze_summary_v08.csv",
        "data/derived/m0_no_dark_family_prediction_row_emission_v08.csv",
        "data/derived/m0_no_dark_family_prediction_row_emission_summary_v08.csv",
        "data/derived/m0_label_rule_table_v06.csv",
        "data/derived/m0_label_rule_table_summary_v06.csv",
        "data/derived/m1_tau_response_formula_table_v06.csv",
        "data/derived/m1_tau_response_formula_table_summary_v06.csv",
        "data/derived/m1_admissibility_table_v06.csv",
        "data/derived/m1_admissibility_table_summary_v06.csv",
        "data/derived/m1_response_parameter_inventory_v10.csv",
        "data/derived/m1_response_parameter_inventory_summary_v10.csv",
        "data/derived/m1_response_parameter_count_classification_v11.csv",
        "data/derived/m1_response_parameter_count_classification_summary_v11.csv",
        "data/derived/m1_response_parameter_count_value_ledger_v12.csv",
        "data/derived/m1_response_parameter_count_value_ledger_summary_v12.csv",
        "data/derived/m1_response_parameter_adjustable_slot_resolution_v13.csv",
        "data/derived/m1_response_parameter_adjustable_slot_resolution_summary_v13.csv",
        "data/derived/m1_response_parameter_final_count_candidate_v14.csv",
        "data/derived/m1_response_parameter_final_count_candidate_summary_v14.csv",
        "data/derived/m1_response_parameter_final_count_freeze_v15.csv",
        "data/derived/m1_response_parameter_final_count_freeze_summary_v15.csv",
        "data/derived/m1_per_galaxy_response_privilege_count_audit_v10.csv",
        "data/derived/m1_per_galaxy_response_privilege_count_audit_summary_v10.csv",
        "data/derived/m1_per_galaxy_response_privilege_count_freeze_v11.csv",
        "data/derived/m1_per_galaxy_response_privilege_count_freeze_summary_v11.csv",
        "data/derived/m2_benchmark_parameter_inventory_v10.csv",
        "data/derived/m2_benchmark_parameter_inventory_summary_v10.csv",
        "data/derived/m2_benchmark_parameter_count_classification_v11.csv",
        "data/derived/m2_benchmark_parameter_count_classification_summary_v11.csv",
        "data/derived/m2_benchmark_parameter_count_value_ledger_v12.csv",
        "data/derived/m2_benchmark_parameter_count_value_ledger_summary_v12.csv",
        "data/derived/m2_benchmark_profile_table_v06.csv",
        "data/derived/m2_benchmark_profile_table_summary_v06.csv",
        "data/derived/m2_nuisance_policy_table_v06.csv",
        "data/derived/m2_nuisance_policy_table_summary_v06.csv",
        "data/derived/shared_scoring_input_table_v06.csv",
        "data/derived/shared_scoring_input_table_summary_v06.csv",
        "data/derived/numeric_parameter_count_table_v06.csv",
        "data/derived/numeric_parameter_count_table_summary_v06.csv",
        "data/derived/numeric_parameter_count_table_v08.csv",
        "data/derived/numeric_parameter_count_table_summary_v08.csv",
        "data/derived/m0_global_parameter_inventory_v10.csv",
        "data/derived/m0_global_parameter_inventory_summary_v10.csv",
        "data/derived/m0_global_parameter_count_classification_v11.csv",
        "data/derived/m0_global_parameter_count_classification_summary_v11.csv",
        "data/derived/m0_global_parameter_count_value_ledger_v12.csv",
        "data/derived/m0_global_parameter_count_value_ledger_summary_v12.csv",
        "data/derived/m0_global_adjustable_slot_resolution_v13.csv",
        "data/derived/m0_global_adjustable_slot_resolution_summary_v13.csv",
        "data/derived/m0_global_final_count_candidate_v14.csv",
        "data/derived/m0_global_final_count_candidate_summary_v14.csv",
        "data/derived/m0_global_final_count_freeze_v15.csv",
        "data/derived/m0_global_final_count_freeze_summary_v15.csv",
        "data/derived/m0_per_galaxy_privilege_count_audit_v10.csv",
        "data/derived/m0_per_galaxy_privilege_count_audit_summary_v10.csv",
        "data/derived/m0_per_galaxy_privilege_count_freeze_v11.csv",
        "data/derived/m0_per_galaxy_privilege_count_freeze_summary_v11.csv",
        "data/derived/m2_benchmark_parameter_adjustable_slot_resolution_v13.csv",
        "data/derived/m2_benchmark_parameter_adjustable_slot_resolution_summary_v13.csv",
        "data/derived/m2_benchmark_parameter_final_count_candidate_v14.csv",
        "data/derived/m2_benchmark_parameter_final_count_candidate_summary_v14.csv",
        "data/derived/m2_benchmark_parameter_final_count_freeze_v15.csv",
        "data/derived/m2_benchmark_parameter_final_count_freeze_summary_v15.csv",
        "data/derived/m2_per_galaxy_benchmark_privilege_count_audit_v10.csv",
        "data/derived/m2_per_galaxy_benchmark_privilege_count_audit_summary_v10.csv",
        "data/derived/m2_per_galaxy_benchmark_privilege_count_freeze_v11.csv",
        "data/derived/m2_per_galaxy_benchmark_privilege_count_freeze_summary_v11.csv",
        "data/derived/shared_input_count_discount_policy_v10.csv",
        "data/derived/shared_input_count_discount_policy_summary_v10.csv",
        "data/derived/numeric_parameter_count_table_final_values_v10.csv",
        "data/derived/numeric_parameter_count_table_final_values_summary_v10.csv",
        "data/derived/control_runner_outputs_v08.csv",
        "data/derived/control_runner_outputs_summary_v08.csv",
        "data/derived/control_execution_readiness_v09.csv",
        "data/derived/control_execution_readiness_summary_v09.csv",
        "data/derived/endpoint_scoring_runner_v01.csv",
        "data/derived/endpoint_scoring_runner_summary_v01.csv",
        "data/derived/numeric_decision_thresholds_v08.csv",
        "data/derived/numeric_decision_thresholds_summary_v08.csv",
        "data/derived/numeric_count_readiness_closure_v09.csv",
        "data/derived/numeric_count_readiness_closure_summary_v09.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package/README.md",
        "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package/DO_NOT_INGEST_WITHOUT_INDEPENDENT_REVIEW.md",
        "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package/REVIEW_MANIFEST.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package/templates/leakage_partial_candidate_sufficiency_v71_review_response_DRAFT.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package/data/leakage_partial_candidate_sufficiency_response_draft_summary_v75.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package/data/leakage_partial_candidate_sufficiency_preaudit_v74.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package/data/leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv",
        "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package.zip",
        "data/derived/source_import_values_v11.csv",
        "data/derived/observed_numeric_values_v11.csv",
        "data/derived/leakage_evidence_values_v11.csv",
        "data/derived/source_import_values_summary_v11.csv",
        "data/derived/source_import_real_values_schema_v12.csv",
        "data/derived/source_import_real_values_gate_v12.csv",
        "data/derived/source_import_real_values_summary_v12.csv",
        "data/derived/scoring_activation_gate_v13.csv",
        "data/derived/scoring_activation_global_blockers_v13.csv",
        "data/derived/scoring_activation_summary_v13.csv",
        "data/input/source_import_real_values_v12_TEMPLATE.csv",
        "data/derived/source_import_template_columns_v14.csv",
        "data/derived/source_import_template_summary_v14.csv",
        "data/derived/source_import_raw_adapter_schema_v15.csv",
        "data/derived/source_import_raw_adapter_gate_v15.csv",
        "data/derived/source_import_raw_adapter_summary_v15.csv",
        "data/input/source_import_raw_sparc_like_v15.csv",
        "data/derived/active_v15_raw_sparc_like_input_writer_summary_v56.csv",
        "data/input/source_import_real_values_write_authorization_v57.csv",
        "data/derived/active_v12_real_values_write_authorization_summary_v57.csv",
        "data/input/source_import_real_values_v12.csv",
        "data/derived/source_import_write_authorization_v16.csv",
        "data/derived/source_import_write_authorization_summary_v16.csv",
        "data/derived/source_import_authorized_writer_v17.csv",
        "data/derived/source_import_authorized_writer_summary_v17.csv",
        "data/input/source_import_raw_sparc_like_v15_TEMPLATE.csv",
        "data/derived/source_import_raw_template_columns_v18.csv",
        "data/derived/source_import_raw_template_summary_v18.csv",
        "data/derived/source_import_provenance_manifest_v19.csv",
        "data/derived/source_import_provenance_columns_v19.csv",
        "data/derived/source_import_provenance_summary_v19.csv",
        "data/derived/source_import_provenance_audit_v20.csv",
        "data/derived/source_import_provenance_audit_summary_v20.csv",
        "data/input/source_import_provenance_evidence_v21_TEMPLATE.csv",
        "data/derived/source_import_provenance_template_columns_v21.csv",
        "data/derived/source_import_provenance_template_summary_v21.csv",
        "data/derived/source_import_provenance_evidence_gate_v22.csv",
        "data/derived/source_import_provenance_evidence_gate_summary_v22.csv",
        "data/derived/source_import_provenance_promotion_gate_v23.csv",
        "data/derived/source_import_provenance_promotion_summary_v23.csv",
        "data/derived/scoring_dependency_closure_v24.csv",
        "data/derived/scoring_dependency_closure_summary_v24.csv",
        "data/derived/scoring_unblock_priority_v25.csv",
        "data/derived/scoring_unblock_priority_summary_v25.csv",
        "data/derived/scoring_frontier_status_v72.csv",
        "data/derived/scoring_frontier_status_summary_v72.csv",
        "data/derived/frontier_provenance_evidence_acceptance_v26.csv",
        "data/derived/frontier_provenance_evidence_acceptance_summary_v26.csv",
        "data/derived/frontier_provenance_evidence_work_order_v27.csv",
        "data/derived/frontier_provenance_evidence_work_order_summary_v27.csv",
        "data/derived/frontier_work_order_completion_gate_v28.csv",
        "data/derived/frontier_work_order_completion_gate_summary_v28.csv",
        "data/derived/frontier_evidence_write_authorization_v29.csv",
        "data/derived/frontier_evidence_write_authorization_summary_v29.csv",
        "data/derived/frontier_authorized_evidence_writer_v30.csv",
        "data/derived/frontier_authorized_evidence_writer_summary_v30.csv",
        "data/derived/frontier_post_writer_evidence_absence_audit_v31.csv",
        "data/derived/frontier_post_writer_evidence_absence_audit_summary_v31.csv",
        "data/derived/post_writer_evidence_gate_recheck_v32.csv",
        "data/derived/post_writer_evidence_gate_recheck_summary_v32.csv",
        "data/derived/post_writer_provenance_promotion_recheck_v33.csv",
        "data/derived/post_writer_provenance_promotion_recheck_summary_v33.csv",
        "data/derived/post_writer_raw_import_recheck_v34.csv",
        "data/derived/post_writer_raw_import_recheck_summary_v34.csv",
        "data/derived/post_writer_raw_adapter_recheck_v35.csv",
        "data/derived/post_writer_raw_adapter_recheck_summary_v35.csv",
        "data/derived/post_writer_real_values_gate_recheck_v36.csv",
        "data/derived/post_writer_real_values_gate_recheck_summary_v36.csv",
        "data/derived/post_writer_leakage_audit_recheck_v37.csv",
        "data/derived/post_writer_leakage_audit_recheck_summary_v37.csv",
        "data/derived/post_writer_scoring_activation_recheck_v38.csv",
        "data/derived/post_writer_scoring_activation_recheck_summary_v38.csv",
        "data/derived/post_writer_scoring_preflight_recheck_v39.csv",
        "data/derived/post_writer_scoring_preflight_recheck_summary_v39.csv",
        "data/derived/post_writer_scoring_dependency_closure_recheck_v40.csv",
        "data/derived/post_writer_scoring_dependency_closure_recheck_summary_v40.csv",
        "data/derived/post_writer_scoring_unblock_priority_recheck_v41.csv",
        "data/derived/post_writer_scoring_unblock_priority_recheck_summary_v41.csv",
        "data/derived/post_writer_frontier_evidence_acceptance_recheck_v42.csv",
        "data/derived/post_writer_frontier_evidence_acceptance_recheck_summary_v42.csv",
        "data/derived/post_writer_frontier_work_order_recheck_v43.csv",
        "data/derived/post_writer_frontier_work_order_recheck_summary_v43.csv",
        "data/derived/frontier_provenance_evidence_intake_contract_v44.csv",
        "data/derived/frontier_provenance_evidence_intake_checklist_v44.csv",
        "data/derived/frontier_provenance_evidence_intake_contract_summary_v44.csv",
        "data/derived/frontier_provenance_source_candidate_ledger_v45.csv",
        "data/derived/frontier_provenance_source_candidate_coverage_v45.csv",
        "data/derived/frontier_provenance_source_candidate_ledger_summary_v45.csv",
        "data/derived/frontier_provenance_evidence_payload_draft_v46.csv",
        "data/derived/frontier_provenance_evidence_payload_draft_review_v46.csv",
        "data/derived/frontier_provenance_evidence_payload_draft_summary_v46.csv",
        "review_packages/frontier_provenance_v46_review_package/README.md",
        "review_packages/frontier_provenance_v46_review_package/DO_NOT_COPY_WITHOUT_REVIEW.md",
        "review_packages/frontier_provenance_v46_review_package/REVIEW_MANIFEST.csv",
        "review_packages/frontier_provenance_v46_review_package/data/frontier_provenance_evidence_payload_draft_v46.csv",
        "review_packages/frontier_provenance_v46_review_package/data/frontier_provenance_evidence_payload_draft_review_v46.csv",
        "review_packages/frontier_provenance_v46_review_package/data/frontier_provenance_evidence_payload_draft_summary_v46.csv",
        "review_packages/frontier_provenance_v46_review_package.zip",
        "review_packages/frontier_provenance_v46_completed_review_response.zip",
        "review_packages/frontier_provenance_v46_completed_review_response/frontier_provenance_v46_review_response.csv",
        "review_packages/frontier_provenance_v46_completed_review_response/frontier_provenance_v46_review_completed_summary.csv",
        "review_packages/frontier_provenance_v46_completed_review_response/frontier_provenance_v46_review_notes.md",
        "review_packages/frontier_provenance_v46_completed_review_response/frontier_provenance_v46_review_validation_log.txt",
        "data/derived/frontier_provenance_review_response_intake_v48.csv",
        "data/derived/frontier_provenance_review_response_intake_summary_v48.csv",
        "data/derived/frontier_review_promotion_gate_v49.csv",
        "data/derived/frontier_review_promotion_gate_summary_v49.csv",
        "data/external/sparc_hash_audit_v50/SPARC_Lelli2016c.mrt",
        "data/external/sparc_hash_audit_v50/MassModels_Lelli2016c.mrt",
        "data/derived/frontier_external_hash_recompute_audit_v50.csv",
        "data/derived/frontier_external_hash_recompute_audit_summary_v50.csv",
        "data/derived/post_hash_frontier_review_promotion_recheck_v51.csv",
        "data/derived/post_hash_frontier_review_promotion_recheck_summary_v51.csv",
        "review_packages/frontier_post_hash_review_promotion_v51_review_package.zip",
        "review_packages/frontier_post_hash_review_promotion_v51_review_package/README.md",
        "review_packages/frontier_post_hash_review_promotion_v51_review_package/DO_NOT_COPY_WITHOUT_EXPLICIT_PROMOTION.md",
        "review_packages/frontier_post_hash_review_promotion_v51_review_package/REVIEW_MANIFEST.csv",
        "review_packages/frontier_post_hash_review_promotion_v51_review_package/data/frontier_external_hash_recompute_audit_v50.csv",
        "review_packages/frontier_post_hash_review_promotion_v51_review_package/data/frontier_external_hash_recompute_audit_summary_v50.csv",
        "review_packages/frontier_post_hash_review_promotion_v51_review_package/data/post_hash_frontier_review_promotion_recheck_v51.csv",
        "review_packages/frontier_post_hash_review_promotion_v51_review_package/data/post_hash_frontier_review_promotion_recheck_summary_v51.csv",
        "review_packages/frontier_post_hash_review_promotion_v51_review_package/templates/frontier_review_promotion_authorization_TEMPLATE.csv",
        "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response.zip",
        "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response/frontier_post_hash_review_promotion_v51_authorization_response.csv",
        "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response/frontier_post_hash_review_promotion_v51_completed_summary.csv",
        "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response/frontier_post_hash_review_promotion_v51_review_notes.md",
        "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response/frontier_post_hash_review_promotion_v51_validation_log.txt",
        "data/derived/post_hash_review_promotion_response_intake_v53.csv",
        "data/derived/post_hash_review_promotion_response_intake_summary_v53.csv",
        "data/derived/authorized_provenance_evidence_payload_v54.csv",
        "data/derived/authorized_provenance_evidence_payload_summary_v54.csv",
        "data/input/source_import_provenance_evidence_v21.csv",
        "data/derived/active_v21_provenance_evidence_writer_summary_v55.csv",
        "data/derived/m0_no_dark_expression_rule_derivation_contract_v13.csv",
        "data/derived/m0_no_dark_expression_rule_derivation_contract_summary_v13.csv",
        "data/derived/m0_no_dark_expression_source_rule_contract_v12.csv",
        "data/derived/m0_no_dark_expression_source_rule_contract_summary_v12.csv",
        "data/derived/m0_no_dark_frozen_expression_contract_v11.csv",
        "data/derived/m0_no_dark_frozen_expression_contract_summary_v11.csv",
        "data/derived/m0_no_dark_kernel_expression_contract_v10.csv",
        "data/derived/m0_no_dark_kernel_expression_contract_summary_v10.csv",
        "data/derived/m0_no_dark_kernel_expression_interface_v10.csv",
        "data/derived/m0_no_dark_kernel_expression_interface_summary_v10.csv",
        "data/derived/m0_no_dark_frozen_expression_payload_v11.csv",
        "data/derived/m0_no_dark_frozen_expression_payload_summary_v11.csv",
        "data/derived/m0_no_dark_frozen_expression_statement_v12.csv",
        "data/derived/m0_no_dark_frozen_expression_statement_summary_v12.csv",
        "data/derived/m0_no_dark_source_side_expression_statement_v13.csv",
        "data/derived/m0_no_dark_source_side_expression_statement_summary_v13.csv",
        "data/derived/m0_no_dark_statement_term_list_v13.csv",
        "data/derived/m0_no_dark_statement_term_list_summary_v13.csv",
        "data/derived/m0_no_dark_statement_argument_signature_v13.csv",
        "data/derived/m0_no_dark_statement_argument_signature_summary_v13.csv",
        "data/derived/m0_no_dark_statement_constraint_guards_v13.csv",
        "data/derived/m0_no_dark_statement_constraint_guards_summary_v13.csv",
        "data/derived/m0_no_dark_statement_pre_dimensional_proof_v13.csv",
        "data/derived/m0_no_dark_statement_pre_dimensional_proof_summary_v13.csv",
        "data/derived/m0_no_dark_statement_freeze_provenance_v13.csv",
        "data/derived/m0_no_dark_statement_freeze_provenance_summary_v13.csv",
        "data/derived/m0_no_dark_payload_symbol_binding_table_v12.csv",
        "data/derived/m0_no_dark_payload_symbol_binding_table_summary_v12.csv",
        "data/derived/m0_no_dark_payload_constant_policy_v12.csv",
        "data/derived/m0_no_dark_payload_constant_policy_summary_v12.csv",
        "data/derived/m0_no_dark_payload_dimensional_trace_v12.csv",
        "data/derived/m0_no_dark_payload_dimensional_trace_summary_v12.csv",
        "data/derived/m0_no_dark_payload_machine_form_v12.csv",
        "data/derived/m0_no_dark_payload_machine_form_summary_v12.csv",
        "data/derived/m0_no_dark_payload_leakage_certificate_v12.csv",
        "data/derived/m0_no_dark_payload_leakage_certificate_summary_v12.csv",
        "data/derived/m0_no_dark_frozen_expression_body_v14.csv",
        "data/derived/m0_no_dark_frozen_expression_body_summary_v14.csv",
        "scripts/run_readiness_audit.py",
        "scripts/run_scoring_preflight.py",
        "scripts/build_family_prediction_comparability.py",
        "scripts/build_scoring_input_scaffold.py",
        "scripts/run_source_import_leakage_audit.py",
        "scripts/build_source_import_contract.py",
        "scripts/build_leakage_audit_evidence_template.py",
        "scripts/build_leakage_audit_review_package.py",
        "scripts/ingest_leakage_audit_review_response.py",
        "scripts/build_leakage_prescore_artifact_work_order.py",
        "scripts/build_leakage_prescore_artifact_collection_package.py",
        "scripts/run_leakage_prescore_artifact_collection_intake.py",
        "scripts/build_leakage_prescore_artifact_request_ledger.py",
        "scripts/build_leakage_prescore_artifact_request_review_package.py",
        "scripts/run_leakage_prescore_artifact_request_review_intake.py",
        "scripts/build_leakage_prescore_artifact_candidate_ledger.py",
        "scripts/build_leakage_prescore_artifact_candidate_review_package.py",
        "scripts/run_leakage_prescore_artifact_candidate_review_intake.py",
        "scripts/run_leakage_evidence_candidate_ingestion_gate.py",
        "scripts/build_leakage_partial_candidate_sufficiency_review_package.py",
        "scripts/run_leakage_partial_candidate_sufficiency_review_intake.py",
        "scripts/build_leakage_partial_candidate_sufficiency_preaudit.py",
        "scripts/build_leakage_partial_candidate_sufficiency_response_draft.py",
        "scripts/run_full_leakage_evidence_ingestion_gate.py",
        "scripts/run_leakage_audit_evidence_v10_writer.py",
        "scripts/run_leakage_audit_pass_review_gate.py",
        "scripts/run_scoring_row_activation_policy.py",
        "scripts/build_m0_no_dark_rule_parent_assumption_basis.py",
        "scripts/build_m0_no_dark_rule_selection_map.py",
        "scripts/build_m0_no_dark_rule_term_generation_record.py",
        "scripts/build_m0_no_dark_rule_invariance_null_checks.py",
        "scripts/build_m0_no_dark_rule_dimensional_precheck.py",
        "scripts/build_m0_no_dark_rule_derivation_provenance_leakage.py",
        "scripts/build_m0_no_dark_expression_source_basis.py",
        "scripts/build_m0_no_dark_expression_admissibility_rule.py",
        "scripts/build_m0_no_dark_expression_null_fallback_policy.py",
        "scripts/build_m0_no_dark_expression_output_class.py",
        "scripts/build_m0_no_dark_expression_source_rule_leakage_audit.py",
        "scripts/build_m0_no_dark_expression_symbolic_form.py",
        "scripts/build_m0_no_dark_expression_input_domain.py",
        "scripts/build_m0_no_dark_expression_coefficient_freeze.py",
        "scripts/build_m0_no_dark_expression_dimensional_audit.py",
        "scripts/build_m0_no_dark_expression_machine_form.py",
        "scripts/build_m0_no_dark_expression_rule_derivation_contract.py",
        "scripts/build_m0_no_dark_expression_source_rule_contract.py",
        "scripts/build_m0_no_dark_frozen_expression_contract.py",
        "scripts/build_m0_no_dark_kernel_expression_contract.py",
        "scripts/build_m0_no_dark_kernel_expression_interface.py",
        "scripts/build_m0_no_dark_frozen_expression_payload_contract.py",
        "scripts/build_m0_no_dark_frozen_expression_statement_contract.py",
        "scripts/build_m0_no_dark_source_side_expression_statement.py",
        "scripts/build_m0_no_dark_statement_term_list.py",
        "scripts/build_m0_no_dark_statement_argument_signature.py",
        "scripts/build_m0_no_dark_statement_constraint_guards.py",
        "scripts/build_m0_no_dark_statement_pre_dimensional_proof.py",
        "scripts/build_m0_no_dark_statement_freeze_provenance.py",
        "scripts/build_m0_no_dark_payload_symbol_binding_table.py",
        "scripts/build_m0_no_dark_payload_constant_policy.py",
        "scripts/build_m0_no_dark_payload_dimensional_trace.py",
        "scripts/build_m0_no_dark_payload_machine_form.py",
        "scripts/build_m0_no_dark_payload_leakage_certificate.py",
        "scripts/build_m0_no_dark_frozen_expression_body.py",
        "scripts/build_m0_no_dark_equation_kernel_contract.py",
        "scripts/build_m0_no_dark_equation_kernel_interface.py",
        "scripts/build_m0_no_dark_readout_equation_contract.py",
        "scripts/build_m0_no_dark_readout_equation_interface.py",
        "scripts/build_m0_no_dark_formula_body_interface.py",
        "scripts/build_m0_no_dark_formula_body_contract.py",
        "scripts/build_m0_no_dark_formula_table_contract.py",
        "scripts/build_m0_no_dark_prediction_row_writer.py",
        "scripts/build_m0_no_dark_executable_prediction_kernel.py",
        "scripts/build_m0_no_dark_velocity_readout_formula.py",
        "scripts/build_m0_no_dark_source_to_rotation_equation_body.py",
        "scripts/build_m0_no_dark_source_to_velocity_coupling_rule.py",
        "scripts/build_m0_no_dark_velocity_unit_lift_rule.py",
        "scripts/build_m0_no_dark_velocity_dimension_anchor_rule.py",
        "scripts/build_m0_no_dark_velocity_anchor_source_law.py",
        "scripts/build_m0_no_dark_velocity_anchor_candidate_basis.py",
        "scripts/build_m0_no_dark_velocity_anchor_selection_rule.py",
        "scripts/build_m0_no_dark_velocity_anchor_value_freeze.py",
        "scripts/build_m0_no_dark_velocity_anchor_unit_normalization.py",
        "scripts/build_m0_no_dark_velocity_anchor_component_combination_rule.py",
        "scripts/build_m0_no_dark_velocity_anchor_component_weight_policy.py",
        "scripts/build_m0_no_dark_velocity_anchor_component_weight_value_freeze.py",
        "scripts/build_m0_no_dark_velocity_anchor_combined_anchor_rule.py",
        "scripts/build_m0_no_dark_velocity_anchor_combined_anchor_expression_freeze.py",
        "scripts/build_m0_no_dark_velocity_anchor_combined_anchor_value_freeze.py",
        "scripts/build_m0_no_dark_velocity_readout_formula_body_freeze.py",
        "scripts/build_m0_no_dark_prediction_row_value_freeze.py",
        "scripts/build_m0_no_dark_family_prediction_row_emission.py",
        "scripts/build_m0_label_rule_table.py",
        "scripts/build_m1_tau_response_formula_table.py",
        "scripts/build_m1_admissibility_table.py",
        "scripts/build_m1_response_parameter_inventory.py",
        "scripts/build_m1_response_parameter_count_classification.py",
        "scripts/build_m1_response_parameter_count_value_ledger.py",
        "scripts/build_m1_response_parameter_adjustable_slot_resolution.py",
        "scripts/build_m1_response_parameter_final_count_candidate.py",
        "scripts/build_m1_response_parameter_final_count_freeze.py",
        "scripts/build_m1_per_galaxy_response_privilege_count_audit.py",
        "scripts/build_m1_per_galaxy_response_privilege_count_freeze.py",
        "scripts/build_m2_benchmark_parameter_inventory.py",
        "scripts/build_m2_benchmark_parameter_count_classification.py",
        "scripts/build_m2_benchmark_parameter_count_value_ledger.py",
        "scripts/build_m2_benchmark_profile_table.py",
        "scripts/build_m2_nuisance_policy_table.py",
        "scripts/build_m2_benchmark_parameter_adjustable_slot_resolution.py",
        "scripts/build_m2_benchmark_parameter_final_count_candidate.py",
        "scripts/build_m2_benchmark_parameter_final_count_freeze.py",
        "scripts/build_m2_per_galaxy_benchmark_privilege_count_audit.py",
        "scripts/build_m2_per_galaxy_benchmark_privilege_count_freeze.py",
        "scripts/build_shared_scoring_input_table.py",
        "scripts/build_shared_input_count_discount_policy.py",
        "scripts/build_numeric_parameter_count_table.py",
        "scripts/build_numeric_parameter_count_table_v08.py",
        "scripts/build_numeric_parameter_count_table_final_values.py",
        "scripts/build_control_runner_outputs.py",
        "scripts/build_control_execution_readiness.py",
        "scripts/run_endpoint_scoring_runner.py",
        "scripts/build_numeric_decision_thresholds.py",
        "scripts/build_m0_global_parameter_inventory.py",
        "scripts/build_m0_global_parameter_count_classification.py",
        "scripts/build_m0_global_parameter_count_value_ledger.py",
        "scripts/build_m0_global_adjustable_slot_resolution.py",
        "scripts/build_m0_global_final_count_candidate.py",
        "scripts/build_m0_global_final_count_freeze.py",
        "scripts/build_m0_per_galaxy_privilege_count_audit.py",
        "scripts/build_m0_per_galaxy_privilege_count_freeze.py",
        "scripts/build_numeric_count_readiness_closure.py",
        "scripts/build_family_prediction_table_contract.py",
        "scripts/build_family_prediction_frontier_trace.py",
        "scripts/build_source_import_values.py",
        "scripts/run_source_import_real_values_gate.py",
        "scripts/run_scoring_activation_gate.py",
        "scripts/build_source_import_real_values_template.py",
        "scripts/run_source_import_raw_adapter.py",
        "scripts/run_active_v15_raw_sparc_like_input_writer.py",
        "scripts/run_active_v12_real_values_write_authorization.py",
        "scripts/run_source_import_write_authorization.py",
        "scripts/run_source_import_authorized_writer.py",
        "scripts/build_source_import_raw_template.py",
        "scripts/build_source_import_provenance_manifest.py",
        "scripts/run_source_import_provenance_audit.py",
        "scripts/build_source_import_provenance_template.py",
        "scripts/run_source_import_provenance_evidence_gate.py",
        "scripts/run_source_import_provenance_promotion_gate.py",
        "scripts/build_scoring_dependency_closure.py",
        "scripts/build_scoring_unblock_priority.py",
        "scripts/build_scoring_frontier_status.py",
        "scripts/build_frontier_provenance_evidence_acceptance.py",
        "scripts/build_frontier_provenance_evidence_work_order.py",
        "scripts/run_frontier_work_order_completion_gate.py",
        "scripts/run_frontier_evidence_write_authorization.py",
        "scripts/run_frontier_authorized_evidence_writer.py",
        "scripts/run_frontier_post_writer_evidence_absence_audit.py",
        "scripts/run_post_writer_evidence_gate_recheck.py",
        "scripts/run_post_writer_provenance_promotion_recheck.py",
        "scripts/run_post_writer_raw_import_recheck.py",
        "scripts/run_post_writer_raw_adapter_recheck.py",
        "scripts/run_post_writer_real_values_gate_recheck.py",
        "scripts/run_post_writer_leakage_audit_recheck.py",
        "scripts/run_post_writer_scoring_activation_recheck.py",
        "scripts/run_post_writer_scoring_preflight_recheck.py",
        "scripts/run_post_writer_scoring_dependency_closure_recheck.py",
        "scripts/run_post_writer_scoring_unblock_priority_recheck.py",
        "scripts/run_post_writer_frontier_evidence_acceptance_recheck.py",
        "scripts/run_post_writer_frontier_work_order_recheck.py",
        "scripts/build_frontier_provenance_evidence_intake_contract.py",
        "scripts/build_frontier_provenance_source_candidate_ledger.py",
        "scripts/build_frontier_provenance_evidence_payload_draft.py",
        "scripts/build_frontier_provenance_review_package.py",
        "scripts/ingest_frontier_provenance_review_response.py",
        "scripts/run_frontier_review_promotion_gate.py",
        "scripts/run_frontier_external_hash_recompute_audit.py",
        "scripts/run_post_hash_frontier_review_promotion_recheck.py",
        "scripts/build_post_hash_review_promotion_package.py",
        "scripts/ingest_post_hash_review_promotion_response.py",
        "scripts/build_authorized_provenance_evidence_payload.py",
        "scripts/run_active_v21_provenance_evidence_writer.py",
        "scripts/reproduce.py",
        "scripts/validate_protocol_manifests.py",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_manuscript_scope_and_forbidden_overclaims() -> None:
    text = (ROOT / "paper11_submission_source/main.tex").read_text()
    assert "dark-sector necessity" in text.lower()
    assert "Response" in text
    forbidden = [
        "dark matter does not exist",
        "Tau Core replaces the standard dark sector",
        "lensing, CMB, BAO, growth, or cosmology are solved",
    ]
    for phrase in forbidden:
        assert phrase in text


def test_model_family_manifest_is_endpoint_disabled() -> None:
    path = ROOT / "data/source_manifest/model_family_decision_protocol.csv"
    rows = list(csv.DictReader(path.open()))
    assert {row["family_id"] for row in rows} == {"M0", "M1", "M2"}
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_policy_bundle_and_endpoint_manifest_are_not_results() -> None:
    bundle = list(csv.DictReader((ROOT / "data/source_manifest/frozen_policy_bundle_instance_v01.csv").open()))
    endpoint = list(csv.DictReader((ROOT / "data/source_manifest/galaxy_decision_endpoint_manifest_v01.csv").open()))
    assert len(bundle) == 9
    assert len(endpoint) == 8
    assert all(row["endpoint_scoring_allowed"] == "false" for row in bundle)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in endpoint)
    statuses = " ".join(row["current_status"] for row in endpoint)
    assert "M0_wins" not in statuses
    assert "M1_wins" not in statuses
    assert "M2_wins" not in statuses


def test_pre_registration_manifests_are_not_endpoint_results() -> None:
    files = [
        "galaxy_sample_freeze_v01.csv",
        "scoring_rule_freeze_v01.csv",
        "control_manifest_v01.csv",
    ]
    for name in files:
        rows = list(csv.DictReader((ROOT / "data/source_manifest" / name).open()))
        assert rows
        assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    thresholds = list(csv.DictReader((ROOT / "data/source_manifest/decision_threshold_v01.csv").open()))
    assert {row["verdict_label"] for row in thresholds} == {
        "M0_SUFFICIENT",
        "M1_FAVORED",
        "M2_BENCHMARK_STRONGER",
        "UNRESOLVED",
    }
    assert all("PENDING" in row["current_status"] for row in thresholds)


def test_v02_freezes_are_concrete_but_not_activated() -> None:
    galaxy_rows = list(csv.DictReader((ROOT / "data/source_manifest/galaxy_list_freeze_v02.csv").open()))
    assert len(galaxy_rows) >= 10
    assert {"NGC4088", "UGC12506", "NGC4183"}.issubset({row["galaxy_id"] for row in galaxy_rows})
    assert all(row["endpoint_scoring_allowed"] == "false" for row in galaxy_rows)
    assert all("NOT_ACTIVE" in row["scoring_activation_status"] for row in galaxy_rows)

    formula_rows = list(csv.DictReader((ROOT / "data/source_manifest/scoring_formula_freeze_v02.csv").open()))
    assert {row["formula_id"] for row in formula_rows} == {
        "SF02_FULL_CURVE",
        "SF02_INNER_ZONE",
        "SF02_OUTER_ZONE",
        "SF02_PARSIMONY",
        "SF02_GALAXY_SCORE",
        "SF02_HELDOUT",
        "SF02_CONTROL_VETO",
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in formula_rows)
    assert all("FORMULA_POLICY_FROZEN_NOT_RUN" in row["current_status"] for row in formula_rows)


def test_v03_family_budget_and_controls_are_frozen_not_run() -> None:
    budget_rows = list(csv.DictReader((ROOT / "data/source_manifest/family_parameter_count_freeze_v03.csv").open()))
    assert {"M0", "M1", "M2", "ALL"}.issubset({row["family_id"] for row in budget_rows})
    assert all(row["endpoint_scoring_allowed"] == "false" for row in budget_rows)
    assert all("COUNT_RULE_FROZEN_NUMERIC_COUNT_PENDING" in row["numeric_count_status"] for row in budget_rows)
    assert any("Response_tau formula claimed" in row["claim_boundary"] for row in budget_rows)

    control_rows = list(csv.DictReader((ROOT / "data/source_manifest/control_implementation_freeze_v03.csv").open()))
    assert {row["control_id"] for row in control_rows} == {
        "CIF03_SHUFFLE",
        "CIF03_WRONG_FAMILY",
        "CIF03_NULL_SOURCE",
        "CIF03_LEAKAGE",
        "CIF03_RADIAL",
        "CIF03_PARITY",
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in control_rows)
    assert all("IMPLEMENTATION_POLICY_FROZEN_NOT_RUN" in row["current_status"] for row in control_rows)


def test_v04_contracts_are_declared_not_implemented() -> None:
    source_rows = list(csv.DictReader((ROOT / "data/source_manifest/source_field_completeness_v04.csv").open()))
    assert len(source_rows) >= 6
    assert all(row["endpoint_scoring_allowed"] == "false" for row in source_rows)
    assert all("PENDING" in row["activation_status"] for row in source_rows)
    assert any(row["required_field"] == "source_packet_leakage_audit" for row in source_rows)

    registry_rows = list(csv.DictReader((ROOT / "data/source_manifest/family_formula_registry_v04.csv").open()))
    assert {"M0", "M1", "M2", "ALL"}.issubset({row["family_id"] for row in registry_rows})
    assert all(row["endpoint_scoring_allowed"] == "false" for row in registry_rows)
    assert all("PENDING" in row["numeric_count_status"] for row in registry_rows)
    assert any("Response_tau formula" in row["claim_boundary"] for row in registry_rows)

    runner_rows = list(csv.DictReader((ROOT / "data/source_manifest/control_runner_contract_v04.csv").open()))
    assert {row["control_id"] for row in runner_rows} == {
        "CIF03_SHUFFLE",
        "CIF03_WRONG_FAMILY",
        "CIF03_NULL_SOURCE",
        "CIF03_LEAKAGE",
        "CIF03_RADIAL",
        "CIF03_PARITY",
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in runner_rows)
    assert all(row["execution_status"] == "RUNNER_CONTRACT_DECLARED_NOT_IMPLEMENTED" for row in runner_rows)


def test_v05_readiness_ledgers_block_activation_and_counts() -> None:
    audit_rows = list(csv.DictReader((ROOT / "data/source_manifest/source_row_audit_v05.csv").open()))
    galaxy_rows = list(csv.DictReader((ROOT / "data/source_manifest/galaxy_list_freeze_v02.csv").open()))
    assert {row["galaxy_id"] for row in audit_rows} == {row["galaxy_id"] for row in galaxy_rows}
    assert all(row["endpoint_scoring_allowed"] == "false" for row in audit_rows)
    assert all(row["activation_status"] == "ACTIVATION_BLOCKED" for row in audit_rows)
    assert all("PENDING" in row["leakage_audit_status"] for row in audit_rows)

    formula_rows = list(csv.DictReader((ROOT / "data/source_manifest/family_formula_table_v05.csv").open()))
    assert {"M0", "M1", "M2", "ALL"}.issubset({row["family_id"] for row in formula_rows})
    assert all(row["endpoint_scoring_allowed"] == "false" for row in formula_rows)
    assert all(row["formula_table_status"] == "FORMULA_TABLE_REQUIRED_NOT_FILLED" for row in formula_rows)
    assert any("Response_tau formula" in row["claim_boundary"] for row in formula_rows)

    count_rows = list(csv.DictReader((ROOT / "data/source_manifest/numeric_count_readiness_v05.csv").open()))
    assert {"M0", "M1", "M2", "ALL"}.issubset({row["family_id"] for row in count_rows})
    assert all(row["endpoint_scoring_allowed"] == "false" for row in count_rows)
    assert all(row["count_readiness_status"] == "COUNT_NOT_READY" for row in count_rows)


def test_v06_readiness_audit_blocks_endpoint_scoring() -> None:
    activation_rows = list(csv.DictReader((ROOT / "data/derived/activation_blockers_v06.csv").open()))
    assert len(activation_rows) == 18
    assert all(row["activation_status"] == "ACTIVATION_BLOCKED" for row in activation_rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in activation_rows)

    formula_rows = list(csv.DictReader((ROOT / "data/derived/formula_and_count_blockers_v06.csv").open()))
    assert any(row["blocker_type"] == "formula_table" for row in formula_rows)
    assert any(row["blocker_type"] == "numeric_count" for row in formula_rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in formula_rows)

    runner_rows = list(csv.DictReader((ROOT / "data/derived/control_runner_blockers_v06.csv").open()))
    assert len(runner_rows) == 6
    assert all(row["execution_status"] == "RUNNER_CONTRACT_DECLARED_NOT_IMPLEMENTED" for row in runner_rows)

    summary = list(csv.DictReader((ROOT / "data/derived/readiness_summary_v06.csv").open()))
    assert summary == [
        {
            "summary_id": "READINESS_V06",
            "blocked_galaxy_rows": "18",
            "unfilled_formula_tables": "8",
            "blocked_numeric_counts": "7",
            "unimplemented_control_runners": "6",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "ENDPOINT_SCORING_BLOCKED",
            "claim_boundary": "readiness_audit_only_no_dark_sector_verdict",
        }
    ]


def test_v07_scoring_preflight_names_required_inputs_without_scoring() -> None:
    requirements = list(csv.DictReader((ROOT / "data/derived/scoring_input_requirements_v07.csv").open()))
    assert {row["required_artifact"] for row in requirements} == {
        "activated_scoring_rows_v10.csv",
        "data/input/source_import_real_values_v12.csv",
        "family_prediction_tables_v08.csv",
        "numeric_parameter_count_table_final_values_v10.csv",
        "control_runner_outputs_v08.csv",
        "numeric_decision_thresholds_v08.csv",
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in requirements)
    assert sum(row["current_status"].startswith("BLOCKED") for row in requirements) == 0
    assert {
        row["requirement_id"]
        for row in requirements
        if row["current_status"].startswith("BLOCKED")
    } == set()
    family_row = next(row for row in requirements if row["requirement_id"] == "SPR07_FAMILY_PREDICTIONS")
    assert family_row["current_status"] == "READY_M0_ADEQUACY_BASIS_FULL_FAMILY_COMPARISON_BLOCKED_NO_SCORES"

    components = list(csv.DictReader((ROOT / "data/derived/scoring_formula_components_v07.csv").open()))
    assert len(components) == 7
    assert all(row["formula_policy_status"] == "READY_AS_POLICY_NOT_RUN" for row in components)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in components)

    summary = list(csv.DictReader((ROOT / "data/derived/scoring_preflight_summary_v07.csv").open()))
    assert summary == [
        {
            "summary_id": "SCORING_PREFLIGHT_V07",
            "readiness_dependency": "ENDPOINT_SCORING_BLOCKED",
            "blocked_scoring_requirements": "0",
            "formula_policy_components_ready": "7",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_PREFLIGHT_REQUIREMENTS_READY_RAW_M0_ADEQUACY_RUNNER_NEXT_VERDICT_BLOCKED",
            "next_required_artifact": "endpoint_scoring_runner_v01",
            "claim_boundary": "scoring_preflight_only_no_dark_sector_verdict",
        }
    ]


def test_v08_scoring_input_scaffold_declares_shapes_without_data() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/activated_scoring_rows_v08.csv").open()))
    assert len(rows) == 18
    assert all(row["activation_status"] == "NOT_ACTIVATED" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["proposed_split"] for row in rows}.issuperset({"train_candidate", "transfer_candidate"})

    schema = list(csv.DictReader((ROOT / "data/derived/scoring_observed_input_schema_v08.csv").open()))
    assert {"galaxy_id", "radius_kpc", "v_obs_km_s", "sigma_v_km_s"}.issubset({row["field_name"] for row in schema})
    assert all(row["endpoint_scoring_allowed"] == "false" for row in schema)

    observed = list(csv.DictReader((ROOT / "data/derived/scoring_observed_inputs_v08.csv").open()))
    assert len(observed) == 18
    assert all(row["v_obs_km_s"] == "PENDING_SOURCE_IMPORT" for row in observed)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in observed)

    summary = list(csv.DictReader((ROOT / "data/derived/scoring_input_scaffold_summary_v08.csv").open()))
    assert summary == [
        {
            "summary_id": "SCORING_INPUT_SCAFFOLD_V08",
            "scoring_rows_declared": "18",
            "activated_rows": "0",
            "observed_input_rows": "18",
            "observed_numeric_rows": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "INPUT_SCAFFOLD_READY_DATA_MISSING",
            "next_required_artifact": "source_import_and_leakage_audit_v09.csv",
            "claim_boundary": "scoring_input_scaffold_only_no_scores",
        }
    ]


def test_v09_source_import_leakage_audit_blocks_activation() -> None:
    audit = list(csv.DictReader((ROOT / "data/derived/source_import_and_leakage_audit_v09.csv").open()))
    assert len(audit) == 18
    assert all(row["source_import_status"] == "REAL_VALUES_PRESENT_VALIDATION_PENDING_LEAKAGE" for row in audit)
    assert all(row["leakage_audit_status"] == "LEAKAGE_AUDIT_PASS" for row in audit)
    assert all(row["activation_decision"] == "DO_NOT_ACTIVATE" for row in audit)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in audit)

    requirements = list(csv.DictReader((ROOT / "data/derived/source_import_requirements_v09.csv").open()))
    assert {row["required_artifact"] for row in requirements} == {
        "data/input/source_import_real_values_v12.csv",
        "scoring_observed_inputs_v10.csv",
        "leakage_audit_evidence_v10.csv",
        "activated_scoring_rows_v10.csv",
    }
    assert {row["current_status"] for row in requirements} == {"PENDING", "REAL_VALUE_GATE_PRESENT_INPUT_READY_FOR_LEAKAGE"}
    assert all(row["endpoint_scoring_allowed"] == "false" for row in requirements)

    findings = list(csv.DictReader((ROOT / "data/derived/leakage_audit_findings_v09.csv").open()))
    assert len(findings) == 18
    assert all(row["leakage_status"] == "LEAKAGE_AUDIT_PASS" for row in findings)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_leakage_summary_v09.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_LEAKAGE_AUDIT_V09",
            "audited_rows": "18",
            "source_import_pending_rows": "0",
            "leakage_pass_rows": "18",
            "activated_rows": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_AND_LEAKAGE_READY",
            "next_required_artifact": "scoring_row_activation_policy_v79",
            "claim_boundary": "source_import_leakage_audit_only_no_dark_sector_verdict",
        }
    ]


def test_v10_source_import_contract_declares_required_values_without_importing() -> None:
    source_rows = list(csv.DictReader((ROOT / "data/derived/source_import_table_v10.csv").open()))
    assert len(source_rows) == 18
    assert all(row["source_route_status"] == "SOURCE_ROUTE_REQUIRED_NOT_FILLED" for row in source_rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in source_rows)

    observed_contract = list(csv.DictReader((ROOT / "data/derived/observed_input_contract_v10.csv").open()))
    assert {"radius_kpc", "v_obs_km_s", "sigma_v_km_s"}.issubset({row["field_name"] for row in observed_contract})
    assert all(row["source_import_status"] == "CONTRACT_DECLARED_VALUE_PENDING" for row in observed_contract)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in observed_contract)

    leakage_contract = list(csv.DictReader((ROOT / "data/derived/leakage_evidence_contract_v10.csv").open()))
    assert len(leakage_contract) == 4
    assert all(row["status"] == "EVIDENCE_REQUIRED_NOT_FILLED" for row in leakage_contract)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_contract_summary_v10.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_CONTRACT_V10",
            "source_import_rows": "18",
            "source_routes_filled": "0",
            "numeric_observed_rows_filled": "0",
            "leakage_evidence_filled": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_CONTRACT_READY_VALUES_MISSING",
            "next_required_artifact": "source_import_values_v11.csv",
            "claim_boundary": "source_import_contract_only_no_scores",
        }
    ]


def test_v58_leakage_audit_evidence_template_is_not_evidence() -> None:
    rows = list(csv.DictReader((ROOT / "data/input/leakage_audit_evidence_v10_TEMPLATE.csv").open()))
    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["evidence_id"] for row in rows} == {
        "LEC10_SOURCE_ROUTE",
        "LEC10_OBSERVED_INPUTS",
        "LEC10_MORPH_LABELS",
        "LEC10_BENCHMARK_INPUTS",
    }
    assert all(row["review_decision"] == "TEMPLATE_ROW_DO_NOT_IMPORT" for row in rows)
    assert all(row["evidence_status"] == "TEMPLATE_ROW_DO_NOT_IMPORT" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/leakage_audit_evidence_template_summary_v58.csv").open()))
    assert summary == [
        {
            "summary_id": "LEAKAGE_AUDIT_EVIDENCE_TEMPLATE_V58",
            "template_file": "data/input/leakage_audit_evidence_v10_TEMPLATE.csv",
            "target_evidence_file": "data/input/leakage_audit_evidence_v10.csv",
            "template_rows": "72",
            "galaxies_covered": "18",
            "evidence_checks_per_galaxy": "4",
            "leakage_pass_rows_created": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "LEAKAGE_AUDIT_EVIDENCE_TEMPLATE_READY_NOT_EVIDENCE",
            "claim_boundary": "leakage_evidence_template_only_no_pass_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v59_leakage_audit_review_package_is_not_evidence() -> None:
    package_root = ROOT / "review_packages/leakage_audit_v58_review_package"
    zip_path = ROOT / "review_packages/leakage_audit_v58_review_package.zip"
    required = {
        "README.md",
        "DO_NOT_COPY_WITHOUT_COMPLETED_REVIEW.md",
        "REVIEW_MANIFEST.csv",
        "templates/leakage_audit_evidence_v10_TEMPLATE.csv",
        "templates/leakage_audit_review_response_TEMPLATE.csv",
        "data/leakage_audit_evidence_template_summary_v58.csv",
        "data/leakage_evidence_contract_v10.csv",
        "data/source_import_leakage_summary_v09.csv",
        "data/source_import_real_values_summary_v12.csv",
        "data/scoring_unblock_priority_summary_v25.csv",
    }
    assert package_root.exists()
    assert zip_path.exists()
    for rel in required:
        assert (package_root / rel).exists(), rel

    manifest = list(csv.DictReader((package_root / "REVIEW_MANIFEST.csv").open()))
    assert len(manifest) == len(required) - 1
    assert {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"}
    assert all(row["claim_boundary"] == "leakage_review_package_only_no_evidence_no_scores" for row in manifest)

    response = list(csv.DictReader((package_root / "templates/leakage_audit_review_response_TEMPLATE.csv").open()))
    assert len(response) == 72
    assert all(row["review_decision"] == "KEEP_TEMPLATE_NOT_REVIEWED_NO_LEAKAGE_PASS" for row in response)
    assert all(row["reviewer_leakage_pass_authorized"] == "false" for row in response)
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in response)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in response)

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert {f"leakage_audit_v58_review_package/{rel}" for rel in required}.issubset(names)


def test_v60_leakage_audit_review_response_intake_is_no_go_not_evidence() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/leakage_audit_review_response_intake_v60.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/leakage_audit_review_response_intake_summary_v60.csv").open()))
    response_dir = ROOT / "review_packages/leakage_audit_v58_completed_review_response"
    response_zip = ROOT / "review_packages/leakage_audit_v58_completed_review_response.zip"
    required = {
        "leakage_audit_v58_review_response.csv",
        "leakage_audit_v58_review_completed_summary.csv",
        "leakage_audit_v58_review_notes.md",
        "leakage_audit_v58_review_validation_log.txt",
    }
    assert response_zip.exists()
    assert response_dir.exists()
    for rel in required:
        assert (response_dir / rel).exists(), rel
    with zipfile.ZipFile(response_zip) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    assert required.issubset(names)

    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert all(row["review_decision"] == "NO_GO_EVIDENCE_REQUIRED_NOT_FILLED" for row in rows)
    assert all(row["reviewer_leakage_pass_authorized"] == "false" for row in rows)
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["intake_decision"] == "ACCEPT_AS_REVIEWED_NO_GO_NOT_EVIDENCE" for row in rows)

    assert summary == [
        {
            "summary_id": "LEAKAGE_AUDIT_REVIEW_RESPONSE_INTAKE_V60",
            "response_zip": "review_packages/leakage_audit_v58_completed_review_response.zip",
            "response_files_present": "4",
            "review_rows": "72",
            "galaxies_covered": "18",
            "evidence_checks_per_galaxy": "4",
            "review_decision": "NO_GO_EVIDENCE_REQUIRED_NOT_FILLED",
            "no_go_rows": "72",
            "leakage_pass_rows_authorized": "0",
            "activation_rows_authorized": "0",
            "target_evidence_rows_created_by_response": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "LEAKAGE_REVIEW_RESPONSE_ACCEPTED_AS_NO_GO_NOT_EVIDENCE",
            "next_required_action": "provide_reviewed_prescore_source_or_protocol_artifacts_for_LEC10_SOURCE_ROUTE_LEC10_OBSERVED_INPUTS_LEC10_MORPH_LABELS_LEC10_BENCHMARK_INPUTS",
            "claim_boundary": "leakage_review_response_intake_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v61_leakage_prescore_artifact_work_order_is_open_not_evidence() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_work_order_v61.csv").open()))
    coverage = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_work_order_coverage_v61.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_work_order_summary_v61.csv").open()))
    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["evidence_id"] for row in rows} == {
        "LEC10_SOURCE_ROUTE",
        "LEC10_OBSERVED_INPUTS",
        "LEC10_MORPH_LABELS",
        "LEC10_BENCHMARK_INPUTS",
    }
    assert all(row["artifact_collection_status"] == "OPEN_PRESCORE_ARTIFACT_REQUIRED" for row in rows)
    assert all(row["may_create_leakage_evidence_after_work_order"] == "false" for row in rows)
    assert all(row["may_activate_row_after_work_order"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    assert len(coverage) == 4
    assert all(row["galaxy_rows"] == "18" for row in coverage)
    assert all(row["open_prescore_artifact_rows"] == "18" for row in coverage)
    assert all(row["ready_for_leakage_evidence_rows"] == "0" for row in coverage)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in coverage)

    assert summary == [
        {
            "summary_id": "LEAKAGE_PRESCORE_ARTIFACT_WORK_ORDER_V61",
            "work_order_rows": "72",
            "galaxies_covered": "18",
            "evidence_checks_per_galaxy": "4",
            "open_prescore_artifact_rows": "72",
            "ready_for_leakage_evidence_rows": "0",
            "leakage_pass_rows_created": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "LEAKAGE_PRESCORE_ARTIFACT_WORK_ORDER_OPEN",
            "next_required_artifact": "reviewed_prescore_source_or_protocol_artifacts_for_v61",
            "claim_boundary": "leakage_prescore_artifact_work_order_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v62_leakage_prescore_artifact_collection_package_is_not_evidence() -> None:
    package_root = ROOT / "review_packages/leakage_prescore_artifact_v61_collection_package"
    zip_path = ROOT / "review_packages/leakage_prescore_artifact_v61_collection_package.zip"
    required = {
        "README.md",
        "DO_NOT_COPY_WITHOUT_COMPLETED_ARTIFACT_REVIEW.md",
        "REVIEW_MANIFEST.csv",
        "data/leakage_prescore_artifact_work_order_v61.csv",
        "data/leakage_prescore_artifact_work_order_coverage_v61.csv",
        "data/leakage_prescore_artifact_work_order_summary_v61.csv",
        "data/leakage_audit_review_response_intake_summary_v60.csv",
        "data/leakage_audit_evidence_template_summary_v58.csv",
        "templates/leakage_prescore_artifact_collection_response_TEMPLATE.csv",
    }
    assert package_root.exists()
    assert zip_path.exists()
    for rel in required:
        assert (package_root / rel).exists(), rel

    manifest = list(csv.DictReader((package_root / "REVIEW_MANIFEST.csv").open()))
    assert len(manifest) == len(required) - 1
    assert {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"}
    assert all(
        row["claim_boundary"] == "leakage_prescore_artifact_collection_package_only_no_evidence_no_scores"
        for row in manifest
    )

    response = list(
        csv.DictReader((package_root / "templates/leakage_prescore_artifact_collection_response_TEMPLATE.csv").open())
    )
    assert len(response) == 72
    assert len({row["galaxy_id"] for row in response}) == 18
    assert all(row["artifact_review_decision"] == "KEEP_OPEN_ARTIFACT_REQUIRED_NOT_FILLED" for row in response)
    assert all(row["prescore_artifact_uri_or_id"] == "FILL_REVIEWED_PRESCORE_ARTIFACT" for row in response)
    assert all(row["prescore_artifact_hash_or_accession"] == "FILL_HASH_OR_ACCESSION" for row in response)
    assert all(row["artifact_is_prescore"] == "false" for row in response)
    assert all(row["artifact_uses_endpoint_residual_or_family_winner"] == "UNKNOWN_REVIEW_REQUIRED" for row in response)
    assert all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in response)
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in response)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in response)

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert {f"leakage_prescore_artifact_v61_collection_package/{rel}" for rel in required}.issubset(names)


def test_v63_leakage_prescore_artifact_collection_intake_is_no_go_not_evidence() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_collection_intake_v63.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_collection_intake_summary_v63.csv").open())
    )
    response_dir = ROOT / "review_packages/leakage_prescore_artifact_v61_completed_collection_response"
    response_zip = ROOT / "review_packages/leakage_prescore_artifact_v61_completed_collection_response.zip"
    required = {
        "leakage_prescore_artifact_v61_collection_response.csv",
        "leakage_prescore_artifact_v61_collection_completed_summary.csv",
        "leakage_prescore_artifact_v61_collection_notes.md",
        "leakage_prescore_artifact_v61_collection_validation_log.txt",
    }
    assert response_zip.exists()
    assert response_dir.exists()
    for rel in required:
        assert (response_dir / rel).exists(), rel
    with zipfile.ZipFile(response_zip) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    assert required.issubset(names)

    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["evidence_id"] for row in rows} == {
        "LEC10_SOURCE_ROUTE",
        "LEC10_OBSERVED_INPUTS",
        "LEC10_MORPH_LABELS",
        "LEC10_BENCHMARK_INPUTS",
    }
    assert all(row["source_mode"] == "completed_response" for row in rows)
    assert all(row["intake_decision"] == "BLOCKED_PRESCORE_ARTIFACT_REVIEW_INCOMPLETE_OR_UNSAFE" for row in rows)
    assert all(row["leakage_evidence_candidate_status"] == "NOT_CANDIDATE_REVIEW_INCOMPLETE_OR_UNSAFE" for row in rows)
    assert all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in rows)
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    assert summary == [
        {
            "summary_id": "LEAKAGE_PRESCORE_ARTIFACT_COLLECTION_INTAKE_V63",
            "expected_response_zip": "review_packages/leakage_prescore_artifact_v61_completed_collection_response.zip",
            "expected_response_files_present": "4",
            "intake_rows": "72",
            "galaxies_covered": "18",
            "evidence_checks_per_galaxy": "4",
            "completed_response_present": "true",
            "candidate_rows_for_later_leakage_evidence": "0",
            "blocked_or_missing_rows": "72",
            "leakage_evidence_rows_created": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PRESCORE_ARTIFACT_RESPONSE_PRESENT_BUT_BLOCKED",
            "next_required_artifact": "reviewed_prescore_artifact_uri_and_hash_or_accession_for_each_open_LEC10_row",
            "claim_boundary": "leakage_prescore_artifact_collection_intake_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v64_leakage_prescore_artifact_request_ledger_is_open_not_evidence() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_request_ledger_v64.csv").open()))
    coverage = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_request_coverage_v64.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_request_summary_v64.csv").open()))
    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["evidence_id"] for row in rows} == {
        "LEC10_SOURCE_ROUTE",
        "LEC10_OBSERVED_INPUTS",
        "LEC10_MORPH_LABELS",
        "LEC10_BENCHMARK_INPUTS",
    }
    assert all(row["request_status"] == "OPEN_REVIEWED_PRESCORE_ARTIFACT_REQUIRED" for row in rows)
    assert all(row["minimal_required_fields"] for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert all(row["may_create_leakage_evidence_from_request"] == "false" for row in rows)
    assert all(row["may_activate_row_from_request"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    assert len(coverage) == 4
    assert all(row["request_rows"] == "18" for row in coverage)
    assert all(row["open_request_rows"] == "18" for row in coverage)
    assert all(row["candidate_rows_already_available"] == "0" for row in coverage)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in coverage)

    assert summary == [
        {
            "summary_id": "LEAKAGE_PRESCORE_ARTIFACT_REQUEST_LEDGER_V64",
            "request_rows": "72",
            "galaxies_covered": "18",
            "evidence_checks_per_galaxy": "4",
            "open_request_rows": "72",
            "candidate_rows_already_available": "0",
            "leakage_evidence_rows_created": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PRESCORE_ARTIFACT_REQUEST_LEDGER_OPEN",
            "next_required_artifact": "completed_prescore_artifact_response_with_uri_hash_or_accession_for_each_open_request",
            "claim_boundary": "leakage_prescore_artifact_request_ledger_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v65_leakage_prescore_artifact_request_review_package_is_not_evidence() -> None:
    package_root = ROOT / "review_packages/leakage_prescore_artifact_request_v64_review_package"
    zip_path = ROOT / "review_packages/leakage_prescore_artifact_request_v64_review_package.zip"
    required = {
        "README.md",
        "DO_NOT_COPY_WITHOUT_COMPLETED_REQUEST_REVIEW.md",
        "REVIEW_MANIFEST.csv",
        "data/leakage_prescore_artifact_request_ledger_v64.csv",
        "data/leakage_prescore_artifact_request_coverage_v64.csv",
        "data/leakage_prescore_artifact_request_summary_v64.csv",
        "data/leakage_prescore_artifact_collection_intake_summary_v63.csv",
        "templates/leakage_prescore_artifact_request_review_response_TEMPLATE.csv",
    }
    assert package_root.exists()
    assert zip_path.exists()
    for rel in required:
        assert (package_root / rel).exists(), rel

    manifest = list(csv.DictReader((package_root / "REVIEW_MANIFEST.csv").open()))
    assert len(manifest) == len(required) - 1
    assert {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"}
    assert all(
        row["claim_boundary"] == "leakage_prescore_artifact_request_review_package_only_no_evidence_no_scores"
        for row in manifest
    )

    response = list(
        csv.DictReader((package_root / "templates/leakage_prescore_artifact_request_review_response_TEMPLATE.csv").open())
    )
    assert len(response) == 72
    assert len({row["galaxy_id"] for row in response}) == 18
    assert all(row["artifact_review_decision"] == "KEEP_OPEN_REVIEWED_PRESCORE_ARTIFACT_REQUIRED_NOT_FILLED" for row in response)
    assert all(row["prescore_artifact_uri_or_id"] == "FILL_REVIEWED_PRESCORE_ARTIFACT" for row in response)
    assert all(row["prescore_artifact_hash_or_accession"] == "FILL_HASH_OR_ACCESSION" for row in response)
    assert all(row["minimal_required_fields_covered"] == "false" for row in response)
    assert all(row["artifact_is_prescore"] == "false" for row in response)
    assert all(row["artifact_uses_forbidden_inputs"] == "UNKNOWN_REVIEW_REQUIRED" for row in response)
    assert all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in response)
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in response)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in response)

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert {f"leakage_prescore_artifact_request_v64_review_package/{rel}" for rel in required}.issubset(names)


def test_v66_leakage_prescore_artifact_request_review_intake_is_no_go_not_evidence() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_request_review_intake_v66.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_request_review_intake_summary_v66.csv").open())
    )
    response_dir = ROOT / "review_packages/leakage_prescore_artifact_request_v64_completed_review_response"
    response_zip = ROOT / "review_packages/leakage_prescore_artifact_request_v64_completed_review_response.zip"
    required = {
        "leakage_prescore_artifact_request_v64_review_response.csv",
        "leakage_prescore_artifact_request_v64_review_completed_summary.csv",
        "leakage_prescore_artifact_request_v64_review_notes.md",
        "leakage_prescore_artifact_request_v64_review_validation_log.txt",
    }
    assert response_zip.exists()
    assert response_dir.exists()
    for rel in required:
        assert (response_dir / rel).exists(), rel
    with zipfile.ZipFile(response_zip) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    assert required.issubset(names)

    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert all(row["source_mode"] == "completed_response" for row in rows)
    assert all(row["intake_decision"] == "BLOCKED_PRESCORE_REQUEST_REVIEW_INCOMPLETE_OR_UNSAFE" for row in rows)
    assert all(row["leakage_evidence_candidate_status"] == "NOT_CANDIDATE_REVIEW_INCOMPLETE_OR_UNSAFE" for row in rows)
    assert all(row["minimal_required_fields_covered"] == "false" for row in rows)
    assert all(row["artifact_is_prescore"] == "false" for row in rows)
    assert all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in rows)
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    assert summary == [
        {
            "summary_id": "LEAKAGE_PRESCORE_ARTIFACT_REQUEST_REVIEW_INTAKE_V66",
            "response_zip": "review_packages/leakage_prescore_artifact_request_v64_completed_review_response.zip",
            "response_files_present": "4",
            "intake_rows": "72",
            "galaxies_covered": "18",
            "evidence_checks_per_galaxy": "4",
            "completed_response_present": "true",
            "candidate_rows_for_later_leakage_evidence": "0",
            "blocked_or_missing_rows": "72",
            "leakage_evidence_rows_created": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PRESCORE_REQUEST_REVIEW_RESPONSE_PRESENT_BUT_BLOCKED",
            "next_required_artifact": "completed_prescore_artifact_response_with_uri_hash_or_accession_for_each_open_request",
            "claim_boundary": "leakage_prescore_artifact_request_review_intake_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v67_leakage_prescore_artifact_candidate_ledger_is_review_required_not_evidence() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_candidate_ledger_v67.csv").open()))
    coverage = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_candidate_coverage_v67.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_candidate_summary_v67.csv").open()))
    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["evidence_id"] for row in rows} == {
        "LEC10_SOURCE_ROUTE",
        "LEC10_OBSERVED_INPUTS",
        "LEC10_MORPH_LABELS",
        "LEC10_BENCHMARK_INPUTS",
    }
    assert all(row["candidate_artifact_uri_or_id"] for row in rows)
    assert all(row["candidate_artifact_hash_or_accession"].startswith("sha256:") for row in rows)
    assert all(row["candidate_review_status"].endswith("REVIEW_REQUIRED") for row in rows)
    assert all(row["may_promote_to_leakage_evidence_without_review"] == "false" for row in rows)
    assert all(row["may_activate_row_from_candidate"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    assert len(coverage) == 4
    assert all(row["candidate_rows"] == "18" for row in coverage)
    assert all(row["review_required_rows"] == "18" for row in coverage)
    assert all(row["ready_for_leakage_evidence_rows"] == "0" for row in coverage)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in coverage)

    assert summary == [
        {
            "summary_id": "LEAKAGE_PRESCORE_ARTIFACT_CANDIDATE_LEDGER_V67",
            "candidate_rows": "72",
            "galaxies_covered": "18",
            "evidence_checks_per_galaxy": "4",
            "full_candidate_rows": "36",
            "partial_candidate_rows": "36",
            "review_required_rows": "72",
            "ready_for_leakage_evidence_rows": "0",
            "leakage_evidence_rows_created": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PRESCORE_ARTIFACT_CANDIDATES_IDENTIFIED_REVIEW_REQUIRED",
            "next_required_artifact": "completed_candidate_review_response_authorizing_prescore_artifacts",
            "claim_boundary": "leakage_prescore_artifact_candidate_ledger_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v68_leakage_prescore_artifact_candidate_review_package_is_not_evidence() -> None:
    package_root = ROOT / "review_packages/leakage_prescore_artifact_candidate_v67_review_package"
    zip_path = ROOT / "review_packages/leakage_prescore_artifact_candidate_v67_review_package.zip"
    required = {
        "README.md",
        "DO_NOT_COPY_WITHOUT_COMPLETED_CANDIDATE_REVIEW.md",
        "REVIEW_MANIFEST.csv",
        "data/leakage_prescore_artifact_candidate_ledger_v67.csv",
        "data/leakage_prescore_artifact_candidate_coverage_v67.csv",
        "data/leakage_prescore_artifact_candidate_summary_v67.csv",
        "data/leakage_prescore_artifact_request_review_intake_summary_v66.csv",
        "templates/leakage_prescore_artifact_candidate_review_response_TEMPLATE.csv",
    }
    assert package_root.exists()
    assert zip_path.exists()
    for rel in required:
        assert (package_root / rel).exists(), rel

    manifest = list(csv.DictReader((package_root / "REVIEW_MANIFEST.csv").open()))
    assert len(manifest) == len(required) - 1
    assert {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"}
    assert all(
        row["claim_boundary"] == "leakage_prescore_artifact_candidate_review_package_only_no_evidence_no_scores"
        for row in manifest
    )

    response = list(
        csv.DictReader((package_root / "templates/leakage_prescore_artifact_candidate_review_response_TEMPLATE.csv").open())
    )
    assert len(response) == 72
    assert len({row["galaxy_id"] for row in response}) == 18
    assert all(row["candidate_review_decision"] == "KEEP_REVIEW_REQUIRED_NOT_AUTHORIZED" for row in response)
    assert all(row["candidate_artifact_accepted"] == "false" for row in response)
    assert all(row["minimal_required_fields_covered"] == "false" for row in response)
    assert all(row["artifact_is_prescore"] == "false" for row in response)
    assert all(row["artifact_uses_forbidden_inputs"] == "UNKNOWN_REVIEW_REQUIRED" for row in response)
    assert all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in response)
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in response)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in response)

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert {f"leakage_prescore_artifact_candidate_v67_review_package/{rel}" for rel in required}.issubset(names)


def test_v69_leakage_prescore_artifact_candidate_review_intake_accepts_only_full_candidates_not_evidence() -> None:
    response_root = ROOT / "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response"
    response_zip = ROOT / "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response.zip"
    required = {
        "leakage_prescore_artifact_candidate_v67_review_response.csv",
        "leakage_prescore_artifact_candidate_v67_review_completed_summary.csv",
        "leakage_prescore_artifact_candidate_v67_review_notes.md",
        "leakage_prescore_artifact_candidate_v67_review_validation_log.txt",
    }
    assert response_root.exists()
    assert response_zip.exists()
    for rel in required:
        assert (response_root / rel).exists(), rel
    with zipfile.ZipFile(response_zip) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    assert required.issubset(names)

    rows = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_candidate_review_intake_v69.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_candidate_review_intake_summary_v69.csv").open())
    )
    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    accepted = [
        row
        for row in rows
        if row["leakage_evidence_candidate_status"] == "CANDIDATE_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION"
    ]
    blocked = [row for row in rows if row["leakage_evidence_candidate_status"] == "NOT_CANDIDATE_PARTIAL_REVIEW_REQUIRED"]
    assert len(accepted) == 36
    assert len(blocked) == 36
    assert {row["evidence_id"] for row in accepted} == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS"}
    assert {row["evidence_id"] for row in blocked} == {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"}
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "LEAKAGE_PRESCORE_ARTIFACT_CANDIDATE_REVIEW_INTAKE_V69",
            "response_zip": "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response.zip",
            "response_files_present": "4",
            "intake_rows": "72",
            "galaxies_covered": "18",
            "evidence_checks_per_galaxy": "4",
            "completed_response_present": "true",
            "accepted_candidate_rows": "36",
            "blocked_partial_rows": "36",
            "candidate_rows_for_later_leakage_evidence": "36",
            "leakage_evidence_rows_created": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PRESCORE_CANDIDATE_REVIEW_PARTIAL_ACCEPTANCE_NEEDS_LEAKAGE_EVIDENCE_GATE",
            "next_required_artifact": "leakage_evidence_candidate_ingestion_gate_for_36_accepted_candidates",
            "claim_boundary": "leakage_prescore_artifact_candidate_review_intake_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v70_leakage_evidence_candidate_ingestion_gate_is_partial_not_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/leakage_evidence_candidate_ingestion_gate_v70.csv").open()))
    coverage = list(csv.DictReader((ROOT / "data/derived/leakage_evidence_candidate_ingestion_coverage_v70.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/leakage_evidence_candidate_ingestion_summary_v70.csv").open()))
    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    draft = [
        row
        for row in rows
        if row["draft_evidence_candidate_status"] == "DRAFT_CANDIDATE_AVAILABLE_FOR_LATER_LEAKAGE_EVIDENCE_ROW"
    ]
    blocked = [row for row in rows if row["draft_evidence_candidate_status"] == "NOT_AVAILABLE_FOR_LEAKAGE_EVIDENCE_ROW"]
    assert len(draft) == 36
    assert len(blocked) == 36
    assert {row["evidence_id"] for row in draft} == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS"}
    assert {row["evidence_id"] for row in blocked} == {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"}
    assert all(row["target_evidence_file_written"] == "false" for row in rows)
    assert all(row["leakage_pass_authorized"] == "false" for row in rows)
    assert all(row["activation_rows_authorized"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    coverage_by_id = {row["evidence_id"]: row for row in coverage}
    assert len(coverage) == 4
    assert coverage_by_id["LEC10_SOURCE_ROUTE"]["draft_available_rows"] == "18"
    assert coverage_by_id["LEC10_OBSERVED_INPUTS"]["draft_available_rows"] == "18"
    assert coverage_by_id["LEC10_MORPH_LABELS"]["blocked_rows"] == "18"
    assert coverage_by_id["LEC10_BENCHMARK_INPUTS"]["blocked_rows"] == "18"
    assert all(row["target_evidence_rows_created"] == "0" for row in coverage)
    assert all(row["leakage_pass_rows_authorized"] == "0" for row in coverage)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in coverage)

    assert summary == [
        {
            "summary_id": "LEAKAGE_EVIDENCE_CANDIDATE_INGESTION_GATE_V70",
            "input_artifact": "data/derived/leakage_prescore_artifact_candidate_review_intake_v69.csv",
            "gate_rows": "72",
            "galaxies_covered": "18",
            "draft_evidence_candidate_rows": "36",
            "blocked_partial_rows": "36",
            "galaxies_with_source_and_observed_candidates": "18",
            "galaxies_with_all_four_evidence_candidates": "0",
            "target_evidence_rows_created": "0",
            "leakage_pass_rows_authorized": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "LEAKAGE_EVIDENCE_INGESTION_GATE_PARTIAL_READY_STILL_BLOCKED",
            "next_required_artifact": "partial_candidate_sufficiency_review_or_minimum_leakage_policy_decision",
            "claim_boundary": "leakage_evidence_candidate_ingestion_gate_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v71_partial_candidate_sufficiency_review_package_requires_full_four_component_leakage() -> None:
    policy = list(csv.DictReader((ROOT / "data/derived/leakage_partial_candidate_sufficiency_policy_v71.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/leakage_partial_candidate_sufficiency_policy_summary_v71.csv").open())
    )
    package_root = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v71_review_package"
    zip_path = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v71_review_package.zip"
    required = {
        "README.md",
        "DO_NOT_COPY_WITHOUT_COMPLETED_SUFFICIENCY_REVIEW.md",
        "REVIEW_MANIFEST.csv",
        "data/leakage_evidence_candidate_ingestion_gate_v70.csv",
        "data/leakage_evidence_candidate_ingestion_coverage_v70.csv",
        "data/leakage_evidence_candidate_ingestion_summary_v70.csv",
        "data/leakage_partial_candidate_sufficiency_policy_v71.csv",
        "data/leakage_partial_candidate_sufficiency_policy_summary_v71.csv",
        "templates/leakage_partial_candidate_sufficiency_v71_review_response_TEMPLATE.csv",
    }
    assert len(policy) == 4
    by_id = {row["evidence_id"]: row for row in policy}
    assert set(by_id) == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS", "LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"}
    assert by_id["LEC10_SOURCE_ROUTE"]["v70_draft_available_rows"] == "18"
    assert by_id["LEC10_OBSERVED_INPUTS"]["v70_draft_available_rows"] == "18"
    assert by_id["LEC10_MORPH_LABELS"]["requires_completed_sufficiency_review"] == "true"
    assert by_id["LEC10_BENCHMARK_INPUTS"]["requires_completed_sufficiency_review"] == "true"
    assert all(row["required_for_full_leakage_pass"] == "true" for row in policy)
    assert all(row["may_use_minimum_two_component_gate_for_endpoint_scoring"] == "false" for row in policy)
    assert all(row["target_evidence_rows_created"] == "0" for row in policy)
    assert all(row["leakage_pass_authorized"] == "false" for row in policy)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in policy)
    assert summary == [
        {
            "summary_id": "LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_POLICY_V71",
            "policy_rows": "4",
            "required_components_for_full_scoring_leakage_pass": "4",
            "components_with_full_draft_available": "2",
            "components_requiring_sufficiency_review": "2",
            "partial_candidate_rows_requiring_review": "36",
            "minimum_scoring_policy": "FULL_FOUR_COMPONENT_LEAKAGE_REQUIRED_BEFORE_ENDPOINT_SCORING",
            "target_evidence_rows_created": "0",
            "leakage_pass_authorized": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PARTIAL_SUFFICIENCY_REVIEW_PACKAGE_REQUIRED_BEFORE_LEAKAGE_PASS",
            "next_required_artifact": "completed_leakage_partial_candidate_sufficiency_v71_review_response",
            "claim_boundary": "leakage_partial_candidate_sufficiency_policy_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]
    assert package_root.exists()
    assert zip_path.exists()
    for rel in required:
        assert (package_root / rel).exists(), rel
    manifest = list(csv.DictReader((package_root / "REVIEW_MANIFEST.csv").open()))
    assert len(manifest) == len(required) - 1
    assert {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"}
    assert all(
        row["claim_boundary"] == "leakage_partial_candidate_sufficiency_review_package_only_no_evidence_no_scores"
        for row in manifest
    )
    template = list(
        csv.DictReader((package_root / "templates/leakage_partial_candidate_sufficiency_v71_review_response_TEMPLATE.csv").open())
    )
    assert len(template) == 36
    assert {row["evidence_id"] for row in template} == {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"}
    assert all(row["sufficiency_review_decision"] == "KEEP_BLOCKED_PARTIAL_REVIEW_REQUIRED_NOT_AUTHORIZED" for row in template)
    assert all(row["partial_candidate_sufficient_for_later_ingestion"] == "false" for row in template)
    assert all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in template)
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in template)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in template)
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert {f"leakage_partial_candidate_sufficiency_v71_review_package/{rel}" for rel in required}.issubset(names)


def test_v73_partial_candidate_sufficiency_review_intake_accepts_for_later_ingestion_only() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/leakage_partial_candidate_sufficiency_review_intake_v73.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/leakage_partial_candidate_sufficiency_review_intake_summary_v73.csv").open())
    )
    assert len(rows) == 36
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["evidence_id"] for row in rows} == {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"}
    assert all(row["source_mode"] == "completed_response" for row in rows)
    assert all(
        row["intake_decision"] == "ACCEPT_PARTIAL_SUFFICIENCY_FOR_LATER_LEAKAGE_EVIDENCE_GATE_NOT_EVIDENCE"
        for row in rows
    )
    assert all(
        row["sufficiency_candidate_status"] == "SUFFICIENCY_ACCEPTED_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION"
        for row in rows
    )
    assert all(row["may_promote_to_leakage_evidence_after_ingestion"] == "true" for row in rows)
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_REVIEW_INTAKE_V73",
            "response_zip": "review_packages/leakage_partial_candidate_sufficiency_v71_completed_review_response.zip",
            "response_files_present": "4",
            "intake_rows": "36",
            "galaxies_covered": "18",
            "partial_evidence_components": "2",
            "completed_response_present": "true",
            "accepted_sufficiency_rows": "36",
            "blocked_or_missing_rows": "0",
            "target_evidence_rows_created": "0",
            "leakage_pass_authorized": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PARTIAL_SUFFICIENCY_REVIEW_READY_FOR_LATER_LEAKAGE_EVIDENCE_GATE",
            "next_required_artifact": "full_leakage_evidence_ingestion_gate_after_accepted_v71_response",
            "claim_boundary": "leakage_partial_candidate_sufficiency_review_intake_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v74_partial_candidate_sufficiency_preaudit_is_review_ready_not_accepted() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/leakage_partial_candidate_sufficiency_preaudit_v74.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv").open())
    )
    assert len(rows) == 36
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["evidence_id"] for row in rows} == {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"}
    assert all(row["artifact_exists"] == "true" for row in rows)
    assert all(row["row_selector_found"] == "true" for row in rows)
    assert all(row["source_side_fields_present"] == "true" for row in rows)
    assert all(row["endpoint_scoring_disabled_in_source"] == "true" for row in rows)
    assert all(row["not_active_or_not_run"] == "true" for row in rows)
    assert all(row["forbidden_input_guard_present"] == "true" for row in rows)
    assert all(row["preaudit_decision"] == "PREAUDIT_REVIEW_READY_NOT_ACCEPTED" for row in rows)
    assert all(row["target_evidence_rows_created"] == "0" for row in rows)
    assert all(row["leakage_pass_authorized"] == "false" for row in rows)
    assert all(row["activation_rows_authorized"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_PREAUDIT_V74",
            "preaudit_rows": "36",
            "galaxies_covered": "18",
            "partial_evidence_components": "2",
            "preaudit_review_ready_rows": "36",
            "preaudit_blocked_rows": "0",
            "accepted_sufficiency_rows": "0",
            "target_evidence_rows_created": "0",
            "leakage_pass_authorized": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PARTIAL_SUFFICIENCY_PREAUDIT_REVIEW_READY_NOT_ACCEPTED",
            "next_required_artifact": "completed_leakage_partial_candidate_sufficiency_v71_review_response.zip",
            "claim_boundary": "leakage_partial_candidate_sufficiency_preaudit_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v75_partial_candidate_sufficiency_response_draft_is_not_completed_response() -> None:
    package_root = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package"
    zip_path = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package.zip"
    required = {
        "README.md",
        "DO_NOT_INGEST_WITHOUT_INDEPENDENT_REVIEW.md",
        "REVIEW_MANIFEST.csv",
        "templates/leakage_partial_candidate_sufficiency_v71_review_response_DRAFT.csv",
        "data/leakage_partial_candidate_sufficiency_response_draft_summary_v75.csv",
        "data/leakage_partial_candidate_sufficiency_preaudit_v74.csv",
        "data/leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv",
    }
    assert package_root.exists()
    assert zip_path.exists()
    for rel in required:
        assert (package_root / rel).exists(), rel
    manifest = list(csv.DictReader((package_root / "REVIEW_MANIFEST.csv").open()))
    assert len(manifest) == len(required) - 1
    assert {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"}
    assert all(
        row["claim_boundary"] == "leakage_partial_candidate_sufficiency_response_draft_only_no_evidence_no_scores"
        for row in manifest
    )
    rows = list(
        csv.DictReader((package_root / "templates/leakage_partial_candidate_sufficiency_v71_review_response_DRAFT.csv").open())
    )
    assert len(rows) == 36
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["evidence_id"] for row in rows} == {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"}
    assert all(
        row["sufficiency_review_decision"] == "ACCEPT_PARTIAL_CANDIDATE_SUFFICIENT_FOR_LATER_INGESTION_GATE"
        for row in rows
    )
    assert all(row["partial_candidate_sufficient_for_later_ingestion"] == "true" for row in rows)
    assert all(row["minimal_required_fields_covered"] == "true" for row in rows)
    assert all(row["artifact_is_prescore"] == "true" for row in rows)
    assert all(row["artifact_uses_forbidden_inputs"] == "false" for row in rows)
    assert all(row["may_promote_to_leakage_evidence_after_ingestion"] == "true" for row in rows)
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    summary = list(csv.DictReader((ROOT / "data/derived/leakage_partial_candidate_sufficiency_response_draft_summary_v75.csv").open()))
    assert summary == [
        {
            "summary_id": "LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_RESPONSE_DRAFT_V75",
            "draft_rows": "36",
            "galaxies_covered": "18",
            "partial_evidence_components": "2",
            "proposed_accept_rows": "36",
            "proposed_block_rows": "0",
            "completed_response_created": "false",
            "target_evidence_rows_created": "0",
            "leakage_pass_authorized": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "DRAFT_RESPONSE_READY_FOR_INDEPENDENT_REVIEW_NOT_INGESTED",
            "next_required_artifact": "independently_reviewed_completed_leakage_partial_candidate_sufficiency_v71_response",
            "claim_boundary": "leakage_partial_candidate_sufficiency_response_draft_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert {f"leakage_partial_candidate_sufficiency_v75_response_draft_package/{rel}" for rel in required}.issubset(names)


def test_v76_full_leakage_evidence_ingestion_gate_is_ready_but_non_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/full_leakage_evidence_ingestion_gate_v76.csv").open()))
    coverage = list(csv.DictReader((ROOT / "data/derived/full_leakage_evidence_ingestion_coverage_v76.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/full_leakage_evidence_ingestion_summary_v76.csv").open()))
    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["evidence_id"] for row in rows} == {
        "LEC10_SOURCE_ROUTE",
        "LEC10_OBSERVED_INPUTS",
        "LEC10_MORPH_LABELS",
        "LEC10_BENCHMARK_INPUTS",
    }
    assert all(row["full_ingestion_decision"] == "READY_FOR_LEAKAGE_EVIDENCE_ROW_WRITE_NOT_WRITTEN" for row in rows)
    assert all(row["full_ingestion_component_status"] == "FULL_COMPONENT_READY_NOT_ACTIVE_EVIDENCE" for row in rows)
    assert all(row["target_evidence_row_written"] == "false" for row in rows)
    assert all(row["leakage_pass_authorized"] == "false" for row in rows)
    assert all(row["activation_rows_authorized"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert len(coverage) == 18
    assert all(row["ready_components"] == "4" for row in coverage)
    assert all(row["missing_components"] == "" for row in coverage)
    assert all(row["full_leakage_evidence_ingestion_ready"] == "true" for row in coverage)
    assert all(row["target_evidence_rows_created"] == "0" for row in coverage)
    assert all(row["leakage_pass_authorized"] == "false" for row in coverage)
    assert all(row["activation_rows_authorized"] == "0" for row in coverage)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in coverage)
    assert summary == [
        {
            "summary_id": "FULL_LEAKAGE_EVIDENCE_INGESTION_GATE_V76",
            "input_artifacts": "data/derived/leakage_evidence_candidate_ingestion_gate_v70.csv;data/derived/leakage_partial_candidate_sufficiency_review_intake_v73.csv",
            "gate_rows": "72",
            "galaxies_covered": "18",
            "ready_component_rows": "72",
            "galaxies_with_all_four_ready_components": "18",
            "target_evidence_rows_created": "0",
            "leakage_pass_rows_authorized": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FULL_LEAKAGE_EVIDENCE_INGESTION_READY_FOR_TARGET_EVIDENCE_WRITE",
            "next_required_artifact": "leakage_audit_evidence_v10_writer_from_v76_full_ingestion_gate",
            "claim_boundary": "full_leakage_evidence_ingestion_gate_only_no_evidence_write_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v77_leakage_audit_evidence_writer_creates_review_pending_input_only() -> None:
    rows = list(csv.DictReader((ROOT / "data/input/leakage_audit_evidence_v10.csv").open()))
    coverage = list(csv.DictReader((ROOT / "data/derived/leakage_audit_evidence_v10_writer_coverage_v77.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/leakage_audit_evidence_v10_writer_summary_v77.csv").open()))
    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["evidence_id"] for row in rows} == {
        "LEC10_SOURCE_ROUTE",
        "LEC10_OBSERVED_INPUTS",
        "LEC10_MORPH_LABELS",
        "LEC10_BENCHMARK_INPUTS",
    }
    assert all(row["review_decision"] == "READY_FOR_LEAKAGE_REVIEW_NOT_PASS" for row in rows)
    assert all(row["evidence_status"] == "TARGET_EVIDENCE_ROW_WRITTEN_REVIEW_PENDING" for row in rows)
    assert all(row["reviewer_leakage_pass_authorized"] == "false" for row in rows)
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert len(coverage) == 18
    assert all(row["target_evidence_rows_written"] == "4" for row in coverage)
    assert all(row["leakage_review_ready"] == "true" for row in coverage)
    assert all(row["leakage_pass_authorized"] == "false" for row in coverage)
    assert all(row["activation_rows_authorized"] == "0" for row in coverage)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in coverage)
    assert summary == [
        {
            "summary_id": "LEAKAGE_AUDIT_EVIDENCE_V10_WRITER_V77",
            "target_evidence_file": "data/input/leakage_audit_evidence_v10.csv",
            "input_artifact": "data/derived/full_leakage_evidence_ingestion_gate_v76.csv",
            "target_evidence_rows_written": "72",
            "galaxies_covered": "18",
            "galaxies_ready_for_leakage_review": "18",
            "leakage_pass_rows_authorized": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "LEAKAGE_AUDIT_EVIDENCE_WRITTEN_REVIEW_PENDING",
            "next_required_artifact": "leakage_audit_pass_review_gate_after_v10_evidence",
            "claim_boundary": "leakage_audit_evidence_v10_writer_only_review_pending_no_pass_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v78_leakage_audit_pass_review_authorizes_pass_only() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/leakage_audit_pass_review_gate_v78.csv").open()))
    coverage = list(csv.DictReader((ROOT / "data/derived/leakage_audit_pass_review_coverage_v78.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/leakage_audit_pass_review_summary_v78.csv").open()))
    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert all(row["pass_review_decision"] == "LEAKAGE_COMPONENT_PASS_REVIEWED_NO_ACTIVATION" for row in rows)
    assert all(row["leakage_component_pass_authorized"] == "true" for row in rows)
    assert all(row["activation_rows_authorized"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert len(coverage) == 18
    assert all(row["passed_leakage_components"] == "4" for row in coverage)
    assert all(row["galaxy_leakage_pass_authorized"] == "true" for row in coverage)
    assert all(row["activation_rows_authorized"] == "0" for row in coverage)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in coverage)
    assert summary == [
        {
            "summary_id": "LEAKAGE_AUDIT_PASS_REVIEW_GATE_V78",
            "input_artifact": "data/input/leakage_audit_evidence_v10.csv",
            "component_rows_reviewed": "72",
            "component_pass_rows_authorized": "72",
            "galaxies_covered": "18",
            "galaxy_leakage_pass_rows_authorized": "18",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "LEAKAGE_AUDIT_PASS_REVIEWED_ACTIVATION_PENDING",
            "next_required_artifact": "scoring_row_activation_policy_v79",
            "claim_boundary": "leakage_audit_pass_review_gate_only_no_activation_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v11_source_import_values_are_declared_but_unfilled() -> None:
    source_values = list(csv.DictReader((ROOT / "data/derived/source_import_values_v11.csv").open()))
    assert len(source_values) == 18
    assert all(row["source_route_value_status"] == "VALUE_REQUIRED_NOT_FILLED" for row in source_values)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in source_values)

    observed_values = list(csv.DictReader((ROOT / "data/derived/observed_numeric_values_v11.csv").open()))
    assert len(observed_values) == 18
    assert all(row["observed_value_status"] == "VALUE_REQUIRED_NOT_FILLED" for row in observed_values)
    assert all(row["v_obs_km_s"] == "VALUE_REQUIRED_NOT_FILLED" for row in observed_values)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in observed_values)

    leakage_values = list(csv.DictReader((ROOT / "data/derived/leakage_evidence_values_v11.csv").open()))
    assert len(leakage_values) == 4
    assert all(row["evidence_status"] == "VALUE_REQUIRED_NOT_FILLED" for row in leakage_values)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_values_summary_v11.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_VALUES_V11",
            "source_value_rows": "18",
            "source_routes_filled": "0",
            "observed_value_rows": "18",
            "observed_numeric_rows_filled": "0",
            "leakage_evidence_rows": "4",
            "leakage_evidence_filled": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_VALUES_DECLARED_NOT_FILLED",
            "next_required_artifact": "source_import_real_values_v12.csv",
            "claim_boundary": "source_import_values_placeholder_only_no_scores",
        }
    ]


def test_v12_real_value_import_gate_blocks_until_input_file_exists() -> None:
    schema = list(csv.DictReader((ROOT / "data/derived/source_import_real_values_schema_v12.csv").open()))
    assert {"galaxy_id", "radius_kpc", "v_obs_km_s", "source_route"}.issubset(
        {row["field_name"] for row in schema}
    )
    assert all(row["endpoint_scoring_allowed"] == "false" for row in schema)

    gates = list(csv.DictReader((ROOT / "data/derived/source_import_real_values_gate_v12.csv").open()))
    assert len(gates) == 18
    assert all(row["input_file_status"] == "REAL_VALUE_HEADER_OK" for row in gates)
    assert sum(int(row["imported_numeric_rows"]) for row in gates) == 450
    assert all(row["real_value_gate_status"] == "REAL_VALUES_PRESENT_VALIDATION_PENDING_LEAKAGE" for row in gates)
    assert all(row["activation_decision"] == "VALUE_GATE_PASSED_PENDING_LEAKAGE" for row in gates)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in gates)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_real_values_summary_v12.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_REAL_VALUES_GATE_V12",
            "expected_galaxy_rows": "18",
            "galaxies_with_imported_rows": "18",
            "imported_numeric_rows": "450",
            "rows_passing_value_gate": "18",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_REAL_VALUES_READY_FOR_LEAKAGE",
            "next_required_artifact": "data/derived/source_import_leakage_summary_v09.csv",
            "claim_boundary": "real_value_import_gate_only_no_dark_sector_verdict",
        }
    ]


def test_v13_scoring_activation_gate_blocks_all_rows() -> None:
    gates = list(csv.DictReader((ROOT / "data/derived/scoring_activation_gate_v13.csv").open()))
    assert len(gates) == 18
    assert all(row["activation_decision"] == "ACTIVATE_FOR_SCORING" for row in gates)
    assert all("real_source_values_missing" not in row["blocking_requirements"] for row in gates)
    assert all("leakage_audit_not_passed" not in row["blocking_requirements"] for row in gates)
    assert all("source_row_not_activated" not in row["blocking_requirements"] for row in gates)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in gates)

    blockers = list(csv.DictReader((ROOT / "data/derived/scoring_activation_global_blockers_v13.csv").open()))
    assert {row["blocker_id"] for row in blockers} == {
        "SAG13_FAMILY_FORMULA_TABLES",
        "SAG13_PARAMETER_COUNTS",
        "SAG13_CONTROL_RUNNERS",
        "SAG13_DECISION_THRESHOLDS",
    }
    assert {row["blocker_id"] for row in blockers if row["current_status"] == "READY"} == {
        "SAG13_FAMILY_FORMULA_TABLES",
        "SAG13_PARAMETER_COUNTS",
        "SAG13_CONTROL_RUNNERS",
        "SAG13_DECISION_THRESHOLDS",
    }
    assert {row["blocker_id"] for row in blockers if row["current_status"] == "BLOCKED"} == set()
    assert all(row["endpoint_scoring_allowed"] == "false" for row in blockers)

    summary = list(csv.DictReader((ROOT / "data/derived/scoring_activation_summary_v13.csv").open()))
    assert summary == [
        {
            "summary_id": "SCORING_ACTIVATION_GATE_V13",
            "candidate_rows": "18",
            "rows_activated_for_scoring": "18",
            "row_level_blocked_rows": "0",
            "global_blockers": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_ACTIVATION_READY_GLOBAL_PREREQUISITES_READY",
            "next_required_artifact": "scoring_preflight_v07.csv",
            "claim_boundary": "activation_gate_only_no_dark_sector_verdict",
        }
    ]


def test_v79_scoring_row_activation_policy_activates_rows_not_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/activated_scoring_rows_v10.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/scoring_row_activation_policy_summary_v79.csv").open()))
    assert len(rows) == 18
    assert all(row["activation_status"] == "ACTIVATED" for row in rows)
    assert all(row["activation_policy_blockers"] == "" for row in rows)
    assert all(row["leakage_audit_status"] == "LEAKAGE_AUDIT_PASS" for row in rows)
    assert all(row["v78_leakage_pass_authorized"] == "true" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "SCORING_ROW_ACTIVATION_POLICY_V79",
            "candidate_rows": "18",
            "activated_rows_written": "18",
            "blocked_rows": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_ROW_ACTIVATION_POLICY_READY_GLOBAL_SCORING_BLOCKED",
            "next_required_artifact": "family_prediction_tables_v08.csv",
            "claim_boundary": "row_activation_policy_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v14_m0_no_dark_rule_parent_assumption_basis_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_rule_parent_assumption_basis_v14.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_rule_parent_assumption_basis_summary_v14.csv").open()))
    assert len(rows) == 6
    assert {row["basis_id"] for row in rows} == {
        "M0NDPB14_SOURCE_FREEZE",
        "M0NDPB14_NO_DARK_RESPONSE_EXCLUSION",
        "M0NDPB14_MORPHOLOGY_READOUT",
        "M0NDPB14_LOCAL_CLOSURE_DIAGNOSTIC",
        "M0NDPB14_BARYONIC_INPUT_BOUNDARY",
        "M0NDPB14_FAILURE_POLICY",
    }
    assert all(row["basis_status"] == "READY" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_RULE_PARENT_ASSUMPTION_BASIS_V14",
            "basis_artifact": "m0_no_dark_rule_parent_assumption_basis_v14",
            "basis_rows": "6",
            "ready_basis_rows": "6",
            "blocked_basis_rows": "0",
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_RULE_PARENT_ASSUMPTION_BASIS_READY",
            "next_required_artifact": "m0_no_dark_rule_selection_map_v14",
            "claim_boundary": "m0_no_dark_rule_parent_assumption_basis_only_no_rule_no_predictions_no_scores",
        }
    ]


def test_v14_m0_no_dark_rule_selection_map_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_rule_selection_map_v14.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_rule_selection_map_summary_v14.csv").open()))
    assert len(rows) == 6
    assert {row["selection_id"] for row in rows} == {
        "M0NDRSM14_SOURCE_FREEZE_TO_INPUT_DOMAIN",
        "M0NDRSM14_NO_DARK_TO_RESPONSE_EXCLUSION",
        "M0NDRSM14_MORPHOLOGY_TO_SOURCE_TERMS",
        "M0NDRSM14_U_READ_TO_ADMISSIBILITY_ORDER",
        "M0NDRSM14_BARYONIC_BOUNDARY_TO_BINDINGS",
        "M0NDRSM14_FAILURE_POLICY_TO_BLOCK_ROUTE",
    }
    assert all(row["selection_status"] == "READY" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_RULE_SELECTION_MAP_V14",
            "selection_artifact": "m0_no_dark_rule_selection_map_v14",
            "parent_basis_status": "READY",
            "selection_rows": "6",
            "ready_selection_rows": "6",
            "blocked_selection_rows": "0",
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_RULE_SELECTION_MAP_READY",
            "next_required_artifact": "m0_no_dark_rule_term_generation_record_v14",
            "claim_boundary": "m0_no_dark_rule_selection_map_only_no_terms_no_formula_no_scores",
        }
    ]


def test_v14_m0_no_dark_rule_term_generation_record_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_rule_term_generation_record_v14.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_rule_term_generation_record_summary_v14.csv").open()))
    assert len(rows) == 6
    assert {row["term_record_id"] for row in rows} == {
        "M0NDTG14_INPUT_DOMAIN_TERM",
        "M0NDTG14_NO_DARK_EXCLUSION_TERM",
        "M0NDTG14_MORPHOLOGY_SOURCE_TERM_CLASS",
        "M0NDTG14_U_READ_ADMISSIBILITY_MARKER",
        "M0NDTG14_BARYONIC_BINDING_TERM_CLASS",
        "M0NDTG14_FAILURE_ROUTE_TERM",
    }
    assert all(row["term_generation_status"] == "READY" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_RULE_TERM_GENERATION_RECORD_V14",
            "term_generation_artifact": "m0_no_dark_rule_term_generation_record_v14",
            "selection_map_status": "READY",
            "term_rows": "6",
            "ready_term_rows": "6",
            "blocked_term_rows": "0",
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_RULE_TERM_GENERATION_RECORD_READY",
            "next_required_artifact": "m0_no_dark_rule_invariance_null_checks_v14",
            "claim_boundary": "m0_no_dark_rule_term_generation_record_only_no_expression_no_formula_no_scores",
        }
    ]


def test_v14_m0_no_dark_rule_invariance_null_checks_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_rule_invariance_null_checks_v14.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_rule_invariance_null_checks_summary_v14.csv").open()))
    assert len(rows) == 6
    assert {row["check_id"] for row in rows} == {
        "M0NDINC14_INPUT_DOMAIN_NULL_CHECK",
        "M0NDINC14_NO_DARK_EXCLUSION_CHECK",
        "M0NDINC14_MORPHOLOGY_SOURCE_INVARIANCE_CHECK",
        "M0NDINC14_U_READ_INCOMPARABILITY_CHECK",
        "M0NDINC14_BARYONIC_BINDING_CHECK",
        "M0NDINC14_FAILURE_ROUTE_CHECK",
    }
    assert all(row["check_status"] == "READY" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_RULE_INVARIANCE_NULL_CHECKS_V14",
            "check_artifact": "m0_no_dark_rule_invariance_null_checks_v14",
            "term_generation_status": "READY",
            "check_rows": "6",
            "ready_check_rows": "6",
            "blocked_check_rows": "0",
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_RULE_INVARIANCE_NULL_CHECKS_READY",
            "next_required_artifact": "m0_no_dark_rule_dimensional_precheck_v14",
            "claim_boundary": "m0_no_dark_rule_invariance_null_checks_only_no_expression_no_formula_no_scores",
        }
    ]


def test_v14_m0_no_dark_rule_dimensional_precheck_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_rule_dimensional_precheck_v14.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_rule_dimensional_precheck_summary_v14.csv").open()))
    assert len(rows) == 6
    assert {row["precheck_id"] for row in rows} == {
        "M0NDDP14_INPUT_DOMAIN_DIMENSION_ROUTE",
        "M0NDDP14_NO_DARK_EXCLUSION_DIMENSION_ROUTE",
        "M0NDDP14_MORPHOLOGY_SOURCE_DIMENSION_ROUTE",
        "M0NDDP14_U_READ_DIMENSIONLESS_ORDER_ROUTE",
        "M0NDDP14_BARYONIC_BINDING_DIMENSION_ROUTE",
        "M0NDDP14_FAILURE_ROUTE_DIMENSION_SAFE_BLOCK",
    }
    assert all(row["dimensional_precheck_status"] == "READY" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_RULE_DIMENSIONAL_PRECHECK_V14",
            "precheck_artifact": "m0_no_dark_rule_dimensional_precheck_v14",
            "invariance_null_status": "READY",
            "precheck_rows": "6",
            "ready_precheck_rows": "6",
            "blocked_precheck_rows": "0",
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_RULE_DIMENSIONAL_PRECHECK_READY",
            "next_required_artifact": "m0_no_dark_rule_derivation_provenance_leakage_v14",
            "claim_boundary": "m0_no_dark_rule_dimensional_precheck_only_no_expression_no_formula_no_scores",
        }
    ]


def test_v14_m0_no_dark_rule_derivation_provenance_leakage_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_rule_derivation_provenance_leakage_v14.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_rule_derivation_provenance_leakage_summary_v14.csv").open()))
    assert len(rows) == 6
    assert {row["audit_id"] for row in rows} == {
        "M0NDPAL14_PARENT_BASIS_PROVENANCE",
        "M0NDPAL14_SELECTION_MAP_PROVENANCE",
        "M0NDPAL14_TERM_GENERATION_PROVENANCE",
        "M0NDPAL14_INVARIANCE_NULL_PROVENANCE",
        "M0NDPAL14_DIMENSIONAL_PRECHECK_PROVENANCE",
        "M0NDPAL14_FRONTIER_HANDOFF",
    }
    assert all(row["audit_status"] == "READY" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["derivation_claim_allowed"] == "false" for row in rows)
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_RULE_DERIVATION_PROVENANCE_LEAKAGE_V14",
            "audit_artifact": "m0_no_dark_rule_derivation_provenance_leakage_v14",
            "dimensional_precheck_status": "READY",
            "audit_rows": "6",
            "ready_audit_rows": "6",
            "blocked_audit_rows": "0",
            "derivation_claim_allowed": "false",
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_RULE_DERIVATION_PROVENANCE_LEAKAGE_READY",
            "next_required_artifact": "m0_no_dark_expression_source_basis_v13",
            "claim_boundary": "m0_no_dark_rule_derivation_provenance_leakage_only_no_rule_no_formula_no_scores",
        }
    ]


def test_v13_m0_no_dark_expression_rule_derivation_contract_ready_for_source_basis() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_rule_derivation_contract_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_rule_derivation_contract_summary_v13.csv").open()))
    assert len(rows) == 6
    assert {row["derivation_slot_id"] for row in rows} == {
        "M0NDER13_PARENT_ASSUMPTIONS",
        "M0NDER13_RULE_SELECTION_MAP",
        "M0NDER13_TERM_GENERATION",
        "M0NDER13_INVARIANCE_CHECKS",
        "M0NDER13_DIMENSIONAL_PRECHECK",
        "M0NDER13_PROVENANCE_AND_LEAKAGE",
    }
    assert all(row["derivation_claim_allowed"] == "false" for row in rows)
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert rows[0]["completion_status"] == "READY"
    assert rows[0]["next_required_artifact"] == "m0_no_dark_rule_parent_assumption_basis_v14"
    assert rows[1]["completion_status"] == "READY"
    assert rows[1]["next_required_artifact"] == "m0_no_dark_rule_selection_map_v14"
    assert rows[2]["completion_status"] == "READY"
    assert rows[2]["next_required_artifact"] == "m0_no_dark_rule_term_generation_record_v14"
    assert rows[3]["completion_status"] == "READY"
    assert rows[3]["next_required_artifact"] == "m0_no_dark_rule_invariance_null_checks_v14"
    assert rows[4]["completion_status"] == "READY"
    assert rows[4]["next_required_artifact"] == "m0_no_dark_rule_dimensional_precheck_v14"
    assert rows[5]["completion_status"] == "READY"
    assert rows[5]["next_required_artifact"] == "m0_no_dark_rule_derivation_provenance_leakage_v14"
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_RULE_DERIVATION_CONTRACT_V13",
            "rule_derivation_artifact": "m0_no_dark_expression_rule_derivation_v13",
            "required_derivation_slots": "6",
            "ready_derivation_slots": "6",
            "blocked_derivation_slots": "0",
            "derivation_records_written": "0",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_RULE_DERIVATION_READY_FOR_SOURCE_BASIS",
            "next_required_artifact": "m0_no_dark_expression_source_basis_v13",
            "claim_boundary": "m0_no_dark_expression_rule_derivation_contract_only_no_derivation_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v13_m0_no_dark_expression_source_basis_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_source_basis_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_source_basis_summary_v13.csv").open()))
    assert len(rows) == 6
    assert {row["basis_id"] for row in rows} == {
        "M0NDESB13_SOURCE_FREEZE_BASIS",
        "M0NDESB13_NO_DARK_EXCLUSION_BASIS",
        "M0NDESB13_MORPHOLOGY_READOUT_BASIS",
        "M0NDESB13_U_READ_ADMISSIBILITY_BASIS",
        "M0NDESB13_BARYONIC_BINDING_BASIS",
        "M0NDESB13_FAILURE_ROUTE_BASIS",
    }
    assert all(row["basis_status"] == "READY" for row in rows)
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_SOURCE_BASIS_V13",
            "source_basis_artifact": "m0_no_dark_expression_source_basis_v13",
            "derivation_contract_status": "READY",
            "basis_rows": "6",
            "ready_basis_rows": "6",
            "blocked_basis_rows": "0",
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_SOURCE_BASIS_READY",
            "next_required_artifact": "m0_no_dark_expression_admissibility_rule_v13",
            "claim_boundary": "m0_no_dark_expression_source_basis_only_no_rule_no_formula_no_scores",
        }
    ]


def test_v13_m0_no_dark_expression_admissibility_rule_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_admissibility_rule_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_admissibility_rule_summary_v13.csv").open()))
    assert len(rows) == 6
    assert {row["admissibility_id"] for row in rows} == {
        "M0NDADM13_SOURCE_FREEZE_ADMISSIBILITY",
        "M0NDADM13_NO_DARK_EXCLUSION_ADMISSIBILITY",
        "M0NDADM13_MORPHOLOGY_READOUT_ADMISSIBILITY",
        "M0NDADM13_U_READ_MARKER_ADMISSIBILITY",
        "M0NDADM13_BARYONIC_BINDING_ADMISSIBILITY",
        "M0NDADM13_FAILURE_ROUTE_ADMISSIBILITY",
    }
    assert all(row["admissibility_status"] == "READY" for row in rows)
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_ADMISSIBILITY_RULE_V13",
            "admissibility_artifact": "m0_no_dark_expression_admissibility_rule_v13",
            "source_basis_status": "READY",
            "admissibility_rows": "6",
            "ready_admissibility_rows": "6",
            "blocked_admissibility_rows": "0",
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_ADMISSIBILITY_RULE_READY",
            "next_required_artifact": "m0_no_dark_expression_null_fallback_policy_v13",
            "claim_boundary": "m0_no_dark_expression_admissibility_rule_only_no_source_rule_no_formula_no_scores",
        }
    ]


def test_v13_m0_no_dark_expression_null_fallback_policy_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_null_fallback_policy_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_null_fallback_policy_summary_v13.csv").open()))
    assert len(rows) == 6
    assert {row["policy_id"] for row in rows} == {
        "M0NDNFB13_SOURCE_FREEZE_NULL_POLICY",
        "M0NDNFB13_NO_DARK_CONSTRAINT_POLICY",
        "M0NDNFB13_MORPHOLOGY_LABEL_POLICY",
        "M0NDNFB13_U_READ_INCOMPARABILITY_POLICY",
        "M0NDNFB13_BARYONIC_BINDING_POLICY",
        "M0NDNFB13_FAILURE_ROUTE_POLICY",
    }
    assert all(row["policy_status"] == "READY" for row in rows)
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_NULL_FALLBACK_POLICY_V13",
            "null_fallback_artifact": "m0_no_dark_expression_null_fallback_policy_v13",
            "admissibility_status": "READY",
            "policy_rows": "6",
            "ready_policy_rows": "6",
            "blocked_policy_rows": "0",
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_NULL_FALLBACK_POLICY_READY",
            "next_required_artifact": "m0_no_dark_expression_output_class_v13",
            "claim_boundary": "m0_no_dark_expression_null_fallback_policy_only_no_source_rule_no_formula_no_scores",
        }
    ]


def test_v13_m0_no_dark_expression_output_class_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_output_class_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_output_class_summary_v13.csv").open()))
    assert len(rows) == 6
    assert {row["output_class_id"] for row in rows} == {
        "M0NDOC13_SOURCE_DOMAIN_OUTPUT_CLASS",
        "M0NDOC13_NO_DARK_CONSTRAINT_OUTPUT_CLASS",
        "M0NDOC13_MORPHOLOGY_FACTOR_OUTPUT_CLASS",
        "M0NDOC13_U_READ_MARKER_OUTPUT_CLASS",
        "M0NDOC13_BARYONIC_BINDING_OUTPUT_CLASS",
        "M0NDOC13_FAILURE_ROUTE_OUTPUT_CLASS",
    }
    assert all(row["output_class_status"] == "READY" for row in rows)
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_OUTPUT_CLASS_V13",
            "output_class_artifact": "m0_no_dark_expression_output_class_v13",
            "null_fallback_status": "READY",
            "output_class_rows": "6",
            "ready_output_class_rows": "6",
            "blocked_output_class_rows": "0",
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_OUTPUT_CLASS_READY",
            "next_required_artifact": "m0_no_dark_expression_source_rule_leakage_audit_v13",
            "claim_boundary": "m0_no_dark_expression_output_class_only_no_source_rule_no_formula_no_scores",
        }
    ]


def test_v13_m0_no_dark_expression_source_rule_leakage_audit_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_source_rule_leakage_audit_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_source_rule_leakage_audit_summary_v13.csv").open()))
    assert len(rows) == 6
    assert {row["audit_id"] for row in rows} == {
        "M0NDSRLA13_SOURCE_DOMAIN_LEAKAGE_AUDIT",
        "M0NDSRLA13_NO_DARK_CONSTRAINT_LEAKAGE_AUDIT",
        "M0NDSRLA13_MORPHOLOGY_FACTOR_LEAKAGE_AUDIT",
        "M0NDSRLA13_U_READ_MARKER_LEAKAGE_AUDIT",
        "M0NDSRLA13_BARYONIC_BINDING_LEAKAGE_AUDIT",
        "M0NDSRLA13_FAILURE_ROUTE_LEAKAGE_AUDIT",
    }
    assert all(row["audit_status"] == "READY" for row in rows)
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_SOURCE_RULE_LEAKAGE_AUDIT_V13",
            "source_rule_leakage_audit_artifact": "m0_no_dark_expression_source_rule_leakage_audit_v13",
            "output_class_status": "READY",
            "audit_rows": "6",
            "ready_audit_rows": "6",
            "blocked_audit_rows": "0",
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_SOURCE_RULE_LEAKAGE_AUDIT_READY",
            "next_required_artifact": "m0_no_dark_expression_symbolic_form_v12",
            "claim_boundary": "m0_no_dark_expression_source_rule_leakage_audit_only_no_rule_no_formula_no_scores",
        }
    ]


def test_v12_m0_no_dark_expression_source_rule_contract_ready_for_symbolic_form_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_source_rule_contract_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_source_rule_contract_summary_v12.csv").open()))
    assert len(rows) == 6
    assert {row["source_rule_slot_id"] for row in rows} == {
        "M0NDESR12_RULE_DERIVATION",
        "M0NDESR12_SOURCE_BASIS",
        "M0NDESR12_ADMISSIBILITY",
        "M0NDESR12_NULL_AND_FALLBACK",
        "M0NDESR12_OUTPUT_CLASS",
        "M0NDESR12_LEAKAGE_AUDIT",
    }
    assert all(row["source_rule_claim_allowed"] == "false" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert rows[0]["completion_status"] == "READY"
    assert rows[0]["next_required_artifact"] == "m0_no_dark_expression_source_basis_v13"
    assert rows[1]["completion_status"] == "READY"
    assert rows[1]["next_required_artifact"] == "m0_no_dark_expression_source_basis_v13"
    assert rows[2]["completion_status"] == "READY"
    assert rows[2]["next_required_artifact"] == "m0_no_dark_expression_admissibility_rule_v13"
    assert rows[3]["completion_status"] == "READY"
    assert rows[3]["next_required_artifact"] == "m0_no_dark_expression_null_fallback_policy_v13"
    assert rows[4]["completion_status"] == "READY"
    assert rows[4]["next_required_artifact"] == "m0_no_dark_expression_output_class_v13"
    assert rows[5]["completion_status"] == "READY"
    assert rows[5]["next_required_artifact"] == "m0_no_dark_expression_source_rule_leakage_audit_v13"
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_SOURCE_RULE_CONTRACT_V12",
            "source_rule_artifact": "m0_no_dark_expression_source_rule_v12",
            "required_source_rule_slots": "6",
            "ready_source_rule_slots": "6",
            "blocked_source_rule_slots": "0",
            "source_rules_written": "0",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_SOURCE_RULE_READY_FOR_SYMBOLIC_FORM",
            "next_required_artifact": "m0_no_dark_expression_symbolic_form_v12",
            "claim_boundary": "m0_no_dark_expression_source_rule_contract_only_no_rule_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v12_m0_no_dark_expression_symbolic_form_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_symbolic_form_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_symbolic_form_summary_v12.csv").open()))
    assert len(rows) == 6
    assert {row["symbolic_component_id"] for row in rows} == {
        "M0NDSF12_SOURCE_STATE_PLACEHOLDER",
        "M0NDSF12_NO_DARK_CONSTRAINT_PLACEHOLDER",
        "M0NDSF12_BARYONIC_INPUT_PLACEHOLDER",
        "M0NDSF12_READOUT_OPERATOR_PLACEHOLDER",
        "M0NDSF12_FAILURE_ROUTE_PLACEHOLDER",
        "M0NDSF12_FORM_ASSEMBLY_SHELL",
    }
    assert all(row["symbolic_component_status"] == "READY" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_SYMBOLIC_FORM_V12",
            "symbolic_form_artifact": "m0_no_dark_expression_symbolic_form_v12",
            "source_rule_contract_status": "READY",
            "symbolic_components": "6",
            "ready_symbolic_components": "6",
            "blocked_symbolic_components": "0",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_SYMBOLIC_FORM_READY",
            "next_required_artifact": "m0_no_dark_expression_input_domain_v12",
            "claim_boundary": "m0_no_dark_expression_symbolic_form_only_shell_no_formula_no_scores",
        }
    ]


def test_v12_m0_no_dark_expression_input_domain_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_input_domain_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_input_domain_summary_v12.csv").open()))
    assert len(rows) == 6
    assert {row["input_domain_id"] for row in rows} == {
        "M0NDID12_SOURCE_STATE_DOMAIN",
        "M0NDID12_NO_DARK_CONSTRAINT_DOMAIN",
        "M0NDID12_BARYONIC_INPUT_DOMAIN",
        "M0NDID12_READOUT_OPERATOR_DOMAIN",
        "M0NDID12_FAILURE_ROUTE_DOMAIN",
        "M0NDID12_FORM_ASSEMBLY_DOMAIN",
    }
    assert all(row["input_domain_status"] == "READY" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_INPUT_DOMAIN_V12",
            "input_domain_artifact": "m0_no_dark_expression_input_domain_v12",
            "symbolic_form_status": "READY",
            "input_domain_rows": "6",
            "ready_input_domain_rows": "6",
            "blocked_input_domain_rows": "0",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_INPUT_DOMAIN_READY",
            "next_required_artifact": "m0_no_dark_expression_coefficient_freeze_v12",
            "claim_boundary": "m0_no_dark_expression_input_domain_only_no_formula_no_scores",
        }
    ]


def test_v12_m0_no_dark_expression_coefficient_freeze_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_coefficient_freeze_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_coefficient_freeze_summary_v12.csv").open()))
    assert len(rows) == 6
    assert {row["coefficient_policy_id"] for row in rows} == {
        "M0NDCF12_SOURCE_STATE_COEFFICIENT_POLICY",
        "M0NDCF12_NO_DARK_CONSTRAINT_COEFFICIENT_POLICY",
        "M0NDCF12_BARYONIC_INPUT_COEFFICIENT_POLICY",
        "M0NDCF12_READOUT_OPERATOR_COEFFICIENT_POLICY",
        "M0NDCF12_FAILURE_ROUTE_COEFFICIENT_POLICY",
        "M0NDCF12_ASSEMBLY_COEFFICIENT_POLICY",
    }
    assert all(row["coefficient_policy_status"] == "READY" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_COEFFICIENT_FREEZE_V12",
            "coefficient_freeze_artifact": "m0_no_dark_expression_coefficient_freeze_v12",
            "input_domain_status": "READY",
            "coefficient_policy_rows": "6",
            "ready_coefficient_policy_rows": "6",
            "blocked_coefficient_policy_rows": "0",
            "numeric_coefficient_values_written": "0",
            "numeric_parameter_counts_written": "0",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_COEFFICIENT_FREEZE_READY",
            "next_required_artifact": "m0_no_dark_expression_dimensional_audit_v12",
            "claim_boundary": "m0_no_dark_expression_coefficient_freeze_only_policy_no_values_no_scores",
        }
    ]


def test_v12_m0_no_dark_expression_dimensional_audit_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_dimensional_audit_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_dimensional_audit_summary_v12.csv").open()))
    assert len(rows) == 6
    assert {row["dimensional_audit_id"] for row in rows} == {
        "M0NDDA12_SOURCE_STATE_UNIT_AUDIT",
        "M0NDDA12_NO_DARK_CONSTRAINT_UNIT_AUDIT",
        "M0NDDA12_BARYONIC_INPUT_UNIT_AUDIT",
        "M0NDDA12_READOUT_OPERATOR_UNIT_AUDIT",
        "M0NDDA12_FAILURE_ROUTE_UNIT_AUDIT",
        "M0NDDA12_ASSEMBLY_UNIT_AUDIT",
    }
    assert all(row["dimensional_audit_status"] == "READY" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_DIMENSIONAL_AUDIT_V12",
            "dimensional_audit_artifact": "m0_no_dark_expression_dimensional_audit_v12",
            "coefficient_freeze_status": "READY",
            "dimensional_audit_rows": "6",
            "ready_dimensional_audit_rows": "6",
            "blocked_dimensional_audit_rows": "0",
            "velocity_formula_written": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_DIMENSIONAL_AUDIT_READY",
            "next_required_artifact": "m0_no_dark_expression_machine_form_v12",
            "claim_boundary": "m0_no_dark_expression_dimensional_audit_only_no_formula_no_scores",
        }
    ]


def test_v12_m0_no_dark_expression_machine_form_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_machine_form_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_expression_machine_form_summary_v12.csv").open()))
    assert len(rows) == 6
    assert {row["machine_form_id"] for row in rows} == {
        "M0NDMF12_SOURCE_STATE_SERIALIZATION",
        "M0NDMF12_NO_DARK_CONSTRAINT_SERIALIZATION",
        "M0NDMF12_BARYONIC_INPUT_SERIALIZATION",
        "M0NDMF12_READOUT_OPERATOR_SERIALIZATION",
        "M0NDMF12_FAILURE_ROUTE_SERIALIZATION",
        "M0NDMF12_ASSEMBLY_SERIALIZATION",
    }
    assert all(row["machine_form_status"] == "READY" for row in rows)
    assert all(row["frozen_expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_MACHINE_FORM_V12",
            "machine_form_artifact": "m0_no_dark_expression_machine_form_v12",
            "dimensional_audit_status": "READY",
            "machine_form_rows": "6",
            "ready_machine_form_rows": "6",
            "blocked_machine_form_rows": "0",
            "serialized_prediction_callable_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_MACHINE_FORM_READY",
            "next_required_artifact": "family_prediction_tables_v08.csv",
            "claim_boundary": "m0_no_dark_expression_machine_form_only_serialization_contract_no_formula_no_scores",
        }
    ]


def test_v11_m0_no_dark_frozen_expression_contract_ready_for_prediction_writer_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_frozen_expression_contract_v11.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_frozen_expression_contract_summary_v11.csv").open()))
    assert len(rows) == 6
    assert {row["freeze_slot_id"] for row in rows} == {
        "M0NDFE11_SOURCE_RULE",
        "M0NDFE11_SYMBOLIC_FORM",
        "M0NDFE11_INPUT_DOMAIN",
        "M0NDFE11_COEFFICIENT_FREEZE",
        "M0NDFE11_DIMENSIONAL_AUDIT",
        "M0NDFE11_MACHINE_FORM",
    }
    assert all(row["frozen_expression_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert rows[0]["completion_status"] == "READY"
    assert rows[0]["next_required_artifact"] == "m0_no_dark_expression_symbolic_form_v12"
    assert rows[1]["completion_status"] == "READY"
    assert rows[1]["next_required_artifact"] == "m0_no_dark_expression_symbolic_form_v12"
    assert rows[2]["completion_status"] == "READY"
    assert rows[2]["next_required_artifact"] == "m0_no_dark_expression_input_domain_v12"
    assert rows[3]["completion_status"] == "READY"
    assert rows[3]["next_required_artifact"] == "m0_no_dark_expression_coefficient_freeze_v12"
    assert rows[4]["completion_status"] == "READY"
    assert rows[4]["next_required_artifact"] == "m0_no_dark_expression_dimensional_audit_v12"
    assert rows[5]["completion_status"] == "READY"
    assert rows[5]["next_required_artifact"] == "m0_no_dark_expression_machine_form_v12"
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_FROZEN_EXPRESSION_CONTRACT_V11",
            "frozen_expression_artifact": "m0_no_dark_frozen_expression_v11",
            "required_freeze_slots": "6",
            "ready_freeze_slots": "6",
            "blocked_freeze_slots": "0",
            "frozen_expressions_written": "0",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FROZEN_EXPRESSION_READY_FOR_PREDICTION_WRITER",
            "next_required_artifact": "family_prediction_tables_v08.csv",
            "claim_boundary": "m0_no_dark_frozen_expression_contract_only_no_expression_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v10_m0_no_dark_kernel_expression_contract_blocks_frozen_expression() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_kernel_expression_contract_v10.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_kernel_expression_contract_summary_v10.csv").open()))
    assert len(rows) == 5
    assert {row["expression_slot_id"] for row in rows} == {
        "M0NDKE10_FROZEN_EXPRESSION",
        "M0NDKE10_VARIABLE_BINDINGS",
        "M0NDKE10_CONSTANTS",
        "M0NDKE10_DIMENSIONAL_PATH",
        "M0NDKE10_SERIALIZED_FORM",
    }
    assert rows[0]["expression_claim_allowed"] == "true"
    assert all(row["expression_claim_allowed"] == "false" for row in rows[1:])
    assert all(row["kernel_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert rows[0]["next_required_artifact"] == "m0_no_dark_frozen_expression_body_v14"
    assert all(row["completion_status"] == "READY" for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_KERNEL_EXPRESSION_CONTRACT_V10",
            "kernel_expression_artifact": "m0_no_dark_kernel_expression_v10",
            "required_expression_slots": "5",
            "ready_expression_slots": "5",
            "blocked_expression_slots": "0",
            "frozen_expressions_written": "1",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_KERNEL_EXPRESSION_READY_FOR_KERNEL_FREEZE",
            "next_required_artifact": "m0_no_dark_equation_kernel_v09",
            "claim_boundary": "m0_no_dark_kernel_expression_contract_only_no_expression_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v10_m0_no_dark_kernel_expression_interface_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_kernel_expression_interface_v10.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_kernel_expression_interface_summary_v10.csv").open()))
    assert len(rows) == 4
    assert {row["expression_slot_id"] for row in rows} == {
        "M0NDKE10_VARIABLE_BINDINGS",
        "M0NDKE10_CONSTANTS",
        "M0NDKE10_DIMENSIONAL_PATH",
        "M0NDKE10_SERIALIZED_FORM",
    }
    assert all(row["interface_status"] == "READY" for row in rows)
    assert all(row["expression_claim_allowed"] == "false" for row in rows)
    assert all(row["kernel_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_KERNEL_EXPRESSION_INTERFACE_V10",
            "interface_artifact": "m0_no_dark_kernel_expression_interface_v10",
            "equation_kernel_interface_status": "READY",
            "frozen_expression_contract_status": "READY_CONTRACT_ONLY_NO_PAYLOAD",
            "interface_rows": "4",
            "ready_interface_rows": "4",
            "blocked_interface_rows": "0",
            "frozen_expression_payload_written": "false",
            "expression_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_KERNEL_EXPRESSION_INTERFACE_READY",
            "next_required_artifact": "m0_no_dark_frozen_expression_payload_v11",
            "claim_boundary": "m0_no_dark_kernel_expression_interface_only_no_payload_no_predictions_no_scores",
        }
    ]


def test_v11_m0_no_dark_frozen_expression_payload_contract_ready_for_kernel_expression() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_frozen_expression_payload_v11.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_frozen_expression_payload_summary_v11.csv").open()))
    assert len(rows) == 6
    assert {row["payload_slot_id"] for row in rows} == {
        "M0NDFEP11_EXPRESSION_STATEMENT",
        "M0NDFEP11_SYMBOL_BINDING_TABLE",
        "M0NDFEP11_CONSTANT_POLICY",
        "M0NDFEP11_DIMENSIONAL_TRACE",
        "M0NDFEP11_MACHINE_PAYLOAD",
        "M0NDFEP11_LEAKAGE_CERTIFICATE",
    }
    assert all(row["payload_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert rows[0]["completion_status"] == "READY"
    assert rows[0]["next_required_artifact"] == "m0_no_dark_frozen_expression_payload_v11"
    assert rows[1]["completion_status"] == "READY"
    assert rows[1]["next_required_artifact"] == "m0_no_dark_payload_symbol_binding_table_v12"
    assert rows[2]["completion_status"] == "READY"
    assert rows[2]["next_required_artifact"] == "m0_no_dark_payload_constant_policy_v12"
    assert rows[3]["completion_status"] == "READY"
    assert rows[3]["next_required_artifact"] == "m0_no_dark_payload_dimensional_trace_v12"
    assert rows[4]["completion_status"] == "READY"
    assert rows[4]["next_required_artifact"] == "m0_no_dark_payload_machine_form_v12"
    assert rows[5]["completion_status"] == "READY"
    assert rows[5]["next_required_artifact"] == "m0_no_dark_payload_leakage_certificate_v12"
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_V11",
            "payload_artifact": "m0_no_dark_frozen_expression_payload_v11",
            "kernel_expression_interface_status": "READY",
            "required_payload_slots": "6",
            "ready_payload_slots": "6",
            "blocked_payload_slots": "0",
            "frozen_expression_payload_written": "true",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_FOR_KERNEL_EXPRESSION",
            "next_required_artifact": "family_prediction_tables_v08.csv",
            "claim_boundary": "m0_no_dark_frozen_expression_payload_contract_only_no_payload_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v12_m0_no_dark_payload_symbol_binding_table_blocks_constant_policy() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_payload_symbol_binding_table_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_payload_symbol_binding_table_summary_v12.csv").open()))
    assert len(rows) == 6
    assert {row["binding_id"] for row in rows} == {
        "M0NDPSBT12_SOURCE_STATE_SYMBOL",
        "M0NDPSBT12_BARYONIC_INPUT_SYMBOL",
        "M0NDPSBT12_RADIUS_GRID_SYMBOL",
        "M0NDPSBT12_READOUT_OPERATOR_SYMBOL",
        "M0NDPSBT12_GUARD_SYMBOL",
        "M0NDPSBT12_ASSEMBLY_SYMBOL",
    }
    assert all(row["completion_status"] == "READY" for row in rows)
    assert all(row["next_required_artifact"] == "m0_no_dark_payload_constant_policy_v12" for row in rows)
    assert all(row["binding_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_PAYLOAD_SYMBOL_BINDING_TABLE_V12",
            "symbol_binding_artifact": "m0_no_dark_payload_symbol_binding_table_v12",
            "payload_contract_status": "READY",
            "binding_rows": "6",
            "ready_binding_rows": "6",
            "blocked_binding_rows": "0",
            "symbol_binding_table_written": "true",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PAYLOAD_SYMBOL_BINDING_TABLE_READY_FOR_CONSTANT_POLICY",
            "next_required_artifact": "m0_no_dark_payload_constant_policy_v12",
            "claim_boundary": "m0_no_dark_payload_symbol_binding_table_only_bindings_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v12_m0_no_dark_payload_constant_policy_blocks_dimensional_trace() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_payload_constant_policy_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_payload_constant_policy_summary_v12.csv").open()))
    assert len(rows) == 6
    assert {row["policy_id"] for row in rows} == {
        "M0NDPCP12_FIXED_SOURCE_CONSTANTS",
        "M0NDPCP12_FREE_PARAMETER_DECLARATION",
        "M0NDPCP12_SCALE_POLICY",
        "M0NDPCP12_BRANCH_SWITCH_POLICY",
        "M0NDPCP12_NULL_FALLBACK_CONSTANT_POLICY",
        "M0NDPCP12_HANDOFF_TO_DIMENSIONAL_TRACE",
    }
    assert all(row["completion_status"] == "READY" for row in rows)
    assert all(row["next_required_artifact"] == "m0_no_dark_payload_dimensional_trace_v12" for row in rows)
    assert all(row["policy_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_PAYLOAD_CONSTANT_POLICY_V12",
            "constant_policy_artifact": "m0_no_dark_payload_constant_policy_v12",
            "symbol_binding_status": "READY",
            "policy_rows": "6",
            "ready_policy_rows": "6",
            "blocked_policy_rows": "0",
            "constant_policy_written": "true",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PAYLOAD_CONSTANT_POLICY_READY_FOR_DIMENSIONAL_TRACE",
            "next_required_artifact": "m0_no_dark_payload_dimensional_trace_v12",
            "claim_boundary": "m0_no_dark_payload_constant_policy_only_policy_no_values_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v12_m0_no_dark_payload_dimensional_trace_blocks_machine_payload() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_payload_dimensional_trace_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_payload_dimensional_trace_summary_v12.csv").open()))
    assert len(rows) == 6
    assert {row["trace_id"] for row in rows} == {
        "M0NDPDT12_INPUT_DIMENSION_CLASSES",
        "M0NDPDT12_OPERATOR_DIMENSION_EFFECTS",
        "M0NDPDT12_CONSTANT_UNIT_COMPATIBILITY",
        "M0NDPDT12_OUTPUT_UNIT_TARGET",
        "M0NDPDT12_NULL_FALLBACK_DIMENSION_POLICY",
        "M0NDPDT12_HANDOFF_TO_MACHINE_PAYLOAD",
    }
    assert all(row["completion_status"] == "READY" for row in rows)
    assert all(row["next_required_artifact"] == "m0_no_dark_payload_machine_form_v12" for row in rows)
    assert all(row["trace_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_PAYLOAD_DIMENSIONAL_TRACE_V12",
            "dimensional_trace_artifact": "m0_no_dark_payload_dimensional_trace_v12",
            "constant_policy_status": "READY",
            "trace_rows": "6",
            "ready_trace_rows": "6",
            "blocked_trace_rows": "0",
            "dimensional_trace_written": "true",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PAYLOAD_DIMENSIONAL_TRACE_READY_FOR_MACHINE_PAYLOAD",
            "next_required_artifact": "m0_no_dark_payload_machine_form_v12",
            "claim_boundary": "m0_no_dark_payload_dimensional_trace_only_units_no_formula_no_values_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v12_m0_no_dark_payload_machine_form_blocks_leakage_certificate() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_payload_machine_form_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_payload_machine_form_summary_v12.csv").open()))
    assert len(rows) == 6
    assert {row["machine_payload_id"] for row in rows} == {
        "M0NDPMF12_SOURCE_STATE_PAYLOAD",
        "M0NDPMF12_BARYONIC_RADIAL_PAYLOAD",
        "M0NDPMF12_OPERATOR_GUARD_PAYLOAD",
        "M0NDPMF12_CONSTANT_POLICY_PAYLOAD",
        "M0NDPMF12_DIMENSION_TRACE_PAYLOAD",
        "M0NDPMF12_HANDOFF_TO_LEAKAGE_CERTIFICATE",
    }
    assert all(row["completion_status"] == "READY" for row in rows)
    assert all(row["next_required_artifact"] == "m0_no_dark_payload_leakage_certificate_v12" for row in rows)
    assert all(row["machine_payload_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_PAYLOAD_MACHINE_FORM_V12",
            "machine_payload_artifact": "m0_no_dark_payload_machine_form_v12",
            "dimensional_trace_status": "READY",
            "machine_payload_rows": "6",
            "ready_machine_payload_rows": "6",
            "blocked_machine_payload_rows": "0",
            "machine_payload_written": "true",
            "prediction_callable_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PAYLOAD_MACHINE_FORM_READY_FOR_LEAKAGE_CERTIFICATE",
            "next_required_artifact": "m0_no_dark_payload_leakage_certificate_v12",
            "claim_boundary": "m0_no_dark_payload_machine_form_only_serialization_no_formula_no_values_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v12_m0_no_dark_payload_leakage_certificate_blocks_formula_tables() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_payload_leakage_certificate_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_payload_leakage_certificate_summary_v12.csv").open()))
    assert len(rows) == 6
    assert {row["certificate_id"] for row in rows} == {
        "M0NDPLC12_FORBIDDEN_INPUT_MANIFEST",
        "M0NDPLC12_FREEZE_ORDER_CERTIFICATE",
        "M0NDPLC12_SERIALIZATION_HASH_POLICY",
        "M0NDPLC12_SOURCE_PROVENANCE_GUARDS",
        "M0NDPLC12_NULL_FALLBACK_STOP_CERTIFICATE",
        "M0NDPLC12_HANDOFF_TO_FORMULA_TABLES",
    }
    assert all(row["completion_status"] == "READY" for row in rows)
    assert all(row["next_required_artifact"] == "family_prediction_tables_v08.csv" for row in rows)
    assert all(row["certificate_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_PAYLOAD_LEAKAGE_CERTIFICATE_V12",
            "payload_leakage_certificate_artifact": "m0_no_dark_payload_leakage_certificate_v12",
            "machine_payload_status": "READY",
            "certificate_rows": "6",
            "ready_certificate_rows": "6",
            "blocked_certificate_rows": "0",
            "payload_leakage_certificate_written": "true",
            "prediction_callable_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PAYLOAD_LEAKAGE_CERTIFICATE_READY_FOR_FORMULA_TABLES",
            "next_required_artifact": "family_prediction_tables_v08.csv",
            "claim_boundary": "m0_no_dark_payload_leakage_certificate_only_no_formula_no_values_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v14_m0_no_dark_frozen_expression_body_formulated_no_velocity_formula() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_frozen_expression_body_v14.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_frozen_expression_body_summary_v14.csv").open()))
    assert len(rows) == 6
    assert {row["body_component"] for row in rows} == {
        "scope_and_family_binding",
        "argument_vector",
        "assembly_body",
        "no_dark_exclusion",
        "output_class",
        "freeze_guard",
    }
    assert all(row["completion_status"] == "READY" for row in rows)
    assert all(row["expression_body_claim_allowed"] == "true" for row in rows)
    assert all(row["velocity_formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["dark_sector_verdict_allowed"] == "false" for row in rows)
    assert rows[2]["body_component"] == "assembly_body"
    assert "Assemble_M0" in rows[2]["frozen_expression_body_statement"]
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_FROZEN_EXPRESSION_BODY_V14",
            "body_artifact": "m0_no_dark_frozen_expression_body_v14",
            "payload_status": "READY",
            "body_rows": "6",
            "ready_body_rows": "6",
            "blocked_body_rows": "0",
            "expression_body_written": "true",
            "velocity_formula_written": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "M0_NO_DARK_FROZEN_EXPRESSION_BODY_READY_FOR_KERNEL_EXPRESSION_REVIEW",
            "next_required_artifact": "m0_no_dark_kernel_expression_contract_v10",
            "claim_boundary": "m0_no_dark_frozen_expression_body_definition_only_no_velocity_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v12_m0_no_dark_frozen_expression_statement_contract_blocks_source_statement() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_frozen_expression_statement_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_frozen_expression_statement_summary_v12.csv").open()))
    assert len(rows) == 6
    assert {row["statement_slot_id"] for row in rows} == {
        "M0NDFES12_SOURCE_SIDE_STATEMENT",
        "M0NDFES12_TERM_LIST",
        "M0NDFES12_ARGUMENT_SIGNATURE",
        "M0NDFES12_CONSTRAINT_GUARDS",
        "M0NDFES12_PRE_DIMENSIONAL_PROOF",
        "M0NDFES12_FREEZE_PROVENANCE",
    }
    assert all(row["statement_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert rows[0]["next_required_artifact"] == "m0_no_dark_source_side_expression_statement_v13"
    assert rows[0]["completion_status"] == "READY"
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_V12",
            "statement_artifact": "m0_no_dark_frozen_expression_statement_v12",
            "kernel_expression_interface_status": "READY",
            "required_statement_slots": "6",
            "ready_statement_slots": "6",
            "blocked_statement_slots": "0",
            "source_side_expression_statement_written": "true",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FOR_PAYLOAD",
            "next_required_artifact": "m0_no_dark_frozen_expression_payload_v11",
            "claim_boundary": "m0_no_dark_frozen_expression_statement_contract_only_no_statement_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v13_m0_no_dark_source_side_expression_statement_envelope_blocks_term_list() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_source_side_expression_statement_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_source_side_expression_statement_summary_v13.csv").open()))
    assert len(rows) == 6
    assert {row["statement_component_id"] for row in rows} == {
        "M0NDSS13_STATEMENT_ENVELOPE",
        "M0NDSS13_SOURCE_SIDE_SCOPE",
        "M0NDSS13_NO_DARK_FAMILY_BINDING",
        "M0NDSS13_OUTPUT_INTENT",
        "M0NDSS13_FREEZE_GUARD",
        "M0NDSS13_NEXT_SLOT_HANDOFF",
    }
    assert all(row["completion_status"] == "READY" for row in rows)
    assert all(row["next_required_artifact"] == "m0_no_dark_statement_term_list_v13" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_SOURCE_SIDE_EXPRESSION_STATEMENT_V13",
            "statement_artifact": "m0_no_dark_source_side_expression_statement_v13",
            "frozen_expression_statement_contract_status": "READY",
            "statement_components": "6",
            "ready_statement_components": "6",
            "blocked_statement_components": "0",
            "source_side_statement_record_written": "true",
            "statement_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_SOURCE_SIDE_EXPRESSION_STATEMENT_READY_FOR_TERM_LIST",
            "next_required_artifact": "m0_no_dark_statement_term_list_v13",
            "claim_boundary": "m0_no_dark_source_side_expression_statement_envelope_only_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v13_m0_no_dark_statement_term_list_blocks_argument_signature() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_statement_term_list_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_statement_term_list_summary_v13.csv").open()))
    assert len(rows) == 6
    assert {row["term_entry_id"] for row in rows} == {
        "M0NDSTL13_SOURCE_STATE_TERM",
        "M0NDSTL13_BARYONIC_INPUT_TERM",
        "M0NDSTL13_READOUT_OPERATOR_TERM",
        "M0NDSTL13_NO_DARK_CONSTRAINT_TERM",
        "M0NDSTL13_NULL_FALLBACK_TERM",
        "M0NDSTL13_ASSEMBLY_OPERATOR_TERM",
    }
    assert all(row["completion_status"] == "READY" for row in rows)
    assert all(row["next_required_artifact"] == "m0_no_dark_statement_argument_signature_v13" for row in rows)
    assert all(row["term_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_STATEMENT_TERM_LIST_V13",
            "term_list_artifact": "m0_no_dark_statement_term_list_v13",
            "source_side_statement_status": "READY",
            "term_entries": "6",
            "ready_term_entries": "6",
            "blocked_term_entries": "0",
            "term_list_written": "true",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_STATEMENT_TERM_LIST_READY_FOR_ARGUMENT_SIGNATURE",
            "next_required_artifact": "m0_no_dark_statement_argument_signature_v13",
            "claim_boundary": "m0_no_dark_statement_term_list_only_term_classes_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v13_m0_no_dark_statement_argument_signature_blocks_constraint_guards() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_statement_argument_signature_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_statement_argument_signature_summary_v13.csv").open()))
    assert len(rows) == 6
    assert {row["argument_slot_id"] for row in rows} == {
        "M0NDSAS13_SOURCE_STATE_ARGUMENT",
        "M0NDSAS13_BARYONIC_INPUT_ARGUMENT",
        "M0NDSAS13_RADIUS_GRID_ARGUMENT",
        "M0NDSAS13_READOUT_OPERATOR_ARGUMENT",
        "M0NDSAS13_GUARD_ARGUMENT",
        "M0NDSAS13_ASSEMBLY_ARGUMENT",
    }
    assert all(row["completion_status"] == "READY" for row in rows)
    assert all(row["next_required_artifact"] == "m0_no_dark_statement_constraint_guards_v13" for row in rows)
    assert all(row["argument_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_STATEMENT_ARGUMENT_SIGNATURE_V13",
            "argument_signature_artifact": "m0_no_dark_statement_argument_signature_v13",
            "term_list_status": "READY",
            "argument_slots": "6",
            "ready_argument_slots": "6",
            "blocked_argument_slots": "0",
            "argument_signature_written": "true",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_STATEMENT_ARGUMENT_SIGNATURE_READY_FOR_CONSTRAINT_GUARDS",
            "next_required_artifact": "m0_no_dark_statement_constraint_guards_v13",
            "claim_boundary": "m0_no_dark_statement_argument_signature_only_bindings_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v13_m0_no_dark_statement_constraint_guards_block_pre_dimensional_proof() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_statement_constraint_guards_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_statement_constraint_guards_summary_v13.csv").open()))
    assert len(rows) == 6
    assert {row["guard_id"] for row in rows} == {
        "M0NDSCG13_DOMAIN_GUARD",
        "M0NDSCG13_NULL_GUARD",
        "M0NDSCG13_GAUGE_GUARD",
        "M0NDSCG13_NO_DARK_GUARD",
        "M0NDSCG13_FALLBACK_GUARD",
        "M0NDSCG13_LEAKAGE_FREEZE_GUARD",
    }
    assert all(row["completion_status"] == "READY" for row in rows)
    assert all(row["next_required_artifact"] == "m0_no_dark_statement_pre_dimensional_proof_v13" for row in rows)
    assert all(row["guard_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_STATEMENT_CONSTRAINT_GUARDS_V13",
            "constraint_guards_artifact": "m0_no_dark_statement_constraint_guards_v13",
            "argument_signature_status": "READY",
            "guard_rows": "6",
            "ready_guard_rows": "6",
            "blocked_guard_rows": "0",
            "constraint_guards_written": "true",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_STATEMENT_CONSTRAINT_GUARDS_READY_FOR_PRE_DIMENSIONAL_PROOF",
            "next_required_artifact": "m0_no_dark_statement_pre_dimensional_proof_v13",
            "claim_boundary": "m0_no_dark_statement_constraint_guards_only_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v13_m0_no_dark_statement_pre_dimensional_proof_blocks_freeze_provenance() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_statement_pre_dimensional_proof_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_statement_pre_dimensional_proof_summary_v13.csv").open()))
    assert len(rows) == 6
    assert {row["proof_step_id"] for row in rows} == {
        "M0NDSPDP13_OUTPUT_CLASS_ROUTE",
        "M0NDSPDP13_ARGUMENT_DIMENSION_PLACEHOLDERS",
        "M0NDSPDP13_OPERATOR_DIMENSION_RULE",
        "M0NDSPDP13_GUARD_DIMENSION_POLICY",
        "M0NDSPDP13_NO_POSTHOC_UNIT_RESCALING",
        "M0NDSPDP13_HANDOFF_TO_FREEZE_PROVENANCE",
    }
    assert all(row["completion_status"] == "READY" for row in rows)
    assert all(row["next_required_artifact"] == "m0_no_dark_statement_freeze_provenance_v13" for row in rows)
    assert all(row["proof_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_STATEMENT_PRE_DIMENSIONAL_PROOF_V13",
            "pre_dimensional_proof_artifact": "m0_no_dark_statement_pre_dimensional_proof_v13",
            "constraint_guards_status": "READY",
            "proof_rows": "6",
            "ready_proof_rows": "6",
            "blocked_proof_rows": "0",
            "pre_dimensional_proof_written": "true",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_STATEMENT_PRE_DIMENSIONAL_PROOF_READY_FOR_FREEZE_PROVENANCE",
            "next_required_artifact": "m0_no_dark_statement_freeze_provenance_v13",
            "claim_boundary": "m0_no_dark_statement_pre_dimensional_proof_only_route_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v13_m0_no_dark_statement_freeze_provenance_blocks_payload_symbol_binding() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_statement_freeze_provenance_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_statement_freeze_provenance_summary_v13.csv").open()))
    assert len(rows) == 6
    assert {row["freeze_record_id"] for row in rows} == {
        "M0NDSFP13_UPSTREAM_ROUTE_HASH",
        "M0NDSFP13_FORBIDDEN_INPUT_CUTOFF",
        "M0NDSFP13_SOURCE_SIDE_ONLY_SCOPE",
        "M0NDSFP13_REPRODUCIBLE_BUILD_HOOK",
        "M0NDSFP13_DOWNSTREAM_PAYLOAD_HANDOFF",
        "M0NDSFP13_DARK_SECTOR_NEUTRALITY",
    }
    assert all(row["completion_status"] == "READY" for row in rows)
    assert all(row["next_required_artifact"] == "m0_no_dark_frozen_expression_payload_v11" for row in rows)
    assert all(row["freeze_claim_allowed"] == "false" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_STATEMENT_FREEZE_PROVENANCE_V13",
            "freeze_provenance_artifact": "m0_no_dark_statement_freeze_provenance_v13",
            "pre_dimensional_proof_status": "READY",
            "freeze_rows": "6",
            "ready_freeze_rows": "6",
            "blocked_freeze_rows": "0",
            "freeze_provenance_written": "true",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_STATEMENT_FREEZE_PROVENANCE_READY_FOR_PAYLOAD",
            "next_required_artifact": "m0_no_dark_frozen_expression_payload_v11",
            "claim_boundary": "m0_no_dark_statement_freeze_provenance_only_route_timing_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v09_m0_no_dark_equation_kernel_contract_accepts_expression_body() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_equation_kernel_contract_v09.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_equation_kernel_contract_summary_v09.csv").open()))
    assert len(rows) == 6
    assert {row["kernel_slot_id"] for row in rows} == {
        "M0NDEK09_EXPRESSION",
        "M0NDEK09_INPUT_BINDING",
        "M0NDEK09_OUTPUT_MAP",
        "M0NDEK09_PARAMETER_AUDIT",
        "M0NDEK09_FAILURE_POLICY",
        "M0NDEK09_REPRODUCIBLE_HOOK",
    }
    assert all(row["kernel_claim_allowed"] == "false" for row in rows)
    assert all(row["equation_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert rows[0]["next_required_artifact"] == "m0_no_dark_kernel_expression_contract_v10"
    assert all(row["completion_status"] == "READY" for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EQUATION_KERNEL_CONTRACT_V09",
            "equation_kernel_artifact": "m0_no_dark_equation_kernel_v09",
            "required_kernel_slots": "6",
            "ready_kernel_slots": "6",
            "blocked_kernel_slots": "0",
            "kernel_expressions_written": "1",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EQUATION_KERNEL_READY_FOR_READOUT_EQUATION",
            "next_required_artifact": "m0_no_dark_readout_equation_v08",
            "claim_boundary": "m0_no_dark_equation_kernel_contract_only_no_kernel_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v09_m0_no_dark_equation_kernel_interface_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_equation_kernel_interface_v09.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_equation_kernel_interface_summary_v09.csv").open()))
    assert len(rows) == 5
    assert {row["kernel_slot_id"] for row in rows} == {
        "M0NDEK09_INPUT_BINDING",
        "M0NDEK09_OUTPUT_MAP",
        "M0NDEK09_PARAMETER_AUDIT",
        "M0NDEK09_FAILURE_POLICY",
        "M0NDEK09_REPRODUCIBLE_HOOK",
    }
    assert all(row["interface_status"] == "READY" for row in rows)
    assert all(row["kernel_claim_allowed"] == "false" for row in rows)
    assert all(row["equation_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EQUATION_KERNEL_INTERFACE_V09",
            "interface_artifact": "m0_no_dark_equation_kernel_interface_v09",
            "readout_equation_interface_status": "READY",
            "interface_rows": "5",
            "ready_interface_rows": "5",
            "blocked_interface_rows": "0",
            "kernel_expression_written": "false",
            "kernel_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EQUATION_KERNEL_INTERFACE_READY",
            "next_required_artifact": "m0_no_dark_kernel_expression_v10",
            "claim_boundary": "m0_no_dark_equation_kernel_interface_only_no_expression_no_predictions_no_scores",
        }
    ]


def test_v08_m0_no_dark_readout_equation_contract_accepts_kernel() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_readout_equation_contract_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_readout_equation_contract_summary_v08.csv").open()))
    assert len(rows) == 6
    assert {row["equation_slot_id"] for row in rows} == {
        "M0NDRE08_KERNEL",
        "M0NDRE08_ARGUMENT_SIGNATURE",
        "M0NDRE08_UNITS",
        "M0NDRE08_PARAMETERS",
        "M0NDRE08_DOMAIN",
        "M0NDRE08_SERIALIZATION",
    }
    assert all(row["equation_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert rows[0]["next_required_artifact"] == "m0_no_dark_equation_kernel_contract_v09"
    assert all(row["completion_status"] == "READY" for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_READOUT_EQUATION_CONTRACT_V08",
            "readout_equation_artifact": "m0_no_dark_readout_equation_v08",
            "required_equation_slots": "6",
            "ready_equation_slots": "6",
            "blocked_equation_slots": "0",
            "equations_written": "0",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_READOUT_EQUATION_READY_FOR_FORMULA_BODY",
            "next_required_artifact": "m0_no_dark_formula_body_v07",
            "claim_boundary": "m0_no_dark_readout_equation_contract_only_no_equation_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v08_m0_no_dark_readout_equation_interface_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_readout_equation_interface_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_readout_equation_interface_summary_v08.csv").open()))
    assert len(rows) == 5
    assert {row["equation_slot_id"] for row in rows} == {
        "M0NDRE08_ARGUMENT_SIGNATURE",
        "M0NDRE08_UNITS",
        "M0NDRE08_PARAMETERS",
        "M0NDRE08_DOMAIN",
        "M0NDRE08_SERIALIZATION",
    }
    assert all(row["interface_status"] == "READY" for row in rows)
    assert all(row["equation_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_READOUT_EQUATION_INTERFACE_V08",
            "interface_artifact": "m0_no_dark_readout_equation_interface_v08",
            "formula_body_interface_status": "READY",
            "interface_rows": "5",
            "ready_interface_rows": "5",
            "blocked_interface_rows": "0",
            "kernel_written": "false",
            "equation_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_READOUT_EQUATION_INTERFACE_READY",
            "next_required_artifact": "m0_no_dark_equation_kernel_v09",
            "claim_boundary": "m0_no_dark_readout_equation_interface_only_no_kernel_no_predictions_no_scores",
        }
    ]


def test_v08_m0_no_dark_formula_body_interface_ready_no_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_formula_body_interface_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_formula_body_interface_summary_v08.csv").open()))
    assert len(rows) == 6
    assert {row["body_slot_id"] for row in rows} == {
        "M0NDB07_SOURCE_ARGUMENTS",
        "M0NDB07_BARYONIC_HANDOFF",
        "M0NDB07_SCALE_LAW",
        "M0NDB07_COEFFICIENT_DOMAIN",
        "M0NDB07_FALLBACK_BRANCHES",
        "M0NDB07_OUTPUT_UNIT_CHECK",
    }
    assert all(row["interface_status"] == "READY" for row in rows)
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_prediction_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_FORMULA_BODY_INTERFACE_V08",
            "interface_artifact": "m0_no_dark_formula_body_interface_v08",
            "machine_form_status": "READY",
            "interface_rows": "6",
            "ready_interface_rows": "6",
            "blocked_interface_rows": "0",
            "readout_equation_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FORMULA_BODY_INTERFACE_READY",
            "next_required_artifact": "m0_no_dark_readout_equation_v08",
            "claim_boundary": "m0_no_dark_formula_body_interface_only_no_equation_no_predictions_no_scores",
        }
    ]


def test_v07_m0_no_dark_formula_body_contract_accepts_readout_equation() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_formula_body_contract_v07.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_formula_body_contract_summary_v07.csv").open()))
    assert len(rows) == 7
    assert {row["body_slot_id"] for row in rows} == {
        "M0NDB07_READOUT_EQUATION",
        "M0NDB07_SOURCE_ARGUMENTS",
        "M0NDB07_BARYONIC_HANDOFF",
        "M0NDB07_SCALE_LAW",
        "M0NDB07_COEFFICIENT_DOMAIN",
        "M0NDB07_FALLBACK_BRANCHES",
        "M0NDB07_OUTPUT_UNIT_CHECK",
    }
    assert all(row["formula_claim_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert rows[0]["next_required_artifact"] == "m0_no_dark_readout_equation_contract_v08"
    assert all(row["completion_status"] == "READY" for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_FORMULA_BODY_CONTRACT_V07",
            "formula_body_artifact": "m0_no_dark_formula_body_v07",
            "required_body_slots": "7",
            "ready_body_slots": "7",
            "blocked_body_slots": "0",
            "formula_equations_written": "0",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FORMULA_BODY_READY_FOR_TABLE_FREEZE",
            "next_required_artifact": "m0_no_dark_formula_table_v06",
            "claim_boundary": "m0_no_dark_formula_body_contract_only_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v06_m0_no_dark_formula_table_contract_blocks_policy_slots() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_formula_table_contract_v06.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_formula_table_contract_summary_v06.csv").open()))
    assert len(rows) == 6
    assert {row["component_id"] for row in rows} == {
        "M0ND06_SOURCE_INPUTS",
        "M0ND06_READOUT_MAP",
        "M0ND06_COEFFICIENT_POLICY",
        "M0ND06_FIXED_SCALES",
        "M0ND06_FALLBACK_POLICY",
        "M0ND06_OUTPUT_SCHEMA",
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert rows[0]["next_required_artifact"] == "m0_no_dark_formula_body_contract_v07"
    assert rows[0]["completion_status"] == "READY"
    assert rows[1]["completion_status"] == "READY"
    assert rows[5]["completion_status"] == "READY"
    assert rows[2]["completion_status"] == "READY"
    assert rows[3]["completion_status"] == "READY"
    assert rows[4]["completion_status"] == "READY"
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_FORMULA_TABLE_CONTRACT_V06",
            "formula_artifact": "m0_no_dark_formula_table_v06",
            "required_components": "6",
            "ready_components": "6",
            "blocked_components": "0",
            "formula_body_rows_written": "0",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FORMULA_TABLE_READY_FOR_PREDICTION_ROWS",
            "next_required_artifact": "family_prediction_tables_v08.csv",
            "claim_boundary": "m0_no_dark_formula_table_contract_only_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v80_family_prediction_table_contract_blocks_on_formula_slots() -> None:
    schema = list(csv.DictReader((ROOT / "data/derived/family_prediction_table_schema_v80.csv").open()))
    slots = list(csv.DictReader((ROOT / "data/derived/family_prediction_table_slot_requirements_v80.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/family_prediction_table_contract_summary_v80.csv").open()))
    assert {"scoring_row_id", "family_id", "v_pred_km_s"}.issubset({row["field_name"] for row in schema})
    assert all(row["endpoint_scoring_allowed"] == "false" for row in schema)
    assert len(slots) == 8
    assert slots[0]["prediction_slot_status"] == "PREDICTION_SLOT_READY"
    assert slots[1]["prediction_slot_status"] == "PREDICTION_SLOT_READY"
    assert slots[2]["prediction_slot_status"] == "PREDICTION_SLOT_READY"
    assert slots[3]["prediction_slot_status"] == "PREDICTION_SLOT_READY"
    assert slots[4]["prediction_slot_status"] == "PREDICTION_SLOT_READY"
    assert slots[5]["prediction_slot_status"] == "PREDICTION_SLOT_READY"
    assert slots[6]["prediction_slot_status"] == "PREDICTION_SLOT_READY"
    assert slots[7]["prediction_slot_status"] == "PREDICTION_SLOT_READY"
    assert all(row["endpoint_scoring_allowed"] == "false" for row in slots)
    assert slots[0]["required_formula_artifact"] == "family_prediction_tables_v08.csv"
    assert slots[1]["required_formula_artifact"] == "m0_label_rule_table_v06"
    assert slots[2]["required_formula_artifact"] == "m1_tau_response_formula_table_v06"
    assert slots[3]["required_formula_artifact"] == "m1_admissibility_table_v06"
    assert slots[4]["required_formula_artifact"] == "m2_benchmark_profile_table_v06"
    assert slots[5]["required_formula_artifact"] == "m2_nuisance_policy_table_v06"
    assert slots[6]["required_formula_artifact"] == "shared_scoring_input_table_v06"
    assert slots[7]["required_formula_artifact"] == "numeric_parameter_count_table_v06"
    assert summary == [
        {
            "summary_id": "FAMILY_PREDICTION_TABLE_CONTRACT_V80",
            "required_formula_slots": "8",
            "ready_formula_slots": "8",
            "blocked_formula_slots": "0",
            "numeric_prediction_rows_written": "450",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FAMILY_PREDICTION_TABLE_CONTRACT_READY_PARAMETER_COUNTS_BLOCKED",
            "next_required_artifact": "numeric_parameter_count_table_v08.csv",
            "claim_boundary": "family_prediction_table_contract_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v08_family_prediction_tables_contains_m0_no_dark_rows_without_scores() -> None:
    table_path = ROOT / "data/derived/family_prediction_tables_v08.csv"
    rows = list(csv.DictReader(table_path.open()))
    summary = list(csv.DictReader((ROOT / "data/derived/family_prediction_tables_summary_v08.csv").open()))
    note = (ROOT / "docs/family_prediction_tables_v08.md").read_text()

    assert len(rows) == 450
    assert {row["family_id"] for row in rows} == {"M0"}
    assert {row["prediction_source_slot"] for row in rows} == {"M0:no_dark_readout_formula"}
    assert {row["prediction_status"] for row in rows} == {"PREDICTION_ROW_EMITTED_NOT_SCORED"}
    assert list(csv.DictReader(table_path.open()).fieldnames or []) == [
        "scoring_row_id",
        "galaxy_id",
        "family_id",
        "radial_index",
        "radius_kpc",
        "v_pred_km_s",
        "prediction_source_slot",
        "formula_table_status",
        "prediction_status",
    ]
    assert summary == [
        {
            "summary_id": "FAMILY_PREDICTION_TABLES_V08",
            "prediction_table_artifact": "family_prediction_tables_v08.csv",
            "table_header_written": "true",
            "numeric_prediction_rows_written": "450",
            "families_with_numeric_predictions": "1",
            "m0_no_dark_formula_table_status": "M0_NO_DARK_ROWS_EMITTED",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FAMILY_PREDICTION_TABLES_M0_NO_DARK_ROWS_EMITTED_SCORING_BLOCKED",
            "next_required_artifact": "m0_label_rule_table_v06",
            "claim_boundary": "family_prediction_tables_m0_no_dark_rows_only_no_scores_no_dark_sector_verdict",
        }
    ]
    assert "M0 no-dark" in note
    assert "does not compute endpoint scores" in note


def test_v09_family_prediction_comparability_separates_m0_adequacy_from_family_verdict() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/family_prediction_comparability_v09.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/family_prediction_comparability_summary_v09.csv").open()))
    note = (ROOT / "docs/family_prediction_comparability_v09.md").read_text()

    assert [row["family_id"] for row in rows] == ["M0", "M1", "M2"]
    assert {row["family_id"]: row["numeric_prediction_rows_written"] for row in rows} == {
        "M0": "450",
        "M1": "0",
        "M2": "0",
    }
    assert rows[0]["allowed_scoring_mode"] == "M0_ADEQUACY_DIAGNOSTIC_ONLY"
    assert rows[0]["blocked_scoring_mode"] == "M0_M1_M2_FAMILY_COMPARISON"
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["dark_sector_verdict_allowed"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "FAMILY_PREDICTION_COMPARABILITY_V09",
            "families_checked": "3",
            "families_with_numeric_predictions": "1",
            "families_without_numeric_predictions": "2",
            "m0_adequacy_scoring_basis_available": "true",
            "family_comparison_scoring_allowed": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "dark_sector_verdict_allowed_anywhere": "false",
            "overall_status": "FAMILY_PREDICTION_COMPARABILITY_M0_ONLY_FAMILY_COMPARISON_BLOCKED",
            "next_required_artifact": "control_runner_outputs_v08.csv",
            "claim_boundary": "family_prediction_comparability_only_no_scores_no_dark_sector_verdict",
        }
    ]
    assert "M0 adequacy diagnostics" in note
    assert "Full M0/M1/M2 family-comparison scoring remains blocked" in note


def test_v08_m0_no_dark_prediction_row_writer_blocks_without_executable_kernel() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_prediction_row_writer_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_prediction_row_writer_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_prediction_row_writer_v08.md").read_text()
    assert len(rows) == 5
    assert rows[0]["writer_decision"] == "READY_FOR_WRITER_REVIEW"
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_executable_prediction_kernel_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_PREDICTION_ROW_WRITER_V08",
            "writer_artifact": "m0_no_dark_prediction_row_writer_v08",
            "writer_checks": "5",
            "blocked_writer_checks": "4",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PREDICTION_ROW_WRITER_PRESENT_BLOCKED_EXECUTABLE_KERNEL_MISSING",
            "next_required_artifact": "m0_no_dark_executable_prediction_kernel_v08",
            "claim_boundary": "m0_no_dark_prediction_row_writer_gate_only_no_predictions_no_scores_no_dark_sector_verdict",
        }
    ]
    assert "without writing `v_pred_km_s` rows" in note


def test_v08_m0_no_dark_executable_prediction_kernel_blocks_without_velocity_formula() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_executable_prediction_kernel_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_executable_prediction_kernel_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_executable_prediction_kernel_v08.md").read_text()
    assert len(rows) == 6
    assert rows[0]["kernel_decision"] == "READY_FOR_EXECUTABLE_KERNEL_REVIEW"
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_readout_formula_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_EXECUTABLE_PREDICTION_KERNEL_V08",
            "kernel_artifact": "m0_no_dark_executable_prediction_kernel_v08",
            "kernel_checks": "6",
            "blocked_kernel_checks": "5",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXECUTABLE_KERNEL_PRESENT_BLOCKED_VELOCITY_FORMULA_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_readout_formula_v08",
            "claim_boundary": "m0_no_dark_executable_prediction_kernel_gate_only_no_formula_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not define a velocity formula" in note


def test_v08_m0_no_dark_velocity_readout_formula_blocks_without_equation_body() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_readout_formula_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_readout_formula_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_velocity_readout_formula_v08.md").read_text()
    assert len(rows) == 5
    assert rows[0]["formula_decision"] == "READY_FOR_VELOCITY_FORMULA_REVIEW"
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_source_to_rotation_equation_body_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_READOUT_FORMULA_V08",
            "formula_artifact": "m0_no_dark_velocity_readout_formula_v08",
            "formula_checks": "5",
            "blocked_formula_checks": "2",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_VELOCITY_FORMULA_PRESENT_BLOCKED_EQUATION_BODY_MISSING",
            "next_required_artifact": "m0_no_dark_source_to_rotation_equation_body_v08",
            "claim_boundary": "m0_no_dark_velocity_readout_formula_gate_only_no_equation_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not define the equation body" in note


def test_v08_m0_no_dark_source_to_rotation_equation_body_blocks_without_coupling_rule() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_source_to_rotation_equation_body_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_source_to_rotation_equation_body_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_source_to_rotation_equation_body_v08.md").read_text()
    assert len(rows) == 6
    assert rows[0]["equation_body_decision"] == "READY_FOR_EQUATION_BODY_REVIEW"
    assert all(row["equation_body_written"] == "false" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_source_to_velocity_coupling_rule_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_SOURCE_TO_ROTATION_EQUATION_BODY_V08",
            "equation_body_artifact": "m0_no_dark_source_to_rotation_equation_body_v08",
            "equation_body_checks": "6",
            "blocked_equation_body_checks": "2",
            "equation_body_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EQUATION_BODY_PRESENT_BLOCKED_SOURCE_TO_VELOCITY_COUPLING_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_source_to_velocity_coupling_rule_v08",
            "claim_boundary": "m0_no_dark_source_to_rotation_equation_body_gate_only_no_coupling_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not choose a coupling law" in note


def test_v08_m0_no_dark_source_to_velocity_coupling_rule_blocks_without_unit_lift() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_source_to_velocity_coupling_rule_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_source_to_velocity_coupling_rule_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_source_to_velocity_coupling_rule_v08.md").read_text()
    assert len(rows) == 6
    assert rows[0]["coupling_rule_decision"] == "READY_FOR_COUPLING_RULE_REVIEW"
    assert all(row["coupling_rule_written"] == "false" for row in rows)
    assert all(row["velocity_unit_lift_written"] == "false" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_unit_lift_rule_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_SOURCE_TO_VELOCITY_COUPLING_RULE_V08",
            "coupling_rule_artifact": "m0_no_dark_source_to_velocity_coupling_rule_v08",
            "coupling_rule_checks": "6",
            "blocked_coupling_rule_checks": "3",
            "coupling_rule_written": "false",
            "velocity_unit_lift_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_COUPLING_RULE_PRESENT_BLOCKED_VELOCITY_UNIT_LIFT_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_unit_lift_rule_v08",
            "claim_boundary": "m0_no_dark_source_to_velocity_coupling_rule_gate_only_no_unit_lift_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not choose a unit lift" in note


def test_v08_m0_no_dark_velocity_unit_lift_rule_blocks_without_dimension_anchor() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_unit_lift_rule_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_unit_lift_rule_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_velocity_unit_lift_rule_v08.md").read_text()
    assert len(rows) == 6
    assert rows[0]["unit_lift_decision"] == "READY_FOR_UNIT_LIFT_REVIEW"
    assert all(row["velocity_unit_lift_written"] == "false" for row in rows)
    assert all(row["dimension_anchor_written"] == "false" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_dimension_anchor_rule_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_UNIT_LIFT_RULE_V08",
            "unit_lift_artifact": "m0_no_dark_velocity_unit_lift_rule_v08",
            "unit_lift_checks": "6",
            "blocked_unit_lift_checks": "2",
            "velocity_unit_lift_written": "false",
            "dimension_anchor_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_VELOCITY_UNIT_LIFT_PRESENT_BLOCKED_DIMENSION_ANCHOR_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_dimension_anchor_rule_v08",
            "claim_boundary": "m0_no_dark_velocity_unit_lift_rule_gate_only_no_dimension_anchor_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not declare a dimension anchor" in note


def test_v08_m0_no_dark_velocity_dimension_anchor_rule_blocks_without_anchor_source_law() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_dimension_anchor_rule_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_dimension_anchor_rule_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_velocity_dimension_anchor_rule_v08.md").read_text()
    assert len(rows) == 6
    assert rows[0]["dimension_anchor_decision"] == "READY_FOR_DIMENSION_ANCHOR_REVIEW"
    assert all(row["dimension_anchor_written"] == "false" for row in rows)
    assert all(row["anchor_source_law_written"] == "false" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_source_law_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_DIMENSION_ANCHOR_RULE_V08",
            "dimension_anchor_artifact": "m0_no_dark_velocity_dimension_anchor_rule_v08",
            "dimension_anchor_checks": "6",
            "blocked_dimension_anchor_checks": "2",
            "dimension_anchor_written": "false",
            "anchor_source_law_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_DIMENSION_ANCHOR_PRESENT_BLOCKED_ANCHOR_SOURCE_LAW_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_source_law_v08",
            "claim_boundary": "m0_no_dark_velocity_dimension_anchor_rule_gate_only_no_anchor_source_law_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not declare the anchor source law" in note


def test_v08_m0_no_dark_velocity_anchor_source_law_blocks_without_candidate_basis() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_source_law_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_source_law_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_velocity_anchor_source_law_v08.md").read_text()
    assert len(rows) == 6
    assert rows[0]["anchor_source_law_decision"] == "READY_FOR_ANCHOR_SOURCE_LAW_REVIEW"
    assert any(row["anchor_source_law_decision"] == "BLOCKED_ANCHOR_CANDIDATE_BASIS_MISSING" for row in rows)
    assert all(row["anchor_source_law_written"] == "true" for row in rows)
    assert all(row["anchor_candidate_basis_written"] == "false" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_candidate_basis_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_SOURCE_LAW_V08",
            "anchor_source_law_artifact": "m0_no_dark_velocity_anchor_source_law_v08",
            "anchor_source_law_checks": "6",
            "blocked_anchor_source_law_checks": "1",
            "anchor_source_law_written": "true",
            "anchor_candidate_basis_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_SOURCE_LAW_PRESENT_BLOCKED_ANCHOR_CANDIDATE_BASIS_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_candidate_basis_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_source_law_gate_only_no_candidate_basis_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not choose an anchor candidate" in note


def test_v08_m0_no_dark_velocity_anchor_candidate_basis_blocks_without_selection_rule() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_candidate_basis_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_candidate_basis_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_velocity_anchor_candidate_basis_v08.md").read_text()
    assert len(rows) == 6
    assert rows[0]["candidate_basis_decision"] == "READY_FOR_ANCHOR_CANDIDATE_BASIS_REVIEW"
    assert sum(row["candidate_basis_decision"] == "ADMISSIBLE_CANDIDATE_CLASS_DECLARED" for row in rows) == 2
    assert sum(row["candidate_basis_decision"] == "CONDITIONAL_CANDIDATE_CLASS_DECLARED" for row in rows) == 1
    assert any(row["candidate_basis_decision"] == "REJECTED_CANDIDATE_CLASS_DECLARED" for row in rows)
    assert any(row["candidate_basis_decision"] == "BLOCKED_ANCHOR_SELECTION_RULE_MISSING" for row in rows)
    assert all(row["candidate_basis_written"] == "true" for row in rows)
    assert all(row["anchor_selection_rule_written"] == "false" for row in rows)
    assert all(row["anchor_value_written"] == "false" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_selection_rule_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_CANDIDATE_BASIS_V08",
            "anchor_candidate_basis_artifact": "m0_no_dark_velocity_anchor_candidate_basis_v08",
            "candidate_basis_checks": "6",
            "admissible_candidate_classes": "3",
            "rejected_candidate_classes": "1",
            "blocked_candidate_basis_checks": "1",
            "candidate_basis_written": "true",
            "anchor_selection_rule_written": "false",
            "anchor_value_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_CANDIDATE_BASIS_PRESENT_BLOCKED_ANCHOR_SELECTION_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_selection_rule_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_candidate_basis_gate_only_no_selection_rule_no_anchor_value_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not choose an anchor candidate" in note


def test_v08_m0_no_dark_velocity_anchor_selection_rule_blocks_without_value_freeze() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_selection_rule_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_selection_rule_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_velocity_anchor_selection_rule_v08.md").read_text()
    assert len(rows) == 6
    assert rows[0]["selection_rule_decision"] == "READY_FOR_ANCHOR_SELECTION_RULE_REVIEW"
    assert any(row["selection_rule_decision"] == "ANCHOR_SELECTION_PRIORITY_RULE_DECLARED" for row in rows)
    assert any(row["selection_rule_decision"] == "ANCHOR_SELECTION_FALLBACK_RULE_DECLARED" for row in rows)
    assert any(row["selection_rule_decision"] == "ANCHOR_SELECTION_REJECTION_RULE_DECLARED" for row in rows)
    assert any(row["selection_rule_decision"] == "BLOCKED_ANCHOR_VALUE_FREEZE_MISSING" for row in rows)
    assert all(row["anchor_selection_rule_written"] == "true" for row in rows)
    assert all(row["anchor_value_written"] == "false" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_value_freeze_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_SELECTION_RULE_V08",
            "anchor_selection_rule_artifact": "m0_no_dark_velocity_anchor_selection_rule_v08",
            "selection_rule_checks": "6",
            "declared_selection_rule_clauses": "4",
            "blocked_selection_rule_checks": "1",
            "anchor_selection_rule_written": "true",
            "anchor_value_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_SELECTION_RULE_PRESENT_BLOCKED_ANCHOR_VALUE_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_value_freeze_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_selection_rule_gate_only_no_anchor_value_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not freeze an anchor value" in note


def test_v08_m0_no_dark_velocity_anchor_value_freeze_blocks_without_unit_normalization() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_value_freeze_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_value_freeze_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_velocity_anchor_value_freeze_v08.md").read_text()
    assert len(rows) == 22
    assert rows[0]["value_freeze_decision"] == "READY_FOR_ANCHOR_VALUE_FREEZE_REVIEW"
    assert any(row["value_freeze_decision"] == "BLOCKED_ANCHOR_UNIT_NORMALIZATION_MISSING" for row in rows)
    galaxy_rows = [row for row in rows if row["galaxy_id"] != "ALL"]
    assert len(galaxy_rows) == 18
    assert sum(int(row["imported_source_rows"]) for row in galaxy_rows) == 450
    assert all(row["selected_anchor_class"] == "source_side_baryonic_gravity_velocity_carrier" for row in rows)
    assert all(row["frozen_source_columns"] == "v_gas_km_s;v_disk_km_s;v_bulge_km_s" for row in rows)
    assert all("v_obs_km_s" in row["forbidden_inputs"] for row in rows)
    assert all(row["anchor_value_source_frozen"] == "true" for row in rows)
    assert all(row["anchor_numeric_value_rows_written"] == "0" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_unit_normalization_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_VALUE_FREEZE_V08",
            "anchor_value_freeze_artifact": "m0_no_dark_velocity_anchor_value_freeze_v08",
            "value_freeze_rows": "22",
            "galaxy_value_freeze_rows": "18",
            "imported_source_rows_referenced": "450",
            "blocked_value_freeze_checks": "1",
            "anchor_value_source_frozen": "true",
            "anchor_numeric_value_rows_written": "0",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_VALUE_FREEZE_PRESENT_BLOCKED_UNIT_NORMALIZATION_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_unit_normalization_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_value_freeze_source_columns_only_no_unit_normalization_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not compute a combined anchor value" in note


def test_v08_m0_no_dark_velocity_anchor_unit_normalization_blocks_without_component_combination_rule() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_unit_normalization_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_unit_normalization_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_velocity_anchor_unit_normalization_v08.md").read_text()
    assert len(rows) == 7
    assert rows[0]["unit_normalization_decision"] == "READY_FOR_ANCHOR_UNIT_NORMALIZATION_REVIEW"
    assert sum(row["unit_normalization_decision"] == "ANCHOR_UNIT_NORMALIZATION_DECLARED_NO_RESCALE" for row in rows) == 3
    assert any(row["unit_normalization_decision"] == "BLOCKED_COMPONENT_COMBINATION_RULE_MISSING" for row in rows)
    assert {row["source_column"] for row in rows if row["anchor_unit_component"] == "source_component_unit"} == {
        "v_gas_km_s",
        "v_disk_km_s",
        "v_bulge_km_s",
    }
    assert all(row["normalized_unit"] == "km/s" for row in rows)
    assert all("posthoc_unit_rescale" in row["forbidden_inputs"] for row in rows)
    assert all(row["unit_normalization_written"] == "true" for row in rows)
    assert all(row["component_combination_rule_written"] == "false" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_component_combination_rule_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_UNIT_NORMALIZATION_V08",
            "anchor_unit_normalization_artifact": "m0_no_dark_velocity_anchor_unit_normalization_v08",
            "unit_normalization_checks": "7",
            "source_component_units_normalized": "3",
            "blocked_unit_normalization_checks": "1",
            "unit_normalization_written": "true",
            "component_combination_rule_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_UNIT_NORMALIZATION_PRESENT_BLOCKED_COMPONENT_COMBINATION_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_combination_rule_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_unit_normalization_gate_only_no_component_combination_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not combine" in note


def test_v08_m0_no_dark_velocity_anchor_component_combination_rule_blocks_without_weight_policy() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_component_combination_rule_v08.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_component_combination_rule_summary_v08.csv").open())
    )
    note = (ROOT / "docs/m0_no_dark_velocity_anchor_component_combination_rule_v08.md").read_text()
    assert len(rows) == 6
    assert rows[0]["component_combination_decision"] == "READY_FOR_COMPONENT_COMBINATION_RULE_REVIEW"
    assert any(row["component_combination_decision"] == "BLOCKED_COMPONENT_WEIGHT_POLICY_MISSING" for row in rows)
    assert all(row["source_columns"] == "v_gas_km_s;v_disk_km_s;v_bulge_km_s" for row in rows)
    assert all("v_obs_km_s" in row["forbidden_inputs"] for row in rows)
    assert all("posthoc_weight_fit" in row["forbidden_inputs"] for row in rows)
    assert all(row["component_combination_rule_written"] == "true" for row in rows)
    assert all(row["component_weight_policy_written"] == "false" for row in rows)
    assert all(row["combined_anchor_values_written"] == "0" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_component_weight_policy_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_COMPONENT_COMBINATION_RULE_V08",
            "anchor_component_combination_artifact": "m0_no_dark_velocity_anchor_component_combination_rule_v08",
            "component_combination_checks": "6",
            "declared_component_combination_guards": "4",
            "blocked_component_combination_checks": "1",
            "component_combination_rule_written": "true",
            "component_weight_policy_written": "false",
            "combined_anchor_values_written": "0",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_COMPONENT_COMBINATION_RULE_PRESENT_BLOCKED_COMPONENT_WEIGHT_POLICY_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_policy_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_component_combination_rule_only_no_weight_policy_no_combined_values_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not choose component weights" in note


def test_v08_m0_no_dark_velocity_anchor_component_weight_policy_blocks_without_value_freeze() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_component_weight_policy_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_component_weight_policy_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_velocity_anchor_component_weight_policy_v08.md").read_text()
    assert len(rows) == 6
    assert rows[0]["weight_policy_decision"] == "READY_FOR_COMPONENT_WEIGHT_POLICY_REVIEW"
    assert any(row["weight_policy_decision"] == "BLOCKED_COMPONENT_WEIGHT_VALUE_FREEZE_MISSING" for row in rows)
    assert all(row["source_columns"] == "v_gas_km_s;v_disk_km_s;v_bulge_km_s" for row in rows)
    assert all("posthoc_weight_fit" in row["forbidden_inputs"] for row in rows)
    assert all("posthoc_normalization" in row["forbidden_inputs"] for row in rows)
    assert all(row["component_weight_policy_written"] == "true" for row in rows)
    assert all(row["component_weight_values_frozen"] == "false" for row in rows)
    assert all(row["combined_anchor_values_written"] == "0" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_component_weight_value_freeze_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_COMPONENT_WEIGHT_POLICY_V08",
            "anchor_component_weight_policy_artifact": "m0_no_dark_velocity_anchor_component_weight_policy_v08",
            "component_weight_policy_checks": "6",
            "declared_component_weight_policy_guards": "4",
            "blocked_component_weight_policy_checks": "1",
            "component_weight_policy_written": "true",
            "component_weight_values_frozen": "false",
            "combined_anchor_values_written": "0",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_COMPONENT_WEIGHT_POLICY_PRESENT_BLOCKED_WEIGHT_VALUE_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_component_weight_policy_only_no_weight_value_freeze_no_combined_values_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not freeze component-weight values" in note


def test_v08_m0_no_dark_velocity_anchor_component_weight_value_freeze_blocks_without_combined_anchor_rule() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_component_weight_value_freeze_v08.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/m0_no_dark_velocity_anchor_component_weight_value_freeze_summary_v08.csv").open()
        )
    )
    note = (ROOT / "docs/m0_no_dark_velocity_anchor_component_weight_value_freeze_v08.md").read_text()
    assert len(rows) == 6
    assert rows[0]["weight_value_freeze_decision"] == "READY_FOR_COMPONENT_WEIGHT_VALUE_FREEZE_REVIEW"
    assert any(row["weight_value_freeze_decision"] == "BLOCKED_COMBINED_ANCHOR_RULE_MISSING" for row in rows)
    assert all(row["source_columns"] == "v_gas_km_s;v_disk_km_s;v_bulge_km_s" for row in rows)
    assert all("posthoc_combined_anchor_value" in row["forbidden_inputs"] for row in rows)
    assert all(row["component_weight_values_frozen"] == "true" for row in rows)
    assert all(row["numeric_weight_values_written"] == "0" for row in rows)
    assert all(row["combined_anchor_rule_written"] == "false" for row in rows)
    assert all(row["combined_anchor_values_written"] == "0" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_combined_anchor_rule_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_COMPONENT_WEIGHT_VALUE_FREEZE_V08",
            "anchor_component_weight_value_freeze_artifact": "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08",
            "component_weight_value_freeze_checks": "6",
            "symbolic_weight_value_slots_frozen": "3",
            "blocked_component_weight_value_freeze_checks": "1",
            "component_weight_values_frozen": "true",
            "numeric_weight_values_written": "0",
            "combined_anchor_rule_written": "false",
            "combined_anchor_values_written": "0",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_COMPONENT_WEIGHT_VALUE_FREEZE_PRESENT_BLOCKED_COMBINED_ANCHOR_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_rule_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_component_weight_value_freeze_only_symbolic_slots_no_combined_values_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "freezing the allowed symbolic slots" in note


def test_v08_m0_no_dark_velocity_anchor_combined_anchor_rule_blocks_without_expression_freeze() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_combined_anchor_rule_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_combined_anchor_rule_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_velocity_anchor_combined_anchor_rule_v08.md").read_text()
    assert len(rows) == 6
    assert rows[0]["combined_anchor_rule_decision"] == "READY_FOR_COMBINED_ANCHOR_RULE_REVIEW"
    assert any(row["combined_anchor_rule_decision"] == "BLOCKED_COMBINED_ANCHOR_EXPRESSION_FREEZE_MISSING" for row in rows)
    assert all(row["source_columns"] == "v_gas_km_s;v_disk_km_s;v_bulge_km_s" for row in rows)
    assert all("w_gas" in row["symbolic_slots"] and "n_anchor" in row["symbolic_slots"] for row in rows)
    assert all("posthoc_formula_switch" in row["forbidden_inputs"] for row in rows)
    assert all(row["combined_anchor_rule_written"] == "true" for row in rows)
    assert all(row["combined_anchor_expression_written"] == "false" for row in rows)
    assert all(row["combined_anchor_values_written"] == "0" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {
        "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08"
    }
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_COMBINED_ANCHOR_RULE_V08",
            "anchor_combined_anchor_rule_artifact": "m0_no_dark_velocity_anchor_combined_anchor_rule_v08",
            "combined_anchor_rule_checks": "6",
            "declared_combined_anchor_rule_guards": "3",
            "blocked_combined_anchor_rule_checks": "1",
            "combined_anchor_rule_written": "true",
            "combined_anchor_expression_written": "false",
            "combined_anchor_values_written": "0",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_RULE_PRESENT_BLOCKED_EXPRESSION_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_combined_anchor_rule_only_no_expression_freeze_no_combined_values_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "does not freeze the exact symbolic expression" in note


def test_v08_m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_blocks_without_value_freeze() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_summary_v08.csv").open()
        )
    )
    note = (ROOT / "docs/m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08.md").read_text()
    expression = (
        "v_anchor_sq_km2_s2 = (s_gas*w_gas*v_gas_km_s^2 + "
        "s_disk*w_disk*v_disk_km_s^2 + s_bulge*w_bulge*v_bulge_km_s^2) / n_anchor"
    )
    assert len(rows) == 6
    assert rows[0]["expression_freeze_decision"] == "READY_FOR_COMBINED_ANCHOR_EXPRESSION_FREEZE_REVIEW"
    assert any(row["expression_freeze_decision"] == "BLOCKED_COMBINED_ANCHOR_VALUE_FREEZE_MISSING" for row in rows)
    assert all(row["frozen_expression"] == expression for row in rows)
    assert all(row["source_columns"] == "v_gas_km_s;v_disk_km_s;v_bulge_km_s" for row in rows)
    assert all("w_gas" in row["symbolic_slots"] and "n_anchor" in row["symbolic_slots"] for row in rows)
    assert all("v_obs_km_s" in row["forbidden_inputs"] for row in rows)
    assert all(row["combined_anchor_expression_frozen"] == "true" for row in rows)
    assert all(row["combined_anchor_values_written"] == "0" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {
        "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08"
    }
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_COMBINED_ANCHOR_EXPRESSION_FREEZE_V08",
            "anchor_combined_anchor_expression_artifact": "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08",
            "expression_freeze_checks": "6",
            "frozen_expression_checks": "4",
            "blocked_expression_freeze_checks": "1",
            "combined_anchor_expression_frozen": "true",
            "frozen_expression": expression,
            "combined_anchor_values_written": "0",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_EXPRESSION_FROZEN_BLOCKED_VALUE_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_only_no_combined_values_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "v_anchor_sq_km2_s2" in note
    assert "does not evaluate combined-anchor values" in note


def test_v08_m0_no_dark_velocity_anchor_combined_anchor_value_freeze_blocks_without_formula_body_freeze() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_summary_v08.csv").open()
        )
    )
    note = (ROOT / "docs/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08.md").read_text()
    assert len(rows) == 450
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert all(row["s_gas"] == row["s_disk"] == row["s_bulge"] == "1" for row in rows)
    assert all(row["w_gas"] == row["w_disk"] == row["w_bulge"] == "1" for row in rows)
    assert all(row["n_anchor"] == "1" for row in rows)
    assert all(float(row["v_anchor_sq_km2_s2"]) >= 0.0 for row in rows)
    assert all(float(row["v_anchor_km_s"]) >= 0.0 for row in rows)
    assert all("v_obs_km_s" in row["forbidden_inputs"] for row in rows)
    assert all(row["combined_anchor_values_written"] == "true" for row in rows)
    assert all(row["velocity_formula_written"] == "false" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {
        "m0_no_dark_velocity_readout_formula_body_freeze_v08"
    }
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_COMBINED_ANCHOR_VALUE_FREEZE_V08",
            "anchor_combined_anchor_value_artifact": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
            "source_rows_evaluated": "450",
            "galaxies_with_anchor_values": "18",
            "identity_weight_rows": "450",
            "negative_anchor_sq_rows": "0",
            "combined_anchor_values_written": "450",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_VALUES_FROZEN_BLOCKED_VELOCITY_FORMULA_BODY_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_readout_formula_body_freeze_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_only_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]
    assert "identity carrier" in note
    assert "not `v_pred_km_s`" in note


def test_v08_m0_no_dark_velocity_readout_formula_body_freeze_blocks_without_prediction_row_values() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/m0_no_dark_velocity_readout_formula_body_freeze_v08.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/m0_no_dark_velocity_readout_formula_body_freeze_summary_v08.csv").open()
        )
    )
    note = (ROOT / "docs/m0_no_dark_velocity_readout_formula_body_freeze_v08.md").read_text()
    formula_body = "v_body_km_s(R) := v_anchor_km_s(R)"

    assert len(rows) == 5
    assert rows[0]["formula_body_freeze_decision"] == "READY_FOR_VELOCITY_FORMULA_BODY_FREEZE_REVIEW"
    assert any(
        row["formula_body_freeze_decision"] == "BLOCKED_PREDICTION_ROW_VALUE_FREEZE_MISSING" for row in rows
    )
    assert all(row["frozen_formula_body"] == formula_body for row in rows)
    assert all(row["formula_body_frozen"] == "true" for row in rows)
    assert all(row["velocity_formula_body_written"] == "true" for row in rows)
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_prediction_row_value_freeze_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_READOUT_FORMULA_BODY_FREEZE_V08",
            "formula_body_freeze_artifact": "m0_no_dark_velocity_readout_formula_body_freeze_v08",
            "formula_body_freeze_checks": "5",
            "frozen_formula_body_checks": "3",
            "blocked_formula_body_freeze_checks": "1",
            "formula_body_frozen": "true",
            "frozen_formula_body": formula_body,
            "velocity_formula_body_written": "true",
            "numeric_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_VELOCITY_FORMULA_BODY_FROZEN_BLOCKED_PREDICTION_ROW_VALUE_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_prediction_row_value_freeze_v08",
            "claim_boundary": "m0_no_dark_velocity_readout_formula_body_freeze_only_no_prediction_rows_no_scores_no_dark_sector_verdict",
        }
    ]
    assert formula_body in note
    assert "does not emit" in note


def test_v08_m0_no_dark_prediction_row_value_freeze_blocks_without_family_row_emission() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_prediction_row_value_freeze_v08.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/m0_no_dark_prediction_row_value_freeze_summary_v08.csv").open())
    )
    note = (ROOT / "docs/m0_no_dark_prediction_row_value_freeze_v08.md").read_text()
    formula_body = "v_body_km_s(R) := v_anchor_km_s(R)"

    assert len(rows) == 450
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["family_id"] for row in rows} == {"M0"}
    assert all(row["frozen_formula_body"] == formula_body for row in rows)
    assert all(row["v_anchor_km_s"] == row["frozen_prediction_value_km_s"] for row in rows)
    assert all("v_obs_km_s" in row["forbidden_inputs"] for row in rows)
    assert all(row["prediction_row_values_frozen"] == "true" for row in rows)
    assert all(row["family_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_no_dark_family_prediction_row_emission_v08"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_PREDICTION_ROW_VALUE_FREEZE_V08",
            "prediction_row_value_freeze_artifact": "m0_no_dark_prediction_row_value_freeze_v08",
            "source_formula_body_artifact": "m0_no_dark_velocity_readout_formula_body_freeze_v08",
            "source_anchor_value_artifact": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
            "source_rows_evaluated": "450",
            "galaxies_with_frozen_values": "18",
            "family_id": "M0",
            "frozen_formula_body": formula_body,
            "prediction_row_values_frozen": "450",
            "family_prediction_rows_written": "0",
            "families_with_numeric_predictions": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PREDICTION_ROW_VALUES_FROZEN_BLOCKED_FAMILY_ROW_EMISSION_MISSING",
            "next_required_artifact": "m0_no_dark_family_prediction_row_emission_v08",
            "claim_boundary": "m0_no_dark_prediction_row_value_freeze_only_no_family_table_rows_no_scores_no_dark_sector_verdict",
        }
    ]
    assert "does not write rows into" in note
    assert "does not compute endpoint scores" in note


def test_v08_m0_no_dark_family_prediction_row_emission_writes_rows_without_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_family_prediction_row_emission_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_family_prediction_row_emission_summary_v08.csv").open()))
    note = (ROOT / "docs/m0_no_dark_family_prediction_row_emission_v08.md").read_text()

    assert len(rows) == 450
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["family_id"] for row in rows} == {"M0"}
    assert {row["prediction_source_slot"] for row in rows} == {"M0:no_dark_readout_formula"}
    assert {row["prediction_status"] for row in rows} == {"PREDICTION_ROW_EMITTED_NOT_SCORED"}
    assert all(row["family_prediction_row_written"] == "true" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_label_rule_table_v06"}
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_FAMILY_PREDICTION_ROW_EMISSION_V08",
            "family_row_emission_artifact": "m0_no_dark_family_prediction_row_emission_v08",
            "target_prediction_table_artifact": "family_prediction_tables_v08.csv",
            "source_prediction_row_value_artifact": "m0_no_dark_prediction_row_value_freeze_v08",
            "family_id": "M0",
            "emitted_prediction_rows": "450",
            "galaxies_with_emitted_rows": "18",
            "families_with_numeric_predictions": "1",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FAMILY_PREDICTION_ROWS_EMITTED_SCORING_BLOCKED",
            "next_required_artifact": "m0_label_rule_table_v06",
            "claim_boundary": "m0_no_dark_family_prediction_row_emission_only_no_scores_no_dark_sector_verdict",
        }
    ]
    assert "M0_NO_DARK_FAMILY_PREDICTION_ROWS_EMITTED_SCORING_BLOCKED" in note
    assert "does not compute endpoint scores" in note


def test_v06_m0_label_rule_table_closes_label_rule_without_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_label_rule_table_v06.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_label_rule_table_summary_v06.csv").open()))
    note = (ROOT / "docs/m0_label_rule_table_v06.md").read_text()

    assert len(rows) == 6
    assert {row["family_id"] for row in rows} == {"M0"}
    assert {row["formula_slot"] for row in rows} == {"morphology_label_rule"}
    assert {row["rule_component"] for row in rows} == {
        "source_observables",
        "label_categories",
        "fallback_labels",
        "exception_policy",
        "row_selector",
        "freeze_audit",
    }
    assert all(row["frozen_before_scoring"] == "true" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m1_tau_response_formula_table_v06"}
    assert summary == [
        {
            "summary_id": "M0_LABEL_RULE_TABLE_V06",
            "label_rule_artifact": "m0_label_rule_table_v06",
            "family_id": "M0",
            "formula_slot": "morphology_label_rule",
            "rule_components": "6",
            "activated_rows_covered": "18",
            "row_label_values_written": "0",
            "label_rule_status": "M0_LABEL_RULE_TABLE_READY_NO_LABEL_VALUES",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_LABEL_RULE_TABLE_READY_SCORING_BLOCKED",
            "next_required_artifact": "m1_tau_response_formula_table_v06",
            "claim_boundary": "m0_label_rule_table_only_no_label_validation_no_scores_no_dark_sector_verdict",
        }
    ]
    assert "M0_LABEL_RULE_TABLE_READY_SCORING_BLOCKED" in note
    assert "writes no row-level label values" in note
    assert "does not compute endpoint scores" in note


def test_v06_m1_tau_response_formula_table_closes_response_slot_without_formula_or_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m1_tau_response_formula_table_v06.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m1_tau_response_formula_table_summary_v06.csv").open()))
    note = (ROOT / "docs/m1_tau_response_formula_table_v06.md").read_text()

    assert len(rows) == 6
    assert {row["family_id"] for row in rows} == {"M1"}
    assert {row["formula_slot"] for row in rows} == {"tau_response_formula"}
    assert {row["response_component"] for row in rows} == {
        "activation_rule",
        "carrier",
        "amplitude_law",
        "scale_law",
        "channel_handoff",
        "zero_response_policy",
    }
    assert all(row["response_tau_formula_claimed"] == "false" for row in rows)
    assert all(row["numeric_response_values_written"] == "0" for row in rows)
    assert all(row["family_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m1_admissibility_table_v06"}
    assert summary == [
        {
            "summary_id": "M1_TAU_RESPONSE_FORMULA_TABLE_V06",
            "response_formula_table_artifact": "m1_tau_response_formula_table_v06",
            "family_id": "M1",
            "formula_slot": "tau_response_formula",
            "response_components": "6",
            "response_tau_formula_claimed": "false",
            "numeric_response_values_written": "0",
            "family_prediction_rows_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_TAU_RESPONSE_FORMULA_TABLE_READY_ADMISSIBILITY_BLOCKED",
            "next_required_artifact": "m1_admissibility_table_v06",
            "claim_boundary": "m1_tau_response_formula_table_only_no_response_tau_formula_no_predictions_no_scores",
        }
    ]
    assert "M1_TAU_RESPONSE_FORMULA_TABLE_READY_ADMISSIBILITY_BLOCKED" in note
    assert "does not claim a `Response_tau` formula" in note
    assert "writes no M1 prediction" in note


def test_v06_m1_admissibility_table_closes_admissibility_without_values_or_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m1_admissibility_table_v06.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m1_admissibility_table_summary_v06.csv").open()))
    note = (ROOT / "docs/m1_admissibility_table_v06.md").read_text()

    assert len(rows) == 6
    assert {row["family_id"] for row in rows} == {"M1"}
    assert {row["formula_slot"] for row in rows} == {"response_admissibility_rule"}
    assert {row["admissibility_class"] for row in rows} == {
        "source_freeze_admissibility",
        "non_circularity_guard",
        "no_posthoc_rescue_guard",
        "scale_readout_guard",
        "zero_response_guard",
        "prediction_handoff_guard",
    }
    assert all(row["admissibility_status"] == "READY" for row in rows)
    assert all(row["response_tau_formula_claim_allowed"] == "false" for row in rows)
    assert all(row["numeric_response_values_allowed"] == "false" for row in rows)
    assert all(row["family_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m2_benchmark_profile_table_v06"}
    assert summary == [
        {
            "summary_id": "M1_ADMISSIBILITY_TABLE_V06",
            "admissibility_artifact": "m1_admissibility_table_v06",
            "response_formula_table_status": "READY",
            "family_id": "M1",
            "formula_slot": "response_admissibility_rule",
            "admissibility_rows": "6",
            "ready_admissibility_rows": "6",
            "blocked_admissibility_rows": "0",
            "response_tau_formula_claim_allowed": "false",
            "numeric_response_values_allowed": "false",
            "family_prediction_rows_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_ADMISSIBILITY_TABLE_READY_M2_BENCHMARK_BLOCKED",
            "next_required_artifact": "m2_benchmark_profile_table_v06",
            "claim_boundary": "m1_admissibility_table_only_no_response_tau_formula_no_values_no_predictions_no_scores",
        }
    ]
    assert "M1_ADMISSIBILITY_TABLE_READY_M2_BENCHMARK_BLOCKED" in note
    assert "does not claim a `Response_tau` formula" in note
    assert "writes no M1 prediction" in note


def test_v10_m1_response_parameter_inventory_prepares_countability_without_values_or_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m1_response_parameter_inventory_v10.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m1_response_parameter_inventory_summary_v10.csv").open()))
    note = (ROOT / "docs/m1_response_parameter_inventory_v10.md").read_text()

    assert len(rows) == 6
    assert [row["inventory_row_id"] for row in rows] == [f"M1RPI10_{idx:03d}" for idx in range(1, 7)]
    assert {row["readiness_id"] for row in rows} == {"NCR05_M1_GLOBAL"}
    assert {row["inventory_scope"] for row in rows} == {"global_response_parameters"}
    assert {row["response_component"] for row in rows} == {
        "activation_rule",
        "carrier",
        "amplitude_law",
        "scale_law",
        "channel_handoff",
        "zero_response_policy",
    }
    assert all(row["countability_status"] == "COUNTABILITY_CLASSIFICATION_PENDING" for row in rows)
    assert all(row["count_value_written"] == "0" for row in rows)
    assert all(row["numeric_response_value_written"] == "0" for row in rows)
    assert all(row["per_galaxy_privilege_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "m1_response_parameter_count_classification_v11.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "M1_RESPONSE_PARAMETER_INVENTORY_V10",
            "inventory_artifact": "m1_response_parameter_inventory_v10",
            "readiness_id": "NCR05_M1_GLOBAL",
            "family_id": "M1",
            "inventory_rows": "6",
            "inventory_rows_present": "6",
            "countability_classified_rows": "0",
            "numeric_count_values_written": "0",
            "numeric_response_values_written": "0",
            "per_galaxy_privilege_values_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_RESPONSE_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING",
            "next_required_artifact": "m1_response_parameter_count_classification_v11.csv",
            "claim_boundary": "m1_response_parameter_inventory_only_no_counts_no_values_no_scores",
        }
    ]
    assert "Response_tau formula" in note
    assert "m1_response_parameter_count_classification_v11.csv" in note


def test_v11_m1_response_parameter_count_classification_defers_values_and_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m1_response_parameter_count_classification_v11.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m1_response_parameter_count_classification_summary_v11.csv").open()))
    note = (ROOT / "docs/m1_response_parameter_count_classification_v11.md").read_text()

    assert len(rows) == 6
    assert [row["classification_row_id"] for row in rows] == [f"M1RPCC11_{idx:03d}" for idx in range(1, 7)]
    assert {row["readiness_id"] for row in rows} == {"NCR05_M1_GLOBAL"}
    assert {row["family_id"] for row in rows} == {"M1"}
    assert {row["response_component"] for row in rows} == {
        "activation_rule",
        "carrier",
        "amplitude_law",
        "scale_law",
        "channel_handoff",
        "zero_response_policy",
    }
    classes = {row["response_component"]: row["countability_class"] for row in rows}
    assert classes == {
        "activation_rule": "FIXED_ADMISSIBILITY_GUARD_COUNTS_IF_ROW_SPECIFIC_SWITCH",
        "carrier": "FIXED_PLACEHOLDER_COUNTS_IF_PHYSICAL_CARRIER_PARAMETERIZED",
        "amplitude_law": "COUNT_IF_ADJUSTABLE_RESPONSE_AMPLITUDE",
        "scale_law": "COUNT_IF_ADJUSTABLE_RESPONSE_SCALE",
        "channel_handoff": "FIXED_PROTOCOL_HANDOFF_CHILD_SLOTS_COUNT",
        "zero_response_policy": "FIXED_NULL_ROUTE_COUNTS_IF_RESCUE_TERM",
    }
    assert all(row["classification_status"] == "CLASSIFIED_COUNT_VALUE_PENDING" for row in rows)
    assert all(row["numeric_count_value_written"] == "0" for row in rows)
    assert all(row["numeric_response_value_written"] == "0" for row in rows)
    assert all(row["per_galaxy_privilege_value_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "m1_response_parameter_count_value_ledger_v12.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "M1_RESPONSE_PARAMETER_COUNT_CLASSIFICATION_V11",
            "classification_artifact": "m1_response_parameter_count_classification_v11",
            "inventory_status": "M1_RESPONSE_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING",
            "classification_rows": "6",
            "classified_rows": "6",
            "fixed_or_guard_classes": "4",
            "count_if_adjustable_classes": "2",
            "disqualifying_classes": "0",
            "numeric_count_values_written": "0",
            "numeric_response_values_written": "0",
            "per_galaxy_privilege_values_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_RESPONSE_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING",
            "next_required_artifact": "m1_response_parameter_count_value_ledger_v12.csv",
            "claim_boundary": "m1_response_parameter_count_classification_only_no_counts_no_values_no_scores",
        }
    ]
    assert "Response_tau formula" in note
    assert "m1_response_parameter_count_value_ledger_v12.csv" in note


def test_v12_m1_response_parameter_count_value_ledger_keeps_response_slots_pending() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m1_response_parameter_count_value_ledger_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m1_response_parameter_count_value_ledger_summary_v12.csv").open()))
    note = (ROOT / "docs/m1_response_parameter_count_value_ledger_v12.md").read_text()

    assert len(rows) == 6
    assert [row["ledger_row_id"] for row in rows] == [f"M1RPCVL12_{idx:03d}" for idx in range(1, 7)]
    assert {row["readiness_id"] for row in rows} == {"NCR05_M1_GLOBAL"}
    assert {row["family_id"] for row in rows} == {"M1"}
    statuses = {row["response_component"]: row["count_value_status"] for row in rows}
    assert statuses == {
        "activation_rule": "RESOLVED_ZERO_ADMISSIBILITY_GUARD",
        "carrier": "CONDITIONAL_COUNT_VALUE_PENDING",
        "amplitude_law": "CONDITIONAL_COUNT_VALUE_PENDING",
        "scale_law": "CONDITIONAL_COUNT_VALUE_PENDING",
        "channel_handoff": "RESOLVED_ZERO_PROTOCOL_HANDOFF_CONTAINER",
        "zero_response_policy": "RESOLVED_ZERO_NULL_ROUTE_GUARD",
    }
    values = {row["response_component"]: row["slot_count_value"] for row in rows}
    assert values["activation_rule"] == "0"
    assert values["channel_handoff"] == "0"
    assert values["zero_response_policy"] == "0"
    assert values["carrier"] == "VALUE_PENDING_RESPONSE_SLOT_RESOLUTION"
    assert values["amplitude_law"] == "VALUE_PENDING_RESPONSE_SLOT_RESOLUTION"
    assert values["scale_law"] == "VALUE_PENDING_RESPONSE_SLOT_RESOLUTION"
    assert sum(row["resolution_needed"] == "true" for row in rows) == 3
    assert all(row["final_m1_global_count_input_allowed"] == "false" for row in rows)
    assert all(row["response_value_input_allowed"] == "false" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(
        row["next_required_artifact"] in {"m1_response_parameter_adjustable_slot_resolution_v13.csv", "none_until_response_slot_resolution"}
        for row in rows
    )
    assert summary == [
        {
            "summary_id": "M1_RESPONSE_PARAMETER_COUNT_VALUE_LEDGER_V12",
            "ledger_artifact": "m1_response_parameter_count_value_ledger_v12",
            "classification_status": "M1_RESPONSE_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING",
            "ledger_rows": "6",
            "resolved_zero_rows": "3",
            "conditional_pending_rows": "3",
            "numeric_slot_count_values_written": "3",
            "final_m1_global_count_written": "false",
            "numeric_response_values_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_RESPONSE_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
            "next_required_artifact": "m1_response_parameter_adjustable_slot_resolution_v13.csv",
            "claim_boundary": "m1_response_parameter_count_value_ledger_only_no_final_k_no_response_values_no_scores",
        }
    ]
    assert "Response_tau formula" in note
    assert "m1_response_parameter_adjustable_slot_resolution_v13.csv" in note


def test_v13_m1_response_parameter_adjustable_slot_resolution_resolves_current_scaffold_slots_without_response_values() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m1_response_parameter_adjustable_slot_resolution_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m1_response_parameter_adjustable_slot_resolution_summary_v13.csv").open()))
    note = (ROOT / "docs/m1_response_parameter_adjustable_slot_resolution_v13.md").read_text()

    assert len(rows) == 3
    assert [row["resolution_row_id"] for row in rows] == [f"M1RPASR13_{idx:03d}" for idx in range(1, 4)]
    assert {row["ledger_row_id"] for row in rows} == {"M1RPCVL12_002", "M1RPCVL12_003", "M1RPCVL12_004"}
    assert {row["response_component"] for row in rows} == {"carrier", "amplitude_law", "scale_law"}
    assert all(row["slot_resolution_status"] == "RESOLVED_ZERO_INACTIVE_OR_PLACEHOLDER_RESPONSE_SLOT" for row in rows)
    assert all(row["slot_count_value"] == "0" for row in rows)
    assert all(row["adjustable_response_parameter_found"] == "false" for row in rows)
    assert all(row["final_count_candidate_input_allowed"] == "true" for row in rows)
    assert all(row["response_value_input_allowed"] == "false" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "m1_response_parameter_final_count_candidate_v14.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "M1_RESPONSE_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13",
            "resolution_artifact": "m1_response_parameter_adjustable_slot_resolution_v13",
            "ledger_status": "M1_RESPONSE_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
            "conditional_rows_checked": "3",
            "resolved_zero_rows": "3",
            "unresolved_rows": "0",
            "adjustable_response_parameters_found": "0",
            "final_m1_global_count_candidate_ready": "true",
            "final_m1_global_count_written": "false",
            "numeric_response_values_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_RESPONSE_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE",
            "next_required_artifact": "m1_response_parameter_final_count_candidate_v14.csv",
            "claim_boundary": "m1_response_parameter_adjustable_slot_resolution_only_no_final_k_no_response_values_no_scores",
        }
    ]
    assert "does not prove that an M1 response layer is physically absent" in note
    assert "m1_response_parameter_final_count_candidate_v14.csv" in note


def test_v14_m1_response_parameter_final_count_candidate_ready_for_freeze_only() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m1_response_parameter_final_count_candidate_v14.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m1_response_parameter_final_count_candidate_summary_v14.csv").open()))
    note = (ROOT / "docs/m1_response_parameter_final_count_candidate_v14.md").read_text()

    assert rows == [
        {
            "candidate_row_id": "M1RPFC14_001",
            "family_id": "M1",
            "count_domain": "global_response_parameters",
            "input_artifacts": "m1_response_parameter_count_value_ledger_v12.csv;m1_response_parameter_adjustable_slot_resolution_v13.csv",
            "slot_count_rows_used": "6",
            "resolved_zero_slot_rows": "6",
            "unresolved_slot_rows": "0",
            "adjustable_response_parameters_found": "0",
            "candidate_k_m1_global": "0",
            "candidate_status": "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
            "freeze_input_allowed": "true",
            "response_value_input_allowed": "false",
            "parsimony_input_allowed": "false",
            "next_required_artifact": "m1_response_parameter_final_count_freeze_v15.csv",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_response_activation;posthoc_response_amplitude;numeric_score_value",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "m1_response_parameter_final_count_candidate_only_no_freeze_no_response_values_no_scores",
        }
    ]
    assert summary == [
        {
            "summary_id": "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14",
            "candidate_artifact": "m1_response_parameter_final_count_candidate_v14",
            "v12_ledger_status": "M1_RESPONSE_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
            "v13_resolution_status": "M1_RESPONSE_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE",
            "slot_count_rows_used": "6",
            "resolved_zero_slot_rows": "6",
            "unresolved_slot_rows": "0",
            "adjustable_response_parameters_found": "0",
            "candidate_k_m1_global": "0",
            "final_count_frozen": "false",
            "numeric_response_values_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
            "next_required_artifact": "m1_response_parameter_final_count_freeze_v15.csv",
            "claim_boundary": "m1_response_parameter_final_count_candidate_only_no_freeze_no_response_values_no_scores",
        }
    ]
    assert "`Response_tau`" in note
    assert "m1_response_parameter_final_count_freeze_v15.csv" in note


def test_v15_m1_response_parameter_final_count_freeze_hands_off_to_per_galaxy_response_privilege_audit() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m1_response_parameter_final_count_freeze_v15.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m1_response_parameter_final_count_freeze_summary_v15.csv").open()))
    note = (ROOT / "docs/m1_response_parameter_final_count_freeze_v15.md").read_text()

    assert rows == [
        {
            "freeze_row_id": "M1RPFCF15_001",
            "candidate_row_id": "M1RPFC14_001",
            "family_id": "M1",
            "count_domain": "global_response_parameters",
            "frozen_k_m1_global": "0",
            "freeze_status": "M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_RESPONSE_PRIVILEGE_AUDIT_PENDING",
            "candidate_status": "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
            "source_artifacts": "m1_response_parameter_count_value_ledger_v12.csv;m1_response_parameter_adjustable_slot_resolution_v13.csv",
            "per_galaxy_response_privilege_input_allowed": "true",
            "response_value_input_allowed": "false",
            "parsimony_input_allowed": "false",
            "next_required_artifact": "m1_per_galaxy_response_privilege_count_audit_v10.csv",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_response_activation;posthoc_response_amplitude;numeric_score_value",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "m1_response_parameter_final_count_freeze_only_no_response_values_no_parsimony_no_scores",
        }
    ]
    assert summary == [
        {
            "summary_id": "M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15",
            "freeze_artifact": "m1_response_parameter_final_count_freeze_v15",
            "candidate_status": "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
            "frozen_k_m1_global": "0",
            "final_count_frozen": "true",
            "numeric_response_values_written": "0",
            "per_galaxy_response_privilege_counts_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_RESPONSE_PRIVILEGE_AUDIT_PENDING",
            "next_required_artifact": "m1_per_galaxy_response_privilege_count_audit_v10.csv",
            "claim_boundary": "m1_response_parameter_final_count_freeze_only_no_response_values_no_parsimony_no_scores",
        }
    ]
    assert "`Response_tau`" in note
    assert "m1_per_galaxy_response_privilege_count_audit_v10.csv" in note


def test_v10_m1_per_galaxy_response_privilege_count_audit_prepares_freeze_without_response_values() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m1_per_galaxy_response_privilege_count_audit_v10.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m1_per_galaxy_response_privilege_count_audit_summary_v10.csv").open()))
    note = (ROOT / "docs/m1_per_galaxy_response_privilege_count_audit_v10.md").read_text()

    assert len(rows) == 18
    assert [row["audit_row_id"] for row in rows] == [f"M1PGRPCA10_{idx:03d}" for idx in range(1, 19)]
    assert {row["source_activation_status"] for row in rows} == {"ACTIVATION_BLOCKED"}
    assert {row["m1_global_freeze_status"] for row in rows} == {
        "M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_RESPONSE_PRIVILEGE_AUDIT_PENDING"
    }
    assert {row["m1_admissibility_status"] for row in rows} == {"M1_ADMISSIBILITY_TABLE_READY_M2_BENCHMARK_BLOCKED"}
    assert {row["row_response_privilege_status"] for row in rows} == {
        "RESOLVED_ZERO_NO_ROW_SPECIFIC_M1_RESPONSE_PRIVILEGE"
    }
    assert all(row["per_galaxy_response_privilege_count_value"] == "0" for row in rows)
    assert all(row["freeze_input_allowed"] == "true" for row in rows)
    assert all(row["response_value_input_allowed"] == "false" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "m1_per_galaxy_response_privilege_count_freeze_v11.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_AUDIT_V10",
            "audit_artifact": "m1_per_galaxy_response_privilege_count_audit_v10",
            "source_rows_checked": "18",
            "resolved_zero_rows": "18",
            "unresolved_rows": "0",
            "per_galaxy_response_privilege_values_written": "18",
            "per_galaxy_response_count_freeze_ready": "true",
            "per_galaxy_response_count_frozen": "false",
            "numeric_response_values_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE",
            "next_required_artifact": "m1_per_galaxy_response_privilege_count_freeze_v11.csv",
            "claim_boundary": "m1_per_galaxy_response_privilege_count_audit_only_no_freeze_no_response_values_no_scores",
        }
    ]
    assert "RESOLVED_ZERO_NO_ROW_SPECIFIC_M1_RESPONSE_PRIVILEGE" in note
    assert "`Response_tau`" in note
    assert "m1_per_galaxy_response_privilege_count_freeze_v11.csv" in note


def test_v11_m1_per_galaxy_response_privilege_count_freeze_hands_off_to_m2_global_inventory() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m1_per_galaxy_response_privilege_count_freeze_v11.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m1_per_galaxy_response_privilege_count_freeze_summary_v11.csv").open()))
    note = (ROOT / "docs/m1_per_galaxy_response_privilege_count_freeze_v11.md").read_text()

    assert len(rows) == 18
    assert [row["freeze_row_id"] for row in rows] == [f"M1PGRPCF11_{idx:03d}" for idx in range(1, 19)]
    assert {row["freeze_status"] for row in rows} == {
        "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11_FROZEN"
    }
    assert {row["audit_status"] for row in rows} == {"RESOLVED_ZERO_NO_ROW_SPECIFIC_M1_RESPONSE_PRIVILEGE"}
    assert all(row["frozen_per_galaxy_response_privilege_count"] == "0" for row in rows)
    assert all(row["response_value_input_allowed"] == "false" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "m2_benchmark_parameter_inventory_v10.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11",
            "freeze_artifact": "m1_per_galaxy_response_privilege_count_freeze_v11",
            "audit_status": "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE",
            "source_rows_checked": "18",
            "frozen_zero_rows": "18",
            "unresolved_rows": "0",
            "per_galaxy_response_count_frozen": "true",
            "frozen_per_galaxy_response_privilege_count_total": "0",
            "numeric_response_values_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11_READY_M2_GLOBAL_COUNT_PENDING",
            "next_required_artifact": "m2_benchmark_parameter_inventory_v10.csv",
            "claim_boundary": (
                "m1_per_galaxy_response_privilege_count_freeze_only_no_response_values_no_parsimony_no_scores"
            ),
        }
    ]
    assert "`Response_tau`" in note
    assert "m2_benchmark_parameter_inventory_v10.csv" in note


def test_v10_m2_benchmark_parameter_inventory_prepares_countability_classification() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_parameter_inventory_v10.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_parameter_inventory_summary_v10.csv").open()))
    note = (ROOT / "docs/m2_benchmark_parameter_inventory_v10.md").read_text()

    assert len(rows) == 12
    assert [row["inventory_row_id"] for row in rows] == [f"M2BPI10_{idx:03d}" for idx in range(1, 13)]
    assert {row["readiness_id"] for row in rows} == {"NCR05_M2_GLOBAL"}
    assert {row["family_id"] for row in rows} == {"M2"}
    assert {row["source_artifact"] for row in rows} == {
        "m2_benchmark_profile_table_v06",
        "m2_nuisance_policy_table_v06",
    }
    assert sum(row["source_artifact"] == "m2_benchmark_profile_table_v06" for row in rows) == 6
    assert sum(row["source_artifact"] == "m2_nuisance_policy_table_v06" for row in rows) == 6
    assert all(row["countability_status"] == "COUNTABILITY_CLASSIFICATION_PENDING" for row in rows)
    assert all(row["count_value_written"] == "0" for row in rows)
    assert all(row["numeric_benchmark_value_written"] == "0" for row in rows)
    assert all(row["family_prediction_rows_written"] == "0" for row in rows)
    assert all(row["per_galaxy_privilege_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "m2_benchmark_parameter_count_classification_v11.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "M2_BENCHMARK_PARAMETER_INVENTORY_V10",
            "inventory_artifact": "m2_benchmark_parameter_inventory_v10",
            "readiness_id": "NCR05_M2_GLOBAL",
            "family_id": "M2",
            "inventory_rows": "12",
            "profile_source_rows": "6",
            "nuisance_source_rows": "6",
            "inventory_rows_present": "12",
            "countability_classified_rows": "0",
            "numeric_count_values_written": "0",
            "numeric_benchmark_values_written": "0",
            "family_prediction_rows_written": "0",
            "per_galaxy_privilege_values_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M2_BENCHMARK_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING",
            "next_required_artifact": "m2_benchmark_parameter_count_classification_v11.csv",
            "claim_boundary": "m2_benchmark_parameter_inventory_only_no_counts_no_values_no_predictions_no_scores",
        }
    ]
    assert "benchmark-profile and nuisance-policy rows" in note
    assert "m2_benchmark_parameter_count_classification_v11.csv" in note


def test_v11_m2_benchmark_parameter_count_classification_prepares_value_ledger() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_parameter_count_classification_v11.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_parameter_count_classification_summary_v11.csv").open()))
    note = (ROOT / "docs/m2_benchmark_parameter_count_classification_v11.md").read_text()

    assert len(rows) == 12
    assert [row["classification_row_id"] for row in rows] == [f"M2BPCC11_{idx:03d}" for idx in range(1, 13)]
    assert {row["readiness_id"] for row in rows} == {"NCR05_M2_GLOBAL"}
    assert {row["family_id"] for row in rows} == {"M2"}
    assert {row["classification_status"] for row in rows} == {"CLASSIFIED_COUNT_VALUE_PENDING"}
    assert sum(row["countability_class"].startswith("FIXED_") for row in rows) == 4
    assert sum("COUNT_IF" in row["countability_class"] for row in rows) == 8
    assert all(row["numeric_count_value_written"] == "0" for row in rows)
    assert all(row["numeric_benchmark_value_written"] == "0" for row in rows)
    assert all(row["family_prediction_rows_written"] == "0" for row in rows)
    assert all(row["per_galaxy_privilege_value_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "m2_benchmark_parameter_count_value_ledger_v12.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "M2_BENCHMARK_PARAMETER_COUNT_CLASSIFICATION_V11",
            "classification_artifact": "m2_benchmark_parameter_count_classification_v11",
            "inventory_status": "M2_BENCHMARK_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING",
            "classification_rows": "12",
            "classified_rows": "12",
            "fixed_or_guard_classes": "4",
            "count_if_adjustable_classes": "8",
            "disqualifying_classes": "0",
            "numeric_count_values_written": "0",
            "numeric_benchmark_values_written": "0",
            "family_prediction_rows_written": "0",
            "per_galaxy_privilege_values_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M2_BENCHMARK_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING",
            "next_required_artifact": "m2_benchmark_parameter_count_value_ledger_v12.csv",
            "claim_boundary": "m2_benchmark_parameter_count_classification_only_no_counts_no_values_no_predictions_no_scores",
        }
    ]
    assert "twelve M2 benchmark" in note
    assert "m2_benchmark_parameter_count_value_ledger_v12.csv" in note


def test_v12_m2_benchmark_parameter_count_value_ledger_prepares_adjustable_slot_resolution() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_parameter_count_value_ledger_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_parameter_count_value_ledger_summary_v12.csv").open()))
    note = (ROOT / "docs/m2_benchmark_parameter_count_value_ledger_v12.md").read_text()

    assert len(rows) == 12
    assert [row["ledger_row_id"] for row in rows] == [f"M2BPCVL12_{idx:03d}" for idx in range(1, 13)]
    assert {row["readiness_id"] for row in rows} == {"NCR05_M2_GLOBAL"}
    assert {row["family_id"] for row in rows} == {"M2"}
    assert sum(row["slot_count_value"] == "0" for row in rows) == 4
    assert sum(row["resolution_needed"] == "true" for row in rows) == 8
    assert sum(row["slot_count_value"] == "VALUE_PENDING_BENCHMARK_SLOT_RESOLUTION" for row in rows) == 8
    assert all(row["final_m2_global_count_input_allowed"] == "false" for row in rows)
    assert all(row["benchmark_value_input_allowed"] == "false" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(
        row["next_required_artifact"] in {
            "m2_benchmark_parameter_adjustable_slot_resolution_v13.csv",
            "none_until_benchmark_slot_resolution",
        }
        for row in rows
    )
    assert summary == [
        {
            "summary_id": "M2_BENCHMARK_PARAMETER_COUNT_VALUE_LEDGER_V12",
            "ledger_artifact": "m2_benchmark_parameter_count_value_ledger_v12",
            "classification_status": "M2_BENCHMARK_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING",
            "ledger_rows": "12",
            "resolved_zero_rows": "4",
            "conditional_pending_rows": "8",
            "numeric_slot_count_values_written": "4",
            "final_m2_global_count_written": "false",
            "numeric_benchmark_values_written": "0",
            "family_prediction_rows_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M2_BENCHMARK_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
            "next_required_artifact": "m2_benchmark_parameter_adjustable_slot_resolution_v13.csv",
            "claim_boundary": "m2_benchmark_parameter_count_value_ledger_only_no_final_k_no_values_no_predictions_no_scores",
        }
    ]
    assert "benchmark-slot resolution" in note
    assert "m2_benchmark_parameter_adjustable_slot_resolution_v13.csv" in note


def test_v13_m2_benchmark_parameter_adjustable_slot_resolution_prepares_final_count_candidate() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_parameter_adjustable_slot_resolution_v13.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/m2_benchmark_parameter_adjustable_slot_resolution_summary_v13.csv").open())
    )
    note = (ROOT / "docs/m2_benchmark_parameter_adjustable_slot_resolution_v13.md").read_text()

    assert len(rows) == 8
    assert [row["resolution_row_id"] for row in rows] == [f"M2BPASR13_{idx:03d}" for idx in range(1, 9)]
    assert {row["readiness_id"] for row in rows} == {"NCR05_M2_GLOBAL"}
    assert {row["family_id"] for row in rows} == {"M2"}
    assert {row["prior_count_value_status"] for row in rows} == {"CONDITIONAL_COUNT_VALUE_PENDING"}
    assert {row["slot_resolution_status"] for row in rows} == {
        "RESOLVED_ZERO_NO_ACTIVE_BENCHMARK_SLOT_UNDER_CURRENT_SCAFFOLD"
    }
    assert all(row["slot_count_value"] == "0" for row in rows)
    assert all(row["adjustable_benchmark_parameter_found"] == "false" for row in rows)
    assert all(row["final_count_candidate_input_allowed"] == "true" for row in rows)
    assert all(row["benchmark_value_input_allowed"] == "false" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "m2_benchmark_parameter_final_count_candidate_v14.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "M2_BENCHMARK_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13",
            "resolution_artifact": "m2_benchmark_parameter_adjustable_slot_resolution_v13",
            "ledger_status": "M2_BENCHMARK_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
            "conditional_rows_checked": "8",
            "resolved_zero_rows": "8",
            "unresolved_rows": "0",
            "adjustable_benchmark_parameters_found": "0",
            "final_m2_global_count_candidate_ready": "true",
            "final_m2_global_count_written": "false",
            "numeric_benchmark_values_written": "0",
            "family_prediction_rows_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M2_BENCHMARK_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE",
            "next_required_artifact": "m2_benchmark_parameter_final_count_candidate_v14.csv",
            "claim_boundary": "m2_benchmark_parameter_adjustable_slot_resolution_only_no_final_k_no_values_no_predictions_no_scores",
        }
    ]
    assert "eight conditional M2 benchmark and nuisance slots" in note
    assert "does not decide the dark-sector question" in note


def test_v14_m2_benchmark_parameter_final_count_candidate_prepares_freeze() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_parameter_final_count_candidate_v14.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_parameter_final_count_candidate_summary_v14.csv").open()))
    note = (ROOT / "docs/m2_benchmark_parameter_final_count_candidate_v14.md").read_text()

    assert rows == [
        {
            "candidate_row_id": "M2BPFC14_001",
            "family_id": "M2",
            "count_domain": "global_benchmark_parameters",
            "input_artifacts": "m2_benchmark_parameter_count_value_ledger_v12.csv;m2_benchmark_parameter_adjustable_slot_resolution_v13.csv",
            "slot_count_rows_used": "12",
            "resolved_zero_slot_rows": "12",
            "unresolved_slot_rows": "0",
            "adjustable_benchmark_parameters_found": "0",
            "candidate_k_m2_global": "0",
            "candidate_status": "M2_BENCHMARK_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
            "freeze_input_allowed": "true",
            "benchmark_value_input_allowed": "false",
            "parsimony_input_allowed": "false",
            "next_required_artifact": "m2_benchmark_parameter_final_count_freeze_v15.csv",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_profile_switch;posthoc_prior_width;posthoc_uncertainty_policy;posthoc_baryonic_rescaling;numeric_score_value",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "m2_benchmark_parameter_final_count_candidate_only_no_freeze_no_values_no_predictions_no_scores",
        }
    ]
    assert summary == [
        {
            "summary_id": "M2_BENCHMARK_PARAMETER_FINAL_COUNT_CANDIDATE_V14",
            "candidate_artifact": "m2_benchmark_parameter_final_count_candidate_v14",
            "v12_ledger_status": "M2_BENCHMARK_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
            "v13_resolution_status": "M2_BENCHMARK_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE",
            "slot_count_rows_used": "12",
            "resolved_zero_slot_rows": "12",
            "unresolved_slot_rows": "0",
            "adjustable_benchmark_parameters_found": "0",
            "candidate_k_m2_global": "0",
            "final_count_frozen": "false",
            "numeric_benchmark_values_written": "0",
            "family_prediction_rows_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M2_BENCHMARK_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
            "next_required_artifact": "m2_benchmark_parameter_final_count_freeze_v15.csv",
            "claim_boundary": "m2_benchmark_parameter_final_count_candidate_only_no_freeze_no_values_no_predictions_no_scores",
        }
    ]
    assert "candidate M2 global benchmark-parameter count" in note
    assert "does not decide whether a dark-sector benchmark is physically absent" in note


def test_v15_m2_benchmark_parameter_final_count_freeze_prepares_per_galaxy_audit() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_parameter_final_count_freeze_v15.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_parameter_final_count_freeze_summary_v15.csv").open()))
    note = (ROOT / "docs/m2_benchmark_parameter_final_count_freeze_v15.md").read_text()

    assert rows == [
        {
            "freeze_row_id": "M2BPFCF15_001",
            "candidate_row_id": "M2BPFC14_001",
            "family_id": "M2",
            "count_domain": "global_benchmark_parameters",
            "frozen_k_m2_global": "0",
            "freeze_status": "M2_BENCHMARK_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_BENCHMARK_PRIVILEGE_AUDIT_PENDING",
            "candidate_status": "M2_BENCHMARK_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
            "source_artifacts": "m2_benchmark_parameter_count_value_ledger_v12.csv;m2_benchmark_parameter_adjustable_slot_resolution_v13.csv",
            "per_galaxy_benchmark_privilege_input_allowed": "true",
            "benchmark_value_input_allowed": "false",
            "parsimony_input_allowed": "false",
            "next_required_artifact": "m2_per_galaxy_benchmark_privilege_count_audit_v10.csv",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_profile_switch;posthoc_prior_width;posthoc_uncertainty_policy;posthoc_baryonic_rescaling;numeric_score_value",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "m2_benchmark_parameter_final_count_freeze_only_no_benchmark_values_no_predictions_no_parsimony_no_scores",
        }
    ]
    assert summary == [
        {
            "summary_id": "M2_BENCHMARK_PARAMETER_FINAL_COUNT_FREEZE_V15",
            "freeze_artifact": "m2_benchmark_parameter_final_count_freeze_v15",
            "candidate_status": "M2_BENCHMARK_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
            "frozen_k_m2_global": "0",
            "final_count_frozen": "true",
            "numeric_benchmark_values_written": "0",
            "per_galaxy_benchmark_privilege_counts_written": "0",
            "family_prediction_rows_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M2_BENCHMARK_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_BENCHMARK_PRIVILEGE_AUDIT_PENDING",
            "next_required_artifact": "m2_per_galaxy_benchmark_privilege_count_audit_v10.csv",
            "claim_boundary": "m2_benchmark_parameter_final_count_freeze_only_no_benchmark_values_no_predictions_no_parsimony_no_scores",
        }
    ]
    assert "k_M2_global = 0" in note
    assert "does not authorize endpoint scoring" in note


def test_v10_m2_per_galaxy_benchmark_privilege_count_audit_prepares_freeze_without_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m2_per_galaxy_benchmark_privilege_count_audit_v10.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m2_per_galaxy_benchmark_privilege_count_audit_summary_v10.csv").open()))
    note = (ROOT / "docs/m2_per_galaxy_benchmark_privilege_count_audit_v10.md").read_text()

    assert len(rows) == 18
    assert [row["audit_row_id"] for row in rows] == [f"M2PGBMPCA10_{idx:03d}" for idx in range(1, 19)]
    assert {row["row_benchmark_privilege_status"] for row in rows} == {
        "RESOLVED_ZERO_NO_ROW_SPECIFIC_M2_BENCHMARK_PRIVILEGE"
    }
    assert all(row["per_galaxy_benchmark_privilege_count_value"] == "0" for row in rows)
    assert all(row["benchmark_value_input_allowed"] == "false" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "m2_per_galaxy_benchmark_privilege_count_freeze_v11.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_AUDIT_V10",
            "audit_artifact": "m2_per_galaxy_benchmark_privilege_count_audit_v10",
            "source_rows_checked": "18",
            "resolved_zero_rows": "18",
            "unresolved_rows": "0",
            "per_galaxy_benchmark_privilege_values_written": "18",
            "per_galaxy_benchmark_count_freeze_ready": "true",
            "per_galaxy_benchmark_count_frozen": "false",
            "numeric_benchmark_values_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE",
            "next_required_artifact": "m2_per_galaxy_benchmark_privilege_count_freeze_v11.csv",
            "claim_boundary": "m2_per_galaxy_benchmark_privilege_count_audit_only_no_freeze_no_benchmark_values_no_parsimony_no_scores",
        }
    ]
    assert "RESOLVED_ZERO_NO_ROW_SPECIFIC_M2_BENCHMARK_PRIVILEGE" in note
    assert "does not decide whether a dark-sector benchmark is physically absent" in note


def test_v11_m2_per_galaxy_benchmark_privilege_count_freeze_hands_off_to_shared_count_policy() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m2_per_galaxy_benchmark_privilege_count_freeze_v11.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m2_per_galaxy_benchmark_privilege_count_freeze_summary_v11.csv").open()))
    note = (ROOT / "docs/m2_per_galaxy_benchmark_privilege_count_freeze_v11.md").read_text()

    assert len(rows) == 18
    assert [row["freeze_row_id"] for row in rows] == [f"M2PGBMPCF11_{idx:03d}" for idx in range(1, 19)]
    assert {row["freeze_status"] for row in rows} == {"M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_FREEZE_V11_FROZEN"}
    assert {row["audit_status"] for row in rows} == {"RESOLVED_ZERO_NO_ROW_SPECIFIC_M2_BENCHMARK_PRIVILEGE"}
    assert all(row["frozen_per_galaxy_benchmark_privilege_count"] == "0" for row in rows)
    assert all(row["benchmark_value_input_allowed"] == "false" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "shared_input_count_discount_policy_v10.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_FREEZE_V11",
            "freeze_artifact": "m2_per_galaxy_benchmark_privilege_count_freeze_v11",
            "audit_status": "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE",
            "source_rows_checked": "18",
            "frozen_zero_rows": "18",
            "unresolved_rows": "0",
            "per_galaxy_benchmark_count_frozen": "true",
            "frozen_per_galaxy_benchmark_privilege_count_total": "0",
            "numeric_benchmark_values_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_FREEZE_V11_READY_SHARED_COUNT_PENDING",
            "next_required_artifact": "shared_input_count_discount_policy_v10.csv",
            "claim_boundary": "m2_per_galaxy_benchmark_privilege_count_freeze_only_no_benchmark_values_no_parsimony_no_scores",
        }
    ]
    assert "All" in note
    assert "shared_input_count_discount_policy_v10.csv" in note


def test_v06_m2_benchmark_profile_table_closes_profile_without_values_or_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_profile_table_v06.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m2_benchmark_profile_table_summary_v06.csv").open()))
    note = (ROOT / "docs/m2_benchmark_profile_table_v06.md").read_text()

    assert len(rows) == 6
    assert {row["family_id"] for row in rows} == {"M2"}
    assert {row["formula_slot"] for row in rows} == {"benchmark_profile_formula"}
    assert {row["profile_component"] for row in rows} == {
        "profile_family_registry",
        "halo_parameter_slots",
        "prior_policy",
        "nuisance_policy_link",
        "profile_switch_policy",
        "prediction_handoff",
    }
    assert all(row["profile_table_status"] == "READY" for row in rows)
    assert all(row["numeric_profile_values_written"] == "0" for row in rows)
    assert all(row["family_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m2_nuisance_policy_table_v06"}
    assert summary == [
        {
            "summary_id": "M2_BENCHMARK_PROFILE_TABLE_V06",
            "benchmark_profile_artifact": "m2_benchmark_profile_table_v06",
            "family_id": "M2",
            "formula_slot": "benchmark_profile_formula",
            "profile_components": "6",
            "numeric_profile_values_written": "0",
            "family_prediction_rows_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M2_BENCHMARK_PROFILE_TABLE_READY_NUISANCE_BLOCKED",
            "next_required_artifact": "m2_nuisance_policy_table_v06",
            "claim_boundary": "m2_benchmark_profile_table_only_no_profile_values_no_predictions_no_scores_no_validation",
        }
    ]
    assert "M2_BENCHMARK_PROFILE_TABLE_READY_NUISANCE_BLOCKED" in note
    assert "does not validate the standard dark sector" in note
    assert "writes no M2 prediction" in note


def test_v06_m2_nuisance_policy_table_closes_policy_without_values_or_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m2_nuisance_policy_table_v06.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m2_nuisance_policy_table_summary_v06.csv").open()))
    note = (ROOT / "docs/m2_nuisance_policy_table_v06.md").read_text()

    assert len(rows) == 6
    assert {row["family_id"] for row in rows} == {"M2"}
    assert {row["formula_slot"] for row in rows} == {"benchmark_nuisance_policy"}
    assert {row["nuisance_component"] for row in rows} == {
        "stellar_mass_to_light_policy",
        "gas_scaling_policy",
        "uncertainty_policy",
        "nuisance_prior_policy",
        "shared_baryonic_fairness_policy",
        "prediction_handoff",
    }
    assert all(row["nuisance_policy_status"] == "READY" for row in rows)
    assert all(row["numeric_nuisance_values_written"] == "0" for row in rows)
    assert all(row["family_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"shared_scoring_input_table_v06"}
    assert summary == [
        {
            "summary_id": "M2_NUISANCE_POLICY_TABLE_V06",
            "nuisance_policy_artifact": "m2_nuisance_policy_table_v06",
            "benchmark_profile_status": "M2_BENCHMARK_PROFILE_TABLE_READY_NUISANCE_BLOCKED",
            "family_id": "M2",
            "formula_slot": "benchmark_nuisance_policy",
            "nuisance_components": "6",
            "numeric_nuisance_values_written": "0",
            "family_prediction_rows_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M2_NUISANCE_POLICY_TABLE_READY_SHARED_INPUTS_BLOCKED",
            "next_required_artifact": "shared_scoring_input_table_v06",
            "claim_boundary": "m2_nuisance_policy_table_only_no_nuisance_values_no_predictions_no_scores_no_validation",
        }
    ]
    assert "M2_NUISANCE_POLICY_TABLE_READY_SHARED_INPUTS_BLOCKED" in note
    assert "does not validate the standard dark sector" in note
    assert "writes no M2 prediction" in note


def test_v06_shared_scoring_input_table_closes_policy_without_values_or_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/shared_scoring_input_table_v06.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/shared_scoring_input_table_summary_v06.csv").open()))
    note = (ROOT / "docs/shared_scoring_input_table_v06.md").read_text()

    assert len(rows) == 6
    assert {row["family_scope"] for row in rows} == {"ALL"}
    assert {row["formula_slot"] for row in rows} == {"shared_scoring_inputs"}
    assert {row["input_component"] for row in rows} == {
        "data_loader_policy",
        "radial_grid_policy",
        "radial_mask_policy",
        "uncertainty_handling_policy",
        "baryonic_component_policy",
        "parameter_count_handoff",
    }
    assert all(row["shared_input_status"] == "READY" for row in rows)
    assert all(row["numeric_input_values_written"] == "0" for row in rows)
    assert all(row["family_prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"numeric_parameter_count_table_v06"}
    assert summary == [
        {
            "summary_id": "SHARED_SCORING_INPUT_TABLE_V06",
            "shared_input_artifact": "shared_scoring_input_table_v06",
            "m2_nuisance_status": "M2_NUISANCE_POLICY_TABLE_READY_SHARED_INPUTS_BLOCKED",
            "family_scope": "ALL",
            "formula_slot": "shared_scoring_inputs",
            "shared_input_components": "6",
            "numeric_input_values_written": "0",
            "family_prediction_rows_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SHARED_SCORING_INPUT_TABLE_READY_PARAMETER_COUNTS_BLOCKED",
            "next_required_artifact": "numeric_parameter_count_table_v06",
            "claim_boundary": "shared_scoring_input_table_only_no_numeric_inputs_no_predictions_no_scores_no_validation",
        }
    ]
    assert "SHARED_SCORING_INPUT_TABLE_READY_PARAMETER_COUNTS_BLOCKED" in note
    assert "writes no family prediction rows" in note
    assert "computes no endpoint scores" in note


def test_v06_numeric_parameter_count_table_closes_contract_without_final_counts_or_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/numeric_parameter_count_table_v06.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/numeric_parameter_count_table_summary_v06.csv").open()))
    note = (ROOT / "docs/numeric_parameter_count_table_v06.md").read_text()

    assert len(rows) == 8
    assert {"M0", "M1", "M2", "ALL"}.issubset({row["family_id"] for row in rows})
    assert all(row["count_value_status"] == "FINAL_NUMERIC_COUNT_VALUE_BLOCKED_UNTIL_V08" for row in rows)
    assert all(row["numeric_count_value"] == "VALUE_NOT_WRITTEN_IN_V06" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("family_winner" in row["forbidden_inputs"] for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"numeric_parameter_count_table_v08.csv"}
    assert summary == [
        {
            "summary_id": "NUMERIC_PARAMETER_COUNT_TABLE_V06",
            "count_artifact": "numeric_parameter_count_table_v06",
            "shared_input_status": "SHARED_SCORING_INPUT_TABLE_READY_PARAMETER_COUNTS_BLOCKED",
            "count_rows": "8",
            "numeric_count_values_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "NUMERIC_PARAMETER_COUNT_TABLE_CONTRACT_READY_FINAL_COUNTS_BLOCKED",
            "next_required_artifact": "numeric_parameter_count_table_v08.csv",
            "claim_boundary": "numeric_parameter_count_table_contract_only_no_final_counts_no_parsimony_no_scores",
        }
    ]
    assert "NUMERIC_PARAMETER_COUNT_TABLE_CONTRACT_READY_FINAL_COUNTS_BLOCKED" in note
    assert "writes no final numeric count values" in note
    assert "computes no parsimony penalty" in note


def test_v10_shared_input_count_discount_policy_freezes_zero_discount_without_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/shared_input_count_discount_policy_v10.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/shared_input_count_discount_policy_summary_v10.csv").open()))
    note = (ROOT / "docs/shared_input_count_discount_policy_v10.md").read_text()

    assert len(rows) == 6
    assert [row["policy_row_id"] for row in rows] == [f"SICDP10_{idx:03d}" for idx in range(1, 7)]
    assert {row["discount_policy_status"] for row in rows} == {"RESOLVED_ZERO_NO_SHARED_INPUT_COUNT_DISCOUNT"}
    assert all(row["shared_discount_count_value"] == "0" for row in rows)
    assert all(row["final_count_input_allowed"] == "true" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "numeric_parameter_count_table_final_values_v10.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10",
            "policy_artifact": "shared_input_count_discount_policy_v10",
            "shared_input_status": "SHARED_SCORING_INPUT_TABLE_READY_PARAMETER_COUNTS_BLOCKED",
            "shared_input_rows_checked": "6",
            "zero_discount_rows": "6",
            "unresolved_rows": "0",
            "shared_discount_policy_frozen": "true",
            "shared_discount_count_total": "0",
            "final_numeric_count_values_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10_READY_FINAL_NUMERIC_COUNTS_PENDING",
            "next_required_artifact": "numeric_parameter_count_table_final_values_v10.csv",
            "claim_boundary": "shared_input_count_discount_policy_only_no_discount_no_final_counts_no_parsimony_no_scores",
        }
    ]
    assert "RESOLVED_ZERO_NO_SHARED_INPUT_COUNT_DISCOUNT" in note
    assert "writes no final numeric parameter counts" in note
    assert "computes no endpoint scores" in note


def test_v08_numeric_parameter_count_table_blocks_final_counts_on_readiness_closure() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/numeric_parameter_count_table_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/numeric_parameter_count_table_summary_v08.csv").open()))
    note = (ROOT / "docs/numeric_parameter_count_table_v08.md").read_text()

    assert len(rows) == 7
    assert {"M0", "M1", "M2", "ALL"}.issubset({row["family_id"] for row in rows})
    assert all(row["readiness_status"] == "COUNT_NOT_READY" for row in rows)
    assert all(row["final_numeric_count_status"] == "FINAL_NUMERIC_COUNT_VALUE_PENDING_EXPLICIT_FINAL_VALUES" for row in rows)
    assert all(row["numeric_parameter_count_value"] == "VALUE_PENDING_READINESS_CLOSURE" for row in rows)
    assert all(row["per_galaxy_privilege_count_value"] == "VALUE_PENDING_READINESS_CLOSURE" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"numeric_parameter_count_table_final_values_v10.csv"}
    assert summary == [
        {
            "summary_id": "NUMERIC_PARAMETER_COUNT_TABLE_V08",
            "count_artifact": "numeric_parameter_count_table_v08",
            "source_contract_status": "NUMERIC_PARAMETER_COUNT_TABLE_CONTRACT_READY_FINAL_COUNTS_BLOCKED",
            "readiness_rows_checked": "7",
            "blocked_count_rows": "7",
            "numeric_count_values_written": "0",
            "per_galaxy_privilege_values_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "NUMERIC_PARAMETER_COUNT_TABLE_V08_BLOCKED_ON_FINAL_NUMERIC_COUNT_VALUES",
            "next_required_artifact": "numeric_parameter_count_table_final_values_v10.csv",
            "claim_boundary": "numeric_parameter_count_table_v08_only_no_parsimony_no_scores_no_verdict",
        }
    ]
    assert "NUMERIC_PARAMETER_COUNT_TABLE_V08" in note
    assert "writes no final numeric parameter counts" in note
    assert "no parsimony penalty" in note


def test_v10_numeric_parameter_count_table_final_values_freezes_zero_counts_without_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/numeric_parameter_count_table_final_values_v10.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/numeric_parameter_count_table_final_values_summary_v10.csv").open()))
    note = (ROOT / "docs/numeric_parameter_count_table_final_values_v10.md").read_text()

    assert len(rows) == 7
    assert [row["final_count_row_id"] for row in rows] == [f"NPCFV10_{idx:03d}" for idx in range(1, 8)]
    assert {row["family_id"] for row in rows} == {"M0", "M1", "M2", "ALL"}
    assert all(row["source_final_numeric_count_status"] == "FINAL_NUMERIC_COUNT_VALUE_PENDING_EXPLICIT_FINAL_VALUES" for row in rows)
    assert all(row["closure_decision"] == "COUNT_READINESS_READY" for row in rows)
    assert all(row["final_numeric_count_status"] == "FINAL_NUMERIC_COUNT_VALUE_FROZEN" for row in rows)
    assert all(row["numeric_parameter_count_value"] == "0" for row in rows)
    assert all(row["per_galaxy_privilege_count_value"] == "0" for row in rows)
    assert all(row["shared_discount_count_value"] == "0" for row in rows)
    assert all(row["final_parsimony_count_value"] == "0" for row in rows)
    assert all(row["parsimony_input_allowed"] == "true" for row in rows)
    assert all(row["next_required_artifact"] == "control_runner_outputs_v08.csv" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "NUMERIC_PARAMETER_COUNT_TABLE_FINAL_VALUES_V10",
            "final_values_artifact": "numeric_parameter_count_table_final_values_v10",
            "v08_status": "NUMERIC_PARAMETER_COUNT_TABLE_V08_BLOCKED_ON_FINAL_NUMERIC_COUNT_VALUES",
            "closure_status": "NUMERIC_COUNT_READINESS_CLOSURE_READY_FOR_FINAL_COUNTS",
            "shared_discount_status": "SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10_READY_FINAL_NUMERIC_COUNTS_PENDING",
            "final_count_rows": "7",
            "final_numeric_count_values_written": "7",
            "per_galaxy_privilege_values_written": "3",
            "shared_discount_count_total": "0",
            "final_parsimony_count_total": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "NUMERIC_PARAMETER_COUNT_TABLE_FINAL_VALUES_V10_READY_FOR_GLOBAL_SCORING_PREREQUISITES",
            "next_required_artifact": "control_runner_outputs_v08.csv",
            "claim_boundary": "numeric_parameter_count_table_final_values_only_no_parsimony_no_scores_no_verdict",
        }
    ]
    assert "M0 global = 0" in note
    assert "does not compute endpoint residuals" in note


def test_v08_control_runner_outputs_materializes_contracts_without_results() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/control_runner_outputs_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/control_runner_outputs_summary_v08.csv").open()))
    note = (ROOT / "docs/control_runner_outputs_v08.md").read_text()

    assert len(rows) == 6
    assert [row["control_output_id"] for row in rows] == [f"CRO08_{idx:03d}" for idx in range(1, 7)]
    assert {row["output_contract_status"] for row in rows} == {"OUTPUT_CONTRACT_READY_NOT_RUN"}
    assert all(row["source_execution_status"] == "RUNNER_CONTRACT_DECLARED_NOT_IMPLEMENTED" for row in rows)
    assert all(row["control_result_rows_written"] == "0" for row in rows)
    assert all(row["control_scores_written"] == "0" for row in rows)
    assert all(row["control_pass_claim_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "numeric_decision_thresholds_v08.csv" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "CONTROL_RUNNER_OUTPUTS_V08",
            "control_output_artifact": "control_runner_outputs_v08",
            "runner_contract_rows_checked": "6",
            "output_contract_rows_written": "6",
            "control_result_rows_written": "0",
            "control_scores_written": "0",
            "control_pass_claim_allowed_anywhere": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "CONTROL_RUNNER_OUTPUTS_V08_READY_FOR_DECISION_THRESHOLDS",
            "next_required_artifact": "numeric_decision_thresholds_v08.csv",
            "claim_boundary": "control_runner_outputs_v08_contract_only_no_control_results_no_scores_no_verdict",
        }
    ]
    assert "writes no control result rows" in note
    assert "makes no dark-sector verdict" in note


def test_v09_control_execution_readiness_allows_score_calculation_preflight_not_verdict() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/control_execution_readiness_v09.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/control_execution_readiness_summary_v09.csv").open()))
    note = (ROOT / "docs/control_execution_readiness_v09.md").read_text()

    assert len(rows) == 6
    assert {row["score_calculation_preflight_status"] for row in rows} == {
        "READY_FOR_SCORE_CALCULATION_PRECHECK"
    }
    assert {row["verdict_control_status"] for row in rows} == {"BLOCKED_NOT_EXECUTED_NO_PASS_CLAIM"}
    assert {row["control_result_rows_written"] for row in rows} == {"0"}
    assert {row["control_scores_written"] for row in rows} == {"0"}
    assert all(row["control_pass_claim_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["dark_sector_verdict_allowed"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "CONTROL_EXECUTION_READINESS_V09",
            "controls_checked": "6",
            "score_calculation_ready_controls": "6",
            "verdict_ready_controls": "0",
            "control_result_rows_written": "0",
            "control_scores_written": "0",
            "control_pass_claim_allowed_anywhere": "false",
            "score_calculation_preflight_ready": "true",
            "family_verdict_controls_ready": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "dark_sector_verdict_allowed_anywhere": "false",
            "overall_status": "CONTROL_EXECUTION_READINESS_SCORE_CALCULATION_READY_VERDICT_CONTROLS_BLOCKED",
            "next_required_artifact": "endpoint_scoring_runner_v01",
            "claim_boundary": "control_execution_readiness_only_no_control_results_no_scores_no_verdict",
        }
    ]
    assert "score-calculation preflight readiness" in note
    assert "no control pass" in note


def test_v01_endpoint_scoring_runner_writes_raw_m0_diagnostics_without_verdict() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/endpoint_scoring_runner_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/endpoint_scoring_runner_summary_v01.csv").open()))
    note = (ROOT / "docs/endpoint_scoring_runner_v01.md").read_text()

    assert len(rows) == 18
    assert {row["family_id"] for row in rows} == {"M0"}
    assert sum(int(row["radial_points_scored"]) for row in rows) == 450
    assert {row["raw_score_status"] for row in rows} == {"RAW_M0_ADEQUACY_DIAGNOSTIC_WRITTEN_NOT_VERDICT"}
    for row in rows:
        full = float(row["chi2_full_raw"])
        inner = float(row["chi2_inner_raw"])
        outer = float(row["chi2_outer_raw"])
        penalty = float(row["parsimony_penalty_raw"])
        raw_score = float(row["raw_m0_adequacy_diagnostic"])
        assert abs(raw_score - (full + 0.5 * inner + 0.5 * outer + penalty)) < 0.000002
        assert row["family_comparison_allowed"] == "false"
        assert row["control_pass_claim_allowed"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"
        assert row["dark_sector_verdict_allowed"] == "false"

    assert summary == [
        {
            "summary_id": "ENDPOINT_SCORING_RUNNER_V01",
            "scoring_mode": "RAW_M0_ADEQUACY_DIAGNOSTIC_ONLY",
            "preflight_status": "SCORING_PREFLIGHT_REQUIREMENTS_READY_RAW_M0_ADEQUACY_RUNNER_NEXT_VERDICT_BLOCKED",
            "raw_diagnostic_rows_written": "18",
            "radial_points_scored": "450",
            "families_scored": "1",
            "family_comparison_rows_written": "0",
            "control_result_rows_written": "0",
            "endpoint_verdict_scores_written": "0",
            "family_comparison_allowed_anywhere": "false",
            "control_pass_claim_allowed_anywhere": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "dark_sector_verdict_allowed_anywhere": "false",
            "overall_status": "ENDPOINT_SCORING_RUNNER_V01_RAW_M0_ADEQUACY_DIAGNOSTICS_WRITTEN_VERDICT_BLOCKED",
            "next_required_artifact": "control_result_execution_v01.csv",
            "claim_boundary": "endpoint_scoring_runner_v01_raw_m0_adequacy_diagnostic_only_no_family_comparison_no_verdict",
        }
    ]
    assert "raw adequacy diagnostics" in note
    assert "does not compare M0 against M1 or M2" in note


def test_v08_numeric_decision_thresholds_freeze_rules_without_verdicts() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/numeric_decision_thresholds_v08.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/numeric_decision_thresholds_summary_v08.csv").open()))
    note = (ROOT / "docs/numeric_decision_thresholds_v08.md").read_text()

    assert len(rows) == 4
    assert [row["numeric_threshold_id"] for row in rows] == [f"NDT08_{idx:03d}" for idx in range(1, 5)]
    assert {row["verdict_label"] for row in rows} == {"M0_SUFFICIENT", "M1_FAVORED", "M2_BENCHMARK_STRONGER", "UNRESOLVED"}
    assert {row["numeric_threshold_status"] for row in rows} == {"NUMERIC_THRESHOLD_FROZEN_NOT_EVALUATED"}
    assert {row["minimum_heldout_margin"] for row in rows} == {"0"}
    assert {row["maximum_control_failures"] for row in rows} == {"0"}
    assert all(row["stability_required"] == "true" for row in rows)
    assert {row["rank_required"] for row in rows if row["verdict_label"] != "UNRESOLVED"} == {"1"}
    assert [row["rank_required"] for row in rows if row["verdict_label"] == "UNRESOLVED"] == ["0"]
    assert [row["unresolved_fallback_allowed"] for row in rows if row["verdict_label"] == "UNRESOLVED"] == ["true"]
    assert all(row["next_required_artifact"] == "scoring_preflight_v07.csv" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "NUMERIC_DECISION_THRESHOLDS_V08",
            "threshold_artifact": "numeric_decision_thresholds_v08",
            "source_threshold_rows_checked": "4",
            "numeric_threshold_rows_written": "4",
            "endpoint_scores_written": "0",
            "verdicts_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "NUMERIC_DECISION_THRESHOLDS_V08_READY_FOR_SCORING_PREFLIGHT",
            "next_required_artifact": "scoring_preflight_v07.csv",
            "claim_boundary": "numeric_decision_thresholds_v08_threshold_freeze_only_no_scores_no_verdict",
        }
    ]
    assert "minimum_heldout_margin = 0" in note
    assert "writes no verdict labels" in note


def test_v10_m0_global_parameter_inventory_exposes_slots_without_counts() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_global_parameter_inventory_v10.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_global_parameter_inventory_summary_v10.csv").open()))
    note = (ROOT / "docs/m0_global_parameter_inventory_v10.md").read_text()

    assert len(rows) == 6
    assert [row["inventory_row_id"] for row in rows] == [f"M0GPI10_{idx:03d}" for idx in range(1, 7)]
    assert {row["readiness_id"] for row in rows} == {"NCR05_M0_GLOBAL"}
    assert {row["family_id"] for row in rows} == {"M0"}
    assert {row["inventory_scope"] for row in rows} == {"global_formula_parameters"}
    assert {row["countability_status"] for row in rows} == {"COUNTABILITY_CLASSIFICATION_PENDING"}
    assert all(row["count_value_written"] == "0" for row in rows)
    assert all(row["numeric_value_written"] == "0" for row in rows)
    assert all(row["per_galaxy_privilege_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_global_parameter_count_classification_v11.csv"}
    assert "readout_operator" in {row["global_slot_name"] for row in rows}
    assert "no_dark_constraint" in {row["global_slot_name"] for row in rows}
    assert summary == [
        {
            "summary_id": "M0_GLOBAL_PARAMETER_INVENTORY_V10",
            "inventory_artifact": "m0_global_parameter_inventory_v10",
            "readiness_id": "NCR05_M0_GLOBAL",
            "family_id": "M0",
            "inventory_rows": "6",
            "inventory_rows_present": "6",
            "countability_classified_rows": "0",
            "numeric_count_values_written": "0",
            "numeric_values_written": "0",
            "per_galaxy_privilege_values_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_GLOBAL_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING",
            "next_required_artifact": "m0_global_parameter_count_classification_v11.csv",
            "claim_boundary": "m0_global_parameter_inventory_only_no_counts_no_values_no_scores",
        }
    ]
    assert "writes no final numeric parameter count" in note
    assert "m0_global_parameter_count_classification_v11.csv" in note


def test_v11_m0_global_parameter_count_classification_without_numeric_counts() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_global_parameter_count_classification_v11.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_global_parameter_count_classification_summary_v11.csv").open()))
    note = (ROOT / "docs/m0_global_parameter_count_classification_v11.md").read_text()

    assert len(rows) == 6
    assert [row["classification_row_id"] for row in rows] == [f"M0GPCC11_{idx:03d}" for idx in range(1, 7)]
    assert {row["readiness_id"] for row in rows} == {"NCR05_M0_GLOBAL"}
    assert {row["family_id"] for row in rows} == {"M0"}
    assert {row["classification_status"] for row in rows} == {"CLASSIFIED_COUNT_VALUE_PENDING"}
    assert all(row["numeric_count_value_written"] == "0" for row in rows)
    assert all(row["numeric_value_written"] == "0" for row in rows)
    assert all(row["per_galaxy_privilege_value_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["next_required_artifact"] for row in rows} == {"m0_global_parameter_count_value_ledger_v12.csv"}
    classes = {row["global_slot_name"]: row["countability_class"] for row in rows}
    assert classes["no_dark_constraint"] == "FIXED_FAMILY_GUARD_DISQUALIFIES_IF_COMPENSATOR"
    assert classes["readout_operator"] == "COUNT_IF_ADJUSTABLE_READOUT_OPERATOR_PARAMETER"
    assert classes["assembly"] == "AGGREGATE_AUDIT_ROW_CHILD_SLOTS_COUNT"
    assert summary == [
        {
            "summary_id": "M0_GLOBAL_PARAMETER_COUNT_CLASSIFICATION_V11",
            "classification_artifact": "m0_global_parameter_count_classification_v11",
            "inventory_status": "M0_GLOBAL_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING",
            "classification_rows": "6",
            "classified_rows": "6",
            "fixed_or_neutral_classes": "1",
            "count_if_adjustable_classes": "4",
            "disqualifying_classes": "1",
            "numeric_count_values_written": "0",
            "numeric_values_written": "0",
            "per_galaxy_privilege_values_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_GLOBAL_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING",
            "next_required_artifact": "m0_global_parameter_count_value_ledger_v12.csv",
            "claim_boundary": "m0_global_parameter_count_classification_only_no_numeric_counts_no_scores",
        }
    ]
    assert "writes no final numeric parameter count" in note
    assert "m0_global_parameter_count_value_ledger_v12.csv" in note


def test_v12_m0_global_parameter_count_value_ledger_keeps_final_count_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_global_parameter_count_value_ledger_v12.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_global_parameter_count_value_ledger_summary_v12.csv").open()))
    note = (ROOT / "docs/m0_global_parameter_count_value_ledger_v12.md").read_text()

    assert len(rows) == 6
    assert [row["ledger_row_id"] for row in rows] == [f"M0GPCVL12_{idx:03d}" for idx in range(1, 7)]
    assert {row["readiness_id"] for row in rows} == {"NCR05_M0_GLOBAL"}
    assert {row["family_id"] for row in rows} == {"M0"}
    assert sum(row["slot_count_value"] == "0" for row in rows) == 2
    assert sum(row["resolution_needed"] == "true" for row in rows) == 4
    assert all(row["final_m0_global_count_input_allowed"] == "false" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    values = {row["global_slot_name"]: row["slot_count_value"] for row in rows}
    assert values["no_dark_constraint"] == "0"
    assert values["assembly"] == "0"
    assert values["readout_operator"] == "VALUE_PENDING_ADJUSTABLE_SLOT_RESOLUTION"
    assert summary == [
        {
            "summary_id": "M0_GLOBAL_PARAMETER_COUNT_VALUE_LEDGER_V12",
            "ledger_artifact": "m0_global_parameter_count_value_ledger_v12",
            "classification_status": "M0_GLOBAL_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING",
            "ledger_rows": "6",
            "resolved_zero_rows": "2",
            "conditional_pending_rows": "4",
            "disqualifying_guard_rows": "1",
            "numeric_slot_count_values_written": "2",
            "final_m0_global_count_written": "false",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_GLOBAL_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
            "next_required_artifact": "m0_global_adjustable_slot_resolution_v13.csv",
            "claim_boundary": "m0_global_parameter_count_value_ledger_only_no_final_k_no_parsimony_no_scores",
        }
    ]
    assert "does not write the final M0 global parameter count" in note
    assert "m0_global_adjustable_slot_resolution_v13.csv" in note


def test_v13_m0_global_adjustable_slot_resolution_prepares_final_count_candidate() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_global_adjustable_slot_resolution_v13.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_global_adjustable_slot_resolution_summary_v13.csv").open()))
    note = (ROOT / "docs/m0_global_adjustable_slot_resolution_v13.md").read_text()

    assert len(rows) == 4
    assert [row["resolution_row_id"] for row in rows] == [f"M0GASR13_{idx:03d}" for idx in range(1, 5)]
    assert {row["global_slot_name"] for row in rows} == {
        "source_state",
        "baryonic_input",
        "readout_operator",
        "failure_route",
    }
    assert all(row["prior_count_value_status"] == "CONDITIONAL_COUNT_VALUE_PENDING" for row in rows)
    assert all(row["slot_resolution_status"] == "RESOLVED_ZERO_FIXED_SOURCE_SIDE_OR_GUARD" for row in rows)
    assert all(row["slot_count_value"] == "0" for row in rows)
    assert all(row["adjustable_privilege_found"] == "false" for row in rows)
    assert all(row["final_count_candidate_input_allowed"] == "true" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert any("M0NDRE08_PARAMETERS" in row["resolution_evidence"] for row in rows)
    assert any("M0NDFP07_FAILURE_REPORTING_ROUTE" in row["resolution_evidence"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION_V13",
            "resolution_artifact": "m0_global_adjustable_slot_resolution_v13",
            "ledger_status": "M0_GLOBAL_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
            "conditional_rows_checked": "4",
            "resolved_zero_rows": "4",
            "unresolved_rows": "0",
            "adjustable_privileges_found": "0",
            "final_m0_global_count_candidate_ready": "true",
            "final_m0_global_count_written": "false",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE",
            "next_required_artifact": "m0_global_final_count_candidate_v14.csv",
            "claim_boundary": "m0_global_adjustable_slot_resolution_only_no_final_k_no_parsimony_no_scores",
        }
    ]
    assert "does not write the final M0 global parameter count" in note
    assert "m0_global_final_count_candidate_v14.csv" in note


def test_v14_m0_global_final_count_candidate_ready_for_freeze_only() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_global_final_count_candidate_v14.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_global_final_count_candidate_summary_v14.csv").open()))
    note = (ROOT / "docs/m0_global_final_count_candidate_v14.md").read_text()

    assert rows == [
        {
            "candidate_row_id": "M0GFC14_001",
            "family_id": "M0",
            "count_domain": "global_formula_parameters",
            "input_artifacts": "m0_global_parameter_count_value_ledger_v12.csv;m0_global_adjustable_slot_resolution_v13.csv",
            "slot_count_rows_used": "6",
            "resolved_zero_slot_rows": "6",
            "unresolved_slot_rows": "0",
            "adjustable_privileges_found": "0",
            "candidate_k_m0_global": "0",
            "candidate_status": "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
            "freeze_input_allowed": "true",
            "parsimony_input_allowed": "false",
            "next_required_artifact": "m0_global_final_count_freeze_v15.csv",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_parameter_discount",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "m0_global_final_count_candidate_only_no_freeze_no_parsimony_no_scores",
        }
    ]
    assert summary == [
        {
            "summary_id": "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14",
            "candidate_artifact": "m0_global_final_count_candidate_v14",
            "v12_ledger_status": "M0_GLOBAL_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
            "v13_resolution_status": "M0_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE",
            "slot_count_rows_used": "6",
            "resolved_zero_slot_rows": "6",
            "unresolved_slot_rows": "0",
            "adjustable_privileges_found": "0",
            "candidate_k_m0_global": "0",
            "final_count_frozen": "false",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
            "next_required_artifact": "m0_global_final_count_freeze_v15.csv",
            "claim_boundary": "m0_global_final_count_candidate_only_no_freeze_no_parsimony_no_scores",
        }
    ]
    assert "does not freeze the final M0 global count" in note
    assert "m0_global_final_count_freeze_v15.csv" in note


def test_v15_m0_global_final_count_freeze_hands_off_to_per_galaxy_audit() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_global_final_count_freeze_v15.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_global_final_count_freeze_summary_v15.csv").open()))
    note = (ROOT / "docs/m0_global_final_count_freeze_v15.md").read_text()

    assert rows == [
        {
            "freeze_row_id": "M0GFCF15_001",
            "candidate_row_id": "M0GFC14_001",
            "family_id": "M0",
            "count_domain": "global_formula_parameters",
            "frozen_k_m0_global": "0",
            "freeze_status": "M0_GLOBAL_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_PRIVILEGE_AUDIT_PENDING",
            "candidate_status": "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
            "source_artifacts": "m0_global_parameter_count_value_ledger_v12.csv;m0_global_adjustable_slot_resolution_v13.csv",
            "per_galaxy_count_input_allowed": "true",
            "parsimony_input_allowed": "false",
            "next_required_artifact": "m0_per_galaxy_privilege_count_audit_v10.csv",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_parameter_discount",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "m0_global_final_count_freeze_only_no_per_galaxy_counts_no_parsimony_no_scores",
        }
    ]
    assert summary == [
        {
            "summary_id": "M0_GLOBAL_FINAL_COUNT_FREEZE_V15",
            "freeze_artifact": "m0_global_final_count_freeze_v15",
            "candidate_status": "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
            "frozen_k_m0_global": "0",
            "final_count_frozen": "true",
            "per_galaxy_counts_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_GLOBAL_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_PRIVILEGE_AUDIT_PENDING",
            "next_required_artifact": "m0_per_galaxy_privilege_count_audit_v10.csv",
            "claim_boundary": "m0_global_final_count_freeze_only_no_per_galaxy_counts_no_parsimony_no_scores",
        }
    ]
    assert "k_M0_global = 0" in note
    assert "per-galaxy" in note
    assert "privilege counts" in note


def test_v10_m0_per_galaxy_privilege_count_audit_prepares_freeze_without_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_per_galaxy_privilege_count_audit_v10.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_per_galaxy_privilege_count_audit_summary_v10.csv").open()))
    note = (ROOT / "docs/m0_per_galaxy_privilege_count_audit_v10.md").read_text()

    assert len(rows) == 18
    assert [row["audit_row_id"] for row in rows] == [f"M0PGPCA10_{idx:03d}" for idx in range(1, 19)]
    assert {row["source_activation_status"] for row in rows} == {"ACTIVATION_BLOCKED"}
    assert {row["m0_label_rule_status"] for row in rows} == {"M0_LABEL_RULE_TABLE_READY_SCORING_BLOCKED"}
    assert {row["row_privilege_status"] for row in rows} == {"RESOLVED_ZERO_NO_ROW_SPECIFIC_M0_PRIVILEGE"}
    assert all(row["per_galaxy_privilege_count_value"] == "0" for row in rows)
    assert all(row["freeze_input_allowed"] == "true" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "m0_per_galaxy_privilege_count_freeze_v11.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "M0_PER_GALAXY_PRIVILEGE_COUNT_AUDIT_V10",
            "audit_artifact": "m0_per_galaxy_privilege_count_audit_v10",
            "source_rows_checked": "18",
            "resolved_zero_rows": "18",
            "unresolved_rows": "0",
            "per_galaxy_privilege_values_written": "18",
            "per_galaxy_count_freeze_ready": "true",
            "per_galaxy_count_frozen": "false",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_PER_GALAXY_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE",
            "next_required_artifact": "m0_per_galaxy_privilege_count_freeze_v11.csv",
            "claim_boundary": "m0_per_galaxy_privilege_count_audit_only_no_freeze_no_parsimony_no_scores",
        }
    ]
    assert "RESOLVED_ZERO_NO_ROW_SPECIFIC_M0_PRIVILEGE" in note
    assert "does not\nfreeze the per-galaxy count" in note


def test_v11_m0_per_galaxy_privilege_count_freeze_hands_off_to_m1_global_inventory() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_per_galaxy_privilege_count_freeze_v11.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_per_galaxy_privilege_count_freeze_summary_v11.csv").open()))
    note = (ROOT / "docs/m0_per_galaxy_privilege_count_freeze_v11.md").read_text()

    assert len(rows) == 18
    assert [row["freeze_row_id"] for row in rows] == [f"M0PGPCF11_{idx:03d}" for idx in range(1, 19)]
    assert {row["freeze_status"] for row in rows} == {"M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11_FROZEN"}
    assert {row["audit_status"] for row in rows} == {"RESOLVED_ZERO_NO_ROW_SPECIFIC_M0_PRIVILEGE"}
    assert all(row["frozen_per_galaxy_privilege_count"] == "0" for row in rows)
    assert all(row["parsimony_input_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["next_required_artifact"] == "m1_response_parameter_inventory_v10.csv" for row in rows)
    assert summary == [
        {
            "summary_id": "M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11",
            "freeze_artifact": "m0_per_galaxy_privilege_count_freeze_v11",
            "audit_status": "M0_PER_GALAXY_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE",
            "source_rows_checked": "18",
            "frozen_zero_rows": "18",
            "unresolved_rows": "0",
            "per_galaxy_count_frozen": "true",
            "frozen_per_galaxy_privilege_count_total": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11_READY_M1_GLOBAL_COUNT_PENDING",
            "next_required_artifact": "m1_response_parameter_inventory_v10.csv",
            "claim_boundary": "m0_per_galaxy_privilege_count_freeze_only_no_parsimony_no_scores",
        }
    ]
    assert "All eighteen" in note
    assert "m1_response_parameter_inventory_v10.csv" in note


def test_v09_numeric_count_readiness_closure_decomposes_blockers_without_counts() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/numeric_count_readiness_closure_v09.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/numeric_count_readiness_closure_summary_v09.csv").open()))
    note = (ROOT / "docs/numeric_count_readiness_closure_v09.md").read_text()

    assert len(rows) == 7
    assert [row["closure_row_id"] for row in rows] == [f"NCRC09_{idx:03d}" for idx in range(1, 8)]
    assert {row["family_id"] for row in rows} == {"M0", "M1", "M2", "ALL"}
    assert all(row["source_readiness_status"] == "COUNT_NOT_READY" for row in rows)
    assert rows[0]["closure_decision"] == "COUNT_READINESS_READY"
    assert rows[1]["closure_decision"] == "COUNT_READINESS_READY"
    assert rows[2]["closure_decision"] == "COUNT_READINESS_READY"
    assert rows[3]["closure_decision"] == "COUNT_READINESS_READY"
    assert rows[4]["closure_decision"] == "COUNT_READINESS_READY"
    assert rows[5]["closure_decision"] == "COUNT_READINESS_READY"
    assert rows[6]["closure_decision"] == "COUNT_READINESS_READY"
    assert all(row["numeric_count_values_written"] == "0" for row in rows)
    assert all(row["parsimony_scores_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert rows[0]["readiness_id"] == "NCR05_M0_GLOBAL"
    assert rows[0]["closure_blocker"] == "none"
    assert rows[0]["next_required_artifact"] == "none"
    assert rows[1]["closure_blocker"] == "none"
    assert rows[1]["next_required_artifact"] == "none"
    assert rows[2]["closure_blocker"] == "none"
    assert rows[2]["next_required_artifact"] == "none"
    assert rows[3]["closure_blocker"] == "none"
    assert rows[3]["next_required_artifact"] == "none"
    assert rows[4]["closure_blocker"] == "none"
    assert rows[4]["next_required_artifact"] == "none"
    assert rows[5]["closure_blocker"] == "none"
    assert rows[5]["next_required_artifact"] == "none"
    assert rows[6]["closure_blocker"] == "none"
    assert rows[6]["next_required_artifact"] == "none"
    assert "M0_NO_DARK_FORMULA_TABLE_READY_FOR_PREDICTION_ROWS" in rows[0]["upstream_artifact_status"]
    assert "SOURCE_ROW_AUDIT_SKELETON_PRESENT_NOT_COUNT_READY" in rows[1]["upstream_artifact_status"]
    assert summary == [
        {
            "summary_id": "NUMERIC_COUNT_READINESS_CLOSURE_V09",
            "closure_artifact": "numeric_count_readiness_closure_v09",
            "v08_status": "NUMERIC_PARAMETER_COUNT_TABLE_V08_BLOCKED_ON_FINAL_NUMERIC_COUNT_VALUES",
            "readiness_rows_checked": "7",
            "closure_ready_rows": "7",
            "closure_blocked_rows": "0",
            "numeric_count_values_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "NUMERIC_COUNT_READINESS_CLOSURE_READY_FOR_FINAL_COUNTS",
            "next_required_artifact": "numeric_parameter_count_table_final_values_v10.csv",
            "claim_boundary": "numeric_count_readiness_closure_only_no_counts_no_parsimony_no_scores",
        }
    ]
    assert "numeric_parameter_count_table_final_values_v10.csv" in note
    assert "writes no numeric parameter counts" in note


def test_v81_family_prediction_frontier_trace_narrows_to_final_numeric_parameter_count_artifact() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/family_prediction_frontier_trace_v81.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/family_prediction_frontier_trace_summary_v81.csv").open()))
    assert len(rows) == 7
    assert [row["frontier_layer"] for row in rows] == [
        "family_prediction_table",
        "m0_formula_table",
        "m0_formula_body",
        "m0_readout_equation",
        "m0_equation_kernel",
        "m0_frozen_expression_body",
        "m0_payload_evidence",
    ]
    assert rows[0]["numeric_prediction_rows_written"] == "450"
    assert all(row["numeric_prediction_rows_written"] == "0" for row in rows[1:])
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(row["dark_sector_verdict_allowed"] == "false" for row in rows)
    assert rows[1]["artifact"] == "m0_no_dark_formula_table_v06"
    assert rows[1]["blocking_slot"] == "formula_table_policy"
    assert rows[0]["narrowed_next_artifact"] == "scoring_preflight_v07.csv"
    assert rows[1]["narrowed_next_artifact"] == "family_prediction_tables_v08.csv"
    assert summary == [
        {
            "summary_id": "FAMILY_PREDICTION_FRONTIER_TRACE_V81",
            "trace_artifact": "family_prediction_frontier_trace_v81",
            "trace_steps": "7",
            "payload_side_ready": "true",
            "first_family_prediction_frontier": "family_prediction_tables_v08.csv",
            "first_content_blocker": "scoring_preflight_v07.csv",
            "formula_rows_written": "0",
            "numeric_prediction_rows_written": "450",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FAMILY_PREDICTION_FRONTIER_TRACED_TO_SCORING_PREFLIGHT",
            "next_required_artifact": "scoring_preflight_v07.csv",
            "claim_boundary": "family_prediction_frontier_trace_only_no_formula_no_predictions_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v07_m0_no_dark_coefficient_policy_closes_without_values_or_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_coefficient_policy_v07.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_coefficient_policy_summary_v07.csv").open()))
    note = (ROOT / "docs/m0_no_dark_coefficient_policy_v07.md").read_text()

    assert len(rows) == 6
    assert {row["policy_status"] for row in rows} == {"READY"}
    assert all(row["numeric_values_written"] == "0" for row in rows)
    assert all(row["prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert any(row["policy_id"] == "M0NDCP07_NO_DARK_EXCLUSION" for row in rows)
    assert any(row["policy_id"] == "M0NDCP07_READOUT_OPERATOR_SHAPE" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert all("posthoc_shape_selection" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_COEFFICIENT_POLICY_V07",
            "source_artifact": "m0_no_dark_expression_coefficient_freeze_v12",
            "policy_rows": "6",
            "ready_policy_rows": "6",
            "blocked_policy_rows": "0",
            "numeric_values_written": "0",
            "prediction_rows_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_COEFFICIENT_POLICY_READY",
            "next_required_artifact": "m0_no_dark_scale_policy_v07",
            "claim_boundary": "m0_no_dark_coefficient_policy_only_no_values_no_predictions_no_scores_no_dark_sector_verdict",
        }
    ]
    assert "level/amplitude support != shape/readout support" in note
    assert "does not assign numeric coefficient values" in note


def test_v07_m0_no_dark_scale_policy_closes_without_values_or_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_scale_policy_v07.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_scale_policy_summary_v07.csv").open()))
    note = (ROOT / "docs/m0_no_dark_scale_policy_v07.md").read_text()

    assert len(rows) == 6
    assert {row["policy_status"] for row in rows} == {"READY"}
    assert all(row["numeric_scale_values_written"] == "0" for row in rows)
    assert all(row["prediction_rows_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert any(row["scale_policy_id"] == "M0NDSP07_RADIAL_DOMAIN" for row in rows)
    assert any(row["scale_policy_id"] == "M0NDSP07_FALLBACK_HANDOFF" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert all("posthoc_scale_selection" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_SCALE_POLICY_V07",
            "source_artifact": "m0_no_dark_coefficient_policy_v07",
            "policy_rows": "6",
            "ready_policy_rows": "6",
            "blocked_policy_rows": "0",
            "numeric_scale_values_written": "0",
            "prediction_rows_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_SCALE_POLICY_READY",
            "next_required_artifact": "m0_no_dark_fallback_policy_v07",
            "claim_boundary": "m0_no_dark_scale_policy_only_no_values_no_predictions_no_scores_no_dark_sector_verdict",
        }
    ]
    assert "scale choice != residual-window rescue" in note
    assert "does not assign numeric scale values" in note


def test_v07_m0_no_dark_fallback_policy_closes_without_predictions_or_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_fallback_policy_v07.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/m0_no_dark_fallback_policy_summary_v07.csv").open()))
    note = (ROOT / "docs/m0_no_dark_fallback_policy_v07.md").read_text()

    assert len(rows) == 6
    assert {row["policy_status"] for row in rows} == {"READY"}
    assert all(row["fallback_prediction_rows_written"] == "0" for row in rows)
    assert all(row["numeric_predictions_written"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert any(row["fallback_policy_id"] == "M0NDFP07_ZERO_RESPONSE_ROUTE" for row in rows)
    assert any(row["fallback_policy_id"] == "M0NDFP07_PREDICTION_TABLE_HANDOFF" for row in rows)
    assert all("endpoint_residual" in row["forbidden_inputs"] for row in rows)
    assert all("posthoc_exception" in row["forbidden_inputs"] for row in rows)
    assert summary == [
        {
            "summary_id": "M0_NO_DARK_FALLBACK_POLICY_V07",
            "source_artifact": "m0_no_dark_scale_policy_v07",
            "policy_rows": "6",
            "ready_policy_rows": "6",
            "blocked_policy_rows": "0",
            "fallback_prediction_rows_written": "0",
            "numeric_predictions_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FALLBACK_POLICY_READY",
            "next_required_artifact": "family_prediction_tables_v08.csv",
            "claim_boundary": "m0_no_dark_fallback_policy_only_no_predictions_no_scores_no_dark_sector_verdict",
        }
    ]
    assert "fallback route != fitted rescue" in note
    assert "does not write fallback velocity predictions" in note


def test_v14_source_import_template_is_not_data() -> None:
    template = list(csv.DictReader((ROOT / "data/input/source_import_real_values_v12_TEMPLATE.csv").open()))
    assert len(template) == 18
    assert all(row["import_status"] == "TEMPLATE_ROW_DO_NOT_IMPORT" for row in template)
    assert all(row["v_obs_km_s"] == "FILL_NUMERIC_OBSERVED_VELOCITY" for row in template)

    columns = list(csv.DictReader((ROOT / "data/derived/source_import_template_columns_v14.csv").open()))
    assert len(columns) == 16
    assert {"galaxy_id", "radius_kpc", "v_obs_km_s", "import_status"}.issubset(
        {row["field_name"] for row in columns}
    )
    assert all(row["endpoint_scoring_allowed"] == "false" for row in columns)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_template_summary_v14.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_TEMPLATE_V14",
            "template_file": "data/input/source_import_real_values_v12_TEMPLATE.csv",
            "target_real_input_file": "data/input/source_import_real_values_v12.csv",
            "template_rows": "18",
            "required_columns": "16",
            "real_input_file_present": "true",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_TEMPLATE_READY_NOT_DATA",
            "claim_boundary": "template_only_no_source_import_no_scores",
        }
    ]


def test_v15_raw_adapter_validates_raw_input_without_writing_v12() -> None:
    schema = list(csv.DictReader((ROOT / "data/derived/source_import_raw_adapter_schema_v15.csv").open()))
    assert len(schema) == 16
    assert {"galaxy_id", "radius_kpc", "v_obs_km_s", "import_status"}.issubset(
        {row["target_field_name"] for row in schema}
    )
    assert all(row["endpoint_scoring_allowed"] == "false" for row in schema)

    gate = list(csv.DictReader((ROOT / "data/derived/source_import_raw_adapter_gate_v15.csv").open()))
    assert gate == [
        {
            "adapter_gate_id": "SIRA15_RAW_TO_V12",
            "raw_input_file": "data/input/source_import_raw_sparc_like_v15.csv",
            "target_input_file": "data/input/source_import_real_values_v12.csv",
            "raw_input_status": "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW",
            "raw_rows_seen": "450",
            "valid_raw_rows": "450",
            "galaxies_with_valid_raw_rows": "18",
            "target_file_written": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "raw_adapter_gate_only_no_source_import_no_scores",
        }
    ]

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_raw_adapter_summary_v15.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_RAW_ADAPTER_V15",
            "raw_input_file": "data/input/source_import_raw_sparc_like_v15.csv",
            "target_input_file": "data/input/source_import_real_values_v12.csv",
            "raw_input_status": "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW",
            "target_input_file_present": "true",
            "target_file_written_by_adapter": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "RAW_ADAPTER_READY_VALIDATION_PENDING_REVIEW",
            "claim_boundary": "raw_adapter_only_no_source_import_no_scores",
        }
    ]


def test_v56_active_raw_sparc_like_writer_outputs_frozen_rows() -> None:
    rows = list(csv.DictReader((ROOT / "data/input/source_import_raw_sparc_like_v15.csv").open()))
    assert len(rows) == 450
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert all(row["catalog"] == "SPARC" for row in rows)
    assert all(row["table_or_file"] == "MassModels_Lelli2016c.mrt" for row in rows)
    assert all(row["sha256_or_external_accession"].startswith("sha256:") for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/active_v15_raw_sparc_like_input_writer_summary_v56.csv").open()))
    assert summary == [
        {
            "summary_id": "ACTIVE_V15_RAW_SPARC_LIKE_INPUT_WRITER_V56",
            "source_file": "data/external/sparc_hash_audit_v50/MassModels_Lelli2016c.mrt",
            "target_raw_input": "data/input/source_import_raw_sparc_like_v15.csv",
            "raw_rows_written": "450",
            "galaxies_written": "18",
            "target_file_written": "true",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "ACTIVE_V15_RAW_SPARC_LIKE_INPUT_WRITTEN",
            "claim_boundary": "active_v15_raw_input_writer_only_no_v12_write_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v57_active_v12_real_values_write_authorization_grants_write_without_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/input/source_import_real_values_write_authorization_v57.csv").open()))
    assert rows == [
        {
            "authorization_id": "ARV57_WRITE_REAL_VALUES_FROM_V15_RAW",
            "source_raw_adapter_summary": "data/derived/source_import_raw_adapter_summary_v15.csv",
            "target_input_file": "data/input/source_import_real_values_v12.csv",
            "raw_input_status": "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW",
            "raw_input_review_status": "RAW_INPUT_REVIEW_ACCEPTED_FOR_V12_WRITE",
            "write_authorization": "AUTHORIZE_V12_WRITE_FROM_ACTIVE_V15_RAW",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "active_v12_write_authorization_only_no_leakage_pass_no_scores_no_dark_sector_verdict",
        }
    ]

    summary = list(csv.DictReader((ROOT / "data/derived/active_v12_real_values_write_authorization_summary_v57.csv").open()))
    assert summary == [
        {
            "summary_id": "ACTIVE_V12_REAL_VALUES_WRITE_AUTHORIZATION_V57",
            "authorization_file": "data/input/source_import_real_values_write_authorization_v57.csv",
            "target_input_file": "data/input/source_import_real_values_v12.csv",
            "raw_input_status": "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW",
            "write_authorized": "true",
            "target_file_written": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "ACTIVE_V12_WRITE_AUTHORIZATION_GRANTED",
            "claim_boundary": "active_v12_write_authorization_only_no_v12_write_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v16_write_authorization_allows_target_input_creation_without_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/source_import_write_authorization_v16.csv").open()))
    assert len(rows) == 1
    row = rows[0]
    assert row["authorization_id"] == "SIWA16_WRITE_V12"
    assert row["authorization_file"] == "data/input/source_import_real_values_write_authorization_v57.csv"
    assert row["explicit_write_authorization"] == "true"
    assert row["raw_input_status"] == "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW"
    assert row["write_authorized"] == "true"
    assert row["write_blockers"] == "none"
    assert row["target_file_written"] == "false"
    assert row["endpoint_scoring_allowed"] == "false"

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_write_authorization_summary_v16.csv").open()))
    assert len(summary) == 1
    summary_row = summary[0]
    assert summary_row["write_authorized"] == "true"
    assert summary_row["target_file_written"] == "false"
    assert summary_row["endpoint_scoring_allowed_anywhere"] == "false"
    assert summary_row["overall_status"] == "WRITE_AUTHORIZATION_READY"
    assert summary_row["next_required_artifact"] == "data/input/source_import_real_values_v12.csv"
    assert summary_row["claim_boundary"] == "write_authorization_only_no_source_import_no_scores"


def test_v17_authorized_writer_writes_real_values_without_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/source_import_authorized_writer_v17.csv").open()))
    assert len(rows) == 1
    row = rows[0]
    assert row["writer_id"] == "SIAW17_AUTHORIZED_RAW_TO_V12"
    assert row["write_authorized"] == "true"
    assert row["raw_input_present"] == "true"
    assert row["target_file_written"] == "true"
    assert row["rows_written"] == "450"
    assert row["writer_status"] == "TARGET_INPUT_WRITTEN_FROM_AUTHORIZED_RAW"
    assert row["endpoint_scoring_allowed"] == "false"

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_authorized_writer_summary_v17.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_AUTHORIZED_WRITER_V17",
            "writer_status": "TARGET_INPUT_WRITTEN_FROM_AUTHORIZED_RAW",
            "target_file_written": "true",
            "rows_written": "450",
            "target_input_file_present_after_writer": "true",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "AUTHORIZED_WRITER_WROTE_TARGET_INPUT",
            "next_required_artifact": "data/input/source_import_real_values_v12.csv",
            "claim_boundary": "authorized_writer_only_no_source_import_no_scores",
        }
    ]


def test_v18_raw_template_is_not_data() -> None:
    template = list(csv.DictReader((ROOT / "data/input/source_import_raw_sparc_like_v15_TEMPLATE.csv").open()))
    assert len(template) == 18
    assert all(row["v_obs_km_s"] == "FILL_NUMERIC_OBSERVED_VELOCITY" for row in template)
    assert all(row["radial_index"] == "FILL_INTEGER_INDEX_REPEAT_FOR_EACH_RADIAL_POINT" for row in template)

    columns = list(csv.DictReader((ROOT / "data/derived/source_import_raw_template_columns_v18.csv").open()))
    assert len(columns) == 15
    assert {"galaxy_id", "radius_kpc", "v_obs_km_s", "source_route"}.issubset(
        {row["raw_field_name"] for row in columns}
    )
    assert all(row["endpoint_scoring_allowed"] == "false" for row in columns)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_raw_template_summary_v18.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_RAW_TEMPLATE_V18",
            "template_file": "data/input/source_import_raw_sparc_like_v15_TEMPLATE.csv",
            "target_raw_input_file": "data/input/source_import_raw_sparc_like_v15.csv",
            "template_rows": "18",
            "required_columns": "15",
            "raw_input_file_present": "true",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "RAW_TEMPLATE_READY_NOT_DATA",
            "claim_boundary": "raw_template_only_no_source_import_no_scores",
        }
    ]


def test_v19_source_import_provenance_is_required_but_unfilled() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_manifest_v19.csv").open()))
    assert len(rows) == 18
    assert all(row["catalog_status"] == "PROVENANCE_REQUIRED_NOT_FILLED" for row in rows)
    assert all(row["hash_or_accession_status"] == "PROVENANCE_REQUIRED_NOT_FILLED" for row in rows)
    assert all(row["raw_import_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    columns = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_columns_v19.csv").open()))
    assert {row["field_name"] for row in columns} == {
        "catalog",
        "table_or_file",
        "version_or_date",
        "row_id",
        "sha256_or_external_accession",
        "source_route",
        "leakage_evidence_id",
    }
    assert all(row["required_before_raw_import"] == "true" for row in columns)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_summary_v19.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_V19",
            "candidate_rows": "18",
            "provenance_complete_rows": "0",
            "raw_import_allowed_rows": "0",
            "required_provenance_fields": "7",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PROVENANCE_REQUIRED_NOT_FILLED",
            "next_required_artifact": "data/input/source_import_raw_sparc_like_v15.csv",
            "claim_boundary": "provenance_manifest_only_no_source_import_no_scores",
        }
    ]


def test_v20_source_import_provenance_audit_allows_raw_import_after_active_v21() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_audit_v20.csv").open()))
    assert len(rows) == 18
    assert all(row["provenance_complete"] == "true" for row in rows)
    assert all(row["raw_import_decision"] == "ALLOW_RAW_IMPORT" for row in rows)
    assert all(row["blocking_requirements"] == "none" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_audit_summary_v20.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_AUDIT_V20",
            "audited_rows": "18",
            "provenance_complete_rows": "18",
            "raw_import_allowed_rows": "18",
            "raw_import_blocked_rows": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "RAW_IMPORT_READY_BY_PROVENANCE",
            "next_required_artifact": "data/input/source_import_raw_sparc_like_v15.csv",
            "claim_boundary": "provenance_audit_only_no_source_import_no_scores",
        }
    ]


def test_v21_source_import_provenance_template_is_not_evidence() -> None:
    template = list(csv.DictReader((ROOT / "data/input/source_import_provenance_evidence_v21_TEMPLATE.csv").open()))
    assert len(template) == 18
    assert all(row["provenance_evidence_status"] == "TEMPLATE_ROW_DO_NOT_IMPORT" for row in template)
    assert all(row["catalog"] == "FILL_SOURCE_CATALOG" for row in template)

    columns = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_template_columns_v21.csv").open()))
    assert {row["field_name"] for row in columns} == {
        "galaxy_id",
        "catalog",
        "table_or_file",
        "version_or_date",
        "row_id",
        "sha256_or_external_accession",
        "source_route",
        "leakage_evidence_id",
        "provenance_evidence_status",
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in columns)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_template_summary_v21.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_TEMPLATE_V21",
            "template_file": "data/input/source_import_provenance_evidence_v21_TEMPLATE.csv",
            "target_evidence_file": "data/input/source_import_provenance_evidence_v21.csv",
            "template_rows": "18",
            "required_columns": "9",
            "evidence_input_file_present": "true",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PROVENANCE_TEMPLATE_READY_NOT_DATA",
            "claim_boundary": "provenance_template_only_no_source_import_no_scores",
        }
    ]


def test_v22_source_import_provenance_evidence_gate_allows_promotion() -> None:
    gate = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_evidence_gate_v22.csv").open()))
    assert gate == [
        {
            "evidence_gate_id": "SIPEG22_EVIDENCE_TO_PROVENANCE",
            "evidence_input_file": "data/input/source_import_provenance_evidence_v21.csv",
            "provenance_manifest": "data/derived/source_import_provenance_manifest_v19.csv",
            "evidence_input_status": "EVIDENCE_INPUT_PRESENT_VALIDATION_PENDING_REVIEW",
            "evidence_rows_seen": "18",
            "valid_evidence_rows": "18",
            "galaxies_with_valid_evidence": "18",
            "provenance_promotion_allowed": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "provenance_evidence_gate_only_no_promotion_no_scores",
        }
    ]

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_evidence_gate_summary_v22.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_EVIDENCE_GATE_V22",
            "evidence_input_status": "EVIDENCE_INPUT_PRESENT_VALIDATION_PENDING_REVIEW",
            "evidence_rows_seen": "18",
            "valid_evidence_rows": "18",
            "galaxies_with_valid_evidence": "18",
            "provenance_promotion_allowed": "true",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PROVENANCE_EVIDENCE_READY_FOR_PROMOTION",
            "next_required_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "claim_boundary": "provenance_evidence_gate_only_no_source_import_no_scores",
        }
    ]


def test_v23_source_import_provenance_promotion_gate_allows_raw_import() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_promotion_gate_v23.csv").open()))
    assert len(rows) == 18
    assert all(row["v22_provenance_promotion_allowed"] == "true" for row in rows)
    assert all(row["promotion_allowed"] == "true" for row in rows)
    assert all(row["promotion_decision"] == "PROMOTE_PROVENANCE" for row in rows)
    assert all(row["promotion_blockers"] == "none" for row in rows)
    assert all(row["provenance_rows_promoted"] == "1" for row in rows)
    assert all(row["raw_import_allowed_after_promotion"] == "true" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_promotion_summary_v23.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_PROMOTION_GATE_V23",
            "candidate_rows": "18",
            "promotion_allowed_rows": "18",
            "promotion_blocked_rows": "0",
            "provenance_rows_promoted": "18",
            "raw_import_allowed_rows_after_promotion": "18",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PROVENANCE_PROMOTION_READY_NOT_IMPORTED",
            "next_required_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "claim_boundary": "provenance_promotion_gate_only_no_source_import_no_scores",
        }
    ]


def test_v24_scoring_dependency_closure_blocks_all_score_dependencies() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/scoring_dependency_closure_v24.csv").open()))
    assert len(rows) == 13
    assert {row["dependency_id"] for row in rows} == {
        "SCD24_PROVENANCE_EVIDENCE",
        "SCD24_PROVENANCE_PROMOTION",
        "SCD24_PROVENANCE_AUDIT",
        "SCD24_RAW_ADAPTER_INPUT",
        "SCD24_WRITE_AUTHORIZATION",
        "SCD24_AUTHORIZED_WRITER",
        "SCD24_REAL_VALUES",
        "SCD24_LEAKAGE_AUDIT",
        "SCD24_ROW_ACTIVATION",
        "SCD24_FAMILY_FORMULA_TABLES",
        "SCD24_PARAMETER_COUNTS",
        "SCD24_CONTROL_RUNNERS",
        "SCD24_DECISION_THRESHOLDS",
    }
    ready_ids = {row["dependency_id"] for row in rows if row["dependency_decision"] == "READY"}
    assert ready_ids == {
        "SCD24_PROVENANCE_EVIDENCE",
        "SCD24_PROVENANCE_PROMOTION",
        "SCD24_PROVENANCE_AUDIT",
        "SCD24_RAW_ADAPTER_INPUT",
        "SCD24_WRITE_AUTHORIZATION",
        "SCD24_AUTHORIZED_WRITER",
        "SCD24_REAL_VALUES",
        "SCD24_LEAKAGE_AUDIT",
            "SCD24_ROW_ACTIVATION",
            "SCD24_FAMILY_FORMULA_TABLES",
            "SCD24_PARAMETER_COUNTS",
            "SCD24_CONTROL_RUNNERS",
            "SCD24_DECISION_THRESHOLDS",
        }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert any(row["upstream_status"] == "PROVENANCE_PROMOTION_READY_NOT_IMPORTED" for row in rows)
    assert any(row["upstream_status"] == "SCORING_ACTIVATION_READY_GLOBAL_PREREQUISITES_READY" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/scoring_dependency_closure_summary_v24.csv").open()))
    assert summary == [
        {
            "summary_id": "SCORING_DEPENDENCY_CLOSURE_V24",
            "dependencies_checked": "13",
            "ready_dependencies": "13",
            "blocked_dependencies": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_DEPENDENCY_CLOSURE_READY",
            "next_required_artifact": "none",
            "claim_boundary": "scoring_dependency_closure_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v25_scoring_unblock_priority_identifies_first_frontier() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/scoring_unblock_priority_v25.csv").open()))
    assert len(rows) == 13
    assert [row["priority_rank"] for row in rows] == [str(i) for i in range(1, 14)]
    ready_ids = {row["dependency_id"] for row in rows if row["dependency_decision"] == "READY"}
    assert ready_ids == {
        "SCD24_PROVENANCE_EVIDENCE",
        "SCD24_PROVENANCE_PROMOTION",
        "SCD24_PROVENANCE_AUDIT",
        "SCD24_RAW_ADAPTER_INPUT",
        "SCD24_WRITE_AUTHORIZATION",
        "SCD24_AUTHORIZED_WRITER",
        "SCD24_REAL_VALUES",
        "SCD24_LEAKAGE_AUDIT",
            "SCD24_ROW_ACTIVATION",
            "SCD24_FAMILY_FORMULA_TABLES",
            "SCD24_PARAMETER_COUNTS",
            "SCD24_CONTROL_RUNNERS",
            "SCD24_DECISION_THRESHOLDS",
        }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    frontier = [row for row in rows if row["frontier_now"] == "true"]
    assert frontier == []

    summary = list(csv.DictReader((ROOT / "data/derived/scoring_unblock_priority_summary_v25.csv").open()))
    assert summary == [
        {
            "summary_id": "SCORING_UNBLOCK_PRIORITY_V25",
            "priority_rows": "13",
            "blocked_priority_rows": "0",
            "frontier_now_rows": "0",
            "first_frontier_dependency": "none",
            "first_frontier_artifact": "none",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_UNBLOCK_FRONTIER_CLEAR",
            "claim_boundary": "scoring_unblock_priority_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v72_scoring_frontier_status_targets_completed_v71_response_not_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/scoring_frontier_status_v72.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/scoring_frontier_status_summary_v72.csv").open()))
    assert len(rows) == 3
    assert [row["frontier_id"] for row in rows] == [
        "SFS72_LEAKAGE_PARTIAL_SUFFICIENCY_RESPONSE",
        "SFS72_FULL_LEAKAGE_EVIDENCE_INGESTION",
        "SFS72_SCORING_ACTIVATION_RECHECK",
    ]
    assert all(row["required_before_scoring"] == "true" for row in rows)
    assert all(row["target_evidence_rows_created"] == "0" for row in rows)
    assert all(row["leakage_pass_authorized"] == "false" for row in rows)
    assert all(row["activation_rows_authorized"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert rows[0]["current_status"] == "PARTIAL_SUFFICIENCY_REVIEW_READY_FOR_LATER_LEAKAGE_EVIDENCE_GATE"
    assert "36 partial rows are preaudit review-ready" in rows[0]["ready_detail"]
    assert rows[0]["next_required_artifact"] == "full_leakage_evidence_ingestion_gate_after_accepted_v71_response"
    assert rows[1]["current_status"] == "LEAKAGE_AUDIT_PASS_REVIEWED_ACTIVATION_PENDING"
    assert rows[1]["next_required_artifact"] == "scoring_preflight_v07.csv"
    assert rows[2]["current_status"] == "FAMILY_PREDICTION_TABLE_CONTRACT_READY_PARAMETER_COUNTS_BLOCKED"
    assert rows[2]["next_required_artifact"] == "scoring_preflight_v07.csv"
    assert summary == [
        {
            "summary_id": "SCORING_FRONTIER_STATUS_V72",
            "frontier_rows": "3",
            "blocked_frontier_rows": "3",
            "first_frontier_id": "SFS72_LEAKAGE_PARTIAL_SUFFICIENCY_RESPONSE",
            "first_frontier_artifact": "scoring_preflight_v07.csv",
            "required_components_for_full_scoring_leakage_pass": "4",
            "partial_candidate_rows_requiring_review": "0",
            "target_evidence_rows_created": "0",
            "leakage_pass_authorized": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_FRONTIER_BLOCKED_ON_SCORING_PREFLIGHT",
            "claim_boundary": "scoring_frontier_status_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v26_frontier_provenance_evidence_acceptance_is_review_ready() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_acceptance_v26.csv").open()))
    assert len(rows) == 18
    assert all(row["frontier_dependency"] == "SCD24_PROVENANCE_EVIDENCE" for row in rows)
    assert all(row["frontier_artifact"] == "data/input/source_import_provenance_evidence_v21.csv" for row in rows)
    assert all(row["evidence_input_present"] == "true" for row in rows)
    assert all(row["missing_or_placeholder_fields"] == "none" for row in rows)
    assert all(row["acceptance_status"] == "ACCEPTED_FOR_REVIEW" for row in rows)
    assert all(row["accepted_for_promotion_review"] == "true" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_acceptance_summary_v26.csv").open()))
    assert summary == [
        {
            "summary_id": "FRONTIER_PROVENANCE_EVIDENCE_ACCEPTANCE_V26",
            "frontier_dependency": "SCD24_PROVENANCE_EVIDENCE",
            "frontier_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "candidate_rows": "18",
            "evidence_input_rows_present": "18",
            "accepted_for_promotion_review_rows": "18",
            "blocked_rows": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_ACCEPTANCE_REVIEW_READY",
            "claim_boundary": "frontier_evidence_acceptance_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v27_frontier_provenance_evidence_work_order_stays_open() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_work_order_v27.csv").open()))
    assert len(rows) == 18
    assert all(row["frontier_dependency"] == "SCD24_PROVENANCE_EVIDENCE" for row in rows)
    assert all(row["target_evidence_artifact"] == "data/input/source_import_provenance_evidence_v21.csv" for row in rows)
    assert all(row["current_acceptance_status"] == "ACCEPTED_FOR_REVIEW" for row in rows)
    assert all(row["work_order_status"] == "OPEN_EVIDENCE_COLLECTION_REQUIRED" for row in rows)
    assert all(row["may_write_evidence_input"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all("set_PROVENANCE_EVIDENCE_COMPLETE_only_after_review" in row["minimum_source_tasks"] for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_work_order_summary_v27.csv").open()))
    assert summary == [
        {
            "summary_id": "FRONTIER_PROVENANCE_EVIDENCE_WORK_ORDER_V27",
            "work_order_rows": "18",
            "open_work_order_rows": "18",
            "closed_work_order_rows": "0",
            "target_evidence_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "may_write_evidence_input_anywhere": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_WORK_ORDER_OPEN",
            "claim_boundary": "frontier_work_order_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v28_frontier_work_order_completion_gate_blocks_closure() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/frontier_work_order_completion_gate_v28.csv").open()))
    assert len(rows) == 18
    assert all(row["accepted_for_promotion_review"] == "true" for row in rows)
    assert all(row["work_order_status"] == "OPEN_EVIDENCE_COLLECTION_REQUIRED" for row in rows)
    assert all("work_order_open" in row["completion_blockers"] for row in rows)
    assert all("not_accepted_for_promotion_review" not in row["completion_blockers"] for row in rows)
    assert all(row["completion_decision"] == "DO_NOT_CLOSE_WORK_ORDER" for row in rows)
    assert all(row["may_write_evidence_input_after_completion"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/frontier_work_order_completion_gate_summary_v28.csv").open()))
    assert summary == [
        {
            "summary_id": "FRONTIER_WORK_ORDER_COMPLETION_GATE_V28",
            "completion_gate_rows": "18",
            "work_orders_closed": "0",
            "work_orders_blocked": "18",
            "may_write_evidence_input_anywhere": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_WORK_ORDER_COMPLETION_BLOCKED",
            "claim_boundary": "frontier_work_order_completion_gate_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v29_frontier_evidence_write_authorization_blocks_write() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/frontier_evidence_write_authorization_v29.csv").open()))
    assert rows == [
        {
            "authorization_id": "FEWA29_FRONTIER_EVIDENCE_WRITE",
            "completion_gate_source": "data/derived/frontier_work_order_completion_gate_summary_v28.csv",
            "target_evidence_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "completion_gate_status": "FRONTIER_WORK_ORDER_COMPLETION_BLOCKED",
            "completion_gate_rows": "18",
            "work_orders_closed": "0",
            "target_evidence_input_present": "true",
            "write_blockers": "frontier_work_orders_not_closed;target_evidence_input_already_present",
            "write_authorized": "false",
            "target_file_written": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "frontier_evidence_write_authorization_only_no_evidence_no_scores",
        }
    ]

    summary = list(csv.DictReader((ROOT / "data/derived/frontier_evidence_write_authorization_summary_v29.csv").open()))
    assert summary == [
        {
            "summary_id": "FRONTIER_EVIDENCE_WRITE_AUTHORIZATION_V29",
            "write_authorized": "false",
            "target_evidence_input_present": "true",
            "target_file_written": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_WRITE_BLOCKED",
            "claim_boundary": "frontier_evidence_write_authorization_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v30_frontier_authorized_evidence_writer_writes_zero_rows() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/frontier_authorized_evidence_writer_v30.csv").open()))
    assert rows == [
        {
            "writer_id": "FAEW30_AUTHORIZED_FRONTIER_EVIDENCE_WRITER",
            "authorization_source": "data/derived/frontier_evidence_write_authorization_v29.csv",
            "target_evidence_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "write_authorized": "false",
            "target_preexisting": "true",
            "target_file_written": "false",
            "rows_written": "0",
            "writer_status": "WRITER_BLOCKED_BY_FRONTIER_AUTHORIZATION",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "frontier_authorized_evidence_writer_only_no_evidence_no_scores",
        }
    ]

    summary = list(csv.DictReader((ROOT / "data/derived/frontier_authorized_evidence_writer_summary_v30.csv").open()))
    assert summary == [
        {
            "summary_id": "FRONTIER_AUTHORIZED_EVIDENCE_WRITER_V30",
            "writer_status": "WRITER_BLOCKED_BY_FRONTIER_AUTHORIZATION",
            "write_authorized": "false",
            "target_file_written": "false",
            "rows_written": "0",
            "target_input_file_present_after_writer": "true",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_AUTHORIZED_EVIDENCE_WRITER_BLOCKED",
            "claim_boundary": "frontier_authorized_evidence_writer_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v31_frontier_post_writer_evidence_absence_audit_confirms_absence() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/frontier_post_writer_evidence_absence_audit_v31.csv").open()))
    assert rows == [
        {
            "audit_id": "FPWEA31_POST_WRITER_EVIDENCE_ABSENCE",
            "writer_summary_source": "data/derived/frontier_authorized_evidence_writer_summary_v30.csv",
            "active_writer_summary_source": "data/derived/active_v21_provenance_evidence_writer_summary_v55.csv",
            "target_evidence_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "writer_status": "WRITER_BLOCKED_BY_FRONTIER_AUTHORIZATION",
            "writer_rows_written": "0",
            "writer_target_file_written": "false",
            "active_writer_status": "ACTIVE_V21_PROVENANCE_EVIDENCE_WRITTEN",
            "target_evidence_input_present_after_audit": "true",
            "absence_confirmed": "false",
            "evidence_gate_may_be_promoted": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "post_writer_evidence_presence_audit_only_no_scores",
        }
    ]

    summary = list(csv.DictReader((ROOT / "data/derived/frontier_post_writer_evidence_absence_audit_summary_v31.csv").open()))
    assert summary == [
        {
            "summary_id": "FRONTIER_POST_WRITER_EVIDENCE_ABSENCE_AUDIT_V31",
            "absence_confirmed": "false",
            "target_evidence_input_present_after_audit": "true",
            "evidence_gate_may_be_promoted": "true",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_INPUT_PRESENT_VIA_ACTIVE_V21_WRITER",
            "claim_boundary": "post_writer_evidence_presence_audit_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v32_post_writer_evidence_gate_recheck_blocks_promotion() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_evidence_gate_recheck_v32.csv").open()))
    assert rows == [
        {
            "recheck_id": "PWEGR32_POST_WRITER_EVIDENCE_GATE_RECHECK",
            "absence_audit_source": "data/derived/frontier_post_writer_evidence_absence_audit_summary_v31.csv",
            "evidence_gate_source": "data/derived/source_import_provenance_evidence_gate_summary_v22.csv",
            "absence_confirmed": "false",
            "evidence_input_status": "EVIDENCE_INPUT_PRESENT_VALIDATION_PENDING_REVIEW",
            "valid_evidence_rows": "18",
            "provenance_promotion_allowed_before_recheck": "true",
            "recheck_blockers": "none",
            "provenance_promotion_allowed_after_recheck": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "post_writer_evidence_gate_recheck_only_no_promotion_no_scores",
        }
    ]

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_evidence_gate_recheck_summary_v32.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_EVIDENCE_GATE_RECHECK_V32",
            "absence_confirmed": "false",
            "valid_evidence_rows": "18",
            "provenance_promotion_allowed_after_recheck": "true",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_EVIDENCE_GATE_RECHECK_READY",
            "claim_boundary": "post_writer_evidence_gate_recheck_only_no_promotion_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v33_post_writer_provenance_promotion_recheck_blocks_all_rows() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_provenance_promotion_recheck_v33.csv").open()))
    assert len(rows) == 18
    assert all(row["v23_promotion_decision"] == "PROMOTE_PROVENANCE" for row in rows)
    assert all(row["valid_evidence_rows_after_writer"] == "18" for row in rows)
    assert all(row["promotion_recheck_blockers"] == "none" for row in rows)
    assert all(row["provenance_promotion_allowed_after_recheck"] == "true" for row in rows)
    assert all(row["provenance_rows_promoted_after_recheck"] == "1" for row in rows)
    assert all(row["raw_import_allowed_after_recheck"] == "true" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_provenance_promotion_recheck_summary_v33.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_PROVENANCE_PROMOTION_RECHECK_V33",
            "promotion_recheck_rows": "18",
            "promotion_allowed_rows_after_recheck": "18",
            "promotion_blocked_rows_after_recheck": "0",
            "provenance_rows_promoted_after_recheck": "18",
            "raw_import_allowed_rows_after_recheck": "18",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_PROVENANCE_PROMOTION_RECHECK_READY",
            "claim_boundary": "post_writer_provenance_promotion_recheck_only_no_promotion_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v34_post_writer_raw_import_recheck_blocks_all_rows() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_raw_import_recheck_v34.csv").open()))
    assert len(rows) == 18
    assert all(row["v20_raw_import_decision"] == "ALLOW_RAW_IMPORT" for row in rows)
    assert all(row["provenance_rows_promoted_after_recheck"] == "1" for row in rows)
    assert all(row["raw_import_recheck_blockers"] == "none" for row in rows)
    assert all(row["raw_import_allowed_after_recheck"] == "true" for row in rows)
    assert all(row["raw_rows_imported_after_recheck"] == "0" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_raw_import_recheck_summary_v34.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_RAW_IMPORT_RECHECK_V34",
            "raw_import_recheck_rows": "18",
            "raw_import_allowed_rows_after_recheck": "18",
            "raw_import_blocked_rows_after_recheck": "0",
            "raw_rows_imported_after_recheck": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_RAW_IMPORT_RECHECK_READY",
            "claim_boundary": "post_writer_raw_import_recheck_only_no_raw_import_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v35_post_writer_raw_adapter_recheck_blocks_v12_write() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_raw_adapter_recheck_v35.csv").open()))
    assert rows == [
        {
            "recheck_id": "PWRAR35_POST_WRITER_RAW_ADAPTER_RECHECK",
            "raw_import_recheck_source": "data/derived/post_writer_raw_import_recheck_summary_v34.csv",
            "raw_adapter_source": "data/derived/source_import_raw_adapter_gate_v15.csv",
            "raw_input_status": "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW",
            "raw_rows_seen": "450",
            "valid_raw_rows": "450",
            "raw_rows_imported_after_recheck": "0",
            "adapter_recheck_blockers": "zero_raw_rows_imported_after_recheck",
            "target_file_written_after_recheck": "false",
            "real_values_input_may_exist_after_recheck": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "post_writer_raw_adapter_recheck_only_no_v12_write_no_scores",
        }
    ]

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_raw_adapter_recheck_summary_v35.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_RAW_ADAPTER_RECHECK_V35",
            "raw_input_status": "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW",
            "valid_raw_rows": "450",
            "target_file_written_after_recheck": "false",
            "real_values_input_may_exist_after_recheck": "true",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_RAW_ADAPTER_RECHECK_BLOCKED",
            "claim_boundary": "post_writer_raw_adapter_recheck_only_no_v12_write_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v36_post_writer_real_values_gate_recheck_blocks_activation() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_real_values_gate_recheck_v36.csv").open()))
    assert len(rows) == 18
    assert all(row["v12_input_file_status"] == "REAL_VALUE_HEADER_OK" for row in rows)
    assert sum(int(row["v12_imported_numeric_rows"]) for row in rows) == 450
    assert all(row["v12_real_value_gate_status"] == "REAL_VALUES_PRESENT_VALIDATION_PENDING_LEAKAGE" for row in rows)
    assert all(row["rows_passing_value_gate_after_recheck"] == "1" for row in rows)
    assert all(row["activation_decision_after_recheck"] == "VALUE_GATE_PASSED_PENDING_LEAKAGE" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_real_values_gate_recheck_summary_v36.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_REAL_VALUES_GATE_RECHECK_V36",
            "real_value_recheck_rows": "18",
            "imported_numeric_rows_after_recheck": "450",
            "rows_passing_value_gate_after_recheck": "18",
            "rows_activated_after_recheck": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_REAL_VALUES_GATE_RECHECK_READY",
            "claim_boundary": "post_writer_real_values_gate_recheck_only_no_activation_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v37_post_writer_leakage_audit_recheck_blocks_activation() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_leakage_audit_recheck_v37.csv").open()))
    assert len(rows) == 18
    assert all(row["v09_leakage_status"] == "LEAKAGE_AUDIT_PASS" for row in rows)
    assert all(row["rows_passing_value_gate_after_recheck"] == "1" for row in rows)
    assert all("post_writer_real_values_gate_not_passed" not in row["leakage_recheck_blockers"] for row in rows)
    assert all("v09_leakage_audit_not_passed" not in row["leakage_recheck_blockers"] for row in rows)
    assert all(row["leakage_pass_after_recheck"] == "true" for row in rows)
    assert all(row["activation_allowed_after_recheck"] == "true" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_leakage_audit_recheck_summary_v37.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_LEAKAGE_AUDIT_RECHECK_V37",
            "leakage_recheck_rows": "18",
            "leakage_pass_rows_after_recheck": "18",
            "leakage_blocked_rows_after_recheck": "0",
            "activation_allowed_rows_after_recheck": "18",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_LEAKAGE_AUDIT_RECHECK_READY",
            "claim_boundary": "post_writer_leakage_audit_recheck_only_no_activation_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v38_post_writer_scoring_activation_recheck_blocks_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_scoring_activation_recheck_v38.csv").open()))
    assert len(rows) == 18
    assert all(row["v37_leakage_pass_after_recheck"] == "true" for row in rows)
    assert all(row["v37_activation_allowed_after_recheck"] == "true" for row in rows)
    assert all(row["v13_activation_decision"] == "ACTIVATE_FOR_SCORING" for row in rows)
    assert all("post_writer_leakage_audit_not_passed" not in row["activation_recheck_blockers"] for row in rows)
    assert all("post_writer_leakage_recheck_disallows_activation" not in row["activation_recheck_blockers"] for row in rows)
    assert all("v13_activation_gate_not_passed" not in row["activation_recheck_blockers"] for row in rows)
    assert all(row["activation_decision_after_recheck"] == "ACTIVATE_FOR_SCORING" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_scoring_activation_recheck_summary_v38.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_SCORING_ACTIVATION_RECHECK_V38",
            "activation_recheck_rows": "18",
            "rows_activated_after_recheck": "18",
            "row_level_blocked_rows_after_recheck": "0",
            "global_blockers_after_recheck": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_SCORING_ACTIVATION_RECHECK_READY",
            "claim_boundary": "post_writer_scoring_activation_recheck_only_no_activation_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v39_post_writer_scoring_preflight_recheck_blocks_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_scoring_preflight_recheck_v39.csv").open()))
    assert len(rows) == 6
    assert sum(row["v07_current_status"].startswith("BLOCKED") for row in rows) == 0
    assert all(row["v38_rows_activated_after_recheck"] == "18" for row in rows)
    assert all("v07_requirement_blocked" not in row["preflight_recheck_blockers"] for row in rows)
    assert all("post_writer_activation_recheck_zero_rows" not in row["preflight_recheck_blockers"] for row in rows)
    assert all("post_writer_activation_recheck_scoring_not_allowed" in row["preflight_recheck_blockers"] for row in rows)
    assert all(row["preflight_requirement_status_after_recheck"] == "BLOCKED" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_scoring_preflight_recheck_summary_v39.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_SCORING_PREFLIGHT_RECHECK_V39",
            "preflight_requirement_rows": "6",
            "blocked_requirements_after_recheck": "6",
            "ready_requirements_after_recheck": "0",
            "formula_policy_components_ready_not_run": "7",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_SCORING_PREFLIGHT_RECHECK_BLOCKED",
            "claim_boundary": "post_writer_scoring_preflight_recheck_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v40_post_writer_scoring_dependency_closure_recheck_blocks_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_scoring_dependency_closure_recheck_v40.csv").open()))
    assert len(rows) == 13
    assert sum(row["v24_dependency_decision"] == "READY" for row in rows) == 13
    assert sum(row["v24_dependency_decision"] == "BLOCKED" for row in rows) == 0
    assert all(row["v39_ready_requirements_after_recheck"] == "0" for row in rows)
    assert all(
        ("v24_dependency_not_ready" in row["dependency_recheck_blockers"])
        == (row["v24_dependency_decision"] != "READY")
        for row in rows
    )
    assert all("post_writer_preflight_recheck_zero_ready_requirements" in row["dependency_recheck_blockers"] for row in rows)
    assert all("post_writer_preflight_recheck_scoring_not_allowed" in row["dependency_recheck_blockers"] for row in rows)
    assert all(row["dependency_decision_after_recheck"] == "BLOCKED" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_scoring_dependency_closure_recheck_summary_v40.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_SCORING_DEPENDENCY_CLOSURE_RECHECK_V40",
            "dependencies_rechecked": "13",
            "ready_dependencies_after_recheck": "0",
            "blocked_dependencies_after_recheck": "13",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_SCORING_DEPENDENCY_CLOSURE_RECHECK_BLOCKED",
            "claim_boundary": "post_writer_scoring_dependency_closure_recheck_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v41_post_writer_scoring_unblock_priority_recheck_confirms_frontier() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_scoring_unblock_priority_recheck_v41.csv").open()))
    assert len(rows) == 13
    assert all(row["v40_ready_dependencies_after_recheck"] == "0" for row in rows)
    assert all("v25_priority_dependency_blocked" not in row["priority_recheck_blockers"] for row in rows)
    assert all("post_writer_dependency_recheck_zero_ready_dependencies" in row["priority_recheck_blockers"] for row in rows)
    assert all("post_writer_dependency_recheck_scoring_not_allowed" in row["priority_recheck_blockers"] for row in rows)
    assert sum(row["frontier_now_after_recheck"] == "true" for row in rows) == 0
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_scoring_unblock_priority_recheck_summary_v41.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_SCORING_UNBLOCK_PRIORITY_RECHECK_V41",
            "priority_rows_rechecked": "13",
            "blocked_priority_rows_after_recheck": "13",
            "frontier_now_rows_after_recheck": "0",
            "first_frontier_dependency_after_recheck": "none",
            "first_frontier_artifact_after_recheck": "none",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_SCORING_UNBLOCK_FRONTIER_CLEAR",
            "claim_boundary": "post_writer_scoring_unblock_priority_recheck_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v42_post_writer_frontier_evidence_acceptance_recheck_blocks_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_frontier_evidence_acceptance_recheck_v42.csv").open()))
    assert len(rows) == 18
    assert all(row["v41_frontier_dependency"] == "none" for row in rows)
    assert all(row["v41_frontier_artifact"] == "none" for row in rows)
    assert all(row["v26_acceptance_status"] == "ACCEPTED_FOR_REVIEW" for row in rows)
    assert all(row["v26_evidence_input_present"] == "true" for row in rows)
    assert all(row["v26_accepted_for_promotion_review"] == "true" for row in rows)
    assert all(row["acceptance_recheck_blockers"] == "post_writer_frontier_not_provenance_evidence" for row in rows)
    assert all(row["accepted_for_promotion_review_after_recheck"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_frontier_evidence_acceptance_recheck_summary_v42.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_FRONTIER_EVIDENCE_ACCEPTANCE_RECHECK_V42",
            "acceptance_recheck_rows": "18",
            "evidence_input_rows_present_after_recheck": "18",
            "accepted_for_promotion_review_rows_after_recheck": "0",
            "blocked_rows_after_recheck": "18",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_FRONTIER_EVIDENCE_ACCEPTANCE_RECHECK_BLOCKED",
            "claim_boundary": "post_writer_frontier_evidence_acceptance_recheck_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v43_post_writer_frontier_work_order_recheck_blocks_evidence_write() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_frontier_work_order_recheck_v43.csv").open()))
    assert len(rows) == 18
    assert all(row["v42_accepted_for_promotion_review_after_recheck"] == "false" for row in rows)
    assert all(row["v27_work_order_status"] == "OPEN_EVIDENCE_COLLECTION_REQUIRED" for row in rows)
    assert all(row["v27_may_write_evidence_input"] == "false" for row in rows)
    assert all("post_writer_frontier_acceptance_not_passed" in row["work_order_recheck_blockers"] for row in rows)
    assert all("v27_work_order_not_closed" in row["work_order_recheck_blockers"] for row in rows)
    assert all("v27_evidence_write_not_allowed" in row["work_order_recheck_blockers"] for row in rows)
    assert all(row["work_order_status_after_recheck"] == "OPEN_EVIDENCE_COLLECTION_REQUIRED" for row in rows)
    assert all(row["may_write_evidence_input_after_recheck"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_frontier_work_order_recheck_summary_v43.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_FRONTIER_WORK_ORDER_RECHECK_V43",
            "work_order_recheck_rows": "18",
            "open_work_order_rows_after_recheck": "18",
            "closed_work_order_rows_after_recheck": "0",
            "may_write_evidence_input_rows_after_recheck": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_FRONTIER_WORK_ORDER_RECHECK_BLOCKED",
            "claim_boundary": "post_writer_frontier_work_order_recheck_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v44_frontier_provenance_evidence_intake_contract_is_not_evidence() -> None:
    rules = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_intake_contract_v44.csv").open()))
    checklist = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_intake_checklist_v44.csv").open()))
    required_fields = {
        "galaxy_id",
        "catalog",
        "table_or_file",
        "version_or_date",
        "row_id",
        "sha256_or_external_accession",
        "source_route",
        "leakage_evidence_id",
        "provenance_evidence_status",
    }
    assert len(rules) == 9
    assert {row["field_name"] for row in rules} == required_fields
    assert all(row["target_evidence_file"] == "data/input/source_import_provenance_evidence_v21.csv" for row in rules)
    assert all(row["required_before_promotion"] == "true" for row in rules)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rules)
    assert any("uses_rotation_residual_or_family_score" in row["reject_if"] for row in rules)

    assert len(checklist) == 18
    assert all(row["work_order_recheck_source"] == "data/derived/post_writer_frontier_work_order_recheck_v43.csv" for row in checklist)
    assert all(row["manual_collection_status"] == "READY_FOR_REVIEWED_SOURCE_COLLECTION" for row in checklist)
    assert all(row["may_copy_template_to_evidence_input"] == "true" for row in checklist)
    assert all(row["may_mark_complete_without_review"] == "false" for row in checklist)
    assert all(row["may_promote_after_contract_only"] == "false" for row in checklist)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in checklist)

    summary = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_intake_contract_summary_v44.csv").open()))
    assert summary == [
        {
            "summary_id": "FRONTIER_PROVENANCE_EVIDENCE_INTAKE_CONTRACT_V44",
            "target_evidence_file": "data/input/source_import_provenance_evidence_v21.csv",
            "review_rule_rows": "9",
            "row_checklist_rows": "18",
            "manual_collection_ready_rows": "18",
            "evidence_rows_created_by_contract": "0",
            "promotion_allowed_by_contract_only": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_INTAKE_CONTRACT_READY_NOT_EVIDENCE",
            "claim_boundary": "frontier_evidence_intake_contract_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v45_frontier_provenance_source_candidate_ledger_is_not_evidence() -> None:
    sources = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_source_candidate_ledger_v45.csv").open()))
    coverage = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_source_candidate_coverage_v45.csv").open()))
    assert len(sources) == 2
    assert {row["source_candidate_id"] for row in sources} == {"FPSC45_SPARC_TABLE1", "FPSC45_SPARC_MASSMODELS"}
    assert all(row["catalog"] == "SPARC" for row in sources)
    assert any(
        row["table_or_file"] == "SPARC_Lelli2016c.mrt"
        and row["sha256_or_external_accession"]
        == "sha256:5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243"
        for row in sources
    )
    assert any(
        row["table_or_file"] == "MassModels_Lelli2016c.mrt"
        and row["sha256_or_external_accession"]
        == "sha256:9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c"
        for row in sources
    )
    assert all(row["review_status"] == "SOURCE_CANDIDATE_READY_FOR_HUMAN_REVIEW" for row in sources)
    assert all(row["may_write_v21_evidence_input"] == "false" for row in sources)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in sources)

    assert len(coverage) == 18
    assert all(row["primary_source_candidate_id"] == "FPSC45_SPARC_TABLE1" for row in coverage)
    assert all(row["coverage_status"] == "CANDIDATE_ROW_IDENTIFIED_NOT_V21_EVIDENCE" for row in coverage)
    assert all(row["may_mark_provenance_complete"] == "false" for row in coverage)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in coverage)

    summary = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_source_candidate_ledger_summary_v45.csv").open()))
    assert summary == [
        {
            "summary_id": "FRONTIER_PROVENANCE_SOURCE_CANDIDATE_LEDGER_V45",
            "source_candidate_rows": "2",
            "ready_for_human_review_source_rows": "2",
            "coverage_rows": "18",
            "candidate_rows_identified": "18",
            "v21_evidence_rows_created": "0",
            "may_write_v21_evidence_input_anywhere": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_PROVENANCE_SOURCE_CANDIDATES_READY_NOT_EVIDENCE",
            "claim_boundary": "frontier_provenance_source_candidate_ledger_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v46_frontier_provenance_evidence_payload_draft_is_review_required() -> None:
    draft = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_payload_draft_v46.csv").open()))
    review = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_payload_draft_review_v46.csv").open()))
    required_fields = {
        "galaxy_id",
        "catalog",
        "table_or_file",
        "version_or_date",
        "row_id",
        "sha256_or_external_accession",
        "source_route",
        "leakage_evidence_id",
        "provenance_evidence_status",
    }
    assert len(draft) == 18
    assert set(draft[0].keys()) == required_fields
    assert all(row["catalog"] == "SPARC" for row in draft)
    assert all(row["table_or_file"] == "SPARC_Lelli2016c.mrt" for row in draft)
    assert all(
        row["sha256_or_external_accession"]
        == "sha256:5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243"
        for row in draft
    )
    assert all(row["provenance_evidence_status"] == "REVIEW_REQUIRED_NOT_COMPLETE" for row in draft)

    assert len(review) == 18
    assert all(row["review_required"] == "true" for row in review)
    assert all(row["may_copy_to_v21_after_review"] == "false" for row in review)
    assert all(row["may_mark_complete_without_review"] == "false" for row in review)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in review)

    summary = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_payload_draft_summary_v46.csv").open()))
    assert summary == [
        {
            "summary_id": "FRONTIER_PROVENANCE_EVIDENCE_PAYLOAD_DRAFT_V46",
            "draft_rows": "18",
            "draft_rows_requiring_review": "18",
            "complete_evidence_rows": "0",
            "v21_evidence_rows_created": "0",
            "may_copy_to_v21_without_review": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_PAYLOAD_DRAFT_READY_REVIEW_REQUIRED",
            "claim_boundary": "frontier_provenance_evidence_payload_draft_only_no_v21_write_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v47_frontier_provenance_review_package_contains_review_artifacts() -> None:
    package_root = ROOT / "review_packages/frontier_provenance_v46_review_package"
    zip_path = ROOT / "review_packages/frontier_provenance_v46_review_package.zip"
    required = {
        "README.md",
        "DO_NOT_COPY_WITHOUT_REVIEW.md",
        "REVIEW_MANIFEST.csv",
        "data/frontier_provenance_evidence_intake_contract_v44.csv",
        "data/frontier_provenance_evidence_intake_checklist_v44.csv",
        "data/frontier_provenance_source_candidate_ledger_v45.csv",
        "data/frontier_provenance_source_candidate_coverage_v45.csv",
        "data/frontier_provenance_evidence_payload_draft_v46.csv",
        "data/frontier_provenance_evidence_payload_draft_review_v46.csv",
        "data/frontier_provenance_evidence_payload_draft_summary_v46.csv",
        "templates/source_import_provenance_evidence_v21_TEMPLATE.csv",
    }
    assert package_root.exists()
    assert zip_path.exists()
    for rel in required:
        assert (package_root / rel).exists(), rel

    manifest = list(csv.DictReader((package_root / "REVIEW_MANIFEST.csv").open()))
    assert len(manifest) == len(required) - 1
    assert {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"}
    assert all(row["claim_boundary"] == "review_package_only_no_evidence_no_scores" for row in manifest)

    draft = list(csv.DictReader((package_root / "data/frontier_provenance_evidence_payload_draft_v46.csv").open()))
    assert len(draft) == 18
    assert all(row["provenance_evidence_status"] == "REVIEW_REQUIRED_NOT_COMPLETE" for row in draft)

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert {f"frontier_provenance_v46_review_package/{rel}" for rel in required}.issubset(names)


def test_v48_frontier_provenance_review_response_intake_keeps_draft_not_promoted() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_review_response_intake_v48.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_review_response_intake_summary_v48.csv").open()))
    response_dir = ROOT / "review_packages/frontier_provenance_v46_completed_review_response"
    response_zip = ROOT / "review_packages/frontier_provenance_v46_completed_review_response.zip"
    required = {
        "frontier_provenance_v46_review_response.csv",
        "frontier_provenance_v46_review_completed_summary.csv",
        "frontier_provenance_v46_review_notes.md",
        "frontier_provenance_v46_review_validation_log.txt",
    }
    assert response_zip.exists()
    assert response_dir.exists()
    for rel in required:
        assert (response_dir / rel).exists(), rel
    with zipfile.ZipFile(response_zip) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    assert required.issubset(names)
    assert len(rows) == 18
    assert all(row["row_route_internal_consistency"] == "pass" for row in rows)
    assert all(
        row["source_hash_route_status"] == "source_hash_matches_package_candidate_ledger_external_sha_not_recomputed"
        for row in rows
    )
    assert all(row["leakage_evidence_status"] == "pass_prescore_source_route_review_id" for row in rows)
    assert all(row["reviewer_decision"] == "KEEP_REVIEW_REQUIRED_NOT_COMPLETE_NO_V21_WRITE" for row in rows)
    assert all(row["may_copy_to_v21_after_review"] == "false" for row in rows)
    assert all(row["may_mark_provenance_complete"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    assert summary == [
        {
            "summary_id": "FRONTIER_PROVENANCE_REVIEW_RESPONSE_INTAKE_V48",
            "response_zip": "review_packages/frontier_provenance_v46_completed_review_response.zip",
            "response_files_present": "4",
            "review_rows": "18",
            "route_and_prescore_pass_rows": "18",
            "review_decision": "ACCEPT_AS_REVIEW_READY_DRAFT_ONLY_NOT_PROMOTED",
            "completion_status": "PASS_WITH_CAVEAT",
            "external_hash_recomputed": "false",
            "complete_evidence_rows_authorized": "0",
            "v21_evidence_rows_created": "0",
            "may_copy_to_v21_without_separate_promotion": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "REVIEW_RESPONSE_ACCEPTED_AS_DRAFT_ONLY_NOT_PROMOTED",
            "claim_boundary": "frontier_provenance_review_response_intake_only_no_v21_write_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v49_frontier_review_promotion_gate_blocks_caveated_review_response() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/frontier_review_promotion_gate_v49.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/frontier_review_promotion_gate_summary_v49.csv").open()))
    assert len(rows) == 18
    assert all(row["v48_route_consistency"] == "pass" for row in rows)
    assert all(
        row["v48_source_hash_route_status"] == "source_hash_matches_package_candidate_ledger_external_sha_not_recomputed"
        for row in rows
    )
    assert all(row["v48_leakage_evidence_status"] == "pass_prescore_source_route_review_id" for row in rows)
    assert all(row["v48_reviewer_decision"] == "KEEP_REVIEW_REQUIRED_NOT_COMPLETE_NO_V21_WRITE" for row in rows)
    assert all(row["v48_completion_status"] == "PASS_WITH_CAVEAT" for row in rows)
    assert all(row["external_hash_recomputed"] == "false" for row in rows)
    assert all("external_source_hash_not_independently_recomputed" in row["promotion_gate_blockers"] for row in rows)
    assert all("reviewer_decision_keeps_review_required_not_complete" in row["promotion_gate_blockers"] for row in rows)
    assert all(row["promotion_gate_decision"] == "DO_NOT_PROMOTE_TO_V21_EVIDENCE" for row in rows)
    assert all(row["may_write_v21_evidence_input_after_gate"] == "false" for row in rows)
    assert all(row["may_mark_provenance_complete_after_gate"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    assert summary == [
        {
            "summary_id": "FRONTIER_REVIEW_PROMOTION_GATE_V49",
            "review_rows": "18",
            "promotion_allowed_rows": "0",
            "promotion_blocked_rows": "18",
            "v21_evidence_rows_created": "0",
            "provenance_complete_rows_marked": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_REVIEW_PROMOTION_BLOCKED",
            "next_required_action": "independently_recompute_external_sparc_hash_and_issue_explicit_promotion_authorization",
            "claim_boundary": "frontier_review_promotion_gate_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v50_frontier_external_hash_recompute_audit_matches_sparc_sources() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/frontier_external_hash_recompute_audit_v50.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/frontier_external_hash_recompute_audit_summary_v50.csv").open()))
    expected = {
        "FPSC45_SPARC_TABLE1": ("SPARC_Lelli2016c.mrt", "5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243"),
        "FPSC45_SPARC_MASSMODELS": ("MassModels_Lelli2016c.mrt", "9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c"),
    }
    assert len(rows) == 2
    by_id = {row["source_candidate_id"]: row for row in rows}
    assert set(by_id) == set(expected)
    for source_id, (table, digest) in expected.items():
        row = by_id[source_id]
        assert row["table_or_file"] == table
        assert row["expected_sha256"] == digest
        assert row["recomputed_sha256"] == digest
        assert int(row["file_size_bytes"]) > 0
        assert row["source_access_status"] == "LIVE_DOWNLOAD_CACHED_FOR_HASH_AUDIT"
        assert row["hash_recompute_status"] == "EXTERNAL_HASH_RECOMPUTED_MATCHED"
        assert row["may_promote_v21_by_hash_alone"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"

    assert summary == [
        {
            "summary_id": "FRONTIER_EXTERNAL_HASH_RECOMPUTE_AUDIT_V50",
            "source_candidate_rows": "2",
            "hash_recomputed_matched_rows": "2",
            "primary_table1_hash_recomputed_matched": "true",
            "v21_evidence_rows_created": "0",
            "provenance_complete_rows_marked": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EXTERNAL_HASH_RECOMPUTED_MATCHED",
            "claim_boundary": "frontier_external_hash_recompute_audit_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v51_post_hash_frontier_review_promotion_recheck_still_requires_authorization() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_hash_frontier_review_promotion_recheck_v51.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/post_hash_frontier_review_promotion_recheck_summary_v51.csv").open()))
    assert len(rows) == 18
    assert all(row["primary_table1_hash_recomputed_matched"] == "true" for row in rows)
    assert all(row["v48_reviewer_decision"] == "KEEP_REVIEW_REQUIRED_NOT_COMPLETE_NO_V21_WRITE" for row in rows)
    assert all("primary_table1_hash_not_recomputed_matched" not in row["promotion_recheck_blockers"] for row in rows)
    assert all("explicit_promotion_authorization_missing" in row["promotion_recheck_blockers"] for row in rows)
    assert all(row["promotion_recheck_decision"] == "DO_NOT_PROMOTE_TO_V21_EVIDENCE" for row in rows)
    assert all(row["may_write_v21_evidence_input_after_recheck"] == "false" for row in rows)
    assert all(row["may_mark_provenance_complete_after_recheck"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    assert summary == [
        {
            "summary_id": "POST_HASH_FRONTIER_REVIEW_PROMOTION_RECHECK_V51",
            "review_rows": "18",
            "primary_hash_matched_review_rows": "18",
            "promotion_allowed_rows_after_hash": "0",
            "promotion_blocked_rows_after_hash": "18",
            "v21_evidence_rows_created": "0",
            "provenance_complete_rows_marked": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_HASH_FRONTIER_REVIEW_PROMOTION_RECHECK_BLOCKED",
            "next_required_action": "issue_explicit_review_promotion_authorization_for_v21_copy_and_provenance_completion",
            "claim_boundary": "post_hash_frontier_review_promotion_recheck_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v52_post_hash_review_promotion_package_is_review_only() -> None:
    package_root = ROOT / "review_packages/frontier_post_hash_review_promotion_v51_review_package"
    zip_path = ROOT / "review_packages/frontier_post_hash_review_promotion_v51_review_package.zip"
    required = {
        "README.md",
        "DO_NOT_COPY_WITHOUT_EXPLICIT_PROMOTION.md",
        "REVIEW_MANIFEST.csv",
        "data/frontier_provenance_evidence_payload_draft_v46.csv",
        "data/frontier_provenance_evidence_payload_draft_review_v46.csv",
        "data/frontier_provenance_review_response_intake_v48.csv",
        "data/frontier_provenance_review_response_intake_summary_v48.csv",
        "data/frontier_review_promotion_gate_v49.csv",
        "data/frontier_review_promotion_gate_summary_v49.csv",
        "data/frontier_external_hash_recompute_audit_v50.csv",
        "data/frontier_external_hash_recompute_audit_summary_v50.csv",
        "data/post_hash_frontier_review_promotion_recheck_v51.csv",
        "data/post_hash_frontier_review_promotion_recheck_summary_v51.csv",
        "templates/frontier_review_promotion_authorization_TEMPLATE.csv",
    }
    assert package_root.exists()
    assert zip_path.exists()
    for rel in required:
        assert (package_root / rel).exists(), rel

    manifest = list(csv.DictReader((package_root / "REVIEW_MANIFEST.csv").open()))
    assert len(manifest) == len(required) - 1
    assert {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"}
    assert all(row["claim_boundary"] == "post_hash_review_promotion_package_only_no_evidence_no_scores" for row in manifest)

    template = list(csv.DictReader((package_root / "templates/frontier_review_promotion_authorization_TEMPLATE.csv").open()))
    assert len(template) == 18
    assert all(row["primary_table1_hash_recomputed_matched"] == "true" for row in template)
    assert all(row["reviewer_promotion_decision"] == "KEEP_REVIEW_REQUIRED_NOT_COMPLETE_NO_V21_WRITE" for row in template)
    assert all(row["may_copy_to_v21_after_authorization"] == "false" for row in template)
    assert all(row["may_mark_provenance_complete_after_authorization"] == "false" for row in template)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in template)

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert {f"frontier_post_hash_review_promotion_v51_review_package/{rel}" for rel in required}.issubset(names)


def test_v53_post_hash_review_promotion_response_intake_accepts_authorization() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_hash_review_promotion_response_intake_v53.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/post_hash_review_promotion_response_intake_summary_v53.csv").open()))
    response_dir = ROOT / "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response"
    response_zip = ROOT / "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response.zip"
    required = {
        "frontier_post_hash_review_promotion_v51_authorization_response.csv",
        "frontier_post_hash_review_promotion_v51_completed_summary.csv",
        "frontier_post_hash_review_promotion_v51_review_notes.md",
        "frontier_post_hash_review_promotion_v51_validation_log.txt",
    }
    assert response_zip.exists()
    assert response_dir.exists()
    for rel in required:
        assert (response_dir / rel).exists(), rel
    with zipfile.ZipFile(response_zip) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    assert required.issubset(names)
    assert len(rows) == 18
    assert all(row["primary_table1_hash_recomputed_matched"] == "true" for row in rows)
    assert all(row["reviewer_promotion_decision"] == "PROMOTE_TO_COMPLETE_V21_EVIDENCE" for row in rows)
    assert all(row["may_copy_to_v21_after_authorization"] == "true" for row in rows)
    assert all(row["may_mark_provenance_complete_after_authorization"] == "true" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    assert summary == [
        {
            "summary_id": "POST_HASH_REVIEW_PROMOTION_RESPONSE_INTAKE_V53",
            "response_zip": "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response.zip",
            "response_files_present": "4",
            "review_rows": "18",
            "promote_to_complete_v21_evidence_rows": "18",
            "copy_to_v21_authorized_rows": "18",
            "provenance_complete_authorized_rows": "18",
            "primary_hash_matched_rows": "18",
            "source_decision": "AUTHORIZE_PROMOTION_FOR_LATER_INGESTION_GATE_ONLY",
            "v21_evidence_rows_created_by_response": "0",
            "provenance_complete_rows_marked_by_response": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_HASH_REVIEW_PROMOTION_AUTHORIZATION_ACCEPTED_FOR_INGESTION",
            "claim_boundary": "post_hash_review_promotion_response_intake_only_no_v21_write_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v54_authorized_provenance_evidence_payload_is_ready_for_active_input() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/authorized_provenance_evidence_payload_v54.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/authorized_provenance_evidence_payload_summary_v54.csv").open()))
    assert len(rows) == 18
    assert all(row["catalog"] == "SPARC" for row in rows)
    assert all(row["table_or_file"] == "SPARC_Lelli2016c.mrt" for row in rows)
    assert all(row["provenance_evidence_status"] == "PROVENANCE_EVIDENCE_COMPLETE" for row in rows)
    assert all(row["payload_write_status"] == "READY_FOR_SEPARATE_ACTIVE_V21_WRITE_GATE" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert (ROOT / "data/input/source_import_provenance_evidence_v21.csv").exists()

    assert summary == [
        {
            "summary_id": "AUTHORIZED_PROVENANCE_EVIDENCE_PAYLOAD_V54",
            "payload_rows": "18",
            "complete_provenance_payload_rows": "18",
            "ready_for_active_v21_write_rows": "18",
            "active_v21_target": "data/input/source_import_provenance_evidence_v21.csv",
            "active_v21_target_present": "true",
            "active_v21_rows_written_by_this_step": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "AUTHORIZED_PROVENANCE_EVIDENCE_PAYLOAD_READY_NOT_ACTIVE_INPUT",
            "next_required_action": "run_separate_active_v21_write_gate_then_recompute_source_import_provenance_gates",
            "claim_boundary": "authorized_provenance_evidence_payload_only_no_active_input_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v55_active_v21_provenance_evidence_writer_writes_complete_input() -> None:
    rows = list(csv.DictReader((ROOT / "data/input/source_import_provenance_evidence_v21.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/active_v21_provenance_evidence_writer_summary_v55.csv").open()))
    assert len(rows) == 18
    assert all(row["catalog"] == "SPARC" for row in rows)
    assert all(row["table_or_file"] == "SPARC_Lelli2016c.mrt" for row in rows)
    assert all(row["provenance_evidence_status"] == "PROVENANCE_EVIDENCE_COMPLETE" for row in rows)
    assert summary == [
        {
            "summary_id": "ACTIVE_V21_PROVENANCE_EVIDENCE_WRITER_V55",
            "source_payload": "data/derived/authorized_provenance_evidence_payload_v54.csv",
            "target_evidence_input": "data/input/source_import_provenance_evidence_v21.csv",
            "rows_written": "18",
            "complete_provenance_rows_written": "18",
            "target_file_written": "true",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "ACTIVE_V21_PROVENANCE_EVIDENCE_WRITTEN",
            "claim_boundary": "active_v21_provenance_evidence_writer_only_no_observed_values_no_scores_no_dark_sector_verdict",
        }
    ]


def test_arxiv_zip_is_source_only_if_present() -> None:
    zip_path = ROOT / "arxiv_submission_source.zip"
    if not zip_path.exists():
        return
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "main.pdf" not in names


def test_theory_side_scoring_anchor_preserves_claim_boundary() -> None:
    note = (ROOT / "docs/theory_side_scoring_anchor_v81.md").read_text()
    tex = (ROOT / "paper11_submission_source/main.tex").read_text()
    readme = (ROOT / "README.md").read_text()

    required_markers = [
        "THEORY_SIDE_SCORING_ANCHOR_V81_CREATED",
        "RESTRICTED_LOCAL_SCORING_PRIMITIVE_IMPORTED_AS_PROTOCOL_ANCHOR",
        "ENDPOINT_SCORING_NOT_ACTIVATED_BY_THEORY_ANCHOR",
        "DARK_SECTOR_DECISION_NOT_CLAIMED",
        "PHYSICAL_TIME_NOT_CLAIMED",
        "PHYSICAL_READOUT_NOT_CLAIMED",
    ]
    for marker in required_markers:
        assert marker in note

    assert "restricted local `U_read`" in readme
    assert "restricted formal local order-readout" in tex
    assert "admissibility pass under stated assumptions" in tex
    assert "It does not activate endpoint scoring" in tex
    assert "prove physical time/readout" in readme


def test_upstream_results_scoring_impact_v82_preserves_scoring_boundary() -> None:
    note = (ROOT / "docs/upstream_results_scoring_impact_v82.md").read_text()
    tex = (ROOT / "paper11_submission_source/main.tex").read_text()
    readme = (ROOT / "README.md").read_text()

    required_markers = [
        "UPSTREAM_RESULTS_SCORING_IMPACT_V82_CREATED",
        "PAPER10_SHAPE_READOUT_IMPACT_RECORDED",
        "TAU_CORE_K_TIME_RANK_DOMAIN_DISCIPLINE_RECORDED",
        "SCORING_DESIGN_UPDATED_NOT_ACTIVATED",
        "NEXT_SCORING_BLOCKER_MOVED_TO_M0_NO_DARK_SCALE_POLICY_V07",
        "DARK_SECTOR_DECISION_NOT_CLAIMED",
        "PHYSICAL_READOUT_NOT_CLAIMED",
        "PHYSICAL_TIME_NOT_CLAIMED",
    ]
    for marker in required_markers:
        assert marker in note

    assert "m0_no_dark_scale_policy_v07" in note
    assert "Paper 10 Shape/Readout Consequence" in tex
    assert "does not activate scoring" in tex
    assert "does not prove `Theta_time`" in readme
    assert "activates Paper 11 endpoint scoring" in readme
