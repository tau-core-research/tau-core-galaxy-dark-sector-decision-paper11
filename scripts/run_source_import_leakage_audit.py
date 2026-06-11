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


def row_audit() -> list[dict[str, object]]:
    scoring_rows = read_csv(DERIVED / "activated_scoring_rows_v08.csv")
    observed = {row["galaxy_id"]: row for row in read_csv(DERIVED / "scoring_observed_inputs_v08.csv")}
    source_import_path = DERIVED / "source_import_table_v10.csv"
    source_import = {}
    if source_import_path.exists():
        source_import = {row["galaxy_id"]: row for row in read_csv(source_import_path)}
    source_values_path = DERIVED / "source_import_values_v11.csv"
    source_values = {}
    if source_values_path.exists():
        source_values = {row["galaxy_id"]: row for row in read_csv(source_values_path)}
    out: list[dict[str, object]] = []
    for row in scoring_rows:
        obs = observed[row["galaxy_id"]]
        source_row = source_import.get(row["galaxy_id"], {})
        source_value_row = source_values.get(row["galaxy_id"], {})
        missing = [
            field
            for field in ("radius_kpc", "v_obs_km_s", "sigma_v_km_s", "v_gas_km_s", "v_disk_km_s", "source_route")
            if obs[field] == "PENDING_SOURCE_IMPORT"
        ]
        source_status = source_value_row.get(
            "source_route_value_status",
            source_row.get("source_route_status", "SOURCE_IMPORT_PENDING"),
        )
        out.append(
            {
                "audit_id": row["scoring_row_id"].replace("ASR08", "SIL09"),
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "source_import_status": source_status,
                "missing_required_fields": ";".join(missing),
                "leakage_audit_status": "LEAKAGE_AUDIT_NOT_RUN_SOURCE_MISSING",
                "activation_decision": "DO_NOT_ACTIVATE",
                "endpoint_scoring_allowed": "false",
                "blocking_reason": "observed source import and leakage audit are incomplete",
                "claim_boundary": "source_import_leakage_audit_only_no_scores",
            }
        )
    return out


def requirements() -> list[dict[str, object]]:
    return [
        {
            "requirement_id": "SIL09_SOURCE_ROUTE",
            "required_artifact": "data/input/source_import_real_values_v12.csv",
            "purpose": "Provide reproducible source route and file/hash provenance for every activated galaxy row",
            "current_status": "REAL_VALUE_GATE_PRESENT_INPUT_MISSING",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "requirement_only_no_source_claim",
        },
        {
            "requirement_id": "SIL09_NUMERIC_OBSERVED_ROWS",
            "required_artifact": "scoring_observed_inputs_v10.csv",
            "purpose": "Replace placeholder observed rows with numeric radial-grid and baryonic-component rows",
            "current_status": "PENDING",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "requirement_only_no_observed_data_claim",
        },
        {
            "requirement_id": "SIL09_LEAKAGE_CHECK",
            "required_artifact": "leakage_audit_evidence_v10.csv",
            "purpose": "Show no endpoint residual, best-fit curve, held-out score, or family winner entered source fields",
            "current_status": "PENDING",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "requirement_only_no_leakage_pass_claim",
        },
        {
            "requirement_id": "SIL09_ACTIVATION_DECISION",
            "required_artifact": "activated_scoring_rows_v10.csv",
            "purpose": "Activate only rows that have source import, observed inputs, benchmark inputs, and leakage audit pass",
            "current_status": "PENDING",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "requirement_only_no_activation_claim",
        },
    ]


def leakage_findings(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "finding_id": row["audit_id"].replace("SIL09", "LF09"),
            "galaxy_id": row["galaxy_id"],
            "checked_fields": "source_route;observed_inputs;morphology_label;benchmark_inputs",
            "leakage_status": row["leakage_audit_status"],
            "endpoint_scoring_allowed": "false",
            "finding": "cannot pass leakage audit before source import is present",
            "claim_boundary": "leakage_placeholder_only_no_pass_claim",
        }
        for row in rows
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    source_import_blocked = sum(
        1
        for row in rows
        if row["source_import_status"] in {"SOURCE_IMPORT_PENDING", "SOURCE_ROUTE_REQUIRED_NOT_FILLED", "VALUE_REQUIRED_NOT_FILLED"}
    )
    return [
        {
            "summary_id": "SOURCE_IMPORT_LEAKAGE_AUDIT_V09",
            "audited_rows": len(rows),
            "source_import_pending_rows": source_import_blocked,
            "leakage_pass_rows": 0,
            "activated_rows": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "SOURCE_IMPORT_AND_LEAKAGE_BLOCKED",
            "next_required_artifact": "source_import_real_values_v12.csv",
            "claim_boundary": "source_import_leakage_audit_only_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    audit_rows = row_audit()
    requirement_rows = requirements()
    finding_rows = leakage_findings(audit_rows)
    summary_rows = summary(audit_rows)

    write_csv(
        DERIVED / "source_import_and_leakage_audit_v09.csv",
        audit_rows,
        [
            "audit_id",
            "galaxy_id",
            "proposed_split",
            "source_import_status",
            "missing_required_fields",
            "leakage_audit_status",
            "activation_decision",
            "endpoint_scoring_allowed",
            "blocking_reason",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_requirements_v09.csv",
        requirement_rows,
        ["requirement_id", "required_artifact", "purpose", "current_status", "endpoint_scoring_allowed", "claim_boundary"],
    )
    write_csv(
        DERIVED / "leakage_audit_findings_v09.csv",
        finding_rows,
        ["finding_id", "galaxy_id", "checked_fields", "leakage_status", "endpoint_scoring_allowed", "finding", "claim_boundary"],
    )
    write_csv(
        DERIVED / "source_import_leakage_summary_v09.csv",
        summary_rows,
        [
            "summary_id",
            "audited_rows",
            "source_import_pending_rows",
            "leakage_pass_rows",
            "activated_rows",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_LEAKAGE_AUDIT_V09_BUILT")


if __name__ == "__main__":
    main()
