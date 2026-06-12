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


def activation_rows() -> list[dict[str, object]]:
    scaffold = read_csv(DERIVED / "activated_scoring_rows_v08.csv")
    value_gates = {row["galaxy_id"]: row for row in read_csv(DERIVED / "source_import_real_values_gate_v12.csv")}
    leakage = {row["galaxy_id"]: row for row in read_csv(DERIVED / "source_import_and_leakage_audit_v09.csv")}
    pass_coverage = {row["galaxy_id"]: row for row in read_csv(DERIVED / "leakage_audit_pass_review_coverage_v78.csv")}
    out: list[dict[str, object]] = []
    for row in scaffold:
        galaxy_id = row["galaxy_id"]
        value_row = value_gates[galaxy_id]
        leakage_row = leakage[galaxy_id]
        pass_row = pass_coverage[galaxy_id]
        blockers = []
        if value_row["real_value_gate_status"] != "REAL_VALUES_PRESENT_VALIDATION_PENDING_LEAKAGE":
            blockers.append("real_values_not_ready")
        if leakage_row["leakage_audit_status"] != "LEAKAGE_AUDIT_PASS":
            blockers.append("source_import_leakage_not_passed")
        if pass_row["galaxy_leakage_pass_authorized"] != "true":
            blockers.append("v78_leakage_pass_not_authorized")
        activated = not blockers
        out.append(
            {
                "scoring_row_id": row["scoring_row_id"].replace("ASR08", "ASR10"),
                "source_scaffold_row_id": row["scoring_row_id"],
                "galaxy_id": galaxy_id,
                "decision_role": row["decision_role"],
                "proposed_split": row["proposed_split"],
                "value_gate_status": value_row["real_value_gate_status"],
                "leakage_audit_status": leakage_row["leakage_audit_status"],
                "v78_leakage_pass_authorized": pass_row["galaxy_leakage_pass_authorized"],
                "activation_policy_blockers": ";".join(blockers),
                "activation_status": "ACTIVATED" if activated else "NOT_ACTIVATED",
                "endpoint_scoring_allowed": "false",
                "required_after_activation": "family_prediction_tables;parameter_counts;control_runner_outputs;decision_thresholds",
                "claim_boundary": "row_activation_policy_only_no_endpoint_score",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    activated = sum(row["activation_status"] == "ACTIVATED" for row in rows)
    return [
        {
            "summary_id": "SCORING_ROW_ACTIVATION_POLICY_V79",
            "candidate_rows": len(rows),
            "activated_rows_written": activated,
            "blocked_rows": len(rows) - activated,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SCORING_ROW_ACTIVATION_POLICY_READY_GLOBAL_SCORING_BLOCKED"
            if activated == len(rows)
            else "SCORING_ROW_ACTIVATION_POLICY_BLOCKED",
            "next_required_artifact": "family_prediction_tables_v08.csv",
            "claim_boundary": "row_activation_policy_only_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = activation_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "activated_scoring_rows_v10.csv",
        rows,
        [
            "scoring_row_id",
            "source_scaffold_row_id",
            "galaxy_id",
            "decision_role",
            "proposed_split",
            "value_gate_status",
            "leakage_audit_status",
            "v78_leakage_pass_authorized",
            "activation_policy_blockers",
            "activation_status",
            "endpoint_scoring_allowed",
            "required_after_activation",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_row_activation_policy_summary_v79.csv",
        summary_rows,
        [
            "summary_id",
            "candidate_rows",
            "activated_rows_written",
            "blocked_rows",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SCORING_ROW_ACTIVATION_POLICY_V79_BUILT")


if __name__ == "__main__":
    main()
