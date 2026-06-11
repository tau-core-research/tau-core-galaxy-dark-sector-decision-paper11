#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"


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


def source_values() -> list[dict[str, object]]:
    rows = read_csv(DERIVED / "source_import_table_v10.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "source_value_id": row["source_import_id"].replace("SIT10", "SIV11"),
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "catalog": "VALUE_REQUIRED_NOT_FILLED",
                "table_or_file": "VALUE_REQUIRED_NOT_FILLED",
                "version_or_date": "VALUE_REQUIRED_NOT_FILLED",
                "row_id": "VALUE_REQUIRED_NOT_FILLED",
                "sha256_or_external_accession": "VALUE_REQUIRED_NOT_FILLED",
                "source_route_value_status": "VALUE_REQUIRED_NOT_FILLED",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "source_import_values_placeholder_only_no_data",
            }
        )
    return out


def observed_values() -> list[dict[str, object]]:
    rows = read_csv(DERIVED / "activated_scoring_rows_v08.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "observed_value_id": row["scoring_row_id"].replace("ASR08", "OIV11"),
                "galaxy_id": row["galaxy_id"],
                "radial_index": "VALUE_REQUIRED_NOT_FILLED",
                "radius_kpc": "VALUE_REQUIRED_NOT_FILLED",
                "v_obs_km_s": "VALUE_REQUIRED_NOT_FILLED",
                "sigma_v_km_s": "VALUE_REQUIRED_NOT_FILLED",
                "v_gas_km_s": "VALUE_REQUIRED_NOT_FILLED",
                "v_disk_km_s": "VALUE_REQUIRED_NOT_FILLED",
                "v_bulge_km_s": "OPTIONAL_VALUE_NOT_FILLED",
                "observed_value_status": "VALUE_REQUIRED_NOT_FILLED",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "observed_values_placeholder_only_no_data",
            }
        )
    return out


def leakage_values() -> list[dict[str, object]]:
    rows = read_csv(DERIVED / "leakage_evidence_contract_v10.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "leakage_value_id": row["evidence_id"].replace("LEC10", "LEV11"),
                "checked_object": row["checked_object"],
                "evidence_value": "VALUE_REQUIRED_NOT_FILLED",
                "evidence_status": "VALUE_REQUIRED_NOT_FILLED",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_evidence_placeholder_only_no_pass_claim",
            }
        )
    return out


def summary(source_rows: list[dict[str, object]], observed_rows: list[dict[str, object]], leakage_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "SOURCE_IMPORT_VALUES_V11",
            "source_value_rows": len(source_rows),
            "source_routes_filled": 0,
            "observed_value_rows": len(observed_rows),
            "observed_numeric_rows_filled": 0,
            "leakage_evidence_rows": len(leakage_rows),
            "leakage_evidence_filled": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_VALUES_DECLARED_NOT_FILLED",
            "next_required_artifact": "source_import_real_values_v12.csv",
            "claim_boundary": "source_import_values_placeholder_only_no_scores",
        }
    ]


def main() -> None:
    source_rows = source_values()
    observed_rows = observed_values()
    leakage_rows = leakage_values()
    summary_rows = summary(source_rows, observed_rows, leakage_rows)
    write_csv(
        DERIVED / "source_import_values_v11.csv",
        source_rows,
        [
            "source_value_id",
            "galaxy_id",
            "proposed_split",
            "catalog",
            "table_or_file",
            "version_or_date",
            "row_id",
            "sha256_or_external_accession",
            "source_route_value_status",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "observed_numeric_values_v11.csv",
        observed_rows,
        [
            "observed_value_id",
            "galaxy_id",
            "radial_index",
            "radius_kpc",
            "v_obs_km_s",
            "sigma_v_km_s",
            "v_gas_km_s",
            "v_disk_km_s",
            "v_bulge_km_s",
            "observed_value_status",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_evidence_values_v11.csv",
        leakage_rows,
        [
            "leakage_value_id",
            "checked_object",
            "evidence_value",
            "evidence_status",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_values_summary_v11.csv",
        summary_rows,
        [
            "summary_id",
            "source_value_rows",
            "source_routes_filled",
            "observed_value_rows",
            "observed_numeric_rows_filled",
            "leakage_evidence_rows",
            "leakage_evidence_filled",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_VALUES_V11_BUILT")


if __name__ == "__main__":
    main()
