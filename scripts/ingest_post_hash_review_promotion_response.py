#!/usr/bin/env python3
from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
RESPONSE_DIR = ROOT / "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response"
RESPONSE_ZIP = ROOT / "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response.zip"

REQUIRED_RESPONSE_FILES = {
    "frontier_post_hash_review_promotion_v51_authorization_response.csv",
    "frontier_post_hash_review_promotion_v51_completed_summary.csv",
    "frontier_post_hash_review_promotion_v51_review_notes.md",
    "frontier_post_hash_review_promotion_v51_validation_log.txt",
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


def zip_file_count() -> int:
    with zipfile.ZipFile(RESPONSE_ZIP) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    return len(names & REQUIRED_RESPONSE_FILES)


def response_rows() -> list[dict[str, object]]:
    rows = read_csv(RESPONSE_DIR / "frontier_post_hash_review_promotion_v51_authorization_response.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "review_id": row["review_id"],
                "galaxy_id": row["galaxy_id"],
                "primary_table1_hash_recomputed_matched": row["primary_table1_hash_recomputed_matched"],
                "current_recheck_decision": row["current_recheck_decision"],
                "reviewer_promotion_decision": row["reviewer_promotion_decision"],
                "may_copy_to_v21_after_authorization": row["may_copy_to_v21_after_authorization"],
                "may_mark_provenance_complete_after_authorization": row["may_mark_provenance_complete_after_authorization"],
                "endpoint_scoring_allowed": row["endpoint_scoring_allowed"],
                "reviewer_notes": row["reviewer_notes"],
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    source_summary = read_csv(RESPONSE_DIR / "frontier_post_hash_review_promotion_v51_completed_summary.csv")[0]
    promoted = sum(row["reviewer_promotion_decision"] == "PROMOTE_TO_COMPLETE_V21_EVIDENCE" for row in rows)
    copy_allowed = sum(row["may_copy_to_v21_after_authorization"] == "true" for row in rows)
    complete_allowed = sum(row["may_mark_provenance_complete_after_authorization"] == "true" for row in rows)
    hash_matched = sum(row["primary_table1_hash_recomputed_matched"] == "true" for row in rows)
    scoring_allowed = any(row["endpoint_scoring_allowed"] == "true" for row in rows)
    return [
        {
            "summary_id": "POST_HASH_REVIEW_PROMOTION_RESPONSE_INTAKE_V53",
            "response_zip": "review_packages/frontier_post_hash_review_promotion_v51_completed_review_response.zip",
            "response_files_present": zip_file_count(),
            "review_rows": len(rows),
            "promote_to_complete_v21_evidence_rows": promoted,
            "copy_to_v21_authorized_rows": copy_allowed,
            "provenance_complete_authorized_rows": complete_allowed,
            "primary_hash_matched_rows": hash_matched,
            "source_decision": source_summary["decision"],
            "v21_evidence_rows_created_by_response": source_summary["v21_evidence_rows_created_by_this_package"],
            "provenance_complete_rows_marked_by_response": source_summary["provenance_complete_rows_marked_by_this_package"],
            "endpoint_scoring_allowed_anywhere": str(scoring_allowed).lower(),
            "overall_status": "POST_HASH_REVIEW_PROMOTION_AUTHORIZATION_ACCEPTED_FOR_INGESTION"
            if promoted == len(rows) and copy_allowed == len(rows) and complete_allowed == len(rows) and hash_matched == len(rows) and not scoring_allowed
            else "POST_HASH_REVIEW_PROMOTION_AUTHORIZATION_BLOCKED",
            "claim_boundary": "post_hash_review_promotion_response_intake_only_no_v21_write_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = response_rows()
    write_csv(
        DERIVED / "post_hash_review_promotion_response_intake_v53.csv",
        rows,
        [
            "review_id",
            "galaxy_id",
            "primary_table1_hash_recomputed_matched",
            "current_recheck_decision",
            "reviewer_promotion_decision",
            "may_copy_to_v21_after_authorization",
            "may_mark_provenance_complete_after_authorization",
            "endpoint_scoring_allowed",
            "reviewer_notes",
        ],
    )
    write_csv(
        DERIVED / "post_hash_review_promotion_response_intake_summary_v53.csv",
        summary(rows),
        [
            "summary_id",
            "response_zip",
            "response_files_present",
            "review_rows",
            "promote_to_complete_v21_evidence_rows",
            "copy_to_v21_authorized_rows",
            "provenance_complete_authorized_rows",
            "primary_hash_matched_rows",
            "source_decision",
            "v21_evidence_rows_created_by_response",
            "provenance_complete_rows_marked_by_response",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_HASH_REVIEW_PROMOTION_RESPONSE_INTAKE_V53_BUILT")


if __name__ == "__main__":
    main()
