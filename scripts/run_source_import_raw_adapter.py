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


def is_number(value: str) -> bool:
    try:
        float(value)
    except (TypeError, ValueError):
        return False
    return True


def schema_rows() -> list[dict[str, object]]:
    return [
        {
            "raw_field_name": column,
            "target_field_name": column,
            "adapter_rule": "copy_if_nonempty" if column != "v_bulge_km_s" else "copy_if_present_else_blank",
            "required_before_import": "false" if column == "v_bulge_km_s" else "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "raw_adapter_schema_only_no_observed_data_claim",
        }
        for column in RAW_COLUMNS
    ] + [
        {
            "raw_field_name": "adapter_generated",
            "target_field_name": "import_status",
            "adapter_rule": "write_IMPORTED_SOURCE_VALUE_only_after_all_required_raw_checks_pass",
            "required_before_import": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "raw_adapter_schema_only_no_observed_data_claim",
        }
    ]


def raw_status(expected_galaxies: set[str]) -> tuple[str, int, int, int]:
    if not RAW_INPUT.exists():
        return "RAW_INPUT_FILE_MISSING", 0, 0, 0
    rows = read_csv(RAW_INPUT)
    header = set(rows[0].keys()) if rows else set()
    if not set(RAW_COLUMNS).issubset(header):
        return "RAW_INPUT_HEADER_INVALID", len(rows), 0, 0
    numeric = ["radial_index", "radius_kpc", "v_obs_km_s", "sigma_v_km_s", "v_gas_km_s", "v_disk_km_s"]
    valid_rows = 0
    valid_galaxies: set[str] = set()
    for row in rows:
        galaxy_id = row.get("galaxy_id", "")
        required_present = all(row.get(column, "") != "" for column in RAW_COLUMNS if column != "v_bulge_km_s")
        numeric_ok = all(is_number(row.get(column, "")) for column in numeric)
        if galaxy_id in expected_galaxies and required_present and numeric_ok:
            valid_rows += 1
            valid_galaxies.add(galaxy_id)
    status = "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW" if valid_rows else "RAW_INPUT_PRESENT_NO_VALID_ROWS"
    return status, len(rows), valid_rows, len(valid_galaxies)


def gate_rows() -> list[dict[str, object]]:
    expected = read_csv(DERIVED / "activated_scoring_rows_v08.csv")
    expected_galaxies = {row["galaxy_id"] for row in expected}
    status, raw_rows, valid_rows, valid_galaxies = raw_status(expected_galaxies)
    return [
        {
            "adapter_gate_id": "SIRA15_RAW_TO_V12",
            "raw_input_file": "data/input/source_import_raw_sparc_like_v15.csv",
            "target_input_file": "data/input/source_import_real_values_v12.csv",
            "raw_input_status": status,
            "raw_rows_seen": raw_rows,
            "valid_raw_rows": valid_rows,
            "galaxies_with_valid_raw_rows": valid_galaxies,
            "target_file_written": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "raw_adapter_gate_only_no_source_import_no_scores",
        }
    ]


def summary(gate: list[dict[str, object]]) -> list[dict[str, object]]:
    row = gate[0]
    overall_status = (
        "RAW_ADAPTER_READY_VALIDATION_PENDING_REVIEW"
        if row["raw_input_status"] == "RAW_INPUT_PRESENT_VALIDATION_PENDING_REVIEW"
        else "RAW_ADAPTER_READY_INPUT_MISSING"
        if row["raw_input_status"] == "RAW_INPUT_FILE_MISSING"
        else "RAW_ADAPTER_BLOCKED"
    )
    return [
        {
            "summary_id": "SOURCE_IMPORT_RAW_ADAPTER_V15",
            "raw_input_file": row["raw_input_file"],
            "target_input_file": row["target_input_file"],
            "raw_input_status": row["raw_input_status"],
            "target_input_file_present": str(TARGET_INPUT.exists()).lower(),
            "target_file_written_by_adapter": row["target_file_written"],
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": overall_status,
            "claim_boundary": "raw_adapter_only_no_source_import_no_scores",
        }
    ]


def main() -> None:
    schema = schema_rows()
    gate = gate_rows()
    summary_rows = summary(gate)
    write_csv(
        DERIVED / "source_import_raw_adapter_schema_v15.csv",
        schema,
        [
            "raw_field_name",
            "target_field_name",
            "adapter_rule",
            "required_before_import",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_raw_adapter_gate_v15.csv",
        gate,
        [
            "adapter_gate_id",
            "raw_input_file",
            "target_input_file",
            "raw_input_status",
            "raw_rows_seen",
            "valid_raw_rows",
            "galaxies_with_valid_raw_rows",
            "target_file_written",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_raw_adapter_summary_v15.csv",
        summary_rows,
        [
            "summary_id",
            "raw_input_file",
            "target_input_file",
            "raw_input_status",
            "target_input_file_present",
            "target_file_written_by_adapter",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_RAW_ADAPTER_V15_BUILT")


if __name__ == "__main__":
    main()
