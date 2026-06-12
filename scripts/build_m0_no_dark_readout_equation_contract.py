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
    kernel_contract_path = DERIVED / "m0_no_dark_equation_kernel_contract_summary_v09.csv"
    kernel_contract = read_csv(kernel_contract_path)[0] if kernel_contract_path.exists() else {}
    kernel_next = (
        str(kernel_contract["next_required_artifact"])
        if kernel_contract
        else "m0_no_dark_equation_kernel_v09"
    )
    rows = [
        {
            "equation_slot_id": "M0NDRE08_KERNEL",
            "equation_slot_class": "equation_kernel",
            "required_specification": "explicit frozen algebraic or algorithmic kernel mapping declared arguments to a velocity prediction",
            "completion_status": "EQUATION_KERNEL_REQUIRED_NOT_FILLED",
            "next_required_artifact": kernel_next,
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
        {
            "equation_slot_id": "M0NDRE08_ARGUMENT_SIGNATURE",
            "equation_slot_class": "argument_signature",
            "required_specification": "ordered signature of all source, baryonic, radial, scale, and coefficient arguments",
            "completion_status": "ARGUMENT_SIGNATURE_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_argument_signature_v09",
            "forbidden_inputs": "endpoint_residual;posthoc_label_switch;family_winner",
        },
        {
            "equation_slot_id": "M0NDRE08_UNITS",
            "equation_slot_class": "dimensional_contract",
            "required_specification": "unit path showing the kernel output is v_pred_km_s at each frozen radial grid point",
            "completion_status": "DIMENSIONAL_CONTRACT_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_equation_unit_path_v09",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_unit_rescale",
        },
        {
            "equation_slot_id": "M0NDRE08_PARAMETERS",
            "equation_slot_class": "parameter_exposure",
            "required_specification": "all constants and switches exposed to the numeric parameter-count ledger",
            "completion_status": "PARAMETER_EXPOSURE_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_equation_parameter_exposure_v09",
            "forbidden_inputs": "endpoint_residual;family_winner;posthoc_parameter_discount",
        },
        {
            "equation_slot_id": "M0NDRE08_DOMAIN",
            "equation_slot_class": "domain_and_failure_modes",
            "required_specification": "valid input domain plus invalid-input behavior before prediction rows are written",
            "completion_status": "DOMAIN_CONTRACT_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_equation_domain_v09",
            "forbidden_inputs": "endpoint_residual;best_fit_curve;posthoc_exception",
        },
        {
            "equation_slot_id": "M0NDRE08_SERIALIZATION",
            "equation_slot_class": "machine_serialization",
            "required_specification": "machine-readable expression or implementation hook usable by the family prediction writer",
            "completion_status": "SERIALIZATION_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_equation_serialization_v09",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner",
        },
    ]
    for row in rows:
        row["equation_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_readout_equation_contract_only_no_equation_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = [row for row in rows if row["completion_status"] != "READY"]
    return [
        {
            "summary_id": "M0_NO_DARK_READOUT_EQUATION_CONTRACT_V08",
            "readout_equation_artifact": "m0_no_dark_readout_equation_v08",
            "required_equation_slots": len(rows),
            "ready_equation_slots": ready,
            "blocked_equation_slots": len(blocked),
            "equations_written": 0,
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_READOUT_EQUATION_CONTRACT_READY_KERNEL_BLOCKED"
            if blocked
            else "M0_NO_DARK_READOUT_EQUATION_READY_FOR_FORMULA_BODY",
            "next_required_artifact": blocked[0]["next_required_artifact"] if blocked else "m0_no_dark_formula_body_v07",
            "claim_boundary": "m0_no_dark_readout_equation_contract_only_no_equation_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = contract_rows()
    write_csv(
        DERIVED / "m0_no_dark_readout_equation_contract_v08.csv",
        rows,
        [
            "equation_slot_id",
            "equation_slot_class",
            "required_specification",
            "completion_status",
            "next_required_artifact",
            "forbidden_inputs",
            "equation_claim_allowed",
            "numeric_prediction_allowed",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "m0_no_dark_readout_equation_contract_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "readout_equation_artifact",
            "required_equation_slots",
            "ready_equation_slots",
            "blocked_equation_slots",
            "equations_written",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_M0_NO_DARK_READOUT_EQUATION_CONTRACT_V08_BUILT")


if __name__ == "__main__":
    main()
