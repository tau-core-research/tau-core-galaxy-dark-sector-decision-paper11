#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
INPUT = ROOT / "data/input"
TEMPLATE = INPUT / "source_import_real_values_v12_TEMPLATE.csv"
REAL_INPUT = INPUT / "source_import_real_values_v12.csv"

REQUIRED_COLUMNS = [
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
    "import_status",
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
    scoring_rows = read_csv(DERIVED / "activated_scoring_rows_v08.csv")
    rows: list[dict[str, object]] = []
    for row in scoring_rows:
        galaxy_id = row["galaxy_id"]
        rows.append(
            {
                "galaxy_id": galaxy_id,
                "radial_index": "FILL_INTEGER_INDEX_PER_RADIAL_POINT",
                "radius_kpc": "FILL_NUMERIC_RADIUS_KPC",
                "v_obs_km_s": "FILL_NUMERIC_OBSERVED_VELOCITY",
                "sigma_v_km_s": "FILL_NUMERIC_UNCERTAINTY",
                "v_gas_km_s": "FILL_NUMERIC_GAS_COMPONENT",
                "v_disk_km_s": "FILL_NUMERIC_DISK_COMPONENT",
                "v_bulge_km_s": "FILL_NUMERIC_BULGE_COMPONENT_OR_BLANK",
                "catalog": "FILL_SOURCE_CATALOG",
                "table_or_file": "FILL_SOURCE_TABLE_OR_FILE",
                "version_or_date": "FILL_SOURCE_VERSION_OR_DATE",
                "row_id": f"FILL_SOURCE_ROW_ID_FOR_{galaxy_id}",
                "sha256_or_external_accession": "FILL_HASH_OR_EXTERNAL_ACCESSION",
                "source_route": "FILL_REPRODUCIBLE_SOURCE_ROUTE",
                "leakage_evidence_id": "FILL_PRE_SCORE_LEAKAGE_EVIDENCE_ID",
                "import_status": "TEMPLATE_ROW_DO_NOT_IMPORT",
            }
        )
    return rows


def column_rows() -> list[dict[str, object]]:
    schema = {row["field_name"]: row for row in read_csv(DERIVED / "source_import_real_values_schema_v12.csv")}
    return [
        {
            "field_name": column,
            "validation_rule": schema[column]["validation_rule"],
            "template_value_policy": "replace_placeholder_before_copying_to_real_input",
            "required_before_scoring": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "template_column_only_no_observed_data_claim",
        }
        for column in REQUIRED_COLUMNS
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "SOURCE_IMPORT_TEMPLATE_V14",
            "template_file": "data/input/source_import_real_values_v12_TEMPLATE.csv",
            "target_real_input_file": "data/input/source_import_real_values_v12.csv",
            "template_rows": len(rows),
            "required_columns": len(REQUIRED_COLUMNS),
            "real_input_file_present": str(REAL_INPUT.exists()).lower(),
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_TEMPLATE_READY_NOT_DATA",
            "claim_boundary": "template_only_no_source_import_no_scores",
        }
    ]


def main() -> None:
    rows = template_rows()
    columns = column_rows()
    summary_rows = summary(rows)
    write_csv(TEMPLATE, rows, REQUIRED_COLUMNS)
    write_csv(
        DERIVED / "source_import_template_columns_v14.csv",
        columns,
        [
            "field_name",
            "validation_rule",
            "template_value_policy",
            "required_before_scoring",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_template_summary_v14.csv",
        summary_rows,
        [
            "summary_id",
            "template_file",
            "target_real_input_file",
            "template_rows",
            "required_columns",
            "real_input_file_present",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_TEMPLATE_V14_BUILT")


if __name__ == "__main__":
    main()
