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


def recheck_rows() -> list[dict[str, object]]:
    values_by_galaxy = {
        row["galaxy_id"]: row for row in read_csv(DERIVED / "post_writer_real_values_gate_recheck_v36.csv")
    }
    leakage_rows = read_csv(DERIVED / "leakage_audit_findings_v09.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(leakage_rows, start=1):
        value_row = values_by_galaxy[row["galaxy_id"]]
        blockers = []
        if value_row["rows_passing_value_gate_after_recheck"] == "0":
            blockers.append("post_writer_real_values_gate_not_passed")
        if row["leakage_status"] != "LEAKAGE_AUDIT_PASS":
            blockers.append("v09_leakage_audit_not_passed")
        out.append(
            {
                "recheck_id": f"PWLAR37_{index:03d}",
                "source_finding_id": row["finding_id"],
                "galaxy_id": row["galaxy_id"],
                "real_values_recheck_source": "data/derived/post_writer_real_values_gate_recheck_v36.csv",
                "v09_leakage_status": row["leakage_status"],
                "rows_passing_value_gate_after_recheck": value_row["rows_passing_value_gate_after_recheck"],
                "leakage_recheck_blockers": ";".join(blockers),
                "leakage_pass_after_recheck": "false",
                "activation_allowed_after_recheck": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "post_writer_leakage_audit_recheck_only_no_activation_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    leakage_pass = sum(row["leakage_pass_after_recheck"] == "true" for row in rows)
    activation_allowed = sum(row["activation_allowed_after_recheck"] == "true" for row in rows)
    return [
        {
            "summary_id": "POST_WRITER_LEAKAGE_AUDIT_RECHECK_V37",
            "leakage_recheck_rows": len(rows),
            "leakage_pass_rows_after_recheck": leakage_pass,
            "leakage_blocked_rows_after_recheck": len(rows) - leakage_pass,
            "activation_allowed_rows_after_recheck": activation_allowed,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_LEAKAGE_AUDIT_RECHECK_BLOCKED"
            if leakage_pass == 0
            else "POST_WRITER_LEAKAGE_AUDIT_RECHECK_READY",
            "claim_boundary": "post_writer_leakage_audit_recheck_only_no_activation_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "post_writer_leakage_audit_recheck_v37.csv",
        rows,
        [
            "recheck_id",
            "source_finding_id",
            "galaxy_id",
            "real_values_recheck_source",
            "v09_leakage_status",
            "rows_passing_value_gate_after_recheck",
            "leakage_recheck_blockers",
            "leakage_pass_after_recheck",
            "activation_allowed_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_writer_leakage_audit_recheck_summary_v37.csv",
        summary_rows,
        [
            "summary_id",
            "leakage_recheck_rows",
            "leakage_pass_rows_after_recheck",
            "leakage_blocked_rows_after_recheck",
            "activation_allowed_rows_after_recheck",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_WRITER_LEAKAGE_AUDIT_RECHECK_V37_BUILT")


if __name__ == "__main__":
    main()
