#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
INTERFACE_SUMMARY = DERIVED / "m0_no_dark_kernel_expression_interface_summary_v10.csv"
PAYLOAD_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_payload_summary_v11.csv"
BODY_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_body_summary_v14.csv"


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


def interface_ready() -> bool:
    if not INTERFACE_SUMMARY.exists():
        return False
    rows = read_csv(INTERFACE_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_KERNEL_EXPRESSION_INTERFACE_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def body_ready() -> bool:
    if not BODY_SUMMARY.exists():
        return False
    rows = read_csv(BODY_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_FROZEN_EXPRESSION_BODY_READY_FOR_KERNEL_EXPRESSION_REVIEW"
        and rows[0]["velocity_formula_written"] == "false"
        and rows[0]["numeric_predictions_written"] == "0"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["dark_sector_verdict_allowed"] == "false"
    )


def interface_next() -> str:
    if PAYLOAD_SUMMARY.exists():
        rows = read_csv(PAYLOAD_SUMMARY)
        if len(rows) == 1:
            return rows[0]["next_required_artifact"]
    if not INTERFACE_SUMMARY.exists():
        return "m0_no_dark_frozen_expression_payload_v11"
    rows = read_csv(INTERFACE_SUMMARY)
    if len(rows) != 1:
        return "m0_no_dark_frozen_expression_payload_v11"
    return rows[0]["next_required_artifact"]


def contract_rows() -> list[dict[str, object]]:
    next_payload = interface_next()
    frozen_body_ready = body_ready()
    rows = [
        {
            "expression_slot_id": "M0NDKE10_FROZEN_EXPRESSION",
            "expression_slot_class": "frozen_expression",
            "required_specification": "complete symbolic or algorithmic expression with no endpoint-selected terms",
            "completion_status": "READY" if frozen_body_ready else "FROZEN_EXPRESSION_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_frozen_expression_body_v14" if frozen_body_ready else next_payload,
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
        {
            "expression_slot_id": "M0NDKE10_VARIABLE_BINDINGS",
            "expression_slot_class": "variable_binding",
            "required_specification": "one-to-one mapping between expression symbols and source-side input columns",
            "completion_status": "READY" if interface_ready() else "VARIABLE_BINDINGS_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_kernel_expression_interface_v10",
            "forbidden_inputs": "endpoint_residual;posthoc_label_switch;family_winner",
        },
        {
            "expression_slot_id": "M0NDKE10_CONSTANTS",
            "expression_slot_class": "constant_declaration",
            "required_specification": "all constants with fixed/free status, units, and parameter-count treatment",
            "completion_status": "READY" if interface_ready() else "CONSTANT_DECLARATION_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_kernel_expression_interface_v10",
            "forbidden_inputs": "endpoint_residual;family_winner;posthoc_parameter_discount",
        },
        {
            "expression_slot_id": "M0NDKE10_DIMENSIONAL_PATH",
            "expression_slot_class": "dimensional_path",
            "required_specification": "dimensional derivation from expression inputs to km/s velocity output",
            "completion_status": "READY" if interface_ready() else "DIMENSIONAL_PATH_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_kernel_expression_interface_v10",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_unit_rescale",
        },
        {
            "expression_slot_id": "M0NDKE10_SERIALIZED_FORM",
            "expression_slot_class": "serialized_form",
            "required_specification": "machine-readable expression form for later prediction writer execution",
            "completion_status": "READY" if interface_ready() else "SERIALIZED_FORM_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_kernel_expression_interface_v10",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner",
        },
    ]
    for row in rows:
        row["expression_claim_allowed"] = (
            "true"
            if row["expression_slot_id"] == "M0NDKE10_FROZEN_EXPRESSION" and body_ready()
            else "false"
        )
        row["kernel_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_kernel_expression_contract_expression_body_only_no_velocity_formula_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = [row for row in rows if row["completion_status"] != "READY"]
    return [
        {
            "summary_id": "M0_NO_DARK_KERNEL_EXPRESSION_CONTRACT_V10",
            "kernel_expression_artifact": "m0_no_dark_kernel_expression_v10",
            "required_expression_slots": len(rows),
            "ready_expression_slots": ready,
            "blocked_expression_slots": len(blocked),
            "frozen_expressions_written": 1 if body_ready() else 0,
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_KERNEL_EXPRESSION_CONTRACT_READY_FROZEN_EXPRESSION_BLOCKED"
            if blocked
            else "M0_NO_DARK_KERNEL_EXPRESSION_READY_FOR_KERNEL_FREEZE",
            "next_required_artifact": blocked[0]["next_required_artifact"] if blocked else "m0_no_dark_equation_kernel_v09",
            "claim_boundary": "m0_no_dark_kernel_expression_contract_only_no_expression_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = contract_rows()
    write_csv(
        DERIVED / "m0_no_dark_kernel_expression_contract_v10.csv",
        rows,
        [
            "expression_slot_id",
            "expression_slot_class",
            "required_specification",
            "completion_status",
            "next_required_artifact",
            "forbidden_inputs",
            "expression_claim_allowed",
            "kernel_claim_allowed",
            "numeric_prediction_allowed",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "m0_no_dark_kernel_expression_contract_summary_v10.csv",
        summary(rows),
        [
            "summary_id",
            "kernel_expression_artifact",
            "required_expression_slots",
            "ready_expression_slots",
            "blocked_expression_slots",
            "frozen_expressions_written",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_M0_NO_DARK_KERNEL_EXPRESSION_CONTRACT_V10_BUILT")


if __name__ == "__main__":
    main()
