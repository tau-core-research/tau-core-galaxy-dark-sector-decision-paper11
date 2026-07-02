#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
PARENT_BASIS_SUMMARY = DERIVED / "m0_no_dark_rule_parent_assumption_basis_summary_v14.csv"
SELECTION_MAP_SUMMARY = DERIVED / "m0_no_dark_rule_selection_map_summary_v14.csv"
TERM_GENERATION_SUMMARY = DERIVED / "m0_no_dark_rule_term_generation_record_summary_v14.csv"
INVARIANCE_SUMMARY = DERIVED / "m0_no_dark_rule_invariance_null_checks_summary_v14.csv"
DIMENSIONAL_PRECHECK_SUMMARY = DERIVED / "m0_no_dark_rule_dimensional_precheck_summary_v14.csv"
DERIVATION_PROVENANCE_LEAKAGE_SUMMARY = DERIVED / "m0_no_dark_rule_derivation_provenance_leakage_summary_v14.csv"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parent_basis_ready() -> bool:
    if not PARENT_BASIS_SUMMARY.exists():
        return False
    with PARENT_BASIS_SUMMARY.open() as handle:
        rows = list(csv.DictReader(handle))
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_RULE_PARENT_ASSUMPTION_BASIS_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def selection_map_ready() -> bool:
    if not SELECTION_MAP_SUMMARY.exists():
        return False
    with SELECTION_MAP_SUMMARY.open() as handle:
        rows = list(csv.DictReader(handle))
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_RULE_SELECTION_MAP_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def term_generation_ready() -> bool:
    if not TERM_GENERATION_SUMMARY.exists():
        return False
    with TERM_GENERATION_SUMMARY.open() as handle:
        rows = list(csv.DictReader(handle))
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_RULE_TERM_GENERATION_RECORD_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def invariance_checks_ready() -> bool:
    if not INVARIANCE_SUMMARY.exists():
        return False
    with INVARIANCE_SUMMARY.open() as handle:
        rows = list(csv.DictReader(handle))
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_RULE_INVARIANCE_NULL_CHECKS_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def dimensional_precheck_ready() -> bool:
    if not DIMENSIONAL_PRECHECK_SUMMARY.exists():
        return False
    with DIMENSIONAL_PRECHECK_SUMMARY.open() as handle:
        rows = list(csv.DictReader(handle))
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_RULE_DIMENSIONAL_PRECHECK_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def derivation_provenance_leakage_ready() -> bool:
    if not DERIVATION_PROVENANCE_LEAKAGE_SUMMARY.exists():
        return False
    with DERIVATION_PROVENANCE_LEAKAGE_SUMMARY.open() as handle:
        rows = list(csv.DictReader(handle))
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_RULE_DERIVATION_PROVENANCE_LEAKAGE_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def contract_rows() -> list[dict[str, object]]:
    parent_ready = parent_basis_ready()
    selection_ready = selection_map_ready()
    term_ready = term_generation_ready()
    invariance_ready = invariance_checks_ready()
    dimensional_ready = dimensional_precheck_ready()
    provenance_ready = derivation_provenance_leakage_ready()
    rows = [
        {
            "derivation_slot_id": "M0NDER13_PARENT_ASSUMPTIONS",
            "derivation_slot_class": "parent_assumption_basis",
            "required_specification": "explicit Tau/source-side assumptions allowed to generate the no-dark rule family",
            "completion_status": "READY" if parent_ready else "PARENT_ASSUMPTION_BASIS_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_rule_parent_assumption_basis_v14",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
        {
            "derivation_slot_id": "M0NDER13_RULE_SELECTION_MAP",
            "derivation_slot_class": "rule_selection_map",
            "required_specification": "pre-endpoint map from source-side assumptions to candidate no-dark rule class",
            "completion_status": "READY" if selection_ready else "RULE_SELECTION_MAP_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_rule_selection_map_v14",
            "forbidden_inputs": "endpoint_residual;posthoc_label_switch;family_winner",
        },
        {
            "derivation_slot_id": "M0NDER13_TERM_GENERATION",
            "derivation_slot_class": "term_generation_record",
            "required_specification": "record showing how admissible expression terms are generated before fitting",
            "completion_status": "READY" if term_ready else "TERM_GENERATION_RECORD_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_rule_term_generation_record_v14",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_term_selection",
        },
        {
            "derivation_slot_id": "M0NDER13_INVARIANCE_CHECKS",
            "derivation_slot_class": "invariance_and_null_checks",
            "required_specification": "source-side invariance, null, gauge, and fallback checks for the rule family",
            "completion_status": "READY" if invariance_ready else "INVARIANCE_AND_NULL_CHECKS_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_rule_invariance_null_checks_v14",
            "forbidden_inputs": "endpoint_residual;best_fit_curve;posthoc_exception",
        },
        {
            "derivation_slot_id": "M0NDER13_DIMENSIONAL_PRECHECK",
            "derivation_slot_class": "dimensional_precheck",
            "required_specification": "pre-expression dimensional route showing that generated terms can feed a velocity readout",
            "completion_status": "READY" if dimensional_ready else "DIMENSIONAL_PRECHECK_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_rule_dimensional_precheck_v14",
            "forbidden_inputs": "endpoint_residual;heldout_score;posthoc_unit_rescale",
        },
        {
            "derivation_slot_id": "M0NDER13_PROVENANCE_AND_LEAKAGE",
            "derivation_slot_class": "derivation_provenance_leakage_audit",
            "required_specification": "audit trail proving the derivation record predates endpoint scoring and family outcomes",
            "completion_status": "READY" if provenance_ready else "DERIVATION_PROVENANCE_LEAKAGE_AUDIT_REQUIRED_NOT_FILLED",
            "next_required_artifact": "m0_no_dark_rule_derivation_provenance_leakage_v14",
            "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve",
        },
    ]
    for row in rows:
        row["derivation_claim_allowed"] = "false"
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_expression_rule_derivation_contract_only_no_derivation_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = [row for row in rows if row["completion_status"] != "READY"]
    if blocked:
        first_blocked_class = blocked[0]["derivation_slot_class"].upper()
        status = f"M0_NO_DARK_EXPRESSION_RULE_DERIVATION_CONTRACT_READY_{first_blocked_class}_BLOCKED"
    else:
        status = "M0_NO_DARK_EXPRESSION_RULE_DERIVATION_READY_FOR_SOURCE_BASIS"
    return [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_RULE_DERIVATION_CONTRACT_V13",
            "rule_derivation_artifact": "m0_no_dark_expression_rule_derivation_v13",
            "required_derivation_slots": len(rows),
            "ready_derivation_slots": ready,
            "blocked_derivation_slots": len(blocked),
            "derivation_records_written": 0,
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": status,
            "next_required_artifact": blocked[0]["next_required_artifact"] if blocked else "m0_no_dark_expression_source_basis_v13",
            "claim_boundary": "m0_no_dark_expression_rule_derivation_contract_only_no_derivation_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = contract_rows()
    write_csv(
        DERIVED / "m0_no_dark_expression_rule_derivation_contract_v13.csv",
        rows,
        [
            "derivation_slot_id",
            "derivation_slot_class",
            "required_specification",
            "completion_status",
            "next_required_artifact",
            "forbidden_inputs",
            "derivation_claim_allowed",
            "source_rule_claim_allowed",
            "expression_claim_allowed",
            "numeric_prediction_allowed",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "m0_no_dark_expression_rule_derivation_contract_summary_v13.csv",
        summary(rows),
        [
            "summary_id",
            "rule_derivation_artifact",
            "required_derivation_slots",
            "ready_derivation_slots",
            "blocked_derivation_slots",
            "derivation_records_written",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_M0_NO_DARK_EXPRESSION_RULE_DERIVATION_CONTRACT_V13_BUILT")


if __name__ == "__main__":
    main()
