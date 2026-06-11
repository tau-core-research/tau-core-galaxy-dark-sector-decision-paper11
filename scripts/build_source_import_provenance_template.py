#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
INPUT = ROOT / "data/input"
TEMPLATE = INPUT / "source_import_provenance_evidence_v21_TEMPLATE.csv"
EVIDENCE_INPUT = INPUT / "source_import_provenance_evidence_v21.csv"

EVIDENCE_COLUMNS = [
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


def template_rows() -> list[dict[str, object]]:
    rows = read_csv(DERIVED / "source_import_provenance_manifest_v19.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        galaxy_id = row["galaxy_id"]
        out.append(
            {
                "galaxy_id": galaxy_id,
                "catalog": "FILL_SOURCE_CATALOG",
                "table_or_file": "FILL_SOURCE_TABLE_OR_FILE",
                "version_or_date": "FILL_SOURCE_VERSION_OR_DATE",
                "row_id": f"FILL_STABLE_SOURCE_ROW_ID_FOR_{galaxy_id}",
                "sha256_or_external_accession": "FILL_SHA256_OR_EXTERNAL_ACCESSION",
                "source_route": "FILL_REPRODUCIBLE_SOURCE_ROUTE",
                "leakage_evidence_id": "FILL_PRE_SCORE_LEAKAGE_EVIDENCE_ID",
                "provenance_evidence_status": "TEMPLATE_ROW_DO_NOT_IMPORT",
            }
        )
    return out


def column_rows() -> list[dict[str, object]]:
    return [
        {
            "field_name": column,
            "template_value_policy": "replace_placeholder_before_copying_to_evidence_input",
            "required_before_raw_import": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "provenance_template_column_only_no_source_claim",
        }
        for column in EVIDENCE_COLUMNS
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_TEMPLATE_V21",
            "template_file": "data/input/source_import_provenance_evidence_v21_TEMPLATE.csv",
            "target_evidence_file": "data/input/source_import_provenance_evidence_v21.csv",
            "template_rows": len(rows),
            "required_columns": len(EVIDENCE_COLUMNS),
            "evidence_input_file_present": str(EVIDENCE_INPUT.exists()).lower(),
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "PROVENANCE_TEMPLATE_READY_NOT_DATA",
            "claim_boundary": "provenance_template_only_no_source_import_no_scores",
        }
    ]


def main() -> None:
    rows = template_rows()
    columns = column_rows()
    summary_rows = summary(rows)
    write_csv(TEMPLATE, rows, EVIDENCE_COLUMNS)
    write_csv(
        DERIVED / "source_import_provenance_template_columns_v21.csv",
        columns,
        [
            "field_name",
            "template_value_policy",
            "required_before_raw_import",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_provenance_template_summary_v21.csv",
        summary_rows,
        [
            "summary_id",
            "template_file",
            "target_evidence_file",
            "template_rows",
            "required_columns",
            "evidence_input_file_present",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_PROVENANCE_TEMPLATE_V21_BUILT")


if __name__ == "__main__":
    main()
