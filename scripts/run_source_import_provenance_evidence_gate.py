#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
INPUT = ROOT / "data/input/source_import_provenance_evidence_v21.csv"

REQUIRED_COLUMNS = [
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


def evidence_statuses(expected_galaxies: set[str]) -> tuple[str, int, int, int]:
    if not INPUT.exists():
        return "EVIDENCE_INPUT_FILE_MISSING", 0, 0, 0
    rows = read_csv(INPUT)
    header = set(rows[0].keys()) if rows else set()
    if not set(REQUIRED_COLUMNS).issubset(header):
        return "EVIDENCE_INPUT_HEADER_INVALID", len(rows), 0, 0
    valid_rows = 0
    valid_galaxies: set[str] = set()
    for row in rows:
        galaxy_id = row.get("galaxy_id", "")
        required_present = all(row.get(column, "") != "" for column in REQUIRED_COLUMNS)
        status_ok = row.get("provenance_evidence_status") == "PROVENANCE_EVIDENCE_COMPLETE"
        if galaxy_id in expected_galaxies and required_present and status_ok:
            valid_rows += 1
            valid_galaxies.add(galaxy_id)
    if valid_rows:
        return "EVIDENCE_INPUT_PRESENT_VALIDATION_PENDING_REVIEW", len(rows), valid_rows, len(valid_galaxies)
    return "EVIDENCE_INPUT_PRESENT_NO_VALID_ROWS", len(rows), 0, 0


def gate_rows() -> list[dict[str, object]]:
    manifest = read_csv(DERIVED / "source_import_provenance_manifest_v19.csv")
    expected_galaxies = {row["galaxy_id"] for row in manifest}
    input_status, rows_seen, valid_rows, valid_galaxies = evidence_statuses(expected_galaxies)
    all_valid = valid_rows == len(expected_galaxies) and valid_galaxies == len(expected_galaxies)
    return [
        {
            "evidence_gate_id": "SIPEG22_EVIDENCE_TO_PROVENANCE",
            "evidence_input_file": "data/input/source_import_provenance_evidence_v21.csv",
            "provenance_manifest": "data/derived/source_import_provenance_manifest_v19.csv",
            "evidence_input_status": input_status,
            "evidence_rows_seen": rows_seen,
            "valid_evidence_rows": valid_rows,
            "galaxies_with_valid_evidence": valid_galaxies,
            "provenance_promotion_allowed": str(all_valid).lower(),
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "provenance_evidence_gate_only_no_promotion_no_scores",
        }
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row = rows[0]
    promotion_allowed = row["provenance_promotion_allowed"] == "true"
    return [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_EVIDENCE_GATE_V22",
            "evidence_input_status": row["evidence_input_status"],
            "evidence_rows_seen": row["evidence_rows_seen"],
            "valid_evidence_rows": row["valid_evidence_rows"],
            "galaxies_with_valid_evidence": row["galaxies_with_valid_evidence"],
            "provenance_promotion_allowed": row["provenance_promotion_allowed"],
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PROVENANCE_EVIDENCE_READY_FOR_PROMOTION"
            if promotion_allowed
            else "PROVENANCE_EVIDENCE_INPUT_MISSING",
            "next_required_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "claim_boundary": "provenance_evidence_gate_only_no_source_import_no_scores",
        }
    ]


def main() -> None:
    rows = gate_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "source_import_provenance_evidence_gate_v22.csv",
        rows,
        [
            "evidence_gate_id",
            "evidence_input_file",
            "provenance_manifest",
            "evidence_input_status",
            "evidence_rows_seen",
            "valid_evidence_rows",
            "galaxies_with_valid_evidence",
            "provenance_promotion_allowed",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_provenance_evidence_gate_summary_v22.csv",
        summary_rows,
        [
            "summary_id",
            "evidence_input_status",
            "evidence_rows_seen",
            "valid_evidence_rows",
            "galaxies_with_valid_evidence",
            "provenance_promotion_allowed",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_PROVENANCE_EVIDENCE_GATE_V22_BUILT")


if __name__ == "__main__":
    main()
