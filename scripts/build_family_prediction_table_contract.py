#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
DERIVED = ROOT / "data/derived"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def schema_rows() -> list[dict[str, object]]:
    fields = [
        ("scoring_row_id", "string", "Activated scoring row id from activated_scoring_rows_v10.csv"),
        ("galaxy_id", "string", "Galaxy identifier matching the activated row"),
        ("family_id", "enum", "One of M0, M1, or M2"),
        ("radial_index", "integer", "Radial grid index shared with the observed-input table"),
        ("radius_kpc", "float", "Radius in kpc on the frozen shared radial grid"),
        ("v_pred_km_s", "float", "Frozen family prediction at this radial point"),
        ("prediction_source_slot", "string", "Formula slot used to produce the prediction"),
        ("formula_table_status", "string", "Formula-slot readiness status before scoring"),
        ("prediction_status", "string", "Prediction-row readiness status"),
    ]
    return [
        {
            "field_name": name,
            "field_type": field_type,
            "definition": definition,
            "required_before_scoring": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "family_prediction_table_schema_only_no_predictions",
        }
        for name, field_type, definition in fields
    ]


def slot_rows() -> list[dict[str, object]]:
    formula_rows = read_csv(SOURCE / "family_formula_table_v05.csv")
    m0_contract_path = DERIVED / "m0_no_dark_formula_table_contract_summary_v06.csv"
    m0_contract = read_csv(m0_contract_path)[0] if m0_contract_path.exists() else {}
    prediction_tables_path = DERIVED / "family_prediction_tables_summary_v08.csv"
    prediction_tables = read_csv(prediction_tables_path)[0] if prediction_tables_path.exists() else {}
    row_writer_path = DERIVED / "m0_no_dark_prediction_row_writer_summary_v08.csv"
    row_writer = read_csv(row_writer_path)[0] if row_writer_path.exists() else {}
    executable_kernel_path = DERIVED / "m0_no_dark_executable_prediction_kernel_summary_v08.csv"
    executable_kernel = read_csv(executable_kernel_path)[0] if executable_kernel_path.exists() else {}
    velocity_formula_path = DERIVED / "m0_no_dark_velocity_readout_formula_summary_v08.csv"
    velocity_formula = read_csv(velocity_formula_path)[0] if velocity_formula_path.exists() else {}
    equation_body_path = DERIVED / "m0_no_dark_source_to_rotation_equation_body_summary_v08.csv"
    equation_body = read_csv(equation_body_path)[0] if equation_body_path.exists() else {}
    coupling_rule_path = DERIVED / "m0_no_dark_source_to_velocity_coupling_rule_summary_v08.csv"
    coupling_rule = read_csv(coupling_rule_path)[0] if coupling_rule_path.exists() else {}
    unit_lift_path = DERIVED / "m0_no_dark_velocity_unit_lift_rule_summary_v08.csv"
    unit_lift = read_csv(unit_lift_path)[0] if unit_lift_path.exists() else {}
    dimension_anchor_path = DERIVED / "m0_no_dark_velocity_dimension_anchor_rule_summary_v08.csv"
    dimension_anchor = read_csv(dimension_anchor_path)[0] if dimension_anchor_path.exists() else {}
    anchor_source_law_path = DERIVED / "m0_no_dark_velocity_anchor_source_law_summary_v08.csv"
    anchor_source_law = read_csv(anchor_source_law_path)[0] if anchor_source_law_path.exists() else {}
    anchor_candidate_basis_path = DERIVED / "m0_no_dark_velocity_anchor_candidate_basis_summary_v08.csv"
    anchor_candidate_basis = read_csv(anchor_candidate_basis_path)[0] if anchor_candidate_basis_path.exists() else {}
    anchor_selection_rule_path = DERIVED / "m0_no_dark_velocity_anchor_selection_rule_summary_v08.csv"
    anchor_selection_rule = read_csv(anchor_selection_rule_path)[0] if anchor_selection_rule_path.exists() else {}
    anchor_value_freeze_path = DERIVED / "m0_no_dark_velocity_anchor_value_freeze_summary_v08.csv"
    anchor_value_freeze = read_csv(anchor_value_freeze_path)[0] if anchor_value_freeze_path.exists() else {}
    anchor_unit_normalization_path = DERIVED / "m0_no_dark_velocity_anchor_unit_normalization_summary_v08.csv"
    anchor_unit_normalization = read_csv(anchor_unit_normalization_path)[0] if anchor_unit_normalization_path.exists() else {}
    anchor_component_combination_path = DERIVED / "m0_no_dark_velocity_anchor_component_combination_rule_summary_v08.csv"
    anchor_component_combination = (
        read_csv(anchor_component_combination_path)[0] if anchor_component_combination_path.exists() else {}
    )
    anchor_component_weight_policy_path = DERIVED / "m0_no_dark_velocity_anchor_component_weight_policy_summary_v08.csv"
    anchor_component_weight_policy = (
        read_csv(anchor_component_weight_policy_path)[0] if anchor_component_weight_policy_path.exists() else {}
    )
    anchor_component_weight_value_freeze_path = (
        DERIVED / "m0_no_dark_velocity_anchor_component_weight_value_freeze_summary_v08.csv"
    )
    anchor_component_weight_value_freeze = (
        read_csv(anchor_component_weight_value_freeze_path)[0]
        if anchor_component_weight_value_freeze_path.exists()
        else {}
    )
    anchor_combined_anchor_rule_path = DERIVED / "m0_no_dark_velocity_anchor_combined_anchor_rule_summary_v08.csv"
    anchor_combined_anchor_rule = (
        read_csv(anchor_combined_anchor_rule_path)[0] if anchor_combined_anchor_rule_path.exists() else {}
    )
    anchor_combined_anchor_expression_path = (
        DERIVED / "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_summary_v08.csv"
    )
    anchor_combined_anchor_expression = (
        read_csv(anchor_combined_anchor_expression_path)[0] if anchor_combined_anchor_expression_path.exists() else {}
    )
    anchor_combined_anchor_value_path = (
        DERIVED / "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_summary_v08.csv"
    )
    anchor_combined_anchor_value = (
        read_csv(anchor_combined_anchor_value_path)[0] if anchor_combined_anchor_value_path.exists() else {}
    )
    velocity_formula_body_path = DERIVED / "m0_no_dark_velocity_readout_formula_body_freeze_summary_v08.csv"
    velocity_formula_body = read_csv(velocity_formula_body_path)[0] if velocity_formula_body_path.exists() else {}
    prediction_row_value_path = DERIVED / "m0_no_dark_prediction_row_value_freeze_summary_v08.csv"
    prediction_row_value = read_csv(prediction_row_value_path)[0] if prediction_row_value_path.exists() else {}
    family_row_emission_path = DERIVED / "m0_no_dark_family_prediction_row_emission_summary_v08.csv"
    family_row_emission = read_csv(family_row_emission_path)[0] if family_row_emission_path.exists() else {}
    m0_label_rule_path = DERIVED / "m0_label_rule_table_summary_v06.csv"
    m0_label_rule = read_csv(m0_label_rule_path)[0] if m0_label_rule_path.exists() else {}
    m1_response_path = DERIVED / "m1_tau_response_formula_table_summary_v06.csv"
    m1_response = read_csv(m1_response_path)[0] if m1_response_path.exists() else {}
    m1_admissibility_path = DERIVED / "m1_admissibility_table_summary_v06.csv"
    m1_admissibility = read_csv(m1_admissibility_path)[0] if m1_admissibility_path.exists() else {}
    m2_profile_path = DERIVED / "m2_benchmark_profile_table_summary_v06.csv"
    m2_profile = read_csv(m2_profile_path)[0] if m2_profile_path.exists() else {}
    m2_nuisance_path = DERIVED / "m2_nuisance_policy_table_summary_v06.csv"
    m2_nuisance = read_csv(m2_nuisance_path)[0] if m2_nuisance_path.exists() else {}
    shared_inputs_path = DERIVED / "shared_scoring_input_table_summary_v06.csv"
    shared_inputs = read_csv(shared_inputs_path)[0] if shared_inputs_path.exists() else {}
    numeric_counts_path = DERIVED / "numeric_parameter_count_table_summary_v06.csv"
    numeric_counts = read_csv(numeric_counts_path)[0] if numeric_counts_path.exists() else {}
    out: list[dict[str, object]] = []
    for index, row in enumerate(formula_rows, start=1):
        ready = row["formula_table_status"] == "FORMULA_TABLE_READY"
        required_artifact = row["next_required_artifact"]
        prediction_status = "PREDICTION_SLOT_READY" if ready else "PREDICTION_SLOT_BLOCKED_FORMULA_TABLE_MISSING"
        if row["next_required_artifact"] == "m0_no_dark_formula_table_v06" and m0_contract:
            required_artifact = str(m0_contract["next_required_artifact"])
            if m0_contract["overall_status"] == "M0_NO_DARK_FORMULA_TABLE_CONTRACT_READY_POLICY_SLOTS_BLOCKED":
                prediction_status = "PREDICTION_SLOT_BLOCKED_FORMULA_POLICY_MISSING"
            elif m0_contract["overall_status"] == "M0_NO_DARK_FORMULA_TABLE_READY_FOR_PREDICTION_ROWS":
                if family_row_emission.get("overall_status") == (
                    "M0_NO_DARK_FAMILY_PREDICTION_ROWS_EMITTED_SCORING_BLOCKED"
                ):
                    required_artifact = "family_prediction_tables_v08.csv"
                    prediction_status = "PREDICTION_SLOT_READY"
                elif prediction_tables.get("overall_status") == "FAMILY_PREDICTION_TABLES_PRESENT_NO_NUMERIC_ROWS":
                    if row_writer.get("overall_status") == (
                        "M0_NO_DARK_PREDICTION_ROW_WRITER_PRESENT_BLOCKED_EXECUTABLE_KERNEL_MISSING"
                    ):
                        if executable_kernel.get("overall_status") == (
                            "M0_NO_DARK_EXECUTABLE_KERNEL_PRESENT_BLOCKED_VELOCITY_FORMULA_MISSING"
                        ):
                            if velocity_formula.get("overall_status") == (
                                "M0_NO_DARK_VELOCITY_FORMULA_PRESENT_BLOCKED_EQUATION_BODY_MISSING"
                            ):
                                if equation_body.get("overall_status") == (
                                    "M0_NO_DARK_EQUATION_BODY_PRESENT_BLOCKED_SOURCE_TO_VELOCITY_COUPLING_RULE_MISSING"
                                ):
                                    if coupling_rule.get("overall_status") == (
                                        "M0_NO_DARK_COUPLING_RULE_PRESENT_BLOCKED_VELOCITY_UNIT_LIFT_MISSING"
                                    ):
                                        if unit_lift.get("overall_status") == (
                                            "M0_NO_DARK_VELOCITY_UNIT_LIFT_PRESENT_BLOCKED_DIMENSION_ANCHOR_MISSING"
                                        ):
                                            if dimension_anchor.get("overall_status") == (
                                                "M0_NO_DARK_DIMENSION_ANCHOR_PRESENT_BLOCKED_ANCHOR_SOURCE_LAW_MISSING"
                                            ):
                                                if anchor_source_law.get("overall_status") == (
                                                    "M0_NO_DARK_ANCHOR_SOURCE_LAW_PRESENT_BLOCKED_ANCHOR_CANDIDATE_BASIS_MISSING"
                                                ):
                                                    if anchor_candidate_basis.get("overall_status") == (
                                                        "M0_NO_DARK_ANCHOR_CANDIDATE_BASIS_PRESENT_BLOCKED_ANCHOR_SELECTION_RULE_MISSING"
                                                    ):
                                                        if anchor_selection_rule.get("overall_status") == (
                                                            "M0_NO_DARK_ANCHOR_SELECTION_RULE_PRESENT_BLOCKED_ANCHOR_VALUE_FREEZE_MISSING"
                                                        ):
                                                            if anchor_value_freeze.get("overall_status") == (
                                                                "M0_NO_DARK_ANCHOR_VALUE_FREEZE_PRESENT_BLOCKED_UNIT_NORMALIZATION_MISSING"
                                                            ):
                                                                if anchor_unit_normalization.get("overall_status") == (
                                                                    "M0_NO_DARK_ANCHOR_UNIT_NORMALIZATION_PRESENT_BLOCKED_COMPONENT_COMBINATION_RULE_MISSING"
                                                                ):
                                                                    if anchor_component_combination.get("overall_status") == (
                                                                        "M0_NO_DARK_ANCHOR_COMPONENT_COMBINATION_RULE_PRESENT_BLOCKED_COMPONENT_WEIGHT_POLICY_MISSING"
                                                                    ):
                                                                        if anchor_component_weight_policy.get("overall_status") == (
                                                                            "M0_NO_DARK_ANCHOR_COMPONENT_WEIGHT_POLICY_PRESENT_BLOCKED_WEIGHT_VALUE_FREEZE_MISSING"
                                                                        ):
                                                                            if anchor_component_weight_value_freeze.get("overall_status") == (
                                                                                "M0_NO_DARK_ANCHOR_COMPONENT_WEIGHT_VALUE_FREEZE_PRESENT_BLOCKED_COMBINED_ANCHOR_RULE_MISSING"
                                                                            ):
                                                                                if anchor_combined_anchor_rule.get("overall_status") == (
                                                                                    "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_RULE_PRESENT_BLOCKED_EXPRESSION_FREEZE_MISSING"
                                                                                ):
                                                                                    if anchor_combined_anchor_expression.get("overall_status") == (
                                                                                        "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_EXPRESSION_FROZEN_BLOCKED_VALUE_FREEZE_MISSING"
                                                                                    ):
                                                                                        if anchor_combined_anchor_value.get("overall_status") == (
                                                                                            "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_VALUES_FROZEN_BLOCKED_VELOCITY_FORMULA_BODY_FREEZE_MISSING"
                                                                                        ):
                                                                                            if velocity_formula_body.get("overall_status") == (
                                                                                                "M0_NO_DARK_VELOCITY_FORMULA_BODY_FROZEN_BLOCKED_PREDICTION_ROW_VALUE_FREEZE_MISSING"
                                                                                            ):
                                                                                                if prediction_row_value.get("overall_status") == (
                                                                                                    "M0_NO_DARK_PREDICTION_ROW_VALUES_FROZEN_BLOCKED_FAMILY_ROW_EMISSION_MISSING"
                                                                                                ):
                                                                                                    if family_row_emission.get("overall_status") == (
                                                                                                        "M0_NO_DARK_FAMILY_PREDICTION_ROWS_EMITTED_SCORING_BLOCKED"
                                                                                                    ):
                                                                                                        required_artifact = "family_prediction_tables_v08.csv"
                                                                                                        prediction_status = "PREDICTION_SLOT_READY"
                                                                                                    else:
                                                                                                        required_artifact = str(
                                                                                                            prediction_row_value[
                                                                                                                "next_required_artifact"
                                                                                                            ]
                                                                                                        )
                                                                                                        prediction_status = (
                                                                                                            "PREDICTION_SLOT_BLOCKED_FAMILY_ROW_EMISSION_MISSING"
                                                                                                        )
                                                                                                else:
                                                                                                    required_artifact = str(
                                                                                                        velocity_formula_body[
                                                                                                            "next_required_artifact"
                                                                                                        ]
                                                                                                    )
                                                                                                    prediction_status = (
                                                                                                        "PREDICTION_SLOT_BLOCKED_PREDICTION_ROW_VALUE_FREEZE_MISSING"
                                                                                                    )
                                                                                            else:
                                                                                                required_artifact = str(
                                                                                                    anchor_combined_anchor_value[
                                                                                                        "next_required_artifact"
                                                                                                    ]
                                                                                                )
                                                                                                prediction_status = (
                                                                                                    "PREDICTION_SLOT_BLOCKED_VELOCITY_FORMULA_BODY_FREEZE_MISSING"
                                                                                                )
                                                                                        else:
                                                                                            required_artifact = str(
                                                                                                anchor_combined_anchor_expression[
                                                                                                    "next_required_artifact"
                                                                                                ]
                                                                                            )
                                                                                            prediction_status = (
                                                                                                "PREDICTION_SLOT_BLOCKED_COMBINED_ANCHOR_VALUE_FREEZE_MISSING"
                                                                                            )
                                                                                    else:
                                                                                        required_artifact = str(
                                                                                            anchor_combined_anchor_rule[
                                                                                                "next_required_artifact"
                                                                                            ]
                                                                                        )
                                                                                        prediction_status = (
                                                                                            "PREDICTION_SLOT_BLOCKED_COMBINED_ANCHOR_EXPRESSION_FREEZE_MISSING"
                                                                                        )
                                                                                else:
                                                                                    required_artifact = str(
                                                                                        anchor_component_weight_value_freeze[
                                                                                            "next_required_artifact"
                                                                                        ]
                                                                                    )
                                                                                    prediction_status = (
                                                                                        "PREDICTION_SLOT_BLOCKED_COMBINED_ANCHOR_RULE_MISSING"
                                                                                    )
                                                                            else:
                                                                                required_artifact = str(
                                                                                    anchor_component_weight_policy[
                                                                                        "next_required_artifact"
                                                                                    ]
                                                                                )
                                                                                prediction_status = (
                                                                                    "PREDICTION_SLOT_BLOCKED_COMPONENT_WEIGHT_VALUE_FREEZE_MISSING"
                                                                                )
                                                                        else:
                                                                            required_artifact = str(
                                                                                anchor_component_combination["next_required_artifact"]
                                                                            )
                                                                            prediction_status = (
                                                                                "PREDICTION_SLOT_BLOCKED_COMPONENT_WEIGHT_POLICY_MISSING"
                                                                            )
                                                                    else:
                                                                        required_artifact = str(
                                                                            anchor_unit_normalization["next_required_artifact"]
                                                                        )
                                                                        prediction_status = (
                                                                            "PREDICTION_SLOT_BLOCKED_COMPONENT_COMBINATION_RULE_MISSING"
                                                                        )
                                                                else:
                                                                    required_artifact = str(anchor_value_freeze["next_required_artifact"])
                                                                    prediction_status = "PREDICTION_SLOT_BLOCKED_ANCHOR_UNIT_NORMALIZATION_MISSING"
                                                            else:
                                                                required_artifact = str(anchor_selection_rule["next_required_artifact"])
                                                                prediction_status = "PREDICTION_SLOT_BLOCKED_ANCHOR_VALUE_FREEZE_MISSING"
                                                        else:
                                                            required_artifact = str(anchor_candidate_basis["next_required_artifact"])
                                                            prediction_status = "PREDICTION_SLOT_BLOCKED_ANCHOR_SELECTION_RULE_MISSING"
                                                    else:
                                                        required_artifact = str(anchor_source_law["next_required_artifact"])
                                                        prediction_status = "PREDICTION_SLOT_BLOCKED_ANCHOR_CANDIDATE_BASIS_MISSING"
                                                else:
                                                    required_artifact = str(dimension_anchor["next_required_artifact"])
                                                    prediction_status = "PREDICTION_SLOT_BLOCKED_ANCHOR_SOURCE_LAW_MISSING"
                                            else:
                                                required_artifact = str(unit_lift["next_required_artifact"])
                                                prediction_status = "PREDICTION_SLOT_BLOCKED_DIMENSION_ANCHOR_MISSING"
                                        else:
                                            required_artifact = str(coupling_rule["next_required_artifact"])
                                            prediction_status = "PREDICTION_SLOT_BLOCKED_VELOCITY_UNIT_LIFT_MISSING"
                                    else:
                                        required_artifact = str(equation_body["next_required_artifact"])
                                        prediction_status = "PREDICTION_SLOT_BLOCKED_COUPLING_RULE_MISSING"
                                else:
                                    required_artifact = str(velocity_formula["next_required_artifact"])
                                    prediction_status = "PREDICTION_SLOT_BLOCKED_EQUATION_BODY_MISSING"
                            else:
                                required_artifact = str(executable_kernel["next_required_artifact"])
                                prediction_status = "PREDICTION_SLOT_BLOCKED_VELOCITY_FORMULA_MISSING"
                        else:
                            required_artifact = str(row_writer["next_required_artifact"])
                            prediction_status = "PREDICTION_SLOT_BLOCKED_EXECUTABLE_KERNEL_MISSING"
                    else:
                        required_artifact = str(prediction_tables["next_required_artifact"])
                        prediction_status = "PREDICTION_SLOT_BLOCKED_PREDICTION_WRITER_MISSING"
                else:
                    prediction_status = "PREDICTION_SLOT_BLOCKED_PREDICTION_ROWS_MISSING"
            else:
                prediction_status = "PREDICTION_SLOT_BLOCKED_FORMULA_BODY_MISSING"
        elif row["next_required_artifact"] == "m0_label_rule_table_v06" and m0_label_rule:
            if m0_label_rule["overall_status"] == "M0_LABEL_RULE_TABLE_READY_SCORING_BLOCKED":
                required_artifact = "m0_label_rule_table_v06"
                prediction_status = "PREDICTION_SLOT_READY"
            else:
                required_artifact = str(m0_label_rule["next_required_artifact"])
                prediction_status = "PREDICTION_SLOT_BLOCKED_LABEL_RULE_MISSING"
        elif row["next_required_artifact"] == "m1_tau_response_formula_table_v06" and m1_response:
            if m1_response["overall_status"] == "M1_TAU_RESPONSE_FORMULA_TABLE_READY_ADMISSIBILITY_BLOCKED":
                required_artifact = "m1_tau_response_formula_table_v06"
                prediction_status = "PREDICTION_SLOT_READY"
            else:
                required_artifact = str(m1_response["next_required_artifact"])
                prediction_status = "PREDICTION_SLOT_BLOCKED_RESPONSE_FORMULA_TABLE_MISSING"
        elif row["next_required_artifact"] == "m1_admissibility_table_v06" and m1_admissibility:
            if m1_admissibility["overall_status"] == "M1_ADMISSIBILITY_TABLE_READY_M2_BENCHMARK_BLOCKED":
                required_artifact = "m1_admissibility_table_v06"
                prediction_status = "PREDICTION_SLOT_READY"
            else:
                required_artifact = str(m1_admissibility["next_required_artifact"])
                prediction_status = "PREDICTION_SLOT_BLOCKED_ADMISSIBILITY_TABLE_MISSING"
        elif row["next_required_artifact"] == "m2_benchmark_profile_table_v06" and m2_profile:
            if m2_profile["overall_status"] == "M2_BENCHMARK_PROFILE_TABLE_READY_NUISANCE_BLOCKED":
                required_artifact = "m2_benchmark_profile_table_v06"
                prediction_status = "PREDICTION_SLOT_READY"
            else:
                required_artifact = str(m2_profile["next_required_artifact"])
                prediction_status = "PREDICTION_SLOT_BLOCKED_BENCHMARK_PROFILE_TABLE_MISSING"
        elif row["next_required_artifact"] == "m2_nuisance_policy_table_v06" and m2_nuisance:
            if m2_nuisance["overall_status"] == "M2_NUISANCE_POLICY_TABLE_READY_SHARED_INPUTS_BLOCKED":
                required_artifact = "m2_nuisance_policy_table_v06"
                prediction_status = "PREDICTION_SLOT_READY"
            else:
                required_artifact = str(m2_nuisance["next_required_artifact"])
                prediction_status = "PREDICTION_SLOT_BLOCKED_NUISANCE_POLICY_TABLE_MISSING"
        elif row["next_required_artifact"] == "shared_scoring_input_table_v06" and shared_inputs:
            if shared_inputs["overall_status"] == "SHARED_SCORING_INPUT_TABLE_READY_PARAMETER_COUNTS_BLOCKED":
                required_artifact = "shared_scoring_input_table_v06"
                prediction_status = "PREDICTION_SLOT_READY"
            else:
                required_artifact = str(shared_inputs["next_required_artifact"])
                prediction_status = "PREDICTION_SLOT_BLOCKED_SHARED_SCORING_INPUTS_MISSING"
        elif row["next_required_artifact"] == "numeric_parameter_count_table_v06" and numeric_counts:
            if numeric_counts["overall_status"] == "NUMERIC_PARAMETER_COUNT_TABLE_CONTRACT_READY_FINAL_COUNTS_BLOCKED":
                required_artifact = "numeric_parameter_count_table_v06"
                prediction_status = "PREDICTION_SLOT_READY"
            else:
                required_artifact = str(numeric_counts["next_required_artifact"])
                prediction_status = "PREDICTION_SLOT_BLOCKED_NUMERIC_PARAMETER_COUNT_TABLE_MISSING"
        out.append(
            {
                "slot_requirement_id": f"FPT80_{index:03d}",
                "family_id": row["family_id"],
                "formula_slot": row["formula_slot"],
                "required_formula_artifact": required_artifact,
                "minimum_required_entries": row["minimum_required_entries"],
                "formula_table_status": row["formula_table_status"],
                "prediction_slot_status": prediction_status,
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "family_prediction_slot_requirement_only_no_formula_claim",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["prediction_slot_status"] == "PREDICTION_SLOT_READY" for row in rows)
    blocked = len(rows) - ready
    prediction_table_path = DERIVED / "family_prediction_tables_summary_v08.csv"
    prediction_table = read_csv(prediction_table_path)[0] if prediction_table_path.exists() else {}
    numeric_rows = int(prediction_table.get("numeric_prediction_rows_written", 0) or 0)
    next_required = next(
        (row["required_formula_artifact"] for row in rows if row["prediction_slot_status"] != "PREDICTION_SLOT_READY"),
        "numeric_parameter_count_table_v08.csv",
    )
    return [
        {
            "summary_id": "FAMILY_PREDICTION_TABLE_CONTRACT_V80",
            "required_formula_slots": len(rows),
            "ready_formula_slots": ready,
            "blocked_formula_slots": blocked,
            "numeric_prediction_rows_written": numeric_rows,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FAMILY_PREDICTION_TABLE_CONTRACT_READY_FORMULA_SLOTS_BLOCKED"
            if blocked
            else "FAMILY_PREDICTION_TABLE_CONTRACT_READY_PARAMETER_COUNTS_BLOCKED",
            "next_required_artifact": next_required,
            "claim_boundary": "family_prediction_table_contract_only_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    schema = schema_rows()
    slots = slot_rows()
    summary_rows = summary(slots)
    write_csv(
        DERIVED / "family_prediction_table_schema_v80.csv",
        schema,
        [
            "field_name",
            "field_type",
            "definition",
            "required_before_scoring",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "family_prediction_table_slot_requirements_v80.csv",
        slots,
        [
            "slot_requirement_id",
            "family_id",
            "formula_slot",
            "required_formula_artifact",
            "minimum_required_entries",
            "formula_table_status",
            "prediction_slot_status",
            "forbidden_inputs",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "family_prediction_table_contract_summary_v80.csv",
        summary_rows,
        [
            "summary_id",
            "required_formula_slots",
            "ready_formula_slots",
            "blocked_formula_slots",
            "numeric_prediction_rows_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_FAMILY_PREDICTION_TABLE_CONTRACT_V80_BUILT")


if __name__ == "__main__":
    main()
