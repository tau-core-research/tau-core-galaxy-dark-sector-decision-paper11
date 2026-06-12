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
            "source_rule_slot_id": "M0NDESR12_RULE_DERIVATION",
            "source_rule_slot_class": "rule_derivation",
            "required_specification": "pre-endpoint derivation record for selecting the no-dark source-to-readout rule family",
            "completion_status": "RULE_DERIVATION_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_rule_derivation_v13",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
        {
            "source_rule_slot_id": "M0NDESR12_SOURCE_BASIS",
            "source_rule_slot_class": "source_basis",
            "required_specification": "allowed Tau/morphology/readout source-side basis terms before any velocity fit",
            "completion_status": "SOURCE_BASIS_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_source_basis_v13",
            "forbidden_inputs": "endpoint_residual;posthoc_label_switch;family_winner",
        },
        {
            "source_rule_slot_id": "M0NDESR12_ADMISSIBILITY",
            "source_rule_slot_class": "admissibility_rule",
            "required_specification": "admissibility gate for which source-side terms may enter the no-dark expression",
            "completion_status": "ADMISSIBILITY_RULE_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_admissibility_rule_v13",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_term_selection",
        },
        {
            "source_rule_slot_id": "M0NDESR12_NULL_AND_FALLBACK",
            "source_rule_slot_class": "null_and_fallback_policy",
            "required_specification": "null, gauge, missing-input, and fallback behavior before prediction writing",
            "completion_status": "NULL_AND_FALLBACK_POLICY_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_null_fallback_policy_v13",
            "forbidden_inputs": "endpoint_residual;best_fit_curve;posthoc_exception",
        },
        {
            "source_rule_slot_id": "M0NDESR12_OUTPUT_CLASS",
            "source_rule_slot_class": "output_class",
            "required_specification": "declared expression output class and allowed handoff to symbolic or algorithmic form",
            "completion_status": "OUTPUT_CLASS_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_output_class_v13",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner",
        },
        {
            "source_rule_slot_id": "M0NDESR12_LEAKAGE_AUDIT",
            "source_rule_slot_class": "source_rule_leakage_audit",
            "required_specification": "audit proving the source rule was not selected from endpoint residuals or family outcome",
            "completion_status": "SOURCE_RULE_LEAKAGE_AUDIT_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_source_rule_leakage_audit_v13",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
    ]
    for row in rows:
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_expression_source_rule_contract_only_no_rule_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = [row for row in rows if row["completion_status"] != "READY"]
    return [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_SOURCE_RULE_CONTRACT_V12",
            "source_rule_artifact": "m0_no_dark_expression_source_rule_v12",
            "required_source_rule_slots": len(rows),
            "ready_source_rule_slots": ready,
            "blocked_source_rule_slots": len(blocked),
            "source_rules_written": 0,
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_SOURCE_RULE_CONTRACT_READY_DERIVATION_BLOCKED"
            if blocked
            else "M0_NO_DARK_EXPRESSION_SOURCE_RULE_READY_FOR_SYMBOLIC_FORM",
            "next_required_artifact": blocked[0]["next_required_artifact"] if blocked else "m0_no_dark_expression_symbolic_form_v12",
            "claim_boundary": "m0_no_dark_expression_source_rule_contract_only_no_rule_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = contract_rows()
    write_csv(
        DERIVED / "m0_no_dark_expression_source_rule_contract_v12.csv",
        rows,
        [
            "source_rule_slot_id",
            "source_rule_slot_class",
            "required_specification",
            "completion_status",
            "next_required_artifact",
            "forbidden_inputs",
            "source_rule_claim_allowed",
            "expression_claim_allowed",
            "numeric_prediction_allowed",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "m0_no_dark_expression_source_rule_contract_summary_v12.csv",
        summary(rows),
        [
            "summary_id",
            "source_rule_artifact",
            "required_source_rule_slots",
            "ready_source_rule_slots",
            "blocked_source_rule_slots",
            "source_rules_written",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_M0_NO_DARK_EXPRESSION_SOURCE_RULE_CONTRACT_V12_BUILT")


if __name__ == "__main__":
    main()
