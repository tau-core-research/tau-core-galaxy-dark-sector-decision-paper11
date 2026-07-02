#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
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


def row_gates() -> list[dict[str, object]]:
    scoring_source = DERIVED / "activated_scoring_rows_v10.csv"
    scoring_rows = read_csv(scoring_source if scoring_source.exists() else DERIVED / "activated_scoring_rows_v08.csv")
    value_gates = {row["galaxy_id"]: row for row in read_csv(DERIVED / "source_import_real_values_gate_v12.csv")}
    leakage = {row["galaxy_id"]: row for row in read_csv(DERIVED / "leakage_audit_findings_v09.csv")}
    out: list[dict[str, object]] = []
    for row in scoring_rows:
        galaxy_id = row["galaxy_id"]
        value_row = value_gates[galaxy_id]
        leakage_row = leakage[galaxy_id]
        blockers = []
        if value_row["real_value_gate_status"] != "REAL_VALUES_PRESENT_VALIDATION_PENDING_LEAKAGE":
            blockers.append("real_source_values_missing")
        if leakage_row["leakage_status"] != "LEAKAGE_AUDIT_PASS":
            blockers.append("leakage_audit_not_passed")
        if row["activation_status"] != "ACTIVATED":
            blockers.append("source_row_not_activated")
        out.append(
            {
                "activation_gate_id": row["scoring_row_id"].replace("ASR08", "SAG13"),
                "galaxy_id": galaxy_id,
                "proposed_split": row["proposed_split"],
                "real_value_gate_status": value_row["real_value_gate_status"],
                "leakage_audit_status": leakage_row["leakage_status"],
                "row_activation_status": row["activation_status"],
                "blocking_requirements": ";".join(blockers),
                "activation_decision": "DO_NOT_ACTIVATE" if blockers else "ACTIVATE_FOR_SCORING",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "activation_gate_only_no_scores",
            }
        )
    return out


def global_blockers() -> list[dict[str, object]]:
    formula_rows = read_csv(SOURCE / "family_formula_table_v05.csv")
    count_rows = read_csv(SOURCE / "numeric_count_readiness_v05.csv")
    runners = read_csv(SOURCE / "control_runner_contract_v04.csv")
    thresholds = read_csv(SOURCE / "decision_threshold_v01.csv")
    prediction_contract_path = DERIVED / "family_prediction_table_contract_summary_v80.csv"
    prediction_contract = read_csv(prediction_contract_path)[0] if prediction_contract_path.exists() else {}
    numeric_count_path = DERIVED / "numeric_parameter_count_table_summary_v08.csv"
    numeric_count_summary = read_csv(numeric_count_path)[0] if numeric_count_path.exists() else {}
    final_count_path = DERIVED / "numeric_parameter_count_table_final_values_summary_v10.csv"
    final_count_summary = read_csv(final_count_path)[0] if final_count_path.exists() else {}
    control_output_path = DERIVED / "control_runner_outputs_summary_v08.csv"
    control_output_summary = read_csv(control_output_path)[0] if control_output_path.exists() else {}
    threshold_path = DERIVED / "numeric_decision_thresholds_summary_v08.csv"
    threshold_summary = read_csv(threshold_path)[0] if threshold_path.exists() else {}
    count_closure_path = DERIVED / "numeric_count_readiness_closure_summary_v09.csv"
    count_closure_summary = read_csv(count_closure_path)[0] if count_closure_path.exists() else {}
    final_counts_ready = final_count_summary.get("overall_status") == (
        "NUMERIC_PARAMETER_COUNT_TABLE_FINAL_VALUES_V10_READY_FOR_GLOBAL_SCORING_PREREQUISITES"
    )
    control_outputs_ready = control_output_summary.get("overall_status") == (
        "CONTROL_RUNNER_OUTPUTS_V08_READY_FOR_DECISION_THRESHOLDS"
    )
    thresholds_ready = threshold_summary.get("overall_status") == "NUMERIC_DECISION_THRESHOLDS_V08_READY_FOR_SCORING_PREFLIGHT"
    count_next = count_closure_summary.get(
        "next_required_artifact",
        numeric_count_summary.get("next_required_artifact", "numeric_parameter_count_table_v08.csv"),
    )
    formula_ready = prediction_contract.get("overall_status") == (
        "FAMILY_PREDICTION_TABLE_CONTRACT_READY_PARAMETER_COUNTS_BLOCKED"
    ) or all(row["formula_table_status"] == "FORMULA_TABLE_READY" for row in formula_rows)
    formula_required_artifact = (
        prediction_contract.get("next_required_artifact")
        if prediction_contract.get("overall_status") == "FAMILY_PREDICTION_TABLE_CONTRACT_READY_FORMULA_SLOTS_BLOCKED"
        else "family_prediction_tables_v08.csv"
    )
    formula_blocking_detail = (
        "family prediction contract is ready, but formula slot tables are not filled"
        if prediction_contract.get("overall_status") == "FAMILY_PREDICTION_TABLE_CONTRACT_READY_FORMULA_SLOTS_BLOCKED"
        else "family formula tables are not filled"
    )
    return [
        {
            "blocker_id": "SAG13_FAMILY_FORMULA_TABLES",
            "required_artifact": formula_required_artifact,
            "current_status": "BLOCKED" if not formula_ready else "READY",
            "blocking_detail": formula_blocking_detail,
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "global_activation_blocker_only_no_formula_claim",
        },
        {
            "blocker_id": "SAG13_PARAMETER_COUNTS",
            "required_artifact": "numeric_parameter_count_table_final_values_v10.csv"
            if final_counts_ready
            else count_next
            if any(row["count_readiness_status"] != "COUNT_READY" for row in count_rows)
            else "numeric_parameter_count_table_v08.csv",
            "current_status": "READY"
            if final_counts_ready
            else "BLOCKED"
            if any(row["count_readiness_status"] != "COUNT_READY" for row in count_rows)
            else "READY",
            "blocking_detail": "none"
            if final_counts_ready
            else "numeric parameter counts remain blocked by count-readiness closure"
            if numeric_count_summary.get("overall_status") == "NUMERIC_PARAMETER_COUNT_TABLE_V08_BLOCKED_BY_COUNT_READINESS"
            else "numeric parameter counts are not ready",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "global_activation_blocker_only_no_parsimony_claim",
        },
        {
            "blocker_id": "SAG13_CONTROL_RUNNERS",
            "required_artifact": "control_runner_outputs_v08.csv",
            "current_status": "READY" if control_outputs_ready else "BLOCKED",
            "blocking_detail": "none" if control_outputs_ready else "control runner output contracts are not materialized",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "global_activation_blocker_only_no_control_result",
        },
        {
            "blocker_id": "SAG13_DECISION_THRESHOLDS",
            "required_artifact": "numeric_decision_thresholds_v08.csv",
            "current_status": "READY"
            if thresholds_ready
            else "BLOCKED"
            if any("PENDING" in row["current_status"] for row in thresholds)
            else "READY",
            "blocking_detail": "none" if thresholds_ready else "numeric decision thresholds are pending",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "global_activation_blocker_only_no_verdict",
        },
    ]


def summary(rows: list[dict[str, object]], blockers: list[dict[str, object]]) -> list[dict[str, object]]:
    activated = sum(1 for row in rows if row["activation_decision"] == "ACTIVATE_FOR_SCORING")
    blocked_global = sum(1 for row in blockers if row["current_status"] == "BLOCKED")
    value_ready = all(row["real_value_gate_status"] == "REAL_VALUES_PRESENT_VALIDATION_PENDING_LEAKAGE" for row in rows)
    leakage_ready = all(row["leakage_audit_status"] == "LEAKAGE_AUDIT_PASS" for row in rows)
    first_blocker_artifact = next(
        (row["required_artifact"] for row in blockers if row["current_status"] == "BLOCKED"),
        "none",
    )
    return [
        {
            "summary_id": "SCORING_ACTIVATION_GATE_V13",
            "candidate_rows": len(rows),
            "rows_activated_for_scoring": activated,
            "row_level_blocked_rows": len(rows) - activated,
            "global_blockers": blocked_global,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_ROW_ACTIVATION_READY_GLOBAL_SCORING_BLOCKED"
            if activated == len(rows) and blocked_global
            else "SCORING_ACTIVATION_READY_GLOBAL_PREREQUISITES_READY"
            if activated == len(rows)
            else "SCORING_ACTIVATION_BLOCKED",
            "next_required_artifact": first_blocker_artifact
            if activated == len(rows) and blocked_global
            else "scoring_preflight_v07.csv"
            if activated == len(rows)
            else "activated_scoring_rows_v10_or_activation_policy_after_leakage_pass"
            if leakage_ready
            else "data/derived/source_import_leakage_summary_v09.csv"
            if value_ready
            else "data/input/source_import_real_values_v12.csv",
            "claim_boundary": "activation_gate_only_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = row_gates()
    blockers = global_blockers()
    summary_rows = summary(rows, blockers)
    write_csv(
        DERIVED / "scoring_activation_gate_v13.csv",
        rows,
        [
            "activation_gate_id",
            "galaxy_id",
            "proposed_split",
            "real_value_gate_status",
            "leakage_audit_status",
            "row_activation_status",
            "blocking_requirements",
            "activation_decision",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_activation_global_blockers_v13.csv",
        blockers,
        [
            "blocker_id",
            "required_artifact",
            "current_status",
            "blocking_detail",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_activation_summary_v13.csv",
        summary_rows,
        [
            "summary_id",
            "candidate_rows",
            "rows_activated_for_scoring",
            "row_level_blocked_rows",
            "global_blockers",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SCORING_ACTIVATION_GATE_V13_BUILT")


if __name__ == "__main__":
    main()
