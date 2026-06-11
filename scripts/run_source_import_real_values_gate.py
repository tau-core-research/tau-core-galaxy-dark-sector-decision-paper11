#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
INPUT = ROOT / "data/input/source_import_real_values_v12.csv"

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


def is_number(value: str) -> bool:
    try:
        float(value)
    except (TypeError, ValueError):
        return False
    return True


def schema_rows() -> list[dict[str, object]]:
    rules = {
        "galaxy_id": "must_match_declared_scoring_galaxy",
        "radial_index": "integer_nonnegative_monotonic_within_galaxy",
        "radius_kpc": "numeric_positive",
        "v_obs_km_s": "numeric_finite_velocity_km_s",
        "sigma_v_km_s": "numeric_positive",
        "v_gas_km_s": "numeric_finite_velocity_km_s",
        "v_disk_km_s": "numeric_finite_velocity_km_s",
        "v_bulge_km_s": "numeric_finite_velocity_km_s_or_blank",
        "catalog": "nonempty_source_identifier",
        "table_or_file": "nonempty_source_table_or_file",
        "version_or_date": "nonempty_source_version_or_date",
        "row_id": "nonempty_source_row_identifier",
        "sha256_or_external_accession": "nonempty_hash_or_external_accession",
        "source_route": "nonempty_reproducible_route",
        "leakage_evidence_id": "nonempty_pre_score_leakage_evidence_reference",
        "import_status": "must_equal_IMPORTED_SOURCE_VALUE",
    }
    return [
        {
            "field_name": name,
            "validation_rule": rules[name],
            "required_before_scoring": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "schema_only_no_observed_data_claim",
        }
        for name in REQUIRED_COLUMNS
    ]


def validate_input(rows: list[dict[str, str]], expected_galaxies: set[str]) -> tuple[dict[str, int], dict[str, str]]:
    counts = {galaxy_id: 0 for galaxy_id in expected_galaxies}
    statuses = {galaxy_id: "REAL_VALUES_MISSING_FOR_GALAXY" for galaxy_id in expected_galaxies}
    numeric_required = ["radius_kpc", "v_obs_km_s", "sigma_v_km_s", "v_gas_km_s", "v_disk_km_s"]
    for row in rows:
        galaxy_id = row.get("galaxy_id", "")
        if galaxy_id not in expected_galaxies:
            continue
        required_present = all(row.get(column, "") != "" for column in REQUIRED_COLUMNS if column != "v_bulge_km_s")
        numeric_ok = all(is_number(row.get(column, "")) for column in numeric_required)
        status_ok = row.get("import_status") == "IMPORTED_SOURCE_VALUE"
        if required_present and numeric_ok and status_ok:
            counts[galaxy_id] += 1
            statuses[galaxy_id] = "REAL_VALUES_PRESENT_VALIDATION_PENDING_LEAKAGE"
        else:
            statuses[galaxy_id] = "REAL_VALUES_PRESENT_VALIDATION_FAILED"
    return counts, statuses


def gate_rows() -> list[dict[str, object]]:
    expected = read_csv(DERIVED / "activated_scoring_rows_v08.csv")
    expected_galaxies = {row["galaxy_id"] for row in expected}
    input_exists = INPUT.exists()
    header_status = "REAL_VALUE_FILE_MISSING"
    imported_rows: list[dict[str, str]] = []
    counts = {galaxy_id: 0 for galaxy_id in expected_galaxies}
    statuses = {galaxy_id: "REAL_VALUE_FILE_MISSING" for galaxy_id in expected_galaxies}
    if input_exists:
        imported_rows = read_csv(INPUT)
        header = set(imported_rows[0].keys()) if imported_rows else set()
        missing_columns = set(REQUIRED_COLUMNS) - header
        header_status = "REAL_VALUE_HEADER_OK" if not missing_columns else "REAL_VALUE_HEADER_INVALID"
        if not missing_columns:
            counts, statuses = validate_input(imported_rows, expected_galaxies)
    return [
        {
            "gate_id": row["scoring_row_id"].replace("ASR08", "SRV12"),
            "galaxy_id": row["galaxy_id"],
            "proposed_split": row["proposed_split"],
            "expected_input_file": "data/input/source_import_real_values_v12.csv",
            "input_file_status": header_status,
            "imported_numeric_rows": counts[row["galaxy_id"]],
            "real_value_gate_status": statuses[row["galaxy_id"]],
            "activation_decision": "DO_NOT_ACTIVATE",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "real_value_import_gate_only_no_scores",
        }
        for row in expected
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    imported = sum(int(row["imported_numeric_rows"]) for row in rows)
    galaxies_with_rows = sum(1 for row in rows if int(row["imported_numeric_rows"]) > 0)
    return [
        {
            "summary_id": "SOURCE_IMPORT_REAL_VALUES_GATE_V12",
            "expected_galaxy_rows": len(rows),
            "galaxies_with_imported_rows": galaxies_with_rows,
            "imported_numeric_rows": imported,
            "rows_passing_value_gate": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_REAL_VALUES_BLOCKED",
            "next_required_artifact": "data/input/source_import_real_values_v12.csv",
            "claim_boundary": "real_value_import_gate_only_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    schema = schema_rows()
    gates = gate_rows()
    summary_rows = summary(gates)
    write_csv(
        DERIVED / "source_import_real_values_schema_v12.csv",
        schema,
        ["field_name", "validation_rule", "required_before_scoring", "endpoint_scoring_allowed", "claim_boundary"],
    )
    write_csv(
        DERIVED / "source_import_real_values_gate_v12.csv",
        gates,
        [
            "gate_id",
            "galaxy_id",
            "proposed_split",
            "expected_input_file",
            "input_file_status",
            "imported_numeric_rows",
            "real_value_gate_status",
            "activation_decision",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_real_values_summary_v12.csv",
        summary_rows,
        [
            "summary_id",
            "expected_galaxy_rows",
            "galaxies_with_imported_rows",
            "imported_numeric_rows",
            "rows_passing_value_gate",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_REAL_VALUES_GATE_V12_BUILT")


if __name__ == "__main__":
    main()
