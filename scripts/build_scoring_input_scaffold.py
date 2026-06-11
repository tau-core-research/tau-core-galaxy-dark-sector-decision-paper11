#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
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


def split_from_role(role: str) -> str:
    if role == "train_formula_candidate":
        return "train_candidate"
    if role == "heldout_weak_control":
        return "heldout_control_candidate"
    if role.startswith("challenge"):
        return "challenge_candidate"
    if role == "null_or_reject_current_proxy":
        return "null_control_candidate"
    if role == "beta_closure_transfer_candidate":
        return "transfer_candidate"
    return "unclassified_candidate"


def activated_rows() -> list[dict[str, object]]:
    rows = read_csv(SOURCE / "source_row_audit_v05.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "scoring_row_id": row["audit_id"].replace("SRA05", "ASR08"),
                "galaxy_id": row["galaxy_id"],
                "decision_role": row["decision_role"],
                "proposed_split": split_from_role(row["decision_role"]),
                "activation_status": "NOT_ACTIVATED",
                "endpoint_scoring_allowed": "false",
                "blocking_reason": row["blocking_reason"],
                "required_before_activation": "source_import;observed_inputs;benchmark_inputs;leakage_audit",
                "claim_boundary": "scoring_row_scaffold_only_no_endpoint_score",
            }
        )
    return out


def observed_schema() -> list[dict[str, object]]:
    fields = [
        ("galaxy_id", "string", "Galaxy identifier matching activated_scoring_rows_v08.csv", "true"),
        ("radial_index", "integer", "Stable point index on the declared radial grid", "true"),
        ("radius_kpc", "float", "Declared radius in kpc", "true"),
        ("v_obs_km_s", "float", "Observed circular velocity", "true"),
        ("sigma_v_km_s", "float", "Velocity uncertainty used by the shared score", "true"),
        ("v_gas_km_s", "float", "Gas contribution under the shared baryonic policy", "true"),
        ("v_disk_km_s", "float", "Disk contribution under the shared baryonic policy", "true"),
        ("v_bulge_km_s", "float", "Bulge contribution under the shared baryonic policy", "false"),
        ("source_route", "string", "Reproducible source route for the row", "true"),
        ("leakage_audit_status", "string", "Leakage status before scoring activation", "true"),
    ]
    return [
        {
            "field_name": name,
            "field_type": field_type,
            "definition": definition,
            "required_before_scoring": required,
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "schema_only_no_observed_data_claim",
        }
        for name, field_type, definition, required in fields
    ]


def observed_inputs(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "galaxy_id": row["galaxy_id"],
                "radial_index": "PENDING_SOURCE_IMPORT",
                "radius_kpc": "PENDING_SOURCE_IMPORT",
                "v_obs_km_s": "PENDING_SOURCE_IMPORT",
                "sigma_v_km_s": "PENDING_SOURCE_IMPORT",
                "v_gas_km_s": "PENDING_SOURCE_IMPORT",
                "v_disk_km_s": "PENDING_SOURCE_IMPORT",
                "v_bulge_km_s": "PENDING_SOURCE_IMPORT",
                "source_route": "PENDING_SOURCE_IMPORT",
                "leakage_audit_status": "LEAKAGE_AUDIT_PENDING",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "placeholder_row_only_no_observed_data",
            }
        )
    return out


def summary(rows: list[dict[str, object]], observed: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "SCORING_INPUT_SCAFFOLD_V08",
            "scoring_rows_declared": len(rows),
            "activated_rows": sum(1 for row in rows if row["activation_status"] == "ACTIVATED"),
            "observed_input_rows": len(observed),
            "observed_numeric_rows": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "INPUT_SCAFFOLD_READY_DATA_MISSING",
            "next_required_artifact": "source_import_and_leakage_audit_v09.csv",
            "claim_boundary": "scoring_input_scaffold_only_no_scores",
        }
    ]


def main() -> None:
    scoring_rows = activated_rows()
    schema_rows = observed_schema()
    observed_rows = observed_inputs(scoring_rows)
    summary_rows = summary(scoring_rows, observed_rows)

    write_csv(
        DERIVED / "activated_scoring_rows_v08.csv",
        scoring_rows,
        [
            "scoring_row_id",
            "galaxy_id",
            "decision_role",
            "proposed_split",
            "activation_status",
            "endpoint_scoring_allowed",
            "blocking_reason",
            "required_before_activation",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_observed_input_schema_v08.csv",
        schema_rows,
        [
            "field_name",
            "field_type",
            "definition",
            "required_before_scoring",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_observed_inputs_v08.csv",
        observed_rows,
        [
            "galaxy_id",
            "radial_index",
            "radius_kpc",
            "v_obs_km_s",
            "sigma_v_km_s",
            "v_gas_km_s",
            "v_disk_km_s",
            "v_bulge_km_s",
            "source_route",
            "leakage_audit_status",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "scoring_input_scaffold_summary_v08.csv",
        summary_rows,
        [
            "summary_id",
            "scoring_rows_declared",
            "activated_rows",
            "observed_input_rows",
            "observed_numeric_rows",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SCORING_INPUT_SCAFFOLD_V08_BUILT")


if __name__ == "__main__":
    main()
