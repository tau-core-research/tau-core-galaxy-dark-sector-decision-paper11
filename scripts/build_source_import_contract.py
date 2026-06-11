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


def source_import_rows() -> list[dict[str, object]]:
    scoring_rows = read_csv(DERIVED / "activated_scoring_rows_v08.csv")
    out: list[dict[str, object]] = []
    for row in scoring_rows:
        out.append(
            {
                "source_import_id": row["scoring_row_id"].replace("ASR08", "SIT10"),
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "required_source_family": "rotation_curve_plus_baryonic_components",
                "source_route_status": "SOURCE_ROUTE_REQUIRED_NOT_FILLED",
                "required_provenance_fields": "catalog;table_or_file;version_or_date;row_id;sha256_or_external_accession",
                "required_numeric_fields": "radius_kpc;v_obs_km_s;sigma_v_km_s;v_gas_km_s;v_disk_km_s",
                "optional_numeric_fields": "v_bulge_km_s",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "source_import_contract_only_no_observed_data",
            }
        )
    return out


def observed_input_contract() -> list[dict[str, object]]:
    fields = read_csv(DERIVED / "scoring_observed_input_schema_v08.csv")
    out: list[dict[str, object]] = []
    for row in fields:
        out.append(
            {
                "contract_id": f"OIC10_{row['field_name'].upper()}",
                "field_name": row["field_name"],
                "field_type": row["field_type"],
                "required_before_scoring": row["required_before_scoring"],
                "validation_rule": validation_rule(row["field_name"]),
                "source_import_status": "CONTRACT_DECLARED_VALUE_PENDING",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "observed_input_contract_only_no_values",
            }
        )
    return out


def validation_rule(field_name: str) -> str:
    numeric_positive = {"radius_kpc", "sigma_v_km_s"}
    numeric_velocity = {"v_obs_km_s", "v_gas_km_s", "v_disk_km_s", "v_bulge_km_s"}
    if field_name == "galaxy_id":
        return "must_match_activated_scoring_rows_v08"
    if field_name == "radial_index":
        return "integer_nonnegative_monotonic_within_galaxy"
    if field_name in numeric_positive:
        return "numeric_positive"
    if field_name in numeric_velocity:
        return "numeric_finite_velocity_km_s"
    if field_name == "source_route":
        return "nonempty_reproducible_route_with_provenance"
    if field_name == "leakage_audit_status":
        return "must_be_leakage_audit_pass_before_activation"
    return "nonempty_if_required"


def leakage_evidence_contract() -> list[dict[str, object]]:
    return [
        {
            "evidence_id": "LEC10_SOURCE_ROUTE",
            "checked_object": "source_route",
            "required_evidence": "source route chosen before endpoint score visibility",
            "status": "EVIDENCE_REQUIRED_NOT_FILLED",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "leakage_contract_only_no_pass_claim",
        },
        {
            "evidence_id": "LEC10_OBSERVED_INPUTS",
            "checked_object": "observed_input_rows",
            "required_evidence": "observed values imported from source files without endpoint-derived edits",
            "status": "EVIDENCE_REQUIRED_NOT_FILLED",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "leakage_contract_only_no_pass_claim",
        },
        {
            "evidence_id": "LEC10_MORPH_LABELS",
            "checked_object": "morphology_readout_labels",
            "required_evidence": "labels assigned from source-side observables and not residual/best-fit curves",
            "status": "EVIDENCE_REQUIRED_NOT_FILLED",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "leakage_contract_only_no_pass_claim",
        },
        {
            "evidence_id": "LEC10_BENCHMARK_INPUTS",
            "checked_object": "benchmark_profile_inputs",
            "required_evidence": "benchmark priors and nuisance policies frozen before family comparison",
            "status": "EVIDENCE_REQUIRED_NOT_FILLED",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "leakage_contract_only_no_pass_claim",
        },
    ]


def summary(source_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "SOURCE_IMPORT_CONTRACT_V10",
            "source_import_rows": len(source_rows),
            "source_routes_filled": 0,
            "numeric_observed_rows_filled": 0,
            "leakage_evidence_filled": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_CONTRACT_READY_VALUES_MISSING",
            "next_required_artifact": "source_import_values_v11.csv",
            "claim_boundary": "source_import_contract_only_no_scores",
        }
    ]


def main() -> None:
    source_rows = source_import_rows()
    observed_rows = observed_input_contract()
    leakage_rows = leakage_evidence_contract()
    summary_rows = summary(source_rows)
    write_csv(
        DERIVED / "source_import_table_v10.csv",
        source_rows,
        [
            "source_import_id",
            "galaxy_id",
            "proposed_split",
            "required_source_family",
            "source_route_status",
            "required_provenance_fields",
            "required_numeric_fields",
            "optional_numeric_fields",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "observed_input_contract_v10.csv",
        observed_rows,
        [
            "contract_id",
            "field_name",
            "field_type",
            "required_before_scoring",
            "validation_rule",
            "source_import_status",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_evidence_contract_v10.csv",
        leakage_rows,
        ["evidence_id", "checked_object", "required_evidence", "status", "endpoint_scoring_allowed", "claim_boundary"],
    )
    write_csv(
        DERIVED / "source_import_contract_summary_v10.csv",
        summary_rows,
        [
            "summary_id",
            "source_import_rows",
            "source_routes_filled",
            "numeric_observed_rows_filled",
            "leakage_evidence_filled",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_CONTRACT_V10_BUILT")


if __name__ == "__main__":
    main()
