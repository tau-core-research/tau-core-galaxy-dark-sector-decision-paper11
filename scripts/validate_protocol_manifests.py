#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
import zipfile


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
            "activated_scoring_rows_v10.csv",
            "data/input/source_import_real_values_v12.csv",
            "family_prediction_tables_v08.csv",
            "numeric_parameter_count_table_final_values_v10.csv",
            "control_runner_outputs_v08.csv",
            "numeric_decision_thresholds_v08.csv",
        },
        f"v07 scoring requirements mismatch: {required_artifacts}",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in requirements), "v07 requirements cannot allow scoring")
    blocked_requirement_ids = {
        row["requirement_id"]
        for row in requirements
        if row["current_status"].startswith("BLOCKED")
    }
    require(blocked_requirement_ids == set(), f"v07 must clear preflight blockers: {blocked_requirement_ids}")
    require(len(components) == 7, "v07 must expose seven scoring formula components")
    require(all(row["formula_policy_status"] == "READY_AS_POLICY_NOT_RUN" for row in components), "v07 formulas must be policy-only")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in components), "v07 components cannot allow scoring")
    require(len(summary) == 1, "v07 scoring summary must have one row")
    row = summary[0]
    require(row["readiness_dependency"] == "ENDPOINT_SCORING_BLOCKED", "v07 must depend on blocked readiness")
    require(
        row["blocked_scoring_requirements"] == "0",
        "v07 must report zero blocked scoring requirements",
    )
    require(
        row["overall_status"] == "SCORING_PREFLIGHT_REQUIREMENTS_READY_RAW_M0_ADEQUACY_RUNNER_NEXT_VERDICT_BLOCKED",
        "v07 scoring preflight status mismatch",
    )
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v07 summary must forbid endpoint scoring")
    require(row["next_required_artifact"] == "endpoint_scoring_runner_v01", "v07 must point to endpoint scoring runner")


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
        all(row["source_import_status"] == "REAL_VALUES_PRESENT_VALIDATION_PENDING_LEAKAGE" for row in audit),
        "v09 source import must be present pending leakage",
    )
    require(all(row["leakage_audit_status"] == "LEAKAGE_AUDIT_PASS" for row in audit), "v09 leakage must pass")
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
        "REAL_VALUE_GATE_PRESENT_INPUT_READY_FOR_LEAKAGE",
    }
    require(
        all(row["current_status"] in allowed_requirement_statuses for row in requirements),
        "v09 requirements must remain pending or contract-present",
    )
    require(len(findings) == 18, "v09 leakage findings must cover eighteen rows")
    require(
        all(row["leakage_status"] == "LEAKAGE_AUDIT_PASS" for row in findings),
        "v09 findings must pass leakage",
    )
    require(len(summary) == 1, "v09 summary must have one row")
    row = summary[0]
    require(
        row["overall_status"] == "SOURCE_IMPORT_AND_LEAKAGE_READY",
        "v09 status must be leakage-ready",
    )
    require(row["source_import_pending_rows"] == "0", "v09 source import must have zero pending rows")
    require(row["leakage_pass_rows"] == "18", "v09 must pass eighteen leakage rows")
    require(row["activated_rows"] == "0", "v09 must activate zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v09 summary must forbid scoring")
    require(
        row["next_required_artifact"] == "scoring_row_activation_policy_v79",
        "v09 must point to scoring activation recheck",
    )


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


def validate_leakage_audit_evidence_template_v58() -> None:
    rows = read_csv(ROOT / "data/input/leakage_audit_evidence_v10_TEMPLATE.csv")
    summary = read_csv(ROOT / "data/derived/leakage_audit_evidence_template_summary_v58.csv")
    require(len(rows) == 72, "v58 leakage template must cover 72 galaxy/check rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v58 leakage template must cover eighteen galaxies")
    require(
        {row["evidence_id"] for row in rows}
        == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS", "LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v58 evidence ids must match v10 leakage contract",
    )
    require(all(row["review_decision"] == "TEMPLATE_ROW_DO_NOT_IMPORT" for row in rows), "v58 rows must be template-only")
    require(all(row["evidence_status"] == "TEMPLATE_ROW_DO_NOT_IMPORT" for row in rows), "v58 evidence cannot be active")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v58 rows cannot allow scoring")
    require(len(summary) == 1, "v58 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_AUDIT_EVIDENCE_TEMPLATE_V58", "v58 summary id mismatch")
    require(row["template_rows"] == "72", "v58 summary must report 72 template rows")
    require(row["galaxies_covered"] == "18", "v58 summary must report eighteen galaxies")
    require(row["evidence_checks_per_galaxy"] == "4", "v58 must require four checks per galaxy")
    require(row["leakage_pass_rows_created"] == "0", "v58 must create zero leakage pass rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v58 summary must forbid scoring")
    require(
        row["overall_status"] == "LEAKAGE_AUDIT_EVIDENCE_TEMPLATE_READY_NOT_EVIDENCE",
        "v58 must remain template-only",
    )


def validate_leakage_audit_review_package_v59() -> None:
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
    require(package_root.exists(), "v59 leakage review package directory must exist")
    require(zip_path.exists(), "v59 leakage review package zip must exist")
    for rel in required:
        require((package_root / rel).exists(), f"v59 package missing {rel}")
    manifest = read_csv(package_root / "REVIEW_MANIFEST.csv")
    require(len(manifest) == len(required) - 1, "v59 manifest row count mismatch")
    require(
        {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"},
        "v59 manifest package paths mismatch",
    )
    require(
        all(row["claim_boundary"] == "leakage_review_package_only_no_evidence_no_scores" for row in manifest),
        "v59 manifest claim boundary mismatch",
    )
    response = read_csv(package_root / "templates/leakage_audit_review_response_TEMPLATE.csv")
    require(len(response) == 72, "v59 response template must cover 72 rows")
    require(
        all(row["review_decision"] == "KEEP_TEMPLATE_NOT_REVIEWED_NO_LEAKAGE_PASS" for row in response),
        "v59 response template must default to no leakage pass",
    )
    require(
        all(row["reviewer_leakage_pass_authorized"] == "false" for row in response),
        "v59 response template cannot authorize leakage pass by default",
    )
    require(
        all(row["may_activate_row_after_ingestion"] == "false" for row in response),
        "v59 response template cannot activate rows by default",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in response), "v59 response cannot allow scoring")
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    zipped_required = {f"leakage_audit_v58_review_package/{rel}" for rel in required}
    require(zipped_required.issubset(names), "v59 zip missing required package files")


def validate_leakage_audit_review_response_intake_v60() -> None:
    rows = read_csv(ROOT / "data/derived/leakage_audit_review_response_intake_v60.csv")
    summary = read_csv(ROOT / "data/derived/leakage_audit_review_response_intake_summary_v60.csv")
    response_dir = ROOT / "review_packages/leakage_audit_v58_completed_review_response"
    response_zip = ROOT / "review_packages/leakage_audit_v58_completed_review_response.zip"
    required = {
        "leakage_audit_v58_review_response.csv",
        "leakage_audit_v58_review_completed_summary.csv",
        "leakage_audit_v58_review_notes.md",
        "leakage_audit_v58_review_validation_log.txt",
    }
    require(response_zip.exists(), "v60 completed response zip must exist")
    require(response_dir.exists(), "v60 completed response directory must exist")
    for rel in required:
        require((response_dir / rel).exists(), f"v60 response missing {rel}")
    with zipfile.ZipFile(response_zip) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    require(required.issubset(names), "v60 response zip missing required files")
    require(len(rows) == 72, "v60 intake must cover 72 review rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v60 intake must cover eighteen galaxies")
    require(
        all(row["review_decision"] == "NO_GO_EVIDENCE_REQUIRED_NOT_FILLED" for row in rows),
        "v60 rows must record no-go decisions",
    )
    require(all(row["reviewer_leakage_pass_authorized"] == "false" for row in rows), "v60 must authorize zero passes")
    require(all(row["may_activate_row_after_ingestion"] == "false" for row in rows), "v60 must authorize zero activations")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v60 rows cannot allow scoring")
    require(
        all(row["intake_decision"] == "ACCEPT_AS_REVIEWED_NO_GO_NOT_EVIDENCE" for row in rows),
        "v60 intake rows must be accepted only as no-go review",
    )
    require(len(summary) == 1, "v60 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_AUDIT_REVIEW_RESPONSE_INTAKE_V60", "v60 summary id mismatch")
    require(row["response_files_present"] == "4", "v60 must record four response files")
    require(row["review_rows"] == "72", "v60 summary must record 72 rows")
    require(row["no_go_rows"] == "72", "v60 summary must record 72 no-go rows")
    require(row["leakage_pass_rows_authorized"] == "0", "v60 summary must authorize zero leakage passes")
    require(row["activation_rows_authorized"] == "0", "v60 summary must authorize zero activations")
    require(row["target_evidence_rows_created_by_response"] == "0", "v60 response cannot create target evidence")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v60 summary must forbid scoring")
    require(
        row["overall_status"] == "LEAKAGE_REVIEW_RESPONSE_ACCEPTED_AS_NO_GO_NOT_EVIDENCE",
        "v60 summary must be no-go not evidence",
    )


def validate_leakage_prescore_artifact_work_order_v61() -> None:
    rows = read_csv(ROOT / "data/derived/leakage_prescore_artifact_work_order_v61.csv")
    coverage = read_csv(ROOT / "data/derived/leakage_prescore_artifact_work_order_coverage_v61.csv")
    summary = read_csv(ROOT / "data/derived/leakage_prescore_artifact_work_order_summary_v61.csv")
    require(len(rows) == 72, "v61 work order must cover 72 leakage artifact rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v61 work order must cover eighteen galaxies")
    require(
        {row["evidence_id"] for row in rows}
        == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS", "LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v61 evidence ids must match leakage contract",
    )
    require(
        all(row["artifact_collection_status"] == "OPEN_PRESCORE_ARTIFACT_REQUIRED" for row in rows),
        "v61 rows must remain open",
    )
    require(
        all(row["may_create_leakage_evidence_after_work_order"] == "false" for row in rows),
        "v61 cannot create leakage evidence",
    )
    require(all(row["may_activate_row_after_work_order"] == "false" for row in rows), "v61 cannot activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v61 rows cannot allow scoring")
    require(len(coverage) == 4, "v61 coverage must summarize four leakage checks")
    require(all(row["galaxy_rows"] == "18" for row in coverage), "v61 coverage rows must cover eighteen galaxies")
    require(all(row["open_prescore_artifact_rows"] == "18" for row in coverage), "v61 coverage must keep all rows open")
    require(all(row["ready_for_leakage_evidence_rows"] == "0" for row in coverage), "v61 coverage cannot mark ready rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in coverage), "v61 coverage cannot allow scoring")
    require(len(summary) == 1, "v61 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_PRESCORE_ARTIFACT_WORK_ORDER_V61", "v61 summary id mismatch")
    require(row["work_order_rows"] == "72", "v61 must summarize 72 work order rows")
    require(row["open_prescore_artifact_rows"] == "72", "v61 must keep 72 rows open")
    require(row["ready_for_leakage_evidence_rows"] == "0", "v61 must mark zero rows ready")
    require(row["leakage_pass_rows_created"] == "0", "v61 cannot create leakage passes")
    require(row["activation_rows_authorized"] == "0", "v61 cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v61 summary must forbid scoring")
    require(row["overall_status"] == "LEAKAGE_PRESCORE_ARTIFACT_WORK_ORDER_OPEN", "v61 must remain open")


def validate_leakage_prescore_artifact_collection_package_v62() -> None:
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
    require(package_root.exists(), "v62 collection package directory must exist")
    require(zip_path.exists(), "v62 collection package zip must exist")
    for rel in required:
        require((package_root / rel).exists(), f"v62 package missing {rel}")

    manifest = read_csv(package_root / "REVIEW_MANIFEST.csv")
    require(len(manifest) == len(required) - 1, "v62 manifest row count mismatch")
    require(
        {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"},
        "v62 manifest package paths mismatch",
    )
    require(
        all(
            row["claim_boundary"] == "leakage_prescore_artifact_collection_package_only_no_evidence_no_scores"
            for row in manifest
        ),
        "v62 manifest claim boundary mismatch",
    )

    response = read_csv(package_root / "templates/leakage_prescore_artifact_collection_response_TEMPLATE.csv")
    require(len(response) == 72, "v62 response template must cover 72 work-order rows")
    require(len({row["galaxy_id"] for row in response}) == 18, "v62 response template must cover eighteen galaxies")
    require(
        all(row["artifact_review_decision"] == "KEEP_OPEN_ARTIFACT_REQUIRED_NOT_FILLED" for row in response),
        "v62 response template must default to open artifact review",
    )
    require(all(row["artifact_is_prescore"] == "false" for row in response), "v62 cannot prescore-confirm by default")
    require(
        all(row["artifact_uses_endpoint_residual_or_family_winner"] == "UNKNOWN_REVIEW_REQUIRED" for row in response),
        "v62 must require endpoint-leakage review by default",
    )
    require(
        all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in response),
        "v62 cannot promote leakage evidence by default",
    )
    require(
        all(row["may_activate_row_after_ingestion"] == "false" for row in response),
        "v62 cannot activate rows by default",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in response), "v62 cannot allow scoring")

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    zipped_required = {f"leakage_prescore_artifact_v61_collection_package/{rel}" for rel in required}
    require(zipped_required.issubset(names), "v62 zip missing required package files")


def validate_leakage_prescore_artifact_collection_intake_v63() -> None:
    rows = read_csv(ROOT / "data/derived/leakage_prescore_artifact_collection_intake_v63.csv")
    summary = read_csv(ROOT / "data/derived/leakage_prescore_artifact_collection_intake_summary_v63.csv")
    response_dir = ROOT / "review_packages/leakage_prescore_artifact_v61_completed_collection_response"
    response_zip = ROOT / "review_packages/leakage_prescore_artifact_v61_completed_collection_response.zip"
    required = {
        "leakage_prescore_artifact_v61_collection_response.csv",
        "leakage_prescore_artifact_v61_collection_completed_summary.csv",
        "leakage_prescore_artifact_v61_collection_notes.md",
        "leakage_prescore_artifact_v61_collection_validation_log.txt",
    }
    require(response_zip.exists(), "v63 completed collection response zip must exist")
    require(response_dir.exists(), "v63 completed collection response directory must exist")
    for rel in required:
        require((response_dir / rel).exists(), f"v63 response missing {rel}")
    with zipfile.ZipFile(response_zip) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    require(required.issubset(names), "v63 response zip missing required files")
    require(len(rows) == 72, "v63 intake must cover 72 work-order rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v63 intake must cover eighteen galaxies")
    require(
        {row["evidence_id"] for row in rows}
        == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS", "LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v63 evidence ids must match leakage contract",
    )
    require(
        all(row["source_mode"] == "completed_response" for row in rows),
        "v63 must run from completed response once response package is present",
    )
    require(
        all(row["intake_decision"] == "BLOCKED_PRESCORE_ARTIFACT_REVIEW_INCOMPLETE_OR_UNSAFE" for row in rows),
        "v63 rows must remain blocked when completed response provides no prescore artifacts",
    )
    require(
        all(row["leakage_evidence_candidate_status"] == "NOT_CANDIDATE_REVIEW_INCOMPLETE_OR_UNSAFE" for row in rows),
        "v63 cannot mark leakage evidence candidates without reviewed prescore artifacts",
    )
    require(
        all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in rows),
        "v63 cannot promote leakage evidence from template rows",
    )
    require(all(row["may_activate_row_after_ingestion"] == "false" for row in rows), "v63 cannot activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v63 rows cannot allow scoring")
    require(len(summary) == 1, "v63 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_PRESCORE_ARTIFACT_COLLECTION_INTAKE_V63", "v63 summary id mismatch")
    require(row["expected_response_files_present"] == "4", "v63 must record four completed response files")
    require(row["intake_rows"] == "72", "v63 summary must record 72 intake rows")
    require(row["completed_response_present"] == "true", "v63 completed response must be present")
    require(row["candidate_rows_for_later_leakage_evidence"] == "0", "v63 cannot create candidates yet")
    require(row["blocked_or_missing_rows"] == "72", "v63 must keep all rows blocked")
    require(row["leakage_evidence_rows_created"] == "0", "v63 cannot create leakage evidence")
    require(row["activation_rows_authorized"] == "0", "v63 cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v63 summary must forbid scoring")
    require(row["overall_status"] == "PRESCORE_ARTIFACT_RESPONSE_PRESENT_BUT_BLOCKED", "v63 must remain blocked")


def validate_leakage_prescore_artifact_request_ledger_v64() -> None:
    rows = read_csv(ROOT / "data/derived/leakage_prescore_artifact_request_ledger_v64.csv")
    coverage = read_csv(ROOT / "data/derived/leakage_prescore_artifact_request_coverage_v64.csv")
    summary = read_csv(ROOT / "data/derived/leakage_prescore_artifact_request_summary_v64.csv")
    require(len(rows) == 72, "v64 request ledger must cover 72 rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v64 request ledger must cover eighteen galaxies")
    require(
        {row["evidence_id"] for row in rows}
        == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS", "LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v64 evidence ids must match leakage contract",
    )
    require(
        all(row["request_status"] == "OPEN_REVIEWED_PRESCORE_ARTIFACT_REQUIRED" for row in rows),
        "v64 request rows must remain open",
    )
    require(all(row["minimal_required_fields"] for row in rows), "v64 rows must state minimal required fields")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "v64 rows must forbid endpoint residuals")
    require(
        all(row["may_create_leakage_evidence_from_request"] == "false" for row in rows),
        "v64 cannot create leakage evidence",
    )
    require(all(row["may_activate_row_from_request"] == "false" for row in rows), "v64 cannot activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v64 cannot allow scoring")
    require(len(coverage) == 4, "v64 coverage must summarize four leakage checks")
    require(all(row["request_rows"] == "18" for row in coverage), "v64 coverage rows must cover eighteen galaxies")
    require(all(row["open_request_rows"] == "18" for row in coverage), "v64 coverage must keep all rows open")
    require(all(row["candidate_rows_already_available"] == "0" for row in coverage), "v64 coverage cannot mark candidates")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in coverage), "v64 coverage cannot allow scoring")
    require(len(summary) == 1, "v64 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_PRESCORE_ARTIFACT_REQUEST_LEDGER_V64", "v64 summary id mismatch")
    require(row["request_rows"] == "72", "v64 must summarize 72 request rows")
    require(row["open_request_rows"] == "72", "v64 must keep 72 rows open")
    require(row["candidate_rows_already_available"] == "0", "v64 cannot mark candidates")
    require(row["leakage_evidence_rows_created"] == "0", "v64 cannot create leakage evidence")
    require(row["activation_rows_authorized"] == "0", "v64 cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v64 summary must forbid scoring")
    require(row["overall_status"] == "PRESCORE_ARTIFACT_REQUEST_LEDGER_OPEN", "v64 must remain open")


def validate_leakage_prescore_artifact_request_review_package_v65() -> None:
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
    require(package_root.exists(), "v65 review package directory must exist")
    require(zip_path.exists(), "v65 review package zip must exist")
    for rel in required:
        require((package_root / rel).exists(), f"v65 package missing {rel}")
    manifest = read_csv(package_root / "REVIEW_MANIFEST.csv")
    require(len(manifest) == len(required) - 1, "v65 manifest row count mismatch")
    require(
        {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"},
        "v65 manifest package paths mismatch",
    )
    require(
        all(row["claim_boundary"] == "leakage_prescore_artifact_request_review_package_only_no_evidence_no_scores" for row in manifest),
        "v65 manifest claim boundary mismatch",
    )
    response = read_csv(package_root / "templates/leakage_prescore_artifact_request_review_response_TEMPLATE.csv")
    require(len(response) == 72, "v65 response template must cover 72 request rows")
    require(len({row["galaxy_id"] for row in response}) == 18, "v65 response template must cover eighteen galaxies")
    require(
        all(row["artifact_review_decision"] == "KEEP_OPEN_REVIEWED_PRESCORE_ARTIFACT_REQUIRED_NOT_FILLED" for row in response),
        "v65 response template must default to open review",
    )
    require(all(row["minimal_required_fields_covered"] == "false" for row in response), "v65 cannot field-cover by default")
    require(all(row["artifact_is_prescore"] == "false" for row in response), "v65 cannot prescore-confirm by default")
    require(
        all(row["artifact_uses_forbidden_inputs"] == "UNKNOWN_REVIEW_REQUIRED" for row in response),
        "v65 must require forbidden-input review by default",
    )
    require(
        all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in response),
        "v65 cannot promote leakage evidence by default",
    )
    require(all(row["may_activate_row_after_ingestion"] == "false" for row in response), "v65 cannot activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in response), "v65 cannot allow scoring")
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    zipped_required = {f"leakage_prescore_artifact_request_v64_review_package/{rel}" for rel in required}
    require(zipped_required.issubset(names), "v65 zip missing required package files")


def validate_leakage_prescore_artifact_request_review_intake_v66() -> None:
    rows = read_csv(ROOT / "data/derived/leakage_prescore_artifact_request_review_intake_v66.csv")
    summary = read_csv(ROOT / "data/derived/leakage_prescore_artifact_request_review_intake_summary_v66.csv")
    response_dir = ROOT / "review_packages/leakage_prescore_artifact_request_v64_completed_review_response"
    response_zip = ROOT / "review_packages/leakage_prescore_artifact_request_v64_completed_review_response.zip"
    required = {
        "leakage_prescore_artifact_request_v64_review_response.csv",
        "leakage_prescore_artifact_request_v64_review_completed_summary.csv",
        "leakage_prescore_artifact_request_v64_review_notes.md",
        "leakage_prescore_artifact_request_v64_review_validation_log.txt",
    }
    require(response_zip.exists(), "v66 completed review response zip must exist")
    require(response_dir.exists(), "v66 completed review response directory must exist")
    for rel in required:
        require((response_dir / rel).exists(), f"v66 response missing {rel}")
    with zipfile.ZipFile(response_zip) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    require(required.issubset(names), "v66 response zip missing required files")
    require(len(rows) == 72, "v66 intake must cover 72 request rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v66 intake must cover eighteen galaxies")
    require(
        all(row["source_mode"] == "completed_response" for row in rows),
        "v66 must run from completed response",
    )
    require(
        all(row["intake_decision"] == "BLOCKED_PRESCORE_REQUEST_REVIEW_INCOMPLETE_OR_UNSAFE" for row in rows),
        "v66 rows must remain blocked when artifacts are not provided",
    )
    require(
        all(row["leakage_evidence_candidate_status"] == "NOT_CANDIDATE_REVIEW_INCOMPLETE_OR_UNSAFE" for row in rows),
        "v66 cannot mark candidates without reviewed prescore artifacts",
    )
    require(all(row["minimal_required_fields_covered"] == "false" for row in rows), "v66 cannot field-cover rows")
    require(all(row["artifact_is_prescore"] == "false" for row in rows), "v66 cannot prescore-confirm rows")
    require(all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in rows), "v66 cannot promote evidence")
    require(all(row["may_activate_row_after_ingestion"] == "false" for row in rows), "v66 cannot activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v66 cannot allow scoring")
    require(len(summary) == 1, "v66 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_PRESCORE_ARTIFACT_REQUEST_REVIEW_INTAKE_V66", "v66 summary id mismatch")
    require(row["response_files_present"] == "4", "v66 must record four response files")
    require(row["intake_rows"] == "72", "v66 summary must record 72 rows")
    require(row["completed_response_present"] == "true", "v66 response must be present")
    require(row["candidate_rows_for_later_leakage_evidence"] == "0", "v66 cannot create candidates")
    require(row["blocked_or_missing_rows"] == "72", "v66 must keep all rows blocked")
    require(row["leakage_evidence_rows_created"] == "0", "v66 cannot create leakage evidence")
    require(row["activation_rows_authorized"] == "0", "v66 cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v66 summary must forbid scoring")
    require(row["overall_status"] == "PRESCORE_REQUEST_REVIEW_RESPONSE_PRESENT_BUT_BLOCKED", "v66 must remain blocked")


def validate_leakage_prescore_artifact_candidate_ledger_v67() -> None:
    rows = read_csv(ROOT / "data/derived/leakage_prescore_artifact_candidate_ledger_v67.csv")
    coverage = read_csv(ROOT / "data/derived/leakage_prescore_artifact_candidate_coverage_v67.csv")
    summary = read_csv(ROOT / "data/derived/leakage_prescore_artifact_candidate_summary_v67.csv")
    require(len(rows) == 72, "v67 candidate ledger must cover 72 rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v67 candidate ledger must cover eighteen galaxies")
    require(
        {row["evidence_id"] for row in rows}
        == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS", "LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v67 evidence ids must match leakage contract",
    )
    require(
        all(row["candidate_artifact_uri_or_id"] for row in rows),
        "v67 rows must identify candidate artifact ids",
    )
    require(
        all(row["candidate_artifact_hash_or_accession"].startswith("sha256:") for row in rows),
        "v67 rows must carry sha256/accession support",
    )
    require(
        all(row["candidate_review_status"].endswith("REVIEW_REQUIRED") for row in rows),
        "v67 candidates must remain review-required",
    )
    require(
        all(row["may_promote_to_leakage_evidence_without_review"] == "false" for row in rows),
        "v67 cannot promote candidates without review",
    )
    require(all(row["may_activate_row_from_candidate"] == "false" for row in rows), "v67 cannot activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v67 cannot allow scoring")
    require(len(coverage) == 4, "v67 coverage must summarize four leakage checks")
    require(all(row["candidate_rows"] == "18" for row in coverage), "v67 coverage rows must cover eighteen galaxies")
    require(all(row["review_required_rows"] == "18" for row in coverage), "v67 coverage must require review")
    require(all(row["ready_for_leakage_evidence_rows"] == "0" for row in coverage), "v67 coverage cannot mark ready rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in coverage), "v67 coverage cannot allow scoring")
    require(len(summary) == 1, "v67 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_PRESCORE_ARTIFACT_CANDIDATE_LEDGER_V67", "v67 summary id mismatch")
    require(row["candidate_rows"] == "72", "v67 must summarize 72 candidate rows")
    require(row["full_candidate_rows"] == "36", "v67 must mark 36 full candidate rows")
    require(row["partial_candidate_rows"] == "36", "v67 must mark 36 partial candidate rows")
    require(row["review_required_rows"] == "72", "v67 must keep all candidates review-required")
    require(row["ready_for_leakage_evidence_rows"] == "0", "v67 cannot mark ready rows")
    require(row["leakage_evidence_rows_created"] == "0", "v67 cannot create leakage evidence")
    require(row["activation_rows_authorized"] == "0", "v67 cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v67 summary must forbid scoring")
    require(row["overall_status"] == "PRESCORE_ARTIFACT_CANDIDATES_IDENTIFIED_REVIEW_REQUIRED", "v67 status mismatch")


def validate_leakage_prescore_artifact_candidate_review_package_v68() -> None:
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
    require(package_root.exists(), "v68 review package directory must exist")
    require(zip_path.exists(), "v68 review package zip must exist")
    for rel in required:
        require((package_root / rel).exists(), f"v68 package missing {rel}")
    manifest = read_csv(package_root / "REVIEW_MANIFEST.csv")
    require(len(manifest) == len(required) - 1, "v68 manifest row count mismatch")
    require(
        {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"},
        "v68 manifest package paths mismatch",
    )
    require(
        all(row["claim_boundary"] == "leakage_prescore_artifact_candidate_review_package_only_no_evidence_no_scores" for row in manifest),
        "v68 manifest claim boundary mismatch",
    )
    response = read_csv(package_root / "templates/leakage_prescore_artifact_candidate_review_response_TEMPLATE.csv")
    require(len(response) == 72, "v68 response template must cover 72 candidate rows")
    require(len({row["galaxy_id"] for row in response}) == 18, "v68 response template must cover eighteen galaxies")
    require(
        all(row["candidate_review_decision"] == "KEEP_REVIEW_REQUIRED_NOT_AUTHORIZED" for row in response),
        "v68 response template must default to review required",
    )
    require(all(row["candidate_artifact_accepted"] == "false" for row in response), "v68 cannot accept candidates by default")
    require(all(row["minimal_required_fields_covered"] == "false" for row in response), "v68 cannot field-cover by default")
    require(all(row["artifact_is_prescore"] == "false" for row in response), "v68 cannot prescore-confirm by default")
    require(
        all(row["artifact_uses_forbidden_inputs"] == "UNKNOWN_REVIEW_REQUIRED" for row in response),
        "v68 must require forbidden-input review by default",
    )
    require(
        all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in response),
        "v68 cannot promote leakage evidence by default",
    )
    require(all(row["may_activate_row_after_ingestion"] == "false" for row in response), "v68 cannot activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in response), "v68 cannot allow scoring")
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    zipped_required = {f"leakage_prescore_artifact_candidate_v67_review_package/{rel}" for rel in required}
    require(zipped_required.issubset(names), "v68 zip missing required package files")


def validate_leakage_prescore_artifact_candidate_review_intake_v69() -> None:
    rows = read_csv(ROOT / "data/derived/leakage_prescore_artifact_candidate_review_intake_v69.csv")
    summary = read_csv(ROOT / "data/derived/leakage_prescore_artifact_candidate_review_intake_summary_v69.csv")
    response_dir = ROOT / "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response"
    response_zip = ROOT / "review_packages/leakage_prescore_artifact_candidate_v67_completed_review_response.zip"
    required = {
        "leakage_prescore_artifact_candidate_v67_review_response.csv",
        "leakage_prescore_artifact_candidate_v67_review_completed_summary.csv",
        "leakage_prescore_artifact_candidate_v67_review_notes.md",
        "leakage_prescore_artifact_candidate_v67_review_validation_log.txt",
    }
    require(response_zip.exists(), "v69 completed review response zip must exist")
    require(response_dir.exists(), "v69 completed review response directory must exist")
    for rel in required:
        require((response_dir / rel).exists(), f"v69 response missing {rel}")
    with zipfile.ZipFile(response_zip) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    require(required.issubset(names), "v69 response zip missing required files")
    require(len(rows) == 72, "v69 intake must cover 72 candidate rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v69 intake must cover eighteen galaxies")
    accepted = [
        row
        for row in rows
        if row["leakage_evidence_candidate_status"] == "CANDIDATE_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION"
    ]
    blocked = [
        row
        for row in rows
        if row["leakage_evidence_candidate_status"] == "NOT_CANDIDATE_PARTIAL_REVIEW_REQUIRED"
    ]
    require(len(accepted) == 36, "v69 must accept exactly 36 full candidates")
    require(len(blocked) == 36, "v69 must keep exactly 36 partial candidates blocked")
    require(
        {row["evidence_id"] for row in accepted} == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS"},
        "v69 accepted candidates must be source-route or observed-input rows",
    )
    require(
        {row["evidence_id"] for row in blocked} == {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v69 blocked candidates must be partial morphology-label or benchmark-policy rows",
    )
    require(
        all(row["intake_decision"] == "ACCEPT_AS_PRESCORE_CANDIDATE_FOR_LATER_LEAKAGE_EVIDENCE_GATE_NOT_EVIDENCE" for row in accepted),
        "v69 accepted rows must stay candidate-only",
    )
    require(
        all(row["intake_decision"] == "BLOCKED_PARTIAL_CANDIDATE_REVIEW_INCOMPLETE_OR_UNSAFE" for row in blocked),
        "v69 partial rows must remain blocked",
    )
    require(all(row["may_activate_row_after_ingestion"] == "false" for row in rows), "v69 cannot activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v69 cannot allow scoring")
    require(len(summary) == 1, "v69 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_PRESCORE_ARTIFACT_CANDIDATE_REVIEW_INTAKE_V69", "v69 summary id mismatch")
    require(row["response_files_present"] == "4", "v69 must record four response files")
    require(row["intake_rows"] == "72", "v69 summary must record 72 rows")
    require(row["accepted_candidate_rows"] == "36", "v69 summary must record 36 accepted candidates")
    require(row["blocked_partial_rows"] == "36", "v69 summary must record 36 blocked partial candidates")
    require(row["candidate_rows_for_later_leakage_evidence"] == "36", "v69 must expose 36 later-ingestion candidates")
    require(row["leakage_evidence_rows_created"] == "0", "v69 cannot create leakage evidence")
    require(row["activation_rows_authorized"] == "0", "v69 cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v69 summary must forbid scoring")
    require(
        row["overall_status"] == "PRESCORE_CANDIDATE_REVIEW_PARTIAL_ACCEPTANCE_NEEDS_LEAKAGE_EVIDENCE_GATE",
        "v69 status mismatch",
    )
    require(
        row["next_required_artifact"] == "leakage_evidence_candidate_ingestion_gate_for_36_accepted_candidates",
        "v69 next artifact mismatch",
    )


def validate_leakage_evidence_candidate_ingestion_gate_v70() -> None:
    rows = read_csv(ROOT / "data/derived/leakage_evidence_candidate_ingestion_gate_v70.csv")
    coverage = read_csv(ROOT / "data/derived/leakage_evidence_candidate_ingestion_coverage_v70.csv")
    summary = read_csv(ROOT / "data/derived/leakage_evidence_candidate_ingestion_summary_v70.csv")
    require(len(rows) == 72, "v70 ingestion gate must cover 72 candidate rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v70 ingestion gate must cover eighteen galaxies")
    draft = [
        row
        for row in rows
        if row["draft_evidence_candidate_status"] == "DRAFT_CANDIDATE_AVAILABLE_FOR_LATER_LEAKAGE_EVIDENCE_ROW"
    ]
    blocked = [row for row in rows if row["draft_evidence_candidate_status"] == "NOT_AVAILABLE_FOR_LEAKAGE_EVIDENCE_ROW"]
    require(len(draft) == 36, "v70 must expose exactly 36 draft evidence candidates")
    require(len(blocked) == 36, "v70 must keep exactly 36 partial rows blocked")
    require(
        {row["evidence_id"] for row in draft} == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS"},
        "v70 draft candidates must only cover source-route and observed-input rows",
    )
    require(
        {row["evidence_id"] for row in blocked} == {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v70 blocked rows must be morphology-label and benchmark-policy rows",
    )
    require(all(row["target_evidence_file_written"] == "false" for row in rows), "v70 cannot write target evidence")
    require(all(row["leakage_pass_authorized"] == "false" for row in rows), "v70 cannot authorize leakage pass")
    require(all(row["activation_rows_authorized"] == "0" for row in rows), "v70 cannot authorize activation")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v70 cannot allow scoring")
    require(len(coverage) == 4, "v70 coverage must summarize four evidence ids")
    coverage_by_id = {row["evidence_id"]: row for row in coverage}
    require(coverage_by_id["LEC10_SOURCE_ROUTE"]["draft_available_rows"] == "18", "v70 source-route coverage mismatch")
    require(coverage_by_id["LEC10_OBSERVED_INPUTS"]["draft_available_rows"] == "18", "v70 observed-input coverage mismatch")
    require(coverage_by_id["LEC10_MORPH_LABELS"]["blocked_rows"] == "18", "v70 morphology coverage mismatch")
    require(coverage_by_id["LEC10_BENCHMARK_INPUTS"]["blocked_rows"] == "18", "v70 benchmark coverage mismatch")
    require(all(row["target_evidence_rows_created"] == "0" for row in coverage), "v70 coverage cannot create evidence")
    require(all(row["leakage_pass_rows_authorized"] == "0" for row in coverage), "v70 coverage cannot authorize pass")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in coverage), "v70 coverage cannot allow scoring")
    require(len(summary) == 1, "v70 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_EVIDENCE_CANDIDATE_INGESTION_GATE_V70", "v70 summary id mismatch")
    require(row["gate_rows"] == "72", "v70 summary must record 72 rows")
    require(row["draft_evidence_candidate_rows"] == "36", "v70 summary must record 36 draft rows")
    require(row["blocked_partial_rows"] == "36", "v70 summary must record 36 blocked rows")
    require(row["galaxies_with_source_and_observed_candidates"] == "18", "v70 must cover source+observed for 18 galaxies")
    require(row["galaxies_with_all_four_evidence_candidates"] == "0", "v70 cannot claim full leakage coverage")
    require(row["target_evidence_rows_created"] == "0", "v70 cannot create target evidence")
    require(row["leakage_pass_rows_authorized"] == "0", "v70 cannot authorize leakage pass")
    require(row["activation_rows_authorized"] == "0", "v70 cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v70 summary must forbid scoring")
    require(
        row["overall_status"] == "LEAKAGE_EVIDENCE_INGESTION_GATE_PARTIAL_READY_STILL_BLOCKED",
        "v70 status mismatch",
    )


def validate_leakage_partial_candidate_sufficiency_review_package_v71() -> None:
    policy = read_csv(ROOT / "data/derived/leakage_partial_candidate_sufficiency_policy_v71.csv")
    summary = read_csv(ROOT / "data/derived/leakage_partial_candidate_sufficiency_policy_summary_v71.csv")
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
    require(len(policy) == 4, "v71 policy must cover four leakage components")
    by_id = {row["evidence_id"]: row for row in policy}
    require(
        set(by_id) == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS", "LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v71 policy evidence ids mismatch",
    )
    require(by_id["LEC10_SOURCE_ROUTE"]["v70_draft_available_rows"] == "18", "v71 source-route draft mismatch")
    require(by_id["LEC10_OBSERVED_INPUTS"]["v70_draft_available_rows"] == "18", "v71 observed-input draft mismatch")
    require(by_id["LEC10_MORPH_LABELS"]["requires_completed_sufficiency_review"] == "true", "v71 morphology must need review")
    require(by_id["LEC10_BENCHMARK_INPUTS"]["requires_completed_sufficiency_review"] == "true", "v71 benchmark must need review")
    require(
        all(row["required_for_full_leakage_pass"] == "true" for row in policy),
        "v71 must require all components for full leakage pass",
    )
    require(
        all(row["may_use_minimum_two_component_gate_for_endpoint_scoring"] == "false" for row in policy),
        "v71 cannot allow two-component endpoint scoring",
    )
    require(all(row["target_evidence_rows_created"] == "0" for row in policy), "v71 cannot create evidence")
    require(all(row["leakage_pass_authorized"] == "false" for row in policy), "v71 cannot authorize leakage pass")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in policy), "v71 cannot allow scoring")
    require(len(summary) == 1, "v71 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_POLICY_V71", "v71 summary id mismatch")
    require(row["policy_rows"] == "4", "v71 summary must record four policy rows")
    require(row["required_components_for_full_scoring_leakage_pass"] == "4", "v71 must require four components")
    require(row["components_with_full_draft_available"] == "2", "v71 must record two draft-ready components")
    require(row["components_requiring_sufficiency_review"] == "2", "v71 must record two blocked components")
    require(row["partial_candidate_rows_requiring_review"] == "36", "v71 must require review for 36 partial rows")
    require(
        row["minimum_scoring_policy"] == "FULL_FOUR_COMPONENT_LEAKAGE_REQUIRED_BEFORE_ENDPOINT_SCORING",
        "v71 minimum scoring policy mismatch",
    )
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v71 summary must forbid scoring")
    require(
        row["overall_status"] == "PARTIAL_SUFFICIENCY_REVIEW_PACKAGE_REQUIRED_BEFORE_LEAKAGE_PASS",
        "v71 overall status mismatch",
    )
    require(package_root.exists(), "v71 review package directory must exist")
    require(zip_path.exists(), "v71 review package zip must exist")
    for rel in required:
        require((package_root / rel).exists(), f"v71 package missing {rel}")
    manifest = read_csv(package_root / "REVIEW_MANIFEST.csv")
    require(len(manifest) == len(required) - 1, "v71 manifest row count mismatch")
    require(
        {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"},
        "v71 manifest package paths mismatch",
    )
    require(
        all(
            row["claim_boundary"] == "leakage_partial_candidate_sufficiency_review_package_only_no_evidence_no_scores"
            for row in manifest
        ),
        "v71 manifest claim boundary mismatch",
    )
    template = read_csv(package_root / "templates/leakage_partial_candidate_sufficiency_v71_review_response_TEMPLATE.csv")
    require(len(template) == 36, "v71 response template must cover 36 partial rows")
    require(
        {row["evidence_id"] for row in template} == {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v71 response template must only cover partial components",
    )
    require(
        all(row["sufficiency_review_decision"] == "KEEP_BLOCKED_PARTIAL_REVIEW_REQUIRED_NOT_AUTHORIZED" for row in template),
        "v71 response template must default to blocked",
    )
    require(all(row["partial_candidate_sufficient_for_later_ingestion"] == "false" for row in template), "v71 cannot pre-accept rows")
    require(all(row["may_promote_to_leakage_evidence_after_ingestion"] == "false" for row in template), "v71 cannot promote by default")
    require(all(row["may_activate_row_after_ingestion"] == "false" for row in template), "v71 cannot activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in template), "v71 cannot allow scoring")
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    require(
        {f"leakage_partial_candidate_sufficiency_v71_review_package/{rel}" for rel in required}.issubset(names),
        "v71 zip missing required package files",
    )


def validate_leakage_partial_candidate_sufficiency_review_intake_v73() -> None:
    rows = read_csv(ROOT / "data/derived/leakage_partial_candidate_sufficiency_review_intake_v73.csv")
    summary = read_csv(ROOT / "data/derived/leakage_partial_candidate_sufficiency_review_intake_summary_v73.csv")
    require(len(rows) == 36, "v73 intake must cover 36 partial rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v73 intake must cover eighteen galaxies")
    require(
        {row["evidence_id"] for row in rows} == {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v73 intake must cover only partial leakage components",
    )
    require(
        all(row["source_mode"] == "completed_response" for row in rows),
        "v73 must run from completed response after response package is present",
    )
    require(
        all(row["intake_decision"] == "ACCEPT_PARTIAL_SUFFICIENCY_FOR_LATER_LEAKAGE_EVIDENCE_GATE_NOT_EVIDENCE" for row in rows),
        "v73 must accept only partial sufficiency for later leakage-evidence ingestion",
    )
    require(
        all(row["sufficiency_candidate_status"] == "SUFFICIENCY_ACCEPTED_FOR_LATER_LEAKAGE_EVIDENCE_INGESTION" for row in rows),
        "v73 accepted rows must remain later-ingestion sufficiency only",
    )
    require(
        all(row["may_promote_to_leakage_evidence_after_ingestion"] == "true" for row in rows),
        "v73 may only permit later promotion after a separate ingestion gate",
    )
    require(all(row["may_activate_row_after_ingestion"] == "false" for row in rows), "v73 cannot activate")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v73 cannot allow scoring")
    require(len(summary) == 1, "v73 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_REVIEW_INTAKE_V73", "v73 summary id mismatch")
    require(row["response_files_present"] == "4", "v73 must record four response files")
    require(row["intake_rows"] == "36", "v73 summary must record 36 rows")
    require(row["galaxies_covered"] == "18", "v73 summary must record eighteen galaxies")
    require(row["partial_evidence_components"] == "2", "v73 summary must record two partial components")
    require(row["completed_response_present"] == "true", "v73 completed response must be present")
    require(row["accepted_sufficiency_rows"] == "36", "v73 must accept 36 sufficiency rows")
    require(row["blocked_or_missing_rows"] == "0", "v73 must clear the completed-response blocker")
    require(row["target_evidence_rows_created"] == "0", "v73 cannot create evidence")
    require(row["leakage_pass_authorized"] == "0", "v73 cannot authorize leakage pass")
    require(row["activation_rows_authorized"] == "0", "v73 cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v73 summary must forbid scoring")
    require(
        row["overall_status"] == "PARTIAL_SUFFICIENCY_REVIEW_READY_FOR_LATER_LEAKAGE_EVIDENCE_GATE",
        "v73 status mismatch",
    )
    require(
        row["next_required_artifact"] == "full_leakage_evidence_ingestion_gate_after_accepted_v71_response",
        "v73 next artifact mismatch",
    )


def validate_leakage_partial_candidate_sufficiency_preaudit_v74() -> None:
    rows = read_csv(ROOT / "data/derived/leakage_partial_candidate_sufficiency_preaudit_v74.csv")
    summary = read_csv(ROOT / "data/derived/leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv")
    require(len(rows) == 36, "v74 preaudit must cover 36 partial rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v74 preaudit must cover eighteen galaxies")
    require(
        {row["evidence_id"] for row in rows} == {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v74 preaudit must cover only partial components",
    )
    require(all(row["artifact_exists"] == "true" for row in rows), "v74 artifacts must exist")
    require(all(row["row_selector_found"] == "true" for row in rows), "v74 row selectors must resolve")
    require(all(row["source_side_fields_present"] == "true" for row in rows), "v74 source/policy fields must exist")
    require(all(row["endpoint_scoring_disabled_in_source"] == "true" for row in rows), "v74 source scoring must be disabled")
    require(all(row["not_active_or_not_run"] == "true" for row in rows), "v74 rows must be inactive or not run")
    require(all(row["forbidden_input_guard_present"] == "true" for row in rows), "v74 forbidden guards must exist")
    require(
        all(row["preaudit_decision"] == "PREAUDIT_REVIEW_READY_NOT_ACCEPTED" for row in rows),
        "v74 rows must be review-ready but not accepted",
    )
    require(all(row["target_evidence_rows_created"] == "0" for row in rows), "v74 cannot create evidence")
    require(all(row["leakage_pass_authorized"] == "false" for row in rows), "v74 cannot authorize pass")
    require(all(row["activation_rows_authorized"] == "0" for row in rows), "v74 cannot activate")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v74 cannot score")
    require(len(summary) == 1, "v74 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_PREAUDIT_V74", "v74 summary id mismatch")
    require(row["preaudit_rows"] == "36", "v74 summary must record 36 rows")
    require(row["galaxies_covered"] == "18", "v74 summary must record eighteen galaxies")
    require(row["partial_evidence_components"] == "2", "v74 summary must record two components")
    require(row["preaudit_review_ready_rows"] == "36", "v74 must mark all rows review-ready")
    require(row["preaudit_blocked_rows"] == "0", "v74 must have zero preaudit-blocked rows")
    require(row["accepted_sufficiency_rows"] == "0", "v74 cannot accept sufficiency")
    require(row["target_evidence_rows_created"] == "0", "v74 cannot create evidence")
    require(row["leakage_pass_authorized"] == "0", "v74 cannot authorize leakage pass")
    require(row["activation_rows_authorized"] == "0", "v74 cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v74 summary must forbid scoring")
    require(
        row["overall_status"] == "PARTIAL_SUFFICIENCY_PREAUDIT_REVIEW_READY_NOT_ACCEPTED",
        "v74 status mismatch",
    )


def validate_leakage_partial_candidate_sufficiency_response_draft_v75() -> None:
    package_root = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package"
    zip_path = ROOT / "review_packages/leakage_partial_candidate_sufficiency_v75_response_draft_package.zip"
    summary = read_csv(ROOT / "data/derived/leakage_partial_candidate_sufficiency_response_draft_summary_v75.csv")
    required = {
        "README.md",
        "DO_NOT_INGEST_WITHOUT_INDEPENDENT_REVIEW.md",
        "REVIEW_MANIFEST.csv",
        "templates/leakage_partial_candidate_sufficiency_v71_review_response_DRAFT.csv",
        "data/leakage_partial_candidate_sufficiency_response_draft_summary_v75.csv",
        "data/leakage_partial_candidate_sufficiency_preaudit_v74.csv",
        "data/leakage_partial_candidate_sufficiency_preaudit_summary_v74.csv",
    }
    require(package_root.exists(), "v75 draft package directory must exist")
    require(zip_path.exists(), "v75 draft package zip must exist")
    for rel in required:
        require((package_root / rel).exists(), f"v75 package missing {rel}")
    manifest = read_csv(package_root / "REVIEW_MANIFEST.csv")
    require(len(manifest) == len(required) - 1, "v75 manifest row count mismatch")
    require(
        {row["package_path"] for row in manifest} == required - {"REVIEW_MANIFEST.csv"},
        "v75 manifest package paths mismatch",
    )
    require(
        all(row["claim_boundary"] == "leakage_partial_candidate_sufficiency_response_draft_only_no_evidence_no_scores" for row in manifest),
        "v75 manifest claim boundary mismatch",
    )
    rows = read_csv(package_root / "templates/leakage_partial_candidate_sufficiency_v71_review_response_DRAFT.csv")
    require(len(rows) == 36, "v75 draft response must cover 36 rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v75 draft response must cover eighteen galaxies")
    require(
        {row["evidence_id"] for row in rows} == {"LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v75 draft must cover only partial components",
    )
    require(
        all(row["sufficiency_review_decision"] == "ACCEPT_PARTIAL_CANDIDATE_SUFFICIENT_FOR_LATER_INGESTION_GATE" for row in rows),
        "v75 draft must propose accept decisions",
    )
    require(all(row["partial_candidate_sufficient_for_later_ingestion"] == "true" for row in rows), "v75 draft must propose sufficiency")
    require(all(row["minimal_required_fields_covered"] == "true" for row in rows), "v75 draft must propose field coverage")
    require(all(row["artifact_is_prescore"] == "true" for row in rows), "v75 draft must keep prescore status")
    require(all(row["artifact_uses_forbidden_inputs"] == "false" for row in rows), "v75 draft must propose no forbidden inputs")
    require(all(row["may_promote_to_leakage_evidence_after_ingestion"] == "true" for row in rows), "v75 draft must propose later ingestion only")
    require(all(row["may_activate_row_after_ingestion"] == "false" for row in rows), "v75 draft cannot activate")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v75 draft cannot score")
    require(len(summary) == 1, "v75 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_PARTIAL_CANDIDATE_SUFFICIENCY_RESPONSE_DRAFT_V75", "v75 summary id mismatch")
    require(row["draft_rows"] == "36", "v75 summary must record 36 draft rows")
    require(row["proposed_accept_rows"] == "36", "v75 must propose 36 accept rows")
    require(row["proposed_block_rows"] == "0", "v75 must propose zero blocked rows")
    require(row["completed_response_created"] == "false", "v75 must not create completed response")
    require(row["target_evidence_rows_created"] == "0", "v75 cannot create evidence")
    require(row["leakage_pass_authorized"] == "0", "v75 cannot authorize leakage pass")
    require(row["activation_rows_authorized"] == "0", "v75 cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v75 summary must forbid scoring")
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    require(
        {f"leakage_partial_candidate_sufficiency_v75_response_draft_package/{rel}" for rel in required}.issubset(names),
        "v75 zip missing required package files",
    )


def validate_full_leakage_evidence_ingestion_gate_v76() -> None:
    rows = read_csv(ROOT / "data/derived/full_leakage_evidence_ingestion_gate_v76.csv")
    coverage = read_csv(ROOT / "data/derived/full_leakage_evidence_ingestion_coverage_v76.csv")
    summary = read_csv(ROOT / "data/derived/full_leakage_evidence_ingestion_summary_v76.csv")
    require(len(rows) == 72, "v76 must cover 72 leakage component rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v76 must cover eighteen galaxies")
    require(
        {row["evidence_id"] for row in rows}
        == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS", "LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v76 must cover all four leakage evidence components",
    )
    require(
        all(row["full_ingestion_decision"] == "READY_FOR_LEAKAGE_EVIDENCE_ROW_WRITE_NOT_WRITTEN" for row in rows),
        "v76 rows must be ready for later evidence write only",
    )
    require(
        all(row["full_ingestion_component_status"] == "FULL_COMPONENT_READY_NOT_ACTIVE_EVIDENCE" for row in rows),
        "v76 rows must not become active evidence",
    )
    require(all(row["target_evidence_row_written"] == "false" for row in rows), "v76 cannot write target evidence rows")
    require(all(row["leakage_pass_authorized"] == "false" for row in rows), "v76 cannot authorize leakage pass")
    require(all(row["activation_rows_authorized"] == "0" for row in rows), "v76 cannot authorize activation")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v76 cannot allow scoring")
    require(len(coverage) == 18, "v76 coverage must have eighteen galaxy rows")
    require(all(row["ready_components"] == "4" for row in coverage), "v76 coverage must have four ready components")
    require(all(row["missing_components"] == "" for row in coverage), "v76 coverage must have no missing components")
    require(
        all(row["full_leakage_evidence_ingestion_ready"] == "true" for row in coverage),
        "v76 coverage must mark all galaxies ready",
    )
    require(all(row["target_evidence_rows_created"] == "0" for row in coverage), "v76 coverage cannot create evidence")
    require(all(row["leakage_pass_authorized"] == "false" for row in coverage), "v76 coverage cannot authorize leakage pass")
    require(all(row["activation_rows_authorized"] == "0" for row in coverage), "v76 coverage cannot authorize activation")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in coverage), "v76 coverage cannot allow scoring")
    require(len(summary) == 1, "v76 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "FULL_LEAKAGE_EVIDENCE_INGESTION_GATE_V76", "v76 summary id mismatch")
    require(row["gate_rows"] == "72", "v76 summary must record 72 rows")
    require(row["galaxies_covered"] == "18", "v76 summary must record eighteen galaxies")
    require(row["ready_component_rows"] == "72", "v76 summary must record 72 ready components")
    require(row["galaxies_with_all_four_ready_components"] == "18", "v76 summary must record 18 complete galaxies")
    require(row["target_evidence_rows_created"] == "0", "v76 summary cannot create evidence")
    require(row["leakage_pass_rows_authorized"] == "0", "v76 summary cannot authorize leakage pass")
    require(row["activation_rows_authorized"] == "0", "v76 summary cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v76 summary must forbid scoring")
    require(
        row["overall_status"] == "FULL_LEAKAGE_EVIDENCE_INGESTION_READY_FOR_TARGET_EVIDENCE_WRITE",
        "v76 status mismatch",
    )
    require(
        row["next_required_artifact"] == "leakage_audit_evidence_v10_writer_from_v76_full_ingestion_gate",
        "v76 next artifact mismatch",
    )


def validate_leakage_audit_evidence_v10_writer_v77() -> None:
    rows = read_csv(ROOT / "data/input/leakage_audit_evidence_v10.csv")
    coverage = read_csv(ROOT / "data/derived/leakage_audit_evidence_v10_writer_coverage_v77.csv")
    summary = read_csv(ROOT / "data/derived/leakage_audit_evidence_v10_writer_summary_v77.csv")
    require(len(rows) == 72, "v77 must write 72 target evidence rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v77 must cover eighteen galaxies")
    require(
        {row["evidence_id"] for row in rows}
        == {"LEC10_SOURCE_ROUTE", "LEC10_OBSERVED_INPUTS", "LEC10_MORPH_LABELS", "LEC10_BENCHMARK_INPUTS"},
        "v77 must write all four leakage evidence components",
    )
    require(all(row["review_decision"] == "READY_FOR_LEAKAGE_REVIEW_NOT_PASS" for row in rows), "v77 rows must await review")
    require(
        all(row["evidence_status"] == "TARGET_EVIDENCE_ROW_WRITTEN_REVIEW_PENDING" for row in rows),
        "v77 rows must be written but review-pending",
    )
    require(all(row["reviewer_leakage_pass_authorized"] == "false" for row in rows), "v77 cannot authorize leakage pass")
    require(all(row["may_activate_row_after_ingestion"] == "false" for row in rows), "v77 cannot authorize activation")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v77 cannot allow scoring")
    require(len(coverage) == 18, "v77 coverage must have eighteen galaxy rows")
    require(all(row["target_evidence_rows_written"] == "4" for row in coverage), "v77 coverage must write four rows per galaxy")
    require(all(row["leakage_review_ready"] == "true" for row in coverage), "v77 coverage must be review-ready")
    require(all(row["leakage_pass_authorized"] == "false" for row in coverage), "v77 coverage cannot authorize leakage pass")
    require(all(row["activation_rows_authorized"] == "0" for row in coverage), "v77 coverage cannot authorize activation")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in coverage), "v77 coverage cannot allow scoring")
    require(len(summary) == 1, "v77 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_AUDIT_EVIDENCE_V10_WRITER_V77", "v77 summary id mismatch")
    require(row["target_evidence_file"] == "data/input/leakage_audit_evidence_v10.csv", "v77 target file mismatch")
    require(row["target_evidence_rows_written"] == "72", "v77 summary must record 72 written rows")
    require(row["galaxies_covered"] == "18", "v77 summary must record eighteen galaxies")
    require(row["galaxies_ready_for_leakage_review"] == "18", "v77 summary must mark 18 galaxies review-ready")
    require(row["leakage_pass_rows_authorized"] == "0", "v77 summary cannot authorize leakage pass")
    require(row["activation_rows_authorized"] == "0", "v77 summary cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v77 summary must forbid scoring")
    require(
        row["overall_status"] == "LEAKAGE_AUDIT_EVIDENCE_WRITTEN_REVIEW_PENDING",
        "v77 status mismatch",
    )
    require(
        row["next_required_artifact"] == "leakage_audit_pass_review_gate_after_v10_evidence",
        "v77 next artifact mismatch",
    )


def validate_leakage_audit_pass_review_gate_v78() -> None:
    rows = read_csv(ROOT / "data/derived/leakage_audit_pass_review_gate_v78.csv")
    coverage = read_csv(ROOT / "data/derived/leakage_audit_pass_review_coverage_v78.csv")
    summary = read_csv(ROOT / "data/derived/leakage_audit_pass_review_summary_v78.csv")
    require(len(rows) == 72, "v78 must review 72 leakage components")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v78 must cover eighteen galaxies")
    require(all(row["pass_review_decision"] == "LEAKAGE_COMPONENT_PASS_REVIEWED_NO_ACTIVATION" for row in rows), "v78 must pass reviewed components")
    require(all(row["leakage_component_pass_authorized"] == "true" for row in rows), "v78 must authorize component pass")
    require(all(row["activation_rows_authorized"] == "0" for row in rows), "v78 cannot authorize activation")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v78 cannot allow scoring")
    require(len(coverage) == 18, "v78 coverage must have eighteen rows")
    require(all(row["passed_leakage_components"] == "4" for row in coverage), "v78 must pass four components per galaxy")
    require(all(row["galaxy_leakage_pass_authorized"] == "true" for row in coverage), "v78 must authorize galaxy leakage pass")
    require(all(row["activation_rows_authorized"] == "0" for row in coverage), "v78 coverage cannot authorize activation")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in coverage), "v78 coverage cannot allow scoring")
    require(len(summary) == 1, "v78 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "LEAKAGE_AUDIT_PASS_REVIEW_GATE_V78", "v78 summary id mismatch")
    require(row["component_rows_reviewed"] == "72", "v78 must review 72 components")
    require(row["component_pass_rows_authorized"] == "72", "v78 must pass 72 components")
    require(row["galaxies_covered"] == "18", "v78 must cover eighteen galaxies")
    require(row["galaxy_leakage_pass_rows_authorized"] == "18", "v78 must pass eighteen galaxies")
    require(row["activation_rows_authorized"] == "0", "v78 cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v78 must forbid scoring")
    require(row["overall_status"] == "LEAKAGE_AUDIT_PASS_REVIEWED_ACTIVATION_PENDING", "v78 status mismatch")
    require(
        row["next_required_artifact"] == "scoring_row_activation_policy_v79",
        "v78 next artifact mismatch",
    )


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
    require(all(row["input_file_status"] == "REAL_VALUE_HEADER_OK" for row in gates), "v12 input file must be present")
    require(sum(int(row["imported_numeric_rows"]) for row in gates) == 450, "v12 must import 450 numeric rows")
    require(
        all(row["real_value_gate_status"] == "REAL_VALUES_PRESENT_VALIDATION_PENDING_LEAKAGE" for row in gates),
        "v12 gate must be leakage-pending",
    )
    require(
        all(row["activation_decision"] == "VALUE_GATE_PASSED_PENDING_LEAKAGE" for row in gates),
        "v12 value gate must pass pending leakage",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in gates), "v12 gates cannot allow scoring")
    require(len(summary) == 1, "v12 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SOURCE_IMPORT_REAL_VALUES_READY_FOR_LEAKAGE", "v12 real-value import must be leakage-ready")
    require(row["expected_galaxy_rows"] == "18", "v12 summary must expect eighteen rows")
    require(row["galaxies_with_imported_rows"] == "18", "v12 must import eighteen galaxies")
    require(row["imported_numeric_rows"] == "450", "v12 must import 450 numeric rows")
    require(row["rows_passing_value_gate"] == "18", "v12 must pass eighteen value gates")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v12 summary must forbid scoring")
    require(row["next_required_artifact"] == "data/derived/source_import_leakage_summary_v09.csv", "v12 must point to leakage audit")


def validate_scoring_activation_gate_v13() -> None:
    gates = read_csv(ROOT / "data/derived/scoring_activation_gate_v13.csv")
    blockers = read_csv(ROOT / "data/derived/scoring_activation_global_blockers_v13.csv")
    summary = read_csv(ROOT / "data/derived/scoring_activation_summary_v13.csv")
    require(len(gates) == 18, "v13 activation gate must cover eighteen rows")
    require(all(row["activation_decision"] == "ACTIVATE_FOR_SCORING" for row in gates), "v13 must activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in gates), "v13 row gates cannot allow scoring")
    require(all("real_source_values_missing" not in row["blocking_requirements"] for row in gates), "v13 rows must not be blocked by missing real values")
    require(all("leakage_audit_not_passed" not in row["blocking_requirements"] for row in gates), "v13 rows must clear leakage blocker")
    require(all("source_row_not_activated" not in row["blocking_requirements"] for row in gates), "v13 rows must clear source row activation")
    require(len(blockers) == 4, "v13 must list four global blockers")
    ready_blockers = {row["blocker_id"] for row in blockers if row["current_status"] == "READY"}
    blocked_blockers = {row["blocker_id"] for row in blockers if row["current_status"] == "BLOCKED"}
    require(
        ready_blockers
        == {"SAG13_FAMILY_FORMULA_TABLES", "SAG13_PARAMETER_COUNTS", "SAG13_CONTROL_RUNNERS", "SAG13_DECISION_THRESHOLDS"},
        "v13 must ready family formula, parameter-count, control-runner, and threshold blockers",
    )
    require(
        blocked_blockers == set(),
        "v13 must clear global blockers before scoring preflight",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in blockers), "v13 blockers cannot allow scoring")
    require(len(summary) == 1, "v13 summary must have one row")
    row = summary[0]
    require(
        row["overall_status"] == "SCORING_ACTIVATION_READY_GLOBAL_PREREQUISITES_READY",
        "v13 row activation must be ready with global prerequisites cleared",
    )
    require(row["candidate_rows"] == "18", "v13 summary must cover eighteen candidate rows")
    require(row["rows_activated_for_scoring"] == "18", "v13 must activate eighteen rows")
    require(row["row_level_blocked_rows"] == "0", "v13 must block zero rows at row level")
    require(row["global_blockers"] == "0", "v13 must report zero global blockers")
    require(
        row["next_required_artifact"] == "scoring_preflight_v07.csv",
        "v13 scoring activation must point to scoring preflight",
    )
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v13 summary must forbid scoring")


def validate_scoring_row_activation_policy_v79() -> None:
    rows = read_csv(ROOT / "data/derived/activated_scoring_rows_v10.csv")
    summary = read_csv(ROOT / "data/derived/scoring_row_activation_policy_summary_v79.csv")
    require(len(rows) == 18, "v79 activation policy must cover eighteen rows")
    require(all(row["activation_status"] == "ACTIVATED" for row in rows), "v79 must activate all rows")
    require(all(row["activation_policy_blockers"] == "" for row in rows), "v79 rows must have no activation policy blockers")
    require(all(row["leakage_audit_status"] == "LEAKAGE_AUDIT_PASS" for row in rows), "v79 rows must inherit leakage pass")
    require(all(row["v78_leakage_pass_authorized"] == "true" for row in rows), "v79 rows must inherit v78 pass authorization")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v79 rows cannot allow scoring")
    require(len(summary) == 1, "v79 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "SCORING_ROW_ACTIVATION_POLICY_V79", "v79 summary id mismatch")
    require(row["candidate_rows"] == "18", "v79 must summarize eighteen rows")
    require(row["activated_rows_written"] == "18", "v79 must write eighteen activated rows")
    require(row["blocked_rows"] == "0", "v79 must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v79 summary must forbid scoring")
    require(
        row["overall_status"] == "SCORING_ROW_ACTIVATION_POLICY_READY_GLOBAL_SCORING_BLOCKED",
        "v79 status mismatch",
    )
    require(row["next_required_artifact"] == "family_prediction_tables_v08.csv", "v79 next artifact mismatch")


def validate_m0_no_dark_rule_parent_assumption_basis_v14() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_rule_parent_assumption_basis_v14.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_rule_parent_assumption_basis_summary_v14.csv")
    require(len(rows) == 6, "M0 v14 parent basis must define six basis rows")
    require(
        {row["basis_id"] for row in rows}
        == {
            "M0NDPB14_SOURCE_FREEZE",
            "M0NDPB14_NO_DARK_RESPONSE_EXCLUSION",
            "M0NDPB14_MORPHOLOGY_READOUT",
            "M0NDPB14_LOCAL_CLOSURE_DIAGNOSTIC",
            "M0NDPB14_BARYONIC_INPUT_BOUNDARY",
            "M0NDPB14_FAILURE_POLICY",
        },
        "M0 v14 parent basis ids mismatch",
    )
    require(all(row["basis_status"] == "READY" for row in rows), "M0 v14 basis rows must be ready")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v14 cannot allow scoring")
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v14 cannot claim a source rule")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v14 cannot claim an expression")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v14 cannot write predictions")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v14 must forbid residual leakage")
    require(len(summary) == 1, "M0 v14 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_RULE_PARENT_ASSUMPTION_BASIS_V14", "M0 v14 summary id mismatch")
    require(row["basis_artifact"] == "m0_no_dark_rule_parent_assumption_basis_v14", "M0 v14 artifact id mismatch")
    require(row["basis_rows"] == "6", "M0 v14 must summarize six basis rows")
    require(row["ready_basis_rows"] == "6", "M0 v14 must ready six basis rows")
    require(row["blocked_basis_rows"] == "0", "M0 v14 must block zero basis rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v14 summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_RULE_PARENT_ASSUMPTION_BASIS_READY", "M0 v14 status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_rule_selection_map_v14", "M0 v14 next artifact mismatch")


def validate_m0_no_dark_rule_selection_map_v14() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_rule_selection_map_v14.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_rule_selection_map_summary_v14.csv")
    require(len(rows) == 6, "M0 v14 selection map must define six selection rows")
    require(
        {row["selection_id"] for row in rows}
        == {
            "M0NDRSM14_SOURCE_FREEZE_TO_INPUT_DOMAIN",
            "M0NDRSM14_NO_DARK_TO_RESPONSE_EXCLUSION",
            "M0NDRSM14_MORPHOLOGY_TO_SOURCE_TERMS",
            "M0NDRSM14_U_READ_TO_ADMISSIBILITY_ORDER",
            "M0NDRSM14_BARYONIC_BOUNDARY_TO_BINDINGS",
            "M0NDRSM14_FAILURE_POLICY_TO_BLOCK_ROUTE",
        },
        "M0 v14 selection ids mismatch",
    )
    require(all(row["selection_status"] == "READY" for row in rows), "M0 v14 selection rows must be ready")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v14 selection cannot allow scoring")
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v14 selection cannot claim a source rule")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v14 selection cannot claim an expression")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v14 selection cannot write predictions")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v14 selection must forbid residual leakage")
    require(len(summary) == 1, "M0 v14 selection summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_RULE_SELECTION_MAP_V14", "M0 v14 selection summary id mismatch")
    require(row["selection_artifact"] == "m0_no_dark_rule_selection_map_v14", "M0 v14 selection artifact id mismatch")
    require(row["parent_basis_status"] == "READY", "M0 v14 selection must inherit ready parent basis")
    require(row["selection_rows"] == "6", "M0 v14 selection must summarize six rows")
    require(row["ready_selection_rows"] == "6", "M0 v14 selection must ready six rows")
    require(row["blocked_selection_rows"] == "0", "M0 v14 selection must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v14 selection summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_RULE_SELECTION_MAP_READY", "M0 v14 selection status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_rule_term_generation_record_v14", "M0 v14 selection next artifact mismatch")


def validate_m0_no_dark_rule_term_generation_record_v14() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_rule_term_generation_record_v14.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_rule_term_generation_record_summary_v14.csv")
    require(len(rows) == 6, "M0 v14 term generation must define six term rows")
    require(
        {row["term_record_id"] for row in rows}
        == {
            "M0NDTG14_INPUT_DOMAIN_TERM",
            "M0NDTG14_NO_DARK_EXCLUSION_TERM",
            "M0NDTG14_MORPHOLOGY_SOURCE_TERM_CLASS",
            "M0NDTG14_U_READ_ADMISSIBILITY_MARKER",
            "M0NDTG14_BARYONIC_BINDING_TERM_CLASS",
            "M0NDTG14_FAILURE_ROUTE_TERM",
        },
        "M0 v14 term record ids mismatch",
    )
    require(all(row["term_generation_status"] == "READY" for row in rows), "M0 v14 term rows must be ready")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v14 terms cannot allow scoring")
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v14 terms cannot claim a source rule")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v14 terms cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v14 terms cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v14 terms cannot write predictions")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v14 terms must forbid residual leakage")
    require(len(summary) == 1, "M0 v14 term summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_RULE_TERM_GENERATION_RECORD_V14", "M0 v14 term summary id mismatch")
    require(row["term_generation_artifact"] == "m0_no_dark_rule_term_generation_record_v14", "M0 v14 term artifact id mismatch")
    require(row["selection_map_status"] == "READY", "M0 v14 term generation must inherit ready selection map")
    require(row["term_rows"] == "6", "M0 v14 term generation must summarize six rows")
    require(row["ready_term_rows"] == "6", "M0 v14 term generation must ready six rows")
    require(row["blocked_term_rows"] == "0", "M0 v14 term generation must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v14 term summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_RULE_TERM_GENERATION_RECORD_READY", "M0 v14 term status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_rule_invariance_null_checks_v14", "M0 v14 term next artifact mismatch")


def validate_m0_no_dark_rule_invariance_null_checks_v14() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_rule_invariance_null_checks_v14.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_rule_invariance_null_checks_summary_v14.csv")
    require(len(rows) == 6, "M0 v14 invariance/null checks must define six rows")
    require(
        {row["check_id"] for row in rows}
        == {
            "M0NDINC14_INPUT_DOMAIN_NULL_CHECK",
            "M0NDINC14_NO_DARK_EXCLUSION_CHECK",
            "M0NDINC14_MORPHOLOGY_SOURCE_INVARIANCE_CHECK",
            "M0NDINC14_U_READ_INCOMPARABILITY_CHECK",
            "M0NDINC14_BARYONIC_BINDING_CHECK",
            "M0NDINC14_FAILURE_ROUTE_CHECK",
        },
        "M0 v14 invariance/null check ids mismatch",
    )
    require(all(row["check_status"] == "READY" for row in rows), "M0 v14 invariance/null checks must be ready")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v14 checks cannot allow scoring")
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v14 checks cannot claim a source rule")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v14 checks cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v14 checks cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v14 checks cannot write predictions")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v14 checks must forbid residual leakage")
    require(len(summary) == 1, "M0 v14 invariance summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_RULE_INVARIANCE_NULL_CHECKS_V14", "M0 v14 invariance summary id mismatch")
    require(row["check_artifact"] == "m0_no_dark_rule_invariance_null_checks_v14", "M0 v14 invariance artifact id mismatch")
    require(row["term_generation_status"] == "READY", "M0 v14 invariance must inherit ready term generation")
    require(row["check_rows"] == "6", "M0 v14 invariance must summarize six rows")
    require(row["ready_check_rows"] == "6", "M0 v14 invariance must ready six rows")
    require(row["blocked_check_rows"] == "0", "M0 v14 invariance must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v14 invariance summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_RULE_INVARIANCE_NULL_CHECKS_READY", "M0 v14 invariance status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_rule_dimensional_precheck_v14", "M0 v14 invariance next artifact mismatch")


def validate_m0_no_dark_rule_dimensional_precheck_v14() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_rule_dimensional_precheck_v14.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_rule_dimensional_precheck_summary_v14.csv")
    require(len(rows) == 6, "M0 v14 dimensional precheck must define six rows")
    require(
        {row["precheck_id"] for row in rows}
        == {
            "M0NDDP14_INPUT_DOMAIN_DIMENSION_ROUTE",
            "M0NDDP14_NO_DARK_EXCLUSION_DIMENSION_ROUTE",
            "M0NDDP14_MORPHOLOGY_SOURCE_DIMENSION_ROUTE",
            "M0NDDP14_U_READ_DIMENSIONLESS_ORDER_ROUTE",
            "M0NDDP14_BARYONIC_BINDING_DIMENSION_ROUTE",
            "M0NDDP14_FAILURE_ROUTE_DIMENSION_SAFE_BLOCK",
        },
        "M0 v14 dimensional precheck ids mismatch",
    )
    require(all(row["dimensional_precheck_status"] == "READY" for row in rows), "M0 v14 dimensional precheck rows must be ready")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v14 dimensional precheck cannot allow scoring")
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v14 dimensional precheck cannot claim a source rule")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v14 dimensional precheck cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v14 dimensional precheck cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v14 dimensional precheck cannot write predictions")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v14 dimensional precheck must forbid residual leakage")
    require(len(summary) == 1, "M0 v14 dimensional precheck summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_RULE_DIMENSIONAL_PRECHECK_V14", "M0 v14 dimensional precheck summary id mismatch")
    require(row["precheck_artifact"] == "m0_no_dark_rule_dimensional_precheck_v14", "M0 v14 dimensional precheck artifact id mismatch")
    require(row["invariance_null_status"] == "READY", "M0 v14 dimensional precheck must inherit ready invariance/null checks")
    require(row["precheck_rows"] == "6", "M0 v14 dimensional precheck must summarize six rows")
    require(row["ready_precheck_rows"] == "6", "M0 v14 dimensional precheck must ready six rows")
    require(row["blocked_precheck_rows"] == "0", "M0 v14 dimensional precheck must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v14 dimensional precheck summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_RULE_DIMENSIONAL_PRECHECK_READY", "M0 v14 dimensional precheck status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_rule_derivation_provenance_leakage_v14", "M0 v14 dimensional precheck next artifact mismatch")


def validate_m0_no_dark_rule_derivation_provenance_leakage_v14() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_rule_derivation_provenance_leakage_v14.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_rule_derivation_provenance_leakage_summary_v14.csv")
    require(len(rows) == 6, "M0 v14 derivation provenance/leakage audit must define six rows")
    require(
        {row["audit_id"] for row in rows}
        == {
            "M0NDPAL14_PARENT_BASIS_PROVENANCE",
            "M0NDPAL14_SELECTION_MAP_PROVENANCE",
            "M0NDPAL14_TERM_GENERATION_PROVENANCE",
            "M0NDPAL14_INVARIANCE_NULL_PROVENANCE",
            "M0NDPAL14_DIMENSIONAL_PRECHECK_PROVENANCE",
            "M0NDPAL14_FRONTIER_HANDOFF",
        },
        "M0 v14 derivation provenance/leakage audit ids mismatch",
    )
    require(all(row["audit_status"] == "READY" for row in rows), "M0 v14 derivation provenance/leakage rows must be ready")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v14 derivation provenance/leakage cannot allow scoring")
    require(all(row["derivation_claim_allowed"] == "false" for row in rows), "M0 v14 derivation provenance/leakage cannot claim derivation")
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v14 derivation provenance/leakage cannot claim a source rule")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v14 derivation provenance/leakage cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v14 derivation provenance/leakage cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v14 derivation provenance/leakage cannot write predictions")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v14 derivation provenance/leakage must forbid residual leakage")
    require(len(summary) == 1, "M0 v14 derivation provenance/leakage summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_RULE_DERIVATION_PROVENANCE_LEAKAGE_V14", "M0 v14 derivation provenance/leakage summary id mismatch")
    require(row["audit_artifact"] == "m0_no_dark_rule_derivation_provenance_leakage_v14", "M0 v14 derivation provenance/leakage artifact id mismatch")
    require(row["dimensional_precheck_status"] == "READY", "M0 v14 derivation provenance/leakage must inherit ready dimensional precheck")
    require(row["audit_rows"] == "6", "M0 v14 derivation provenance/leakage must summarize six rows")
    require(row["ready_audit_rows"] == "6", "M0 v14 derivation provenance/leakage must ready six rows")
    require(row["blocked_audit_rows"] == "0", "M0 v14 derivation provenance/leakage must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v14 derivation provenance/leakage summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_RULE_DERIVATION_PROVENANCE_LEAKAGE_READY", "M0 v14 derivation provenance/leakage status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_expression_source_basis_v13", "M0 v14 derivation provenance/leakage next artifact mismatch")


def validate_m0_no_dark_expression_rule_derivation_contract_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_expression_rule_derivation_contract_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_expression_rule_derivation_contract_summary_v13.csv")
    require(len(rows) == 6, "M0 v13 rule derivation contract must define six slots")
    require(
        {row["derivation_slot_id"] for row in rows}
        == {
            "M0NDER13_PARENT_ASSUMPTIONS",
            "M0NDER13_RULE_SELECTION_MAP",
            "M0NDER13_TERM_GENERATION",
            "M0NDER13_INVARIANCE_CHECKS",
            "M0NDER13_DIMENSIONAL_PRECHECK",
            "M0NDER13_PROVENANCE_AND_LEAKAGE",
        },
        "M0 v13 derivation slot ids mismatch",
    )
    require(all(row["derivation_claim_allowed"] == "false" for row in rows), "M0 v13 cannot allow derivation claims")
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v13 cannot allow source-rule claims")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v13 cannot allow expression claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v13 cannot allow numeric predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v13 must forbid residual leakage")
    require(rows[0]["completion_status"] == "READY", "M0 v13 parent-basis slot must be ready")
    require(rows[0]["next_required_artifact"] == "m0_no_dark_rule_parent_assumption_basis_v14", "M0 v13 parent-basis artifact mismatch")
    require(rows[1]["completion_status"] == "READY", "M0 v13 rule-selection slot must be ready")
    require(rows[1]["next_required_artifact"] == "m0_no_dark_rule_selection_map_v14", "M0 v13 next rule-selection artifact mismatch")
    require(rows[2]["completion_status"] == "READY", "M0 v13 term-generation slot must be ready")
    require(rows[2]["next_required_artifact"] == "m0_no_dark_rule_term_generation_record_v14", "M0 v13 next term-generation artifact mismatch")
    require(rows[3]["completion_status"] == "READY", "M0 v13 invariance slot must be ready")
    require(rows[3]["next_required_artifact"] == "m0_no_dark_rule_invariance_null_checks_v14", "M0 v13 next invariance artifact mismatch")
    require(rows[4]["completion_status"] == "READY", "M0 v13 dimensional slot must be ready")
    require(rows[4]["next_required_artifact"] == "m0_no_dark_rule_dimensional_precheck_v14", "M0 v13 next dimensional artifact mismatch")
    require(rows[5]["completion_status"] == "READY", "M0 v13 provenance/leakage slot must be ready")
    require(rows[5]["next_required_artifact"] == "m0_no_dark_rule_derivation_provenance_leakage_v14", "M0 v13 next provenance/leakage artifact mismatch")
    require(len(summary) == 1, "M0 v13 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXPRESSION_RULE_DERIVATION_CONTRACT_V13", "M0 v13 summary id mismatch")
    require(row["rule_derivation_artifact"] == "m0_no_dark_expression_rule_derivation_v13", "M0 v13 artifact id mismatch")
    require(row["required_derivation_slots"] == "6", "M0 v13 must require six derivation slots")
    require(row["ready_derivation_slots"] == "6", "M0 v13 must ready six derivation slots")
    require(row["blocked_derivation_slots"] == "0", "M0 v13 must block zero derivation slots")
    require(row["derivation_records_written"] == "0", "M0 v13 must write zero derivation records")
    require(row["numeric_predictions_written"] == "0", "M0 v13 must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_EXPRESSION_RULE_DERIVATION_READY_FOR_SOURCE_BASIS",
        "M0 v13 status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_expression_source_basis_v13", "M0 v13 next artifact mismatch")


def validate_m0_no_dark_expression_source_basis_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_expression_source_basis_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_expression_source_basis_summary_v13.csv")
    require(len(rows) == 6, "M0 v13 source basis must define six rows")
    require(
        {row["basis_id"] for row in rows}
        == {
            "M0NDESB13_SOURCE_FREEZE_BASIS",
            "M0NDESB13_NO_DARK_EXCLUSION_BASIS",
            "M0NDESB13_MORPHOLOGY_READOUT_BASIS",
            "M0NDESB13_U_READ_ADMISSIBILITY_BASIS",
            "M0NDESB13_BARYONIC_BINDING_BASIS",
            "M0NDESB13_FAILURE_ROUTE_BASIS",
        },
        "M0 v13 source basis ids mismatch",
    )
    require(all(row["basis_status"] == "READY" for row in rows), "M0 v13 source basis rows must be ready")
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v13 source basis cannot claim a source rule")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v13 source basis cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v13 source basis cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v13 source basis cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 source basis cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v13 source basis must forbid residual leakage")
    require(len(summary) == 1, "M0 v13 source basis summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXPRESSION_SOURCE_BASIS_V13", "M0 v13 source basis summary id mismatch")
    require(row["source_basis_artifact"] == "m0_no_dark_expression_source_basis_v13", "M0 v13 source basis artifact id mismatch")
    require(row["derivation_contract_status"] == "READY", "M0 v13 source basis must inherit ready derivation contract")
    require(row["basis_rows"] == "6", "M0 v13 source basis must summarize six rows")
    require(row["ready_basis_rows"] == "6", "M0 v13 source basis must ready six rows")
    require(row["blocked_basis_rows"] == "0", "M0 v13 source basis must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 source basis summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_EXPRESSION_SOURCE_BASIS_READY", "M0 v13 source basis status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_expression_admissibility_rule_v13", "M0 v13 source basis next artifact mismatch")


def validate_m0_no_dark_expression_admissibility_rule_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_expression_admissibility_rule_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_expression_admissibility_rule_summary_v13.csv")
    require(len(rows) == 6, "M0 v13 admissibility rule must define six rows")
    require(
        {row["admissibility_id"] for row in rows}
        == {
            "M0NDADM13_SOURCE_FREEZE_ADMISSIBILITY",
            "M0NDADM13_NO_DARK_EXCLUSION_ADMISSIBILITY",
            "M0NDADM13_MORPHOLOGY_READOUT_ADMISSIBILITY",
            "M0NDADM13_U_READ_MARKER_ADMISSIBILITY",
            "M0NDADM13_BARYONIC_BINDING_ADMISSIBILITY",
            "M0NDADM13_FAILURE_ROUTE_ADMISSIBILITY",
        },
        "M0 v13 admissibility rule ids mismatch",
    )
    require(all(row["admissibility_status"] == "READY" for row in rows), "M0 v13 admissibility rows must be ready")
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v13 admissibility cannot claim a source rule")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v13 admissibility cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v13 admissibility cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v13 admissibility cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 admissibility cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v13 admissibility must forbid residual leakage")
    require(len(summary) == 1, "M0 v13 admissibility summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXPRESSION_ADMISSIBILITY_RULE_V13", "M0 v13 admissibility summary id mismatch")
    require(row["admissibility_artifact"] == "m0_no_dark_expression_admissibility_rule_v13", "M0 v13 admissibility artifact id mismatch")
    require(row["source_basis_status"] == "READY", "M0 v13 admissibility must inherit ready source basis")
    require(row["admissibility_rows"] == "6", "M0 v13 admissibility must summarize six rows")
    require(row["ready_admissibility_rows"] == "6", "M0 v13 admissibility must ready six rows")
    require(row["blocked_admissibility_rows"] == "0", "M0 v13 admissibility must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 admissibility summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_EXPRESSION_ADMISSIBILITY_RULE_READY", "M0 v13 admissibility status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_expression_null_fallback_policy_v13", "M0 v13 admissibility next artifact mismatch")


def validate_m0_no_dark_expression_null_fallback_policy_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_expression_null_fallback_policy_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_expression_null_fallback_policy_summary_v13.csv")
    require(len(rows) == 6, "M0 v13 null/fallback policy must define six rows")
    require(
        {row["policy_id"] for row in rows}
        == {
            "M0NDNFB13_SOURCE_FREEZE_NULL_POLICY",
            "M0NDNFB13_NO_DARK_CONSTRAINT_POLICY",
            "M0NDNFB13_MORPHOLOGY_LABEL_POLICY",
            "M0NDNFB13_U_READ_INCOMPARABILITY_POLICY",
            "M0NDNFB13_BARYONIC_BINDING_POLICY",
            "M0NDNFB13_FAILURE_ROUTE_POLICY",
        },
        "M0 v13 null/fallback policy ids mismatch",
    )
    require(all(row["policy_status"] == "READY" for row in rows), "M0 v13 null/fallback policy rows must be ready")
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v13 null/fallback cannot claim a source rule")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v13 null/fallback cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v13 null/fallback cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v13 null/fallback cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 null/fallback cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v13 null/fallback must forbid residual leakage")
    require(len(summary) == 1, "M0 v13 null/fallback summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXPRESSION_NULL_FALLBACK_POLICY_V13", "M0 v13 null/fallback summary id mismatch")
    require(row["null_fallback_artifact"] == "m0_no_dark_expression_null_fallback_policy_v13", "M0 v13 null/fallback artifact id mismatch")
    require(row["admissibility_status"] == "READY", "M0 v13 null/fallback must inherit ready admissibility")
    require(row["policy_rows"] == "6", "M0 v13 null/fallback must summarize six rows")
    require(row["ready_policy_rows"] == "6", "M0 v13 null/fallback must ready six rows")
    require(row["blocked_policy_rows"] == "0", "M0 v13 null/fallback must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 null/fallback summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_EXPRESSION_NULL_FALLBACK_POLICY_READY", "M0 v13 null/fallback status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_expression_output_class_v13", "M0 v13 null/fallback next artifact mismatch")


def validate_m0_no_dark_expression_output_class_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_expression_output_class_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_expression_output_class_summary_v13.csv")
    require(len(rows) == 6, "M0 v13 output class must define six rows")
    require(
        {row["output_class_id"] for row in rows}
        == {
            "M0NDOC13_SOURCE_DOMAIN_OUTPUT_CLASS",
            "M0NDOC13_NO_DARK_CONSTRAINT_OUTPUT_CLASS",
            "M0NDOC13_MORPHOLOGY_FACTOR_OUTPUT_CLASS",
            "M0NDOC13_U_READ_MARKER_OUTPUT_CLASS",
            "M0NDOC13_BARYONIC_BINDING_OUTPUT_CLASS",
            "M0NDOC13_FAILURE_ROUTE_OUTPUT_CLASS",
        },
        "M0 v13 output class ids mismatch",
    )
    require(all(row["output_class_status"] == "READY" for row in rows), "M0 v13 output class rows must be ready")
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v13 output class cannot claim a source rule")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v13 output class cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v13 output class cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v13 output class cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 output class cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v13 output class must forbid residual leakage")
    require(len(summary) == 1, "M0 v13 output class summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXPRESSION_OUTPUT_CLASS_V13", "M0 v13 output class summary id mismatch")
    require(row["output_class_artifact"] == "m0_no_dark_expression_output_class_v13", "M0 v13 output class artifact id mismatch")
    require(row["null_fallback_status"] == "READY", "M0 v13 output class must inherit ready null/fallback")
    require(row["output_class_rows"] == "6", "M0 v13 output class must summarize six rows")
    require(row["ready_output_class_rows"] == "6", "M0 v13 output class must ready six rows")
    require(row["blocked_output_class_rows"] == "0", "M0 v13 output class must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 output class summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_EXPRESSION_OUTPUT_CLASS_READY", "M0 v13 output class status mismatch")
    require(
        row["next_required_artifact"] == "m0_no_dark_expression_source_rule_leakage_audit_v13",
        "M0 v13 output class next artifact mismatch",
    )


def validate_m0_no_dark_expression_source_rule_leakage_audit_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_expression_source_rule_leakage_audit_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_expression_source_rule_leakage_audit_summary_v13.csv")
    require(len(rows) == 6, "M0 v13 source-rule leakage audit must define six rows")
    require(
        {row["audit_id"] for row in rows}
        == {
            "M0NDSRLA13_SOURCE_DOMAIN_LEAKAGE_AUDIT",
            "M0NDSRLA13_NO_DARK_CONSTRAINT_LEAKAGE_AUDIT",
            "M0NDSRLA13_MORPHOLOGY_FACTOR_LEAKAGE_AUDIT",
            "M0NDSRLA13_U_READ_MARKER_LEAKAGE_AUDIT",
            "M0NDSRLA13_BARYONIC_BINDING_LEAKAGE_AUDIT",
            "M0NDSRLA13_FAILURE_ROUTE_LEAKAGE_AUDIT",
        },
        "M0 v13 source-rule leakage audit ids mismatch",
    )
    require(all(row["audit_status"] == "READY" for row in rows), "M0 v13 source-rule leakage audit rows must be ready")
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v13 leakage audit cannot claim a source rule")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v13 leakage audit cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v13 leakage audit cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v13 leakage audit cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 leakage audit cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v13 leakage audit must forbid residual leakage")
    require(len(summary) == 1, "M0 v13 source-rule leakage audit summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXPRESSION_SOURCE_RULE_LEAKAGE_AUDIT_V13", "M0 v13 leakage audit summary id mismatch")
    require(
        row["source_rule_leakage_audit_artifact"] == "m0_no_dark_expression_source_rule_leakage_audit_v13",
        "M0 v13 leakage audit artifact id mismatch",
    )
    require(row["output_class_status"] == "READY", "M0 v13 leakage audit must inherit ready output class")
    require(row["audit_rows"] == "6", "M0 v13 leakage audit must summarize six rows")
    require(row["ready_audit_rows"] == "6", "M0 v13 leakage audit must ready six rows")
    require(row["blocked_audit_rows"] == "0", "M0 v13 leakage audit must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 leakage audit summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_EXPRESSION_SOURCE_RULE_LEAKAGE_AUDIT_READY", "M0 v13 leakage audit status mismatch")
    require(
        row["next_required_artifact"] == "m0_no_dark_expression_symbolic_form_v12",
        "M0 v13 leakage audit next artifact mismatch",
    )


def validate_m0_no_dark_expression_source_rule_contract_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_expression_source_rule_contract_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_expression_source_rule_contract_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 expression source-rule contract must define six slots")
    require(
        {row["source_rule_slot_id"] for row in rows}
        == {
            "M0NDESR12_RULE_DERIVATION",
            "M0NDESR12_SOURCE_BASIS",
            "M0NDESR12_ADMISSIBILITY",
            "M0NDESR12_NULL_AND_FALLBACK",
            "M0NDESR12_OUTPUT_CLASS",
            "M0NDESR12_LEAKAGE_AUDIT",
        },
        "M0 v12 source-rule slot ids mismatch",
    )
    require(all(row["source_rule_claim_allowed"] == "false" for row in rows), "M0 v12 cannot allow source-rule claims")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v12 cannot allow expression claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v12 cannot allow numeric predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v12 must forbid residual leakage")
    require(rows[0]["completion_status"] == "READY", "M0 v12 derivation slot must be ready")
    require(rows[0]["next_required_artifact"] == "m0_no_dark_expression_source_basis_v13", "M0 v12 next derivation artifact mismatch")
    require(rows[1]["completion_status"] == "READY", "M0 v12 source-basis slot must be ready")
    require(rows[1]["next_required_artifact"] == "m0_no_dark_expression_source_basis_v13", "M0 v12 source-basis artifact mismatch")
    require(rows[2]["completion_status"] == "READY", "M0 v12 admissibility slot must be ready")
    require(rows[2]["next_required_artifact"] == "m0_no_dark_expression_admissibility_rule_v13", "M0 v12 admissibility artifact mismatch")
    require(rows[3]["completion_status"] == "READY", "M0 v12 null/fallback slot must be ready")
    require(rows[3]["next_required_artifact"] == "m0_no_dark_expression_null_fallback_policy_v13", "M0 v12 null/fallback artifact mismatch")
    require(rows[4]["completion_status"] == "READY", "M0 v12 output class slot must be ready")
    require(rows[4]["next_required_artifact"] == "m0_no_dark_expression_output_class_v13", "M0 v12 output class artifact mismatch")
    require(rows[5]["completion_status"] == "READY", "M0 v12 leakage-audit slot must be ready")
    require(
        rows[5]["next_required_artifact"] == "m0_no_dark_expression_source_rule_leakage_audit_v13",
        "M0 v12 leakage-audit artifact mismatch",
    )
    require(len(summary) == 1, "M0 v12 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXPRESSION_SOURCE_RULE_CONTRACT_V12", "M0 v12 summary id mismatch")
    require(row["source_rule_artifact"] == "m0_no_dark_expression_source_rule_v12", "M0 v12 artifact id mismatch")
    require(row["required_source_rule_slots"] == "6", "M0 v12 must require six source-rule slots")
    require(row["ready_source_rule_slots"] == "6", "M0 v12 must ready six source-rule slots")
    require(row["blocked_source_rule_slots"] == "0", "M0 v12 must block zero source-rule slots")
    require(row["source_rules_written"] == "0", "M0 v12 must write zero source rules")
    require(row["numeric_predictions_written"] == "0", "M0 v12 must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_EXPRESSION_SOURCE_RULE_READY_FOR_SYMBOLIC_FORM",
        "M0 v12 status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_expression_symbolic_form_v12", "M0 v12 next artifact mismatch")


def validate_m0_no_dark_expression_symbolic_form_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_expression_symbolic_form_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_expression_symbolic_form_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 symbolic form must define six shell components")
    require(
        {row["symbolic_component_id"] for row in rows}
        == {
            "M0NDSF12_SOURCE_STATE_PLACEHOLDER",
            "M0NDSF12_NO_DARK_CONSTRAINT_PLACEHOLDER",
            "M0NDSF12_BARYONIC_INPUT_PLACEHOLDER",
            "M0NDSF12_READOUT_OPERATOR_PLACEHOLDER",
            "M0NDSF12_FAILURE_ROUTE_PLACEHOLDER",
            "M0NDSF12_FORM_ASSEMBLY_SHELL",
        },
        "M0 v12 symbolic form component ids mismatch",
    )
    require(all(row["symbolic_component_status"] == "READY" for row in rows), "M0 v12 symbolic form rows must be ready")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v12 symbolic form cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v12 symbolic form cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v12 symbolic form cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 symbolic form cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v12 symbolic form must forbid residual leakage")
    require(len(summary) == 1, "M0 v12 symbolic form summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXPRESSION_SYMBOLIC_FORM_V12", "M0 v12 symbolic form summary id mismatch")
    require(row["symbolic_form_artifact"] == "m0_no_dark_expression_symbolic_form_v12", "M0 v12 symbolic form artifact id mismatch")
    require(row["source_rule_contract_status"] == "READY", "M0 v12 symbolic form must inherit ready source-rule contract")
    require(row["symbolic_components"] == "6", "M0 v12 symbolic form must summarize six components")
    require(row["ready_symbolic_components"] == "6", "M0 v12 symbolic form must ready six components")
    require(row["blocked_symbolic_components"] == "0", "M0 v12 symbolic form must block zero components")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 symbolic form summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_EXPRESSION_SYMBOLIC_FORM_READY", "M0 v12 symbolic form status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_expression_input_domain_v12", "M0 v12 symbolic form next artifact mismatch")


def validate_m0_no_dark_expression_input_domain_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_expression_input_domain_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_expression_input_domain_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 input domain must define six rows")
    require(
        {row["input_domain_id"] for row in rows}
        == {
            "M0NDID12_SOURCE_STATE_DOMAIN",
            "M0NDID12_NO_DARK_CONSTRAINT_DOMAIN",
            "M0NDID12_BARYONIC_INPUT_DOMAIN",
            "M0NDID12_READOUT_OPERATOR_DOMAIN",
            "M0NDID12_FAILURE_ROUTE_DOMAIN",
            "M0NDID12_FORM_ASSEMBLY_DOMAIN",
        },
        "M0 v12 input-domain ids mismatch",
    )
    require(all(row["input_domain_status"] == "READY" for row in rows), "M0 v12 input-domain rows must be ready")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v12 input domain cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v12 input domain cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v12 input domain cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 input domain cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v12 input domain must forbid residual leakage")
    require(len(summary) == 1, "M0 v12 input-domain summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXPRESSION_INPUT_DOMAIN_V12", "M0 v12 input-domain summary id mismatch")
    require(row["input_domain_artifact"] == "m0_no_dark_expression_input_domain_v12", "M0 v12 input-domain artifact id mismatch")
    require(row["symbolic_form_status"] == "READY", "M0 v12 input domain must inherit ready symbolic form")
    require(row["input_domain_rows"] == "6", "M0 v12 input domain must summarize six rows")
    require(row["ready_input_domain_rows"] == "6", "M0 v12 input domain must ready six rows")
    require(row["blocked_input_domain_rows"] == "0", "M0 v12 input domain must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 input domain summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_EXPRESSION_INPUT_DOMAIN_READY", "M0 v12 input-domain status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_expression_coefficient_freeze_v12", "M0 v12 input-domain next artifact mismatch")


def validate_m0_no_dark_expression_coefficient_freeze_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_expression_coefficient_freeze_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_expression_coefficient_freeze_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 coefficient freeze must define six policy rows")
    require(
        {row["coefficient_policy_id"] for row in rows}
        == {
            "M0NDCF12_SOURCE_STATE_COEFFICIENT_POLICY",
            "M0NDCF12_NO_DARK_CONSTRAINT_COEFFICIENT_POLICY",
            "M0NDCF12_BARYONIC_INPUT_COEFFICIENT_POLICY",
            "M0NDCF12_READOUT_OPERATOR_COEFFICIENT_POLICY",
            "M0NDCF12_FAILURE_ROUTE_COEFFICIENT_POLICY",
            "M0NDCF12_ASSEMBLY_COEFFICIENT_POLICY",
        },
        "M0 v12 coefficient-freeze ids mismatch",
    )
    require(all(row["coefficient_policy_status"] == "READY" for row in rows), "M0 v12 coefficient-freeze rows must be ready")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v12 coefficient freeze cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v12 coefficient freeze cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v12 coefficient freeze cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 coefficient freeze cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v12 coefficient freeze must forbid residual leakage")
    require(len(summary) == 1, "M0 v12 coefficient-freeze summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXPRESSION_COEFFICIENT_FREEZE_V12", "M0 v12 coefficient-freeze summary id mismatch")
    require(
        row["coefficient_freeze_artifact"] == "m0_no_dark_expression_coefficient_freeze_v12",
        "M0 v12 coefficient-freeze artifact id mismatch",
    )
    require(row["input_domain_status"] == "READY", "M0 v12 coefficient freeze must inherit ready input domain")
    require(row["coefficient_policy_rows"] == "6", "M0 v12 coefficient freeze must summarize six rows")
    require(row["ready_coefficient_policy_rows"] == "6", "M0 v12 coefficient freeze must ready six rows")
    require(row["blocked_coefficient_policy_rows"] == "0", "M0 v12 coefficient freeze must block zero rows")
    require(row["numeric_coefficient_values_written"] == "0", "M0 v12 coefficient freeze cannot write coefficient values")
    require(row["numeric_parameter_counts_written"] == "0", "M0 v12 coefficient freeze cannot write final parameter counts")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 coefficient freeze summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_EXPRESSION_COEFFICIENT_FREEZE_READY", "M0 v12 coefficient-freeze status mismatch")
    require(
        row["next_required_artifact"] == "m0_no_dark_expression_dimensional_audit_v12",
        "M0 v12 coefficient-freeze next artifact mismatch",
    )


def validate_m0_no_dark_expression_dimensional_audit_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_expression_dimensional_audit_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_expression_dimensional_audit_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 dimensional audit must define six rows")
    require(
        {row["dimensional_audit_id"] for row in rows}
        == {
            "M0NDDA12_SOURCE_STATE_UNIT_AUDIT",
            "M0NDDA12_NO_DARK_CONSTRAINT_UNIT_AUDIT",
            "M0NDDA12_BARYONIC_INPUT_UNIT_AUDIT",
            "M0NDDA12_READOUT_OPERATOR_UNIT_AUDIT",
            "M0NDDA12_FAILURE_ROUTE_UNIT_AUDIT",
            "M0NDDA12_ASSEMBLY_UNIT_AUDIT",
        },
        "M0 v12 dimensional-audit ids mismatch",
    )
    require(all(row["dimensional_audit_status"] == "READY" for row in rows), "M0 v12 dimensional-audit rows must be ready")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v12 dimensional audit cannot claim an expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v12 dimensional audit cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v12 dimensional audit cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 dimensional audit cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v12 dimensional audit must forbid residual leakage")
    require(len(summary) == 1, "M0 v12 dimensional-audit summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXPRESSION_DIMENSIONAL_AUDIT_V12", "M0 v12 dimensional-audit summary id mismatch")
    require(
        row["dimensional_audit_artifact"] == "m0_no_dark_expression_dimensional_audit_v12",
        "M0 v12 dimensional-audit artifact id mismatch",
    )
    require(row["coefficient_freeze_status"] == "READY", "M0 v12 dimensional audit must inherit ready coefficient freeze")
    require(row["dimensional_audit_rows"] == "6", "M0 v12 dimensional audit must summarize six rows")
    require(row["ready_dimensional_audit_rows"] == "6", "M0 v12 dimensional audit must ready six rows")
    require(row["blocked_dimensional_audit_rows"] == "0", "M0 v12 dimensional audit must block zero rows")
    require(row["velocity_formula_written"] == "false", "M0 v12 dimensional audit cannot write a velocity formula")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 dimensional audit summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_EXPRESSION_DIMENSIONAL_AUDIT_READY", "M0 v12 dimensional-audit status mismatch")
    require(
        row["next_required_artifact"] == "m0_no_dark_expression_machine_form_v12",
        "M0 v12 dimensional-audit next artifact mismatch",
    )


def validate_m0_no_dark_expression_machine_form_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_expression_machine_form_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_expression_machine_form_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 machine form must define six rows")
    require(
        {row["machine_form_id"] for row in rows}
        == {
            "M0NDMF12_SOURCE_STATE_SERIALIZATION",
            "M0NDMF12_NO_DARK_CONSTRAINT_SERIALIZATION",
            "M0NDMF12_BARYONIC_INPUT_SERIALIZATION",
            "M0NDMF12_READOUT_OPERATOR_SERIALIZATION",
            "M0NDMF12_FAILURE_ROUTE_SERIALIZATION",
            "M0NDMF12_ASSEMBLY_SERIALIZATION",
        },
        "M0 v12 machine-form ids mismatch",
    )
    require(all(row["machine_form_status"] == "READY" for row in rows), "M0 v12 machine-form rows must be ready")
    require(all(row["frozen_expression_claim_allowed"] == "false" for row in rows), "M0 v12 machine form cannot claim a frozen expression")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v12 machine form cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v12 machine form cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 machine form cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v12 machine form must forbid residual leakage")
    require(len(summary) == 1, "M0 v12 machine-form summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXPRESSION_MACHINE_FORM_V12", "M0 v12 machine-form summary id mismatch")
    require(row["machine_form_artifact"] == "m0_no_dark_expression_machine_form_v12", "M0 v12 machine-form artifact id mismatch")
    require(row["dimensional_audit_status"] == "READY", "M0 v12 machine form must inherit ready dimensional audit")
    require(row["machine_form_rows"] == "6", "M0 v12 machine form must summarize six rows")
    require(row["ready_machine_form_rows"] == "6", "M0 v12 machine form must ready six rows")
    require(row["blocked_machine_form_rows"] == "0", "M0 v12 machine form must block zero rows")
    require(row["serialized_prediction_callable_written"] == "false", "M0 v12 machine form cannot write a prediction callable")
    require(row["formula_claim_allowed"] == "false", "M0 v12 machine-form summary cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v12 machine-form summary cannot write predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 machine-form summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_EXPRESSION_MACHINE_FORM_READY", "M0 v12 machine-form status mismatch")
    require(row["next_required_artifact"] == "family_prediction_tables_v08.csv", "M0 v12 machine-form next artifact mismatch")


def validate_m0_no_dark_frozen_expression_contract_v11() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_frozen_expression_contract_v11.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_frozen_expression_contract_summary_v11.csv")
    require(len(rows) == 6, "M0 v11 frozen expression contract must define six slots")
    require(
        {row["freeze_slot_id"] for row in rows}
        == {
            "M0NDFE11_SOURCE_RULE",
            "M0NDFE11_SYMBOLIC_FORM",
            "M0NDFE11_INPUT_DOMAIN",
            "M0NDFE11_COEFFICIENT_FREEZE",
            "M0NDFE11_DIMENSIONAL_AUDIT",
            "M0NDFE11_MACHINE_FORM",
        },
        "M0 v11 frozen expression slot ids mismatch",
    )
    require(all(row["frozen_expression_claim_allowed"] == "false" for row in rows), "M0 v11 cannot allow frozen expression claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v11 cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v11 cannot allow numeric predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v11 cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v11 must forbid residual leakage")
    require(rows[0]["completion_status"] == "READY", "M0 v11 source-rule slot must be ready")
    require(rows[0]["next_required_artifact"] == "m0_no_dark_expression_symbolic_form_v12", "M0 v11 next source-rule artifact mismatch")
    require(rows[1]["completion_status"] == "READY", "M0 v11 symbolic-form slot must be ready")
    require(rows[1]["next_required_artifact"] == "m0_no_dark_expression_symbolic_form_v12", "M0 v11 symbolic-form artifact mismatch")
    require(rows[2]["completion_status"] == "READY", "M0 v11 input-domain slot must be ready")
    require(rows[2]["next_required_artifact"] == "m0_no_dark_expression_input_domain_v12", "M0 v11 input-domain artifact mismatch")
    require(rows[3]["completion_status"] == "READY", "M0 v11 coefficient-freeze slot must be ready")
    require(rows[3]["next_required_artifact"] == "m0_no_dark_expression_coefficient_freeze_v12", "M0 v11 coefficient-freeze artifact mismatch")
    require(rows[4]["completion_status"] == "READY", "M0 v11 dimensional-audit slot must be ready")
    require(rows[4]["next_required_artifact"] == "m0_no_dark_expression_dimensional_audit_v12", "M0 v11 dimensional-audit artifact mismatch")
    require(rows[5]["completion_status"] == "READY", "M0 v11 machine-form slot must be ready")
    require(rows[5]["next_required_artifact"] == "m0_no_dark_expression_machine_form_v12", "M0 v11 machine-form artifact mismatch")
    require(len(summary) == 1, "M0 v11 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_FROZEN_EXPRESSION_CONTRACT_V11", "M0 v11 summary id mismatch")
    require(row["frozen_expression_artifact"] == "m0_no_dark_frozen_expression_v11", "M0 v11 artifact id mismatch")
    require(row["required_freeze_slots"] == "6", "M0 v11 must require six freeze slots")
    require(row["ready_freeze_slots"] == "6", "M0 v11 must ready six freeze slots")
    require(row["blocked_freeze_slots"] == "0", "M0 v11 must block zero freeze slots")
    require(row["frozen_expressions_written"] == "0", "M0 v11 must write zero frozen expressions")
    require(row["numeric_predictions_written"] == "0", "M0 v11 must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v11 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_FROZEN_EXPRESSION_READY_FOR_PREDICTION_WRITER",
        "M0 v11 status mismatch",
    )
    require(row["next_required_artifact"] == "family_prediction_tables_v08.csv", "M0 v11 next artifact mismatch")


def validate_m0_no_dark_kernel_expression_contract_v10() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_kernel_expression_contract_v10.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_kernel_expression_contract_summary_v10.csv")
    require(len(rows) == 5, "M0 v10 kernel expression contract must define five slots")
    require(
        {row["expression_slot_id"] for row in rows}
        == {
            "M0NDKE10_FROZEN_EXPRESSION",
            "M0NDKE10_VARIABLE_BINDINGS",
            "M0NDKE10_CONSTANTS",
            "M0NDKE10_DIMENSIONAL_PATH",
            "M0NDKE10_SERIALIZED_FORM",
        },
        "M0 v10 expression slot ids mismatch",
    )
    require(rows[0]["expression_claim_allowed"] == "true", "M0 v10 must allow the frozen expression-body claim")
    require(
        all(row["expression_claim_allowed"] == "false" for row in rows[1:]),
        "M0 v10 non-body slots cannot allow expression claims",
    )
    require(all(row["kernel_claim_allowed"] == "false" for row in rows), "M0 v10 cannot allow kernel claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v10 cannot allow numeric predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v10 cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v10 must forbid residual leakage")
    require(
        rows[0]["next_required_artifact"] == "m0_no_dark_frozen_expression_body_v14",
        "M0 v10 next frozen expression artifact mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v10 expression slots must be ready")
    require(len(summary) == 1, "M0 v10 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_KERNEL_EXPRESSION_CONTRACT_V10", "M0 v10 summary id mismatch")
    require(row["kernel_expression_artifact"] == "m0_no_dark_kernel_expression_v10", "M0 v10 artifact id mismatch")
    require(row["required_expression_slots"] == "5", "M0 v10 must require five expression slots")
    require(row["ready_expression_slots"] == "5", "M0 v10 must ready five expression slots")
    require(row["blocked_expression_slots"] == "0", "M0 v10 must block zero expression slots")
    require(row["frozen_expressions_written"] == "1", "M0 v10 must register one frozen expression body")
    require(row["numeric_predictions_written"] == "0", "M0 v10 must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v10 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_KERNEL_EXPRESSION_READY_FOR_KERNEL_FREEZE",
        "M0 v10 status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_equation_kernel_v09", "M0 v10 next artifact mismatch")


def validate_m0_no_dark_kernel_expression_interface_v10() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_kernel_expression_interface_v10.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_kernel_expression_interface_summary_v10.csv")
    require(len(rows) == 4, "M0 v10 kernel-expression interface must define four rows")
    require(
        {row["expression_slot_id"] for row in rows}
        == {
            "M0NDKE10_VARIABLE_BINDINGS",
            "M0NDKE10_CONSTANTS",
            "M0NDKE10_DIMENSIONAL_PATH",
            "M0NDKE10_SERIALIZED_FORM",
        },
        "M0 v10 kernel-expression interface slot ids mismatch",
    )
    require(all(row["interface_status"] == "READY" for row in rows), "M0 v10 kernel-expression interface rows must be ready")
    require(all(row["expression_claim_allowed"] == "false" for row in rows), "M0 v10 kernel-expression interface cannot allow expression claims")
    require(all(row["kernel_claim_allowed"] == "false" for row in rows), "M0 v10 kernel-expression interface cannot allow kernel claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v10 kernel-expression interface cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v10 kernel-expression interface cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v10 kernel-expression interface must forbid residual leakage")
    require(len(summary) == 1, "M0 v10 kernel-expression interface summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_KERNEL_EXPRESSION_INTERFACE_V10", "M0 v10 kernel-expression interface summary id mismatch")
    require(row["interface_artifact"] == "m0_no_dark_kernel_expression_interface_v10", "M0 v10 kernel-expression interface artifact mismatch")
    require(row["equation_kernel_interface_status"] == "READY", "M0 v10 kernel-expression interface must inherit ready equation-kernel interface")
    require(row["frozen_expression_contract_status"] == "READY_CONTRACT_ONLY_NO_PAYLOAD", "M0 v10 kernel-expression interface must distinguish contract from payload")
    require(row["interface_rows"] == "4", "M0 v10 kernel-expression interface must summarize four rows")
    require(row["ready_interface_rows"] == "4", "M0 v10 kernel-expression interface must ready four rows")
    require(row["blocked_interface_rows"] == "0", "M0 v10 kernel-expression interface must block zero interface rows")
    require(row["frozen_expression_payload_written"] == "false", "M0 v10 kernel-expression interface cannot write payload")
    require(row["expression_claim_allowed"] == "false", "M0 v10 kernel-expression interface cannot allow expression claims")
    require(row["numeric_predictions_written"] == "0", "M0 v10 kernel-expression interface must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v10 kernel-expression interface summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_KERNEL_EXPRESSION_INTERFACE_READY",
        "M0 v10 kernel-expression interface status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_frozen_expression_payload_v11", "M0 v10 kernel-expression interface next artifact mismatch")


def validate_m0_no_dark_frozen_expression_payload_contract_v11() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_frozen_expression_payload_v11.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_frozen_expression_payload_summary_v11.csv")
    require(len(rows) == 6, "M0 v11 frozen-expression payload contract must define six slots")
    require(
        {row["payload_slot_id"] for row in rows}
        == {
            "M0NDFEP11_EXPRESSION_STATEMENT",
            "M0NDFEP11_SYMBOL_BINDING_TABLE",
            "M0NDFEP11_CONSTANT_POLICY",
            "M0NDFEP11_DIMENSIONAL_TRACE",
            "M0NDFEP11_MACHINE_PAYLOAD",
            "M0NDFEP11_LEAKAGE_CERTIFICATE",
        },
        "M0 v11 frozen-expression payload slot ids mismatch",
    )
    require(all(row["payload_claim_allowed"] == "false" for row in rows), "M0 v11 payload cannot allow payload claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v11 payload cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v11 payload cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v11 payload cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v11 payload must forbid residual leakage")
    require(
        rows[0]["next_required_artifact"] == "m0_no_dark_frozen_expression_payload_v11",
        "M0 v11 payload next expression statement artifact mismatch",
    )
    require(rows[0]["completion_status"] == "READY", "M0 v11 payload must accept ready frozen expression statement")
    require(rows[1]["completion_status"] == "READY", "M0 v11 payload must accept ready symbol-binding table")
    require(
        rows[1]["next_required_artifact"] == "m0_no_dark_payload_symbol_binding_table_v12",
        "M0 v11 payload next symbol-binding artifact mismatch",
    )
    require(
        rows[2]["next_required_artifact"] == "m0_no_dark_payload_constant_policy_v12",
        "M0 v11 payload next constant-policy artifact mismatch",
    )
    require(rows[2]["completion_status"] == "READY", "M0 v11 payload must accept ready constant policy")
    require(
        rows[3]["next_required_artifact"] == "m0_no_dark_payload_dimensional_trace_v12",
        "M0 v11 payload next dimensional-trace artifact mismatch",
    )
    require(rows[3]["completion_status"] == "READY", "M0 v11 payload must accept ready dimensional trace")
    require(
        rows[4]["next_required_artifact"] == "m0_no_dark_payload_machine_form_v12",
        "M0 v11 payload next machine payload artifact mismatch",
    )
    require(rows[4]["completion_status"] == "READY", "M0 v11 payload must accept ready machine payload")
    require(
        rows[5]["next_required_artifact"] == "m0_no_dark_payload_leakage_certificate_v12",
        "M0 v11 payload next leakage certificate artifact mismatch",
    )
    require(rows[5]["completion_status"] == "READY", "M0 v11 payload must accept ready payload leakage certificate")
    require(len(summary) == 1, "M0 v11 payload summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_V11", "M0 v11 payload summary id mismatch")
    require(row["payload_artifact"] == "m0_no_dark_frozen_expression_payload_v11", "M0 v11 payload artifact mismatch")
    require(row["kernel_expression_interface_status"] == "READY", "M0 v11 payload must inherit ready kernel-expression interface")
    require(row["required_payload_slots"] == "6", "M0 v11 payload must require six slots")
    require(row["ready_payload_slots"] == "6", "M0 v11 payload must ready all six payload slots")
    require(row["blocked_payload_slots"] == "0", "M0 v11 payload must block zero payload slots")
    require(row["frozen_expression_payload_written"] == "true", "M0 v11 payload must record ready statement handoff")
    require(row["formula_claim_allowed"] == "false", "M0 v11 payload cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v11 payload must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v11 payload summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_FROZEN_EXPRESSION_PAYLOAD_CONTRACT_READY_FOR_KERNEL_EXPRESSION",
        "M0 v11 payload status mismatch",
    )
    require(row["next_required_artifact"] == "family_prediction_tables_v08.csv", "M0 v11 payload next artifact mismatch")


def validate_m0_no_dark_payload_symbol_binding_table_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_payload_symbol_binding_table_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_payload_symbol_binding_table_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 payload symbol-binding table must define six bindings")
    require(
        {row["binding_id"] for row in rows}
        == {
            "M0NDPSBT12_SOURCE_STATE_SYMBOL",
            "M0NDPSBT12_BARYONIC_INPUT_SYMBOL",
            "M0NDPSBT12_RADIUS_GRID_SYMBOL",
            "M0NDPSBT12_READOUT_OPERATOR_SYMBOL",
            "M0NDPSBT12_GUARD_SYMBOL",
            "M0NDPSBT12_ASSEMBLY_SYMBOL",
        },
        "M0 v12 payload symbol-binding ids mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v12 payload symbol bindings must be ready")
    require(
        all(row["next_required_artifact"] == "m0_no_dark_payload_constant_policy_v12" for row in rows),
        "M0 v12 payload symbol bindings must hand off to constant policy",
    )
    require(all(row["binding_claim_allowed"] == "false" for row in rows), "M0 v12 binding table cannot allow binding claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v12 binding table cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v12 binding table cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 binding table cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v12 binding table must forbid residual leakage")
    require(len(summary) == 1, "M0 v12 binding summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_PAYLOAD_SYMBOL_BINDING_TABLE_V12", "M0 v12 binding summary id mismatch")
    require(row["symbol_binding_artifact"] == "m0_no_dark_payload_symbol_binding_table_v12", "M0 v12 binding artifact mismatch")
    require(row["payload_contract_status"] == "READY", "M0 v12 binding must inherit ready payload contract")
    require(row["binding_rows"] == "6", "M0 v12 binding must summarize six rows")
    require(row["ready_binding_rows"] == "6", "M0 v12 binding must ready six rows")
    require(row["blocked_binding_rows"] == "0", "M0 v12 binding must block zero rows")
    require(row["symbol_binding_table_written"] == "true", "M0 v12 binding table must be written")
    require(row["formula_body_written"] == "false", "M0 v12 binding cannot write formula body")
    require(row["formula_claim_allowed"] == "false", "M0 v12 binding cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v12 binding must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 binding summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_PAYLOAD_SYMBOL_BINDING_TABLE_READY_FOR_CONSTANT_POLICY",
        "M0 v12 binding status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_payload_constant_policy_v12", "M0 v12 binding next artifact mismatch")


def validate_m0_no_dark_payload_constant_policy_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_payload_constant_policy_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_payload_constant_policy_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 payload constant policy must define six policy rows")
    require(
        {row["policy_id"] for row in rows}
        == {
            "M0NDPCP12_FIXED_SOURCE_CONSTANTS",
            "M0NDPCP12_FREE_PARAMETER_DECLARATION",
            "M0NDPCP12_SCALE_POLICY",
            "M0NDPCP12_BRANCH_SWITCH_POLICY",
            "M0NDPCP12_NULL_FALLBACK_CONSTANT_POLICY",
            "M0NDPCP12_HANDOFF_TO_DIMENSIONAL_TRACE",
        },
        "M0 v12 payload constant-policy ids mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v12 payload constant policies must be ready")
    require(
        all(row["next_required_artifact"] == "m0_no_dark_payload_dimensional_trace_v12" for row in rows),
        "M0 v12 payload constant policy must hand off to dimensional trace",
    )
    require(all(row["policy_claim_allowed"] == "false" for row in rows), "M0 v12 constant policy cannot allow policy claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v12 constant policy cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v12 constant policy cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 constant policy cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v12 constant policy must forbid residual leakage")
    require(len(summary) == 1, "M0 v12 constant policy summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_PAYLOAD_CONSTANT_POLICY_V12", "M0 v12 constant policy summary id mismatch")
    require(row["constant_policy_artifact"] == "m0_no_dark_payload_constant_policy_v12", "M0 v12 constant policy artifact mismatch")
    require(row["symbol_binding_status"] == "READY", "M0 v12 constant policy must inherit ready symbol binding")
    require(row["policy_rows"] == "6", "M0 v12 constant policy must summarize six rows")
    require(row["ready_policy_rows"] == "6", "M0 v12 constant policy must ready six rows")
    require(row["blocked_policy_rows"] == "0", "M0 v12 constant policy must block zero rows")
    require(row["constant_policy_written"] == "true", "M0 v12 constant policy must be written")
    require(row["formula_body_written"] == "false", "M0 v12 constant policy cannot write formula body")
    require(row["formula_claim_allowed"] == "false", "M0 v12 constant policy cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v12 constant policy must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 constant policy summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_PAYLOAD_CONSTANT_POLICY_READY_FOR_DIMENSIONAL_TRACE",
        "M0 v12 constant policy status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_payload_dimensional_trace_v12", "M0 v12 constant policy next artifact mismatch")


def validate_m0_no_dark_payload_dimensional_trace_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_payload_dimensional_trace_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 payload dimensional trace must define six trace rows")
    require(
        {row["trace_id"] for row in rows}
        == {
            "M0NDPDT12_INPUT_DIMENSION_CLASSES",
            "M0NDPDT12_OPERATOR_DIMENSION_EFFECTS",
            "M0NDPDT12_CONSTANT_UNIT_COMPATIBILITY",
            "M0NDPDT12_OUTPUT_UNIT_TARGET",
            "M0NDPDT12_NULL_FALLBACK_DIMENSION_POLICY",
            "M0NDPDT12_HANDOFF_TO_MACHINE_PAYLOAD",
        },
        "M0 v12 payload dimensional-trace ids mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v12 payload dimensional traces must be ready")
    require(
        all(row["next_required_artifact"] == "m0_no_dark_payload_machine_form_v12" for row in rows),
        "M0 v12 payload dimensional trace must hand off to machine payload",
    )
    require(all(row["trace_claim_allowed"] == "false" for row in rows), "M0 v12 dimensional trace cannot allow trace claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v12 dimensional trace cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v12 dimensional trace cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 dimensional trace cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v12 dimensional trace must forbid residual leakage")
    require(len(summary) == 1, "M0 v12 dimensional trace summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_PAYLOAD_DIMENSIONAL_TRACE_V12", "M0 v12 dimensional trace summary id mismatch")
    require(row["dimensional_trace_artifact"] == "m0_no_dark_payload_dimensional_trace_v12", "M0 v12 dimensional trace artifact mismatch")
    require(row["constant_policy_status"] == "READY", "M0 v12 dimensional trace must inherit ready constant policy")
    require(row["trace_rows"] == "6", "M0 v12 dimensional trace must summarize six rows")
    require(row["ready_trace_rows"] == "6", "M0 v12 dimensional trace must ready six rows")
    require(row["blocked_trace_rows"] == "0", "M0 v12 dimensional trace must block zero rows")
    require(row["dimensional_trace_written"] == "true", "M0 v12 dimensional trace must be written")
    require(row["formula_body_written"] == "false", "M0 v12 dimensional trace cannot write formula body")
    require(row["formula_claim_allowed"] == "false", "M0 v12 dimensional trace cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v12 dimensional trace must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 dimensional trace summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_PAYLOAD_DIMENSIONAL_TRACE_READY_FOR_MACHINE_PAYLOAD",
        "M0 v12 dimensional trace status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_payload_machine_form_v12", "M0 v12 dimensional trace next artifact mismatch")


def validate_m0_no_dark_payload_machine_form_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_payload_machine_form_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_payload_machine_form_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 payload machine form must define six payload rows")
    require(
        {row["machine_payload_id"] for row in rows}
        == {
            "M0NDPMF12_SOURCE_STATE_PAYLOAD",
            "M0NDPMF12_BARYONIC_RADIAL_PAYLOAD",
            "M0NDPMF12_OPERATOR_GUARD_PAYLOAD",
            "M0NDPMF12_CONSTANT_POLICY_PAYLOAD",
            "M0NDPMF12_DIMENSION_TRACE_PAYLOAD",
            "M0NDPMF12_HANDOFF_TO_LEAKAGE_CERTIFICATE",
        },
        "M0 v12 payload machine-form ids mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v12 payload machine-form rows must be ready")
    require(
        all(row["next_required_artifact"] == "m0_no_dark_payload_leakage_certificate_v12" for row in rows),
        "M0 v12 payload machine form must hand off to leakage certificate",
    )
    require(all(row["machine_payload_claim_allowed"] == "false" for row in rows), "M0 v12 machine form cannot allow payload claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v12 machine form cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v12 machine form cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 machine form cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v12 machine form must forbid residual leakage")
    require(len(summary) == 1, "M0 v12 machine form summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_PAYLOAD_MACHINE_FORM_V12", "M0 v12 machine form summary id mismatch")
    require(row["machine_payload_artifact"] == "m0_no_dark_payload_machine_form_v12", "M0 v12 machine form artifact mismatch")
    require(row["dimensional_trace_status"] == "READY", "M0 v12 machine form must inherit ready dimensional trace")
    require(row["machine_payload_rows"] == "6", "M0 v12 machine form must summarize six rows")
    require(row["ready_machine_payload_rows"] == "6", "M0 v12 machine form must ready six rows")
    require(row["blocked_machine_payload_rows"] == "0", "M0 v12 machine form must block zero rows")
    require(row["machine_payload_written"] == "true", "M0 v12 machine form must be written")
    require(row["prediction_callable_written"] == "false", "M0 v12 machine form cannot write a prediction callable")
    require(row["formula_claim_allowed"] == "false", "M0 v12 machine form cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v12 machine form must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 machine form summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_PAYLOAD_MACHINE_FORM_READY_FOR_LEAKAGE_CERTIFICATE",
        "M0 v12 machine form status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_payload_leakage_certificate_v12", "M0 v12 machine form next artifact mismatch")


def validate_m0_no_dark_payload_leakage_certificate_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_payload_leakage_certificate_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_payload_leakage_certificate_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 payload leakage certificate must define six certificate rows")
    require(
        {row["certificate_id"] for row in rows}
        == {
            "M0NDPLC12_FORBIDDEN_INPUT_MANIFEST",
            "M0NDPLC12_FREEZE_ORDER_CERTIFICATE",
            "M0NDPLC12_SERIALIZATION_HASH_POLICY",
            "M0NDPLC12_SOURCE_PROVENANCE_GUARDS",
            "M0NDPLC12_NULL_FALLBACK_STOP_CERTIFICATE",
            "M0NDPLC12_HANDOFF_TO_FORMULA_TABLES",
        },
        "M0 v12 payload leakage-certificate ids mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v12 payload leakage certificate rows must be ready")
    require(
        all(row["next_required_artifact"] == "family_prediction_tables_v08.csv" for row in rows),
        "M0 v12 payload leakage certificate must hand off to family prediction tables",
    )
    require(all(row["certificate_claim_allowed"] == "false" for row in rows), "M0 v12 leakage certificate cannot allow certificate claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v12 leakage certificate cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v12 leakage certificate cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 leakage certificate cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v12 leakage certificate must forbid residual leakage")
    require(len(summary) == 1, "M0 v12 leakage certificate summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_PAYLOAD_LEAKAGE_CERTIFICATE_V12", "M0 v12 leakage certificate summary id mismatch")
    require(row["payload_leakage_certificate_artifact"] == "m0_no_dark_payload_leakage_certificate_v12", "M0 v12 leakage certificate artifact mismatch")
    require(row["machine_payload_status"] == "READY", "M0 v12 leakage certificate must inherit ready machine payload")
    require(row["certificate_rows"] == "6", "M0 v12 leakage certificate must summarize six rows")
    require(row["ready_certificate_rows"] == "6", "M0 v12 leakage certificate must ready six rows")
    require(row["blocked_certificate_rows"] == "0", "M0 v12 leakage certificate must block zero rows")
    require(row["payload_leakage_certificate_written"] == "true", "M0 v12 leakage certificate must be written")
    require(row["prediction_callable_written"] == "false", "M0 v12 leakage certificate cannot write a prediction callable")
    require(row["formula_claim_allowed"] == "false", "M0 v12 leakage certificate cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v12 leakage certificate must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 leakage certificate summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_PAYLOAD_LEAKAGE_CERTIFICATE_READY_FOR_FORMULA_TABLES",
        "M0 v12 leakage certificate status mismatch",
    )
    require(row["next_required_artifact"] == "family_prediction_tables_v08.csv", "M0 v12 leakage certificate next artifact mismatch")


def validate_m0_no_dark_frozen_expression_body_v14() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_frozen_expression_body_v14.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_frozen_expression_body_summary_v14.csv")
    require(len(rows) == 6, "M0 v14 frozen expression body must define six rows")
    require(
        {row["body_component"] for row in rows}
        == {
            "scope_and_family_binding",
            "argument_vector",
            "assembly_body",
            "no_dark_exclusion",
            "output_class",
            "freeze_guard",
        },
        "M0 v14 body components mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v14 body rows must be ready")
    require(
        all(row["expression_body_claim_allowed"] == "true" for row in rows),
        "M0 v14 must allow expression-body claim only",
    )
    require(
        all(row["velocity_formula_claim_allowed"] == "false" for row in rows),
        "M0 v14 must not allow velocity formula claim",
    )
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v14 cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v14 cannot allow scoring")
    require(
        all(row["dark_sector_verdict_allowed"] == "false" for row in rows),
        "M0 v14 cannot decide dark-sector verdict",
    )
    require(rows[2]["body_component"] == "assembly_body", "M0 v14 assembly row order mismatch")
    require("Assemble_M0" in rows[2]["frozen_expression_body_statement"], "M0 v14 assembly body missing")
    require(len(summary) == 1, "M0 v14 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_FROZEN_EXPRESSION_BODY_V14", "M0 v14 summary id mismatch")
    require(row["body_artifact"] == "m0_no_dark_frozen_expression_body_v14", "M0 v14 artifact id mismatch")
    require(row["payload_status"] == "READY", "M0 v14 payload status mismatch")
    require(row["body_rows"] == "6", "M0 v14 body row count mismatch")
    require(row["ready_body_rows"] == "6", "M0 v14 ready row count mismatch")
    require(row["blocked_body_rows"] == "0", "M0 v14 blocked row count mismatch")
    require(row["expression_body_written"] == "true", "M0 v14 expression body must be written")
    require(row["velocity_formula_written"] == "false", "M0 v14 must not write velocity formula")
    require(row["numeric_predictions_written"] == "0", "M0 v14 must write zero numeric predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v14 summary cannot allow scoring")
    require(row["dark_sector_verdict_allowed"] == "false", "M0 v14 summary cannot decide dark-sector verdict")
    require(
        row["overall_status"] == "M0_NO_DARK_FROZEN_EXPRESSION_BODY_READY_FOR_KERNEL_EXPRESSION_REVIEW",
        "M0 v14 status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_kernel_expression_contract_v10",
        "M0 v14 next artifact mismatch",
    )


def validate_m0_no_dark_frozen_expression_statement_contract_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_frozen_expression_statement_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_frozen_expression_statement_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 frozen-expression statement contract must define six slots")
    require(
        {row["statement_slot_id"] for row in rows}
        == {
            "M0NDFES12_SOURCE_SIDE_STATEMENT",
            "M0NDFES12_TERM_LIST",
            "M0NDFES12_ARGUMENT_SIGNATURE",
            "M0NDFES12_CONSTRAINT_GUARDS",
            "M0NDFES12_PRE_DIMENSIONAL_PROOF",
            "M0NDFES12_FREEZE_PROVENANCE",
        },
        "M0 v12 frozen-expression statement slot ids mismatch",
    )
    require(all(row["statement_claim_allowed"] == "false" for row in rows), "M0 v12 statement cannot allow statement claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v12 statement cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v12 statement cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 statement cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v12 statement must forbid residual leakage")
    require(
        rows[0]["next_required_artifact"] == "m0_no_dark_source_side_expression_statement_v13",
        "M0 v12 statement next source-side statement artifact mismatch",
    )
    require(rows[0]["completion_status"] == "READY", "M0 v12 statement must accept v13 source-side statement envelope")
    require(len(summary) == 1, "M0 v12 statement summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_V12", "M0 v12 statement summary id mismatch")
    require(row["statement_artifact"] == "m0_no_dark_frozen_expression_statement_v12", "M0 v12 statement artifact mismatch")
    require(row["kernel_expression_interface_status"] == "READY", "M0 v12 statement must inherit ready kernel-expression interface")
    require(row["required_statement_slots"] == "6", "M0 v12 statement must require six slots")
    require(row["ready_statement_slots"] == "6", "M0 v12 statement must ready all statement slots")
    require(row["blocked_statement_slots"] == "0", "M0 v12 statement must block zero statement slots")
    require(row["source_side_expression_statement_written"] == "true", "M0 v12 statement must record the source-side statement envelope")
    require(row["formula_claim_allowed"] == "false", "M0 v12 statement cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v12 statement must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 statement summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FOR_PAYLOAD",
        "M0 v12 statement status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_frozen_expression_payload_v11", "M0 v12 statement next artifact mismatch")


def validate_m0_no_dark_source_side_expression_statement_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_source_side_expression_statement_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_source_side_expression_statement_summary_v13.csv")
    require(len(rows) == 6, "M0 v13 source-side expression statement must define six components")
    require(
        {row["statement_component_id"] for row in rows}
        == {
            "M0NDSS13_STATEMENT_ENVELOPE",
            "M0NDSS13_SOURCE_SIDE_SCOPE",
            "M0NDSS13_NO_DARK_FAMILY_BINDING",
            "M0NDSS13_OUTPUT_INTENT",
            "M0NDSS13_FREEZE_GUARD",
            "M0NDSS13_NEXT_SLOT_HANDOFF",
        },
        "M0 v13 source-side statement component ids mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v13 source-side statement components must be ready")
    require(
        all(row["next_required_artifact"] == "m0_no_dark_statement_term_list_v13" for row in rows),
        "M0 v13 source-side statement must hand off to term list",
    )
    require(all(row["statement_claim_allowed"] == "false" for row in rows), "M0 v13 statement cannot allow statement claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v13 statement cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v13 statement cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 statement cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v13 statement must forbid residual leakage")
    require(len(summary) == 1, "M0 v13 source-side statement summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_SOURCE_SIDE_EXPRESSION_STATEMENT_V13", "M0 v13 source-side statement summary id mismatch")
    require(row["statement_artifact"] == "m0_no_dark_source_side_expression_statement_v13", "M0 v13 source-side statement artifact mismatch")
    require(row["frozen_expression_statement_contract_status"] == "READY", "M0 v13 source-side statement must inherit ready v12 contract")
    require(row["statement_components"] == "6", "M0 v13 source-side statement must summarize six components")
    require(row["ready_statement_components"] == "6", "M0 v13 source-side statement must ready six components")
    require(row["blocked_statement_components"] == "0", "M0 v13 source-side statement must block zero envelope components")
    require(row["source_side_statement_record_written"] == "true", "M0 v13 source-side statement record must be written")
    require(row["statement_body_written"] == "false", "M0 v13 source-side statement cannot write formula body")
    require(row["formula_claim_allowed"] == "false", "M0 v13 source-side statement cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v13 source-side statement must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 source-side statement summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_SOURCE_SIDE_EXPRESSION_STATEMENT_READY_FOR_TERM_LIST",
        "M0 v13 source-side statement status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_statement_term_list_v13", "M0 v13 source-side statement next artifact mismatch")


def validate_m0_no_dark_statement_term_list_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_statement_term_list_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_statement_term_list_summary_v13.csv")
    require(len(rows) == 6, "M0 v13 statement term list must define six term classes")
    require(
        {row["term_entry_id"] for row in rows}
        == {
            "M0NDSTL13_SOURCE_STATE_TERM",
            "M0NDSTL13_BARYONIC_INPUT_TERM",
            "M0NDSTL13_READOUT_OPERATOR_TERM",
            "M0NDSTL13_NO_DARK_CONSTRAINT_TERM",
            "M0NDSTL13_NULL_FALLBACK_TERM",
            "M0NDSTL13_ASSEMBLY_OPERATOR_TERM",
        },
        "M0 v13 statement term-list ids mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v13 term-list entries must be ready")
    require(
        all(row["next_required_artifact"] == "m0_no_dark_statement_argument_signature_v13" for row in rows),
        "M0 v13 term list must hand off to argument signature",
    )
    require(all(row["term_claim_allowed"] == "false" for row in rows), "M0 v13 term list cannot allow term claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v13 term list cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v13 term list cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 term list cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v13 term list must forbid residual leakage")
    require(len(summary) == 1, "M0 v13 term-list summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_STATEMENT_TERM_LIST_V13", "M0 v13 term-list summary id mismatch")
    require(row["term_list_artifact"] == "m0_no_dark_statement_term_list_v13", "M0 v13 term-list artifact mismatch")
    require(row["source_side_statement_status"] == "READY", "M0 v13 term list must inherit ready source-side statement")
    require(row["term_entries"] == "6", "M0 v13 term list must summarize six entries")
    require(row["ready_term_entries"] == "6", "M0 v13 term list must ready six entries")
    require(row["blocked_term_entries"] == "0", "M0 v13 term list must block zero term entries")
    require(row["term_list_written"] == "true", "M0 v13 term-list record must be written")
    require(row["formula_body_written"] == "false", "M0 v13 term list cannot write formula body")
    require(row["formula_claim_allowed"] == "false", "M0 v13 term list cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v13 term list must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 term-list summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_STATEMENT_TERM_LIST_READY_FOR_ARGUMENT_SIGNATURE",
        "M0 v13 term-list status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_statement_argument_signature_v13", "M0 v13 term-list next artifact mismatch")


def validate_m0_no_dark_statement_argument_signature_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_statement_argument_signature_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_statement_argument_signature_summary_v13.csv")
    require(len(rows) == 6, "M0 v13 statement argument signature must define six slots")
    require(
        {row["argument_slot_id"] for row in rows}
        == {
            "M0NDSAS13_SOURCE_STATE_ARGUMENT",
            "M0NDSAS13_BARYONIC_INPUT_ARGUMENT",
            "M0NDSAS13_RADIUS_GRID_ARGUMENT",
            "M0NDSAS13_READOUT_OPERATOR_ARGUMENT",
            "M0NDSAS13_GUARD_ARGUMENT",
            "M0NDSAS13_ASSEMBLY_ARGUMENT",
        },
        "M0 v13 statement argument-signature ids mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v13 argument slots must be ready")
    require(
        all(row["next_required_artifact"] == "m0_no_dark_statement_constraint_guards_v13" for row in rows),
        "M0 v13 argument signature must hand off to constraint guards",
    )
    require(all(row["argument_claim_allowed"] == "false" for row in rows), "M0 v13 argument signature cannot allow argument claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v13 argument signature cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v13 argument signature cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 argument signature cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v13 argument signature must forbid residual leakage")
    require(len(summary) == 1, "M0 v13 argument-signature summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_STATEMENT_ARGUMENT_SIGNATURE_V13", "M0 v13 argument-signature summary id mismatch")
    require(row["argument_signature_artifact"] == "m0_no_dark_statement_argument_signature_v13", "M0 v13 argument-signature artifact mismatch")
    require(row["term_list_status"] == "READY", "M0 v13 argument signature must inherit ready term list")
    require(row["argument_slots"] == "6", "M0 v13 argument signature must summarize six slots")
    require(row["ready_argument_slots"] == "6", "M0 v13 argument signature must ready six slots")
    require(row["blocked_argument_slots"] == "0", "M0 v13 argument signature must block zero argument slots")
    require(row["argument_signature_written"] == "true", "M0 v13 argument signature record must be written")
    require(row["formula_body_written"] == "false", "M0 v13 argument signature cannot write formula body")
    require(row["formula_claim_allowed"] == "false", "M0 v13 argument signature cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v13 argument signature must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 argument-signature summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_STATEMENT_ARGUMENT_SIGNATURE_READY_FOR_CONSTRAINT_GUARDS",
        "M0 v13 argument-signature status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_statement_constraint_guards_v13",
        "M0 v13 argument-signature next artifact mismatch",
    )


def validate_m0_no_dark_statement_constraint_guards_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_statement_constraint_guards_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_statement_constraint_guards_summary_v13.csv")
    require(len(rows) == 6, "M0 v13 statement constraint guards must define six guards")
    require(
        {row["guard_id"] for row in rows}
        == {
            "M0NDSCG13_DOMAIN_GUARD",
            "M0NDSCG13_NULL_GUARD",
            "M0NDSCG13_GAUGE_GUARD",
            "M0NDSCG13_NO_DARK_GUARD",
            "M0NDSCG13_FALLBACK_GUARD",
            "M0NDSCG13_LEAKAGE_FREEZE_GUARD",
        },
        "M0 v13 statement constraint-guard ids mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v13 guard rows must be ready")
    require(
        all(row["next_required_artifact"] == "m0_no_dark_statement_pre_dimensional_proof_v13" for row in rows),
        "M0 v13 guard rows must hand off to pre-dimensional proof",
    )
    require(all(row["guard_claim_allowed"] == "false" for row in rows), "M0 v13 guards cannot allow guard claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v13 guards cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v13 guards cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 guards cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v13 guards must forbid residual leakage")
    require(len(summary) == 1, "M0 v13 constraint-guard summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_STATEMENT_CONSTRAINT_GUARDS_V13", "M0 v13 guard summary id mismatch")
    require(row["constraint_guards_artifact"] == "m0_no_dark_statement_constraint_guards_v13", "M0 v13 guard artifact mismatch")
    require(row["argument_signature_status"] == "READY", "M0 v13 guards must inherit ready argument signature")
    require(row["guard_rows"] == "6", "M0 v13 guards must summarize six rows")
    require(row["ready_guard_rows"] == "6", "M0 v13 guards must ready six rows")
    require(row["blocked_guard_rows"] == "0", "M0 v13 guards must block zero guard rows")
    require(row["constraint_guards_written"] == "true", "M0 v13 guard record must be written")
    require(row["formula_body_written"] == "false", "M0 v13 guards cannot write formula body")
    require(row["formula_claim_allowed"] == "false", "M0 v13 guards cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v13 guards must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 guard summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_STATEMENT_CONSTRAINT_GUARDS_READY_FOR_PRE_DIMENSIONAL_PROOF",
        "M0 v13 guard status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_statement_pre_dimensional_proof_v13", "M0 v13 guard next artifact mismatch")


def validate_m0_no_dark_statement_pre_dimensional_proof_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_statement_pre_dimensional_proof_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_statement_pre_dimensional_proof_summary_v13.csv")
    require(len(rows) == 6, "M0 v13 statement pre-dimensional proof must define six proof rows")
    require(
        {row["proof_step_id"] for row in rows}
        == {
            "M0NDSPDP13_OUTPUT_CLASS_ROUTE",
            "M0NDSPDP13_ARGUMENT_DIMENSION_PLACEHOLDERS",
            "M0NDSPDP13_OPERATOR_DIMENSION_RULE",
            "M0NDSPDP13_GUARD_DIMENSION_POLICY",
            "M0NDSPDP13_NO_POSTHOC_UNIT_RESCALING",
            "M0NDSPDP13_HANDOFF_TO_FREEZE_PROVENANCE",
        },
        "M0 v13 statement pre-dimensional proof ids mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v13 pre-dimensional proof rows must be ready")
    require(
        all(row["next_required_artifact"] == "m0_no_dark_statement_freeze_provenance_v13" for row in rows),
        "M0 v13 pre-dimensional proof rows must hand off to freeze provenance",
    )
    require(all(row["proof_claim_allowed"] == "false" for row in rows), "M0 v13 proof route cannot allow proof claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v13 proof route cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v13 proof route cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 proof route cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v13 proof route must forbid residual leakage")
    require(len(summary) == 1, "M0 v13 pre-dimensional proof summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_STATEMENT_PRE_DIMENSIONAL_PROOF_V13", "M0 v13 proof summary id mismatch")
    require(
        row["pre_dimensional_proof_artifact"] == "m0_no_dark_statement_pre_dimensional_proof_v13",
        "M0 v13 proof artifact mismatch",
    )
    require(row["constraint_guards_status"] == "READY", "M0 v13 proof must inherit ready constraint guards")
    require(row["proof_rows"] == "6", "M0 v13 proof must summarize six rows")
    require(row["ready_proof_rows"] == "6", "M0 v13 proof must ready six rows")
    require(row["blocked_proof_rows"] == "0", "M0 v13 proof must block zero proof rows")
    require(row["pre_dimensional_proof_written"] == "true", "M0 v13 proof record must be written")
    require(row["formula_body_written"] == "false", "M0 v13 proof cannot write formula body")
    require(row["formula_claim_allowed"] == "false", "M0 v13 proof cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v13 proof must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 proof summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_STATEMENT_PRE_DIMENSIONAL_PROOF_READY_FOR_FREEZE_PROVENANCE",
        "M0 v13 proof status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_statement_freeze_provenance_v13", "M0 v13 proof next artifact mismatch")


def validate_m0_no_dark_statement_freeze_provenance_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_statement_freeze_provenance_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_statement_freeze_provenance_summary_v13.csv")
    require(len(rows) == 6, "M0 v13 statement freeze provenance must define six freeze rows")
    require(
        {row["freeze_record_id"] for row in rows}
        == {
            "M0NDSFP13_UPSTREAM_ROUTE_HASH",
            "M0NDSFP13_FORBIDDEN_INPUT_CUTOFF",
            "M0NDSFP13_SOURCE_SIDE_ONLY_SCOPE",
            "M0NDSFP13_REPRODUCIBLE_BUILD_HOOK",
            "M0NDSFP13_DOWNSTREAM_PAYLOAD_HANDOFF",
            "M0NDSFP13_DARK_SECTOR_NEUTRALITY",
        },
        "M0 v13 statement freeze-provenance ids mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v13 freeze rows must be ready")
    require(
        all(row["next_required_artifact"] == "m0_no_dark_frozen_expression_payload_v11" for row in rows),
        "M0 v13 freeze rows must hand off to payload",
    )
    require(all(row["freeze_claim_allowed"] == "false" for row in rows), "M0 v13 freeze cannot allow freeze claims")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v13 freeze cannot allow formula claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v13 freeze cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 freeze cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v13 freeze must forbid residual leakage")
    require(len(summary) == 1, "M0 v13 freeze summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_STATEMENT_FREEZE_PROVENANCE_V13", "M0 v13 freeze summary id mismatch")
    require(row["freeze_provenance_artifact"] == "m0_no_dark_statement_freeze_provenance_v13", "M0 v13 freeze artifact mismatch")
    require(row["pre_dimensional_proof_status"] == "READY", "M0 v13 freeze must inherit ready pre-dimensional proof")
    require(row["freeze_rows"] == "6", "M0 v13 freeze must summarize six rows")
    require(row["ready_freeze_rows"] == "6", "M0 v13 freeze must ready six rows")
    require(row["blocked_freeze_rows"] == "0", "M0 v13 freeze must block zero rows")
    require(row["freeze_provenance_written"] == "true", "M0 v13 freeze record must be written")
    require(row["formula_body_written"] == "false", "M0 v13 freeze cannot write formula body")
    require(row["formula_claim_allowed"] == "false", "M0 v13 freeze cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v13 freeze must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 freeze summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_STATEMENT_FREEZE_PROVENANCE_READY_FOR_PAYLOAD",
        "M0 v13 freeze status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_frozen_expression_payload_v11", "M0 v13 freeze next artifact mismatch")


def validate_m0_no_dark_equation_kernel_contract_v09() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_equation_kernel_contract_v09.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_equation_kernel_contract_summary_v09.csv")
    require(len(rows) == 6, "M0 v09 equation kernel contract must define six slots")
    require(
        {row["kernel_slot_id"] for row in rows}
        == {
            "M0NDEK09_EXPRESSION",
            "M0NDEK09_INPUT_BINDING",
            "M0NDEK09_OUTPUT_MAP",
            "M0NDEK09_PARAMETER_AUDIT",
            "M0NDEK09_FAILURE_POLICY",
            "M0NDEK09_REPRODUCIBLE_HOOK",
        },
        "M0 v09 kernel slot ids mismatch",
    )
    require(all(row["kernel_claim_allowed"] == "false" for row in rows), "M0 v09 cannot allow kernel claims")
    require(all(row["equation_claim_allowed"] == "false" for row in rows), "M0 v09 cannot allow equation claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v09 cannot allow numeric predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v09 cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v09 must forbid residual leakage")
    require(
        rows[0]["next_required_artifact"] == "m0_no_dark_kernel_expression_contract_v10",
        "M0 v09 next expression artifact mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v09 kernel slots must be ready")
    require(len(summary) == 1, "M0 v09 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EQUATION_KERNEL_CONTRACT_V09", "M0 v09 summary id mismatch")
    require(row["equation_kernel_artifact"] == "m0_no_dark_equation_kernel_v09", "M0 v09 artifact id mismatch")
    require(row["required_kernel_slots"] == "6", "M0 v09 must require six kernel slots")
    require(row["ready_kernel_slots"] == "6", "M0 v09 must ready six kernel slots")
    require(row["blocked_kernel_slots"] == "0", "M0 v09 must block zero expression slots")
    require(row["kernel_expressions_written"] == "1", "M0 v09 must register one kernel expression")
    require(row["numeric_predictions_written"] == "0", "M0 v09 must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v09 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_EQUATION_KERNEL_READY_FOR_READOUT_EQUATION",
        "M0 v09 status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_readout_equation_v08", "M0 v09 next artifact mismatch")


def validate_m0_no_dark_equation_kernel_interface_v09() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_equation_kernel_interface_v09.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_equation_kernel_interface_summary_v09.csv")
    require(len(rows) == 5, "M0 v09 kernel interface must define five rows")
    require(
        {row["kernel_slot_id"] for row in rows}
        == {
            "M0NDEK09_INPUT_BINDING",
            "M0NDEK09_OUTPUT_MAP",
            "M0NDEK09_PARAMETER_AUDIT",
            "M0NDEK09_FAILURE_POLICY",
            "M0NDEK09_REPRODUCIBLE_HOOK",
        },
        "M0 v09 kernel interface slot ids mismatch",
    )
    require(all(row["interface_status"] == "READY" for row in rows), "M0 v09 kernel interface rows must be ready")
    require(all(row["kernel_claim_allowed"] == "false" for row in rows), "M0 v09 kernel interface cannot allow kernel claims")
    require(all(row["equation_claim_allowed"] == "false" for row in rows), "M0 v09 kernel interface cannot allow equation claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v09 kernel interface cannot allow predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v09 kernel interface cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v09 kernel interface must forbid residual leakage")
    require(len(summary) == 1, "M0 v09 kernel interface summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EQUATION_KERNEL_INTERFACE_V09", "M0 v09 kernel interface summary id mismatch")
    require(row["interface_artifact"] == "m0_no_dark_equation_kernel_interface_v09", "M0 v09 kernel interface artifact mismatch")
    require(row["readout_equation_interface_status"] == "READY", "M0 v09 kernel interface must inherit ready readout interface")
    require(row["interface_rows"] == "5", "M0 v09 kernel interface must summarize five rows")
    require(row["ready_interface_rows"] == "5", "M0 v09 kernel interface must ready five rows")
    require(row["blocked_interface_rows"] == "0", "M0 v09 kernel interface must block zero rows")
    require(row["kernel_expression_written"] == "false", "M0 v09 kernel interface cannot write a kernel expression")
    require(row["kernel_claim_allowed"] == "false", "M0 v09 kernel interface cannot allow kernel claims")
    require(row["numeric_predictions_written"] == "0", "M0 v09 kernel interface must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v09 kernel interface summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_EQUATION_KERNEL_INTERFACE_READY",
        "M0 v09 kernel interface status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_kernel_expression_v10", "M0 v09 kernel interface next artifact mismatch")


def validate_m0_no_dark_readout_equation_contract_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_readout_equation_contract_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_readout_equation_contract_summary_v08.csv")
    require(len(rows) == 6, "M0 v08 readout equation contract must define six slots")
    require(
        {row["equation_slot_id"] for row in rows}
        == {
            "M0NDRE08_KERNEL",
            "M0NDRE08_ARGUMENT_SIGNATURE",
            "M0NDRE08_UNITS",
            "M0NDRE08_PARAMETERS",
            "M0NDRE08_DOMAIN",
            "M0NDRE08_SERIALIZATION",
        },
        "M0 v08 equation slot ids mismatch",
    )
    require(all(row["equation_claim_allowed"] == "false" for row in rows), "M0 v08 cannot allow equation claims")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v08 cannot allow numeric predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v08 cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v08 must forbid residual leakage")
    require(
        rows[0]["next_required_artifact"] == "m0_no_dark_equation_kernel_contract_v09",
        "M0 v08 next kernel artifact mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v08 equation slots must be ready")
    require(len(summary) == 1, "M0 v08 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_READOUT_EQUATION_CONTRACT_V08", "M0 v08 summary id mismatch")
    require(row["readout_equation_artifact"] == "m0_no_dark_readout_equation_v08", "M0 v08 artifact id mismatch")
    require(row["required_equation_slots"] == "6", "M0 v08 must require six equation slots")
    require(row["ready_equation_slots"] == "6", "M0 v08 must ready six equation slots")
    require(row["blocked_equation_slots"] == "0", "M0 v08 must block zero kernel slots")
    require(row["equations_written"] == "0", "M0 v08 must write zero equations")
    require(row["numeric_predictions_written"] == "0", "M0 v08 must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v08 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_READOUT_EQUATION_READY_FOR_FORMULA_BODY",
        "M0 v08 status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_formula_body_v07", "M0 v08 next artifact mismatch")


def validate_m0_no_dark_readout_equation_interface_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_readout_equation_interface_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_readout_equation_interface_summary_v08.csv")
    require(len(rows) == 5, "M0 v08 readout-equation interface must define five rows")
    require(
        {row["equation_slot_id"] for row in rows}
        == {
            "M0NDRE08_ARGUMENT_SIGNATURE",
            "M0NDRE08_UNITS",
            "M0NDRE08_PARAMETERS",
            "M0NDRE08_DOMAIN",
            "M0NDRE08_SERIALIZATION",
        },
        "M0 v08 readout-equation interface slot ids mismatch",
    )
    require(all(row["interface_status"] == "READY" for row in rows), "M0 v08 readout-equation interface rows must be ready")
    require(all(row["equation_claim_allowed"] == "false" for row in rows), "M0 v08 readout-equation interface cannot claim equation")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v08 readout-equation interface cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v08 readout-equation interface cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v08 readout-equation interface must forbid residual leakage")
    require(len(summary) == 1, "M0 v08 readout-equation interface summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_READOUT_EQUATION_INTERFACE_V08", "M0 v08 readout-equation interface summary id mismatch")
    require(row["interface_artifact"] == "m0_no_dark_readout_equation_interface_v08", "M0 v08 readout-equation interface artifact mismatch")
    require(row["formula_body_interface_status"] == "READY", "M0 v08 readout-equation interface must inherit formula-body interface")
    require(row["interface_rows"] == "5", "M0 v08 readout-equation interface must summarize five rows")
    require(row["ready_interface_rows"] == "5", "M0 v08 readout-equation interface must ready five rows")
    require(row["blocked_interface_rows"] == "0", "M0 v08 readout-equation interface must block zero interface rows")
    require(row["kernel_written"] == "false", "M0 v08 readout-equation interface cannot write kernel")
    require(row["equation_claim_allowed"] == "false", "M0 v08 readout-equation interface summary cannot allow equation claim")
    require(row["numeric_predictions_written"] == "0", "M0 v08 readout-equation interface summary cannot write predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v08 readout-equation interface summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_READOUT_EQUATION_INTERFACE_READY", "M0 v08 readout-equation interface status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_equation_kernel_v09", "M0 v08 readout-equation interface next artifact mismatch")


def validate_m0_no_dark_formula_body_interface_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_formula_body_interface_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_formula_body_interface_summary_v08.csv")
    require(len(rows) == 6, "M0 v08 formula-body interface must define six rows")
    require(
        {row["body_slot_id"] for row in rows}
        == {
            "M0NDB07_SOURCE_ARGUMENTS",
            "M0NDB07_BARYONIC_HANDOFF",
            "M0NDB07_SCALE_LAW",
            "M0NDB07_COEFFICIENT_DOMAIN",
            "M0NDB07_FALLBACK_BRANCHES",
            "M0NDB07_OUTPUT_UNIT_CHECK",
        },
        "M0 v08 formula-body interface slot ids mismatch",
    )
    require(all(row["interface_status"] == "READY" for row in rows), "M0 v08 interface rows must be ready")
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v08 interface cannot claim a formula")
    require(all(row["numeric_prediction_allowed"] == "false" for row in rows), "M0 v08 interface cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v08 interface cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v08 interface must forbid residual leakage")
    require(len(summary) == 1, "M0 v08 formula-body interface summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_FORMULA_BODY_INTERFACE_V08", "M0 v08 interface summary id mismatch")
    require(row["interface_artifact"] == "m0_no_dark_formula_body_interface_v08", "M0 v08 interface artifact mismatch")
    require(row["machine_form_status"] == "READY", "M0 v08 interface must inherit ready machine form")
    require(row["interface_rows"] == "6", "M0 v08 interface must summarize six rows")
    require(row["ready_interface_rows"] == "6", "M0 v08 interface must ready six rows")
    require(row["blocked_interface_rows"] == "0", "M0 v08 interface must block zero interface rows")
    require(row["readout_equation_written"] == "false", "M0 v08 interface cannot write readout equation")
    require(row["formula_claim_allowed"] == "false", "M0 v08 interface summary cannot allow formula claims")
    require(row["numeric_predictions_written"] == "0", "M0 v08 interface summary cannot write predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v08 interface summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_FORMULA_BODY_INTERFACE_READY", "M0 v08 interface status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_readout_equation_v08", "M0 v08 interface next artifact mismatch")


def validate_m0_no_dark_formula_body_contract_v07() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_formula_body_contract_v07.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_formula_body_contract_summary_v07.csv")
    require(len(rows) == 7, "M0 v07 body contract must define seven slots")
    require(
        {row["body_slot_id"] for row in rows}
        == {
            "M0NDB07_READOUT_EQUATION",
            "M0NDB07_SOURCE_ARGUMENTS",
            "M0NDB07_BARYONIC_HANDOFF",
            "M0NDB07_SCALE_LAW",
            "M0NDB07_COEFFICIENT_DOMAIN",
            "M0NDB07_FALLBACK_BRANCHES",
            "M0NDB07_OUTPUT_UNIT_CHECK",
        },
        "M0 v07 body slot ids mismatch",
    )
    require(all(row["formula_claim_allowed"] == "false" for row in rows), "M0 v07 cannot allow formula claims")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v07 cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v07 must forbid residual leakage")
    require(
        rows[0]["next_required_artifact"] == "m0_no_dark_readout_equation_contract_v08",
        "M0 v07 next equation artifact mismatch",
    )
    require(all(row["completion_status"] == "READY" for row in rows), "M0 v07 body slots must be ready")
    require(len(summary) == 1, "M0 v07 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_FORMULA_BODY_CONTRACT_V07", "M0 v07 summary id mismatch")
    require(row["formula_body_artifact"] == "m0_no_dark_formula_body_v07", "M0 v07 artifact id mismatch")
    require(row["required_body_slots"] == "7", "M0 v07 must require seven body slots")
    require(row["ready_body_slots"] == "7", "M0 v07 must ready seven body slots")
    require(row["blocked_body_slots"] == "0", "M0 v07 must block zero equation slots")
    require(row["formula_equations_written"] == "0", "M0 v07 must write zero equations")
    require(row["numeric_predictions_written"] == "0", "M0 v07 must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v07 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_FORMULA_BODY_READY_FOR_TABLE_FREEZE",
        "M0 v07 status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_formula_table_v06", "M0 v07 next artifact mismatch")


def validate_m0_no_dark_scale_policy_v07() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_scale_policy_v07.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_scale_policy_summary_v07.csv")
    require(len(rows) == 6, "M0 scale policy must define six rows")
    require(
        {row["scale_policy_id"] for row in rows}
        == {
            "M0NDSP07_RADIAL_DOMAIN",
            "M0NDSP07_NORMALIZATION_SCALE",
            "M0NDSP07_TRANSITION_SCALE",
            "M0NDSP07_SCALE_INVARIANCE_LIMITS",
            "M0NDSP07_ROW_SHARED_POLICY",
            "M0NDSP07_FALLBACK_HANDOFF",
        },
        "M0 scale policy ids mismatch",
    )
    require(all(row["policy_status"] == "READY" for row in rows), "M0 scale policy rows must be ready")
    require(all(row["numeric_scale_values_written"] == "0" for row in rows), "M0 scale policy cannot write values")
    require(all(row["prediction_rows_written"] == "0" for row in rows), "M0 scale policy cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 scale policy cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 scale policy must forbid residual leakage")
    require(all("posthoc_scale_selection" in row["forbidden_inputs"] for row in rows), "M0 scale policy must forbid posthoc scales")
    require(len(summary) == 1, "M0 scale policy summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_SCALE_POLICY_V07", "M0 scale policy summary id mismatch")
    require(row["source_artifact"] == "m0_no_dark_coefficient_policy_v07", "M0 scale policy source artifact mismatch")
    require(row["policy_rows"] == "6", "M0 scale policy must summarize six rows")
    require(row["ready_policy_rows"] == "6", "M0 scale policy must ready six rows")
    require(row["blocked_policy_rows"] == "0", "M0 scale policy must block zero rows")
    require(row["numeric_scale_values_written"] == "0", "M0 scale policy summary cannot write values")
    require(row["prediction_rows_written"] == "0", "M0 scale policy summary cannot write predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 scale policy summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_SCALE_POLICY_READY", "M0 scale policy status mismatch")
    require(row["next_required_artifact"] == "m0_no_dark_fallback_policy_v07", "M0 scale policy next artifact mismatch")


def validate_m0_no_dark_fallback_policy_v07() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_fallback_policy_v07.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_fallback_policy_summary_v07.csv")
    require(len(rows) == 6, "M0 fallback policy must define six rows")
    require(
        {row["fallback_policy_id"] for row in rows}
        == {
            "M0NDFP07_ZERO_RESPONSE_ROUTE",
            "M0NDFP07_MISSING_LABEL_ROUTE",
            "M0NDFP07_INADMISSIBLE_INPUT_ROUTE",
            "M0NDFP07_NULL_GAUGE_ROUTE",
            "M0NDFP07_FAILURE_REPORTING_ROUTE",
            "M0NDFP07_PREDICTION_TABLE_HANDOFF",
        },
        "M0 fallback policy ids mismatch",
    )
    require(all(row["policy_status"] == "READY" for row in rows), "M0 fallback policy rows must be ready")
    require(all(row["fallback_prediction_rows_written"] == "0" for row in rows), "M0 fallback policy cannot write fallback predictions")
    require(all(row["numeric_predictions_written"] == "0" for row in rows), "M0 fallback policy cannot write numeric predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 fallback policy cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 fallback policy must forbid residual leakage")
    require(all("posthoc_exception" in row["forbidden_inputs"] for row in rows), "M0 fallback policy must forbid posthoc exceptions")
    require(len(summary) == 1, "M0 fallback policy summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_FALLBACK_POLICY_V07", "M0 fallback policy summary id mismatch")
    require(row["source_artifact"] == "m0_no_dark_scale_policy_v07", "M0 fallback policy source artifact mismatch")
    require(row["policy_rows"] == "6", "M0 fallback policy must summarize six rows")
    require(row["ready_policy_rows"] == "6", "M0 fallback policy must ready six rows")
    require(row["blocked_policy_rows"] == "0", "M0 fallback policy must block zero rows")
    require(row["fallback_prediction_rows_written"] == "0", "M0 fallback policy summary cannot write fallback predictions")
    require(row["numeric_predictions_written"] == "0", "M0 fallback policy summary cannot write numeric predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 fallback policy summary cannot allow scoring")
    require(row["overall_status"] == "M0_NO_DARK_FALLBACK_POLICY_READY", "M0 fallback policy status mismatch")
    require(row["next_required_artifact"] == "family_prediction_tables_v08.csv", "M0 fallback policy next artifact mismatch")


def validate_m0_no_dark_formula_table_contract_v06() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_formula_table_contract_v06.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_formula_table_contract_summary_v06.csv")
    require(len(rows) == 6, "M0 v06 contract must define six components")
    require(
        {row["component_id"] for row in rows}
        == {
            "M0ND06_SOURCE_INPUTS",
            "M0ND06_READOUT_MAP",
            "M0ND06_COEFFICIENT_POLICY",
            "M0ND06_FIXED_SCALES",
            "M0ND06_FALLBACK_POLICY",
            "M0ND06_OUTPUT_SCHEMA",
        },
        "M0 v06 component ids mismatch",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v06 cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 v06 must forbid residual leakage")
    require(
        rows[0]["next_required_artifact"] == "m0_no_dark_formula_body_contract_v07",
        "M0 v06 next body artifact mismatch",
    )
    require(rows[0]["completion_status"] == "READY", "M0 v06 source inputs must be ready")
    require(rows[1]["completion_status"] == "READY", "M0 v06 readout map must be ready")
    require(rows[2]["completion_status"] == "READY", "M0 v06 coefficient policy must be ready")
    require(rows[3]["completion_status"] == "READY", "M0 v06 scale policy must be ready")
    require(rows[4]["completion_status"] == "READY", "M0 v06 fallback policy must be ready")
    require(rows[5]["completion_status"] == "READY", "M0 v06 output schema must be ready")
    require(len(summary) == 1, "M0 v06 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_FORMULA_TABLE_CONTRACT_V06", "M0 v06 summary id mismatch")
    require(row["formula_artifact"] == "m0_no_dark_formula_table_v06", "M0 v06 artifact id mismatch")
    require(row["required_components"] == "6", "M0 v06 must require six components")
    require(row["ready_components"] == "6", "M0 v06 must ready all six components after fallback policy")
    require(row["blocked_components"] == "0", "M0 v06 must block zero policy slots")
    require(row["formula_body_rows_written"] == "0", "M0 v06 must write zero formula-body rows")
    require(row["numeric_predictions_written"] == "0", "M0 v06 must write zero predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v06 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_FORMULA_TABLE_READY_FOR_PREDICTION_ROWS",
        "M0 v06 status mismatch",
    )
    require(row["next_required_artifact"] == "family_prediction_tables_v08.csv", "M0 v06 next artifact mismatch")


def validate_family_prediction_table_contract_v80() -> None:
    schema = read_csv(ROOT / "data/derived/family_prediction_table_schema_v80.csv")
    slots = read_csv(ROOT / "data/derived/family_prediction_table_slot_requirements_v80.csv")
    summary = read_csv(ROOT / "data/derived/family_prediction_table_contract_summary_v80.csv")
    fields = {row["field_name"] for row in schema}
    require({"scoring_row_id", "family_id", "v_pred_km_s"}.issubset(fields), "v80 schema missing required fields")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in schema), "v80 schema cannot allow scoring")
    require(len(slots) == 8, "v80 must cover eight formula slots")
    require(slots[0]["prediction_slot_status"] == "PREDICTION_SLOT_READY", "v80 first M0 slot must be ready")
    require(slots[1]["prediction_slot_status"] == "PREDICTION_SLOT_READY", "v80 second M0 slot must be ready")
    require(slots[2]["prediction_slot_status"] == "PREDICTION_SLOT_READY", "v80 first M1 slot must be ready")
    require(slots[3]["prediction_slot_status"] == "PREDICTION_SLOT_READY", "v80 second M1 slot must be ready")
    require(slots[4]["prediction_slot_status"] == "PREDICTION_SLOT_READY", "v80 first M2 slot must be ready")
    require(slots[5]["prediction_slot_status"] == "PREDICTION_SLOT_READY", "v80 second M2 slot must be ready")
    require(slots[6]["prediction_slot_status"] == "PREDICTION_SLOT_READY", "v80 shared input slot must be ready")
    require(slots[7]["prediction_slot_status"] == "PREDICTION_SLOT_READY", "v80 numeric count slot must be ready")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in slots), "v80 slots cannot allow scoring")
    require(
        slots[0]["required_formula_artifact"] == "family_prediction_tables_v08.csv",
        "v80 first formula artifact mismatch",
    )
    require(
        slots[1]["required_formula_artifact"] == "m0_label_rule_table_v06",
        "v80 second formula artifact mismatch",
    )
    require(
        slots[2]["required_formula_artifact"] == "m1_tau_response_formula_table_v06",
        "v80 third formula artifact mismatch",
    )
    require(
        slots[3]["required_formula_artifact"] == "m1_admissibility_table_v06",
        "v80 fourth formula artifact mismatch",
    )
    require(
        slots[4]["required_formula_artifact"] == "m2_benchmark_profile_table_v06",
        "v80 fifth formula artifact mismatch",
    )
    require(
        slots[5]["required_formula_artifact"] == "m2_nuisance_policy_table_v06",
        "v80 sixth formula artifact mismatch",
    )
    require(
        slots[6]["required_formula_artifact"] == "shared_scoring_input_table_v06",
        "v80 seventh formula artifact mismatch",
    )
    require(
        slots[7]["required_formula_artifact"] == "numeric_parameter_count_table_v06",
        "v80 eighth formula artifact mismatch",
    )
    require(len(summary) == 1, "v80 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "FAMILY_PREDICTION_TABLE_CONTRACT_V80", "v80 summary id mismatch")
    require(row["required_formula_slots"] == "8", "v80 must require eight formula slots")
    require(row["ready_formula_slots"] == "8", "v80 must ready eight formula slots")
    require(row["blocked_formula_slots"] == "0", "v80 must block zero formula slots")
    require(row["numeric_prediction_rows_written"] == "450", "v80 must write 450 M0 prediction rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v80 summary must forbid scoring")
    require(
        row["overall_status"] == "FAMILY_PREDICTION_TABLE_CONTRACT_READY_PARAMETER_COUNTS_BLOCKED",
        "v80 status mismatch",
    )
    require(row["next_required_artifact"] == "numeric_parameter_count_table_v08.csv", "v80 next artifact mismatch")
    require(
        row["claim_boundary"] == "family_prediction_table_contract_only_no_scores_no_dark_sector_verdict",
        "v80 claim boundary mismatch",
    )


def validate_family_prediction_tables_v08() -> None:
    table_path = ROOT / "data/derived/family_prediction_tables_v08.csv"
    rows = read_csv(table_path)
    summary = read_csv(ROOT / "data/derived/family_prediction_tables_summary_v08.csv")
    with table_path.open(newline="") as handle:
        fieldnames = csv.DictReader(handle).fieldnames
    require(len(rows) == 450, "v08 family prediction table must contain 450 M0 no-dark rows")
    require({row["family_id"] for row in rows} == {"M0"}, "v08 family prediction table must contain only M0")
    require(
        {row["prediction_source_slot"] for row in rows} == {"M0:no_dark_readout_formula"},
        "v08 family prediction source slot mismatch",
    )
    require(
        {row["prediction_status"] for row in rows} == {"PREDICTION_ROW_EMITTED_NOT_SCORED"},
        "v08 family prediction rows must remain unscored",
    )
    require(
        fieldnames
        == [
            "scoring_row_id",
            "galaxy_id",
            "family_id",
            "radial_index",
            "radius_kpc",
            "v_pred_km_s",
            "prediction_source_slot",
            "formula_table_status",
            "prediction_status",
        ],
        "v08 family prediction table header mismatch",
    )
    require(len(summary) == 1, "v08 family prediction table summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "FAMILY_PREDICTION_TABLES_V08", "v08 family prediction table summary id mismatch")
    require(row["table_header_written"] == "true", "v08 family prediction table header must be written")
    require(row["numeric_prediction_rows_written"] == "450", "v08 family prediction table must write 450 M0 rows")
    require(row["families_with_numeric_predictions"] == "1", "v08 family prediction table must ready one numeric family")
    require(row["m0_no_dark_formula_table_status"] == "M0_NO_DARK_ROWS_EMITTED", "v08 family prediction table must see M0 rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v08 family prediction table cannot allow scoring")
    require(
        row["overall_status"] == "FAMILY_PREDICTION_TABLES_M0_NO_DARK_ROWS_EMITTED_SCORING_BLOCKED",
        "v08 family prediction table status mismatch",
    )
    require(row["next_required_artifact"] == "m0_label_rule_table_v06", "v08 family prediction table next artifact mismatch")
    require(
        row["claim_boundary"] == "family_prediction_tables_m0_no_dark_rows_only_no_scores_no_dark_sector_verdict",
        "v08 family prediction table claim boundary mismatch",
    )


def validate_m0_no_dark_prediction_row_writer_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_prediction_row_writer_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_prediction_row_writer_summary_v08.csv")
    require(len(rows) == 5, "M0 prediction-row writer must have five checks")
    require(rows[0]["writer_decision"] == "READY_FOR_WRITER_REVIEW", "M0 writer handoff check mismatch")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 writer cannot write numeric prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 writer cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_executable_prediction_kernel_v08"},
        "M0 writer next artifact mismatch",
    )
    require(len(summary) == 1, "M0 writer summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_PREDICTION_ROW_WRITER_V08", "M0 writer summary id mismatch")
    require(row["writer_artifact"] == "m0_no_dark_prediction_row_writer_v08", "M0 writer artifact mismatch")
    require(row["writer_checks"] == "5", "M0 writer check count mismatch")
    require(row["blocked_writer_checks"] == "4", "M0 writer blocked check count mismatch")
    require(row["numeric_prediction_rows_written"] == "0", "M0 writer summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 writer summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 writer summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_PREDICTION_ROW_WRITER_PRESENT_BLOCKED_EXECUTABLE_KERNEL_MISSING",
        "M0 writer status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_executable_prediction_kernel_v08",
        "M0 writer next artifact mismatch",
    )


def validate_m0_no_dark_executable_prediction_kernel_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_executable_prediction_kernel_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_executable_prediction_kernel_summary_v08.csv")
    require(len(rows) == 6, "M0 executable kernel gate must have six checks")
    require(rows[0]["kernel_decision"] == "READY_FOR_EXECUTABLE_KERNEL_REVIEW", "M0 executable kernel handoff mismatch")
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 executable kernel cannot write formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 executable kernel cannot write prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 executable kernel cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_readout_formula_v08"},
        "M0 executable kernel next artifact mismatch",
    )
    require(len(summary) == 1, "M0 executable kernel summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_EXECUTABLE_PREDICTION_KERNEL_V08", "M0 executable kernel summary id mismatch")
    require(row["kernel_artifact"] == "m0_no_dark_executable_prediction_kernel_v08", "M0 executable kernel artifact mismatch")
    require(row["kernel_checks"] == "6", "M0 executable kernel check count mismatch")
    require(row["blocked_kernel_checks"] == "5", "M0 executable kernel blocked check count mismatch")
    require(row["velocity_formula_written"] == "false", "M0 executable kernel summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 executable kernel summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 executable kernel summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 executable kernel summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_EXECUTABLE_KERNEL_PRESENT_BLOCKED_VELOCITY_FORMULA_MISSING",
        "M0 executable kernel status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_readout_formula_v08",
        "M0 executable kernel next artifact mismatch",
    )


def validate_m0_no_dark_velocity_readout_formula_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_readout_formula_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_readout_formula_summary_v08.csv")
    require(len(rows) == 5, "M0 velocity formula gate must have five checks")
    require(rows[0]["formula_decision"] == "READY_FOR_VELOCITY_FORMULA_REVIEW", "M0 formula handoff mismatch")
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 formula gate cannot write formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 formula gate cannot write prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 formula gate cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_source_to_rotation_equation_body_v08"},
        "M0 formula gate next artifact mismatch",
    )
    require(len(summary) == 1, "M0 formula gate summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_VELOCITY_READOUT_FORMULA_V08", "M0 formula summary id mismatch")
    require(row["formula_artifact"] == "m0_no_dark_velocity_readout_formula_v08", "M0 formula artifact mismatch")
    require(row["formula_checks"] == "5", "M0 formula check count mismatch")
    require(row["blocked_formula_checks"] == "2", "M0 formula blocked check count mismatch")
    require(row["velocity_formula_written"] == "false", "M0 formula summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 formula summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 formula summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 formula summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_VELOCITY_FORMULA_PRESENT_BLOCKED_EQUATION_BODY_MISSING",
        "M0 formula status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_source_to_rotation_equation_body_v08",
        "M0 formula next artifact mismatch",
    )


def validate_m0_no_dark_source_to_rotation_equation_body_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_source_to_rotation_equation_body_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_source_to_rotation_equation_body_summary_v08.csv")
    require(len(rows) == 6, "M0 source-to-rotation equation-body gate must have six checks")
    require(rows[0]["equation_body_decision"] == "READY_FOR_EQUATION_BODY_REVIEW", "M0 equation-body handoff mismatch")
    require(all(row["equation_body_written"] == "false" for row in rows), "M0 equation-body gate cannot write equation body")
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 equation-body gate cannot write velocity formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 equation-body gate cannot write prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 equation-body gate cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_source_to_velocity_coupling_rule_v08"},
        "M0 equation-body gate next artifact mismatch",
    )
    require(len(summary) == 1, "M0 equation-body summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_SOURCE_TO_ROTATION_EQUATION_BODY_V08", "M0 equation-body summary id mismatch")
    require(row["equation_body_artifact"] == "m0_no_dark_source_to_rotation_equation_body_v08", "M0 equation-body artifact mismatch")
    require(row["equation_body_checks"] == "6", "M0 equation-body check count mismatch")
    require(row["blocked_equation_body_checks"] == "2", "M0 equation-body blocked check count mismatch")
    require(row["equation_body_written"] == "false", "M0 equation-body summary cannot write equation body")
    require(row["velocity_formula_written"] == "false", "M0 equation-body summary cannot write velocity formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 equation-body summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 equation-body summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 equation-body summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_EQUATION_BODY_PRESENT_BLOCKED_SOURCE_TO_VELOCITY_COUPLING_RULE_MISSING",
        "M0 equation-body status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_source_to_velocity_coupling_rule_v08",
        "M0 equation-body next artifact mismatch",
    )


def validate_m0_no_dark_source_to_velocity_coupling_rule_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_source_to_velocity_coupling_rule_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_source_to_velocity_coupling_rule_summary_v08.csv")
    require(len(rows) == 6, "M0 source-to-velocity coupling-rule gate must have six checks")
    require(rows[0]["coupling_rule_decision"] == "READY_FOR_COUPLING_RULE_REVIEW", "M0 coupling-rule handoff mismatch")
    require(all(row["coupling_rule_written"] == "false" for row in rows), "M0 coupling-rule gate cannot write coupling")
    require(all(row["velocity_unit_lift_written"] == "false" for row in rows), "M0 coupling-rule gate cannot write unit lift")
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 coupling-rule gate cannot write velocity formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 coupling-rule gate cannot write prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 coupling-rule gate cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_unit_lift_rule_v08"},
        "M0 coupling-rule gate next artifact mismatch",
    )
    require(len(summary) == 1, "M0 coupling-rule summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_SOURCE_TO_VELOCITY_COUPLING_RULE_V08", "M0 coupling-rule summary id mismatch")
    require(row["coupling_rule_artifact"] == "m0_no_dark_source_to_velocity_coupling_rule_v08", "M0 coupling-rule artifact mismatch")
    require(row["coupling_rule_checks"] == "6", "M0 coupling-rule check count mismatch")
    require(row["blocked_coupling_rule_checks"] == "3", "M0 coupling-rule blocked check count mismatch")
    require(row["coupling_rule_written"] == "false", "M0 coupling-rule summary cannot write coupling")
    require(row["velocity_unit_lift_written"] == "false", "M0 coupling-rule summary cannot write unit lift")
    require(row["velocity_formula_written"] == "false", "M0 coupling-rule summary cannot write velocity formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 coupling-rule summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 coupling-rule summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 coupling-rule summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_COUPLING_RULE_PRESENT_BLOCKED_VELOCITY_UNIT_LIFT_MISSING",
        "M0 coupling-rule status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_unit_lift_rule_v08",
        "M0 coupling-rule next artifact mismatch",
    )


def validate_m0_no_dark_velocity_unit_lift_rule_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_unit_lift_rule_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_unit_lift_rule_summary_v08.csv")
    require(len(rows) == 6, "M0 velocity-unit lift gate must have six checks")
    require(rows[0]["unit_lift_decision"] == "READY_FOR_UNIT_LIFT_REVIEW", "M0 unit-lift handoff mismatch")
    require(all(row["velocity_unit_lift_written"] == "false" for row in rows), "M0 unit-lift gate cannot write unit lift")
    require(all(row["dimension_anchor_written"] == "false" for row in rows), "M0 unit-lift gate cannot write dimension anchor")
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 unit-lift gate cannot write velocity formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 unit-lift gate cannot write prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 unit-lift gate cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_dimension_anchor_rule_v08"},
        "M0 unit-lift gate next artifact mismatch",
    )
    require(len(summary) == 1, "M0 unit-lift summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_VELOCITY_UNIT_LIFT_RULE_V08", "M0 unit-lift summary id mismatch")
    require(row["unit_lift_artifact"] == "m0_no_dark_velocity_unit_lift_rule_v08", "M0 unit-lift artifact mismatch")
    require(row["unit_lift_checks"] == "6", "M0 unit-lift check count mismatch")
    require(row["blocked_unit_lift_checks"] == "2", "M0 unit-lift blocked check count mismatch")
    require(row["velocity_unit_lift_written"] == "false", "M0 unit-lift summary cannot write unit lift")
    require(row["dimension_anchor_written"] == "false", "M0 unit-lift summary cannot write dimension anchor")
    require(row["velocity_formula_written"] == "false", "M0 unit-lift summary cannot write velocity formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 unit-lift summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 unit-lift summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 unit-lift summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_VELOCITY_UNIT_LIFT_PRESENT_BLOCKED_DIMENSION_ANCHOR_MISSING",
        "M0 unit-lift status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_dimension_anchor_rule_v08",
        "M0 unit-lift next artifact mismatch",
    )


def validate_m0_no_dark_velocity_dimension_anchor_rule_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_dimension_anchor_rule_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_dimension_anchor_rule_summary_v08.csv")
    require(len(rows) == 6, "M0 velocity-dimension anchor gate must have six checks")
    require(
        rows[0]["dimension_anchor_decision"] == "READY_FOR_DIMENSION_ANCHOR_REVIEW",
        "M0 dimension-anchor handoff mismatch",
    )
    require(
        all(row["dimension_anchor_written"] == "false" for row in rows),
        "M0 dimension-anchor gate cannot write dimension anchor",
    )
    require(
        all(row["anchor_source_law_written"] == "false" for row in rows),
        "M0 dimension-anchor gate cannot write anchor source law",
    )
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 dimension-anchor gate cannot write formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 dimension-anchor gate cannot write prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 dimension-anchor gate cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_source_law_v08"},
        "M0 dimension-anchor gate next artifact mismatch",
    )
    require(len(summary) == 1, "M0 dimension-anchor summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_VELOCITY_DIMENSION_ANCHOR_RULE_V08", "M0 dimension-anchor summary id mismatch")
    require(
        row["dimension_anchor_artifact"] == "m0_no_dark_velocity_dimension_anchor_rule_v08",
        "M0 dimension-anchor artifact mismatch",
    )
    require(row["dimension_anchor_checks"] == "6", "M0 dimension-anchor check count mismatch")
    require(row["blocked_dimension_anchor_checks"] == "2", "M0 dimension-anchor blocked count mismatch")
    require(row["dimension_anchor_written"] == "false", "M0 dimension-anchor summary cannot write anchor")
    require(row["anchor_source_law_written"] == "false", "M0 dimension-anchor summary cannot write anchor law")
    require(row["velocity_formula_written"] == "false", "M0 dimension-anchor summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 dimension-anchor summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 dimension-anchor summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 dimension-anchor summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_DIMENSION_ANCHOR_PRESENT_BLOCKED_ANCHOR_SOURCE_LAW_MISSING",
        "M0 dimension-anchor status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_anchor_source_law_v08",
        "M0 dimension-anchor next artifact mismatch",
    )


def validate_m0_no_dark_velocity_anchor_source_law_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_source_law_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_source_law_summary_v08.csv")
    require(len(rows) == 6, "M0 velocity-anchor source-law gate must have six checks")
    require(
        rows[0]["anchor_source_law_decision"] == "READY_FOR_ANCHOR_SOURCE_LAW_REVIEW",
        "M0 anchor-source-law handoff mismatch",
    )
    require(
        any(row["anchor_source_law_decision"] == "BLOCKED_ANCHOR_CANDIDATE_BASIS_MISSING" for row in rows),
        "M0 anchor-source-law gate must block on candidate basis",
    )
    require(
        all(row["anchor_source_law_written"] == "true" for row in rows),
        "M0 anchor-source-law gate must write the source-law layer",
    )
    require(
        all(row["anchor_candidate_basis_written"] == "false" for row in rows),
        "M0 anchor-source-law gate cannot write candidate basis",
    )
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 anchor-source-law gate cannot write formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 anchor-source-law gate cannot write prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 anchor-source-law gate cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_candidate_basis_v08"},
        "M0 anchor-source-law gate next artifact mismatch",
    )
    require(len(summary) == 1, "M0 anchor-source-law summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_VELOCITY_ANCHOR_SOURCE_LAW_V08", "M0 anchor-source-law summary id mismatch")
    require(
        row["anchor_source_law_artifact"] == "m0_no_dark_velocity_anchor_source_law_v08",
        "M0 anchor-source-law artifact mismatch",
    )
    require(row["anchor_source_law_checks"] == "6", "M0 anchor-source-law check count mismatch")
    require(row["blocked_anchor_source_law_checks"] == "1", "M0 anchor-source-law blocked count mismatch")
    require(row["anchor_source_law_written"] == "true", "M0 anchor-source-law summary must write source law")
    require(row["anchor_candidate_basis_written"] == "false", "M0 anchor-source-law summary cannot write candidate basis")
    require(row["velocity_formula_written"] == "false", "M0 anchor-source-law summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 anchor-source-law summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 anchor-source-law summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 anchor-source-law summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_ANCHOR_SOURCE_LAW_PRESENT_BLOCKED_ANCHOR_CANDIDATE_BASIS_MISSING",
        "M0 anchor-source-law status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_anchor_candidate_basis_v08",
        "M0 anchor-source-law next artifact mismatch",
    )


def validate_m0_no_dark_velocity_anchor_candidate_basis_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_candidate_basis_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_candidate_basis_summary_v08.csv")
    require(len(rows) == 6, "M0 velocity-anchor candidate-basis gate must have six checks")
    require(
        rows[0]["candidate_basis_decision"] == "READY_FOR_ANCHOR_CANDIDATE_BASIS_REVIEW",
        "M0 anchor-candidate-basis handoff mismatch",
    )
    require(
        sum(row["candidate_basis_decision"] == "ADMISSIBLE_CANDIDATE_CLASS_DECLARED" for row in rows) == 2,
        "M0 anchor-candidate basis must declare two admissible classes",
    )
    require(
        sum(row["candidate_basis_decision"] == "CONDITIONAL_CANDIDATE_CLASS_DECLARED" for row in rows) == 1,
        "M0 anchor-candidate basis must declare one conditional class",
    )
    require(
        any(row["candidate_basis_decision"] == "REJECTED_CANDIDATE_CLASS_DECLARED" for row in rows),
        "M0 anchor-candidate basis must reject rotation-fit carriers",
    )
    require(
        any(row["candidate_basis_decision"] == "BLOCKED_ANCHOR_SELECTION_RULE_MISSING" for row in rows),
        "M0 anchor-candidate basis must block on selection rule",
    )
    require(all(row["candidate_basis_written"] == "true" for row in rows), "M0 anchor-candidate basis must be written")
    require(
        all(row["anchor_selection_rule_written"] == "false" for row in rows),
        "M0 anchor-candidate basis cannot write selection rule",
    )
    require(all(row["anchor_value_written"] == "false" for row in rows), "M0 anchor-candidate basis cannot write values")
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 anchor-candidate basis cannot write formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 anchor-candidate basis cannot write prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 anchor-candidate basis cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_selection_rule_v08"},
        "M0 anchor-candidate basis next artifact mismatch",
    )
    require(len(summary) == 1, "M0 anchor-candidate basis summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M0_NO_DARK_VELOCITY_ANCHOR_CANDIDATE_BASIS_V08",
        "M0 anchor-candidate basis summary id mismatch",
    )
    require(
        row["anchor_candidate_basis_artifact"] == "m0_no_dark_velocity_anchor_candidate_basis_v08",
        "M0 anchor-candidate basis artifact mismatch",
    )
    require(row["candidate_basis_checks"] == "6", "M0 anchor-candidate basis check count mismatch")
    require(row["admissible_candidate_classes"] == "3", "M0 anchor-candidate basis admissible count mismatch")
    require(row["rejected_candidate_classes"] == "1", "M0 anchor-candidate basis rejected count mismatch")
    require(row["blocked_candidate_basis_checks"] == "1", "M0 anchor-candidate basis blocked count mismatch")
    require(row["candidate_basis_written"] == "true", "M0 anchor-candidate basis summary must write basis")
    require(row["anchor_selection_rule_written"] == "false", "M0 anchor-candidate basis summary cannot write selection rule")
    require(row["anchor_value_written"] == "false", "M0 anchor-candidate basis summary cannot write values")
    require(row["velocity_formula_written"] == "false", "M0 anchor-candidate basis summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 anchor-candidate basis summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 anchor-candidate basis summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 anchor-candidate basis summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_ANCHOR_CANDIDATE_BASIS_PRESENT_BLOCKED_ANCHOR_SELECTION_RULE_MISSING",
        "M0 anchor-candidate basis status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_anchor_selection_rule_v08",
        "M0 anchor-candidate basis next artifact mismatch",
    )


def validate_m0_no_dark_velocity_anchor_selection_rule_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_selection_rule_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_selection_rule_summary_v08.csv")
    require(len(rows) == 6, "M0 velocity-anchor selection-rule gate must have six checks")
    require(
        rows[0]["selection_rule_decision"] == "READY_FOR_ANCHOR_SELECTION_RULE_REVIEW",
        "M0 anchor-selection-rule handoff mismatch",
    )
    require(
        any(row["selection_rule_decision"] == "ANCHOR_SELECTION_PRIORITY_RULE_DECLARED" for row in rows),
        "M0 anchor-selection rule must declare priority order",
    )
    require(
        any(row["selection_rule_decision"] == "ANCHOR_SELECTION_FALLBACK_RULE_DECLARED" for row in rows),
        "M0 anchor-selection rule must declare fallback rule",
    )
    require(
        any(row["selection_rule_decision"] == "ANCHOR_SELECTION_REJECTION_RULE_DECLARED" for row in rows),
        "M0 anchor-selection rule must preserve rejected carrier class",
    )
    require(
        any(row["selection_rule_decision"] == "BLOCKED_ANCHOR_VALUE_FREEZE_MISSING" for row in rows),
        "M0 anchor-selection rule must block on value freeze",
    )
    require(
        all(row["anchor_selection_rule_written"] == "true" for row in rows),
        "M0 anchor-selection rule must be written",
    )
    require(all(row["anchor_value_written"] == "false" for row in rows), "M0 anchor-selection rule cannot write values")
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 anchor-selection rule cannot write formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 anchor-selection rule cannot write prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 anchor-selection rule cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_value_freeze_v08"},
        "M0 anchor-selection rule next artifact mismatch",
    )
    require(len(summary) == 1, "M0 anchor-selection rule summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M0_NO_DARK_VELOCITY_ANCHOR_SELECTION_RULE_V08",
        "M0 anchor-selection rule summary id mismatch",
    )
    require(
        row["anchor_selection_rule_artifact"] == "m0_no_dark_velocity_anchor_selection_rule_v08",
        "M0 anchor-selection rule artifact mismatch",
    )
    require(row["selection_rule_checks"] == "6", "M0 anchor-selection rule check count mismatch")
    require(row["declared_selection_rule_clauses"] == "4", "M0 anchor-selection rule declared clause count mismatch")
    require(row["blocked_selection_rule_checks"] == "1", "M0 anchor-selection rule blocked count mismatch")
    require(row["anchor_selection_rule_written"] == "true", "M0 anchor-selection rule summary must write rule")
    require(row["anchor_value_written"] == "false", "M0 anchor-selection rule summary cannot write values")
    require(row["velocity_formula_written"] == "false", "M0 anchor-selection rule summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 anchor-selection rule summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 anchor-selection rule summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 anchor-selection rule summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_ANCHOR_SELECTION_RULE_PRESENT_BLOCKED_ANCHOR_VALUE_FREEZE_MISSING",
        "M0 anchor-selection rule status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_anchor_value_freeze_v08",
        "M0 anchor-selection rule next artifact mismatch",
    )


def validate_m0_no_dark_velocity_anchor_value_freeze_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_value_freeze_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_value_freeze_summary_v08.csv")
    require(len(rows) == 22, "M0 anchor-value freeze must include four gate rows plus eighteen galaxy rows")
    require(
        rows[0]["value_freeze_decision"] == "READY_FOR_ANCHOR_VALUE_FREEZE_REVIEW",
        "M0 anchor-value freeze handoff mismatch",
    )
    require(
        any(row["value_freeze_decision"] == "BLOCKED_ANCHOR_UNIT_NORMALIZATION_MISSING" for row in rows),
        "M0 anchor-value freeze must block on unit normalization",
    )
    galaxy_rows = [row for row in rows if row["galaxy_id"] != "ALL"]
    require(len(galaxy_rows) == 18, "M0 anchor-value freeze must cover eighteen galaxies")
    require(
        sum(int(row["imported_source_rows"]) for row in galaxy_rows) == 450,
        "M0 anchor-value freeze must reference 450 imported source rows",
    )
    require(
        all(row["selected_anchor_class"] == "source_side_baryonic_gravity_velocity_carrier" for row in rows),
        "M0 anchor-value freeze must use the selected baryonic carrier class",
    )
    require(
        all(row["frozen_source_columns"] == "v_gas_km_s;v_disk_km_s;v_bulge_km_s" for row in rows),
        "M0 anchor-value freeze source columns mismatch",
    )
    require(
        all("v_obs_km_s" in row["forbidden_inputs"] for row in rows),
        "M0 anchor-value freeze must forbid observed velocity",
    )
    require(all(row["anchor_value_source_frozen"] == "true" for row in rows), "M0 anchor-value source must be frozen")
    require(
        all(row["anchor_numeric_value_rows_written"] == "0" for row in rows),
        "M0 anchor-value freeze cannot write numeric anchor rows",
    )
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 anchor-value freeze cannot write formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 anchor-value freeze cannot write prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 anchor-value freeze cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_unit_normalization_v08"},
        "M0 anchor-value freeze next artifact mismatch",
    )
    require(len(summary) == 1, "M0 anchor-value freeze summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M0_NO_DARK_VELOCITY_ANCHOR_VALUE_FREEZE_V08",
        "M0 anchor-value freeze summary id mismatch",
    )
    require(
        row["anchor_value_freeze_artifact"] == "m0_no_dark_velocity_anchor_value_freeze_v08",
        "M0 anchor-value freeze artifact mismatch",
    )
    require(row["value_freeze_rows"] == "22", "M0 anchor-value freeze row count mismatch")
    require(row["galaxy_value_freeze_rows"] == "18", "M0 anchor-value freeze galaxy count mismatch")
    require(row["imported_source_rows_referenced"] == "450", "M0 anchor-value freeze imported row count mismatch")
    require(row["blocked_value_freeze_checks"] == "1", "M0 anchor-value freeze blocked count mismatch")
    require(row["anchor_value_source_frozen"] == "true", "M0 anchor-value freeze summary must freeze source")
    require(row["anchor_numeric_value_rows_written"] == "0", "M0 anchor-value freeze summary cannot write numeric anchors")
    require(row["velocity_formula_written"] == "false", "M0 anchor-value freeze summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 anchor-value freeze summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 anchor-value freeze summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 anchor-value freeze summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_ANCHOR_VALUE_FREEZE_PRESENT_BLOCKED_UNIT_NORMALIZATION_MISSING",
        "M0 anchor-value freeze status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_anchor_unit_normalization_v08",
        "M0 anchor-value freeze next artifact mismatch",
    )


def validate_m0_no_dark_velocity_anchor_unit_normalization_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_unit_normalization_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_unit_normalization_summary_v08.csv")
    require(len(rows) == 7, "M0 anchor-unit normalization must have seven checks")
    require(
        rows[0]["unit_normalization_decision"] == "READY_FOR_ANCHOR_UNIT_NORMALIZATION_REVIEW",
        "M0 anchor-unit normalization handoff mismatch",
    )
    require(
        sum(row["unit_normalization_decision"] == "ANCHOR_UNIT_NORMALIZATION_DECLARED_NO_RESCALE" for row in rows) == 3,
        "M0 anchor-unit normalization must declare three source component units",
    )
    require(
        any(row["unit_normalization_decision"] == "BLOCKED_COMPONENT_COMBINATION_RULE_MISSING" for row in rows),
        "M0 anchor-unit normalization must block on component-combination rule",
    )
    require(
        {row["source_column"] for row in rows if row["anchor_unit_component"] == "source_component_unit"}
        == {"v_gas_km_s", "v_disk_km_s", "v_bulge_km_s"},
        "M0 anchor-unit normalization source component columns mismatch",
    )
    require(all(row["normalized_unit"] == "km/s" for row in rows), "M0 anchor-unit normalization must keep km/s")
    require(all("posthoc_unit_rescale" in row["forbidden_inputs"] for row in rows), "M0 anchor-unit must forbid posthoc rescale")
    require(all(row["unit_normalization_written"] == "true" for row in rows), "M0 anchor-unit normalization must be written")
    require(
        all(row["component_combination_rule_written"] == "false" for row in rows),
        "M0 anchor-unit normalization cannot write combination rule",
    )
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 anchor-unit normalization cannot write formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 anchor-unit normalization cannot write predictions",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 anchor-unit normalization cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_component_combination_rule_v08"},
        "M0 anchor-unit normalization next artifact mismatch",
    )
    require(len(summary) == 1, "M0 anchor-unit normalization summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M0_NO_DARK_VELOCITY_ANCHOR_UNIT_NORMALIZATION_V08",
        "M0 anchor-unit normalization summary id mismatch",
    )
    require(
        row["anchor_unit_normalization_artifact"] == "m0_no_dark_velocity_anchor_unit_normalization_v08",
        "M0 anchor-unit normalization artifact mismatch",
    )
    require(row["unit_normalization_checks"] == "7", "M0 anchor-unit normalization check count mismatch")
    require(row["source_component_units_normalized"] == "3", "M0 anchor-unit normalized component count mismatch")
    require(row["blocked_unit_normalization_checks"] == "1", "M0 anchor-unit blocked count mismatch")
    require(row["unit_normalization_written"] == "true", "M0 anchor-unit summary must write normalization")
    require(row["component_combination_rule_written"] == "false", "M0 anchor-unit summary cannot write combination rule")
    require(row["velocity_formula_written"] == "false", "M0 anchor-unit summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 anchor-unit summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 anchor-unit summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 anchor-unit summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_ANCHOR_UNIT_NORMALIZATION_PRESENT_BLOCKED_COMPONENT_COMBINATION_RULE_MISSING",
        "M0 anchor-unit normalization status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_anchor_component_combination_rule_v08",
        "M0 anchor-unit normalization next artifact mismatch",
    )


def validate_m0_no_dark_velocity_anchor_component_combination_rule_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_component_combination_rule_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_component_combination_rule_summary_v08.csv")
    require(len(rows) == 6, "M0 anchor component-combination rule must have six checks")
    require(
        rows[0]["component_combination_decision"] == "READY_FOR_COMPONENT_COMBINATION_RULE_REVIEW",
        "M0 anchor component-combination handoff mismatch",
    )
    require(
        any(row["component_combination_decision"] == "BLOCKED_COMPONENT_WEIGHT_POLICY_MISSING" for row in rows),
        "M0 anchor component-combination rule must block on component-weight policy",
    )
    require(
        all(row["source_columns"] == "v_gas_km_s;v_disk_km_s;v_bulge_km_s" for row in rows),
        "M0 anchor component-combination source columns mismatch",
    )
    require(
        all("v_obs_km_s" in row["forbidden_inputs"] for row in rows),
        "M0 anchor component-combination must forbid observed velocity",
    )
    require(
        all("posthoc_weight_fit" in row["forbidden_inputs"] for row in rows),
        "M0 anchor component-combination must forbid posthoc weight fitting",
    )
    require(
        all(row["component_combination_rule_written"] == "true" for row in rows),
        "M0 anchor component-combination rule must be written",
    )
    require(
        all(row["component_weight_policy_written"] == "false" for row in rows),
        "M0 anchor component-combination cannot write weight policy",
    )
    require(
        all(row["combined_anchor_values_written"] == "0" for row in rows),
        "M0 anchor component-combination cannot write combined values",
    )
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 anchor component-combination cannot write formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 anchor component-combination cannot write predictions",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 anchor component-combination cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_component_weight_policy_v08"},
        "M0 anchor component-combination next artifact mismatch",
    )
    require(len(summary) == 1, "M0 anchor component-combination summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M0_NO_DARK_VELOCITY_ANCHOR_COMPONENT_COMBINATION_RULE_V08",
        "M0 anchor component-combination summary id mismatch",
    )
    require(
        row["anchor_component_combination_artifact"] == "m0_no_dark_velocity_anchor_component_combination_rule_v08",
        "M0 anchor component-combination artifact mismatch",
    )
    require(row["component_combination_checks"] == "6", "M0 anchor component-combination check count mismatch")
    require(row["declared_component_combination_guards"] == "4", "M0 anchor component-combination guard count mismatch")
    require(row["blocked_component_combination_checks"] == "1", "M0 anchor component-combination blocked count mismatch")
    require(row["component_combination_rule_written"] == "true", "M0 anchor component-combination summary must write rule")
    require(row["component_weight_policy_written"] == "false", "M0 anchor component-combination summary cannot write weights")
    require(row["combined_anchor_values_written"] == "0", "M0 anchor component-combination summary cannot write values")
    require(row["velocity_formula_written"] == "false", "M0 anchor component-combination summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 anchor component-combination summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 anchor component-combination summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 anchor component-combination summary cannot allow scoring")
    require(
        row["overall_status"]
        == "M0_NO_DARK_ANCHOR_COMPONENT_COMBINATION_RULE_PRESENT_BLOCKED_COMPONENT_WEIGHT_POLICY_MISSING",
        "M0 anchor component-combination status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_anchor_component_weight_policy_v08",
        "M0 anchor component-combination next artifact mismatch",
    )


def validate_m0_no_dark_velocity_anchor_component_weight_policy_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_component_weight_policy_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_component_weight_policy_summary_v08.csv")
    require(len(rows) == 6, "M0 anchor component-weight policy must have six checks")
    require(
        rows[0]["weight_policy_decision"] == "READY_FOR_COMPONENT_WEIGHT_POLICY_REVIEW",
        "M0 anchor component-weight policy handoff mismatch",
    )
    require(
        any(row["weight_policy_decision"] == "BLOCKED_COMPONENT_WEIGHT_VALUE_FREEZE_MISSING" for row in rows),
        "M0 anchor component-weight policy must block on weight-value freeze",
    )
    require(
        all(row["source_columns"] == "v_gas_km_s;v_disk_km_s;v_bulge_km_s" for row in rows),
        "M0 anchor component-weight policy source columns mismatch",
    )
    require(
        all("posthoc_weight_fit" in row["forbidden_inputs"] for row in rows),
        "M0 anchor component-weight policy must forbid posthoc weight fitting",
    )
    require(
        all("posthoc_normalization" in row["forbidden_inputs"] for row in rows),
        "M0 anchor component-weight policy must forbid posthoc normalization",
    )
    require(
        all(row["component_weight_policy_written"] == "true" for row in rows),
        "M0 anchor component-weight policy must be written",
    )
    require(
        all(row["component_weight_values_frozen"] == "false" for row in rows),
        "M0 anchor component-weight policy cannot freeze values",
    )
    require(
        all(row["combined_anchor_values_written"] == "0" for row in rows),
        "M0 anchor component-weight policy cannot write combined values",
    )
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 anchor component-weight policy cannot write formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 anchor component-weight policy cannot write predictions",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 anchor component-weight policy cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_component_weight_value_freeze_v08"},
        "M0 anchor component-weight policy next artifact mismatch",
    )
    require(len(summary) == 1, "M0 anchor component-weight policy summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M0_NO_DARK_VELOCITY_ANCHOR_COMPONENT_WEIGHT_POLICY_V08",
        "M0 anchor component-weight policy summary id mismatch",
    )
    require(
        row["anchor_component_weight_policy_artifact"] == "m0_no_dark_velocity_anchor_component_weight_policy_v08",
        "M0 anchor component-weight policy artifact mismatch",
    )
    require(row["component_weight_policy_checks"] == "6", "M0 anchor component-weight policy check count mismatch")
    require(row["declared_component_weight_policy_guards"] == "4", "M0 anchor component-weight policy guard count mismatch")
    require(row["blocked_component_weight_policy_checks"] == "1", "M0 anchor component-weight policy blocked count mismatch")
    require(row["component_weight_policy_written"] == "true", "M0 anchor component-weight policy summary must write policy")
    require(row["component_weight_values_frozen"] == "false", "M0 anchor component-weight policy summary cannot freeze values")
    require(row["combined_anchor_values_written"] == "0", "M0 anchor component-weight policy summary cannot write values")
    require(row["velocity_formula_written"] == "false", "M0 anchor component-weight policy summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 anchor component-weight policy summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 anchor component-weight policy summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 anchor component-weight policy summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_ANCHOR_COMPONENT_WEIGHT_POLICY_PRESENT_BLOCKED_WEIGHT_VALUE_FREEZE_MISSING",
        "M0 anchor component-weight policy status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08",
        "M0 anchor component-weight policy next artifact mismatch",
    )


def validate_m0_no_dark_velocity_anchor_component_weight_value_freeze_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_component_weight_value_freeze_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_component_weight_value_freeze_summary_v08.csv")
    require(len(rows) == 6, "M0 anchor component-weight value freeze must have six checks")
    require(
        rows[0]["weight_value_freeze_decision"] == "READY_FOR_COMPONENT_WEIGHT_VALUE_FREEZE_REVIEW",
        "M0 anchor component-weight value-freeze handoff mismatch",
    )
    require(
        any(row["weight_value_freeze_decision"] == "BLOCKED_COMBINED_ANCHOR_RULE_MISSING" for row in rows),
        "M0 anchor component-weight value freeze must block on combined-anchor rule",
    )
    require(
        all(row["source_columns"] == "v_gas_km_s;v_disk_km_s;v_bulge_km_s" for row in rows),
        "M0 anchor component-weight value freeze source columns mismatch",
    )
    require(
        all("posthoc_combined_anchor_value" in row["forbidden_inputs"] for row in rows),
        "M0 anchor component-weight value freeze must forbid posthoc combined anchors",
    )
    require(
        all(row["component_weight_values_frozen"] == "true" for row in rows),
        "M0 anchor component-weight value freeze must freeze symbolic slots",
    )
    require(
        all(row["numeric_weight_values_written"] == "0" for row in rows),
        "M0 anchor component-weight value freeze cannot write numeric weights",
    )
    require(
        all(row["combined_anchor_rule_written"] == "false" for row in rows),
        "M0 anchor component-weight value freeze cannot write combined-anchor rule",
    )
    require(
        all(row["combined_anchor_values_written"] == "0" for row in rows),
        "M0 anchor component-weight value freeze cannot write combined values",
    )
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 anchor component-weight value freeze cannot write formula")
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 anchor component-weight value freeze cannot write predictions",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 anchor component-weight value freeze cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_velocity_anchor_combined_anchor_rule_v08"},
        "M0 anchor component-weight value freeze next artifact mismatch",
    )
    require(len(summary) == 1, "M0 anchor component-weight value freeze summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M0_NO_DARK_VELOCITY_ANCHOR_COMPONENT_WEIGHT_VALUE_FREEZE_V08",
        "M0 anchor component-weight value freeze summary id mismatch",
    )
    require(
        row["anchor_component_weight_value_freeze_artifact"]
        == "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08",
        "M0 anchor component-weight value freeze artifact mismatch",
    )
    require(row["component_weight_value_freeze_checks"] == "6", "M0 anchor component-weight value freeze check count mismatch")
    require(row["symbolic_weight_value_slots_frozen"] == "3", "M0 anchor component-weight value freeze frozen count mismatch")
    require(row["blocked_component_weight_value_freeze_checks"] == "1", "M0 anchor component-weight value freeze blocked count mismatch")
    require(row["component_weight_values_frozen"] == "true", "M0 anchor component-weight value freeze summary must freeze slots")
    require(row["numeric_weight_values_written"] == "0", "M0 anchor component-weight value freeze summary cannot write weights")
    require(row["combined_anchor_rule_written"] == "false", "M0 anchor component-weight value freeze summary cannot write rule")
    require(row["combined_anchor_values_written"] == "0", "M0 anchor component-weight value freeze summary cannot write values")
    require(row["velocity_formula_written"] == "false", "M0 anchor component-weight value freeze summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 anchor component-weight value freeze summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 anchor component-weight value freeze summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 anchor component-weight value freeze summary cannot allow scoring")
    require(
        row["overall_status"]
        == "M0_NO_DARK_ANCHOR_COMPONENT_WEIGHT_VALUE_FREEZE_PRESENT_BLOCKED_COMBINED_ANCHOR_RULE_MISSING",
        "M0 anchor component-weight value freeze status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_anchor_combined_anchor_rule_v08",
        "M0 anchor component-weight value freeze next artifact mismatch",
    )


def validate_m0_no_dark_velocity_anchor_combined_anchor_rule_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_combined_anchor_rule_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_combined_anchor_rule_summary_v08.csv")
    require(len(rows) == 6, "M0 combined-anchor rule must have six checks")
    require(
        rows[0]["combined_anchor_rule_decision"] == "READY_FOR_COMBINED_ANCHOR_RULE_REVIEW",
        "M0 combined-anchor rule handoff mismatch",
    )
    require(
        any(row["combined_anchor_rule_decision"] == "BLOCKED_COMBINED_ANCHOR_EXPRESSION_FREEZE_MISSING" for row in rows),
        "M0 combined-anchor rule must block on expression freeze",
    )
    require(
        all(row["source_columns"] == "v_gas_km_s;v_disk_km_s;v_bulge_km_s" for row in rows),
        "M0 combined-anchor rule source columns mismatch",
    )
    require(
        all("w_gas" in row["symbolic_slots"] and "n_anchor" in row["symbolic_slots"] for row in rows),
        "M0 combined-anchor rule symbolic slot mismatch",
    )
    require(
        all("posthoc_formula_switch" in row["forbidden_inputs"] for row in rows),
        "M0 combined-anchor rule must forbid posthoc formula switching",
    )
    require(all(row["combined_anchor_rule_written"] == "true" for row in rows), "M0 combined-anchor rule must be written")
    require(
        all(row["combined_anchor_expression_written"] == "false" for row in rows),
        "M0 combined-anchor rule cannot freeze expression",
    )
    require(
        all(row["combined_anchor_values_written"] == "0" for row in rows),
        "M0 combined-anchor rule cannot write values",
    )
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 combined-anchor rule cannot write formula")
    require(all(row["numeric_prediction_rows_written"] == "0" for row in rows), "M0 combined-anchor rule cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 combined-anchor rule cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows}
        == {"m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08"},
        "M0 combined-anchor rule next artifact mismatch",
    )
    require(len(summary) == 1, "M0 combined-anchor rule summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M0_NO_DARK_VELOCITY_ANCHOR_COMBINED_ANCHOR_RULE_V08",
        "M0 combined-anchor rule summary id mismatch",
    )
    require(
        row["anchor_combined_anchor_rule_artifact"] == "m0_no_dark_velocity_anchor_combined_anchor_rule_v08",
        "M0 combined-anchor rule artifact mismatch",
    )
    require(row["combined_anchor_rule_checks"] == "6", "M0 combined-anchor rule check count mismatch")
    require(row["declared_combined_anchor_rule_guards"] == "3", "M0 combined-anchor rule guard count mismatch")
    require(row["blocked_combined_anchor_rule_checks"] == "1", "M0 combined-anchor rule blocked count mismatch")
    require(row["combined_anchor_rule_written"] == "true", "M0 combined-anchor rule summary must write rule")
    require(row["combined_anchor_expression_written"] == "false", "M0 combined-anchor rule summary cannot write expression")
    require(row["combined_anchor_values_written"] == "0", "M0 combined-anchor rule summary cannot write values")
    require(row["velocity_formula_written"] == "false", "M0 combined-anchor rule summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 combined-anchor rule summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 combined-anchor rule summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 combined-anchor rule summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_RULE_PRESENT_BLOCKED_EXPRESSION_FREEZE_MISSING",
        "M0 combined-anchor rule status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08",
        "M0 combined-anchor rule next artifact mismatch",
    )


def validate_m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_summary_v08.csv")
    expression = (
        "v_anchor_sq_km2_s2 = (s_gas*w_gas*v_gas_km_s^2 + "
        "s_disk*w_disk*v_disk_km_s^2 + s_bulge*w_bulge*v_bulge_km_s^2) / n_anchor"
    )
    require(len(rows) == 6, "M0 combined-anchor expression freeze must have six checks")
    require(
        rows[0]["expression_freeze_decision"] == "READY_FOR_COMBINED_ANCHOR_EXPRESSION_FREEZE_REVIEW",
        "M0 combined-anchor expression freeze handoff mismatch",
    )
    require(
        any(row["expression_freeze_decision"] == "BLOCKED_COMBINED_ANCHOR_VALUE_FREEZE_MISSING" for row in rows),
        "M0 combined-anchor expression freeze must block on value freeze",
    )
    require(all(row["frozen_expression"] == expression for row in rows), "M0 combined-anchor expression mismatch")
    require(
        all(row["source_columns"] == "v_gas_km_s;v_disk_km_s;v_bulge_km_s" for row in rows),
        "M0 combined-anchor expression source columns mismatch",
    )
    require(
        all("w_gas" in row["symbolic_slots"] and "n_anchor" in row["symbolic_slots"] for row in rows),
        "M0 combined-anchor expression symbolic slot mismatch",
    )
    require(all("v_obs_km_s" in row["forbidden_inputs"] for row in rows), "M0 expression must forbid observed velocity")
    require(
        all(row["combined_anchor_expression_frozen"] == "true" for row in rows),
        "M0 combined-anchor expression must be frozen",
    )
    require(
        all(row["combined_anchor_values_written"] == "0" for row in rows),
        "M0 combined-anchor expression freeze cannot write values",
    )
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 expression freeze cannot write formula")
    require(all(row["numeric_prediction_rows_written"] == "0" for row in rows), "M0 expression freeze cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 expression freeze cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows}
        == {"m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08"},
        "M0 combined-anchor expression next artifact mismatch",
    )
    require(len(summary) == 1, "M0 combined-anchor expression summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M0_NO_DARK_VELOCITY_ANCHOR_COMBINED_ANCHOR_EXPRESSION_FREEZE_V08",
        "M0 combined-anchor expression summary id mismatch",
    )
    require(
        row["anchor_combined_anchor_expression_artifact"]
        == "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08",
        "M0 combined-anchor expression artifact mismatch",
    )
    require(row["expression_freeze_checks"] == "6", "M0 combined-anchor expression check count mismatch")
    require(row["frozen_expression_checks"] == "4", "M0 combined-anchor expression frozen count mismatch")
    require(row["blocked_expression_freeze_checks"] == "1", "M0 combined-anchor expression blocked count mismatch")
    require(row["combined_anchor_expression_frozen"] == "true", "M0 combined-anchor expression summary must freeze")
    require(row["frozen_expression"] == expression, "M0 combined-anchor expression summary expression mismatch")
    require(row["combined_anchor_values_written"] == "0", "M0 combined-anchor expression summary cannot write values")
    require(row["velocity_formula_written"] == "false", "M0 combined-anchor expression summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 combined-anchor expression summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 combined-anchor expression summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 combined-anchor expression summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_EXPRESSION_FROZEN_BLOCKED_VALUE_FREEZE_MISSING",
        "M0 combined-anchor expression status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
        "M0 combined-anchor expression next artifact mismatch",
    )


def validate_m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_summary_v08.csv")
    require(len(rows) == 450, "M0 combined-anchor value freeze must cover 450 source rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "M0 combined-anchor value freeze must cover eighteen galaxies")
    require(all(row["s_gas"] == row["s_disk"] == row["s_bulge"] == "1" for row in rows), "M0 signs must be identity")
    require(all(row["w_gas"] == row["w_disk"] == row["w_bulge"] == "1" for row in rows), "M0 weights must be identity")
    require(all(row["n_anchor"] == "1" for row in rows), "M0 normalization must be identity")
    require(all(float(row["v_anchor_sq_km2_s2"]) >= 0.0 for row in rows), "M0 anchor square cannot be negative")
    require(all(float(row["v_anchor_km_s"]) >= 0.0 for row in rows), "M0 anchor velocity cannot be negative")
    require(all("v_obs_km_s" in row["forbidden_inputs"] for row in rows), "M0 value freeze must forbid observed velocity")
    require(all(row["combined_anchor_values_written"] == "true" for row in rows), "M0 combined-anchor values must be written")
    require(all(row["velocity_formula_written"] == "false" for row in rows), "M0 value freeze cannot write formula")
    require(all(row["numeric_prediction_rows_written"] == "0" for row in rows), "M0 value freeze cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 value freeze cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows}
        == {"m0_no_dark_velocity_readout_formula_body_freeze_v08"},
        "M0 combined-anchor value next artifact mismatch",
    )
    require(len(summary) == 1, "M0 combined-anchor value summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M0_NO_DARK_VELOCITY_ANCHOR_COMBINED_ANCHOR_VALUE_FREEZE_V08",
        "M0 combined-anchor value summary id mismatch",
    )
    require(
        row["anchor_combined_anchor_value_artifact"] == "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
        "M0 combined-anchor value artifact mismatch",
    )
    require(row["source_rows_evaluated"] == "450", "M0 combined-anchor value row count mismatch")
    require(row["galaxies_with_anchor_values"] == "18", "M0 combined-anchor galaxy count mismatch")
    require(row["identity_weight_rows"] == "450", "M0 combined-anchor identity rows mismatch")
    require(row["negative_anchor_sq_rows"] == "0", "M0 combined-anchor negative square count mismatch")
    require(row["combined_anchor_values_written"] == "450", "M0 combined-anchor written count mismatch")
    require(row["velocity_formula_written"] == "false", "M0 combined-anchor value summary cannot write formula")
    require(row["numeric_prediction_rows_written"] == "0", "M0 combined-anchor value summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 combined-anchor value summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 combined-anchor value summary cannot allow scoring")
    require(
        row["overall_status"]
        == "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_VALUES_FROZEN_BLOCKED_VELOCITY_FORMULA_BODY_FREEZE_MISSING",
        "M0 combined-anchor value status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_velocity_readout_formula_body_freeze_v08",
        "M0 combined-anchor value summary next artifact mismatch",
    )


def validate_m0_no_dark_velocity_readout_formula_body_freeze_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_velocity_readout_formula_body_freeze_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_velocity_readout_formula_body_freeze_summary_v08.csv")
    formula_body = "v_body_km_s(R) := v_anchor_km_s(R)"
    require(len(rows) == 5, "M0 velocity formula-body freeze must have five checks")
    require(
        rows[0]["formula_body_freeze_decision"] == "READY_FOR_VELOCITY_FORMULA_BODY_FREEZE_REVIEW",
        "M0 formula-body freeze handoff mismatch",
    )
    require(
        any(row["formula_body_freeze_decision"] == "BLOCKED_PREDICTION_ROW_VALUE_FREEZE_MISSING" for row in rows),
        "M0 formula-body freeze must block on prediction row value freeze",
    )
    require(all(row["frozen_formula_body"] == formula_body for row in rows), "M0 formula-body freeze formula mismatch")
    require(all(row["formula_body_frozen"] == "true" for row in rows), "M0 formula body must be frozen")
    require(
        all(row["velocity_formula_body_written"] == "true" for row in rows),
        "M0 formula-body freeze must write the formula body",
    )
    require(
        all(row["numeric_prediction_rows_written"] == "0" for row in rows),
        "M0 formula-body freeze cannot write prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 formula-body freeze cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_prediction_row_value_freeze_v08"},
        "M0 formula-body freeze next artifact mismatch",
    )
    require(len(summary) == 1, "M0 formula-body freeze summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M0_NO_DARK_VELOCITY_READOUT_FORMULA_BODY_FREEZE_V08",
        "M0 formula-body freeze summary id mismatch",
    )
    require(
        row["formula_body_freeze_artifact"] == "m0_no_dark_velocity_readout_formula_body_freeze_v08",
        "M0 formula-body freeze artifact mismatch",
    )
    require(row["formula_body_freeze_checks"] == "5", "M0 formula-body freeze check count mismatch")
    require(row["frozen_formula_body_checks"] == "3", "M0 formula-body frozen check count mismatch")
    require(row["blocked_formula_body_freeze_checks"] == "1", "M0 formula-body blocked count mismatch")
    require(row["formula_body_frozen"] == "true", "M0 formula-body summary must freeze formula body")
    require(row["frozen_formula_body"] == formula_body, "M0 formula-body summary formula mismatch")
    require(row["velocity_formula_body_written"] == "true", "M0 formula-body summary must write formula body")
    require(row["numeric_prediction_rows_written"] == "0", "M0 formula-body summary cannot write predictions")
    require(row["families_with_numeric_predictions"] == "0", "M0 formula-body summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 formula-body summary cannot allow scoring")
    require(
        row["overall_status"]
        == "M0_NO_DARK_VELOCITY_FORMULA_BODY_FROZEN_BLOCKED_PREDICTION_ROW_VALUE_FREEZE_MISSING",
        "M0 formula-body freeze status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_prediction_row_value_freeze_v08",
        "M0 formula-body freeze summary next artifact mismatch",
    )


def validate_m0_no_dark_prediction_row_value_freeze_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_prediction_row_value_freeze_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_prediction_row_value_freeze_summary_v08.csv")
    formula_body = "v_body_km_s(R) := v_anchor_km_s(R)"
    require(len(rows) == 450, "M0 prediction row value freeze must cover 450 rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "M0 prediction row value freeze must cover eighteen galaxies")
    require({row["family_id"] for row in rows} == {"M0"}, "M0 prediction row value freeze must be M0-only")
    require(all(row["frozen_formula_body"] == formula_body for row in rows), "M0 prediction row value formula mismatch")
    require(
        all(row["v_anchor_km_s"] == row["frozen_prediction_value_km_s"] for row in rows),
        "M0 frozen prediction values must equal the frozen anchor values",
    )
    require(all("v_obs_km_s" in row["forbidden_inputs"] for row in rows), "M0 prediction value freeze must forbid observed velocity")
    require(all(row["prediction_row_values_frozen"] == "true" for row in rows), "M0 prediction row values must be frozen")
    require(all(row["family_prediction_rows_written"] == "0" for row in rows), "M0 prediction value freeze cannot write family rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 prediction value freeze cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_no_dark_family_prediction_row_emission_v08"},
        "M0 prediction value freeze next artifact mismatch",
    )
    require(len(summary) == 1, "M0 prediction value freeze summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_PREDICTION_ROW_VALUE_FREEZE_V08", "M0 prediction value summary id mismatch")
    require(
        row["prediction_row_value_freeze_artifact"] == "m0_no_dark_prediction_row_value_freeze_v08",
        "M0 prediction value artifact mismatch",
    )
    require(
        row["source_formula_body_artifact"] == "m0_no_dark_velocity_readout_formula_body_freeze_v08",
        "M0 prediction value formula-body source mismatch",
    )
    require(
        row["source_anchor_value_artifact"] == "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
        "M0 prediction value anchor source mismatch",
    )
    require(row["source_rows_evaluated"] == "450", "M0 prediction value source row count mismatch")
    require(row["galaxies_with_frozen_values"] == "18", "M0 prediction value galaxy count mismatch")
    require(row["family_id"] == "M0", "M0 prediction value summary family mismatch")
    require(row["frozen_formula_body"] == formula_body, "M0 prediction value summary formula mismatch")
    require(row["prediction_row_values_frozen"] == "450", "M0 prediction value frozen count mismatch")
    require(row["family_prediction_rows_written"] == "0", "M0 prediction value summary cannot write family rows")
    require(row["families_with_numeric_predictions"] == "0", "M0 prediction value summary cannot ready families")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 prediction value summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_PREDICTION_ROW_VALUES_FROZEN_BLOCKED_FAMILY_ROW_EMISSION_MISSING",
        "M0 prediction value status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_no_dark_family_prediction_row_emission_v08",
        "M0 prediction value summary next artifact mismatch",
    )


def validate_m0_no_dark_family_prediction_row_emission_v08() -> None:
    rows = read_csv(ROOT / "data/derived/m0_no_dark_family_prediction_row_emission_v08.csv")
    summary = read_csv(ROOT / "data/derived/m0_no_dark_family_prediction_row_emission_summary_v08.csv")
    require(len(rows) == 450, "M0 family prediction row emission must cover 450 rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "M0 family prediction row emission must cover 18 galaxies")
    require({row["family_id"] for row in rows} == {"M0"}, "M0 family prediction row emission family mismatch")
    require(
        {row["prediction_source_slot"] for row in rows} == {"M0:no_dark_readout_formula"},
        "M0 family prediction row emission source slot mismatch",
    )
    require(
        {row["prediction_status"] for row in rows} == {"PREDICTION_ROW_EMITTED_NOT_SCORED"},
        "M0 family prediction rows must remain unscored",
    )
    require(all(row["family_prediction_row_written"] == "true" for row in rows), "M0 family rows must be written")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 family rows cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_label_rule_table_v06"},
        "M0 family row emission next artifact mismatch",
    )
    require(len(summary) == 1, "M0 family row emission summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_NO_DARK_FAMILY_PREDICTION_ROW_EMISSION_V08", "M0 family row emission summary id mismatch")
    require(
        row["family_row_emission_artifact"] == "m0_no_dark_family_prediction_row_emission_v08",
        "M0 family row emission artifact mismatch",
    )
    require(
        row["target_prediction_table_artifact"] == "family_prediction_tables_v08.csv",
        "M0 family row emission target table mismatch",
    )
    require(
        row["source_prediction_row_value_artifact"] == "m0_no_dark_prediction_row_value_freeze_v08",
        "M0 family row emission source value artifact mismatch",
    )
    require(row["family_id"] == "M0", "M0 family row emission summary family mismatch")
    require(row["emitted_prediction_rows"] == "450", "M0 family row emission count mismatch")
    require(row["galaxies_with_emitted_rows"] == "18", "M0 family row emission galaxy count mismatch")
    require(row["families_with_numeric_predictions"] == "1", "M0 family row emission numeric family count mismatch")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 family row emission cannot allow scoring")
    require(
        row["overall_status"] == "M0_NO_DARK_FAMILY_PREDICTION_ROWS_EMITTED_SCORING_BLOCKED",
        "M0 family row emission status mismatch",
    )
    require(row["next_required_artifact"] == "m0_label_rule_table_v06", "M0 family row emission next artifact mismatch")
    require(
        row["claim_boundary"] == "m0_no_dark_family_prediction_row_emission_only_no_scores_no_dark_sector_verdict",
        "M0 family row emission claim boundary mismatch",
    )


def validate_m0_label_rule_table_v06() -> None:
    rows = read_csv(ROOT / "data/derived/m0_label_rule_table_v06.csv")
    summary = read_csv(ROOT / "data/derived/m0_label_rule_table_summary_v06.csv")
    require(len(rows) == 6, "M0 label rule table must define six components")
    require({row["family_id"] for row in rows} == {"M0"}, "M0 label rule family mismatch")
    require({row["formula_slot"] for row in rows} == {"morphology_label_rule"}, "M0 label rule slot mismatch")
    require(
        {row["rule_component"] for row in rows}
        == {
            "source_observables",
            "label_categories",
            "fallback_labels",
            "exception_policy",
            "row_selector",
            "freeze_audit",
        },
        "M0 label rule components mismatch",
    )
    require(all(row["frozen_before_scoring"] == "true" for row in rows), "M0 label rule must be frozen before scoring")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 label rule cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M0 label rule must forbid residual leakage")
    require(
        {row["next_required_artifact"] for row in rows} == {"m1_tau_response_formula_table_v06"},
        "M0 label rule next artifact mismatch",
    )
    require(len(summary) == 1, "M0 label rule summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_LABEL_RULE_TABLE_V06", "M0 label rule summary id mismatch")
    require(row["label_rule_artifact"] == "m0_label_rule_table_v06", "M0 label rule artifact mismatch")
    require(row["family_id"] == "M0", "M0 label rule summary family mismatch")
    require(row["formula_slot"] == "morphology_label_rule", "M0 label rule summary slot mismatch")
    require(row["rule_components"] == "6", "M0 label rule component count mismatch")
    require(row["activated_rows_covered"] == "18", "M0 label rule activated row count mismatch")
    require(row["row_label_values_written"] == "0", "M0 label rule cannot write row labels")
    require(row["label_rule_status"] == "M0_LABEL_RULE_TABLE_READY_NO_LABEL_VALUES", "M0 label rule status mismatch")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 label rule cannot allow scoring")
    require(row["overall_status"] == "M0_LABEL_RULE_TABLE_READY_SCORING_BLOCKED", "M0 label rule overall status mismatch")
    require(row["next_required_artifact"] == "m1_tau_response_formula_table_v06", "M0 label rule summary next artifact mismatch")
    require(
        row["claim_boundary"] == "m0_label_rule_table_only_no_label_validation_no_scores_no_dark_sector_verdict",
        "M0 label rule claim boundary mismatch",
    )


def validate_m1_tau_response_formula_table_v06() -> None:
    rows = read_csv(ROOT / "data/derived/m1_tau_response_formula_table_v06.csv")
    summary = read_csv(ROOT / "data/derived/m1_tau_response_formula_table_summary_v06.csv")
    require(len(rows) == 6, "M1 response formula table must define six components")
    require({row["family_id"] for row in rows} == {"M1"}, "M1 response formula family mismatch")
    require({row["formula_slot"] for row in rows} == {"tau_response_formula"}, "M1 response formula slot mismatch")
    require(
        {row["response_component"] for row in rows}
        == {
            "activation_rule",
            "carrier",
            "amplitude_law",
            "scale_law",
            "channel_handoff",
            "zero_response_policy",
        },
        "M1 response components mismatch",
    )
    require(all(row["response_tau_formula_claimed"] == "false" for row in rows), "M1 cannot claim Response_tau formula")
    require(all(row["numeric_response_values_written"] == "0" for row in rows), "M1 cannot write response values")
    require(all(row["family_prediction_rows_written"] == "0" for row in rows), "M1 cannot write prediction rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M1 response table cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M1 response table must forbid residual leakage")
    require(
        {row["next_required_artifact"] for row in rows} == {"m1_admissibility_table_v06"},
        "M1 response table next artifact mismatch",
    )
    require(len(summary) == 1, "M1 response summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M1_TAU_RESPONSE_FORMULA_TABLE_V06", "M1 response summary id mismatch")
    require(
        row["response_formula_table_artifact"] == "m1_tau_response_formula_table_v06",
        "M1 response artifact mismatch",
    )
    require(row["family_id"] == "M1", "M1 response summary family mismatch")
    require(row["formula_slot"] == "tau_response_formula", "M1 response summary slot mismatch")
    require(row["response_components"] == "6", "M1 response component count mismatch")
    require(row["response_tau_formula_claimed"] == "false", "M1 response summary cannot claim formula")
    require(row["numeric_response_values_written"] == "0", "M1 response summary cannot write values")
    require(row["family_prediction_rows_written"] == "0", "M1 response summary cannot write prediction rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M1 response summary cannot allow scoring")
    require(
        row["overall_status"] == "M1_TAU_RESPONSE_FORMULA_TABLE_READY_ADMISSIBILITY_BLOCKED",
        "M1 response overall status mismatch",
    )
    require(row["next_required_artifact"] == "m1_admissibility_table_v06", "M1 response next artifact mismatch")
    require(
        row["claim_boundary"] == "m1_tau_response_formula_table_only_no_response_tau_formula_no_predictions_no_scores",
        "M1 response claim boundary mismatch",
    )


def validate_m1_admissibility_table_v06() -> None:
    rows = read_csv(ROOT / "data/derived/m1_admissibility_table_v06.csv")
    summary = read_csv(ROOT / "data/derived/m1_admissibility_table_summary_v06.csv")
    require(len(rows) == 6, "M1 admissibility table must define six rows")
    require({row["family_id"] for row in rows} == {"M1"}, "M1 admissibility family mismatch")
    require({row["formula_slot"] for row in rows} == {"response_admissibility_rule"}, "M1 admissibility slot mismatch")
    require(
        {row["admissibility_class"] for row in rows}
        == {
            "source_freeze_admissibility",
            "non_circularity_guard",
            "no_posthoc_rescue_guard",
            "scale_readout_guard",
            "zero_response_guard",
            "prediction_handoff_guard",
        },
        "M1 admissibility classes mismatch",
    )
    require(all(row["admissibility_status"] == "READY" for row in rows), "M1 admissibility rows must be ready")
    require(
        all(row["response_tau_formula_claim_allowed"] == "false" for row in rows),
        "M1 admissibility cannot allow Response_tau formula claim",
    )
    require(
        all(row["numeric_response_values_allowed"] == "false" for row in rows),
        "M1 admissibility cannot allow response values",
    )
    require(all(row["family_prediction_rows_written"] == "0" for row in rows), "M1 admissibility cannot write rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M1 admissibility cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M1 admissibility must forbid residual leakage")
    require(
        {row["next_required_artifact"] for row in rows} == {"m2_benchmark_profile_table_v06"},
        "M1 admissibility next artifact mismatch",
    )
    require(len(summary) == 1, "M1 admissibility summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M1_ADMISSIBILITY_TABLE_V06", "M1 admissibility summary id mismatch")
    require(row["admissibility_artifact"] == "m1_admissibility_table_v06", "M1 admissibility artifact mismatch")
    require(row["response_formula_table_status"] == "READY", "M1 admissibility must inherit ready response table")
    require(row["admissibility_rows"] == "6", "M1 admissibility summary row count mismatch")
    require(row["ready_admissibility_rows"] == "6", "M1 admissibility must ready six rows")
    require(row["blocked_admissibility_rows"] == "0", "M1 admissibility must block zero rows")
    require(row["response_tau_formula_claim_allowed"] == "false", "M1 admissibility cannot allow formula claim")
    require(row["numeric_response_values_allowed"] == "false", "M1 admissibility cannot allow values")
    require(row["family_prediction_rows_written"] == "0", "M1 admissibility cannot write rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M1 admissibility cannot allow scoring")
    require(
        row["overall_status"] == "M1_ADMISSIBILITY_TABLE_READY_M2_BENCHMARK_BLOCKED",
        "M1 admissibility status mismatch",
    )
    require(row["next_required_artifact"] == "m2_benchmark_profile_table_v06", "M1 admissibility next artifact mismatch")
    require(
        row["claim_boundary"] == "m1_admissibility_table_only_no_response_tau_formula_no_values_no_predictions_no_scores",
        "M1 admissibility claim boundary mismatch",
    )


def validate_m1_response_parameter_inventory_v10() -> None:
    rows = read_csv(ROOT / "data/derived/m1_response_parameter_inventory_v10.csv")
    summary = read_csv(ROOT / "data/derived/m1_response_parameter_inventory_summary_v10.csv")
    require(len(rows) == 6, "M1 response inventory must define six rows")
    require(
        [row["inventory_row_id"] for row in rows] == [f"M1RPI10_{index:03d}" for index in range(1, 7)],
        "M1 response inventory ids mismatch",
    )
    require({row["readiness_id"] for row in rows} == {"NCR05_M1_GLOBAL"}, "M1 response inventory readiness mismatch")
    require({row["inventory_scope"] for row in rows} == {"global_response_parameters"}, "M1 response inventory scope mismatch")
    require(
        {row["response_component"] for row in rows}
        == {
            "activation_rule",
            "carrier",
            "amplitude_law",
            "scale_law",
            "channel_handoff",
            "zero_response_policy",
        },
        "M1 response inventory component mismatch",
    )
    require(all(row["countability_status"] == "COUNTABILITY_CLASSIFICATION_PENDING" for row in rows), "M1 inventory must defer countability")
    require(all(row["count_value_written"] == "0" for row in rows), "M1 inventory cannot write count values")
    require(all(row["numeric_response_value_written"] == "0" for row in rows), "M1 inventory cannot write response values")
    require(all(row["per_galaxy_privilege_written"] == "0" for row in rows), "M1 inventory cannot write per-galaxy privileges")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M1 inventory cannot allow scoring")
    require(
        all(row["next_required_artifact"] == "m1_response_parameter_count_classification_v11.csv" for row in rows),
        "M1 inventory next artifact mismatch",
    )
    require(len(summary) == 1, "M1 response inventory summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M1_RESPONSE_PARAMETER_INVENTORY_V10", "M1 inventory summary id mismatch")
    require(row["inventory_artifact"] == "m1_response_parameter_inventory_v10", "M1 inventory artifact mismatch")
    require(row["readiness_id"] == "NCR05_M1_GLOBAL", "M1 inventory summary readiness mismatch")
    require(row["inventory_rows"] == "6", "M1 inventory row count mismatch")
    require(row["inventory_rows_present"] == "6", "M1 inventory present count mismatch")
    require(row["countability_classified_rows"] == "0", "M1 inventory cannot classify rows")
    require(row["numeric_count_values_written"] == "0", "M1 inventory cannot write counts")
    require(row["numeric_response_values_written"] == "0", "M1 inventory cannot write values")
    require(row["per_galaxy_privilege_values_written"] == "0", "M1 inventory cannot write per-galaxy privileges")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M1 inventory cannot allow scoring")
    require(
        row["overall_status"] == "M1_RESPONSE_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING",
        "M1 inventory status mismatch",
    )
    require(
        row["next_required_artifact"] == "m1_response_parameter_count_classification_v11.csv",
        "M1 inventory summary next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m1_response_parameter_inventory_only_no_counts_no_values_no_scores",
        "M1 inventory claim boundary mismatch",
    )


def validate_m1_response_parameter_count_classification_v11() -> None:
    rows = read_csv(ROOT / "data/derived/m1_response_parameter_count_classification_v11.csv")
    summary = read_csv(ROOT / "data/derived/m1_response_parameter_count_classification_summary_v11.csv")
    require(len(rows) == 6, "M1 response count classification must define six rows")
    require(
        [row["classification_row_id"] for row in rows] == [f"M1RPCC11_{index:03d}" for index in range(1, 7)],
        "M1 response count classification ids mismatch",
    )
    require({row["readiness_id"] for row in rows} == {"NCR05_M1_GLOBAL"}, "M1 response classification readiness mismatch")
    require({row["family_id"] for row in rows} == {"M1"}, "M1 response classification family mismatch")
    require(
        {row["response_component"] for row in rows}
        == {
            "activation_rule",
            "carrier",
            "amplitude_law",
            "scale_law",
            "channel_handoff",
            "zero_response_policy",
        },
        "M1 response classification component mismatch",
    )
    classes = {row["response_component"]: row["countability_class"] for row in rows}
    require(
        classes
        == {
            "activation_rule": "FIXED_ADMISSIBILITY_GUARD_COUNTS_IF_ROW_SPECIFIC_SWITCH",
            "carrier": "FIXED_PLACEHOLDER_COUNTS_IF_PHYSICAL_CARRIER_PARAMETERIZED",
            "amplitude_law": "COUNT_IF_ADJUSTABLE_RESPONSE_AMPLITUDE",
            "scale_law": "COUNT_IF_ADJUSTABLE_RESPONSE_SCALE",
            "channel_handoff": "FIXED_PROTOCOL_HANDOFF_CHILD_SLOTS_COUNT",
            "zero_response_policy": "FIXED_NULL_ROUTE_COUNTS_IF_RESCUE_TERM",
        },
        "M1 response countability classes mismatch",
    )
    require(all(row["classification_status"] == "CLASSIFIED_COUNT_VALUE_PENDING" for row in rows), "M1 classification status mismatch")
    require(all(row["numeric_count_value_written"] == "0" for row in rows), "M1 classification cannot write counts")
    require(all(row["numeric_response_value_written"] == "0" for row in rows), "M1 classification cannot write response values")
    require(all(row["per_galaxy_privilege_value_written"] == "0" for row in rows), "M1 classification cannot write privileges")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M1 classification cannot allow scoring")
    require(
        all(row["next_required_artifact"] == "m1_response_parameter_count_value_ledger_v12.csv" for row in rows),
        "M1 classification next artifact mismatch",
    )
    require(len(summary) == 1, "M1 response classification summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M1_RESPONSE_PARAMETER_COUNT_CLASSIFICATION_V11", "M1 classification summary id mismatch")
    require(row["classification_artifact"] == "m1_response_parameter_count_classification_v11", "M1 classification artifact mismatch")
    require(row["classification_rows"] == "6", "M1 classification row count mismatch")
    require(row["classified_rows"] == "6", "M1 classification classified count mismatch")
    require(row["fixed_or_guard_classes"] == "4", "M1 classification fixed/guard count mismatch")
    require(row["count_if_adjustable_classes"] == "2", "M1 classification adjustable count mismatch")
    require(row["numeric_count_values_written"] == "0", "M1 classification summary cannot write counts")
    require(row["numeric_response_values_written"] == "0", "M1 classification summary cannot write response values")
    require(row["per_galaxy_privilege_values_written"] == "0", "M1 classification summary cannot write privileges")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M1 classification summary cannot allow scoring")
    require(
        row["overall_status"] == "M1_RESPONSE_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING",
        "M1 classification status mismatch",
    )
    require(
        row["next_required_artifact"] == "m1_response_parameter_count_value_ledger_v12.csv",
        "M1 classification summary next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m1_response_parameter_count_classification_only_no_counts_no_values_no_scores",
        "M1 classification claim boundary mismatch",
    )


def validate_m1_response_parameter_count_value_ledger_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m1_response_parameter_count_value_ledger_v12.csv")
    summary = read_csv(ROOT / "data/derived/m1_response_parameter_count_value_ledger_summary_v12.csv")
    require(len(rows) == 6, "M1 response count-value ledger must define six rows")
    require(
        [row["ledger_row_id"] for row in rows] == [f"M1RPCVL12_{index:03d}" for index in range(1, 7)],
        "M1 response count-value ledger ids mismatch",
    )
    require({row["readiness_id"] for row in rows} == {"NCR05_M1_GLOBAL"}, "M1 ledger readiness mismatch")
    require({row["family_id"] for row in rows} == {"M1"}, "M1 ledger family mismatch")
    statuses = {row["response_component"]: row["count_value_status"] for row in rows}
    require(
        statuses
        == {
            "activation_rule": "RESOLVED_ZERO_ADMISSIBILITY_GUARD",
            "carrier": "CONDITIONAL_COUNT_VALUE_PENDING",
            "amplitude_law": "CONDITIONAL_COUNT_VALUE_PENDING",
            "scale_law": "CONDITIONAL_COUNT_VALUE_PENDING",
            "channel_handoff": "RESOLVED_ZERO_PROTOCOL_HANDOFF_CONTAINER",
            "zero_response_policy": "RESOLVED_ZERO_NULL_ROUTE_GUARD",
        },
        "M1 ledger count-value statuses mismatch",
    )
    require(sum(row["slot_count_value"] == "0" for row in rows) == 3, "M1 ledger must write three zero slot values")
    require(sum(row["resolution_needed"] == "true" for row in rows) == 3, "M1 ledger must leave three conditional rows")
    require(all(row["final_m1_global_count_input_allowed"] == "false" for row in rows), "M1 ledger cannot allow final M1 count")
    require(all(row["response_value_input_allowed"] == "false" for row in rows), "M1 ledger cannot allow response values")
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "M1 ledger cannot allow parsimony")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M1 ledger cannot allow scoring")
    require(len(summary) == 1, "M1 response count-value ledger summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M1_RESPONSE_PARAMETER_COUNT_VALUE_LEDGER_V12", "M1 ledger summary id mismatch")
    require(row["ledger_artifact"] == "m1_response_parameter_count_value_ledger_v12", "M1 ledger artifact mismatch")
    require(row["classification_status"] == "M1_RESPONSE_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING", "M1 ledger classification status mismatch")
    require(row["ledger_rows"] == "6", "M1 ledger row count mismatch")
    require(row["resolved_zero_rows"] == "3", "M1 ledger zero row count mismatch")
    require(row["conditional_pending_rows"] == "3", "M1 ledger conditional row count mismatch")
    require(row["numeric_slot_count_values_written"] == "3", "M1 ledger numeric slot count mismatch")
    require(row["final_m1_global_count_written"] == "false", "M1 ledger cannot write final M1 count")
    require(row["numeric_response_values_written"] == "0", "M1 ledger cannot write response values")
    require(row["parsimony_scores_written"] == "0", "M1 ledger cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M1 ledger cannot allow scoring")
    require(
        row["overall_status"] == "M1_RESPONSE_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
        "M1 ledger status mismatch",
    )
    require(
        row["next_required_artifact"] == "m1_response_parameter_adjustable_slot_resolution_v13.csv",
        "M1 ledger next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m1_response_parameter_count_value_ledger_only_no_final_k_no_response_values_no_scores",
        "M1 ledger claim boundary mismatch",
    )


def validate_m1_response_parameter_adjustable_slot_resolution_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m1_response_parameter_adjustable_slot_resolution_v13.csv")
    summary = read_csv(ROOT / "data/derived/m1_response_parameter_adjustable_slot_resolution_summary_v13.csv")
    require(len(rows) == 3, "M1 response adjustable-slot resolution must define three rows")
    require(
        [row["resolution_row_id"] for row in rows] == [f"M1RPASR13_{index:03d}" for index in range(1, 4)],
        "M1 adjustable-slot resolution ids mismatch",
    )
    require(
        {row["ledger_row_id"] for row in rows} == {"M1RPCVL12_002", "M1RPCVL12_003", "M1RPCVL12_004"},
        "M1 adjustable-slot resolution source rows mismatch",
    )
    require(
        {row["response_component"] for row in rows} == {"carrier", "amplitude_law", "scale_law"},
        "M1 adjustable-slot resolution components mismatch",
    )
    require(
        all(row["slot_resolution_status"] == "RESOLVED_ZERO_INACTIVE_OR_PLACEHOLDER_RESPONSE_SLOT" for row in rows),
        "M1 adjustable-slot resolution statuses mismatch",
    )
    require(all(row["slot_count_value"] == "0" for row in rows), "M1 adjustable-slot resolution must write zero slot values")
    require(
        all(row["adjustable_response_parameter_found"] == "false" for row in rows),
        "M1 adjustable-slot resolution cannot find adjustable response parameters",
    )
    require(
        all(row["final_count_candidate_input_allowed"] == "true" for row in rows),
        "M1 adjustable-slot resolution must allow only final-count candidate input",
    )
    require(all(row["response_value_input_allowed"] == "false" for row in rows), "M1 adjustable-slot resolution cannot allow response values")
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "M1 adjustable-slot resolution cannot allow parsimony")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M1 adjustable-slot resolution cannot allow scoring")
    require(
        all(row["next_required_artifact"] == "m1_response_parameter_final_count_candidate_v14.csv" for row in rows),
        "M1 adjustable-slot resolution next artifact mismatch",
    )
    require(len(summary) == 1, "M1 adjustable-slot resolution summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M1_RESPONSE_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13", "M1 adjustable-slot summary id mismatch")
    require(row["resolution_artifact"] == "m1_response_parameter_adjustable_slot_resolution_v13", "M1 adjustable-slot artifact mismatch")
    require(
        row["ledger_status"] == "M1_RESPONSE_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
        "M1 adjustable-slot ledger status mismatch",
    )
    require(row["conditional_rows_checked"] == "3", "M1 adjustable-slot conditional row count mismatch")
    require(row["resolved_zero_rows"] == "3", "M1 adjustable-slot resolved-zero count mismatch")
    require(row["unresolved_rows"] == "0", "M1 adjustable-slot unresolved row count mismatch")
    require(row["adjustable_response_parameters_found"] == "0", "M1 adjustable-slot adjustable count mismatch")
    require(row["final_m1_global_count_candidate_ready"] == "true", "M1 adjustable-slot must ready the final-count candidate input")
    require(row["final_m1_global_count_written"] == "false", "M1 adjustable-slot cannot write final M1 count")
    require(row["numeric_response_values_written"] == "0", "M1 adjustable-slot cannot write response values")
    require(row["parsimony_scores_written"] == "0", "M1 adjustable-slot cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M1 adjustable-slot cannot allow scoring")
    require(
        row["overall_status"] == "M1_RESPONSE_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE",
        "M1 adjustable-slot status mismatch",
    )
    require(
        row["next_required_artifact"] == "m1_response_parameter_final_count_candidate_v14.csv",
        "M1 adjustable-slot next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m1_response_parameter_adjustable_slot_resolution_only_no_final_k_no_response_values_no_scores",
        "M1 adjustable-slot claim boundary mismatch",
    )


def validate_m1_response_parameter_final_count_candidate_v14() -> None:
    rows = read_csv(ROOT / "data/derived/m1_response_parameter_final_count_candidate_v14.csv")
    summary = read_csv(ROOT / "data/derived/m1_response_parameter_final_count_candidate_summary_v14.csv")
    require(len(rows) == 1, "M1 v14 final-count candidate must have one row")
    row = rows[0]
    require(row["candidate_row_id"] == "M1RPFC14_001", "M1 v14 candidate row id mismatch")
    require(row["family_id"] == "M1", "M1 v14 family mismatch")
    require(row["count_domain"] == "global_response_parameters", "M1 v14 count domain mismatch")
    require(
        row["input_artifacts"] == "m1_response_parameter_count_value_ledger_v12.csv;m1_response_parameter_adjustable_slot_resolution_v13.csv",
        "M1 v14 input artifacts mismatch",
    )
    require(row["slot_count_rows_used"] == "6", "M1 v14 must use six slot count rows")
    require(row["resolved_zero_slot_rows"] == "6", "M1 v14 must resolve six zero rows")
    require(row["unresolved_slot_rows"] == "0", "M1 v14 unresolved row count mismatch")
    require(row["adjustable_response_parameters_found"] == "0", "M1 v14 adjustable response count mismatch")
    require(row["candidate_k_m1_global"] == "0", "M1 v14 candidate count mismatch")
    require(
        row["candidate_status"] == "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
        "M1 v14 candidate status mismatch",
    )
    require(row["freeze_input_allowed"] == "true", "M1 v14 must allow freeze input")
    require(row["response_value_input_allowed"] == "false", "M1 v14 cannot allow response values")
    require(row["parsimony_input_allowed"] == "false", "M1 v14 cannot allow parsimony")
    require(row["endpoint_scoring_allowed"] == "false", "M1 v14 cannot allow scoring")
    require(
        row["next_required_artifact"] == "m1_response_parameter_final_count_freeze_v15.csv",
        "M1 v14 next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m1_response_parameter_final_count_candidate_only_no_freeze_no_response_values_no_scores",
        "M1 v14 claim boundary mismatch",
    )
    require(len(summary) == 1, "M1 v14 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14", "M1 v14 summary id mismatch")
    require(row["candidate_artifact"] == "m1_response_parameter_final_count_candidate_v14", "M1 v14 artifact mismatch")
    require(
        row["v12_ledger_status"] == "M1_RESPONSE_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
        "M1 v14 v12 status mismatch",
    )
    require(
        row["v13_resolution_status"] == "M1_RESPONSE_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE",
        "M1 v14 v13 status mismatch",
    )
    require(row["slot_count_rows_used"] == "6", "M1 v14 summary slot count mismatch")
    require(row["resolved_zero_slot_rows"] == "6", "M1 v14 summary zero rows mismatch")
    require(row["unresolved_slot_rows"] == "0", "M1 v14 summary unresolved rows mismatch")
    require(row["adjustable_response_parameters_found"] == "0", "M1 v14 summary adjustable response count mismatch")
    require(row["candidate_k_m1_global"] == "0", "M1 v14 summary candidate count mismatch")
    require(row["final_count_frozen"] == "false", "M1 v14 cannot freeze final count")
    require(row["numeric_response_values_written"] == "0", "M1 v14 cannot write response values")
    require(row["parsimony_scores_written"] == "0", "M1 v14 cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M1 v14 summary cannot allow scoring")
    require(
        row["overall_status"] == "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
        "M1 v14 summary status mismatch",
    )
    require(
        row["next_required_artifact"] == "m1_response_parameter_final_count_freeze_v15.csv",
        "M1 v14 summary next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m1_response_parameter_final_count_candidate_only_no_freeze_no_response_values_no_scores",
        "M1 v14 summary claim boundary mismatch",
    )


def validate_m1_response_parameter_final_count_freeze_v15() -> None:
    rows = read_csv(ROOT / "data/derived/m1_response_parameter_final_count_freeze_v15.csv")
    summary = read_csv(ROOT / "data/derived/m1_response_parameter_final_count_freeze_summary_v15.csv")
    require(len(rows) == 1, "M1 v15 final-count freeze must have one row")
    row = rows[0]
    require(row["freeze_row_id"] == "M1RPFCF15_001", "M1 v15 freeze row id mismatch")
    require(row["candidate_row_id"] == "M1RPFC14_001", "M1 v15 candidate row id mismatch")
    require(row["family_id"] == "M1", "M1 v15 family mismatch")
    require(row["count_domain"] == "global_response_parameters", "M1 v15 count domain mismatch")
    require(row["frozen_k_m1_global"] == "0", "M1 v15 frozen count mismatch")
    require(
        row["freeze_status"] == "M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_RESPONSE_PRIVILEGE_AUDIT_PENDING",
        "M1 v15 freeze status mismatch",
    )
    require(
        row["candidate_status"] == "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
        "M1 v15 candidate status mismatch",
    )
    require(row["per_galaxy_response_privilege_input_allowed"] == "true", "M1 v15 must allow the per-galaxy audit input")
    require(row["response_value_input_allowed"] == "false", "M1 v15 cannot allow response values")
    require(row["parsimony_input_allowed"] == "false", "M1 v15 cannot allow parsimony")
    require(row["endpoint_scoring_allowed"] == "false", "M1 v15 cannot allow scoring")
    require(
        row["next_required_artifact"] == "m1_per_galaxy_response_privilege_count_audit_v10.csv",
        "M1 v15 next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m1_response_parameter_final_count_freeze_only_no_response_values_no_parsimony_no_scores",
        "M1 v15 claim boundary mismatch",
    )
    require(len(summary) == 1, "M1 v15 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15", "M1 v15 summary id mismatch")
    require(row["freeze_artifact"] == "m1_response_parameter_final_count_freeze_v15", "M1 v15 artifact mismatch")
    require(
        row["candidate_status"] == "M1_RESPONSE_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
        "M1 v15 summary candidate status mismatch",
    )
    require(row["frozen_k_m1_global"] == "0", "M1 v15 summary frozen count mismatch")
    require(row["final_count_frozen"] == "true", "M1 v15 must freeze final count")
    require(row["numeric_response_values_written"] == "0", "M1 v15 cannot write response values")
    require(row["per_galaxy_response_privilege_counts_written"] == "0", "M1 v15 cannot write per-galaxy counts")
    require(row["parsimony_scores_written"] == "0", "M1 v15 cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M1 v15 summary cannot allow scoring")
    require(
        row["overall_status"] == "M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_RESPONSE_PRIVILEGE_AUDIT_PENDING",
        "M1 v15 summary status mismatch",
    )
    require(
        row["next_required_artifact"] == "m1_per_galaxy_response_privilege_count_audit_v10.csv",
        "M1 v15 summary next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m1_response_parameter_final_count_freeze_only_no_response_values_no_parsimony_no_scores",
        "M1 v15 summary claim boundary mismatch",
    )


def validate_m1_per_galaxy_response_privilege_count_audit_v10() -> None:
    rows = read_csv(ROOT / "data/derived/m1_per_galaxy_response_privilege_count_audit_v10.csv")
    summary = read_csv(ROOT / "data/derived/m1_per_galaxy_response_privilege_count_audit_summary_v10.csv")
    require(len(rows) == 18, "M1 per-galaxy response privilege audit must cover eighteen rows")
    require(
        [row["audit_row_id"] for row in rows] == [f"M1PGRPCA10_{index:03d}" for index in range(1, 19)],
        "M1 per-galaxy response privilege audit ids mismatch",
    )
    require(
        {row["source_activation_status"] for row in rows} == {"ACTIVATION_BLOCKED"},
        "M1 per-galaxy audit must preserve source activation status",
    )
    require(
        {row["m1_global_freeze_status"] for row in rows}
        == {"M1_RESPONSE_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_RESPONSE_PRIVILEGE_AUDIT_PENDING"},
        "M1 per-galaxy audit must inherit M1 global freeze status",
    )
    require(
        {row["m1_admissibility_status"] for row in rows} == {"M1_ADMISSIBILITY_TABLE_READY_M2_BENCHMARK_BLOCKED"},
        "M1 per-galaxy audit must inherit M1 admissibility status",
    )
    require(
        {row["row_response_privilege_status"] for row in rows}
        == {"RESOLVED_ZERO_NO_ROW_SPECIFIC_M1_RESPONSE_PRIVILEGE"},
        "M1 per-galaxy audit must resolve all rows as zero response privileges",
    )
    require(
        all(row["per_galaxy_response_privilege_count_value"] == "0" for row in rows),
        "M1 per-galaxy audit counts must be zero",
    )
    require(all(row["freeze_input_allowed"] == "true" for row in rows), "M1 per-galaxy audit must allow freeze input")
    require(
        all(row["response_value_input_allowed"] == "false" for row in rows),
        "M1 per-galaxy audit cannot allow response values",
    )
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "M1 per-galaxy audit cannot allow parsimony")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M1 per-galaxy audit cannot allow scoring")
    require(
        all(row["next_required_artifact"] == "m1_per_galaxy_response_privilege_count_freeze_v11.csv" for row in rows),
        "M1 per-galaxy audit next artifact mismatch",
    )
    require(len(summary) == 1, "M1 per-galaxy audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_AUDIT_V10",
        "M1 per-galaxy audit summary id mismatch",
    )
    require(
        row["audit_artifact"] == "m1_per_galaxy_response_privilege_count_audit_v10",
        "M1 per-galaxy audit artifact mismatch",
    )
    require(row["source_rows_checked"] == "18", "M1 per-galaxy audit source row count mismatch")
    require(row["resolved_zero_rows"] == "18", "M1 per-galaxy audit resolved row count mismatch")
    require(row["unresolved_rows"] == "0", "M1 per-galaxy audit unresolved count mismatch")
    require(row["per_galaxy_response_privilege_values_written"] == "18", "M1 per-galaxy audit value count mismatch")
    require(row["per_galaxy_response_count_freeze_ready"] == "true", "M1 per-galaxy audit must be ready for freeze")
    require(row["per_galaxy_response_count_frozen"] == "false", "M1 per-galaxy audit cannot freeze count")
    require(row["numeric_response_values_written"] == "0", "M1 per-galaxy audit cannot write response values")
    require(row["parsimony_scores_written"] == "0", "M1 per-galaxy audit cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M1 per-galaxy audit cannot allow scoring")
    require(
        row["overall_status"] == "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE",
        "M1 per-galaxy audit status mismatch",
    )
    require(
        row["next_required_artifact"] == "m1_per_galaxy_response_privilege_count_freeze_v11.csv",
        "M1 per-galaxy audit summary next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m1_per_galaxy_response_privilege_count_audit_only_no_freeze_no_response_values_no_scores",
        "M1 per-galaxy audit claim boundary mismatch",
    )


def validate_m1_per_galaxy_response_privilege_count_freeze_v11() -> None:
    rows = read_csv(ROOT / "data/derived/m1_per_galaxy_response_privilege_count_freeze_v11.csv")
    summary = read_csv(ROOT / "data/derived/m1_per_galaxy_response_privilege_count_freeze_summary_v11.csv")
    require(len(rows) == 18, "M1 per-galaxy response privilege freeze must cover eighteen rows")
    require(
        [row["freeze_row_id"] for row in rows] == [f"M1PGRPCF11_{index:03d}" for index in range(1, 19)],
        "M1 per-galaxy response privilege freeze ids mismatch",
    )
    require(
        {row["freeze_status"] for row in rows}
        == {"M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11_FROZEN"},
        "M1 per-galaxy response privilege freeze status mismatch",
    )
    require(
        {row["audit_status"] for row in rows} == {"RESOLVED_ZERO_NO_ROW_SPECIFIC_M1_RESPONSE_PRIVILEGE"},
        "M1 per-galaxy response privilege freeze audit status mismatch",
    )
    require(
        all(row["frozen_per_galaxy_response_privilege_count"] == "0" for row in rows),
        "M1 per-galaxy response privilege freeze values must be zero",
    )
    require(
        all(row["response_value_input_allowed"] == "false" for row in rows),
        "M1 per-galaxy response privilege freeze cannot allow response values",
    )
    require(
        all(row["parsimony_input_allowed"] == "false" for row in rows),
        "M1 per-galaxy response privilege freeze cannot allow parsimony",
    )
    require(
        all(row["endpoint_scoring_allowed"] == "false" for row in rows),
        "M1 per-galaxy response privilege freeze cannot allow scoring",
    )
    require(
        all(row["next_required_artifact"] == "m2_benchmark_parameter_inventory_v10.csv" for row in rows),
        "M1 per-galaxy response privilege freeze next artifact mismatch",
    )
    require(len(summary) == 1, "M1 per-galaxy response privilege freeze summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11",
        "M1 per-galaxy response privilege freeze summary id mismatch",
    )
    require(
        row["freeze_artifact"] == "m1_per_galaxy_response_privilege_count_freeze_v11",
        "M1 per-galaxy response privilege freeze artifact mismatch",
    )
    require(
        row["audit_status"] == "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE",
        "M1 per-galaxy response privilege freeze audit summary status mismatch",
    )
    require(row["source_rows_checked"] == "18", "M1 per-galaxy response privilege freeze source row count mismatch")
    require(row["frozen_zero_rows"] == "18", "M1 per-galaxy response privilege freeze zero row count mismatch")
    require(row["unresolved_rows"] == "0", "M1 per-galaxy response privilege freeze unresolved count mismatch")
    require(row["per_galaxy_response_count_frozen"] == "true", "M1 per-galaxy response privilege freeze must freeze")
    require(
        row["frozen_per_galaxy_response_privilege_count_total"] == "0",
        "M1 per-galaxy response privilege freeze total mismatch",
    )
    require(row["numeric_response_values_written"] == "0", "M1 per-galaxy response privilege freeze cannot write values")
    require(row["parsimony_scores_written"] == "0", "M1 per-galaxy response privilege freeze cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M1 per-galaxy response privilege freeze cannot score")
    require(
        row["overall_status"] == "M1_PER_GALAXY_RESPONSE_PRIVILEGE_COUNT_FREEZE_V11_READY_M2_GLOBAL_COUNT_PENDING",
        "M1 per-galaxy response privilege freeze status mismatch",
    )
    require(
        row["next_required_artifact"] == "m2_benchmark_parameter_inventory_v10.csv",
        "M1 per-galaxy response privilege freeze summary next artifact mismatch",
    )
    require(
        row["claim_boundary"]
        == "m1_per_galaxy_response_privilege_count_freeze_only_no_response_values_no_parsimony_no_scores",
        "M1 per-galaxy response privilege freeze claim boundary mismatch",
    )


def validate_m2_benchmark_parameter_inventory_v10() -> None:
    rows = read_csv(ROOT / "data/derived/m2_benchmark_parameter_inventory_v10.csv")
    summary = read_csv(ROOT / "data/derived/m2_benchmark_parameter_inventory_summary_v10.csv")
    require(len(rows) == 12, "M2 benchmark parameter inventory must cover twelve rows")
    require(
        [row["inventory_row_id"] for row in rows] == [f"M2BPI10_{index:03d}" for index in range(1, 13)],
        "M2 benchmark parameter inventory ids mismatch",
    )
    require({row["readiness_id"] for row in rows} == {"NCR05_M2_GLOBAL"}, "M2 inventory readiness id mismatch")
    require({row["family_id"] for row in rows} == {"M2"}, "M2 inventory family id mismatch")
    require(
        {row["source_artifact"] for row in rows}
        == {"m2_benchmark_profile_table_v06", "m2_nuisance_policy_table_v06"},
        "M2 inventory source artifacts mismatch",
    )
    require(
        sum(row["source_artifact"] == "m2_benchmark_profile_table_v06" for row in rows) == 6,
        "M2 inventory profile source row count mismatch",
    )
    require(
        sum(row["source_artifact"] == "m2_nuisance_policy_table_v06" for row in rows) == 6,
        "M2 inventory nuisance source row count mismatch",
    )
    require(
        all(row["countability_status"] == "COUNTABILITY_CLASSIFICATION_PENDING" for row in rows),
        "M2 inventory countability must remain pending",
    )
    require(all(row["count_value_written"] == "0" for row in rows), "M2 inventory cannot write count values")
    require(
        all(row["numeric_benchmark_value_written"] == "0" for row in rows),
        "M2 inventory cannot write benchmark values",
    )
    require(
        all(row["family_prediction_rows_written"] == "0" for row in rows),
        "M2 inventory cannot write prediction rows",
    )
    require(
        all(row["per_galaxy_privilege_written"] == "0" for row in rows),
        "M2 inventory cannot write per-galaxy privileges",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M2 inventory cannot allow scoring")
    require(
        all(row["next_required_artifact"] == "m2_benchmark_parameter_count_classification_v11.csv" for row in rows),
        "M2 inventory next artifact mismatch",
    )
    require(len(summary) == 1, "M2 inventory summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M2_BENCHMARK_PARAMETER_INVENTORY_V10", "M2 inventory summary id mismatch")
    require(row["inventory_artifact"] == "m2_benchmark_parameter_inventory_v10", "M2 inventory artifact mismatch")
    require(row["readiness_id"] == "NCR05_M2_GLOBAL", "M2 inventory summary readiness id mismatch")
    require(row["family_id"] == "M2", "M2 inventory summary family id mismatch")
    require(row["inventory_rows"] == "12", "M2 inventory summary row count mismatch")
    require(row["profile_source_rows"] == "6", "M2 inventory profile row count mismatch")
    require(row["nuisance_source_rows"] == "6", "M2 inventory nuisance row count mismatch")
    require(row["inventory_rows_present"] == "12", "M2 inventory rows present mismatch")
    require(row["countability_classified_rows"] == "0", "M2 inventory cannot classify countability")
    require(row["numeric_count_values_written"] == "0", "M2 inventory cannot write count values")
    require(row["numeric_benchmark_values_written"] == "0", "M2 inventory cannot write benchmark values")
    require(row["family_prediction_rows_written"] == "0", "M2 inventory cannot write prediction rows")
    require(row["per_galaxy_privilege_values_written"] == "0", "M2 inventory cannot write privilege values")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M2 inventory cannot allow scoring")
    require(
        row["overall_status"] == "M2_BENCHMARK_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING",
        "M2 inventory status mismatch",
    )
    require(
        row["next_required_artifact"] == "m2_benchmark_parameter_count_classification_v11.csv",
        "M2 inventory summary next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m2_benchmark_parameter_inventory_only_no_counts_no_values_no_predictions_no_scores",
        "M2 inventory claim boundary mismatch",
    )


def validate_m2_benchmark_parameter_count_classification_v11() -> None:
    rows = read_csv(ROOT / "data/derived/m2_benchmark_parameter_count_classification_v11.csv")
    summary = read_csv(ROOT / "data/derived/m2_benchmark_parameter_count_classification_summary_v11.csv")
    require(len(rows) == 12, "M2 benchmark parameter classification must cover twelve rows")
    require(
        [row["classification_row_id"] for row in rows] == [f"M2BPCC11_{index:03d}" for index in range(1, 13)],
        "M2 benchmark parameter classification ids mismatch",
    )
    require({row["readiness_id"] for row in rows} == {"NCR05_M2_GLOBAL"}, "M2 classification readiness id mismatch")
    require({row["family_id"] for row in rows} == {"M2"}, "M2 classification family id mismatch")
    require(
        {row["classification_status"] for row in rows} == {"CLASSIFIED_COUNT_VALUE_PENDING"},
        "M2 classification status mismatch",
    )
    require(
        sum(row["countability_class"].startswith("FIXED_") for row in rows) == 4,
        "M2 classification fixed/guard count mismatch",
    )
    require(
        sum("COUNT_IF" in row["countability_class"] for row in rows) == 8,
        "M2 classification count-if count mismatch",
    )
    require(all(row["numeric_count_value_written"] == "0" for row in rows), "M2 classification cannot write counts")
    require(
        all(row["numeric_benchmark_value_written"] == "0" for row in rows),
        "M2 classification cannot write benchmark values",
    )
    require(
        all(row["family_prediction_rows_written"] == "0" for row in rows),
        "M2 classification cannot write prediction rows",
    )
    require(
        all(row["per_galaxy_privilege_value_written"] == "0" for row in rows),
        "M2 classification cannot write privilege values",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M2 classification cannot allow scoring")
    require(
        all(row["next_required_artifact"] == "m2_benchmark_parameter_count_value_ledger_v12.csv" for row in rows),
        "M2 classification next artifact mismatch",
    )
    require(len(summary) == 1, "M2 classification summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M2_BENCHMARK_PARAMETER_COUNT_CLASSIFICATION_V11",
        "M2 classification summary id mismatch",
    )
    require(
        row["classification_artifact"] == "m2_benchmark_parameter_count_classification_v11",
        "M2 classification artifact mismatch",
    )
    require(
        row["inventory_status"] == "M2_BENCHMARK_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING",
        "M2 classification inventory status mismatch",
    )
    require(row["classification_rows"] == "12", "M2 classification row count mismatch")
    require(row["classified_rows"] == "12", "M2 classified row count mismatch")
    require(row["fixed_or_guard_classes"] == "4", "M2 fixed/guard summary mismatch")
    require(row["count_if_adjustable_classes"] == "8", "M2 count-if summary mismatch")
    require(row["disqualifying_classes"] == "0", "M2 disqualifying summary mismatch")
    require(row["numeric_count_values_written"] == "0", "M2 classification cannot write count values")
    require(row["numeric_benchmark_values_written"] == "0", "M2 classification cannot write benchmark values")
    require(row["family_prediction_rows_written"] == "0", "M2 classification cannot write prediction rows")
    require(row["per_galaxy_privilege_values_written"] == "0", "M2 classification cannot write privileges")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M2 classification cannot allow scoring")
    require(
        row["overall_status"] == "M2_BENCHMARK_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING",
        "M2 classification status mismatch",
    )
    require(
        row["next_required_artifact"] == "m2_benchmark_parameter_count_value_ledger_v12.csv",
        "M2 classification summary next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m2_benchmark_parameter_count_classification_only_no_counts_no_values_no_predictions_no_scores",
        "M2 classification claim boundary mismatch",
    )


def validate_m2_benchmark_parameter_count_value_ledger_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m2_benchmark_parameter_count_value_ledger_v12.csv")
    summary = read_csv(ROOT / "data/derived/m2_benchmark_parameter_count_value_ledger_summary_v12.csv")
    require(len(rows) == 12, "M2 benchmark parameter value ledger must cover twelve rows")
    require(
        [row["ledger_row_id"] for row in rows] == [f"M2BPCVL12_{index:03d}" for index in range(1, 13)],
        "M2 benchmark parameter value ledger ids mismatch",
    )
    require({row["readiness_id"] for row in rows} == {"NCR05_M2_GLOBAL"}, "M2 ledger readiness id mismatch")
    require({row["family_id"] for row in rows} == {"M2"}, "M2 ledger family id mismatch")
    require(sum(row["slot_count_value"] == "0" for row in rows) == 4, "M2 ledger zero row count mismatch")
    require(sum(row["resolution_needed"] == "true" for row in rows) == 8, "M2 ledger conditional row count mismatch")
    require(
        sum(row["slot_count_value"] == "VALUE_PENDING_BENCHMARK_SLOT_RESOLUTION" for row in rows) == 8,
        "M2 ledger pending slot value count mismatch",
    )
    require(
        all(row["final_m2_global_count_input_allowed"] == "false" for row in rows),
        "M2 ledger cannot allow final global count input",
    )
    require(
        all(row["benchmark_value_input_allowed"] == "false" for row in rows),
        "M2 ledger cannot allow benchmark values",
    )
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "M2 ledger cannot allow parsimony")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M2 ledger cannot allow scoring")
    require(len(summary) == 1, "M2 ledger summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M2_BENCHMARK_PARAMETER_COUNT_VALUE_LEDGER_V12", "M2 ledger summary id mismatch")
    require(row["ledger_artifact"] == "m2_benchmark_parameter_count_value_ledger_v12", "M2 ledger artifact mismatch")
    require(
        row["classification_status"] == "M2_BENCHMARK_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING",
        "M2 ledger classification status mismatch",
    )
    require(row["ledger_rows"] == "12", "M2 ledger row count mismatch")
    require(row["resolved_zero_rows"] == "4", "M2 ledger resolved-zero count mismatch")
    require(row["conditional_pending_rows"] == "8", "M2 ledger conditional count mismatch")
    require(row["numeric_slot_count_values_written"] == "4", "M2 ledger numeric slot count mismatch")
    require(row["final_m2_global_count_written"] == "false", "M2 ledger cannot write final M2 count")
    require(row["numeric_benchmark_values_written"] == "0", "M2 ledger cannot write benchmark values")
    require(row["family_prediction_rows_written"] == "0", "M2 ledger cannot write prediction rows")
    require(row["parsimony_scores_written"] == "0", "M2 ledger cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M2 ledger cannot allow scoring")
    require(
        row["overall_status"]
        == "M2_BENCHMARK_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
        "M2 ledger status mismatch",
    )
    require(
        row["next_required_artifact"] == "m2_benchmark_parameter_adjustable_slot_resolution_v13.csv",
        "M2 ledger next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m2_benchmark_parameter_count_value_ledger_only_no_final_k_no_values_no_predictions_no_scores",
        "M2 ledger claim boundary mismatch",
    )


def validate_m2_benchmark_parameter_adjustable_slot_resolution_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m2_benchmark_parameter_adjustable_slot_resolution_v13.csv")
    summary = read_csv(ROOT / "data/derived/m2_benchmark_parameter_adjustable_slot_resolution_summary_v13.csv")
    require(len(rows) == 8, "M2 adjustable-slot resolution must cover eight conditional rows")
    require(
        [row["resolution_row_id"] for row in rows] == [f"M2BPASR13_{index:03d}" for index in range(1, 9)],
        "M2 adjustable-slot resolution ids mismatch",
    )
    require({row["readiness_id"] for row in rows} == {"NCR05_M2_GLOBAL"}, "M2 adjustable readiness id mismatch")
    require({row["family_id"] for row in rows} == {"M2"}, "M2 adjustable family id mismatch")
    require(
        {row["prior_count_value_status"] for row in rows} == {"CONDITIONAL_COUNT_VALUE_PENDING"},
        "M2 adjustable rows must resolve conditional ledger rows",
    )
    require(
        {row["slot_resolution_status"] for row in rows}
        == {"RESOLVED_ZERO_NO_ACTIVE_BENCHMARK_SLOT_UNDER_CURRENT_SCAFFOLD"},
        "M2 adjustable resolution status mismatch",
    )
    require(all(row["slot_count_value"] == "0" for row in rows), "M2 adjustable rows must resolve to zero")
    require(
        all(row["adjustable_benchmark_parameter_found"] == "false" for row in rows),
        "M2 adjustable rows cannot find active benchmark parameters",
    )
    require(
        all(row["final_count_candidate_input_allowed"] == "true" for row in rows),
        "M2 adjustable rows must allow final-count candidate input",
    )
    require(
        all(row["benchmark_value_input_allowed"] == "false" for row in rows),
        "M2 adjustable rows cannot allow benchmark values",
    )
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "M2 adjustable rows cannot allow parsimony")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M2 adjustable rows cannot allow scoring")
    require(
        all(row["next_required_artifact"] == "m2_benchmark_parameter_final_count_candidate_v14.csv" for row in rows),
        "M2 adjustable rows next artifact mismatch",
    )
    require(len(summary) == 1, "M2 adjustable summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M2_BENCHMARK_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13",
        "M2 adjustable summary id mismatch",
    )
    require(
        row["resolution_artifact"] == "m2_benchmark_parameter_adjustable_slot_resolution_v13",
        "M2 adjustable artifact mismatch",
    )
    require(
        row["ledger_status"]
        == "M2_BENCHMARK_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
        "M2 adjustable ledger status mismatch",
    )
    require(row["conditional_rows_checked"] == "8", "M2 adjustable conditional count mismatch")
    require(row["resolved_zero_rows"] == "8", "M2 adjustable zero count mismatch")
    require(row["unresolved_rows"] == "0", "M2 adjustable unresolved count mismatch")
    require(row["adjustable_benchmark_parameters_found"] == "0", "M2 adjustable parameter count mismatch")
    require(row["final_m2_global_count_candidate_ready"] == "true", "M2 final count candidate readiness mismatch")
    require(row["final_m2_global_count_written"] == "false", "M2 adjustable cannot write final count")
    require(row["numeric_benchmark_values_written"] == "0", "M2 adjustable cannot write benchmark values")
    require(row["family_prediction_rows_written"] == "0", "M2 adjustable cannot write predictions")
    require(row["parsimony_scores_written"] == "0", "M2 adjustable cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M2 adjustable cannot allow scoring")
    require(
        row["overall_status"]
        == "M2_BENCHMARK_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE",
        "M2 adjustable status mismatch",
    )
    require(
        row["next_required_artifact"] == "m2_benchmark_parameter_final_count_candidate_v14.csv",
        "M2 adjustable next artifact mismatch",
    )
    require(
        row["claim_boundary"]
        == "m2_benchmark_parameter_adjustable_slot_resolution_only_no_final_k_no_values_no_predictions_no_scores",
        "M2 adjustable claim boundary mismatch",
    )


def validate_m2_benchmark_parameter_final_count_candidate_v14() -> None:
    rows = read_csv(ROOT / "data/derived/m2_benchmark_parameter_final_count_candidate_v14.csv")
    summary = read_csv(ROOT / "data/derived/m2_benchmark_parameter_final_count_candidate_summary_v14.csv")
    require(len(rows) == 1, "M2 final count candidate must have one row")
    row = rows[0]
    require(row["candidate_row_id"] == "M2BPFC14_001", "M2 final count candidate row id mismatch")
    require(row["family_id"] == "M2", "M2 final count candidate family mismatch")
    require(row["count_domain"] == "global_benchmark_parameters", "M2 final count candidate domain mismatch")
    require(row["slot_count_rows_used"] == "12", "M2 final count candidate must use twelve slot rows")
    require(row["resolved_zero_slot_rows"] == "12", "M2 final count candidate zero-row count mismatch")
    require(row["unresolved_slot_rows"] == "0", "M2 final count candidate cannot have unresolved rows")
    require(row["adjustable_benchmark_parameters_found"] == "0", "M2 final count candidate cannot find adjustable parameters")
    require(row["candidate_k_m2_global"] == "0", "M2 final count candidate value mismatch")
    require(
        row["candidate_status"] == "M2_BENCHMARK_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
        "M2 final count candidate status mismatch",
    )
    require(row["freeze_input_allowed"] == "true", "M2 final count candidate must allow freeze input")
    require(row["benchmark_value_input_allowed"] == "false", "M2 final count candidate cannot allow benchmark values")
    require(row["parsimony_input_allowed"] == "false", "M2 final count candidate cannot allow parsimony")
    require(row["endpoint_scoring_allowed"] == "false", "M2 final count candidate cannot allow scoring")
    require(
        row["next_required_artifact"] == "m2_benchmark_parameter_final_count_freeze_v15.csv",
        "M2 final count candidate next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m2_benchmark_parameter_final_count_candidate_only_no_freeze_no_values_no_predictions_no_scores",
        "M2 final count candidate claim boundary mismatch",
    )
    require(len(summary) == 1, "M2 final count candidate summary must have one row")
    summary_row = summary[0]
    require(
        summary_row["summary_id"] == "M2_BENCHMARK_PARAMETER_FINAL_COUNT_CANDIDATE_V14",
        "M2 final count candidate summary id mismatch",
    )
    require(
        summary_row["candidate_artifact"] == "m2_benchmark_parameter_final_count_candidate_v14",
        "M2 final count candidate artifact mismatch",
    )
    require(
        summary_row["v13_resolution_status"]
        == "M2_BENCHMARK_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE",
        "M2 final count candidate v13 status mismatch",
    )
    require(summary_row["slot_count_rows_used"] == "12", "M2 final count candidate summary row count mismatch")
    require(summary_row["resolved_zero_slot_rows"] == "12", "M2 final count candidate summary zero count mismatch")
    require(summary_row["unresolved_slot_rows"] == "0", "M2 final count candidate summary unresolved mismatch")
    require(summary_row["adjustable_benchmark_parameters_found"] == "0", "M2 final count candidate summary adjustable mismatch")
    require(summary_row["candidate_k_m2_global"] == "0", "M2 final count candidate summary value mismatch")
    require(summary_row["final_count_frozen"] == "false", "M2 final count candidate cannot freeze count")
    require(summary_row["numeric_benchmark_values_written"] == "0", "M2 final count candidate cannot write values")
    require(summary_row["family_prediction_rows_written"] == "0", "M2 final count candidate cannot write predictions")
    require(summary_row["parsimony_scores_written"] == "0", "M2 final count candidate cannot write parsimony")
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "M2 final count candidate cannot allow scoring")
    require(
        summary_row["overall_status"] == "M2_BENCHMARK_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
        "M2 final count candidate summary status mismatch",
    )
    require(
        summary_row["next_required_artifact"] == "m2_benchmark_parameter_final_count_freeze_v15.csv",
        "M2 final count candidate summary next artifact mismatch",
    )
    require(
        summary_row["claim_boundary"]
        == "m2_benchmark_parameter_final_count_candidate_only_no_freeze_no_values_no_predictions_no_scores",
        "M2 final count candidate summary claim boundary mismatch",
    )


def validate_m2_benchmark_parameter_final_count_freeze_v15() -> None:
    rows = read_csv(ROOT / "data/derived/m2_benchmark_parameter_final_count_freeze_v15.csv")
    summary = read_csv(ROOT / "data/derived/m2_benchmark_parameter_final_count_freeze_summary_v15.csv")
    require(len(rows) == 1, "M2 final count freeze must have one row")
    row = rows[0]
    require(row["freeze_row_id"] == "M2BPFCF15_001", "M2 final count freeze row id mismatch")
    require(row["candidate_row_id"] == "M2BPFC14_001", "M2 final count freeze candidate id mismatch")
    require(row["family_id"] == "M2", "M2 final count freeze family mismatch")
    require(row["count_domain"] == "global_benchmark_parameters", "M2 final count freeze domain mismatch")
    require(row["frozen_k_m2_global"] == "0", "M2 final count freeze value mismatch")
    require(
        row["freeze_status"]
        == "M2_BENCHMARK_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_BENCHMARK_PRIVILEGE_AUDIT_PENDING",
        "M2 final count freeze status mismatch",
    )
    require(
        row["candidate_status"] == "M2_BENCHMARK_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
        "M2 final count freeze candidate status mismatch",
    )
    require(row["per_galaxy_benchmark_privilege_input_allowed"] == "true", "M2 freeze must allow per-galaxy audit input")
    require(row["benchmark_value_input_allowed"] == "false", "M2 freeze cannot allow benchmark values")
    require(row["parsimony_input_allowed"] == "false", "M2 freeze cannot allow parsimony")
    require(row["endpoint_scoring_allowed"] == "false", "M2 freeze cannot allow scoring")
    require(
        row["next_required_artifact"] == "m2_per_galaxy_benchmark_privilege_count_audit_v10.csv",
        "M2 final count freeze next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m2_benchmark_parameter_final_count_freeze_only_no_benchmark_values_no_predictions_no_parsimony_no_scores",
        "M2 final count freeze claim boundary mismatch",
    )
    require(len(summary) == 1, "M2 final count freeze summary must have one row")
    summary_row = summary[0]
    require(summary_row["summary_id"] == "M2_BENCHMARK_PARAMETER_FINAL_COUNT_FREEZE_V15", "M2 freeze summary id mismatch")
    require(summary_row["freeze_artifact"] == "m2_benchmark_parameter_final_count_freeze_v15", "M2 freeze artifact mismatch")
    require(summary_row["frozen_k_m2_global"] == "0", "M2 freeze summary value mismatch")
    require(summary_row["final_count_frozen"] == "true", "M2 freeze summary must freeze count")
    require(summary_row["numeric_benchmark_values_written"] == "0", "M2 freeze cannot write values")
    require(
        summary_row["per_galaxy_benchmark_privilege_counts_written"] == "0",
        "M2 freeze cannot write per-galaxy counts",
    )
    require(summary_row["family_prediction_rows_written"] == "0", "M2 freeze cannot write predictions")
    require(summary_row["parsimony_scores_written"] == "0", "M2 freeze cannot write parsimony")
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "M2 freeze cannot allow scoring")
    require(
        summary_row["overall_status"]
        == "M2_BENCHMARK_PARAMETER_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_BENCHMARK_PRIVILEGE_AUDIT_PENDING",
        "M2 freeze summary status mismatch",
    )
    require(
        summary_row["next_required_artifact"] == "m2_per_galaxy_benchmark_privilege_count_audit_v10.csv",
        "M2 freeze summary next artifact mismatch",
    )
    require(
        summary_row["claim_boundary"]
        == "m2_benchmark_parameter_final_count_freeze_only_no_benchmark_values_no_predictions_no_parsimony_no_scores",
        "M2 freeze summary claim boundary mismatch",
    )


def validate_m2_per_galaxy_benchmark_privilege_count_audit_v10() -> None:
    rows = read_csv(ROOT / "data/derived/m2_per_galaxy_benchmark_privilege_count_audit_v10.csv")
    summary = read_csv(ROOT / "data/derived/m2_per_galaxy_benchmark_privilege_count_audit_summary_v10.csv")
    require(len(rows) == 18, "M2 per-galaxy benchmark audit must cover eighteen rows")
    require(
        [row["audit_row_id"] for row in rows] == [f"M2PGBMPCA10_{idx:03d}" for idx in range(1, 19)],
        "M2 per-galaxy benchmark audit row ids mismatch",
    )
    require(
        {row["row_benchmark_privilege_status"] for row in rows}
        == {"RESOLVED_ZERO_NO_ROW_SPECIFIC_M2_BENCHMARK_PRIVILEGE"},
        "M2 per-galaxy benchmark audit status mismatch",
    )
    require(
        all(row["per_galaxy_benchmark_privilege_count_value"] == "0" for row in rows),
        "M2 per-galaxy benchmark audit must write zero privilege values",
    )
    require(all(row["benchmark_value_input_allowed"] == "false" for row in rows), "M2 audit cannot allow values")
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "M2 audit cannot allow parsimony")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M2 audit cannot allow scoring")
    require(
        all(row["next_required_artifact"] == "m2_per_galaxy_benchmark_privilege_count_freeze_v11.csv" for row in rows),
        "M2 audit next artifact mismatch",
    )
    require(len(summary) == 1, "M2 per-galaxy benchmark audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_AUDIT_V10",
        "M2 per-galaxy benchmark audit summary id mismatch",
    )
    require(row["source_rows_checked"] == "18", "M2 audit summary row count mismatch")
    require(row["resolved_zero_rows"] == "18", "M2 audit summary zero row count mismatch")
    require(row["unresolved_rows"] == "0", "M2 audit summary unresolved mismatch")
    require(row["per_galaxy_benchmark_count_freeze_ready"] == "true", "M2 audit must be freeze-ready")
    require(row["per_galaxy_benchmark_count_frozen"] == "false", "M2 audit cannot freeze counts")
    require(row["numeric_benchmark_values_written"] == "0", "M2 audit cannot write benchmark values")
    require(row["parsimony_scores_written"] == "0", "M2 audit cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M2 audit cannot allow scoring")
    require(
        row["overall_status"] == "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE",
        "M2 audit summary status mismatch",
    )
    require(
        row["next_required_artifact"] == "m2_per_galaxy_benchmark_privilege_count_freeze_v11.csv",
        "M2 audit summary next artifact mismatch",
    )


def validate_m2_per_galaxy_benchmark_privilege_count_freeze_v11() -> None:
    rows = read_csv(ROOT / "data/derived/m2_per_galaxy_benchmark_privilege_count_freeze_v11.csv")
    summary = read_csv(ROOT / "data/derived/m2_per_galaxy_benchmark_privilege_count_freeze_summary_v11.csv")
    require(len(rows) == 18, "M2 per-galaxy benchmark freeze must cover eighteen rows")
    require(
        [row["freeze_row_id"] for row in rows] == [f"M2PGBMPCF11_{idx:03d}" for idx in range(1, 19)],
        "M2 per-galaxy benchmark freeze row ids mismatch",
    )
    require(
        {row["freeze_status"] for row in rows} == {"M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_FREEZE_V11_FROZEN"},
        "M2 per-galaxy benchmark freeze status mismatch",
    )
    require(
        {row["audit_status"] for row in rows} == {"RESOLVED_ZERO_NO_ROW_SPECIFIC_M2_BENCHMARK_PRIVILEGE"},
        "M2 per-galaxy benchmark freeze audit status mismatch",
    )
    require(
        all(row["frozen_per_galaxy_benchmark_privilege_count"] == "0" for row in rows),
        "M2 per-galaxy benchmark freeze must freeze zero values",
    )
    require(all(row["benchmark_value_input_allowed"] == "false" for row in rows), "M2 freeze cannot allow values")
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "M2 freeze cannot allow parsimony")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M2 freeze cannot allow scoring")
    require(
        all(row["next_required_artifact"] == "shared_input_count_discount_policy_v10.csv" for row in rows),
        "M2 per-galaxy benchmark freeze next artifact mismatch",
    )
    require(len(summary) == 1, "M2 per-galaxy benchmark freeze summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_FREEZE_V11",
        "M2 per-galaxy benchmark freeze summary id mismatch",
    )
    require(row["source_rows_checked"] == "18", "M2 freeze summary row count mismatch")
    require(row["frozen_zero_rows"] == "18", "M2 freeze summary zero row count mismatch")
    require(row["unresolved_rows"] == "0", "M2 freeze summary unresolved mismatch")
    require(row["per_galaxy_benchmark_count_frozen"] == "true", "M2 freeze summary must freeze count")
    require(row["frozen_per_galaxy_benchmark_privilege_count_total"] == "0", "M2 freeze total mismatch")
    require(row["numeric_benchmark_values_written"] == "0", "M2 freeze cannot write benchmark values")
    require(row["parsimony_scores_written"] == "0", "M2 freeze cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M2 freeze cannot allow scoring")
    require(
        row["overall_status"] == "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_FREEZE_V11_READY_SHARED_COUNT_PENDING",
        "M2 freeze summary status mismatch",
    )
    require(
        row["next_required_artifact"] == "shared_input_count_discount_policy_v10.csv",
        "M2 freeze summary next artifact mismatch",
    )


def validate_m2_benchmark_profile_table_v06() -> None:
    rows = read_csv(ROOT / "data/derived/m2_benchmark_profile_table_v06.csv")
    summary = read_csv(ROOT / "data/derived/m2_benchmark_profile_table_summary_v06.csv")
    require(len(rows) == 6, "M2 benchmark profile table must define six rows")
    require({row["family_id"] for row in rows} == {"M2"}, "M2 profile family mismatch")
    require({row["formula_slot"] for row in rows} == {"benchmark_profile_formula"}, "M2 profile slot mismatch")
    require(
        {row["profile_component"] for row in rows}
        == {
            "profile_family_registry",
            "halo_parameter_slots",
            "prior_policy",
            "nuisance_policy_link",
            "profile_switch_policy",
            "prediction_handoff",
        },
        "M2 profile components mismatch",
    )
    require(all(row["profile_table_status"] == "READY" for row in rows), "M2 profile rows must be ready")
    require(all(row["numeric_profile_values_written"] == "0" for row in rows), "M2 profile cannot write values")
    require(all(row["family_prediction_rows_written"] == "0" for row in rows), "M2 profile cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M2 profile cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M2 profile must forbid residual leakage")
    require(
        {row["next_required_artifact"] for row in rows} == {"m2_nuisance_policy_table_v06"},
        "M2 profile next artifact mismatch",
    )
    require(len(summary) == 1, "M2 profile summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M2_BENCHMARK_PROFILE_TABLE_V06", "M2 profile summary id mismatch")
    require(row["benchmark_profile_artifact"] == "m2_benchmark_profile_table_v06", "M2 profile artifact mismatch")
    require(row["family_id"] == "M2", "M2 profile summary family mismatch")
    require(row["formula_slot"] == "benchmark_profile_formula", "M2 profile summary slot mismatch")
    require(row["profile_components"] == "6", "M2 profile component count mismatch")
    require(row["numeric_profile_values_written"] == "0", "M2 profile summary cannot write values")
    require(row["family_prediction_rows_written"] == "0", "M2 profile summary cannot write predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M2 profile summary cannot allow scoring")
    require(
        row["overall_status"] == "M2_BENCHMARK_PROFILE_TABLE_READY_NUISANCE_BLOCKED",
        "M2 profile status mismatch",
    )
    require(row["next_required_artifact"] == "m2_nuisance_policy_table_v06", "M2 profile next artifact mismatch")
    require(
        row["claim_boundary"] == "m2_benchmark_profile_table_only_no_profile_values_no_predictions_no_scores_no_validation",
        "M2 profile claim boundary mismatch",
    )


def validate_m2_nuisance_policy_table_v06() -> None:
    rows = read_csv(ROOT / "data/derived/m2_nuisance_policy_table_v06.csv")
    summary = read_csv(ROOT / "data/derived/m2_nuisance_policy_table_summary_v06.csv")
    require(len(rows) == 6, "M2 nuisance policy table must define six rows")
    require({row["family_id"] for row in rows} == {"M2"}, "M2 nuisance family mismatch")
    require({row["formula_slot"] for row in rows} == {"benchmark_nuisance_policy"}, "M2 nuisance slot mismatch")
    require(
        {row["nuisance_component"] for row in rows}
        == {
            "stellar_mass_to_light_policy",
            "gas_scaling_policy",
            "uncertainty_policy",
            "nuisance_prior_policy",
            "shared_baryonic_fairness_policy",
            "prediction_handoff",
        },
        "M2 nuisance components mismatch",
    )
    require(all(row["nuisance_policy_status"] == "READY" for row in rows), "M2 nuisance rows must be ready")
    require(all(row["numeric_nuisance_values_written"] == "0" for row in rows), "M2 nuisance cannot write values")
    require(all(row["family_prediction_rows_written"] == "0" for row in rows), "M2 nuisance cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M2 nuisance cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "M2 nuisance must forbid residual leakage")
    require(
        {row["next_required_artifact"] for row in rows} == {"shared_scoring_input_table_v06"},
        "M2 nuisance next artifact mismatch",
    )
    require(len(summary) == 1, "M2 nuisance summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M2_NUISANCE_POLICY_TABLE_V06", "M2 nuisance summary id mismatch")
    require(row["nuisance_policy_artifact"] == "m2_nuisance_policy_table_v06", "M2 nuisance artifact mismatch")
    require(
        row["benchmark_profile_status"] == "M2_BENCHMARK_PROFILE_TABLE_READY_NUISANCE_BLOCKED",
        "M2 nuisance benchmark profile status mismatch",
    )
    require(row["family_id"] == "M2", "M2 nuisance summary family mismatch")
    require(row["formula_slot"] == "benchmark_nuisance_policy", "M2 nuisance summary slot mismatch")
    require(row["nuisance_components"] == "6", "M2 nuisance component count mismatch")
    require(row["numeric_nuisance_values_written"] == "0", "M2 nuisance summary cannot write values")
    require(row["family_prediction_rows_written"] == "0", "M2 nuisance summary cannot write predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M2 nuisance summary cannot allow scoring")
    require(
        row["overall_status"] == "M2_NUISANCE_POLICY_TABLE_READY_SHARED_INPUTS_BLOCKED",
        "M2 nuisance status mismatch",
    )
    require(row["next_required_artifact"] == "shared_scoring_input_table_v06", "M2 nuisance next artifact mismatch")
    require(
        row["claim_boundary"] == "m2_nuisance_policy_table_only_no_nuisance_values_no_predictions_no_scores_no_validation",
        "M2 nuisance claim boundary mismatch",
    )


def validate_shared_scoring_input_table_v06() -> None:
    rows = read_csv(ROOT / "data/derived/shared_scoring_input_table_v06.csv")
    summary = read_csv(ROOT / "data/derived/shared_scoring_input_table_summary_v06.csv")
    require(len(rows) == 6, "shared scoring input table must define six rows")
    require({row["family_scope"] for row in rows} == {"ALL"}, "shared input family scope mismatch")
    require({row["formula_slot"] for row in rows} == {"shared_scoring_inputs"}, "shared input slot mismatch")
    require(
        {row["input_component"] for row in rows}
        == {
            "data_loader_policy",
            "radial_grid_policy",
            "radial_mask_policy",
            "uncertainty_handling_policy",
            "baryonic_component_policy",
            "parameter_count_handoff",
        },
        "shared input components mismatch",
    )
    require(all(row["shared_input_status"] == "READY" for row in rows), "shared input rows must be ready")
    require(all(row["numeric_input_values_written"] == "0" for row in rows), "shared input cannot write values")
    require(all(row["family_prediction_rows_written"] == "0" for row in rows), "shared input cannot write predictions")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "shared input cannot allow scoring")
    require(all("endpoint_residual" in row["forbidden_inputs"] for row in rows), "shared input must forbid residual leakage")
    require(
        {row["next_required_artifact"] for row in rows} == {"numeric_parameter_count_table_v06"},
        "shared input next artifact mismatch",
    )
    require(len(summary) == 1, "shared input summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "SHARED_SCORING_INPUT_TABLE_V06", "shared input summary id mismatch")
    require(row["shared_input_artifact"] == "shared_scoring_input_table_v06", "shared input artifact mismatch")
    require(
        row["m2_nuisance_status"] == "M2_NUISANCE_POLICY_TABLE_READY_SHARED_INPUTS_BLOCKED",
        "shared input M2 nuisance status mismatch",
    )
    require(row["family_scope"] == "ALL", "shared input summary scope mismatch")
    require(row["formula_slot"] == "shared_scoring_inputs", "shared input summary slot mismatch")
    require(row["shared_input_components"] == "6", "shared input component count mismatch")
    require(row["numeric_input_values_written"] == "0", "shared input summary cannot write values")
    require(row["family_prediction_rows_written"] == "0", "shared input summary cannot write predictions")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "shared input summary cannot allow scoring")
    require(
        row["overall_status"] == "SHARED_SCORING_INPUT_TABLE_READY_PARAMETER_COUNTS_BLOCKED",
        "shared input status mismatch",
    )
    require(row["next_required_artifact"] == "numeric_parameter_count_table_v06", "shared input next artifact mismatch")
    require(
        row["claim_boundary"] == "shared_scoring_input_table_only_no_numeric_inputs_no_predictions_no_scores_no_validation",
        "shared input claim boundary mismatch",
    )


def validate_numeric_parameter_count_table_v06() -> None:
    rows = read_csv(ROOT / "data/derived/numeric_parameter_count_table_v06.csv")
    summary = read_csv(ROOT / "data/derived/numeric_parameter_count_table_summary_v06.csv")
    require(len(rows) == 8, "numeric parameter count table v06 must define eight count-rule rows")
    require({"M0", "M1", "M2", "ALL"}.issubset({row["family_id"] for row in rows}), "v06 count rows missing families")
    require(
        all(row["count_value_status"] == "FINAL_NUMERIC_COUNT_VALUE_BLOCKED_UNTIL_V08" for row in rows),
        "v06 count values must remain final-count blocked",
    )
    require(all(row["numeric_count_value"] == "VALUE_NOT_WRITTEN_IN_V06" for row in rows), "v06 cannot write final counts")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v06 count rows cannot allow scoring")
    require(all("family_winner" in row["forbidden_inputs"] for row in rows), "v06 count rows must forbid winner leakage")
    require(
        {row["next_required_artifact"] for row in rows} == {"numeric_parameter_count_table_v08.csv"},
        "v06 count next artifact mismatch",
    )
    require(len(summary) == 1, "v06 count summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "NUMERIC_PARAMETER_COUNT_TABLE_V06", "v06 count summary id mismatch")
    require(row["count_artifact"] == "numeric_parameter_count_table_v06", "v06 count artifact mismatch")
    require(
        row["shared_input_status"] == "SHARED_SCORING_INPUT_TABLE_READY_PARAMETER_COUNTS_BLOCKED",
        "v06 count shared input status mismatch",
    )
    require(row["count_rows"] == "8", "v06 count row count mismatch")
    require(row["numeric_count_values_written"] == "0", "v06 cannot write final count values")
    require(row["parsimony_scores_written"] == "0", "v06 cannot write parsimony scores")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v06 count summary cannot allow scoring")
    require(
        row["overall_status"] == "NUMERIC_PARAMETER_COUNT_TABLE_CONTRACT_READY_FINAL_COUNTS_BLOCKED",
        "v06 count status mismatch",
    )
    require(row["next_required_artifact"] == "numeric_parameter_count_table_v08.csv", "v06 count next artifact mismatch")
    require(
        row["claim_boundary"] == "numeric_parameter_count_table_contract_only_no_final_counts_no_parsimony_no_scores",
        "v06 count claim boundary mismatch",
    )


def validate_shared_input_count_discount_policy_v10() -> None:
    rows = read_csv(ROOT / "data/derived/shared_input_count_discount_policy_v10.csv")
    summary = read_csv(ROOT / "data/derived/shared_input_count_discount_policy_summary_v10.csv")
    require(len(rows) == 6, "shared input count-discount policy must cover six rows")
    require(
        [row["policy_row_id"] for row in rows] == [f"SICDP10_{idx:03d}" for idx in range(1, 7)],
        "shared input discount policy row ids mismatch",
    )
    require(
        {row["discount_policy_status"] for row in rows} == {"RESOLVED_ZERO_NO_SHARED_INPUT_COUNT_DISCOUNT"},
        "shared input discount policy status mismatch",
    )
    require(all(row["shared_discount_count_value"] == "0" for row in rows), "shared discount values must be zero")
    require(all(row["final_count_input_allowed"] == "true" for row in rows), "shared policy must allow final-count handoff")
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "shared policy cannot allow parsimony")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "shared policy cannot allow scoring")
    require(
        all(row["next_required_artifact"] == "numeric_parameter_count_table_final_values_v10.csv" for row in rows),
        "shared policy next artifact mismatch",
    )
    require(len(summary) == 1, "shared input discount policy summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10", "shared policy summary id mismatch")
    require(row["shared_input_rows_checked"] == "6", "shared policy row count mismatch")
    require(row["zero_discount_rows"] == "6", "shared policy zero row count mismatch")
    require(row["unresolved_rows"] == "0", "shared policy unresolved row mismatch")
    require(row["shared_discount_policy_frozen"] == "true", "shared policy must be frozen")
    require(row["shared_discount_count_total"] == "0", "shared policy total mismatch")
    require(row["final_numeric_count_values_written"] == "0", "shared policy cannot write final counts")
    require(row["parsimony_scores_written"] == "0", "shared policy cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "shared policy cannot allow scoring")
    require(
        row["overall_status"] == "SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10_READY_FINAL_NUMERIC_COUNTS_PENDING",
        "shared policy summary status mismatch",
    )
    require(
        row["next_required_artifact"] == "numeric_parameter_count_table_final_values_v10.csv",
        "shared policy summary next artifact mismatch",
    )


def validate_numeric_parameter_count_table_v08() -> None:
    rows = read_csv(ROOT / "data/derived/numeric_parameter_count_table_v08.csv")
    summary = read_csv(ROOT / "data/derived/numeric_parameter_count_table_summary_v08.csv")
    require(len(rows) == 7, "numeric parameter count table v08 must check seven readiness rows")
    require({"M0", "M1", "M2", "ALL"}.issubset({row["family_id"] for row in rows}), "v08 count rows missing families")
    require(all(row["readiness_status"] == "COUNT_NOT_READY" for row in rows), "v08 readiness rows must remain not ready")
    require(
        all(row["final_numeric_count_status"] == "FINAL_NUMERIC_COUNT_VALUE_PENDING_EXPLICIT_FINAL_VALUES" for row in rows),
        "v08 count values must wait for explicit final-value freeze",
    )
    require(
        all(row["numeric_parameter_count_value"] == "VALUE_PENDING_READINESS_CLOSURE" for row in rows),
        "v08 cannot write numeric count values",
    )
    require(
        all(row["per_galaxy_privilege_count_value"] == "VALUE_PENDING_READINESS_CLOSURE" for row in rows),
        "v08 cannot write per-galaxy privilege count values",
    )
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "v08 cannot allow parsimony input")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v08 cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"numeric_parameter_count_table_final_values_v10.csv"},
        "v08 next artifact mismatch",
    )
    require(len(summary) == 1, "v08 count summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "NUMERIC_PARAMETER_COUNT_TABLE_V08", "v08 count summary id mismatch")
    require(row["count_artifact"] == "numeric_parameter_count_table_v08", "v08 count artifact mismatch")
    require(
        row["source_contract_status"] == "NUMERIC_PARAMETER_COUNT_TABLE_CONTRACT_READY_FINAL_COUNTS_BLOCKED",
        "v08 source contract status mismatch",
    )
    require(row["readiness_rows_checked"] == "7", "v08 readiness row count mismatch")
    require(row["blocked_count_rows"] == "7", "v08 blocked count row mismatch")
    require(row["numeric_count_values_written"] == "0", "v08 cannot write final count values")
    require(row["per_galaxy_privilege_values_written"] == "0", "v08 cannot write privilege count values")
    require(row["parsimony_scores_written"] == "0", "v08 cannot write parsimony scores")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v08 count summary cannot allow scoring")
    require(
        row["overall_status"] == "NUMERIC_PARAMETER_COUNT_TABLE_V08_BLOCKED_ON_FINAL_NUMERIC_COUNT_VALUES",
        "v08 count status mismatch",
    )
    require(
        row["next_required_artifact"] == "numeric_parameter_count_table_final_values_v10.csv",
        "v08 count next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "numeric_parameter_count_table_v08_only_no_parsimony_no_scores_no_verdict",
        "v08 count claim boundary mismatch",
    )


def validate_numeric_parameter_count_table_final_values_v10() -> None:
    rows = read_csv(ROOT / "data/derived/numeric_parameter_count_table_final_values_v10.csv")
    summary = read_csv(ROOT / "data/derived/numeric_parameter_count_table_final_values_summary_v10.csv")
    require(len(rows) == 7, "v10 final count values must freeze seven rows")
    require(
        [row["final_count_row_id"] for row in rows] == [f"NPCFV10_{idx:03d}" for idx in range(1, 8)],
        "v10 final count row ids mismatch",
    )
    require({row["family_id"] for row in rows} == {"M0", "M1", "M2", "ALL"}, "v10 final count rows missing families")
    require(
        all(row["source_final_numeric_count_status"] == "FINAL_NUMERIC_COUNT_VALUE_PENDING_EXPLICIT_FINAL_VALUES" for row in rows),
        "v10 final count source status mismatch",
    )
    require(all(row["closure_decision"] == "COUNT_READINESS_READY" for row in rows), "v10 closure decisions must be ready")
    require(
        all(row["final_numeric_count_status"] == "FINAL_NUMERIC_COUNT_VALUE_FROZEN" for row in rows),
        "v10 final count values must be frozen",
    )
    require(all(row["numeric_parameter_count_value"] == "0" for row in rows), "v10 numeric count values must be zero")
    require(all(row["per_galaxy_privilege_count_value"] == "0" for row in rows), "v10 privilege count values must be zero")
    require(all(row["shared_discount_count_value"] == "0" for row in rows), "v10 shared discount values must be zero")
    require(all(row["final_parsimony_count_value"] == "0" for row in rows), "v10 parsimony count values must be zero")
    require(all(row["parsimony_input_allowed"] == "true" for row in rows), "v10 must hand count values to parsimony input")
    require(
        all(row["next_required_artifact"] == "control_runner_outputs_v08.csv" for row in rows),
        "v10 final count next artifact mismatch",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v10 final count rows cannot allow scoring")
    require(len(summary) == 1, "v10 final count summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "NUMERIC_PARAMETER_COUNT_TABLE_FINAL_VALUES_V10", "v10 final count summary id mismatch")
    require(row["final_values_artifact"] == "numeric_parameter_count_table_final_values_v10", "v10 final count artifact mismatch")
    require(row["v08_status"] == "NUMERIC_PARAMETER_COUNT_TABLE_V08_BLOCKED_ON_FINAL_NUMERIC_COUNT_VALUES", "v10 v08 status mismatch")
    require(row["closure_status"] == "NUMERIC_COUNT_READINESS_CLOSURE_READY_FOR_FINAL_COUNTS", "v10 closure status mismatch")
    require(
        row["shared_discount_status"] == "SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10_READY_FINAL_NUMERIC_COUNTS_PENDING",
        "v10 shared discount status mismatch",
    )
    require(row["final_count_rows"] == "7", "v10 final count row count mismatch")
    require(row["final_numeric_count_values_written"] == "7", "v10 final count written mismatch")
    require(row["per_galaxy_privilege_values_written"] == "3", "v10 privilege written mismatch")
    require(row["shared_discount_count_total"] == "0", "v10 shared discount total mismatch")
    require(row["final_parsimony_count_total"] == "0", "v10 parsimony count total mismatch")
    require(row["parsimony_scores_written"] == "0", "v10 must not write parsimony scores")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v10 cannot allow endpoint scoring")
    require(
        row["overall_status"] == "NUMERIC_PARAMETER_COUNT_TABLE_FINAL_VALUES_V10_READY_FOR_GLOBAL_SCORING_PREREQUISITES",
        "v10 final count status mismatch",
    )
    require(row["next_required_artifact"] == "control_runner_outputs_v08.csv", "v10 final count next artifact mismatch")
    require(
        row["claim_boundary"] == "numeric_parameter_count_table_final_values_only_no_parsimony_no_scores_no_verdict",
        "v10 final count claim boundary mismatch",
    )


def validate_control_runner_outputs_v08() -> None:
    rows = read_csv(ROOT / "data/derived/control_runner_outputs_v08.csv")
    summary = read_csv(ROOT / "data/derived/control_runner_outputs_summary_v08.csv")
    require(len(rows) == 6, "v08 control runner outputs must cover six runners")
    require(
        [row["control_output_id"] for row in rows] == [f"CRO08_{idx:03d}" for idx in range(1, 7)],
        "v08 control runner output row ids mismatch",
    )
    require(
        {row["output_contract_status"] for row in rows} == {"OUTPUT_CONTRACT_READY_NOT_RUN"},
        "v08 control output contract status mismatch",
    )
    require(
        all(row["source_execution_status"] == "RUNNER_CONTRACT_DECLARED_NOT_IMPLEMENTED" for row in rows),
        "v08 control output source status mismatch",
    )
    require(all(row["control_result_rows_written"] == "0" for row in rows), "v08 cannot write control result rows")
    require(all(row["control_scores_written"] == "0" for row in rows), "v08 cannot write control scores")
    require(all(row["control_pass_claim_allowed"] == "false" for row in rows), "v08 cannot allow control pass claims")
    require(
        all(row["next_required_artifact"] == "numeric_decision_thresholds_v08.csv" for row in rows),
        "v08 control output next artifact mismatch",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v08 cannot allow endpoint scoring")
    require(len(summary) == 1, "v08 control output summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "CONTROL_RUNNER_OUTPUTS_V08", "v08 control output summary id mismatch")
    require(row["control_output_artifact"] == "control_runner_outputs_v08", "v08 control output artifact mismatch")
    require(row["runner_contract_rows_checked"] == "6", "v08 control output runner count mismatch")
    require(row["output_contract_rows_written"] == "6", "v08 control output contract count mismatch")
    require(row["control_result_rows_written"] == "0", "v08 cannot write control result rows")
    require(row["control_scores_written"] == "0", "v08 cannot write control scores")
    require(row["control_pass_claim_allowed_anywhere"] == "false", "v08 cannot allow control pass claims")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v08 cannot allow endpoint scoring")
    require(
        row["overall_status"] == "CONTROL_RUNNER_OUTPUTS_V08_READY_FOR_DECISION_THRESHOLDS",
        "v08 control output status mismatch",
    )
    require(row["next_required_artifact"] == "numeric_decision_thresholds_v08.csv", "v08 control output next artifact mismatch")
    require(
        row["claim_boundary"] == "control_runner_outputs_v08_contract_only_no_control_results_no_scores_no_verdict",
        "v08 control output claim boundary mismatch",
    )


def validate_control_execution_readiness_v09() -> None:
    rows = read_csv(ROOT / "data/derived/control_execution_readiness_v09.csv")
    summary = read_csv(ROOT / "data/derived/control_execution_readiness_summary_v09.csv")
    require(len(rows) == 6, "v09 control execution readiness must cover six controls")
    require(
        {row["score_calculation_preflight_status"] for row in rows} == {"READY_FOR_SCORE_CALCULATION_PRECHECK"},
        "v09 controls must be ready for score-calculation preflight",
    )
    require(
        {row["verdict_control_status"] for row in rows} == {"BLOCKED_NOT_EXECUTED_NO_PASS_CLAIM"},
        "v09 controls must block verdict readiness",
    )
    require({row["control_result_rows_written"] for row in rows} == {"0"}, "v09 cannot write control result rows")
    require({row["control_scores_written"] for row in rows} == {"0"}, "v09 cannot write control scores")
    require(all(row["control_pass_claim_allowed"] == "false" for row in rows), "v09 cannot allow control pass claims")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v09 cannot allow endpoint scoring")
    require(all(row["dark_sector_verdict_allowed"] == "false" for row in rows), "v09 cannot allow verdicts")
    require(len(summary) == 1, "v09 control execution summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "CONTROL_EXECUTION_READINESS_V09", "v09 control readiness summary id mismatch")
    require(row["controls_checked"] == "6", "v09 must check six controls")
    require(row["score_calculation_ready_controls"] == "6", "v09 must ready six controls for score calculation")
    require(row["verdict_ready_controls"] == "0", "v09 must ready zero controls for verdicts")
    require(row["control_result_rows_written"] == "0", "v09 summary cannot write control result rows")
    require(row["control_scores_written"] == "0", "v09 summary cannot write control scores")
    require(row["control_pass_claim_allowed_anywhere"] == "false", "v09 summary cannot allow control pass")
    require(row["score_calculation_preflight_ready"] == "true", "v09 score-calculation preflight must be ready")
    require(row["family_verdict_controls_ready"] == "false", "v09 family verdict controls must remain blocked")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v09 summary cannot allow endpoint scoring")
    require(row["dark_sector_verdict_allowed_anywhere"] == "false", "v09 summary cannot allow verdicts")
    require(
        row["overall_status"] == "CONTROL_EXECUTION_READINESS_SCORE_CALCULATION_READY_VERDICT_CONTROLS_BLOCKED",
        "v09 control readiness status mismatch",
    )
    require(row["next_required_artifact"] == "endpoint_scoring_runner_v01", "v09 next artifact mismatch")


def validate_endpoint_scoring_runner_v01() -> None:
    rows = read_csv(ROOT / "data/derived/endpoint_scoring_runner_v01.csv")
    summary = read_csv(ROOT / "data/derived/endpoint_scoring_runner_summary_v01.csv")
    require(len(rows) == 18, "v01 endpoint scoring runner must write eighteen raw diagnostic rows")
    require({row["family_id"] for row in rows} == {"M0"}, "v01 runner must be M0-only")
    require(
        {row["raw_score_status"] for row in rows} == {"RAW_M0_ADEQUACY_DIAGNOSTIC_WRITTEN_NOT_VERDICT"},
        "v01 runner must write raw diagnostics only",
    )
    require(
        sum(int(row["radial_points_scored"]) for row in rows) == 450,
        "v01 runner must score 450 radial points",
    )
    for row in rows:
        full = float(row["chi2_full_raw"])
        inner = float(row["chi2_inner_raw"])
        outer = float(row["chi2_outer_raw"])
        penalty = float(row["parsimony_penalty_raw"])
        raw_score = float(row["raw_m0_adequacy_diagnostic"])
        require(abs(raw_score - (full + 0.5 * inner + 0.5 * outer + penalty)) < 0.000002, "v01 score formula mismatch")
        require(row["family_comparison_allowed"] == "false", "v01 cannot allow family comparison")
        require(row["control_pass_claim_allowed"] == "false", "v01 cannot allow control pass claims")
        require(row["endpoint_scoring_allowed"] == "false", "v01 cannot allow endpoint scoring")
        require(row["dark_sector_verdict_allowed"] == "false", "v01 cannot allow dark-sector verdicts")
    require(len(summary) == 1, "v01 runner summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "ENDPOINT_SCORING_RUNNER_V01", "v01 runner summary id mismatch")
    require(row["scoring_mode"] == "RAW_M0_ADEQUACY_DIAGNOSTIC_ONLY", "v01 scoring mode mismatch")
    require(row["raw_diagnostic_rows_written"] == "18", "v01 summary row count mismatch")
    require(row["radial_points_scored"] == "450", "v01 summary radial count mismatch")
    require(row["families_scored"] == "1", "v01 summary family count mismatch")
    require(row["family_comparison_rows_written"] == "0", "v01 cannot write family comparison rows")
    require(row["control_result_rows_written"] == "0", "v01 cannot write control result rows")
    require(row["endpoint_verdict_scores_written"] == "0", "v01 cannot write endpoint verdict scores")
    require(row["family_comparison_allowed_anywhere"] == "false", "v01 summary cannot allow family comparison")
    require(row["control_pass_claim_allowed_anywhere"] == "false", "v01 summary cannot allow control pass")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v01 summary cannot allow endpoint scoring")
    require(row["dark_sector_verdict_allowed_anywhere"] == "false", "v01 summary cannot allow verdicts")
    require(
        row["overall_status"] == "ENDPOINT_SCORING_RUNNER_V01_RAW_M0_ADEQUACY_DIAGNOSTICS_WRITTEN_VERDICT_BLOCKED",
        "v01 runner status mismatch",
    )
    require(row["next_required_artifact"] == "control_result_execution_v01.csv", "v01 next artifact mismatch")


def validate_family_prediction_comparability_v09() -> None:
    rows = read_csv(ROOT / "data/derived/family_prediction_comparability_v09.csv")
    summary = read_csv(ROOT / "data/derived/family_prediction_comparability_summary_v09.csv")
    require([row["family_id"] for row in rows] == ["M0", "M1", "M2"], "v09 comparability family order mismatch")
    require(
        {row["family_id"]: row["numeric_prediction_rows_written"] for row in rows}
        == {"M0": "450", "M1": "0", "M2": "0"},
        "v09 comparability prediction row counts mismatch",
    )
    require(rows[0]["allowed_scoring_mode"] == "M0_ADEQUACY_DIAGNOSTIC_ONLY", "v09 M0 adequacy mode mismatch")
    require(rows[0]["blocked_scoring_mode"] == "M0_M1_M2_FAMILY_COMPARISON", "v09 M0 blocked mode mismatch")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v09 cannot allow endpoint scoring")
    require(all(row["dark_sector_verdict_allowed"] == "false" for row in rows), "v09 cannot allow verdicts")
    require(len(summary) == 1, "v09 comparability summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "FAMILY_PREDICTION_COMPARABILITY_V09", "v09 comparability summary id mismatch")
    require(row["families_checked"] == "3", "v09 must check three families")
    require(row["families_with_numeric_predictions"] == "1", "v09 must report one family with predictions")
    require(row["families_without_numeric_predictions"] == "2", "v09 must report two families without predictions")
    require(row["m0_adequacy_scoring_basis_available"] == "true", "v09 M0 adequacy basis mismatch")
    require(row["family_comparison_scoring_allowed"] == "false", "v09 family comparison must remain blocked")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v09 summary cannot allow scoring")
    require(row["dark_sector_verdict_allowed_anywhere"] == "false", "v09 summary cannot allow verdicts")
    require(
        row["overall_status"] == "FAMILY_PREDICTION_COMPARABILITY_M0_ONLY_FAMILY_COMPARISON_BLOCKED",
        "v09 comparability status mismatch",
    )
    require(row["next_required_artifact"] == "control_runner_outputs_v08.csv", "v09 next artifact mismatch")


def validate_numeric_decision_thresholds_v08() -> None:
    rows = read_csv(ROOT / "data/derived/numeric_decision_thresholds_v08.csv")
    summary = read_csv(ROOT / "data/derived/numeric_decision_thresholds_summary_v08.csv")
    require(len(rows) == 4, "v08 numeric decision thresholds must cover four verdict labels")
    require(
        [row["numeric_threshold_id"] for row in rows] == [f"NDT08_{idx:03d}" for idx in range(1, 5)],
        "v08 numeric decision threshold ids mismatch",
    )
    require(
        {row["verdict_label"] for row in rows} == {"M0_SUFFICIENT", "M1_FAVORED", "M2_BENCHMARK_STRONGER", "UNRESOLVED"},
        "v08 numeric decision threshold labels mismatch",
    )
    require(
        {row["numeric_threshold_status"] for row in rows} == {"NUMERIC_THRESHOLD_FROZEN_NOT_EVALUATED"},
        "v08 numeric decision threshold status mismatch",
    )
    require({row["minimum_heldout_margin"] for row in rows} == {"0"}, "v08 minimum heldout margin mismatch")
    require({row["maximum_control_failures"] for row in rows} == {"0"}, "v08 maximum control failures mismatch")
    require(all(row["stability_required"] == "true" for row in rows), "v08 thresholds must require stability")
    require(
        {row["rank_required"] for row in rows if row["verdict_label"] != "UNRESOLVED"} == {"1"},
        "v08 non-unresolved rank requirement mismatch",
    )
    require(
        [row["rank_required"] for row in rows if row["verdict_label"] == "UNRESOLVED"] == ["0"],
        "v08 unresolved rank requirement mismatch",
    )
    require(
        [row["unresolved_fallback_allowed"] for row in rows if row["verdict_label"] == "UNRESOLVED"] == ["true"],
        "v08 unresolved fallback mismatch",
    )
    require(
        all(row["next_required_artifact"] == "scoring_preflight_v07.csv" for row in rows),
        "v08 numeric decision thresholds must point to scoring preflight",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v08 thresholds cannot allow endpoint scoring")
    require(len(summary) == 1, "v08 numeric decision threshold summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "NUMERIC_DECISION_THRESHOLDS_V08", "v08 numeric threshold summary id mismatch")
    require(row["source_threshold_rows_checked"] == "4", "v08 source threshold row count mismatch")
    require(row["numeric_threshold_rows_written"] == "4", "v08 numeric threshold row count mismatch")
    require(row["endpoint_scores_written"] == "0", "v08 cannot write endpoint scores")
    require(row["verdicts_written"] == "0", "v08 cannot write verdicts")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v08 cannot allow endpoint scoring")
    require(
        row["overall_status"] == "NUMERIC_DECISION_THRESHOLDS_V08_READY_FOR_SCORING_PREFLIGHT",
        "v08 numeric threshold status mismatch",
    )
    require(row["next_required_artifact"] == "scoring_preflight_v07.csv", "v08 numeric threshold next artifact mismatch")
    require(
        row["claim_boundary"] == "numeric_decision_thresholds_v08_threshold_freeze_only_no_scores_no_verdict",
        "v08 numeric threshold claim boundary mismatch",
    )


def validate_m0_global_parameter_inventory_v10() -> None:
    rows = read_csv(ROOT / "data/derived/m0_global_parameter_inventory_v10.csv")
    summary = read_csv(ROOT / "data/derived/m0_global_parameter_inventory_summary_v10.csv")
    require(len(rows) == 6, "M0 v10 global inventory must expose six slots")
    require(
        [row["inventory_row_id"] for row in rows] == [f"M0GPI10_{index:03d}" for index in range(1, 7)],
        "M0 v10 inventory row ids mismatch",
    )
    require({row["readiness_id"] for row in rows} == {"NCR05_M0_GLOBAL"}, "M0 v10 readiness id mismatch")
    require({row["family_id"] for row in rows} == {"M0"}, "M0 v10 family mismatch")
    require({row["inventory_scope"] for row in rows} == {"global_formula_parameters"}, "M0 v10 scope mismatch")
    require(
        {row["countability_status"] for row in rows} == {"COUNTABILITY_CLASSIFICATION_PENDING"},
        "M0 v10 must leave countability pending",
    )
    require(all(row["count_value_written"] == "0" for row in rows), "M0 v10 cannot write count values")
    require(all(row["numeric_value_written"] == "0" for row in rows), "M0 v10 cannot write numeric values")
    require(
        all(row["per_galaxy_privilege_written"] == "0" for row in rows),
        "M0 v10 cannot write per-galaxy privilege values",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v10 cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_global_parameter_count_classification_v11.csv"},
        "M0 v10 next artifact mismatch",
    )
    require("readout_operator" in {row["global_slot_name"] for row in rows}, "M0 v10 missing readout operator slot")
    require("no_dark_constraint" in {row["global_slot_name"] for row in rows}, "M0 v10 missing no-dark slot")
    require(len(summary) == 1, "M0 v10 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_GLOBAL_PARAMETER_INVENTORY_V10", "M0 v10 summary id mismatch")
    require(row["inventory_artifact"] == "m0_global_parameter_inventory_v10", "M0 v10 artifact mismatch")
    require(row["readiness_id"] == "NCR05_M0_GLOBAL", "M0 v10 summary readiness mismatch")
    require(row["family_id"] == "M0", "M0 v10 summary family mismatch")
    require(row["inventory_rows"] == "6", "M0 v10 must summarize six rows")
    require(row["inventory_rows_present"] == "6", "M0 v10 must present six rows")
    require(row["countability_classified_rows"] == "0", "M0 v10 cannot classify countability")
    require(row["numeric_count_values_written"] == "0", "M0 v10 cannot write numeric counts")
    require(row["numeric_values_written"] == "0", "M0 v10 cannot write numeric values")
    require(row["per_galaxy_privilege_values_written"] == "0", "M0 v10 cannot write privilege values")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v10 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_GLOBAL_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING",
        "M0 v10 status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_global_parameter_count_classification_v11.csv",
        "M0 v10 summary next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m0_global_parameter_inventory_only_no_counts_no_values_no_scores",
        "M0 v10 claim boundary mismatch",
    )


def validate_m0_global_parameter_count_classification_v11() -> None:
    rows = read_csv(ROOT / "data/derived/m0_global_parameter_count_classification_v11.csv")
    summary = read_csv(ROOT / "data/derived/m0_global_parameter_count_classification_summary_v11.csv")
    require(len(rows) == 6, "M0 v11 countability classification must expose six rows")
    require(
        [row["classification_row_id"] for row in rows] == [f"M0GPCC11_{index:03d}" for index in range(1, 7)],
        "M0 v11 classification row ids mismatch",
    )
    require({row["readiness_id"] for row in rows} == {"NCR05_M0_GLOBAL"}, "M0 v11 readiness id mismatch")
    require({row["family_id"] for row in rows} == {"M0"}, "M0 v11 family mismatch")
    require(
        {row["classification_status"] for row in rows} == {"CLASSIFIED_COUNT_VALUE_PENDING"},
        "M0 v11 rows must remain count-value pending",
    )
    require(all(row["numeric_count_value_written"] == "0" for row in rows), "M0 v11 cannot write count values")
    require(all(row["numeric_value_written"] == "0" for row in rows), "M0 v11 cannot write numeric values")
    require(
        all(row["per_galaxy_privilege_value_written"] == "0" for row in rows),
        "M0 v11 cannot write per-galaxy privilege values",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v11 cannot allow scoring")
    require(
        {row["next_required_artifact"] for row in rows} == {"m0_global_parameter_count_value_ledger_v12.csv"},
        "M0 v11 next artifact mismatch",
    )
    classes = {row["global_slot_name"]: row["countability_class"] for row in rows}
    require(
        classes["no_dark_constraint"] == "FIXED_FAMILY_GUARD_DISQUALIFIES_IF_COMPENSATOR",
        "M0 v11 no-dark guard class mismatch",
    )
    require(
        classes["readout_operator"] == "COUNT_IF_ADJUSTABLE_READOUT_OPERATOR_PARAMETER",
        "M0 v11 readout operator class mismatch",
    )
    require(
        classes["assembly"] == "AGGREGATE_AUDIT_ROW_CHILD_SLOTS_COUNT",
        "M0 v11 assembly class mismatch",
    )
    require(len(summary) == 1, "M0 v11 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_GLOBAL_PARAMETER_COUNT_CLASSIFICATION_V11", "M0 v11 summary id mismatch")
    require(
        row["classification_artifact"] == "m0_global_parameter_count_classification_v11",
        "M0 v11 artifact mismatch",
    )
    require(
        row["inventory_status"] == "M0_GLOBAL_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING",
        "M0 v11 must inherit ready v10 inventory",
    )
    require(row["classification_rows"] == "6", "M0 v11 must summarize six rows")
    require(row["classified_rows"] == "6", "M0 v11 must classify six rows")
    require(row["fixed_or_neutral_classes"] == "1", "M0 v11 fixed class count mismatch")
    require(row["count_if_adjustable_classes"] == "4", "M0 v11 count-if class count mismatch")
    require(row["disqualifying_classes"] == "1", "M0 v11 disqualifying class count mismatch")
    require(row["numeric_count_values_written"] == "0", "M0 v11 cannot write numeric counts")
    require(row["numeric_values_written"] == "0", "M0 v11 cannot write numeric values")
    require(row["per_galaxy_privilege_values_written"] == "0", "M0 v11 cannot write privilege values")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v11 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_GLOBAL_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING",
        "M0 v11 status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_global_parameter_count_value_ledger_v12.csv",
        "M0 v11 summary next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m0_global_parameter_count_classification_only_no_numeric_counts_no_scores",
        "M0 v11 claim boundary mismatch",
    )


def validate_m0_global_parameter_count_value_ledger_v12() -> None:
    rows = read_csv(ROOT / "data/derived/m0_global_parameter_count_value_ledger_v12.csv")
    summary = read_csv(ROOT / "data/derived/m0_global_parameter_count_value_ledger_summary_v12.csv")
    require(len(rows) == 6, "M0 v12 count value ledger must expose six rows")
    require(
        [row["ledger_row_id"] for row in rows] == [f"M0GPCVL12_{index:03d}" for index in range(1, 7)],
        "M0 v12 ledger row ids mismatch",
    )
    require({row["readiness_id"] for row in rows} == {"NCR05_M0_GLOBAL"}, "M0 v12 readiness id mismatch")
    require({row["family_id"] for row in rows} == {"M0"}, "M0 v12 family mismatch")
    require(sum(row["slot_count_value"] == "0" for row in rows) == 2, "M0 v12 must resolve two zero slot values")
    require(sum(row["resolution_needed"] == "true" for row in rows) == 4, "M0 v12 must leave four conditional rows")
    require(
        all(row["final_m0_global_count_input_allowed"] == "false" for row in rows),
        "M0 v12 cannot allow final M0 global count input",
    )
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "M0 v12 cannot allow parsimony")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v12 cannot allow scoring")
    values = {row["global_slot_name"]: row["slot_count_value"] for row in rows}
    require(values["no_dark_constraint"] == "0", "M0 v12 no-dark guard must have zero slot value")
    require(values["assembly"] == "0", "M0 v12 assembly row must have zero direct slot value")
    require(
        values["readout_operator"] == "VALUE_PENDING_ADJUSTABLE_SLOT_RESOLUTION",
        "M0 v12 readout operator must remain resolution-pending",
    )
    require(len(summary) == 1, "M0 v12 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_GLOBAL_PARAMETER_COUNT_VALUE_LEDGER_V12", "M0 v12 summary id mismatch")
    require(row["ledger_artifact"] == "m0_global_parameter_count_value_ledger_v12", "M0 v12 artifact mismatch")
    require(
        row["classification_status"] == "M0_GLOBAL_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING",
        "M0 v12 must inherit ready v11 classification",
    )
    require(row["ledger_rows"] == "6", "M0 v12 must summarize six rows")
    require(row["resolved_zero_rows"] == "2", "M0 v12 resolved zero count mismatch")
    require(row["conditional_pending_rows"] == "4", "M0 v12 conditional pending count mismatch")
    require(row["disqualifying_guard_rows"] == "1", "M0 v12 disqualifying guard count mismatch")
    require(row["numeric_slot_count_values_written"] == "2", "M0 v12 numeric slot value count mismatch")
    require(row["final_m0_global_count_written"] == "false", "M0 v12 cannot write final M0 count")
    require(row["parsimony_scores_written"] == "0", "M0 v12 cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v12 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_GLOBAL_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
        "M0 v12 status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_global_adjustable_slot_resolution_v13.csv",
        "M0 v12 next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m0_global_parameter_count_value_ledger_only_no_final_k_no_parsimony_no_scores",
        "M0 v12 claim boundary mismatch",
    )


def validate_m0_global_adjustable_slot_resolution_v13() -> None:
    rows = read_csv(ROOT / "data/derived/m0_global_adjustable_slot_resolution_v13.csv")
    summary = read_csv(ROOT / "data/derived/m0_global_adjustable_slot_resolution_summary_v13.csv")
    require(len(rows) == 4, "M0 v13 adjustable-slot resolution must check four rows")
    require(
        [row["resolution_row_id"] for row in rows] == [f"M0GASR13_{index:03d}" for index in range(1, 5)],
        "M0 v13 resolution row ids mismatch",
    )
    require(
        {row["global_slot_name"] for row in rows}
        == {"source_state", "baryonic_input", "readout_operator", "failure_route"},
        "M0 v13 must resolve the four conditional v12 slots",
    )
    require(
        all(row["prior_count_value_status"] == "CONDITIONAL_COUNT_VALUE_PENDING" for row in rows),
        "M0 v13 rows must inherit conditional pending status",
    )
    require(
        all(row["slot_resolution_status"] == "RESOLVED_ZERO_FIXED_SOURCE_SIDE_OR_GUARD" for row in rows),
        "M0 v13 rows must resolve as source-side or guard zero slots",
    )
    require(all(row["slot_count_value"] == "0" for row in rows), "M0 v13 rows must resolve to zero")
    require(all(row["adjustable_privilege_found"] == "false" for row in rows), "M0 v13 cannot find adjustable privileges")
    require(
        all(row["final_count_candidate_input_allowed"] == "true" for row in rows),
        "M0 v13 must allow final-count-candidate input",
    )
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "M0 v13 cannot allow parsimony")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v13 cannot allow scoring")
    require(
        any("M0NDRE08_PARAMETERS" in row["resolution_evidence"] for row in rows),
        "M0 v13 must cite readout parameter evidence",
    )
    require(
        any("M0NDFP07_FAILURE_REPORTING_ROUTE" in row["resolution_evidence"] for row in rows),
        "M0 v13 must cite fallback failure-route evidence",
    )
    require(len(summary) == 1, "M0 v13 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION_V13", "M0 v13 summary id mismatch")
    require(row["resolution_artifact"] == "m0_global_adjustable_slot_resolution_v13", "M0 v13 artifact mismatch")
    require(
        row["ledger_status"] == "M0_GLOBAL_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
        "M0 v13 must inherit v12 ledger status",
    )
    require(row["conditional_rows_checked"] == "4", "M0 v13 checked row count mismatch")
    require(row["resolved_zero_rows"] == "4", "M0 v13 resolved zero count mismatch")
    require(row["unresolved_rows"] == "0", "M0 v13 unresolved row count mismatch")
    require(row["adjustable_privileges_found"] == "0", "M0 v13 adjustable privilege count mismatch")
    require(row["final_m0_global_count_candidate_ready"] == "true", "M0 v13 must ready final-count candidate")
    require(row["final_m0_global_count_written"] == "false", "M0 v13 cannot write final M0 count")
    require(row["parsimony_scores_written"] == "0", "M0 v13 cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v13 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE",
        "M0 v13 status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_global_final_count_candidate_v14.csv",
        "M0 v13 next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m0_global_adjustable_slot_resolution_only_no_final_k_no_parsimony_no_scores",
        "M0 v13 claim boundary mismatch",
    )


def validate_m0_global_final_count_candidate_v14() -> None:
    rows = read_csv(ROOT / "data/derived/m0_global_final_count_candidate_v14.csv")
    summary = read_csv(ROOT / "data/derived/m0_global_final_count_candidate_summary_v14.csv")
    require(len(rows) == 1, "M0 v14 final-count candidate must have one row")
    row = rows[0]
    require(row["candidate_row_id"] == "M0GFC14_001", "M0 v14 candidate row id mismatch")
    require(row["family_id"] == "M0", "M0 v14 family mismatch")
    require(row["count_domain"] == "global_formula_parameters", "M0 v14 count domain mismatch")
    require(row["slot_count_rows_used"] == "6", "M0 v14 must use six slot count rows")
    require(row["resolved_zero_slot_rows"] == "6", "M0 v14 must resolve six zero rows")
    require(row["unresolved_slot_rows"] == "0", "M0 v14 unresolved row count mismatch")
    require(row["adjustable_privileges_found"] == "0", "M0 v14 adjustable privilege count mismatch")
    require(row["candidate_k_m0_global"] == "0", "M0 v14 candidate count mismatch")
    require(
        row["candidate_status"] == "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
        "M0 v14 candidate status mismatch",
    )
    require(row["freeze_input_allowed"] == "true", "M0 v14 must allow freeze input")
    require(row["parsimony_input_allowed"] == "false", "M0 v14 cannot allow parsimony")
    require(row["endpoint_scoring_allowed"] == "false", "M0 v14 cannot allow scoring")
    require(
        row["next_required_artifact"] == "m0_global_final_count_freeze_v15.csv",
        "M0 v14 next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m0_global_final_count_candidate_only_no_freeze_no_parsimony_no_scores",
        "M0 v14 claim boundary mismatch",
    )
    require(len(summary) == 1, "M0 v14 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14", "M0 v14 summary id mismatch")
    require(row["candidate_artifact"] == "m0_global_final_count_candidate_v14", "M0 v14 artifact mismatch")
    require(
        row["v12_ledger_status"] == "M0_GLOBAL_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING",
        "M0 v14 v12 status mismatch",
    )
    require(
        row["v13_resolution_status"] == "M0_GLOBAL_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE",
        "M0 v14 v13 status mismatch",
    )
    require(row["slot_count_rows_used"] == "6", "M0 v14 summary slot count mismatch")
    require(row["resolved_zero_slot_rows"] == "6", "M0 v14 summary zero rows mismatch")
    require(row["unresolved_slot_rows"] == "0", "M0 v14 summary unresolved rows mismatch")
    require(row["adjustable_privileges_found"] == "0", "M0 v14 summary adjustable count mismatch")
    require(row["candidate_k_m0_global"] == "0", "M0 v14 summary candidate count mismatch")
    require(row["final_count_frozen"] == "false", "M0 v14 cannot freeze final count")
    require(row["parsimony_scores_written"] == "0", "M0 v14 cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v14 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
        "M0 v14 summary status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_global_final_count_freeze_v15.csv",
        "M0 v14 summary next artifact mismatch",
    )


def validate_m0_global_final_count_freeze_v15() -> None:
    rows = read_csv(ROOT / "data/derived/m0_global_final_count_freeze_v15.csv")
    summary = read_csv(ROOT / "data/derived/m0_global_final_count_freeze_summary_v15.csv")
    require(len(rows) == 1, "M0 v15 final-count freeze must have one row")
    row = rows[0]
    require(row["freeze_row_id"] == "M0GFCF15_001", "M0 v15 freeze row id mismatch")
    require(row["candidate_row_id"] == "M0GFC14_001", "M0 v15 candidate row id mismatch")
    require(row["family_id"] == "M0", "M0 v15 family mismatch")
    require(row["count_domain"] == "global_formula_parameters", "M0 v15 count domain mismatch")
    require(row["frozen_k_m0_global"] == "0", "M0 v15 frozen count mismatch")
    require(
        row["freeze_status"] == "M0_GLOBAL_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_PRIVILEGE_AUDIT_PENDING",
        "M0 v15 freeze status mismatch",
    )
    require(
        row["candidate_status"] == "M0_GLOBAL_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE",
        "M0 v15 candidate status mismatch",
    )
    require(row["per_galaxy_count_input_allowed"] == "true", "M0 v15 must allow per-galaxy audit input")
    require(row["parsimony_input_allowed"] == "false", "M0 v15 cannot allow parsimony")
    require(row["endpoint_scoring_allowed"] == "false", "M0 v15 cannot allow scoring")
    require(
        row["next_required_artifact"] == "m0_per_galaxy_privilege_count_audit_v10.csv",
        "M0 v15 next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m0_global_final_count_freeze_only_no_per_galaxy_counts_no_parsimony_no_scores",
        "M0 v15 claim boundary mismatch",
    )
    require(len(summary) == 1, "M0 v15 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_GLOBAL_FINAL_COUNT_FREEZE_V15", "M0 v15 summary id mismatch")
    require(row["freeze_artifact"] == "m0_global_final_count_freeze_v15", "M0 v15 artifact mismatch")
    require(row["frozen_k_m0_global"] == "0", "M0 v15 summary frozen count mismatch")
    require(row["final_count_frozen"] == "true", "M0 v15 must freeze the global count")
    require(row["per_galaxy_counts_written"] == "0", "M0 v15 cannot write per-galaxy counts")
    require(row["parsimony_scores_written"] == "0", "M0 v15 cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v15 summary cannot allow scoring")
    require(
        row["overall_status"] == "M0_GLOBAL_FINAL_COUNT_FREEZE_V15_READY_PER_GALAXY_PRIVILEGE_AUDIT_PENDING",
        "M0 v15 summary status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_per_galaxy_privilege_count_audit_v10.csv",
        "M0 v15 summary next artifact mismatch",
    )


def validate_m0_per_galaxy_privilege_count_audit_v10() -> None:
    rows = read_csv(ROOT / "data/derived/m0_per_galaxy_privilege_count_audit_v10.csv")
    summary = read_csv(ROOT / "data/derived/m0_per_galaxy_privilege_count_audit_summary_v10.csv")
    require(len(rows) == 18, "M0 v10 per-galaxy privilege audit must cover eighteen rows")
    require(
        [row["audit_row_id"] for row in rows] == [f"M0PGPCA10_{index:03d}" for index in range(1, 19)],
        "M0 v10 per-galaxy audit ids mismatch",
    )
    require(
        {row["source_activation_status"] for row in rows} == {"ACTIVATION_BLOCKED"},
        "M0 v10 must preserve source activation status",
    )
    require(
        {row["m0_label_rule_status"] for row in rows} == {"M0_LABEL_RULE_TABLE_READY_SCORING_BLOCKED"},
        "M0 v10 must inherit label-rule status",
    )
    require(
        {row["row_privilege_status"] for row in rows} == {"RESOLVED_ZERO_NO_ROW_SPECIFIC_M0_PRIVILEGE"},
        "M0 v10 must resolve all rows as zero row-specific privileges",
    )
    require(all(row["per_galaxy_privilege_count_value"] == "0" for row in rows), "M0 v10 counts must be zero")
    require(all(row["freeze_input_allowed"] == "true" for row in rows), "M0 v10 must allow freeze input")
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "M0 v10 cannot allow parsimony")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v10 cannot allow scoring")
    require(
        all(row["next_required_artifact"] == "m0_per_galaxy_privilege_count_freeze_v11.csv" for row in rows),
        "M0 v10 next artifact must be the per-galaxy count freeze",
    )
    require(len(summary) == 1, "M0 v10 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_PER_GALAXY_PRIVILEGE_COUNT_AUDIT_V10", "M0 v10 summary id mismatch")
    require(row["audit_artifact"] == "m0_per_galaxy_privilege_count_audit_v10", "M0 v10 artifact mismatch")
    require(row["source_rows_checked"] == "18", "M0 v10 source row count mismatch")
    require(row["resolved_zero_rows"] == "18", "M0 v10 resolved row count mismatch")
    require(row["unresolved_rows"] == "0", "M0 v10 unresolved count mismatch")
    require(row["per_galaxy_privilege_values_written"] == "18", "M0 v10 value count mismatch")
    require(row["per_galaxy_count_freeze_ready"] == "true", "M0 v10 must be ready for freeze")
    require(row["per_galaxy_count_frozen"] == "false", "M0 v10 cannot freeze count")
    require(row["parsimony_scores_written"] == "0", "M0 v10 cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v10 cannot allow scoring")
    require(
        row["overall_status"] == "M0_PER_GALAXY_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE",
        "M0 v10 summary status mismatch",
    )
    require(
        row["next_required_artifact"] == "m0_per_galaxy_privilege_count_freeze_v11.csv",
        "M0 v10 summary next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m0_per_galaxy_privilege_count_audit_only_no_freeze_no_parsimony_no_scores",
        "M0 v10 claim boundary mismatch",
    )


def validate_m0_per_galaxy_privilege_count_freeze_v11() -> None:
    rows = read_csv(ROOT / "data/derived/m0_per_galaxy_privilege_count_freeze_v11.csv")
    summary = read_csv(ROOT / "data/derived/m0_per_galaxy_privilege_count_freeze_summary_v11.csv")
    require(len(rows) == 18, "M0 v11 per-galaxy privilege freeze must cover eighteen rows")
    require(
        [row["freeze_row_id"] for row in rows] == [f"M0PGPCF11_{index:03d}" for index in range(1, 19)],
        "M0 v11 freeze ids mismatch",
    )
    require(
        {row["freeze_status"] for row in rows} == {"M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11_FROZEN"},
        "M0 v11 rows must be frozen",
    )
    require(
        {row["audit_status"] for row in rows} == {"RESOLVED_ZERO_NO_ROW_SPECIFIC_M0_PRIVILEGE"},
        "M0 v11 must inherit zero row-specific privilege audit status",
    )
    require(all(row["frozen_per_galaxy_privilege_count"] == "0" for row in rows), "M0 v11 frozen counts must be zero")
    require(all(row["parsimony_input_allowed"] == "false" for row in rows), "M0 v11 cannot allow parsimony")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "M0 v11 cannot allow scoring")
    require(
        all(row["next_required_artifact"] == "m1_response_parameter_inventory_v10.csv" for row in rows),
        "M0 v11 must hand off to M1 global inventory",
    )
    require(len(summary) == 1, "M0 v11 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11", "M0 v11 summary id mismatch")
    require(row["freeze_artifact"] == "m0_per_galaxy_privilege_count_freeze_v11", "M0 v11 artifact mismatch")
    require(row["source_rows_checked"] == "18", "M0 v11 source row count mismatch")
    require(row["frozen_zero_rows"] == "18", "M0 v11 frozen zero count mismatch")
    require(row["unresolved_rows"] == "0", "M0 v11 unresolved count mismatch")
    require(row["per_galaxy_count_frozen"] == "true", "M0 v11 must freeze per-galaxy count")
    require(row["frozen_per_galaxy_privilege_count_total"] == "0", "M0 v11 total count mismatch")
    require(row["parsimony_scores_written"] == "0", "M0 v11 cannot write parsimony")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "M0 v11 cannot allow scoring")
    require(
        row["overall_status"] == "M0_PER_GALAXY_PRIVILEGE_COUNT_FREEZE_V11_READY_M1_GLOBAL_COUNT_PENDING",
        "M0 v11 status mismatch",
    )
    require(
        row["next_required_artifact"] == "m1_response_parameter_inventory_v10.csv",
        "M0 v11 next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "m0_per_galaxy_privilege_count_freeze_only_no_parsimony_no_scores",
        "M0 v11 claim boundary mismatch",
    )


def validate_numeric_count_readiness_closure_v09() -> None:
    rows = read_csv(ROOT / "data/derived/numeric_count_readiness_closure_v09.csv")
    summary = read_csv(ROOT / "data/derived/numeric_count_readiness_closure_summary_v09.csv")
    require(len(rows) == 7, "v09 count readiness closure must check seven rows")
    require(
        [row["closure_row_id"] for row in rows] == [f"NCRC09_{index:03d}" for index in range(1, 8)],
        "v09 closure row ids mismatch",
    )
    require({row["family_id"] for row in rows} == {"M0", "M1", "M2", "ALL"}, "v09 closure rows missing families")
    require(all(row["source_readiness_status"] == "COUNT_NOT_READY" for row in rows), "v09 source readiness must remain source-manifest blocked")
    require(rows[0]["closure_decision"] == "COUNT_READINESS_READY", "v09 M0 global row must be ready after v15 freeze")
    require(rows[1]["closure_decision"] == "COUNT_READINESS_READY", "v09 M0 per-galaxy row must be ready after v11 freeze")
    require(rows[2]["closure_decision"] == "COUNT_READINESS_READY", "v09 M1 global row must be ready after v15 freeze")
    require(rows[3]["closure_decision"] == "COUNT_READINESS_READY", "v09 fourth closure row must now be ready")
    require(rows[4]["closure_decision"] == "COUNT_READINESS_READY", "v09 fifth closure row must now be ready")
    require(rows[5]["closure_decision"] == "COUNT_READINESS_READY", "v09 sixth closure row must now be ready")
    require(rows[6]["closure_decision"] == "COUNT_READINESS_READY", "v09 seventh closure row must now be ready")
    require(all(row["numeric_count_values_written"] == "0" for row in rows), "v09 cannot write numeric counts")
    require(all(row["parsimony_scores_written"] == "0" for row in rows), "v09 cannot write parsimony scores")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v09 cannot allow endpoint scoring")
    require(rows[0]["readiness_id"] == "NCR05_M0_GLOBAL", "v09 first closure row must be M0 global")
    require(
        rows[0]["closure_blocker"] == "none",
        "v09 first blocker must be cleared after M0 global final-count freeze",
    )
    require(
        rows[0]["next_required_artifact"] == "none",
        "v09 first next artifact mismatch",
    )
    require(rows[1]["closure_blocker"] == "none", "v09 second blocker mismatch")
    require(
        rows[1]["next_required_artifact"] == "none",
        "v09 second next artifact mismatch",
    )
    require(rows[2]["closure_blocker"] == "none", "v09 third blocker mismatch")
    require(
        rows[2]["next_required_artifact"] == "none",
        "v09 third next artifact mismatch",
    )
    require(rows[3]["closure_blocker"] == "none", "v09 fourth blocker mismatch")
    require(
        rows[3]["next_required_artifact"] == "none",
        "v09 fourth next artifact mismatch",
    )
    require(
        rows[4]["closure_blocker"] == "none",
        "v09 fifth blocker mismatch",
    )
    require(
        rows[4]["next_required_artifact"] == "none",
        "v09 fifth next artifact mismatch",
    )
    require(
        "M0_NO_DARK_FORMULA_TABLE_READY_FOR_PREDICTION_ROWS" in rows[0]["upstream_artifact_status"],
        "v09 must record M0 formula table status",
    )
    require(
        "SOURCE_ROW_AUDIT_SKELETON_PRESENT_NOT_COUNT_READY" in rows[1]["upstream_artifact_status"],
        "v09 must record source-row audit skeleton status",
    )
    require(len(summary) == 1, "v09 closure summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "NUMERIC_COUNT_READINESS_CLOSURE_V09", "v09 summary id mismatch")
    require(row["closure_artifact"] == "numeric_count_readiness_closure_v09", "v09 artifact mismatch")
    require(
        row["v08_status"] == "NUMERIC_PARAMETER_COUNT_TABLE_V08_BLOCKED_ON_FINAL_NUMERIC_COUNT_VALUES",
        "v09 must record the current v08 final-values-blocked status",
    )
    require(row["readiness_rows_checked"] == "7", "v09 readiness row count mismatch")
    require(rows[5]["closure_blocker"] == "none", "v09 sixth blocker mismatch")
    require(rows[5]["next_required_artifact"] == "none", "v09 sixth next artifact mismatch")
    require(rows[6]["closure_blocker"] == "none", "v09 seventh blocker mismatch")
    require(rows[6]["next_required_artifact"] == "none", "v09 seventh next artifact mismatch")
    require(row["closure_ready_rows"] == "7", "v09 must ready all closure rows")
    require(row["closure_blocked_rows"] == "0", "v09 must clear all closure blockers")
    require(row["numeric_count_values_written"] == "0", "v09 cannot write numeric count values")
    require(row["parsimony_scores_written"] == "0", "v09 cannot write parsimony scores")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v09 cannot allow endpoint scoring")
    require(
        row["overall_status"] == "NUMERIC_COUNT_READINESS_CLOSURE_READY_FOR_FINAL_COUNTS",
        "v09 status mismatch",
    )
    require(
        row["next_required_artifact"] == "numeric_parameter_count_table_final_values_v10.csv",
        "v09 next artifact mismatch",
    )
    require(
        row["claim_boundary"] == "numeric_count_readiness_closure_only_no_counts_no_parsimony_no_scores",
        "v09 claim boundary mismatch",
    )


def validate_family_prediction_frontier_trace_v81() -> None:
    rows = read_csv(ROOT / "data/derived/family_prediction_frontier_trace_v81.csv")
    summary = read_csv(ROOT / "data/derived/family_prediction_frontier_trace_summary_v81.csv")
    require(len(rows) == 7, "v81 frontier trace must have seven rows")
    require(
        [row["frontier_layer"] for row in rows]
        == [
            "family_prediction_table",
            "m0_formula_table",
            "m0_formula_body",
            "m0_readout_equation",
            "m0_equation_kernel",
            "m0_frozen_expression_body",
            "m0_payload_evidence",
        ],
        "v81 frontier trace order mismatch",
    )
    require(
        rows[0]["numeric_prediction_rows_written"] == "450"
        and all(row["numeric_prediction_rows_written"] == "0" for row in rows[1:]),
        "v81 trace must report only the emitted M0 family prediction rows",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v81 trace cannot allow scoring")
    require(
        all(row["dark_sector_verdict_allowed"] == "false" for row in rows),
        "v81 trace cannot decide dark-sector verdict",
    )
    require(rows[1]["artifact"] == "m0_no_dark_formula_table_v06", "v81 formula-table artifact mismatch")
    require(rows[1]["blocking_slot"] == "formula_table_policy", "v81 first policy blocker slot mismatch")
    require(
        rows[1]["narrowed_next_artifact"] == "family_prediction_tables_v08.csv",
        "v81 first policy blocker artifact mismatch",
    )
    require(
        rows[0]["narrowed_next_artifact"] == "scoring_preflight_v07.csv",
        "v81 family prediction blocker artifact mismatch",
    )
    require(len(summary) == 1, "v81 trace summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "FAMILY_PREDICTION_FRONTIER_TRACE_V81", "v81 summary id mismatch")
    require(row["trace_artifact"] == "family_prediction_frontier_trace_v81", "v81 trace artifact mismatch")
    require(row["trace_steps"] == "7", "v81 summary trace count mismatch")
    require(row["payload_side_ready"] == "true", "v81 payload side must be ready")
    require(
        row["first_family_prediction_frontier"] == "family_prediction_tables_v08.csv",
        "v81 family frontier mismatch",
    )
    require(
        row["first_content_blocker"] == "scoring_preflight_v07.csv",
        "v81 first content blocker mismatch",
    )
    require(row["formula_rows_written"] == "0", "v81 must write zero formula rows")
    require(row["numeric_prediction_rows_written"] == "450", "v81 must report 450 emitted M0 prediction rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v81 summary cannot allow scoring")
    require(
        row["overall_status"] == "FAMILY_PREDICTION_FRONTIER_TRACED_TO_SCORING_PREFLIGHT",
        "v81 status mismatch",
    )
    require(
        row["next_required_artifact"] == "scoring_preflight_v07.csv",
        "v81 next artifact mismatch",
    )


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
    require(row["real_input_file_present"] == "true", "v14 must report the packaged real input file")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v14 summary must forbid scoring")


def validate_source_import_raw_adapter_v15() -> None:
    schema = read_csv(ROOT / "data/derived/source_import_raw_adapter_schema_v15.csv")
    gate = read_csv(ROOT / "data/derived/source_import_raw_adapter_gate_v15.csv")
    summary = read_csv(ROOT / "data/derived/source_import_raw_adapter_summary_v15.csv")
    require(len(schema) == 16, "v15 raw adapter schema must map sixteen target fields")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in schema), "v15 schema cannot allow scoring")
    require(len(gate) == 1, "v15 raw adapter gate must have one row")
    gate_row = gate[0]
    require(
        gate_row["raw_input_status"] == "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW",
        "v15 raw input must be present for review",
    )
    require(gate_row["raw_rows_seen"] == "450", "v15 must see 450 raw rows")
    require(gate_row["valid_raw_rows"] == "450", "v15 must validate 450 raw rows")
    require(gate_row["galaxies_with_valid_raw_rows"] == "18", "v15 must cover eighteen galaxies")
    require(gate_row["target_file_written"] == "false", "v15 must not write the target input")
    require(gate_row["endpoint_scoring_allowed"] == "false", "v15 gate cannot allow scoring")
    require(len(summary) == 1, "v15 summary must have one row")
    row = summary[0]
    require(
        row["overall_status"] == "RAW_ADAPTER_READY_VALIDATION_PENDING_REVIEW",
        "v15 must be raw-input validation-pending",
    )
    require(row["raw_input_status"] == "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW", "v15 summary must report raw input")
    require(row["target_input_file_present"] == "true", "v15 must report the packaged target input")
    require(row["target_file_written_by_adapter"] == "false", "v15 adapter must not write target file")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v15 summary must forbid scoring")


def validate_source_import_write_authorization_v16() -> None:
    rows = read_csv(ROOT / "data/derived/source_import_write_authorization_v16.csv")
    summary = read_csv(ROOT / "data/derived/source_import_write_authorization_summary_v16.csv")
    require(len(rows) == 1, "v16 write authorization must have one row")
    row = rows[0]
    require(row["authorization_file"] == "data/input/source_import_real_values_write_authorization_v57.csv", "v16 auth file mismatch")
    require(row["explicit_write_authorization"] == "true", "v16 explicit write authorization must be present")
    require(row["raw_input_status"] == "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW", "v16 raw input must be present")
    require(row["target_input_file_present"] == "true", "v16 must report the packaged target input")
    require(row["write_authorized"] == "true", "v16 write authorization must be ready")
    require(row["write_blockers"] == "none", "v16 must have no write blockers")
    require("raw_input_not_validated" not in row["write_blockers"], "v16 must not block on raw validation")
    require(row["target_file_written"] == "false", "v16 must not write target input")
    require(row["endpoint_scoring_allowed"] == "false", "v16 row cannot allow scoring")
    require(len(summary) == 1, "v16 summary must have one row")
    summary_row = summary[0]
    require(summary_row["overall_status"] == "WRITE_AUTHORIZATION_READY", "v16 write authorization must be ready")
    require(summary_row["write_authorized"] == "true", "v16 summary must authorize writing")
    require(summary_row["target_file_written"] == "false", "v16 summary must not write target file")
    require(summary_row["target_input_file_present"] == "true", "v16 summary must report present target file")
    require(
        summary_row["next_required_artifact"] == "data/input/source_import_real_values_v12.csv",
        "v16 next required artifact must be v12 target",
    )
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "v16 summary must forbid scoring")


def validate_source_import_authorized_writer_v17() -> None:
    rows = read_csv(ROOT / "data/derived/source_import_authorized_writer_v17.csv")
    summary = read_csv(ROOT / "data/derived/source_import_authorized_writer_summary_v17.csv")
    require(len(rows) == 1, "v17 authorized writer must have one row")
    row = rows[0]
    require(row["write_authorized"] == "true", "v17 write authorization must be true")
    require(row["raw_input_present"] == "true", "v17 raw input must be present")
    require(row["target_file_written"] == "true", "v17 must write target input")
    require(row["rows_written"] == "450", "v17 must write 450 rows")
    require(row["writer_status"] == "TARGET_INPUT_WRITTEN_FROM_AUTHORIZED_RAW", "v17 writer must write target")
    require(row["endpoint_scoring_allowed"] == "false", "v17 row cannot allow scoring")
    require(len(summary) == 1, "v17 summary must have one row")
    summary_row = summary[0]
    require(summary_row["overall_status"] == "AUTHORIZED_WRITER_WROTE_TARGET_INPUT", "v17 summary must write target")
    require(summary_row["target_file_written"] == "true", "v17 summary must write target input")
    require(summary_row["rows_written"] == "450", "v17 summary must write 450 rows")
    require(summary_row["target_input_file_present_after_writer"] == "true", "v17 target input must be present after writer")
    require(
        summary_row["next_required_artifact"] == "data/input/source_import_real_values_v12.csv",
        "v17 next required artifact must be v12 target",
    )
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "v17 summary must forbid scoring")


def validate_active_v15_raw_sparc_like_input_writer_v56() -> None:
    rows = read_csv(ROOT / "data/input/source_import_raw_sparc_like_v15.csv")
    summary = read_csv(ROOT / "data/derived/active_v15_raw_sparc_like_input_writer_summary_v56.csv")
    require(len(rows) == 450, "v56 raw input must contain 450 rows")
    require(len({row["galaxy_id"] for row in rows}) == 18, "v56 raw input must cover eighteen galaxies")
    require(all(row["catalog"] == "SPARC" for row in rows), "v56 rows must use SPARC catalog")
    require(all(row["table_or_file"] == "MassModels_Lelli2016c.mrt" for row in rows), "v56 table mismatch")
    require(all(row["sha256_or_external_accession"].startswith("sha256:") for row in rows), "v56 rows need sha256 source")
    require(len(summary) == 1, "v56 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "ACTIVE_V15_RAW_SPARC_LIKE_INPUT_WRITER_V56", "v56 summary id mismatch")
    require(row["raw_rows_written"] == "450", "v56 summary row count mismatch")
    require(row["galaxies_written"] == "18", "v56 summary galaxy count mismatch")
    require(row["target_file_written"] == "true", "v56 target file must be written")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v56 summary must forbid scoring")
    require(row["overall_status"] == "ACTIVE_V15_RAW_SPARC_LIKE_INPUT_WRITTEN", "v56 status mismatch")


def validate_active_v12_real_values_write_authorization_v57() -> None:
    rows = read_csv(ROOT / "data/input/source_import_real_values_write_authorization_v57.csv")
    summary = read_csv(ROOT / "data/derived/active_v12_real_values_write_authorization_summary_v57.csv")
    require(len(rows) == 1, "v57 authorization must have one row")
    row = rows[0]
    require(row["authorization_id"] == "ARV57_WRITE_REAL_VALUES_FROM_V15_RAW", "v57 authorization id mismatch")
    require(row["raw_input_status"] == "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW", "v57 raw status mismatch")
    require(row["write_authorization"] == "AUTHORIZE_V12_WRITE_FROM_ACTIVE_V15_RAW", "v57 must authorize v12 write")
    require(row["endpoint_scoring_allowed"] == "false", "v57 cannot allow scoring")
    require(len(summary) == 1, "v57 summary must have one row")
    summary_row = summary[0]
    require(summary_row["summary_id"] == "ACTIVE_V12_REAL_VALUES_WRITE_AUTHORIZATION_V57", "v57 summary id mismatch")
    require(summary_row["write_authorized"] == "true", "v57 summary must authorize write")
    require(summary_row["target_file_written"] == "false", "v57 itself must not write target")
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "v57 summary cannot allow scoring")
    require(summary_row["overall_status"] == "ACTIVE_V12_WRITE_AUTHORIZATION_GRANTED", "v57 status mismatch")


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
    require(row["raw_input_file_present"] == "true", "v18 must report the active raw input file")
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
    require(all(row["provenance_complete"] == "true" for row in rows), "v20 must complete all provenance rows")
    require(all(row["raw_import_decision"] == "ALLOW_RAW_IMPORT" for row in rows), "v20 must allow raw import")
    require(all(row["blocking_requirements"] == "none" for row in rows), "v20 must clear provenance blockers")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v20 rows cannot allow scoring")
    require(len(summary) == 1, "v20 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "RAW_IMPORT_READY_BY_PROVENANCE", "v20 must allow raw import by provenance")
    require(row["audited_rows"] == "18", "v20 summary must audit eighteen rows")
    require(row["provenance_complete_rows"] == "18", "v20 must complete eighteen provenance rows")
    require(row["raw_import_allowed_rows"] == "18", "v20 must allow eighteen raw imports")
    require(row["raw_import_blocked_rows"] == "0", "v20 must block zero rows")
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
    require(row["evidence_input_file_present"] == "true", "v21 must detect real evidence input")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v21 summary must forbid scoring")


def validate_source_import_provenance_evidence_gate_v22() -> None:
    gate = read_csv(ROOT / "data/derived/source_import_provenance_evidence_gate_v22.csv")
    summary = read_csv(ROOT / "data/derived/source_import_provenance_evidence_gate_summary_v22.csv")
    require(len(gate) == 1, "v22 evidence gate must have one row")
    row = gate[0]
    require(row["evidence_input_status"] == "EVIDENCE_INPUT_PRESENT_VALIDATION_PENDING_REVIEW", "v22 evidence input must be present")
    require(row["evidence_rows_seen"] == "18", "v22 must see eighteen evidence rows")
    require(row["valid_evidence_rows"] == "18", "v22 must validate eighteen evidence rows")
    require(row["galaxies_with_valid_evidence"] == "18", "v22 must validate eighteen galaxies")
    require(row["provenance_promotion_allowed"] == "true", "v22 must allow provenance promotion")
    require(row["endpoint_scoring_allowed"] == "false", "v22 row cannot allow scoring")
    require(len(summary) == 1, "v22 summary must have one row")
    summary_row = summary[0]
    require(summary_row["overall_status"] == "PROVENANCE_EVIDENCE_READY_FOR_PROMOTION", "v22 summary must report ready evidence")
    require(
        summary_row["evidence_input_status"] == "EVIDENCE_INPUT_PRESENT_VALIDATION_PENDING_REVIEW",
        "v22 summary must report present evidence input",
    )
    require(summary_row["valid_evidence_rows"] == "18", "v22 summary must validate eighteen rows")
    require(summary_row["provenance_promotion_allowed"] == "true", "v22 summary must allow promotion")
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "v22 summary must forbid scoring")


def validate_source_import_provenance_promotion_gate_v23() -> None:
    rows = read_csv(ROOT / "data/derived/source_import_provenance_promotion_gate_v23.csv")
    summary = read_csv(ROOT / "data/derived/source_import_provenance_promotion_summary_v23.csv")
    require(len(rows) == 18, "v23 promotion gate must cover eighteen candidate rows")
    require(
        all(row["v22_provenance_promotion_allowed"] == "true" for row in rows),
        "v23 must inherit the ready v22 promotion decision",
    )
    require(all(row["promotion_allowed"] == "true" for row in rows), "v23 must allow all promotions")
    require(
        all(row["promotion_decision"] == "PROMOTE_PROVENANCE" for row in rows),
        "v23 must promote provenance",
    )
    require(all(row["promotion_blockers"] == "none" for row in rows), "v23 must clear promotion blockers")
    require(all(row["provenance_rows_promoted"] == "1" for row in rows), "v23 must promote all rows")
    require(all(row["raw_import_allowed_after_promotion"] == "true" for row in rows), "v23 must allow raw import")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v23 rows cannot allow scoring")
    require(len(summary) == 1, "v23 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "PROVENANCE_PROMOTION_READY_NOT_IMPORTED", "v23 summary must be ready")
    require(row["candidate_rows"] == "18", "v23 summary must cover eighteen rows")
    require(row["promotion_allowed_rows"] == "18", "v23 must allow eighteen promotions")
    require(row["promotion_blocked_rows"] == "0", "v23 must block zero promotions")
    require(row["provenance_rows_promoted"] == "18", "v23 must promote eighteen provenance rows")
    require(row["raw_import_allowed_rows_after_promotion"] == "18", "v23 must allow eighteen raw imports")
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
    ready_ids = {row["dependency_id"] for row in rows if row["dependency_decision"] == "READY"}
    require(
        ready_ids
        == {
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
        },
        f"v24 ready ids mismatch: {ready_ids}",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v24 rows cannot allow scoring")
    require(any(row["upstream_status"] == "PROVENANCE_PROMOTION_READY_NOT_IMPORTED" for row in rows), "v24 must include v23 ready")
    require(
        any(row["upstream_status"] == "SCORING_ACTIVATION_READY_GLOBAL_PREREQUISITES_READY" for row in rows),
        "v24 must include v13 row activation readiness",
    )
    require(len(summary) == 1, "v24 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SCORING_DEPENDENCY_CLOSURE_READY", "v24 summary must mark dependency closure ready")
    require(row["dependencies_checked"] == "13", "v24 must check thirteen dependencies")
    require(row["ready_dependencies"] == "13", "v24 must have thirteen ready dependencies")
    require(row["blocked_dependencies"] == "0", "v24 must block zero dependencies")
    require(
        row["next_required_artifact"] == "none",
        "v24 next artifact mismatch",
    )
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v24 summary must forbid scoring")


def validate_scoring_unblock_priority_v25() -> None:
    rows = read_csv(ROOT / "data/derived/scoring_unblock_priority_v25.csv")
    summary = read_csv(ROOT / "data/derived/scoring_unblock_priority_summary_v25.csv")
    require(len(rows) == 13, "v25 priority ledger must cover thirteen dependencies")
    ranks = [int(row["priority_rank"]) for row in rows]
    require(ranks == list(range(1, 14)), f"v25 ranks must be contiguous: {ranks}")
    ready_ids = {row["dependency_id"] for row in rows if row["dependency_decision"] == "READY"}
    require(
        ready_ids
        == {
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
        },
        f"v25 ready ids mismatch: {ready_ids}",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v25 rows cannot allow scoring")
    frontier = [row for row in rows if row["frontier_now"] == "true"]
    require(frontier == [], "v25 must clear dependency frontiers")
    require(len(summary) == 1, "v25 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SCORING_UNBLOCK_FRONTIER_CLEAR", "v25 must clear dependency frontier")
    require(row["priority_rows"] == "13", "v25 must summarize thirteen priorities")
    require(row["blocked_priority_rows"] == "0", "v25 must preserve zero blocked rows")
    require(row["frontier_now_rows"] == "0", "v25 must summarize zero current frontiers")
    require(row["first_frontier_dependency"] == "none", "v25 frontier dependency mismatch")
    require(
        row["first_frontier_artifact"] == "none",
        "v25 frontier artifact mismatch",
    )
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v25 summary must forbid scoring")


def validate_scoring_frontier_status_v72() -> None:
    rows = read_csv(ROOT / "data/derived/scoring_frontier_status_v72.csv")
    summary = read_csv(ROOT / "data/derived/scoring_frontier_status_summary_v72.csv")
    require(len(rows) == 3, "v72 frontier status must have three rows")
    require(
        [row["frontier_id"] for row in rows]
        == [
            "SFS72_LEAKAGE_PARTIAL_SUFFICIENCY_RESPONSE",
            "SFS72_FULL_LEAKAGE_EVIDENCE_INGESTION",
            "SFS72_SCORING_ACTIVATION_RECHECK",
        ],
        "v72 frontier order mismatch",
    )
    require(all(row["required_before_scoring"] == "true" for row in rows), "v72 rows must be required before scoring")
    require(all(row["target_evidence_rows_created"] == "0" for row in rows), "v72 cannot create evidence")
    require(all(row["leakage_pass_authorized"] == "false" for row in rows), "v72 cannot authorize leakage pass")
    require(all(row["activation_rows_authorized"] == "0" for row in rows), "v72 cannot authorize activation")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v72 cannot allow scoring")
    require(
        rows[0]["next_required_artifact"] == "full_leakage_evidence_ingestion_gate_after_accepted_v71_response",
        "v72 first frontier artifact mismatch",
    )
    require(
        rows[0]["current_status"] == "PARTIAL_SUFFICIENCY_REVIEW_READY_FOR_LATER_LEAKAGE_EVIDENCE_GATE",
        "v72 first frontier must reflect accepted v73 response",
    )
    require(
        "36 partial rows are preaudit review-ready" in rows[0]["ready_detail"],
        "v72 first frontier must expose v74 preaudit readiness",
    )
    require(
        rows[1]["current_status"] == "LEAKAGE_AUDIT_PASS_REVIEWED_ACTIVATION_PENDING",
        "v72 second frontier must reflect v78 leakage pass",
    )
    require(
        rows[1]["next_required_artifact"] == "scoring_preflight_v07.csv",
        "v72 second frontier must hand off to scoring preflight",
    )
    require(
        rows[2]["current_status"] == "FAMILY_PREDICTION_TABLE_CONTRACT_READY_PARAMETER_COUNTS_BLOCKED",
        "v72 third frontier must reflect v80 formula-slot blocker",
    )
    require(
        rows[2]["next_required_artifact"] == "scoring_preflight_v07.csv",
        "v72 third frontier must point to scoring preflight",
    )
    require(len(summary) == 1, "v72 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "SCORING_FRONTIER_STATUS_V72", "v72 summary id mismatch")
    require(row["frontier_rows"] == "3", "v72 summary must record three frontier rows")
    require(row["blocked_frontier_rows"] == "3", "v72 must keep all frontier rows blocked")
    require(row["first_frontier_id"] == "SFS72_LEAKAGE_PARTIAL_SUFFICIENCY_RESPONSE", "v72 first frontier mismatch")
    require(
        row["first_frontier_artifact"] == "scoring_preflight_v07.csv",
        "v72 first frontier artifact summary mismatch",
    )
    require(row["required_components_for_full_scoring_leakage_pass"] == "4", "v72 must require four leakage components")
    require(row["partial_candidate_rows_requiring_review"] == "0", "v72 must clear the 36-row partial blocker")
    require(row["target_evidence_rows_created"] == "0", "v72 summary cannot create evidence")
    require(row["leakage_pass_authorized"] == "0", "v72 summary cannot authorize leakage pass")
    require(row["activation_rows_authorized"] == "0", "v72 summary cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v72 summary must forbid scoring")
    require(
        row["overall_status"] == "SCORING_FRONTIER_BLOCKED_ON_SCORING_PREFLIGHT",
        "v72 status mismatch",
    )


def validate_frontier_provenance_evidence_acceptance_v26() -> None:
    rows = read_csv(ROOT / "data/derived/frontier_provenance_evidence_acceptance_v26.csv")
    summary = read_csv(ROOT / "data/derived/frontier_provenance_evidence_acceptance_summary_v26.csv")
    require(len(rows) == 18, "v26 acceptance checklist must cover eighteen candidate rows")
    require(all(row["frontier_dependency"] == "SCD24_PROVENANCE_EVIDENCE" for row in rows), "v26 must target the v25 frontier")
    require(
        all(row["frontier_artifact"] == "data/input/source_import_provenance_evidence_v21.csv" for row in rows),
        "v26 must target the provenance evidence input",
    )
    require(all(row["evidence_input_present"] == "true" for row in rows), "v26 must see real evidence input")
    require(all(row["missing_or_placeholder_fields"] == "none" for row in rows), "v26 must clear missing input fields")
    require(all(row["acceptance_status"] == "ACCEPTED_FOR_REVIEW" for row in rows), "v26 rows must be accepted")
    require(all(row["accepted_for_promotion_review"] == "true" for row in rows), "v26 must accept all rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v26 rows cannot allow scoring")
    require(len(summary) == 1, "v26 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "FRONTIER_EVIDENCE_ACCEPTANCE_REVIEW_READY", "v26 must be review-ready")
    require(row["candidate_rows"] == "18", "v26 must summarize eighteen candidates")
    require(row["evidence_input_rows_present"] == "18", "v26 must see eighteen evidence rows")
    require(row["accepted_for_promotion_review_rows"] == "18", "v26 must accept eighteen rows")
    require(row["blocked_rows"] == "0", "v26 must block zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v26 summary must forbid scoring")


def validate_frontier_provenance_evidence_work_order_v27() -> None:
    rows = read_csv(ROOT / "data/derived/frontier_provenance_evidence_work_order_v27.csv")
    summary = read_csv(ROOT / "data/derived/frontier_provenance_evidence_work_order_summary_v27.csv")
    require(len(rows) == 18, "v27 work order must cover eighteen candidate rows")
    require(all(row["frontier_dependency"] == "SCD24_PROVENANCE_EVIDENCE" for row in rows), "v27 must target the first frontier")
    require(
        all(row["target_evidence_artifact"] == "data/input/source_import_provenance_evidence_v21.csv" for row in rows),
        "v27 must target the provenance evidence input",
    )
    require(all(row["current_acceptance_status"] == "ACCEPTED_FOR_REVIEW" for row in rows), "v27 must inherit v26 accepted status")
    require(
        all(row["work_order_status"] == "OPEN_EVIDENCE_COLLECTION_REQUIRED" for row in rows),
        "v27 work orders must remain open",
    )
    require(all(row["may_write_evidence_input"] == "false" for row in rows), "v27 cannot authorize evidence writes")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v27 rows cannot allow scoring")
    require(all("set_PROVENANCE_EVIDENCE_COMPLETE_only_after_review" in row["minimum_source_tasks"] for row in rows), "v27 must require reviewed completion")
    require(len(summary) == 1, "v27 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "FRONTIER_EVIDENCE_WORK_ORDER_OPEN", "v27 summary must remain open")
    require(row["work_order_rows"] == "18", "v27 must summarize eighteen work orders")
    require(row["open_work_order_rows"] == "18", "v27 must keep eighteen open work orders")
    require(row["closed_work_order_rows"] == "0", "v27 must close zero work orders")
    require(row["may_write_evidence_input_anywhere"] == "false", "v27 summary cannot authorize evidence writes")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v27 summary must forbid scoring")


def validate_frontier_work_order_completion_gate_v28() -> None:
    rows = read_csv(ROOT / "data/derived/frontier_work_order_completion_gate_v28.csv")
    summary = read_csv(ROOT / "data/derived/frontier_work_order_completion_gate_summary_v28.csv")
    require(len(rows) == 18, "v28 completion gate must cover eighteen work orders")
    require(all(row["accepted_for_promotion_review"] == "true" for row in rows), "v28 must inherit accepted rows")
    require(
        all(row["work_order_status"] == "OPEN_EVIDENCE_COLLECTION_REQUIRED" for row in rows),
        "v28 must inherit open work orders",
    )
    require(all("work_order_open" in row["completion_blockers"] for row in rows), "v28 must report open work-order blocker")
    require(
        all("not_accepted_for_promotion_review" not in row["completion_blockers"] for row in rows),
        "v28 must clear promotion-review blocker",
    )
    require(
        all(row["completion_decision"] == "DO_NOT_CLOSE_WORK_ORDER" for row in rows),
        "v28 must close zero work orders",
    )
    require(all(row["may_write_evidence_input_after_completion"] == "false" for row in rows), "v28 cannot authorize evidence writes")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v28 rows cannot allow scoring")
    require(len(summary) == 1, "v28 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "FRONTIER_WORK_ORDER_COMPLETION_BLOCKED", "v28 summary must block completion")
    require(row["completion_gate_rows"] == "18", "v28 must summarize eighteen gates")
    require(row["work_orders_closed"] == "0", "v28 must close zero work orders")
    require(row["work_orders_blocked"] == "18", "v28 must block eighteen work orders")
    require(row["may_write_evidence_input_anywhere"] == "false", "v28 summary cannot authorize evidence writes")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v28 summary must forbid scoring")


def validate_frontier_evidence_write_authorization_v29() -> None:
    rows = read_csv(ROOT / "data/derived/frontier_evidence_write_authorization_v29.csv")
    summary = read_csv(ROOT / "data/derived/frontier_evidence_write_authorization_summary_v29.csv")
    require(len(rows) == 1, "v29 write authorization must have one row")
    row = rows[0]
    require(row["completion_gate_status"] == "FRONTIER_WORK_ORDER_COMPLETION_BLOCKED", "v29 must inherit blocked v28 status")
    require(row["completion_gate_rows"] == "18", "v29 must inspect eighteen completion rows")
    require(row["work_orders_closed"] == "0", "v29 must see zero closed work orders")
    require(row["target_evidence_input_present"] == "true", "v29 target evidence input must be present from v55")
    require("frontier_work_orders_not_closed" in row["write_blockers"], "v29 must block on open frontier work orders")
    require(row["write_authorized"] == "false", "v29 cannot authorize evidence writes")
    require(row["target_file_written"] == "false", "v29 must write no target file")
    require(row["endpoint_scoring_allowed"] == "false", "v29 row cannot allow scoring")
    require(len(summary) == 1, "v29 summary must have one row")
    summary_row = summary[0]
    require(summary_row["overall_status"] == "FRONTIER_EVIDENCE_WRITE_BLOCKED", "v29 summary must block evidence writing")
    require(summary_row["write_authorized"] == "false", "v29 summary cannot authorize writing")
    require(summary_row["target_evidence_input_present"] == "true", "v29 summary must detect target")
    require(summary_row["target_file_written"] == "false", "v29 summary must write no target")
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "v29 summary must forbid scoring")


def validate_frontier_authorized_evidence_writer_v30() -> None:
    rows = read_csv(ROOT / "data/derived/frontier_authorized_evidence_writer_v30.csv")
    summary = read_csv(ROOT / "data/derived/frontier_authorized_evidence_writer_summary_v30.csv")
    require(len(rows) == 1, "v30 authorized evidence writer must have one row")
    row = rows[0]
    require(row["write_authorized"] == "false", "v30 must inherit blocked authorization")
    require(row["target_preexisting"] == "true", "v30 target evidence input must be preexisting")
    require(row["target_file_written"] == "false", "v30 must write no target file")
    require(row["rows_written"] == "0", "v30 must write zero rows")
    require(row["writer_status"] == "WRITER_BLOCKED_BY_FRONTIER_AUTHORIZATION", "v30 writer must be blocked")
    require(row["endpoint_scoring_allowed"] == "false", "v30 row cannot allow scoring")
    require(len(summary) == 1, "v30 summary must have one row")
    summary_row = summary[0]
    require(summary_row["overall_status"] == "FRONTIER_AUTHORIZED_EVIDENCE_WRITER_BLOCKED", "v30 summary must block writer")
    require(summary_row["writer_status"] == "WRITER_BLOCKED_BY_FRONTIER_AUTHORIZATION", "v30 summary status mismatch")
    require(summary_row["write_authorized"] == "false", "v30 summary cannot authorize writing")
    require(summary_row["target_file_written"] == "false", "v30 summary must write no target")
    require(summary_row["rows_written"] == "0", "v30 summary must write zero rows")
    require(summary_row["target_input_file_present_after_writer"] == "true", "v30 target must remain present after writer")
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "v30 summary must forbid scoring")


def validate_frontier_post_writer_evidence_absence_audit_v31() -> None:
    rows = read_csv(ROOT / "data/derived/frontier_post_writer_evidence_absence_audit_v31.csv")
    summary = read_csv(ROOT / "data/derived/frontier_post_writer_evidence_absence_audit_summary_v31.csv")
    require(len(rows) == 1, "v31 post-writer absence audit must have one row")
    row = rows[0]
    require(row["writer_status"] == "WRITER_BLOCKED_BY_FRONTIER_AUTHORIZATION", "v31 must inherit blocked writer")
    require(row["writer_rows_written"] == "0", "v31 must inherit zero writer rows")
    require(row["writer_target_file_written"] == "false", "v31 must inherit no target write")
    require(row["active_writer_status"] == "ACTIVE_V21_PROVENANCE_EVIDENCE_WRITTEN", "v31 must see active v21 writer")
    require(row["target_evidence_input_present_after_audit"] == "true", "v31 target evidence input must be present")
    require(row["absence_confirmed"] == "false", "v31 must no longer confirm target evidence absence")
    require(row["evidence_gate_may_be_promoted"] == "true", "v31 must allow evidence gate promotion")
    require(row["endpoint_scoring_allowed"] == "false", "v31 row cannot allow scoring")
    require(len(summary) == 1, "v31 summary must have one row")
    summary_row = summary[0]
    require(
        summary_row["overall_status"] == "FRONTIER_EVIDENCE_INPUT_PRESENT_VIA_ACTIVE_V21_WRITER",
        "v31 summary must record active writer evidence presence",
    )
    require(summary_row["absence_confirmed"] == "false", "v31 summary must not confirm absence")
    require(summary_row["target_evidence_input_present_after_audit"] == "true", "v31 summary target must be present")
    require(summary_row["evidence_gate_may_be_promoted"] == "true", "v31 summary must promote evidence gate")
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "v31 summary must forbid scoring")


def validate_post_writer_evidence_gate_recheck_v32() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_evidence_gate_recheck_v32.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_evidence_gate_recheck_summary_v32.csv")
    require(len(rows) == 1, "v32 post-writer evidence gate recheck must have one row")
    row = rows[0]
    require(row["absence_confirmed"] == "false", "v32 must inherit evidence presence")
    require(
        row["evidence_input_status"] == "EVIDENCE_INPUT_PRESENT_VALIDATION_PENDING_REVIEW",
        "v32 evidence input must be present",
    )
    require(row["valid_evidence_rows"] == "18", "v32 must see eighteen valid evidence rows")
    require(row["provenance_promotion_allowed_before_recheck"] == "true", "v32 must inherit allowed promotion")
    require(row["recheck_blockers"] == "none", "v32 must have no evidence recheck blockers")
    require(row["provenance_promotion_allowed_after_recheck"] == "true", "v32 must allow promotion")
    require(row["endpoint_scoring_allowed"] == "false", "v32 row cannot allow scoring")
    require(len(summary) == 1, "v32 summary must have one row")
    summary_row = summary[0]
    require(summary_row["overall_status"] == "POST_WRITER_EVIDENCE_GATE_RECHECK_READY", "v32 summary must be ready")
    require(summary_row["absence_confirmed"] == "false", "v32 summary must inherit evidence presence")
    require(summary_row["valid_evidence_rows"] == "18", "v32 summary must see eighteen valid rows")
    require(summary_row["provenance_promotion_allowed_after_recheck"] == "true", "v32 summary must promote")
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "v32 summary must forbid scoring")


def validate_post_writer_provenance_promotion_recheck_v33() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_provenance_promotion_recheck_v33.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_provenance_promotion_recheck_summary_v33.csv")
    require(len(rows) == 18, "v33 promotion recheck must cover eighteen rows")
    require(all(row["v23_promotion_decision"] == "PROMOTE_PROVENANCE" for row in rows), "v33 must inherit v23 promotion")
    require(all(row["valid_evidence_rows_after_writer"] == "18" for row in rows), "v33 must see valid evidence rows")
    require(all(row["promotion_recheck_blockers"] == "none" for row in rows), "v33 must have no promotion blockers")
    require(
        all(row["provenance_promotion_allowed_after_recheck"] == "true" for row in rows),
        "v33 must allow provenance promotion",
    )
    require(all(row["provenance_rows_promoted_after_recheck"] == "1" for row in rows), "v33 must promote all rows")
    require(all(row["raw_import_allowed_after_recheck"] == "true" for row in rows), "v33 must allow raw import")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v33 rows cannot allow scoring")
    require(len(summary) == 1, "v33 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "POST_WRITER_PROVENANCE_PROMOTION_RECHECK_READY", "v33 summary must be ready")
    require(row["promotion_recheck_rows"] == "18", "v33 must summarize eighteen rows")
    require(row["promotion_allowed_rows_after_recheck"] == "18", "v33 must allow eighteen promotions")
    require(row["promotion_blocked_rows_after_recheck"] == "0", "v33 must block zero promotions")
    require(row["provenance_rows_promoted_after_recheck"] == "18", "v33 must promote eighteen rows")
    require(row["raw_import_allowed_rows_after_recheck"] == "18", "v33 must allow eighteen raw imports")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v33 summary must forbid scoring")


def validate_post_writer_raw_import_recheck_v34() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_raw_import_recheck_v34.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_raw_import_recheck_summary_v34.csv")
    require(len(rows) == 18, "v34 raw import recheck must cover eighteen rows")
    require(all(row["v20_raw_import_decision"] == "ALLOW_RAW_IMPORT" for row in rows), "v34 must inherit v20 raw import allowance")
    require(all(row["provenance_rows_promoted_after_recheck"] == "1" for row in rows), "v34 must inherit promoted provenance rows")
    require(all(row["raw_import_recheck_blockers"] == "none" for row in rows), "v34 must have no raw import blockers")
    require(all(row["raw_import_allowed_after_recheck"] == "true" for row in rows), "v34 must allow raw import")
    require(all(row["raw_rows_imported_after_recheck"] == "0" for row in rows), "v34 must import zero raw rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v34 rows cannot allow scoring")
    require(len(summary) == 1, "v34 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "POST_WRITER_RAW_IMPORT_RECHECK_READY", "v34 summary must be ready")
    require(row["raw_import_recheck_rows"] == "18", "v34 must summarize eighteen rows")
    require(row["raw_import_allowed_rows_after_recheck"] == "18", "v34 must allow eighteen raw imports")
    require(row["raw_import_blocked_rows_after_recheck"] == "0", "v34 must block zero raw imports")
    require(row["raw_rows_imported_after_recheck"] == "0", "v34 must import zero raw rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v34 summary must forbid scoring")


def validate_post_writer_raw_adapter_recheck_v35() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_raw_adapter_recheck_v35.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_raw_adapter_recheck_summary_v35.csv")
    require(len(rows) == 1, "v35 raw adapter recheck must have one row")
    row = rows[0]
    require(row["raw_input_status"] == "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW", "v35 raw input must be present")
    require(row["raw_rows_seen"] == "450", "v35 must see 450 raw rows")
    require(row["valid_raw_rows"] == "450", "v35 must validate 450 raw rows")
    require(row["raw_rows_imported_after_recheck"] == "0", "v35 must inherit zero raw imports")
    require("post_writer_raw_import_not_allowed" not in row["adapter_recheck_blockers"], "v35 must not block on v34 raw import")
    require("zero_raw_rows_imported_after_recheck" in row["adapter_recheck_blockers"], "v35 must block on zero raw rows")
    require("raw_adapter_input_not_present" not in row["adapter_recheck_blockers"], "v35 must not block on raw input")
    require(row["target_file_written_after_recheck"] == "false", "v35 must not write v12 target")
    require(row["real_values_input_may_exist_after_recheck"] == "true", "v35 must see v12 real values input")
    require(row["endpoint_scoring_allowed"] == "false", "v35 row cannot allow scoring")
    require(len(summary) == 1, "v35 summary must have one row")
    summary_row = summary[0]
    require(summary_row["overall_status"] == "POST_WRITER_RAW_ADAPTER_RECHECK_BLOCKED", "v35 summary must block")
    require(summary_row["raw_input_status"] == "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW", "v35 summary raw input mismatch")
    require(summary_row["valid_raw_rows"] == "450", "v35 summary must validate 450 rows")
    require(summary_row["target_file_written_after_recheck"] == "false", "v35 summary must not write target")
    require(summary_row["real_values_input_may_exist_after_recheck"] == "true", "v35 summary must see v12 real values")
    require(summary_row["endpoint_scoring_allowed_anywhere"] == "false", "v35 summary must forbid scoring")


def validate_post_writer_real_values_gate_recheck_v36() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_real_values_gate_recheck_v36.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_real_values_gate_recheck_summary_v36.csv")
    require(len(rows) == 18, "v36 real-values recheck must cover eighteen rows")
    require(all(row["v12_input_file_status"] == "REAL_VALUE_HEADER_OK" for row in rows), "v36 v12 input must be present")
    require(sum(int(row["v12_imported_numeric_rows"]) for row in rows) == 450, "v36 must import 450 numeric rows")
    require(
        all(row["v12_real_value_gate_status"] == "REAL_VALUES_PRESENT_VALIDATION_PENDING_LEAKAGE" for row in rows),
        "v36 gate status mismatch",
    )
    require(
        all("post_writer_raw_adapter_did_not_write_v12" not in row["real_value_recheck_blockers"] for row in rows),
        "v36 must not block on v35 no-write",
    )
    require(all(row["rows_passing_value_gate_after_recheck"] == "1" for row in rows), "v36 must pass eighteen rows")
    require(
        all(row["activation_decision_after_recheck"] == "VALUE_GATE_PASSED_PENDING_LEAKAGE" for row in rows),
        "v36 must pass value gate pending leakage",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v36 rows cannot allow scoring")
    require(len(summary) == 1, "v36 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "POST_WRITER_REAL_VALUES_GATE_RECHECK_READY", "v36 summary must be ready")
    require(row["real_value_recheck_rows"] == "18", "v36 must summarize eighteen rows")
    require(row["imported_numeric_rows_after_recheck"] == "450", "v36 must import 450 numeric rows")
    require(row["rows_passing_value_gate_after_recheck"] == "18", "v36 must pass eighteen rows")
    require(row["rows_activated_after_recheck"] == "0", "v36 must activate zero rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v36 summary must forbid scoring")


def validate_post_writer_leakage_audit_recheck_v37() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_leakage_audit_recheck_v37.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_leakage_audit_recheck_summary_v37.csv")
    require(len(rows) == 18, "v37 leakage recheck must cover eighteen rows")
    require(
        all(row["v09_leakage_status"] == "LEAKAGE_AUDIT_PASS" for row in rows),
        "v37 must inherit the passed v09 leakage status",
    )
    require(all(row["rows_passing_value_gate_after_recheck"] == "1" for row in rows), "v37 must pass value rows")
    require(
        all("post_writer_real_values_gate_not_passed" not in row["leakage_recheck_blockers"] for row in rows),
        "v37 must not block on the v36 value gate",
    )
    require(
        all("v09_leakage_audit_not_passed" not in row["leakage_recheck_blockers"] for row in rows),
        "v37 must clear the v09 leakage audit blocker",
    )
    require(all(row["leakage_pass_after_recheck"] == "true" for row in rows), "v37 must pass leakage")
    require(all(row["activation_allowed_after_recheck"] == "true" for row in rows), "v37 must allow activation handoff")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v37 rows cannot allow scoring")
    require(len(summary) == 1, "v37 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "POST_WRITER_LEAKAGE_AUDIT_RECHECK_V37", "v37 summary id mismatch")
    require(row["leakage_recheck_rows"] == "18", "v37 must summarize eighteen rows")
    require(row["leakage_pass_rows_after_recheck"] == "18", "v37 must pass eighteen leakage rows")
    require(row["leakage_blocked_rows_after_recheck"] == "0", "v37 must block zero leakage rows")
    require(row["activation_allowed_rows_after_recheck"] == "18", "v37 must allow eighteen activation handoffs")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v37 summary must forbid scoring")
    require(row["overall_status"] == "POST_WRITER_LEAKAGE_AUDIT_RECHECK_READY", "v37 summary must be ready")
    require(
        row["claim_boundary"] == "post_writer_leakage_audit_recheck_only_no_activation_no_scores_no_dark_sector_verdict",
        "v37 claim boundary mismatch",
    )


def validate_post_writer_scoring_activation_recheck_v38() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_scoring_activation_recheck_v38.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_scoring_activation_recheck_summary_v38.csv")
    require(len(rows) == 18, "v38 activation recheck must cover eighteen rows")
    require(all(row["v37_leakage_pass_after_recheck"] == "true" for row in rows), "v38 must inherit leakage passes")
    require(
        all(row["v37_activation_allowed_after_recheck"] == "true" for row in rows),
        "v38 must inherit activation handoff allowance",
    )
    require(all(row["v13_activation_decision"] == "ACTIVATE_FOR_SCORING" for row in rows), "v38 must inherit v13 row activation")
    require(
        all("post_writer_leakage_audit_not_passed" not in row["activation_recheck_blockers"] for row in rows),
        "v38 must clear the v37 leakage failure blocker",
    )
    require(
        all("post_writer_leakage_recheck_disallows_activation" not in row["activation_recheck_blockers"] for row in rows),
        "v38 must clear v37 activation denial",
    )
    require(
        all("v13_activation_gate_not_passed" not in row["activation_recheck_blockers"] for row in rows),
        "v38 must clear v13 activation gate",
    )
    require(all(row["activation_decision_after_recheck"] == "ACTIVATE_FOR_SCORING" for row in rows), "v38 must activate rows")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v38 rows cannot allow scoring")
    require(len(summary) == 1, "v38 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "POST_WRITER_SCORING_ACTIVATION_RECHECK_V38", "v38 summary id mismatch")
    require(row["activation_recheck_rows"] == "18", "v38 must summarize eighteen rows")
    require(row["rows_activated_after_recheck"] == "18", "v38 must activate eighteen rows")
    require(row["row_level_blocked_rows_after_recheck"] == "0", "v38 must block zero rows at row level")
    require(row["global_blockers_after_recheck"] == "0", "v38 must clear global blockers")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v38 summary must forbid scoring")
    require(row["overall_status"] == "POST_WRITER_SCORING_ACTIVATION_RECHECK_READY", "v38 summary must be ready")
    require(
        row["claim_boundary"] == "post_writer_scoring_activation_recheck_only_no_activation_no_scores_no_dark_sector_verdict",
        "v38 claim boundary mismatch",
    )


def validate_post_writer_scoring_preflight_recheck_v39() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_scoring_preflight_recheck_v39.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_scoring_preflight_recheck_summary_v39.csv")
    require(len(rows) == 6, "v39 preflight recheck must cover six requirements")
    require(
        sum(row["v07_current_status"].startswith("BLOCKED") for row in rows) == 0,
        "v39 must inherit zero blocked v07 requirements",
    )
    require(all(row["v38_rows_activated_after_recheck"] == "18" for row in rows), "v39 must inherit eighteen activated rows")
    require(
        all("v07_requirement_blocked" not in row["preflight_recheck_blockers"] for row in rows),
        "v39 must not block on v07 requirements after preflight clears",
    )
    require(
        all("post_writer_activation_recheck_zero_rows" not in row["preflight_recheck_blockers"] for row in rows),
        "v39 must clear zero-row activation blocker",
    )
    require(
        all("post_writer_activation_recheck_scoring_not_allowed" in row["preflight_recheck_blockers"] for row in rows),
        "v39 must block on scoring denial",
    )
    require(
        all(row["preflight_requirement_status_after_recheck"] == "BLOCKED" for row in rows),
        "v39 requirements must remain blocked",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v39 rows cannot allow scoring")
    require(len(summary) == 1, "v39 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "POST_WRITER_SCORING_PREFLIGHT_RECHECK_V39", "v39 summary id mismatch")
    require(row["preflight_requirement_rows"] == "6", "v39 must summarize six requirements")
    require(row["blocked_requirements_after_recheck"] == "6", "v39 must block six requirements")
    require(row["ready_requirements_after_recheck"] == "0", "v39 must ready zero requirements")
    require(row["formula_policy_components_ready_not_run"] == "7", "v39 must preserve seven policy components")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v39 summary must forbid scoring")
    require(row["overall_status"] == "POST_WRITER_SCORING_PREFLIGHT_RECHECK_BLOCKED", "v39 summary must block")
    require(
        row["claim_boundary"] == "post_writer_scoring_preflight_recheck_only_no_scores_no_dark_sector_verdict",
        "v39 claim boundary mismatch",
    )


def validate_post_writer_scoring_dependency_closure_recheck_v40() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_scoring_dependency_closure_recheck_v40.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_scoring_dependency_closure_recheck_summary_v40.csv")
    require(len(rows) == 13, "v40 dependency recheck must cover thirteen dependencies")
    require(sum(row["v24_dependency_decision"] == "READY" for row in rows) == 13, "v40 must inherit thirteen ready v24 dependencies")
    require(sum(row["v24_dependency_decision"] == "BLOCKED" for row in rows) == 0, "v40 must inherit zero blocked v24 dependencies")
    require(all(row["v39_ready_requirements_after_recheck"] == "0" for row in rows), "v40 must inherit zero ready requirements")
    require(
        all(
            ("v24_dependency_not_ready" in row["dependency_recheck_blockers"])
            == (row["v24_dependency_decision"] != "READY")
            for row in rows
        ),
        "v40 must only flag v24 blockers for non-ready dependencies",
    )
    require(
        all("post_writer_preflight_recheck_zero_ready_requirements" in row["dependency_recheck_blockers"] for row in rows),
        "v40 must block on zero ready preflight requirements",
    )
    require(
        all("post_writer_preflight_recheck_scoring_not_allowed" in row["dependency_recheck_blockers"] for row in rows),
        "v40 must block on preflight scoring denial",
    )
    require(
        all(row["dependency_decision_after_recheck"] == "BLOCKED" for row in rows),
        "v40 dependencies must remain blocked",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v40 rows cannot allow scoring")
    require(len(summary) == 1, "v40 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "POST_WRITER_SCORING_DEPENDENCY_CLOSURE_RECHECK_V40", "v40 summary id mismatch")
    require(row["dependencies_rechecked"] == "13", "v40 must summarize thirteen dependencies")
    require(row["ready_dependencies_after_recheck"] == "0", "v40 must ready zero dependencies")
    require(row["blocked_dependencies_after_recheck"] == "13", "v40 must block thirteen dependencies")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v40 summary must forbid scoring")
    require(row["overall_status"] == "POST_WRITER_SCORING_DEPENDENCY_CLOSURE_RECHECK_BLOCKED", "v40 summary must block")
    require(
        row["claim_boundary"] == "post_writer_scoring_dependency_closure_recheck_only_no_scores_no_dark_sector_verdict",
        "v40 claim boundary mismatch",
    )


def validate_post_writer_scoring_unblock_priority_recheck_v41() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_scoring_unblock_priority_recheck_v41.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_scoring_unblock_priority_recheck_summary_v41.csv")
    require(len(rows) == 13, "v41 priority recheck must cover thirteen rows")
    require(all(row["v40_ready_dependencies_after_recheck"] == "0" for row in rows), "v41 must inherit zero ready dependencies")
    require(
        all("v25_priority_dependency_blocked" not in row["priority_recheck_blockers"] for row in rows),
        "v41 must not flag v25 dependency blockers after v25 frontier clears",
    )
    require(
        all("post_writer_dependency_recheck_zero_ready_dependencies" in row["priority_recheck_blockers"] for row in rows),
        "v41 must block on zero ready dependencies",
    )
    require(
        all("post_writer_dependency_recheck_scoring_not_allowed" in row["priority_recheck_blockers"] for row in rows),
        "v41 must block on dependency scoring denial",
    )
    require(sum(row["frontier_now_after_recheck"] == "true" for row in rows) == 0, "v41 must mark zero frontier rows")
    frontier_rows = [row for row in rows if row["frontier_now_after_recheck"] == "true"]
    require(frontier_rows == [], "v41 frontier rows must be empty")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v41 rows cannot allow scoring")
    require(len(summary) == 1, "v41 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "POST_WRITER_SCORING_UNBLOCK_PRIORITY_RECHECK_V41", "v41 summary id mismatch")
    require(row["priority_rows_rechecked"] == "13", "v41 must summarize thirteen priority rows")
    require(row["blocked_priority_rows_after_recheck"] == "13", "v41 must block thirteen priority rows")
    require(row["frontier_now_rows_after_recheck"] == "0", "v41 must summarize zero frontier rows")
    require(row["first_frontier_dependency_after_recheck"] == "none", "v41 frontier dependency mismatch")
    require(
        row["first_frontier_artifact_after_recheck"] == "none",
        "v41 frontier artifact mismatch",
    )
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v41 summary must forbid scoring")
    require(row["overall_status"] == "POST_WRITER_SCORING_UNBLOCK_FRONTIER_CLEAR", "v41 summary must clear frontier")
    require(
        row["claim_boundary"] == "post_writer_scoring_unblock_priority_recheck_only_no_scores_no_dark_sector_verdict",
        "v41 claim boundary mismatch",
    )


def validate_post_writer_frontier_evidence_acceptance_recheck_v42() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_frontier_evidence_acceptance_recheck_v42.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_frontier_evidence_acceptance_recheck_summary_v42.csv")
    require(len(rows) == 18, "v42 frontier acceptance recheck must cover eighteen rows")
    require(all(row["v41_frontier_dependency"] == "none" for row in rows), "v42 must inherit no v41 frontier")
    require(
        all(row["v41_frontier_artifact"] == "none" for row in rows),
        "v42 must inherit the v41 frontier artifact",
    )
    require(all(row["v26_acceptance_status"] == "ACCEPTED_FOR_REVIEW" for row in rows), "v42 must inherit accepted v26 review")
    require(all(row["v26_evidence_input_present"] == "true" for row in rows), "v42 must see evidence inputs")
    require(all(row["v26_accepted_for_promotion_review"] == "true" for row in rows), "v42 must inherit accepted rows")
    require(
        all(row["acceptance_recheck_blockers"] == "post_writer_frontier_not_provenance_evidence" for row in rows),
        "v42 must bypass acceptance because the current frontier is raw input",
    )
    require(
        all(row["accepted_for_promotion_review_after_recheck"] == "false" for row in rows),
        "v42 must accept zero rows after recheck",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v42 rows cannot allow scoring")
    require(len(summary) == 1, "v42 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "POST_WRITER_FRONTIER_EVIDENCE_ACCEPTANCE_RECHECK_V42", "v42 summary id mismatch")
    require(row["acceptance_recheck_rows"] == "18", "v42 must summarize eighteen rows")
    require(row["evidence_input_rows_present_after_recheck"] == "18", "v42 must see eighteen evidence rows")
    require(row["accepted_for_promotion_review_rows_after_recheck"] == "0", "v42 must accept zero rows")
    require(row["blocked_rows_after_recheck"] == "18", "v42 must block eighteen rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v42 summary must forbid scoring")
    require(row["overall_status"] == "POST_WRITER_FRONTIER_EVIDENCE_ACCEPTANCE_RECHECK_BLOCKED", "v42 summary must block")
    require(
        row["claim_boundary"] == "post_writer_frontier_evidence_acceptance_recheck_only_no_scores_no_dark_sector_verdict",
        "v42 claim boundary mismatch",
    )


def validate_post_writer_frontier_work_order_recheck_v43() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_frontier_work_order_recheck_v43.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_frontier_work_order_recheck_summary_v43.csv")
    require(len(rows) == 18, "v43 work-order recheck must cover eighteen rows")
    require(
        all(row["v42_accepted_for_promotion_review_after_recheck"] == "false" for row in rows),
        "v43 must inherit zero accepted rows",
    )
    require(
        all(row["v27_work_order_status"] == "OPEN_EVIDENCE_COLLECTION_REQUIRED" for row in rows),
        "v43 must inherit open v27 work orders",
    )
    require(all(row["v27_may_write_evidence_input"] == "false" for row in rows), "v43 must inherit no-write v27 status")
    require(
        all("post_writer_frontier_acceptance_not_passed" in row["work_order_recheck_blockers"] for row in rows),
        "v43 must block on v42 acceptance",
    )
    require(
        all("v27_work_order_not_closed" in row["work_order_recheck_blockers"] for row in rows),
        "v43 must block on open v27 work orders",
    )
    require(
        all("v27_evidence_write_not_allowed" in row["work_order_recheck_blockers"] for row in rows),
        "v43 must block on v27 no-write",
    )
    require(
        all(row["work_order_status_after_recheck"] == "OPEN_EVIDENCE_COLLECTION_REQUIRED" for row in rows),
        "v43 work orders must remain open",
    )
    require(
        all(row["may_write_evidence_input_after_recheck"] == "false" for row in rows),
        "v43 must not authorize evidence writes",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v43 rows cannot allow scoring")
    require(len(summary) == 1, "v43 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "POST_WRITER_FRONTIER_WORK_ORDER_RECHECK_V43", "v43 summary id mismatch")
    require(row["work_order_recheck_rows"] == "18", "v43 must summarize eighteen rows")
    require(row["open_work_order_rows_after_recheck"] == "18", "v43 must keep eighteen work orders open")
    require(row["closed_work_order_rows_after_recheck"] == "0", "v43 must close zero work orders")
    require(row["may_write_evidence_input_rows_after_recheck"] == "0", "v43 must allow zero evidence writes")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v43 summary must forbid scoring")
    require(row["overall_status"] == "POST_WRITER_FRONTIER_WORK_ORDER_RECHECK_BLOCKED", "v43 summary must block")
    require(
        row["claim_boundary"] == "post_writer_frontier_work_order_recheck_only_no_evidence_no_scores_no_dark_sector_verdict",
        "v43 claim boundary mismatch",
    )


def validate_frontier_provenance_evidence_intake_contract_v44() -> None:
    rules = read_csv(ROOT / "data/derived/frontier_provenance_evidence_intake_contract_v44.csv")
    checklist = read_csv(ROOT / "data/derived/frontier_provenance_evidence_intake_checklist_v44.csv")
    summary = read_csv(ROOT / "data/derived/frontier_provenance_evidence_intake_contract_summary_v44.csv")
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
    require(len(rules) == 9, "v44 must define nine review rules")
    require({row["field_name"] for row in rules} == required_fields, "v44 review fields mismatch")
    require(
        all(row["target_evidence_file"] == "data/input/source_import_provenance_evidence_v21.csv" for row in rules),
        "v44 rules must target the frontier evidence file",
    )
    require(all(row["required_before_promotion"] == "true" for row in rules), "v44 rules must be required")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rules), "v44 rules cannot allow scoring")
    require(
        any("uses_rotation_residual_or_family_score" in row["reject_if"] for row in rules),
        "v44 must reject endpoint-score leakage routes",
    )
    require(len(checklist) == 18, "v44 checklist must cover eighteen rows")
    require(
        all(row["work_order_recheck_source"] == "data/derived/post_writer_frontier_work_order_recheck_v43.csv" for row in checklist),
        "v44 checklist must cite v43 work orders",
    )
    require(
        all(row["manual_collection_status"] == "READY_FOR_REVIEWED_SOURCE_COLLECTION" for row in checklist),
        "v44 checklist must be ready for reviewed collection",
    )
    require(all(row["may_copy_template_to_evidence_input"] == "true" for row in checklist), "v44 may allow template copying")
    require(all(row["may_mark_complete_without_review"] == "false" for row in checklist), "v44 cannot allow unreviewed completion")
    require(all(row["may_promote_after_contract_only"] == "false" for row in checklist), "v44 cannot promote by contract alone")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in checklist), "v44 checklist cannot allow scoring")
    require(len(summary) == 1, "v44 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "FRONTIER_PROVENANCE_EVIDENCE_INTAKE_CONTRACT_V44", "v44 summary id mismatch")
    require(row["target_evidence_file"] == "data/input/source_import_provenance_evidence_v21.csv", "v44 target mismatch")
    require(row["review_rule_rows"] == "9", "v44 must summarize nine review rules")
    require(row["row_checklist_rows"] == "18", "v44 must summarize eighteen checklist rows")
    require(row["manual_collection_ready_rows"] == "18", "v44 must ready eighteen manual collection rows")
    require(row["evidence_rows_created_by_contract"] == "0", "v44 must create zero evidence rows")
    require(row["promotion_allowed_by_contract_only"] == "false", "v44 cannot allow promotion by contract alone")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v44 summary must forbid scoring")
    require(row["overall_status"] == "FRONTIER_EVIDENCE_INTAKE_CONTRACT_READY_NOT_EVIDENCE", "v44 summary status mismatch")
    require(
        row["claim_boundary"] == "frontier_evidence_intake_contract_only_no_evidence_no_scores_no_dark_sector_verdict",
        "v44 claim boundary mismatch",
    )


def validate_frontier_provenance_source_candidate_ledger_v45() -> None:
    sources = read_csv(ROOT / "data/derived/frontier_provenance_source_candidate_ledger_v45.csv")
    coverage = read_csv(ROOT / "data/derived/frontier_provenance_source_candidate_coverage_v45.csv")
    summary = read_csv(ROOT / "data/derived/frontier_provenance_source_candidate_ledger_summary_v45.csv")
    require(len(sources) == 2, "v45 must define two source candidates")
    require({row["source_candidate_id"] for row in sources} == {"FPSC45_SPARC_TABLE1", "FPSC45_SPARC_MASSMODELS"}, "v45 source ids mismatch")
    require(all(row["catalog"] == "SPARC" for row in sources), "v45 sources must be SPARC")
    require(
        any(
            row["table_or_file"] == "SPARC_Lelli2016c.mrt"
            and row["sha256_or_external_accession"]
            == "sha256:5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243"
            for row in sources
        ),
        "v45 must record Table1 hash",
    )
    require(
        any(
            row["table_or_file"] == "MassModels_Lelli2016c.mrt"
            and row["sha256_or_external_accession"]
            == "sha256:9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c"
            for row in sources
        ),
        "v45 must record mass-model hash",
    )
    require(all(row["review_status"] == "SOURCE_CANDIDATE_READY_FOR_HUMAN_REVIEW" for row in sources), "v45 sources must be review-ready")
    require(all(row["may_write_v21_evidence_input"] == "false" for row in sources), "v45 cannot write v21 evidence")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in sources), "v45 sources cannot allow scoring")
    require(len(coverage) == 18, "v45 coverage must cover eighteen rows")
    require(
        all(row["primary_source_candidate_id"] == "FPSC45_SPARC_TABLE1" for row in coverage),
        "v45 coverage must use SPARC Table1 as primary candidate",
    )
    require(
        all(row["coverage_status"] == "CANDIDATE_ROW_IDENTIFIED_NOT_V21_EVIDENCE" for row in coverage),
        "v45 coverage rows must remain candidate-only",
    )
    require(all(row["may_mark_provenance_complete"] == "false" for row in coverage), "v45 cannot mark provenance complete")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in coverage), "v45 coverage cannot allow scoring")
    require(len(summary) == 1, "v45 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "FRONTIER_PROVENANCE_SOURCE_CANDIDATE_LEDGER_V45", "v45 summary id mismatch")
    require(row["source_candidate_rows"] == "2", "v45 must summarize two source candidates")
    require(row["ready_for_human_review_source_rows"] == "2", "v45 must have two review-ready candidates")
    require(row["coverage_rows"] == "18", "v45 must summarize eighteen coverage rows")
    require(row["candidate_rows_identified"] == "18", "v45 must identify eighteen candidate rows")
    require(row["v21_evidence_rows_created"] == "0", "v45 must create zero v21 evidence rows")
    require(row["may_write_v21_evidence_input_anywhere"] == "false", "v45 cannot write v21 evidence")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v45 summary must forbid scoring")
    require(row["overall_status"] == "FRONTIER_PROVENANCE_SOURCE_CANDIDATES_READY_NOT_EVIDENCE", "v45 summary status mismatch")
    require(
        row["claim_boundary"] == "frontier_provenance_source_candidate_ledger_only_no_evidence_no_scores_no_dark_sector_verdict",
        "v45 claim boundary mismatch",
    )


def validate_frontier_provenance_evidence_payload_draft_v46() -> None:
    draft = read_csv(ROOT / "data/derived/frontier_provenance_evidence_payload_draft_v46.csv")
    review = read_csv(ROOT / "data/derived/frontier_provenance_evidence_payload_draft_review_v46.csv")
    summary = read_csv(ROOT / "data/derived/frontier_provenance_evidence_payload_draft_summary_v46.csv")
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
    require(len(draft) == 18, "v46 draft must cover eighteen rows")
    require(set(draft[0].keys()) == required_fields, "v46 draft columns must match v21 columns")
    require(all(row["catalog"] == "SPARC" for row in draft), "v46 draft must use SPARC catalog")
    require(all(row["table_or_file"] == "SPARC_Lelli2016c.mrt" for row in draft), "v46 draft must use Table1")
    require(
        all(
            row["sha256_or_external_accession"]
            == "sha256:5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243"
            for row in draft
        ),
        "v46 draft must preserve Table1 hash",
    )
    require(
        all(row["provenance_evidence_status"] == "REVIEW_REQUIRED_NOT_COMPLETE" for row in draft),
        "v46 draft rows must require review",
    )
    require(len(review) == 18, "v46 review ledger must cover eighteen rows")
    require(all(row["review_required"] == "true" for row in review), "v46 review rows must require review")
    require(all(row["may_copy_to_v21_after_review"] == "false" for row in review), "v46 cannot copy before review")
    require(all(row["may_mark_complete_without_review"] == "false" for row in review), "v46 cannot allow unreviewed completion")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in review), "v46 review rows cannot allow scoring")
    require(len(summary) == 1, "v46 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "FRONTIER_PROVENANCE_EVIDENCE_PAYLOAD_DRAFT_V46", "v46 summary id mismatch")
    require(row["draft_rows"] == "18", "v46 must summarize eighteen draft rows")
    require(row["draft_rows_requiring_review"] == "18", "v46 must require review for eighteen rows")
    require(row["complete_evidence_rows"] == "0", "v46 must have zero complete evidence rows")
    require(row["v21_evidence_rows_created"] == "0", "v46 must create zero v21 evidence rows")
    require(row["may_copy_to_v21_without_review"] == "false", "v46 cannot copy without review")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v46 summary must forbid scoring")
    require(row["overall_status"] == "FRONTIER_EVIDENCE_PAYLOAD_DRAFT_READY_REVIEW_REQUIRED", "v46 summary status mismatch")
    require(
        row["claim_boundary"] == "frontier_provenance_evidence_payload_draft_only_no_v21_write_no_scores_no_dark_sector_verdict",
        "v46 claim boundary mismatch",
    )


def validate_frontier_provenance_review_package_v47() -> None:
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
    require(package_root.exists(), "v47 review package directory must exist")
    require(zip_path.exists(), "v47 review package zip must exist")
    for rel in required:
        require((package_root / rel).exists(), f"v47 package missing {rel}")
    manifest = read_csv(package_root / "REVIEW_MANIFEST.csv")
    require(len(manifest) == len(required) - 1, "v47 manifest row count mismatch")
    manifest_paths = {row["package_path"] for row in manifest}
    require(required - {"REVIEW_MANIFEST.csv"} == manifest_paths, "v47 manifest paths mismatch")
    require(all(row["claim_boundary"] == "review_package_only_no_evidence_no_scores" for row in manifest), "v47 claim boundary mismatch")
    draft = read_csv(package_root / "data/frontier_provenance_evidence_payload_draft_v46.csv")
    require(len(draft) == 18, "v47 packaged draft must have eighteen rows")
    require(
        all(row["provenance_evidence_status"] == "REVIEW_REQUIRED_NOT_COMPLETE" for row in draft),
        "v47 packaged draft must remain review-required",
    )
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    zipped_required = {f"frontier_provenance_v46_review_package/{rel}" for rel in required}
    require(zipped_required.issubset(names), "v47 zip missing required package files")


def validate_frontier_provenance_review_response_intake_v48() -> None:
    rows = read_csv(ROOT / "data/derived/frontier_provenance_review_response_intake_v48.csv")
    summary = read_csv(ROOT / "data/derived/frontier_provenance_review_response_intake_summary_v48.csv")
    response_dir = ROOT / "review_packages/frontier_provenance_v46_completed_review_response"
    response_zip = ROOT / "review_packages/frontier_provenance_v46_completed_review_response.zip"
    required = {
        "frontier_provenance_v46_review_response.csv",
        "frontier_provenance_v46_review_completed_summary.csv",
        "frontier_provenance_v46_review_notes.md",
        "frontier_provenance_v46_review_validation_log.txt",
    }
    require(response_zip.exists(), "v48 response zip must exist")
    require(response_dir.exists(), "v48 extracted response directory must exist")
    for rel in required:
        require((response_dir / rel).exists(), f"v48 response missing {rel}")
    with zipfile.ZipFile(response_zip) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    require(required.issubset(names), "v48 response zip missing required files")
    require(len(rows) == 18, "v48 response must cover eighteen rows")
    require(all(row["row_route_internal_consistency"] == "pass" for row in rows), "v48 route consistency must pass")
    require(
        all(row["source_hash_route_status"] == "source_hash_matches_package_candidate_ledger_external_sha_not_recomputed" for row in rows),
        "v48 source hash status must preserve external hash caveat",
    )
    require(
        all(row["leakage_evidence_status"] == "pass_prescore_source_route_review_id" for row in rows),
        "v48 leakage route review ids must pass",
    )
    require(
        all(row["reviewer_decision"] == "KEEP_REVIEW_REQUIRED_NOT_COMPLETE_NO_V21_WRITE" for row in rows),
        "v48 rows must remain review-required and not complete",
    )
    require(all(row["may_copy_to_v21_after_review"] == "false" for row in rows), "v48 cannot copy to v21")
    require(all(row["may_mark_provenance_complete"] == "false" for row in rows), "v48 cannot mark provenance complete")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v48 cannot allow scoring")
    require(len(summary) == 1, "v48 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "FRONTIER_PROVENANCE_REVIEW_RESPONSE_INTAKE_V48", "v48 summary id mismatch")
    require(row["response_files_present"] == "4", "v48 must record four response files")
    require(row["review_rows"] == "18", "v48 must summarize eighteen review rows")
    require(row["route_and_prescore_pass_rows"] == "18", "v48 must summarize eighteen route/prescore passes")
    require(row["review_decision"] == "ACCEPT_AS_REVIEW_READY_DRAFT_ONLY_NOT_PROMOTED", "v48 review decision mismatch")
    require(row["completion_status"] == "PASS_WITH_CAVEAT", "v48 must preserve caveated pass")
    require(row["external_hash_recomputed"] == "false", "v48 must preserve external hash recomputation caveat")
    require(row["complete_evidence_rows_authorized"] == "0", "v48 cannot authorize complete evidence rows")
    require(row["v21_evidence_rows_created"] == "0", "v48 cannot create v21 evidence rows")
    require(row["may_copy_to_v21_without_separate_promotion"] == "false", "v48 cannot copy without promotion gate")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v48 summary must forbid scoring")
    require(row["overall_status"] == "REVIEW_RESPONSE_ACCEPTED_AS_DRAFT_ONLY_NOT_PROMOTED", "v48 summary status mismatch")
    require(
        row["claim_boundary"] == "frontier_provenance_review_response_intake_only_no_v21_write_no_scores_no_dark_sector_verdict",
        "v48 claim boundary mismatch",
    )


def validate_frontier_review_promotion_gate_v49() -> None:
    rows = read_csv(ROOT / "data/derived/frontier_review_promotion_gate_v49.csv")
    summary = read_csv(ROOT / "data/derived/frontier_review_promotion_gate_summary_v49.csv")
    require(len(rows) == 18, "v49 gate must cover eighteen review rows")
    require(all(row["v48_route_consistency"] == "pass" for row in rows), "v49 must preserve v48 route pass")
    require(
        all(row["v48_source_hash_route_status"] == "source_hash_matches_package_candidate_ledger_external_sha_not_recomputed" for row in rows),
        "v49 must preserve external source hash caveat",
    )
    require(
        all(row["v48_leakage_evidence_status"] == "pass_prescore_source_route_review_id" for row in rows),
        "v49 must preserve v48 prescore route pass",
    )
    require(
        all(row["v48_reviewer_decision"] == "KEEP_REVIEW_REQUIRED_NOT_COMPLETE_NO_V21_WRITE" for row in rows),
        "v49 reviewer decisions must remain not promoted",
    )
    require(all(row["v48_completion_status"] == "PASS_WITH_CAVEAT" for row in rows), "v49 must preserve caveated status")
    require(all(row["external_hash_recomputed"] == "false" for row in rows), "v49 must preserve hash recomputation caveat")
    require(
        all("external_source_hash_not_independently_recomputed" in row["promotion_gate_blockers"] for row in rows),
        "v49 must block on external hash recomputation",
    )
    require(
        all("reviewer_decision_keeps_review_required_not_complete" in row["promotion_gate_blockers"] for row in rows),
        "v49 must block on reviewer not-promoted decision",
    )
    require(all(row["promotion_gate_decision"] == "DO_NOT_PROMOTE_TO_V21_EVIDENCE" for row in rows), "v49 cannot promote rows")
    require(all(row["may_write_v21_evidence_input_after_gate"] == "false" for row in rows), "v49 cannot write v21 evidence")
    require(
        all(row["may_mark_provenance_complete_after_gate"] == "false" for row in rows),
        "v49 cannot mark provenance complete",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v49 cannot allow scoring")
    require(len(summary) == 1, "v49 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "FRONTIER_REVIEW_PROMOTION_GATE_V49", "v49 summary id mismatch")
    require(row["review_rows"] == "18", "v49 must summarize eighteen rows")
    require(row["promotion_allowed_rows"] == "0", "v49 cannot allow promotion")
    require(row["promotion_blocked_rows"] == "18", "v49 must block all rows")
    require(row["v21_evidence_rows_created"] == "0", "v49 cannot create v21 evidence")
    require(row["provenance_complete_rows_marked"] == "0", "v49 cannot mark provenance complete")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v49 summary must forbid scoring")
    require(row["overall_status"] == "FRONTIER_REVIEW_PROMOTION_BLOCKED", "v49 summary status mismatch")
    require(
        row["next_required_action"] == "independently_recompute_external_sparc_hash_and_issue_explicit_promotion_authorization",
        "v49 next action mismatch",
    )
    require(
        row["claim_boundary"] == "frontier_review_promotion_gate_only_no_evidence_no_scores_no_dark_sector_verdict",
        "v49 claim boundary mismatch",
    )


def validate_frontier_external_hash_recompute_audit_v50() -> None:
    rows = read_csv(ROOT / "data/derived/frontier_external_hash_recompute_audit_v50.csv")
    summary = read_csv(ROOT / "data/derived/frontier_external_hash_recompute_audit_summary_v50.csv")
    require(len(rows) == 2, "v50 must audit two SPARC source candidates")
    expected = {
        "FPSC45_SPARC_TABLE1": ("SPARC_Lelli2016c.mrt", "5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243"),
        "FPSC45_SPARC_MASSMODELS": ("MassModels_Lelli2016c.mrt", "9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c"),
    }
    by_id = {row["source_candidate_id"]: row for row in rows}
    require(set(by_id) == set(expected), "v50 source ids mismatch")
    for source_id, (table, digest) in expected.items():
        row = by_id[source_id]
        require(row["table_or_file"] == table, f"v50 table mismatch for {source_id}")
        require(row["expected_sha256"] == digest, f"v50 expected hash mismatch for {source_id}")
        require(row["recomputed_sha256"] == digest, f"v50 recomputed hash mismatch for {source_id}")
        require(int(row["file_size_bytes"]) > 0, f"v50 file size missing for {source_id}")
        require(row["source_access_status"] == "LIVE_DOWNLOAD_CACHED_FOR_HASH_AUDIT", f"v50 access status mismatch for {source_id}")
        require(row["hash_recompute_status"] == "EXTERNAL_HASH_RECOMPUTED_MATCHED", f"v50 hash not matched for {source_id}")
        require(row["may_promote_v21_by_hash_alone"] == "false", "v50 hash alone cannot promote v21")
        require(row["endpoint_scoring_allowed"] == "false", "v50 cannot allow scoring")
    require(len(summary) == 1, "v50 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "FRONTIER_EXTERNAL_HASH_RECOMPUTE_AUDIT_V50", "v50 summary id mismatch")
    require(row["source_candidate_rows"] == "2", "v50 must summarize two sources")
    require(row["hash_recomputed_matched_rows"] == "2", "v50 must match both hashes")
    require(row["primary_table1_hash_recomputed_matched"] == "true", "v50 primary table hash must match")
    require(row["v21_evidence_rows_created"] == "0", "v50 cannot create v21 evidence")
    require(row["provenance_complete_rows_marked"] == "0", "v50 cannot mark provenance complete")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v50 summary must forbid scoring")
    require(row["overall_status"] == "FRONTIER_EXTERNAL_HASH_RECOMPUTED_MATCHED", "v50 status mismatch")
    require(
        row["claim_boundary"] == "frontier_external_hash_recompute_audit_only_no_evidence_no_scores_no_dark_sector_verdict",
        "v50 claim boundary mismatch",
    )


def validate_post_hash_frontier_review_promotion_recheck_v51() -> None:
    rows = read_csv(ROOT / "data/derived/post_hash_frontier_review_promotion_recheck_v51.csv")
    summary = read_csv(ROOT / "data/derived/post_hash_frontier_review_promotion_recheck_summary_v51.csv")
    require(len(rows) == 18, "v51 must cover eighteen review rows")
    require(all(row["primary_table1_hash_recomputed_matched"] == "true" for row in rows), "v51 primary hash must be matched")
    require(
        all(row["v48_reviewer_decision"] == "KEEP_REVIEW_REQUIRED_NOT_COMPLETE_NO_V21_WRITE" for row in rows),
        "v51 must preserve v48 reviewer decision",
    )
    require(
        all("primary_table1_hash_not_recomputed_matched" not in row["promotion_recheck_blockers"] for row in rows),
        "v51 must close the hash blocker",
    )
    require(
        all("explicit_promotion_authorization_missing" in row["promotion_recheck_blockers"] for row in rows),
        "v51 must block on explicit promotion authorization",
    )
    require(all(row["promotion_recheck_decision"] == "DO_NOT_PROMOTE_TO_V21_EVIDENCE" for row in rows), "v51 cannot promote")
    require(all(row["may_write_v21_evidence_input_after_recheck"] == "false" for row in rows), "v51 cannot write v21 evidence")
    require(
        all(row["may_mark_provenance_complete_after_recheck"] == "false" for row in rows),
        "v51 cannot mark provenance complete",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v51 cannot allow scoring")
    require(len(summary) == 1, "v51 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "POST_HASH_FRONTIER_REVIEW_PROMOTION_RECHECK_V51", "v51 summary id mismatch")
    require(row["review_rows"] == "18", "v51 must summarize eighteen rows")
    require(row["primary_hash_matched_review_rows"] == "18", "v51 must match primary hash for all rows")
    require(row["promotion_allowed_rows_after_hash"] == "0", "v51 cannot allow promotion")
    require(row["promotion_blocked_rows_after_hash"] == "18", "v51 must keep all rows blocked")
    require(row["v21_evidence_rows_created"] == "0", "v51 cannot create v21 evidence")
    require(row["provenance_complete_rows_marked"] == "0", "v51 cannot mark provenance complete")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v51 summary must forbid scoring")
    require(row["overall_status"] == "POST_HASH_FRONTIER_REVIEW_PROMOTION_RECHECK_BLOCKED", "v51 status mismatch")
    require(
        row["next_required_action"] == "issue_explicit_review_promotion_authorization_for_v21_copy_and_provenance_completion",
        "v51 next action mismatch",
    )
    require(
        row["claim_boundary"] == "post_hash_frontier_review_promotion_recheck_only_no_evidence_no_scores_no_dark_sector_verdict",
        "v51 claim boundary mismatch",
    )


def validate_post_hash_review_promotion_package_v52() -> None:
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
    require(package_root.exists(), "v52 review package directory must exist")
    require(zip_path.exists(), "v52 review package zip must exist")
    for rel in required:
        require((package_root / rel).exists(), f"v52 package missing {rel}")
    manifest = read_csv(package_root / "REVIEW_MANIFEST.csv")
    require(len(manifest) == len(required) - 1, "v52 manifest row count mismatch")
    manifest_paths = {row["package_path"] for row in manifest}
    require(required - {"REVIEW_MANIFEST.csv"} == manifest_paths, "v52 manifest paths mismatch")
    require(
        all(row["claim_boundary"] == "post_hash_review_promotion_package_only_no_evidence_no_scores" for row in manifest),
        "v52 claim boundary mismatch",
    )
    template = read_csv(package_root / "templates/frontier_review_promotion_authorization_TEMPLATE.csv")
    require(len(template) == 18, "v52 authorization template must cover eighteen rows")
    require(
        all(row["primary_table1_hash_recomputed_matched"] == "true" for row in template),
        "v52 template must preserve primary hash support",
    )
    require(
        all(row["reviewer_promotion_decision"] == "KEEP_REVIEW_REQUIRED_NOT_COMPLETE_NO_V21_WRITE" for row in template),
        "v52 template must default to no promotion",
    )
    require(
        all(row["may_copy_to_v21_after_authorization"] == "false" for row in template),
        "v52 template cannot default to v21 copy",
    )
    require(
        all(row["may_mark_provenance_complete_after_authorization"] == "false" for row in template),
        "v52 template cannot default to provenance completion",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in template), "v52 template cannot allow scoring")
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    zipped_required = {f"frontier_post_hash_review_promotion_v51_review_package/{rel}" for rel in required}
    require(zipped_required.issubset(names), "v52 zip missing required package files")


def validate_post_hash_review_promotion_response_intake_v53() -> None:
    rows = read_csv(ROOT / "data/derived/post_hash_review_promotion_response_intake_v53.csv")
    summary = read_csv(ROOT / "data/derived/post_hash_review_promotion_response_intake_summary_v53.csv")
    response_dir = ROOT / "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response"
    response_zip = ROOT / "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response.zip"
    required = {
        "frontier_post_hash_review_promotion_v51_authorization_response.csv",
        "frontier_post_hash_review_promotion_v51_completed_summary.csv",
        "frontier_post_hash_review_promotion_v51_review_notes.md",
        "frontier_post_hash_review_promotion_v51_validation_log.txt",
    }
    require(response_zip.exists(), "v53 response zip must exist")
    require(response_dir.exists(), "v53 extracted response directory must exist")
    for rel in required:
        require((response_dir / rel).exists(), f"v53 response missing {rel}")
    with zipfile.ZipFile(response_zip) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    require(required.issubset(names), "v53 response zip missing required files")
    require(len(rows) == 18, "v53 response must cover eighteen rows")
    require(all(row["primary_table1_hash_recomputed_matched"] == "true" for row in rows), "v53 must preserve hash support")
    require(all(row["reviewer_promotion_decision"] == "PROMOTE_TO_COMPLETE_V21_EVIDENCE" for row in rows), "v53 must promote all rows")
    require(all(row["may_copy_to_v21_after_authorization"] == "true" for row in rows), "v53 must authorize v21 copy")
    require(
        all(row["may_mark_provenance_complete_after_authorization"] == "true" for row in rows),
        "v53 must authorize provenance completion",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v53 cannot allow scoring")
    require(len(summary) == 1, "v53 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "POST_HASH_REVIEW_PROMOTION_RESPONSE_INTAKE_V53", "v53 summary id mismatch")
    require(row["response_files_present"] == "4", "v53 must record four response files")
    require(row["review_rows"] == "18", "v53 must summarize eighteen rows")
    require(row["promote_to_complete_v21_evidence_rows"] == "18", "v53 must promote eighteen rows")
    require(row["copy_to_v21_authorized_rows"] == "18", "v53 must authorize eighteen copy rows")
    require(row["provenance_complete_authorized_rows"] == "18", "v53 must authorize eighteen complete rows")
    require(row["primary_hash_matched_rows"] == "18", "v53 must preserve eighteen hash matches")
    require(row["source_decision"] == "AUTHORIZE_PROMOTION_FOR_LATER_INGESTION_GATE_ONLY", "v53 source decision mismatch")
    require(row["v21_evidence_rows_created_by_response"] == "0", "v53 response itself cannot create v21 rows")
    require(row["provenance_complete_rows_marked_by_response"] == "0", "v53 response itself cannot mark complete")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v53 summary must forbid scoring")
    require(
        row["overall_status"] == "POST_HASH_REVIEW_PROMOTION_AUTHORIZATION_ACCEPTED_FOR_INGESTION",
        "v53 status mismatch",
    )
    require(
        row["claim_boundary"] == "post_hash_review_promotion_response_intake_only_no_v21_write_no_scores_no_dark_sector_verdict",
        "v53 claim boundary mismatch",
    )


def validate_authorized_provenance_evidence_payload_v54() -> None:
    rows = read_csv(ROOT / "data/derived/authorized_provenance_evidence_payload_v54.csv")
    summary = read_csv(ROOT / "data/derived/authorized_provenance_evidence_payload_summary_v54.csv")
    require(len(rows) == 18, "v54 payload must cover eighteen rows")
    require(all(row["catalog"] == "SPARC" for row in rows), "v54 payload must use SPARC")
    require(all(row["table_or_file"] == "SPARC_Lelli2016c.mrt" for row in rows), "v54 payload must use SPARC Table1")
    require(
        all(row["provenance_evidence_status"] == "PROVENANCE_EVIDENCE_COMPLETE" for row in rows),
        "v54 payload rows must be complete",
    )
    require(
        all(row["payload_write_status"] == "READY_FOR_SEPARATE_ACTIVE_V21_WRITE_GATE" for row in rows),
        "v54 rows must be ready for a separate active write gate",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v54 cannot allow scoring")
    require(len(summary) == 1, "v54 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "AUTHORIZED_PROVENANCE_EVIDENCE_PAYLOAD_V54", "v54 summary id mismatch")
    require(row["payload_rows"] == "18", "v54 must summarize eighteen rows")
    require(row["complete_provenance_payload_rows"] == "18", "v54 must have eighteen complete payload rows")
    require(row["ready_for_active_v21_write_rows"] == "18", "v54 must have eighteen ready rows")
    require(row["active_v21_target"] == "data/input/source_import_provenance_evidence_v21.csv", "v54 target mismatch")
    require(row["active_v21_target_present"] == "true", "v54 must detect active target")
    require(row["active_v21_rows_written_by_this_step"] == "0", "v54 must write zero active rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v54 summary must forbid scoring")
    require(row["overall_status"] == "AUTHORIZED_PROVENANCE_EVIDENCE_PAYLOAD_READY_NOT_ACTIVE_INPUT", "v54 status mismatch")
    require(
        row["claim_boundary"] == "authorized_provenance_evidence_payload_only_no_active_input_no_scores_no_dark_sector_verdict",
        "v54 claim boundary mismatch",
    )


def validate_active_v21_provenance_evidence_writer_v55() -> None:
    rows = read_csv(ROOT / "data/input/source_import_provenance_evidence_v21.csv")
    summary = read_csv(ROOT / "data/derived/active_v21_provenance_evidence_writer_summary_v55.csv")
    require(len(rows) == 18, "v55 active input must contain eighteen rows")
    require(all(row["catalog"] == "SPARC" for row in rows), "v55 active input must use SPARC")
    require(all(row["table_or_file"] == "SPARC_Lelli2016c.mrt" for row in rows), "v55 active input must use Table1")
    require(
        all(row["provenance_evidence_status"] == "PROVENANCE_EVIDENCE_COMPLETE" for row in rows),
        "v55 active input rows must be complete",
    )
    require(len(summary) == 1, "v55 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "ACTIVE_V21_PROVENANCE_EVIDENCE_WRITER_V55", "v55 summary id mismatch")
    require(row["rows_written"] == "18", "v55 must write eighteen rows")
    require(row["complete_provenance_rows_written"] == "18", "v55 must write eighteen complete rows")
    require(row["target_file_written"] == "true", "v55 target must be written")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v55 cannot allow scoring")
    require(row["overall_status"] == "ACTIVE_V21_PROVENANCE_EVIDENCE_WRITTEN", "v55 status mismatch")
    require(
        row["claim_boundary"] == "active_v21_provenance_evidence_writer_only_no_observed_values_no_scores_no_dark_sector_verdict",
        "v55 claim boundary mismatch",
    )


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
    validate_leakage_audit_evidence_template_v58()
    validate_leakage_audit_review_package_v59()
    validate_leakage_audit_review_response_intake_v60()
    validate_leakage_prescore_artifact_work_order_v61()
    validate_leakage_prescore_artifact_collection_package_v62()
    validate_leakage_prescore_artifact_collection_intake_v63()
    validate_leakage_prescore_artifact_request_ledger_v64()
    validate_leakage_prescore_artifact_request_review_package_v65()
    validate_leakage_prescore_artifact_request_review_intake_v66()
    validate_leakage_prescore_artifact_candidate_ledger_v67()
    validate_leakage_prescore_artifact_candidate_review_package_v68()
    validate_leakage_prescore_artifact_candidate_review_intake_v69()
    validate_leakage_evidence_candidate_ingestion_gate_v70()
    validate_leakage_partial_candidate_sufficiency_review_package_v71()
    validate_leakage_partial_candidate_sufficiency_review_intake_v73()
    validate_leakage_partial_candidate_sufficiency_preaudit_v74()
    validate_leakage_partial_candidate_sufficiency_response_draft_v75()
    validate_full_leakage_evidence_ingestion_gate_v76()
    validate_leakage_audit_evidence_v10_writer_v77()
    validate_leakage_audit_pass_review_gate_v78()
    validate_source_import_values_v11()
    validate_source_import_real_values_gate_v12()
    validate_scoring_row_activation_policy_v79()
    validate_m0_no_dark_rule_parent_assumption_basis_v14()
    validate_m0_no_dark_rule_selection_map_v14()
    validate_m0_no_dark_rule_term_generation_record_v14()
    validate_m0_no_dark_rule_invariance_null_checks_v14()
    validate_m0_no_dark_rule_dimensional_precheck_v14()
    validate_m0_no_dark_rule_derivation_provenance_leakage_v14()
    validate_m0_no_dark_expression_rule_derivation_contract_v13()
    validate_m0_no_dark_expression_source_basis_v13()
    validate_m0_no_dark_expression_admissibility_rule_v13()
    validate_m0_no_dark_expression_null_fallback_policy_v13()
    validate_m0_no_dark_expression_output_class_v13()
    validate_m0_no_dark_expression_source_rule_leakage_audit_v13()
    validate_m0_no_dark_expression_source_rule_contract_v12()
    validate_m0_no_dark_expression_symbolic_form_v12()
    validate_m0_no_dark_expression_input_domain_v12()
    validate_m0_no_dark_expression_coefficient_freeze_v12()
    validate_m0_no_dark_expression_dimensional_audit_v12()
    validate_m0_no_dark_expression_machine_form_v12()
    validate_m0_no_dark_frozen_expression_contract_v11()
    validate_m0_no_dark_kernel_expression_interface_v10()
    validate_m0_no_dark_frozen_expression_statement_contract_v12()
    validate_m0_no_dark_source_side_expression_statement_v13()
    validate_m0_no_dark_statement_term_list_v13()
    validate_m0_no_dark_statement_argument_signature_v13()
    validate_m0_no_dark_statement_constraint_guards_v13()
    validate_m0_no_dark_statement_pre_dimensional_proof_v13()
    validate_m0_no_dark_statement_freeze_provenance_v13()
    validate_m0_no_dark_frozen_expression_payload_contract_v11()
    validate_m0_no_dark_payload_symbol_binding_table_v12()
    validate_m0_no_dark_payload_constant_policy_v12()
    validate_m0_no_dark_payload_dimensional_trace_v12()
    validate_m0_no_dark_payload_machine_form_v12()
    validate_m0_no_dark_payload_leakage_certificate_v12()
    validate_m0_no_dark_frozen_expression_body_v14()
    validate_m0_no_dark_kernel_expression_contract_v10()
    validate_m0_no_dark_equation_kernel_interface_v09()
    validate_m0_no_dark_equation_kernel_contract_v09()
    validate_m0_no_dark_readout_equation_interface_v08()
    validate_m0_no_dark_readout_equation_contract_v08()
    validate_m0_no_dark_formula_body_interface_v08()
    validate_m0_no_dark_formula_body_contract_v07()
    validate_m0_no_dark_scale_policy_v07()
    validate_m0_no_dark_fallback_policy_v07()
    validate_m0_no_dark_formula_table_contract_v06()
    validate_family_prediction_tables_v08()
    validate_family_prediction_comparability_v09()
    validate_m0_no_dark_prediction_row_writer_v08()
    validate_m0_no_dark_executable_prediction_kernel_v08()
    validate_m0_no_dark_velocity_readout_formula_v08()
    validate_m0_no_dark_source_to_rotation_equation_body_v08()
    validate_m0_no_dark_source_to_velocity_coupling_rule_v08()
    validate_m0_no_dark_velocity_unit_lift_rule_v08()
    validate_m0_no_dark_velocity_dimension_anchor_rule_v08()
    validate_m0_no_dark_velocity_anchor_source_law_v08()
    validate_m0_no_dark_velocity_anchor_candidate_basis_v08()
    validate_m0_no_dark_velocity_anchor_selection_rule_v08()
    validate_m0_no_dark_velocity_anchor_value_freeze_v08()
    validate_m0_no_dark_velocity_anchor_unit_normalization_v08()
    validate_m0_no_dark_velocity_anchor_component_combination_rule_v08()
    validate_m0_no_dark_velocity_anchor_component_weight_policy_v08()
    validate_m0_no_dark_velocity_anchor_component_weight_value_freeze_v08()
    validate_m0_no_dark_velocity_anchor_combined_anchor_rule_v08()
    validate_m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08()
    validate_m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08()
    validate_m0_no_dark_velocity_readout_formula_body_freeze_v08()
    validate_m0_no_dark_prediction_row_value_freeze_v08()
    validate_m0_no_dark_family_prediction_row_emission_v08()
    validate_m0_label_rule_table_v06()
    validate_m1_tau_response_formula_table_v06()
    validate_m1_admissibility_table_v06()
    validate_m1_response_parameter_inventory_v10()
    validate_m1_response_parameter_count_classification_v11()
    validate_m1_response_parameter_count_value_ledger_v12()
    validate_m1_response_parameter_adjustable_slot_resolution_v13()
    validate_m1_response_parameter_final_count_candidate_v14()
    validate_m1_response_parameter_final_count_freeze_v15()
    validate_m1_per_galaxy_response_privilege_count_audit_v10()
    validate_m1_per_galaxy_response_privilege_count_freeze_v11()
    validate_m2_benchmark_profile_table_v06()
    validate_m2_nuisance_policy_table_v06()
    validate_m2_benchmark_parameter_inventory_v10()
    validate_m2_benchmark_parameter_count_classification_v11()
    validate_m2_benchmark_parameter_count_value_ledger_v12()
    validate_m2_benchmark_parameter_adjustable_slot_resolution_v13()
    validate_m2_benchmark_parameter_final_count_candidate_v14()
    validate_m2_benchmark_parameter_final_count_freeze_v15()
    validate_m2_per_galaxy_benchmark_privilege_count_audit_v10()
    validate_m2_per_galaxy_benchmark_privilege_count_freeze_v11()
    validate_shared_scoring_input_table_v06()
    validate_shared_input_count_discount_policy_v10()
    validate_numeric_parameter_count_table_v06()
    validate_numeric_parameter_count_table_v08()
    validate_numeric_parameter_count_table_final_values_v10()
    validate_control_runner_outputs_v08()
    validate_control_execution_readiness_v09()
    validate_endpoint_scoring_runner_v01()
    validate_numeric_decision_thresholds_v08()
    validate_m0_global_parameter_inventory_v10()
    validate_m0_global_parameter_count_classification_v11()
    validate_m0_global_parameter_count_value_ledger_v12()
    validate_m0_global_adjustable_slot_resolution_v13()
    validate_m0_global_final_count_candidate_v14()
    validate_m0_global_final_count_freeze_v15()
    validate_m0_per_galaxy_privilege_count_audit_v10()
    validate_m0_per_galaxy_privilege_count_freeze_v11()
    validate_numeric_count_readiness_closure_v09()
    validate_family_prediction_table_contract_v80()
    validate_family_prediction_frontier_trace_v81()
    validate_scoring_activation_gate_v13()
    validate_source_import_template_v14()
    validate_active_v15_raw_sparc_like_input_writer_v56()
    validate_source_import_raw_adapter_v15()
    validate_active_v12_real_values_write_authorization_v57()
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
    validate_scoring_frontier_status_v72()
    validate_frontier_provenance_evidence_acceptance_v26()
    validate_frontier_provenance_evidence_work_order_v27()
    validate_frontier_work_order_completion_gate_v28()
    validate_frontier_evidence_write_authorization_v29()
    validate_frontier_authorized_evidence_writer_v30()
    validate_frontier_post_writer_evidence_absence_audit_v31()
    validate_post_writer_evidence_gate_recheck_v32()
    validate_post_writer_provenance_promotion_recheck_v33()
    validate_post_writer_raw_import_recheck_v34()
    validate_post_writer_raw_adapter_recheck_v35()
    validate_post_writer_real_values_gate_recheck_v36()
    validate_post_writer_leakage_audit_recheck_v37()
    validate_post_writer_scoring_activation_recheck_v38()
    validate_post_writer_scoring_preflight_recheck_v39()
    validate_post_writer_scoring_dependency_closure_recheck_v40()
    validate_post_writer_scoring_unblock_priority_recheck_v41()
    validate_post_writer_frontier_evidence_acceptance_recheck_v42()
    validate_post_writer_frontier_work_order_recheck_v43()
    validate_frontier_provenance_evidence_intake_contract_v44()
    validate_frontier_provenance_source_candidate_ledger_v45()
    validate_frontier_provenance_evidence_payload_draft_v46()
    validate_frontier_provenance_review_package_v47()
    validate_frontier_provenance_review_response_intake_v48()
    validate_frontier_review_promotion_gate_v49()
    validate_frontier_external_hash_recompute_audit_v50()
    validate_post_hash_frontier_review_promotion_recheck_v51()
    validate_post_hash_review_promotion_package_v52()
    validate_post_hash_review_promotion_response_intake_v53()
    validate_authorized_provenance_evidence_payload_v54()
    validate_active_v21_provenance_evidence_writer_v55()
    print("PAPER11_PROTOCOL_MANIFESTS_VALID")


if __name__ == "__main__":
    main()
