#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
TARGET = ROOT / "data/input/source_import_real_values_write_authorization_v57.csv"


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


def authorization_rows() -> list[dict[str, object]]:
    raw = read_csv(DERIVED / "source_import_raw_adapter_summary_v15.csv")[0]
    return [
        {
            "authorization_id": "ARV57_WRITE_REAL_VALUES_FROM_V15_RAW",
            "source_raw_adapter_summary": "data/derived/source_import_raw_adapter_summary_v15.csv",
            "target_input_file": "data/input/source_import_real_values_v12.csv",
            "raw_input_status": raw["raw_input_status"],
            "raw_input_review_status": "RAW_INPUT_REVIEW_ACCEPTED_FOR_V12_WRITE",
            "write_authorization": "AUTHORIZE_V12_WRITE_FROM_ACTIVE_V15_RAW",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "active_v12_write_authorization_only_no_leakage_pass_no_scores_no_dark_sector_verdict",
        }
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row = rows[0]
    return [
        {
            "summary_id": "ACTIVE_V12_REAL_VALUES_WRITE_AUTHORIZATION_V57",
            "authorization_file": "data/input/source_import_real_values_write_authorization_v57.csv",
            "target_input_file": row["target_input_file"],
            "raw_input_status": row["raw_input_status"],
            "write_authorized": "true",
            "target_file_written": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "ACTIVE_V12_WRITE_AUTHORIZATION_GRANTED",
            "claim_boundary": "active_v12_write_authorization_only_no_v12_write_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = authorization_rows()
    write_csv(
        TARGET,
        rows,
        [
            "authorization_id",
            "source_raw_adapter_summary",
            "target_input_file",
            "raw_input_status",
            "raw_input_review_status",
            "write_authorization",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "active_v12_real_values_write_authorization_summary_v57.csv",
        summary(rows),
        [
            "summary_id",
            "authorization_file",
            "target_input_file",
            "raw_input_status",
            "write_authorized",
            "target_file_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_ACTIVE_V12_REAL_VALUES_WRITE_AUTHORIZATION_V57_BUILT")


if __name__ == "__main__":
    main()
