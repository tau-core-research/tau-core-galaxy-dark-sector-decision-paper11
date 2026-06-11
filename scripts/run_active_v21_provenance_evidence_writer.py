#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
TARGET = ROOT / "data/input/source_import_provenance_evidence_v21.csv"

TARGET_COLUMNS = [
    "galaxy_id",
    "catalog",
    "table_or_file",
    "version_or_date",
    "row_id",
    "sha256_or_external_accession",
    "source_route",
    "leakage_evidence_id",
    "provenance_evidence_status",
]


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


def target_rows() -> list[dict[str, object]]:
    payload = read_csv(DERIVED / "authorized_provenance_evidence_payload_v54.csv")
    out: list[dict[str, object]] = []
    for row in payload:
        if row["payload_write_status"] != "READY_FOR_SEPARATE_ACTIVE_V21_WRITE_GATE":
            continue
        out.append({column: row[column] for column in TARGET_COLUMNS})
    return out


def writer_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "ACTIVE_V21_PROVENANCE_EVIDENCE_WRITER_V55",
            "source_payload": "data/derived/authorized_provenance_evidence_payload_v54.csv",
            "target_evidence_input": "data/input/source_import_provenance_evidence_v21.csv",
            "rows_written": len(rows),
            "complete_provenance_rows_written": sum(
                row["provenance_evidence_status"] == "PROVENANCE_EVIDENCE_COMPLETE" for row in rows
            ),
            "target_file_written": str(TARGET.exists()).lower(),
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "ACTIVE_V21_PROVENANCE_EVIDENCE_WRITTEN"
            if len(rows) == 18
            else "ACTIVE_V21_PROVENANCE_EVIDENCE_WRITE_BLOCKED",
            "claim_boundary": "active_v21_provenance_evidence_writer_only_no_observed_values_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = target_rows()
    write_csv(TARGET, rows, TARGET_COLUMNS)
    summary_rows = writer_summary(rows)
    write_csv(
        DERIVED / "active_v21_provenance_evidence_writer_summary_v55.csv",
        summary_rows,
        [
            "summary_id",
            "source_payload",
            "target_evidence_input",
            "rows_written",
            "complete_provenance_rows_written",
            "target_file_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_ACTIVE_V21_PROVENANCE_EVIDENCE_WRITER_V55_BUILT")


if __name__ == "__main__":
    main()
