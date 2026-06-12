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
    source_rule_contract_path = DERIVED / "m0_no_dark_expression_source_rule_contract_summary_v12.csv"
    source_rule_contract = read_csv(source_rule_contract_path)[0] if source_rule_contract_path.exists() else {}
    source_rule_next = (
        str(source_rule_contract["next_required_artifact"])
        if source_rule_contract
        else "m0_no_dark_expression_source_rule_v12"
    )
    rows = [
        {
            "freeze_slot_id": "M0NDFE11_SOURCE_RULE",
            "freeze_slot_class": "source_rule",
            "required_specification": "source-side derivation rule selecting the no-dark response form before endpoint data are used",
            "completion_status": "SOURCE_RULE_REQUIRED_NOT_FILLED",
            "next_required_artifact": source_rule_next,
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
        {
            "freeze_slot_id": "M0NDFE11_SYMBOLIC_FORM",
            "freeze_slot_class": "symbolic_or_algorithmic_form",
            "required_specification": "complete symbolic or algorithmic expression body produced by the source rule",
            "completion_status": "SYMBOLIC_FORM_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_symbolic_form_v12",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;posthoc_formula_switch",
        },
        {
            "freeze_slot_id": "M0NDFE11_INPUT_DOMAIN",
            "freeze_slot_class": "input_domain",
            "required_specification": "allowed radial, baryonic, morphology/readout, and null/fallback input domain",
            "completion_status": "INPUT_DOMAIN_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_input_domain_v12",
            "forbidden_inputs": "endpoint_residual;posthoc_label_switch;family_winner",
        },
        {
            "freeze_slot_id": "M0NDFE11_COEFFICIENT_FREEZE",
            "freeze_slot_class": "coefficient_freeze",
            "required_specification": "fixed/free coefficient policy with parameter-count exposure before prediction writing",
            "completion_status": "COEFFICIENT_FREEZE_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_coefficient_freeze_v12",
            "forbidden_inputs": "endpoint_residual;family_winner;posthoc_parameter_discount",
        },
        {
            "freeze_slot_id": "M0NDFE11_DIMENSIONAL_AUDIT",
            "freeze_slot_class": "dimensional_audit",
            "required_specification": "unit path from declared inputs to km/s velocity output with no posthoc rescale",
            "completion_status": "DIMENSIONAL_AUDIT_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_dimensional_audit_v12",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_unit_rescale",
        },
        {
            "freeze_slot_id": "M0NDFE11_MACHINE_FORM",
            "freeze_slot_class": "machine_form",
            "required_specification": "serialized expression or callable contract for the later prediction writer",
            "completion_status": "MACHINE_FORM_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_machine_form_v12",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner",
        },
    ]
    for row in rows:
        row["frozen_expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_frozen_expression_contract_only_no_expression_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = [row for row in rows if row["completion_status"] != "READY"]
    return [
        {
            "summary_id": "M0_NO_DARK_FROZEN_EXPRESSION_CONTRACT_V11",
            "frozen_expression_artifact": "m0_no_dark_frozen_expression_v11",
            "required_freeze_slots": len(rows),
            "ready_freeze_slots": ready,
            "blocked_freeze_slots": len(blocked),
            "frozen_expressions_written": 0,
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FROZEN_EXPRESSION_CONTRACT_READY_SOURCE_RULE_BLOCKED"
            if blocked
            else "M0_NO_DARK_FROZEN_EXPRESSION_READY_FOR_PREDICTION_WRITER",
            "next_required_artifact": blocked[0]["next_required_artifact"] if blocked else "family_prediction_tables_v08.csv",
            "claim_boundary": "m0_no_dark_frozen_expression_contract_only_no_expression_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = contract_rows()
    write_csv(
        DERIVED / "m0_no_dark_frozen_expression_contract_v11.csv",
        rows,
        [
            "freeze_slot_id",
            "freeze_slot_class",
            "required_specification",
            "completion_status",
            "next_required_artifact",
            "forbidden_inputs",
            "frozen_expression_claim_allowed",
            "formula_claim_allowed",
            "numeric_prediction_allowed",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "m0_no_dark_frozen_expression_contract_summary_v11.csv",
        summary(rows),
        [
            "summary_id",
            "frozen_expression_artifact",
            "required_freeze_slots",
            "ready_freeze_slots",
            "blocked_freeze_slots",
            "frozen_expressions_written",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_M0_NO_DARK_FROZEN_EXPRESSION_CONTRACT_V11_BUILT")


if __name__ == "__main__":
    main()
