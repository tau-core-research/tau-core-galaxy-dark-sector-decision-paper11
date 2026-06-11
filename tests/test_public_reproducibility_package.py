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
        "docs/source_import_values_v11.md",
        "docs/source_import_real_values_gate_v12.md",
        "docs/scoring_activation_gate_v13.md",
        "docs/source_import_real_values_template_v14.md",
        "docs/source_import_raw_adapter_v15.md",
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
        "scripts/run_readiness_audit.py",
        "scripts/run_scoring_preflight.py",
        "scripts/build_scoring_input_scaffold.py",
        "scripts/run_source_import_leakage_audit.py",
        "scripts/build_source_import_contract.py",
        "scripts/build_source_import_values.py",
        "scripts/run_source_import_real_values_gate.py",
        "scripts/run_scoring_activation_gate.py",
        "scripts/build_source_import_real_values_template.py",
        "scripts/run_source_import_raw_adapter.py",
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
    assert all(row["source_import_status"] == "VALUE_REQUIRED_NOT_FILLED" for row in audit)
    assert all(row["leakage_audit_status"] == "LEAKAGE_AUDIT_NOT_RUN_SOURCE_MISSING" for row in audit)
    assert all(row["activation_decision"] == "DO_NOT_ACTIVATE" for row in audit)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in audit)

    requirements = list(csv.DictReader((ROOT / "data/derived/source_import_requirements_v09.csv").open()))
    assert {row["required_artifact"] for row in requirements} == {
        "data/input/source_import_real_values_v12.csv",
        "scoring_observed_inputs_v10.csv",
        "leakage_audit_evidence_v10.csv",
        "activated_scoring_rows_v10.csv",
    }
    assert {row["current_status"] for row in requirements} == {"PENDING", "REAL_VALUE_GATE_PRESENT_INPUT_MISSING"}
    assert all(row["endpoint_scoring_allowed"] == "false" for row in requirements)

    findings = list(csv.DictReader((ROOT / "data/derived/leakage_audit_findings_v09.csv").open()))
    assert len(findings) == 18
    assert all(row["leakage_status"] == "LEAKAGE_AUDIT_NOT_RUN_SOURCE_MISSING" for row in findings)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_leakage_summary_v09.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_LEAKAGE_AUDIT_V09",
            "audited_rows": "18",
            "source_import_pending_rows": "18",
            "leakage_pass_rows": "0",
            "activated_rows": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_AND_LEAKAGE_BLOCKED",
            "next_required_artifact": "source_import_real_values_v12.csv",
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
    assert all(row["input_file_status"] == "REAL_VALUE_FILE_MISSING" for row in gates)
    assert all(row["imported_numeric_rows"] == "0" for row in gates)
    assert all(row["real_value_gate_status"] == "REAL_VALUE_FILE_MISSING" for row in gates)
    assert all(row["activation_decision"] == "DO_NOT_ACTIVATE" for row in gates)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in gates)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_real_values_summary_v12.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_REAL_VALUES_GATE_V12",
            "expected_galaxy_rows": "18",
            "galaxies_with_imported_rows": "0",
            "imported_numeric_rows": "0",
            "rows_passing_value_gate": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_REAL_VALUES_BLOCKED",
            "next_required_artifact": "data/input/source_import_real_values_v12.csv",
            "claim_boundary": "real_value_import_gate_only_no_dark_sector_verdict",
        }
    ]


def test_v13_scoring_activation_gate_blocks_all_rows() -> None:
    gates = list(csv.DictReader((ROOT / "data/derived/scoring_activation_gate_v13.csv").open()))
    assert len(gates) == 18
    assert all(row["activation_decision"] == "DO_NOT_ACTIVATE" for row in gates)
    assert all("real_source_values_missing" in row["blocking_requirements"] for row in gates)
    assert all("leakage_audit_not_passed" in row["blocking_requirements"] for row in gates)
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
            "next_required_artifact": "data/input/source_import_real_values_v12.csv",
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
            "real_input_file_present": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_TEMPLATE_READY_NOT_DATA",
            "claim_boundary": "template_only_no_source_import_no_scores",
        }
    ]


def test_v15_raw_adapter_is_ready_but_has_no_raw_input() -> None:
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
            "raw_input_status": "RAW_INPUT_FILE_MISSING",
            "raw_rows_seen": "0",
            "valid_raw_rows": "0",
            "galaxies_with_valid_raw_rows": "0",
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
            "raw_input_status": "RAW_INPUT_FILE_MISSING",
            "target_input_file_present": "false",
            "target_file_written_by_adapter": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "RAW_ADAPTER_READY_INPUT_MISSING",
            "claim_boundary": "raw_adapter_only_no_source_import_no_scores",
        }
    ]


def test_v16_write_authorization_blocks_target_input_creation() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/source_import_write_authorization_v16.csv").open()))
    assert rows == [
        {
            "authorization_id": "SIWA16_WRITE_V12",
            "source_adapter_gate": "source_import_raw_adapter_gate_v15.csv",
            "target_input_file": "data/input/source_import_real_values_v12.csv",
            "explicit_write_authorization": "false",
            "raw_input_status": "RAW_INPUT_FILE_MISSING",
            "target_input_file_present": "false",
            "write_authorized": "false",
            "write_blockers": "explicit_write_authorization_missing;raw_input_not_validated",
            "target_file_written": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "write_authorization_only_no_source_import_no_scores",
        }
    ]

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_write_authorization_summary_v16.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_WRITE_AUTHORIZATION_V16",
            "write_authorized": "false",
            "target_file_written": "false",
            "target_input_file_present": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "WRITE_AUTHORIZATION_BLOCKED",
            "next_required_artifact": "data/input/source_import_raw_sparc_like_v15.csv",
            "claim_boundary": "write_authorization_only_no_source_import_no_scores",
        }
    ]


def test_v17_authorized_writer_is_implemented_but_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/source_import_authorized_writer_v17.csv").open()))
    assert rows == [
        {
            "writer_id": "SIAW17_AUTHORIZED_RAW_TO_V12",
            "authorization_source": "source_import_write_authorization_v16.csv",
            "raw_input_file": "data/input/source_import_raw_sparc_like_v15.csv",
            "target_input_file": "data/input/source_import_real_values_v12.csv",
            "write_authorized": "false",
            "raw_input_present": "false",
            "target_preexisting": "false",
            "target_file_written": "false",
            "rows_written": "0",
            "writer_status": "WRITER_BLOCKED_BY_AUTHORIZATION",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "authorized_writer_only_no_scores_no_verdict",
        }
    ]

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_authorized_writer_summary_v17.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_AUTHORIZED_WRITER_V17",
            "writer_status": "WRITER_BLOCKED_BY_AUTHORIZATION",
            "target_file_written": "false",
            "rows_written": "0",
            "target_input_file_present_after_writer": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "AUTHORIZED_WRITER_BLOCKED",
            "next_required_artifact": "data/input/source_import_raw_sparc_like_v15.csv",
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
            "raw_input_file_present": "false",
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


def test_v20_source_import_provenance_audit_blocks_raw_import() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_audit_v20.csv").open()))
    assert len(rows) == 18
    assert all(row["provenance_complete"] == "false" for row in rows)
    assert all(row["raw_import_decision"] == "DO_NOT_IMPORT_RAW" for row in rows)
    assert all("catalog_provenance_missing" in row["blocking_requirements"] for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_audit_summary_v20.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_AUDIT_V20",
            "audited_rows": "18",
            "provenance_complete_rows": "0",
            "raw_import_allowed_rows": "0",
            "raw_import_blocked_rows": "18",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "RAW_IMPORT_BLOCKED_BY_PROVENANCE",
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
            "evidence_input_file_present": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PROVENANCE_TEMPLATE_READY_NOT_DATA",
            "claim_boundary": "provenance_template_only_no_source_import_no_scores",
        }
    ]


def test_v22_source_import_provenance_evidence_gate_blocks_promotion() -> None:
    gate = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_evidence_gate_v22.csv").open()))
    assert gate == [
        {
            "evidence_gate_id": "SIPEG22_EVIDENCE_TO_PROVENANCE",
            "evidence_input_file": "data/input/source_import_provenance_evidence_v21.csv",
            "provenance_manifest": "data/derived/source_import_provenance_manifest_v19.csv",
            "evidence_input_status": "EVIDENCE_INPUT_FILE_MISSING",
            "evidence_rows_seen": "0",
            "valid_evidence_rows": "0",
            "galaxies_with_valid_evidence": "0",
            "provenance_promotion_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "provenance_evidence_gate_only_no_promotion_no_scores",
        }
    ]

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_evidence_gate_summary_v22.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_EVIDENCE_GATE_V22",
            "evidence_input_status": "EVIDENCE_INPUT_FILE_MISSING",
            "evidence_rows_seen": "0",
            "valid_evidence_rows": "0",
            "galaxies_with_valid_evidence": "0",
            "provenance_promotion_allowed": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PROVENANCE_EVIDENCE_INPUT_MISSING",
            "next_required_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "claim_boundary": "provenance_evidence_gate_only_no_source_import_no_scores",
        }
    ]


def test_v23_source_import_provenance_promotion_gate_blocks_manifest_promotion() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_promotion_gate_v23.csv").open()))
    assert len(rows) == 18
    assert all(row["v22_provenance_promotion_allowed"] == "false" for row in rows)
    assert all(row["promotion_allowed"] == "false" for row in rows)
    assert all(row["promotion_decision"] == "DO_NOT_PROMOTE_PROVENANCE" for row in rows)
    assert all("provenance_evidence_gate_not_allowed" in row["promotion_blockers"] for row in rows)
    assert all(row["provenance_rows_promoted"] == "0" for row in rows)
    assert all(row["raw_import_allowed_after_promotion"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/source_import_provenance_promotion_summary_v23.csv").open()))
    assert summary == [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_PROMOTION_GATE_V23",
            "candidate_rows": "18",
            "promotion_allowed_rows": "0",
            "promotion_blocked_rows": "18",
            "provenance_rows_promoted": "0",
            "raw_import_allowed_rows_after_promotion": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PROVENANCE_PROMOTION_BLOCKED",
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
    assert all(row["dependency_decision"] == "BLOCKED" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert any(row["upstream_status"] == "PROVENANCE_PROMOTION_BLOCKED" for row in rows)
    assert any(row["upstream_status"] == "SCORING_ACTIVATION_BLOCKED" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/scoring_dependency_closure_summary_v24.csv").open()))
    assert summary == [
        {
            "summary_id": "SCORING_DEPENDENCY_CLOSURE_V24",
            "dependencies_checked": "13",
            "ready_dependencies": "0",
            "blocked_dependencies": "13",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_DEPENDENCY_CLOSURE_BLOCKED",
            "next_required_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "claim_boundary": "scoring_dependency_closure_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v25_scoring_unblock_priority_identifies_first_frontier() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/scoring_unblock_priority_v25.csv").open()))
    assert len(rows) == 13
    assert [row["priority_rank"] for row in rows] == [str(i) for i in range(1, 14)]
    assert all(row["dependency_decision"] == "BLOCKED" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    frontier = [row for row in rows if row["frontier_now"] == "true"]
    assert len(frontier) == 1
    assert frontier[0]["dependency_id"] == "SCD24_PROVENANCE_EVIDENCE"
    assert frontier[0]["next_required_artifact"] == "data/input/source_import_provenance_evidence_v21.csv"

    summary = list(csv.DictReader((ROOT / "data/derived/scoring_unblock_priority_summary_v25.csv").open()))
    assert summary == [
        {
            "summary_id": "SCORING_UNBLOCK_PRIORITY_V25",
            "priority_rows": "13",
            "blocked_priority_rows": "13",
            "frontier_now_rows": "1",
            "first_frontier_dependency": "SCD24_PROVENANCE_EVIDENCE",
            "first_frontier_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_UNBLOCK_FRONTIER_IDENTIFIED",
            "claim_boundary": "scoring_unblock_priority_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v26_frontier_provenance_evidence_acceptance_waits_for_input() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_acceptance_v26.csv").open()))
    assert len(rows) == 18
    assert all(row["frontier_dependency"] == "SCD24_PROVENANCE_EVIDENCE" for row in rows)
    assert all(row["frontier_artifact"] == "data/input/source_import_provenance_evidence_v21.csv" for row in rows)
    assert all(row["evidence_input_present"] == "false" for row in rows)
    assert all(row["missing_or_placeholder_fields"] == "input_row_missing" for row in rows)
    assert all(row["acceptance_status"] == "PENDING_INPUT" for row in rows)
    assert all(row["accepted_for_promotion_review"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    summary = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_acceptance_summary_v26.csv").open()))
    assert summary == [
        {
            "summary_id": "FRONTIER_PROVENANCE_EVIDENCE_ACCEPTANCE_V26",
            "frontier_dependency": "SCD24_PROVENANCE_EVIDENCE",
            "frontier_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "candidate_rows": "18",
            "evidence_input_rows_present": "0",
            "accepted_for_promotion_review_rows": "0",
            "blocked_rows": "18",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_ACCEPTANCE_PENDING_INPUT",
            "claim_boundary": "frontier_evidence_acceptance_only_no_scores_no_dark_sector_verdict",
        }
    ]


def test_v27_frontier_provenance_evidence_work_order_stays_open() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/frontier_provenance_evidence_work_order_v27.csv").open()))
    assert len(rows) == 18
    assert all(row["frontier_dependency"] == "SCD24_PROVENANCE_EVIDENCE" for row in rows)
    assert all(row["target_evidence_artifact"] == "data/input/source_import_provenance_evidence_v21.csv" for row in rows)
    assert all(row["current_acceptance_status"] == "PENDING_INPUT" for row in rows)
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
    assert all(row["accepted_for_promotion_review"] == "false" for row in rows)
    assert all(row["work_order_status"] == "OPEN_EVIDENCE_COLLECTION_REQUIRED" for row in rows)
    assert all("work_order_open" in row["completion_blockers"] for row in rows)
    assert all("not_accepted_for_promotion_review" in row["completion_blockers"] for row in rows)
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


def test_arxiv_zip_is_source_only_if_present() -> None:
    zip_path = ROOT / "arxiv_submission_source.zip"
    if not zip_path.exists():
        return
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "main.pdf" not in names
