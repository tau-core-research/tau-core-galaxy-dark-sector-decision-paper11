#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"

V21_COLUMNS = [
    "galaxy_id",
    "catalog",
    "table_or_file",
    "version_or_date",
    "row_id",
    "sha256_or_external_accession",
    "source_route",
    "leakage_evidence_id",
    "provenance_evidence_status",
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


def source_by_id() -> dict[str, dict[str, str]]:
    return {
        row["source_candidate_id"]: row
        for row in read_csv(DERIVED / "frontier_provenance_source_candidate_ledger_v45.csv")
    }


def draft_rows() -> list[dict[str, object]]:
    sources = source_by_id()
    coverage = read_csv(DERIVED / "frontier_provenance_source_candidate_coverage_v45.csv")
    out: list[dict[str, object]] = []
    for row in coverage:
        source = sources[row["primary_source_candidate_id"]]
        out.append(
            {
                "galaxy_id": row["galaxy_id"],
                "catalog": source["catalog"],
                "table_or_file": source["table_or_file"],
                "version_or_date": source["version_or_date"],
                "row_id": row["candidate_row_id_rule"],
                "sha256_or_external_accession": source["sha256_or_external_accession"],
                "source_route": row["candidate_source_route"],
                "leakage_evidence_id": row["candidate_leakage_evidence_id"],
                "provenance_evidence_status": "REVIEW_REQUIRED_NOT_COMPLETE",
            }
        )
    return out


def review_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "review_id": f"FPEPD46_REVIEW_{index:03d}",
            "galaxy_id": row["galaxy_id"],
            "draft_source": "data/derived/frontier_provenance_evidence_payload_draft_v46.csv",
            "target_evidence_file": "data/input/source_import_provenance_evidence_v21.csv",
            "review_required": "true",
            "required_review_action": "verify_source_row_route_and_leakage_evidence_before_status_complete",
            "may_copy_to_v21_after_review": "false",
            "may_mark_complete_without_review": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "frontier_provenance_evidence_payload_draft_review_only_no_scores",
        }
        for index, row in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    complete = sum(row["provenance_evidence_status"] == "PROVENANCE_EVIDENCE_COMPLETE" for row in rows)
    return [
        {
            "summary_id": "FRONTIER_PROVENANCE_EVIDENCE_PAYLOAD_DRAFT_V46",
            "draft_rows": len(rows),
            "draft_rows_requiring_review": len(rows) - complete,
            "complete_evidence_rows": complete,
            "v21_evidence_rows_created": "0",
            "may_copy_to_v21_without_review": "false",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_PAYLOAD_DRAFT_READY_REVIEW_REQUIRED",
            "claim_boundary": "frontier_provenance_evidence_payload_draft_only_no_v21_write_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = draft_rows()
    write_csv(DERIVED / "frontier_provenance_evidence_payload_draft_v46.csv", rows, V21_COLUMNS)
    write_csv(
        DERIVED / "frontier_provenance_evidence_payload_draft_review_v46.csv",
        review_rows(rows),
        [
            "review_id",
            "galaxy_id",
            "draft_source",
            "target_evidence_file",
            "review_required",
            "required_review_action",
            "may_copy_to_v21_after_review",
            "may_mark_complete_without_review",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_provenance_evidence_payload_draft_summary_v46.csv",
        summary(rows),
        [
            "summary_id",
            "draft_rows",
            "draft_rows_requiring_review",
            "complete_evidence_rows",
            "v21_evidence_rows_created",
            "may_copy_to_v21_without_review",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_FRONTIER_PROVENANCE_EVIDENCE_PAYLOAD_DRAFT_V46_BUILT")


if __name__ == "__main__":
    main()
