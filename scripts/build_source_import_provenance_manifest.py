#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"

PROVENANCE_FIELDS = [
    "catalog",
    "table_or_file",
    "version_or_date",
    "row_id",
    "sha256_or_external_accession",
    "source_route",
    "leakage_evidence_id",
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


def provenance_rows() -> list[dict[str, object]]:
    scoring_rows = read_csv(DERIVED / "activated_scoring_rows_v08.csv")
    return [
        {
            "provenance_id": row["scoring_row_id"].replace("ASR08", "SIP19"),
            "galaxy_id": row["galaxy_id"],
            "proposed_split": row["proposed_split"],
            "required_provenance_fields": ";".join(PROVENANCE_FIELDS),
            "catalog_status": "PROVENANCE_REQUIRED_NOT_FILLED",
            "file_or_table_status": "PROVENANCE_REQUIRED_NOT_FILLED",
            "row_identity_status": "PROVENANCE_REQUIRED_NOT_FILLED",
            "hash_or_accession_status": "PROVENANCE_REQUIRED_NOT_FILLED",
            "leakage_evidence_status": "PROVENANCE_REQUIRED_NOT_FILLED",
            "raw_import_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "provenance_manifest_only_no_source_values_no_scores",
        }
        for row in scoring_rows
    ]


def column_rows() -> list[dict[str, object]]:
    return [
        {
            "field_name": field,
            "required_before_raw_import": "true",
            "validation_rule": validation_rule(field),
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "provenance_column_only_no_source_claim",
        }
        for field in PROVENANCE_FIELDS
    ]


def validation_rule(field: str) -> str:
    rules = {
        "catalog": "nonempty_source_catalog_identifier",
        "table_or_file": "nonempty_table_or_file_reference",
        "version_or_date": "nonempty_source_version_or_date",
        "row_id": "stable_row_identifier_or_radial_row_key",
        "sha256_or_external_accession": "sha256_hash_or_external_accession_required",
        "source_route": "reproducible_local_or_external_route",
        "leakage_evidence_id": "pre_score_leakage_evidence_reference",
    }
    return rules[field]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_V19",
            "candidate_rows": len(rows),
            "provenance_complete_rows": 0,
            "raw_import_allowed_rows": 0,
            "required_provenance_fields": len(PROVENANCE_FIELDS),
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PROVENANCE_REQUIRED_NOT_FILLED",
            "next_required_artifact": "data/input/source_import_raw_sparc_like_v15.csv",
            "claim_boundary": "provenance_manifest_only_no_source_import_no_scores",
        }
    ]


def main() -> None:
    rows = provenance_rows()
    columns = column_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "source_import_provenance_manifest_v19.csv",
        rows,
        [
            "provenance_id",
            "galaxy_id",
            "proposed_split",
            "required_provenance_fields",
            "catalog_status",
            "file_or_table_status",
            "row_identity_status",
            "hash_or_accession_status",
            "leakage_evidence_status",
            "raw_import_allowed",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_provenance_columns_v19.csv",
        columns,
        ["field_name", "required_before_raw_import", "validation_rule", "endpoint_scoring_allowed", "claim_boundary"],
    )
    write_csv(
        DERIVED / "source_import_provenance_summary_v19.csv",
        summary_rows,
        [
            "summary_id",
            "candidate_rows",
            "provenance_complete_rows",
            "raw_import_allowed_rows",
            "required_provenance_fields",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_PROVENANCE_V19_BUILT")


if __name__ == "__main__":
    main()
