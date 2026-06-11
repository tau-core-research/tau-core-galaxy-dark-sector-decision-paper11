#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
TARGET = ROOT / "data/input/source_import_provenance_evidence_v21.csv"


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


def writer_rows() -> list[dict[str, object]]:
    authorization = read_csv(DERIVED / "frontier_evidence_write_authorization_v29.csv")[0]
    authorized = authorization["write_authorized"] == "true"
    target_preexisting = TARGET.exists()
    rows_written = 0
    writer_status = "WRITER_BLOCKED_BY_FRONTIER_AUTHORIZATION"
    if authorized and not target_preexisting:
        writer_status = "WRITER_AUTHORIZED_BUT_NO_SOURCE_PAYLOAD"
    return [
        {
            "writer_id": "FAEW30_AUTHORIZED_FRONTIER_EVIDENCE_WRITER",
            "authorization_source": "data/derived/frontier_evidence_write_authorization_v29.csv",
            "target_evidence_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "write_authorized": authorization["write_authorized"],
            "target_preexisting": str(target_preexisting).lower(),
            "target_file_written": "false",
            "rows_written": rows_written,
            "writer_status": writer_status,
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "frontier_authorized_evidence_writer_only_no_evidence_no_scores",
        }
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row = rows[0]
    return [
        {
            "summary_id": "FRONTIER_AUTHORIZED_EVIDENCE_WRITER_V30",
            "writer_status": row["writer_status"],
            "write_authorized": row["write_authorized"],
            "target_file_written": row["target_file_written"],
            "rows_written": row["rows_written"],
            "target_input_file_present_after_writer": str(TARGET.exists()).lower(),
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_AUTHORIZED_EVIDENCE_WRITER_BLOCKED",
            "claim_boundary": "frontier_authorized_evidence_writer_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = writer_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "frontier_authorized_evidence_writer_v30.csv",
        rows,
        [
            "writer_id",
            "authorization_source",
            "target_evidence_artifact",
            "write_authorized",
            "target_preexisting",
            "target_file_written",
            "rows_written",
            "writer_status",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_authorized_evidence_writer_summary_v30.csv",
        summary_rows,
        [
            "summary_id",
            "writer_status",
            "write_authorized",
            "target_file_written",
            "rows_written",
            "target_input_file_present_after_writer",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_FRONTIER_AUTHORIZED_EVIDENCE_WRITER_V30_BUILT")


if __name__ == "__main__":
    main()
