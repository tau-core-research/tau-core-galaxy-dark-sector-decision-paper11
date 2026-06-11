#!/usr/bin/env python3
from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
RESPONSE_DIR = ROOT / "review_packages/frontier_provenance_v46_completed_review_response"
RESPONSE_ZIP = ROOT / "review_packages/frontier_provenance_v46_completed_review_response.zip"

REQUIRED_RESPONSE_FILES = {
    "frontier_provenance_v46_review_response.csv",
    "frontier_provenance_v46_review_completed_summary.csv",
    "frontier_provenance_v46_review_notes.md",
    "frontier_provenance_v46_review_validation_log.txt",
}


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


def response_rows() -> list[dict[str, object]]:
    rows = read_csv(RESPONSE_DIR / "frontier_provenance_v46_review_response.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "review_id": row["review_id"],
                "galaxy_id": row["galaxy_id"],
                "row_route_internal_consistency": row["row_route_internal_consistency"],
                "source_hash_route_status": row["source_hash_route_status"],
                "leakage_evidence_status": row["leakage_evidence_status"],
                "reviewer_decision": row["reviewer_decision"],
                "may_copy_to_v21_after_review": row["may_copy_to_v21_after_review"],
                "may_mark_provenance_complete": row["may_mark_provenance_complete"],
                "endpoint_scoring_allowed": row["endpoint_scoring_allowed"],
                "claim_boundary": row["claim_boundary"],
            }
        )
    return out


def zip_file_count() -> int:
    with zipfile.ZipFile(RESPONSE_ZIP) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    return len(names & REQUIRED_RESPONSE_FILES)


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    source_summary = read_csv(RESPONSE_DIR / "frontier_provenance_v46_review_completed_summary.csv")[0]
    log_text = (RESPONSE_DIR / "frontier_provenance_v46_review_validation_log.txt").read_text(encoding="utf-8")
    notes_text = (RESPONSE_DIR / "frontier_provenance_v46_review_notes.md").read_text(encoding="utf-8")
    pass_rows = sum(
        row["row_route_internal_consistency"] == "pass" and row["leakage_evidence_status"] == "pass_prescore_source_route_review_id"
        for row in rows
    )
    return [
        {
            "summary_id": "FRONTIER_PROVENANCE_REVIEW_RESPONSE_INTAKE_V48",
            "response_zip": "review_packages/frontier_provenance_v46_completed_review_response.zip",
            "response_files_present": zip_file_count(),
            "review_rows": len(rows),
            "route_and_prescore_pass_rows": pass_rows,
            "review_decision": source_summary["decision"],
            "completion_status": "PASS_WITH_CAVEAT" if "PASS_WITH_CAVEAT" in log_text else "UNKNOWN",
            "external_hash_recomputed": "false" if "not recomputed" in notes_text or "not independently recomputed" in notes_text else "unknown",
            "complete_evidence_rows_authorized": source_summary["complete_evidence_rows_authorized"],
            "v21_evidence_rows_created": source_summary["v21_evidence_rows_created"],
            "may_copy_to_v21_without_separate_promotion": source_summary["may_copy_to_v21_without_separate_promotion"],
            "endpoint_scoring_allowed_anywhere": source_summary["endpoint_scoring_allowed"],
            "overall_status": "REVIEW_RESPONSE_ACCEPTED_AS_DRAFT_ONLY_NOT_PROMOTED",
            "claim_boundary": "frontier_provenance_review_response_intake_only_no_v21_write_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = response_rows()
    write_csv(
        DERIVED / "frontier_provenance_review_response_intake_v48.csv",
        rows,
        [
            "review_id",
            "galaxy_id",
            "row_route_internal_consistency",
            "source_hash_route_status",
            "leakage_evidence_status",
            "reviewer_decision",
            "may_copy_to_v21_after_review",
            "may_mark_provenance_complete",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_provenance_review_response_intake_summary_v48.csv",
        summary(rows),
        [
            "summary_id",
            "response_zip",
            "response_files_present",
            "review_rows",
            "route_and_prescore_pass_rows",
            "review_decision",
            "completion_status",
            "external_hash_recomputed",
            "complete_evidence_rows_authorized",
            "v21_evidence_rows_created",
            "may_copy_to_v21_without_separate_promotion",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_FRONTIER_PROVENANCE_REVIEW_RESPONSE_INTAKE_V48_BUILT")


if __name__ == "__main__":
    main()
