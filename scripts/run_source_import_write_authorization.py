#!/usr/bin/env python3
from __future__ import annotations

import csv
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
TARGET_INPUT = ROOT / "data/input/source_import_real_values_v12.csv"
AUTH_INPUT = ROOT / "data/input/source_import_real_values_write_authorization_v57.csv"


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


def authorization_row() -> list[dict[str, object]]:
    adapter = read_csv(DERIVED / "source_import_raw_adapter_gate_v15.csv")[0]
    auth_rows = read_csv(AUTH_INPUT) if AUTH_INPUT.exists() else []
    file_authorized = any(
        row.get("write_authorization") == "AUTHORIZE_V12_WRITE_FROM_ACTIVE_V15_RAW" for row in auth_rows
    )
    explicit_write = os.environ.get("PAPER11_ALLOW_REAL_SOURCE_IMPORT_WRITE") == "1" or file_authorized
    raw_valid = adapter["raw_input_status"] == "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW"
    authorized = explicit_write and raw_valid
    blockers = []
    if not explicit_write:
        blockers.append("explicit_write_authorization_missing")
    if not raw_valid:
        blockers.append("raw_input_not_validated")
    return [
        {
            "authorization_id": "SIWA16_WRITE_V12",
            "source_adapter_gate": "source_import_raw_adapter_gate_v15.csv",
            "target_input_file": "data/input/source_import_real_values_v12.csv",
            "authorization_file": "data/input/source_import_real_values_write_authorization_v57.csv",
            "explicit_write_authorization": str(explicit_write).lower(),
            "raw_input_status": adapter["raw_input_status"],
            "target_input_file_present": str(TARGET_INPUT.exists()).lower(),
            "write_authorized": str(authorized).lower(),
            "write_blockers": ";".join(blockers) if blockers else "none",
            "target_file_written": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "write_authorization_only_no_source_import_no_scores",
        }
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row = rows[0]
    next_required = (
        "data/input/source_import_real_values_v12.csv"
        if row["write_authorized"] == "true"
        else "data/input/source_import_real_values_write_authorization_v57.csv"
        if row["raw_input_status"] == "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW"
        else "data/input/source_import_raw_sparc_like_v15.csv"
    )
    overall_status = "WRITE_AUTHORIZATION_READY" if row["write_authorized"] == "true" else "WRITE_AUTHORIZATION_BLOCKED"
    return [
        {
            "summary_id": "SOURCE_IMPORT_WRITE_AUTHORIZATION_V16",
            "write_authorized": row["write_authorized"],
            "target_file_written": row["target_file_written"],
            "target_input_file_present": row["target_input_file_present"],
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": overall_status,
            "next_required_artifact": next_required,
            "claim_boundary": "write_authorization_only_no_source_import_no_scores",
        }
    ]


def main() -> None:
    rows = authorization_row()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "source_import_write_authorization_v16.csv",
        rows,
        [
            "authorization_id",
            "source_adapter_gate",
            "target_input_file",
            "authorization_file",
            "explicit_write_authorization",
            "raw_input_status",
            "target_input_file_present",
            "write_authorized",
            "write_blockers",
            "target_file_written",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_write_authorization_summary_v16.csv",
        summary_rows,
        [
            "summary_id",
            "write_authorized",
            "target_file_written",
            "target_input_file_present",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_WRITE_AUTHORIZATION_V16_BUILT")


if __name__ == "__main__":
    main()
