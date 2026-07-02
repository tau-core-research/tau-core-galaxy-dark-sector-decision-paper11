#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DERIVATION_CONTRACT_SUMMARY = DERIVED / "m0_no_dark_expression_rule_derivation_contract_summary_v13.csv"
SOURCE_BASIS_SUMMARY = DERIVED / "m0_no_dark_expression_source_basis_summary_v13.csv"
ADMISSIBILITY_SUMMARY = DERIVED / "m0_no_dark_expression_admissibility_rule_summary_v13.csv"
NULL_FALLBACK_SUMMARY = DERIVED / "m0_no_dark_expression_null_fallback_policy_summary_v13.csv"
OUTPUT_CLASS_SUMMARY = DERIVED / "m0_no_dark_expression_output_class_summary_v13.csv"
SOURCE_RULE_LEAKAGE_AUDIT_SUMMARY = DERIVED / "m0_no_dark_expression_source_rule_leakage_audit_summary_v13.csv"


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


def derivation_contract_ready() -> bool:
    if not DERIVATION_CONTRACT_SUMMARY.exists():
        return False
    rows = read_csv(DERIVATION_CONTRACT_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_RULE_DERIVATION_READY_FOR_SOURCE_BASIS"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def source_basis_ready() -> bool:
    if not SOURCE_BASIS_SUMMARY.exists():
        return False
    rows = read_csv(SOURCE_BASIS_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_SOURCE_BASIS_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def admissibility_ready() -> bool:
    if not ADMISSIBILITY_SUMMARY.exists():
        return False
    rows = read_csv(ADMISSIBILITY_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_ADMISSIBILITY_RULE_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def null_fallback_ready() -> bool:
    if not NULL_FALLBACK_SUMMARY.exists():
        return False
    rows = read_csv(NULL_FALLBACK_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_NULL_FALLBACK_POLICY_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def output_class_ready() -> bool:
    if not OUTPUT_CLASS_SUMMARY.exists():
        return False
    rows = read_csv(OUTPUT_CLASS_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_OUTPUT_CLASS_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def source_rule_leakage_audit_ready() -> bool:
    if not SOURCE_RULE_LEAKAGE_AUDIT_SUMMARY.exists():
        return False
    rows = read_csv(SOURCE_RULE_LEAKAGE_AUDIT_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_SOURCE_RULE_LEAKAGE_AUDIT_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def contract_rows() -> list[dict[str, object]]:
    derivation_contract_path = DERIVATION_CONTRACT_SUMMARY
    derivation_contract = read_csv(derivation_contract_path)[0] if derivation_contract_path.exists() else {}
    derivation_next = (
        str(derivation_contract["next_required_artifact"])
        if derivation_contract
        else "m0_no_dark_expression_rule_derivation_v13"
    )
    rows = [
        {
            "source_rule_slot_id": "M0NDESR12_RULE_DERIVATION",
            "source_rule_slot_class": "rule_derivation",
            "required_specification": "pre-endpoint derivation record for selecting the no-dark source-to-readout rule family",
            "completion_status": "READY" if derivation_contract_ready() else "RULE_DERIVATION_REQUIRED_NOT_FILLED",
            "next_required_artifact": derivation_next,
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
        {
            "source_rule_slot_id": "M0NDESR12_SOURCE_BASIS",
            "source_rule_slot_class": "source_basis",
            "required_specification": "allowed Tau/morphology/readout source-side basis terms before any velocity fit",
            "completion_status": "READY" if source_basis_ready() else "SOURCE_BASIS_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_source_basis_v13",
            "forbidden_inputs": "endpoint_residual;posthoc_label_switch;family_winner",
        },
        {
            "source_rule_slot_id": "M0NDESR12_ADMISSIBILITY",
            "source_rule_slot_class": "admissibility_rule",
            "required_specification": "admissibility gate for which source-side terms may enter the no-dark expression",
            "completion_status": "READY" if admissibility_ready() else "ADMISSIBILITY_RULE_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_admissibility_rule_v13",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_term_selection",
        },
        {
            "source_rule_slot_id": "M0NDESR12_NULL_AND_FALLBACK",
            "source_rule_slot_class": "null_and_fallback_policy",
            "required_specification": "null, gauge, missing-input, and fallback behavior before prediction writing",
            "completion_status": "READY" if null_fallback_ready() else "NULL_AND_FALLBACK_POLICY_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_null_fallback_policy_v13",
            "forbidden_inputs": "endpoint_residual;best_fit_curve;posthoc_exception",
        },
        {
            "source_rule_slot_id": "M0NDESR12_OUTPUT_CLASS",
            "source_rule_slot_class": "output_class",
            "required_specification": "declared expression output class and allowed handoff to symbolic or algorithmic form",
            "completion_status": "READY" if output_class_ready() else "OUTPUT_CLASS_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_expression_output_class_v13",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner",
        },
        {
            "source_rule_slot_id": "M0NDESR12_LEAKAGE_AUDIT",
            "source_rule_slot_class": "source_rule_leakage_audit",
            "required_specification": "audit proving the source rule was not selected from endpoint residuals or family outcome",
            "completion_status": "READY" if source_rule_leakage_audit_ready() else "SOURCE_RULE_LEAKAGE_AUDIT_REQUIRED_NOT_FILLED",
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
    if blocked:
        first_blocked_class = blocked[0]["source_rule_slot_class"].upper()
        status = f"M0_NO_DARK_EXPRESSION_SOURCE_RULE_CONTRACT_READY_{first_blocked_class}_BLOCKED"
    else:
        status = "M0_NO_DARK_EXPRESSION_SOURCE_RULE_READY_FOR_SYMBOLIC_FORM"
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
            "overall_status": status,
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
