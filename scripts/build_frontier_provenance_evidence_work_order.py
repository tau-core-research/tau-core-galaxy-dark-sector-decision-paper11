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
    acceptance = read_csv(DERIVED / "frontier_provenance_evidence_acceptance_v26.csv")
    rows: list[dict[str, object]] = []
    for index, row in enumerate(acceptance, start=1):
        rows.append(
            {
                "work_order_id": f"FPEW27_{index:03d}",
                "galaxy_id": row["galaxy_id"],
                "frontier_dependency": row["frontier_dependency"],
                "target_evidence_artifact": row["frontier_artifact"],
                "required_fields": row["required_fields"],
                "minimum_source_tasks": (
                    "identify_catalog;"
                    "identify_table_or_file;"
                    "record_version_or_date;"
                    "record_stable_row_id;"
                    "record_sha256_or_external_accession;"
                    "record_reproducible_source_route;"
                    "record_pre_score_leakage_evidence_id;"
                    "set_PROVENANCE_EVIDENCE_COMPLETE_only_after_review"
                ),
                "current_acceptance_status": row["acceptance_status"],
                "work_order_status": "OPEN_EVIDENCE_COLLECTION_REQUIRED",
                "may_write_evidence_input": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "frontier_work_order_only_no_evidence_no_source_import_no_scores",
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    open_rows = sum(row["work_order_status"] == "OPEN_EVIDENCE_COLLECTION_REQUIRED" for row in rows)
    return [
        {
            "summary_id": "FRONTIER_PROVENANCE_EVIDENCE_WORK_ORDER_V27",
            "work_order_rows": len(rows),
            "open_work_order_rows": open_rows,
            "closed_work_order_rows": len(rows) - open_rows,
            "target_evidence_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "may_write_evidence_input_anywhere": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_WORK_ORDER_OPEN",
            "claim_boundary": "frontier_work_order_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = work_order_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "frontier_provenance_evidence_work_order_v27.csv",
        rows,
        [
            "work_order_id",
            "galaxy_id",
            "frontier_dependency",
            "target_evidence_artifact",
            "required_fields",
            "minimum_source_tasks",
            "current_acceptance_status",
            "work_order_status",
            "may_write_evidence_input",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_provenance_evidence_work_order_summary_v27.csv",
        summary_rows,
        [
            "summary_id",
            "work_order_rows",
            "open_work_order_rows",
            "closed_work_order_rows",
            "target_evidence_artifact",
            "may_write_evidence_input_anywhere",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_FRONTIER_PROVENANCE_EVIDENCE_WORK_ORDER_V27_BUILT")


if __name__ == "__main__":
    main()
