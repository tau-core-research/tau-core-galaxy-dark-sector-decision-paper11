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


def activation_blockers() -> list[dict[str, object]]:
    rows = read_csv(SOURCE / "source_row_audit_v05.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        blockers = []
        for key in (
            "radial_grid_status",
            "baryonic_input_status",
            "morphology_label_status",
            "response_proxy_status",
            "benchmark_input_status",
            "leakage_audit_status",
        ):
            value = row[key]
            if "PENDING" in value or "ZERO_UNLESS_NEW_SOURCE" in value:
                blockers.append(f"{key}={value}")
        out.append(
            {
                "audit_id": row["audit_id"],
                "galaxy_id": row["galaxy_id"],
                "decision_role": row["decision_role"],
                "activation_status": row["activation_status"],
                "endpoint_scoring_allowed": row["endpoint_scoring_allowed"],
                "blocker_count": len(blockers),
                "blockers": ";".join(blockers),
                "claim_boundary": "readiness_audit_only_no_endpoint_score",
            }
        )
    return out


def formula_blockers() -> list[dict[str, object]]:
    formula_rows = read_csv(SOURCE / "family_formula_table_v05.csv")
    count_rows = read_csv(SOURCE / "numeric_count_readiness_v05.csv")
    out: list[dict[str, object]] = []
    for row in formula_rows:
        out.append(
            {
                "blocker_id": row["table_id"],
                "blocker_type": "formula_table",
                "family_id": row["family_id"],
                "target": row["formula_slot"],
                "readiness_status": row["formula_table_status"],
                "endpoint_scoring_allowed": row["endpoint_scoring_allowed"],
                "blocked_by": row["next_required_artifact"],
                "claim_boundary": "formula_readiness_only_no_formula_claim",
            }
        )
    for row in count_rows:
        out.append(
            {
                "blocker_id": row["readiness_id"],
                "blocker_type": "numeric_count",
                "family_id": row["family_id"],
                "target": row["count_domain"],
                "readiness_status": row["count_readiness_status"],
                "endpoint_scoring_allowed": row["endpoint_scoring_allowed"],
                "blocked_by": row["blocked_by"],
                "claim_boundary": "count_readiness_only_no_parsimony_claim",
            }
        )
    return out


def runner_blockers() -> list[dict[str, object]]:
    rows = read_csv(SOURCE / "control_runner_contract_v04.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "runner_id": row["runner_id"],
                "control_id": row["control_id"],
                "execution_status": row["execution_status"],
                "endpoint_scoring_allowed": row["endpoint_scoring_allowed"],
                "activation_dependency": row["activation_dependency"],
                "blocking_reason": "runner_contract_declared_but_not_implemented",
                "claim_boundary": "runner_readiness_only_no_control_result",
            }
        )
    return out


def summary(
    activation_rows: list[dict[str, object]],
    formula_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    blocked_galaxies = sum(1 for row in activation_rows if row["activation_status"] == "ACTIVATION_BLOCKED")
    unfilled_formulas = sum(1 for row in formula_rows if row["blocker_type"] == "formula_table")
    blocked_counts = sum(1 for row in formula_rows if row["blocker_type"] == "numeric_count")
    unimplemented_runners = sum(1 for row in runner_rows if row["execution_status"] == "RUNNER_CONTRACT_DECLARED_NOT_IMPLEMENTED")
    endpoint_allowed = any(
        row["endpoint_scoring_allowed"] == "true"
        for rows in (activation_rows, formula_rows, runner_rows)
        for row in rows
    )
    return [
        {
            "summary_id": "READINESS_V06",
            "blocked_galaxy_rows": blocked_galaxies,
            "unfilled_formula_tables": unfilled_formulas,
            "blocked_numeric_counts": blocked_counts,
            "unimplemented_control_runners": unimplemented_runners,
            "endpoint_scoring_allowed_anywhere": str(endpoint_allowed).lower(),
            "overall_status": "ENDPOINT_SCORING_BLOCKED",
            "claim_boundary": "readiness_audit_only_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    activation_rows = activation_blockers()
    formula_rows = formula_blockers()
    runner_rows = runner_blockers()
    summary_rows = summary(activation_rows, formula_rows, runner_rows)

    write_csv(
        DERIVED / "activation_blockers_v06.csv",
        activation_rows,
        [
            "audit_id",
            "galaxy_id",
            "decision_role",
            "activation_status",
            "endpoint_scoring_allowed",
            "blocker_count",
            "blockers",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "formula_and_count_blockers_v06.csv",
        formula_rows,
        [
            "blocker_id",
            "blocker_type",
            "family_id",
            "target",
            "readiness_status",
            "endpoint_scoring_allowed",
            "blocked_by",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "control_runner_blockers_v06.csv",
        runner_rows,
        [
            "runner_id",
            "control_id",
            "execution_status",
            "endpoint_scoring_allowed",
            "activation_dependency",
            "blocking_reason",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "readiness_summary_v06.csv",
        summary_rows,
        [
            "summary_id",
            "blocked_galaxy_rows",
            "unfilled_formula_tables",
            "blocked_numeric_counts",
            "unimplemented_control_runners",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_READINESS_AUDIT_V06_BUILT")


if __name__ == "__main__":
    main()
