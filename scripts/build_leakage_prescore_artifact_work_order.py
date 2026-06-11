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


def work_order_rows() -> list[dict[str, object]]:
    intake_rows = read_csv(DERIVED / "leakage_audit_review_response_intake_v60.csv")
    out: list[dict[str, object]] = []
    for row in intake_rows:
        source_artifact_missing = row["source_artifact"] == "FILL_REVIEWED_PRESCORE_SOURCE_OR_PROTOCOL_ARTIFACT"
        out.append(
            {
                "work_order_id": row["leakage_evidence_row_id"].replace("LAET58", "LPAWO61"),
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "checked_object": row["checked_object"],
                "required_prescore_artifact": required_prescore_artifact(row["evidence_id"]),
                "current_source_artifact": row["source_artifact"],
                "review_decision": row["review_decision"],
                "artifact_collection_status": "OPEN_PRESCORE_ARTIFACT_REQUIRED"
                if source_artifact_missing
                else "PRESCORE_ARTIFACT_PRESENT_REVIEW_REQUIRED",
                "may_create_leakage_evidence_after_work_order": "false",
                "may_activate_row_after_work_order": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_prescore_artifact_work_order_only_no_evidence_no_scores",
            }
        )
    return out


def required_prescore_artifact(evidence_id: str) -> str:
    mapping = {
        "LEC10_SOURCE_ROUTE": "reviewed_prescore_source_route_artifact",
        "LEC10_OBSERVED_INPUTS": "reviewed_prescore_observed_input_import_artifact",
        "LEC10_MORPH_LABELS": "reviewed_prescore_morphology_label_artifact",
        "LEC10_BENCHMARK_INPUTS": "reviewed_prescore_benchmark_policy_artifact",
    }
    return mapping[evidence_id]


def coverage_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    evidence_ids = sorted({str(row["evidence_id"]) for row in rows})
    for evidence_id in evidence_ids:
        subset = [row for row in rows if row["evidence_id"] == evidence_id]
        open_rows = sum(row["artifact_collection_status"] == "OPEN_PRESCORE_ARTIFACT_REQUIRED" for row in subset)
        out.append(
            {
                "coverage_id": f"LPAWO61_{evidence_id}",
                "evidence_id": evidence_id,
                "required_prescore_artifact": required_prescore_artifact(evidence_id),
                "galaxy_rows": len(subset),
                "open_prescore_artifact_rows": open_rows,
                "ready_for_leakage_evidence_rows": 0,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_prescore_artifact_work_order_coverage_only_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    open_rows = sum(row["artifact_collection_status"] == "OPEN_PRESCORE_ARTIFACT_REQUIRED" for row in rows)
    return [
        {
            "summary_id": "LEAKAGE_PRESCORE_ARTIFACT_WORK_ORDER_V61",
            "work_order_rows": len(rows),
            "galaxies_covered": len({row["galaxy_id"] for row in rows}),
            "evidence_checks_per_galaxy": 4,
            "open_prescore_artifact_rows": open_rows,
            "ready_for_leakage_evidence_rows": 0,
            "leakage_pass_rows_created": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "LEAKAGE_PRESCORE_ARTIFACT_WORK_ORDER_OPEN",
            "next_required_artifact": "reviewed_prescore_source_or_protocol_artifacts_for_v61",
            "claim_boundary": "leakage_prescore_artifact_work_order_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = work_order_rows()
    coverage = coverage_rows(rows)
    write_csv(
        DERIVED / "leakage_prescore_artifact_work_order_v61.csv",
        rows,
        [
            "work_order_id",
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "checked_object",
            "required_prescore_artifact",
            "current_source_artifact",
            "review_decision",
            "artifact_collection_status",
            "may_create_leakage_evidence_after_work_order",
            "may_activate_row_after_work_order",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_prescore_artifact_work_order_coverage_v61.csv",
        coverage,
        [
            "coverage_id",
            "evidence_id",
            "required_prescore_artifact",
            "galaxy_rows",
            "open_prescore_artifact_rows",
            "ready_for_leakage_evidence_rows",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_prescore_artifact_work_order_summary_v61.csv",
        summary(rows),
        [
            "summary_id",
            "work_order_rows",
            "galaxies_covered",
            "evidence_checks_per_galaxy",
            "open_prescore_artifact_rows",
            "ready_for_leakage_evidence_rows",
            "leakage_pass_rows_created",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_LEAKAGE_PRESCORE_ARTIFACT_WORK_ORDER_V61_BUILT")


if __name__ == "__main__":
    main()
