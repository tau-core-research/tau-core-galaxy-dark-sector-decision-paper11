#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
RAW_INPUT = ROOT / "data/input/source_import_raw_sparc_like_v15.csv"
TARGET_INPUT = ROOT / "data/input/source_import_real_values_v12.csv"

RAW_COLUMNS = [
    "galaxy_id",
    "radial_index",
    "radius_kpc",
    "v_obs_km_s",
    "sigma_v_km_s",
    "v_gas_km_s",
    "v_disk_km_s",
    "v_bulge_km_s",
    "catalog",
    "table_or_file",
    "version_or_date",
    "row_id",
    "sha256_or_external_accession",
    "source_route",
    "leakage_evidence_id",
]

TARGET_COLUMNS = RAW_COLUMNS + ["import_status"]


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


def target_rows_from_raw() -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in read_csv(RAW_INPUT):
        out.append({column: row.get(column, "") for column in RAW_COLUMNS} | {"import_status": "IMPORTED_SOURCE_VALUE"})
    return out


def writer_result() -> list[dict[str, object]]:
    authorization = read_csv(DERIVED / "source_import_write_authorization_v16.csv")[0]
    authorized = authorization["write_authorized"] == "true"
    raw_present = RAW_INPUT.exists()
    target_preexisting = TARGET_INPUT.exists()
    rows_written = 0
    writer_status = "WRITER_BLOCKED_BY_AUTHORIZATION"
    if authorized and raw_present and not target_preexisting:
        rows = target_rows_from_raw()
        write_csv(TARGET_INPUT, rows, TARGET_COLUMNS)
        rows_written = len(rows)
        writer_status = "TARGET_INPUT_WRITTEN_FROM_AUTHORIZED_RAW"
    return [
        {
            "writer_id": "SIAW17_AUTHORIZED_RAW_TO_V12",
            "authorization_source": "source_import_write_authorization_v16.csv",
            "raw_input_file": "data/input/source_import_raw_sparc_like_v15.csv",
            "target_input_file": "data/input/source_import_real_values_v12.csv",
            "write_authorized": authorization["write_authorized"],
            "raw_input_present": str(raw_present).lower(),
            "target_preexisting": str(target_preexisting).lower(),
            "target_file_written": str(rows_written > 0).lower(),
            "rows_written": rows_written,
            "writer_status": writer_status,
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "authorized_writer_only_no_scores_no_verdict",
        }
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row = rows[0]
    next_required = (
        "PAPER11_ALLOW_REAL_SOURCE_IMPORT_WRITE=1"
        if row["raw_input_present"] == "true" and row["write_authorized"] == "false"
        else "data/input/source_import_raw_sparc_like_v15.csv"
    )
    return [
        {
            "summary_id": "SOURCE_IMPORT_AUTHORIZED_WRITER_V17",
            "writer_status": row["writer_status"],
            "target_file_written": row["target_file_written"],
            "rows_written": row["rows_written"],
            "target_input_file_present_after_writer": str(TARGET_INPUT.exists()).lower(),
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "AUTHORIZED_WRITER_BLOCKED",
            "next_required_artifact": next_required,
            "claim_boundary": "authorized_writer_only_no_source_import_no_scores",
        }
    ]


def main() -> None:
    rows = writer_result()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "source_import_authorized_writer_v17.csv",
        rows,
        [
            "writer_id",
            "authorization_source",
            "raw_input_file",
            "target_input_file",
            "write_authorized",
            "raw_input_present",
            "target_preexisting",
            "target_file_written",
            "rows_written",
            "writer_status",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_authorized_writer_summary_v17.csv",
        summary_rows,
        [
            "summary_id",
            "writer_status",
            "target_file_written",
            "rows_written",
            "target_input_file_present_after_writer",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_AUTHORIZED_WRITER_V17_BUILT")


if __name__ == "__main__":
    main()
