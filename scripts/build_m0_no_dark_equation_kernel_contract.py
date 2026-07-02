#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
INTERFACE_SUMMARY = DERIVED / "m0_no_dark_equation_kernel_interface_summary_v09.csv"
EXPRESSION_SUMMARY = DERIVED / "m0_no_dark_kernel_expression_contract_summary_v10.csv"


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
        and rows[0]["overall_status"] == "M0_NO_DARK_EQUATION_KERNEL_INTERFACE_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def expression_ready() -> bool:
    if not EXPRESSION_SUMMARY.exists():
        return False
    rows = read_csv(EXPRESSION_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_KERNEL_EXPRESSION_READY_FOR_KERNEL_FREEZE"
        and rows[0]["frozen_expressions_written"] == "1"
        and rows[0]["numeric_predictions_written"] == "0"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def contract_rows() -> list[dict[str, object]]:
    expression_contract_path = DERIVED / "m0_no_dark_kernel_expression_contract_summary_v10.csv"
    expression_contract = read_csv(expression_contract_path)[0] if expression_contract_path.exists() else {}
    expression_next = (
        str(expression_contract["next_required_artifact"])
        if expression_contract
        else "m0_no_dark_kernel_expression_v10"
    )
    rows = [
        {
            "kernel_slot_id": "M0NDEK09_EXPRESSION",
            "kernel_slot_class": "kernel_expression",
            "required_specification": "frozen symbolic or algorithmic expression for the no-dark velocity readout kernel",
            "completion_status": "READY" if expression_ready() else "KERNEL_EXPRESSION_REQUIRED_NOT_FILLED",
            "next_required_artifact": (
                "m0_no_dark_kernel_expression_contract_v10" if expression_ready() else expression_next
            ),
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
        {
            "kernel_slot_id": "M0NDEK09_INPUT_BINDING",
            "kernel_slot_class": "input_binding",
            "required_specification": "binding from declared source/baryonic/radial arguments to kernel variables",
            "completion_status": "READY" if interface_ready() else "INPUT_BINDING_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_equation_kernel_interface_v09",
            "forbidden_inputs": "endpoint_residual;posthoc_label_switch;family_winner",
        },
        {
            "kernel_slot_id": "M0NDEK09_OUTPUT_MAP",
            "kernel_slot_class": "output_map",
            "required_specification": "map from kernel output to v_pred_km_s rows on the frozen radial grid",
            "completion_status": "READY" if interface_ready() else "OUTPUT_MAP_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_equation_kernel_interface_v09",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_unit_rescale",
        },
        {
            "kernel_slot_id": "M0NDEK09_PARAMETER_AUDIT",
            "kernel_slot_class": "parameter_audit",
            "required_specification": "parameter exposure table for every coefficient, switch, branch, and scale used by the kernel",
            "completion_status": "READY" if interface_ready() else "PARAMETER_AUDIT_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_equation_kernel_interface_v09",
            "forbidden_inputs": "endpoint_residual;family_winner;posthoc_parameter_discount",
        },
        {
            "kernel_slot_id": "M0NDEK09_FAILURE_POLICY",
            "kernel_slot_class": "failure_policy",
            "required_specification": "invalid-input, missing-source, and zero-response behavior before any predictions are written",
            "completion_status": "READY" if interface_ready() else "FAILURE_POLICY_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_equation_kernel_interface_v09",
            "forbidden_inputs": "endpoint_residual;best_fit_curve;posthoc_exception",
        },
        {
            "kernel_slot_id": "M0NDEK09_REPRODUCIBLE_HOOK",
            "kernel_slot_class": "reproducible_hook",
            "required_specification": "machine hook or expression serialization callable by the later prediction writer",
            "completion_status": "READY" if interface_ready() else "REPRODUCIBLE_HOOK_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_equation_kernel_interface_v09",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner",
        },
    ]
    for row in rows:
        row["kernel_claim_allowed"] = "false"
        row["equation_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_equation_kernel_contract_only_no_kernel_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = [row for row in rows if row["completion_status"] != "READY"]
    return [
        {
            "summary_id": "M0_NO_DARK_EQUATION_KERNEL_CONTRACT_V09",
            "equation_kernel_artifact": "m0_no_dark_equation_kernel_v09",
            "required_kernel_slots": len(rows),
            "ready_kernel_slots": ready,
            "blocked_kernel_slots": len(blocked),
            "kernel_expressions_written": 1 if expression_ready() else 0,
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EQUATION_KERNEL_CONTRACT_READY_EXPRESSION_BLOCKED"
            if blocked
            else "M0_NO_DARK_EQUATION_KERNEL_READY_FOR_READOUT_EQUATION",
            "next_required_artifact": blocked[0]["next_required_artifact"] if blocked else "m0_no_dark_readout_equation_v08",
            "claim_boundary": "m0_no_dark_equation_kernel_contract_only_no_kernel_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = contract_rows()
    write_csv(
        DERIVED / "m0_no_dark_equation_kernel_contract_v09.csv",
        rows,
        [
            "kernel_slot_id",
            "kernel_slot_class",
            "required_specification",
            "completion_status",
            "next_required_artifact",
            "forbidden_inputs",
            "kernel_claim_allowed",
            "equation_claim_allowed",
            "numeric_prediction_allowed",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "m0_no_dark_equation_kernel_contract_summary_v09.csv",
        summary(rows),
        [
            "summary_id",
            "equation_kernel_artifact",
            "required_kernel_slots",
            "ready_kernel_slots",
            "blocked_kernel_slots",
            "kernel_expressions_written",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_M0_NO_DARK_EQUATION_KERNEL_CONTRACT_V09_BUILT")


if __name__ == "__main__":
    main()
