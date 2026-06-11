#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_model_families() -> None:
    rows = read_csv(ROOT / "data/source_manifest/model_family_decision_protocol.csv")
    ids = {row["family_id"] for row in rows}
    require(ids == {"M0", "M1", "M2"}, f"unexpected model families: {ids}")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "endpoint scoring must be disabled")
        require("claim" not in row["current_status"].lower(), "status must not be a claim")


def validate_freeze_requirements() -> None:
    rows = read_csv(ROOT / "data/source_manifest/policy_bundle_freeze_requirements.csv")
    require(len(rows) == 9, "expected nine policy-bundle requirements")
    for row in rows:
        require(row["required_before_endpoint"] == "true", f"{row['requirement_id']} must freeze before endpoint")
        forbidden = row["endpoint_forbidden_inputs"]
        require("endpoint" in forbidden or "rotation_residual" in forbidden, "missing forbidden endpoint inputs")


def validate_outcomes() -> None:
    rows = read_csv(ROOT / "data/source_manifest/decision_outcome_ladder.csv")
    ids = {row["outcome_id"] for row in rows}
    require(ids == {"O0", "O1", "O2", "O3", "O4"}, f"unexpected outcomes: {ids}")
    forbidden_joined = " ".join(row["forbidden_interpretation"] for row in rows).lower()
    require("global dark matter rejection" in forbidden_joined, "missing no-global-rejection guard")


def validate_policy_bundle_instance() -> None:
    rows = read_csv(ROOT / "data/source_manifest/frozen_policy_bundle_instance_v01.csv")
    require(len(rows) == 9, "expected nine frozen policy-bundle component references")
    components = {row["component"] for row in rows}
    require("delta_M_extraction_freeze" in components, "missing delta_M extraction freeze")
    require("ChannelHandoff_policy" in components, "missing channel handoff policy")
    for row in rows:
        require(row["bundle_id"] == "PB11_v01", "unexpected bundle id")
        require(row["endpoint_scoring_allowed"] == "false", "policy bundle cannot allow endpoint scoring")
        require(row["missing_content"], f"{row['component']} must list missing content")


def validate_galaxy_endpoint_manifest() -> None:
    rows = read_csv(ROOT / "data/source_manifest/galaxy_decision_endpoint_manifest_v01.csv")
    ids = {row["endpoint_id"] for row in rows}
    required = {
        "E11_SCOPE",
        "E11_SAMPLE_TRAIN",
        "E11_SAMPLE_HELDOUT",
        "E11_SCORE",
        "E11_CONTROL_WRONG_FAMILY",
        "E11_CONTROL_SHUFFLE",
        "E11_ZONE",
        "E11_VERDICT",
    }
    require(ids == required, f"unexpected endpoint manifest ids: {ids}")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "endpoint manifest v01 must disable scoring")
        require(row["required_before_scoring"] == "true", f"{row['endpoint_id']} must precede scoring")
        require(row["allowed_model_families"] == "M0;M1;M2", "all families must share the endpoint manifest")


def validate_sample_freeze() -> None:
    rows = read_csv(ROOT / "data/source_manifest/galaxy_sample_freeze_v01.csv")
    ids = {row["sample_id"] for row in rows}
    require(ids == {"GS_SCOPE", "GS_TRAIN", "GS_HELDOUT", "GS_CHALLENGE", "GS_EXCLUSION"}, "bad sample freeze ids")
    for row in rows:
        require(row["required_before_scoring"] == "true", f"{row['sample_id']} must precede scoring")
        require(row["endpoint_scoring_allowed"] == "false", "sample v01 must disable endpoint scoring")
        require(row["forbidden_inputs"], f"{row['sample_id']} missing forbidden inputs")


def validate_scoring_freeze() -> None:
    rows = read_csv(ROOT / "data/source_manifest/scoring_rule_freeze_v01.csv")
    ids = {row["score_id"] for row in rows}
    required = {"SC_FULL_CURVE", "SC_ZONE_INNER", "SC_ZONE_FLAT", "SC_HELDOUT", "SC_PARSIMONY", "SC_CONTROL"}
    require(ids == required, f"bad scoring ids: {ids}")
    for row in rows:
        require(row["required_before_scoring"] == "true", f"{row['score_id']} must precede scoring")
        require(row["endpoint_scoring_allowed"] == "false", "scoring v01 must disable endpoint scoring")
        require("PENDING" in row["current_status"], "v01 scoring must remain formula-pending")


def validate_controls() -> None:
    rows = read_csv(ROOT / "data/source_manifest/control_manifest_v01.csv")
    ids = {row["control_id"] for row in rows}
    required = {"CTRL_SHUFFLE", "CTRL_WRONG_FAMILY", "CTRL_NULL_SOURCE", "CTRL_LEAKAGE", "CTRL_RADIAL_PERMUTE"}
    require(ids == required, f"bad control ids: {ids}")
    for row in rows:
        require(row["required_before_scoring"] == "true", f"{row['control_id']} must precede scoring")
        require(row["endpoint_scoring_allowed"] == "false", "controls v01 must disable endpoint scoring")
        require("IMPLEMENTATION_PENDING" in row["current_status"], "controls must remain implementation-pending")


def validate_thresholds() -> None:
    rows = read_csv(ROOT / "data/source_manifest/decision_threshold_v01.csv")
    labels = {row["verdict_label"] for row in rows}
    required = {"M0_SUFFICIENT", "M1_FAVORED", "M2_BENCHMARK_STRONGER", "UNRESOLVED"}
    require(labels == required, f"bad verdict labels: {labels}")
    forbidden = " ".join(row["forbidden_interpretation"] for row in rows).lower()
    require("global dark matter rejection" in forbidden, "thresholds must block global no-DM claim")
    require("physical tau dark-sector field" in forbidden, "thresholds must block physical-field promotion")
    for row in rows:
        require("NUMERIC_CUTOFF_PENDING" in row["current_status"], "numeric cutoffs must remain pending")


def validate_galaxy_list_v02() -> None:
    rows = read_csv(ROOT / "data/source_manifest/galaxy_list_freeze_v02.csv")
    galaxies = {row["galaxy_id"] for row in rows}
    required = {"NGC4559", "NGC4010", "NGC5585", "UGC06930", "NGC4183", "NGC4088", "UGC12506"}
    require(required.issubset(galaxies), f"v02 galaxy role list missing required rows: {required - galaxies}")
    roles = {row["decision_role"] for row in rows}
    require("train_formula_candidate" in roles, "v02 list missing train role")
    require("challenge_high_spin_edge_on" in roles, "v02 list missing high-spin challenge role")
    require("beta_closure_transfer_candidate" in roles, "v02 list missing beta transfer role")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "v02 galaxy list must disable endpoint scoring")
        require("NOT_ACTIVE" in row["scoring_activation_status"], "v02 galaxy rows must remain inactive")
        require("family_winner" in row["forbidden_inputs"], "v02 galaxy rows must forbid family-winner leakage")


def validate_scoring_formula_v02() -> None:
    rows = read_csv(ROOT / "data/source_manifest/scoring_formula_freeze_v02.csv")
    ids = {row["formula_id"] for row in rows}
    required = {
        "SF02_FULL_CURVE",
        "SF02_INNER_ZONE",
        "SF02_OUTER_ZONE",
        "SF02_PARSIMONY",
        "SF02_GALAXY_SCORE",
        "SF02_HELDOUT",
        "SF02_CONTROL_VETO",
    }
    require(ids == required, f"bad v02 scoring formula ids: {ids}")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "v02 scoring formula must disable endpoint scoring")
        require("FORMULA_POLICY_FROZEN_NOT_RUN" in row["current_status"], "v02 formulas must remain unrun")
        require(row["forbidden_inputs"], f"{row['formula_id']} missing forbidden inputs")


def validate_family_parameter_count_v03() -> None:
    rows = read_csv(ROOT / "data/source_manifest/family_parameter_count_freeze_v03.csv")
    families = {row["family_id"] for row in rows}
    require({"M0", "M1", "M2", "ALL"}.issubset(families), "v03 family-budget rows missing families")
    joined_policy = " ".join(row["parameter_count_policy"] for row in rows).lower()
    require("per-galaxy" in joined_policy, "v03 count rules must count per-galaxy adjustments")
    require("post-freeze" in joined_policy, "v03 count rules must count post-freeze switches")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "v03 parameter-count rows must disable scoring")
        require(
            row["numeric_count_status"] == "COUNT_RULE_FROZEN_NUMERIC_COUNT_PENDING",
            "v03 parameter counts must remain numeric-count pending",
        )
        require("family_winner" in row["forbidden_inputs"], "v03 count rows must forbid family-winner leakage")


def validate_control_implementation_v03() -> None:
    rows = read_csv(ROOT / "data/source_manifest/control_implementation_freeze_v03.csv")
    ids = {row["control_id"] for row in rows}
    required = {
        "CIF03_SHUFFLE",
        "CIF03_WRONG_FAMILY",
        "CIF03_NULL_SOURCE",
        "CIF03_LEAKAGE",
        "CIF03_RADIAL",
        "CIF03_PARITY",
    }
    require(ids == required, f"bad v03 control ids: {ids}")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "v03 controls must disable endpoint scoring")
        require("IMPLEMENTATION_POLICY_FROZEN_NOT_RUN" in row["current_status"], "v03 controls must remain unrun")
        require(row["pass_condition"], f"{row['control_id']} missing pass condition")
        require(row["verdict_effect"], f"{row['control_id']} missing verdict effect")


def validate_source_field_completeness_v04() -> None:
    rows = read_csv(ROOT / "data/source_manifest/source_field_completeness_v04.csv")
    fields = {row["required_field"] for row in rows}
    required = {
        "declared_radial_grid",
        "observed_velocity_and_uncertainty",
        "baryonic_rotation_components",
        "source_morphology_readout_label",
        "source_packet_leakage_audit",
    }
    require(required.issubset(fields), f"v04 source completeness missing fields: {required - fields}")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "v04 source fields must disable endpoint scoring")
        require("PENDING" in row["activation_status"], "v04 source fields must remain activation-pending")
        require(row["forbidden_inputs"], f"{row['field_id']} missing forbidden inputs")


def validate_family_formula_registry_v04() -> None:
    rows = read_csv(ROOT / "data/source_manifest/family_formula_registry_v04.csv")
    families = {row["family_id"] for row in rows}
    require({"M0", "M1", "M2", "ALL"}.issubset(families), "v04 registry missing model families")
    slots = {row["formula_slot"] for row in rows}
    require("tau_response_formula" in slots, "v04 registry missing Tau response slot")
    require("numeric_parameter_count_table" in slots, "v04 registry missing numeric parameter-count table")
    for row in rows:
        require(row["required_before_numeric_count"] == "true", f"{row['registry_id']} must precede numeric count")
        require(row["endpoint_scoring_allowed"] == "false", "v04 registry must disable endpoint scoring")
        require("PENDING" in row["numeric_count_status"], "v04 registry must remain pending")


def validate_control_runner_contract_v04() -> None:
    rows = read_csv(ROOT / "data/source_manifest/control_runner_contract_v04.csv")
    ids = {row["control_id"] for row in rows}
    required = {
        "CIF03_SHUFFLE",
        "CIF03_WRONG_FAMILY",
        "CIF03_NULL_SOURCE",
        "CIF03_LEAKAGE",
        "CIF03_RADIAL",
        "CIF03_PARITY",
    }
    require(ids == required, f"bad v04 runner control ids: {ids}")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "v04 control runners must disable endpoint scoring")
        require(row["execution_status"] == "RUNNER_CONTRACT_DECLARED_NOT_IMPLEMENTED", "v04 runners must be unimplemented")
        require(row["input_contract"], f"{row['runner_id']} missing input contract")
        require(row["output_contract"], f"{row['runner_id']} missing output contract")


def validate_source_row_audit_v05() -> None:
    rows = read_csv(ROOT / "data/source_manifest/source_row_audit_v05.csv")
    galaxy_rows = read_csv(ROOT / "data/source_manifest/galaxy_list_freeze_v02.csv")
    audited = {row["galaxy_id"] for row in rows}
    listed = {row["galaxy_id"] for row in galaxy_rows}
    require(audited == listed, f"v05 audit galaxy set mismatch: {listed ^ audited}")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "v05 row audit must disable endpoint scoring")
        require(row["activation_status"] == "ACTIVATION_BLOCKED", "v05 rows must remain activation-blocked")
        require("PENDING" in row["leakage_audit_status"], "v05 rows must keep leakage audit pending")
        require(row["blocking_reason"], f"{row['audit_id']} missing blocking reason")


def validate_family_formula_table_v05() -> None:
    rows = read_csv(ROOT / "data/source_manifest/family_formula_table_v05.csv")
    families = {row["family_id"] for row in rows}
    require({"M0", "M1", "M2", "ALL"}.issubset(families), "v05 formula table missing families")
    slots = {row["formula_slot"] for row in rows}
    require("tau_response_formula" in slots, "v05 formula table missing response slot")
    require("numeric_parameter_count_table" in slots, "v05 formula table missing count slot")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "v05 formula rows must disable endpoint scoring")
        require(row["formula_table_status"] == "FORMULA_TABLE_REQUIRED_NOT_FILLED", "v05 formula tables must remain unfilled")
        require("BLOCKED" in row["parameter_count_status"] or "PENDING" in row["parameter_count_status"], "v05 count status must be blocked or pending")


def validate_numeric_count_readiness_v05() -> None:
    rows = read_csv(ROOT / "data/source_manifest/numeric_count_readiness_v05.csv")
    families = {row["family_id"] for row in rows}
    require({"M0", "M1", "M2", "ALL"}.issubset(families), "v05 numeric readiness missing families")
    for row in rows:
        require(row["endpoint_scoring_allowed"] == "false", "v05 count rows must disable endpoint scoring")
        require(row["count_readiness_status"] == "COUNT_NOT_READY", "v05 counts must remain not ready")
        require(row["blocked_by"], f"{row['readiness_id']} missing blocker")
        require(row["minimum_completion_condition"], f"{row['readiness_id']} missing completion condition")


def validate_readiness_audit_v06() -> None:
    activation = read_csv(ROOT / "data/derived/activation_blockers_v06.csv")
    formula = read_csv(ROOT / "data/derived/formula_and_count_blockers_v06.csv")
    runners = read_csv(ROOT / "data/derived/control_runner_blockers_v06.csv")
    summary = read_csv(ROOT / "data/derived/readiness_summary_v06.csv")
    require(len(activation) == 18, "v06 activation audit must cover eighteen galaxy rows")
    require(all(row["activation_status"] == "ACTIVATION_BLOCKED" for row in activation), "v06 activation rows must be blocked")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in activation), "v06 activation cannot allow scoring")
    require(any(row["blocker_type"] == "formula_table" for row in formula), "v06 formula blockers missing")
    require(any(row["blocker_type"] == "numeric_count" for row in formula), "v06 numeric count blockers missing")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in formula), "v06 formula/count cannot allow scoring")
    require(len(runners) == 6, "v06 runner audit must cover six controls")
    require(
        all(row["execution_status"] == "RUNNER_CONTRACT_DECLARED_NOT_IMPLEMENTED" for row in runners),
        "v06 runners must remain unimplemented",
    )
    require(len(summary) == 1, "v06 readiness summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "ENDPOINT_SCORING_BLOCKED", "v06 readiness must block endpoint scoring")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v06 summary must forbid endpoint scoring")


def validate_scoring_preflight_v07() -> None:
    requirements = read_csv(ROOT / "data/derived/scoring_input_requirements_v07.csv")
    components = read_csv(ROOT / "data/derived/scoring_formula_components_v07.csv")
    summary = read_csv(ROOT / "data/derived/scoring_preflight_summary_v07.csv")
    required_artifacts = {row["required_artifact"] for row in requirements}
    require(
        required_artifacts
        == {
            "activated_scoring_rows_v08.csv",
            "scoring_observed_inputs_v08.csv",
            "family_prediction_tables_v08.csv",
            "numeric_parameter_count_table_v08.csv",
            "control_runner_outputs_v08.csv",
            "numeric_decision_thresholds_v08.csv",
        },
        f"v07 scoring requirements mismatch: {required_artifacts}",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in requirements), "v07 requirements cannot allow scoring")
    require(all(row["current_status"].startswith("BLOCKED") for row in requirements), "v07 requirements must remain blocked")
    require(len(components) == 7, "v07 must expose seven scoring formula components")
    require(all(row["formula_policy_status"] == "READY_AS_POLICY_NOT_RUN" for row in components), "v07 formulas must be policy-only")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in components), "v07 components cannot allow scoring")
    require(len(summary) == 1, "v07 scoring summary must have one row")
    row = summary[0]
    require(row["readiness_dependency"] == "ENDPOINT_SCORING_BLOCKED", "v07 must depend on blocked readiness")
    require(row["overall_status"] == "SCORING_NOT_READY", "v07 scoring must remain not ready")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v07 summary must forbid endpoint scoring")
    require(row["next_required_artifact"] == "source_import_and_leakage_audit_v09.csv", "v07 must point to v09 source import")


def validate_scoring_input_scaffold_v08() -> None:
    rows = read_csv(ROOT / "data/derived/activated_scoring_rows_v08.csv")
    schema = read_csv(ROOT / "data/derived/scoring_observed_input_schema_v08.csv")
    observed = read_csv(ROOT / "data/derived/scoring_observed_inputs_v08.csv")
    summary = read_csv(ROOT / "data/derived/scoring_input_scaffold_summary_v08.csv")
    require(len(rows) == 18, "v08 must declare eighteen scoring rows")
    require(all(row["activation_status"] == "NOT_ACTIVATED" for row in rows), "v08 must not activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v08 rows cannot allow scoring")
    fields = {row["field_name"] for row in schema}
    require({"galaxy_id", "radius_kpc", "v_obs_km_s", "sigma_v_km_s"}.issubset(fields), "v08 observed schema incomplete")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in schema), "v08 schema cannot allow scoring")
    require(len(observed) == 18, "v08 must provide one placeholder observed row per scoring row")
    require(all(row["v_obs_km_s"] == "PENDING_SOURCE_IMPORT" for row in observed), "v08 observed data must remain pending")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in observed), "v08 observed rows cannot allow scoring")
    require(len(summary) == 1, "v08 summary must have one row")
    row = summary[0]
    require(row["activated_rows"] == "0", "v08 must activate zero rows")
    require(row["observed_numeric_rows"] == "0", "v08 must import zero numeric observed rows")
    require(row["overall_status"] == "INPUT_SCAFFOLD_READY_DATA_MISSING", "v08 status must remain data-missing")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v08 summary must forbid scoring")


def validate_source_import_leakage_audit_v09() -> None:
    audit = read_csv(ROOT / "data/derived/source_import_and_leakage_audit_v09.csv")
    requirements = read_csv(ROOT / "data/derived/source_import_requirements_v09.csv")
    findings = read_csv(ROOT / "data/derived/leakage_audit_findings_v09.csv")
    summary = read_csv(ROOT / "data/derived/source_import_leakage_summary_v09.csv")
    require(len(audit) == 18, "v09 source/leakage audit must cover eighteen rows")
    require(
        all(
            row["source_import_status"]
            in {"SOURCE_IMPORT_PENDING", "SOURCE_ROUTE_REQUIRED_NOT_FILLED", "VALUE_REQUIRED_NOT_FILLED"}
            for row in audit
        ),
        "v09 source import must remain blocked",
    )
    require(all(row["leakage_audit_status"] == "LEAKAGE_AUDIT_NOT_RUN_SOURCE_MISSING" for row in audit), "v09 leakage cannot pass")
    require(all(row["activation_decision"] == "DO_NOT_ACTIVATE" for row in audit), "v09 must not activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in audit), "v09 audit cannot allow scoring")
    required_artifacts = {row["required_artifact"] for row in requirements}
    require(
        required_artifacts
        == {
            "data/input/source_import_real_values_v12.csv",
            "scoring_observed_inputs_v10.csv",
            "leakage_audit_evidence_v10.csv",
            "activated_scoring_rows_v10.csv",
        },
        f"v09 requirement mismatch: {required_artifacts}",
    )
    allowed_requirement_statuses = {
        "PENDING",
        "CONTRACT_PRESENT_VALUES_PENDING",
        "VALUES_LEDGER_PRESENT_VALUES_PENDING",
        "REAL_VALUE_GATE_PRESENT_INPUT_MISSING",
    }
    require(
        all(row["current_status"] in allowed_requirement_statuses for row in requirements),
        "v09 requirements must remain pending or contract-present",
    )
    require(len(findings) == 18, "v09 leakage findings must cover eighteen rows")
    require(all(row["leakage_status"] == "LEAKAGE_AUDIT_NOT_RUN_SOURCE_MISSING" for row in findings), "v09 findings cannot pass leakage")
    require(len(summary) == 1, "v09 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SOURCE_IMPORT_AND_LEAKAGE_BLOCKED", "v09 status must remain blocked")
    require(row["activated_rows"] == "0", "v09 must activate zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v09 summary must forbid scoring")
    require(row["next_required_artifact"] == "source_import_real_values_v12.csv", "v09 must point to real source import values")


def validate_source_import_contract_v10() -> None:
    source_rows = read_csv(ROOT / "data/derived/source_import_table_v10.csv")
    observed = read_csv(ROOT / "data/derived/observed_input_contract_v10.csv")
    leakage = read_csv(ROOT / "data/derived/leakage_evidence_contract_v10.csv")
    summary = read_csv(ROOT / "data/derived/source_import_contract_summary_v10.csv")
    require(len(source_rows) == 18, "v10 source import contract must cover eighteen rows")
    require(
        all(row["source_route_status"] == "SOURCE_ROUTE_REQUIRED_NOT_FILLED" for row in source_rows),
        "v10 source routes must remain unfilled",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in source_rows), "v10 source rows cannot allow scoring")
    fields = {row["field_name"] for row in observed}
    require({"radius_kpc", "v_obs_km_s", "sigma_v_km_s"}.issubset(fields), "v10 observed contract incomplete")
    require(
        all(row["source_import_status"] == "CONTRACT_DECLARED_VALUE_PENDING" for row in observed),
        "v10 observed contract values must remain pending",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in observed), "v10 observed contract cannot allow scoring")
    require(len(leakage) == 4, "v10 leakage contract must have four rows")
    require(all(row["status"] == "EVIDENCE_REQUIRED_NOT_FILLED" for row in leakage), "v10 leakage evidence must be unfilled")
    require(len(summary) == 1, "v10 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SOURCE_IMPORT_CONTRACT_READY_VALUES_MISSING", "v10 status must keep values missing")
    require(row["source_routes_filled"] == "0", "v10 must fill zero source routes")
    require(row["numeric_observed_rows_filled"] == "0", "v10 must fill zero numeric observed rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v10 summary must forbid scoring")


def validate_source_import_values_v11() -> None:
    source_rows = read_csv(ROOT / "data/derived/source_import_values_v11.csv")
    observed = read_csv(ROOT / "data/derived/observed_numeric_values_v11.csv")
    leakage = read_csv(ROOT / "data/derived/leakage_evidence_values_v11.csv")
    summary = read_csv(ROOT / "data/derived/source_import_values_summary_v11.csv")
    require(len(source_rows) == 18, "v11 source value ledger must cover eighteen rows")
    require(
        all(row["source_route_value_status"] == "VALUE_REQUIRED_NOT_FILLED" for row in source_rows),
        "v11 source route values must remain unfilled",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in source_rows), "v11 source values cannot allow scoring")
    require(len(observed) == 18, "v11 observed value ledger must cover eighteen rows")
    require(
        all(row["observed_value_status"] == "VALUE_REQUIRED_NOT_FILLED" for row in observed),
        "v11 observed values must remain unfilled",
    )
    require(all(row["v_obs_km_s"] == "VALUE_REQUIRED_NOT_FILLED" for row in observed), "v11 observed velocities must be unfilled")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in observed), "v11 observed values cannot allow scoring")
    require(len(leakage) == 4, "v11 leakage evidence ledger must have four rows")
    require(all(row["evidence_status"] == "VALUE_REQUIRED_NOT_FILLED" for row in leakage), "v11 leakage evidence must be unfilled")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in leakage), "v11 leakage values cannot allow scoring")
    require(len(summary) == 1, "v11 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SOURCE_IMPORT_VALUES_DECLARED_NOT_FILLED", "v11 status must keep values unfilled")
    require(row["source_routes_filled"] == "0", "v11 must fill zero source routes")
    require(row["observed_numeric_rows_filled"] == "0", "v11 must fill zero numeric observed rows")
    require(row["leakage_evidence_filled"] == "0", "v11 must fill zero leakage evidence rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v11 summary must forbid scoring")
    require(row["next_required_artifact"] == "source_import_real_values_v12.csv", "v11 must point to real value import")


def validate_source_import_real_values_gate_v12() -> None:
    schema = read_csv(ROOT / "data/derived/source_import_real_values_schema_v12.csv")
    gates = read_csv(ROOT / "data/derived/source_import_real_values_gate_v12.csv")
    summary = read_csv(ROOT / "data/derived/source_import_real_values_summary_v12.csv")
    fields = {row["field_name"] for row in schema}
    required = {
        "galaxy_id",
        "radial_index",
        "radius_kpc",
        "v_obs_km_s",
        "sigma_v_km_s",
        "v_gas_km_s",
        "v_disk_km_s",
        "source_route",
        "leakage_evidence_id",
        "import_status",
    }
    require(required.issubset(fields), f"v12 source import schema incomplete: {required - fields}")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in schema), "v12 schema cannot allow scoring")
    require(len(gates) == 18, "v12 real-value gate must cover eighteen scoring rows")
    require(all(row["input_file_status"] == "REAL_VALUE_FILE_MISSING" for row in gates), "v12 input file must remain absent in package")
    require(all(row["imported_numeric_rows"] == "0" for row in gates), "v12 must import zero numeric rows")
    require(all(row["real_value_gate_status"] == "REAL_VALUE_FILE_MISSING" for row in gates), "v12 gate must remain file-missing")
    require(all(row["activation_decision"] == "DO_NOT_ACTIVATE" for row in gates), "v12 must not activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in gates), "v12 gates cannot allow scoring")
    require(len(summary) == 1, "v12 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SOURCE_IMPORT_REAL_VALUES_BLOCKED", "v12 real-value import must remain blocked")
    require(row["expected_galaxy_rows"] == "18", "v12 summary must expect eighteen rows")
    require(row["galaxies_with_imported_rows"] == "0", "v12 must import zero galaxies")
    require(row["imported_numeric_rows"] == "0", "v12 must import zero numeric rows")
    require(row["rows_passing_value_gate"] == "0", "v12 must pass zero value gates")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v12 summary must forbid scoring")
    require(row["next_required_artifact"] == "data/input/source_import_real_values_v12.csv", "v12 must point to the input file")


def validate_scoring_activation_gate_v13() -> None:
    gates = read_csv(ROOT / "data/derived/scoring_activation_gate_v13.csv")
    blockers = read_csv(ROOT / "data/derived/scoring_activation_global_blockers_v13.csv")
    summary = read_csv(ROOT / "data/derived/scoring_activation_summary_v13.csv")
    require(len(gates) == 18, "v13 activation gate must cover eighteen rows")
    require(all(row["activation_decision"] == "DO_NOT_ACTIVATE" for row in gates), "v13 must activate zero rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in gates), "v13 row gates cannot allow scoring")
    require(all("real_source_values_missing" in row["blocking_requirements"] for row in gates), "v13 rows must be blocked by missing real values")
    require(all("leakage_audit_not_passed" in row["blocking_requirements"] for row in gates), "v13 rows must be blocked by leakage")
    require(len(blockers) == 4, "v13 must list four global blockers")
    require(all(row["current_status"] == "BLOCKED" for row in blockers), "v13 global blockers must remain blocked")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in blockers), "v13 blockers cannot allow scoring")
    require(len(summary) == 1, "v13 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SCORING_ACTIVATION_BLOCKED", "v13 activation must remain blocked")
    require(row["candidate_rows"] == "18", "v13 summary must cover eighteen candidate rows")
    require(row["rows_activated_for_scoring"] == "0", "v13 must activate zero rows")
    require(row["row_level_blocked_rows"] == "18", "v13 must block eighteen rows")
    require(row["global_blockers"] == "4", "v13 must report four global blockers")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v13 summary must forbid scoring")


def validate_source_import_template_v14() -> None:
    template = read_csv(ROOT / "data/input/source_import_real_values_v12_TEMPLATE.csv")
    columns = read_csv(ROOT / "data/derived/source_import_template_columns_v14.csv")
    summary = read_csv(ROOT / "data/derived/source_import_template_summary_v14.csv")
    require(len(template) == 18, "v14 template must include one placeholder row per candidate galaxy")
    require(all(row["import_status"] == "TEMPLATE_ROW_DO_NOT_IMPORT" for row in template), "v14 template rows must not be importable")
    require(len(columns) == 16, "v14 template must document sixteen required columns")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in columns), "v14 template columns cannot allow scoring")
    require(len(summary) == 1, "v14 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SOURCE_IMPORT_TEMPLATE_READY_NOT_DATA", "v14 must remain template-only")
    require(row["template_rows"] == "18", "v14 summary must report eighteen template rows")
    require(row["required_columns"] == "16", "v14 summary must report sixteen columns")
    require(row["real_input_file_present"] == "false", "v14 must not include the real input file")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v14 summary must forbid scoring")


def validate_source_import_raw_adapter_v15() -> None:
    schema = read_csv(ROOT / "data/derived/source_import_raw_adapter_schema_v15.csv")
    gate = read_csv(ROOT / "data/derived/source_import_raw_adapter_gate_v15.csv")
    summary = read_csv(ROOT / "data/derived/source_import_raw_adapter_summary_v15.csv")
    require(len(schema) == 16, "v15 raw adapter schema must map sixteen target fields")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in schema), "v15 schema cannot allow scoring")
    require(len(gate) == 1, "v15 raw adapter gate must have one row")
    gate_row = gate[0]
    require(gate_row["raw_input_status"] == "RAW_INPUT_FILE_MISSING", "v15 raw input must remain absent")
    require(gate_row["raw_rows_seen"] == "0", "v15 must see zero raw rows")
    require(gate_row["valid_raw_rows"] == "0", "v15 must validate zero raw rows")
    require(gate_row["target_file_written"] == "false", "v15 must not write the target input")
    require(gate_row["endpoint_scoring_allowed"] == "false", "v15 gate cannot allow scoring")
    require(len(summary) == 1, "v15 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "RAW_ADAPTER_READY_INPUT_MISSING", "v15 must remain raw-input missing")
    require(row["raw_input_status"] == "RAW_INPUT_FILE_MISSING", "v15 summary must report missing raw input")
    require(row["target_input_file_present"] == "false", "v15 target input must remain absent")
    require(row["target_file_written_by_adapter"] == "false", "v15 adapter must not write target file")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v15 summary must forbid scoring")


def validate_source_import_write_authorization_v16() -> None:
    rows = read_csv(ROOT / "data/derived/source_import_write_authorization_v16.csv")
    summary = read_csv(ROOT / "data/derived/source_import_write_authorization_summary_v16.csv")
    require(len(rows) == 1, "v16 write authorization must have one row")
    row = rows[0]
    require(row["explicit_write_authorization"] == "false", "v16 explicit write authorization must be absent")
    require(row["raw_input_status"] == "RAW_INPUT_FILE_MISSING", "v16 raw input must remain missing")
    require(row["target_input_file_present"] == "false", "v16 target input must remain absent")
    require(row["write_authorized"] == "false", "v16 write authorization must be blocked")
    require("explicit_write_authorization_missing" in row["write_blockers"], "v16 must require explicit authorization")
    require("raw_input_not_validated" in row["write_blockers"], "v16 must require validated raw input")
    require(row["target_file_written"] == "false", "v16 must not write target input")
    require(row["endpoint_scoring_allowed"] == "false", "v16 row cannot allow scoring")
    require(len(summary) == 1, "v16 summary must have one row")
    summary_row = summary[0]
    require(summary_row["overall_status"] == "WRITE_AUTHORIZATION_BLOCKED", "v16 write authorization must remain blocked")
    require(summary_row["write_authorized"] == "false", "v16 summary must block writing")
    require(summary_row["target_file_written"] == "false", "v16 summary must not write target file")
    require(summary_row["target_input_file_present"] == "false", "v16 summary must report absent target file")
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "v16 summary must forbid scoring")


def validate_source_import_authorized_writer_v17() -> None:
    rows = read_csv(ROOT / "data/derived/source_import_authorized_writer_v17.csv")
    summary = read_csv(ROOT / "data/derived/source_import_authorized_writer_summary_v17.csv")
    require(len(rows) == 1, "v17 authorized writer must have one row")
    row = rows[0]
    require(row["write_authorized"] == "false", "v17 write authorization must remain false")
    require(row["raw_input_present"] == "false", "v17 raw input must remain absent")
    require(row["target_preexisting"] == "false", "v17 target input must not preexist")
    require(row["target_file_written"] == "false", "v17 must not write target input")
    require(row["rows_written"] == "0", "v17 must write zero rows")
    require(row["writer_status"] == "WRITER_BLOCKED_BY_AUTHORIZATION", "v17 writer must be authorization-blocked")
    require(row["endpoint_scoring_allowed"] == "false", "v17 row cannot allow scoring")
    require(len(summary) == 1, "v17 summary must have one row")
    summary_row = summary[0]
    require(summary_row["overall_status"] == "AUTHORIZED_WRITER_BLOCKED", "v17 summary must remain blocked")
    require(summary_row["target_file_written"] == "false", "v17 summary must not write target input")
    require(summary_row["rows_written"] == "0", "v17 summary must write zero rows")
    require(summary_row["target_input_file_present_after_writer"] == "false", "v17 target input must remain absent after writer")
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "v17 summary must forbid scoring")


def validate_source_import_raw_template_v18() -> None:
    template = read_csv(ROOT / "data/input/source_import_raw_sparc_like_v15_TEMPLATE.csv")
    columns = read_csv(ROOT / "data/derived/source_import_raw_template_columns_v18.csv")
    summary = read_csv(ROOT / "data/derived/source_import_raw_template_summary_v18.csv")
    require(len(template) == 18, "v18 raw template must include one placeholder row per candidate galaxy")
    require(all(row["v_obs_km_s"] == "FILL_NUMERIC_OBSERVED_VELOCITY" for row in template), "v18 template must remain placeholder-only")
    require(len(columns) == 15, "v18 raw template must document fifteen raw columns")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in columns), "v18 template columns cannot allow scoring")
    require(len(summary) == 1, "v18 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "RAW_TEMPLATE_READY_NOT_DATA", "v18 must remain template-only")
    require(row["template_rows"] == "18", "v18 summary must report eighteen template rows")
    require(row["required_columns"] == "15", "v18 summary must report fifteen raw columns")
    require(row["raw_input_file_present"] == "false", "v18 must not include the real raw input file")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v18 summary must forbid scoring")


def validate_source_import_provenance_v19() -> None:
    rows = read_csv(ROOT / "data/derived/source_import_provenance_manifest_v19.csv")
    columns = read_csv(ROOT / "data/derived/source_import_provenance_columns_v19.csv")
    summary = read_csv(ROOT / "data/derived/source_import_provenance_summary_v19.csv")
    require(len(rows) == 18, "v19 provenance manifest must cover eighteen candidate rows")
    require(all(row["catalog_status"] == "PROVENANCE_REQUIRED_NOT_FILLED" for row in rows), "v19 catalog provenance must be unfilled")
    require(all(row["raw_import_allowed"] == "false" for row in rows), "v19 raw import must not be allowed")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v19 rows cannot allow scoring")
    require(len(columns) == 7, "v19 must document seven provenance fields")
    require(all(row["required_before_raw_import"] == "true" for row in columns), "v19 provenance fields must precede raw import")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in columns), "v19 columns cannot allow scoring")
    require(len(summary) == 1, "v19 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "PROVENANCE_REQUIRED_NOT_FILLED", "v19 provenance must remain unfilled")
    require(row["candidate_rows"] == "18", "v19 summary must cover eighteen rows")
    require(row["provenance_complete_rows"] == "0", "v19 must complete zero provenance rows")
    require(row["raw_import_allowed_rows"] == "0", "v19 must allow zero raw imports")
    require(row["required_provenance_fields"] == "7", "v19 must require seven provenance fields")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v19 summary must forbid scoring")


def validate_source_import_provenance_audit_v20() -> None:
    rows = read_csv(ROOT / "data/derived/source_import_provenance_audit_v20.csv")
    summary = read_csv(ROOT / "data/derived/source_import_provenance_audit_summary_v20.csv")
    require(len(rows) == 18, "v20 provenance audit must cover eighteen candidate rows")
    require(all(row["provenance_complete"] == "false" for row in rows), "v20 must complete zero provenance rows")
    require(all(row["raw_import_decision"] == "DO_NOT_IMPORT_RAW" for row in rows), "v20 must block raw import")
    require(all("catalog_provenance_missing" in row["blocking_requirements"] for row in rows), "v20 must report catalog blockers")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v20 rows cannot allow scoring")
    require(len(summary) == 1, "v20 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "RAW_IMPORT_BLOCKED_BY_PROVENANCE", "v20 must block raw import by provenance")
    require(row["audited_rows"] == "18", "v20 summary must audit eighteen rows")
    require(row["provenance_complete_rows"] == "0", "v20 must complete zero provenance rows")
    require(row["raw_import_allowed_rows"] == "0", "v20 must allow zero raw imports")
    require(row["raw_import_blocked_rows"] == "18", "v20 must block eighteen rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v20 summary must forbid scoring")


def validate_source_import_provenance_template_v21() -> None:
    template = read_csv(ROOT / "data/input/source_import_provenance_evidence_v21_TEMPLATE.csv")
    columns = read_csv(ROOT / "data/derived/source_import_provenance_template_columns_v21.csv")
    summary = read_csv(ROOT / "data/derived/source_import_provenance_template_summary_v21.csv")
    require(len(template) == 18, "v21 provenance template must include one placeholder row per candidate galaxy")
    require(
        all(row["provenance_evidence_status"] == "TEMPLATE_ROW_DO_NOT_IMPORT" for row in template),
        "v21 template rows must not be importable",
    )
    require(len(columns) == 9, "v21 provenance template must document nine fields")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in columns), "v21 columns cannot allow scoring")
    require(len(summary) == 1, "v21 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "PROVENANCE_TEMPLATE_READY_NOT_DATA", "v21 must remain template-only")
    require(row["template_rows"] == "18", "v21 summary must report eighteen rows")
    require(row["required_columns"] == "9", "v21 summary must report nine columns")
    require(row["evidence_input_file_present"] == "false", "v21 must not include real evidence input")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v21 summary must forbid scoring")


def validate_source_import_provenance_evidence_gate_v22() -> None:
    gate = read_csv(ROOT / "data/derived/source_import_provenance_evidence_gate_v22.csv")
    summary = read_csv(ROOT / "data/derived/source_import_provenance_evidence_gate_summary_v22.csv")
    require(len(gate) == 1, "v22 evidence gate must have one row")
    row = gate[0]
    require(row["evidence_input_status"] == "EVIDENCE_INPUT_FILE_MISSING", "v22 evidence input must remain absent")
    require(row["evidence_rows_seen"] == "0", "v22 must see zero evidence rows")
    require(row["valid_evidence_rows"] == "0", "v22 must validate zero evidence rows")
    require(row["galaxies_with_valid_evidence"] == "0", "v22 must validate zero galaxies")
    require(row["provenance_promotion_allowed"] == "false", "v22 must not allow provenance promotion")
    require(row["endpoint_scoring_allowed"] == "false", "v22 row cannot allow scoring")
    require(len(summary) == 1, "v22 summary must have one row")
    summary_row = summary[0]
    require(summary_row["overall_status"] == "PROVENANCE_EVIDENCE_INPUT_MISSING", "v22 summary must report missing evidence")
    require(summary_row["evidence_input_status"] == "EVIDENCE_INPUT_FILE_MISSING", "v22 summary must report missing evidence input")
    require(summary_row["valid_evidence_rows"] == "0", "v22 summary must validate zero rows")
    require(summary_row["provenance_promotion_allowed"] == "false", "v22 summary must block promotion")
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "v22 summary must forbid scoring")


def validate_source_import_provenance_promotion_gate_v23() -> None:
    rows = read_csv(ROOT / "data/derived/source_import_provenance_promotion_gate_v23.csv")
    summary = read_csv(ROOT / "data/derived/source_import_provenance_promotion_summary_v23.csv")
    require(len(rows) == 18, "v23 promotion gate must cover eighteen candidate rows")
    require(
        all(row["v22_provenance_promotion_allowed"] == "false" for row in rows),
        "v23 must inherit the blocked v22 promotion decision",
    )
    require(all(row["promotion_allowed"] == "false" for row in rows), "v23 must block all promotions")
    require(
        all(row["promotion_decision"] == "DO_NOT_PROMOTE_PROVENANCE" for row in rows),
        "v23 must not promote provenance",
    )
    require(
        all("provenance_evidence_gate_not_allowed" in row["promotion_blockers"] for row in rows),
        "v23 must report the evidence-gate blocker",
    )
    require(all(row["provenance_rows_promoted"] == "0" for row in rows), "v23 must promote zero rows")
    require(all(row["raw_import_allowed_after_promotion"] == "false" for row in rows), "v23 cannot allow raw import")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v23 rows cannot allow scoring")
    require(len(summary) == 1, "v23 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "PROVENANCE_PROMOTION_BLOCKED", "v23 summary must block promotion")
    require(row["candidate_rows"] == "18", "v23 summary must cover eighteen rows")
    require(row["promotion_allowed_rows"] == "0", "v23 must allow zero promotions")
    require(row["promotion_blocked_rows"] == "18", "v23 must block eighteen promotions")
    require(row["provenance_rows_promoted"] == "0", "v23 must promote zero provenance rows")
    require(row["raw_import_allowed_rows_after_promotion"] == "0", "v23 must allow zero raw imports")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v23 summary must forbid scoring")


def validate_scoring_dependency_closure_v24() -> None:
    rows = read_csv(ROOT / "data/derived/scoring_dependency_closure_v24.csv")
    summary = read_csv(ROOT / "data/derived/scoring_dependency_closure_summary_v24.csv")
    require(len(rows) == 13, "v24 dependency closure must check thirteen dependencies")
    ids = {row["dependency_id"] for row in rows}
    required = {
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
    require(ids == required, f"v24 dependency ids mismatch: {ids ^ required}")
    require(all(row["dependency_decision"] == "BLOCKED" for row in rows), "v24 must block all dependencies")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v24 rows cannot allow scoring")
    require(any(row["upstream_status"] == "PROVENANCE_PROMOTION_BLOCKED" for row in rows), "v24 must include v23 block")
    require(any(row["upstream_status"] == "SCORING_ACTIVATION_BLOCKED" for row in rows), "v24 must include v13 block")
    require(len(summary) == 1, "v24 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SCORING_DEPENDENCY_CLOSURE_BLOCKED", "v24 summary must block scoring closure")
    require(row["dependencies_checked"] == "13", "v24 must check thirteen dependencies")
    require(row["ready_dependencies"] == "0", "v24 must have zero ready dependencies")
    require(row["blocked_dependencies"] == "13", "v24 must block thirteen dependencies")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v24 summary must forbid scoring")


def validate_scoring_unblock_priority_v25() -> None:
    rows = read_csv(ROOT / "data/derived/scoring_unblock_priority_v25.csv")
    summary = read_csv(ROOT / "data/derived/scoring_unblock_priority_summary_v25.csv")
    require(len(rows) == 13, "v25 priority ledger must cover thirteen dependencies")
    ranks = [int(row["priority_rank"]) for row in rows]
    require(ranks == list(range(1, 14)), f"v25 ranks must be contiguous: {ranks}")
    require(all(row["dependency_decision"] == "BLOCKED" for row in rows), "v25 must preserve blocked dependencies")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v25 rows cannot allow scoring")
    frontier = [row for row in rows if row["frontier_now"] == "true"]
    require(len(frontier) == 1, "v25 must identify exactly one current frontier")
    require(frontier[0]["dependency_id"] == "SCD24_PROVENANCE_EVIDENCE", "v25 first frontier must be provenance evidence")
    require(
        frontier[0]["next_required_artifact"] == "data/input/source_import_provenance_evidence_v21.csv",
        "v25 frontier artifact must be provenance evidence input",
    )
    require(len(summary) == 1, "v25 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SCORING_UNBLOCK_FRONTIER_IDENTIFIED", "v25 must identify a frontier")
    require(row["priority_rows"] == "13", "v25 must summarize thirteen priorities")
    require(row["blocked_priority_rows"] == "13", "v25 must preserve thirteen blocked rows")
    require(row["frontier_now_rows"] == "1", "v25 must summarize one current frontier")
    require(row["first_frontier_dependency"] == "SCD24_PROVENANCE_EVIDENCE", "v25 frontier dependency mismatch")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v25 summary must forbid scoring")


def main() -> None:
    validate_model_families()
    validate_freeze_requirements()
    validate_outcomes()
    validate_policy_bundle_instance()
    validate_galaxy_endpoint_manifest()
    validate_sample_freeze()
    validate_scoring_freeze()
    validate_controls()
    validate_thresholds()
    validate_galaxy_list_v02()
    validate_scoring_formula_v02()
    validate_family_parameter_count_v03()
    validate_control_implementation_v03()
    validate_source_field_completeness_v04()
    validate_family_formula_registry_v04()
    validate_control_runner_contract_v04()
    validate_source_row_audit_v05()
    validate_family_formula_table_v05()
    validate_numeric_count_readiness_v05()
    validate_readiness_audit_v06()
    validate_scoring_preflight_v07()
    validate_scoring_input_scaffold_v08()
    validate_source_import_leakage_audit_v09()
    validate_source_import_contract_v10()
    validate_source_import_values_v11()
    validate_source_import_real_values_gate_v12()
    validate_scoring_activation_gate_v13()
    validate_source_import_template_v14()
    validate_source_import_raw_adapter_v15()
    validate_source_import_write_authorization_v16()
    validate_source_import_authorized_writer_v17()
    validate_source_import_raw_template_v18()
    validate_source_import_provenance_v19()
    validate_source_import_provenance_audit_v20()
    validate_source_import_provenance_template_v21()
    validate_source_import_provenance_evidence_gate_v22()
    validate_source_import_provenance_promotion_gate_v23()
    validate_scoring_dependency_closure_v24()
    validate_scoring_unblock_priority_v25()
    print("PAPER11_PROTOCOL_MANIFESTS_VALID")


if __name__ == "__main__":
    main()
