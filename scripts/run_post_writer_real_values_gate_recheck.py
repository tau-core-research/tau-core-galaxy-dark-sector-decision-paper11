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
    adapter = read_csv(DERIVED / "post_writer_raw_adapter_recheck_summary_v35.csv")[0]
    value_rows = read_csv(DERIVED / "source_import_real_values_gate_v12.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(value_rows, start=1):
        blockers = []
        if adapter["real_values_input_may_exist_after_recheck"] == "false":
            blockers.append("post_writer_raw_adapter_did_not_write_v12")
        if row["input_file_status"] == "REAL_VALUE_FILE_MISSING":
            blockers.append("real_value_file_missing")
        value_gate_passed = row["activation_decision"] == "VALUE_GATE_PASSED_PENDING_LEAKAGE"
        if row["activation_decision"] == "DO_NOT_ACTIVATE":
            blockers.append("v12_activation_decision_not_activate")
        out.append(
            {
                "recheck_id": f"PWRVG36_{index:03d}",
                "source_gate_id": row["gate_id"],
                "galaxy_id": row["galaxy_id"],
                "raw_adapter_recheck_source": "data/derived/post_writer_raw_adapter_recheck_summary_v35.csv",
                "v12_input_file_status": row["input_file_status"],
                "v12_imported_numeric_rows": row["imported_numeric_rows"],
                "v12_real_value_gate_status": row["real_value_gate_status"],
                "real_value_recheck_blockers": ";".join(blockers),
                "rows_passing_value_gate_after_recheck": 1 if value_gate_passed and not blockers else 0,
                "activation_decision_after_recheck": "VALUE_GATE_PASSED_PENDING_LEAKAGE"
                if value_gate_passed and not blockers
                else "DO_NOT_ACTIVATE",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "post_writer_real_values_gate_recheck_only_no_activation_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    imported = sum(int(row["v12_imported_numeric_rows"]) for row in rows)
    passing = sum(int(row["rows_passing_value_gate_after_recheck"]) for row in rows)
    return [
        {
            "summary_id": "POST_WRITER_REAL_VALUES_GATE_RECHECK_V36",
            "real_value_recheck_rows": len(rows),
            "imported_numeric_rows_after_recheck": imported,
            "rows_passing_value_gate_after_recheck": passing,
            "rows_activated_after_recheck": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_REAL_VALUES_GATE_RECHECK_BLOCKED"
            if passing == 0
            else "POST_WRITER_REAL_VALUES_GATE_RECHECK_READY",
            "claim_boundary": "post_writer_real_values_gate_recheck_only_no_activation_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "post_writer_real_values_gate_recheck_v36.csv",
        rows,
        [
            "recheck_id",
            "source_gate_id",
            "galaxy_id",
            "raw_adapter_recheck_source",
            "v12_input_file_status",
            "v12_imported_numeric_rows",
            "v12_real_value_gate_status",
            "real_value_recheck_blockers",
            "rows_passing_value_gate_after_recheck",
            "activation_decision_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_writer_real_values_gate_recheck_summary_v36.csv",
        summary_rows,
        [
            "summary_id",
            "real_value_recheck_rows",
            "imported_numeric_rows_after_recheck",
            "rows_passing_value_gate_after_recheck",
            "rows_activated_after_recheck",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_WRITER_REAL_VALUES_GATE_RECHECK_V36_BUILT")


if __name__ == "__main__":
    main()
