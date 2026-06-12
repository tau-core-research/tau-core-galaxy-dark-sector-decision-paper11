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
    require(all(row["current_status"] == "BLOCKED" for row in blockers), "v13 global blockers must remain blocked")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in blockers), "v13 blockers cannot allow scoring")
    require(len(summary) == 1, "v13 summary must have one row")
    row = summary[0]
    require(
        row["overall_status"] == "SCORING_ROW_ACTIVATION_READY_GLOBAL_SCORING_BLOCKED",
        "v13 row activation must be ready while global scoring remains blocked",
    )
    require(row["candidate_rows"] == "18", "v13 summary must cover eighteen candidate rows")
    require(row["rows_activated_for_scoring"] == "18", "v13 must activate eighteen rows")
    require(row["row_level_blocked_rows"] == "0", "v13 must block zero rows at row level")
    require(row["global_blockers"] == "4", "v13 must report four global blockers")
    require(
        row["next_required_artifact"] == "m0_no_dark_formula_table_v06",
        "v13 must point to first missing formula slot",
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


def validate_family_prediction_table_contract_v80() -> None:
    schema = read_csv(ROOT / "data/derived/family_prediction_table_schema_v80.csv")
    slots = read_csv(ROOT / "data/derived/family_prediction_table_slot_requirements_v80.csv")
    summary = read_csv(ROOT / "data/derived/family_prediction_table_contract_summary_v80.csv")
    fields = {row["field_name"] for row in schema}
    require({"scoring_row_id", "family_id", "v_pred_km_s"}.issubset(fields), "v80 schema missing required fields")
    require(all(row["endpoint_scoring_allowed"] == "false" for row in schema), "v80 schema cannot allow scoring")
    require(len(slots) == 8, "v80 must cover eight formula slots")
    require(
        all(row["prediction_slot_status"] == "PREDICTION_SLOT_BLOCKED_FORMULA_TABLE_MISSING" for row in slots),
        "v80 slots must remain blocked on formula tables",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in slots), "v80 slots cannot allow scoring")
    require(slots[0]["required_formula_artifact"] == "m0_no_dark_formula_table_v06", "v80 first formula artifact mismatch")
    require(len(summary) == 1, "v80 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "FAMILY_PREDICTION_TABLE_CONTRACT_V80", "v80 summary id mismatch")
    require(row["required_formula_slots"] == "8", "v80 must require eight formula slots")
    require(row["ready_formula_slots"] == "0", "v80 must ready zero formula slots")
    require(row["blocked_formula_slots"] == "8", "v80 must block eight formula slots")
    require(row["numeric_prediction_rows_written"] == "0", "v80 must write zero numeric prediction rows")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v80 summary must forbid scoring")
    require(
        row["overall_status"] == "FAMILY_PREDICTION_TABLE_CONTRACT_READY_FORMULA_SLOTS_BLOCKED",
        "v80 status mismatch",
    )
    require(row["next_required_artifact"] == "m0_no_dark_formula_table_v06", "v80 next artifact mismatch")


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
        },
        f"v24 ready ids mismatch: {ready_ids}",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v24 rows cannot allow scoring")
    require(any(row["upstream_status"] == "PROVENANCE_PROMOTION_READY_NOT_IMPORTED" for row in rows), "v24 must include v23 ready")
    require(
        any(row["upstream_status"] == "SCORING_ROW_ACTIVATION_READY_GLOBAL_SCORING_BLOCKED" for row in rows),
        "v24 must include v13 row activation readiness",
    )
    require(len(summary) == 1, "v24 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SCORING_DEPENDENCY_CLOSURE_BLOCKED", "v24 summary must block scoring closure")
    require(row["dependencies_checked"] == "13", "v24 must check thirteen dependencies")
    require(row["ready_dependencies"] == "9", "v24 must have nine ready dependencies")
    require(row["blocked_dependencies"] == "4", "v24 must block four dependencies")
    require(
        row["next_required_artifact"] == "m0_no_dark_formula_table_v06",
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
        },
        f"v25 ready ids mismatch: {ready_ids}",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v25 rows cannot allow scoring")
    frontier = [row for row in rows if row["frontier_now"] == "true"]
    require(len(frontier) == 1, "v25 must identify exactly one current frontier")
    require(frontier[0]["dependency_id"] == "SCD24_FAMILY_FORMULA_TABLES", "v25 first frontier must be family formula tables")
    require(
        frontier[0]["next_required_artifact"] == "m0_no_dark_formula_table_v06",
        "v25 frontier artifact must be family prediction tables",
    )
    require(len(summary) == 1, "v25 summary must have one row")
    row = summary[0]
    require(row["overall_status"] == "SCORING_UNBLOCK_FRONTIER_IDENTIFIED", "v25 must identify a frontier")
    require(row["priority_rows"] == "13", "v25 must summarize thirteen priorities")
    require(row["blocked_priority_rows"] == "4", "v25 must preserve four blocked rows")
    require(row["frontier_now_rows"] == "1", "v25 must summarize one current frontier")
    require(row["first_frontier_dependency"] == "SCD24_FAMILY_FORMULA_TABLES", "v25 frontier dependency mismatch")
    require(
        row["first_frontier_artifact"] == "m0_no_dark_formula_table_v06",
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
        rows[1]["next_required_artifact"] == "m0_no_dark_formula_table_v06",
        "v72 second frontier must hand off to family prediction tables after v79",
    )
    require(
        rows[2]["current_status"] == "FAMILY_PREDICTION_TABLE_CONTRACT_READY_FORMULA_SLOTS_BLOCKED",
        "v72 third frontier must reflect v80 formula-slot blocker",
    )
    require(
        rows[2]["next_required_artifact"] == "m0_no_dark_formula_table_v06",
        "v72 third frontier must point to family prediction tables",
    )
    require(len(summary) == 1, "v72 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "SCORING_FRONTIER_STATUS_V72", "v72 summary id mismatch")
    require(row["frontier_rows"] == "3", "v72 summary must record three frontier rows")
    require(row["blocked_frontier_rows"] == "3", "v72 must keep all frontier rows blocked")
    require(row["first_frontier_id"] == "SFS72_LEAKAGE_PARTIAL_SUFFICIENCY_RESPONSE", "v72 first frontier mismatch")
    require(
        row["first_frontier_artifact"] == "m0_no_dark_formula_table_v06",
        "v72 first frontier artifact summary mismatch",
    )
    require(row["required_components_for_full_scoring_leakage_pass"] == "4", "v72 must require four leakage components")
    require(row["partial_candidate_rows_requiring_review"] == "0", "v72 must clear the 36-row partial blocker")
    require(row["target_evidence_rows_created"] == "0", "v72 summary cannot create evidence")
    require(row["leakage_pass_authorized"] == "0", "v72 summary cannot authorize leakage pass")
    require(row["activation_rows_authorized"] == "0", "v72 summary cannot authorize activation")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v72 summary must forbid scoring")
    require(
        row["overall_status"] == "SCORING_FRONTIER_BLOCKED_ON_GLOBAL_SCORING_PREREQUISITES",
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
    require(row["global_blockers_after_recheck"] == "4", "v38 must preserve four global blockers")
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v38 summary must forbid scoring")
    require(row["overall_status"] == "POST_WRITER_SCORING_ACTIVATION_RECHECK_BLOCKED", "v38 summary must block")
    require(
        row["claim_boundary"] == "post_writer_scoring_activation_recheck_only_no_activation_no_scores_no_dark_sector_verdict",
        "v38 claim boundary mismatch",
    )


def validate_post_writer_scoring_preflight_recheck_v39() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_scoring_preflight_recheck_v39.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_scoring_preflight_recheck_summary_v39.csv")
    require(len(rows) == 6, "v39 preflight recheck must cover six requirements")
    require(all(row["v07_current_status"].startswith("BLOCKED") for row in rows), "v39 must inherit blocked v07 requirements")
    require(all(row["v38_rows_activated_after_recheck"] == "18" for row in rows), "v39 must inherit eighteen activated rows")
    require(
        all("v07_requirement_blocked" in row["preflight_recheck_blockers"] for row in rows),
        "v39 must block on v07 requirements",
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
    require(sum(row["v24_dependency_decision"] == "READY" for row in rows) == 9, "v40 must inherit nine ready v24 dependencies")
    require(sum(row["v24_dependency_decision"] == "BLOCKED" for row in rows) == 4, "v40 must inherit four blocked v24 dependencies")
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
        all(
            ("v25_priority_dependency_blocked" in row["priority_recheck_blockers"])
            == (row["v25_frontier_now"] != "false" or int(row["priority_rank"]) >= 10)
            for row in rows
        ),
        "v41 must flag v25 dependency blockers for the formula-table frontier and later blocked priorities",
    )
    require(
        all("post_writer_dependency_recheck_zero_ready_dependencies" in row["priority_recheck_blockers"] for row in rows),
        "v41 must block on zero ready dependencies",
    )
    require(
        all("post_writer_dependency_recheck_scoring_not_allowed" in row["priority_recheck_blockers"] for row in rows),
        "v41 must block on dependency scoring denial",
    )
    require(sum(row["frontier_now_after_recheck"] == "true" for row in rows) == 1, "v41 must mark one frontier row")
    frontier_rows = [row for row in rows if row["frontier_now_after_recheck"] == "true"]
    require(frontier_rows[0]["dependency_id"] == "SCD24_FAMILY_FORMULA_TABLES", "v41 frontier row must be formula tables")
    require(
        frontier_rows[0]["next_required_artifact"] == "m0_no_dark_formula_table_v06",
        "v41 frontier artifact mismatch",
    )
    require(all(row["endpoint_scoring_allowed"] == "false" for row in rows), "v41 rows cannot allow scoring")
    require(len(summary) == 1, "v41 summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "POST_WRITER_SCORING_UNBLOCK_PRIORITY_RECHECK_V41", "v41 summary id mismatch")
    require(row["priority_rows_rechecked"] == "13", "v41 must summarize thirteen priority rows")
    require(row["blocked_priority_rows_after_recheck"] == "13", "v41 must block thirteen priority rows")
    require(row["frontier_now_rows_after_recheck"] == "1", "v41 must summarize one frontier row")
    require(row["first_frontier_dependency_after_recheck"] == "SCD24_FAMILY_FORMULA_TABLES", "v41 frontier dependency mismatch")
    require(
        row["first_frontier_artifact_after_recheck"] == "m0_no_dark_formula_table_v06",
        "v41 frontier artifact mismatch",
    )
    require(row["endpoint_scoring_allowed_anywhere"] == "false", "v41 summary must forbid scoring")
    require(row["overall_status"] == "POST_WRITER_SCORING_UNBLOCK_FRONTIER_CONFIRMED", "v41 summary must confirm frontier")
    require(
        row["claim_boundary"] == "post_writer_scoring_unblock_priority_recheck_only_no_scores_no_dark_sector_verdict",
        "v41 claim boundary mismatch",
    )


def validate_post_writer_frontier_evidence_acceptance_recheck_v42() -> None:
    rows = read_csv(ROOT / "data/derived/post_writer_frontier_evidence_acceptance_recheck_v42.csv")
    summary = read_csv(ROOT / "data/derived/post_writer_frontier_evidence_acceptance_recheck_summary_v42.csv")
    require(len(rows) == 18, "v42 frontier acceptance recheck must cover eighteen rows")
    require(all(row["v41_frontier_dependency"] == "SCD24_FAMILY_FORMULA_TABLES" for row in rows), "v42 must inherit the formula-table frontier")
    require(
        all(row["v41_frontier_artifact"] == "m0_no_dark_formula_table_v06" for row in rows),
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
    validate_family_prediction_table_contract_v80()
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
