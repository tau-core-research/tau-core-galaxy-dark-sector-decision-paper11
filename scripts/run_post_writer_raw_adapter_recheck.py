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
    raw_recheck = read_csv(DERIVED / "post_writer_raw_import_recheck_summary_v34.csv")[0]
    adapter = read_csv(DERIVED / "source_import_raw_adapter_gate_v15.csv")[0]
    blockers = []
    if raw_recheck["raw_import_allowed_rows_after_recheck"] == "0":
        blockers.append("post_writer_raw_import_not_allowed")
    if raw_recheck["raw_rows_imported_after_recheck"] == "0":
        blockers.append("zero_raw_rows_imported_after_recheck")
    if adapter["raw_input_status"] != "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW":
        blockers.append("raw_adapter_input_not_present")
    return [
        {
            "recheck_id": "PWRAR35_POST_WRITER_RAW_ADAPTER_RECHECK",
            "raw_import_recheck_source": "data/derived/post_writer_raw_import_recheck_summary_v34.csv",
            "raw_adapter_source": "data/derived/source_import_raw_adapter_gate_v15.csv",
            "raw_input_status": adapter["raw_input_status"],
            "raw_rows_seen": adapter["raw_rows_seen"],
            "valid_raw_rows": adapter["valid_raw_rows"],
            "raw_rows_imported_after_recheck": raw_recheck["raw_rows_imported_after_recheck"],
            "adapter_recheck_blockers": ";".join(blockers),
            "target_file_written_after_recheck": "false",
            "real_values_input_may_exist_after_recheck": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "post_writer_raw_adapter_recheck_only_no_v12_write_no_scores",
        }
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row = rows[0]
    return [
        {
            "summary_id": "POST_WRITER_RAW_ADAPTER_RECHECK_V35",
            "raw_input_status": row["raw_input_status"],
            "valid_raw_rows": row["valid_raw_rows"],
            "target_file_written_after_recheck": row["target_file_written_after_recheck"],
            "real_values_input_may_exist_after_recheck": row["real_values_input_may_exist_after_recheck"],
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_RAW_ADAPTER_RECHECK_BLOCKED"
            if row["target_file_written_after_recheck"] == "false"
            else "POST_WRITER_RAW_ADAPTER_RECHECK_READY",
            "claim_boundary": "post_writer_raw_adapter_recheck_only_no_v12_write_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "post_writer_raw_adapter_recheck_v35.csv",
        rows,
        [
            "recheck_id",
            "raw_import_recheck_source",
            "raw_adapter_source",
            "raw_input_status",
            "raw_rows_seen",
            "valid_raw_rows",
            "raw_rows_imported_after_recheck",
            "adapter_recheck_blockers",
            "target_file_written_after_recheck",
            "real_values_input_may_exist_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_writer_raw_adapter_recheck_summary_v35.csv",
        summary_rows,
        [
            "summary_id",
            "raw_input_status",
            "valid_raw_rows",
            "target_file_written_after_recheck",
            "real_values_input_may_exist_after_recheck",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_WRITER_RAW_ADAPTER_RECHECK_V35_BUILT")


if __name__ == "__main__":
    main()
