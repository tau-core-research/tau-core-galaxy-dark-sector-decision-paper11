from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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
        "data/derived/leakage_prescore_artifact_collection_intake_v63.csv",
        "data/derived/leakage_prescore_artifact_collection_intake_summary_v63.csv",
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
        "scripts/run_readiness_audit.py",
        "scripts/run_scoring_preflight.py",
        "scripts/build_scoring_input_scaffold.py",
        "scripts/run_source_import_leakage_audit.py",
        "scripts/build_source_import_contract.py",
        "scripts/build_leakage_audit_evidence_template.py",
        "scripts/build_leakage_audit_review_package.py",
        "scripts/ingest_leakage_audit_review_response.py",
        "scripts/build_leakage_prescore_artifact_work_order.py",
        "scripts/build_leakage_prescore_artifact_collection_package.py",
        "scripts/run_leakage_prescore_artifact_collection_intake.py",
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
        "activated_scoring_rows_v08.csv",
        "scoring_observed_inputs_v08.csv",
        "family_prediction_tables_v08.csv",
        "numeric_parameter_count_table_v08.csv",
        "control_runner_outputs_v08.csv",
        "numeric_decision_thresholds_v08.csv",
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in requirements)
    assert all(row["current_status"].startswith("BLOCKED") for row in requirements)

    components = list(csv.DictReader((ROOT / "data/derived/scoring_formula_components_v07.csv").open()))
    assert len(components) == 7
    assert all(row["formula_policy_status"] == "READY_AS_POLICY_NOT_RUN" for row in components)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in components)

    summary = list(csv.DictReader((ROOT / "data/derived/scoring_preflight_summary_v07.csv").open()))
    assert summary == [
        {
            "summary_id": "SCORING_PREFLIGHT_V07",
            "readiness_dependency": "ENDPOINT_SCORING_BLOCKED",
            "blocked_scoring_requirements": "6",
            "formula_policy_components_ready": "7",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_NOT_READY",
            "next_required_artifact": "source_import_and_leakage_audit_v09.csv",
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
    assert all(row["leakage_audit_status"] == "LEAKAGE_AUDIT_PENDING_REVIEW_SOURCE_PRESENT" for row in audit)
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
    assert all(row["leakage_status"] == "LEAKAGE_AUDIT_PENDING_REVIEW_SOURCE_PRESENT" for row in findings)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_leakage_summary_v09.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_LEAKAGE_AUDIT_V09",
            "audited_rows": "18",
            "source_import_pending_rows": "0",
            "leakage_pass_rows": "0",
            "activated_rows": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_READY_LEAKAGE_PENDING",
            "next_required_artifact": "leakage_audit_evidence_v10.csv",
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


def test_v63_leakage_prescore_artifact_collection_intake_is_blocked_without_response() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_collection_intake_v63.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/leakage_prescore_artifact_collection_intake_summary_v63.csv").open())
    )
    assert len(rows) == 72
    assert len({row["galaxy_id"] for row in rows}) == 18
    assert {row["evidence_id"] for row in rows} == {
        "LEC10_SOURCE_ROUTE",
        "LEC10_OBSERVED_INPUTS",
        "LEC10_MORPH_LABELS",
        "LEC10_BENCHMARK_INPUTS",
    }
    assert all(row["source_mode"] == "template_absent_completed_response" for row in rows)
    assert all(row["intake_decision"] == "BLOCKED_COMPLETED_PRESCORE_ARTIFACT_RESPONSE_ABSENT" for row in rows)
    assert all(row["leakage_evidence_candidate_status"] == "NOT_CANDIDATE_COMPLETED_RESPONSE_ABSENT" for row in rows)
    assert all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in rows)
    assert all(row["may_activate_row_after_ingestion"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    assert summary == [
        {
            "summary_id": "LEAKAGE_PRESCORE_ARTIFACT_COLLECTION_INTAKE_V63",
            "expected_response_zip": "review_packages/leakage_prescore_artifact_v61_completed_collection_response.zip",
            "expected_response_files_present": "0",
            "intake_rows": "72",
            "galaxies_covered": "18",
            "evidence_checks_per_galaxy": "4",
            "completed_response_present": "false",
            "candidate_rows_for_later_leakage_evidence": "0",
            "blocked_or_missing_rows": "72",
            "leakage_evidence_rows_created": "0",
            "activation_rows_authorized": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PRESCORE_ARTIFACT_RESPONSE_BLOCKED_OR_ABSENT",
            "next_required_artifact": "review_packages/leakage_prescore_artifact_v61_completed_collection_response.zip",
            "claim_boundary": "leakage_prescore_artifact_collection_intake_only_no_evidence_no_scores_no_dark_sector_verdict",
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
    assert all(row["activation_decision"] == "DO_NOT_ACTIVATE" for row in gates)
    assert all("real_source_values_missing" not in row["blocking_requirements"] for row in gates)
    assert all("leakage_audit_not_passed" in row["blocking_requirements"] for row in gates)
    assert all("source_row_not_activated" in row["blocking_requirements"] for row in gates)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in gates)

    blockers = list(csv.DictReader((ROOT / "data/derived/scoring_activation_global_blockers_v13.csv").open()))
    assert {row["blocker_id"] for row in blockers} == {
        "SAG13_FAMILY_FORMULA_TABLES",
        "SAG13_PARAMETER_COUNTS",
        "SAG13_CONTROL_RUNNERS",
        "SAG13_DECISION_THRESHOLDS",
    }
    assert all(row["current_status"] == "BLOCKED" for row in blockers)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in blockers)

    summary = list(csv.DictReader((ROOT / "data/derived/scoring_activation_summary_v13.csv").open()))
    assert summary == [
        {
            "summary_id": "SCORING_ACTIVATION_GATE_V13",
            "candidate_rows": "18",
            "rows_activated_for_scoring": "0",
            "row_level_blocked_rows": "18",
            "global_blockers": "4",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_ACTIVATION_BLOCKED",
            "next_required_artifact": "data/derived/source_import_leakage_summary_v09.csv",
            "claim_boundary": "activation_gate_only_no_dark_sector_verdict",
        }
    ]


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
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert any(row["upstream_status"] == "PROVENANCE_PROMOTION_READY_NOT_IMPORTED" for row in rows)
    assert any(row["upstream_status"] == "SCORING_ACTIVATION_BLOCKED" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/scoring_dependency_closure_summary_v24.csv").open()))
    assert summary == [
        {
            "summary_id": "SCORING_DEPENDENCY_CLOSURE_V24",
            "dependencies_checked": "13",
            "ready_dependencies": "7",
            "blocked_dependencies": "6",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_DEPENDENCY_CLOSURE_BLOCKED",
            "next_required_artifact": "leakage_audit_evidence_v10.csv",
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
    }
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    frontier = [row for row in rows if row["frontier_now"] == "true"]
    assert len(frontier) == 1
    assert frontier[0]["dependency_id"] == "SCD24_LEAKAGE_AUDIT"
    assert frontier[0]["next_required_artifact"] == "leakage_audit_evidence_v10.csv"

    summary = list(csv.DictReader((ROOT / "data/derived/scoring_unblock_priority_summary_v25.csv").open()))
    assert summary == [
        {
            "summary_id": "SCORING_UNBLOCK_PRIORITY_V25",
            "priority_rows": "13",
            "blocked_priority_rows": "6",
            "frontier_now_rows": "1",
            "first_frontier_dependency": "SCD24_LEAKAGE_AUDIT",
            "first_frontier_artifact": "leakage_audit_evidence_v10.csv",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_UNBLOCK_FRONTIER_IDENTIFIED",
            "claim_boundary": "scoring_unblock_priority_only_no_scores_no_dark_sector_verdict",
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
    assert all(row["v09_leakage_status"] == "LEAKAGE_AUDIT_PENDING_REVIEW_SOURCE_PRESENT" for row in rows)
    assert all(row["rows_passing_value_gate_after_recheck"] == "1" for row in rows)
    assert all("post_writer_real_values_gate_not_passed" not in row["leakage_recheck_blockers"] for row in rows)
    assert all("v09_leakage_audit_not_passed" in row["leakage_recheck_blockers"] for row in rows)
    assert all(row["leakage_pass_after_recheck"] == "false" for row in rows)
    assert all(row["activation_allowed_after_recheck"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_leakage_audit_recheck_summary_v37.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_LEAKAGE_AUDIT_RECHECK_V37",
            "leakage_recheck_rows": "18",
            "leakage_pass_rows_after_recheck": "0",
            "leakage_blocked_rows_after_recheck": "18",
            "activation_allowed_rows_after_recheck": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_LEAKAGE_AUDIT_RECHECK_BLOCKED",
            "claim_boundary": "post_writer_leakage_audit_recheck_only_no_activation_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v38_post_writer_scoring_activation_recheck_blocks_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_scoring_activation_recheck_v38.csv").open()))
    assert len(rows) == 18
    assert all(row["v37_leakage_pass_after_recheck"] == "false" for row in rows)
    assert all(row["v37_activation_allowed_after_recheck"] == "false" for row in rows)
    assert all(row["v13_activation_decision"] == "DO_NOT_ACTIVATE" for row in rows)
    assert all("post_writer_leakage_audit_not_passed" in row["activation_recheck_blockers"] for row in rows)
    assert all("post_writer_leakage_recheck_disallows_activation" in row["activation_recheck_blockers"] for row in rows)
    assert all("v13_activation_gate_not_passed" in row["activation_recheck_blockers"] for row in rows)
    assert all(row["activation_decision_after_recheck"] == "DO_NOT_ACTIVATE" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_scoring_activation_recheck_summary_v38.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_SCORING_ACTIVATION_RECHECK_V38",
            "activation_recheck_rows": "18",
            "rows_activated_after_recheck": "0",
            "row_level_blocked_rows_after_recheck": "18",
            "global_blockers_after_recheck": "4",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_SCORING_ACTIVATION_RECHECK_BLOCKED",
            "claim_boundary": "post_writer_scoring_activation_recheck_only_no_activation_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v39_post_writer_scoring_preflight_recheck_blocks_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_scoring_preflight_recheck_v39.csv").open()))
    assert len(rows) == 6
    assert all(row["v07_current_status"].startswith("BLOCKED") for row in rows)
    assert all(row["v38_rows_activated_after_recheck"] == "0" for row in rows)
    assert all("v07_requirement_blocked" in row["preflight_recheck_blockers"] for row in rows)
    assert all("post_writer_activation_recheck_zero_rows" in row["preflight_recheck_blockers"] for row in rows)
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
    assert sum(row["v24_dependency_decision"] == "READY" for row in rows) == 7
    assert sum(row["v24_dependency_decision"] == "BLOCKED" for row in rows) == 6
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
    assert all(
        ("v25_priority_dependency_blocked" in row["priority_recheck_blockers"])
        == (row["v25_frontier_now"] != "false" or int(row["priority_rank"]) >= 8)
        for row in rows
    )
    assert all("post_writer_dependency_recheck_zero_ready_dependencies" in row["priority_recheck_blockers"] for row in rows)
    assert all("post_writer_dependency_recheck_scoring_not_allowed" in row["priority_recheck_blockers"] for row in rows)
    assert sum(row["frontier_now_after_recheck"] == "true" for row in rows) == 1
    frontier = [row for row in rows if row["frontier_now_after_recheck"] == "true"][0]
    assert frontier["dependency_id"] == "SCD24_LEAKAGE_AUDIT"
    assert frontier["next_required_artifact"] == "leakage_audit_evidence_v10.csv"
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/post_writer_scoring_unblock_priority_recheck_summary_v41.csv").open()))
    assert summary == [
        {
            "summary_id": "POST_WRITER_SCORING_UNBLOCK_PRIORITY_RECHECK_V41",
            "priority_rows_rechecked": "13",
            "blocked_priority_rows_after_recheck": "13",
            "frontier_now_rows_after_recheck": "1",
            "first_frontier_dependency_after_recheck": "SCD24_LEAKAGE_AUDIT",
            "first_frontier_artifact_after_recheck": "leakage_audit_evidence_v10.csv",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_SCORING_UNBLOCK_FRONTIER_CONFIRMED",
            "claim_boundary": "post_writer_scoring_unblock_priority_recheck_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v42_post_writer_frontier_evidence_acceptance_recheck_blocks_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/post_writer_frontier_evidence_acceptance_recheck_v42.csv").open()))
    assert len(rows) == 18
    assert all(row["v41_frontier_dependency"] == "SCD24_LEAKAGE_AUDIT" for row in rows)
    assert all(row["v41_frontier_artifact"] == "leakage_audit_evidence_v10.csv" for row in rows)
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
