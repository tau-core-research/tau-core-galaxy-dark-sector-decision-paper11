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


def first_row(path: Path) -> dict[str, str]:
    rows = read_csv(path)
    if not rows:
        raise ValueError(f"empty csv: {path}")
    return rows[0]


def input_requirements() -> list[dict[str, object]]:
    activation = first_row(DERIVED / "scoring_row_activation_policy_summary_v79.csv")
    real_values = first_row(DERIVED / "source_import_real_values_summary_v12.csv")
    leakage = first_row(DERIVED / "source_import_leakage_summary_v09.csv")
    family_predictions = first_row(DERIVED / "family_prediction_tables_summary_v08.csv")
    family_comparability = first_row(DERIVED / "family_prediction_comparability_summary_v09.csv")
    parameter_counts = first_row(DERIVED / "numeric_parameter_count_table_final_values_summary_v10.csv")
    control_outputs = first_row(DERIVED / "control_runner_outputs_summary_v08.csv")
    control_readiness = first_row(DERIVED / "control_execution_readiness_summary_v09.csv")
    thresholds = first_row(DERIVED / "numeric_decision_thresholds_summary_v08.csv")

    active_rows_ready = (
        activation["activated_rows_written"] == "18"
        and activation["blocked_rows"] == "0"
        and activation["endpoint_scoring_allowed_anywhere"] == "false"
    )
    observed_inputs_ready = (
        real_values["expected_galaxy_rows"] == "18"
        and real_values["galaxies_with_imported_rows"] == "18"
        and int(real_values["imported_numeric_rows"]) > 0
        and leakage["leakage_pass_rows"] == "18"
    )
    family_predictions_ready = (
        family_predictions["numeric_prediction_rows_written"] != "0"
        and family_predictions["families_with_numeric_predictions"] == "3"
    )
    m0_adequacy_basis_ready = (
        family_comparability["m0_adequacy_scoring_basis_available"] == "true"
        and family_comparability["family_comparison_scoring_allowed"] == "false"
    )
    parameter_counts_ready = (
        parameter_counts["final_numeric_count_values_written"] == "7"
        and parameter_counts["parsimony_scores_written"] == "0"
    )
    control_outputs_ready = (
        control_readiness["score_calculation_preflight_ready"] == "true"
        and control_outputs["control_result_rows_written"] == "0"
        and control_outputs["control_scores_written"] == "0"
    )
    thresholds_ready = (
        thresholds["numeric_threshold_rows_written"] == "4"
        and thresholds["endpoint_scores_written"] == "0"
        and thresholds["verdicts_written"] == "0"
    )

    return [
        {
            "requirement_id": "SPR07_ACTIVE_ROWS",
            "required_artifact": "activated_scoring_rows_v10.csv",
            "purpose": "Declare exactly which galaxy rows enter train, heldout, challenge, and control scoring",
            "current_status": "READY_ACTIVATED_ROWS_PRESENT_NO_SCORES"
            if active_rows_ready
            else "BLOCKED_BY_ACTIVATION_POLICY",
            "endpoint_scoring_allowed": "false",
            "blocking_source": "data/derived/scoring_row_activation_policy_summary_v79.csv",
            "claim_boundary": "preflight_only_no_scores",
        },
        {
            "requirement_id": "SPR07_OBSERVED_INPUTS",
            "required_artifact": "data/input/source_import_real_values_v12.csv",
            "purpose": "Provide radial grid, observed velocity, uncertainty, and baryonic component inputs",
            "current_status": "READY_OBSERVED_INPUTS_IMPORTED_AND_LEAKAGE_PASSED"
            if observed_inputs_ready
            else "BLOCKED_BY_SOURCE_IMPORT_OR_LEAKAGE",
            "endpoint_scoring_allowed": "false",
            "blocking_source": "data/derived/source_import_real_values_summary_v12.csv;data/derived/source_import_leakage_summary_v09.csv",
            "claim_boundary": "preflight_only_no_scores",
        },
        {
            "requirement_id": "SPR07_FAMILY_PREDICTIONS",
            "required_artifact": "family_prediction_tables_v08.csv",
            "purpose": "Provide frozen predicted velocity/readout arrays for M0, M1, and M2 before score aggregation",
            "current_status": "READY_ALL_FAMILY_PREDICTIONS_PRESENT_NO_SCORES"
            if family_predictions_ready
            else "READY_M0_ADEQUACY_BASIS_FULL_FAMILY_COMPARISON_BLOCKED_NO_SCORES"
            if m0_adequacy_basis_ready
            else "BLOCKED_PARTIAL_FAMILY_PREDICTIONS_ONLY_M0",
            "endpoint_scoring_allowed": "false",
            "blocking_source": "data/derived/family_prediction_comparability_summary_v09.csv",
            "claim_boundary": "preflight_only_no_family_comparison",
        },
        {
            "requirement_id": "SPR07_PARAMETER_COUNTS",
            "required_artifact": "numeric_parameter_count_table_final_values_v10.csv",
            "purpose": "Provide numeric parameter and per-galaxy privilege counts for parsimony penalty",
            "current_status": "READY_PARAMETER_COUNTS_FROZEN_NO_PARSIMONY_SCORE"
            if parameter_counts_ready
            else "BLOCKED_BY_FINAL_NUMERIC_COUNT_VALUES",
            "endpoint_scoring_allowed": "false",
            "blocking_source": "data/derived/numeric_parameter_count_table_final_values_summary_v10.csv",
            "claim_boundary": "preflight_only_no_parsimony_claim",
        },
        {
            "requirement_id": "SPR07_CONTROL_OUTPUTS",
            "required_artifact": "control_runner_outputs_v08.csv",
            "purpose": "Provide shuffle, wrong-family, null-source, leakage, radial, and parity control outputs",
            "current_status": "READY_CONTROL_CONTRACTS_FOR_SCORE_CALCULATION_VERDICT_CONTROLS_BLOCKED"
            if control_outputs_ready
            else "BLOCKED_CONTROL_OUTPUT_CONTRACTS_READY_NOT_RUN",
            "endpoint_scoring_allowed": "false",
            "blocking_source": "data/derived/control_execution_readiness_summary_v09.csv",
            "claim_boundary": "preflight_only_no_control_result",
        },
        {
            "requirement_id": "SPR07_DECISION_THRESHOLDS",
            "required_artifact": "numeric_decision_thresholds_v08.csv",
            "purpose": "Provide numeric adequacy, improvement, stability, and unresolved thresholds before verdict",
            "current_status": "READY_NUMERIC_THRESHOLDS_FROZEN_NOT_EVALUATED"
            if thresholds_ready
            else "BLOCKED_BY_THRESHOLD_PENDING",
            "endpoint_scoring_allowed": "false",
            "blocking_source": "data/derived/numeric_decision_thresholds_summary_v08.csv",
            "claim_boundary": "preflight_only_no_verdict",
        },
    ]


def formula_components() -> list[dict[str, object]]:
    rows = read_csv(SOURCE / "scoring_formula_freeze_v02.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "formula_id": row["formula_id"],
                "score_component": row["score_component"],
                "formula_policy_status": "READY_AS_POLICY_NOT_RUN",
                "requires_input_artifacts": "activated_scoring_rows_v08.csv;scoring_observed_inputs_v08.csv;family_prediction_tables_v08.csv",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "scoring_formula_policy_only_no_score",
            }
        )
    return out


def summary(requirements: list[dict[str, object]], components: list[dict[str, object]]) -> list[dict[str, object]]:
    readiness = read_csv(DERIVED / "readiness_summary_v06.csv")[0]
    blocked_requirements = sum(1 for row in requirements if str(row["current_status"]).startswith("BLOCKED"))
    formula_policy_ready = len(components)
    endpoint_allowed = any(row["endpoint_scoring_allowed"] == "true" for row in requirements + components)
    return [
        {
            "summary_id": "SCORING_PREFLIGHT_V07",
            "readiness_dependency": readiness["overall_status"],
            "blocked_scoring_requirements": blocked_requirements,
            "formula_policy_components_ready": formula_policy_ready,
            "endpoint_scoring_allowed_anywhere": str(endpoint_allowed).lower(),
            "overall_status": "SCORING_PREFLIGHT_REQUIREMENTS_READY_RAW_M0_ADEQUACY_RUNNER_NEXT_VERDICT_BLOCKED"
            if blocked_requirements == 0
            else "SCORING_PREFLIGHT_M0_ADEQUACY_BASIS_READY_BLOCKED_ON_CONTROLS_FULL_COMPARISON_BLOCKED"
            if blocked_requirements == 1
            else "SCORING_PREFLIGHT_PARTIAL_READY_BLOCKED_ON_FAMILY_PREDICTIONS_AND_CONTROLS"
            if blocked_requirements
            else "SCORING_PREFLIGHT_REQUIREMENTS_READY_RAW_M0_ADEQUACY_RUNNER_NEXT_VERDICT_BLOCKED",
            "next_required_artifact": "control_runner_outputs_v08.csv"
            if blocked_requirements == 1
            else "family_prediction_tables_v08.csv"
            if blocked_requirements
            else "endpoint_scoring_runner_v01",
            "claim_boundary": "scoring_preflight_only_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    requirements = input_requirements()
    components = formula_components()
    summary_rows = summary(requirements, components)
    write_csv(
        DERIVED / "scoring_input_requirements_v07.csv",
        requirements,
        [
            "requirement_id",
            "required_artifact",
            "purpose",
            "current_status",
            "endpoint_scoring_allowed",
            "blocking_source",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_formula_components_v07.csv",
        components,
        [
            "formula_id",
            "score_component",
            "formula_policy_status",
            "requires_input_artifacts",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_preflight_summary_v07.csv",
        summary_rows,
        [
            "summary_id",
            "readiness_dependency",
            "blocked_scoring_requirements",
            "formula_policy_components_ready",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SCORING_PREFLIGHT_V07_BUILT")


if __name__ == "__main__":
    main()
