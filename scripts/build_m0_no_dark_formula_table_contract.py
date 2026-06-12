#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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


def contract_rows() -> list[dict[str, object]]:
    body_contract_path = DERIVED / "m0_no_dark_formula_body_contract_summary_v07.csv"
    body_contract = read_csv(body_contract_path)[0] if body_contract_path.exists() else {}
    body_next = str(body_contract["next_required_artifact"]) if body_contract else "m0_no_dark_formula_body_v07"
    rows = [
        {
            "component_id": "M0ND06_SOURCE_INPUTS",
            "component_class": "source_input_contract",
            "required_entry": "activated source-side morphology/readout labels plus shared baryonic inputs",
            "completion_status": "CONTRACT_DECLARED_FORMULA_BODY_PENDING",
            "next_required_artifact": body_next,
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;posthoc_formula_switch",
        },
        {
            "component_id": "M0ND06_READOUT_MAP",
            "component_class": "formula_body_contract",
            "required_entry": "explicit source-to-rotation readout map producing v_pred_km_s on the frozen radial grid",
            "completion_status": "FORMULA_BODY_REQUIRED_NOT_FILLED",
            "next_required_artifact": body_next,
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
        {
            "component_id": "M0ND06_COEFFICIENT_POLICY",
            "component_class": "coefficient_freeze_contract",
            "required_entry": "allowed global coefficients and any per-galaxy privileges declared before endpoint scoring",
            "completion_status": "COEFFICIENT_POLICY_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_coefficient_policy_v07",
            "forbidden_inputs": "endpoint_residual;family_winner;posthoc_parameter_discount",
        },
        {
            "component_id": "M0ND06_FIXED_SCALES",
            "component_class": "scale_freeze_contract",
            "required_entry": "fixed radial and normalization scale policy shared with the scoring grid",
            "completion_status": "SCALE_POLICY_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_scale_policy_v07",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_scale_selection",
        },
        {
            "component_id": "M0ND06_FALLBACK_POLICY",
            "component_class": "fallback_policy_contract",
            "required_entry": "zero-response and missing-label fallback rules frozen before any family comparison",
            "completion_status": "FALLBACK_POLICY_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_fallback_policy_v07",
            "forbidden_inputs": "endpoint_residual;best_fit_curve;posthoc_exception",
        },
        {
            "component_id": "M0ND06_OUTPUT_SCHEMA",
            "component_class": "prediction_output_contract",
            "required_entry": "row-level v_pred_km_s output schema compatible with family_prediction_table_contract_v80",
            "completion_status": "OUTPUT_SCHEMA_READY_FORMULA_BODY_PENDING",
            "next_required_artifact": body_next,
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner",
        },
    ]
    for row in rows:
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_formula_table_contract_only_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    body_ready = all(row["completion_status"] == "READY" for row in rows)
    blocked = [row for row in rows if row["completion_status"] != "READY"]
    return [
        {
            "summary_id": "M0_NO_DARK_FORMULA_TABLE_CONTRACT_V06",
            "formula_artifact": "m0_no_dark_formula_table_v06",
            "required_components": len(rows),
            "ready_components": len(rows) - len(blocked),
            "blocked_components": len(blocked),
            "formula_body_rows_written": 0,
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": (
                "M0_NO_DARK_FORMULA_TABLE_READY_FOR_PREDICTION_ROWS"
                if body_ready
                else "M0_NO_DARK_FORMULA_TABLE_CONTRACT_READY_BODY_BLOCKED"
            ),
            "next_required_artifact": blocked[0]["next_required_artifact"] if blocked else "family_prediction_tables_v08.csv",
            "claim_boundary": "m0_no_dark_formula_table_contract_only_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = contract_rows()
    write_csv(
        DERIVED / "m0_no_dark_formula_table_contract_v06.csv",
        rows,
        [
            "component_id",
            "component_class",
            "required_entry",
            "completion_status",
            "next_required_artifact",
            "forbidden_inputs",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "m0_no_dark_formula_table_contract_summary_v06.csv",
        summary(rows),
        [
            "summary_id",
            "formula_artifact",
            "required_components",
            "ready_components",
            "blocked_components",
            "formula_body_rows_written",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_M0_NO_DARK_FORMULA_TABLE_CONTRACT_V06_BUILT")


if __name__ == "__main__":
    main()
