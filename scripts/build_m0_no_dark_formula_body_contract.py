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
            "body_slot_id": "M0NDB07_READOUT_EQUATION",
            "body_slot_class": "readout_equation",
            "required_specification": "single source-to-rotation equation mapping frozen Tau/source inputs to v_pred_km_s",
            "completion_status": "READOUT_EQUATION_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_readout_equation_v08",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
        {
            "body_slot_id": "M0NDB07_SOURCE_ARGUMENTS",
            "body_slot_class": "source_argument_declaration",
            "required_specification": "complete list of allowed source-side morphology/readout arguments",
            "completion_status": "SOURCE_ARGUMENTS_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_source_argument_table_v08",
            "forbidden_inputs": "endpoint_residual;posthoc_label_switch;family_winner",
        },
        {
            "body_slot_id": "M0NDB07_BARYONIC_HANDOFF",
            "body_slot_class": "shared_baryonic_handoff",
            "required_specification": "explicit handoff rule for shared baryonic velocity components used by M0",
            "completion_status": "BARYONIC_HANDOFF_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_baryonic_handoff_v08",
            "forbidden_inputs": "endpoint_residual;posthoc_mass_model;family_winner",
        },
        {
            "body_slot_id": "M0NDB07_SCALE_LAW",
            "body_slot_class": "scale_law",
            "required_specification": "radial scale and normalization law declared before any endpoint residual inspection",
            "completion_status": "SCALE_LAW_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_scale_law_v08",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_scale_selection",
        },
        {
            "body_slot_id": "M0NDB07_COEFFICIENT_DOMAIN",
            "body_slot_class": "coefficient_domain",
            "required_specification": "allowed constants, fixed/free status, units, and parameter-count impact",
            "completion_status": "COEFFICIENT_DOMAIN_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_coefficient_domain_v08",
            "forbidden_inputs": "endpoint_residual;family_winner;posthoc_parameter_discount",
        },
        {
            "body_slot_id": "M0NDB07_FALLBACK_BRANCHES",
            "body_slot_class": "fallback_branching",
            "required_specification": "zero-response, missing-label, and invalid-input branch rules",
            "completion_status": "FALLBACK_BRANCHES_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_fallback_branches_v08",
            "forbidden_inputs": "endpoint_residual;best_fit_curve;posthoc_exception",
        },
        {
            "body_slot_id": "M0NDB07_OUTPUT_UNIT_CHECK",
            "body_slot_class": "output_unit_contract",
            "required_specification": "dimensional path proving the readout output is velocity in km/s on the frozen radial grid",
            "completion_status": "OUTPUT_UNIT_CHECK_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_output_unit_check_v08",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner",
        },
    ]
    for row in rows:
        row["formula_claim_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_formula_body_contract_only_no_formula_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = [row for row in rows if row["completion_status"] != "READY"]
    return [
        {
            "summary_id": "M0_NO_DARK_FORMULA_BODY_CONTRACT_V07",
            "formula_body_artifact": "m0_no_dark_formula_body_v07",
            "required_body_slots": len(rows),
            "ready_body_slots": ready,
            "blocked_body_slots": len(blocked),
            "formula_equations_written": 0,
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FORMULA_BODY_CONTRACT_READY_EQUATION_BLOCKED"
            if blocked
            else "M0_NO_DARK_FORMULA_BODY_READY_FOR_TABLE_FREEZE",
            "next_required_artifact": blocked[0]["next_required_artifact"] if blocked else "m0_no_dark_formula_table_v06",
            "claim_boundary": "m0_no_dark_formula_body_contract_only_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = contract_rows()
    write_csv(
        DERIVED / "m0_no_dark_formula_body_contract_v07.csv",
        rows,
        [
            "body_slot_id",
            "body_slot_class",
            "required_specification",
            "completion_status",
            "next_required_artifact",
            "forbidden_inputs",
            "formula_claim_allowed",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "m0_no_dark_formula_body_contract_summary_v07.csv",
        summary(rows),
        [
            "summary_id",
            "formula_body_artifact",
            "required_body_slots",
            "ready_body_slots",
            "blocked_body_slots",
            "formula_equations_written",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_M0_NO_DARK_FORMULA_BODY_CONTRACT_V07_BUILT")


if __name__ == "__main__":
    main()
