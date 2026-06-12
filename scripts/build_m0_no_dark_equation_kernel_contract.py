#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def contract_rows() -> list[dict[str, object]]:
    rows = [
        {
            "kernel_slot_id": "M0NDEK09_EXPRESSION",
            "kernel_slot_class": "kernel_expression",
            "required_specification": "frozen symbolic or algorithmic expression for the no-dark velocity readout kernel",
            "completion_status": "KERNEL_EXPRESSION_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_kernel_expression_v10",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
        {
            "kernel_slot_id": "M0NDEK09_INPUT_BINDING",
            "kernel_slot_class": "input_binding",
            "required_specification": "binding from declared source/baryonic/radial arguments to kernel variables",
            "completion_status": "INPUT_BINDING_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_kernel_input_binding_v10",
            "forbidden_inputs": "endpoint_residual;posthoc_label_switch;family_winner",
        },
        {
            "kernel_slot_id": "M0NDEK09_OUTPUT_MAP",
            "kernel_slot_class": "output_map",
            "required_specification": "map from kernel output to v_pred_km_s rows on the frozen radial grid",
            "completion_status": "OUTPUT_MAP_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_kernel_output_map_v10",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_unit_rescale",
        },
        {
            "kernel_slot_id": "M0NDEK09_PARAMETER_AUDIT",
            "kernel_slot_class": "parameter_audit",
            "required_specification": "parameter exposure table for every coefficient, switch, branch, and scale used by the kernel",
            "completion_status": "PARAMETER_AUDIT_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_kernel_parameter_audit_v10",
            "forbidden_inputs": "endpoint_residual;family_winner;posthoc_parameter_discount",
        },
        {
            "kernel_slot_id": "M0NDEK09_FAILURE_POLICY",
            "kernel_slot_class": "failure_policy",
            "required_specification": "invalid-input, missing-source, and zero-response behavior before any predictions are written",
            "completion_status": "FAILURE_POLICY_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_kernel_failure_policy_v10",
            "forbidden_inputs": "endpoint_residual;best_fit_curve;posthoc_exception",
        },
        {
            "kernel_slot_id": "M0NDEK09_REPRODUCIBLE_HOOK",
            "kernel_slot_class": "reproducible_hook",
            "required_specification": "machine hook or expression serialization callable by the later prediction writer",
            "completion_status": "REPRODUCIBLE_HOOK_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_kernel_reproducible_hook_v10",
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
            "kernel_expressions_written": 0,
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
